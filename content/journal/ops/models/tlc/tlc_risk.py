"""Risk layer: Monte Carlo of freight, FX, tariff scenario and China supply disruption for fixed sourcing plans. V1."""
import json, math
import numpy as np
import tlc_model as T

RNG_SEED = 2026
N_YEARS = 20000
P_SCEN = {"base": 0.6, "us_noremit": 0.2, "cn_broad": 0.2}      # illustrative stress-test weights
P_DISRUPT = 0.15                                                   # chance per year of an ocean/port disruption on the China lane
DELAY = (28, 56)                                                   # extra days, uniform
SPOT_PREMIUM = 0.15                                                # domestic spot buy premium over the Canadian list price
SPOT_FRAC = 1.0                                                    # share of the uncovered gap a spot buy or air freight can fill
SHORT_COST = 0.0                                                   # cost per part unit short (line-down / lost margin), CAD
BACKUP_RAMP = 2.0                                                  # a 30% backup can lift to 2x its normal volume during a disruption


def plan_cost(plan, sc_name, feu_usd, fx, lcl_scale):
    """Total landed cost of a plan with FX applied to imported prices and LCL rates scaled with the container market."""
    old = (T.FX, T.LCL_RT, {k: dict(P["p"]) for k, P in T.PARTS.items()})
    try:
        T.FX = fx
        T.LCL_RT = old[1] * lcl_scale
        for k, P in T.PARTS.items():
            for r in P["p"]:
                if r != "CA":
                    P["p"][r] = old[2][k][r] * fx / 1.38
        return T.evaluate_fixed(plan, sc_name, feu_usd)["total"]
    finally:
        T.FX, T.LCL_RT = old[0], old[1]
        for k, P in T.PARTS.items():
            P["p"].update(old[2][k])


def disruption_cost(plan, delay):
    """Extra cost of covering a China-lane delay: demand in the gap beyond safety stock, covered by a backup supplier
    (if dual sourced) at its normal landed price, else by air from China or a domestic spot buy, whichever is cheaper.
    Cost counted as the premium over the planned unit cost."""
    cost = 0.0; extra = 0.0
    by_part = {}
    for (k, r, m, n, s) in plan:
        by_part.setdefault(k, []).append((r, m, n, s))
    for k, streams in by_part.items():
        P = T.PARTS[k]; d = P["D"] / 365
        cn = [x for x in streams if x[0] == "CN"]
        if not cn:
            continue
        r, m, n, s = cn[0]
        c = T.stream_cost(k, r, m, n, s, T.SCENARIOS["base"])
        gap = max(0.0, d * s * delay - c["ss"])
        if gap <= 0:
            continue
        planned_unit = c["unit_landed"]
        backup = [x for x in streams if x[0] != "CN"]
        covered = 0.0
        if backup:
            br, bm, bn, bs = backup[0]
            cap = d * bs * (BACKUP_RAMP - 1) * delay
            covered = min(gap, cap)
            bc = T.stream_cost(k, br, bm, bn, bs, T.SCENARIOS["base"])
            extra += covered * max(0.0, bc["unit_landed"] - planned_unit)
        rest = gap - covered
        air_unit = P["p"]["CN"] + (T.AIR_KG * max(P["kg"], P["m3"] * 167))
        spot_unit = P["p"]["CA"] * (1 + SPOT_PREMIUM)
        fill = rest * SPOT_FRAC
        extra += fill * max(0.0, min(air_unit, spot_unit) - planned_unit) + (rest - fill) * SHORT_COST
    return cost + extra


def simulate(plan, seed=RNG_SEED, n=N_YEARS):
    rng = np.random.default_rng(seed)
    feu = np.exp(rng.normal(math.log(4500), 0.45, n))          # median US$4,500; ~5-95%: 2,150-9,450
    fx = rng.normal(1.38, 0.05, n)
    sc = rng.choice(list(P_SCEN), p=list(P_SCEN.values()), size=n)
    dis = rng.random(n) < P_DISRUPT
    delay = rng.uniform(*DELAY, n)
    # cache by scenario on a grid to keep it fast: evaluate exactly for each draw (plans are small)
    out = np.empty(n)
    for i in range(n):
        c = plan_cost(plan, sc[i], feu[i], fx[i], feu[i] / T.FEU_USD)
        if dis[i]:
            c += disruption_cost(plan, delay[i])
        out[i] = c
    return out


def summary(a):
    return dict(mean=round(float(a.mean())), p50=round(float(np.percentile(a, 50))), p95=round(float(np.percentile(a, 95))),
                sd=round(float(a.std())), se=round(float(a.std() / math.sqrt(len(a)))))


if __name__ == "__main__":
    import time
    t = time.time()
    plans = {}
    plans["price_only"] = T.price_only_plan()
    base = T.solve("base")
    plans["tlc_optimal"] = [(l["part"], l["region"], l["mode"], l["orders"], l["share"]) for l in base["lines"]]
    dual = T.solve("base", dual={"operator": "MX", "lock": "US", "weather": "MX", "spacer": "CA", "handle": "MX"})
    plans["tlc_dual"] = [(l["part"], l["region"], l["mode"], l["orders"], l["share"]) for l in dual["lines"]]
    res = {}
    for nm, pl in plans.items():
        a = simulate(pl, n=4000)
        res[nm] = summary(a); print(nm, res[nm], pl, round(time.time() - t, 1))
