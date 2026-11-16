"""Warehouse operations series for Insights (V5.32). Part 2: pick methods and pick paths.

Same distributor and pallet-rack zone as Part 1 (wh_model.py). The picking numbers come from wh2_model.py, which
also writes the data behind the 3D figure (assets/js/wh3d2.js).

Usage:  python3 content/articles/wh2_articles.py
        python3 content/gen/add_article.py pickers-walk-half-the-day-pick-methods-and-pick-paths
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import js3d, nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, PURPLE, MUTED, LINE, PALE, eq, im, mathjs
import wh_model as W
import wh2_model as P
from wh_articles import W1, SER, ABC1, OEE1

DATE = "2026-11-15"
W2 = "pickers-walk-half-the-day-pick-methods-and-pick-paths"
W3 = "the-dock-door-bottleneck-receiving-put-away-and-cross-docking"
NOTE = ('<p class="oee-note"><em>The distributor, its orders and its times in this series are an illustrative example built from stated '
        'assumptions. Measure your own pick rates and walking distances before choosing a method.</em></p>')
f0 = lambda x: f"{x:,.0f}"
f1 = lambda x: f"{x:,.1f}"
pc = lambda x: f"{x * 100:.0f}%"

G = P.grid(); I = P.VOLUMES.index(P.ORDERS)
def g(st, m, r=None, i=I): return G[(st, m, r or P.best_route(G, st, m, i))][i]
BASE = g(0, "single", "return")                                    # how the example works today
NEED = lambda x: math.ceil(x["total"] / 3600 / P.SHIFT_H - 1e-9)
COL = {"single": "#9AA8BA", "batch": BLUE, "zone": GREEN, "wave": ORANGE}


def fig_routes():
    """Return and S-shape routes through the same eight picks in a five-aisle schematic. Each straight leg carries one
    arrowhead 40% along it (the line runs into the middle of the arrowhead's flat base); legs that would overlap run
    on separate offset lines."""
    picks = [(0, 0.35), (0, 0.15), (1, 0.8), (2, 0.25), (3, 0.55), (3, 0.9), (4, 0.2), (4, 0.4)]
    L, top, gap = 230, 60, 44

    def arrowhead(x1, y1, x2, y2, f=0.4):
        mx, my = x1 + (x2 - x1) * f, y1 + (y2 - y1) * f; dx, dy = x2 - x1, y2 - y1; d = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / d, dy / d; px, py = -uy, ux; hl, hw = 9, 5            # tip ahead of the midpoint, flat base behind it
        tip = (mx + ux * hl / 2, my + uy * hl / 2); bc = (mx - ux * hl / 2, my - uy * hl / 2)
        return (f'<path d="M{tip[0]:.1f},{tip[1]:.1f} L{bc[0] + px * hw:.1f},{bc[1] + py * hw:.1f} '
                f'L{bc[0] - px * hw:.1f},{bc[1] - py * hw:.1f} z" fill="{BLUE}"/>')

    def draw(pts, dots):
        out = f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{BLUE}" stroke-width="2.2" stroke-linejoin="round"/>'
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if abs(x2 - x1) + abs(y2 - y1) < 26: continue
            for f in (0.4, 0.6, 0.25, 0.75, 0.5, 0.15, 0.85):      # keep the arrowhead clear of the pick dots
                ax, ay = x1 + (x2 - x1) * f, y1 + (y2 - y1) * f
                if all(abs(ax - dx) + abs(ay - dy) > 16 for dx, dy in dots): break
            out += arrowhead(x1, y1, x2, y2, f)
        return out

    def panel(x0, route, title, note):
        s = txt(x0 + 140, 24, title, "middle", NAVY, 14, True)
        X = lambda f: x0 + 30 + f * L
        FR, BK, DOWN = x0 + 14, x0 + L + 50, x0 + 4               # front cross-aisle, back cross-aisle, the walk back to packing
        ybot = top + 4 * gap
        for a in range(5):
            y = top + a * gap
            s += f'<rect x="{x0 + 30}" y="{y - 16}" width="{L}" height="8" fill="#C9D3DE"/><rect x="{x0 + 30}" y="{y + 8}" width="{L}" height="8" fill="#C9D3DE"/>'
        by = {}
        for a, f in picks: by.setdefault(a, []).append(f)
        aisles = sorted(by, reverse=True)
        pts = [(FR, ybot + 40)]; end = "F"
        for i, a in enumerate(aisles):
            y = top + a * gap; last = i == len(aisles) - 1
            if route == "s" and not (last and end == "F"):
                pts += [(FR if end == "F" else BK, y), (BK if end == "F" else FR, y)]; end = "B" if end == "F" else "F"
            else:                                                 # in along the upper side of the aisle, out along the lower side
                xm = X(max(by[a])) + 10
                pts += [(FR, y - 6), (xm, y - 6), (xm, y + 6), (FR, y + 6)]
        ytop = pts[-1][1]
        pts += [(DOWN, ytop), (DOWN, ybot + 40)]                  # back down to packing on its own line
        dots = [(X(f), top + a * gap - (6 if route == "r" else 0)) for a, f in picks]
        s += draw(pts, dots)
        for a, f in picks: s += f'<circle cx="{X(f):.1f}" cy="{top + a * gap - (6 if route == "r" else 0)}" r="5.5" fill="{ORANGE}" stroke="#fff" stroke-width="1.5"/>'
        s += f'<rect x="{x0 - 8}" y="{ybot + 40}" width="34" height="18" rx="3" fill="{NAVY}"/>' + txt(x0 + 9, ybot + 53, "Pack", "middle", "#fff", 10.5, True)
        s += txt(x0 + 140, ybot + 82, note, "middle", NAVY, 13, True)
        return s
    s = panel(20, "r", "Return: in and back out of each aisle", "Best when picks sit near the front") + panel(380, "s", "S-shape: right through each aisle", "Best when picks are spread along the aisles")
    s += txt(360, 340, "Orange dots: the same eight picks in both cases. Front cross-aisle on the left, back cross-aisle on the right.", "middle", MUTED, 12)
    return svg("Two schematic routes through five aisles with the same eight picks. The return route enters each aisle with picks as far as the farthest one "
               "and comes back out the front. The S-shape route walks right through every aisle with picks, snaking from front to back and back again. "
               "Both end with the walk back down the front to the pack station.", 720, 350, s, 560)


def fig_time():
    rows = [("Single-order, as-is", g(0, "single", "return")), ("Single-order", g(4, "single")), ("Batch", g(4, "batch")),
            ("Zone", g(4, "zone")), ("Wave", g(4, "wave"))]
    parts = [("t_walk", "Walking", "#E06B4A"), ("t_pick", "Picking", BLUE), ("t_setup", "Trip set-up", "#9AA8BA"), ("t_extra", "Sorting and consolidation", PURPLE)]
    x0, w = 190, 430; mx = max(r["total"] for _, r in rows); sc = w / mx; s = ""
    lx = x0
    for _, lab, c in parts: s += f'<rect x="{lx}" y="10" width="12" height="12" rx="2" fill="{c}"/>' + txt(lx + 18, 21, lab, fill=NAVY, fs=12); lx += 30 + len(lab) * 6.6
    for k, (lab, r) in enumerate(rows):
        y = 40 + k * 46; x = x0
        s += txt(x0 - 10, y + 19, lab, "end", NAVY, 13, k == 0)
        for key, _, c in parts:
            ww = r[key] * sc; s += f'<rect x="{x:.1f}" y="{y}" width="{ww:.1f}" height="28" fill="{c}"/>'
            if ww > 34: s += txt(x + ww / 2, y + 19, f"{r[key] / r['total'] * 100:.0f}%", "middle", "#fff", 11.5, True)
            x += ww
        s += txt(x + 8, y + 19, f"{r['total'] / 3600:.1f} h", fill=NAVY, fs=13, bold=True)
    s += txt(x0, 40 + 5 * 46 + 8, f"Picker-hours a day for {P.ORDERS} orders ({f0(BASE['lines'])} case picks). All but the first row use the Part 1 layout.", fill=MUTED, fs=12)
    return svg("Stacked bars of picker-hours a day split into walking, picking, trip set-up, and sorting and consolidation. "
               f"Single-order picking in the as-is layout takes {BASE['total'] / 3600:.1f} hours, {pc(BASE['share_walk'])} of it walking. "
               f"In the re-slotted layout single-order takes {g(4, 'single')['total'] / 3600:.1f} hours, batch {g(4, 'batch')['total'] / 3600:.1f}, "
               f"zone {g(4, 'zone')['total'] / 3600:.1f} and wave {g(4, 'wave')['total'] / 3600:.1f}.", 720, 296, s, 560)


def fig_volume():
    x0, y0, w, h = 70, 30, 560, 230; vmax = P.VOLUMES[-1]; s = ""
    ymax = max(G[(4, "single", P.best_route(G, 4, "single", i))][i]["total"] for i in range(len(P.VOLUMES))) / 3600
    ymax = math.ceil(ymax / 10) * 10
    X = lambda v: x0 + (v - P.VOLUMES[0]) / (vmax - P.VOLUMES[0]) * w
    Y = lambda hh: y0 + h - hh / ymax * h
    for t in range(0, ymax + 1, 10):
        s += f'<line x1="{x0}" y1="{Y(t):.1f}" x2="{x0 + w}" y2="{Y(t):.1f}" stroke="#E4E1D8"/>' + txt(x0 - 8, Y(t) + 4, str(t), "end", MUTED, 12)
    for v in range(150, 601, 75): s += txt(X(v), y0 + h + 18, str(v), "middle", MUTED, 12)
    s += txt(x0 + w / 2, y0 + h + 40, "Orders a day", "middle", NAVY, 12.5, True)
    s += f'<text x="20" y="{y0 + h / 2}" transform="rotate(-90 20 {y0 + h / 2})" text-anchor="middle" font-size="12.5" font-weight="600" fill="{NAVY}">Picker-hours a day</text>'
    for k in (1, 2, 3):
        s += f'<line x1="{x0}" y1="{Y(k * P.SHIFT_H):.1f}" x2="{x0 + w}" y2="{Y(k * P.SHIFT_H):.1f}" stroke="{NAVY}" stroke-dasharray="3 4" opacity=".5"/>'
        s += txt(x0 + w + 6, Y(k * P.SHIFT_H) + 4, f"{k} picker{'s' if k > 1 else ''}", fill=MUTED, fs=11.5)
    ends = []
    for m in P.METHODS:
        pts = [(X(v), Y(G[(4, m, P.best_route(G, 4, m, i))][i]["total"] / 3600)) for i, v in enumerate(P.VOLUMES)]
        s += f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{COL[m]}" stroke-width="3"/>'
        ends.append([pts[-1][1], m])
    for k, m in enumerate(P.METHODS):                            # legend, top left, in the chart's empty corner
        s += f'<rect x="{x0 + 14}" y="{y0 + 6 + k * 18}" width="12" height="12" rx="2" fill="{COL[m]}"/>' + txt(x0 + 32, y0 + 16 + k * 18, P.NAMES[m], fill=NAVY, fs=12.5, bold=True)
    return svg("Line chart of picker-hours a day against orders a day, from 150 to 600, for the four methods in the re-slotted layout. "
               "Single-order rises steeply. Batch and zone rise at about half the rate, and wave rises least because its trips get denser as volume grows.",
               700, 310, s, 560)


def figure_data():
    pal = []
    for p in M_pal:
        pal.append([p["cls"], p["h"], M1["locs"][0][p["id"]], M1["locs"][4].get(p["id"], -1), M1["p2"][p["id"]]["h"] if p["id"] in M1["p2"] else p["h"]])
    ex = {}
    for st in (0, 4):
        for r in ("return", "sshape"):
            e = P.example_trips(st, r, __import__("random").Random(5))
            ex[f"{st}{r[0]}"] = {m: [[[[round(c, 2) for c in pt] for pt in path], [[round(c, 2) for c in pt] for pt in stops]] for path, stops in e[m]]
                                 for m in P.METHODS}
    keys = ["m_order", "lph", "total", "share_walk"]
    gr = {f"{st}{m}{r[0]}": [[round(x[k], 4) for k in keys] for x in G[(st, m, r)]] for (st, m, r) in G}
    return dict(bld=[W.BLD_X, W.BLD_Z, W.CLEAR_H], rows=W.ROW_Z, aisles=W.AISLE_Z, bays=W.BAYS, bayW=W.BAY_W, rowD=W.ROW_D, x0=W.RACK_X0,
                perBay=W.PER_BAY, beam=W.BEAM, levels=[W.LEVELS_ASIS, W.LEVELS_NEW], fx=P.FX, bx=P.BX, depot=P.DEPOT,
                vols=P.VOLUMES, shift=P.SHIFT_H, grid=gr, ex=ex, p=pal)


M1 = W.run(); M_pal = M1["pallets"]


def figure_markup():
    data = json.dumps(figure_data(), separators=(",", ":"))
    v0 = P.ORDERS; b = g(0, "single", "return")
    btn = lambda m, on: f'<button type="button" class="wh3d-btn" data-m="{m}" aria-pressed="{on}">{P.NAMES[m] if m != "all" else "Compare all"}</button>'
    return f"""<p>Figure 2 puts pickers into the Part 1 warehouse. Each coloured trail is one trip, and each glowing dot a case pick. Choose a method, or Compare all to see the four side by side, switch between the as-is layout and the layout after Part 1's fixes, and move the slider to change the day's orders. The numbers come from the same model as the tables.</p>
<figure class="wh3d wh3d2" id="wh3d2">
<div class="wh3d-box">
<div class="wh3d-stage">
<canvas role="img" aria-label="3D model of the example distributor's pallet-rack zone with pickers walking their routes. Each trip is drawn as a coloured trail from the pack stations through the aisles and back, with a marker at every case pick. In the compare view the four pick methods are shown side by side."></canvas>
<span class="wh3d-drag" aria-hidden="true">Drag to turn</span>
<span class="wh3d-chip" id="wh3d2-chip">Single-order</span>
<p class="wh3d-nogl" id="wh3d2-nogl" hidden>This browser cannot show the 3D model. The controls below still update the numbers.</p>
</div>
<div class="wh3d-panel">
<div class="wh3d2-row" role="group" aria-label="Pick method">{btn("single", "true")}{btn("batch", "false")}{btn("zone", "false")}{btn("wave", "false")}{btn("all", "false")}</div>
<div class="wh3d2-opts">
<div class="wh3d2-seg" role="group" aria-label="Layout"><span>Layout</span><button type="button" class="wh3d-btn" data-l="0" aria-pressed="true">As-is</button><button type="button" class="wh3d-btn" data-l="4" aria-pressed="false">After Part 1</button></div>
<div class="wh3d2-seg" role="group" aria-label="Route"><span>Route</span><button type="button" class="wh3d-btn" data-r="return" aria-pressed="true">Return</button><button type="button" class="wh3d-btn" data-r="sshape" aria-pressed="false">S-shape</button></div>
<div class="wh3d2-sl"><label for="wh3d2-vol">Orders a day <output id="wh3d2-vol-o" for="wh3d2-vol">{v0}</output></label><input type="range" id="wh3d2-vol" min="{P.VOLUMES[0]}" max="{P.VOLUMES[-1]}" step="25" value="{v0}"></div>
</div>
<div class="wh3d-cells">
<div class="wh3d-cell wh3d-key"><span class="k">Walk per order</span><strong id="wh3d2-m">{f0(b["m_order"])} m</strong></div>
<div class="wh3d-cell wh3d-key"><span class="k">Lines per picker-hour</span><strong id="wh3d2-lph">{f0(b["lph"])}</strong></div>
<div class="wh3d-cell"><span class="k">Picker-hours a day</span><strong id="wh3d2-h">{f1(b["total"] / 3600)}</strong></div>
<div class="wh3d-cell"><span class="k">Pickers needed</span><strong id="wh3d2-n">{NEED(b)}</strong></div>
<div class="wh3d-cell"><span class="k">Time spent walking</span><strong id="wh3d2-w">{pc(b["share_walk"])}</strong></div>
<div class="wh3d-cell"><span class="k">Case picks a day</span><strong id="wh3d2-l">{f0(b["lines"])}</strong></div>
</div>
<div class="wh3d2-bars" id="wh3d2-bars" aria-hidden="true"></div>
<p class="wh3d-say" id="wh3d2-say" aria-live="polite"></p>
<div class="wh3d-last"><ul class="wh3d-legend"><li><i style="background:#9AA8BA"></i>Single-order</li><li><i style="background:#3FA7F5"></i>Batch</li><li><i style="background:#8DC63F"></i>Zone</li><li><i style="background:#FF8A3D"></i>Wave</li><li><i style="background:#FFE27A;border-radius:50%"></i>Case pick</li></ul></div>
</div>
</div>
<figcaption>Figure 2. Pickers in the Part 1 warehouse. Trails show example trips at {P.ORDERS} orders a day, drawn faster than life. Single-order and batch trips start and end at the pack stations. Zone and wave pickers each work one aisle and hand totes over at the front. The bars compare picker-hours a day for the four methods at the chosen layout, route and volume. The route applies to single-order and batch only.</figcaption>
<script type="application/json" id="wh3d2-data">{data}</script>
</figure>
"""


def part2():
    rows = ""
    for st, lab in ((0, "As-is layout"), (4, "After Part 1")):
        for m in P.METHODS:
            r = P.best_route(G, st, m, I); x = g(st, m, r)
            rows += (f'<tr><td>{lab if m == "single" else ""}</td><td>{P.NAMES[m]}</td><td>{"S-shape" if r == "sshape" else "Return"}</td><td class="num">{f0(x["m_order"])}&nbsp;m</td>'
                     f'<td class="num">{f0(x["lph"])}</td><td class="num">{f1(x["total"] / 3600)}</td><td class="num">{NEED(x)}</td><td class="num">{pc(x["share_walk"])}</td></tr>')
    sr0, rr0 = g(0, "single", "sshape"), g(0, "single", "return"); sr4, rr4 = g(4, "single", "sshape"), g(4, "single", "return")
    BEST = g(4, "batch"); WV = g(4, "wave"); ZN = g(4, "zone")
    i600 = P.VOLUMES.index(600); i150 = P.VOLUMES.index(150)
    body = f"""{CSS}
<p>Orders are going out late. The 3 pm carrier pickup leaves with half a dozen orders still on the pick list, overtime has become normal, and the first answer is always the same: hire another picker. Before you do, follow one of your pickers for an hour. Most of that hour is not spent picking. It is spent walking.</p>
<p>Part&nbsp;1 of this series won back space in the example distributor's pallet-rack zone and moved the fast movers to the front. This part follows the pickers through the same warehouse. It compares the four common ways of picking orders and the two simple routes through the aisles, and shows how many picker-hours each one takes for the same day's work.</p>
<h2>Where a picker's day goes</h2>
<p>A pick trip has four parts: getting the list and the cart, walking between locations, picking the case off the pallet, and sorting or consolidating the result for packing. The order-picking literature has long reported that travel is the largest of these, often about half of a picker's time or more, which is why most of the ways to pick faster are ways to walk less.</p>
<p>The example picks {f0(BASE["lines"])} cases a day from the rack zone: {P.ORDERS} orders of about {P.LINES:.0f} lines each. The times assumed throughout are:</p>
<table>
<tr><th>Assumption</th><th class="num">Value</th></tr>
<tr><td>Walking speed with a cart</td><td class="num">{P.SPEED} m/s</td></tr>
<tr><td>Pick one case off a pallet</td><td class="num">{f0(P.T_PICK)} s</td></tr>
<tr><td>Put a line into the right order's tote (batch, wave)</td><td class="num">{f0(P.T_TOTE)} s</td></tr>
<tr><td>Set up a trip: list, labels, cart</td><td class="num">{f0(P.T_SETUP)} s</td></tr>
<tr><td>Set up a zone trip</td><td class="num">{f0(P.T_ZSET)} s</td></tr>
<tr><td>Bring an order's totes together at packing (zone, wave)</td><td class="num">{f0(P.T_CONS)} s</td></tr>
<tr><td>Productive picking hours per picker a day</td><td class="num">{P.SHIFT_H:.0f} h</td></tr>
</table>
<p>With single-order picking in the as-is layout, each order costs about {f0(BASE["m_order"])}&nbsp;m of walking. The day takes {f1(BASE["total"] / 3600)} picker-hours, and {pc(BASE["share_walk"])} of that is walking. That is {NEED(BASE)} pickers' worth of work for {f0(BASE["lines"])} cases.</p>
<h2>The four pick methods</h2>
<table>
<tr><th>Method</th><th>How it works</th><th>Suits</th><th>Watch out for</th></tr>
<tr><td>Single-order</td><td>One picker takes one order from start to finish, then comes back for the next</td><td>Few orders a day, large orders, urgent one-offs</td><td>Walks the whole warehouse for every order. Picker-hours rise in step with orders</td></tr>
<tr><td>Batch</td><td>One trip picks several orders at once onto a cart of totes, one tote per order, and each line goes straight into its order's tote</td><td>Many small orders: e-commerce, parts and service orders</td><td>A put-to-the-wrong-tote error. Needs a scan or a clear tote label at each put</td></tr>
<tr><td>Zone</td><td>Each picker owns one area and picks only the lines in it. An order's totes meet at packing</td><td>Larger buildings, several storage types, several pickers a shift</td><td>Uneven zones leave one picker swamped and another idle. Consolidation at packing</td></tr>
<tr><td>Wave</td><td>Orders are released in timed waves set by the carrier pickups. Each zone picker sweeps their zone once per wave</td><td>Fixed carrier cut-offs, steady daily volume</td><td>Needs a WMS or a disciplined release routine. A late wave misses its truck</td></tr>
</table>
<p>The methods combine. Wave picking, as modelled here, is zone picking with orders released in {P.WAVES} waves a day, timed to the pickups. Each zone picker carries up to {P.CART} lines a trip. Batch and zone trips here hold {P.BATCH} orders.</p>
<h2>Routing: return or S-shape</h2>
<p>The route matters as much as the method. Two simple rules cover most small warehouses, and both can be printed on a pick list as a sorted location sequence.</p>
{fig(fig_routes(), 1, "Two routes through the same picks. Neither is best everywhere: it depends on where the picks sit along the aisles.")}
<p>In the example the answer flips with the layout. In the as-is warehouse, fast movers are scattered along the aisles, so the S-shape route is a little shorter for single-order picking ({f0(sr0["m_order"])}&nbsp;m against {f0(rr0["m_order"])}&nbsp;m an order). After Part&nbsp;1's re-slot, the busy pallets sit in the front bays, and the return route wins clearly: {f0(rr4["m_order"])}&nbsp;m against {f0(sr4["m_order"])}&nbsp;m. Slotting and routing have to be decided together.</p>
{figure_markup()}<h2>The result</h2>
<p>The table gives each method with its better route, at {P.ORDERS} orders a day, in both layouts.</p>
<table>
<tr><th>Layout</th><th>Method</th><th>Route</th><th class="num">Walk per order</th><th class="num">Lines per hour</th><th class="num">Picker-hours</th><th class="num">Pickers</th><th class="num">Walking</th></tr>
{rows}
</table>
{fig(fig_time(), 3, "Where the picker-hours go. Re-slotting and batching remove most of the walking. What is left is mostly picking.")}
<p>Three things stand out.</p>
<ul>
<li><strong>Slotting comes first.</strong> Part&nbsp;1's re-slot alone, with no change of method, cuts single-order picking from {f1(BASE["total"] / 3600)} to {f1(g(4, "single")["total"] / 3600)} picker-hours a day.</li>
<li><strong>Batching halves it again.</strong> Picking {P.BATCH} orders a trip brings the walk down to about {f0(BEST["m_order"])}&nbsp;m an order and the day to {f1(BEST["total"] / 3600)} picker-hours. Two pickers can now do what took {NEED(BASE)}.</li>
<li><strong>Zone and wave win on walking, not always on hours.</strong> Wave picking walks only about {f0(WV["m_order"])}&nbsp;m an order, but it pays for consolidation at packing. At {P.ORDERS} orders it saves about {f1((BEST["total"] - WV["total"]) / 3600)} picker-hours a day over batch picking, and it needs the zones staffed and balanced.</li>
</ul>
{fig(fig_volume(), 4, "Picker-hours as the day's orders grow, in the re-slotted layout. Single-order grows in step with orders. The others grow at about half the rate.")}
<p>Volume changes the choice. At {P.VOLUMES[i150]} orders a day, batch picking takes {f1(G[(4, "batch", P.best_route(G, 4, "batch", i150))][i150]["total"] / 3600)} picker-hours and fits one picker. At {P.VOLUMES[i600]} orders, single-order picking would need {f1(G[(4, "single", P.best_route(G, 4, "single", i600))][i600]["total"] / 3600)} hours, or {math.ceil(G[(4, "single", P.best_route(G, 4, "single", i600))][i600]["total"] / 3600 / P.SHIFT_H)} pickers. Batch takes {f1(G[(4, "batch", P.best_route(G, 4, "batch", i600))][i600]["total"] / 3600)} hours and wave {f1(G[(4, "wave", "return")][i600]["total"] / 3600)}, because each wave's trips get denser as the orders grow.</p>
<h2>Choosing a method</h2>
<table>
<tr><th>Your situation</th><th>Start with</th><th>Then</th></tr>
<tr><td>Under about 100 orders a day, one picker</td><td>Single-order with a sorted pick list and good slotting</td><td>Batch two to four orders a trip when the orders are small</td></tr>
<tr><td>Many small orders, one to three pickers</td><td>Batch picking with a tote per order on the cart</td><td>Add scan-to-tote to stop put errors (Part&nbsp;5)</td></tr>
<tr><td>Several pickers in the same aisles</td><td>Zone picking, with zones sized by picks, not by floor area</td><td>Re-balance the zones every quarter</td></tr>
<tr><td>Fixed carrier pickups that keep being missed</td><td>Wave release timed to each pickup, with batch or zone picking inside each wave</td><td>A WMS to release and track waves (Part&nbsp;7)</td></tr>
</table>
<h2>Measures to track</h2>
<table>
<tr><th>Measure</th><th>What it shows</th></tr>
<tr><td>Lines picked per picker-hour</td><td>The headline productivity number. Track it by method and by person</td></tr>
<tr><td>Walk per order or per line</td><td>Slotting and routing at work. A handheld's step count or a few timed trips are enough to start</td></tr>
<tr><td>Orders shipped by the carrier cut-off</td><td>The number customers feel</td></tr>
<tr><td>Picks from the front bays and the floor or first beam</td><td>Whether slotting is drifting (Part&nbsp;1)</td></tr>
<tr><td>Pick errors per 1,000 lines</td><td>Whether speed is being bought with mistakes</td></tr>
</table>
<h2>Common mistakes</h2>
<ul>
<li><strong>Hiring before measuring.</strong> Time five trips. If walking is half the trip, the fix is the route and the method, not another person.</li>
<li><strong>Unsorted pick lists.</strong> A list in order-entry sequence sends the picker back and forth. Sort it by location along the route.</li>
<li><strong>Batching without a put check.</strong> Faster picking is lost if the wrong case lands in the wrong tote.</li>
<li><strong>Zones by floor area.</strong> Size zones by picks a day, or one picker carries the fast movers for everyone.</li>
<li><strong>Changing the method before the slotting.</strong> The best route and method depend on where the fast movers sit.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>Walking is the largest part of a picker's day. In the example it is {pc(BASE["share_walk"])} of single-order picking as-is.</li>
<li>Re-slot first, then batch: together they take the example from {f1(BASE["total"] / 3600)} to {f1(BEST["total"] / 3600)} picker-hours a day.</li>
<li>Choose the route with the layout. Return suits fast movers at the front; S-shape suits picks spread along the aisles.</li>
<li>Zone and wave picking cut walking most and suit higher volumes, fixed cut-offs and several pickers.</li>
<li>Track lines per picker-hour and orders shipped by the cut-off.</li>
</ul>
<p>Earlier in this series: <a href="{W1}.html">Part&nbsp;1</a> won back space and re-slotted the fast movers. Next: <a href="{W3}.html">Part&nbsp;3</a> goes to the dock, where receiving, put-away and cross-docking decide how fast stock becomes pickable. Related: <a href="{ABC1}.html">ABC inventory analysis</a> for ranking SKUs by picks.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://doi.org/10.1016/j.ejor.2006.07.009" rel="noopener" target="_blank">De Koster, Le-Duc and Roodbergen (2007), Design and control of warehouse order picking: a literature review, European Journal of Operational Research</a> (travel share of picking time, routing and batching methods)</li>
<li><a href="https://www.goramp.com/blog/warehouse-slotting-guide" rel="noopener" target="_blank">Ramp: Warehouse slotting guide</a> (travel share of pick time)</li>
</ul>
{NOTE}{js3d("wh3d2")}"""
    body = nowrap(body, [(1, 0, 40), (2, 0, 14), (3, 1, 14), (5, 0, 30)])
    return dict(slug=W2, title="Pickers Walk Half the Day: Pick Methods and Pick Paths for SME Warehouses",
                desc="Single-order, batch, zone and wave picking compared in one warehouse, with return and S-shape routes and the picker-hours each one takes.",
                cats=["operational-efficiency", "inventory-management"], tags=["order picking", "batch picking", "zone picking", "wave picking", "pick path", "warehouse productivity"],
                body=body, date=DATE, author="Quak Foo Lee", read="10 min read", series=SER(2), cover_label="Warehouse operations",
                related=[W1, ABC1, OEE1])


if __name__ == "__main__":
    a = part2()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])}\n")
