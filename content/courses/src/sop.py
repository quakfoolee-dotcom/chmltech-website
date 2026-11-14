"""Source for content/courses/sop.json (run: python3 content/courses/src/sop.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import step, E, write

M1 = [
step("What S&OP is and the problems it solves", 6, """
<p><strong>Sales and operations planning (S&amp;OP)</strong> is a monthly management process that brings sales, operations, purchasing and finance together to agree one plan for the coming months, balancing demand, supply and money.</p>
<h3>The problems it solves</h3>
<ul><li><strong>Several plans:</strong> sales forecasts one number, operations plans another, purchasing buys to a third and finance budgets a fourth.</li>
<li><strong>Surprises:</strong> peaks and shortages discovered too late to respond without expediting, overtime or lost orders.</li>
<li><strong>Too much and too little inventory at the same time:</strong> excess of some items, shortages of others.</li>
<li><strong>Firefighting:</strong> managers spend their time reacting instead of planning.</li>
<li><strong>Cash surprises:</strong> inventory builds or capacity spending that finance did not see coming.</li></ul>
<h3>What S&amp;OP is not</h3>
<p>S&amp;OP is not detailed production scheduling or item-by-item purchasing. It works at the level of <strong>product families</strong> and months, looking typically 3 to 18 months ahead. Detailed plans follow from it.</p>
<h3>The benefits</h3>
<p>Companies that run S&amp;OP well typically report better customer service, lower and better-balanced inventory, steadier production, fewer expedites and more confidence in financial forecasts. The biggest change is often cultural: departments work to one shared plan and resolve trade-offs openly, with the leader deciding.</p>
<p>The term <strong>integrated business planning (IBP)</strong> is often used for a more mature form of S&amp;OP that ties the plan more tightly to financial and strategic planning. For most SMEs, a disciplined monthly S&amp;OP is the right place to start.</p>
""", ["S&OP aligns sales, operations, purchasing and finance on one monthly plan.", "It works with product families and months, typically 3 to 18 months ahead.", "It reduces surprises, balances inventory and builds trust in one plan."],
 "List three surprises in the past six months, such as a shortage, a peak or a cash squeeze, that an agreed monthly plan might have flagged earlier.",
 "At what level does S&OP usually plan?", ["Individual items by day", "Product families by month", "Each machine by hour", "Each customer order"], 1,
 "S&OP works at aggregate family and monthly levels; detailed planning follows."),
step("Planning levels, horizons and product families", 7, """
<p>S&amp;OP sits in a hierarchy of plans, each with its own level of detail and horizon.</p>
<table><thead><tr><th>Plan</th><th>Detail</th><th>Horizon</th><th>Typical owner</th></tr></thead><tbody>
<tr><td>Strategic or business plan</td><td>Company, markets, revenue and profit</td><td>1–5 years</td><td>Owner and leadership</td></tr>
<tr><td>S&amp;OP</td><td>Product families, units and dollars by month</td><td>3–18 months</td><td>Leadership team</td></tr>
<tr><td>Master production schedule or purchasing plan</td><td>Items by week</td><td>Weeks to a few months</td><td>Planning</td></tr>
<tr><td>Detailed schedule</td><td>Orders by day or shift</td><td>Days to weeks</td><td>Operations</td></tr>
</tbody></table>
<h3>Choosing product families</h3>
<p>A product family groups items that share demand patterns and, ideally, the same production resources or suppliers. Good families let you plan demand and capacity together. Most SMEs need between 5 and 15 families; more makes the meeting unmanageable, fewer hides important differences.</p>
<p>Examples: a cabinet maker might use families such as kitchen cabinets, bathroom vanities and custom projects; a distributor might group by product category and main supplier.</p>
<h3>Units and dollars</h3>
<p>Plan in units (or another physical measure such as tonnes or hours) for operations, and convert to dollars for finance. Both views must agree.</p>
<h3>Time fences</h3>
<p>Near-term plans are harder to change because materials are ordered and schedules set. Many companies define a <strong>frozen</strong> period, often a few weeks, where changes need special approval, followed by a <strong>slushy</strong> zone with limited changes and a <strong>liquid</strong> zone where S&amp;OP can change plans freely.</p>
""", ["S&OP sits between the strategic plan and detailed schedules.", "Plan 5 to 15 product families that share demand patterns and resources.", "Use units for operations, dollars for finance, and time fences to control changes."],
 "Draft a list of 5 to 15 product families for your business. For each, note the main production resource or supplier it depends on.",
 "What makes a good product family for S&OP?", ["Items with the same colour", "Items that share demand patterns and production resources or suppliers", "Every item on its own", "Items sold by the same salesperson only"], 1,
 "Families that share demand and resources let you plan demand and capacity together."),
step("The monthly S&OP cycle", 8, """
<p>S&amp;OP runs as a monthly cycle of steps, each feeding the next.</p>
<table><thead><tr><th>Step</th><th>Timing</th><th>Who</th><th>Output</th></tr></thead><tbody>
<tr><td>1. Data gathering</td><td>Working days 1–3</td><td>Planning, finance</td><td>Last month's actuals, forecast accuracy, inventory and backlog by family</td></tr>
<tr><td>2. Demand review</td><td>Week 1–2</td><td>Sales, marketing, planning</td><td>Updated demand plan by family with assumptions and risks</td></tr>
<tr><td>3. Supply review</td><td>Week 2</td><td>Operations, purchasing, planning</td><td>Supply plan and capacity check against demand; constraints and options</td></tr>
<tr><td>4. Pre-S&amp;OP (reconciliation)</td><td>Week 3</td><td>Department heads, finance</td><td>Resolved issues, scenarios for unresolved trade-offs, financial view</td></tr>
<tr><td>5. Executive S&amp;OP</td><td>Week 3–4</td><td>Owner or general manager and leadership</td><td>Decisions on trade-offs; approved plan</td></tr>
</tbody></table>
<h3>How it flows</h3>
<p>Each step resolves what it can and passes only the unresolved issues upward. By the time the executive meeting happens, most issues are settled and the leadership spends its time on a few real trade-offs: for example, whether to add a shift, build inventory ahead of a peak or accept a large order with a tight deadline.</p>
<h3>For small companies</h3>
<p>In a small business, the five steps may compress into two meetings: a working meeting that combines the demand and supply reviews, and a short leadership decision meeting. The discipline of reviewing demand, checking supply and deciding trade-offs each month matters more than the number of meetings. The lab after this lesson asks you to match issues to the right step.</p>
""", ["S&OP runs monthly: data, demand review, supply review, pre-S&OP, executive meeting.", "Each step resolves what it can and passes trade-offs upward.", "Small companies can compress the steps into two meetings."],
 "Draft your monthly S&OP calendar: which working days each step happens and who attends.",
 "What should the executive S&OP meeting mainly spend its time on?", ["Reviewing every item's forecast", "Deciding a few trade-offs that could not be resolved earlier", "Scheduling tomorrow's production", "Data entry"], 1,
 "Earlier steps resolve most issues; leaders decide the remaining trade-offs."),
step("Roles, ownership and starting small", 7, """
<p>S&amp;OP succeeds when the leader owns it and each function brings honest input.</p>
<h3>Roles</h3>
<table><thead><tr><th>Role</th><th>Contribution</th></tr></thead><tbody>
<tr><td>Owner or general manager</td><td>Chairs the executive meeting, makes trade-off decisions, insists on one plan</td></tr>
<tr><td>S&amp;OP coordinator (often a planner)</td><td>Runs the calendar, prepares data and the meeting pack, tracks actions</td></tr>
<tr><td>Sales and marketing</td><td>Own the demand plan and its assumptions</td></tr>
<tr><td>Operations and purchasing</td><td>Own the supply plan, capacity and material constraints</td></tr>
<tr><td>Finance</td><td>Converts plans to dollars, checks against budget and cash</td></tr>
</tbody></table>
<h3>Getting started</h3>
<ol><li>Get the leader's commitment to chair the monthly meeting.</li>
<li>Define product families and gather 12 to 24 months of history by family.</li>
<li>Build a simple spreadsheet: demand, supply, inventory and backlog by family by month.</li>
<li>Run the first cycle, imperfect as it will be.</li>
<li>Improve a little each month: better forecasts, capacity data and financial views.</li></ol>
<h3>Common pitfalls</h3>
<ul><li>The leader delegates the meeting and decisions drift.</li>
<li>Too much detail: reviewing items instead of families.</li>
<li>Sales treats the forecast as a target or a hope rather than an honest estimate.</li>
<li>Meetings report numbers but make no decisions.</li></ul>
<p>Expect it to take several monthly cycles before the process feels natural and the benefits are clear.</p>
""", ["The leader must own and chair S&OP.", "Start with families, history and a simple spreadsheet, then improve monthly.", "Avoid delegation, excess detail, forecasts used as targets and meetings without decisions."],
 "Name the people for each S&OP role in your business and set the date of your first monthly cycle.",
 "What is a common reason S&OP efforts fail?", ["Using a spreadsheet", "The leader delegates the meeting and decisions drift", "Planning by family", "Meeting monthly"], 1,
 "Leadership ownership is essential for decisions and discipline."),
]

M2 = [
step("Building the demand plan", 8, """
<p>The demand plan is the best estimate of what customers will buy, by family and month. It is an honest forecast, not a sales target or budget.</p>
<h3>Two inputs</h3>
<ol><li><strong>Statistical baseline:</strong> a forecast from history, using methods such as moving averages, exponential smoothing and seasonal indices.</li>
<li><strong>Market intelligence:</strong> what the history cannot know: new customers, lost accounts, price changes, promotions, competitor moves, economic conditions and large projects.</li></ol>
<p>Start with the baseline, then adjust it for known events, recording each adjustment and its reason.</p>
<h3>Assumptions and risks</h3>
<p>Every demand plan rests on assumptions, such as "Customer X places its annual order in March" or "the housing market stays flat". Write them down. List risks and opportunities with rough sizes and probabilities, such as "a 30% chance of a new contract worth 2,000 units a month from September".</p>
<h3>Unconstrained demand</h3>
<p>The demand plan should show what customers want, not what you think you can supply. If demand exceeds capacity, that gap is exactly what the supply review and executive meeting need to see and decide on. Hiding demand to match capacity removes the chance to respond.</p>
<h3>Forecast, budget and target</h3>
<table><thead><tr><th>Number</th><th>Purpose</th></tr></thead><tbody>
<tr><td>Forecast (demand plan)</td><td>Honest best estimate, updated monthly</td></tr>
<tr><td>Budget</td><td>Financial plan for the year, fixed at the start</td></tr>
<tr><td>Sales target</td><td>Stretch goal to motivate the sales team</td></tr>
</tbody></table>
<p>Mixing them causes trouble: forecasting to the target builds excess inventory; forecasting to the budget hides changes in the market.</p>
""", ["Combine a statistical baseline with market intelligence and record adjustments.", "Write down assumptions and size risks and opportunities.", "Show unconstrained demand and keep forecasts separate from budgets and targets."],
 "For your largest product family, write the baseline forecast for the next six months, list three assumptions and one risk and one opportunity with rough sizes.",
 "Why should the demand plan show unconstrained demand?", ["To make sales look good", "So gaps between demand and capacity are visible and can be decided on", "Because capacity never matters", "To avoid forecasting"], 1,
 "Showing true demand lets leaders decide how to respond to capacity gaps."),
step("Forecast accuracy, bias and consensus", 7, """
<p>Measuring forecast performance builds trust and shows where to improve.</p>
<h3>Accuracy and bias</h3>
<ul><li><strong>Accuracy</strong> measures the size of errors, for example mean absolute percentage error (MAPE) by family, or a weighted measure that gives large families more weight.</li>
<li><strong>Bias</strong> measures the direction: consistently over- or under-forecasting. Track the sum of errors with their signs over several months.</li></ul>
<p>Bias is often more damaging than random error because it accumulates: steady over-forecasting builds excess inventory month after month; steady under-forecasting causes repeated shortages.</p>
<h3>Measure at the right lag</h3>
<p>Measure the forecast made at the point when supply decisions are locked, such as the forecast made two months ahead if your lead time is two months. Measuring last week's forecast for this week flatters accuracy and says little about the plan you actually acted on.</p>
<h3>Forecast value added</h3>
<p>Compare the accuracy of the statistical baseline with the final forecast after adjustments. If adjustments make the forecast worse, which is common, review who adjusts and why. Keep adjustments that add value and stop those that don't.</p>
<h3>Consensus</h3>
<p>The demand review ends with one agreed demand plan that sales, marketing and planning stand behind. Disagreements are resolved by discussing assumptions and evidence, not by averaging opinions. Where a real difference remains, show it as a scenario for the executive meeting.</p>
""", ["Track accuracy for size and bias for direction; bias accumulates.", "Measure at the lag when supply decisions are locked.", "Check whether adjustments add value and agree one consensus plan."],
 "Calculate MAPE and bias for your top three families over the last six months, using forecasts made at your typical lead time.",
 "A family's forecast has been higher than actual demand in 10 of the last 12 months. What does this show?", ["Low accuracy only", "Positive bias that builds excess inventory", "A perfect forecast", "Random error that will cancel out"], 1,
 "Consistent over-forecasting is bias, which accumulates as excess stock."),
step("Big customers, promotions and new products", 7, """
<p>Some demand is lumpy or unusual and needs special handling in the demand plan.</p>
<h3>Large customers</h3>
<p>When a few customers make up a large share of demand, plan them individually. Ask for their forecasts, share yours, and agree how far ahead firm orders arrive. Collaborative planning with key customers often improves accuracy more than any forecasting method.</p>
<h3>Projects and one-off orders</h3>
<p>Treat large project orders separately from the baseline so they don't distort history. Track them as named opportunities with probabilities and expected timing, and include them in the plan when they reach an agreed probability or are confirmed.</p>
<h3>Promotions and price changes</h3>
<p>Promotions shift demand: a lift during the promotion and often a dip afterwards as customers stocked up. Record past promotion effects to estimate future ones, and agree promotion calendars with operations early.</p>
<h3>New products and phase-outs</h3>
<ul><li><strong>New products:</strong> with no history, forecast using similar past launches, customer commitments and market estimates. Review weekly at first and plan supply flexibly.</li>
<li><strong>Phase-outs:</strong> agree the last date to sell, plan the run-down of inventory and stop purchasing in time to avoid obsolete stock.</li></ul>
<h3>Product lifecycle review</h3>
<p>Many companies add a short product review at the start of the S&amp;OP cycle covering launches, changes and phase-outs, so demand and supply plans reflect them from the start.</p>
""", ["Plan large customers individually and collaborate with them.", "Keep projects and promotions separate from the baseline with probabilities and timing.", "Forecast new products from analogues and plan phase-outs to avoid obsolete stock."],
 "List your five largest customers and decide which you could share forecasts with. Draft the questions you would ask each.",
 "How should a large one-off project order be treated in the demand plan?", ["Hidden from planners", "Separately from the baseline, with probability and timing", "Added to the history as normal demand", "Ignored until it ships"], 1,
 "Separating projects keeps the baseline clean and makes their risk visible."),
step("The demand review meeting", 7, """
<p>The demand review turns inputs into the agreed demand plan for the month.</p>
<h3>Agenda (60 to 90 minutes)</h3>
<ol><li>Last month's actual demand versus forecast by family; accuracy and bias.</li>
<li>Changes in the market and key customers since last month.</li>
<li>The updated plan by family for the next 3 to 18 months, with changes highlighted.</li>
<li>Assumptions, risks and opportunities.</li>
<li>New products, promotions and phase-outs.</li>
<li>Agreement on the plan and issues to pass to the supply review.</li></ol>
<h3>Focus on change and exceptions</h3>
<p>Don't review every family in detail every month. Focus on families where the forecast changed significantly, where accuracy or bias is poor, or where big risks and opportunities exist.</p>
<h3>A simple display</h3>
<p>For each family, a chart showing the last 12 months of actuals, last month's forecast and the new forecast for the coming months, with last year for comparison, makes changes obvious. Add a table of the numbers and key assumptions.</p>
<h3>Output</h3>
<p>The agreed demand plan goes to the supply review. Sales owns it and should be able to explain each number. Any unresolved disagreement goes forward as a scenario, such as "base case" and "if the new contract is won".</p>
""", ["Review accuracy, market changes, the updated plan, assumptions and product changes.", "Focus on families with big changes, poor accuracy or major risks.", "Sales owns the agreed plan; unresolved differences become scenarios."],
 "Prepare a one-page demand review chart for one family: 12 months of actuals, last month's forecast, the new forecast and last year.",
 "Who owns the agreed demand plan?", ["Purchasing", "Sales (with marketing and planning)", "The warehouse", "IT"], 1,
 "Sales is closest to customers and owns the demand plan and its assumptions."),
]

M3 = [
step("Rough-cut capacity planning", 8, """
<p>The supply review checks whether the demand plan can be met with the capacity and materials available. <strong>Rough-cut capacity planning</strong> does this at family level, focusing on the few resources that limit output.</p>
<h3>The method</h3>
<ol><li>Identify the critical resources: the bottleneck machine or line, key skilled labour, a supplier with limited capacity, warehouse space.</li>
<li>For each family, estimate how much of each critical resource one unit requires, such as hours per 100 units.</li>
<li>Multiply planned volumes by these rates to get the load on each resource by month.</li>
<li>Compare load with available capacity, allowing for realistic efficiency (OEE), holidays and planned maintenance.</li></ol>
<h3>Example</h3>
<p>A family's plan is 15,000 units in October. The bottleneck line's ideal rate is 60 units an hour and it runs at about 70% OEE, so it effectively makes 42 units an hour. It needs about 357 hours, but only 320 are available on two shifts. That is a shortfall of about 37 hours, roughly 1,550 units, which the supply review must address.</p>
<h3>Look ahead</h3>
<p>A load chart showing demand against capacity for each month of the horizon reveals peaks long before they arrive. A peak in four months may be met by building inventory now, scheduling overtime or arranging outsourcing; discovered in the same month, it means lost orders or expensive expediting.</p>
<p>The lab after this lesson calculates load, shortfall and maximum output for a family and resource.</p>
""", ["Check load against capacity for the few critical resources.", "Use realistic efficiency, holidays and maintenance in available capacity.", "Look months ahead so peaks can be handled calmly."],
 "Identify your two most critical resources and estimate next quarter's load on each from your demand plan. Mark any month over 90% load.",
 "Why must available capacity allow for realistic efficiency such as OEE?", ["It makes the plan look better", "Equipment rarely runs at its ideal rate all the time, so ideal capacity overstates what can be made", "OEE is only for accounting", "It is a legal requirement"], 1,
 "Planning at ideal rate overstates output and hides real shortfalls."),
step("Supply options: level, chase and in between", 7, """
<p>When demand and capacity don't match month by month, there are several ways to respond.</p>
<h3>Two basic strategies</h3>
<table><thead><tr><th>Strategy</th><th>How it works</th><th>Pros</th><th>Cons</th></tr></thead><tbody>
<tr><td>Level</td><td>Produce at a steady rate; inventory absorbs the peaks and valleys</td><td>Stable workforce, efficient operations</td><td>Inventory carrying cost; risk if demand changes</td></tr>
<tr><td>Chase</td><td>Change production to match demand each month</td><td>Low inventory</td><td>Overtime, hiring and layoffs, idle time, quality risk</td></tr>
</tbody></table>
<p>Most businesses use a mix: a fairly level base rate with some flexibility for peaks.</p>
<h3>Ways to add capacity</h3>
<ul><li>Overtime or extra shifts, short term.</li>
<li>Temporary staff or cross-trained employees.</li>
<li>Outsourcing or subcontracting some work.</li>
<li>Improving OEE on the bottleneck.</li>
<li>Building inventory ahead of the peak.</li>
<li>Longer term: new equipment, a new line or more space.</li></ul>
<h3>Ways to manage demand</h3>
<ul><li>Agree delivery dates with customers to smooth the load.</li>
<li>Offer incentives for off-peak orders.</li>
<li>Prioritize the most profitable or strategic customers when capacity is short.</li></ul>
<h3>Present options with their costs</h3>
<p>The supply review shouldn't simply say "we can't do it". It should present options with their costs and service effects, for example: overtime for 37 hours at a given cost, building 1,500 units in August at a given carrying cost, or delaying some orders with a given risk to customer relationships.</p>
""", ["Level strategies use inventory; chase strategies change output each month.", "Add capacity with overtime, staff, outsourcing, OEE gains or pre-builds.", "Present options with costs and service effects, not just 'we can't'."],
 "For your peak month, list three ways to close a capacity gap and estimate the cost and service effect of each.",
 "What is the main drawback of a pure chase strategy?", ["High inventory", "Frequent changes in staffing and overtime, with idle time and quality risk", "No flexibility", "Lower customer service"], 1,
 "Chasing demand means constant changes in labour and capacity."),
step("Materials and suppliers", 7, """
<p>Capacity is not only internal. Materials and suppliers can constrain the plan just as much as machines and people.</p>
<h3>Critical materials</h3>
<p>Identify materials and components that are long lead time, single-sourced, capacity-limited at the supplier or volatile in price. Check planned demand for them against supplier capacity and lead times each month.</p>
<h3>Share the plan</h3>
<p>Share family-level forecasts with key suppliers for the next three to six months. Suppliers who see your plan can reserve capacity and materials. Agree how firm each part of the forecast is: for example, the next month firm, months two and three flexible within 20%, beyond that indicative.</p>
<h3>Long lead times</h3>
<p>For items with lead times longer than your firm order window, S&amp;OP decisions effectively commit purchases. Make sure the supply review flags these, so the executive meeting understands which decisions lock in spending.</p>
<h3>Supply risk</h3>
<p>List the main supply risks with likelihood and impact: a single supplier, a long ocean shipment, a commodity price swing. Agree mitigation: a second source, safety stock, a forward purchase or an alternate material. Review the list at each supply review.</p>
""", ["Identify long-lead, single-source and capacity-limited materials.", "Share forecasts with key suppliers and agree how firm each horizon is.", "Flag decisions that commit long-lead purchases and review supply risks monthly."],
 "List your five most critical materials or components, with lead times and suppliers. Mark single-source items and decide a mitigation for each.",
 "Why share family-level forecasts with key suppliers?", ["To reduce prices automatically", "So they can reserve capacity and materials for your needs", "It is required by law", "To avoid placing orders"], 1,
 "Visibility lets suppliers plan capacity and materials ahead."),
step("Inventory and backlog targets by family", 7, """
<p>S&amp;OP plans inventory and backlog by family, not just production. The plan shows how they will move month by month.</p>
<h3>Make-to-stock families</h3>
<p>For families sold from stock, the plan balances demand and production to reach a <strong>target inventory</strong>, often expressed in days of supply:</p>
<p><strong>Ending inventory = beginning inventory + production − demand</strong></p>
<p>If the plan shows inventory falling below target ahead of a peak, production must rise earlier; if it climbs well above, production should slow.</p>
<h3>Make-to-order families</h3>
<p>For families made to order, the equivalent measure is the <strong>backlog</strong> of orders waiting: a healthy backlog gives a steady workload; a growing backlog means lead times are stretching; a shrinking one means capacity may sit idle.</p>
<p><strong>Ending backlog = beginning backlog + new orders − shipments</strong></p>
<h3>Setting targets</h3>
<p>Set inventory targets by family from service level needs, demand variability and supply lead times, using the methods in the Inventory Management for SMEs course. Set backlog targets from the lead time customers accept. Review targets quarterly.</p>
<h3>A simple S&amp;OP sheet</h3>
<table><thead><tr><th>Family A (units)</th><th>Jul</th><th>Aug</th><th>Sep</th><th>Oct</th></tr></thead><tbody>
<tr><td>Demand plan</td><td>10,000</td><td>11,000</td><td>13,000</td><td>15,000</td></tr>
<tr><td>Production plan</td><td>12,000</td><td>12,500</td><td>13,000</td><td>13,400</td></tr>
<tr><td>Ending inventory (start 6,000)</td><td>8,000</td><td>9,500</td><td>9,500</td><td>7,900</td></tr>
</tbody></table>
<p>Building inventory in July and August covers the October peak that exceeds capacity.</p>
""", ["Plan inventory for make-to-stock and backlog for make-to-order families.", "Ending inventory = beginning + production − demand.", "Set targets from service, variability and lead times; review quarterly."],
 "Build a four-month S&OP sheet for one family with demand, production and ending inventory or backlog. Check it against your target.",
 "Beginning inventory is 4,000, production is 9,000 and demand is 10,000. What is ending inventory?", ["3,000", "5,000", "13,000", "23,000"], 0,
 "4,000 + 9,000 − 10,000 = 3,000."),
]

M4 = [
step("The financial view", 7, """
<p>S&amp;OP becomes a management process, not just a planning exercise, when the plan is expressed in money.</p>
<h3>Converting volume to dollars</h3>
<p>Finance multiplies planned volumes by average prices and costs by family to show:</p>
<ul><li>Revenue by month and family.</li>
<li>Gross margin.</li>
<li>Inventory value and its change.</li>
<li>Capacity costs: overtime, temporary labour, outsourcing.</li>
<li>Cash effects of inventory builds and capital spending.</li></ul>
<h3>Compare with budget</h3>
<p>Show the S&amp;OP plan against the annual budget. Gaps are not failures; they are early warnings. If demand is running below budget, leadership can decide to push sales, cut costs or accept a lower result months before year-end. If above budget, capacity and cash may need attention.</p>
<h3>The latest estimate</h3>
<p>Combining year-to-date actuals with the S&amp;OP plan for the remaining months gives a rolling <strong>latest estimate</strong> of the year's results, usually far more reliable than the original budget by mid-year.</p>
<h3>Price the options</h3>
<p>When the supply review presents options, finance adds their effect on margin and cash. Choosing between overtime and an inventory build becomes a clear comparison: extra labour cost against carrying cost and risk.</p>
""", ["Convert the volume plan into revenue, margin, inventory value, capacity costs and cash.", "Compare with budget to get early warnings, not to assign blame.", "Use a rolling latest estimate and price each supply option."],
 "Convert next quarter's plan for your largest family into revenue, gross margin and inventory value, and compare it with the budget.",
 "Why compare the S&OP plan with the budget each month?", ["To punish the sales team", "To get early warning of gaps so leaders can act months before year-end", "To replace the budget entirely", "Because auditors require it"], 1,
 "Gaps signal where action is needed while there is still time."),
step("Pre-S&OP: resolve issues and prepare scenarios", 7, """
<p>The pre-S&amp;OP meeting is the working session that prepares the executive meeting. Its job is to resolve what can be resolved and frame the rest as clear decisions.</p>
<h3>Agenda</h3>
<ol><li>Review the demand and supply plans and the financial view.</li>
<li>Resolve imbalances within the team's authority, such as shifting production between months or using approved overtime.</li>
<li>For issues that need leadership decisions, prepare scenarios with costs, risks and recommendations.</li>
<li>Check performance measures and open actions.</li>
<li>Prepare the executive meeting pack.</li></ol>
<h3>Good scenarios</h3>
<p>Present two or three options for each decision, each with:</p>
<ul><li>What happens to customer service.</li>
<li>Cost and margin effect.</li>
<li>Inventory and cash effect.</li>
<li>Risks and assumptions.</li>
<li>A recommendation.</li></ul>
<p>Example: "October demand exceeds capacity by about 1,550 units. Option A: build ahead in July–August (carrying cost and some obsolescence risk). Option B: Saturday overtime in September–October (labour cost; fatigue risk). Option C: delay lower-priority orders by two weeks (risk to two customers). Recommendation: A, with B as backup if demand rises further."</p>
<h3>Keep the pack short</h3>
<p>A good executive pack is a few pages: key measures, the plan summary by family, the decisions needed with scenarios, and risks. If the pack runs to 40 pages, the pre-S&amp;OP has not done its job. The lab after this lesson asks you to compare options by cost and service.</p>
""", ["Pre-S&OP resolves issues within the team's authority.", "Frame leadership decisions as two or three costed scenarios with a recommendation.", "Keep the executive pack to a few pages."],
 "Take one current supply–demand imbalance and write two or three options with service, cost, cash and risk effects and a recommendation.",
 "What should the pre-S&OP meeting pass to the executive meeting?", ["Every detail of every item", "Clear decisions framed as costed scenarios with recommendations", "Nothing; it makes all decisions", "Only last month's actuals"], 1,
 "Leaders need focused decisions, not raw data."),
step("The executive S&OP meeting and measures", 7, """
<p>The executive meeting is where the plan becomes the company's plan. It should be short, focused and decisive.</p>
<h3>Agenda (about 60 to 90 minutes)</h3>
<ol><li>Performance: key measures from last month.</li>
<li>Business and market changes.</li>
<li>Plan summary by family: demand, supply, inventory or backlog, financial view against budget.</li>
<li>Decisions: the scenarios prepared in pre-S&amp;OP.</li>
<li>Risks and opportunities.</li>
<li>Confirm the approved plan and actions.</li></ol>
<h3>Key S&amp;OP measures</h3>
<table><thead><tr><th>Area</th><th>Measure</th></tr></thead><tbody>
<tr><td>Demand</td><td>Forecast accuracy and bias by family</td></tr>
<tr><td>Supply</td><td>Production or purchasing plan attainment</td></tr>
<tr><td>Customer</td><td>On-time delivery, fill rate, lead time</td></tr>
<tr><td>Inventory</td><td>Inventory versus target by family, days of supply</td></tr>
<tr><td>Financial</td><td>Revenue and margin versus budget and latest estimate</td></tr>
<tr><td>Process</td><td>Meetings held on schedule, actions completed</td></tr>
</tbody></table>
<h3>Decide and record</h3>
<p>Every decision is recorded with an owner and communicated to the teams who must act on it. The approved plan becomes the basis for the master schedule, purchasing and the financial forecast. If people later work to a different plan, S&amp;OP has not yet taken hold.</p>
""", ["Run a short executive meeting that reviews performance and decides trade-offs.", "Track demand, supply, customer, inventory, financial and process measures.", "Record decisions with owners and make the approved plan the basis for all detailed plans."],
 "Draft a one-page executive S&OP agenda and pick six measures to review each month.",
 "What should happen to the approved S&OP plan after the executive meeting?", ["It is filed away", "It becomes the basis for the master schedule, purchasing and financial forecast", "Each department adjusts it privately", "It is reviewed again next year"], 1,
 "One approved plan should drive all detailed plans."),
step("Implementing S&OP: a six-cycle roadmap", 7, """
<p>S&amp;OP matures over several monthly cycles. A realistic plan expects the first cycles to be rough and improves each month.</p>
<table><thead><tr><th>Cycle</th><th>Focus</th></tr></thead><tbody>
<tr><td>Before cycle 1</td><td>Leader commitment; families defined; coordinator named; history gathered; calendar set</td></tr>
<tr><td>Cycles 1–2</td><td>Basic spreadsheet with demand, supply and inventory or backlog by family; first meetings; learn the rhythm</td></tr>
<tr><td>Cycles 3–4</td><td>Add rough-cut capacity for critical resources; start forecast accuracy and bias tracking; first scenarios</td></tr>
<tr><td>Cycles 5–6</td><td>Add the financial view against budget; refine families and targets; measure process discipline</td></tr>
<tr><td>Beyond</td><td>Supplier and customer collaboration, longer horizon, better tools, link to strategic planning</td></tr>
</tbody></table>
<h3>Tools</h3>
<p>Most SMEs start successfully with a well-structured spreadsheet. As the process matures, planning modules in ERP systems or dedicated planning software can automate data gathering and scenarios. Choose tools after the process works, not before.</p>
<h3>Signs S&amp;OP is working</h3>
<ul><li>One set of numbers is used across sales, operations and finance.</li>
<li>Peaks and shortages are seen months ahead.</li>
<li>Executive meetings make decisions, quickly.</li>
<li>Inventory is better balanced and expedites fall.</li></ul>
<h3>Related courses</h3>
<p>Inventory Management for SMEs covers inventory targets and replenishment in depth; OEE helps raise bottleneck capacity; and Data and Dashboards for SMEs helps automate the S&amp;OP data.</p>
""", ["Expect S&OP to mature over about six monthly cycles.", "Start with a spreadsheet; add capacity, accuracy and financial views step by step.", "Choose tools after the process works."],
 "Put the six-cycle roadmap into your calendar with dates for each monthly meeting and the improvement focus of each cycle.",
 "When should a company buy dedicated S&OP planning software?", ["Before the first meeting", "After the process works and its needs are clear", "Never", "Only if competitors have it"], 1,
 "Tools should support a working process, not substitute for one."),
]

course = dict(
 id="sales-and-operations-planning",
 title="Sales and Operations Planning (S&OP) for SMEs",
 tagline="Bring sales, operations and finance together each month to agree one plan that balances demand, capacity, inventory and cash.",
 summary="A practical S&OP course for owners, general managers, planners and department heads in small and mid-sized manufacturers and distributors. You will learn what S&OP is, how to define product families and run the monthly cycle, then build an honest demand plan, measure accuracy and bias, check rough-cut capacity, choose between level and chase strategies, manage materials and suppliers, and set inventory and backlog targets. It closes with the financial view, pre-S&OP scenarios, the executive meeting, key measures and a six-cycle roadmap.",
 audience=["Owners and general managers of manufacturers and distributors",
           "Planners, buyers and supply chain staff",
           "Sales, operations and finance leaders who contribute to the plan",
           "Companies facing frequent shortages, excess stock or capacity surprises"],
 outcomes=["Explain S&OP, planning levels, product families and time fences",
           "Run the monthly cycle from data gathering to the executive meeting",
           "Build an unconstrained demand plan and track forecast accuracy and bias",
           "Check rough-cut capacity and compare level, chase and mixed supply strategies",
           "Plan inventory and backlog by family and convert the plan into dollars",
           "Prepare scenarios, run a decisive executive meeting and implement S&OP over six cycles"],
 modules=[
  dict(title="S&OP Foundations", summary="What S&OP is, planning levels and product families, the monthly cycle and getting started.", steps=M1),
  dict(title="Demand Planning", summary="Building the demand plan, accuracy and bias, large customers, promotions and new products, and the demand review.", steps=M2),
  dict(title="Supply Planning", summary="Rough-cut capacity, level and chase strategies, materials and suppliers, and inventory and backlog targets.", steps=M3),
  dict(title="Integrate and Decide", summary="The financial view, pre-S&OP scenarios, the executive meeting and measures, and a six-cycle roadmap.", steps=M4)],
 labs=[
  dict(id="sop-which-step", type="classify", title="Which S&OP step handles it?", after_step=3,
       intro="Match twelve issues to the step of the monthly S&OP cycle where they belong: demand review, supply review, pre-S&OP or the executive meeting. Then check your answers.",
       config=dict(categories=["Demand review", "Supply review", "Pre-S&OP", "Executive meeting"], items=[
        dict(text="A key customer says its spring order will be 20% larger than last year", answer=0, why="Customer and market intelligence updates the demand plan."),
        dict(text="Forecast bias shows family B has been over-forecast for six months", answer=0, why="Forecast performance is reviewed in the demand review."),
        dict(text="A new product launch date moves from May to July", answer=0, why="Launch timing changes the demand plan (often via a product review)."),
        dict(text="The bottleneck line will be 115% loaded in October", answer=1, why="Capacity checks against demand happen in the supply review."),
        dict(text="A supplier warns its capacity for a key resin is limited next quarter", answer=1, why="Material constraints are assessed in the supply review."),
        dict(text="Planned maintenance will take line 2 down for a week in August", answer=1, why="Available capacity, including maintenance, is checked in supply review."),
        dict(text="Shifting 500 units of production from October to August within approved overtime", answer=2, why="Imbalances within the team's authority are resolved in pre-S&OP."),
        dict(text="Preparing three costed options for covering the October capacity gap", answer=2, why="Pre-S&OP frames unresolved trade-offs as scenarios."),
        dict(text="Checking the financial view of the plan against budget before the leadership meeting", answer=2, why="The integrated financial view is prepared in pre-S&OP."),
        dict(text="Deciding whether to add a third shift for the fall season", answer=3, why="Major trade-offs with cost and staffing effects are leadership decisions."),
        dict(text="Approving an inventory build that will tie up significant cash", answer=3, why="Decisions with large financial impact go to the executive meeting."),
        dict(text="Choosing which customers get priority when capacity is short", answer=3, why="Service trade-offs between customers are leadership decisions."),
       ])),
  dict(id="sop-capacity-check", type="calc", title="Rough-cut capacity check for one family", after_step=9,
       intro="Enter planned demand, the ideal rate on the critical resource, expected efficiency and available hours to see load, shortfall or spare capacity and maximum output.",
       config=dict(calc="capacity_gap", note="Use the critical resource for the family, such as the bottleneck line. Include holidays and planned maintenance when estimating available hours.")),
  dict(id="sop-option-matrix", type="matrix", title="Comparing ways to close a capacity gap", after_step=14,
       intro="Place seven options for covering a seasonal capacity gap on a grid of cost against service benefit, to see which to recommend at the executive meeting.",
       config=dict(x="Cost and risk", y="Service benefit", x_low="Low cost", x_high="High cost", y_low="Little benefit", y_high="Large benefit",
        quadrants=dict(top_left="Recommend first", top_right="Consider if needed", bottom_left="Easy but small", bottom_right="Avoid"),
        items=[dict(name="Build inventory ahead of the peak", x=2, y=5),
               dict(name="Saturday overtime in peak months", x=3, y=4),
               dict(name="Improve OEE on the bottleneck", x=2, y=4),
               dict(name="Outsource part of the volume", x=4, y=3),
               dict(name="Buy a second line", x=5, y=5),
               dict(name="Delay low-priority orders two weeks", x=1, y=2),
               dict(name="Hire temporary staff without training", x=4, y=2)])),
 ],
 figures=[
  dict(step=2, type="stack", title="The planning hierarchy", caption="Click each level, from the bottom up, to see how detail falls and horizon lengthens.",
       config=dict(top_label="Strategic plan", layers=[
        dict(label="Detailed schedule", text="Orders by day or shift, days to weeks ahead."),
        dict(label="Master schedule and purchasing plan", text="Items by week, weeks to a few months ahead."),
        dict(label="S&OP", text="Product families by month, 3 to 18 months ahead."),
        dict(label="Business and strategic plan", text="Markets, revenue and profit, 1 to 5 years ahead.")])),
  dict(step=3, type="cycle", title="The monthly S&OP cycle", caption="Click each step. Each resolves what it can and passes trade-offs upward.",
       config=dict(center="One plan", stages=[
        dict(label="Data", text="Actuals, accuracy, inventory and backlog by family."),
        dict(label="Demand review", text="Agree the unconstrained demand plan with assumptions."),
        dict(label="Supply review", text="Check capacity and materials; develop options."),
        dict(label="Pre-S&OP", text="Resolve issues; cost the scenarios; prepare the pack."),
        dict(label="Executive S&OP", text="Decide trade-offs and approve the plan.")])),
  dict(step=9, type="bars", title="Example: load on the bottleneck by month", caption="Hours needed on the bottleneck line versus 320 hours available. October is over capacity.",
       config=dict(unit="hours needed", items=[dict(label="July", value=238), dict(label="August", value=262), dict(label="September", value=310), dict(label="October", value=357, highlight=True)],
        note="At 42 effective units an hour, October's 15,000 units need about 357 hours, a shortfall of about 37 hours.")),
  dict(step=10, type="compare", title="Level vs chase", caption="Toggle between the two strategies and compare their effects.",
       config=dict(left=dict(title="Level", points=["Steady production rate", "Inventory absorbs peaks and valleys", "Stable workforce and efficient operations", "Carrying cost and demand risk"]),
                   right=dict(title="Chase", points=["Production follows demand each month", "Low inventory", "Overtime, hiring and idle time", "Quality and morale risks"]))),
  dict(step=13, type="flow", title="From volume plan to financial view", caption="Click each step to see how finance turns the plan into money.",
       config=dict(steps=[
        dict(label="Volume plan", text="Demand, production and inventory by family in units."),
        dict(label="Price and cost", text="Average prices and costs by family."),
        dict(label="Revenue and margin", text="Monthly revenue and gross margin by family."),
        dict(label="Inventory and cash", text="Inventory value, capacity costs and cash effects."),
        dict(label="Compare", text="Against budget and the rolling latest estimate.")])),
  dict(step=16, type="timeline", title="Implementing S&OP over six cycles", caption="Click each phase to see its focus.",
       config=dict(phases=[
        dict(label="Before", title="Prepare", items=["Leader commitment", "Families and coordinator", "History and calendar"]),
        dict(label="Cycles 1–2", title="Rhythm", items=["Basic family spreadsheet", "First meetings"]),
        dict(label="Cycles 3–4", title="Capacity and accuracy", items=["Rough-cut capacity", "Accuracy and bias", "First scenarios"]),
        dict(label="Cycles 5–6", title="Financial view", items=["Plan vs budget", "Refine families and targets", "Process measures"])])),
 ],
 exam=[
  E("What is the main purpose of S&OP?", ["To agree one monthly plan that balances demand, supply and money across functions", "To schedule tomorrow's production", "To set salespeople's commissions", "To replace the annual budget"], 0, "S&OP aligns functions on one plan."),
  E("Over what horizon does S&OP usually plan?", ["Hours", "About 3 to 18 months", "Days", "Ten years"], 1, "S&OP covers the medium term."),
  E("How many product families do most SMEs need for S&OP?", ["One", "Hundreds", "About 5 to 15", "One per customer"], 2, "A manageable number of families keeps the meeting focused."),
  E("What is a frozen time fence?", ["A period with no sales", "A cold storage area", "A forecast method", "A near-term period where plan changes need special approval"], 3, "Frozen periods protect near-term schedules and materials."),
  E("What is the correct order of the S&OP steps?", ["Data, demand review, supply review, pre-S&OP, executive meeting", "Executive meeting, data, supply, demand", "Supply review, data, executive, demand", "Pre-S&OP, demand, data, executive"], 0, "Each step feeds the next."),
  E("Who should chair the executive S&OP meeting?", ["The newest planner", "The owner or general manager", "An outside consultant", "The IT manager"], 1, "Leadership ownership drives decisions."),
  E("What should the demand plan represent?", ["The sales target", "The budget", "An honest, unconstrained estimate of customer demand", "What operations can produce"], 2, "Demand plans show real demand so gaps are visible."),
  E("What are the two main inputs to a demand plan?", ["Payroll and rent", "Supplier invoices and receipts", "Machine hours and scrap", "A statistical baseline and market intelligence"], 3, "History plus known events."),
  E("Why is forecast bias especially damaging?", ["It accumulates into excess or shortages month after month", "It is always small", "It only affects finance", "It cancels out over time"], 0, "Consistent errors build up."),
  E("What is forecast value added?", ["The price increase on products", "Comparing accuracy before and after adjustments to see if they help", "The margin on forecasted sales", "The value of inventory"], 1, "It checks whether human adjustments improve the forecast."),
  E("How should large one-off project orders be handled in the demand plan?", ["Hidden", "Added to history as normal", "Separately, with probability and timing", "Ignored"], 2, "Separating them protects the baseline and shows risk."),
  E("What does rough-cut capacity planning check?", ["Each worker's daily tasks", "Exact machine schedules", "Office supplies", "Load on critical resources against available capacity by family and month"], 3, "It tests feasibility at an aggregate level."),
  E("A family needs 15,000 units; the line makes 42 effective units an hour. Roughly how many hours are needed?", ["About 357", "About 250", "About 630", "About 42"], 0, "15,000 ÷ 42 ≈ 357 hours."),
  E("What characterizes a level production strategy?", ["Production changes every month to match demand", "A steady production rate with inventory absorbing peaks", "No inventory at all", "Production only when orders arrive"], 1, "Level strategies smooth production."),
  E("Why share family forecasts with key suppliers?", ["To avoid ordering", "To reduce prices automatically", "So they can reserve capacity and materials", "It is legally required"], 2, "Visibility helps suppliers plan."),
  E("Beginning inventory 5,000, production 8,000, demand 9,500. What is ending inventory?", ["2,500", "4,500", "13,000", "3,500"], 3, "5,000 + 8,000 − 9,500 = 3,500."),
  E("Why compare the S&OP plan with the budget?", ["For early warning of gaps so leaders can act", "To blame sales", "To replace the plan", "To satisfy auditors only"], 0, "Gaps are early signals."),
  E("What should the pre-S&OP meeting pass to the executive meeting?", ["Every item-level detail", "Costed scenarios with recommendations", "Only last month's actuals", "Nothing"], 1, "Leaders need clear decisions."),
  E("What should the approved S&OP plan drive?", ["Nothing; it is advisory", "Only marketing", "The master schedule, purchasing and financial forecast", "Annual salary reviews"], 2, "One plan should guide all detailed plans."),
  E("When should dedicated S&OP software be introduced?", ["Before the first cycle", "Never", "Only by large companies", "After the process works and its needs are clear"], 3, "Process first, tools second."),
 ],
)

if __name__ == "__main__":
    write(course, "sop", __file__, balance=True)
