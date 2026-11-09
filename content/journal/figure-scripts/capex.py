"""Figures for Vol. 104(4): Engineering CAPEX and OPEX Estimation for Process Plants."""
import numpy as np, matplotlib.pyplot as plt
from style import *

SLUG = "engineering-capex-and-opex-estimation-for-process-plants"

# Figure 1 — AACE 18R-97 accuracy ranges by class (Table 1 of the paper)
cls = ["Class 5", "Class 4", "Class 3", "Class 2", "Class 1"]
lo = [(-20, -50), (-15, -30), (-10, -20), (-5, -15), (-3, -10)]   # (narrowest, widest) low bound
hi = [(30, 100), (20, 50), (10, 30), (5, 20), (3, 15)]           # (narrowest, widest) high bound
fig, ax = plt.subplots(figsize=(7.6, 3.5))
for k, c in enumerate(cls):
    y = len(cls) - 1 - k
    ax.barh(y, hi[k][1] - lo[k][1], left=lo[k][1], height=0.56, color=LIGHT, edgecolor="#B9C7D8", label="Widest range" if k == 0 else None)
    ax.barh(y, hi[k][0] - lo[k][0], left=lo[k][0], height=0.56, color=BLUE, label="Narrowest range" if k == 0 else None)
    ax.text(lo[k][1] - 2, y, f"{lo[k][1]}%", ha="right", va="center", fontsize=9, color="#4A5568")
    ax.text(hi[k][1] + 2, y, f"+{hi[k][1]}%", ha="left", va="center", fontsize=9, color="#4A5568")
ax.axvline(0, color=NAVY, lw=1.2)
ax.set_yticks(range(len(cls))); ax.set_yticklabels(cls[::-1]); ax.set_xlim(-72, 122)
ax.set_xlabel("Expected accuracy range relative to the estimate (%)")
ax.grid(axis="y", visible=False)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)
ax.set_ylim(-0.6, 4.6)
save(fig, SLUG, "fig1-aace-accuracy")

# Figure 2 — capacity-exponent scaling, Eq. (2)
r = np.linspace(0.25, 4, 300)
fig, ax = plt.subplots(figsize=(6.6, 4.0))
for n, col, ls in [(0.4, GREEN_D, "-"), (0.6, BLUE, "-"), (0.8, ORANGE, "-"), (1.0, GREY, "--")]:
    ax.plot(r, r ** n, color=col, ls=ls, label=f"n = {n}" + (" (linear)" if n == 1.0 else " (six-tenths rule)" if n == 0.6 else ""))
ax.set_xscale("log"); ax.set_yscale("log")
ticks = [0.25, 0.5, 1, 2, 4]
ax.set_xticks(ticks); ax.set_xticklabels([str(t) for t in ticks]); ax.set_yticks(ticks); ax.set_yticklabels([str(t) for t in ticks])
ax.minorticks_off()
ax.plot([1.6], [1.6 ** 0.6], "o", color=NAVY, ms=7, zorder=5)
ax.annotate("Worked example (Section 9):\ncapacity × 1.6 → cost × 1.326", xy=(1.6, 1.326), xytext=(0.3, 1.9), fontsize=9, color=NAVY,
            arrowprops=dict(arrowstyle="->", color=NAVY, lw=1))
ax.set_xlabel("Capacity ratio  S₂ / S₁"); ax.set_ylabel("Cost ratio  C₂ / C₁")
ax.legend(loc="lower right")
save(fig, SLUG, "fig2-scaling")

# Figure 3 — CAPEX–OPEX trade-off, Eq. (10), schematic heat-recovery case
dT = np.linspace(2, 40, 400)
cap = 6.0 / dT ** 0.9 + 0.6          # annualized capital: exchanger area grows as ΔTmin falls (schematic)
op = 0.07 * dT + 0.35                # utility cost grows with ΔTmin (schematic)
tac = cap + op
i = tac.argmin()
fig, ax = plt.subplots(figsize=(6.6, 3.9))
ax.plot(dT, cap, color=BLUE, label=r"Annualized capital, CRF × $C_{\mathrm{cap}}$")
ax.plot(dT, op, color=ORANGE, label=r"Operating (utility) cost, $C_{\mathrm{op}}$")
ax.plot(dT, tac, color=NAVY, lw=2.8, label="Total annualized cost, TAC")
ax.plot(dT[i], tac[i], "o", color=GREEN_D, ms=8, zorder=5)
ax.annotate(r"Optimum $\Delta T_{\min}$", xy=(dT[i], tac[i]), xytext=(dT[i] + 5, tac[i] - 0.9), color=GREEN_D, fontsize=9.5, fontweight="600",
            arrowprops=dict(arrowstyle="->", color=GREEN_D, lw=1))
ax.set_ylim(0, 4.2); ax.set_xlim(2, 40)
ax.set_xlabel(r"Minimum approach temperature  $\Delta T_{\min}$ (K)"); ax.set_ylabel("Annual cost (relative units)")
ax.set_yticklabels([])
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, fontsize=9)
save(fig, SLUG, "fig3-tradeoff")

# Figure 4 — Monte Carlo results of the worked example (same model and inputs as Section 9; seed 42, 20,000 trials)
def npv(FCI, price, rm, i=0.10):
    R = 80000 * price / 1e6; WC = 0.15 * FCI; COMd = 0.18 * FCI + 2.73 * 3.5 + 1.23 * (rm + 7); D = FCI / 10
    v = -0.4 * FCI - (0.6 * FCI + WC) / (1 + i)
    for k in range(15):
        d = D if k < 10 else 0
        v = v + ((R - COMd - d) * 0.75 + d) / (1 + i) ** (2 + k)
    return v + WC / (1 + i) ** 16
rng = np.random.default_rng(42); N = 20000
F = 175 * rng.triangular(0.75, 1, 1.40, N); P = 1800 * rng.triangular(0.85, 1, 1.10, N); RM = 45 * rng.triangular(0.90, 1, 1.15, N)
V = npv(F, P, RM)
assert abs(npv(175, 1800, 45) - 43.0) < 0.1
p10, p50, p90 = np.percentile(V, [10, 50, 90]); f50, f90 = np.percentile(F, [50, 90])
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.7), gridspec_kw=dict(wspace=0.28))
xs = np.sort(F); a1.plot(xs, np.arange(1, N + 1) / N * 100, color=BLUE)
for v, lab, col, y in [(175, "Base 175", GREY, 8), (f50, f"P50 {f50:.0f}", NAVY, 60), (f90, f"P90 {f90:.0f}", ORANGE, 30)]:
    a1.axvline(v, color=col, lw=1.3, ls="--"); a1.text(v + 1.5, y, lab, color=col, fontsize=9, bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
a1.set_xlabel("Fixed capital investment ($ million)"); a1.set_ylabel("Cumulative probability (%)"); a1.set_title("(a) FCI distribution")
a2.hist(V, bins=60, color=LIGHT, edgecolor="#B9C7D8", linewidth=0.4)
a2.hist(V[V < 0], bins=np.histogram_bin_edges(V, 60), color="#F3C3A3", edgecolor="#E0A07A", linewidth=0.4)
ymax = a2.get_ylim()[1] * 1.42; a2.set_ylim(0, ymax)
for v, lab, col, y, ha in [(p10, f"P10 {p10:.0f}", ORANGE, 0.93, "right"), (p50, f"P50 {p50:.0f}", NAVY, 0.93, "left"), (43.0, "Deterministic 43", GREY, 0.82, "left"), (p90, f"P90 {p90:.0f}", GREEN_D, 0.71, "left")]:
    a2.axvline(v, color=col, lw=1.3, ls="--"); a2.text(v + (4 if ha == "left" else -4), ymax * y, lab, color=col, fontsize=9, ha=ha, bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
a2.text(-195, ymax * 0.58, f"NPV < 0:\n≈ {(V < 0).mean() * 100:.0f}% of trials", color="#B4410C", fontsize=9)
a2.set_xlabel("NPV at 10% ($ million)"); a2.set_ylabel("Number of trials"); a2.set_title("(b) NPV distribution")
save(fig, SLUG, "fig4-monte-carlo")
print("capex figures:", round(p10), round(p50), round(p90), round(f50), round(f90))
