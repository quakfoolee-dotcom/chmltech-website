"""Figures for the hybrid digital twin paper on preheater fouling (Chmltech Online Journal, Vol. 106 draft). V1.
Data: data/twin/twin_results.json and twin_summary.json, written by twin_model.py and twin_summary.py."""
import json, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from style import *
import style

HERE = os.path.dirname(os.path.abspath(__file__))
style.OUT = os.path.join(HERE, "..", "figures")
SLUG = "hybrid-digital-twins-for-heat-exchanger-fouling-physics-machine-learning-and-the-combination-tested-on-a-steam-preheater"
INK2 = "#4A5568"
plt.rcParams["axes.axisbelow"] = True; plt.rcParams["text.parse_math"] = False
D = os.path.join(HERE, "data", "twin")
R = json.load(open(os.path.join(D, "twin_results.json"))); S = json.load(open(os.path.join(D, "twin_summary.json")))
r5 = [r for r in R if r["seed"] == 5][0]
COL = {"P": ORANGE, "O": GREY, "H": BLUE, "M": GREEN_D}
NAME = {"P": "Physics only", "O": "Physics, constant correction", "H": "Hybrid", "M": "Machine learning only"}

# ---------- Figure 1: learned correction to the tube-side coefficient ----------
Re = np.linspace(7000, 22000, 200)
f18, b = r5["calib_H"]; c = r5["calib_O"]
fig, ax = plt.subplots(figsize=(8.6, 4.0))
ax.plot(Re, 0.88 * (Re / 17800) ** 0.15, color=NAVY, lw=2.4, label="Plant (true, unknown to the monitors)")
ax.plot(Re, f18 * (Re / 18000) ** b, color=BLUE, lw=2, ls=(0, (4, 2)), label="Hybrid: learned from the clean days of runs 1 and 2")
ax.plot(Re, np.full_like(Re, c), color=GREY, lw=1.8, label="Constant correction from the same data")
ax.axhline(1.0, color=ORANGE, lw=1.6, label="Physics only: correlation as published")
ax.axvspan(7000, 11500, color=LIGHT, alpha=0.6, lw=0); ax.text(9250, 1.055, "turndown", ha="center", fontsize=8.6, color=INK2)
ax.axvspan(14300, 22000, color=LIGHT, alpha=0.35, lw=0); ax.text(18150, 1.055, "normal rate", ha="center", fontsize=8.6, color=INK2)
ax.plot([14200, 18500], [1.025, 1.025], color=BLUE, lw=3, solid_capstyle="butt"); ax.text(16350, 1.032, "clean-day calibration data (first 120 h)", ha="center", fontsize=8.0, color=BLUE, va="bottom")
ax.set_ylim(0.7, 1.08); ax.set_xlim(6500, 22500)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.set_xlabel("Tube-side Reynolds number"); ax.set_ylabel("Tube-side coefficient / correlation")
ax.legend(loc="lower right", fontsize=8.4)
save(fig, SLUG, "fig1-learned-correction")

# ---------- Figure 2: fouling estimates on the test run ----------
fig, ax = plt.subplots(figsize=(8.6, 4.4))
tr = r5["rf"]["true"]
for k in ("P", "O", "H"):
    t = np.array(r5["rf"][k]["t"]) / 8000 * 12; x = np.array(r5["rf"][k]["x"]) * 1e4
    ax.plot(t, x, color=COL[k], lw=1.1 if k != "H" else 1.4, alpha=0.9, label=f"{NAME[k]} (RMSE {r5['rf'][k]['rmse'] * 1e4:.2f})")
ax.plot(np.array(tr["t"]) / 8000 * 12, np.array(tr["x"]) * 1e4, color=NAVY, lw=2.4, label="True fouling resistance")
ax.set_xlim(0, 24); ax.set_xticks(range(0, 25, 3)); ax.set_ylim(-1, 8.5)
ax.set_xlabel("Months since cleaning, test run (daily medians of 4-hourly records)")
ax.set_ylabel("Fouling resistance (10⁻⁴ m²K/W)")
ax.legend(loc="upper left", fontsize=8.4, ncol=2)
save(fig, SLUG, "fig2-fouling-estimates")

# ---------- Figure 3: forecast error against months of data ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 4.0))
for k in ("P", "O", "H", "M"):
    rows = S["forecast"][k]; m = [r["month"] for r in rows]
    a1.plot(m, [r["median_err"] for r in rows], color=COL[k], marker="o", ms=4, lw=2, label=NAME[k])
    a2.plot(m, [r["share_within20"] for r in rows], color=COL[k], marker="o", ms=4, lw=2)
a1.set_ylim(0, 1.05); a2.set_ylim(0, 1.05)
for a in (a1, a2): a.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}")); a.set_xlabel("Months of data on the test run"); a.set_xticks([0.5, 1, 1.5, 2, 3])
a1.set_ylabel("Median error of forecast (capped at 100%)"); a2.set_ylabel("Forecasts within 20% of the truth")
a1.text(0.45, 0.03, "Errors above 100% and 'never'\nanswers count as 100%", fontsize=7.8, color=INK2, va="bottom")
fig.legend(*a1.get_legend_handles_labels(), loc="lower center", ncol=4, fontsize=8.2, bbox_to_anchor=(0.5, -0.06))
fig.tight_layout(rect=(0, 0.07, 1, 1))
save(fig, SLUG, "fig3-forecast-error")

# ---------- Figure 4: extrapolation to turndown ----------
fig, ax = plt.subplots(figsize=(8.6, 3.8))
keys = ["P", "O", "M", "H"]
med = [S["mae"][k] for k in keys]; p90 = [S["mae_p90"][k] for k in keys]
y = np.arange(len(keys))
ax.barh(y, med, color=[COL[k] for k in keys], height=0.55)
from matplotlib.patches import Patch
ax.scatter(p90, y, color=NAVY, marker="|", s=300, lw=2.2, zorder=3, label="P90 of 20 histories")
for yi, v, w in zip(y, med, p90): ax.text(max(v, w) + 0.015, yi, f"{v:.2f} (P90 {w:.2f})", va="center", fontsize=8.6)
ax.set_yticks(y); ax.set_yticklabels([NAME[k] for k in keys])
ax.set_xlim(0, 0.85); ax.set_xlabel("Mean absolute error of shell pressure at turndown, test run (bar)")
h_, l_ = ax.get_legend_handles_labels()
ax.legend([Patch(facecolor="white", edgecolor="#555555")] + h_, ["Bar length: median of 20 histories"] + l_, loc="upper right", fontsize=8.4)
save(fig, SLUG, "fig4-turndown-extrapolation")
print("ok")
