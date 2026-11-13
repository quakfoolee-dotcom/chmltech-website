"""V4.80: extra long-form sections (anchor string, or END = before Sources/Related reading)."""
import re
from v478_extra import table

END = "END"
EXTRA = {
"customization-standardization-and-flexibility-understanding-manufacturing-principles": [
(END, """<h2>Signs your strategy no longer fits</h2>
<ul>
<li><strong>Lead times are longer than customers will accept,</strong> and you lose quotes on delivery rather than price.</li>
<li><strong>Finished stock keeps growing</strong> while you are still short of the items customers want.</li>
<li><strong>Engineering is always behind,</strong> because every order is treated as new even when it is similar to past ones.</li>
<li><strong>Expediting is daily,</strong> a sign that work is started too late in the process for the lead time you promise.</li>
<li><strong>Margins vary widely between similar jobs,</strong> often because custom work is priced like standard work.</li>
</ul>
<h2>Making the change</h2>
<ol>
<li><strong>Analyse two years of orders</strong> by product family: volume, variety, lead time quoted and achieved.</li>
<li><strong>Find the common parts and modules</strong> that appear in most orders.</li>
<li><strong>Pick the decoupling point</strong> for each family and decide which items to hold in stock and at what levels.</li>
<li><strong>Standardize the options</strong> customers can choose, and price custom work separately.</li>
<li><strong>Update the planning system:</strong> stocking rules, planning bills of materials and quoted lead times.</li>
<li><strong>Review quarterly:</strong> demand shifts, and the right decoupling point shifts with it.</li>
</ol>
"""),
],
"10-effective-communication-strategies-for-manufacturing-companies": [
(END, """<h2>What to put on a tier 1 board</h2>
""" + table(["Row", "Example content"], [
    ("Safety", "Days since last incident; today's hazard or reminder"),
    ("Quality", "Defects yesterday by type; any holds"),
    ("Delivery", "Output by hour against plan; jobs due today"),
    ("Cost", "Scrap and downtime minutes yesterday"),
    ("People", "Attendance, training, recognition"),
    ("Problems", "Open items with owner and due date; items escalated to tier 2"),
]) + """
<h2>Common mistakes</h2>
<ul>
<li>Meetings that run long because they turn into problem-solving sessions; solve offline and report back.</li>
<li>Boards updated by supervisors only, so operators do not own them.</li>
<li>Escalations that never get an answer, which quickly teaches people to stop raising issues.</li>
<li>Too many measures; five or six that matter are enough.</li>
<li>Skipping meetings on busy days, which are the days communication matters most.</li>
</ul>
"""),
],
"10-proven-ways-to-boost-traffic-to-your-ecommerce-website": [
(END, """<h2>A 90-day plan for a small store</h2>
""" + table(["When", "Focus"], [
    ("Weeks 1–2", "Set up GA4 e-commerce events and Search Console; check mobile speed; fix shipping-cost clarity at checkout"),
    ("Weeks 3–4", "Rewrite descriptions for the 20 best-selling products; add product structured data; submit a Merchant Center feed"),
    ("Month 2", "Launch welcome and abandoned-cart emails; ask recent buyers for reviews; start one social channel with a weekly rhythm"),
    ("Month 3", "Test a small paid campaign on the best-converting products; review results by channel; drop what does not convert"),
]) + """
<h2>Common mistakes</h2>
<ul>
<li>Spending on ads before the store converts the traffic it already has.</li>
<li>Copying manufacturer descriptions, which gives search engines no reason to rank your page.</li>
<li>Hiding delivery costs until the last step of checkout.</li>
<li>Judging channels by visits rather than orders and margin.</li>
<li>Ignoring existing customers, who are usually the cheapest source of the next order.</li>
</ul>
"""),
],
"bridging-the-gap-a-step-by-step-guide-to-conducting-a-gap-analysis-for-operational-efficiency": [
("<h2>Tips for a useful result</h2>", """<h2>Tools that help</h2>
""" + table(["Step", "Useful tools"], [
    ("Future state", "Customer requirements, the relevant standard's clauses, benchmarks, a target scorecard"),
    ("Current state", "Process maps, time studies, system reports, document samples, staff interviews"),
    ("Gaps and causes", "5 whys, fishbone diagram, Pareto chart of errors or delays"),
    ("Prioritization", "Impact and effort matrix, simple scoring against business goals"),
    ("Plan", "Action plan with owners and dates; a roadmap for larger projects"),
]) + """
<h2>Gap analysis and digital adoption</h2>
<p>A digital adoption plan is essentially a gap analysis for systems and data: which processes are manual, which systems do not connect, where data is re-keyed, and what technology and changes would close those gaps. The same discipline applies: define the future state in business terms first (faster quotes, fewer errors, better visibility), and only then choose the software. Starting from a product rather than a gap is the most common reason digital projects disappoint.</p>
"""),
],
}


def expand(a):
    body = a["body"]
    for anchor, html in EXTRA.get(a["slug"], []):
        if anchor == END:
            m = re.search(r"<h2>(Sources|Related reading)</h2>", body); at = m.start() if m else len(body)
        else:
            at = body.find(anchor); assert at >= 0, (a["slug"], anchor)
        body = body[:at] + html + body[at:]
    a["body"] = body
    return a
