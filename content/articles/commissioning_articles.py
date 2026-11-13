"""Commissioning series for Insights (Process Engineering), three articles (V4.68).

Part 1  From mechanical completion to handover: the commissioning sequence
Part 2  The pre-startup safety review: what to check before hazardous materials go in
Part 3  First run to steady state: start-up, the punch list and the performance test

The example is the 50,000 t/y, $100M plant of the FEED and scale-up series, and the feed section
(T-101, P-101, E-101, R-101) from the PFD/P&ID and HAZOP posts.

Usage:  python3 content/articles/commissioning_articles.py
        python3 content/gen/add_article.py <slug>   (each)
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import (nowrap, svg, fig, box, txt, arrow, DEFS, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, RED,
                           MUTED, LINE, SAND, PALE, GREENF, ORANGEF, S1 as FEED1)
from process_eng_articles import PF as PFDPID, U3 as MEB
from refresh_articles import src

C1 = "from-mechanical-completion-to-handover-the-commissioning-sequence"
C2 = "the-pre-startup-safety-review-what-to-check-before-start-up"
C3 = "first-run-to-steady-state-start-up-punch-list-and-performance-test"
HAZOP = "a-worked-hazop-the-feed-heater-node-by-node"
MOC = "management-of-change-for-small-plants"
RLF = "pressure-relief-basics-what-a-psv-protects-against"
DATE = "2026-11-13"
L = {1: f'<a href="{C1}.html">Part&nbsp;1</a>', 2: f'<a href="{C2}.html">Part&nbsp;2</a>', 3: f'<a href="{C3}.html">Part&nbsp;3</a>'}
NOTE = ('<p class="oee-note"><em>The plant, schedule and numbers in this series are an illustrative example. Commissioning and start-up '
        'must follow your own procedures, the vendors\' instructions and the regulations that apply where you operate.</em></p>')
SER = lambda n: {"name": "Commissioning series", "part": n, "of": 3}
OSHA = ("U.S. eCFR: 29 CFR 1910.119, Process safety management of highly hazardous chemicals",
        "https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XVII/part-1910/subpart-H/section-1910.119")

# ── performance test example ──
FEED_KG = 72 * 11_000.0          # kg of reactant fed over a 72 h test (illustrative)
PROD_KG = 72 * 9_700.0           # kg of product made
STOICH = 1.0                     # kg product per kg reactant at 100 % yield (illustrative)
YIELD = PROD_KG / (FEED_KG * STOICH)
U_FEED, U_PROD, U_ASSAY = 0.010, 0.010, 0.005     # relative standard uncertainties
U_YIELD = math.sqrt(U_FEED ** 2 + U_PROD ** 2 + U_ASSAY ** 2)
GUAR = 0.87
IN_T, OUT_T = 1_000.0, 982.0     # t in and out over the test for the closure example
CLOSURE = OUT_T / IN_T


def fig_sequence():
    s = DEFS
    st = [("Construction", PALE), ("Mechanical\ncompletion", PALE), ("Pre-\ncommissioning", SAND), ("Commissioning", SAND),
          ("Pre-startup\nsafety review", ORANGEF), ("Start-up", GREENF), ("Performance\ntest", GREENF), ("Handover", GREENF)]
    xs = [8 + i * 108 for i in range(8)]
    for i, ((t, fc), x) in enumerate(zip(st, xs)):
        s += box(x, 60, 98, 58, t.split("\n"), fill=fc, stroke="#9AB0C8", fs=12.5)
        if i < 7: s += arrow(x + 98, 89, x + 107, 89)
    for x, lab, col in ((xs[1] + 49, "MC certificate", NAVY), (xs[3] + 49, "Ready for start-up", NAVY), (xs[4] + 49, "Go / no-go", ORANGE), (xs[6] + 49, "Acceptance", GREEND)):
        s += f'<path d="M{x},126 l7,10 l-7,10 l-7,-10 z" fill="#fff" stroke="{col}" stroke-width="1.5"/>' + txt(x, 162, lab, "middle", col, 11.5, True)
    s += f'<path d="M{xs[0]},44 h{xs[1] + 98 - xs[0]}" stroke="{MUTED}" stroke-width="1.4"/>' + txt((xs[0] + xs[1] + 98) / 2, 36, "Construction team", "middle", MUTED, 12, True)
    s += f'<path d="M{xs[2]},44 h{xs[4] + 98 - xs[2]}" stroke="{BLUE}" stroke-width="1.4"/>' + txt((xs[2] + xs[4] + 98) / 2, 36, "Commissioning team: no process fluids", "middle", BLUE, 12, True)
    s += f'<path d="M{xs[5]},44 h{xs[7] + 98 - xs[5]}" stroke="{GREEND}" stroke-width="1.4"/>' + txt((xs[5] + xs[7] + 98) / 2, 36, "Operations lead: process fluids in", "middle", GREEND, 12, True)
    return svg("Eight stages in a row: construction, mechanical completion, pre-commissioning, commissioning, pre-startup safety review, start-up, performance test and handover. "
               "Gates are marked after mechanical completion (the MC certificate), after commissioning (ready for start-up), at the safety review (go or no-go) and after the performance test (acceptance). "
               "Brackets above show the construction team, then the commissioning team working without process fluids, then operations leading once process fluids are introduced.",
               876, 172, s, 700, x0=4)


def fig_ramp():
    X = lambda h: 80 + h / 120 * 600; Y = lambda p: 230 - p / 100 * 190
    s = ""
    for p in (0, 25, 50, 75, 100):
        s += f'<line x1="80" y1="{Y(p)}" x2="680" y2="{Y(p)}" stroke="{LINE}"/>' + txt(72, Y(p) + 4, f"{p}%", "end", MUTED, 12)
    for h in range(0, 121, 24):
        s += txt(X(h), 250, f"{h} h", "middle", MUTED, 12)
    pts = [(0, 0), (6, 0), (8, 30), (24, 30), (26, 50), (48, 50), (50, 75), (66, 75), (68, 100), (120, 100)]
    s += '<polyline fill="none" stroke="' + BLUE + '" stroke-width="2.6" points="' + " ".join(f"{X(h):.1f},{Y(p):.1f}" for h, p in pts) + '"/>'
    for h, p, lab in ((14, 8, "0–6 h: utilities, inerting, solvent circulation and heat-up"), (16, 30, "First feed at 30%"), (37, 50, "Hold: check balances"),
                      (58, 75, "Hold: tune loops"), (94, 100, "Design rate; performance test follows")):
        s += txt(X(10) if p == 8 else X(h), Y(p) - (2 if p == 8 else 10), lab, "start" if p == 8 else "middle", NAVY, 12, True)
    s += txt(380, 272, "Hours from first feed preparation", "middle", NAVY, 12.5, True)
    return svg("Chart of plant rate against time. Zero for the first six hours while utilities are brought in, the plant is inerted and solvent is circulated and heated. "
               "First feed at 30 percent, held until 24 hours; then 50 percent to 48 hours with a check of the balances; 75 percent to 66 hours while loops are tuned; "
               "then 100 percent design rate, after which the performance test follows.", 700, 282, s, 600, x0=0)


def part1():
    body = f"""{CSS}
<p>A plant can be fully built and still be weeks from making product. The gap is commissioning: proving, system by system, that what was built works as designed, and only then putting process materials into it. Projects that rush this stage tend to pay for it at start-up, with leaks, trips, damaged equipment and, at worst, incidents.</p>
<p>This three-part series follows the 50,000&nbsp;t/y plant from the <a href="{FEED1}.html">FEED series</a> from the end of construction to handover. This part sets out the sequence. {L[2]} covers the pre-startup safety review, the last check before hazardous materials go in. {L[3]} covers start-up, the punch list and the performance test.</p>
<h2>The sequence</h2>
{fig(fig_sequence(), 1, "The commissioning sequence, with the gates between stages and who leads each stage.")}
<table>
<tr><th>Stage</th><th>What it proves</th><th>Typical activities</th></tr>
<tr><td>Mechanical completion</td><td>The system is built as designed and tested for integrity</td><td>Walkdown against P&amp;IDs, pressure tests, punch list, completion certificate</td></tr>
<tr><td>Pre-commissioning</td><td>Each component works on its own, with no process fluids</td><td>Flushing and cleaning, instrument calibration, loop checks, motor rotation and run-in, valve stroking</td></tr>
<tr><td>Commissioning</td><td>Systems work together, on water, air, nitrogen or solvent</td><td>Water runs, utility start-up, control loop checks, alarm tests, safety function testing</td></tr>
<tr><td>Pre-startup safety review</td><td>The plant is safe to receive hazardous materials</td><td>Review against design, procedures, training, hazard study actions</td></tr>
<tr><td>Start-up</td><td>The plant runs on process materials</td><td>First feed at reduced rate, stepwise increase to design rate</td></tr>
<tr><td>Performance test</td><td>The plant meets its design and guarantees</td><td>Sustained test at design rate with measured inputs and outputs</td></tr>
<tr><td>Handover</td><td>Responsibility passes to operations</td><td>Documents, spares, training records, remaining punch items</td></tr>
</table>
<h2>Systemization: the unit of commissioning</h2>
<p>A plant is not commissioned all at once. It is divided into <strong>systems</strong>, each a set of equipment that can be tested together, with clear boundaries on the P&amp;IDs. Each system gets a test pack: the drawings marked up with its boundary, the test procedures, the check sheets and the punch list. Construction hands over by system, so commissioning can start on the first systems while others are still being built.</p>
<table>
<tr><th>System</th><th>Boundary</th><th>Key commissioning tests</th></tr>
<tr><td>Electrical supply</td><td>Substation to motor control centres</td><td>Protection relay tests, energization, motor rotation</td></tr>
<tr><td>Control and safety systems</td><td>DCS, safety system, field instruments</td><td>Loop checks, alarm tests, cause and effect testing of every safety function</td></tr>
<tr><td>Steam and condensate</td><td>Boiler or header to E-101 and condensate return</td><td>Steam blowing to clean lines, trap checks, heat-up of E-101 on water</td></tr>
<tr><td>Cooling water</td><td>Pumps, tower, R-101 jacket</td><td>Flow and temperature checks at design load</td></tr>
<tr><td>Feed system</td><td>T-101, P-101, E-101 to R-101 inlet</td><td>Flushing, P-101 run on water or solvent, flow control, level trips on T-101</td></tr>
<tr><td>Reactor</td><td>R-101 with agitator, jacket and vent</td><td>Agitator run, temperature control on solvent, emergency cooling and vent tests</td></tr>
<tr><td>Vent and relief</td><td>Relief valves, headers, knock-out drum, flare or scrubber</td><td>Valve set pressures certified, block valves car-sealed open, flare pilot lit</td></tr>
</table>
<p>Utilities come first, because everything else needs them. Then the control and safety systems, because nothing should be operated without its protections working. Then the process systems, in the order the process runs.</p>
<h2>Pre-commissioning in practice</h2>
<p>Pre-commissioning is the unglamorous work that prevents most start-up problems. For the feed system it includes:</p>
<ul>
<li><strong>Flushing and cleaning.</strong> Construction debris left in pipes ends up in pump impellers, control valves and exchanger tubes. Temporary strainers protect the pumps for the first weeks.</li>
<li><strong>Leak and pressure testing.</strong> Hydrostatic tests prove the strength of the piping at the time of construction. A leak test with nitrogen before start-up finds the flanges disturbed since.</li>
<li><strong>Instrument loop checks.</strong> Each instrument is checked from the field device to the control room display, so that a high level in T-101 shows as a high level on the right screen and trips the right pump.</li>
<li><strong>Rotating equipment.</strong> Motors are run uncoupled to check rotation and vibration, then coupled and aligned. Pumps are not run dry.</li>
</ul>
<h2>Commissioning: proving the systems together</h2>
<p>With components proven, systems are run together on safe fluids. The feed system runs on water or the plant solvent, P-101 pushing through E-101 into R-101, with flow controlled and E-101 heated on steam. Control loops are tuned. Alarms are triggered from the field. Every safety instrumented function is tested end to end, from sensor to final element, against the cause and effect diagram. The functional safety standard IEC 61511 requires the safety system to be validated before the hazards it protects against are present.</p>
<p>Water runs also test the people. Operators run the plant on their procedures, find the steps that are wrong or missing, and fix them before the procedures matter.</p>
<h2>Who leads, and when</h2>
<p>The handover points in Figure&nbsp;1 are also changes of responsibility. Construction leads until mechanical completion. A commissioning team, usually a mix of the engineering contractor, vendors and the owner's future operators, leads until the plant is ready for start-up. Operations leads once process materials are in. Projects that blur these lines tend to discover, during start-up, that nobody owned a particular check.</p>
<h2>Key points</h2>
<ul>
<li>Commissioning proves the plant works before process materials go in, one system at a time.</li>
<li>Divide the plant into systems with clear boundaries and a test pack each; start with utilities and the control and safety systems.</li>
<li>Pre-commissioning (cleaning, testing, loop checks, run-in) prevents most start-up problems.</li>
<li>Test every safety function end to end before the hazard is present.</li>
<li>Be clear who leads each stage and what proves it is complete.</li>
</ul>
<p>Next: {L[2]}, the pre-startup safety review.</p>
{NOTE}"""
    body = nowrap(body, [(1, 0, 26), (2, 0, 26)])
    return dict(slug=C1, title="From Mechanical Completion to Handover: The Commissioning Sequence",
                desc="How a process plant is commissioned: the stages from mechanical completion to handover, systemization, pre-commissioning checks and who leads when.",
                cats=["process-engineering"], tags=["commissioning", "mechanical completion", "pre-commissioning", "systemization", "start-up", "process plant"],
                body=body, date=DATE, author="Quak Foo Lee", read="7 min read", series=SER(1), cover_label="Commissioning",
                related=[C2, C3, FEED1])


def part2():
    body = f"""{CSS}
<p>There is a moment in every project when hazardous material is about to enter equipment for the first time. Before it does, someone has to be satisfied that the plant is ready: built as designed, with its protections working, its procedures written and its people trained. In process safety that check is the <strong>pre-startup safety review</strong> (PSSR).</p>
<p>{L[1]} set out the commissioning sequence. This part explains what the PSSR covers, who should do it, and how it works on the feed section from the <a href="{HAZOP}.html">worked HAZOP</a>.</p>
<h2>Where the requirement comes from</h2>
<p>In the United States, the OSHA process safety management standard requires a pre-startup safety review for new facilities and for modified facilities when the modification is significant enough to require a change in the process safety information. It must confirm, before highly hazardous chemicals are introduced, that:</p>
<ul>
<li>construction and equipment are in accordance with design specifications;</li>
<li>safety, operating, maintenance and emergency procedures are in place and adequate;</li>
<li>for new facilities, a process hazard analysis has been performed and its recommendations resolved or implemented before start-up, and modified facilities meet the management of change requirements; and</li>
<li>training of each employee involved in operating the process has been completed.</li>
</ul>
<p>Canada has no single federal equivalent, but the same elements appear in the CSA Z767 standard for process safety management and in provincial requirements for regulated facilities. Whatever the jurisdiction, the four questions above are good practice for any plant handling hazardous materials, and for small plants that are not regulated as major hazard sites.</p>
<h2>What the review covers</h2>
<table>
<tr><th>Area</th><th>Questions the review asks</th><th>Evidence</th></tr>
<tr><td>Built as designed</td><td>Does the plant match the latest P&amp;IDs? Are materials, ratings and supports as specified?</td><td>Walkdown with marked-up P&amp;IDs; mechanical completion certificates</td></tr>
<tr><td>Integrity</td><td>Have pressure tests and leak tests passed? Are temporary blinds and strainers recorded?</td><td>Test records; blind list</td></tr>
<tr><td>Relief and protection</td><td>Are relief valves installed, set and certified, with block valves car-sealed open? Have all safety functions been tested?</td><td>Relief valve certificates; safety function test records</td></tr>
<tr><td>Hazard study actions</td><td>Is every HAZOP action closed, or accepted as not needed before start-up with a reason?</td><td>Action register with sign-offs</td></tr>
<tr><td>Changes</td><td>Has every change since the HAZOP been through management of change?</td><td>MOC records</td></tr>
<tr><td>Procedures</td><td>Are operating, start-up, shutdown, emergency and maintenance procedures written, reviewed and available?</td><td>Approved procedures in the control room</td></tr>
<tr><td>People</td><td>Are operators trained on the procedures? Is the start-up team staffed for every shift?</td><td>Training records; start-up roster</td></tr>
<tr><td>Emergency response</td><td>Are fire protection, gas detection, safety showers and emergency plans in place and tested?</td><td>Test records; drill record</td></tr>
</table>
<h2>Worked example: the feed section</h2>
<p>The HAZOP of feed heater E-101 produced seven actions. Before feed enters E-101, the review checks each one. The status below is an illustration of what a review might find.</p>
<table>
<tr><th>No.</th><th>HAZOP action</th><th>Status at review</th><th>Before start-up?</th></tr>
<tr><td>1</td><td>Independent outlet temperature trip: TT-103 and TSHH-103 close new steam shutoff valve XV-103 at 95&nbsp;°C</td><td>Installed; tested end to end from TT-103 to XV-103</td><td>Required; closed</td></tr>
<tr><td>2</td><td>High and low temperature alarms on TIC-101; low alarm at 70&nbsp;°C stops reactant addition</td><td>Configured; alarms and the addition stop tested</td><td>Required; closed</td></tr>
<tr><td>3</td><td>Confirm shell design pressure is at least the maximum steam header pressure, or the header has its own relief</td><td>Nameplate and header regulator settings checked</td><td>Required; closed</td></tr>
<tr><td>4</td><td>Decide how a tube leak will be detected before condensate returns to the boiler</td><td>Study under way; interim daily conductivity check of the condensate</td><td>Deferred with interim measure, owner and date</td></tr>
<tr><td>5</td><td>Confirm PSV-102 is sized for blocked-in heating and define its discharge</td><td>Calculation checked; discharge routed to the closed drain; certificate on file</td><td>Required; closed</td></tr>
<tr><td>6</td><td>Check valve on line DN50-P-1004 against reverse flow from R-101</td><td>Installed and inspected</td><td>Required; closed</td></tr>
<tr><td>7</td><td>High flow alarm or trip that keeps the reactant addition to three hours or longer</td><td>High flow alarm installed; trip still in design with the reactor node</td><td>Required; <strong>open</strong></td></tr>
</table>
<p>One required action is open. Action 7 protects against adding reactant faster than the reactor jacket can remove the heat, the scenario in the <a href="what-happens-if-the-cooling-fails-runaway-reactions.html">runaway reaction post</a>. The review cannot say "go" for the reactor until it closes, or until the team agrees and documents an equivalent safeguard. The feed section can still be commissioned on solvent in the meantime. Action 4 can be deferred because a daily check of the condensate covers the risk until the study is done, provided the deferral is recorded with a date and an owner.</p>
<h2>Who should do it</h2>
<p>A PSSR is not a sign-off by the project manager. A small team with independence from the people who built the plant works best: an operations lead who will run the plant, a process engineer, a maintenance or mechanical integrity representative, and someone from health and safety. For a modification, a review sized to the change is enough; the <a href="{MOC}.html">management of change</a> process should say when a PSSR is required and how large.</p>
<h2>Go, go with conditions, or no-go</h2>
<p>The review ends with a decision. <strong>Go</strong>: all required items closed. <strong>Go with conditions</strong>: items that do not affect safe start-up are listed with owners and dates, and the conditions under which the plant may run until they close (for example, a reduced rate). <strong>No-go</strong>: a required item is open. The decision and its conditions are written down and signed by the person accountable for the plant.</p>
<h2>Key points</h2>
<ul>
<li>A PSSR confirms, before hazardous materials go in, that the plant is built as designed, procedures are ready, hazard study actions are dealt with and people are trained.</li>
<li>Every HAZOP action is either closed or formally deferred with a reason, an owner and a date.</li>
<li>Relief devices and safety functions are verified, not assumed.</li>
<li>Use an independent team, and record a clear go, go-with-conditions or no-go decision.</li>
</ul>
<p>Next: {L[3]}, start-up and the performance test.</p>
{NOTE}
{src([OSHA])}"""
    body = nowrap(body, [(1, 0, 22), (2, 0, 3)])
    return dict(slug=C2, title="The Pre-Startup Safety Review: What to Check Before Hazardous Materials Go In",
                desc="What a pre-startup safety review covers, who should do it, how HAZOP actions are closed or deferred, and a worked go/no-go decision for a feed section.",
                cats=["process-engineering"], tags=["PSSR", "pre-startup safety review", "process safety", "HAZOP actions", "commissioning", "start-up"],
                body=body, date=DATE, author="Quak Foo Lee", read="7 min read", series=SER(2), cover_label="Commissioning",
                related=[C1, C3, HAZOP])


def part3():
    body = f"""{CSS}
<p>The pre-startup safety review in {L[2]} has said "go". This part covers what happens next: bringing the plant from its first feed to steady operation at design rate, managing the punch list, and proving with a performance test that the plant does what it was bought to do.</p>
<h2>Start-up: step by step, with holds</h2>
<p>A plant is not taken to full rate in one move. It is brought up in steps, with a hold at each step to confirm that it behaves as expected before going further. Figure&nbsp;1 shows a typical ramp for the example plant.</p>
{fig(fig_ramp(), 1, "An illustrative start-up ramp from first feed to design rate, with holds to check balances and tune control loops.")}
<ol>
<li><strong>Utilities and preparation.</strong> Steam, cooling water, nitrogen and power are on. Equipment is purged with nitrogen so that no air remains where flammable material will go. Solvent is circulated and heated to operating temperature.</li>
<li><strong>First feed at reduced rate.</strong> A lower rate gives time to respond and smaller consequences if something is wrong. Operators and engineers watch temperatures, pressures and levels against expected values.</li>
<li><strong>Holds to check.</strong> At each step, a quick mass balance confirms that what goes in comes out. Control loops tuned on solvent are retuned on process material. Analyses confirm product quality.</li>
<li><strong>Design rate.</strong> Once the plant runs steadily at design rate, the performance test can be scheduled.</li>
</ol>
<p>The start-up procedure, with these steps and their hold criteria, is one of the documents the PSSR confirmed was ready. During start-up, deviations from it are handled through the start-up team's own change process, not improvised.</p>
<h2>The punch list</h2>
<p>Every project ends with a list of things not quite finished. The punch list sorts them by when they must be done:</p>
<table>
<tr><th>Category</th><th>Meaning</th><th>Example</th></tr>
<tr><td>A</td><td>Must be done before start-up of the system</td><td>Missing pipe support on the P-101 discharge</td></tr>
<tr><td>B</td><td>Must be done before handover or the performance test, but not before start-up</td><td>Insulation on a section of steam line</td></tr>
<tr><td>C</td><td>Can be done after handover</td><td>Paint touch-up; permanent labels to replace temporary ones</td></tr>
</table>
<p>The categories need discipline. An item moved from A to B to start on time is a decision with risk attached, and should be agreed by the same people who signed the PSSR. A long tail of category C items after handover is normal; a long tail of B items usually means the performance test will be delayed.</p>
<h2>The performance test</h2>
<p>The performance test proves the plant meets its design basis and the contractor's or licensor's guarantees. Typical guaranteed items are capacity, yield or conversion, product quality, and consumption of utilities such as steam, power and cooling water per tonne of product. The test conditions, duration, measurements and acceptance criteria should be written into the contract long before the test, not negotiated on the day.</p>
<h3>Mass balance closure</h3>
<p>The first check on test data is whether the mass balance closes. Over the test period, total mass out should equal total mass in:</p>
<p>Closure = Σ mass out / Σ mass in</p>
<p>If {f0(IN_T)}&nbsp;t went in and {f0(OUT_T)}&nbsp;t of measured streams came out, closure is {CLOSURE * 100:.1f}%. The missing {f0(IN_T - OUT_T)}&nbsp;t is either an unmeasured stream (a vent, a drain, a sample) or measurement error. A closure within a few percent is typical for a well-instrumented plant; the parties should agree the acceptable band in advance. Data reconciliation, which adjusts measured flows within their uncertainties so that balances close, makes the best use of imperfect data and is described in the <a href="digital-twins-in-chemical-process-plants-architecture-modeling-and-applications.html">digital twins paper</a>.</p>
<h3>Testing a yield guarantee</h3>
<p>The scale-up series set a design yield of 87% from pilot data (<a href="{MEB}.html">from pilot data to a mass and energy balance</a>). Suppose the contract guarantees that yield, and a 72-hour test measures {f0(FEED_KG / 1000)}&nbsp;t of reactant fed and {f0(PROD_KG / 1000)}&nbsp;t of product made, on a basis where full conversion would give one tonne of product per tonne of reactant. The measured yield is {YIELD * 100:.1f}%.</p>
<p>Is that above the guarantee? Every measurement has uncertainty. If the feed meter, the product weighing and the product assay each have a relative standard uncertainty of {U_FEED * 100:.1f}%, {U_PROD * 100:.1f}% and {U_ASSAY * 100:.1f}%, the combined relative uncertainty of the yield is the root of the sum of squares:</p>
<p>u<sub>yield</sub> = √(0.010² + 0.010² + 0.005²) = {U_YIELD * 100:.1f}%</p>
<p>That is about ±{YIELD * U_YIELD * 100:.1f} percentage points at one standard uncertainty, or ±{2 * YIELD * U_YIELD * 100:.1f} at about 95% confidence. The measured {YIELD * 100:.1f}% is {YIELD * 100 - GUAR * 100:.1f} points above the 87% guarantee, which is within the measurement uncertainty. Whether the guarantee is met then depends on what the contract says about uncertainty: whether the measured value is compared directly, or a tolerance is allowed. This is why test procedures specify the meters, their calibration before the test and how uncertainty is treated.</p>
<h2>Handover</h2>
<p>When the performance test is accepted and category A and B items are closed, the plant is handed over to operations. The handover package includes as-built drawings, the process safety information, operating and maintenance procedures, vendor manuals, spare parts, training records, the remaining punch list and the performance test report. Many of these documents started life in the <a href="what-a-feed-package-contains-and-what-each-document-decides.html">FEED package</a>; handover is where they become the plant's operating record.</p>
<h2>Key points</h2>
<ul>
<li>Start up in steps from a reduced rate, with holds to check balances, tune loops and confirm quality.</li>
<li>Sort the punch list by when items must be done, and treat moving an item to a later category as a risk decision.</li>
<li>Write the performance test into the contract early: guarantees, duration, measurements and acceptance criteria.</li>
<li>Check mass balance closure first, and agree how measurement uncertainty is treated before the test.</li>
</ul>
<p>This completes the Commissioning series. For the earlier stages of the same plant, see the <a href="{FEED1}.html">FEED series</a> and the <a href="scale-up-what-changes-from-lab-to-pilot-to-commercial.html">scale-up series</a>.</p>
{NOTE}"""
    body = nowrap(body, [(1, 0, 4)])
    return dict(slug=C3, title="First Run to Steady State: Start-Up, the Punch List and the Performance Test",
                desc="How a process plant goes from first feed to design rate: a stepped start-up, punch list categories, mass balance closure and testing a yield guarantee.",
                cats=["process-engineering"], tags=["start-up", "punch list", "performance test", "mass balance closure", "yield guarantee", "commissioning"],
                body=body, date=DATE, author="Quak Foo Lee", read="7 min read", series=SER(3), cover_label="Commissioning",
                related=[C1, C2, MEB])


def f0(x): return f"{x:,.0f}"


if __name__ == "__main__":
    for a in (part1(), part2(), part3()):
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("wrote", a["slug"], len(a["desc"]))
    print(f"yield={YIELD:.4f} u={U_YIELD:.4f} closure={CLOSURE:.3f}")
