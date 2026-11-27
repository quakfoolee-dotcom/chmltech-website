"""Cost contingency by Monte Carlo for a C$100M process plant - Chmltech Online Journal (contingency paper).
Base estimate: the 50,000 t/y plant of the FEED series, Class 3 at the end of FEED, fixed capital C$100.0M before
contingency, in 12 cost accounts. Two kinds of uncertainty: systemic (each account's estimating error, correlated
through common drivers, plus escalation and exchange rate) and project-specific risk events (a risk register with
probabilities, cost impacts and delays, delays priced at the time-dependent indirect burn rate).
Python 3 with NumPy and SciPy."""
import json
import numpy as np
from scipy import stats

N = 50_000
# account: base C$M, (low, most likely, high) multiplier at Class 3, group for correlation
ACCOUNTS = [
    ("Major equipment",                     24.0, (0.92, 1.00, 1.15), "mat"),
    ("Piping (bulk materials)",              9.0, (0.88, 1.00, 1.27), "mat"),
    ("Instruments and controls",             5.0, (0.90, 1.00, 1.25), "mat"),
    ("Electrical",                           5.0, (0.90, 1.00, 1.25), "mat"),
    ("Civil, structural and buildings",      8.0, (0.90, 1.00, 1.35), "site"),
    ("Insulation, painting, fireproofing",   2.0, (0.90, 1.00, 1.30), "mat"),
    ("Direct field labour",                 17.0, (0.86, 1.00, 1.33), "lab"),
    ("Construction indirects",               8.0, (0.90, 1.00, 1.30), "lab"),
    ("Engineering, procurement, CM",        13.0, (0.95, 1.00, 1.20), "eng"),
    ("Owner's costs",                        4.0, (0.95, 1.00, 1.25), "eng"),
    ("Start-up and commissioning",           3.0, (0.90, 1.00, 1.40), "lab"),
    ("Freight and duties",                   2.0, (0.90, 1.00, 1.20), "mat"),
]
BASE = sum(a[1] for a in ACCOUNTS)
RHO = {("mat", "mat"): 0.5, ("lab", "lab"): 0.7, ("eng", "eng"): 0.5, ("site", "site"): 1.0}
RHO_X = 0.3                                   # between groups
IMPORT_SHARE = 0.40                           # share of major equipment bought in US$
FX = (-0.12, 0.0, 0.12)                       # change in C$ cost of imports (triangular)
ESC = (0.02, 0.03, 0.06)                      # escalation rate a year; base carries 3.0% over 1.5 years to mid-spend
ESC_BASE, ESC_YEARS = 0.03, 1.5
BURN = 0.20                                   # C$M a week of time-dependent cost (indirects, CM, owner's team)
# risk: name, probability, cost impact C$M (low, ml, high) or None, delay weeks (low, ml, high) or None
RISKS = [
    ("Poor soil: piling needed",                  0.25, (1.5, 2.5, 5.0), (2, 4, 8)),
    ("Reactor delivered late",                    0.30, None,            (4, 8, 16)),
    ("Scale-up issue forces a process change",    0.20, (2.0, 4.0, 8.0), (4, 8, 12)),
    ("HAZOP or code change adds equipment",       0.40, (0.5, 1.5, 3.0), None),
    ("Permit delayed",                            0.15, None,            (4, 10, 20)),
    ("Labour shortage: premium crews needed",     0.30, (1.0, 2.5, 5.0), None),
    ("Key vendor fails: re-procurement",          0.10, (0.5, 1.5, 3.0), (6, 10, 16)),
    ("Commissioning problems",                    0.25, (0.5, 1.5, 4.0), (2, 6, 12)),
]


def tri_ppf(u, a, m, b):
    return stats.triang.ppf(u, (m - a) / (b - a), a, b - a)


def corr_matrix(rho_scale=1.0):
    g = [a[3] for a in ACCOUNTS]; n = len(g); C = np.eye(n)
    for i in range(n):
        for j in range(n):
            if i != j:
                r = RHO.get((g[i], g[j]), RHO_X) if g[i] == g[j] else RHO_X
                C[i, j] = r * rho_scale
    w, v = np.linalg.eigh(C); C = v @ np.diag(np.clip(w, 1e-9, None)) @ v.T; d = np.sqrt(np.diag(C))
    return C / np.outer(d, d)


def simulate(n=N, seed=7, rho_scale=1.0, range_scale=1.0, risks=True, systemic=True, risk_mask=None, p_scale=1.0,
             market=False, escfx=True):
    """Returns total cost and its parts. 'core' = accounts + risk events at base-date prices (the contingency);
    'escfx' = escalation and exchange-rate effect beyond what the base carries (the escalation reserve)."""
    rng = np.random.default_rng(seed)
    nA = len(ACCOUNTS); C = np.eye(nA + 2); C[:nA, :nA] = corr_matrix(rho_scale)
    if market:                                  # escalation and the labour-shortage risk move with the market
        g = [a[3] for a in ACCOUNTS]
        for j in range(nA):
            if g[j] in ("mat", "lab"): C[j, nA] = C[nA, j] = 0.5 * rho_scale
            if g[j] == "lab": C[j, nA + 1] = C[nA + 1, j] = 0.5 * rho_scale
        C[nA, nA + 1] = C[nA + 1, nA] = 0.5
        w, v = np.linalg.eigh(C); C = v @ np.diag(np.clip(w, 1e-9, None)) @ v.T; d = np.sqrt(np.diag(C)); C = C / np.outer(d, d)
    z = rng.multivariate_normal(np.zeros(nA + 2), C, size=n); u = stats.norm.cdf(z)
    acc = np.zeros((n, nA))
    for j, (_, base, (a, m, b), _) in enumerate(ACCOUNTS):
        if systemic:
            a2, m2, b2 = 1 + (a - 1) * range_scale, 1 + (m - 1) * range_scale, 1 + (b - 1) * range_scale
            acc[:, j] = base * tri_ppf(u[:, j], a2, m2, b2)
        else:
            acc[:, j] = base
    esc = tri_ppf(u[:, nA], *ESC) if (systemic and escfx) else np.full(n, ESC_BASE)
    fx = tri_ppf(rng.random(n), *FX) if (systemic and escfx) else np.zeros(n)
    escf = ((1 + esc) / (1 + ESC_BASE)) ** ESC_YEARS
    core_acc = acc.sum(1)
    esc_acc = acc.copy(); esc_acc[:, :9] *= escf[:, None]            # escalation on direct and contractor costs
    esc_acc[:, 0] += ACCOUNTS[0][1] * IMPORT_SHARE * fx * escf        # imports in US$, after escalation
    sys_cost = esc_acc.sum(1)
    risk_cost = np.zeros(n); delay = np.zeros(n); per_risk = np.zeros((n, len(RISKS)))
    if risks:
        for k, (name, p, ci, di) in enumerate(RISKS):
            if risk_mask is not None and not risk_mask[k]: continue
            pk = min(1.0, p * p_scale)
            hit = (u[:, nA + 1] < pk) if (market and k == 5) else (rng.random(n) < pk)
            c = tri_ppf(rng.random(n), *ci) if ci else np.zeros(n)
            d = tri_ppf(rng.random(n), *di) if di else np.zeros(n)
            per_risk[:, k] = hit * (c + BURN * d)
            risk_cost += hit * c; delay += hit * d
    rk = risk_cost + BURN * delay
    return dict(total=sys_cost + rk, core=core_acc + rk, escfx=sys_cost - core_acc, sys=core_acc, risk=rk, delay=delay,
                acc=acc, per_risk=per_risk, fx=fx, esc=esc)


def pct(x, q): return float(np.percentile(x, q))


def swing_accounts(base80, n=N):
    """P80 reduction if each account (or FX, escalation) were known exactly at its mean value."""
    out = {}
    for j, acc in enumerate(ACCOUNTS):
        keep = ACCOUNTS[j]
        a, m, b = keep[2]; mean = (a + m + b) / 3
        ACCOUNTS[j] = (keep[0], keep[1], (mean - 1e-6, mean, mean + 1e-6), keep[3])
        out[keep[0]] = base80 - pct(simulate(n=n)["core"], 80)
        ACCOUNTS[j] = keep
    return out


if __name__ == "__main__":
    R = {"base": BASE, "accounts": [dict(name=a[0], base=a[1], rng=a[2], grp=a[3]) for a in ACCOUNTS],
         "risks": [dict(name=r[0], p=r[1], cost=r[2], delay=r[3]) for r in RISKS], "burn": BURN}
    S = simulate(); c = S["core"]; t = S["total"]
    R["main"] = {f"P{q}": pct(c, q) for q in (5, 10, 20, 50, 80, 90, 95)}
    R["main"].update(mean=float(c.mean()), p_under_base=float(np.mean(c <= BASE)), p_over_110=float(np.mean(c > 110)),
                     p_over_115=float(np.mean(c > 115)), sys_mean=float(S["sys"].mean()), risk_mean=float(S["risk"].mean()),
                     delay_mean=float(S["delay"].mean()), delay_p80=pct(S["delay"], 80))
    R["escfx"] = {f"P{q}": pct(S["escfx"], q) for q in (10, 50, 80, 90)}; R["escfx"]["mean"] = float(S["escfx"].mean())
    R["total"] = {f"P{q}": pct(t, q) for q in (10, 50, 80, 90)}
    print("core", {k: round(v, 3) for k, v in R["main"].items()}); print("escfx", R["escfx"]); print("total", R["total"])
    a = simulate(risks=False)["core"]; b = simulate(systemic=False)["core"]
    R["split"] = dict(sys_P50=pct(a, 50), sys_P80=pct(a, 80), sys_P90=pct(a, 90), risk_P50=pct(b, 50), risk_P80=pct(b, 80), risk_P90=pct(b, 90))
    print("split", {k: round(v, 2) for k, v in R["split"].items()})
    R["corr"] = {str(rs): {f"P{q}": pct(simulate(rho_scale=rs)["core"], q) for q in (50, 80, 90)} for rs in (0.0, 1.0)}
    Sm = simulate(market=True); R["market"] = dict(core={f"P{q}": pct(Sm["core"], q) for q in (50, 80, 90)},
                                                   total={f"P{q}": pct(Sm["total"], q) for q in (50, 80, 90)})
    print("corr", R["corr"], "market", R["market"])
    R["wide"] = {}
    for rs in (1.5, 2.0):
        for rho in (0.0, 1.0):
            R["wide"][f"{rs}_{rho}"] = {f"P{q}": pct(simulate(range_scale=rs, rho_scale=rho)["core"], q) for q in (50, 80, 90)}
    R["classes"] = {}
    for cl, rs, ps in (("Class 3", 1.0, 1.0), ("Class 4", 2.0, 1.3), ("Class 5", 3.0, 1.6)):
        x = simulate(range_scale=rs, p_scale=ps)
        xc, xt = x["core"], x["total"]
        R["classes"][cl] = {f"P{q}": pct(xc, q) for q in (5, 10, 50, 80, 90, 95)}
        R["classes"][cl].update(lo=pct(xt, 10) / pct(xt, 50) - 1, hi=pct(xt, 90) / pct(xt, 50) - 1)
        R["classes"][cl]["hist"] = np.histogram(xc, bins=np.linspace(80, 200, 121))[0].tolist()
    print("classes", {k: {q: round(v, 3) for q, v in d.items() if q != "hist"} for k, d in R["classes"].items()})
    base80 = R["main"]["P80"]; R["risk_p80"] = {}; R["risk_p80_ev"] = {}
    for k, r in enumerate(RISKS):
        m = [True] * len(RISKS); m[k] = False
        R["risk_p80"][r[0]] = base80 - pct(simulate(risk_mask=m)["core"], 80)
        ev = r[1] * ((sum(r[2]) / 3 if r[2] else 0) + BURN * (sum(r[3]) / 3 if r[3] else 0))
        R["risk_p80_ev"][r[0]] = base80 - (pct(simulate(risk_mask=m)["core"], 80) + ev)
    R["ev_risk"] = sum(p * ((sum(ci) / 3 if ci else 0) + BURN * (sum(di) / 3 if di else 0)) for _, p, ci, di in RISKS)
    print("risk eliminated", {k: round(v, 2) for k, v in R["risk_p80"].items()}, "EV", round(R["ev_risk"], 2))
    print("risk at EV", {k: round(v, 2) for k, v in R["risk_p80_ev"].items()})
    R["swing"] = swing_accounts(base80)
    print("swing", {k: round(v, 2) for k, v in sorted(R["swing"].items(), key=lambda kv: -kv[1])})
    r0 = RISKS[2]; RISKS[2] = (r0[0], 0.5, tuple(1.5 * v for v in r0[2]), tuple(1.5 * v for v in r0[3]))
    R["foak"] = {f"P{q}": pct(simulate()["core"], q) for q in (50, 80, 90)}; RISKS[2] = r0
    print("foak", R["foak"])
    qs = np.linspace(0.5, 99.5, 199); R["scurve"] = dict(q=qs.tolist(), main=np.percentile(c, qs).tolist(),
                                                         nocorr=np.percentile(simulate(rho_scale=0.0)["core"], qs).tolist())
    R["seeds_P80"] = [pct(simulate(seed=sd)["core"], 80) for sd in (1, 2, 3, 4, 5)]
    json.dump(R, open("contingency_results.json", "w"), indent=1, default=float)


