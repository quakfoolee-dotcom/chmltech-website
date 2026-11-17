"""Due-date quoting experiments on the windows-and-doors job shop (Chmltech scheduling paper model). V1.

Adds a quote hook to the shop simulation: when an order arrives, a quoting rule sets its due date from what is known
at order entry (routing, planned work content, current welder backlog). Dispatch and release rules then run as before.
"""
import heapq, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import tune                                     # applies the calibrated plant (single Cut/Glaze/Assemble, Clean times)
from shop import STATIONS, SETUP, FAM, FAMS, MIX, HPW, WARM, WEEKS

SEEDS = list(range(1000, 1100))


def planned(f, n):
    """Planned (expected) hours by station for an order of n units of family f, as an ERP routing would hold them."""
    return [(st, SETUP[st] + n * u) for st, u in FAM[f][2]]


def make_orders(seed, rate=12.4, cv=0.4, bmean=2.0, spike=None, weeks=WARM + WEEKS + 8):
    """Same random stream as tune.mj: clumped arrivals, geometric order sizes, lognormal processing noise."""
    r = np.random.default_rng(seed); jobs = []; t = 0.0; end = weeks * HPW; s2 = np.log(1 + cv ** 2)
    while True:
        lam = rate / bmean
        if spike and spike[0] * HPW <= t < spike[1] * HPW:
            lam *= spike[2]
        t += r.exponential(HPW / lam)
        if t > end:
            break
        for _ in range(int(r.geometric(1 / bmean))):
            f = FAMS[r.choice(len(FAMS), p=MIX)]; mu = FAM[f][1]; n = max(1, int(r.geometric(1 / mu)))
            ops = [(st, (SETUP[st] + n * u) * r.lognormal(-s2 / 2, np.sqrt(s2))) for st, u in FAM[f][2]]
            pl = planned(f, n)
            jobs.append(dict(id=len(jobs), fam=f, units=n, arr=t, ops=ops, nops=len(ops),
                             pwork=sum(h for _, h in pl), pweld=sum(h for s, h in pl if s == 'Weld')))
    return jobs


# ---- quoting rules: return quoted lead time in working hours, given order j and welder backlog (planned hours) ----
def q_erp(j, backlog, m):            # ERP routing rule: one day per operation + m days margin
    return (j['nops'] + m) * 8.0
def q_flat(j, backlog, m):           # one standard lead time for every order: m days
    return m * 8.0
def q_backlog(j, backlog, m):        # routing rule plus the current welder backlog in days
    return (j['nops'] + m) * 8.0 + backlog
def q_load(j, backlog, m):           # welder backlog + the order's own planned work + m days
    return backlog + j['pwork'] + m * 8.0
QUOTE_RULES = dict(erp=q_erp, flat=q_flat, backlog=q_backlog, load=q_load)


def simulate(jobs, quote, m, rule='FIFO', release='push', B=24.0, bn_rule=None, coef=None, down=None):
    """Event simulation as in the scheduling paper, with a due date set at order arrival by `quote`.
    quote may be a rule name or 'fit' (linear predictor with coefficients `coef` + m days)."""
    ev = []; seq = 0
    def push(t, typ, d):
        nonlocal seq; heapq.heappush(ev, (t, seq, typ, d)); seq += 1
    for j in jobs:
        j.update(k=0, rel=None, done=None, qin=None, weld_done=('Weld' not in [s for s, _ in j['ops']]))
        push(j['arr'], 'arr', j['id'])
    busy = {s: 0 for s in STATIONS}; Q = {s: [] for s in STATIONS}
    pool = []; weld_load = 0.0; active = []
    downuntil = -1; inproc = {}; ver = defaultdict(int)
    if down:
        push(down[0], 'down', down[1])
    def prio(j, s, now):
        r_ = rule if (bn_rule is None or s == 'Weld') else 'FIFO'
        if r_ == 'FIFO': return j['qin']
        if r_ == 'EDD': return j['due']
        rem = sum(pp for _, pp in j['ops'][j['k']:])
        if r_ == 'MDD': return max(j['due'], now + rem)
        return j['qin']
    def weldh(j): return sum(p for s, p in j['ops'][j['k']:] if s == 'Weld')
    def try_start(s, now):
        while Q[s] and busy[s] < STATIONS[s] and not (s == 'Weld' and now < downuntil):
            j = min(Q[s], key=lambda x: prio(x, s, now)); Q[s].remove(j)
            busy[s] += 1; p = j['ops'][j['k']][1]
            if s == 'Weld': inproc[j['id']] = now + p
            push(now + p, 'fin', (j['id'], ver[j['id']]))
    def enter(j, now):
        s = j['ops'][j['k']][0]; j['qin'] = now; Q[s].append(j); try_start(s, now)
    def release_jobs(now):
        nonlocal weld_load
        pool.sort(key=lambda x: x['due']); i = 0
        while i < len(pool):
            j = pool[i]; w = weldh(j)
            if release == 'load' and w > 0 and weld_load + w > B and weld_load > 1e-6:
                i += 1; continue
            pool.pop(i); j['rel'] = now; weld_load += w; enter(j, now)
    J = {j['id']: j for j in jobs}
    while ev:
        t, _, typ, d = heapq.heappop(ev)
        if typ == 'arr':
            j = J[d]
            backlog = sum(a['pweld'] for a in active if not a['weld_done'])     # planned welder hours ahead
            j['backlog'] = backlog
            if quote == 'fit':
                c = coef
                j['quote'] = (c[0] + c[1] * backlog + c[2] * j['pwork'] + c[3] * j['pweld'] + c[4] * j['nops'] + m) * 8.0
            else:
                j['quote'] = QUOTE_RULES[quote](j, backlog, m)
            j['due'] = t + j['quote']
            active.append(j)
            if release == 'push': j['rel'] = t; enter(j, t)
            else: pool.append(j); release_jobs(t)
        elif typ == 'fin':
            jid, v = d
            if v != ver[jid]: continue
            j = J[jid]; s = j['ops'][j['k']][0]; busy[s] -= 1
            if s == 'Weld':
                inproc.pop(jid, None); weld_load -= j['ops'][j['k']][1]; j['weld_done'] = True
                if j in active: active.remove(j)
            j['k'] += 1
            if j['k'] < len(j['ops']): enter(j, t)
            else:
                j['done'] = t
                if j in active: active.remove(j)
            try_start(s, t)
            if release != 'push': release_jobs(t)
        elif typ == 'down':
            downuntil = t + d
            for jid, f in list(inproc.items()):
                ver[jid] += 1; inproc[jid] = f + d; push(f + d, 'fin', (jid, ver[jid]))
            push(t + d, 'up', None)
        elif typ == 'up':
            try_start('Weld', t)
    return jobs


def measure(jobs, w0=WARM, w1=WARM + WEEKS):
    sel = [j for j in jobs if w0 * HPW <= j['arr'] < w1 * HPW]
    q = np.array([j['quote'] / 8 for j in sel]); lt = np.array([(j['done'] - j['arr']) / 8 for j in sel])
    late = lt - q
    return dict(ot=float((late <= 1e-9).mean() * 100), quote=float(q.mean()), lt=float(lt.mean()),
                tard=float(np.maximum(late, 0).mean()), early=float(np.maximum(-late, 0).mean()),
                p95late=float(np.percentile(np.maximum(late, 0), 95)), n=len(sel))


SCHED = {'FIFO': dict(rule='FIFO'), 'Rec': dict(rule='MDD', bn_rule=True, release='load')}


def run(seed, quote, m, sched='FIFO', coef=None, rate=12.4, spike=None, down=None):
    return simulate(make_orders(seed, rate, spike=spike), quote, m, coef=coef, down=down, **SCHED[sched])
