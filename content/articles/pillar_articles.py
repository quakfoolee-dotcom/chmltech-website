"""Two pillar articles that replace clusters of overlapping older posts (V4.72), kept at the older addresses.

1. post/how-to-increase-operational-efficiency-for-small-business
   becomes the single operational efficiency guide. Merged into it, then retired to redirects:
     7-ways-operational-efficiency-can-help-reduce-costs-in-your-business
     boosting-business-success-with-operations-efficiency-tips-and-strategies
     improving-operational-efficiency-technology-kpis-and-integration-for-small-businesses
2. post/ai-agents-101-and-how-to-use-them-to-improve-efficiency
   becomes the single AI agents guide for small businesses. Merged into it, then retired to redirects:
     maximizing-business-efficiency-with-ai-agents
     unlocking-the-power-of-agentic-ai-for-small-business-growth-and-efficiency
     how-ai-agents-are-revolutionizing-business-and-impacting-daily-life

Usage:  python3 content/articles/pillar_articles.py
        python3 content/gen/refresh_article.py <slug>                 (each pillar)
        python3 content/gen/refresh_article.py --retire <old> <slug>  (each merged post)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, MUTED, LINE, SAND, PALE, GREENF, ORANGEF

OE = "how-to-increase-operational-efficiency-for-small-business"
OE_MERGED = ["7-ways-operational-efficiency-can-help-reduce-costs-in-your-business",
             "boosting-business-success-with-operations-efficiency-tips-and-strategies",
             "improving-operational-efficiency-technology-kpis-and-integration-for-small-businesses"]
AG = "ai-agents-101-and-how-to-use-them-to-improve-efficiency"
AG_MERGED = ["maximizing-business-efficiency-with-ai-agents",
             "unlocking-the-power-of-agentic-ai-for-small-business-growth-and-efficiency",
             "how-ai-agents-are-revolutionizing-business-and-impacting-daily-life"]
DATE = "2026-11-13"


def src(items):
    return "<h2>Sources</h2><ul>" + "".join(
        f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in items) + "</ul>"


def rel(items):
    return "<h2>Related reading</h2><ul>" + "".join(f'<li><a href="../post/{s}.html">{t}</a></li>' for s, t in items) + "</ul>"


def money(x):
    return f"${x:,.0f}"


# ═════════════════════════ 1. Operational efficiency ═════════════════════════
# Worked example: order-to-ship at a 25-person distributor (illustrative numbers).
ORDERS_DAY, DAYS_YR = 120, 250
LT_BEFORE = [("Waiting for order entry", 0.6), ("Waiting for the daily credit check", 0.9), ("Queue for picking", 1.1),
             ("Picking and packing", 0.2), ("Waiting for the carrier", 0.4)]
LT_AFTER = [("Waiting for order entry", 0.1), ("Waiting for the daily credit check", 0.1), ("Queue for picking", 0.5),
            ("Picking and packing", 0.15), ("Waiting for the carrier", 0.4)]
ERR_BEFORE, ERR_AFTER, ERR_COST = 0.025, 0.008, 85          # pick errors per order; cost of each (reship, credit, admin)
OT_BEFORE, OT_AFTER, OT_RATE, WEEKS = 60, 20, 45, 50         # overtime hours a week; $/h at time and a half
CAPEX, SETUP = 38_000, 22_000                                # scanners and warehouse software; setup, training, outside help

LTB = sum(v for _, v in LT_BEFORE); LTA = sum(v for _, v in LT_AFTER)
ORDERS_YR = ORDERS_DAY * DAYS_YR
WIP_B, WIP_A = ORDERS_DAY * LTB, ORDERS_DAY * LTA
ERRS_B, ERRS_A = ORDERS_YR * ERR_BEFORE, ORDERS_YR * ERR_AFTER
SAVE_ERR = (ERRS_B - ERRS_A) * ERR_COST
SAVE_OT = (OT_BEFORE - OT_AFTER) * WEEKS * OT_RATE
SAVE = SAVE_ERR + SAVE_OT
INVEST = CAPEX + SETUP
PAYBACK_M = INVEST / SAVE * 12


def fig_loop():
    s = DEFS
    steps = [("1", "Measure a", "baseline"), ("2", "Find the", "waste"), ("3", "Fix the", "constraint"),
             ("4", "Standardize", "the new way"), ("5", "Review it", "every month")]
    cols = [BLUE, ORANGE, PURPLE, GREEND, NAVY]
    fills = [PALE, ORANGEF, "#E7E7F8", GREENF, "#E4E9F0"]
    for i, ((n, a, b), c, f) in enumerate(zip(steps, cols, fills)):
        x = 14 + i * 146
        s += f'<rect x="{x}" y="30" width="122" height="78" rx="10" fill="{f}" stroke="{c}" stroke-width="1.4"/>'
        s += f'<circle cx="{x + 61}" cy="30" r="13" fill="{c}"/>' + txt(x + 61, 35, n, "middle", "#fff", 13, True)
        s += txt(x + 61, 70, a, "middle", NAVY, 13.5, True) + txt(x + 61, 89, b, "middle", NAVY, 13.5, True)
        if i < 4: s += arrow(x + 124, 69, x + 144, 69)
    s += f'<path d="M685 108 V138 H75 V114" fill="none" stroke="{MUTED}" stroke-width="1.4" marker-end="url(#ah)"/>'
    s += txt(380, 156, "Then pick the next constraint: it has moved", "middle", MUTED, 12.5)
    tips = ["4 numbers,", "2 weeks of data", "Walk the process;", "8 wastes", "Work on the", "slowest step", "Checklists, one", "best way", "15-minute weekly", "huddle"]
    for i in range(5):
        s += txt(75 + i * 146, 184, tips[2 * i], "middle", NAVY, 12) + txt(75 + i * 146, 200, tips[2 * i + 1], "middle", NAVY, 12)
    return svg("Improvement loop in five steps: 1 measure a baseline, with four numbers and two weeks of data; 2 find the waste by walking "
               "the process with the eight wastes in mind; 3 fix the constraint, the slowest step; 4 standardize the new way with "
               "checklists and one best way; 5 review it every month in a 15-minute weekly huddle. An arrow returns from step 5 to step 1: "
               "pick the next constraint, because it has moved.", 730, 212, s, 600)


def fig_leadtime():
    s = ""
    scale = 185          # px per day
    cols = ["#9AB0C8", ORANGE, PURPLE, GREEND, "#C9C2B2"]
    for row, (lab, parts, tot) in enumerate([("Before", LT_BEFORE, LTB), ("After", LT_AFTER, LTA)]):
        y = 34 + row * 70
        s += txt(66, y + 25, lab, "end", NAVY, 13.5, True)
        x = 78
        for (name, v), c in zip(parts, cols):
            w = v * scale
            s += f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="38" fill="{c}" stroke="#fff"/>'
            if w > 34: s += txt(x + w / 2, y + 24, f"{v:g}", "middle", "#fff", 12, True)
            x += w
        s += txt(x + 8, y + 24, f"{tot:g} days", "start", NAVY, 13.5, True)
    for i, ((name, _), c) in enumerate(zip(LT_BEFORE, cols)):
        x = 78 + (i % 3) * 225; y = 190 + (i // 3) * 22
        s += f'<rect x="{x}" y="{y - 11}" width="13" height="13" fill="{c}"/>' + txt(x + 19, y, name, "start", NAVY, 12)
    return svg(f"Stacked bars of order lead time, in days. Before: waiting for order entry {LT_BEFORE[0][1]}, waiting for the daily credit "
               f"check {LT_BEFORE[1][1]}, queue for picking {LT_BEFORE[2][1]}, picking and packing {LT_BEFORE[3][1]}, waiting for the carrier "
               f"{LT_BEFORE[4][1]}, total {LTB:g} days. After: {LT_AFTER[0][1]}, {LT_AFTER[1][1]}, {LT_AFTER[2][1]}, {LT_AFTER[3][1]} and "
               f"{LT_AFTER[4][1]}, total {LTA:g} days. Almost all of the time removed was waiting, not work.", 760, 222, s, 600)


def oe():
    rows_lt = "".join(f"<tr><td>{n}</td><td>{b:g}</td><td>{a:g}</td></tr>" for (n, b), (_, a) in zip(LT_BEFORE, LT_AFTER))
    body = f"""
<p>Operational efficiency means getting the same or better output for customers with less time, money, material and effort. For a small business it is rarely about working harder. It is about removing the waiting, rework and double handling that sit between the steps of work people already do well.</p>
<p>This guide brings together what used to be four separate Chmltech articles into one practical method: the measures that matter, a five-step improvement loop, a worked example from a 25-person distributor, and the mistakes that stall most efforts. It applies to a shop floor, a warehouse or an office.</p>
<h2>Why it matters more in Canada now</h2>
<p>Canada has a long-running productivity problem. In March 2024 the Bank of Canada's Senior Deputy Governor, Carolyn Rogers, called it an emergency and said it was "time to break the glass". She pointed in particular to low business investment in machinery, equipment and intellectual property. The recent data are uneven: business sector labour productivity fell 0.5% in the first quarter of 2026 while unit labour costs rose for a fourth straight quarter, then rebounded 1.0% in the second quarter, the largest gain since 2020.</p>
<p>For an owner the national numbers translate into something simpler. Wages and input costs keep rising, so the only way to protect margins without raising prices is to produce more per hour worked. Budget 2026 also confirmed the Productivity Mega Deduction, which lets most businesses write off the full cost of equipment and software in the year it is put in use, so the tax system now rewards efficiency investments faster than before.</p>
<h2>What to measure</h2>
<p>You cannot improve what you have not measured, but you also do not need fifty KPIs. Start with four numbers for one process, such as order-to-ship, quote-to-order or a production line.</p>
<table>
<tr><th>Measure</th><th>How to calculate it</th><th>What it tells you</th></tr>
<tr><td>Throughput</td><td>Units, orders or jobs completed per day or week</td><td>How much the process delivers</td></tr>
<tr><td>Lead time</td><td>Time from request to delivery, from timestamps</td><td>How long customers wait; mostly waiting time</td></tr>
<tr><td>First-pass yield</td><td>Share of units done right the first time, with no rework or return</td><td>How much effort goes into fixing mistakes</td></tr>
<tr><td>Cost per unit</td><td>Labour, material and overhead of the process divided by units</td><td>Whether improvements reach the bottom line</td></tr>
</table>
<p>For equipment-heavy work, add overall equipment effectiveness (OEE), which splits lost time into availability, performance and quality losses. Our <a href="../post/what-oee-really-measures.html">OEE series</a> explains how. A useful rule ties the first two numbers together. Little's Law says that the work in progress equals throughput multiplied by lead time. If you ship 120 orders a day and each takes 3 days, about 360 orders are sitting somewhere in the business at any time. Cut the lead time and that pile shrinks with it.</p>
{fig(fig_loop(), 1, "The improvement loop. Each pass fixes one constraint; then the constraint moves and the loop starts again.")}
<h2>Step 1: Measure a baseline</h2>
<p>Pick one process that customers notice and that costs you money, not the whole business. Collect two weeks of real data: timestamps from your order system or ERP, job tickets, or a simple tally sheet. Two weeks is enough to see normal variation and short enough that people do not lose interest. Write the four numbers on a whiteboard where the team works. A baseline matters later, when you need to show that a change worked and when a funding program or lender asks for evidence.</p>
<h2>Step 2: Find the waste</h2>
<p>Walk the process from start to finish with the people who do it, following one order or one job. Lean practice groups waste into eight types. Most of them look normal until someone asks why they happen.</p>
<table>
<tr><th>Waste</th><th>On the shop floor</th><th>In the office</th></tr>
<tr><td>Waiting</td><td>Machines idle for material or approval</td><td>Orders waiting for a daily credit check</td></tr>
<tr><td>Defects</td><td>Scrap, rework, returns</td><td>Wrong prices, re-keyed data, credit notes</td></tr>
<tr><td>Overproduction</td><td>Making ahead of demand</td><td>Reports nobody reads</td></tr>
<tr><td>Transportation</td><td>Moving parts between distant areas</td><td>Emailing files between people and systems</td></tr>
<tr><td>Inventory</td><td>Excess raw material and work in progress</td><td>Backlogs of unprocessed requests</td></tr>
<tr><td>Motion</td><td>Walking to fetch tools</td><td>Searching folders and inboxes</td></tr>
<tr><td>Extra processing</td><td>Tighter tolerances than needed</td><td>Three approvals for a small purchase</td></tr>
<tr><td>Unused skills</td><td>Operators' ideas ignored</td><td>Staff doing data entry a tool could do</td></tr>
</table>
<p>Most lead time is waiting, not work. When you add up the steps you will usually find that hands-on work is a small share of the total, and that the rest is queues between people, shifts or systems.</p>
<h2>Step 3: Fix the constraint</h2>
<p>Every process has one step that limits the whole. The <a href="../post/things-you-need-to-know-about-the-theory-of-constraints-toc.html">theory of constraints</a> says that an hour saved at the constraint is an hour gained for the business, while an hour saved anywhere else is mostly an illusion. Find the step with the longest queue in front of it. Make sure it never waits for inputs, never works on defective material, and never stops for breaks or changeovers that someone else could cover. Only then think about adding capacity or technology.</p>
<p>Fix the process before you automate it. Technology such as barcode scanning, a warehouse or production system, an ERP or AI tools multiplies whatever process it is given. Automating a step that should not exist just makes the waste faster.</p>
<h2>Step 4: Standardize the new way</h2>
<p>Once a change works, write it down as the one best current way: a checklist, a short work instruction with photos, or a swim lane map showing who does what. Train everyone on it and make the new way the easy way, for example by setting defaults in software or putting tools where they are used. Standard work is not bureaucracy. It is what stops the process drifting back when the person who championed the change is on holiday.</p>
<h2>Step 5: Review it every month</h2>
<p>Hold a 15-minute standing huddle each week at the whiteboard: the four numbers, what got in the way, and one action with an owner. Once a month, review the trend with the owner or manager and decide whether the constraint has moved. It usually has, and the loop starts again on the new one. Teams sustain improvement when they can see the numbers move and when their own ideas get acted on, so the huddle is also the place where communication problems and training gaps come out.</p>
<h2>Worked example: order-to-ship at a distributor</h2>
<p>A distributor with 25 staff ships about {ORDERS_DAY} orders a day. Customers complain about slow delivery and wrong items, and the warehouse works about {OT_BEFORE} hours of overtime a week. The numbers below are an illustrative example built from typical figures, not a specific client.</p>
<p><strong>Baseline.</strong> Two weeks of order timestamps show an average lead time of {LTB:g} days from order to shipment, and {ERR_BEFORE:.1%} of orders have a picking error. By Little's Law about {WIP_B:.0f} orders are in progress at any time. Hands-on picking and packing take only {LT_BEFORE[3][1]} of the {LTB:g} days.</p>
<p><strong>Waste and constraint.</strong> Walking the process shows that orders entered by email wait for someone to key them in, a credit check runs once a day in a batch, and pickers work from paper lists sorted by order rather than by location. Picking is the constraint: the queue in front of it is the longest.</p>
<p><strong>Changes.</strong> Orders from repeat customers skip the batch credit check below an agreed limit; order entry happens twice a day instead of once; pickers get handheld scanners and pick lists sorted by bin location; scanning each item against the order stops wrong picks before packing.</p>
<table>
<tr><th>Stage</th><th>Before (days)</th><th>After (days)</th></tr>
{rows_lt}
<tr><td><strong>Total lead time</strong></td><td><strong>{LTB:g}</strong></td><td><strong>{LTA:g}</strong></td></tr>
</table>
{fig(fig_leadtime(), 2, "Order lead time before and after. The work itself barely changed; the waiting did.")}
<p><strong>Results after three months.</strong> Lead time falls from {LTB:g} to {LTA:g} days, so orders in progress drop from about {WIP_B:.0f} to {WIP_A:.0f}. Picking errors fall from {ERR_BEFORE:.1%} to {ERR_AFTER:.1%}, or from about {ERRS_B:,.0f} to {ERRS_A:,.0f} orders a year. Overtime falls from {OT_BEFORE} to {OT_AFTER} hours a week.</p>
<table>
<tr><th>Item</th><th>Calculation</th><th>Per year</th></tr>
<tr><td>Fewer picking errors</td><td>({ERRS_B:,.0f} − {ERRS_A:,.0f}) errors × {money(ERR_COST)} each</td><td>{money(SAVE_ERR)}</td></tr>
<tr><td>Less overtime</td><td>({OT_BEFORE} − {OT_AFTER}) h × {WEEKS} weeks × {money(OT_RATE)}/h</td><td>{money(SAVE_OT)}</td></tr>
<tr><td><strong>Total saving</strong></td><td></td><td><strong>{money(SAVE)}</strong></td></tr>
<tr><td>Investment</td><td>Scanners and software {money(CAPEX)} + setup and training {money(SETUP)}</td><td>{money(INVEST)} once</td></tr>
<tr><td><strong>Simple payback</strong></td><td>{money(INVEST)} ÷ {money(SAVE)} × 12</td><td><strong>{PAYBACK_M:.1f} months</strong></td></tr>
</table>
<p>The savings exclude the hardest number to measure and often the largest: customers who order more because delivery is faster and right. Under the Mega Deduction the scanners and software can also be written off in the first year, which improves the after-tax payback further.</p>
<h2>Common mistakes</h2>
<ul>
<li><strong>Starting with technology.</strong> Buying software before fixing the process locks in the waste and makes it more expensive to change.</li>
<li><strong>Improving everything at once.</strong> Ten small projects with no owner deliver less than one finished project on the constraint.</li>
<li><strong>Measuring activity instead of flow.</strong> Busy people and machines are not the goal; orders delivered right and on time are.</li>
<li><strong>No baseline.</strong> Without before numbers nobody can prove the change worked, and the next idea gets less support.</li>
<li><strong>Leaving the team out.</strong> The people doing the work know where the waste is. Changes imposed without them rarely last.</li>
<li><strong>Stopping after one win.</strong> Once the first constraint is fixed, a different step becomes the bottleneck. Keep the loop running.</li>
</ul>
<h2>Where to start this month</h2>
<ol>
<li>Choose one process that customers notice.</li>
<li>Collect two weeks of data for the four measures and put them on a board.</li>
<li>Walk the process with the team and list the waste you see.</li>
<li>Find the step with the longest queue and agree one change to it.</li>
<li>Start a 15-minute weekly huddle and keep it going for three months.</li>
</ol>
<p>If you would like help, Chmltech's <a href="../operational-efficiency.html">operational efficiency consulting</a> and two-week <a href="../rapid-lean-assessment.html">Rapid Lean assessment</a> follow this method, and our <a href="../funding.html">funding finder</a> lists the programs that can share the cost.</p>
""" + src([
        ("Bank of Canada: Time to break the glass, fixing Canada's productivity problem (Carolyn Rogers, 26 March 2024)", "https://www.bankofcanada.ca/wp-content/uploads/2024/03/remarks-2024-03-26.pdf"),
        ("Statistics Canada: Labour productivity, hourly compensation and unit labour cost, first quarter 2026", "https://www150.statcan.gc.ca/n1/daily-quotidien/260603/dq260603a-eng.htm"),
        ("Statistics Canada: Labour productivity, hourly compensation and unit labour cost, second quarter 2026", "https://www150.statcan.gc.ca/daily-quotidien/260903/dq260903c-eng.htm"),
    ]) + rel([
        ("what-oee-really-measures", "What OEE really measures"),
        ("things-you-need-to-know-about-the-theory-of-constraints-toc", "Things you need to know about the theory of constraints"),
        ("how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations", "How to use Lean methodology to eliminate waste"),
        ("50-must-track-kpis-for-business-success-from-finance-to-product-development", "50 must-track KPIs for business success"),
        ("canada-budget-2026-what-manufacturers-and-process-plants-should-know", "Budget 2026: what manufacturers and process plants should know"),
        ("boost-your-business-with-cdap-funding-support-for-digital-adoption", "After CDAP: where Canadian businesses find digital and AI funding"),
    ])
    return dict(slug=OE, title="Operational Efficiency for Small Businesses: A Practical Guide",
                desc="How small businesses raise operational efficiency: four measures, a five-step improvement loop, and a worked order-to-ship example with payback.",
                cats=["operational-efficiency", "process-improvement"],
                tags=["operational efficiency", "productivity", "lean", "theory of constraints", "lead time", "Little's Law", "small business"],
                body=body.strip(), date=DATE, author="Quak Foo Lee", read="8 min read", cover_label="Operations",
                related=["what-oee-really-measures", "things-you-need-to-know-about-the-theory-of-constraints-toc",
                         "how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations"])


# ═════════════════════════ 2. AI agents ═════════════════════════
# Worked example: quote requests at a 40-person fabrication shop (illustrative numbers).
REQ_WK, WEEKS_YR = 60, 48
MIN_BEFORE, MIN_AGENT_REVIEW = 25, 8          # minutes per request: manual; human review of the agent's draft
RATE_H = 45                                   # $/h loaded cost of the estimator's time
COST_RUN = 0.40                               # $ model and platform usage per request
BUILD = 15_000                                # one-time setup, integration and testing
MAINT_H, MAINT_RATE = 3, 90                   # hours a month of upkeep, $/h

HRS_SAVED_WK = REQ_WK * (MIN_BEFORE - MIN_AGENT_REVIEW) / 60
GAIN = HRS_SAVED_WK * WEEKS_YR * RATE_H
RUN_YR = REQ_WK * WEEKS_YR * COST_RUN
MAINT_YR = MAINT_H * 12 * MAINT_RATE
NET_YR = GAIN - RUN_YR - MAINT_YR
PAYBACK_AG = BUILD / NET_YR * 12


def fig_ladder():
    s = DEFS
    tiers = [("AI assistant", ["A person asks;", "the model answers."], ["e.g. drafting an email or", "summarizing a contract"], BLUE, PALE),
             ("Workflow automation", ["Code sets the steps;", "the model fills some in."], ["e.g. read an invoice, extract", "fields, post to accounting"], GREEND, GREENF),
             ("AI agent", ["The model chooses the", "steps and the tools."], ["e.g. chase a late order across", "email, the ERP and the carrier"], PURPLE, "#E7E7F8")]
    for i, (name, how, ex, c, f) in enumerate(tiers):
        x = 20 + i * 238; y = 110 - i * 40
        s += f'<rect x="{x}" y="{y}" width="222" height="{140 + i * 40}" rx="10" fill="{f}" stroke="{c}" stroke-width="1.4"/>'
        s += txt(x + 111, y + 28, name, "middle", NAVY, 15, True)
        for j, ln in enumerate(how): s += txt(x + 111, y + 54 + 18 * j, ln, "middle", NAVY, 13)
        for j, ln in enumerate(ex): s += txt(x + 111, y + 104 + 17 * j, ln, "middle", MUTED, 12)
    s += arrow(30, 268, 700, 268, MUTED)
    s += txt(30, 290, "More predictable, easier to test", "start", MUTED, 12.5)
    s += txt(700, 290, "More flexible, needs more guardrails", "end", MUTED, 12.5)
    return svg("Three levels of AI use, rising left to right. AI assistant: a person asks and the model answers, for example drafting an "
               "email. Workflow automation: code sets the steps and the model fills some in, for example reading an invoice, extracting "
               "fields and posting to accounting. AI agent: the model chooses the steps and the tools, for example investigating a late "
               "order across email, the ERP and the carrier's site. An arrow along the bottom runs from more predictable and easier to "
               "test, to more flexible and needing more guardrails.", 730, 300, s, 600)


def fig_plan():
    s = DEFS
    phases = [("Days 1–30", "Pick and prepare", ["Choose one task", "Write the procedure", "Collect 30 real examples", "Set the measures"], BLUE, PALE),
              ("Days 31–60", "Pilot, draft only", ["Agent drafts, people decide", "Log every run", "Score against examples", "Fix prompts and tools"], GREEND, GREENF),
              ("Days 61–90", "Decide and scale", ["Compare to baseline", "Approve limited actions", "Write the runbook", "Pick the next task"], PURPLE, "#E7E7F8")]
    for i, (when, what, items, c, f) in enumerate(phases):
        x = 16 + i * 240
        s += f'<rect x="{x}" y="14" width="214" height="48" rx="10" fill="{c}"/>'
        s += txt(x + 107, 34, when, "middle", "#fff", 13, True) + txt(x + 107, 52, what, "middle", "#fff", 13.5, True)
        s += f'<rect x="{x}" y="70" width="214" height="114" rx="10" fill="{f}" stroke="{c}"/>'
        for j, it in enumerate(items): s += txt(x + 16, 96 + j * 24, "• " + it, "start", NAVY, 12.5)
        if i < 2:
            s += arrow(x + 216, 38, x + 238, 38)
            s += f'<rect x="{x + 219}" y="118" width="18" height="18" rx="3" fill="#fff" stroke="{ORANGE}" stroke-width="1.6"/>'
            s += txt(x + 228, 132, "?", "middle", ORANGE, 13, True)
    s += txt(370, 210, "Orange gates: go on only if the numbers from the previous phase are good enough", "middle", MUTED, 12.5)
    return svg("A 90-day plan in three phases. Days 1 to 30, pick and prepare: choose one task, write the procedure, collect 30 real "
               "examples, set the measures. Days 31 to 60, pilot in draft-only mode: the agent drafts and people decide, log every run, score "
               "against the examples, fix prompts and tools. Days 61 to 90, decide and scale: compare to the baseline, approve limited "
               "actions, write the runbook and pick the next task. Between phases, gates: go on only if the numbers from the previous phase "
               "are good enough.", 740, 222, s, 600)


def ag():
    body = f"""
<p>An AI agent is software that uses a language model to work toward a goal in several steps, choosing which tools to use along the way: reading an email, looking up an order in the ERP, checking a supplier's price list, drafting a reply. That is different from a chatbot, which answers one question at a time, and from ordinary automation, which follows steps fixed in advance.</p>
<p>This guide replaces four earlier Chmltech articles on AI agents with one practical reference for small and mid-sized businesses: what agents are, where they pay off, a worked cost example, the guardrails that matter, and a 90-day plan to start. For the deeper research behind each section, see the linked Chmltech Online Journal papers.</p>
<h2>Where Canadian businesses are</h2>
<p>Adoption is rising quickly from a low base. Statistics Canada reports that 19.2% of businesses used AI to produce goods or deliver services in the 12 months to the second quarter of 2026, up from 12.2% a year earlier and 6.1% in 2024. Use is concentrated in information and cultural industries, finance and insurance, and professional services, and is far lower in rural businesses and smaller firms. Among businesses using AI, virtual agents or chatbots were used by 28.2%, behind data analytics and text analytics.</p>
<p>So most Canadian small businesses are still at the start. That is an advantage: you can learn from what has gone wrong elsewhere and begin with a task where the payoff is clear.</p>
<h2>Assistants, workflows and agents</h2>
<p>The word "agent" is used loosely. A useful distinction comes from Anthropic's guide to building effective agents: <em>workflows</em> are systems where language models and tools follow predefined code paths, while <em>agents</em> are systems where the model directs its own process and tool use. The guide's main advice is to use the simplest approach that works, because agents trade predictability and cost for flexibility.</p>
{fig(fig_ladder(), 1, "Three levels of AI use. Most small-business wins today come from the middle level; full agents need more guardrails.")}
<p>In practice, many valuable "agents" in small firms are workflows with one or two flexible steps. That is fine. What matters is whether the task gets done well, cheaply and safely, not what it is called.</p>
<h2>Where agents help in a small business</h2>
<table>
<tr><th>Function</th><th>Good first task</th><th>What it needs</th></tr>
<tr><td>Sales</td><td>Turn emailed quote requests into a draft quote</td><td>Price list, product rules, past quotes</td></tr>
<tr><td>Customer service</td><td>Answer order-status questions from the ERP and carrier</td><td>Read access to orders and tracking</td></tr>
<tr><td>Finance</td><td>Match supplier invoices to purchase orders and receipts</td><td>Accounting system, PO and receiving data</td></tr>
<tr><td>Operations</td><td>Summarize shift logs and flag recurring downtime causes</td><td>Logs or maintenance records</td></tr>
<tr><td>HR and admin</td><td>Answer policy questions from the employee handbook</td><td>Current, approved documents</td></tr>
<tr><td>Purchasing</td><td>Compare supplier quotes and flag missing terms</td><td>Quote documents, approved supplier list</td></tr>
</table>
<p>A good first task is frequent, mostly digital, follows a documented procedure with some judgment, is easy to check, and can be undone if it goes wrong. Avoid tasks where one mistake is costly or cannot be reversed, such as paying invoices or changing customer contracts, until the agent has a track record. Our journal paper on <a href="../post/agent-readiness-for-small-and-mid-sized-firms-data-process-staged-adoption.html">agent readiness for small and mid-sized firms</a> includes a readiness score for choosing.</p>
<h2>Worked example: quote requests at a fabrication shop</h2>
<p>A 40-person metal fabrication shop receives about {REQ_WK} quote requests a week by email. An estimator spends about {MIN_BEFORE} minutes on each: reading the drawing and specification, checking material and finishing options, looking up past jobs and prices, and writing the quote. The numbers below are an illustrative example built from typical figures.</p>
<p>The agent reads each request, extracts dimensions, material, quantity and finish, finds similar past quotes, applies the shop's pricing rules, and drafts the quote with its assumptions listed. The estimator reviews and corrects the draft before anything goes to the customer, which takes about {MIN_AGENT_REVIEW} minutes.</p>
<table>
<tr><th>Item</th><th>Calculation</th><th>Per year</th></tr>
<tr><td>Estimator time saved</td><td>{REQ_WK} requests × ({MIN_BEFORE} − {MIN_AGENT_REVIEW}) min = {HRS_SAVED_WK:g} h/week × {WEEKS_YR} weeks × {money(RATE_H)}/h</td><td>{money(GAIN)}</td></tr>
<tr><td>Model and platform usage</td><td>{REQ_WK * WEEKS_YR:,} requests × ${COST_RUN:.2f}</td><td>−{money(RUN_YR)}</td></tr>
<tr><td>Upkeep</td><td>{MAINT_H} h/month × 12 × {money(MAINT_RATE)}/h</td><td>−{money(MAINT_YR)}</td></tr>
<tr><td><strong>Net benefit</strong></td><td></td><td><strong>{money(NET_YR)}</strong></td></tr>
<tr><td>Setup, integration and testing</td><td>One time</td><td>{money(BUILD)}</td></tr>
<tr><td><strong>Simple payback</strong></td><td>{money(BUILD)} ÷ {money(NET_YR)} × 12</td><td><strong>{PAYBACK_AG:.1f} months</strong></td></tr>
</table>
<p>Two points stand out. First, the model usage is small next to the value of the estimator's time; the real costs are setup and upkeep. Second, the estimator's freed time is only worth money if it goes somewhere useful, such as answering more requests faster. Faster quotes often win more work, which this calculation leaves out. Our paper on <a href="../post/the-economics-of-agentic-ai-cost-per-task-total-cost-and-payback.html">the economics of agentic AI</a> explains how to estimate cost per task and total cost of ownership in more detail.</p>
<h2>Guardrails that matter</h2>
<ul>
<li><strong>Start in draft-only mode.</strong> Let the agent prepare and people decide. Give it more autonomy one action at a time, as evidence builds. Our paper on <a href="../post/levels-of-autonomy-and-human-in-the-loop-design-for-ai-agents.html">levels of autonomy and human-in-the-loop design</a> sets out a rule for when to do this.</li>
<li><strong>Least privilege.</strong> Give the agent only the system access the task needs, read-only where possible, with its own account rather than a person's login.</li>
<li><strong>Treat incoming content as untrusted.</strong> Prompt injection, where instructions hidden in an email, document or web page steer the model, is the top risk in the OWASP Top 10 for LLM applications, and OWASP notes there is no fool-proof prevention. Keep agents that read outside content away from actions that move money or data. See <a href="../post/agent-security-and-identity-prompt-injection-least-privilege-credentials-audit.html">agent security and identity</a>.</li>
<li><strong>Protect personal information.</strong> Canada's federal, provincial and territorial privacy regulators have published principles for generative AI that ask organizations to limit the sharing of personal and confidential information and to be open about how it is used. Check where your provider stores and processes data.</li>
<li><strong>Log and test.</strong> Keep a record of every run, and test changes against a set of real examples before they go live. Public benchmark scores say little about your own task; see <a href="../post/evaluating-ai-agents-why-benchmarks-mislead-and-how-to-build-your-own-evaluation.html">evaluating AI agents</a>.</li>
</ul>
<h2>A 90-day plan to start</h2>
{fig(fig_plan(), 2, "Ninety days from choosing a task to a decision on scaling, with a go or no-go check between phases.")}
<p>Measure the same things before and during the pilot: time per task, error rate after review, and cost per task. If the pilot does not beat the baseline by a clear margin, stop or change the task. A failed pilot that costs a few weeks is a good outcome compared with an agent nobody trusts.</p>
<h2>Common mistakes</h2>
<ul>
<li><strong>Starting with the most impressive use case</strong> instead of the most frequent, checkable one.</li>
<li><strong>Automating an undocumented process.</strong> If people do the task three different ways, the agent will too. Write the procedure first.</li>
<li><strong>Connecting everything at once.</strong> Each extra system the agent can reach adds risk. Add tools one at a time.</li>
<li><strong>No owner.</strong> Someone must review the logs, handle exceptions and decide changes.</li>
<li><strong>Ignoring the people.</strong> Staff who see the agent as a threat will route work around it. Involve them in choosing and testing the task.</li>
</ul>
<p>If you would like help choosing and building a first agent, see Chmltech's <a href="../ai-operating-system.html">AI Operating System design and build</a> and <a href="../artificial-intelligence.html">AI consulting</a>, our <a href="../llm-leaderboard.html">AI model comparison</a>, and the <a href="../post/boost-your-business-with-cdap-funding-support-for-digital-adoption.html">funding programs</a> that can share the cost.</p>
""" + src([
        ("Statistics Canada: Analysis on artificial intelligence use by businesses in Canada, second quarter of 2026", "https://www150.statcan.gc.ca/n1/pub/11-621-m/11-621-m2026010-eng.htm"),
        ("Statistics Canada: Analysis on artificial intelligence use by businesses in Canada, second quarter of 2025", "https://www150.statcan.gc.ca/n1/pub/11-621-m/11-621-m2025008-eng.htm"),
        ("Anthropic: Building effective agents (December 2024)", "https://www.anthropic.com/engineering/building-effective-agents"),
        ("OWASP: Top 10 for LLM Applications 2025", "https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/"),
        ("Office of the Privacy Commissioner of Canada: Principles for responsible, trustworthy and privacy-protective generative AI technologies", "https://www.priv.gc.ca/en/privacy-topics/technology/artificial-intelligence/gd_principles_ai/"),
    ]) + rel([
        ("agent-readiness-for-small-and-mid-sized-firms-data-process-staged-adoption", "Agent readiness for small and mid-sized firms"),
        ("the-economics-of-agentic-ai-cost-per-task-total-cost-and-payback", "The economics of agentic AI"),
        ("agent-security-and-identity-prompt-injection-least-privilege-credentials-audit", "Agent security and identity"),
        ("agent-interoperability-standards-mcp-a2a-erp-crm-plant-systems", "Agent interoperability standards: MCP, A2A and ERP integration"),
        ("ai-readiness-preparing-your-organization-for-successful-ai-adoption", "AI readiness: preparing your organization"),
        ("private-ai-assistant-on-your-own-pc-anythingllm-and-ollama", "Your own private AI assistant with AnythingLLM and Ollama"),
    ])
    return dict(slug=AG, title="AI Agents for Small Businesses: What They Are, Where They Help and How to Start",
                desc="What AI agents are, how they differ from chatbots and automation, where they pay off in small businesses, a worked cost example and a 90-day plan.",
                cats=["artificial-intelligence", "operational-efficiency"],
                tags=["AI agents", "agentic AI", "small business", "automation", "AI adoption Canada", "prompt injection", "human in the loop"],
                body=body.strip(), date=DATE, author="Quak Foo Lee", read="7 min read", cover_label="AI",
                related=["agent-readiness-for-small-and-mid-sized-firms-data-process-staged-adoption",
                         "the-economics-of-agentic-ai-cost-per-task-total-cost-and-payback",
                         "levels-of-autonomy-and-human-in-the-loop-design-for-ai-agents"])


if __name__ == "__main__":
    for a in (oe(), ag()):
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        words = len(__import__("re").sub(r"<svg.*?</svg>|<[^>]+>", " ", a["body"], flags=__import__("re").S).split())
        print(a["slug"], words, "words")
    print(f"OE: lead time {LTB:g}->{LTA:g} d, WIP {WIP_B:.0f}->{WIP_A:.0f}, errors {ERRS_B:.0f}->{ERRS_A:.0f}, save {SAVE:,.0f}, invest {INVEST:,}, payback {PAYBACK_M:.1f} mo")
    print(f"AG: {HRS_SAVED_WK:g} h/wk, gain {GAIN:,.0f}, run {RUN_YR:,.0f}, maint {MAINT_YR:,.0f}, net {NET_YR:,.0f}, payback {PAYBACK_AG:.1f} mo")
