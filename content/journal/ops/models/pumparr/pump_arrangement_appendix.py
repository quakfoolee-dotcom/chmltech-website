"""Pump arrangements under uncertainty - Chmltech Online Journal (appendix script).
Average electrical power of four arrangements over 20,000 correlated operating cases, at normal rate and at 50%
turndown: A 1 x 100% with a control valve, B 1 x 100% on a drive, C 2 x 50% with a valve (staged), E 2 x 50% on
drives (staged). Python 3 with NumPy and SciPy."""
import numpy as np
from scipy import stats

G, PATM, DS, DD = 9.81, 101325.0, 0.0779, 0.0525
rho = lambda T: 900.0 - 0.95 * (T - 20)
mu = lambda T: 1.6e-3 * np.exp(-0.018 * (T - 20))
IN = {"rate": ("tri", (0.85, 1.0, 1.10)), "recycle": ("uni", (0.15, 0.25)), "T": ("uni", (5, 40)),
      "p_rx": ("nor", (4.0, 0.15)), "level": ("uni", (0.5, 7.5)), "blanket": ("uni", (0.02, 0.05)),
      "L_dis": ("tri", (120, 140, 180)), "K_dis": ("tri", (6, 8, 12)), "eps": ("uni", (0.045e-3, 0.15e-3)),
      "foul": ("uni", (1.0, 1.5)), "strainer": ("uni", (1.0, 5.0))}
CORR = {("rate", "p_rx"): 0.5, ("rate", "recycle"): 0.3}
QR, HR, S = 10.683, 82.497, 1.20                    # P95 rated point of the 100% pump (Issue 8); shutoff ratio
ETA = {100: 0.40, 50: 0.34}                       # best efficiencies; motor 92%, drive 97%


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


def friction(Q, D, L, K, eps, r, m):
    v = Q / 3600 / (np.pi * D ** 2 / 4); Re = r * v * D / m; f = np.full_like(np.asarray(Re, float), 0.02)
    for _ in range(30): f = (-2 * np.log10(eps / D / 3.7 + 2.51 / (Re * np.sqrt(f)))) ** -2
    return (f * L / D + K) * r * v ** 2 / 2


def system_head(x, Q):
    r, m = rho(x["T"]), mu(x["T"]); q = Q / 10
    suction = PATM + x["blanket"] * 1e5 + r * G * (1.0 + x["level"]) - friction(Q, DS, 12, 2, x["eps"], r, m) - 0.02e5 * x["strainer"] * q ** 2
    reactor = PATM + x["p_rx"] * 1e5 + r * G * 14.0 + 0.20e5 * q ** 2
    losses = friction(Q, DD, x["L_dis"], x["K_dis"], x["eps"], r, m) + 0.15e5 * q ** 2 + 0.30e5 * x["foul"] * q ** 1.8 * (m / mu(20)) ** 0.2
    return (reactor + losses - suction) / (r * G), r


def pump(q, qr, size, n=1.0):                      # head and efficiency of one pump at flow q and speed n
    x = q / (1.05 * qr * n)
    return HR * (S * n ** 2 - (S - 1) * (q / qr) ** 2), np.clip(ETA[size] * (2 * x - x ** 2), 0.05, None)


def valve(Q, H, r, k, size):                       # k fixed-speed pumps, control valve takes the rest of the head
    qr = QR * size / 100; Hp, eta = pump(Q / k, qr, size)
    return Q / 3600 * r * G * Hp / eta / 1000 / 0.92, (Hp - H) * r * G / 1e5


def drive(Q, H, r, k, size):                       # k pumps at equal speed on drives, no valve
    qr = QR * size / 100; n = np.sqrt((H / HR + (S - 1) * (Q / k / qr) ** 2) / S); _, eta = pump(Q / k, qr, size, n)
    return Q / 3600 * r * G * H / eta / 1000 / (0.92 * 0.97), n


X = sample(20000)
Qn = 6250 * X["rate"] / 0.85 * (1 + X["recycle"]) / rho(X["T"])
for label, Q in (("normal", Qn), ("50% turndown", 0.5 * Qn)):
    H, r = system_head(X, Q)
    PA, _ = valve(Q, H, r, 1, 100)
    PB, _ = drive(Q, H, r, 1, 100)
    P1, dp1 = valve(Q, H, r, 1, 50); P2, _ = valve(Q, H, r, 2, 50)
    PC = np.where(dp1 >= 0.7, P1, P2)                                  # second pump only if one cannot keep 0.7 bar
    E1, n1 = drive(Q, H, r, 1, 50); E2, n2 = drive(Q, H, r, 2, 50)
    PE = np.where((n1 <= 1) & (E1 <= E2), E1, E2)                       # fewer pumps when feasible and cheaper
    print(f"{label:13s} mean kW  A {PA.mean():.2f}  B {PB.mean():.2f}  C {PC.mean():.2f}  E {PE.mean():.2f}")
