"""Business case series for Insights, November 2026 (V5.25).

Eight teaching cases in the style of a business school case: each opens on one decision, gives the facts and
exhibits the decision-maker had, sets out the options and the discussion questions, and keeps "what happened"
in a closed section at the end so a reader can decide first.

1  Costco: 4,000 products and a capped markup            (Strategy, Inventory Management)
2  Amazon Prime: betting on free two-day shipping         (Sales & Marketing, Operational Efficiency)
3  Shopify: build, buy or exit logistics                  (Strategy, Digital Technology)
4  Apple: from months of inventory to days                (Inventory Management, Process Improvement)
5  Starbucks 2008: closing every store for an afternoon   (Change Management, Operational Efficiency)
6  Toyota: how lean is too lean?                          (Lean, Inventory Management)
7  Lululemon 2013: the yoga pants recall                  (ISO / quality, Change Management)
8  Netflix 2011: splitting DVD from streaming             (Strategy, Sales & Marketing)

All figures come from the public sources listed at the end of each case. The cases describe what was publicly
reported; they do not invent private conversations or quotes.

The series is unnumbered: cases stand alone and are read in any order. To add a case, write its function, add its
slug to ORDER, TITLES and ARTICLES, then run the steps below for every case (each case's "More cases" list is rebuilt).

Usage:  python3 content/articles/case_studies.py
        python3 content/gen/add_article.py <slug>      (for each article)
        python3 content/gen/series_labels.py ; python3 content/gen/insights_finder.py . ; python3 content/gen/seo_pass.py .
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import svg, fig, txt, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, RED, MUTED, LINE, PALE
from refresh_articles import src, rel

DATE = "2026-11-14"
SERIES = "Business case series"
CSS = '<link rel="stylesheet" href="../assets/css/oee.css">'

S_COSTCO = "costco-case-study-4000-products-and-a-capped-markup"
S_AMAZON = "amazon-prime-case-study-betting-on-free-two-day-shipping"
S_SHOPIFY = "shopify-case-study-build-buy-or-exit-logistics"
S_APPLE = "apple-case-study-from-months-of-inventory-to-days"
S_SBUX = "starbucks-case-study-closing-every-store-for-an-afternoon"
S_TOYOTA = "toyota-case-study-how-lean-is-too-lean"
S_LULU = "lululemon-case-study-the-2013-yoga-pants-recall"
S_NFLX = "netflix-case-study-splitting-dvd-from-streaming"
ORDER = [S_COSTCO, S_AMAZON, S_SHOPIFY, S_APPLE, S_SBUX, S_TOYOTA, S_LULU, S_NFLX]

TITLES = {
    S_COSTCO: "Costco Case Study: 4,000 Products and a Capped Markup",
    S_AMAZON: "Amazon Prime Case Study: Betting on Free Two-Day Shipping",
    S_SHOPIFY: "Shopify Case Study: Build, Buy or Exit Logistics?",
    S_APPLE: "Apple Case Study: From Months of Inventory to Days",
    S_SBUX: "Starbucks Case Study: Closing Every Store for an Afternoon",
    S_TOYOTA: "Toyota Case Study: How Lean Is Too Lean?",
    S_LULU: "Lululemon Case Study: The 2013 Yoga Pants Recall",
    S_NFLX: "Netflix Case Study: Splitting DVD from Streaming",
}


def L(slug, text=None):
    return f'<a href="../post/{slug}.html">{text or TITLES[slug]}</a>'


# ───────────────────────── shared building blocks ─────────────────────────
def intro(company, decision):
    return (f'<p class="oee-note"><em>This case is part of the Chmltech {SERIES}. It is written for discussion, '
            f'in the style of a business school teaching case: it stops at the decision and leaves the outcome to a closed section at the end, '
            f'so you can decide first. {decision} It is drawn from public reporting and company statements listed under Sources; '
            f'it is not based on interviews or private documents.</em></p>')


def table(n, title, head, rows, num=()):
    th = "".join(f'<th{" class=\"num\"" if i in num else ""}>{h}</th>' for i, h in enumerate(head))
    tr = "".join("<tr>" + "".join(f'<td{" class=\"num\"" if i in num else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<p class="oee-cap">Exhibit {n}. {title}</p>\n<table>\n<tr>{th}</tr>\n{tr}\n</table>'


def bars(label, rows, unit="", w=720, maxv=None, lw=230):
    """Horizontal bar chart: rows of (name, value, colour, value label)."""
    maxv = maxv or max(v for _, v, _, _ in rows) * 1.12
    rh, top = 46, 16
    h = top + rh * len(rows) + 10
    s, span = "", w - lw - 90
    for i, (name, v, col, lab) in enumerate(rows):
        y = top + i * rh
        s += txt(lw - 12, y + 22, name, "end", NAVY, 13.5, True)
        bw = max(2, span * v / maxv)
        s += f'<rect x="{lw}" y="{y + 6}" width="{bw:.1f}" height="26" rx="4" fill="{col}"/>'
        s += txt(lw + bw + 8, y + 24, lab, "start", NAVY, 13.5, True)
    s += f'<line x1="{lw}" y1="{top - 4}" x2="{lw}" y2="{h - 6}" stroke="{MUTED}" stroke-width="1"/>'
    return svg(label, w, h, s, 520)


def cols(label, rows, w=720, h=280, maxv=None, ymin=0):
    """Column chart: rows of (category, value, colour, value label)."""
    maxv = maxv or max(v for _, v, _, _ in rows) * 1.15
    left, base, top = 40, h - 50, 20
    n = len(rows); slot = (w - left - 20) / n; bw = min(90, slot * 0.58)
    s = f'<line x1="{left}" y1="{base}" x2="{w - 20}" y2="{base}" stroke="{MUTED}" stroke-width="1"/>'
    for i, (cat, v, col, lab) in enumerate(rows):
        cx = left + slot * (i + 0.5)
        bh = (base - top) * (v - ymin) / (maxv - ymin)
        s += f'<rect x="{cx - bw / 2:.1f}" y="{base - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="4" fill="{col}"/>'
        s += txt(cx, base - bh - 8, lab, "middle", NAVY, 13.5, True)
        for j, ln in enumerate(cat if isinstance(cat, list) else [cat]):
            s += txt(cx, base + 20 + j * 16, ln, "middle", MUTED, 12.5)
    return svg(label, w, h, s, 520)


def exfig(s, cap):
    return f'<figure>\n<div style="overflow-x:auto">{s}</div>\n<figcaption>{cap}</figcaption>\n</figure>'


def options(items):
    return "".join(f"<h3>Option {chr(65 + i)}: {t}</h3>\n<p>{d}</p>\n" for i, (t, d) in enumerate(items))


def questions(qs):
    return "<h2>Discussion questions</h2>\n<ol>" + "".join(f"<li>{q}</li>" for q in qs) + "</ol>"


def reveal(inner):
    return ('<h2>What happened next</h2>\n<p>Decide what you would do before you open this section.</p>\n'
            '<details style="border:1px solid var(--line-2,#D9D5CA);border-radius:10px;padding:14px 18px;margin:1em 0 1.6em">'
            '<summary style="cursor:pointer;font-weight:600;color:var(--ink,#0B2A5A)">Show what the company did and how it turned out</summary>\n'
            '<div style="margin-top:14px">' + inner.replace("<p>", '<p style="margin:0 0 1em">') + '</div></details>')


def lessons(items):
    return "<h2>Lessons for small and mid-sized businesses</h2>\n" + "".join(f"<p><strong>{t}</strong> {d}</p>\n" for t, d in items)


def nav(slug):
    """'More cases': every other case in the series, built from ORDER, so a new case appears in all of them on the next build."""
    return ("<h2>More cases</h2>\n<ul>" + "".join(f"<li>{L(s)}</li>" for s in ORDER if s != slug) + "</ul>\n"
            '<p><a href="../insights.html#cat=case-study">All case studies</a></p>')


# ───────────────────────── 1. Costco ─────────────────────────
def costco():
    ex2 = bars("Sales per hourly employee in 2004: Costco about 500,000 dollars, Sam's Club about 343,000 dollars.",
               [("Costco (68,000 staff)", 500, BLUE, "≈ $500,000"), ("Sam's Club (102,000 staff)", 343, MUTED, "≈ $343,000")])
    ex4 = bars("Costco fiscal 2025: net sales 269.9 billion dollars, membership fees 5.3 billion dollars, net income 8.1 billion dollars.",
               [("Membership fees", 5.32, GREEND, "$5.3B"), ("Net income", 8.1, BLUE, "$8.1B")], maxv=10)
    return f"""{CSS}{intro(S_COSTCO, "The decision belongs to Jim Sinegal, Costco's co-founder and chief executive, in the spring of 2004.")}
<h2>The decision</h2>
<p>In March 2004 Costco reported results that beat Wall Street's expectations, and its share price fell anyway. The complaint was not about sales. It was about how the company chose to spend its margin. Costco paid its warehouse staff well above its main rival, Walmart's Sam's Club, covered most of their health insurance, and refused to mark up any product by more than a fixed percentage. A Deutsche Bank analyst summed up the frustration in BusinessWeek: at Costco, he said, it was better to be an employee or a customer than a shareholder.</p>
<p>Jim Sinegal had set those rules himself when he co-founded the company in 1983. Now investors wanted a choice from him. Costco could raise its margins a little, trim wage and benefit costs toward the industry norm, and give the share price the lift analysts were asking for. Or it could hold the model and keep explaining why it worked.</p>
<h2>Company background</h2>
<p>Costco runs membership warehouses. Shoppers pay an annual fee to get in, and in return the company promises prices that no conventional retailer can match. Three operating rules make that promise possible:</p>
<ul>
<li><strong>A capped markup.</strong> No branded item may be marked up more than 14% over cost, and no item under its own label (later Kirkland Signature) more than 15%. Supermarkets and department stores commonly mark up by 25% to 50%.</li>
<li><strong>A narrow range.</strong> A warehouse carries about 4,000 products. A typical supermarket carries 30,000 or more, and a Walmart Supercenter well over 100,000. Costco offers one or two choices in each category, bought in very large volumes.</li>
<li><strong>A low-cost box.</strong> Goods arrive on pallets and are sold from them, with no shelf stocking, little décor and limited advertising.</li>
</ul>
<p>The narrow range is what turns the capped markup into a profit. Each product sells in huge volume, so Costco has buying power with suppliers far beyond its size, and inventory turns over so fast that the company often sells goods before it has to pay for them. The membership fee then supplies most of the profit: the merchandise is priced to cover costs plus a thin margin, and the fees, which cost almost nothing to collect, flow through to earnings. The company also became known for small symbols of the same idea, such as the hot dog and soda combo it has sold for $1.50 since 1985.</p>
<h2>The situation in 2004</h2>
<p>Costco's critics had a point that could be measured. Its pay was well above Sam's Club's. Its supporters had a point that could be measured too: Costco got much more out of each employee.</p>
{table(1, "Costco and Sam's Club, 2004 (as reported in BusinessWeek and The New York Times)",
       ["Measure", "Costco", "Sam's Club"],
       [["U.S. hourly employees", "about 68,000", "about 102,000"], ["U.S. sales", "about $34 billion", "about $35 billion"],
        ["Starting hourly pay", "$11.00", "$10.00"], ["Hourly pay after about 4½ years", "$19.50", "$12.50"],
        ["Markup limit", "14% branded, 15% own label", "No published limit"]])}
{exfig(ex2, "Exhibit 2. Sales per hourly employee in 2004, from the figures in Exhibit 1. Costco produced about 45% more sales per person with fewer people.")}
<p>Costco's management argued that the wages paid for themselves through lower staff turnover, less theft and more productive warehouses. Its chief financial officer told BusinessWeek that paying higher wages translated into more efficiency. The analysts' reply was that the same efficiency at normal wages would be worth even more to shareholders. Both sides agreed on one thing: Costco's expenses as a share of sales were the lowest in the industry. Walmart's selling, general and administrative costs were about 17% of sales and Target's about 24%, while Costco's were about 9.8%.</p>
<p>There was a second pressure. Sam's Club, with Walmart's purchasing power behind it, had improved its stores and its merchandise, and it was competing hard on price. Raising markups would make Costco's prices easier to beat. Not raising them meant that any growth in profit had to come from more members, more sales per member, or a higher fee.</p>
<h2>The options</h2>
{options([
    ("Raise margins a little", "Lift the markup cap by one or two points on selected categories. On net sales of about $47 billion, each point of margin is worth more than $400 million a year, roughly half of Costco's net income at the time. The risk is that members notice, and that the price gap to Sam's Club narrows."),
    ("Bring wages and benefits toward the industry norm", "Slow pay increases and ask staff to pay more of their health costs. This answers the analysts directly, but it puts at risk the low turnover and high productivity that Exhibit 2 shows."),
    ("Hold the model and grow the fee base", "Keep the markup cap and pay policy, open more warehouses, and raise the membership fee every few years instead. Profit growth is slower in the short run, and the company has to keep defending its approach to investors."),
    ("Widen the range", "Add more products and categories to raise sales per visit. This would dilute the buying power of the narrow range and add inventory, store space and complexity."),
])}
{questions([
    "What is Costco actually selling: products, or the membership? How does your answer change which option looks right?",
    "Use Exhibit 1. If Costco cut its hourly pay to Sam's Club's level, what would it save, and what would it risk losing?",
    "Why does a narrow product range make a capped markup affordable? Trace the link through buying power, inventory turns and labour.",
    "Who should the company serve first: members, employees or shareholders? Is that a real trade-off over ten years, or only over one?",
    "If you were Sinegal, how would you answer the analyst's remark at the next earnings call?",
])}
{reveal(f'''<p>Sinegal held the model. He kept the markup cap and the pay policy, told reporters that raising prices to please Wall Street would be the company's downfall, and described the wage policy as good business rather than generosity. Profit growth came from new warehouses, more members and periodic fee increases instead. The Gold Star membership fee was raised in 2006, 2011 and 2017, and again in September 2024, from $60 to $65 (Executive from $120 to $130), the first increase in seven years. Renewal rates barely moved.</p>
<p>Two decades later the numbers make the case. In fiscal 2025 Costco had net sales of $269.9 billion, total revenue of $275.2 billion and net income of $8.1 billion, from 914 warehouses. Membership fees were $5.3 billion, less than 2% of revenue but about two-thirds of net income. The renewal rate was 92.3% in the United States and Canada and 89.8% worldwide, with 145 million cardholders. Kirkland Signature, the own label held to the 15% cap, had grown into one of the largest consumer brands in North America.</p>
{exfig(ex4, "Exhibit 3. Costco in fiscal 2025. Membership fees equal about two-thirds of net income, which is why the company can sell merchandise close to cost.")}
<p>The share price that analysts worried about in 2004 rose many times over in the years that followed. The model the analysts wanted changed is now the one competitors are told to copy.</p>''')}
{lessons([
    ("A narrow range can be a strategy, not a limitation.", f"Fewer products means larger orders, better prices from suppliers, faster turns and simpler operations. An {L('abc-inventory-analysis', 'ABC analysis')} of your own range often shows that a small share of products earns most of the margin."),
    ("Decide what you sell, then price for it.", "Costco sells access and trust; the goods are priced to protect them. A service firm that sells a retainer, or a manufacturer that sells a maintenance contract, can apply the same logic."),
    ("Measure the return on people, not only their cost.", "Sales per employee, turnover and error rates tell you whether higher pay is buying productivity. Track them before you cut."),
    ("Publish your rules.", "A visible rule, such as a markup cap or a delivery promise, is easy for customers to trust and hard for managers to erode one exception at a time."),
])}
{src([("Costco, fourth quarter and fiscal 2004 results (net sales $47.1 billion, net income $882 million)", "https://s201.q4cdn.com/287523651/files/doc_news/2004/10/costco-wholesale-corporation-releases-fourth-quarter-and-3.pdf"),
      ("Costco 2006 annual report (SG&amp;A 9.83% of net sales in fiscal 2004)", "https://s201.q4cdn.com/287523651/files/doc_financials/2006/ar/Annual_report_2006.pdf"),
      ("BusinessWeek, \"The Costco Way: Higher wages mean higher profits. But try telling Wall Street\" (April 2004, reproduced by LaborNet)", "https://labornet.igc.org/news/0404/costco.htm"),
      ("Snopes, fact check of the 2005 New York Times profile of Jim Sinegal (pay comparison with Sam's Club)", "https://www.snopes.com/fact-check/costco-ceo/"),
      ("Retail Insider, Costco fourth quarter and fiscal 2025 results", "https://retail-insider.com/retail-insider/2025/09/costco-wholesale-corp-4th-q-fiscal-2025-earnings-review-commentary-bruce-winder/"),
      ("Costco fourth quarter fiscal 2025 earnings call (renewal rates)", "https://allmind.ai/earnings/event/bt_COST_2025_Q4"),
      ("Think Insights, How Costco Makes Money (fiscal 2025 figures, warehouse count)", "https://thinkinsights.net/strategy/how-costco-makes-money")])}
{nav(S_COSTCO)}"""


# ───────────────────────── 2. Amazon Prime ─────────────────────────
def amazon():
    ex2 = bars("Break-even for a Prime member in 2005: the 79 dollar fee equals about eight two-day shipments at 9.48 dollars each.",
               [("One two-day shipment", 9.48, MUTED, "$9.48"), ("Prime fee, one year", 79, BLUE, "$79 = about 8 shipments")], maxv=100)
    return f"""{CSS}{intro(S_AMAZON, "The decision belongs to Jeff Bezos, Amazon's founder and chief executive, in January 2005.")}
<h2>The decision</h2>
<p>A few weeks before Amazon was due to report its results in February 2005, Jeff Bezos asked a small group of employees to meet him on a Saturday at the boathouse behind his home. He wanted a shipping membership: customers would pay one annual fee and get fast shipping on everything, with no minimum order. He wanted it announced with the earnings.</p>
<p>The finance team had modelled it, and the results were, in Bezos's later word, horrifying. The customers most likely to join were the ones who already bought the most, so Amazon would give away shipping it was being paid for today. Two-day shipping was expensive to provide. Nobody could show from data that members would buy enough extra to cover the cost. Bezos had to decide whether to launch anyway, and at what price.</p>
<h2>Company background</h2>
<p>Amazon had started as an online bookstore in 1995 and by 2004 sold electronics, toys, kitchenware and much more, with net sales of about $6.9 billion. Its central idea was that lower prices and better service would bring more customers, more customers would attract more sellers and selection, and the growing volume would lower costs, allowing lower prices again.</p>
<p>Shipping was the weak point in that loop. Shoppers disliked paying for it, and many abandoned their carts when they saw the charge. In 2002 Amazon had introduced Free Super Saver Shipping, free standard delivery on orders above a minimum, and lowered the threshold over time. It worked, but it trained customers to batch their orders and wait, which is the opposite of the habit Amazon wanted them to form. Fast delivery was available but rare: two-day shipping cost about $9.48 for a typical order, and few customers paid for it.</p>
<h2>The situation in early 2005</h2>
<p>An engineer, Charlie Ward, had suggested a premium shipping club, borrowing from airline loyalty programs. Bezos took the idea and set a deadline that the team considered impossible. The project, code-named Futurama, pulled people from other teams to build the sign-up flow, the eligibility rules and the changes to the fulfilment centres needed to promise two-day delivery reliably.</p>
{table(1, "The proposal on the table",
       ["Element", "Proposed design"],
       [["Annual fee", "$79"], ["Benefit", "Unlimited free two-day shipping on eligible items, no minimum order"],
        ["Extra", "Overnight shipping for $3.99 per item"], ["Eligible items", "More than a million items sold and shipped by Amazon"],
        ["Household sharing", "Up to four household members on one membership"],
        ["Comparable cost to the customer", "About $9.48 for each two-day shipment"]])}
{exfig(ex2, "Exhibit 2. The customer's arithmetic. A member who placed about nine two-day orders a year came out ahead; heavy buyers came out far ahead, which is exactly what worried finance.")}
<p>The economics depended on three things nobody could prove in advance. First, members had to change behaviour and buy more often, from more categories, once shipping cost nothing at the margin. Second, the operations team had to bring down the cost of two-day fulfilment as volume grew. Third, the fee had to be high enough to matter and low enough that customers would try it. According to Brad Stone's account, Bezos settled on $79 because it was large enough to feel like a commitment but small enough that customers would take the risk.</p>
<h2>The options</h2>
{options([
    ("Launch Prime at $79 for everyone", "Announce it with the earnings and accept losses on heavy buyers, betting that changed behaviour and lower fulfilment costs will pay for it over years."),
    ("Run a quiet pilot first", "Offer it to a sample of customers, measure the change in spending for six to twelve months, then decide. Lower risk, but slower, and a pilot this visible would be hard to keep quiet from competitors."),
    ("Price it higher", "Charge $99 or more to protect the margin. Fewer customers would join, and the habit Amazon wanted to build would spread more slowly."),
    ("Improve Super Saver Shipping instead", "Lower the minimum order or speed up free standard shipping. Cheaper and safer, but it does not create a reason for customers to come back to Amazon first."),
])}
{questions([
    "Finance said heavy buyers would join first and cost the most. Is that a reason to stop, or the point of the program?",
    "Use Exhibit 2. What would you need to believe about member spending for Prime to pay back within three years?",
    "Which part of the bet was a marketing question and which part was an operations question? Which was harder to win?",
    "Why might a fee customers pay up front change their behaviour more than free shipping with a minimum order?",
    "If you ran Prime as a pilot, what would you measure, and how long would you wait?",
])}
{reveal(f'''<p>Bezos launched. Amazon Prime went live on February 2, 2005, announced as "all-you-can-eat" express shipping for $79 a year, with unlimited two-day delivery on more than a million items. Tens of thousands of customers signed up in the first month. Press coverage was muted and focused on the cost to Amazon.</p>
<p>The early members were mostly existing heavy buyers, just as finance had predicted, and the program lost money at first. By 2007 internal data showed that customers who joined Prime roughly doubled their spending on the site. Amazon then used Prime to pull in sellers: in September 2006 it launched Fulfillment by Amazon, which let other merchants store goods in Amazon's warehouses and make them eligible for Prime shipping. That made Prime's selection grow faster than Amazon could buy inventory itself.</p>
{table(3, "Prime after the launch", ["Year", "Change"],
       [["2005", "Launched at $79 a year"], ["2006", "Fulfillment by Amazon opens Prime shipping to other sellers"], ["2011", "Prime Video added"],
        ["2014", "Fee raised to $99"], ["2015", "First Prime Day"], ["2018", "Fee raised to $119"], ["2021", "More than 200 million members worldwide"],
        ["2022", "Fee raised to $139, citing higher labour and shipping costs"]])}
<p>Prime became the centre of Amazon's retail business: the main reason customers start their shopping there, and the reason sellers accept its fees. The operational bet mattered as much as the marketing one. Each new fulfilment centre and each step toward faster delivery lowered the cost of the promise and raised its value.</p>''')}
{lessons([
    ("Some decisions cannot be proven with data in advance.", "When a choice depends on how customers will change, a model can only show the downside. Decide how much you can afford to lose while you find out, and set a date to review it."),
    ("A promise is only as good as the operation behind it.", f"Prime worked because fulfilment could deliver it. Before you promise faster delivery or shorter lead times, check your {L('quote-to-cash-process-in-manufacturing', 'quote-to-cash process')} and capacity can hold it."),
    ("Subscriptions change behaviour.", "A small business can apply the same idea with a service plan, a maintenance contract or a priority-delivery membership: an up-front fee that removes a per-order cost the customer dislikes."),
    ("Price to be tried.", "Bezos priced Prime to feel like a commitment, not a burden. A first price can be raised later, as Prime's was four times; a price that stops people trying cannot be fixed."),
])}
{src([("Amazon.com press release, results for 2004 and the introduction of Amazon Prime (February 2, 2005)", "https://press.aboutamazon.com/2005/2/amazon-com-announces-record-free-cash-flow-fueled-by-lower-prices-and-free-shipping-introduces-new-express-shipping-program-amazon-prime"),
      ("Retail Brew, \"How Amazon Prime backed the retail industry into a corner\" (2025)", "https://www.retailbrew.com/stories/2025/03/13/how-amazon-prime-backed-the-retail-industry-into-a-corner"),
      ("Benzinga, Jeff Bezos on Prime's risky beginnings (\"the results were horrifying\")", "https://benzinga.com/25/03/44132215/jeff-bezos-once-spoke-about-amazon-primes-risky-beginnings-and-why-free-shipping-seemed-like-a-terrible-idea-at-first"),
      ("WRAL / CNN, the boathouse meeting and the $79 price, after Brad Stone's The Everything Store", "https://www.wral.com/archive/17515891/"),
      ("Phys.org (AP), \"10 years later, Amazon celebrates Prime's growth\" (2015)", "https://phys.org/news/2015-02-years-amazon-celebrates-prime-growth.amp"),
      ("Commoncog, Amazon Prime case (launch press release, 2007 spending data)", "https://commoncog.com/case/amazon-prime/"),
      ("Bloomberg oral history via The Lowdown Blog (two-day shipping cost, Charlie Ward, Futurama)", "https://www.thelowdownblog.com/2019/05/how-amazon-prime-became-dominant-force.html"),
      ("Wikipedia, Amazon Prime (membership counts and fee history)", "https://en.wikipedia.org/wiki/Amazon_Prime")])}
{nav(S_AMAZON)}"""


# ───────────────────────── 3. Shopify ─────────────────────────
def shopify():
    ex2 = bars("What Shopify spent on logistics: 6 River Systems 450 million dollars, Deliverr 2.1 billion dollars, plus a 1 billion dollar build-out budget.",
               [("6 River Systems (2019)", 0.45, PURPLE, "$0.45B"), ("Fulfillment network budget (2019)", 1.0, BLUE, "$1.0B over five years"),
                ("Deliverr (2022)", 2.1, ORANGE, "$2.1B")], maxv=2.8, lw=260)
    return f"""{CSS}{intro(S_SHOPIFY, "The decision belongs to Tobi Lütke, Shopify's co-founder and chief executive, in early 2023.")}
<h2>The decision</h2>
<p>By early 2023 Shopify had spent four years and billions of dollars trying to give its merchants what Amazon gave its sellers: fast, reliable delivery from a shared network of warehouses. It had bought a warehouse robotics company and a fast-growing logistics start-up, and it was running its own fulfilment centres. The network was starting to work. It was also consuming cash and management attention at a time when growth across e-commerce had slowed and investors had turned against loss-making expansion.</p>
<p>Tobi Lütke had to decide whether logistics was part of Shopify's core business or a distraction from it. Keep investing, and Shopify might one day offer merchants a real alternative to Fulfillment by Amazon. Pull back, and it could return to the software platform that had made it one of Canada's most valuable companies.</p>
<h2>Company background</h2>
<p>Lütke founded Shopify in Ottawa in 2006 after building an online store for his own snowboard shop and finding the available software poor. Shopify sells merchants the tools to run an online store, and later point-of-sale, payments, shipping labels and marketing. It makes money from subscriptions and from a share of payments and other services. By 2019 it powered more than 800,000 businesses in about 175 countries.</p>
<p>Shopify positioned itself as the arms dealer to the rebels: the platform that let independent brands sell directly to customers instead of depending on Amazon's marketplace. That made Amazon's delivery promise a direct competitive threat. Shoppers had come to expect two-day delivery, and merchants on Shopify had to arrange it themselves through third-party logistics providers of varying quality.</p>
<h2>The situation in early 2023</h2>
{table(1, "Shopify's logistics build-out", ["Date", "Step"],
       [["June 2019", "Shopify Fulfillment Network announced, with about $1 billion budgeted over five years for U.S. fulfilment centres"],
        ["September 2019", "Agrees to buy 6 River Systems, maker of the \"Chuck\" warehouse robot, for about $450 million (60% cash, 40% shares)"],
        ["2020–2021", "Pandemic lifts e-commerce sharply; Shopify's revenue and share price soar"],
        ["February 2022", "Shifts the network to fewer, larger warehouses that Shopify will run itself"],
        ["May 2022", "Agrees to buy Deliverr, a fulfilment start-up, for about $2.1 billion, its largest acquisition"],
        ["July 2022", "Lays off about 10% of staff; Lütke says he bet wrong that the pandemic's shift to online shopping would last"],
        ["Early 2023", "E-commerce growth normalises; investors reward profit over expansion"]])}
{exfig(ex2, "Exhibit 2. The scale of the bet. The two acquisitions alone came to more than $2.5 billion, before the cost of running the warehouses.")}
<p>The strategic case for logistics was real. Delivery speed affects conversion, and merchants wanted one partner for software and fulfilment. Amazon had shown that owning the warehouses could become a lasting advantage. The case against was also real. Warehouses are a business of capital, labour and thin margins, very different from software. Building a network dense enough to promise fast delivery across North America would take many more years and billions more dollars, and Amazon, the competitor to beat, was spending tens of billions a year on the same thing.</p>
{table(3, "Software and logistics compared", ["Feature", "Shopify's software business", "A fulfilment network"],
       [["Capital needed", "Low; mostly people", "High; buildings, equipment, inventory systems"],
        ["Cost of serving one more merchant", "Close to zero", "Rises with every order shipped"],
        ["Typical margin", "High", "Thin"], ["Main management skill", "Product and engineering", "Operations, labour, real estate"],
        ["Scale needed to compete", "Already achieved", "Years away"]])}
<h2>The options</h2>
{options([
    ("Keep building", "Stay the course with the owned network, integrate Deliverr fully and accept several more years of losses in logistics to match Amazon's delivery promise."),
    ("Narrow the network", "Keep the software that routes orders and promises delivery dates, but run only a few warehouses in the largest markets and lean on partners elsewhere."),
    ("Sell the operation to a logistics specialist and partner with it", "Hand the warehouses and staff to a company whose core business is logistics, keep a stake and a preferred-partner agreement, and return to software."),
    ("Close it down", "Shut the warehouses and leave merchants to choose their own providers, writing off the investment."),
])}
{questions([
    "What is Shopify's core business? Does owning warehouses strengthen it or compete with it for money and attention?",
    "Use Exhibit 3. Why might a company that is excellent at software struggle in logistics, even with the same people at the top?",
    "How should Lütke weigh the money already spent? What should the $2.1 billion paid for Deliverr count for in this decision?",
    "If Shopify exits, how does it still answer merchants who need fast delivery to compete with Amazon?",
    "What would have had to be true in 2023 for Option A to be the right choice?",
])}
{reveal(f'''<p>Lütke chose to sell. On May 4, 2023, Shopify announced that it would sell its logistics business, including Deliverr, to Flexport, a freight forwarding company, in an all-stock deal that gave Shopify about a 13% stake in Flexport (and a stake in the high teens in total) plus a board seat. Flexport became Shopify's preferred logistics partner. 6 River Systems was sold separately to Ocado Group. Shopify cut about 20% of its workforce, more than 2,000 people, its second large round of layoffs in a year, and recorded an impairment charge of about $1.5 billion on the logistics business.</p>
<p>In his letter to staff, Lütke called logistics a "side quest" and said Shopify's main mission was to make commerce simpler and more widely accessible. The same day, Shopify reported first-quarter revenue of $1.51 billion, up 25%, ahead of forecasts. Its shares rose about 23% that day.</p>
<p>Over the following years Shopify concentrated on software, payments and its merchant tools, and returned to steady profitability. The decision is now widely cited as an example of a company admitting that an expensive strategy no longer fit, and exiting before it consumed more.</p>''')}
{lessons([
    ("Be clear about what your core business is.", f"Every company is tempted to own more of the chain. Ask whether the new activity uses the same skills and economics as the business you are good at. For many SMEs, logistics, IT hosting or in-house manufacturing are better bought from a specialist, as the growth of third-party logistics providers shows."),
    ("Money already spent should not decide the next step.", "The $2.1 billion was gone whichever option Shopify chose. The only question was whether the next dollar would earn more in logistics or in software."),
    ("A partnership can deliver the customer benefit without the ownership.", "Shopify kept a stake and a preferred partner, so merchants still had an answer on delivery."),
    ("Set exit criteria when you start.", "Decide in advance what results, by what date, would make you stop. It makes a hard decision easier to take on time."),
])}
{src([("Shopify press release, \"Shopify to Acquire 6 River Systems\" (September 9, 2019)", "https://www.shopify.com/news/shopify-to-acquire-6-river-systems"),
      ("Digital Commerce 360, Shopify's $1 billion fulfilment network plan and the 6 River deal (2019)", "https://www.digitalcommerce360.com/?p=919293"),
      ("The Logic, \"Shopify unloads logistics business as it cuts 20% of workforce\" (May 4, 2023)", "https://thelogic.co/news/why-axis/shopify-unloads-logistics-business-to-flexport-in-major-strategic-shift-as-it-cuts-20-of-workforce/"),
      ("FreightWaves, \"Shopify sells fulfillment business to Flexport, slashes 20% of staff\" (2023)", "https://www.freightwaves.com/news/flexport-acquires-shopifys-fulfillment-business"),
      ("CBC News, \"Shopify to lay off 20% of staff\" (impairment charge)", "https://www.cbc.ca/1.6831842"),
      ("Yahoo Finance Canada, what to know about Shopify's layoffs (\"side quest\" letter, share price)", "https://ca.finance.yahoo.com/news/leave-shopify-today-know-tech-193053351.html"),
      ("Business Insider, Shopify sale of 6 River Systems to Ocado", "https://www.businessinsider.in/stock-market/news/shopify-soars-28-on-strong-earnings-and-sale-of-logistics-unit-plans-to-slash-headcount/articleshow/99995880.cms")])}
{nav(S_SHOPIFY)}"""


# ───────────────────────── 4. Apple ─────────────────────────
def apple():
    ex3 = cols("Apple's inventory on hand: about two months in 1997, one month in early 1998, six days by September 1998 and two days by September 1999.",
               [(["1997"], 60, MUTED, "≈ 60 days"), (["Early 1998"], 30, ORANGE, "≈ 30 days"), (["Sept 1998"], 6, BLUE, "6 days"), (["Sept 1999"], 2, GREEND, "2 days")])
    return f"""{CSS}{intro(S_APPLE, "The decision belongs to Tim Cook, who joined Apple as senior vice president of worldwide operations in March 1998, and to Steve Jobs, who hired him.")}
<h2>The decision</h2>
<p>When Tim Cook arrived at Apple in March 1998, the company had just lost about $1 billion in a single year. Its products were confusing, its factories and warehouses were full, and computers were losing value on the shelves every week. Steve Jobs, back as interim chief executive since 1997, had already cut the product line to a handful of models. He had hired Cook, a supply chain manager from Compaq, to fix the operation behind them.</p>
<p>Cook's question was how far to go. Apple could tidy up its existing operations: fewer suppliers, tighter forecasting, a few warehouse closures. Or it could stop making computers itself, hand production to contract manufacturers, and run with almost no inventory at all, just as the company was about to launch the product meant to save it, the iMac.</p>
<h2>Company background</h2>
<p>Apple had grown in the 1980s on the Macintosh. In the 1990s it lost its way: a stream of overlapping models, a failed attempt to license the Mac operating system to clone makers, and a run of short-lived chief executives. In fiscal 1997 Apple lost $1.045 billion on sales of about $7 billion. It ran its own factories in California, Ireland and Singapore and kept stock in warehouses around the world. In 1995 it had been carrying about $1.8 billion in inventory.</p>
<p>When Jobs returned, he drew a two-by-two grid on a whiteboard: consumer and professional, desktop and portable. Apple would make one great product for each box and cancel the rest. Roughly 70% of the product line was cut. A short, simple range was the precondition for everything Cook did next.</p>
<h2>The situation in 1998</h2>
<p>In the personal computer business, inventory is a perishable good. Components drop in price every few months and new models make old ones hard to sell. Cook later said that computer inventory loses value at 1% to 2% a week, and that it should be managed like dairy products: once past its freshness date, it is a problem. Dell, the industry leader in operations, built computers to order and held only days of stock. Apple held about two months.</p>
{table(1, "Apple's operations before and after the first year of changes",
       ["Measure", "Before (1997)", "After (1998–1999)"],
       [["Key suppliers", "about 100", "24"], ["Warehouses", "19", "about half closed"],
        ["Inventory on hand", "about two months", "6 days (Sept 1998), 2 days (Sept 1999)"],
        ["Time to build a computer", "about four months", "about two months"], ["Manufacturing", "Own factories", "Moving to contract manufacturers in Asia"],
        ["Product line", "Dozens of overlapping models", "Four product categories"]])}
<p>The cuts Cook had in mind carried real risks. With 24 key suppliers instead of 100, a single supplier's failure could stop production. Contract manufacturers would build Apple's products alongside other companies' and would need to be managed closely to protect quality and secrets. And a company with six days of stock has no cushion if demand is higher than expected, at the moment of its most important product launch in a decade.</p>
{exfig(ex3, "Exhibit 2. Days of inventory on hand, as reported by Walter Isaacson and others. Each step down released cash and reduced the risk of writing off obsolete stock.")}
<h2>The options</h2>
{options([
    ("Tidy up the existing operation", "Rationalise suppliers and forecasting, close some warehouses, keep the factories. Lower risk, but Apple would still carry weeks of stock in a business where stock loses value weekly."),
    ("Go lean in-house", "Keep the factories but run them on a build-to-order model like Dell's, with suppliers holding components nearby. A large change in Apple's own plants, with capital still tied up in manufacturing."),
    ("Outsource manufacturing and run on days of inventory", "Close factories and warehouses, concentrate spending with a small number of suppliers on tough terms, and move assembly to contract manufacturers. The largest gain in cash and cost, and the largest change in how Apple controls its products."),
])}
{questions([
    "Why does inventory cost a computer company more than it costs a hardware store or a food wholesaler? What does that imply for how much to hold?",
    "Use Exhibit 1. What made it possible to cut inventory from about two months to six days in six months? Which change mattered most?",
    "What does Apple give up when it stops building its own products? How would you protect quality and confidentiality with a contract manufacturer?",
    "With only 24 key suppliers, how would you manage the risk that one of them fails?",
    "Could Cook's changes have worked without Jobs's decision to cut the product line? Why or why not?",
])}
{reveal(f'''<p>Cook took the most aggressive option. Within months he reduced Apple's key suppliers from about 100 to 24, used the concentrated spending to negotiate better prices and terms, and persuaded many suppliers to locate near Apple's plants. He closed about half of the company's 19 warehouses. By September 1998 inventory was down from about a month to six days, and by September 1999 to about two days. The time to build a computer fell from four months to two. Over the following years Apple moved its assembly to contract manufacturers in Asia. Cook described inventory as "fundamentally evil."</p>
<p>The iMac launched in August 1998 and sold about 278,000 units in its first six weeks. Apple swung from the $1.045 billion loss of fiscal 1997 to a profit of $309 million in fiscal 1998.</p>
<p>The operating model Cook built became the base for everything that followed, including the iPod, the iPhone and the iPad. Apple used its purchasing scale to secure components years ahead, prepaying suppliers and even buying production equipment for them. More than a decade later it still carried less than a week of inventory while its revenue grew more than twenty-fold. Cook became chief operating officer in 2005 and chief executive in 2011.</p>''')}
{lessons([
    ("Simplify the product range before you optimise the supply chain.", "Apple could run on days of stock only because it sold a few products. Fewer variants make forecasting easier and every other improvement larger."),
    ("Know what your inventory costs you.", f"If your stock loses value, ties up cash or risks becoming obsolete, put a number on it. The {L('reorder-point-and-eoq-when-to-order-and-how-much', 'reorder point and EOQ')} and {L('setting-safety-stock', 'safety stock')} posts show how to set levels from demand and lead time rather than habit."),
    ("Concentrate spending to gain leverage, and manage the risk that comes with it.", "Fewer suppliers bring better terms and closer cooperation, but each one matters more. Keep a backup source for critical parts."),
    ("Outsource what others do better, but keep control of what makes you different.", "Apple handed over assembly and kept design, software and the relationship with suppliers."),
])}
{src([("The Motley Fool, \"Apple Inc.'s Operational Excellence Continues\" (2014), citing Walter Isaacson", "https://www.fool.com/investing/general/2014/07/09/apple-incs-operational-excellence-continues.aspx"),
      ("Kaizen Institute, \"The Apple story\" (inventory two months to one, six days, two days)", "https://afr.kaizen.com/blog/post/2013/03/19/the-apple-story.html"),
      ("CPO Rising, \"The strategies that propelled Tim Cook from CPO to CEO\" (2012/2019)", "https://cporising.com/2019/07/18/throwback-thursday-the-strategies-that-propelled-tim-cook-from-cpo-to-ceo-1/"),
      ("ICMR, \"Apple Inc: Setting New Inventory Management Standards\" (case excerpt: 1995 inventory, iMac sales, 1998 profit)", "https://icmrindia.org/Casestudies/catalogue/Finance/Apple%20Inventory%20Management%20Standards-Excerpts1.htm"),
      ("QuickBooks, \"Apple supply chain\" (inventory losing value 1% to 2% a week)", "https://quickbooks.intuit.com/au/blog/running-a-business/apple-supply-chain/")])}
{nav(S_APPLE)}"""


# ───────────────────────── 5. Starbucks ─────────────────────────
def starbucks():
    return f"""{CSS}{intro(S_SBUX, "The decision belongs to Howard Schultz, who returned as Starbucks' chief executive in January 2008.")}
<h2>The decision</h2>
<p>In January 2008 the Starbucks board asked Howard Schultz, the man who had built the company, to return as chief executive. The share price had fallen about 42% in 2007. For the first time, the average number of transactions in U.S. stores was falling. Competitors from McDonald's to independent cafés were selling espresso drinks, and customers were telling Starbucks that the experience no longer felt special.</p>
<p>Schultz believed the problem started behind the counter. In the rush to open stores, Starbucks had automated its espresso machines, sped up its service and added products, and in his view baristas no longer knew how to make a great drink. He wanted to retrain all of them, at once, in a way the whole company and its customers would notice. The most direct way to do that was to close every company-owned store in the United States for an afternoon. It would cost millions of dollars in lost sales, hand customers to competitors for a day and invite ridicule.</p>
<h2>Company background</h2>
<p>Starbucks began in Seattle in 1971 as a seller of coffee beans. Schultz joined in 1982, was inspired by the espresso bars of Milan, and bought the company in 1987. His idea was a "third place" between home and work, built on high-quality coffee, well-trained staff (called partners) and a consistent experience. Starbucks offered health insurance and stock options to part-time staff, unusual in retail.</p>
<p>The company grew at a pace few retailers have matched. By 2007 it had more than 15,000 stores worldwide and was opening several new stores a day. Schultz stepped down as chief executive in 2000 and stayed on as chairman.</p>
<h2>The situation in early 2008</h2>
<p>In February 2007 Schultz had sent an internal memo to senior leaders, later leaked, warning that a series of decisions, each sensible on its own, had led to the "commoditization" of the Starbucks experience. Automatic espresso machines blocked the customer's view of the barista. Pre-ground, flavour-locked packaging had removed the aroma of freshly ground coffee. Stores were being designed for efficiency rather than warmth. Hot breakfast sandwiches, which sold well, filled the stores with the smell of burnt cheese instead of coffee.</p>
{table(1, "Starbucks in early 2008", ["Indicator", "Position"],
       [["Share price, 2007", "Down about 42%"], ["U.S. transactions per store", "Falling for the first time (down about 1%)"],
        ["Company-owned U.S. stores", "about 7,100"], ["Licensed U.S. stores (in airports, supermarkets and so on)", "about 4,000"],
        ["U.S. baristas", "about 135,000"], ["Competition", "McDonald's adding espresso drinks; Dunkin' expanding; independents growing"],
        ["Economy", "U.S. housing market falling; recession beginning"]])}
<p>Schultz had already moved quickly after his return: he replaced senior managers, announced job cuts at headquarters, introduced free wireless internet and said hot breakfast sandwiches would go. The question was whether the training needed a gesture this large. The alternatives were cheaper and less visible.</p>
{table(2, "Ways to retrain 135,000 baristas", ["Approach", "Cost", "Speed", "Signal to staff and customers"],
       [["Store by store, in quiet hours", "Low", "Months", "Little"], ["Regional training days", "Medium", "Weeks", "Moderate"],
        ["Close all company-owned stores at once for an evening", "High (lost sales, wages, competitors' promotions)", "One evening", "Very strong, in both directions"]])}
<h2>The options</h2>
{options([
    ("Retrain quietly, store by store", "Use slow hours and store managers to retrain staff over several months. No lost sales and no headlines, but no clear moment of change either."),
    ("Close every company-owned U.S. store for one evening", "Retrain all baristas on the same evening, with a video message from Schultz, and tell the public why. Expensive, risky and impossible to ignore."),
    ("Focus on products and marketing instead", "Leave training to the normal programs and put the effort into new drinks, prices and advertising to bring traffic back. Faster to show results, but it does not address what Schultz saw as the cause."),
])}
{questions([
    "Schultz saw the decline as a quality problem behind the counter; others saw it as a recession and competition problem. How would you test which was right?",
    "Use Exhibit 2. What is the value of the signal sent by closing every store? How would you put a number on it?",
    "What could go wrong with a nationwide closure? How would you plan for it?",
    "Each of the changes in the 2007 memo made sense on its own. How does a growing company stop a series of sensible decisions from eroding what made it good?",
    "What would you do after the training evening to make sure the improvement lasted?",
])}
{reveal(f'''<p>Schultz closed the stores. On Tuesday, February 26, 2008, Starbucks shut about 7,100 company-owned U.S. stores from 5:30 to 9:00 p.m. local time for what it called Espresso Excellence Training, retraining about 135,000 baristas in pulling espresso shots, steaming milk and serving customers. The 4,000 licensed stores stayed open. Dunkin' Donuts offered 99-cent espresso drinks that evening, and independent cafés gave away coffee. In a video that opened the session, Schultz told staff that the company had lost its way over the years.</p>
<p>Schultz later said the closure cost millions of dollars and was meant to show how serious he was about returning to the core. It was the first of many steps. In July 2008 Starbucks announced it would close about 600 underperforming U.S. stores. In October 2008, as the financial crisis deepened, he took about 10,000 store managers to a leadership conference in New Orleans costing about $30 million, over the board's reluctance. The company restructured its supply chain, brought back the smell of fresh coffee and later returned breakfast sandwiches with a new recipe.</p>
<p>The recovery took two years. By fiscal 2010 Starbucks was reporting record profits, and the turnaround, told in Schultz's book Onward, is taught at business schools, including in a Harvard Business School course on leadership.</p>''')}
{lessons([
    ("Growth can erode the process that made you good.", f"Each shortcut can be justified on its own. A regular check of your core process against your own standard, through {L('essentials-of-effective-process-documentation', 'documented procedures')} and audits, shows the drift before customers do."),
    ("Training is an operational investment, not an overhead.", "Starbucks treated an evening of lost sales as the price of consistent quality. Measure what poor quality costs you in rework, complaints and lost customers before you decide training is too expensive."),
    ("Visible actions change behaviour faster than memos.", f"People believe what leaders do. A {L('change-management-toolkit-the-top-10-models-and-how-to-choose-the-right-one-for-your-organization', 'change management model')} helps plan the follow-through, but one clear act shows what matters."),
    ("A single gesture is not a turnaround.", "The closure worked because it was followed by store closures, supply chain changes and manager training. Plan the next steps before the first one."),
])}
{src([("Mail &amp; Guardian (Guardian News), \"Starbucks closes to learn how to make coffee\" (February 26, 2008)", "https://mg.co.za/?p=478515"),
      ("TIME, \"Starbucks Looks for a Fresh Jolt\" (2008)", "https://content.time.com/time/subscriber/article/0,33009,1725973-2,00.html"),
      ("Retail Customer Experience, citing The Wall Street Journal, \"Starbucks closes 7,100 stores for training\" (2008)", "https://www.retailcustomerexperience.com/news/starbucks-closes-7100-stores-for-training/"),
      ("Harvard Business School Working Knowledge, Nancy Koehn on Howard Schultz and the Starbucks turnaround", "https://hbswk.hbs.edu/item/7593.html"),
      ("NPR, \"Starbucks CEO: Can You 'Get Big And Stay Small'?\" (2011)", "https://www.npr.org/2011/03/28/134738487/starbucks-ceo-can-you-get-big-and-stay-small")])}
{nav(S_SBUX)}"""


# ───────────────────────── 6. Toyota ─────────────────────────
def toyota():
    ex3 = cols("Toyota September 2021 global production: planned just under 900,000 vehicles, revised to about 540,000.",
               [(["Original plan"], 900, MUTED, "≈ 900,000"), (["Revised plan"], 540, RED, "≈ 540,000")], w=520, h=260)
    return f"""{CSS}{intro(S_TOYOTA, "The decision belongs to Toyota's purchasing and production leadership in late 2021, after the company's September production cut.")}
<h2>The decision</h2>
<p>For most of 2021, Toyota was the automaker that had beaten the chip shortage. While rivals idled plants and parked unfinished cars waiting for semiconductors, Toyota kept its lines running, because after the 2011 earthquake it had asked suppliers to hold months of chips in reserve. Then, on August 19, 2021, Toyota announced that it would cut its global production for September by about 40%. The cause was not mainly chips. COVID outbreaks in Vietnam, Malaysia and Thailand had closed suppliers of other parts that Toyota had never thought to stockpile.</p>
<p>The company that taught the world just-in-time had to decide what its rule should now be. How much inventory should it hold, of which parts, held by whom, and at whose cost?</p>
<h2>Company background</h2>
<p>The Toyota Production System, developed from the 1950s by Taiichi Ohno and others, treats excess inventory as waste. Parts arrive just in time for use, problems are exposed rather than buried under stock, and suppliers deliver in small, frequent lots. The system made Toyota one of the most efficient and highest-quality carmakers in the world and was copied across industries under the name lean manufacturing.</p>
<p>Just-in-time has a known weakness: when a supplier stops, the line stops soon after. Toyota learned this painfully on March 11, 2011, when the Tohoku earthquake and tsunami struck northeastern Japan. One of the plants destroyed belonged to Renesas Electronics, a key maker of automotive microcontrollers. Toyota's production fell 78% year on year in April 2011. It took four months to return Japanese production to normal and six months overseas.</p>
<h2>What Toyota changed after 2011</h2>
{table(1, "Toyota's changes after the 2011 earthquake", ["Change", "What it does"],
       [["RESCUE supplier database", "Maps thousands of parts back through tier-two and lower suppliers, so Toyota knows which factory makes what, and where"],
        ["Business continuity plan (BCP)", "Classifies parts by risk; for the most critical, requires suppliers to hold extra stock, reported as two to six months of chips depending on lead time"],
        ["Semiconductor know-how", "Toyota had run its own chip plant since 1989 and understood its chip supply chain in unusual depth"],
        ["Faster escalation", "Routines to detect a disruption and act on it within days"]])}
<p>The approach paid off at first. In February 2021, Toyota's chief financial officer said the company had secured one to four months of stock for various semiconductors and did not expect a major impact on production. The consultancy AlixPartners estimated that the chip shortage cost the industry about $210 billion in lost sales in 2021. Toyota kept its U.S. lines running at close to 90% of capacity through June.</p>
<h2>The situation in late 2021</h2>
<p>The September cut showed the limit of the plan. Toyota had protected the parts it knew were risky. The new shortage came from ordinary parts, made by suppliers in Southeast Asia whose factories were closed by public health orders. Twenty-seven of Toyota's 28 assembly lines in Japan were affected for part of September.</p>
{exfig(ex3, "Exhibit 2. Toyota's September 2021 global production plan, before and after the cut announced on August 19, 2021.")}
{table(3, "The trade-off in numbers (illustrative)", ["Item", "Just-in-time", "Two months' buffer on critical parts"],
       [["Inventory carrying cost", "Low", "Typically 20% to 30% a year of the value of the stock held"],
        ["Cash tied up", "Minimal", "Two months of spend on the covered parts"], ["Problems exposed quickly", "Yes", "Partly hidden by stock"],
        ["Survives a short supplier outage", "No", "Yes, up to the buffer"], ["Survives an outage of an uncovered part", "No", "No"]])}
<h2>The options</h2>
{options([
    ("Keep the plan as it is", "The BCP worked for chips; the Southeast Asia closures were a once-in-a-century pandemic event. Keep buffers for the critical list only and protect the efficiency of just-in-time."),
    ("Widen the buffer to more parts", "Extend extra stock to more categories, including ordinary parts from concentrated regions. Higher carrying cost, borne by Toyota or its suppliers."),
    ("Diversify sources instead of stocking", "Qualify second suppliers in other regions for parts made in one area. Slower and costly to set up, but it protects against regional events without holding stock."),
    ("Combine visibility, targeted buffers and dual sourcing", "Use the RESCUE data to rank parts by impact and recovery time, and choose stock, a second source or nothing for each."),
])}
{questions([
    "Is holding months of chips a departure from the Toyota Production System, or an application of it? What did Ohno's rule actually aim to eliminate?",
    "Use Exhibit 3. How would you decide which parts deserve a buffer? Which two or three measures would you use?",
    "Who should pay for the buffer stock, Toyota or the supplier? What happens to the relationship either way?",
    "The 2011 plan protected the risks Toyota knew about. How do you plan for the risk you have not identified?",
    "When should a company stop adding buffers? What is the cost of being too safe?",
])}
{reveal(f'''<p>Toyota did not abandon just-in-time, and it did not return to its pre-2011 settings either. It kept the business continuity plan and the RESCUE database, and continued to hold targeted stocks of critical parts, while adjusting production plans repeatedly through late 2021 and 2022 as parts shortages came and went. Even with the cuts, Toyota outsold General Motors in the United States in 2021, the first time since 1931 that GM had not been the top-selling carmaker there, which analysts largely credited to Toyota's supply chain management.</p>
<p>The wider industry moved toward Toyota's approach. Carmakers that had cut inventories to the bone after the 2008 financial crisis began to map their lower-tier suppliers and to hold more stock of critical parts. In Europe, a group led by BMW and SAP founded Catena-X in 2021 to build a shared supplier database similar to RESCUE.</p>
<p>The lasting lesson is that lean and resilient are not opposites. Toyota's system removes stock that hides problems; it does not forbid stock held on purpose against a risk the company has measured.</p>''')}
{lessons([
    ("Hold stock on purpose, not by habit.", f"Lean removes inventory that hides waste. A buffer sized against a known risk is a decision, not waste. The {L('safety-stock-for-manufacturers', 'safety stock for manufacturers')} post shows how to size one from demand and lead-time variation."),
    ("Know your suppliers' suppliers.", "Most SMEs know their direct suppliers well and little beyond them. A simple list of where your critical parts are actually made shows where a single event could stop you."),
    ("Rank parts by impact, not by value.", f"A cheap part with one source can stop a line as surely as an expensive one. Combine an {L('abc-analysis-for-manufacturers', 'ABC analysis')} by value with a ranking by supply risk."),
    ("Plans protect against known risks; flexibility protects against the rest.", "Second sources, alternate designs and fast escalation help when the disruption is one you did not foresee."),
])}
{src([("Reuters via Nippon.com, \"How Toyota thrives when the chips are down\" (March 2021)", "https://www.nippon.com/en/news/reu20210309KBN2B1004/"),
      ("Supply Chain Dive, Toyota on the semiconductor shortage and its business continuity plan (2021)", "https://www.supplychaindive.com/news/toyota-semiconductor-shortage-earthquake-inventory-ihs-gartner-forecast-2022/600193/"),
      ("Bloomberg Businessweek, \"How Toyota Steered Clear of the Chip Shortage Mess\" (April 2021)", "https://brp-prod-bcc.bloomberg.com/news/articles/2021-04-07/how-toyota-s-supply-chain-helped-it-weather-the-chip-shortage"),
      ("Fortune, \"Toyota's chip shortage strategy\" and the RESCUE database (August 2021)", "https://fortune.com/2021/08/02/toyota-cars-chip-shortage-semiconductors/"),
      ("The Japan Times, Toyota cuts September output by 360,000 units (August 19, 2021)", "https://www.japantimes.co.jp/news/2021/08/19/business/toyota-cut/"),
      ("IndustryWeek, \"Toyota Announces 40% Worldwide Production Cut\" (2021)", "https://www.industryweek.com/supply-chain/article/21172830/toyota-announces-40-worldwide-production-cut-due-next-month"),
      ("Fortune, Toyota beats GM in U.S. sales for 2021 (January 2022)", "https://dc.fortune.com/2022/01/05/toyota-beats-gm-car-sales-chip-shortage-supply-chain")])}
{nav(S_TOYOTA)}"""


# ───────────────────────── 7. Lululemon ─────────────────────────
def lululemon():
    ex2 = bars("Lululemon's 2012 net income was 271 million dollars; the expected 2013 revenue impact of the recall was 57 to 67 million dollars.",
               [("Net income, fiscal 2012", 271, BLUE, "$271M"), ("Expected 2013 revenue hit", 67, RED, "$57M to $67M")], maxv=320, lw=220)
    return f"""{CSS}{intro(S_LULU, "The decision belongs to Christine Day, Lululemon's chief executive, in March 2013.")}
<h2>The decision</h2>
<p>In March 2013, store managers at Lululemon Athletica began reporting the same complaint from customers: some of the company's best-selling black yoga pants became see-through when the wearer bent over. The pants were made from Luon, Lululemon's own nylon and Lycra fabric, by the same manufacturer and with the same materials the company had used since 2004. Nothing in the standard laboratory tests had flagged a problem.</p>
<p>The affected styles were the core of the business: the black Wunder Under and Groove pants that had made the brand. Christine Day, the chief executive, had to decide quickly. Pulling every suspect pair would empty shelves for months and cut tens of millions of dollars from the year's revenue. Selling through, or quietly replacing stock, would protect the quarter and put the brand's reputation for quality at risk.</p>
<h2>Company background</h2>
<p>Chip Wilson founded Lululemon in Vancouver in 1998 to sell technical yoga wear, and the company created a category: premium athletic clothing worn far beyond the gym. It sold through its own stores, staffed by "educators" and tied to local yoga and running communities, and kept prices high, with few discounts. The company went public in 2007. Day, a former Starbucks executive, became chief executive in 2008 and led a period of rapid growth.</p>
{table(1, "Lululemon before the recall", ["Measure", "Position"],
       [["Revenue, fiscal 2012", "about $1.37 billion, up 37%"], ["Net income, fiscal 2012", "about $271 million"],
        ["Sales per square foot", "about $1,800, among the highest in U.S. retail"],
        ["Black Luon pants pulled", "about 17% of all women's pants in stores"],
        ["Earlier quality issue", "Colour bleeding in some bright fabrics in 2012"]])}
<h2>The situation in March 2013</h2>
<p>The defect was hard to detect. The fabric looked normal on the table and passed tests for pilling, shrinkage, abrasion and colourfastness by an independent testing company. It became sheer only when stretched in four directions at once, as it is in a yoga pose. Day later told investors that the only way to test for it was to put the pants on and bend over. The cause was not yet known; it could be the fabric, the dyeing or the finishing.</p>
{exfig(ex2, "Exhibit 2. The size of the decision. A full recall was expected to remove $57 million to $67 million of revenue in 2013, a large sum against $271 million of net income the year before.")}
{table(3, "What each option protects", ["", "Pull all suspect stock", "Pull only confirmed defects", "Keep selling, fix the next batch"],
       [["Brand reputation for quality", "Best protected", "Partly", "At risk"], ["2013 revenue", "Largest loss", "Smaller loss", "Protected in the short run"],
        ["Customer experience", "Shortage of core styles", "Inconsistent", "Some customers buy defective pants"],
        ["Supplier relationship", "Strained", "Strained", "Unchanged until the cause is found"]])}
<h2>The options</h2>
{options([
    ("Pull all black Luon pants from the suspect shipments and say so publicly", "Remove the stock from stores and the website, offer refunds or exchanges, and announce the problem before customers spread it. Expect a shortage of core styles for months."),
    ("Test and pull only confirmed defects", "Inspect stock and remove only pants that fail a stretch test. Less revenue lost, but slower, and hard to do consistently in hundreds of stores."),
    ("Sell through and correct future production", "Keep current stock on sale, handle complaints case by case, and fix the cause in the next batch. Protects the quarter, but if the problem becomes public, the company will look as if it hid it."),
])}
{questions([
    "Lululemon's product passed every laboratory test it ran. What does that tell you about how test methods should be chosen?",
    "Use Exhibit 2. Is a $60 million hit to revenue a reasonable price for protecting the brand? How would you decide?",
    "How should the company talk to customers, investors and staff in the first 48 hours?",
    "Who is accountable for the defect: the supplier, the product team or the chief executive? Does the answer change what you do next?",
    "What quality controls would you put in place so the next problem is found before it reaches stores?",
])}
{reveal(f'''<p>Day chose the full recall. On March 18, 2013, Lululemon announced that it was pulling the affected black Luon pants, about 17% of the women's pants in its stores, from shelves and its website, and offering customers refunds or exchanges. The company warned of a shortage of those styles in the near term and later estimated that the problem would reduce 2013 revenue by $57 million to $67 million. The share price fell about 5% on the news.</p>
<p>The recall itself was widely seen as the right call, but the handling drew ridicule. Day's remark that the only test was to bend over in the pants became a punchline, and reports that some store staff asked customers to demonstrate the problem made it worse; the company said that was not its policy. The chief product officer, Sheree Waterson, left the company. In June 2013 Day announced she would step down once a successor was found, and the shares fell about 16% in a day.</p>
<p>The year ended with a second crisis. In November 2013, founder Chip Wilson said in a Bloomberg television interview that some women's bodies were not suited to the pants. The backlash was immediate, he apologised, and in December he stepped down as chairman. Laurent Potdevin, president of TOMS Shoes, was named chief executive.</p>
<p>Lululemon recovered. It overhauled its quality checks and product leadership and grew into one of the largest athletic apparel companies in the world. The recall is now taught as a case in which the operational decision was right and the communication around it was not.</p>''')}
{lessons([
    ("Test the product the way the customer uses it.", f"A test that does not reproduce real use gives false confidence. This is a core idea of {L('building-effective-quality-management-systems', 'quality management systems')} and of {L('iso-9001-for-small-and-mid-sized-businesses', 'ISO 9001')}: verify against the requirement, not only against a standard method."),
    ("A change you did not make can still change your product.", "The supplier and the materials were the same, but the product changed. Incoming inspection and periodic re-testing catch drift that a supplier may not report."),
    ("Recall fast, and plan what you will say.", "Pulling the product protected the brand; careless words cost the chief executive her job. Prepare a short, factual message for customers, staff and investors before you need it."),
    ("Quality problems repeat until the system changes.", "Colour bleeding in 2012 was a warning. Track defects and complaints over time, not one incident at a time."),
])}
{src([("ABC News, \"Lululemon Expects Shortage of Luon Pants\" (March 19, 2013)", "https://www.goodmorningamerica.com/news/story/lululemon-luon-sheer-pants-shortage-18762600"),
      ("Toronto Star via PressReader, \"Downward dog reveals sheer extent of Lululemon's mistake\" (March 22, 2013)", "https://www.pressreader.com/canada/toronto-star/20130322/281513633600255"),
      ("Bloomberg Businessweek, \"What Lululemon's Yoga Pants Recall Reveals\" (March 2013)", "https://www.bloomberg.com/news/articles/2013-03-28/what-lululemons-yoga-pants-recall-reveals"),
      ("The Motley Fool, \"Can This Retailer Correct Its Wardrobe Malfunction?\" (March 2013: 2012 revenue, net income, testing)", "https://www.fool.com/investing/general/2013/03/30/can-this-retailer-correct-its-wardrobe-malfunction.aspx"),
      ("UPI, \"Lululemon stock plummets after CEO resignation\" (June 2013)", "https://www.upi.com/Business_News/Blog/2013/06/12/Lululemon-stock-plummets-after-CEO-resignation/4141371048001/"),
      ("Wikipedia, Lululemon Athletica (history, 2013 recall, leadership changes)", "https://en.wikipedia.org/wiki/Lululemon")])}
{nav(S_LULU)}"""


# ───────────────────────── 8. Netflix ─────────────────────────
def netflix():
    ex2 = cols("Netflix U.S. subscribers: 24.6 million at the end of June 2011, 23.8 million at the end of September, 24.4 million at the end of December.",
               [(["June 2011"], 24.6, BLUE, "24.6M"), (["Sept 2011"], 23.8, RED, "23.8M"), (["Dec 2011"], 24.4, GREEND, "24.4M")], w=560, h=260, maxv=25.2, ymin=22.5)
    return f"""{CSS}{intro(S_NFLX, "The decision belongs to Reed Hastings, Netflix's co-founder and chief executive, in the spring and summer of 2011.")}
<h2>The decision</h2>
<p>In mid-2011 Netflix looked unstoppable. Its old rival Blockbuster had gone bankrupt the previous autumn. Its share price had climbed past $300. Most of its customers paid $9.99 a month for a plan that combined unlimited streaming with one DVD by mail at a time. Reed Hastings believed the DVD business, profitable as it was, would shrink, and that the company's future was streaming alone. Streaming needed much more money for film and TV licences, and the content owners were raising their prices sharply.</p>
<p>Hastings had to decide how fast to move. Netflix could keep the combined plan and let customers drift to streaming in their own time. Or it could separate the two services and price them separately now, so that each paid its own way and the company could put its money into streaming. Separate prices meant that a customer who wanted both would pay much more.</p>
<h2>Company background</h2>
<p>Hastings and Marc Randolph founded Netflix in 1997 as a DVD-by-mail rental service. Its subscription model, with no late fees and a queue of films delivered in red envelopes, beat Blockbuster's stores and fees. In 2007 Netflix added streaming at no extra charge for its DVD subscribers. Streaming grew rapidly as broadband spread and Netflix's app appeared on game consoles, TVs and phones, and in 2010 the company launched its first streaming-only plan and expanded to Canada.</p>
<p>The two businesses had very different economics. DVD rental relied on owning physical discs, distribution centres and postage, a business with a known cost but no growth. Streaming relied on licensing content from studios for a fixed fee over a period, which became more expensive every time a deal was renewed, but cost almost nothing to deliver to one more customer.</p>
<h2>The situation in mid-2011</h2>
{table(1, "Netflix's plans before and after the proposed change (U.S.)", ["Plan", "Before", "Proposed"],
       [["Unlimited streaming only", "$7.99", "$7.99"], ["One DVD at a time only", "Not offered separately", "$7.99"],
        ["Streaming plus one DVD", "$9.99", "$15.98 ($7.99 + $7.99)"], ["Change for a combined customer", "", "+60%"]])}
<p>Netflix's management saw that the combined plan hid the real cost of each service and slowed the shift to streaming. Content costs were rising fast; a major licence with Starz, which supplied many recent films, was up for renewal. Hastings had also seen how hard it was for a company to give up a business that still made money: AOL with dial-up, Blockbuster with stores. He wanted Netflix to move before the change was forced on it.</p>
<p>The risk was customer anger. A 60% price increase for the most loyal customers, with no new benefit, would be the largest in the company's history. Netflix had few streaming competitors of its size in 2011, but customers could cancel with a click.</p>
<h2>The options</h2>
{options([
    ("Keep the combined plan for now", "Raise prices modestly over time and let DVD decline naturally. Smoother for customers, but streaming growth stays tied to an old business and Netflix may be too slow when rivals arrive."),
    ("Separate prices, one company", "Price streaming and DVD separately at $7.99 each, under one brand and one website. Clear economics and a strong push to streaming, at the cost of a 60% increase for combined customers."),
    ("Separate prices and separate companies", "Split the DVD service into its own brand with its own website, account and management, so each can be run for its own market. Maximum focus on streaming, but customers who want both must manage two accounts."),
    ("Exit DVD outright", "Announce a closing date for the DVD service and move all effort to streaming. Clear, but it gives up a profitable business and millions of customers who still want discs."),
])}
{questions([
    "Was Hastings right that the DVD business would shrink? If so, why did moving early cause so much damage?",
    "Use Exhibit 1. How would you have introduced the new prices to soften the reaction? What would you have offered existing customers?",
    "What is the difference between Option B and Option C for the customer? For the company?",
    "When should a company stop protecting a profitable product that it believes is declining?",
    "How much customer loss would you have accepted to reach a streaming-only future a year or two earlier?",
])}
{reveal(f'''<p>Hastings went further than most observers expected. On July 12, 2011, Netflix announced that it would separate the plans, raising the price for customers who wanted both from $9.99 to $15.98 a month, about 60% more. The reaction was furious, on Netflix's own blog, Facebook page and in the press. On September 18, Hastings published an apology for how the change had been explained, and in the same post announced that the DVD service would become a separate company called Qwikster, with its own website and account. Customers who wanted both services would have to use two sites.</p>
<p>The second announcement made things worse. On October 10, just over three weeks later, Netflix cancelled Qwikster, though it kept the new prices. In the third quarter Netflix lost about 800,000 U.S. subscribers, ending September with 23.8 million, its first decline in years and more than the 600,000 it had predicted. The share price fell from a peak near $305 in July to the $60s and $70s by late 2011, a loss of more than three-quarters of its value. Hastings later said Netflix had moved too fast.</p>
{exfig(ex2, "Exhibit 2. U.S. subscribers in 2011. Netflix lost about 800,000 in the quarter after the price change and regained about 600,000 in the next.")}
<p>The recovery came quicker than the reaction suggested. Netflix added about 600,000 U.S. subscribers in the fourth quarter, ending 2011 with 24.4 million. It then put its money into streaming and, from 2013, its own programming, starting with House of Cards. The DVD service continued, shrinking, until Netflix closed it on September 29, 2023. By the end of 2024 Netflix had more than 300 million paid memberships worldwide.</p>
<p>In hindsight, the strategy was right and the execution was wrong. Separating the prices pushed customers toward the future Netflix was betting on. Doing it suddenly, with a large increase, no new benefit and then a confusing split, turned loyal customers into critics.</p>''')}
{lessons([
    ("Be willing to replace your own product before a competitor does.", "Netflix chose to shrink a profitable business to grow the one with a future. Most SMEs have a legacy product or service that will decline; plan the move rather than waiting for it."),
    ("A right strategy can still fail on execution.", f"The size of a price change, how it is explained and what customers get in return matter as much as the logic behind it. Test the message with a few customers first. The {L('navigating-change-implementing-digital-technology-with-effective-change-management', 'change management')} principles apply to customers as much as to staff."),
    ("Do not make customers do the work of your reorganisation.", "Qwikster asked customers to manage two accounts so that Netflix could run two businesses. Organise internally however you like; keep it simple for the customer."),
    ("Correct mistakes quickly.", "Netflix reversed Qwikster in three weeks, which limited the damage. Admitting a wrong call early costs less than defending it."),
])}
{src([("TIME, top 10 business flops of 2011: Netflix (prices, share price)", "https://content.time.com/time/specials/packages/article/0,28804,2101344_2101318_2101320,00.html"),
      ("Associated Press via The Washington Times, \"Netflix loses 800,000 U.S. subscribers in tough 3Q\" (October 24, 2011)", "https://www.washingtontimes.com/news/2011/oct/24/netflix-loses-800000-us-subscribers-in-tough-3q/"),
      ("Associated Press via Manufacturing.net, timeline of Netflix events in 2011 and fourth-quarter recovery", "https://www.manufacturing.net/home/news/13228950/netflix-gets-back-on-track-after-rough-2011"),
      ("Quartz, \"As Netflix turns 20, let's revisit its biggest blunder\"", "https://qz.com/1245107/as-netflix-turns-20-lets-revisit-its-biggest-blunder/"),
      ("Yahoo News (AP), \"A look at Netflix since stock plunged from peak\"", "https://news.yahoo.com/look-netflix-since-stock-plunged-222335750.html")])}
{nav(S_NFLX)}"""


ARTICLES = [
    dict(slug=S_COSTCO, cats=["case-study", "strategy", "inventory-management"], fn=costco,
         desc="A teaching case: in 2004 Wall Street pressed Costco to raise margins and cut wages. The 14% markup cap, the 4,000-product range, the options, and what happened.",
         tags=["Costco", "case study", "business model", "membership", "markup", "retail strategy"],
         related=["abc-inventory-analysis", S_AMAZON, "analyzing-tesla-s-business-model-canvas-how-the-company-drives-sustainable-innovation"]),
    dict(slug=S_AMAZON, cats=["case-study", "marketing", "operational-efficiency"], fn=amazon,
         desc="A teaching case: in 2005 Jeff Bezos launched Prime though finance's numbers looked bad. The $79 fee, shipping economics, the options, and what happened.",
         tags=["Amazon", "Amazon Prime", "case study", "subscription", "customer loyalty", "fulfilment"],
         related=[S_COSTCO, S_SHOPIFY, "quote-to-cash-process-in-manufacturing"]),
    dict(slug=S_SHOPIFY, cats=["case-study", "strategy", "digital-technology"], fn=shopify,
         desc="A teaching case: after four years and billions of dollars on logistics, Shopify had to decide whether warehouses belonged in its core business.",
         tags=["Shopify", "case study", "logistics", "core business", "Deliverr", "Flexport"],
         related=[S_AMAZON, "how-shopify-and-lovable-are-empowering-aspiring-entrepreneurs-to-launch-online-stores", S_NFLX]),
    dict(slug=S_APPLE, cats=["case-study", "inventory-management", "process-improvement"], fn=apple,
         desc="A teaching case: in 1998 Tim Cook cut Apple's inventory from two months to six days and moved to outsourced manufacturing. The options and the outcome.",
         tags=["Apple", "Tim Cook", "case study", "inventory", "supply chain", "outsourcing"],
         related=["setting-safety-stock", "reorder-point-and-eoq-when-to-order-and-how-much", S_TOYOTA]),
    dict(slug=S_SBUX, cats=["case-study", "change-management", "operational-efficiency"], fn=starbucks,
         desc="A teaching case: in 2008 Howard Schultz closed 7,100 Starbucks stores for an evening to retrain 135,000 baristas. The situation, options and outcome.",
         tags=["Starbucks", "Howard Schultz", "case study", "turnaround", "training", "customer experience"],
         related=["change-management-toolkit-the-top-10-models-and-how-to-choose-the-right-one-for-your-organization", "essentials-of-effective-process-documentation", S_LULU]),
    dict(slug=S_TOYOTA, cats=["case-study", "lean", "inventory-management"], fn=toyota,
         desc="A teaching case: Toyota stockpiled chips after 2011 and rode out the shortage, then cut output 40% in 2021. How much buffer should a lean company hold?",
         tags=["Toyota", "just-in-time", "case study", "supply chain resilience", "lean", "safety stock"],
         related=["safety-stock-for-manufacturers", "how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations", S_APPLE]),
    dict(slug=S_LULU, cats=["case-study", "iso", "change-management"], fn=lululemon,
         desc="A teaching case: in 2013 Lululemon found its best-selling yoga pants were see-through. Recall or sell through? The tests, the options and the outcome.",
         tags=["Lululemon", "case study", "product recall", "quality control", "Vancouver", "crisis communication"],
         related=["building-effective-quality-management-systems", "iso-9001-for-small-and-mid-sized-businesses", S_SBUX]),
    dict(slug=S_NFLX, cats=["case-study", "strategy", "marketing"], fn=netflix,
         desc="A teaching case: in 2011 Netflix split DVD from streaming and raised prices 60%, then launched and dropped Qwikster. The decision, the options and the outcome.",
         tags=["Netflix", "Qwikster", "case study", "pricing", "disruption", "strategy"],
         related=[S_SHOPIFY, S_COSTCO, "navigating-change-implementing-digital-technology-with-effective-change-management"]),
]

if __name__ == "__main__":
    for i, a in enumerate(ARTICLES):
        body = a.pop("fn")()
        words = len(re.sub(r"<svg.*?</svg>|<[^>]+>", " ", body, flags=re.S).split())
        a.update(title=TITLES[a["slug"]], body=body, date=DATE, author="Quak Foo Lee",
                 read=f"{max(1, round(words / 220))} min read", cover_label="Case study",
                 series=dict(name=SERIES))                  # unnumbered: the cases stand alone, and more will be added
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"], words, "words,", a["read"])
