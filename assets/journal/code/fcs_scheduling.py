"""Finite-capacity job-shop simulation - Chmltech Online Journal (compact version)."""
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
            ops = [(c, (SETUP.get(c, .25) + n * u) * r.lognormal(-s2 / 2, np.sqrt(s2)))
                   for c, u in route]
            due = t + (len(ops) + 2) * 8                # ERP: 1 day per op + 2 days
            orders.append(dict(arr=t, due=due, ops=ops, k=0, done=None))


def simulate(orders, rule='FIFO', gate=None, bn_only=False):
    """rule: FIFO, EDD, SPT, CR, MDD. gate: buffer in welder hours (load-based release) or None."""
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
    lead = np.mean([(o['done'] - o['arr']) / 8 for o in measured])
    return on_time, lead


for label, kw in [('FIFO (ERP push)', dict(rule='FIFO')),
                  ('Critical ratio', dict(rule='CR')),
                  ('MDD at welder only', dict(rule='MDD', bn_only=True)),
                  ('Load-based release + MDD at welder', dict(rule='MDD', bn_only=True, gate=24))]:
    res = [simulate(make_orders(seed), **kw) for seed in range(1000, 1100)]
    print(f"{label:36s} on time {np.mean([r[0] for r in res]):5.1f}%   "
          f"mean lead time {np.mean([r[1] for r in res]):4.1f} days")
