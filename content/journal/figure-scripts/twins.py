"""Figures for: Digital Twins in Chemical Process Plants: Architecture, Modeling Approaches and Applications."""
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
from style import *

SLUG = "digital-twins-in-chemical-process-plants-architecture-modeling-and-applications"

def box(ax, x0, y0, w, h, txt, fill=LIGHT, tc=NAVY, fs=9, bold=False, ec="#9AB0C8"):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.25,rounding_size=1.0", fc=fill, ec=ec, lw=1))
    ax.text(x0 + w / 2, y0 + h / 2, txt, ha="center", va="center", fontsize=fs, color=tc, fontweight="600" if bold else "normal", linespacing=1.2)
def arr(ax, p, q, col=NAVY, lw=1.6, ls="-", style="-|>", ms=11):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=col, lw=lw, ls=ls, shrinkA=0, shrinkB=0))

# Figure 1 — Kritzinger et al. classification: digital model, digital shadow, digital twin
AUTO, MAN = BLUE, GREY
fig, axs = plt.subplots(1, 3, figsize=(9.2, 3.7), gridspec_kw=dict(wspace=0.08))
panels = [("Digital model", (MAN, MAN), "Off-line simulation tuned\nto plant data for studies"),
          ("Digital shadow", (AUTO, MAN), "On-line simulation that tracks\nthe plant and advises operators"),
          ("Digital twin", (AUTO, AUTO), "Model-driven optimizer or\ncontroller writing set points")]
for ax, (title, (up, down), ex) in zip(axs, panels):
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    ax.text(50, 98, title, ha="center", va="top", fontsize=11, color=NAVY, fontweight="600")
    box(ax, 6, 64, 30, 18, "Physical\nobject")
    box(ax, 64, 64, 30, 18, "Digital\nobject", fill="#CFE6F3")
    arr(ax, (37.5, 77), (62.5, 77), up, lw=2.2 if up == AUTO else 1.6, ls="-" if up == AUTO else (0, (4, 3)))
    arr(ax, (62.5, 69), (37.5, 69), down, lw=2.2 if down == AUTO else 1.6, ls="-" if down == AUTO else (0, (4, 3)))
    ax.text(50, 86, "data", ha="center", fontsize=8.5, color=up)
    ax.text(50, 57, "information / action", ha="center", fontsize=8.5, color=down, va="top")
    ax.text(50, 34, ex, ha="center", va="center", fontsize=8.5, color="#4A5568", linespacing=1.25)
    ax.add_patch(FancyBboxPatch((3, 22), 94, 24, boxstyle="round,pad=0,rounding_size=1.5", fc="none", ec="#DCE4EE", lw=1))
fig.legend(handles=[Line2D([], [], color=AUTO, lw=2.2, label="Automatic data flow"), Line2D([], [], color=MAN, lw=1.6, ls=(0, (4, 3)), label="Manual data flow (human in the loop)")],
           loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.06))
save(fig, SLUG, "fig1-model-shadow-twin")

# Figure 2 — layered architecture of a process plant digital twin with the feedback path
fig, ax = plt.subplots(figsize=(8.6, 6.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
X0, W = 15, 64
rows = [
    (2, 8, "Physical process and field instruments\nsensors · analyzers · control valves", "#E7EEF6"),
    (14, 7, "DCS / PLC: monitoring and regulatory control", "#E7EEF6"),
    (26, 8, "Plant historian · LIMS · maintenance records\nOPC UA with context: tags, units, tolerances", LIGHT),
    (39, 6, "(i) Data acquisition and validation: range, frozen-signal, spike checks", LIGHT),
    (50, 6, "(ii) Data reconciliation and gross-error detection, Eq. (4)", LIGHT),
    (61, 6, "(iii) State and parameter estimation: KF, EKF, MHE, Eqs. (5)–(7)", LIGHT),
]
for y, h, t, c in rows:
    box(ax, X0, y, W, h, t, fill=c)
# models row
mw = (W - 4) / 3
for i, t in enumerate(["First-principles\nmodel", "Data-driven\nmodel", "Hybrid\nmodel"]):
    box(ax, X0 + i * (mw + 2), 72, mw, 8, t, fill="#CFE6F3")
# applications row
aw = (W - 8) / 5
for i, t in enumerate(["RTO", "MPC", "Monitoring,\npredictive\nmaintenance", "OTS and\nwhat-if", "Energy\noptimization"]):
    box(ax, X0 + i * (aw + 2), 86, aw, 11, t, fill=BLUE, tc="white", fs=8.5)
# upward arrows between layers
for y in [10.6, 21.6, 34.6, 45.6, 56.6, 67.6, 80.6]:
    arr(ax, (X0 + W / 2, y), (X0 + W / 2, y + 2.8 if y != 80.6 else 85.2), BLUE)
ax.text(X0 + W / 2 + 1.5, 82.6, "(iv) prediction and optimization services", fontsize=8.5, color=NAVY, ha="left", va="center")
# left labels: ISA-95 levels and twin bracket
for y, t in [(6, "L0–1"), (17.5, "L2"), (30, "L3")]:
    ax.text(X0 - 1.5, y, t, ha="right", va="center", fontsize=8.5, color="#4A5568")
ax.plot([3.5, 3.5], [2, 21], color=GREY, lw=1.4); ax.text(2, 11.5, "Control system", rotation=90, ha="center", va="center", fontsize=8.5, color="#4A5568")
ax.plot([3.5, 3.5], [26, 97], color=BLUE, lw=1.4); ax.text(2, 61.5, "Digital twin (ISA-95 Level 3; edge, plant servers or cloud)", rotation=90, ha="center", va="center", fontsize=8.5, color=BLUE)
# feedback paths on the right
xr1, xr2 = 84, 92
ax.plot([X0 + W + 0.8, xr2], [93, 93], color=GREEN_D, lw=2); arr(ax, (xr2, 93), (xr2, 18), GREEN_D, lw=2); arr(ax, (xr2, 18), (X0 + W + 0.8, 18), GREEN_D, lw=2)
ax.plot([X0 + W + 0.8, xr1], [89, 89], color=GREY, lw=1.6, ls=(0, (4, 3))); arr(ax, (xr1, 89), (xr1, 16.5), GREY, lw=1.6, ls=(0, (4, 3))); arr(ax, (xr1, 16.5), (X0 + W + 0.8, 16.5), GREY, lw=1.6, ls=(0, (4, 3)))
ax.text(xr1 - 1.3, 55, "Advice to operators (digital shadow)", rotation=90, ha="center", va="center", fontsize=8.5, color="#4A5568",
        bbox=dict(facecolor="white", edgecolor="none", pad=1))
ax.text(xr2 + 1.6, 55, "(v) Set points written to Level 2 (digital twin)", rotation=90, ha="center", va="center", fontsize=8.5, color=GREEN_D)
save(fig, SLUG, "fig2-architecture")

# Figure 3 — illustrative data reconciliation (Section 8, Table 3), Eq. (4)
A = np.array([[1.0, -1.0, -1.0]])
def recon(y, s):
    V = np.diag(np.array(s) ** 2); y = np.array(y)
    r = A @ y; S = A @ V @ A.T
    return y - (V @ A.T @ np.linalg.solve(S, r)), float(r @ np.linalg.solve(S, r))
cases = [("(a) Case 1: random errors only", [100.0, 61.0, 41.0], [2.00, 1.22, 0.82]), ("(b) Case 2: bias on F$_3$", [100.0, 61.0, 47.0], [2.00, 1.22, 0.94])]
ref = [[101.30, 60.52, 40.78], [105.02, 59.13, 45.89]]
fig, axs = plt.subplots(1, 2, figsize=(9.0, 3.9), sharey=True, gridspec_kw=dict(wspace=0.08))
for k, (ax, (title, y, s)) in enumerate(zip(axs, cases)):
    xh, g = recon(y, s)
    assert np.allclose(xh, ref[k], atol=0.01), xh
    d = xh - np.array(y); xs = np.arange(3)
    ax.errorbar(xs - 0.08, np.zeros(3), yerr=s, fmt="s", color=GREY, ms=6, capsize=5, lw=1.6, label="Measured ± 1σ")
    ax.plot(xs + 0.08, d, "o", color=ORANGE if g > 3.84 else BLUE, ms=8, zorder=5, label="Reconciled")
    for xi, di in zip(xs, d):
        ax.annotate(f"{di:+.2f}".replace("-", "−"), (xi + 0.08, di), xytext=(9, 0), textcoords="offset points", va="center", fontsize=9, color=NAVY)
    ax.axhline(0, color="#C7D2DF", lw=1)
    ax.set_xticks(xs); ax.set_xticklabels([f"F$_1$ feed\n{y[0]:.1f}", f"F$_2$ product\n{y[1]:.1f}", f"F$_3$ recycle\n{y[2]:.1f}"], fontsize=9)
    ax.set_xlim(-0.5, 2.6); ax.set_ylim(-3.2, 6.2); ax.set_title(title, loc="left")
    ok = g <= 3.84
    ax.text(0.97, 0.95, f"γ = {g:.2f} {'<' if ok else '>'} 3.84\n" + ("no gross error" if ok else "gross error flagged"), transform=ax.transAxes, ha="right", va="top",
            fontsize=9, color=GREEN_D if ok else "#B4410C", bbox=dict(facecolor="white", edgecolor="#DCE4EE", pad=3))
    ax.grid(axis="x", visible=False)
axs[0].set_ylabel(r"Adjustment from measured value (t h$^{-1}$)")
h, l = axs[0].get_legend_handles_labels(); fig.legend(h[::-1], l[::-1], loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.07))
save(fig, SLUG, "fig3-reconciliation")
print("recon ok")
