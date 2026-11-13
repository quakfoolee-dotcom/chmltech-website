"""V4.80: the last 2023 posts in the audit (plan V8), rewritten or retired. Rewrites keep their address and original date.

Rewritten:
1. customization-standardization-and-flexibility-understanding-manufacturing-principles   MTS, ATO/CTO, MTO, ETO
2. 10-effective-communication-strategies-for-manufacturing-companies                     shop-floor communication
3. 10-proven-ways-to-boost-traffic-to-your-ecommerce-website                             traffic and conversion for a small store
4. bridging-the-gap-a-step-by-step-guide-to-conducting-a-gap-analysis-for-operational-efficiency   gap analysis

Retired:
- everything-you-need-to-know-about-iso-9001-2015-quality-management-system -> iso-9001-2026-what-changed-from-2015
- navigating-the-intersection-of-marketing-4-0-and-the-modern-customer-journey
    -> understanding-the-power-of-tofu-mofu-and-bofu-in-your-digital-marketing-strategy (new section FUNNEL_5A, v476_articles.fun)
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, MUTED, LINE, SAND, PALE, GREENF, ORANGEF
from v478_articles import src, rel, money, table, words, art, steps_fig

MFG = "customization-standardization-and-flexibility-understanding-manufacturing-principles"
COMMS = "10-effective-communication-strategies-for-manufacturing-companies"
ECOM = "10-proven-ways-to-boost-traffic-to-your-ecommerce-website"
GAP = "bridging-the-gap-a-step-by-step-guide-to-conducting-a-gap-analysis-for-operational-efficiency"
FUN = "understanding-the-power-of-tofu-mofu-and-bofu-in-your-digital-marketing-strategy"
ISO26 = "iso-9001-2026-what-changed-from-2015"
RETIRE = {ISO26: ["everything-you-need-to-know-about-iso-9001-2015-quality-management-system"],
          FUN: ["navigating-the-intersection-of-marketing-4-0-and-the-modern-customer-journey"]}
ORIGINAL = {MFG: "2023-03-27", COMMS: "2023-04-02", ECOM: "2023-04-02", GAP: "2023-04-08"}


# ═════════════════════════ 1. Manufacturing strategies ═════════════════════════
def fig_decouple():
    s = DEFS
    stages = ["Design", "Buy materials", "Make parts", "Assemble", "Ship"]
    xs = [200 + i * 106 for i in range(5)]
    for i, (x, st) in enumerate(zip(xs, stages)):
        s += txt(x + 48, 22, st, "middle", NAVY, 12.5, True)
    rows = [("Make-to-stock", 4, BLUE), ("Assemble-to-order", 3, GREEND), ("Make-to-order", 2, PURPLE), ("Engineer-to-order", 0, ORANGE)]
    for j, (n, k, c) in enumerate(rows):
        y = 36 + j * 40
        s += txt(190, y + 21, n, "end", NAVY, 12.5, True)
        for i, x in enumerate(xs):
            done = i < k
            s += f'<rect x="{x}" y="{y + 4}" width="96" height="26" rx="5" fill="{PALE if done else c}" stroke="{"#9AB0C8" if done else c}" opacity="{1 if done else .9}"/>'
        if 0 < k < 5:  # order line
            s += f'<line x1="{xs[k] - 5}" y1="{y}" x2="{xs[k] - 5}" y2="{y + 34}" stroke="{NAVY}" stroke-width="2.5"/>'
    s += f'<rect x="200" y="200" width="14" height="14" fill="{PALE}" stroke="#9AB0C8"/>' + txt(220, 212, "Done ahead of the order (to forecast)", "start", MUTED, 12)
    s += txt(470, 212, "Coloured: done after the order arrives", "start", MUTED, 12)
    return svg("Where the customer order enters the process for four strategies. Make-to-stock: design, buying, making, assembling and shipping "
               "are all done ahead of the order except shipping from stock. Assemble-to-order: design, buying and making parts are done ahead; "
               "assembly and shipping happen after the order. Make-to-order: design and buying ahead; making, assembly and shipping after the "
               "order. Engineer-to-order: everything, including design, happens after the order.", 742, 224, s, 600)


def mfg():
    strat = [("Make-to-stock (MTS)", "Finished products built to a forecast and shipped from stock", "Fast delivery; standard products; steady demand", "Inventory cost and obsolescence; forecast errors", "Fasteners, consumer goods, standard spare parts"),
             ("Assemble- or configure-to-order (ATO/CTO)", "Stocked sub-assemblies combined to the customer's choice", "Variety with short lead times", "Managing option rules and sub-assembly stock", "Pumps with motor options, furniture, computers"),
             ("Make-to-order (MTO)", "Standard designs built after the order", "Little finished stock; some customization", "Longer lead times; capacity planning matters", "Fabricated parts, industrial equipment, printing"),
             ("Engineer-to-order (ETO)", "Designed and built for each order", "Fully custom solutions", "Longest lead times; engineering is often the bottleneck", "Process skids, special machinery, structural steel")]
    body = f"""
<p>Every manufacturer has to decide how much work to do before a customer orders and how much after. Doing more in advance gives faster delivery but ties up money in stock that might not sell. Doing more after the order allows customization but makes customers wait. This trade-off between standardization and flexibility sits behind the four classic manufacturing strategies. This article, first written in 2023, has been rewritten with a figure, a comparison table and a worked example.</p>
<h2>The four strategies</h2>
{table(["Strategy", "How it works", "Strength", "Main challenge", "Typical products"], strat)}
<h2>The decoupling point</h2>
<p>The clearest way to see the difference is to ask where the customer order enters the process, sometimes called the order penetration or decoupling point. Everything before it is done to a forecast; everything after it is done to the order.</p>
{fig(fig_decouple(), 1, "The later the customer order enters the process, the more is done to forecast and the faster the delivery.")}
<p>Moving the decoupling point is one of the most powerful choices a manufacturer can make. Moving it later (towards make-to-stock) shortens lead times but needs better forecasts and more stock. Moving it earlier (towards make-to-order) cuts stock but needs more flexible capacity and shorter internal lead times.</p>
<h2>Standardize the parts, customize the product</h2>
<p>The best manufacturers do not choose between standardization and flexibility; they combine them. Standard modules, common parts across product families and a limited menu of options let customers get what feels like a custom product, while the plant builds mostly standard components to stock. This is the logic of assemble-to-order, and it is often the most profitable move for a small make-to-order or engineer-to-order shop.</p>
<h2>Worked example: moving from make-to-order to assemble-to-order</h2>
<p>A manufacturer of small industrial pumps builds every unit to order, with a lead time of six weeks, most of it waiting for machined housings and motors. Analysing two years of orders shows that 80% use one of four housing sizes and three motor ratings. The company decides to stock machined housings and the common motors, and to assemble and test to order. Lead time for the common configurations falls to about one week; unusual configurations stay at six weeks. The extra stock is a few weeks of the most common parts, worth far less than the orders previously lost to competitors with shorter lead times. The figures are illustrative.</p>
<h2>Choosing a strategy for each product family</h2>
<ul>
<li><strong>How long will customers wait?</strong> If the market expects delivery faster than your total lead time, some work must be done before the order.</li>
<li><strong>How predictable is demand?</strong> Stable, high-volume items suit stock; erratic, low-volume ones do not.</li>
<li><strong>How many variants?</strong> Many variants of a few common parts point to assemble-to-order.</li>
<li><strong>What does stock cost?</strong> Bulky, expensive or perishable items favour building later.</li>
<li><strong>Where is your bottleneck?</strong> In engineer-to-order shops it is often engineering, so standard designs and pre-engineered modules save the most time.</li>
</ul>
<p>Most small manufacturers run more than one strategy. Plan each product family on its own terms; see <a href="../post/production-planning-and-scheduling-for-manufacturing.html">production planning and scheduling</a> and <a href="../post/setting-safety-stock.html">setting safety stock</a> for how this flows into the plan.</p>
<h2>What it means for systems</h2>
<p>Each strategy needs different things from your planning software. Make-to-stock leans on forecasting and replenishment. Assemble-to-order needs product configurators and planning bills of materials. Make-to-order and engineer-to-order need job costing, capacity planning and project-style tracking. When choosing an <a href="../post/understanding-erp-vs-mrp-a-comprehensive-comparison-of-manufacturing-systems.html">MRP or ERP system</a>, test it against your actual mix of strategies.</p>
"""
    r = [("production-planning-and-scheduling-for-manufacturing", "Production planning and scheduling"),
         ("demystifying-mrp-a-comprehensive-guide-to-the-material-requirements-planning-process", "Material requirements planning (MRP), explained"),
         ("sales-and-operations-planning-for-small-manufacturers", "Sales and operations planning for small manufacturers")]
    return art(MFG, "Make-to-Stock, Assemble-to-Order, Make-to-Order or Engineer-to-Order? Choosing a Manufacturing Strategy",
               "The four manufacturing strategies compared, the customer order decoupling point, combining standard parts with custom products, and a worked pump example.",
               ["process-improvement", "lean", "operational-efficiency"], ["make to stock", "make to order", "assemble to order", "engineer to order", "decoupling point", "manufacturing strategy"],
               body, "Manufacturing", r)


# ═════════════════════════ 2. Shop-floor communication ═════════════════════════
def fig_tiers():
    s = DEFS
    tiers = [("Tier 1", "Team at the line", "Start of shift, 10 min", "Safety, yesterday's output, today's plan, problems", BLUE, PALE),
             ("Tier 2", "Supervisors and support", "Daily, 15 min", "Problems from tier 1 that need help; staffing; materials", GREEND, GREENF),
             ("Tier 3", "Plant manager and department heads", "Daily or weekly, 20–30 min", "Issues crossing departments; trends; priorities", PURPLE, "#E7E7F8")]
    for i, (t, who, when, what, c, f) in enumerate(tiers):
        y = 12 + i * 58
        s += f'<rect x="14" y="{y}" width="110" height="48" rx="8" fill="{c}"/>' + txt(69, y + 30, t, "middle", "#fff", 14, True)
        s += f'<rect x="132" y="{y}" width="596" height="48" rx="8" fill="{f}" stroke="{c}"/>'
        s += txt(146, y + 20, f"{who}  ·  {when}", "start", NAVY, 12.8, True) + txt(146, y + 38, what, "start", NAVY, 12.3)
    s += f'<path d="M740,170 L740,20" stroke="{ORANGE}" stroke-width="2" marker-end="url(#ah)"/>'
    return svg("Tiered daily meetings. Tier 1: the team at the line meets at the start of the shift for 10 minutes on safety, yesterday's output, "
               "today's plan and problems. Tier 2: supervisors and support staff meet daily for 15 minutes on problems from tier 1 that need "
               "help, staffing and materials. Tier 3: the plant manager and department heads meet daily or weekly for 20 to 30 minutes on issues "
               "that cross departments, trends and priorities. Problems escalate upward the same day.", 752, 186, s, 600)


def comms():
    handover = [("Safety", "Incidents, near misses, hazards left in place"), ("Production", "Output against plan; job in progress and where it stopped"),
                ("Quality", "Defects found, holds, first-off checks pending"), ("Equipment", "Breakdowns, temporary fixes, maintenance requested"),
                ("Materials", "Shortages, wrong material, deliveries expected"), ("People", "Absences, training, overtime approved")]
    body = f"""
<p>In a manufacturing plant, most communication problems show up as something physical: a wrong part made because a drawing changed and the old one was still at the machine, a breakdown nobody told the next shift about, or a defect that repeats for days because the people who saw it never reached the people who could fix it. This article, first written in 2023 as a list of general tips, has been rewritten around the practices that solve those problems on the shop floor.</p>
<h2>Tiered daily meetings</h2>
<p>Short, standing meetings at fixed times, in layers, move information up and decisions down within the same day. Each tier uses a simple board with the same few measures, and any problem the tier cannot solve goes up to the next one.</p>
{fig(fig_tiers(), 1, "Tiered meetings: each layer meets briefly, at the same time every day, and escalates what it cannot solve.")}
<h2>Shift handovers</h2>
<p>Information lost between shifts causes a large share of repeat problems. A written or digital handover, completed by the outgoing lead and read with the incoming lead at the machine or line, covers the same six areas every time:</p>
{table(["Area", "What to pass on"], handover)}
<p>Keep the form to one page. The conversation matters as much as the form; a two-minute walk of the line together catches what writing misses.</p>
<h2>Visual management</h2>
<p>The best communication on the shop floor often needs no words. Boards showing hourly output against target, red and green status on each machine, andon lights or calls for help, marked floor locations and current drawings at the point of use let anyone see the state of the work at a glance. The rule: if a supervisor has to ask how the line is doing, the board is not working.</p>
<h2>Instructions that people can follow</h2>
<ul>
<li><strong>Work instructions with photos</strong> at the workstation, controlled so the old version is removed when a new one is issued. See <a href="../post/essentials-of-effective-process-documentation.html">process documentation that people use</a>.</li>
<li><strong>Plain language,</strong> with key steps translated where the workforce speaks several languages.</li>
<li><strong>Change notices</strong> for engineering changes, explained at the tier 1 meeting before the first affected job starts.</li>
<li><strong>Teach-back:</strong> for critical tasks, ask the operator to explain the step back rather than asking "any questions?"</li>
</ul>
<h2>Listening upward</h2>
<p>Operators see problems first. Make it easy and safe to raise them: a problem board at each area, a promise that every item gets an answer within a week, and recognition for ideas that are used. When people see their suggestions acted on, they keep making them; when suggestions disappear, they stop.</p>
<h2>Worked example: cutting repeat defects with a handover and tier 1 meeting</h2>
<p>A plastics moulder runs three shifts and sees the same short-shot defect reappear after almost every shift change, because setting adjustments made by one shift are not passed on. The plant introduces a one-page handover covering process settings, defects and holds, and a ten-minute tier 1 meeting at each shift start. Within two months, repeat defects of the same type fall by more than half, and the tier 2 meeting starts fixing causes rather than symptoms. The figures are illustrative.</p>
<h2>Digital tools, used carefully</h2>
<p>Tablets at the line, digital boards, shift logs and team messaging apps can make all of this faster, especially across shifts and sites. Keep the paper version's simplicity: the same measures every day, one place to look, and no expectation that operators read messages while running a machine. Our <a href="../post/effective-communication-of-goals-and-performance.html">scorecards and meeting rhythm</a> article covers the management side of the same system.</p>
"""
    r = [("effective-communication-of-goals-and-performance", "Scorecards and a meeting rhythm that work"),
         ("what-oee-really-measures", "What OEE really measures"), ("perform-kaizen-event", "How to run a Kaizen event")]
    return art(COMMS, "Communication on the Shop Floor: Tiered Meetings, Shift Handovers and Visual Management",
               "How manufacturers fix communication where it matters: tiered daily meetings, shift handovers, visual management, usable instructions, listening upward and a worked example.",
               ["operational-efficiency", "lean"], ["manufacturing communication", "tiered meetings", "shift handover", "visual management", "andon", "shop floor"],
               body, "Shop floor", r)


# ═════════════════════════ 3. E-commerce ═════════════════════════
SESS, CONV_A, CONV_B, AOV = 20_000, 0.012, 0.016, 85


def ecom():
    channels = [("Search (SEO)", "Category and product pages that match what people search; fast mobile pages; structured data", "Months", "Low, ongoing"),
                ("Google free listings and Shopping ads", "Product feed in Google Merchant Center", "Days to weeks", "Free listings; ads pay per click"),
                ("Email", "Welcome series, abandoned-cart reminders, a regular newsletter", "Weeks", "Low"),
                ("Social media", "Short video, behind the scenes, user content; links in bio and Stories", "Weeks to months", "Low to medium"),
                ("Paid social", "Targeted ads to look-alike and retargeting audiences", "Days", "Medium to high"),
                ("Marketplaces", "Amazon or others as a second channel", "Weeks", "Fees per sale"),
                ("Partnerships and creators", "Reviews, bundles and collaborations with complementary brands", "Weeks", "Varies")]
    body = f"""
<p>For a small online store, traffic is only half the problem. A store converting 1% of visitors needs twice the traffic of one converting 2% to make the same sales, so improving the store often pays faster than buying more visitors. This guide, first written in 2023 as ten traffic tips, has been rewritten to cover both: the main traffic channels, and the conversion basics that decide whether the traffic pays off.</p>
<h2>Traffic channels compared</h2>
{table(["Channel", "What it takes", "Time to results", "Cost"], channels)}
<p>Most small stores do best with two or three channels done well: search and Google listings for people already looking, email for repeat sales, and one social channel for discovery.</p>
<h2>Product pages that rank and sell</h2>
<ul>
<li><strong>Write your own descriptions.</strong> Manufacturer text is on hundreds of other sites; your own words, sizing advice and use cases help both search and buyers.</li>
<li><strong>Answer the questions that stop a purchase:</strong> dimensions, materials, compatibility, delivery time and cost, returns.</li>
<li><strong>Show it properly:</strong> several photos, a short video, and the product in use.</li>
<li><strong>Collect and show reviews,</strong> including photos from customers.</li>
<li><strong>Add product structured data</strong> so search engines can show price, availability and ratings.</li>
</ul>
<h2>Conversion basics</h2>
<ol>
<li><strong>Speed on mobile.</strong> Most visits are on phones; slow pages lose buyers. See <a href="../post/what-is-technical-seo-basics-and-10-best-practices.html">technical SEO and Core Web Vitals</a>.</li>
<li><strong>Clear shipping costs early.</strong> Unexpected costs at checkout are a leading reason for abandoned carts.</li>
<li><strong>A short checkout</strong> with guest checkout and common payment options.</li>
<li><strong>Trust signals:</strong> real contact details, returns policy, secure payment, reviews.</li>
<li><strong>Abandoned-cart emails,</strong> sent within hours, often recover a meaningful share of lost sales.</li>
</ol>
<h2>Worked example: traffic or conversion?</h2>
<p>A store has {SESS:,} sessions a month, converts {CONV_A:.1%} and has an average order of {money(AOV)}, giving about {SESS * CONV_A:.0f} orders and {money(SESS * CONV_A * AOV)} a month. Raising conversion to {CONV_B:.1%} through faster pages, clearer shipping costs and abandoned-cart emails gives about {SESS * CONV_B:.0f} orders and {money(SESS * CONV_B * AOV)}, an extra {money(SESS * (CONV_B - CONV_A) * AOV)} a month with no extra traffic. Getting the same increase from traffic alone would need about {SESS * CONV_B / CONV_A - SESS:,.0f} more sessions a month. The figures are illustrative; your own analytics will show which lever is cheaper.</p>
<h2>Measure what matters</h2>
<p>Track sessions, conversion rate, average order value and revenue by channel in Google Analytics 4, with e-commerce events set up so you can see where shoppers drop off: product view, add to cart, begin checkout, purchase. Tag links from email and social with UTM parameters. Review monthly and move effort towards the channels that bring buyers, not just visitors. See our <a href="../post/how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide.html">GA4 guide</a>.</p>
<h2>Repeat customers</h2>
<p>Winning a first order is expensive; repeat orders are where many small stores make their margin. A good post-purchase email, a reason to come back (replenishment reminders, new arrivals, a loyalty offer) and excellent service when something goes wrong all raise repeat rates. Keep commercial email within Canada's anti-spam legislation (CASL) by collecting consent at checkout.</p>
"""
    r = [("5-tips-to-drive-more-website-traffic-from-instagram", "Instagram and social media for small businesses"),
         ("what-is-technical-seo-basics-and-10-best-practices", "Technical SEO in 2026"),
         ("from-creation-to-conversion-measuring-the-success-of-your-content-marketing-strategy", "How to measure content marketing")]
    return art(ECOM, "Growing a Small Online Store: Traffic Channels and the Conversion Basics That Make Them Pay",
               "Traffic channels for a small online store compared, product pages that rank and sell, conversion basics, a traffic-versus-conversion worked example and what to measure.",
               ["marketing", "digital-technology"], ["e-commerce", "online store", "conversion rate", "Google Shopping", "email marketing", "product pages", "SEO"], body, "E-commerce", r)


# ═════════════════════════ 4. Gap analysis ═════════════════════════
def fig_gap():
    return steps_fig([("1. Scope", ["Process, area or", "standard to assess"]), ("2. Future state", ["What good looks", "like, measurably"]),
                      ("3. Current state", ["Map and measure", "how it works now"]), ("4. Gaps", ["Differences,", "with their causes"]),
                      ("5. Prioritize", ["Value against", "effort and risk"]), ("6. Plan and act", ["Owners, dates,", "measures; review"])],
                     "Six steps of a gap analysis: scope the process, area or standard to assess; define the future state measurably; map and measure "
                     "the current state; list the gaps with their causes; prioritize by value against effort and risk; and plan and act with owners, "
                     "dates and measures, then review.")


def gap():
    rows = [("Quote turnaround", "6 working days", "2 working days", "Material prices requested from suppliers for every quote", "Monthly price list for top materials", "High", "Low"),
            ("Order entry", "Re-keyed from email into ERP", "Web orders flow into ERP", "No integration", "Connector between store and ERP", "High", "Medium"),
            ("Schedule visibility", "Whiteboard updated daily", "Live schedule on screens", "Schedule kept in a spreadsheet", "Use ERP scheduling; screens at lines", "Medium", "Medium"),
            ("Inventory accuracy", "About 85%", "95% or better", "No cycle counting; unrecorded issues", "Weekly cycle counts; scan on issue", "High", "Low"),
            ("Supplier invoices", "Paper approval, 9 days", "Automatic match, 3 days", "Manual three-way match", "Automate PO, receipt and invoice match", "Medium", "Medium")]
    body = f"""
<p>A gap analysis compares where a process, team or business is today with where it needs to be, and lists the differences with their causes and a plan to close them. It is one of the most practical tools in improvement work: simple enough to do in a few workshops, structured enough to turn opinions into a prioritized plan. This guide, first written in 2023, has been rewritten with a figure, a worked example table and the common uses in small and mid-sized businesses.</p>
<h2>Where gap analysis is used</h2>
<ul>
<li><strong>Process improvement:</strong> current versus target performance for a process such as quoting, order entry or month-end close.</li>
<li><strong>Digital adoption:</strong> the systems and data you have versus what you need, often the core of a digital adoption plan.</li>
<li><strong>Standards and certification:</strong> your quality system against ISO 9001, or your security controls against a framework.</li>
<li><strong>Skills:</strong> the capabilities the team has versus those the plan requires.</li>
<li><strong>Strategy:</strong> the capabilities and market position needed to reach a goal versus today's.</li>
</ul>
<h2>Six steps</h2>
{fig(fig_gap(), 1, "A gap analysis in six steps.")}
<h3>1. Scope</h3>
<p>Be specific: "order handling from receipt to shipment" or "our quality system against ISO 9001:2026", not "operations". A narrow scope gives a usable result in weeks.</p>
<h3>2. Define the future state</h3>
<p>Describe what good looks like in measurable terms: quote turnaround of two days, inventory accuracy of 95%, all orders entered once. Where possible, base targets on customer needs, a standard or a credible benchmark rather than aspiration.</p>
<h3>3. Map the current state</h3>
<p>Walk the process with the people who do it, measure it and collect evidence. Resist the temptation to describe the current state from memory in a meeting room.</p>
<h3>4. List the gaps and their causes</h3>
<p>For each difference, ask why it exists. A gap described only as a symptom ("quotes are slow") leads to the wrong fix; one described with its cause ("we wait for supplier prices on every quote") points to the right one.</p>
<h3>5. Prioritize</h3>
<p>Score each gap on the value of closing it and the effort and risk involved. Close high-value, low-effort gaps first; plan the large ones as projects.</p>
<h3>6. Plan, act and review</h3>
<p>Give each action an owner, a date and a measure, and review progress monthly. Repeat the gap analysis after six to twelve months to see what moved.</p>
<h2>Worked example: a small manufacturer's operations</h2>
<p>The table shows part of a gap analysis for order handling and planning in a 40-person fabrication business. The figures are illustrative.</p>
{table(["Area", "Current state", "Future state", "Cause of the gap", "Action", "Value", "Effort"], rows)}
<p>The two high-value, low-effort items, the price list for quotes and weekly cycle counting, start immediately. The ERP connector and scheduling work become a planned project, because both depend on clean item data, which the cycle counting also improves.</p>
<h2>Tips for a useful result</h2>
<ul>
<li>Involve people from each step of the process; gaps often sit in the hand-offs between teams.</li>
<li>Use evidence: timings, error counts, samples of documents, not impressions.</li>
<li>Keep the output to a few pages; a 60-page report rarely gets acted on.</li>
<li>Separate quick fixes from projects so momentum starts while bigger changes are planned.</li>
<li>Re-run it: a gap analysis is a snapshot, and its value comes from repeating it.</li>
</ul>
<p>For certification-style gap analyses, see our <a href="../post/iso-9001-2026-transition-plan.html">ISO 9001:2026 transition plan</a>; for process work, <a href="../post/how-to-perform-a-successful-business-process-optimization.html">business process optimization</a>.</p>
"""
    r = [("how-to-perform-a-successful-business-process-optimization", "Business process optimization: map, measure, redesign"),
         ("iso-9001-2026-transition-plan", "ISO 9001:2026 transition plan"),
         ("boost-your-business-with-cdap-funding-support-for-digital-adoption", "Digital adoption planning and funding")]
    return art(GAP, "Gap Analysis: A Step-by-Step Guide with a Worked Example",
               "How to run a gap analysis in six steps, where it is used, a worked example for a small manufacturer's operations, and tips for a result people act on.",
               ["process-improvement", "project-management", "operational-efficiency"], ["gap analysis", "current state", "future state", "process improvement", "digital adoption plan", "ISO gap analysis"],
               body, "Gap analysis", r)


FUNNEL_5A = """<h2>The funnel and the 5A customer path</h2>
<p>An older article on this site discussed <cite>Marketing 4.0</cite> by Philip Kotler, Hermawan Kartajaya and Iwan Setiawan, which proposed the "5A" customer path as an update to the classic funnel for a connected world: aware, appeal, ask, act and advocate. Two of its ideas are worth keeping alongside the funnel. First, the ask stage: buyers now research by asking others, reading reviews and comparing online before they contact you, so your reputation and content answer questions you never hear. Second, advocacy: satisfied customers who recommend you become a source of new awareness, so the path loops back on itself. In practice this means measuring reviews, referrals and repeat business alongside the funnel stages above, and treating existing customers as part of marketing.</p>
"""


if __name__ == "__main__":
    op = os.path.join(HERE, "original_dates.json")
    od = json.load(open(op, encoding="utf-8")); od.update(ORIGINAL)
    note = od.pop("_note"); json.dump({"_note": note, **dict(sorted(od.items()))}, open(op, "w", encoding="utf-8"), indent=1)
    from v480_extra import expand
    for f in (mfg, comms, ecom, gap):
        a = expand(f())
        a["read"] = f"{max(4, round(words(a['body']) / 200))} min read"
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"][:50], words(a["body"]), "words", a["read"])
