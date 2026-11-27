"""Summarises the 20 synthetic plant histories: fouling-estimate error and forecast error by approach."""
import json, numpy as np
R = json.load(open("twin_results.json")); M = [0.5, 1, 1.5, 2, 3]
S = {"n": len(R)}
for k in ("P", "O", "H"):
    S[f"rmse_{k}"] = float(np.median([r["rf"][k]["rmse"] for r in R])); S[f"bias_{k}"] = float(np.median([r["rf"][k]["bias"] for r in R]))
    S[f"rmse_td_{k}"] = float(np.median([r["rf"][k]["rmse_td"] for r in R]))
S["mae"] = {k: float(np.median([r["extrap_mae"][k] for r in R])) for k in ("P", "O", "H", "M")}
S["mae_p90"] = {k: float(np.percentile([r["extrap_mae"][k] for r in R], 90)) for k in ("P", "O", "H", "M")}
fc = {}
for k in ("P", "O", "H", "M"):
    rows = []
    for j, mo in enumerate(M):
        errs = []; within20 = 0; fails = 0; nvalid = 0
        for r in R:
            t = r["truth"][2]; f = r["fc"][k][j]
            if t is None or not np.isfinite(t) or mo * 8000 / 12 >= t: continue   # only forecasts made before the limit is reached
            nvalid += 1
            if f is None or not np.isfinite(f): fails += 1; errs.append(1.0); continue
            e = abs(f - t) / t; errs.append(min(e, 1.0)); within20 += e <= 0.2
        rows.append(dict(month=mo, n=nvalid, median_err=float(np.median(errs)) if errs else None, share_within20=within20 / nvalid if nvalid else None, no_answer=fails))
    fc[k] = rows
S["forecast"] = fc
S["truth3"] = [r["truth"][2] for r in R]
json.dump(S, open("twin_summary.json", "w"), indent=1, default=float)
print(json.dumps({k: v for k, v in S.items() if k != "truth3"}, indent=1, default=float))
