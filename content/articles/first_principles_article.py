"""V5.25: "First Principles Thinking" rewritten in the current article format (Oct 2025 post, same address, original date kept).

What changed from the V4.82 in-place version: the untraceable client case is replaced by two worked examples with stated,
illustrative numbers (ingredient yield at a food plant; should-cost of a machined part), three figures, numbered tables,
typeset equations, a yield-gap payback calculator (assets/js/fp.js), a section on when not to use the method, and sources.
Now filed under Process Improvement and Strategy (was Process Improvement, Change Management, Operational Efficiency).

Usage: python3 content/articles/first_principles_article.py
       python3 content/gen/refresh_article.py first-principles-thinking-the-core-of-breakthrough-problem-solving-in-business
       python3 content/gen/seo_pass.py .
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import feed_articles as F

NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE = F.NAVY, F.BLUE, F.GREEN, F.GREEND, F.ORANGE, F.PURPLE
MUTED, LINE, PALE, GREENF, ORANGEF = F.MUTED, F.LINE, F.PALE, F.GREENF, F.ORANGEF
svg, fig, txt, box, arrow, DEFS = F.svg, F.fig, F.txt, F.box, F.arrow, F.DEFS

SLUG = "first-principles-thinking-the-core-of-breakthrough-problem-solving-in-business"
ORIGINAL = "2025-10-19"
DATE = "2026-11-14"
JS = '<script src="../assets/js/fp.js" defer></script>'
NOTE = ('<p class="oee-note"><em>The snack bar plant, the machined bracket and their figures are illustrative examples with round-number '
        'inputs. They do not describe any real company or supplier. Use your own data before acting on a result.</em></p>')
P = lambda s, t: f'<a href="{s}.html">{t}</a>'
OEE, OEEC, Q2C, SS = "what-oee-really-measures", "what-oee-losses-cost", "quote-to-cash-process-in-manufacturing", "setting-safety-stock"
LEAN, GAP, CLEAR = ("how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations",
                    "bridging-the-gap-a-step-by-step-guide-to-conducting-a-gap-analysis-for-operational-efficiency",
                    "clear-thinking-by-shane-parrish-book-review-lessons-and-how-to-apply-them")
OODA = "ooda-loop-vs-pdca-cycle-which-framework-drives-faster-and-smarter-decisions"
MCK = "innovation-in-small-businesses"
EXAM = "../exams/decision-thinking/Critical_Thinking_Business_Guided_Path_100.html"


def eq(tex): return f'<p class="eq">\\[{tex}\\]</p>'
def im(tex): return f'\\({tex}\\)'


def mathjs():
    return ('\n<link rel="stylesheet" href="../assets/js/vendor/katex/katex.min.css">'
            '\n<script src="../assets/js/vendor/katex/katex.min.js" defer></script>'
            '\n<script src="../assets/js/vendor/katex/auto-render.min.js" defer></script>'
            '\n<script src="../assets/js/math.js" defer></script>')


def m(x): return f"${x:,.0f}"
def m2(x): return f"${x:,.2f}"


# ───────────────────────── Example 1: ingredient yield at a snack bar plant ─────────────────────────
SPEND = 2_400_000                     # ingredients bought a year
LOSSES = [  # (loss, now %, after %, fix)
    ("Changeover purges and start-up", 3.5, 2.1, "Schedule by recipe family: 6 changeovers a week instead of 10"),
    ("Overfill (giveaway)", 2.5, 1.0, "Checkweigher feeds back to the depositor; fill target set from the measured weight variation and the net quantity rules, not a guess"),
    ("Rejected bars", 2.0, 1.5, "Wrapper settings recorded per product; first-off check after every changeover"),
    ("Spills, expiry and other", 1.0, 1.0, "No change in the first round"),
]
LOSS_NOW = sum(l[1] for l in LOSSES)            # 9.0 %
LOSS_NEW = sum(l[2] for l in LOSSES)            # 5.6 %
Y, YT = 1 - LOSS_NOW / 100, 1 - LOSS_NEW / 100  # 0.91, 0.944
GAP_NOW = SPEND * (1 - Y)                       # 216,000
SAVE = SPEND * (1 - Y / YT)                     # 86,441
COST = 60_000
PAYBACK = COST / SAVE * 12                      # 8.3 months

# ───────────────────────── Example 2: should-cost of a machined bracket ─────────────────────────
QUOTE, QTY = 38.00, 2000
RATE, LAB = 110.0, 60.0          # CNC rate $/h incl. operator; bench rate $/h
BLANK, PRICE = 0.95, 9.50        # kg of bar per part; $/kg
def shouldcost(cycle_min, setup_h, batch):
    rows = [("Material", f"{BLANK} kg of 6061 aluminium bar at {m2(PRICE)}/kg", BLANK * PRICE),
            ("Machining", f"{cycle_min} min on a CNC mill at {m(RATE)}/h", cycle_min / 60 * RATE),
            ("Set-up", f"{setup_h} h at {m(RATE)}/h, spread over a batch of {batch}", setup_h * RATE / batch),
            ("Deburr and inspect", f"3 min at {m(LAB)}/h", 3 / 60 * LAB),
            ("Anodizing", "Outside service, per part", 2.20)]
    sub = sum(r[2] for r in rows)
    return rows, sub, sub * 1.15
SC_A = shouldcost(7, 2, 100)     # as drawn and ordered: tight tolerances everywhere, 100 a month
SC_B = shouldcost(5, 2, 500)     # tolerances opened on non-critical faces, 500 a quarter
TARGET = 30.00
SAVE2 = (QUOTE - TARGET) * QTY


def fig_paths():
    """Reasoning by analogy (top lane) against reasoning from first principles (bottom lane)."""
    s = DEFS
    s += txt(20, 34, "By analogy", "start", MUTED, 13, True)
    top = [("How do others", "do it?"), ("Copy it and", "adjust a little"), ("A result close", "to theirs")]
    for i, (a, b) in enumerate(top):
        x = 150 + i * 244
        s += box(x, 14, 190, 50, [a, b], "#EEF0F3", "#B8C2CC", NAVY, False)
        if i < 2: s += arrow(x + 190, 39, x + 241, 39, MUTED)
    s += txt(20, 128, "From first", "start", BLUE, 13, True) + txt(20, 146, "principles", "start", BLUE, 13, True)
    bot = [("1 State the", "problem in numbers"), ("2 Break it into", "its parts"), ("3 Sort facts from", "assumptions"),
           ("4 Test the", "assumptions"), ("5 Rebuild and", "try it small")]
    for i, (a, b) in enumerate(bot):
        x = 150 + i * 140
        s += box(x, 112, 118, 50, [a, b], PALE if i < 4 else GREENF, "#9AB0C8" if i < 4 else GREEND, NAVY, True, 11.5)
        if i < 4: s += arrow(x + 118, 137, x + 137, 137, NAVY)
    s += txt(489, 194, "Slower and harder, but it can find an option nobody has tried", "middle", MUTED, 12.5)
    s += txt(489, 94, "Fast and usually good enough, but it inherits everyone's assumptions", "middle", MUTED, 12.5)
    return svg("Two ways to reason about a problem. By analogy: ask how others do it, copy it and adjust a little, and get a result "
               "close to theirs; fast and usually good enough, but it inherits everyone's assumptions. From first principles, in five "
               "steps: state the problem in numbers, break it into its parts, sort facts from assumptions, test the assumptions, then "
               "rebuild and try it small; slower and harder, but it can find an option nobody has tried.", 838, 210, s, 640, 10)


def fig_waterfall():
    """Ingredient cost: what the recipe needs, then each loss, up to what is bought."""
    s = DEFS
    x0, base, sc, AX = 96, 300, 600 / 1e6, 2_000_000   # axis starts at $2.0M; $0.4M -> 240 px
    bars = [("Recipe needs", SPEND * Y, 0, BLUE)]
    run = SPEND * Y
    for name, now, _, _ in LOSSES:
        v = SPEND * now / 100; bars.append((name, v, run, ORANGE)); run += v
    bars.append(("Bought", SPEND, 0, NAVY))
    labels = [["What the", "recipe needs"], ["Changeover", "purges"], ["Overfill"], ["Rejected", "bars"], ["Spills and", "other"], ["What is", "bought"]]
    w, gap = 78, 30
    for i, (name, v, start, col) in enumerate(bars):
        x = x0 + i * (w + gap)
        lo = max(start, AX) if start else AX
        y1 = base - (start + v - AX) * sc; h = (start + v - lo) * sc
        s += f'<rect x="{x}" y="{y1:.1f}" width="{w}" height="{max(h, 1):.1f}" fill="{col}" rx="3"/>'
        val = m(v / 1000) + "k" if v < 1_000_000 else f"${v / 1e6:.2f}M"
        s += txt(x + w / 2, y1 - 7, val, "middle", NAVY, 12.5, True)
        for j, ln in enumerate(labels[i]): s += txt(x + w / 2, base + 20 + j * 16, ln, "middle", NAVY, 12)
        if 0 < i < len(bars) - 1:
            pass
    s += f'<line x1="{x0 - 10}" y1="{base}" x2="{x0 + 6 * (w + gap) - gap + 10}" y2="{base}" stroke="{LINE}"/>'
    s += txt(x0 - 14, base + 4, "$2.0M", "end", MUTED, 11.5)
    s += f'<path d="M{x0 - 4},{base - 12} l8,-4 l-8,-4 l8,-4" fill="none" stroke="{MUTED}"/>'
    s += txt(x0 + 3 * (w + gap) - gap / 2, 22, f"Losses: {m(GAP_NOW)} a year ({LOSS_NOW:.0f}% of what is bought)", "middle", ORANGE, 13, True)
    return svg(f"A waterfall chart of ingredient cost at the example snack bar plant. The recipe needs {m(SPEND * Y)} of ingredients a year. "
               f"Changeover purges add {m(SPEND * .035)}, overfill {m(SPEND * .025)}, rejected bars {m(SPEND * .02)} and spills and other losses "
               f"{m(SPEND * .01)}, so the plant buys {m(SPEND)}. The vertical axis starts at $2.0 million. Losses total {m(GAP_NOW)} a year, {LOSS_NOW:.0f}% of what is bought.", 766, 350, s, 560)


def fig_shouldcost():
    """Stacked bars: supplier quote against should-cost as drawn and after the changes."""
    s = DEFS
    cols = {"Material": BLUE, "Machining": PURPLE, "Set-up": "#7FB2CF", "Deburr and inspect": "#8794A1", "Anodizing": "#B9A6E0",
            "Overhead and profit": GREEN}
    base, sc, x0, w = 300, 6.4, 110, 110
    def stack(x, rows, sub, tot, title):
        out, y = "", base
        for name, _, v in rows + [("Overhead and profit", "", tot - sub)]:
            h = v * sc; y -= h
            out += f'<rect x="{x}" y="{y:.1f}" width="{w}" height="{h:.1f}" fill="{cols[name]}" stroke="#fff"/>'
            if h > 16: out += txt(x + w / 2, y + h / 2 + 4.5, m2(v), "middle", "#fff", 12, True)
        out += txt(x + w / 2, y - 8, m2(tot), "middle", NAVY, 13.5, True)
        for j, ln in enumerate(title): out += txt(x + w / 2, base + 20 + j * 16, ln, "middle", NAVY, 12.5)
        return out
    y = base - QUOTE * sc
    s += f'<rect x="{x0}" y="{y:.1f}" width="{w}" height="{QUOTE * sc:.1f}" fill="#EEF0F3" stroke="#B8C2CC"/>'
    s += txt(x0 + w / 2, y + QUOTE * sc / 2, "No breakdown", "middle", MUTED, 12) + txt(x0 + w / 2, y - 8, m2(QUOTE), "middle", NAVY, 13.5, True)
    s += txt(x0 + w / 2, base + 20, "Supplier's quote", "middle", NAVY, 12.5)
    s += stack(x0 + 170, *SC_A, ["Should-cost,", "as drawn"])
    s += stack(x0 + 340, *SC_B, ["Should-cost,", "after changes"])
    s += f'<line x1="{x0 - 20}" y1="{base}" x2="{x0 + 340 + w + 20}" y2="{base}" stroke="{LINE}"/>'
    ly = 70
    for i, (k, c) in enumerate(cols.items()):
        s += f'<rect x="{x0 + 500}" y="{ly + i * 24 - 11}" width="14" height="14" fill="{c}" rx="2"/>' + txt(x0 + 522, ly + i * 24, k, "start", NAVY, 12.5)
    return svg(f"Stacked bars comparing the supplier's quote of {m2(QUOTE)} per bracket, with no breakdown, against a should-cost of "
               f"{m2(SC_A[2])} as the part is drawn and ordered, and {m2(SC_B[2])} after the tolerances are opened on non-critical faces and "
               f"the batch is raised to 500. In both should-cost bars machining time is the largest part and material is the second.",
               800, 350, s, 600, 80)


def body():
    loss_rows = "".join(f'<tr><td class="nw">{n}</td><td class="num">{a:.1f}%</td><td class="num">{m(SPEND * a / 100)}</td>'
                        f'<td class="num">{b:.1f}%</td><td>{fx}</td></tr>' for n, a, b, fx in LOSSES)
    sc_rows = "".join(f'<tr><td class="nw">{a[0]}</td><td>{a[1]}</td><td class="num">{m2(a[2])}</td><td>{b[1]}</td><td class="num">{m2(b[2])}</td></tr>'
                      for a, b in zip(SC_A[0], SC_B[0]))
    return f"""{F.CSS}<p>Most business decisions are made by analogy. We look at what competitors do, what we did last year or what the industry calls normal, and adjust it a little. That is fast and usually good enough. It also means every inherited assumption comes along for free.</p>
<p>First principles thinking does the opposite. It breaks a problem down to what must be true, sets aside what is only habit, and builds the answer up again from there. This article explains where the idea comes from, gives a five-step method, and works through two examples with numbers: a food plant that blamed ingredient prices for its costs, and a purchased part whose price nobody had questioned. A calculator lets you test the first example with your own figures. The article was first published in October 2025 and has been rewritten and extended.</p>

<h2>What first principles thinking means</h2>
<p>Aristotle described a first principle as the first basis from which a thing is known: a starting point that does not depend on anything more basic. Physics and engineering work this way. A chemical engineer sizing a plant does not start from what a similar plant used. The engineer starts from conservation of mass and energy, because every kilogram that goes in must come out somewhere, and builds the design up from there.</p>
<p>In business the idea is the same, applied to costs, constraints and customer needs. You ask what is actually required, what it would cost at its physical or contractual minimum, and why the current answer is so far from that minimum.</p>
<p class="oee-cap">Table 1. Reasoning by analogy and from first principles</p>
<table>
<tr><th></th><th>By analogy</th><th>From first principles</th></tr>
<tr><td class="nw">Starting question</td><td>How do others do it?</td><td>What has to be true?</td></tr>
<tr><td class="nw">Starting data</td><td>Benchmarks, past practice, industry norms</td><td>Physical limits, laws, contracts, measured facts</td></tr>
<tr><td class="nw">Speed</td><td>Fast</td><td>Slow; needs data and time to think</td></tr>
<tr><td class="nw">Typical result</td><td>A small improvement on the current way</td><td>Sometimes a different way altogether</td></tr>
<tr><td class="nw">Main risk</td><td>Copies other people's mistakes</td><td>Reinvents things that already work</td></tr>
<tr><td class="nw">Best used for</td><td>Routine, low-stakes, reversible decisions</td><td>Large costs, hard constraints, problems that have resisted normal fixes</td></tr>
</table>
{fig(fig_paths(), 1, "Two ways to reason about a problem. The five steps in the lower lane are explained below.")}

<h2>The best-known example</h2>
<p>Elon Musk made the term popular in business. In a 2012 video interview with Kevin Rose he described how battery packs were then said to cost about $600 per kilowatt-hour, and the common view was that they would stay expensive. His team instead listed what a battery is made of (carbon, nickel, aluminium, polymers and a steel can) and priced those materials at commodity-exchange rates. The answer was about $80 per kilowatt-hour. The gap between $80 and $600 was not set by nature. It came from how cells were designed and made, which meant it could be attacked.</p>
<p>The lesson for a small business is not about batteries. It is the method: work out the floor set by materials, physics or contracts, compare it with what you pay or accept today, and ask what fills the gap.</p>

<h2>Facts, constraints and assumptions</h2>
<p>The core skill is sorting statements into three kinds. Teams usually treat all three as fixed. Only the first two are.</p>
<p class="oee-cap">Table 2. Three kinds of statement and how to test each</p>
<table>
<tr><th>Kind</th><th>What it is</th><th>Example</th><th>How to test it</th></tr>
<tr><td class="nw">Hard constraint</td><td>Physics, law, safety code or a signed contract</td><td>Packaged food must contain its declared net quantity, within the tolerance set in the regulations</td><td>Read the rule or contract itself, not someone's summary of it</td></tr>
<tr><td class="nw">Measured fact</td><td>Something observed and recorded</td><td>9% of ingredients bought never reach a sold bar</td><td>Check how it was measured, by whom and over what period</td></tr>
<tr><td class="nw">Assumption</td><td>A belief, habit or rule of thumb</td><td>"Ingredient prices are the problem and we can't control them"</td><td>Ask what evidence supports it and what would change if it were false</td></tr>
</table>
<p>A useful sign of an assumption is a sentence that starts with "we always", "customers expect", "the industry standard is" or "we can't". Each may be true. None is a first principle until it has been checked.</p>

<h2>The five steps</h2>
<h3>1. State the problem in numbers</h3>
<p>"Margins are falling" is a complaint. "Ingredient cost rose from 38% to 43% of sales in two years" is a problem you can break down. Put a number, a unit and a time period on it.</p>
<h3>2. Break it into its parts</h3>
<p>Draw the problem as a tree. Cost splits into price times quantity; quantity splits into what the product needs and what is lost. Revenue splits into customers, orders per customer and value per order. Keep splitting until each branch is something you can measure.</p>
<h3>3. Sort facts from assumptions</h3>
<p>Go through each branch with Table 2. Mark what is a hard constraint, what has been measured, and what is believed. The believed items are where the opportunity usually is.</p>
<h3>4. Test the assumptions</h3>
<p>Find the cheapest way to check each important assumption: a week of measurement, a call to a supplier, a reading of the actual regulation, a small trial. Work out the theoretical minimum for the branch (the cost if nothing were lost, the time if nothing waited) so you know how big the gap is.</p>
<h3>5. Rebuild and try it small</h3>
<p>Put the parts back together using only what survived the test. Then try the new design on one product, one line or one customer before rolling it out. A first-principles answer is still a hypothesis until it works in practice.</p>

<h2>Questions that expose assumptions</h2>
<p class="oee-cap">Table 3. Questions to ask at each branch of the tree</p>
<table>
<tr><th>Purpose</th><th>Question</th></tr>
<tr><td class="nw">Clarify</td><td>What exactly do we mean by this? How is it measured?</td></tr>
<tr><td class="nw">Find the source</td><td>Where did this rule come from? Who decided it, and when?</td></tr>
<tr><td class="nw">Check the evidence</td><td>What data shows this is true today, here, for us?</td></tr>
<tr><td class="nw">Find the floor</td><td>What would this cost, or how long would it take, if nothing were wasted?</td></tr>
<tr><td class="nw">Test the opposite</td><td>What would have to be true for the opposite to work?</td></tr>
<tr><td class="nw">Check the consequence</td><td>If this assumption is wrong, what changes, and how much is it worth?</td></tr>
</table>

<h2>Worked example 1: "ingredient prices are killing our margin"</h2>
<p>A snack bar maker buys {m(SPEND)} of ingredients a year. Ingredient cost has risen as a share of sales, and the management team's view is that world commodity prices are to blame and nothing can be done internally.</p>
<p><strong>Step 1, the problem in numbers.</strong> Ingredient cost is 43% of sales, up from 38%.</p>
<p><strong>Step 2, the parts.</strong> Ingredient cost = price per kilogram × kilograms bought. Kilograms bought = kilograms the recipe needs + kilograms lost.</p>
<p><strong>Step 3, facts and assumptions.</strong> Prices rising is a fact. "Nothing can be done" is an assumption. Nobody had measured the second branch, the kilograms lost.</p>
<p><strong>Step 4, the test.</strong> A mass balance does the work. The recipes say how much of each ingredient goes into a bar, and the sales records say how many bars were sold. Multiplied together, they give what the plant should have bought if nothing were lost. It bought {LOSS_NOW:.0f}% more. That {LOSS_NOW:.0f}% is worth {m(GAP_NOW)} a year, and a week of weighing at each step showed where it goes (Figure 2 and Table 4).</p>
{fig(fig_waterfall(), 2, "Where the ingredient money goes in the example. Orange bars are losses. The vertical axis starts at $2.0 million so the losses can be seen.")}
<p class="oee-cap">Table 4. Ingredient losses and the first round of fixes</p>
<table>
<tr><th>Loss</th><th class="num">Now</th><th class="num">A year</th><th class="num">After</th><th>Fix</th></tr>
{loss_rows}
<tr class="oee-total"><td>Total</td><td class="num">{LOSS_NOW:.1f}%</td><td class="num">{m(GAP_NOW)}</td><td class="num">{LOSS_NEW:.1f}%</td><td></td></tr>
</table>
<p><strong>Step 5, rebuild.</strong> None of the fixes touches the supplier or the price list. Yield, the share of ingredients that ends up in a sold bar, rises from {Y:.0%} to {YT:.1%}. The plant can make the same output while buying less:</p>
{eq(r"\text{Saving a year} = M\left(1-\frac{Y}{Y^{*}}\right)")}
<p>where {im("M")} is the ingredients bought a year, {im("Y")} the yield now and {im("Y^{*}")} the yield after the fixes. Here {im(r"2{,}400{,}000 \times (1 - 0.910/0.944)")} ≈ {m(SAVE)} a year. With an assumed {m(COST)} for a checkweigher, scheduling work and training, payback is about {PAYBACK:.0f} months. The first round closes {SAVE / GAP_NOW:.0%} of the gap to the theoretical minimum, and the rest is a target for the next round.</p>
<p>Two points in this example are worth noting. The overfill fix needed the actual rule, not the rule of thumb: the line had been set well above the label weight "to be safe", and nobody had read what the net quantity rules in the Safe Food for Canadians Regulations actually require. And the changeover fix is a scheduling decision, which is why the team that owned the schedule had never seen it as an ingredient cost. The same losses show up in {P(OEE, "OEE")} as quality and changeover losses; {P(OEEC, "What OEE Losses Cost")} puts dollars on them.</p>

<div class="oee-calc" role="group" aria-labelledby="fph">
<h3 id="fph">Try it: the value of closing a yield gap</h3>
<p class="oee-hint">The starting values are the example above. Set your own material spend, the yield you measure today, the yield you think is reachable and the cost of the work.</p>
<div class="oee-sliders">
<div class="oee-sl"><label for="fp-m">Material bought a year <output id="fp-m-o"></output></label><input type="range" id="fp-m" min="200000" max="10000000" step="100000" value="{SPEND}"></div>
<div class="oee-sl"><label for="fp-y">Yield today <output id="fp-y-o"></output></label><input type="range" id="fp-y" min="70" max="99.5" step="0.5" value="{Y * 100:.1f}"></div>
<div class="oee-sl"><label for="fp-t">Target yield <output id="fp-t-o"></output></label><input type="range" id="fp-t" min="70" max="100" step="0.1" value="{YT * 100:.1f}"></div>
<div class="oee-sl"><label for="fp-c">Cost of the work <output id="fp-c-o"></output></label><input type="range" id="fp-c" min="5000" max="500000" step="5000" value="{COST}"></div>
</div>
<div class="oee-tiles">
<div class="oee-tile"><span class="k">Lost today</span><span class="v" id="fp-gap"></span><span class="n">a year, against a perfect yield</span></div>
<div class="oee-tile key"><span class="k">Saving</span><span class="v" id="fp-save"></span><span class="n">a year at the target yield</span></div>
<div class="oee-tile"><span class="k">Payback</span><span class="v" id="fp-pay"></span></div>
<div class="oee-tile"><span class="k">Each point of yield</span><span class="v" id="fp-pt"></span><span class="n">a year, near today's yield</span></div>
</div>
</div>

<h2>Worked example 2: a price nobody had questioned</h2>
<p>A machinery builder buys {QTY:,} aluminium brackets a year from one machine shop at {m2(QUOTE)} each, {m(QUOTE * QTY)} a year. The price has risen with every renewal, and the buyer's view is that "that's what machining costs". The first-principles version is a should-cost: build the price up from what the part physically needs.</p>
<p class="oee-cap">Table 5. Should-cost of the bracket, as drawn and after two changes</p>
<table>
<tr><th>Element</th><th>As drawn, 100 a month</th><th class="num">Per part</th><th>After changes, 500 a quarter</th><th class="num">Per part</th></tr>
{sc_rows}
<tr><td class="nw">Overhead and profit</td><td>15% of the above</td><td class="num">{m2(SC_A[2] - SC_A[1])}</td><td>15% of the above</td><td class="num">{m2(SC_B[2] - SC_B[1])}</td></tr>
<tr class="oee-total"><td>Should-cost</td><td></td><td class="num">{m2(SC_A[2])}</td><td></td><td class="num">{m2(SC_B[2])}</td></tr>
</table>
{fig(fig_shouldcost(), 3, "The supplier's quote against the should-cost. Machining time, not aluminium, is the largest element.")}
<p>Three things come out of the build-up:</p>
<ul>
<li><strong>Material is under a third of the cost.</strong> Arguing about aluminium prices would have missed the point.</li>
<li><strong>Machining time is the biggest element, and the drawing drives it.</strong> Every face carried a tight tolerance copied from an older part. Only two faces locate anything. Opening the others lets the shop cut faster and skip a finishing pass: 7 minutes becomes 5 in the example.</li>
<li><strong>Ordering 100 a month repeats the set-up twelve times a year.</strong> A quarterly order of 500, with the shop holding a small stock, spreads the set-up across five times as many parts.</li>
</ul>
<p>The should-cost does not tell the supplier what to charge. It gives both sides a shared picture of where the cost is. In the example, the buyer takes the revised drawing and the new order pattern to the supplier and agrees {m2(TARGET)}, which still leaves the shop a better margin than the should-cost assumes. That saves {m(SAVE2)} a year on one part number, and the same review can be repeated on the next ten.</p>
<p>Make sure engineering approves any change to a drawing. A tolerance that looks arbitrary may protect a fit or a safety function. Checking that is part of step 4.</p>

<h2>Common business assumptions worth testing</h2>
<p class="oee-cap">Table 6. Assumptions that often fail a first-principles check</p>
<table>
<tr><th>Assumption</th><th>First-principles question</th><th>What is often found</th></tr>
<tr><td>"We need more capacity"</td><td>How many hours does the bottleneck actually make good product?</td><td>Lost hours to stoppages, slow running and changeovers, often 30 to 40% of planned time. See {P(OEE, "What OEE Really Measures")}.</td></tr>
<tr><td>"We need more customers"</td><td>Revenue = customers × orders each × value per order. Which branch is weak?</td><td>Customers leave or order less often; retention is cheaper to fix than acquisition</td></tr>
<tr><td>"Cash is tight because sales are down"</td><td>How many days pass between paying for materials and being paid?</td><td>Weeks lost to slow quotes, late invoices and unchased debts. See {P(Q2C, "the quote-to-cash process")}.</td></tr>
<tr><td>"We need more stock to avoid running out"</td><td>What does demand variation and supplier lead time actually require?</td><td>Too much stock of slow items and too little of the critical ones. See {P(SS, "setting safety stock")}.</td></tr>
<tr><td>"We need a new system"</td><td>Which steps of the process fail, and why?</td><td>A broken process that a new system would only speed up</td></tr>
<tr><td>"Our price must match the competitor's"</td><td>What does the customer value, and what does it cost us to provide?</td><td>Customers paying for speed, reliability or service the price list ignores</td></tr>
</table>

<h2>How it fits with other problem-solving tools</h2>
<p class="oee-cap">Table 7. First principles and related tools</p>
<table>
<tr><th>Tool</th><th>What it does</th><th>How it relates</th></tr>
<tr><td class="nw">5 Whys</td><td>Follows one chain of cause back from a failure</td><td>Good for a single incident; first principles questions the whole design, not one failure</td></tr>
<tr><td class="nw">Root cause analysis</td><td>Finds why a known problem happens</td><td>Assumes the target is right; first principles asks whether the target itself is</td></tr>
<tr><td class="nw">Zero-based budgeting</td><td>Justifies every cost from zero each period</td><td>First principles applied to a budget</td></tr>
<tr><td class="nw">Mass and energy balance</td><td>Accounts for every unit of input</td><td>The engineer's way of finding the theoretical minimum (example 1)</td></tr>
<tr><td class="nw">Should-cost model</td><td>Builds a price up from its parts</td><td>First principles applied to purchasing (example 2)</td></tr>
<tr><td class="nw">Benchmarking</td><td>Compares you with others</td><td>Reasoning by analogy; useful for spotting gaps, not for setting the floor</td></tr>
</table>
<p>For a structured way to measure the distance between where a process is and where it should be, see {P(GAP, "how to run a gap analysis")}. For the waste categories that usually fill the gap, see {P(LEAN, "Lean methodology")}.</p>

<h2>When not to use it</h2>
<ul>
<li><strong>Routine, reversible decisions.</strong> Choosing a printer or a meeting time by analogy is fine. Save the effort for large costs and stubborn problems.</li>
<li><strong>Rules that exist for a reason you have not found yet.</strong> Before removing a step, find out why it was put there. A check that looks pointless may be the one that stopped a recall years ago.</li>
<li><strong>Proven methods.</strong> Accounting standards, safety codes and established engineering practice already encode first principles. Rebuilding them from scratch wastes time and adds risk.</li>
<li><strong>Problems without data.</strong> If nothing can be measured, the method turns into opinion. Collect a week of data first.</li>
</ul>
<p>The common failure is calling an opinion a first principle. "Customers only care about price" is not a fundamental truth because someone senior says it firmly. Test it like any other assumption.</p>

<h2>Making it a team habit</h2>
<p>Pick one recurring problem, such as a cost that keeps rising or a delay nobody can explain, and keep an assumption log while you work on it. One line per belief is enough.</p>
<p class="oee-cap">Table 8. An assumption log</p>
<table>
<tr><th>Assumption</th><th>Kind</th><th>Evidence today</th><th>How we will test it</th><th>Owner and date</th><th>Result</th></tr>
<tr><td>Nothing can be done about ingredient cost</td><td>Assumption</td><td>None; losses never measured</td><td>Mass balance from recipes and sales; one week of weighing</td><td>Plant manager, 2 weeks</td><td>False: 9% lost in the plant</td></tr>
<tr><td>Label weight needs a large safety margin</td><td>Assumption</td><td>"We've always done it"</td><td>Read the net quantity rules; check the checkweigher data</td><td>Quality lead, 1 week</td><td>Margin can be cut by more than half</td></tr>
<tr><td>Bracket tolerances are needed on every face</td><td>Assumption</td><td>Copied from an older drawing</td><td>Engineering review of which faces locate</td><td>Design engineer, 1 week</td><td>Two of eight faces are critical</td></tr>
</table>
<p>Three questions help in any meeting: "Is that a fact, a constraint or an assumption?", "How do we know?" and "What would it be if nothing were wasted?" Ask them about the problem, never about the person, so challenge feels safe. Leaders go first by putting their own assumptions in the log.</p>
<p>To practise the reasoning, try the {f'<a href="{EXAM}">critical thinking for business practice exam</a>'}. For related reading, the review of {P(CLEAR, "Clear Thinking by Shane Parrish")} covers how to stop reacting and start reasoning, and {P(OODA, "OODA vs PDCA")} covers how to turn a decision into a test.</p>

<div class="oee-takeaway"><p><strong>Takeaway.</strong> Put the problem in numbers, break it into parts, and find the floor set by physics, law or contract. Then ask what fills the gap between that floor and today. In the first example the gap was {m(GAP_NOW)} of lost ingredients that everyone had blamed on prices; in the second it was a drawing and an order pattern that nobody had questioned.</p></div>
{NOTE}{JS}{mathjs()}"""


def article():
    sources = [("Aristotle, Metaphysics, Book V, Part 1, translated by W. D. Ross", "https://www.ellopos.net/elpenor/greek-texts/ancient-Greece/aristotle/metaphysics.asp?pg=70"),
               ("Elon Musk on first principles, interview with Kevin Rose (2012), transcript", "https://lawwu.github.io/transcripts/transcript_bLv9MGsUt6g.html"),
               ("Safe Food for Canadians Regulations (SOR/2018-108): net quantity tolerances", "https://laws.justice.gc.ca/eng/regulations/SOR-2018-108/page-27.html"),
               ("Canadian Food Inspection Agency: food net quantity verification", "https://www.inspection.gc.ca/food/compliance-continuum/guidance-for-inspectors/sip/net-quantity-verification/eng/1539273539145/1539273539349")]
    related = [(CLEAR, "Clear Thinking by Shane Parrish: book review and how to apply it"),
               (MCK, "Innovation in a small business: six practices"),
               (OEEC, "What OEE losses cost"),
               (GAP, "How to run a gap analysis")]
    b = body()
    b += "<h2>Sources</h2><ul>" + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in sources) + "</ul>"
    b += "<h2>Related reading</h2><ul>" + "".join(f'<li><a href="../post/{s}.html">{t}</a></li>' for s, t in related) + "</ul>"
    words = len(re.sub(r"<svg.*?</svg>|<script.*?</script>|<link[^>]*>|<[^>]+>", " ", b, flags=re.S).split())
    return dict(slug=SLUG, title="First Principles Thinking for Business: A Five-Step Method with Worked Examples",
                desc="What first principles thinking is, a five-step method for business problems, and two worked examples: an ingredient yield gap and a should-cost model.",
                cats=["process-improvement", "strategy"],
                tags=["first principles thinking", "first principles", "problem solving", "should-cost", "mass balance", "assumptions", "critical thinking"],
                body=F.nowrap(b.strip(), [(1, 0, 20), (2, 0, 20), (3, 0, 22), (4, 0, 32)]), date=DATE, author="Quak Foo Lee",
                read=f"{max(4, round(words / 220))} min read", cover_label="First Principles", related=[r for r, _ in related]), words


if __name__ == "__main__":
    op = os.path.join(HERE, "original_dates.json")
    od = json.load(open(op, encoding="utf-8")); od[SLUG] = ORIGINAL
    note = od.pop("_note"); json.dump({"_note": note, **dict(sorted(od.items()))}, open(op, "w", encoding="utf-8"), indent=1)
    a, n = article()
    json.dump(a, open(os.path.join(HERE, SLUG + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(SLUG[:40], n, "words", a["read"], "| desc", len(a["desc"]), "| save", round(SAVE), "payback", round(PAYBACK, 1),
          "| SC", round(SC_A[2], 2), round(SC_B[2], 2))
