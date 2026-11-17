"""Figures for the Monte Carlo pump and control valve sizing paper (V5.45; V2 adds the moderate deterministic baseline; V3 reruns at 40% pump efficiency, moderate case at the most likely route).
Data: data/pe/pumpvalve.json, written from content/journal/pe/models/pumpvalve/ (20,000 correlated cases).
Usage: python3 -I content/journal/figure-scripts/pe_figs.py
"""
import json, os
import numpy as np
import matplotlib.pyplot as plt
from style import *
import style

HERE = os.path.dirname(os.path.abspath(__file__))
style.OUT = os.path.join(HERE, "..", "figures")
SLUG = "sizing-pumps-and-control-valves-under-uncertainty-monte-carlo-design-points-for-chemical-plants"
INK2 = "#4A5568"
plt.rcParams["axes.axisbelow"] = True
plt.rcParams["text.parse_math"] = False
D = json.load(open(os.path.join(HERE, "data", "pe", "pumpvalve.json")))
R = D["R"]


def curve(Qr, Hr, q): return Hr * (1.20 - 0.20 * (q / Qr) ** 2)


# ---------- Figure 1: head the pump must deliver, 20,000 cases ----------
need = np.array(D["need"])
fig, ax = plt.subplots(figsize=(8.6, 4.0))
ax.hist(need, bins=70, color=BLUE, alpha=0.85, edgecolor="white", lw=0.3)
p50, p95, p99 = np.percentile(need, [50, 95, 99])
top = ax.get_ylim()[1]
for v, lab, c, dy in [(p50, f"P50 {p50:.1f} m", NAVY, 0.97), (p95, f"P95 {p95:.1f} m", NAVY, 0.84), (p99, f"P99 {p99:.1f} m", NAVY, 0.71),
                      (R["moderate"]["Hr"], f'Moderate\nmargins {R["moderate"]["Hr"]:.1f} m', GREEN_D, 0.97),
                      (R["stacked"]["Hr"], f'Full stacked\nmargins {R["stacked"]["Hr"]:.1f} m', ORANGE, 0.97)]:
    ax.axvline(v, color=c, lw=1.2, ls="-" if c in (ORANGE, GREEN_D) else (0, (5, 3)))
    ax.text(v + 0.5, top * dy, lab, fontsize=9.5, color=c, va="top", fontweight="600" if c in (ORANGE, GREEN_D) else "normal",
            bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none", alpha=0.9))
ax.set_xlim(60, 112); ax.set_xlabel("Head the pump must deliver at the case's own flow, with 0.7 bar across the control valve (m)")
ax.set_ylabel("Cases"); ax.grid(axis="x", visible=False)
save(fig, SLUG, "fig1-required-head")

# ---------- Figure 2: pump curves against the cloud of operating demands ----------
q = np.linspace(0, 14, 200)
fig, ax = plt.subplots(figsize=(8.6, 4.6))
ax.scatter(D["Q_pts"], D["need_pts"], s=5, color="#9AA8BA", alpha=0.45, lw=0, label="Operating demands (2,500 of 20,000 cases)")
for key, lab, c, lw in [("stacked", "Full stacked margins", ORANGE, 2.2), ("moderate", "Moderate margins", GREEN_D, 2.0),
                        ("mc95", "Monte Carlo P95", BLUE, 2.6)]:
    Qr, Hr = R[key]["Qr"], R[key]["Hr"]
    ax.plot(q, curve(Qr, Hr, q), color=c, lw=lw, label=f"{lab}: rated {Qr:.1f} m³/h at {Hr:.1f} m")
    ax.scatter([Qr], [Hr], s=46, color=c, zorder=4, edgecolor="white")
ax.axvline(R["Qn"], color=NAVY, lw=1.0, ls=(0, (5, 3))); ax.text(R["Qn"] + 0.15, 128, f'Normal flow\n{R["Qn"]:.1f} m³/h', ha="left", va="top", fontsize=9.5, color=NAVY)
ax.set_xlim(0, 14); ax.set_ylim(50, 135)
ax.set_xlabel("Flow (m³/h)"); ax.set_ylabel("Head (m)"); ax.legend(loc="lower left")
save(fig, SLUG, "fig2-pump-curves")

# ---------- Figure 5: control valve opening, normal operation and 50% turndown ----------
fig, axs = plt.subplots(1, 2, figsize=(8.6, 3.8), sharey=True, gridspec_kw=dict(wspace=0.08))
bins = np.linspace(0, 100, 41)
for ax, key, lab in [(axs[0], "mc95", "Monte Carlo P95 design\n(1.5-inch valve, rated Cv 34)"), (axs[1], "stacked", "Full stacked-margin design\n(1-inch valve, rated Cv 16)")]:
    op, lo = np.array(D["open"][key][0]) * 100, np.array(D["open"][key][1]) * 100
    ax.axvspan(0, 10, color="#FBEBEB", zorder=0); ax.axvspan(90, 100, color="#FBEBEB", zorder=0)
    ax.hist(lo, bins=bins, color=LIGHT, edgecolor="#B9C7D8", lw=0.6, label="50% turndown")
    ax.hist(op, bins=bins, color=BLUE, alpha=0.9, edgecolor="white", lw=0.3, label="Normal operation")
    ax.set_title(lab, fontsize=10.5, color=NAVY, loc="left")
    ax.set_xlim(0, 100); ax.set_xlabel("Valve opening (% of travel)"); ax.grid(axis="x", visible=False)
axs[0].set_ylabel("Cases (4,000 of each)"); axs[0].legend(loc="upper left", fontsize=9)
axs[1].text(95, axs[1].get_ylim()[1] * 0.95, "Outside\n10-90%", ha="center", va="top", fontsize=9, color="#9B2C2C")
save(fig, SLUG, "fig5-valve-opening")

# ---------- Figure 3: what drives the size (one at a time, P5 to P95 of each input) ----------
label = {"level": ("Tank level", "{:.2f} to {:.2f} m", 1), "p_rx": ("Reactor pressure", "{:.2f} to {:.2f} barg", 1),
         "rate": ("Production rate", "{:.0f}% to {:.0f}%", 100), "T": ("Feed temperature", "{:.0f} to {:.0f} °C", 1),
         "recycle": ("Recycle ratio", "{:.2f} to {:.2f}", 1), "L_dis": ("Discharge route length", "{:.0f} to {:.0f} m", 1),
         "foul": ("Preheater fouling multiplier", "{:.2f} to {:.2f}", 1), "eps": ("Pipe roughness", "{:.2f} to {:.2f} mm", 1000),
         "strainer": ("Strainer clogging multiplier", "{:.1f} to {:.1f}", 1), "K_dis": ("Fittings, sum of K", "{:.1f} to {:.1f}", 1),
         "blanket": ("Nitrogen blanket", "{:.3f} to {:.3f} barg", 1)}
names = {t["name"]: f'{label[t["name"]][0]} ({label[t["name"]][1].format(t["lo"] * label[t["name"]][2], t["hi"] * label[t["name"]][2])})'
         for t in R["tornado"]}
T = R["tornado"][::-1]; base = R["tornado_base"]
fig, ax = plt.subplots(figsize=(8.6, 4.8))
for i, t in enumerate(T):
    lo, hi = min(t["h_lo"], t["h_hi"]), max(t["h_lo"], t["h_hi"])
    op = t["name"] in ("level", "p_rx", "rate", "T", "recycle", "blanket")
    ax.barh(i, hi - lo, left=lo, height=0.55, color=BLUE if op else LIGHT, edgecolor=BLUE if op else "#B9C7D8")
    ax.text(hi + 0.15, i, f"{hi - lo:.1f} m", va="center", fontsize=9.2, color=INK2)
ax.axvline(base, color=NAVY, lw=1.1)
ax.text(base, len(T) - 0.4, f"Base case {base:.1f} m", ha="center", va="bottom", fontsize=9.5, color=NAVY, fontweight="600", clip_on=False)
ax.set_yticks(range(len(T))); ax.set_yticklabels([names[t["name"]] for t in T])
ax.set_xlim(70, 81); ax.set_ylim(-0.6, len(T) - 0.4)
ax.set_xlabel("Head needed at the case's own flow (m); dark bars are operating variables, light bars design unknowns")
ax.grid(axis="y", visible=False)
save(fig, SLUG, "fig3-tornado")

# ---------- Figure 4: convergence of the P95 rated head ----------
C = R["convergence"]
n = [c["n"] for c in C]
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ax.fill_between(n, [c["lo"] for c in C], [c["hi"] for c in C], color=LIGHT, label="Range of 95% of 200 repeat runs")
ax.plot(n, [c["mean"] for c in C], color=BLUE, lw=2.4, marker="o", ms=4, label="Mean of 200 runs")
ax.set_xscale("log"); ax.set_xticks(n); ax.set_xticklabels([f"{v:,}" for v in n])
ax.set_xlabel("Cases per run"); ax.set_ylabel("P95 rated head (m)"); ax.set_ylim(80.5, 84.5); ax.legend(loc="upper right")
save(fig, SLUG, "fig4-convergence")

# ---------- Figure 6: 20-year life-cycle cost of five options ----------
opts = [("stacked", "Full stacked\nmargins, valve"), ("moderate", "Moderate\nmargins, valve"), ("mc95", "Monte Carlo\nP95, valve"),
        ("stacked_vfd", "Full stacked\nmargins, drive"), ("mc95_vfd", "Monte Carlo\nP95, drive")]
pvf = (1 - 1.08 ** -20) / 0.08
fig, ax = plt.subplots(figsize=(8.6, 4.2))
for i, (k, lab) in enumerate(opts):
    d = R["designs"][k]; cap = d["capex_total"] / 1000; en = d["energy_cy"] * pvf / 1000
    ax.bar(i, cap, width=0.56, color=NAVY, label="Purchased equipment (2 pumps, 2 motors, valve or drives)" if i == 0 else None)
    ax.bar(i, en, bottom=cap, width=0.56, color=BLUE, label="Electricity, present value over 20 years" if i == 0 else None)
    ax.text(i, cap + en + 1.5, f"C${(cap + en):,.0f}k", ha="center", fontsize=10, color=NAVY, fontweight="600")
ax.set_xticks(range(len(opts))); ax.set_xticklabels([o[1] for o in opts], fontsize=9.5)
ax.set_ylabel("C$ thousand"); ax.set_ylim(0, 175)
ax.legend(loc="upper center", ncol=2, fontsize=9.2, frameon=False, bbox_to_anchor=(0.5, 1.0)); ax.grid(axis="x", visible=False)
save(fig, SLUG, "fig6-life-cycle-cost")
print("6 figures written")
