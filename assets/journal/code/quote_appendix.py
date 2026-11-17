"""Due-date quoting on a job-shop simulation - Chmltech Online Journal (compact version)."""
import heapq
import numpy as np

HPW = 40.0                                   # working hours per week
MACHINES = {'Cut': 1, 'CNC': 1, 'Weld': 1, 'Clean': 1, 'Glaze': 1,
            'Assemble': 1, 'DoorPrep': 1, 'Pack': 1}
SETUP = {'Weld': 0.4}                        # hours; other centres 0.25
FAMILIES = {  # share, mean units/order, routing (centre, hours per unit)
    'Casement': (.35, 10, [('Cut', .15), ('Weld', .30), ('Clean', .18), ('Glaze', .20), ('Assemble', .25), ('Pack', .08)]),
    'Slider':   (.25, 10, [('Cut', .12), ('Weld', .25), ('Clean', .15), ('Glaze', .18), ('Pack', .06)]),
    'Patio':    (.15, 3,  [('Cut', .30), ('CNC', .40), ('Weld', .60), ('Clean', .25), ('Glaze', .50), ('Assemble', .60), ('Pack', .15)]),
    'Entry':    (.15, 3,  [('CNC', .50), ('DoorPrep', .80), ('Glaze', .30), ('Assemble', .70), ('Pack', .15)]),
    'Custom':   (.10, 4,  [('Cut', .40), ('CNC', .60), ('Weld', .90), ('Clean', .40), ('Glaze', .60), ('Assemble', .80), ('Pack', .20)]),
}
NAMES = list(FAMILIES)
SHARE = [FAMILIES[f][0] for f in NAMES]


def make_orders(seed, per_week=12.4, weeks=68, cv=0.4, group=2.0):
    r = np.random.default_rng(seed)
    s2 = np.log(1 + cv**2)
    orders, t = [], 0.0
    while True:
        t += r.exponential(HPW * group / per_week)      # clumped arrivals
        if t > weeks * HPW:
            return orders
        for _ in range(r.geometric(1 / group)):
            share, mean_units, route = FAMILIES[NAMES[r.choice(5, p=SHARE)]]
            n = r.geometric(1 / mean_units)
            plan = [(c, SETUP.get(c, .25) + n * u) for c, u in route]      # ERP routing hours
            ops = [(c, h * r.lognormal(-s2 / 2, np.sqrt(s2))) for c, h in plan]
            orders.append(dict(arr=t, ops=ops, k=0, done=None, n_ops=len(ops),
                               work=sum(h for _, h in plan),
                               weld=sum(h for c, h in plan if c == 'Weld')))


def quote(o, backlog, how, margin):
    """Quoted lead time in working hours, set when the order is entered."""
    if how == 'routing':                        # ERP: one day per operation + margin
        return (o['n_ops'] + margin) * 8
    if how == 'backlog+work':                   # Eq. (1): (welder backlog + own planned hours) / 8 + margin
        return backlog + o['work'] + margin * 8


def simulate(orders, how='routing', margin=2, rule='FIFO', gate=None, bn_only=False):
    """how/margin: quoting rule. rule: FIFO or MDD. gate: buffer in welder hours (load-based release) or None."""
    waiting_weld = []                           # entered orders not yet through the welder
    events, seq = [], 0
    busy = {c: 0 for c in MACHINES}
    queue = {c: [] for c in MACHINES}
    pool, weld_on_floor = [], 0.0

    def push(t, kind, o):
        nonlocal seq
        heapq.heappush(events, (t, seq, kind, o))
        seq += 1

    def priority(o, centre, now):
        r_ = rule if (not bn_only or centre == 'Weld') else 'FIFO'
        rem = sum(p for _, p in o['ops'][o['k']:])
        if r_ == 'EDD': return o['due']
        if r_ == 'SPT': return o['ops'][o['k']][1]
        if r_ == 'CR':  return (o['due'] - now) / rem
        if r_ == 'MDD': return max(o['due'], now + rem)
        return o['q_in']                                # FIFO

    def start(centre, now):
        while queue[centre] and busy[centre] < MACHINES[centre]:
            o = min(queue[centre], key=lambda x: priority(x, centre, now))
            queue[centre].remove(o)
            busy[centre] += 1
            push(now + o['ops'][o['k']][1], 'finish', o)

    def enter(o, now):
        o['q_in'] = now
        queue[o['ops'][o['k']][0]].append(o)
        start(o['ops'][o['k']][0], now)

    def weld_hours(o):
        return sum(p for c, p in o['ops'][o['k']:] if c == 'Weld')

    def release(now):
        nonlocal weld_on_floor
        pool.sort(key=lambda o: o['due'])
        for o in list(pool):
            w = weld_hours(o)
            if w == 0 or weld_on_floor < 1e-6 or weld_on_floor + w <= gate:
                pool.remove(o)
                weld_on_floor += w
                enter(o, now)

    for o in orders:
        push(o['arr'], 'arrive', o)
    while events:
        now, _, kind, o = heapq.heappop(events)
        if kind == 'arrive':
            backlog = sum(x['weld'] for x in waiting_weld)  # planned welder hours ahead
            o['quote'] = quote(o, backlog, how, margin)
            o['due'] = now + o['quote']
            if o['weld'] > 0:
                waiting_weld.append(o)
            if gate is None:
                enter(o, now)
            else:
                pool.append(o)
                release(now)
            continue
        centre = o['ops'][o['k']][0]
        busy[centre] -= 1
        if centre == 'Weld':
            weld_on_floor -= o['ops'][o['k']][1]
            waiting_weld.remove(o)
        o['k'] += 1
        if o['k'] < len(o['ops']):
            enter(o, now)
        else:
            o['done'] = now
        start(centre, now)
        if gate is not None:
            release(now)
    measured = [o for o in orders if 10 * HPW <= o['arr'] < 60 * HPW]
    on_time = np.mean([o['done'] <= o['due'] for o in measured]) * 100
    quoted = np.mean([o['quote'] / 8 for o in measured])
    worst = max((o['done'] - o['due']) / 8 for o in measured)
    return on_time, quoted, worst


for label, kw in [('Routing rule, ERP default (m = 2)', dict(how='routing', margin=2)),
                  ('Routing rule set for 95% (m = 7.87)', dict(how='routing', margin=7.87)),
                  ('Backlog plus work (m = 2.99)', dict(how='backlog+work', margin=2.99)),
                  ('Backlog plus work, MDD + gate (m = 2.54)', dict(how='backlog+work', margin=2.54, rule='MDD', bn_only=True, gate=24))]:
    res = [simulate(make_orders(seed), **kw) for seed in range(1000, 1100)]
    print(f"{label:42s} on time {np.mean([r[0] for r in res]):5.1f}%   "
          f"average quote {np.mean([r[1] for r in res]):5.2f} days   worst order {np.median([r[2] for r in res]):5.1f} days late")
