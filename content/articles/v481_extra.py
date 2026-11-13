"""V4.81 long-form sections, appended to the end of each rewritten body (before Sources and Related reading)."""
from v478_articles import table

EXTRA = {}

EXTRA["shop"] = f"""
<h2>A launch checklist</h2>
{table(["Area", "Check before going live"], [
    ("Products", "Every product has your own description, at least three clear photos, price, weight and stock"),
    ("Checkout", "Place a test order end to end, including a refund"),
    ("Payments", "Payment provider set up and payouts going to the right bank account"),
    ("Shipping", "Rates for each zone you ship to; free-shipping threshold if you offer one"),
    ("Taxes", "GST/HST and provincial sales tax settings checked with your accountant"),
    ("Policies", "Returns, shipping, privacy and terms pages published and linked in the footer"),
    ("Mobile", "Home, product and checkout pages tested on a phone, on mobile data"),
    ("Search", "Page titles and descriptions written; store connected to Google Search Console"),
    ("Measurement", "Analytics working; UTM links on every social post and ad"),
])}
<h2>Alternatives worth comparing</h2>
<p>The Lovable route is one of several ways to get a Shopify store online. A standard Shopify theme, free or paid, is still the most common choice, and it is the easiest to maintain because the theme developer handles updates. Shopify's own editor and built-in AI writing tools can draft product text without a separate subscription. Website builders such as Wix and Squarespace include e-commerce in their plans and suit businesses whose site is mainly about services with a small shop on the side. For a business that already has a custom website, a Shopify "Buy Button" can add checkout to existing pages. The right choice depends less on the tool than on who will maintain the store a year from now.</p>
<h2>Our view</h2>
<p>The integration is a genuine shortcut for getting a presentable store in front of customers quickly, and that has real value for testing ideas. It does not remove the work that makes a store succeed: a product people want, honest and useful product pages, fair shipping, and steady marketing. Use it to start fast, and plan from day one how the store will be maintained once it is earning money.</p>
"""

EXTRA["sales"] = f"""
<h2>Qualifying questions that save time</h2>
<p>Qualifying early stops salespeople spending weeks on deals that were never going to close. Simple frameworks such as BANT (budget, authority, need, timing) are a useful starting point; adapt the questions to how your customers buy.</p>
{table(["Topic", "Question to ask", "What a good answer sounds like"], [
    ("Need", "What problem are you trying to solve, and what happens if you do nothing?", "A specific problem with a cost or deadline attached"),
    ("Decision", "Who else is involved in choosing, and how will the decision be made?", "Named people and a clear process"),
    ("Budget", "Have you set aside funds, or does this need approval?", "A budget range or a known approval route"),
    ("Timing", "When do you need this in place, and why then?", "A date tied to an event, such as a shutdown or a season"),
    ("Fit", "What would make this project a success for you?", "Measurable success criteria you can meet"),
])}
<h2>The hand-off between marketing and sales</h2>
<p>Many leads are lost in the gap between marketing and sales. Agree in writing what counts as a lead ready for sales (for example, a quote request, or a contact from a target industry who has downloaded a guide and visited the pricing page), how fast sales will respond, and what happens to leads that are not ready yet. Review together each month how many leads were passed over and how many became qualified opportunities. See <a href="../post/from-creation-to-conversion-measuring-the-success-of-your-content-marketing-strategy.html">measuring content performance</a> for the marketing side.</p>
<h2>A 30-minute weekly pipeline review</h2>
<ol>
<li><strong>New this week (5 minutes):</strong> leads and opportunities added, by source.</li>
<li><strong>Deals that moved (10 minutes):</strong> what advanced or was won, and what helped.</li>
<li><strong>Deals that stalled (10 minutes):</strong> anything with no activity for two weeks; agree a next step or close it as lost.</li>
<li><strong>Forecast (5 minutes):</strong> weighted pipeline against target for the month and quarter.</li>
</ol>
<p>Keep the meeting about decisions and next steps, not reading out the CRM. Over time, the stalled-deal discussion is where most of the process improvements come from.</p>
"""

EXTRA["innov"] = f"""
<h2>A simple idea log</h2>
<p>An idea log keeps suggestions visible and makes sure each one gets a decision. A spreadsheet or a shared board is enough.</p>
{table(["Idea", "Raised by", "Problem it solves", "Cheapest test", "Decision", "Owner and date"], [
    ("Online booking for service visits", "Service coordinator", "Phone tag with customers to schedule", "Booking link for one technician for a month", "Test", "Service lead, end of month"),
    ("Reusable crates for local deliveries", "Driver", "Packaging cost and waste", "Ten crates with two customers", "Test", "Operations, six weeks"),
    ("New product colour range", "Sales", "Customer requests", "Show samples to five customers", "Park until spring", "Sales manager"),
])}
<h2>Measuring whether it is working</h2>
{table(["Measure", "Why it helps"], [
    ("Ideas raised per quarter, and by whom", "Shows whether people across the business feel able to contribute"),
    ("Share of ideas that get a decision within a month", "Shows whether ideas are taken seriously"),
    ("Experiments run per quarter", "Measures learning activity, not just talk"),
    ("Revenue or savings from ideas launched in the last two years", "Links innovation to results over a realistic period"),
])}
<p>Avoid judging the programme on a single big win. Most value comes from many small, tested improvements, and a few experiments that fail cheaply are a sign the process is working.</p>
<h2>Common traps</h2>
<ul>
<li><strong>Brainstorming without a problem.</strong> Idea sessions without a clear question produce lists that go nowhere.</li>
<li><strong>The loudest voice wins.</strong> Have people write ideas down individually before discussing them.</li>
<li><strong>Testing too late.</strong> Spending months polishing an idea before any customer has seen it.</li>
<li><strong>No follow-through.</strong> People stop suggesting ideas once they see that nothing happens to them.</li>
</ul>
<p>The fix for most of these is a small, steady routine rather than a big programme: a clear problem to work on, a short time each month to review ideas, a cheap test for the promising ones, and a visible record of what was decided and why.</p>
"""

EXTRA["agile"] = f"""
<h2>Agility and efficiency: the trade-off</h2>
<p>Some agility costs money: a second supplier may be a little dearer, spare capacity sits idle in quiet weeks, and cross-training takes people off the line. The aim is not maximum flexibility but enough to handle the disruptions you are likely to face. A useful test is to list your last three disruptions, estimate what each cost in lost sales, overtime or expediting, and compare that with the cost of the lever that would have softened it. Often the cheapest levers, such as cross-training, faster decisions and shared forecasts with suppliers, pay for themselves after one event.</p>
<h2>A 90-day agility plan</h2>
{table(["Weeks", "Focus", "Output"], [
    ("1–2", "Review recent disruptions and their cost", "A short list of the risks that matter most"),
    ("3–4", "Build the skills matrix and supplier risk list", "Gaps where one person or one supplier could stop work"),
    ("5–8", "Cross-train for the two biggest skill gaps; find second sources for the riskiest items", "Training plan under way; quotes from alternative suppliers"),
    ("9–10", "Shorten one lead time: a changeover, a batch size or an approval step", "A measured improvement at one step"),
    ("11–12", "Set up a weekly scorecard and decision meeting", "A routine that spots change early and acts on it"),
    ("13", "Review results and choose the next levers", "The next 90-day plan"),
])}
<h2>Signs your operation is not agile enough</h2>
<ul>
<li>Urgent orders are handled by expediting and overtime every time.</li>
<li>One absence stops a process for a day or more.</li>
<li>Decisions wait for a monthly meeting or for one person to return.</li>
<li>A single supplier failure delays most of your orders.</li>
<li>You find out about a drop in demand from the month-end accounts.</li>
</ul>
<h2>Where technology helps</h2>
<p>Agility depends on seeing change early and acting on it quickly, and simple systems help with both. An ERP or inventory system that shows orders, stock and capacity in one place lets a planner answer "can we take this order?" in minutes rather than days. Shared forecasts with key suppliers, even a monthly spreadsheet, give them time to react. Automating routine data entry frees people to deal with exceptions. Technology does not create agility on its own, though: it speeds up decisions only when people have the authority and the habit of making them. See <a href="../post/top-10-inventory-management-software-a-comprehensive-comparison-guide.html">inventory management software</a> and <a href="../post/sales-and-operations-planning-for-small-manufacturers.html">sales and operations planning</a> for more.</p>
"""

EXTRA["lean"] = f"""
<h2>Lean outside the factory</h2>
<p>The same thinking works in offices and service businesses, where the "product" is a quote, an invoice, a claim or a patient visit. The wastes look different but are just as common.</p>
{table(["Office process", "Typical waste", "Lean fix"], [
    ("Quoting", "Waiting for pricing approval; re-keying data from email", "Pricing rules with authority limits; a quote template linked to the CRM"),
    ("Invoicing", "Errors from manual entry; invoices waiting for month-end", "Invoice from the shipping record; invoice daily"),
    ("Purchasing", "Several approvals for small items; chasing suppliers", "Approval limits by value; a reorder point for common items"),
    ("Onboarding staff", "Equipment and access not ready on day one", "A standard checklist started when the offer is accepted"),
])}
<h2>Common reasons Lean efforts stall</h2>
<ul>
<li><strong>Tools without purpose:</strong> 5S or kanban introduced because they are "Lean", not to solve a known problem.</li>
<li><strong>No time for improvement:</strong> people are expected to improve on top of a full workload.</li>
<li><strong>Using Lean to cut jobs:</strong> once people fear that ideas cost them their jobs, the ideas stop.</li>
<li><strong>Not sustaining:</strong> improvements slip back without standard work and regular checks.</li>
</ul>
<p>Leaders keep Lean alive by visiting the work regularly, asking questions rather than giving answers, and protecting time for improvement.</p>
"""
