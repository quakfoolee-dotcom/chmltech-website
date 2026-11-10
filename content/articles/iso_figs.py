"""Diagrams for the ISO 9001 article series (V4.20). One SVG per article, written to articles/figs/<slug>.svg."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "jfigs"))
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
from style import NAVY, BLUE, GREEN_D, ORANGE, GREY, LIGHT
import style  # noqa: sets rcParams

OUT = os.path.join(HERE, "..", "articles", "figs"); os.makedirs(OUT, exist_ok=True)
INK = "#4A5568"; PALE = "#EEF3F9"; SKY = "#CFE6F3"; GREENF = "#E4F1D3"; ORANGEF = "#FBE6D8"; WHITE = "white"


def save(fig, slug):
    fig.savefig(os.path.join(OUT, slug + ".svg"), format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off"); return fig, ax


def box(ax, x0, y0, w, h, txt, fill=LIGHT, tc=NAVY, fs=9, bold=False, ec="#9AB0C8", lw=1):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.25,rounding_size=1.0", fc=fill, ec=ec, lw=lw))
    ax.text(x0 + w / 2, y0 + h / 2, txt, ha="center", va="center", fontsize=fs, color=tc, fontweight="600" if bold else "normal", linespacing=1.25)


def arr(ax, p, q, col=NAVY, lw=1.6, style="-|>", ms=11):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=col, lw=lw, shrinkA=0, shrinkB=0))


# 1 — clause map: where the 2026 edition changed
fig, ax = canvas(8.4, 5.4)
cl = [("3", "Terms and definitions", 1, "The harmonized terms are now listed in the standard itself"),
      ("4", "Context of the organization", 1, "Climate change wording from the 2024 amendment is built in"),
      ("5", "Leadership", 2, "Quality culture and ethical behaviour; policy tied to strategy"),
      ("6", "Planning", 2, "Risks and opportunities split; planning of changes reinforced"),
      ("7", "Support", 1, "Awareness now covers quality culture and ethical behaviour"),
      ("8", "Operation", 0, "Wording and layout only"),
      ("9", "Performance evaluation", 0, "Minimal change"),
      ("10", "Improvement", 1, "Continual improvement requirements consolidated"),
      ("A", "Annex A (guidance)", 2, "Rewritten and expanded, clause by clause; adds no requirements")]
col = {0: (PALE, "#9AB0C8"), 1: (SKY, BLUE), 2: (ORANGEF, ORANGE)}
for k, (n, name, lvl, t) in enumerate(cl):
    y0 = 84 - k * 8.6; f_, e_ = col[lvl]
    ax.add_patch(FancyBboxPatch((1, y0), 98, 6.6, boxstyle="round,pad=0.2,rounding_size=0.8", fc=f_, ec=e_, lw=1.1))
    ax.text(5, y0 + 3.3, n, ha="center", va="center", fontsize=11.5, color=NAVY, fontweight="600")
    ax.text(10, y0 + 3.3, name, ha="left", va="center", fontsize=9, color=NAVY, fontweight="600")
    ax.text(38, y0 + 3.3, t, ha="left", va="center", fontsize=8.4, color=INK)
for i, (lab, lvl) in enumerate([("Main changes", 2), ("Smaller changes", 1), ("Largely unchanged", 0)]):
    f_, e_ = col[lvl]; xx = 14 + i * 27
    ax.add_patch(FancyBboxPatch((xx, 3.2), 3.4, 4, boxstyle="round,pad=0.2,rounding_size=0.8", fc=f_, ec=e_, lw=1.2))
    ax.text(xx + 5.6, 5.2, lab, ha="left", va="center", fontsize=9, color=NAVY)
ax.text(50, 96.5, "ISO 9001:2026 compared with ISO 9001:2015, by clause", ha="center", va="center", fontsize=10.5, color=NAVY, fontweight="600")
save(fig, "iso-9001-2026-what-changed-from-2015")

# 2 — transition timeline
fig, ax = canvas(8.8, 4.4)
ax.plot([5, 95], [62, 62], color=NAVY, lw=2.2)
ms = [(8, "16 Sep 2026", "ISO 9001:2026\npublished"), (30, "During 2027", "Certification bodies\naccredited for\nthe new edition"),
      (58, "Spring 2028", "New certificates\nissued to the\n2026 edition only"), (92, "30 Sep 2029", "2015 certificates\nstop being valid")]
for xx, d, t in ms:
    ax.add_patch(Circle((xx, 62), 1.5, fc=ORANGE if xx == 92 else BLUE, ec="white", lw=1.5, zorder=4))
    ax.text(xx, 70, d, ha="center", va="bottom", fontsize=9.5, color=NAVY, fontweight="600")
    ax.text(xx, 88, t, ha="center", va="center", fontsize=8.3, color=INK, linespacing=1.2)
steps = [(5, 17, "1  Read the standard\nand run a gap\nassessment"), (24, 17, "2  Update policy,\nrisk and change\nplanning"), (43, 17, "3  Train leaders,\nstaff and internal\nauditors"),
         (62, 16, "4  Internal audit and\nmanagement review\nto the new edition"), (80, 15, "5  Transition audit\nwith your\ncertification body")]
for x0, wd, t in steps:
    box(ax, x0, 22, wd, 24, t, fill=GREENF, ec=GREEN_D, fs=8.2)
for x0 in (22.3, 41.3, 60.3, 78.3):
    arr(ax, (x0 - 0.2, 34), (x0 + 1.6, 34), GREEN_D, lw=1.4, ms=9)
ax.text(5, 52, "Your work", ha="left", va="center", fontsize=9, color=GREEN_D, fontweight="600")
ax.text(50, 9, "Aim to finish step 5 at a scheduled surveillance or recertification audit, well before the deadline.", ha="center", va="center", fontsize=8.6, color=INK)
save(fig, "iso-9001-2026-transition-plan")

# 3 — certification path for a small business
fig, ax = canvas(8.8, 4.2)
r1 = ["Decide scope\nand who leads", "Gap assessment\nagainst the\nstandard", "Close the gaps:\nfix processes,\nwrite only what\nyou need", "Run the system\nand keep records\nfor 2–3 months", "Internal audit\nand management\nreview"]
r2 = ["Stage 1 audit\nreadiness and\ndocuments", "Stage 2 audit\nthe system\nin use", "Certificate\nvalid 3 years", "Surveillance\naudits in\nyears 1 and 2", "Recertification\naudit in year 3"]
for k, t in enumerate(r1):
    x0 = 1 + k * 20; box(ax, x0, 60, 17.5, 28, t, fill=SKY, ec=BLUE, fs=8.2)
    if k < 4: arr(ax, (x0 + 18.1, 74), (x0 + 19.5, 74), BLUE, lw=1.4, ms=9)
for k, t in enumerate(r2):
    x0 = 1 + k * 20; box(ax, x0, 14, 17.5, 28, t, fill=GREENF if k < 3 else PALE, ec=GREEN_D if k < 3 else "#9AB0C8", fs=8.2)
    if k < 4: arr(ax, (x0 + 18.1, 28), (x0 + 19.5, 28), GREEN_D, lw=1.4, ms=9)
ax.plot([89.7, 97.5, 97.5], [60, 54, 51], color=NAVY, lw=0); arr(ax, (89.7, 59.4), (89.7, 51), NAVY, lw=1.2, style="-", ms=1)
ax.plot([9.7, 89.7], [51, 51], color=NAVY, lw=1.2); arr(ax, (9.7, 51), (9.7, 42.8), NAVY, lw=1.2, ms=9)
ax.text(1, 94, "Your preparation", fontsize=9.5, color=BLUE, fontweight="600", va="center")
ax.text(1, 6, "Certification body", fontsize=9.5, color=GREEN_D, fontweight="600", va="center")
save(fig, "iso-9001-for-small-and-mid-sized-businesses")

# 4 — anatomy of an audit finding
fig, ax = canvas(8.8, 3.8)
st = [("Requirement", "What the\nstandard or\nprocedure says", SKY, BLUE), ("Evidence", "What you saw:\nrecord, date,\nplace, sample", SKY, BLUE), ("Gap", "The difference,\nstated as fact", ORANGEF, ORANGE),
      ("Cause", "Why the\nprocess\nallowed it", ORANGEF, ORANGE), ("Corrective\naction", "Removes the\ncause; owner\nand date", GREENF, GREEN_D), ("Verification", "Later check\nthat it has\nnot recurred", GREENF, GREEN_D)]
for k, (h, t, f, e) in enumerate(st):
    x0 = 0.8 + k * 16.6; box(ax, x0, 28, 14.6, 46, "", fill=f, ec=e, lw=1.2)
    ax.text(x0 + 7.3, 65, h, ha="center", va="center", fontsize=8.6, color=NAVY, fontweight="600", linespacing=1.15)
    ax.text(x0 + 7.3, 44, t, ha="center", va="center", fontsize=7.8, color=INK, linespacing=1.25)
    if k < 5: arr(ax, (x0 + 15.2, 51), (x0 + 16.2, 51), NAVY, lw=1.3, ms=9)
ax.text(17.4, 86, "The auditor writes", ha="center", fontsize=9.5, color=BLUE, fontweight="600"); ax.plot([1, 49.5], [81, 81], color=BLUE, lw=1.6)
ax.text(75.5, 86, "The process owner completes", ha="center", fontsize=9.5, color=GREEN_D, fontweight="600"); ax.plot([51, 99], [81, 81], color=GREEN_D, lw=1.6)
ax.text(50, 12, "A finding with the first three parts can be acted on. A finding that stops at “procedure not followed” cannot.", ha="center", va="center", fontsize=8.6, color=INK)
save(fig, "iso-9001-internal-audits-that-find-real-problems")

# 5 — risk grid with the worked examples
fig, ax = plt.subplots(figsize=(6.6, 4.6))
cols = [["#E4F1D3", "#E4F1D3", "#FFF1C9"], ["#E4F1D3", "#FFF1C9", "#FBD9C6"], ["#FFF1C9", "#FBD9C6", "#F4B8A0"]]
for i in range(3):
    for j in range(3):
        ax.add_patch(Rectangle((j, i), 1, 1, fc=cols[i][j], ec="white", lw=2))
pts = [(2.5, 2.42, "R1", "Single-source\nresin supplier"), (1.5, 2.42, "R2", "Calibration\noverdue"), (2.5, 1.42, "R3", "Key setter\nretires"), (0.5, 1.42, "R4", "Drawing revision\nmix-up"), (1.5, 0.42, "R5", "Late customer\nspec changes")]
for x, y, lab, t in pts:
    ax.add_patch(Circle((x, y + 0.2), 0.17, fc=NAVY, ec="white", lw=1.5, zorder=4))
    ax.text(x, y + 0.2, lab, ha="center", va="center", fontsize=8.5, color="white", fontweight="600", zorder=5)
    ax.text(x, y - 0.17, t, ha="center", va="center", fontsize=8, color=NAVY, linespacing=1.15)
ax.set_xlim(0, 3); ax.set_ylim(0, 3); ax.set_xticks([0.5, 1.5, 2.5]); ax.set_xticklabels(["Low", "Medium", "High"]); ax.set_yticks([0.5, 1.5, 2.5]); ax.set_yticklabels(["Low", "Medium", "High"])
ax.set_xlabel("Impact on customers or the business"); ax.set_ylabel("Likelihood"); ax.grid(False); ax.tick_params(length=0)
for s in ax.spines.values(): s.set_visible(False)
ax.set_aspect(0.62)
save(fig, "iso-9001-risk-based-thinking-in-practice")

# 6 — AI inside a quality system
fig, ax = canvas(8.8, 4.5)
uses = [("Document control", "draft, compare versions,\ncheck cross-references", "7.5"), ("Audit preparation", "checklists, sampling plans,\nevidence summaries", "9.2"),
        ("Nonconformity trends", "classify and cluster\ncomplaints and NCRs", "9.1 · 10.2"), ("Training and answers", "questions answered from\napproved documents", "7.2 · 7.3")]
for k, (h, t, c) in enumerate(uses):
    y0 = 76 - k * 21
    box(ax, 1, y0, 31, 17, "", fill=SKY, ec=BLUE, lw=1.2)
    ax.text(16.5, y0 + 12.4, h + "  (" + c + ")", ha="center", va="center", fontsize=8.8, color=NAVY, fontweight="600")
    ax.text(16.5, y0 + 5.4, t, ha="center", va="center", fontsize=7.9, color=INK, linespacing=1.2)
    arr(ax, (32.6, y0 + 8.5), (44.4, 50 + (1.5 - k) * 5), BLUE, lw=1.2, ms=9)
box(ax, 45, 30, 20, 40, "Human review\nand approval\n\nnamed owner\nchecks the output\nagainst the source", fill=ORANGEF, ec=ORANGE, fs=8.6, bold=False, lw=1.5)
arr(ax, (65.6, 50), (73.4, 50), ORANGE, lw=1.8)
box(ax, 74, 30, 25, 40, "Controlled result\n\napproved document,\naudit record or\ncorrective action\nin the QMS", fill=GREENF, ec=GREEN_D, fs=8.6, lw=1.3)
ax.text(72, 88, "Controls that apply to the AI tool itself", ha="center", va="center", fontsize=9.2, color=NAVY, fontweight="600")
ax.text(72, 80, "risk assessment (6.1) · supplier control (8.4)\ncompetence (7.2) · confidentiality · record of use", ha="center", va="center", fontsize=8, color=INK, linespacing=1.3)
ax.text(72, 14, "The AI tool prepares. A person decides.\nNothing enters the system unreviewed.", ha="center", va="center", fontsize=8.8, color=NAVY, linespacing=1.3)
save(fig, "iso-9001-and-ai-using-ai-tools-inside-a-quality-system")

# 7 — integrated management system
fig, ax = canvas(8.8, 4.6)
box(ax, 2, 6, 96, 30, "", fill=PALE, ec=NAVY, lw=1.4)
ax.text(50, 30, "Shared core: build once", ha="center", va="center", fontsize=10, color=NAVY, fontweight="600")
ax.text(50, 17.5, "context and interested parties · leadership and policy · objectives · risks and opportunities\ncompetence and awareness · communication · documented information\ninternal audit · management review · corrective action and improvement",
        ha="center", va="center", fontsize=8.3, color=INK, linespacing=1.35)
colm = [("ISO 9001\nQuality", "customer requirements\ndesign and development\nexternal providers\nrelease and nonconforming\noutputs", SKY, BLUE),
        ("ISO 14001\nEnvironment", "environmental aspects\ncompliance obligations\nlife cycle perspective\nemergency preparedness", GREENF, GREEN_D),
        ("ISO 45001\nHealth and safety", "hazard identification\nworker consultation\nand participation\nemergency preparedness\nincident investigation", ORANGEF, ORANGE)]
for k, (h, t, f, e) in enumerate(colm):
    x0 = 2 + k * 33
    box(ax, x0, 42, 30, 52, "", fill=f, ec=e, lw=1.3)
    ax.text(x0 + 15, 85, h, ha="center", va="center", fontsize=9.6, color=NAVY, fontweight="600", linespacing=1.2)
    ax.text(x0 + 15, 61, t, ha="center", va="center", fontsize=8.2, color=INK, linespacing=1.35)
    arr(ax, (x0 + 15, 41.4), (x0 + 15, 36.8), e, lw=1.6, style="<|-|>", ms=10)
save(fig, "integrated-management-system-iso-9001-14001-45001")

# 8 — management review on one page
fig, ax = canvas(8.8, 4.3)
ins = ["Actions from\nlast review", "Changes in context,\ncustomers, regulations", "Performance:\nobjectives, processes,\ncustomers, suppliers", "Audits and\nnonconformities", "Resources, risks\nand opportunities"]
for k, t in enumerate(ins):
    y0 = 78 - k * 17.5; box(ax, 1, y0, 26, 14, t, fill=SKY, ec=BLUE, fs=8.1)
    arr(ax, (27.6, y0 + 7), (37.4, 50 + (2 - k) * 4.5), BLUE, lw=1.1, ms=8)
box(ax, 38, 26, 24, 48, "Review meeting\n\n60–90 minutes\ndata sent in advance\ndecisions recorded\nin the room", fill=ORANGEF, ec=ORANGE, fs=8.8, lw=1.5)
outs = ["Improvement actions\nwith owner and date", "Changes to the\nquality system", "Resources approved\nor reallocated"]
for k, t in enumerate(outs):
    y0 = 70 - k * 24; box(ax, 73, y0, 26, 17, t, fill=GREENF, ec=GREEN_D, fs=8.3)
    arr(ax, (62.6, 50 + (1 - k) * 6), (72.4, y0 + 8.5), GREEN_D, lw=1.3, ms=9)
ax.text(14, 96, "Inputs", ha="center", fontsize=9.8, color=BLUE, fontweight="600"); ax.text(50, 80, "Decide", ha="center", fontsize=9.8, color=ORANGE, fontweight="600"); ax.text(86, 92, "Outputs", ha="center", fontsize=9.8, color=GREEN_D, fontweight="600")
ax.text(50, 12, "If no decision changes anything,\nthe review has not done its job.", ha="center", va="center", fontsize=8.6, color=INK, linespacing=1.3)
save(fig, "iso-9001-management-review-that-leadership-finds-useful")
print("iso figures written")

# 9 — document lifecycle (V4.21)
fig, ax = canvas(8.8, 4.8)
st = [(4, 62, "1  Draft", "author prepares or\nrevises; change marked", SKY, BLUE),
      (28, 62, "2  Review", "process owner checks\nit matches the work", SKY, BLUE),
      (52, 62, "3  Approve", "authorized person\nsigns; revision raised", ORANGEF, ORANGE),
      (76, 62, "4  Release", "published to the one\nmaster location", GREENF, GREEN_D),
      (76, 22, "5  Use", "current revision at the\npoint of use", GREENF, GREEN_D),
      (52, 22, "6  Change request", "anyone can raise one;\nowner decides", PALE, "#9AB0C8"),
      (28, 22, "7  Supersede", "when the new revision\nis released, old one\nwithdrawn", PALE, "#9AB0C8"),
      (4, 22, "8  Archive", "kept for the retention\nperiod, then disposed", PALE, "#9AB0C8")]
for x0, y0, h, t, f_, e_ in st:
    box(ax, x0, y0, 20, 20, "", fill=f_, ec=e_, lw=1.2)
    ax.text(x0 + 10, y0 + 14, h, ha="center", va="center", fontsize=9, color=NAVY, fontweight="600")
    ax.text(x0 + 10, y0 + 6.5, t, ha="center", va="center", fontsize=7.6, color=INK, linespacing=1.2)
for xa in (24.6, 48.6, 72.6):
    arr(ax, (xa, 72), (xa + 2.8, 72), NAVY, lw=1.4, ms=9)
arr(ax, (86, 61.4), (86, 42.6), NAVY, lw=1.4, ms=9)
for xa in (75.4, 51.4, 27.4):
    arr(ax, (xa, 32), (xa - 2.8, 32), NAVY, lw=1.4, ms=9)
ax.plot([62, 62, 14], [42.6, 50, 50], color=ORANGE, lw=1.6, ls=(0, (4, 2)))
arr(ax, (14, 50), (14, 61.4), ORANGE, lw=1.6, ms=10)
ax.text(38, 52.5, "approved change starts a new revision", ha="center", va="bottom", fontsize=8.2, color=ORANGE)
ax.text(50, 94, "One document, one owner, one current revision", ha="center", va="center", fontsize=10.5, color=NAVY, fontweight="600")
ax.text(50, 9, "Records (evidence of what was done) are not revised: they are retained, protected and eventually disposed of.", ha="center", va="center", fontsize=8.4, color=INK)
save(fig, "iso-9001-document-and-revision-control")
print("doc figure written")
