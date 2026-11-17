"""Monte Carlo rated point for a feed pump - Chmltech Online Journal (appendix script).
20,000 correlated cases of the reactor feed system; prints the P90/P95/P99 and stacked-margin rated points.
Python 3 with NumPy and SciPy."""
import numpy as np
from scipy import stats

G, PATM, DS, DD = 9.81, 101325.0, 0.0779, 0.0525          # m/s2, Pa, 3" and 2" Sch 40 bore (m)
rho = lambda T: 900.0 - 0.95 * (T - 20)                     # organic feed blend, kg/m3
mu = lambda T: 1.6e-3 * np.exp(-0.018 * (T - 20))          # Pa.s
IN = {"rate": ("tri", (0.85, 1.0, 1.10)), "recycle": ("uni", (0.15, 0.25)), "T": ("uni", (5, 40)),
      "p_rx": ("nor", (4.0, 0.15)), "level": ("uni", (0.5, 7.5)), "blanket": ("uni", (0.02, 0.05)),
      "L_dis": ("tri", (120, 140, 180)), "K_dis": ("tri", (6, 8, 12)), "eps": ("uni", (0.045e-3, 0.15e-3)),
      "foul": ("uni", (1.0, 1.5)), "strainer": ("uni", (1.0, 5.0))}
BASE = dict(rate=1.0, recycle=0.20, T=20.0)
WORST = dict(rate=1.10, recycle=0.25, T=5.0, p_rx=4.45, level=0.5, blanket=0.02, L_dis=180.0, K_dis=12.0, eps=0.15e-3, foul=1.5, strainer=5.0)
CORR = {("rate", "p_rx"): 0.5, ("rate", "recycle"): 0.3}  # rank correlations (Gaussian copula)


def sample(n, seed=1):
    names = list(IN); C = np.eye(len(names))
    for (a, b), r in CORR.items():
        i, j = names.index(a), names.index(b); C[i, j] = C[j, i] = 2 * np.sin(np.pi * r / 6)
    u = np.clip(stats.norm.cdf(np.random.default_rng(seed).multivariate_normal(np.zeros(len(names)), C, size=n)), 1e-9, 1 - 1e-9)
    out = {}
    for i, k in enumerate(names):
        kind, a = IN[k]; x = u[:, i]
        out[k] = (a[0] + (a[1] - a[0]) * x if kind == "uni" else stats.norm.ppf(x, *a) if kind == "nor"
                  else stats.triang.ppf(x, (a[1] - a[0]) / (a[2] - a[0]), a[0], a[2] - a[0]))
    return out


def friction(Q, D, L, K, eps, r, m):                       # Darcy-Weisbach, Colebrook friction factor; Pa
    v = Q / 3600 / (np.pi * D ** 2 / 4); Re = r * v * D / m; f = np.full_like(np.asarray(Re, float), 0.02)
    for _ in range(30): f = (-2 * np.log10(eps / D / 3.7 + 2.51 / (Re * np.sqrt(f)))) ** -2
    return (f * L / D + K) * r * v ** 2 / 2


def head(x, Q=None):
    """Pump head (m) needed with no control valve drop, and the feed flow (m3/h)."""
    r, m = rho(x["T"]), mu(x["T"])
    Q = 6250 * x["rate"] / 0.85 * (1 + x["recycle"]) / r if Q is None else Q
    q = Q / 10
    suction = PATM + x["blanket"] * 1e5 + r * G * (1.0 + x["level"]) - friction(Q, DS, 12, 2, x["eps"], r, m) - 0.02e5 * x["strainer"] * q ** 2
    reactor = PATM + x["p_rx"] * 1e5 + r * G * 14.0 + 0.20e5 * q ** 2
    losses = friction(Q, DD, x["L_dis"], x["K_dis"], x["eps"], r, m) + 0.15e5 * q ** 2 + 0.30e5 * x["foul"] * q ** 1.8 * (m / mu(20)) ** 0.2
    return (reactor + losses - suction) / (r * G), Q, r


X = sample(20000)
H, Q, r = head(X)
need = H + 0.7e5 / (r * G)                                  # keep 0.7 bar across the control valve
for p in (90, 95, 99):
    Qr = np.percentile(Q, p)
    Hr = np.percentile(need / (1.20 - 0.20 * (Q / Qr) ** 2), p)   # curve shape: shutoff 1.2 x rated head
    print(f"P{p}: rated {Qr:.2f} m3/h at {Hr:.1f} m")
Qn = 6250 / 0.85 * 1.2 / rho(20.0)
Hw, _, rw = head(WORST, 1.2 * Qn)
print(f"Stacked margins: rated {1.2 * Qn:.2f} m3/h at {1.1 * (Hw + 0.7e5 / (rw * G)):.1f} m")
