"""Source for content/courses/inventory-management.json (run: python3 content/courses/src/inventory_management.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import step, E, write

M1 = [
step("Why inventory matters: cash, service and cost", 6, """
<p>Inventory sits between what you buy and what you sell. Too little and you miss orders, expedite freight and stop production lines. Too much and cash is tied up on shelves, space fills, and stock ages, gets damaged or becomes obsolete. Good inventory management is the balance between <strong>service</strong> (having what customers need when they need it) and <strong>cost</strong> (the money and effort tied up in stock).</p>
<h3>What inventory really costs</h3>
<p>The price paid for an item is only the start. Holding it costs money every day it sits there. <strong>Carrying cost</strong> includes:</p>
<table><thead><tr><th>Component</th><th>Examples</th></tr></thead><tbody>
<tr><td>Cost of capital</td><td>Interest on the line of credit, or the return you could earn elsewhere</td></tr>
<tr><td>Storage</td><td>Rent, racking, heating or cooling, warehouse staff</td></tr>
<tr><td>Risk</td><td>Obsolescence, damage, shrinkage, expiry, price drops</td></tr>
<tr><td>Service</td><td>Insurance, property taxes on inventory where they apply, handling</td></tr>
</tbody></table>
<p>Annual carrying cost is often estimated at around 20 to 30 percent of average inventory value, and higher for perishable, fashion or fast-changing technical products. Estimate your own: even a rough figure changes decisions. At 25 percent, an extra $200,000 of stock costs about $50,000 a year to hold.</p>
<h3>The cost of running out</h3>
<p>Stock-outs cost too: lost sales, expedited freight, overtime, idle production, partial shipments and, most of all, customer trust. Unlike carrying cost these rarely show up as one line in the accounts, which is why many businesses overstock "to be safe". This course gives you methods to decide how much is enough, item by item.</p>
<h3>Who owns inventory?</h3>
<p>Inventory touches sales (forecasts and promises), purchasing (what and when to buy), operations (what to make), the warehouse (accuracy) and finance (cash). Problems often come from these groups working to different goals. A shared set of measures and a regular planning meeting, covered later in the course, align them.</p>
""", ["Inventory management balances customer service against the cost of holding stock.", "Carrying cost is often 20 to 30 percent of inventory value per year.", "Stock-outs have real costs even if they do not show as one line in the accounts."],
 "Estimate your annual carrying cost rate using the four components above. Multiply it by your current average inventory value to see what holding stock costs you each year.",
 "Average inventory is $400,000 and the carrying cost rate is 25% a year. What does it cost to hold this inventory for a year?", ["$40,000", "$100,000", "$25,000", "$400,000"], 1,
 "Annual carrying cost = $400,000 × 25% = $100,000."),
step("Types of inventory and why each exists", 7, """
<p>Inventory is classified two ways: by <strong>form</strong> and by <strong>purpose</strong>. Both matter, because each purpose calls for a different decision.</p>
<table><thead><tr><th>By form</th><th>Examples</th></tr></thead><tbody>
<tr><td>Raw materials and components</td><td>Steel coil, resin, purchased parts, packaging</td></tr>
<tr><td>Work in progress (WIP)</td><td>Partly made products between operations</td></tr>
<tr><td>Finished goods</td><td>Products ready to ship, or bought-in goods for resale at a distributor</td></tr>
<tr><td>MRO</td><td>Maintenance, repair and operating supplies: spare parts, lubricants, gloves</td></tr>
</tbody></table>
<table><thead><tr><th>By purpose</th><th>Why it exists</th><th>Main lever to reduce it</th></tr></thead><tbody>
<tr><td>Cycle stock</td><td>You buy or make in batches larger than one day's need</td><td>Smaller, more frequent orders; lower ordering or setup cost</td></tr>
<tr><td>Safety stock</td><td>Protects against uncertainty in demand and supply</td><td>Better forecasts; shorter, more reliable lead times</td></tr>
<tr><td>Anticipation stock</td><td>Built ahead of a known peak, promotion or shutdown</td><td>Level production; plan the build carefully</td></tr>
<tr><td>Pipeline (in-transit) stock</td><td>Goods on the way from suppliers or between sites</td><td>Shorter transit; nearer suppliers</td></tr>
<tr><td>Excess and obsolete</td><td>No longer needed in the quantity held</td><td>Prevent with reviews; clear with disposition plans</td></tr>
</tbody></table>
<p>When someone says "we have too much inventory", ask which kind. A warehouse full of anticipation stock before a seasonal peak is planned and healthy. The same space full of slow movers from discontinued lines is a problem. Splitting inventory by purpose turns a vague complaint into specific actions.</p>
<p>The lab after this lesson asks you to classify examples by purpose.</p>
""", ["Classify inventory by form and by purpose.", "Each purpose has a different lever: batch size, uncertainty, peaks or transit.", "Ask 'which kind?' before trying to cut inventory."],
 "Estimate how your inventory value splits across cycle, safety, anticipation, pipeline and excess stock. Which group would you target first?",
 "A distributor builds stock in August ahead of its October peak season. What type of inventory is this?", ["Safety stock", "Excess stock", "Anticipation stock", "Pipeline stock"], 2,
 "Stock built ahead of a known peak is anticipation stock."),
step("Measuring inventory performance", 7, """
<p>You cannot manage inventory by feel. A short set of measures, tracked monthly and by item class, shows whether you are improving.</p>
<table><thead><tr><th>Measure</th><th>How it is calculated</th><th>What it tells you</th></tr></thead><tbody>
<tr><td>Inventory turns</td><td>Annual cost of goods sold ÷ average inventory value at cost</td><td>How many times stock is used and replaced in a year</td></tr>
<tr><td>Days on hand</td><td>365 ÷ turns, or inventory ÷ average daily cost of goods sold</td><td>How many days of usage you hold</td></tr>
<tr><td>Fill rate</td><td>Units (or lines) shipped complete from stock ÷ units (or lines) ordered</td><td>How often customers get what they ask for</td></tr>
<tr><td>Stock-out rate</td><td>Items or days out of stock ÷ total items or days</td><td>How often you run out</td></tr>
<tr><td>Inventory record accuracy</td><td>Locations or items where the count matches the system ÷ items counted</td><td>Whether the system can be trusted</td></tr>
<tr><td>Excess and obsolete</td><td>Value with no usage in, say, 12 months or above a set months-of-supply</td><td>Stock at risk of write-off</td></tr>
</tbody></table>
<h3>Example</h3>
<p>A distributor's annual cost of goods sold is $6 million and its average inventory is $1.5 million at cost. Turns are 6,000,000 ÷ 1,500,000 = 4, so it holds about 365 ÷ 4 ≈ 91 days of stock. If better ordering lifts turns to 5 at the same sales, average inventory falls to $1.2 million, freeing $300,000 of cash and saving the carrying cost on it.</p>
<h3>Use measures in pairs</h3>
<p>Turns and fill rate pull in opposite directions: cutting stock raises turns but can lower fill rate. Always report them together, and by item class, so no one improves one by quietly damaging the other. Compare yourself with your own history first; industry averages vary too widely to be a reliable target.</p>
""", ["Track turns, days on hand, fill rate, stock-outs, accuracy and excess.", "Turns = cost of goods sold ÷ average inventory value at cost.", "Report service and stock measures together so one is not improved at the other's expense."],
 "Calculate your inventory turns and days on hand for the last 12 months. Then find or estimate your fill rate for the same period.",
 "Annual cost of goods sold is $3 million and average inventory at cost is $750,000. What are the inventory turns?", ["2", "3", "4", "5"], 2,
 "Turns = $3,000,000 ÷ $750,000 = 4."),
step("Inventory accuracy and cycle counting", 7, """
<p>Every inventory method in this course depends on the system's quantities being right. If the system says 40 and the shelf has 12, the reorder point never triggers and you run out. If the shelf has 80, you buy more of what you already have. <strong>Inventory record accuracy</strong> is the foundation.</p>
<h3>Why records drift</h3>
<ul><li>Receipts not entered, or entered against the wrong item or location.</li>
<li>Picks taken from a different location than the system says.</li>
<li>Unit-of-measure confusion: cases versus eaches, metres versus rolls.</li>
<li>Scrap, samples and returns not recorded.</li>
<li>Production consumption that differs from the bill of materials.</li></ul>
<h3>Cycle counting instead of one big count</h3>
<p>An annual wall-to-wall count shuts operations for a day or more, finds errors months after they happened and fixes the numbers but not the causes. <strong>Cycle counting</strong> counts a small set of items every day or week, so every item is counted several times a year, more often for important items. Typical frequencies: A items monthly or quarterly, B items quarterly or twice a year, C items once or twice a year. Many firms also count when a location reaches zero, since it is quick and catches errors early.</p>
<h3>Make the counts improve the process</h3>
<p>The real value of cycle counting is finding why errors happen. For each discrepancy above a tolerance, investigate the recent transactions, find the cause and fix it: a missing receiving step, an unclear label, a picker using the wrong unit. Measure accuracy as the percentage of counts within tolerance. Many organizations aim for 95 percent or better on all items and higher on A items.</p>
<p>Make counts blind (the counter does not see the system quantity), and separate counting from the person who adjusts the record.</p>
""", ["Every method depends on accurate inventory records.", "Cycle count small sets often, with A items counted most frequently.", "Investigate and fix the cause of each discrepancy, not just the number."],
 "Pick ten items in your system and count them today. Compare with the system, then trace the recent transactions for any that differ and note the likely cause.",
 "What is the main advantage of cycle counting over a single annual count?", ["It finds errors soon after they occur so their causes can be fixed", "It never needs any staff time", "It removes the need for a warehouse system", "Auditors no longer review inventory"], 0,
 "Frequent small counts catch errors close to when they happen, making root causes traceable and fixable."),
]

M2 = [
step("ABC analysis: focus where the value is", 8, """
<p>Not all items deserve the same attention. <strong>ABC analysis</strong> ranks items by annual usage value (annual units used or sold × unit cost) and groups them:</p>
<table><thead><tr><th>Class</th><th>Typical share of items</th><th>Typical share of annual value</th></tr></thead><tbody>
<tr><td>A</td><td>About 10–20%</td><td>About 70–80%</td></tr>
<tr><td>B</td><td>About 20–30%</td><td>About 15–20%</td></tr>
<tr><td>C</td><td>About 50–70%</td><td>About 5–10%</td></tr>
</tbody></table>
<p>The exact cut-offs are a choice, not a law. Pick ones that give you a manageable number of A items.</p>
<h3>How to do it</h3>
<ol><li>Export 12 months of usage or sales by item, with unit cost.</li>
<li>Calculate annual usage value for each item.</li>
<li>Sort from highest to lowest.</li>
<li>Add a running total and a cumulative percentage of total value.</li>
<li>Assign classes at your chosen cut-offs, for example A up to 80 percent cumulative value, B up to 95 percent, C the rest.</li></ol>
<p>Then adjust with judgement. A low-value item that stops a production line or is critical to a key customer may need A-level care. Many firms add a criticality flag rather than changing the ABC class itself.</p>
<p>Repeat the analysis every quarter or twice a year: products move between classes as sales change. The Chmltech Insights series walks through full worked examples for a <a href="../post/abc-inventory-analysis.html">distributor</a> and a <a href="../post/abc-analysis-for-manufacturers.html">manufacturer</a>, with a downloadable Excel template.</p>
""", ["Rank items by annual usage value and split them into A, B and C.", "A small share of items usually carries most of the value.", "Adjust for criticality and repeat the analysis regularly."],
 "Export last year's usage by item with unit costs and run an ABC analysis. How many A items do you have, and what share of value do they carry?",
 "How is annual usage value calculated for ABC analysis?", ["Unit price × items on hand", "Annual units used × unit cost", "Number of orders × order size", "Unit cost × lead time"], 1,
 "ABC ranks items by annual usage value, which is annual units used or sold multiplied by unit cost."),
step("XYZ analysis: how predictable is demand?", 7, """
<p>ABC tells you how much an item is worth. It does not tell you how hard it is to plan. <strong>XYZ analysis</strong> classifies items by how variable their demand is, usually using the <strong>coefficient of variation (CV)</strong>: the standard deviation of demand per period divided by the average demand per period.</p>
<table><thead><tr><th>Class</th><th>Typical CV of monthly demand</th><th>Demand pattern</th></tr></thead><tbody>
<tr><td>X</td><td>Below about 0.5</td><td>Steady and predictable</td></tr>
<tr><td>Y</td><td>About 0.5 to 1.0</td><td>Variable, with trends or seasonality</td></tr>
<tr><td>Z</td><td>Above about 1.0</td><td>Erratic or intermittent; many periods with no demand</td></tr>
</tbody></table>
<p>As with ABC, the cut-offs are a choice. Use the same period length for every item, usually months, and at least 12 periods of history.</p>
<h3>Combining ABC and XYZ</h3>
<p>The nine-cell ABC-XYZ grid gives each group a sensible policy:</p>
<table><thead><tr><th></th><th>X (steady)</th><th>Y (variable)</th><th>Z (erratic)</th></tr></thead><tbody>
<tr><td>A</td><td>Automate replenishment; tight review; low safety stock relative to demand</td><td>Forecast carefully; review often</td><td>Plan with customers; consider make or buy to order</td></tr>
<tr><td>B</td><td>Automated reorder points</td><td>Standard safety stock rules</td><td>Review case by case</td></tr>
<tr><td>C</td><td>Simple rules such as two-bin or min-max</td><td>Simple rules; generous safety stock is cheap</td><td>Stock only if needed; consider not stocking</td></tr>
</tbody></table>
<p>AZ items, high value and erratic demand, are the hardest. Holding enough safety stock for erratic demand on expensive items costs a lot. Better options are working with customers on advance notice, agreeing lead times, or not stocking at all. The lab after this lesson lets you place items on a value and variability grid.</p>
""", ["XYZ classifies items by demand variability using the coefficient of variation.", "Combine ABC and XYZ to give each group a fitting policy.", "High-value, erratic items often need customer collaboration rather than more stock."],
 "Calculate the coefficient of variation of monthly demand for five of your A items. Which are X, Y or Z, and does their current policy fit?",
 "An item's monthly demand averages 100 units with a standard deviation of 120 units. Which XYZ class is it?", ["X", "Y", "Z", "A"], 2,
 "CV = 120 ÷ 100 = 1.2, which is above 1.0, so the item is erratic: class Z."),
step("Setting policies by class", 7, """
<p>Classes are only useful if they lead to different treatment. Write a one-page <strong>inventory policy</strong> that sets, for each class, the rules people should follow.</p>
<table><thead><tr><th>Policy area</th><th>A items</th><th>B items</th><th>C items</th></tr></thead><tbody>
<tr><td>Target service level</td><td>Set per item group; often high for key customers</td><td>Moderate to high</td><td>High is cheap, so often high</td></tr>
<tr><td>Review frequency</td><td>Weekly or continuous</td><td>Every two to four weeks</td><td>Monthly or automatic</td></tr>
<tr><td>Cycle count frequency</td><td>Monthly to quarterly</td><td>Quarterly to twice a year</td><td>Once or twice a year</td></tr>
<tr><td>Forecasting effort</td><td>Detailed, with sales input</td><td>Statistical, reviewed for exceptions</td><td>Simple rules</td></tr>
<tr><td>Ordering</td><td>Smaller, more frequent orders</td><td>Standard reorder points</td><td>Larger orders, two-bin or min-max</td></tr>
</tbody></table>
<h3>Why C items often get high service levels</h3>
<p>It seems backwards, but it is usually right. C items are cheap, so extra safety stock costs little. Yet a missing C item, such as a fastener or a label, can still stop a shipment. Holding a bit more of C items and buying them less often frees the planners' time for A items, where every unit of stock is expensive.</p>
<h3>Service level targets</h3>
<p>Define service level clearly. <strong>Cycle service level</strong> is the probability of not running out during a replenishment cycle. <strong>Fill rate</strong> is the share of demand met from stock. They are not the same: a 95 percent cycle service level usually gives a fill rate well above 95 percent, because when you do run out it is often only for part of the demand. Use cycle service level to set safety stock and fill rate to report service to customers.</p>
""", ["Write a one-page policy that treats each class differently.", "C items often get high service levels because extra stock is cheap.", "Distinguish cycle service level from fill rate."],
 "Draft your policy table for A, B and C items: service level, review frequency, count frequency and ordering approach. Share it with purchasing and sales.",
 "Why do many companies set high service levels for C items?", ["C items are the most profitable", "C items never run out", "Customers only buy C items", "Extra safety stock on cheap items costs little, and their absence can still stop shipments"], 3,
 "Low unit value makes extra C stock cheap, while a missing C item can still halt an order or a line."),
step("Slow-moving, excess and obsolete stock", 7, """
<p>Every business accumulates stock it does not need: discontinued products, over-buys, customer-specific items left after a contract ended, engineering changes that made parts redundant. This <strong>excess and obsolete (E&amp;O)</strong> stock costs space, handling and carrying cost, and the longer it sits the less it is worth.</p>
<h3>Find it</h3>
<p>Run a monthly report of items with no usage in the last 6 or 12 months, and items with more than a set number of months of supply, such as 12 months based on the last year's usage. Show the value and age of each.</p>
<h3>Decide what to do</h3>
<table><thead><tr><th>Option</th><th>When it fits</th></tr></thead><tbody>
<tr><td>Use it up</td><td>Substitute it for current items where quality and customer approval allow</td></tr>
<tr><td>Return to supplier</td><td>Often possible for recent, unopened stock, sometimes with a restocking fee</td></tr>
<tr><td>Sell or discount</td><td>To other customers, brokers or through clearance channels</td></tr>
<tr><td>Rework</td><td>Convert it into a current product if the cost makes sense</td></tr>
<tr><td>Donate, recycle or scrap</td><td>When no better option exists; follow accounting and environmental rules</td></tr>
</tbody></table>
<p>Involve finance early. Write-downs and write-offs affect the financial statements, and the timing and treatment may have tax implications that your accountant should advise on. Holding obsolete stock in the hope that its value returns usually costs more than acting.</p>
<h3>Prevent it</h3>
<ul><li>Review new-product and end-of-life plans with purchasing so buying stops in time.</li>
<li>Check engineering changes for stock on hand and on order before they take effect.</li>
<li>Agree customer commitments for customer-specific stock in writing.</li>
<li>Avoid large buys for small discounts without checking months of supply.</li></ul>
""", ["Report items with no recent usage and high months of supply every month.", "Choose a disposition: use, return, sell, rework or scrap.", "Prevent E&O with end-of-life, engineering change and customer-commitment checks."],
 "Run a report of items with no usage in 12 months. Total their value and pick the five largest for a disposition decision this month.",
 "What should happen before an engineering change takes effect?", ["Nothing; the change is engineering's responsibility", "Check stock on hand and on order for the affected parts", "Write off all old parts immediately", "Double the order for the new parts"], 1,
 "Checking affected stock and open orders first avoids creating obsolete inventory that could have been used up or cancelled."),
]

M3 = [
step("Understanding demand patterns", 7, """
<p>Before choosing how to forecast or how much safety stock to hold, look at the shape of each item's demand. Plot 24 months of history by item. Most items show one or more of these patterns:</p>
<table><thead><tr><th>Pattern</th><th>What it looks like</th><th>Example</th></tr></thead><tbody>
<tr><td>Level</td><td>Varies around a steady average</td><td>Standard fasteners, consumables</td></tr>
<tr><td>Trend</td><td>Steadily rising or falling</td><td>A growing product line; a product being phased out</td></tr>
<tr><td>Seasonal</td><td>Repeats at the same time each year</td><td>Heating products, landscaping supplies, holiday goods</td></tr>
<tr><td>Intermittent (lumpy)</td><td>Many periods of zero, then occasional orders</td><td>Spare parts, project-driven items</td></tr>
</tbody></table>
<h3>Clean the history first</h3>
<p>Forecasts built on raw sales can mislead. Adjust for:</p>
<ul><li><strong>Stock-outs:</strong> sales were zero because you had none, not because no one wanted it. Use orders or estimated lost demand where you can.</li>
<li><strong>One-off events:</strong> a single project order or a customer's one-time stock-up.</li>
<li><strong>Promotions:</strong> a price promotion that pulled demand forward.</li>
<li><strong>Calendar effects:</strong> months with different numbers of working days.</li></ul>
<h3>Dependent and independent demand</h3>
<p>Finished products sold to customers have <strong>independent demand</strong>: you forecast it. Components used to make those products have <strong>dependent demand</strong>: you calculate it from the production plan and the bill of materials. Forecasting components separately from their parent products adds avoidable error. Manufacturers use material requirements planning (MRP) for dependent items, covered later in the course.</p>
""", ["Plot each item's history to see level, trend, seasonal or intermittent demand.", "Clean the history for stock-outs, one-offs, promotions and calendar effects.", "Forecast independent demand; calculate dependent demand from the plan."],
 "Plot 24 months of demand for three of your A items. Label each as level, trend, seasonal or intermittent and note any months you would clean before forecasting.",
 "A component is used only inside one finished product. How should its demand be planned?", ["Forecast it from its own sales history", "Calculate it from the finished product plan and the bill of materials", "Hold a fixed six months of stock", "Order it only when it runs out"], 1,
 "A component has dependent demand, which is calculated from the parent product's plan and the bill of materials."),
step("Simple forecasting methods that work", 8, """
<p>Small and mid-sized businesses rarely need complex forecasting software to start. A few simple methods, applied consistently, beat gut feel.</p>
<table><thead><tr><th>Method</th><th>How it works</th><th>Fits</th></tr></thead><tbody>
<tr><td>Moving average</td><td>Average of the last n periods, for example 3 or 6 months</td><td>Level demand</td></tr>
<tr><td>Exponential smoothing</td><td>New forecast = old forecast + α × (actual − old forecast), with α between 0 and 1</td><td>Level demand; reacts smoothly to change</td></tr>
<tr><td>Trend-adjusted smoothing</td><td>Smooths both the level and the trend</td><td>Steadily growing or declining items</td></tr>
<tr><td>Seasonal indices</td><td>Forecasts the underlying level, then multiplies by each month's seasonal factor</td><td>Repeating yearly patterns</td></tr>
<tr><td>Judgemental overlay</td><td>Adjusts a statistical forecast for known events: a new customer, a promotion, a lost contract</td><td>Any item, used sparingly and documented</td></tr>
</tbody></table>
<h3>Exponential smoothing in one example</h3>
<p>Last month's forecast was 200 units and actual demand was 240. With α = 0.2, the new forecast is 200 + 0.2 × (240 − 200) = 208. A higher α reacts faster to change but also to noise; a lower α is steadier. Values around 0.1 to 0.3 are common starting points.</p>
<h3>Seasonal indices</h3>
<p>If November demand has averaged 1.4 times the monthly average over several years, its seasonal index is 1.4. With an underlying level of 500 units a month, the November forecast is 500 × 1.4 = 700. Use at least two, ideally three, years of history to estimate seasonal indices.</p>
<h3>Forecast at the right level</h3>
<p>Forecasts are more accurate for groups than for single items, and for longer periods than shorter ones. Many firms forecast product families by month, then split to items by recent mix. Always keep a record of who overrode a forecast and why, so you can learn whether the overrides helped.</p>
""", ["Moving averages and exponential smoothing handle level demand well.", "Add trend and seasonal indices where the pattern needs them.", "Forecast groups and longer periods where you can; document overrides."],
 "Choose one item with level demand. Calculate a 3-month moving average and an exponential smoothing forecast with α = 0.2 for the last six months, and compare both with actual demand.",
 "Last month's forecast was 500 and actual demand was 400. With α = 0.3, what is the new exponentially smoothed forecast?", ["470", "430", "400", "530"], 0,
 "500 + 0.3 × (400 − 500) = 500 − 30 = 470."),
step("Measuring forecast error and bias", 7, """
<p>Every forecast is wrong; the question is by how much and in which direction. Measuring error tells you how much safety stock you need and whether your method is improving.</p>
<table><thead><tr><th>Measure</th><th>Calculation</th><th>What it shows</th></tr></thead><tbody>
<tr><td>Error</td><td>Actual − forecast for each period</td><td>The raw miss</td></tr>
<tr><td>MAD (mean absolute deviation)</td><td>Average of the absolute errors</td><td>Typical size of a miss, in units</td></tr>
<tr><td>MAPE</td><td>Average of absolute error ÷ actual, as a percentage</td><td>Typical size of a miss relative to demand</td></tr>
<tr><td>Bias</td><td>Sum or average of the errors, keeping the sign</td><td>Whether you consistently forecast too high or too low</td></tr>
</tbody></table>
<h3>Example</h3>
<p>Over four months an item had actuals of 100, 120, 90 and 110 against forecasts of 110, 110, 110 and 110. Errors are −10, +10, −20 and 0. MAD = (10 + 10 + 20 + 0) ÷ 4 = 10 units. Bias = (−10 + 10 − 20 + 0) ÷ 4 = −5 units a month: on average the forecast was 5 units too high.</p>
<h3>Why bias matters most</h3>
<p>Random error averages out; bias does not. A forecast that is always 15 percent high builds excess stock month after month. A forecast that is always low causes repeated stock-outs and expediting. Bias often comes from people: sales teams rounding up to protect supply, or planners rounding down under cash pressure. Track bias by item group and by who made the forecast.</p>
<p>MAPE can mislead for low-volume items, because a miss of 2 units on actual demand of 1 is a 200 percent error. For intermittent items, use MAD or a weighted measure instead. Review error and bias monthly in the planning meeting covered in the next lesson.</p>
""", ["Track MAD or MAPE for the size of the miss and bias for its direction.", "Bias builds excess or shortages month after month; random error averages out.", "Use MAD rather than MAPE for low-volume, intermittent items."],
 "Calculate MAD and bias for three A items over the last six months. Is any of them consistently over- or under-forecast?",
 "Over a year a forecast is above actual demand in 11 of 12 months. What does this show?", ["Low MAPE", "A positive bias toward over-forecasting that builds excess stock", "Random error that will average out", "Perfect accuracy"], 1,
 "Consistent over-forecasting is bias, which accumulates as excess inventory rather than averaging out."),
step("Sales and operations planning for SMEs", 7, """
<p><strong>Sales and operations planning (S&amp;OP)</strong> is a monthly routine that brings sales, operations, purchasing and finance together to agree one plan for the next several months. Without it, sales forecasts one number, operations plans another, purchasing buys to a third and finance discovers the result in the bank balance.</p>
<h3>A simple monthly cycle</h3>
<table><thead><tr><th>Week</th><th>Step</th><th>Output</th></tr></thead><tbody>
<tr><td>1</td><td>Data gathering</td><td>Last month's actuals, forecast error and bias, inventory by class</td></tr>
<tr><td>2</td><td>Demand review</td><td>Sales and planning agree the demand plan by product family, with known events</td></tr>
<tr><td>2–3</td><td>Supply review</td><td>Operations and purchasing check capacity, materials and lead times against the demand plan</td></tr>
<tr><td>3</td><td>Pre-meeting</td><td>Resolve issues and prepare options with cost and service impacts</td></tr>
<tr><td>4</td><td>Executive meeting</td><td>The owner or general manager decides between options and approves the plan</td></tr>
</tbody></table>
<p>In a small company this can be two meetings a month of an hour each, using a shared spreadsheet. The discipline matters more than the tools.</p>
<h3>What the plan covers</h3>
<ul><li>Demand by product family for the next 3 to 18 months.</li>
<li>Production or purchasing plan and capacity, including overtime or extra shifts.</li>
<li>Planned inventory by family, in units and dollars, compared with targets.</li>
<li>Key risks: a large customer's uncertain order, a supplier's capacity, a planned shutdown.</li></ul>
<p>The benefit is fewer surprises: purchasing sees peaks early, operations plans capacity, and finance sees the cash needed for inventory builds. The Chmltech article on <a href="../post/sales-and-operations-planning-for-small-manufacturers.html">S&amp;OP for small manufacturers</a> goes further.</p>
""", ["S&OP agrees one plan across sales, operations, purchasing and finance each month.", "A small company can run it in two short monthly meetings.", "Plan demand, supply and inventory by product family for the next several months."],
 "Draft an agenda for a one-hour monthly planning meeting: who attends, which three reports to bring and which decisions to make.",
 "What is the main purpose of the executive step in S&OP?", ["To produce the detailed weekly production schedule", "To count inventory", "To decide between options and approve one integrated plan", "To set individual sales commissions"], 2,
 "The executive meeting resolves trade-offs between service, cost and inventory and approves the single agreed plan."),
]

M4 = [
step("Reorder points and lead time", 7, """
<p>The two core questions of replenishment are <strong>when to order</strong> and <strong>how much</strong>. The <strong>reorder point (ROP)</strong> answers the first: when stock on hand plus stock on order falls to the ROP, place an order.</p>
<p>ROP = demand during lead time + safety stock</p>
<p>If an item sells 40 units a working day and the supplier takes 10 working days to deliver, demand during lead time is 400 units. Without safety stock, you would order when 400 are left and expect to run out just as the delivery arrives. Safety stock, covered next, protects against demand being higher or the delivery being later than expected.</p>
<h3>Lead time is more than transit</h3>
<p>The lead time that matters is the full replenishment time, from the moment stock reaches the reorder point to the moment new stock is available to pick or use:</p>
<ul><li>Time to notice the need and raise the purchase order (review delay).</li>
<li>Supplier processing and production time.</li>
<li>Transit time, including customs for imports.</li>
<li>Receiving, inspection and put-away.</li></ul>
<p>Many companies use the supplier's quoted lead time and are surprised by stock-outs. Measure actual lead times from your purchase order and receipt dates, and track their variation as well as their average.</p>
<h3>Use inventory position, not just on-hand</h3>
<p>Compare the ROP with <strong>inventory position</strong>: on hand + on order − backorders and committed stock. Using only on-hand stock causes duplicate orders: the item stays below the ROP while the first order is in transit, so the system keeps suggesting more.</p>
""", ["Reorder point = demand during lead time + safety stock.", "Measure the full actual lead time, from need to available stock.", "Compare inventory position (on hand + on order − committed) with the ROP."],
 "For five A items, measure actual lead times from your last ten purchase orders. Compare the average and the range with the supplier's quoted lead time.",
 "An item sells 25 units a day, lead time is 8 days and safety stock is 60 units. What is the reorder point?", ["200", "85", "140", "260"], 3,
 "ROP = 25 × 8 + 60 = 200 + 60 = 260 units."),
step("Setting safety stock", 8, """
<p><strong>Safety stock</strong> is extra stock held to cover uncertainty: demand higher than forecast, or a delivery that arrives late. The question is how much, and the answer depends on how variable demand and lead time are and on the service level you want.</p>
<h3>The standard formula (demand variability only)</h3>
<p>Safety stock = z × σ<sub>d</sub> × √L</p>
<ul><li><strong>z</strong> is the service factor for the target cycle service level: about 1.28 for 90%, 1.65 for 95%, 1.96 for 97.5% and 2.33 for 99%.</li>
<li><strong>σ<sub>d</sub></strong> is the standard deviation of demand per period (for example per day), ideally of forecast error rather than raw demand.</li>
<li><strong>L</strong> is the lead time in the same periods.</li></ul>
<p>Example: daily demand varies with a standard deviation of 12 units, lead time is 10 days and the target is 95%. Safety stock = 1.65 × 12 × √10 ≈ 1.65 × 12 × 3.16 ≈ 63 units. With average demand of 40 units a day, the reorder point is 400 + 63 = 463 units.</p>
<h3>When lead time varies too</h3>
<p>If lead times vary, safety stock must cover that as well. A common formula combines both sources: z × √(L × σ<sub>d</sub>² + d² × σ<sub>L</sub>²), where d is average demand per period and σ<sub>L</sub> is the standard deviation of lead time. Unreliable suppliers can require much more safety stock than variable demand.</p>
<h3>Why service level choices matter</h3>
<p>Safety stock rises steeply as the target nears 100%. Going from 95% to 99% needs about 40% more safety stock (2.33 ÷ 1.65). Set high targets for items and customers where stock-outs are costly, and lower targets where they are not.</p>
<p>Review safety stocks at least quarterly. They are not set-and-forget numbers. For more worked examples see the Insights articles on <a href="../post/setting-safety-stock.html">setting safety stock</a> and <a href="../post/safety-stock-for-manufacturers.html">safety stock for manufacturers</a>.</p>
""", ["Safety stock = z × σd × √L when demand is the main uncertainty.", "Variable lead times can require much more safety stock.", "Safety stock rises steeply as service targets approach 100%."],
 "For one A item, find the standard deviation of daily or weekly demand and the lead time, and calculate safety stock at 95%. Compare it with the safety stock in your system.",
 "Raising the target service level from 95% to 99% changes z from about 1.65 to about 2.33. Roughly how much more safety stock is needed?", ["About 4% more", "Twice as much", "No change", "About 40% more"], 3,
 "Safety stock is proportional to z, and 2.33 ÷ 1.65 ≈ 1.41, so about 40% more is needed."),
step("How much to order: EOQ and real-world constraints", 8, """
<p>The reorder point says when to order. The order quantity says how much. Ordering large amounts rarely means fewer orders and less ordering effort but more cycle stock; ordering small amounts often means the opposite. The <strong>economic order quantity (EOQ)</strong> finds the balance.</p>
<p>EOQ = √(2 × D × S ÷ H)</p>
<ul><li><strong>D</strong> is annual demand in units.</li>
<li><strong>S</strong> is the cost to place and receive one order: purchasing time, receiving, inspection and invoice processing. For manufactured items, the setup cost.</li>
<li><strong>H</strong> is the annual cost of holding one unit: unit cost × carrying cost rate.</li></ul>
<p>Example: annual demand is 10,000 units, each order costs $60 to process and a unit costs $18 with a 25% carrying rate, so H = $4.50. EOQ = √(2 × 10,000 × 60 ÷ 4.50) ≈ √266,667 ≈ 516 units, about 19 orders a year.</p>
<h3>EOQ is a starting point</h3>
<p>The total cost curve is flat near the EOQ, so rounding to a convenient quantity costs little. Then adjust for real constraints:</p>
<ul><li><strong>Minimum order quantities</strong> and pack sizes from the supplier.</li>
<li><strong>Price breaks:</strong> compare the saving on price with the extra carrying cost of the larger order.</li>
<li><strong>Shelf life</strong> and storage space.</li>
<li><strong>Freight:</strong> full pallets or full truckloads may be worth more than a small move away from EOQ.</li></ul>
<h3>Reduce the cost of ordering</h3>
<p>The most powerful lever is not the formula but S. If blanket orders, supplier-managed replenishment or automated purchase orders cut the cost per order, EOQ falls, orders become smaller and more frequent, and cycle stock drops. The same logic drives quick changeovers in manufacturing. The lab after this lesson calculates safety stock, reorder point and EOQ together.</p>
""", ["EOQ = √(2DS ÷ H) balances ordering cost against holding cost.", "Treat EOQ as a starting point and adjust for MOQs, price breaks, shelf life and freight.", "Cutting the cost per order lowers EOQ and cycle stock."],
 "Calculate EOQ for one item using your own estimates of ordering cost and carrying rate. Compare it with how much you actually order, and list the constraints that explain any gap.",
 "If the cost of placing an order falls sharply, what happens to EOQ?", ["It falls, so orders become smaller and more frequent", "It rises", "It stays the same", "It becomes zero"], 0,
 "EOQ is proportional to the square root of ordering cost, so cheaper orders lead to smaller, more frequent orders."),
step("Replenishment methods: reorder point, periodic review and min-max", 7, """
<p>How often you check stock shapes how you order. There are three common approaches.</p>
<table><thead><tr><th>Method</th><th>How it works</th><th>Fits</th></tr></thead><tbody>
<tr><td>Continuous review (reorder point, order quantity)</td><td>Stock is checked after every transaction; when inventory position hits the ROP, order a fixed quantity such as EOQ</td><td>A items and items with a good system; lower safety stock</td></tr>
<tr><td>Periodic review (order-up-to)</td><td>Every fixed period, such as each Monday, order enough to bring inventory position up to a target level</td><td>Items bought from the same supplier on a set schedule; consolidated freight</td></tr>
<tr><td>Min-max</td><td>When stock falls to or below min, order enough to reach max</td><td>Simple systems, MRO and C items</td></tr>
<tr><td>Two-bin (kanban)</td><td>When the first bin empties, it triggers a refill while you use the second</td><td>Cheap, steady items at the point of use</td></tr>
</tbody></table>
<h3>The trade-off of periodic review</h3>
<p>With periodic review, safety stock must cover the review period plus the lead time, because you might drop just after a review and not order until the next one. Weekly review with a 10-day lead time means protecting about 15 working days, not 10. That means more safety stock, but it allows one consolidated order per supplier per week, which can cut freight and ordering effort.</p>
<h3>Setting the target levels</h3>
<ul><li>For periodic review: order-up-to level = demand over (review period + lead time) + safety stock for that period.</li>
<li>For min-max: min is the reorder point; max is min plus a sensible order quantity.</li></ul>
<p>Whichever method you use, the parameters must be recalculated as demand and lead times change. Parameters set years ago and never reviewed are one of the most common causes of both excess stock and shortages.</p>
""", ["Continuous review needs less safety stock; periodic review consolidates orders.", "Periodic review safety stock must cover the review period plus lead time.", "Recalculate replenishment parameters as demand and lead times change."],
 "List your top suppliers and decide for each whether continuous or periodic review fits better. For one periodic-review supplier, calculate the protection period (review + lead time).",
 "An item is reviewed weekly (5 working days) and has a 10-day lead time. What period must safety stock protect?", ["5 days", "10 days", "15 days", "50 days"], 2,
 "Under periodic review, safety stock covers the review period plus the lead time: 5 + 10 = 15 days."),
]

M5 = [
step("Working with suppliers to cut lead time and variability", 7, """
<p>Safety stock and cycle stock both depend on suppliers: how long they take, how reliably they deliver and how small an order they accept. Working with key suppliers is often the biggest lever on inventory.</p>
<h3>Measure supplier performance</h3>
<table><thead><tr><th>Measure</th><th>Definition</th></tr></thead><tbody>
<tr><td>On-time in-full (OTIF)</td><td>Share of order lines delivered on the agreed date in the full quantity</td></tr>
<tr><td>Lead time average and variation</td><td>From purchase order to receipt, from your own records</td></tr>
<tr><td>Quality</td><td>Share of receipts with defects or rejections</td></tr>
</tbody></table>
<p>Share the results with suppliers each quarter. Many delivery problems come from unclear expectations on both sides.</p>
<h3>Levers to discuss</h3>
<ul><li><strong>Share forecasts</strong> for the next three to six months so suppliers can plan capacity.</li>
<li><strong>Blanket orders</strong> with scheduled releases cut ordering effort and secure capacity.</li>
<li><strong>Smaller, more frequent deliveries</strong> for high-volume items, sometimes on a fixed weekly run.</li>
<li><strong>Vendor-managed inventory (VMI)</strong> or consignment, where the supplier manages or owns stock at your site.</li>
<li><strong>Local or second sources</strong> for items with long, variable import lead times.</li></ul>
<h3>Total cost, not unit price</h3>
<p>A cheaper overseas supplier with a 12-week, variable lead time may cost more in total than a local one with a 2-week lead time, once safety stock, cycle stock, freight, duties, expediting and stock-out risk are counted. Compare suppliers on total landed cost and inventory impact, not purchase price alone.</p>
""", ["Measure OTIF, lead time and its variation, and quality for key suppliers.", "Share forecasts and use blanket orders, smaller deliveries or VMI.", "Compare suppliers on total cost, including the inventory a long lead time requires."],
 "Calculate OTIF and lead time variation for your top three suppliers over the last six months. Pick one improvement to discuss with each at your next meeting.",
 "Why can a supplier with a lower unit price cost more in total?", ["Lower prices always mean lower quality", "Longer, more variable lead times require more safety and cycle stock and cause expediting", "Freight is always free from local suppliers", "Unit price does not affect cost of goods sold"], 1,
 "Long, variable lead times raise inventory and expediting costs, which can outweigh a lower unit price."),
step("Manufacturers: MRP and bill of materials accuracy", 8, """
<p>Manufacturers plan components differently from finished goods. <strong>Material requirements planning (MRP)</strong> works out what to buy and make, and when, from three inputs:</p>
<ol><li><strong>The master production schedule (MPS):</strong> which finished products to make, how many and when.</li>
<li><strong>The bill of materials (BOM):</strong> which components, and how many of each, go into each product.</li>
<li><strong>Inventory records:</strong> what is on hand and on order.</li></ol>
<p>MRP explodes the MPS through the BOM to get <strong>gross requirements</strong> for each component, subtracts on-hand and scheduled receipts to get <strong>net requirements</strong>, and offsets by lead time to suggest when to release orders.</p>
<h3>Example</h3>
<p>A plant plans 500 cabinets in week 6. Each cabinet uses 4 hinges. Gross requirement: 2,000 hinges in week 6. With 600 on hand and 400 on order arriving in week 3, net requirement is 1,000. With a 3-week lead time, the purchase order for 1,000 hinges, rounded up to the supplier's pack size, must be released in week 3.</p>
<h3>Garbage in, garbage out</h3>
<p>MRP is only as good as its data. The most common problems:</p>
<ul><li><strong>BOM errors:</strong> wrong quantities, missing parts or outdated revisions. Aim for very high BOM accuracy, verified by audits against actual builds.</li>
<li><strong>Inventory inaccuracy</strong>, covered earlier.</li>
<li><strong>Unrealistic lead times</strong> or schedules that exceed capacity.</li>
<li><strong>Unrecorded scrap and substitutions</strong> on the shop floor.</li></ul>
<p>Planners who do not trust the system build spreadsheets and buffers around it, which raises inventory and hides the data problems. Fix the data, then trust the system. The Insights article on <a href="../post/demystifying-mrp-a-comprehensive-guide-to-the-material-requirements-planning-process.html">MRP</a> covers the logic in more detail.</p>
""", ["MRP combines the production schedule, BOMs and inventory records.", "It nets requirements against stock and offsets them by lead time.", "MRP fails without accurate BOMs, inventory and lead times."],
 "Pick one finished product and walk its BOM on the shop floor against an actual build. List any differences in parts or quantities and who should correct them.",
 "A product plan needs 300 units in week 8. Each uses 2 brackets. 150 brackets are on hand and none on order. Lead time is 2 weeks. What should MRP suggest?", ["Order 600 brackets in week 8", "Order 300 brackets in week 6", "Order 450 brackets in week 6", "Order 150 brackets in week 2"], 2,
 "Gross need is 600; net of 150 on hand is 450; offsetting a 2-week lead time from week 8 gives a release in week 6."),
step("Systems, barcodes and data discipline", 7, """
<p>Inventory methods need a system to run them. For many SMEs that starts in accounting software or a spreadsheet and grows into an ERP system, sometimes with a warehouse management system (WMS) for larger or more complex warehouses.</p>
<table><thead><tr><th>Capability</th><th>Why it matters</th></tr></thead><tbody>
<tr><td>Item master with units of measure, lead times and replenishment parameters</td><td>Holds the rules the system uses to suggest orders</td></tr>
<tr><td>Locations and bins</td><td>Tells people where stock is, so picks and counts are accurate</td></tr>
<tr><td>Barcode or RFID scanning</td><td>Captures receipts, moves and picks at the moment they happen, with far fewer errors than typing</td></tr>
<tr><td>Purchase suggestions from reorder points or MRP</td><td>Turns your policy into daily actions</td></tr>
<tr><td>Cycle count programme</td><td>Schedules counts by class and records discrepancies</td></tr>
<tr><td>Reports by class</td><td>Turns, fill rate, excess, accuracy and forecast error</td></tr>
</tbody></table>
<h3>Data discipline beats features</h3>
<p>Most inventory systems underperform because of data, not software. Common gaps: missing or wrong lead times, replenishment parameters never updated, units of measure mixed up, and transactions recorded hours or days after the event. Assign an owner to the item master, set rules for creating and changing items, and review parameters on a schedule.</p>
<h3>Before you buy a new system</h3>
<p>Fix what you can in the current one first: clean the item master, add bin locations, start cycle counting and set parameters by class. You will learn what you really need, and a new system will start with clean data instead of migrating the old problems. When you do select a system, script demonstrations around your own processes and data rather than the vendor's standard demo.</p>
""", ["Systems turn inventory policy into daily actions.", "Scan transactions at the moment they happen.", "Data discipline and an item-master owner matter more than features."],
 "Check ten items in your item master: lead time, unit of measure, reorder point and safety stock. How many are missing or clearly out of date?",
 "A company plans to buy a new ERP because its inventory data is unreliable. What should it do first?", ["Buy the system with the most features", "Migrate all existing data as it is", "Stop recording transactions until the new system arrives", "Clean the item master and fix transaction discipline in the current system"], 3,
 "Fixing data and discipline first shows what is really needed and avoids migrating the same problems into a new system."),
step("Your 90-day inventory improvement plan", 7, """
<p>Inventory improvement works best as a short, focused programme with clear measures. Here is a 90-day plan that fits most SMEs.</p>
<table><thead><tr><th>Days</th><th>Focus</th><th>Actions</th></tr></thead><tbody>
<tr><td>1–30</td><td>Baseline and foundations</td><td>Measure turns, fill rate, accuracy and excess by class; run ABC and XYZ; start cycle counting A items; estimate your carrying cost rate</td></tr>
<tr><td>31–60</td><td>Policies and parameters</td><td>Write the class policy; measure actual lead times; recalculate reorder points, safety stock and order quantities for A and B items; act on the five largest excess items</td></tr>
<tr><td>61–90</td><td>Routines and suppliers</td><td>Start the monthly planning meeting; review forecast error and bias; agree improvements with the top three suppliers; set the quarterly review cycle</td></tr>
</tbody></table>
<h3>Set targets in pairs</h3>
<p>For example: raise turns from 4 to 5 <em>and</em> keep fill rate at or above 97 percent; raise inventory accuracy to 95 percent; cut excess and obsolete stock by a third. Report progress monthly by class.</p>
<h3>Common traps</h3>
<ul><li><strong>Across-the-board cuts:</strong> "reduce inventory 20 percent" without class rules usually cuts the wrong items and causes stock-outs.</li>
<li><strong>Ignoring data:</strong> new parameters on inaccurate records give confident wrong answers.</li>
<li><strong>One-time projects:</strong> parameters drift back if nobody owns the quarterly review.</li></ul>
<h3>Where to go next</h3>
<p>If your shortages come from internal processes rather than inventory rules, such as order errors, long changeovers or erratic production, the Lean Six Sigma and Operational Excellence courses address those causes. The Excel template from the Insights inventory series is a practical place to run your first ABC and safety-stock calculations.</p>
""", ["Run inventory improvement as a 90-day programme with a clear baseline.", "Set targets in pairs: stock and service together.", "Avoid across-the-board cuts and give someone ownership of the quarterly review."],
 "Fill in the 90-day table with your own dates, owners and the three measures you will report monthly.",
 "Why is an across-the-board 20% inventory cut risky?", ["It cuts the wrong items and causes stock-outs when there are no class rules", "It always increases carrying cost", "It is illegal in Canada", "It has no effect on cash"], 0,
 "Without class-based rules, blanket cuts often remove stock that was needed while leaving excess elsewhere."),
]

course = dict(
 id="inventory-management-for-smes",
 title="Inventory Management for SMEs: Service, Stock and Cash",
 tagline="Hold the right stock in the right amount: classify items, forecast demand and set reorder points, safety stock and order quantities.",
 summary="A practical inventory course for owners, buyers, planners and operations managers in small and mid-sized distributors and manufacturers. You will learn what inventory really costs, how to measure it, how to classify items with ABC and XYZ analysis, how to forecast simply and measure forecast error, and how to set reorder points, safety stock and order quantities. It closes with supplier collaboration, MRP basics for manufacturers, system and data discipline, and a 90-day improvement plan.",
 audience=["Owners and general managers of distributors, wholesalers and manufacturers",
           "Buyers, planners and purchasing managers who decide what to order and when",
           "Warehouse and operations managers responsible for stock accuracy and service",
           "Finance staff who want to understand the cash tied up in inventory"],
 outcomes=["Estimate carrying cost and measure turns, days on hand, fill rate, accuracy and excess",
           "Run ABC and XYZ analysis and set a different policy for each class",
           "Clean demand history, forecast with simple methods and track error and bias",
           "Calculate reorder points, safety stock and economic order quantities",
           "Choose between continuous review, periodic review, min-max and two-bin methods",
           "Improve inventory through suppliers, MRP data, system discipline and a 90-day plan"],
 modules=[
  dict(title="Inventory Basics", summary="Why inventory matters, what it costs, the types of inventory and their purposes, the measures that matter and how to keep records accurate.", steps=M1),
  dict(title="Classifying Items", summary="ABC analysis by value, XYZ analysis by demand variability, policies for each class and how to handle slow-moving and obsolete stock.", steps=M2),
  dict(title="Demand and Forecasting", summary="Demand patterns, simple forecasting methods, forecast error and bias, and a monthly sales and operations planning routine.", steps=M3),
  dict(title="When and How Much to Order", summary="Reorder points and real lead times, safety stock, economic order quantity and the main replenishment methods.", steps=M4),
  dict(title="Improve and Sustain", summary="Supplier collaboration, MRP and bill-of-materials accuracy, systems and data discipline, and a 90-day improvement plan.", steps=M5)],
 labs=[
  dict(id="inv-stock-purpose", type="classify", title="Why is this stock here?", after_step=2,
       intro="Sort twelve situations from a distributor and a manufacturer by the purpose of the stock, then check your answers. Knowing why stock exists tells you which lever reduces it.",
       config=dict(categories=["Cycle stock", "Safety stock", "Anticipation stock", "Excess or obsolete"], items=[
        dict(text="A full pallet of cleaning supplies bought because the supplier ships only by the pallet", answer=0, why="Stock that exists because you buy in batches larger than immediate need is cycle stock."),
        dict(text="A month's supply of resin bought in one order to get a better price", answer=0, why="Buying a batch for price or ordering efficiency creates cycle stock; weigh the saving against carrying cost."),
        dict(text="Production of 2,000 units in one run to avoid a long changeover", answer=0, why="Large production batches driven by setup time are cycle stock; quicker changeovers reduce it."),
        dict(text="Extra filters held in case a large customer orders more than forecast", answer=1, why="Stock held against demand uncertainty is safety stock."),
        dict(text="A buffer of imported parts because the ocean shipment is often a week late", answer=1, why="Stock that covers supply uncertainty is safety stock."),
        dict(text="Minimum stock kept of a critical spare part for the packaging line", answer=1, why="Holding a minimum to protect against an uncertain breakdown is safety stock (often for critical MRO items)."),
        dict(text="Air conditioners received in April ahead of summer demand", answer=2, why="Stock built ahead of a known seasonal peak is anticipation stock."),
        dict(text="Products built up before a planned two-week plant shutdown", answer=2, why="Stock built to cover a planned shutdown is anticipation stock."),
        dict(text="Extra inventory of a product ahead of a planned promotion", answer=2, why="Building for a known promotion is anticipation stock."),
        dict(text="Labels printed with an old logo after the rebrand", answer=3, why="Stock that can no longer be used as intended is obsolete."),
        dict(text="Three years of supply of a slow-selling item bought for a volume discount", answer=3, why="Far more than needed for the foreseeable future is excess stock; check months of supply before large buys."),
        dict(text="Parts left over after a customer cancelled its custom product", answer=3, why="Customer-specific stock with no remaining demand is obsolete; agree commitments in writing to prevent it."),
       ])),
  dict(id="inv-abc-xyz-matrix", type="matrix", title="Value and variability: where each item belongs", after_step=6,
       intro="Place seven items on a grid of annual value against demand variability to see which need tight control, which suit simple rules and which need customer collaboration.",
       config=dict(x="Demand variability", y="Annual usage value", x_low="Steady (X)", x_high="Erratic (Z)", y_low="Low value (C)", y_high="High value (A)",
        quadrants=dict(top_left="Automate and review often", top_right="Collaborate with customers", bottom_left="Simple rules", bottom_right="Stock only if needed"),
        items=[dict(name="Best-selling standard fitting", x=1, y=5),
               dict(name="Seasonal heating product", x=3, y=4),
               dict(name="Custom project valve", x=5, y=5),
               dict(name="Packaging tape", x=1, y=1),
               dict(name="Rarely sold spare part", x=5, y=1),
               dict(name="Mid-volume cable assembly", x=2, y=3),
               dict(name="Promotional display kit", x=4, y=2)])),
  dict(id="inv-safety-stock-calculator", type="calc", title="Safety stock, reorder point and order quantity", after_step=15,
       intro="Enter demand, variability, lead time, service level and costs for one item to calculate safety stock, reorder point, economic order quantity and average inventory value.",
       config=dict(calc="safety_stock", note="Uses safety stock = z × σd × √L, which covers demand variability only. If lead times vary, add protection for that too, and round the order quantity to supplier pack sizes and minimums.")),
 ],
 figures=[
  dict(step=4, type="cycle", title="Cycle counting that fixes causes", caption="Click each stage to see what it involves. The loop only pays off when discrepancies lead to process fixes.",
       config=dict(center="Accuracy", stages=[
        dict(label="Schedule", text="Pick today's items by class: A items most often, plus any location that just hit zero."),
        dict(label="Count blind", text="The counter records what is on the shelf without seeing the system quantity."),
        dict(label="Compare", text="Flag counts outside tolerance for investigation; record the result."),
        dict(label="Investigate", text="Trace recent receipts, picks and adjustments to find why the record drifted."),
        dict(label="Fix the cause", text="Correct the record and fix the process step, label or unit of measure that caused it.")])),
  dict(step=5, type="bars", title="ABC analysis: share of annual value by class", caption="Example for a distributor with 1,000 items. A small group of items carries most of the value.",
       config=dict(unit="% of value", items=[dict(label="A items (15% of items)", value=75, highlight=True), dict(label="B items (25% of items)", value=17), dict(label="C items (60% of items)", value=8)],
        note="In this example, 150 A items carry three quarters of annual usage value, so they get the most planning attention.")),
  dict(step=13, type="flow", title="What the real lead time includes", caption="Watch a replenishment move through each stage, then click 'Fix the bottleneck' to see where days are often hidden.",
       config=dict(steps=[
        dict(label="Reach ROP", text="Stock falls to the reorder point."),
        dict(label="Raise PO", text="The buyer notices at the next review and raises a purchase order."),
        dict(label="Supplier", text="The supplier processes, makes or picks the order."),
        dict(label="Transit", text="Goods travel, including customs for imports."),
        dict(label="Receive", text="Goods are received, inspected and put away, ready to use.")], bottleneck=1,
        fix_text="Automated purchase suggestions reviewed daily remove the days lost waiting for a weekly buying review.")),
  dict(step=14, type="bars", title="Safety stock rises steeply near 100%", caption="Safety stock for the same item at different cycle service levels (demand standard deviation 12 units a day, 10-day lead time).",
       config=dict(unit="units", items=[dict(label="90% (z = 1.28)", value=49), dict(label="95% (z = 1.65)", value=63), dict(label="97.5% (z = 1.96)", value=74), dict(label="99% (z = 2.33)", value=88, highlight=True)],
        note="Moving from 95% to 99% adds about 40% more safety stock for the same item.")),
  dict(step=16, type="compare", title="Continuous review vs periodic review", caption="Toggle between the two methods and compare what each needs and what each saves.",
       config=dict(left=dict(title="Continuous review", points=["Stock checked after every transaction", "Order a fixed quantity at the reorder point", "Safety stock covers the lead time only", "Orders go out on any day"]),
                   right=dict(title="Periodic review", points=["Stock checked on a fixed schedule, such as weekly", "Order up to a target level", "Safety stock covers review period plus lead time", "One consolidated order per supplier per cycle"]))),
  dict(step=20, type="timeline", title="A 90-day inventory improvement plan", caption="Click each phase to see its main actions.",
       config=dict(phases=[
        dict(label="Days 1–30", title="Baseline and foundations", items=["Measure turns, fill rate, accuracy, excess", "ABC and XYZ analysis", "Start cycle counting A items"]),
        dict(label="Days 31–60", title="Policies and parameters", items=["Write the class policy", "Measure actual lead times", "Recalculate ROP, safety stock, order quantities", "Act on top excess items"]),
        dict(label="Days 61–90", title="Routines and suppliers", items=["Monthly planning meeting", "Review forecast error and bias", "Supplier improvement agreements", "Quarterly parameter review"])])),
 ],
 exam=[
  E("What is the main balance inventory management tries to strike?", ["Customer service against the cost of holding stock", "Sales commissions against salaries", "Warehouse size against office size", "Supplier count against customer count"], 0, "Inventory management balances having stock to serve customers with the cost of holding it."),
  E("Which is NOT usually part of inventory carrying cost?", ["Cost of capital", "Storage and handling", "Obsolescence and damage", "The sales team's travel budget"], 3, "Carrying cost covers capital, storage, risk and service costs of holding stock, not unrelated expenses."),
  E("Stock held because orders are placed in batches larger than immediate need is called:", ["Safety stock", "Cycle stock", "Anticipation stock", "Pipeline stock"], 1, "Cycle stock results from ordering or producing in batches."),
  E("Annual cost of goods sold is $4.8 million and average inventory at cost is $1.2 million. How many days of stock are held, roughly?", ["30 days", "60 days", "91 days", "120 days"], 2, "Turns = 4.8 ÷ 1.2 = 4; days on hand ≈ 365 ÷ 4 ≈ 91."),
  E("Why should fill rate be reported alongside inventory turns?", ["So that cutting stock does not quietly damage customer service", "Because auditors require it", "Because they are the same measure", "To calculate EOQ"], 0, "Turns and service pull in opposite directions, so tracking both prevents improving one at the expense of the other."),
  E("What is the main benefit of investigating each cycle count discrepancy?", ["It lets the counter skip future counts", "It finds and fixes the process cause of record errors", "It increases inventory value", "It removes the need for barcodes"], 1, "The value of cycle counting is fixing the causes of inaccuracy, not just correcting numbers."),
  E("In ABC analysis, A items are typically:", ["Most items carrying a small share of value", "Items with the most stock-outs", "A small share of items carrying most of the annual usage value", "Items bought from overseas"], 2, "A items are the few items with the highest annual usage value."),
  E("An item's coefficient of variation of monthly demand is 0.3. Which XYZ class does it usually fall in?", ["Z", "Y", "C", "X"], 3, "A CV below about 0.5 indicates steady, predictable demand: class X."),
  E("Which group is usually hardest to manage and may need customer collaboration rather than more stock?", ["AZ: high value, erratic demand", "CX: low value, steady demand", "BX: medium value, steady demand", "CY: low value, variable demand"], 0, "High value combined with erratic demand makes safety stock very expensive."),
  E("What is the difference between cycle service level and fill rate?", ["They are identical", "Cycle service level is the chance of no stock-out per cycle; fill rate is the share of demand met from stock", "Fill rate is set by the supplier", "Cycle service level applies only to C items"], 1, "Cycle service level is used to set safety stock; fill rate measures the share of demand served."),
  E("Before writing off obsolete stock, who should be involved because of financial statement and possible tax effects?", ["Only the warehouse team", "The customer", "Finance and the company's accountant", "The supplier's sales rep"], 2, "Write-downs affect the financial statements, and treatment and timing may have tax implications."),
  E("Sales were zero for two months because the item was out of stock. What should be done before forecasting?", ["Use the zeros as they are", "Delete the item", "Double next month's forecast", "Adjust the history for the stock-out, using orders or estimated lost demand"], 3, "Stock-out periods understate true demand and should be cleaned before forecasting."),
  E("Last forecast 300, actual 360, α = 0.25. What is the new exponentially smoothed forecast?", ["315", "330", "345", "360"], 0, "300 + 0.25 × (360 − 300) = 315."),
  E("Why is bias more damaging than random forecast error?", ["Bias is always larger", "Random error never happens", "Bias accumulates as excess or shortages month after month, while random error tends to average out", "Bias only affects C items"], 2, "Consistent over- or under-forecasting builds up rather than cancelling."),
  E("What is the reorder point for an item with demand of 50 units a day, lead time of 6 days and safety stock of 70 units?", ["300", "370", "120", "420"], 1, "ROP = 50 × 6 + 70 = 370."),
  E("Why should the reorder point be compared with inventory position rather than on-hand stock?", ["On-hand stock is always wrong", "Inventory position includes stock on order, which prevents duplicate orders", "Inventory position excludes safety stock", "Suppliers require it"], 1, "Ignoring stock on order causes repeated suggestions while the first order is in transit."),
  E("Safety stock = 1.65 × 10 × √9. What is it?", ["49.5 units", "16.5 units", "148.5 units", "99 units"], 0, "1.65 × 10 × 3 = 49.5 units."),
  E("Annual demand is 8,000 units, ordering cost is $50 and holding cost is $5 per unit per year. What is the EOQ?", ["200", "283", "400", "800"], 2, "EOQ = √(2 × 8,000 × 50 ÷ 5) = √160,000 = 400."),
  E("Under weekly periodic review with a 2-week lead time, safety stock must cover:", ["1 week", "2 weeks", "Zero weeks", "3 weeks"], 3, "Periodic review protection covers the review period plus the lead time."),
  E("In MRP, what turns gross requirements into net requirements?", ["Multiplying by the safety factor", "Adding the EOQ", "Dividing by lead time", "Subtracting stock on hand and scheduled receipts"], 3, "Net requirements are gross requirements minus available stock and scheduled receipts."),
 ],
)
# balance check helper: keep the answer key spread across positions
if __name__ == "__main__":
    write(course, "inventory-management", __file__)
