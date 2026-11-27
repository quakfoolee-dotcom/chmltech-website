"""Figures for the feed preheater fouling paper (Chmltech Online Journal, Vol. 106 draft). V2 (red-team fixes).
Data: data/preheater/hx.json and hx_extras.json, written by hx_model.py and hx_extras.py.  Usage: python3 hx_figs.py"""
import json, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from style import *
import style

HERE = os.path.dirname(os.path.abspath(__file__))
style.OUT = os.path.join(HERE, "..", "figures")
SLUG = "sizing-the-feed-preheater-under-fouling-uncertainty-area-margin-cleaning-and-condensate-stall"
INK2 = "#4A5568"
plt.rcParams["axes.axisbelow"] = True
plt.rcParams["text.parse_math"] = False
R = json.load(open(os.path.join(HERE, "data", "preheater", "hx.json")))
X = json.load(open(os.path.join(HERE, "data", "preheater", "hx_extras.json")))
D = R["design"]; BA = R["by_area"]; AREAS = [a for a in R["areas"]]

# ---------- Figure 1: fouling resistance over a run ----------
fc = R["foul_curve"]; t = np.array(fc["t"]) / 8000 * 12
fig, ax = plt.subplots(figsize=(8.6, 4.2))
ax.fill_between(t, np.array(fc["p10"]) * 1e4, np.array(fc["p90"]) * 1e4, color=BLUE, alpha=0.15, lw=0, label="P10 to P90 of 500 scenarios")
ax.plot(t, np.array(fc["p50"]) * 1e4, color=BLUE, lw=2.2, label="Median")
ax.axhline(1.76, color=ORANGE, lw=1.3, ls=(0, (4, 3)))
ax.text(23.6, 1.76 - 0.12, "TEMA design value for the tube side, 1.76", color=ORANGE, fontsize=8.8, ha="right", va="top")
ax.set_xlim(0, 24); ax.set_ylim(0, 7.5); ax.set_xticks(range(0, 25, 3))
ax.set_xlabel("Months of operation since the last cleaning")
ax.set_ylabel("Tube-side fouling resistance (10⁻⁴ m²K/W)")
ax.legend(loc="upper left", fontsize=9)
save(fig, SLUG, "fig1-fouling-over-a-run")

# ---------- Figure 3 (file fig3): required steam pressure over a run ----------
sp = R["steam_path"]
fig, ax = plt.subplots(figsize=(8.6, 4.6))
cols = {"6": ORANGE, "8": BLUE, "10": GREEN_D}
for A in ("6", "8", "10"):
    ax.plot(t, sp[A]["normal"], color=cols[A], lw=2.2, label=f"{A} m², normal rate")
    ax.plot(t, sp[A]["turndown"], color=cols[A], lw=1.6, ls=(0, (4, 2.5)), label=f"{A} m², 50% turndown")
ax.axhline(R["steam_max_barg"], color=NAVY, lw=1.2)
ax.text(0.3, R["steam_max_barg"] + 0.05, f"Highest shell pressure available: {R['steam_max_barg']:.1f} barg (header less valve drop)", fontsize=8.6, color=NAVY, va="bottom")
ax.axhspan(-0.6, 0.0, color=GREY, alpha=0.13, lw=0)
ax.axhline(0.0, color=INK2, lw=1)
ax.text(23.7, -0.53, "Below atmospheric: no pressure to push condensate through the trap into an atmospheric return (stall)", fontsize=8.6, color=INK2, ha="right", va="bottom")
ax.set_xlim(0, 24); ax.set_ylim(-0.6, 3.0); ax.set_xticks(range(0, 25, 3))
ax.set_xlabel("Months of operation since the last cleaning (median fouling scenario, median feed case)")
ax.set_ylabel("Shell-side steam pressure needed (barg)")
ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.90), fontsize=8.6, ncol=2)
save(fig, SLUG, "fig3-steam-pressure-over-a-run")

# ---------- Figure 2 (file fig2): annual cost against area ----------
A_ = np.array([BA[str(a)]["A_act"] for a in AREAS], float)
cap = np.array([BA[str(a)]["total"] - BA[str(a)]["clean_cost"] - BA[str(a)]["lost_cost"] for a in AREAS])
cln = np.array([BA[str(a)]["clean_cost"] for a in AREAS]); lst = np.array([BA[str(a)]["lost_cost"] for a in AREAS])
tot = np.array([BA[str(a)]["total"] for a in AREAS]); p95 = np.array([BA[str(a)]["total_p95"] for a in AREAS])
fig, ax = plt.subplots(figsize=(8.6, 4.6))
ax.plot(A_, tot / 1e3, color=NAVY, lw=2.4, marker="o", ms=4, label="Mean total annual cost")
ax.plot(A_, p95 / 1e3, color=NAVY, lw=1.3, ls=(0, (4, 3)), label="P95 total annual cost")
ax.plot(A_, cln / 1e3, color=ORANGE, lw=1.6, label="Unplanned cleaning, incl. lost production")
ax.plot(A_, np.maximum(lst, 1) / 1e3, color=GREY, lw=1.6, label="Rate cuts before cleaning")
ax.plot(A_, cap / 1e3, color=GREEN_D, lw=1.6, label="Annualised installed cost")
ax.set_yscale("log"); ax.set_ylim(0.3, 6000); ax.set_xlim(3.6, 14.4)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}" if v >= 1 else f"{v:.1f}"))
for x, lab, yy in ((D["A_clean"], "Clean,\ndesign case", 0.4), (D["A_tema"], "TEMA\nfouling", 0.4), (D["A_tema20"], "TEMA\n+ 20%", 0.4)):
    ax.axvline(x, color=INK2, lw=0.9, ls=(0, (2, 2)))
    ax.text(x + 0.08, yy, lab, fontsize=8.2, color=INK2, va="bottom", ha="left")
ax.set_xlabel("Heat-transfer area (m², outside of tubes)"); ax.set_ylabel("C$ thousand a year (log scale)")
ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.62), fontsize=8.6)
save(fig, SLUG, "fig2-annual-cost-against-area")

# ---------- Figure 4: the trade-off, rate cut against stall ----------
pc = np.array([BA[str(a)]["p_cut_in_run"] for a in AREAS]); sN = np.array([BA[str(a)]["stallN"] for a in AREAS]); sT = np.array([BA[str(a)]["stallT"] for a in AREAS])
lin = X["linear"]; la = np.array([float(k) for k in lin]); lpc = np.array([lin[k]["p_cut"] for k in lin])
fig, ax = plt.subplots(figsize=(8.6, 4.6))
ax.plot(A_, pc, color=ORANGE, lw=2.4, marker="o", ms=4, label="Chance of a rate cut within a 24-month run")
ax.plot(la, lpc, color=ORANGE, lw=1.3, ls=(0, (4, 3)), marker="o", ms=3, label="Same, if fouling keeps growing (linear)")
ax.plot(A_, sN, color=BLUE, lw=2.2, marker="o", ms=4, label="Share of normal-rate hours in stall")
ax.plot(A_, sT, color=BLUE, lw=1.4, ls=(0, (4, 2.5)), marker="o", ms=3, label="Share of turndown hours in stall")
ax.axvspan(8, 9, color=GREEN, alpha=0.15, lw=0)
ax.text(8.5, 1.03, "8 to 9 m²", ha="center", fontsize=8.8, color=GREEN_D, va="bottom")
ax.set_xlim(3.6, 14.4); ax.set_ylim(0, 1.1)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.set_xlabel("Heat-transfer area (m²)"); ax.set_ylabel("Probability or share of hours")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), fontsize=8.6, ncol=2)
save(fig, SLUG, "fig4-rate-cut-against-stall")

# ---------- Figure 5: drivers ----------
names = {"rinf": "Asymptotic fouling resistance", "f_hi": "Tube-side coefficient factor", "p_hdr": "Steam header pressure",
         "tau": "Fouling time constant", "margin": "Product margin", "h_o": "Condensing coefficient", "td": "Share of hours at turndown"}
dr = sorted(R["drivers7"].items(), key=lambda kv: abs(kv[1]))
fig, ax = plt.subplots(figsize=(8.6, 3.9))
ax.barh(range(len(dr)), [v for _, v in dr], color=[ORANGE if v > 0 else BLUE for _, v in dr], height=0.6)
for i, (k, v) in enumerate(dr):
    ax.text(v + (0.015 if v >= 0 else -0.015), i, f"{v:+.2f}", va="center", ha="left" if v >= 0 else "right", fontsize=8.6)
ax.set_yticks(range(len(dr))); ax.set_yticklabels([names[k] for k, _ in dr])
ax.axvline(0, color=INK2, lw=0.9); ax.set_xlim(-0.6, 0.85)
ax.set_xlabel("Rank correlation with total annual cost at 7 m² (positive: raises cost)")
save(fig, SLUG, "fig5-drivers")
print("ok")
