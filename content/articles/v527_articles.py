"""V5.27: two older posts rewritten in the current article format and moved to shorter addresses.

  6-mckinsey-principles-to-unlock-creative-thinking-and-innovation          -> innovation-in-small-businesses
  navigating-the-global-economy-in-2025-why-operational-efficiency-matters-more-than-ever -> operational-efficiency-in-an-uncertain-economy

The old addresses become redirect stubs (refresh_article.py --retire), so links and search results keep working.
Original publish dates kept (2025-11-03 and 2025-04-09). Calculators: assets/js/bets.js and assets/js/stress.js.

Usage: python3 content/articles/v526_articles.py
       python3 content/gen/add_article.py <new slug>                 (for each)
       python3 content/gen/refresh_article.py --retire <old> <new>   (for each)
       python3 content/gen/seo_pass.py .
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import feed_articles as F

NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE = F.NAVY, F.BLUE, F.GREEN, F.GREEND, F.ORANGE, F.PURPLE
MUTED, LINE, PALE, GREENF, ORANGEF = F.MUTED, F.LINE, F.PALE, F.GREENF, F.ORANGEF
svg, fig, txt, box, arrow, DEFS = F.svg, F.fig, F.txt, F.box, F.arrow, F.DEFS
DATE = "2026-11-15"

INNOV, INNOV_OLD, INNOV_ORIG = "innovation-in-small-businesses", "6-mckinsey-principles-to-unlock-creative-thinking-and-innovation", "2025-11-03"
ECON, ECON_OLD, ECON_ORIG = ("operational-efficiency-in-an-uncertain-economy",
                             "navigating-the-global-economy-in-2025-why-operational-efficiency-matters-more-than-ever", "2025-04-09")
P = lambda s, t: f'<a href="{s}.html">{t}</a>'
FIRST = "first-principles-thinking-the-core-of-breakthrough-problem-solving-in-business"
KAIZEN, CORE = "perform-kaizen-event", "what-are-the-core-values-of-process-improvement-part-i"
CHANGE = "change-management-toolkit-the-top-10-models-and-how-to-choose-the-right-one-for-your-organization"
OODA = "ooda-loop-vs-pdca-cycle-which-framework-drives-faster-and-smarter-decisions"
OPEFF, OEE, Q2C, Q2C3 = ("how-to-increase-operational-efficiency-for-small-business", "what-oee-really-measures",
                         "quote-to-cash-process-in-manufacturing", "shorten-quote-to-cash-what-to-fix-first")
LEAN = "how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations"
SS, BUDGET = "setting-safety-stock", "canada-budget-2026-what-manufacturers-and-process-plants-should-know"
AGILE = "adapting-business-operations-for-enhanced-agility-and-market-competitiveness"
RISK = "iso-9001-risk-based-thinking-in-practice"


def m(x): return f"${x:,.0f}"
def k(x):
    sg, a = ("−" if x < 0 else ""), abs(x)
    return sg + (f"${a / 1000:,.0f}k" if a < 1e6 else f"${a / 1e6:,.2f}M")


def src(items): return "<h2>Sources</h2><ul>" + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in items) + "</ul>"
def rel(items): return "<h2>Related reading</h2><ul>" + "".join(f'<li><a href="../post/{s}.html">{t}</a></li>' for s, t in items) + "</ul>"
def nwords(b): return len(re.sub(r"<svg.*?</svg>|<script.*?</script>|<link[^>]*>|<[^>]+>", " ", b, flags=re.S).split())


# ═════════════════════════ Article 1: innovation in a small business ═════════════════════════
FUNNEL = [("Ideas raised", 60), ("Ideas decided within a month", 52), ("Tested cheaply", 12), ("Passed the test", 3), ("Launched", 2)]
TESTS, TCOST, TRATE, TVALUE = 12, 3000, 0.20, 40000
PILOT_PRICE, LIST_PRICE, RATE_H = 4500, 7500, 95
PILOT_HOURS, STD_HOURS, YEAR1 = [42, 38, 34], 30, 10


def fig_loop():
    """Problem -> ideas -> cheap test -> decide, with the loop back."""
    s = DEFS
    steps = [("1 Define the", "customer's problem"), ("2 Generate ideas,", "alone, then together"), ("3 Run a cheap test", "with a pass mark"),
             ("4 Decide: stop,", "change or scale")]
    for i, (a, b) in enumerate(steps):
        x = 20 + i * 190
        s += box(x, 40, 160, 56, [a, b], PALE if i < 3 else GREENF, "#9AB0C8" if i < 3 else GREEND, NAVY, True, 12.5)
        if i < 3: s += arrow(x + 160, 68, x + 187, 68)
    s += f'<path d="M680,96 L680,130 L100,130 L100,98" fill="none" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#ah)"/>'
    s += txt(390, 150, "Change: improve the idea and test again. Stop: record what was learned.", "middle", MUTED, 12.5)
    s += txt(390, 22, "Short cycles of two to four weeks", "middle", BLUE, 13, True)
    return svg("A loop of four steps run in short cycles of two to four weeks: define the customer's problem; generate ideas, alone and then "
               "together; run a cheap test with a pass mark set in advance; decide whether to stop, change or scale. Changed ideas go back "
               "round the loop, and stopped ideas are recorded with what was learned.", 790, 165, s, 600, 10)


def fig_funnel():
    s = DEFS
    mx, x0, w = FUNNEL[0][1], 250, 470
    for i, (name, n) in enumerate(FUNNEL):
        y = 18 + i * 44; bw = max(w * n / mx, 18)
        col = BLUE if i < 3 else (GREEN if i == 4 else GREEND)
        s += txt(x0 - 12, y + 21, name, "end", NAVY, 13)
        s += f'<rect x="{x0}" y="{y}" width="{bw:.1f}" height="30" rx="4" fill="{col}"/>'
        s += txt(x0 + bw + 8, y + 21, str(n), "start", NAVY, 13.5, True)
    return svg("A horizontal funnel for one year at the example firm: 60 ideas raised, 52 decided within a month, 12 tested cheaply, 3 passed "
               "their test and 2 launched.", 760, 240, s, 560)


def innov_body():
    tc, ev = TESTS * TCOST, TESTS * TRATE * TVALUE
    pr = PILOT_PRICE * 3; pc = sum(PILOT_HOURS) * RATE_H
    sc = STD_HOURS * RATE_H; marg = LIST_PRICE - sc
    return f"""{F.CSS}<p>Innovation in a small business is rarely a laboratory breakthrough. It is a new service built on skills the team already has, a product variant customers keep asking for, or a change to a process that removes a daily frustration. What separates firms that keep finding these from firms that don't is not talent. It is a routine: a clear problem, ideas from more than one head, cheap tests, and a decision on every idea.</p>
<p>This article sets out six practices that make that routine work, a two-hour idea session, a test card, a worked example with numbers, and a calculator that shows why many small tests beat one big bet. It was first published in November 2025 under a title that credited the practices to McKinsey &amp; Company. We found no McKinsey source for the list, so the practices are described here in our own words, and the article has moved to a shorter address.</p>

<h2>Six practices that build innovation</h2>
<p class="oee-cap">Table 1. Six practices, what they mean and how to start</p>
<table>
<tr><th>Practice</th><th>What it means</th><th>How to start</th></tr>
<tr><td>1. Start from the customer's problem</td><td>Understand the problem before proposing solutions</td><td>Five customer interviews and one problem statement in a sentence</td></tr>
<tr><td>2. Make curiosity part of leadership</td><td>Leaders ask questions and change course on evidence</td><td>In each review, ask which assumption the plan depends on most</td></tr>
<tr><td>3. Mix perspectives</td><td>Different roles see different options</td><td>Put a front-line person and a customer-facing person in every idea session</td></tr>
<tr><td>4. Run small, cheap experiments</td><td>Learn before investing</td><td>A one-page offer, a mock-up or a two-week trial with a pass mark</td></tr>
<tr><td>5. Make ideas visible</td><td>Sketches and models get better feedback than descriptions</td><td>Whiteboard, storyboard, paper prototype</td></tr>
<tr><td>6. Work in short cycles</td><td>Plan, try, review and adjust every few weeks</td><td>Two- to four-week cycles with a short review at the end</td></tr>
</table>
{fig(fig_loop(), 1, "The innovation loop. Each practice in Table 1 supports one or more of the four steps.")}

<h2>1. Start from the customer's problem</h2>
<p>Most weak ideas are answers to a question nobody asked. Write the problem as one sentence about a real customer: "Contractors cannot get a firm delivery date when they order" leads to better ideas than "improve the customer experience". Design thinking, a widely used method, follows the same order: understand the people you serve, define the problem, generate ideas, build a rough prototype and test it with them.</p>
<p>Five short customer interviews are usually enough to sharpen a problem statement. Ask about the last time the problem happened, what it cost them and what they did about it. Avoid asking whether they would like your idea; people are polite.</p>

<h2>2. Make curiosity part of leadership</h2>
<p>Teams copy what leaders do. A manager who asks why, listens and changes course when the evidence says so gives everyone permission to do the same. A useful habit is to ask, in every plan review, "What would have to be true for this to work, and how could we check that cheaply?" The {P(FIRST, "first principles thinking")} article covers this way of questioning in more depth.</p>

<h2>3. Mix perspectives</h2>
<p>People who do the same job tend to see the same options. Bring sales, operations, finance and someone who talks to customers daily into the same session. In a small firm, inviting a trusted customer or supplier can be the most productive change of all.</p>
<p>How the session runs matters as much as who attends. Research on brainstorming has found for decades that people generate more ideas working alone first than talking in a group, mainly because in a group only one person can speak at a time while the others wait and forget. So have people write ideas silently first, then share and build on them.</p>
<p class="oee-cap">Table 2. A two-hour idea session</p>
<table>
<tr><th>Time</th><th>Step</th><th>How</th></tr>
<tr><td class="nw">10 min</td><td>The problem</td><td>Read the one-sentence problem and what the customer interviews found</td></tr>
<tr><td class="nw">15 min</td><td>Silent ideas</td><td>Everyone writes at least five ideas on separate notes, without discussion</td></tr>
<tr><td class="nw">30 min</td><td>Share and build</td><td>Each person reads theirs out; similar ideas are grouped; others add to them</td></tr>
<tr><td class="nw">15 min</td><td>Vote</td><td>Three dots each, placed silently, so the loudest voice does not decide</td></tr>
<tr><td class="nw">40 min</td><td>Design tests</td><td>One test card (Table 3) for each of the top two or three ideas</td></tr>
<tr><td class="nw">10 min</td><td>Owners and dates</td><td>Each test gets an owner, a budget and a review date</td></tr>
</table>

<h2>4. Run small, cheap experiments</h2>
<p>Most ideas fail, so the aim is to fail cheaply and learn quickly. Before a test starts, write down what you expect, how you will measure it and the result that counts as a pass. Setting the pass mark first stops a disappointing result being explained away afterwards.</p>
<p class="oee-cap">Table 3. A test card</p>
<table>
<tr><th>Field</th><th>Example</th></tr>
<tr><td class="nw">We believe that</td><td>Existing clients will pay for help preparing for a regulatory audit</td></tr>
<tr><td class="nw">To test it we will</td><td>Offer a one-page service to five clients at a pilot price of {m(PILOT_PRICE)}</td></tr>
<tr><td class="nw">We will measure</td><td>How many accept, and the hours each engagement takes</td></tr>
<tr><td class="nw">It passes if</td><td>At least three accept, and the work can be done in under 35 hours once standardised</td></tr>
<tr><td class="nw">Budget and time</td><td>No marketing spend; eight weeks</td></tr>
<tr><td class="nw">Decision by</td><td>The leadership review at the end of week eight</td></tr>
</table>

<h3>Why many small tests beat one big bet</h3>
<p>If one idea in five passes its test, a business that runs {TESTS} cheap tests a year can expect two or three successes. Each success might be worth far more than all the tests together cost. The calculator shows the arithmetic with your own figures.</p>
<div class="oee-calc" role="group" aria-labelledby="bth">
<h3 id="bth">Try it: the value of a portfolio of small tests</h3>
<p class="oee-hint">The starting values are illustrative: {TESTS} tests a year at {m(TCOST)} each, one in five passing, and each success worth {m(TVALUE)} a year in extra profit.</p>
<div class="oee-sliders">
<div class="oee-sl"><label for="bt-n">Tests a year <output id="bt-n-o"></output></label><input type="range" id="bt-n" min="2" max="40" step="1" value="{TESTS}"></div>
<div class="oee-sl"><label for="bt-c">Cost of one test <output id="bt-c-o"></output></label><input type="range" id="bt-c" min="500" max="25000" step="500" value="{TCOST}"></div>
<div class="oee-sl"><label for="bt-p">Share that pass <output id="bt-p-o"></output></label><input type="range" id="bt-p" min="5" max="60" step="5" value="{TRATE * 100:.0f}"></div>
<div class="oee-sl"><label for="bt-v">Value of one success a year <output id="bt-v-o"></output></label><input type="range" id="bt-v" min="5000" max="250000" step="5000" value="{TVALUE}"></div>
</div>
<div class="oee-tiles">
<div class="oee-tile"><span class="k">Expected successes</span><span class="v" id="bt-s"></span><span class="n">a year</span></div>
<div class="oee-tile"><span class="k">Cost of testing</span><span class="v" id="bt-tc"></span><span class="n">a year</span></div>
<div class="oee-tile key"><span class="k">Expected value</span><span class="v" id="bt-ev"></span><span class="n">a year from the successes</span></div>
<div class="oee-tile"><span class="k">Return on testing</span><span class="v" id="bt-r"></span></div>
</div>
</div>
<p>At the starting values, {m(tc)} of testing is expected to produce {TESTS * TRATE:.1f} successes worth about {m(ev)} a year, {ev / tc:.1f} times the cost. The result is sensitive to the pass rate and the value of a success, both of which are uncertain. The point is the shape: keep each test cheap, and the few that succeed pay for all of them.</p>

<h2>5. Make ideas visible</h2>
<p>A rough sketch, a storyboard of the customer's experience or a cardboard model draws better feedback than a written description. People find it easier to criticise a picture constructively, and the picture improves faster. A whiteboard and sticky notes are enough.</p>

<h2>6. Work in short cycles</h2>
<p>Agree a short goal, work on it for two to four weeks, review what was learned and decide the next step. Short cycles keep momentum and limit the cost of a wrong turn. They also fit naturally with the plan-do-check-act cycle many firms already use; see {P(OODA, "OODA vs PDCA")} for how the two compare.</p>

<h2>Worked example: a new service from existing skills</h2>
<p>A 15-person engineering firm hears the same request from several clients: help preparing documents for a regulatory audit. The tempting move is to launch a new service line with a web page, a brochure and an advertising budget. Instead, the team writes the test card in Table 3 and offers the service to five existing clients at a pilot price of {m(PILOT_PRICE)}, against an intended price of {m(LIST_PRICE)}.</p>
<p class="oee-cap">Table 4. The three pilots and what changed</p>
<table>
<tr><th>Pilot</th><th class="num">Hours</th><th>What was learned</th></tr>
<tr><td class="nw">1</td><td class="num">{PILOT_HOURS[0]}</td><td>A third of the time went on chasing the client for documents; a request list is written for the next pilot</td></tr>
<tr><td class="nw">2</td><td class="num">{PILOT_HOURS[1]}</td><td>The request list helps; a standard checklist of 40 items replaces notes made from scratch</td></tr>
<tr><td class="nw">3</td><td class="num">{PILOT_HOURS[2]}</td><td>Checklist and templates in place; the remaining time is the review itself</td></tr>
</table>
<p>Three of the five clients accepted, so the test passed. The pilots earned {m(pr)} against {m(pc)} of staff time at {m(RATE_H)} an hour, roughly breaking even while the method was worked out. With the checklist and templates, the team expects {STD_HOURS} hours per engagement, a cost of {m(sc)} against the {m(LIST_PRICE)} price, or {m(marg)} contribution each. Ten engagements in the first year would add {m(YEAR1 * LIST_PRICE)} of revenue and {m(YEAR1 * marg)} of contribution, and the firm launches with a proven method, a realistic price and two client testimonials. The figures are illustrative.</p>

<h2>Protecting time and keeping an idea log</h2>
<p>Innovation competes with daily work and usually loses. Protect a small, regular slot: an hour a month for the leadership team to review ideas and tests, and a quarterly idea session with a mixed group. Keep every idea in one log and decide on each within a month.</p>
<p class="oee-cap">Table 5. An idea log</p>
<table>
<tr><th>Idea</th><th>Raised by</th><th>Problem it solves</th><th>Cheapest test</th><th>Decision</th><th>Owner and date</th></tr>
<tr><td>Online booking for service visits</td><td>Service coordinator</td><td>Phone tag to schedule visits</td><td>Booking link for one technician for a month</td><td>Test</td><td>Service lead, end of month</td></tr>
<tr><td>Reusable crates for local deliveries</td><td>Driver</td><td>Packaging cost and waste</td><td>Ten crates with two customers</td><td>Test</td><td>Operations, six weeks</td></tr>
<tr><td>New product colour range</td><td>Sales</td><td>Customer requests</td><td>Show samples to five customers</td><td>Park until spring</td><td>Sales manager</td></tr>
<tr><td>Audit preparation service</td><td>Project engineer</td><td>Clients asking for audit help</td><td>Pilot with five clients (Table 3)</td><td>Scale</td><td>Principal, next quarter</td></tr>
</table>

<h2>Measuring whether it is working</h2>
{fig(fig_funnel(), 2, "The idea funnel at the example firm over one year. Most ideas never reach a test; that is normal.")}
<p class="oee-cap">Table 6. Measures for an innovation routine</p>
<table>
<tr><th>Measure</th><th>Why it helps</th><th class="num">Example</th></tr>
<tr><td>Ideas raised per quarter, and by whom</td><td>Shows whether people across the business feel able to contribute</td><td class="num">15</td></tr>
<tr><td>Share of ideas decided within a month</td><td>Shows whether ideas are taken seriously</td><td class="num">87%</td></tr>
<tr><td>Tests run per quarter</td><td>Measures learning, not talk</td><td class="num">3</td></tr>
<tr><td>Average cost per test</td><td>Keeps tests cheap</td><td class="num">{m(TCOST)}</td></tr>
<tr><td>Revenue or savings from ideas launched in the last two years</td><td>Links the routine to results over a realistic period</td><td class="num">Track yearly</td></tr>
</table>
<p>Do not judge the routine on a single big win. Most of the value comes from many small, tested improvements, and tests that fail cheaply are a sign the process is working.</p>

<h2>Common traps</h2>
<ul>
<li><strong>Ideas without a problem.</strong> A session with no clear question produces a list that goes nowhere.</li>
<li><strong>The loudest voice wins.</strong> Write ideas silently first and vote silently.</li>
<li><strong>Testing too late.</strong> Months spent polishing an idea before any customer sees it.</li>
<li><strong>No pass mark.</strong> Without one, every result looks "promising" and nothing is ever stopped.</li>
<li><strong>No follow-through.</strong> People stop suggesting ideas once they see nothing happens to them. Tell each person what was decided about theirs.</li>
</ul>
<p>Changing how people work also needs care; the {P(CHANGE, "change management toolkit")} covers the main models.</p>

<div class="oee-takeaway"><p><strong>Takeaway.</strong> Start from one customer problem, collect ideas silently before discussing them, and test the best with a pass mark set in advance. Keep tests cheap and decide on every idea within a month. In the example, three pilots costing almost nothing turned a client request into a priced, proven service.</p></div>
<p class="oee-note"><em>The engineering firm, its pilots and the calculator's starting values are illustrative examples with round-number inputs. They do not describe any real company.</em></p>
<script src="../assets/js/bets.js" defer></script>"""


def innov():
    s = [("Diehl, M. and Stroebe, W. (1987). Productivity loss in brainstorming groups: toward the solution of a riddle. Journal of Personality and Social Psychology, 53(3), 497–509",
          "https://scilit.com/publications/ca2c6d170553eab396c33a8aa7c48d54")]
    r = [(FIRST, "First principles thinking for business"), (KAIZEN, "How to run a Kaizen event"),
         (CORE, "The core values of process improvement"), (CHANGE, "Change management toolkit")]
    b = innov_body() + src(s) + rel(r)
    return dict(slug=INNOV, title="Innovation in a Small Business: Six Practices, Cheap Tests and an Idea Log",
                desc="Six practices that build innovation in a small business, a two-hour idea session, a test card, a worked example and a calculator for small tests.",
                cats=["process-improvement", "strategy"],
                tags=["innovation", "creative thinking", "design thinking", "experiments", "idea management", "small business"],
                body=F.nowrap(b.strip(), [(1, 0, 34)]), date=DATE, author="Quak Foo Lee",
                read=f"{max(4, round(nwords(b) / 220))} min read", cover_label="Innovation", related=[x for x, _ in r]), nwords(b)


# ═════════════════════════ Article 2: operational efficiency in an uncertain economy ═════════════════════════
R0, V0, F0 = 6_000_000, 0.55, 2_200_000          # revenue, variable cost share, fixed costs (incl. interest)
MAT, STEEL, ENERGY = 0.35, 0.60, 0.05            # materials share of revenue, steel share of materials, energy and freight share
D_STEEL, D_ENERGY, VOL, D_INT = 0.15, 0.20, 0.90, 15_000
DV = MAT * STEEL * D_STEEL + ENERGY * D_ENERGY   # 0.0415 of revenue
SURCH, WASTE, FIXCUT = 2 / 3 * MAT * STEEL * D_STEEL, 0.015, 80_000


def profit(R, v, F): return R * (1 - v) - F


BASE = profit(R0, V0, F0)                                      # 500k
S_VOL = profit(R0 * VOL, V0, F0)                               # 230k
S_COST = profit(R0 * VOL, V0 + DV, F0)                         # ~5.9k
S_ALL = profit(R0 * VOL, V0 + DV, F0 + D_INT)                  # ~ -9.1k
A_SUR = profit(R0 * VOL, V0 + DV - SURCH, F0 + D_INT)
A_WST = profit(R0 * VOL, V0 + DV - SURCH - WASTE, F0 + D_INT)
AFTER = profit(R0 * VOL, V0 + DV - SURCH - WASTE, F0 + D_INT - FIXCUT)
BE = lambda v, F: F / (1 - v)


def fig_breakeven():
    """Profit against sales for the base cost structure, after the shock, and after the moves."""
    s = DEFS
    x0, x1, y0, y1 = 90, 690, 30, 290          # plot box
    rmin, rmax, pmin, pmax = 4.0e6, 6.6e6, -600_000, 800_000
    X = lambda r: x0 + (r - rmin) / (rmax - rmin) * (x1 - x0)
    Y = lambda p: y1 - (p - pmin) / (pmax - pmin) * (y1 - y0)
    for p in range(-600_000, 800_001, 200_000):
        s += f'<line x1="{x0}" y1="{Y(p):.1f}" x2="{x1}" y2="{Y(p):.1f}" stroke="{LINE}" stroke-width="{1.4 if p == 0 else .6}"/>'
        s += txt(x0 - 8, Y(p) + 4, k(p) if p else "$0", "end", MUTED, 11.5)
    for r in [4.0e6, 4.5e6, 5.0e6, 5.5e6, 6.0e6, 6.5e6]:
        s += txt(X(r), y1 + 18, f"${r / 1e6:.1f}M", "middle", MUTED, 11.5)
    s += txt((x0 + x1) / 2, y1 + 38, "Sales a year", "middle", MUTED, 12)
    lines = [("Before the shock", V0, F0, BLUE, ""), ("After the shock", V0 + DV, F0 + D_INT, ORANGE, ' stroke-dasharray="6 4"'),
             ("After the moves", V0 + DV - SURCH - WASTE, F0 + D_INT - FIXCUT, GREEND, "")]
    for i, (name, v, F, col, dash) in enumerate(lines):
        s += f'<line x1="{X(rmin):.1f}" y1="{Y(profit(rmin, v, F)):.1f}" x2="{X(rmax):.1f}" y2="{Y(profit(rmax, v, F)):.1f}" stroke="{col}" stroke-width="2.4"{dash}/>'
        be = BE(v, F); s += f'<circle cx="{X(be):.1f}" cy="{Y(0):.1f}" r="4.5" fill="{col}"/>'
        s += f'<line x1="{x0 + 14}" y1="{y0 + 14 + i * 20}" x2="{x0 + 40}" y2="{y0 + 14 + i * 20}" stroke="{col}" stroke-width="2.4"{dash}/>'
        s += txt(x0 + 48, y0 + 18 + i * 20, f"{name} (break-even {k(be)})", "start", NAVY, 12)
    for r, lab in [(R0, "Today"), (R0 * VOL, "Sales down 10%")]:
        s += f'<line x1="{X(r):.1f}" y1="{y0}" x2="{X(r):.1f}" y2="{y1}" stroke="{MUTED}" stroke-dasharray="2 3"/>'
        s += txt(X(r), y1 - 6, lab, "middle", MUTED, 11.5)
    return svg(f"A break-even chart for the example fabricator: profit against sales for three cost structures. Before the shock, break-even "
               f"is {k(BE(V0, F0))} of sales and profit at today's {k(R0)} is {k(BASE)}. After the shock in input costs and interest, "
               f"break-even rises to {k(BE(V0 + DV, F0 + D_INT))}, above the {k(R0 * VOL)} of sales left after a 10% drop, so the business "
               f"makes a small loss. After the three moves, break-even falls to {k(BE(V0 + DV - SURCH - WASTE, F0 + D_INT - FIXCUT))}.",
               720, 345, s, 580)


def fig_bridge():
    """Profit bridge from today to the stressed case and back up after the moves."""
    s = DEFS
    steps = [("Profit today", BASE, None), ("Sales down 10%", S_VOL - BASE, BASE), ("Input costs up", S_COST - S_VOL, S_VOL),
             ("Interest up", S_ALL - S_COST, S_COST), ("Stressed profit", S_ALL, None), ("Surcharge", A_SUR - S_ALL, S_ALL),
             ("Less waste", A_WST - A_SUR, A_SUR), ("Fixed cost review", AFTER - A_WST, A_WST), ("Profit after moves", AFTER, None)]
    x0, w, gap, z, sc = 70, 62, 16, 250, 0.00038       # z: y of zero line; px per $
    s += f'<line x1="{x0 - 10}" y1="{z}" x2="{x0 + 9 * (w + gap)}" y2="{z}" stroke="{LINE}" stroke-width="1.4"/>'
    s += txt(x0 - 14, z + 4, "$0", "end", MUTED, 11.5)
    labels = [["Profit", "today"], ["Sales", "down 10%"], ["Input", "costs up"], ["Interest", "up"], ["Stressed", "profit"],
              ["Steel", "surcharge"], ["Less", "waste"], ["Fixed cost", "review"], ["After", "the moves"]]
    for i, (name, v, start) in enumerate(steps):
        x = x0 + i * (w + gap)
        if start is None: a, b, col = 0, v, (NAVY if i == 0 else (ORANGE if v < 0 else GREEND))
        else: a, b, col = start, start + v, (ORANGE if v < 0 else GREEN)
        top, bot = z - max(a, b) * sc, z - min(a, b) * sc
        s += f'<rect x="{x}" y="{top:.1f}" width="{w}" height="{max(bot - top, 1.5):.1f}" rx="3" fill="{col}"/>'
        val = (("+" if v > 0 and start is not None else "") + k(v)) if start is not None else k(v)
        s += txt(x + w / 2, (top - 6) if v >= 0 or start is None and v >= 0 else bot + 15, val, "middle", NAVY, 11.5, True)
        for j, ln in enumerate(labels[i]): s += txt(x + w / 2, 300 + j * 15, ln, "middle", NAVY, 11.5)
    return svg(f"A profit bridge for the example fabricator. Profit today is {k(BASE)}. A 10% drop in sales removes {k(BASE - S_VOL)}, higher "
               f"steel, energy and freight costs remove {k(S_VOL - S_COST)}, and higher interest removes {k(S_COST - S_ALL)}, leaving a loss of "
               f"about {k(-S_ALL)}. A steel surcharge adds {k(A_SUR - S_ALL)}, less waste adds {k(A_WST - A_SUR)} and a fixed cost review adds "
               f"{k(AFTER - A_WST)}, for a profit of {k(AFTER)} after the moves.", 790, 335, s, 600, 10)


def econ_body():
    v_after = V0 + DV - SURCH - WASTE; f_after = F0 + D_INT - FIXCUT
    mos = lambda R, v, F: (R - BE(v, F)) / R
    rows = [("Today", R0, V0, F0), ("Sales down 10%", R0 * VOL, V0, F0), ("Sales down 10%, costs up", R0 * VOL, V0 + DV, F0 + D_INT),
            ("After the three moves", R0 * VOL, v_after, f_after)]
    trows = "".join(f'<tr><td class="nw">{n}</td><td class="num">{k(R)}</td><td class="num">{v:.1%}</td><td class="num">{k(F)}</td>'
                    f'<td class="num">{k(profit(R, v, F))}</td><td class="num">{k(BE(v, F))}</td><td class="num">{mos(R, v, F):.0%}</td></tr>' for n, R, v, F in rows)
    dvc = DV / V0
    return f"""{F.CSS}<p>Costs, interest rates and trade rules are all moving at once, and none of them is under a small firm's control. What is under its control is how much a shock hurts: how close the business runs to break-even, how quickly cash comes back, how much it wastes, and how exposed it is to a single supplier, customer or border.</p>
<p>This article looks at the pressures on Canadian businesses as of November 2026, shows how to stress test your own profit and loss, and works through an example of a small manufacturer hit by falling sales and rising costs at the same time. A calculator lets you run the test with your own figures. It replaces a post first published in April 2025, which described the outlook at that time, and has moved to a shorter address.</p>

<h2>The pressures in late 2026</h2>
<p class="oee-cap">Table 1. Pressures on Canadian businesses, as of November 2026</p>
<table>
<tr><th>Pressure</th><th>What is happening</th><th>What it does to a small business</th></tr>
<tr><td class="nw">Prices</td><td>Consumer prices rose 3.1% in the year to September 2026, up from 3.0% in August; excluding gasoline the rise was 2.2%.</td><td>Energy, fuel and freight costs climb faster than the prices you can charge</td></tr>
<tr><td class="nw">Interest rates</td><td>The Bank of Canada raised its policy rate by a quarter point to 2.5% on October 28, 2026, its first increase since July 2023. The next decision is due on December 9.</td><td>Higher cost on credit lines and equipment loans; more pressure to free cash</td></tr>
<tr><td class="nw">Trade</td><td>The US applies tariffs of 50% on steel, aluminum and copper, and 10% on most other goods, with goods that comply with the trade agreement exempt from the 10%. At the July 2026 joint review the US declined to renew CUSMA in its current form; the agreement remains in force with annual reviews. Canada has applied counter-tariffs on C$27.6 billion of US goods since September 8, 2026.</td><td>Higher costs for metal inputs; uncertain prices and rules for exporters; paperwork to prove origin</td></tr>
<tr><td class="nw">What owners report</td><td>In Statistics Canada's spring 2026 survey, businesses with 1 to 19 employees most often expected inflation (48.7%), input costs (27.1%) and transportation costs (26.0%) to be obstacles; 21.4% expected recruiting skilled staff to be one.</td><td>Cost control and productivity, not only growth, decide this year's margin</td></tr>
</table>
<p>These figures will change. The point of the rest of the article is a method that works whatever the next headline says.</p>

<h2>Efficiency and resilience are not the same thing</h2>
<p>Efficiency is doing the work with less waste. Resilience is surviving a shock. The two usually support each other: less scrap, faster invoicing and fewer errors improve margins in good times and lower break-even in bad times. They pull apart in a few places, and those need a deliberate choice.</p>
<p class="oee-cap">Table 2. Where efficiency and resilience agree and where they pull apart</p>
<table>
<tr><th>Area</th><th>Pure efficiency says</th><th>Resilience says</th><th>A sensible middle</th></tr>
<tr><td class="nw">Inventory</td><td>Hold as little as possible</td><td>Hold buffers against disruption</td><td>Buffers on the few critical, long-lead or single-source items only. See {P(SS, "setting safety stock")}.</td></tr>
<tr><td class="nw">Suppliers</td><td>One supplier, best price</td><td>Several suppliers, more cost</td><td>A qualified second source for anything that would stop the line</td></tr>
<tr><td class="nw">Staff</td><td>No slack</td><td>Spare capacity</td><td>Cross-training, so people can cover each other's critical tasks</td></tr>
<tr><td class="nw">Scrap, rework, invoicing delays</td><td>Remove them</td><td>Remove them</td><td>No conflict: remove them first</td></tr>
</table>

<h2>Stress test your profit and loss</h2>
<p>A stress test asks one question: what happens to profit if sales fall and costs rise at the same time? It needs only three numbers from your accounts.</p>
<ul>
<li><strong>Sales</strong> for the last twelve months.</li>
<li><strong>Variable costs</strong>, the costs that rise and fall with sales: materials, direct labour paid by the hour, energy, freight, commissions. Express them as a share of sales.</li>
<li><strong>Fixed costs</strong>, the costs that stay the same: rent, salaries, insurance, software, interest.</li>
</ul>
<p>Profit is sales × (1 − variable share) − fixed costs. Break-even sales is fixed costs ÷ (1 − variable share). The margin of safety is how far sales can fall before you reach break-even, as a share of today's sales.</p>

<h2>Worked example: a metal fabricator</h2>
<p>A 25-person metal fabricator in British Columbia has sales of {k(R0)} a year. Variable costs are {V0:.0%} of sales: materials {MAT:.0%} (of which {STEEL:.0%} is steel), direct labour 15% and energy and freight {ENERGY:.0%}. Fixed costs, including interest on a $1.5 million credit line, are {k(F0)}. Profit is {k(BASE)}, and break-even is {k(BE(V0, F0))}: sales can fall {mos(R0, V0, F0):.0%} before the business loses money.</p>
<p>The owner tests a plausible bad year: sales down 10%, steel up {D_STEEL:.0%}, energy and freight up {D_ENERGY:.0%}, and one percentage point more on the credit line ({m(D_INT)} a year). Steel and energy together add {DV:.2%} of sales to variable cost, a {dvc:.1%} increase.</p>
<p class="oee-cap">Table 3. The stress test</p>
<table>
<tr><th>Case</th><th class="num">Sales</th><th class="num">Variable share</th><th class="num">Fixed costs</th><th class="num">Profit</th><th class="num">Break-even</th><th class="num">Margin of safety</th></tr>
{trows}
</table>
{fig(fig_bridge(), 1, "From today's profit to the stressed case, and back after three moves. Orange is a loss of profit, green a gain.")}
<p>A 10% fall in sales alone more than halves profit, because the fixed costs do not fall with it. Add the cost increases and the business slips just below break-even. Nothing in the stressed case is dramatic on its own; it is the combination that hurts.</p>
<p>The owner then tests three moves, chosen because none needs new equipment or lay-offs:</p>
<ol>
<li><strong>A steel surcharge.</strong> New quotes carry a price adjustment clause tied to a published steel price index, and existing customers are told the surcharge applies from the next order. The owner assumes two-thirds of the steel increase is recovered, about {SURCH:.1%} of sales.</li>
<li><strong>Less waste.</strong> Scrap, rework and overtime from rushed jobs come to about 4% of sales. Nesting software, a first-off check and a frozen weekly schedule cut that by {WASTE:.1%} of sales. {P(LEAN, "Lean methodology")} and {P(OEE, "OEE")} help find these losses.</li>
<li><strong>A fixed cost review.</strong> Unused software subscriptions, an under-used leased forklift and an insurance renewal tendered to three brokers save {m(FIXCUT)} a year.</li>
</ol>
<p>Together they bring profit back to {k(AFTER)} in the stressed year and lower break-even to {k(BE(v_after, f_after))}. Figure 2 shows how each line moves.</p>
{fig(fig_breakeven(), 2, "Break-even chart for the example. A dot marks each break-even point. The moves make the business profitable again even at the lower sales.")}

<div class="oee-calc" role="group" aria-labelledby="sth">
<h3 id="sth">Try it: stress test your own business</h3>
<p class="oee-hint">The starting values are the example: {k(R0)} of sales, {V0:.0%} variable costs, {k(F0)} fixed costs, sales down 10% and variable costs up {dvc:.1%}. Interest is left out here, so the stressed profit is a little higher than in Table 3.</p>
<div class="oee-sliders">
<div class="oee-sl"><label for="st-r">Sales a year <output id="st-r-o"></output></label><input type="range" id="st-r" min="500000" max="50000000" step="100000" value="{R0}"></div>
<div class="oee-sl"><label for="st-v">Variable costs, share of sales <output id="st-v-o"></output></label><input type="range" id="st-v" min="20" max="85" step="1" value="{V0 * 100:.0f}"></div>
<div class="oee-sl"><label for="st-f">Fixed costs a year <output id="st-f-o"></output></label><input type="range" id="st-f" min="50000" max="20000000" step="50000" value="{F0}"></div>
<div class="oee-sl"><label for="st-dv">Change in sales volume <output id="st-dv-o"></output></label><input type="range" id="st-dv" min="-30" max="10" step="1" value="-10"></div>
<div class="oee-sl"><label for="st-dc">Change in variable costs <output id="st-dc-o"></output></label><input type="range" id="st-dc" min="-10" max="30" step="0.5" value="{dvc * 100:.1f}"></div>
</div>
<div class="oee-tiles">
<div class="oee-tile"><span class="k">Profit today</span><span class="v" id="st-p0"></span></div>
<div class="oee-tile key"><span class="k">Profit under stress</span><span class="v" id="st-p1"></span></div>
<div class="oee-tile"><span class="k">Break-even sales under stress</span><span class="v" id="st-be"></span></div>
<div class="oee-tile"><span class="k">Margin of safety today</span><span class="v" id="st-ms"></span><span class="n">fall in sales before a loss</span></div>
</div>
</div>

<h2>Five moves that lower break-even</h2>
<p class="oee-cap">Table 4. Moves, what they change and where to read more</p>
<table>
<tr><th>Move</th><th>What it changes</th><th>Effort</th><th>Read more</th></tr>
<tr><td>Pass cost changes through</td><td>Price adjustment clauses, surcharges, shorter quote validity</td><td>Low</td><td>Review terms on every new quote</td></tr>
<tr><td>Remove waste</td><td>Variable cost: scrap, rework, overtime, energy per unit</td><td>Medium</td><td>{P(OPEFF, "Operational efficiency guide")}, {P(OEE, "OEE")}</td></tr>
<tr><td>Free cash</td><td>Invoice on delivery, chase overdue accounts, take deposits</td><td>Low to medium</td><td>{P(Q2C3, "Shorten quote to cash")}</td></tr>
<tr><td>Reduce exposure</td><td>Second sources, CUSMA origin records, customers in more than one market</td><td>Medium</td><td>{P(RISK, "Risk-based thinking")}</td></tr>
<tr><td>Invest in productivity</td><td>Automation and software that cut hours per unit, using tax incentives and funding</td><td>Higher</td><td>{P(BUDGET, "Budget 2026 measures")}, <a href="../funding.html">funding finder</a></td></tr>
</table>
<p>Cash deserves its own mention. A business can be profitable on paper and still run out of cash when customers pay late and credit costs more. Every day cut from the time between paying suppliers and being paid releases cash that no longer has to be borrowed; {P(Q2C, "the quote-to-cash process")} shows where those days usually sit.</p>

<h2>A 90-day plan</h2>
<p class="oee-cap">Table 5. What to do in the next 90 days</p>
<table>
<tr><th>Days</th><th>Work</th><th>Result to check</th></tr>
<tr><td class="nw">1 to 30</td><td>Run the stress test. List the ten largest cost lines and the five largest customers and suppliers. Add a price adjustment clause to new quotes.</td><td>Break-even and margin of safety known; exposure list written</td></tr>
<tr><td class="nw">31 to 60</td><td>Measure scrap, rework and overtime for a month. Review every subscription, lease and insurance policy. Invoice on delivery day.</td><td>Waste as a share of sales; fixed cost savings agreed; invoice lag</td></tr>
<tr><td class="nw">61 to 90</td><td>Qualify a second source for the riskiest input. Fix the two largest waste causes. Check which productivity investments qualify for incentives.</td><td>New break-even; cash runway in weeks</td></tr>
</table>

<h2>Measures to review every month</h2>
<p class="oee-cap">Table 6. A one-page monthly review</p>
<table>
<tr><th>Measure</th><th>How to calculate it</th><th class="num">Example today</th></tr>
<tr><td class="nw">Break-even sales</td><td>Fixed costs ÷ (1 − variable share)</td><td class="num">{k(BE(V0, F0))}</td></tr>
<tr><td class="nw">Margin of safety</td><td>(Sales − break-even) ÷ sales</td><td class="num">{mos(R0, V0, F0):.0%}</td></tr>
<tr><td class="nw">Cash runway</td><td>Cash and unused credit ÷ average weekly cash outflow</td><td class="num">Track weekly</td></tr>
<tr><td class="nw">Days sales outstanding</td><td>Unpaid invoices ÷ sales per day</td><td class="num">Track monthly</td></tr>
<tr><td class="nw">Waste</td><td>Scrap, rework and avoidable overtime ÷ sales</td><td class="num">4%</td></tr>
<tr><td class="nw">Largest customer share</td><td>Sales to the largest customer ÷ total sales</td><td class="num">Track quarterly</td></tr>
</table>

<h2>Common mistakes</h2>
<ul>
<li><strong>Cutting across the board.</strong> A 10% cut to every budget removes capability along with waste. Cut what the stress test and the waste measures point to.</li>
<li><strong>Cutting maintenance and training first.</strong> Both are easy to defer and expensive later, when breakdowns and errors rise.</li>
<li><strong>Hoarding stock everywhere.</strong> Buffers on every item tie up cash that may be needed more. Protect the critical few.</li>
<li><strong>Waiting for certainty.</strong> Rates, tariffs and prices will keep moving. A business that knows its break-even can act on each change as it comes.</li>
</ul>
<p>For how to keep plans flexible as conditions change, see {P(AGILE, "operational agility")}.</p>

<div class="oee-takeaway"><p><strong>Takeaway.</strong> Know your break-even and margin of safety, then test them against a bad year. In the example, a 10% fall in sales with higher steel, energy and interest costs turned a {k(BASE)} profit into a small loss; a surcharge, less waste and a fixed cost review restored about {k(AFTER)} without new equipment or lay-offs.</p></div>
<p class="oee-note"><em>The fabricator and its figures are an illustrative example with round-number inputs. It does not describe any real company. The economic figures in Table 1 are as published in October and November 2026 and will change.</em></p>
<script src="../assets/js/stress.js" defer></script>"""


def econ():
    s = [("Statistics Canada: The Weekly Review, October 19 to 23, 2026 (Consumer Price Index, September 2026)", "https://www.statcan.gc.ca/o1/en/plus/9368-weekly-review-october-19-23-2026"),
         ("Bank of Canada: Bank of Canada raises the policy rate by 25 basis points to 2½% (October 28, 2026)", "https://www.bankofcanada.ca/2026/10/fad-press-release-2026-10-28"),
         ("Congressional Research Service: U.S.-Canada Trade Relations (IF12595)", "https://www.everycrsreport.com/reports/IF12595.html"),
         ("McMillan LLP: Following July 1st review, CUSMA remains in effect until 2036", "https://mcmillan.ca/insights/following-july-1st-review-cusma-remains-in-effect-until-2036-on-going-negotiations-as-part-of-annual-reviews-to-agree-on-north-american-free-trade-will-continue/"),
         ("Statistics Canada: Analysis on small businesses in Canada, second quarter of 2026", "https://www150.statcan.gc.ca/n1/pub/11-621-m/11-621-m2026008-eng.htm")]
    r = [(OPEFF, "Operational efficiency for small businesses: a practical guide"), (Q2C3, "Shorten quote to cash: what to fix first"),
         (BUDGET, "Budget 2026: what manufacturers and process plants should know"), (SS, "Setting safety stock without guessing")]
    b = econ_body() + src(s) + rel(r)
    return dict(slug=ECON, title="Operational Efficiency in an Uncertain Economy: Stress Test Your Business and Lower Break-Even",
                desc="Pressures on Canadian businesses in late 2026, how to stress test profit and break-even, a worked fabricator example, five moves and a calculator.",
                cats=["operational-efficiency", "strategy"],
                tags=["operational efficiency", "break-even", "stress test", "tariffs", "interest rates", "cost control", "resilience"],
                body=F.nowrap(b.strip(), [(4, 0, 30), (5, 0, 30)]), date=DATE, author="Quak Foo Lee",
                read=f"{max(4, round(nwords(b) / 220))} min read", cover_label="Uncertain Economy", related=[x for x, _ in r]), nwords(b)


if __name__ == "__main__":
    op = os.path.join(HERE, "original_dates.json")
    od = json.load(open(op, encoding="utf-8")); od[INNOV] = INNOV_ORIG; od[ECON] = ECON_ORIG
    note = od.pop("_note"); json.dump({"_note": note, **dict(sorted(od.items()))}, open(op, "w", encoding="utf-8"), indent=1)
    for fn in (innov, econ):
        a, n = fn()
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"], n, "words", a["read"], "| desc", len(a["desc"]))
    print("profits", round(BASE), round(S_VOL), round(S_COST), round(S_ALL), round(A_SUR), round(A_WST), round(AFTER))
