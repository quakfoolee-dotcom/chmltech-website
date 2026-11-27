"""Cost contingency by Monte Carlo - Chmltech Online Journal (appendix script).
P50, P80 and P90 of the final fixed capital of a C$100M Class 3 estimate at base-date prices: 12 accounts with
triangular ranges correlated through a Gaussian copula, and an 8-event risk register with delays. Escalation and
exchange rate are reported separately, as an escalation reserve. Python 3 with NumPy and SciPy."""
import numpy as np
from scipy import stats

ACC = [(24.0, 0.92, 1.00, 1.15, "m"), (9.0, 0.88, 1.00, 1.27, "m"), (5.0, 0.90, 1.00, 1.25, "m"), (5.0, 0.90, 1.00, 1.25, "m"),
       (8.0, 0.90, 1.00, 1.35, "s"), (2.0, 0.90, 1.00, 1.30, "m"), (17.0, 0.86, 1.00, 1.33, "l"), (8.0, 0.90, 1.00, 1.30, "l"),
       (13.0, 0.95, 1.00, 1.20, "e"), (4.0, 0.95, 1.00, 1.25, "e"), (3.0, 0.90, 1.00, 1.40, "l"), (2.0, 0.90, 1.00, 1.20, "m")]
RHO = {"m": 0.5, "l": 0.7, "e": 0.5, "s": 1.0}                     # within a group; 0.3 between groups
RISKS = [(0.25, (1.5, 2.5, 5.0), (2, 4, 8)), (0.30, None, (4, 8, 16)), (0.20, (2.0, 4.0, 8.0), (4, 8, 12)),
         (0.40, (0.5, 1.5, 3.0), None), (0.15, None, (4, 10, 20)), (0.30, (1.0, 2.5, 5.0), None),
         (0.10, (0.5, 1.5, 3.0), (6, 10, 16)), (0.25, (0.5, 1.5, 4.0), (2, 6, 12))]
BURN, N = 0.20, 50_000                                             # C$M per week of delay; iterations
tri = lambda u, a, m, b: stats.triang.ppf(u, (m - a) / (b - a), a, b - a)

rng = np.random.default_rng(7)
g = [a[4] for a in ACC]
C = np.array([[1.0 if i == j else (RHO[g[i]] if g[i] == g[j] else 0.3) for j in range(12)] for i in range(12)])
u = stats.norm.cdf(rng.multivariate_normal(np.zeros(12), C, size=N))          # Eq. (3)
acc = np.column_stack([b * tri(u[:, j], lo, ml, hi) for j, (b, lo, ml, hi, _) in enumerate(ACC)])
core = acc.sum(1)
for p, c, d in RISKS:                                                          # risk events and delays, Eq. (1)
    hit = rng.random(N) < p
    core += hit * ((tri(rng.random(N), *c) if c else 0) + BURN * (tri(rng.random(N), *d) if d else 0))
ef = ((1 + tri(rng.random(N), 0.02, 0.03, 0.06)) / 1.03) ** 1.5                # Eq. (2): escalation beyond the 3% in the base
esc = acc[:, :9].sum(1) * (ef - 1) + 24.0 * 0.40 * tri(rng.random(N), -0.12, 0.0, 0.12) * ef
for q in (50, 80, 90):
    v = np.percentile(core, q); print(f"P{q}: C${v:6.1f}M   contingency C${v - 100:5.1f}M ({v - 100:.0f}% of base)")   # Eq. (4)
for flat in (10, 15):
    print(f"Base + {flat}%: chance of overrun {np.mean(core > 100 * (1 + flat / 100)):.0%}")
print(f"Escalation and exchange-rate reserve: P50 C${np.percentile(esc, 50):.1f}M, P80 C${np.percentile(esc, 80):.1f}M")
