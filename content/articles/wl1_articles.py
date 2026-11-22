"""Warehouse layout series for Insights (V5.67). Part 1: good layout, bad layout.

The example is the Vancouver distributor of the warehouse operations series (72 x 52 m, about 40,300 sq ft). The
Layout Lab simulator (assets/sim/layout-lab.html, engine assets/js/wl-engine.js, drawing assets/js/wl-lab.js) runs
the same order stream and the same trucks through two layouts of the same racks. Every number quoted here comes from
content/articles/wl1_results.json, written by wl1_model.js from the same engine.

Usage:  node content/articles/wl1_model.js
        python3 content/articles/wl1_articles.py
        python3 content/gen/add_article.py good-layout-bad-layout-what-travel-and-congestion-cost-an-sme-warehouse
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, MUTED, LINE, eq, im, mathjs
W1 = "were-out-of-space-or-are-we-warehouse-cube-utilization-and-slotting"
W2 = "pickers-walk-half-the-day-pick-methods-and-pick-paths"
W3 = "the-dock-door-bottleneck-receiving-put-away-and-cross-docking"
ABC1 = "abc-inventory-analysis"

DATE = "2026-11-21"
WL1 = "good-layout-bad-layout-what-travel-and-congestion-cost-an-sme-warehouse"
WL2 = "u-shape-straight-through-or-l-shape-choosing-a-warehouse-flow-pattern"
SER = lambda n: {"name": "Warehouse layout series", "part": n, "of": 5}
SIM = "../assets/sim/layout-lab.html"
D = json.load(open(os.path.join(HERE, "wl1_results.json"), encoding="utf-8"))
A, R, SO, LO = D["base"]["asis"], D["base"]["redesign"], D["base"]["slotOnly"], D["base"]["layoutOnly"]
SEEDS = D["seeds"]
def rng(k, key): v = [x[k][key] for x in SEEDS]; return min(v), max(v)
P = D["P"]
NOTE = ('<p class="oee-note"><em>The distributor, its layouts, orders and times are an illustrative example built from stated assumptions, '
        'and the simulator is a simplified model. It shows how two layouts compare, not what your building will achieve. Time a few '
        'trips and watch your own dock before you move a rack.</em></p>')
f0 = lambda x: f"{x:,.0f}"
f1 = lambda x: f"{x:,.1f}"
money = lambda x: f"${round(x / 1000) * 1000:,.0f}"
pc = lambda x: f"{x * 100:.0f}%"
def down(a, b): return pc((a - b) / a)

GREY, WAITC = "#9AA8BA", "#E2574C"


def fig_split():
    """Picker-hours a day by activity: as-is, re-slotted only, redesigned."""
    rows = [("As-is layout", A), ("As-is racks, re-slotted", SO), ("Redesigned layout", R)]
    x0, y0, w, bh, gap = 190, 40, 430, 30, 22
    mx = math.ceil(A["busy"] / 5) * 5; X = lambda v: x0 + v / mx * w
    s = ""
    for t in range(0, mx + 1, 5):
        s += f'<line x1="{X(t):.1f}" y1="{y0 - 8}" x2="{X(t):.1f}" y2="{y0 + 3 * (bh + gap) - gap + 6}" stroke="#E4E1D8"/>' + txt(X(t), y0 + 3 * (bh + gap) - gap + 22, str(t), "middle", MUTED, 12)
    s += txt(x0 + w / 2, y0 + 3 * (bh + gap) - gap + 42, "Picker-hours a day", "middle", NAVY, 12.5, True)
    for i, (lab, r) in enumerate(rows):
        y = y0 + i * (bh + gap); x = x0
        s += txt(x0 - 12, y + bh / 2 + 5, lab, "end", NAVY, 13, True)
        for key, col in (("walk", BLUE), ("pick", GREEN), ("other", GREY), ("wait", WAITC)):
            v = r["split"][key]; ww = v / mx * w
            s += f'<rect x="{x:.1f}" y="{y}" width="{max(ww, 0.0):.1f}" height="{bh}" fill="{col}"/>'
            x += ww
        s += txt(x + 8, y + bh / 2 + 5, f1(r["busy"]), "start", NAVY, 13, True)
    lx = x0
    for lab, col in (("Walking", BLUE), ("Picking", GREEN), ("List, cart and drop-off", GREY), ("Giving way", WAITC)):
        s += f'<rect x="{lx}" y="10" width="12" height="12" rx="2" fill="{col}"/>' + txt(lx + 18, 21, lab, fill=NAVY, fs=12.5)
        lx += 18 + len(lab) * 7.2 + 18
    return svg(f"Bar chart of picker-hours a day by activity. As-is {f1(A['busy'])} hours, mostly walking. "
               f"The as-is racks re-slotted {f1(SO['busy'])} hours. The redesigned layout {f1(R['busy'])} hours. Picking time is the same in all three.",
               700, y0 + 3 * (bh + gap) + 40, s, 560)


def fig_volume():
    V = D["volume"]; x0, y0, w, h = 70, 30, 560, 230
    vmin, vmax = V[0]["orders"], V[-1]["orders"]
    ymax = math.ceil(max(v["asis"]["pickHoursDay"] for v in V) / 10) * 10
    X = lambda v: x0 + (v - vmin) / (vmax - vmin) * w
    Y = lambda hh: y0 + h - hh / ymax * h
    s = ""
    for t in range(0, ymax + 1, 10):
        s += f'<line x1="{x0}" y1="{Y(t):.1f}" x2="{x0 + w}" y2="{Y(t):.1f}" stroke="#E4E1D8"/>' + txt(x0 - 8, Y(t) + 4, str(t), "end", MUTED, 12)
    for v in range(150, 601, 75): s += txt(X(v), y0 + h + 18, str(v), "middle", MUTED, 12)
    s += txt(x0 + w / 2, y0 + h + 40, "Orders a day", "middle", NAVY, 12.5, True)
    s += f'<text x="20" y="{y0 + h / 2}" transform="rotate(-90 20 {y0 + h / 2})" text-anchor="middle" font-size="12.5" font-weight="600" fill="{NAVY}">Picker-hours a day</text>'
    for key, col, lab in (("asis", RED, "As-is layout"), ("redesign", GREEND, "Redesigned layout")):
        pts = [(X(v["orders"]), Y(v[key]["pickHoursDay"])) for v in V]
        s += f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{col}" stroke-width="3"/>'
        s += "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3.5" fill="{col}"/>' for a, b in pts)
    for k, (col, lab) in enumerate(((RED, "As-is layout"), (GREEND, "Redesigned layout"))):
        s += f'<rect x="{x0 + 14}" y="{y0 + 6 + k * 18}" width="12" height="12" rx="2" fill="{col}"/>' + txt(x0 + 32, y0 + 16 + k * 18, lab, fill=NAVY, fs=12.5, bold=True)
    return svg("Line chart of picker-hours a day against orders a day, 150 to 600, for both layouts. Both rise in a straight line; "
               "the as-is line rises about twice as steeply, so the gap grows with volume.", 700, 310, s, 560)


def part1():
    LA, LR = D["layout"]["asis"], D["layout"]["redesign"]
    save_lab = A["pickCostYear"] - R["pickCostYear"]; save_det = A["detYear"] - R["detYear"]
    v600 = D["volume"][-1]; v150 = D["volume"][0]
    rows = [
        ("Walk per order", f'{f0(A["walkOrder"])}&nbsp;m', f'{f0(SO["walkOrder"])}&nbsp;m', f'{f0(R["walkOrder"])}&nbsp;m'),
        ("Lines picked per picker-hour", f0(A["lph"]), f0(SO["lph"]), f0(R["lph"])),
        ("Picker-hours a day", f1(A["pickHoursDay"]), f1(SO["pickHoursDay"]), f1(R["pickHoursDay"])),
        ("Give-way stops in the shift", f0(A["waits"]), f0(SO["waits"]), f0(R["waits"])),
        ("Inbound truck time on site (average)*", f'{f0(A["truckIn"])}&nbsp;min', f'{f0(SO["truckIn"])}&nbsp;min', f'{f0(R["truckIn"])}&nbsp;min'),
        ("Inbound trucks still on site at 15:00", f0(A["trucksOnSite"]), f0(SO["trucksOnSite"]), f0(R["trucksOnSite"])),
        ("Dock-to-stock time (average)", f'{f0(A["dts"])}&nbsp;min', f'{f0(SO["dts"])}&nbsp;min', f'{f0(R["dts"])}&nbsp;min'),
        ("Inbound pallets not put away by 15:00", f0(A["notAway"]), f0(SO["notAway"]), f0(R["notAway"])),
        ("Picking labour a year", money(A["pickCostYear"]), money(SO["pickCostYear"]), money(R["pickCostYear"])),
        ("Truck detention a year*", money(A["detYear"]), money(SO["detYear"]), money(R["detYear"])),
    ]
    trs = "".join(f'<tr><td>{a}</td><td class="num">{b}</td><td class="num">{c}</td><td class="num">{d}</td></tr>' for a, b, c, d in rows)
    body = f"""{CSS}
<p>Most small warehouses were never designed. The racks went up along the longest wall, packing went wherever there was room, and the dock doors were shared because that was how the building came. The layout was decided once, years ago. It is paid for every day, in walking, waiting and trucks that sit at the door.</p>
<p>The <a href="{W1}.html">warehouse operations series</a> fixed one thing at a time inside the same building: slotting, pick methods, the dock, counting. This series steps back and looks at the whole floor. Part&nbsp;1 runs the same Vancouver distributor through two layouts of the same racks, side by side, and measures what layout alone costs.</p>
<h2>What a layout decides</h2>
<ul>
<li><strong>How far people walk.</strong> Aisle length, cross-aisles and where the fast movers sit set the walk for every order.</li>
<li><strong>Where people and forklifts meet.</strong> Every crossing point is lost time and a safety risk.</li>
<li><strong>How fast a truck is emptied.</strong> Door use and staging space decide whether unloading flows or stalls.</li>
<li><strong>Where stock waits.</strong> Pallets parked in aisles block traffic and hide stock.</li>
<li><strong>How much room there is to grow.</strong> A layout that is full on day one has no slack for a busy season.</li>
</ul>
<h2>Two layouts of the same building</h2>
<p>The example is the distributor from the warehouse operations series: a 72 by 52&nbsp;m building (about 40,300&nbsp;sq&nbsp;ft) with 780 SKUs picked by the case from pallet racks, 300 orders a day and 14 inbound trucks. It is a receiving-heavy day, as in <a href="{W3}.html">Part&nbsp;3</a> of that series: about 190 pallets come in while about 15 pallets of orders go out, the kind of day when stock is built up ahead of a busy season. Both layouts hold about the same racks ({f0(LA["rackCells"])} and {f0(LR["rackCells"])} pallet positions a level), the same five dock doors, the same crew, the same orders and the same trucks. Only the arrangement changes.</p>
<p class="oee-cap">Table 1. The two layouts</p>
<table>
<tr><th>Feature</th><th>As-is layout</th><th>Redesigned layout</th></tr>
<tr><td>Rack rows</td><td>{LA["aisles"]} aisles of 65&nbsp;m along the building</td><td>{LR["aisles"]} aisles of 30&nbsp;m across the building</td></tr>
<tr><td>Aisle ends</td><td>Open at the west end only; closed at the east wall</td><td>Open at both ends, with a front and a back cross-aisle</td></tr>
<tr><td>Slotting</td><td>Random: SKUs went wherever there was a gap</td><td>By picks a day: the busiest SKUs in the front bays next to packing</td></tr>
<tr><td>Dock doors</td><td>Five doors shared by receiving and shipping</td><td>Three receiving doors on the left, two shipping doors on the right</td></tr>
<tr><td>Staging</td><td>One shared area of {LA["recv"]} spots, plus overflow pallets in the main aisle</td><td>{LR["recv"]} receiving spots and {LR["ship"]} shipping spots in their own lanes</td></tr>
<tr><td>Packing</td><td>At the west end, far from the doors</td><td>Next to shipping staging</td></tr>
<tr><td>Flow</td><td>Forklifts and pickers share the main aisle and every aisle entrance</td><td>U-flow: in on the left, out on the right</td></tr>
</table>
<h2>The Layout Lab</h2>
<p>The simulator below runs one shift, 07:00 to 15:00, in both layouts at once. Orders arrive through the day. Pickers walk each order from packing to its pick faces and back. Trucks arrive, wait for a door and unload into staging, and a forklift puts each pallet away. When two people or vehicles meet within a metre, one gives way.</p>
<p>The heat map shows where the whole shift's traffic went; red rings mark where people and vehicles most often had to stop for each other. The numbered points match the list under the figure. Move the sliders to change the volume and how concentrated the picks are.</p>
<figure>
<iframe id="wl-sim" src="{SIM}#embed" title="Warehouse Layout Lab: two layouts of the same building, simulated side by side" loading="lazy" style="width:100%;height:2060px;border:0;display:block"></iframe>
<figcaption>Figure 1. The Warehouse Layout Lab. Left, the as-is layout; right, the redesigned layout. It switches between the 2D plan and the 3D view on its own until you pick a view; in 3D, drag to turn the building (both views turn together). The animation replays the shift 12 times faster than life; the table is the whole simulated shift.</figcaption>
</figure>
<p class="oee-hint"><a href="{SIM}">Open the Layout Lab on its own page</a> for a larger view.</p>
<h2>What the simulation shows</h2>
<p>Table 2 gives the shift at {f0(A["orders"])} orders a day. The middle column keeps the as-is racks, doors and staging and changes only the slotting, to show how much of the gain comes from where SKUs sit and how much from the layout itself.</p>
<p class="oee-cap">Table 2. One shift at {f0(A["orders"])} orders a day</p>
<table>
<tr><th>Measure</th><th class="num">As-is</th><th class="num">As-is, re-slotted</th><th class="num">Redesigned</th></tr>
{trs}
</table>
<p class="oee-hint">* Trucks still at a door or waiting at 15:00 are counted up to 15:00, so the as-is figures are a lower bound.</p>
{fig(fig_split(), 2, "Where the picker-hours go. Picking takes the same time in all three; what changes is the walking.")}
<p>Four things stand out.</p>
<ul>
<li><strong>Walking is the cost.</strong> As-is, a picker walks about {f0(A["walkOrder"])}&nbsp;m for a three-line order, because every line means a trip into a 65&nbsp;m dead-end aisle and back out the same end. Walking is {pc(A["split"]["walk"] / A["busy"])} of the picker-hours. The redesign cuts the walk to {f0(R["walkOrder"])}&nbsp;m and the day from {f1(A["pickHoursDay"])} to {f1(R["pickHoursDay"])} picker-hours, {down(A["pickHoursDay"], R["pickHoursDay"])} less.</li>
<li><strong>Slotting does much of it, and costs least.</strong> Re-slotting the as-is racks alone takes the walk to {f0(SO["walkOrder"])}&nbsp;m and the day to {f1(SO["pickHoursDay"])} picker-hours: about {pc((A["pickHoursDay"] - SO["pickHoursDay"]) / (A["pickHoursDay"] - R["pickHoursDay"]))} of the picking gain, with no rack moved. The share depends on the order of the changes. Build the new aisles first with random slotting and the day falls to {f1(LO["pickHoursDay"])} picker-hours; re-slotting then adds the last {pc((LO["pickHoursDay"] - R["pickHoursDay"]) / (A["pickHoursDay"] - R["pickHoursDay"]))}. Either way, slotting is the cheapest step, so do it first.</li>
<li><strong>Fewer meetings, mainly a safety gain.</strong> Give-way stops fall from {f0(A["waits"])} to {f0(R["waits"])} a shift. The time lost to them is small at this volume (about {f0(A["split"]["wait"] * 60)} minutes of picker time a day as-is), but each one is a moment when a person and a forklift, or two pickers with carts, share the same metre of aisle.</li>
<li><strong>At the dock, the forklift is the bottleneck.</strong> As-is, the single forklift spends about {f1(A["forkCycle"])} minutes on each pallet, most of it driving into 65&nbsp;m dead-end aisles to random locations. That is about {f1(A["forkCycle"] * A["inPallets"] / 60)} hours of put-away for an 8-hour shift. Staging fills, unloading stops, trucks average {f0(A["truckIn"])} minutes on site, and {f0(A["notAway"])} pallets are still waiting at 15:00. Shared doors were not the problem on this day: trucks waited under a minute for a door. Re-slotting alone brings the forklift's trip down to {f1(SO["forkCycle"])} minutes and clears the backlog; the redesign brings it to {f1(R["forkCycle"])} minutes and {f0(R["truckIn"])} minutes a truck.</li>
</ul>
<h2>What it is worth</h2>
<p>Picking labour a year is the picker-hours a day times the loaded wage and the working days:</p>
{eq(r"C = H \times w \times d")}
<p>where {im("H")} is picker-hours a day, {im("w")} is ${f0(P["wage"])} an hour loaded and {im("d")} is {f0(P["days"])} days a year. As-is that is {f1(A["pickHoursDay"])} × ${f0(P["wage"])} × {f0(P["days"])} = {money(A["pickCostYear"])}; redesigned, {money(R["pickCostYear"])}. The difference is about <strong>{money(save_lab)} a year</strong>, plus at least {money(save_det)} of truck detention (charged at ${f0(P["detention"])} an hour after two hours on site, as in <a href="{W3}.html">Part&nbsp;3</a> of the operations series).</p>
<p>Against that sits the one-off cost of the change: taking down and re-erecting racks, rack engineering and permits where required, relabelling, and the days of disruption while it happens. <a href="from-layout-to-cash-inventory-turns-and-a-layout-payback-calculator.html">Part&nbsp;5</a> of this series builds that payback, and shows when a better layout also frees cash tied up in stock.</p>
{fig(fig_volume(), 3, "Picker-hours a day as volume grows. The as-is layout needs about twice the picker-hours at every volume, so the gap in people grows with the business.")}
<p>The gap grows with volume. At {f0(v150["orders"])} orders a day the redesign saves {f1(v150["asis"]["pickHoursDay"] - v150["redesign"]["pickHoursDay"])} picker-hours a day; at {f0(v600["orders"])} it saves {f1(v600["asis"]["pickHoursDay"] - v600["redesign"]["pickHoursDay"])}, the work of about {round((v600["asis"]["pickHoursDay"] - v600["redesign"]["pickHoursDay"]) / 7)} pickers on 7-hour shifts. The dock follows the same pattern: as-is, trucks average {f0(v600["asis"]["truckIn"])} minutes at {f0(v600["orders"])} orders a day, even with a second forklift.</p>
<p>One simulated day is one sample. Across ten other days with different orders and truck times, the as-is layout needed {f1(rng("asis","pickHoursDay")[0])} to {f1(rng("asis","pickHoursDay")[1])} picker-hours and the redesign {f1(rng("redesign","pickHoursDay")[0])} to {f1(rng("redesign","pickHoursDay")[1])}, so the picking result holds. The dock swings much more: as-is, trucks averaged {f0(rng("asis","truckIn")[0])} to {f0(rng("asis","truckIn")[1])} minutes on site and {f0(rng("asis","notAway")[0])} to {f0(rng("asis","notAway")[1])} pallets were left at 15:00, while the redesign stayed at {f0(rng("redesign","truckIn")[0])} to {f0(rng("redesign","truckIn")[1])} minutes with none left. Treat the detention figure as an order of magnitude, not a forecast.</p>
<h2>Six faults to look for in your own building</h2>
<p class="oee-cap">Table 3. Layout faults, how to spot them and the first fix</p>
<table>
<tr><th>Fault</th><th>How to spot it</th><th>First fix</th></tr>
<tr><td>Dead-end aisles</td><td>Pickers walk into an aisle and come back out the same end</td><td>Cut a cross-aisle through the middle of long rows, or open the far end</td></tr>
<tr><td>Random slotting</td><td>Your 50 busiest SKUs are spread across the building</td><td>Re-slot by picks a day, busiest closest to packing (<a href="{W1}.html">operations Part&nbsp;1</a>)</td></tr>
<tr><td>Crossing flows</td><td>Forklifts and pickers use the same aisle to reach the same entrances</td><td>Send put-away in from the back or the far side; mark pedestrian lanes</td></tr>
<tr><td>Staging in aisles</td><td>Pallets parked "for now" in the main aisle</td><td>Paint staging lanes in the dock zone and keep the main aisle clear</td></tr>
<tr><td>Shared doors and lanes</td><td>Outbound pallets wait where trucks unload; trucks queue for a door at peak</td><td>Assign doors and lanes to receiving or shipping, at least at peak hours</td></tr>
<tr><td>Packing far from shipping</td><td>Every outbound pallet crosses the building</td><td>Move packing next to shipping staging; packing benches move easily</td></tr>
</table>
<h2>Check your layout in one afternoon</h2>
<ol>
<li><strong>Draw the floor to scale.</strong> Racks, aisles, doors, packing, staging. Graph paper or a spreadsheet with one cell per metre is enough.</li>
<li><strong>Trace ten orders.</strong> Follow a picker and draw each trip on the plan: a spaghetti diagram. Measure the walk per order.</li>
<li><strong>Mark the crossings.</strong> Watch the main aisle for an hour and mark every time a person stops for a forklift or another person.</li>
<li><strong>Log the dock.</strong> For one day, note each truck's arrival, door time and departure, and when staging was full.</li>
<li><strong>Find your top 50 SKUs.</strong> Rank by picks a day (<a href="{ABC1}.html">ABC analysis</a>) and mark where they sit. If they are scattered, re-slot before anything else.</li>
<li><strong>Look for pallets that live in aisles.</strong> Each one is a missing staging lane or a slotting problem.</li>
</ol>
<h2>What the model leaves out</h2>
<ul>
<li>One shift, one fixed seed. A real day has more variation: late trucks, rush orders, absences.</li>
<li>Single-order picking from the floor level of the racks. Batch, zone and wave picking (<a href="{W2}.html">operations Part&nbsp;2</a>) would cut walking in both layouts.</li>
<li>People and vehicles move on a 1&nbsp;m grid and give way within a metre. Real congestion depends on aisle width, sight lines and site rules.</li>
<li>Replenishment of the pick faces, cycle counts and returns are not simulated.</li>
<li>A receiving-heavy day: far more pallets come in than go out, which loads the forklift. On a balanced day the dock gap would be smaller; the picking gap would not change.</li>
<li>The redesign keeps the same building, about the same racks and the same number of doors. It does not count the cost of moving them.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>The same building and about the same racks can need about half the picker-hours with a different layout: {f1(A["pickHoursDay"])} against {f1(R["pickHoursDay"])} a day in the example.</li>
<li>Slotting is the cheapest step and a large part of the picking gain. Start there.</li>
<li>At the dock, long put-away trips make the forklift the bottleneck. Shorter trips clear the backlog before more doors would.</li>
<li>Separating flows cuts the moments when people and forklifts share an aisle, which is a safety gain as much as a time gain.</li>
<li>Measure first: a spaghetti diagram of ten orders and a day's dock log tell you which fault you have.</li>
</ul>
<p>Next in this series: <a href="{WL2}.html">Part&nbsp;2</a> compares the three common flow patterns (U-shape, straight-through and L-shape) and where each one puts the docks, packing and fast movers. Related: <a href="{W1}.html">cube utilization and slotting</a>, <a href="{W2}.html">pick methods and pick paths</a> and <a href="{W3}.html">the dock door bottleneck</a> in the warehouse operations series.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://doi.org/10.1016/j.ejor.2006.07.009" rel="noopener" target="_blank">De Koster, Le-Duc and Roodbergen (2007), Design and control of warehouse order picking: a literature review, European Journal of Operational Research</a> (travel as the largest share of picking time; layout, storage assignment and routing)</li>
</ul>
{NOTE}{mathjs()}
<script src="../assets/js/wl1.js" defer></script>"""
    body = nowrap(body, [(1, 0, 14), (2, 0, 40), (3, 0, 26)])
    return dict(slug=WL1, title="Good Layout, Bad Layout: What Travel and Congestion Cost an SME Warehouse",
                desc="The same warehouse, racks and orders simulated in two layouts side by side, in 2D and 3D: walking, congestion, dock time and what the layout costs a year.",
                cats=["operational-efficiency", "inventory-management"], tags=["warehouse layout", "warehouse design", "slotting", "dock doors", "warehouse simulation", "warehouse productivity"],
                body=body, date=DATE, author="Quak Foo Lee", read="11 min read", series=SER(1), cover_label="Warehouse layout",
                related=[W1, W2, W3])


if __name__ == "__main__":
    a = part1()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])}\n")
