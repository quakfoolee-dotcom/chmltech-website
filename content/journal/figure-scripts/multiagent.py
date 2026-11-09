"""Figures for Vol. 104(2): Multi-Agent AI Systems: Architectures, Coordination Patterns and Failure Modes."""
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
from style import *

SLUG = "multi-agent-ai-systems-architectures-coordination-and-failure-modes"
FILL = "#EEF3F9"

# ---------------------------------------------------------------- Figure 1 — five coordination topologies (Table 1)
fig, ax = plt.subplots(figsize=(9.0, 6.6))
ax.set_xlim(0, 15); ax.set_ylim(0, 11); ax.set_aspect("equal"); ax.axis("off")
R = 0.42


def node(x, y, lab, col=BLUE, fill="white", r=R, ls="-", fs=9):
    ax.add_patch(Circle((x, y), r, facecolor=fill, edgecolor=col, lw=1.6, ls=ls, zorder=3))
    ax.text(x, y, lab, ha="center", va="center", fontsize=fs, color=NAVY, fontweight="600", zorder=4)


def arrow(p, q, style="-|>", col=NAVY, ls="-", rad=0.0, sb=None, lw=1.2):
    # shrink in points: convert one data unit to points from the axis transform
    u = (ax.transData.transform((1, 0)) - ax.transData.transform((0, 0)))[0] * 72 / fig.dpi
    a = FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=10, color=col, lw=lw, ls=ls,
                        shrinkA=R * u + 1, shrinkB=(R * u + 1) if sb is None else sb, connectionstyle=f"arc3,rad={rad}", zorder=2)
    ax.add_patch(a)


def panel(x0, y0, w, h, title, sub):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0,rounding_size=0.25", facecolor=FILL, edgecolor=LIGHT, lw=1, zorder=0))
    ax.text(x0 + 0.25, y0 + h - 0.35, title, ha="left", va="center", fontsize=10.5, color=NAVY, fontweight="700")
    ax.text(x0 + 0.25, y0 + 0.2, sub, ha="left", va="bottom", fontsize=9, color="#4A5568")


# (a) orchestrator–worker
panel(0.1, 5.5, 4.8, 5.4, "(a) Orchestrator–worker", "Central lead;\nisolated worker contexts")
L = (2.5, 9.2); node(*L, "Lead", NAVY, "#DCE9F7", r=0.52)
for i, x in enumerate([1.1, 2.5, 3.9]):
    W = (x, 7.3); node(*W, f"W{i + 1}")
    if x == 2.5:
        arrow((2.38, 9.2), (2.38, 7.3)); arrow((2.62, 7.3), (2.62, 9.2), ls=(0, (3, 2)), col=GREEN_D)
    else:
        arrow(L, W); arrow(W, L, ls=(0, (3, 2)), rad=0.25 if x > 2.5 else -0.25, col=GREEN_D)
ax.text(4.75, 8.55, "results", ha="right", fontsize=9, color=GREEN_D)

# (b) hierarchical
panel(5.1, 5.5, 4.8, 5.4, "(b) Hierarchical", "Nested managers;\nrole-specific documents")
M = (7.5, 9.45); node(*M, "M", NAVY, "#DCE9F7")
for sx, sl in [(6.4, "S1"), (8.6, "S2")]:
    S = (sx, 8.25); node(*S, sl, BLUE, "#DCE9F7"); arrow(M, S)
    for dx in (-0.55, 0.55):
        W = (sx + dx, 7.05); node(*W, "W", r=0.34, fs=9); arrow(S, W)

# (c) peer / debate
panel(10.1, 5.5, 4.8, 5.4, "(c) Peer / debate", "Distributed; shared\ntranscript; R rounds")
cx, cy = 12.1, 8.15
pts = [(cx + 1.05 * np.cos(t), cy + 1.05 * np.sin(t)) for t in np.deg2rad([90, 210, 330])]
for i, p in enumerate(pts):
    node(*p, f"A{i + 1}")
for i in range(3):
    for j in range(i + 1, 3):
        arrow(pts[i], pts[j], style="<|-|>")
J = (14.15, 8.15); node(*J, "J", ORANGE, "white", ls=(0, (3, 2)))
arrow(pts[2], J, col=ORANGE, ls=(0, (3, 2)))
ax.text(14.15, 7.45, "judge\n(optional)", ha="center", va="top", fontsize=9, color=ORANGE)

# (d) blackboard
panel(0.1, 0.1, 6.0, 5.2, "(d) Blackboard", "Shared workspace;\npublish–subscribe")
ax.add_patch(FancyBboxPatch((1.95, 2.4), 2.3, 1.2, boxstyle="round,pad=0,rounding_size=0.15", facecolor="#E9F4DC", edgecolor=GREEN_D, lw=1.6, zorder=3))
ax.text(3.1, 3.0, "Shared\nworkspace", ha="center", va="center", fontsize=9.5, color=NAVY, fontweight="600", zorder=4)
for (x, y, lab) in [(0.85, 4.05, "A1"), (5.35, 4.05, "A2"), (0.85, 1.8, "A3"), (5.35, 1.8, "A4")]:
    node(x, y, lab)
    bx = 1.95 if x < 3 else 4.25
    by = min(max(y, 2.55), 3.45)
    arrow((x, y), (bx, by), style="<|-|>", sb=2, col=GREEN_D)
ax.text(3.1, 4.25, "read / write", ha="center", fontsize=9, color=GREEN_D)

# (e) sequential pipeline
panel(6.3, 0.1, 8.6, 5.2, "(e) Sequential pipeline", "Fixed order; hand-off artifacts;\nerrors propagate downstream")
xs = [7.2, 9.2, 11.2, 13.2]
for i, x in enumerate(xs):
    node(x, 3.15, f"A{i + 1}")
for i in range(3):
    a, b = xs[i], xs[i + 1]
    arrow((a, 3.15), (b, 3.15))
    m = (a + b) / 2
    ax.add_patch(FancyBboxPatch((m - 0.22, 3.65), 0.44, 0.5, boxstyle="round,pad=0,rounding_size=0.06", facecolor="white", edgecolor=GREY, lw=1, zorder=3))
    ax.plot([m - 0.12, m + 0.12], [3.98, 3.98], color=GREY, lw=0.8, zorder=4); ax.plot([m - 0.12, m + 0.12], [3.85, 3.85], color=GREY, lw=0.8, zorder=4)
ax.text(8.2, 4.35, "hand-off artifact", ha="center", fontsize=9, color="#4A5568")
V = (12.2, 1.9); node(*V, "V", ORANGE, "white", ls=(0, (3, 2)))
arrow((11.2, 3.15), V, col=ORANGE, ls=(0, (3, 2))); arrow(V, (13.2, 3.15), col=ORANGE, ls=(0, (3, 2)))
ax.text(12.75, 1.55, "optional verifier stage", ha="left", va="center", fontsize=9, color=ORANGE)
save(fig, SLUG, "fig1-topologies")

# ---------------------------------------------------------------- Figure 2 — token multiplication, Eq. (2)
T0, Lt = 1000, 500
N = np.arange(1, 11)


def terms(N, R):
    return N * R * T0, N ** 2 * Lt * R * (R - 1) / 2, N * R * Lt


fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.9), gridspec_kw=dict(wspace=0.3, width_ratios=[1.15, 1]))
for R, col in [(2, GREEN_D), (3, BLUE), (4, ORANGE)]:
    t = sum(terms(N, R)); a1.plot(N, t / 1000, color=col, marker="o", ms=3.5, label=f"Eq. (2), R = {R}")
lin = terms(N, 3); a1.plot(N, (lin[0] + lin[2]) / 1000, color=BLUE, ls="--", lw=1.6, label="R = 3, linear terms only")
w = sum(terms(3, 3)); assert w == 27000
a1.plot([3], [27], "o", color=NAVY, ms=7, zorder=5)
a1.annotate("Worked example:\nN = 3, R = 3 → 27,000", xy=(3, 27), xytext=(1.2, 120), fontsize=9, color=NAVY,
            arrowprops=dict(arrowstyle="->", color=NAVY, lw=1))
a1.set_xlabel("Number of agents N"); a1.set_ylabel("Total tokens (thousands)"); a1.set_xticks(N)
a1.set_title("(a) Total tokens per task"); a1.legend(loc="upper left", fontsize=9, bbox_to_anchor=(0.0, 0.83))
a1.set_ylim(0, 380)
Nb = np.arange(1, 9); p = np.array(terms(Nb, 3), dtype=float); sh = p / p.sum(axis=0) * 100
a2.bar(Nb, sh[0], color=LIGHT, edgecolor="#B9C7D8", label=r"Task prompt, $N R T_0$")
a2.bar(Nb, sh[1], bottom=sh[0], color=BLUE, label=r"Cross-reading, $N^2 L R(R-1)/2$")
a2.bar(Nb, sh[2], bottom=sh[0] + sh[1], color=GREEN, label=r"Output, $N R L$")
a2.set_xticks(Nb); a2.set_ylim(0, 100); a2.set_xlabel("Number of agents N (R = 3)"); a2.set_ylabel("Share of total tokens (%)")
a2.set_title("(b) Composition of Eq. (2)"); a2.grid(axis="x", visible=False)
a2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=1, fontsize=9)
save(fig, SLUG, "fig2-token-growth")

# ---------------------------------------------------------------- Figure 3 — compounding error, Eqs. (4) and (5)
k = np.arange(1, 21)
fig, ax = plt.subplots(figsize=(7.0, 4.1))
for p, col in [(0.99, GREEN_D), (0.95, BLUE), (0.90, ORANGE)]:
    ax.plot(k, p ** k, color=col, marker="o", ms=3, label=f"p = {p:.2f}, no verification")
pv = 0.95 + 0.05 * 0.8 * 0.7
assert abs(pv - 0.978) < 1e-9
ax.plot(k, pv ** k, color=NAVY, ls="--", marker="s", ms=3, label="p = 0.95 with verifier (δ = 0.8, ρ = 0.7): p′ = 0.978")
for x, y, txt, tx, ty in [(5, 0.95 ** 5, "0.774", 6.4, 0.655), (10, 0.95 ** 10, "0.599", 11.3, 0.675), (5, pv ** 5, "0.895", 6.4, 0.795)]:
    ax.plot([x], [y], "o", color=NAVY, ms=6.5, mfc="white", mew=1.6, zorder=5)
    ax.annotate(txt, xy=(x, y), xytext=(tx, ty), fontsize=9.5, color=NAVY, fontweight="600", va="center",
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.8, shrinkB=4))
ax.set_xlim(0.5, 20.5); ax.set_ylim(0, 1.02); ax.set_xticks([1, 5, 10, 15, 20])
ax.set_xlabel("Number of sequential stages k"); ax.set_ylabel(r"End-to-end success probability $P_{\mathrm{success}}$")
ax.legend(loc="lower left", fontsize=9)
save(fig, SLUG, "fig3-compounding-error")
print("multiagent figures written; p' =", round(pv, 4), "P5' =", round(pv ** 5, 3))
