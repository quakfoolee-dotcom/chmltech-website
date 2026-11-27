"""Critical spare parts under uncertainty - Chmltech Online Journal, Vol. 106 (spares paper).
How many of each critical spare to hold for the 50,000 t/y plant of Issues 8 and 9.

Demand for a spare comes from equipment failures (Poisson, with an uncertain rate). Each failure takes a part
from stock if there is one and places a replacement order ((S-1, S) one-for-one policy). The plant loses
production when fewer equipment units are working than it needs, after any buffer is used up. A discrete-event
simulation gives the downtime for each stock level S in each scenario; holding cost is S x unit cost x carrying
rate. The answer is compared with the normal-formula safety stock, a Poisson service level, 'one of each' and
the cost optimum at nominal values. Python 3 with NumPy and SciPy."""
import heapq, json, math
import numpy as np
from scipy import stats

RATE_TH = 6.25          # t/h of product (50,000 t/y over 8,000 h)
HOURS = 8000.0          # operating hours a year: the failure clock, lead times and downtime all run in operating hours
OP = HOURS / 8760.0     # operating hours per calendar hour (lead times and repairs are quoted in calendar time)
SMAX = 4

# part: name, equipment, units installed N, units needed K, failure rate per running unit-year (most likely),
# lead time weeks (most likely), unit cost C$, repair hours once the part is on hand, share of plant capacity
# lost while fewer than K units work, buffer hours before that loss starts, repairable turnaround weeks (or None)
PARTS = [
 dict(id="P1",  name="Mechanical seal cartridge", eq="Reactor feed pumps P-101A/B", N=2, K=1, lam=0.20, lt=6,  cost=4500,   rep=12, cap=1.0, buf=0),
 dict(id="P2",  name="Bearing set",               eq="Reactor feed pumps P-101A/B", N=2, K=1, lam=0.10, lt=2,  cost=600,    rep=12, cap=1.0, buf=0),
 dict(id="P3",  name="Mechanical seal cartridge", eq="Product transfer pumps P-201A/B", N=2, K=1, lam=0.20, lt=6, cost=4000, rep=12, cap=1.0, buf=12),
 dict(id="P4",  name="Motor, 7.5 kW explosion-proof", eq="Reactor feed pumps P-101A/B", N=2, K=1, lam=0.03, lt=10, cost=6000, rep=8, cap=1.0, buf=0),
 dict(id="P5",  name="Rotating assembly",         eq="Cooling water pumps P-301A/B/C", N=3, K=2, lam=0.15, lt=12, cost=18000, rep=24, cap=1.0, buf=0),
 dict(id="P6",  name="Gearbox",                   eq="Reactor agitator A-101", N=1, K=1, lam=0.05, lt=20, cost=45000,   rep=48, cap=1.0, buf=0),
 dict(id="P7",  name="Double mechanical seal",    eq="Reactor agitator A-101", N=1, K=1, lam=0.25, lt=8,  cost=15000,   rep=24, cap=1.0, buf=0),
 dict(id="P8",  name="Valve set",                 eq="Recycle compressor K-101", N=1, K=1, lam=0.80, lt=4, cost=8000,   rep=12, cap=1.0, buf=0),
 dict(id="P9",  name="Motor, 250 kW",             eq="Recycle compressor K-101", N=1, K=1, lam=0.02, lt=26, cost=90000, rep=72, cap=1.0, buf=0),
 dict(id="P10", name="Tube bundle",               eq="Feed preheater E-101", N=1, K=1, lam=0.02, lt=30, cost=120000,    rep=96, cap=0.3, buf=0),
 dict(id="P11", name="Valve trim kit",            eq="Flow control valve FCV-101", N=1, K=1, lam=0.10, lt=8, cost=5000, rep=8, cap=0.1, buf=0),
 dict(id="P12", name="Drive power module",        eq="Pump drives (option B)", N=2, K=1, lam=0.07, lt=8, cost=3000, rep=8, cap=1.0, buf=0),
 dict(id="P13", name="Pressure transmitter",      eq="Reactor trip, 2-out-of-3", N=3, K=2, lam=0.05, lt=3, cost=3500, rep=4, cap=1.0, buf=0, hot=True),
]

# uncertain inputs of a scenario (min, most likely, max); failure-rate factor is lognormal per part
SCEN = dict(margin=(150, 300, 500), carry=(0.15, 0.25, 0.35), lt_f=(0.8, 1.0, 1.5), restart=(4, 8, 16))
LAM_SIGMA = 0.5          # lognormal sigma of each part's failure-rate factor (few records per part)
LT_CV = 0.2              # order-to-order variation in lead time


def tri(rng, a, m, b, n):
    return rng.triangular(a, m, b, n)


def simulate(p, S, lam, lt_h, cost_h, restart_h, T, rng, m=1, transfer_h=0.0):
    """Discrete-event simulation of m identical equipment groups sharing one stock of S parts.
    Returns (downtime cost per year, lost full-rate hours per year, stockouts per year)."""
    N, K, buf, cap = p["N"], p["K"], p["buf"] * OP, p["cap"]; rep = p["rep"] * OP
    up = [N] * m; down_since = [None] * m; stock = S
    ev = []; waiting = []; lost_h = 0.0; restarts = 0; stockouts = 0
    hot = p.get("hot", False)                    # hot standby (voting instruments): every working unit can fail
    def run(g): return up[g] if hot else min(up[g], K)
    def sched_fail(g, t):
        r = run(g)
        if r > 0: heapq.heappush(ev, (t + rng.exponential(HOURS / (lam * r)), "fail", g, ver[g]))
    ver = [0] * m
    for g in range(m): sched_fail(g, 0.0)
    def close(g, t):
        nonlocal lost_h, restarts
        dur = t - down_since[g]
        if dur > buf:
            lost_h += (dur - buf) * cap
            if cap >= 1.0: restarts += 1
        down_since[g] = None
    while ev:
        t, kind, g, v = heapq.heappop(ev)
        if t > T: break
        if kind == "fail":
            if v != ver[g]: continue
            up[g] -= 1; ver[g] += 1
            if up[g] < K and down_since[g] is None: down_since[g] = t
            heapq.heappush(ev, (t + lt_h * rng.lognormal(-LT_CV ** 2 / 2, LT_CV), "arrive", -1, 0))
            if stock > 0:
                stock -= 1; heapq.heappush(ev, (t + rep + (transfer_h if m > 1 else 0), "fixed", g, 0))
            else:
                waiting.append(g); stockouts += 1
            sched_fail(g, t)
        elif kind == "arrive":
            if waiting:
                w = waiting.pop(0); heapq.heappush(ev, (t + rep + (transfer_h if m > 1 else 0), "fixed", w, 0))
            else:
                stock += 1
        else:  # repair finished
            up[g] += 1; ver[g] += 1
            if up[g] >= K and down_since[g] is not None: close(g, t)
            sched_fail(g, t)
    for g in range(m):
        if down_since[g] is not None: close(g, T)
    yrs = T / HOURS
    cost = (lost_h + restarts * restart_h) * cost_h / yrs
    return cost / m, lost_h / yrs / m, stockouts / yrs / m, restarts / yrs / m


def scenarios(n, seed=11):
    """Same draws for every run with the same n and seed: one failure-rate factor per base part (P1...P13)."""
    rng = np.random.default_rng(seed)
    sc = {k: tri(rng, *v, n) for k, v in SCEN.items()}
    z = rng.standard_normal(size=(n, len(PARTS)))
    sc["lam_f"] = np.exp(LAM_SIGMA * z - LAM_SIGMA ** 2 / 2)
    sc["col"] = {p["id"]: j for j, p in enumerate(PARTS)}
    return sc


def evaluate(n=2000, T_years=200, seed=11, parts=PARTS, m=1, transfer_h=0.0, nominal=False):
    sc = scenarios(n, seed)
    if nominal:
        sc = {k: (np.full(n, SCEN[k][1]) if k in SCEN else v if k == "col" else np.ones_like(v)) for k, v in sc.items()}
    T = T_years * HOURS
    out = {}
    for p in parts:
        j = sc["col"][p.get("base_id", p["id"])]
        down = np.zeros((n, SMAX + 1)); lost = np.zeros_like(down); so = np.zeros_like(down); rs_ = np.zeros_like(down)
        for i in range(n):
            lam = p["lam"] * sc["lam_f"][i, j]; lt_h = p["lt"] * 168 * OP * sc["lt_f"][i]
            cost_h = RATE_TH * sc["margin"][i]; rs = sc["restart"][i]
            for S in range(SMAX + 1):
                rng = np.random.default_rng([seed, j, i])            # common random numbers across S
                down[i, S], lost[i, S], so[i, S], rs_[i, S] = simulate(p, S, lam, lt_h, cost_h, rs, T, rng, m, transfer_h * OP)
        hold = np.outer(sc["carry"], np.arange(SMAX + 1)) * p["cost"]
        out[p["id"]] = dict(down=down, lost=lost, stockouts=so, restarts=rs_, hold=hold, total=down + hold)
    return out, sc


def palm_ebo(S, mlt):
    """Expected backorders for one-for-one replenishment with Poisson demand of mean mlt in a lead time."""
    x = np.arange(0, int(mlt + 12 * math.sqrt(mlt + 1) + 30))
    p = stats.poisson.pmf(x, mlt)
    return float(np.sum(np.clip(x - S, 0, None) * p))


def policies(p, carry=0.25):
    """Stock levels from the usual rules (base stock S; reorder when the inventory position falls to S - 1)."""
    d = p["lam"] * p["N"] if p.get("hot") else p["lam"] * p["K"]; mlt = d * p["lt"] / 52
    z = stats.norm.ppf(0.95)
    rop = max(0, int(round(mlt + z * math.sqrt(mlt))))               # textbook reorder point m + z sqrt(m), rounded
    s_normal = rop + 1                                               # base stock = reorder point + 1 (one-for-one)
    s_ready = int(stats.poisson.ppf(0.95, mlt))                      # 95% ready rate: P(no part owed at a random moment) = P(X <= S)
    s_fill = int(stats.poisson.ppf(0.95, mlt)) + 1                   # 95% fill rate: P(a failure finds a part) = P(X <= S - 1)
    return dict(d=d, mlt=mlt, rop=rop, normal=s_normal, ready95=s_ready, fill95=s_fill, one=1)


if __name__ == "__main__":
    import time
    t0 = time.time()
    res, sc = evaluate()
    R = dict(parts=[], const=dict(RATE_TH=RATE_TH, SMAX=SMAX, SCEN=SCEN, LAM_SIGMA=LAM_SIGMA, LT_CV=LT_CV))
    for p in PARTS:
        r = res[p["id"]]; mean_tot = r["total"].mean(0); S_rob = int(np.argmin(mean_tot))
        best = np.argmin(r["total"], axis=1)
        pol = policies(p)
        R["parts"].append(dict(**{k: p[k] for k in p}, **pol, S_robust=S_rob,
                               mean_total=mean_tot.tolist(), mean_down=r["down"].mean(0).tolist(),
                               mean_lost=r["lost"].mean(0).tolist(), mean_hold=r["hold"].mean(0).tolist(),
                               mean_restarts=r["restarts"].mean(0).tolist(),
                               p_best=[float(np.mean(best == s)) for s in range(SMAX + 1)]))
        print(f'{p["id"]:4s} {p["name"][:24]:24s} d={pol["d"]:.3f} mLT={pol["mlt"]:.3f} normal={pol["normal"]} ready={pol["ready95"]} fill={pol["fill95"]} '
              f'robust={S_rob}  tot={[round(x) for x in mean_tot]}  lost_h={[round(x,2) for x in r["lost"].mean(0)]}')
    json.dump(R, open("spares_results.json", "w"), indent=1, default=float)
    print("time", round(time.time() - t0, 1))
