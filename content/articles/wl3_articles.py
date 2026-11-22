"""Warehouse layout series for Insights (V5.69). Part 3: wide, narrow or very narrow aisles?

Density against access. The same Vancouver distributor, doors, orders and trucks on the U-shape plan of Part 2, with
4 m aisles (counterbalance truck), 3 m aisles (reach truck) and 2 m aisles (wire-guided turret truck). The Layout Lab
(assets/sim/layout-lab.html, opened with s=p3) runs them side by side; every number quoted here comes from
content/articles/wl3_results.json, written by wl3_model.js from the same engine (assets/js/wl-engine.js).

Usage:  node content/articles/wl3_model.js
        python3 content/articles/wl3_articles.py
        python3 content/gen/add_article.py wide-narrow-or-very-narrow-aisles-warehouse-density-against-access
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, MUTED, LINE, eq, im, mathjs, tn

DATE = "2026-11-21"
WL1 = "good-layout-bad-layout-what-travel-and-congestion-cost-an-sme-warehouse"
WL2 = "u-shape-straight-through-or-l-shape-choosing-a-warehouse-flow-pattern"
WL3 = "wide-narrow-or-very-narrow-aisles-warehouse-density-against-access"
W1 = "were-out-of-space-or-are-we-warehouse-cube-utilization-and-slotting"
W3 = "the-dock-door-bottleneck-receiving-put-away-and-cross-docking"
SER = lambda n: {"name": "Warehouse layout series", "part": n, "of": 5}
SIM = "../assets/sim/layout-lab.html"
D = json.load(open(os.path.join(HERE, "wl3_results.json"), encoding="utf-8"))
K = D["kinds"]
Wd, Nr, Vn = (D["base"][k] for k in K)
LY = D["layout"]
EC = D["econ"]; C = EC["C"]; OP = EC["opts"]; P = D["P"]
NAME = {"wide": "Wide aisles", "redesign": "Narrow aisles", "vna": "Very narrow aisles"}
TRUCK = {"wide": "counterbalance truck", "redesign": "reach truck", "vna": "wire-guided turret truck"}
COLR = {"wide": ORANGE, "redesign": BLUE, "vna": GREEND}
NOTE = ('<p class="oee-note"><em>The distributor, its three set-ups, orders and times are an illustrative example built from stated assumptions, '
        'and the simulator is a simplified model. The prices are published ranges, not quotes: racks, trucks and floor work in your building, '
        'with Vancouver seismic requirements, need quotes from suppliers. This is not financial advice.</em></p>')
f0 = lambda x: f"{x:,.0f}"
f1 = lambda x: f"{x:,.1f}"
f2 = lambda x: f"{x:,.2f}"
money = lambda x: f"${round(x / 1000) * 1000:,.0f}"
GREY, WAITC = "#9AA8BA", "#E2574C"
usd = lambda x: f"US${x:,.0f}"
def rng(a, b, fn=money): return f"{fn(a)} to {fn(b)}"
def srng(k, key): v = [s[k][key] for s in D["seeds"]]; return min(v), max(v)


def fig_positions():
    """Pallet positions against forklift time per pallet and waiting, for the three set-ups."""
    x0, y0, w, bh, gap = 170, 40, 430, 30, 22
    mx = 4500; X = lambda v: x0 + v / mx * w
    s = ""
    yb = y0 + 3 * (bh + gap) - gap
    for t in range(0, mx + 1, 1000):
        s += f'<line x1="{X(t):.1f}" y1="{y0 - 8}" x2="{X(t):.1f}" y2="{yb + 6}" stroke="#E4E1D8"/>' + txt(X(t), yb + 22, f0(t), "middle", MUTED, 12)
    s += txt(x0 + w / 2, yb + 42, "Pallet positions (floor plus three beam levels)", "middle", NAVY, 12.5, True)
    for i, k in enumerate(K):
        y = y0 + i * (bh + gap); p = LY[k]["positions"]
        s += txt(x0 - 12, y + bh / 2 + 5, f'{NAME[k]} ({LY[k]["aisle"]} m)', "end", NAVY, 13, True)
        s += f'<rect x="{x0}" y="{y}" width="{X(p) - x0:.1f}" height="{bh}" fill="{COLR[k]}"/>'
        s += txt(X(p) + 8, y + bh / 2 + 5, f0(p), "start", NAVY, 13, True)
    return svg("Bar chart of pallet positions: " + ", ".join(f"{NAME[k]} {f0(LY[k]['positions'])}" for k in K) +
               ". Each step down in aisle width adds about 720 positions in the same building.", 700, yb + 50, s, 560)


def fig_wait():
    """Turret-truck and picker waiting at the aisle ends as volume grows (very narrow aisles), against the other two."""
    V = D["volume"]; x0, y0, w, h = 70, 30, 560, 230
    vmin, vmax = V[0]["orders"], V[-1]["orders"]
    ymax = math.ceil(max(v[k]["forkWait"] for v in V for k in K) / 5) * 5
    X = lambda v: x0 + (v - vmin) / (vmax - vmin) * w
    Y = lambda m: y0 + h - m / ymax * h
    s = ""
    for t in range(0, ymax + 1, 5):
        s += f'<line x1="{x0}" y1="{Y(t):.1f}" x2="{x0 + w}" y2="{Y(t):.1f}" stroke="#E4E1D8"/>' + txt(x0 - 8, Y(t) + 4, str(t), "end", MUTED, 12)
    for v in range(150, 601, 75): s += txt(X(v), y0 + h + 18, str(v), "middle", MUTED, 12)
    s += txt(x0 + w / 2, y0 + h + 40, "Orders a day", "middle", NAVY, 12.5, True)
    s += f'<text x="20" y="{y0 + h / 2}" transform="rotate(-90 20 {y0 + h / 2})" text-anchor="middle" font-size="12.5" font-weight="600" fill="{NAVY}">Truck minutes waiting a shift</text>'
    for k in K:
        pts = [(X(v["orders"]), Y(v[k]["forkWait"])) for v in V]
        s += f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{COLR[k]}" stroke-width="2.6"/>'
        s += "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3.2" fill="{COLR[k]}"/>' for a, b in pts)
    for i, k in enumerate(K):
        s += f'<rect x="{x0 + 14}" y="{y0 + 6 + i * 18}" width="12" height="12" rx="2" fill="{COLR[k]}"/>' + txt(x0 + 32, y0 + 16 + i * 18, NAME[k], fill=NAVY, fs=12.5, bold=True)
    v6 = V[-1]
    return svg("Line chart of minutes the pallet truck spends waiting in a shift against orders a day. Wide and narrow aisles stay under one minute; "
               f"very narrow aisles rise to {f0(v6['vna']['forkWait'])} minutes at {f0(v6['orders'])} orders, because the turret truck waits for pickers to leave an aisle.",
               700, 310, s, 560)


def fig_payback():
    """Payback range in years for narrow and very narrow aisles."""
    x0, y0, w, bh, gap = 170, 30, 360, 30, 26
    mx = math.ceil(max(OP[k]["payback"][1] for k in OP)); X = lambda v: x0 + v / mx * w
    s = ""
    yb = y0 + 2 * (bh + gap) - gap
    for t in range(0, mx + 1):
        s += f'<line x1="{X(t):.1f}" y1="{y0 - 8}" x2="{X(t):.1f}" y2="{yb + 6}" stroke="#E4E1D8"/>' + txt(X(t), yb + 22, str(t), "middle", MUTED, 12)
    s += txt(x0 + w / 2, yb + 42, "Years to pay back, against leasing the same positions", "middle", NAVY, 12.5, True)
    for i, k in enumerate(["redesign", "vna"]):
        y = y0 + i * (bh + gap); a, b = OP[k]["payback"]
        s += txt(x0 - 12, y + bh / 2 + 5, NAME[k], "end", NAVY, 13, True)
        s += f'<rect x="{X(a):.1f}" y="{y}" width="{X(b) - X(a):.1f}" height="{bh}" rx="3" fill="{COLR[k]}"/>'
        s += txt(X(b) + 8, y + bh / 2 + 5, f"{f1(a)} to {f1(b)} years", "start", NAVY, 13, True)
    return svg("Range bars of payback in years: narrow aisles " + f"{f1(OP['redesign']['payback'][0])} to {f1(OP['redesign']['payback'][1])}, very narrow aisles "
               f"{f1(OP['vna']['payback'][0])} to {f1(OP['vna']['payback'][1])}. The ranges come from the low and high published prices.", 700, yb + 50, s, 560)


def part3():
    for k in K: D["base"][k]["pos"] = LY[k]["positions"]
    rows = [
        ("Pallet positions", lambda r: f0(r["pos"])),
        ("Pick faces for 780 SKUs", lambda r: f0(r["pos"] / D["levels"])),
        ("Walk per order", lambda r: f'{f0(r["walkOrder"])}&nbsp;m'),
        ("Picker-hours a day", lambda r: f1(r["pickHoursDay"])),
        ("Picker time giving way or waiting at an aisle end", lambda r: f'{f0(r["split"]["wait"] * 60)}&nbsp;min'),
        ("Truck time per pallet put away", lambda r: f'{f2(r["forkCycle"])}&nbsp;min'),
        ("Truck time waiting in the shift", lambda r: f'{f1(r["forkWait"])}&nbsp;min'),
        ("Dock-to-stock time (average)", lambda r: f'{f0(r["dts"])}&nbsp;min'),
    ]
    trs = "".join(f'<tr><td>{lab}</td>' + "".join(f'<td class="num">{fn(D["base"][k])}</td>' for k in K) + '</tr>' for lab, fn in rows)
    v6 = D["volume"][-1]; v4 = [v for v in D["volume"] if v["orders"] == 400][0]
    pw = {k: srng(k, "pickHoursDay") for k in K}
    CROSS = min(v["orders"] for v in D["volume"] if v["vna"]["pickHoursDay"] > v["redesign"]["pickHoursDay"])
    GAP = max(sd["wide"]["pickHoursDay"] - sd["vna"]["pickHoursDay"] for sd in D["seeds"])
    ORDER = all(sd["wide"]["pickHoursDay"] > sd["redesign"]["pickHoursDay"] > sd["vna"]["pickHoursDay"] for sd in D["seeds"])
    assert ORDER
    sq = EC["sqftPerPos"]; rp = EC["rentPerPosYear"]; rent = C["netRent"] + C["addRent"]
    oN, oV = OP["redesign"], OP["vna"]
    shared = 780 - LY["wide"]["faces"]
    lab_w = lambda k: D["base"][k]["pickHoursDay"] * P["wage"] * P["days"] + D["base"][k]["forkCycle"] / 60 * D["base"][k]["putaway"] * P["wage"] * P["days"]
    cost_rows = [
        ("Added pallet positions", lambda o, k: f0(o["add"])),
        ("New racking (narrow: added positions only; very narrow: every position)", lambda o, k: rng(LY[k]["positions"] * C["fx"] * C["rackVNA"][0], LY[k]["positions"] * C["fx"] * C["rackVNA"][1]) if k == "vna" else rng(o["add"] * C["fx"] * C["rack"][0], o["add"] * C["fx"] * C["rack"][1])),
        ("Taking down and re-erecting the existing racks", lambda o, k: "None" if k == "vna" else rng(LY["wide"]["positions"] * C["fx"] * C["rack"][0] * C["move"][0], LY["wide"]["positions"] * C["fx"] * C["rack"][1] * C["move"][1])),
        ("Truck", lambda o, k: rng(C["fx"] * (C["turret"] if k == "vna" else C["reach"])[0], C["fx"] * (C["turret"] if k == "vna" else C["reach"])[1])),
        ("Superflat floor in the rack zone (guide wire not included)", lambda o, k: rng(C["fx"] * C["floor"][0] * C["rackZoneM2"] * 10.7639, C["fx"] * C["floor"][1] * C["rackZoneM2"] * 10.7639) if k == "vna" else "None"),
        ("<strong>Total one-off cost</strong>", lambda o, k: f'<strong>{rng(*o["capex"])}</strong>'),
        ("Cost per added position", lambda o, k: rng(*o["perPos"], fn=lambda x: f"${x:,.0f}")),
        ("Space you would otherwise lease", lambda o, k: f'{f0(o["leaseSqft"])}&nbsp;sq&nbsp;ft'),
        ("Rent avoided a year", lambda o, k: money(o["rentAvoided"])),
        ("Picking and truck time saved a year against wide aisles", lambda o, k: money(o["labour"])),
        ("<strong>Payback</strong>", lambda o, k: f'<strong>{f1(o["payback"][0])} to {f1(o["payback"][1])} years</strong>'),
    ]
    ctrs = "".join(f'<tr><td>{lab}</td>' + "".join(f'<td class="num">{fn(OP[k], k)}</td>' for k in ("redesign", "vna")) + '</tr>' for lab, fn in cost_rows)
    body = f"""{CSS}
<p><a href="{WL2}.html">Part&nbsp;2</a> found that, laid out well, the U-shape, straight-through and L-shape pick at almost the same cost. This part keeps the U-shape and asks the next question every growing warehouse meets: when the racks are full, do you narrow the aisles to fit more pallets in, or lease more space?</p>
<p>Narrower aisles mean more pallet positions in the same building, but a different truck, more cost up front and less room for the people working in the aisles. The trade-off is density against access. This part runs three aisle widths through the same shift and prices the extra positions against Metro Vancouver rents.</p>
<h2>Three aisle widths, three trucks</h2>
<p>The aisle width is set by the truck that has to turn or work in it. Aisles for a standard counterbalance truck are usually about 12&nbsp;ft (3.7&nbsp;m); reach trucks and other narrow-aisle trucks work in about 9 to 10&nbsp;ft (2.7 to 3&nbsp;m); very-narrow-aisle (VNA) trucks fit aisles of about 6&nbsp;ft (1.8&nbsp;m) or less.</p>
<p class="oee-cap">Table 1. The three set-ups</p>
<table>
<tr><th>Set-up</th><th>Aisle</th><th>Truck</th><th>How it stores a pallet</th><th>What else it needs</th></tr>
<tr><td>Wide aisles</td><td>4&nbsp;m</td><td>Counterbalance truck</td><td>Drives in, turns 90 degrees to face the rack, lifts</td><td>Nothing special; the same truck can also load trailers</td></tr>
<tr><td>Narrow aisles</td><td>3&nbsp;m</td><td>Reach truck</td><td>Turns in the aisle in less room, reaches the forks out</td><td>A trained operator; it is not built for trailers</td></tr>
<tr><td>Very narrow aisles</td><td>2&nbsp;m</td><td>Wire-guided turret truck</td><td>Drives straight down the aisle and swivels its forks to either side; never turns in the aisle</td><td>A superflat floor in the aisles, a guide wire or rail, VNA-tolerance racking, and rules that keep people out of an aisle while the truck is in it. A man-down turret truck can also fetch pallets from staging, but loses time each trip leaving and rejoining the guide wire</td></tr>
</table>
<h2>The same building, three ways</h2>
<p>All three use the Part&nbsp;2 U-shape: the same 72 by 52&nbsp;m building, three receiving and two shipping doors, staging, packing, crew, 300 orders and 14 inbound trucks. The racks run across the building with front and back cross-aisles, and the busiest SKUs sit nearest packing. Only the aisle width changes, and with it the number of rack rows:</p>
<ul>
<li><strong>Wide aisles (4&nbsp;m):</strong> {LY["wide"]["aisles"]} aisles, {f0(LY["wide"]["faces"])} pick faces. That is fewer than the 780 SKUs, so the {f0(shared)} slowest SKUs share a face, two to a pallet position.</li>
<li><strong>Narrow aisles (3&nbsp;m):</strong> the Part&nbsp;1 and 2 layout. {LY["redesign"]["aisles"]} aisles, {f0(LY["redesign"]["faces"])} pick faces: one per SKU with some to spare.</li>
<li><strong>Very narrow aisles (2&nbsp;m):</strong> {LY["vna"]["aisles"]} aisles, {f0(LY["vna"]["faces"])} pick faces. The turret truck and pickers never share an aisle: whoever arrives second waits at the aisle end.</li>
</ul>
<p>All three keep the same clear height: a floor position and three beam levels. In a taller building VNA gains more, because turret trucks lift higher than counterbalance trucks.</p>
{fig(fig_positions(), 1, "Pallet positions in the same building. Each step down in aisle width adds about 720 positions.")}
<h2>The Layout Lab</h2>
<p>The simulator runs the three set-ups through the same shift. Pick <em>All three</em> to compare them or one set-up to see it larger, and switch between the 2D plan and the 3D view. In the very narrow aisles, watch for amber rings at the aisle ends where pickers and the turret truck wait for each other.</p>
<figure>
<iframe id="wl-sim" src="{SIM}#embed&amp;s=p3" title="Warehouse Layout Lab: wide, narrow and very narrow aisles in the same building, simulated side by side" loading="lazy" style="width:100%;height:4030px;border:0;display:block"></iframe>
<figcaption>Figure 2. The Warehouse Layout Lab with three aisle widths. The animation replays the shift 12 times faster than life; the table is the whole simulated shift.</figcaption>
</figure>
<p class="oee-hint"><a href="{SIM}?s=p3">Open the Layout Lab on its own page</a> for a larger view.</p>
<h2>What the simulation shows</h2>
<p class="oee-cap">Table 2. One shift at {f0(Wd["orders"])} orders a day</p>
<table>
<tr><th>Measure</th>{"".join(f'<th class="num">{NAME[k]}</th>' for k in K)}</tr>
{trs}
</table>
<ul>
<li><strong>Picking barely changes.</strong> The busy SKUs sit near packing in all three, so pickers need {f1(Wd["pickHoursDay"])}, {f1(Nr["pickHoursDay"])} and {f1(Vn["pickHoursDay"])} hours a day. Across ten other simulated days the order never changed, and wide aisles were never more than {f2(GAP)} picker-hours a day behind very narrow aisles. At this volume more faces even help a little: more of the busy SKUs fit in the front bays. From {f0(CROSS)} orders a day, with more pickers waiting at aisle ends, very narrow aisles fall behind narrow aisles. In wide aisles the shared faces push the slowest SKUs to the back, which costs little because they are rarely picked.</li>
<li><strong>Narrow aisles put away fastest.</strong> The reach truck needs {f2(Nr["forkCycle"])} minutes a pallet. The counterbalance truck needs {f2(Wd["forkCycle"])}: it has to turn in the aisle to face the rack. Dock-to-stock is {f0(Nr["dts"])} minutes against {f0(Wd["dts"])}.</li>
<li><strong>Very narrow aisles cost time at the aisle ends.</strong> The turret truck is set to store a pallet 10 seconds faster than a reach truck, but each trip off the guide wire to staging costs time, and it cannot enter an aisle with a picker in it. It needs {f2(Vn["forkCycle"])} minutes a pallet and waits {f1(Vn["forkWait"])} minutes in the shift. Pickers wait {f0(Vn["split"]["wait"] * 60)} minutes in total, against about {f0(Nr["split"]["wait"] * 60)} in the other set-ups.</li>
</ul>
{fig(fig_wait(), 3, "Minutes the pallet truck waits in a shift as volume grows. In very narrow aisles people and the turret truck take turns, and the waiting grows with the traffic.")}
<p>The waiting grows with volume. At {f0(v4["orders"])} orders a day, with more pickers in the aisles, the turret truck waits {f1(v4["vna"]["forkWait"])} minutes a shift; at {f0(v6["orders"])}, {f1(v6["vna"]["forkWait"])} minutes, while the other two stay under a minute, and pickers lose {f0(v6['vna']['split']['wait'] * 60)} minutes in total waiting to get into an aisle. The more people pick from the ground level of VNA aisles, the more they and the truck get in each other's way, which is why many VNA sites keep their fast movers in a separate wide-aisle pick zone.</p>
<h2>What the extra positions cost</h2>
<p>The published price ranges below are in US dollars and converted at {C["fx"]:.2f} Canadian dollars per US dollar (mid-November 2026). Treat them as a first screen, not a quote.</p>
<p class="oee-cap">Table 3. Published price ranges used</p>
<table>
<tr><th>Item</th><th>Published range</th><th>Source</th></tr>
<tr><td>Selective pallet racking, new</td><td>{usd(C["rack"][0])} to {usd(C["rack"][1])} a pallet position</td><td>Bastian Solutions and TranSystems' rules of thumb quoted by Modern Materials Handling ($50 to $75); a 2026 buyer's guide ($50 to $120)</td></tr>
<tr><td>VNA racking (tighter tolerances), for every position</td><td>{usd(C["rackVNA"][0])} to {usd(C["rackVNA"][1])} a pallet position</td><td>Supplier price guide</td></tr>
<tr><td>Counterbalance truck, new</td><td>US$15,000 to US$50,000</td><td>Municibid pricing guide</td></tr>
<tr><td>Reach truck, new</td><td>{usd(C["reach"][0])} to {usd(C["reach"][1])}</td><td>Municibid pricing guide</td></tr>
<tr><td>Turret truck, new</td><td>{usd(C["turret"][0])} to {usd(C["turret"][1])}</td><td>Our estimate, not a published price: Modern Materials Handling says narrow-aisle trucks cost up to twice a counterbalance truck and advanced turret trucks double that again. Get quotes</td></tr>
<tr><td>Superflat floor in VNA aisles</td><td>US$1.50 to US$8 a sq&nbsp;ft (2003), used here as US${C["floor"][0]:.2f} to US${C["floor"][1]:.2f} in today's money</td><td>Published 2003 figures for grinding (lowest) to replacing the floor (highest), raised by 75%; get a floor survey and quote</td></tr>
<tr><td>Industrial rent, Metro Vancouver</td><td>C${C["netRent"]:.2f} net plus about C${C["addRent"]:.2f} additional rent a sq&nbsp;ft a year</td><td>CBRE Q3 2026 net asking rate; Avison Young additional rent</td></tr>
</table>
<p>To compare like with like, the extra positions are priced against leasing the same storage elsewhere. The wide-aisle rack zone holds one pallet position for every {f1(sq)}&nbsp;sq&nbsp;ft. At C${rent:.2f} a sq&nbsp;ft a year, one leased position costs</p>
{eq(r"R = a \times r = " + f"{sq:.2f}" + r"\ \text{sq ft} \times \$" + f"{rent:.2f}" + r" \approx \$" + tn(f"{rp:,.0f}") + r"\ \text{a position a year}")}
<p>where {im("a")} is the floor area per position and {im("r")} the gross rent. That counts the rack floor only, with no second dock, staff or shuttle trucks, so it understates the real cost of a second building. The payback is then</p>
{eq(r"\text{Payback} = \frac{\text{One-off cost}}{n \times R + \Delta L}")}
<p>where {im("n")} is the number of added positions and {im(r"\Delta L")} the labour saved a year against wide aisles (picking plus put-away time at ${f0(P["wage"])} an hour, {f0(P["days"])} days a year). For narrow aisles the existing racks are reused; taking them down and re-erecting them is our assumption at 25% to 40% of their new price. For very narrow aisles all racking is new, to VNA tolerances. The payback is at 300 orders a day with one truck; from 400 orders every set-up needs a second truck, and for very narrow aisles that second truck is another turret truck at {rng(C['fx'] * C['turret'][0], C['fx'] * C['turret'][1])}, not counted here.</p>
<p class="oee-cap">Table 4. Moving from wide aisles to narrow or very narrow aisles (Canadian dollars)</p>
<table>
<tr><th>Item</th><th class="num">Narrow aisles</th><th class="num">Very narrow aisles</th></tr>
{ctrs}
</table>
{fig(fig_payback(), 4, "Payback against leasing the same number of pallet positions, from the low and high ends of the published prices.")}
<ul>
<li><strong>Narrow aisles are the cheaper step.</strong> {f0(oN["add"])} more positions for {rng(*oN["perPos"], fn=lambda x: f"${x:,.0f}")} each, paid back in {f1(oN["payback"][0])} to {f1(oN["payback"][1])} years against leasing about {f0(oN["leaseSqft"])}&nbsp;sq&nbsp;ft.</li>
<li><strong>Very narrow aisles add twice the positions at a higher price each.</strong> {f0(oV["add"])} more positions at {rng(*oV["perPos"], fn=lambda x: f"${x:,.0f}")} each, because every position needs new VNA racking, and the turret truck and the floor come on top. Payback is {f1(oV["payback"][0])} to {f1(oV["payback"][1])} years.</li>
<li><strong>The time saving is small.</strong> About {money(oN["labour"])} and {money(oV["labour"])} a year: the case for narrower aisles is the space, not the speed. Those are minutes of people already paid for the shift, so treat them as capacity rather than cash.</li>
<li><strong>The payback is real only if you need the positions.</strong> Rent avoided is the whole saving. If the racks are not full most of the year, or slotting and clearing dead stock would free enough space (see <a href="{W1}.html">cube utilization and slotting</a>), narrower aisles buy capacity you pay for and do not use.</li>
</ul>
<h2>What the shift does not show</h2>
<ul>
<li><strong>One truck per aisle.</strong> VNA trucks are made for one aisle width; if the only turret truck is down, nothing else can work those aisles.</li>
<li><strong>Operators.</strong> Reach and turret trucks need more training, and experienced VNA operators are harder to find and keep.</li>
<li><strong>Safety rules.</strong> VNA sites keep pedestrians out of an aisle while the truck works in it, usually with gates, sensors or a permit system. Narrow aisles shared by people and reach trucks need clear give-way rules.</li>
<li><strong>Racks in Vancouver.</strong> Seismic design and anchoring raise rack costs above the published averages, and moving racks needs an engineer's sign-off.</li>
<li><strong>Fire and sprinklers.</strong> More pallets and narrower flue spaces can change sprinkler requirements; check with your fire protection engineer before narrowing aisles.</li>
<li><strong>Lease terms.</strong> Leasing more space is flexible; a VNA floor and guide wire stay with the building.</li>
</ul>
<p class="oee-cap">Table 5. Choosing an aisle width (rules of thumb; the simulation informs the second and third rows)</p>
<table>
<tr><th>If this is true</th><th>Start with</th></tr>
<tr><td>The racks are not full most of the year</td><td>Keep the aisles; fix slotting and dead stock first</td></tr>
<tr><td>You need up to about a quarter more positions and pick from the racks</td><td>Narrow aisles with reach trucks</td></tr>
<tr><td>You need the most positions, with few people picking from the same aisles</td><td>Very narrow aisles, with fast movers in a separate wide-aisle pick zone</td></tr>
<tr><td>The building is tall (over about 9&nbsp;m clear) and the floor is new or good</td><td>VNA gains more; ask for a floor flatness survey</td></tr>
<tr><td>You expect to move within a few years</td><td>Lease space or narrow the aisles, rather than invest in a VNA floor</td></tr>
</table>
<h2>How to check your own building</h2>
<ol>
<li><strong>Measure how full the racks are,</strong> month by month for a year. Narrower aisles pay only for positions you would otherwise rent.</li>
<li><strong>Count the positions each width gives you,</strong> on a scale plan of your own building, with the clear height and the columns.</li>
<li><strong>Price the space you would lease instead,</strong> including additional rent, shuttling between buildings and a second set of staff.</li>
<li><strong>Get quotes,</strong> for racks (with seismic design), trucks, and, for VNA, a floor survey.</li>
<li><strong>Count the people in the aisles.</strong> If many picks are from the ground level of the racks, plan where pickers will work while the turret truck is in an aisle.</li>
</ol>
<h2>What the model leaves out</h2>
<ul>
<li>One shift with one fixed seed per day, single-order case picking, one pallet truck (two from 400 orders a day).</li>
<li>The same building height for all three; truck lift heights and speeds at height are not modelled.</li>
<li>Truck differences are fixed times, not results: the counterbalance truck takes 15 seconds longer to store a pallet, the turret truck 10 seconds less, plus 20 seconds a trip to leave and rejoin the guide wire.</li>
<li>At 350 orders a day, just below the switch to two trucks, all three set-ups leave some inbound pallets not put away by 15:00.</li>
<li>No replenishment of pick faces, no returns, no breakdowns.</li>
<li>Prices are published ranges in US dollars at one exchange rate, with no resale value for the old truck and no financing cost.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>In this building, 3&nbsp;m aisles hold {f0(oN["add"])} more pallet positions than 4&nbsp;m aisles, and 2&nbsp;m aisles {f0(oV["add"])} more.</li>
<li>Picking cost hardly depends on aisle width when the fast movers are near packing. Very narrow aisles add waiting at the aisle ends, which grows with volume.</li>
<li>Against Metro Vancouver rents, narrow aisles paid back in about {f1(oN["payback"][0])} to {f1(oN["payback"][1])} years and very narrow aisles in about {f1(oV["payback"][0])} to {f1(oV["payback"][1])} years, but only if the extra positions would otherwise be leased.</li>
<li>Check how full the racks really are before you pay for density.</li>
</ul>
<p>Earlier in this series: <a href="{WL1}.html">Part&nbsp;1</a>, what a bad layout costs, and <a href="{WL2}.html">Part&nbsp;2</a>, choosing a flow pattern. Related: <a href="{W1}.html">cube utilization and slotting</a> and <a href="{W3}.html">the dock door bottleneck</a> in the warehouse operations series.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://www.logisticsmgmt.com/article/jumping_on_the_narrow_aisle_trend/Racks" rel="noopener" target="_blank">Logistics Management: Jumping on the narrow aisle trend</a> (aisle widths by truck type)</li>
<li><a href="https://www.mmh.com/article/jumping_on_the_narrow_aisle_trend" rel="noopener" target="_blank">Modern Materials Handling: Jumping on the narrow aisle trend</a> (narrow-aisle and turret truck prices against counterbalance trucks)</li>
<li><a href="https://www.mmh.com/article/lift_truck_tips_avoiding_a_tight_spot_in_narrow_aisles" rel="noopener" target="_blank">Modern Materials Handling: Avoiding a tight spot in narrow aisles</a> (VNA trucks are specific to their aisle width)</li>
<li><a href="https://www.catlifttruck.com/blog/very-narrow-aisle-vna-applications-everything-you-need-know" rel="noopener" target="_blank">Cat Lift Trucks: Very narrow aisle applications</a> (guidance, one truck an aisle, no pedestrians while the truck works)</li>
<li><a href="https://www.bastiansolutions.com/blog/how-much-does-pallet-racking-cost-" rel="noopener" target="_blank">Bastian Solutions: How much does pallet racking cost?</a> and <a href="https://www.mmh.com/article/pallet_rack_basics_behind_the_backbone/Equipment_Report" rel="noopener" target="_blank">Modern Materials Handling: Pallet rack basics</a> (selective rack per position)</li>
<li><a href="https://mh-usa.com/?p=404809" rel="noopener" target="_blank">The complete guide to pallet rack systems: types, costs and installation (2026)</a> (selective rack $50 to $120 a position)</li>
<li><a href="https://directindustry.com/prod/cat-lift-trucks/product-19271-2606737.html" rel="noopener" target="_blank">Cat man-down VNA truck NTD13-15N3</a> (a man-down turret truck that also carries pallets to and from the racking area)</li>
<li><a href="https://www.hedashelving.com/info/cost-of-new-pallet-racking-system-102881929.html" rel="noopener" target="_blank">Heda Shelving: Cost of a new pallet racking system</a> (VNA racking per position)</li>
<li><a href="https://municibid.com/blog/comprehensive-guide-to-forklift-pricing" rel="noopener" target="_blank">Municibid: Comprehensive guide to forklift pricing</a> (counterbalance and reach truck prices)</li>
<li><a href="https://www.wealthmanagement.com/investment-news/the-skinny-on-super-flat-floors" rel="noopener" target="_blank">The skinny on super-flat floors</a> (2003 floor grinding, overlay and replacement costs)</li>
<li><a href="https://www.cbre.com/insights/figures/vancouver-industrial-figures-q3-2026" rel="noopener" target="_blank">CBRE: Vancouver industrial figures Q3 2026</a> (average net asking rate) and <a href="https://www.avisonyoung.ca/web/vancouver/industrial-market-report" rel="noopener" target="_blank">Avison Young: Metro Vancouver industrial market report</a> (additional rent)</li>
</ul>
{NOTE}{mathjs()}
<script src="../assets/js/wl1.js" defer></script>"""
    body = nowrap(body, [(1, 0, 26), (2, 0, 40)])
    return dict(slug=WL3, title="Wide, Narrow or Very Narrow Aisles? Warehouse Density Against Access",
                desc="Three aisle widths in the same warehouse, simulated and priced: what more pallet positions cost against leasing space in Metro Vancouver.",
                cats=["operational-efficiency", "inventory-management"], tags=["warehouse layout", "narrow aisle", "very narrow aisle", "reach truck", "pallet racking cost", "warehouse simulation"],
                body=body, date=DATE, author="Quak Foo Lee", read="11 min read", series=SER(3), cover_label="Warehouse layout",
                related=[WL2, WL1, W1])


if __name__ == "__main__":
    a = part3()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])}\n")
