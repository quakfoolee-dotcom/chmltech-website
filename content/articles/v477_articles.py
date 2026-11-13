"""V4.77: 2021–2023 process and manufacturing posts rewritten in our own words (audit plan V8). Each keeps its address
and its original publish date (content/articles/original_dates.json).

1. implement-process-improvements-part-1        one complete guide; Part 2 retired into it
2. perform-kaizen-event                         Kaizen events: charter, five-day agenda, worked results
3. lessons-learned-from-deploying-5s-in-the-service-industry   5S for offices, clinics and service businesses
4. things-you-need-to-know-about-the-theory-of-constraints-toc  five focusing steps with a worked line example
5. production-planning-and-scheduling-for-manufacturing         planning levels and a worked scheduling-rule example
6. demystifying-mrp-a-comprehensive-guide-to-the-material-requirements-planning-process   MRP with a worked netting table
7. understanding-erp-vs-mrp-a-comprehensive-comparison-of-manufacturing-systems           ERP vs MRP decision guide
8. six-sigma-tools-a-comprehensive-guide-to-process-improvement  tools by DMAIC phase, DPMO and Cpk worked examples

Usage:  python3 content/articles/v477_articles.py
        python3 content/gen/refresh_article.py <slug>                 (each of the eight)
        python3 content/gen/refresh_article.py --retire <old> <new>   (Part 2)
"""
import json, math, os, re, sys
from statistics import NormalDist
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, MUTED, LINE, SAND, PALE, GREENF, ORANGEF

DATE = "2026-11-13"
PI = "implement-process-improvements-part-1"
KZ = "perform-kaizen-event"
S5 = "lessons-learned-from-deploying-5s-in-the-service-industry"
TOC = "things-you-need-to-know-about-the-theory-of-constraints-toc"
PP = "production-planning-and-scheduling-for-manufacturing"
MRP = "demystifying-mrp-a-comprehensive-guide-to-the-material-requirements-planning-process"
EVM = "understanding-erp-vs-mrp-a-comprehensive-comparison-of-manufacturing-systems"
SS = "six-sigma-tools-a-comprehensive-guide-to-process-improvement"
RETIRE = {PI: ["how-to-implement-process-improvements-part-2"]}
ORIGINAL = {PI: "2021-08-24", KZ: "2021-08-24", S5: "2021-08-28", TOC: "2021-08-30", PP: "2021-09-02", MRP: "2023-03-19", EVM: "2023-03-19", SS: "2023-03-31"}


def src(items):
    return "<h2>Sources</h2><ul>" + "".join(
        f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in items) + "</ul>"


def rel(items):
    return "<h2>Related reading</h2><ul>" + "".join(f'<li><a href="../post/{s}.html">{t}</a></li>' for s, t in items) + "</ul>"


def money(x):
    return f"${x:,.0f}"


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table>\n<tr>{h}</tr>\n{b}\n</table>"


def art(slug, title, desc, cats, tags, body, read, label, related):
    return dict(slug=slug, title=title, desc=desc, cats=cats, tags=tags, body=body.strip(), date=DATE, author="Quak Foo Lee",
                read=read, cover_label=label, related=[r for r, _ in related])


# ═════════════════════════ 1. Process improvement guide ═════════════════════════
def pi():
    methods = [
        ("PDCA (plan, do, check, act)", "A simple loop for any change", "Small, frequent improvements by the team that does the work"),
        ("Lean", "Removes waiting, re-work and needless steps so work flows", "Long lead times, many hand-offs, piles of work in progress"),
        ("Six Sigma (DMAIC)", "Uses data to find and remove causes of variation and defects", "A recurring defect whose cause is not obvious"),
        ("Theory of Constraints", "Finds the one step that limits output and focuses on it", "Output is capped and adding effort everywhere has not helped"),
        ("Business process management", "Documents, owns and measures processes across the company", "Processes that cross several departments and drift over time"),
        ("Kaizen event", "A focused 3 to 5 day workshop on one process", "A clear, contained problem that a small team can fix quickly"),
    ]
    steps = [
        ("1. Choose the process", "Pick one that customers notice or that costs real time or money. Write the problem as a fact with a number."),
        ("2. Set a goal and a sponsor", "A measurable target, a date, and a manager who can remove obstacles."),
        ("3. Form a small team", "The people who do the work, plus someone from each step upstream and downstream."),
        ("4. Map the current process", "Walk it, time it, and note waits, re-work and hand-offs."),
        ("5. Find the causes", "Ask why the problem happens until you reach something you can change; check with data."),
        ("6. Design and trial the change", "Start small: one shift, one product line, one customer. Measure the result."),
        ("7. Make it the standard", "Write the new way down, train everyone, and update forms and systems."),
        ("8. Check and sustain", "Review the measure monthly for six months; it is easy to slide back."),
    ]
    body = f"""
<p>Process improvement means changing how work is done so it is faster, cheaper, more reliable or easier for customers. This guide brings together a two-part series first published on this site in 2021, rewritten as one article: which method to use, an eight-step project you can run without consultants, and the habits that make results last.</p>
<h2>Which method fits your problem</h2>
<p>The methods overlap more than their names suggest. Most small businesses do best by starting with PDCA and a process map, and borrowing tools from the others as needed.</p>
{table(["Method", "What it does", "Use it when"], methods)}
<h2>An eight-step improvement project</h2>
{table(["Step", "What to do"], steps)}
<h2>Worked example: quote turnaround</h2>
<p>A machine shop takes an average of 6 working days to send quotes, and loses work to faster competitors. The team maps the process and finds that a quote waits in three queues: for the estimator, for a material price from the supplier, and for the owner's approval. The actual work is about 3 hours. Three changes follow: a price list for the ten most-used materials, refreshed monthly, so most quotes no longer wait for the supplier; approval only for quotes over $25,000; and a shared queue board so the estimator works oldest first. After a six-week trial, average turnaround is 2 days. The numbers are illustrative, but the pattern is typical: the work is short and the waits are long.</p>
<h2>What makes improvements last</h2>
<ul>
<li><strong>Leaders show up.</strong> A manager who attends the review and removes obstacles matters more than any method.</li>
<li><strong>The new way is written down</strong> and replaces the old instructions everywhere. See <a href="../post/essentials-of-effective-process-documentation.html">process documentation that people use</a>.</li>
<li><strong>One measure is tracked</strong> on the team's scorecard after the project ends.</li>
<li><strong>People are not blamed for problems the process caused,</strong> so they keep raising them. <a href="../post/what-are-the-core-values-of-process-improvement-part-i.html">The core values of process improvement</a> covers the culture side.</li>
</ul>
"""
    r = [("what-are-the-core-values-of-process-improvement-part-i", "The core values of process improvement"),
         ("how-to-perform-a-successful-business-process-optimization", "Business process optimization: map, measure, redesign"),
         ("perform-kaizen-event", "How to run a Kaizen event")]
    return art(PI, "How to Implement Process Improvements: Methods, an Eight-Step Project and a Worked Example",
               "Which process improvement method fits your problem, an eight-step project a small business can run itself, a worked quote example, and how to make it last.",
               ["process-improvement"], ["process improvement", "PDCA", "Lean", "Six Sigma", "continuous improvement", "improvement project"],
               body + rel(r), "6 min read", "Process", r)


# ═════════════════════════ 2. Kaizen ═════════════════════════
def fig_kaizen():
    s = DEFS
    days = [("Day 1", ["Train the team;", "walk the process"]), ("Day 2", ["Measure; find", "waste and causes"]), ("Day 3", ["Design and", "try changes"]),
            ("Day 4", ["Refine; write", "the new standard"]), ("Day 5", ["Report out;", "30-day action list"])]
    for i, (d, l) in enumerate(days):
        x = 10 + i * 146
        s += box(x, 40, 128, 34, d, fill=NAVY, stroke=NAVY, tc="#fff", fs=13)
        s += box(x, 80, 128, 54, l, fill=PALE, stroke="#9AB0C8", fs=12, bold=False)
        if i < 4: s += arrow(x + 130, 57, x + 144, 57)
    s += f'<rect x="10" y="8" width="128" height="24" rx="6" fill="{SAND}"/>' + txt(74, 25, "2–4 weeks before:", "middle", NAVY, 11.5, True)
    s += txt(146, 25, "charter, team, baseline data", "start", MUTED, 11.5)
    s += f'<rect x="604" y="146" width="128" height="24" rx="6" fill="{SAND}"/>' + txt(668, 163, "30 days after:", "middle", NAVY, 11.5, True)
    s += txt(596, 163, "finish actions, check results", "end", MUTED, 11.5)
    return svg("A five-day Kaizen event. Two to four weeks before: charter, team and baseline data. Day 1: train the team and walk "
               "the process. Day 2: measure and find waste and causes. Day 3: design and try changes. Day 4: refine and write the new "
               "standard. Day 5: report out and agree a 30-day action list. Thirty days after: finish the actions and check the results.",
               742, 180, s, 600)


def kz():
    charter = [("Process and boundaries", "Changeover on press line 2, from last good part to first good part"), ("Problem", "Changeovers average 52 minutes; 4 a day"),
               ("Goal", "Under 25 minutes, sustained for 30 days"), ("Team", "Two operators, a setter, maintenance, the supervisor; a facilitator"),
               ("Sponsor", "Plant manager: attends day 1 and the report-out, approves spending up to $3,000"), ("Out of scope", "Buying new presses; changing the product mix")]
    results = [("Average changeover", "52 min", "21 min"), ("Changeovers a day", "4", "4"), ("Press time recovered", "—", "about 2 hours a day"),
               ("Tools fetched during changeover", "11 trips", "0 (cart pre-staged)"), ("Written standard", "None", "One-page checklist with photos")]
    body = f"""
<p>A Kaizen event is a short, intense improvement workshop: a small team spends three to five days on one process, makes changes on the spot, and leaves with a new standard and a short action list. The word kaizen means change for the better. This article, first published in 2021, has been rewritten with a charter template, a five-day agenda and a worked example.</p>
<h2>When a Kaizen event is the right tool</h2>
<ul>
<li>The problem is contained to one process or area, such as a changeover, a work cell, a picking route or an approval loop.</li>
<li>The people who do the work can be released for most of a week.</li>
<li>The fix is likely to be a change in layout, method or standard work, not a new IT system or a large capital purchase.</li>
</ul>
<p>If the cause is unknown and needs weeks of data, a Six Sigma project fits better. If the problem spans several departments, start with a process map across all of them.</p>
<h2>The charter: one page, agreed in advance</h2>
<p>Most failed events were set up badly, not run badly. A one-page charter, agreed with the sponsor two to four weeks before, prevents that. The example below is for a changeover event in a small stamping plant.</p>
{table(["Item", "Example"], charter)}
<h2>The five-day agenda</h2>
{fig(fig_kaizen(), 1, "A typical five-day Kaizen event, with preparation before and follow-up after.")}
<p>Shorter three-day events work well in offices and for smaller problems: combine days 1 and 2, and days 3 and 4. Whatever the length, keep the team in the work area, not a meeting room, and try changes for real during the event.</p>
<h2>Worked example: results from the changeover event</h2>
{table(["Measure", "Before", "After 30 days"], results)}
<p>The team filmed a changeover, listed every step, and split them into work that needs the press stopped and work that can be done while it runs (the core idea of SMED, single-minute exchange of die). Staging tools and the next die on a cart before the press stops removed most of the time. The figures are illustrative.</p>
<h2>After the event</h2>
<ol>
<li>Finish the 30-day action list; assign every item to a person with a date.</li>
<li>Check the measure weekly for a month, then monthly.</li>
<li>Audit the new standard at 30 and 90 days: is it being followed, and does it still make sense?</li>
<li>Share the result with the rest of the business; it is the best way to get volunteers for the next event.</li>
</ol>
<h2>Common mistakes</h2>
<ul>
<li>Choosing a problem too large for a week.</li>
<li>No sponsor, so changes that need approval stall.</li>
<li>Talking about changes instead of trying them during the event.</li>
<li>No follow-up, so the area drifts back within months.</li>
</ul>
"""
    r = [("implement-process-improvements-part-1", "How to implement process improvements"),
         ("how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations", "How to use Lean to eliminate waste"),
         ("what-oee-really-measures", "What OEE really measures")]
    return art(KZ, "How to Run a Kaizen Event: Charter, Five-Day Agenda and a Worked Example",
               "When to use a Kaizen event, a one-page charter, a five-day agenda, a worked changeover example with results, and how to make the gains last.",
               ["lean"], ["Kaizen", "Kaizen event", "Lean", "SMED", "changeover", "continuous improvement"],
               body + rel(r), "6 min read", "Kaizen", r)


# ═════════════════════════ 3. 5S in services ═════════════════════════
def s5():
    ss = [("Sort", "Remove what is not needed", "Old forms, broken equipment, duplicate files", "Unused folders and old versions on the shared drive"),
          ("Set in order", "A place for everything, labelled", "Supply cupboard with labelled bins and minimum levels", "One folder structure; clear file names"),
          ("Shine", "Clean and check", "Daily wipe-down of reception and treatment rooms; spot faults early", "Weekly clear-out of the inbox and downloads folder"),
          ("Standardize", "Make the first three routine", "Photo of how the area should look; a short checklist", "A naming rule and templates everyone uses"),
          ("Sustain", "Keep it going", "Monthly 15-minute audit by rotating staff", "Quarterly review of access and folders")]
    audit = [("Only needed items in the area", 3, 5), ("Every item has a labelled place", 2, 4), ("Area clean; nothing damaged", 3, 4),
             ("Standard posted and followed", 1, 4), ("Audit done on schedule last month", 0, 5)]
    tb = sum(a for _, a, _ in audit); ta = sum(b for _, _, b in audit)
    body = f"""
<p>5S is a method for organizing a workplace so that what people need is where they expect it, and problems are easy to see. It started in Japanese factories, but it works just as well in an office, a clinic, a hotel or a field service van. This article, first written in 2021, has been rewritten with service examples, a digital version, and a simple audit.</p>
<h2>The five steps, with service examples</h2>
{table(["Step", "What it means", "Physical example", "Digital example"], ss)}
<h2>Why it matters in a service business</h2>
<p>In a service business the product is often time: the time a customer waits, or the time staff spend looking for something instead of serving. A receptionist who searches for a form, a technician who drives back for a part, or an account manager who cannot find the latest proposal are all symptoms that 5S addresses. It also improves safety and makes a better first impression on customers who see the space.</p>
<h2>Lessons from service deployments</h2>
<ul>
<li><strong>Start with one visible area,</strong> such as the supply room or a shared drive, and finish it before moving on.</li>
<li><strong>Involve the people who use the space.</strong> They know what they need and will keep a system they designed.</li>
<li><strong>Take before and after photos.</strong> They make the result obvious and become the standard.</li>
<li><strong>Do not stop at Shine.</strong> Most programs fade because the last two steps, Standardize and Sustain, were never put in place.</li>
<li><strong>Keep the audit short and regular.</strong> Fifteen minutes a month beats a long annual inspection.</li>
</ul>
<h2>A simple 5S audit</h2>
<p>Score each line from 0 (not at all) to 5 (fully). The example shows one clinic supply room before and three months after a 5S project; the scores are illustrative.</p>
{table(["Check", "Before", "After 3 months"], [(c, a, b) for c, a, b in audit] + [("<strong>Total (out of 25)</strong>", f"<strong>{tb}</strong>", f"<strong>{ta}</strong>")])}
<p>The low before-scores on Standardize and Sustain are typical, and they are where to focus. 5S is often the first step of a wider Lean program; see <a href="../post/how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations.html">how to use Lean to eliminate waste</a>.</p>
""" + src([("ASQ: What are the five S's (5S) of Lean", "https://asq.org/quality-resources/lean/five-s-tutorial")])
    r = [("how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations", "How to use Lean to eliminate waste"),
         ("perform-kaizen-event", "How to run a Kaizen event"), ("essentials-of-effective-process-documentation", "Process documentation that people use")]
    return art(S5, "5S in Service Businesses: Offices, Clinics and Digital Workspaces",
               "The five steps of 5S with physical and digital examples for service businesses, lessons from deployments, and a simple monthly audit with a worked score.",
               ["lean"], ["5S", "Lean", "service industry", "workplace organization", "digital 5S", "visual management"],
               body + rel(r), "4 min read", "5S", r)


# ═════════════════════════ 4. Theory of constraints ═════════════════════════
STATIONS = [("Cut", 60), ("Weld", 25), ("Paint", 40), ("Pack", 80)]
MARGIN, HRS_DAY, EXTRA_H, WORK_DAYS = 40, 15, 1.0, 240
GAIN_DAY = STATIONS[1][1] * EXTRA_H * MARGIN
GAIN_YR = GAIN_DAY * WORK_DAYS


def fig_toc():
    s = DEFS; Y = lambda v: 200 - v * 1.9
    for v in (0, 20, 40, 60, 80):
        s += f'<line x1="60" y1="{Y(v)}" x2="700" y2="{Y(v)}" stroke="{LINE}"/>' + txt(52, Y(v) + 4, str(v), "end", MUTED, 12)
    for i, (n, c) in enumerate(STATIONS):  # bars
        x = 110 + i * 150; col = ORANGE if c == min(x[1] for x in STATIONS) else BLUE
        s += f'<rect x="{x}" y="{Y(c)}" width="90" height="{200 - Y(c)}" fill="{col}" opacity=".85"/>'
        s += txt(x + 45, Y(c) - 6, f"{c}/h", "middle", NAVY, 13, True) + txt(x + 45, 220, n, "middle", NAVY, 13, True)
        if i < 3: s += arrow(x + 96, 130, x + 144, 130, MUTED)
    s += f'<line x1="60" y1="{Y(25)}" x2="700" y2="{Y(25)}" stroke="{ORANGE}" stroke-dasharray="5 4" stroke-width="1.5"/>'
    s += txt(700, 16, "Dashed line: line output = 25/h", "end", ORANGE, 12, True) + txt(16, 16, "Capacity, units per hour", "start", MUTED, 12)
    return svg("Capacity of four stations in a line, in units per hour: cut 60, weld 25, paint 40, pack 80. Welding is the constraint, "
               "so the whole line can only produce 25 units an hour however fast the other stations run.", 742, 232, s, 600)


def toc():
    five = [("1. Identify the constraint", "Find the step with the least capacity for the work you have. Look for the biggest pile of work waiting in front of it."),
            ("2. Exploit it", "Get the most out of it with what you already have: no idle time at breaks, no defective parts reaching it, the right job next."),
            ("3. Subordinate everything else", "Pace the rest of the process to the constraint. Releasing more work into the line only builds inventory."),
            ("4. Elevate it", "If more output is still needed, add capacity at the constraint: overtime, another machine, outsourcing part of its work."),
            ("5. Repeat", "Once it is no longer the constraint, another step will be. Go back to step 1 and avoid letting old rules become the new limit.")]
    body = f"""
<p>The theory of constraints (TOC), set out by Eliyahu Goldratt in his 1984 novel <cite>The Goal</cite>, starts from a simple observation: in any process, one step limits how much the whole process can deliver. Improving anything else does not raise output. This article, first published in 2021, has been rewritten with a worked example that puts a dollar value on the idea.</p>
<h2>The idea in one picture</h2>
{fig(fig_toc(), 1, "A four-station line. Welding is the constraint, so the line makes 25 units an hour.")}
<p>Speeding up cutting or packing in this line achieves nothing except more parts waiting in front of welding. An hour lost at welding is an hour lost for the whole business. An hour lost at packing costs nothing, because packing has spare capacity.</p>
<h2>The five focusing steps</h2>
{table(["Step", "What it means"], five)}
<h2>Worked example: what is an hour at the constraint worth?</h2>
<p>Each unit earns {money(MARGIN)} of contribution margin (price minus materials and other truly variable costs). Welding runs {HRS_DAY} hours a day over two shifts and stops for breaks and shift handovers. If the team staggers breaks so welding keeps running and adds {EXTRA_H:g} productive hour a day, the line makes {STATIONS[1][1] * EXTRA_H:.0f} more units a day, worth {money(GAIN_DAY)} a day or about {money(GAIN_YR)} over {WORK_DAYS} working days, with no new equipment. The same hour gained at painting would be worth nothing. The figures are illustrative; the method is to value time at the constraint at the margin it produces.</p>
<h2>Drum, buffer, rope</h2>
<p>TOC's scheduling method follows from the five steps. The constraint is the <strong>drum</strong> that sets the pace. A small <strong>buffer</strong> of work is kept in front of it so it never starves. The <strong>rope</strong> ties the release of new work to the drum's pace, so the rest of the line does not flood the floor with work in progress.</p>
<h2>Beyond the factory floor</h2>
<p>The constraint is often not a machine. It can be one engineer who approves every drawing, a single estimator, a test lab, or a policy such as "all orders over $5,000 need the owner's approval". The same five steps apply. In some businesses the constraint is the market: demand, not capacity, limits sales, and the effort belongs in sales and marketing.</p>
"""
    r = [("production-planning-and-scheduling-for-manufacturing", "Production planning and scheduling"),
         ("what-oee-really-measures", "What OEE really measures"), ("implement-process-improvements-part-1", "How to implement process improvements")]
    return art(TOC, "The Theory of Constraints: Five Focusing Steps and What an Hour at the Bottleneck Is Worth",
               "The theory of constraints explained with a four-station example, the five focusing steps, drum-buffer-rope, and how to value an hour at the bottleneck.",
               ["operational-efficiency"], ["theory of constraints", "TOC", "bottleneck", "five focusing steps", "drum buffer rope", "throughput"],
               body + rel(r), "5 min read", "Constraints", r)


# ═════════════════════════ 5. Production planning ═════════════════════════
JOBS = [("A", 6, 8), ("B", 2, 6), ("C", 8, 18), ("D", 3, 15), ("E", 9, 23)]   # (job, processing days, due day), in arrival order


def sched(order):
    t = 0; out = []
    for j, p, d in order:
        t += p; out.append((j, t, max(0, t - d)))
    flow = sum(c for _, c, _ in out) / len(out)
    late = sum(1 for *_, l in out if l > 0); mx = max(l for *_, l in out); tot = sum(l for *_, l in out)
    return out, flow, late, mx, tot


RULES = [("First come, first served", JOBS), ("Shortest job first", sorted(JOBS, key=lambda j: j[1])), ("Earliest due date", sorted(JOBS, key=lambda j: j[2]))]


def fig_levels():
    s = DEFS
    lv = [("Sales and operations plan", "Monthly, 12–18 months: volumes by product family; staffing", BLUE, PALE),
          ("Master production schedule", "Weekly: how many of each end product, and when", GREEND, GREENF),
          ("Material requirements plan", "Weekly or daily: parts and materials to buy or make", PURPLE, "#E7E7F8"),
          ("Shop floor schedule", "Daily: which job runs on which machine, in what order", ORANGE, ORANGEF)]
    for i, (h, d, c, f) in enumerate(lv):
        y = 12 + i * 50
        s += f'<rect x="{14 + i * 18}" y="{y}" width="250" height="40" rx="8" fill="{c}"/>' + txt(139 + i * 18, y + 25, h, "middle", "#fff", 13, True)
        s += f'<rect x="{274 + i * 18}" y="{y}" width="{454 - i * 18}" height="40" rx="8" fill="{f}" stroke="{c}"/>' + txt(288 + i * 18, y + 25, d, "start", NAVY, 12.3)
    return svg("Four levels of production planning, from long to short horizon. Sales and operations plan: monthly, 12 to 18 months, "
               "volumes by product family and staffing. Master production schedule: weekly, how many of each end product and when. "
               "Material requirements plan: weekly or daily, parts and materials to buy or make. Shop floor schedule: daily, which job "
               "runs on which machine and in what order.", 742, 214, s, 600)


def pp():
    rows = []
    for name, order in RULES:
        out, flow, late, mx, tot = sched(order)
        rows.append((name, " → ".join(j for j, *_ in order), f"{flow:.1f}", f"{late} of 5", f"{tot}", f"{mx}"))
    body = f"""
<p>Production planning decides what to make and when; scheduling decides the order of jobs on each machine or line, day by day. Done well, they let a manufacturer promise realistic dates, keep inventory down and avoid the daily firefight of expediting. This article, first published in 2021, has been rewritten with the planning levels most manufacturers use and a worked example comparing common scheduling rules.</p>
<h2>Four levels of planning</h2>
{fig(fig_levels(), 1, "Each level sets the limits for the one below it.")}
<p>Small manufacturers often skip straight to the shop floor schedule. That works until demand changes, and then every day becomes a re-plan. Even a simple monthly <a href="../post/sales-and-operations-planning-for-small-manufacturers.html">sales and operations plan</a> and a weekly master schedule make the daily schedule far calmer.</p>
<h2>Inputs a schedule needs</h2>
<ul>
<li><strong>Orders and forecasts,</strong> with due dates the customer actually needs.</li>
<li><strong>Routings:</strong> the steps each job goes through and the time each takes, including set-up.</li>
<li><strong>Capacity:</strong> machine and labour hours available, after planned maintenance and holidays.</li>
<li><strong>Material availability,</strong> from the material plan and purchasing. See <a href="../post/demystifying-mrp-a-comprehensive-guide-to-the-material-requirements-planning-process.html">the MRP guide</a>.</li>
<li><strong>The constraint:</strong> schedule the bottleneck first and the other steps around it. <a href="../post/things-you-need-to-know-about-the-theory-of-constraints-toc.html">The theory of constraints</a> explains why.</li>
</ul>
<h2>Worked example: which job goes first?</h2>
<p>Five jobs wait for one machine. Job A takes {JOBS[0][1]} days and is due on day {JOBS[0][2]}; B takes {JOBS[1][1]} days, due day {JOBS[1][2]}; C takes {JOBS[2][1]}, due day {JOBS[2][2]}; D takes {JOBS[3][1]}, due day {JOBS[3][2]}; E takes {JOBS[4][1]}, due day {JOBS[4][2]}. Three common rules give different results.</p>
{table(["Rule", "Order", "Average days in the system", "Jobs late", "Total days late", "Worst lateness (days)"], rows)}
<p>Shortest job first gets jobs out of the door fastest on average, which keeps work in progress low. Earliest due date makes the fewest customers wait past their date. First come, first served feels fair but gives the longest average time and the most total lateness here. In practice many shops use earliest due date as the default, then adjust for set-up: running similar jobs together can save more time than any sequencing rule.</p>
<h2>Making the schedule stick</h2>
<ol>
<li><strong>Freeze the next few days.</strong> Changes inside the frozen window need the production manager's approval.</li>
<li><strong>Publish one schedule</strong> that everyone works from, on a board or screen at the line.</li>
<li><strong>Track schedule adherence</strong> (jobs completed on the planned day) and on-time delivery weekly.</li>
<li><strong>Review misses for causes:</strong> material late, machine down, wrong routing time. Fix the cause, not just the date.</li>
</ol>
"""
    r = [("sales-and-operations-planning-for-small-manufacturers", "Sales and operations planning for small manufacturers"),
         ("demystifying-mrp-a-comprehensive-guide-to-the-material-requirements-planning-process", "Material requirements planning (MRP), explained"),
         ("things-you-need-to-know-about-the-theory-of-constraints-toc", "The theory of constraints")]
    return art(PP, "Production Planning and Scheduling for Manufacturers: Planning Levels and Scheduling Rules",
               "The four levels of production planning, the inputs a schedule needs, a worked example comparing three scheduling rules, and how to make the schedule stick.",
               ["operational-efficiency"], ["production planning", "production scheduling", "master production schedule", "S&OP", "scheduling rules", "manufacturing"],
               body + rel(r), "6 min read", "Planning", r)


# ═════════════════════════ 6. MRP ═════════════════════════
WEEKS = 6
STOOL_GROSS = [0, 40, 0, 60, 0, 50]
STOOL_ONHAND, STOOL_LT = 30, 1
LEG_ONHAND, LEG_LT, LEG_LOT = 100, 2, 150


def mrp_record(gross, onhand, lt, lot=None, receipts=None):
    receipts = receipts or [0] * WEEKS
    proj, net, por, rel_ = [], [], [0] * WEEKS, [0] * WEEKS
    oh = onhand
    for w in range(WEEKS):
        avail = oh + receipts[w]
        n = max(0, gross[w] - avail)
        q = 0 if n == 0 else (n if lot is None else math.ceil(n / lot) * lot)
        por[w] = q
        if q and w - lt >= 0: rel_[w - lt] = q
        oh = avail + q - gross[w]
        net.append(n); proj.append(oh)
    return proj, net, por, rel_


def mrp_table(label, gross, rec):
    proj, net, por, rel_ = rec
    head = ["", *[f"Wk {w + 1}" for w in range(WEEKS)]]
    rows = [("Gross requirements", *gross), ("Projected on hand", *proj), ("Net requirements", *net),
            ("Planned order receipts", *por), ("<strong>Planned order releases</strong>", *[f"<strong>{x}</strong>" if x else 0 for x in rel_])]
    return f"<p><strong>{label}</strong></p>\n" + table(head, [[str(c) for c in r] for r in rows])


def mrp():
    st = mrp_record(STOOL_GROSS, STOOL_ONHAND, STOOL_LT)
    leg_gross = [3 * x for x in st[3]]
    lg = mrp_record(leg_gross, LEG_ONHAND, LEG_LT, LEG_LOT)
    body = f"""
<p>Material requirements planning (MRP) works out which parts and materials you need, how many, and when to order or start making them, so that finished products can be built on time without holding piles of stock. It was developed in the 1960s and 1970s and is still the core of every manufacturing ERP. This guide, first published in 2023, has been rewritten around a worked example, because MRP is easiest to understand by doing one by hand.</p>
<h2>The three inputs</h2>
<ul>
<li><strong>Master production schedule:</strong> how many of each finished product you plan to make, and when.</li>
<li><strong>Bill of materials (BOM):</strong> the parts and quantities that go into each product, level by level.</li>
<li><strong>Inventory records:</strong> what is on hand and already on order, plus each item's lead time and ordering rule.</li>
</ul>
<h2>Worked example: a stool and its legs</h2>
<p>A workshop makes stools. Each stool needs one seat and three legs. The master schedule calls for {", ".join(f"{q} stools in week {w + 1}" for w, q in enumerate(STOOL_GROSS) if q)}. There are {STOOL_ONHAND} finished stools in stock, and assembly takes {STOOL_LT} week. Legs are bought in lots of {LEG_LOT} with a {LEG_LT}-week lead time, and {LEG_ONHAND} are in stock.</p>
<p>MRP works top-down. First the stool: subtract stock from demand to get net requirements, then offset each planned order by the lead time to find when it must be released.</p>
{mrp_table("Stool (assembly lead time 1 week, made to the exact quantity needed)", STOOL_GROSS, st)}
<p>The stool's planned order releases become the legs' gross requirements, multiplied by three. This step, called exploding the BOM, is what makes MRP different from simply reordering when stock runs low.</p>
{mrp_table(f"Legs (3 per stool; lead time {LEG_LT} weeks; ordered in lots of {LEG_LOT})", leg_gross, lg)}
<p>The result is a purchasing plan: order {", ".join(f"{q} legs in week {w + 1}" for w, q in enumerate(lg[3]) if q)}. Because legs come in lots of {LEG_LOT}, some stock carries over between orders. The seat would get its own record in the same way. Real systems do exactly this for thousands of items, and re-run it whenever orders or stock change.</p>
<h2>Choices that change the plan</h2>
<ul>
<li><strong>Lot sizing:</strong> ordering exactly what is needed keeps stock lowest; fixed lots or economic order quantities reduce ordering and set-up costs. See <a href="../post/reorder-point-and-eoq-when-to-order-and-how-much.html">reorder point and EOQ</a>.</li>
<li><strong>Safety stock:</strong> a buffer for items with unreliable supply or demand. See <a href="../post/setting-safety-stock.html">setting safety stock</a>.</li>
<li><strong>Lead times:</strong> the most common source of bad plans. If the system says 2 weeks and the supplier takes 4, every plan will be late.</li>
<li><strong>Capacity:</strong> basic MRP assumes unlimited capacity. Check the plan against machine and labour hours, or use a system with capacity planning.</li>
</ul>
<h2>Why MRP plans go wrong</h2>
<ol>
<li>Inaccurate inventory records. MRP is only as good as the stock count; aim for 95% record accuracy or better.</li>
<li>BOMs that do not match how the product is actually built.</li>
<li>A master schedule that changes every day, so the plan never settles. Freeze the near term.</li>
<li>People overriding the plan with their own spreadsheets because they do not trust it.</li>
</ol>
<p>For the software side, see <a href="../post/understanding-erp-vs-mrp-a-comprehensive-comparison-of-manufacturing-systems.html">ERP vs MRP</a> and <a href="../post/top-10-inventory-management-software-a-comprehensive-comparison-guide.html">inventory and MRP software for small businesses</a>.</p>
"""
    r = [("understanding-erp-vs-mrp-a-comprehensive-comparison-of-manufacturing-systems", "ERP vs MRP: which does your business need?"),
         ("reorder-point-and-eoq-when-to-order-and-how-much", "Reorder point and EOQ"),
         ("production-planning-and-scheduling-for-manufacturing", "Production planning and scheduling")]
    return art(MRP, "Material Requirements Planning (MRP) Explained with a Worked Example",
               "How MRP works: the three inputs, a worked stool-and-legs netting example with lead-time offsets and lot sizes, the choices that change the plan, and why plans fail.",
               ["process-improvement", "operational-efficiency", "erp", "inventory-management"],
               ["MRP", "material requirements planning", "bill of materials", "master production schedule", "lot sizing", "inventory"],
               body + rel(r), "7 min read", "MRP", r), st, lg


# ═════════════════════════ 7. ERP vs MRP ═════════════════════════
def fig_scope():
    s = DEFS
    s += f'<rect x="14" y="14" width="714" height="190" rx="14" fill="{PALE}" stroke="#9AB0C8"/>' + txt(30, 38, "ERP: the whole business", "start", NAVY, 14, True)
    mods = [("Accounting", 40, 56), ("Sales and CRM", 40, 112), ("HR and payroll", 40, 158), ("Purchasing", 560, 56), ("Warehouse", 560, 112), ("Quality, service", 560, 158)]
    for t, x, y in mods: s += box(x, y, 150, 36, t, fill="#fff", stroke="#9AB0C8", fs=12.5)
    s += f'<rect x="220" y="52" width="310" height="140" rx="12" fill="{GREENF}" stroke="{GREEND}" stroke-width="1.6"/>'
    s += txt(375, 76, "MRP: production and materials", "middle", GREEND, 13.5, True)
    for i, t in enumerate(["Bills of materials and routings", "Master schedule and material plan", "Work orders and shop floor", "Inventory of parts and materials"]):
        s += txt(375, 104 + i * 22, t, "middle", NAVY, 12.3)
    return svg("Scope of MRP and ERP. MRP covers production and materials: bills of materials and routings, the master schedule and "
               "material plan, work orders and the shop floor, and inventory of parts and materials. ERP covers the whole business: "
               "the MRP functions plus accounting, sales and CRM, HR and payroll, purchasing, warehouse, quality and service.", 742, 216, s, 600)


def evm():
    comp = [("Main purpose", "Plan materials and production", "Run the whole business on one system"),
            ("Typical users", "Planners, buyers, production supervisors", "Everyone: finance, sales, operations, HR"),
            ("Accounting", "Usually links to a separate package (QuickBooks, Xero, Sage)", "Built in: general ledger, payables, receivables"),
            ("Typical cost for a small manufacturer", "Tens to a few hundred dollars per user per month", "Higher, plus implementation that often costs more than the first years of licences"),
            ("Implementation", "Weeks to a few months", "Several months to a year"),
            ("Examples", "MRPeasy, Katana, Fishbowl Manufacturing", "Business Central, NetSuite, Odoo, Acumatica, SAP Business One")]
    body = f"""
<p>MRP (material requirements planning) and ERP (enterprise resource planning) are often confused because every manufacturing ERP contains MRP. The practical question for a small or mid-sized manufacturer is whether a focused MRP system is enough, or whether it is time for an ERP. This article, first published in 2023, has been rewritten as a decision guide.</p>
<h2>How they relate</h2>
{fig(fig_scope(), 1, "MRP is the production and materials core; ERP adds the rest of the business around it.")}
<h2>Side by side</h2>
{table(["", "MRP system", "ERP system"], comp)}
<h2>An MRP system is usually enough when</h2>
<ul>
<li>You have fewer than about 25 people using the system and one site.</li>
<li>Your accounting package works well and your accountant is happy with it.</li>
<li>The main pain is on the shop floor: shortages, late orders, no visibility of work in progress.</li>
<li>You need results in weeks, not a year-long project.</li>
</ul>
<h2>It is time to look at ERP when</h2>
<ul>
<li>You run several sites, companies or currencies.</li>
<li>Finance spends days each month reconciling the MRP system with accounting.</li>
<li>You need job or project costing that ties production directly to the ledger.</li>
<li>Customers or regulators require full traceability across sales, production and finance.</li>
<li>Sales, service and production each keep separate customer and order data.</li>
</ul>
<h2>A common path</h2>
<p>Many small manufacturers start with an MRP system linked to their accounting package and move to an ERP as they add sites or complexity. If you take that path, keep your item numbers, BOMs and routings clean from the start; they are what moves to the next system, and clean data shortens any future ERP project by months. Read <a href="../post/the-ultimate-guide-to-choosing-the-right-erp-for-your-business.html">choosing and implementing an ERP</a> and <a href="../post/10-best-erp-systems-for-small-and-medium-sized-enterprises.html">10 ERP systems for small and mid-sized businesses</a> when you get there.</p>
"""
    r = [("demystifying-mrp-a-comprehensive-guide-to-the-material-requirements-planning-process", "Material requirements planning (MRP), explained"),
         ("the-ultimate-guide-to-choosing-the-right-erp-for-your-business", "Choosing and implementing an ERP"),
         ("10-best-erp-systems-for-small-and-medium-sized-enterprises", "10 ERP systems for small and mid-sized businesses")]
    return art(EVM, "ERP vs MRP: Which Does Your Manufacturing Business Need?",
               "How MRP and ERP differ, a side-by-side comparison, signs an MRP system is enough, signs it is time for ERP, and a common upgrade path.",
               ["erp", "digital-technology"], ["ERP", "MRP", "manufacturing software", "small manufacturers", "ERP selection"],
               body + rel(r), "4 min read", "ERP", r)


# ═════════════════════════ 8. Six Sigma tools ═════════════════════════
UNITS, OPP, DEFECTS = 2400, 5, 36
DPMO = DEFECTS / (UNITS * OPP) * 1e6
SIGMA = NormalDist().inv_cdf(1 - DPMO / 1e6) + 1.5
LSL, USL, MEAN, SD = 9.70, 10.30, 10.08, 0.06
CP = (USL - LSL) / (6 * SD)
CPK = min(USL - MEAN, MEAN - LSL) / (3 * SD)
CPK_CENTRED = (USL - 10.0) / (3 * SD)


def fig_dmaic():
    s = DEFS
    ph = [("Define", "Problem, goal,; customer, scope"), ("Measure", "Baseline data;; check the gauge"), ("Analyze", "Find and prove; root causes"),
          ("Improve", "Test and; implement fixes"), ("Control", "Hold the gain;; hand over")]
    for i, (h, d) in enumerate(ph):
        x = 10 + i * 146
        s += box(x, 14, 130, 40, h, fill=NAVY, stroke=NAVY, tc="#fff", fs=14)
        words = [w.strip(" ;") for w in d.split("; ")]
        s += box(x, 60, 130, 52, words, fill=PALE, stroke="#9AB0C8", fs=11.5, bold=False)
        if i < 4: s += arrow(x + 132, 34, x + 144, 34)
    return svg("The five phases of DMAIC. Define: problem, goal, customer and scope. Measure: baseline data and a check of the "
               "measurement system. Analyze: find and prove root causes. Improve: test and implement solutions. Control: hold the gain "
               "and hand over.", 742, 122, s, 600)


def ss():
    tools = [("Define", "Project charter, SIPOC, voice of the customer, CTQ tree", "Agree what the problem is and what good looks like"),
             ("Measure", "Process map, data collection plan, measurement system analysis (gauge R&amp;R), baseline capability", "Know where you start, and trust the numbers"),
             ("Analyze", "Pareto chart, fishbone diagram, 5 whys, scatter plots, hypothesis tests, regression", "Separate the few real causes from the many possible ones"),
             ("Improve", "Brainstorming, design of experiments, FMEA, pilot runs, mistake-proofing", "Find the change that fixes the cause, and test it safely"),
             ("Control", "Control charts, control plan, standard work, visual management", "Keep the process where you put it")]
    body = f"""
<p>Six Sigma is a data-driven method for reducing defects and variation in a process. Its projects follow five phases, DMAIC: define, measure, analyze, improve and control. This guide, first published in 2023, has been rewritten to show which tools belong to which phase, with worked examples of the two calculations people most often get wrong.</p>
<h2>The DMAIC phases</h2>
{fig(fig_dmaic(), 1, "DMAIC: each phase ends with a short review before the next begins.")}
<h2>Tools by phase</h2>
{table(["Phase", "Common tools", "Purpose"], tools)}
<p>A small business rarely needs all of them. A process map, a Pareto chart, a fishbone diagram and a control chart cover most projects. The statistical tools matter when the cause is not obvious and a wrong guess would be expensive.</p>
<h2>Worked example 1: defects per million opportunities</h2>
<p>An accounts team issues {UNITS:,} invoices a month. Each invoice has {OPP} things that can go wrong (customer, items, prices, tax, terms). Last month, {DEFECTS} errors were found. Defects per million opportunities (DPMO) is {DEFECTS} ÷ ({UNITS:,} × {OPP}) × 1,000,000 = {DPMO:,.0f}. Using the standard conversion with a 1.5 sigma shift, that is about a {SIGMA:.1f} sigma process. "Six sigma" corresponds to 3.4 DPMO, so there is room to improve, but for an invoicing process {SIGMA:.1f} sigma may be good enough; the goal is set by what errors cost, not by the name of the method.</p>
<h2>Worked example 2: process capability, Cp and Cpk</h2>
<p>A machined shaft must be {LSL:.2f} to {USL:.2f} mm. Measurements show an average of {MEAN:.2f} mm with a standard deviation of {SD:.2f} mm.</p>
<ul>
<li><strong>Cp</strong>, which compares the tolerance width with the spread of the process, is ({USL:.2f} − {LSL:.2f}) ÷ (6 × {SD:.2f}) = {CP:.2f}.</li>
<li><strong>Cpk</strong>, which also accounts for how well the process is centred, is the smaller of ({USL:.2f} − {MEAN:.2f}) and ({MEAN:.2f} − {LSL:.2f}), divided by 3 × {SD:.2f} = {CPK:.2f}.</li>
</ul>
<p>The process has enough precision (Cp {CP:.2f}) but sits off-centre, which lowers Cpk to {CPK:.2f}. Re-centring it on 10.00 mm would raise Cpk to {CPK_CENTRED:.2f} with no other change. Many customers require a Cpk of at least 1.33. Capability figures are only meaningful if the process is stable, which a control chart confirms first.</p>
<h2>Lean and Six Sigma together</h2>
<p>Lean removes waste and waiting; Six Sigma removes defects and variation. Most improvement programs now use both: Lean tools to make work flow, and Six Sigma tools when a quality problem needs data to solve. Our <a href="../lean-six-sigma-training.html">Lean Six Sigma training</a> covers both.</p>
""" + src([("ASQ: The define, measure, analyze, improve, control (DMAIC) process", "https://asq.org/quality-resources/dmaic"),
           ("ASQ: Process capability indices", "https://asq.org/quality-resources/process-capability")])
    r = [("implement-process-improvements-part-1", "How to implement process improvements"),
         ("how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations", "How to use Lean to eliminate waste"),
         ("50-must-track-kpis-for-business-success-from-finance-to-product-development", "50 KPIs with formulas")]
    return art(SS, "Six Sigma Tools by DMAIC Phase, with DPMO and Cpk Worked Examples",
               "Which Six Sigma tools belong to each DMAIC phase, worked examples of DPMO and sigma level and of Cp and Cpk, and how Lean and Six Sigma fit together.",
               ["six-sigma"], ["Six Sigma", "DMAIC", "DPMO", "Cpk", "process capability", "control chart", "Lean Six Sigma"],
               body + rel(r), "6 min read", "Six Sigma", r)


if __name__ == "__main__":
    op = os.path.join(HERE, "original_dates.json")
    od = json.load(open(op, encoding="utf-8")); od.update(ORIGINAL)
    note = od.pop("_note"); json.dump({"_note": note, **dict(sorted(od.items()))}, open(op, "w", encoding="utf-8"), indent=1)
    m, st, lg = mrp()
    from v477_extra import expand
    for a in (pi(), kz(), s5(), toc(), pp(), m, evm(), ss()):
        a = expand(a)                                         # long-form sections (V4.77 owner's request)
        words = len(re.sub(r"<svg.*?</svg>|<[^>]+>", " ", a["body"], flags=re.S).split())
        a["read"] = f"{max(4, round(words / 200))} min read"
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"][:50], len(re.sub(r"<svg.*?</svg>|<[^>]+>", " ", a["body"], flags=re.S).split()), "words")
    for n, o in RULES: print(n, sched(o)[1:])
    print("stool", st); print("legs", lg)
    print(f"DPMO {DPMO:.0f} sigma {SIGMA:.2f}; Cp {CP:.2f} Cpk {CPK:.2f} centred {CPK_CENTRED:.2f}; TOC {GAIN_DAY}/day {GAIN_YR}/yr")
