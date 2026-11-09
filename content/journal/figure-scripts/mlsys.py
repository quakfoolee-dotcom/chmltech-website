"""Figures for Vol. 104: Designing Machine Learning Systems: From Problem Framing to Production."""
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from style import *

SLUG = "designing-machine-learning-systems-from-problem-framing-to-production"

# ---------------------------------------------------------------- Figure 1 — life-cycle loop with feedback paths
fig, ax = plt.subplots(figsize=(9.2, 4.7))
ax.set_xlim(0, 16); ax.set_ylim(0.6, 8.8); ax.axis("off")
BW, BH = 3.3, 1.55


def box(x, y, title, sub, ec=BLUE, fc="white"):
    ax.add_patch(FancyBboxPatch((x - BW / 2, y - BH / 2), BW, BH, boxstyle="round,pad=0,rounding_size=0.14", facecolor=fc, edgecolor=ec, lw=1.6, zorder=3))
    ax.text(x, y + 0.36, title, ha="center", va="center", fontsize=9.8, color=NAVY, fontweight="700", zorder=4)
    ax.text(x, y - 0.25, sub, ha="center", va="center", fontsize=9, color="#4A5568", zorder=4, linespacing=1.15)


def arr(p, q, col=NAVY, ls="-", rad=0.0, lw=1.4):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11, color=col, lw=lw, ls=ls, shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}", zorder=2))


xs = [2.0, 6.0, 10.0, 14.0]; yt, yb = 6.6, 1.5
top = [("1  Problem framing", "decision, error costs,\nnon-ML baseline (§2–3)"), ("2  Data", "labels, imbalance,\nleakage checks (§4)"),
       ("3  Features", "shared train/serve\ndefinitions (§5)"), ("4  Training", "baseline first; nested\nCV for selection (§6)")]
bot = [("5  Evaluation", "metrics, calibration,\nA/B or shadow (§7–8)"), ("6  Deployment", "shadow → canary →\nrollout; rollback (§9)"),
       ("7  Monitoring", "data quality, drift,\ndelayed labels (§10)"), ("8  Retraining", "scheduled or\ndetector-triggered (§10)")]
for x, (t, s) in zip(xs, top):
    box(x, yt, t, s, fc="#F4F8FC")
for x, (t, s) in zip(xs[::-1], bot):
    box(x, yb, t, s, ec=GREEN_D, fc="#F5FAEF")
for i in range(3):
    arr((xs[i] + BW / 2, yt), (xs[i + 1] - BW / 2, yt))
    arr((xs[::-1][i] - BW / 2, yb), (xs[::-1][i + 1] + BW / 2, yb))
arr((14.0, yt - BH / 2), (14.0, yb + BH / 2))
# main loop closes: retraining -> data
arr((2.0 + 0.6, yb + BH / 2), (6.0 - 0.6, yt - BH / 2), col=NAVY)
ax.text(3.55, 4.05, "new data\nwindow", fontsize=9, color=NAVY, ha="right", va="center")
# feedback paths (dashed)
FB = dict(color=ORANGE, lw=1.4, ls=(0, (4, 2.5)), zorder=2)
ax.plot([14.0 + BW / 2, 15.9, 15.9, 2.0], [yb, yb, 8.25, 8.25], **FB)
arr((2.0, 8.25), (2.0, yt + BH / 2), col=ORANGE, ls=(0, (4, 2.5)))
ax.text(9.0, 8.32, "fails to beat the baseline or move the business metric → reframe or stop", fontsize=9, color="#B4410C", ha="center", va="bottom")
arr((6.0, yb + BH / 2), (6.0, yt - BH / 2), col=ORANGE, ls=(0, (4, 2.5)))
ax.text(6.15, 4.3, "data-quality alerts,\nlabel issues", fontsize=9, color="#B4410C", ha="left", va="center")
save(fig, SLUG, "fig1-lifecycle")

# ---------------------------------------------------------------- Figure 2 — threshold trade-off on a synthetic imbalanced set
rng = np.random.default_rng(7)
n_neg, n_pos = 1900, 100                       # 5% prevalence (synthetic)
s = np.r_[rng.beta(2.2, 6.0, n_neg), rng.beta(5.0, 2.6, n_pos)]; y = np.r_[np.zeros(n_neg), np.ones(n_pos)]
T = np.linspace(0.02, 0.98, 481)
def pr(t):
    p = s >= t; TP = np.sum(p & (y == 1)); FP = np.sum(p & (y == 0)); FN = np.sum(~p & (y == 1))
    P = TP / (TP + FP) if TP + FP else 1.0; R = TP / (TP + FN); F = 2 * P * R / (P + R) if P + R else 0.0
    return P, R, F, TP, FP, FN
M = np.array([pr(t)[:3] for t in T]); Pc, Rc, Fc = M.T
auc = np.mean(s[y == 1][:, None] > s[y == 0][None, :])          # Eq. (3)
cost = np.array([pr(t)[4] * 1 + pr(t)[5] * 20 for t in T])     # synthetic cost: a missed positive costs 20 false alarms
t05 = 0.5; tF = T[Fc.argmax()]; tC = T[cost.argmin()]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.9), gridspec_kw=dict(wspace=0.3))
a1.plot(T, Pc, color=BLUE, label="Precision"); a1.plot(T, Rc, color=GREEN_D, label="Recall"); a1.plot(T, Fc, color=NAVY, ls="--", lw=1.8, label=r"$F_1$")
marks = [(tC, "cost-based", ORANGE), (tF, r"max $F_1$", NAVY), (t05, "default 0.5", GREY)]
for t, lab, col in marks:
    a1.axvline(t, color=col, lw=1.2, ls=":")
a1.text(tC - 0.015, 1.07, f"cost\n{tC:.2f}", color=ORANGE, fontsize=9, ha="right", va="top")
a1.text(tF + 0.015, 1.07, f"max F₁\n{tF:.2f}", color=NAVY, fontsize=9, ha="left", va="top")
a1.text(t05 + 0.008, 0.03, "default 0.50", color="#4A5568", fontsize=9, ha="left", va="bottom", rotation=90)
a1.set_xlim(0, 1); a1.set_ylim(0, 1.08); a1.set_xlabel("Decision threshold on score"); a1.set_ylabel("Metric value, Eq. (2)")
a1.set_title("(a) Metrics against threshold"); a1.legend(loc="center left", fontsize=9, bbox_to_anchor=(0.02, 0.6))
a2.plot(Rc, Pc, color=BLUE)
a2.axhline(n_pos / (n_pos + n_neg), color=GREY, ls="--", lw=1.2)
a2.text(0.02, 0.08, f"no-skill baseline = prevalence {n_pos / (n_pos + n_neg):.0%}", color="#4A5568", fontsize=9)
for t, lab, col in marks:
    P_, R_ = pr(t)[:2]; a2.plot([R_], [P_], "o", color=col, ms=7, mfc="white", mew=2, zorder=5)
    ty = {"cost-based": 0.17, "default 0.5": 0.33}.get(lab, 0.5)
    a2.annotate(f"{lab}: P {P_:.2f}, R {R_:.2f}", (R_, P_), xytext=(0.04, ty), textcoords="data", ha="left", va="center", fontsize=9,
                color=col if col != GREY else "#4A5568", arrowprops=dict(arrowstyle="-", color=col, lw=0.8, shrinkB=5, relpos=(1, 0.5)))
a2.text(0.97, 0.97, f"ROC-AUC (Eq. 3) = {auc:.2f}", ha="right", va="top", fontsize=9.5, color=NAVY, transform=a2.transAxes)
a2.set_xlim(0, 1.02); a2.set_ylim(0, 1.05); a2.set_xlabel("Recall"); a2.set_ylabel("Precision"); a2.set_title("(b) Precision–recall curve")
save(fig, SLUG, "fig2-threshold")
info2 = dict(auc=round(auc, 3), tC=round(tC, 2), tF=round(tF, 2), at05=[round(v, 2) for v in pr(0.5)[:3]], atF=[round(v, 2) for v in pr(tF)[:3]], atC=[round(v, 2) for v in pr(tC)[:3]])
print("fig2", info2)

# ---------------------------------------------------------------- Figure 3 — PSI drift monitoring on synthetic data
rng = np.random.default_rng(11)
ref = rng.normal(0, 1, 10000)
edges = np.quantile(ref, np.linspace(0, 1, 11)); edges[0], edges[-1] = -np.inf, np.inf
e = np.histogram(ref, edges)[0] / ref.size
def psi(x):
    a = np.histogram(x, edges)[0] / x.size
    v = np.sum((a - e) * np.log(a / e))
    assert abs(v - (np.sum(a * np.log(a / e)) + np.sum(e * np.log(e / a)))) < 1e-12   # PSI = KL(A||E) + KL(E||A)
    return v, a
n = 2000; weeks = np.arange(1, 17)
shift = np.where(weeks <= 4, 0.0, 0.05 * (weeks - 4))           # stable for 4 weeks, then incremental drift of 0.05 SD per week
vals, last = [], None
for w, m in zip(weeks, shift):
    v, a = psi(rng.normal(m, 1, n)); vals.append(v); last = a
vals = np.array(vals)
null = np.array([psi(rng.normal(0, 1, n))[0] for _ in range(3000)])
q99 = np.quantile(null, 0.99)
w_null = weeks[np.argmax(vals > q99)]; w10 = weeks[np.argmax(vals > 0.10)]; w25 = weeks[np.argmax(vals > 0.25)] if (vals > 0.25).any() else None
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.9), gridspec_kw=dict(wspace=0.3, width_ratios=[1, 1.25]))
b = np.arange(10)
a1.bar(b - 0.2, e * 100, width=0.4, color=LIGHT, edgecolor="#B9C7D8", label="Reference (expected, eᵢ)")
a1.bar(b + 0.2, last * 100, width=0.4, color=BLUE, label=f"Week 16 (actual, aᵢ)")
a1.set_xticks(b); a1.set_xticklabels([str(i + 1) for i in b]); a1.set_xlabel("Bin (reference deciles)"); a1.set_ylabel("Share of observations (%)")
a1.set_title(f"(a) Bin shares, week 16: PSI = {vals[-1]:.2f}"); a1.grid(axis="x", visible=False); a1.set_ylim(0, 28)
a1.legend(loc="upper left", fontsize=9)
a2.plot(weeks, vals, color=NAVY, marker="o", ms=4, label="Weekly PSI, Eq. (6)")
a2.axhspan(0, q99, color="#E9F4DC", zorder=0)
a2.axhline(q99, color=GREEN_D, lw=1.4, ls="--")
a2.text(0.8, 0.045, f"no-drift 99th pct. = {q99:.3f}", color=GREEN_D, fontsize=9, va="bottom", ha="left")
for v, lab in [(0.10, "rule of thumb 0.10"), (0.25, "rule of thumb 0.25")]:
    a2.axhline(v, color=ORANGE, lw=1.2, ls=":"); a2.text(0.8, v + 0.006, lab, color="#B4410C", fontsize=9, va="bottom")
a2.axvline(4.5, color=GREY, lw=1, ls="-"); a2.text(4.7, 0.33, "drift starts", color="#4A5568", fontsize=9, va="top")
for w, col in [(w_null, GREEN_D), (w10, ORANGE)] + ([(w25, ORANGE)] if w25 else []):
    a2.plot([w], [vals[w - 1]], "o", ms=9, mfc="none", mec=col, mew=2, zorder=5)
a2.set_xlim(0.5, 16.5); a2.set_ylim(0, 0.34); a2.set_xticks([1, 4, 8, 12, 16]); a2.set_xlabel("Week"); a2.set_ylabel("PSI")
a2.set_title("(b) PSI over time against alert thresholds")
save(fig, SLUG, "fig3-psi-drift")
print("fig3", dict(q99=round(q99, 4), w_null=int(w_null), w10=int(w10), w25=w25, psi=[round(v, 3) for v in vals], shift16=shift[-1]))
