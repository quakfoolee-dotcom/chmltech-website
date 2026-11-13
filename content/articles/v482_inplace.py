"""V4.82 light fixes on the remaining 2025 and 2026 posts (audit plan V8), edited in place.

1. Unsourced statistics: removed, attributed to a real source, or shown as an illustrative example.
2. Filler openers ("In today's fast-paced...") rewritten to start with the point.
3. Additions the audit asked for: series labels, worked examples, figures, Google Business Profile steps, links.
4. The Nvidia Way post is credited to the book (Tae Kim, 2024) and moved to Book Review.

Idempotent: each replacement is skipped once applied, and each new section carries data-v482="<id>".
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "content", "gen"))
from feed_articles import svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEND, ORANGE, MUTED, PALE, GREENF, ORANGEF
from v478_articles import table

ARTWAR = "the-art-of-the-deal-vs-the-art-of-war-a-strategic-comparison-through-economics-philosophy-and-et"
MISTAKES = "8-mistakes-to-avoid-while-building-your-first-business-a-comprehensive-guide-for-new-entrepreneurs"
ATOMIC = "atomic-habits-by-james-clear-a-deep-dive-review-and-guide-to-habit-transformation"
EMYTH = "the-e-myth-revisited-by-michael-e-gerber-a-comprehensive-book-review-for-small-business-owners"
ONE = "the-one-thing-by-gary-keller-and-jay-papasan-a-deep-dive-review-for-achieving-extraordinary-results"
FAST = "the-millionaire-fastlane-by-mj-demarco-a-bold-blueprint-for-rapid-wealth-creation"
MONEY = "the-psychology-of-money-by-morgan-housel-a-thought-provoking-review-on-wealth-behavior-and-happin"
FIRST = "first-principles-thinking-the-core-of-breakthrough-problem-solving-in-business"
REV = "top-5-proven-strategies-to-boost-revenue-for-small-businesses"
NVIDIA = "unlocking-success-with-the-nvidia-way-strategies-for-innovation-and-growth"
PPM1 = "achieving-success-with-project-portfolio-management"
PPM2 = "how-to-benchmark-and-elevate-your-organization-ppm-maturity-level"
SCEN = "leveraging-ai-tools-for-effective-scenario-analysis-and-predictive-modelling-in-strategic-decision-m"
OPSC = "maximizing-business-efficiency-through-operational-consulting-and-data-driven-strategies"
DUAL = "navigating-complex-transformations-with-a-dual-ceo-structure"
LOCAL = "maximize-your-visibility-with-these-local-seo-tips-for-small-businesses"
DASH = "boost-performance-with-effective-dashboard-strategies-for-entrepreneurs"
BPS = "mastering-the-business-performance-system-bps-for-success"
DOWN = "10-essential-strategies-to-manage-costs-during-economic-downturns"
OODA = "ooda-loop-vs-pdca-cycle-which-framework-drives-faster-and-smarter-decisions"
B2C = "10-essential-steps-to-create-an-effective-online-marketing-strategy-for-b2c-success"
COST = "how-to-reduce-costs-with-proven-process-improvement-strategies"
BENCH = "implement-these-proven-steps-to-benchmark-and-optimize-your-business-processes"
LINKS = "turn-mentions-into-measurable-results-how-to-build-campaigns-that-earn-backlinks-brand-mentions"
AIREADY = "ai-readiness-preparing-your-organization-for-successful-ai-adoption"
DATA = "data-strategy-for-ai-building-the-foundation-for-scalable"
AISTEPS = "5-proven-steps-to-integrate-ai-into-your-operations-workflow-for-smarter-faster-results"
SLUGS = [ARTWAR, MISTAKES, ATOMIC, EMYTH, ONE, FAST, MONEY, FIRST, REV, NVIDIA, PPM1, PPM2, SCEN, OPSC, DUAL, LOCAL, DASH, BPS, DOWN,
         OODA, B2C, COST, BENCH, LINKS, AIREADY, DATA, AISTEPS]

L = lambda slug, text: f'<a href="{slug}.html">{text}</a>'           # link to another post
P = lambda page, text: f'<a href="../{page}">{text}</a>'            # link to a site page
ILL = " (an illustrative example)"

# ───────────── 1 + 2. Sentence-level replacements: (slug, old, new) ─────────────
R = [
    # filler left in the AI steps post
    (AISTEPS, "Artificial intelligence is no longer a futuristic concept. It is transforming how companies manage their operations, driving smarter decisions and faster outcomes. For operations managers, process engineers, and supply chain leaders, integrating AI into your workflow can unlock new levels of efficiency and operational excellence.",
              "AI tools can now read documents, forecast demand, schedule work and answer routine questions, so they can take real work off operations teams. For operations managers, process engineers and supply chain leaders, the question is how to integrate them into daily workflow."),
    (AISTEPS, "This approach will help you unlock the full potential of AI operations and drive lasting operational excellence.", "Each success builds the data, skills and trust the next step needs."),
    (AISTEPS, "In conclusion, the integration of AI into operations is a strategic move that can yield significant benefits. By following the steps outlined in this guide, you can position your organization for success. Embrace the journey, and let AI lead you toward operational excellence.",
              "Choose one process this quarter, set a measure before you start, and keep a person checking the results until the evidence says the tool can be trusted."),
    (SCEN, "In conclusion, the integration of AI into scenario analysis and predictive modeling is not just a trend; it's a necessity for businesses aiming for operational excellence. By embracing these technologies, organizations can navigate uncertainties with confidence and make data-driven decisions that lead to sustainable growth. ",
           "Start with one decision that depends on an uncertain forecast, such as inventory, staffing or pricing, build three scenarios for it, and decide in advance what you will do in each. "),
    (OODA, "<li>Your organization operates in a fast-paced and dynamic environment.</li>", "<li>The situation changes faster than a formal plan can be tested.</li>"),
    # book reviews
    (ONE, "Once she focused her mornings on this, her business saw a 40% increase in revenue in six months.",
          "Once she focused her mornings on this, enquiries became steadier and her other tasks easier to schedule. (Lisa is an illustrative example, not a case from the book.)"),
    (MONEY, "Example: Warren Buffett made 99% of his wealth after his 50th birthday.",
            "Example: Housel points out that almost all of Warren Buffett's fortune was accumulated after his 50th birthday, the result of decades of compounding."),
    (EMYTH, "this review will help you understand how Gerber’s principles can revolutionize the way you approach entrepreneurship.",
            "this review explains Gerber’s main ideas and how to apply them to the way you run your business."),
    (FAST, "This review delves into the core concepts", "This review explains the core concepts"),
    (ARTWAR, "Success in today’s volatile world demands both ambition and wisdom.", "Business success demands both ambition and wisdom."),
    # first principles
    (FIRST, "In today’s hyper-competitive market, most organizations make decisions by analogy",
            "Most organizations make decisions by analogy"),
    (FIRST, "<li><strong>Truth:</strong>\u00a010–12% of material was lost during changeovers and packaging errors.</li>",
            "<li><strong>Truth:</strong> a significant share of material was being lost during changeovers and packaging errors.</li>"),
    (FIRST, "By re-engineering workflows and introducing digital monitoring, the company reduced material waste by 8% and saved over <strong>CAD 900,000 annually</strong>, without changing suppliers or raising prices.",
            "By re-engineering workflows and introducing digital monitoring, the company cut material waste substantially, without changing suppliers or raising prices."),
    (FIRST, "<li><strong>It unlocks innovation.</strong>", "<li><strong>It opens up new options.</strong>"),
    # revenue
    (REV, "In today's competitive market, increasing revenue is crucial for small businesses. With limited resources, every dollar counts.",
          "Small businesses have limited resources, so every dollar spent on growth has to count."),
    (REV, " Businesses that effectively segment their market can see a revenue increase of up to 10% within the first year.", ""),
    (REV, " In fact, businesses that implement loyalty programs can generate up to 20% more revenue through repeat customers.",
          " A loyalty programme rewards repeat customers, who usually cost far less to win than new ones."),
    (REV, " Companies that listen to customer feedback often see a loyalty increase of 5% to 10%, translating to higher revenue.", ""),
    (REV, "According to research, businesses that develop additional income streams can expect to see revenue growth by 15% or more compared to those that do not. ",
          "Additional income streams, such as services, maintenance plans or training built on what you already sell, also reduce dependence on one product. "),
    (REV, " Businesses that invest in customer relationships see an increase in sales by up to 25% over time.", ""),
    (REV, "In a landscape filled with competition, adaptability and proactive strategies will set your small business apart. Embrace these methods to watch your business flourish in an ever-changing marketplace.",
          "Pick the one or two strategies that fit your business best, set a measurable target for each, and review the results every quarter."),
    # nvidia
    (NVIDIA, "In the fast-paced world of technology, few companies have managed to carve out a niche as significant as Nvidia.",
             "This post draws on <em>The Nvidia Way: Jensen Huang and the Making of a Tech Giant</em> by Tae Kim (W. W. Norton, 2024), a history of the company based on interviews with its executives, employees and partners. Few technology companies have carved out a position as significant as Nvidia."),
    (NVIDIA, "Nvidia's business strategy is a testament to its adaptability in a rapidly evolving tech landscape.", "Nvidia's business strategy shows how adaptable the company has been as its markets changed."),
    (NVIDIA, "which revolutionized parallel computing", "which made parallel computing on GPUs accessible to ordinary developers"),
    (NVIDIA, "To navigate this landscape, Nvidia must remain agile", "To keep growing, Nvidia must remain agile"),
    (NVIDIA, "we too can unlock success in our respective fields.", "we can apply the same habits in our own businesses."),
    # scenario analysis
    (SCEN, " For example, in 2022, research showed that companies using AI for predictive analytics saw their forecasting accuracy enhance by nearly 25%.", ""),
    (SCEN, " In fact, studies suggest that companies prioritizing data analytics are 23 times more likely to attract customers, 6 times more likely to retain them, and 19 times more likely to be profitable.", ""),
    (SCEN, "This responsiveness is critical in today's rapidly changing market, where swift adaptations can determine success or failure.",
           "This responsiveness matters most when demand, prices or supply change quickly."),
    (SCEN, "The business landscape changes often, and organizations must remain flexible to stay competitive.", "Markets change, and the models need to change with them."),
    # operational consulting
    (OPSC, "In the dynamic world of business, finding ways to improve efficiency and increase profitability is crucial. Organizations are continuously looking for effective methods to enhance productivity and streamline processes. ",
           ""),
    (OPSC, "This post will discuss how operational consulting can revolutionize your organization", "This post explains how operational consulting can improve your organization"),
    (OPSC, "For instance, a manufacturing company we worked with reduced production time by 25% after adopting Lean principles that eliminated non-value-adding activities.",
           "For instance, a manufacturer can shorten production time considerably by applying Lean principles to remove non-value-adding steps."),
    (OPSC, " Research shows that companies using data analytics effectively are 5 times more likely to make rapid decisions compared to their peers, allowing them to face challenges with confidence.", ""),
    (OPSC, "For instance, a company that implemented value stream analysis reduced lead times by 30%, resulting in faster delivery to customers.",
           "Because most lead time is usually waiting between steps, value stream analysis often shortens delivery times without speeding up any single task."),
    (OPSC, "A successful reengineering project we managed resulted in a 50% reduction in operational costs for a client in the logistics sector.",
           "In logistics, for example, redesigning how orders are picked, checked and dispatched can remove whole steps rather than speeding them up."),
    (OPSC, "For instance, a gap analysis for an e-commerce client revealed a 20% higher return rate due to inefficiencies in their fulfillment processes.",
           "For instance, a gap analysis for an online retailer might show that its return rate is well above where it should be because of picking and packing errors."),
    (OPSC, "With a clear roadmap, one client successfully transitioned to an online sales model, increasing their revenue by 75% within just a few months.",
           "Businesses with a clear roadmap were able to move to online sales far faster than those starting from scratch."),
    (OPSC, "In the evolving business landscape, operational consulting serves", "Operational consulting serves"),
    # dual CEO
    (DUAL, "In today's fast-paced business environment, organizations face the pressing need for complex transformations.",
           "Large transformations, such as a merger, a new business model or a digital overhaul, stretch a single chief executive."),
    (DUAL, "In today’s fast-changing business landscape, leaders with different backgrounds and skill sets can provide significant value.",
           "Leaders with different backgrounds and skill sets can cover more of a complex agenda than one person."),
    (DUAL, " According to a study by McKinsey, organizations with diverse leadership teams can outperform their competitors by up to 35%. ", " "),
    (DUAL, " Research shows that companies engaged in strategic alliances can increase their innovation revenue by as much as 22%.", ""),
    (DUAL, " A survey by Deloitte found that organizations with dual leadership are 27% more successful at post-merger integration.", ""),
    (DUAL, "For example, clear communication can help mitigate anxiety about job roles—71% of employees feel more secure when leadership keeps them well-informed.",
           "Clear, consistent communication reduces anxiety about job roles during change."),
    (DUAL, "companies can adapt to the ever-changing business landscape with greater success.", "companies can carry out complex change with greater success."),
    (DUAL, "organizations can unlock the full potential of a dual CEO setup", "organizations can get the most from a dual CEO setup"),
    # local SEO
    (LOCAL, "In today’s digital world, small businesses need all the help they can get to stand out. ", ""),
    (LOCAL, "For example, 46% of all Google searches are local. That’s a significant number! By mastering local SEO",
            "Searches such as \"near me\", or a service plus a town name, are among the most valuable a small business can win, because the person is usually ready to buy. By mastering local SEO"),
    (LOCAL, " Studies show that businesses with a 4.0-star rating or higher on Google can see an increase in customer engagement of up to 20%.",
            " Google says that high-quality, positive reviews can improve your business's visibility."),
    (LOCAL, "With more than 50% of local searches being conducted on mobile devices, having a mobile-friendly website is a must.",
            "Many local searches happen on a phone, often on the way somewhere, so a mobile-friendly website is a must."),
    (LOCAL, " A site that is easy to use on mobile will likely lower your bounce rates, which are around 40% for sites that are not mobile-friendly.",
            " Visitors leave sites that are hard to use on a phone."),
    # dashboard
    (DASH, "In today’s fast-paced business world, measuring and analyzing performance is more important than ever. Management thinker Peter Drucker famously said, \"What’s measured, improves.\"",
           "A dashboard puts the handful of numbers that matter most in one place. The saying \"what gets measured gets managed\", often attributed to Peter Drucker, sums up why."),
    (DASH, "Embrace the idea that \"what's measured improves,\" and you can unlock new levels of success while ensuring your business thrives in a competitive landscape.",
           "Start with one dashboard, review it at a regular meeting, and act on what it shows."),
    # BPS
    (BPS, "After adopting a structured growth system, they improved project completion rates by 30% within six months.",
          "After adopting a structured growth system, more projects finished on time within six months."),
    (BPS, "companies can unlock their full potential and achieve lasting success.", "companies can grow steadily and keep improving."),
    # downturn
    (DOWN, "In today’s uncertain economic climate, businesses face critical challenges that can impact their financial well-being. From global recessions to local hardships, having effective cost control strategies is more important than ever.",
           "When sales slow, cost control decides which businesses come through in good shape."),
    (DOWN, "For instance, a small business that implements an automated payroll system can cut payroll processing costs by up to 40%.",
           "For instance, a small business that moves to an automated payroll service can cut the time spent on each pay run and reduce errors."),
    (DOWN, "Companies that actively engage employees can experience up to a 21% boost in profitability and are better equipped to tackle cost-saving initiatives.",
           "Gallup's research on employee engagement links highly engaged teams with higher productivity and profitability, and engaged people are also the best source of cost-saving ideas."),
    # OODA
    (OODA, "In today’s fast-paced business world, quick and informed decision-making is crucial for success. Organizations continually strive for improvement, creating a demand for effective frameworks. Two prominent options",
           "Some decisions must be made fast, against a changing situation; others are improvements that should be tested carefully. Two frameworks"),
    (OODA, "In manufacturing, Toyota is celebrated for its use of the PDCA Cycle as part of its Lean Six Sigma initiatives.",
           "In manufacturing, Toyota is known for building the PDCA cycle into daily problem solving as part of the Toyota Production System."),
    (OODA, " Reports indicate that the continuous improvement strategies led to a 50% reduction in manufacturing time for certain models.", ""),
    (OODA, "that drive sustainable growth in today’s competitive landscape.", "that drive sustainable growth."),
    # B2C
    (B2C, "In today's digital world, having a strong online marketing strategy is vital for B2C businesses seeking to increase engagement and drive sales.",
          "An online marketing strategy decides where a consumer business spends its time and money to win customers online."),
    (B2C, " In fact, companies that effectively use buyer personas in their marketing see a 73% increase in conversions.", ""),
    (B2C, "For local businesses, focus on local SEO; studies show that 46% of all Google searches seek local information.",
          "For local businesses, focus on local SEO."),
    (B2C, "For instance, running a giveaway on Instagram boosted engagement by 55% for one retail brand, enhancing brand visibility and attracting new followers.",
          "Giveaways and contests can raise engagement quickly, but measure whether the new followers ever buy."),
    (B2C, " According to studies, 49% of consumers depend on influencer recommendations, making it a powerful avenue for driving sales and brand trust.",
          " Choose influencers whose audience matches yours, and track sales with a unique code or link for each."),
    (B2C, "In 2023, the average open rate for emails in the retail sector was about 21.3%, showing the potential for high engagement if done right.",
          "Track open and click rates against your own past campaigns rather than published averages, which vary widely by industry and by how they are measured."),
    (B2C, " According to recent studies, a single-second delay in page loading can result in a 7% reduction in conversion rates.",
          " Slow pages lose buyers, so test your site's speed on a phone with Google's PageSpeed Insights."),
    (B2C, " Brands that base decisions on analytics typically enjoy 10-20% higher sales growth compared to those that do not.", ""),
    (B2C, "The digital marketing landscape is always changing.", "Platforms, algorithms and advertising rules change often."),
    (B2C, " In 2023, 75% of marketers cited staying updated with trends as crucial for their campaign's success.", ""),
    # cost reduction
    (COST, "In today's fiercely competitive business environment, cost reduction is vital for organizations aiming to boost profitability and improve efficiency. ",
           ""),
    (COST, " A study by the Lean Enterprise Institute found that companies that adopt process improvement strategies can increase their productivity by as much as 25%.", ""),
    (COST, " This tool has been shown to help organizations identify up to 30% of their wasted time.",
           " It usually shows that most of the elapsed time is waiting between steps rather than work."),
    (COST, "<li><strong>Pull Systems</strong>: Producing based on customer demand rather than forecasts can decrease excess inventory by as much as 40%.</li>",
           "<li><strong>Pull Systems</strong>: Producing based on customer demand rather than forecasts reduces excess inventory.</li>"),
    (COST, " Research suggests that automating tasks can increase efficiency by approximately 20% to 50%.", ""),
    (COST, "As a result of these targeted improvements, they reduced production costs by <strong>20%</strong> and improved lead times by <strong>30%</strong>.",
           "Targeted improvements reduced production costs and shortened lead times" + ILL + "."),
    (COST, "By automating routine inquiries and implementing a new ticketing system, they cut response times by over <strong>50%</strong>.",
           "By automating routine inquiries and implementing a new ticketing system, they cut response times sharply" + ILL + "."),
    # benchmark
    (BENCH, "In today's fast-paced business landscape, the ability to refine processes is essential for staying competitive. ", ""),
    (BENCH, " For example, firms that focus on process improvement can see productivity boosts of up to 20%. Additionally, better outcomes can lead to greater customer satisfaction, where an increase of just 5% in customer retention can result in profitability growth of 25% to 95%.",
            " Better processes also keep customers: Frederick Reichheld of Bain &amp; Company found that raising customer retention by five percentage points can increase profits by 25% to 95%."),
    (BENCH, "A financial services company might automate invoice processing, cutting handling time by up to 50%.",
            "A financial services company might automate invoice processing, so staff handle exceptions rather than every invoice."),
    (BENCH, "A well-trained team can work more efficiently, potentially increasing output by 30%.", "A well-trained team makes fewer errors and needs less supervision."),
    (BENCH, "stay agile in today’s ever-evolving business landscape.", "keep improving as conditions change."),
    (BENCH, "Start your journey toward process optimization today, and watch your business bloom.", "Pick one process this month, measure it, and compare it with a benchmark."),
    # backlinks
    (LINKS, "In today's fast-paced digital world, backlinks, brand mentions, and citations are essential for boosting your online presence.",
            "Backlinks, brand mentions and citations help search engines and customers decide whether to trust your business."),
    (LINKS, "In this post, we will delve into actionable strategies", "This post sets out practical strategies"),
    (LINKS, " For instance, sites with a substantial amount of quality backlinks can see their rankings improve by as much as 50% in search results.",
            " Links from relevant, respected sites count for far more than many links from weak ones."),
    (LINKS, " For example, when your brand is cited on a popular site, you can expect an increase in referral traffic by up to 30%.",
            " A mention on a popular site in your field can also send visitors directly."),
    (LINKS, " Research shows that businesses with consistent NAP information can rank up to 19% higher in local searches.",
            " Inconsistent details across directories confuse both customers and search engines."),
    (LINKS, "This exposure not only provided a valuable backlink but also boosted their brand awareness by 25%.",
            "This exposure provided a valuable backlink and introduced the brand to a new audience" + ILL + "."),
    (LINKS, "As a direct result, the business experienced a 30% increase in foot traffic and inquiries.",
            "Over the following months, the business saw more calls and visits from local searches" + ILL + "."),
]


# ───────────── 3. Figures ─────────────
def fig_dash():
    s = DEFS
    tiles = [("Sales this month", "$182k", "vs target $175k", GREEND), ("Gross margin", "31%", "target 30%", GREEND),
             ("On-time delivery", "88%", "target 95%", ORANGE), ("Overdue invoices", "$24k", "up from $15k", ORANGE)]
    for i, (h, v, sub, col) in enumerate(tiles):
        x = 10 + i * 182
        s += f'<rect x="{x}" y="10" width="170" height="92" rx="8" fill="#fff" stroke="#C9D3DE"/>'
        s += txt(x + 12, 32, h, fill=MUTED, fs=12) + txt(x + 12, 66, v, fill=NAVY, fs=24, bold=True) + txt(x + 12, 90, sub, fill=col, fs=12, bold=True)
    s += f'<rect x="10" y="114" width="352" height="120" rx="8" fill="#fff" stroke="#C9D3DE"/>' + txt(22, 136, "Weekly sales ($k)", fill=MUTED, fs=12)
    vals = [38, 42, 47, 44, 51]
    for i, v in enumerate(vals):
        h = v * 1.6; s += f'<rect x="{40 + i * 62}" y="{224 - h:.0f}" width="34" height="{h:.0f}" fill="{BLUE}" opacity=".85"/>'
        s += txt(57 + i * 62, 220 - h, str(v), "middle", NAVY, 11)
    s += f'<rect x="374" y="114" width="352" height="120" rx="8" fill="#fff" stroke="#C9D3DE"/>' + txt(386, 136, "Actions from this week's review", fill=MUTED, fs=12)
    for i, a in enumerate(["Late deliveries: check Line 2 schedule (Ops, Fri)", "Overdue invoices: call top 5 accounts (Finance, Wed)", "Margin on track: no action"]):
        s += txt(388, 162 + i * 24, "• " + a, fill=NAVY, fs=12)
    return svg("An example small-business dashboard: four tiles show sales this month of 182 thousand dollars against a 175 thousand target, gross margin "
               "31 percent against a 30 percent target, on-time delivery 88 percent against 95, and overdue invoices of 24 thousand dollars up from 15. "
               "A bar chart shows weekly sales rising from 38 to 51 thousand dollars, and a panel lists actions agreed at the weekly review.", 736, 244, s, 600)


def fig_ooda():
    s = DEFS
    def loop(cx, title, steps, col):
        out = txt(cx, 22, title, "middle", col, 15, True)
        pos = [(cx, 52), (cx + 110, 120), (cx, 188), (cx - 110, 120)]
        for i, (n, (x, y)) in enumerate(zip(steps, pos)):
            out += box(x - 52, y - 18, 104, 36, n, fill=PALE if col == BLUE else GREENF, stroke=col, fs=13)
        for (x1, y1), (x2, y2) in zip(pos, pos[1:] + pos[:1]):
            dx, dy = x2 - x1, y2 - y1
            out += arrow(x1 + dx * 0.36, y1 + dy * 0.36, x1 + dx * 0.66, y1 + dy * 0.66, col, 2)
        return out
    s += loop(185, "OODA loop: fast decisions", ["Observe", "Orient", "Decide", "Act"], BLUE)
    s += loop(551, "PDCA cycle: tested improvement", ["Plan", "Do", "Check", "Act"], GREEND)
    s += txt(185, 232, "Hours to days · changing situation", "middle", MUTED, 12) + txt(551, 232, "Weeks · stable process to improve", "middle", MUTED, 12)
    return svg("Two cycles side by side. The OODA loop runs observe, orient, decide, act, and suits fast decisions in a changing situation over hours to days. "
               "The PDCA cycle runs plan, do, check, act, and suits tested improvements to a stable process over weeks.", 736, 244, s, 600)


def fig_ready():
    s = DEFS
    dims = [("Business case", 4), ("Data", 2), ("Process", 3), ("Technology", 3), ("People and skills", 2), ("Governance", 1), ("Change management", 3)]
    s += txt(370, 22, "Score (1 = not started, 5 = established)", "middle", MUTED, 12)
    for i, (d, v) in enumerate(dims):
        y = 34 + i * 30
        s += txt(166, y + 15, d, "end", NAVY, 13, True)
        s += f'<rect x="180" y="{y + 3}" width="380" height="18" rx="4" fill="#EEF1F4"/>'
        col = GREEND if v >= 3 else ORANGE
        s += f'<rect x="180" y="{y + 3}" width="{v * 76}" height="18" rx="4" fill="{col}"/>' + txt(186 + v * 76, y + 16, str(v), fill=NAVY, fs=12, bold=True)
    s += txt(590, 70, "Fix first:", fill=ORANGE, fs=13, bold=True) + txt(590, 90, "governance, data,", fill=NAVY, fs=12.5) + txt(590, 108, "people and skills", fill=NAVY, fs=12.5)
    return svg("An example AI readiness scorecard rating seven dimensions from 1 to 5: business case 4, data 2, process 3, technology 3, people and skills 2, "
               "governance 1 and change management 3. The lowest scores, governance, data and people, are the ones to fix first.", 736, 250, s, 600)


# ───────────── 3. New sections: (slug, id, html, where) — where = "START" | "END" | regex anchor ─────────────
def note(text):
    return f'<blockquote data-note="v482">{text}</blockquote>\n'


BOOKS = [(ATOMIC, "Atomic Habits"), (EMYTH, "The E-Myth Revisited"), (ONE, "The ONE Thing"), (FAST, "The Millionaire Fastlane"), (MONEY, "The Psychology of Money"),
         (NVIDIA, "The Nvidia Way"), (ARTWAR, "The Art of the Deal vs The Art of War")]


def more_reviews(me, extra=""):
    items = "; ".join(L(s, t) for s, t in BOOKS if s != me)
    return f'<h2>More book reviews</h2>\n<p>{extra}Other reviews on Chmltech: {items}.</p>\n'


ADD = [
    (ATOMIC, "books", more_reviews(ATOMIC, f'Test what you remember with our {P("atomic-habits.html", "Atomic Habits quiz")}. '), "END"),
    (EMYTH, "books", more_reviews(EMYTH, f'Gerber\'s idea of working on the business, not in it, is the starting point of an operating system for a small company; see our {P("eos.html", "EOS implementation")} and {P("leadership-operating-system.html", "leadership operating system")} pages. '), "END"),
    (ONE, "books", more_reviews(ONE), "END"),
    (FAST, "books", more_reviews(FAST), "END"),
    (MONEY, "books", more_reviews(MONEY, f'Test what you remember with our {P("psychology-of-money.html", "Psychology of Money quiz")}. '), "END"),
    (ARTWAR, "books", more_reviews(ARTWAR), "END"),
    (NVIDIA, "books", more_reviews(NVIDIA), "END"),
    (MISTAKES, "links", f'<h2>Getting help</h2>\n<p>Many first businesses in Canada qualify for government funding or advisory programmes. Our {P("funding.html", "funding finder")} lists the main ones, and {P("plans-pricing.html", "plans and pricing")} explains how we work with new and growing businesses.</p>\n', "END"),
    (PPM1, "series", note(f'<strong>Project portfolio management, part 1 of 2.</strong> This part covers aligning projects with business goals. Part 2, {L(PPM2, "benchmarking your PPM maturity")}, shows how to assess and improve your practice. See also our {P("project-portfolio-management.html", "project portfolio management service")}.'), "START"),
    (PPM2, "series", note(f'<strong>Project portfolio management, part 2 of 2.</strong> Part 1, {L(PPM1, "achieving success with project portfolio management")}, covers aligning projects with business goals. See also our {P("project-portfolio-management.html", "project portfolio management service")}.'), "START"),
    (FIRST, "example", f"""<h2>Worked example: questioning a cost assumption</h2>
<p>A distributor believes freight costs are fixed by the market. Breaking the problem down to fundamentals gives a different picture:</p>
{table(["Assumption", "First-principles question", "What they found"], [
    ("Freight rates are set by the carriers", "What actually drives our cost per shipment?", "Shipment size and urgency, not the rate card"),
    ("Customers need next-day delivery", "Which customers, for which items?", "Only a small group of urgent orders needed it"),
    ("Small orders must ship separately", "Could orders be consolidated?", "Two fixed delivery days per region cover most customers"),
])}
<p>The distributor introduced scheduled regional deliveries, kept an express option for genuinely urgent orders at a charge, and reduced freight cost per order without changing carriers. The example is illustrative; the method is to separate what must be true from what has simply always been done.</p>
""", "END"),
    (REV, "example", f"""<h2>Worked example: choosing where to start</h2>
<p>A small commercial cleaning company has $400,000 in annual revenue from 40 clients. It compares three options by effort and likely return:</p>
{table(["Option", "What it involves", "Likely effect"], [
    ("Raise prices 5% at renewal", "Letters to clients; explain the service and costs", "About $20,000 a year if most clients stay"),
    ("Add a periodic deep-clean service", "Price list; offer to existing clients", "New revenue from clients who already trust you"),
    ("Win new clients through referrals", "Ask satisfied clients; small referral reward", "Slower, but builds the base"),
])}
<p>It starts with the price review and the add-on service, because both use existing relationships, and tracks the results each month. The figures are illustrative.</p>
""", "END"),
    (SCEN, "example", f"""<h2>Worked example: three demand scenarios</h2>
<p>A building-products distributor plans next year's inventory. Instead of one forecast, it builds three scenarios from its sales history, housing-start forecasts and interest-rate outlook:</p>
{table(["Scenario", "Assumption", "Sales", "Inventory plan"], [
    ("Downside", "Housing starts fall; rates stay high", "−10%", "Cut orders of slow movers; keep fast movers"),
    ("Base", "Market flat", "0%", "Hold current stock levels"),
    ("Upside", "Rates fall; renovation demand rises", "+12%", "Agree extra supply with two key vendors, to be confirmed by spring"),
])}
<p>A predictive model then updates the probability of each scenario monthly as new data arrives, and the purchasing plan shifts accordingly. The figures are illustrative; the value is in deciding in advance what you will do in each case.</p>
""", "END"),
    (LOCAL, "gbp", f"""<h2>Setting up your Google Business Profile: step by step</h2>
<ol>
<li><strong>Claim or create the profile</strong> at Google Business Profile and verify it (by video, phone, email or postcard, depending on what Google offers).</li>
<li><strong>Choose the right primary category</strong>; it matters more than any other field. Add a few secondary categories only if they truly apply.</li>
<li><strong>Complete every field:</strong> name exactly as on your signage, address or service area, phone, website, hours and holiday hours.</li>
<li><strong>Add services or products</strong> with short descriptions and prices where possible.</li>
<li><strong>Upload real photos</strong> of your premises, team and work, and add new ones regularly.</li>
<li><strong>Ask for reviews</strong> after each job with a direct link, and reply to every review, good or bad.</li>
<li><strong>Post updates</strong> such as offers, events or new work a few times a month.</li>
<li><strong>Check the performance report</strong> monthly: searches, calls, direction requests and website clicks.</li>
</ol>
<p>AI search tools also draw on business profiles and reviews; see {L("the-key-differences-between-seo-and-geo-for-enhancing-your-online-presence", "SEO vs GEO: being found in Google and in AI answers")}.</p>
""", "END"),
    (DASH, "figure", f"""<h2>What a small-business dashboard can look like</h2>
{fig(fig_dash(), 1, "An example weekly dashboard: four headline numbers with targets, one trend, and the actions agreed at the review. The figures are illustrative.")}
<p>Keep it to one screen, show each number against a target, and record the actions agreed when you review it. For choosing the measures, see {L("50-must-track-kpis-for-business-success-from-finance-to-product-development", "50 KPIs to track, from finance to product development")}; for factories, {L("what-oee-really-measures", "what OEE really measures")} explains the most common production measure.</p>
""", "END"),
    (BPS, "links", f'<h2>Related reading</h2>\n<p>A business performance system is one form of a business operating system. See our {P("leadership-operating-system.html", "leadership operating system")} and {P("eos.html", "EOS implementation")} pages, and {L("navigating-complex-transformations-with-a-dual-ceo-structure", "dual CEO structures for complex transformations")}.</p>\n', "END"),
    (DOWN, "links", f'<h2>Related reading</h2>\n<p>For lasting savings rather than one-off cuts, see {L(COST, "how to reduce costs with process improvement")}. For federal measures that can ease cash flow, such as tax incentives for investment, see {L("canada-budget-2026-what-manufacturers-and-process-plants-should-know", "Canada Budget 2026: what manufacturers should know")}.</p>\n', "END"),
    (COST, "links", f'<p>During a slowdown, combine these with short-term measures; see {L(DOWN, "ten strategies to manage costs during an economic downturn")}.</p>\n', "END"),
    (OODA, "figure", f"""<h2>The two cycles side by side</h2>
{fig(fig_ooda(), 1, "OODA suits fast decisions in a changing situation; PDCA suits tested improvements to a stable process.")}
""", r'<h2[^>]*>(?:<strong>)?Key Differences Between OODA and PDCA'),
    (BENCH, "links", f'<p>Benchmarking shows how far you are from where you want to be; {L("bridging-the-gap-a-step-by-step-guide-to-conducting-a-gap-analysis-for-operational-efficiency", "a gap analysis")} turns that into a plan.</p>\n', "END"),
    (AIREADY, "figure", f"""<h2>Example: a readiness scorecard</h2>
{fig(fig_ready(), 1, "Score each dimension from 1 to 5 with the people who do the work, then fix the lowest scores first. The scores shown are an example.")}
<p>For what needs to be in place before AI tools act on their own, see our journal paper on {L("agent-readiness-for-small-and-mid-sized-firms-data-process-staged-adoption", "agent readiness for small and mid-sized firms")}. To connect AI tools, data and governance into one working system, see our {P("ai-operating-system.html", "AI operating system")} service.</p>
""", r'<h2[^>]*>Practical AI Readiness Roadmap'),
    (DATA, "links", f'<h2>Related reading</h2>\n<p>Data is one of seven readiness areas; see {L(AIREADY, "AI readiness: preparing your organization for AI adoption")} for the others, and our journal paper on {L("agent-readiness-for-small-and-mid-sized-firms-data-process-staged-adoption", "agent readiness for small and mid-sized firms")} for the data needed before AI agents act on their own.</p>\n', "END"),
]


def body_of(s):
    m = re.search(r'(<article class="prose">)(.*?)(</article>)', s, re.S)
    return m, m.group(2)


def insert(b, nid, html, where):
    if f'data-v482="{nid}"' in b:
        if html.startswith("<blockquote"): return b
        return re.sub(r'<section data-v482="' + nid + r'">.*?</section>\n', lambda m: f'<section data-v482="{nid}">\n{html}</section>\n', b, count=1, flags=re.S)
    blk = f'<section data-v482="{nid}">\n{html}</section>\n' if not html.startswith("<blockquote") else html.replace('data-note="v482"', f'data-note="v482" data-v482="{nid}"')
    if where == "START":
        b = re.sub(r'^\s*<details class="a-toc-m" data-toc.*?</details>\n?', "", b, flags=re.S)   # article_toc re-adds it after the note
        return blk + b.lstrip()
    if where == "END":
        m = re.search(r'<p data-readnext|<h2[^>]*>(?:<strong>)?(?:Sources|Related reading)\b', b)
        at = m.start() if m else len(b)
        return b[:at] + blk + b[at:]
    m = re.search(where, b)
    assert m, (nid, where)
    return b[:m.start()] + blk + b[m.start():]


def recat_nvidia():
    """Move the Nvidia Way card to Book Review, Strategy and AI; adjust the category counts."""
    import add_article as A
    old, new = ["process-improvement", "operational-efficiency", "artificial-intelligence"], ["book-review", "strategy", "artificial-intelligence"]
    for f in [os.path.join(ROOT, "insights.html")] + [os.path.join(ROOT, "post", x) for x in os.listdir(os.path.join(ROOT, "post"))]:
        s = open(f, encoding="utf-8").read()
        card = r'<article class="article" data-cats="' + re.escape(" ".join(old)) + r'"(?:(?!</article>).)*?' + NVIDIA + r'\.html.*?</article>'
        t = re.sub(card, lambda m: m.group(0).replace(f'data-cats="{" ".join(old)}"', f'data-cats="{" ".join(new)}"', 1)
                   .replace('<p class="cat-label">Process Improvement</p>', '<p class="cat-label">Book Review</p>', 1), s, flags=re.S)
        if f.endswith("insights.html") and t != s:
            for c in set(old) - set(new): t = A.bump(t, r'(data-cat="' + c + r'" aria-pressed="false">[^<(]*\()(\d+)(\)<)', -1)
            for c in set(new) - set(old): t = A.bump(t, r'(data-cat="' + c + r'" aria-pressed="false">[^<(]*\()(\d+)(\)<)', 1)
        if t != s: open(f, "w", encoding="utf-8").write(t); print("recat", os.path.basename(f))


def run():
    missing = []
    for slug in SLUGS:
        p = os.path.join(ROOT, "post", slug + ".html")
        s = open(p, encoding="utf-8").read()
        m, b = body_of(s)
        for sl, old, new in R:
            if sl != slug: continue
            if old in b: b = b.replace(old, new, 1)
            elif not (new and new in b): missing.append((slug[:40], old[:70]))
        for sl, nid, html, where in ADD:
            if sl == slug: b = insert(b, nid, html, where)
        t = s[:m.start(2)] + b + s[m.end(2):]
        if t != s: open(p, "w", encoding="utf-8").write(t); print("updated", slug[:60])
    recat_nvidia()
    for x in missing: print("NOT FOUND", x)


if __name__ == "__main__":
    run()
