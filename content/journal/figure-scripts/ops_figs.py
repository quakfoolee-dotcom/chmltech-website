"""Figures for Vol. 106, Issues 3-4 (V5.41): Monte Carlo safety stock, and finite-capacity scheduling.
Data: data/ops/safety_stock.json and data/ops/fcs.json, written from the simulation models
(safety stock: 100,000-cycle lead-time-demand Monte Carlo, 40 x 200-year policy runs; scheduling: 100 x 50-week job-shop runs).
Usage: python3 -I content/journal/figure-scripts/ops_figs.py
"""
import json, os
import numpy as np
import matplotlib.pyplot as plt
from style import *
import style

HERE = os.path.dirname(os.path.abspath(__file__))
style.OUT = os.path.join(HERE, "..", "figures")
SS = "beyond-the-formula-setting-safety-stock-with-monte-carlo-simulation"
FCS = "why-the-erp-schedule-fails-on-the-shop-floor-finite-capacity-scheduling-rules-for-high-mix-manufacturers"
INK2 = "#4A5568"
plt.rcParams["axes.axisbelow"] = True
S = json.load(open(os.path.join(HERE, "data", "ops", "safety_stock.json")))
F = json.load(open(os.path.join(HERE, "data", "ops", "fcs.json")))


def usd(v): return f"${v:,.0f}"


# ---------- Safety stock, Figure 1: lead-time demand distribution ----------
fig, ax = plt.subplots(figsize=(8.6, 4.2))
h = [x for x in S["hist"] if x["lo"] >= 100]
ax.bar([x["lo"] + 25 for x in h], [x["share"] for x in h], width=46, color=LIGHT, edgecolor="#B9C7D8")
ymax = 21
for r, y, c, lw, ls in zip(S["rops"], [19.6, 17.8, 16.0], [GREY, GREY, BLUE], [1.3, 1.3, 2.2], ["--", "--", "-"]):
    ax.plot([r["rop"], r["rop"]], [0, y - 0.6], color=c, lw=lw, ls=ls)
    ax.text(r["rop"] + 6, y, f'{r["label"]}: {r["rop"]} pails, covers {r["cover"]:.1f}%', fontsize=9.5, va="center",
            color=NAVY, fontweight="600" if r["key"] == "mc" else "normal")
ax.set_xlim(100, 1250); ax.set_ylim(0, ymax)
ax.set_xlabel("Lead-time demand (pails)"); ax.set_ylabel("Share of simulated cycles (%)")
ax.grid(axis="x", visible=False)
save(fig, SS, "fig1-ltd-distribution")

# ---------- Safety stock, Figure 2: cycle service and fill rate against reorder point ----------
P = S["policy"]
fig, ax = plt.subplots(figsize=(8.6, 4.4))
s = [p["s"] for p in P]
ax.plot(s, [100 * p["fill"] for p in P], color=GREY, marker="o", ms=3.5, label="Fill rate (share of pails shipped from stock)")
ax.plot(s, [100 * p["csl"] for p in P], color=BLUE, marker="o", ms=3.5, lw=2.6, label="Cycle service level (cycles with no stockout)")
ax.axhline(95, color="#9AA8BA", ls=(0, (5, 4)), lw=1.2)
ax.text(898, 94.2, "95% cycle service target", ha="right", va="top", fontsize=9.5, color=INK2)
for x, lab, y, strong in [(715, "Formula: 715", 104.0, False), (759, "Monte Carlo: 759", 102.7, False), (S["undershoot_rop"], "Monte Carlo + undershoot: 777", 101.4, True)]:
    ax.plot([x, x], [75, y - 0.45], color=NAVY if strong else GREY, lw=1.6 if strong else 1.2, ls="-" if strong else ":")
    ax.text(x + 3, y, lab, fontsize=9.5, va="center", color=NAVY, fontweight="600" if strong else "normal")
ax.set_xlim(600, 900); ax.set_ylim(75, 105); ax.set_yticks([75, 80, 85, 90, 95, 100])
ax.set_xlabel("Reorder point s (pails)"); ax.set_ylabel("Service level (%)")
ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.1))
save(fig, SS, "fig2-service-vs-rop")

# ---------- Safety stock, Figure 3: annual cost against reorder point ----------
fig, ax = plt.subplots(figsize=(8.6, 4.4))
ax.plot(s, [p["hold"] / 1000 for p in P], color=GREY, lw=1.6, label="Holding cost")
ax.plot(s, [p["shortc"] / 1000 for p in P], color=GREY, lw=1.6, ls="--", label="Shortage cost ($60 per pail, assumed)")
ax.plot(s, [p["total"] / 1000 for p in P], color=BLUE, lw=2.6, marker="o", ms=3.5, label="Total cost")
best = min(P, key=lambda p: p["total"]); tgt = next(p for p in P if p["csl"] >= 0.945)
for p, lab, dy in [(best, f'Minimum {usd(best["total"])} at {best["s"]}', 2.6), (tgt, f'{100 * tgt["csl"]:.1f}% cycle service: {usd(tgt["total"])} at {tgt["s"]}', 4.6)]:
    ax.plot(p["s"], p["total"] / 1000, "o", ms=9, mfc="none", mec=NAVY, mew=1.2)
    ax.plot([p["s"], p["s"]], [p["total"] / 1000 + 0.35, p["total"] / 1000 + dy - 0.5], color=NAVY, lw=0.9)
    ax.text(p["s"], p["total"] / 1000 + dy, lab, ha="center", fontsize=9.5, color=NAVY, fontweight="600")
ax.set_xlim(595, 905); ax.set_ylim(0, 33)
ax.set_xlabel("Reorder point s (pails)"); ax.set_ylabel("Annual cost ($ thousand)")
ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.22))
save(fig, SS, "fig3-cost-vs-rop")

# ---------- Safety stock, Figure 4: sensitivity of safety stock ----------
C = sorted(S["sens"]["cases"], key=lambda c: c["high"] - c["low"])
base = S["sens"]["base"]
fig, ax = plt.subplots(figsize=(8.6, 3.8))
names = {"Base lead time (days)": "Normal lead time (days)"}
for i, c in enumerate(C):
    top = i >= len(C) - 2
    ax.barh(i, c["high"] - c["low"], left=c["low"], height=0.5, color=BLUE if top else LIGHT, edgecolor=BLUE if top else "#B9C7D8")
    ax.text(c["low"] - 3, i, f'{c["lo"]} → {c["low"]:.0f}', ha="right", va="center", fontsize=9.5, color=INK2)
    ax.text(c["high"] + 3, i, f'{c["hi"]} → {c["high"]:.0f}', ha="left", va="center", fontsize=9.5, color=INK2)
ax.axvline(base, color=NAVY, lw=1.2)
ax.text(base, len(C) - 0.02, f"Base case {base:.0f}", ha="center", va="bottom", fontsize=9.5, color=NAVY, fontweight="600", clip_on=False)   # above the plot, clear of the line (V5.44)
ax.set_yticks(range(len(C))); ax.set_yticklabels([names.get(c["name"], c["name"]) for c in C])
ax.set_xlim(150, 375); ax.set_ylim(-0.6, len(C) - 0.1)
ax.set_xlabel("Safety stock at the 95th percentile of lead-time demand (pails)")
ax.grid(axis="y", visible=False)
save(fig, SS, "fig4-ss-sensitivity")

# ---------- Scheduling, Figure 1: lead time against bottleneck utilization ----------
cv = F["curve"]; plan = float(np.mean([c["plan"] for c in cv]))
fig, ax = plt.subplots(figsize=(8.6, 4.3))
u = [c["util"] for c in cv]
ax.plot(u, [c["p95"] for c in cv], color=BLUE, lw=2.6, marker="o", ms=3.5)
ax.plot(u, [c["lt"] for c in cv], color=GREY, lw=2.0, marker="o", ms=3.5)
ax.axhline(plan, color="#9AA8BA", ls=(0, (6, 4)), lw=1.4)
ax.text(61, plan - 0.9, f"ERP planned lead time {plan:.1f} days", fontsize=9.5, color=NAVY, va="top")
ax.text(u[-1] + 0.6, cv[-1]["p95"], f'95th percentile {cv[-1]["p95"]:.1f}', fontsize=9.5, color=BLUE, va="center", fontweight="600")
ax.text(u[-1] + 0.6, cv[-1]["lt"] - 0.9, f'Mean {cv[-1]["lt"]:.1f}', fontsize=9.5, color=INK2, va="center")
ax.axvline(82, color=GREY, ls=":", lw=1.1); ax.text(81.6, 20.6, "This case: 82%", ha="right", fontsize=9.5, color=INK2)
ax.set_xlim(50, 99); ax.set_ylim(0, 21.5)
ax.set_xlabel("Welder utilization (%)"); ax.set_ylabel("Lead time from order entry (working days)")
save(fig, FCS, "fig1-leadtime-vs-load")

# ---------- Scheduling, Figure 2: on-time delivery by dispatching rule ----------
cf = F["configs"]
rows = [("SPT", "SPT", False), ("MDD all", "MDD, all work centres", True), ("MDD weld", "MDD at the welder only", True),
        ("FIFO", "FIFO (ERP default)", False), ("EDD", "EDD", False), ("CR", "Critical ratio", False)]
fig, ax = plt.subplots(figsize=(8.6, 3.9))
for i, (k, lab, acc) in enumerate(rows[::-1]):
    v, e = cf[k]["ot"], cf[k]["ot_ci"]
    ax.barh(i, v, height=0.56, color=BLUE if acc else LIGHT, edgecolor=BLUE if acc else "#B9C7D8")
    ax.errorbar(v, i, xerr=e, color=NAVY, capsize=3, lw=1.1)
    ax.text(v + e + 1, i, f"{v:.1f}%", va="center", fontsize=9.5, color=NAVY, fontweight="600" if acc else "normal")
ax.axvline(cf["FIFO"]["ot"], color="#9AA8BA", ls=(0, (5, 4)), lw=1.1)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[1] for r in rows[::-1]])
ax.set_xlim(0, 104); ax.set_xlabel("Orders shipped by the promised date (%, mean of 100 runs with 95% CI)")
ax.grid(axis="y", visible=False)
save(fig, FCS, "fig2-ontime-by-rule")

# ---------- Scheduling, Figure 3: on-time delivery against release buffer ----------
sw = F["sweep"]
fig, ax = plt.subplots(figsize=(8.6, 4.2))
B = [x["B"] for x in sw]
ax.plot(B, [x["lb_ot"] for x in sw], color=BLUE, lw=2.6, marker="o", ms=4, label="Load-based release, MDD at the welder")
ax.plot(B, [x["strict_ot"] for x in sw], color=GREY, lw=2.0, marker="o", ms=4, label="Strict DBR, FIFO")
ax.axhline(cf["FIFO"]["ot"], color="#9AA8BA", ls=(0, (6, 4)), lw=1.2)
ax.text(46, cf["FIFO"]["ot"] + 3.2, f'ERP default (push, FIFO): {cf["FIFO"]["ot"]:.1f}%', ha="center", fontsize=9.5, color=INK2)
bb = max(sw, key=lambda x: x["lb_ot"])
ax.annotate(f'{bb["lb_ot"]:.1f}% at {bb["B"]} h', (bb["B"], bb["lb_ot"]), xytext=(bb["B"], bb["lb_ot"] + 5.5), ha="center", fontsize=9.5,
            color=NAVY, fontweight="600", arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9))
ax.text(9.5, sw[0]["strict_ot"], "welder starves", fontsize=9.5, color=INK2, va="center")
ax.set_xlim(0, 66); ax.set_ylim(0, 104); ax.set_xticks([0, 8, 16, 24, 32, 40, 48, 64])
ax.set_xlabel("Release buffer (hours of welder work on the floor; 8 hours = 1 day)"); ax.set_ylabel("Orders on time (%)")
ax.legend(loc="lower right")
save(fig, FCS, "fig3-buffer-sweep")

# ---------- Scheduling, Figure 4: weekly on-time delivery through an order spike ----------
sp = F["spike"]; w = sp["weeks"]
fig, ax = plt.subplots(figsize=(8.6, 4.2))
ax.axvspan(19.5, 23.5, color="#EEF2F7", zorder=0)
ax.text(21.5, 101.5, "Order spike: +40% for 4 weeks", ha="center", fontsize=9.5, color=INK2)
ax.plot(w, sp["rec"], color=BLUE, lw=2.6, marker="o", ms=3.5, label="Load-based release, MDD at the welder")
ax.plot(w, sp["erp"], color=GREY, lw=2.0, marker="o", ms=3.5, label="ERP default (push, FIFO)")
lo = min(range(len(w)), key=lambda i: sp["erp"][i]); lr = min(range(len(w)), key=lambda i: sp["rec"][i])
ax.text(w[lo], sp["erp"][lo] - 4, f'{sp["erp"][lo]:.1f}%', ha="center", va="top", fontsize=9.5, color=NAVY, fontweight="600")
ax.text(w[lr], sp["rec"][lr] + 3, f'{sp["rec"][lr]:.1f}%', ha="center", va="bottom", fontsize=9.5, color=BLUE, fontweight="600")
ax.set_xlim(13.5, 33.5); ax.set_ylim(0, 105); ax.set_xticks(range(14, 34, 2))
ax.set_xlabel("Week of order entry"); ax.set_ylabel("Orders on time (%, pooled over 100 runs)")
ax.legend(loc="lower left")
save(fig, FCS, "fig4-spike-weekly")
print("8 figures written")
