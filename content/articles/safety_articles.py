"""Process safety series for Insights (Process Engineering): three articles.

Part 1  What happens if the cooling fails: runaway reactions and MTSR (calculator: assets/js/runaway.js)
Part 2  A worked HAZOP of the feed heater (drawings: assets/media/pfd-pid/feed-heater-hazop-nodes.svg, feed-heater-pid-revc.svg)
Part 3  Management of change for small plants

Usage:  python3 content/articles/safety_articles.py
Writes content/articles/<slug>.json for each article. Then build each page with
        python3 content/gen/add_article.py <slug>
and run python3 content/gen/series_labels.py so the cards show the series label.
The worked examples reuse the scale-up series reactor and the feed heater from the PFD and P&ID article.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import (nowrap, svg, fig, box, txt, arrow, DEFS, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, RED,
                           MUTED, LINE, SAND, PALE, GREENF, ORANGEF)
from process_eng_articles import geom, drawing, U1 as SCALE1, U3 as SCALE3, PF as PFDPID

P1 = "what-happens-if-the-cooling-fails-runaway-reactions"
P2 = "a-worked-hazop-the-feed-heater-node-by-node"
P3 = "management-of-change-for-small-plants"
L1 = f'<a href="{P1}.html">Post&nbsp;1</a>'
L2 = f'<a href="{P2}.html">Post&nbsp;2</a>'
L3 = f'<a href="{P3}.html">Post&nbsp;3</a>'
NOTE = ('<p class="oee-note"><em>The reaction, temperatures and equipment in this series are an illustrative example. '
        'The calculations are screening estimates. They do not replace calorimetry testing, a formal hazard study '
        'or a design by a qualified engineer.</em></p>')
EXAM = ('<a href="https://quakfoolee-dotcom.github.io/exam-library/process-chemeng/Process_Engineering_Reactor_Design_150Q_V2.html" '
        'target="_blank" rel="noopener">Reactor Design Exam</a>')

# ───────────────────────── example data, shared with the scale-up series ─────────────────────────
DH, CP, TP, MTT, TD24, ACC = 150, 2.0, 60, 110, 150, 20          # kJ/kg, kJ/kg.K, C, C, C, %
DTAD = DH / CP                                                     # 75 K
MTSR_BATCH = TP + DTAD                                             # 135 C
MTSR_SEMI = TP + ACC / 100 * DTAD                                  # 75 C
ACC_LIMIT = (MTT - TP) / DTAD * 100                                # accumulation at which MTSR reaches MTT, 67%
JACKET = geom(10)[3] * 10                                          # kW for the 10 m3 reactor, 154
QRXN_GJ = 10000 * DH / 1e6                                         # 1.5 GJ per batch


def klass(mtsr, mtt=MTT, td=TD24):
    if mtsr <= td:
        if mtsr <= mtt: return 1 if td >= mtt else 2
        return 3
    return 4 if mtt < td else 5


# ───────────────────────── Part 1 figures ─────────────────────────
def fig_ladder():
    Y = lambda t: 250 - (t - 40) * 1.6; s = DEFS
    for t in range(40, 181, 20):
        s += f'<line x1="70" y1="{Y(t)}" x2="690" y2="{Y(t)}" stroke="{LINE}"/>' + txt(62, Y(t) + 4, f"{t} °C", "end", MUTED, 12)
    for t, lab, col in ((TD24, f"TD24, decomposition: {TD24} °C", PURPLE), (MTT, f"Boiling point (MTT): {MTT} °C", BLUE)):
        s += f'<line x1="70" y1="{Y(t)}" x2="690" y2="{Y(t)}" stroke="{col}" stroke-width="2" stroke-dasharray="7 4"/>' + txt(686, Y(t) - 7, lab, "end", col, 12.5, True)
    for x, mt, lab, sub, col in ((190, MTSR_BATCH, "All reactant charged at once", "100% accumulated", RED),
                                 (440, MTSR_SEMI, "Added over 3 hours", f"{ACC}% accumulated at most", GREEND)):
        s += f'<rect x="{x - 36}" y="{Y(mt)}" width="72" height="{Y(TP) - Y(mt)}" rx="5" fill="{col}" opacity=".85"/>'
        s += f'<line x1="{x - 50}" y1="{Y(TP)}" x2="{x + 50}" y2="{Y(TP)}" stroke="{NAVY}" stroke-width="2.4"/>'
        s += txt(x + 46, Y(mt) + 5, f"MTSR {mt:.0f} °C", fill=col, fs=13, bold=True)
        s += txt(x, 272, lab, "middle", NAVY, 12.5, True) + txt(x, 289, sub, "middle", MUTED, 12)
    s += txt(612, Y(TP) + 5, f"Process {TP} °C", "end", NAVY, 12.5, True)
    return svg(f"Two bars rising from the process temperature of {TP} °C. With all reactant charged at once the batch could reach {MTSR_BATCH:.0f} °C, "
               f"above the boiling point of {MTT} °C but below the decomposition temperature of {TD24} °C. With the reactant added over three hours "
               f"and at most {ACC}% accumulated, it could reach only {MTSR_SEMI:.0f} °C.", 694, 298, s, x0=0)


def fig_acc():
    X = lambda a: 80 + a * 6; Y = lambda t: 240 - (t - 40) * 1.6; s = ""
    for t in range(40, 161, 20):
        s += f'<line x1="80" y1="{Y(t)}" x2="680" y2="{Y(t)}" stroke="{LINE}"/>' + txt(72, Y(t) + 4, f"{t} °C", "end", MUTED, 12)
    for a in range(0, 101, 20):
        s += txt(X(a), 262, f"{a}%", "middle", MUTED, 12)
    s += txt(380, 282, "Unreacted reactant in the reactor when cooling fails (accumulation)", "middle", MUTED, 12.5)
    s += f'<rect x="{X(ACC_LIMIT):.1f}" y="{Y(TD24)}" width="{X(100) - X(ACC_LIMIT):.1f}" height="{Y(MTT) - Y(TD24)}" fill="{RED}" opacity=".08"/>'
    for t, lab, col in ((TD24, f"TD24 {TD24} °C", PURPLE), (MTT, f"Boiling point {MTT} °C", BLUE)):
        s += f'<line x1="80" y1="{Y(t)}" x2="680" y2="{Y(t)}" stroke="{col}" stroke-width="2" stroke-dasharray="7 4"/>' + txt(86, Y(t) - 7, lab, fill=col, fs=12.5, bold=True)
    s += f'<line x1="{X(0)}" y1="{Y(TP)}" x2="{X(100)}" y2="{Y(MTSR_BATCH)}" stroke="{NAVY}" stroke-width="3"/>'
    s += f'<circle cx="{X(ACC)}" cy="{Y(MTSR_SEMI)}" r="6" fill="{GREEND}"/>' + txt(X(ACC) + 10, Y(MTSR_SEMI) + 18, f"Normal operation: {ACC}%, {MTSR_SEMI:.0f} °C", fill=GREEND, fs=12.5, bold=True)
    s += f'<circle cx="{X(ACC_LIMIT):.1f}" cy="{Y(MTT)}" r="6" fill="{RED}"/>' + txt(X(ACC_LIMIT) + 10, Y(MTT) + 20, f"Boiling reached at {ACC_LIMIT:.0f}%", fill=RED, fs=12.5, bold=True)
    s += txt(X(100) - 4, Y(MTSR_BATCH) - 10, f"{MTSR_BATCH:.0f} °C", "end", NAVY, 12.5, True)
    return svg(f"Line chart of MTSR against accumulation. MTSR rises in a straight line from {TP} °C at 0% to {MTSR_BATCH:.0f} °C at 100%. "
               f"Normal operation, at {ACC}%, gives {MTSR_SEMI:.0f} °C. The batch reaches its boiling point of {MTT} °C at {ACC_LIMIT:.0f}% accumulation.", 692, 290, s, x0=10)


def post1():
    acc_rows = "".join(f'<tr><td class="num">{a}%</td><td class="num">{TP + a / 100 * DTAD:.0f} °C</td><td class="num">Class {klass(TP + a / 100 * DTAD)}</td><td>{w}</td></tr>'
                       for a, w in ((0, "Reactant consumed as fast as it is added"), (ACC, "Normal operation, measured in calorimetry"),
                                    (40, "Feed slightly too cold"), (60, "Reaction slowed, for example by low temperature or weak catalyst"),
                                    (80, "Reaction barely running while feed continues"), (100, "Reaction never started; all reactant added")))
    cls_rows = "".join(f'<tr><td class="nw">Class {n}</td><td class="nw">{o}</td><td>{m}</td></tr>' for n, o, m in (
        (1, "MTSR &lt; MTT &lt; TD24", "Neither boiling nor decomposition is reached. Avoid holding the batch hot for long."),
        (2, "MTSR &lt; TD24 &lt; MTT", "Boiling is not reached, but decomposition starts below the boiling point. Avoid long holds."),
        (3, "MTT &lt; MTSR &lt; TD24", "The batch boils before it can decompose. Condenser and vent must handle boiling at full rate."),
        (4, "MTT &lt; TD24 &lt; MTSR", "Boiling comes first, but decomposition can follow. Evaporative cooling must be proven."),
        (5, "TD24 &lt; MTT, TD24 &lt; MTSR", "Decomposition starts before boiling. Boiling gives no protection. Change the process.")))
    return f"""{CSS}<p>Every exothermic reactor is designed to remove its heat of reaction. The safety question is what happens when that stops: a pump trips, a cooling water valve sticks, or the power fails. The answer depends on how much heat is still to come and how hot it can make the batch.</p>
<p>This series uses examples from earlier posts. This part takes the 10,000&nbsp;L reactor from the <a href="{SCALE1}.html">scale-up series</a>. {L2} runs a HAZOP on the feed heater from <a href="{PFDPID}.html">How to Read a PFD and a P&amp;ID</a>, and {L3} shows how a small change can undo both.</p>
<h2>Four temperatures decide the outcome</h2>
<p>A cooling failure assessment compares four temperatures. The method is widely used in the fine chemical and pharmaceutical industries and was set out by Francis Stoessel.</p>
<p class="oee-cap">Table 1. The four temperatures in a cooling failure assessment</p>
<table>
<tr><th>Temperature</th><th>Meaning</th><th class="num">Example</th></tr>
<tr><td class="nw">Process temperature</td><td>The normal operating temperature of the batch</td><td class="num">{TP} °C</td></tr>
<tr><td class="nw">MTSR</td><td>Maximum temperature of the synthesis reaction: how hot the batch gets if cooling stops and the remaining reactant reacts</td><td class="num">Calculated below</td></tr>
<tr><td class="nw">MTT</td><td>Maximum temperature for technical reasons. For a reactor open to a condenser, this is the boiling point of the batch</td><td class="num">{MTT} °C</td></tr>
<tr><td class="nw">TD24</td><td>The temperature at which a decomposition, with no cooling, would take 24 hours to reach its maximum rate. Measured by thermal stability tests</td><td class="num">{TD24} °C</td></tr>
</table>
<p>The first is set by the process. MTT comes from the equipment and the solvent. TD24 comes from laboratory tests on the reaction mixture. MTSR is calculated.</p>
<h2>Step 1: the adiabatic temperature rise</h2>
<p>If no heat leaves the reactor, all the heat of reaction goes into warming the batch. The rise in temperature is:</p>
<p class="oee-formula">ΔT<sub>ad</sub> = heat of reaction ÷ heat capacity = {DH} kJ/kg ÷ {CP:.1f} kJ/kg·K = {DTAD:.0f} K</p>
<p>The reaction and heat capacity are the ones used in the scale-up series. If the whole reaction could still happen after the cooling fails, the batch would climb {DTAD:.0f}&nbsp;K above its starting temperature.</p>
<h2>Step 2: how much reaction is still to come</h2>
<p>In the plant the reactant is added over three hours, so at any moment only part of it is in the reactor unreacted. That unreacted part is called the accumulation. Only the accumulated reactant can still release heat if the feed stops when the cooling fails.</p>
<p class="oee-formula">MTSR = process temperature + accumulation × ΔT<sub>ad</sub></p>
<p>Reaction calorimetry measures the accumulation during the addition. In the example the highest value is {ACC}%:</p>
<p class="oee-formula">MTSR = {TP} °C + {ACC / 100:.2f} × {DTAD:.0f} K = {MTSR_SEMI:.0f} °C</p>
{fig(fig_ladder(), 1, f"The same reaction run two ways. Adding the reactant over three hours keeps the possible temperature rise to {MTSR_SEMI - TP:.0f}&nbsp;K.")}
<p>Had all the reactant been charged at once, as in a simple lab procedure, the accumulation would be 100% and the MTSR {MTSR_BATCH:.0f}&nbsp;°C. The batch would reach its boiling point.</p>
<h2>Step 3: place the result in a criticality class</h2>
<p>The order of the four temperatures gives a criticality class from 1 to 5.</p>
<p class="oee-cap">Table 2. Criticality classes for a cooling failure</p>
<table>
<tr><th>Class</th><th>Order of temperatures</th><th>What it means</th></tr>
{cls_rows}
</table>
<p>With the three-hour addition, the example is Class&nbsp;{klass(MTSR_SEMI)}: {MTSR_SEMI:.0f}&nbsp;°C is well below both the boiling point and TD24. Charged all at once it would be Class&nbsp;{klass(MTSR_BATCH)}. The batch would boil, and the condenser and vent would have to cope with the remaining third of the reaction heat, about 0.5&nbsp;GJ, boiling off around 1,250&nbsp;kg of solvent.</p>
<h2>Accumulation is the number to protect</h2>
<p>The semi-batch result holds only while the reaction keeps up with the feed. If the reaction slows and the feed carries on, unreacted material builds up and the MTSR rises with it.</p>
{fig(fig_acc(), 2, f"MTSR rises with accumulation. Above {ACC_LIMIT:.0f}% the batch could reach its boiling point after a cooling failure.")}
<p class="oee-cap">Table 3. MTSR for different accumulations in the example</p>
<table>
<tr><th class="num">Accumulation</th><th class="num">MTSR</th><th class="num">Class</th><th>When it could happen</th></tr>
{acc_rows}
</table>
<p>The common causes of high accumulation are a feed that is too cold, a reaction that has not started, a missing or weak catalyst, and poor mixing. That gives three practical rules for the plant:</p>
<ul>
<li><strong>Stop the feed when cooling is lost.</strong> An interlock on cooling water flow or reactor temperature that stops the feed pump caps the accumulation at its current value.</li>
<li><strong>Confirm the reaction has started before adding at full rate.</strong> A small first portion, followed by a check that heat is being released, shows the reaction is running.</li>
<li><strong>Do not add reactant below the minimum temperature.</strong> A cold batch reacts slowly while the feed continues. The HAZOP in {L2} finds exactly this case on the feed heater.</li>
</ul>
<div class="oee-calc" role="group" aria-labelledby="rwh">
<h3 id="rwh">Try it: cooling failure at your conditions</h3>
<p class="oee-hint">Set the reaction data and the three limiting temperatures. The calculator gives the MTSR and the criticality class.</p>
<div class="oee-sliders">
<div class="oee-sl"><label for="rw-H">Heat of reaction, per kg of batch <output id="rw-H-o"></output></label><input type="range" id="rw-H" min="20" max="600" step="5" value="{DH}"></div>
<div class="oee-sl"><label for="rw-cp">Heat capacity of the batch <output id="rw-cp-o"></output></label><input type="range" id="rw-cp" min="1.2" max="4.2" step="0.1" value="{CP}"></div>
<div class="oee-sl"><label for="rw-Tp">Process temperature <output id="rw-Tp-o"></output></label><input type="range" id="rw-Tp" min="0" max="150" step="1" value="{TP}"></div>
<div class="oee-sl"><label for="rw-acc">Maximum accumulation <output id="rw-acc-o"></output></label><input type="range" id="rw-acc" min="0" max="100" step="1" value="{ACC}"></div>
<div class="oee-sl"><label for="rw-MTT">Boiling point of the batch (MTT) <output id="rw-MTT-o"></output></label><input type="range" id="rw-MTT" min="40" max="250" step="1" value="{MTT}"></div>
<div class="oee-sl"><label for="rw-TD">Decomposition temperature (TD24) <output id="rw-TD-o"></output></label><input type="range" id="rw-TD" min="40" max="300" step="1" value="{TD24}"></div>
</div>
<div class="oee-tiles">
<div class="oee-tile"><span class="k">Adiabatic temperature rise</span><span class="v" id="rw-ad"></span></div>
<div class="oee-tile"><span class="k">MTSR</span><span class="v" id="rw-mtsr"></span></div>
<div class="oee-tile"><span class="k">MTSR against boiling point</span><span class="v" id="rw-gap"></span></div>
<div class="oee-tile key"><span class="k">Criticality</span><span class="v" id="rw-cls"></span></div>
</div>
<p class="oee-hint" id="rw-msg"></p>
<p class="oee-hint" id="rw-warn" style="color:#B43E3E"></p>
<figure>
<div class="oee-chart" id="rw-chart"></div>
<figcaption>Figure 3. The four temperatures for your inputs. The coloured bar shows how far the batch could heat up after a cooling failure.</figcaption>
</figure>
</div>
<h2>What this assessment does not cover</h2>
<ul>
<li><strong>Gas generation.</strong> A reaction or decomposition that releases gas can pressurise the reactor well below the temperatures above. Gas release must be measured separately.</li>
<li><strong>Relief sizing.</strong> A Class&nbsp;3 or 4 result means the vent must be sized for boiling or two-phase flow. That is a specialist calculation.</li>
<li><strong>The data.</strong> Heat of reaction, accumulation and TD24 come from calorimetry and thermal stability tests on the actual mixture. Literature values are a starting point only.</li>
</ul>
<p>To practise the underlying calculations, try the free {EXAM}.</p>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> Calculate how hot the batch could get if cooling fails, and compare it with the boiling point and the decomposition temperature. In the example, a three-hour addition with {ACC}% accumulation keeps the MTSR at {MTSR_SEMI:.0f}&nbsp;°C. Charging everything at once would give {MTSR_BATCH:.0f}&nbsp;°C.</p></div>
<div class="oee-next"><a class="oee-fwd" href="{P2}.html">Next: Post&nbsp;2, a worked HAZOP →</a></div>
<noscript><p class="oee-note">The calculator on this page needs JavaScript. The tables show the worked example.</p></noscript>
{NOTE}
<script src="../assets/js/runaway.js" defer></script>"""


# ───────────────────────── Part 2 ─────────────────────────
def fig_method():
    s = DEFS
    steps = [["1. Choose a", "node"], ["2. Apply a", "guide word"], ["3. Find causes", "and consequences"], ["4. List the", "safeguards"], ["5. Agree", "actions"]]
    for i, st in enumerate(steps):
        x = 10 + i * 146
        s += box(x, 40, 124, 64, st, fill=PALE if i < 4 else GREENF, stroke="#9AB0C8" if i < 4 else "#A9C77E", fs=12.5)
        if i < 4: s += arrow(x + 124, 72, x + 144, 72, w=1.8)
    s += f'<path d="M598,104 V128 Q598,138 588,138 H162 Q152,138 152,128 V114" fill="none" stroke="{NAVY}" stroke-width="1.4" stroke-dasharray="4 3"/>'
    s += f'<line x1="152" y1="118" x2="152" y2="114" stroke="{NAVY}" stroke-width="1.4"/><path d="M146.5,115 L157.5,115 L152,105 z" fill="{NAVY}"/>'
    s += txt(375, 158, "Next guide word, then the next node", "middle", MUTED, 12.5)
    return svg("Five steps in a row: choose a node, apply a guide word, find causes and consequences, list the safeguards, and agree actions. "
               "A dashed arrow loops back to the guide word step for the next guide word and node.", 716, 168, s, 600, x0=4)


WS1 = [("More steam flow", "TV-101 fails open; TT-101 reads low; TIC-101 left in manual",
        "Feed leaves hotter than 80 °C, up to steam temperature. Extra heat goes into R-101 and speeds the reaction.",
        "TIC-101 (but its failure is one of the causes)", "1"),
       ("Less or no steam flow", "TV-101 fails closed; steam trap ST-201 blocked and the shell floods; steam supply lost",
        "Feed reaches R-101 cold. The reaction slows while the feed continues, so reactant accumulates (see Post&nbsp;1).",
        "TIC-101 shows the temperature, but nothing alerts the operator", "2"),
       ("More steam pressure", "Steam header pressure regulator fails",
        "Shell side pressure above 3.0 barg. Overpressure if the shell is rated lower than the header.",
        "None shown on this drawing", "3"),
       ("Other than: tube leak", "Corrosion or fatigue of a tube",
        "Feed at 3.5 barg leaks into the shell at 3.0 barg and contaminates the condensate return.",
        "None", "4")]
WS2 = [("No flow", "P-101 stops, or both manual valves are closed while steam is on",
        "Liquid trapped in the tubes is heated, expands and can boil. Overpressure of the tubes and line.",
        "PSV-102, set at 6.0 barg", "5"),
       ("Reverse flow", "P-101 stops while R-101 is under pressure",
        "Reactor contents flow back through E-101 towards the feed tank, where they may react.",
        "None", "6"),
       ("More flow", "Feed pump speed raised; flow control on the reactor P&amp;ID fails",
        "Addition faster than three hours. Heat release exceeds jacket capacity (see Post&nbsp;1).",
        "Flow control on the reactor P&amp;ID (outside this node)", "7"),
       ("Less flow", "Partial blockage, pump wear",
        "TIC-101 reduces the steam to match. Addition takes longer, which is the safe direction.",
        "TIC-101", "None")]
ACTIONS = [("1", "Add an outlet temperature trip independent of loop 101: TT-103 and TSHH-103 close a new steam shutoff valve XV-103 at 95 °C", "Rev C drawing"),
           ("2", "Add high and low temperature alarms on TIC-101. The low alarm at 70 °C also stops reactant addition to R-101", "Rev C drawing"),
           ("3", "Confirm the shell design pressure is at least the maximum steam header pressure, or that the header has its own relief", "Check"),
           ("4", "Decide how a tube leak will be detected before condensate returns to the boiler", "Study"),
           ("5", "Confirm PSV-102 is sized for the blocked-in heating case, and define where it discharges", "Check"),
           ("6", "Add a check valve on line DN50-P-1004 against reverse flow from R-101", "Rev C drawing"),
           ("7", "Confirm the feed rate to R-101 has a high flow alarm or trip that keeps the addition at three hours or longer", "Reactor node")]


def post2():
    def ws(rows):
        return "".join(f'<tr><td>{d}</td><td>{c}</td><td>{q}</td><td>{s}</td><td class="num">{a}</td></tr>' for d, c, q, s, a in rows)
    head = '<tr><th>Deviation</th><th>Possible causes</th><th>Consequences</th><th>Existing safeguards</th><th class="num">Action</th></tr>'
    acts = "".join(f'<tr><td class="num">{n}</td><td>{t}</td><td class="nw">{r}</td></tr>' for n, t, r in ACTIONS)
    return f"""{CSS}<p>A HAZOP, short for hazard and operability study, is a structured way of asking what could go wrong with a design. A small team takes the P&amp;ID one section at a time and applies a fixed set of guide words to each. The method is described in the international standard IEC&nbsp;61882.</p>
<p>{L1} showed how hot a reactor could get if its cooling failed. This post runs a HAZOP on a smaller and simpler item: the steam-heated feed heater E-101 from <a href="{PFDPID}.html">How to Read a PFD and a P&amp;ID</a>. It heats the feed that goes to that reactor. {L3} covers what happens to the design after the study.</p>
<h2>How a HAZOP works</h2>
{fig(fig_method(), 1, "The HAZOP sequence. The team repeats steps 2 to 5 for every guide word, then moves to the next node.")}
<p>A <strong>node</strong> is a section of the drawing with one design intent, such as "supply steam to E-101". A <strong>deviation</strong> is a guide word combined with a process parameter.</p>
<p class="oee-cap">Table 1. Guide words and the deviations they produce</p>
<table>
<tr><th>Guide word</th><th>Meaning</th><th>Example deviations</th></tr>
<tr><td class="nw">No</td><td>None of the intent is achieved</td><td>No flow, no steam</td></tr>
<tr><td class="nw">More</td><td>A quantitative increase</td><td>More flow, more temperature, more pressure</td></tr>
<tr><td class="nw">Less</td><td>A quantitative decrease</td><td>Less flow, less temperature</td></tr>
<tr><td class="nw">Reverse</td><td>The opposite of the intent</td><td>Reverse flow</td></tr>
<tr><td class="nw">As well as</td><td>Something extra happens</td><td>Contamination, a second phase</td></tr>
<tr><td class="nw">Other than</td><td>Something different happens</td><td>A leak, a wrong material, start-up and shutdown</td></tr>
</table>
<p>The team needs at least a facilitator, a scribe, a process engineer, an experienced operator and an instrument or control engineer. A drawing the size of this one takes two to three hours.</p>
<h2>The nodes</h2>
{drawing(2, "feed-heater-hazop-nodes.svg", 860, 665, "The Rev B feed heater P&amp;ID with two HAZOP nodes highlighted. Node 1, in orange, is the steam supply through TV-101 into the shell and the condensate leaving through steam trap ST-201. Node 2, in green, is the feed through the heater tubes to the reactor, including relief valve PSV-102.", "The feed heater P&amp;ID divided into two nodes.")}
<ul>
<li><strong>Node 1: steam supply and condensate.</strong> Intent: supply 350&nbsp;kg/h of steam at 3.0&nbsp;barg to heat the feed to 80&nbsp;°C, and return the condensate.</li>
<li><strong>Node 2: feed through the heater.</strong> Intent: pass 6,250&nbsp;kg/h of feed from P-101 through the tubes to reactor R-101.</li>
</ul>
<h2>Node 1: steam supply and condensate</h2>
<p class="oee-cap">Table 2. HAZOP worksheet, node 1</p>
<table>
{head}
{ws(WS1)}
</table>
<p>The first row shows the most common finding in a HAZOP. The control loop that could cause the deviation is listed as the safeguard against it. If TT-101 fails reading low, TIC-101 opens the steam valve, so TIC-101 cannot also be what protects against overheating. A safeguard must be independent of the cause.</p>
<p>The second row connects to {L1}. A heater fault that looks harmless, a cold feed, slows the reaction in R-101 while the feed carries on. Reactant accumulates, and the MTSR rises with it.</p>
<h2>Node 2: feed through the heater</h2>
<p class="oee-cap">Table 3. HAZOP worksheet, node 2</p>
<table>
{head}
{ws(WS2)}
</table>
<p>Not every deviation needs an action. Less flow is handled by the existing control loop and moves the process in the safe direction, so the team records it and moves on.</p>
<h2>The actions</h2>
<p class="oee-cap">Table 4. Action list</p>
<table>
<tr><th class="num">No.</th><th>Action</th><th>Result</th></tr>
{acts}
</table>
<p>Each action gets a named owner and a due date. Three of them change the drawing. The others are checks that may change it later, and action 7 belongs to the reactor node.</p>
{drawing(3, "feed-heater-pid-revc.svg", 1000, 770, "The feed heater P&amp;ID at Rev C. New items are marked with a revision triangle: steam shutoff valve XV-103, temperature transmitter TT-103 and trip TSHH-103, high and low temperature alarms on TIC-101, and a check valve on the outlet line.", "The P&amp;ID after the HAZOP, Rev C. New items carry a revision triangle.")}
<h2>Five rules for a useful HAZOP</h2>
<ul>
<li><strong>Use a current, complete P&amp;ID.</strong> The study is only as good as the drawing. Freeze it before the meeting.</li>
<li><strong>Record causes, not just deviations.</strong> "More temperature" is not a finding. "TV-101 fails open" is.</li>
<li><strong>Test every safeguard for independence.</strong> A device that fails along with the cause does not count.</li>
<li><strong>Write actions the owner can close.</strong> "Review the heater" cannot be closed. "Add an independent high temperature trip" can.</li>
<li><strong>Close the actions before start-up.</strong> An open HAZOP action at start-up is an accepted risk. Someone should sign for it.</li>
</ul>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> Work through the drawing node by node, and check that each safeguard is independent of the cause. On the feed heater, two hours of review produced seven actions, three of them changes to the P&amp;ID.</p></div>
<div class="oee-next"><a href="{P1}.html">← Post&nbsp;1: runaway reactions</a><a class="oee-fwd" href="{P3}.html">Next: Post&nbsp;3, management of change →</a></div>
{NOTE}"""


# ───────────────────────── Part 3 ─────────────────────────
ADD = [(2.0, "Proposed"), (2.5, ""), (3.0, "Current design")]


def fig_moc():
    s = DEFS
    s += txt(4, 18, "Every change goes through the screen. Only changes that are not like for like go on to the review.", fill=MUTED, fs=12.5)
    s += box(10, 40, 130, 56, ["Change", "requested"], fill=SAND, stroke=LINE, fs=12.5)
    s += arrow(140, 68, 168, 68, w=1.8)
    s += f'<path d="M230,32 L292,68 L230,104 L168,68 Z" fill="#ffffff" stroke="{NAVY}" stroke-width="1.6"/>'
    s += txt(230, 64, "Replacement", "middle", NAVY, 12, True) + txt(230, 79, "in kind?", "middle", NAVY, 12, True)
    s += arrow(292, 68, 338, 68, w=1.6) + txt(315, 60, "Yes", "middle", MUTED, 12)
    s += box(340, 44, 150, 48, ["Normal work order"], fill=SAND, stroke=LINE, fs=12.5, bold=False)
    s += f'<path d="M230,104 V122 Q230,130 222,130 H78 Q70,130 70,138 V146" fill="none" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#ah)"/>'
    s += txt(240, 120, "No", fill=MUTED, fs=12)
    labels = [["Hazard review", "scaled to risk"], ["Approve"], ["Implement"], ["Update drawings,", "procedures, training"], ["Pre-start-up", "check, then close"]]
    for i, l in enumerate(labels):
        x = 10 + i * 140; last = i == len(labels) - 1
        s += box(x, 148, 122, 58, l, fill=GREENF if last else PALE, stroke="#A9C77E" if last else "#9AB0C8", fs=12.5)
        if not last: s += arrow(x + 122, 177, x + 138, 177, w=1.8)
    return svg("Management of change flow. A change request goes to a screen: if it is a replacement in kind it becomes a normal work order. "
               "Otherwise it goes through a hazard review scaled to risk, approval, implementation, updates to drawings, procedures and training, "
               "and a pre-start-up check before it is closed.", 700, 214, s, 600, x0=2)


def fig_heat():
    s = ""; X0, X1 = 150, 700; Xv = lambda kw: X0 + kw / 250 * (X1 - X0)
    for kw in (0, 50, 100, 150, 200, 250):
        s += f'<line x1="{Xv(kw)}" y1="20" x2="{Xv(kw)}" y2="170" stroke="{LINE}"/>' + txt(Xv(kw), 188, f"{kw} kW", "middle", MUTED, 12)
    for i, (h, lab) in enumerate(ADD):
        q = QRXN_GJ * 1e6 / (h * 3600); y = 34 + i * 46; ok = q <= JACKET
        s += f'<rect x="{X0}" y="{y}" width="{Xv(q) - X0:.1f}" height="28" rx="4" fill="{GREEND if ok else RED}" opacity=".85"/>'
        s += txt(X0 - 10, y + 13, f"{h:g} h addition", "end", NAVY, 12.5, True) + (txt(X0 - 10, y + 28, lab, "end", MUTED, 11.5) if lab else "")
        if ok and Xv(q) + 70 > Xv(JACKET):   # label would sit on the jacket line: put it inside the bar
            s += txt(Xv(q) - 8, y + 19, f"{q:.0f} kW", "end", "#fff", 12.5, True)
        else:
            s += txt(Xv(q) + 8, y + 19, f"{q:.0f} kW", fill=NAVY, fs=12.5, bold=True)
    s += f'<line x1="{Xv(JACKET):.1f}" y1="16" x2="{Xv(JACKET):.1f}" y2="172" stroke="{ORANGE}" stroke-width="2.4" stroke-dasharray="7 4"/>'
    s += txt(Xv(JACKET) + 6, 14, f"Jacket can remove {JACKET:.0f} kW", fill=ORANGE, fs=12.5, bold=True)
    return svg(f"Bar chart of the average heat release during the addition: {QRXN_GJ * 1e6 / 7200:.0f} kilowatts for a two hour addition, "
               f"{QRXN_GJ * 1e6 / 9000:.0f} for two and a half hours and {QRXN_GJ * 1e6 / 10800:.0f} for three hours, against a jacket capacity of {JACKET:.0f} kilowatts. "
               "Only the three hour addition is within the jacket capacity.", 716, 196, s, x0=10)


def post3():
    cyc_new = 7; nb_new = 8000 / cyc_new
    return f"""{CSS}<p>Most process incidents do not start with a bad design. They start with a good design that was changed. A faster addition to gain capacity, a cheaper solvent, a temporary pipe to keep running during a repair: each looks small, and each can remove a safeguard that someone added for a reason.</p>
<p>Management of change, or MOC, is the procedure that catches this. Before a change is made, someone who understands the design checks what it affects. MOC is an element of process safety management standards, including CSA&nbsp;Z767 in Canada and the OSHA process safety management rule in the United States.</p>
<p>{L1} and {L2} built up the safeguards on one reactor and its feed heater. This post shows how quickly a change could undo them, and how a small plant can run MOC without a large safety department.</p>
<h2>What counts as a change</h2>
<p>The key test is whether the replacement is <strong>in kind</strong>: identical to what it replaces, or a different item that meets the same specification. A replacement in kind needs no MOC. Everything else does.</p>
<p class="oee-cap">Table 1. Change or replacement in kind?</p>
<table>
<tr><th>Situation</th><th>Needs MOC?</th><th>Why</th></tr>
<tr><td>Gasket replaced with the same specification</td><td class="nw">No</td><td>Replacement in kind</td></tr>
<tr><td>Pump replaced with the same model</td><td class="nw">No</td><td>Replacement in kind</td></tr>
<tr><td>Pump replaced with a larger model</td><td class="nw">Yes</td><td>Higher flow can exceed what the reactor can cool</td></tr>
<tr><td>Addition time shortened</td><td class="nw">Yes</td><td>Changes the heat release rate and the accumulation</td></tr>
<tr><td>Solvent from a new supplier, same specification</td><td class="nw">Usually no</td><td>Check the specification covers the properties that matter</td></tr>
<tr><td>Different solvent</td><td class="nw">Yes</td><td>Changes the boiling point, MTT in Post&nbsp;1</td></tr>
<tr><td>Alarm or trip set point changed</td><td class="nw">Yes</td><td>The safeguard no longer acts where the HAZOP assumed</td></tr>
<tr><td>Trip bypassed to keep running</td><td class="nw">Yes</td><td>Removes a safeguard, even if only for a shift</td></tr>
<tr><td>Temporary hose or pipe</td><td class="nw">Yes</td><td>Temporary changes need the same review, plus an end date</td></tr>
</table>
<h2>Worked example 1: a faster addition</h2>
<p>The plant from the <a href="{SCALE3}.html">scale-up series</a> runs 1,000 batches a year on an eight-hour cycle that includes a three-hour addition. Sales want more product. Cutting the addition to two hours shortens the cycle to {cyc_new} hours and gives about {nb_new:,.0f} batches a year, {(nb_new / 1000 - 1) * 100:.0f}% more output without new equipment.</p>
<p>The MOC review starts from the design numbers. The reaction releases {QRXN_GJ:.1f}&nbsp;GJ per batch. Spread over the addition time, that gives the average heat the jacket must remove.</p>
{fig(fig_heat(), 1, f"Average heat release during the addition against the jacket capacity of {JACKET:.0f}&nbsp;kW. The two-hour addition exceeds it.")}
<p class="oee-cap">Table 2. What the review finds for a two-hour addition</p>
<table>
<tr><th>Check</th><th>Three hours (current)</th><th>Two hours (proposed)</th><th>Source</th></tr>
<tr><td>Average heat release</td><td class="nw">{QRXN_GJ * 1e6 / 10800:.0f} kW</td><td class="nw">{QRXN_GJ * 1e6 / 7200:.0f} kW</td><td>{QRXN_GJ:.1f} GJ over the addition time</td></tr>
<tr><td>Jacket capacity</td><td class="nw">{JACKET:.0f} kW</td><td class="nw">{JACKET:.0f} kW</td><td><a href="{SCALE1}.html">Scale-up Part 1</a></td></tr>
<tr><td>Temperature control</td><td>Holds 60 °C</td><td>Batch temperature rises</td><td>Heat release above capacity</td></tr>
<tr><td>Accumulation</td><td class="nw">{ACC}%</td><td>Higher; needs new calorimetry</td><td>Faster feed, same reaction rate</td></tr>
<tr><td>High flow trip (HAZOP action 7)</td><td>Set for three hours</td><td>Would have to be raised</td><td>Removes a safeguard</td></tr>
</table>
<p>The change is not safe as proposed. The review does not have to end with a refusal, though. It can point to options that are: a larger cooling capacity, a lower coolant temperature, or a second reactor. Each of those is a change with its own MOC.</p>
<h2>Worked example 2: a cheaper solvent</h2>
<p>Purchasing finds a solvent that does the same job at a lower price, but it boils at 95&nbsp;°C instead of {MTT}&nbsp;°C. The process chemistry is unchanged.</p>
<p>In {L1}, the boiling point is MTT. At normal accumulation the MTSR is {MTSR_SEMI:.0f}&nbsp;°C, still below 95&nbsp;°C. But the margin to boiling falls from {MTT - MTSR_SEMI:.0f}&nbsp;K to {95 - MTSR_SEMI:.0f}&nbsp;K, and the accumulation at which a cooling failure would reach boiling drops from {ACC_LIMIT:.0f}% to {(95 - TP) / DTAD * 100:.0f}%. A cold-feed event, the case found in {L2}, now reaches boiling sooner. The condenser, the vent and the solvent recovery design all assumed the old boiling point.</p>
<p>Nothing in this change looks like engineering, which is why it is easy to miss. That is the case for routing purchasing changes to raw materials through the MOC screen.</p>
<h2>The MOC procedure</h2>
{fig(fig_moc(), 2, "A management of change procedure. The screen sends like-for-like work straight to maintenance, and the review is scaled to the risk of the change.")}
<p>A small plant does not need a HAZOP for every change. Scale the review to the risk.</p>
<p class="oee-cap">Table 3. Review level by type of change</p>
<table>
<tr><th>Type of change</th><th>Example</th><th>Review</th></tr>
<tr><td>Low risk</td><td>A new instrument of a different make with the same range and function</td><td>Checklist, signed by the process engineer</td></tr>
<tr><td>Medium risk</td><td>New alarm set point, different raw material supplier</td><td>"What if" review with an engineer and an operator</td></tr>
<tr><td>High risk</td><td>Faster addition, new solvent, bypass of a trip</td><td>HAZOP of the affected nodes, approved by the plant manager</td></tr>
</table>
<h2>A one-page MOC form</h2>
<p class="oee-cap">Table 4. Fields on a one-page MOC form</p>
<table>
<tr><th>Field</th><th>What to record</th></tr>
<tr><td>Description</td><td>What will change, where, and why</td></tr>
<tr><td>Permanent or temporary</td><td>For a temporary change, the date it must be removed</td></tr>
<tr><td>Screen result</td><td>Replacement in kind, or the risk level for review</td></tr>
<tr><td>Effects checked</td><td>Process conditions, safeguards, relief, materials, operating procedures, environment</td></tr>
<tr><td>Review and findings</td><td>Who reviewed it, the method used and the actions</td></tr>
<tr><td>Approval</td><td>Name, role and date</td></tr>
<tr><td>Documents to update</td><td>P&amp;IDs, procedures, alarm and trip lists, training records</td></tr>
<tr><td>Pre-start-up check</td><td>Installed as approved, people trained, documents updated</td></tr>
<tr><td>Closed</td><td>Name and date</td></tr>
</table>
<h2>Five ways MOC fails in practice</h2>
<ul>
<li><strong>Temporary becomes permanent.</strong> A temporary change has no end date, so it is never reviewed again.</li>
<li><strong>Small changes add up.</strong> Each change passes on its own, and together they remove the margin. Review the history of the unit, not only the latest request.</li>
<li><strong>Drawings fall behind.</strong> The plant no longer matches the P&amp;ID, and the next HAZOP studies a plant that does not exist.</li>
<li><strong>Purchasing and staffing changes skip the screen.</strong> A new supplier or a reduced crew can change the hazard as much as new pipework.</li>
<li><strong>The operators are not told.</strong> A change is only complete when the people running the plant know what is different.</li>
</ul>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> Screen every change, and scale the review to the risk. In the example, a two-hour addition would add {(nb_new / 1000 - 1) * 100:.0f}% capacity but push the heat release to {QRXN_GJ * 1e6 / 7200:.0f}&nbsp;kW against a jacket that can remove {JACKET:.0f}&nbsp;kW.</p></div>
<div class="oee-next oee-end"><a href="{P1}.html">← Post&nbsp;1: runaway reactions</a><a href="{P2}.html">← Post&nbsp;2: a worked HAZOP</a></div>
{NOTE}"""


ARTICLES = [
    dict(slug=P1, title="What Happens If the Cooling Fails: Runaway Reactions and MTSR", cats=["process-engineering", "operational-efficiency"],
         desc="How hot a reactor can get when cooling stops. Adiabatic temperature rise, accumulation, MTSR and criticality classes, with a calculator.",
         tags=["process safety", "runaway reaction", "MTSR", "criticality class", "reaction calorimetry", "semi-batch"],
         body=nowrap(post1(), [(3, 3, 44)]), related=[P2, P3, SCALE1], series=dict(name="Process safety series", part=1, of=3)),
    dict(slug=P2, title="A Worked HAZOP: The Feed Heater, Node by Node", cats=["process-engineering", "operational-efficiency"],
         desc="A HAZOP of one steam heater: guide words, two nodes, the worksheets, seven actions, and the P&ID before and after the study.",
         tags=["HAZOP", "process safety", "P&ID", "IEC 61882", "safeguards", "hazard review"],
         body=nowrap(post2(), [(1, 2, 44)]), related=[P1, P3, PFDPID], series=dict(name="Process safety series", part=2, of=3)),
    dict(slug=P3, title="Management of Change for Small Plants", cats=["process-engineering", "operational-efficiency"],
         desc="How small changes undo a safe design, with two worked examples, a review scaled to risk and a one-page MOC form for small plants.",
         tags=["management of change", "MOC", "process safety", "CSA Z767", "HAZOP"],
         body=nowrap(post3(), [(1, 1, 12)]), related=[P1, P2, SCALE3], series=dict(name="Process safety series", part=3, of=3)),
]

if __name__ == "__main__":
    for a in ARTICLES:
        words = len(re.sub(r"<svg.*?</svg>|<script.*?</script>|<[^>]+>", " ", a["body"], flags=re.S).split())
        assert len(a["desc"]) <= 165, (a["slug"], len(a["desc"]))
        a.update(date="2026-11-12", author="Quak Foo Lee", read=f"{max(1, round(words / 220))} min read", cover_label="Process Engineering")
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"], words, "words,", a["read"])
