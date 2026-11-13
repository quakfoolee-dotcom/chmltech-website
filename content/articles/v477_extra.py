"""V4.77: extra sections that turn the eight rewrites into long-form guides (owner's request, Nov 2026).

expand(a) inserts each block before an anchor in the article body. Anchors are exact strings from v477_articles.py;
"END" means before the Sources or Related reading heading, whichever comes first.
"""
import math, re

TEND = "END"


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table>\n<tr>{h}</tr>\n{b}\n</table>"


def money(x):
    return f"${x:,.0f}"


# ── numbers used below ──
# ERP vs MRP five-year cost (illustrative)
MRP_SUB, ACC_SUB, MRP_SETUP, MRP_STAFF = 12_000, 1_200, 12_000, 15_000
ERP_LIC, ERP_SUP, ERP_PARTNER, ERP_DATA, ERP_TRAIN, ERP_STAFF = 24_000, 6_000, 45_000, 15_000, 6_000, 33_000
MRP5 = MRP_SETUP + MRP_STAFF + 5 * (MRP_SUB + ACC_SUB)
ERP5 = ERP_PARTNER + ERP_DATA + ERP_TRAIN + ERP_STAFF + 5 * (ERP_LIC + ERP_SUP)
# production planning load check (hours next week)
LOAD = [("Laser cutting", 32, 37.5), ("Press brake", 44, 37.5), ("Welding", 60, 75), ("Paint", 20, 37.5)]
# MRP lot sizing comparison for the legs record
LEG_GROSS = [30, 0, 180, 0, 150, 0]
ORDER_COST, HOLD_WK = 50, 0.05


def lot_compare():
    out = []
    for name, lot in (("Lot for lot", None), ("Fixed lot of 150", 150), ("Fixed lot of 300", 300)):
        oh, orders, hold = 100, 0, 0.0
        for g in LEG_GROSS:
            n = max(0, g - oh)
            if n:
                q = n if lot is None else math.ceil(n / lot) * lot
                oh += q; orders += 1
            oh -= g; hold += oh
        out.append((name, orders, hold, orders * ORDER_COST + hold * HOLD_WK))
    return out


LOTS = lot_compare()
# Six Sigma Pareto
PARETO = [("Wrong price", 14), ("Wrong quantity", 9), ("Missing PO number", 6), ("Wrong tax code", 4), ("Wrong address", 3)]
# TOC: Saturday overtime at the constraint
SAT_H, RATE_W, MARGIN, OT_COST = 7.5, 25, 40, 1_200
SAT_T = SAT_H * RATE_W * MARGIN


EXTRA = {
# ─────────────────────────────── 1. Process improvement guide ───────────────────────────────
"implement-process-improvements-part-1": [
("<h2>Which method fits your problem</h2>", f"""<h2>Signs a process needs improving</h2>
<p>Most businesses do not lack improvement ideas; they lack a clear view of which process to fix first. These symptoms usually point to a process problem rather than a people problem:</p>
<ul>
<li><strong>The same mistake keeps happening,</strong> even with different people doing the work.</li>
<li><strong>Work waits more than it moves.</strong> Orders, quotes or approvals sit in someone's inbox for days and take minutes to do.</li>
<li><strong>Customers chase you</strong> for updates, dates or corrections.</li>
<li><strong>Information is typed twice</strong> into different systems or spreadsheets.</li>
<li><strong>Only one person knows how it is done,</strong> and things stall when they are away.</li>
<li><strong>Overtime and expediting are normal</strong> even though demand has not grown.</li>
</ul>
"""),
("<h2>An eight-step improvement project</h2>", f"""<h2>Choosing the first project</h2>
<p>List the candidate processes and score each one on two questions: how much would fixing it be worth (to customers, cash or capacity), and how hard is it to change? Start with a process that is high on value and low or medium on effort. A visible early win builds the support you need for the harder projects.</p>
{table(["", "Low effort", "High effort"], [
    ("<strong>High value</strong>", "Do first: quote turnaround, order entry, month-end close", "Plan carefully: ERP replacement, new plant layout"),
    ("<strong>Low value</strong>", "Quick fixes during normal work", "Avoid for now"),
])}
<h2>Roles in an improvement project</h2>
{table(["Role", "Who", "What they do"], [
    ("Sponsor", "A manager or the owner", "Sets the goal, removes obstacles, approves changes and spending, attends reviews"),
    ("Process owner", "The person accountable for the process day to day", "Owns the result after the project ends and keeps the standard current"),
    ("Team", "Three to six people who do the work, upstream and downstream", "Map, measure, find causes, design and trial changes"),
    ("Facilitator", "An internal improvement lead or an outside coach", "Keeps the method on track, runs workshops, coaches the team"),
])}
"""),
("<h2>Worked example: quote turnaround</h2>", f"""<h2>Tools at each step</h2>
{table(["Step", "Useful tools"], [
    ("Choose and scope", "Problem statement, SIPOC (suppliers, inputs, process, outputs, customers), project charter"),
    ("Map and measure", "Swim lane map, value stream map, time study, check sheet, simple run chart"),
    ("Find causes", "5 whys, fishbone diagram, Pareto chart, data by shift, product or customer"),
    ("Design the change", "Brainstorming, impact-effort matrix, mistake-proofing, standard work"),
    ("Trial and standardize", "Pilot plan, before-and-after comparison, written procedure, training record"),
    ("Sustain", "Scorecard measure, monthly review, audit at 30 and 90 days"),
])}
"""),
("<h2>What makes improvements last</h2>", f"""<p>The before-and-after picture for the machine shop:</p>
{table(["Measure", "Before", "After six weeks"], [
    ("Average quote turnaround", "6 working days", "2 working days"),
    ("Quotes waiting for a material price", "About 60%", "About 15%"),
    ("Quotes needing owner approval", "All", "Only those over $25,000"),
    ("Quote win rate", "Tracked from now on", "Reviewed monthly"),
])}
<h2>Common pitfalls</h2>
<ul>
<li><strong>Jumping to a solution,</strong> often new software, before the current process is mapped and measured.</li>
<li><strong>A problem statement that blames a person</strong> instead of describing what happens and how often.</li>
<li><strong>Too big a scope.</strong> "Fix operations" is not a project; "cut quote turnaround to two days" is.</li>
<li><strong>No baseline,</strong> so nobody can show the change worked.</li>
<li><strong>Running several projects at once</strong> with the same few people, so none finishes.</li>
</ul>
"""),
],
# ─────────────────────────────── 2. Kaizen ───────────────────────────────
"perform-kaizen-event": [
("<h2>The charter: one page, agreed in advance</h2>", f"""<h2>Types of Kaizen event</h2>
{table(["Type", "Typical focus", "Length"], [
    ("Process Kaizen", "Flow through a cell or line: layout, hand-offs, work in progress", "4 to 5 days"),
    ("Set-up reduction (SMED)", "Changeover time on a machine or line", "3 to 5 days"),
    ("Office or transactional Kaizen", "Approvals, order entry, invoicing, onboarding", "2 to 3 days"),
    ("5S blitz", "Organizing one work area or shared drive", "1 to 2 days"),
    ("Quality Kaizen", "One recurring defect with a known location", "3 to 5 days"),
])}
<h2>Who takes part</h2>
<p>Six to eight people is the right size. Include the people who do the work every day (at least half the team), someone from the step before and the step after, a person from maintenance or IT if equipment or systems will change, and one "fresh eyes" member from another area who will ask the obvious questions. A facilitator runs the method; the sponsor opens day 1 and attends the report-out.</p>
"""),
("<h2>The five-day agenda</h2>", f"""<h2>Preparation checklist</h2>
<ul>
<li>Charter signed by the sponsor, with goal and boundaries.</li>
<li>Team members released from normal duties for the event; their work covered.</li>
<li>Baseline data collected: cycle times, changeover times, defects, lead time, at least two weeks' worth.</li>
<li>Area prepared: production plan adjusted so changes can be tried, materials for quick changes (tape, labels, carts, shelving).</li>
<li>Maintenance and IT on call for the week.</li>
<li>Room booked near the work area, with a large wall for maps and charts.</li>
<li>Report-out time set in the sponsor's and managers' calendars.</li>
</ul>
"""),
("<h2>Worked example: results from the changeover event</h2>", f"""<h2>A day-by-day plan</h2>
{table(["Day", "Morning", "Afternoon", "End-of-day output"], [
    ("1", "Kick-off by sponsor; short training on waste and the method", "Walk the process; film or time it", "Current-state map and baseline"),
    ("2", "Detailed timing; separate work from waiting", "Root causes with 5 whys and a fishbone", "List of wastes and causes, ranked"),
    ("3", "Design changes; quick experiments in the area", "Try the best options for real", "Changes tested, results timed"),
    ("4", "Refine; second round of trials", "Write the standard and train operators on it", "New standard work, checklists, photos"),
    ("5", "Prepare the report-out", "Report-out to sponsor and managers; agree actions", "Results, 30-day action list with owners"),
])}
"""),
("<h2>After the event</h2>", f"""<h2>Second example: an office Kaizen</h2>
<p>Kaizen events work just as well away from the shop floor. A distributor ran a three-day event on supplier invoice approval, which averaged 9 working days and caused late-payment charges. The team found 14 steps, three of them duplicate checks and two of them waits for a manager who checked only that a purchase order existed. They changed the process so invoices with a matching purchase order and goods receipt are approved automatically, and only exceptions go to a manager. The process dropped to 8 steps and about 3 working days, and late-payment charges stopped. The figures are illustrative.</p>
<h2>Facilitator tips</h2>
<ul>
<li>Keep the team in the work area as much as possible; the answers are there, not in the meeting room.</li>
<li>Try changes the same day they are suggested. A tested idea beats a debated one.</li>
<li>Make the before-and-after visible with photos, timings and a simple chart.</li>
<li>Protect the team's time; one person called away each day weakens the result.</li>
<li>End every day with a 15-minute review: what we learned, what we try tomorrow.</li>
</ul>
"""),
("<h2>Common mistakes</h2>", f"""<h2>A 30-60-90 day check</h2>
{table(["When", "Check"], [
    ("30 days", "Action list complete? Standard followed on every shift? Measure holding at the new level?"),
    ("60 days", "Any drift? Do operators suggest refinements? Has training reached new staff?"),
    ("90 days", "Results confirmed and reported; standard updated with what was learned; next event chosen"),
])}
"""),
],
# ─────────────────────────────── 3. 5S ───────────────────────────────
"lessons-learned-from-deploying-5s-in-the-service-industry": [
("<h2>Why it matters in a service business</h2>", f"""<h2>Each step in more detail</h2>
<h3>1. Sort</h3>
<p>Go through the area with the people who use it and tag every item that has not been used in the last month or two. Tagged items go to a holding area for two weeks; anything nobody claims is moved, sold, recycled or archived. Be firm with "just in case" items; they hide the things people need. On a shared drive, the equivalent is moving folders untouched for a year to an archive.</p>
<h3>2. Set in order</h3>
<p>Put frequently used items closest to where they are used and give every item a labelled place. Outlines on shelves, labelled bins with minimum and maximum quantities, and colour coding by use make it obvious when something is missing. For digital files, agree one folder structure and a naming rule (for example, client, project, document type, date) and stick to it.</p>
<h3>3. Shine</h3>
<p>Cleaning is also inspection. A daily five-minute clean of a reception desk, treatment room or service van reveals worn equipment, low supplies and safety issues before they become complaints. Write a short cleaning schedule with names and times.</p>
<h3>4. Standardize</h3>
<p>Photograph each area when it is right and post the photo where the work happens, with a short checklist. Standard layouts for repeated spaces, such as every treatment room or every service van, let staff work in any of them without searching.</p>
<h3>5. Sustain</h3>
<p>Schedule a short audit each month, rotate the auditor so everyone learns the standard, and post the score. Managers who walk the area and ask about the score signal that it matters.</p>
"""),
("<h2>Lessons from service deployments</h2>", f"""<h2>Service examples</h2>
{table(["Setting", "Typical 5S changes"], [
    ("Dental or physiotherapy clinic", "Identical layout in every treatment room; labelled supply bins with reorder cards; daily room checklist"),
    ("Hotel housekeeping", "Standard cart layout photographed; par levels per floor; linen room organized by room type"),
    ("Field service van", "Shadow boards and labelled bins for tools; minimum stock of common parts; weekly van audit"),
    ("Accounting or engineering office", "Shared drive structure and naming rule; templates in one place; clear-desk policy for confidential papers"),
    ("Restaurant kitchen", "Labelled stations; first-in, first-out storage; cleaning schedule by shift"),
])}
<h2>An eight-week roll-out plan</h2>
{table(["Weeks", "Activity"], [
    ("1", "Pick a pilot area; brief the team; take before photos; set up a red-tag holding area"),
    ("2–3", "Sort and set in order in the pilot area; label everything"),
    ("4", "Shine: cleaning schedule and inspection points"),
    ("5", "Standardize: photos, checklists, layout standard"),
    ("6–7", "First two monthly audits; fix what slips"),
    ("8", "Review results with staff; choose the next area"),
])}
"""),
("<h2>A simple 5S audit</h2>", f"""<h2>Digital 5S in more detail</h2>
<p>For many service businesses the most valuable 5S project is the shared drive or document system. Wasted time searching for the latest version of a proposal, contract or drawing is invisible but large, and the wrong version sent to a customer is a real risk. The steps are the same: archive what is old (sort), agree a structure and naming rule (set in order), delete duplicates and clear personal desktops and downloads regularly (shine), use templates and a short guide (standardize), and review access and structure every quarter (sustain). For controlled documents such as procedures, see <a href="../post/iso-9001-document-and-revision-control.html">document and revision control</a>.</p>
"""),
(TEND, f"""<h2>Common mistakes</h2>
<ul>
<li>Doing 5S to the staff instead of with them.</li>
<li>Treating it as a one-off clean-up day.</li>
<li>Labelling everything without first removing what is not needed.</li>
<li>Audits that only managers do, so staff see them as inspections.</li>
<li>Starting in too many areas at once and finishing none.</li>
</ul>
"""),
],
# ─────────────────────────────── 4. TOC ───────────────────────────────
"things-you-need-to-know-about-the-theory-of-constraints-toc": [
("<h2>The five focusing steps</h2>", f"""<h2>How to find the constraint</h2>
<ul>
<li><strong>Look for the pile.</strong> Work waits in front of the constraint. The step with the largest and most persistent queue is usually it.</li>
<li><strong>Compare load with capacity.</strong> For each step, divide the hours of work needed by the hours available. The highest ratio is the constraint.</li>
<li><strong>Watch where expediting happens.</strong> If supervisors spend their days pushing jobs through one area, that is a strong signal.</li>
<li><strong>Check what idles when one step stops.</strong> When the constraint stops, the whole output stops. When a non-constraint stops briefly, nothing downstream notices.</li>
<li><strong>Be suspicious of averages.</strong> A step that is busy only 70% of the time on average can still be the constraint for a particular product mix or during peaks.</li>
</ul>
"""),
("<h2>Worked example: what is an hour at the constraint worth?</h2>", f"""<h2>Exploit, subordinate and elevate in practice</h2>
{table(["Step", "Typical actions"], [
    ("Exploit", "Stagger breaks so the constraint keeps running; put the best operator there; inspect parts before the constraint so it never works on scrap; cut its set-up time; run the most profitable jobs per constraint hour first"),
    ("Subordinate", "Release work into the line only at the constraint's pace; let non-constraints have idle time; schedule maintenance on non-constraints during peaks, never on the constraint"),
    ("Elevate", "Overtime or an extra shift at the constraint only; move some of its work to another machine or a subcontractor; buy capacity only after exploiting and subordinating"),
])}
"""),
("<h2>Drum, buffer, rope</h2>", f"""<h2>Elevating: is overtime worth it?</h2>
<p>Continuing the example: a Saturday shift of {SAT_H:g} hours at welding only, at {RATE_W} units an hour and {money(MARGIN)} margin per unit, adds about {money(SAT_T)} of throughput, against overtime costs of about {money(OT_COST)} for the welders and a supervisor. Running the whole line on Saturday would cost far more and produce the same extra output, because only welding limits it. The figures are illustrative.</p>
<h2>Throughput accounting in brief</h2>
<p>TOC uses three measures to judge decisions. <strong>Throughput</strong> is sales minus truly variable costs, mostly materials. <strong>Investment</strong> is money tied up in inventory and equipment. <strong>Operating expense</strong> is everything else spent to run the business, including wages. A good decision raises throughput, or lowers investment or operating expense, without hurting the others. This view explains why cutting cost at a non-constraint rarely helps, while one extra hour at the constraint adds directly to profit.</p>
"""),
("<h2>Beyond the factory floor</h2>", f"""<h2>TOC, Lean and Six Sigma</h2>
{table(["", "Theory of constraints", "Lean", "Six Sigma"], [
    ("Main question", "Where is the limit?", "Where is the waste?", "Where does the variation come from?"),
    ("Main measure", "Throughput", "Lead time, flow", "Defects, capability"),
    ("Best used when", "Output is capped by one step", "Work waits and moves too much", "A defect recurs and its cause is unclear"),
])}
<p>They work well together: TOC tells you where to focus, Lean removes the waste there, and Six Sigma solves the stubborn quality problems at that point.</p>
"""),
(TEND, f"""<h2>A service example</h2>
<p>A small engineering firm finds that every project waits for one senior engineer to check and stamp drawings. The other engineers are often idle, waiting for comments. Applying the five steps: the senior engineer stops doing drafting and admin work that others can do (exploit), drawings are released for checking in a planned order rather than whenever they are finished (subordinate), a second engineer is trained and authorized to check simpler drawings (elevate), and the firm then looks for the next limit, which turns out to be sales. Project lead time falls without hiring anyone new.</p>
"""),
],
# ─────────────────────────────── 5. Production planning ───────────────────────────────
"production-planning-and-scheduling-for-manufacturing": [
("<h2>Inputs a schedule needs</h2>", f"""<h2>Make-to-stock, make-to-order and engineer-to-order</h2>
{table(["Strategy", "What triggers production", "Planning focus"], [
    ("Make-to-stock", "Forecast and stock levels", "Forecast accuracy, finished goods safety stock, batch sizes"),
    ("Make-to-order", "A customer order for a standard product", "Quoted lead times, component availability, capacity"),
    ("Assemble-to-order", "A customer order, built from stocked sub-assemblies", "Sub-assembly stock and final assembly capacity"),
    ("Engineer-to-order", "A customer order that needs design work", "Engineering capacity, long-lead materials, project milestones"),
])}
<p>Many small manufacturers run a mix. Plan each product family according to its strategy rather than forcing one approach on everything.</p>
"""),
("<h2>Worked example: which job goes first?</h2>", f"""<h2>Checking load against capacity</h2>
<p>Before sequencing jobs, check that next week's work fits. The table compares the hours of work scheduled at each work centre with the hours available; the figures are illustrative.</p>
{table(["Work centre", "Hours of work", "Hours available", "Load"], [(n, f"{w:g}", f"{c:g}", f"<strong>{w / c:.0%}</strong>" if w > c else f"{w / c:.0%}") for n, w, c in LOAD])}
<p>The press brake is loaded at {LOAD[1][1] / LOAD[1][2]:.0%}, so the schedule cannot be met as it stands. The options are overtime at the press brake, moving some jobs a week later, or splitting jobs so the most urgent part ships on time. Planning with finite capacity like this avoids promising dates the shop cannot meet.</p>
<h2>Forward and backward scheduling</h2>
<p><strong>Forward scheduling</strong> starts each job as soon as possible and calculates when it will finish; it shows the earliest date you can promise. <strong>Backward scheduling</strong> starts from the due date and works back through the routing to find the latest start; it keeps inventory and work in progress low but leaves no slack. Many shops schedule backward from due dates and then check the result forward against capacity.</p>
"""),
("<h2>Making the schedule stick</h2>", f"""<h2>Set-up and sequencing</h2>
<p>Where changeovers are long, the order of jobs matters as much as the rule. Grouping jobs by material, colour, thickness or tooling into families, and running light-to-dark or thin-to-thick sequences, can save hours a week. Reducing the changeover itself, through a <a href="../post/perform-kaizen-event.html">set-up reduction Kaizen</a>, makes smaller batches and shorter lead times affordable.</p>
<h2>Tools: from whiteboard to software</h2>
{table(["Tool", "Fits", "Limits"], [
    ("Whiteboard or spreadsheet", "One or two work centres, a few dozen jobs a week", "Hard to keep current; no link to materials"),
    ("MRP or ERP scheduling", "Material-driven planning, standard routings", "Often assumes unlimited capacity unless set up for it"),
    ("Advanced planning and scheduling (APS)", "Many work centres, complex set-ups, frequent changes", "Needs accurate routings and times; more cost and set-up"),
])}
<h2>A weekly planning meeting</h2>
<p>Thirty minutes each week with sales, production, purchasing and the planner keeps the schedule real: review last week's adherence and misses, confirm next week's load against capacity, flag material shortages, and agree any priority changes before the frozen window starts.</p>
"""),
(TEND, f"""<h2>Handling rush orders</h2>
<p>Every shop gets urgent orders. The damage comes from accepting them without seeing what they push out. A simple rule helps: before saying yes, check the load at the constraint for the days affected, name the jobs that will move, and get agreement from whoever owns those customers. Some shops keep a small amount of capacity unscheduled each week, perhaps five to ten percent at the constraint, for genuine rush work. If rush orders are routine, the real problem is usually quoted lead times that are too long or a forecast that misses predictable demand.</p>
<h2>Measures to track</h2>
{table(["Measure", "What it tells you"], [
    ("Schedule adherence", "Share of jobs completed on the planned day; the discipline of the plan"),
    ("On-time delivery", "Share of orders shipped by the promised date; what the customer sees"),
    ("Work in progress", "Jobs or value started but not finished; high WIP means long lead times"),
    ("Manufacturing lead time", "Days from release to completion"),
    ("Capacity utilization at the constraint", "Whether the bottleneck is fully used"),
])}
"""),
],
# ─────────────────────────────── 6. MRP ───────────────────────────────
"demystifying-mrp-a-comprehensive-guide-to-the-material-requirements-planning-process": [
("<h2>The three inputs</h2>", f"""<h2>Dependent and independent demand</h2>
<p>The key idea behind MRP is the difference between two kinds of demand. <strong>Independent demand</strong> comes from customers for finished products and must be forecast or taken from orders. <strong>Dependent demand</strong> is for the parts and materials that go into those products; it does not need to be forecast, because it can be calculated from the production plan and the bill of materials. Reorder-point methods treat every item as if its demand were independent, which leads to shortages of some parts and excess of others. MRP calculates dependent demand exactly.</p>
"""),
("<h2>Worked example: a stool and its legs</h2>", f"""<h2>How the bill of materials is structured</h2>
<p>A bill of materials is arranged in levels. Level 0 is the finished product; level 1 holds the parts and sub-assemblies that go directly into it; level 2 holds what goes into those, and so on. MRP processes one level at a time, from the top down, so that every item's total requirement, from all the products that use it, is known before its orders are planned. An item used at several levels is planned at its lowest level, which software handles with a "low-level code".</p>
<h2>The gross-to-net logic</h2>
<ol>
<li><strong>Gross requirements:</strong> total demand for the item in each period, from customer orders or from parent items.</li>
<li><strong>Scheduled receipts:</strong> orders already placed and due in.</li>
<li><strong>Projected on hand:</strong> stock carried forward from the last period, plus receipts, minus requirements.</li>
<li><strong>Net requirements:</strong> what is still short after stock and receipts are used.</li>
<li><strong>Planned order receipts:</strong> net requirements rounded to the ordering rule (exact quantity, fixed lot, minimum).</li>
<li><strong>Planned order releases:</strong> the same quantities moved earlier by the lead time; these become requirements for the components one level down.</li>
</ol>
"""),
("<h2>Choices that change the plan</h2>", f"""<h2>Comparing lot-sizing rules</h2>
<p>For the legs, with an ordering cost of {money(ORDER_COST)} per order and a holding cost of {HOLD_WK:.2f} dollars per leg per week (both illustrative), three ordering rules over the six weeks compare as follows.</p>
{table(["Rule", "Orders placed", "Leg-weeks held in stock", "Ordering + holding cost"], [(n, o, f"{h:,.0f}", money(c)) for n, o, h, c in LOTS])}
<p>Ordering exactly what is needed holds the least stock. One lot of 300 needs only one order but carries the most stock through the six weeks. With these costs the single large order is cheapest, because holding a leg costs little; for a bulky or expensive part, or one that can become obsolete, the answer flips. The right rule depends on the two costs and on practical limits such as supplier minimums, storage space and shelf life.</p>
"""),
("<h2>Why MRP plans go wrong</h2>", f"""<h2>Capacity planning and MRP II</h2>
<p>Basic MRP assumes that any planned order can be made in its time slot. Capacity requirements planning (CRP) adds up the hours that planned and released orders need at each work centre, period by period, so overloads show before they happen. When MRP was extended in the 1980s to include capacity, shop floor control and the financial side of the plan, it became manufacturing resource planning (MRP II), the direct ancestor of today's ERP systems.</p>
<h2>Exception messages</h2>
<p>An MRP system re-plans every time something changes and then tells planners what to do through exception messages: release an order, expedite one (bring it in), de-expedite one (push it out), or cancel one. Working the exception list every day is the planner's core job. A list with hundreds of messages usually means bad data or a master schedule that changes too often.</p>
"""),
(TEND, f"""<h2>Implementing MRP in a small manufacturer</h2>
{table(["Step", "What to do"], [
    ("1. Clean the item master", "One part number per item; units of measure; lead times checked with suppliers"),
    ("2. Build accurate BOMs", "Walk the shop floor to confirm how products are really built; include packaging and consumables that matter"),
    ("3. Fix inventory accuracy", "Cycle count high-value and fast-moving items weekly; aim for 95% or better before go-live"),
    ("4. Set planning rules", "Lot sizes, safety stocks and order minimums by item, starting simple"),
    ("5. Run in parallel", "Compare the MRP plan with what planners would have done for a few weeks"),
    ("6. Go live by product family", "Start with one family; expand once the plan is trusted"),
])}
"""),
],
# ─────────────────────────────── 7. ERP vs MRP ───────────────────────────────
"understanding-erp-vs-mrp-a-comprehensive-comparison-of-manufacturing-systems": [
("<h2>An MRP system is usually enough when</h2>", f"""<h2>What each system does day to day</h2>
{table(["Activity", "With an MRP system", "With an ERP system"], [
    ("Customer order", "Entered in MRP; invoice raised in the accounting package", "Entered once; flows to production, shipping and invoicing"),
    ("Material shortage", "MRP plans purchase orders; receipts update stock", "Same, and the supplier invoice is matched and paid in the same system"),
    ("Job costing", "Labour and material per job in MRP; summary posted to accounting", "Costs post to the ledger as work is done"),
    ("Month-end", "Reconcile inventory value between MRP and accounting", "Inventory and ledger are the same data"),
    ("Reporting", "Production reports in MRP; financial reports in accounting", "Combined reports across sales, production and finance"),
])}
"""),
("<h2>A common path</h2>", f"""<h2>Five-year cost: a worked comparison</h2>
<p>A manufacturer with 30 staff, about 15 of them system users, compares a cloud MRP system linked to its accounting package with a mid-market cloud ERP. All figures are illustrative.</p>
{table(["Cost item", "MRP + accounting", "ERP"], [
    ("Subscriptions per year", money(MRP_SUB + ACC_SUB), money(ERP_LIC)),
    ("Support per year", "Included", money(ERP_SUP)),
    ("Implementation partner", money(MRP_SETUP), money(ERP_PARTNER)),
    ("Data migration and integrations", "Included above", money(ERP_DATA)),
    ("Training", "Included above", money(ERP_TRAIN)),
    ("Internal staff time", money(MRP_STAFF), money(ERP_STAFF)),
    ("<strong>Five-year total</strong>", f"<strong>{money(MRP5)}</strong>", f"<strong>{money(ERP5)}</strong>"),
])}
<p>The ERP costs about {ERP5 / MRP5:.1f} times as much over five years. It is worth it only if it removes costs the MRP route keeps, such as days of month-end reconciliation, double entry between systems, or the risk of errors in inventory valuation, or if it enables growth the MRP route cannot support, such as a second site.</p>
<h2>Questions to ask vendors</h2>
<ul>
<li>Show us our own order, built from our BOM and routing, from quote to invoice, in a scripted demo.</li>
<li>How does the system handle our costing method (standard, average or actual job cost)?</li>
<li>What does it integrate with out of the box: our accounting package, e-commerce, shipping, EDI?</li>
<li>What is the full five-year cost, including partner fees, support and price increases?</li>
<li>Can we export all our data if we leave?</li>
<li>Can we speak to two customers of our size and industry?</li>
</ul>
"""),
(TEND, f"""<h2>Linking MRP to your accounting package</h2>
<p>If you choose the MRP route, the link to accounting decides how much manual work remains. Check which of these flow automatically and which need re-keying: customer invoices, supplier bills from purchase orders and receipts, inventory value and cost of goods sold, and labour costs from job time. A good connector posts summaries daily so accounting stays current. Agree with your accountant which system is the master for customers, suppliers and items, and reconcile inventory value monthly; a small difference caught every month is easy to explain, a large one found at year-end is not.</p>
<h2>Signs your data is ready for either system</h2>
<ul>
<li>Every item has one part number, a description people recognize, a unit of measure and a lead time.</li>
<li>BOMs match how products are actually built today.</li>
<li>Routings list the real work centres and realistic times.</li>
<li>Stock counts match the records for at least 95% of the items you count.</li>
<li>Someone owns each of these and keeps them current.</li>
</ul>
<h2>Typical timelines</h2>
{table(["Phase", "MRP system", "ERP system"], [
    ("Selection", "2 to 6 weeks", "2 to 4 months"),
    ("Data preparation (items, BOMs, routings, stock)", "2 to 6 weeks", "1 to 3 months"),
    ("Configuration and testing", "2 to 4 weeks", "2 to 6 months"),
    ("Training and go-live", "1 to 2 weeks", "1 to 2 months"),
])}
<p>Data preparation is the step most often underestimated, and it is the same work for either system. Doing it well is the best preparation for whichever route you choose.</p>
"""),
],
# ─────────────────────────────── 8. Six Sigma ───────────────────────────────
"six-sigma-tools-a-comprehensive-guide-to-process-improvement": [
("<h2>The DMAIC phases</h2>", f"""<h2>Roles and belts</h2>
{table(["Role", "Typical training", "What they do"], [
    ("Champion or sponsor", "Half-day to two-day overview", "Selects projects, provides resources, removes obstacles"),
    ("Black Belt", "About four weeks spread over several months, plus projects", "Leads complex projects full or part time; coaches Green Belts"),
    ("Green Belt", "About one to two weeks, plus a project", "Leads projects in their own area alongside their normal job"),
    ("Yellow Belt", "One to two days", "Takes part in projects; collects data; applies basic tools"),
])}
<p>Small businesses rarely need Black Belts on staff. One or two trained Green Belts, with an outside coach for harder projects, is usually enough.</p>
"""),
("<h2>Tools by phase</h2>", f"""<h2>What each phase should deliver</h2>
{table(["Phase", "Deliverables at the review"], [
    ("Define", "Signed charter, SIPOC, customer requirements, project scope and timeline"),
    ("Measure", "Process map, data collection plan, measurement system check, baseline performance and capability"),
    ("Analyze", "Root causes confirmed with data, not opinion; size of each cause's effect"),
    ("Improve", "Solution chosen and piloted; before-and-after results; risks reviewed with FMEA"),
    ("Control", "Control plan, updated procedures, training done, control chart in use, handover to the process owner"),
])}
"""),
("<h2>Worked example 1: defects per million opportunities</h2>", f"""<h2>A Pareto chart in practice</h2>
<p>The invoicing team sorts last month's {sum(n for _, n in PARETO)} errors by type. The table shows the count and cumulative share of each.</p>
{table(["Error type", "Count", "Cumulative share"], [(t, n, f"{sum(x for _, x in PARETO[:i + 1]) / sum(x for _, x in PARETO):.0%}") for i, (t, n) in enumerate(PARETO)])}
<p>The first two types account for {(PARETO[0][1] + PARETO[1][1]) / sum(n for _, n in PARETO):.0%} of errors. The project focuses there first: price errors come from an out-of-date price list, quantity errors from manual entry of handwritten orders.</p>
<h2>The fishbone diagram</h2>
<p>A fishbone (Ishikawa) diagram lists possible causes of a problem under headings, often the six Ms: methods, machines, materials, measurement, manpower (people) and mother nature (environment). It is a structured brainstorm. Its output is a list of suspects to test with data in the Analyze phase, not a conclusion.</p>
"""),
("<h2>Lean and Six Sigma together</h2>", f"""<h2>Control charts</h2>
<p>A control chart plots a measure over time with a centre line and upper and lower control limits, usually set three standard deviations from the mean, calculated from the process itself. Points inside the limits with no pattern show a stable process; the variation is common-cause and only a process change will reduce it. A point outside the limits, or a run of several points on one side of the centre line, signals a special cause worth investigating. Control limits are not specification limits: a stable process can still make parts out of specification, which is what capability indices reveal.</p>
<h2>When not to use Six Sigma</h2>
<ul>
<li>The cause is obvious and the fix is cheap; just fix it.</li>
<li>The problem is flow and waiting, not defects; use Lean.</li>
<li>There is no reliable data and no way to collect it in a reasonable time.</li>
<li>The process runs too rarely to measure, such as an annual event.</li>
</ul>
"""),
],
}


def expand(a):
    body = a["body"]
    for anchor, html in EXTRA.get(a["slug"], []):
        if anchor == TEND:
            m = re.search(r"<h2>(Sources|Related reading)</h2>", body)
            at = m.start() if m else len(body)
        else:
            at = body.find(anchor)
            assert at >= 0, (a["slug"], anchor)
        body = body[:at] + html + body[at:]
    a["body"] = body
    return a
