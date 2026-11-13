"""V4.79: 2022–2023 posts rewritten or retired (audit plan V8). Rewrites keep their address and original publish date.

Rewritten:
1. introduction-to-leads-to-cash-for-saas-self-serve-model                 lead-to-cash, for any business, with a SaaS section
2. physical-servers-vs-cloud-servers-which-is-better-for-digitizing-your-data   on-premises vs cloud in 2026, five-year cost
3. how-to-build-a-predictable-and-scalable-sales-model-lessons-from-predictable-revenue-by-aaron-ros   book review in our words

Retired (their topics are covered by sections added elsewhere):
- alignment-business-needs, achieving-organizational-excellence-with-the-organizational-performance-system-ops
    -> effective-communication-of-goals-and-performance (new section in v476_articles.com: "Aligning work with what the business needs")
- navigating-change-implementing-digital-technology-with-effective-change-management
    -> change-management-toolkit-... (AI and data section widened to digital technology, v473b_inplace.py)
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, MUTED, LINE, SAND, PALE, GREENF, ORANGEF
from v478_articles import src, rel, money, table, words, art, steps_fig

L2C = "introduction-to-leads-to-cash-for-saas-self-serve-model"
SRV = "physical-servers-vs-cloud-servers-which-is-better-for-digitizing-your-data"
PR = "how-to-build-a-predictable-and-scalable-sales-model-lessons-from-predictable-revenue-by-aaron-ros"
COM = "effective-communication-of-goals-and-performance"
TOOLKIT = "change-management-toolkit-the-top-10-models-and-how-to-choose-the-right-one-for-your-organization"
RETIRE = {COM: ["alignment-business-needs", "achieving-organizational-excellence-with-the-organizational-performance-system-ops"],
          TOOLKIT: ["navigating-change-implementing-digital-technology-with-effective-change-management"]}
ORIGINAL = {L2C: "2023-03-11", SRV: "2023-03-12", PR: "2023-03-20"}


# ═════════════════════════ 1. Lead to cash ═════════════════════════
def fig_l2c():
    return steps_fig([("Lead", ["Enquiry or", "trial sign-up"]), ("Qualify", ["Fit, need,", "budget, timing"]), ("Quote", ["Price, terms,", "approval"]),
                      ("Order", ["Contract or PO;", "set up account"]), ("Deliver", ["Ship, install,", "or provision"]), ("Invoice", ["Accurate,", "on time, with", "right terms"]),
                      ("Cash", ["Collect and", "apply payment;", "follow up"])],
                     "The lead-to-cash process in seven steps: lead, from an enquiry, web form or trial sign-up; qualify for fit, need, budget and "
                     "timing; quote with price, terms and approval; order through a contract or purchase order and account set-up; deliver by "
                     "shipping, installing or provisioning; invoice accurately, on time and on the right terms; and collect cash, apply the payment "
                     "and follow up.")


FUNNEL_SAAS = [("Trial sign-ups", 1200), ("Activated (completed setup)", 540), ("Converted to paid", 108), ("Still paying after 12 months", 81)]


def l2c():
    leaks = [("Lead", "Enquiries not logged or answered late", "Response within one working day; every lead in the CRM"),
             ("Qualify", "Time spent on poor-fit prospects", "Agreed qualifying questions; disqualify early and politely"),
             ("Quote", "Slow quotes; prices or terms wrong", "Price list and templates; approval only above a threshold"),
             ("Order", "Order details re-keyed; missing information", "Quote converts to order in one system; required fields"),
             ("Deliver", "Dates missed; partial shipments not communicated", "Realistic promise dates; automatic shipping notices"),
             ("Invoice", "Invoices late, wrong or disputed", "Invoice on shipment or milestone automatically; match to PO"),
             ("Cash", "Slow collection; payments not applied", "Clear terms, reminders before and after due date, online payment")]
    rates = [FUNNEL_SAAS[i][1] / FUNNEL_SAAS[i - 1][1] for i in range(1, len(FUNNEL_SAAS))]
    body = f"""
<p>Lead-to-cash is the end-to-end process that turns interest into money in the bank: capturing a lead, qualifying it, quoting, taking the order, delivering, invoicing and collecting payment. It crosses marketing, sales, operations and finance, which is exactly why it leaks. Each team optimizes its own part, and the hand-offs between them lose time, information and sometimes the customer. This article was first written in 2023 about software companies that sell online without salespeople. It has been rewritten for any small or mid-sized business, with a section on that self-serve software model and a worked example.</p>
<h2>The seven steps</h2>
{fig(fig_l2c(), 1, "Lead-to-cash runs from first interest to payment received, across several teams.")}
<p>Some companies split it into two linked processes: lead-to-order (marketing and sales) and order-to-cash (operations and finance). Looking at the whole chain matters because a decision in one part, such as non-standard payment terms agreed to win a deal, creates work and delay in another.</p>
<h2>Where the process usually leaks</h2>
{table(["Step", "Common leak", "Typical fix"], leaks)}
<h2>Measures for the whole chain</h2>
{table(["Measure", "What it tells you"], [
    ("Lead response time", "How quickly a new enquiry gets a real reply"),
    ("Lead-to-order conversion", "Share of qualified leads that become orders"),
    ("Quote turnaround", "Days from request to quote sent"),
    ("Order-to-invoice time", "Days from delivery to invoice; any gap is free credit to the customer"),
    ("Invoice accuracy", "Share of invoices not disputed or corrected"),
    ("Days sales outstanding (DSO)", "How long customers take to pay"),
    ("Lead-to-cash cycle time", "Days from first enquiry to payment received"),
])}
<h2>Worked example: a distributor's order-to-cash</h2>
<p>A distributor ships orders on the day they are packed, but invoices are raised in a weekly batch by the office, and statements go out monthly. Mapping the process shows invoices are issued an average of 4 days after shipment and customers pay, on average, 41 days after invoice. Two changes follow: invoices are created automatically when the shipment is confirmed in the system, and a polite reminder goes out five days before the due date with an online payment link. Days from shipment to cash fall from about 45 to about 34. On annual sales of $6 million, cutting 11 days frees roughly {money(6_000_000 / 365 * 11)} of cash that was sitting with customers. The figures are illustrative.</p>
<h2>The self-serve software model</h2>
<p>Software-as-a-service companies that sell online without salespeople run the same chain, but most steps are automated and the customer moves through it alone: sign up for a trial, set the product up, choose a plan, pay by card, and renew. The leaks are in activation and retention rather than in quoting and invoicing. A simple example, with illustrative numbers:</p>
{table(["Stage", "Customers", "Conversion from previous stage"], [(n, f"{c:,}", f"{rates[i - 1]:.0%}" if i else "—") for i, (n, c) in enumerate(FUNNEL_SAAS)])}
<p>Here the biggest loss is between sign-up and activation: more than half of trial users never complete setup, so they never see the value. Better onboarding (a guided first task, a short email sequence, a check-in at day three) usually does more for revenue than more sign-ups. After that, failed card payments and silent churn matter: automatic retries, reminders before a card expires and a quick check-in when usage drops all keep cash coming in.</p>
<h2>Systems that support lead-to-cash</h2>
<p>Most small businesses run lead-to-cash across a CRM, an accounting package and sometimes an ERP or e-commerce platform. The goal is to enter each piece of information once and let it flow: the CRM quote becomes the order, the order drives shipping, shipping triggers the invoice, and the payment updates the customer's record. Where systems do not connect, an integration often pays back quickly; see <a href="../post/decoding-the-mysteries-of-api-architecture-a-software-designer-s-guide.html">APIs for small businesses</a> and <a href="../post/choosing-the-right-crm-system-how-to-make-the-best-choice-for-your-business.html">choosing a CRM</a>.</p>
<h2>How to improve it</h2>
<ol>
<li><strong>Map the full chain</strong> with one person from each team, using a swim lane map so hand-offs are visible.</li>
<li><strong>Measure cycle time</strong> for a sample of recent orders, from enquiry to payment.</li>
<li><strong>Fix the longest wait first,</strong> which is often invoicing delay or slow quotes, not selling.</li>
<li><strong>Agree rules across teams,</strong> such as standard payment terms and who can approve exceptions.</li>
<li><strong>Review the measures monthly</strong> in one meeting with sales, operations and finance together.</li>
</ol>
"""
    r = [("how-to-perform-a-successful-business-process-optimization", "Business process optimization: map, measure, redesign"),
         ("6-essential-steps-to-streamline-and-enhance-your-sales-process", "Six steps to streamline your sales process"),
         ("essentials-of-effective-process-documentation", "Process documentation, with a quote-to-order swim lane")]
    return art(L2C, "Lead-to-Cash: Mapping and Improving the Process from Enquiry to Payment",
               "The seven steps of lead-to-cash, where the process leaks, measures for the whole chain, a cash-flow worked example, and the self-serve SaaS version.",
               ["process-improvement", "marketing"], ["lead to cash", "order to cash", "sales process", "DSO", "SaaS", "process mapping"], body, "Process", r)


# ═════════════════════════ 2. Servers vs cloud ═════════════════════════
SRV_HW, SRV_LIC, SRV_IT, SRV_POWER, SRV_BACKUP = 14_000, 4_000, 6_000, 600, 1_500
CLOUD_MO, CLOUD_IT, MIGRATE = 900, 2_500, 6_000
ONPREM5 = SRV_HW + SRV_LIC + 5 * (SRV_IT + SRV_POWER + SRV_BACKUP)
CLOUD5 = MIGRATE + 5 * (CLOUD_MO * 12 + CLOUD_IT)


def srv():
    comp = [("Up-front cost", "Hardware and licences bought at the start", "Little or none; pay monthly"),
            ("Running cost", "Power, cooling, maintenance, IT support, backups", "Subscription; grows with use"),
            ("Control", "Full control of hardware, software and data location", "Provider runs the infrastructure; you control configuration and data"),
            ("Security", "Your responsibility, end to end", "Shared: provider secures the platform; you secure accounts, data and settings"),
            ("Remote access", "Needs VPN or remote desktop set up and secured", "Built in, from anywhere"),
            ("Scaling", "Buy more hardware", "Add capacity in minutes"),
            ("Backups and recovery", "You design and test them", "Options built in, but still your job to configure and test"),
            ("Internet dependence", "Works on the local network if the internet is down", "Needs reliable internet"),
            ("Specialized software", "Runs anything, including old or plant-floor software", "Some older or machine-connected software may not move easily")]
    body = f"""
<p>Should a small business keep its own server in the back room or move to the cloud? In 2023, when this article was first written, the answer was already shifting toward cloud services for most office work. In 2026 the question is usually narrower: which workloads still need a local server, and what is the cheapest safe way to run the rest. This rewrite adds a five-year cost example and a note on Windows Server support dates that affect many small businesses this year.</p>
<h2>What we mean by each</h2>
<ul>
<li><strong>On-premises (physical) server:</strong> a computer you own, in your building, running files, accounting, email or line-of-business software.</li>
<li><strong>Cloud services:</strong> software and storage run by a provider and used over the internet. For small businesses this usually means software-as-a-service, such as Microsoft 365, Google Workspace, cloud accounting and cloud ERP, rather than renting virtual servers.</li>
<li><strong>Hybrid:</strong> most work in the cloud, with a small local server or device for software or equipment that must stay on site.</li>
</ul>
<h2>Side by side</h2>
{table(["", "On-premises server", "Cloud services"], comp)}
<h2>A deadline many small businesses face</h2>
<p>Microsoft ends extended support for Windows Server 2016 on January 12, 2027; after that, security updates are available only through a paid Extended Security Updates program. Windows Server 2019 follows on January 9, 2029. If your office server runs 2016, now is the natural time to decide whether to replace it, upgrade it, or move its work to the cloud, rather than buying new hardware out of habit.</p>
<h2>Worked example: five-year cost</h2>
<p>A 15-person firm compares replacing its file and accounting server with moving files to cloud storage and accounting to a cloud package. All figures are illustrative; get quotes for your own situation.</p>
{table(["Cost", "New on-premises server", "Cloud services"], [
    ("Hardware", money(SRV_HW), "—"), ("Server and user licences", money(SRV_LIC), "Included"),
    ("Migration and set-up", "Included in IT support", money(MIGRATE)),
    ("Subscriptions per year", "—", money(CLOUD_MO * 12)),
    ("IT support per year", money(SRV_IT), money(CLOUD_IT)),
    ("Power and cooling per year", money(SRV_POWER), "—"),
    ("Backup service per year", money(SRV_BACKUP), "Included in subscriptions"),
    ("<strong>Five-year total</strong>", f"<strong>{money(ONPREM5)}</strong>", f"<strong>{money(CLOUD5)}</strong>"),
])}
<p>On these figures the new server is cheaper over five years, by about {money(CLOUD5 - ONPREM5)}. That is common for a small, stable office. The decision usually turns on what the extra cloud cost buys: access from anywhere, no single server whose failure stops the office, less IT effort, and no hardware to replace in five years; against that, whether any software must stay local. Note that the cloud subscription grows with users, while the server cost is largely fixed until the next replacement.</p>
<h2>When a local server still makes sense</h2>
<ul>
<li>Software that controls or collects data from machines on the shop floor.</li>
<li>Very large files, such as CAD models or video, with a slow internet connection.</li>
<li>Older line-of-business software with no cloud version, until it is replaced.</li>
<li>Strict contractual or regulatory requirements on where data is held, where a cloud region in Canada does not meet them.</li>
<li>Sites with unreliable internet that must keep working offline.</li>
</ul>
<h2>Making the move safely</h2>
<ol>
<li><strong>Inventory what the server does:</strong> files, applications, printers, user accounts, scheduled jobs.</li>
<li><strong>Clean up first:</strong> archive old files and remove unused applications; do not migrate clutter.</li>
<li><strong>Choose data location deliberately:</strong> major providers offer Canadian data centres; select them if customers or contracts expect it.</li>
<li><strong>Turn on multi-factor authentication</strong> for every cloud account before moving data.</li>
<li><strong>Set up backups for cloud data too.</strong> Providers keep services running, but recovering deleted or encrypted files is often your responsibility.</li>
<li><strong>Move in stages,</strong> one workload at a time, and keep the old server read-only for a few weeks.</li>
</ol>
<p>Whichever route you choose, the security basics in our <a href="../post/cybersecurity-for-small-businesses-tips-and-best-practices.html">cybersecurity guide</a> apply.</p>
"""
    r = [("cybersecurity-for-small-businesses-tips-and-best-practices", "Cybersecurity for small businesses: the 13 baseline controls"),
         ("understanding-erp-vs-mrp-a-comprehensive-comparison-of-manufacturing-systems", "ERP vs MRP"),
         ("the-iot-revolution-how-connected-devices-are-transforming-industries", "Industrial IoT for small manufacturers")]
    s = [("endoflife.ai: Windows Server 2016 end of life, ESU and upgrades", "https://endoflife.ai/article-windows-server-2016-eol"),
         ("Microsoft Q&amp;A: End of support for Windows Server 2016 and 2019", "https://learn.microsoft.com/en-us/answers/a/1973922")]
    return art(SRV, "On-Premises Server or Cloud? A 2026 Guide for Small Businesses",
               "On-premises servers versus cloud services for small businesses in 2026: a side-by-side comparison, the Windows Server 2016 deadline, a five-year cost example and how to move safely.",
               ["digital-technology"], ["cloud", "servers", "Microsoft 365", "Windows Server 2016", "IT", "small business IT"], body, "Cloud", r, s)


# ═════════════════════════ 3. Predictable Revenue ═════════════════════════
def fig_roles():
    return steps_fig([("Marketing", ["Generates inbound", "leads"]), ("Qualifying", ["Responds to inbound;", "qualifies"]),
                      ("Prospecting", ["Researches and", "contacts targets"]), ("Closing", ["Account executives", "run the sale; close"]),
                      ("Customer success", ["Onboard, retain,", "grow accounts"])],
                     "The specialized sales roles described in Predictable Revenue: marketing generates inbound leads; a lead qualification role "
                     "responds to inbound leads and qualifies them; an outbound prospecting role researches and contacts target accounts; account "
                     "executives run the sales conversation and close; customer success onboards, retains and grows accounts.")


def pr():
    adapt = [("1. Separate prospecting from closing", "Even with one or two salespeople, block fixed time for prospecting so it is not squeezed out by closing work"),
             ("2. Define your ideal customer", "Industry, size, location, trigger events; write it down and use it to choose targets"),
             ("3. Send short, specific outreach", "A brief message to the right role asking who handles a specific problem, not a long pitch"),
             ("4. Measure the pipeline in numbers", "New conversations, qualified opportunities, proposals and wins per month; work backward from the revenue target"),
             ("5. Hand over and follow through", "Clear criteria for passing a lead on; customer success owns retention and growth after the sale")]
    body = f"""
<p><cite>Predictable Revenue</cite> by Aaron Ross and Marylou Tyler, first published in 2011, describes how a sales team at Salesforce.com built a repeatable way of generating new business. It became one of the most influential sales books of the last fifteen years, especially among software companies. This review, rewritten in our own words from an earlier summary on this site, explains the book's main ideas, where they apply outside software, and what has changed since it was written. It is a review, not a substitute for reading the book.</p>
<h2>The core idea: specialize the sales roles</h2>
<p>The book's central argument is that one salesperson should not be expected to find prospects, qualify them, close deals and look after customers. Each of those jobs needs different skills and gets crowded out by the others, usually with prospecting losing first. Splitting them into specialized roles makes each step measurable and the whole pipeline more predictable.</p>
{fig(fig_roles(), 1, "The specialized roles at the heart of the book's model.")}
<h2>Other key ideas</h2>
<ul>
<li><strong>Outbound prospecting without cold calling.</strong> The book popularized short, targeted emails to senior people asking who in their organization handles a specific issue, followed by a conversation, in place of unannounced calls.</li>
<li><strong>Three kinds of lead generation.</strong> The authors distinguish broad inbound marketing, referrals and community; targeted outbound prospecting; and one-to-many campaigns, and argue that a predictable pipeline needs targeted outbound work alongside the other two.</li>
<li><strong>A pipeline you can calculate.</strong> When each role has clear inputs and conversion rates, you can estimate how many prospects you need to hit a revenue target, and see quickly which step is failing.</li>
<li><strong>The ideal customer profile.</strong> Focusing on companies most likely to buy and succeed makes outreach efficient and keeps customers longer.</li>
</ul>
<h2>Does it apply to a small business outside software?</h2>
<p>A small engineering firm, distributor or manufacturer rarely has enough people for five separate sales roles. The underlying lessons still transfer well:</p>
{table(["Lesson", "How to apply it with a small team"], adapt)}
<h2>A worked pipeline calculation</h2>
<p>A firm wants 12 new customers a year. From its own records, it wins 1 in 3 proposals, sends a proposal to 1 in 2 qualified opportunities, and finds 1 qualified opportunity in every 5 first conversations. Working backward: 12 wins need 36 proposals, 72 qualified opportunities and about 360 first conversations a year, or roughly 7 a week. That single number, seven first conversations a week, is easier to manage than a revenue target and shows immediately when prospecting is slipping. The figures are illustrative; use your own conversion rates.</p>
<h2>What has changed since the book</h2>
<ul>
<li><strong>Inboxes are crowded.</strong> The email approach the book made famous has been copied by many, and automated sequences have made recipients and spam filters much less forgiving. Relevance and personal research matter more than volume.</li>
<li><strong>Privacy and anti-spam rules.</strong> In Canada, commercial email is governed by Canada's anti-spam legislation (CASL), which requires consent with limited exceptions. Check how it applies before any outbound email campaign.</li>
<li><strong>AI tools.</strong> Research, drafting and follow-up are now much faster with AI, which makes the book's emphasis on specific, well-targeted outreach more important, not less.</li>
<li><strong>Customer success is mainstream.</strong> The book's point that retention and growth deserve their own role has become standard practice in subscription businesses.</li>
</ul>
<h2>Our verdict</h2>
<p><cite>Predictable Revenue</cite> is worth reading for any owner who depends on one or two people to both find and close business. The specific tactics have aged, but the discipline of separating prospecting from closing, defining the ideal customer and running the pipeline by numbers remains the most useful idea in it.</p>
"""
    r = [("6-essential-steps-to-streamline-and-enhance-your-sales-process", "Six steps to streamline your sales process"),
         ("introduction-to-leads-to-cash-for-saas-self-serve-model", "Lead-to-cash: from enquiry to payment"),
         ("choosing-the-right-crm-system-how-to-make-the-best-choice-for-your-business", "Choosing a CRM for a small business")]
    return art(PR, "Predictable Revenue by Aaron Ross and Marylou Tyler: Review and Lessons for Small Businesses",
               "A review of Predictable Revenue: specialized sales roles, outbound prospecting, pipeline math, how to apply it in a small business, and what has changed since 2011.",
               ["book-review", "marketing"], ["Predictable Revenue", "Aaron Ross", "sales model", "book review", "prospecting", "sales pipeline"], body, "Book review", r)


COM_SECTION = """<h2>Aligning work with what the business needs</h2>
<p>Goals and scorecards only help if everyday work actually serves them. A simple alignment check, done once a quarter by the leadership team, catches drift before it becomes waste:</p>
<ol>
<li><strong>List the three to five business needs</strong> for the year, such as on-time delivery, margin on new work, or cash collection.</li>
<li><strong>List the main activities and projects</strong> each team is spending time on.</li>
<li><strong>Mark each activity</strong> with the need it serves. Activities that serve none are candidates to stop or pause.</li>
<li><strong>Check the measures:</strong> each need should have at least one number on the scorecard, and every number on the scorecard should map to a need.</li>
<li><strong>Agree what to stop</strong> as well as what to start; capacity freed from low-value work is what makes new priorities possible.</li>
</ol>
<p>This is the core of any organizational performance system, whatever framework you use: a clear purpose and a few goals, measures that show progress, a regular rhythm for reviewing them, and the discipline to stop work that does not help.</p>
"""


if __name__ == "__main__":
    op = os.path.join(HERE, "original_dates.json")
    od = json.load(open(op, encoding="utf-8")); od.update(ORIGINAL)
    note = od.pop("_note"); json.dump({"_note": note, **dict(sorted(od.items()))}, open(op, "w", encoding="utf-8"), indent=1)
    for f in (l2c, srv, pr):
        a = f()
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"][:50], words(a["body"]), "words", a["read"])
    print(f"servers: on-prem {ONPREM5:,} cloud {CLOUD5:,}")
