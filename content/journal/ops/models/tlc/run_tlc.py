import json, numpy as np, tlc_model as T, tlc_risk as R
def lines(res): return [(l["part"], l["region"], l["mode"], l["orders"], l["share"]) for l in res["lines"]]
plans = {"price_only": T.price_only_plan(), "landed_price": T.landed_price_plan(),
         "tlc_optimal": lines(T.solve("base")),
         "tlc_dual": lines(T.solve("base", dual={"operator": "MX", "lock": "CA", "roller": "MX", "handle": "MX"})),
         "north_america": lines(T.solve("cn_broad"))}
out = {"plans": plans, "det": {}, "mc": {}, "scen": {}}
for nm, pl in plans.items():
    out["det"][nm] = T.evaluate_fixed(pl, "base")
    out["scen"][nm] = {sc: T.evaluate_fixed(pl, sc)["total"] for sc in T.SCENARIOS}
    a = R.simulate(pl, n=20000); out["mc"][nm] = R.summary(a)
    np.save(f"mc_{nm}.npy", a)
    print(nm, out["det"][nm]["total"], out["scen"][nm], out["mc"][nm])
json.dump(out, open("results_v1.json", "w"), indent=1)
