"""Figures for the cost contingency paper (Chmltech Online Journal, Vol. 106 draft). V1.
Data: data/contingency/contingency.json, written by contingency_model.py.  Usage: python3 cont_figs.py"""
import json, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from style import *
import style

HERE = os.path.dirname(os.path.abspath(__file__))
style.OUT = os.path.join(HERE, "..", "figures")
SLUG = "setting-cost-contingency-by-monte-carlo-p50-p80-and-the-risks-behind-them-for-a-100-million-process-plant"
INK2 = "#4A5568"
plt.rcParams["axes.axisbelow"] = True
plt.rcParams["text.parse_math"] = False
R = json.load(open(os.path.join(HERE, "data", "contingency", "contingency.json")))
M = R["main"]; B = R["base"]

# ---------- Figure 1: S-curve ----------
fig, ax = plt.subplots(figsize=(8.6, 4.6))
q = np.array(R["scurve"]["q"]) / 100; x = np.array(R["scurve"]["main"])
ax.plot(x, q, color=BLUE, lw=2.2)
for p, lab, col in ((50, "P50", GREEN_D), (80, "P80", ORANGE), (90, "P90", NAVY)):
    v = M[f"P{p}"]; ax.plot([v, v], [0, p / 100], color=col, lw=1.2, ls=(0, (4, 3))); ax.plot([95, v], [p / 100] * 2, color=col, lw=1.2, ls=(0, (4, 3)))
    left = p == 80
    ax.text(v + (-0.4 if left else 0.4), {50: 0.04, 80: 0.14, 90: 0.27}[p], f"{lab} C${v:.1f}M\n(+{v - B:.1f}%)", color=col, fontsize=9,
            ha="right" if left else "left")
for flat, col in ((10, GREY), (15, GREY)):
    v = B * (1 + flat / 100); pr = float(np.interp(v, x, q))
    ax.scatter([v], [pr], color=col, zorder=3, s=36)
    ax.annotate(f"Base + {flat}%:\n{1 - pr:.0%} chance of overrun", (v, pr), xytext=(101.0, 0.36 if flat == 10 else 0.64),
                fontsize=8.8, color=INK2, ha="left", arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.axvline(B, color=INK2, lw=1); ax.text(B + 0.3, 0.92, "Base estimate\nC$100M", fontsize=8.8, color=INK2)
ax.set_xlim(95, 130); ax.set_ylim(0, 1.0)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.set_xlabel("Final fixed capital cost at base-date prices (C$ million)"); ax.set_ylabel("Probability of not exceeding")
save(fig, SLUG, "fig1-s-curve")

# ---------- Figure 2: contingency build-up ----------
sysm = M["sys_mean"] - B; rk = M["risk_mean"]; mean = M["mean"]
steps = [("Base estimate", B, B, BLUE), ("Skew in the\nline-item ranges", sysm, B + sysm, GREY), ("Expected cost of\nrisk events", rk, mean, ORANGE),
         ("Mean", mean, mean, NAVY), ("Margin to P80", M["P80"] - mean, M["P80"], GREEN_D), ("P80 budget", M["P80"], M["P80"], GREEN_D)]
fig, ax = plt.subplots(figsize=(8.6, 4.4))
for i, (lab, v, top, col) in enumerate(steps):
    if lab in ("Base estimate", "Mean", "P80 budget"):
        ax.bar(i, v - 90, bottom=90, color=col, width=0.6); ax.text(i, v + 0.4, f"C${v:.1f}M", ha="center", fontsize=9)
    else:
        ax.bar(i, v, bottom=top - v, color=col, width=0.6); ax.text(i, top + 0.4, f"+{v:.1f}", ha="center", fontsize=9)
ax.set_xticks(range(len(steps))); ax.set_xticklabels([s[0] for s in steps], fontsize=9)
ax.set_ylim(90, 122); ax.set_ylabel("C$ million (axis starts at 90)")
er = R["escfx"]["P80"]
ax.text(1.5, 92.5, f"Held separately: escalation and\nexchange-rate reserve, C${er:.1f}M at P80", ha="center", fontsize=8.6, color=INK2)
save(fig, SLUG, "fig2-contingency-build-up")

# ---------- Figure 3: what drives P80 ----------
from matplotlib.patches import Patch
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 4.4), gridspec_kw=dict(width_ratios=[1, 1.15]))
sw = sorted(R["swing"].items(), key=lambda kv: -kv[1])[:8][::-1]
ax1.barh(range(len(sw)), [v for _, v in sw], color=BLUE, height=0.6)
for i, (k_, v) in enumerate(sw): ax1.text(v + 0.02, i, f"{v:.2f}", va="center", fontsize=8.4)
ax1.set_yticks(range(len(sw))); ax1.set_yticklabels([k_ for k_, _ in sw], fontsize=8.6)
ax1.set_xlim(0, 0.95); ax1.set_xlabel("Fall in P80 if the account\nwere fixed at its mean (C$M)", fontsize=8.8)
ax1.set_title("Estimating uncertainty", fontsize=9.2, loc="left")
rk = sorted(R["risk_p80"].items(), key=lambda kv: -kv[1])[::-1]
yy = np.arange(len(rk))
ax2.barh(yy + 0.18, [v for _, v in rk], color=ORANGE, height=0.34, label="Risk eliminated")
ax2.barh(yy - 0.18, [R["risk_p80_ev"][k_] for k_, _ in rk], color="#F2B880", height=0.34, label="Risk replaced by its expected value")
for i, (k_, v) in enumerate(rk): ax2.text(v + 0.02, i + 0.18, f"{v:.2f}", va="center", fontsize=8.0)
ax2.set_yticks(yy); ax2.set_yticklabels([k_ for k_, _ in rk], fontsize=8.4)
ax2.set_xlim(0, 2.1); ax2.set_xlabel("Fall in P80 (C$M)", fontsize=8.8); ax2.set_title("Risk events", fontsize=9.2, loc="left")
ax2.legend(fontsize=8.2, loc="upper center", bbox_to_anchor=(0.3, -0.16), ncol=2, frameon=False)
fig.tight_layout()
save(fig, SLUG, "fig3-drivers")

# ---------- Figure 4: correlation and range width ----------
cases = [("Class 3 ranges", R["corr"]["0.0"]["P80"], R["corr"]["1.0"]["P80"]),
         ("Ranges 1.5 times wider", R["wide"]["1.5_0.0"]["P80"], R["wide"]["1.5_1.0"]["P80"]),
         ("Ranges 2 times wider", R["wide"]["2.0_0.0"]["P80"], R["wide"]["2.0_1.0"]["P80"])]
fig, ax = plt.subplots(figsize=(8.6, 4.0))
xx = np.arange(len(cases))
ax.bar(xx - 0.18, [c[1] - B for c in cases], width=0.34, color=GREY, label="Line items independent")
ax.bar(xx + 0.18, [c[2] - B for c in cases], width=0.34, color=BLUE, label="Line items correlated through common drivers")
for i, c in enumerate(cases):
    ax.text(i - 0.18, c[1] - B + 0.3, f"{c[1]-B:.1f}", ha="center", fontsize=9); ax.text(i + 0.18, c[2] - B + 0.3, f"{c[2]-B:.1f}", ha="center", fontsize=9)
ax.set_xticks(xx); ax.set_xticklabels([c[0] for c in cases], fontsize=9.2)
ax.set_ylabel("P80 contingency (C$ million)"); ax.legend(fontsize=8.8, loc="upper left"); ax.set_ylim(0, 34)
save(fig, SLUG, "fig4-correlation")

# ---------- Figure 5: estimate class ----------
edges = np.linspace(80, 200, 121); ctr = (edges[:-1] + edges[1:]) / 2
fig, ax = plt.subplots(figsize=(8.6, 4.4))
cols = {"Class 5": GREY, "Class 4": BLUE, "Class 3": GREEN_D}
for cl in ("Class 5", "Class 4", "Class 3"):
    h = np.array(R["classes"][cl]["hist"], float); h /= h.sum()
    ax.plot(ctr, h, color=cols[cl], lw=2, label=f'{cl}: P50 C${R["classes"][cl]["P50"]:.0f}M, P80 C${R["classes"][cl]["P80"]:.0f}M')
    ax.fill_between(ctr, h, color=cols[cl], alpha=0.12)
    ax.axvline(R["classes"][cl]["P80"], color=cols[cl], lw=1, ls=(0, (4, 3)))
ax.axvline(B, color=INK2, lw=1); ax.text(B + 0.6, ax.get_ylim()[1] * 0.97, "Base\nC$100M", ha="left", va="top", fontsize=8.6, color=INK2)
ax.set_xlim(90, 180); ax.set_xlabel("Final fixed capital cost (C$ million); dashed lines: P80")
ax.set_ylabel("Share of iterations per C$1M"); ax.legend(fontsize=8.8, loc="upper right")
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
save(fig, SLUG, "fig5-estimate-class")
print("ok")
