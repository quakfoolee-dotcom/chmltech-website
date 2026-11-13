"""Inventory series, Parts 5 and 6 (V4.68): reorder point and EOQ; sales and operations planning.

Both use Ridgeline Coatings, the fictional manufacturer of Posts 3 and 4. All figures are computed here.
Usage:  python3 content/articles/inventory2_articles.py
        python3 content/gen/add_article.py <slug>   (each)
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from inventory_articles import S1, S2, S3, S4, S5, S6, T5, T6, CLOSE, part
from feed_articles import nowrap, svg, fig, txt, NAVY, BLUE, GREEND, ORANGE, RED, MUTED, LINE, SAND, PALE, GREENF

P = {i: f'<a href="{s}.html">Post&nbsp;{i}</a>' for i, s in enumerate([S1, S2, S3, S4, S5, S6], 1)}
OEE = "what-oee-really-measures"

# ───────────── Part 5 data: Ridgeline RM-01 epoxy resin and RM-08 dispersant (from Post 4) ─────────────
WK = 52
R1 = dict(name="RM-01 Epoxy resin", d=3462, c=4.20, S=250.0, ss=12554, rop=33324, unit="kg")
R8 = dict(name="RM-08 Dispersant additive", d=46, c=14.00, S=150.0, ss=229, rop=599, unit="kg")
HOLD = 0.25


def eoq(r):
    D = r["d"] * WK; H = HOLD * r["c"]
    return D, H, math.sqrt(2 * D * r["S"] / H)


def tc(r, Q, price=None):
    D, H, _ = eoq(r); c = price or r["c"]; h = HOLD * c
    return D / Q * r["S"] + Q / 2 * h, D * c


D1, H1, Q1 = eoq(R1)
D8, H8, Q8 = eoq(R8)
TRUCK, DISC = 20000, 0.02
C_EOQ_REL, C_EOQ_BUY = tc(R1, Q1)
C_TRK_REL, C_TRK_BUY = tc(R1, TRUCK, R1["c"] * (1 - DISC))
SAVE = (C_EOQ_REL + C_EOQ_BUY) - (C_TRK_REL + C_TRK_BUY)


def fig_eoq():
    Qs = [q for q in range(2000, 30001, 250)]
    order = [D1 / q * R1["S"] for q in Qs]; hold = [q / 2 * H1 for q in Qs]; tot = [a + b for a, b in zip(order, hold)]
    X = lambda q: 80 + (q - 2000) / 28000 * 600; Y = lambda v: 240 - v / 25000 * 210
    s = ""
    for v in range(0, 25001, 5000):
        s += f'<line x1="80" y1="{Y(v):.1f}" x2="680" y2="{Y(v):.1f}" stroke="{LINE}"/>' + txt(72, Y(v) + 4, f"${v / 1000:.0f}k", "end", MUTED, 12)
    for q in (5000, 10000, 15000, 20000, 25000, 30000):
        s += txt(X(q), 258, f"{q:,}", "middle", MUTED, 12)
    band = f'<rect x="{X(Q1 * 0.7):.1f}" y="30" width="{X(Q1 * 1.4) - X(Q1 * 0.7):.1f}" height="210" fill="{GREENF}" opacity=".55"/>'
    s += band
    for ys, col, lab, at, dy in ((order, ORANGE, "Ordering cost", 26000, -8), (hold, BLUE, "Holding cost", 27500, 20), (tot, NAVY, "Total", 17000, -10)):
        s += '<polyline fill="none" stroke="' + col + '" stroke-width="2.4" points="' + " ".join(f"{X(q):.1f},{Y(v):.1f}" for q, v in zip(Qs, ys)) + '"/>'
        v = ys[Qs.index(at)]; s += txt(X(at), Y(v) + dy, lab, "middle", col, 12.5, True)
    s += f'<line x1="{X(Q1):.1f}" y1="30" x2="{X(Q1):.1f}" y2="240" stroke="{GREEND}" stroke-width="1.6" stroke-dasharray="5 4"/>'
    s += txt(X(Q1), 24, f"EOQ ≈ {Q1:,.0f} kg", "middle", GREEND, 12.5, True)
    s += f'<line x1="{X(TRUCK):.1f}" y1="30" x2="{X(TRUCK):.1f}" y2="240" stroke="{RED}" stroke-width="1.6" stroke-dasharray="5 4"/>'
    s += txt(X(TRUCK) + 6, 44, "Truckload 20,000 kg", "start", RED, 12.5, True)
    s += txt(380, 278, "Order quantity (kg)", "middle", NAVY, 12.5, True)
    return svg(f"Annual ordering cost, holding cost and their total for epoxy resin RM-01 against order quantity from 2,000 to 30,000 kilograms. Ordering cost falls and holding cost rises; "
               f"the total is lowest at the economic order quantity of about {Q1:,.0f} kilograms and is flat around it: a shaded band from 70 to 140 percent of the EOQ costs only a few percent more. "
               "A line marks a 20,000 kilogram truckload.", 716, 288, s, 600, x0=0)


def post5():
    body = f"""{part(5)}
<p>{P[2]} and {P[4]} answered <em>when</em> to order: when stock falls to the reorder point. They did not answer <em>how much</em> to order each time. Order too little and the business spends its days raising purchase orders and receiving small deliveries. Order too much and cash sits in the warehouse. This post sets the order quantity for two of the Ridgeline Coatings materials from {P[4]}, using the classic economic order quantity, and then shows why the real answer is often a truckload.</p>
<h2>The two questions, together</h2>
<p>A reorder-point system has two settings for each item:</p>
<ul>
<li><strong>Reorder point (when).</strong> Average demand during the lead time plus safety stock. {P[4]} set it at {R1['rop']:,}&nbsp;kg for epoxy resin RM-01.</li>
<li><strong>Order quantity (how much).</strong> The amount ordered each time stock reaches the reorder point. This post sets it.</li>
</ul>
<p>The two interact. Average stock on hand is roughly the safety stock plus half the order quantity, so a larger order raises average inventory one for one.</p>
<h2>The economic order quantity</h2>
<p>Each order has a fixed cost: raising and approving the purchase order, receiving, inspection and paying the invoice. Holding stock has a cost too: the capital tied up, storage, insurance and the risk of damage or obsolescence, usually expressed as a percentage of the item's cost per year. Small orders keep holding cost low but make ordering cost high; large orders do the opposite. The economic order quantity (EOQ) balances the two:</p>
<p style="background:var(--sand);padding:14px 18px;border-radius:8px;font-family:Georgia,serif;font-size:17px;overflow-x:auto;white-space:nowrap">EOQ = √( 2 × D × S / H )</p>
<p>where D is annual demand, S the cost of placing one order and H the cost of holding one unit for a year.</p>
<h2>Worked example: two Ridgeline materials</h2>
<table>
<tr><th>Input</th><th>{R1['name']}</th><th>{R8['name']}</th></tr>
<tr><td>Average weekly use (from {P[4]})</td><td>{R1['d']:,}&nbsp;kg</td><td>{R8['d']:,}&nbsp;kg</td></tr>
<tr><td>Annual demand, D</td><td>{D1:,.0f}&nbsp;kg</td><td>{D8:,.0f}&nbsp;kg</td></tr>
<tr><td>Unit cost</td><td>${R1['c']:.2f}</td><td>${R8['c']:.2f}</td></tr>
<tr><td>Cost per order, S</td><td>${R1['S']:,.0f} (incl. incoming QC test)</td><td>${R8['S']:,.0f}</td></tr>
<tr><td>Holding cost, H ({HOLD * 100:.0f}% a year)</td><td>${H1:.2f} per kg a year</td><td>${H8:.2f} per kg a year</td></tr>
<tr><td><strong>EOQ</strong></td><td><strong>{Q1:,.0f}&nbsp;kg</strong></td><td><strong>{Q8:,.0f}&nbsp;kg</strong></td></tr>
<tr><td>Weeks of use per order</td><td>{Q1 / R1['d']:.1f}</td><td>{Q8 / R8['d']:.1f}</td></tr>
<tr><td>Orders per year</td><td>{D1 / Q1:.0f}</td><td>{D8 / Q8:.0f}</td></tr>
<tr><td>Reorder point (from {P[4]})</td><td>{R1['rop']:,}&nbsp;kg</td><td>{R8['rop']:,}&nbsp;kg</td></tr>
<tr><td>Average stock ≈ safety stock + EOQ/2</td><td>{R1['ss'] + Q1 / 2:,.0f}&nbsp;kg</td><td>{R8['ss'] + Q8 / 2:,.0f}&nbsp;kg</td></tr>
</table>
<p>For epoxy resin, the EOQ is about {Q1 / R1['d']:.1f} weeks of use per order. For the low-volume dispersant it is about {Q8 / R8['d']:.0f} weeks, because the fixed cost of an order is large relative to what is bought. Before accepting that, check the dispersant's shelf life: ten weeks of an additive with a six-month shelf life is fine; with a two-month shelf life it is not.</p>
<h2>The curve is flat at the bottom</h2>
{fig(fig_eoq(), 1, f"Annual ordering, holding and total cost for epoxy resin RM-01. The total is lowest at the EOQ and changes little over a wide range around it.")}
<p>The most useful property of the EOQ is that the total cost curve is flat near its minimum. Ordering 30% less or 40% more than the EOQ raises the combined ordering and holding cost by only a few percent. That makes the EOQ robust to rough estimates of S and H, and it means practical constraints can usually override it at little cost.</p>
<h2>When the truckload wins</h2>
<p>Real suppliers sell in lots, pallets, totes and truckloads, and they price accordingly. Suppose Ridgeline's resin supplier offers a {DISC * 100:.0f}% discount on full {TRUCK:,}&nbsp;kg truckloads. Compare a year of each:</p>
<table>
<tr><th>Annual cost</th><th>EOQ, {Q1:,.0f}&nbsp;kg</th><th>Truckload, {TRUCK:,}&nbsp;kg</th></tr>
<tr><td>Ordering + holding</td><td>${C_EOQ_REL:,.0f}</td><td>${C_TRK_REL:,.0f}</td></tr>
<tr><td>Material</td><td>${C_EOQ_BUY:,.0f}</td><td>${C_TRK_BUY:,.0f}</td></tr>
<tr><td><strong>Total</strong></td><td><strong>${C_EOQ_REL + C_EOQ_BUY:,.0f}</strong></td><td><strong>${C_TRK_REL + C_TRK_BUY:,.0f}</strong></td></tr>
</table>
<p>The truckload costs more to hold, but the discount is worth more than the extra holding cost, saving about ${SAVE:,.0f} a year. The truckload is the better choice, provided two checks pass:</p>
<ul>
<li><strong>Storage.</strong> Peak stock just after a delivery is the safety stock plus the order: {R1['ss']:,} + {TRUCK:,} = {R1['ss'] + TRUCK:,}&nbsp;kg. The tank or warehouse must hold it.</li>
<li><strong>Cash.</strong> Average stock rises from about {R1['ss'] + Q1 / 2:,.0f}&nbsp;kg to {R1['ss'] + TRUCK / 2:,.0f}&nbsp;kg, about ${(TRUCK - Q1) / 2 * R1['c']:,.0f} more inventory on the balance sheet. A business short of working capital may still choose the smaller order.</li>
</ul>
<h2>Setting the rules in your system</h2>
<ol>
<li>Calculate the EOQ for class A and B items. For class C items, a simple rule, such as three or six months of use, is usually good enough.</li>
<li>Round to the supplier's pack size, pallet or truckload, and test any quantity discount as above.</li>
<li>Check the result against shelf life, storage capacity and cash.</li>
<li>Enter the reorder point from {P[2]} or {P[4]} and the order quantity from this post in the ERP, and review both at least yearly.</li>
</ol>
<h2>Your checklist</h2>
<ul>
<li>Estimate the cost of placing one order, including receiving and inspection</li>
<li>Set a holding cost rate, typically 20 to 30% of item cost a year</li>
<li>Calculate the EOQ for class A and B items</li>
<li>Test pack sizes and quantity discounts against the EOQ</li>
<li>Check peak stock against storage and shelf life</li>
</ul>
<p><strong>Next in the series:</strong> {P[6]} steps back from individual items to the monthly plan that sets how much the plant will make and buy.</p>
{CLOSE}"""
    body = nowrap(body, [(2, 0, 30)])
    return dict(slug=S5, title=T5, desc="How much to order each time: the economic order quantity, why its cost curve is flat, and when a truckload discount wins, on two worked materials.",
                cats=["operational-efficiency", "process-improvement"], tags=["EOQ", "economic order quantity", "reorder point", "order quantity", "inventory management", "quantity discount"],
                body=body, date="2026-11-13", author="Quak Foo Lee", read="7 min read", cover_label="Inventory",
                series=dict(name="Inventory series", part=5, of=6), related=[S4, S2, S6])


# ───────────── Part 6 data: Ridgeline S&OP ─────────────
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
SEAS = [0.80, 0.90, 1.10, 1.30, 1.35, 1.20]
FAM = [("Primers", 165, 2.0), ("Topcoats", 135, 1.5), ("Specialty", 30, 0.8)]   # t/month base, t/h line rate
CAP_H = 2 * 8 * 21 * 0.75            # two shifts, 21 days, OEE 75 %
DEM_T = [[b * k for k in SEAS] for _, b, _ in FAM]
DEM_H = [sum(DEM_T[i][m] / FAM[i][2] for i in range(3)) for m in range(6)]
TOTAL_DEM_H = sum(DEM_H)


def level_plan():
    """Produce at capacity in early months to build stock for the peak (pre-build), never above capacity."""
    prod, inv = [], []; stock = 0.0
    need_after = [sum(max(0, DEM_H[j] - CAP_H) for j in range(m, 6)) for m in range(6)]
    for m in range(6):
        p = min(CAP_H, DEM_H[m] + max(0, need_after[m] - stock)) if DEM_H[m] <= CAP_H else CAP_H
        stock += p - DEM_H[m]; prod.append(p); inv.append(stock)
    return prod, inv


PROD, INV = level_plan()
SHORT = sum(max(0, DEM_H[m] - CAP_H) for m in range(6))


def fig_sop():
    X = lambda m: 110 + m * 95; Y = lambda h: 240 - h / 320 * 210
    s = ""
    for h in range(0, 321, 80):
        s += f'<line x1="80" y1="{Y(h):.1f}" x2="690" y2="{Y(h):.1f}" stroke="{LINE}"/>' + txt(72, Y(h) + 4, f"{h} h", "end", MUTED, 12)
    for m in range(6):
        s += f'<rect x="{X(m) - 30}" y="{Y(DEM_H[m]):.1f}" width="28" height="{240 - Y(DEM_H[m]):.1f}" fill="{BLUE}" opacity=".85"/>'
        s += f'<rect x="{X(m) + 2}" y="{Y(PROD[m]):.1f}" width="28" height="{240 - Y(PROD[m]):.1f}" fill="{GREEND}" opacity=".85"/>'
        s += txt(X(m), 258, MONTHS[m], "middle", NAVY, 12.5, True)
    s += f'<line x1="80" y1="{Y(CAP_H):.1f}" x2="690" y2="{Y(CAP_H):.1f}" stroke="{RED}" stroke-width="2" stroke-dasharray="7 4"/>'
    s += txt(686, Y(CAP_H) - 7, f"Effective capacity {CAP_H:.0f} h", "end", RED, 12.5, True)
    s += f'<rect x="90" y="16" width="14" height="14" fill="{BLUE}"/>' + txt(110, 28, "Demand (line hours)", fill=NAVY, fs=12.5)
    s += f'<rect x="270" y="16" width="14" height="14" fill="{GREEND}"/>' + txt(290, 28, "Planned production", fill=NAVY, fs=12.5)
    return svg("Bar chart of demand and planned production in mixing line hours for January to June, against an effective capacity line of "
               f"{CAP_H:.0f} hours. Demand is " + ", ".join(f"{MONTHS[m]} {DEM_H[m]:.0f}" for m in range(6)) +
               f" hours. Production is planned above demand in January to build about {max(INV):.0f} hours of stock, which covers April and May, when demand exceeds capacity.", 720, 268, s, 600, x0=0)


def post6():
    rows = "".join(f"<tr><td>{MONTHS[m]}</td><td class=\"num\">{sum(DEM_T[i][m] for i in range(3)):,.0f}</td><td class=\"num\">{DEM_H[m]:,.0f}</td>"
                   f"<td class=\"num\">{CAP_H:,.0f}</td><td class=\"num\">{CAP_H - DEM_H[m]:+,.0f}</td><td class=\"num\">{PROD[m]:,.0f}</td><td class=\"num\">{INV[m]:,.0f}</td></tr>" for m in range(6))
    body = f"""{part(6)}
<p>The first five posts in this series dealt with items: which matter ({P[1]}, {P[3]}), how much buffer each needs ({P[2]}, {P[4]}) and how much to order each time ({P[5]}). All of those settings assume someone has decided how much the business will sell and make in the coming months. In many small manufacturers, no one has. Sales forecasts live in one spreadsheet, the production schedule in another, purchasing works from the ERP's suggestions, and finance learns the result at month end.</p>
<p>Sales and operations planning (S&amp;OP) is the monthly routine that produces one agreed plan. This post describes a version sized for a business of 20 to 200 people, and runs it for Ridgeline Coatings.</p>
<h2>What S&amp;OP is, and is not</h2>
<p>S&amp;OP balances expected demand against the capacity to supply it, by product family, over a horizon of roughly 6 to 18 months, and records the decisions taken to close the gaps. It is not a detailed schedule; the schedule comes later and works within the plan. It is not a sales forecast either; the forecast is one input. Its output is a single plan that sales, operations, purchasing and finance all work to.</p>
<h2>The monthly cycle</h2>
<table>
<tr><th>Week</th><th>Step</th><th>Who</th><th>Output</th></tr>
<tr><td>1</td><td>Data: last month's actuals, updated forecast inputs</td><td>Planner</td><td>Sales, production, inventory and backlog by family</td></tr>
<tr><td>1–2</td><td>Demand review</td><td>Sales lead, planner</td><td>Unconstrained demand plan by family, with assumptions</td></tr>
<tr><td>2</td><td>Supply review</td><td>Operations, purchasing, planner</td><td>Capacity and material check against the demand plan; gaps and options</td></tr>
<tr><td>3</td><td>Pre-meeting</td><td>Planner, finance</td><td>Options costed; recommendation</td></tr>
<tr><td>3–4</td><td>Executive meeting (one hour)</td><td>Owner or general manager, department heads</td><td>Decisions; one approved plan</td></tr>
</table>
<p>In a small business, the same few people attend several steps, and the whole cycle may take a few hours of each person's month. The discipline is in doing it every month, on a fixed calendar, with the decisions written down.</p>
<h2>Worked example: Ridgeline's spring peak</h2>
<p>Ridgeline makes three product families on one mixing line. Demand for coatings peaks in spring. The line runs two shifts on 21 working days a month; at the plant's 75% <a href="{OEE}.html">OEE</a>, that gives about {CAP_H:,.0f} effective hours a month. The table converts the demand plan into line hours using each family's rate (primers {FAM[0][2]}&nbsp;t/h, topcoats {FAM[1][2]}&nbsp;t/h, specialty {FAM[2][2]}&nbsp;t/h).</p>
<table>
<tr><th>Month</th><th class="num">Demand (t)</th><th class="num">Demand (h)</th><th class="num">Capacity (h)</th><th class="num">Gap (h)</th><th class="num">Plan (h)</th><th class="num">Pre-built stock (h)</th></tr>
{rows}
</table>
{fig(fig_sop(), 1, f"Ridgeline's demand and planned production in line hours. Building about {max(INV):.0f} hours of stock in January covers the April and May peak.")}
<p>Demand exceeds capacity in April and May by a total of about {SHORT:,.0f} line hours. Over the six months, total demand is {TOTAL_DEM_H:,.0f} hours against {6 * CAP_H:,.0f} available, so the problem is timing, not total capacity. The supply review lays out the options:</p>
<ul>
<li><strong>Pre-build.</strong> Make more than demand in a quiet month and store the surplus. Costs: inventory carrying cost and warehouse space for the stock built ahead, and the risk that the mix of demand changes.</li>
<li><strong>Overtime or a third shift in April and May.</strong> Costs: premium labour, and fatigue if extended.</li>
<li><strong>Raise OEE.</strong> Each point of OEE adds about {CAP_H / 75:,.1f} hours a month. Changeover reduction on the mixing line, prepared before the peak, may close part of the gap.</li>
<li><strong>Shape demand.</strong> Offer early-order incentives to distributors, or agree longer lead times on specialty products.</li>
</ul>
<p>The plan in the table pre-builds, which is often the cheapest option for products with a long shelf life. The executive meeting approves it, and in doing so approves the consequences: purchasing brings forward resin and solvent orders using the reorder points and order quantities from {P[4]} and {P[5]}, finance plans for the extra inventory held from January to May, and the warehouse arranges space.</p>
<h2>Measures that make it work</h2>
<table>
<tr><th>Measure</th><th>What it shows</th></tr>
<tr><td>Forecast accuracy by family</td><td>How far actual demand was from the plan, for example as mean absolute percentage error</td></tr>
<tr><td>Plan attainment</td><td>Production against the approved plan</td></tr>
<tr><td>On time in full (OTIF)</td><td>Whether customers got what they ordered, when promised</td></tr>
<tr><td>Inventory in weeks of supply</td><td>Whether stock is in line with the plan, by family</td></tr>
<tr><td>Decisions closed</td><td>Whether last month's actions were done</td></tr>
</table>
<p>Measure forecast accuracy at the family level, where S&amp;OP works, and track bias as well as error: a forecast that is always 10% high does more damage than one that is randomly wrong by 10%, because everything built on it is consistently too large.</p>
<h2>Starting small</h2>
<ol>
<li>Define three to six product families that share capacity and materials.</li>
<li>Pull 12 months of actual sales and production by family.</li>
<li>Agree a simple capacity measure for the bottleneck resource, in hours.</li>
<li>Hold the first executive meeting with a six-month view and one decision to make.</li>
<li>Repeat monthly; extend the horizon to 12 to 18 months once the routine holds.</li>
</ol>
<h2>Your checklist</h2>
<ul>
<li>Set a fixed monthly calendar for the S&amp;OP steps</li>
<li>Convert demand to bottleneck hours by family</li>
<li>Cost the options for every month where demand exceeds capacity</li>
<li>Record decisions and owners, and review them next month</li>
<li>Feed the approved plan into purchasing settings and the schedule</li>
</ul>
<h2>The series in one place</h2>
<ol>
<li><a href="{S1}.html">ABC Inventory Analysis: What It Is, How to Do It, and a Worked Example</a></li>
<li><a href="{S2}.html">Setting Safety Stock Without Guessing: Three Methods and a Worked Example</a></li>
<li><a href="{S3}.html">ABC Analysis for Manufacturers: Why Dollar Value Is Not Enough</a></li>
<li><a href="{S4}.html">Safety Stock for Manufacturers: Raw Materials and Spare Parts</a></li>
<li><a href="{S5}.html">{T5}</a></li>
<li>{T6} (this post)</li>
</ol>
{CLOSE}"""
    body = nowrap(body, [(1, 0, 6), (2, 0, 10), (3, 0, 32)])
    return dict(slug=S6, title=T6, desc="A monthly sales and operations planning routine for small manufacturers: the five steps, a worked capacity plan for a seasonal peak, and the measures.",
                cats=["operational-efficiency", "process-improvement"], tags=["S&OP", "sales and operations planning", "capacity planning", "demand planning", "production planning", "manufacturing"],
                body=body, date="2026-11-13", author="Quak Foo Lee", read="7 min read", cover_label="Inventory",
                series=dict(name="Inventory series", part=6, of=6), related=[S5, S4, OEE])


if __name__ == "__main__":
    for a in (post5(), post6()):
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("wrote", a["slug"], len(a["desc"]))
    print(f"Q1={Q1:.0f} Q8={Q8:.0f} save={SAVE:.0f} cap={CAP_H:.0f} dem={[round(x) for x in DEM_H]} prod={[round(x) for x in PROD]} inv={[round(x) for x in INV]}")
