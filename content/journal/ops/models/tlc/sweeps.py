"""Freight-rate and shortage-cost sweeps (Figures 2 and 4 of Vol. 106(5)). Run after run_tlc.py. Writes feu_sweep.json, short_sweep.json."""
import json
import tlc_model as T, tlc_risk as R


def lines(res): return [(l["part"], l["region"], l["mode"], l["orders"], l["share"]) for l in res["lines"]]


base = T.solve("base"); plan_7500 = lines(base)
feu = []
LCL0 = T.LCL_RT
for f in [1500, 2000, 2500, 3000, 4000, 5000, 6000, 7500, 9000, 11000]:
    T.LCL_RT = LCL0 * f / T.FEU_USD           # LCL rates move in proportion to the container rate
    opt = T.solve("base", feu_usd=f)
    feu.append(dict(feu=f, optimal=round(opt["totals"]["total"]), containers=opt.get("containers"),
                    price_only=round(T.evaluate_fixed(T.price_only_plan(), "base", feu_usd=f)["total"]),
                    plan_7500=round(T.evaluate_fixed(plan_7500, "base", feu_usd=f, containers=base.get("containers"))["total"]),
                    china_parts=sum(1 for l in opt["lines"] if l["region"] == "CN")))
    print(feu[-1])
T.LCL_RT = LCL0
json.dump(feu, open("feu_sweep.json", "w"), indent=1)

plans = {"tlc_optimal": plan_7500,
         "tlc_dual": lines(T.solve("base", dual={"operator": "MX", "lock": "CA", "roller": "MX", "handle": "MX"})),
         "north_america": lines(T.solve("cn_broad"))}
import sys
if "--feu-only" in sys.argv: raise SystemExit
R.SPOT_FRAC = 0.0                     # no spot market or air cover: every unit short costs SHORT_COST
short = {}
for s in [0, 25, 50, 75, 100, 125, 150, 175, 200, 250, 300]:
    R.SHORT_COST = float(s)
    short[str(s)] = {k: {kk: round(v) for kk, v in R.summary(R.simulate(p, n=10000)).items() if kk in ("mean", "p95")} for k, p in plans.items()}
    print(s, short[str(s)])
json.dump(short, open("short_sweep.json", "w"), indent=1)
