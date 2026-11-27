import json, numpy as np, copy, math
import spares_model as M
from scipy import stats
R = json.load(open("spares_results.json"))
res, sc = M.evaluate()
resN, _ = M.evaluate(nominal=True)
P = {p["id"]: p for p in M.PARTS}
pol = {}
for r in R["parts"]:
    i = r["id"]
    pol.setdefault("normal", {})[i] = r["normal"]; pol.setdefault("ready95", {})[i] = r["ready95"]; pol.setdefault("fill95", {})[i] = r["fill95"]
    pol.setdefault("one", {})[i] = 1; pol.setdefault("robust", {})[i] = r["S_robust"]
    pol.setdefault("nominal", {})[i] = int(np.argmin(resN[i]["total"].mean(0)))
    pol.setdefault("none", {})[i] = 0
port = {}
for k, ss in pol.items():
    tot = sum(res[i]["total"][:, s] for i, s in ss.items())
    hold = sum(res[i]["hold"][:, s] for i, s in ss.items())
    down = sum(res[i]["down"][:, s] for i, s in ss.items())
    lost = sum(res[i]["lost"][:, s] for i, s in ss.items())
    so = sum(res[i]["stockouts"][:, s] for i, s in ss.items())
    value = sum(P[i]["cost"] * s for i, s in ss.items())
    rst = sum(res[i]["restarts"][:, s] for i, s in ss.items())
    port[k] = dict(restarts=float(rst.mean()), S=ss, total=float(tot.mean()), total_p5=float(np.percentile(tot, 5)), total_p95=float(np.percentile(tot, 95)),
                   hold=float(hold.mean()), down=float(down.mean()), lost_h=float(lost.mean()), stockouts=float(so.mean()), value=value)
    print(f"{k:10s} value {value:>8,} total {tot.mean():>10,.0f} hold {hold.mean():>8,.0f} down {down.mean():>10,.0f} lost h {lost.mean():6.1f} so {so.mean():.2f}  S={list(ss.values())}")
# regret of robust portfolio vs per-scenario best per part
best = sum(res[i]["total"].min(1) for i in P)
rob = sum(res[i]["total"][:, pol["robust"][i]] for i in P)
print("robust regret mean", (rob - best).mean(), "P95", np.percentile(rob - best, 95))
R["portfolio"] = port; R["robust_regret"] = dict(mean=float((rob - best).mean()), p95=float(np.percentile(rob - best, 95)))
R["nominal_S"] = pol["nominal"]
# screening index: value of first spare vs its holding cost
idx = []
for i, p in P.items():
    ch = M.RATE_TH * 300 * p["cap"]; L = p["lt"] * 168 * M.OP; hold1 = 0.25 * p["cost"]
    first = p["lam"] * p["K"] * L * ch if p["N"] == p["K"] else None
    pair = (3 * p["lam"]) * (2 * p["lam"]) if p.get("hot") else (p["K"] * p["lam"]) ** 2
    idx2 = None if p["N"] == p["K"] else pair * L ** 2 * ch / (2 * M.HOURS) / hold1
    sim_saving = float(res[i]["down"][:, 0].mean() - res[i]["down"][:, 1].mean())
    idx.append(dict(id=i, index=(first / hold1) if first else None, index2=idx2, sim_ratio=sim_saving / float(res[i]["hold"][:, 1].mean()), redundant=p["N"] > p["K"]))
    print(i, "index", None if first is None else round(first / hold1, 2), "sim ratio", round(sim_saving / res[i]["hold"][:, 1].mean(), 2))
R["screen"] = idx
json.dump(R, open("spares_results.json", "w"), indent=1, default=float)
