"""Quote-to-cash series for Insights (Operational Efficiency): three articles.
Part 1 the process, Part 2 the 3D simulation (embeds assets/sim/q2c-factory.html), Part 3 what to fix first.

Usage:  python3 content/articles/q2c_articles.py
Writes content/articles/<slug>.json. Then run
        python3 content/gen/add_article.py <slug>
        python3 content/gen/series_labels.py
(see README, "Adding a new article").

The numbers are the baseline of the simulation model used in Part 2 (Quote-to-Cash Factory Simulator,
default settings, seed 7, one simulated year). If the model's defaults change, update DAYS and RESULTS and
the figures quoted in the text. Script for Parts 2 and 3: assets/js/q2c.js.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import feed_articles as F

NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE = F.NAVY, F.BLUE, F.GREEN, F.GREEND, F.ORANGE, F.PURPLE
MUTED, LINE, PALE, GREENF, ORANGEF = F.MUTED, F.LINE, F.PALE, F.GREENF, F.ORANGEF
GREY, GREYF, PURPLEF = "#8794A1", "#EEF0F3", "#E9E8FA"
svg, fig, txt = F.svg, F.fig, F.txt

S1 = "quote-to-cash-process-in-manufacturing"
S2 = "quote-to-cash-simulation-run-a-window-factory-in-3d"
S3 = "shorten-quote-to-cash-what-to-fix-first"
L1 = f'<a href="{S1}.html">Part&nbsp;1</a>'
L2 = f'<a href="{S2}.html">Part&nbsp;2</a>'
L3 = f'<a href="{S3}.html">Part&nbsp;3</a>'
SIM = "../assets/sim/q2c-factory.html"
JS = '<script src="../assets/js/q2c.js" defer></script>'
OEE = "what-oee-really-measures"
PLAN = "production-planning-and-scheduling-for-manufacturing"

# Baseline of the model: (stage, days, who controls it, money state)
DAYS = [("Writing the quote", 5.0, "Sales", "idle"),
        ("Customer decides", 2.9, "Customer", "idle"),
        ("Order entry and materials", 7.1, "Sales, purchasing, suppliers", "spent"),
        ("Production", 4.7, "Factory", "spent"),
        ("Delivery", 2.0, "Shipping", "spent"),
        ("Waiting to invoice", 5.0, "Finance", "spent"),
        ("Waiting to be paid", 39.6, "Customer, finance", "billed")]
TOTAL = round(sum(d[1] for d in DAYS), 1)                      # 66.3
STATE = {"idle": ("Nothing spent yet", GREY, GREYF), "spent": ("Cash spent, not billed", ORANGE, ORANGEF),
         "billed": ("Billed, not paid", PURPLE, PURPLEF), "paid": ("Paid", GREEND, GREENF)}
NOTE = ('<p class="oee-note"><em>Example Windows Co. and its figures are an illustrative example. The days and dollars come from a '
        'simulation model with round-number inputs, and they do not describe any real company.</em></p>')


AH = 9          # arrowhead length


def head(x, y, d="down", col=NAVY):
    """Arrowhead with its tip at (x, y). The connector must end at the midpoint of the flat base, AH units back."""
    if d == "down": pts = f"{x - 5},{y - AH} {x + 5},{y - AH} {x},{y}"
    elif d == "left": pts = f"{x + AH},{y - 5} {x + AH},{y + 5} {x},{y}"
    else: pts = f"{x - AH},{y - 5} {x - AH},{y + 5} {x},{y}"
    return f'<polygon points="{pts}" fill="{col}"/>'


def fig_swimlane(standalone=False):
    lanes = [["Customer"], ["Sales"], ["Planning and", "purchasing"], ["Production"], ["Shipping"], ["Finance"]]
    G, LW, HH, PITCH, BW, BH, Y0 = 64, 116, 44, 66, 106, 36, 58
    steps = [(0, "Asks for a quote", "idle", "Day 0"), (1, "1. Prepare quote", "idle", "Day 5"), (0, "Accepts quote", "idle", "Day 8"),
             (1, "2. Enter order", "idle", ""), (2, "3. Schedule job", "idle", ""), (2, "4. Buy materials", "spent", "Day 15"),
             (3, "5. Build", "spent", ""), (3, "6. Inspect, pack", "spent", "Day 20"), (4, "7. Deliver", "spent", "Day 22"),
             (5, "8. Send invoice", "billed", "Day 27"), (0, "Pays invoice", "billed", "Day 66"), (5, "Record cash", "paid", "")]
    waits = {1, 9}                                               # arrows leaving these rows wait on the customer
    W = G + LW * len(lanes); H = Y0 + PITCH * len(steps) + 30
    s = f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>' if standalone else ""
    for i, nm in enumerate(lanes):
        x = G + i * LW
        s += f'<rect x="{x}" y="0" width="{LW}" height="{H - 34}" fill="{"#F7F9FB" if i % 2 == 0 else "#fff"}" stroke="{LINE}"/>'
        s += f'<rect x="{x}" y="0" width="{LW}" height="{HH}" fill="{PALE}" stroke="#9AB0C8"/>'
        for j, ln in enumerate(nm):
            s += txt(x + LW / 2, HH / 2 + 4.5 + (j - (len(nm) - 1) / 2) * 15, ln, "middle", NAVY, 13, True)
    s += txt(G - 10, HH / 2 + 4.5, "Done by", "end", MUTED, 12, True)
    s += f'<line x1="{G - 6}" y1="{HH}" x2="{G - 6}" y2="{H - 34}" stroke="{LINE}"/>'
    cx = lambda r: G + steps[r][0] * LW + LW / 2
    top = lambda r: Y0 + r * PITCH
    for r, (ln, label, st, day) in enumerate(steps):
        _, stroke, fill = STATE[st]
        s += f'<rect x="{cx(r) - BW / 2}" y="{top(r)}" width="{BW}" height="{BH}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>'
        s += txt(cx(r), top(r) + BH / 2 + 4.3, label, "middle", NAVY, 12, label[0].isdigit())
        if day:
            s += txt(G - 10, top(r) + BH / 2 + 4.3, day, "end", MUTED, 12)
            s += f'<line x1="{G - 6}" y1="{top(r) + BH / 2}" x2="{G - 1}" y2="{top(r) + BH / 2}" stroke="{MUTED}"/>'
    for r in range(len(steps) - 1):
        x1, x2, y1, y2 = cx(r), cx(r + 1), top(r) + BH, top(r + 1)
        # Elbow with rounded corners. The last straight run into the arrowhead is always solid and ends at the
        # midpoint of the head's flat base, so a dashed connector never leaves a gap or meets the head off-centre.
        dash = ' stroke-dasharray="5 4"' if r in waits else ""
        st = f'fill="none" stroke="{NAVY}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
        if x1 == x2:
            s += f'<path d="M{x1},{y1} V{y2 - AH}" {st}/>'
        else:
            ym, rr, sg = y1 + 9, 6, (1 if x2 > x1 else -1)
            s += (f'<path d="M{x1},{y1} V{ym - rr} Q{x1},{ym} {x1 + sg * rr},{ym} H{x2 - sg * rr} Q{x2},{ym} {x2},{ym + rr}" {st}{dash}/>'
                  f'<path d="M{x2},{ym + rr} V{y2 - AH}" {st}/>')
        s += head(x2, y2)
    ly = H - 12; lx = G
    for key in ("idle", "spent", "billed", "paid"):
        name, stroke, fill = STATE[key]
        s += f'<rect x="{lx}" y="{ly - 11}" width="14" height="14" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>' + txt(lx + 20, ly, name, "start", MUTED, 12)
        lx += 32 + len(name) * 6.2
    s += f'<path d="M{lx},{ly - 4} H{lx + 14}" stroke="{NAVY}" stroke-width="1.6" stroke-dasharray="5 4"/><path d="M{lx + 16},{ly - 4} H{lx + 22}" stroke="{NAVY}" stroke-width="1.6"/>' + head(lx + 31, ly - 4, "right") + txt(lx + 38, ly, "Waiting on the customer", "start", MUTED, 12)
    return svg("Swim lane diagram of the quote-to-cash process with six lanes: customer, sales, planning and purchasing, production, shipping and finance. "
               "Twelve steps run from the customer asking for a quote on day 0 to the payment being recorded on day 66.", W, H, s, 640)


def fig_days():
    W, LBL, R, ROW, T = 760, 186, 58, 28, 8
    px = lambda d: LBL + (W - LBL - R) * d / TOTAL
    H = T + ROW * len(DAYS) + 78
    s = ""; start = 0; base = T + ROW * len(DAYS) + 6
    for d in (0, 10, 20, 30, 40, 50, 60):
        s += f'<line x1="{px(d):.1f}" y1="{T}" x2="{px(d):.1f}" y2="{base}" stroke="{LINE}"/>' + txt(px(d), base + 16, str(d), "middle", MUTED, 12)
    s += txt(px(TOTAL / 2), base + 34, "Days since the customer asked for a quote", "middle", MUTED, 12.5)
    tot = {}
    for i, (name, d, _, st) in enumerate(DAYS):
        _, stroke, fill = STATE[st]; y = T + i * ROW + 4
        s += txt(LBL - 10, y + 15, name, "end", NAVY, 12.5)
        s += f'<rect x="{px(start):.1f}" y="{y}" width="{px(start + d) - px(start):.1f}" height="20" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>'
        s += txt(px(start + d) + 7, y + 15, f"{d:.1f}", "start", NAVY, 12.5, True)
        start += d; tot[st] = tot.get(st, 0) + d
    lx = 4; ly = H - 6
    for st, d in tot.items():
        name, stroke, fill = STATE[st]; label = f"{name}: {d:.0f} days"
        s += f'<rect x="{lx}" y="{ly - 11}" width="14" height="14" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>' + txt(lx + 20, ly, label, "start", MUTED, 12)
        lx += 40 + len(label) * 6.3
    return svg(f"Cascade chart of the {TOTAL} days of an average order. Writing the quote and the customer's decision take 8 days with nothing spent. "
               "Order entry, materials, production, delivery and the wait to invoice take 19 days with cash spent. Waiting to be paid takes 40 days.", W, H, s, 600)


def fig_cash():
    W, H, L, R, T, B = 760, 320, 76, 20, 18, 44
    px = lambda d: L + (W - L - R) * d / 70
    py = lambda v: T + (H - T - B) * (10000 - v) / 27500
    s = ""
    for v in (8000, 0, -8000, -12000):
        s += f'<line x1="{L}" y1="{py(v):.1f}" x2="{W - R}" y2="{py(v):.1f}" stroke="{NAVY if v == 0 else LINE}" stroke-width="{1.3 if v == 0 else 1}"/>'
        s += txt(L - 8, py(v) + 4, ("+" if v > 0 else "−" if v < 0 else "") + f"${abs(v):,}", "end", MUTED, 12)
    for d in (0, 10, 20, 30, 40, 50, 60):
        s += f'<line x1="{px(d):.1f}" y1="{H - B}" x2="{px(d):.1f}" y2="{H - B + 5}" stroke="{MUTED}"/>' + txt(px(d), H - B + 19, str(d), "middle", MUTED, 12)
    s += txt((L + W - R) / 2, H - 6, "Days since the customer asked for a quote", "middle", MUTED, 12.5)
    pts = [(0, 0), (8, 0), (8, -8000), (15, -8000), (20, -12000), (66, -12000), (66, 8000), (70, 8000)]
    s += (f'<path d="M{px(8):.1f},{py(0):.1f} L{px(8):.1f},{py(-8000):.1f} L{px(15):.1f},{py(-8000):.1f} L{px(20):.1f},{py(-12000):.1f} '
          f'L{px(66):.1f},{py(-12000):.1f} L{px(66):.1f},{py(0):.1f} z" fill="{ORANGEF}"/>')
    s += f'<path d="M{px(66):.1f},{py(0):.1f} L{px(66):.1f},{py(8000):.1f} L{px(70):.1f},{py(8000):.1f} L{px(70):.1f},{py(0):.1f} z" fill="{GREENF}"/>'
    s += '<path d="' + " ".join(("M" if i == 0 else "L") + f"{px(d):.1f},{py(v):.1f}" for i, (d, v) in enumerate(pts)) + f'" fill="none" stroke="{NAVY}" stroke-width="2.2" stroke-linejoin="round"/>'
    s += txt(px(8) + 8, py(-4000) + 4, "Materials bought: −$8,000", "start", ORANGE, 12.5, True)
    s += txt(px(20) + 8, py(-10300), "Labour added: −$4,000", "start", ORANGE, 12.5, True)
    s += txt(px(43), py(-6000) + 4, "58 days out of pocket", "middle", NAVY, 13, True)
    s += txt(px(66) - 8, py(4000) + 4, "Customer pays: +$20,000", "end", GREEND, 12.5, True)
    for d, lab in ((22, "Delivered"), (27, "Invoiced")):
        s += f'<line x1="{px(d):.1f}" y1="{py(-12000) - 5:.1f}" x2="{px(d):.1f}" y2="{py(-12000) + 5:.1f}" stroke="{NAVY}" stroke-width="1.5"/>'
    s += txt(px(22) - 3, py(-12000) + 19, "Delivered", "end", MUTED, 12) + txt(px(27) + 3, py(-12000) + 19, "Invoiced", "start", MUTED, 12)
    return svg("Line chart of the cash position of one $20,000 order. It is zero until day 8, falls to minus $8,000 when materials are bought, "
               "falls to minus $12,000 by day 20 as labour is added, stays there until the customer pays on day 66, then rises to plus $8,000.", W, H, s, 600)


def post1():
    rows = "".join(f'<tr><td class="nw">{n}</td><td class="num">{d:.1f}</td><td>{who}</td><td>{STATE[st][0]}</td></tr>' for n, d, who, st in DAYS)
    office = DAYS[0][1] + DAYS[5][1] + 10
    return f"""{F.CSS}<p>The order was quoted, won, built and delivered. The money arrives two months later. Quote to cash is the name for that whole path, and most of it runs through the office, not the factory.</p>
<p>This series follows one example: Example Windows Co., a made-up 40-person window maker with sales of about $12 million a year. This post maps the process and shows where the days and the cash sit. {L2} lets you run the factory in a live 3D simulation. {L3} covers what to fix first and the payback.</p>
<h2>What quote to cash means</h2>
<p>Quote to cash (Q2C) covers every step from a customer's request for a price to the payment reaching the bank. Order to cash (O2C) is the same path without the quoting step. A made-to-order manufacturer should include the quote, because every job starts with one and nothing else can start until the customer accepts it.</p>
<p>Two numbers describe the process:</p>
<ul>
<li><strong>Quote-to-cash days.</strong> The time from the customer's request to the payment.</li>
<li><strong>Cash tied up.</strong> The money already paid out for materials and labour on orders that customers have not yet paid for.</li>
</ul>
<h2>The eight stages</h2>
<p>Six groups handle an order: the customer, sales, planning and purchasing, production, shipping and finance. Figure 1 shows who does each step and when it is finished in the example.</p>
{fig(fig_swimlane(), 1, "The quote-to-cash process at Example Windows Co. The numbered boxes are the eight stages. The colour shows where the money is at each step.")}
<p>Every stage hands something to the next one. Days are lost at the handovers, where work waits in a queue or goes back for missing information.</p>
<p class="oee-cap">Table 1. The eight stages, who owns them and where days are lost</p>
<table>
<tr><th>Stage</th><th>Owner</th><th>What it hands over</th><th>Where the days are lost</th></tr>
<tr><td class="nw">1. Quote</td><td>Sales</td><td>A price, a specification and a delivery date</td><td>Requests queue behind one estimator. Prices are worked out by hand.</td></tr>
<tr><td class="nw">2. Order</td><td>Sales</td><td>A confirmed order that matches the quote</td><td>Details are typed again from the quote. Sizes or colours are missing.</td></tr>
<tr><td class="nw">3. Schedule</td><td>Planning</td><td>A production slot and a promised date</td><td>The date is promised before capacity is checked.</td></tr>
<tr><td class="nw">4. Procure</td><td>Purchasing</td><td>Glass, profiles and hardware for the job</td><td>Materials are ordered late. Supplier lead times vary.</td></tr>
<tr><td class="nw">5. Produce</td><td>Production</td><td>Finished windows</td><td>Orders wait for a full batch. Changeovers and machine stoppages.</td></tr>
<tr><td class="nw">6. Inspect</td><td>Production</td><td>Packed windows that meet the specification</td><td>Defects are found at the end of the line and reworked.</td></tr>
<tr><td class="nw">7. Ship</td><td>Shipping</td><td>Delivery to the site, with proof of delivery</td><td>Part loads wait for a full truck. The signed slip goes missing.</td></tr>
<tr><td class="nw">8. Invoice and collect</td><td>Finance</td><td>An invoice, then the payment</td><td>Invoices are raised in a weekly batch. Nobody follows up overdue accounts.</td></tr>
</table>
<h2>Where the days go</h2>
<p>In the example, an average order takes {TOTAL:.0f} days from request to payment. The figures come from the simulation model in {L2}, run for one year at its starting settings.</p>
<p class="oee-cap">Table 2. Average days in each stage of the example</p>
<table>
<tr><th>Stage</th><th class="num">Days</th><th>Who controls it</th><th>Where the money is</th></tr>
{rows}
<tr class="oee-total"><td>Total</td><td class="num">{TOTAL:.1f}</td><td></td><td></td></tr>
</table>
{fig(fig_days(), 2, f"The {TOTAL:.0f} days of an average order, stage by stage. Production is the fourth bar.")}
<p>Three points stand out.</p>
<ul>
<li><strong>Production is about 7% of the time.</strong> The windows spend under 5 days in the factory, and that includes waiting for a batch. A faster line would barely change the total. For what happens inside those days, see <a href="{OEE}.html">What OEE Really Measures</a>.</li>
<li><strong>Office waits take four times as long as production.</strong> Writing the quote takes 5 days, sending the invoice takes another 5, and customers pay about 10 days late. Those {office:.0f} days need no new equipment to fix.</li>
<li><strong>Waiting to be paid is 60% of the total.</strong> The terms are 30 days, and the average customer takes about 40. The clock starts when the invoice goes out, so every day of invoicing delay is added on top.</li>
</ul>
<h2>Where the cash sits</h2>
<p>An average order is 20 windows for $20,000. The company pays $8,000 for materials when the order is confirmed and adds $4,000 of labour on the line. The remaining $8,000 covers overhead and profit. Figure 3 follows the cash for one order.</p>
{fig(fig_cash(), 3, "Cash position of one order. The company pays out on day 8 and is paid on day 66.")}
<p>The company is out of pocket on each order for 58 days. It takes about 1.6 orders a day, so about 96 orders are open with money spent on them at any time. Together they tie up about $1.06 million. The owner funds that amount from a credit line or from retained profit.</p>
<p>The same arithmetic gives a useful rule for this example. After an order is built it carries $12,000 of cost, and 1.6 orders a day reach that point. Each day removed between delivery and payment therefore frees about $19,000 of cash. Invoicing on the day of delivery, 5 days sooner, frees close to $100,000.</p>
<h2>Five measures to track</h2>
<p>Most accounting and ERP systems already hold the dates needed for these measures. If yours does not, a spreadsheet with one row per order and six dates is enough to start.</p>
<p class="oee-cap">Table 3. Quote-to-cash measures and their values in the example</p>
<table>
<tr><th>Measure</th><th>How to calculate it</th><th class="num">Example</th></tr>
<tr><td class="nw">Quote turnaround</td><td>Days from the request to the quote being sent</td><td class="num">5 days</td></tr>
<tr><td class="nw">Order lead time</td><td>Days from the confirmed order to delivery</td><td class="num">14 days</td></tr>
<tr><td class="nw">On-time delivery</td><td>Orders delivered by the promised date ÷ orders delivered</td><td class="num">80%</td></tr>
<tr><td class="nw">Invoice lag</td><td>Days from delivery to the invoice being sent</td><td class="num">5 days</td></tr>
<tr><td class="nw">Days sales outstanding (DSO)</td><td>Unpaid invoices ÷ sales per day. Here $1.28 million ÷ $32,000.</td><td class="num">40 days</td></tr>
</table>
<p>The promised date in the example is 15 days after the order. One order in five misses it, mostly because materials arrive late or the order waits for a batch. <a href="{PLAN}.html">Production Planning and Scheduling for Manufacturing</a> covers how to set dates the plant can keep.</p>
<h2>Three common mistakes</h2>
<ul>
<li><strong>Measuring only the factory.</strong> Output and scrap are tracked daily, while nobody knows how long a quote or an invoice takes.</li>
<li><strong>Treating the invoice as paperwork.</strong> The invoice starts the customer's payment clock. A weekly invoicing run adds several days to every order.</li>
<li><strong>Looking at each department alone.</strong> Each group meets its own target, and the order still waits at every handover. One person should own the total number of days.</li>
</ul>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> Map the eight stages, put a date on each handover and add up the days. In the example an order takes {TOTAL:.0f} days to become cash, the factory accounts for about 5 of them, and about $1.06 million is tied up in open orders.</p></div>
<div class="oee-next"><a class="oee-fwd" href="{S2}.html">Next: Part&nbsp;2, run the factory in 3D →</a></div>
{NOTE}"""


# ───────────────────────── Results of the model, one change at a time ─────────────────────────
# (key, name, change, quote-to-cash days, cash tied up $, on-time %)   seed 7, one simulated year
BASE = (66.3, 1061296, 80)
RESULTS = [("invoice", "Invoice on delivery day", "Invoice lag 5 → 0 days", 61.1, 965696, 80),
           ("late", "Follow up overdue invoices", "Late payment 10 → 3 days", 59.5, 938096, 80),
           ("deposit", "Take a 30% deposit", "Deposit 0 → 30%", 66.3, 496962, 80),
           ("quote", "Quote in one day", "Quote turnaround 5 → 1 day", 62.1, 1062472, 83),
           ("batch", "Halve the batch size", "Batch 4 → 2 orders", 65.3, 1049116, 97),
           ("uptime", "Raise machine uptime", "Uptime 90 → 95%", 65.7, 1053485, 90)]
TROUBLE = (69.0, 1098415, 15)          # machine uptime 75%
OFFICE = (50.5, 386406, 83)            # quote 1 day, invoice lag 0, late 3 days, deposit 30%
ALL = (49.0, 380204, 100)              # office package plus batch 2 and uptime 95%
k = lambda v: f"${round(v / 1000) * 1000:,.0f}"
freed = lambda v: BASE[1] - v


def harrow(x1, y, x2, col=NAVY):
    """Horizontal arrow; the line stops at the midpoint of the head's flat base."""
    d = "right" if x2 > x1 else "left"; end = x2 - AH if x2 > x1 else x2 + AH
    return f'<path d="M{x1},{y} H{end}" fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round"/>' + head(x2, y, d, col)


def elbow(x1, y1, x2, y2, col=NAVY):
    """Down, across, down, with rounded corners and a straight run into the head."""
    ym, rr, sg = (y1 + y2 - AH) / 2, 6, (1 if x2 > x1 else -1)
    return (f'<path d="M{x1},{y1} V{ym - rr} Q{x1},{ym} {x1 + sg * rr},{ym} H{x2 - sg * rr} Q{x2},{ym} {x2},{ym + rr} V{y2 - AH}" '
            f'fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>') + head(x2, y2, "down", col)


def fig_floor():
    def b(x, y, w, label, st, h=40, bold=False):
        stroke, fill = (NAVY, "#fff") if st == "machine" else STATE[st][1:]
        lines = label if isinstance(label, list) else [label]
        t = "".join(txt(x + w / 2, y + h / 2 + 4.3 + (i - (len(lines) - 1) / 2) * 14, ln, "middle", NAVY, 12, bold) for i, ln in enumerate(lines))
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>' + t
    YA, YB, YC = 30, 132, 234
    s = txt(748, YA - 12, "Quote requests", "end", MUTED, 12)
    s += b(520, YA, 170, "Quote desk", "idle") + b(290, YA, 170, "Customer decides", "idle") + b(40, YA, 190, "Order entry and materials", "spent")
    s += harrow(750, YA + 20, 690) + harrow(520, YA + 20, 460) + harrow(290, YA + 20, 230)
    s += b(4, YB, 112, ["Waiting for", "a full batch"], "spent")
    xs = [142, 244, 346, 448, 550]
    for x, nm in zip(xs, ["Cut", "Weld", "Hardware", "Glaze", ["Inspect,", "pack"]]):
        s += b(x, YB, 80, nm, "machine", bold=True)
    s += b(652, YB, 104, ["Out for", "delivery"], "spent")
    s += harrow(116, YB + 20, 142)
    for x in xs[:-1]: s += harrow(x + 80, YB + 20, x + 102)
    s += harrow(630, YB + 20, 652)
    s += f'<path d="M142,{YB - 10} v-6 h488 v6" fill="none" stroke="{MUTED}" stroke-width="1.3"/>' + txt(386, YB - 22, "The line: five machines", "middle", MUTED, 12)
    s += elbow(135, YA + 40, 60, YB)
    s += b(520, YC, 190, "Delivered, not invoiced", "spent") + b(270, YC, 190, "Invoiced, not paid", "billed") + b(100, YC, 110, "Bank", "paid")
    s += elbow(704, YB + 40, 615, YC) + harrow(520, YC + 20, 460) + harrow(270, YC + 20, 210)
    ly = YC + 68; lx = 4
    for key in ("idle", "spent", "billed", "paid"):
        name, stroke, fill = STATE[key]
        s += f'<rect x="{lx}" y="{ly - 11}" width="14" height="14" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>' + txt(lx + 20, ly, name, "start", MUTED, 12)
        lx += 34 + len(name) * 6.3
    return svg("Map of the simulated factory floor. Quote requests flow from the quote desk to the customer's decision and to order entry and materials. "
               "Orders then wait for a full batch, pass through five machines and go out for delivery. "
               "Delivered orders wait to be invoiced, then wait to be paid, then reach the bank.", 760, ly + 10, s, 640)


def fig_fixes():
    W, LBL, ROW, T = 760, 190, 30, 30
    x1, w1, x2, w2 = LBL, 200, LBL + 290, 210
    s = txt(x1, 16, "Days saved", "start", NAVY, 12.5, True) + txt(x2, 16, "Cash freed", "start", NAVY, 12.5, True)
    for i, (_, name, _, days, cash, _) in enumerate(RESULTS):
        y = T + i * ROW; ds = BASE[0] - days; cf = freed(cash)
        s += txt(LBL - 10, y + 17, name, "end", NAVY, 12.5)
        s += f'<rect x="{x1}" y="{y + 3}" width="{max(1.5, w1 * ds / 7.5):.1f}" height="20" rx="3" fill="{PALE}" stroke="{BLUE}" stroke-width="1.3"/>'
        s += txt(x1 + max(1.5, w1 * ds / 7.5) + 7, y + 17, f"{ds:.1f}" if ds >= 0.05 else "0", "start", NAVY, 12.5, True)
        s += f'<rect x="{x2}" y="{y + 3}" width="{max(1.5, w2 * max(cf, 0) / 600000):.1f}" height="20" rx="3" fill="{GREENF}" stroke="{GREEND}" stroke-width="1.3"/>'
        s += txt(x2 + max(1.5, w2 * max(cf, 0) / 600000) + 7, y + 17, k(cf) if cf > 500 else "None", "start", NAVY, 12.5, True)
    H = T + ROW * len(RESULTS) + 6
    s += f'<line x1="{x1}" y1="{T}" x2="{x1}" y2="{H - 4}" stroke="{MUTED}"/><line x1="{x2}" y1="{T}" x2="{x2}" y2="{H - 4}" stroke="{MUTED}"/>'
    return svg("Two bar charts side by side for six fixes. Days saved: follow-up of overdue invoices 6.8, invoicing on delivery day 5.2, quoting in one day 4.2, "
               "halving the batch 1.0, raising uptime 0.6 and the deposit 0. Cash freed: the deposit frees the most, about $564,000, "
               "then overdue follow-up $123,000 and invoicing $96,000.", W, H, s, 620)


def post2():
    rows = "".join(f'<tr><td class="nw">{n}</td><td class="num">{d:.0f} days</td><td class="num">{k(c)}</td><td class="num">{o}%</td></tr>'
                   for n, (d, c, o) in [("Baseline", BASE), ("Invoice on delivery day", RESULTS[0][3:]), ("Halve the batch size", RESULTS[4][3:]),
                                        ("Machine trouble", TROUBLE), ("Fix the office", OFFICE)])
    return f"""{F.CSS}<p>{L1} mapped the quote-to-cash process at Example Windows Co., a made-up window maker. An order takes 66 days to become cash, and about $1.06 million sits in open orders. This post lets you test changes to that process before you spend money on them.</p>
<p>The model below is a working simulation. Orders arrive, wait, pass through five machines and get paid. The results change when you change the settings.</p>
<h2>The simulator</h2>
<p>Every tile or window frame is one customer order worth $20,000. Its colour shows where the money is. Start with the buttons in the Try row, then move the sliders.</p>
<figure>
<iframe id="q2c-sim" src="{SIM}#embed" title="Quote-to-cash factory simulator" loading="lazy" style="width:100%;height:1750px;border:0;display:block"></iframe>
<figcaption>Figure 1. The quote-to-cash simulator. Drag to rotate, click a machine for its numbers, and use 4x or 16x to speed up time. On a phone, tap Move view first.</figcaption>
</figure>
<p class="oee-hint"><a href="{SIM}">Open the simulator on its own page</a> for a larger view.</p>
<h2>How to read the floor</h2>
<p>The floor follows the order of the process. Work starts at the back right, runs through the line in the middle and ends at the bank at the front left.</p>
{fig(fig_floor(), 2, "Map of the simulated floor. The colours match the simulator.")}
<p class="oee-cap">Table 1. What the colours mean</p>
<table>
<tr><th>Colour</th><th>Where the money is</th><th>Where you see it</th></tr>
<tr><td class="nw">Grey</td><td>Quoted, nothing spent</td><td>Quote desk and the customer's decision</td></tr>
<tr><td class="nw">Orange</td><td>Cash spent, not billed</td><td>Materials, the line, delivery and delivered orders waiting for an invoice</td></tr>
<tr><td class="nw">Purple</td><td>Billed, not paid</td><td>The block of unpaid invoices</td></tr>
<tr><td class="nw">Green</td><td>Paid</td><td>Tiles moving to the bank</td></tr>
</table>
<p>The purple block is the largest group on the floor. At the starting settings it holds about 64 orders, or $1.28 million of unpaid invoices.</p>
<p>Each machine has a light: green when it is running, yellow when it is waiting, blue during a changeover and red when it has stopped for repair.</p>
<h2>Three experiments</h2>
<h3>1. Invoice on delivery day</h3>
<p>Click <strong>Invoice on delivery day</strong>. The pad of delivered orders waiting for an invoice empties. Quote to cash falls from 66 to 61 days and about $96,000 of cash is freed. No machine changed.</p>
<h3>2. Halve the batch size</h3>
<p>Click <strong>Halve the batch size</strong>. Orders stop waiting for a batch of four, so they reach the line sooner. Deliveries on time rise from 80% to 97%. Quote to cash moves by one day and the cash tied up barely changes.</p>
<h3>3. Machine trouble</h3>
<p>Click <strong>Machine trouble</strong>. Uptime drops from 90% to 75% and window frames queue in front of the first machine. Only 15% of orders now arrive on time. Quote to cash rises by just 3 days.</p>
<p class="oee-cap">Table 2. Results of the experiments</p>
<table>
<tr><th>Setting</th><th class="num">Quote to cash</th><th class="num">Cash tied up</th><th class="num">Delivered on time</th></tr>
{rows}
</table>
<p>The pattern is consistent. The factory decides whether the customer gets the order on time. The office decides how long the money takes. <strong>Fix the office</strong> combines a one-day quote, same-day invoicing, follow-up of late payers and a 30% deposit, and it frees about $675,000 without touching a machine.</p>
<h2>What the model assumes</h2>
<p class="oee-cap">Table 3. Inputs of the model</p>
<table>
<tr><th>Item</th><th>Value in the model</th></tr>
<tr><td class="nw">Orders</td><td>About 1.6 a day, each 20 windows worth $20,000</td></tr>
<tr><td class="nw">Costs</td><td>$8,000 of materials bought when the order is confirmed, $4,000 of labour added on the line</td></tr>
<tr><td class="nw">Customer's decision</td><td>About 3 days after the quote is sent</td></tr>
<tr><td class="nw">Order entry and materials</td><td>About 7 days, varying from 5 to 9 with the supplier</td></tr>
<tr><td class="nw">The line</td><td>Five machines, 0.4 of a day per order each, with room for two orders between machines</td></tr>
<tr><td class="nw">Stoppages</td><td>Random, about 2 hours to repair</td></tr>
<tr><td class="nw">Batches</td><td>Orders wait for a full batch. The first machine has one changeover per batch.</td></tr>
<tr><td class="nw">Delivery</td><td>2 days, promised within 15 days of the order</td></tr>
<tr><td class="nw">Payment</td><td>30-day terms, paid about 10 days late on average</td></tr>
</table>
<p>The model has limits. It shows won orders only, so it cannot tell you how many more quotes a faster answer would win. It ignores weekends and bad debts. Each change restarts the model and runs one year in the background, so the results are settled averages. They come from a random simulation and move a little from run to run.</p>
<h2>Use your own numbers</h2>
<p>Set the office sliders to your own quote turnaround, invoice lag, payment terms, late days and deposit. The order value and costs stay those of the example. Read the direction and the relative size of each change, not the exact dollars.</p>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> Test a change in the model before paying for it. In this example the office settings move the cash, and the factory settings move the delivery promise.</p></div>
<div class="oee-next"><a href="{S1}.html">← Part&nbsp;1, the process</a><a class="oee-fwd" href="{S3}.html">Next: Part&nbsp;3, what to fix first →</a></div>
{NOTE}{JS}"""


def post3():
    rows = f'<tr><td class="nw">Starting point</td><td></td><td class="num">{BASE[0]:.1f}</td><td class="num">{k(BASE[1])}</td><td class="num"></td><td class="num">{BASE[2]}%</td></tr>'
    for _, name, change, days, cash, ot in RESULTS:
        cf = freed(cash)
        rows += (f'<tr><td class="nw">{name}</td><td>{change}</td><td class="num">{days:.1f}</td><td class="num">{k(cash)}</td>'
                 f'<td class="num">{k(cf) if cf > 500 else "None"}</td><td class="num">{ot}%</td></tr>')
    off_freed = freed(OFFICE[1]); rate, cost = 7, 60000
    yearly = round(off_freed / 1000) * 1000 * rate / 100; months = cost / yearly * 12
    return f"""{F.CSS}<p>{L1} showed that an order at Example Windows Co. takes 66 days to become cash and that about $1.06 million sits in open orders. {L2} gave you the model. This post uses it to decide what to fix first.</p>
<h2>Six fixes, tested one at a time</h2>
<p>Each fix was run in the simulator on its own for one simulated year. Everything else stayed at the starting settings.</p>
<p class="oee-cap">Table 1. Effect of each fix on its own. Days are quote-to-cash days.</p>
<table>
<tr><th>Fix</th><th>Change</th><th class="num">Days</th><th class="num">Cash tied up</th><th class="num">Cash freed</th><th class="num">On time</th></tr>
{rows}
</table>
{fig(fig_fixes(), 1, "Days saved and cash freed by each fix on its own.")}
<h2>What the results say</h2>
<ul>
<li><strong>Three fixes free cash, and all three are in the office.</strong> The deposit frees the most, about {k(freed(RESULTS[2][4]))}. Following up overdue invoices frees about {k(freed(RESULTS[1][4]))} and invoicing on delivery day about {k(freed(RESULTS[0][4]))}.</li>
<li><strong>A faster quote saves days and frees no cash.</strong> Nothing has been spent on an order while it is being quoted. The value of a one-day quote is commercial. The model does not count orders won or lost, so it cannot show that gain.</li>
<li><strong>The factory fixes protect the delivery promise.</strong> Smaller batches lift on-time delivery from 80% to 97%, and better uptime lifts it to 90%. Neither moves much cash.</li>
</ul>
<p>On-time figures within about 3 points of each other are the same result, because the simulation is random.</p>
<h2>Rank the fixes by effort</h2>
<p>Start with the fixes that cost the least and need no agreement from customers.</p>
<p class="oee-cap">Table 2. Suggested order of work</p>
<table>
<tr><th>Order</th><th>Fix</th><th>Effort</th><th>What it takes</th><th>Owner</th></tr>
<tr><td class="num">1</td><td>Invoice on delivery day</td><td>Low</td><td>Raise the invoice from the delivery confirmation. Capture proof of delivery on a phone.</td><td>Finance</td></tr>
<tr><td class="num">2</td><td>Follow up overdue invoices</td><td>Low</td><td>Automatic reminders before and after the due date. One person owns the overdue list.</td><td>Finance</td></tr>
<tr><td class="num">3</td><td>Take a deposit</td><td>Medium</td><td>New terms on quotes, applied to new orders first. Sales needs to explain the change.</td><td>Sales and the owner</td></tr>
<tr><td class="num">4</td><td>Quote in one day</td><td>Medium</td><td>A price book and a product configurator, so a quote no longer waits for one estimator.</td><td>Sales</td></tr>
<tr><td class="num">5</td><td>Halve the batch size</td><td>Medium</td><td>Shorter changeovers and scheduling by due date.</td><td>Production</td></tr>
<tr><td class="num">6</td><td>Raise machine uptime</td><td>Higher</td><td>Planned maintenance and a log of every stoppage. See <a href="{OEE}.html">What OEE Really Measures</a>.</td><td>Production and maintenance</td></tr>
</table>
<h2>The office package</h2>
<p>Fixes 1 to 4 together take quote to cash from {BASE[0]:.0f} days to {OFFICE[0]:.0f}. Cash tied up falls from $1.06 million to about {k(OFFICE[1])}, which frees about {k(off_freed)}. Adding the two factory fixes brings the total to {ALL[0]:.0f} days, and every order in the simulated year arrives on time.</p>
<p>A deposit is the largest item and the hardest to win. Some customers will refuse it. Even a 10% deposit on new orders frees a useful share of the amount, and the simulator in {L2} lets you test any level.</p>
<h2>The payback</h2>
<p>Freed cash is a one-time release, not profit. Its yearly value is the cost of that money: the interest on a credit line, or what the cash could earn elsewhere in the business.</p>
<div class="oee-calc" role="group" aria-labelledby="q3h">
<h3 id="q3h">Try it: payback on the cash you free</h3>
<p class="oee-hint">The starting values are the office package in this example, with an assumed 7% cost of borrowing and an assumed project cost of $60,000.</p>
<div class="oee-sliders">
<div class="oee-sl"><label for="q3-cash">Cash freed <output id="q3-cash-o"></output></label><input type="range" id="q3-cash" min="50000" max="1000000" step="25000" value="{round(off_freed / 25000) * 25000}"></div>
<div class="oee-sl"><label for="q3-rate">Cost of borrowing <output id="q3-rate-o"></output></label><input type="range" id="q3-rate" min="3" max="12" step="0.5" value="{rate}"></div>
<div class="oee-sl"><label for="q3-cost">Project cost <output id="q3-cost-o"></output></label><input type="range" id="q3-cost" min="10000" max="200000" step="5000" value="{cost}"></div>
</div>
<div class="oee-tiles">
<div class="oee-tile"><span class="k">Interest saved a year</span><span class="v" id="q3-int"></span></div>
<div class="oee-tile key"><span class="k">Payback</span><span class="v" id="q3-pay"></span><span class="n">on interest alone</span></div>
<div class="oee-tile"><span class="k">Cash freed against cost</span><span class="v" id="q3-mult"></span></div>
</div>
</div>
<p>In the example, {k(off_freed)} at 7% is worth about ${yearly:,.0f} a year. A $60,000 project covering the invoicing change, reminders, a price book and a configurator pays back in about {months:.0f} months on interest alone. The cash released is about {off_freed / cost:.0f} times the project cost. Both the 7% and the $60,000 are assumptions. Use your own figures in the calculator.</p>
<p>Some of this work may qualify for government support. The <a href="../funding.html">funding finder</a> lists current programs.</p>
<h2>A 90-day plan</h2>
<p class="oee-cap">Table 3. What to do in the first 90 days</p>
<table>
<tr><th>Days</th><th>Work</th><th>Result to check</th></tr>
<tr><td class="nw">1 to 30</td><td>Record six dates for every order: request, quote, order, delivery, invoice and payment. Invoice on delivery day. Turn on payment reminders.</td><td>Invoice lag under 1 day</td></tr>
<tr><td class="nw">31 to 60</td><td>Put deposit terms on new quotes. Build the price book for the most common products.</td><td>Share of new orders with a deposit. Quote turnaround.</td></tr>
<tr><td class="nw">61 to 90</td><td>Try a smaller batch on one product family. Log every machine stoppage.</td><td>On-time delivery. Days sales outstanding.</td></tr>
</table>
<h2>What the model leaves out</h2>
<ul>
<li><strong>Orders won or lost.</strong> A faster quote and a deposit both change how many customers say yes.</li>
<li><strong>Bad debts.</strong> Every invoice in the model is paid in the end.</li>
<li><strong>Weekends and holidays.</strong> The model runs every day.</li>
<li><strong>Your own mix.</strong> The example has one product at one price. Real orders vary in size, margin and terms.</li>
</ul>
<div class="oee-takeaway"><p><strong>Takeaway.</strong> Fix the office first. In the example, four changes that need no new equipment cut quote to cash from {BASE[0]:.0f} days to {OFFICE[0]:.0f} and free about {k(off_freed)}. Then use smaller batches and better uptime to protect the delivery promise.</p></div>
<div class="oee-next oee-end"><a href="{S1}.html">← Part&nbsp;1, the process</a><a href="{S2}.html">← Part&nbsp;2, the 3D simulation</a></div>
{NOTE}{JS}"""


ARTICLES = [
    dict(slug=S1, title="The Quote-to-Cash Process in Manufacturing: Where the Days and the Cash Go",
         desc="The quote-to-cash process for a manufacturer, stage by stage: who does what, where 66 days go and why $1 million sits in open orders.",
         tags=["quote to cash", "order to cash", "Q2C", "cash conversion", "days sales outstanding", "working capital", "manufacturing"],
         body=F.nowrap(post1(), [(3, 0, 30)]), related=[S2, S3, OEE]),
    dict(slug=S2, title="Quote-to-Cash Simulation: Run a Window Factory in 3D",
         desc="A live 3D simulation of a window factory. Change quoting, invoicing, deposits, batch size and uptime, and watch the days and the cash respond.",
         tags=["quote to cash", "simulation", "3D factory model", "discrete-event simulation", "on-time delivery", "working capital"],
         body=post2(), related=[S1, S3, OEE]),
    dict(slug=S3, title="Shorten Quote to Cash: What to Fix First and the Payback",
         desc="Six fixes for a slow quote-to-cash process, tested in a simulation and ranked by days saved, cash freed and effort, with a payback calculator.",
         tags=["quote to cash", "cash flow", "invoicing", "deposits", "payback", "process improvement", "working capital"],
         body=F.nowrap(post3(), [(2, 1, 30)]), related=[S1, S2, PLAN]),
]

if __name__ == "__main__":
    for i, a in enumerate(ARTICLES):
        words = len(re.sub(r"<svg.*?</svg>|<script.*?</script>|<[^>]+>", " ", a["body"], flags=re.S).split())
        a.update(cats=["operational-efficiency", "process-improvement"], date="2026-11-14", author="Quak Foo Lee",
                 read=f"{max(1, round(words / 220))} min read", cover_label="Quote to Cash",
                 series=dict(name="Quote-to-cash series", part=i + 1, of=len(ARTICLES)))
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"], words, "words,", a["read"], "| desc", len(a["desc"]), "chars")
    if "--svg" in sys.argv:                                     # standalone swim lane for the PNG export
        out = sys.argv[sys.argv.index("--svg") + 1]
        open(out, "w", encoding="utf-8").write(fig_swimlane(standalone=True))
