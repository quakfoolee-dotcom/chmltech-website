"""Figures for the critical spare parts paper (Chmltech Online Journal, Vol. 106, Issue 10 draft). V1.
Data: data/spares/spares.json, written by the spares model (spares_model.py, analyse.py, extras.py).
Usage: python3 spares_figs.py   (from this folder)
"""
import json, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter
from matplotlib.colors import ListedColormap
from style import *
import style

HERE = os.path.dirname(os.path.abspath(__file__))
style.OUT = os.path.join(HERE, "..", "figures")
SLUG = "stocking-critical-spare-parts-under-uncertainty-when-abc-analysis-and-safety-stock-formulas-fail"
INK2 = "#4A5568"
plt.rcParams["axes.axisbelow"] = True
plt.rcParams["text.parse_math"] = False
R = json.load(open(os.path.join(HERE, "data", "spares", "spares.json")))
PT = {p["id"]: p for p in R["parts"]}
def k(x): return f"C${x:,.0f}" if x < 1000 else f"C${x/1000:,.0f}k" if x < 1e6 else f"C${x/1e6:,.2f}M"

# ---------- Figure 1: annual cost against stock level for four parts ----------
show = [("P8", "Compressor valve set (1.0 failures in a lead time per 13 years)"), ("P7", "Agitator double seal"),
        ("P10", "Preheater tube bundle (capacity 70% while waiting)"), ("P13", "Pressure transmitter, 2-out-of-3")]
fig, axs = plt.subplots(2, 2, figsize=(8.6, 5.6))
for ax, (pid, ttl) in zip(axs.flat, show):
    p = PT[pid]; S = np.arange(len(p["mean_total"]))
    hold = np.array(p["mean_hold"]) / 1000; down = np.array(p["mean_down"]) / 1000; tot = hold + down
    ax.bar(S, hold, color=BLUE, width=0.6, label="Holding cost")
    ax.bar(S, down, bottom=hold, color=ORANGE, width=0.6, label="Expected lost production")
    b = int(np.argmin(tot)); top = max(tot[1:].max(), tot[b] * 3)
    ax.set_ylim(0, top * 1.18)
    for s in S:
        y = min(tot[s], top * 1.08)
        ax.text(s, y + top * 0.02, (f"{tot[s]:,.1f}" if tot[s] < 10 else f"{tot[s]:,.0f}" if tot[s] < 1000 else f"{tot[s]/1000:,.1f}M") + ("▲" if tot[s] > top * 1.08 else ""),
                ha="center", fontsize=8.4, color=GREEN_D if s == b else INK2, fontweight="bold" if s == b else "normal")
    ax.set_title(f'{pid} {p["name"]}, {p["eq"].split(" ")[0] if False else p["eq"]}', fontsize=9.2, loc="left")
    ax.set_xticks(S); ax.set_xlabel("Spares held, S", fontsize=9); ax.set_ylabel("C$ thousand a year", fontsize=9)
    ax.tick_params(labelsize=8.5)
axs[0, 0].legend(fontsize=8.4, loc="upper right")
fig.tight_layout(h_pad=1.2)
save(fig, SLUG, "fig1-cost-against-stock")

# ---------- Figure 2: portfolio cost of each stocking policy ----------
order = [("none", "No spares\n(slow movers purged)"), ("ready95", "Poisson,\n95% ready rate"), ("normal", "Safety stock formula,\n95%, base stock = ROP + 1"),
         ("one", "One of each"), ("fill95", "Poisson,\n95% fill rate"), ("robust", "Cost optimum\n(this paper)")]
fig, axs = plt.subplots(1, 3, figsize=(8.6, 4.3), sharey=True)
y = np.arange(len(order))[::-1]
metrics = [("total", "Expected cost a year (C$)"), ("value", "Value of spares held (C$)"), ("lost_h", "Lost full-rate hours a year")]
for ax, (mkey, lab) in zip(axs, metrics):
    v = [R["portfolio"][kk][mkey] for kk, _ in order]
    cols = [GREY, GREY, BLUE, BLUE, BLUE, GREEN_D]
    ax.barh(y, v, color=cols, height=0.6)
    for yi, vi in zip(y, v):
        t = (k(vi) if mkey != "lost_h" else f"{vi:,.0f} h") if vi > 0 else "C$0"
        ax.text(vi + max(v) * 0.03, yi, t, va="center", fontsize=8.6)
    ax.set_xlabel(lab, fontsize=8.8); ax.tick_params(labelsize=8.3)
    ax.set_xlim(0, max(v) * 1.55)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: (k(x) if mkey != "lost_h" else f"{x:,.0f}") if x else "0"))
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
axs[0].set_yticks(y); axs[0].set_yticklabels([n for _, n in order], fontsize=8.8)
fig.tight_layout()
save(fig, SLUG, "fig2-policies")

# ---------- Figure 4: screening index against the simulation ----------
fig, ax = plt.subplots(figsize=(8.6, 4.4))
for s_ in R["screen"]:
    red = s_["redundant"]; xv = s_["index2"] if red else s_["index"]
    ax.scatter(xv, s_["sim_ratio"], s=48, color=ORANGE if red else BLUE, zorder=3,
               label=("Equipment with an installed spare, Eq. (4)" if red else "Single equipment, Eq. (3)"))
    ax.annotate(s_["id"], (xv, s_["sim_ratio"]), xytext={"P1": (-16, 5), "P3": (5, -10)}.get(s_["id"], (5, -3)), textcoords="offset points", fontsize=8.6, color=INK2)
lim = [0.1, 1000]
ax.plot(lim, lim, color=INK2, lw=1, ls=(0, (4, 3)))
ax.text(400, 250, "Index equals simulation", color=INK2, fontsize=8.6, rotation=37, ha="center")
ax.axhline(1, color=GREEN_D, lw=1); ax.axvline(1, color=GREEN_D, lw=1)
ax.text(30, 1.15, "First spare pays for itself above this line", color=GREEN_D, fontsize=8.6, va="bottom")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(*lim); ax.set_ylim(*lim)
for a_ in (ax.xaxis, ax.yaxis):
    a_.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}")); a_.set_minor_formatter(NullFormatter())
ax.set_xlabel("Screening index at most likely values: value of the first spare / its holding cost")
ax.set_ylabel("Same ratio from the simulation (scenario mean)")
h, l = ax.get_legend_handles_labels(); u = dict(zip(l, h)); ax.legend(u.values(), u.keys(), fontsize=8.8, loc="upper left")
save(fig, SLUG, "fig4-screening-index")

# ---------- Figure 3: installed spares, repair and pooling ----------
X = R["extras"]
def best(v): return min(v)
cases = [
    ("Feed pump seal P1", [("With installed spare pump", best(X["redundancy"]["P1"]["total"])), ("No installed spare pump", best(X["redundancy"]["P1x"]["total"]))]),
    ("Agitator gearbox P6", [("Own spare, new in 20 wk", best(PT["P6"]["mean_total"])), ("Repaired in 6 wk", best(X["repairable"]["P6r"]["total"])),
                             ("Shared by 3 plants", best(X["pool"]["P6"]["pooled_per_plant"]))]),
    ("Compressor motor P9", [("Own spare, new in 26 wk", best(PT["P9"]["mean_total"])), ("Rewound in 4 wk", best(X["repairable"]["P9r"]["total"])),
                             ("Shared by 3 plants", best(X["pool"]["P9"]["pooled_per_plant"]))]),
    ("Tube bundle P10", [("Own spare, new in 30 wk", best(PT["P10"]["mean_total"])), ("Repaired in 8 wk", best(X["repairable"]["P10r"]["total"])),
                         ("Shared by 3 plants", best(X["pool"]["P10"]["pooled_per_plant"]))]),
]
fig, ax = plt.subplots(figsize=(8.6, 4.6))
yy = 0; ticks = []; labs = []
cols = [BLUE, ORANGE, GREEN_D]
for gname, items in cases:
    for j, (lab, v) in enumerate(items):
        ax.barh(yy, v / 1000, color=cols[j] if gname != "Feed pump seal P1" else [BLUE, GREY][j], height=0.7)
        ax.text(v / 1000 + 0.8, yy, f"C${v/1000:,.1f}k", va="center", fontsize=8.6)
        ticks.append(yy); labs.append(lab); yy -= 1
    ax.text(-0.5, yy + len(items) + 0.55, gname, fontsize=9.2, fontweight="bold", ha="left", transform=ax.get_yaxis_transform() if False else ax.transData)
    yy -= 0.9
ax.set_yticks(ticks); ax.set_yticklabels(labs, fontsize=8.8)
ax.set_xlabel("Expected cost a year at the best stock level, per plant (C$ thousand)")
ax.set_xlim(0, max(v for _, it in cases for _, v in it) / 1000 * 1.2)
save(fig, SLUG, "fig3-redundancy-repair-pooling")

# ---------- Figure 5: decision map ----------
mp = X["map"]; m = np.array(mp["m"]); rho = np.array(mp["rho"]); G = np.array(mp["S"])
fig, ax = plt.subplots(figsize=(8.6, 4.8))
cmap = ListedColormap(["#FFFFFF", "#BFDAF2", "#7FB2E0", "#4A8FD0", "#1F5E9E", "#0B2E59", "#061A33", "#000000"])
ax.pcolormesh(m, rho, G, cmap=cmap, vmin=-0.5, vmax=7.5, shading="auto")
ax.contour(m, rho, G, levels=[0.5, 1.5, 2.5, 3.5, 4.5], colors="#1F3864", linewidths=0.7)
for s, (xm, yr) in {0: (0.05, 1.5), 1: (0.0025, 3000), 2: (0.06, 2200), 3: (0.25, 2200), 4: (0.6, 4000), 5: (1.9, 30000)}.items():
        ax.text(xm, yr, f"S = {s}" if s < 5 else "S ≥ 5", color="white" if s >= 3 else INK2, fontsize=9.4, ha="center", va="center", fontweight="bold")
if False:
    pass
for p in R["parts"]:
    if p["N"] != p["K"]: continue
    ch = 6.25 * 300 * p["cap"]; r_ = ch * 8000 / (0.25 * p["cost"])
    ax.scatter(p["mlt"], r_, s=40, color=ORANGE, edgecolor="#7A3E00", zorder=3)
    ax.annotate(p["id"], (p["mlt"], r_), xytext={"P11": (-24, 4), "P6": (5, -10)}.get(p["id"], (5, 3)), textcoords="offset points", fontsize=8.6, color="#7A3E00")
ax.set_xscale("log"); ax.set_yscale("log")
for a_ in (ax.xaxis, ax.yaxis):
    a_.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}")); a_.set_minor_formatter(NullFormatter())
ax.set_xlabel("Expected failures during one replenishment lead time, m = λ K L")
ax.set_ylabel("Cost of a year of downtime / holding cost of one part")
ax.text(0.99, 0.02, "Single equipment, no buffer; points: this plant's single-equipment parts at most likely values",
        transform=ax.transAxes, ha="right", fontsize=8.2, color=INK2)
save(fig, SLUG, "fig5-decision-map")
print("ok")
