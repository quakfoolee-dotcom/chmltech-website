"""Figures for Vol. 105(7)-(11), the November 13 batch of journal papers (V4.67).

Run from this folder:  python3 -I -c "import sys; sys.path.insert(0,'.'); exec(open('agentic2.py').read())"
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Rectangle
from style import *

S7 = "levels-of-autonomy-and-human-in-the-loop-design-for-ai-agents"
S8 = "the-economics-of-agentic-ai-cost-per-task-total-cost-and-payback"
S9 = "agentic-ai-in-manufacturing-operations-use-cases-architecture-and-safety-boundaries"
S10 = "evaluating-ai-agents-why-benchmarks-mislead-and-how-to-build-your-own-evaluation"
S11 = "the-eu-ai-act-for-canadian-businesses-scope-obligations-and-a-compliance-path"
INK = "#4A5568"; PALE = "#EEF3F9"; SKY = "#CFE6F3"; GREENF = "#E4F1D3"; ORANGEF = "#FBE6D8"; REDF = "#F8DEDB"; RED = "#C0392B"


def box(ax, x0, y0, w, h, txt, fill=LIGHT, tc=NAVY, fs=9, bold=False, ec="#9AB0C8", ls="-", lw=1):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.25,rounding_size=1.0", fc=fill, ec=ec, lw=lw, ls=ls))
    if txt:
        ax.text(x0 + w / 2, y0 + h / 2, txt, ha="center", va="center", fontsize=fs, color=tc, fontweight="600" if bold else "normal", linespacing=1.25)


def arr(ax, p, q, col=NAVY, lw=1.5, style="-|>", ms=11):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=col, lw=lw, shrinkA=0, shrinkB=0))


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off"); return fig, ax


def run(only=None):
    for name, f in list(globals().items()):
        if name.startswith("f_") and (only is None or name.startswith(f"f_{only}_")):
            f()


# =============================================================== 105(7) Figure 1 — oversight regions
def f_7_regions():
    cr, dh, da = 1.33, 0.9, 0.3
    p = np.logspace(-3, -1, 200)
    C = cr / (p * (dh - da))
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.fill_between(p, C, 1e4, color=SKY, alpha=.7, lw=0)
    ax.fill_between(p, 10, C, color=GREENF, alpha=.9, lw=0)
    ax.plot(p, C, color=NAVY, lw=2.2)
    ax.axvspan(0.04, 0.1, color=REDF, alpha=.8, lw=0)
    ax.set_xlim(1e-3, 1e-1); ax.set_ylim(10, 1e4)
    ax.set_xticks([1e-3, 3e-3, 1e-2, 3e-2, 1e-1]); ax.set_xticklabels(["0.1%", "0.3%", "1%", "3%", "10%"])
    ax.set_yticks([10, 100, 1000, 10000]); ax.set_yticklabels(["$10", "$100", "$1,000", "$10,000"])
    ax.set_xlabel("Agent error rate, p"); ax.set_ylabel("Cost of an uncaught error, C")
    ax.text(0.0025, 3000, "Approval pays", fontsize=11, color=NAVY, fontweight="600")
    ax.text(0.0016, 22, "Sample and monitor", fontsize=11, color=GREEN_D, fontweight="600")
    ax.text(0.063, 2500, "Approval queue\nexceeds capacity:\nfix the agent first", fontsize=9, color=RED, ha="center", fontweight="600")
    ax.annotate("Break-even, Eq. (1)", xy=(0.006, cr / (0.006 * 0.6)), xytext=(0.0105, 1300), fontsize=9, color=NAVY,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=1))
    ax.plot([0.02], [300], "o", color=ORANGE, ms=8, zorder=5)
    ax.annotate("Refund example:\n2% errors, $300", xy=(0.02, 300), xytext=(0.026, 900), fontsize=9, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1))
    ax.grid(True, which="major")
    save(fig, S7, "fig1-oversight-regions")


# =============================================================== 105(7) Figure 2 — rule of three
def f_7_rule3():
    n = np.logspace(1, 3, 200)
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.plot(n, 3 / n * 100, color=BLUE)
    for k in (30, 100, 300, 1000):
        ax.plot([k], [300 / k], "o", color=NAVY, ms=7, zorder=5)
        ax.annotate(f"{k} trials → {300 / k:.1f}%".replace(".0%", "%"), xy=(k, 300 / k), xytext=(8, 6), textcoords="offset points", fontsize=9.5, color=NAVY)
    ax.set_xlim(10, 1000); ax.set_ylim(0.2, 35)
    ax.set_xticks([10, 30, 100, 300, 1000]); ax.set_xticklabels(["10", "30", "100", "300", "1,000"])
    ax.set_yticks([0.3, 1, 3, 10, 30]); ax.set_yticklabels(["0.3%", "1%", "3%", "10%", "30%"])
    ax.set_xlabel("Consecutive error-free trials, n"); ax.set_ylabel("95% upper bound on error rate")
    save(fig, S7, "fig2-rule-of-three")


# =============================================================== 105(7) Figure 3 — promotion path
def f_7_promotion():
    fig, ax = canvas(9.0, 4.8)
    steps = [("Shadow mode", "agent drafts,\nperson does the work"), ("Approve", "agent acts after\napproval"),
             ("Act and sample", "agent acts;\nsample reviewed"), ("Act and monitor", "agent acts;\nmetrics watched")]
    fills = [PALE, SKY, GREENF, "#D6EBC0"]
    for i, (t, sub) in enumerate(steps):
        x, y = 4 + i * 23.5, 12 + i * 17
        box(ax, x, y, 19, 16, "", fill=fills[i], ec=BLUE if i else "#9AB0C8", lw=1.3)
        ax.text(x + 9.5, y + 11.2, t, ha="center", va="center", fontsize=9.8, color=NAVY, fontweight="600")
        ax.text(x + 9.5, y + 5, sub, ha="center", va="center", fontsize=8.4, color=INK, linespacing=1.15)
        if i < 3:
            arr(ax, (x + 19.6, y + 16.3), (x + 23.3, y + 19.5), col=GREEN_D, lw=1.8)
            ax.text(x + 20.5, y + 21.5, f"Gate {i + 1}", ha="center", fontsize=8.6, color=GREEN_D, fontweight="600")
    ax.text(2, 96, "Gates", fontsize=9.5, color=GREEN_D, fontweight="600", va="top")
    for j, g in enumerate(["1  error-free trials ≥ 3 ÷ target error rate, Eq. (3)", "2  every rejection explained; error rate on target",
                           "3  sampled error rate on target for a set period"]):
        ax.text(2, 89 - j * 6.5, g, fontsize=8.6, color=NAVY, va="top")
    ax.plot([96, 99, 99, 13.5, 13.5], [69, 69, 7, 7, 9], color=RED, lw=1.6)
    arr(ax, (13.5, 8.5), (13.5, 11.4), col=RED, lw=1.6)
    ax.text(56, 1.2, "Demotion: material error · untested input · model, tool or instruction change · process change",
            ha="center", fontsize=8.6, color=RED, fontweight="600")
    save(fig, S7, "fig3-promotion-path")



# =============================================================== 105(8) figures
def _p8():
    import importlib.util, os
    f = os.path.join(os.path.dirname(os.path.abspath("agentic2.py")), "..", "agentic", "paper_v105_i8.py")
    spec = importlib.util.spec_from_file_location("p8", f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def f_8_steps():
    m = _p8()
    def cost(st, cache):
        n_in = sum(m.SYS + m.ADD * k for k in range(st)); new = m.SYS + m.ADD * (st - 1)
        if cache: return (n_in - new) * m.P_CACHE / 1e6 + new * m.P_IN / 1e6 * 1.25 + m.OUT * st * m.P_OUT / 1e6 + m.TOOLS
        return n_in * m.P_IN / 1e6 + m.OUT * st * m.P_OUT / 1e6 + m.TOOLS
    st = np.arange(1, 21)
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    ax.plot(st, [cost(k, 0) for k in st], color=ORANGE, label="Without caching")
    ax.plot(st, [cost(k, 1) for k in st], color=BLUE, label="With prompt caching")
    for c, col in ((0, ORANGE), (1, BLUE)):
        ax.plot([m.STEPS], [cost(m.STEPS, c)], "o", color=col, ms=7, zorder=5)
    ax.annotate(f"Example, {m.STEPS} steps: ${cost(m.STEPS, 0):.2f}", xy=(m.STEPS, cost(m.STEPS, 0)), xytext=(3.2, 0.62), fontsize=9.3, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1))
    ax.annotate(f"${cost(m.STEPS, 1):.2f} with caching", xy=(m.STEPS, cost(m.STEPS, 1)), xytext=(10.5, 0.05), fontsize=9.3, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=1))
    ax.set_xlim(1, 20); ax.set_ylim(0, 1.3); ax.set_xticks([1, 4, 8, 12, 16, 20])
    ax.set_xlabel("Agent steps per task"); ax.set_ylabel("Cost per task ($)")
    ax.legend(loc="upper left")
    save(fig, S8, "fig1-cost-vs-steps")


def f_8_tornado():
    m = _p8()
    base = dict(V=m.VOL, r=m.REV_SHARE, B=m.BUILD, th=m.T_H, F=m.FIXED, redo=m.REDO, price=1.0)
    def pb(d):
        ch = d["th"] / 60 * m.WAGE
        cu = m.C_CACHE * d["price"] + d["r"] * m.T_REV / 60 * m.WAGE + d["redo"] * ch
        net = d["V"] * (ch - cu) - d["F"]
        return d["B"] / net
    b0 = pb(base)
    rows = [("Monthly volume", "V", 1000, 4000, "1,000", "4,000"), ("Review share", "r", 0.10, 0.60, "10%", "60%"),
            ("Build cost", "B", 25000, 80000, "$25k", "$80k"), ("Human minutes per invoice", "th", 4, 9, "4", "9"),
            ("Fixed cost per month", "F", 500, 3000, "$500", "$3,000"), ("Rework share", "redo", 0.02, 0.15, "2%", "15%"),
            ("Token price", "price", 0.5, 2.0, "½×", "2×")]
    res = []
    for lab, k, lo, hi, tlo, thi in rows:
        a = pb({**base, k: lo}); b = pb({**base, k: hi}); res.append((lab, a, b, tlo, thi))
    res.sort(key=lambda r: abs(r[2] - r[1]))
    fig, ax = plt.subplots(figsize=(7.8, 4.0))
    for i, (lab, a, b, tlo, thi) in enumerate(res):
        lo_, hi_ = min(a, b), max(a, b)
        ax.barh(i, hi_ - lo_, left=lo_, color=BLUE if i % 2 else BRIGHT, height=0.55)
        ax.text(lo_ - 0.25, i, tlo if a <= b else thi, ha="right", va="center", fontsize=8.8, color=INK)
        ax.text(hi_ + 0.25, i, thi if a <= b else tlo, ha="left", va="center", fontsize=8.8, color=INK)
    ax.axvline(b0, color=NAVY, lw=1.6, ls="--")
    ax.text(b0 + 0.4, len(res) - 0.35, f"Base case {b0:.1f} months", ha="left", fontsize=9.2, color=NAVY, fontweight="600")
    ax.set_yticks(range(len(res))); ax.set_yticklabels([r[0] for r in res])
    ax.set_xlabel("Payback period (months)"); ax.set_xlim(0, 28); ax.set_ylim(-0.6, len(res) - 0.1)
    ax.grid(axis="y", visible=False)
    save(fig, S8, "fig2-payback-sensitivity")



# =============================================================== 105(9) figures
def f_9_isa95():
    fig, ax = canvas(8.8, 5.0)
    ax.add_patch(Rectangle((1, 54), 74, 44, fc=GREENF, ec=GREEN_D, lw=1.4, ls="--"))
    ax.text(3, 95.5, "Agents operate here", fontsize=10, color=GREEN_D, fontweight="600", va="top")
    box(ax, 5, 76, 66, 11, "Level 4  Business planning and logistics: ERP", fill="white", fs=9.5, bold=True)
    box(ax, 5, 58, 66, 12, "Level 3  Operations management: MES · CMMS · historian · LIMS · quality", fill="white", fs=9.5, bold=True)
    ax.plot([1, 99], [49.5, 49.5], color=RED, lw=2.2)
    ax.text(3, 45.5, "No agent writes below this line", ha="left", fontsize=9, color=RED, fontweight="600")
    box(ax, 5, 25, 66, 12, "Level 2  Supervisory control: SCADA · DCS operator stations", fill=PALE, fs=9.5, bold=True)
    box(ax, 5, 4, 66, 13, "Levels 0–1  Process, sensors, actuators, PLCs", fill=PALE, fs=9.5, bold=True)
    box(ax, 79, 4, 19, 33, "Safety\ninstrumented\nsystem\n\nno agent role", fill=REDF, ec=RED, fs=9, bold=True)
    arr(ax, (52, 37.5), (52, 57.5), col=BLUE, lw=1.8)
    ax.text(54, 43, "read-only\n(historian, OPC UA)", fontsize=8.8, color=BLUE, va="center", linespacing=1.1)
    save(fig, S9, "fig1-isa95-boundary")


def f_9_mttr():
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    mins = np.linspace(0, 60, 121)
    for mtbf, col in ((20, ORANGE), (40, BLUE), (100, GREEN_D)):
        a0 = mtbf / (mtbf + 2.0); g = [(mtbf / (mtbf + 2.0 - m / 60) - a0) * 100 for m in mins]
        ax.plot(mins, g, color=col, label=f"MTBF {mtbf} h")
    a0 = 40 / 42; g = (40 / 41.5 - a0) * 100
    ax.plot([30], [g], "o", color=NAVY, ms=7, zorder=5)
    ax.annotate(f"Worked example: +{g:.1f} points", xy=(30, g), xytext=(41, 0.2), fontsize=9.3, color=NAVY, arrowprops=dict(arrowstyle="-", color=NAVY, lw=1))
    ax.set_xlim(0, 60); ax.set_ylim(0, 4.6)
    ax.set_xlabel("Diagnosis time saved per failure (minutes)"); ax.set_ylabel("Availability gain (percentage points)")
    ax.legend(loc="upper left"); ax.text(59, 3.1, "MTTR before = 2 h", ha="right", fontsize=8.8, color=INK)
    save(fig, S9, "fig2-mttr-availability")


def f_9_arch():
    fig, ax = canvas(9.0, 6.0)
    def zone(y, h, t, fc):
        ax.add_patch(Rectangle((1, y), 98, h, fc=fc, ec="#9AB0C8", lw=1))
        ax.text(2.5, y + h - 2.5, t, fontsize=9.5, color=NAVY, fontweight="600", va="top")
    zone(70, 28, "Enterprise zone", PALE); zone(38, 28, "Plant DMZ", "#F4F7FB"); zone(2, 32, "Control zone", "#EEF1F4")
    box(ax, 6, 74, 30, 12, "AI agents", fill=SKY, ec=BLUE, bold=True, fs=10)
    box(ax, 44, 72, 26, 16, "Gateway\nidentity · scopes · audit log", fill="white", ec=BLUE, fs=8.8, bold=True)
    box(ax, 76, 76, 20, 9, "ERP tool server", fill="white", fs=8.6)
    arr(ax, (36.5, 80), (43.5, 80)); arr(ax, (70.5, 80.5), (75.5, 80.5))
    for x, t in ((6, "CMMS\ntool server"), (28, "MES and quality\ntool server"), (52, "Historian\nreplica")):
        box(ax, x, 42, 19, 13, t, fill="white", fs=8.6)
    arr(ax, (52, 71.5), (15.5, 55.5)); arr(ax, (56, 71.5), (37.5, 55.5)); arr(ax, (60, 71.5), (61.5, 55.5))
    ax.plot([1, 99], [36, 36], color=NAVY, lw=2.4); ax.text(98, 37.2, "firewall", ha="right", fontsize=8.6, color=NAVY)
    box(ax, 6, 8, 40, 14, "SCADA · DCS · PLCs", fill=PALE, fs=9.5, bold=True)
    box(ax, 72, 6, 24, 18, "Safety\ninstrumented system\n(own zone)", fill=REDF, ec=RED, fs=8.8, bold=True)
    arr(ax, (40, 22.5), (58, 41.5), col=BLUE, lw=1.8)
    ax.text(51, 28, "one-way\nprocess data", fontsize=8.6, color=BLUE, ha="left", linespacing=1.1)
    ax.text(79, 58, "No path from agents\nto the control zone", fontsize=9, color=RED, fontweight="600", ha="center", linespacing=1.15)
    save(fig, S9, "fig3-plant-architecture")



# =============================================================== 105(10) figures
def f_10_passk():
    k = np.arange(1, 17)
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    for p, col in ((0.99, GREEN_D), (0.95, BLUE), (0.90, ORANGE)):
        ax.plot(k, p ** k * 100, color=col, marker="o", ms=3.5, label=f"{p * 100:.0f}% per attempt")
        ax.annotate(f"{p ** 8 * 100:.0f}%", xy=(8, p ** 8 * 100), xytext=(6, 4), textcoords="offset points", fontsize=9.2, color=col)
    ax.axvline(8, color=GREY, lw=1, ls="--")
    ax.set_xlim(1, 16); ax.set_ylim(0, 102); ax.set_xticks([1, 2, 4, 8, 12, 16])
    ax.set_xlabel("Attempts at the same task, k"); ax.set_ylabel("Succeeds on all k attempts (%)")
    ax.legend(loc="lower left")
    save(fig, S10, "fig1-pass-k")


def f_10_wilson():
    import math
    def w(n, p=0.9, z=1.96):
        d = 1 + z * z / n; return 2 * z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d * 100
    n = np.logspace(math.log10(20), 3, 200)
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    ax.set_xscale("log")
    ax.plot(n, [w(x) for x in n], color=BLUE)
    for x in (50, 400):
        ax.plot([x], [w(x)], "o", color=NAVY, ms=7, zorder=5)
        ax.annotate(f"{x} tasks: ±{w(x) / 2:.1f} points", xy=(x, w(x)), xytext=(10, 6), textcoords="offset points", fontsize=9.3, color=NAVY)
    ax.set_xlim(20, 1000); ax.set_ylim(0, 30)
    ax.set_xticks([20, 50, 100, 200, 400, 1000]); ax.set_xticklabels(["20", "50", "100", "200", "400", "1,000"]); ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_xlabel("Tasks in the evaluation set, n"); ax.set_ylabel("Width of 95% interval (points)")
    save(fig, S10, "fig2-interval-width")



# =============================================================== 105(11) figures
def f_11_timeline():
    import datetime as dt
    ev = [(dt.date(2024, 8, 1), "Act enters\ninto force", NAVY, 1),
          (dt.date(2025, 2, 2), "Prohibitions,\nAI literacy", RED, -1),
          (dt.date(2025, 8, 2), "General-purpose\nAI models", BLUE, 1),
          (dt.date(2026, 7, 27), "Digital Omnibus\nin force", GREY, -1),
          (dt.date(2026, 8, 2), "Transparency (Art. 50),\nenforcement powers", GREEN_D, 1),
          (dt.date(2026, 12, 2), "Content marking for\nexisting systems", GREEN_D, -1),
          (dt.date(2027, 12, 2), "High-risk:\nAnnex III", ORANGE, 1),
          (dt.date(2028, 8, 2), "High-risk:\nAnnex I products", ORANGE, -1)]
    x0 = dt.date(2024, 5, 1).toordinal()
    X = lambda d: (d.toordinal() - x0) / 365.25
    fig, ax = plt.subplots(figsize=(9.0, 3.6))
    ax.axhline(0, color=NAVY, lw=2)
    for y in range(2025, 2030):
        ax.plot([X(dt.date(y, 1, 1))] * 2, [-0.08, 0.08], color=NAVY, lw=1.5)
        ax.text(X(dt.date(y, 1, 1)), -0.22, str(y), ha="center", va="top", fontsize=9.5, color=NAVY, fontweight="600")
    for d, t, col, side in ev:
        x = X(d); h = 0.75 if side > 0 else -0.62
        ax.plot([x, x], [0, h * 0.82], color=col, lw=1.2)
        ax.plot([x], [0], "o", color=col, ms=7, zorder=5)
        ha, tx = "center", x
        if d == dt.date(2026, 7, 27): ha, tx = "right", x - 0.03
        if d == dt.date(2026, 12, 2): ha, tx = "left", x + 0.03
        ax.text(tx, h, d.strftime("%-d %b %Y") + "\n" + t, ha=ha, va="bottom" if side > 0 else "top", fontsize=8.2, color=col, linespacing=1.15)
    ax.set_xlim(-0.1, X(dt.date(2029, 1, 31))); ax.set_ylim(-1.45, 1.6); ax.axis("off")
    save(fig, S11, "fig1-timeline")


def f_11_flow():
    fig, ax = canvas(9.0, 5.4)
    def dia(cx, cy, w, h, t):
        ax.add_patch(Polygon([(cx - w, cy), (cx, cy + h), (cx + w, cy), (cx, cy - h)], closed=True, fc=PALE, ec="#9AB0C8", lw=1))
        ax.text(cx, cy, t, ha="center", va="center", fontsize=8.6, color=NAVY, linespacing=1.15)
    dia(22, 82, 20, 13, "Places AI on the EU\nmarket, or output\nused in the EU?")
    box(ax, 3, 46, 30, 14, "No: Act does not apply.\nFollow good practice\n(NIST AI RMF, ISO/IEC 42001)", fill="white", fs=8.4)
    arr(ax, (22, 68.5), (22, 60.5)); ax.text(23.5, 64.5, "no", fontsize=8.6, color=INK)
    arr(ax, (42.5, 82), (50, 82)); ax.text(46, 84, "yes", fontsize=8.6, color=INK, ha="center")
    box(ax, 50.5, 75, 22, 14, "Decide role:\nprovider or deployer", fill=SKY, ec=BLUE, fs=8.8, bold=True)
    arr(ax, (61.5, 74.5), (61.5, 66.5))
    box(ax, 46, 55, 31, 11, "Classify the use (Art. 5, 6, 50;\nAnnexes I and III)", fill=SKY, ec=BLUE, fs=8.6, bold=True)
    outs = [(4, "Prohibited", "stop", REDF, RED), (28, "High-risk", "full duties by Dec 2027\nor Aug 2028", ORANGEF, ORANGE),
            (52, "Limited risk", "transparency duties now", GREENF, GREEN_D), (76, "Minimal risk", "AI literacy measures only", PALE, "#9AB0C8")]
    ax.plot([15, 87], [44, 44], color=NAVY, lw=1.4); ax.plot([61.5, 61.5], [54.5, 44], color=NAVY, lw=1.4)
    for x, t, sub, fc, ec in outs:
        arr(ax, (x + 11, 44), (x + 11, 36.5))
        box(ax, x, 18, 22, 18, "", fill=fc, ec=ec, lw=1.3)
        ax.text(x + 11, 31, t, ha="center", va="center", fontsize=9.4, color=NAVY, fontweight="600")
        ax.text(x + 11, 23.5, sub, ha="center", va="center", fontsize=8.2, color=INK, linespacing=1.15)
    ax.text(50, 8, "Then: inventory kept current · contracts set roles and information · governance in a management system", ha="center", fontsize=8.6, color=NAVY)
    save(fig, S11, "fig2-decision-flow")


if __name__ == "__main__" or True:
    import sys as _s
    run(_s.argv[1] if len(_s.argv) > 1 and not _s.argv[1].startswith("-") else None)
