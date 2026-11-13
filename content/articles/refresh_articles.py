"""Rewritten older Insights articles (V4.66), kept at their original addresses.

1. post/boost-your-business-with-cdap-funding-support-for-digital-adoption
   was a 2023 notice about CDAP grants. CDAP has closed, so it is now a guide to the funding that replaced it.
2. post/the-key-differences-between-seo-and-geo-for-enhancing-your-online-presence
   is merged with the near-duplicate "Understanding the differences between SEO and GEO strategies"
   (which used GEO to mean local search) and rewritten with current Google guidance and the GEO research.
   The duplicate becomes a redirect: python3 content/gen/refresh_article.py --retire <old> <new>.

Usage:  python3 content/articles/refresh_articles.py
        python3 content/gen/refresh_article.py <slug>      (for each article)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import (nowrap, svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE,
                           MUTED, LINE, SAND, PALE, GREENF, ORANGEF)

CDAP = "boost-your-business-with-cdap-funding-support-for-digital-adoption"
SEO = "the-key-differences-between-seo-and-geo-for-enhancing-your-online-presence"
SEO_OLD = "understanding-the-differences-between-seo-and-geo-strategies-for-online-success"
LIFT = "bdc-lift-program"
DATE = "2026-11-13"


def src(items):
    return "<h2>Sources</h2><ul>" + "".join(
        f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in items) + "</ul>"


def rel(items):
    return "<h2>Related reading</h2><ul>" + "".join(f'<li><a href="../post/{s}.html">{t}</a></li>' for s, t in items) + "</ul>"


# ───────────────────────── 1. After CDAP ─────────────────────────
def fig_route():
    s = DEFS
    s += box(220, 14, 300, 46, "What will the money pay for?", fill=NAVY, stroke=NAVY, tc="#fff", fs=14.5)
    s += f'<path d="M370 60 V78 M95 78 H645 M95 78 V92 M278 78 V92 M462 78 V92 M645 78 V92" stroke="{MUTED}" stroke-width="1.4" fill="none"/>'
    cols = [
        (95, BLUE, PALE, ["A plan", "before you buy"], ["Ontario DMAP: $15,000", "Quebec ESSOR 1B: $20,000", "BDC Advisory (paid)"]),
        (278, GREEND, GREENF, ["Buying and", "implementing tech"], ["BDC LIFT loan", "$25K to $5M", "Regional AI Initiative", "$125K+, repayable"]),
        (462, PURPLE, "#E7E7F8", ["Developing new", "technology"], ["NRC IRAP funding", "SR&amp;ED tax credits", "35% on up to $6M"]),
        (645, ORANGE, ORANGEF, ["A joint AI project", "with partners"], ["Scale AI: up to 40%", "of project costs", "Innovation Clusters"]),
    ]
    for x, col, fill, head, lines in cols:
        s += box(x - 85, 92, 170, 52, head, fill=fill, stroke=col, fs=13.5)
        s += f'<line x1="{x}" y1="144" x2="{x}" y2="160" stroke="{col}" stroke-width="1.4"/>'
        s += f'<rect x="{x - 85}" y="160" width="170" height="{22 + 19 * len(lines)}" rx="8" fill="#fff" stroke="{col}" stroke-width="1.2"/>'
        for i, ln in enumerate(lines):
            s += txt(x, 184 + 19 * i, ln, "middle", NAVY if (len(lines) == 3 or i % 2 == 0) else MUTED, 12.5, len(lines) == 4 and i % 2 == 0)
    s += f'<rect x="10" y="266" width="720" height="40" rx="8" fill="{SAND}" stroke="#C9C2B2"/>'
    s += txt(370, 291, "Every path: apply before you spend, keep a baseline, and check the stacking limits", "middle", NAVY, 13.5, True)
    return svg("Decision diagram. One question, what will the money pay for, leads to four paths. A plan before you buy: Ontario DMAP up to "
               "15,000 dollars, Quebec ESSOR component 1B up to 20,000 dollars, or paid BDC Advisory Services. Buying and implementing "
               "technology: a BDC LIFT loan of 25,000 dollars to 5 million dollars, or a repayable Regional AI Initiative contribution for "
               "projects of 125,000 dollars and up. Developing new technology: NRC IRAP advice and funding and SR&ED tax credits of 35 percent "
               "on up to 6 million dollars. A joint AI project with partners: Scale AI co-investment of up to 40 percent of costs, or the Global "
               "Innovation Clusters. Every path: apply before you spend, keep a baseline and check the stacking limits.", 740, 316, s, 640, x0=0)


def cdap():
    body = f"""<blockquote style="font-size:16.5px"><strong>Updated November 2026.</strong> This article first appeared in April 2023, when CDAP grants were open. CDAP has since closed, so it now explains what replaced it. If a website still offers you a $15,000 CDAP grant, that offer is out of date.</blockquote>
<p>For three years the Canada Digital Adoption Program (CDAP) was the easy answer to "who pays for our digital plan?" Its Boost Your Business Technology grant covered most of the cost of a digital adoption plan, up to $15,000, and opened the door to an interest-free BDC loan of up to $100,000 to carry the plan out. Chmltech wrote more than 300 of those plans for Canadian businesses.</p>
<p>The program ended sooner than planned. Boost Your Business Technology was fully subscribed and stopped taking new applications on 19 February 2024. The smaller Grow Your Business Online grant closed as well, and the government scheduled the program to end on 31 March 2025.</p>
<p>No single program took its place. The money for digital adoption and AI is now spread across loans with advice attached, regional repayable contributions, R&amp;D supports and a few provincial plan grants. This article sorts them by what you want to pay for, so you can find your starting point in a few minutes.</p>
<h2>Why the landscape looks different now</h2>
<p>Two things changed. First, the federal government moved its support for adoption toward larger, repayable instruments. CDAP was a small grant for many firms. Its successors are mostly loans and interest-free contributions for fewer, bigger projects.</p>
<p>Second, AI became the headline. On 4 June 2026 the government released its national AI strategy, <em>AI for All</em>. It aims to raise the share of Canadian businesses using AI from about 12 percent in 2025 to 60 percent by 2034, and it names small and mid-sized firms as a priority. The strategy is a policy package rather than a grant program. In practice, the money reaches businesses through the programs below.</p>
<h2>The main options in 2026</h2>
<table>
<tr><th>Program</th><th>What you get</th><th>Best fit</th><th>Type</th></tr>
<tr><td><a href="{LIFT}.html">BDC LIFT</a></td><td>Consulting plus a loan of $25,000 to $2 million (digital and AI) or $350,000 to $5 million (equipment)</td><td>Firms with $1 million or more in revenue buying AI, software or digitally enabled equipment</td><td>Loan</td></tr>
<tr><td>Regional Artificial Intelligence Initiative (RAII)</td><td>Up to 50% of eligible costs, interest-free and repayable. In B.C., $200,000 to $5 million per project</td><td>Established firms adopting AI, or Canadian firms taking an AI product to market</td><td>Repayable contribution</td></tr>
<tr><td>NRC IRAP</td><td>Advice from an Industrial Technology Advisor, then project funding</td><td>Firms with up to 500 employees developing a new product, service or process</td><td>Contribution</td></tr>
<tr><td>SR&amp;ED</td><td>35% refundable tax credit on up to $6 million a year of qualifying R&amp;D for eligible Canadian-controlled private corporations</td><td>Any firm solving a technical problem it cannot solve with standard practice, including custom software</td><td>Tax credit</td></tr>
<tr><td>Scale AI</td><td>Up to 40% of eligible project costs, non-repayable</td><td>AI projects in supply chains and operations run by two or more partners, with at least one SME</td><td>Co-investment</td></tr>
<tr><td>Ontario DMAP</td><td>Up to $15,000 for a digital adoption plan with a registered consultant</td><td>Ontario firms with 1 to 499 employees</td><td>Grant</td></tr>
<tr><td>Quebec ESSOR, component 1</td><td>Up to 50% of the cost of a digital diagnostic or plan (up to $20,000) and of carrying it out (up to $50,000)</td><td>Quebec firms with 250 or fewer employees and at least $2.5 million in revenue</td><td>Grant</td></tr>
<tr><td>Mitacs Business Strategy Internship</td><td>A student or recent graduate on a digital or strategy project. Mitacs adds an award to the company's $5,000 share</td><td>Firms that need hands to carry out a plan</td><td>Wage support</td></tr>
</table>
<p>Amounts are taken from the program pages as checked on 11 November 2026, and they change. The <a href="../funding.html">Chmltech funding finder</a> lists more than 400 federal, provincial and territorial programs with their current status. Filter it by your province and purpose before you rely on any figure here.</p>
{fig(fig_route(), 1, "Where to start, by what the money will pay for. Amounts are the published ranges as of November 2026.")}
<h2>If you need a plan first</h2>
<p>This is the gap CDAP left. Outside Ontario and Quebec, no open program pays most of the cost of a general digital plan for a small business. Three routes remain:</p>
<ul>
<li><strong>A provincial plan grant</strong>, if you are in Ontario (DMAP) or Quebec (ESSOR component 1B).</li>
<li><strong>A plan built into a loan.</strong> LIFT's digital and AI path requires a BDC Advisory Services Digital Plan before the loan, and BDC can finance the cost of the consulting.</li>
<li><strong>Paying for the plan yourself</strong> and treating it as the first, cheapest phase of the project. A good plan usually pays for itself by stopping a poor purchase.</li>
</ul>
<h2>If you are ready to buy and implement</h2>
<p>For most small and mid-sized firms the choice is between LIFT and RAII. They are built differently:</p>
<table>
<tr><th></th><th>BDC LIFT</th><th>RAII</th></tr>
<tr><td>Delivered by</td><td>BDC</td><td>Your regional development agency, such as PacifiCan in B.C. or FedDev Ontario</td></tr>
<tr><td>Form</td><td>Loan at a preferential rate</td><td>Interest-free repayable contribution, normally with no collateral</td></tr>
<tr><td>Share of cost</td><td>Financing for the investment, including integration</td><td>Up to 50% of eligible costs. You fund the rest from non-government sources</td></tr>
<tr><td>Smallest project</td><td>$25,000</td><td>$125,000 to $250,000, depending on the region</td></tr>
<tr><td>Plan required</td><td>Yes: a BDC Digital Plan or a productivity plan</td><td>A project plan with costs and outcomes, judged by the agency</td></tr>
<tr><td>Watch for</td><td>Canadian supplier and integrator rules</td><td>Off-the-shelf AI software without significant customization is not eligible in B.C.</td></tr>
</table>
<p>RAII repayment typically starts a year after the project ends and runs over five years. Read the terms for your region: the minimum project size, the employee range and the years in operation all differ between agencies.</p>
<h2>If you are developing something new</h2>
<p>If your project involves real technical uncertainty, such as a new process, a custom model or software that does something standard tools cannot, look at NRC IRAP and SR&amp;ED together. IRAP starts with a conversation with an advisor and can fund part of the project. SR&amp;ED returns part of the qualifying spending as a tax credit after the year ends. Since April 2026 the CRA also offers an elective pre-claim approval, so a business can get the technical eligibility of a project confirmed before it spends the money.</p>
<h2>Five lessons CDAP taught that still apply</h2>
<ol>
<li><strong>Apply before you spend.</strong> Almost every program reimburses costs incurred after approval, not before. A signed purchase order can disqualify the item.</li>
<li><strong>Plan, then buy.</strong> The plan was the most valuable part of CDAP. LIFT and RAII both expect one. Expect to show the process today, the process after, and what changes in hours, errors or revenue.</li>
<li><strong>Measure a baseline.</strong> Cycle time, order errors, labour hours, downtime. Without a "before" number you cannot show a benefit, and repayable funding needs a benefit.</li>
<li><strong>Check the stacking limits.</strong> Most programs cap total government help on a project, often at 50 to 75 percent of costs. Two approvals can still be cut back if together they exceed the cap.</li>
<li><strong>Budget for repayment.</strong> Many of today's programs are loans or repayable contributions. Treat the low or zero interest as a saving on a project worth doing anyway.</li>
</ol>
<h2>Key points</h2>
<ul>
<li>CDAP's Boost Your Business Technology grant closed on 19 February 2024, and the program was scheduled to end on 31 March 2025. It is not coming back in its old form.</li>
<li>Funding for digital adoption and AI now comes mainly through LIFT, the regional AI initiatives, IRAP, SR&amp;ED, Scale AI and a few provincial programs.</li>
<li>Most of the money is repayable, and the projects are larger than CDAP's.</li>
<li>Start from what the money will pay for: a plan, a purchase, development work or a joint project.</li>
</ul>
<p><strong>Not sure which path fits?</strong> Chmltech has written more than 300 digital adoption plans for Canadian businesses. We can map your processes, set the baseline and build the business case a lender or agency expects. <a href="../book.html">Book a strategy call</a> or search the <a href="../funding.html">funding finder</a>.</p>
<p style="font-size:15px"><em>This article is general information, not financial or tax advice. Chmltech Ltd. does not speak for BDC, ISED, the regional development agencies or the CRA, which set the terms of their programs and decide eligibility. Program details are as published in November 2026 and may change.</em></p>
{src([("ISED: Canada Digital Adoption Program (status)", "https://ic.gc.ca/eic/site/152.nsf/eng/00002.html"),
      ("BDC: Canada Digital Adoption Program notice, February 19, 2024", "https://www.bdc.ca/en/canada-digital-adoption-program"),
      ("Blakes: Canada's AI for All strategy, key takeaways for businesses", "https://www.blakes.com/insights/canada-s-ai-for-all-strategy-key-takeaways-for-businesses/"),
      ("Osler: What Canada's ambitious AI strategy means for business", "https://www.osler.com/en/insights/updates/what-canadas-ambitious-ai-strategy-means-for-business/"),
      ("BDC: LIFT", "https://www.bdc.ca/en/solutions/lift"),
      ("PacifiCan: Regional Artificial Intelligence Initiative, funding overview", "https://www.canada.ca/en/pacific-economic-development/services/funding/regional-artificial-intelligence-initiative/raii-funding-overview.html"),
      ("FedDev Ontario: Regional Artificial Intelligence Initiative", "https://feddev-ontario.canada.ca/en/funding-southern-ontario/regional-artificial-intelligence-initiative-southern-ontario"),
      ("NRC IRAP: Financial support for technology innovation", "https://nrc.canada.ca/en/support-technology-innovation/financial-support-technology-innovation"),
      ("CRA: SR&amp;ED investment tax credit policy", "https://www.canada.ca/en/revenue-agency/services/scientific-research-experimental-development-tax-incentive-program/investment-tax-credit-policy.html"),
      ("Scale AI: Projects", "https://scaleai.ca/projects"),
      ("Ontario Centre of Innovation: Digital Competence Centre", "https://www.oc-innovation.ca/programs/digital-competence-centre/"),
      ("Investissement Québec: ESSOR", "https://www.investquebec.com/fr/financement/programmes-gouvernementaux/essor/appui-la-concretisation-de-projets-dinvestissement"),
      ("Mitacs: Business Strategy Internship", "https://www.mitacs.ca/our-programs/business-strategy-internship/")])}
{rel([(LIFT, "BDC's LIFT program: who qualifies and how to prepare"),
      ("ai-readiness-preparing-your-organization-for-successful-ai-adoption", "AI readiness: preparing your organization for successful AI adoption"),
      ("agent-readiness-for-small-and-mid-sized-firms-data-process-staged-adoption", "Agent readiness for small and mid-sized firms")])}"""
    body = nowrap(body, [(1, 3, 22), (2, 0, 16)])
    return dict(slug=CDAP, title="After CDAP: Where Canadian Businesses Find Digital and AI Funding in 2026",
                desc="CDAP closed to new applicants in 2024. Where digital and AI funding comes from now: LIFT, regional AI loans, IRAP, SR&ED, Scale AI and provincial plans.",
                cats=["digital-technology", "artificial-intelligence"],
                tags=["CDAP", "digital adoption funding", "AI funding Canada", "BDC LIFT", "RAII", "NRC IRAP", "SR&ED", "small business grants"],
                body=body, date=DATE, author="Quak Foo Lee", read="8 min read", cover_label="Funding",
                related=[LIFT, "ai-readiness-preparing-your-organization-for-successful-ai-adoption",
                         "agent-readiness-for-small-and-mid-sized-firms-data-process-staged-adoption"])


# ───────────────────────── 2. SEO vs GEO ─────────────────────────
def fig_paths():
    s = DEFS
    s += box(10, 70, 140, 56, ["Your page"], fill=NAVY, stroke=NAVY, tc="#fff", fs=15)
    s += box(200, 70, 150, 56, ["Crawled and", "indexed"], fs=13.5)
    s += arrow(150, 98, 198, 98)
    s += f'<path d="M350 98 H390 M390 38 V158" stroke="{NAVY}" stroke-width="1.6" fill="none"/>'
    s += arrow(390, 38, 438, 38) + arrow(390, 158, 438, 158)
    s += box(440, 12, 290, 52, ["SEO: ranked in a list of links"], fill=PALE, stroke=BLUE, fs=13.5)
    s += txt(585, 82, "Won by relevance, authority and page experience", "middle", MUTED, 12)
    s += box(440, 132, 290, 52, ["GEO: quoted inside an AI answer"], fill=GREENF, stroke=GREEND, fs=13.5)
    s += txt(585, 202, "Won by clear claims, evidence and citable facts", "middle", MUTED, 12)
    s += f'<rect x="10" y="222" width="720" height="40" rx="8" fill="{SAND}" stroke="#C9C2B2"/>'
    s += txt(370, 247, "Same foundation: a page that cannot be crawled and indexed can be neither ranked nor cited", "middle", NAVY, 13.5, True)
    return svg("A page is crawled and indexed, then takes one of two paths. SEO: ranked in a list of links, won by relevance, authority and page "
               "experience. GEO: quoted inside an AI answer, won by clear claims, evidence and citable facts. Both rest on the same foundation: "
               "a page that cannot be crawled and indexed can be neither ranked nor cited.", 740, 272, s, 600, x0=0)


def seo():
    body = f"""<blockquote style="font-size:16.5px"><strong>Updated November 2026.</strong> This article replaces two earlier posts on SEO and GEO, one of which used "GEO" to mean local search. It reflects Google's 2026 guidance on AI search and the research that named the field. For local search, see <a href="maximize-your-visibility-with-these-local-seo-tips-for-small-businesses.html">our local SEO tips</a>.</blockquote>
<p>A buyer looking for a supplier used to type a few words into Google and scan ten blue links. Many now ask a full question and read an answer written by an AI: Google's AI Overviews and AI Mode, ChatGPT, Perplexity or Copilot. The answer names a few sources. Being one of them is the new prize.</p>
<p>Search engine optimization (SEO) is the work of ranking in the list of links. Generative engine optimization (GEO) is the work of being quoted in the AI answer. This article explains how the two differ, what the evidence says works, and a short checklist a small business can follow without hiring an agency.</p>
<h2>Two ways to be found</h2>
<p>A search engine retrieves pages and ranks them. The reader chooses where to click. A generative engine retrieves pages too, then reads them, combines them and writes one answer, with its sources cited inside the text. The reader may never click at all.</p>
{fig(fig_paths(), 1, "SEO and GEO share a foundation. They differ in what wins at the last step.")}
<table>
<tr><th></th><th>SEO</th><th>GEO</th></tr>
<tr><td>Goal</td><td>Rank high in the list of results</td><td>Be cited, or quoted, in the generated answer</td></tr>
<tr><td>Where it shows</td><td>Google and Bing results pages</td><td>AI Overviews, AI Mode, ChatGPT search, Perplexity, Copilot</td></tr>
<tr><td>Unit of success</td><td>Position, clicks, click-through rate</td><td>Citations, and how much of the answer draws on you</td></tr>
<tr><td>What helps most</td><td>Relevance, links from trusted sites, speed and mobile experience</td><td>Clear statements, evidence, statistics and quoted sources</td></tr>
<tr><td>How you measure it</td><td>Search Console, analytics</td><td>Search Console (Google's AI features are counted in search traffic), plus checking AI answers by hand</td></tr>
</table>
<h2>Where the term GEO comes from</h2>
<p>The name comes from a 2024 research paper by Aggarwal and colleagues at Princeton, IIT Delhi and other institutions, presented at the KDD data mining conference. The authors built a benchmark of about 10,000 queries and tested how changes to a page affected how visible it was in generated answers.</p>
<p>Their main finding: adding citations to sources, quotations from relevant experts and statistics raised a page's visibility in AI answers by up to 40 percent. Writing more fluently and plainly also helped. Keyword stuffing, the oldest SEO trick, did little or nothing. The effects varied by subject, so treat 40 percent as a best case from an experiment, not a promise.</p>
<h2>What Google says</h2>
<p>Google has been direct about its own AI features. Its Search Central documentation says that SEO best practices still apply to AI Overviews and AI Mode, and that there are no additional requirements or special optimizations needed to appear in them. To be shown as a supporting link, a page must be indexed and eligible to be shown in Google Search with a snippet. In May 2026 Google published a longer guide, "Optimizing your website for generative AI features on Google Search," which repeats the point: write helpful, people-first content and keep the site technically sound.</p>
<p>That settles the question for Google. Other AI engines, such as ChatGPT and Perplexity, use their own crawlers and may weigh signals differently. The practical answer is the same: a page that is easy to crawl, clearly written and backed by evidence does well in both.</p>
<h2>A GEO checklist for a small business</h2>
<ol>
<li><strong>Make sure you can be crawled.</strong> Check robots.txt, your firewall and your hosting settings. Some security tools block AI search crawlers such as OAI-SearchBot (ChatGPT search) and PerplexityBot by default. Decide deliberately whether to allow them.</li>
<li><strong>Answer one question per page, early.</strong> Put the direct answer in the first two sentences, then the detail. AI engines lift short, self-contained statements.</li>
<li><strong>Back claims with evidence.</strong> Name your sources and link to them. Use numbers from your own work where you have them: "we cut order errors from 4 percent to 1 percent" is more citable than "we improve accuracy."</li>
<li><strong>Use plain headings and tables.</strong> Clear structure helps readers and machines find the part they need. Do not bend the writing around AI. Google advises against it.</li>
<li><strong>Show who wrote it and when.</strong> An author name, a date and a short bio make a page easier to trust and to cite.</li>
<li><strong>Keep your facts consistent everywhere.</strong> Your name, address, services and prices should match on your site, your Google Business Profile, LinkedIn and directories. AI answers draw on all of them.</li>
<li><strong>Publish what only you know.</strong> Worked examples, original data, real costs and lessons from projects. A rewrite of what is already online gives an AI no reason to cite you.</li>
<li><strong>Check the answers yourself.</strong> Once a month, ask your customers' top five questions in Google AI Mode, ChatGPT and Perplexity. Note who is cited. Keep the log, because the answers change.</li>
</ol>
<h2>What not to spend money on</h2>
<ul>
<li><strong>"AI-only" rewrites of pages that already rank.</strong> Google says no special optimization is needed for its AI features.</li>
<li><strong>Separate pages for every variant of a question.</strong> Thin, repetitive pages help neither SEO nor GEO.</li>
<li><strong>Guaranteed AI citations.</strong> No one controls which sources an AI engine picks. Treat any guarantee as a warning sign.</li>
</ul>
<p>An <code>llms.txt</code> file, a plain list of your key pages for AI tools, is cheap to add and does no harm. Google says it does not need one, so do not expect it to change much on its own.</p>
<h2>Key points</h2>
<ul>
<li>SEO wins a place in the list of links. GEO wins a place inside the AI answer.</li>
<li>Both start from the same foundation: pages that can be crawled, indexed and understood.</li>
<li>Research found that citations, quotations and statistics raised visibility in AI answers by up to 40 percent. Keyword stuffing did not help.</li>
<li>Google says its AI features need no special optimization beyond good SEO.</li>
<li>For a small business, the best GEO is specific, evidence-backed writing about what you actually know.</li>
</ul>
<p><strong>Want a second opinion on your site?</strong> Chmltech reviews websites for small businesses: what search engines and AI answers can find, what they cannot, and what to fix first. <a href="../book.html">Book a strategy call</a>.</p>
{src([("Google Search Central: AI features and your website", "https://developers.google.com/search/docs/appearance/ai-features"),
      ("Search Engine Journal: Google's new AI search guide calls AEO and GEO still SEO", "https://searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026"),
      ("Aggarwal et al. (2024), GEO: Generative Engine Optimization, KDD '24", "https://arxiv.org/abs/2311.09735")])}
{rel([("what-is-technical-seo-basics-and-10-best-practices", "What is technical SEO? Basics and 10 best practices"),
      ("maximize-your-visibility-with-these-local-seo-tips-for-small-businesses", "Local SEO tips for small businesses"),
      ("boost-your-search-rankings-with-ai-powered-seo-strategies", "Boost your search rankings with AI-powered SEO strategies")])}"""
    body = nowrap(body, [(1, 0, 16)])
    return dict(slug=SEO, title="SEO vs GEO: How to Be Found in Google and in AI Answers",
                desc="SEO ranks you in the list of links; GEO gets you quoted in AI answers. What Google says, what the research found, and a checklist for small businesses.",
                cats=["marketing", "artificial-intelligence"],
                tags=["SEO", "GEO", "generative engine optimization", "AI Overviews", "AI search", "ChatGPT search", "small business marketing"],
                body=body, date=DATE, author="Quak Foo Lee", read="7 min read", cover_label="Search",
                related=["what-is-technical-seo-basics-and-10-best-practices",
                         "maximize-your-visibility-with-these-local-seo-tips-for-small-businesses",
                         "boost-your-search-rankings-with-ai-powered-seo-strategies"])


if __name__ == "__main__":
    for a in (cdap(), seo()):
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("wrote", a["slug"], len(a["desc"]), "chars desc")
