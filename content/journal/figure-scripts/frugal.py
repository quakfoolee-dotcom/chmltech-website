"""Figures for Vol. 103(1): FrugalGPT and MultiModal-GPT."""
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
from style import *

SLUG = "chmltech-online-journal-volume-103-issue-1"
TXT = "#4A5568"


def box(ax, x, y, w, h, text, fc=LIGHT, ec="#9AB0C8", tc=NAVY, fs=9.5, weight="normal", ls="-", r=0.08):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=1.2, ls=ls))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, fontweight=weight, linespacing=1.25)


def arrow(ax, p, q, col=NAVY, lw=1.3, ls="-", cs="arc3"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11, color=col, lw=lw, ls=ls, connectionstyle=cs, shrinkA=0, shrinkB=0))


def diamond(ax, x, y, w, h, text, fc="white", ec=BLUE, fs=9):
    ax.add_patch(Polygon([(x - w / 2, y), (x, y + h / 2), (x + w / 2, y), (x, y - h / 2)], closed=True, fc=fc, ec=ec, lw=1.3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=NAVY, linespacing=1.2)


# Figure 1 — LLM cascade, Eqs. (4)-(5), with the learned HEADLINES policy
fig, ax = plt.subplots(figsize=(8.8, 4.3)); ax.axis("off"); ax.set_xlim(0, 10.6); ax.set_ylim(-0.75, 5.2)
box(ax, 0.75, 3.9, 1.2, 0.75, "Query $q$", fc=NAVY, ec=NAVY, tc="white", weight="600")
stages = [(2.75, "Stage 1: $L_1$", "GPT-J", r"$\tau_1 = 0.96$"), (5.65, "Stage 2: $L_2$", "J1-Large", r"$\tau_2 = 0.37$"), (8.55, "Stage 3: $L_3$", "GPT-4", None)]
for k, (x, lab, name, tau) in enumerate(stages):
    fc = ["#E4F1E0", "#E6EEF7", "#FBE6D8"][k]; ec = [GREEN_D, BLUE, ORANGE][k]
    box(ax, x, 3.9, 1.85, 0.85, f"{lab}\n{name}", fc=fc, ec=ec, weight="600")
    ax.text(x, 4.55, ["cheapest", "", "most expensive"][k], ha="center", va="bottom", fontsize=9, color=TXT, style="italic")
    if tau:
        diamond(ax, x, 2.35, 2.05, 1.15, "$g(q, a_" + str(k + 1) + r") \geq \tau_" + str(k + 1) + "$?\n" + tau)
        arrow(ax, (x, 3.47), (x, 2.93))
        ax.text(x + 0.08, 3.2, f"answer $a_{k + 1}$", fontsize=9, color=TXT, va="center")
        nx = stages[k + 1][0]
        arrow(ax, (x + 1.03, 2.35), (nx - 0.93, 3.62), col=ORANGE, cs="arc3,rad=0.25")
        ax.text((x + nx) / 2, 2.2, "reject:\nescalate", fontsize=9, color="#B4410C", ha="center", va="top")
        arrow(ax, (x, 1.77), (x, 1.12), col=GREEN_D)
        ax.text(x + 0.1, 1.45, "accept", fontsize=9, color=GREEN_D, va="center", fontweight="600")
    else:
        arrow(ax, (x, 3.47), (x, 1.12), col=NAVY)
        ax.text(x + 0.1, 2.35, "last stage:\nanswer $a_3$\nreturned\nwithout scoring", fontsize=9, color=TXT, va="center")
arrow(ax, (1.35, 3.9), (1.82, 3.9))
box(ax, 5.65, 0.78, 7.9, 0.62, r"Return one answer $f_{L_z}(q)$ from the stopping stage $z$, Eq. (4)", fc="#EEF4FA", ec=NAVY, weight="600")
ax.text(0.15, 0.3, r"Cost paid per query $= \Sigma_{i=1}^{z}\, c_{L_i}(q)$.  Learned offline: ordering $L$, thresholds $\tau$ and scorer $g$ (DistilBERT),"+"\n"+r"chosen to maximize expected accuracy subject to expected cost $\leq b$, Eq. (5).",
        fontsize=9, color=NAVY, va="top", linespacing=1.5)
save(fig, SLUG, "fig1-cascade")

# Figure 2 — reported cost and accuracy (Table 2 and the HEADLINES case of Section 3.5)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.8), gridspec_kw=dict(wspace=0.42, width_ratios=[1, 1.15]))
ds = ["HEADLINES", "OVERRULING", "COQA"]; best = [33.1, 9.7, 72.5]; fr = [0.6, 2.6, 29.6]; red = ["98.3%", "73.3%", "59.2%"]
y = np.arange(3)[::-1]
a1.barh(y + 0.18, best, height=0.34, color=LIGHT, edgecolor="#B9C7D8", label="Best individual LLM")
a1.barh(y - 0.18, fr, height=0.34, color=BLUE, label="FrugalGPT (matched performance)")
for k in range(3):
    a1.text(best[k] + 1.2, y[k] + 0.18, f"${best[k]}", va="center", fontsize=9, color=TXT)
    a1.text(fr[k] + 1.2, y[k] - 0.18, f"${fr[k]}  (−{red[k]})", va="center", fontsize=9, color=NAVY, fontweight="600")
a1.set_yticks(y); a1.set_yticklabels([f"{d}\n({b})" for d, b in zip(ds, ["vs GPT-4", "vs GPT-4", "vs GPT-3"])], fontsize=9)
a1.set_xlim(0, 100); a1.set_xlabel("Cost of evaluation workload (USD)"); a1.grid(axis="y", visible=False)
a1.legend(loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=1, fontsize=9); a1.set_title("(a) Cost to match the best LLM", pad=44)
# (b) HEADLINES: cost relative to GPT-4 on every query vs accuracy
a2.axvspan(0, 0.2, color="#EEF4FA", zorder=0)
a2.text(0.012, 0.8472, "budget $b$ = 1/5 of\nGPT-4 cost", fontsize=9, color=BLUE, va="bottom")
a2.plot([1.0], [0.857], "o", color=GREY, ms=9, zorder=4); a2.text(1.04, 0.8545, "GPT-4 alone\naccuracy 0.857", ha="right", va="top", fontsize=9, color=TXT)
a2.plot([0.2], [0.872], "o", color=GREEN_D, ms=9, zorder=4); a2.text(0.225, 0.8728, "FrugalGPT cascade\naccuracy 0.872", ha="left", va="bottom", fontsize=9, color=GREEN_D, fontweight="600")
a2.add_patch(FancyArrowPatch((0.95, 0.8578), (0.218, 0.8707), arrowstyle="-|>", mutation_scale=11, color=NAVY, lw=1.1, connectionstyle="arc3,rad=0", ls="--"))
a2.text(0.78, 0.8655, "≈ 80% lower cost,\n+1.5 points accuracy", ha="center", va="bottom", fontsize=9, color=NAVY, rotation=0)
a2.set_xlim(0, 1.08); a2.set_ylim(0.845, 0.88)
a2.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]); a2.set_xticklabels(["0", "0.2", "0.4", "0.6", "0.8", "1.0"])
a2.set_xlabel("Cost relative to GPT-4 on every query"); a2.set_ylabel("Accuracy on HEADLINES")
a2.set_title("(b) HEADLINES at a fixed budget", pad=10)
save(fig, SLUG, "fig2-cost-accuracy")

# Figure 3 — MultiModal-GPT: frozen OpenFlamingo with LoRA adapters (after Gong et al. and Flamingo)
fig, ax = plt.subplots(figsize=(8.8, 4.6)); ax.axis("off"); ax.set_xlim(0, 10.6); ax.set_ylim(0, 5.6)
FZ, FZE = "#EEF1F5", "#A9B6C6"           # frozen
TR, TRE = "#E4F1E0", GREEN_D             # trainable
box(ax, 0.95, 4.65, 1.6, 0.7, "Image $I$", fc=NAVY, ec=NAVY, tc="white", weight="600")
box(ax, 0.95, 3.35, 1.6, 0.95, "Vision encoder\n(CLIP-based)", fc=FZ, ec=FZE)
box(ax, 0.95, 1.95, 1.6, 0.95, "Perceiver\nResampler", fc=FZ, ec=FZE)
ax.text(0.95, 1.22, "fixed set of\nvisual tokens $V$", ha="center", va="top", fontsize=9, color=TXT)
arrow(ax, (0.95, 4.3), (0.95, 3.83)); arrow(ax, (0.95, 2.87), (0.95, 2.43))
# one decoder layer of the language model, repeated
ax.add_patch(FancyBboxPatch((2.75, 0.55), 5.1, 4.55, boxstyle="round,pad=0,rounding_size=0.12", fc="white", ec=NAVY, lw=1.3, ls="--"))
ax.text(5.3, 4.85, "LLaMA decoder layer (repeated × N)", ha="center", va="center", fontsize=9.5, color=NAVY, fontweight="600")
rows = [(1.45, "Gated cross-attention to $V$\n" + r"$y = x + \tanh(\alpha)\,\mathrm{XAttn}(x, V)$", "LoRA"),
        (2.75, "Self-attention (causal)", "LoRA"),
        (4.05, "Feed-forward network (FFN)", "LoRA")]
for yy, t, l in rows:
    box(ax, 4.6, yy, 3.3, 0.88, t, fc=FZ, ec=FZE, fs=9.2)
    box(ax, 7.05, yy, 1.05, 0.6, l, fc=TR, ec=TRE, tc=GREEN_D, weight="600", fs=9)
    ax.plot([6.25, 6.52], [yy, yy], color=GREEN_D, lw=1.3)
arrow(ax, (4.6, 1.9), (4.6, 2.3)); arrow(ax, (4.6, 3.2), (4.6, 3.6))
arrow(ax, (1.75, 1.95), (2.94, 1.6), col=BLUE)
ax.text(4.6, 0.3, "text tokens: instruction + response", ha="center", va="center", fontsize=9, color=TXT)
arrow(ax, (4.6, 0.45), (4.6, 1.0))
# right panel: training recipe
box(ax, 9.35, 4.05, 2.2, 1.05, "Next-token loss on\nresponse tokens only,\nEq. (8)", fc="#EEF4FA", ec=NAVY, fs=9)
box(ax, 9.35, 2.45, 2.2, 1.45, "Each step pairs:\n1 vision-language +\n1 language-only\ninstruction example", fc="#EEF4FA", ec=NAVY, fs=9)
ax.text(9.35, 1.15, r"LoRA: $h = W_0 x + \frac{\alpha_L}{r} BAx$" + "\nonly $A$, $B$ trained, Eq. (7)", ha="center", va="center", fontsize=9, color=GREEN_D)
# legend
ax.add_patch(FancyBboxPatch((8.3, 0.18), 0.3, 0.22, boxstyle="round,pad=0,rounding_size=0.04", fc=FZ, ec=FZE)); ax.text(8.68, 0.29, "frozen", fontsize=9, color=TXT, va="center")
ax.add_patch(FancyBboxPatch((9.4, 0.18), 0.3, 0.22, boxstyle="round,pad=0,rounding_size=0.04", fc=TR, ec=TRE)); ax.text(9.78, 0.29, "trained", fontsize=9, color=TXT, va="center")
save(fig, SLUG, "fig3-multimodal-gpt")
print("frugal figures done")
