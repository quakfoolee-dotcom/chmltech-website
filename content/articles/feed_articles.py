"""FEED series for Insights (Process Engineering): three articles with tables and inline SVG figures.

Usage:  python3 content/articles/feed_articles.py
Writes content/articles/<slug>.json for each article. Then run
        python3 content/gen/add_article.py <slug>
for each slug to build the pages (see README, "Adding a new article").
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, RED = "#0B2A5A", "#0B6FA4", "#8DC63F", "#4D7F12", "#C27712", "#5B5BD0", "#B43E3E"
MUTED, LINE, SAND, PALE, GREENF, ORANGEF = "#5A6475", "#D9D5CA", "#ECE9E1", "#E6F0F7", "#E4F1D3", "#FBEBD3"

S1 = "from-concept-to-construction-five-stages-of-a-process-plant-project"
S2 = "the-design-basis-ten-decisions-to-fix-before-engineering-starts"
S3 = "what-a-feed-package-contains-and-what-each-document-decides"
CAPEX = "engineering-capex-and-opex-estimation-for-process-plants"
L1 = f'<a href="{S1}.html">Post&nbsp;1</a>'
L2 = f'<a href="{S2}.html">Post&nbsp;2</a>'
L3 = f'<a href="{S3}.html">Post&nbsp;3</a>'
CSS = '<link rel="stylesheet" href="../assets/css/oee.css?v=4.36">'
NOTE = ('<p class="oee-note"><em>The plant, its capacity and its costs in this series are an illustrative example. '
        'The ranges and percentages are typical industry values and do not replace an estimate prepared for your project.</em></p>')


def svg(label, w, h, inner, minw=560):
    return (f'<svg role="img" aria-label="{label}" viewBox="0 0 {w} {h}" width="{w}" '
            f'style="max-width:100%;height:auto;display:block;margin:0 auto;min-width:{minw}px" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="Inter,system-ui,sans-serif" font-size="13">{inner}</svg>')


def fig(s, n, cap):
    return f'<figure>\n<div style="overflow-x:auto">{s}</div>\n<figcaption>Figure {n}. {cap}</figcaption>\n</figure>'


def box(x, y, w, h, lines, fill=PALE, stroke="#9AB0C8", tc=NAVY, bold=True, fs=13, rx=8):
    lines = lines if isinstance(lines, list) else [lines]
    lh = fs + 4; y0 = y + h / 2 - (len(lines) - 1) * lh / 2 + fs * 0.35
    t = "".join(f'<text x="{x + w / 2}" y="{y0 + i * lh:.1f}" text-anchor="middle" font-size="{fs}" fill="{tc}"'
                f'{" font-weight=\"600\"" if bold else ""}>{ln}</text>' for i, ln in enumerate(lines))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>' + t


def txt(x, y, s, anchor="start", fill=NAVY, fs=13, bold=False):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{fill}"{" font-weight=\"600\"" if bold else ""}>{s}</text>'


def arrow(x1, y1, x2, y2, col=NAVY, w=1.6):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" marker-end="url(#ah)"/>'


DEFS = f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{NAVY}"/></marker></defs>'


def smooth(pts):
    """Catmull-Rom spline through the points, as an SVG path."""
    d = f"M{pts[0][0]},{pts[0][1]}"
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]},{p2[1]}"
    return d


# ───────────────────────── Post 1: the five stages ─────────────────────────
def fig_stages():
    names = [["1. Concept"], ["2. Pre-FEED"], ["3. FEED"], ["4. Detailed design,", "purchasing and", "construction"], ["5. Commissioning", "and start-up"]]
    cls = ["Class 5 estimate", "Class 4 estimate", "Class 3 estimate", "Class 2, then Class 1", "Actual cost"]
    xs = [10, 164, 318, 472, 626]; s = DEFS
    for i, x in enumerate(xs):
        fe = i < 3
        s += box(x, 50, 124, 78, names[i], fill=PALE if fe else SAND, stroke="#9AB0C8" if fe else LINE, fs=12.5)
        s += txt(x + 62, 150, cls[i], "middle", MUTED, 12)
        if i < 4:
            gx = x + 139; key = i == 2
            s += f'<path d="M{gx},{75} L{gx + 13},{89} L{gx},{103} L{gx - 13},{89} z" fill="{GREEN if key else "#fff"}" stroke="{GREEND if key else NAVY}" stroke-width="1.5"/>'
            s += txt(gx, 30 if key else 38, "Final investment" if key else f"Gate {i + 1}", "middle", GREEND if key else MUTED, 12, key)
            if key: s += txt(gx, 45, "decision", "middle", GREEND, 12, True)
    s += f'<path d="M10,176 v8 h432 v-8" fill="none" stroke="{BLUE}" stroke-width="1.5"/>' + txt(226, 204, "Front-end loading: decide what to build", "middle", BLUE, 13, True)
    s += f'<path d="M472,176 v8 h278 v-8" fill="none" stroke="{MUTED}" stroke-width="1.5"/>' + txt(611, 204, "Execution: build it", "middle", MUTED, 13, True)
    return svg("Five project stages in a row: concept, pre-FEED, FEED, detailed design with purchasing and construction, and commissioning. "
               "A gate follows each of the first four stages. The gate after FEED is the final investment decision.", 760, 216, s, 640)


RANGES = [("Class 5", "Concept", 50, 100), ("Class 4", "Pre-FEED", 30, 50), ("Class 3", "FEED", 20, 30),
          ("Class 2", "Detailed design", 15, 20), ("Class 1", "Construction", 10, 15)]


def fig_funnel():
    X = lambda v: 190 + v * 2.24; s = ""
    for v in (0, 50, 100, 150, 200):
        s += f'<line x1="{X(v)}" y1="28" x2="{X(v)}" y2="232" stroke="{LINE}"/>' + txt(X(v), 250, f"${v}M", "middle", MUTED, 12)
    for i, (c, st, lo, hi) in enumerate(RANGES):
        y = 44 + i * 38; a, b = 100 * (1 - lo / 100), 100 * (1 + hi / 100)
        s += txt(10, y + 9, c, fill=NAVY, bold=True) + txt(70, y + 9, st, fill=MUTED, fs=12.5)
        s += f'<rect x="{X(a)}" y="{y - 6}" width="{X(b) - X(a):.1f}" height="22" rx="4" fill="{BLUE}" opacity="{0.45 + i * 0.12:.2f}"/>'
        s += txt(X(a) - 6, y + 9, f"${a:.0f}M", "end", NAVY, 12) + txt(X(b) + 6, y + 9, f"${b:.0f}M", "start", NAVY, 12)
    s += f'<line x1="{X(100)}" y1="22" x2="{X(100)}" y2="232" stroke="{NAVY}" stroke-width="1.6" stroke-dasharray="5 4"/>' + txt(X(100), 16, "$100M estimate", "middle", NAVY, 12.5, True)
    return svg("Range bars for a $100M estimate at each estimate class. Class 5 spans $50M to $200M, Class 4 $70M to $150M, Class 3 $80M to $130M, "
               "Class 2 $85M to $120M and Class 1 $90M to $115M.", 720, 262, s)


def fig_influence():
    xs = [60, 186, 312, 438, 564, 690]; Y = lambda v: 250 - v * 2.2; s = ""
    for i, n in enumerate(["Concept", "Pre-FEED", "FEED", "Design and build", "Start-up"]):
        if i % 2 == 0: s += f'<rect x="{xs[i]}" y="30" width="126" height="220" fill="{SAND}" opacity=".55"/>'
        s += txt(xs[i] + 63, 270, n, "middle", MUTED, 12.5)
    for v in (0, 50, 100):
        s += f'<line x1="56" y1="{Y(v)}" x2="690" y2="{Y(v)}" stroke="{LINE}"/>' + txt(50, Y(v) + 4, f"{v}%", "end", MUTED, 12)
    inf = [100, 82, 52, 22, 8, 3]; sp = [0, 0.4, 1.5, 4.5, 92, 100]
    s += f'<line x1="438" y1="30" x2="438" y2="250" stroke="{GREEND}" stroke-width="1.5" stroke-dasharray="5 4"/>' + txt(438, 22, "Final investment decision", "middle", GREEND, 12.5, True)
    s += f'<path d="{smooth([(x, round(Y(v), 1)) for x, v in zip(xs, inf)])}" fill="none" stroke="{BLUE}" stroke-width="3"/>'
    s += f'<path d="M60,250 C150,250 300,248 438,{Y(4.5):.1f} C500,{Y(8):.1f} 560,{Y(85):.1f} 690,30" fill="none" stroke="{ORANGE}" stroke-width="3"/>'
    s += txt(250, 78, "Ability to change the cost", fill=BLUE, bold=True) + txt(520, 200, "Money spent", fill=ORANGE, bold=True)
    return svg("Two curves across the five project stages. The ability to change the final cost starts near 100% and falls to about 20% by the "
               "final investment decision. Cumulative spending stays under 5% until that decision, then rises steeply during design and construction.", 720, 282, s)


def post1():
    rows = "".join(f'<tr><td class="nw">{c}</td><td>{st}</td><td class="num">−{lo}% to +{hi}%</td><td class="num">${100 * (1 - lo / 100):.0f}M</td>'
                   f'<td class="num">${100 * (1 + hi / 100):.0f}M</td><td class="num">${100 * (hi + lo) / 100:.0f}M</td></tr>' for c, st, lo, hi in RANGES)
    return f"""{CSS}<p><em>Part 1 of 3 in the FEED series.</em></p>
<p>Most of the cost of a process plant is fixed by decisions made on paper, long before any equipment is ordered. A stage-gate process puts those decisions in order. At each gate the owner asks one question and spends only enough to answer it.</p>
<p>This series follows one example: a specialty chemical producer planning a new plant with a first estimate of $100M. This post covers the five stages. {L2} covers the design basis, and {L3} covers the FEED package.</p>
<h2>The five stages</h2>
<p>Companies use different names for the stages, but the sequence is the same. The first three are called front-end loading (FEL). FEED stands for front-end engineering design and is the last of them.</p>
{fig(fig_stages(), 1, "The five stages and the gates between them. The largest commitment is made at the gate after FEED.")}
<p class="oee-cap">Table 1. What each stage answers and delivers</p>
<table>
<tr><th>Stage</th><th>Also called</th><th>Question it answers</th><th>Main deliverables</th></tr>
<tr><td class="nw">1. Concept</td><td>FEL-1, appraise</td><td>Is there a business case worth studying?</td><td>Block flow diagram, market and site assumptions, Class 5 estimate</td></tr>
<tr><td class="nw">2. Pre-FEED</td><td>FEL-2, select, feasibility study</td><td>Which process route, capacity and site?</td><td>Options compared, preliminary process flow diagrams (PFDs), design basis draft, Class 4 estimate</td></tr>
<tr><td class="nw">3. FEED</td><td>FEL-3, define, basic engineering</td><td>What exactly will we build, and what will it cost?</td><td>Piping and instrumentation diagrams (P&amp;IDs), equipment list, layout, hazard review, Class 3 estimate, schedule</td></tr>
<tr><td class="nw">4. Execution</td><td>Detailed engineering, procurement and construction (EPC)</td><td>Is it built to the design, on budget?</td><td>Construction drawings, purchase orders, installed plant</td></tr>
<tr><td class="nw">5. Start-up</td><td>Commissioning</td><td>Does it make product at the design rate?</td><td>Tested systems, trained operators, performance test</td></tr>
</table>
<p>Each gate has three possible outcomes: proceed, go back and rework, or stop. A project that stops at Gate 1 or Gate 2 has done its job. It cost little and prevented a larger loss.</p>
<h2>How accurate is the estimate at each stage?</h2>
<p>An estimate can only be as accurate as the design behind it. AACE International groups estimates into five classes by how much of the project is defined. Class 5 is the roughest and Class 1 is the most detailed. The ranges below are the widest typical values for process plants.</p>
<p class="oee-cap">Table 2. Estimate classes applied to a $100M estimate</p>
<table>
<tr><th>Class</th><th>Stage</th><th class="num">Typical accuracy</th><th class="num">Low</th><th class="num">High</th><th class="num">Spread</th></tr>
{rows}
</table>
{fig(fig_funnel(), 2, "The same $100M estimate at each class. The range is wider on the high side, because estimates miss scope more often than they add it.")}
<p>Two points follow from the table.</p>
<ul>
<li><strong>A Class 5 number is a screening figure.</strong> A $100M concept estimate means the plant will probably cost between $50M and $200M. It is enough to decide whether to study the project. It is too wide to set a budget.</li>
<li><strong>Class 3 is the usual basis for approval.</strong> After FEED, the range narrows to about $80M to $130M. Most owners and lenders take the final investment decision at this point. For more on how these estimates are built, see <a href="{CAPEX}.html">Engineering CAPEX and OPEX Estimation for Process Plants</a>.</li>
</ul>
<h2>Why the early stages matter most</h2>
<p>Early decisions are cheap to change and affect almost everything. A change of process route at the concept stage costs a few days of study. The same change during construction means scrapped equipment and rework.</p>
{fig(fig_influence(), 3, "Illustrative curves. The ability to change the final cost falls quickly, while most of the money is spent after the final investment decision.")}
<p>By the final investment decision, the owner has spent a few percent of the project cost and has already fixed most of the final cost. Front-end work is therefore the least expensive place to reduce cost and risk.</p>
<h2>How much to spend before committing</h2>
<p>A common rule of thumb is that front-end work costs 3% to 5% of the installed cost, with FEED as the largest part. The percentages run higher on small or first-of-a-kind projects.</p>
<p class="oee-cap">Table 3. Typical front-end spend for the $100M example</p>
<table>
<tr><th>Stage</th><th class="num">Share of installed cost</th><th class="num">Spend</th><th>What the money buys</th></tr>
<tr><td class="nw">1. Concept</td><td class="num">0.25% to 0.5%</td><td class="num">$250,000 to $500,000</td><td>A decision to study the project or drop it</td></tr>
<tr><td class="nw">2. Pre-FEED</td><td class="num">0.5% to 1%</td><td class="num">$500,000 to $1,000,000</td><td>One selected option and a design basis</td></tr>
<tr><td class="nw">3. FEED</td><td class="num">2% to 3%</td><td class="num">$2,000,000 to $3,000,000</td><td>A defined plant, a Class 3 estimate and an execution plan</td></tr>
<tr class="oee-total"><td>Total before approval</td><td class="num">2.75% to 4.5%</td><td class="num">$2,750,000 to $4,500,000</td><td></td></tr>
</table>
<p>Compare that with the estimate range. Moving from Class 4 to Class 3 narrows the spread from $80M to $50M. The owner pays about $2.5M for FEED and removes $30M of uncertainty before committing $100M.</p>
<h2>Four common mistakes</h2>
<ul>
<li><strong>Skipping pre-FEED.</strong> The team designs the first option in detail and never compares it with the alternatives.</li>
<li><strong>Using a Class 5 number as the budget.</strong> The first figure given to the board becomes the target, and every later estimate looks like an overrun.</li>
<li><strong>Starting FEED with an open design basis.</strong> Capacity or product specifications change during FEED and the work is done twice. {L2} lists the decisions to fix first.</li>
<li><strong>Ordering equipment before the P&amp;IDs are frozen.</strong> Long-lead items bought early often need modification after the hazard review.</li>
</ul>
<h2>What smaller projects can do</h2>
<p>A $5M project does not need five formal gates. Stages can be combined, and concept and pre-FEED often become one study. The questions should still be answered in the same order: business case, option, definition, then money.</p>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> Spend in stages and match the decision to the accuracy of the estimate. On a $100M plant, about $2.75M to $4.5M of front-end work takes the estimate from a range of $50M to $200M down to $80M to $130M.</p></div>
<div class="oee-next"><a class="oee-fwd" href="{S2}.html">Next: Post&nbsp;2, the design basis →</a></div>
{NOTE}"""


# ───────────────────────── Post 2: the design basis ─────────────────────────
HOURS = [(8000, "Continuous, 24/7"), (7000, "Continuous, longer shutdowns"), (6000, "Five days a week, 24 hours"), (4000, "Two shifts, five days")]
SHORT = ["Continuous", "Longer shutdowns", "24 hours, five days", "Two shifts, five days"]
RATE = lambda h: 50_000_000 / h
COSTF = lambda h: (RATE(h) / RATE(8000)) ** 0.6


def fig_rate():
    s = ""; Y = lambda v: 230 - v * 0.014
    for v in (0, 5000, 10000):
        s += f'<line x1="70" y1="{Y(v)}" x2="700" y2="{Y(v)}" stroke="{LINE}"/>' + txt(62, Y(v) + 4, f"{v:,}", "end", MUTED, 12)
    s += txt(16, 24, "Design rate, kg/h", fill=MUTED, fs=12)
    for i, (h, lab) in enumerate(HOURS):
        x = 105 + i * 150; r = RATE(h)
        s += f'<rect x="{x}" y="{Y(r):.1f}" width="90" height="{230 - Y(r):.1f}" rx="4" fill="{BLUE if i == 0 else "#7FB2CF"}"/>'
        s += txt(x + 45, Y(r) - 8, f"{r:,.0f} kg/h", "middle", NAVY, 13, True)
        s += txt(x + 45, 250, f"{h:,} h/y", "middle", NAVY, 12.5, True) + txt(x + 45, 267, SHORT[i], "middle", MUTED, 11.5)
    return svg("Bar chart of the design rate needed to make 50,000 tonnes a year at four operating schedules: 6,250 kg/h at 8,000 hours, "
               "7,143 kg/h at 7,000 hours, 8,333 kg/h at 6,000 hours and 12,500 kg/h at 4,000 hours.", 720, 278, s)


def fig_ripple():
    s = DEFS + box(20, 110, 150, 70, ["Design basis"], fill=NAVY, stroke=NAVY, tc="#fff", fs=15)
    s += box(230, 110, 150, 70, ["Heat and material", "balance"], fs=12.5) + arrow(170, 145, 228, 145)
    outs = [["PFDs and P&amp;IDs"], ["Equipment sizes", "and datasheets"], ["Utility loads"], ["Plot plan and", "layout"], ["Cost estimate", "and schedule"]]
    for i, o in enumerate(outs):
        y = 12 + i * 56
        s += box(470, y, 170, 44, o, fill=SAND, stroke=LINE, fs=12.5, bold=False)
        s += f'<path d="M380,145 C425,145 425,{y + 22} 468,{y + 22}" fill="none" stroke="{NAVY}" stroke-width="1.4" marker-end="url(#ah)"/>'
    return svg("The design basis feeds the heat and material balance, which in turn feeds five groups of documents: PFDs and P&IDs, equipment sizes "
               "and datasheets, utility loads, plot plan and layout, and the cost estimate and schedule.", 660, 292, s, 520)


def post2():
    dec = [("Capacity", "Annual production, in tonnes of saleable product. Minimum rate the plant must run at (turndown).", "Size of every item of equipment"),
           ("Operating schedule", "Hours per year, shifts, planned shutdowns.", "Hourly design rate, staffing"),
           ("Feedstocks", "Specification of each raw material, its range of quality and how it is delivered.", "Reactor design, purification steps, storage"),
           ("Products", "Specification and grades of each product, by-products and how they leave the site.", "Separation and finishing equipment, packaging"),
           ("Site conditions", "Location, design temperatures, elevation, seismic and wind data, soil conditions.", "Cooling design, structures, winterization"),
           ("Utilities", "What the site supplies and at what conditions: power, steam, cooling water, nitrogen, compressed air.", "New utility systems or tie-ins"),
           ("Battery limits", "What is inside the project and what is outside. Every tie-in point.", "Scope and cost estimate"),
           ("Codes and permits", "Design codes, provincial and municipal rules, emission and effluent limits.", "Materials, safety systems, treatment units"),
           ("Operating philosophy", "Batch or continuous, level of automation, spare equipment, days of storage.", "Control system, equipment count, tank sizes"),
           ("Future expansion and margins", "Allowance for later capacity, design margins on equipment, plant life.", "Plot space, line and utility sizing")]
    rows = "".join(f'<tr><td class="nw">{i + 1}. {a}</td><td>{b}</td><td>{c}</td></tr>' for i, (a, b, c) in enumerate(dec))
    hrs = "".join(f'<tr><td>{lab}</td><td class="num">{h:,} h/y</td><td class="num">{RATE(h):,.0f} kg/h</td><td class="num">{"Base" if h == 8000 else f"+{(RATE(h) / RATE(8000) - 1) * 100:.0f}%"}</td>'
                  f'<td class="num">{"Base" if h == 8000 else f"+{(COSTF(h) - 1) * 100:.0f}%"}</td></tr>' for h, lab in HOURS)
    return f"""{CSS}<p><em>Part 2 of 3 in the FEED series.</em></p>
<p>The design basis is a short document, usually 10 to 20 pages. It records the decisions that every other engineering document depends on. If one of them changes later, the change runs through the whole design.</p>
<p>{L1} set out the five project stages. The design basis is drafted in pre-FEED and frozen at the start of FEED. This post lists the ten decisions it should contain, using the same $100M specialty chemical plant.</p>
<h2>The ten decisions</h2>
<p class="oee-cap">Table 1. The ten decisions in a design basis</p>
<table>
<tr><th>Decision</th><th>What to fix</th><th>What it drives</th></tr>
{rows}
</table>
<p>Most of these are business decisions, and only the owner can make them. The engineer's role is to ask for each one, explain what depends on it and record the answer.</p>
<h2>Worked example: capacity and operating hours</h2>
<p>Suppose the owner wants 50,000 tonnes of product a year. That figure does not set the size of the plant until the operating hours are fixed. Equipment is sized for an hourly rate:</p>
<p class="oee-formula">Design rate = 50,000,000 kg ÷ 8,000 h = 6,250 kg/h</p>
<p>A continuous plant typically runs about 8,000 hours a year, which leaves time for maintenance shutdowns. Fewer hours mean a higher hourly rate and larger equipment for the same annual output.</p>
{fig(fig_rate(), 1, "Design rate needed to produce 50,000 tonnes a year at four operating schedules.")}
<p class="oee-cap">Table 2. Effect of operating hours on design rate and equipment cost</p>
<table>
<tr><th>Schedule</th><th class="num">Operating hours</th><th class="num">Design rate</th><th class="num">Rate against base</th><th class="num">Equipment cost against base</th></tr>
{hrs}
</table>
<p>The cost column uses the six-tenths rule, in which equipment cost rises with capacity to the power of 0.6. It is an approximation for screening. Even so, the choice between 8,000 and 6,000 hours changes the equipment cost by about 19%, and it is made in one line of the design basis.</p>
<h2>Why a late change costs so much</h2>
<p>The design basis sits at the start of a chain. It sets the heat and material balance, and the balance sets the documents that follow.</p>
{fig(fig_ripple(), 2, "Every later document is calculated from the design basis, so a change at the start has to be carried through all of them.")}
<p class="oee-cap">Table 3. What a 20% capacity increase affects, by when it is made</p>
<table>
<tr><th>When the change is made</th><th>What has to be redone</th><th>Relative cost</th></tr>
<tr><td>Pre-FEED</td><td>One line in the design basis and the option study</td><td>Low</td></tr>
<tr><td>During FEED</td><td>Balance, PFDs, equipment sizes, utility loads, estimate</td><td>Medium: weeks of rework</td></tr>
<tr><td>Detailed design</td><td>All of the above, plus vendor quotations, piping and structural design</td><td>High: months of delay</td></tr>
<tr><td>Construction</td><td>Purchased equipment replaced or modified, installed work removed</td><td>Very high</td></tr>
</table>
<h2>What a completed design basis looks like</h2>
<p>For the example plant, the summary page might read as follows.</p>
<p class="oee-cap">Table 4. Design basis summary for the example plant</p>
<table>
<tr><th>Item</th><th>Basis</th></tr>
<tr><td>Capacity</td><td class="nw">50,000 t/y of product, turndown to 50%</td></tr>
<tr><td>Operating schedule</td><td>8,000 h/y, continuous, one planned shutdown a year</td></tr>
<tr><td>Design rate</td><td class="nw">6,250 kg/h</td></tr>
<tr><td>Main feedstock</td><td>Delivered by rail car and tank truck, minimum purity 98%, 10 days of storage</td></tr>
<tr><td>Product</td><td>Two grades, minimum purity 99.5%, shipped in bulk and in 1,000 kg totes</td></tr>
<tr><td>Site</td><td>Existing industrial site, design temperatures −30°C to 35°C</td></tr>
<tr><td>Utilities from site</td><td>Power and natural gas. Cooling water, nitrogen and steam are in project scope.</td></tr>
<tr><td>Operating philosophy</td><td>Automated control from one control room, spare pumps on critical services</td></tr>
<tr><td>Expansion</td><td>Plot space and utility headers sized for a second train</td></tr>
</table>
<h2>Three rules for managing it</h2>
<ul>
<li><strong>The owner signs it.</strong> A signed design basis is the agreed starting point. Later changes go through a formal change request with a cost and schedule estimate.</li>
<li><strong>Open items are listed.</strong> Any value still unknown is marked as a hold, with a named person and a date. A hold that is still open at the end of FEED becomes a risk in the estimate.</li>
<li><strong>Each value has a source.</strong> A specification from a customer contract carries more weight than a figure someone remembered. Record which one it is.</li>
</ul>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> Fix the ten decisions before FEED starts and have the owner sign them. On the example plant, one of them alone, operating hours, moves equipment cost by 8% to 52%.</p></div>
<div class="oee-next"><a href="{S1}.html">← Post&nbsp;1: the five stages</a><a class="oee-fwd" href="{S3}.html">Next: Post&nbsp;3, the FEED package →</a></div>
{NOTE}"""


# ───────────────────────── Post 3: the FEED package ─────────────────────────
BUILD = [("Equipment", 30.0, BLUE), ("Bulk materials", 15.0, "#7FB2CF"), ("Construction labour", 22.5, PURPLE),
         ("Engineering and project management", 12.5, GREEND), ("Owner's and other indirect costs", 10.0, ORANGE), ("Contingency", 10.0, RED)]


def fig_flow():
    s = DEFS
    tiers = [("Define the process", PALE, "#9AB0C8", [["Design basis"], ["Heat and material", "balance, PFDs"], ["P&amp;IDs"], ["Hazard review", "(HAZOP)"]]),
             ("Define the plant", SAND, LINE, [["Equipment list", "and datasheets"], ["Plot plan", "and layout"], ["Electrical and", "instrument lists"], ["Vendor budget", "quotations"]]),
             ("Define the project", GREENF, "#A9C77E", [["Class 3 cost", "estimate"], ["Schedule"], ["Execution and", "contracting plan"], ["Risk register"]])]
    for r, (name, fill, st, bxs) in enumerate(tiers):
        y = 40 + r * 104
        s += txt(10, y - 8, name, fill=NAVY, fs=13, bold=True)
        for i, b in enumerate(bxs):
            x = 10 + i * 186
            s += box(x, y, 162, 52, b, fill=fill, stroke=st, fs=12.5, bold=False)
            if r == 0 and i < 3: s += arrow(x + 162, y + 26, x + 184, y + 26)
        if r < 2: s += arrow(370, y + 56, 370, y + 78, w=2)
    # Feedback from the hazard review to the P&IDs: dashed line that runs straight down into a drawn arrowhead.
    s += f'<path d="M649,40 V22 Q649,12 639,12 H473 Q463,12 463,22 V26" fill="none" stroke="{NAVY}" stroke-width="1.4" stroke-dasharray="4 3"/>'
    s += f'<line x1="463" y1="24" x2="463" y2="32" stroke="{NAVY}" stroke-width="1.4"/><path d="M457.5,31 L468.5,31 L463,40 z" fill="{NAVY}"/>'
    s += txt(556, 29, "actions", "middle", MUTED, 11.5)
    return svg("Three tiers of FEED documents. The process tier runs from the design basis through the heat and material balance and PFDs to the P&IDs "
               "and the hazard review, whose actions feed back into the P&IDs. The plant tier holds the equipment list, plot plan, electrical and instrument "
               "lists and vendor quotations. The project tier holds the Class 3 estimate, schedule, execution plan and risk register.", 760, 306, s, 640)


def fig_build():
    s = ""; x = 20.0; tot = sum(v for _, v, _ in BUILD)
    for n, v, c in BUILD:
        w = v / tot * 680
        s += f'<rect x="{x:.1f}" y="20" width="{w:.1f}" height="46" fill="{c}"/>' + txt(x + w / 2, 48, f"${v:g}M", "middle", "#fff", 13, True)
        x += w
    for i, (n, v, c) in enumerate(BUILD):
        cx = 20 + (i % 2) * 350; cy = 96 + (i // 2) * 26
        s += f'<rect x="{cx}" y="{cy - 11}" width="12" height="12" rx="2" fill="{c}"/>' + txt(cx + 20, cy, f"{n}: ${v:g}M ({v / tot * 100:g}%)", fill=NAVY, fs=12.5)
    return svg("Stacked bar of a $100M estimate: equipment $30M, bulk materials $15M, construction labour $22.5M, engineering and project management $12.5M, "
               "owner's and other indirect costs $10M and contingency $10M.", 720, 164, s)


def post3():
    docs = [("Process", "Design basis", "The agreed starting assumptions", "Rework when capacity or specifications change"),
            ("Process", "Heat and material balance with PFDs", "Every stream: flow, composition, temperature and pressure", "Equipment sized on guesses"),
            ("Process", "P&amp;IDs", "Every pipe, valve, instrument and control loop", "Scope missed in the estimate, late design changes"),
            ("Process", "Equipment list and datasheets", "Size, duty and material of each item", "Vendors cannot quote, so costs are factored"),
            ("Process", "Utility summary", "Peak and normal demand for power, steam, cooling and gases", "Undersized utilities found at start-up"),
            ("Safety", "Hazard review (HAZID or HAZOP)", "Safeguards the design needs", "Safety changes made during construction"),
            ("Safety", "Relief and hazardous area studies", "Relief device loads, electrical classification", "Wrong equipment ratings, permit delays"),
            ("Layout", "Plot plan and equipment layout", "Where everything sits and how it is reached", "Piping and civil quantities unknown"),
            ("Electrical and controls", "Single-line diagram, load list, instrument index", "Power supply and control system size", "Electrical cost, often 10% or more, estimated blind"),
            ("Project", "Class 3 estimate and basis of estimate", "The budget and its accuracy range", "Approval based on an unreliable number"),
            ("Project", "Schedule and long-lead list", "Duration and what to order first", "Late equipment drives the completion date"),
            ("Project", "Execution plan and risk register", "How the work will be contracted and what could go wrong", "Disputes over scope during construction")]
    rows = "".join(f'<tr><td class="nw">{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in docs)
    tot = sum(v for _, v, _ in BUILD)
    brow = "".join(f'<tr><td>{n}</td><td class="num">${v * 1e6:,.0f}</td><td class="num">{v / tot * 100:g}%</td><td>{src}</td></tr>' for (n, v, _), src in zip(BUILD, [
        "Vendor budget quotations against datasheets", "Quantities taken from P&amp;IDs and layout", "Hours estimated from quantities and local rates",
        "Planned hours by discipline", "Permits, spares, commissioning, owner's team", "Set from the risk register"]))
    return f"""{CSS}<p><em>Part 3 of 3 in the FEED series.</em></p>
<p>FEED, or front-end engineering design, turns a selected concept into a defined plant. It ends with a package of documents that an owner can approve, a lender can review and a contractor can bid on.</p>
<p>{L1} placed FEED as the third of five project stages. {L2} covered the design basis that FEED starts from. This post goes through what the package contains, using the same $100M specialty chemical plant.</p>
<h2>What FEED has to produce</h2>
<p>A FEED package answers three questions.</p>
<ul>
<li><strong>What are we building?</strong> A scope defined well enough that two engineers would design the same plant from it.</li>
<li><strong>What will it cost?</strong> A Class 3 estimate, typically accurate to between −20% and +30%.</li>
<li><strong>How will we build it?</strong> A schedule, a contracting plan and a list of risks.</li>
</ul>
<p>The documents are produced in a set order, because each one is calculated from the one before.</p>
{fig(fig_flow(), 1, "The main FEED documents in three tiers. Each tier is built from the one above it. Actions from the hazard review go back into the P&amp;IDs.")}
<h2>The documents and what each one decides</h2>
<p class="oee-cap">Table 1. Main FEED deliverables</p>
<table>
<tr><th>Group</th><th>Document</th><th>What it decides</th><th>If it is skipped</th></tr>
{rows}
</table>
<p>A package for a small plant may combine some of these. None of the questions in the third column can be left unanswered.</p>
<h2>PFD and P&amp;ID: the two drawings to know</h2>
<p>Owners are asked to review both drawings, and they serve different purposes.</p>
<p class="oee-cap">Table 2. PFD and P&amp;ID compared</p>
<table>
<tr><th></th><th>Process flow diagram (PFD)</th><th>Piping and instrumentation diagram (P&amp;ID)</th></tr>
<tr><td class="nw">Purpose</td><td>Shows how the process works</td><td>Shows how the plant is built and controlled</td></tr>
<tr><td class="nw">Shows</td><td>Main equipment, main streams, key operating conditions</td><td>Every line, valve, instrument, control loop and relief device</td></tr>
<tr><td class="nw">Typical count</td><td class="nw">10 to 20 sheets</td><td class="nw">80 to 150 sheets</td></tr>
<tr><td class="nw">Used for</td><td>Heat and material balance, equipment sizing</td><td>Hazard review, cost estimate, construction, operation</td></tr>
<tr><td class="nw">Owner should check</td><td>Capacity, feeds and products match the design basis</td><td>Operators can start, stop, isolate and maintain each item</td></tr>
</table>
<p>The sheet counts are for a plant of the example's size. The P&amp;IDs are the most important drawings in the package, because the hazard review, the estimate and the construction scope are all taken from them.</p>
<h2>How the Class 3 estimate is built</h2>
<p>A Class 3 estimate is built up from the documents and is no longer factored from a single number. Each line has a source in the package.</p>
{fig(fig_build(), 2, "Illustrative build-up of the $100M estimate for the example plant.")}
<p class="oee-cap">Table 3. Estimate build-up and the source of each line</p>
<table>
<tr><th>Cost element</th><th class="num">Amount</th><th class="num">Share</th><th>Where the number comes from</th></tr>
{brow}
<tr class="oee-total"><td>Total installed cost</td><td class="num">${tot * 1e6:,.0f}</td><td class="num">100%</td><td></td></tr>
</table>
<p>Equipment is under a third of the total. The rest is the cost of installing it, connecting it and managing the work. An estimate that prices the equipment well and factors everything else has not reached Class 3. The methods are covered in <a href="{CAPEX}.html">Engineering CAPEX and OPEX Estimation for Process Plants</a>.</p>
<h2>What FEED does not include</h2>
<p>FEED stops short of construction drawings. Piping isometrics, structural steel details, cable schedules and vendor fabrication drawings belong to detailed engineering, which follows approval. That work typically costs three to five times as much as FEED, so it should start only after the investment decision.</p>
<h2>Eight questions to ask when you receive a FEED package</h2>
<ol>
<li>Is the design basis signed, and are any holds still open?</li>
<li>Does the heat and material balance close, and does it match the capacity in the design basis?</li>
<li>Have the P&amp;IDs been through a hazard review, and are the actions closed or listed?</li>
<li>How much of the equipment cost is backed by vendor quotations?</li>
<li>Does the estimate state its class, its accuracy range and its exclusions?</li>
<li>Is contingency tied to named risks?</li>
<li>Which items have the longest delivery, and when must they be ordered?</li>
<li>What is outside the battery limits, and who pays for it?</li>
</ol>
<p>A package that answers all eight is ready for an investment decision. A gap in any of them is a reason to extend FEED before committing the full budget.</p>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> A FEED package defines the scope, the cost and the plan. Judge it by whether each number in the estimate can be traced to a document in the package.</p></div>
<div class="oee-next oee-end"><a href="{S1}.html">← Post&nbsp;1: the five stages</a><a href="{S2}.html">← Post&nbsp;2: the design basis</a></div>
{NOTE}"""


ARTICLES = [
    dict(slug=S1, title="From Concept to Construction: The Five Stages of a Process Plant Project",
         desc="The five stages of a process plant project, the decision at each gate, how accurate the cost estimate is at each stage, and how much to spend before committing.",
         tags=["FEED", "front-end loading", "stage-gate", "AACE estimate classes", "capital projects"], body=post1(), related=[S2, S3, CAPEX]),
    dict(slug=S2, title="The Design Basis: Ten Decisions to Fix Before Engineering Starts",
         desc="The ten decisions a design basis must record before FEED starts, with a worked example showing how operating hours alone change equipment cost.",
         tags=["design basis", "FEED", "plant capacity", "six-tenths rule", "process design"], body=post2(), related=[S1, S3, CAPEX]),
    dict(slug=S3, title="What a FEED Package Contains, and What Each Document Decides",
         desc="The documents in a FEED package, what each one decides, how the Class 3 estimate is built from them, and eight questions to ask before you approve the project.",
         tags=["FEED", "P&ID", "PFD", "Class 3 estimate", "HAZOP", "basic engineering"], body=post3(), related=[S1, S2, CAPEX]),
]

if __name__ == "__main__":
    for i, a in enumerate(ARTICLES):
        words = len(re.sub(r"<svg.*?</svg>|<[^>]+>", " ", a["body"], flags=re.S).split())
        a.update(cats=["process-engineering", "project-management"], date="2026-11-11", author="Quak Foo Lee",
                 read=f"{max(1, round(words / 220))} min read", cover_label="Process Engineering")
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"], words, "words,", a["read"])
