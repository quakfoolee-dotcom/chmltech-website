"""Hybrid digital twin for fouling of the feed preheater E-101 - Chmltech Online Journal (hybrid twin paper).
Synthetic plant history: three 24-month runs of E-101 with true fouling (Kern-Seaton, different level each run),
a true tube-side coefficient 12% below the correlation, seasonal feed temperature, turndown periods and noisy,
slowly drifting instruments. Four monitors estimate the fouling resistance and forecast when the exchanger will
force a rate cut at the design case:
  P  physics only  - U from measured duty and LMTD, fouling = 1/U_meas - 1/U_clean(correlation)
  M  machine learning only - gradient boosting maps operating data and time since cleaning to shell pressure
  H  hybrid - physics structure, clean coefficient recalibrated by regression on the clean weeks after each
     cleaning, Kern-Seaton curve fitted to the estimated fouling and propagated to the design case
Python 3 with NumPy, SciPy and scikit-learn."""
import json, math
import numpy as np
from scipy.optimize import least_squares
from sklearn.ensemble import GradientBoostingRegressor

CP, KF, T_OUT = 2000.0, 0.13, 80.0
OD, ID, TPP, A, PASSES = 0.01905, 0.01575, 12, 6.0, 2
L = A / (PASSES * TPP * math.pi * OD)
R_WALL = OD * math.log(OD / ID) / (2 * 45.0)
RF_O = 1e-4
rho = lambda T: 900.0 - 0.95 * (T - 20.0)
mu = lambda T: 1.6e-3 * np.exp(-0.018 * (T - 20.0))
tsat = lambda p: 1810.94 / (8.14019 - np.log10((p + 1.01325) * 750.062)) - 244.485
psat = lambda T: 10 ** (8.14019 - 1810.94 / (T + 244.485)) / 750.062 - 1.01325
DT_H = 4.0                                  # hours per record
RUN_H = 16000.0                             # 24 months of operation
TS_MAX = float(tsat(2.7))                   # highest shell temperature available
DESIGN = dict(m=9569.0, Tin=6.8)            # design case of the preheater paper
CAL_H = 120.0                               # clean-period calibration window after each cleaning, operating hours


def h_tube(m, T, f_hi=1.0):
    v = m / 3600 / rho(T) / (TPP * math.pi * ID ** 2 / 4); Re = rho(T) * v * ID / mu(T); Pr = CP * mu(T) / KF
    if isinstance(f_hi, str): f_hi = 0.88 * (Re / 17800.0) ** 0.15        # "true": plant 12% below the correlation at design flow, more at low Re
    f = (0.79 * np.log(np.maximum(Re, 2300)) - 1.64) ** -2
    nu_t = (f / 8) * (Re - 1000) * Pr / (1 + 12.7 * np.sqrt(f / 8) * (Pr ** (2 / 3) - 1))
    nu_l = np.maximum(3.66, 1.86 * (Re * Pr * ID / L) ** (1 / 3))
    return f_hi * np.where(Re >= 2300, np.maximum(nu_t, nu_l), nu_l) * KF / ID, Re


def U_of(m, T, rf, f_hi=1.0, h_o=8000.0):
    hi, _ = h_tube(m, T, f_hi)
    return 1 / (OD / (hi * ID) + R_WALL + 1 / h_o + rf * OD / ID + RF_O)


def ts_req(m, Tin, rf, f_hi=1.0, h_o=8000.0):
    E = np.exp(-U_of(m, (Tin + T_OUT) / 2, rf, f_hi, h_o) * A / (m / 3600 * CP))
    return (T_OUT - Tin * E) / (1 - E)


# ---------------- synthetic plant ----------------
TRUE = dict(f_hi="true", h_o=7000.0)
RUNS = [dict(rinf=3.0e-4, tau=2500.0), dict(rinf=4.5e-4, tau=3500.0), dict(rinf=2.2e-4, tau=2000.0)]


def plant(seed=5, runs=None):
    rng = np.random.default_rng(seed); recs = []
    runs = runs or RUNS
    t_abs = 0.0
    for r, run in enumerate(runs):
        n = int(RUN_H / DT_H)
        t = np.arange(n) * DT_H
        day = (t_abs + t) / 24.0
        Tin = 22.5 - 14.0 * np.cos(2 * np.pi * day / 365.0) + rng.normal(0, 1.5, n)           # outdoor tank, seasonal
        rate = np.clip(1.0 + 0.05 * rng.standard_normal(n), 0.85, 1.10)
        td = np.zeros(n, bool)                                                               # turndown campaigns
        for _ in range(4):
            s = rng.integers(0, n - 300); td[s:s + rng.integers(60, 240)] = True
        if r == 2: td[:] = td | ((day % 365) < 50)                                           # run 3: winter turndown, new regime
        m = 8690.0 * rate * np.where(td, 0.5, 1.0)
        rf = run["rinf"] * (1 - np.exp(-t / run["tau"]))
        Ts = ts_req(m, Tin, rf, **TRUE)
        lim = Ts > TS_MAX                                                                     # steam runs out: valve wide open
        Ts = np.minimum(Ts, TS_MAX)
        E = np.exp(-U_of(m, (Tin + T_OUT) / 2, rf, **TRUE) * A / (m / 3600 * CP))
        Tout_t = np.where(lim, Ts - (Ts - Tin) * E, T_OUT)
        p = psat(Ts)                                                                          # shell pressure (control holds 80 C)
        # instruments: flow +-2% noise and a slow drift, temperatures 0.3 K, pressure 0.015 bar
        drift = 1 + 0.015 * np.sin(2 * np.pi * t / RUN_H + r)
        recs.append(dict(run=r, t=t, t_abs=t_abs + t, m_true=m, Tin_true=Tin, rf_true=rf, p_true=p,
                         m=m * drift * (1 + rng.normal(0, 0.02, n)), Tin=Tin + rng.normal(0, 0.3, n),
                         Tout=Tout_t + rng.normal(0, 0.3, n), lim=lim, p=p + rng.normal(0, 0.015, n), td=td))
        t_abs += RUN_H + 500
    return recs


def u_measured(d):
    """Overall coefficient from measured duty and steam temperature; NaN where the shell is below 0.05 barg
    (stall region: condensate backs up, the uniform-condensing assumption fails)."""
    Ts = tsat(np.maximum(d["p"], -0.9)); Q = d["m"] / 3600 * CP * (d["Tout"] - d["Tin"])
    lm = ((Ts - d["Tin"]) - (Ts - d["Tout"])) / np.log((Ts - d["Tin"]) / (Ts - d["Tout"]))
    U = Q / (A * lm)
    return np.where(d["p"] > 0.05, U, np.nan)


def time_to_limit(rinf, tau, f_hi=1.0, h_o=8000.0, t0=0.0):
    """Operating hours from cleaning until the design case needs more than TS_MAX."""
    tt = np.arange(0, 60000, 50.0)
    rf = rinf * (1 - np.exp(-tt / tau))
    ts = ts_req(DESIGN["m"], DESIGN["Tin"], rf, f_hi, h_o)
    i = np.argmax(ts > TS_MAX)
    return float(tt[i]) if ts[i] > TS_MAX else np.inf


def ks_fit(t, rf, tau0=3000.0):
    ok = np.isfinite(rf)
    if ok.sum() < 10: return np.nan, np.nan
    res = least_squares(lambda x: x[0] * 1e-4 * (1 - np.exp(-t[ok] / x[1])) - rf[ok], [3.0, tau0],
                        bounds=([0.1, 200], [20.0, 30000]), loss="soft_l1", f_scale=0.3e-4)
    return res.x[0] * 1e-4, res.x[1]


def calibrate_offset(recs_train):
    """Physics with a constant correction: one factor on the tube-side coefficient from the clean weeks."""
    Y = []
    for d in recs_train:
        sel = (d["t"] < CAL_H) & np.isfinite(u_measured(d))
        Um = u_measured(d)[sel]; hi_corr, _ = h_tube(d["m"][sel], (d["Tin"][sel] + T_OUT) / 2)
        inv = (1 / Um - R_WALL - 1 / 8000.0 - RF_O) * ID / OD; ok = inv > 0
        Y += list(np.log((1 / inv[ok]) / hi_corr[ok]))
    c = float(np.exp(np.mean(Y)))
    return lambda Re: np.full_like(np.asarray(Re, float), c), c


def calibrate_clean(recs_train):
    """Hybrid step: on the first 120 h after each cleaning (fouling 2-11% of asymptote), regress the ratio of the
    measured to the correlation tube-side coefficient on Reynolds number; returns f_hi(Re) as a fitted power law."""
    X, Y = [], []
    for d in recs_train:
        sel = (d["t"] < CAL_H) & np.isfinite(u_measured(d))
        Um = u_measured(d)[sel]; m = d["m"][sel]; Tm = (d["Tin"][sel] + T_OUT) / 2
        hi_corr, Re = h_tube(m, Tm)
        inv_hi_meas = (1 / Um - R_WALL - 1 / 8000.0 - RF_O) * ID / OD      # what the clean tube side must be
        ok = inv_hi_meas > 0
        X += list(np.log(Re[ok])); Y += list(np.log((1 / inv_hi_meas[ok]) / hi_corr[ok]))
    b, a = np.polyfit(X, Y, 1)
    return lambda Re: np.exp(a + b * np.log(Re)), (float(np.exp(a + b * np.log(18000))), float(b))


def estimate_rf(d, f_fun=None):
    Um = u_measured(d); Tm = (d["Tin"] + T_OUT) / 2
    hi, Re = h_tube(d["m"], Tm)
    if f_fun is not None: hi = hi * f_fun(Re)
    Uc = 1 / (OD / (hi * ID) + R_WALL + 1 / 8000.0 + RF_O)
    return (1 / Um - 1 / Uc) * ID / OD


def daily(t, x):
    """Daily medians to suppress noise."""
    k = (t // 24).astype(int); out_t, out_x = [], []
    for kk in np.unique(k):
        s = (k == kk) & np.isfinite(x)
        if s.sum() >= 2: out_t.append(t[k == kk].mean()); out_x.append(np.median(x[s]))
    return np.array(out_t), np.array(out_x)



def draw_runs(seed):
    rng = np.random.default_rng(1000 + seed)
    return [dict(rinf=float(rng.triangular(1.5e-4, 3e-4, 6e-4)), tau=float(rng.triangular(1000, 2500, 6000))) for _ in range(3)]


MONTHS = [0.5, 1, 1.5, 2, 3]


def evaluate(seed, detail=False):
    runs = draw_runs(seed) if seed != 5 else RUNS
    recs = plant(seed, runs)
    truth = [time_to_limit(r["rinf"], r["tau"], **TRUE) for r in runs]
    f_H, calibH = calibrate_clean(recs[:2]); f_O, calibO = calibrate_offset(recs[:2])
    out = dict(seed=seed, runs=runs, truth=truth, calib_H=calibH, calib_O=calibO, rf={}, fc={})
    d = recs[2]
    est = {"P": estimate_rf(d), "O": estimate_rf(d, f_O), "H": estimate_rf(d, f_H)}
    tT, xT = daily(d["t"], d["rf_true"])
    for k, r in est.items():
        tt, xx = daily(d["t"], r); it = np.interp(tt, tT, xT)
        out["rf"][k] = dict(rmse=float(np.sqrt(np.mean((xx - it) ** 2))), bias=float(np.mean(xx - it)),
                            rmse_td=float(np.sqrt(np.nanmean(((r - d["rf_true"])[d["td"]]) ** 2))))
        if detail: out["rf"][k].update(t=tt.tolist(), x=xx.tolist())
    if detail: out["rf"]["true"] = dict(t=tT.tolist(), x=xT.tolist())
    # forecasts on run 3
    Xtr = np.column_stack([np.concatenate([x["m"] for x in recs[:2]]), np.concatenate([x["Tin"] for x in recs[:2]]), np.concatenate([x["t"] for x in recs[:2]])])
    ytr = np.concatenate([x["p"] for x in recs[:2]])
    hi0, Re0 = h_tube(np.array([DESIGN["m"]]), (DESIGN["Tin"] + T_OUT) / 2)
    tgrid = np.arange(0, 20000, 50.0)
    for key in ("P", "O", "H", "M"): out["fc"][key] = []
    for mo in MONTHS:
        tc = mo * 8000 / 12; s = d["t"] <= tc
        for key, fn in (("P", None), ("O", f_O), ("H", f_H)):
            tt, xx = daily(d["t"][s], est[key][s]); rinf, tau = ks_fit(tt, xx)
            fval = 1.0 if fn is None else float(fn(Re0)[0])
            out["fc"][key].append(time_to_limit(rinf, tau, f_hi=fval) if np.isfinite(rinf) else np.nan)
        Xs = np.vstack([Xtr, np.column_stack([d["m"][s], d["Tin"][s], d["t"][s]])]); ys = np.concatenate([ytr, d["p"][s]])
        g2 = GradientBoostingRegressor(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, random_state=0).fit(Xs, ys)
        pd_ = g2.predict(np.column_stack([np.full_like(tgrid, DESIGN["m"]), np.full_like(tgrid, DESIGN["Tin"]), tgrid]))
        i = np.argmax(pd_ > 2.69); out["fc"]["M"].append(float(tgrid[i]) if pd_[i] > 2.69 else np.inf)
    # extrapolation: shell pressure on run-3 turndown records, models fitted on runs 1-2 (ML) or run-3 fouling fit (physics)
    sel = d["td"]; true_p = d["p_true"][sel]
    keep = ~sel                                                                  # ML also sees the test run outside the scored records
    Xe = np.vstack([Xtr, np.column_stack([d["m"][keep], d["Tin"][keep], d["t"][keep]])]); ye = np.concatenate([ytr, d["p"][keep]])
    gbr = GradientBoostingRegressor(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, random_state=0).fit(Xe, ye)
    pM = gbr.predict(np.column_stack([d["m"][sel], d["Tin"][sel], d["t"][sel]]))
    mae = {"M": float(np.mean(np.abs(np.minimum(pM, 2.7) - true_p)))}
    for key, fn in (("P", None), ("O", f_O), ("H", f_H)):
        rinf, tau = ks_fit(*daily(d["t"], est[key]))
        fs = 1.0 if fn is None else fn(h_tube(d["m"][sel], (d["Tin"][sel] + T_OUT) / 2)[1])
        pp = psat(np.minimum(ts_req(d["m"][sel], d["Tin"][sel], rinf * (1 - np.exp(-d["t"][sel] / tau)), f_hi=fs), TS_MAX))
        mae[key] = float(np.mean(np.abs(pp - true_p)))
    out["extrap_mae"] = mae; out["n_td"] = int(sel.sum())
    return out


if __name__ == "__main__":
    import sys
    seeds = list(range(5, 5 + int(sys.argv[1]) if len(sys.argv) > 1 else 15))
    res = []
    for sd in seeds:
        o = evaluate(sd, detail=(sd == 5)); res.append(o)
        print(sd, "truth", [round(x) if np.isfinite(x) else None for x in o["truth"]], "calib", round(o["calib_H"][0], 3), round(o["calib_O"], 3),
              "rmse", {k: round(v["rmse"] * 1e4, 2) for k, v in o["rf"].items() if k != "true"},
              "fc", {k: [None if not np.isfinite(x) else round(x) for x in v] for k, v in o["fc"].items()}, "mae", {k: round(v, 3) for k, v in o["extrap_mae"].items()})
    json.dump(res, open("twin_results.json", "w"), indent=1, default=float)
