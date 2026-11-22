"""Warehouse layout series for Insights (V5.71). Part 5: from layout to cash.

Inventory turns and a layout payback calculator. The calculator (assets/js/wl5.js) starts from the Vancouver
distributor of Parts 1 to 3 and Ridgeline Coatings of Part 4; every number quoted here comes from
content/articles/wl5_results.json, written by wl5_model.js from the results of Parts 1-4 and one new Layout Lab check.

Usage:  node content/articles/wl5_model.js
        python3 content/articles/wl5_articles.py
        python3 content/gen/add_article.py from-layout-to-cash-inventory-turns-and-a-layout-payback-calculator
        python3 content/gen/series_labels.py
"""
import json, math, os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, MUTED, LINE, eq, im, mathjs, tn

DATE = "2026-11-22"
WL1 = "good-layout-bad-layout-what-travel-and-congestion-cost-an-sme-warehouse"
WL2 = "u-shape-straight-through-or-l-shape-choosing-a-warehouse-flow-pattern"
WL3 = "wide-narrow-or-very-narrow-aisles-warehouse-density-against-access"
WL4 = "central-store-supermarket-or-kanban-feeding-the-production-line"
WL5 = "from-layout-to-cash-inventory-turns-and-a-layout-payback-calculator"
SS = "setting-safety-stock"
ABC = "abc-inventory-analysis"
OEE3 = "oee-project-payback"
SER = lambda n: {"name": "Warehouse layout series", "part": n, "of": 5}
SIM = "../assets/sim/layout-lab.html"
D = json.load(open(os.path.join(HERE, "wl5_results.json"), encoding="utf-8"))
PR = D["presets"]; CA = D["calc"]; P = D["P"]
Pd, Pm = PR["dist"], PR["mfg"]
NOTE = ('<p class="oee-note"><em>The distributor and Ridgeline Coatings are illustrative examples: their inventory, cost of goods sold, delivery costs, '
        'dead stock and project costs are stated assumptions, and the operating savings come from the simplified Layout Lab model. Put your own numbers in '
        'the calculator before you make a decision. This is not financial advice.</em></p>')
f0 = lambda x: f"{x:,.0f}"
f1 = lambda x: f"{x:,.1f}"
money = lambda x: ("−" if x < 0 else "") + f"${round(abs(x) / 1000) * 1000:,.0f}"
GREY = "#9AA8BA"


def fig_deliveries():
    """Truck minutes on site against inbound deliveries a day, the same pallets, as-is against redesigned (Part 1)."""
    V = D["deliveries"]; x0, y0, w, h = 70, 30, 560, 220
    xmin, xmax = V[0]["trucks"], V[-1]["trucks"]
    ymax = 100
    X = lambda v: x0 + (v - xmin) / (xmax - xmin) * w
    Y = lambda m: y0 + h - m / ymax * h
    s = ""
    for t in range(0, ymax + 1, 20):
        s += f'<line x1="{x0}" y1="{Y(t):.1f}" x2="{x0 + w}" y2="{Y(t):.1f}" stroke="#E4E1D8"/>' + txt(x0 - 8, Y(t) + 4, str(t), "end", MUTED, 12)
    for v in V: s += txt(X(v["trucks"]), y0 + h + 18, str(v["trucks"]), "middle", MUTED, 12)
    s += txt(x0 + w / 2, y0 + h + 40, "Inbound deliveries a day (the same pallets, in smaller loads)", "middle", NAVY, 12.5, True)
    s += f'<text x="20" y="{y0 + h / 2}" transform="rotate(-90 20 {y0 + h / 2})" text-anchor="middle" font-size="12.5" font-weight="600" fill="{NAVY}">Minutes a truck is on site</text>'
    for k, col, lab in (("asis", ORANGE, "As-is layout"), ("redesign", GREEND, "Redesigned layout")):
        pts = [(X(v["trucks"]), Y(v[k]["truckIn"])) for v in V]
        s += f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{col}" stroke-width="2.6"/>'
        s += "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3.4" fill="{col}"/>' for a, b in pts)
    for i, (col, lab) in enumerate(((ORANGE, "As-is layout"), (GREEND, "Redesigned layout"))):
        s += f'<rect x="{x0 + w - 170}" y="{y0 + 6 + i * 18}" width="12" height="12" rx="2" fill="{col}"/>' + txt(x0 + w - 152, y0 + 16 + i * 18, lab, fill=NAVY, fs=12.5, bold=True)
    a, b = V[0], V[-1]
    return svg(f"Line chart of minutes a truck spends on site against inbound deliveries a day. As-is: {f0(a['asis']['truckIn'])} minutes at {a['trucks']} deliveries and "
               f"{f0(b['asis']['truckIn'])} at {b['trucks']}, with detention charges rising. Redesigned: {f0(a['redesign']['truckIn'])} minutes falling to {f0(b['redesign']['truckIn'])}.",
               700, 310, s, 560)


def fig_cash():
    """Where the distributor's cash comes from: yearly items and one-off items."""
    c = CA["dist"]["lo"]
    carry = c["freed"] * Pd["carry"] / 100
    hold = Pd["dead"] * Pd["hold"] / 100
    rows = [("Picking labour saved", Pd["labour"], "y"), ("Truck detention saved", Pd["other"], "y"), ("Carrying cost on stock freed", carry, "y"),
            ("Holding cost on dead stock cleared", hold, "y"), ("Extra freight for more deliveries", -c["freight"], "y"),
            ("Cycle stock freed (once)", c["freed"], "o"), ("Dead stock sold (once)", c["deadCash"], "o")]
    x0, w, rh = 270, 330, 30
    mx = max(abs(r[1]) for r in rows); mn = min(0, min(r[1] for r in rows))
    span = mx - mn; X = lambda v: x0 + (v - mn) / span * w
    s = ""; y = 20
    s += txt(x0 - 12, 14, "Every year", "end", MUTED, 12, True)
    for i, (lab, v, kind) in enumerate(rows):
        if kind == "o" and rows[i - 1][2] == "y":
            y += 14; s += txt(x0 - 12, y - 2, "Once", "end", MUTED, 12, True); y += 6
        col = (GREEND if v >= 0 else RED) if kind == "y" else BLUE
        s += txt(x0 - 12, y + rh / 2 + 4, lab, "end", NAVY, 12.5)
        s += f'<rect x="{min(X(0), X(v)):.1f}" y="{y + 4}" width="{abs(X(v) - X(0)):.1f}" height="{rh - 10}" fill="{col}"/>'
        s += txt(max(X(0), X(v)) + 6, y + rh / 2 + 4, money(v), "start", NAVY, 12.5, True)
        y += rh
    s += f'<line x1="{X(0):.1f}" y1="16" x2="{X(0):.1f}" y2="{y + 2}" stroke="{NAVY}" stroke-width="1"/>'
    return svg("Bar chart of the distributor's cash: every year, picking labour saved " + money(Pd["labour"]) + ", detention saved " + money(Pd["other"]) +
               ", carrying cost " + money(carry) + ", holding cost " + money(hold) + ", less extra freight " + money(c["freight"]) +
               "; once, cycle stock freed " + money(c["freed"]) + " and dead stock sold " + money(c["deadCash"]) + ".", 700, y + 16, s, 560)


def calc_html():
    def inp(k, lab, unit, step, help_=""):
        h = f'<small>{help_}</small>' if help_ else ""
        return f'<label class="wl5-f" for="wl5-{k}"><span>{lab}</span><span class="wl5-in"><input type="number" id="wl5-{k}" step="any" min="0" inputmode="decimal"><em>{unit}</em></span>{h}</label>'
    pre = {k: dict(v) for k, v in PR.items()}
    pre["dist"]["note"] = "The distributor of Parts 1 to 3: savings from the Part 1 redesign; inventory, freight and dead stock are illustrative."
    pre["mfg"]["note"] = "Ridgeline Coatings, Part 4: overtime saved moving from the central store to the kanban milk run; two bins add stock at the lines."
    data = html.escape(json.dumps({k: {q: v for q, v in d.items()} for k, d in pre.items()}), quote=True)
    return f"""<style>
.wl5 fieldset{{border:1px solid var(--line-2);border-radius:8px;padding:12px 14px 6px;margin:0;min-width:0}}
.wl5 legend{{font-weight:600;color:var(--ink);padding:0 6px;font-size:14.5px}}
.wl5-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}}
.wl5-f{{display:flex;flex-direction:column;gap:3px;margin:0 0 10px;font-size:13.5px;color:var(--ink)}}
.wl5-in{{display:flex;align-items:center;gap:6px}}
.wl5-in input{{width:100%;min-width:0;padding:6px 8px;border:1px solid var(--line-2);border-radius:6px;font:inherit;font-variant-numeric:tabular-nums;background:#fff}}
.wl5-in em{{font-style:normal;color:var(--muted);font-size:12.5px;white-space:nowrap}}
.wl5-f small{{color:var(--muted);font-size:12px;line-height:1.35}}
.wl5-pre{{display:flex;flex-wrap:wrap;gap:8px;align-items:center}}
.wl5-pre button{{font:inherit;font-size:14px;padding:6px 12px;border-radius:999px;border:1px solid var(--line-2);background:#fff;cursor:pointer;color:var(--ink)}}
.wl5-pre button[aria-pressed="true"]{{background:var(--ink);color:#fff;border-color:var(--ink)}}
#wl5-note{{font-size:13px;color:var(--muted);margin:0}}
</style>
<div class="oee-calc wl5" id="wl5-calc" role="group" aria-labelledby="wl5h" data-presets="{data}">
<h3 id="wl5h">Try it: layout to cash</h3>
<div class="wl5-pre"><span style="font-size:13.5px;color:var(--muted)">Start from:</span><button type="button" data-preset="dist" aria-pressed="true">Distributor (Parts 1 to 3)</button><button type="button" data-preset="mfg" aria-pressed="false">Ridgeline Coatings (Part 4)</button></div>
<p id="wl5-note"></p>
<div class="wl5-grid">
<fieldset><legend>1. What the layout saves every year</legend>
{inp("labour", "Labour saved", "$ a year", 1000, "Picking or handling hours saved, if they are cut or replace paid work.")}
{inp("other", "Other running costs saved", "$ a year", 1000, "Truck detention, overtime.")}
{inp("rent", "Rent avoided", "$ a year", 1000, "Space you no longer lease (Part&nbsp;3).")}
{inp("cost", "One-off cost of the change", "$", 1000, "Moving racks, engineering, permits, labels, disruption.")}
</fieldset>
<fieldset><legend>2. Smaller, more frequent deliveries</legend>
{inp("inv", "Average inventory", "$", 10000)}
{inp("cogs", "Cost of goods sold", "$ a year", 10000)}
{inp("cycShare", "Cycle stock of the suppliers that change", "% of inventory", 1, "The stock that goes up and down between their deliveries.")}
{inp("freqX", "Deliveries become", "times as often", 0.5)}
{inp("extraDel", "Extra deliveries", "a week", 1)}
{inp("delCost", "Extra freight per extra delivery", "$", 5)}
</fieldset>
<fieldset><legend>3. Dead stock and carrying cost</legend>
{inp("dead", "Dead stock cleared in the re-layout", "$ at cost", 1000)}
{inp("recov", "Recovered when sold or returned", "%", 5)}
{inp("hold", "Holding cost of dead stock you actually save", "% a year", 1, "Insurance and shrinkage; add space and handling only if rent or labour really fall.")}
{inp("carry", "Carrying cost you actually save", "% a year", 1, "The cash part: capital, insurance, shrinkage. Count space and handling (to 20% to 30% in all) only if rent or labour really fall.")}
{inp("lineStock", "Extra stock the change adds", "$", 100, "For example, two bins at the lines (Part&nbsp;4).")}
</fieldset>
</div>
<div class="oee-tiles" aria-live="polite">
<div class="oee-tile"><span class="k">Cash every year</span><span class="v" id="wl5-yearly"></span><span class="n">savings, less extra freight</span></div>
<div class="oee-tile"><span class="k">Cash once</span><span class="v" id="wl5-once"></span><span class="n">stock freed and dead stock sold, less the cost of the change</span></div>
<div class="oee-tile key"><span class="k">Payback, layout only</span><span class="v" id="wl5-payl"></span><span class="n">from section 1 alone</span></div>
<div class="oee-tile key"><span class="k">Payback, all moves</span><span class="v" id="wl5-pay"></span><span class="n" id="wl5-pay-n"></span></div>
<div class="oee-tile"><span class="k">Cash over 3 years</span><span class="v" id="wl5-three"></span><span class="n">undiscounted</span></div>
<div class="oee-tile"><span class="k">Inventory turns</span><span class="v" id="wl5-turns"></span><span class="n" id="wl5-dio"></span></div>
<div class="oee-tile"><span class="k">Cycle stock freed</span><span class="v" id="wl5-freed"></span><span class="n" id="wl5-be"></span></div>
</div>
<p class="oee-hint" id="wl5-wd"></p>
</div>"""


def part5():
    dl, dh = CA["dist"]["lo"], CA["dist"]["hi"]
    ll, lh = CA["distLayout"]["lo"], CA["distLayout"]["hi"]
    ml, mh = CA["mfg"]["lo"], CA["mfg"]["hi"]
    V = D["deliveries"]; v14, v28 = V[0], V[-1]
    pay = lambda c: "covered by the stock freed" if c["payback"] == 0 else ("never" if c["payback"] is None else f'{f1(c["payback"])} months')
    carry_freed = dl["freed"] * Pd["carry"] / 100
    rows = [
        ("Yearly savings from the layout", money(Pd["labour"] + Pd["other"]), money(Pm["labour"] + Pm["other"])),
        ("One-off cost of the change", f'{money(Pd["cost"][0])} to {money(Pd["cost"][1])}', f'{money(Pm["cost"][0])} to {money(Pm["cost"][1])}'),
        ("Payback, layout only", f'{f1(ll["payback"])} to {f1(lh["payback"])} months', f'{f1(CA["mfgLayout"]["lo"]["payback"])} to {f1(CA["mfgLayout"]["hi"]["payback"])} months'),
        ("Cycle stock freed by more frequent deliveries", money(dl["freed"]), "None"),
        ("Extra freight a year", money(dl["freight"]), "None"),
        ("Dead stock sold (written off)", f'{money(dl["deadCash"])} ({money(dl["writeDown"])})', "None"),
        ("Extra stock at the lines", "None", money(Pm["lineStock"])),
        ("Cash every year, all moves", money(dl["yearly"]), money(ml["yearly"])),
        ("Payback, all moves", pay(dl), f'{f1(ml["payback"])} to {f1(mh["payback"])} months'),
        ("Inventory turns", f'{dl["turns0"]:.1f} → {dl["turns1"]:.1f}', f'{ml["turns0"]:.2f} → {ml["turns1"]:.2f}'),
        ("Days of stock", f'{f0(dl["dio0"])} → {f0(dl["dio1"])}', f'{f0(ml["dio0"])} → {f0(ml["dio1"])}'),
    ]
    trs = "".join(f'<tr><td>{a}</td><td class="num">{b}</td><td class="num">{c}</td></tr>' for a, b, c in rows)
    body = f"""{CSS}
<p>Parts <a href="{WL1}.html">1</a> to <a href="{WL4}.html">4</a> measured what a layout does to walking, waiting, dock time, space and line stops. This last part turns those results into cash: how much a better layout frees each year, how much it frees once, how fast it pays back, and what it does to inventory turns.</p>
<p>The honest answer is that most of the cash from a layout comes from people and space, not from inventory. A layout raises inventory turns only when you use what it makes possible: a dock that can take smaller, more frequent deliveries, and a re-layout that clears out dead stock. The calculator below keeps the three apart, so you can see which part of the case is carrying the result.</p>
<h2>Three ways a layout turns into cash</h2>
<p class="oee-cap">Table 1. Where the cash comes from</p>
<table>
<tr><th>Source</th><th>Cash every year or once</th><th>What the series showed</th></tr>
<tr><td>Running costs: labour, truck detention, overtime</td><td>Every year</td><td><a href="{WL1}.html">Part&nbsp;1</a>: about {money(Pd["labour"])} of picking labour and {money(Pd["other"])} of detention a year (averages of ten simulated days). <a href="{WL4}.html">Part&nbsp;4</a>: {money(Pm["other"])} of overtime a year.</td></tr>
<tr><td>Space: rent avoided or a move put off</td><td>Every year</td><td><a href="{WL3}.html">Part&nbsp;3</a>: narrower aisles fit up to 1,440 more pallet positions instead of leasing more space.</td></tr>
<tr><td>Inventory: less stock for the same sales</td><td>Once, plus a smaller carrying cost every year</td><td>Only if deliveries become smaller and more frequent, or dead stock is cleared. This part.</td></tr>
</table>
<h2>Inventory turns and days of stock</h2>
<p>Inventory turns compare what you sell, at cost, with what you hold:</p>
{eq(r"\text{Turns} = \frac{\text{Cost of goods sold}}{\text{Average inventory}}")}
{eq(r"\text{Days of stock} = \frac{365}{\text{Turns}}")}
<p>The illustrative distributor sells ${Pd["cogs"] / 1e6:.0f}M a year at cost and holds ${Pd["inv"] / 1e6:.1f}M of stock on average: {dl["turns0"]:.0f} turns, or {f0(dl["dio0"])} days of stock. Carrying costs are usually quoted at 20% to 30% of inventory value a year: capital, space, insurance, handling, shrinkage and obsolescence. But when stock falls, only part of that becomes cash. The capital, insurance and shrinkage go; the space and handling go only if rent or labour actually fall. The calculator therefore starts at {Pd["carry"]}% for the cash part, and you can raise it if the space would really be released.</p>
<p>A layout changes neither number on its own. Picking faster does not shrink the stock, and putting pallets away an hour sooner frees a few thousand dollars at most. What does shrink it:</p>
<ul>
<li><strong>Smaller, more frequent deliveries.</strong> Between deliveries, stock falls from a full order to nothing, so on average you hold half an order: the cycle stock. Receive twice as often in half the quantity, and that cycle stock halves. But every extra delivery needs dock time, and a congested dock is the usual reason a business buys in big lots.</li>
<li><strong>Dead stock cleared.</strong> A re-layout means touching every pallet, which is the moment to find and sell, return or scrap the stock that has not moved for a year.</li>
</ul>
<h2>Can the dock take more deliveries?</h2>
<p>To test the first lever, the Part&nbsp;1 distributor received the same pallets in more, smaller deliveries: from {v14["trucks"]} trucks a day up to {v28["trucks"]}, averaged over five simulated days.</p>
{fig(fig_deliveries(), 1, "Minutes a truck spends on site as the same pallets arrive in more, smaller deliveries. The redesigned dock absorbs the extra trucks; the as-is dock does not.")}
<ul>
<li><strong>The as-is layout already cannot keep up.</strong> With equal loads, trucks spend {f0(v14["asis"]["truckIn"])} minutes on site at {v14["trucks"]} deliveries and still {f0(v28["asis"]["truckIn"])} at {v28["trucks"]}; detention stays between {money(min(v["asis"]["detYear"] for v in V))} and {money(max(v["asis"]["detYear"] for v in V))} a year, and about {f0(sum(v["asis"]["notAway"] for v in V) / len(V))} pallets are still not put away at the end of the shift at every number of deliveries. (With Part&nbsp;1's own mix of full and part loads, the as-is trucks spend {f0(D["mix14"]["asis"]["truckIn"])} minutes on site, averaged over ten days; {f0(D["mix14"]["asis"]["day"])} on Part&nbsp;1's example day.)</li>
<li><strong>The redesigned layout can.</strong> Trucks spend {f0(v14["redesign"]["truckIn"])} minutes on site at {v14["trucks"]} deliveries and {f0(v28["redesign"]["truckIn"])} at {v28["trucks"]}, with no detention and every pallet put away.</li>
<li><strong>The bottleneck is the forklift behind the dock, not the doors.</strong> Give the as-is layout a second forklift and its trucks spend {f0(D["twoForks"][0]["asis"]["truckIn"])} and {f0(D["twoForks"][1]["asis"]["truckIn"])} minutes on site, the same as the redesign. A second forklift is another way to free the dock, though it does nothing for the pickers' walking, and a driver for a full shift (about ${f0(P['wage'] * 8 * P['days'] / 1000)},000 a year at ${f0(P['wage'])} an hour, before the truck itself) costs more than the {money(Pd['other'])} a year of detention it would save.</li>
</ul>
<p>So the redesign (or a second forklift) does not raise turns by itself, but it removes the dock as the reason to keep buying in big lots. Whether to receive more often is then a buying decision: it depends on what each extra delivery costs.</p>
<h2>When more deliveries pay</h2>
<p>The cycle stock freed, and the break-even freight per extra delivery, are</p>
{eq(r"\text{Freed} = I \times s \times \left(1 - \frac{1}{f}\right)")}
{eq(r"\text{Break-even} = \frac{\text{Freed} \times c}{n}")}
<p>where {im("I")} is average inventory, {im("s")} the share of it that is cycle stock of the suppliers that change, {im("f")} how many times as often they deliver, {im("c")} the carrying cost rate and {im("n")} the extra deliveries a year. For the distributor, the suppliers behind 7 of its 14 daily trucks, holding {Pd["cycShare"]}% of the inventory as cycle stock, deliver twice as often: {f0(Pd["extraDel"])} extra deliveries a week. That frees {money(dl["freed"])} once, over the next few delivery cycles, and saves {money(carry_freed)} a year in carrying cost at {Pd["carry"]}%. So the extra deliveries pay for themselves only if each costs less than <strong>${dl["breakEven"]:.0f}</strong> in extra freight (${D["calc"]["dist25"]["lo"]["breakEven"]:.0f} if the full 25% carrying cost would really be saved). At the ${f0(Pd["delCost"])} a delivery in the example, they cost {money(dl["freight"] - carry_freed)} a year more than they save. They are still worth considering when cash is tight, because they bring in {money(dl["freed"])} up front; with a supplier's own trucks on fixed routes, the extra cost can be close to nothing.</p>
<h2>The calculator</h2>
<p>Start from either example, then put in your own numbers. All amounts are in Canadian dollars.</p>
{calc_html()}
<h2>The two examples</h2>
<p class="oee-cap">Table 2. The two examples in the calculator, at the low and high end of the one-off cost</p>
<table>
<tr><th>Measure</th><th class="num">Distributor (Parts 1 to 3)</th><th class="num">Ridgeline Coatings (Part 4)</th></tr>
{trs}
</table>
{fig(fig_cash(), 2, "Where the distributor's cash comes from. The yearly cash is mostly labour and detention; inventory adds a one-off sum and a small yearly saving, less the extra freight.")}
<ul>
<li><strong>The distributor's layout pays back on running costs alone</strong>, in {f1(ll["payback"])} to {f1(lh["payback"])} months, from {money(Pd["labour"])} of picking labour and {money(Pd["other"])} of detention a year (averages of Part&nbsp;1's ten simulated days). The one-off cost is moving about 3,360 pallet positions of racking at the Part&nbsp;3 rates, plus engineering, permits and labels.</li>
<li><strong>The inventory moves bring cash forward but cost a little every year.</strong> More frequent deliveries free {money(dl["freed"])} and clearing dead stock brings in {money(dl["deadCash"])}, enough to cover the one-off cost once deliveries change. But the extra freight outweighs the carrying cost saved, so the yearly cash falls from {money(ll["yearly"])} to {money(dl["yearly"])}. Turns rise from {dl["turns0"]:.1f} to {dl["turns1"]:.1f} and days of stock fall from {f0(dl["dio0"])} to {f0(dl["dio1"])}; without the dead stock, turns would reach {D["calc"]["distNoDead"]["lo"]["turns1"]:.2f}. Clearing dead stock does not need a new layout, and it means an {money(dl["writeDown"])} write-off: that cash was lost when the stock was bought, not when it is cleared.</li>
<li><strong>Ridgeline pays back in about {f1(CA["mfgLayout"]["lo"]["payback"])} to {f1(CA["mfgLayout"]["hi"]["payback"])} months</strong> on overtime alone ({f1(ml["payback"])} to {f1(mh["payback"])} months after the extra stock at the lines), and its turns fall slightly, from {ml["turns0"]:.2f} to {ml["turns1"]:.2f}: the second bin at each line adds {money(Pm["lineStock"])} of stock. Not every good layout change raises turns; some trade a little stock for a lot of uptime.</li>
</ul>
<h2>What the calculator leaves out</h2>
<ul>
<li><strong>Labour savings are cash only when hours are cut</strong> or the freed time replaces overtime, temporary staff or hiring. Time freed and kept on the payroll is capacity, not cash.</li>
<li><strong>Disruption.</strong> A re-layout stops or slows the warehouse for days. Put the lost output or overtime into the one-off cost.</li>
<li><strong>Safety stock.</strong> More frequent deliveries can also reduce safety stock (see <a href="{SS}.html">setting safety stock</a>), but only if the supplier's lead time and reliability improve too; the calculator counts cycle stock only.</li>
<li><strong>Tax, financing and the time value of money.</strong> The 3-year cash is undiscounted. For longer projects, use a discounted payback, as in the <a href="{OEE3}.html">OEE project payback</a> post.</li>
<li><strong>Which stock to change.</strong> Start with the A items of an <a href="{ABC}.html">ABC analysis</a>: they carry most of the value, so more frequent deliveries free the most cash for the fewest extra trucks.</li>
</ul>
<h2>The series in one table</h2>
<p class="oee-cap">Table 3. What each part found</p>
<table>
<tr><th>Part</th><th>Question</th><th>Finding in the example</th></tr>
<tr><td><a href="{WL1}.html">1</a></td><td>What does a bad layout cost?</td><td>Walking per order fell from 233 to 70&nbsp;m; picker-hours from 32.9 to 17.7 a day.</td></tr>
<tr><td><a href="{WL2}.html">2</a></td><td>U-shape, straight-through or L-shape?</td><td>Laid out well, all three pick at about the same cost; where receiving sits next to the fast movers matters more.</td></tr>
<tr><td><a href="{WL3}.html">3</a></td><td>Wide, narrow or very narrow aisles?</td><td>Narrower aisles fit 720 to 1,440 more positions and pay back against leasing, but only if the positions are needed.</td></tr>
<tr><td><a href="{WL4}.html">4</a></td><td>How should materials reach a line?</td><td>Calling before a material runs out, with a second load at the line, removed the waiting; the supermarket and milk run cut the handling.</td></tr>
<tr><td>5</td><td>What is it worth in cash?</td><td>Mostly labour and space; inventory turns rise only when the dock is used to buy smaller and dead stock is cleared.</td></tr>
</table>
<h2>Key points</h2>
<ul>
<li>A layout frees cash mainly through labour, truck detention, overtime and space. In the distributor example it paid back in {f1(ll["payback"])} to {f1(lh["payback"])} months on running costs alone.</li>
<li>Inventory turns rise only when the business uses the layout: smaller, more frequent deliveries that the redesigned dock can now take, and dead stock cleared during the move.</li>
<li>More frequent deliveries free cash once, but pay every year only when each extra delivery costs less than the carrying cost it saves: here, about ${dl["breakEven"]:.0f} a delivery.</li>
<li>Count labour as cash only when hours are actually cut or replace paid work.</li>
</ul>
<p>The whole series: <a href="{WL1}.html">Part&nbsp;1</a>, what a bad layout costs; <a href="{WL2}.html">Part&nbsp;2</a>, flow patterns; <a href="{WL3}.html">Part&nbsp;3</a>, aisle widths; <a href="{WL4}.html">Part&nbsp;4</a>, feeding the production line. The <a href="{SIM}">Layout Lab</a> runs all of them.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://www.bdc.ca/en/articles-tools/entrepreneur-toolkit/financial-tools/inventory-turnover-benchmarking-tool" rel="noopener" target="_blank">BDC: Inventory turnover ratio</a> (turns as cost of goods sold over average inventory, and days of stock)</li>
<li><a href="https://www.netsuite.com/portal/resource/articles/inventory-management/inventory-carrying-costs.shtml" rel="noopener" target="_blank">NetSuite: Inventory carrying costs</a> (carrying costs often 20% to 30% of inventory value)</li>
<li><a href="https://www.cleverence.com/articles/for-business/what-is-cycle-stock-inventory-5829/" rel="noopener" target="_blank">Cleverence: What is cycle stock?</a> (average cycle stock is half the order quantity)</li>
<li><a href="https://www.taylorfrancis.com/chapters/mono/10.4324/9781315231532-11/delivery-quantities-tony-wild" rel="noopener" target="_blank">Tony Wild: Delivery quantities</a> (more frequent deliveries can raise transport costs)</li>
</ul>
{NOTE}{mathjs()}
<script src="../assets/js/wl5.js" defer></script>"""
    body = nowrap(body, [(1, 0, 26), (2, 0, 30)])
    return dict(slug=WL5, title="From Layout to Cash: Inventory Turns and a Layout Payback Calculator",
                desc="What a better warehouse layout is worth in cash: labour, space and inventory turns, with a payback calculator built on Parts 1 to 4.",
                cats=["operational-efficiency", "inventory-management"], tags=["warehouse layout", "inventory turns", "payback", "cash flow", "carrying cost", "cycle stock"],
                body=body, date=DATE, author="Quak Foo Lee", read="10 min read", series=SER(5), cover_label="Warehouse layout",
                related=[WL1, WL4, SS])


if __name__ == "__main__":
    a = part5()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])}\n")
