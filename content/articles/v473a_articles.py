"""V4.73 (first half): four older articles rewritten at their original addresses, and three posts retired.

1. post/esg-frameworks-and-standards               rewritten: ESG reporting frameworks in 2026 for Canadian SMEs
     retired into it: esg-2022-the-transformation-of-the-c-suite-and-boardroom (dated, thin)
                      what-is-esg-investing (closely followed a syndicated personal-finance article; off-topic)
2. post/the-ultimate-guide-to-choosing-the-right-erp-for-your-business   rewritten: choosing and implementing ERP
     retired into it: navigating-the-challenges-of-erp-implementation-common-pitfalls-and-how-to-avoid-them
3. post/10-best-erp-systems-for-small-and-medium-sized-enterprises        refreshed: 10 ERP systems grouped by company size, 2026
     (Infor CloudSuite Industrial and Sage Intacct replaced by MRPeasy and ERPNext after an SME-fit check)
4. post/how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide   rewritten for GA4

Usage:  python3 content/articles/v473a_articles.py
        python3 content/gen/refresh_article.py <slug>                 (each of the four)
        python3 content/gen/refresh_article.py --retire <old> <new>   (each retired post)
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, MUTED, LINE, SAND, PALE, GREENF, ORANGEF

DATE = "2026-11-13"
ESG = "esg-frameworks-and-standards"
ESG_RETIRE = ["esg-2022-the-transformation-of-the-c-suite-and-boardroom", "what-is-esg-investing"]
ERP = "the-ultimate-guide-to-choosing-the-right-erp-for-your-business"
ERP_RETIRE = ["navigating-the-challenges-of-erp-implementation-common-pitfalls-and-how-to-avoid-them"]
TOP = "10-best-erp-systems-for-small-and-medium-sized-enterprises"
GA = "how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide"


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


# ═════════════════════════ 1. ESG ═════════════════════════
def fig_esg_asks():
    s = DEFS
    askers = [("A large customer", "supplier questionnaire", BLUE, PALE),
              ("A lender or investor", "loan or due diligence", GREEND, GREENF),
              ("An EU customer", "CSRD value chain request", PURPLE, "#E7E7F8"),
              ("Your own marketing", "green or net-zero claims", ORANGE, ORANGEF)]
    behind = ["ISSB / CSSB, GHG Protocol,", "CDP or EcoVadis formats", "CSDS 2 climate topics,", "OSFI B-15 for banks",
              "VSME standard caps what", "they can ask of you", "Competition Act: claims", "must be substantiated"]
    for i, (who, what, c, f) in enumerate(askers):
        x = 14 + i * 182
        s += f'<rect x="{x}" y="14" width="168" height="62" rx="10" fill="{f}" stroke="{c}" stroke-width="1.4"/>'
        s += txt(x + 84, 40, who, "middle", NAVY, 13.5, True) + txt(x + 84, 60, what, "middle", NAVY, 12)
        s += arrow(x + 84, 78, x + 84, 104, c)
        s += f'<rect x="{x}" y="106" width="168" height="60" rx="8" fill="#fff" stroke="{c}"/>'
        s += txt(x + 84, 131, behind[2 * i], "middle", NAVY, 11.8) + txt(x + 84, 149, behind[2 * i + 1], "middle", NAVY, 11.8)
    s += f'<rect x="14" y="186" width="714" height="44" rx="10" fill="{SAND}" stroke="#C9C2B2"/>'
    s += txt(371, 213, "One core data set answers most of them: energy and emissions, people, safety, governance, policies", "middle", NAVY, 13, True)
    return svg("Four sources of ESG requests to a small business and the framework behind each. A large customer sends a supplier "
               "questionnaire, usually based on the ISSB or CSSB standards, the GHG Protocol, CDP or EcoVadis. A lender or investor asks "
               "during a loan or due diligence, often using CSDS 2 climate topics; banks follow OSFI Guideline B-15. An EU customer sends "
               "a CSRD value chain request, limited for firms under 1,000 employees to the VSME standard. Your own marketing makes green "
               "or net-zero claims, which the Competition Act requires to be adequately and properly substantiated. One core data set "
               "answers most of them: energy and emissions, people, safety, governance and policies.", 742, 242, s, 600)


def esg():
    frameworks = [
        ("ISSB standards (IFRS S1, S2)", "International Sustainability Standards Board, part of the IFRS Foundation", "Global baseline for investor-focused sustainability and climate disclosure; issued June 2023", "The reference most others now point to"),
        ("CSDS 1 and CSDS 2", "Canadian Sustainability Standards Board", "Canada's version of IFRS S1 and S2, with transition reliefs; final December 2024", "Voluntary; the CSA paused its mandatory rule in April 2025"),
        ("SASB Standards", "Maintained by the ISSB", "Industry-specific metrics used inside IFRS S2", "Useful to pick the metrics that matter in your industry"),
        ("TCFD recommendations", "Disbanded October 2023", "Four pillars: governance, strategy, risk management, metrics and targets", "Absorbed into IFRS S2; still seen in older questionnaires"),
        ("GRI Standards", "Global Reporting Initiative", "Impact reporting for a broad audience: what the company does to people and the environment", "Common in sustainability reports and customer requests"),
        ("GHG Protocol", "WRI and WBCSD", "How to count Scope 1, 2 and 3 greenhouse gas emissions", "The method behind almost every emissions number"),
        ("EU CSRD and VSME", "European Union; EFRAG", "Mandatory reporting for large EU companies; VSME is the voluntary standard for smaller firms", "Caps what EU customers can ask of you"),
    ]
    body = f"""
<p>ESG (environmental, social and governance) reporting has gone through a large consolidation since this article was first written in 2022. Several of the frameworks it described have merged or disappeared, Canada has its own sustainability standards, and the rules on green marketing claims have changed twice. This updated guide is written for small and mid-sized Canadian businesses that are not required to publish a sustainability report but are increasingly asked for ESG information anyway.</p>
<h2>Why a small business gets asked</h2>
<p>Most mandatory sustainability reporting applies to large listed companies and banks. Smaller firms meet it indirectly, through four channels: customers who must report on their supply chains, lenders and investors who need climate information about their borrowers, European customers covered by EU rules, and the business's own marketing claims.</p>
{fig(fig_esg_asks(), 1, "Who asks a small business for ESG information, and the framework behind each request.")}
<h2>The frameworks in 2026</h2>
{table(["Framework", "Who sets it", "What it covers", "What it means for you"], frameworks)}
<p>Three changes stand out. First, the International Sustainability Standards Board (ISSB) issued IFRS S1 and IFRS S2 in June 2023, and the Task Force on Climate-related Financial Disclosures (TCFD) disbanded in October 2023 after its recommendations were fully built into IFRS S2. A company applying the ISSB standards meets the TCFD recommendations. Second, the SASB Standards are now maintained by the ISSB and supply the industry-specific metrics in IFRS S2. Third, the Climate Disclosure Standards Board, which this article used to list, was folded into the IFRS Foundation in 2022.</p>
<h2>Where Canada stands</h2>
<p>The Canadian Sustainability Standards Board finalized CSDS 1 (general requirements) and CSDS 2 (climate) on 18 December 2024. They follow IFRS S1 and S2 with some transition reliefs, such as more time for Scope 3 emissions, and are available for reporting periods beginning on or after 1 January 2025. They are voluntary: on 23 April 2025 the Canadian Securities Administrators paused work on the rule that would have made climate disclosure mandatory for public companies, and that pause still stands. Federally regulated banks and insurers do face climate disclosure requirements under OSFI Guideline B-15, which is one reason lenders ask their business clients for emissions data.</p>
<p>In practice, voluntary does not mean irrelevant. Large Canadian companies and their banks are building reports on CSDS and ISSB lines, and the questions reach their suppliers as questionnaires.</p>
<h2>If you sell to European customers</h2>
<p>The EU's Corporate Sustainability Reporting Directive (CSRD) was scaled back by the "Omnibus" package agreed in December 2025. It now applies to companies with more than 1,000 employees and over €450 million in turnover, plus large non-EU groups with significant EU business. Importantly for Canadian suppliers, it adds a value-chain cap: a reporting company may not demand more information from a business partner with fewer than 1,000 employees than is covered by the EU's voluntary standard for small and mid-sized enterprises, known as VSME. Its basic module covers topics such as energy use and greenhouse gas emissions, pollution, water, waste, workforce, health and safety, pay and training, and anti-corruption. If you prepare that data once, you can answer most EU customer requests.</p>
<h2>Green claims and the Competition Act</h2>
<p>Since June 2024 the Competition Act has expressly covered misleading environmental claims. Claims about a product's environmental benefits must be based on adequate and proper tests, and claims about the environmental benefits of a business or its activities must be substantiated. Bill C-15, which received royal assent on 26 March 2026, softened two points: business-level claims now need adequate and proper substantiation rather than an "internationally recognized methodology", and private parties can no longer take these claims directly to the Competition Tribunal, so enforcement rests with the Competition Bureau. The prohibition on false or misleading claims remains. Before you say "carbon neutral", "net zero" or "eco-friendly" on a website or label, keep the evidence on file.</p>
<h2>A practical starting point for a small business</h2>
<ol>
<li><strong>Collect one core data set each year:</strong> fuel and electricity use, Scope 1 and 2 emissions calculated with the GHG Protocol, headcount, turnover, training hours, safety incidents, and your main policies (code of conduct, health and safety, anti-corruption, privacy).</li>
<li><strong>Map it to the requests you actually get.</strong> Most customer questionnaires and the EU VSME basic module ask for the same items in different layouts.</li>
<li><strong>Add Scope 3 only where it matters,</strong> such as purchased materials for a manufacturer or freight for a distributor, and say how you estimated it.</li>
<li><strong>Check every environmental claim in your marketing</strong> against the evidence you hold.</li>
<li><strong>Use a management system to keep it going.</strong> An ISO 14001 environmental management system, or the integrated ISO 9001, 14001 and 45001 approach, gives the data an owner and a yearly review.</li>
</ol>
<p>Energy and emissions data often reveal savings too. Investments that cut fuel or electricity may also qualify for the clean technology tax credits extended in Budget 2026.</p>
""" + src([
        ("IFRS Foundation: The ISSB and the TCFD", "https://www.ifrs.org/sustainability/tcfd/"),
        ("Torys: Final CSSB standards and SEC rules (January 2025)", "https://www.torys.com/our-latest-thinking/publications/2025/01/final-cssb-standards-and-sec-rules"),
        ("Keslio: Sustainability reporting in Canada (CSDS, CSA pause, OSFI B-15)", "https://www.keslio.com/requirements/canada"),
        ("De Brauw: Omnibus final agreement on CSRD and CSDDD (December 2025)", "https://www.debrauw.com/articles/omnibus-now-final-agreement-reached-on-directive-amending-csrd-and-csddd"),
        ("Accountancy Europe: Omnibus explained, CSRD factsheet (January 2026)", "https://accountancyeurope.eu/wp-content/uploads/2026/01/260129-Omnibus-explained-CSRD-factsheet.pdf"),
        ("KPMG: Changes to Canada's anti-greenwashing laws (April 2026)", "https://kpmg.com/ca/en/insights/2026/04/changes-to-canadas-anti-greenwashing-laws.html"),
        ("CPA Ontario: Bill C-59, what CPAs need to know (updated April 2026)", "https://www.cpaontario.ca/sustainability/sustainability-simplified/bill-c-59-what-cpas-need-to-know"),
    ]) + rel([
        ("integrated-management-system-iso-9001-14001-45001", "One system, three standards: integrating ISO 9001, 14001 and 45001"),
        ("canada-budget-2026-what-manufacturers-and-process-plants-should-know", "Budget 2026: what manufacturers and process plants should know"),
        ("clean-hydrogen-itc-explained-for-plant-owners", "The Clean Hydrogen ITC, explained for plant owners"),
    ])
    return dict(slug=ESG, title="ESG Reporting Frameworks in 2026: A Guide for Canadian Small and Mid-Sized Businesses",
                desc="Which ESG frameworks still matter in 2026 (ISSB, CSSB, GRI, VSME), where Canada stands, the green-claims rules, and how a small business starts.",
                cats=["esg"], tags=["ESG", "ISSB", "CSSB", "CSDS", "GRI", "CSRD", "VSME", "greenwashing", "Competition Act"],
                body=body.strip(), date=DATE, author="Quak Foo Lee", read="6 min read", cover_label="ESG",
                related=["integrated-management-system-iso-9001-14001-45001", "canada-budget-2026-what-manufacturers-and-process-plants-should-know",
                         "clean-hydrogen-itc-explained-for-plant-owners"])


# ═════════════════════════ 2. ERP guide ═════════════════════════
# Worked 5-year cost example (illustrative): 25 users, cloud ERP.
FULL_U, FULL_P, LIGHT_U, LIGHT_P = 15, 110, 10, 8
LIC_YR = (FULL_U * FULL_P + LIGHT_U * LIGHT_P) * 12
ONE_TIME = [("Implementation partner (configuration, setup, project management)", 45_000),
            ("Data migration and cleansing", 8_000), ("Integrations (e-commerce, shipping, banking)", 10_000),
            ("Training", 6_000), ("Internal staff time: 600 hours at $55", 33_000)]
SUPPORT_YR = 6_000
ONE = sum(v for _, v in ONE_TIME)
TCO5 = ONE + 5 * (LIC_YR + SUPPORT_YR)
LIC_SHARE = 5 * LIC_YR / TCO5

CRIT = [("Fit to your critical processes", 30), ("Total five-year cost", 20), ("Implementation partner", 15),
        ("Ease of use", 15), ("Integration with your other systems", 10), ("Vendor and product future", 10)]
SCORES = {"Option A": [4, 3, 4, 4, 3, 4], "Option B": [3, 5, 3, 3, 4, 3], "Option C": [5, 2, 3, 3, 4, 4]}
WEIGHTED = {k: sum(w * s for (_, w), s in zip(CRIT, v)) / 100 for k, v in SCORES.items()}


def fig_phases():
    s = DEFS
    ph = [("1. Prepare", ["Map processes", "List requirements", "Clean data"], BLUE, PALE, "4–8 wk"),
          ("2. Select", ["Shortlist 3", "Scripted demos", "Score and check"], GREEND, GREENF, "6–10 wk"),
          ("3. Design", ["Fit-gap", "Configure", "Plan migration"], PURPLE, "#E7E7F8", "6–10 wk"),
          ("4. Test and train", ["Test real scenarios", "Load data", "Train users"], ORANGE, ORANGEF, "4–8 wk"),
          ("5. Go live", ["Cut over", "Support", "Review at 90 days"], NAVY, "#E4E9F0", "2–4 wk")]
    for i, (name, items, c, f, t) in enumerate(ph):
        x = 12 + i * 146
        s += f'<rect x="{x}" y="14" width="130" height="40" rx="8" fill="{c}"/>' + txt(x + 65, 39, name, "middle", "#fff", 13, True)
        s += f'<rect x="{x}" y="60" width="130" height="86" rx="8" fill="{f}" stroke="{c}"/>'
        for j, it in enumerate(items): s += txt(x + 65, 84 + j * 22, it, "middle", NAVY, 12.3)
        s += txt(x + 65, 168, t, "middle", MUTED, 12)
        if i < 4: s += arrow(x + 132, 34, x + 144, 34)
    s += f'<rect x="12" y="182" width="714" height="34" rx="8" fill="{SAND}" stroke="#C9C2B2"/>'
    s += txt(369, 204, "Change management and data quality run through every phase", "middle", NAVY, 13, True)
    return svg("Five phases of an ERP project for a small or mid-sized business. 1 Prepare, 4 to 8 weeks: map processes, list "
               "requirements, clean data. 2 Select, 6 to 10 weeks: shortlist three, scripted demos, score and check references. 3 Design, "
               "6 to 10 weeks: fit-gap, configure, plan migration. 4 Test and train, 4 to 8 weeks: test real scenarios, load data, train "
               "users. 5 Go live, 2 to 4 weeks: cut over, support, review at 90 days. Change management and data quality run through "
               "every phase.", 740, 226, s, 600)


def erp():
    crit_rows = [[c, f"{w}%"] + [str(SCORES[k][i]) for k in SCORES] for i, (c, w) in enumerate(CRIT)]
    crit_rows.append(["<strong>Weighted score (out of 5)</strong>", "100%"] + [f"<strong>{WEIGHTED[k]:.2f}</strong>" for k in SCORES])
    tco_rows = [[n, money(v)] for n, v in ONE_TIME] + [
        ["<strong>One-time total</strong>", f"<strong>{money(ONE)}</strong>"],
        [f"Licences: {FULL_U} full users at {money(FULL_P)}/month and {LIGHT_U} light users at {money(LIGHT_P)}/month", f"{money(LIC_YR)} a year"],
        ["Partner support and updates", f"{money(SUPPORT_YR)} a year"],
        ["<strong>Five-year total cost</strong>", f"<strong>{money(TCO5)}</strong>"]]
    pitfalls = [
        ("Choosing before mapping processes", "Requirements are vague, demos impress, gaps appear after signing", "Map the main processes first and turn them into demo scripts"),
        ("Too much customization", "Upgrades break and costs rise every year", "Change the process before changing the software; keep a short list of must-have customizations"),
        ("Dirty data", "Wrong stock, prices and balances on day one", "Clean and de-duplicate customers, items and open balances before migration"),
        ("No internal project lead", "Decisions stall and the partner fills the gap at your expense", "Name a project lead with authority and protected time"),
        ("Too little training and change management", "People keep spreadsheets alongside the new system", "Train on your own scenarios; appoint super-users in each team"),
        ("Underestimated scope", "Extra modules and integrations surface late", "Include integrations, reports and data migration in the quote; hold a contingency"),
        ("Big-bang go-live with no fallback", "Shipping or invoicing stops", "Rehearse the cut-over, go live at a quiet time, keep the old system read-only"),
    ]
    body = f"""
<p>An enterprise resource planning (ERP) system brings finance, sales, purchasing, inventory and often production into one database. For a growing small or mid-sized business it replaces a tangle of accounting software, spreadsheets and re-keyed orders. It is also one of the largest and riskiest projects such a business takes on. This guide combines two earlier Chmltech articles, on choosing an ERP and on implementation pitfalls, into one practical method.</p>
<h2>Signs you need an ERP</h2>
<ul>
<li>The same order or item is typed into two or more systems.</li>
<li>Nobody can say with confidence what is in stock or what an order really earned.</li>
<li>Month-end closing takes more than a week because data must be collected from several places.</li>
<li>Growth is limited by administration rather than demand.</li>
<li>Your accounting package cannot handle inventory, multiple locations, production or currencies well.</li>
</ul>
<p>If only one of these applies, a better accounting package or a single add-on may be enough. An ERP pays off when several apply at once.</p>
{fig(fig_phases(), 1, "The five phases of an ERP project. Durations are typical for a business with 15 to 100 users.")}
<h2>Step 1: Start with your processes, not the software</h2>
<p>Map how work actually flows today: quote to cash, procure to pay, plan to produce, and record to report. Mark where data is re-keyed, where people wait, and where errors start. From the maps, write requirements in your own words, such as "allocate stock to orders by promised date" rather than "advanced inventory". Rank them as must-have, important and nice-to-have. This step usually takes a few weeks and is the best protection against the most common cause of overruns: discovering missing functions after the contract is signed.</p>
<h2>Step 2: Shortlist three and run scripted demos</h2>
<p>Use your requirements to shortlist three systems and, just as importantly, three implementation partners. Then send each the same demo script built from your own processes and sample data, so that you compare like with like instead of watching each vendor's best features. Score each demo on the same criteria straight after it ends.</p>
{table(["Criterion", "Weight"] + list(SCORES), crit_rows)}
<p>In this illustrative example, Option A wins narrowly on a weighted score of {WEIGHTED['Option A']:.2f} even though Option B is cheaper and Option C fits the processes best. The weights make the trade-off explicit, so the decision does not rest on the most persuasive presenter. Always call two reference customers of a similar size and industry for each finalist, and ask what went wrong.</p>
<h2>Step 3: Count the five-year cost, not the licence</h2>
<p>Licence prices are the most visible cost and rarely the largest. The worked example below is for a 25-user distributor on a cloud ERP with per-user pricing. The numbers are illustrative; use quotes for your own case.</p>
{table(["Item", "Cost"], tco_rows)}
<p>Licences make up only {LIC_SHARE:.0%} of the five-year cost here. Implementation services, data migration and the time of your own staff make up the rest, and staff time is the item most often left out. A useful check is that implementation services commonly cost one to two times the annual licence fee for a small project. The Productivity Mega Deduction confirmed in Budget 2026 lets most businesses write off depreciable software and hardware in the year they are put in use, and the BDC LIFT program can finance technology projects.</p>
<h2>Step 4: Implement in phases, with an owner</h2>
<p>Name an internal project lead with the authority to make decisions and protected time to do the work. Hold a fit-gap review where the partner shows how the standard system handles each requirement; change your process where the standard way is good enough and keep customizations to the few that give you a real advantage. Test with real scenarios from your own business, not the partner's examples, and train people on those same scenarios. Most failures are not about the software. They come from vague scope, customization, poor data and too little attention to the people who will use the system every day.</p>
<h2>Common pitfalls and how to avoid them</h2>
{table(["Pitfall", "What happens", "How to avoid it"], pitfalls)}
<h2>After go-live</h2>
<p>Plan for a stabilization period of four to eight weeks with extra support, then review the project after 90 days against the problems that started it: order errors, stock accuracy, days to close the month, and time spent on administration. Most of the benefits come in the year after go-live, as people stop using workarounds and start using the reports.</p>
""" + src([
        ("ERP Research: Why do ERP projects fail? (citing Panorama Consulting's 2026 ERP Report)", "https://www.erpresearch.com/en-us/blog/why-do-erp-projects-fail"),
        ("TechTarget: Explaining the hidden costs of ERP implementations", "https://www.techtarget.com/enterprise-software/feature/Explaining-the-hidden-costs-of-ERP-implementations"),
    ]) + rel([
        (TOP, "10 ERP systems for small and mid-sized businesses in 2026"),
        ("understanding-erp-vs-mrp-a-comprehensive-comparison-of-manufacturing-systems", "ERP vs MRP: a comparison of manufacturing systems"),
        ("demystifying-mrp-a-comprehensive-guide-to-the-material-requirements-planning-process", "Demystifying MRP"),
        ("bdc-lift-program", "The BDC LIFT program"),
    ])
    return dict(slug=ERP, title="Choosing and Implementing an ERP for a Small or Mid-Sized Business: A Practical Guide",
                desc="How a growing business chooses and implements an ERP: process-first requirements, scripted demos, a weighted scorecard, five-year cost and pitfalls.",
                cats=["erp", "digital-technology"], tags=["ERP", "ERP selection", "ERP implementation", "total cost of ownership", "small business", "digital transformation"],
                body=body.strip(), date=DATE, author="Quak Foo Lee", read="6 min read", cover_label="ERP",
                related=[TOP, "understanding-erp-vs-mrp-a-comprehensive-comparison-of-manufacturing-systems", "bdc-lift-program"])


# ═════════════════════════ 3. Top 10 ERP ═════════════════════════
def top():
    head = ["System", "Typical size", "Typical fit", "Pricing model", "Published price (checked November 2026)"]
    small = [
        ("Microsoft Dynamics 365 Business Central", "10–250 employees", "Distributors, light manufacturers and service firms already on Microsoft 365", "Per user, per month", "US$80 Essentials, US$110 Premium (manufacturing), US$8 light user; list prices since 1 November 2025"),
        ("SAP Business One", "10–250 employees", "Small manufacturers and distributors wanting a mature package", "Subscription or perpetual, through partners", "Partner quotes"),
        ("Odoo", "5–250 employees", "Small firms wanting many modules at low licence cost; results depend heavily on the partner", "Per user, per month; Community edition free", "Canadian Standard plan about C$44 per user per month at list (lower first-year promotional rate); Custom plan higher"),
        ("MRPeasy", "10–200 employees", "Small manufacturers moving off spreadsheets: production planning, BOMs, stock and purchasing", "Per user, per month", "US$49 to US$149 per user per month, by plan"),
        ("ERPNext", "1–250 employees", "Budget-conscious small businesses with technical help; fully open source", "Free software; pay for hosting and implementation", "Licence free; Frappe Cloud hosting from about US$5 a month, unlimited users"),
    ]
    mid = [
        ("Oracle NetSuite", "50–500+ employees", "Fast-growing, multi-entity or e-commerce businesses; overkill for small, simple operations", "Annual base licence plus per-user fees and modules; around a 10-user minimum", "No published price; quotes only"),
        ("Acumatica", "25–500+ employees", "Distribution, construction and manufacturing firms with many occasional users", "Resource-based; unlimited users", "No published price; based on modules and transaction volume"),
        ("Epicor Kinetic (formerly Epicor ERP)", "50–1,000 employees", "Discrete manufacturers, job shops and make-to-order", "Subscription", "Quotes only"),
        ("SYSPRO", "50–500 employees", "Manufacturers and distributors wanting a faster, lower-cost implementation", "Subscription or perpetual", "Partner quotes"),
        ("DELMIAworks (formerly IQMS)", "50–500 employees", "Plastics, medical and repetitive manufacturers needing ERP and MES together", "Subscription or perpetual", "Quotes only"),
    ]
    body = f"""
<p>This list was first published in 2023 with prices that are now out of date. It has been rewritten for 2026 and checked against analyst and review data for company size, so that every system on it is one that small and mid-sized businesses actually buy. For each system it shows the typical company size, the kind of business it fits, how it is priced, and the published price where one exists. Typical sizes are approximate ranges drawn from analyst profiles and review data. It is not a ranking: the right system depends on your processes, your industry and, above all, the implementation partner. For how to choose, see our guide to <a href="../post/{ERP}.html">choosing and implementing an ERP</a>.</p>
<h2>For small businesses (about 10 to 100 employees)</h2>
{table(head, small)}
<p>These five can be implemented by a small business in a few months with a modest budget. MRPeasy is a manufacturing system first, with lighter accounting, so many users keep their accounting package alongside it. ERPNext costs nothing to license, but implementation is where the money goes, and experienced partners are fewer in Canada than for Odoo or Business Central.</p>
<h2>For mid-sized businesses (about 50 to 500 employees)</h2>
{table(head, mid)}
<p>These five suit businesses with more users, more sites or more complex production. They usually need a partner-led project of several months and a budget in the low to mid six figures including implementation. Smaller firms with simple operations will often pay for capability they do not use.</p>
<h2>What changed from the 2023 list</h2>
<ul>
<li><strong>Two systems were replaced.</strong> Infor CloudSuite Industrial (SyteLine) is a capable manufacturing ERP, but Infor's mid-market target is 200 to 2,000 employees and even small deployments are estimated at six figures in the first year, so it is replaced by MRPeasy. Sage Intacct is excellent financial software but has no native manufacturing or warehouse management, so it is replaced by ERPNext. Service firms that mainly need strong accounting rather than a full ERP should still look at Sage Intacct.</li>
<li><strong>Prices rose.</strong> Microsoft raised Business Central list prices on 1 November 2025, its first significant increase in more than five years: Essentials from US$70 to US$80 and Premium from US$100 to US$110 per user per month. Odoo also raises its regional prices periodically.</li>
<li><strong>Names changed.</strong> Epicor ERP is now sold as Epicor Kinetic, and IQMS, bought by Dassault Systèmes in 2019, is now DELMIAworks.</li>
<li><strong>Pricing models diverged.</strong> Per-user pricing (Business Central, Odoo, MRPeasy, NetSuite) favours firms with a few heavy users. Acumatica's resource-based model and ERPNext's hosting-only cost favour firms where many people need occasional access.</li>
<li><strong>AI features are now standard in sales pitches.</strong> Ask to see them working on your own data during the scripted demo, and ask whether they cost extra.</li>
</ul>
<h2>How to narrow the list</h2>
<ol>
<li><strong>Start with your size and growth plan.</strong> Choose from the group you will be in three years from now, not just today, to avoid replacing the system again.</li>
<li><strong>Then your industry.</strong> Manufacturers need production planning, bills of materials and shop-floor data; distributors need warehouse and pricing depth; project and service firms need project accounting.</li>
<li><strong>Check the local partner.</strong> A capable partner in your province with experience in your industry matters more than small feature differences.</li>
<li><strong>Model five years of cost,</strong> including your own staff time, for two or three finalists, and run the same scripted demo for each using your own data.</li>
</ol>
<p>Below about 20 people, a full ERP is often premature. A good accounting package with an inventory or MRP add-on may be the better first step.</p>
""" + src([
        ("TechTarget: Evaluating today's 10 leading ERP software vendors", "https://www.techtarget.com/enterprise-software/feature/Evaluating-todays-10-leading-ERP-software-vendors"),
        ("ERP Research: SAP Business One (target market)", "https://erpresearch.com/en-us/sap-business-one"),
        ("ERP Research: Best ERP software 2026 by company size", "https://erpresearch.com/en-gb/best-erp"),
        ("Alphavima: Business Central pricing guide (2026)", "https://alphavima.com/blog/business-central-pricing-guide/"),
        ("OEC.sh: Odoo pricing in Canada (July 2026)", "https://oec.sh/odoo-pricing/canada"),
        ("CostBench: MRPeasy pricing and alternatives (November 2026)", "https://costbench.com/software/manufacturing-erp/mrpeasy/alternatives/"),
        ("ERP Research: ERPNext", "https://erpresearch.com/erp/erpnext"),
        ("BrokenRubik: NetSuite for small businesses", "https://brokenrubik.com/blog/netsuite-for-small-businesses"),
        ("ERP Research: Acumatica pricing", "https://www.erpresearch.com/pricing/acumatica"),
        ("ERP Research: Epicor Kinetic", "https://www.erpresearch.com/pages/en-us/epicor-erp-kinetic"),
        ("ERP Research: SYSPRO", "https://erpresearch.com/erp/syspro"),
        ("ERP Research: Is Infor CloudSuite good for mid-market companies?", "https://www.erpresearch.com/en-us/blog/infor-erp-mid-market"),
        ("ERP Research: Acumatica vs Sage Intacct", "https://www.erpresearch.com/compare/acumatica-vs-sage-intacct"),
        ("Dassault Systèmes: Completion of the IQMS acquisition (January 2019)", "https://www.3ds.com/newsroom/news-releases/dassault-systemes-completes-iqms-acquisition"),
    ]) + rel([
        (ERP, "Choosing and implementing an ERP for a small or mid-sized business"),
        ("understanding-erp-vs-mrp-a-comprehensive-comparison-of-manufacturing-systems", "ERP vs MRP"),
        ("top-10-inventory-management-software-a-comprehensive-comparison-guide", "Inventory management software compared"),
    ])
    return dict(slug=TOP, title="10 ERP Systems for Small and Mid-Sized Businesses in 2026, Grouped by Company Size",
                desc="Ten ERP systems for Canadian SMEs in 2026, split into small and mid-sized groups: typical company size, fit, pricing model and published prices.",
                cats=["erp"], tags=["ERP", "Business Central", "SAP Business One", "Odoo", "MRPeasy", "ERPNext", "NetSuite", "Acumatica", "ERP pricing", "small business"],
                body=body.strip(), date=DATE, author="Quak Foo Lee", read="5 min read", cover_label="ERP",
                related=[ERP, "understanding-erp-vs-mrp-a-comprehensive-comparison-of-manufacturing-systems",
                         "top-10-inventory-management-software-a-comprehensive-comparison-guide"])


# ═════════════════════════ 4. GA4 ═════════════════════════
# Worked month for a B2B services site (illustrative).
CH = [("Organic search", 1150, 730, 9), ("Direct", 520, 300, 4), ("Referral (incl. AI assistants)", 180, 120, 3),
      ("Organic social", 310, 140, 1), ("Email", 240, 160, 2)]
SESS = sum(c[1] for c in CH); ENG = sum(c[2] for c in CH); KEY = sum(c[3] for c in CH)


def fig_plan():
    s = DEFS
    cols = [("Business goal", ["More quote requests", "from the website"], BLUE, PALE),
            ("Key event", ["quote_request form", "submitted"], GREEND, GREENF),
            ("Where to look", ["Reports › Acquisition ›", "Traffic acquisition"], PURPLE, "#E7E7F8"),
            ("Monthly question", ["Which channels and pages", "bring quote requests?"], ORANGE, ORANGEF)]
    for i, (h, lines, c, f) in enumerate(cols):
        x = 12 + i * 182
        s += f'<rect x="{x}" y="14" width="164" height="36" rx="8" fill="{c}"/>' + txt(x + 82, 37, h, "middle", "#fff", 13, True)
        s += f'<rect x="{x}" y="56" width="164" height="70" rx="8" fill="{f}" stroke="{c}"/>'
        s += txt(x + 82, 86, lines[0], "middle", NAVY, 12.5) + txt(x + 82, 106, lines[1], "middle", NAVY, 12.5)
        if i < 3: s += arrow(x + 166, 91, x + 180, 91)
    return svg("A measurement plan in four steps. Business goal: more quote requests from the website. Key event: the quote request "
               "form submitted. Where to look: Reports, Acquisition, Traffic acquisition. Monthly question: which channels and pages "
               "bring quote requests?", 740, 138, s, 600)


def ga():
    ch_rows = [[n, f"{s:,}", f"{e / s:.0%}", str(k), f"{k / s:.2%}"] for n, s, e, k in CH]
    ch_rows.append(["<strong>Total</strong>", f"<strong>{SESS:,}</strong>", f"<strong>{ENG / SESS:.0%}</strong>", f"<strong>{KEY}</strong>", f"<strong>{KEY / SESS:.2%}</strong>"])
    body = f"""
<p>This guide was first written in 2023 for Universal Analytics. Google stopped processing data in standard Universal Analytics properties on 1 July 2023 and has since removed access to them, so every website now measures with Google Analytics 4 (GA4). The ideas are the same: know where visitors come from, what they do, and whether they become enquiries or sales. The tools and names have changed. This rewrite covers what a small business needs to set up and which reports to read each month.</p>
<h2>What is different in GA4</h2>
<ul>
<li><strong>Everything is an event.</strong> A page view, a scroll, a file download and a form submission are all events with details attached.</li>
<li><strong>Goals are now key events.</strong> You mark the events that matter to the business, such as a form submission or purchase, as key events. Google called these conversions until March 2024.</li>
<li><strong>Engagement replaces bounce rate as the main quality measure.</strong> GA4 counts a session as engaged if it lasts longer than 10 seconds, includes a key event, or has two or more page views. Bounce rate still exists, but in GA4 it simply means the share of sessions that were not engaged.</li>
<li><strong>Detailed data has a time limit.</strong> Standard reports keep their aggregated data, but explorations and funnel reports only reach back as far as the data retention setting, which is 2 months by default and 14 months at most on the free version.</li>
</ul>
<h2>Set-up checklist</h2>
<ol>
<li><strong>Set data retention to 14 months</strong> (Admin › Data collection and modification › Data retention). The change is not retroactive, so do it on day one.</li>
<li><strong>Mark your key events:</strong> contact or quote form submitted, phone number or email clicked, brochure downloaded, purchase. Do not mark page views as key events, or every visit will count as a success.</li>
<li><strong>Filter out your own visits</strong> by defining internal traffic for your office IP address.</li>
<li><strong>Link Google Search Console</strong> to see which searches bring visitors, and link Google Ads if you advertise.</li>
<li><strong>Handle consent properly.</strong> Use a consent banner that matches the privacy laws where your visitors are, and say in your privacy policy that you use analytics.</li>
</ol>
{fig(fig_plan(), 1, "Start every report from a business goal, the key event that measures it, and the question you want answered.")}
<h2>Six reports to read each month</h2>
{table(["Report", "Where", "What to look for"], [
        ("Traffic acquisition", "Reports › Acquisition", "Sessions, engagement rate and key events by channel"),
        ("Pages and screens", "Reports › Engagement", "Which pages people read, and which lead to key events"),
        ("Landing page", "Reports › Engagement", "Which entry pages engage visitors and which lose them"),
        ("Key events", "Reports › Engagement", "Count of each key event, month on month"),
        ("Search Console queries", "Reports › Search Console (once linked)", "Searches you appear for, clicks and average position"),
        ("Tech: device and browser", "Reports › Tech", "Whether mobile visitors engage less, a sign of a layout problem"),
    ])}
<h2>Worked example: one month on a B2B website</h2>
<p>An engineering services firm has a website with a quote request form, marked as its key event. One month's numbers by channel are below; they are illustrative.</p>
{table(["Channel", "Sessions", "Engagement rate", "Quote requests", "Key event rate"], ch_rows)}
<p>Organic search brings the most sessions and the most quote requests. Referral traffic, which now includes visits from AI assistants such as ChatGPT and Perplexity, is small but converts at {CH[2][3] / CH[2][1]:.1%}, the highest rate of any channel, which suggests that people arriving from an AI answer have already done their research. Organic social brings visitors who rarely engage. Three actions follow: improve the pages that rank in search but have low engagement, make sure the site is easy for AI assistants to cite (see <a href="../post/the-key-differences-between-seo-and-geo-for-enhancing-your-online-presence.html">SEO vs GEO</a>), and spend less effort chasing social traffic that does not convert.</p>
<h2>Common mistakes</h2>
<ul>
<li>Leaving data retention at 2 months and losing a year of detail.</li>
<li>Counting your own team's visits.</li>
<li>Marking too many or the wrong events as key events.</li>
<li>Comparing GA4 bounce rates with old Universal Analytics figures; the definitions differ.</li>
<li>Reading traffic without key events. More visitors is only good if more of them call, write or buy.</li>
</ul>
""" + src([
        ("Google Analytics Help: Make the switch to Google Analytics 4", "https://support.google.com/analytics/answer/10759417?hl=en"),
        ("Google Analytics Help: Dimensions and metrics (engaged sessions)", "https://support.google.com/analytics/answer/12195621?hl=en"),
        ("Google Analytics Help: Data retention", "https://support.google.com/analytics/answer/7667196?hl=en"),
        ("PPC Land: Key events in GA4 (the 2024 rename from conversions)", "https://ppc.land/key-event/"),
    ]) + rel([
        ("the-key-differences-between-seo-and-geo-for-enhancing-your-online-presence", "SEO vs GEO: how to be found in Google and in AI answers"),
        ("maximize-your-visibility-with-these-local-seo-tips-for-small-businesses", "Local SEO tips for small businesses"),
        ("what-is-technical-seo-basics-and-10-best-practices", "Technical SEO basics"),
    ])
    return dict(slug=GA, title="How to Measure Your Website with Google Analytics 4: A Small Business Guide",
                desc="Measure a small business website with Google Analytics 4: key events, engaged sessions, a set-up checklist, six monthly reports and a worked example.",
                cats=["marketing"], tags=["Google Analytics 4", "GA4", "key events", "engagement rate", "web analytics", "small business marketing"],
                body=body.strip(), date=DATE, author="Quak Foo Lee", read="5 min read", cover_label="Analytics",
                related=["the-key-differences-between-seo-and-geo-for-enhancing-your-online-presence",
                         "maximize-your-visibility-with-these-local-seo-tips-for-small-businesses", "what-is-technical-seo-basics-and-10-best-practices"])


if __name__ == "__main__":
    for a in (esg(), erp(), top(), ga()):
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"][:50], len(re.sub(r"<svg.*?</svg>|<[^>]+>", " ", a["body"], flags=re.S).split()), "words")
    print(f"ERP: licence {LIC_YR:,}/yr, one-time {ONE:,}, TCO5 {TCO5:,}, licence share {LIC_SHARE:.0%}; scores {WEIGHTED}")
    print(f"GA: sessions {SESS}, engaged {ENG / SESS:.1%}, key {KEY}, rate {KEY / SESS:.2%}")
