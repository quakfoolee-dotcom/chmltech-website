"""Figures for Vol. 105(1)-(3): the three Physical AI papers (V4.19)."""
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
from style import *

S1 = "physical-ai-foundations-architectures-and-the-sim-to-real-gap"
S2 = "physical-ai-in-process-plants-and-factories-inspection-manipulation-and-control"
S3 = "safety-reliability-and-economics-of-deploying-physical-ai"
INK = "#4A5568"; PALE = "#EEF3F9"; SKY = "#CFE6F3"; GREENF = "#E4F1D3"; ORANGEF = "#FBE6D8"


def box(ax, x0, y0, w, h, txt, fill=LIGHT, tc=NAVY, fs=9, bold=False, ec="#9AB0C8", ls="-", lw=1):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.25,rounding_size=1.0", fc=fill, ec=ec, lw=lw, ls=ls))
    ax.text(x0 + w / 2, y0 + h / 2, txt, ha="center", va="center", fontsize=fs, color=tc, fontweight="600" if bold else "normal", linespacing=1.25)


def arr(ax, p, q, col=NAVY, lw=1.6, ls="-", style="-|>", ms=11, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=col, lw=lw, ls=ls, shrinkA=0, shrinkB=0, connectionstyle=f"arc3,rad={rad}"))


# =============================================================== 105(1)
# Figure 1 — the stack and its timescales (Section 3.3)
fig, ax = plt.subplots(figsize=(8.6, 5.2)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
X0, W = 16, 44
rows = [
    (84, 11, "Task instruction\n(language or goal)", PALE, "Changes per task", ""),
    (64, 13, "Reasoning module\nvision-language model", SKY, "1–10 Hz", "RT-2: 1–3 Hz · OpenVLA: ~6 Hz\nGR00T N1 (System 2): 10 Hz"),
    (44, 13, "Action generator\naction chunks, Eq. (1)", SKY, "50–120 Hz", "π₀: up to 50 Hz\nGR00T N1 (System 1): 120 Hz"),
    (25, 12, "Joint servo control\nconventional feedback", LIGHT, "Faster still (not learned)", ""),
    (4, 13, "Robot and environment\nmotors · cameras · joint sensors", PALE, "Physical world", ""),
]
for y, h, t, c, rate, ex in rows:
    box(ax, X0, y, W, h, t, fill=c, fs=9.5)
    ax.text(X0 + W + 5, y + h / 2 + (4.2 if ex else 0), rate, ha="left", va="center", fontsize=10.5, color=NAVY, fontweight="600")
    if ex: ax.text(X0 + W + 5, y + h / 2 - 2.4, ex, ha="left", va="center", fontsize=8.5, color=INK, linespacing=1.25)
for ya, yb in [(83.4, 78), (63.4, 58), (43.4, 38), (24.4, 18)]:
    arr(ax, (X0 + W / 2, ya), (X0 + W / 2, yb), BLUE)
# feedback path on the left
xl = 8
ax.plot([X0 - 0.8, xl], [10.5, 10.5], color=GREEN_D, lw=1.8)
ax.plot([xl, xl], [10.5, 70.5], color=GREEN_D, lw=1.8)
for y in (70.5, 50.5, 31):
    arr(ax, (xl, y), (X0 - 0.8, y), GREEN_D, lw=1.8)
ax.text(xl - 2.2, 40, "Observations (images, joint readings)", rotation=90, ha="center", va="center", fontsize=9, color=GREEN_D)
ax.text(X0 + W / 2 + 2, 80.6, "instruction", fontsize=8.5, color=BLUE, va="center")
ax.text(X0 + W / 2 + 2, 60.6, "plan or latent goal", fontsize=8.5, color=BLUE, va="center")
ax.text(X0 + W / 2 + 2, 40.6, "target poses", fontsize=8.5, color=BLUE, va="center")
ax.text(X0 + W / 2 + 2, 21.2, "motor commands", fontsize=8.5, color=BLUE, va="center")
ax.text(X0 + W + 5, 99, "Update rate", ha="left", va="top", fontsize=9, color=INK)
save(fig, S1, "fig1-stack-timescales")

# Figure 2 — compounding error, Eq. (3), with eps = 0.01
eps = 0.01; T = np.arange(1, 101)
fig, ax = plt.subplots(figsize=(6.8, 4.0))
ax.plot(T, eps * T ** 2, color=ORANGE, label=r"Behavior cloning bound, $\varepsilon T^{2}$")
ax.plot(T, eps * T, color=BLUE, label=r"Interactive learning, order $\varepsilon T$")
ax.plot(T, T, color=GREY, ls=(0, (4, 3)), lw=1.4, label=r"Upper limit: a mistake at every step, $T$")
ax.set_yscale("log"); ax.set_ylim(0.008, 150); ax.set_xlim(0, 100)
ax.set_yticks([0.01, 0.1, 1, 10, 100]); ax.set_yticklabels(["0.01", "0.1", "1", "10", "100"]); ax.minorticks_off()
for t in (50,):
    ax.plot([t, t], [eps * t, eps * t ** 2], color=NAVY, lw=1, ls=":")
    ax.plot([t], [eps * t ** 2], "o", color=ORANGE, ms=6); ax.plot([t], [eps * t], "o", color=BLUE, ms=6)
    ax.annotate("25 mistakes", xy=(t, eps * t ** 2), xytext=(t - 31, 42), fontsize=9, color=NAVY, arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.9))
    ax.annotate("0.5 mistakes", xy=(t, eps * t), xytext=(t + 8, 0.17), fontsize=9, color=NAVY, arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.9))
ax.set_xlabel(r"Task horizon $T$ (steps)"); ax.set_ylabel("Expected number of mistakes")
ax.legend(loc="lower right", fontsize=9)
save(fig, S1, "fig2-compounding-error")

# Figure 3 — domain randomization (schematic), Eq. (5)
x = np.linspace(0, 10, 500); real = 6.6
g = lambda m, s: np.exp(-0.5 * ((x - m) / s) ** 2) / s
fig, axs = plt.subplots(3, 1, figsize=(7.2, 4.9), sharex=True, gridspec_kw=dict(hspace=0.32))
cases = [("(a) Too narrow: the real system lies outside the training range", 3.6, 0.55, ORANGE, "Transfer fails"),
         ("(b) Suitable: the range covers the real system", 5.6, 1.25, GREEN_D, "Transfer succeeds"),
         ("(c) Too wide: covered, but the policy must compromise", 5.0, 3.4, BLUE, "Conservative policy")]
for ax, (ttl, m, s, col, verdict) in zip(axs, cases):
    y = g(m, s); y = y / y.max()
    ax.fill_between(x, 0, y, color=col, alpha=0.22, lw=0); ax.plot(x, y, color=col, lw=2)
    ax.axvline(real, color=NAVY, lw=1.6, ls=(0, (4, 3)))
    ax.set_ylim(0, 1.32); ax.set_yticks([]); ax.set_xticks([]); ax.grid(False)
    ax.spines["left"].set_visible(False)
    ax.text(0.0, 1.06, ttl, transform=ax.transAxes, fontsize=9.5, color=NAVY, fontweight="600", ha="left", va="bottom")
    ax.text(0.995, 0.86, verdict, transform=ax.transAxes, fontsize=9, color=col, ha="right", va="top", fontweight="600")
axs[0].text(real - 0.15, 0.62, "real system\n(value unknown)", fontsize=8.5, color=NAVY, ha="right", va="center", linespacing=1.2)
axs[2].set_xlabel("Simulator parameter ξ, e.g. friction coefficient (relative units)")
fig.text(0.075, 0.5, r"Training distribution $p(\xi)$", rotation=90, va="center", ha="center", fontsize=10, color=NAVY)
save(fig, S1, "fig3-domain-randomization")

# =============================================================== 105(2)
# Figure 1 — where the three application classes sit in the plant hierarchy (Section 3)
fig, ax = plt.subplots(figsize=(8.8, 5.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
X0, W = 24, 40
layers = [(80, 13, "Operations and maintenance systems\ndigital twin · maintenance management", PALE),
          (60, 12, "Supervisory control\nMPC · optimization", LIGHT),
          (41, 12, "Regulatory control\nDCS / PLC loops", LIGHT),
          (22, 12, "Field devices\nsensors · valves · drives", LIGHT),
          (3, 12, "Process equipment,\nmaterials and work areas", PALE)]
for y, h, t, c in layers:
    box(ax, X0, y, W, h, t, fill=c, fs=9.2)
for ya, yb in [(59.4, 54), (40.4, 35), (21.4, 16)]:
    arr(ax, (X0 + W / 2 - 4, ya), (X0 + W / 2 - 4, yb), BLUE, lw=1.4)
    arr(ax, (X0 + W / 2 + 4, yb), (X0 + W / 2 + 4, ya), BLUE, lw=1.4)
arr(ax, (X0 + W / 2 + 4, 73), (X0 + W / 2 + 4, 79.4), BLUE, lw=1.4); arr(ax, (X0 + W / 2 - 4, 79.4), (X0 + W / 2 - 4, 73), BLUE, lw=1.4)
# independent safety system (right of the control layers)
box(ax, X0 + W + 4, 22, 12, 31, "Safety\ninstrumented\nsystem\n\nindependent", fill="#F4F6F9", fs=8.6, ec=NAVY, lw=1.3)
arr(ax, (X0 + W + 10, 21.4), (X0 + W + 10, 15.6), NAVY, lw=1.4)
ax.plot([X0 + W + 0.8, X0 + W + 10], [9, 9], color=NAVY, lw=1.4); ax.plot([X0 + W + 10, X0 + W + 10], [9, 15.6], color=NAVY, lw=1.4)
# class C: learned controller at the supervisory layer
box(ax, 84, 59, 15, 14, "(C) Learned\ncontroller", fill=ORANGEF, ec=ORANGE, fs=9.2, bold=True)
arr(ax, (83.4, 66), (X0 + W + 0.8, 66), ORANGE, lw=1.8)
ax.text(74.5, 68, "set points\nwithin limits", fontsize=8.3, color=ORANGE, ha="center", va="bottom", linespacing=1.15)
# class A: inspection robot (left, bottom to top)
box(ax, 1, 3, 17, 14, "(A) Inspection\nrobot", fill=GREENF, ec=GREEN_D, fs=9.2, bold=True)
arr(ax, (X0 - 0.8, 6.5), (18.6, 6.5), GREEN_D, lw=1.8)
ax.text(21.3, 0.2, "observes", fontsize=8.3, color=GREEN_D, ha="center", va="bottom")
ax.plot([9.5, 9.5], [17.6, 86.5], color=GREEN_D, lw=1.8); arr(ax, (9.5, 86.5), (X0 - 0.8, 86.5), GREEN_D, lw=1.8)
ax.text(7.2, 52, "inspection data", rotation=90, fontsize=8.5, color=GREEN_D, ha="center", va="center")
# class B: manipulation robot (right, bottom)
box(ax, 82, 3, 17, 14, "(B) Manipulation\nrobot", fill=SKY, ec=BLUE, fs=9.2, bold=True)
arr(ax, (81.4, 6.5), (X0 + W + 0.8, 6.5), BLUE, lw=1.8)
ax.text(73, 0.2, "handles objects", fontsize=8.3, color=BLUE, ha="center", va="bottom")
ax.text(X0 + W / 2, 97.5, "Existing plant hierarchy", ha="center", va="center", fontsize=9.5, color=INK)
save(fig, S2, "fig1-plant-hierarchy")

# Figure 2 — detection probability after n rounds, Eq. (1)
n = np.arange(0, 13)
fig, ax = plt.subplots(figsize=(6.8, 3.9))
for pd_, col in [(0.1, GREY), (0.3, BLUE), (0.5, GREEN_D)]:
    ax.plot(n, 1 - (1 - pd_) ** n, color=col, marker="o", ms=4, label=rf"$p_{{\mathrm{{d}}}}$ = {pd_}")
for k, dx, dy in [(1, 0.3, -0.085), (4, 0.35, -0.14), (8, 0.35, -0.14)]:
    v = 1 - 0.7 ** k
    ax.plot([k], [v], "o", color=NAVY, ms=7, zorder=5)
    ax.annotate(f"{v:.2f}", xy=(k, v), xytext=(k + dx, v + dy), fontsize=9, color=NAVY)
ax.set_xlim(0, 12); ax.set_ylim(0, 1.03); ax.set_xticks(range(0, 13, 2))
ax.set_xlabel(r"Number of inspection rounds $n$ within the fault's development time")
ax.set_ylabel(r"Probability of detection $P_n$")
ax.legend(loc="lower right", title="Detection probability per round", title_fontsize=9)
save(fig, S2, "fig2-detection-rounds")

# Figure 3 — indicative readiness ranges (Table 2)
apps = [("Robot and drone inspection rounds", 8, 9, GREEN_D), ("Anomaly detection on inspection data", 6, 8, GREEN_D),
        ("Bin picking and depalletizing", 8, 9, BLUE), ("Self-driving laboratories", 5, 7, BLUE),
        ("General-purpose manipulation (VLA)", 4, 6, BLUE), ("General-purpose humanoid labor", 4, 6, BLUE),
        ("Learned supervisory control, one unit", 6, 8, ORANGE)]
fig, ax = plt.subplots(figsize=(8.2, 3.9))
for k, (lab, a, b, col) in enumerate(apps):
    y = len(apps) - 1 - k
    ax.barh(y, b - a, left=a, height=0.5, color=col, alpha=0.85)
    ax.plot([a, b], [y, y], "o", color=col, ms=7)
    ax.text(b + 0.18, y, f"{a}–{b}", va="center", ha="left", fontsize=9, color=INK)
ax.set_yticks(range(len(apps))); ax.set_yticklabels([a[0] for a in apps][::-1], fontsize=9.5)
ax.set_xlim(1, 10); ax.set_xticks(range(1, 10)); ax.set_ylim(-0.6, len(apps) - 0.4)
ax.axvline(6, color=NAVY, lw=1, ls=(0, (4, 3))); ax.text(6, len(apps) - 0.33, "TRL 6: prototype in a\nrelevant environment", fontsize=8.3, color=NAVY, ha="right", va="bottom", linespacing=1.15)
ax.axvline(9, color=NAVY, lw=1, ls=(0, (4, 3))); ax.text(9, len(apps) - 0.33, "TRL 9: proven\nin operation", fontsize=8.3, color=NAVY, ha="right", va="bottom", linespacing=1.15)
ax.set_xlabel("Indicative technology readiness level (author's assessment, November 2026)")
ax.grid(axis="y", visible=False)
ax.legend(handles=[Line2D([], [], color=GREEN_D, lw=6, label="Inspection"), Line2D([], [], color=BLUE, lw=6, label="Manipulation"), Line2D([], [], color=ORANGE, lw=6, label="Process control")],
          loc="upper center", bbox_to_anchor=(0.36, -0.2), ncol=3)
save(fig, S2, "fig3-readiness")

# =============================================================== 105(3)
# Figure 1 — performance channel enclosed by a safety-rated layer (Section 4)
fig, ax = plt.subplots(figsize=(9.0, 4.9)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
ax.add_patch(FancyBboxPatch((51, 6), 27, 86, boxstyle="round,pad=0.3,rounding_size=1.5", fc="#F4F8EE", ec=GREEN_D, lw=1.6))
ax.text(64.5, 87, "Safety-rated layer", ha="center", va="center", fontsize=10, color=GREEN_D, fontweight="600")
ax.text(64.5, 81.5, "conventional, verified, PL d", ha="center", va="center", fontsize=8.5, color=GREEN_D)
box(ax, 54, 52, 21, 20, "Safety filter\nspeed · force\nworkspace · separation\nEqs. (1)–(2)", fill="white", ec=GREEN_D, fs=8.6)
box(ax, 54, 14, 21, 18, "Safety-rated sensing\nscanners\nlight curtains · e-stop", fill="white", ec=GREEN_D, fs=8.6)
arr(ax, (64.5, 32.6), (64.5, 51.2), GREEN_D, lw=1.6)
box(ax, 1, 54, 13, 16, "Cameras\njoint\nsensors", fill=PALE, fs=8.8)
box(ax, 19, 52, 18, 20, "Learned policy\n(performance\nchannel)", fill=SKY, ec=BLUE, fs=9, bold=True)
arr(ax, (14.8, 62), (18.2, 62), BLUE)
arr(ax, (37.8, 62), (53.2, 62), BLUE)
ax.text(44.3, 64.5, "proposed\naction", fontsize=8.2, color=BLUE, ha="center", va="bottom", linespacing=1.1)
box(ax, 88, 52, 11, 20, "Drives\nand\nactuators", fill=LIGHT, fs=8.8)
arr(ax, (75.8, 62), (87.2, 62), GREEN_D, lw=2)
ax.text(83.2, 64.5, "safe\naction", fontsize=8.2, color=GREEN_D, ha="center", va="bottom", linespacing=1.1)
ax.plot([75.8, 93.5], [22, 22], color=NAVY, lw=1.4); arr(ax, (93.5, 22), (93.5, 51.2), NAVY, lw=1.4)
ax.text(86.5, 18.5, "protective stop", fontsize=8.3, color=NAVY, ha="center", va="top")
box(ax, 19, 16, 18, 18, "Run-time monitor\nunfamiliar input,\nlow confidence", fill=ORANGEF, ec=ORANGE, fs=8.6)
arr(ax, (28, 51.2), (28, 34.8), ORANGE, lw=1.4, style="<|-|>")
box(ax, 1, 17, 13, 16, "Supervisor\n(asked\nfor help)", fill=PALE, fs=8.6)
arr(ax, (18.2, 25), (14.8, 25), ORANGE, lw=1.4)
ax.text(24, 6.5, "Improves task success and availability;\nnot part of the safety function", ha="center", va="center", fontsize=8.2, color=ORANGE, linespacing=1.2)
save(fig, S3, "fig1-safety-architecture")

# Figure 2 — task success against number of steps, Eq. (3)
n = np.arange(1, 101)
fig, ax = plt.subplots(figsize=(6.8, 3.9))
for p, col in [(0.999, GREEN_D), (0.99, BLUE), (0.95, ORANGE)]:
    ax.plot(n, p ** n, color=col, label=rf"$p$ = {p}")
for (k, p, dx, dy) in [(10, 0.99, 3, -0.11), (50, 0.99, 3, 0.04), (50, 0.999, 3, -0.10)]:
    v = p ** k; ax.plot([k], [v], "o", color=NAVY, ms=6.5, zorder=5)
    ax.annotate(f"{v:.2f}", xy=(k, v), xytext=(k + dx, v + dy), fontsize=9, color=NAVY)
ax.set_xlim(0, 100); ax.set_ylim(0, 1.03)
ax.set_xlabel(r"Number of steps in the task, $n$"); ax.set_ylabel(r"Probability the task succeeds, $P_{\mathrm{task}}$")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, title="Success probability per step", title_fontsize=9)
save(fig, S3, "fig2-task-success")

# Figure 3 — NPV against intervention fraction, Eqs. (6)-(7), inputs of Table 2
I, cL, M, af = 250000.0, 40.0, 30000.0, (1 - 1.1 ** -7) / 0.1
npv = lambda H, A, f: (-I + (H * A * cL * (1 - f) - M) * af) / 1000.0
f = np.linspace(0, 0.5, 200)
fig, ax = plt.subplots(figsize=(7.0, 4.1))
ax.axhline(0, color=NAVY, lw=1.2)
ax.plot(f, npv(6000, 0.9, f), color=GREEN_D, label="Three shifts, A = 0.90")
ax.plot(f, npv(4000, 0.9, f), color=BLUE, label="Two shifts, A = 0.90")
ax.plot(f, npv(4000, 0.7, f), color=BLUE, ls=(0, (5, 3)), lw=1.8, label="Two shifts, A = 0.70")
ax.plot(f, npv(2000, 0.9, f), color=ORANGE, label="One shift, A = 0.90")
for (H, A, ff, lab, dx, dy) in [(4000, 0.9, 0.10, "Base case\n+235", 0.012, 55), (4000, 0.7, 0.30, "Low reliability: −14", -0.04, 180), (2000, 0.9, 0.10, "Single shift: −81", -0.08, -115)]:
    v = npv(H, A, ff); ax.plot([ff], [v], "o", color=NAVY, ms=7, zorder=5)
    ax.annotate(lab, xy=(ff, v), xytext=(ff + dx, v + dy), fontsize=9, color=NAVY, linespacing=1.15, arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.8))
ax.set_xlim(0, 0.5); ax.set_ylim(-250, 620)
ax.set_xlabel(r"Intervention fraction $f$ (person-hours per robot-hour)"); ax.set_ylabel("NPV, 7 years at 10% (thousand USD)")
ax.legend(loc="upper right", fontsize=9)
save(fig, S3, "fig3-npv-intervention")
print("figures written")
