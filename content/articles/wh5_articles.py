"""Warehouse operations series for Insights (V5.35). Part 5: mis-picks, mis-ships and the real cost of an error.

Same distributor as Parts 1 to 4. The numbers come from wh5_model.py, which also sets the rates in the 3D pack line
(assets/js/wh3d5.js).

Usage:  python3 content/articles/wh5_articles.py
        python3 content/gen/add_article.py mis-picks-mis-ships-and-the-real-cost-of-an-error
        python3 content/gen/series_labels.py
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import js3d, nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, MUTED, DEFS, box, eq, tn, mathjs
import wh5_model as E
from wh_articles import W1, W2, SER
from wh3_articles import W3
from wh4_articles import W4

DATE = "2026-11-16"
W5 = "mis-picks-mis-ships-and-the-real-cost-of-an-error"
NOTE = ('<p class="oee-note"><em>The distributor, its error rates, times and costs are an illustrative example built from stated assumptions. '
        'The benchmarks are published industry figures. Measure your own error rate and cost per error before choosing checks.</em></p>')
f0 = lambda x: f"{x:,.0f}"
f1 = lambda x: f"{x:,.1f}"
pc2 = lambda x: f"{x * 100:.2f}%"
money = lambda x: f"${round(x, -2 if abs(x) < 10000 else -3):,.0f}"
S = E.all_steps(); S0, S1, S2, S3, S4 = S
LABEL = ["As-is", "1. Pack check", "2. Scan at pick", "3. Scan at pack", "4. Weigh at ship"]


def fig_stages():
    s = DEFS
    stages = [("At the pick face", E.COST_PICK, "The scanner says wrong item. Put it back, pick again", GREEND),
              ("At packing", E.COST_PACK, "The packer finds it. Someone walks back to re-pick", ORANGE),
              ("At the customer", E.COST_ESC, "Return, reship, handling, credit, and some customers lost", RED)]
    x0, w, gap, base, hmax = 30, 200, 30, 230, 150
    for i, (lab, c, note, col) in enumerate(stages):
        x = x0 + i * (w + gap); hh = max(6, hmax * (c / E.COST_ESC) ** 0.5)
        s += f'<rect x="{x + 50}" y="{base - hh:.1f}" width="{w - 100}" height="{hh:.1f}" rx="3" fill="{col}"/>'
        s += txt(x + w / 2, base - hh - 10, f"${c:,.2f}" if c < 1 else f"${c:,.0f}", "middle", NAVY, 17, True)
        s += txt(x + w / 2, base + 22, lab, "middle", NAVY, 13.5, True)
        words = note.split(); line = ""; yy = base + 42
        for wd in words:
            if len(line) + len(wd) > 30: s += txt(x + w / 2, yy, line.strip(), "middle", MUTED, 12); yy += 16; line = ""
            line += wd + " "
        s += txt(x + w / 2, yy, line.strip(), "middle", MUTED, 12)
        if i < 2: s += f'<line x1="{x + w - 12}" y1="{base - 70}" x2="{x + w + gap + 10}" y2="{base - 70}" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#ah)"/>'
    s += txt(360, 20, "Cost of one picking error, by where it is found", "middle", NAVY, 14, True)
    return svg(f"Bar diagram of the cost of one picking error by where it is found: about ${E.COST_PICK:.2f} at the pick face, about ${E.COST_PACK:.0f} at packing "
               f"and about ${E.COST_ESC:.0f} once it reaches the customer. Bar heights are drawn on a square-root scale so the smallest stays visible.", 720, 322, s, 560)


def fig_costs():
    x0, w = 170, 430; mx = max(s["total"] for s in S); sc = w / mx; out = ""
    parts = [("cost_esc", "Errors reaching customers", RED), ("cost_fix", "Errors fixed in-house", ORANGE), ("cost_check", "Checks: labour and equipment", BLUE)]
    lx = 20
    for _, lab, c in parts: out += f'<rect x="{lx}" y="10" width="12" height="12" rx="2" fill="{c}"/>' + txt(lx + 18, 21, lab, fill=NAVY, fs=12); lx += 30 + len(lab) * 6.6
    best = min(range(5), key=lambda i: S[i]["total"])
    for i, st in enumerate(S):
        y = 40 + i * 44; x = x0
        out += txt(x0 - 10, y + 19, LABEL[i], "end", NAVY, 13, i == best)
        for key, _, c in parts:
            ww = st[key] * sc; out += f'<rect x="{x:.1f}" y="{y}" width="{ww:.1f}" height="28" fill="{c}"/>'; x += ww
        out += txt(x + 8, y + 19, money(st["total"]) + (" lowest" if i == best else ""), fill=NAVY, fs=13, bold=True)
    out += txt(x0, 40 + 5 * 44 + 6, f"Yearly cost for {f0(E.ORDERS)} orders. Equipment spread over {E.LIFE} years.", fill=MUTED, fs=12)
    return svg(f"Stacked bars of the yearly cost of picking errors and of the checks, for each step. As-is the errors cost about {money(S0['total'])} a year. "
               f"With scanning at pick and at pack the total is about {money(S3['total'])}, the lowest. Adding a check scale raises it to about {money(S4['total'])}, "
               "because the scale costs more than the few errors it still catches.", 720, 290, out, 560)


def figure_markup():
    data = dict(steps=[dict(p=E.detection_probs(n), s=[round(st["shipped_right"], 5), round(st["esc"]), round(st["cost_esc"] + st["cost_fix"]),
                                                        round(st["cost_check"]), round(st["total"]), round(st["saving"])]) for n, st in enumerate(S)],
                mag=10, names=E.STEPS)
    js = json.dumps(data, separators=(",", ":"))
    btn = "".join(f'<button type="button" class="wh3d-step" data-s="{n}" aria-pressed="{"true" if n == 0 else "false"}"><b>{n}</b><span>{E.STEPS[n]}</span></button>' for n in range(5))
    return f"""<p>Figure 2 is the example's packing line. Each order leaves the pick zone on the left in a tote, the plastic bin the picker fills. At the pack station it is packed into a parcel, which passes the check scale (when it is on) and goes into the truck on the right. Red marks an order with an error. Every active checkpoint lights green as it checks an order, and red when it catches one, which then goes back along the re-pick lane. The check scale stops each parcel for a moment and shows its weight against the expected weight. An error that gets past every checkpoint goes to the customer, and a little later its return comes back. Errors are shown ten times more often than they happen so that you can see them. The figure steps through the fixes on its own, about twenty seconds each, until you pick one.</p>
<figure class="wh3d wh3d5" id="wh3d5">
<div class="wh3d-box">
<div class="wh3d-stage">
<canvas role="img" aria-label="3D model of the example distributor's packing line: totes on a conveyor from the pick zone, through a pick scanner and a pack station where they become parcels, over a check scale with a weight display, into a truck. Orders with errors are red; caught ones divert to a re-pick lane, and escaped ones go to the truck and later come back as returns."></canvas>
<span class="wh3d-drag" aria-hidden="true">Drag to turn</span>
<span class="wh3d-chip" id="wh3d5-chip">As-is</span>
<p class="wh3d-nogl" id="wh3d5-nogl" hidden>This browser cannot show the 3D model. The steps below still update the numbers.</p>
</div>
<div class="wh3d-panel">
<div class="wh3d-steps" role="group" aria-label="Checks, added in order">{btn}</div>
<div class="wh3d5-tour" id="wh3d5-tour" aria-hidden="true"><b><i></i></b><span></span></div>
<div class="wh3d-cells">
<div class="wh3d-cell wh3d-key"><span class="k">Orders shipped right</span><strong id="wh3d5-right"></strong></div>
<div class="wh3d-cell wh3d-key"><span class="k">Errors reaching customers a year</span><strong id="wh3d5-esc"></strong></div>
<div class="wh3d-cell"><span class="k">Cost of errors a year</span><strong id="wh3d5-cerr"></strong></div>
<div class="wh3d-cell"><span class="k">Cost of the checks a year</span><strong id="wh3d5-cchk"></strong></div>
<div class="wh3d-cell"><span class="k">Total a year</span><strong id="wh3d5-tot"></strong></div>
<div class="wh3d-cell"><span class="k">Saving against as-is</span><strong id="wh3d5-sav"></strong></div>
</div>
<p class="wh3d-say" id="wh3d5-say" aria-live="polite"></p>
<div class="wh3d-last"><ul class="wh3d-legend"><li><i style="background:#9FB2CC"></i>Tote (a picked order)</li><li><i style="background:#C9A46A"></i>Parcel (packed order)</li><li><i style="background:#FF5A4A"></i>Order with an error</li><li><i style="background:#8DC63F"></i>Checkpoint checking</li></ul>
<button type="button" class="wh3d-btn wh3d-small" id="wh3d5-names" aria-pressed="true">Station names</button></div>
</div>
</div>
<figcaption>Figure 2. The example's packing line. The checks apply in order and build on each other; step&nbsp;3 replaces the visual pack check with a scan. In the animation, errors are made ten times as often as in the model so that they can be seen; the catch rates are the model's. The numbers in the panel are the model's yearly figures for {f0(E.ORDERS)} orders.</figcaption>
<script type="application/json" id="wh3d5-data">{js}</script>
</figure>
"""


def part5():
    trs = "".join(f'<tr><td>{LABEL[i]}</td><td class="num">{pc2(st["picked_right"])}</td><td class="num">{pc2(st["shipped_right"])}</td><td class="num">{f0(st["esc"])}</td>'
                  f'<td class="num">{money(st["cost_esc"] + st["cost_fix"])}</td><td class="num">{money(st["cost_check"])}</td><td class="num">{money(st["total"])}</td></tr>' for i, st in enumerate(S))
    cost_rows = "".join(f'<tr><td>{k.replace("_", " ").capitalize()}</td><td class="num">${v:,.0f}</td></tr>' for k, v in E.COST_CUST.items())
    body = f"""{CSS}
<p>The customer ordered 12 cases of the 3/4-inch fitting and received 12 cases of the 1/2-inch. Now there is a phone call, a return label, a second shipment, a credit note, a carton coming back to be received and restocked, and a customer wondering whether to order from you next time. Picking that line took about twenty seconds. Fixing it takes most of an hour and a good part of the margin on the order.</p>
<p>Parts&nbsp;1 to 4 made the warehouse faster and its records right. This part looks at the errors that still get through: what they cost, where they come from, and which checks pay for themselves in the example warehouse.</p>
<h2>An error costs more the later it is found</h2>
{fig(fig_stages(), 1, "The same mistake, caught at three points. The cost rises by about ten times at each step, the old 1-10-100 rule.")}
<p>Published estimates put the cost of one mis-pick that reaches the customer at about $22 to $100, depending on the product, the freight and the customer. Operations that do not use barcodes commonly see error rates of 1 to 2%. The example uses ${E.COST_ESC:.0f} for an error that reaches the customer, built up as follows:</p>
<table>
<tr><th>Cost of one error at the customer</th><th class="num">Assumed</th></tr>
{cost_rows}
<tr class="oee-total"><td>Total</td><td class="num">${E.COST_ESC:,.0f}</td></tr>
</table>
<p>The lost-customer line is an expected value: a small share of customers who receive a wrong order buy less afterwards, and that lost margin is spread over every error.</p>
<h2>The example's errors</h2>
<p>The distributor picks {f0(E.LINES)} lines a year for {f0(E.ORDERS)} orders. With paper pick lists, {pc2(sum(E.P_ERR.values()))} of lines are picked wrong: the wrong item ({pc2(E.P_ERR["item"])} of lines), the wrong quantity ({pc2(E.P_ERR["qty"])}) or the right item in the wrong order's tote after batch picking ({pc2(E.P_ERR["tote"])}). That is about {f0(S0["made"])} errors a year, and with no check before shipping every one reaches a customer.</p>
{eq(r"\text{Cost of errors a year} = %s \times \$%d \approx %s" % (tn(f0(S0["esc"])), E.COST_ESC, tn("\\$" + f0(S0["cost_esc"]))))}
<p>Order picking accuracy is about {pc2(S0["picked_right"])} of orders. The WERC benchmark puts best-in-class order picking accuracy at 99.68% or better in its 2025 report, and earlier reports gave a median of about 99.3%, so the example sits in the bottom group.</p>
<h2>The checks, in order</h2>
<p><strong>Check 1: compare at packing.</strong> The packer compares each case with the packing slip before taping the carton. It costs about {f0(E.T_VISUAL)} seconds an order and needs nothing new. A careful visual check catches perhaps half to two-thirds of errors: in the example about {f0(S1["caught_pack"])} a year, which leaves {f0(S1["esc"])} going out.</p>
<p><strong>Check 2: scan at the pick face.</strong> A handheld scanner confirms the location and the item at each pick, and the tote at each put. A wrong item or a wrong tote is refused at the shelf, where fixing it costs a few seconds. Quantity errors are harder: the picker scans once and keys the quantity, so many still get through. In the example, scanning stops about {f0(S2["caught_pick"])} errors at the shelf, and orders picked right rise to {pc2(S2["picked_right"])}. It needs handhelds and a mobile licence, about {money(E.EQUIP[2][0])} up front and {money(E.EQUIP[2][1])} a year.</p>
<p><strong>Check 3: scan every case at packing.</strong> Replace the visual check with a scan of each case against the order. It catches almost every remaining wrong item and most wrong quantities, and at about {f0(E.T_SCAN_PACK)} seconds a line it takes less time than the visual check for a typical order. Errors reaching customers fall to about {f0(S3["esc"])} a year, and orders shipped right reach {pc2(S3["shipped_right"])}.</p>
<p><strong>Check 4: weigh the parcel.</strong> A check scale compares each packed parcel with its expected weight. It catches most remaining quantity errors, but by now there are very few to catch: about {f0(S4["caught_weigh"])} a year. The scale and the {f0(E.T_WEIGH)} seconds an order cost more than they save, and the total rises from {money(S3["total"])} to {money(S4["total"])}. A check scale pays where errors are frequent or costly, for example many small, similar items or expensive goods. In this warehouse, after scanning, it does not.</p>
{figure_markup()}<h2>The result</h2>
<table>
<tr><th>Step</th><th class="num">Orders picked right</th><th class="num">Orders shipped right</th><th class="num">Errors to customers</th><th class="num">Cost of errors</th><th class="num">Cost of checks</th><th class="num">Total a year</th></tr>
{trs}
</table>
{fig(fig_costs(), 3, "Yearly cost of errors and checks. Scanning at pick and at pack gives the lowest total. The check scale adds more cost than it removes.")}
<p>Scanning at the pick face and at packing takes the example from about {money(S0["total"])} a year in errors to about {money(S3["total"])} in errors and checks together, a saving of about {money(S3["saving"])} a year. The handhelds pay for themselves within months. Accuracy is the other half of the story: the customer now gets the right order {pc2(S3["shipped_right"])} of the time.</p>
<h2>Fix the causes too</h2>
<p>Checks catch errors. The cause log tells you why they happened. Most mis-picks come from a short list:</p>
<ul>
<li><strong>Look-alike items side by side.</strong> Two sizes of the same fitting in neighbouring slots. Separate them when re-slotting (Part&nbsp;1).</li>
<li><strong>Poor labels.</strong> Faded, missing or ambiguous location labels. Label every location and every pick face clearly, with a barcode.</li>
<li><strong>Wrong records.</strong> The system sends the picker to a location holding something else. That is phantom stock (Part&nbsp;4).</li>
<li><strong>Units of measure.</strong> A case of 12 against a pack of 6. Show the unit on the pick list and the scanner screen.</li>
<li><strong>Pressure at the cut-off.</strong> Errors cluster in the last hour before the truck. Wave release (Part&nbsp;2) spreads the load.</li>
</ul>
<h2>Measures to track</h2>
<table>
<tr><th>Measure</th><th>What it shows</th></tr>
<tr><td>Order picking accuracy, by order</td><td>Errors made in picking, caught or not. The WERC definition</td></tr>
<tr><td>Orders shipped right</td><td>What the customer sees. The core of a perfect order rate</td></tr>
<tr><td>Errors caught by checkpoint</td><td>Which checks are doing the work, and which may not be needed</td></tr>
<tr><td>Errors by cause, picker and location</td><td>Where to fix the process. Used for coaching, not blame</td></tr>
<tr><td>Cost per error reaching a customer</td><td>The number that justifies the checks</td></tr>
</table>
<h2>Common mistakes</h2>
<ul>
<li><strong>Not knowing the cost of an error.</strong> Without it, every check looks either essential or unaffordable.</li>
<li><strong>Checking everything twice.</strong> Each check costs time on every order. Add checks where errors are, and stop when the next one costs more than it saves.</li>
<li><strong>Allowing scan overrides.</strong> A scanner that lets the picker skip a "wrong item" warning catches nothing.</li>
<li><strong>Blaming people for system errors.</strong> Most mis-picks trace back to slotting, labels and records.</li>
<li><strong>Measuring at the dock only.</strong> Count returns and customer complaints too, or escaped errors stay invisible.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>An error costs about ten times more at each later stage: cents at the shelf, dollars at packing, ${E.COST_ESC:.0f} at the customer here.</li>
<li>With paper picking and no checks, the example sends about {f0(S0["esc"])} errors a year to customers, costing about {money(S0["cost_esc"])}.</li>
<li>Scanning at the pick face and at packing cuts that to about {f0(S3["esc"])} errors and saves about {money(S3["saving"])} a year, including the cost of the checks.</li>
<li>Stop adding checks when the next one costs more than the errors it catches: here, the check scale.</li>
<li>Log the cause of every error, and fix slotting, labels and records as well as checking.</li>
</ul>
<p>Earlier in this series: <a href="{W1}.html">Part&nbsp;1</a> space and slotting, <a href="{W2}.html">Part&nbsp;2</a> picking, <a href="{W3}.html">Part&nbsp;3</a> the dock, and <a href="{W4}.html">Part&nbsp;4</a> stock records. Next: <a href="peak-season-without-the-panic-warehouse-labour-planning.html">Part&nbsp;6</a> plans labour for the peak season.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://www.yale.com/globalassets/coms/yale/north-america/documents/white-papers/improving-dc-metrics.pdf" rel="noopener" target="_blank">Yale: Improving DC metrics, with WERC 2025 DC Measures</a> (best-in-class order picking accuracy)</li>
<li><a href="https://sps.honeywell.com/us/en/support/blog/productivity/which-metrics-matter-most-to-dc-operations" rel="noopener" target="_blank">Honeywell: Which metrics matter most to DC operations</a> (WERC order picking accuracy median)</li>
<li><a href="https://dmsiworks.com/blog/the-cost-of-a-mispick-improve-the-bottom-line-by-reducing-errors" rel="noopener" target="_blank">DMSi: The cost of a mispick</a> (cost per mis-pick)</li>
<li><a href="https://www.fcbco.com/blog/6-ways-to-reduce-picking-errors" rel="noopener" target="_blank">FCBCO: 6 ways to reduce picking errors</a> (error rates without barcodes)</li>
</ul>
{NOTE}{js3d("wh3d5")}{mathjs()}"""
    body = nowrap(body, [(2, 0, 18)])
    return dict(slug=W5, title="Mis-Picks, Mis-Ships and the Real Cost of an Error",
                desc="What a picking error really costs, where to catch it, and which checks pay in an SME warehouse: pack checks, scanning and check scales.",
                cats=["operational-efficiency", "inventory-management"], tags=["picking accuracy", "mis-pick", "order accuracy", "barcode scanning", "pack verification", "perfect order"],
                body=body, date=DATE, author="Quak Foo Lee", read="10 min read", series=SER(5), cover_label="Warehouse operations",
                related=[W2, W4, W3])


if __name__ == "__main__":
    a = part5()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])}\n")
