"""Figures for Vol. 106, Issues 16-18: industrial LLMs for smart factory assessment and optimization.
Data: results.json of each model in content/journal/ilm/models/ (assess, oee, sched).
Usage: cd content/journal/figure-scripts && python3 -I -c "import sys; sys.path.insert(0,'.'); exec(open('ilm_figs.py').read())" [16|17|18]
"""
import json, os, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from style import *
import style

HERE = os.path.dirname(os.path.abspath("ilm_figs.py"))
M = os.path.join(HERE, "..", "ilm", "models")
style.OUT = os.path.join(HERE, "..", "figures")
INK2 = "#4A5568"
plt.rcParams["axes.axisbelow"] = True
P1 = "can-an-llm-assess-a-factory-validating-ai-scored-smart-factory-maturity-against-human-assessors"
P2 = "the-llm-should-not-do-the-arithmetic-a-tool-grounded-architecture-for-oee-and-kpi-analysis"
P3 = "from-plain-english-to-optimal-schedule-verifying-llm-written-scheduling-models"
WHICH = sys.argv[1:] or ["16", "17", "18"]


def box(ax, x, y, w, h, text, fc=LIGHT, ec="#9AA8BA", tc=NAVY, fs=9.5, bold=False, r=0.012):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=1.1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc, fontweight="600" if bold else "normal",
            linespacing=1.3)


def arrow(ax, p, q, color=NAVY, ls="-", lw=1.4):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12, color=color, lw=lw, ls=ls, shrinkA=0, shrinkB=0))


# ======================================================================= Issue 17: OEE
if "17" in WHICH:
    R = json.load(open(os.path.join(M, "oee", "results.json")))
    ref = 100 * R["REF"]["plant"]["OEE"]
    order = ["E3b", "E6", "E7", "REF", "E1", "E2", "E5", "E4", "E3"]
    lab = {"REF": "Reference (ISO 22400 elements, pooled)", "E1": "E1  Average of shift OEE values", "E2": "E2  Product of averaged A, P and Q",
           "E3": "E3  One ideal rate, fastest SKU", "E3b": "E3b One ideal rate, slowest SKU", "E4": "E4  Planned downtime counted as loss",
           "E5": "E5  Overlapping stops summed", "E6": "E6  Rework counted as good", "E7": "E7  Unweighted mean of line OEEs"}
    fig, ax = plt.subplots(figsize=(8.8, 4.4))
    vals = [100 * R[e]["plant"]["OEE"] for e in order]
    cols = [NAVY if e == "REF" else (ORANGE if abs(v - ref) >= 2 else GREY) for e, v in zip(order, vals)]
    y = np.arange(len(order))[::-1]
    ax.barh(y, vals, color=cols, height=0.62)
    ax.axvline(ref, color=NAVY, lw=1.2, ls=(0, (4, 3)))
    for yi, v, e in zip(y, vals, order):
        d = v - ref
        t = f"{v:.1f}%" + ("" if e == "REF" else f"  ({d:+.1f} pts)")
        ax.text(max(v, ref) + 1.5, yi, t, va="center", fontsize=9.5, color=NAVY, fontweight="600" if abs(d) >= 2 or e == "REF" else "normal")
    ax.set_yticks(y); ax.set_yticklabels([lab[e] for e in order])
    ax.set_xlim(0, 175); ax.set_xticks([0, 25, 50, 75, 100, 125, 150])
    ax.set_xlabel("Plant OEE over four weeks (%)")
    ax.grid(axis="y", visible=False)
    save(fig, P2, "fig1-oee-by-error")

    # Figure 2: loss hours by line, reference vs E5 vs E3
    def loss(e):
        out = {}
        for l, v in R[e]["lines"].items():
            out[l] = v
        return out
    # recompute loss split from factors stored in results: availability = (1-A)*PBT etc. need PBT per line
    import importlib.util
    sp = importlib.util.spec_from_file_location("oeeref", os.path.join(M, "oee", "oee_reference.py"))
    O = importlib.util.module_from_spec(sp); sp.loader.exec_module(O)
    sh, st = O.build()
    fig, axs = plt.subplots(1, 3, figsize=(9.2, 3.9), sharey=True)
    for ax, (e, title) in zip(axs, [("REF", "Reference"), ("E5", "E5: overlapping stops summed"), ("E3", "E3: one rate (fastest SKU)")]):
        el = O.elements(sh, st, None if e == "REF" else e)
        L = {l: O.loss_hours([x for x in el if x["line"] == l]) for l in O.LINES}
        x = np.arange(3); w = 0.26
        for i, (k, c) in enumerate([("availability", BLUE), ("performance", ORANGE), ("quality", GREEN_D)]):
            ax.bar(x + (i - 1) * w, [L[l][k] for l in O.LINES], width=w, color=c, label=k.capitalize() + " loss")
        ax.set_xticks(x); ax.set_xticklabels(list(O.LINES)); ax.set_title(title, fontsize=10.5)
        ax.grid(axis="x", visible=False)
        for xi, l in zip(x, O.LINES):
            big = max(L[l], key=L[l].get); i = ["availability", "performance", "quality"].index(big)
            ax.text(xi + (i - 1) * w, L[l][big] + 3, "▲", ha="center", fontsize=8, color=NAVY)
    axs[0].set_ylabel("Hours lost over four weeks")
    axs[0].set_ylim(0, 160)
    axs[0].plot([], [], ls="none", marker="^", color=NAVY, ms=6, label="Largest loss on the line")
    axs[0].legend(loc="upper left", fontsize=9)
    save(fig, P2, "fig2-loss-allocation")

    # Figure 3: architecture
    fig, ax = plt.subplots(figsize=(9.2, 4.7)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    box(ax, 0.00, 0.35, 0.13, 0.30, "Question\n\"Which line\nlost most last\nmonth, and\non what?\"", fc="white", fs=9)
    box(ax, 0.17, 0.38, 0.14, 0.24, "LLM planner\nchooses tool,\nfilters and\ndefinition", fc=LIGHT, fs=9)
    box(ax, 0.36, 0.70, 0.27, 0.20, "KPI definitions as code\nISO 22400 elements,\nversioned (oee-def v3)", fc="#EAF3E0", ec=GREEN_D, fs=9)
    box(ax, 0.36, 0.40, 0.27, 0.20, "KPI tools\ncompute_oee · loss_tree\nmerge_stops · compare", fc="#EAF3E0", ec=GREEN_D, fs=9)
    box(ax, 0.36, 0.10, 0.27, 0.20, "Plant data\nMES shifts, stop log,\ncounts, SKU rates", fc="white", fs=9)
    box(ax, 0.68, 0.38, 0.14, 0.24, "Result with\nprovenance:\nrows, filter,\ndefinition id", fc="white", fs=9)
    box(ax, 0.86, 0.38, 0.14, 0.24, "LLM writes\nthe answer;\nnumber-echo\ncheck", fc=LIGHT, fs=9)
    arrow(ax, (0.13, 0.50), (0.17, 0.50))
    arrow(ax, (0.31, 0.50), (0.36, 0.50))
    arrow(ax, (0.495, 0.70), (0.495, 0.60))
    arrow(ax, (0.495, 0.30), (0.495, 0.40))
    arrow(ax, (0.63, 0.50), (0.68, 0.50))
    arrow(ax, (0.82, 0.50), (0.86, 0.50))
    ax.text(0.86, 0.27, "No number in the answer\nthat a tool did not return", fontsize=9, color=ORANGE, ha="center", fontweight="600")
    ax.text(0.495, 0.955, "Deterministic, versioned, regression-tested", fontsize=9, color=GREEN_D, ha="center", fontweight="600")
    ax.add_patch(FancyBboxPatch((0.345, 0.06), 0.30, 0.87, boxstyle="round,pad=0,rounding_size=0.015", fc="none", ec=GREEN_D, lw=1.0, ls=(0, (4, 3))))
    save(fig, P2, "fig3-architecture")

# ======================================================================= Issue 16: assessment
if "16" in WHICH:
    R = json.load(open(os.path.join(M, "assess", "results.json")))
    fig, ax = plt.subplots(figsize=(8.6, 4.3))
    ns = [10, 20, 30, 50, 80]
    style_ = {"S1": (BLUE, "-", "o"), "S5": (GREEN_D, "-", "s"), "S2": (ORANGE, "--", "o"), "S3": (GREY, "--", "^"), "S4": (NAVY, ":", "D")}
    lbl = {"S1": "S1 LLM as consistent as a human", "S2": "S2 LLM noisier than a human", "S3": "S3 LLM lenient by half a band",
           "S4": "S4 evidence gaps, LLM guesses", "S5": "S5 evidence gaps, LLM abstains"}
    for k in ["S1", "S5", "S2", "S3", "S4"]:
        c, ls, mk = style_[k]
        ax.plot(ns, [100 * R["power"][k][str(n)] for n in ns], color=c, ls=ls, marker=mk, ms=4.5, label=lbl[k])
    ax.axhline(80, color="#9AA8BA", lw=1.1, ls=(0, (5, 4)))
    ax.text(81, 82, "80% power", fontsize=9, color=INK2, ha="right")
    ax.set_xlabel("Plants in the validation study"); ax.set_ylabel("Studies that pass non-inferiority (%)")
    ax.set_xticks(ns); ax.set_ylim(-3, 105); ax.set_xlim(7, 83)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=9)
    save(fig, P1, "fig2-power")

    fig, ax = plt.subplots(figsize=(9.2, 4.6)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    steps = [("1  Evidence pack", "Documents, data\nextracts, interviews,\nphotos; each tagged\nby dimension"),
             ("2  Retrieve per\ndimension", "Only the evidence\nfor one dimension\nat a time goes\nto the model"),
             ("3  Score against\nthe rubric", "Band 0–5, rubric\nsentence, quoted\nevidence, or\n\"insufficient\nevidence\""),
             ("4  Check", "Citations resolve;\nno band without\nevidence; repeat runs\nagree"),
             ("5  Assessor review", "Human accepts or\nchanges each band;\nreasons logged for\nthe next calibration")]
    x0, w, gap = 0.01, 0.178, 0.0245
    for i, (t, d) in enumerate(steps):
        x = x0 + i * (w + gap)
        fc = "#EAF3E0" if i == 4 else LIGHT
        box(ax, x, 0.60, w, 0.20, t, fc=fc, bold=True, fs=10)
        box(ax, x, 0.20, w, 0.33, d, fc="white", fs=9)
        if i < 4: arrow(ax, (x + w, 0.70), (x + w + gap, 0.70))
    ax.text(0.5, 0.92, "Each band carries its evidence; gaps are reported, never filled", ha="center", fontsize=10, color=NAVY, fontweight="600")
    ax.text(0.5, 0.08, "Agreement with human assessors (weighted κ, bias, coverage) is measured on step 3 before step 5 is relaxed",
            ha="center", fontsize=9, color=INK2)
    save(fig, P1, "fig1-pipeline")

    # Figure 3: what each statistic sees
    B = R["big"]
    keys = ["S1", "S2", "S3", "S4", "S5"]
    fig, axs = plt.subplots(1, 3, figsize=(9.2, 3.7))
    short = {"S1": "S1 equal", "S2": "S2 noisy", "S3": "S3 lenient", "S4": "S4 guesses", "S5": "S5 abstains"}
    for ax, (m, title, f, ref) in zip(axs, [("k_lh", "Weighted κ with assessor", lambda v: v, B["S1"]["k_hh"]),
                                         ("bias", "Mean band difference", lambda v: v, 0.0),
                                         ("coverage", "Dimensions scored (%)", lambda v: 100 * v, 100)]):
        v = [f(B[k][m]) for k in keys]
        ax.barh(np.arange(5)[::-1], v, color=[BLUE, ORANGE, GREY, NAVY, GREEN_D], height=0.6)
        ax.set_yticks(np.arange(5)[::-1]); ax.set_yticklabels([short[k] for k in keys] if ax is axs[0] else [])
        ax.set_title(title, fontsize=10.5); ax.grid(axis="y", visible=False)
        ax.axvline(ref, color=NAVY, lw=1.1, ls=(0, (4, 3)))
        for yi, vi in zip(np.arange(5)[::-1], v):
            off = {"k_lh": 0.008, "bias": 0.015, "coverage": 2}[m]
            ax.text(max(vi, ref) + off, yi, f"{abs(vi) if abs(vi) < 0.005 else vi:.2f}" if m != "coverage" else f"{vi:.0f}%", va="center", fontsize=9, color=NAVY)
    axs[0].set_xlim(0.5, 0.86); axs[1].set_xlim(-0.05, 0.65); axs[2].set_xlim(0, 125)
    save(fig, P1, "fig3-statistics")

# ======================================================================= Issue 18: scheduling
if "18" in WHICH:
    R = json.load(open(os.path.join(M, "sched", "summary.json")))
    # Figure 2: total tardiness over all snapshots, after repair
    F = [f for f in R["order"] if f != "F8"]
    fig, ax = plt.subplots(figsize=(8.8, 4.4))
    y = np.arange(len(F))[::-1]
    v = [R["total"][f] for f in F]
    ax.barh(y, v, color=[NAVY if f == "F0" else ORANGE for f in F], height=0.6)
    br = R["best_rule_total"]
    ax.axvline(br, color=GREEN_D, lw=1.4, ls=(0, (4, 3)))
    ax.text(br + 60, len(F) - 0.05, f"Best dispatching rule (MDD): {br:,.0f} h", color=GREEN_D, fontsize=9.5, va="center")
    for yi, vi in zip(y, v):
        ax.text(max(vi, br) + 60, yi, f"{vi:,.0f} h", va="center", fontsize=9.5, color=NAVY)
    ax.set_yticks(y); ax.set_yticklabels([R["short"][f] for f in F])
    ax.set_xlim(0, 8600); ax.set_ylim(-0.6, len(F) + 0.3)
    ax.set_xlabel("Total tardiness over 30 weekly snapshots, after repair (hours)")
    ax.grid(axis="y", visible=False)
    save(fig, P3, "fig2-tardiness")

    # Figure 3: detection matrix
    G = ["G1", "G2", "G3", "G4"]
    gl = {"G1": "G1 Solver\nstatus", "G2": "G2 Feasibility\ncheck", "G3": "G3 Objective\nrecompute", "G4": "G4 Beats best\nrule"}
    FF = [f for f in R["order"] if f != "F0"]
    mat = np.array([[R["detect"][f][g] for g in G] for f in FF])
    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    ax.imshow(mat, cmap=matplotlib.colors.LinearSegmentedColormap.from_list("d", ["#FFFFFF", "#F6D6C2", ORANGE]), vmin=0, vmax=100, aspect="auto")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, f"{mat[i, j]:.0f}%", ha="center", va="center", fontsize=10, color=NAVY, fontweight="600" if mat[i, j] >= 50 else "normal")
        anyc = R["any"][FF[i]]
        ax.text(len(G) - 0.35, i, f"{anyc:.0f}%", ha="left", va="center", fontsize=10, color=NAVY, fontweight="600")
    ax.text(len(G) - 0.35, -0.85, "Any gate", ha="left", va="center", fontsize=9.5, color=NAVY, fontweight="600")
    ax.set_xticks(range(len(G))); ax.set_xticklabels([gl[g] for g in G])
    ax.set_yticks(range(len(FF))); ax.set_yticklabels([R["short"][f] for f in FF])
    ax.xaxis.tick_top(); ax.grid(False); ax.tick_params(length=0)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xlim(-0.5, len(G) + 0.25)
    save(fig, P3, "fig3-detection")

    # Figure 1: pipeline
    fig, ax = plt.subplots(figsize=(9.2, 4.8)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    row = [("Planner's request\nin plain English\n+ ERP extract", "white"), ("LLM writes\nthe model\n(CP-SAT or MILP)", LIGHT),
           ("Solver", LIGHT), ("Proposed\nschedule", "white")]
    xs = [0.02, 0.27, 0.52, 0.77]
    for (t, fc), x in zip(row, xs): box(ax, x, 0.66, 0.20, 0.20, t, fc=fc, fs=9.5)
    for x in xs[:-1]: arrow(ax, (x + 0.20, 0.76), (x + 0.25, 0.76))
    gates = [("G1", "Solver status"), ("G2", "Feasibility check\non the true data"), ("G3", "Objective\nrecomputed"), ("G4", "Beats the best\ndispatching rule")]
    for i, (g, t) in enumerate(gates):
        box(ax, xs[i], 0.16, 0.20, 0.22, f"{g}\n{t}", fc="#EAF3E0", ec=GREEN_D, fs=9.5)
        if i < 3: arrow(ax, (xs[i] + 0.20, 0.27), (xs[i] + 0.25, 0.27))
    ax.plot([0.87, 0.87, 0.12], [0.66, 0.53, 0.53], color=NAVY, lw=1.4)
    arrow(ax, (0.12, 0.53), (0.12, 0.38))
    ax.add_patch(FancyBboxPatch((0.005, 0.10), 0.98, 0.34, boxstyle="round,pad=0,rounding_size=0.015", fc="none", ec=GREEN_D, lw=1.0, ls=(0, (4, 3))))
    ax.text(0.5, 0.465, "Verification gates: independent of the LLM, written and tested once by the plant", ha="center", fontsize=9, color=GREEN_D, fontweight="600")
    ax.text(0.5, 0.04, "Pass all four: release the schedule.  Any gate fails: return the model to the LLM with the failing check, or run the best rule.",
            ha="center", fontsize=9, color=ORANGE)
    save(fig, P3, "fig1-pipeline")
