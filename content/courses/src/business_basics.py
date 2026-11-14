"""Source for content/courses/business-basics.json (run: python3 content/courses/src/business_basics.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import step, E, write

M1 = [
step("Reading the three financial statements", 8, """
<p>Every business produces three core financial statements. Each answers a different question, and an owner who can read all three makes better decisions.</p>
<table><thead><tr><th>Statement</th><th>Question it answers</th><th>Key lines</th></tr></thead><tbody>
<tr><td>Income statement (profit and loss)</td><td>Did we make a profit over a period?</td><td>Revenue, cost of goods sold, gross profit, operating expenses, net income</td></tr>
<tr><td>Balance sheet</td><td>What do we own and owe at a point in time?</td><td>Assets (cash, receivables, inventory, equipment), liabilities (payables, loans), owner's equity</td></tr>
<tr><td>Cash flow statement</td><td>Where did cash come from and go over a period?</td><td>Cash from operations, investing and financing</td></tr>
</tbody></table>
<h3>How they connect</h3>
<p>Net income from the income statement flows into owner's equity on the balance sheet. The cash flow statement explains why cash on the balance sheet changed between two dates. A profitable business can still run short of cash if money is tied up in receivables or inventory, or spent on equipment and loan repayments. That is why owners need all three.</p>
<h3>A monthly habit</h3>
<p>Ask your bookkeeper or accountant for monthly statements within two to three weeks of month-end. Compare each month with the same month last year and with your budget. Look first at revenue, gross margin percentage, operating expenses, net income, cash balance, receivables and inventory. Ask about any line that moved more than you expected.</p>
<p>The balance sheet equation always holds: <strong>assets = liabilities + owner's equity</strong>. If you borrow $50,000, cash (an asset) and loans (a liability) both rise by $50,000, and equity is unchanged.</p>
<p>The lab after this lesson asks you to match items to the statement where they appear. This course is general business education; for tax, accounting and legal decisions, work with your accountant and other qualified advisers.</p>
""", ["The income statement shows profit, the balance sheet shows position, the cash flow statement shows cash movement.", "Profit and cash are different; you need all three statements.", "Review monthly statements against last year and budget."],
 "Ask for last month's three statements and write one sentence on what each tells you about the business.",
 "Which statement shows what the business owns and owes on a specific date?", ["Income statement", "Balance sheet", "Cash flow statement", "Sales report"], 1,
 "The balance sheet is a snapshot of assets, liabilities and equity at a point in time."),
step("Profit is not cash", 7, """
<p>Many profitable businesses get into trouble because they run out of cash. Profit is an accounting measure of whether revenue exceeds costs over a period. Cash is the money in the bank that pays wages, suppliers and the bank.</p>
<h3>Why they differ</h3>
<ul><li><strong>Customers pay later:</strong> a sale counts as revenue when invoiced, but cash arrives 30, 60 or 90 days later.</li>
<li><strong>Inventory ties up cash:</strong> you pay for stock before you sell it.</li>
<li><strong>Equipment purchases</strong> use cash at once but are expensed gradually as depreciation.</li>
<li><strong>Loan repayments</strong> use cash but only the interest is an expense.</li>
<li><strong>Growth needs cash:</strong> more sales mean more receivables and inventory before customers pay.</li></ul>
<h3>The cash conversion cycle</h3>
<p>The <strong>cash conversion cycle (CCC)</strong> measures how many days cash is tied up between paying suppliers and collecting from customers:</p>
<p><strong>CCC = days sales outstanding (DSO) + days inventory outstanding (DIO) − days payables outstanding (DPO)</strong></p>
<p>If customers pay in 45 days, inventory sits for 60 days and you pay suppliers in 30 days, the cycle is 45 + 60 − 30 = 75 days. Every day you cut from the cycle frees cash. For a business with $3 million of annual cost of sales, one day is worth roughly $8,000 of cash (3,000,000 ÷ 365).</p>
<h3>Growing broke</h3>
<p>Fast growth with a long cash cycle can drain the bank account even when every sale is profitable. Before chasing a large new contract, estimate how much extra receivables and inventory it will require and how you will fund them.</p>
""", ["Profit is an accounting measure; cash pays the bills.", "CCC = DSO + DIO − DPO; shorter frees cash.", "Fast growth can drain cash even when sales are profitable."],
 "Estimate your DSO, DIO and DPO from your last balance sheet and income statement, and calculate your cash conversion cycle.",
 "Customers pay in 50 days, inventory sits 40 days and suppliers are paid in 30 days. What is the cash conversion cycle?", ["120 days", "60 days", "40 days", "20 days"], 1,
 "CCC = 50 + 40 − 30 = 60 days."),
step("Margin, markup and contribution margin", 7, """
<p>Three terms are often confused, and the confusion can cost money when setting prices.</p>
<table><thead><tr><th>Term</th><th>Formula</th><th>Example: cost $60, price $100</th></tr></thead><tbody>
<tr><td>Gross margin</td><td>(price − cost) ÷ price</td><td>$40 ÷ $100 = 40%</td></tr>
<tr><td>Markup</td><td>(price − cost) ÷ cost</td><td>$40 ÷ $60 = 66.7%</td></tr>
<tr><td>Contribution margin</td><td>price − all variable costs</td><td>If freight and commission add $8: $100 − $68 = $32</td></tr>
</tbody></table>
<p>A 40% markup is not a 40% margin. If you want a 40% gross margin on an item costing $60, the price must be $60 ÷ (1 − 0.40) = $100, not $60 × 1.40 = $84.</p>
<h3>Why contribution margin matters</h3>
<p><strong>Variable costs</strong> change with each unit sold: materials, direct labour paid by the piece, freight, commissions, card fees. <strong>Fixed costs</strong> stay roughly the same whatever the volume over a period: rent, salaries, insurance, software subscriptions. Contribution margin is what each sale contributes toward fixed costs and then profit. It is the right number for decisions about discounts, special orders and which products to push.</p>
<h3>Margin by product and customer</h3>
<p>Average margins hide winners and losers. Calculate gross or contribution margin by product line and by major customer at least twice a year. Many businesses find a few products or customers earn most of the profit while others barely cover their costs once discounts, freight and service time are counted.</p>
""", ["Margin is profit over price; markup is profit over cost.", "Price = cost ÷ (1 − target margin).", "Use contribution margin for discount and product decisions, and review it by product and customer."],
 "Pick five products or services and calculate gross margin and markup for each. Check whether your price list uses margin or markup and whether staff know the difference.",
 "An item costs $80. What price gives a 20% gross margin?", ["$96", "$100", "$84", "$120"], 1,
 "Price = $80 ÷ (1 − 0.20) = $100."),
step("Break-even and pricing", 8, """
<p>The <strong>break-even point</strong> is the sales level at which the business covers all its costs and makes zero profit. Above it, each sale's contribution margin becomes profit.</p>
<p><strong>Break-even units = fixed costs ÷ contribution margin per unit</strong></p>
<p>Example: fixed costs are $40,000 a month, the average price is $120 and variable cost is $72. Contribution margin is $48 per unit, so break-even is 40,000 ÷ 48 ≈ 834 units a month, or about $100,000 of revenue. To earn $10,000 profit a month, you need (40,000 + 10,000) ÷ 48 ≈ 1,042 units.</p>
<h3>What break-even tells you</h3>
<ul><li>How far current sales are above or below break-even: your safety margin.</li>
<li>How much extra volume a new fixed cost, such as a hire or a lease, requires.</li>
<li>What a discount really costs: a 10% price cut on the example above cuts contribution from $48 to $36, so break-even rises to about 1,112 units, a third more volume.</li></ul>
<h3>Pricing approaches</h3>
<table><thead><tr><th>Approach</th><th>How it works</th><th>Watch out for</th></tr></thead><tbody>
<tr><td>Cost-plus</td><td>Cost plus a target margin</td><td>Ignores what customers value and what competitors charge</td></tr>
<tr><td>Competitive</td><td>Priced against alternatives</td><td>Can start a race to the bottom</td></tr>
<tr><td>Value-based</td><td>Priced on the value delivered to the customer</td><td>Needs a clear understanding of the customer's gains</td></tr>
</tbody></table>
<p>Most SMEs use cost to set a floor and value and competition to set the price. Review prices at least yearly and when costs change. Small, regular increases are usually easier for customers to accept than rare large ones. The lab after this lesson calculates break-even for your own numbers.</p>
""", ["Break-even units = fixed costs ÷ contribution margin per unit.", "Discounts raise break-even volume sharply.", "Use cost as a floor; set price with value and competition in mind."],
 "Estimate your monthly fixed costs and average contribution margin, and calculate break-even. How far above or below it were you last month?",
 "Fixed costs are $30,000 a month and contribution margin is $25 per unit. What is break-even volume?", ["750 units", "1,200 units", "1,500 units", "3,000 units"], 1,
 "30,000 ÷ 25 = 1,200 units a month."),
]

M2 = [
step("Budgets and a 13-week cash flow forecast", 8, """
<p>A <strong>budget</strong> is your financial plan for the year: expected revenue, costs and profit by month. A <strong>cash flow forecast</strong> predicts the bank balance week by week. Together they let you see problems coming instead of discovering them in the bank account.</p>
<h3>Building a simple annual budget</h3>
<ol><li>Start with a sales forecast by month, by product line or customer group, using last year, known contracts and realistic growth.</li>
<li>Apply expected gross margins to get cost of sales.</li>
<li>List operating expenses line by line: wages, rent, marketing, software, insurance, professional fees.</li>
<li>Add planned hires and investments in the months they start.</li>
<li>Review the result: does the profit meet your goals? If not, adjust plans, not just numbers.</li></ol>
<h3>The 13-week cash flow forecast</h3>
<p>A rolling 13-week forecast shows the next quarter week by week. For each week list opening cash, expected receipts (based on when customers actually pay, not when you invoice), expected payments (payroll, suppliers, rent, loan payments, taxes) and closing cash. Update it every week, replacing forecasts with actuals.</p>
<table><thead><tr><th></th><th>Week 1</th><th>Week 2</th><th>Week 3</th></tr></thead><tbody>
<tr><td>Opening cash</td><td>$80,000</td><td>$62,000</td><td>$71,000</td></tr>
<tr><td>Customer receipts</td><td>$45,000</td><td>$60,000</td><td>$38,000</td></tr>
<tr><td>Payroll</td><td>$35,000</td><td>$0</td><td>$35,000</td></tr>
<tr><td>Suppliers and other</td><td>$28,000</td><td>$51,000</td><td>$30,000</td></tr>
<tr><td>Closing cash</td><td>$62,000</td><td>$71,000</td><td>$44,000</td></tr>
</tbody></table>
<p>When the forecast shows a low point weeks ahead, you have time to act: chase receivables, delay a purchase, agree terms with a supplier or arrange credit before you need it. Banks are far more helpful when you ask early with a forecast in hand.</p>
""", ["A budget plans the year; a cash forecast predicts the bank balance.", "Forecast receipts by when customers actually pay.", "Update a rolling 13-week forecast weekly to see low points early."],
 "Build a 13-week cash forecast in a spreadsheet using your expected receipts and payments. Mark the lowest week and what you would do about it.",
 "Why forecast customer receipts by actual payment timing rather than invoice date?", ["Invoice dates are illegal to use", "Cash arrives when customers pay, often weeks after invoicing", "It makes revenue look higher", "Banks require invoice dates"], 1,
 "Cash forecasts must reflect when money actually arrives, which is usually later than the invoice date."),
step("Managing working capital", 7, """
<p><strong>Working capital</strong> is current assets (cash, receivables, inventory) minus current liabilities (payables, short-term debt). Managing it well frees cash without selling more.</p>
<h3>Receivables: get paid sooner</h3>
<ul><li>Invoice promptly and accurately; errors are a common reason for late payment.</li>
<li>Set clear terms and check new customers' credit.</li>
<li>Offer easy payment methods, such as electronic funds transfer.</li>
<li>Follow up systematically: a reminder before the due date, a call when overdue.</li>
<li>Consider deposits or progress billing on large or custom jobs.</li>
<li>Review an aged receivables report every week.</li></ul>
<h3>Inventory: hold what you need</h3>
<p>Classify items by value, set reorder points and safety stock by item, and act on slow-moving stock. The Inventory Management for SMEs course covers this in depth.</p>
<h3>Payables: pay on time, not early</h3>
<p>Pay suppliers on the agreed due date, not before, unless an early-payment discount is worth more than the cash. Negotiate terms that match your cash cycle, and keep good relationships: suppliers who trust you are more flexible when you need help.</p>
<h3>Early-payment discounts</h3>
<p>A term of "2/10 net 30" means a 2% discount if you pay in 10 days instead of 30. Giving up the discount to keep the cash for 20 more days costs about 2% for 20 days, which works out to well over 30% a year. Taking such discounts is usually worth it if you have the cash or cheap credit.</p>
""", ["Working capital = current assets − current liabilities.", "Invoice promptly, follow up systematically and review aged receivables weekly.", "Pay on the due date, and take early-payment discounts when they are worth it."],
 "Review your aged receivables report. List every invoice over 60 days, the reason it is late and the next action.",
 "A supplier offers 2/10 net 30. What does it mean?", ["2% discount if paid within 10 days; otherwise full amount due in 30 days", "2 invoices due every 10 days", "Pay 10% now and 30% later", "Interest of 2% per month after 30 days"], 0,
 "2/10 net 30 gives a 2% discount for payment within 10 days, with the net amount due in 30."),
step("KPIs and a monthly management dashboard", 7, """
<p>Financial statements arrive weeks after month-end and describe the past. <strong>Key performance indicators (KPIs)</strong> give earlier and more specific signals. A one-page monthly dashboard of 8 to 12 KPIs keeps the owner and managers focused on what matters.</p>
<h3>Choosing KPIs</h3>
<table><thead><tr><th>Area</th><th>Example KPIs</th></tr></thead><tbody>
<tr><td>Sales</td><td>New orders, quotes sent, quote win rate, sales by segment</td></tr>
<tr><td>Profitability</td><td>Gross margin %, operating expenses as % of revenue</td></tr>
<tr><td>Cash</td><td>Cash balance, DSO, overdue receivables, inventory days</td></tr>
<tr><td>Operations</td><td>On-time delivery, quality or return rate, productivity</td></tr>
<tr><td>Customers</td><td>Retention, complaints, satisfaction or referral score</td></tr>
<tr><td>People</td><td>Staff turnover, overtime, open positions</td></tr>
</tbody></table>
<h3>Leading and lagging</h3>
<p><strong>Lagging indicators</strong>, such as revenue and profit, report results. <strong>Leading indicators</strong>, such as quotes sent, pipeline value and on-time delivery, predict them. A good dashboard includes both, so you can act before results suffer.</p>
<h3>Making KPIs useful</h3>
<ul><li>Give each KPI an owner, a definition and a target.</li>
<li>Show trends over 12 months, not just this month's number.</li>
<li>Use simple colour coding: on target, watch, off target.</li>
<li>Review the dashboard in a monthly management meeting and agree actions for anything off target.</li></ul>
<p>The Data and Dashboards for SMEs course shows how to build and automate these dashboards.</p>
""", ["Use 8 to 12 KPIs on one page across sales, profit, cash, operations, customers and people.", "Include leading indicators that predict results.", "Give each KPI an owner, definition, target and trend."],
 "Draft your one-page dashboard: pick 8 to 12 KPIs, assign an owner and target to each, and note where the data comes from.",
 "Which is a leading indicator of future sales?", ["Last year's revenue", "Net income", "Value of quotes in the pipeline", "Taxes paid"], 2,
 "Pipeline value signals future orders before revenue is recorded."),
step("Financing, advisers and your accountant", 7, """
<p>Most businesses need outside money at some point: to buy equipment, fund growth or bridge a seasonal low. Matching the financing to the purpose avoids expensive mistakes.</p>
<table><thead><tr><th>Need</th><th>Common financing</th></tr></thead><tbody>
<tr><td>Seasonal or working capital swings</td><td>Operating line of credit</td></tr>
<tr><td>Equipment and vehicles</td><td>Term loan or lease over the asset's useful life</td></tr>
<tr><td>Real estate</td><td>Commercial mortgage</td></tr>
<tr><td>Growth projects, technology</td><td>Term loan; some government programs; in some cases equity</td></tr>
<tr><td>Receivables tied up</td><td>Receivable financing or factoring (usually costly)</td></tr>
</tbody></table>
<p>A key rule: do not fund long-term assets with short-term money. Using the operating line to buy a machine leaves no room for the next cash squeeze.</p>
<h3>Debt versus equity</h3>
<p>Debt must be repaid with interest but leaves ownership with you. Equity brings in money and often expertise but gives up part of the ownership and future profits. Many owners prefer debt for predictable needs and consider equity for large, risky growth.</p>
<h3>Preparing to ask</h3>
<p>Lenders, including banks, credit unions and development lenders, look for repayment ability, a credible plan and the owner's commitment. Bring recent financial statements, a budget and cash forecast, a clear use of funds and how the loan will be repaid. Check the Funding page on this site for programs that support SMEs, and confirm eligibility directly with each.</p>
<h3>Your advisory team</h3>
<p>An accountant does more than file taxes: they can help with budgets, cost analysis, tax planning, structure and succession. Meet them at least twice a year to discuss the business, not just at year-end. Add a lawyer for contracts and agreements, an insurance broker and, as you grow, a banker who understands your industry.</p>
""", ["Match financing to the purpose; don't fund long-term assets with short-term credit.", "Weigh debt, which must be repaid, against equity, which shares ownership.", "Bring statements, forecasts and a clear plan to lenders, and meet your accountant regularly."],
 "List your expected financing needs for the next two years by purpose, and match each to a suitable type of financing.",
 "Why should a new machine generally not be bought with the operating line of credit?", ["Lines of credit cannot be used for purchases", "Long-term assets should be funded with long-term financing so the line stays available for working capital", "Machines must always be leased", "Banks prohibit it"], 1,
 "Using the operating line for long-term assets leaves no room for normal cash swings."),
]

M3 = [
step("Vision, focus and where you compete", 7, """
<p>Strategy is about choices: what the business will do, for whom, and what it will not do. Without clear choices, owners spread time and money across too many opportunities and do none of them well.</p>
<h3>Core elements</h3>
<ul><li><strong>Purpose:</strong> why the business exists beyond making money.</li>
<li><strong>Vision:</strong> what the business will look like in three to five years: size, markets, reputation.</li>
<li><strong>Core values:</strong> a few behaviours you hire, reward and correct for.</li>
<li><strong>Target customers:</strong> the segments you serve best and most profitably.</li>
<li><strong>Value proposition:</strong> why those customers choose you over alternatives.</li></ul>
<h3>Where to compete and how to win</h3>
<p>Two questions sharpen strategy:</p>
<ol><li><strong>Where will we play?</strong> Which customers, products, regions and channels.</li>
<li><strong>How will we win there?</strong> Lower cost, better quality, faster service, specialist expertise, a stronger relationship, a unique product.</li></ol>
<p>Small businesses rarely win on price against larger competitors. They win by specializing: a niche, a region, a service level or an expertise that larger firms cannot or will not match.</p>
<h3>Saying no</h3>
<p>Strategy shows in what you decline: customers who are unprofitable or a poor fit, products that distract, projects outside your strengths. Write down three things the business will stop doing or not start this year. It is often the most valuable part of a strategy session.</p>
""", ["Strategy is a set of choices about where to play and how to win.", "SMEs usually win by specializing, not on price.", "Decide what to stop or decline, not only what to add."],
 "Write one paragraph describing your target customers and why they choose you. Then list three things you will stop doing or not start.",
 "How do most small businesses compete successfully against larger rivals?", ["By always offering the lowest price", "By specializing in a niche, region, service level or expertise", "By copying the largest competitor", "By serving every possible customer"], 1,
 "Specialization lets small firms deliver value larger competitors cannot match."),
step("SWOT and understanding your market", 7, """
<p>Good strategy rests on an honest view of the business and its environment. Two simple tools help.</p>
<h3>SWOT</h3>
<table><thead><tr><th></th><th>Helpful</th><th>Harmful</th></tr></thead><tbody>
<tr><td>Internal</td><td><strong>Strengths:</strong> skills, reputation, relationships, assets</td><td><strong>Weaknesses:</strong> gaps in skills, systems, capacity or finances</td></tr>
<tr><td>External</td><td><strong>Opportunities:</strong> market growth, new customer needs, technology, competitors' gaps</td><td><strong>Threats:</strong> new competitors, cost increases, regulation, economic changes</td></tr>
</tbody></table>
<p>Make it specific and evidence-based. "Good customer service" is weak; "on-time delivery of 97% and two-hour quote turnaround, both better than our main competitors" is strong. Then ask: how do we use strengths to seize opportunities, and which weaknesses expose us to threats?</p>
<h3>Talk to customers</h3>
<p>The best market insight comes from customers. Interview five to ten good customers and a few lost ones each year. Ask why they chose you, what nearly made them switch, what problems they face that you could solve and how they compare you with alternatives. Listen more than you talk.</p>
<h3>Watch competitors and trends</h3>
<p>Track your main competitors' offers, prices, hiring and marketing. Keep an eye on changes in your customers' industries, regulation, technology and costs. Many opportunities and threats are visible early to owners who look.</p>
""", ["Use SWOT with specific, evidence-based points.", "Interview good and lost customers every year.", "Watch competitors, customer industries, technology and regulation."],
 "Run a one-hour SWOT with your leadership team. Then schedule interviews with five customers, including at least one you lost.",
 "Which is a strong SWOT strength statement?", ["We are great", "Good service", "97% on-time delivery and two-hour quote turnaround, better than our main competitors", "We work hard"], 2,
 "Strong SWOT points are specific and backed by evidence."),
step("A one-page plan and annual priorities", 7, """
<p>A strategy that lives in the owner's head cannot guide the team. Capturing it on one page makes it easy to share, review and act on.</p>
<h3>What the one-page plan includes</h3>
<ul><li>Purpose, vision and core values.</li>
<li>Target customers and value proposition.</li>
<li>Three-year targets: revenue, profit and a few key measures.</li>
<li>This year's targets.</li>
<li><strong>Three to five annual priorities:</strong> the projects that move the business toward the vision.</li>
<li>Key measures to track progress.</li></ul>
<h3>Good priorities</h3>
<p>Priorities are specific, measurable, owned and limited. "Grow sales" is a wish. "Win five new customers in the food-processing segment by December, owned by the sales manager" is a priority. Fewer is better: three priorities done well beat ten started.</p>
<h3>Breaking priorities into quarters</h3>
<p>Each annual priority is split into quarterly milestones with owners. Quarterly steps are close enough to feel urgent and long enough to achieve something meaningful. At the end of each quarter, review results, learn and set the next quarter's milestones.</p>
<h3>Share it</h3>
<p>Present the plan to the whole team. People who understand where the business is going make better decisions in their own work and are more likely to bring forward useful ideas.</p>
""", ["Put strategy on one page: purpose, vision, values, customers, targets, priorities, measures.", "Choose three to five specific, owned annual priorities.", "Break priorities into quarterly milestones and share the plan with the team."],
 "Draft your one-page plan. Limit yourself to five annual priorities, each with an owner and a measurable result.",
 "Which is a well-written annual priority?", ["Grow sales", "Improve things", "Win five new customers in the food-processing segment by December, owned by the sales manager", "Be the best"], 2,
 "A good priority is specific, measurable, time-bound and owned."),
step("A management rhythm that keeps plans on track", 7, """
<p>Plans fail without a regular rhythm of review. A simple meeting cadence keeps priorities moving and problems visible.</p>
<table><thead><tr><th>Meeting</th><th>Who</th><th>Length</th><th>Focus</th></tr></thead><tbody>
<tr><td>Daily huddle</td><td>Each team</td><td>10–15 minutes</td><td>Today's work, issues, help needed</td></tr>
<tr><td>Weekly leadership meeting</td><td>Owner and managers</td><td>60–90 minutes</td><td>KPIs, priority progress, issues, decisions</td></tr>
<tr><td>Monthly review</td><td>Leadership</td><td>2–3 hours</td><td>Financials, dashboard, customers, people</td></tr>
<tr><td>Quarterly planning</td><td>Leadership</td><td>Half to one day</td><td>Review the quarter, set next quarter's milestones</td></tr>
<tr><td>Annual planning</td><td>Leadership</td><td>One to two days</td><td>Update the one-page plan, budget and priorities</td></tr>
</tbody></table>
<h3>Running a good weekly meeting</h3>
<ul><li>Same day, same time, start and end on time.</li>
<li>Review KPIs and priority milestones quickly: on track or off track.</li>
<li>Spend most of the time solving the most important issues, one at a time.</li>
<li>End with a list of actions, owners and dates, and review it next week.</li></ul>
<h3>Accountability without blame</h3>
<p>Accountability means each priority, KPI and action has one owner who reports progress honestly. When something is off track, the question is "what do you need?" rather than "whose fault is it?". Owners who model this get earlier warnings and better ideas from their teams.</p>
<p>Start small: a consistent weekly meeting and a quarterly planning session make a big difference in most SMEs.</p>
""", ["Use a rhythm of daily, weekly, monthly, quarterly and annual reviews.", "Run weekly meetings to a fixed agenda that ends with owned actions.", "Hold people accountable by asking what they need, not who is to blame."],
 "Set a fixed day and time for a weekly leadership meeting and draft its agenda. Book your next quarterly planning session.",
 "What should most of a weekly leadership meeting be spent on?", ["Reading reports aloud", "Solving the most important issues, one at a time", "Discussing last year's results", "Social conversation"], 1,
 "KPIs and milestones should be reviewed quickly so most time goes to solving issues."),
]

M4 = [
step("Know your customer and your value proposition", 7, """
<p>Sales and marketing start with a clear answer to two questions: who is the ideal customer, and why should they buy from you?</p>
<h3>The ideal customer profile</h3>
<p>Look at your best customers: profitable, easy to work with, loyal and likely to refer others. What do they have in common? Industry, size, location, the problem they need solved, who makes the buying decision and how they buy. Write this down as an <strong>ideal customer profile</strong>. It guides where to spend marketing money and which leads to chase.</p>
<h3>The value proposition</h3>
<p>A value proposition states the specific result you deliver for your ideal customer and why you are a better choice than the alternatives, including doing nothing. A simple format:</p>
<p><em>For [target customer] who [need or problem], we provide [offering] that [key benefit], unlike [alternative], because [proof].</em></p>
<p>Example: "For food processors in Western Canada who cannot afford unplanned downtime, we provide 24-hour emergency repair of packaging equipment, unlike national service firms with multi-day response times, because our technicians are based within two hours of most plants."</p>
<h3>Benefits over features</h3>
<p>Customers buy outcomes, not features. "Stainless steel construction" is a feature; "passes food-safety inspections and lasts twice as long in wash-down areas" is a benefit. Translate each feature into what it means for the customer's business: less downtime, lower cost, less risk, more revenue, less hassle.</p>
""", ["Define an ideal customer profile from your best existing customers.", "Write a value proposition: who, what problem, what result, why you.", "Sell outcomes and benefits, not features."],
 "Write your ideal customer profile and a value proposition using the format in this lesson. Test it on two customers and one staff member.",
 "Which is a benefit rather than a feature?", ["Stainless steel construction", "A 5 kW motor", "Fewer breakdowns and lower maintenance cost for the customer", "Available in three colours"], 2,
 "A benefit describes the outcome for the customer."),
step("Marketing basics for SMEs", 8, """
<p>Marketing makes the right customers aware of you and willing to talk. For most SMEs, a few channels done consistently beat many done occasionally.</p>
<table><thead><tr><th>Channel</th><th>Good for</th><th>Basics</th></tr></thead><tbody>
<tr><td>Website</td><td>Credibility and enquiries</td><td>Clear statement of what you do and for whom, proof (projects, testimonials), easy contact, fast on phones</td></tr>
<tr><td>Search (SEO)</td><td>Being found when people look</td><td>Pages for each service and location, useful articles answering customer questions, a complete business profile on search and map listings</td></tr>
<tr><td>Referrals and reviews</td><td>Trust</td><td>Ask happy customers for referrals and reviews; make it easy</td></tr>
<tr><td>Email and newsletters</td><td>Staying in touch</td><td>Useful content monthly or quarterly to customers and prospects who opted in</td></tr>
<tr><td>LinkedIn and social media</td><td>B2B visibility</td><td>Regular posts from the owner and team sharing expertise and projects</td></tr>
<tr><td>Trade shows and associations</td><td>Industry relationships</td><td>Pick a few events where ideal customers gather; follow up quickly</td></tr>
<tr><td>Paid ads</td><td>Fast, targeted reach</td><td>Start small, track cost per lead, stop what does not work</td></tr>
</tbody></table>
<h3>Content that helps</h3>
<p>Useful content, such as guides, checklists, calculators and case studies that answer your customers' real questions, builds trust and attracts people searching for answers. It also gives your sales team something valuable to share.</p>
<h3>Measure what matters</h3>
<p>Track where enquiries come from, the cost per lead by channel, and which channels produce customers, not just clicks. Ask every new enquiry how they heard of you. Shift budget toward what works.</p>
<p>When collecting contact details and sending marketing email, follow Canada's anti-spam legislation (CASL): get consent, identify yourself and offer an easy way to unsubscribe.</p>
""", ["Do a few channels consistently: website, search, referrals and one or two others.", "Create useful content that answers customers' questions.", "Track leads and customers by channel and follow CASL for email."],
 "Ask your last 20 new customers how they found you. Rank the channels and decide where to put more effort.",
 "What does CASL require when sending commercial email in Canada?", ["Nothing; email is unregulated", "Consent, sender identification and an easy unsubscribe", "A paper copy of every email", "Government approval of each message"], 1,
 "Canada's anti-spam legislation requires consent, identification and an unsubscribe mechanism."),
step("A sales pipeline and CRM basics", 7, """
<p>A <strong>sales pipeline</strong> shows every opportunity and the stage it has reached. Managing it turns sales from a hopeful activity into a predictable process.</p>
<h3>Typical B2B pipeline stages</h3>
<table><thead><tr><th>Stage</th><th>Exit criterion</th></tr></thead><tbody>
<tr><td>Lead</td><td>Contact identified as a possible fit</td></tr>
<tr><td>Qualified</td><td>Need, budget, decision-maker and timing confirmed</td></tr>
<tr><td>Proposal</td><td>Quote or proposal sent</td></tr>
<tr><td>Negotiation</td><td>Terms being discussed; verbal interest</td></tr>
<tr><td>Won or lost</td><td>Order received or opportunity closed, with the reason recorded</td></tr>
</tbody></table>
<h3>Pipeline numbers</h3>
<p>Track the number and value of opportunities at each stage, the conversion rate between stages and the average time to close. If 25% of proposals become orders, the average order is $20,000 and you need $100,000 of new orders a month, you need about $400,000 of proposals out each month. Working backwards like this shows how much activity the goal really requires.</p>
<h3>A CRM system</h3>
<p>A customer relationship management (CRM) system records contacts, opportunities, activities and follow-ups in one place, instead of in individual inboxes and spreadsheets. Even a simple, affordable CRM helps: nothing falls through the cracks, managers see the pipeline, and customer history stays when a salesperson leaves. The key is discipline: every opportunity and follow-up goes into the CRM.</p>
<h3>Follow up</h3>
<p>Many opportunities are lost simply because nobody followed up. Set a rule: every proposal gets a follow-up within a few days, and every opportunity has a next step and a date.</p>
""", ["Define pipeline stages with clear exit criteria.", "Use conversion rates to work out how much activity a sales goal needs.", "Keep every opportunity and follow-up in a CRM with a next step and date."],
 "List your current open opportunities by stage with values. Calculate your proposal win rate for the last six months and what pipeline you need for next quarter's goal.",
 "The win rate on proposals is 20% and the target is $60,000 of new orders a month. Roughly how much in proposals is needed each month?", ["$12,000", "$60,000", "$120,000", "$300,000"], 3,
 "$60,000 ÷ 20% = $300,000 of proposals."),
step("Your 90-day owner's plan", 7, """
<p>Bring the course together in a 90-day plan that strengthens the business's finances, focus and sales.</p>
<table><thead><tr><th>Days</th><th>Focus</th><th>Actions</th></tr></thead><tbody>
<tr><td>1–30</td><td>Know your numbers</td><td>Monthly statements and review routine; cash conversion cycle; margins by product and customer; break-even; start a 13-week cash forecast</td></tr>
<tr><td>31–60</td><td>Set direction</td><td>SWOT and customer interviews; ideal customer profile and value proposition; one-page plan with three to five priorities; weekly leadership meeting</td></tr>
<tr><td>61–90</td><td>Build the engine</td><td>Monthly KPI dashboard; pipeline stages and CRM discipline; marketing channel review; receivables and pricing actions; first quarterly planning session</td></tr>
</tbody></table>
<h3>Signs of progress</h3>
<ul><li>You know your cash position for the next 13 weeks.</li>
<li>Your team can describe the target customer and this year's priorities.</li>
<li>Weekly meetings end with owned actions that get done.</li>
<li>You can see the sales pipeline and where new customers come from.</li></ul>
<h3>Where to go next</h3>
<p>The Data and Dashboards course helps automate your KPIs; Sales and Operations Planning aligns sales, operations and finance; Inventory Management frees cash tied up in stock; and the Digital Automation course helps you plan technology investments.</p>
<p>Use the self-assessment lab after this lesson to see where the business is strong and where to focus first, and retake it after 90 days.</p>
""", ["Days 1–30: know your numbers and cash.", "Days 31–60: set direction with a one-page plan and weekly meeting.", "Days 61–90: dashboard, pipeline, marketing and quarterly planning."],
 "Put the 90-day plan into your calendar with owners and dates, and book a 90-day review with your leadership team.",
 "Which action belongs in the first 30 days of the plan?", ["Starting a 13-week cash flow forecast", "Writing a ten-year vision", "Launching paid ads everywhere", "Buying a new building"], 0,
 "Knowing your numbers and cash position comes first."),
]

course = dict(
 id="business-basics-for-owners",
 title="Business Basics for Owners: Cash, Costs, Strategy and Sales",
 tagline="Read your numbers, protect cash, price with confidence, set a clear one-page plan and build a sales pipeline that delivers.",
 summary="A practical course for owners and new managers of small and mid-sized businesses. You will learn to read the three financial statements, manage cash and working capital, understand margin, markup and break-even, build a budget and a 13-week cash forecast, choose KPIs and work with lenders and advisers. You will then set strategy with a one-page plan and a management rhythm, and build sales and marketing on a clear customer profile, value proposition and pipeline. It is general business education, not accounting, tax or legal advice.",
 audience=["Owners and founders of small and mid-sized businesses",
           "New general managers and managers stepping into business leadership",
           "Technical professionals, such as engineers and tradespeople, running their own firm",
           "Successors preparing to take over a family business"],
 outcomes=["Read income statements, balance sheets and cash flow statements and spot what matters",
           "Calculate margin, markup, contribution margin, break-even and the cash conversion cycle",
           "Build a budget, a 13-week cash forecast and a monthly KPI dashboard",
           "Set strategy with a SWOT, a one-page plan and quarterly priorities",
           "Define your ideal customer and value proposition and build a sales pipeline",
           "Run a 90-day plan to strengthen finances, focus and sales"],
 modules=[
  dict(title="Know Your Numbers", summary="The three financial statements, profit versus cash, margin, markup and contribution margin, and break-even and pricing.", steps=M1),
  dict(title="Plan and Control", summary="Budgets and 13-week cash forecasts, working capital, KPIs and dashboards, and financing and advisers.", steps=M2),
  dict(title="Strategy", summary="Vision and focus, SWOT and market insight, a one-page plan with annual priorities and a management rhythm.", steps=M3),
  dict(title="Customers and Sales", summary="Ideal customer profile and value proposition, marketing basics, sales pipeline and CRM, and a 90-day owner's plan.", steps=M4)],
 labs=[
  dict(id="biz-which-statement", type="classify", title="Which statement shows it?", after_step=1,
       intro="Match twelve items to the financial statement where you would find them, then check your answers.",
       config=dict(categories=["Income statement", "Balance sheet", "Cash flow statement"], items=[
        dict(text="Revenue for the year", answer=0, why="Revenue over a period appears on the income statement."),
        dict(text="Cost of goods sold", answer=0, why="Cost of goods sold is deducted from revenue on the income statement."),
        dict(text="Wages expense for the quarter", answer=0, why="Operating expenses for a period appear on the income statement."),
        dict(text="Depreciation expense", answer=0, why="Depreciation is an expense on the income statement (and added back in cash from operations)."),
        dict(text="Accounts receivable at year-end", answer=1, why="Amounts customers owe at a date are an asset on the balance sheet."),
        dict(text="Inventory on hand at month-end", answer=1, why="Inventory is a current asset on the balance sheet."),
        dict(text="Bank loan outstanding", answer=1, why="Loans owed are liabilities on the balance sheet."),
        dict(text="Owner's equity", answer=1, why="Equity appears on the balance sheet."),
        dict(text="Cash spent buying a new machine this year", answer=2, why="Purchases of equipment appear under investing activities on the cash flow statement."),
        dict(text="Loan principal repaid during the year", answer=2, why="Principal repayments appear under financing activities on the cash flow statement."),
        dict(text="Cash received from a new bank loan", answer=2, why="Loan proceeds are a financing cash inflow."),
        dict(text="Net change in cash for the year", answer=2, why="The cash flow statement explains the change in cash between two dates."),
       ])),
  dict(id="biz-break-even", type="calc", title="Break-even and target profit calculator", after_step=4,
       intro="Enter your monthly fixed costs, average price and variable cost per unit to see contribution margin, break-even and the sales needed for a target profit.",
       config=dict(calc="break_even", note="Use averages for a product line or the whole business. Variable costs include materials, freight, commissions and other costs that rise with each sale.")),
  dict(id="biz-health-check", type="assessment", title="Business health check", after_step=16,
       intro="Rate your business on eight areas covered in this course. The radar chart shows strengths and gaps, with a next step for each. Retake it after your 90-day plan.",
       config=dict(scale=["Not started", "Ad hoc", "Defined", "Managed", "Optimized"], dimensions=[
        dict(name="Financial reporting", question="Do you receive and review monthly financial statements within a few weeks of month-end?", low="Ask your bookkeeper for monthly statements and set a review meeting each month.", high="Compare with budget and last year, and track a few ratios such as gross margin and DSO."),
        dict(name="Cash management", question="Do you run a rolling cash forecast and manage receivables, inventory and payables actively?", low="Build a 13-week cash forecast and review aged receivables weekly.", high="Set cash conversion cycle targets and review them monthly."),
        dict(name="Pricing and margins", question="Do you know your margins by product and customer and review prices regularly?", low="Calculate margins for your top products and customers.", high="Use contribution margin for discount decisions and review prices yearly."),
        dict(name="Budget and KPIs", question="Do you have an annual budget and a monthly KPI dashboard with owners and targets?", low="Draft a simple budget and pick 8 to 12 KPIs.", high="Include leading indicators and act on anything off target each month."),
        dict(name="Strategy", question="Is your strategy written on one page with three to five owned annual priorities?", low="Run a SWOT and draft a one-page plan.", high="Review the plan quarterly and share progress with the team."),
        dict(name="Management rhythm", question="Do you hold consistent weekly, monthly and quarterly meetings that end with owned actions?", low="Start a weekly leadership meeting with a fixed agenda.", high="Add quarterly planning and track action completion."),
        dict(name="Marketing", question="Do you know where customers come from and invest consistently in the channels that work?", low="Ask every new customer how they found you and track it.", high="Measure cost per lead and per customer by channel and shift budget accordingly."),
        dict(name="Sales pipeline", question="Do you manage a pipeline with clear stages, conversion rates and CRM discipline?", low="List open opportunities by stage and put them in a CRM.", high="Use conversion rates to plan activity and review the pipeline weekly."),
       ])),
 ],
 figures=[
  dict(step=2, type="cycle", title="The cash conversion cycle", caption="Click each stage to see where cash is tied up between paying suppliers and collecting from customers.",
       config=dict(center="Cash", stages=[
        dict(label="Buy", text="Purchase materials or goods; supplier terms give you time to pay (DPO)."),
        dict(label="Hold", text="Inventory waits to be used or sold (DIO)."),
        dict(label="Sell", text="Deliver to the customer and invoice."),
        dict(label="Collect", text="Customer pays after their terms (DSO)."),
        dict(label="Reinvest", text="Cash pays suppliers, wages and the next purchase.")])),
  dict(step=6, type="bars", title="Days of cash tied up: an example", caption="DSO 45 + DIO 60 − DPO 30 = a 75-day cash conversion cycle. Cutting any of the first two, or extending the third, frees cash.",
       config=dict(unit="days", items=[dict(label="Days sales outstanding (DSO)", value=45, highlight=True), dict(label="Days inventory outstanding (DIO)", value=60, highlight=True), dict(label="Days payables outstanding (DPO)", value=30), dict(label="Cash conversion cycle", value=75)],
        note="For $3 million of annual cost of sales, each day cut from the cycle frees roughly $8,000 of cash.")),
  dict(step=8, type="compare", title="Debt vs equity", caption="Toggle between the two and compare what each costs the owner.",
       config=dict(left=dict(title="Debt", points=["Must be repaid with interest", "Owner keeps full ownership", "Needs repayment ability and often security", "Suits predictable needs such as equipment"]),
                   right=dict(title="Equity", points=["No fixed repayment", "Gives up part of ownership and future profits", "Investor may add expertise and contacts", "Suits large, riskier growth"]))),
  dict(step=11, type="stack", title="The one-page plan", caption="Click each layer, from the bottom up, to see how the plan builds from purpose to this quarter's actions.",
       config=dict(top_label="This quarter's milestones", layers=[
        dict(label="Purpose and values", text="Why the business exists and the behaviours you expect."),
        dict(label="Vision and targets", text="Where the business will be in three years, in numbers."),
        dict(label="Customers and value", text="Who you serve and why they choose you."),
        dict(label="Annual priorities", text="Three to five owned projects that move you toward the vision."),
        dict(label="Quarterly milestones", text="The steps each owner will finish this quarter.")])),
  dict(step=15, type="flow", title="A B2B sales pipeline", caption="Click each stage to see its exit criterion. Every opportunity needs a next step and a date.",
       config=dict(steps=[
        dict(label="Lead", text="A contact identified as a possible fit."),
        dict(label="Qualified", text="Need, budget, decision-maker and timing confirmed."),
        dict(label="Proposal", text="Quote or proposal sent, with a follow-up date."),
        dict(label="Negotiation", text="Terms discussed; verbal interest."),
        dict(label="Won or lost", text="Order received, or closed with the reason recorded.")])),
  dict(step=16, type="timeline", title="A 90-day owner's plan", caption="Click each phase to see its main actions.",
       config=dict(phases=[
        dict(label="Days 1–30", title="Know your numbers", items=["Monthly statements and review", "Margins and break-even", "13-week cash forecast"]),
        dict(label="Days 31–60", title="Set direction", items=["SWOT and customer interviews", "Value proposition", "One-page plan", "Weekly leadership meeting"]),
        dict(label="Days 61–90", title="Build the engine", items=["KPI dashboard", "Pipeline and CRM", "Marketing review", "Quarterly planning"])])),
 ],
 exam=[
  E("Which statement shows profit over a period?", ["Income statement", "Balance sheet", "Cash flow statement", "Aged receivables report"], 0, "The income statement reports revenue, expenses and profit for a period."),
  E("A business borrows $50,000. What happens on the balance sheet?", ["Equity rises by $50,000", "Cash and liabilities both rise by $50,000", "Revenue rises by $50,000", "Nothing changes"], 1, "Assets and liabilities rise equally; equity is unchanged."),
  E("Why can a profitable business run out of cash?", ["Profit is always equal to cash", "Taxes are never due", "Cash is tied up in receivables, inventory, equipment and loan repayments", "Banks hold profits for a year"], 2, "Timing differences and non-expense uses of cash separate profit from cash."),
  E("DSO is 30 days, DIO is 50 days and DPO is 40 days. What is the cash conversion cycle?", ["120 days", "80 days", "60 days", "40 days"], 3, "CCC = 30 + 50 − 40 = 40 days."),
  E("An item costs $60 and sells for $100. What is the markup?", ["About 66.7%", "40%", "60%", "100%"], 0, "Markup = $40 ÷ $60 ≈ 66.7%."),
  E("What price gives a 25% gross margin on an item costing $75?", ["$93.75", "$100", "$90", "$125"], 1, "Price = $75 ÷ (1 − 0.25) = $100."),
  E("Which cost is usually fixed over a month?", ["Materials for each order", "Sales commission", "Office rent", "Freight per shipment"], 2, "Rent stays the same regardless of volume within a period."),
  E("Fixed costs are $24,000 a month, price $50 and variable cost $30. What is break-even volume?", ["480 units", "800 units", "2,000 units", "1,200 units"], 3, "Contribution margin $20; 24,000 ÷ 20 = 1,200 units."),
  E("What is the main purpose of a 13-week cash flow forecast?", ["To see cash low points early enough to act", "To calculate income tax", "To replace financial statements", "To set product prices"], 0, "A rolling weekly forecast reveals shortfalls in time to respond."),
  E("Which action shortens days sales outstanding?", ["Paying suppliers early", "Invoicing promptly and following up overdue accounts", "Buying more inventory", "Extending customer terms"], 1, "Faster, accurate invoicing and follow-up get cash in sooner."),
  E("What is a leading indicator?", ["Last year's net income", "Total taxes paid", "A measure that predicts future results, such as pipeline value", "The bank balance on December 31"], 2, "Leading indicators signal results before they appear."),
  E("Why should long-term assets not be funded with the operating line of credit?", ["It is illegal", "Lines of credit have no interest", "Assets must be paid in cash", "It leaves no room for normal working capital swings"], 3, "Short-term credit should cover short-term needs."),
  E("What is a key trade-off of equity financing?", ["You give up part of ownership and future profits", "It must be repaid monthly", "It always costs less than debt", "It requires no investor involvement"], 0, "Equity investors share ownership and profits."),
  E("How do most small businesses compete successfully?", ["Lowest price on everything", "By specializing in a niche, region, service level or expertise", "Serving every possible customer", "Copying large competitors"], 1, "Specialization creates value large firms cannot match."),
  E("In a SWOT, which item is an external opportunity?", ["Strong engineering team", "Old IT systems", "A competitor exiting your region", "High staff turnover"], 2, "Opportunities come from outside the business."),
  E("How many annual priorities does the course recommend?", ["As many as possible", "One", "Ten to fifteen", "Three to five"], 3, "Fewer, owned priorities are more likely to be completed."),
  E("What should end every weekly leadership meeting?", ["A list of actions with owners and dates", "A long financial presentation", "A vote on next year's budget", "A review of every customer"], 0, "Owned actions turn discussion into progress."),
  E("Which statement is a benefit rather than a feature?", ["Powder-coated finish", "Reduces the customer's downtime and maintenance costs", "Available in 12 sizes", "Made with a 3 kW motor"], 1, "Benefits describe customer outcomes."),
  E("What does Canada's anti-spam legislation (CASL) require for commercial email?", ["Nothing", "Approval from a regulator for each email", "Consent, sender identification and an easy unsubscribe", "Sending only on weekdays"], 2, "CASL requires consent, identification and unsubscribe options."),
  E("The proposal win rate is 25% and the target is $50,000 of new orders a month. How much in proposals is needed?", ["$12,500", "$50,000", "$100,000", "$200,000"], 3, "$50,000 ÷ 25% = $200,000."),
 ],
)

if __name__ == "__main__":
    write(course, "business-basics", __file__, balance=True)
