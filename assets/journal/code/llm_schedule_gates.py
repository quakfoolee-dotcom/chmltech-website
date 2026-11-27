"""Verification gates for an LLM-written scheduling model - Chmltech Online Journal, Vol. 106, Issue 18 (compact).

orders: list of dicts {'rel': release minute, 'due': due minute, 'ops': [(machine, minutes incl. setup, setup minutes), ...]}
m0:     {machine: minute it becomes free} for operations already running (empty dict if none)
sched:  sched[j][k] = start minute of operation k of order j, as returned by the LLM-written model.
The gates read the plant's own data and the solver's output, never the model itself.
"""


def violations(orders, sched, m0):
    """G2: check the schedule against the TRUE constraints (release, routing order, busy machines, one job per machine)."""
    v, by_machine = [], {}
    for j, o in enumerate(orders):
        ready = o['rel']
        for k, (m, p, _) in enumerate(o['ops']):
            s = sched[j][k]
            if s < ready:
                v.append(('release' if k == 0 else 'precedence', j, k))
            if s < m0.get(m, 0):
                v.append(('machine busy', j, k))
            ready = s + p
            by_machine.setdefault(m, []).append((s, s + p, j))
    for m, iv in by_machine.items():
        iv.sort()
        v += [('capacity', m, a[2], b[2]) for a, b in zip(iv, iv[1:]) if b[0] < a[1]]
    return v


def total_tardiness_h(orders, sched):
    """The plant's KPI, computed from the schedule with the true processing times."""
    return sum(max(0, sched[j][-1] + o['ops'][-1][1] - o['due']) for j, o in enumerate(orders)) / 60


def dispatch(orders, m0, priority):
    """Non-delay list scheduling: whenever a machine is free and work waits, start the waiting operation with the
    lowest priority(orders, j, k, now, queued_since). Used for the G4 baseline."""
    t0 = min([0] + [o['rel'] for o in orders])
    nxt, ready = [0] * len(orders), [o['rel'] for o in orders]
    free = {m: m0.get(m, t0) for o in orders for m, _, _ in o['ops']}
    out = [[None] * len(o['ops']) for o in orders]
    while True:
        cand = [(max(free[o['ops'][nxt[j]][0]], ready[j]), j) for j, o in enumerate(orders) if nxt[j] < len(o['ops'])]
        if not cand:
            return out
        t = min(c for c, _ in cand)
        for m in sorted({orders[j]['ops'][nxt[j]][0] for c, j in cand if c <= t}):
            q = [j for c, j in cand if c <= t and orders[j]['ops'][nxt[j]][0] == m and free[m] <= t and out[j][nxt[j]] is None]
            if not q:
                continue
            j = min(q, key=lambda j: (priority(orders, j, nxt[j], t, ready[j]), j))
            p = orders[j]['ops'][nxt[j]][1]
            out[j][nxt[j]] = t; free[m] = ready[j] = t + p; nxt[j] += 1
            cand = [(max(free[o['ops'][nxt[i]][0]], ready[i]), i) for i, o in enumerate(orders) if nxt[i] < len(o['ops'])]


def fifo(O, j, k, now, since): return since                       # first come, first served at each machine
def edd(O, j, k, now, since):  return O[j]['due']
def spt(O, j, k, now, since):  return O[j]['ops'][k][1]
def mdd(O, j, k, now, since):  return max(O[j]['due'], now + sum(p for _, p, _ in O[j]['ops'][k:]))


def repair(orders, sched, m0):
    """What the floor does with an infeasible plan: keep each machine's order of operations from the plan and
    start every operation as soon as its order and its machine allow (right-shift)."""
    out, free = [[None] * len(o['ops']) for o in orders], dict(m0)
    pend = sorted((sched[j][k], j, k) for j, o in enumerate(orders) for k in range(len(o['ops'])))
    while pend:
        i = next(i for i, (_, j, k) in enumerate(pend) if k == 0 or out[j][k - 1] is not None)
        _, j, k = pend.pop(i); m, p, _ = orders[j]['ops'][k]
        ready = orders[j]['rel'] if k == 0 else out[j][k - 1] + orders[j]['ops'][k - 1][1]
        out[j][k] = max(ready, free.get(m, 0)); free[m] = out[j][k] + p
    return out


def gates(orders, m0, status, sched, reported_objective_h, rules=(fifo, edd, spt, mdd)):
    """Run G1-G4. reported_objective_h must be the solver's own objective value in hours, not a KPI that the
    generated code recomputed from its schedule. Returns (passed, report)."""
    if status not in ('OPTIMAL', 'FEASIBLE') or sched is None:
        return False, {'G1': 'solver returned ' + status}
    rep = {'G1': 'ok'}
    v = violations(orders, sched, m0)
    rep['G2'] = f'{len(v)} violations' if v else 'ok'
    true = total_tardiness_h(orders, sched)
    rep['G3'] = 'ok' if abs(true - reported_objective_h) <= 0.05 else f'model claims {reported_objective_h:.1f} h, schedule gives {true:.1f} h'
    final = total_tardiness_h(orders, repair(orders, sched, m0) if v else sched)
    best = min(total_tardiness_h(orders, dispatch(orders, m0, r)) for r in rules)
    rep['G4'] = 'ok' if final <= best + 0.05 else f'{final:.1f} h against {best:.1f} h for the best rule'
    return all(x == 'ok' for x in rep.values()), rep
