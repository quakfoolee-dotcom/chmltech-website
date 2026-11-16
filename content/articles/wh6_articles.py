"""Warehouse operations series for Insights (V5.36). Part 6: labour planning for the peak season.

Same distributor as Parts 1 to 5. The numbers come from wh6_model.py, which also feeds the 3D labour heat map in
Figure 2 (assets/js/wh3d6.js).

Usage:  python3 content/articles/wh6_articles.py
        python3 content/gen/add_article.py peak-season-without-the-panic-warehouse-labour-planning
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import js3d, nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, PURPLE, MUTED, eq, tn, mathjs
import wh_model as W
import wh6_model as L
from wh_articles import W1, W2, SER
from wh3_articles import W3
from wh4_articles import W4
from wh5_articles import W5

DATE = "2026-11-16"
W6 = "peak-season-without-the-panic-warehouse-labour-planning"
NOTE = ('<p class="oee-note"><em>The distributor, its demand pattern, labour standards and rates are an illustrative example built from stated '
        'assumptions. Overtime rules are British Columbia\'s standard rules; averaging agreements and other provinces differ. This is not legal advice.</em></p>')
f0 = lambda x: f"{x:,.0f}"
f1 = lambda x: f"{x:,.1f}"
pc = lambda x: f"{x * 100:.0f}%"
money = lambda x: f"${round(x, -2 if abs(x) < 10000 else -3):,.0f}"
R = {p: L.plan(p) for p in L.PLANS}
OT, PK, TP, FX = R["ot"], R["peak"], R["temps"], R["flex"]
ORD_YEAR = sum(L.ORDERS) * L.DAYS_WEEK
COL = {"ot": RED, "peak": PURPLE, "temps": ORANGE, "flex": GREEND}
KEYW = [("January", 3), ("Spring build", 16), ("Typical week", 30), ("Holiday peak", 47)]


def cap_orders(n): return n * L.HOURS * L.PROD / L.H_PER_ORDER


def fig_year():
    x0, y0, w, h = 64, 30, 590, 230; ymax = 550; s = ""
    X = lambda wk: x0 + (wk - 0.5) / L.WEEKS * w; Y = lambda v: y0 + h - v / ymax * h
    for v in range(0, ymax + 1, 100): s += f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x0 + w}" y2="{Y(v):.1f}" stroke="#E4E1D8"/>' + txt(x0 - 8, Y(v) + 4, str(v), "end", MUTED, 12)
    for wk, lab in ((1, "Jan"), (14, "Apr"), (27, "Jul"), (40, "Oct"), (52, "Dec")): s += txt(X(wk), y0 + h + 18, lab, "middle", MUTED, 12)
    bw = w / L.WEEKS - 1.5; c7 = cap_orders(L.CORE)
    for i, o in enumerate(L.ORDERS):
        s += f'<rect x="{X(i + 1) - bw / 2:.1f}" y="{Y(o):.1f}" width="{bw:.1f}" height="{(o / ymax) * h:.1f}" fill="{RED if o > c7 else BLUE}" opacity=".8"/>'
    for n, lab, col in ((L.CORE, f"Lean crew of {L.CORE}", NAVY), (L.PEAK_CREW, f"Peak crew of {L.PEAK_CREW}", PURPLE)):
        y = Y(cap_orders(n)); s += f'<line x1="{x0}" y1="{y:.1f}" x2="{x0 + w}" y2="{y:.1f}" stroke="{col}" stroke-width="2" stroke-dasharray="6 4"/>'
        s += txt(x0 + 8, y - 6, f"{lab}: about {f0(cap_orders(n))} orders a day", fill=col, fs=12, bold=True)
    s += f'<text x="16" y="{y0 + h / 2}" transform="rotate(-90 16 {y0 + h / 2})" text-anchor="middle" font-size="12.5" font-weight="600" fill="{NAVY}">Orders a day</text>'
    s += f'<rect x="{x0 + w - 230}" y="{y0 + 4}" width="12" height="12" fill="{RED}" opacity=".8"/>' + txt(x0 + w - 212, y0 + 14, "Weeks above the lean crew's capacity", fill=NAVY, fs=12)
    n_over = sum(1 for o in L.ORDERS if o > c7)
    return svg(f"Bar chart of orders a day for each week of the year, from about {f0(min(L.ORDERS))} in January to about {f0(max(L.ORDERS))} at the holiday peak. "
               f"A dashed line marks the capacity of the lean crew of {L.CORE}, about {f0(c7)} orders a day, which {n_over} weeks exceed. A second line marks the peak crew of {L.PEAK_CREW}.", 700, 300, s, 560)


def fig_cost():
    x0, w = 210, 390; mx = max(r["cost"]["total"] for r in R.values()); sc = w / mx; out = ""
    parts = [("core", "Core crew", BLUE), ("ot", "Overtime", ORANGE), ("temps", "Temps and training", "#E3C58E"), ("late", "Late orders", RED)]
    lx = 20
    for _, lab, c in parts: out += f'<rect x="{lx}" y="10" width="12" height="12" rx="2" fill="{c}"/>' + txt(lx + 18, 21, lab, fill=NAVY, fs=12); lx += 34 + len(lab) * 6.6
    best = min(L.PLANS, key=lambda p: R[p]["cost"]["total"])
    for i, p in enumerate(L.PLANS):
        y = 40 + i * 50; x = x0; r = R[p]
        out += txt(x0 - 10, y + 19, L.PNAME[p], "end", NAVY, 13, p == best)
        for key, _, c in parts:
            ww = r["cost"][key] * sc; out += f'<rect x="{x:.1f}" y="{y}" width="{ww:.1f}" height="28" fill="{c}"/>'; x += ww
        out += txt(x + 8, y + 19, money(r["cost"]["total"]), fill=NAVY, fs=13, bold=True)
        note = f"{f0(r['tot']['late'])} late orders · {r['tot']['burn']} weeks of heavy overtime" if r["tot"]["late"] > 1 else f"{pc(r['tot']['idle_share'])} of paid time idle"
        out += txt(x0, y + 42, note, fill=MUTED, fs=11.5)
    return svg(f"Stacked bars of the yearly labour cost of each plan. Lean crew with overtime: {money(OT['cost']['total'])}, with {f0(OT['tot']['late'])} late orders. "
               f"Crew sized for the peak: {money(PK['cost']['total'])}. Core crew with planned temps: {money(TP['cost']['total'])}. Temps with a cross-trained crew: "
               f"{money(FX['cost']['total'])}, the lowest.", 720, 250, out, 560)


def heads(r, w):
    """People in each zone in each hour of week w: core and temps; in the flexible plan the movable share of the core
    follows the work hour by hour."""
    wk = r["weeks"][w]; out = []
    for h in range(L.HOURS):
        row = {}
        if r["flex"]:
            mov = {z: round(r["core"][z] * L.FLEX_SHARE) for z in L.ZONES}; fixed = {z: r["core"][z] - mov[z] for z in L.ZONES}
            pool = sum(mov.values())
            need = {z: max(0.0, wk["load"][z][h] - (fixed[z] + wk["temps"][z]) * L.PROD) + 1e-6 for z in L.ZONES}
            alloc = L.split(pool, need) if pool >= len(L.ZONES) else L._place(pool, need)
            for z in L.ZONES: row[z] = [fixed[z] + alloc[z], wk["temps"][z]]
        else:
            for z in L.ZONES: row[z] = [r["core"][z], wk["temps"][z]]
        out.append(row)
    return out


def figure_data():
    data = dict(zones=L.ZONES, names=[L.ZNAME[z] for z in L.ZONES], plans=L.PLANS, pnames=[L.PNAME[p] for p in L.PLANS], keyw=KEYW,
                need=[round(wk["need_day"] / (L.HOURS * L.PROD), 2) for wk in OT["weeks"]], orders=[round(o) for o in L.ORDERS], P={})
    for p in L.PLANS:
        r = R[p]; wl = []
        for w, wk in enumerate(r["weeks"]):
            hd = heads(r, w)
            u = [[round(wk["load"][z][h] / max(0.01, wk["cap"][z][h]), 3) for h in range(L.HOURS)] for z in L.ZONES]
            wl.append([[[hd[h][z][0] for h in range(L.HOURS)] for z in L.ZONES], [[hd[h][z][1] for h in range(L.HOURS)] for z in L.ZONES], u,
                       round(wk["ot_pp"], 1), round(wk["late"]), round(wk["cap_day"] / (L.HOURS * L.PROD), 2)])
        data["P"][p] = dict(w=wl, s=[round(r["cost"]["total"], -3), round(r["per_order"], 2), round(r["tot"]["late"]), r["tot"]["burn"], round(r["tot"]["idle_share"], 3)])
    data["bld"] = [W.BLD_X, W.BLD_Z, W.CLEAR_H]; data["rows"] = W.ROW_Z; data["bays"] = W.BAYS; data["bayW"] = W.BAY_W; data["rowD"] = W.ROW_D
    data["x0"] = W.RACK_X0; data["levels"] = W.LEVELS_NEW; data["beam"] = W.BEAM; data["aisles"] = W.AISLE_Z
    return data


def figure_markup():
    js = json.dumps(figure_data(), separators=(",", ":"))
    pb = "".join(f'<button type="button" class="wh3d-btn" data-p="{p}" aria-pressed="{"true" if p == "ot" else "false"}">{L.PNAME[p]}</button>' for p in L.PLANS)
    kb = "".join(f'<button type="button" class="wh3d-btn wh3d-small" data-w="{w - 1}">{n}</button>' for n, w in KEYW)
    return f"""<p>Figure 2 is a labour heat map of the example's warehouse. Each zone's floor is coloured by how loaded its people are in that hour: blue is idle, green busy, amber stretched and red more work than people. The figures are the people in each zone, blue for the core crew and orange for temps. The day runs from 06:00 to 14:30 on a loop, and the figure tours four typical weeks of the year on its own. Choose a plan, or Compare all to see the four side by side, and pick any week from the year chart.</p>
<figure class="wh3d wh3d6" id="wh3d6">
<div class="wh3d-box">
<div class="wh3d-stage">
<canvas role="img" aria-label="3D labour heat map of the example distributor's warehouse: five zones (receiving, put-away, picking, packing and shipping) drawn as coloured floor areas, each with figures for its core crew and temps. The colours show how loaded the people in each zone are, hour by hour, through a working day. In the compare view the four staffing plans are shown side by side."></canvas>
<span class="wh3d-drag" aria-hidden="true">Drag to turn</span>
<span class="wh3d-chip" id="wh3d6-chip">Week 3 · 06:00</span>
<p class="wh3d-nogl" id="wh3d6-nogl" hidden>This browser cannot show the 3D model. The controls below still update the numbers.</p>
</div>
<div class="wh3d-panel">
<div class="wh3d6-row" role="group" aria-label="Staffing plan">{pb}<button type="button" class="wh3d-btn" data-p="all" aria-pressed="false">Compare all</button></div>
<div class="wh3d6-weeks" role="group" aria-label="Week"><span>Week</span>{kb}</div>
<div class="wh3d5-tour" id="wh3d6-tour" aria-hidden="true"><b><i></i></b><span></span></div>
<div class="wh3d-cells">
<div class="wh3d-cell wh3d-key"><span class="k">Orders a day this week</span><strong id="wh3d6-ord"></strong></div>
<div class="wh3d-cell wh3d-key"><span class="k">People on the floor</span><strong id="wh3d6-ppl"></strong></div>
<div class="wh3d-cell"><span class="k">Overtime a person this week</span><strong id="wh3d6-ot"></strong></div>
<div class="wh3d-cell"><span class="k">Late orders this week</span><strong id="wh3d6-late"></strong></div>
<div class="wh3d-cell"><span class="k">Labour cost a year</span><strong id="wh3d6-cost"></strong></div>
<div class="wh3d-cell"><span class="k">Labour cost an order</span><strong id="wh3d6-cpo"></strong></div>
</div>
<div class="wh3d6-year" aria-label="Year chart: people-days of work needed each week against the plan's people. Click a week to show it."><svg id="wh3d6-ysvg" viewBox="0 0 600 90" preserveAspectRatio="none"></svg><p><span>People needed each week (bars) and the plan's people (line). Click a week.</span><span id="wh3d6-wk"></span></p></div>
<p class="wh3d-say" id="wh3d6-say" aria-live="polite"></p>
<div class="wh3d-last"><ul class="wh3d-legend"><li><i style="background:#3FA7F5"></i>Idle (under 60%)</li><li><i style="background:#6ECD69"></i>Busy</li><li><i style="background:#F5A032"></i>Stretched</li><li><i style="background:#FF5A4A"></i>More work than people</li><li><i style="background:#2f6db5;border-radius:50%"></i>Core crew</li><li><i style="background:#FF8A3D;border-radius:50%"></i>Temp</li></ul></div>
</div>
</div>
<figcaption>Figure 2. Labour heat map of the example's five zones through a working day, for any week of the year and any of the four plans. Load is the work arriving in each zone and hour from that week's orders; the colours compare it with the productive hours of the people there. Temps work at 60% in their first week and 85% in their second. The yearly numbers in the panel come from the same model as the tables.</figcaption>
<script type="application/json" id="wh3d6-data">{js}</script>
</figure>
"""


def part6():
    std = "".join(f'<tr><td>{L.ZNAME[z]}</td><td>{src}</td><td class="num">{L.H_ORDER[z] * 60:.1f} min</td></tr>' for z, src in
                  (("receive", f'Unload and scan 0.61 pallets an order (<a href="{W3}.html">Part&nbsp;3</a>)'), ("putaway", "Put away three pallets in four, cross-dock the rest (Part&nbsp;3)"),
                   ("pick", f'Batch picking in the re-slotted racks (<a href="{W2}.html">Part&nbsp;2</a>)'), ("pack", f'Scan every case and pack (<a href="{W5}.html">Part&nbsp;5</a>)'),
                   ("ship", "Stage, load and paperwork")))
    rows = "".join(f'<tr><td>{L.PNAME[p]}</td><td class="num">{R[p]["core_n"]}</td><td class="num">{R[p]["tot"]["temps_hired"]}</td><td class="num">{f0(R[p]["tot"]["ot_h"])}</td>'
                   f'<td class="num">{f0(R[p]["tot"]["late"])}</td><td class="num">{R[p]["tot"]["burn"]}</td><td class="num">{pc(R[p]["tot"]["idle_share"])}</td>'
                   f'<td class="num">{money(R[p]["cost"]["total"])}</td><td class="num">${R[p]["per_order"]:.2f}</td></tr>' for p in L.PLANS)
    pk_w = max(range(L.WEEKS), key=lambda w: L.ORDERS[w])
    body = f"""{CSS}
<p>Every year it is the same. Orders start climbing in October, the crew starts staying late, and by the third week of November people are working ten-hour days and Saturdays. Someone calls the temp agency, and the temps arrive in the busiest week, when nobody has time to train them. Errors go up, a good picker quits in December, and in January the warehouse is half idle.</p>
<p>Peak season does not have to go like that. It is the most predictable problem a warehouse has. This part uses the example distributor's year to compare four ways of staffing it, with the work each order brings taken from the earlier parts of the series.</p>
<h2>Step 1: turn the forecast into hours</h2>
<p>Labour planning starts with two numbers: how many orders are coming, and how many hours each order takes. The first comes from last year's sales by week, adjusted with what the sales team knows about this year. The second is a labour standard for each zone, measured on the floor. For the example, with the fixes from Parts&nbsp;1 to 5 in place:</p>
<table>
<tr><th>Zone</th><th>Work</th><th class="num">Time an order</th></tr>
{std}
<tr class="oee-total"><td>Total</td><td></td><td class="num">{L.H_PER_ORDER * 60:.1f} min</td></tr>
</table>
{eq(r"\text{People needed} = \dfrac{\text{orders a day} \times \text{hours an order}}{\text{productive hours a person a day}} = \dfrac{%d \times %s}{%s} \approx %s" % (L.AVG_ORDERS, tn(f"{L.H_PER_ORDER:.3f}"), tn(f"{L.HOURS * L.PROD:.0f}"), tn(f1(L.AVG_DAY / (L.HOURS * L.PROD)))))}
<p>A day of {L.HOURS} paid hours gives about {L.HOURS * L.PROD:.0f} productive hours after breaks, meetings and set-up. So an average day of {L.AVG_ORDERS} orders needs about {f1(L.AVG_DAY / (L.HOURS * L.PROD))} people, a crew of {L.CORE}. At the holiday peak of about {f0(max(L.ORDERS))} orders a day it needs about {f1(L.PEAK_DAY / (L.HOURS * L.PROD))}, a crew of {L.PEAK_CREW}.</p>
{fig(fig_year(), 1, "Orders a day through the example's year. The lean crew covers most weeks. The spring build and the holiday peak go over.")}
<h2>Step 2: look inside the day</h2>
<p>A daily total hides a second problem. Each zone has its own rhythm: receiving is busiest first thing, when the trucks arrive; packing builds through the late morning; and shipping is concentrated in the last two hours before the carriers come. A crew that is big enough for the day can still be short in shipping at 13:00 while receiving stands idle. This is why cross-training matters as much as headcount, and it is what Figure&nbsp;2 shows hour by hour.</p>
<h2>Four ways to staff the year</h2>
<p><strong>Plan 1: lean crew plus overtime.</strong> Keep a crew of {L.CORE}, sized for the average day, and cover peaks with overtime. In BC, most employees earn time and a half after 8 hours in a day or 40 in a week, and double time after 12 hours in a day. The example allows up to two hours of overtime a person a day. When even that is not enough, orders ship a day late.</p>
<p><strong>Plan 2: crew sized for the peak.</strong> Hire {L.PEAK_CREW} people and keep them all year. Nothing ships late, but for most of the year a large share of paid time is idle.</p>
<p><strong>Plan 3: core crew plus planned temps.</strong> Keep the crew of {L.CORE}, and book agency temps from the forecast, starting each one {L.LEAD} weeks before the week they are needed so they are trained before the rush. Temps are assumed to work at {pc(L.RAMP[0])} of full pace in their first week and {pc(L.RAMP[1])} in their second, and each one costs {f0(L.TRAIN_H)} paid hours of training and {f0(L.SUP_H)} hours of a supervisor's time.</p>
<p><strong>Plan 4: temps plus a cross-trained crew.</strong> As Plan&nbsp;3, but {pc(L.FLEX_SHARE)} of the core crew is trained in more than one zone and moves each hour to where the work is. The crew covers the zones' different rhythms itself, so fewer temps are needed and fewer hours go to overtime.</p>
{figure_markup()}<h2>The result</h2>
<table>
<tr><th>Plan</th><th class="num">Core crew</th><th class="num">Temps hired</th><th class="num">Overtime hours</th><th class="num">Late orders</th><th class="num">Heavy overtime weeks</th><th class="num">Idle time</th><th class="num">Cost a year</th><th class="num">Cost an order</th></tr>
{rows}
</table>
{fig(fig_cost(), 3, "Yearly labour cost of each plan. Overtime looks cheap until the late orders and the burnout are counted.")}
<p><strong>Overtime alone looks cheaper than it is.</strong> At {money(OT["cost"]["total"])} a year, Plan&nbsp;1 costs less on paper than planned temps. But {f0(OT["tot"]["late"])} orders ship late, and for {OT["tot"]["burn"]} weeks of the year the crew averages more than eight hours of overtime a person a week, up to {f1(OT["tot"]["max_ot_pp"])} hours. Research on long hours, best known from Pencavel's study of munitions workers, found output per hour falls once people work beyond about 50 hours a week, and that very long weeks add little. Long peaks also bring errors (Part&nbsp;5) and resignations, which this table does not count.</p>
<p><strong>Staffing for the peak is safe and expensive.</strong> Plan&nbsp;2 never ships late, but it costs {money(PK["cost"]["total"] - OT["cost"]["total"])} a year more than Plan&nbsp;1, and {pc(PK["tot"]["idle_share"])} of paid productive time has no work.</p>
<p><strong>Planned temps buy reliability.</strong> Plan&nbsp;3 ships everything on time with no heavy overtime weeks, for {money(TP["cost"]["total"])} a year. Without cross-training, though, temps are booked zone by zone and still leave gaps at each zone's busiest hour, which overtime fills.</p>
<p><strong>Cross-training is the cheapest capacity there is.</strong> Plan&nbsp;4 needs fewer temp weeks and less overtime, and its idle time falls to {pc(FX["tot"]["idle_share"])}. At {money(FX["cost"]["total"])} a year, or ${FX["per_order"]:.2f} an order, it is the lowest-cost plan and the most reliable.</p>
<h2>A peak-readiness calendar</h2>
<table>
<tr><th>When</th><th>Action</th></tr>
<tr><td>12 weeks out</td><td>Weekly forecast agreed with sales. Labour standards checked on the floor. Temp needs by week and zone</td></tr>
<tr><td>10 weeks out</td><td>Agency booked with dates and numbers. Cross-training plan for the core crew. Holiday and leave requests settled</td></tr>
<tr><td>6 weeks out</td><td>Re-slot fast movers for peak items (Part&nbsp;1). Clear dead stock. Check scanners and spare batteries</td></tr>
<tr><td>2 to 4 weeks out</td><td>Temps start, are trained and work alongside the core crew. Short written work instructions at each station</td></tr>
<tr><td>Peak weeks</td><td>Daily stand-up on yesterday's numbers. Overtime capped and shared. Carrier pickups confirmed</td></tr>
<tr><td>After the peak</td><td>Temps released in order of need. Review what the forecast missed. Thank the crew</td></tr>
</table>
<h2>A simple skills matrix</h2>
<p>Cross-training works when it is planned and visible. A skills matrix on the wall shows who can work where, and who is learning what:</p>
<table>
<tr><th>Person</th><th>Receiving</th><th>Put-away</th><th>Picking</th><th>Packing</th><th>Shipping</th></tr>
<tr><td>Crew member A</td><td>Trainer</td><td>Trained</td><td>Trained</td><td>Learning</td><td></td></tr>
<tr><td>Crew member B</td><td></td><td>Trainer</td><td>Trained</td><td>Trained</td><td>Trained</td></tr>
<tr><td>Crew member C</td><td>Trained</td><td></td><td>Trainer</td><td>Trained</td><td>Learning</td></tr>
</table>
<p>Aim for every zone to have at least three trained people, and every person to be trained in at least two zones. Forklift work also needs certified operators, so plan that training early.</p>
<h2>Measures to track</h2>
<table>
<tr><th>Measure</th><th>What it shows</th></tr>
<tr><td>Labour hours an order, by zone</td><td>The labour standard. It drives every staffing number</td></tr>
<tr><td>Forecast against actual orders, by week</td><td>Whether the plan can be trusted, and how much buffer it needs</td></tr>
<tr><td>Overtime hours a person a week</td><td>Fatigue and cost. Set a ceiling and keep to it</td></tr>
<tr><td>Orders shipped on time in peak weeks</td><td>Whether the plan worked</td></tr>
<tr><td>Temp productivity by week of service</td><td>Whether the training and the start dates were right</td></tr>
</table>
<h2>Common mistakes</h2>
<ul>
<li><strong>Booking temps in the peak week.</strong> They arrive when nobody can train them, and work at half pace when you need them most.</li>
<li><strong>Planning by headcount, not hours.</strong> Ten people at seven productive hours is not the same as ten people at eight.</li>
<li><strong>Ignoring the hours inside the day.</strong> The shortage is usually in one zone at one time, not in the day's total.</li>
<li><strong>Running the crew on overtime for weeks.</strong> Output per hour falls, errors rise and people leave.</li>
<li><strong>Skipping the post-peak review.</strong> Next year's plan starts with what this year's forecast missed.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>Peak season is predictable. Turn the weekly forecast into hours with a labour standard for each zone.</li>
<li>Look inside the day. Each zone peaks at a different hour, so a crew that is big enough can still be short in one place.</li>
<li>Overtime alone is cheap on paper and expensive in late orders, errors and burnout. In the example, {f0(OT["tot"]["late"])} orders ship late.</li>
<li>Book temps from the forecast and start them two weeks early, so they are trained before the rush.</li>
<li>Cross-train the core crew. In the example it is the lowest-cost and most reliable plan, at {money(FX["cost"]["total"])} a year.</li>
</ul>
<p>Earlier in this series: <a href="{W1}.html">Part&nbsp;1</a> space, <a href="{W2}.html">Part&nbsp;2</a> picking, <a href="{W3}.html">Part&nbsp;3</a> the dock, <a href="{W4}.html">Part&nbsp;4</a> stock records and <a href="{W5}.html">Part&nbsp;5</a> errors. Next: <a href="do-we-need-a-wms-yet-when-spreadsheets-stop-scaling.html">Part&nbsp;7</a> asks when an SME needs a warehouse management system.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://www2.gov.bc.ca/gov/content/employment-business/employment-standards-advice/employment-standards/forms-resources/igm/esa-part-4-section-40" rel="noopener" target="_blank">Government of BC: Overtime wages, Employment Standards Act Part 4, Section 40</a></li>
<li><a href="https://ftp.iza.org/dp8129.pdf" rel="noopener" target="_blank">Pencavel (2014), The Productivity of Working Hours, IZA Discussion Paper 8129</a></li>
</ul>
{NOTE}{js3d("wh3d6")}{mathjs()}"""
    body = nowrap(body, [(1, 0, 14), (2, 0, 30), (3, 0, 16)])
    return dict(slug=W6, title="Peak Season Without the Panic: Warehouse Labour Planning",
                desc="Turn the forecast into hours, look inside the day, and compare overtime, a peak-sized crew, planned temps and cross-training in one warehouse.",
                cats=["operational-efficiency"], tags=["labour planning", "peak season", "warehouse staffing", "temporary workers", "cross-training", "overtime"],
                body=body, date=DATE, author="Quak Foo Lee", read="11 min read", series=SER(6), cover_label="Warehouse operations",
                related=[W5, W2, W3])


if __name__ == "__main__":
    a = part6()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])}\n")
