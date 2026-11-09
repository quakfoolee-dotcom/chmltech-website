"""Figures for: AI Operating Systems — A Reference Architecture and Governance Model for Enterprise AI."""
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from style import *

SLUG = "ai-operating-systems-architecture-and-governance-for-enterprise-ai"
TXT = "#4A5568"


def box(ax, x, y, w, h, text="", fc=LIGHT, ec="#9AB0C8", tc=NAVY, fs=9.2, weight="normal", r=0.06, lw=1.2, ls="-", ha="center"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, ls=ls))
    if text:
        tx = x if ha == "center" else x - w / 2 + 0.15
        ax.text(tx, y, text, ha=ha, va="center", fontsize=fs, color=tc, fontweight=weight, linespacing=1.25)


def arrow(ax, p, q, col=NAVY, lw=1.2, cs="arc3", ms=10, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, color=col, lw=lw, connectionstyle=cs, shrinkA=0, shrinkB=0, ls=ls))


# Figure 1 — ten-layer reference architecture (Table 1): six stacked layers and four cross-cutting layers
fig, ax = plt.subplots(figsize=(9.2, 5.0)); ax.axis("off"); ax.set_xlim(0, 11); ax.set_ylim(0, 6.3)
L = [("Workflow orchestration", "state machines, queues, retries, human-approval gates"),
     ("Agent and tool", "tool registry with schemas, ReAct-style loops, sandboxes"),
     ("Memory", "session state, episodic and semantic stores, retention rules"),
     ("Model access and routing", "model gateway, routers, cascades, caching, fallbacks"),
     ("Knowledge and retrieval", "hybrid search, re-ranking, access-filtered indexes"),
     ("Data and integration", "connectors, APIs, MCP servers, data contracts")]
fills = ["#E6EEF7", "#E6EEF7", "#EEF1F5", "#E4F1E0", "#E4F1E0", "#E4F1E0"]
edges = [BLUE, BLUE, "#9AB0C8", GREEN_D, GREEN_D, GREEN_D]
X0, X1 = 0.15, 6.65; xc = (X0 + X1) / 2; w = X1 - X0
box(ax, xc, 5.85, w, 0.5, "AI applications and agents (consumers of the platform)", fc="white", ec=NAVY, ls="--", fs=9.2, weight="600")
for k, ((name, mech), fc, ec) in enumerate(zip(L, fills, edges)):
    y = 5.05 - k * 0.74
    box(ax, xc, y, w, 0.62, "", fc=fc, ec=ec)
    ax.text(X0 + 0.15, y + 0.11, name, ha="left", va="center", fontsize=9.5, color=NAVY, fontweight="600")
    ax.text(X0 + 0.15, y - 0.15, mech, ha="left", va="center", fontsize=9, color=TXT)
box(ax, xc, 0.35, w, 0.5, "Systems of record: ERP, CRM, document management, email", fc="white", ec=NAVY, ls="--", fs=9.2)
V = [("Identity and permissions", "SSO, delegated tokens, RBAC/ABAC", "#FBE6D8", ORANGE),
     ("Governance", "inventory, risk assessment, model cards", "#FBE6D8", ORANGE),
     ("Evaluation and observability", "test suites, calibrated judges, traces", "#E6EEF7", NAVY),
     ("Cost control", "metering, budgets, quotas", "#E6EEF7", NAVY)]
ytop, ybot = 5.36, 0.7
for k, (name, mech, fc, ec) in enumerate(V):
    x = 7.25 + k * 1.0
    box(ax, x, (ytop + ybot) / 2, 0.86, ytop - ybot, "", fc=fc, ec=ec)
    ax.text(x - 0.13, (ytop + ybot) / 2, name, rotation=90, ha="center", va="center", fontsize=9.5, color=NAVY, fontweight="600")
    ax.text(x + 0.18, (ytop + ybot) / 2, mech, rotation=90, ha="center", va="center", fontsize=9, color=TXT)
ax.text(8.75, 5.85, "Cross-cutting layers apply\nto every request", ha="center", va="center", fontsize=9, color=NAVY, style="italic")
save(fig, SLUG, "fig1-reference-architecture")

# Figure 2 — five-stage maturity model (Table 3) as a staircase
stages = [("0", "Ad hoc", "Individual use of\npublic assistants;\nno shared capability", "Acceptable-use policy\nissued; usage\ninventoried"),
          ("1", "Managed access", "+ Single sign-on\n+ Gateway logging\n+ Data-handling\n   rules", "All model traffic\npasses through\nthe gateway"),
          ("2", "Grounded\nassistance", "+ Permission-\n   filtered\n   knowledge layer\n+ Evaluation suite", "Retrieval quality\nmeasured; no\npermission leakage"),
          ("3", "Supervised\nautomation", "+ Tool registry\n+ Orchestration\n+ Delegated identity\n+ Cost attribution", "Eqs. (2)–(4)\nreported per\nworkflow"),
          ("4", "Governed\nautonomy", "+ Policy engine\n+ Continuous\n   evaluation\n+ Incident response\n+ Management\n   system", "Audit against the\nchosen framework\npassed")]
fig, ax = plt.subplots(figsize=(9.2, 5.0)); ax.axis("off"); ax.set_xlim(0, 10.2); ax.set_ylim(-0.95, 7.2)
cols = ["#EEF1F5", "#E6EEF7", "#D7E6F3", "#C9DDEE", "#B8D2EA"]
for k, (n, name, cap, ex) in enumerate(stages):
    x0 = 0.08 + k * 2.03; h = 2.2 + k * 0.8
    ax.add_patch(FancyBboxPatch((x0, 0), 1.96, h, boxstyle="round,pad=0,rounding_size=0.06", fc=cols[k], ec=BLUE, lw=1.2))
    ax.text(x0 + 0.12, h - 0.15, f"Stage {n}", ha="left", va="top", fontsize=9, color=BLUE, fontweight="600")
    ax.text(x0 + 0.12, h - 0.48, name, ha="left", va="top", fontsize=9.8, color=NAVY, fontweight="600", linespacing=1.15)
    ax.text(x0 + 0.12, 0.15, cap, ha="left", va="bottom", fontsize=9, color=NAVY, linespacing=1.3)
    ax.text(x0 + 0.98, h + 0.12, "Exit: " + ex, ha="center", va="bottom", fontsize=9, color=TXT, style="italic", linespacing=1.2)
for x0, x1, lab, col in [(0.1, 5.9, "No tool actions: read-only use and grounding", GREEN_D), (6.1, 7.9, "Tools under\nhuman approval", ORANGE), (8.1, 9.9, "Autonomy within\npolicy", "#B4410C")]:
    ax.plot([x0, x1], [-0.22, -0.22], color=col, lw=3, solid_capstyle="butt")
    ax.text((x0 + x1) / 2, -0.33, lab, ha="center", va="top", fontsize=9, color=col, fontweight="600", linespacing=1.1)
save(fig, SLUG, "fig2-maturity")

# Figure 3 — the Section 7 invoice workflow with its controls and metrics (hypothetical example)
fig, ax = plt.subplots(figsize=(9.2, 5.2)); ax.axis("off"); ax.set_xlim(0, 11.6); ax.set_ylim(-0.1, 6.15)
steps = [(2.25, "1  Intake and\nclassification", "#EEF1F5", "#9AB0C8"), (4.0, "2  Field\nextraction\n(large model)", "#E6EEF7", BLUE),
         (5.75, "3  Validation\nvs purchase\norders", "#E6EEF7", BLUE), (7.5, "Human review\n(escalations)", "#FBE6D8", ORANGE),
         (9.25, "4  Posting by\ndeterministic\ncode", "#E4F1E0", GREEN_D)]
YS, SW = 4.95, 1.58
box(ax, 0.66, YS, 1.24, 0.95, "Supplier\ninvoice\n(untrusted)", fc="white", ec=NAVY, ls="--", fs=9)
box(ax, 10.9, YS, 1.3, 0.95, "Accounting\nsystem", fc="white", ec=NAVY, ls="--", fs=9)
for x, t, fc, ec in steps: box(ax, x, YS, SW, 0.95, t, fc=fc, ec=ec, fs=9)
xs = [1.28] + [x for st in steps for x in (st[0] - SW / 2, st[0] + SW / 2)] + [10.25]
for k in range(6):
    arrow(ax, (xs[2 * k], YS), (xs[2 * k + 1], YS), col=ORANGE if k == 3 else NAVY, ms=9)
arrow(ax, (6.0, YS + 0.48), (9.0, YS + 0.48), col=GREEN_D, cs="arc3,rad=-0.25")
ax.text(7.5, 5.9, "85% straight through", ha="center", va="center", fontsize=9, color=GREEN_D, fontweight="600")
ax.text(6.63, YS - 0.6, "15%", ha="center", va="center", fontsize=9, color="#B4410C", fontweight="600")
rel = ["r = 0.99", "r = 0.98", "r = 0.97, or\n0.9991 with retry", "not a step of R", "r = 0.99"]
cost = ["tools and infra-\nstructure $0.005\n(all steps)", "$0.0255", "$0.00075", "$2.00 each,\n$0.30 averaged", ""]
ctrl = [("Whole workflow:\nregistered with\nowner, evaluation\nsuite and model\nversion", NAVY),
        ("Reads untrusted\ndocuments, so\nholds no write-\ncapable tools", "#B4410C"),
        ("Second attempt\nwhen a checksum\nfails; code does\nthe checking", BLUE),
        ("Approval above a\nvalue threshold\nunder approver's\nown delegated\nidentity", "#B4410C"),
        ("Posts only after\nvalidation and\nany required\napproval", GREEN_D)]
ax.text(0.12, 3.98, "Reliability", ha="left", va="center", fontsize=9, color=TXT, fontweight="600")
ax.text(0.12, 3.15, "Cost per\ninvoice", ha="left", va="center", fontsize=9, color=TXT, fontweight="600")
ax.text(0.12, 1.75, "Control", ha="left", va="center", fontsize=9, color=TXT, fontweight="600")
for (x, *_), r_, c_, (t, col) in zip(steps, rel, cost, ctrl):
    ax.text(x, 3.98, r_, ha="center", va="center", fontsize=9, color=NAVY, linespacing=1.15)
    ax.text(x, 3.15, c_, ha="center", va="center", fontsize=9, color=NAVY, linespacing=1.15)
    ax.text(x, 1.75, t, ha="center", va="center", fontsize=9, color=col, linespacing=1.2)
for yy in [3.62, 2.68]: ax.plot([0.1, 11.5], [yy, yy], color="#DCE4EE", lw=0.9)
box(ax, 5.8, 0.42, 11.4, 0.8, "", fc="#EEF4FA", ec=NAVY)
ax.text(5.8, 0.6, r"Traces from every step:  $C_{\mathrm{task}}$ = (\$0.0255 + \$0.00075 + \$0.005 + \$0.30) / 0.97 ≈ \$0.34 per invoice, Eq. (2)",
        ha="center", va="center", fontsize=9, color=NAVY)
ax.text(5.8, 0.24, "A = 0.85, Eq. (3);   R = 0.932 unattended, ≈ 0.960 with the validation retry, Eq. (4)", ha="center", va="center", fontsize=9, color=NAVY)
save(fig, SLUG, "fig3-invoice-workflow")
print("aios figures done")
