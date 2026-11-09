"""Figures for Vol. 103(2): Advancements in Machine Learning and Deep Learning for Intelligent Systems."""
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon
from style import *

SLUG = "copy-of-chmltech-online-journal-volume-103-issue-2"
TXT = "#4A5568"
MLF, MLE = "#E4F1E0", GREEN_D
DLF, DLE = "#E6EEF7", BLUE


def box(ax, x, y, w, h, text, fc=LIGHT, ec="#9AB0C8", tc=NAVY, fs=9.2, weight="normal", r=0.06, lw=1.2):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    if text: ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, fontweight=weight, linespacing=1.2)


def arrow(ax, p, q, col=NAVY, lw=1.2, cs="arc3", ms=10):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, color=col, lw=lw, connectionstyle=cs, shrinkA=0, shrinkB=0))


# Figure 1 — milestones discussed in the paper, with the years of the cited works
ML = {1986: ["Backpropagation trains multi-layer networks [6]"], 2001: ["Random forests [8]"], 2014: ["Transferability of deep CNN features [12]"],
      2015: ["DQN learns 49 Atari games from pixels [9]"], 2016: ["AlphaGo defeats European Go champion 5–0 [10]", "LIME local explanations [16]"],
      2017: ["AlphaGo Zero beats AlphaGo 100–0, no human data [11]", "SHAP feature attributions [17]", "Federated averaging [28]"],
      2019: ["Case for interpretable models in high stakes [18]"]}
DL = {1997: ["LSTM gated memory cell [21]"], 1998: ["LeNet: gradient-trained CNNs [19]"], 2009: ["ImageNet database [25]"],
      2012: ["AlexNet: 15.3% vs 26.2% top-5 error [20]"], 2014: ["GAN: generator vs discriminator [23]"],
      2015: ["ResNet: 152 layers, 3.57% top-5 error [14]", "4.94% top-5, below 5.1% human estimate [26]"],
      2017: ["Transformer: attention only, 28.4 BLEU [22]"], 2019: ["StyleGAN photorealistic faces [24]"]}
years = sorted(set(ML) | set(DL))
LS = 0.34                                   # line spacing (data units)
rows = [max(len(ML.get(y, [])), len(DL.get(y, []))) for y in years]
H = sum(r * LS + 0.16 for r in rows)
fig, ax = plt.subplots(figsize=(8.6, 5.6)); ax.axis("off"); ax.set_xlim(-4.3, 4.3); ax.set_ylim(-H - 0.15, 0.62)
ax.plot([0, 0], [0.05, -H + 0.05], color=NAVY, lw=2.2, solid_capstyle="round")
ax.text(-0.55, 0.42, "Machine learning, RL, explainability, privacy", ha="right", va="center", fontsize=9.5, color=GREEN_D, fontweight="600")
ax.text(0.55, 0.42, "Deep architectures, data and benchmarks", ha="left", va="center", fontsize=9.5, color=BLUE, fontweight="600")
y = 0
for yr, r in zip(years, rows):
    top = y - 0.08
    ax.text(0, top - LS / 2, str(yr), ha="center", va="center", fontsize=9, color=NAVY, fontweight="600", zorder=5,
            bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=NAVY, lw=1.0))
    for side, items, col in [(-1, ML.get(yr, []), GREEN_D), (1, DL.get(yr, []), BLUE)]:
        for k, t in enumerate(items):
            yy = top - LS / 2 - k * LS
            ax.plot([side * 0.42, side * 0.55], [yy, yy], color=col, lw=1.0)
            ax.plot([side * 0.55], [yy], "o", color=col, ms=4)
            ax.text(side * 0.66, yy, t, ha="right" if side < 0 else "left", va="center", fontsize=9, color=NAVY)
    y -= r * LS + 0.16
save(fig, SLUG, "fig1-timeline")

# Figure 2 — CNN, LSTM cell and Transformer encoder block
fig, axs = plt.subplots(1, 3, figsize=(9.2, 4.9), gridspec_kw=dict(wspace=0.06, width_ratios=[1, 1.15, 1]))
for a in axs: a.axis("off"); a.set_xlim(0, 4); a.set_ylim(0, 6.2)
# (a) CNN
a = axs[0]; a.set_title("(a) Convolutional network", fontsize=10.5)
def stack(a, x, y, w, h, k, fc, ec, dx=0.09):
    for j in range(k - 1, -1, -1):
        a.add_patch(Rectangle((x - w / 2 + j * dx, y - h / 2 + j * dx), w, h, fc=fc, ec=ec, lw=1.0))
stack(a, 2.0, 0.72, 1.9, 0.78, 1, "#F3F6FA", "#9AB0C8"); a.text(2.0, 0.62, "Input image $I$", ha="center", va="center", fontsize=9, color=NAVY)
a.add_patch(Rectangle((1.2, 0.8), 0.28, 0.2, fc="none", ec=ORANGE, lw=1.6)); a.text(0.5, 0.9, "kernel $K$", fontsize=9, color="#B4410C", ha="center")
stack(a, 2.0, 2.0, 1.0, 0.5, 4, DLF, DLE); a.text(3.25, 2.1, "conv,\nEq. (4):\nshared\nfilter", fontsize=9, color=NAVY, ha="center", va="center")
stack(a, 2.0, 3.05, 0.7, 0.36, 5, DLF, DLE, dx=0.07); a.text(3.25, 3.1, "pool +\nconv", fontsize=9, color=NAVY, ha="center", va="center")
stack(a, 2.0, 3.95, 0.42, 0.24, 6, DLF, DLE, dx=0.055); a.text(3.25, 4.0, "pool", fontsize=9, color=NAVY, ha="center", va="center")
box(a, 2.0, 4.85, 2.1, 0.44, "Fully connected", fc="#EEF1F5", ec="#A9B6C6", fs=9)
box(a, 2.0, 5.65, 2.3, 0.5, r"$p_\theta(y \mid x)$, Eq. (1)", fc=NAVY, ec=NAVY, tc="white", fs=9)
for y0, y1 in [(1.11, 1.68), (2.33, 2.78), (3.32, 3.75), (4.22, 4.63), (5.06, 5.39)]: arrow(a, (2.0, y0), (2.0, y1))
# (b) LSTM cell
a = axs[1]; a.set_title("(b) LSTM cell, one time step", fontsize=10.5); a.set_xlim(0, 4.75)
a.add_patch(FancyBboxPatch((0.3, 2.0), 4.15, 3.1, boxstyle="round,pad=0,rounding_size=0.12", fc="#FAFBFD", ec="#9AB0C8", lw=1.2))
yc = 4.55
a.plot([0.0, 4.6], [yc, yc], color=GREEN_D, lw=2.4, zorder=1)
a.text(0.02, yc + 0.18, "$c_{t-1}$", fontsize=9.5, color=GREEN_D, va="bottom"); a.text(4.73, yc + 0.18, "$c_t$", fontsize=9.5, color=GREEN_D, va="bottom", ha="right")
arrow(a, (4.4, yc), (4.75, yc), col=GREEN_D, lw=2.0)
def op(a, x, y, s, col=NAVY):
    a.add_patch(Circle((x, y), 0.19, fc="white", ec=col, lw=1.4, zorder=4)); a.text(x, y, s, ha="center", va="center", fontsize=10, color=col, zorder=5)
op(a, 0.95, yc, "⊙", GREEN_D); op(a, 2.25, yc, "+", GREEN_D)
gates = [(0.95, r"$f_t$: $\sigma$", 0.66), (1.8, r"$i_t$: $\sigma$", 0.66), (2.72, r"$\tilde c_t$: tanh", 0.98), (3.65, r"$o_t$: $\sigma$", 0.66)]
for x, lab, w in gates:
    t = "tanh" in lab
    box(a, x, 2.55, w, 0.46, lab, fc=DLF if t else "#FBE6D8", ec=BLUE if t else ORANGE, fs=9)
arrow(a, (0.95, 2.78), (0.95, yc - 0.19))
op(a, 2.25, 3.55, "⊙")
arrow(a, (1.8, 2.78), (2.12, 3.42)); arrow(a, (2.72, 2.78), (2.38, 3.42)); arrow(a, (2.25, 3.74), (2.25, yc - 0.19))
# output path
a.plot([3.65, 3.65], [yc, 4.15], color=GREEN_D, lw=1.2)
box(a, 3.65, 3.92, 0.6, 0.36, "tanh", fc=DLF, ec=BLUE, fs=9)
op(a, 4.12, 3.25, "⊙"); arrow(a, (3.8, 3.75), (4.02, 3.4)); arrow(a, (3.75, 2.78), (3.98, 3.12))
a.plot([4.12, 4.12], [3.06, 1.5], color=NAVY, lw=1.2); arrow(a, (4.12, 1.5), (4.75, 1.5))
a.text(4.73, 1.62, "$h_t$", fontsize=9.5, color=NAVY, ha="right", va="bottom")
# inputs
a.plot([0.0, 3.65], [1.75, 1.75], color=NAVY, lw=1.2)
for x, _, _ in gates: arrow(a, (x, 1.75), (x, 2.32))
a.text(0.02, 1.65, "$h_{t-1}$, $x_t$", fontsize=9.5, color=NAVY, va="top")
a.text(2.37, 0.75, r"Eq. (5): $c_t = f_t \odot c_{t-1} + i_t \odot \tilde c_t$" + "\nadditive path lets gradients\nflow across many steps", ha="center", va="center", fontsize=9, color=GREEN_D)
# (c) Transformer encoder block
a = axs[2]; a.set_title("(c) Transformer encoder block", fontsize=10.5); a.set_xlim(0, 4.3)
a.add_patch(FancyBboxPatch((0.08, 1.5), 4.14, 3.55, boxstyle="round,pad=0,rounding_size=0.12", fc="#FAFBFD", ec="#9AB0C8", lw=1.2, ls="--"))
a.text(4.16, 1.6, "× N", fontsize=9.5, color=NAVY, ha="right", va="bottom", fontweight="600")
XC, BW = 2.3, 3.0
box(a, XC, 0.5, 3.6, 0.72, "Token embeddings\n+ positional encoding", fc="#F3F6FA", ec="#9AB0C8", fs=9)
box(a, XC, 2.25, BW, 0.72, "Multi-head self-\nattention, Eq. (6)", fc="#FBE6D8", ec=ORANGE, fs=9)
box(a, XC, 3.05, BW, 0.44, "Add & LayerNorm", fc=MLF, ec=GREEN_D, fs=9)
box(a, XC, 3.8, BW, 0.5, "Feed-forward net", fc=DLF, ec=BLUE, fs=9)
box(a, XC, 4.55, BW, 0.44, "Add & LayerNorm", fc=MLF, ec=GREEN_D, fs=9)
box(a, XC, 5.68, BW, 0.72, "Contextual token\nrepresentations", fc=NAVY, ec=NAVY, tc="white", fs=9)
arrow(a, (XC, 0.86), (XC, 1.89)); arrow(a, (XC, 2.61), (XC, 2.83)); arrow(a, (XC, 3.27), (XC, 3.55)); arrow(a, (XC, 4.05), (XC, 4.33)); arrow(a, (XC, 4.77), (XC, 5.32))
for y0, y1 in [(1.72, 3.05), (3.4, 4.55)]:
    a.plot([XC, 0.5, 0.5], [y0, y0, y1], color=GREEN_D, lw=1.2); arrow(a, (0.5, y1), (XC - BW / 2, y1), col=GREEN_D)
a.text(0.38, 2.4, "residual", fontsize=9, color=GREEN_D, rotation=90, ha="right", va="center")
save(fig, SLUG, "fig2-architectures")
print("mldl figures done")
