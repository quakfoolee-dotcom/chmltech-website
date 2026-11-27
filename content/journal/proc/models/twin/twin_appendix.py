"""Hybrid fouling twin for a steam-heated exchanger - Chmltech Online Journal (appendix script).
Learns a Reynolds-number correction to the Gnielinski coefficient from clean-period records (Eq. 3), estimates the
fouling resistance of each record (Eqs. 1-2), fits Kern-Seaton (Eq. 4) and forecasts when the design case runs out
of steam. A small synthetic plant stands in for historian data. Python 3 with NumPy and SciPy."""
import math
import numpy as np
from scipy.optimize import least_squares

CP, KF, OD, ID, TPP, A, HO, RWO = 2000.0, 0.13, 0.01905, 0.01575, 12, 6.0, 8000.0, 1e-4
RW = OD * math.log(OD / ID) / (2 * 45.0)
rho = lambda T: 900 - 0.95 * (T - 20); mu = lambda T: 1.6e-3 * np.exp(-0.018 * (T - 20))
tsat = lambda p: 1810.94 / (8.14019 - np.log10((p + 1.01325) * 750.062)) - 244.485


def gnielinski(m, T):                                   # tube-side coefficient (W/m2K) and Reynolds number
    v = m / 3600 / rho(T) / (TPP * math.pi * ID ** 2 / 4); Re = rho(T) * v * ID / mu(T); Pr = CP * mu(T) / KF
    f = (0.79 * np.log(Re) - 1.64) ** -2
    return (f / 8) * (Re - 1000) * Pr / (1 + 12.7 * np.sqrt(f / 8) * (Pr ** (2 / 3) - 1)) * KF / ID, Re


def u_from_hi(hi, rf=0.0):                              # resistances in series on the outside area (used in Eq. 2)
    return 1 / (OD / (hi * ID) + RW + 1 / HO + rf * OD / ID + RWO)


def u_measured(m, Tin, Tout, p):                        # Eq. (1): duty over LMTD, from four instruments
    Ts = tsat(p); lm = (Tout - Tin) / np.log((Ts - Tin) / (Ts - Tout))
    return m / 3600 * CP * (Tout - Tin) / (A * lm)


def calibrate(m, Tin, Tout, p):                         # Eq. (3): f(Re) = a Re^b from clean records
    hi_c, Re = gnielinski(m, (Tin + 80) / 2)
    hi_m = OD / ID / (1 / u_measured(m, Tin, Tout, p) - RW - 1 / HO - RWO)
    b, ln_a = np.polyfit(np.log(Re), np.log(hi_m / hi_c), 1)
    return lambda R: np.exp(ln_a) * R ** b


def fouling(m, Tin, Tout, p, f):                        # Eq. (2), with the learned correction
    hi_c, Re = gnielinski(m, (Tin + 80) / 2)
    return (1 / u_measured(m, Tin, Tout, p) - 1 / u_from_hi(f(Re) * hi_c)) * ID / OD


def forecast(t, rf, f, m_d=9569.0, T_d=6.8, p_max=2.7):  # Eq. (4) fit, then hours until the design case runs out of steam
    x = least_squares(lambda x: x[0] * 1e-4 * (1 - np.exp(-t / x[1])) - rf, [3, 3000], bounds=([0.1, 200], [20, 3e4]), loss="soft_l1", f_scale=3e-5).x
    hi_c, Re = gnielinski(m_d, (T_d + 80) / 2); T_s = tsat(p_max)
    for h in np.arange(0, 3e4, 50):
        U = u_from_hi(f(Re) * hi_c, x[0] * 1e-4 * (1 - math.exp(-h / x[1])))
        if 80 > T_s - (T_s - T_d) * math.exp(-U * A / (m_d / 3600 * CP)): return h, x
    return float("inf"), x


# ---- synthetic plant: true coefficient 12% below the correlation at normal rate, more at low flow ----
rng = np.random.default_rng(3)
def plant(n, t, rinf, tau):
    m = 8690 * np.where(rng.random(n) < 0.15, 0.5, 1.0) * (1 + 0.05 * rng.standard_normal(n)); Tin = rng.uniform(8, 36, n)
    hi_c, Re = gnielinski(m, (Tin + 80) / 2); hi = 0.88 * (Re / 17800) ** 0.15 * hi_c
    U = 1 / (OD / (hi * ID) + RW + 1 / 7000 + rinf * (1 - np.exp(-t / tau)) * OD / ID + RWO)
    E = np.exp(-U * A / (m / 3600 * CP)); Ts = (80 - Tin * E) / (1 - E)
    p = 10 ** (8.14019 - 1810.94 / (Ts + 244.485)) / 750.062 - 1.01325
    return m * (1 + 0.02 * rng.standard_normal(n)), Tin + 0.3 * rng.standard_normal(n), 80 + 0.3 * rng.standard_normal(n), p + 0.015 * rng.standard_normal(n)

f = calibrate(*plant(150, np.zeros(150), 0, 1))         # clean weeks after a cleaning
t = np.arange(0, 1340, 4.0)                             # first two months of a new run
rf = fouling(*plant(len(t), t, 3.5e-4, 2500), f)
day = (t // 24).astype(int); td = np.array([t[day == d].mean() for d in np.unique(day)]); rd = np.array([np.median(rf[day == d]) for d in np.unique(day)])
h, x = forecast(td, rd, f)
print(f"Learned correction at Re 18,000: {f(18000):.3f};  fitted Rinf {x[0]:.2f}e-4 m2K/W, tau {x[1]:.0f} h (true 3.50e-4, 2,500 h)")
print(f"Forecast after two months: design case runs out of steam at {h:.0f} h after cleaning (true: 1,650 h)")
