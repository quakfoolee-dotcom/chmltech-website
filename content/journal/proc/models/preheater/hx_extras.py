"""Sensitivity runs for the preheater paper: linear fouling, a 12-month run, condensate back pressure for stall,
and the cost of area ten times the correlation."""
import json, numpy as np, hx_model as H
res = {}
areas = [6, 7, 8, 9, 10]
for lab, kw in (("linear", dict(linear=True)), ("run12", dict(run_months=12))):
    out, sc = H.run(areas, **kw); res[lab] = {}
    for A in areas:
        o = out[A]; tot = H.installed_cost(A) * H.CRF + o["lost_cost"] + o["clean_cost"]
        res[lab][str(A)] = dict(cleans_y=float(o["cleans_y"].mean()), total=float(tot.mean()), p_cut=float(np.mean(np.isfinite(o["first_cut"]))),
                                stallN=float(o["stallN"].mean()), stallT=float(o["stallT"].mean()))
        print(lab, A, {k: round(v, 4) for k, v in res[lab][str(A)].items()})
res["stall_bp"] = {}
for bp in (0.1, 0.3):
    out, sc = H.run([5.42, 6.5, 8], stall_bp=bp); res["stall_bp"][str(bp)] = {}
    for A in (5.42, 6.5, 8):
        res["stall_bp"][str(bp)][str(A)] = dict(stallN=float(out[A]["stallN"].mean()), stallT=float(out[A]["stallT"].mean()))
        print("bp", bp, A, res["stall_bp"][str(bp)][str(A)])
R = json.load(open("hx_results.json")); base = H.installed_cost(0.0)
c10 = {}
for a, d in R["by_area"].items():
    extra = (d["cost"] - base) * 10 + base
    c10[a] = d["total"] - d["cost"] * H.CRF + extra * H.CRF
res["area_cost_x10"] = c10; print("area cost x10:", {k: round(v) for k, v in c10.items()})
json.dump(res, open("hx_extras.json", "w"), indent=1)
