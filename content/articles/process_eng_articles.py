"""Process Engineering articles for Insights: the three-part scale-up series and "How to read a PFD and a P&ID".

Usage:  python3 content/articles/process_eng_articles.py
Writes content/articles/<slug>.json for each article. Then build each page with
        python3 content/gen/add_article.py <slug>
and run python3 content/gen/series_labels.py so the cards show the series label.

The PFD and P&ID drawings are SVG files in assets/media/pfd-pid/. The Part 1 calculator is assets/js/scaleup.js.
Table and layout styles come from assets/css/oee.css. Figure helpers come from feed_articles.py.
"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import (nowrap, svg, fig, box, txt, arrow, DEFS, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, RED,
                           MUTED, LINE, SAND, PALE, GREENF, ORANGEF, S1 as FEED1, S2 as FEED2, S3 as FEED3)

U1 = "scale-up-what-changes-from-lab-to-pilot-to-commercial"
U2 = "what-a-pilot-plant-is-for"
U3 = "from-pilot-data-to-a-mass-and-energy-balance"
PF = "how-to-read-a-pfd-and-a-pid"
K1 = f'<a href="{U1}.html">Post&nbsp;1</a>'
K2 = f'<a href="{U2}.html">Post&nbsp;2</a>'
K3 = f'<a href="{U3}.html">Post&nbsp;3</a>'
NOTE = ('<p class="oee-note"><em>The reaction, the vessels and the costs in this series are an illustrative example. '
        'The calculations are screening estimates and do not replace process safety testing or a design by a qualified engineer.</em></p>')

# ───────────────────────── shared numbers for the scale-up example ─────────────────────────
U_COEF, DT, DH, RHO = 300, 30, 150, 1000          # W/m2.K, K, kJ/kg of batch, kg/m3
SCALES = [("Lab", 0.001, "1 L"), ("Pilot", 0.1, "100 L"), ("Commercial", 10, "10,000 L")]


def geom(V):
    D = (4 * V / math.pi) ** (1 / 3); A = math.pi * D * D
    return D, A, A / V, U_COEF * DT * A / V / 1000                 # diameter m, area m2, m2/m3, kW/m3


GEN = DH * RHO / 3600                                             # kWh of reaction heat per m3 of batch (41.7)


# ───────────────────────── Part 1 figures ─────────────────────────
def fig_vessels():
    s = ""; xs = [110, 330, 590]; hs = [34, 84, 170]; base = 216
    for (name, V, lab), x, h in zip(SCALES, xs, hs):
        D, A, av, _ = geom(V); w = h
        s += f'<rect x="{x - w / 2}" y="{base - h}" width="{w}" height="{h}" rx="{max(4, h * 0.14):.0f}" fill="{PALE}" stroke="{BLUE}" stroke-width="2"/>'
        s += f'<rect x="{x - w / 2 - 5}" y="{base - h * 0.8:.0f}" width="{w + 10}" height="{h * 0.8:.0f}" rx="{max(4, h * 0.14):.0f}" fill="none" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="5 3"/>'
        s += txt(x, base + 24, f"{name}: {lab}", "middle", NAVY, 13.5, True)
        s += txt(x, base + 43, f"Diameter {D:.2f} m", "middle", MUTED, 12.5)
        s += txt(x, base + 61, f"{av:.1f} m² of jacket per m³", "middle", NAVY, 12.5, True)
    s += f'<line x1="10" y1="20" x2="34" y2="20" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="5 3"/>' + txt(42, 24, "Cooling jacket on the wall", fill=MUTED, fs=12.5)
    return svg("Three reactors drawn side by side: a 1 litre lab flask with 36.9 square metres of jacket per cubic metre, a 100 litre pilot reactor "
               "with 8.0, and a 10,000 litre commercial reactor with 1.7. The vessels are not drawn to scale.", 720, 284, s, x0=4)


def fig_capacity():
    X0, X1, YB, YT = 150, 690, 232, 30
    Y = lambda v: YB - (math.log10(v) - 1) / 2 * (YB - YT)           # log axis 10 to 1000 kW/m3
    s = txt(4, 18, "kW per m³ of batch (log scale)", fill=MUTED, fs=12)
    for v in (10, 100, 1000):
        s += f'<line x1="{X0 - 6}" y1="{Y(v):.1f}" x2="{X1}" y2="{Y(v):.1f}" stroke="{LINE}"/>' + txt(X0 - 12, Y(v) + 4, f"{v:,}", "end", MUTED, 12)
    for i, (name, V, lab) in enumerate(SCALES):
        c = geom(V)[3]; x = X0 + 60 + i * 170; ok = c >= GEN
        s += f'<rect x="{x}" y="{Y(c):.1f}" width="90" height="{YB - Y(c):.1f}" rx="4" fill="{BLUE if ok else RED}"/>'
        s += txt(x + 45, Y(c) - 8, f"{c:,.0f} kW/m³" if c >= 100 else f"{c:.1f} kW/m³", "middle", NAVY, 13, True)
        s += txt(x + 45, YB + 20, f"{name}, {lab}", "middle", NAVY, 12.5, True)
    s += f'<line x1="{X0}" y1="{Y(GEN):.1f}" x2="{X1}" y2="{Y(GEN):.1f}" stroke="{ORANGE}" stroke-width="2.2" stroke-dasharray="7 4"/>'
    s += f'<line x1="262" y1="14" x2="296" y2="14" stroke="{ORANGE}" stroke-width="2.2" stroke-dasharray="7 4"/>'
    s += txt(304, 18, f"Heat released when the reaction runs in 1 hour: {GEN:.1f} kW/m³", fill=ORANGE, fs=12.5, bold=True)
    return svg("Bar chart on a log scale of the cooling capacity per cubic metre: 332 kilowatts in the 1 litre lab reactor, 71.6 in the 100 litre pilot "
               "reactor and 15.4 in the 10,000 litre commercial reactor. A line at 41.7 marks the heat released when the reaction runs in one hour. "
               "Only the commercial reactor falls below the line.", 694, 262, s, x0=0)


def post_s1():
    rows = "".join(f'<tr><td class="nw">{n}</td><td class="num">{lab}</td><td class="num">{geom(V)[0]:.2f} m</td>'
                   f'<td class="num">{geom(V)[2]:.1f} m²/m³</td><td class="num">{geom(V)[3]:,.1f} kW/m³</td>'
                   f'<td class="num">{GEN / geom(V)[3] * 60:,.0f} min</td></tr>' for n, V, lab in SCALES)
    r = 10000 ** (1 / 3)
    return f"""{CSS}<p>A reaction that behaves in a one-litre flask can overheat in a ten-cubic-metre reactor with the same recipe. The chemistry is identical. The geometry has changed, and with it the rate at which the vessel can remove heat and mix its contents.</p>
<p>This series follows one example: an exothermic liquid reaction scaled from a 1&nbsp;L lab reactor to a 100&nbsp;L pilot reactor and then to a 10,000&nbsp;L commercial reactor. This post covers what changes with size. {K2} covers what the pilot plant must find out, and {K3} turns the pilot data into a mass and energy balance.</p>
<h2>Volume grows faster than surface area</h2>
<p>Heat is generated throughout the volume of the liquid and leaves through the wall. When a vessel is made larger in every direction, its volume rises with the cube of the diameter and its wall area with the square. The area available per cubic metre therefore falls as the vessel grows.</p>
<p class="oee-formula">Jacket area per unit volume = 4 ÷ diameter &nbsp;(for a vessel filled to a depth equal to its diameter)</p>
{fig(fig_vessels(), 1, "The same reactor shape at three sizes, not drawn to scale. Each step is 100 times the volume, and the jacket area per cubic metre falls by a factor of 4.6 each time.")}
<p>From 1&nbsp;L to 10,000&nbsp;L the volume increases 10,000 times and the jacket area per cubic metre falls {r:.1f} times.</p>
<h2>Worked example: can the jacket remove the heat?</h2>
<p>Suppose the reaction releases {DH}&nbsp;kJ for each kilogram of batch. A jacket removes heat at a rate set by three things: the heat transfer coefficient, the wall area and the temperature difference between the batch and the coolant.</p>
<p class="oee-formula">Cooling capacity = U × A × ΔT = {U_COEF} W/m²·K × A × {DT} K</p>
<p class="oee-cap">Table 1. Cooling capacity at three scales, for U = {U_COEF} W/m²·K and ΔT = {DT} K</p>
<table>
<tr><th>Scale</th><th class="num">Volume</th><th class="num">Diameter</th><th style="text-align:right">Jacket area per volume</th><th style="text-align:right">Cooling capacity</th><th style="text-align:right">Shortest safe reaction time</th></tr>
{rows}
</table>
<p>The heat to remove is {DH}&nbsp;kJ/kg × {RHO:,}&nbsp;kg/m³ = {DH * RHO:,}&nbsp;kJ per cubic metre of batch, or {GEN:.1f}&nbsp;kWh. If the reaction is run in one hour, as in the lab, the heat is released at {GEN:.1f}&nbsp;kW per cubic metre.</p>
{fig(fig_capacity(), 2, "Cooling capacity per cubic metre against the heat released by a one-hour reaction. The lab and pilot reactors have capacity to spare. The commercial reactor does not.")}
<p>The lab reactor can remove eight times the heat that is generated, and the pilot reactor 1.7 times. The commercial reactor can remove only {geom(10)[3]:.1f}&nbsp;kW/m³ against {GEN:.1f}&nbsp;kW/m³ generated. With the lab recipe, its temperature would climb.</p>
<p>The usual answer is to add one reactant gradually, so the reaction can only proceed as fast as the feed arrives. The addition time must then be at least:</p>
<p class="oee-formula">{GEN:.1f} kWh/m³ ÷ {geom(10)[3]:.1f} kW/m³ = {GEN / geom(10)[3]:.1f} hours</p>
<p>A one-hour lab procedure becomes an addition of about three hours in the plant. That change affects the batch cycle time, the number of batches a year and the size of the reactor needed for a given output.</p>
<div class="oee-calc" role="group" aria-labelledby="suh">
<h3 id="suh">Try it: cooling capacity at your scale</h3>
<p class="oee-hint">Set the reactor volume and the reaction data. The calculator assumes a jacket on the wall only, a liquid depth equal to the diameter and a batch density of 1,000 kg/m³.</p>
<div class="oee-sliders">
<div class="oee-sl"><label for="su-V">Reactor volume <output id="su-V-o"></output></label><input type="range" id="su-V" min="0" max="4.6" step="0.05" value="4"></div>
<div class="oee-sl"><label for="su-U">Heat transfer coefficient, U <output id="su-U-o"></output></label><input type="range" id="su-U" min="100" max="600" step="10" value="{U_COEF}"></div>
<div class="oee-sl"><label for="su-T">Temperature difference, ΔT <output id="su-T-o"></output></label><input type="range" id="su-T" min="5" max="60" step="1" value="{DT}"></div>
<div class="oee-sl"><label for="su-H">Heat of reaction <output id="su-H-o"></output></label><input type="range" id="su-H" min="20" max="400" step="5" value="{DH}"></div>
<div class="oee-sl"><label for="su-t">Planned addition time <output id="su-t-o"></output></label><input type="range" id="su-t" min="0.25" max="12" step="0.25" value="1"></div>
</div>
<div class="oee-tiles">
<div class="oee-tile"><span class="k">Jacket area per volume</span><span class="v" id="su-av"></span></div>
<div class="oee-tile"><span class="k">Cooling capacity</span><span class="v" id="su-c"></span><span class="n">per m³ of batch</span></div>
<div class="oee-tile"><span class="k">Heat release rate</span><span class="v" id="su-g"></span><span class="n">at the planned time</span></div>
<div class="oee-tile key"><span class="k">Shortest safe addition</span><span class="v" id="su-m"></span><span class="n" id="su-ok"></span></div>
</div>
<figure>
<div class="oee-chart" id="su-chart"></div>
<figcaption>Figure 3. Cooling capacity against reactor volume for your inputs. The dashed line is the heat release rate at the planned addition time.</figcaption>
</figure>
</div>
<h2>What else changes with size</h2>
<p>Heat removal is usually the first limit, and several other quantities change at the same time. The table assumes the same vessel shape and the same agitator power per cubic metre at each scale.</p>
<p class="oee-cap">Table 2. How key quantities change from 1 L to 10,000 L</p>
<table>
<tr><th>Quantity</th><th>Changes with</th><th class="num">1 L to 10,000 L</th><th>What it means in the plant</th></tr>
<tr><td>Jacket area per volume</td><td>1 ÷ diameter</td><td class="num">÷ {r:.1f}</td><td>Less cooling and heating per kilogram of batch</td></tr>
<tr><td>Heat-up and cool-down time</td><td>Diameter</td><td class="num">× {r:.1f}</td><td>Minutes in the lab become hours</td></tr>
<tr><td>Mixing time</td><td>Diameter to the power ⅔</td><td class="num">× {r ** (2 / 3):.1f}</td><td>Added reactant stays concentrated for longer, which can change selectivity</td></tr>
<tr><td>Agitator tip speed</td><td>Diameter to the power ⅓</td><td class="num">× {r ** (1 / 3):.1f}</td><td>More shear, which matters for crystals, emulsions and cells</td></tr>
<tr><td>Liquid depth</td><td>Diameter</td><td class="num">× {r:.1f}</td><td>Higher pressure at the bottom changes boiling point and gas solubility</td></tr>
</table>
<p>No single rule keeps all of these constant. Scale-up means deciding which quantity matters most for the process and holding that one, then checking that the others stay acceptable. Finding out which one matters is the purpose of the pilot plant, covered in {K2}.</p>
<h2>Three cautions</h2>
<ul>
<li><strong>The heat transfer coefficient is not constant.</strong> Thicker walls, glass lining and fouling all lower it at plant scale. Measure it on the pilot reactor and check the vendor's figure for the commercial vessel.</li>
<li><strong>Gradual addition only works if the reaction keeps up.</strong> If the reactant accumulates unreacted and then reacts all at once, the heat arrives faster than the feed rate suggests. Reaction calorimetry shows whether this can happen.</li>
<li><strong>Cooling failure must be assessed separately.</strong> This post covers normal operation. The temperature the batch could reach with no cooling at all is a process safety question and needs its own study.</li>
</ul>
<p>To practise the calculations, try the free <a href="../scale-up-exam.html">Engineering Scale Up Exam&nbsp;I</a> and the <a href="../engineering-scale-up-calc-exam-iii.html">Scale Up Calc Exam&nbsp;III</a>.</p>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> Cooling capacity per cubic metre falls as the reactor grows. In the example it drops from {geom(0.001)[3]:,.0f} to {geom(10)[3]:.1f}&nbsp;kW/m³, and a one-hour lab reaction needs at least {GEN / geom(10)[3]:.1f} hours of controlled addition at 10,000&nbsp;L.</p></div>
<div class="oee-next"><a class="oee-fwd" href="{U2}.html">Next: Post&nbsp;2, what a pilot plant is for →</a></div>
<noscript><p class="oee-note">The calculator on this page needs JavaScript. The tables show the worked example.</p></noscript>
{NOTE}
<script src="../assets/js/scaleup.js" defer></script>"""


# ───────────────────────── Part 2 ─────────────────────────
YIELDS = [86, 88, 87, 85, 89, 88, 87, 88, 86, 88]
YMEAN = sum(YIELDS) / len(YIELDS)
YD = round(YMEAN)                                                 # design yield, %


def fig_loop():
    s = DEFS
    s += box(10, 60, 190, 80, ["Open questions", "from the lab"], fill=ORANGEF, stroke="#E0B877", fs=13.5)
    s += box(265, 60, 190, 80, ["Pilot plant runs", "designed to answer them"], fill=PALE, fs=13.5)
    s += box(520, 60, 190, 80, ["Measured data for", "the commercial design"], fill=GREENF, stroke="#A9C77E", fs=13.5)
    s += arrow(200, 100, 263, 100, w=2) + arrow(455, 100, 518, 100, w=2)
    s += f'<path d="M615,140 V176 Q615,186 605,186 H115 Q105,186 105,176 V150" fill="none" stroke="{NAVY}" stroke-width="1.4" stroke-dasharray="4 3"/>'
    s += f'<line x1="105" y1="156" x2="105" y2="150" stroke="{NAVY}" stroke-width="1.4"/><path d="M99.5,151 L110.5,151 L105,141 z" fill="{NAVY}"/>'
    s += txt(360, 206, "A result that raises a new question goes back on the list", "middle", MUTED, 12.5)
    s += txt(105, 44, "Before the pilot", "middle", MUTED, 12.5) + txt(360, 44, "During", "middle", MUTED, 12.5) + txt(615, 44, "After", "middle", MUTED, 12.5)
    return svg("Three boxes in a row: open questions from the lab, pilot plant runs designed to answer them, and measured data for the commercial design. "
               "A dashed arrow returns from the data to the questions.", 702, 216, s, x0=9)


def fig_yield():
    X = lambda i: 90 + i * 64; Y = lambda v: 222 - (v - 82) * 22; s = ""
    for v in (82, 84, 86, 88, 90):
        s += f'<line x1="60" y1="{Y(v)}" x2="690" y2="{Y(v)}" stroke="{LINE}"/>' + txt(52, Y(v) + 4, f"{v}%", "end", MUTED, 12)
    s += f'<rect x="60" y="{Y(max(YIELDS))}" width="630" height="{Y(min(YIELDS)) - Y(max(YIELDS))}" fill="{BLUE}" opacity=".10"/>'
    s += f'<line x1="60" y1="{Y(YMEAN):.1f}" x2="690" y2="{Y(YMEAN):.1f}" stroke="{GREEND}" stroke-width="2" stroke-dasharray="7 4"/>'
    s += txt(698, Y(YMEAN) + 4.5, f"Mean {YMEAN:.1f}%", fill=GREEND, fs=12.5, bold=True)
    s += f'<polyline points="{" ".join(f"{X(i)},{Y(v)}" for i, v in enumerate(YIELDS))}" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
    for i, v in enumerate(YIELDS):
        s += f'<circle cx="{X(i)}" cy="{Y(v)}" r="5.5" fill="{BLUE}"/>' + txt(X(i), 246, str(i + 1), "middle", MUTED, 12)
    s += txt(18, 18, "Yield", fill=MUTED, fs=12) + txt(375, 266, "Pilot run number", "middle", MUTED, 12.5)
    return svg(f"Line chart of yield in ten consecutive pilot runs, between {min(YIELDS)}% and {max(YIELDS)}% with a mean of {YMEAN:.1f}%.", 764, 274, s, x0=16)


def post_s2():
    q = [("How fast is heat released, and can any reactant build up unreacted?", "Heat flow and conversion against time during the addition", "Addition time, cooling system, relief design"),
         ("Is the result sensitive to mixing?", "Yield and impurities at two or three agitator speeds", "Agitator type and power, feed point location"),
         ("How well does the product filter, wash and dry?", "Filtration rate, cake moisture, drying curve", "Filter and dryer type and size"),
         ("What do recycled streams do over many batches?", "Impurity levels in recycled solvent over consecutive runs", "Purge rate, solvent make-up, purification steps"),
         ("Which materials resist the process fluids?", "Corrosion coupons and gasket samples exposed in the reactor", "Materials of construction"),
         ("Does commercial-grade raw material give the same product?", "Runs using the grade and supplier planned for the plant", "Raw material specifications in the design basis"),
         ("What leaves as waste and emissions?", "Quantity and composition of every waste stream and vent", "Treatment systems and permit applications"),
         ("Can operators run and clean it?", "Blockages, fouling, cleaning time, manual interventions", "Operating procedures, staffing, cycle time")]
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in q)
    return f"""{CSS}<p>A pilot plant exists to answer the questions the laboratory cannot. Its product is data. A pilot campaign that makes good material and leaves those questions open has not done its job.</p>
<p>{K1} showed why size changes behaviour, using a reaction scaled from 1&nbsp;L to 10,000&nbsp;L. This post covers the middle step, the 100&nbsp;L pilot reactor: what it should be designed to find out, how large it should be, and what to have in hand before it is shut down. {K3} uses the results.</p>
<h2>Start from the questions</h2>
<p>The pilot plant sits between two lists. The first is the list of questions the lab work left open. The second is the list of numbers the commercial design needs. Each pilot run should move an item from the first list to the second.</p>
{fig(fig_loop(), 1, "A pilot campaign is planned from the open questions and judged by the design data it produces.")}
<p class="oee-cap">Table 1. Eight questions a pilot plant commonly has to answer</p>
<table>
<tr><th>Question</th><th>What to measure</th><th>Design decision it feeds</th></tr>
{rows}
</table>
<p>Not every project has all eight. A project should write down its own list before the pilot plant is designed, because the list decides which instruments, sample points and equipment the pilot plant needs.</p>
<h2>How large should the pilot be?</h2>
<p>The pilot should be large enough to show the effects of scale and small enough to change cheaply. The step that is safe to take depends on what is in the process.</p>
<p class="oee-cap">Table 2. Typical size of one scale-up step</p>
<table>
<tr><th>Type of operation</th><th class="num">Typical step in volume</th><th>Why</th></tr>
<tr><td>Single-phase liquid or gas reactions with known kinetics</td><td class="num">100 to 1,000 times</td><td>Behaviour can be calculated with confidence</td></tr>
<tr><td>Liquid reactions limited by mixing or heat removal</td><td class="num">50 to 100 times</td><td>Results depend on vessel geometry</td></tr>
<tr><td>Gas-liquid and liquid-liquid reactions</td><td class="num">20 to 100 times</td><td>Contact area between the phases is hard to predict</td></tr>
<tr><td>Solids: crystallization, filtration, drying</td><td class="num">10 to 50 times</td><td>Particle size and cake behaviour change with scale</td></tr>
</table>
<p>These ranges are a guide and vary with how well the process is understood. In the example, each step is 100 times: 1&nbsp;L to 100&nbsp;L, then 100&nbsp;L to 10,000&nbsp;L. If the product had to be crystallized and filtered, that part of the process would justify a smaller step or a separate test on vendor equipment.</p>
<h2>Run until the results repeat</h2>
<p>One good run shows that the process can work. A design needs to know how it works on an ordinary day. That takes consecutive runs under the same conditions, with every input and output weighed.</p>
{fig(fig_yield(), 2, f"Illustrative yield in ten consecutive pilot runs. The design uses the mean, {YMEAN:.0f}%, and the range shows the variation the plant must tolerate.")}
<p>In the example, ten consecutive runs gave yields between {min(YIELDS)}% and {max(YIELDS)}%, with a mean of {YMEAN:.1f}%. The commercial design in {K3} uses {YMEAN:.0f}%. Using the best run, {max(YIELDS)}%, would understate raw material use and waste for every year of operation.</p>
<h2>What to have before you shut the pilot down</h2>
<p class="oee-cap">Table 3. Data to collect before the pilot campaign ends</p>
<table>
<tr><th>Data</th><th>Test of completeness</th></tr>
<tr><td>Mass balance</td><td>Everything in and out weighed. Totals agree within about 2%.</td></tr>
<tr><td>Energy balance</td><td>Heat of reaction and heat transfer coefficient measured on the pilot reactor</td></tr>
<tr><td>Yield and quality</td><td>At least five consecutive runs at the design conditions, using commercial-grade raw materials</td></tr>
<tr><td>Operating limits</td><td>Runs at the edges of temperature, addition rate and concentration, showing where quality is lost</td></tr>
<tr><td>Recycle effects</td><td>Recycled solvent used for enough runs to show whether impurities level off</td></tr>
<tr><td>Separation data</td><td>Filtration, washing and drying rates measured on representative material</td></tr>
<tr><td>Materials</td><td>Corrosion rates from coupons exposed for the whole campaign</td></tr>
<tr><td>Waste and emissions</td><td>Each stream measured and analysed</td></tr>
<tr><td>Product samples</td><td>Enough material for customer approval</td></tr>
</table>
<p>The first two rows matter most. A pilot plant without flow meters, load cells and temperature measurements on the jacket cannot produce a mass or energy balance, however well it runs.</p>
<h2>Five common mistakes</h2>
<ul>
<li><strong>Building the pilot to make samples.</strong> It is designed around the product and has too few instruments to give design data.</li>
<li><strong>Using lab-grade raw materials.</strong> Trace impurities in commercial grades are a frequent cause of surprises at start-up.</li>
<li><strong>Stopping after the first good run.</strong> The design is then based on the best result.</li>
<li><strong>Running once through with fresh solvent.</strong> The plant will recycle, and impurities that build up never appear in the pilot.</li>
<li><strong>Keeping no record of problems.</strong> Blockages, foaming and cleaning difficulties are design information and should be logged like any other result.</li>
</ul>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> List the questions before designing the pilot plant, instrument it to close a mass and energy balance, and run it until the results repeat. In the example, ten runs give a design yield of {YMEAN:.0f}%.</p></div>
<div class="oee-next"><a href="{U1}.html">← Post&nbsp;1: what changes when you scale up</a><a class="oee-fwd" href="{U3}.html">Next: Post&nbsp;3, the mass and energy balance →</a></div>
{NOTE}"""


# ───────────────────────── Part 3 ─────────────────────────
BATCH = dict(A=3000, B=2750, S=4250, P=5000, W=750, SR=4000, SW=250)       # kg per commercial batch
NB = 1000                                                                   # batches a year
PRICE = dict(A=2.00, B=1.50, S=1.20, waste=0.30, steam=0.04)               # $/kg
CP, LAT_STEAM, LAT_SOLV = 2.0, 2133, 400                                   # kJ/kg.K, kJ/kg, kJ/kg
Q_RXN = (BATCH["A"] + BATCH["B"] + BATCH["S"]) * DH                        # kJ
Q_HEAT = 10000 * CP * 40
Q_DIST = BATCH["SR"] * LAT_SOLV
STEAM = (Q_HEAT + Q_DIST) / LAT_STEAM                                      # kg per batch
COST = [("Raw material A", BATCH["A"] / BATCH["P"] * PRICE["A"], BLUE), ("Raw material B", BATCH["B"] / BATCH["P"] * PRICE["B"], "#7FB2CF"),
        ("Solvent make-up", BATCH["SW"] / BATCH["P"] * PRICE["S"], PURPLE), ("Waste disposal", (BATCH["W"] + BATCH["SW"]) / BATCH["P"] * PRICE["waste"], ORANGE),
        ("Steam", STEAM / BATCH["P"] * PRICE["steam"], RED)]
CTOT = sum(c for _, c, _ in COST)


def fig_bfd():
    s = DEFS
    s += box(190, 70, 150, 80, ["Reactor", "10 m³ batch"], fs=13.5)
    s += box(440, 70, 150, 80, ["Separation and", "solvent recovery"], fs=13.5)
    for y, lab in ((84, f"Raw material A: {BATCH['A']:,} kg"), (110, f"Raw material B: {BATCH['B']:,} kg"), (136, f"Fresh solvent: {BATCH['SW']:,} kg")):
        s += arrow(160, y, 188, y, w=1.8) + txt(152, y + 4.5, lab, "end", NAVY, 12.5)
    s += arrow(340, 110, 438, 110, w=2) + txt(389, 100, "10,000 kg", "middle", MUTED, 12)
    s += arrow(590, 92, 640, 92, w=2, col=NAVY) + txt(648, 96.5, f"Product: {BATCH['P']:,} kg", fill=GREEND, fs=13, bold=True)
    s += arrow(590, 130, 640, 130, w=1.8) + txt(648, 134.5, f"Waste: {BATCH['W'] + BATCH['SW']:,} kg", fill=NAVY, fs=12.5)
    s += f'<path d="M515,70 V40 Q515,30 505,30 H275 Q265,30 265,40 V56" fill="none" stroke="{BLUE}" stroke-width="1.8"/>'
    s += f'<path d="M259.5,59 L270.5,59 L265,69 z" fill="{BLUE}"/>' + txt(390, 22, f"Recovered solvent recycled: {BATCH['SR']:,} kg", "middle", BLUE, 12.5, True)
    s += txt(265, 176, f"In: {BATCH['A'] + BATCH['B'] + BATCH['SW']:,} kg", "middle", MUTED, 12.5) + txt(650, 176, f"Out: {BATCH['P'] + BATCH['W'] + BATCH['SW']:,} kg", "start", MUTED, 12.5)
    return svg(f"Block flow diagram for one batch. Raw material A {BATCH['A']:,} kilograms, raw material B {BATCH['B']:,} and fresh solvent {BATCH['SW']} enter the reactor, "
               f"with {BATCH['SR']:,} kilograms of recycled solvent. Separation gives {BATCH['P']:,} kilograms of product and {BATCH['W'] + BATCH['SW']:,} of waste. "
               "Total in and total out are both 6,000 kilograms.", 812, 188, s, 640, x0=-22)


def fig_cost():
    s = ""; x = 0.0
    for n, c, col in COST:
        w = c / CTOT * 700
        s += f'<rect x="{x:.1f}" y="14" width="{max(w, 1.5):.1f}" height="46" fill="{col}"/>'
        if w > 60: s += txt(x + w / 2, 42, f"${c:.2f}", "middle", "#fff", 13, True)
        x += w
    for i, (n, c, col) in enumerate(COST):
        cx = (i % 2) * 350; cy = 90 + (i // 2) * 26
        s += f'<rect x="{cx}" y="{cy - 11}" width="12" height="12" rx="2" fill="{col}"/>' + txt(cx + 20, cy, f"{n}: ${c:.3f} per kg ({c / CTOT * 100:.1f}%)", fill=NAVY, fs=12.5)
    return svg("Stacked bar of variable cost per kilogram of product: " + ", ".join(f"{n.lower()} ${c:.3f}" for n, c, _ in COST) + f". Total ${CTOT:.2f}.", 700, 158, s)


def post_s3():
    b = BATCH; rm = (COST[0][1] + COST[1][1]) * b["P"] * NB
    mrows = [("Raw material A", "in", 30.0, b["A"]), ("Raw material B", "in", 27.5, b["B"]), ("Solvent, fresh", "in", 2.5, b["SW"]), ("Solvent, recycled", "in", 40.0, b["SR"])]
    orow = [("Product", 50.0, b["P"]), ("Waste: by-products and unreacted material", 7.5, b["W"]), ("Waste: solvent losses", 2.5, b["SW"]), ("Solvent recovered for recycle", 40.0, b["SR"])]
    tin = "".join(f'<tr><td>{n}</td><td class="num">{p:.1f} kg</td><td class="num">{c:,} kg</td><td class="num">{c * NB / 1000:,.0f} t/y</td></tr>' for n, _, p, c in mrows)
    tout = "".join(f'<tr><td>{n}</td><td class="num">{p:.1f} kg</td><td class="num">{c:,} kg</td><td class="num">{c * NB / 1000:,.0f} t/y</td></tr>' for n, p, c in orow)
    crow = "".join(f'<tr><td><span class="oee-sw" style="background:{col}"></span>{n}</td><td class="num">${c:.3f}</td><td class="num">${c * b["P"] * NB:,.0f}</td><td class="num">{c / CTOT * 100:.1f}%</td></tr>' for n, c, col in COST)
    return f"""{CSS}<p>The mass and energy balance is the first engineering document of a commercial design. It states how much of everything goes in and comes out, and how much heat must be added and removed. Equipment sizes, utility demand and operating cost are all calculated from it.</p>
<p>{K1} showed why the commercial reactor needs a longer addition time than the lab. {K2} covered the pilot campaign and its design yield of {YMEAN:.0f}%. This post turns those results into a balance for a plant making 5,000&nbsp;tonnes of product a year.</p>
<h2>Step 1: set the basis</h2>
<p>A balance needs a stated basis. For a batch process the natural basis is one batch.</p>
<p class="oee-cap">Table 1. Basis for the commercial balance</p>
<table>
<tr><th>Item</th><th>Value</th><th>Source</th></tr>
<tr><td>Annual production</td><td class="nw">5,000 t/y of product</td><td>Business plan</td></tr>
<tr><td>Operating time</td><td class="nw">8,000 h/y</td><td>Design basis</td></tr>
<tr><td>Batch cycle time</td><td class="nw">8 hours</td><td>Charge 1 h, addition 3 h, hold 2 h, transfer 1 h, clean 1 h</td></tr>
<tr><td>Batches a year</td><td class="nw">1,000</td><td>8,000 h ÷ 8 h</td></tr>
<tr><td>Product per batch</td><td class="nw">5,000 kg</td><td>5,000 t ÷ 1,000 batches</td></tr>
<tr><td>Yield</td><td class="nw">{YMEAN:.0f}%</td><td>Mean of ten pilot runs</td></tr>
</table>
<p>The three-hour addition comes from {K1}: the 10,000&nbsp;L reactor needs at least 2.7 hours to remove the heat of reaction. A one-hour addition would have given a six-hour cycle and a smaller reactor, and the jacket could not have kept up.</p>
<h2>Step 2: scale the pilot mass balance</h2>
<p>The pilot runs used 100&nbsp;kg batches. Each quantity is scaled by the ratio of product required, 5,000&nbsp;kg ÷ 50&nbsp;kg = 100.</p>
<p class="oee-cap">Table 2. Mass balance: pilot batch, commercial batch and annual totals</p>
<table>
<tr><th>Stream</th><th class="num">Pilot batch</th><th class="num">Commercial batch</th><th class="num">Annual</th></tr>
{tin}
<tr class="oee-total"><td>Total in</td><td class="num">100.0 kg</td><td class="num">10,000 kg</td><td class="num">10,000 t/y</td></tr>
{tout}
<tr class="oee-total"><td>Total out</td><td class="num">100.0 kg</td><td class="num">10,000 kg</td><td class="num">10,000 t/y</td></tr>
</table>
<p>The check on yield: raw materials A and B together are {b['A'] + b['B']:,}&nbsp;kg, and {b['P']:,}&nbsp;kg becomes product. That is {b['P'] / (b['A'] + b['B']) * 100:.0f}%, which matches the pilot result. The totals in and out agree, so the balance closes.</p>
{fig(fig_bfd(), 1, "Block flow diagram for one commercial batch. Recycled solvent circulates inside the plant, so only the fresh solvent crosses the boundary.")}
<p>Two results stand out. The reactor must hold a 10,000&nbsp;kg batch, about 10&nbsp;m³, so the vessel needs roughly 12.5&nbsp;m³ of total volume at 80% fill. And the plant produces {(b['W'] + b['SW']) * NB / 1000:,.0f}&nbsp;t/y of waste, one tonne for every five tonnes of product, which sets the size of the waste handling system and the permit application.</p>
<h2>Step 3: add the energy balance</h2>
<p>Each heating or cooling step is calculated from the masses in Table 2 and the properties measured in the pilot plant.</p>
<p class="oee-cap">Table 3. Energy balance for one batch</p>
<table>
<tr><th>Step</th><th>Calculation</th><th class="num">Heat</th><th>Utility</th></tr>
<tr><td>Heat the batch from 20°C to 60°C</td><td>10,000 kg × {CP:.1f} kJ/kg·K × 40 K</td><td class="num">{Q_HEAT / 1e6:.1f} GJ</td><td class="nw">{Q_HEAT / LAT_STEAM:,.0f} kg of steam</td></tr>
<tr><td>Remove the heat of reaction</td><td>10,000 kg × {DH} kJ/kg</td><td class="num">{Q_RXN / 1e6:.1f} GJ</td><td>Cooling water on the jacket</td></tr>
<tr><td>Evaporate the solvent for recovery</td><td>{b['SR']:,} kg × {LAT_SOLV} kJ/kg</td><td class="num">{Q_DIST / 1e6:.1f} GJ</td><td class="nw">{Q_DIST / LAT_STEAM:,.0f} kg of steam</td></tr>
<tr><td>Condense the recovered solvent</td><td>Same heat, removed</td><td class="num">{Q_DIST / 1e6:.1f} GJ</td><td>Cooling water on the condenser</td></tr>
<tr class="oee-total"><td>Total per batch</td><td></td><td class="num"></td><td>{STEAM:,.0f} kg of steam, {(Q_RXN + Q_DIST) / 1e6:.1f} GJ of cooling</td></tr>
</table>
<p>Utilities are sized for the peak, which is higher than the average. The reaction heat of {Q_RXN / 1e6:.1f}&nbsp;GJ leaves over the three-hour addition, an average of {Q_RXN / 3 / 3600:.0f}&nbsp;kW. The jacket can remove {geom(10)[3] * 10:.0f}&nbsp;kW, so it has about 10% in hand. That margin is thin, and it is the kind of result a design review should question.</p>
<h2>Step 4: read the operating cost from the balance</h2>
<p>With prices for each stream, the balance gives the variable cost of production. The prices below are illustrative.</p>
{fig(fig_cost(), 2, f"Variable cost per kilogram of product, ${CTOT:.2f} in total. Raw materials are {(COST[0][1] + COST[1][1]) / CTOT * 100:.0f}% of it.")}
<p class="oee-cap">Table 4. Variable cost from the mass and energy balance</p>
<table>
<tr><th>Cost element</th><th class="num">Per kg of product</th><th class="num">Annual</th><th class="num">Share</th></tr>
{crow}
<tr class="oee-total"><td>Total variable cost</td><td class="num">${CTOT:.3f}</td><td class="num">${CTOT * b['P'] * NB:,.0f}</td><td class="num">100%</td></tr>
</table>
<p>Raw materials cost ${rm / 1e6:.1f}M a year. Yield therefore matters more than any utility saving. One more point of yield, from {YD}% to {YD + 1}%, would cut raw material use by 1.1% and save about ${round(rm * (1 - YD / (YD + 1)), -3):,.0f} a year. Halving the steam bill would save about ${COST[4][1] * b['P'] * NB / 2:,.0f}.</p>
<h2>What the balance hands to the next stage</h2>
<p class="oee-cap">Table 5. Where each result goes</p>
<table>
<tr><th>Result from the balance</th><th>Used for</th></tr>
<tr><td>Batch size and cycle time</td><td>Reactor volume and the number of reactors</td></tr>
<tr><td>Raw material and product quantities</td><td>Storage tanks, deliveries and shipping</td></tr>
<tr><td>Heat loads and their timing</td><td>Jacket area, condenser, boiler and cooling water system</td></tr>
<tr><td>Recycle and waste streams</td><td>Solvent recovery equipment, waste treatment and permits</td></tr>
<tr><td>Consumption per kilogram of product</td><td>Operating cost estimate and the business case</td></tr>
</table>
<p>These figures become the design basis and the heat and material balance for front-end engineering. The FEED series picks up from here, starting with <a href="{FEED2}.html">the design basis</a>.</p>
<p>To practise balance calculations, try the free <a href="../mass-momentum-energy-exam.html">Mass, Momentum &amp; Energy Exam</a>.</p>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> Scale the pilot balance to the commercial batch, check that it closes, then add the energy balance and prices. In the example, a {YMEAN:.0f}% yield and a three-hour addition lead to a 10&nbsp;m³ batch, {(b['W'] + b['SW']) * NB / 1000:,.0f}&nbsp;t/y of waste and a variable cost of ${CTOT:.2f} per kilogram.</p></div>
<div class="oee-next oee-end"><a href="{U1}.html">← Post&nbsp;1: what changes when you scale up</a><a href="{U2}.html">← Post&nbsp;2: what a pilot plant is for</a></div>
{NOTE}"""


# ───────────────────────── How to read a PFD and a P&ID ─────────────────────────
def drawing(n, f, w, h, alt, cap):
    src = f"../assets/media/pfd-pid/{f}"
    return (f'<figure>\n<a href="{src}" target="_blank" rel="noopener"><img src="{src}" alt="{alt}" width="{w}" height="{h}" '
            f'style="width:100%;height:auto;border-radius:0;border:1px solid var(--line-2)"></a>\n'
            f'<figcaption>Figure {n}. {cap} Select the drawing to open it full size.</figcaption>\n</figure>')


def post_pfd():
    return f"""{CSS}<p>Two drawings come up in almost every review of a process plant: the process flow diagram (PFD) and the piping and instrumentation diagram (P&amp;ID). Owners, investors and operations managers are asked to comment on both, often without having been shown how to read them.</p>
<p>This guide reads one small example on both drawings: a section that heats a feed liquid with steam before it enters a reactor. The same heater appears on the PFD and on the P&amp;ID, so you can see what each drawing adds.</p>
<h2>The two drawings in one sentence each</h2>
<ul>
<li><strong>A PFD shows how the process works.</strong> It has the main equipment, the main streams and their flows, temperatures and pressures.</li>
<li><strong>A P&amp;ID shows how the plant is built and controlled.</strong> It has every pipe, valve and instrument, and the control loops that connect them.</li>
</ul>
<h2>Reading the PFD</h2>
{drawing(1, "feed-heating-pfd.svg", 860, 770, "Process flow diagram of a feed heating section. Feed from storage enters feed tank T-101, feed pump P-101 sends it through steam heater E-101, and it leaves for reactor R-101. Low pressure steam enters the heater and condensate leaves. A stream table lists flow, temperature and pressure for five numbered streams.", "Example PFD of a feed heating section, with its stream table.")}
<p>Read a PFD in four steps.</p>
<ol>
<li><strong>Follow the main flow.</strong> It normally runs left to right. Here the feed enters tank T-101, pump P-101 raises its pressure, heater E-101 warms it, and it leaves for reactor R-101.</li>
<li><strong>Identify the equipment.</strong> Each item has a tag. The letter gives the type and the number identifies the item.</li>
<li><strong>Look up each stream.</strong> The numbers in diamonds refer to columns in the stream table.</li>
<li><strong>Check that it balances.</strong> What goes into each item must come out.</li>
</ol>
<p class="oee-cap">Table 1. Common equipment tag letters</p>
<table>
<tr><th>Letter</th><th>Equipment</th><th>On the example</th></tr>
<tr><td class="nw">T or TK</td><td>Storage tank</td><td>T-101, feed tank</td></tr>
<tr><td class="nw">P</td><td>Pump</td><td>P-101, feed pump</td></tr>
<tr><td class="nw">E</td><td>Heat exchanger</td><td>E-101, feed heater</td></tr>
<tr><td class="nw">R</td><td>Reactor</td><td>R-101, on another sheet</td></tr>
<tr><td class="nw">V or D</td><td>Pressure vessel or drum</td><td>None</td></tr>
<tr><td class="nw">C</td><td>Column or compressor</td><td>None</td></tr>
</table>
<p>Letters vary between companies, so check the legend sheet that comes with the drawings.</p>
<h3>Using the stream table</h3>
<p>The stream table is where a PFD can be checked with a calculator. On the example:</p>
<ul>
<li><strong>Mass.</strong> The feed is 6,250&nbsp;kg/h in streams 1, 2 and 3. Nothing is added or lost. The steam in stream 4 equals the condensate in stream 5, at 350&nbsp;kg/h.</li>
<li><strong>Pressure.</strong> The pump raises the feed from 0 to 4.0&nbsp;barg. The heater takes 0.5&nbsp;bar of that, leaving 3.5&nbsp;barg to reach the reactor.</li>
<li><strong>Heat.</strong> The feed is heated from 20°C to 80°C. With a heat capacity of 2.0&nbsp;kJ/kg·K, that needs 6,250 × 2.0 × 60 = 750,000&nbsp;kJ/h, or 208&nbsp;kW. The steam supplies 350&nbsp;kg/h × 2,133&nbsp;kJ/kg = 746,550&nbsp;kJ/h, or 207&nbsp;kW. The two agree.</li>
</ul>
<p>If these checks fail on a real PFD, ask why before the drawing is used for anything else.</p>
<h3>What the PFD leaves out</h3>
<p>The PFD has no valves, no instruments and no pipe sizes. It does not show how the outlet temperature is held at 80°C or what happens if it rises. Those answers are on the P&amp;ID.</p>
<h2>Reading the P&amp;ID</h2>
{drawing(2, "feed-heater-pid.svg", 860, 665, "Piping and instrumentation diagram of feed heater E-101. The process line has an isolation valve on each side of the heater, a temperature transmitter TT-101 and a relief valve PSV-102 on the outlet. Controller TIC-101 receives the temperature signal and positions steam control valve TV-101, which fails closed. The steam line has pressure gauge PI-201, and condensate leaves through steam trap ST-201. Each line carries a line number.", "Example P&amp;ID of the same heater, E-101.")}
<p>The heater is the same item as on the PFD. The P&amp;ID adds everything needed to build, operate and maintain it.</p>
<p class="oee-cap">Table 2. Symbols on the example P&amp;ID</p>
<table>
<tr><th>Symbol</th><th>Tag on the example</th><th>What it is</th></tr>
<tr><td>Circle</td><td class="nw">PI-201, TT-101</td><td>An instrument mounted in the field, on or near the pipe</td></tr>
<tr><td>Circle inside a square</td><td class="nw">TIC-101</td><td>A function in the control system, seen on the control room screens</td></tr>
<tr><td>Two triangles, point to point</td><td>Not tagged</td><td>A manual valve, used here to isolate the heater</td></tr>
<tr><td>Two triangles with an actuator on top</td><td class="nw">TV-101</td><td>A control valve, positioned by a signal</td></tr>
<tr><td>Angled valve with a spring</td><td class="nw">PSV-102</td><td>A pressure relief valve, which opens by itself at its set pressure</td></tr>
<tr><td>Square with a diagonal</td><td class="nw">ST-201</td><td>A steam trap, which lets condensate out and holds steam in</td></tr>
<tr><td>Solid line</td><td class="nw">DN50-P-1003</td><td>A pipe</td></tr>
<tr><td>Dashed line with an arrow</td><td>None</td><td>An instrument signal, pointing to the device that receives it</td></tr>
</table>
<h3>Reading an instrument tag</h3>
<p>Instrument tags follow the ISA-5.1 standard. The first letter is what is measured. The letters after it say what the device does. The number identifies the loop.</p>
<p class="oee-cap">Table 3. Instrument tag letters used on the example</p>
<table>
<tr><th>Tag</th><th>First letter</th><th>Following letters</th><th>Meaning</th></tr>
<tr><td class="nw">TT-101</td><td>T, temperature</td><td>T, transmitter</td><td>Measures temperature and sends it to the control system</td></tr>
<tr><td class="nw">TIC-101</td><td>T, temperature</td><td>I, indicator; C, controller</td><td>Displays the temperature and controls it</td></tr>
<tr><td class="nw">TV-101</td><td>T, temperature</td><td>V, valve</td><td>The valve that the temperature loop moves</td></tr>
<tr><td class="nw">PI-201</td><td>P, pressure</td><td>I, indicator</td><td>A pressure gauge read at the pipe</td></tr>
<tr><td class="nw">PSV-102</td><td>P, pressure</td><td>S, safety; V, valve</td><td>A pressure relief valve</td></tr>
</table>
<p>Other common first letters are F for flow and L for level. Everything with the number 101 belongs to one control loop.</p>
<h3>Tracing a control loop</h3>
<p>A control loop has three parts: a measurement, a controller and a final element. Follow the dashed lines and their arrows.</p>
<ol>
<li><strong>TT-101</strong> measures the temperature of the feed leaving the heater.</li>
<li><strong>TIC-101</strong> compares it with the set point of 80°C.</li>
<li><strong>TV-101</strong> opens to admit more steam if the feed is too cold and closes if it is too hot.</li>
</ol>
<p>The note "FC" beside the valve means fail closed. If instrument air or the signal is lost, the valve shuts and the steam stops. For a heater that is the safe direction. Every control valve should show its failure position, and each one is worth asking about in a review.</p>
<h3>Reading a line number</h3>
<p>Each pipe has a line number that links the drawing to the line list and the piping specification.</p>
<p class="oee-cap">Table 4. The parts of line number DN50-P-1003</p>
<table>
<tr><th>Part</th><th>Meaning</th><th>Other examples on the drawing</th></tr>
<tr><td class="nw">DN50</td><td>Nominal pipe size, 50 mm (2 inch)</td><td>DN40 steam, DN25 condensate</td></tr>
<tr><td class="nw">P</td><td>Service: process</td><td>LS, low pressure steam; C, condensate</td></tr>
<tr><td class="nw">1003</td><td>Sequence number of the line</td><td>1004 after the heater</td></tr>
</table>
<p>The number changes from 1003 to 1004 across the heater because the fluid conditions change. Full line numbers often add a piping class and an insulation code. Formats differ between companies.</p>
<h2>Five questions to ask in a P&amp;ID review</h2>
<p>You do not need to be an engineer to ask useful questions. On the example:</p>
<ol>
<li><strong>Can this equipment be isolated for maintenance?</strong> Yes on the process side, with a manual valve on each side of the heater.</li>
<li><strong>What protects it from overpressure?</strong> PSV-102. If both manual valves are shut with steam on, the trapped liquid heats and expands, and the relief valve opens at 6.0&nbsp;barg.</li>
<li><strong>Where does the relief go?</strong> The drawing says "to safe location". Ask where that is.</li>
<li><strong>What happens on loss of air or power?</strong> TV-101 fails closed and heating stops.</li>
<li><strong>How does the operator know something is wrong?</strong> TIC-101 shows the temperature in the control room. This drawing has no high temperature alarm, which is a fair point to raise.</li>
</ol>
<h2>Side by side</h2>
<p class="oee-cap">Table 5. What each drawing shows for the same heater</p>
<table>
<tr><th>Item</th><th>PFD</th><th>P&amp;ID</th></tr>
<tr><td>Heater E-101</td><td>Shown, with duty</td><td>Shown</td></tr>
<tr><td>Flows, temperatures, pressures</td><td>Stream table</td><td>Key values only</td></tr>
<tr><td>Pipe sizes and line numbers</td><td>Not shown</td><td>Every line</td></tr>
<tr><td>Manual valves</td><td>Not shown</td><td>Shown</td></tr>
<tr><td>Control loop</td><td>Not shown</td><td>TT-101, TIC-101, TV-101</td></tr>
<tr><td>Relief valve and steam trap</td><td>Not shown</td><td>PSV-102, ST-201</td></tr>
</table>
<p>The example is simplified for teaching. A real P&amp;ID of this heater would also show drains, vents, a bypass around the control valve and insulation. For where these drawings fit in a project, see <a href="{FEED3}.html">What a FEED Package Contains</a>.</p>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> Use the PFD to check that the process balances, and the P&amp;ID to check that the plant can be operated, maintained and kept safe. On both, start by following one line from end to end.</p></div>
<p class="oee-note"><em>The drawings are illustrative examples and are not for construction. Symbols and tag formats vary between companies and standards.</em></p>"""


ARTICLES = [
    dict(slug=U1, title="Lab to Pilot to Commercial: What Changes When You Scale Up", cats=["process-engineering", "operational-efficiency"],
         desc="Why a reaction that works in a flask can overheat in a plant reactor. Surface area, heat removal and mixing at three scales, with a calculator.",
         tags=["scale-up", "heat transfer", "jacketed reactor", "exothermic reaction", "mixing", "process design"], body=nowrap(post_s1(), [(2, 0, 30), (2, 1, 26)]), related=[U2, U3, FEED1],
         series=dict(name="Scale-up series", part=1, of=3)),
    dict(slug=U2, title="What a Pilot Plant Is For: The Questions It Must Answer", cats=["process-engineering", "project-management"],
         desc="A pilot plant exists to produce design data. Eight questions it should answer, how large to build it, and what to collect before shutting it down.",
         tags=["pilot plant", "scale-up", "process development", "mass balance", "design data"], body=nowrap(post_s2(), [(3, 0, 22)]), related=[U1, U3, FEED1],
         series=dict(name="Scale-up series", part=2, of=3)),
    dict(slug=U3, title="From Pilot Data to a Mass and Energy Balance", cats=["process-engineering", "operational-efficiency"],
         desc="A worked example that scales a 100 kg pilot batch to a 5,000 t/y plant: mass balance, energy balance, utility loads and variable cost per kilogram.",
         tags=["mass balance", "energy balance", "scale-up", "operating cost", "yield", "process design"], body=nowrap(post_s3(), [(3, 1, 34)]), related=[U1, U2, FEED2],
         series=dict(name="Scale-up series", part=3, of=3)),
    dict(slug=PF, title="How to Read a PFD and a P&ID: A Guide for Owners and Managers", cats=["process-engineering", "project-management"],
         desc="A worked example of one heater on both drawings: equipment tags, stream tables, instrument symbols, control loops, line numbers and review questions.",
         tags=["PFD", "P&ID", "ISA-5.1", "instrument tags", "control loop", "process drawings"], body=nowrap(post_pfd(), [(2, 1, 22), (3, 1, 22), (3, 2, 30)]), related=[FEED3, FEED1, U3]),
]

if __name__ == "__main__":
    for a in ARTICLES:
        words = len(re.sub(r"<svg.*?</svg>|<script.*?</script>|<[^>]+>", " ", a["body"], flags=re.S).split())
        assert len(a["desc"]) <= 165, (a["slug"], len(a["desc"]))
        a.update(date="2026-11-11", author="Quak Foo Lee", read=f"{max(1, round(words / 220))} min read", cover_label="Process Engineering")
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"], words, "words,", a["read"])
