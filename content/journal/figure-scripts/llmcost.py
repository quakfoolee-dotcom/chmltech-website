"""Figures for Vol. 104(7): Score Versus Cost Per Task (returns to reasoning effort).
Data: data/llmcost/*.csv (retrieved 11 Nov 2026; corrected dataset in LLM_Cost_Performance_Dataset_V1.xlsx)."""
import csv, math, os, re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
from style import *
import style
style.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")

SLUG = "score-versus-cost-per-task-returns-to-reasoning-effort-in-frontier-language-models"
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "llmcost")
rd = lambda n: list(csv.DictReader(open(os.path.join(D, n + ".csv"), encoding="utf-8")))
BENCH, IDX = rd("benchmarks"), rd("indexes")
EORD = ["none", "minimal", "low", "medium", "high", "xhigh", "max"]
ELAB = {"minimal": "Min", "low": "Low", "medium": "Med", "high": "High", "xhigh": "Xhigh", "max": "Max"}
INK2 = "#4A5568"
PURPLE, RUST = "#6B4FA0", "#B5523B"
COL = {"Claude Fable 5.2": BLUE, "Claude Opus 5.5": ORANGE, "Opus 5.5": ORANGE, "GPT-6 Astra": GREEN_D, "Gemini 4 Carbon": NAVY,
       "Claude Fable 5.1": GREY, "DeepSeek V4.1 Flash": BRIGHT, "Grok 4.7": NAVY, "Muse Spark 1.3": PURPLE, "GLM-5.3": GREY, "Gemini 4 Argon": RUST}
MK = {"Claude Fable 5.2": "o", "Claude Opus 5.5": "s", "Opus 5.5": "s", "GPT-6 Astra": "^", "Gemini 4 Carbon": "D", "Claude Fable 5.1": "v",
      "DeepSeek V4.1 Flash": "o", "Grok 4.7": "D", "Muse Spark 1.3": "P", "GLM-5.3": "v", "Gemini 4 Argon": "X"}
LEAD = ["Claude Fable 5.2", "Claude Opus 5.5", "GPT-6 Astra", "Gemini 4 Carbon", "Claude Fable 5.1"]
eff = lambda s: s.lower().split(" ")[0].strip(",")
se = lambda p, n: 100 * math.sqrt(max(p, 0) / 100 * (1 - max(p, 0) / 100) / n)


def logx(ax, xs, lo_f=1.5, hi_f=2.0):
    ax.set_xscale("log"); lo, hi = min(xs) / lo_f, max(xs) * hi_f; ax.set_xlim(lo, hi)
    t = [v for v in [0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100] if lo <= v <= hi]
    ax.xaxis.set_major_locator(FixedLocator(t)); ax.xaxis.set_major_formatter(FixedFormatter([f"${v:g}" for v in t])); ax.xaxis.set_minor_locator(NullLocator())


# ---------- data ----------
VALS = []
for x in IDX:
    if x["source"] == "Vals AI (reasoning-effort study)":
        VALS.append(dict(model=x["model"], effort=eff(x["variant_or_effort"]), acc=float(x["quality_value"]), cost=float(x["cost_value_usd"]),
                         se=float(re.search(r"standard error ([\d.]+)", x["notes"]).group(1))))
FC = []
for x in BENCH:
    if x["benchmark"] == "FrontierCode" and x["reported_by"] == "benchmark_operator" and x["model"] in LEAD:
        c = float(x["cost_per_task_usd"])
        FC.append(dict(model=x["model"], effort=eff(x["variant_or_effort"]), score=float(x["score_pct"]), file_cost=c,
                       cost=round(c / 1.25, 3) if x["model"] == "Claude Fable 5.2" else c))
ARC = []
for x in BENCH:
    if x["benchmark"] == "ARC-AGI-2" and x["model"] in LEAD and eff(x["variant_or_effort"]) != "none":
        ARC.append(dict(model=x["model"], effort=eff(x["variant_or_effort"]), score=float(x["score_pct"]), cost=float(x["cost_per_task_usd"]),
                        lb="recorded usage only" in x["notes"]))
srt = lambda pts: sorted(pts, key=lambda p: EORD.index(p["effort"]))

# ---------- Figure 1: anatomy of cost per task (schematic) ----------
fig, ax = plt.subplots(figsize=(8.6, 3.9))
levels = ["Low", "Medium", "High", "Max"]
inp = [1.0] * 4; cached = [0.35] * 4; reason = [0.4, 0.9, 2.0, 4.6]; ans = [0.35, 0.4, 0.45, 0.5]
x = np.arange(4); w = 0.52
b1 = ax.bar(x, inp, w, color=LIGHT, edgecolor="#B9C7D8", label="Input tokens × input price")
b2 = ax.bar(x, cached, w, bottom=inp, color="#BFD8EA", edgecolor="#9CC0DA", label="Cached input × cache price")
b3 = ax.bar(x, reason, w, bottom=np.add(inp, cached), color=BLUE, label="Reasoning tokens × output price")
b4 = ax.bar(x, ans, w, bottom=np.add(np.add(inp, cached), reason), color=NAVY, label="Answer tokens × output price")
for i in range(4):
    tot = inp[i] + cached[i] + reason[i] + ans[i]
    ax.text(i, tot + 0.12, f"{tot / (inp[0] + cached[0] + reason[0] + ans[0]):.1f}×", ha="center", color=NAVY, fontsize=10, fontweight="600")
ax.set_xticks(x); ax.set_xticklabels([f"{l} effort" for l in levels]); ax.set_yticklabels([]); ax.tick_params(axis="y", length=0)
ax.set_ylabel("Cost per task (relative units)"); ax.grid(False); ax.set_ylim(0, 7.6)
ax.legend(loc="upper left", fontsize=9)
save(fig, SLUG, "fig1-cost-anatomy")

# ---------- Figure 2: Vals effort study ----------
fig, ax = plt.subplots(figsize=(9.0, 5.0))
models = list(dict.fromkeys(v["model"] for v in VALS)); xs = []
lab_off = {"Muse Spark 1.3": (-62, 12), "Gemini 4 Argon": (-118, 9), "GLM-5.3": (7, -12), "Opus 5.5": (7, 2), "GPT-6 Astra": (7, -4)}
for m in models:
    pts = srt([v for v in VALS if v["model"] == m]); X = [p["cost"] for p in pts]; Y = [p["acc"] for p in pts]; xs += X
    ax.errorbar(X, Y, yerr=[1.96 * p["se"] for p in pts], color=COL[m], lw=2, elinewidth=0.9, capsize=0, zorder=2)
    ax.scatter(X, Y, s=46, marker=MK[m], color=COL[m], edgecolor="white", linewidth=1.3, zorder=3)
    ax.annotate(ELAB[pts[0]["effort"]], (X[0], Y[0]), xytext=(0, -13), textcoords="offset points", ha="center", fontsize=7.5, color=INK2)
    ax.annotate(m, (X[-1], Y[-1]), xytext=lab_off.get(m, (7, -3)), textcoords="offset points", fontsize=8.8, color=NAVY, fontweight="600")
logx(ax, xs, 1.4, 2.6); ax.set_xlabel("Cost per test (USD, log scale)"); ax.set_ylabel("Vals Index accuracy (%)")
ax.text(0.01, 0.02, "Each line runs from the lowest setting tested (labelled) to the highest. Bars: 95% interval (±1.96 standard errors from Vals AI).",
        transform=ax.transAxes, fontsize=8, color=INK2)
save(fig, SLUG, "fig2-vals-effort")

# ---------- Figure 3: each effort step, cost multiple vs score change ----------
steps_v, steps_f = [], []
for m in models:
    pts = srt([v for v in VALS if v["model"] == m])
    for a, b in zip(pts, pts[1:]):
        d = b["acc"] - a["acc"]; z = d / math.hypot(a["se"], b["se"])
        steps_v.append((b["cost"] / a["cost"], d, abs(z) >= 1.96))
for m in LEAD:
    pts = srt([p for p in FC if p["model"] == m])
    for a, b in zip(pts, pts[1:]):
        d = b["score"] - a["score"]; z = d / math.hypot(se(a["score"], 132), se(b["score"], 132))
        steps_f.append((b["cost"] / a["cost"], d, abs(z) >= 1.96))
fig, axs = plt.subplots(1, 2, figsize=(9.2, 3.9), sharey=False, gridspec_kw=dict(wspace=0.25))
for ax, st, title in [(axs[0], steps_v, "(a) Vals AI effort study (14 steps)"), (axs[1], steps_f, "(b) FrontierCode 2.0, five models (18 steps)")]:
    ax.axhline(0, color="#9AA8BA", lw=1)
    for cr, d, sig in st:
        ax.scatter([cr], [d], s=52, marker="o", zorder=3, facecolor=BLUE if sig else "white", edgecolor=BLUE, linewidth=1.6)
    ax.set_xscale("log"); t = [0.8, 1, 1.5, 2, 3, 5]
    ax.xaxis.set_major_locator(FixedLocator(t)); ax.xaxis.set_major_formatter(FixedFormatter([f"{v:g}×" for v in t])); ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xlim(0.8, 5); ax.set_title(title, loc="left", fontsize=10.5); ax.set_xlabel("Cost multiple of the step")
axs[0].set_ylabel("Score change (points)"); axs[1].set_ylim(-5, 19)
axs[1].scatter([], [], s=52, facecolor=BLUE, edgecolor=BLUE, label="Distinguishable at 95%"); axs[1].scatter([], [], s=52, facecolor="white", edgecolor=BLUE, linewidth=1.6, label="Within noise")
axs[1].legend(loc="upper left", fontsize=8.8)
save(fig, SLUG, "fig3-step-returns")

# ---------- Figure 4: FrontierCode 2.0 ----------
fig, ax = plt.subplots(figsize=(9.0, 5.0)); xs = []
for m in LEAD:
    pts = srt([p for p in FC if p["model"] == m]); X = [p["cost"] for p in pts]; Y = [p["score"] for p in pts]; xs += X
    ax.errorbar(X, Y, yerr=[1.96 * se(y, 132) for y in Y], color=COL[m], lw=2, elinewidth=0.8, capsize=0, alpha=0.95, zorder=2)
    ax.scatter(X, Y, s=48, marker=MK[m], color=COL[m], edgecolor="white", linewidth=1.3, zorder=3)
    if m == "Claude Fable 5.2":
        for p in pts:
            ax.annotate(ELAB[p["effort"]], (p["cost"], p["score"]), xytext=(-8, 7), textcoords="offset points", ha="right", fontsize=8, color=INK2)
        cx = [p["file_cost"] for p in pts]; xs += cx
        ax.plot(cx, Y, color=COL[m], lw=1, ls=":", zorder=1); ax.scatter(cx, Y, s=26, marker="o", facecolor="white", edgecolor=COL[m], zorder=1)
        ax.annotate("Fable 5.2 as costed in\nCognition's file (×1.25)", (cx[-1], Y[-1]), xytext=(-30, -38), textcoords="offset points", fontsize=7.8, color=INK2, ha="center")
    if m == "Gemini 4 Carbon":
        gx = [v * 2 for v in X]; xs += gx
        ax.plot(gx, Y, color=COL[m], lw=1, ls=":", zorder=1); ax.scatter(gx, Y, s=26, marker="D", facecolor="white", edgecolor=COL[m], zorder=1)
        ax.annotate("Gemini 4 Carbon at the\n\\$4/\\$20 price from 1 Dec", (gx[0], Y[0]), xytext=(10, -26), textcoords="offset points", fontsize=7.8, color=INK2)
    ax.annotate(m.replace("Claude ", ""), (X[-1], Y[-1]), xytext={"Gemini 4 Carbon": (8, -14), "Claude Fable 5.2": (-4, -17)}.get(m, (8, -3)), textcoords="offset points", fontsize=8.8, color=NAVY, fontweight="600")
logx(ax, xs, 1.4, 2.0); ax.set_xlabel("Cost per task (USD, log scale)"); ax.set_ylabel("FrontierCode 2.0 score (%)")
ax.text(0.01, 0.02, "Bars: conservative 95% interval (task-level bound, n = 132). Solid points: list prices of 11 Nov 2026.", transform=ax.transAxes, fontsize=8, color=INK2)
save(fig, SLUG, "fig4-frontiercode")

# ---------- Figure 5: ARC-AGI-2 error rate ----------
fig, ax = plt.subplots(figsize=(9.0, 4.8)); xs = []
for m in LEAD:
    pts = srt([p for p in ARC if p["model"] == m]); X = [p["cost"] for p in pts]; E = [100 - p["score"] for p in pts]; xs += X
    ci = [1.96 * se(p["score"], 120) for p in pts]
    lo = [e - max(e - c, 1.6) for e, c in zip(E, ci)]
    ax.errorbar(X, E, yerr=[lo, ci], color=COL[m], lw=2, elinewidth=0.8, capsize=0, zorder=2)
    for p, e in zip(pts, E):
        ax.scatter([p["cost"]], [e], s=48, marker=MK[m], zorder=3, linewidth=1.5, facecolor="white" if p["lb"] else COL[m], edgecolor=COL[m] if p["lb"] else "white")
    ax.scatter([], [], s=48, marker=MK[m], color=COL[m], label=m)
ax.set_yscale("log"); yt = [2, 5, 10, 20, 50]
ax.yaxis.set_major_locator(FixedLocator(yt)); ax.yaxis.set_major_formatter(FixedFormatter([f"{v}%" for v in yt])); ax.yaxis.set_minor_locator(NullLocator())
ax.set_ylim(1.5, 65); ax.invert_yaxis(); ax.axhspan(1.5, 10, color="#EEF3F8", zorder=0)
ax.text(0.01, 0.96, "Scores of 90% and above: intervals overlap", transform=ax.transAxes, fontsize=8.5, color=INK2, va="top")
logx(ax, xs, 1.4, 2.4); ax.set_xlabel("Cost per task (USD, log scale)"); ax.set_ylabel("Error rate (100 − score, log scale)")
ax.text(0.99, 0.03, "Hollow marker: cost is a lower bound (unrecorded attempts excluded)", transform=ax.transAxes, fontsize=8, color=INK2, ha="right")
ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.08), fontsize=8.8)
save(fig, SLUG, "fig5-arc-ceiling")

# ---------- Figure 6: interval half-width vs number of tasks ----------
n = np.arange(20, 2001)
fig, ax = plt.subplots(figsize=(7.6, 3.9))
for p, col in [(0.5, BLUE), (0.9, ORANGE)]:
    ax.plot(n, 196 * np.sqrt(p * (1 - p) / n), color=col, label=f"True score {int(p * 100)}%")
for nn, lab in [(120, "ARC-AGI-2\n120 tasks"), (132, None), (500, "500 tasks")]:
    ax.axvline(nn, color="#B9C7D8", lw=1, ls="--")
    if lab: ax.text(nn * 1.04, 17.5, lab, fontsize=8.5, color=INK2, va="top")
ax.text(132 * 1.04, 12.6, "FrontierCode 2.0: 132", fontsize=8.5, color=INK2)
for nn in (132,):
    v = 196 * math.sqrt(0.25 / nn); ax.plot([nn], [v], "o", color=BLUE, ms=6); ax.annotate(f"±{v:.1f} pts", (nn, v), xytext=(8, 4), textcoords="offset points", fontsize=8.5, color=BLUE)
v = 196 * math.sqrt(0.09 / 120); ax.plot([120], [v], "o", color=ORANGE, ms=6); ax.annotate(f"±{v:.1f} pts", (120, v), xytext=(-48, -14), textcoords="offset points", fontsize=8.5, color=ORANGE)
ax.set_xscale("log"); t = [20, 50, 100, 200, 500, 1000, 2000]
ax.xaxis.set_major_locator(FixedLocator(t)); ax.xaxis.set_major_formatter(FixedFormatter([str(v) for v in t])); ax.xaxis.set_minor_locator(NullLocator())
ax.set_xlabel("Number of independent tasks (log scale)"); ax.set_ylabel("95% interval half-width (points)"); ax.set_ylim(0, 18)
ax.legend(loc="center right")
save(fig, SLUG, "fig6-interval-width")

# ---------- Figure 7: list price vs cost per task (Artificial Analysis) ----------
AA = [x for x in IDX if x["source"] == "Artificial Analysis"]
price = {x["model"]: float(x["cost_value_usd"]) for x in AA if x["cost_metric"].startswith("Blended price") and x["cost_value_usd"]}
cpt = {}
for x in AA:
    if x["cost_metric"].startswith("Cost per Intelligence Index task") and x["model"] in price and x["cost_value_usd"]:
        cpt.setdefault(x["model"], []).append((float(x["cost_value_usd"]), float(x["quality_value"])))
fig, ax = plt.subplots(figsize=(8.8, 4.8))
for m, vals in cpt.items():
    c = [v[0] for v in vals]; p = price[m] * {"Gemini 4 Argon": 0.93, "Gemini 4 Carbon": 1.07}.get(m, 1)
    if len(c) > 1: ax.plot([p, p], [min(c), max(c)], color="#9CC0DA", lw=4, solid_capstyle="round", zorder=1)
    ax.scatter([p] * len(c), c, s=22, color=BLUE, zorder=2)
for m, off in [("Gemini 4 Carbon", (8, -10)), ("Gemini 4 Argon", (-50, 9)), ("Claude Fable 5.2", (8, 0)), ("GPT-6 Astra", (8, 0)), ("Claude Haiku 5.5", (8, 0)), ("DeepSeek V4.1 Flash", (8, -4))]:
    if m in cpt:
        ax.annotate(m, (price[m] * {"Gemini 4 Argon": 0.93, "Gemini 4 Carbon": 1.07}.get(m, 1), max(v[0] for v in cpt[m])), xytext=off, textcoords="offset points", fontsize=8.3, color=NAVY)
ax.set_xscale("log"); ax.set_yscale("log")
for a, t, fmt in [(ax.xaxis, [0.1, 0.2, 0.5, 1, 2, 5, 10], "${:g}"), (ax.yaxis, [0.01, 0.1, 1, 10, 100], "${:g}")]:
    a.set_major_locator(FixedLocator(t)); a.set_major_formatter(FixedFormatter([fmt.format(v) for v in t])); a.set_minor_locator(NullLocator())
ax.set_xlabel("Blended list price, USD per million tokens (7:2:1 cache hit : input : output; log)")
ax.set_ylabel("Cost per Index task (USD, log)")
ax.text(0.99, 0.03, "Each column is one model; dots are its reasoning-effort settings.\nGemini 4 Argon and Carbon share a price and are offset slightly.", transform=ax.transAxes, fontsize=8.5, color=INK2, va="bottom", ha="right")
save(fig, SLUG, "fig7-price-vs-task-cost")

# ---------- Figure 8: decision procedure ----------
fig, ax = plt.subplots(figsize=(9.0, 4.4)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 56)
def box(x, y, w, h, t, fc=LIGHT, ec="#9CC0DA", tc=NAVY, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.5", fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=8.8, color=tc, fontweight="600" if bold else "normal", wrap=True)
def arr(x1, y1, x2, y2, t=None, tx=0, ty=0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12, color=NAVY, lw=1.2))
    if t: ax.text((x1 + x2) / 2 + tx, (y1 + y2) / 2 + ty, t, fontsize=8.3, color=INK2, ha="center")
box(1, 33, 19, 13, "1. Build a test set\nof 100–300 of your\nown tasks", bold=True)
box(26, 33, 19, 13, "2. Run 2–3 candidate\nmodels at a low\neffort setting", bold=True)
box(51, 33, 19, 13, "3. Step one setting\nup and re-run the\nsame tasks", bold=True)
box(76, 33, 22, 13, "4. Is the gain larger\nthan the 95% interval\nand worth the cost?", fc="#FFF4EC", ec="#E9B48C", bold=True)
box(76, 3, 22, 13, "Stop: use the previous\nsetting; budget from\nmeasured tokens", fc="#EEF6E4", ec="#B7D88C", tc=GREEN_D, bold=True)
box(40, 3, 26, 13, "Record cost per task and\ncost per correct answer,\nat a dated price sheet", fc="white", ec="#B9C7D8")
arr(20.5, 39.5, 25.5, 39.5); arr(45.5, 39.5, 50.5, 39.5); arr(70.5, 39.5, 75.5, 39.5)
arr(87, 32.5, 87, 16.5, "No", 3.5, 0)
ax.add_patch(FancyArrowPatch((80, 46.4), (60.5, 46.4), connectionstyle="arc3,rad=0.35", arrowstyle="-|>", mutation_scale=12, color=NAVY, lw=1.2))
ax.text(70, 53.2, "Yes: keep it and test the next setting", fontsize=8.3, color=INK2, ha="center")
arr(75.5, 9.5, 66.5, 9.5)
save(fig, SLUG, "fig8-procedure")
print("figures written")
