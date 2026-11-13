"""V4.78: 2021–2025 digital and marketing posts rewritten in our own words as long-form guides (audit plan V8).
Each keeps its address and its original publish date (content/articles/original_dates.json).

1. from-creation-to-conversion-measuring-the-success-of-your-content-marketing-strategy   measuring content
2. choosing-the-right-crm-system-how-to-make-the-best-choice-for-your-business             choosing a CRM
3. 5-tips-to-drive-more-website-traffic-from-instagram                                     Instagram and social media
     retired into it: how-to-effectively-use-social-media-to-improve-business-visibility-and-attract-customers (2025)
4. the-iot-revolution-how-connected-devices-are-transforming-industries                    IoT for small manufacturers
5. the-future-of-warehousing-how-automation-technology-is-changing-the-game                 warehouse automation
6. analyzing-tesla-s-business-model-canvas-how-the-company-drives-sustainable-innovation     Tesla case study
     retired into it: the-driving-force-behind-tesla-s-operational-efficiency-under-elon-musk-s-leadership (2024)
7. how-chatgpt-can-help-small-businesses-improve-customer-service-and-streamline-operations  AI in customer service
8. the-future-of-ai-new-opportunities-and-jobs                                             AI and jobs in Canada

Usage:  python3 content/articles/v478_articles.py
        python3 content/gen/refresh_article.py <slug>                 (each of the eight)
        python3 content/gen/refresh_article.py --retire <old> <new>   (the two retired posts)
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, MUTED, LINE, SAND, PALE, GREENF, ORANGEF

DATE = "2026-11-13"
CM = "from-creation-to-conversion-measuring-the-success-of-your-content-marketing-strategy"
CRM = "choosing-the-right-crm-system-how-to-make-the-best-choice-for-your-business"
IG = "5-tips-to-drive-more-website-traffic-from-instagram"
IOT = "the-iot-revolution-how-connected-devices-are-transforming-industries"
WH = "the-future-of-warehousing-how-automation-technology-is-changing-the-game"
TS = "analyzing-tesla-s-business-model-canvas-how-the-company-drives-sustainable-innovation"
CS = "how-chatgpt-can-help-small-businesses-improve-customer-service-and-streamline-operations"
JOBS = "the-future-of-ai-new-opportunities-and-jobs"
RETIRE = {IG: ["how-to-effectively-use-social-media-to-improve-business-visibility-and-attract-customers"],
          TS: ["the-driving-force-behind-tesla-s-operational-efficiency-under-elon-musk-s-leadership"]}
ORIGINAL = {CM: "2023-03-10", CRM: "2023-03-11", IG: "2023-03-31", IOT: "2023-03-31", WH: "2023-04-07", TS: "2023-03-18", CS: "2023-03-11", JOBS: "2023-04-23"}


def src(items):
    return "<h2>Sources</h2><ul>" + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in items) + "</ul>"


def rel(items):
    return "<h2>Related reading</h2><ul>" + "".join(f'<li><a href="../post/{s}.html">{t}</a></li>' for s, t in items) + "</ul>"


def money(x):
    return f"${x:,.0f}"


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table>\n<tr>{h}</tr>\n{b}\n</table>"


def words(html):
    return len(re.sub(r"<svg.*?</svg>|<[^>]+>", " ", html, flags=re.S).split())


def art(slug, title, desc, cats, tags, body, label, related, sources=None):
    body = body + (src(sources) if sources else "") + rel(related)
    return dict(slug=slug, title=title, desc=desc, cats=cats, tags=tags, body=body.strip(), date=DATE, author="Quak Foo Lee",
                read=f"{max(4, round(words(body) / 200))} min read", cover_label=label, related=[r for r, _ in related])


def steps_fig(items, label, w=742):
    s = DEFS; n = len(items); bw = (w - 20 - (n - 1) * 16) / n
    for i, (h, lines) in enumerate(items):
        x = 10 + i * (bw + 16)
        s += box(x, 12, bw, 38, h, fill=NAVY, stroke=NAVY, tc="#fff", fs=13)
        s += box(x, 56, bw, 62, lines, fill=PALE, stroke="#9AB0C8", fs=11.8, bold=False)
        if i < n - 1: s += arrow(x + bw + 2, 31, x + bw + 14, 31)
    return svg(label, w, 128, s, 600)


# ═════════════════════════ 1. Measuring content ═════════════════════════
CONTENT = [("Guide: sizing a pump", 2600, 0.71, 14, 9), ("Guide: ISO 9001 for SMEs", 1900, 0.64, 11, 6), ("News: Budget 2026", 1400, 0.48, 2, 1),
           ("Case study: OEE project", 520, 0.69, 8, 5), ("List: 10 productivity tips", 1100, 0.31, 0, 0)]


def cm():
    rows = [(n, f"{v:,}", f"{e:.0%}", k, q, f"{k / v * 1000:.1f}") for n, v, e, k, q in CONTENT]
    funnel = [("Reach", "Are the right people finding it?", "Search impressions and clicks, sessions from search, new users", "Search Console, GA4"),
              ("Engagement", "Do they read it?", "Engaged sessions, engagement rate, scroll to 75%, average engagement time", "GA4"),
              ("Action", "Do they take the next step?", "Downloads, newsletter sign-ups, contact forms, calls (key events)", "GA4"),
              ("Business result", "Does it lead to revenue?", "Qualified leads, proposals and wins that touched the content", "CRM"),
              ("Reputation", "Does it build authority?", "Links from other sites, mentions, citations in AI answers, shares", "Search Console, alerts, manual checks")]
    body = f"""
<p>Content marketing (articles, guides, case studies, videos, templates) only earns its cost if it brings the right people to your business and helps some of them become customers. Measuring it does not need expensive tools. It needs a clear idea of what each piece is for, a few measures that match that purpose, and a monthly habit of looking at them. This article, first written in 2023, has been rewritten for Google Analytics 4 and for a search landscape where AI answers increasingly sit between your content and your readers.</p>
<h2>Start with the job each piece of content does</h2>
<p>A guide written to attract engineers searching for a calculation method should be judged on search traffic and how long people stay. A case study written to reassure buyers late in a decision should be judged on whether it is viewed before enquiries and proposals. Judging both by page views produces the wrong decisions. Before measuring, label each piece by its main job: attract, engage, convert or support sales.</p>
<h2>Five levels of measurement</h2>
{table(["Level", "Question", "Measures", "Where to find them"], funnel)}
<p>Most small businesses stop at reach. The most useful insight usually sits at the action level: which pieces lead visitors to do something. In GA4, mark the actions that matter, such as a contact form submission or a template download, as key events so they can be counted by page. Our <a href="../post/how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide.html">GA4 guide</a> shows how.</p>
<h2>Worked example: a quarterly content review</h2>
<p>An engineering consultancy reviews five pieces of content over a quarter. The figures are illustrative.</p>
{table(["Content", "Visits", "Engagement rate", "Key events", "Of which enquiries", "Key events per 1,000 visits"], rows)}
<p>Three conclusions follow. The two technical guides do the most work: they bring visitors who read and act. The case study has few visits but converts at a high rate, so it should be linked from the guides and sent to prospects, not judged on traffic. The productivity list attracts visitors who leave quickly and never act; it should be improved with specific, expert content or retired. The news piece did its job briefly and needs no further effort.</p>
<h2>A content scorecard you can keep monthly</h2>
<ol>
<li><strong>Organic clicks from Search Console,</strong> for the site and for your top 20 pages.</li>
<li><strong>Engaged sessions and engagement rate</strong> by landing page in GA4.</li>
<li><strong>Key events by page,</strong> and key events per 1,000 visits.</li>
<li><strong>Enquiries that mention or follow content,</strong> recorded in the CRM with a simple source field.</li>
<li><strong>New links and mentions,</strong> checked monthly.</li>
</ol>
<p>Put these on one sheet, compare with last month and the same month last year, and write one sentence on what you will change. That sentence is the point of the exercise.</p>
<h2>Measuring in the age of AI answers</h2>
<p>Search engines and AI assistants now answer many questions directly, so some readers get value from your content without visiting. Two practical responses: track impressions as well as clicks, since rising impressions with falling clicks often means your content is being summarized; and check from time to time whether AI assistants cite your pages for the questions you care about. Content that contains your own data, worked examples and experience is the kind most likely to be cited and the hardest to replace with a summary. See <a href="../post/the-key-differences-between-seo-and-geo-for-enhancing-your-online-presence.html">SEO vs GEO</a> for more.</p>
<h2>Attribution without overthinking it</h2>
<p>Business-to-business buyers often read several pieces over weeks before getting in touch, and analytics tools only see part of that. Do not let imperfect attribution stop you. Ask new enquiries how they found you, add a "how did you hear about us" field to forms, and look at the pages a contact viewed before converting where your tools allow it. Patterns across a year of enquiries are more reliable than any single attribution model.</p>
<h2>Common mistakes</h2>
<ul>
<li>Counting page views and social likes as success.</li>
<li>Not marking key events, so you cannot see which content leads to action.</li>
<li>Judging a sales-support piece by its traffic.</li>
<li>Publishing more instead of improving the pieces that already rank.</li>
<li>Reviewing numbers without deciding anything.</li>
</ul>
"""
    r = [("how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide", "How to measure your website with Google Analytics 4"),
         ("understanding-the-power-of-tofu-mofu-and-bofu-in-your-digital-marketing-strategy", "TOFU, MOFU and BOFU with real numbers"),
         ("the-key-differences-between-seo-and-geo-for-enhancing-your-online-presence", "SEO vs GEO")]
    return art(CM, "How to Measure Content Marketing: From Visits to Enquiries",
               "How to measure content marketing at five levels, from reach to revenue, with a worked quarterly review, a monthly scorecard and what changes with AI answers.",
               ["marketing"], ["content marketing", "content measurement", "GA4", "key events", "Search Console", "B2B marketing"], body, "Content", r)


# ═════════════════════════ 2. CRM ═════════════════════════
USERS = 8
CRM_PRICES = [("Zoho CRM Standard", 14), ("Pipedrive Essential", 14), ("HubSpot Sales Hub Starter", 20), ("Salesforce Starter", 25)]


def crm():
    reqs = [("Contacts and companies", "One record per customer, with history of calls, emails and meetings"),
            ("Pipeline", "Deals by stage, with value and expected close date"),
            ("Email and calendar link", "Emails logged automatically from Outlook or Gmail"),
            ("Tasks and reminders", "Follow-ups that do not depend on memory"),
            ("Quotes", "Quotes from the CRM, or a link to the system that makes them"),
            ("Reporting", "Pipeline by stage, win rate, activity, forecast"),
            ("Integrations", "Accounting, website forms, e-commerce, marketing email"),
            ("Mobile", "Usable on a phone by people who visit customers")]
    cost = [(n, f"${p}", money(p * USERS * 12)) for n, p in CRM_PRICES]
    body = f"""
<p>A customer relationship management (CRM) system keeps everything you know about customers and prospects in one place: who they are, what you have discussed, what you have quoted, and what happens next. For a small business the main benefit is simple: fewer leads and follow-ups lost because they lived in someone's inbox or memory. This guide, first published in 2023, has been rewritten with a requirements checklist, 2026 price ranges and a worked cost example.</p>
<h2>Signs you need a CRM</h2>
<ul>
<li>Leads come in by email, phone and web form, and nobody can say how many there were last month.</li>
<li>Follow-ups are missed when someone is busy or away.</li>
<li>Quotes go out but nobody tracks which are still open.</li>
<li>Customer history leaves with the salesperson who leaves.</li>
<li>Forecasting next quarter's sales is a guess.</li>
</ul>
<h2>Decide what you need before you look</h2>
<p>Start from how you sell, not from feature lists. Map your sales process from first contact to signed order, list the steps, and note what information each step needs. Then score these core requirements as must-have, nice-to-have or not needed.</p>
{table(["Requirement", "What it means in practice"], reqs)}
<h2>2026 price ranges</h2>
<p>Entry-level CRM plans for small teams cost roughly $14 to $25 per user per month in 2026, with several vendors offering free tiers that limit users or contacts. Professional tiers with automation and better reporting typically cost $40 to $100 per user per month, and enterprise tiers more. For {USERS} users on an entry plan, a year's licences look like this (US list prices, billed annually; confirm current pricing with each vendor):</p>
{table(["Plan", "Per user per month", f"Per year for {USERS} users"], cost)}
<p>Licences are rarely the biggest cost. Set-up, importing and cleaning existing contacts, connecting email and accounting, and training usually cost as much as the first year's licences, and the time your team spends using it matters most of all.</p>
<h2>Choosing between the main options</h2>
{table(["If you…", "Look first at"], [
    ("Want a free start and strong marketing tools later", "HubSpot"),
    ("Sell through a clear pipeline of deals and want simplicity", "Pipedrive"),
    ("Want low cost and already use Zoho Books or other Zoho apps", "Zoho CRM or Zoho Bigin"),
    ("Expect to grow to many users with complex processes", "Salesforce or Microsoft Dynamics 365"),
    ("Run Microsoft 365 and want CRM inside Outlook and Teams", "Microsoft Dynamics 365 Sales"),
    ("Need CRM, accounting and operations together", "An ERP with CRM, such as Odoo or NetSuite"),
])}
<h2>Worked example: what does a CRM pay back?</h2>
<p>A small engineering firm receives about 30 enquiries a month and wins work worth an average of $18,000 gross margin per job. Reviewing a quarter, it finds that about one enquiry in ten never received a follow-up. If a CRM with reminders and a shared pipeline recovers even a quarter of those, and the firm wins one in five of them, that is roughly two extra jobs a year, about $36,000 of margin, against licences of a few thousand dollars. The numbers are illustrative; the point is that the value of a CRM comes from follow-up discipline, not features.</p>
<h2>Implementation in six steps</h2>
<ol>
<li><strong>Define your pipeline stages</strong> in plain words, with what must be true to move a deal to the next stage.</li>
<li><strong>Clean your contacts</strong> before importing: remove duplicates and old leads.</li>
<li><strong>Connect email and calendar</strong> so activity is logged without typing.</li>
<li><strong>Start with three reports:</strong> new leads by source, pipeline by stage, and overdue follow-ups.</li>
<li><strong>Train in short sessions</strong> on real deals, not demo data.</li>
<li><strong>Use it in the weekly sales meeting.</strong> If the meeting runs from the CRM, people keep it current.</li>
</ol>
<h2>Why CRM projects fail</h2>
<ul>
<li>Bought for management reports, so salespeople see it as extra admin.</li>
<li>Too many required fields and stages from day one.</li>
<li>No connection to email, so activity has to be typed twice.</li>
<li>Nobody owns the data, so duplicates and old deals pile up.</li>
<li>The owner keeps managing from a spreadsheet, so the team does too.</li>
</ul>
<h2>AI features</h2>
<p>Most CRMs now offer AI features: drafting follow-up emails, summarizing calls and email threads, scoring leads and suggesting next steps. They are useful once the basic data is good, and often sold as paid add-ons. Turn them on after the team uses the CRM consistently, not as a reason to buy one.</p>
"""
    r = [("6-essential-steps-to-streamline-and-enhance-your-sales-process", "Six steps to streamline your sales process"),
         ("understanding-the-power-of-tofu-mofu-and-bofu-in-your-digital-marketing-strategy", "TOFU, MOFU and BOFU with real numbers"),
         ("decoding-the-mysteries-of-api-architecture-a-software-designer-s-guide", "APIs for small businesses")]
    s = [("EngageBay: CRM pricing comparison 2026", "https://www.engagebay.com/blog/crm-pricing/"),
         ("CostBench: CRM pricing benchmarks 2026", "https://costbench.com/stats/crm-pricing-2026/")]
    return art(CRM, "Choosing a CRM for a Small Business: Requirements, 2026 Prices and a Payback Example",
               "How to choose a CRM: signs you need one, a requirements checklist, 2026 price ranges, which option fits which business, a payback example and implementation steps.",
               ["marketing"], ["CRM", "HubSpot", "Pipedrive", "Zoho CRM", "Salesforce", "sales pipeline", "small business software"], body, "CRM", r, s)


# ═════════════════════════ 3. Instagram and social media ═════════════════════════
def ig():
    links = [("Bio links", "Up to five links on your profile", "All accounts", "Your main pages: services, booking, a current offer"),
             ("Story link sticker", "A tappable link on a Story", "All accounts", "Timely posts: a new article, an event, a limited offer"),
             ("Post and Reel captions", "Usually plain text, not clickable", "Most accounts", "Say 'link in bio' or use a Story to carry the link"),
             ("Direct messages", "Links are clickable", "All accounts", "Replies to people who ask for details"),
             ("Ads", "Call-to-action buttons to any page", "Paid", "Driving traffic to a specific landing page")]
    plan = [("Goal", "Pick one: enquiries, bookings, online sales or newsletter sign-ups"), ("Audience", "Who, where, and what they need help with"),
            ("Platform", "Go where your buyers are: Instagram for visual and local consumer businesses; LinkedIn for B2B"),
            ("Content", "Three or four recurring post types you can sustain weekly"), ("Links", "Bio links and Story stickers pointing to pages built for the visitor"),
            ("Measure", "UTM-tagged links, sessions and key events in GA4, monthly review")]
    body = f"""
<p>Instagram can send steady traffic to a website, but only if the account gives people a reason to click and the page they land on gives them a reason to stay. This guide replaces two articles on this site, one from 2023 on Instagram traffic and one from 2025 on using social media for visibility, with a single plan that covers both and reflects how linking on Instagram works in 2026.</p>
<h2>Where links work on Instagram in 2026</h2>
{table(["Place", "What you can do", "Who can use it", "Best use"], links)}
<p>The key constraint has not changed: links typed into a normal post caption are generally not clickable. Your bio links and Story link stickers carry most organic traffic, so treat them as prime real estate and update them as campaigns change.</p>
<h2>A simple social media plan</h2>
{table(["Element", "Decide"], plan)}
<h2>Content that earns the click</h2>
<ul>
<li><strong>Show the work.</strong> Before-and-after photos, short process videos and behind-the-scenes clips perform well for trades, manufacturers, clinics and service firms.</li>
<li><strong>Teach one thing per post.</strong> A tip, a common mistake, a quick calculation. Then offer the full guide behind the link.</li>
<li><strong>Use Reels for reach, Stories for action.</strong> Reels are shown to people who do not follow you yet; Stories reach followers and can carry a link.</li>
<li><strong>Answer questions in public.</strong> Turn the questions customers ask most into posts.</li>
<li><strong>Feature customers and staff,</strong> with permission. People engage with people.</li>
</ul>
<h2>Make the landing page worth the click</h2>
<p>Most lost Instagram traffic is lost after the click. Visitors arrive on a phone, often with little patience. Send them to a page that matches the post they tapped, loads quickly on mobile, makes one clear offer and has a short form or booking button near the top. Sending everyone to your home page wastes the interest you created.</p>
<h2>Paid promotion and collaborations</h2>
<p>A small paid budget can test which posts and offers work before you scale them. Boost posts that already perform organically rather than creating ads from scratch, and target by location and interests. Collaborations with local creators or complementary businesses work best when the partner's audience matches your customers and the offer is specific, such as a joint event or discount.</p>
<h2>Measuring what Instagram sends you</h2>
<p>Add UTM tags to every link you place on Instagram (for example, utm_source=instagram, utm_medium=social, utm_campaign=spring-offer) so Google Analytics can separate bio, Story and ad traffic. Then look at engaged sessions and key events from that traffic, not just visits. Instagram's own insights show reach, profile visits and link taps; GA4 shows what those visitors did next. Our <a href="../post/how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide.html">GA4 guide</a> explains key events.</p>
<h2>Worked example: a physiotherapy clinic</h2>
<p>A clinic posts three Reels a week (exercise tips filmed in the clinic) and two Stories, one of which links to its booking page with a first-visit offer. Its bio links point to booking, services and a page of exercise guides. Over a month, Instagram shows 420 link taps; GA4 shows 360 sessions tagged as Instagram, 230 of them engaged, and 18 online bookings, a 5% conversion rate on sessions. The clinic sees that Story links convert far better than bio links and moves its offer into a weekly Story. The figures are illustrative.</p>
<h2>Common mistakes</h2>
<ul>
<li>Posting without a goal, so nothing can be judged as working or not.</li>
<li>Putting URLs in captions where they cannot be tapped.</li>
<li>One link to the home page for every campaign.</li>
<li>Trying to be on every platform instead of doing one well.</li>
<li>Broadcasting only, never replying to comments and messages.</li>
</ul>
"""
    r = [("how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide", "How to measure your website with Google Analytics 4"),
         ("maximize-your-visibility-with-these-local-seo-tips-for-small-businesses", "Local SEO tips for small businesses"),
         ("from-creation-to-conversion-measuring-the-success-of-your-content-marketing-strategy", "How to measure content marketing")]
    s = [("Taggbox: How to post a link on Instagram in 2026", "https://taggbox.com/blog/how-to-post-a-link-on-instagram/"),
         ("TLinky: Link in bio for Instagram, 2026 guide", "https://tlinky.com/link-in-bio-for-instagram/")]
    return art(IG, "Instagram and Social Media for Small Businesses: Getting Traffic That Turns into Customers",
               "Where links work on Instagram in 2026, a simple social media plan, content that earns clicks, landing pages, measurement with UTM tags and a worked clinic example.",
               ["marketing"], ["Instagram", "social media marketing", "link in bio", "Stories", "Reels", "UTM", "small business marketing"], body, "Social", r, s)


# ═════════════════════════ 4. IoT ═════════════════════════
COMP_KW, COMP_HOURS, LEAK_SHARE, POWER_COST = 75, 6000, 0.20, 0.10
LEAK_SAVE = COMP_KW * COMP_HOURS * LEAK_SHARE * 0.5 * POWER_COST
SENSOR_COST = 6_000


def fig_iot():
    return steps_fig([("Sensors", ["Temperature, vibration,", "current, flow, level"]), ("Connection", ["Wired, Wi-Fi,", "cellular or LoRaWAN"]),
                      ("Platform", ["Store data; rules", "and alerts"]), ("Action", ["Dashboard, alarm,", "work order, report"])],
                     "How an industrial IoT system works: sensors measure temperature, vibration, current, flow or level; a wired, Wi-Fi, cellular or "
                     "LoRaWAN connection carries the data; a platform stores it and applies rules and alerts; the result is a dashboard, an alarm, "
                     "a work order or a report.")


def iot():
    uses = [("Equipment condition", "Vibration and temperature on motors, pumps, fans", "Repair before failure; fewer breakdowns"),
            ("Energy", "Current on compressors, ovens, chillers; meter data", "Find waste, shift loads, verify savings"),
            ("Production counting", "Counts and stop signals from machines", "Live OEE and downtime reasons without clipboards"),
            ("Environment", "Temperature and humidity in storage, cold rooms, labs", "Alarms and records for quality and food safety"),
            ("Tanks and inventory", "Level sensors on bulk materials, fuel, chemicals", "Automatic reordering; fewer stock-outs"),
            ("Assets and vehicles", "GPS and condition on trailers, tools, returnable containers", "Fewer lost assets; better utilization")]
    body = f"""
<p>The Internet of Things (IoT) means connecting physical equipment and sensors to software so that conditions are measured automatically and acted on. For a small manufacturer, warehouse or facility, the value is concrete: knowing a motor is about to fail before it stops the line, seeing which machine wastes energy at night, or getting an alarm when a cold room warms up. This article, first written in 2023, has been rewritten around practical uses, a worked example and the security basics.</p>
<h2>How an IoT system fits together</h2>
{fig(fig_iot(), 1, "Four parts of an industrial IoT system.")}
<p>Sensors have become cheap and wireless, and many newer machines already produce data through their controllers. The harder parts are choosing what to measure, getting the data somewhere useful, and making sure someone acts on it.</p>
<h2>Six uses that pay back for small operations</h2>
{table(["Use", "What is measured", "What it gives you"], uses)}
<h2>Worked example: compressed air leaks</h2>
<p>A plant runs a {COMP_KW} kW air compressor about {COMP_HOURS:,} hours a year. Current sensors on the compressor show it still running at 40% load on weekends when production is stopped, which points to leaks. Leaks commonly waste a significant share of compressed air in plants that do not manage them; assume here that they account for {LEAK_SHARE:.0%} of the compressor's energy. Finding and fixing half of them saves about {COMP_KW * COMP_HOURS * LEAK_SHARE * 0.5:,.0f} kWh a year, or {money(LEAK_SAVE)} at {POWER_COST:.2f} dollars per kWh. Sensors, a gateway and a year of software at about {money(SENSOR_COST)} pay back in roughly {SENSOR_COST / LEAK_SAVE * 12:.0f} months, and the same system keeps watching so leaks do not quietly return. The figures are illustrative; use your own power price and running hours.</p>
<h2>Starting small</h2>
<ol>
<li><strong>Pick one problem with a cost,</strong> such as unplanned downtime on one critical machine, energy on one large load, or spoilage in one cold room.</li>
<li><strong>Measure the minimum</strong> needed to see the problem. Two or three sensors are often enough to prove the case.</li>
<li><strong>Decide who acts</strong> on an alert and what they do. An alarm nobody owns becomes noise.</li>
<li><strong>Run a 90-day pilot</strong> and compare against the period before.</li>
<li><strong>Scale what works,</strong> using the same platform so data stays in one place.</li>
</ol>
<h2>Connectivity options</h2>
{table(["Option", "Good for", "Watch for"], [
    ("Wired (Ethernet, fieldbus)", "Fixed machines; reliable, secure", "Installation cost in existing plants"),
    ("Wi-Fi", "Indoor sensors near existing networks", "Coverage in metal buildings; shared with office traffic"),
    ("Cellular (LTE-M, 5G)", "Remote sites, vehicles, tanks", "Monthly data plans; coverage"),
    ("LoRaWAN and similar low-power radio", "Battery sensors over large sites", "Low data rates; a gateway is needed"),
])}
<h2>Security first</h2>
<p>Every connected device is a possible entry point. Keep IoT devices on a separate network from office computers, change default passwords, update firmware, and limit which systems can talk to them. Choose vendors that support updates for years, not months. The Canadian Centre for Cyber Security's baseline controls, covered in our <a href="../post/cybersecurity-for-small-businesses-tips-and-best-practices.html">cybersecurity guide</a>, apply to IoT as much as to laptops.</p>
<h2>From data to decisions</h2>
<p>IoT data is most valuable when it feeds the measures you already manage: OEE, energy per unit, downtime by cause, spoilage. Connect it to your maintenance system so alerts create work orders, and to your dashboards so supervisors see it daily. Over time, the history it builds is also what AI tools need to predict failures and optimize settings.</p>
"""
    r = [("what-oee-really-measures", "What OEE really measures"),
         ("cybersecurity-for-small-businesses-tips-and-best-practices", "Cybersecurity for small businesses"),
         ("the-future-of-warehousing-how-automation-technology-is-changing-the-game", "Warehouse automation for small and mid-sized operations")]
    return art(IOT, "Industrial IoT for Small Manufacturers: Uses, a Worked Example and How to Start",
               "How industrial IoT works, six uses that pay back for small operations, a compressed-air worked example, connectivity options, security and how to start small.",
               ["digital-technology", "artificial-intelligence"], ["IoT", "industrial IoT", "sensors", "predictive maintenance", "energy monitoring", "manufacturing"], body, "IoT", r)


# ═════════════════════════ 5. Warehouse automation ═════════════════════════
PICKERS, WAGE, WALK_SHARE, CUT = 6, 52_000, 0.50, 0.35
SAVE_WH = PICKERS * WAGE * WALK_SHARE * CUT
AMR_COST = 180_000


def wh():
    levels = [("1. Basics", "Barcode scanning, a WMS or inventory system, labelled locations, slotting by velocity", "Most small warehouses; low cost"),
              ("2. Assisted picking", "Pick-to-light, put-to-light, voice picking, batch carts, mobile printers", "High order lines per day; many small items"),
              ("3. Mobile robots", "Autonomous mobile robots (AMRs) that carry totes or follow pickers", "Long walking distances; growing volumes"),
              ("4. Goods-to-person", "Shuttle or cube storage systems that bring bins to a picking station", "Dense storage, very high volumes, small parts"),
              ("5. Full automation", "Automated storage and retrieval, sortation, robotic picking", "Large, stable volumes; major capital")]
    body = f"""
<p>Warehouse automation ranges from barcode scanners to fully automated storage systems. For small and mid-sized distributors and manufacturers, the right step is rarely the most advanced technology; it is the one that removes the biggest cost or error in the current operation. This article, first written in 2023, has been rewritten as a step-by-step guide with a worked payback example.</p>
<h2>Five levels of automation</h2>
{table(["Level", "Examples", "Fits"], levels)}
<p>Skipping level 1 is the most common and expensive mistake. Robots and goods-to-person systems depend on accurate inventory records, clean item data and a warehouse management system. Without them, automation makes errors faster.</p>
<h2>Where the time goes in a typical warehouse</h2>
<p>In manual picking, much of a picker's time is spent walking between locations rather than picking; the exact share depends on layout and order profile, so measure it by timing a sample of picks. Searching, checking paperwork and correcting errors take much of the rest. That is why the first gains usually come from slotting fast movers near the dispatch area, batching orders, and scanning to confirm picks, all before any robot arrives.</p>
<h2>Worked example: are mobile robots worth it?</h2>
<p>A distributor has {PICKERS} pickers, each costing about {money(WAGE)} a year with benefits. Timing studies show they spend about {WALK_SHARE:.0%} of their time walking. Collaborative mobile robots that carry totes between pick zones and the packing area could cut picker labour time by about {CUT:.0%} of that walking, saving roughly {money(SAVE_WH)} a year, or allowing the same team to handle more volume. A small fleet with software and integration costing about {money(AMR_COST)} would pay back in about {AMR_COST / SAVE_WH:.1f} years. Many vendors also offer robots as a subscription, which changes the decision from capital to operating cost. The figures are illustrative; the timing study is what makes the case.</p>
<h2>Questions to answer before buying</h2>
<ul>
<li>What are your order lines per day, peak versus average, and how fast are they growing?</li>
<li>How many SKUs, and how many account for most picks?</li>
<li>How accurate is your inventory today, and is it in a WMS?</li>
<li>What is the building like: ceiling height, floor quality, aisle widths, Wi-Fi coverage?</li>
<li>Will the system scale down in a slow year, or is it a fixed cost?</li>
<li>Who will maintain it, and what is the vendor's support in your region?</li>
</ul>
<h2>Implementation tips</h2>
<ol>
<li><strong>Fix the basics first:</strong> locations, scanning, inventory accuracy and slotting.</li>
<li><strong>Simulate with your own order data</strong> before committing; good vendors will.</li>
<li><strong>Pilot one zone or one shift</strong> and measure lines per hour, accuracy and safety.</li>
<li><strong>Involve the pickers early;</strong> they know where time is lost and will make or break adoption.</li>
<li><strong>Plan for peak:</strong> design for the busy season, not the average week.</li>
</ol>
<h2>Measures to track</h2>
{table(["Measure", "Why"], [("Order lines picked per labour hour", "Productivity"), ("Pick accuracy", "Errors cost more than speed saves"),
    ("Order cycle time", "What customers feel"), ("Dock-to-stock time", "How fast receipts become sellable"), ("Inventory record accuracy", "The foundation for any automation")])}
<p>For the software side, see <a href="../post/top-10-inventory-management-software-a-comprehensive-comparison-guide.html">inventory management software for small businesses</a>, and for the measures, <a href="../post/50-must-track-kpis-for-business-success-from-finance-to-product-development.html">50 KPIs with formulas</a>.</p>
"""
    r = [("top-10-inventory-management-software-a-comprehensive-comparison-guide", "Inventory management software for small businesses"),
         ("abc-inventory-analysis", "ABC inventory analysis"), ("the-iot-revolution-how-connected-devices-are-transforming-industries", "Industrial IoT for small manufacturers")]
    return art(WH, "Warehouse Automation for Small and Mid-Sized Operations: What to Automate First",
               "Five levels of warehouse automation, where picking time goes, a worked mobile-robot payback example, questions to answer before buying and measures to track.",
               ["erp", "digital-technology", "artificial-intelligence", "inventory-management"],
               ["warehouse automation", "AMR", "goods-to-person", "WMS", "picking", "distribution"], body, "Warehouse", r)


# ═════════════════════════ 6. Tesla ═════════════════════════
def ts():
    canvas = [("Customer segments", "Buyers of premium and mid-priced electric vehicles; utilities and businesses buying battery storage; homeowners buying solar and Powerwall"),
              ("Value propositions", "Electric cars with long range and software that improves over time; a dedicated fast-charging network; large-scale battery storage"),
              ("Channels", "Direct online sales and company-owned stores instead of franchised dealers; over-the-air software updates"),
              ("Customer relationships", "Direct ownership of the customer; app-based service; a strong brand community"),
              ("Revenue streams", "Vehicle sales and leases, energy storage and solar, services, charging, software features, regulatory credits"),
              ("Key resources", "Battery and powertrain technology, factories, software and vehicle data, the Supercharger network, the brand"),
              ("Key activities", "Vehicle and battery design, high-volume manufacturing, software development, energy project delivery"),
              ("Key partners", "Battery cell and raw material suppliers, governments and utilities, charging site hosts"),
              ("Cost structure", "Factories and equipment, materials (especially batteries), research and development, the service and charging network")]
    ops = [("Vertical integration", "Designs its own software, powertrains and many components, and makes some battery cells", "Control of cost and pace of change; more capital and risk"),
           ("Large castings", "Few large cast parts replace many stamped and welded ones in the car body", "Fewer parts, steps and robots; less flexibility to change designs"),
           ("Software-defined product", "Features and fixes delivered over the air", "Improvements without a dealer visit; a direct relationship with the owner"),
           ("Direct sales", "No independent dealers in most markets", "Control of price and experience; owns the cost of stores and service"),
           ("Fast iteration", "Frequent, small changes on the line", "Rapid improvement; quality can vary between builds")]
    body = f"""
<p>Tesla is one of the most discussed companies of the past two decades, both for what it got right and for its recent difficulties. This case study, first written in 2023, has been rewritten to combine the business model canvas with a look at Tesla's operations, replacing a separate 2024 article on its operational efficiency. It uses Tesla's reported 2025 results and ends with lessons a small or mid-sized business can apply. It is an analysis of the business model, not an investment view.</p>
<h2>Tesla in 2025, in numbers</h2>
<p>Tesla delivered about 1.64 million vehicles in 2025, down roughly 9% from 1.79 million in 2024, its second year of decline after a peak of 1.81 million in 2023. Total revenue was about $94.8 billion, its first annual decline. The energy business went the other way: storage deployments rose about 49% to a record 46.7 GWh, and energy generation and storage revenue grew about 27% to $12.8 billion. At year end Tesla operated 8,182 Supercharger stations. Free cash flow rose to about $6.2 billion.</p>
<h2>The business model canvas</h2>
{table(["Building block", "Tesla"], canvas)}
<h2>How the operations support the model</h2>
{table(["Practice", "What Tesla does", "Trade-off"], ops)}
<h2>What worked</h2>
<ul>
<li><strong>Owning the customer relationship.</strong> Direct sales, the app and over-the-air updates give Tesla data and a channel no traditional automaker had.</li>
<li><strong>Building the infrastructure customers needed.</strong> The Supercharger network removed the biggest objection to buying an electric car and became an asset others now connect to.</li>
<li><strong>Treating cost as a design problem.</strong> Large castings and simplified designs cut parts and steps rather than only negotiating with suppliers.</li>
<li><strong>A second business with different demand.</strong> Energy storage grew strongly in 2025 while vehicle sales fell, which is why its share of revenue increased.</li>
</ul>
<h2>What the recent decline shows</h2>
<ul>
<li><strong>Competition caught up.</strong> Many manufacturers, especially in China, now sell capable electric vehicles at lower prices.</li>
<li><strong>An ageing line-up.</strong> Most sales still come from two models first launched years ago.</li>
<li><strong>Brand and policy risk.</strong> Sales fell sharply in parts of Europe and in Canada in 2025, and the end of some purchase incentives hurt demand.</li>
<li><strong>Bets on the future.</strong> The company is spending heavily on autonomy and robots, which may or may not pay off on the timelines it has given.</li>
</ul>
<h2>Lessons for a small or mid-sized business</h2>
<ol>
<li><strong>Remove the customer's biggest obstacle,</strong> even if it means doing something outside your core product, as charging was for Tesla.</li>
<li><strong>Design cost out</strong> of the product and process instead of only squeezing suppliers. A <a href="../post/perform-kaizen-event.html">Kaizen event</a> on one product line is the small-business version.</li>
<li><strong>Keep a direct line to customers.</strong> Owning the relationship gives you data and loyalty that resellers keep for themselves.</li>
<li><strong>Do not rely on one product or one market.</strong> Tesla's energy business softened a weak year in cars.</li>
<li><strong>Refresh before competitors catch up.</strong> A strong position decays faster than it feels from the inside.</li>
</ol>
<p>To build your own canvas, draw the nine blocks on one page and fill them in with your team. It takes an hour and often reveals that the most profitable customers and the most expensive activities are not the ones everyone assumed.</p>
"""
    r = [("how-to-increase-operational-efficiency-for-small-business", "Operational efficiency for small businesses"),
         ("perform-kaizen-event", "How to run a Kaizen event"), ("things-you-need-to-know-about-the-theory-of-constraints-toc", "The theory of constraints")]
    s = [("Drive Tesla Canada: Tesla Q4 and full-year 2025 production and deliveries", "https://driveteslacanada.ca/news/tesla-misses-q4-delivery-consensus-by-narrow-margin-as-energy-outperforms/"),
         ("Yahoo Finance / Just Auto: Tesla revenue slips in 2025 as energy unit grows", "https://finance.yahoo.com/news/tesla-revenue-slips-2025-energy-163645200.html"),
         ("Electrek: Tesla Q4 2025 delivery results", "https://electrek.co/2026/01/02/tesla-tsla-releases-q4-delivery-results/")]
    return art(TS, "Tesla's Business Model and Operations: A 2026 Case Study with Lessons for Smaller Firms",
               "Tesla's business model canvas, how its operations support it, 2025 results including the energy business, what worked, what the decline shows, and lessons for SMEs.",
               ["case-study"], ["Tesla", "business model canvas", "case study", "vertical integration", "manufacturing", "energy storage"], body, "Case study", r, s)


# ═════════════════════════ 7. AI customer service ═════════════════════════
EMAILS_DAY, MIN_BEFORE, MIN_AFTER, CS_RATE, CS_DAYS = 60, 6, 3.5, 32, 250
CS_SAVE_H = EMAILS_DAY * (MIN_BEFORE - MIN_AFTER) / 60 * CS_DAYS


def cs():
    uses = [("Draft replies", "AI drafts an answer from your policies and order data; a person checks and sends", "Low"),
            ("Triage and routing", "Classify incoming emails and tickets by topic and urgency; send to the right person", "Low"),
            ("Summaries", "Summarize long threads or calls so the next person picks up quickly", "Low"),
            ("Knowledge base", "Turn resolved tickets into help articles; keep them current", "Low to medium"),
            ("Website chat for routine questions", "Answer hours, order status, returns policy from approved content", "Medium"),
            ("Actions on the customer's behalf", "Change orders, issue refunds, book appointments", "High: needs strict limits and review")]
    body = f"""
<p>AI tools such as ChatGPT, Claude, Gemini and the assistants built into help desk software can now handle much of the routine work in customer service: drafting replies, sorting incoming messages, summarizing long threads and answering common questions. Used well, they make a small team faster and more consistent. Used carelessly, they give customers wrong answers in your company's name. This article, first written in 2023, has been rewritten with practical uses, a Canadian legal lesson and a worked example.</p>
<h2>Where AI helps, from lowest to highest risk</h2>
{table(["Use", "How it works", "Risk"], uses)}
<p>Start at the top of the table. Uses where a person reviews the output before a customer sees it deliver most of the time savings with little risk.</p>
<h2>A Canadian lesson: you are responsible for what your chatbot says</h2>
<p>In <em>Moffatt v. Air Canada</em> (2024), British Columbia's Civil Resolution Tribunal found Air Canada liable after its website chatbot gave a customer wrong information about bereavement fares. The airline argued, in effect, that the chatbot was responsible for its own statements; the tribunal rejected that and held the company responsible for all information on its website, whether from a static page or a chatbot. The amount awarded was small, but the principle matters for every business: an AI assistant speaking to customers is speaking for you.</p>
<h2>Guardrails that keep AI answers safe</h2>
<ol>
<li><strong>Ground answers in your own content.</strong> Connect the assistant to approved policies, product information and order data, and instruct it to answer only from them.</li>
<li><strong>Tell it what to do when unsure:</strong> say so and hand over to a person, rather than guess.</li>
<li><strong>Keep people in the loop</strong> for refunds, exceptions, complaints and anything involving money, safety or legal terms.</li>
<li><strong>Make handover easy.</strong> Customers should be able to reach a person without fighting the bot.</li>
<li><strong>Protect personal information.</strong> Use business plans of AI tools that do not train on your data, and follow your privacy obligations.</li>
<li><strong>Review a sample of conversations weekly,</strong> and fix the content or instructions behind any wrong answer.</li>
</ol>
<h2>Worked example: email support at a distributor</h2>
<p>A parts distributor's two-person service team answers about {EMAILS_DAY} customer emails a day, at about {MIN_BEFORE} minutes each. They add an assistant inside their help desk that classifies each email, pulls the order details and drafts a reply from the company's policies; staff edit and send. Average handling time falls to about {MIN_AFTER} minutes. That frees roughly {CS_SAVE_H:,.0f} hours a year, worth about {money(CS_SAVE_H * CS_RATE)} at {money(CS_RATE)} an hour, which the team uses to call back customers with complex problems and to clear the backlog of quote requests. Replies also become more consistent, because they all start from the same policy text. The figures are illustrative.</p>
<h2>How to start</h2>
<ol>
<li><strong>Collect your top 30 questions</strong> and the correct answers; this becomes the assistant's source material and a help page.</li>
<li><strong>Pick one channel</strong>, usually email, and use AI for drafts and triage only.</li>
<li><strong>Measure</strong> first response time, handling time, resolution rate and customer satisfaction before and after.</li>
<li><strong>Expand</strong> to website chat for routine questions once draft quality is consistently good.</li>
</ol>
<p>For writing effective instructions, see <a href="../post/harnessing-the-power-of-prompt-engineering-transforming-businesses-with-chatgpt.html">prompting AI models for business work</a>; for when to connect AI to your systems, see <a href="../post/ai-agents-101-and-how-to-use-them-to-improve-efficiency.html">AI agents for small businesses</a>.</p>
"""
    r = [("ai-agents-101-and-how-to-use-them-to-improve-efficiency", "AI agents for small businesses"),
         ("harnessing-the-power-of-prompt-engineering-transforming-businesses-with-chatgpt", "Prompting AI models for business work"),
         ("agent-security-and-identity-prompt-injection-least-privilege-credentials-audit", "Agent security and identity")]
    s = [("American Bar Association, Business Law Today: BC tribunal confirms companies remain liable for information provided by AI chatbot", "https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/"),
         ("Moffatt v. Air Canada, 2024 BCCRT 149 (CanLII)", "https://canlii.ca/t/k2spq")]
    return art(CS, "AI in Customer Service for Small Businesses: Uses, Guardrails and a Worked Example",
               "Where AI helps customer service, from drafts to chatbots, the Moffatt v. Air Canada lesson, six guardrails, a worked email example and how to start.",
               ["artificial-intelligence"], ["AI customer service", "ChatGPT", "chatbot", "Air Canada chatbot case", "help desk", "small business AI"], body, "Service", r, s)


# ═════════════════════════ 8. AI and jobs ═════════════════════════
def fig_exposure():
    s = DEFS
    groups = [("High exposure, high complementarity", 29, GREEND, "AI likely to help: e.g. doctors, engineers"),
              ("High exposure, low complementarity", 31, ORANGE, "Tasks AI may take over: e.g. many clerical roles"),
              ("Low exposure", 40, BLUE, "Little direct effect: e.g. many trades and manual roles")]
    x = 14
    for name, p, c, ex in groups:
        w = p * 7.14
        s += f'<rect x="{x}" y="20" width="{w}" height="50" fill="{c}" opacity=".9"/>' + txt(x + w / 2, 51, f"{p}%", "middle", "#fff", 16, True)
        x += w
    for i, (name, p, c, ex) in enumerate(groups):
        y = 96 + i * 26
        s += f'<rect x="14" y="{y - 12}" width="14" height="14" fill="{c}"/>' + txt(36, y, f"{name}: {ex}", "start", NAVY, 12.3)
    return svg("Canadian workers by AI exposure, from Statistics Canada estimates for May 2021: 29% in jobs with high exposure and high "
               "complementarity, where AI is likely to help, such as doctors and engineers; 31% in jobs with high exposure and low "
               "complementarity, where AI may take over tasks, such as many clerical roles; 40% in jobs with low exposure, such as many "
               "trades and manual roles.", 742, 170, s, 600)


def jobs():
    body = f"""
<p>Will AI take jobs or create them? The honest answer in 2026 is both, unevenly, and more slowly in some places than the headlines suggest. This article, first written in 2023 as a list of AI opportunities, has been rewritten around current Canadian and global data and what it means for small and mid-sized employers and their staff.</p>
<h2>The global picture</h2>
<p>The World Economic Forum's <em>Future of Jobs Report 2025</em>, based on a survey of more than 1,000 large employers, projects that between 2025 and 2030 about 170 million jobs will be created and 92 million displaced worldwide, a net gain of 78 million, with technology, the green transition, demographics and economic pressures all contributing. It also projects that 59 out of every 100 workers will need some reskilling or upskilling by 2030, and that 11 of them are unlikely to receive it. The fastest-growing roles include big data, fintech and AI specialists; the fastest-declining include postal, banking and data-entry clerks.</p>
<h2>Which Canadian jobs are exposed</h2>
<p>Statistics Canada has estimated how exposed Canadian jobs are to AI, separating jobs where AI is likely to complement workers from those where it may replace tasks. Using 2021 census data, it found 29% of workers in jobs highly exposed to and highly complementary with AI, 31% in highly exposed but less complementary jobs, and 40% in jobs not highly exposed. Highly educated workers were more likely to be exposed, but also more likely to be in jobs AI could help. Statistics Canada stresses that high exposure does not necessarily mean a higher risk of job loss.</p>
{fig(fig_exposure(), 1, "How Canadian jobs are exposed to AI, Statistics Canada's experimental estimates for May 2021.")}
<h2>How Canadians actually use AI at work</h2>
<p>Statistics Canada's first survey of AI use by workers, from March 2026, found that 53.8% of workers in high-exposure, high-complementarity occupations used generative AI tools at work, compared with 45.9% in high-exposure, low-complementarity occupations and 14.2% in low-exposure occupations. Use was lowest in accommodation and food services, agriculture, and transportation and warehousing. Most users applied the tools to some tasks rather than most of their work.</p>
<h2>What this means for a small or mid-sized employer</h2>
<ul>
<li><strong>Tasks change before jobs do.</strong> Expect drafting, summarizing, searching, data entry and first-level analysis to be done with AI help, while judgement, relationships and hands-on work stay with people.</li>
<li><strong>The gap is skills, not headcount.</strong> Staff who learn to use AI tools well will be noticeably more productive than those who do not, in the same role.</li>
<li><strong>Clerical roles change most.</strong> Plan with the people in them: many can move to customer, quality, planning or analysis work that the business struggled to staff.</li>
<li><strong>New roles appear in small forms.</strong> Someone who owns your AI tools, data quality and automation, often part time, is the small-business version of the "AI specialist" in the global reports.</li>
</ul>
<h2>A practical plan</h2>
<ol>
<li><strong>List the tasks,</strong> not the jobs, in each role, and mark which AI could draft, speed up or check.</li>
<li><strong>Set a simple AI use policy:</strong> approved tools, what data may go into them, and when a person must review output.</li>
<li><strong>Train everyone in the basics,</strong> using your own documents and tasks, then go deeper with those who use it most.</li>
<li><strong>Redesign one process at a time</strong> with the people who do it, and measure time and quality before and after.</li>
<li><strong>Use the time saved deliberately:</strong> on customers, quality and growth, and say so to staff, so AI is seen as help rather than a threat.</li>
</ol>
<h2>For individuals</h2>
<p>The safest career strategy is to become the person in your role who uses AI well: knows what to ask, checks the output, and spends the saved time on the parts of the job that need judgement and relationships. Skills that the WEF report highlights as growing, such as analytical thinking, resilience, technology literacy and leadership, are exactly the ones that make AI use effective.</p>
"""
    r = [("ai-readiness-preparing-your-organization-for-successful-ai-adoption", "AI readiness: preparing your organization"),
         ("ai-agents-101-and-how-to-use-them-to-improve-efficiency", "AI agents for small businesses"),
         ("change-management-toolkit-the-top-10-models-and-how-to-choose-the-right-one-for-your-organization", "Change management toolkit, including AI and data projects")]
    s = [("World Economic Forum: Future of Jobs Report 2025 press release", "https://www.weforum.org/press/2025/01/future-of-jobs-report-2025-78-million-new-job-opportunities-by-2030-but-urgent-upskilling-needed-to-prepare-workforces/"),
         ("Statistics Canada: Experimental estimates of AI occupational exposure in Canada (2024)", "https://www150.statcan.gc.ca/n1/daily-quotidien/240903/dq240903b-eng.htm"),
         ("Statistics Canada: AI use by Canadian workers, March 2026 (The Daily, July 30, 2026)", "https://www150.statcan.gc.ca/n1/daily-quotidien/260730/dq260730b-eng.htm")]
    return art(JOBS, "AI and Jobs in Canada: What the Data Shows and What Employers Should Do",
               "What 2025–2026 data from the WEF and Statistics Canada says about AI, jobs and skills, which Canadian jobs are exposed, and a practical plan for employers.",
               ["digital-technology", "artificial-intelligence"], ["AI and jobs", "future of work", "Statistics Canada", "WEF Future of Jobs", "upskilling", "AI adoption"], body, "AI jobs", r, s)


ALL = (cm, crm, ig, iot, wh, ts, cs, jobs)

if __name__ == "__main__":
    op = os.path.join(HERE, "original_dates.json")
    od = json.load(open(op, encoding="utf-8")); od.update(ORIGINAL)
    note = od.pop("_note"); json.dump({"_note": note, **dict(sorted(od.items()))}, open(op, "w", encoding="utf-8"), indent=1)
    from v478_extra import expand
    for f in ALL:
        a = expand(f())
        a["read"] = f"{max(4, round(words(a['body']) / 200))} min read"
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"][:50], words(a["body"]), "words", a["read"])
    print(f"IoT save {LEAK_SAVE:,.0f}; WH save {SAVE_WH:,.0f} payback {AMR_COST / SAVE_WH:.1f}; CS hours {CS_SAVE_H:,.0f}")
