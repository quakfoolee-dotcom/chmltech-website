"""LLM-written scheduling models: error-injection study (Chmltech Online Journal, Vol. 106, Issue 18).

A weekly scheduling snapshot of the windows-and-doors plant of Vol. 106, Issue 4 is solved
(1) with a reference CP-SAT model that minimizes total tardiness,
(2) with five dispatching rules (non-delay list scheduling), and
(3) with eight faulty versions of the model, each containing one formulation error of the kind
    reported for LLM-written optimization models (missing constraint, wrong objective, unit error,
    ignored data, mis-sized big-M).
Every schedule is then put through four verification gates. Time unit: minutes.

Usage: python3 llm_sched.py [n_snapshots] [deterministic_time_limit]   ->  results.json  (deterministic: same numbers on every run)
"""
import json, sys
import numpy as np
from ortools.sat.python import cp_model

HPW = 40.0
SETUP = {'Weld': 0.4}
FAMILIES = {  # share, mean units/order, routing (centre, hours per unit) -- as in Vol. 106, Issue 4
    'Casement': (.35, 10, [('Cut', .15), ('Weld', .30), ('Clean', .18), ('Glaze', .20), ('Assemble', .25), ('Pack', .08)]),
    'Slider':   (.25, 10, [('Cut', .12), ('Weld', .25), ('Clean', .15), ('Glaze', .18), ('Pack', .06)]),
    'Patio':    (.15, 3,  [('Cut', .30), ('CNC', .40), ('Weld', .60), ('Clean', .25), ('Glaze', .50), ('Assemble', .60), ('Pack', .15)]),
    'Entry':    (.15, 3,  [('CNC', .50), ('DoorPrep', .80), ('Glaze', .30), ('Assemble', .70), ('Pack', .15)]),
    'Custom':   (.10, 4,  [('Cut', .40), ('CNC', .60), ('Weld', .90), ('Clean', .40), ('Glaze', .60), ('Assemble', .80), ('Pack', .20)]),
}
NAMES = list(FAMILIES)
SHARE = [FAMILIES[f][0] for f in NAMES]
MACH = ['Cut', 'CNC', 'Weld', 'Clean', 'Glaze', 'Assemble', 'DoorPrep', 'Pack']


class Snap(list):
    """List of open orders with m0 = minute each machine becomes free (operation in progress at Monday 07:00)."""
    m0 = {}


def _orders(r, t0, t1, cv=0.4, group=2.0, per_week=12.4):
    s2 = np.log(1 + cv ** 2); t, out = t0, []
    while True:
        t += r.exponential(HPW * group / per_week)
        if t > t1: break
        for _ in range(r.geometric(1 / group)):
            fam = NAMES[r.choice(5, p=SHARE)]
            _, mu, route = FAMILIES[fam]
            n = int(r.geometric(1 / mu))
            ops = []
            for c, u in route:
                f = r.lognormal(-s2 / 2, np.sqrt(s2))
                setup = SETUP.get(c, .25) * f
                ops.append((c, int(round(60 * (setup + n * u * f))), int(round(60 * setup))))
            out.append(dict(fam=fam, n=n, entry=int(round(60 * t)), rel=int(round(60 * t)),
                            due=int(round(60 * (t + (len(ops) + 2) * 8))), ops=ops))
    return out


def snapshot(seed, warmup_h=480.0, window_h=40.0):
    """Monday 07:00 state of the Vol. 106, Issue 4 plant. The plant runs MDD at every work centre for 12 weeks
    (orders arrive at about 82% welder load); operations started before Monday are history, an operation in
    progress keeps its machine busy, and every unstarted operation of an open order is to be scheduled,
    together with the orders that will arrive this week. Times in minutes from Monday 07:00."""
    r = np.random.default_rng(seed)
    past = _orders(r, -warmup_h, 0.0)
    hist = dispatch(past, 'MDD')                       # causal: only orders already arrived are dispatched
    snap, m0 = Snap(), {m: 0 for m in MACH}
    for o, st in zip(past, hist):
        k = next((k for k, s in enumerate(st) if s >= 0), None)
        if k is None: continue                          # all operations started before Monday
        rel = 0
        if k > 0:
            m, p, _ = o['ops'][k - 1]; end = st[k - 1] + p
            if end > 0: m0[m] = max(m0[m], end); rel = end
        snap.append(dict(o, rel=max(rel, 0), ops=o['ops'][k:], done=k))
    for o in _orders(r, 0.0, window_h):
        snap.append(dict(o, done=0))
    snap.m0 = m0
    return snap


# ---------- truth: feasibility check, objective, replay ----------
def check(orders, sched):
    """sched[j][k] = start minute of op k of order j. Returns list of violations on the TRUE problem."""
    v = []
    by_m = {m: [] for m in MACH}
    m0 = getattr(orders, 'm0', {})
    for j, o in enumerate(orders):
        prev_end = o['rel']
        for k, (m, p, _) in enumerate(o['ops']):
            s = sched[j][k]
            if s < prev_end - 0: v.append(('precedence' if k else 'release', j, k))
            if s < m0.get(m, 0): v.append(('machine busy', j, k))
            prev_end = s + p
            by_m[m].append((s, s + p, j, k))
    for m, iv in by_m.items():
        iv.sort()
        for a, b in zip(iv, iv[1:]):
            if b[0] < a[1]: v.append(('capacity', m, a[2], b[2]))
    return v


def tardiness(orders, sched):
    tot, late = 0, 0
    for j, o in enumerate(orders):
        c = sched[j][-1] + o['ops'][-1][1]
        if c > o['due']: tot += c - o['due']; late += 1
    return tot / 60.0, late          # hours, count


def repair(orders, sched, how='rightshift'):
    """What the shop floor does with an infeasible plan.
    rightshift (main): keep the plan's order of operations on each machine and start each operation as soon as
    its order and its machine allow. nondelay (sensitivity): use the plan's start times only as priorities
    and never leave a machine idle while work waits."""
    if how == 'nondelay':
        return dispatch(orders, 'GIVEN', given=sched)
    m0 = getattr(orders, 'm0', {})
    out = [[None] * len(o['ops']) for o in orders]; free = dict(m0)
    pend = sorted((sched[j][k], j, k) for j, o in enumerate(orders) for k in range(len(o['ops'])))
    while pend:
        i = next(i for i, (_, j, k) in enumerate(pend) if k == 0 or out[j][k - 1] is not None)
        _, j, k = pend.pop(i); m, p, _ = orders[j]['ops'][k]
        ready = orders[j]['rel'] if k == 0 else out[j][k - 1] + orders[j]['ops'][k - 1][1]
        out[j][k] = max(ready, free.get(m, 0)); free[m] = out[j][k] + p
    return out


# ---------- dispatching rules (deterministic non-delay list scheduling) ----------
def dispatch(orders, rule, given=None):
    n = len(orders)
    nxt = [0] * n; ready = [o['rel'] for o in orders]; t_start = min([0] + [o['rel'] for o in orders]); mfree = {m: getattr(orders, 'm0', {}).get(m, t_start) for m in MACH}
    out = [[None] * len(o['ops']) for o in orders]
    qin = [o['rel'] for o in orders]
    left = sum(len(o['ops']) for o in orders)

    def prio(j, now):
        o = orders[j]; k = nxt[j]; rem = sum(p for _, p, _ in o['ops'][k:])
        if rule == 'EDD': return o['due']
        if rule == 'SPT': return o['ops'][k][1]
        if rule == 'CR': return (o['due'] - now) / rem
        if rule == 'MDD': return max(o['due'], now + rem)
        if rule == 'GIVEN': return given[j][k]
        return qin[j]
    while left:
        # earliest time any machine can start a waiting op
        cand = [(max(mfree[orders[j]['ops'][nxt[j]][0]], ready[j]), j) for j in range(n) if nxt[j] < len(orders[j]['ops'])]
        t = min(c for c, _ in cand)
        for m in MACH:
            if mfree[m] > t: continue
            q = [j for c, j in cand if c <= t and orders[j]['ops'][nxt[j]][0] == m]
            if not q: continue
            j = min(q, key=lambda j: (prio(j, t), j))
            k = nxt[j]; p = orders[j]['ops'][k][1]
            out[j][k] = t; mfree[m] = t + p; ready[j] = t + p; qin[j] = t + p; nxt[j] += 1; left -= 1
            cand = [(max(mfree[orders[i]['ops'][nxt[i]][0]], ready[i]), i) for i in range(n) if nxt[i] < len(orders[i]['ops'])]
    return out


# ---------- the model (reference) and its faulty variants ----------
FAULTS = {
    'F0': 'Reference model',
    'F1': 'Precedence between an order\'s operations omitted',
    'F2': 'Machine capacity written only for the bottleneck (Weld)',
    'F3': 'Setup time left out of operation times',
    'F4': 'Lateness instead of tardiness (early orders offset late ones)',
    'F5': 'Makespan objective instead of total tardiness',
    'F6': 'Due dates read in working days as if in hours',
    'F7': 'Release times (orders not yet in the plant) ignored',
    'F8': 'Disjunctive big-M sized to one shift (480 min) instead of the horizon',
}


def solve(orders, fault='F0', tlim=20.0, seed=0, hint=None):
    md = cp_model.CpModel()
    H = sum(p for o in orders for _, p, _ in o['ops']) + max([o['rel'] for o in orders] + list(getattr(orders, 'm0', {}).values())) + 1
    S, E, ivs = {}, {}, {m: [] for m in MACH}
    ends = []
    for j, o in enumerate(orders):
        rel = 0 if fault == 'F7' else o['rel']
        prev = None
        for k, (m, p, st) in enumerate(o['ops']):
            d = p - st if fault == 'F3' else p
            lo = max(rel, getattr(orders, 'm0', {}).get(m, 0))
            s = md.NewIntVar(lo, H, f's{j}_{k}'); e = md.NewIntVar(lo, H, f'e{j}_{k}')
            iv = md.NewIntervalVar(s, d, e, f'i{j}_{k}')
            S[j, k], E[j, k] = s, e
            ivs[m].append((iv, s, e, j, k, d))
            if prev is not None and fault != 'F1': md.Add(s >= prev)
            prev = e
        ends.append(prev)
    if fault == 'F8':
        M = 480
        for m, lst in ivs.items():
            for a in range(len(lst)):
                for b in range(a + 1, len(lst)):
                    y = md.NewBoolVar('')
                    md.Add(lst[b][1] >= lst[a][2] - M * (1 - y))
                    md.Add(lst[a][1] >= lst[b][2] - M * y)
    else:
        for m, lst in ivs.items():
            if fault == 'F2' and m != 'Weld': continue
            md.AddNoOverlap([x[0] for x in lst])
    terms = []
    for j, o in enumerate(orders):
        due = o['entry'] + (o['due'] - o['entry']) // 8 if fault == 'F6' else o['due']   # 'D working days' read as D hours
        if fault == 'F4':
            terms.append(ends[j] - due)
        else:
            t = md.NewIntVar(0, 2 * H, f't{j}'); md.Add(t >= ends[j] - due); terms.append(t)
    if fault == 'F5':
        cmax = md.NewIntVar(0, H, 'cmax'); md.AddMaxEquality(cmax, ends); md.Minimize(cmax)
    else:
        md.Minimize(sum(terms))
    if hint is not None:   # warm start from the best dispatching rule (all models get the same hint)
        for (j, k), v in S.items(): md.AddHint(v, hint[j][k])
        for (j, k), v in E.items(): md.AddHint(v, hint[j][k] + orders[j]['ops'][k][1])
    sv = cp_model.CpSolver(); sv.parameters.max_deterministic_time = tlim   # deterministic: same result on every run
    sv.parameters.num_workers = 4; sv.parameters.interleave_search = True; sv.parameters.random_seed = seed   # interleaved workers + deterministic time: reproducible
    st = sv.Solve(md)
    status = sv.StatusName(st)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return status, None, None, None
    sched = [[sv.Value(S[j, k]) for k in range(len(o['ops']))] for j, o in enumerate(orders)]
    return status, sched, sv.ObjectiveValue(), sv.BestObjectiveBound()


def gates(orders, status, sched, reported, best_rule_tard):
    """G1 solver status, G2 independent feasibility check, G3 objective recomputation,
    G4 no worse than the best dispatching rule (after right-shift repair)."""
    g = {'G1': status not in ('OPTIMAL', 'FEASIBLE')}
    if sched is None:
        return g | {'G2': None, 'G3': None, 'G4': None}, None, None, None, None
    viol = check(orders, sched)
    g['G2'] = len(viol) > 0
    true_t, _ = tardiness(orders, sched)
    g['G3'] = abs(reported / 60.0 - true_t) > 0.05       # solver objective vs tardiness recomputed from the schedule
    fixed = repair(orders, sched) if viol else sched
    assert not check(orders, fixed)
    rep_t, rep_late = tardiness(orders, fixed)
    nd_t = tardiness(orders, repair(orders, sched, 'nondelay'))[0] if viol else rep_t
    g['G4'] = rep_t > best_rule_tard + 0.05
    return g, rep_t, rep_late, len(viol), nd_t


def main(n=30, tlim=1.0):
    res = []
    for i in range(n):
        seed = 5000 + i
        orders = snapshot(seed)
        rules, scheds = {}, {}
        for r in ['FIFO', 'EDD', 'SPT', 'CR', 'MDD']:
            sc = dispatch(orders, r); assert not check(orders, sc), r
            rules[r] = tardiness(orders, sc); scheds[r] = sc
        best_rule = min(v[0] for v in rules.values())
        hint = scheds[min(rules, key=lambda r: rules[r][0])]
        row = dict(seed=seed, n_orders=len(orders), n_ops=sum(len(o['ops']) for o in orders),
                   weld_h=sum(p for o in orders for m, p, _ in o['ops'] if m == 'Weld') / 60,
                   rules={k: dict(tard_h=v[0], late=v[1]) for k, v in rules.items()}, faults={}, nohint={})
        for f in FAULTS:
            for key, h in (('faults', hint), ('nohint', None)):   # main: warm start from the best rule; sensitivity: none
                status, sched, rep, bound = solve(orders, f, tlim, hint=h)
                if key == 'faults' and f == 'F0': sched0 = sched
                g, t, late, nviol, nd = gates(orders, status, sched, rep if rep is not None else 0, best_rule)
                row[key][f] = dict(status=status, gates=g, tard_h=t, late=late, n_viol=nviol, nondelay_h=nd,
                                   reported=None if rep is None else rep / 60.0,
                                   gap=None if rep is None or f == 'F4' else (rep - bound) / max(rep, 1))
        # control: the non-delay repair applied to the reference model's own feasible schedule
        row['control_nondelay_h'] = tardiness(orders, repair(orders, sched0, 'nondelay'))[0]
        row['control_rightshift_h'] = tardiness(orders, repair(orders, sched0))[0]
        ref = row['faults']['F0']['tard_h']
        print(f"snap {i:2d}: {row['n_orders']:2d} orders, weld {row['weld_h']:.0f} h | best rule {best_rule:6.1f} | ref {ref} | "
              + " ".join(f"{f}:{'-' if v['tard_h'] is None else round(v['tard_h'])}" for f, v in row['faults'].items()), flush=True)
        res.append(row)
    json.dump(dict(faults=FAULTS, snapshots=res), open('results.json', 'w'), indent=1)


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 30, float(sys.argv[2]) if len(sys.argv) > 2 else 1.0)
