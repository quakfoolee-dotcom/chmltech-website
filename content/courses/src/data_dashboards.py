"""Source for content/courses/data-dashboards.json (run: python3 content/courses/src/data_dashboards.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import step, E, write

M1 = [
step("Why data matters, and what good decisions need", 6, """
<p>Most SMEs have more data than they use. Orders, invoices, inventory, timesheets, quotes and customer records sit in accounting software, ERP systems, CRMs and spreadsheets. Turned into a few clear measures, that data shows what is working, what is slipping and where to act.</p>
<h3>Common symptoms of data that isn't working</h3>
<ul><li>Monthly reports take days to assemble by copying and pasting.</li>
<li>Different people quote different numbers for the same thing.</li>
<li>Problems such as falling margins or late deliveries are found weeks after they start.</li>
<li>Decisions rely on gut feel because the numbers are hard to get.</li></ul>
<h3>What good decisions need</h3>
<table><thead><tr><th>Need</th><th>What it means</th></tr></thead><tbody>
<tr><td>The right measures</td><td>A few KPIs linked to goals, not everything that can be counted</td></tr>
<tr><td>Trustworthy data</td><td>Complete, accurate and consistently defined</td></tr>
<tr><td>Timely access</td><td>Available when the decision is made, ideally automatically refreshed</td></tr>
<tr><td>Clear presentation</td><td>Easy to read in seconds, showing trends and targets</td></tr>
<tr><td>A routine</td><td>Regular reviews where data leads to actions</td></tr>
</tbody></table>
<h3>Start small</h3>
<p>You don't need a data warehouse or a data scientist to start. A handful of well-defined KPIs, clean spreadsheets or a basic business intelligence tool, and a monthly review meeting deliver most of the value. This course walks through each step, from choosing KPIs to building and using dashboards.</p>
""", ["SMEs usually have plenty of data that is hard to use.", "Good decisions need the right measures, trustworthy data, timely access, clear presentation and a routine.", "Start small with a few KPIs and a regular review."],
 "List the reports your business produces each month, how long each takes and who uses them. Mark the ones that lead to decisions.",
 "Which is a common sign that a business's data isn't working?", ["KPIs are reviewed every month", "Different people quote different numbers for the same measure", "Reports refresh automatically", "Each KPI has a clear definition"], 1,
 "Conflicting numbers point to inconsistent definitions or sources."),
step("Choosing KPIs that matter", 7, """
<p>A <strong>key performance indicator (KPI)</strong> is a measure that tells you whether you are achieving an important goal. The word "key" matters: a business with 60 KPIs effectively has none.</p>
<h3>Start from goals</h3>
<p>Begin with your business goals, then ask: what would tell us we are on track? A goal to grow profitably might lead to KPIs for revenue, gross margin percentage and new customers. A goal to improve service might lead to on-time delivery and complaint rate.</p>
<h3>A KPI tree</h3>
<p>Break a top-level result into the drivers that cause it. Profit depends on revenue and costs; revenue depends on number of customers, order frequency and average order value; and so on. A KPI tree shows managers which driver they control and how it links to the result.</p>
<h3>Leading and lagging</h3>
<p>Lagging indicators, such as monthly revenue and profit, show results. Leading indicators, such as quotes sent, pipeline value, on-time delivery or machine downtime, predict them. Include both.</p>
<h3>Define every KPI</h3>
<table><thead><tr><th>Field</th><th>Example: on-time delivery</th></tr></thead><tbody>
<tr><td>Definition</td><td>Order lines delivered complete on or before the promised date ÷ all order lines delivered</td></tr>
<tr><td>Data source</td><td>ERP sales order lines and shipment dates</td></tr>
<tr><td>Frequency</td><td>Weekly, with a monthly trend</td></tr>
<tr><td>Owner</td><td>Operations manager</td></tr>
<tr><td>Target</td><td>95%</td></tr>
</tbody></table>
<h3>Avoid vanity metrics</h3>
<p>Some numbers look good but don't drive decisions, such as total website visits or social media followers. Ask of each KPI: if this changed, would we do something differently? If not, drop it. The lab after this lesson asks you to spot useful KPIs.</p>
""", ["Start from goals and keep KPIs few.", "Use a KPI tree to link drivers to results; include leading and lagging indicators.", "Define each KPI's formula, source, frequency, owner and target."],
 "Pick one business goal and draw a KPI tree with three levels. Write a full definition for the two most useful KPIs.",
 "What question best tests whether a measure deserves to be a KPI?", ["Is it easy to collect?", "If it changed, would we do something differently?", "Does it make us look good?", "Do competitors track it?"], 1,
 "A KPI should drive decisions; if it doesn't, it's not key."),
step("Where your data lives", 7, """
<p>Before building reports, map where the data comes from. In most SMEs it is spread across several systems.</p>
<table><thead><tr><th>Source</th><th>Typical data</th></tr></thead><tbody>
<tr><td>Accounting software</td><td>Invoices, payments, expenses, financial statements</td></tr>
<tr><td>ERP or operations system</td><td>Orders, inventory, purchasing, production, shipping</td></tr>
<tr><td>CRM</td><td>Leads, opportunities, quotes, customer activity</td></tr>
<tr><td>Spreadsheets</td><td>Plans, trackers, manual logs, anything not in a system</td></tr>
<tr><td>Website and marketing tools</td><td>Visits, enquiries, campaign results</td></tr>
<tr><td>Shop floor or equipment</td><td>Output counts, downtime, quality checks</td></tr>
<tr><td>Payroll and timekeeping</td><td>Hours, labour cost, overtime</td></tr>
</tbody></table>
<h3>Map your data</h3>
<p>For each KPI, record which system holds the data, who maintains it, how it can be extracted (built-in report, export to file, direct connection) and how often it changes. This map shows where the reporting effort goes and which sources need connecting.</p>
<h3>One version of the truth</h3>
<p>When the same information is kept in two places, such as customer lists in the CRM and in accounting, they drift apart. Decide which system is the <strong>system of record</strong> for each type of data: customers, products, prices, inventory. Other systems should take their data from it, ideally through an integration, rather than being updated by hand.</p>
<h3>Spreadsheets as a warning sign</h3>
<p>Spreadsheets are flexible and useful, but critical business data kept only in personal spreadsheets is fragile: it can be lost, overwritten or understood only by one person. When a spreadsheet becomes essential to running the business, consider moving that process into a system. The lab after this lesson asks you to prioritize which KPIs to automate first.</p>
""", ["Map each KPI to its source system, owner and extraction method.", "Name one system of record for each type of data.", "Critical data kept only in personal spreadsheets is a risk."],
 "Make a table of your top ten KPIs with their source systems and how the data is extracted today. Mark any that depend on one person's spreadsheet.",
 "What is a system of record?", ["The system with the most users", "The authoritative source for a type of data that other systems should rely on", "A backup copy", "Any spreadsheet"], 1,
 "Each data type should have one authoritative source to avoid conflicting versions."),
step("Data quality basics", 7, """
<p>A dashboard built on poor data gives confident wrong answers. Data quality is the unglamorous foundation of good reporting.</p>
<h3>Dimensions of data quality</h3>
<table><thead><tr><th>Dimension</th><th>Question</th><th>Example problem</th></tr></thead><tbody>
<tr><td>Completeness</td><td>Is anything missing?</td><td>Orders without a promised date, so on-time delivery cannot be measured</td></tr>
<tr><td>Accuracy</td><td>Does it match reality?</td><td>System inventory differs from what is on the shelf</td></tr>
<tr><td>Consistency</td><td>Is it recorded the same way everywhere?</td><td>"ABC Ltd", "A.B.C. Limited" and "ABC" as three customers</td></tr>
<tr><td>Timeliness</td><td>Is it up to date?</td><td>Timesheets entered a week late</td></tr>
<tr><td>Validity</td><td>Does it follow the rules?</td><td>Dates in the future, negative quantities</td></tr>
</tbody></table>
<h3>Master data</h3>
<p>Master data is the core reference data used across transactions: customers, suppliers, products, prices, units of measure. Errors here spread into every report. Assign an owner to each type of master data, set rules for creating and changing records (for example, check for duplicates before adding a customer) and review it regularly.</p>
<h3>Fix at the source</h3>
<p>Cleaning data every month in a spreadsheet treats the symptom. Fix the cause: make key fields mandatory in the system, use drop-down lists instead of free text, train staff on why the data matters and give feedback when errors occur.</p>
<h3>Measure it</h3>
<p>Track a few quality measures, such as the share of orders with a promised date or duplicate customer records, and show them alongside the KPIs they affect. Data quality improves when someone owns it and it is visible.</p>
""", ["Check completeness, accuracy, consistency, timeliness and validity.", "Give master data owners and rules for creating and changing records.", "Fix errors at the source with mandatory fields, drop-downs and training."],
 "Pick one important report and check 20 records for the five quality dimensions. List the top problem and how to fix it at the source.",
 "The same customer appears as 'ABC Ltd', 'A.B.C. Limited' and 'ABC'. Which data quality dimension is affected?", ["Timeliness", "Validity", "Consistency", "Completeness"], 2,
 "Recording the same thing in different ways is a consistency problem."),
]

M2 = [
step("Structuring data in tables", 7, """
<p>Most spreadsheet pain comes from how the data is laid out. Analysis tools work best with data arranged as a simple table, often called <strong>tidy data</strong>.</p>
<h3>Rules for a good data table</h3>
<ul><li><strong>One row per record:</strong> one order line, one invoice, one shipment.</li>
<li><strong>One column per field:</strong> date, customer, product, quantity, price.</li>
<li><strong>One header row</strong> with clear, unique names.</li>
<li><strong>No merged cells, blank rows or subtotals</strong> inside the data.</li>
<li><strong>One type of data per column:</strong> dates as dates, numbers as numbers.</li>
<li><strong>Raw data separate from reports:</strong> keep data on one sheet and summaries on others.</li></ul>
<h3>Wide versus long</h3>
<p>A common layout puts months across columns: Customer, Jan, Feb, Mar and so on. It looks like a report but is hard to analyze. The tidy version has columns Customer, Month and Sales, with one row per customer per month. It is longer but much easier to filter, total, chart and refresh.</p>
<h3>Why it matters</h3>
<p>Tidy tables can be summarized instantly with pivot tables, loaded into business intelligence tools and refreshed by adding new rows. Report-style layouts must be rebuilt by hand each month, which is slow and error-prone.</p>
<h3>Use Excel tables</h3>
<p>In Excel, format a data range as a table (Insert, Table). Tables expand automatically as rows are added, keep formulas consistent and make references readable, which reduces errors in formulas and pivot tables.</p>
""", ["Keep one row per record and one column per field, with no merged cells or subtotals.", "Prefer long (tidy) layouts over months-across-columns.", "Separate raw data from reports and format data as Excel tables."],
 "Take one spreadsheet you update monthly and restructure its data into a tidy table on a separate sheet. Build the report from it.",
 "Which layout is easiest to analyze and refresh?", ["One row per customer with a column for each month", "One row per customer per month with columns Customer, Month, Sales", "Merged header cells with subtotals inside the data", "A different sheet for every month"], 1,
 "Tidy, long tables are simplest to filter, summarize and refresh."),
step("Essential spreadsheet skills: lookups and pivot tables", 8, """
<p>A few spreadsheet features do most of the work in SME reporting.</p>
<h3>Lookups</h3>
<p>Lookups bring data from one table into another using a shared key, such as a product code. In current versions of Excel, <strong>XLOOKUP</strong> is the simplest: <em>=XLOOKUP(A2, Products[Code], Products[Category], "Not found")</em> returns the category for the product code in A2. Older versions use VLOOKUP or INDEX/MATCH. Lookups let you add customer type, product category or region to transaction data for analysis.</p>
<h3>Pivot tables</h3>
<p>A <strong>pivot table</strong> summarizes a data table in seconds: total sales by month and region, average order value by customer type, count of late shipments by carrier. Drag fields into rows, columns, values and filters. Change the view without writing formulas. When the data table grows, refresh the pivot table.</p>
<h3>Other useful features</h3>
<table><thead><tr><th>Feature</th><th>Use</th></tr></thead><tbody>
<tr><td>SUMIFS, COUNTIFS, AVERAGEIFS</td><td>Totals that meet conditions, such as sales for one region in one month</td></tr>
<tr><td>Conditional formatting</td><td>Highlight values above or below targets</td></tr>
<tr><td>Data validation</td><td>Drop-down lists that prevent inconsistent entries</td></tr>
<tr><td>Charts from pivot tables</td><td>Visuals that update with the data</td></tr>
<tr><td>Slicers</td><td>Clickable filters for pivot tables and charts</td></tr>
</tbody></table>
<h3>Let AI help</h3>
<p>AI assistants can write and explain formulas: describe what you need in plain language and test the result on rows where you know the answer. The Prompting and AI Productivity course covers this.</p>
""", ["Use XLOOKUP (or VLOOKUP/INDEX-MATCH) to combine tables by a shared key.", "Pivot tables summarize data in seconds without formulas.", "Use SUMIFS, conditional formatting, data validation and slicers."],
 "Build a pivot table from a tidy sales table showing sales by month and customer type, add a slicer for region, and check one total against your accounting report.",
 "What is a pivot table mainly used for?", ["Drawing logos", "Summarizing a data table quickly by different fields", "Writing emails", "Protecting a file with a password"], 1,
 "Pivot tables summarize and regroup data without formulas."),
step("Cleaning and combining data automatically", 7, """
<p>Monthly reports often start with the same chore: export files from several systems, delete header rows, fix dates, remove duplicates, combine sheets and add lookups. Doing this by hand every month wastes hours and invites mistakes.</p>
<h3>Power Query</h3>
<p>Excel and Power BI include <strong>Power Query</strong>, a tool that records the steps you take to clean and combine data, then repeats them with one click when new data arrives. Typical steps:</p>
<ul><li>Load an export file or a whole folder of monthly files.</li>
<li>Remove extra rows and columns, rename headers.</li>
<li>Change data types: text to dates, text to numbers.</li>
<li>Split or merge columns, trim spaces, standardize text.</li>
<li>Remove duplicates and filter out unwanted records.</li>
<li>Merge with other tables, such as adding product categories.</li>
<li>Append files with the same layout, such as twelve monthly exports.</li></ul>
<h3>Example</h3>
<p>A distributor exports sales from its ERP each month into a folder. A Power Query connected to the folder combines all files, fixes dates, adds product category and customer region from lookup tables and loads one tidy table. The monthly report now takes a minute to refresh instead of half a day.</p>
<h3>Good practice</h3>
<ul><li>Keep source files in a consistent folder and format.</li>
<li>Name query steps clearly so others can follow them.</li>
<li>Check row counts and totals after each refresh against the source system.</li>
<li>Document what each query does and who maintains it.</li></ul>
""", ["Automate repeated cleaning and combining steps instead of doing them by hand.", "Power Query records steps and re-runs them on new data.", "Check row counts and totals after each refresh and document queries."],
 "Pick one report you build from exports every month. List every manual cleaning step, then rebuild them in Power Query and time the next refresh.",
 "What is the main benefit of Power Query for monthly reports?", ["It makes charts more colourful", "It records cleaning steps and repeats them automatically on new data", "It replaces the accounting system", "It sends emails"], 1,
 "Repeatable, recorded steps save time and reduce errors."),
step("Avoiding spreadsheet errors", 7, """
<p>Spreadsheet errors are common and can be costly: a wrong formula in a pricing sheet or a broken link in a forecast can go unnoticed for months. A few habits prevent most of them.</p>
<h3>Common errors</h3>
<table><thead><tr><th>Error</th><th>Example</th></tr></thead><tbody>
<tr><td>Hard-coded numbers in formulas</td><td>=B2*1.13 when the rate should come from an input cell</td></tr>
<tr><td>Ranges that miss new rows</td><td>SUM(B2:B100) after data grows to row 140</td></tr>
<tr><td>Copy-paste errors</td><td>A formula copied down with a reference that should have been fixed</td></tr>
<tr><td>Inconsistent formulas</td><td>One cell in a column overwritten with a typed value</td></tr>
<tr><td>Version confusion</td><td>"Budget_final_v3_REAL.xlsx" emailed around</td></tr>
<tr><td>Broken links</td><td>References to files that moved or were renamed</td></tr>
</tbody></table>
<h3>Good habits</h3>
<ul><li><strong>Separate inputs, calculations and outputs</strong>, with inputs clearly marked.</li>
<li><strong>Use Excel tables and named ranges</strong> so formulas adjust to new data.</li>
<li><strong>Add check totals:</strong> for example, total by region should equal the grand total; show a warning if not.</li>
<li><strong>Keep one shared master copy</strong> in a shared drive or cloud folder with version history, instead of emailing copies.</li>
<li><strong>Protect formula cells</strong> in sheets others fill in.</li>
<li><strong>Have someone else review</strong> important models before decisions are made on them.</li></ul>
<h3>Know when to move on</h3>
<p>When a spreadsheet is used by many people at once, holds critical data or needs an audit trail, it may be time for a proper system or a business intelligence tool. Spreadsheets are excellent for analysis and prototypes; they are risky as the backbone of operations.</p>
""", ["Watch for hard-coded numbers, short ranges, copy errors and version confusion.", "Separate inputs, calculations and outputs, use tables and add check totals.", "Keep one shared master with version history and review important models."],
 "Review one important spreadsheet for the six common errors. Add at least one check total and move any hard-coded rates into input cells.",
 "Why is '=B2*1.13' a risky formula?", ["It is too short", "The rate is hard-coded; if it changes, every formula must be found and edited", "Multiplication is not allowed", "It will not calculate"], 1,
 "Hard-coded values hide assumptions and are easily missed when they change."),
]

M3 = [
step("Designing a dashboard people use", 7, """
<p>A dashboard is a one-screen view of the measures a person or team needs to make decisions. Good design is about the audience and their questions, not about fitting in as many charts as possible.</p>
<h3>Start with the audience and questions</h3>
<ul><li>Who will use it: the owner, a sales manager, a shift supervisor?</li>
<li>What decisions do they make, and how often?</li>
<li>What three to five questions should the dashboard answer at a glance? For example: Are we on track for the month? Which customers are slipping? Where are late orders building up?</li></ul>
<h3>Layout principles</h3>
<ul><li><strong>Most important at top left</strong>, where eyes go first: headline KPIs with targets.</li>
<li><strong>Trends below:</strong> how the KPIs are moving over time.</li>
<li><strong>Detail last:</strong> breakdowns and tables for investigation.</li>
<li><strong>Compare with something:</strong> target, last year or last month. A number alone means little.</li>
<li><strong>Consistent colours:</strong> use colour to highlight exceptions, not to decorate. Avoid relying on red and green alone, since some people cannot tell them apart.</li>
<li><strong>Fewer, clearer visuals:</strong> five to eight is usually plenty.</li></ul>
<h3>Different dashboards for different roles</h3>
<p>The owner needs a monthly overview across sales, margin, cash and operations. A sales manager needs pipeline and customer detail weekly. A supervisor needs today's output and issues. One dashboard trying to serve everyone usually serves no one well.</p>
<h3>Test it</h3>
<p>Show a draft to the users and ask them to answer their key questions in under a minute. Watch where they get stuck, and simplify.</p>
""", ["Design around the audience, their decisions and three to five questions.", "Put headline KPIs top left, trends next, detail last; always compare with a target or history.", "Build different dashboards for different roles and test them with users."],
 "Choose one audience and write the three to five questions their dashboard must answer. Sketch the layout on paper before building anything.",
 "Where should the most important KPIs go on a dashboard?", ["Bottom right", "Top left", "On a separate page", "Hidden behind a filter"], 1,
 "Readers look at the top left first, so headline KPIs belong there."),
step("Choosing the right chart", 7, """
<p>The right chart makes the message obvious; the wrong one hides it. Choose the chart by what you want to show.</p>
<table><thead><tr><th>To show</th><th>Use</th><th>Avoid</th></tr></thead><tbody>
<tr><td>Change over time</td><td>Line chart; column chart for few periods</td><td>Pie charts</td></tr>
<tr><td>Comparison between categories</td><td>Bar chart, sorted largest to smallest</td><td>3D effects</td></tr>
<tr><td>Part of a whole</td><td>Stacked bar, or a pie with very few slices</td><td>Pies with many slices</td></tr>
<tr><td>Actual versus target</td><td>Bar with target line, or a bullet chart</td><td>Speedometer gauges that waste space</td></tr>
<tr><td>Relationship between two measures</td><td>Scatter chart</td><td>Two unrelated axes on one chart</td></tr>
<tr><td>Contribution to a total</td><td>Pareto chart (sorted bars with cumulative line)</td><td>Unsorted bars</td></tr>
<tr><td>Exact values for lookup</td><td>Table with conditional formatting</td><td>A chart where people must estimate values</td></tr>
</tbody></table>
<h3>Clarity rules</h3>
<ul><li>Start bar and column axes at zero, or the differences look larger than they are.</li>
<li>Label clearly: title that states the message, axis units, data source and date.</li>
<li>Remove clutter: heavy gridlines, borders, legends you can replace with direct labels.</li>
<li>Highlight what matters: one colour for the item of interest, grey for the rest.</li></ul>
<h3>Write the message as the title</h3>
<p>Instead of "Sales by region", write "West region sales fell 12% while others grew". A title that states the takeaway helps busy readers and forces you to know what the chart says.</p>
""", ["Choose the chart by what you need to show: time, comparison, part of whole, target, relationship.", "Start bars at zero, label units and sources, and remove clutter.", "Use a title that states the message."],
 "Take three charts from a current report. For each, check the chart type against the table and rewrite the title to state the message.",
 "What is the best chart to show monthly sales over two years?", ["Pie chart", "Line chart", "3D cone chart", "A single number"], 1,
 "Line charts show trends over time clearly."),
step("Business intelligence tools and data models", 7, """
<p>When spreadsheets become slow or hard to maintain, a <strong>business intelligence (BI) tool</strong> is the next step. Common options for SMEs include Microsoft Power BI, Google Looker Studio, Tableau, Zoho Analytics and the reporting tools built into many ERP and accounting systems.</p>
<h3>What BI tools add</h3>
<ul><li>Connections to many data sources, refreshed automatically.</li>
<li>Interactive dashboards with filters and drill-down.</li>
<li>Sharing through a browser or app, with access control.</li>
<li>Handling of larger data volumes than spreadsheets comfortably manage.</li></ul>
<h3>Data model basics</h3>
<p>BI tools work best with a simple <strong>data model</strong>, often called a star schema:</p>
<table><thead><tr><th>Table type</th><th>Contents</th><th>Examples</th></tr></thead><tbody>
<tr><td>Fact table</td><td>Transactions or events with numbers to add up</td><td>Sales lines, shipments, timesheets, downtime events</td></tr>
<tr><td>Dimension tables</td><td>Descriptions used to filter and group</td><td>Date, customer, product, region, employee</td></tr>
</tbody></table>
<p>Facts connect to dimensions through keys such as product code and date. This structure keeps calculations correct and dashboards fast. A <strong>date table</strong> with fiscal periods, weeks and months is almost always worth adding.</p>
<h3>Choosing a tool</h3>
<p>Consider what you already use (Microsoft 365 or Google Workspace), the data sources you need to connect, licence costs per user, who will build and maintain the reports, and whether your ERP's built-in reporting already covers your needs. Start with one dashboard and grow from there.</p>
""", ["BI tools add automatic refresh, interactivity, sharing and scale.", "Use a star schema: fact tables of transactions linked to dimension tables.", "Choose a tool that fits your existing platforms, sources, skills and budget."],
 "For your most important dashboard, list the fact tables and dimension tables it needs. Check whether your current tools can connect to each source.",
 "In a star schema, what does a fact table contain?", ["Descriptions such as customer names only", "Transactions or events with numbers to add up, such as sales lines", "Passwords", "Chart colours"], 1,
 "Fact tables hold measurable events; dimensions describe them."),
step("Automating refresh and connecting sources", 7, """
<p>A dashboard that someone must update by hand each week tends to fall behind. Automating the data flow keeps it current and frees time for analysis.</p>
<h3>Levels of automation</h3>
<table><thead><tr><th>Level</th><th>How data arrives</th><th>Effort</th></tr></thead><tbody>
<tr><td>Manual export</td><td>Someone exports a file and refreshes the report</td><td>Ongoing manual work</td></tr>
<tr><td>Scheduled export to a folder</td><td>The system emails or saves a report file on a schedule; the dashboard reads the folder</td><td>Low setup</td></tr>
<tr><td>Direct connection</td><td>The BI tool connects to the system's database or API and refreshes on a schedule</td><td>Moderate setup; may need IT or a partner</td></tr>
<tr><td>Data warehouse</td><td>Data from several systems is copied regularly into one central database</td><td>Higher setup; useful as sources multiply</td></tr>
</tbody></table>
<h3>Practical tips</h3>
<ul><li>Check which connectors your systems and BI tool support; many cloud applications offer ready-made connectors.</li>
<li>Use a service account with read-only access for data connections, not a personal login.</li>
<li>Schedule refreshes to match decisions: daily for operations, weekly or monthly for management.</li>
<li>Show the "last refreshed" time on the dashboard so users know how current it is.</li>
<li>Set up alerts when a refresh fails, and name who fixes it.</li></ul>
<h3>Start where the pain is</h3>
<p>Automate the reports that take the most manual time or matter most for decisions first. Many SMEs find that automating three or four core reports covers most of their needs.</p>
""", ["Move from manual exports to scheduled exports, direct connections or a warehouse as needed.", "Use read-only service accounts and show the last refresh time.", "Automate the most time-consuming, decision-critical reports first."],
 "Rank your reports by manual hours per month. For the top one, find out whether your systems offer a scheduled export or a connector to your BI tool.",
 "Why should a dashboard show its last refresh time?", ["It looks professional", "So users know how current the data is", "It is legally required", "It speeds up refresh"], 1,
 "Users need to know whether they are looking at current or stale data."),
]

M4 = [
step("Running a data-driven meeting", 7, """
<p>Dashboards create value only when they change decisions. A short, regular meeting built around the dashboard turns data into action.</p>
<h3>A simple agenda (30 to 60 minutes)</h3>
<ol><li><strong>Review KPIs against target</strong> quickly: on track, watch or off track.</li>
<li><strong>Discuss exceptions only:</strong> spend time on what is off track or changing, not on what is fine.</li>
<li><strong>Ask why:</strong> use the dashboard's detail to find causes, such as which customers, products or shifts.</li>
<li><strong>Agree actions</strong> with owners and dates.</li>
<li><strong>Review last meeting's actions</strong> and whether they worked.</li></ol>
<h3>Good habits</h3>
<ul><li>Everyone looks at the same dashboard, on screen or printed.</li>
<li>Data arrives before the meeting, not during it.</li>
<li>Questions about data accuracy are logged and fixed, not argued over in the meeting.</li>
<li>Look at trends, not single points: one bad week may be noise; four in a row is a pattern.</li></ul>
<h3>Avoid common traps</h3>
<ul><li><strong>Reporting without acting:</strong> reading numbers aloud and moving on.</li>
<li><strong>Blame:</strong> people hide or massage numbers if KPIs are used to punish.</li>
<li><strong>Too many measures:</strong> attention spreads thin and nothing changes.</li></ul>
<p>The Business Basics for Owners course covers the wider management rhythm of weekly, monthly and quarterly reviews.</p>
""", ["Review KPIs quickly and spend time on exceptions.", "Use the dashboard's detail to find causes, then agree owned actions.", "Look at trends, fix data issues outside the meeting and avoid blame."],
 "Run your next management meeting with the five-step agenda around one dashboard. Count how many actions with owners and dates come out of it.",
 "Where should most time in a data-driven meeting go?", ["Reading every number aloud", "Exceptions: KPIs off track or changing", "Debating chart colours", "Reviewing measures that are on target"], 1,
 "Focusing on exceptions turns review time into action."),
step("Simple analysis that finds answers", 8, """
<p>You don't need advanced statistics to learn a lot from business data. A handful of simple techniques answer most management questions.</p>
<table><thead><tr><th>Technique</th><th>Question it answers</th><th>Example</th></tr></thead><tbody>
<tr><td>Trend</td><td>Is it getting better or worse?</td><td>Gross margin by month for 24 months</td></tr>
<tr><td>Variance</td><td>How far from plan, and why?</td><td>Actual versus budget by expense line</td></tr>
<tr><td>Year-over-year</td><td>Is change real or seasonal?</td><td>This March versus last March</td></tr>
<tr><td>Segmentation</td><td>Which groups behave differently?</td><td>Margin by customer type, region or product line</td></tr>
<tr><td>Pareto</td><td>Which few items drive most of the result?</td><td>Top 20% of customers by profit; top reasons for returns</td></tr>
<tr><td>Ratios</td><td>How efficient are we?</td><td>Revenue per employee, sales per square metre</td></tr>
</tbody></table>
<h3>Segment before you conclude</h3>
<p>Averages hide important differences. Overall on-time delivery of 92% might be 98% for local customers and 75% for one region served by a particular carrier. Breaking data down by customer, product, region, channel or time usually reveals where the real issue is.</p>
<h3>Correlation is not causation</h3>
<p>Two measures moving together does not mean one causes the other. Sales and overtime may both rise in busy months. Before acting, look for the mechanism and, where possible, test a change and measure the result.</p>
<h3>Small numbers</h3>
<p>Percentages based on few cases swing wildly. Three late orders out of ten is 30%; next week it could be 0%. Show counts alongside percentages, and judge small groups over longer periods.</p>
""", ["Use trend, variance, year-over-year, segmentation, Pareto and ratios.", "Segment data before drawing conclusions; averages hide differences.", "Remember correlation is not causation and beware small numbers."],
 "Take one KPI and break it down by two segments, such as customer type and region. Write one sentence on what the breakdown shows that the average hid.",
 "Overall on-time delivery is 92%. What should you do before concluding service is fine?", ["Nothing; 92% is good", "Break it down by customer, region or carrier to find hidden problems", "Round it to 100%", "Stop measuring it"], 1,
 "Segmentation reveals problems that averages hide."),
step("Data governance, security and privacy", 7, """
<p>As data becomes more central, a light set of rules keeps it trustworthy, secure and compliant.</p>
<h3>Governance in plain language</h3>
<ul><li><strong>Owners:</strong> each key data type and each KPI has a named owner.</li>
<li><strong>Definitions:</strong> a shared list of KPI definitions, so everyone means the same thing.</li>
<li><strong>Change control:</strong> changes to definitions, calculations or source systems are agreed and recorded.</li>
<li><strong>Quality checks:</strong> regular checks and visible quality measures.</li></ul>
<h3>Access and security</h3>
<ul><li>Give people access to the data and dashboards they need, not everything. Salary or customer-specific data may need restricting.</li>
<li>Use work accounts with multi-factor authentication for BI tools and shared drives.</li>
<li>Be careful when exporting data to personal devices or sharing dashboards by public link.</li>
<li>Remove access when people leave.</li></ul>
<h3>Privacy</h3>
<p>Customer and employee personal information is protected by privacy law, including PIPEDA. Collect only what you need, use it for the purposes people were told about, protect it and keep it no longer than necessary. For many dashboards, aggregated or anonymized data is enough; avoid showing personal details when totals will do.</p>
<h3>AI and data</h3>
<p>When using AI tools to analyze data, follow your organization's rules about which tools may handle which data. The Prompting and AI Productivity and Cybersecurity courses cover these practices.</p>
""", ["Name owners, keep shared definitions and control changes.", "Limit access, use MFA and avoid public sharing links.", "Follow privacy law: collect what you need, protect it and aggregate where possible."],
 "Create a one-page KPI definition list with owners for your top ten KPIs, and review who has access to your main dashboard.",
 "A dashboard shows sales by individual customer name to all staff, but totals by region would meet the need. What is the better practice?", ["Keep showing names to everyone", "Show aggregated data where it is enough and restrict detail to those who need it", "Delete the dashboard", "Share it publicly"], 1,
 "Least access and aggregation protect personal and sensitive data."),
step("Your 90-day data and dashboard plan", 7, """
<p>Bring the course together in a 90-day plan that produces one trusted, automated dashboard and the habit of using it.</p>
<table><thead><tr><th>Days</th><th>Focus</th><th>Actions</th></tr></thead><tbody>
<tr><td>1–30</td><td>Define and map</td><td>Choose 8 to 12 KPIs from goals; write definitions with owners and targets; map data sources; check data quality for the top KPIs</td></tr>
<tr><td>31–60</td><td>Build</td><td>Restructure data into tidy tables; automate cleaning with Power Query or connectors; build the first dashboard for one audience; test it with users</td></tr>
<tr><td>61–90</td><td>Use and improve</td><td>Run monthly data-driven meetings; fix data issues at the source; add a second dashboard if needed; set access rules and a definition list</td></tr>
</tbody></table>
<h3>Signs of success</h3>
<ul><li>The monthly report refreshes in minutes instead of days.</li>
<li>Everyone quotes the same numbers.</li>
<li>Meetings end with actions based on the data.</li>
<li>Problems are spotted weeks earlier than before.</li></ul>
<h3>Where to go next</h3>
<p>Business Basics for Owners helps choose financial KPIs; OEE and Inventory Management give detailed operational measures; and Digital Automation for SMEs helps plan system integrations that feed dashboards automatically.</p>
<p>Use the self-assessment lab after this lesson to see your data strengths and gaps, and retake it after 90 days.</p>
""", ["Days 1–30: define KPIs, map sources and check quality.", "Days 31–60: tidy data, automate refresh and build the first dashboard.", "Days 61–90: use it in meetings, fix data at the source and set governance."],
 "Put the 90-day plan in your calendar with owners and choose the audience for your first dashboard.",
 "What should the first 30 days of the plan focus on?", ["Buying the most expensive BI tool", "Defining KPIs, mapping data sources and checking data quality", "Building ten dashboards at once", "Training everyone on advanced statistics"], 1,
 "Defining and mapping comes before building."),
]

course = dict(
 id="data-and-dashboards-for-smes",
 title="Data and Dashboards for SMEs",
 tagline="Choose KPIs that matter, clean and connect your data, and build dashboards your team actually uses to make better decisions.",
 summary="A practical course for owners, managers and the people who build reports in small and mid-sized businesses. You will learn to choose and define KPIs, map where data lives and improve data quality, structure spreadsheets properly, use lookups, pivot tables and Power Query, and avoid spreadsheet errors. You will then design dashboards and choose the right charts, understand business intelligence tools and data models, automate refresh, run data-driven meetings, apply simple analysis and set light governance for security and privacy.",
 audience=["Owners and managers who want clearer, faster reporting",
           "Finance, operations and sales staff who build monthly reports",
           "Anyone who spends hours copying and pasting data between spreadsheets",
           "Teams considering Power BI, Looker Studio or similar tools"],
 outcomes=["Choose and define KPIs with a KPI tree, owners and targets",
           "Map data sources, name systems of record and improve data quality",
           "Structure tidy data and use lookups, pivot tables and Power Query",
           "Design dashboards and choose charts that make the message clear",
           "Understand BI tools, star schemas and automated refresh",
           "Run data-driven meetings, apply simple analysis and set governance"],
 modules=[
  dict(title="Foundations", summary="Why data matters, choosing KPIs, where your data lives and data quality basics.", steps=M1),
  dict(title="Spreadsheets Done Right", summary="Tidy data tables, lookups and pivot tables, automated cleaning with Power Query, and avoiding spreadsheet errors.", steps=M2),
  dict(title="Dashboards", summary="Designing dashboards, choosing charts, business intelligence tools and data models, and automating refresh.", steps=M3),
  dict(title="Using Data Well", summary="Data-driven meetings, simple analysis, governance, security and privacy, and a 90-day plan.", steps=M4)],
 labs=[
  dict(id="data-kpi-or-not", type="classify", title="Useful KPI, vanity metric, or unclear?", after_step=2,
       intro="Sort twelve proposed measures: is each a useful KPI, a vanity metric that won't drive decisions, or a measure that needs a clearer definition first? Then check your answers.",
       config=dict(categories=["Useful KPI", "Vanity metric", "Needs a clearer definition"], items=[
        dict(text="Order lines delivered complete by the promised date ÷ all order lines, weekly", answer=0, why="Clearly defined, linked to service and actionable."),
        dict(text="Gross margin % by product line, monthly", answer=0, why="Links directly to profitability decisions on pricing and mix."),
        dict(text="Days sales outstanding, monthly", answer=0, why="Drives collection actions and cash planning."),
        dict(text="Value of open quotes by stage, weekly", answer=0, why="A leading indicator of sales that guides sales activity."),
        dict(text="Total website page views", answer=1, why="Looks impressive but rarely changes a decision; enquiries or cost per lead are better."),
        dict(text="Number of social media followers", answer=1, why="Not linked to revenue or decisions in most B2B firms."),
        dict(text="Number of emails sent by the sales team", answer=1, why="Activity volume without outcome; meetings booked or quotes sent are more useful."),
        dict(text="Number of reports produced each month", answer=1, why="Measures effort, not results."),
        dict(text="Customer satisfaction", answer=2, why="Important, but how is it measured, how often and from whom? Define it first."),
        dict(text="Productivity", answer=2, why="Units per labour hour? Revenue per employee? It needs a formula."),
        dict(text="Quality", answer=2, why="Return rate, first-pass yield or complaints? Choose and define one."),
        dict(text="On-time delivery", answer=2, why="Shipped or delivered? Against which date? Lines or orders? Define it before tracking."),
       ])),
  dict(id="data-automation-matrix", type="matrix", title="Which reports to automate first?", after_step=3,
       intro="Place seven reports on a grid of decision value against manual effort each month, to see which to automate first and which to drop.",
       config=dict(x="Manual effort each month", y="Value for decisions", x_low="Little effort", x_high="Lots of effort", y_low="Low value", y_high="High value",
        quadrants=dict(top_left="Keep; automate when convenient", top_right="Automate first", bottom_left="Leave as is", bottom_right="Simplify or drop"),
        items=[dict(name="Monthly sales and margin by product line", x=5, y=5),
               dict(name="Weekly on-time delivery report", x=4, y=5),
               dict(name="Daily production output", x=2, y=4),
               dict(name="Cash and receivables summary", x=3, y=5),
               dict(name="Detailed report nobody reads", x=5, y=1),
               dict(name="Monthly office supplies spend", x=2, y=1),
               dict(name="Quarterly customer satisfaction summary", x=3, y=3)])),
  dict(id="data-maturity-check", type="assessment", title="Your data maturity check", after_step=16,
       intro="Rate your business on eight areas of data and reporting. The radar chart shows strengths and gaps, with a next step for each. Retake it after your 90-day plan.",
       config=dict(scale=["Not started", "Ad hoc", "Defined", "Managed", "Optimized"], dimensions=[
        dict(name="KPIs", question="Do you have a short list of KPIs linked to goals, each with a definition, owner and target?", low="Pick 8 to 12 KPIs from your goals and define each one.", high="Use a KPI tree to link team measures to company results."),
        dict(name="Data sources", question="Do you know where each KPI's data comes from, with a system of record for each data type?", low="Map each KPI to its source system and owner.", high="Integrate systems so data flows from systems of record automatically."),
        dict(name="Data quality", question="Is key data complete, accurate and consistent, with master data owners?", low="Check 20 records of your most important data and fix the top issue at the source.", high="Track data quality measures alongside KPIs."),
        dict(name="Spreadsheet practice", question="Are spreadsheets tidy, checked and kept as shared master copies?", low="Restructure one key spreadsheet into a tidy table with check totals.", high="Review important models with a second person and move critical processes into systems."),
        dict(name="Automation", question="Do reports refresh automatically rather than being rebuilt by hand?", low="Automate your most time-consuming report with Power Query or a connector.", high="Schedule refreshes with failure alerts and a named owner."),
        dict(name="Dashboard design", question="Are dashboards designed for specific audiences and easy to read in under a minute?", low="Write the key questions for one audience and sketch a dashboard.", high="Test dashboards with users and simplify regularly."),
        dict(name="Use in decisions", question="Do regular meetings use dashboards to agree owned actions?", low="Run one monthly meeting with the five-step agenda.", high="Review whether actions improved the KPIs and adjust."),
        dict(name="Governance and privacy", question="Are definitions, access and personal data managed with clear rules?", low="Create a KPI definition list and review dashboard access.", high="Control changes to definitions and aggregate personal data wherever possible."),
       ])),
 ],
 figures=[
  dict(step=2, type="stack", title="A simple KPI tree", caption="Click each layer, from the bottom up, to see how everyday drivers add up to the result the owner cares about.",
       config=dict(top_label="Profit", layers=[
        dict(label="Daily drivers", text="Quotes sent, calls made, on-time picks, machine uptime."),
        dict(label="Customers and orders", text="Number of active customers and how often they order."),
        dict(label="Average order value and price", text="What each order is worth after discounts."),
        dict(label="Revenue and gross margin", text="Sales minus the cost of what was sold."),
        dict(label="Operating costs", text="Wages, rent and overheads, subtracted to reach profit.")])),
  dict(step=5, type="compare", title="Report layout vs tidy data", caption="Toggle between the two layouts and compare how easy each is to analyze and refresh.",
       config=dict(left=dict(title="Report-style layout", points=["Months across columns", "Merged headers and subtotals inside the data", "Rebuilt by hand each month", "Hard to filter or chart"]),
                   right=dict(title="Tidy data table", points=["One row per record: customer, month, sales", "One header row, one type per column", "Refresh by adding rows", "Feeds pivot tables and BI tools directly"]))),
  dict(step=12, type="flow", title="From source systems to decisions", caption="Click each step to see what happens to the data on its way to a decision.",
       config=dict(steps=[
        dict(label="Sources", text="Accounting, ERP, CRM, spreadsheets and equipment data."),
        dict(label="Clean and combine", text="Power Query or connectors fix types, remove duplicates and add lookups."),
        dict(label="Model", text="Fact and dimension tables in a simple star schema."),
        dict(label="Visualize", text="A dashboard for one audience, with targets and trends."),
        dict(label="Decide and act", text="A regular meeting turns exceptions into owned actions.")])),
  dict(step=13, type="cycle", title="The data-driven meeting", caption="Click each step in the monthly loop.",
       config=dict(center="Act", stages=[
        dict(label="Review", text="KPIs against target: on track, watch, off track."),
        dict(label="Focus", text="Spend time on exceptions only."),
        dict(label="Diagnose", text="Use the detail to find which customers, products or shifts."),
        dict(label="Agree actions", text="Owners and dates for each action."),
        dict(label="Follow up", text="Check last month's actions and whether they worked.")])),
  dict(step=14, type="bars", title="Example: on-time delivery hides a problem", caption="Overall on-time delivery is 92%, but breaking it down by region shows where the issue is.",
       config=dict(unit="% on time", items=[dict(label="Local", value=98), dict(label="Province-wide", value=95), dict(label="Neighbouring province", value=93), dict(label="Northern region", value=75, highlight=True)],
        note="In this example one region, served by one carrier, drags the average down.")),
  dict(step=16, type="timeline", title="A 90-day data and dashboard plan", caption="Click each phase to see its main actions.",
       config=dict(phases=[
        dict(label="Days 1–30", title="Define and map", items=["8–12 KPIs with definitions", "Map data sources", "Check data quality"]),
        dict(label="Days 31–60", title="Build", items=["Tidy tables", "Automate cleaning and refresh", "First dashboard, tested with users"]),
        dict(label="Days 61–90", title="Use and improve", items=["Monthly data-driven meetings", "Fix data at the source", "Access rules and definition list"])])),
 ],
 exam=[
  E("What makes a measure a key performance indicator?", ["It tells you whether you are achieving an important goal and drives decisions", "It is easy to count", "It makes the business look good", "Competitors use it"], 0, "KPIs link to goals and lead to action."),
  E("Which is a leading indicator?", ["Last quarter's profit", "Value of open quotes in the pipeline", "Annual revenue", "Taxes paid"], 1, "Pipeline value predicts future sales."),
  E("What should every KPI definition include?", ["A colour", "Only a name", "Formula, data source, frequency, owner and target", "The CEO's signature"], 2, "Complete definitions keep KPIs consistent."),
  E("What is a system of record?", ["The largest spreadsheet", "A backup drive", "The newest software", "The authoritative source for a type of data"], 3, "Other systems should rely on the system of record."),
  E("Orders without a promised date affect which data quality dimension?", ["Completeness", "Consistency", "Validity", "Timeliness"], 0, "Missing values are a completeness problem."),
  E("What is the best way to fix recurring data entry errors?", ["Clean them every month in a spreadsheet", "Fix the source with mandatory fields, drop-downs and training", "Ignore them", "Delete the data"], 1, "Fixing at the source prevents recurrence."),
  E("Which layout is a tidy data table?", ["Months across columns with subtotals", "Merged cells with blank rows", "One row per record and one column per field", "A different file for every month"], 2, "Tidy data has one row per record and one column per field."),
  E("What does XLOOKUP do?", ["Draws charts", "Protects cells", "Sends data by email", "Returns a matching value from another table using a key"], 3, "Lookups combine tables by a shared key."),
  E("What is a pivot table for?", ["Summarizing a data table quickly by different fields", "Writing macros", "Encrypting files", "Printing labels"], 0, "Pivot tables regroup and total data without formulas."),
  E("What is the main benefit of Power Query?", ["It replaces the ERP", "It records cleaning steps and repeats them on new data", "It creates logos", "It manages payroll"], 1, "Recorded, repeatable steps save time and reduce errors."),
  E("Why is a formula like =B2*1.13 risky?", ["It is too long", "Multiplication is unreliable", "The rate is hard-coded and easily missed when it changes", "It cannot be copied"], 2, "Hard-coded assumptions should be in input cells."),
  E("Where should headline KPIs be placed on a dashboard?", ["Bottom right", "In a footnote", "On a hidden tab", "Top left"], 3, "Readers look at the top left first."),
  E("Which chart best shows sales over 24 months?", ["Line chart", "Pie chart", "3D cone chart", "Single number"], 0, "Line charts show trends over time."),
  E("Why should bar chart axes start at zero?", ["It is required by law", "Otherwise differences look larger than they are", "It makes bars thinner", "It hides labels"], 1, "Truncated axes exaggerate differences."),
  E("In a star schema, what are dimension tables?", ["Tables of transactions", "Backup copies", "Descriptive tables used to filter and group, such as customer or date", "Password lists"], 2, "Dimensions describe facts and enable grouping."),
  E("What account should a BI tool use to connect to source systems?", ["The owner's personal login", "Any staff member's account", "A shared admin password", "A service account with read-only access"], 3, "Read-only service accounts are safer and do not depend on one person."),
  E("Where should most time go in a data-driven meeting?", ["Exceptions: KPIs off track or changing", "Reading every number aloud", "Debating chart design", "Measures on target"], 0, "Focusing on exceptions drives action."),
  E("Overall on-time delivery is 92%. What should you do before concluding all is well?", ["Celebrate", "Segment it by customer, region or carrier", "Stop measuring it", "Change the target to 90%"], 1, "Segmentation reveals hidden problems."),
  E("Sales and overtime rise together. What can you conclude?", ["Overtime causes sales", "Sales cause overtime", "They are related, but causation has not been shown", "Nothing is related"], 2, "Correlation does not prove causation."),
  E("A dashboard shows customer names when regional totals would meet the need. What is better practice?", ["Share it publicly", "Show names to everyone", "Remove all data", "Use aggregated data and restrict detail to those who need it"], 3, "Aggregation and least access protect personal data."),
 ],
)

if __name__ == "__main__":
    write(course, "data-dashboards", __file__, balance=True)
