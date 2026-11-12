"""Figures for Vol. 105(4)-(6): the three agentic AI papers (V4.61). Same drawings as the review drafts, in the journal style."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
from style import *

S4 = "agent-interoperability-standards-mcp-a2a-erp-crm-plant-systems"
S5 = "agent-security-and-identity-prompt-injection-least-privilege-credentials-audit"
S6 = "agent-readiness-for-small-and-mid-sized-firms-data-process-staged-adoption"
INK = "#4A5568"; PALE = "#EEF3F9"; SKY = "#CFE6F3"; GREENF = "#E4F1D3"; ORANGEF = "#FBE6D8"; REDF = "#F8DEDB"; RED = "#C0392B"


def box(ax, x0, y0, w, h, txt, fill=LIGHT, tc=NAVY, fs=9, bold=False, ec="#9AB0C8", ls="-", lw=1, ha="center"):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.25,rounding_size=1.0", fc=fill, ec=ec, lw=lw, ls=ls))
    if txt:
        ax.text(x0 + w / 2, y0 + h / 2, txt, ha="center", va="center", fontsize=fs, color=tc, fontweight="600" if bold else "normal", linespacing=1.25)


def arr(ax, p, q, col=NAVY, lw=1.5, style="-|>", ms=11):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=col, lw=lw, shrinkA=0, shrinkB=0))


def line(ax, pts, col=NAVY, lw=1.5):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=col, lw=lw, solid_capstyle="butt")


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off"); return fig, ax


def diamond(ax, cx, cy, hw, hh, txt, fs=9):
    ax.add_patch(Polygon([(cx - hw, cy), (cx, cy + hh), (cx + hw, cy), (cx, cy - hh)], closed=True, fc=PALE, ec="#9AB0C8", lw=1))
    ax.text(cx, cy, txt, ha="center", va="center", fontsize=fs, color=NAVY, linespacing=1.2)


# =============================================================== 105(4) Figure 1 — protocol layers
fig, ax = canvas(8.8, 4.6)
for y in (66, 34):
    ax.plot([2, 98], [y, y], color="#DCE4EE", lw=1)
for y, a, b in ((83, "Agent to agent", "A2A"), (50, "Agent to tool", "MCP"), (17, "System to device", "OPC UA")):
    ax.text(2, y + 2.5, a, fontsize=10, color=NAVY, fontweight="600", va="center")
    ax.text(2, y - 4, b, fontsize=9, color=INK, va="center")
box(ax, 26, 76, 26, 14, "Plant scheduling agent", fill=SKY, bold=True, ec=BLUE, lw=1.4)
box(ax, 66, 76, 26, 14, "Supplier's order agent", fill=SKY, bold=True, ec=BLUE, lw=1.4)
arr(ax, (52.5, 83), (65.5, 83), style="<|-|>")
ax.text(59, 86.5, "task", ha="center", fontsize=8.5, color=INK)
box(ax, 22, 43, 15, 14, "MES server")
box(ax, 40, 43, 15, 14, "Historian\nserver")
box(ax, 66, 43, 26, 14, "Supplier ERP server")
arr(ax, (29.5, 75.5), (29.5, 57.5)); arr(ax, (47.5, 75.5), (47.5, 57.5)); arr(ax, (79, 75.5), (79, 57.5))
ax.text(80.5, 61.5, "supplier's systems", fontsize=8.5, color=INK, va="center")
box(ax, 38, 9, 19, 14, "PLC · SCADA", fill=PALE)
arr(ax, (47.5, 23.5), (47.5, 42.5))
ax.text(49, 33, "read-only", fontsize=8.5, color=INK, va="center")
save(fig, S4, "fig1-protocol-layers")

# =============================================================== 105(4) Figure 2 — reference architecture
fig, ax = canvas(8.8, 6.2)
box(ax, 2, 80, 64, 17, "")
ax.text(4, 93.5, "Agent hosts (MCP clients)", fontsize=9.5, color=NAVY, fontweight="600", va="center")
for x, t in ((4, "Assistant"), (25, "Maintenance\nagent"), (46, "Scheduling\nagent")):
    box(ax, x, 81.5, 18, 9, t, fill="white", fs=8.8)
box(ax, 74, 83, 24, 10, "Supplier agents", fill="white")
arr(ax, (66.5, 88), (73.5, 88)); ax.text(70, 90.5, "A2A", ha="center", fontsize=8.5, color=INK)
box(ax, 2, 57, 96, 13, "", fill=SKY, ec=BLUE, lw=1.6)
ax.text(50, 66, "MCP gateway", ha="center", va="center", fontsize=11, color=NAVY, fontweight="600")
ax.text(50, 60.5, "identity · scoped tokens · tool allow-list · audit log", ha="center", va="center", fontsize=9, color=NAVY)
arr(ax, (34, 79.5), (34, 70.5)); ax.text(35.5, 75, "MCP calls", fontsize=8.5, color=INK, va="center")
box(ax, 2, 27, 44, 20, "")
ax.text(4, 43.5, "Enterprise systems (Level 4)", fontsize=9.5, color=NAVY, fontweight="600", va="center")
box(ax, 4, 29, 19, 9, "ERP MCP\nserver", fill="white", fs=8.8); box(ax, 25, 29, 19, 9, "CRM MCP\nserver", fill="white", fs=8.8)
box(ax, 54, 27, 44, 20, "")
ax.text(56, 43.5, "Plant DMZ servers (Level 3)", fontsize=9.5, color=NAVY, fontweight="600", va="center")
for x, t in ((56, "MES"), (70, "Historian"), (84, "CMMS")):
    box(ax, x, 29, 12.5, 9, t, fill="white", fs=8.8)
arr(ax, (24, 56.5), (24, 47.5)); arr(ax, (76, 56.5), (76, 47.5))
box(ax, 54, 3, 44, 10, "PLC · SCADA · DCS (Level 2)", fill=PALE)
arr(ax, (76, 13.5), (76, 26.5)); ax.text(77.5, 20, "OPC UA, read-only", fontsize=8.5, color=INK, va="center")
ax.text(50, 8, "No agent writes to the control layer", ha="right", va="center", fontsize=8.8, color=INK, style="italic")
save(fig, S4, "fig2-reference-architecture")

# =============================================================== 105(5) Figure 1 — breaking the trifecta
fig, ax = canvas(8.8, 5.4)
ax.text(24, 97, "Before: one agent", ha="center", fontsize=10, color=INK, fontweight="600")
ax.text(74, 97, "After: split by role", ha="center", fontsize=10, color=INK, fontweight="600")
box(ax, 4, 40, 40, 51, "", fill=REDF, ec=RED, lw=1.6)
ax.text(24, 85.5, "Purchasing agent", ha="center", fontsize=10, color=NAVY, fontweight="600")
for y, t in ((70, "ERP contract prices (private)"), (57, "Supplier inbox (untrusted)"), (44, "Sends email (external)")):
    box(ax, 7, y, 34, 8.5, t, fill="white", fs=9)
ax.text(24, 31, "All three legs in one agent: one injected\nquote can leak the price list", ha="center", va="center", fontsize=8.8, color=INK)
box(ax, 56, 75, 36, 16, "", fill=GREENF, ec=GREEN_D, lw=1.6)
ax.text(74, 87.5, "Reader agent", ha="center", fontsize=10, color=NAVY, fontweight="600")
box(ax, 59, 76.5, 30, 7.5, "Supplier inbox (untrusted)", fill="white", fs=9)
arr(ax, (74, 74.5), (74, 63.5)); ax.text(75.5, 69, "summary only", fontsize=8.5, color=INK, va="center")
box(ax, 64, 54, 20, 9, "Buyer reviews", fill="white")
arr(ax, (74, 53.5), (74, 44.5))
box(ax, 56, 13, 36, 31, "", fill=GREENF, ec=GREEN_D, lw=1.6)
ax.text(74, 40, "Actor agent", ha="center", fontsize=10, color=NAVY, fontweight="600")
box(ax, 59, 26, 30, 8, "ERP contract prices (private)", fill="white", fs=9)
box(ax, 59, 15, 30, 8, "Sends approved drafts only", fill="white", fs=9)
ax.text(74, 4, "No agent holds all three legs", ha="center", fontsize=8.8, color=INK)
save(fig, S5, "fig1-trifecta-split")

# =============================================================== 105(5) Figure 2 — runtime checkpoints
fig, ax = canvas(8.8, 4.4)
box(ax, 1, 70, 17, 14, "Agent requests\na tool call")
box(ax, 23, 70, 17, 14, "Verify agent and\nuser identity")
diamond(ax, 54, 77, 10, 13, "Policy\nallows?")
diamond(ax, 80, 77, 11, 13, "High-risk or\nirreversible?")
box(ax, 45, 38, 18, 12, "Deny the call")
box(ax, 71, 38, 18, 12, "Human approval")
box(ax, 71, 6, 18, 14, "Execute with\nscoped token")
box(ax, 44, 6, 20, 14, "Write audit record", fill=SKY, ec=BLUE, lw=1.6, bold=True)
arr(ax, (18.5, 77), (22.5, 77)); arr(ax, (40.5, 77), (43.6, 77)); arr(ax, (64.2, 77), (68.6, 77))
ax.text(66.4, 80, "yes", ha="center", fontsize=8.5, color=INK)
arr(ax, (54, 63.8), (54, 50.5)); ax.text(55.5, 57, "no", fontsize=8.5, color=INK, va="center")
arr(ax, (80, 63.8), (80, 50.5)); ax.text(81.5, 57, "yes", fontsize=8.5, color=INK, va="center")
arr(ax, (80, 37.5), (80, 20.5)); ax.text(81.5, 29, "approved", fontsize=8.5, color=INK, va="center")
line(ax, [(91.2, 77), (96, 77), (96, 13)]); arr(ax, (96, 13), (89.5, 13)); ax.text(97, 57, "no", fontsize=8.5, color=INK, va="center")
arr(ax, (54, 37.5), (54, 20.5)); arr(ax, (70.5, 13), (64.5, 13))
save(fig, S5, "fig2-runtime-checkpoints")

# =============================================================== 105(6) Figure 1 — capability gap (data: Statistics Canada, Table 1)
rows = [("Trained existing employees on AI", 24.0, 68.1), ("Trained existing executives on AI", 15.6, 51.7),
        ("Hired employees with AI skills", 8.2, 32.8), ("Used external consultants or vendors", 10.7, 30.2)]
fig, ax = plt.subplots(figsize=(8.4, 3.6))
ys = list(range(len(rows)))[::-1]
for y, (lab, s, l) in zip(ys, rows):
    ax.plot([s, l], [y, y], color="#C9D3E0", lw=3, zorder=1)
    ax.scatter([s], [y], s=70, color=GREY, zorder=2); ax.scatter([l], [y], s=70, color=BLUE, zorder=3)
    ax.text(s, y + 0.27, f"{s:.1f}%", ha="center", fontsize=9, color=INK)
    ax.text(l, y + 0.27, f"{l:.1f}%", ha="center", fontsize=9, color=NAVY, fontweight="600")
    ax.text(89, y, f"{l / s:.1f}×", ha="right", va="center", fontsize=10.5, color=NAVY, fontweight="600")
ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows], fontsize=9.5, color=NAVY)
ax.set_xlim(0, 90); ax.set_xticks([0, 20, 40, 60, 80]); ax.set_xticklabels(["0%", "20%", "40%", "60%", "80%"])
ax.set_ylim(-0.6, len(rows) - 0.3); ax.grid(axis="y", visible=False); ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.text(89, len(rows) - 0.45, "Ratio", ha="right", fontsize=9, color=INK, fontweight="600")
ax.scatter([], [], s=50, color=GREY, label="1–4 employees"); ax.scatter([], [], s=50, color=BLUE, label="100+ employees")
ax.legend(loc="upper center", bbox_to_anchor=(0.45, 1.16), ncol=2, handletextpad=0.3)
ax.set_xlabel("Share of AI-using businesses that took the step", fontsize=9.5)
save(fig, S6, "fig1-capability-gap")

# =============================================================== 105(6) Figure 2 — shadow-mode loop
fig, ax = canvas(8.8, 4.0)
box(ax, 1, 66, 19, 16, "Agent drafts\nin shadow mode")
box(ax, 24, 66, 19, 16, "Compare with\nstaff's own work")
diamond(ax, 56, 74, 8, 13, "Match?")
box(ax, 72, 67, 20, 14, "Log agreement")
diamond(ax, 56, 32, 9, 13, "Cause?")
box(ax, 20, 24, 22, 16, "Fix data, tools\nor instructions")
box(ax, 78, 24, 21, 16, "Write the rule\ninto the SOP", fill=SKY, ec=BLUE, lw=1.6, bold=True)
arr(ax, (20.5, 74), (23.5, 74)); arr(ax, (43.5, 74), (47.6, 74)); arr(ax, (64.2, 74), (71.5, 74))
ax.text(68, 77, "yes", ha="center", fontsize=8.5, color=INK)
arr(ax, (56, 60.8), (56, 45.4)); ax.text(57.5, 53, "no", fontsize=8.5, color=INK, va="center")
arr(ax, (46.8, 32), (42.5, 32)); ax.text(44.6, 35.5, "agent\nerror", ha="center", fontsize=8.2, color=INK, linespacing=1.1)
arr(ax, (65.2, 32), (77.5, 32)); ax.text(71.3, 35.5, "unwritten\nrule", ha="center", fontsize=8.2, color=INK, linespacing=1.1)
line(ax, [(19.5, 32), (8, 32)]); arr(ax, (8, 32), (8, 65.5))
line(ax, [(88.5, 23.5), (88.5, 8), (8, 8), (8, 32)])
ax.text(47, 10.5, "retest on the next cases", ha="center", fontsize=8.5, color=INK)
save(fig, S6, "fig2-shadow-mode-loop")

# =============================================================== 105(6) Figure 3 — staged roadmap
fig, ax = canvas(8.8, 4.4)
stages = [("Stage 0", "Foundations", "Clean the data the\nfirst use case needs\nDocument the process\nName an owner\nSet a data policy"),
          ("Stage 1", "Assist", "Read-only assistant\non documents and ERP\nShadow-mode drafts\nStaff compare with\ntheir own work"),
          ("Stage 2", "Draft and approve", "Agent writes drafts\ninto ERP or CMMS\nA person approves\neach one\nTrack acceptance"),
          ("Stage 3", "Act within limits", "Low-risk actions run\nautomatically\nApproval kept for\nconsequential steps\nAdd a second agent")]
W, G = 22.5, 2.5
for i, (a, b, t) in enumerate(stages):
    x = 1 + i * (W + G)
    box(ax, x, 38, W, 58, "", fill=PALE)
    ax.text(x + 1.5, 91, a, fontsize=10, color=NAVY, fontweight="600", va="center")
    ax.text(x + 1.5, 85, b, fontsize=10, color=NAVY, fontweight="600", va="center")
    ax.text(x + 1.5, 77, t, fontsize=8.8, color=NAVY, va="top", linespacing=1.35)
    if i < 3: arr(ax, (x + W + 0.4, 67), (x + W + G - 0.4, 67))
gates = [("Gate 1", "Readiness index at\nleast 40%"), ("Gate 2", "Shadow drafts match\nstaff work 90%+"), ("Gate 3", "60 days of drafts with\nerror rate on target")]
for i, (g, t) in enumerate(gates):
    cx = 1 + (i + 1) * (W + G) - G / 2
    ax.plot([cx, cx], [37.5, 31], color="#9AB0C8", lw=1)
    ax.add_patch(Polygon([(cx - 1.6, 27), (cx, 31), (cx + 1.6, 27), (cx, 23)], closed=True, fc=BLUE, ec=BLUE))
    ax.text(cx, 17, g, ha="center", va="center", fontsize=9.5, color=NAVY, fontweight="600")
    ax.text(cx, 8, t, ha="center", va="center", fontsize=8.5, color=INK, linespacing=1.2)
save(fig, S6, "fig3-staged-roadmap")
print("7 figures written")
