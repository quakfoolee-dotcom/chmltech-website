"""OEE reference dataset, reference calculator and error study (Chmltech Online Journal, Vol. 106, Issue 17).

Builds a four-week MES extract for a composite three-line bottling plant in Vancouver:
  shifts.csv   one row per line and shift: shift length, planned downtime, counts by SKU (produced, rejects, reworked)
  stops.csv    unplanned stop events with start and end minute; some stops are logged twice by two sources
  skus.csv     ideal rate per SKU (bottles per minute)
then computes OEE the reference way (ISO 22400-2 element definitions, pooled aggregation) and the eight
common calculation errors studied in the paper, and writes a 24-question test set with reference answers.

Usage: python3 oee_reference.py   ->  data/*.csv, results.json, questions.json
Needs numpy. Overwrites the shipped data and answers; numpy does not guarantee identical random streams across versions.
"""
import csv, json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
SKUS = {'B500': 120.0, 'B1000': 80.0, 'B2000': 50.0}          # ideal rate, bottles per minute
LINES = {  # SKU mix, unplanned-stop rate per hour, mean stop minutes, speed loss, reject rate, rework rate
    'L1': dict(mix={'B500': .80, 'B1000': .20}, stops=1.1, stop_min=6.0, speed=.90, rej=.010, rwk=.004),
    'L2': dict(mix={'B500': .35, 'B1000': .40, 'B2000': .25}, stops=0.7, stop_min=9.0, speed=.86, rej=.018, rwk=.012),
    'L3': dict(mix={'B1000': .25, 'B2000': .75}, stops=0.45, stop_min=14.0, speed=.93, rej=.008, rwk=.025),
}


def build(seed=2026):
    r = np.random.default_rng(seed)
    shifts, stops = [], []
    sid = 0
    for week in range(1, 5):
        for day in range(1, 7):                       # Mon..Sat
            for sh in ('Day', 'Evening'):
                for line, cfg in LINES.items():
                    if day == 6 and not (line == 'L1' and sh == 'Day'): continue   # Saturday: one short shift on L1
                    if line == 'L3' and sh == 'Evening': continue                  # L3 runs day shift only
                    length = 300 if day == 6 else 480
                    planned = 15 if day == 6 else 30          # breaks
                    if line == 'L3' and day == 3 and sh == 'Day': planned += 120     # weekly planned maintenance
                    if line == 'L2' and week == 3 and day == 5 and sh == 'Evening': planned += 240   # no orders
                    pbt = length - planned
                    # unplanned stops: Poisson count, lognormal durations, placed inside the run window
                    k = r.poisson(cfg['stops'] * pbt / 60)
                    ev = []
                    for _ in range(k):
                        d = max(1.0, r.lognormal(np.log(cfg['stop_min']) - .3, .8))
                        s0 = r.uniform(0, max(1, pbt - d))
                        ev.append((s0, s0 + d))
                    ev.sort()
                    merged = []
                    for a, b in ev:
                        if merged and a <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], b)
                        else: merged.append([a, b])
                    down = sum(b - a for a, b in merged)
                    for a, b in ev:
                        stops.append(dict(shift_id=sid, line=line, start_min=round(a, 1), end_min=round(b, 1), source='PLC'))
                        if r.random() < 0.25:   # operator also logs the same stop on the HMI, slightly offset
                            off = r.uniform(-1, 1)
                            stops.append(dict(shift_id=sid, line=line, start_min=round(max(0, a + off), 1),
                                              end_min=round(b + off, 1), source='HMI'))
                    run = pbt - down
                    # split run time across SKUs by mix (one changeover is inside planned time for simplicity)
                    row = dict(shift_id=sid, week=week, day=day, shift=sh, line=line, shift_min=length, planned_down_min=planned)
                    for sku in SKUS:
                        share = cfg['mix'].get(sku, 0.0)
                        if share == 0:
                            row[f'{sku}_produced'] = row[f'{sku}_rejected'] = row[f'{sku}_reworked'] = 0; continue
                        sp = cfg['speed'] * r.normal(1, .03)
                        produced = int(SKUS[sku] * sp * run * share)
                        rej = int(r.binomial(produced, cfg['rej'])); rwk = int(r.binomial(produced - rej, cfg['rwk']))
                        row[f'{sku}_produced'] = produced; row[f'{sku}_rejected'] = rej; row[f'{sku}_reworked'] = rwk
                    shifts.append(row); sid += 1
    return shifts, stops


def merged_down(stops_for_shift):
    ev = sorted((s['start_min'], s['end_min']) for s in stops_for_shift)
    m = []
    for a, b in ev:
        if m and a <= m[-1][1]: m[-1][1] = max(m[-1][1], b)
        else: m.append([a, b])
    return sum(b - a for a, b in m)


def elements(shifts, stops, err=None):
    """Per-shift elements. err selects one of the calculation errors that change the elements."""
    by = {}
    for s in stops: by.setdefault(s['shift_id'], []).append(s)
    out = []
    for row in shifts:
        ev = by.get(row['shift_id'], [])
        if err == 'E5': down = sum(s['end_min'] - s['start_min'] for s in ev)      # sum every logged event
        else: down = merged_down(ev)
        pbt = row['shift_min'] - (0 if err == 'E4' else row['planned_down_min'])
        run = row['shift_min'] - row['planned_down_min'] - down
        produced = sum(row[f'{k}_produced'] for k in SKUS)
        bad_k = {k: row[f'{k}_rejected'] + (0 if err == 'E6' else row[f'{k}_reworked']) for k in SKUS}
        if err == 'E3':    rate = {k: max(SKUS.values()) for k in SKUS}     # one rate: the fastest SKU
        elif err == 'E3b': rate = {k: min(SKUS.values()) for k in SKUS}     # one rate: the slowest SKU
        else:              rate = SKUS
        ideal = sum(row[f'{k}_produced'] / rate[k] for k in SKUS)          # ideal minutes for the units made
        good_ideal = sum((row[f'{k}_produced'] - bad_k[k]) / rate[k] for k in SKUS)   # ideal minutes of first-pass good units
        out.append(dict(row, pbt=pbt, down=down, run=run, produced=produced, good=produced - sum(bad_k.values()),
                        ideal=ideal, good_ideal=good_ideal, planned_loss=row['planned_down_min'] if err == 'E4' else 0,
                        A=run / pbt, P=ideal / run, Q=good_ideal / ideal, OEE=good_ideal / pbt))
    return out


def pooled(el):
    pbt = sum(e['pbt'] for e in el); run = sum(e['run'] for e in el); ideal = sum(e['ideal'] for e in el)
    good = sum(e['good_ideal'] for e in el)
    A, P, Q = run / pbt, ideal / run, good / ideal     # quality in ideal-time units, so A*P*Q = good ideal time / PBT
    return dict(A=A, P=P, Q=Q, OEE=A * P * Q, pbt=pbt, run=run)


def aggregate(el, err=None):
    if err == 'E1':   # average of shift OEEs
        return dict(OEE=float(np.mean([e['OEE'] for e in el])))
    if err == 'E2':   # product of averaged factors
        A, P, Q = (float(np.mean([e[k] for e in el])) for k in 'APQ')
        return dict(A=A, P=P, Q=Q, OEE=A * P * Q)
    return pooled(el)


ERRORS = {
    'REF': 'Reference: ISO 22400 elements, merged stops, rate per SKU, pooled sums',
    'E1': 'Average of shift OEE values (unweighted)',
    'E2': 'Product of averaged availability, performance and quality',
    'E3': 'One ideal rate for all SKUs (fastest SKU, 120 bottles/min)',
    'E3b': 'One ideal rate for all SKUs (slowest SKU, 50 bottles/min)',
    'E4': 'Planned downtime counted as availability loss',
    'E5': 'Duplicate stop events summed instead of merged',
    'E6': 'Reworked bottles counted as good',
    'E7': 'Plant OEE as the unweighted mean of the three line OEEs',
}


def plant_and_lines(shifts, stops, err):
    el = elements(shifts, stops, err if err in ('E3', 'E3b', 'E4', 'E5', 'E6') else None)
    agg_err = err if err in ('E1', 'E2') else None
    lines = {l: aggregate([e for e in el if e['line'] == l], agg_err) for l in LINES}
    if err == 'E7': plant = dict(OEE=float(np.mean([v['OEE'] for v in lines.values()])))
    else: plant = aggregate(el, agg_err)
    return plant, lines, el


def loss_hours(el):
    """Loss tree in hours: availability, performance, quality (reference elements only)."""
    a = sum(e['down'] + e['planned_loss'] for e in el) / 60     # planned downtime only when it is (wrongly) counted as loss
    p = sum(e['run'] - e['ideal'] for e in el) / 60
    q = sum(e['ideal'] - e['good_ideal'] for e in el) / 60
    return dict(availability=a, performance=p, quality=q)


def questions(shifts, stops):
    el = elements(shifts, stops)
    qs = []
    def add(q, a, unit, tol, kind):
        qs.append(dict(id=f'Q{len(qs)+1:02d}', question=q, answer=round(a, 4), unit=unit, tolerance=tol, type=kind))
    P = pooled(el)
    add('What was the plant OEE over the four weeks?', 100 * P['OEE'], '%', 0.1, 'aggregate')
    for l in LINES:
        add(f'What was line {l} OEE over the four weeks?', 100 * pooled([e for e in el if e['line'] == l])['OEE'], '%', 0.1, 'aggregate')
    for l in LINES:
        add(f'What was line {l} availability over the four weeks?', 100 * pooled([e for e in el if e['line'] == l])['A'], '%', 0.1, 'factor')
    add('What was line L2 performance over the four weeks?', 100 * pooled([e for e in el if e['line'] == 'L2'])['P'], '%', 0.1, 'factor')
    add('What was line L3 quality (first-pass good share of ideal production time) over the four weeks?', 100 * pooled([e for e in el if e['line'] == 'L3'])['Q'], '%', 0.1, 'factor')
    for w in (1, 3):
        add(f'What was the plant OEE in week {w}?', 100 * pooled([e for e in el if e['week'] == w])['OEE'], '%', 0.1, 'filter')
    add('What was L1 OEE on Saturday shifts only?', 100 * pooled([e for e in el if e['line'] == 'L1' and e['day'] == 6])['OEE'], '%', 0.1, 'filter')
    add('What was L2 OEE on evening shifts in week 3?', 100 * pooled([e for e in el if e['line'] == 'L2' and e['week'] == 3 and e['shift'] == 'Evening'])['OEE'], '%', 0.1, 'filter')
    add('How many hours of unplanned downtime did L3 have (overlapping stop records merged)?', sum(e['down'] for e in el if e['line'] == 'L3') / 60, 'h', 0.1, 'stops')
    add('How many hours of unplanned downtime did the plant have (overlapping stop records merged)?', sum(e['down'] for e in el) / 60, 'h', 0.1, 'stops')
    lh = {l: loss_hours([e for e in el if e['line'] == l]) for l in LINES}
    add('How many hours were lost to speed (performance loss) on L1?', lh['L1']['performance'], 'h', 0.1, 'loss')
    add('How many hours of ideal production were lost to rejects and rework on L3?', lh['L3']['quality'], 'h', 0.1, 'loss')
    add('How many good B2000 bottles did the plant make (rejects and reworked bottles excluded)?',
        sum(r['B2000_produced'] - r['B2000_rejected'] - r['B2000_reworked'] for r in shifts), 'bottles', 0.5, 'count')
    add('How many bottles were reworked on L2?', sum(r[f'{k}_reworked'] for r in shifts if r['line'] == 'L2' for k in SKUS), 'bottles', 0.5, 'count')
    worst = min(LINES, key=lambda l: pooled([e for e in el if e['line'] == l])['OEE'])
    qs.append(dict(id=f'Q{len(qs)+1:02d}', question='Which line had the lowest OEE?', answer=worst, unit='', tolerance=0, type='rank'))
    for l in LINES:
        big = max(lh[l], key=lh[l].get)
        qs.append(dict(id=f'Q{len(qs)+1:02d}', question=f'Which loss (availability, performance or quality) cost line {l} the most hours?', answer=big, unit='', tolerance=0, type='rank'))
    gain = {l: lh[l]['availability'] for l in LINES}
    qs.append(dict(id=f'Q{len(qs)+1:02d}', question='On which line would halving unplanned downtime recover the most production hours?', answer=max(gain, key=gain.get), unit='', tolerance=0, type='rank'))
    return qs


def main():
    shifts, stops = build()
    os.makedirs(DATA, exist_ok=True)
    for name, rows in (('shifts', shifts), ('stops', stops)):
        with open(os.path.join(DATA, f'{name}.csv'), 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open(os.path.join(DATA, 'skus.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['sku', 'ideal_rate_per_min']); [w.writerow([k, v]) for k, v in SKUS.items()]
    res = {}
    ref_plant, ref_lines, ref_el = plant_and_lines(shifts, stops, 'REF')
    for e in ERRORS:
        plant, lines, el = plant_and_lines(shifts, stops, e)
        rank = sorted(lines, key=lambda l: lines[l]['OEE'])
        res[e] = dict(label=ERRORS[e], plant=plant, lines=lines, worst_first=rank,
                      biggest_loss={l: max(loss_hours([x for x in el if x['line'] == l]), key=loss_hours([x for x in el if x['line'] == l]).get) for l in LINES} if e in ('REF', 'E3', 'E3b', 'E4', 'E5', 'E6') else None)
    res['loss_hours'] = {l: loss_hours([x for x in ref_el if x['line'] == l]) for l in LINES}
    res['n_shifts'] = len(shifts); res['n_stop_records'] = len(stops)
    res['n_duplicate_records'] = sum(1 for s in stops if s['source'] == 'HMI')
    json.dump(res, open(os.path.join(HERE, 'results.json'), 'w'), indent=1)
    json.dump(questions(shifts, stops), open(os.path.join(HERE, 'questions.json'), 'w'), indent=1)
    print(f"{len(shifts)} shift rows, {len(stops)} stop records ({res['n_duplicate_records']} duplicates)")
    for e in ERRORS:
        p = res[e]['plant']['OEE']; d = 100 * (p - ref_plant['OEE'])
        ln = '  '.join(f"{l} {100 * res[e]['lines'][l]['OEE']:5.1f}" for l in LINES)
        print(f"{e:4s} plant {100 * p:5.1f}% ({d:+5.1f} pts) | {ln} | worst {res[e]['worst_first'][0]} | {res[e]['biggest_loss']}")
    print({l: {k: round(v, 1) for k, v in d.items()} for l, d in res['loss_hours'].items()})
    for k in 'APQ': print(k, {l: round(100 * ref_lines[l][k], 1) for l in LINES})


if __name__ == '__main__':
    main()
