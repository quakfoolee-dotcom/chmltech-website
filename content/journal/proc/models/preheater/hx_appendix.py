"""Feed preheater E-101 under fouling - Chmltech Online Journal (appendix script).
Design areas of a steam-heated feed preheater (clean and TEMA fouling), and for a chosen area the shell-side steam
pressure it needs clean and fully fouled, at normal rate and at 50% turndown, over sampled fouling scenarios.
Python 3 with NumPy."""
import math
import numpy as np

CP, KF, T_OUT = 2000.0, 0.13, 80.0                      # J/kg.K, W/m.K, C
OD, ID, TPP = 0.01905, 0.01575, 12                      # 3/4 in 16 BWG tubes, 12 tubes per pass
R_WALL = OD * math.log(OD / ID) / (2 * 45.0)            # carbon steel wall, m2K/W on the outside area
rho = lambda T: 900.0 - 0.95 * (T - 20.0)               # feed density, kg/m3
mu = lambda T: 1.6e-3 * math.exp(-0.018 * (T - 20.0))   # feed viscosity, Pa.s
tsat = lambda p: 1810.94 / (8.14019 - math.log10((p + 1.01325) * 750.062)) - 244.485   # C, p in barg
psat = lambda T: 10 ** (8.14019 - 1810.94 / (T + 244.485)) / 750.062 - 1.01325         # barg


def U(m, T, A, rf_i, h_o=8000.0, rf_o=1e-4, f_hi=1.0):  # Eq. (1): overall coefficient on the outside area
    p = 2 if A / (2 * TPP * math.pi * OD) <= 6.1 else 4; L = A / (p * TPP * math.pi * OD)
    v = m / 3600 / rho(T) / (TPP * math.pi * ID ** 2 / 4); Re = rho(T) * v * ID / mu(T); Pr = CP * mu(T) / KF
    f = (0.79 * math.log(max(Re, 2300)) - 1.64) ** -2
    nu = max((f / 8) * (Re - 1000) * Pr / (1 + 12.7 * math.sqrt(f / 8) * (Pr ** (2 / 3) - 1)), 1.86 * (Re * Pr * ID / L) ** (1 / 3)) \
        if Re >= 2300 else max(3.66, 1.86 * (Re * Pr * ID / L) ** (1 / 3))
    hi = f_hi * nu * KF / ID
    return 1 / (OD / (hi * ID) + R_WALL + 1 / h_o + rf_i * OD / ID + rf_o)


def ts_req(m, Tin, A, rf_i, **kw):                      # Eq. (2): steam temperature that heats the feed to 80 C
    E = math.exp(-U(m, (Tin + T_OUT) / 2, A, rf_i, **kw) * A / (m / 3600 * CP))
    return (T_OUT - Tin * E) / (1 - E)


def design_area(m, Tin, ts, rf_i, rf_o):                # area that just meets the duty at steam temperature ts
    A = 5.0
    for _ in range(40):
        A = (m / 3600 * CP) / U(m, (Tin + T_OUT) / 2, A, rf_i, rf_o=rf_o) * math.log((ts - Tin) / (ts - T_OUT))
    return A


mD, TD, TS = 9569.0, 6.8, tsat(3.0 - 0.3)                # design case: P95 feed, P5 inlet temperature, 2.7 barg in the shell
print(f"Clean area {design_area(mD, TD, TS, 0, 0):.2f} m2;  TEMA fouling {design_area(mD, TD, TS, 1.76e-4, 0.88e-4):.2f} m2")

A, m50, T50 = 8.0, 8690.0, 22.5                          # chosen area; median feed rate and temperature
rng = np.random.default_rng(1)
rinf = rng.triangular(1e-4, 3e-4, 8e-4, 2000)            # asymptotic fouling resistance, Eq. (3)
fhi = rng.lognormal(-0.15 ** 2 / 2, 0.15, 2000)          # spread of the tube-side correlation
for lab, m in (("normal rate", m50), ("50% turndown", m50 / 2)):
    clean = psat(ts_req(m, T50, A, 0.0))
    foul = np.array([psat(ts_req(m, T50, A, r, f_hi=f)) for r, f in zip(rinf, fhi)])
    print(f"{A:.0f} m2, {lab}: clean {clean:+.2f} barg; fully fouled P10 {np.percentile(foul, 10):+.2f}, P50 {np.percentile(foul, 50):+.2f}, "
          f"P90 {np.percentile(foul, 90):+.2f} barg; above 2.7 barg {np.mean(foul > 2.7):.1%}, below 0 barg {np.mean(foul < 0):.0%}")
