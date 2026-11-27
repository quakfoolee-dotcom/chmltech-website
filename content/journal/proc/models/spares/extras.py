import json, numpy as np, copy
import spares_model as M
R = json.load(open("spares_results.json")); P = {p["id"]: p for p in M.PARTS}
def robust(parts, n=2000, **kw):
    res, sc = M.evaluate(n=n, parts=parts, **kw)
    return {p["id"]: dict(S=int(np.argmin(res[p["id"]]["total"].mean(0))), total=res[p["id"]]["total"].mean(0).tolist(),
                          lost=res[p["id"]]["lost"].mean(0).tolist()) for p in parts}
X = {}
# failure-rate uncertainty
for sig in (0.0, 1.0):
    M.LAM_SIGMA = sig; r = robust(M.PARTS); X[f"sigma_{sig}"] = {k: v["S"] for k, v in r.items()}; print("sigma", sig, X[f"sigma_{sig}"])
M.LAM_SIGMA = 0.5
# low-value world: margin and carry at the unfavourable ends (fixed), compare S
M_SCEN = copy.deepcopy(M.SCEN)
M.SCEN["margin"] = (150, 150, 150 + 1e-9); M.SCEN["carry"] = (0.35, 0.35, 0.35 + 1e-9)
r = robust(M.PARTS); X["lean"] = {k: v["S"] for k, v in r.items()}; print("lean", X["lean"])
M.SCEN.update(M_SCEN)
# redundancy: reactor feed pump seal without an installed spare pump
p1 = dict(P["P1"], id="P1x", base_id="P1", N=1, K=1); r = robust([P["P1"], p1]); X["redundancy"] = r; print("redund", {k: (v["S"], [round(t) for t in v["total"]]) for k, v in r.items()})
# repairable: compressor motor rewound in 4 weeks; gearbox repaired in 6 weeks
rp = [dict(P["P9"], id="P9r", base_id="P9", lt=4), dict(P["P6"], id="P6r", base_id="P6", lt=6), dict(P["P10"], id="P10r", base_id="P10", lt=8)]
r = robust(rp); X["repairable"] = r; print("repair", {k: (v["S"], [round(t) for t in v["total"]]) for k, v in r.items()})
# pooling across three sister plants, 48 h transfer
X["pool"] = {}
for pid in ("P6", "P9", "P10"):
    res, sc = M.evaluate(n=2000, parts=[P[pid]], m=3, transfer_h=48.0)
    own = R["parts"][[q["id"] for q in R["parts"]].index(pid)]["mean_total"]
    # pooled holding: S shared by three plants -> holding per plant = S/3 x cost x carry
    pooled = (res[pid]["down"].mean(0) + res[pid]["hold"].mean(0) / 3).tolist()
    X["pool"][pid] = dict(own=own, pooled_per_plant=pooled, lost_pooled=res[pid]["lost"].mean(0).tolist())
    print("pool", pid, "own", [round(x) for x in own], "pooled/plant", [round(x) for x in pooled])
# decision map, analytic (single unit, no buffer): optimal S for demand in lead time m and ratio rho = c_h*8000*f/(r*C), operating hours
ms = np.geomspace(1e-3, 3, 120); rhos = np.geomspace(0.1, 1e5, 120)
grid = np.zeros((len(rhos), len(ms)), int)
for a, m in enumerate(ms):
    ebo = np.array([M.palm_ebo(S, m) for S in range(8)])
    for b, rho in enumerate(rhos):
        grid[b, a] = int(np.argmin(np.arange(8) + rho * ebo))
X["map"] = dict(m=ms.tolist(), rho=rhos.tolist(), S=grid.tolist())
R["extras"] = X
json.dump(R, open("spares_results.json", "w"), indent=1, default=float)
