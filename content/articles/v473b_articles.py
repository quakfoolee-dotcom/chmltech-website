"""V4.73 (second half): five older articles rewritten at their original addresses, five posts retired.

1. post/top-10-inventory-management-software-a-comprehensive-comparison-guide   rewritten for 2026
     retired into it: optimize-your-production-schedule-with-kanata-mrp
2. post/what-is-technical-seo-basics-and-10-best-practices                      rewritten (Core Web Vitals, INP, AI features)
     retired into it: the-ultimate-guide-to-seo-and-google-search-expert-tips-and-case-studies
3. post/cybersecurity-for-small-businesses-tips-and-best-practices               rewritten around the Cyber Centre baseline controls
4. post/essentials-of-effective-process-documentation                            rewritten, with a swim lane example (PNG download)
5. post/50-must-track-kpis-for-business-success-from-finance-to-product-development   rewritten: formulas fixed, duplicates removed
     retired into it: do-you-have-the-right-kpis-set-for-each-team-member, understanding-12-types-of-key-performance-indicators

The change management toolkit and the QMS article are upgraded in place by v473b_inplace.py.

Usage:  python3 content/articles/v473b_articles.py
        python3 content/gen/refresh_article.py <slug>                 (each of the five)
        python3 content/gen/refresh_article.py --retire <old> <new>   (each retired post)
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, MUTED, LINE, SAND, PALE, GREENF, ORANGEF

DATE = "2026-11-13"
INV = "top-10-inventory-management-software-a-comprehensive-comparison-guide"
INV_RETIRE = ["optimize-your-production-schedule-with-kanata-mrp"]
SEO = "what-is-technical-seo-basics-and-10-best-practices"
SEO_RETIRE = ["the-ultimate-guide-to-seo-and-google-search-expert-tips-and-case-studies"]
CYB = "cybersecurity-for-small-businesses-tips-and-best-practices"
DOC = "essentials-of-effective-process-documentation"
KPI = "50-must-track-kpis-for-business-success-from-finance-to-product-development"
KPI_RETIRE = ["do-you-have-the-right-kpis-set-for-each-team-member", "understanding-12-types-of-key-performance-indicators"]
SWIM_PNG = "Chmltech_Swim_Lane_Quote_to_Order.png"


def src(items):
    return "<h2>Sources</h2><ul>" + "".join(
        f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in items) + "</ul>"


def rel(items):
    return "<h2>Related reading</h2><ul>" + "".join(f'<li><a href="../post/{s}.html">{t}</a></li>' for s, t in items) + "</ul>"


def money(x):
    return f"${x:,.0f}"


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table>\n<tr>{h}</tr>\n{b}\n</table>"


# ═════════════════════════ 1. Inventory software ═════════════════════════
def fig_inv_types():
    s = DEFS
    cols = [("Track items", ["Tools, supplies,", "spare parts,", "small stock"], "Sortly; the stock", "list in your books", BLUE, PALE),
            ("Sell and ship", ["Orders from several", "channels, purchasing,", "reorder points"], "Zoho Inventory, inFlow,", "Cin7 Core, Unleashed", GREEND, GREENF),
            ("Make products", ["Bills of materials,", "work orders,", "material planning"], "Katana, MRPeasy,", "Fishbowl Manufacturing", PURPLE, "#E7E7F8"),
            ("Run the business", ["Inventory plus", "accounting, CRM", "and HR in one system"], "Odoo; then a", "full ERP", ORANGE, ORANGEF)]
    for i, (h, lines, a, b, c, f) in enumerate(cols):
        x = 14 + i * 182
        s += f'<rect x="{x}" y="14" width="168" height="34" rx="8" fill="{c}"/>' + txt(x + 84, 36, h, "middle", "#fff", 13.5, True)
        s += f'<rect x="{x}" y="54" width="168" height="78" rx="8" fill="{f}" stroke="{c}"/>'
        for k, ln in enumerate(lines): s += txt(x + 84, 78 + k * 18, ln, "middle", NAVY, 12.2)
        s += arrow(x + 84, 134, x + 84, 156, c)
        s += f'<rect x="{x}" y="158" width="168" height="54" rx="8" fill="#fff" stroke="{c}"/>'
        s += txt(x + 84, 181, a, "middle", NAVY, 12, True) + txt(x + 84, 199, b, "middle", NAVY, 12, True)
    s += f'<line x1="14" y1="232" x2="714" y2="232" stroke="{MUTED}" stroke-width="1.4" marker-end="url(#ah)"/>'
    s += txt(14, 252, "Simpler and cheaper", "start", MUTED, 12) + txt(728, 252, "More features, more set-up", "end", MUTED, 12)
    return svg("Four kinds of inventory software, from simplest to broadest. Track items: tools, supplies, spare parts and small stock, "
               "for example Sortly or the stock list in your accounting software. Sell and ship: orders from several channels, purchasing "
               "and reorder points, for example Zoho Inventory, inFlow, Cin7 Core or Unleashed. Make products: bills of materials, work "
               "orders and material planning, for example Katana, MRPeasy or Fishbowl Manufacturing. Run the business: inventory plus "
               "accounting, CRM and HR in one system, for example Odoo and then a full ERP.", 742, 262, s, 600)


# Worked example (illustrative): a distributor moving from spreadsheets to an order-and-stock system.
INV_AVG, CARRY, CUT = 480_000, 0.25, 0.15
SUB_MO = 349                      # Cin7 Core Standard list price, USD per month (5 users)
ONE_TIME_INV = [("Implementation help and data import", 6_000), ("Staff time: 120 hours at $45", 5_400)]
SAVE_YR = INV_AVG * CUT * CARRY
SUB_YR = SUB_MO * 12
ONE_INV = sum(v for _, v in ONE_TIME_INV)
NET_YR = SAVE_YR - SUB_YR
PAYBACK_INV = ONE_INV / (NET_YR / 12)


def inv():
    tools = [
        ("Sortly", "Track items", "Tools, supplies and small stock; mobile app with barcode and QR labels", "Free plan; paid from $49/mo", "Not built for purchasing or multichannel orders"),
        ("Zoho Inventory", "Sell and ship", "Small sellers and wholesalers, especially on Zoho Books", "Free plan; Standard from $29/mo (annual)", "Order limits on each plan"),
        ("inFlow Inventory", "Sell and ship", "Wholesale and B2B distributors; barcode scanning, B2B showroom", "From about $130 to $190/mo, depending on plan and billing", "Flat rate, but plans cap users and orders"),
        ("Cin7 Core", "Sell and ship", "Product brands selling through several channels; light assembly", "Standard $349/mo (5 users)", "Add-ons and onboarding add to the cost"),
        ("Unleashed", "Sell and ship", "Wholesalers, food and beverage, light manufacturing; strong Xero link", "Core from $399/mo", "Higher entry price; onboarding extra"),
        ("Fishbowl", "Sell and ship, make", "Businesses staying on QuickBooks that need warehouse or manufacturing depth", "From about $229/mo billed annually", "Interface is dated; costs rise per user"),
        ("Katana", "Make products", "Small make-to-stock and make-to-order manufacturers, often on Shopify", "Core $299/mo", "Pricing has changed several times; onboarding fee"),
        ("MRPeasy", "Make products", "Small manufacturers that need real MRP: BOMs, routings, scheduling", "From $49 per user/mo", "Per-user pricing climbs with team size"),
        ("Odoo Inventory", "Run the business", "Firms that want inventory now and accounting, CRM or manufacturing later", "About $31 per user/mo for all apps (Standard, monthly)", "Needs a partner or in-house skills to configure well"),
        ("Accounting package stock", "Track items", "Very small resellers; QuickBooks Online Plus and Advanced track inventory quantities and cost", "Included in the plan", "No bins, lots, BOMs or reorder planning"),
    ]
    one_rows = [[n, money(v)] for n, v in ONE_TIME_INV] + [["<strong>One-time total</strong>", f"<strong>{money(ONE_INV)}</strong>"]]
    body = f"""
<p>This comparison was first written in 2023. Since then one of the original ten has disappeared (Intuit discontinued TradeGecko, which had become QuickBooks Commerce, after 31 August 2023), several vendors have changed their prices more than once, and the choice for a small business now depends less on features and more on what kind of business you run. This rewrite groups the options by job, gives list prices checked in November 2026, and adds a worked example of the payback.</p>
<h2>First, decide which job the software must do</h2>
<p>Most poor choices come from buying for the wrong job: a manufacturer on a stock-tracking app, or a five-person distributor paying for an ERP. Start by placing your business in one of four groups.</p>
{fig(fig_inv_types(), 1, "Four kinds of inventory software. Move right only when the simpler tool is holding you back.")}
<h2>Ten options for small and mid-sized businesses in 2026</h2>
{table(["Software", "Job", "Best fit", "List price (USD)", "Watch for"], tools)}
<p class="note"><em>Prices are vendor list prices as reported in November 2026, in US dollars, before taxes, add-ons and onboarding. Vendors change plans often; confirm on the vendor's own pricing page and ask for the price in Canadian dollars.</em></p>
<h2>A note on Katana for production scheduling</h2>
<p>An earlier article on this site covered production scheduling with Katana. That article has been folded into this one. Katana, now marketed as Katana Cloud Inventory, remains a good fit for small manufacturers that sell online: it links sales orders to manufacturing orders, shows whether materials are available for each order, and lets you drag orders into a new sequence when priorities change. It is lighter than a full MRP. If you need finite capacity scheduling across work centres, routings with setup times, or detailed shop-floor costing, compare it with MRPeasy, and read <a href="../post/understanding-erp-vs-mrp-a-comprehensive-comparison-of-manufacturing-systems.html">ERP vs MRP</a> before you decide.</p>
<h2>What to check before you buy</h2>
<ol>
<li><strong>Your accounting link.</strong> Check that it posts cost of goods sold and inventory value correctly to QuickBooks, Xero or Sage, not just invoices.</li>
<li><strong>How you count and locate stock.</strong> Bins, lots, serial numbers and expiry dates are either built in or painful to add.</li>
<li><strong>Your sales channels.</strong> Shopify, Amazon, a B2B portal and EDI all need tested connectors.</li>
<li><strong>The pricing basis.</strong> Per user, per order, per location or flat rate. Model your volume in two years, not today.</li>
<li><strong>Reorder planning.</strong> At minimum, reorder points and lead times by item. Better tools also support <a href="../post/abc-inventory-analysis.html">ABC analysis</a> and <a href="../post/setting-safety-stock.html">safety stock</a>.</li>
<li><strong>Exit and data ownership.</strong> Make sure you can export items, transactions and history if you outgrow the tool.</li>
</ol>
<h2>Worked example: what does it pay back?</h2>
<p>A distributor with 1,800 items and five office users runs its stock in spreadsheets. Average inventory at cost is {money(INV_AVG)}. Holding stock costs about {CARRY:.0%} a year once money tied up, space, insurance, damage and obsolescence are counted. With reorder points and better purchasing in an order-and-stock system, the business expects to cut average inventory by {CUT:.0%} without more stock-outs. The figures are illustrative.</p>
{table(["One-time cost", "Amount"], one_rows)}
<p>The subscription is {money(SUB_MO)} a month, or {money(SUB_YR)} a year. Cutting average inventory by {money(INV_AVG * CUT)} saves {money(SAVE_YR)} a year in carrying cost, so the net annual benefit is {money(NET_YR)} and the one-time cost pays back in about {PAYBACK_INV:.0f} months. Fewer stock-outs and less time spent counting are on top of that. The main risk is the 15% reduction: it only happens if someone owns the reorder settings and reviews them every month.</p>
""" + src([
        ("QuickBooks Community: QuickBooks Commerce discontinued as a standalone product, 31 August 2023", "https://quickbooks.intuit.com/learn-support/en-us/other-questions/re-is-quickbooks-commerce-tradegecko-ever-returning/01/1490527/highlight/true"),
        ("Capterra: Cin7 Core pricing 2026", "https://www.capterra.com/p/133038/Cin7-Core/pricing/"),
        ("Capterra: Katana Cloud Inventory pricing 2026", "https://www.capterra.com/p/172888/Katana-MRP/pricing/"),
        ("Rework: Best inventory management software in 2026", "https://resources.rework.com/tools/inventory-supply-chain/best-inventory-management-software-2026"),
        ("Rework: Best Katana alternatives in 2026 (MRPeasy and inFlow pricing)", "https://resources.rework.com/tools/inventory-supply-chain/best-katana-alternatives"),
        ("Software Advice: inFlow Inventory pricing", "https://www.softwareadvice.com/inventory-management/inflow-inventory-profile"),
        ("Software Advice: Unleashed pricing", "https://www.softwareadvice.com/scm/unleashed-profile/"),
        ("CostBench: Fishbowl and Sortly pricing", "https://www.costbench.com/software/inventory-management/fishbowl/"),
    ]) + rel([
        ("abc-inventory-analysis", "ABC inventory analysis"),
        ("setting-safety-stock", "Setting safety stock"),
        ("10-best-erp-systems-for-small-and-medium-sized-enterprises", "10 ERP systems for small and mid-sized businesses"),
    ])
    return dict(slug=INV, title="Inventory Management Software for Small Businesses in 2026: 10 Options Compared",
                desc="Ten inventory systems for small businesses in 2026, grouped by job (track, sell, make, run), with list prices, what to check, and a payback example.",
                cats=["inventory-management", "erp", "digital-technology"],
                tags=["inventory management software", "Zoho Inventory", "Cin7 Core", "inFlow", "Katana", "MRPeasy", "Fishbowl", "Odoo", "small business"],
                body=body.strip(), date=DATE, author="Quak Foo Lee", read="6 min read", cover_label="Inventory",
                related=["abc-inventory-analysis", "setting-safety-stock", "10-best-erp-systems-for-small-and-medium-sized-enterprises"])


# ═════════════════════════ 2. Technical SEO ═════════════════════════
def fig_seo_pipeline():
    s = DEFS
    steps = [("1. Discover", ["Links, sitemap"]), ("2. Crawl", ["robots.txt,", "server, CDN"]), ("3. Render", ["JavaScript,", "mobile page"]),
             ("4. Index", ["canonical, noindex,", "duplicates"]), ("5. Show", ["results, rich results,", "AI Overviews"])]
    checks = ["XML sitemap; internal links", "No blocked pages; fast 200s", "Content in the HTML", "One canonical; URL per page", "Snippets allowed; good pages"]
    for i, (h, lines) in enumerate(steps):
        x = 10 + i * 146
        s += box(x, 16, 128, 40, h, fill=NAVY, stroke=NAVY, tc="#fff", fs=13.5)
        s += f'<rect x="{x}" y="62" width="128" height="52" rx="8" fill="{PALE}" stroke="#9AB0C8"/>'
        for k, ln in enumerate(lines): s += txt(x + 64, 84 + k * 17 - (8 if len(lines) == 1 else 0), ln, "middle", NAVY, 12)
        if i < 4: s += arrow(x + 130, 36, x + 144, 36)
        s += f'<rect x="{x}" y="128" width="128" height="40" rx="8" fill="{GREENF}" stroke="{GREEND}"/>'
        w = checks[i].split("; ") if "; " in checks[i] else [checks[i]]
        for k, ln in enumerate(w): s += txt(x + 64, 152 + k * 15 - (7 if len(w) == 2 else 0), ln, "middle", NAVY, 11)
    s += txt(10, 188, "Top row: the step.  Blue: what controls it.  Green: what to check.", "start", MUTED, 12)
    return svg("The five steps from a page on your site to a search result. 1, Discover: through links and the sitemap; check the XML "
               "sitemap and internal links. 2, Crawl: controlled by robots.txt, the server and the CDN; check that no important pages are "
               "blocked and that they return fast 200 responses. 3, Render: JavaScript and the mobile page; check that the content is in "
               "the HTML. 4, Index: canonical tags, noindex and duplicates; check that each page has one canonical URL. 5, Show: search "
               "results, rich results and AI Overviews; check that snippets are allowed and the page is good.", 742, 198, s, 600, 0)


def seo():
    practices = [
        ("1. Let Google crawl what matters", "Check robots.txt does not block CSS, JavaScript or key folders; check your CDN or firewall does not block Googlebot.", "Search Console › URL Inspection › Test live URL"),
        ("2. Publish an XML sitemap", "List only canonical, indexable pages; submit it and reference it in robots.txt.", "Search Console › Sitemaps"),
        ("3. One URL per page", "Redirect http to https and the non-preferred host; set a self-referencing canonical; avoid duplicate parameter URLs.", "Page indexing report: 'Duplicate' reasons"),
        ("4. Use HTTPS everywhere", "Valid certificate, no mixed content, 301 redirects from http.", "Browser address bar; a site crawler"),
        ("5. Make the mobile page complete", "Google indexes the mobile version, so the same content, headings and structured data must be on it.", "URL Inspection › View crawled page"),
        ("6. Meet Core Web Vitals", "LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less, at the 75th percentile of real visits.", "Search Console › Core Web Vitals; PageSpeed Insights"),
        ("7. Keep the content in the HTML", "If content appears only after JavaScript runs, check Google renders it, or render on the server.", "URL Inspection › rendered HTML"),
        ("8. Build clear internal links", "Every important page within three clicks of the home page, with descriptive link text; no orphan pages.", "A site crawler; Links report"),
        ("9. Fix broken pages and redirect chains", "Return 404 or 410 for gone pages, use single 301s for moved pages, update internal links.", "Page indexing report; crawler"),
        ("10. Add structured data where it applies", "Organization, Article, Product, LocalBusiness, BreadcrumbList; match what is visible on the page.", "Rich Results Test; Enhancements reports"),
    ]
    body = f"""
<p>Technical SEO is the work that lets search engines find, read and index your pages. Content and links decide how well a page ranks; technical SEO decides whether it can rank at all. This guide was first written in 2023 and has been rewritten for 2026. It also absorbs an older general SEO guide from this site, so the basics of how Google Search works are covered here too.</p>
<h2>How a page gets into Google</h2>
<p>Google finds a page through links or a sitemap, crawls it, renders it as a mobile browser would, decides whether to index it, and then chooses when to show it. A failure at any step stops everything after it. Most technical SEO problems on small business sites are at steps 2 and 4: pages blocked by accident, or several URLs for the same page.</p>
{fig(fig_seo_pipeline(), 1, "Five steps from your page to a search result, what controls each one, and what to check.")}
<h2>Ten best practices, and how to check each</h2>
{table(["Practice", "What to do", "Where to check"], practices)}
<h2>What changed since 2023</h2>
<ul>
<li><strong>INP replaced FID.</strong> Interaction to Next Paint became a Core Web Vital on 12 March 2024, replacing First Input Delay. It measures how quickly a page responds to every click, tap and key press during a visit, not only the first. A good score is 200 milliseconds or less. Heavy scripts, chat widgets and tag managers are the usual cause of poor INP.</li>
<li><strong>Mobile-first indexing is complete.</strong> Google crawls and indexes with its smartphone crawler, so a stripped-down mobile page means a stripped-down index entry.</li>
<li><strong>AI Overviews and AI Mode use the same index.</strong> Google says there are no additional requirements to appear in them. To be eligible as a supporting link, a page must be indexed and eligible to show with a snippet. Google also says you do not need an llms.txt file or special markup for its AI features.</li>
<li><strong>Google-Extended is separate.</strong> This robots.txt token controls whether your content is used to train and ground Google's Gemini models. Blocking it does not remove you from Search or AI Overviews; robots.txt rules for Googlebot and the nosnippet and noindex controls are what govern Search. Other AI companies run their own crawlers, such as GPTBot and ClaudeBot, each with its own robots.txt token. Decide on these as a content licensing choice, not an SEO one.</li>
</ul>
<h2>The basics that still decide rankings</h2>
<p>Technical SEO removes obstacles. Rankings still come from pages that answer a searcher's question better than the alternatives, written by people who know the subject, on a site others link to and mention. For a small business that means one clear page per service, a page for each location you serve, a complete Google Business Profile, and articles that show real experience: worked examples, photos of your own work, and numbers from your own projects.</p>
<h2>A one-hour monthly check</h2>
<ol>
<li>Search Console › Page indexing: look for new "Not indexed" reasons on pages that should be indexed.</li>
<li>Search Console › Core Web Vitals: look for URLs that moved to "Poor" or "Needs improvement".</li>
<li>Search Console › Performance: compare clicks and impressions with last month for your top 20 pages.</li>
<li>Run a crawler over the site for broken links, redirect chains and missing titles.</li>
<li>Inspect one key page with URL Inspection to confirm Google sees the content you expect.</li>
</ol>
""" + src([
        ("Google Search Central: AI features and your website", "https://developers.google.com/search/docs/appearance/ai-features"),
        ("Google Search Central: Understanding Core Web Vitals", "https://developers.google.com/search/docs/appearance/core-web-vitals"),
        ("web.dev: Interaction to Next Paint becomes a Core Web Vital on March 12", "https://web.dev/blog/inp-cwv-march-12"),
        ("Google Search Central: Google Search Essentials", "https://developers.google.com/search/docs/essentials"),
        ("Search Engine Journal: Google's AI search guide calls AEO and GEO still SEO", "https://searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026"),
    ]) + rel([
        ("the-key-differences-between-seo-and-geo-for-enhancing-your-online-presence", "SEO vs GEO: how to be found in Google and in AI answers"),
        ("maximize-your-visibility-with-these-local-seo-tips-for-small-businesses", "Local SEO tips for small businesses"),
        ("how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide", "How to measure your website with Google Analytics 4"),
    ])
    return dict(slug=SEO, title="Technical SEO in 2026: Basics and 10 Best Practices for Small Business Websites",
                desc="How Google crawls, renders and indexes a page, ten technical SEO practices with where to check each, Core Web Vitals with INP, and AI Overviews.",
                cats=["marketing", "digital-technology"],
                tags=["technical SEO", "Core Web Vitals", "INP", "crawling", "indexing", "Search Console", "AI Overviews", "Google-Extended"],
                body=body.strip(), date=DATE, author="Quak Foo Lee", read="6 min read", cover_label="SEO",
                related=["the-key-differences-between-seo-and-geo-for-enhancing-your-online-presence",
                         "maximize-your-visibility-with-these-local-seo-tips-for-small-businesses",
                         "how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide"])


# ═════════════════════════ 3. Cybersecurity ═════════════════════════
CONTROLS = [
    ("Plan", BLUE, PALE, ["1. Incident response plan", "8. Secure mobile devices", "10. Secure cloud and", "outsourced IT"]),
    ("Protect", GREEND, GREENF, ["2. Automatic patching", "3. Security software", "4. Secure device settings", "5. Strong authentication (MFA)",
                                  "9. Basic perimeter defences", "11. Secure websites", "12. Access control", "13. Secure portable media"]),
    ("People", PURPLE, "#E7E7F8", ["6. Employee", "awareness training"]),
    ("Recover", ORANGE, ORANGEF, ["7. Back up and", "encrypt data"]),
]


def fig_cyber():
    s = DEFS
    xs = [(14, 168), (196, 230), (440, 140), (594, 140)]
    for (name, c, f, items), (x, w) in zip(CONTROLS, xs):
        s += f'<rect x="{x}" y="14" width="{w}" height="34" rx="8" fill="{c}"/>' + txt(x + w / 2, 36, name, "middle", "#fff", 13.5, True)
        s += f'<rect x="{x}" y="54" width="{w}" height="166" rx="8" fill="{f}" stroke="{c}"/>'
        for k, it in enumerate(items): s += txt(x + (26 if it[0].isalpha() else 10), 76 + k * 18.5, it, "start", NAVY, 12)
    return svg("The 13 baseline cyber security controls of the Canadian Centre for Cyber Security, grouped. Plan: 1 incident response "
               "plan, 8 secure mobile devices, 10 secure cloud and outsourced IT. Protect: 2 automatic patching, 3 security software, 4 "
               "secure device settings, 5 strong authentication with multi-factor, 9 basic perimeter defences, 11 secure websites, 12 "
               "access control, 13 secure portable media. People: 6 employee awareness training. Recover: 7 back up and encrypt data.",
               748, 232, s, 600)


def cyb():
    first = [
        ("Week 1", "Turn on multi-factor authentication for email, accounting, banking and remote access; remove old accounts", "Controls 5 and 12"),
        ("Week 2", "Set every computer and phone to update automatically; replace anything that no longer gets updates", "Controls 2 and 4"),
        ("Week 3", "Back up key data daily, keep one copy offline or immutable, and test a restore", "Control 7"),
        ("Week 4", "Write a one-page incident plan: who to call, how to isolate a device, how to reach your bank and insurer", "Control 1"),
        ("Month 2", "Run short phishing and payment-fraud training; agree a call-back rule for any change to bank details", "Control 6"),
        ("Month 3", "Review cloud services and IT providers: who has admin rights, where data is kept, what they log", "Controls 8 and 10"),
    ]
    body = f"""
<p>This article was first written in 2023 as a list of general tips. It has been rewritten around the Canadian framework that small businesses can actually follow and be certified against, with a 90-day starting plan.</p>
<h2>Why small businesses are targeted</h2>
<p>The Canadian Centre for Cyber Security (the Cyber Centre) judges cybercrime to be the threat most likely to affect small and medium organizations: ransomware, stolen passwords, and fraud such as fake invoices or requests to change a supplier's bank details. These attacks are not personal. They are automated and aimed at whoever has unpatched software, reused passwords or staff who have not seen the tricks before. AI tools have made phishing emails more convincing and voice impersonation cheaper, so the old advice to look for spelling mistakes no longer works.</p>
<h2>The 13 baseline controls</h2>
<p>The Cyber Centre's <em>Baseline Cyber Security Controls for Small and Medium Organizations</em> is written for organizations with fewer than 500 employees. It applies the 80/20 rule: a short list of lower-cost controls that gives most of the protection. They are grouped below.</p>
{fig(fig_cyber(), 1, "The Cyber Centre's 13 baseline controls, grouped by what they do. Numbers follow the Cyber Centre's own list.")}
<h2>A 90-day starting plan</h2>
{table(["When", "Action", "Baseline controls"], first)}
<p>The first three weeks give the largest reduction in risk for the least money. Multi-factor authentication stops most attacks that start with a stolen password, automatic updates close the holes that ransomware uses, and a tested offline backup is what lets you recover without paying.</p>
<h2>Certification: when a customer asks for proof</h2>
<ul>
<li><strong>CyberSecure Canada</strong> is the federal certification program for small and medium organizations, run by Innovation, Science and Economic Development Canada. It is voluntary and is based on the baseline controls. An accredited certification body audits you, and the certification mark is valid for two years. It is a useful answer when larger customers send security questionnaires.</li>
<li><strong>The Canadian Program for Cyber Security Certification (CPCSC)</strong> is mandatory for some defence suppliers. Level 1, an annual self-assessment, was introduced on 14 April 2026 and started appearing in select National Defence contracts in summer 2026. Level 2 requires an external assessment every three years. If you supply, or want to supply, defence work, start with the Level 1 self-assessment.</li>
</ul>
<h2>If something goes wrong</h2>
<p>Isolate the affected device from the network, but do not wipe it. Call your IT provider, your bank if money moved, and your insurer if you have cyber cover. Report the incident to the Cyber Centre and fraud to the Canadian Anti-Fraud Centre. If personal information was involved and there is a real risk of significant harm to the people affected, organizations covered by PIPEDA must report the breach to the Privacy Commissioner of Canada and notify those people, and must keep a record of every breach for two years. Quebec and some sectors have their own rules.</p>
<h2>Operational technology</h2>
<p>For manufacturers and process plants, control systems need the same discipline: separate the plant network from the office network, remove default passwords on PLCs and HMIs, control remote access by vendors, and keep offline copies of control programs. Treat a change to control system access as a change under your <a href="../post/management-of-change-for-small-plants.html">management of change</a> procedure.</p>
""" + src([
        ("Canadian Centre for Cyber Security: Baseline cyber security controls for small and medium organizations", "https://cyber.gc.ca/en/guidance/baseline-cyber-security-controls-small-and-medium-organizations"),
        ("Canadian Centre for Cyber Security: Top measures to enhance cyber security for small and medium organizations", "https://cyber.gc.ca/en/guidance/top-measures-enhance-cyber-security-small-and-medium-organizations-itsap10035"),
        ("ISED: CyberSecure Canada", "https://ised-isde.canada.ca/site/cybersecure-canada/en"),
        ("PSPC: Government of Canada introduces Level 1 of the CPCSC (April 2026)", "https://www.canada.ca/en/public-services-procurement/news/2026/04/government-of-canada-introduces-level-1-of-canadian-program-for-cyber-security-certification.html"),
        ("PSPC: Cyber security certification for defence suppliers in Canada", "https://www.canada.ca/en/public-services-procurement/services/industrial-security/security-requirements-contracting/cyber-security-certification-defence-suppliers-canada.html"),
        ("Office of the Privacy Commissioner of Canada: What you need to know about mandatory reporting of breaches", "https://www.priv.gc.ca/en/privacy-topics/privacy-breaches/respond-to-a-privacy-breach-at-your-business/gd_pb_201810/"),
    ]) + rel([
        ("management-of-change-for-small-plants", "Management of change for small plants"),
        ("iso-iec-42001-alongside-iso-9001-adding-ai-governance", "ISO/IEC 42001 alongside ISO 9001: adding AI governance"),
        ("iso-9001-risk-based-thinking-in-practice", "ISO 9001 risk-based thinking in practice"),
    ])
    return dict(slug=CYB, title="Cybersecurity for Small Businesses in Canada: The 13 Baseline Controls and a 90-Day Plan",
                desc="The Cyber Centre's 13 baseline controls for small businesses, a 90-day starting plan, CyberSecure Canada and CPCSC certification, and what to do after an incident.",
                cats=["digital-technology"],
                tags=["cybersecurity", "small business", "baseline controls", "Canadian Centre for Cyber Security", "CyberSecure Canada", "CPCSC", "MFA", "ransomware"],
                body=body.strip(), date=DATE, author="Quak Foo Lee", read="5 min read", cover_label="Cybersecurity",
                related=["management-of-change-for-small-plants", "iso-iec-42001-alongside-iso-9001-adding-ai-governance", "iso-9001-risk-based-thinking-in-practice"])


# ═════════════════════════ 4. Process documentation ═════════════════════════
LANES = ["Customer", "Sales", "Engineering", "Operations"]
LANE_C = [(BLUE, PALE), (GREEND, GREENF), (PURPLE, "#E7E7F8"), (ORANGE, ORANGEF)]


def swim_svg(standalone=False):
    W, LH, X0 = 960, 92, 120
    s = DEFS
    if standalone: s += f'<rect width="{W}" height="{LH * 4 + 60}" fill="#fff"/>'
    for i, (n, (c, f)) in enumerate(zip(LANES, LANE_C)):
        y = 14 + i * LH
        s += f'<rect x="10" y="{y}" width="{W - 20}" height="{LH}" fill="{f}" opacity=".55" stroke="{c}"/>'
        s += f'<rect x="10" y="{y}" width="{X0 - 20}" height="{LH}" fill="{c}"/>' + txt(10 + (X0 - 20) / 2, y + LH / 2 + 5, n, "middle", "#fff", 13.5, True)
    cy = lambda lane: 14 + lane * LH + LH / 2
    B = 116; H = 50
    nodes = {1: (0, 130, ["1. Send request", "for quote"]), 2: (1, 270, ["2. Log request;", "info complete?"]),
             3: (2, 410, ["3. Review spec;", "estimate hours"]), 4: (3, 550, ["4. Check capacity", "and lead time"]),
             5: (1, 690, ["5. Send quote", "with date"]), 6: (0, 690, ["6. Accept and", "send PO"]),
             7: (1, 830, ["7. Enter order;", "confirm date"]), 8: (3, 830, ["8. Schedule", "production"])}
    for k, (lane, x, lines) in nodes.items():
        c = LANE_C[lane][0]
        if k == 2:   # decision
            mx, my = x + B / 2, cy(lane)
            s += f'<polygon points="{mx},{my - 34} {mx + 66},{my} {mx},{my + 34} {mx - 66},{my}" fill="#fff" stroke="{c}" stroke-width="1.6"/>'
            s += txt(mx, my - 3, "2. Log request;", "middle", NAVY, 11.5, True) + txt(mx, my + 12, "info complete?", "middle", NAVY, 11.5, True)
        else:
            s += box(x, cy(lane) - H / 2, B, H, lines, fill="#fff", stroke=c, fs=11.8)
    L = lambda a, b, c, d: arrow(a, b, c, d)
    s += L(130 + B / 2, cy(0) + H / 2, 270 + B / 2, cy(1) - 36)                          # 1 → 2
    s += L(270 + B / 2 + 66, cy(1), 410 + B / 2, cy(2) - H / 2 - 2)                      # 2 yes → 3
    s += txt(270 + B / 2 + 76, cy(1) - 8, "Yes", "start", GREEND, 11.5, True)
    s += f'<path d="M{270 + B / 2},{cy(1) - 34} L{270 + B / 2},{cy(0) - 18} L{130 + B + 4},{cy(0) - 18}" fill="none" stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="5 3" marker-end="url(#ah)"/>'
    s += txt(270 + B / 2 + 6, cy(0) + 6, "No: ask for missing", "start", ORANGE, 11, True) + txt(270 + B / 2 + 6, cy(0) + 20, "drawings or quantities", "start", ORANGE, 11, True)
    s += L(410 + B, cy(2), 550 + B / 2, cy(3) - H / 2 - 2)                                # 3 → 4
    s += L(550 + B / 2, cy(3) - H / 2, 690 + B / 2 - 10, cy(1) + H / 2 + 2)                # 4 → 5
    s += L(690 + B / 2, cy(1) - H / 2, 690 + B / 2, cy(0) + H / 2 + 2)                     # 5 → 6
    s += L(690 + B, cy(0), 830 + B / 2, cy(1) - H / 2 - 2)                                 # 6 → 7
    s += L(830 + B / 2, cy(1) + H / 2, 830 + B / 2, cy(3) - H / 2 - 2)                     # 7 → 8
    s += txt(W - 14, LH * 4 + 40, "Target: quote sent within 3 working days of a complete request", "end", MUTED, 12)
    if standalone:
        s += txt(14, LH * 4 + 40, "Chmltech: example swim lane map, quote to order", "start", MUTED, 12)
    return s, W, LH * 4 + 52


def fig_swim():
    s, W, H = swim_svg()
    return svg("Swim lane map of a quote-to-order process with four lanes: customer, sales, engineering and operations. 1, the "
               "customer sends a request for quote. 2, sales logs it and checks whether the information is complete; if not, sales "
               "asks the customer for missing drawings or quantities. 3, engineering reviews the specification and estimates hours. "
               "4, operations checks capacity and lead time. 5, sales sends the quote with a date. 6, the customer accepts and sends a "
               "purchase order. 7, sales enters the order and confirms the date. 8, operations schedules production. Target: quote "
               "sent within 3 working days of a complete request.", W, H, s, 640)


def doc():
    levels = [
        ("Level 1: process map", "The main steps and hand-offs, on one page", "Managers, new staff, auditors", "Swim lane map, SIPOC"),
        ("Level 2: procedure (SOP)", "Who does what, when, with which records, and the rules for exceptions", "The people who run the process", "Written procedure with a RACI"),
        ("Level 3: work instruction", "How to do one task step by step, with photos or screenshots", "The person doing the task", "Checklist, photo guide, short video"),
        ("Level 4: form or record", "The evidence that the task was done", "Supervisors, auditors, customers", "Form, ticket, system screen"),
    ]
    body = f"""
<p>Process documentation is the written record of how work gets done: who does each step, in what order, with what inputs, and what result is expected. Good documentation shortens training, keeps results consistent when people change, and gives you a baseline to improve from. Poor documentation is written once for an audit and never read again. This article, first published in 2021, has been rewritten as a practical guide with a worked example.</p>
<h2>Four levels, for four readers</h2>
<p>The most common mistake is putting everything in one long document. Split it by reader.</p>
{table(["Level", "What it covers", "Who reads it", "Typical format"], levels)}
<h2>Start with a swim lane map</h2>
<p>A swim lane map shows each role in its own horizontal lane, so the hand-offs, where most delays and errors happen, are easy to see. The example below is a quote-to-order process in a small engineering or fabrication business.</p>
{fig(fig_swim(), 1, "A swim lane map of a quote-to-order process. Each lane is a role; each arrow that crosses a lane is a hand-off.")}
<p><a href="../assets/downloads/{SWIM_PNG}" download>Download this swim lane example as a PNG image</a> to use as a model for your own map.</p>
<p>Three things stand out in the map. The decision at step 2 stops incomplete requests before engineering spends time on them. Steps 3 and 4 run in sequence; if they could run at the same time, the quote would go out faster. And the target at the bottom turns the map into something you can measure.</p>
<h2>How to document a process in six steps</h2>
<ol>
<li><strong>Pick one process and set its boundaries.</strong> Name the trigger (a request arrives) and the end (production is scheduled). A SIPOC table, listing suppliers, inputs, process, outputs and customers, helps agree the scope.</li>
<li><strong>Walk it with the people who do it.</strong> Document how the work is actually done, not how the manager thinks it is done. Watch it, or record a walk-through and transcribe it.</li>
<li><strong>Draw the map first, then write.</strong> Agree the map in one short workshop before anyone writes a procedure.</li>
<li><strong>Write the procedure in plain words.</strong> One action per step, starting with a verb. Name roles, not people. Put the rules for exceptions where they apply.</li>
<li><strong>Add a measure and an owner.</strong> Each process needs one owner who keeps it current and one or two measures, such as quote turnaround time.</li>
<li><strong>Control and review it.</strong> Give it a version number and a review date, keep it where people work, and retire old copies. <a href="../post/iso-9001-document-and-revision-control.html">Document and revision control</a> explains how.</li>
</ol>
<h2>Using AI to draft, with care</h2>
<p>AI tools can turn a recorded walk-through or a screen recording into a first draft of a procedure or work instruction in minutes. They are good at structure and plain language. They also fill gaps with plausible steps that nobody actually does. Have the people who run the process check every step, and do not put customer or confidential data into a tool your business has not approved. <a href="../post/iso-9001-and-ai-using-ai-tools-inside-a-quality-system.html">Using AI tools inside a quality system</a> covers the controls.</p>
<h2>Signs your documentation is working</h2>
<ul>
<li>New staff use it in their first week without being told to.</li>
<li>People suggest changes to it, because it matches what they do.</li>
<li>When something goes wrong, the procedure is the first thing you check and update.</li>
</ul>
""" + rel([
        ("iso-9001-document-and-revision-control", "ISO 9001 document and revision control"),
        ("iso-9001-and-ai-using-ai-tools-inside-a-quality-system", "Using AI tools inside a quality system"),
        ("how-to-increase-operational-efficiency-for-small-business", "How to increase operational efficiency for a small business"),
    ])
    return dict(slug=DOC, title="Process Documentation That People Use: Levels, Swim Lane Maps and Six Steps",
                desc="How to document a business process people will use: four levels of documentation, a swim lane example you can download, six steps, and using AI to draft.",
                cats=["operational-efficiency", "process-improvement"],
                tags=["process documentation", "swim lane", "SOP", "work instruction", "SIPOC", "RACI", "process mapping"],
                body=body.strip(), date=DATE, author="Quak Foo Lee", read="5 min read", cover_label="Process",
                related=["iso-9001-document-and-revision-control", "iso-9001-and-ai-using-ai-tools-inside-a-quality-system",
                         "how-to-increase-operational-efficiency-for-small-business"])


# ═════════════════════════ 5. 50 KPIs ═════════════════════════
# (name, what it shows, formula, example). Examples are illustrative and checked by check_kpis() below.
KPIS = {
    "Finance and accounting": [
        ("Revenue growth rate", "How fast sales are growing", "(Revenue this period − revenue last period) ÷ revenue last period", "$1.5M vs $1.2M last year: 25%"),
        ("Gross profit margin", "What is left after the direct cost of what you sold", "(Revenue − cost of goods sold) ÷ revenue", "$1.5M revenue, $1.05M COGS: 30%"),
        ("Return on investment (ROI)", "Whether a project earned more than it cost", "(Gain from the investment − cost) ÷ cost", "$100,000 spent, $150,000 extra gross profit: 50%"),
        ("Days sales outstanding (DSO)", "How long customers take to pay", "Accounts receivable ÷ credit sales × days in the period", "$100,000 owed, $240,000 credit sales in 90 days: 37.5 days"),
        ("Debt-to-equity ratio", "How much the business relies on borrowing", "Total debt ÷ shareholders' equity", "$500,000 debt, $1M equity: 0.5"),
    ],
    "People (HR)": [
        ("Employee turnover rate", "How many people leave", "Leavers in the year ÷ average headcount", "8 leavers, 80 average headcount: 10%"),
        ("Employee engagement", "How committed people are, from a regular survey", "Share of respondents who are engaged on a consistent survey", "56 of 80 engaged: 70%"),
        ("Time to hire", "How long a vacancy stays open", "Days from approval to accepted offer, averaged", "30 days"),
        ("Training hours per employee", "Investment in skills", "Total training hours ÷ headcount", "1,600 hours, 80 people: 20 hours"),
        ("Absenteeism rate", "Unplanned absence", "Days absent ÷ scheduled working days", "320 of 18,400 days: 1.7%"),
    ],
    "Production and manufacturing": [
        ("Overall equipment effectiveness (OEE)", "How much of planned time makes good product at full speed", "Availability × performance × quality", "90% × 80% × 95% = 68.4%"),
        ("First pass yield", "Product right first time, without rework", "Good units first time ÷ units started", "900 of 1,000: 90%"),
        ("Scrap rate", "Material wasted", "Scrapped material ÷ material used", "100 lb of 1,000 lb: 10%"),
        ("Unplanned downtime", "Time lost to breakdowns and shortages", "Hours stopped that were not planned", "6 hours in a 120-hour week: 5%"),
        ("Throughput", "Output rate", "Good units ÷ operating time", "100 units per hour"),
        ("Manufacturing cycle time", "Time from start to finish of one order", "Finish date − start date, averaged", "4 days"),
        ("Changeover time", "Time lost switching products", "Last good part of A to first good part of B", "45 minutes"),
        ("Capacity utilization", "How much of available capacity is used", "Actual output ÷ capacity", "800 of 1,000 units: 80%"),
        ("Work in progress (WIP)", "Unfinished work tied up on the floor", "Value or count of started, unfinished orders", "$85,000, or 12 orders"),
        ("Production cost per unit", "What one unit costs to make", "Total production cost ÷ good units", "$10,000 ÷ 1,000 = $10"),
    ],
    "Inventory": [
        ("Inventory turnover", "How many times stock is used and replaced", "Cost of goods sold ÷ average inventory at cost", "$1.2M ÷ $200,000 = 6 turns"),
        ("Days inventory outstanding (DIO)", "How long stock sits before it is sold", "Average inventory ÷ COGS × 365", "$200,000 ÷ $1.2M × 365 = 61 days"),
        ("Stock-out rate", "How often an item is not available when needed", "Order lines short ÷ order lines", "30 of 1,000 lines: 3%"),
        ("Carrying cost", "The yearly cost of holding stock", "Holding costs ÷ average inventory value", "$50,000 ÷ $200,000 = 25%"),
        ("Obsolete inventory", "Stock you can no longer sell", "Value of items with no use in 12 months ÷ total inventory value", "$10,000 ÷ $200,000 = 5%"),
    ],
    "Warehouse": [
        ("Pick accuracy", "Orders picked correctly", "Correct order lines ÷ lines picked", "980 of 1,000: 98%"),
        ("Inventory record accuracy", "Whether the system matches the shelf", "Items counted that match the record ÷ items counted", "198 of 200: 99%"),
        ("Dock-to-stock time", "Time to put received goods away", "Time from receipt to available in the system", "4 hours"),
        ("Order cycle time", "Time to fulfil an order", "Ship time − order received time", "1.5 days"),
        ("Storage utilization", "How full the warehouse is", "Locations or cubic space used ÷ available", "750 of 1,000 pallet spaces: 75%"),
    ],
    "Shipping": [
        ("On-time delivery", "Orders arriving by the promised date", "Orders on time ÷ orders delivered", "92 of 100: 92%"),
        ("Order lead time", "Time from order to delivery", "Delivery date − order date", "5 days"),
        ("Order accuracy", "Orders delivered correct and complete", "Correct orders ÷ orders delivered", "97 of 100: 97%"),
        ("Freight cost per order", "Shipping cost", "Freight cost ÷ orders shipped", "$10,000 ÷ 1,000 = $10"),
        ("Damage rate", "Goods damaged in transit", "Orders with damage claims ÷ orders shipped", "5 of 1,000: 0.5%"),
    ],
    "Supply chain and purchasing": [
        ("Perfect order rate", "Orders on time, complete, undamaged and correctly invoiced", "Perfect orders ÷ total orders", "85 of 100: 85%"),
        ("Cash-to-cash cycle time", "How long cash is tied up", "DIO + DSO − days payable outstanding", "61 + 37.5 − 45 = 53.5 days"),
        ("Supplier on-time delivery", "Supplier reliability", "Purchase order lines received on time ÷ lines received", "180 of 200: 90%"),
        ("Supplier defect rate", "Quality of what you buy", "Defective units received ÷ units received", "5 of 1,000: 0.5%"),
        ("Purchase price variance", "Paying more or less than planned", "(Actual price − standard price) × quantity", "($10.40 − $10.00) × 5,000 = $2,000 unfavourable"),
    ],
    "Customer service": [
        ("Net Promoter Score (NPS)", "Loyalty: would customers recommend you", "% promoters (9–10) − % detractors (0–6)", "60% − 15% = 45"),
        ("Customer satisfaction (CSAT)", "Satisfaction with a recent interaction", "Satisfied responses (4–5 of 5) ÷ responses", "180 of 200: 90%"),
        ("Customer retention rate", "Customers who stay", "(Customers at end − new customers) ÷ customers at start", "(110 − 20) ÷ 100 = 90%"),
        ("First contact resolution", "Issues solved without a follow-up", "Resolved on first contact ÷ total contacts", "70 of 100: 70%"),
        ("Average response time", "How long customers wait for a first reply", "Total time to first reply ÷ tickets", "3 working hours"),
    ],
    "Product development": [
        ("Time to market", "Speed from idea to launch", "Launch date − project approval date", "6 months"),
        ("Projects on schedule", "Delivery against plan", "Projects hitting the planned gate date ÷ projects", "7 of 10: 70%"),
        ("Development cost vs budget", "Spending control", "Actual cost ÷ budget", "$540,000 ÷ $500,000 = 108%"),
        ("New product revenue share", "How much revenue comes from recent products", "Revenue from products launched in the last 3 years ÷ total revenue", "$300,000 ÷ $1.5M = 20%"),
        ("Early warranty claims", "Quality of new products in the field", "Units with a claim in the first 12 months ÷ units sold", "12 of 1,000: 1.2%"),
    ],
}


def check_kpis():
    n = sum(len(v) for v in KPIS.values())
    names = [k[0] for v in KPIS.values() for k in v]
    assert n == 50 and len(set(names)) == 50, (n, len(set(names)))
    assert abs(0.9 * 0.8 * 0.95 - 0.684) < 1e-9
    assert abs(100_000 / 240_000 * 90 - 37.5) < 1e-9
    assert round(200_000 / 1_200_000 * 365) == 61
    assert 61 + 37.5 - 45 == 53.5
    assert (1.5 - 1.2) / 1.2 == 0.25 or abs((1.5 - 1.2) / 1.2 - 0.25) < 1e-9
    assert abs(320 / 18_400 - 0.0174) < 0.001
    return n


def fig_cascade():
    s = DEFS
    s += box(236, 12, 270, 50, ["Company goal: 95% on-time", "delivery by year end"], fill=NAVY, stroke=NAVY, tc="#fff", fs=13)
    depts = [("Production", "Schedule adherence ≥ 95%", BLUE, PALE), ("Warehouse", "Pick accuracy ≥ 99%", GREEND, GREENF),
             ("Purchasing", "Supplier on-time ≥ 92%", PURPLE, "#E7E7F8")]
    people = [["Planner: schedule", "frozen 2 days ahead"], ["Picker: accuracy", "and picks per hour"], ["Buyer: late POs", "chased every day"]]
    for i, (d, k, c, f) in enumerate(depts):
        x = 14 + i * 244
        s += arrow(371, 64, x + 108, 96, c)
        s += f'<rect x="{x}" y="98" width="216" height="52" rx="8" fill="{f}" stroke="{c}"/>'
        s += txt(x + 108, 120, d, "middle", NAVY, 13, True) + txt(x + 108, 139, k, "middle", NAVY, 12)
        s += arrow(x + 108, 152, x + 108, 176, c)
        s += box(x + 18, 178, 180, 46, people[i], fill="#fff", stroke=c, fs=12, bold=False)
    s += txt(14, 248, "Company KPI  ›  department KPIs that drive it  ›  what each person controls day to day", "start", MUTED, 12)
    return svg("A KPI cascade. The company goal is 95% on-time delivery by year end. It drives three department KPIs: production "
               "schedule adherence of at least 95%, warehouse pick accuracy of at least 99%, and purchasing supplier on-time delivery "
               "of at least 92%. Each department KPI drives what one person controls: the planner freezes the schedule two days ahead, "
               "the picker tracks accuracy and picks per hour, and the buyer chases late purchase orders every day.", 742, 258, s, 600)


def kpi():
    sections = ""
    for sec, rows in KPIS.items():
        sid = re.sub(r"[^a-z]+", "-", sec.lower()).strip("-")
        sections += f'<h2 id="{sid}" data-toc-label="{sec} ({len(rows)})">{sec}</h2>\n' + table(["KPI", "What it shows", "Formula", "Example"], [list(r) for r in rows]) + "\n"
    types = [
        ("Leading", "Predicts a result before it happens", "Late purchase orders this week"),
        ("Lagging", "Reports a result after it happened", "On-time delivery last month"),
        ("Input", "Resources put in", "Training hours"),
        ("Process", "How well the work runs", "Changeover time"),
        ("Output", "What the work produced", "Good units per hour"),
        ("Outcome", "The effect on the customer or the business", "Customer retention"),
        ("Quantitative and qualitative", "A count or ratio, or a rating from feedback", "Scrap rate; customer comments coded by theme"),
        ("Financial and non-financial", "Measured in money, or in time, quality or people", "Gross margin; first pass yield"),
    ]
    body = f"""
<p>A key performance indicator (KPI) is a measure that shows whether you are making progress toward a specific business goal. This list of 50 was first published in 2023. It has been revised: formulas are now given for every KPI, several worked examples have been corrected (return on investment was calculated on revenue instead of gain, and Net Promoter Score was described as a percentage of customers), and duplicates have been removed. Two shorter articles on types of KPIs and on KPIs for individual team members have also been folded into this one.</p>
<h2 id="types">Types of KPIs</h2>
<p>Most KPI types come in pairs. The useful habit is to pair a lagging KPI, which tells you whether you got there, with one or two leading KPIs, which tell you early enough to act.</p>
{table(["Type", "What it means", "Example"], types)}
{sections}
<p class="note"><em>Examples are illustrative. Benchmarks vary widely by industry and size, so compare yourself with your own trend first.</em></p>
<h2 id="cascade">KPIs for each team member</h2>
<p>A company KPI only moves when the people who do the work can see how their part affects it. Cascade each company goal into the department KPIs that drive it, and then into one or two measures each person controls day to day.</p>
{fig(fig_cascade(), 1, "Cascading one company KPI to departments and then to individuals.")}
<p>Three rules keep individual KPIs fair and useful. Measure what the person controls, not results that depend on other teams. Keep it to two or three measures, so people know what matters. And use them for coaching and problem-solving first; tying pay to a single number invites people to game it.</p>
<h2>How to pick your KPIs</h2>
<ol>
<li>Start from three to five business goals, not from this list.</li>
<li>For each goal, choose one lagging and one or two leading KPIs.</li>
<li>Write a one-line definition with the formula, data source, owner and review frequency, so the number means the same thing every month.</li>
<li>Show the trend, not just this month's figure, on a simple dashboard.</li>
<li>Drop any KPI nobody has acted on in six months.</li>
</ol>
""" + rel([
        ("what-oee-really-measures", "What OEE really measures: where your production hours go"),
        ("boost-performance-with-effective-dashboard-strategies-for-entrepreneurs", "Dashboard strategies for entrepreneurs"),
        ("how-to-increase-operational-efficiency-for-small-business", "How to increase operational efficiency for a small business"),
    ])
    return dict(slug=KPI, title="50 KPIs for Business Success: Formulas and Examples from Finance to Product Development",
                desc="Fifty KPIs across nine functions, each with a formula and worked example, plus the types of KPIs and how to cascade them to each team member.",
                cats=["operational-efficiency", "lean", "six-sigma"],
                tags=["KPIs", "key performance indicators", "OEE", "DSO", "inventory turnover", "NPS", "leading and lagging indicators", "KPI cascade"],
                body=body.strip(), date=DATE, author="Quak Foo Lee", read="9 min read", cover_label="KPIs",
                related=["what-oee-really-measures", "boost-performance-with-effective-dashboard-strategies-for-entrepreneurs",
                         "how-to-increase-operational-efficiency-for-small-business"])


if __name__ == "__main__":
    check_kpis()
    for a in (inv(), seo(), cyb(), doc(), kpi()):
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"][:50], len(re.sub(r"<svg.*?</svg>|<[^>]+>", " ", a["body"], flags=re.S).split()), "words")
    s, W, H = swim_svg(True)
    open("/tmp/swim.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W * 2}" height="{H * 2}" '
                                     f'font-family="Inter,system-ui,sans-serif" font-size="13">{s}</svg>')
    print(f"INV: save {SAVE_YR:,.0f}/yr, sub {SUB_YR:,}, net {NET_YR:,.0f}, one-time {ONE_INV:,}, payback {PAYBACK_INV:.1f} months")
