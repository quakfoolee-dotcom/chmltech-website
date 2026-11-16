"""Warehouse operations series for Insights (V5.31). Part 1: cube utilization and slotting.

Every number in the text comes from wh_model.py, which also writes the data behind the 3D warehouse in Figure 2
(content/articles/fig3d/wh.html, script assets/js/wh3d.js).

Usage:  python3 content/articles/wh_articles.py
        python3 content/gen/add_article.py were-out-of-space-or-are-we-warehouse-cube-utilization-and-slotting
        python3 content/gen/series_labels.py
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import js3d, nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, PURPLE, MUTED, LINE, PALE, eq, im, tn, mathjs
import wh_model as W

DATE = "2026-11-15"
W1 = "were-out-of-space-or-are-we-warehouse-cube-utilization-and-slotting"
W2 = "pickers-walk-half-the-day-pick-methods-and-pick-paths"
SER = lambda n: {"name": "Warehouse operations series", "part": n, "of": 8}
ABC1, ABC2, SS1 = "abc-inventory-analysis", "abc-analysis-for-manufacturers", "setting-safety-stock"
OEE1 = "what-oee-really-measures"
NOTE = ('<p class="oee-note"><em>The distributor, its building, inventory and costs in this series are an illustrative example. '
        'The benchmarks are published industry figures. Changes to racking need the rack manufacturer\'s or a rack engineer\'s '
        'confirmation, and sprinkler clearances need your fire protection contractor and the authority having jurisdiction.</em></p>')

M = W.run(); S = M["S"]; I = M["info"]
A0, A1, A2, A3, A4 = S
f0 = lambda x: f"{x:,.0f}"
f1 = lambda x: f"{x:,.1f}"
pc = lambda x: f"{x * 100:.0f}%"
SQFT = 10.7639
BLD_FT2 = W.BLD_X * W.BLD_Z * SQFT
GAIN = A4["free"] - A0["free"]                                         # positions recovered
DENS = W.RACK_ZONE_M2 / A0["positions"]                                # m2 of rack zone per position as built
EQ_FT2 = GAIN * DENS * SQFT                                            # rack-zone floor that would hold them as built
RENT, ADD = 14.77, 5.00                                                # $/sq ft/yr: CBRE Q3 2026 national net asking; assumed additional rent
LEASE = EQ_FT2 * (RENT + ADD)
# one-time cost of the four fixes (assumptions, stated in the table)
WAGE, BEAMS, ENG = 40.0, 150.0, 6000.0
BAYS_ALL = W.ROWS * W.BAYS
C_BEAM_MAT = BAYS_ALL * BEAMS
H_BEAM = BAYS_ALL * 1.5 + A0["occupied"] * 2 * 4 / 60                  # re-beam each bay, and unload and reload its pallets
H_COMB = I["merged"] * 10 / 60
H_DEAD = I["dead"] * 4 / 60
H_SLOT = I["moves4"] * 5 / 60
C_LAB = (H_BEAM + H_COMB + H_DEAD + H_SLOT) * WAGE
C_ALL = C_BEAM_MAT + ENG + C_LAB
GROW = 0.10
import math
YEARS = math.log(0.85 * A4["positions"] / A4["occupied"]) / math.log(1 + GROW)
WALK_CUT = 1 - A4["walk"] / A0["walk"]
TALL = sum(1 for p in M["pallets"] if p["h"] > 1.6)


def fig_bay():
    """Bay elevation: as-is (4 levels at 2.0 m) and re-set (5 levels), with each load and the air above it."""
    sc = 30.0; base = 330; s = ""
    def y(m): return base - m * sc
    loads = [[1.25, 0.45], [1.30, 1.15], [0.55, 1.35], [1.20, 1.28]]
    loads5 = [[1.25, 1.75], [1.30, 0.45], [0.55, 1.20], [1.28, 1.22], [1.25, 1.30]]
    def bay(x0, levels, ld, title):
        w = 200; out = txt(x0 + w / 2, 18, title, "middle", NAVY, 14, True)
        out += f'<rect x="{x0 - 6}" y="{y(W.CLEAR_H)}" width="6" height="{W.CLEAR_H * sc}" fill="#9AB0C8"/><rect x="{x0 + w}" y="{y(W.CLEAR_H)}" width="6" height="{W.CLEAR_H * sc}" fill="#9AB0C8"/>'
        for k, lv in enumerate(levels):
            top = (levels[k + 1] - W.BEAM) if k + 1 < len(levels) else W.MAX_LOAD_TOP
            if k: out += f'<rect x="{x0 - 6}" y="{y(lv)}" width="{w + 12}" height="{W.BEAM * sc:.1f}" fill="{ORANGE}"/>'
            base_k = lv + (W.BEAM if k else 0)
            for j in range(2):
                h = ld[k][j]; px = x0 + 8 + j * 96; pw = 88
                out += f'<rect x="{px}" y="{y(top):.1f}" width="{pw}" height="{(top - base_k - h) * sc:.1f}" fill="url(#air)" stroke="#C9D3DE" stroke-dasharray="3 3"/>'
                out += f'<rect x="{px}" y="{y(base_k + h):.1f}" width="{pw}" height="{h * sc:.1f}" rx="2" fill="{"#C9A46A" if h > 0.9 else "#E3C58E"}" stroke="#8A6A3A"/>'
                out += f'<rect x="{px}" y="{y(base_k + 0.14):.1f}" width="{pw}" height="{0.14 * sc:.1f}" fill="#8A6A3A"/>'
        fill = sum(sum(r) for r in ld) / sum(2 * (((levels[k + 1] - W.BEAM) if k + 1 < len(levels) else W.MAX_LOAD_TOP) - (levels[k] + (W.BEAM if k else 0))) for k in range(len(levels)))
        out += txt(x0 + w / 2, base + 22, f"{len(levels) * 2} positions · {fill * 100:.0f}% of the opening filled", "middle", MUTED, 12.5)
        return out
    s += ('<defs><pattern id="air" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
          '<rect width="8" height="8" fill="#F3F6FA"/><line x1="0" y1="0" x2="0" y2="8" stroke="#DCE4EE" stroke-width="3"/></pattern></defs>')
    s += f'<line x1="20" y1="{base}" x2="700" y2="{base}" stroke="{NAVY}" stroke-width="1.5"/>'
    s += f'<line x1="60" y1="{y(W.MAX_LOAD_TOP)}" x2="660" y2="{y(W.MAX_LOAD_TOP)}" stroke="{RED}" stroke-dasharray="5 4"/>'
    s += txt(360, 44, f"Highest load top: {W.MAX_LOAD_TOP:.2f} m (18 in below the sprinklers)", "middle", RED, 12.5)
    s += bay(100, W.LEVELS_ASIS, loads, "As-is: 4 levels, 2.0 m beam pitch")
    s += bay(420, W.LEVELS_NEW, loads5, "Re-set: 5 levels, 1.7 m pitch")
    s += txt(360, 190, "→", "middle", GREEND, 34, True)
    s += f'<rect x="300" y="{base + 34}" width="12" height="12" fill="url(#air)" stroke="#C9D3DE"/>' + txt(318, base + 44, "Air above the load", fill=NAVY, fs=12)
    s += f'<rect x="430" y="{base + 34}" width="12" height="12" fill="#E3C58E" stroke="#8A6A3A"/>' + txt(448, base + 44, "Partial pallet", fill=NAVY, fs=12)
    return svg("Elevation of one pallet-rack bay before and after the beams are re-set. As built, four levels at a 2.0 metre beam pitch hold "
               "loads of about 1.3 metres, so the top 0.7 metres of most openings is air, and a partial pallet leaves most of its opening empty. "
               "Re-set at a 1.7 metre pitch, with the floor level kept 2.0 metres high for tall loads, the same height holds five levels, "
               "and the top load stays below the sprinkler clearance line.", 720, 382, s, 560)


def fig_bridge():
    steps = [("As-is", A0["free"], None), ("Re-set beam heights", A1["free"] - A0["free"], BLUE), ("Combine partial pallets", A2["free"] - A1["free"], GREEN),
             ("Clear dead stock", A3["free"] - A2["free"], PURPLE), ("Re-slot fast movers", 0, ORANGE), ("After the four fixes", A4["free"], None)]
    x0, sc = 200, 330 / A4["free"]; s = ""; run = 0
    for i, (lab, v, c) in enumerate(steps):
        yy = 20 + i * 44
        s += txt(x0 - 12, yy + 20, lab, "end", NAVY, 13, i in (0, 5))
        if c is None:
            s += f'<rect x="{x0}" y="{yy + 4}" width="{v * sc:.1f}" height="26" rx="3" fill="{NAVY}"/>'; run = v
            s += txt(x0 + v * sc + 8, yy + 22, f"{f0(v)} free positions", fill=NAVY, fs=13, bold=True)
        elif v:
            s += f'<rect x="{x0 + run * sc:.1f}" y="{yy + 4}" width="{v * sc:.1f}" height="26" rx="3" fill="{c}"/>'
            s += txt(x0 + (run + v) * sc + 8, yy + 22, f"+{f0(v)}", fill=NAVY, fs=13, bold=True); run += v
        else:
            s += txt(x0 + 10, yy + 22, f"No new positions · walk per pick −{pc(WALK_CUT)}", fill=NAVY, fs=13, bold=True)
    s += f'<line x1="{x0}" y1="14" x2="{x0}" y2="{20 + 6 * 44}" stroke="{NAVY}"/>'
    return svg(f"Bridge of free pallet positions. As-is there are {A0['free']} free positions. Re-setting the beams adds {A1['free'] - A0['free']}, combining partial pallets "
               f"frees {A2['free'] - A1['free']} and clearing dead stock frees {A3['free'] - A2['free']}. Re-slotting adds no positions but cuts the walk per pick by "
               f"{WALK_CUT * 100:.0f} percent. The result is {A4['free']} free positions.", 720, 296, s, 560)


def figure_markup():
    data = json.dumps(W.figure_data(M), separators=(",", ":"))
    return f"""<p>Figure 2 is the example distributor's pallet-rack zone in 3D, built from the same data as the tables. It steps through the four fixes on its own, about fifteen seconds each. Pick a step to stay on it, colour the pallets by how full their opening is or by how often they are picked, and drag to turn the building.</p>
<figure class="wh3d" id="wh3d">
<div class="wh3d-box">
<div class="wh3d-stage">
<canvas role="img" aria-label="3D model of the example distributor's pallet-rack zone: ten rows of selective pallet rack, twenty bays long, with five aisles, the dock doors and staging area at the front, and small-parts shelving and packing beside the racks. Each pallet is drawn at its real load height and coloured by how much of its rack opening it fills, or by how often it is picked."></canvas>
<svg class="wh3d-lines" aria-hidden="true"></svg>
<span class="wh3d-drag" aria-hidden="true">Drag to turn</span>
<span class="wh3d-chip" id="wh3d-chip">As-is</span>
<p class="wh3d-nogl" id="wh3d-nogl" hidden>This browser cannot show the 3D model. The steps below still update the numbers.</p>
</div>
<div class="wh3d-panel">
<div class="wh3d-steps" role="group" aria-label="Fixes, applied in order">
<button type="button" class="wh3d-step" data-s="0" aria-pressed="true"><b>0</b><span>As-is</span></button>
<button type="button" class="wh3d-step" data-s="1" aria-pressed="false"><b>1</b><span>Re-set beam heights</span></button>
<button type="button" class="wh3d-step" data-s="2" aria-pressed="false"><b>2</b><span>Combine partial pallets</span></button>
<button type="button" class="wh3d-step" data-s="3" aria-pressed="false"><b>3</b><span>Clear dead stock</span></button>
<button type="button" class="wh3d-step" data-s="4" aria-pressed="false"><b>4</b><span>Re-slot fast movers</span></button>
</div>
<div class="wh3d5-tour" id="wh3d-tour" aria-hidden="true"><b><i></i></b><span></span></div>
<div class="wh3d-cells">
<div class="wh3d-cell wh3d-key"><span class="k">Positions occupied</span><strong id="wh3d-loc">{pc(A0["loc_util"])}</strong></div>
<div class="wh3d-cell wh3d-key"><span class="k">Opening filled (cube)</span><strong id="wh3d-cube">{pc(A0["cube_occ"])}</strong></div>
<div class="wh3d-cell"><span class="k">Free positions</span><strong id="wh3d-free">{f0(A0["free"])} of {f0(A0["positions"])}</strong></div>
<div class="wh3d-cell"><span class="k">Pallets in the racks</span><strong id="wh3d-pal">{f0(A0["occupied"])}</strong></div>
<div class="wh3d-cell"><span class="k">Walk per pick</span><strong id="wh3d-walk">{f0(A0["walk"])} m</strong></div>
<div class="wh3d-cell"><span class="k">Picks within easy reach</span><strong id="wh3d-easy">{pc(A0["easy"])}</strong></div>
</div>
<p class="wh3d-say" id="wh3d-say" aria-live="polite">As-is: {pc(A0["loc_util"])} of the positions hold a pallet, so the building feels full, yet the loads fill only {pc(A0["cube_occ"])} of the openings they sit in.</p>
<div class="wh3d-last"><div class="wh3d-mode" role="group" aria-label="Colour the pallets by"><span>Colour by</span><button type="button" class="wh3d-btn" id="wh3d-m-fill" aria-pressed="true">Opening filled</button><button type="button" class="wh3d-btn" id="wh3d-m-abc" aria-pressed="false">Pick speed</button></div>
<ul class="wh3d-legend" id="wh3d-leg-fill" aria-hidden="true"><li><i class="grad"></i>Share of the opening filled, 0 to 100%</li></ul>
<ul class="wh3d-legend" id="wh3d-leg-abc" aria-hidden="true" hidden><li><i style="background:#FF8A3D"></i>A, fast</li><li><i style="background:#3FA7F5"></i>B</li><li><i style="background:#9AA8BA"></i>C, slow</li><li><i style="background:#B07CFF"></i>No picks in 12 months</li></ul>
<button type="button" class="wh3d-btn wh3d-small" id="wh3d-names" aria-pressed="true">Area names</button></div>
</div>
</div>
<figcaption>Figure 2. The example distributor's pallet-rack zone: {W.ROWS} rows of {W.BAYS} bays, two pallets a bay. The fixes apply in order and build on each other. Walk per pick is the round trip from the front cross-aisle, weighted by picks a day. "Easy reach" means the floor or first beam level in the seven bays nearest the front. Loads are drawn at their real heights. Shelving, packing and docks are simplified.</figcaption>
<script type="application/json" id="wh3d-data">{data}</script>
</figure>
"""


def part1():
    rows = [("As-is", A0), ("1. Re-set beam heights", A1), ("2. Combine partial pallets", A2), ("3. Clear dead stock", A3), ("4. Re-slot fast movers", A4)]
    trs = "".join(f'<tr><td>{n}</td><td class="num">{f0(s["positions"])}</td><td class="num">{f0(s["occupied"])}</td><td class="num">{pc(s["loc_util"])}</td>'
                  f'<td class="num">{pc(s["cube_occ"])}</td><td class="num">{f0(s["walk"])}&nbsp;m</td></tr>' for n, s in rows)
    body = f"""{CSS}
<p>Sooner or later every growing distributor hears it from the warehouse: "We're out of space." Receiving has pallets parked in the aisles, the forklift driver spends the morning shuffling loads to make room, and someone starts pricing a bigger building. A move is one of the largest decisions a small business makes. It means a longer lease, racking, a new layout and weeks of disruption.</p>
<p>Very often the building is not full. The <em>positions</em> are full. The space inside them is half air, part of it holds stock that has not moved in a year, and the products picked every day sit at the back on the top level. This first part of the warehouse operations series shows how to tell the two apart, measure it in an afternoon, and win the space back before signing a lease.</p>
<h2>The example distributor</h2>
<p>The series follows one illustrative business: a distributor in a {f0(BLD_FT2)}&nbsp;sq&nbsp;ft building with a {W.CLEAR_H:.1f}&nbsp;m (30&nbsp;ft) clear height and about 3,000 SKUs. Most SKUs are small parts on shelving. The {W.N_SKU} bulkiest SKUs are stored in a pallet-rack zone of {W.ROWS} rows by {W.BAYS} bays, two pallets a bay, served by {len(W.AISLE_Z)} aisles {W.AISLE:.1f}&nbsp;m wide for counterbalance forklifts. As built the racks have four levels, so the zone holds {f0(A0["positions"])} pallets. It is the zone everyone says is full, and it is the one this post works on.</p>
<h2>Step 1: measure three numbers, not one</h2>
<p>"Full" can mean three different things, and each is measured differently.</p>
<table>
<tr><th>Measure</th><th>What it counts</th><th>How to get it</th><th>What it tells you</th></tr>
<tr><td>Floor utilization</td><td>Share of the floor covered by racks, shelving and stored goods</td><td>The layout drawing</td><td>Whether the floor plan is efficient. Says nothing about height</td></tr>
<tr><td>Location utilization</td><td>Share of the storage positions that hold something</td><td>A count from your WMS, ERP or a walk-through</td><td>How full the warehouse <em>feels</em>. This is the number behind "we're full"</td></tr>
<tr><td>Cube utilization</td><td>Share of the volume of the occupied positions that product actually fills</td><td>Load heights against the clear height of each opening</td><td>How much air you are storing. This is where the hidden space is</td></tr>
</table>
<p>The two that matter here are calculated as:</p>
{eq(r"\text{Location utilization} = \dfrac{\text{positions holding a pallet}}{\text{all pallet positions}}")}
{eq(r"\text{Cube utilization} = \dfrac{\sum \text{load volume}}{\sum \text{volume of the openings those loads sit in}}")}
<p>Published benchmarks help put the results in context. Conventional racked warehouses usually run at about 80 to 85% of their locations occupied, and around 85% is where congestion starts: receiving slows, pallets wait in the aisles and loads get handled twice. The same benchmark sources point out that a building can show more than 80% of its positions occupied while product fills well under 60% of the rack volume, because loads are shorter than the beam openings and partial pallets sit in full-size slots. The gap between the two numbers is the space you can recover.</p>
<p>For the example distributor, the count gives {f0(A0["occupied"])} pallets in {f0(A0["positions"])} positions, a location utilization of {pc(A0["loc_util"])}. That is past the 85% congestion point, and it is why the warehouse feels full. Measuring the load heights tells a different story: the loads fill only {pc(A0["cube_occ"])} of the openings they occupy.</p>
<h2>Step 2: find where the air is</h2>
<p>Space in a pallet-rack zone is usually lost in the same five places.</p>
<ul>
<li><strong>Beam openings set for a load you no longer receive.</strong> The racks were installed for tall pallets years ago, and today's loads are 1.2 to 1.4&nbsp;m. Every opening carries half a metre or more of air.</li>
<li><strong>Partial pallets.</strong> Picking leaves broken pallets, and two or three partial pallets of one SKU each take a full position. In the example, {f0(I["partial"])} of the {f0(I["n_pal"])} pallets are partial.</li>
<li><strong>Dead stock.</strong> Product with no sales in twelve months still takes a position. The example has {I["cls_count"]["D"]} such SKUs on {f0(I["cls_pal"]["D"])} pallets.</li>
<li><strong>Put-away to the first free slot.</strong> Without slotting rules, fast movers end up wherever there was a hole on the day they arrived, which is often high and at the back.</li>
<li><strong>The wrong storage for the item.</strong> A pallet position holding three cartons of a small item is a position lost. Small, slow items belong on shelving or in carton flow, not on a pallet.</li>
</ul>
{fig(fig_bay(), 1, "One bay as built and with the beams re-set. The same rack height holds five levels instead of four once the openings match today's loads.")}
<h2>Step 3: fix it in order</h2>
<p>The fixes below are applied one after the other, cheapest and most certain first. Each builds on the one before, which is how Figure 2 runs them.</p>
<p><strong>Fix 1: re-set the beam heights.</strong> Measure the tallest load each SKU really arrives on, then re-space the beams to suit, with about 100&nbsp;mm of lift-off clearance. In the example the floor level stays 2.0&nbsp;m high for the {TALL} tall loads, and the beams above move to a 1.7&nbsp;m pitch. The same uprights now carry five levels, and the top load still stays 450&nbsp;mm (18&nbsp;in) below the sprinkler deflectors. Positions rise from {f0(A0["positions"])} to {f0(A1["positions"])}. Treat this as an engineering change: the rack manufacturer or a rack engineer confirms the new configuration's capacities, new load signs go up, and the fire protection contractor checks the sprinkler clearance. Re-beaming also means emptying each bay in turn, so plan it bay by bay over quiet weeks.</p>
<p><strong>Fix 2: combine partial pallets.</strong> Where a SKU has two partial pallets whose stock fits on one, combine them. In the example that removes {I["merged"]} pallets and frees the same number of positions. Then add a rule so it stays fixed: a pallet below about a third full is consolidated before a new one is put away.</p>
<p><strong>Fix 3: clear the dead stock.</strong> List the SKUs with no picks in twelve months and decide each one: return it to the supplier, sell it to a liquidator, move it to cheaper overflow storage, or scrap it. The money was lost when the stock stopped selling. Keeping it in a prime position only adds the cost of the space. Clearing the example's {I["dead"]} dead pallets frees {I["dead"]} positions.</p>
<p><strong>Fix 4: re-slot the fast movers.</strong> Rank the pallets by picks a day, as in the <a href="{ABC1}.html">ABC inventory analysis</a>, and give the busiest the best positions: the floor and first beam level, nearest the front. Slow movers and reserve pallets go up and to the back. Re-slotting does not add positions, but it decides how far people travel. Reserve pallets follow their pick face, A first, then B, then C, so each class sits above and behind its own picks. In the example that is a full re-slot of {f0(I["moves4"])} pallet moves, done in waves over a few weekends, and it cuts the average walk per pick from {f0(A0["walk"])} to {f0(A4["walk"])}&nbsp;m. Published first-time slotting projects often report travel savings of about 20 to 40%. The example saves more because its put-away was close to random.</p>
{figure_markup()}<h2>The result</h2>
<table>
<tr><th>Step</th><th class="num">Positions</th><th class="num">Pallets</th><th class="num">Occupied</th><th class="num">Opening filled</th><th class="num">Walk per pick</th></tr>
{trs}
</table>
<p>After the four fixes the zone holds the same live stock in {pc(A4["loc_util"])} of its positions, with {f0(A4["free"])} positions free instead of {f0(A0["free"])}. The loads now fill {pc(A4["cube_occ"])} of their openings. The busiest pallets sit within easy reach: {pc(A4["easy"])} of picks come from the floor or first beam level near the front, against {pc(A0["easy"])} before.</p>
{fig(fig_bridge(), 3, "Where the free positions came from. Re-slotting adds no positions, but it decides how far people walk.")}
<h2>Step 4: compare the fixes with a move</h2>
<p>The {f0(GAIN)} recovered positions would need about {f0(round(EQ_FT2, -2))}&nbsp;sq&nbsp;ft of extra racked floor as the zone was built. Canada's national average net asking rent for industrial space was $14.77 per sq&nbsp;ft a year in the third quarter of 2026. With an assumed ${ADD:.2f} of additional rent for taxes and common costs, that floor would cost about ${f0(round(LEASE, -3))} a year, before the cost of moving, new racking and the disruption. The fixes are a one-time cost.</p>
<table>
<tr><th>One-time cost of the four fixes</th><th>Basis (assumed)</th><th class="num">Estimate</th></tr>
<tr><td>New beam pairs for the fifth level</td><td>{BAYS_ALL} bays at ${f0(BEAMS)} a pair</td><td class="num">${f0(C_BEAM_MAT)}</td></tr>
<tr><td>Rack engineering review, load signs</td><td>Allowance</td><td class="num">${f0(ENG)}</td></tr>
<tr><td>Labour: re-beam, unload and reload each bay</td><td>{f0(H_BEAM)} hours at ${f0(WAGE)}</td><td class="num">${f0(H_BEAM * WAGE)}</td></tr>
<tr><td>Labour: combine, clear and re-slot</td><td>{f0(H_COMB + H_DEAD + H_SLOT)} hours at ${f0(WAGE)}</td><td class="num">${f0((H_COMB + H_DEAD + H_SLOT) * WAGE)}</td></tr>
<tr class="oee-total"><td>Total</td><td></td><td class="num">${f0(round(C_ALL, -3))}</td></tr>
</table>
<p>About ${f0(round(C_ALL, -3))} once, against about ${f0(round(LEASE, -3))} every year. There is also time. With {f0(A4["occupied"])} pallets in {f0(A4["positions"])} positions, the zone can grow by {GROW * 100:.0f}% a year for about {YEARS:.0f} years before it reaches the 85% congestion point again. That is time to plan a move properly, if one is ever needed.</p>
<h2>Other levers</h2>
<ul>
<li><strong>Narrower aisles.</strong> Counterbalance forklifts need aisles of about 3.5 to 4&nbsp;m. Reach trucks work in about 2.7 to 3&nbsp;m, which can add a rack row in the same building. It needs new trucks and operator training, so it comes after the cheaper fixes.</li>
<li><strong>Right-size the storage.</strong> Move small, slow items from pallet positions to shelving, carton flow or bins, and very slow items to a mezzanine or high shelving.</li>
<li><strong>Clear the floor.</strong> Staging areas full of stock waiting for put-away usually point to a receiving problem, not a space problem. <a href="the-dock-door-bottleneck-receiving-put-away-and-cross-docking.html">Part&nbsp;3</a> of this series deals with the dock.</li>
<li><strong>Overflow for the peak.</strong> If space runs short for six weeks of the year, short-term overflow storage costs far less than a bigger building for all twelve months.</li>
</ul>
<h2>Keep it from creeping back</h2>
<p>Slotting drifts. New products arrive, sales patterns change, and within a year the fast movers are back at the top and the back. A short routine keeps the gains.</p>
<table>
<tr><th>Measure</th><th>How often</th><th>Signal to act</th></tr>
<tr><td>Location utilization</td><td>Weekly</td><td>Above 85% for more than a few weeks</td></tr>
<tr><td>Cube utilization of occupied positions</td><td>Quarterly</td><td>More than about 15 points below location utilization</td></tr>
<tr><td>Partial pallets</td><td>Monthly</td><td>More than one partial pallet per SKU</td></tr>
<tr><td>SKUs with no picks in 12 months</td><td>Quarterly</td><td>Any in the front or lower positions</td></tr>
<tr><td>Picks from easy reach</td><td>Monthly</td><td>Falling as the product range changes</td></tr>
</table>
<h2>When you really are full</h2>
<p>Sometimes the answer is a bigger building. The signs are clear once the fixes are done: location utilization stays above 85% after the beams, partials and dead stock have been dealt with, the cube utilization of occupied positions is already above about 75%, and the sales forecast takes you past the limit within a year. Then the measurements above become the brief for the new building: the pallet count, the load heights and the pick rates it has to serve.</p>
<h2>Common mistakes</h2>
<ul>
<li><strong>Counting positions and calling it space.</strong> Location utilization tells you how full it feels. Cube utilization tells you how full it is.</li>
<li><strong>Moving beams without the rack maker.</strong> Every configuration has rated capacities. Re-set beams under an engineer's review and post the new load signs.</li>
<li><strong>Stacking into the sprinkler clearance.</strong> An extra level is no gain if the top load blocks the sprinklers.</li>
<li><strong>Re-slotting once.</strong> Without a monthly check the fast movers drift back.</li>
<li><strong>Keeping dead stock because it was expensive.</strong> The cost is already spent. The space it takes is a new cost.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>A warehouse can be full by positions and half empty by volume. Measure location and cube utilization.</li>
<li>Around 85% of positions occupied is where congestion starts. Above it the building feels full whatever the volume says.</li>
<li>Fix in order: beam heights, partial pallets, dead stock, then slotting.</li>
<li>In the example the four fixes free {f0(GAIN)} positions and cut the walk per pick by {pc(WALK_CUT)}, for a one-time cost of about ${f0(round(C_ALL, -3))} against about ${f0(round(LEASE, -3))} a year for equivalent leased space.</li>
<li>Measure again every month, or the gains drift away.</li>
</ul>
<p>Related reading: <a href="{ABC1}.html">ABC inventory analysis</a> ranks SKUs by value and picks, <a href="{ABC2}.html">ABC analysis for manufacturers</a> applies it in a plant, and <a href="{SS1}.html">setting safety stock</a> keeps reserve pallets to what is needed. Next in this series: <a href="{W2}.html">Part&nbsp;2</a> follows the pickers through the same warehouse and compares pick methods.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://camcode.com/blog/how-to-calculate-warehouse-space-utilization/" rel="noopener" target="_blank">Camcode: How to calculate warehouse space utilization</a> (storage cube, location utilization and the 85% congestion point)</li>
<li><a href="https://www.extensiv.com/blog/how-to-calculate-warehouse-utilization-3pl-guide" rel="noopener" target="_blank">Extensiv: How to calculate warehouse utilization</a> (WERC DC Measures benchmarks, slot versus cube utilization)</li>
<li><a href="https://www.cbre.com/insights/figures/canada-industrial-figures-q3-2026" rel="noopener" target="_blank">CBRE: Canada Industrial Figures Q3 2026</a> (national net asking rent)</li>
<li><a href="https://www.goramp.com/blog/warehouse-slotting-guide" rel="noopener" target="_blank">Ramp: Warehouse slotting guide</a> (travel share of pick time, slotting savings)</li>
</ul>
{NOTE}{js3d("wh3d")}{mathjs()}"""
    body = nowrap(body, [(1, 0, 24), (2, 0, 28), (3, 0, 40)])
    return dict(slug=W1, title="We're Out of Space, or Are We? Warehouse Cube Utilization and Slotting",
                desc="Measure location and cube utilization, find the air in your racks, and win space back with beam heights, consolidation, dead stock and slotting.",
                cats=["operational-efficiency", "inventory-management"], tags=["warehouse space utilization", "cube utilization", "warehouse slotting", "pallet racking", "dead stock", "distribution"],
                body=body, date=DATE, author="Quak Foo Lee", read="11 min read", series=SER(1), cover_label="Warehouse operations",
                related=[ABC1, SS1, OEE1])


if __name__ == "__main__":
    a = part1()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])} gain={GAIN} eqft2={EQ_FT2:.0f} lease={LEASE:.0f} cost={C_ALL:.0f} "
                     f"(beam h {H_BEAM:.0f}, other h {H_COMB + H_DEAD + H_SLOT:.0f}) years={YEARS:.2f} walkcut={WALK_CUT:.3f} tall={TALL}\n")
