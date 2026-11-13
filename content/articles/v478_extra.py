"""V4.78: extra long-form sections, inserted before an anchor (exact string) or before Sources/Related reading ("END")."""
import re

END = "END"


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table>\n<tr>{h}</tr>\n{b}\n</table>"


EXTRA = {
"from-creation-to-conversion-measuring-the-success-of-your-content-marketing-strategy": [
("<h2>Measuring in the age of AI answers</h2>", f"""<h2>Improving content that already ranks</h2>
<p>The fastest gains usually come from pages that already get impressions but few clicks or actions, not from new articles. In Search Console, sort pages by impressions and look for those with a low click-through rate or an average position between 5 and 20. For each, check whether the title and description match what searchers want, whether the page answers the question in the first paragraph, whether the content is current, and whether there is a clear next step such as a related guide, a template or a contact link. Updating five such pages a quarter often does more than publishing ten new ones.</p>
<h2>Who should own the numbers</h2>
<p>In a small business, one person should own the content scorecard, even if writing is shared. Their job is not to produce reports but to bring one recommendation to the monthly marketing or management meeting: which piece to improve, which to promote, which to retire, and what to write next based on the questions customers asked that month.</p>
"""),
],
"choosing-the-right-crm-system-how-to-make-the-best-choice-for-your-business": [
("<h2>Implementation in six steps</h2>", f"""<h2>What data to bring across</h2>
{table(["Data", "Bring it?", "Notes"], [
    ("Active customers and their contacts", "Yes", "Clean duplicates and update job titles first"),
    ("Open quotes and deals", "Yes", "Enter with stage, value and next step"),
    ("Leads from the last 12 to 24 months", "Usually", "Older leads rarely convert; archive the rest"),
    ("Email history", "Selectively", "Connect mailboxes going forward; import only key threads"),
    ("Old closed deals", "Summary only", "Totals by customer are enough for history"),
    ("Marketing lists", "Only with consent records", "Follow Canada's anti-spam legislation (CASL) for commercial email"),
])}
"""),
],
"5-tips-to-drive-more-website-traffic-from-instagram": [
("<h2>Common mistakes</h2>", f"""<h2>A sample month of content</h2>
{table(["Week", "Reels (reach)", "Stories (action)", "Feed post"], [
    ("1", "One tip, one behind-the-scenes clip", "Poll on a customer question; link to the related guide", "Customer result, with permission"),
    ("2", "Short how-to; quick before-and-after", "Link to booking or quote page with the month's offer", "Team member introduction"),
    ("3", "Answer a common question; myth vs fact", "Event or new service; link sticker", "Carousel: five-step checklist"),
    ("4", "Recap of the month's best tip; testimonial clip", "Last-chance reminder for the offer", "Case study summary; 'link in bio' to the full story"),
])}
<p>Batch the filming into one or two sessions a month, so posting does not depend on finding time every day.</p>
"""),
],
"the-iot-revolution-how-connected-devices-are-transforming-industries": [
("<h2>Starting small</h2>", f"""<h2>Examples by industry</h2>
{table(["Industry", "Typical first IoT project", "Measure it improves"], [
    ("Food and beverage processing", "Cold room and freezer temperature with alarms and automatic records", "Spoilage, food safety audit findings"),
    ("Metal fabrication", "Machine run signals and counts on lasers, brakes and welders", "OEE, downtime by cause"),
    ("Chemical and process plants", "Vibration on critical pumps and fans; tank levels", "Unplanned downtime, stock-outs of raw materials"),
    ("Warehousing and distribution", "Dock door, forklift battery and cold-chain monitoring", "Energy, equipment availability, product quality"),
    ("Commercial buildings", "Energy meters and HVAC sensors", "Energy cost per square metre, comfort complaints"),
    ("Agriculture and greenhouses", "Soil moisture, greenhouse climate, water use", "Water and energy per unit of output"),
])}
<h2>What it costs</h2>
<p>Costs fall into four parts: the sensors themselves, which for common measurements like temperature or current are now inexpensive; installation, which can cost more than the sensors in an existing plant; connectivity and gateways; and a software subscription, usually priced per device or per site. Ask vendors for a total three-year cost for your pilot, including installation and software, and compare it with the cost of the problem you are trying to solve.</p>
"""),
],
"the-future-of-warehousing-how-automation-technology-is-changing-the-game": [
("<h2>Questions to answer before buying</h2>", f"""<h2>A roadmap for a growing distributor</h2>
{table(["Stage", "Typical volume", "Investments"], [
    ("Getting control", "Up to a few hundred order lines a day", "Inventory system or WMS, barcode labels and scanners, labelled locations, cycle counting"),
    ("Getting faster", "Several hundred to a few thousand lines a day", "Slotting by velocity, batch and zone picking, pick carts, mobile printers, pick-to-light for fast movers"),
    ("Scaling labour", "Thousands of lines a day, labour hard to hire", "Collaborative mobile robots, conveyor to packing, automated packing aids"),
    ("Dense and fast", "High volume of small items, space constrained", "Goods-to-person storage, sortation"),
])}
<h2>Leasing, subscription or purchase</h2>
<p>Robots-as-a-service subscriptions let you start with a small fleet, add units for peak season and avoid a large capital outlay, at a higher cost over many years. Purchase suits stable, predictable volumes and businesses that can maintain equipment. Fixed systems such as goods-to-person storage are almost always capital projects and need a longer planning horizon, so check your lease, building and growth plans before committing.</p>
<h2>Safety and people</h2>
<p>Automation changes how people and machines share space. Update traffic plans, train staff on how robots behave and how to stop them, and review your health and safety program with your provincial requirements in mind. Pickers who move to robot supervision, exception handling or quality checks are often the best source of improvement ideas for the new system.</p>
"""),
],
"analyzing-tesla-s-business-model-canvas-how-the-company-drives-sustainable-innovation": [
("<p>To build your own canvas,", f"""<h2>Build your own canvas in five steps</h2>
{table(["Step", "What to do"], [
    ("1. Customers", "List your three most profitable customer groups and what each is trying to get done"),
    ("2. Value", "For each group, write the one thing you do better than the alternatives"),
    ("3. Channels and relationships", "How each group finds you, buys from you and stays in touch"),
    ("4. Engine", "Key activities, resources and partners that deliver the value; and the costs they drive"),
    ("5. Money", "Revenue by stream; check which customers and activities actually make the margin"),
])}
"""),
],
"how-chatgpt-can-help-small-businesses-improve-customer-service-and-streamline-operations": [
("<h2>How to start</h2>", f"""<h2>Measuring service quality before and after</h2>
{table(["Measure", "What it shows"], [
    ("First response time", "How long customers wait for an initial reply"),
    ("Average handling time", "Staff time per enquiry; where AI drafts save most"),
    ("First contact resolution", "Share solved without a follow-up"),
    ("Customer satisfaction (CSAT)", "Whether faster replies are also good replies"),
    ("Escalation rate", "How often AI or staff hand over to a specialist"),
    ("Error rate in a weekly sample", "Wrong or incomplete answers found in review"),
])}
<h2>Choosing tools</h2>
<p>There are two routes. Help desk platforms such as Zendesk, Freshdesk, HubSpot Service Hub or Zoho Desk now include AI drafting, triage and chat that work on your tickets and knowledge base directly; they are the easiest route for a team that already uses one. General assistants such as ChatGPT, Claude or Microsoft Copilot are flexible for drafting and summarizing but need careful handling of customer data and do not see your order system unless connected. For most small teams, AI inside the help desk or CRM you already use is the right first step.</p>
"""),
],
"the-future-of-ai-new-opportunities-and-jobs": [
("<h2>For individuals</h2>", f"""<h2>How AI is changing work in four sectors</h2>
{table(["Sector", "Tasks changing first", "Where people stay essential"], [
    ("Manufacturing", "Production reports, maintenance records, quality documentation, scheduling suggestions", "Running and fixing equipment, problem solving on the floor, safety"),
    ("Professional services", "Research, first drafts, document review, meeting notes", "Client judgement, accountability, relationships"),
    ("Retail and distribution", "Product descriptions, demand forecasts, customer email", "Store and warehouse operations, supplier relationships"),
    ("Health and care", "Clinical notes, scheduling, coding and billing", "Patient care, diagnosis, empathy"),
])}
<h2>Questions staff ask, and honest answers</h2>
<ul>
<li><strong>"Will AI replace my job?"</strong> In most small businesses, AI changes parts of jobs. Where a role is mainly routine data handling, it will change most, and the business should plan that change with the person.</li>
<li><strong>"Can I use AI tools for my work?"</strong> Yes, within the company's policy on approved tools and data.</li>
<li><strong>"Who is responsible if the AI is wrong?"</strong> The person and the business that use it, which is why output is checked before it reaches customers.</li>
<li><strong>"Will I get training?"</strong> It should be part of the plan; employers that train staff get far more value from the tools.</li>
</ul>
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
