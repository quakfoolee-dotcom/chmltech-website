"""V4.81: 2025 posts upgraded (audit plan V8). Several 2025 posts carried statistics that could not be traced to a source,
so the ones below are rewritten in full at their address, keeping the original publish date; numbers are either sourced
or presented as illustrative worked examples.

Rewritten:
1. how-shopify-and-lovable-are-empowering-aspiring-entrepreneurs-to-launch-online-stores   what the integration actually does
2. 6-essential-steps-to-streamline-and-enhance-your-sales-process                          sales process, with stage table
     retired into it: why-a-strong-sales-process-is-essential-and-how-it-helps-increase-revenue
3. 6-mckinsey-principles-to-unlock-creative-thinking-and-innovation                         retitled: six practices, no McKinsey claim
4. adapting-business-operations-for-enhanced-agility-and-market-competitiveness             operational agility
5. how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations                  Lean with waste walk and value stream map

Merged:   boost-your-search-rankings-with-ai-powered-seo-strategies -> SEO vs GEO (new section SEO_AI, refresh_articles.seo)
In place: 5-proven-steps-to-integrate-ai-into-your-operations-workflow-... gains a worked example (v481_inplace.py)
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, MUTED, LINE, SAND, PALE, GREENF, ORANGEF
from v478_articles import src, rel, money, table, words, art, steps_fig
from v481_extra import EXTRA

SHOP = "how-shopify-and-lovable-are-empowering-aspiring-entrepreneurs-to-launch-online-stores"
SALES = "6-essential-steps-to-streamline-and-enhance-your-sales-process"
INNOV = "6-mckinsey-principles-to-unlock-creative-thinking-and-innovation"
AGILE = "adapting-business-operations-for-enhanced-agility-and-market-competitiveness"
LEAN = "how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations"
SEOGEO = "the-key-differences-between-seo-and-geo-for-enhancing-your-online-presence"
AISTEPS = "5-proven-steps-to-integrate-ai-into-your-operations-workflow-for-smarter-faster-results"
RETIRE = {SALES: ["why-a-strong-sales-process-is-essential-and-how-it-helps-increase-revenue"],
          SEOGEO: ["boost-your-search-rankings-with-ai-powered-seo-strategies"]}
ORIGINAL = {SHOP: "2025-10-28", SALES: "2025-10-30", INNOV: "2025-11-03", AGILE: "2025-11-04", LEAN: "2025-11-04"}


# ═════════════════════════ 1. Shopify and Lovable ═════════════════════════
def shop():
    roles = [("Shopify", "The commerce engine: products, inventory, checkout, payments, taxes, shipping, orders and a large app ecosystem", "Monthly plan plus payment processing fees"),
             ("Lovable", "An AI app builder: you describe the storefront in plain language and it generates the site and its code", "Free tier with daily credits; paid plans from about $25 a month, with credits used per change"),
             ("You", "The products, brand, prices, photos, policies and customer service", "Your time, stock and marketing")]
    body = f"""
<p>Since late 2025, Lovable, an AI app builder, has offered an official integration with Shopify that lets you build an online store by describing it in plain language. This article was first published in October 2025, shortly after the launch. It has been rewritten to explain what the integration actually does and does not do, what it costs, and when it makes sense for a new or small business. The earlier version included statistics we could not trace to a source; those have been removed.</p>
<h2>Who does what</h2>
{table(["Part", "Role", "Cost"], roles)}
<p>The important point is the division of labour. Lovable builds the storefront, the pages customers see. Shopify still runs the business underneath: checkout, payments, taxes, orders and inventory. Lovable does not analyse your customers or make sales recommendations on its own; that comes from Shopify's tools and apps, or from your own analysis.</p>
<h2>How it works</h2>
<ol>
<li><strong>Describe the store</strong> in a Lovable project, for example "a store for handmade candles with a calm, natural look and three featured products".</li>
<li><strong>Connect Shopify.</strong> Lovable can set up a new test (sandbox) store or connect to an existing Shopify store.</li>
<li><strong>Add and edit products</strong>, including AI-drafted descriptions you should check and rewrite in your own voice.</li>
<li><strong>Refine by chatting:</strong> change layouts, colours, sections and copy by describing what you want.</li>
<li><strong>Claim and publish</strong> the store in Shopify, choose a plan, set up payments, shipping and taxes, and go live.</li>
</ol>
<h2>What it costs</h2>
<p>Shopify's plans for a full online store start at its Basic plan, which in 2026 costs about $39 a month in the United States when billed monthly, with a discount for annual billing; Grow and Advanced cost more, and each sale also carries a card processing fee that falls as you move up plans. Lovable has a free tier with a small number of daily credits, and paid plans from about $25 a month for a monthly allowance of credits, where each request for a change uses credits. Shopify apps, a domain, photography and marketing come on top. Check both vendors' pricing pages in Canadian dollars before you budget; both changed their plans during 2026.</p>
<h2>When it makes sense</h2>
{table(["Situation", "Good fit?", "Why"], [
    ("Testing a product idea quickly", "Yes", "A presentable store in hours, not weeks, so you can test demand cheaply"),
    ("A custom look beyond standard themes", "Yes, with care", "The AI can produce distinctive designs, but you own maintaining the code"),
    ("A small catalogue, simple shipping", "Yes", "Few products and settings to configure"),
    ("An existing store that works well", "Rarely", "A standard Shopify theme with good content is easier to maintain"),
    ("Complex B2B pricing, many variants, integrations", "Not alone", "Needs Shopify configuration and apps, and often a developer"),
])}
<h2>Things to watch</h2>
<ul>
<li><strong>Maintenance.</strong> A storefront generated as custom code is yours to keep working as Shopify and browsers change. A standard theme gets updates from its developer.</li>
<li><strong>Credits add up.</strong> Many small change requests use credits quickly; plan your changes and batch them.</li>
<li><strong>Content still matters most.</strong> AI-generated product text is generic. Your own descriptions, photos and policies are what convert visitors and rank in search; see <a href="../post/10-proven-ways-to-boost-traffic-to-your-ecommerce-website.html">growing a small online store</a>.</li>
<li><strong>Check the basics before launch:</strong> mobile speed, checkout, shipping rates, taxes, returns policy and privacy policy.</li>
</ul>
<h2>Worked example: testing a product idea</h2>
<p>A maker wants to know whether a range of handmade cutting boards will sell online before investing in stock. Using the integration, she builds a store in an afternoon with five products, publishes it on a Shopify Basic plan, and spends a modest amount on social ads over a month. Her costs for the test are the Shopify plan, a Lovable paid plan for a month, a domain and the ads. At the end of the month she has real data: visits, add-to-cart rate, orders and questions from customers. That evidence, not the store itself, is what the tool buys her. The approach is illustrative; the point is to treat an AI-built store as a fast, cheap experiment.</p>
"""
    r = [("10-proven-ways-to-boost-traffic-to-your-ecommerce-website", "Growing a small online store"),
         ("5-tips-to-drive-more-website-traffic-from-instagram", "Instagram and social media for small businesses"),
         ("harnessing-the-power-of-prompt-engineering-transforming-businesses-with-chatgpt", "Prompting AI models for business work")]
    s = [("Shopifreaks: Lovable launches a Shopify integration (October 2025)", "https://www.shopifreaks.com/lovable-launches-a-shopify-integration-but-does-anyone-need-it/"),
         ("GemPages: What is the Lovable Shopify integration?", "https://gempages.net/blogs/shopify/lovable-shopify-integration"),
         ("Sellfy: Shopify pricing 2026", "https://sellfy.com/blog/shopify-pricing/"),
         ("Costbench: Lovable plans and pricing", "https://costbench.com/software/ai-coding-assistants/lovable/")]
    body += EXTRA["shop"]
    return art(SHOP, "Building a Shopify Store with Lovable: What the AI Integration Does, Costs and Suits",
               "What the Lovable Shopify integration actually does, how it works step by step, 2026 costs, when it makes sense, what to watch and a worked product-test example.",
               ["marketing", "digital-technology", "artificial-intelligence"], ["Shopify", "Lovable", "AI store builder", "e-commerce", "no-code", "online store"], body, "E-commerce", r, s)


# ═════════════════════════ 2. Sales process ═════════════════════════
def sales():
    stages = [("1. Lead", "A person or company has shown interest or fits your target", "Logged in CRM with source", "Response within one working day"),
              ("2. Qualified", "Real need, budget or funding, decision-maker known, timing", "Qualifying call notes; next step agreed", "Share of leads qualified"),
              ("3. Needs understood", "Requirements, constraints and success criteria agreed", "Discovery notes or site visit; scope", "Time from lead to proposal"),
              ("4. Proposal", "Price and scope sent", "Quote or proposal in CRM; follow-up date", "Proposal win rate"),
              ("5. Negotiation", "Questions, changes and terms being settled", "Revised quote; decision date", "Days in stage"),
              ("6. Won or lost", "Order received, or a clear no", "Order entered; loss reason recorded", "Win rate; reasons for loss")]
    body = f"""
<p>A sales process is the agreed set of steps your business takes from first contact to a signed order, with clear rules for what happens at each step. Without one, every salesperson works differently, follow-ups depend on memory, and forecasting is a guess. This article brings together two posts from late 2025, one on streamlining the sales process and one on why a strong process matters. Both have been rewritten, with a stage table and a worked example; statistics we could not trace to a source have been removed.</p>
<h2>Why a defined process pays</h2>
<ul>
<li><strong>Fewer lost opportunities:</strong> every lead has an owner and a next step.</li>
<li><strong>Faster onboarding:</strong> new salespeople learn one way of working.</li>
<li><strong>Better forecasts:</strong> deals in each stage can be counted and weighted.</li>
<li><strong>Clear problems:</strong> when deals stall, you can see at which stage.</li>
<li><strong>Customer experience:</strong> buyers get consistent, timely responses.</li>
</ul>
<h2>Step 1: map how you sell today</h2>
<p>Take five recent wins and five losses and trace each from first contact to outcome: who did what, how long each step took, and where it waited. The real process is often different from the one people describe, and the differences point to the fixes.</p>
<h2>Step 2: define the stages</h2>
<p>Each stage needs an entry rule (what must be true to be in it), a required action and a measure. A typical business-to-business process looks like this:</p>
{table(["Stage", "Definition", "What must be recorded", "Measure"], stages)}
<h2>Step 3: choose a few measures</h2>
<p>Track new leads by source, conversion from stage to stage, average deal size, sales cycle length and win rate. Customer acquisition cost (what you spend on sales and marketing per new customer) is worth calculating once a quarter. Compare yourself with your own trend rather than general industry averages, which vary too widely to be useful.</p>
<h2>Step 4: build follow-up into the process</h2>
<p>Most lost deals are not lost to a competitor but to silence. Agree a follow-up rule for each stage, such as a call within two days of sending a proposal and a check-in every week until a decision, and let your CRM create the reminders.</p>
<h2>Step 5: use technology to support it</h2>
<p>A CRM holds the pipeline, reminders and history; email and calendar integration logs activity without typing; quoting tools speed up proposals. See <a href="../post/choosing-the-right-crm-system-how-to-make-the-best-choice-for-your-business.html">choosing a CRM</a>. Configure the CRM to match your stages, not the other way round.</p>
<h2>Step 6: forecast and improve</h2>
<p>Multiply the value of deals in each stage by the historical win rate from that stage to get a weighted forecast. Review the pipeline weekly and the process quarterly: which stage loses most deals, and why?</p>
<h2>Worked example: finding the weak stage</h2>
<p>An industrial equipment supplier reviews a year of deals: 240 leads, 120 qualified, 90 with needs understood, 60 proposals and 15 wins. The drop from proposal to win is the steepest: only one proposal in four is won. Loss reasons show most lost proposals went quiet after the quote was sent. The team adds a follow-up call within two days of every proposal and a short summary of the customer's success criteria at the top of each quote. If the win rate on proposals rises from 25% to 33%, the same pipeline produces about 20 wins instead of 15. The figures are illustrative.</p>
<h2>Common mistakes</h2>
<ul>
<li>Stages that describe what the salesperson did rather than where the buyer is.</li>
<li>No loss reasons recorded, so nothing is learned from lost deals.</li>
<li>A CRM set up before the process is agreed.</li>
<li>Reviewing revenue only, not the stage conversion that drives it.</li>
</ul>
"""
    r = [("choosing-the-right-crm-system-how-to-make-the-best-choice-for-your-business", "Choosing a CRM for a small business"),
         ("introduction-to-leads-to-cash-for-saas-self-serve-model", "Lead-to-cash: from enquiry to payment"),
         ("how-to-build-a-predictable-and-scalable-sales-model-lessons-from-predictable-revenue-by-aaron-ros", "Predictable Revenue: review and lessons")]
    body += EXTRA["sales"]
    return art(SALES, "How to Build and Streamline a Sales Process: Stages, Measures and a Worked Example",
               "Why a defined sales process pays, six steps to build one, a pipeline stage table with entry rules and measures, forecasting, and a worked example.",
               ["marketing", "digital-technology"], ["sales process", "sales pipeline", "CRM", "sales forecasting", "win rate", "B2B sales"], body, "Sales", r)


# ═════════════════════════ 3. Innovation ═════════════════════════
def innov():
    practices = [("Start from the customer's problem", "Watch and interview customers; define the problem before ideas", "Design thinking: empathize, define, ideate, prototype, test"),
                 ("Make curiosity part of leadership", "Leaders ask questions, admit what they do not know, and reward good questions", "Regular 'what would have to be true?' discussions"),
                 ("Mix perspectives", "Teams that combine roles, backgrounds and customer contact see more options", "Include front-line staff and a customer-facing person in every idea session"),
                 ("Run small, cheap experiments", "Test ideas quickly with real users before investing", "Prototypes, pilots, mock-ups, one-week trials"),
                 ("Make ideas visible", "Sketches, storyboards and simple models make ideas easier to discuss and improve", "Whiteboards, journey maps, paper prototypes"),
                 ("Work in short cycles", "Plan, build, review and adjust every few weeks", "Two- to four-week sprints with a review")]
    body = f"""
<p>Creative thinking and innovation are not reserved for large companies with research labs. In a small or mid-sized business, most useful innovation is practical: a better way to serve a customer, a new service built on existing skills, a product variant, a process that removes a common frustration. This article was first published in November 2025 under a title that attributed six principles to McKinsey &amp; Company. We could not find a McKinsey source for that list, so the article has been rewritten and retitled; the six practices below are widely used approaches, described in our own words.</p>
<h2>Six practices that build innovation</h2>
{table(["Practice", "What it means", "How to use it"], practices)}
<h2>1. Start from the customer's problem</h2>
<p>Design thinking is a structured way of doing this: understand the people you serve, define their problem precisely, generate many ideas, build quick prototypes and test them with real users. The discipline is in not jumping to solutions. A clear problem statement, such as "contractors cannot get a firm delivery date when they order", produces better ideas than "improve the customer experience".</p>
<h2>2. Make curiosity part of leadership</h2>
<p>Teams copy what leaders do. A manager who asks why, listens to the answer and changes course when the evidence says so gives others permission to do the same. One practical habit: in every review, ask what assumption the plan depends on most, and how it could be tested cheaply.</p>
<h2>3. Mix perspectives</h2>
<p>People who do the same job tend to see the same options. Bring together sales, operations, finance and someone who talks to customers daily. In a small firm, inviting a trusted customer or supplier to an idea session can be the most productive change of all.</p>
<h2>4. Run small, cheap experiments</h2>
<p>Most ideas fail, so the goal is to fail cheaply and learn quickly. Before building a new service, describe it on one page and ask five customers whether they would buy it. Before changing a process across the company, trial it with one team for two weeks. Set a clear success measure before the test starts.</p>
<h2>5. Make ideas visible</h2>
<p>A rough sketch, a storyboard of a customer's experience or a cardboard model gets better feedback than a description. Visible ideas are easier to criticize constructively and improve. Tools can be as simple as a whiteboard and sticky notes.</p>
<h2>6. Work in short cycles</h2>
<p>Agile methods, borrowed from software development, work for many kinds of improvement: agree a short goal, work on it for two to four weeks, review what was learned and decide the next step. Short cycles keep momentum and limit the cost of a wrong turn.</p>
<h2>Worked example: a new service from existing skills</h2>
<p>A small engineering firm hears the same request from several clients: help preparing documents for a regulatory audit. Instead of launching a new service line, the team writes a one-page offer, tests it with three existing clients at a reduced price, and documents what each engagement needed. After the three pilots, they have a standard checklist, a realistic price and two testimonials, and the new service is launched with evidence behind it. The example is illustrative; the pattern of problem, small test, learning and then scale is the point.</p>
<h2>Protecting time for it</h2>
<p>Innovation competes with daily work and usually loses. Protect a small, regular slot: an hour a month for the leadership team to review ideas, or a quarterly half-day workshop with a mixed group. Keep a simple idea log, decide on each idea within a month, and tell people what happened to theirs.</p>
"""
    r = [("what-are-the-core-values-of-process-improvement-part-i", "The core values of process improvement"),
         ("perform-kaizen-event", "How to run a Kaizen event"), ("change-management-toolkit-the-top-10-models-and-how-to-choose-the-right-one-for-your-organization", "Change management toolkit")]
    body += EXTRA["innov"]
    return art(INNOV, "Six Practices to Build Creative Thinking and Innovation in a Small Business",
               "Six practical ways to build creative thinking and innovation: start from customer problems, curious leadership, mixed teams, small experiments, visible ideas and short cycles.",
               ["process-improvement", "change-management", "operational-efficiency"], ["innovation", "creative thinking", "design thinking", "experiments", "agile", "small business"], body, "Innovation", r)


# ═════════════════════════ 4. Agility ═════════════════════════
def agile():
    levers = [("Visibility", "Know quickly when something changes", "Weekly scorecard; demand and order trends; customer feedback"),
              ("Flexible capacity", "Shift people and equipment to where demand is", "Cross-training; a skills matrix; agreed overtime and subcontract options"),
              ("Shorter lead times", "Respond faster without more stock", "Smaller batches; quicker changeovers; fewer approval steps"),
              ("Supplier options", "Avoid single points of failure", "Second sources for critical items; shared forecasts with key suppliers"),
              ("Decision speed", "Decide at the right level, quickly", "Clear authority limits; a weekly meeting that decides, not just reports"),
              ("Automation", "Handle more volume without proportional hiring", "Integrations, automated data entry, self-service for routine requests")]
    skills = [("Ana", "✓", "✓", "✓", "—"), ("Ben", "✓", "—", "✓", "✓"), ("Chris", "—", "✓", "✓", "—"), ("Dana", "✓", "✓", "—", "✓")]
    body = f"""
<p>Operational agility is the ability to change what you make, how much and how fast, without chaos or large extra cost. Demand shifts, a key supplier fails, a new competitor appears, a customer asks for something different: agile businesses adjust within days or weeks, while others take months. This article, first published in November 2025, has been rewritten as a practical guide; the earlier version quoted figures we could not trace to sources, and those have been removed.</p>
<h2>What drives change</h2>
<ul>
<li><strong>Customers:</strong> new requirements, shorter delivery expectations, sustainability questions.</li>
<li><strong>Economy:</strong> interest rates, inflation and trade policy that change demand and costs.</li>
<li><strong>Technology:</strong> new tools, including AI, that change what competitors can offer.</li>
<li><strong>Supply:</strong> supplier failures, shortages and price swings.</li>
<li><strong>People:</strong> retirements, hiring difficulty and changing expectations of work.</li>
</ul>
<h2>Six levers of operational agility</h2>
{table(["Lever", "Purpose", "Practical steps"], levers)}
<h2>A skills matrix: the simplest agility tool</h2>
<p>A skills matrix shows who can do which job. It makes cross-training visible and shows where one absence would stop work.</p>
{table(["Person", "Cutting", "Welding", "Assembly", "Shipping"], skills)}
<p>In this small example, welding depends on two people and shipping on two; cross-training one more person in each removes the risk. Review the matrix monthly and plan training from it.</p>
<h2>Worked example: absorbing a demand swing</h2>
<p>A fabricator's largest customer doubles its order for a quarter at short notice. A business with fixed roles and a long approval chain would turn the order away or miss dates. This business uses its skills matrix to move two assemblers onto the bottleneck process, switches to smaller batches so urgent jobs flow through, agrees overtime at the constraint only, and asks its steel supplier to hold extra stock against a shared forecast. It delivers the order with modest overtime and no new hires. The example is illustrative; each step uses one of the six levers above.</p>
<h2>Agile ways of working beyond IT</h2>
<p>Agile methods, developed for software, are now used for many improvement projects: short cycles of two to four weeks, a visible list of work, regular reviews with the people affected, and the freedom to change direction based on what is learned. They suit projects where the answer is not known in advance, such as a new service or a process redesign. They suit less well work that is already well understood and simply needs doing.</p>
<h2>Measuring agility</h2>
{table(["Measure", "What it tells you"], [
    ("Order-to-delivery lead time", "How quickly you can respond to a new order"),
    ("Changeover time at the constraint", "How easily you can switch between products"),
    ("Share of staff trained in two or more roles", "How flexible your capacity is"),
    ("Critical items with a second source", "How exposed you are to one supplier"),
    ("Time from problem raised to decision", "How fast the organization decides"),
])}
<h2>Where to start</h2>
<p>Pick the lever that would have helped most in your last disruption. For many small firms it is cross-training or supplier options, both inexpensive. Our guides on <a href="../post/things-you-need-to-know-about-the-theory-of-constraints-toc.html">the theory of constraints</a>, <a href="../post/perform-kaizen-event.html">Kaizen events for changeover reduction</a> and <a href="../post/sales-and-operations-planning-for-small-manufacturers.html">sales and operations planning</a> go deeper on specific levers.</p>
"""
    r = [("sales-and-operations-planning-for-small-manufacturers", "Sales and operations planning for small manufacturers"),
         ("things-you-need-to-know-about-the-theory-of-constraints-toc", "The theory of constraints"),
         ("how-to-increase-operational-efficiency-for-small-business", "Operational efficiency for small businesses")]
    body += EXTRA["agile"]
    return art(AGILE, "Operational Agility for Small and Mid-Sized Businesses: Six Levers and a Worked Example",
               "What operational agility means, what drives change, six levers from visibility to automation, a skills matrix, a worked demand-swing example and how to measure it.",
               ["process-improvement", "change-management", "lean"], ["operational agility", "cross-training", "skills matrix", "resilience", "lead time", "agile"], body, "Agility", r)


# ═════════════════════════ 5. Lean ═════════════════════════
VSM = [("Cut", 2, 0.5), ("Weld", 3, 1.5), ("Paint", 4, 1.0), ("Assemble", 1, 2.0), ("Ship", 2, 0.2)]   # (step, days waiting before it, hours of work)


def fig_vsm():
    s = DEFS
    for i, (n, wait, work) in enumerate(VSM):
        x = 60 + i * 136
        s += f'<polygon points="{x - 40},70 {x - 27},46 {x - 14},70" fill="{ORANGEF}" stroke="{ORANGE}"/>' + txt(x - 27, 65, "I", "middle", ORANGE, 12, True)
        s += box(x, 36, 80, 44, n, fill=PALE, stroke="#9AB0C8", fs=13)
        if i < len(VSM) - 1: s += arrow(x + 82, 58, x + 94, 58)
        s += f'<polyline points="{x - 44},110 {x - 44},130 {x - 8},130 {x - 8},110 {x + 82},110 {x + 82},130" fill="none" stroke="{NAVY}"/>'
        s += txt(x - 26, 148, f"{wait} d", "middle", ORANGE, 12, True) + txt(x + 37, 104, f"{work:g} h", "middle", GREEND, 12, True)
    tw = sum(w for _, w, _ in VSM); th = sum(h for *_, h in VSM)
    s += txt(14, 182, f"Lead time ≈ {tw} days of waiting; work content {th:g} hours. Triangles (I) are inventory waiting between steps.", "start", NAVY, 12.5, True)
    return svg(f"A simple value stream map of five steps: cut, weld, paint, assemble and ship, with inventory waiting before each. Waiting "
               f"before each step is {', '.join(f'{w} days before {n.lower()}' for n, w, _ in VSM)}; work time is "
               f"{', '.join(f'{h:g} hours for {n.lower()}' for n, _, h in VSM)}. Total lead time is about {tw} days of waiting for "
               f"{th:g} hours of work.", 742, 196, s, 600)


def lean():
    from v476_inplace import LEAN_HTML
    wastes = [("Transport", "Moving materials or information more than needed", "Parts carried between buildings; files emailed back and forth"),
              ("Inventory", "More stock or work in progress than needed", "Racks of parts waiting; a backlog of half-finished quotes"),
              ("Motion", "People moving more than the work requires", "Walking to fetch tools; searching shared drives"),
              ("Waiting", "People or work idle", "Waiting for approval, material or a machine"),
              ("Overproduction", "Making more or earlier than needed", "Batches built ahead of orders"),
              ("Over-processing", "More work than the customer needs", "Tighter tolerances than specified; reports nobody reads"),
              ("Defects", "Errors and rework", "Scrap, rework, wrong invoices"),
              ("Unused talent", "Not using people's knowledge and ideas", "Operators never asked how to improve their work")]
    walk = [("Parts waiting at paint for a full batch", "Waiting, inventory", "Paint smaller mixed batches twice a day"),
            ("Welders walk to the crib for consumables", "Motion", "Point-of-use bins at each weld bay"),
            ("Travellers re-written by hand at each step", "Over-processing, defects", "One printed traveller with barcode"),
            ("Finished units wait for a supervisor's sign-off", "Waiting", "Operator self-check with a checklist; spot audits")]
    tw = sum(w for _, w, _ in VSM); th = sum(h for *_, h in VSM)
    body = f"""
<p>Lean is a way of improving work by removing everything that does not add value for the customer, so that work flows with less waiting, effort and cost. It started in car manufacturing and is now used in offices, hospitals, warehouses and service businesses. This guide was first published in November 2025 and has been rewritten with a waste walk example and a value stream map. The earlier version quoted percentages we could not trace to sources; they have been replaced with an illustrative worked example.</p>
<h2>The five Lean principles</h2>
{table(["Principle", "What it means"], [
    ("Value", "Define value from the customer's point of view: what they would pay for"),
    ("Value stream", "Map every step that delivers that value, from order to delivery"),
    ("Flow", "Make the value-adding steps run without interruption"),
    ("Pull", "Make only what the next step or the customer needs, when they need it"),
    ("Perfection", "Keep improving; there is always more waste to remove"),
])}
<h2>The eight wastes</h2>
{table(["Waste", "Meaning", "Examples"], wastes)}
{LEAN_HTML}
<h2>A waste walk</h2>
<p>A waste walk (often called a gemba walk) means going to where the work happens, watching one product or transaction from start to finish, and noting every instance of the eight wastes. It takes an hour or two and needs no software. The findings below come from an illustrative walk in a small fabrication shop.</p>
{table(["What we saw", "Waste", "Countermeasure"], walk)}
<h2>A value stream map</h2>
<p>A value stream map draws the steps, the inventory between them and the time each takes, so the gap between working time and elapsed time becomes obvious. For the same shop:</p>
{fig(fig_vsm(), 1, "Most of the lead time is waiting between steps, not work.")}
<p>A product takes about {tw} working days to get through the shop, but only about {th:g} hours of that is work. Cutting the waiting, by smaller batches, a pull signal from assembly to paint, and removing the sign-off queue, shortens lead time far more than speeding up any single step.</p>
<h2>Lean tools in brief</h2>
<ul>
<li><strong>5S:</strong> organize the workplace so everything has a place; see <a href="../post/lessons-learned-from-deploying-5s-in-the-service-industry.html">5S in service businesses</a>.</li>
<li><strong>Kaizen events:</strong> short, focused improvement workshops; see <a href="../post/perform-kaizen-event.html">how to run a Kaizen event</a>.</li>
<li><strong>Standard work:</strong> the current best way of doing a task, written down and followed.</li>
<li><strong>Pull and kanban:</strong> signals that trigger production or replenishment only when needed.</li>
<li><strong>Quick changeover (SMED):</strong> shorter set-ups make small batches affordable.</li>
<li><strong>Root cause analysis:</strong> 5 whys and fishbone diagrams to fix causes rather than symptoms.</li>
</ul>
<h2>Getting started</h2>
<ol>
<li><strong>Pick one value stream</strong> that matters to customers.</li>
<li><strong>Do a waste walk</strong> with the people who run it.</li>
<li><strong>Map it,</strong> measuring waiting as well as work.</li>
<li><strong>Fix the biggest wait first,</strong> often a batch, an approval or a hand-off.</li>
<li><strong>Measure lead time, quality and on-time delivery</strong> before and after, and set realistic targets from your own baseline.</li>
</ol>
"""
    r = [("perform-kaizen-event", "How to run a Kaizen event"), ("how-to-perform-a-successful-business-process-optimization", "Business process optimization"),
         ("things-you-need-to-know-about-the-theory-of-constraints-toc", "The theory of constraints")]
    body += EXTRA["lean"]
    return art(LEAN, "Lean Methodology: The Eight Wastes, a Waste Walk and a Value Stream Map",
               "Lean explained: five principles, the eight wastes, a value-added test, a worked waste walk and value stream map, the main tools and how to get started.",
               ["process-improvement", "lean", "six-sigma"], ["Lean", "eight wastes", "value stream map", "waste walk", "gemba", "continuous improvement"], body, "Lean", r)


SEO_AI = """<h2>Using AI tools in your SEO work</h2>
<p>AI tools are now useful helpers for SEO, as long as a person stays in charge of what gets published. They are good at grouping keywords by intent, drafting outlines, suggesting questions a page should answer, writing first drafts of titles and descriptions, and summarizing what competing pages cover. They are poor at knowing your business, checking facts and producing anything distinctive on their own. Google's guidance is that it rewards helpful content however it is produced, but content made mainly to manipulate rankings, including mass-produced AI pages, breaks its spam policies. A practical rule: use AI to speed up research and drafting, then add what only you can provide, such as your own data, worked examples, photos and experience, and check every fact before publishing. This section replaces an earlier article on AI-powered SEO strategies.</p>
"""


if __name__ == "__main__":
    op = os.path.join(HERE, "original_dates.json")
    od = json.load(open(op, encoding="utf-8")); od.update(ORIGINAL)
    note = od.pop("_note"); json.dump({"_note": note, **dict(sorted(od.items()))}, open(op, "w", encoding="utf-8"), indent=1)
    for f in (shop, sales, innov, agile, lean):
        a = f()
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"][:50], words(a["body"]), "words", a["read"])
