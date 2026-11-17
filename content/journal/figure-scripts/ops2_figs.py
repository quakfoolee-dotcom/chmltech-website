"""Figures for Vol. 106, Issues 5-7 (V5.42): total landed cost sourcing, due-date quoting, intermittent demand forecasting.
Data: data/ops/tlc.json, quote.json, croston.json, written from the models in content/journal/ops/models/
(sourcing: mixed-integer program + 20,000-year Monte Carlo; quoting: 100 x 50-week job-shop runs per setting;
forecasting: five populations of 1,000 simulated items).
Usage: python3 -I content/journal/figure-scripts/ops2_figs.py
"""
import json, os
import numpy as np
import matplotlib.pyplot as plt
from style import *
import style

HERE = os.path.dirname(os.path.abspath(__file__))
style.OUT = os.path.join(HERE, "..", "figures")
TLC = "beyond-the-unit-price-total-landed-cost-optimization-for-sme-sourcing"
QT = "quoting-lead-times-you-can-keep-due-date-setting-for-make-to-order-manufacturers"
CR = "forecasting-lumpy-demand-does-croston-beat-a-moving-average"
INK2 = "#4A5568"
plt.rcParams["axes.axisbelow"] = True
plt.rcParams["text.parse_math"] = False   # "C$" labels are text, not maths
T = json.load(open(os.path.join(HERE, "data", "ops", "tlc.json")))
Q = json.load(open(os.path.join(HERE, "data", "ops", "quote.json")))
C = json.load(open(os.path.join(HERE, "data", "ops", "croston.json")))
k = lambda v: v / 1000

# ---------- Landed cost, Figure 1: waterfall of the change by component ----------
a, b = T["det"]["price_only"], T["det"]["tlc_optimal"]
comp = [("purchase", "Purchase price"), ("duty", "Duty and surtax"), ("freight", "Freight"), ("broker", "Brokerage"),
        ("quality", "Quality"), ("carry", "Carrying cost"), ("terms", "Payment terms"), ("fixed", "Supplier management")]
fig, ax = plt.subplots(figsize=(8.6, 4.6))
x0 = a["total"]; rows = [("Lowest-price plan", 0, a["total"], "total")]
for key, lab in comp:
    d = b[key] - a[key]; rows.append((lab, x0, d, "up" if d > 0 else "down")); x0 += d
rows.append(("Total-cost plan", 0, b["total"], "total"))
for i, (lab, start, d, kind) in enumerate(rows):
    y = len(rows) - 1 - i
    if kind == "total":
        ax.barh(y, k(d), left=0, color=NAVY if i == 0 else BLUE, height=0.58)
        ax.text(k(d) + 2, y, f"C${d:,.0f}", va="center", fontsize=9.5, color=NAVY, fontweight="600")
    else:
        lo, hi = (start, start + d) if d > 0 else (start + d, start)
        ax.barh(y, k(hi - lo), left=k(lo), color=ORANGE if d > 0 else GREEN_D, height=0.58)
        ax.text(k(hi) + 2, y, f"{'+' if d > 0 else '−'}C${abs(d):,.0f}", va="center", fontsize=9.5, color=NAVY)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1])
ax.set_xlim(500, 735); ax.set_xlabel("Annual total landed cost (C$ thousand); the axis starts at C$500,000")
ax.grid(axis="y", visible=False)
save(fig, TLC, "fig1-cost-waterfall")

# ---------- Landed cost, Figure 2: total cost against the container rate ----------
F = T["feu"]; fx = [f["feu"] / 1000 for f in F]
fig, ax = plt.subplots(figsize=(8.6, 4.2))
ax.plot(fx, [k(f["price_only"]) for f in F], color=GREY, marker="o", ms=3.5, label="Lowest-price plan")
ax.plot(fx, [k(f["plan_7500"]) for f in F], color=NAVY, lw=1.6, ls="--", label="Total-cost plan fixed at the US$7,500 choice")
ax.plot(fx, [k(f["optimal"]) for f in F], color=BLUE, lw=2.6, marker="o", ms=3.5, label="Total-cost plan re-optimized at each rate")
ax.axvline(7.5, color="#9AA8BA", ls=(0, (5, 4)), lw=1.1)
ax.text(7.62, 653, "Base case\nUS$7,500", fontsize=9.5, color=INK2, va="top")
ax.set_xlabel("China 40-foot container rate (US$ thousand)"); ax.set_ylabel("Annual total landed cost (C$ thousand)")
ax.set_ylim(555, 655); ax.legend(loc="upper left")
save(fig, TLC, "fig2-freight-sweep")

# ---------- Landed cost, Figure 3: mean against 95th percentile, five plans ----------
M = T["mc"]
lab = {"price_only": "Lowest price", "landed_price": "Lowest price plus freight", "tlc_optimal": "Total-cost plan",
       "tlc_dual": "Total-cost plan, dual-sourced hardware", "north_america": "All North America"}
off = {"price_only": (-4, 6, "right"), "landed_price": (4, 0, "left"), "tlc_optimal": (-3, -9, "right"),
       "tlc_dual": (3, 3, "left"), "north_america": (3, -6, "left")}
fig, ax = plt.subplots(figsize=(8.6, 4.4))
for key, v in M.items():
    best = key == "tlc_optimal"
    ax.scatter(k(v["mean"]), k(v["p95"]), s=70 if best else 50, color=BLUE if best else GREY, zorder=3, edgecolor="white")
    dx, dy, ha = off[key]
    ax.text(k(v["mean"]) + dx, k(v["p95"]) + dy, f'{lab[key]}\nmean C${v["mean"] / 1000:,.0f}k, P95 C${v["p95"] / 1000:,.0f}k',
            fontsize=9.2, ha=ha, va="center", color=NAVY, fontweight="600" if best else "normal")
ax.set_xlim(565, 650); ax.set_ylim(600, 740)
ax.set_xlabel("Mean annual total landed cost (C$ thousand)"); ax.set_ylabel("95th-percentile annual cost (C$ thousand)")
save(fig, TLC, "fig3-risk-scatter")

# ---------- Landed cost, Figure 4: mean cost against the cost per part short ----------
S = T["short"]; sx = sorted(S, key=float)
fig, ax = plt.subplots(figsize=(8.6, 4.2))
for key, lab2, c, lw in [("tlc_optimal", "Total-cost plan (China hardware, single source)", BLUE, 2.6),
                         ("tlc_dual", "Dual-sourced hardware (70/30)", ORANGE, 2.0), ("north_america", "All North America", GREY, 2.0)]:
    ax.plot([float(s) for s in sx], [k(S[s][key]["mean"]) for s in sx], color=c, lw=lw, marker="o", ms=3.5, label=lab2)
ax.axvline(190, color="#9AA8BA", ls=(0, (5, 4)), lw=1.1)
ax.text(186, 610.5, "Break-even on mean cost: about C$190", ha="right", fontsize=9.5, color=INK2)
ax.set_xlabel("Cost per part short, no spot market or air cover (C$)"); ax.set_ylabel("Mean annual total landed cost (C$ thousand)")
ax.set_ylim(574, 612); ax.legend(loc="lower right")
save(fig, TLC, "fig4-shortage-breakeven")

# ---------- Quoting, Figure 1: on-time against average quote, FIFO ----------
fig, ax = plt.subplots(figsize=(8.6, 4.4))
names = [("erp", "Routing (ERP default)", GREY, "-"), ("flat", "Flat", GREY, "--"), ("backlog", "Routing plus backlog", GREEN_D, "-"),
         ("load", "Backlog plus work", BLUE, "-"), ("fit", "Fitted", ORANGE, "--")]
for key, lab3, c, ls in names:
    pts = sorted([(x["quote"], x["ot"]) for x in Q["sweep"] if x["rule"] == key and x["sched"] == "FIFO"])
    pts = [p for p in pts if 4 <= p[0] <= 17]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, ls=ls, lw=2.6 if key == "load" else 1.9, marker="o", ms=3, label=lab3)
ax.axhline(95, color="#9AA8BA", ls=(0, (5, 4)), lw=1.1); ax.text(4.2, 95.8, "95% target", ha="left", fontsize=9.5, color=INK2)
ax.scatter([7.86], [76.7], s=60, color=NAVY, zorder=4)
ax.annotate("Today: 7.9 days, 76.7% on time", (7.86, 76.7), xytext=(9.3, 66), fontsize=9.5, color=NAVY,
            arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9))
ax.set_xlim(4, 17); ax.set_ylim(40, 101)
ax.set_xlabel("Average quoted lead time (working days)"); ax.set_ylabel("Orders delivered by the quoted date (%)")
ax.legend(loc="lower right")
save(fig, QT, "fig1-quote-tradeoff")

# ---------- Quoting, Figure 2: weekly on-time and quote through a spike ----------
w = Q["spike_weeks"]; sp = Q["spike"]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(8.6, 5.6), sharex=True, gridspec_kw=dict(height_ratios=[1.25, 1], hspace=0.12))
for axx in (a1, a2): axx.axvspan(19.5, 23.5, color="#EEF2F7", zorder=0)
for key, lab4, c, lw in [("FIFO load", "Backlog plus work", BLUE, 2.6), ("FIFO erp", "Routing (ERP default)", GREY, 2.0)]:
    a1.plot(w, sp[key]["weekly_ot"], color=c, lw=lw, marker="o", ms=3, label=lab4)
    a2.plot(w, sp[key]["weekly_q"], color=c, lw=lw, marker="o", ms=3, label=lab4)
a1.text(21.5, 101, "Orders +40% for 4 weeks", ha="center", fontsize=9.5, color=INK2)
lo = int(np.argmin(sp["FIFO erp"]["weekly_ot"]))
a1.text(w[lo] + 0.4, sp["FIFO erp"]["weekly_ot"][lo], f'{sp["FIFO erp"]["weekly_ot"][lo]:.0f}%', va="center", fontsize=9.5, color=NAVY, fontweight="600")
a1.set_ylim(60, 104); a1.set_ylabel("On time (%)"); a1.legend(loc="lower left")
a2.set_ylim(6, 16); a2.set_ylabel("Average quote (days)"); a2.set_xlabel("Week of order entry (FIFO dispatch)")
a2.set_xticks(range(14, 36, 2)); a2.set_xlim(13.5, 35.5)
save(fig, QT, "fig2-spike-weekly")

# ---------- Forecasting, Figure 1: weeks of stock for 95% fill ----------
rows = [("ma", "Moving average (13 weeks)"), ("ses", "SES"), ("sba", "SBA"), ("tsb", "TSB"), ("croston", "Croston"),
        ("boot", "Bootstrap, full history"), ("norm52", "Normal formula, last 52 weeks (benchmark)")]
fig, ax = plt.subplots(figsize=(8.6, 4.0))
base = C["ma"]
for i, (key, lab5) in enumerate(rows[::-1]):
    v = C[key]; bench = key == "norm52"
    ax.barh(i, v, height=0.58, color="white" if bench else (BLUE if key != "ma" else LIGHT), edgecolor=BLUE if key != "ma" else "#B9C7D8",
            hatch="///" if bench else None, lw=1.0)
    ch = "" if key == "ma" else f" ({(v / base - 1) * 100:+.1f}%)".replace("-", "−")
    ax.text(v + 0.08, i, f"{v:.2f}{ch}", va="center", fontsize=9.5, color=NAVY)
ax.axvline(base, color="#9AA8BA", ls=(0, (5, 4)), lw=1.1)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[1] for r in rows][::-1])
ax.set_xlim(0, 9.8); ax.set_xlabel("Weeks of stock needed for a 95% fill rate (all 5,000 items)")
ax.grid(axis="y", visible=False)
save(fig, CR, "fig1-stock-at-95")
print("7 figures written")
