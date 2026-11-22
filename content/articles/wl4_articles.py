"""Warehouse layout series for Insights (V5.70). Part 4: feeding the filling lines.

The manufacturer's layout: Ridgeline Coatings (the fictional coatings maker of the ABC and safety stock posts) feeds two
filling lines from a central store, from a line-side supermarket, or by a kanban milk run. The Layout Lab
(assets/sim/layout-lab.html, opened with s=p4) runs them side by side; every number quoted here comes from
content/articles/wl4_results.json, written by wl4_model.js from the same engine (assets/js/wl-engine.js).

Usage:  node content/articles/wl4_model.js
        python3 content/articles/wl4_articles.py
        python3 content/gen/add_article.py central-store-supermarket-or-kanban-feeding-the-production-line
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, MUTED, LINE, eq, im, mathjs, tn

DATE = "2026-11-22"
WL1 = "good-layout-bad-layout-what-travel-and-congestion-cost-an-sme-warehouse"
WL2 = "u-shape-straight-through-or-l-shape-choosing-a-warehouse-flow-pattern"
WL3 = "wide-narrow-or-very-narrow-aisles-warehouse-density-against-access"
WL4 = "central-store-supermarket-or-kanban-feeding-the-production-line"
ABCM = "abc-analysis-for-manufacturers"
SSM = "safety-stock-for-manufacturers"
OEE1 = "what-oee-really-measures"
OEE2 = "what-oee-losses-cost"
SER = lambda n: {"name": "Warehouse layout series", "part": n, "of": 5}
SIM = "../assets/sim/layout-lab.html"
D = json.load(open(os.path.join(HERE, "wl4_results.json"), encoding="utf-8"))
K = D["kinds"]
B = {k: D["base"][k]["mfg"] for k in K}
St, Sd, Kb = (B[k] for k in K)
EC = D["econ"]; C = EC["C"]; OP = EC["opts"]; P = D["P"]
NAME = {"mstore": "Central store", "mside": "Line-side supermarket", "mkanban": "Kanban milk run"}
COLR = {"mstore": ORANGE, "mside": BLUE, "mkanban": GREEND}
NOTE = ('<p class="oee-note"><em>Ridgeline Coatings, its plant, materials, times and costs are an illustrative example built from stated assumptions, '
        'and the simulator is a simplified model. It shows how much the way materials reach a line can matter; it does not predict your plant\'s losses. '
        'Measure your own lines\' waiting time before you change anything.</em></p>')
f0 = lambda x: f"{x:,.0f}"
f1 = lambda x: f"{x:,.1f}"
money = lambda x: f"${round(x / 1000) * 1000:,.0f}"
money100 = lambda x: f"${round(x / 100) * 100:,.0f}"
GREY, WAITC = "#9AA8BA", "#E2574C"
def srng(k, key): v = [s[k]["mfg"][key] for s in D["seeds"]]; return min(v), max(v)


def fig_plan():
    """Plan of the plant: the fixed areas in grey and blue, the supermarket (the one area that changes) in amber."""
    k = 7.6; ox, oy = 20, 20
    X = lambda x: ox + x * k
    Y = lambda z: oy + z * k
    AMB, FIX, EQ = "#E0A12E", "#C9D3E0", "#7F93B2"
    s = f'<rect x="{X(0)}" y="{Y(0)}" width="{72 * k}" height="{52 * k}" fill="#FBFAF6" stroke="{NAVY}" stroke-width="2"/>'
    for a, b in [(1, 1), (5, 6), (10, 11), (15, 16), (20, 21), (25, 25)]:
        s += f'<rect x="{X(a)}" y="{Y(4)}" width="{(b - a + 1) * k}" height="{30 * k}" fill="{FIX}" stroke="#9AA8BA"/>'
    s += txt(X(13.5), Y(2.4), "Central store", "middle", NAVY, 12.5, True)
    for z0, n in ((6, "A"), (21, "B")):
        s += f'<circle cx="{X(38)}" cy="{Y(z0 + 2)}" r="{1.9 * k}" fill="#E4EAF3" stroke="{EQ}" stroke-width="2"/>'
        s += f'<rect x="{X(42)}" y="{Y(z0 + 1)}" width="{23 * k}" height="{2 * k}" fill="{EQ}"/>'
        s += txt(X(53.5), Y(z0 + 2) + 4.5, f"Filling line {n}", "middle", "#FFFFFF", 11.5, True)
    s += txt(X(38), Y(16.6), "Mixing", "middle", NAVY, 12, True)
    s += f'<rect x="{X(43)}" y="{Y(12)}" width="{19 * k}" height="{7 * k}" fill="{AMB}" fill-opacity="0.22" stroke="{AMB}" stroke-width="2" stroke-dasharray="6 4"/>'
    s += f'<rect x="{X(44)}" y="{Y(15)}" width="{17 * k}" height="{2 * k}" fill="{AMB}"/>'
    s += txt(X(52.5), Y(14.2), "Supermarket", "middle", "#8A5A00", 12, True)
    s += f'<rect x="{X(60)}" y="{Y(31)}" width="{7 * k}" height="{2 * k}" fill="{FIX}" stroke="#9AA8BA"/>'
    s += txt(X(63.5), Y(30.2), "Palletising", "middle", NAVY, 12, True)
    for x0, x1, t in ((3, 27, "Receiving staging"), (51, 69, "Shipping staging")):
        s += f'<rect x="{X(x0)}" y="{Y(41.5)}" width="{(x1 - x0) * k}" height="{6 * k}" fill="none" stroke="#9AA8BA" stroke-dasharray="4 3"/>'
        s += txt(X((x0 + x1) / 2), Y(49.6), t, "middle", MUTED, 12)
    for x in (8, 14, 20):
        s += f'<rect x="{X(x - 1.5)}" y="{Y(52) - 3}" width="{3 * k}" height="6" fill="{BLUE}"/>'
    for x in (56, 63):
        s += f'<rect x="{X(x - 1.5)}" y="{Y(52) - 3}" width="{3 * k}" height="6" fill="{GREEN}"/>'
    # callout: right-angle leader from the supermarket's right edge to the note, no arrowhead
    cx0, cy0 = X(62), Y(15.5); nx = X(72) + 14
    s += f'<polyline points="{cx0:.1f},{cy0:.1f} {nx - 6:.1f},{cy0:.1f}" fill="none" stroke="{AMB}" stroke-width="1.6"/>'
    for i, line in enumerate(["The only area that", "changes: none in", "the central-store", "set-up; a double", "rack in the other two"]):
        s += txt(nx, cy0 - 26 + i * 15, line, "start", "#8A5A00", 12, i == 0)
    return svg("Plan of Ridgeline Coatings' plant: the central store to the west, two mixing tanks and two filling lines to the east, palletising at the end of the lines, "
               "receiving and shipping staging along the south wall. The supermarket, a double rack between the two filling lines, is highlighted as the only area that changes between the set-ups.",
               740, int(52 * k + 44), s, 560)


def fig_lines():
    """Line minutes running and waiting for material, both lines, each set-up."""
    x0, y0, w, bh, gap = 190, 40, 420, 30, 22
    mx = St["planned"] * 2; X = lambda v: x0 + v / mx * w
    s = ""
    yb = y0 + 3 * (bh + gap) - gap
    for t in range(0, int(mx) + 1, 120):
        s += f'<line x1="{X(t):.1f}" y1="{y0 - 8}" x2="{X(t):.1f}" y2="{yb + 6}" stroke="#E4E1D8"/>' + txt(X(t), yb + 22, f0(t), "middle", MUTED, 12)
    s += txt(x0 + w / 2, yb + 42, "Line minutes in the shift (two lines, 960 in all)", "middle", NAVY, 12.5, True)
    for i, k in enumerate(K):
        y = y0 + i * (bh + gap); r = B[k]; run = r["lines"][0]["run"] + r["lines"][1]["run"]
        s += txt(x0 - 12, y + bh / 2 + 5, NAME[k], "end", NAVY, 13, True)
        s += f'<rect x="{x0}" y="{y}" width="{X(run) - x0:.1f}" height="{bh}" fill="{GREEN}"/>'
        if r["starved"] > 0.5:
            s += f'<rect x="{X(run):.1f}" y="{y}" width="{X(run + r["starved"]) - X(run):.1f}" height="{bh}" fill="{WAITC}"/>'
        s += txt(X(mx) + 8, y + bh / 2 + 5, f'{r["avail"] * 100:.0f}%', "start", NAVY, 13, True)
    lx = x0
    for lab, col in (("Running", GREEN), ("Waiting for material", WAITC)):
        s += f'<rect x="{lx}" y="10" width="12" height="12" rx="2" fill="{col}"/>' + txt(lx + 18, 21, lab, fill=NAVY, fs=12.5)
        lx += 18 + len(lab) * 7.2 + 18
    return svg("Bar chart of line minutes in the shift. " + ", ".join(f"{NAME[k]}: {f0(B[k]['starved'])} minutes waiting for material, availability {B[k]['avail'] * 100:.0f}%" for k in K) + ".",
               700, yb + 50, s, 560)


def fig_loop():
    """Kanban: line minutes lost against the milk-run interval, at standard speed."""
    Lp = D["loop"]; x0, y0, w, h = 70, 30, 560, 220
    xmax = Lp[-1]["loop"]; ymax = max(60, math.ceil(max(q["starved"] for q in Lp) / 60) * 60)
    X = lambda v: x0 + v / xmax * w
    Y = lambda m: y0 + h - m / ymax * h
    s = ""
    for t in range(0, ymax + 1, 60):
        s += f'<line x1="{x0}" y1="{Y(t):.1f}" x2="{x0 + w}" y2="{Y(t):.1f}" stroke="#E4E1D8"/>' + txt(x0 - 8, Y(t) + 4, str(t), "end", MUTED, 12)
    for q in Lp: s += txt(X(q["loop"]), y0 + h + 18, str(q["loop"]), "middle", MUTED, 12)
    s += txt(x0 + w / 2, y0 + h + 40, "Minutes between milk runs", "middle", NAVY, 12.5, True)
    s += f'<text x="20" y="{y0 + h / 2}" transform="rotate(-90 20 {y0 + h / 2})" text-anchor="middle" font-size="12.5" font-weight="600" fill="{NAVY}">Line minutes lost a shift</text>'
    s += f'<line x1="{X(40):.1f}" y1="{y0}" x2="{X(40):.1f}" y2="{y0 + h}" stroke="{ORANGE}" stroke-dasharray="5 4" stroke-width="1.5"/>'
    s += txt(X(40) - 6, y0 + 14, "One drum of resin lasts 40 min", "end", ORANGE, 12, True)
    pts = [(X(q["loop"]), Y(q["starved"])) for q in Lp]
    s += f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{GREEND}" stroke-width="2.6"/>'
    s += "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3.4" fill="{GREEND}"/>' for a, b in pts)
    return svg("Line chart: with the kanban milk run, no line minutes are lost for intervals of 10 to 40 minutes; at 50 minutes "
               f"{f0(Lp[4]['starved'])} minutes are lost and at 60 minutes {f0(Lp[5]['starved'])}, because a drum of resin lasts 40 minutes.", 700, 300, s, 560)


def part4():
    rows = [
        ("Line time lost waiting for material (both lines)", lambda r: f'{f0(r["starved"])}&nbsp;min'),
        ("Availability, counting material losses only", lambda r: f'{r["avail"] * 100:.1f}%'),
        ("Pails filled", lambda r: f0(r["made"])),
        ("Material deliveries to the lines", lambda r: f0(r["deliveries"])),
        ("Call or card to delivery (average)", lambda r: f'{f1(r["resp"])}&nbsp;min'),
        ("Material handler hours", lambda r: f1(r["handlerHours"])),
        ("Handler walking", lambda r: f'{f1(r["handlerKm"])}&nbsp;km'),
        ("Stock at the lines (average value)", lambda r: money100(r["lineStock"])),
        ("Stock in the supermarket (average value)", lambda r: money100(r["smStock"]) if r["smStock"] > 0 else "None"),
    ]
    trs = "".join(f'<tr><td>{lab}</td>' + "".join(f'<td class="num">{fn(B[k])}</td>' for k in K) + '</tr>' for lab, fn in rows)
    sp = {k: srng(k, "starved") for k in K}
    SP = D["speed"]; s2 = SP[-1]; s05 = SP[0]
    Lp = D["loop"]; okLoop = max(q["loop"] for q in Lp if q["starved"] < 1)
    lstore, lside, lkan = (OP[k] for k in K)
    dStock = Kb["lineStock"] - Sd["lineStock"]
    ot = lambda k: OP[k]["otYear"]
    hy = lambda k: OP[k]["handlerYear"]
    save_side = ot("mstore") - ot("mside") + hy("mstore") - hy("mside")
    save_kan = ot("mstore") - ot("mkanban") + hy("mstore") - hy("mkanban") - dStock * C["carry"]
    rack = lkan["rack"]
    STEP = {q["id"]: q for q in D["steps"]}
    STEPS = "".join(f'<tr><td>{q["t"]}</td><td class="num">{f0(q["starved"])}</td><td class="num">{f1(q["hh"])}</td></tr>' for q in D["steps"])
    LATE = [f0(q["late"]) for q in D["late"]]
    money_rows = [
        ("Line-hours lost a day (both lines)", lambda k: f1(OP[k]["lostHours"])),
        ("Overtime to make up the lost pails, a year", lambda k: money(ot(k))),
        ("Material handler time, a year (time freed, not cash unless reused)", lambda k: money(hy(k))),
        ("Extra stock at the lines against line-side, carrying cost a year", lambda k: money(dStock * C["carry"]) if k == "mkanban" else "–"),
        ("Supermarket racking, one-off", lambda k: f'{money(OP[k]["rack"][0])} to {money(OP[k]["rack"][1])}' if OP[k]["rack"][1] else "None"),
    ]
    mtrs = "".join(f'<tr><td>{lab}</td>' + "".join(f'<td class="num">{fn(k)}</td>' for k in K) + '</tr>' for lab, fn in money_rows)
    body = f"""{CSS}
<p>Parts <a href="{WL1}.html">1</a>, <a href="{WL2}.html">2</a> and <a href="{WL3}.html">3</a> laid out a distributor's warehouse. A manufacturer has a second customer inside the building: the production line. When a line runs out of a material, it stops, and every minute it waits is lost output. In OEE terms it is an availability loss (see <a href="{OEE1}.html">what OEE really measures</a>), and it often starts with the layout: where the materials are kept, and how they reach the line.</p>
<p>This part follows Ridgeline Coatings, the fictional Vancouver coatings maker from the <a href="{ABCM}.html">ABC analysis for manufacturers</a> post, through one shift with three ways of feeding its two filling lines.</p>
<h2>Three ways to feed a line</h2>
<p class="oee-cap">Table 1. The three set-ups</p>
<table>
<tr><th>Set-up</th><th>Where the materials wait</th><th>At the line</th><th>How a refill is triggered</th></tr>
<tr><td>Central store</td><td>In the central store with everything else, laid out by part number</td><td>One load of each material</td><td>The operator calls a material handler when a load runs out; the store issues the load</td></tr>
<tr><td>Line-side supermarket</td><td>A small rack between the lines, holding a few loads of each line material, topped up from the store by forklift</td><td>One load of each material</td><td>The same: called when a load runs out</td></tr>
<tr><td>Kanban milk run</td><td>The same supermarket</td><td>Two loads (two bins)</td><td>When the first load is used up, a card goes up; a handler on a fixed 20-minute loop delivers every carded load</td></tr>
</table>
<p>A supermarket, in lean terms, is a small store owned by production and placed next to the lines it serves, from which material handlers take what the lines use. The two-bin system needs no cards at all: the empty bin is the signal, and the second bin keeps the line running while the first is refilled. A milk run is a handler who follows a standard route on a fixed timetable, for example every 20 minutes, collecting the signals and delivering the materials.</p>
<h2>The plant</h2>
<p>The building is the 72 by 52&nbsp;m building of the earlier parts, with the same doors and staging. The west third is the central store: about 330 pallet faces, each with several levels above. In the east, two mixing tanks feed two filling lines, each filling {f0(P["mRate"])} pails a minute at standard speed. Each line uses five materials: resin and pigment at the mixer, and pails, lids and labels at the filler. One load (a drum of resin, a pallet of pails, a box of label rolls) lasts 40 to 150 minutes of running, and a line stops when any one of its five materials runs out.</p>
<ul>
<li><strong>Two material handlers</strong> walk at 0.9&nbsp;m/s with a pallet jack or cart: 20 seconds to start a job, 40 seconds to pick up a load, 30 seconds to set it down at the line. At the central store, booking the issue of a load adds 2 minutes.</li>
<li><strong>One forklift</strong> puts away inbound pallets (6 trucks a day) and, with a supermarket, brings 3 more loads from the store when a supermarket face is down to 2.</li>
<li><strong>Finished pails</strong> are palletised at the end of the lines (36 to a pallet) and taken to shipping by pallet jack; carriers collect every hour.</li>
</ul>
{fig(fig_plan(), 1, "Ridgeline's plant. Mixing, the filling lines, palletising and the central store are the same in all three set-ups; only the supermarket changes.")}
<p>Mixing and palletising are part of the plant in every set-up: the mixers use the resin and pigment, and palletising stacks the finished pails for shipping. They are drawn so you can follow the materials and the output, but the comparison is about one area, the supermarket between the lines, and about when a refill is asked for.</p>
<h2>The Layout Lab</h2>
<p>The simulator runs the three set-ups through the same shift. The supermarket area is shaded amber where it exists and outlined in dashes where it does not. Each line's outline turns red when it is waiting for material, and the loads waiting at each line are drawn next to it: one in the first two set-ups, two with kanban. Change the line speed to see how each set-up copes when the lines run faster or slower.</p>
<figure>
<iframe id="wl-sim" src="{SIM}#embed&amp;s=p4" title="Warehouse Layout Lab: two filling lines fed from a central store, a line-side supermarket and a kanban milk run, simulated side by side" loading="lazy" style="width:100%;height:3870px;border:0;display:block"></iframe>
<figcaption>Figure 2. The Warehouse Layout Lab with Ridgeline's three set-ups. The animation replays the shift 12 times faster than life; the table is the whole simulated shift.</figcaption>
</figure>
<p class="oee-hint"><a href="{SIM}?s=p4">Open the Layout Lab on its own page</a> for a larger view.</p>
<h2>What the simulation shows</h2>
<p class="oee-cap">Table 2. One shift at standard line speed</p>
<table>
<tr><th>Measure</th>{"".join(f'<th class="num">{NAME[k]}</th>' for k in K)}</tr>
{trs}
</table>
{fig(fig_lines(), 3, "Line minutes running and waiting for material. Only material losses are counted; breakdowns, changeovers and slow running would come on top.")}
<ul>
<li><strong>From the central store, the lines wait {f0(St["starved"])} minutes a shift</strong>, about a quarter of the time. Every run-out stops a line for the whole refill: the call, the walk to the store, the issue, the walk back. That takes {f1(St["resp"])} minutes on average, and it happens {f0(St["deliveries"])} times a shift across the two lines.</li>
<li><strong>A supermarket halves the waiting, but does not remove it.</strong> A refill takes {f1(Sd["resp"])} minutes and the lines wait {f0(Sd["starved"])} minutes. Most of the gain comes from skipping the store's issue booking and its part-number layout, not from the shorter walk (see the next section). The line still stops at every run-out, because nobody is asked for material until it has run out.</li>
<li><strong>Two bins and a milk run remove the waiting here.</strong> The card goes up when the first load is used up, so the line runs on the second load while the milk run comes round. This assumes steady use and cards seen as soon as they go up; see <a href="#sizing-the-milk-run">sizing the milk run</a>. Cards wait {f1(Kb["resp"])} minutes on average for delivery, and the lines never notice. Across ten other simulated days the lines waited {f0(sp["mstore"][0])} to {f0(sp["mstore"][1])} minutes with the central store, {f0(sp["mside"][0])} to {f0(sp["mside"][1])} with the supermarket and {f0(sp["mkanban"][1])} with kanban.</li>
<li><strong>The milk run also needs less handling.</strong> One loop delivers every carded load, so the handlers work {f1(Kb["handlerHours"])} hours against {f1(St["handlerHours"])} from the central store, and walk {f1(Kb["handlerKm"])}&nbsp;km instead of {f1(St["handlerKm"])}&nbsp;km. All three set-ups keep two handlers; the time is freed for other work, not saved as cash, and a timed milk run ties one person to its timetable.</li>
<li><strong>The price is stock and space at the line.</strong> Two bins hold {Kb['lineStock'] / Sd['lineStock']:.1f} times as much at the lines: {money100(Kb["lineStock"])} on average against {money100(Sd["lineStock"])}. The supermarket holds about {money100(Kb["smStock"])}, but that stock moves out of the central store; it does not have to be extra if the store's reorder points are lowered to match.</li>
</ul>
<h2>What each change contributes</h2>
<p>The three set-ups change several things at once: where the materials are, how the store is run, how many loads wait at the line and what triggers a refill. To separate them, the model was also run with one change at a time, averaged over ten simulated days.</p>
<p class="oee-cap">Table 3. One change at a time (ten-day averages; rows 2, 3, 5 and 6 are model checks, not set-ups in the Lab)</p>
<table>
<tr><th>Set-up</th><th class="num">Line minutes lost a shift</th><th class="num">Handler hours</th></tr>
{STEPS}
</table>
<ul>
<li><strong>The trigger matters most.</strong> With two bins at the line and a call when the first runs out, the lines stopped waiting even when every load still came from the central store. Calling before a material runs out, not where it is kept, removes the waiting.</li>
<li><strong>The store's way of working costs more than its distance.</strong> Booking each issue (2 minutes) and keeping line materials in part-number order account for most of the central store's extra waiting. With both removed, the central store loses {f0(STEP["near"]["starved"])} minutes against {f0(STEP["side"]["starved"])} for the supermarket.</li>
<li><strong>The supermarket and the milk run cut the handling.</strong> Two bins fed from the central store need {f1(STEP["store2"]["hh"])} handler-hours a shift; from the supermarket, {f1(STEP["side2"]["hh"])}; with the milk run, {f1(STEP["kanban"]["hh"])}. Note that in the central-store set-up the handlers are idle most of the shift while the lines wait: the problem there is calling late, not a shortage of people.</li>
</ul>
<h2>Sizing the milk run</h2>
<p>Kanban works here because every load lasts longer than the time it can take to replace it. The worst case is a card that goes up just after the milk run has left: it waits a full loop, then the handler collects and delivers. So the rule is</p>
{eq(r"t_{\text{load}} > t_{\text{loop}} + t_{\text{deliver}}")}
<p>where {im(r"t_{\text{load}}")} is how long one load lasts at the line, {im(r"t_{\text{loop}}")} the time between milk runs and {im(r"t_{\text{deliver}}")} the time to collect and deliver. The load that runs out first sets the limit: here a drum of resin lasts 40 minutes.</p>
{fig(fig_loop(), 4, "Line minutes lost with the kanban milk run, as the time between runs grows. Once a run takes longer than a drum of resin lasts, the lines start to wait.")}
<p>With loops of 10 to 30 minutes the lines lost nothing. At {okLoop} minutes the loop is right at the limit: the lines happened to lose nothing on this day, but one unlucky card would stop a line. At 50 and 60 minutes they lost {f0(Lp[4]["starved"])} and {f0(Lp[5]["starved"])} minutes. Line speed works the same way: at {f0(s2["speed"] * 100)}% speed every load lasts half as long. The central store then loses {f0(s2["mstore"]["mfg"]["starved"])} minutes a shift and the supermarket {f0(s2["mside"]["mfg"]["starved"])}. Kanban loses {f0(s2["mkanban"]["mfg"]["starved"])}, but the 20-minute loop is now at its limit: in the speed sweep it lost {f0(max(s["mkanban"]["mfg"]["starved"] for s in SP))} minutes at one speed. When lines speed up or loads get smaller, shorten the loop or add a bin.</p>
<p>The model also assumes the milk run sees every card posted before it leaves, as with an electronic signal or a light. With paper cards picked up on the round, a card can wait a whole extra loop, so the rule becomes {im(r"t_{\text{load}} > 2\,t_{\text{loop}} + t_{\text{deliver}}")}, and a 20-minute loop is too long for a 40-minute drum. In the model, cards seen one loop late cost {LATE[0]} minutes a shift at standard speed, {LATE[1]} at 150% and {LATE[2]} at 200%.</p>
<h2>What the waiting costs</h2>
<p>If Ridgeline makes up the lost pails with overtime, each line-hour lost costs a crew of {C["crew"]} operators at time and a half:</p>
{eq(r"\text{Overtime a year} = h \times c \times w \times 1.5 \times d")}
<p>where {im("h")} is line-hours lost a day, {im("c")} the crew per line, {im("w")} ${f0(C["wage"])} an hour loaded and {im("d")} {f0(C["days"])} days a year. For the central store that is {lstore['lostHours']:.2f} × {C["crew"]} × ${f0(C["wage"])} × 1.5 × {f0(C["days"])} = {money(ot("mstore"))} a year.</p>
<p class="oee-cap">Table 4. What each set-up costs a year (Canadian dollars)</p>
<table>
<tr><th>Item</th>{"".join(f'<th class="num">{NAME[k]}</th>' for k in K)}</tr>
{mtrs}
</table>
<ul>
<li><strong>Moving to a supermarket</strong> saves about {money(ot("mstore") - ot("mside"))} a year in overtime, for {money(rack[0])} to {money(rack[1])} of racking (34 faces on two levels, 68 positions, at the Part&nbsp;3 price range; a material can hold up to {f0(Sd["smMax"])} loads across its positions).</li>
<li><strong>Adding two bins and a milk run</strong> saves about {money(ot("mstore") - ot("mkanban") - dStock * C["carry"])} a year in overtime against the central store, after the carrying cost of the extra stock at the lines (at {C["carry"] * 100:.0f}% a year). Handler time falls too, but it only becomes cash if the freed hours replace other paid work.</li>
<li><strong>If the lines are sold out,</strong> the cost is lost sales, not overtime. At an illustrative ${f0(C["margin"])} contribution a pail, the {f0(lside["lostPails"])} pails a day the line-side set-up loses against kanban would be worth {money100(lside["lostPails"] * C["margin"])} a day. See <a href="{OEE2}.html">what OEE losses cost</a> for how to value lost output.</li>
</ul>
<h2>What the shift does not show</h2>
<ul>
<li><strong>Shelf life and lot control.</strong> Coatings materials have expiry dates and lot numbers. A supermarket must still be used first-expired, first-out, and every load moved to the line must stay traceable.</li>
<li><strong>Inventory records.</strong> Stock that moves to a supermarket or the line without a transaction is how record errors start. Decide where the stock is booked: issued to the line when it leaves the store, or when it is used.</li>
<li><strong>Batch changes.</strong> When a line changes colour or product, the line-side loads change too. Kanban works best for the materials every batch uses (pails, lids, labels); batch-specific materials are often kitted for each batch instead.</li>
<li><strong>Space and safety at the lines.</strong> Two bins and a supermarket need floor space next to the lines, clear of walkways and fire exits, with forklift traffic kept away from operators.</li>
<li><strong>Other losses.</strong> Breakdowns, changeovers and slow running are not modelled. A line that never waits for material can still have a low OEE.</li>
<li><strong>The receiving dock.</strong> Topping up the supermarket takes forklift time ahead of inbound put-away, so pallets wait a little longer at receiving: {f1(D["base"]["mstore"]["dts"])}, {f1(D["base"]["mside"]["dts"])} and {f1(D["base"]["mkanban"]["dts"])} minutes on average.</li>
</ul>
<p class="oee-cap">Table 5. Choosing how to feed a line (rules of thumb; the model checks inform the first three rows)</p>
<table>
<tr><th>If this is true</th><th>Start with</th></tr>
<tr><td>Lines stop at every run-out while a refill is fetched</td><td>Two bins, so the signal comes before the line runs dry, wherever the material is kept</td></tr>
<tr><td>Each refill from the store takes long because of paperwork or a part-number layout</td><td>A supermarket next to the lines for the materials every batch uses, issued in bulk to it</td></tr>
<tr><td>Handlers spend their day walking separate refills</td><td>A timed milk run, with the loop sized for the load that runs out fastest</td></tr>
<tr><td>Materials are specific to each batch or product</td><td>A kit for each batch, delivered before the batch starts</td></tr>
<tr><td>Floor space at the line is very tight</td><td>Smaller loads and a shorter loop, rather than more stock at the line</td></tr>
</table>
<h2>How to check your own plant</h2>
<ol>
<li><strong>Log every stop for a week</strong> with its cause, and count the minutes waiting for material.</li>
<li><strong>Time a refill</strong> from the moment a material runs out to the moment the line restarts.</li>
<li><strong>List the materials each line uses every batch,</strong> how long one load lasts, and where each one is stored today. Use the <a href="{ABCM}.html">criticality rating</a> to find the cheap items that can stop a line.</li>
<li><strong>Size the loop</strong> from the load that runs out fastest, and check that one load lasts longer than the loop plus the delivery time.</li>
<li><strong>Try it on one line</strong> with a temporary rack and cards before buying racking for every line.</li>
</ol>
<h2>What the model leaves out</h2>
<ul>
<li>One shift with fixed times, two lines and five materials a line; real lines use many more items, often in boxes rather than pallets.</li>
<li>Material is always in stock in the store; supplier shortages (see <a href="{SSM}.html">safety stock for manufacturers</a>) are a separate problem.</li>
<li>Loads last a fixed time at a given speed; no scrap, no batch changes, no breakdowns.</li>
<li>Calls are answered in order by the first free handler; in a real plant calls are often noticed late.</li>
<li>The milk run sees every card posted before it leaves; with paper cards collected on the round, add one loop to the delivery time.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>A line waiting for material is an availability loss, and where materials are kept decides how long each wait is.</li>
<li>Calling before a material runs out, with a second load at the line, removed the waiting in the model wherever the material was kept.</li>
<li>Here, a supermarket halved the waiting from {f0(St["starved"])} to {f0(Sd["starved"])} minutes, mostly by skipping the store's issue booking and part-number layout.</li>
<li>Two bins and a timed milk run kept the lines fed with the fewest handler hours, for {Kb['lineStock'] / Sd['lineStock']:.1f} times the stock at the lines.</li>
<li>Size the milk run from the load that runs out fastest: the loop plus delivery must be shorter than that load lasts.</li>
</ul>
<p>Earlier in this series: <a href="{WL1}.html">Part&nbsp;1</a>, what a bad layout costs; <a href="{WL2}.html">Part&nbsp;2</a>, flow patterns; <a href="{WL3}.html">Part&nbsp;3</a>, aisle widths. Next: <a href="from-layout-to-cash-inventory-turns-and-a-layout-payback-calculator.html">Part&nbsp;5</a>, from layout to cash: inventory turns and a layout payback calculator. Related: <a href="{OEE1}.html">what OEE really measures</a> and <a href="{ABCM}.html">ABC analysis for manufacturers</a>.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://lean.org/?p=1756" rel="noopener" target="_blank">Lean Enterprise Institute: Material handling</a> (a standard route at precisely set intervals, such as every 20 minutes, collecting kanban cards)</li>
<li><a href="https://www.taylorfrancis.com/chapters/mono/10.1201/b18933-7/two-bin-systems-material-handling-chris-ortiz" rel="noopener" target="_blank">Chris Ortiz: Two-bin systems for material handling</a> (the empty bin is the signal and the second bin covers the refill; described for small parts, the same logic used here with drums and pallets)</li>
<li><a href="https://michelbaudin.com/tag/milk-run/" rel="noopener" target="_blank">Michel Baudin: Supermarkets and milk runs</a> (what a supermarket is in lean manufacturing, and who owns it)</li>
<li><a href="https://www.allaboutlean.com/milk-run-intro/" rel="noopener" target="_blank">AllAboutLean: The milk run</a> (fixed schedule and fixed stops)</li>
<li><a href="https://www.informs-sim.org/wsc16papers/251.pdf" rel="noopener" target="_blank">Bae: Lean design and analysis of a milk-run delivery system, Winter Simulation Conference 2016</a> (a simulated milk-run case study)</li>
</ul>
{NOTE}{mathjs()}
<script src="../assets/js/wl1.js" defer></script>"""
    body = nowrap(body, [(1, 0, 26), (2, 0, 24)])
    return dict(slug=WL4, title="Central Store, Supermarket or Kanban? Feeding the Production Line",
                desc="Two filling lines fed three ways in the same plant, simulated: how a central store, a line-side supermarket and a kanban milk run change line stops.",
                cats=["operational-efficiency", "inventory-management"], tags=["line-side supermarket", "kanban", "milk run", "two-bin system", "OEE availability", "warehouse simulation"],
                body=body, date=DATE, author="Quak Foo Lee", read="11 min read", series=SER(4), cover_label="Warehouse layout",
                related=[WL3, OEE1, ABCM])


if __name__ == "__main__":
    a = part4()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])}\n")
