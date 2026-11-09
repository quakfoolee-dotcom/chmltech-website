"""Figures for Vol. 104(3): Retrieval-Augmented Generation: Design, Evaluation and Failure Analysis."""
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from style import *

SLUG = "retrieval-augmented-generation-design-evaluation-and-failure-analysis"
FILL = "#EEF3F9"

# ---------------------------------------------------------------- Figure 1 — end-to-end pipeline with failure points
fig, ax = plt.subplots(figsize=(9.2, 5.6))
ax.set_xlim(0, 16.8); ax.set_ylim(0, 9.6); ax.axis("off")
BW, BH = 3.0, 1.35


def box(x, y, txt, ec=BLUE, fc="white", fp=None, bold=False):
    ax.add_patch(FancyBboxPatch((x - BW / 2, y - BH / 2), BW, BH, boxstyle="round,pad=0,rounding_size=0.12", facecolor=fc, edgecolor=ec, lw=1.5, zorder=3))
    ax.text(x, y - 0.07, txt, ha="center", va="center", fontsize=9, color=NAVY, zorder=4, fontweight="700" if bold else "normal", linespacing=1.15)
    if fp:
        ax.text(x + BW / 2 - 0.08, y + BH / 2 + 0.06, fp, ha="right", va="bottom", fontsize=8.8, color="white", fontweight="700", zorder=5,
                bbox=dict(boxstyle="round,pad=0.22,rounding_size=0.3", facecolor=ORANGE, edgecolor="none"))


def arr(p, q, col=NAVY, ls="-", cs="arc3"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=10, color=col, lw=1.3, ls=ls, shrinkA=0, shrinkB=0, connectionstyle=cs, zorder=2))


xs = [1.7, 5.05, 8.4, 11.75, 15.1]
# lanes
ax.add_patch(FancyBboxPatch((0.05, 6.55), 16.7, 2.95, boxstyle="round,pad=0,rounding_size=0.2", facecolor=FILL, edgecolor=LIGHT, zorder=0))
ax.add_patch(FancyBboxPatch((0.05, 0.05), 16.7, 6.2, boxstyle="round,pad=0,rounding_size=0.2", facecolor="#F2F8EC", edgecolor="#D9E8C6", zorder=0))
ax.text(0.3, 9.15, "Offline: ingestion and indexing", fontsize=10.5, color=NAVY, fontweight="700", va="center")
ax.text(0.3, 5.9, "Online: query time", fontsize=10.5, color=GREEN_D, fontweight="700", va="center")
yi = 7.65
for x, t, fp in zip(xs, ["Source documents\n(permissioned)", "Parse and extract\n(text, tables,\nscans)", "Chunk + metadata\n(section, date,\nACL)",
                         "Embed chunks\n(bi-encoder,\nEq. 3)", "Indexes:\nBM25 + ANN\n(HNSW)"], ["FP1", None, None, None, None]):
    box(x, yi, t, fp=fp)
for i in range(4):
    arr((xs[i] + BW / 2, yi), (xs[i + 1] - BW / 2, yi))
ya, yb = 4.45, 1.55
row_a = ["User query", "Query rewrite\n(HyDE,\nsub-queries)", "Hybrid retrieval\nBM25 + dense\n(ACL filter)", "Reciprocal rank\nfusion, Eq. (5)", "Re-rank top\ncandidates\n(cross-encoder)"]
fps_a = [None, "FP6", "FP2", None, None]
for x, t, fp in zip(xs, row_a, fps_a):
    box(x, ya, t, ec=GREEN_D, fp=fp, bold=(t == "User query"))
for i in range(4):
    arr((xs[i] + BW / 2, ya), (xs[i + 1] - BW / 2, ya))
row_b = [(15.1, "Context assembly\n(top-k, order,\nbudget)", "FP3"), (11.75, "Generation (LLM)\nwith citations", "FP4–7"),
         (8.4, "Grounding check\n(faithfulness,\nEq. 8)", None), (5.05, "Cited answer\nor abstention", None)]
for x, t, fp in row_b:
    box(x, yb, t, ec=GREEN_D, fp=fp, bold=t.startswith("Cited"))
arr((15.1, ya - BH / 2), (15.1, yb + BH / 2))
for i in range(3):
    arr((row_b[i][0] - BW / 2, yb), (row_b[i + 1][0] + BW / 2, yb))
# index feeds hybrid retrieval (elbow)
ax.plot([15.1, 15.1, 8.4, 8.4], [yi - BH / 2, 5.95, 5.95, 5.45], color=BLUE, lw=1.3, zorder=2, ls=(0, (4, 2)))
arr((8.4, 5.45), (8.4, ya + BH / 2), col=BLUE)
ax.text(11.75, 6.07, "indexes queried at run time", fontsize=9, color=BLUE, ha="center", va="bottom")
# failed grounding loops back
arr((8.4, yb + BH / 2), (8.4, ya - BH / 2), col=ORANGE, ls=(0, (3, 2)))
ax.text(7.7, 3.0, "retry or\nre-retrieve", fontsize=9, color=ORANGE, ha="right", va="center")
ax.text(0.3, 0.45, "FPn = failure point of Table 2 where evidence is typically lost", fontsize=9, color="#B4410C", va="center")
save(fig, SLUG, "fig1-pipeline")

# ---------------------------------------------------------------- Figure 2 — reciprocal rank fusion worked example
k = 60
bm25 = ["P7", "P2", "P9", "P4", "P1"]
dense = ["P5", "P2", "P1", "P7", "P8"]
docs = sorted(set(bm25) | set(dense))
rb = {d: bm25.index(d) + 1 for d in bm25}; rd = {d: dense.index(d) + 1 for d in dense}
sb = {d: (1 / (k + rb[d]) if d in rb else 0.0) for d in docs}; sd = {d: (1 / (k + rd[d]) if d in rd else 0.0) for d in docs}
tot = {d: sb[d] + sd[d] for d in docs}
order = sorted(docs, key=lambda d: -tot[d])
assert order[:4] == ["P2", "P7", "P1", "P5"]
fig, ax = plt.subplots(figsize=(7.6, 3.9))
ys = np.arange(len(order))[::-1]
for y, d in zip(ys, order):
    ax.barh(y, sb[d] * 1000, color=BLUE, height=0.6, label="BM25 term, 1/(60 + r)" if d == order[0] else None)
    ax.barh(y, sd[d] * 1000, left=sb[d] * 1000, color=GREEN, height=0.6, label="Dense term, 1/(60 + r)" if d == order[0] else None)
    ax.text(tot[d] * 1000 + 0.4, y, f"{tot[d]:.4f}", va="center", fontsize=9, color=NAVY)
labels = []
for i, d in enumerate(order):
    a = f"#{rb[d]}" if d in rb else "–"; b = f"#{rd[d]}" if d in rd else "–"
    labels.append(f"{i + 1}. {d}   BM25 {a}, dense {b}")
ax.set_yticks(ys); ax.set_yticklabels(labels, fontsize=9.5)
ax.set_xlim(0, 38); ax.set_xlabel("RRF score × 1000, Eq. (5) with k = 60")
ax.grid(axis="y", visible=False)
ax.legend(loc="lower right", fontsize=9)
ax.set_title("Fused ranking (top to bottom)", loc="left", fontsize=10.5)
save(fig, SLUG, "fig2-rrf")
print("RRF:", [(d, round(tot[d], 5)) for d in order])

# ---------------------------------------------------------------- Figure 3 — recall@k and nDCG@k for two orderings
relA = [0, 1, 0, 0, 2, 0, 0, 0, 1, 0]    # first-stage hybrid list (hypothetical graded judgments)
relB = [2, 1, 0, 1, 0, 0, 0, 0, 0, 0]    # same ten candidates after re-ranking
assert sorted(relA) == sorted(relB)
nrel = sum(r > 0 for r in relA)
ideal = sorted(relA, reverse=True)
def dcg(rel, kk): return sum((2 ** r - 1) / np.log2(i + 2) for i, r in enumerate(rel[:kk]))
def recall(rel, kk): return sum(r > 0 for r in rel[:kk]) / nrel
K = np.arange(1, 11)
rec = {n: [recall(r, kk) for kk in K] for n, r in [("A", relA), ("B", relB)]}
nd = {n: [dcg(r, kk) / dcg(ideal, kk) for kk in K] for n, r in [("A", relA), ("B", relB)]}
fig = plt.figure(figsize=(9.0, 4.9))
gs = fig.add_gridspec(2, 2, height_ratios=[0.62, 2.2], hspace=0.38, wspace=0.28)
st = fig.add_subplot(gs[0, :]); st.axis("off"); st.set_xlim(-2.6, 10.2); st.set_ylim(-0.1, 2.3)
cmap = {0: "white", 1: "#B9DCF2", 2: BLUE}
for row, (name, rel) in enumerate([("A: hybrid retrieval", relA), ("B: after re-ranking", relB)]):
    y = 1.25 - row * 1.15
    st.text(-0.15, y + 0.4, name, ha="right", va="center", fontsize=9.5, color=NAVY, fontweight="600")
    for i, r in enumerate(rel):
        st.add_patch(FancyBboxPatch((i + 0.06, y), 0.88, 0.8, boxstyle="round,pad=0,rounding_size=0.08", facecolor=cmap[r], edgecolor="#9AA8BA", lw=0.8))
        if r: st.text(i + 0.5, y + 0.4, str(r), ha="center", va="center", fontsize=9, color="white" if r == 2 else NAVY, fontweight="700")
for i in range(10):
    st.text(i + 0.5, 2.18, str(i + 1), ha="center", va="center", fontsize=9, color="#4A5568")
st.text(10.15, 2.18, "rank", ha="left", va="center", fontsize=9, color="#4A5568")
a1 = fig.add_subplot(gs[1, 0]); a2 = fig.add_subplot(gs[1, 1])
for ax_, d, ttl, yl in [(a1, rec, "(a) Recall@k, Eq. (6)", "Recall@k"), (a2, nd, "(b) nDCG@k, Eq. (7)", "nDCG@k")]:
    ax_.plot(K, d["A"], color=ORANGE, marker="o", ms=4, label="A: hybrid retrieval")
    ax_.plot(K, d["B"], color=BLUE, marker="s", ms=4, label="B: after re-ranking")
    ax_.set_xticks(K); ax_.set_ylim(0, 1.08); ax_.set_xlabel("Cutoff k"); ax_.set_ylabel(yl); ax_.set_title(ttl)
    ax_.axvline(5, color=GREY, ls="--", lw=1)
a1.text(5.2, 0.08, "k passed to\ngenerator = 5", fontsize=9, color="#4A5568")
a2.legend(loc="lower right", fontsize=9)
for kk in (5,):
    a1.annotate(f"{rec['A'][kk - 1]:.2f}", (kk, rec["A"][kk - 1]), xytext=(-24, 6), textcoords="offset points", fontsize=9, color=ORANGE)
    a1.annotate(f"{rec['B'][kk - 1]:.2f}", (kk, rec["B"][kk - 1]), xytext=(-24, 6), textcoords="offset points", fontsize=9, color=BLUE)
    a2.annotate(f"{nd['A'][kk - 1]:.2f}", (kk, nd["A"][kk - 1]), xytext=(6, -12), textcoords="offset points", fontsize=9, color=ORANGE)
    a2.annotate(f"{nd['B'][kk - 1]:.2f}", (kk, nd["B"][kk - 1]), xytext=(6, -12), textcoords="offset points", fontsize=9, color=BLUE)
save(fig, SLUG, "fig3-retrieval-metrics")
print("recall@5", rec["A"][4], rec["B"][4], "nDCG@5", round(nd["A"][4], 3), round(nd["B"][4], 3), "nDCG@10", round(nd["A"][9], 3), round(nd["B"][9], 3),
      "MRR A,B", 1 / (relA.index(1) + 1), 1.0)
