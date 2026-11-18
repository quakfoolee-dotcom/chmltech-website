"""Figures for the pump arrangement paper (Chmltech Online Journal, Vol. 106, Issue 9 draft). V1.
Data: data/arr/arrangements.json, written from the arrangement model (arrangements.py, on top of pumpvalve_model.py).
Usage: python3 arr_figs.py   (from this folder)
"""
import json, os
import numpy as np
import matplotlib.pyplot as plt
from style import *
import style

HERE = os.path.dirname(os.path.abspath(__file__))
style.OUT = os.path.join(HERE, "..", "figures")
SLUG = "choosing-the-pump-arrangement-under-uncertainty-monte-carlo-comparison-of-single-parallel-and-variable-speed-options"
INK2 = "#4A5568"
plt.rcParams["axes.axisbelow"] = True
plt.rcParams["text.parse_math"] = False
D = json.load(open(os.path.join(HERE, "data", "arr", "arrangements.json")))
R, F = D["R"], D["F"]
NAMES = ["A", "B", "C3", "C2", "E3", "E2"]
SHORT = {"A": "A\n1×100% + spare\nvalve", "B": "B\n1×100% + spare\ndrives", "C3": "C3\n2×50% + spare\nvalve",
         "C2": "C2\n2×50%, no spare\nvalve", "E3": "E3\n2×50% + spare\ndrives", "E2": "E2\n2×50%, no spare\ndrives"}
COL = {"A": BLUE, "B": GREEN_D, "C3": ORANGE, "C2": "#C9A27A", "E3": NAVY, "E2": GREY}

# ---------- Figure 1: pump curves, staging and the operating demands ----------
c = F["cloud"]; Qr, Hr = c["Qr"], c["Hr"]
q = np.linspace(0, 13.5, 300)
def H(qq, qr, n=1.0, S=1.2): return Hr * (S * n ** 2 - (S - 1) * (qq / qr) ** 2)
fig, ax = plt.subplots(figsize=(8.6, 4.6))
ax.scatter(c["QN"], c["HN"], s=5, color=GREY, alpha=0.35, lw=0, label="Demand, normal operation (system head, valve excluded)")
ax.scatter(c["QT"], c["HT"], s=5, color=BRIGHT, alpha=0.35, lw=0, label="Demand at 50% turndown")
ax.plot(q, H(q, Qr), color=BLUE, label=f"One 100% pump, or two 50% pumps together (rated {Qr:.1f} m³/h at {Hr:.1f} m)")
qh = np.linspace(0, 8.2, 200)
ax.plot(qh, H(qh, Qr / 2), color=ORANGE, label=f"One 50% pump alone (rated {Qr / 2:.2f} m³/h at {Hr:.1f} m)")
for n in (0.85, 0.75):
    ax.plot(q, np.where(H(q, Qr, n) > 0, H(q, Qr, n), np.nan), color=GREEN_D, lw=1.4, ls=(0, (5, 3)))
    qq = 13.3 if n == 0.85 else 7.4
    ax.text(qq, H(qq, Qr, n) + (3.5 if n == 0.85 else 2.0), f"100% pump at {n:.0%} speed", color=GREEN_D, fontsize=9, ha="right",
            bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none", alpha=0.9))
ax.set_xlim(0, 13.5); ax.set_ylim(35, 105)
ax.set_xlabel("Total flow (m³/h)"); ax.set_ylabel("Head (m)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), fontsize=9, markerscale=3, ncol=2)
save(fig, SLUG, "fig1-curves-and-demand")

# ---------- Figure 2: where each pump runs on its curve (share of BEP flow) ----------
keys = ["A", "B", "C", "E", "D"]
lab = {"A": "A: 1×100%,\nvalve", "B": "B: 1×100%,\ndrive", "C": "C: 2×50%,\nvalve, staged", "E": "E: 2×50%,\ndrives, staged",
       "D": "D: 2×50%, drive\non lead only"}
fig, ax = plt.subplots(figsize=(8.6, 4.4))
ax.axhspan(0.70, 1.20, color=GREEN, alpha=0.13, lw=0)
ax.text(5.42, 1.18, "Preferred operating\nregion, 70–120%", color=GREEN_D, fontsize=9, va="top", ha="right")
ax.axhline(0.30, color=ORANGE, lw=1.0, ls=(0, (4, 3)))
ax.text(5.42, 0.315, "Minimum stable flow, 30%", color=ORANGE, fontsize=9, ha="right")
for i, k in enumerate(keys):
    for dx, arr, colr, nm in ((-0.17, F[k]["xN"], BLUE, "Normal operation"), (0.17, F[k]["xT"], BRIGHT, "50% turndown")):
        a = np.array(arr); pcts = np.percentile(a, [1, 25, 50, 75, 99])
        ax.plot([i + 1 + dx] * 2, [pcts[0], pcts[4]], color=colr, lw=1.2)
        ax.add_patch(plt.Rectangle((i + 1 + dx - 0.12, pcts[1]), 0.24, pcts[3] - pcts[1], color=colr, alpha=0.85, lw=0,
                                   label=nm if i == 0 else None))
        ax.plot([i + 1 + dx - 0.12, i + 1 + dx + 0.12], [pcts[2]] * 2, color="white", lw=2)
ax.set_xticks(range(1, 6)); ax.set_xticklabels([lab[k] for k in keys], fontsize=9.2)
ax.set_xlim(0.45, 5.55); ax.set_ylim(0.2, 1.3)
ax.set_ylabel("Flow per running pump / its BEP flow at its speed")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.legend(loc="upper left", fontsize=9); ax.grid(axis="x", visible=False)
save(fig, SLUG, "fig2-share-of-bep")

# ---------- Figure 3: average electrical power, normal and turndown ----------
fig, ax = plt.subplots(figsize=(8.6, 3.8))
x = np.arange(5); w = 0.36
Pn = [R["hyd"][k]["normal"]["P_el"] for k in keys]; Pt = [R["hyd"][k]["turndown"]["P_el"] for k in keys]
b1 = ax.bar(x - w / 2, Pn, w, color=BLUE, label="Normal operation (85–110% of design rate)")
b2 = ax.bar(x + w / 2, Pt, w, color=BRIGHT, label="50% turndown")
for bars in (b1, b2):
    for b in bars: ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.08, f"{b.get_height():.2f}", ha="center", fontsize=8.8, color=INK2)
ax.set_xticks(x); ax.set_xticklabels([lab[k] for k in keys], fontsize=9.2)
ax.set_ylabel("Average electrical power (kW)"); ax.set_ylim(0, 7.8); ax.legend(loc="upper right", fontsize=9, ncol=2)
ax.grid(axis="x", visible=False)
save(fig, SLUG, "fig3-power")

# ---------- Figure 4: availability, lost production and failures ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.9), gridspec_kw=dict(wspace=0.32))
xs = np.arange(len(NAMES))
lost = [R["econ"][o]["lost_h_y"] for o in NAMES]; lost95 = [R["econ"][o]["lost_h_p95"] for o in NAMES]
a1.bar(xs, lost, color=[COL[o] for o in NAMES], width=0.62)
a1.errorbar(xs, lost, yerr=[np.zeros(6), np.array(lost95) - np.array(lost)], fmt="none", ecolor=NAVY, elinewidth=1, capsize=3)
a1.set_yscale("log"); a1.set_ylim(0.05, 120)
a1.set_yticks([0.1, 1, 10]); a1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}")); a1.yaxis.set_minor_formatter(plt.NullFormatter())
a1.set_ylabel("Lost production, full-rate hours a year"); a1.set_title("Lost production (mean, bar to P95)", fontsize=10.5)
for i, (v, v95) in enumerate(zip(lost, lost95)): a1.text(i, v95 * 1.3, f"{v:.2f}" if v < 1 else f"{v:.0f}", ha="center", fontsize=8.6, color=INK2)
fail = [R["econ"][o]["fail_y"] for o in NAMES]
a2.bar(xs, fail, color=[COL[o] for o in NAMES], width=0.62)
for i, v in enumerate(fail): a2.text(i, v + 0.015, f"{v:.2f}", ha="center", fontsize=8.6, color=INK2)
a2.set_ylabel("Pump or drive failures a year"); a2.set_title("Repairs (mean)", fontsize=10.5); a2.set_ylim(0, 0.95)
for a in (a1, a2):
    a.set_xticks(xs); a.set_xticklabels(NAMES, fontsize=9.5); a.grid(axis="x", visible=False)
save(fig, SLUG, "fig4-availability")

# ---------- Figure 5: life-cycle cost, components and spread; probability cheapest ----------
fig, ax = plt.subplots(figsize=(8.6, 4.3))
comp = [("cap", "Installed capital", NAVY), ("energy_y", "Electricity", BRIGHT), ("repair_y", "Repairs", ORANGE), ("lost_y", "Lost production", GREY)]
bottom = np.zeros(6); pvf = R["const"]["PVF"]
for k, nm, colr in comp:
    v = np.array([R["econ"][o][k] * (1 if k == "cap" else pvf) for o in NAMES]) / 1000
    ax.bar(xs, v, 0.6, bottom=bottom, color=colr, label=nm); bottom += v
lo = np.array([R["econ"][o]["lcc_p5"] for o in NAMES]) / 1000; hi = np.array([R["econ"][o]["lcc_p95"] for o in NAMES]) / 1000
mean = np.array([R["econ"][o]["lcc_mean"] for o in NAMES]) / 1000
ax.errorbar(xs + 0.38, mean, yerr=[mean - lo, hi - mean], fmt="o", color=INK2, ms=3.5, elinewidth=1, capsize=3, label="Mean, P5 to P95")
for i, o in enumerate(NAMES):
    p = R["econ"][o]["p_cheapest"]
    ax.text(i, hi[i] + 25, f"cheapest in\n{p:.0%} of scenarios" if p >= 0.005 else ("cheapest in\n<1%" if p > 0 else "cheapest in\n0%"), ha="center", fontsize=8.4,
            color=GREEN_D if p > 0.5 else INK2, fontweight="600" if p > 0.5 else "normal")
ax.set_xticks(xs); ax.set_xticklabels([SHORT[o] for o in NAMES], fontsize=8.6)
ax.set_ylabel("20-year life-cycle cost (C$ thousand)"); ax.set_ylim(0, 1300)
ax.legend(loc="upper left", fontsize=8.8, ncol=3); ax.grid(axis="x", visible=False)
save(fig, SLUG, "fig5-life-cycle-cost")

# ---------- Figure 6: probability cheapest against duty size ----------
fig, ax = plt.subplots(figsize=(8.6, 3.9))
for key, ls, nm in (("base", "-", "turndown 0–25% of hours"), ("0.5", (0, (5, 3)), "turndown 50% of hours")):
    d = R["p_by_size"][key]; kw = R["p_by_size"]["base"]["kw"]
    for o in ("B", "E3", "A"):
        ax.plot(kw, d["p"][o], color=COL[o], ls=ls, lw=2.0 if ls == "-" else 1.6,
                label=f"{o}, {nm}")
ax.set_xscale("log"); ax.set_xticks([4, 6, 10, 20, 40, 100]); ax.set_xticklabels(["4", "6", "10", "20", "40", "100"])
ax.set_xlabel("Duty: average electrical power of option B over the year, base case (kW)")
ax.set_ylabel("Probability cheapest"); ax.set_ylim(0, 1.02)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.legend(loc="center left", fontsize=8.8, ncol=2)
ax.text(0.99, 0.04, "Steps follow motor frame sizes", transform=ax.transAxes, ha="right", fontsize=8.4, color=INK2)
save(fig, SLUG, "fig6-probability-by-size")
print("6 figures written")
