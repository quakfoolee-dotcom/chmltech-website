"""Warehouse operations series for Insights (V5.37). Part 7: when does an SME need a warehouse management system?

Same distributor as Parts 1 to 6. The numbers come from wh7_model.py, which also feeds the 3D model in Figure 2
(assets/js/wh3d7.js).

Usage:  python3 content/articles/wh7_articles.py
        python3 content/gen/add_article.py do-we-need-a-wms-yet-when-spreadsheets-stop-scaling
        python3 content/gen/series_labels.py
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import js3d, nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, PURPLE, MUTED, eq, tn, mathjs
import wh_model as W
import wh7_model as M
from wh_articles import W1, W2, SER
from wh3_articles import W3
from wh4_articles import W4
from wh5_articles import W5
from wh6_articles import W6
sys.path.insert(0, os.path.join(HERE, "..", "gen"))
from wms_demo_links import ARTICLE as WMS_DEMO  # V5.73: link to the Chmltech WMS demo showcase

DATE = "2026-11-16"
W7 = "do-we-need-a-wms-yet-when-spreadsheets-stop-scaling"
NOTE = ('<p class="oee-note"><em>The distributor, its volumes, labour times, error rates and software prices are an illustrative example built from stated '
        'assumptions and published price ranges. Real quotes vary widely by vendor, users and scope. The four options are generic categories, not named products; '
        'Chmltech\'s own WMS is not one of them.</em></p>')
f0 = lambda x: f"{x:,.0f}"
f1 = lambda x: f"{x:,.1f}"
pc = lambda x: f"{x * 100:.0f}%"
money = lambda x: f"${round(x, -2 if abs(x) < 10000 else -3):,.0f}"
T = M.table()
NOW = {o: M.run(o, M.TODAY) for o in M.OPTS}
COL = {"sheet": RED, "erp": ORANGE, "cloud": GREEND, "tier1": PURPLE}
X_SE, X_EC, X_CT = M.crossover("sheet", "erp"), M.crossover("erp", "cloud"), M.crossover("cloud", "tier1")
PB = {o: M.payback(o) for o in M.OPTS}


def fig_curve():
    x0, y0, w, h = 66, 26, 560, 240; xmax, ymax = 1200, 24; s = ""
    X = lambda v: x0 + (v - 50) / (xmax - 50) * w; Y = lambda c: y0 + h - c / ymax * h
    for c in range(0, ymax + 1, 4): s += f'<line x1="{x0}" y1="{Y(c):.1f}" x2="{x0 + w}" y2="{Y(c):.1f}" stroke="#E4E1D8"/>' + txt(x0 - 8, Y(c) + 4, f"${c}", "end", MUTED, 12)
    for v in (50, 200, 400, 600, 800, 1000, 1200): s += txt(X(v), y0 + h + 18, f0(v), "middle", MUTED, 12)
    # cheapest option along the bottom
    for i, v in enumerate(M.VOLS[:-1]):
        s += f'<rect x="{X(v):.1f}" y="{y0 + h - 7}" width="{X(M.VOLS[i + 1]) - X(v):.1f}" height="7" fill="{COL[M.cheapest((v + M.VOLS[i + 1]) / 2)]}" opacity=".85"/>'
    xt = X(M.TODAY); s += f'<line x1="{xt:.1f}" y1="{y0}" x2="{xt:.1f}" y2="{y0 + h}" stroke="{NAVY}" stroke-dasharray="4 4"/>' + txt(xt + 6, y0 + 12, f"The example today: {M.TODAY} a day", fill=NAVY, fs=12, bold=True)
    ends = []
    for o in M.OPTS:
        pts = " ".join(f"{X(r['v']):.1f},{Y(min(ymax, r['per_order'])):.1f}" for r in T[o])
        s += f'<polyline points="{pts}" fill="none" stroke="{COL[o]}" stroke-width="2.6"/>'
        ends.append([Y(T[o][-1]["per_order"]), o])
    ends.sort()
    for i in range(1, len(ends)): ends[i][0] = max(ends[i][0], ends[i - 1][0] + 15)
    for y, o in ends: s += txt(x0 + w + 6, y + 4, f"{M.ONAME[o]}", fill=COL[o], fs=12, bold=True)
    s += f'<text x="16" y="{y0 + h / 2}" transform="rotate(-90 16 {y0 + h / 2})" text-anchor="middle" font-size="12.5" font-weight="600" fill="{NAVY}">Cost an order</text>'
    s += txt(x0 + w / 2, y0 + h + 38, "Orders a day", "middle", NAVY, 12.5, True)
    return svg(f"Line chart of total warehouse cost an order against orders a day, from 50 to 1,200, for four options. Paper and a spreadsheet is cheapest below about {X_SE} orders a day, "
               f"the ERP module with scanners from there to about {X_EC}, and a cloud WMS above that. The enterprise WMS stays dearer than the cloud WMS until about {f0(X_CT)} orders a day, beyond the chart. "
               f"A strip along the bottom shows the cheapest option at each volume.", 790, 316, s, 600)


def fig_stack():
    parts = [("software", "Software and devices", PURPLE), ("xfloor", "Floor labour above the lowest", BLUE), ("office", "Office keying and checking", "#7FA6D6"),
             ("count", "Counting", "#9AB3A0"), ("errors", "Errors reaching customers", RED), ("records", "Wrong stock records", ORANGE)]
    fmin = min(NOW[o]["cost"]["floor"] for o in M.OPTS)
    val = {o: dict(NOW[o]["cost"], xfloor=NOW[o]["cost"]["floor"] - fmin) for o in M.OPTS}
    tot = {o: sum(val[o][k] for k, _, _ in parts) for o in M.OPTS}
    x0, w = 200, 400; sc = w / max(tot.values()); out = ""; lx = 20
    for k, lab, col in parts:
        out += f'<rect x="{lx}" y="8" width="12" height="12" fill="{col}"/>' + txt(lx + 17, 18, lab, fs=12); lx += 26 + len(lab) * 6.3
        if lx > 600: lx = 20
    out2 = ""
    for i, o in enumerate(M.OPTS):
        y = 54 + i * 46; x = x0; out2 += txt(x0 - 10, y + 17, M.ONAME[o], "end", NAVY, 13, o == "cloud")
        for k, _, col in parts:
            ww = val[o][k] * sc; out2 += f'<rect x="{x:.1f}" y="{y}" width="{ww:.1f}" height="24" fill="{col}"/>'; x += ww
        out2 += txt(x + 8, y + 17, money(tot[o]), fill=NAVY, fs=13, bold=True)
    # legend in two lines
    leg = ""; lx, ly = 20, 14
    for k, lab, col in parts:
        wlab = 24 + len(lab) * 6.4
        if lx + wlab > 700: lx, ly = 20, ly + 20
        leg += f'<rect x="{lx}" y="{ly - 10}" width="12" height="12" fill="{col}"/>' + txt(lx + 17, ly, lab, fs=12); lx += wlab + 10
    return svg(f"Stacked bars at {M.TODAY} orders a day of each option's yearly cost besides the floor labour all four share: software and devices, extra floor labour, office keying, counting, "
               f"errors and wrong stock records. Paper and a spreadsheet is {money(tot['sheet'])}, the ERP module {money(tot['erp'])}, the cloud WMS {money(tot['cloud'])} and the enterprise WMS {money(tot['tier1'])}.",
               720, 54 + 4 * 46, leg + out2, 560)


def figure_data():
    R = {}
    for o in M.OPTS:
        R[o] = [[round(r["total"], -3), round(r["per_order"], 2), r["floor_n"], round(r["v"] * M.O[o]["err"], 2), r["acc"], round(r["h"] * 60, 1)] for r in T[o]]
    data = dict(opts=M.OPTS, onames=[M.ONAME[o] for o in M.OPTS], vols=M.VOLS, steps=[M.VOLS.index(v) if v in M.VOLS else None for v in M.STEPS], today=M.VOLS.index(M.TODAY),
                lag=[M.O[o]["lag"] for o in M.OPTS], lagH=[M.O[o]["lag_h"] for o in M.OPTS], R=R, lines=M.LINES)
    data["bld"] = [W.BLD_X, W.BLD_Z, W.CLEAR_H]; data["rows"] = W.ROW_Z; data["bays"] = W.BAYS; data["bayW"] = W.BAY_W; data["rowD"] = W.ROW_D
    data["x0"] = W.RACK_X0; data["levels"] = W.LEVELS_NEW; data["beam"] = W.BEAM; data["aisles"] = W.AISLE_Z; data["rowAisle"] = W.ROW_AISLE; data["perBay"] = W.PER_BAY
    return data


def figure_markup():
    js = json.dumps(figure_data(), separators=(",", ":"))
    ob = "".join(f'<button type="button" class="wh3d-btn" data-o="{o}" aria-pressed="{"true" if o == "sheet" else "false"}">{M.ONAME[o]}</button>' for o in M.OPTS)
    vb = "".join(f'<button type="button" class="wh3d-btn wh3d-small" data-v="{M.VOLS.index(v)}">{v}{" (today)" if v == M.TODAY else ""}</button>' for v in M.STEPS if v in M.VOLS)
    return f"""<p>Figure 2 runs the example's warehouse through a day on each of the four options. Every pallet is coloured by what the system knows about it: steel blue when the record is right, grey when something has moved that the system does not know about yet, and red when the record is wrong. Pickers with paper carry their lists back to the office, where they wait to be keyed in at the end of the shift; pickers with scanners send each pick to the system as it happens, shown as a cyan spark. Choose an option and a volume, or Compare all, and click the chart to try any volume.</p>
<figure class="wh3d wh3d7" id="wh3d7">
<div class="wh3d-box">
<div class="wh3d-stage">
<canvas role="img" aria-label="3D model of the example distributor's warehouse through a working day. Pallets in the racks are coloured by whether the stock record is right, not yet updated or wrong. Pickers walk the aisles to the packing area; with paper they bring their pick lists to an office desk where the pile grows until it is keyed in, and with scanners each pick sends a spark to the office system at once. In the compare view the four options are shown side by side."></canvas>
<span class="wh3d-drag" aria-hidden="true">Drag to turn</span>
<span class="wh3d-chip" id="wh3d7-chip">300 orders a day · 06:00</span>
<p class="wh3d-nogl" id="wh3d7-nogl" hidden>This browser cannot show the 3D model. The controls below still update the numbers.</p>
</div>
<div class="wh3d-panel">
<div class="wh3d6-row" role="group" aria-label="System">{ob}<button type="button" class="wh3d-btn" data-o="all" aria-pressed="false">Compare all</button></div>
<div class="wh3d6-weeks" role="group" aria-label="Orders a day"><span>Orders a day</span>{vb}</div>
<div class="wh3d5-tour" id="wh3d7-tour" aria-hidden="true"><b><i></i></b><span></span></div>
<div class="wh3d-cells">
<div class="wh3d-cell wh3d-key"><span class="k">Warehouse cost a year</span><strong id="wh3d7-cost"></strong></div>
<div class="wh3d-cell wh3d-key"><span class="k">Cost an order</span><strong id="wh3d7-cpo"></strong></div>
<div class="wh3d-cell"><span class="k">Floor people</span><strong id="wh3d7-ppl"></strong></div>
<div class="wh3d-cell"><span class="k">Errors reaching customers a day</span><strong id="wh3d7-err"></strong></div>
<div class="wh3d-cell"><span class="k">Stock records right</span><strong id="wh3d7-acc"></strong></div>
<div class="wh3d-cell"><span class="k">System up to date within</span><strong id="wh3d7-lag"></strong></div>
</div>
<div class="wh3d6-year" aria-label="Chart of cost an order against orders a day for the four options. Click to choose a volume."><svg id="wh3d7-csvg" viewBox="0 0 600 90" preserveAspectRatio="none"></svg><p><span>Cost an order ($5 to $14) from 50 to 1,200 orders a day. Click to choose a volume.</span><span id="wh3d7-cv"></span></p></div>
<p class="wh3d-say" id="wh3d7-say" aria-live="polite"></p>
<div class="wh3d-last"><ul class="wh3d-legend"><li><i style="background:#5D7FA8"></i>Record right</li><li><i style="background:#B9C2CE"></i>Not in the system yet</li><li><i style="background:#FF5A4A"></i>Record wrong</li><li><i style="background:#5FE3FF;border-radius:50%"></i>Scan sent to the system</li><li><i style="background:#FFFFFF"></i>Paper pick list</li></ul></div>
</div>
</div>
<figcaption>Figure 2. A day in the example's warehouse on each option. The share of red pallets is each option's stock-record error rate, and the grey pallets are the locations picked today that the system has not caught up with. The cost, people and error numbers come from the same model as Figure&nbsp;1 and the tables.</figcaption>
<script type="application/json" id="wh3d7-data">{js}</script>
</figure>
"""


def part7():
    o = M.O
    opt_rows = "".join(f'<tr><td>{M.ONAME[k]}</td><td>{d}</td><td class="num">{money(o[k]["impl"]) if o[k]["impl"] else "None"}</td><td>{sub}</td></tr>' for k, d, sub in (
        ("sheet", "Paper pick lists, a spreadsheet or the accounting package's stock list. Locations in people's heads", "$100 a month for printing and the spreadsheet"),
        ("erp", "The ERP's inventory module with bin locations and handheld scanners (Business Central, NetSuite, Acumatica, SAP Business One and similar)", f"${o['erp']['base']} a month plus ${o['erp']['user']} a user"),
        ("cloud", "A cloud WMS linked to the ERP: directed put-away, batch and wave picking, scan at pick and pack, cycle counts, labour reports", f"${f0(o['cloud']['base'])} a month plus ${o['cloud']['user']} a user"),
        ("tier1", "An enterprise WMS licensed through a systems integrator, with labour management and advanced slotting", f"${f0(o['tier1']['base'])} a month plus ${o['tier1']['user']} a user, and an IT administrator")))
    ass = "".join(f'<tr><td>{M.ONAME[k]}</td><td class="num">{o[k]["h"] * 60:.1f} min</td><td class="num">{o[k]["grow"] * 100:.0f}%</td><td class="num">{o[k]["office"]:.1f} min</td>'
                  f'<td class="num">{o[k]["err"] * 100:.2f}%</td><td class="num">{pc(o[k]["acc"]) if o[k]["acc"] < 0.99 else f"{o[k]["acc"] * 100:.1f}%"}</td><td>{o[k]["lag"]}</td></tr>' for k in M.OPTS)
    res = "".join(f'<tr{" class=\"oee-total\"" if k == "cloud" else ""}><td>{M.ONAME[k]}</td><td class="num">{NOW[k]["floor_n"]}</td><td class="num">{money(NOW[k]["cost"]["software"])}</td>'
                  f'<td class="num">{money(NOW[k]["cost"]["floor"] + NOW[k]["cost"]["office"] + NOW[k]["cost"]["count"])}</td><td class="num">{money(NOW[k]["cost"]["errors"] + NOW[k]["cost"]["records"])}</td>'
                  f'<td class="num">{money(NOW[k]["total"])}</td><td class="num">${NOW[k]["per_order"]:.2f}</td><td class="num">{money(M.one_time(k)) if k != "sheet" else "None"}</td>'
                  f'<td class="num">{(f"{PB[k]:.0f} months" if PB[k] < 24 else f"{PB[k] / 12:.0f} years") if PB[k] else "-"}</td></tr>' for k in M.OPTS)
    rs = M.run
    body = f"""{CSS}
<p>Every warehouse starts on paper. Someone prints the orders, walks the floor, ticks the lines and hands the sheets to the office, where they are keyed into a spreadsheet or the accounting package at the end of the day. With two people and a few hundred SKUs it works, because the people know where everything is.</p>
<p>Then the business grows. More SKUs, more locations, more people, a second shift, an e-commerce channel. The question arrives in every growing distributor sooner or later: <em>do we need a warehouse management system yet?</em> Vendors will say yes. The accountant looks at the subscription and says not yet. This part puts numbers on the question with the same distributor as Parts&nbsp;1 to 6, at any volume from 50 to 1,200 orders a day.</p>
<h2>What a WMS actually does</h2>
<p>A WMS is not mainly a stock list. The ERP or accounting system already knows how many of each item the company owns. A WMS knows <strong>where</strong> each one is, down to the location, and it tells people what to do next: where to put this pallet, which orders to pick together, which route to walk, which location to count today. Every move is confirmed with a scan, so the record changes the moment the stock does.</p>
<p>The options an SME usually weighs:</p>
<table>
<tr><th>Option</th><th>What it is</th><th class="num">Implementation</th><th>Subscription in the model</th></tr>
{opt_rows}
</table>
<p>The price ranges come from published guides: cloud WMS subscriptions typically run $100 to $500 a user a month, often with a monthly base fee, and small single-site operations commonly spend $25,000 to $75,000 in the first year including implementation, training and hardware. Enterprise systems with an integrator start in the hundreds of thousands. The model spreads implementation over five years and scanners over four.</p>
<h2>Where the money goes without one</h2>
<p>Software is the easy cost to see. The costs of running without it are spread across the floor and the office, and most of them grow faster than the business:</p>
<ul>
<li><strong>Searching.</strong> When locations live in people's heads, every new SKU, location and person adds searching. The model adds {o['sheet']['grow'] * 100:.0f}% to paper's floor time an order for every 1,000 orders a day of volume, against {o['cloud']['grow'] * 100:.0f}% for a WMS that directs every move.</li>
<li><strong>Keying.</strong> Every pick list, receipt and adjustment is typed in again by someone in the office, and someone answers the phone when a customer asks whether an item is in stock.</li>
<li><strong>Counting.</strong> Without location records, the only way to fix the books is a wall-to-wall count with the warehouse shut (<a href="{W4}.html">Part&nbsp;4</a>).</li>
<li><strong>Errors.</strong> Without a scan at pick and pack, about {o['sheet']['err'] * 100:.2f}% of orders reach the customer wrong, at $75 each (<a href="{W5}.html">Part&nbsp;5</a>).</li>
<li><strong>Wrong records.</strong> With {pc(o['sheet']['acc'])} of locations right, some orders hit a location that is empty or short: a search, a short shipment or a rush order.</li>
</ul>
<p>The assumptions behind the four options:</p>
<table>
<tr><th>Option</th><th class="num">Floor time an order</th><th class="num">Added a 1,000 orders a day</th><th class="num">Office time an order</th><th class="num">Orders reaching customers wrong</th><th class="num">Stock records right</th><th>System up to date within</th></tr>
{ass}
</table>
{eq(r"\text{Cost a year} = \text{software} + \text{floor} + \text{office} + \text{counting} + \underbrace{\text{orders} \times \text{error rate} \times \$75}_{\text{errors}} + \underbrace{\text{lines} \times (1-\text{accuracy}) \times %s \times \$%d}_{\text{wrong records}}" % (tn(f"{M.REC_HIT:.2f}"), M.REC_COST))}
<p>Floor people are the floor hours a day divided by {M.PROD:.0f} productive hours a person, as in <a href="{W6}.html">Part&nbsp;6</a>. Each floor person needs a scanner and a user licence, plus {M.OFFICE_USERS} office users.</p>
<h2>The break-even volume</h2>
{fig(fig_curve(), 1, "Total warehouse cost an order against volume. Each option is cheapest in its own band of volume, shown by the strip along the bottom.")}
<p>Figure&nbsp;1 is the answer in one picture. Below about <strong>{X_SE} orders a day</strong>, paper and a spreadsheet is the cheapest way to run the example's warehouse: the team is small enough to know where everything is, and any software costs more than it saves. From there to about <strong>{X_EC}</strong>, the ERP's own inventory module with scanners wins: most of the benefit comes from the scan, which kills keying and most errors, and it costs little if the ERP is already paid for. Above about {X_EC} orders a day, a cloud WMS is cheapest, and the gap widens with every order.</p>
<p>The enterprise WMS never wins in the SME range. Its cost an order only falls below the cloud WMS at about {f0(X_CT)} orders a day, eight times the example's volume. Its extra capabilities are real, but an SME pays for them long before it can use them.</p>
<p>Between about 100 and 250 orders a day the ERP module and the cloud WMS are close: at 150 orders a day the gap is {money(abs(rs("erp", 150)["total"] - rs("cloud", 150)["total"]))} a year. In that band, choose on fit, not on price (see the questions below).</p>
{figure_markup()}<h2>The example at {M.TODAY} orders a day</h2>
<table>
<tr><th>Option</th><th class="num">Floor people</th><th class="num">Software and devices a year</th><th class="num">Labour a year</th><th class="num">Errors and wrong records</th><th class="num">Total a year</th><th class="num">Cost an order</th><th class="num">One-time cost</th><th class="num">Payback against paper</th></tr>
{res}
</table>
{fig(fig_stack(), 3, f"Yearly cost of each option at {M.TODAY} orders a day, without the floor labour all four share. The cloud WMS costs more in software and saves it several times over in labour, errors and records.")}
<p><strong>A WMS pays for itself at this volume.</strong> The cloud WMS costs about {money(NOW['cloud']['cost']['software'])} a year in subscriptions and devices, against about {money(NOW['sheet']['cost']['software'])} for paper. It saves {money(NOW['sheet']['total'] - NOW['cloud']['total'])} a year overall, mostly in floor and office labour, with {NOW['sheet']['floor_n'] - NOW['cloud']['floor_n']} fewer floor people and fewer errors and wrong records. The one-time cost of {money(M.one_time('cloud'))} includes implementation, scanners and a six-week dip in floor pace after go-live, and is repaid about {PB['cloud']:.0f} months after signing, counting {M.LIVE['cloud']} months to go live.</p>
<p><strong>The ERP module is the cheaper first step.</strong> It gets most of the way for less: {money(NOW['erp']['total'])} a year, and paid back in about {PB['erp']:.0f} months. For a business below about {X_EC} orders a day, or one still cleaning up its processes, it is a sound start. Its limits show as volume grows: no wave planning, weaker put-away logic and slower records.</p>
<p><strong>The enterprise WMS costs more than paper here.</strong> At {money(NOW['tier1']['total'])} a year it is dearer than running on paper, and its {money(M.one_time('tier1'))} one-time cost takes {PB['tier1'] / 12:.0f} years to repay.</p>
<p><strong>The model is conservative about growth.</strong> A business on paper at {M.TODAY} orders a day needs {NOW['sheet']['floor_n']} floor people; at 900 it needs {rs('sheet', 900)['floor_n']}, against {rs('cloud', 900)['floor_n']} with a WMS. Hiring and training those extra people, and the space they need, are not counted.</p>
<h2>Signs you have outgrown spreadsheets</h2>
<table>
<tr><th>Sign</th><th>Why it matters</th></tr>
<tr><td>Only one or two people know where things are</td><td>The warehouse stops when they are away, and it cannot grow past them</td></tr>
<tr><td>Stock records below about 95% right</td><td>Stockouts, rush orders and customers told "in stock" when it is not (<a href="{W4}.html">Part&nbsp;4</a>)</td></tr>
<tr><td>Errors reaching customers above 0.5% of orders</td><td>At $75 each, it adds up quickly (<a href="{W5}.html">Part&nbsp;5</a>)</td></tr>
<tr><td>Someone spends hours a day keying in paperwork</td><td>Paying twice for every transaction, and a day behind</td></tr>
<tr><td>The warehouse shuts for a yearly count</td><td>Lost shipping days and a record that is wrong again within weeks</td></tr>
<tr><td>Lot, expiry or serial numbers must be tracked</td><td>Recalls and first-expired-first-out are not practical on paper</td></tr>
<tr><td>A second channel or site, or 3PL clients</td><td>Stock must be split, reserved and billed by client and location</td></tr>
<tr><td>Large customers ask for advance ship notices and labels</td><td>EDI and compliant labels need system data at the dock</td></tr>
</table>
<p>Three or more of these together usually mean the warehouse has already paid for a WMS in hidden costs.</p>
<h2>ERP module or WMS: the questions to ask</h2>
<ul>
<li><strong>Does the ERP module direct the work, or only record it?</strong> Directed put-away, batch or wave picking and system-chosen cycle counts are where most of a WMS's labour saving comes from.</li>
<li><strong>Does it handle your units?</strong> Cases, inners and eaches; pallets with mixed items; catch weight.</li>
<li><strong>Lot, expiry and serial numbers?</strong> At receiving, at picking and on the shipping documents.</li>
<li><strong>Shipping integration?</strong> Rates, labels and tracking from the carriers you use, without retyping.</li>
<li><strong>Scanners on the floor?</strong> Real offline-capable handhelds, not a web page on a phone that times out in the back aisles.</li>
<li><strong>What happens at 3 times the volume?</strong> Users, licences, performance and the price at that size.</li>
</ul>
<h2>A roadmap that works for SMEs</h2>
<table>
<tr><th>Step</th><th>What to do</th></tr>
<tr><td>1. Fix the process first</td><td>Space and slotting, pick methods, the dock, counting, errors and labour (Parts&nbsp;1 to 6). A WMS on a messy process automates the mess</td></tr>
<tr><td>2. Clean the data</td><td>Label every location. Clean the item master: dimensions, weights, units, barcodes</td></tr>
<tr><td>3. Write requirements by workflow</td><td>Receiving, put-away, picking, packing, shipping, counting, returns. What must happen, and who does it</td></tr>
<tr><td>4. Scripted demos</td><td>Shortlist three to five systems and make each demonstrate your workflows with your items and orders</td></tr>
<tr><td>5. Check the links</td><td>ERP or accounting, shipping, e-commerce and EDI. Integration is where projects go over budget</td></tr>
<tr><td>6. Go live in a quiet month</td><td>January to March for most distributors. Never in the run-up to the peak (<a href="{W6}.html">Part&nbsp;6</a>)</td></tr>
<tr><td>7. Support and measure</td><td>Vendor on site for the first weeks. Track the same measures before and after</td></tr>
</table>
<h2>Common mistakes</h2>
<ul>
<li><strong>Buying for the business you hope to be in ten years.</strong> An enterprise system for a 300-order warehouse costs more than paper.</li>
<li><strong>Waiting until it hurts.</strong> In the example, staying on paper past {X_EC} orders a day costs more every month.</li>
<li><strong>Skipping the data cleanup.</strong> Wrong dimensions and missing barcodes stop a go-live faster than any software bug.</li>
<li><strong>Customising before using.</strong> Run the standard workflows for three months, then change only what the floor really needs.</li>
<li><strong>Counting only the subscription.</strong> Implementation, scanners, training and the go-live dip often cost more than the first year's fees.</li>
</ul>
<h2>Measures to track before and after</h2>
<table>
<tr><th>Measure</th><th>What it shows</th></tr>
<tr><td>Labour hours an order, by zone</td><td>The floor saving, measured the same way as in Part&nbsp;6</td></tr>
<tr><td>Location accuracy</td><td>Whether the records can be trusted (Part&nbsp;4)</td></tr>
<tr><td>Order accuracy at the customer</td><td>Errors that got through (Part&nbsp;5)</td></tr>
<tr><td>Dock-to-stock time</td><td>How quickly received goods can be sold (Part&nbsp;3)</td></tr>
<tr><td>Office hours on warehouse paperwork</td><td>The keying saving</td></tr>
</table>
{WMS_DEMO}<h2>Key points</h2>
<ul>
<li>A WMS's value is knowing where every item is, and directing the work, not keeping a stock list.</li>
<li>In the example, paper is cheapest below about {X_SE} orders a day, the ERP module with scanners up to about {X_EC}, and a cloud WMS above that.</li>
<li>At {M.TODAY} orders a day, a cloud WMS saves {money(NOW['sheet']['total'] - NOW['cloud']['total'])} a year against paper, and pays back about {PB['cloud']:.0f} months after signing.</li>
<li>An enterprise WMS does not pay at SME volumes. In the example it costs more than paper.</li>
<li>Fix the process and the data first, choose on your own workflows, and go live in a quiet month.</li>
</ul>
<p>Earlier in this series: <a href="{W1}.html">Part&nbsp;1</a> space, <a href="{W2}.html">Part&nbsp;2</a> picking, <a href="{W3}.html">Part&nbsp;3</a> the dock, <a href="{W4}.html">Part&nbsp;4</a> stock records, <a href="{W5}.html">Part&nbsp;5</a> errors and <a href="{W6}.html">Part&nbsp;6</a> labour. Next: <a href="automation-roi-for-sme-warehouses-robots-pick-to-light-and-vertical-lifts.html">Part&nbsp;8</a> asks when automation pays.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://www.descartes.com/resources/knowledge-center/how-much-does-wms-software-cost" rel="noopener" target="_blank">Descartes: How much does WMS software cost?</a></li>
<li><a href="https://www.fynd.com/blog/warehouse-management-system-cost-wms-pricing-hidden-costs-and-roi-fynd" rel="noopener" target="_blank">Fynd: Warehouse management system cost, pricing, hidden costs and ROI</a></li>
<li><a href="https://incora.software/insights/warehouse-management-system-cost" rel="noopener" target="_blank">Incora: How much does warehouse management software cost in 2026?</a></li>
<li><a href="https://cpcongroup.com/insights/article/warehouse-management-system-cost-guide/" rel="noopener" target="_blank">CPCON Group: Warehouse management system cost guide</a></li>
<li><a href="https://nucleusresearch.com/?p=37829" rel="noopener" target="_blank">Nucleus Research: WMS improves inventory accuracy by 20 percent</a></li>
</ul>
{NOTE}{js3d("wh3d7")}{mathjs()}"""
    body = nowrap(body, [(1, 0, 22), (2, 0, 22), (3, 0, 22)])
    return dict(slug=W7, title="Do We Need a WMS Yet? When Spreadsheets Stop Scaling",
                desc="Paper, the ERP module, a cloud WMS or an enterprise system: the volume at which each pays, what they cost, and how SMEs should choose and go live.",
                cats=["operational-efficiency", "digital-technology"], tags=["warehouse management system", "WMS", "WMS cost", "barcode scanning", "ERP", "inventory accuracy"],
                body=body, date=DATE, author="Quak Foo Lee", read="11 min read", series=SER(7), cover_label="Warehouse operations",
                related=[W6, W4, W5])


if __name__ == "__main__":
    a = part7()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])}\n")
