"""Warehouse operations series for Insights (V5.34). Part 4: phantom stock, inventory accuracy and cycle counting.

Same distributor as Parts 1 to 3. The numbers come from wh4_model.py (a simulated year, averaged over 20 years),
which also feeds the 3D figure (assets/js/wh3d4.js).

Usage:  python3 content/articles/wh4_articles.py
        python3 content/gen/add_article.py phantom-stock-inventory-accuracy-and-cycle-counting
        python3 content/gen/series_labels.py
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import js3d, nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, MUTED, eq, im, tn, mathjs
import wh_model as W
import wh4_model as Q
from wh_articles import W1, W2, SER, ABC1, SS1
from wh3_articles import W3

DATE = "2026-11-15"
W4 = "phantom-stock-inventory-accuracy-and-cycle-counting"
NOTE = ('<p class="oee-note"><em>The distributor, its error rates and its times are an illustrative example built from stated assumptions. '
        'Measure your own record accuracy with a sample count before choosing a counting plan.</em></p>')
f0 = lambda x: f"{x:,.0f}"
f1 = lambda x: f"{x:,.1f}"
pc = lambda x: f"{x * 100:.0f}%"
pc1 = lambda x: f"{x * 100:.1f}%"
A = {s: Q.averaged(s) for s in Q.STRATS}
AN, CY, FX = A["annual"], A["cycle"], A["fixed"]
CC = Q.class_counts()
FREQ = {c: 52 // Q.PERIOD[c] for c in "ABC"}
COUNTS = sum(CC[c] * FREQ[c] for c in "ABC")
DAYS = 250
COL = {"annual": RED, "cycle": BLUE, "fixed": GREEND}


def fig_accuracy():
    x0, y0, w, h = 64, 30, 590, 230; s = ""; ylo = 0.6
    X = lambda wk: x0 + wk / Q.WEEKS * w; Y = lambda a: y0 + h - (a - ylo) / (1 - ylo) * h
    for a in (0.6, 0.7, 0.8, 0.9, 1.0):
        s += f'<line x1="{x0}" y1="{Y(a):.1f}" x2="{x0 + w}" y2="{Y(a):.1f}" stroke="#E4E1D8"/>' + txt(x0 - 8, Y(a) + 4, f"{a * 100:.0f}%", "end", MUTED, 12)
    for wk in range(0, 53, 13): s += txt(X(wk), y0 + h + 18, f"Week {wk}", "middle", MUTED, 12)
    s += f'<line x1="{x0}" y1="{Y(0.995):.1f}" x2="{x0 + w}" y2="{Y(0.995):.1f}" stroke="{NAVY}" stroke-dasharray="5 4" opacity=".7"/>' + txt(x0 + w - 4, Y(0.995) - 6, "Best in class: 99.5%", "end", NAVY, 12, True)
    for k, sname in enumerate(Q.STRATS):
        pts = " ".join(f"{X(i):.1f},{Y(a):.1f}" for i, a in enumerate(A[sname]["curve"]))
        s += f'<polyline points="{pts}" fill="none" stroke="{COL[sname]}" stroke-width="2.8"/>'
        s += f'<rect x="{x0 + 14}" y="{y0 + h - 64 + k * 18}" width="12" height="12" rx="2" fill="{COL[sname]}"/>' + txt(x0 + 32, y0 + h - 54 + k * 18, Q.NAMES[sname], fill=NAVY, fs=12.5, bold=True)
    s += f'<text x="16" y="{y0 + h / 2}" transform="rotate(-90 16 {y0 + h / 2})" text-anchor="middle" font-size="12.5" font-weight="600" fill="{NAVY}">Location records right</text>'
    return svg(f"Line chart of the share of location records that are right, week by week through a year. With an annual count only, accuracy falls from "
               f"{pc(AN['curve'][0])} to about {pc(AN['low'])} before the year-end count lifts it back. ABC cycle counting holds it near {pc(CY['avg'])}, "
               f"and cycle counting with the causes fixed near {pc(FX['avg'])}. The best-in-class benchmark is 99.5 percent.", 700, 300, s, 560)


def figure_data():
    pos = W.positions(W.LEVELS_NEW)
    locs = []
    for i, (c, ix, h) in enumerate(Q.LOCS): locs.append([c, ix, round(h, 2)])
    st = {}
    for sname in Q.STRATS:
        r = Q.run(sname, events=True)
        st[sname] = dict(ev=[[[w, s] for w, s in e] for e in r["ev"]], acc=[round(a, 4) for a in r["acc"]],
                         s=[round(A[sname]["avg"], 4), round(A[sname]["short"]), round(A[sname]["hours"]), round(A[sname]["total_h"]), A[sname]["closed"] and 2 or 0])
    return dict(bld=[W.BLD_X, W.BLD_Z, W.CLEAR_H], rows=W.ROW_Z, bays=W.BAYS, bayW=W.BAY_W, rowD=W.ROW_D, x0=W.RACK_X0, perBay=W.PER_BAY,
                beam=W.BEAM, levels=W.LEVELS_NEW, weeks=Q.WEEKS, period=Q.PERIOD, periodF=Q.PERIOD_F, locs=locs, st=st,
                curves={s: [round(a, 4) for a in A[s]["curve"]] for s in Q.STRATS})


def figure_markup():
    data = json.dumps(figure_data(), separators=(",", ":"))
    btn = lambda s, on: f'<button type="button" class="wh3d-btn" data-s="{s}" aria-pressed="{on}">{Q.NAMES[s] if s != "all" else "Compare all"}</button>'
    return f"""<p>Figure 2 runs a year of stock records in the example's pallet racks, one week at a time. Each pallet is coloured by what its record says: grey when the record is right, amber when the quantity is wrong, and red for phantom stock, drawn as a see-through ghost because the system shows a pallet that is not really there. Rings mark the locations counted that week. Choose a counting plan, or Compare all to see the three side by side, with the panel showing each plan's numbers in the same order.</p>
<figure class="wh3d wh3d4" id="wh3d4">
<div class="wh3d-box">
<div class="wh3d-stage">
<canvas role="img" aria-label="3D model of the example distributor's pallet racks over one year. Pallets whose records are right are grey, pallets with a wrong quantity are amber, and phantom stock is drawn as a red see-through ghost. Rings show the locations counted each week. In the compare view the three counting plans are shown side by side."></canvas>
<span class="wh3d-drag" aria-hidden="true">Drag to turn</span>
<span class="wh3d-chip" id="wh3d4-chip">Week 0</span>
<span class="wh3d-tag wh3d4-tag" id="wh3d4-tag"></span>
<p class="wh3d-nogl" id="wh3d4-nogl" hidden>This browser cannot show the 3D model. The buttons below still update the numbers.</p>
</div>
<div class="wh3d-panel">
<div class="wh3d4-row" role="group" aria-label="Counting plan">{btn("annual", "true")}{btn("cycle", "false")}{btn("fixed", "false")}{btn("all", "false")}</div>
<div class="wh3d-cells">
<div class="wh3d-cell wh3d-key"><span class="k">Records right this week</span><strong id="wh3d4-now"></strong></div>
<div class="wh3d-cell wh3d-key"><span class="k">Average over the year</span><strong id="wh3d4-avg"></strong></div>
<div class="wh3d-cell"><span class="k">Short picks a year</span><strong id="wh3d4-short"></strong></div>
<div class="wh3d-cell"><span class="k">Counting hours a year</span><strong id="wh3d4-hours"></strong></div>
<div class="wh3d-cell"><span class="k">Counting and searching hours</span><strong id="wh3d4-total"></strong></div>
<div class="wh3d-cell"><span class="k">Days closed to count</span><strong id="wh3d4-closed"></strong></div>
</div>
<div class="wh3d3-chart wh3d4-chart" aria-hidden="true"><svg viewBox="0 0 600 110" preserveAspectRatio="none"><g id="wh3d4-lines"></g><line id="wh3d4-cur" stroke="#FFE27A" stroke-width="1.5" vector-effect="non-scaling-stroke"/></svg><p><span>Records right, week 0 to 52 (60% to 100%)</span><span>Bright line: the plan shown</span></p></div>
<p class="wh3d-say" id="wh3d4-say" aria-live="polite"></p>
<div class="wh3d-last"><ul class="wh3d-legend"><li><i style="background:#5E6A7C"></i>Record right</li><li><i style="background:#F5A032"></i>Wrong quantity</li><li><i style="background:#FF5A4A"></i>Phantom stock</li><li><i style="background:#FFE27A;border-radius:50%"></i>Counted this week</li></ul></div>
</div>
</div>
<figcaption>Figure 2. A simulated year of location records in the example's racks, {f0(Q.N)} occupied locations. The replay shows one year. The numbers in the panel are averages over 20 simulated years. A short pick is a picker finding less stock than the system shows.</figcaption>
<script type="application/json" id="wh3d4-data">{data}</script>
</figure>
"""


def part4():
    rows = "".join(f'<tr><td>{Q.NAMES[s]}</td><td class="num">{pc1(A[s]["avg"])}</td><td class="num">{pc(A[s]["low"])}</td><td class="num">{f0(A[s]["short"])}</td>'
                   f'<td class="num">{f0(A[s]["hours"])}&nbsp;h</td><td class="num">{f0(A[s]["total_h"])}&nbsp;h</td><td class="num">{A[s]["closed"] and 2 or 0}</td></tr>' for s in Q.STRATS)
    body = f"""{CSS}
<p>A customer calls for 40 cases. The system shows 40 in location R3-B12, so sales confirm the order. The picker finds 12. Somewhere there are 28 more cases, or there are not, and nobody can say which until someone searches. The order ships short, the buyer places a rush order for stock that may already be in the building, and the next week the same thing happens with another item.</p>
<p>This is phantom stock: the system says it is there and the shelf says it is not. It undermines everything that relies on the records: sales promises, purchasing, safety stock, and the slotting and put-away of Parts&nbsp;1 to 3. This part measures how fast records go wrong in the example warehouse and compares the classic once-a-year count with cycle counting.</p>
<h2>What accuracy means</h2>
<p>Most systems report how close the total quantity is to the count. That number hides errors, because an over-count in one location cancels a short count in another:</p>
<table>
<tr><th>SKU 4471</th><th class="num">System</th><th class="num">Shelf</th><th>Record right?</th></tr>
<tr><td>Location R3-B12</td><td class="num">40</td><td class="num">12</td><td>No</td></tr>
<tr><td>Location R7-B04</td><td class="num">0</td><td class="num">28</td><td>No</td></tr>
<tr class="oee-total"><td>Total</td><td class="num">40</td><td class="num">40</td><td>Total quantity: 100% accurate</td></tr>
</table>
<p>The total is perfect, yet both location records are wrong, and the picker sent to R3-B12 comes back short. The measure that matters on the floor is <strong>location accuracy</strong>: the share of locations whose SKU and quantity are both right, within a small tolerance for loose items. The WERC benchmark puts best-in-class inventory count accuracy by location at 99.5% or better.</p>
{eq(r"\text{Location accuracy} = \dfrac{\text{locations counted with the right SKU and quantity}}{\text{locations counted}}")}
<h2>Where records go wrong</h2>
<table>
<tr><th>Cause</th><th>How it happens</th><th>Fix at the source</th></tr>
<tr><td>Receiving miscount</td><td>The packing slip is keyed in, not the count. Short or over shipments go unnoticed</td><td>Count or scan at the door, against the ASN (Part&nbsp;3)</td></tr>
<tr><td>Wrong put-away location</td><td>The driver puts the pallet in the nearest hole and means to record it later</td><td>Scan the pallet and the location at put-away (Part&nbsp;3)</td></tr>
<tr><td>Mis-pick</td><td>Wrong item or wrong quantity taken, so two records are now wrong</td><td>Scan at pick (<a href="mis-picks-mis-ships-and-the-real-cost-of-an-error.html">Part&nbsp;5</a>)</td></tr>
<tr><td>Unrecorded moves</td><td>Stock moved to make room or to top up a pick face, with no transaction</td><td>A move is always a scan, or it does not happen</td></tr>
<tr><td>Damage and shrink</td><td>Broken cases thrown away without an adjustment</td><td>A damage bin and a weekly adjustment routine</td></tr>
</table>
<p>Busy locations go wrong most often because they have the most transactions. In the example the chance that a location's record goes wrong in a given week is taken as {pc1(Q.HAZ["A"])} for A items, {pc1(Q.HAZ["B"])} for B and {pc1(Q.HAZ["C"])} for C. About {pc(Q.PHANTOM)} of errors are phantom stock. A phantom on a busy location is usually found by a picker within a week or two, the hard way.</p>
<h2>Annual count or cycle counting</h2>
<p>The traditional fix is the wall-to-wall count: close the warehouse for a couple of days at year-end, count everything and correct the records. It gives a good number on one day. Records then decay all year, and the count does nothing about why they went wrong.</p>
<p>Cycle counting counts a few locations every day instead, so every location is counted several times a year and the busiest most often. The usual rule follows the <a href="{ABC1}.html">ABC classes</a>. In the example:</p>
{eq(r"\text{Counts a year} = \sum_{c} N_c \, f_c = %s \times %d + %s \times %d + %s \times %d = %s" % (f0(CC["A"]), FREQ["A"], f0(CC["B"]), FREQ["B"], f0(CC["C"]), FREQ["C"], tn(f0(COUNTS))))}
<p>That is A locations every {Q.PERIOD["A"]} weeks ({FREQ["A"]} times a year), B every {Q.PERIOD["B"]} weeks and C every {Q.PERIOD["C"]}. Over {DAYS} working days:</p>
{eq(r"\dfrac{%s}{%d} \approx %d \text{ counts a day} \times %d \text{ min} \approx %s \text{ hours a day}" % (tn(f0(COUNTS)), DAYS, round(COUNTS / DAYS), Q.T_COUNT, f1(COUNTS / DAYS * Q.T_COUNT / 60)))}
<p>One person for a quiet part of the morning, before the first wave of picking, with no shutdown.</p>
{figure_markup()}<h2>The result</h2>
<table>
<tr><th>Counting plan</th><th class="num">Average accuracy</th><th class="num">Lowest</th><th class="num">Short picks a year</th><th class="num">Counting hours</th><th class="num">Counting and searching</th><th class="num">Days closed</th></tr>
{rows}
</table>
{fig(fig_accuracy(), 3, "Location records right, week by week. The annual count gives one good day. Cycle counting keeps the records right all year.")}
<p>With the annual count alone, accuracy drifts down from {pc(AN["curve"][0])} to about {pc(AN["low"])} just before the year-end count, and averages {pc1(AN["avg"])} over the year. For most of the year one location record in five is wrong. ABC cycle counting holds it near {pc1(CY["avg"])} and cuts short picks from about {f0(AN["short"])} to {f0(CY["short"])} a year.</p>
<p>Be clear about the cost. Cycle counting takes more counting hours than one annual count: about {f0(CY["hours"])} against {f0(AN["hours"])} in the example's racks, or {f0(CY["total_h"])} against {f0(AN["total_h"])} hours including the time spent searching after short picks. What it buys is records that can be trusted on every day of the year, no two-day shutdown, and the information to fix the causes. In a real warehouse the annual count also covers all the shelving and usually needs every person in the building, which narrows the gap.</p>
<p>The biggest gain comes from fixing the causes. With scanning at receiving, put-away and picking, fewer records go wrong in the first place. Accuracy averages {pc1(FX["avg"])}, short picks fall to about {f0(FX["short"])} a year, and the B and C locations can be counted half as often, bringing the hours down to {f0(FX["hours"])}.</p>
<h2>How to run a cycle count</h2>
<ul>
<li><strong>Count blind.</strong> The counter sees the location and the SKU, not the system quantity, so they count instead of confirming.</li>
<li><strong>Recount before adjusting.</strong> A variance above the tolerance gets a second count by another person, then a check of open transactions such as stock received or picked that day.</li>
<li><strong>Log a cause for every adjustment.</strong> Receiving, put-away, pick, move or damage. The log is what tells you which fix to make.</li>
<li><strong>Count when it is quiet.</strong> First thing in the morning or between waves, and never a location with a pick in progress.</li>
<li><strong>Count when it is cheap.</strong> A location that has just been picked empty, or is down to its last cases, is quick to count, so count it then.</li>
<li><strong>Approve large adjustments.</strong> A manager signs off adjustments above a value limit, which also satisfies the auditors.</li>
</ul>
<h2>Measures to track</h2>
<table>
<tr><th>Measure</th><th>What it shows</th></tr>
<tr><td>Location accuracy from cycle counts</td><td>How far the records can be trusted. Track it by class and by zone</td></tr>
<tr><td>Short picks per 1,000 lines</td><td>Phantom stock found the hard way, by customers' orders</td></tr>
<tr><td>Adjustments by cause</td><td>Where the errors come from, and which fix to make next</td></tr>
<tr><td>Adjustment value, gross and net</td><td>Gross shows the size of the problem. Net hides it</td></tr>
<tr><td>Counts completed against plan</td><td>Whether the counting habit is holding</td></tr>
</table>
<h2>Common mistakes</h2>
<ul>
<li><strong>Measuring total quantity accuracy.</strong> Errors cancel out. Measure by location.</li>
<li><strong>Adjusting without a cause.</strong> The record is fixed and the process that broke it is not.</li>
<li><strong>Counting what is easy.</strong> The slow C items are quick to count and rarely wrong. The A items are where the errors are.</li>
<li><strong>Letting counting slip in busy weeks.</strong> Those are the weeks when records go wrong fastest.</li>
<li><strong>Raising safety stock to cover bad records.</strong> It hides the problem at the cost of cash tied up in stock. Fix the records, then <a href="{SS1}.html">set safety stock</a> properly.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>Phantom stock is the system showing stock that is not on the shelf. It is found by customers' orders, as short picks.</li>
<li>Measure location accuracy, not total quantity accuracy. Best in class is 99.5% or better.</li>
<li>An annual count gives one good day. In the example, records then fall to about {pc(AN["low"])} right before the next count.</li>
<li>ABC cycle counting takes about {f1(COUNTS / DAYS * Q.T_COUNT / 60)} hours a day here and keeps accuracy near {pc(CY["avg"])} all year.</li>
<li>Fixing the causes with scanning lifts accuracy further and cuts the counting needed.</li>
</ul>
<p>Earlier in this series: <a href="{W1}.html">Part&nbsp;1</a> won back space, <a href="{W2}.html">Part&nbsp;2</a> cut the pickers' walking, and <a href="{W3}.html">Part&nbsp;3</a> cleared the dock. Next: <a href="mis-picks-mis-ships-and-the-real-cost-of-an-error.html">Part&nbsp;5</a> looks at mis-picks and mis-ships, and what each error really costs.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://www.yale.com/globalassets/coms/yale/north-america/documents/white-papers/snack-drawer/YALE-1520_WERC-DC-Metrics-infographic.pdf" rel="noopener" target="_blank">Yale: WERC 2025 DC Measures, top metrics and best-in-class scores</a> (inventory count accuracy by location)</li>
</ul>
{NOTE}{js3d("wh3d4")}{mathjs()}"""
    body = nowrap(body, [(1, 0, 20), (2, 0, 24), (3, 0, 32)])
    return dict(slug=W4, title="Phantom Stock: Why Your System Says 40 and the Shelf Says 12",
                desc="Measure location accuracy, find where stock records go wrong, and compare an annual count with ABC cycle counting in one warehouse.",
                cats=["operational-efficiency", "inventory-management"], tags=["inventory accuracy", "cycle counting", "phantom inventory", "stock count", "location accuracy", "ABC analysis"],
                body=body, date=DATE, author="Quak Foo Lee", read="10 min read", series=SER(4), cover_label="Warehouse operations",
                related=[W3, ABC1, SS1])


if __name__ == "__main__":
    a = part4()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])} counts={COUNTS}\n")
