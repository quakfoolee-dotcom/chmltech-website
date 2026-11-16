"""Warehouse operations series for Insights (V5.38). Part 8: when does automation pay for an SME warehouse?

Same distributor as Parts 1 to 7. The numbers come from wh8_model.py, which also feeds the 3D model in Figure 2
(assets/js/wh3d8.js).

Usage:  python3 content/articles/wh8_articles.py
        python3 content/gen/add_article.py automation-roi-for-sme-warehouses-robots-pick-to-light-and-vertical-lifts
        python3 content/gen/series_labels.py
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import js3d, nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, PURPLE, MUTED, eq, tn, mathjs
import wh_model as W
import wh8_model as M
from wh_articles import W1, W2, SER
from wh3_articles import W3
from wh4_articles import W4
from wh5_articles import W5
from wh6_articles import W6
from wh7_articles import W7

DATE = "2026-11-16"
W8 = "automation-roi-for-sme-warehouses-robots-pick-to-light-and-vertical-lifts"
NOTE = ('<p class="oee-note"><em>The distributor, its volumes, labour times and equipment prices are an illustrative example built from stated '
        'assumptions and published price ranges. Real quotes vary widely. Chmltech does not sell or resell any automation equipment.</em></p>')
f0 = lambda x: f"{x:,.0f}"
f1 = lambda x: f"{x:,.1f}"
pc = lambda x: f"{x * 100:.0f}%"
money = lambda x: f"${round(x, -2 if abs(x) < 10000 else -3):,.0f}"
AUTO = ["ptl", "vlm", "amr"]
NOW = {o: M.run(o, M.TODAY) for o in AUTO}
COL = {"ptl": ORANGE, "vlm": PURPLE, "amr": GREEND}
PV = {o: M.payback_volume(o) for o in AUTO}
PV_NS = M.payback_volume("vlm", space=False)


def yrs(p): return "Never" if p is None else (f"{p:.1f} years" if p < 10 else "Over 10 years")


def fig_payback():
    x0, y0, w, h = 66, 26, 540, 240; xmin, xmax, ymax = 150, 900, 10; s = ""
    X = lambda v: x0 + (v - xmin) / (xmax - xmin) * w; Y = lambda p: y0 + h - min(ymax, p) / ymax * h
    s += f'<rect x="{x0}" y="{Y(3):.1f}" width="{w}" height="{Y(0) - Y(3):.1f}" fill="{GREEN}" opacity=".12"/>' + txt(x0 + 8, Y(3) + 16, "Pays back within 3 years", fill=GREEND, fs=12, bold=True)
    for p in range(0, ymax + 1, 2): s += f'<line x1="{x0}" y1="{Y(p):.1f}" x2="{x0 + w}" y2="{Y(p):.1f}" stroke="#E4E1D8"/>' + txt(x0 - 8, Y(p) + 4, f"{p}" + ("+" if p == ymax else ""), "end", MUTED, 12)
    for v in (150, 300, 450, 600, 750, 900): s += txt(X(v), y0 + h + 18, f0(v), "middle", MUTED, 12)
    xt = X(M.TODAY); s += f'<line x1="{xt:.1f}" y1="{y0}" x2="{xt:.1f}" y2="{y0 + h}" stroke="{NAVY}" stroke-dasharray="4 4"/>' + txt(xt + 6, y0 + 12, f"Today: {M.TODAY} a day", fill=NAVY, fs=12, bold=True)
    ends = []
    for o, space, dash, lab in (("ptl", True, "", "Pick-to-light"), ("vlm", True, "", "Vertical lifts, space needed"), ("vlm", False, "6 4", "Vertical lifts, space not needed"), ("amr", True, "", "Mobile robots")):
        vs = list(range(150, 901, 10)); seg = []; segs = []
        for v in vs:
            p = M.run(o, v, space)["payback"]
            if p is None or p > ymax: (segs.append(seg) if seg else None); seg = []; continue
            seg.append(f"{X(v):.1f},{Y(p):.1f}")
        if seg: segs.append(seg)
        for sg in segs:
            if len(sg) > 1: s += f'<polyline points="{" ".join(sg)}" fill="none" stroke="{COL[o]}" stroke-width="2.6"{f" stroke-dasharray=\"{dash}\"" if dash else ""}/>'
        p9 = M.run(o, 900, space)["payback"]; ends.append([Y(p9 if p9 else ymax), lab, COL[o]])
    ends.sort()
    for i in range(1, len(ends)): ends[i][0] = max(ends[i][0], ends[i - 1][0] + 15)
    for y, lab, col in ends: s += txt(x0 + w + 6, y + 4, lab, fill=col, fs=12, bold=True)
    s += f'<text x="16" y="{y0 + h / 2}" transform="rotate(-90 16 {y0 + h / 2})" text-anchor="middle" font-size="12.5" font-weight="600" fill="{NAVY}">Payback (years)</text>'
    s += txt(x0 + w / 2, y0 + h + 38, "Orders a day", "middle", NAVY, 12.5, True)
    return svg(f"Line chart of payback in years against orders a day, from 150 to 900, for three automations. Pick-to-light pays back within three years from about {PV['ptl']} orders a day. "
               f"Vertical lift modules do so from about {PV['vlm']} if the floor they free is needed, and from about {f0(PV_NS)} if it is not. Mobile robots do so from about {PV['amr']}. "
               f"At today's {M.TODAY} orders a day none of them pays back within three years.", 800, 316, s, 600)


def fig_bars():
    x0, w = 210, 380; mx = max(max(NOW[o]["saving"], NOW[o]["run"]) for o in AUTO); sc = w / mx; s = ""
    s += f'<rect x="20" y="6" width="12" height="12" fill="{GREEND}"/>' + txt(37, 16, "Yearly saving (labour, errors, space)", fs=12)
    s += f'<rect x="300" y="6" width="12" height="12" fill="{RED}"/>' + txt(317, 16, "Yearly running cost (fees, maintenance)", fs=12)
    for i, o in enumerate(AUTO):
        r = NOW[o]; y = 40 + i * 62
        s += txt(x0 - 10, y + 24, M.ONAME[o], "end", NAVY, 13, True)
        s += f'<rect x="{x0}" y="{y}" width="{r["saving"] * sc:.1f}" height="20" fill="{GREEND}"/>' + txt(x0 + r["saving"] * sc + 6, y + 15, money(r["saving"]), fill=NAVY, fs=12)
        s += f'<rect x="{x0}" y="{y + 24}" width="{r["run"] * sc:.1f}" height="20" fill="{RED}"/>' + txt(x0 + r["run"] * sc + 6, y + 39, money(r["run"]), fill=NAVY, fs=12)
    return svg(f"Paired bars at {M.TODAY} orders a day. Pick-to-light saves {money(NOW['ptl']['saving'])} a year against {money(NOW['ptl']['run'])} running cost; vertical lifts save {money(NOW['vlm']['saving'])} "
               f"against {money(NOW['vlm']['run'])}, most of it floor space; mobile robots save {money(NOW['amr']['saving'])} against {money(NOW['amr']['run'])} in robot fees.", 720, 40 + 3 * 62, s, 560)


def figure_data():
    R = {}
    for o in M.OPTS:
        rows = []
        for v in M.VOLS:
            r = M.run(o, v)
            rows.append([round(r["one"], -3), round(r["run"], -2), round(r["saving"], -2), round(r["net"], -2), None if r["payback"] is None else round(r["payback"], 1),
                         round(r["labour_h"], 1), r["units"], round(r["freed"]), round(r.get("util", r.get("tray_load", 0)), 2)])
        R[o] = rows
    data = dict(opts=M.OPTS, onames=[M.ONAME[o] for o in M.OPTS], vols=M.VOLS, today=M.VOLS.index(M.TODAY), R=R, caseShare=M.CASE_SHARE, lines=M.LINES,
                ptlLocs=M.PTL["locs"], vlmUnits=M.VLM["units"], freedM2=round(M.SHELF_M2 * (1 - M.VLM["footprint"])))
    data["bld"] = [W.BLD_X, W.BLD_Z, W.CLEAR_H]; data["rows"] = W.ROW_Z; data["bays"] = W.BAYS; data["bayW"] = W.BAY_W; data["rowD"] = W.ROW_D
    data["x0"] = W.RACK_X0; data["levels"] = W.LEVELS_NEW; data["beam"] = W.BEAM; data["aisles"] = W.AISLE_Z; data["rowAisle"] = W.ROW_AISLE; data["perBay"] = W.PER_BAY
    return data


def figure_markup():
    js = json.dumps(figure_data(), separators=(",", ":"))
    ob = "".join(f'<button type="button" class="wh3d-btn" data-o="{o}" aria-pressed="{"true" if o == "base" else "false"}">{M.ONAME[o]}</button>' for o in M.OPTS)
    vb = "".join(f'<button type="button" class="wh3d-btn wh3d-small" data-v="{M.VOLS.index(v)}">{v}{" (today)" if v == M.TODAY else ""}</button>' for v in M.STEPS)
    return f"""<p>Figure 2 shows each automation in the example's warehouse. Pick-to-light puts green lights on the fastest shelving locations; the vertical lift modules replace the shelving with two towers and free the floor around them; the mobile robots carry totes up and down the rack aisles while each picker stays in a zone. Choose an option and a volume, or Compare all, and click the chart to try any volume from 150 to 900 orders a day.</p>
<figure class="wh3d wh3d8" id="wh3d8">
<div class="wh3d-box">
<div class="wh3d-stage">
<canvas role="img" aria-label="3D model of the example distributor's warehouse with pallet racks at the front and small-parts shelving at the back. With pick-to-light, lights flash on the shelving where pickers pick. With vertical lift modules, the shelving is replaced by two tall towers with pickers at their windows, and the freed floor is highlighted. With mobile robots, small robots carrying totes drive through the rack aisles to pickers who stay in their zones. In the compare view the four set-ups are shown side by side."></canvas>
<span class="wh3d-drag" aria-hidden="true">Drag to turn</span>
<span class="wh3d-chip" id="wh3d8-chip">300 orders a day</span>
<p class="wh3d-nogl" id="wh3d8-nogl" hidden>This browser cannot show the 3D model. The controls below still update the numbers.</p>
</div>
<div class="wh3d-panel">
<div class="wh3d6-row" role="group" aria-label="Set-up">{ob}<button type="button" class="wh3d-btn" data-o="all" aria-pressed="false">Compare all</button></div>
<div class="wh3d6-weeks" role="group" aria-label="Orders a day"><span>Orders a day</span>{vb}</div>
<div class="wh3d5-tour" id="wh3d8-tour" aria-hidden="true"><b><i></i></b><span></span></div>
<div class="wh3d-cells">
<div class="wh3d-cell wh3d-key"><span class="k">One-time cost</span><strong id="wh3d8-one"></strong></div>
<div class="wh3d-cell wh3d-key"><span class="k">Payback</span><strong id="wh3d8-pb"></strong></div>
<div class="wh3d-cell"><span class="k">Yearly saving</span><strong id="wh3d8-sav"></strong></div>
<div class="wh3d-cell"><span class="k">Yearly running cost</span><strong id="wh3d8-run"></strong></div>
<div class="wh3d-cell"><span class="k">Labour hours saved a day</span><strong id="wh3d8-hrs"></strong></div>
<div class="wh3d-cell"><span class="k">Equipment</span><strong id="wh3d8-eq"></strong></div>
</div>
<div class="wh3d6-year" aria-label="Chart of payback in years against orders a day for the three automations. Click to choose a volume."><svg id="wh3d8-csvg" viewBox="0 0 600 90" preserveAspectRatio="none"></svg><p><span>Payback (0 to 8 years) from 150 to 900 orders a day; the line marks 3 years. Click to choose a volume.</span><span id="wh3d8-cv"></span></p></div>
<p class="wh3d-say" id="wh3d8-say" aria-live="polite"></p>
<div class="wh3d-last"><ul class="wh3d-legend"><li><i style="background:#3f86e8;border-radius:50%"></i>Picker</li><li><i style="background:#6EF07A"></i>Pick light</li><li><i style="background:#B07CFF"></i>Vertical lift module</li><li><i style="background:#FF8A3D"></i>Robot with tote</li><li><i style="background:rgba(110,205,105,.6)"></i>Floor freed</li></ul></div>
</div>
</div>
<figcaption>Figure 2. The example's warehouse with each automation. The money, hours and equipment in the panel come from the same model as Figure&nbsp;1 and the tables. Vertical lift paybacks count the freed floor at ${M.RENT_FT2:.2f} a square foot a year; without that value they are much longer.</figcaption>
<script type="application/json" id="wh3d8-data">{js}</script>
</figure>
"""


def part8():
    p, v, a = M.PTL, M.VLM, M.AMR
    case, each = M.lines(M.TODAY)
    res = "".join(f'<tr><td>{M.ONAME[o]}</td><td class="num">{money(NOW[o]["one"])}</td><td class="num">{money(NOW[o]["run"])}</td><td class="num">{f1(NOW[o]["labour_h"])}</td>'
                  f'<td class="num">{money(NOW[o]["saving"])}</td><td class="num">{yrs(NOW[o]["payback"])}</td><td class="num">{f0(PV[o])}</td></tr>' for o in AUTO)
    big = {o: M.run(o, 900) for o in AUTO}
    res9 = "".join(f'<tr><td>{M.ONAME[o]}</td><td class="num">{money(big[o]["one"])}</td><td class="num">{money(big[o]["run"])}</td><td class="num">{f1(big[o]["labour_h"])}</td>'
                   f'<td class="num">{money(big[o]["saving"])}</td><td class="num">{yrs(big[o]["payback"])}</td></tr>' for o in AUTO)
    body = f"""{CSS}
<p>The trade shows are full of robots. Mobile robots glide between racks, towers of trays deliver parts to a waist-high window, and every pick face glows green. The brochures promise two or three times the productivity and payback inside two years. For a warehouse of 15 people, the question is simpler: <em>will it pay here, and when?</em></p>
<p>This last part of the series answers that for the same distributor as Parts&nbsp;1 to 7, now running a cloud WMS (<a href="{W7}.html">Part&nbsp;7</a>). Every automation below needs one: the robots, lights and lifts take their orders from it. The answer depends mostly on volume, and on whether the floor space matters.</p>
<h2>Three automations an SME can actually buy</h2>
<table>
<tr><th>Automation</th><th>What it does</th><th>Where in the example</th><th>Price used</th></tr>
<tr><td>Pick-to-light</td><td>A light and a display at each location show the picker where to pick and how many; a button confirms</td><td>The {p["locs"]} fastest shelving locations, which take {pc(p["a_share"])} of small-item lines</td><td>${f0(p["per_loc"])} a location installed, plus {money(p["software"])} software; {pc(p["maint"])} a year to maintain</td></tr>
<tr><td>Vertical lift modules</td><td>Enclosed towers of trays; the machine brings the tray to a pick window, so the picker does not walk</td><td>{v["units"]} towers replace the shelving area of about {f0(M.SHELF_M2)} m&sup2;</td><td>${f0(v["per_ft"])} a foot of height, {v["height_ft"]} ft each, plus {money(v["install"])} installation; {money(v["maint"])} a tower a year</td></tr>
<tr><td>Mobile robots</td><td>Robots carry the totes through the aisles and stop at the picker, who stays in a zone and only picks</td><td>The pallet racks, where {pc(M.CASE_SHARE)} of lines are case picks</td><td>{money(a["fee"])} a robot a month (robots as a service), minimum {a["min_fleet"]} robots, plus {money(a["setup"])} set-up</td></tr>
</table>
<p>The prices sit inside published ranges. Pick-to-light hardware runs about $150 a light device, which is why it is usually limited to a subset of locations. Vertical lift modules typically cost $6,500 to $8,500 a linear foot of height, and vendors quote space savings of up to 85% against shelving. Robots as a service typically costs $2,000 to $8,000 a robot a month, and vendors quote two to three times the picking productivity with collaborative robots.</p>
<h2>What each one saves</h2>
<p>At {M.TODAY} orders a day the example picks about {f0(case)} case lines and {f0(each)} small-item lines a day. With scanners and a WMS, a case line takes about {M.T_CASE:.1f} minutes and a small-item line about {M.T_EACH:.1f} minutes, most of it walking and finding. Each automation cuts part of that:</p>
<ul>
<li><strong>Pick-to-light</strong> cuts the time on the lit locations by {pc(p["cut"])}, within the 30% to 50% gain usually quoted, and halves the errors there.</li>
<li><strong>Vertical lift modules</strong> cut small-item time by {pc(v["cut"])}, because the tray comes to the picker, and free about {pc(1 - v["footprint"])} of the shelving floor: about {f0(M.SHELF_M2 * (1 - v["footprint"]))} m&sup2;.</li>
<li><strong>Mobile robots</strong> halve the time on case lines: the picker stops walking with a cart. Each robot handles about {f0(a["lines_h"])} lines an hour.</li>
</ul>
{eq(r"\text{Payback (years)} = \dfrac{\text{one-time cost}}{\text{labour saved} + \text{errors avoided} + \text{space freed} - \text{running cost}}")}
<p>Labour is valued at ${f0(M.WAGE)} an hour, as in Parts&nbsp;5 to 7. Freed floor is valued at ${M.RENT_FT2:.2f} a square foot a year, the Canadian industrial rent used in <a href="{W1}.html">Part&nbsp;1</a>, but only if the business needs the space: if it saves a move or an extension. Floor that sits empty saves nothing.</p>
<h2>The result at {M.TODAY} orders a day</h2>
<table>
<tr><th>Automation</th><th class="num">One-time cost</th><th class="num">Running cost a year</th><th class="num">Labour hours saved a day</th><th class="num">Saving a year</th><th class="num">Payback</th><th class="num">Pays in 3 years from</th></tr>
{res}
</table>
{fig(fig_bars(), 1, f"Yearly saving against yearly running cost at {M.TODAY} orders a day. Only the vertical lifts clear their running cost by much, and mostly because of the floor they free.")}
<p><strong>At today's volume, nothing pays back within three years.</strong> That is the honest answer for this warehouse, and for many SMEs. The example saves {f1(NOW["ptl"]["labour_h"])} hours a day with pick-to-light, {f1(NOW["vlm"]["labour_h"])} with the lifts and {f1(NOW["amr"]["labour_h"])} with robots, a fraction of one person each, because the work is spread across a small team on one shift.</p>
<p><strong>Robots cost more than they save.</strong> Three robots at {money(a["fee"])} a month are {money(NOW["amr"]["run"])} a year. They save {money(NOW["amr"]["saving"])} in labour. At {M.TODAY} orders a day one robot would be enough for the work, but vendors set a minimum fleet, and on one shift the robots stand idle for two-thirds of the day.</p>
<p><strong>Vertical lifts pay if the space is needed.</strong> At {yrs(NOW["vlm"]["payback"]).lower()}, the lifts come closest, but {money(NOW["vlm"]["space"])} of their {money(NOW["vlm"]["saving"])} yearly saving is floor rent. If the business is not short of space, the payback stretches past ten years. If it is about to sign a lease on a second building, the lifts are worth a serious look.</p>
<p><strong>Pick-to-light is cheap but has little to save.</strong> At {money(NOW["ptl"]["one"])} it is the cheapest to buy, but it only speeds up {f0(each * p["a_share"])} lines a day.</p>
{figure_markup()}<h2>When each one pays</h2>
{fig(fig_payback(), 3, "Payback against volume. Each automation crosses the three-year line at its own volume; the lifts much earlier if the freed floor is needed.")}
<p>Figure&nbsp;3 shows the same calculation across volumes. Savings grow with every order, while most costs do not, so every option gets better with growth:</p>
<ul>
<li><strong>Pick-to-light</strong> pays back within three years from about {PV["ptl"]} orders a day.</li>
<li><strong>Vertical lift modules</strong> do so from about {PV["vlm"]} if the space is needed, and only from about {f0(PV_NS)} if it is not.</li>
<li><strong>Mobile robots</strong> do so from about {PV["amr"]}, when the minimum fleet is fully used. Above that their payback keeps falling quickly, because the fleet grows only as fast as the work.</li>
</ul>
<p>At 900 orders a day, three times today's volume:</p>
<table>
<tr><th>Automation</th><th class="num">One-time cost</th><th class="num">Running cost a year</th><th class="num">Labour hours saved a day</th><th class="num">Saving a year</th><th class="num">Payback</th></tr>
{res9}
</table>
<h2>Before you automate</h2>
<p>The earlier parts of this series cost far less than any of these machines, and each one makes automation cheaper later:</p>
<table>
<tr><th>Part</th><th>Problem</th><th>Low-cost fix</th></tr>
<tr><td><a href="{W1}.html">1</a></td><td>Out of space</td><td>Re-beam the racks, combine partial pallets, clear dead stock and re-slot by velocity</td></tr>
<tr><td><a href="{W2}.html">2</a></td><td>Pickers walk half the day</td><td>Batch and zone picking with better routes</td></tr>
<tr><td><a href="{W3}.html">3</a></td><td>Trucks wait at the dock</td><td>Dock appointments, scanning at receiving and cross-docking</td></tr>
<tr><td><a href="{W4}.html">4</a></td><td>Phantom stock</td><td>Cycle counting by ABC class</td></tr>
<tr><td><a href="{W5}.html">5</a></td><td>Errors reach customers</td><td>Scan at pick and pack, weigh at ship</td></tr>
<tr><td><a href="{W6}.html">6</a></td><td>Panic at the peak</td><td>Forecast in hours, planned temps and a cross-trained crew</td></tr>
<tr><td><a href="{W7}.html">7</a></td><td>Spreadsheets stop scaling</td><td>The right system for the volume: the ERP module or a cloud WMS</td></tr>
</table>
<p>Automation on a disorganised floor automates the disorder. Robots need clean locations and a WMS; lifts need a clean item master and slotting; lights need accurate stock.</p>
<h2>How to buy automation without regret</h2>
<ul>
<li><strong>Start from your own numbers.</strong> Lines a day by type, minutes a line, wage, space cost and growth. A vendor's case study is someone else's warehouse.</li>
<li><strong>Test the payback at today's volume and at your growth plan.</strong> If it only pays at three times today's volume, wait or rent.</li>
<li><strong>Rent before you buy.</strong> Robots as a service and short pilots let you prove the gain on your floor; ask for 60 to 90 days with an exit.</li>
<li><strong>Count the floor only if you need it.</strong> Freed space is worth rent only if it saves a move or an extension.</li>
<li><strong>Plan for the second shift.</strong> Machines that stand idle for 16 hours a day pay back slowly. A second shift can halve the payback.</li>
<li><strong>Check the WMS link first.</strong> The integration between the automation and the WMS is where projects go late.</li>
</ul>
<h2>Common mistakes</h2>
<ul>
<li><strong>Believing "two to three times the productivity" applies to the whole warehouse.</strong> It applies to the work the machine touches. In the example, robots touch case picking only.</li>
<li><strong>Ignoring the minimum fleet.</strong> A small warehouse pays for robots it cannot keep busy.</li>
<li><strong>Counting freed floor that will sit empty.</strong></li>
<li><strong>Automating before fixing.</strong> Slotting, batching and scanning are cheaper and often enough.</li>
<li><strong>Forgetting maintenance and support.</strong> Lights, lifts and robots need spares, service contracts and someone on site who understands them.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>Automation pays when there is enough work for it. Most savings grow with volume; most costs do not.</li>
<li>At the example's {M.TODAY} orders a day, none of the three options pays back within three years.</li>
<li>Pick-to-light pays from about {PV["ptl"]} orders a day, vertical lifts from about {PV["vlm"]} if the space is needed, and mobile robots from about {PV["amr"]}.</li>
<li>Rent and pilot before you buy, and count freed floor only if you need it.</li>
<li>Fix the process first. The seven earlier parts of this series cost far less and make automation work better later.</li>
</ul>
<p>This is the last part of the warehouse operations series: <a href="{W1}.html">Part&nbsp;1</a> space, <a href="{W2}.html">Part&nbsp;2</a> picking, <a href="{W3}.html">Part&nbsp;3</a> the dock, <a href="{W4}.html">Part&nbsp;4</a> stock records, <a href="{W5}.html">Part&nbsp;5</a> errors, <a href="{W6}.html">Part&nbsp;6</a> labour and <a href="{W7}.html">Part&nbsp;7</a> the WMS.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://og.mhi.org/ofs/solutions-guide/pick-to-light" rel="noopener" target="_blank">MHI: Pick to Light solutions guide</a></li>
<li><a href="https://inviarobotics.com/?p=16247717" rel="noopener" target="_blank">inVia Robotics: Goods-to-person automation through pick-to-light technology</a></li>
<li><a href="https://www.southwestsolutions.com/automated-storage/vertical-lift-module/" rel="noopener" target="_blank">Southwest Solutions: Vertical lift module solutions</a></li>
<li><a href="https://og.mhi.org/solutions-community/solutions-guide/vertical-lift" rel="noopener" target="_blank">MHI: Vertical lift solutions guide</a></li>
<li><a href="https://robotomated.com/learn/cost/warehouse-robot-cost-guide" rel="noopener" target="_blank">Robotomated: Warehouse robot cost guide</a></li>
</ul>
{NOTE}{js3d("wh3d8")}{mathjs()}"""
    body = nowrap(body, [(1, 0, 22), (2, 0, 22), (3, 0, 22)])
    return dict(slug=W8, title="Automation ROI for SME Warehouses: Robots, Pick-to-Light and Vertical Lifts",
                desc="Mobile robots, pick-to-light and vertical lift modules in one SME warehouse: what each costs and saves, and the volume at which each pays back.",
                cats=["operational-efficiency", "digital-technology"], tags=["warehouse automation", "AMR", "pick-to-light", "vertical lift module", "automation ROI", "robots as a service"],
                body=body, date=DATE, author="Quak Foo Lee", read="10 min read", series=SER(8), cover_label="Warehouse operations",
                related=[W7, W2, W1])


if __name__ == "__main__":
    a = part8()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])}\n")
