"""Figures for: Advancements and Challenges in Solid-State Hydrogen Absorption: A Comprehensive Review."""
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from style import *

SLUG = "advancements-and-challenges-in-solid-state-hydrogen-absorption-a-comprehensive-review"
R = 8.314

# Figure 1 — schematic pressure–composition isotherms (relative units)
def pci(T, x):
    """Schematic isotherm: alpha solid solution, sloping plateau, beta branch. T in relative units (1 = lowest)."""
    lnp0 = 3.2 * (T - 1)                     # plateau rises with T (van 't Hoff)
    xa, xb = 0.12 + 0.07 * (T - 1), 0.88 - 0.10 * (T - 1)   # miscibility gap narrows with T
    y = np.empty_like(x)
    a = x < xa; b = x > xb; m = ~a & ~b
    y[a] = lnp0 + 0.35 * (x[a] - xa) / xa * 3.5 + np.log(np.maximum(x[a], 1e-3) / xa) * 0.9
    y[m] = lnp0 + 0.35 * (x[m] - xa) / (xb - xa)
    y[b] = lnp0 + 0.35 + 9.0 * (x[b] - xb) ** 1.4 / (1 - xb) ** 0.4
    return y, xa, xb, lnp0
x = np.linspace(0.005, 0.97, 600)
fig, ax = plt.subplots(figsize=(7.4, 4.1))
envx, envy = [], []
for T, col, lab in [(1, BLUE, r"$T_1$"), (1.45, GREEN_D, r"$T_2 > T_1$"), (1.9, ORANGE, r"$T_3 > T_2$")]:
    y, xa, xb, p0 = pci(T, x)
    ax.plot(x, y, color=col, label=lab)
    envx += [xa, xb]; envy += [p0, p0 + 0.35]
# two-phase envelope (dashed dome through plateau ends)
ex = np.array([envx[0], envx[2], envx[4], envx[5], envx[3], envx[1]]); ey = np.array([envy[0], envy[2], envy[4], envy[5], envy[3], envy[1]])
ax.plot(ex, ey, ls=":", color=GREY, lw=1.4)
ax.text(0.03, 7.6, r"$\alpha$" + "\n(solid solution)", color=NAVY, fontsize=10, va="top")
ax.text(0.50, 1.15, r"$\alpha + \beta$ plateau", color=NAVY, fontsize=10, ha="center")
ax.text(0.86, 7.3, r"$\beta$ (hydride)", color=NAVY, fontsize=10, ha="center")
ax.annotate("", xy=(envx[1], -0.75), xytext=(envx[0], -0.75), arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1))
ax.text(0.5, -1.25, r"Reversible capacity at $T_1$ (plateau width)", ha="center", color=NAVY, fontsize=9)
ax.annotate(r"Plateau pressure $P_{\mathrm{eq}}$ rises with $T$ (Eq. 2)", xy=(0.5, envy[4] + 0.2), xytext=(0.5, 8.4), ha="center", color=NAVY, fontsize=9,
            arrowprops=dict(arrowstyle="->", color=NAVY, lw=1))
ax.set_xlim(0, 1); ax.set_ylim(-1.6, 9.2)
ax.set_xticklabels([]); ax.set_yticklabels([])
ax.set_xlabel("Hydrogen content, H/M (relative units)"); ax.set_ylabel(r"ln $P$ (relative units)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3)
save(fig, SLUG, "fig1-pci-isotherms")

# Figure 2 — van 't Hoff plot from the paper's ΔH values and stated equilibrium points (Table 2, Sections 2.2, 3.2)
# ΔS is back-calculated from each stated point via Eq. (2): ΔS_abs = ΔH_abs/T − R ln(P/P0)
mats = [("LaNi$_5$H$_6$", -31e3, 2.0, 298.15, BLUE), ("TiFeH$_2$", -28e3, 5.0, 303.15, BRIGHT),
        ("Mg$_2$NiH$_4$", -64e3, 1.0, 553.15, GREEN_D), ("MgH$_2$", -75e3, 1.0, 573.15, NAVY)]
ias = [("NaAlH$_4$, step 1", -37e3), ("NaAlH$_4$, step 2", -47e3)]   # ΔS = −130 J/mol/K assumed (Section 2.2)
fig, ax = plt.subplots(figsize=(7.8, 4.6))
ax.add_patch(Rectangle((1000 / 358.15, np.log(5)), 1000 / 233.15 - 1000 / 358.15, np.log(12) - np.log(5), color=GREEN, alpha=0.22, lw=0, zorder=0))
ax.text(1000 / 233.15 - 0.03, np.log(12) + 0.25, "DOE delivery window\n5–12 bar, −40 to 85 °C", color=GREEN_D, fontsize=9, ha="right", va="bottom")
inv = np.linspace(1.45, 4.35, 300)
out = []
for name, dH, P, T, col in mats:
    dS = dH / T - R * np.log(P)
    ax.plot(inv, (dH * inv / 1000) / R - dS / R, color=col, label=f"{name}  (ΔH {dH/1e3:.0f}, ΔS {dS:.0f})".replace("-", "−"))
    ax.plot(1000 / T, np.log(P), "o", color=col, ms=5.5, zorder=5)
    out.append((name, round(dS), round(dH / dS - 273.15)))
for (name, dH), col in zip(ias, [ORANGE, "#B4410C"]):
    dS = -130.0
    ax.plot(inv, (dH * inv / 1000) / R - dS / R, color=col, ls="--", label=f"{name}  (ΔH {dH/1e3:.0f}, ΔS −130 assumed)".replace("-", "−"))
ax.axhline(0, color=GREY, lw=1.2, ls="-"); ax.text(4.33, 0.15, "1 bar", color="#4A5568", fontsize=9, ha="right", va="bottom")
ax.axvline(1000 / 298.15, color=GREY, lw=1.2, ls=":"); ax.text(1000 / 298.15 + 0.03, -7.7, "25 °C", color="#4A5568", fontsize=9, rotation=90, va="bottom")
ax.set_xlim(1.45, 4.35); ax.set_ylim(-8, 8)
ax.set_xlabel(r"1000 / $T$ (K$^{-1}$)"); ax.set_ylabel(r"ln($P_{\mathrm{eq}}$ / 1 bar)")
sec = ax.secondary_yaxis("right", functions=(lambda y: y, lambda y: y))
pt = [0.001, 0.01, 0.1, 1, 10, 100, 1000]; sec.set_yticks(np.log(pt)); sec.set_yticklabels(["0.001", "0.01", "0.1", "1", "10", "100", "1000"]); sec.set_ylabel(r"$P_{\mathrm{eq}}$ (bar)")
top = ax.secondary_xaxis("top", functions=(lambda v: v, lambda v: v))
tc = [400, 300, 200, 100, 50, 0, -40]; top.set_xticks([1000 / (t + 273.15) for t in tc]); top.set_xticklabels([f"{t}" for t in tc]); top.set_xlabel("Temperature (°C)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=9, title=r"Absorption ΔH (kJ mol$^{-1}$ H$_2$) and ΔS (J mol$^{-1}$ K$^{-1}$)", title_fontsize=9)
save(fig, SLUG, "fig2-van-t-hoff")
print("van't Hoff:", out)

# Figure 3 — gravimetric vs volumetric material capacities (Table 2) with DOE system targets (Table 1)
pts = [("LaNi$_5$H$_6$", 1.4, 95, (6, -14)), ("TiFeH$_2$", 1.9, 105, (6, 4)), ("Mg$_2$NiH$_4$", 3.6, 98, (6, -13)), ("MgH$_2$", 7.6, 110, (6, 4)),
       ("NaAlH$_4$ (reversible)", 5.6, 70, (-7, -14)), ("LiBH$_4$ (total H)", 18.5, 120, (-8, 6)), ("NH$_3$BH$_3$ (total H)", 19.6, 145, (-8, 6))]
fig, ax = plt.subplots(figsize=(7.8, 4.4))
for lab, (g, v), col in [("Ultimate", (6.5, 50), NAVY), ("2025", (5.5, 40), BLUE), ("2020", (4.5, 30), BRIGHT)]:
    ax.add_patch(Rectangle((g, v), 22 - g, 165 - v, facecolor=col, alpha=0.06, lw=0, zorder=0))
    ax.plot([g, g, 22], [165, v, v], color=col, ls="--", lw=1.2)
    ax.text(g + 0.12, 162, f"DOE {lab}", color=col, fontsize=8.5, va="top", ha="left", rotation=90)
ax.axhline(70.8, color=GREY, lw=1, ls=":"); ax.text(21.8, 72.5, "Liquid H$_2$, 20 K (70.8)", color="#4A5568", fontsize=8.5, ha="right", va="bottom")
ax.axhline(40, color=GREY, lw=1, ls=":"); ax.text(21.8, 41.5, "Compressed H$_2$, 700 bar (≈ 40)", color="#4A5568", fontsize=8.5, ha="right", va="bottom")
for lab, g, v, off in pts:
    ax.plot(g, v, "o", color=ORANGE if "total" in lab else GREEN_D, ms=7, zorder=5, mec="white", mew=0.8)
    ax.annotate(lab, (g, v), xytext=off, textcoords="offset points", fontsize=9, color=NAVY, ha="right" if off[0] < 0 else "left", bbox=dict(facecolor="white", edgecolor="none", pad=0.8, alpha=0.85))
# physisorbents and RHC: gravimetric only (volumetric not quantified in Table 2)
for lab, g in [("AC 77 K", 4.5), ("MOF-177 77 K", 7.5), ("LiBH$_4$+MgH$_2$", 11.4)]:
    ax.plot([g], [4], marker="^", color=GREY, ms=7, zorder=5)
    ax.text(g, 9, lab, fontsize=8.5, color="#4A5568", ha="center", va="bottom", rotation=0)
ax.text(21.8, 4, "▲ volumetric not quantified", fontsize=8.5, color="#4A5568", ha="right", va="center")
ax.set_xlim(0, 22); ax.set_ylim(0, 165)
ax.set_xlabel("Gravimetric capacity (wt% H)"); ax.set_ylabel(r"Volumetric capacity (kg H$_2$ m$^{-3}$)")
save(fig, SLUG, "fig3-capacity-map")
