"""Warehouse layout series for Insights (V5.68). Part 2: U-shape, straight-through or L-shape?

The same Vancouver distributor, racks, orders and trucks as Part 1, in three flow patterns. The Layout Lab
(assets/sim/layout-lab.html, opened with s=p2) runs them side by side; every number quoted here comes from
content/articles/wl2_results.json, written by wl2_model.js from the same engine (assets/js/wl-engine.js).

Usage:  node content/articles/wl2_model.js
        python3 content/articles/wl2_articles.py
        python3 content/gen/add_article.py u-shape-straight-through-or-l-shape-choosing-a-warehouse-flow-pattern
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, MUTED, LINE, eq, im, mathjs

DATE = "2026-11-21"
WL1 = "good-layout-bad-layout-what-travel-and-congestion-cost-an-sme-warehouse"
WL2 = "u-shape-straight-through-or-l-shape-choosing-a-warehouse-flow-pattern"
W1 = "were-out-of-space-or-are-we-warehouse-cube-utilization-and-slotting"
W3 = "the-dock-door-bottleneck-receiving-put-away-and-cross-docking"
ABC1 = "abc-inventory-analysis"
SER = lambda n: {"name": "Warehouse layout series", "part": n, "of": 5}
SIM = "../assets/sim/layout-lab.html"
D = json.load(open(os.path.join(HERE, "wl2_results.json"), encoding="utf-8"))
K = D["kinds"]
U, I, Ls = (D["base"][k] for k in K)
UC = D["base"]["ucentre"]
def avg(k, key): v = [s[k][key] for s in D["seeds"]]; return sum(v) / len(v)
LY = D["layout"]
NAME = {"redesign": "U-shape", "thru": "Straight-through", "lshape": "L-shape"}
COLR = {"redesign": BLUE, "thru": ORANGE, "lshape": GREEND}
NOTE = ('<p class="oee-note"><em>The distributor, its three layouts, orders and times are an illustrative example built from stated assumptions, '
        'and the simulator is a simplified model. It compares the patterns in one building; it does not tell you which pattern your building or '
        'site should have. Land, yards, security and growth plans often decide that first.</em></p>')
f0 = lambda x: f"{x:,.0f}"
f1 = lambda x: f"{x:,.1f}"
f2 = lambda x: f"{x:,.2f}"
money = lambda x: f"${round(x / 1000) * 1000:,.0f}"
pc = lambda x: f"{x * 100:.0f}%"
GREY, WAITC = "#9AA8BA", "#E2574C"
def srng(k, key): v = [s[k][key] for s in D["seeds"]]; return min(v), max(v)
def drng(a, b, key): v = [s[a][key] - s[b][key] for s in D["seeds"]]; return min(v), max(v)


def fig_split():
    rows = [(NAME[k], D["base"][k]) for k in K]
    x0, y0, w, bh, gap = 150, 40, 470, 30, 22
    mx = math.ceil(max(r["busy"] for _, r in rows) / 5) * 5; X = lambda v: x0 + v / mx * w
    s = ""
    yb = y0 + len(rows) * (bh + gap) - gap
    for t in range(0, mx + 1, 5):
        s += f'<line x1="{X(t):.1f}" y1="{y0 - 8}" x2="{X(t):.1f}" y2="{yb + 6}" stroke="#E4E1D8"/>' + txt(X(t), yb + 22, str(t), "middle", MUTED, 12)
    s += txt(x0 + w / 2, yb + 42, "Picker-hours a day", "middle", NAVY, 12.5, True)
    for i, (lab, r) in enumerate(rows):
        y = y0 + i * (bh + gap); x = x0
        s += txt(x0 - 12, y + bh / 2 + 5, lab, "end", NAVY, 13, True)
        for key, col in (("walk", BLUE), ("pick", GREEN), ("other", GREY), ("wait", WAITC)):
            ww = r["split"][key] / mx * w
            s += f'<rect x="{x:.1f}" y="{y}" width="{ww:.1f}" height="{bh}" fill="{col}"/>'; x += ww
        s += txt(x + 8, y + bh / 2 + 5, f1(r["busy"]), "start", NAVY, 13, True)
    lx = x0
    for lab, col in (("Walking", BLUE), ("Picking", GREEN), ("List, cart and drop-off", GREY), ("Giving way", WAITC)):
        s += f'<rect x="{lx}" y="10" width="12" height="12" rx="2" fill="{col}"/>' + txt(lx + 18, 21, lab, fill=NAVY, fs=12.5)
        lx += 18 + len(lab) * 7.2 + 18
    return svg("Bar chart of picker-hours a day by activity for the three flow patterns. " +
               ", ".join(f"{NAME[k]} {f1(D['base'][k]['busy'])} hours" for k in K) + ". Picking time is the same; walking differs.",
               700, yb + 50, s, 560)


def fig_volume():
    V = D["volume"]; x0, y0, w, h = 70, 30, 560, 230
    vmin, vmax = V[0]["orders"], V[-1]["orders"]
    ymax = math.ceil(max(v[k]["pickHoursDay"] for v in V for k in K) / 10) * 10
    X = lambda v: x0 + (v - vmin) / (vmax - vmin) * w
    Y = lambda hh: y0 + h - hh / ymax * h
    s = ""
    for t in range(0, ymax + 1, 10):
        s += f'<line x1="{x0}" y1="{Y(t):.1f}" x2="{x0 + w}" y2="{Y(t):.1f}" stroke="#E4E1D8"/>' + txt(x0 - 8, Y(t) + 4, str(t), "end", MUTED, 12)
    for v in range(150, 601, 75): s += txt(X(v), y0 + h + 18, str(v), "middle", MUTED, 12)
    s += txt(x0 + w / 2, y0 + h + 40, "Orders a day", "middle", NAVY, 12.5, True)
    s += f'<text x="20" y="{y0 + h / 2}" transform="rotate(-90 20 {y0 + h / 2})" text-anchor="middle" font-size="12.5" font-weight="600" fill="{NAVY}">Picker-hours a day</text>'
    for k in K:
        pts = [(X(v["orders"]), Y(v[k]["pickHoursDay"])) for v in V]
        s += f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{COLR[k]}" stroke-width="2.6"/>'
        s += "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3.2" fill="{COLR[k]}"/>' for a, b in pts)
    for i, k in enumerate(K):
        s += f'<rect x="{x0 + 14}" y="{y0 + 6 + i * 18}" width="12" height="12" rx="2" fill="{COLR[k]}"/>' + txt(x0 + 32, y0 + 16 + i * 18, NAME[k], fill=NAVY, fs=12.5, bold=True)
    return svg("Line chart of picker-hours a day against orders a day, 150 to 600, for the three patterns. The three lines "
               "almost overlap at every volume.", 700, 310, s, 560)


def part2():
    rows = [
        ("Walk per order", lambda r: f'{f0(r["walkOrder"])}&nbsp;m'),
        ("Lines picked per picker-hour", lambda r: f0(r["lph"])),
        ("Picker-hours a day", lambda r: f1(r["pickHoursDay"])),
        ("Give-way stops in the shift", lambda r: f0(r["waits"])),
        ("Forklift time per pallet put away", lambda r: f'{f2(r["forkCycle"])}&nbsp;min'),
        ("Forklift driving in the shift", lambda r: f'{f1(r["forkKm"])}&nbsp;km'),
        ("Dock-to-stock time (average)", lambda r: f'{f0(r["dts"])}&nbsp;min'),
        ("Inbound truck time on site (average)", lambda r: f'{f0(r["truckIn"])}&nbsp;min'),
        ("Picking labour a year", lambda r: money(r["pickCostYear"])),
    ]
    trs = "".join(f'<tr><td>{lab}</td>' + "".join(f'<td class="num">{fn(D["base"][k])}</td>' for k in K) + '</tr>' for lab, fn in rows)
    dI = drng("thru", "redesign", "pickHoursDay")
    def spread(sd): v = [sd[k]["pickHoursDay"] for k in K]; return (max(v) - min(v)) / min(v)
    SPR = [spread(sd) for sd in D["seeds"]]
    WINS = {k: sum(1 for sd in D["seeds"] if min(K, key=lambda q: sd[q]["pickHoursDay"]) == k) for k in K}
    v600 = D["volume"][-1]; v150 = D["volume"][0]
    body = f"""{CSS}
<p><a href="{WL1}.html">Part&nbsp;1</a> showed that the same building and racks can need half the picker-hours with a better layout. Its redesign put the receiving and shipping doors on the same wall: a U-shape. That is one of three common flow patterns. The other two put receiving and shipping on opposite walls (straight-through, also called I-flow) or on two walls that meet at a corner (L-shape).</p>
<p>Which one is best is usually argued from rules of thumb. This part runs the same Vancouver distributor, racks, orders and trucks through all three patterns, side by side, and measures what changes.</p>
<h2>The three patterns</h2>
<p class="oee-cap">Table 1. Three ways to arrange the flow (the last two columns are common rules of thumb)</p>
<table>
<tr><th>Pattern</th><th>Where the docks are</th><th>How goods move</th><th>Usually said to suit</th><th>Watch out for</th></tr>
<tr><td>U-shape</td><td>Receiving and shipping on the same wall, side by side</td><td>In, back into storage, and out again near where they came in</td><td>Most SME warehouses; buildings with one good yard side</td><td>Inbound and outbound trucks and staging close together</td></tr>
<tr><td>Straight-through (I-flow)</td><td>Receiving on one wall, shipping on the opposite wall</td><td>One way across the building</td><td>High volumes, cross-docking, separate inbound and outbound sites or security zones</td><td>Two yards; fast movers can sit near shipping or near receiving, not both</td></tr>
<tr><td>L-shape</td><td>Receiving and shipping on two walls that meet at a corner</td><td>In on one side, a turn, out on the next</td><td>Buildings or sites where only two adjacent sides have yard room</td><td>Two yards whose traffic meets at the corner</td></tr>
</table>
<h2>The same building, three ways</h2>
<p>All three keep the building (72 by 52&nbsp;m, about 40,300&nbsp;sq&nbsp;ft), the same racks ({f0(LY["redesign"]["rackCells"])} pallet positions a level), three receiving and two shipping doors, the same crew and the same receiving-heavy day as Part&nbsp;1: 300 orders and 14 inbound trucks. Each one follows the good practice from Part&nbsp;1: aisles open at both ends, busiest SKUs nearest packing, packing next to shipping, separate staging lanes.</p>
<ul>
<li><strong>U-shape:</strong> the Part&nbsp;1 redesign. {LY["redesign"]["aisles"]} aisles of {LY["redesign"]["aisleLen"]}&nbsp;m across the building, receiving doors at the west end of the south wall and shipping doors at the east end.</li>
<li><strong>Straight-through:</strong> receiving on the west wall, shipping and packing on the east wall, {LY["thru"]["aisles"]} aisles of {LY["thru"]["aisleLen"]}&nbsp;m running the same way as the flow (the same number of pallet positions, arranged along the building).</li>
<li><strong>L-shape:</strong> the U-shape's racks, with receiving on the south wall toward the south-east corner, shipping on the east wall, and packing in the corner between them.</li>
</ul>
<h2>The Layout Lab</h2>
<p>The simulator shows the three floors running the same shift. Pick <em>All three</em> to compare them at once or one pattern to see it larger, and switch between the 2D plan and the 3D view. The numbered points explain what to notice in each.</p>
<figure>
<iframe id="wl-sim" src="{SIM}#embed&amp;s=p2" title="Warehouse Layout Lab: U-shape, straight-through and L-shape layouts of the same building, simulated side by side" loading="lazy" style="width:100%;height:3820px;border:0;display:block"></iframe>
<figcaption>Figure 1. The Warehouse Layout Lab with the three flow patterns. Trucks use a yard on each wall that has doors. The animation replays the shift 12 times faster than life; the table is the whole simulated shift.</figcaption>
</figure>
<p class="oee-hint"><a href="{SIM}?s=p2">Open the Layout Lab on its own page</a> for a larger view.</p>
<h2>What the simulation shows</h2>
<p class="oee-cap">Table 2. One shift at {f0(U["orders"])} orders a day</p>
<table>
<tr><th>Measure</th>{"".join(f'<th class="num">{NAME[k]}</th>' for k in K)}</tr>
{trs}
</table>
{fig(fig_split(), 2, "Where the picker-hours go in each pattern. Picking takes the same time; the walking differs.")}
<ul>
<li><strong>Picking hardly changes.</strong> In every pattern the busiest SKUs sit in short aisle ends next to packing, so pickers walk {f0(Ls["walkOrder"])} to {f0(I["walkOrder"])}&nbsp;m an order. Across ten other simulated days the three patterns were within {min(SPR) * 100:.1f}% to {max(SPR) * 100:.1f}% of each other in picker-hours. The L-shape needed the fewest on {WINS["lshape"]} days and the U-shape on {WINS["redesign"]}; straight-through never did, though it was never more than {f2(dI[1])} hours a day behind the U-shape.</li>
<li><strong>Put-away is where the patterns differ, and it is about the receiving doors.</strong> The forklift carries most pallets to the fast movers, which sit next to packing. In the L-shape the receiving doors are close to that corner, so a put-away takes {f2(Ls["forkCycle"])} minutes. In the U-shape they are at the far end of the wall ({f2(U["forkCycle"])} minutes), and in straight-through they are across the building ({f2(I["forkCycle"])} minutes). Dock-to-stock follows: {f0(Ls["dts"])}, {f0(U["dts"])} and {f0(I["dts"])} minutes on average.</li>
<li><strong>It is the door position, not the letter.</strong> To check, the same U-shape was run with its receiving doors moved toward the middle of the wall, next to packing. Its put-away fell to {f2(UC["forkCycle"])} minutes and dock-to-stock to {f0(UC["dts"])} minutes, the same as the L-shape. The flow pattern decides which walls the doors can go on; what pays is putting receiving close to where the fast movers live.</li>
<li><strong>Straight-through separates the docks, not the traffic.</strong> Receiving and packing are on opposite sides, but the forklift still carries fast-mover pallets to the east end, where the pickers work: {f0(I["waits"])} give-way stops against {f0(U["waits"])} in the U-shape and {f0(Ls["waits"])} in the L-shape, all small amounts of time.</li>
</ul>
{fig(fig_volume(), 3, "Picker-hours a day as volume grows. The three lines almost overlap: picking cost hardly depends on the flow pattern when each is laid out well.")}
<p>Volume does not change the picture. At {f0(v150["orders"])} orders a day the three need {", ".join(f1(v150[k]["pickHoursDay"]) for k in K)} picker-hours; at {f0(v600["orders"])}, {", ".join(f1(v600[k]["pickHoursDay"]) for k in K)}.</p>
<h2>What the shift does not show</h2>
<p>A one-shift simulation of picking and put-away is only part of the decision. These usually weigh as much, and often decide it:</p>
<ul>
<li><strong>The site.</strong> A U-shape needs one yard; straight-through and L-shape need two. Many sites only have room for trucks on one side.</li>
<li><strong>Dock capacity.</strong> One wall limits the number of doors. Very high truck counts, or a large share of cross-docking (see <a href="{W3}.html">the dock door bottleneck</a>), are where straight-through earns its reputation for high volume.</li>
<li><strong>Separation.</strong> Food, pharmaceuticals, customs-bonded goods or very different inbound and outbound carriers can call for receiving and shipping on separate sides.</li>
<li><strong>Growth.</strong> A U-shape can extend away from its dock wall without moving a door. Straight-through can extend sideways along both dock walls. An L-shape keeps two walls free.</li>
<li><strong>Yard and dock staff.</strong> Two yards can mean two gates, two sets of dock staff, or people walking across the building.</li>
</ul>
<p class="oee-cap">Table 3. Choosing a pattern (rules of thumb; the simulation tests only the last row's point about door position)</p>
<table>
<tr><th>If this is true</th><th>Start with</th></tr>
<tr><td>Only one side of the site has room for trucks</td><td>U-shape</td></tr>
<tr><td>You pick by the case or piece and a few fast movers drive most picks and put-aways</td><td>Any pattern, with receiving doors placed close to where the fast movers sit</td></tr>
<tr><td>Inbound and outbound truck counts need more doors than one wall holds</td><td>Straight-through</td></tr>
<tr><td>A large share of goods is cross-docked, or inbound and outbound must be kept apart</td><td>Straight-through</td></tr>
<tr><td>Yard room is only on two adjacent sides</td><td>L-shape, with receiving toward the corner where packing and the fast movers are</td></tr>
</table>
<h2>How to check your own building</h2>
<ol>
<li><strong>Mark where trucks can go.</strong> Draw the site with every side that has, or could have, yard room.</li>
<li><strong>Count doors by the hour.</strong> Take your busiest day's truck arrivals and departures and see whether one wall's doors can cover them.</li>
<li><strong>Find the fast movers' path.</strong> Rank SKUs by picks a day (<a href="{ABC1}.html">ABC analysis</a>) and ask whether they can sit close to both receiving and packing.</li>
<li><strong>Measure the put-away trip.</strong> Time a few pallets from the receiving door to where your fast movers sit. If it is the longest trip in the building, the receiving doors are in the wrong place, whatever the pattern.</li>
<li><strong>Test before you move racks.</strong> A plan to scale and ten traced orders, as in Part&nbsp;1, show most of the difference.</li>
</ol>
<h2>What the model leaves out</h2>
<ul>
<li>One shift with one fixed seed per day, single-order case picking, one forklift (two from 400 orders a day).</li>
<li>No cross-docking, no replenishment of pick faces, no returns.</li>
<li>The same building for all three. A real choice usually comes with a different building shape or site.</li>
<li>The yards are drawn to fit the plan; real truck aprons are deeper.</li>
<li>Each pattern is one reasonable layout of it. A different rack block or door position would give different numbers, as the moved-door U-shape shows.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>Laid out well, the three patterns pick at almost the same cost in this building: within {max(SPR) * 100:.1f}% of each other on every simulated day.</li>
<li>Put-away and dock-to-stock depend on how close the receiving doors are to the fast movers. Here the L-shape, with receiving near its corner, and a U-shape with receiving moved to the middle both cut put-away time by about 10% and dock-to-stock by more than half.</li>
<li>Straight-through separates the docks but not the people and forklifts inside.</li>
<li>Site, dock capacity, separation and growth usually decide the pattern before productivity does.</li>
</ul>
<p>Earlier in this series: <a href="{WL1}.html">Part&nbsp;1</a>, what a bad layout costs. Next: <a href="wide-narrow-or-very-narrow-aisles-warehouse-density-against-access.html">Part&nbsp;3</a>, density against access: wide, narrow or very narrow aisles. Related: <a href="{W1}.html">cube utilization and slotting</a> and <a href="{W3}.html">the dock door bottleneck</a> in the warehouse operations series.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://learn.g2.com/warehouse-layout" rel="noopener" target="_blank">G2 Learn Hub: How to plan a warehouse layout that boosts efficiency</a> (the three common flow types and the uses usually given for each)</li>
</ul>
{NOTE}
<script src="../assets/js/wl1.js" defer></script>"""
    body = nowrap(body, [(1, 0, 26), (2, 0, 40)])
    return dict(slug=WL2, title="U-Shape, Straight-Through or L-Shape? Choosing a Warehouse Flow Pattern",
                desc="The same warehouse, racks and orders simulated in three flow patterns: picking barely changes, put-away depends on where receiving sits.",
                cats=["operational-efficiency", "inventory-management"], tags=["warehouse layout", "U-shaped warehouse", "flow-through warehouse", "warehouse design", "dock doors", "warehouse simulation"],
                body=body, date=DATE, author="Quak Foo Lee", read="10 min read", series=SER(2), cover_label="Warehouse layout",
                related=[WL1, W1, W3])


if __name__ == "__main__":
    a = part2()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])}\n")
