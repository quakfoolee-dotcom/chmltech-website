"""Timely Canadian articles for Insights, November 2026 (V4.66).

1  Budget 2026: what manufacturers and process plants should know
2  SR&ED for engineering and software projects: what changed in 2026
3  The Clean Hydrogen ITC, explained for plant owners

(The fourth topic proposed, a map of AI funding after CDAP, became the rewrite of the old CDAP article:
 content/articles/refresh_articles.py.)

Usage:  python3 content/articles/canada_2026_articles.py
        python3 content/gen/add_article.py <slug>      (for each article)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import (nowrap, svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, RED,
                           MUTED, LINE, SAND, PALE, GREENF, ORANGEF)
from refresh_articles import src, rel, CDAP, LIFT

B26 = "canada-budget-2026-what-manufacturers-and-process-plants-should-know"
SRED = "sred-for-engineering-and-software-projects-what-changed-in-2026"
H2 = "clean-hydrogen-itc-explained-for-plant-owners"
DATE = "2026-11-13"
DISC = ('<p style="font-size:15px"><em>This article is general information, not tax or legal advice. Several measures described here '
        'are proposals that are not yet law, and the details can change before they are enacted. Confirm how they apply to your business with '
        'your accountant or tax advisor before you act on them.</em></p>')


# ───────────────────────── 1. Budget 2026 ─────────────────────────
def fig_timeline():
    s = DEFS
    X = lambda i: 60 + i * 155
    s += f'<line x1="40" y1="96" x2="700" y2="96" stroke="{NAVY}" stroke-width="2"/>'
    ev = [("Mar 26, 2026", ["Bill C-15 law:", "SR&ED limit $6M,", "capital eligible"], BLUE),
          ("Apr 1, 2026", ["SR&ED pre-claim", "approval opens"], BLUE),
          ("Sep 15, 2026", ["Productivity Mega", "Deduction: assets", "bought from today"], GREEND),
          ("Nov 5, 2026", ["Budget 2026:", "SR&ED widened,", "clean ITCs to 2040"], ORANGE),
          ("Jan 1, 2027", ["Small business", "rollover widened"], PURPLE)]
    for i, (d, lines, col) in enumerate(ev):
        x = X(i)
        s += f'<circle cx="{x}" cy="96" r="8" fill="#fff" stroke="{col}" stroke-width="3"/>'
        s += txt(x, 70, d, "middle", col, 13, True)
        for j, ln in enumerate(lines):
            s += txt(x, 128 + j * 17, ln, "middle", NAVY, 12.5)
    return svg("Timeline of five dates. March 26, 2026: Bill C-15 becomes law, raising the SR&ED limit to 6 million dollars and restoring "
               "capital expenditures. April 1, 2026: SR&ED pre-claim approval opens. September 15, 2026: the Productivity Mega Deduction applies "
               "to assets bought from that day. November 5, 2026: Budget 2026 widens SR&ED and extends clean economy credits to 2040. "
               "January 1, 2027: the small business rollover is widened.", 740, 186, s, 620, x0=0)


def fig_cash():
    # $1M asset: tax deferred by deducting in year 1 vs a 20% declining-balance class with the half-year rule
    rate = 0.27; cost = 1_000_000; ucc = cost; old = []
    for y in range(1, 6):
        r = 0.10 if y == 1 else 0.20
        d = ucc * r; ucc -= d; old.append(d)
    new = [cost, 0, 0, 0, 0]
    Y = lambda v: 220 - v / 1_000_000 * 180; s = ""
    for v in (0, 250_000, 500_000, 750_000, 1_000_000):
        s += f'<line x1="70" y1="{Y(v)}" x2="700" y2="{Y(v)}" stroke="{LINE}"/>' + txt(62, Y(v) + 4, f"${v / 1000:,.0f}K", "end", MUTED, 12)
    for i in range(5):
        x = 110 + i * 120
        s += f'<rect x="{x}" y="{Y(new[i])}" width="38" height="{220 - Y(new[i]):.1f}" fill="{GREEND}"/>'
        s += f'<rect x="{x + 42}" y="{Y(old[i])}" width="38" height="{220 - Y(old[i]):.1f}" fill="{BLUE}" opacity=".75"/>'
        s += txt(x + 40, 240, f"Year {i + 1}", "middle", NAVY, 12.5, True)
        s += txt(x + 61, Y(old[i]) - 6, f"${old[i] / 1000:,.0f}K", "middle", BLUE, 11.5)
    s += txt(129, Y(cost) - 6, "$1,000K", "middle", GREEND, 11.5, True)
    s += f'<rect x="470" y="22" width="14" height="14" fill="{GREEND}"/>' + txt(490, 34, "Mega Deduction: 100% in year 1", fill=NAVY, fs=12.5)
    s += f'<rect x="470" y="44" width="14" height="14" fill="{BLUE}" opacity=".75"/>' + txt(490, 56, "Standard: 20% declining balance", fill=NAVY, fs=12.5)
    return svg("Bar chart of the tax deduction for a 1 million dollar asset over five years. With the Productivity Mega Deduction, the full "
               "1 million dollars is deducted in year 1. Under a 20 percent declining-balance class with the half-year rule, the deductions are "
               f"100, 180, 144, 115 and 92 thousand dollars in years 1 to 5, with the rest claimed in later years.", 720, 254, s, 600, x0=10), old


def budget():
    timeline = fig_timeline()
    cash, old = fig_cash()
    gap1 = (1_000_000 - old[0]) * 0.27
    body = f"""<p>Canada's 2026 federal budget, titled <em>Masters of our Destiny</em>, was tabled on 5 November 2026. Most of the coverage went to the deficit, defence and a new sovereign wealth fund. For a manufacturer or the owner of a process plant, the important parts are in the tax measures: how fast you can write off equipment, what counts as research, and how long the clean technology credits last.</p>
<p>This article sets out the measures that matter for plants and factories, what each one is worth, and what to do before year end. Several are proposals that are not yet law, so the last section explains how to plan around that.</p>
{fig(timeline, 1, "The 2026 tax changes that matter for manufacturers and process plants, in order.")}
<h2>The measures at a glance</h2>
<table>
<tr><th>Measure</th><th>What it does</th><th>Applies from</th><th>Status</th></tr>
<tr><td>Productivity Mega Deduction</td><td>Write off the full cost of most equipment and other depreciable property in the year it is put in use, permanently</td><td>Property acquired on or after 15 September 2026</td><td>Draft law, confirmed in the budget</td></tr>
<tr><td>Wider SR&amp;ED</td><td>Adds testing and validation work for a first regulatory approval or certification, and the cost of patents and similar protection for IP from SR&amp;ED projects</td><td>Tax years starting on or after 5 November 2026</td><td>Proposed</td></tr>
<tr><td>Clean technology and clean electricity credits extended</td><td>The 30% Clean Technology ITC and 15% Clean Electricity ITC now cover property available for use before 2041, instead of before 2034</td><td>Budget Day</td><td>Proposed</td></tr>
<tr><td>Canada Growth Incentive</td><td>A capital gains exemption of up to $15 million on qualifying new shares of Canadian-controlled private corporations, held for at least 36 months</td><td>Shares issued from Budget Day to the end of 2036</td><td>Proposed</td></tr>
<tr><td>Small business rollover</td><td>A longer window, the year of sale plus three years, to reinvest gains from selling small business shares without paying tax</td><td>Sales on or after 1 January 2027</td><td>Proposed</td></tr>
</table>
<h2>1. The Productivity Mega Deduction</h2>
<p>This is the largest change for any business that buys equipment. The government announced it on 15 September 2026 and confirmed it in the budget. Once enacted, a business can deduct 100 percent of the cost of most depreciable property in the year the property becomes available for use, rather than spreading it over many years through capital cost allowance (CCA).</p>
<p>It is broader than the "Productivity Super-Deduction" from Budget 2025, which applied to selected classes such as manufacturing and processing machinery. The government estimates that the Super-Deduction covered about 15 percent of business investment in capital assets and that the Mega Deduction covers about two thirds. The starting point is now that depreciable property qualifies unless it is excluded.</p>
<ul>
<li><strong>What qualifies:</strong> most depreciable property acquired on or after 15 September 2026, such as production equipment, lab and test equipment, vehicles, computers and network hardware.</li>
<li><strong>What does not:</strong> buildings in CCA classes 1 and 3, and certain other property listed in the rules. Manufacturing and processing buildings keep the temporary immediate expensing introduced in Budget 2025.</li>
<li><strong>Timing:</strong> the property must be both acquired on or after 15 September 2026 and available for use in the year you claim it. Equipment that arrives in December but is not commissioned until February is claimed in the following year.</li>
</ul>
<h3>What it is worth</h3>
<p>The deduction changes when you get the tax relief, not how much you get in total. Take a $1 million asset in a class written off at 20 percent a year on a declining balance. Under the standard CCA rules, with the half-year rule and no accelerated allowance, the first-year deduction is ${old[0] / 1000:,.0f},000 and the asset takes well over a decade to write off. Temporary accelerated allowances, where they apply, narrow the gap. Under the Mega Deduction, the full $1 million is deducted in year one.</p>
{fig(cash, 2, "Deductions for a $1 million asset. The total is the same. The Mega Deduction moves it to year one.")}
<p>For a corporation paying the general rate of 27 percent in British Columbia, deducting $1 million in year one instead of ${old[0] / 1000:,.0f},000 cuts that year's tax by about ${gap1 / 1000:,.0f},000. Later years carry less CCA, so the tax comes back gradually. The benefit is cash now, which is worth most to a business that is borrowing to invest or growing fast.</p>
<p>Two cautions. First, a business with little taxable income, or one taxed at the small business rate, gets less value from a larger deduction. Second, selling written-off equipment later brings the deduction back into income as recapture. Run both cases with your accountant.</p>
<h2>2. SR&amp;ED: wider again</h2>
<p>The Scientific Research and Experimental Development program was already improved this year. Bill C-15 became law on 26 March 2026. It doubled the expenditure limit for the enhanced 35 percent refundable credit to $6 million, raised the taxable capital range over which that limit phases out, and made capital equipment used for SR&amp;ED eligible again. On 1 April the CRA opened an optional pre-claim approval process.</p>
<p>Budget 2026 proposes two additions for tax years that begin on or after 5 November 2026:</p>
<ul>
<li><strong>Regulatory work.</strong> Testing, technological validation and study work needed to obtain an initial regulatory approval or certification would count as SR&amp;ED. For a plant developing a new product, this can include the trials needed for a first certification.</li>
<li><strong>Protecting IP.</strong> The cost of obtaining and maintaining patents and similar protection would be eligible, if the IP comes from an SR&amp;ED project.</li>
</ul>
<p>Our article on <a href="{SRED}.html">SR&amp;ED for engineering and software projects</a> explains what qualifies and how to estimate a claim.</p>
<h2>3. Clean technology credits until 2040</h2>
<p>The refundable Clean Technology ITC (30 percent) and Clean Electricity ITC (15 percent) were due to end for property available for use after 2034. The budget extends both to property available for use before 2041. The Clean Technology ITC drops to 15 percent in its final year, now 2040. The Clean Electricity ITC also gains some large intra-provincial transmission projects.</p>
<p>For a plant, the Clean Technology ITC covers property such as heat pumps, solar and small hydro equipment, and certain energy storage. A longer window gives more room to plan an energy project around a turnaround instead of rushing it.</p>
<p>The summaries we reviewed do not show the same extension for the Clean Hydrogen ITC, which still drops to half its rate in 2034 and ends after 2034. See <a href="{H2}.html">the Clean Hydrogen ITC, explained for plant owners</a>.</p>
<h2>4. Owners raising money or selling</h2>
<p>The new Canada Growth Incentive would exempt up to $15 million of capital gains per person on qualifying shares of a Canadian-controlled private corporation issued from Budget Day to the end of 2036 and held for at least 36 months. Many industries are excluded, including consulting and professional practices, mining, utilities, real estate and finance. Manufacturing is not on the excluded list in the summaries we reviewed. The integrity rules have not been released yet.</p>
<p>The small business rollover, which defers tax when the proceeds from selling small business shares are reinvested, gets a longer window: the year of the sale plus three years, for sales from 1 January 2027.</p>
<h2>What to do before year end</h2>
<ol>
<li><strong>List equipment bought since 15 September 2026.</strong> Note the date each item was acquired and the date it became available for use. Assets acquired before 15 September stay under the old rules.</li>
<li><strong>Plan commissioning dates.</strong> An asset commissioned on 20 December gives a deduction this year. On 5 January it gives a deduction next year. Talk to your accountant about which you want.</li>
<li><strong>Review this year's development work for SR&amp;ED.</strong> If you are likely to claim, consider pre-claim approval for next year's projects.</li>
<li><strong>Put energy projects back on the list.</strong> With the Clean Technology ITC available until 2040 and immediate expensing for most equipment, the after-tax cost of a heat recovery or electrification project may be lower than when you last looked.</li>
<li><strong>Do not count unlegislated measures as cash yet.</strong> Model them as likely, and keep a fallback if the final rules change.</li>
</ol>
<h2>Proposed is not law</h2>
<p>A budget proposal usually becomes law months later, sometimes with changes. The Mega Deduction has been released as draft legislation, which helps, but its details may still move. Businesses generally file on the basis of proposals the government has said it will enact. Make that call with your advisor, and keep the documents that show when each asset was acquired and put in use.</p>
<h2>Key points</h2>
<ul>
<li>The Productivity Mega Deduction lets most equipment acquired from 15 September 2026 be written off in the year it is put in use. It speeds up the deduction. It does not increase the total.</li>
<li>SR&amp;ED would widen again to include first regulatory approvals and IP protection costs, on top of the $6 million limit and capital eligibility enacted in March.</li>
<li>The Clean Technology and Clean Electricity ITCs would run to the end of 2040. The Clean Hydrogen ITC still ends after 2034.</li>
<li>Owners raising equity or selling shares get a new capital gains exemption and a longer rollover window.</li>
</ul>
<p><strong>Planning a capital project?</strong> Chmltech helps manufacturers and process plants build the engineering and business case for new equipment, energy projects and automation. <a href="../book.html">Book a strategy call</a>.</p>
{DISC}
{src([("Gowling WLG: Federal Budget 2026", "https://gowlingwlg.com/en/insights-resources/articles/2026/federal-budget-2026"),
      ("Department of Finance Canada: New Productivity Mega Deduction (September 2026)", "https://www.canada.ca/en/department-finance/news/2026/09/government-of-canada-introduces-new-productivity-mega-deduction-to-boost-canadas-advantage-as-the-most-competitive-g7-country-for-new-business-inve.html"),
      ("Osler: Canadian prime minister announces Productivity Mega Deduction", "https://www.osler.com/en/insights/updates/canadian-prime-minister-announces-productivity-mega-deduction/"),
      ("KPMG: New investment deduction expands immediate expensing", "https://assets.kpmg.com/content/dam/kpmgsites/ca/pdf/tnf/2026/09/ca-new-investment-deduction-expands-immediate-expensing.pdf"),
      ("EY: Bill C-15 receives Royal Assent", "https://taxnews.ey.com/news/2026-0752-canadas-2025-budget-implementation-bill-no-1-receives-royal-assent"),
      ("CRA: SR&amp;ED pre-claim approval process", "https://www.canada.ca/en/revenue-agency/news/newsroom/tax-tips/tax-tips-2026/innovate-confidence-cra-sred-tax-incentive-program-pre-claim-approval-process.html")])}
{rel([(SRED, "SR&amp;ED for engineering and software projects: what changed in 2026"),
      (H2, "The Clean Hydrogen ITC, explained for plant owners"),
      ("engineering-capex-and-opex-estimation-for-process-plants", "Engineering CAPEX and OPEX estimation for process plants")])}"""
    body = nowrap(body, [(1, 0, 28), (1, 3, 20)])
    return dict(slug=B26, title="Budget 2026: What Manufacturers and Process Plants Should Know",
                desc="Budget 2026 for plants and factories: the Productivity Mega Deduction, wider SR&ED, clean technology credits to 2040, and what to do before year end.",
                cats=["strategy", "process-engineering"],
                tags=["Budget 2026", "Productivity Mega Deduction", "immediate expensing", "SR&ED", "Clean Technology ITC", "manufacturing", "capital cost allowance"],
                body=body, date=DATE, author="Quak Foo Lee", read="8 min read", cover_label="Tax",
                related=[SRED, H2, "engineering-capex-and-opex-estimation-for-process-plants"])


# ───────────────────────── 2. SR&ED ─────────────────────────
EX = dict(sal=600_000, mat=50_000, con=200_000, cap=100_000)


def sred_calc():
    ppa = 0.55 * EX["sal"]; con = 0.80 * EX["con"]
    base = EX["sal"] + ppa + EX["mat"] + con + EX["cap"]
    return ppa, con, base, 0.35 * base


def fig_test():
    s = DEFS
    qs = [("1", "Was there a scientific or technological uncertainty?", "Could standard practice and available knowledge solve it?"),
          ("2", "Did you form a hypothesis to reduce it?", "A stated idea of what might work, and why"),
          ("3", "Did you follow a systematic investigation?", "Plan, test, measure, change one thing, test again"),
          ("4", "Did you aim for an advance?", "New knowledge, even if the project failed"),
          ("5", "Did you keep records as you went?", "Test logs, data, commits, notebooks, timesheets")]
    for i, (n, q, sub) in enumerate(qs):
        y = 12 + i * 58
        s += f'<circle cx="34" cy="{y + 22}" r="17" fill="{NAVY}"/>' + txt(34, y + 27, n, "middle", "#fff", 14, True)
        s += f'<rect x="64" y="{y}" width="660" height="46" rx="8" fill="{PALE if i % 2 == 0 else "#fff"}" stroke="#9AB0C8"/>'
        s += txt(80, y + 20, q, fill=NAVY, fs=13.5, bold=True) + txt(80, y + 37, sub, fill=MUTED, fs=12.5)
        if i < 4: s += f'<line x1="34" y1="{y + 39}" x2="34" y2="{y + 63}" stroke="{NAVY}" stroke-width="1.5"/>'
    return svg("Five questions the CRA uses to judge SR&ED work. 1: Was there a scientific or technological uncertainty that standard practice "
               "could not solve? 2: Did you form a hypothesis to reduce it? 3: Did you follow a systematic investigation? 4: Did you aim for an "
               "advance, even if the project failed? 5: Did you keep records as you went?", 734, 300, s, 600, x0=10)


def sred():
    ppa, con, base, itc = sred_calc()
    body = f"""<p>Many engineering firms and plants do SR&amp;ED-eligible work every year and never claim it. They assume the program is for laboratories and software start-ups. It is not. A plant that cannot get a new formulation to scale, or an engineering team that writes software to control something no standard package can handle, may well qualify.</p>
<p>2026 made the program more valuable. The enhanced credit limit doubled, equipment became eligible again, and the CRA started confirming projects before the work begins. Budget 2026 proposes to widen it further. This article explains what qualifies in engineering and software, what changed, and how to estimate a claim.</p>
<h2>What changed in 2026</h2>
<table>
<tr><th>Change</th><th>Before</th><th>Now</th></tr>
<tr><td>Enhanced 35% credit limit</td><td>$3 million of spending a year</td><td>$6 million a year, for tax years starting after 15 December 2024</td></tr>
<tr><td>Phase-out of the limit</td><td>Taxable capital of $10 million to $50 million</td><td>$15 million to $75 million, with an option to use revenue instead</td></tr>
<tr><td>Capital equipment</td><td>Not eligible since 2014</td><td>Eligible again, for property acquired after 15 December 2024</td></tr>
<tr><td>Public corporations</td><td>Basic 15% credit only</td><td>Eligible Canadian public corporations can earn the enhanced 35% credit</td></tr>
<tr><td>Certainty before you start</td><td>Pre-claim consultation, no binding answer</td><td>Pre-claim approval, from 1 April 2026</td></tr>
<tr><td>Regulatory testing and IP costs</td><td>Not eligible</td><td>Proposed in Budget 2026, for tax years starting on or after 5 November 2026</td></tr>
</table>
<p>The first four changes were enacted by Bill C-15, which received Royal Assent on 26 March 2026. The Budget 2026 changes are proposals.</p>
<h2>What qualifies: the five questions</h2>
<p>SR&amp;ED is defined by the work, not the industry. The CRA asks five questions about each project.</p>
{fig(fig_test(), 1, "The five questions the CRA uses to decide whether work is SR&ED.")}
<p>The first question decides most claims. If a competent engineer could solve the problem with standard practice, published methods or known correlations, there is no technological uncertainty, however hard the work was. Difficulty is not uncertainty.</p>
<h2>Engineering and process work: examples</h2>
<table>
<tr><th>Likely SR&amp;ED</th><th>Not SR&amp;ED</th></tr>
<tr><td>Finding why a reaction that works at lab scale gives poor yield in the pilot plant, when published data do not explain it</td><td>Sizing a reactor, pump or heat exchanger with standard methods</td></tr>
<tr><td>Developing a new catalyst, membrane or separation step and testing variants systematically</td><td>Selecting equipment from vendor catalogues</td></tr>
<tr><td>Building a model to predict a property no correlation covers, and validating it against plant data</td><td>A HAZOP, a design review or a routine debottleneck</td></tr>
<tr><td>Trials to make a product meet a specification that existing processes cannot reach</td><td>Routine quality control testing and commissioning</td></tr>
</table>
<p>Our <a href="scale-up-what-changes-from-lab-to-pilot-to-commercial.html">scale-up series</a> describes the kind of work that often contains SR&amp;ED: questions that only a pilot plant can answer.</p>
<h2>Software work: examples</h2>
<p>Software projects qualify when the uncertainty is technological: how to make the system do something, not what it should do.</p>
<ul>
<li><strong>Likely SR&amp;ED:</strong> a control algorithm that has to run within a time limit standard libraries cannot meet; a machine learning model where no known method reaches the required accuracy on your data, and you test alternatives systematically; integrating systems where the published interfaces cannot deliver the required performance and a new approach must be found.</li>
<li><strong>Not SR&amp;ED:</strong> configuring an ERP or CRM, building a website or app with standard frameworks, connecting systems through their documented APIs, data migration, user interface design and routine bug fixing.</li>
</ul>
<p>A useful test: if your team could describe the solution on day one and the rest was effort, it is probably not SR&amp;ED. If they had to try things to find out whether it could be done, it may be.</p>
<h2>Estimating a claim</h2>
<p>Take a Canadian-controlled private corporation with a project that meets the five questions. In one year it spends:</p>
<table>
<tr><th>Item</th><th class="num">Spent</th><th>Rule</th><th class="num">Qualifying</th></tr>
<tr><td>Salaries of staff doing SR&amp;ED</td><td class="num">${EX['sal']:,}</td><td>Time spent on SR&amp;ED</td><td class="num">${EX['sal']:,}</td></tr>
<tr><td>Overhead (proxy method)</td><td class="num">–</td><td>55% of the salary base</td><td class="num">${ppa:,.0f}</td></tr>
<tr><td>Materials consumed in tests</td><td class="num">${EX['mat']:,}</td><td>Consumed or transformed</td><td class="num">${EX['mat']:,}</td></tr>
<tr><td>Contract testing by an arm's-length lab</td><td class="num">${EX['con']:,}</td><td>80% of contract payments</td><td class="num">${con:,.0f}</td></tr>
<tr><td>Test rig (capital)</td><td class="num">${EX['cap']:,}</td><td>Eligible again since December 2024</td><td class="num">${EX['cap']:,}</td></tr>
<tr><td><strong>Total</strong></td><td></td><td></td><td class="num"><strong>${base:,.0f}</strong></td></tr>
</table>
<p>At the enhanced 35 percent rate, the federal credit is about <strong>${itc:,.0f}</strong>. Because the company is under the $6 million limit, the credit on current spending is refundable: it is paid out even if the company owes no tax. In British Columbia a further 10 percent provincial credit applies to SR&amp;ED done in the province. Provincial credits reduce the federal base, so the combined figure is a little less than the sum of the two. This is a simplified example. Salaries of owners and specified employees, government funding received and many other rules change the result.</p>
<h2>Pre-claim approval: worth considering</h2>
<p>Since 1 April 2026, a business can ask the CRA to confirm that planned work is SR&amp;ED before it starts the work or spends the money. The CRA describes the process this way:</p>
<ol>
<li>Request a case number, then apply in My Business Account for up to three projects.</li>
<li>Meet a CRA SR&amp;ED specialist within about four weeks.</li>
<li>Receive a decision within about eight weeks of completing the application. An approval lasts up to three years.</li>
</ol>
<p>Claims for approved projects that need an expenditure review are processed in 90 days instead of 180. The approval covers technical eligibility only. The CRA can still review the costs. To apply, the business must be in good standing, and the work must not have been claimed already.</p>
<p>Pre-claim approval suits a first-time claimant, a large project, or a project whose eligibility is a judgement call. It needs a clear written description of the uncertainty before work starts, which is good discipline in any case.</p>
<h2>Records that make a claim stand up</h2>
<ul>
<li>A short project plan at the start: the uncertainty, the hypothesis and the planned tests.</li>
<li>Dated test logs, run sheets, lab notebooks, code commits and analysis files.</li>
<li>Time records that tie each person's hours to the project.</li>
<li>Invoices for materials and contracts, marked to the project.</li>
<li>A note at the end: what was learned, including what failed.</li>
</ul>
<p>Claims are filed with the tax return on Form T661 and the related schedules. The general deadline is 18 months after the end of the tax year. Late claims are not accepted.</p>
<h2>Key points</h2>
<ul>
<li>SR&amp;ED is about technological uncertainty, not industry. Engineering, process and software work can all qualify.</li>
<li>In 2026 the enhanced credit limit doubled to $6 million, equipment became eligible again, and the CRA began approving projects before they start.</li>
<li>Budget 2026 proposes to add first regulatory approvals and IP protection costs.</li>
<li>Keep records as you go. A strong claim is built during the project, not after it.</li>
</ul>
<p><strong>Not sure whether your project qualifies?</strong> Chmltech helps engineering teams describe the technical uncertainty in their scale-up and process development work, and plan the tests that resolve it. We work alongside your SR&amp;ED preparer. <a href="../book.html">Book a strategy call</a>.</p>
{DISC}
{src([("CRA: SR&amp;ED investment tax credit policy", "https://www.canada.ca/en/revenue-agency/services/scientific-research-experimental-development-tax-incentive-program/investment-tax-credit-policy.html"),
      ("CRA: Innovate with confidence, SR&amp;ED pre-claim approval process (April 8, 2026)", "https://www.canada.ca/en/revenue-agency/news/newsroom/tax-tips/tax-tips-2026/innovate-confidence-cra-sred-tax-incentive-program-pre-claim-approval-process.html"),
      ("CRA: How to apply for pre-claim approval", "https://www.canada.ca/en/revenue-agency/services/scientific-research-experimental-development-tax-incentive-program/apply-pre-claim-approval.html"),
      ("EY: Bill C-15 receives Royal Assent (March 30, 2026)", "https://taxnews.ey.com/news/2026-0752-canadas-2025-budget-implementation-bill-no-1-receives-royal-assent"),
      ("Gowling WLG: Federal Budget 2026", "https://gowlingwlg.com/en/insights-resources/articles/2026/federal-budget-2026"),
      ("Government of B.C.: SR&amp;ED tax credit", "https://www2.gov.bc.ca/gov/content/taxes/income-taxes/corporate/credits/scientific-research-development")])}
{rel([(B26, "Budget 2026: what manufacturers and process plants should know"),
      ("scale-up-what-changes-from-lab-to-pilot-to-commercial", "Lab to pilot to commercial: what changes when you scale up"),
      (CDAP, "After CDAP: where Canadian businesses find digital and AI funding")])}"""
    body = nowrap(body, [(1, 0, 26), (3, 0, 24), (3, 2, 30)])
    return dict(slug=SRED, title="SR&ED for Engineering and Software Projects: What Changed in 2026",
                desc="What counts as SR&ED in engineering, process and software work, what changed in 2026 ($6M limit, equipment, pre-claim approval), and a worked claim.",
                cats=["process-engineering", "digital-technology"],
                tags=["SR&ED", "R&D tax credit", "pre-claim approval", "engineering", "software development", "process development", "Canada"],
                body=body, date=DATE, author="Quak Foo Lee", read="9 min read", cover_label="R&D tax credit",
                related=[B26, "scale-up-what-changes-from-lab-to-pilot-to-commercial", CDAP])


# ───────────────────────── 3. Clean Hydrogen ITC ─────────────────────────
CAPEX = 30.0        # $M eligible clean hydrogen property, illustrative 10 MW electrolysis project


def fig_cliffs():
    Y = lambda p: 220 - p * 4.2; s = ""
    for p in (0, 10, 20, 30, 40):
        s += f'<line x1="80" y1="{Y(p)}" x2="700" y2="{Y(p)}" stroke="{LINE}"/>' + txt(72, Y(p) + 4, f"{p}%", "end", MUTED, 12)
    X = lambda ci: 80 + ci * 124
    tiers = [(0, 0.75, 40, GREEND), (0.75, 2, 25, BLUE), (2, 4, 15, ORANGE), (4, 5, 0, MUTED)]
    for a, b, r, col in tiers:
        s += f'<rect x="{X(a)}" y="{Y(r)}" width="{X(b) - X(a)}" height="{220 - Y(r):.1f}" fill="{col}" opacity=".8"/>'
        if r: s += txt((X(a) + X(b)) / 2, Y(r) - 8, f"{r}% · ${CAPEX * r / 100:.1f}M", "middle", col, 12.5, True)
        s += f'<rect x="{X(a)}" y="{Y(r / 2)}" width="{X(b) - X(a)}" height="2.5" fill="{NAVY}"/>' if r else ""
    for ci in (0, 0.75, 2, 4, 5):
        s += txt(X(ci), 238, f"{ci:g}", "middle", NAVY, 12)
    s += txt(390, 256, "Expected carbon intensity, kg CO₂e per kg H₂", "middle", NAVY, 12.5, True)
    s += txt(X(4.5), Y(4) , "Nil", "middle", MUTED, 12.5, True)
    s += f'<rect x="470" y="10" width="26" height="3" fill="{NAVY}"/>' + txt(502, 15, "Rate if available for use in 2034 (half)", fill=NAVY, fs=12)
    return svg("Step chart of the Clean Hydrogen ITC rate against expected carbon intensity. Below 0.75 kilograms of CO2 equivalent per kilogram "
               f"of hydrogen, 40 percent, worth 12 million dollars on a 30 million dollar project. From 0.75 to under 2, 25 percent, 7.5 million dollars. "
               "From 2 to under 4, 15 percent, 4.5 million dollars. At 4 or above, nil. A line in each step marks half the rate, which applies "
               "to property that becomes available for use in 2034.", 720, 266, s, 600, x0=10)


def fig_schedule():
    s = ""
    rows = [("Available for use in 2033", 40, GREEND), ("Slips into 2034", 20, ORANGE), ("Slips into 2035", 0, RED)]
    for i, (lab, r, col) in enumerate(rows):
        y = 20 + i * 52
        s += txt(196, y + 22, lab, "end", NAVY, 13.5, True)
        w = r / 40 * 330
        s += f'<rect x="210" y="{y}" width="{max(w, 2)}" height="34" rx="4" fill="{col}"/>'
        s += txt(220 + w, y + 22, f"${CAPEX * r / 100:.1f}M credit ({r}%)" if r else "No credit", fill=col, fs=13, bold=True)
    return svg("Bar chart of the credit on a 30 million dollar project below 0.75 kilograms carbon intensity, by the year it becomes available "
               "for use. 2033: 12 million dollars at 40 percent. 2034: 6 million dollars at 20 percent. 2035: no credit.", 740, 176, s, 560, x0=0)


def h2():
    body = f"""<p>The Clean Hydrogen Investment Tax Credit can return up to 40 percent of the capital cost of a hydrogen plant in cash. For a plant owner weighing an electrolyzer, a reformer with carbon capture or a pyrolysis unit, it is often the difference between a project that pencils out and one that does not.</p>
<p>It is also a credit with sharp edges. The rate depends on a carbon intensity threshold, the credit shrinks for a plant that starts up a year late, and the claim is checked against actual operation for years afterwards. This article explains how the credit works from an engineering point of view: what sets the rate, what can move it, and what to design for.</p>
<h2>The basics</h2>
<ul>
<li><strong>What it is:</strong> a refundable credit on the capital cost of eligible clean hydrogen property, claimed by a taxable Canadian corporation on its tax return. Refundable means it is paid out even if the company owes no tax.</li>
<li><strong>What it covers:</strong> equipment used to produce hydrogen in a qualified clean hydrogen project, and at a lower rate, equipment that converts the clean hydrogen into ammonia. Natural Resources Canada's Technical and Equipment Guidance lists what counts.</li>
<li><strong>Which processes:</strong> electrolysis, natural gas reforming with carbon capture, utilization and storage, and, since Budget 2025, methane pyrolysis.</li>
<li><strong>When:</strong> property acquired and available for use from 28 March 2023. The rate halves for property that becomes available for use in 2034, and the credit ends after 2034.</li>
<li><strong>Who decides:</strong> NRCan reviews the project plan and the carbon intensity model. The CRA handles the claim, audit and compliance.</li>
</ul>
<h2>The rate: set by carbon intensity</h2>
<p>The rate depends on the expected carbon intensity (CI) of the hydrogen, measured in kilograms of CO₂ equivalent per kilogram of hydrogen, from cradle to the plant gate. It includes upstream emissions, such as those from the electricity or natural gas you buy, up to the point the hydrogen leaves the plant.</p>
<table>
<tr><th>Expected carbon intensity</th><th class="num">Before 2034</th><th class="num">In 2034</th><th class="num">After 2034</th></tr>
<tr><td>Less than 0.75</td><td class="num">40%</td><td class="num">20%</td><td class="num">Nil</td></tr>
<tr><td>0.75 to less than 2</td><td class="num">25%</td><td class="num">12.5%</td><td class="num">Nil</td></tr>
<tr><td>2 to less than 4</td><td class="num">15%</td><td class="num">7.5%</td><td class="num">Nil</td></tr>
<tr><td>4 or more</td><td class="num">Nil</td><td class="num">Nil</td><td class="num">Nil</td></tr>
<tr><td>Clean ammonia equipment</td><td class="num">15%</td><td class="num">7.5%</td><td class="num">Nil</td></tr>
</table>
<p>These are the full rates, which require the business to elect to meet the labour requirements: prevailing wages and apprentice hours on the project. A business that does not elect them gets 10 percentage points less.</p>
<h2>The cliffs: why the design basis matters</h2>
<p>The rate does not slide. It steps. Take an illustrative electrolysis project with ${CAPEX:.0f} million of eligible property.</p>
{fig(fig_cliffs(), 1, f"The credit on ${CAPEX:.0f} million of eligible property at each carbon intensity tier. Illustrative example.")}
<p>A plant modelled at 0.74 kg earns 40 percent, or $12 million. The same plant at 0.76 kg earns 25 percent, or $7.5 million. A difference of 0.02 kg is worth $4.5 million. That makes the carbon intensity model a design document, not a compliance afterthought. Things that move it include:</p>
<ul>
<li><strong>Electricity supply.</strong> For electrolysis, the emission factor of the power you buy dominates the result. A contract for low-emission power, or on-site generation, can change the tier.</li>
<li><strong>Balance of plant.</strong> Compression, cooling, water treatment and purification all use electricity. A more efficient compressor lowers CI as well as operating cost.</li>
<li><strong>Upstream gas.</strong> For reforming or pyrolysis, methane emissions in the natural gas supply chain count, and the capture rate of the CCUS system matters most.</li>
<li><strong>Utilization.</strong> Start-ups, turndown and standby can raise the average CI per kilogram produced.</li>
</ul>
<p>Design with margin. If the base case sits just under a threshold, a modest change in the power mix or the capture rate can drop the project a tier.</p>
<h2>The calendar: schedule risk is credit risk</h2>
<p>The rate depends on when the property becomes available for use, not when you order it. A project that slips can lose half its credit, or all of it.</p>
{fig(fig_schedule(), 2, f"The credit on the same ${CAPEX:.0f} million project in the top tier, by the year it becomes available for use.")}
<p>For a project starting engineering now, 2033 looks distant. It is not. A hydrogen plant still needs <a href="from-concept-to-construction-five-stages-of-a-process-plant-project.html">FEED, permitting, procurement of long-lead equipment, construction and commissioning</a>. Electrolyzer stacks, compressors and transformers can carry long delivery times. Build the 2034 cut-off into the schedule as a hard constraint, with float.</p>
<p>Budget 2026 extended the Clean Technology and Clean Electricity ITCs to property available for use before 2041. The summaries we reviewed do not show the same extension for the Clean Hydrogen ITC. Industry groups, including the Canadian Hydrogen Association, have asked for changes, so check the current rules before you lock in a schedule.</p>
<h2>The claim is checked against operation</h2>
<p>The credit is paid on expected carbon intensity, before the plant runs. It is then tested against what the plant actually does. The main steps:</p>
<ol>
<li><strong>Project plan and CI model.</strong> Submit the project plan and the expected CI, modelled with NRCan's carbon intensity guidance and workbook, through NRCan's portal.</li>
<li><strong>Validation.</strong> A qualified, independent validation firm reviews the expected CI and prepares a validation report.</li>
<li><strong>Claim.</strong> Claim the credit on the corporate return with Schedule 74 once the property is available for use.</li>
<li><strong>Verification.</strong> During a compliance period after start-up, the actual CI is verified against the tier you claimed. If the plant runs dirtier than claimed, part of the credit can be recovered.</li>
</ol>
<p>Recapture can also apply if the property is later converted to another use, disposed of or exported. Read NRCan's Validation and Verification Guidance before the design is frozen, so the plant is metered and the data are kept in the form verification needs.</p>
<h2>Other rules to know</h2>
<ul>
<li><strong>One credit per property.</strong> Property claimed under the Clean Hydrogen ITC cannot also earn the Clean Technology ITC or another clean economy credit.</li>
<li><strong>Other government money.</strong> Grants and other assistance reduce the capital cost on which the credit is calculated.</li>
<li><strong>Ammonia.</strong> The 15 percent ammonia rate needs hydrogen with a CI below 4. EY's summary notes that the hydrogen and ammonia must be produced by the same taxpayer.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>The Clean Hydrogen ITC pays 15 to 40 percent of eligible capital cost, set by the expected carbon intensity of the hydrogen.</li>
<li>The tiers are cliffs. A small change in CI can move millions of dollars, so design with margin below the threshold.</li>
<li>The rate halves for property available for use in 2034 and ends after 2034. Schedule risk is credit risk.</li>
<li>The claim is validated before start-up and verified against actual operation afterwards. Meter and record for it from day one.</li>
</ul>
<p><strong>Planning a hydrogen project?</strong> Chmltech's process engineers have worked on hydrogen production, storage and scale-up. We prepare design bases, mass and energy balances and FEED packages that hold up to review. <a href="../book.html">Book a strategy call</a>.</p>
<p style="font-size:15px"><em>The project and costs in this article are an illustrative example. This is general information, not tax advice. NRCan and the CRA set the rules and decide eligibility. Confirm the current rules and your project's position with a tax advisor.</em></p>
{src([("CRA: Calculating the credit, Clean Hydrogen ITC", "https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/corporations/business-tax-credits/clean-economy-itc/clean-hydrogen-itc/claiming-credit-ch-itc/calculate.html"),
      ("CRA: Clean Hydrogen Investment Tax Credit", "https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/corporations/business-tax-credits/clean-economy-itc/clean-hydrogen-itc.html"),
      ("Parliamentary Budget Officer: Investment tax credit for clean hydrogen", "https://www.pbo-dpb.ca/en/publications/LEG-2324-021-S--investment-tax-credit-clean-hydrogen--credit-impot-investissement-hydrogene-propre"),
      ("EY: Canada's proposed clean hydrogen investment tax credit", "https://www.ey.com/en_ca/technical/tax/tax-alerts/2024/tax-alert-2024-no-21"),
      ("Gowling WLG: Federal Budget 2026", "https://gowlingwlg.com/en/insights-resources/articles/2026/federal-budget-2026"),
      ("Canadian Hydrogen Association: letter on clean economy ITCs (August 2026)", "https://canadah2.ca/wp-content/uploads/2026/08/2026-08-05-FINAL-Multi-Industry-Letter-on-Clean-Economy-ITCs-1.pdf")])}
{rel([("chmltech-online-journal-volume-102-issue-1", "Process intensification in hydrogen electrolysis plants"),
      ("the-design-basis-ten-decisions-to-fix-before-engineering-starts", "The design basis: ten decisions to fix before engineering starts"),
      (B26, "Budget 2026: what manufacturers and process plants should know")])}"""
    body = nowrap(body, [(1, 0, 26)])
    return dict(slug=H2, title="The Clean Hydrogen ITC, Explained for Plant Owners",
                desc="How Canada's Clean Hydrogen ITC works for a plant owner: carbon intensity tiers, the 2034 cut-off, validation and verification, and what to design for.",
                cats=["process-engineering", "esg"],
                tags=["Clean Hydrogen ITC", "hydrogen", "carbon intensity", "electrolysis", "CCUS", "investment tax credit", "process plant"],
                body=body, date=DATE, author="Quak Foo Lee", read="8 min read", cover_label="Hydrogen",
                related=["chmltech-online-journal-volume-102-issue-1",
                         "the-design-basis-ten-decisions-to-fix-before-engineering-starts", B26])


if __name__ == "__main__":
    for a in (budget(), sred(), h2()):
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("wrote", a["slug"], len(a["desc"]))
