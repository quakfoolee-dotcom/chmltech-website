"""Figures for the AI-agent calculation benchmark paper (Chmltech Online Journal, Vol. 106 draft). V1.
Data: data/aibench/grades*.json written by grade.py / grade2.py and the set-3 rubric scores.  Usage: python3 aibench_figs.py"""
import json, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.colors import ListedColormap
from style import *
import style

HERE = os.path.dirname(os.path.abspath(__file__))
style.OUT = os.path.join(HERE, "..", "figures")
SLUG = "can-an-ai-agent-do-process-engineering-calculations-a-benchmark-of-three-models-with-and-without-code"
INK2 = "#4A5568"
plt.rcParams["axes.axisbelow"] = True; plt.rcParams["text.parse_math"] = False
D = os.path.join(HERE, "data", "aibench")
G1 = json.load(open(os.path.join(D, "grades.json"))); G2 = json.load(open(os.path.join(D, "grades2.json"))); G3 = json.load(open(os.path.join(D, "grades3.json")))
MODELS = [("haiku", "Small model"), ("sonnet", "Medium model"), ("opus", "Large model")]
CONDS = [("reasoning", "Reasoning only"), ("code", "With Python")]

REF1 = json.load(open(os.path.join(D, "reference.json"))); REF2 = json.load(open(os.path.join(D, "reference2.json")))
def band(s_, r):
    a = (REF1 if s_ == "1" else REF2)[str(r["task"])]["answers"][r["key"]]; return a["value"], a["tol"]

# ---------- Figure 1: answers correct, sets 1 and 2 ----------
fig, ax = plt.subplots(figsize=(8.6, 3.9))
x = np.arange(3); w = 0.2
cols = {("1", "reasoning"): LIGHT, ("1", "code"): GREY, ("2", "reasoning"): BRIGHT, ("2", "code"): NAVY}
k = 0
for s_, G in (("1", G1), ("2", G2)):
    for c, clab in CONDS:
        vals = [G[f"{m}_{c}"]["keys_correct"] / G[f"{m}_{c}"]["n_keys"] for m, _ in MODELS]
        n = G[f"{MODELS[0][0]}_{c}"]["n_keys"]
        ax.bar(x + (k - 1.5) * w, vals, w * 0.92, color=cols[(s_, c)], label=f"Set {s_} ({n} answers), {clab[0].lower() + clab[1:]}")
        for xi, v, (m, _) in zip(x + (k - 1.5) * w, vals, MODELS):
            G_ = G[f"{m}_{c}"]; ax.text(xi, 0.04, f"{G_['keys_correct']}/{G_['n_keys']}", ha="center", fontsize=7.8, color=NAVY if cols[(s_, c)] in (LIGHT,) else "white", rotation=90, va="bottom")
        k += 1
ax.set_xticks(x); ax.set_xticklabels([l for _, l in MODELS]); ax.set_ylim(0, 1.05)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.set_ylabel("Answers within tolerance")
ax.legend(loc="upper center", ncol=2, fontsize=8.4, bbox_to_anchor=(0.5, -0.12))
save(fig, SLUG, "fig1-answers-correct")

# ---------- Figure 2: error of every numeric answer relative to its tolerance ----------
fig, ax = plt.subplots(figsize=(8.6, 4.4))
labels = []
for i, (m, mlab) in enumerate(MODELS):
    for j, (c, clab) in enumerate(CONDS):
        pos = i * 2 + j; labels.append(f"{mlab}\n{clab[0].lower() + clab[1:]}")
        for s_, G, mk in (("1", G1, "o"), ("2", G2, "s")):
            pts = []
            for r in G[f"{m}_{c}"]["rows"]:
                ref, tol = band(s_, r)
                if tol == 0 or r["got"] in (None, "None"): continue
                got = float(r["got"]); err = abs(got - ref) if tol < 0 else abs(got - ref) / abs(ref)
                pts.append((max(err / abs(tol), 1e-4), bool(r["ok"])))
            e = np.array([p[0] for p in pts]); ok = np.array([p[1] for p in pts])
            jit = np.random.default_rng(pos * 10 + int(s_)).uniform(-0.25, 0.25, len(e))
            ax.scatter(pos + jit[ok], e[ok], s=14, marker=mk, color=BLUE if s_ == "1" else GREEN_D, alpha=0.7, lw=0)
            ax.scatter(pos + jit[~ok], e[~ok], s=46, marker="X", color=ORANGE, zorder=4)
ax.set_yscale("log"); ax.set_ylim(5e-5, 20)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: {1e-4: "0.0001", 1e-3: "0.001", 1e-2: "0.01", 1e-1: "0.1", 1.0: "1", 10.0: "10"}.get(round(v, 6), "")))
ax.axhline(1.0, color=ORANGE, lw=1.3, ls=(0, (4, 3)))
ax.text(5.45, 1.15, "Tolerance", fontsize=8.4, color=ORANGE, ha="right", va="bottom")
ax.set_xticks(range(6)); ax.set_xticklabels(labels, fontsize=8.4)
ax.set_ylabel("Error / tolerance of that answer (log scale)")
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([], [], marker="o", ls="", color=BLUE, label="Set 1 answer"), Line2D([], [], marker="s", ls="", color=GREEN_D, label="Set 2 answer"),
                   Line2D([], [], marker="X", ls="", color=ORANGE, ms=8, label="Outside tolerance")], loc="upper center", fontsize=8.4, ncol=3, bbox_to_anchor=(0.5, -0.17))
save(fig, SLUG, "fig2-error-of-every-answer")

# ---------- Figure 3: rubric grid for the open design tasks ----------
items = {"41": ["Clean area\nat normal case", "Cold or max\ndesign case", "Fouling\nallowance", "Stall at\nlow load", "Missing data\nand levers"],
         "42": ["40 °C vapour\npressure", "Low-low\nlevel", "Dirty\nstrainer", "NPSHa\n11.7 m", "Margin rule,\nrunout flow"],
         "43": ["Rejects blocked\noutlet only", "Runaway,\ncalorimetry", "Fire\ncase", "Two-phase\nventing", "Further case\nor CSO valve"],
         "44": ["Cv\n10.6", "Max and\nmin flows", "Opening at\nmax and min", "Choked,\ncavitation", "Body size,\ncharacteristic"]}
titles = {"41": "Task 41: preheater", "42": "Task 42: NPSH", "43": "Task 43: relief basis", "44": "Task 44: control valve"}
fig, axes = plt.subplots(4, 1, figsize=(8.6, 6.6))
cmap = ListedColormap(["#F6D2BE", "#CFE6B5"])
for ax, t in zip(axes, ("41", "42", "43", "44")):
    M = np.array([G3[m][t] for m, _ in MODELS])
    ax.imshow(M, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    for i in range(3):
        for j in range(5): ax.text(j, i, "✓" if M[i, j] else "✗", ha="center", va="center", fontsize=10, color=GREEN_D if M[i, j] else ORANGE)
    ax.set_yticks(range(3)); ax.set_yticklabels([l for _, l in MODELS], fontsize=8.4)
    ax.set_xticks(range(5)); ax.set_xticklabels(items[t], fontsize=7.6); ax.xaxis.tick_top()
    ax.set_ylabel(titles[t], rotation=0, ha="right", va="center", fontsize=8.8, labelpad=8)
    ax.grid(False)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_xticks(np.arange(-.5, 5, 1), minor=True); ax.set_yticks(np.arange(-.5, 3, 1), minor=True)
    ax.grid(which="minor", color="white", lw=2); ax.tick_params(which="minor", length=0); ax.tick_params(length=0)
fig.tight_layout(h_pad=0.6)
save(fig, SLUG, "fig3-design-review-rubric")
print("ok")
