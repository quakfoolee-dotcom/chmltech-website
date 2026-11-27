"""Reference OEE calculator - Chmltech Online Journal, Vol. 106, Issue 17 (compact version).
Reads data/shifts.csv, data/stops.csv and data/skus.csv; prints availability, performance, quality and OEE
by line and for the plant, aggregated from sums (never by averaging ratios). Quality is measured in ideal minutes, so A x P x Q is the
ideal time of the good output divided by planned busy time."""
import csv, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
D = lambda f: os.path.join(HERE, "data", f)

rate = {r['sku']: float(r['ideal_rate_per_min']) for r in csv.DictReader(open(D('skus.csv')))}
stops = defaultdict(list)
for s in csv.DictReader(open(D('stops.csv'))):
    stops[s['shift_id']].append((float(s['start_min']), float(s['end_min'])))


def merged_minutes(events):
    """Unplanned downtime: overlapping or duplicate stop records are merged, not summed."""
    total, end = 0.0, None
    for a, b in sorted(events):
        if end is None or a > end:
            total += b - a; end = b
        elif b > end:
            total += b - end; end = b
    return total


sums = defaultdict(lambda: defaultdict(float))      # line -> pbt, run, ideal, good (ideal minutes)
for r in csv.DictReader(open(D('shifts.csv'))):
    pbt = float(r['shift_min']) - float(r['planned_down_min'])        # planned busy time
    run = pbt - merged_minutes(stops[r['shift_id']])                  # actual production time
    for key in (r['line'], 'Plant'):
        t = sums[key]
        t['pbt'] += pbt; t['run'] += run
        for k in rate:
            n = int(r[f'{k}_produced'])
            good = n - int(r[f'{k}_rejected']) - int(r[f'{k}_reworked'])   # first-pass good only
            t['ideal'] += n / rate[k]                                  # ideal minutes for the units made
            t['good'] += good / rate[k]                                # ideal minutes of the good units

for key in sorted(sums, key=lambda k: (k == 'Plant', k)):
    t = sums[key]
    A, P, Q = t['run'] / t['pbt'], t['ideal'] / t['run'], t['good'] / t['ideal']
    print(f"{key:6s} A {100*A:5.1f}%  P {100*P:5.1f}%  Q {100*Q:5.1f}%  OEE {100*A*P*Q:5.1f}%")
