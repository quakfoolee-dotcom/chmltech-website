"""Source for content/courses/lean-six-sigma.json (run: python3 content/courses/src/lean_six_sigma.py)."""
import json, os

def step(title, minutes, body, takeaways, apply, q, opts, a, why):
    return dict(title=title, minutes=minutes, body=" ".join(body.split("\n")).strip(), takeaways=takeaways, apply=apply,
                check=dict(q=q, opts=opts, a=a, why=why))

M1 = [
step("What Lean Six Sigma is, and why it works for SMEs", 6, """
<p>Lean Six Sigma combines two improvement traditions. <strong>Lean</strong>, which grew out of the Toyota Production System, is about flow: delivering what the customer values with as little waste and waiting as possible. <strong>Six Sigma</strong>, developed at Motorola and popularized by large manufacturers, is about variation: making a process consistent enough that it rarely produces a defect. Together they ask two questions of any process: <em>where does time and effort go that the customer would not pay for?</em> and <em>why does the result vary from one day, shift or person to the next?</em></p>
<p>The two traditions share one problem-solving roadmap, <strong>DMAIC</strong>: Define, Measure, Analyze, Improve and Control. Each phase answers a question before the next one starts, so a team does not jump from a complaint straight to a pet solution.</p>
<table><thead><tr><th>Phase</th><th>Question it answers</th><th>Typical outputs</th></tr></thead><tbody>
<tr><td>Define</td><td>What problem, for which customer, and how will we know it is fixed?</td><td>Charter, SIPOC, customer requirements</td></tr>
<tr><td>Measure</td><td>How big is the problem today, measured reliably?</td><td>Data collection plan, baseline, process map</td></tr>
<tr><td>Analyze</td><td>What are the verified root causes?</td><td>Pareto, fishbone, data analysis</td></tr>
<tr><td>Improve</td><td>Which changes remove those causes, and do they work?</td><td>Selected solutions, pilot results</td></tr>
<tr><td>Control</td><td>How do we keep the gain?</td><td>Control plan, standard work, control chart</td></tr>
</tbody></table>
<h3>Why it suits small and mid-sized businesses</h3>
<p>You do not need a statistics department. Most SME problems, such as late shipments, rework, quoting errors or long changeovers, yield to simple tools used with discipline: a clear problem statement, a process map, a tally sheet, a Pareto chart and a check that the fix held. The heavier statistics in Six Sigma matter when the easy causes are gone. This course focuses on the tools that pay off first and tells you when to bring in deeper methods.</p>
<p>A word on belts: White, Yellow, Green and Black Belt are training levels that companies and training bodies define in different ways. This course covers the foundations a Green Belt uses on a project. It is not a certification, but it prepares you to run your first DMAIC project well.</p>
""", ["Lean removes waste and improves flow; Six Sigma reduces variation and defects.", "DMAIC is a five-phase roadmap that stops teams jumping to solutions.", "Simple tools used with discipline solve most SME problems."],
 "Name one recurring problem in your area that costs time or money every week. Write one sentence for each DMAIC question about it, even if your answers are guesses for now.",
 "What does the Measure phase of DMAIC mainly answer?", ["Which solution should we implement first?", "How big is the problem today, measured reliably?", "Who should sponsor the project?", "How do we keep the gain after the project ends?"], 1,
 "Measure establishes a reliable baseline of how the process performs now, before anyone analyzes causes or picks solutions."),
step("The eight wastes", 7, """
<p>Lean sorts every activity into three groups. <strong>Value-added</strong> work changes the product or service in a way the customer cares about and would pay for, and is done right the first time. <strong>Business-necessary non-value-added</strong> work does not add value but is required for now, such as legal records or safety checks. Everything else is <strong>waste</strong>, often called <em>muda</em>.</p>
<p>A handy way to remember the eight wastes is <strong>TIMWOODS</strong>:</p>
<table><thead><tr><th>Waste</th><th>Office example</th><th>Shop-floor example</th></tr></thead><tbody>
<tr><td>Transportation</td><td>Files emailed between four people for approval</td><td>Pallets moved twice between receiving and storage</td></tr>
<tr><td>Inventory</td><td>A backlog of unprocessed orders in an inbox</td><td>Weeks of work-in-progress between stations</td></tr>
<tr><td>Motion</td><td>Switching between three systems to answer one question</td><td>Walking to a distant shared tool crib</td></tr>
<tr><td>Waiting</td><td>Quotes waiting for one manager's sign-off</td><td>Operators idle while a machine is set up</td></tr>
<tr><td>Overproduction</td><td>Reports nobody reads</td><td>Making parts ahead of any order</td></tr>
<tr><td>Over-processing</td><td>Re-keying data already in another system</td><td>Polishing a surface the customer never sees</td></tr>
<tr><td>Defects</td><td>Invoices with the wrong price</td><td>Welds that fail inspection</td></tr>
<tr><td>Skills (unused talent)</td><td>Staff ideas never asked for</td><td>Operators not involved in solving line problems</td></tr>
</tbody></table>
<p>Overproduction is often called the worst waste because it creates several others: extra inventory, transport, storage and the risk that the items become defects or obsolete.</p>
<h3>Seeing waste: the gemba walk</h3>
<p>Waste is easiest to see where the work happens, which Lean calls the <em>gemba</em>. Walk the process from start to finish, follow one order or one part, and note every stop, move and correction. In many processes the value-added time is a small fraction of the total elapsed time; the rest is waiting and handling. That gap is where Lean finds its biggest and cheapest gains.</p>
""", ["Sort activities into value-added, business-necessary and waste.", "TIMWOODS names the eight wastes, including unused skills.", "Walk the process at the gemba and follow one item end to end."],
 "Follow one order, job or document through your process today. List each step and mark it value-added, necessary or waste. Note the step with the longest wait.",
 "A team re-types customer details from email into the ERP and then into a shipping system. Which waste is this mainly?", ["Over-processing", "Overproduction", "Transportation", "Inventory"], 0,
 "Doing more work than the customer needs, such as entering the same data twice, is over-processing."),
step("Variation: why averages mislead", 7, """
<p>Every process varies. Delivery times, fill weights, quote turnaround and machine cycle times are never identical twice. Six Sigma's insight is that customers feel the <strong>variation</strong>, not the average. If your average delivery is three days but one order in five takes eight, the customer remembers the eight.</p>
<p>Imagine two shipping teams that both average three days. Team A ranges from two to four days. Team B ranges from one to nine. Their averages match, but Team B produces many more late orders. Reducing variation, not just shifting the average, is often what fixes the complaint.</p>
<h3>Common cause and special cause</h3>
<table><thead><tr><th></th><th>Common-cause variation</th><th>Special-cause variation</th></tr></thead><tbody>
<tr><td>What it is</td><td>The normal, built-in noise of the process</td><td>An unusual event outside the normal pattern</td></tr>
<tr><td>Example</td><td>Small day-to-day differences in picking time</td><td>A new, untrained picker; a broken scanner</td></tr>
<tr><td>Right response</td><td>Change the process itself (a DMAIC project)</td><td>Find and remove the specific cause</td></tr>
<tr><td>Wrong response</td><td>Reacting to every high or low point</td><td>Redesigning the whole process for one event</td></tr>
</tbody></table>
<p>Reacting to common-cause noise as if every bad day had a special reason is called <strong>tampering</strong>. It usually makes a process more variable, not less, because each adjustment adds its own disturbance.</p>
<h3>Look at the data over time</h3>
<p>A single average hides both kinds of variation. Plot the data in time order, a <em>run chart</em>, before you summarize it. Patterns such as a steady drift, a sudden shift after a change, or a repeating Monday spike tell you far more than one number. Later lessons add control limits, which turn a run chart into a control chart that separates common from special causes.</p>
""", ["Customers feel variation, not the average.", "Common causes need a process change; special causes need a specific fix.", "Plot data in time order before you summarize it."],
 "Take a measure you already track, such as daily shipments or quote turnaround. Plot the last 20 to 30 values in time order and note any shift, trend or repeating pattern.",
 "A supervisor changes the machine setting every time one reading is slightly high or low. What is the likely effect?", ["Variation falls because problems are caught early", "No effect, because the readings are random", "Variation rises because each adjustment adds disturbance", "The average shifts permanently to target"], 2,
 "Adjusting for common-cause noise is tampering, which adds variation rather than removing it."),
step("Roles, project selection and the charter", 7, """
<p>Lean Six Sigma works through projects, and projects need clear roles. In an SME one person may wear several hats, but each role should be filled.</p>
<table><thead><tr><th>Role</th><th>What they do</th></tr></thead><tbody>
<tr><td>Sponsor (Champion)</td><td>Owns the business result, removes obstacles, approves the charter and changes</td></tr>
<tr><td>Process owner</td><td>Runs the process day to day and keeps the gain after the project</td></tr>
<tr><td>Project lead (often a Green Belt)</td><td>Leads the team through DMAIC, plans the work and reports progress</td></tr>
<tr><td>Team members</td><td>People who do the work; they know where the problems are</td></tr>
<tr><td>Coach (Black Belt or experienced lead)</td><td>Advises on method and data, reviews the project at phase gates</td></tr>
</tbody></table>
<h3>Choosing a good first project</h3>
<p>Good first projects are <strong>important, measurable and contained</strong>. They are tied to something the business cares about (cost, delivery, quality, safety or cash), have data you can collect within weeks, and sit mostly within one team's control. Avoid problems where the solution is already decided ("we just need new software"); that is an implementation project, not a DMAIC project.</p>
<h3>The project charter</h3>
<p>The charter is a one-page agreement between the sponsor and the team. It includes:</p>
<ul><li><strong>Problem statement:</strong> what is wrong, where, since when and how big, with no cause or solution in it.</li>
<li><strong>Goal statement:</strong> the measurable target and the date, such as "reduce quote errors from 8% to below 3% by June 30".</li>
<li><strong>Scope:</strong> where the process starts and ends, and what is out of scope.</li>
<li><strong>Business case:</strong> why it matters now, in money or customer terms.</li>
<li><strong>Team, roles and timeline:</strong> including dates for each DMAIC phase review.</li></ul>
<p>A weak problem statement says "customers are unhappy with shipping". A strong one says "In Q3, 14% of standard orders shipped later than the promised date, up from 6% in Q1, generating about 40 complaint calls a month."</p>
""", ["Fill the sponsor, process owner, lead and team roles, even in a small firm.", "Pick a first project that is important, measurable and contained.", "A charter states the problem and goal in numbers, without causes or solutions."],
 "Draft a one-paragraph problem statement and a goal statement for a problem in your area. Check that neither mentions a cause or a solution.",
 "Which is the strongest problem statement for a charter?", ["Our new ERP is causing order errors", "We need to hire another customer service rep", "Order entry is slow and frustrating", "In Q3, 9% of orders had an entry error, up from 4% in Q1, causing about 30 credit notes a month"], 3,
 "A good problem statement is specific and measurable and contains no assumed cause or solution."),
]

M2 = [
step("Voice of the customer, CTQs and the SIPOC", 7, """
<p>Improvement starts with what the customer needs. The <strong>voice of the customer (VOC)</strong> is what customers say, through complaints, surveys, returns, sales feedback and interviews. VOC is usually vague: "fast delivery", "accurate invoices", "easy to order". The team translates it into <strong>critical-to-quality (CTQ)</strong> requirements that can be measured.</p>
<table><thead><tr><th>Voice of the customer</th><th>Need</th><th>CTQ (measurable)</th></tr></thead><tbody>
<tr><td>"Your deliveries are always late."</td><td>Reliable delivery</td><td>Order delivered on or before the promised date</td></tr>
<tr><td>"The invoice never matches the quote."</td><td>Accurate billing</td><td>Invoice price equals quoted price on every line</td></tr>
<tr><td>"I can never get an answer on my order."</td><td>Responsive service</td><td>Order-status query answered within 4 business hours</td></tr>
</tbody></table>
<p>Each CTQ needs an <strong>operational definition</strong>: exactly what counts as a defect. For "on time", decide whether you mean shipped or delivered, which date counts as promised, and how to treat partial shipments. Without this, two people counting the same orders get different answers.</p>
<h3>The SIPOC: one page that frames the process</h3>
<p>A SIPOC lists <strong>S</strong>uppliers, <strong>I</strong>nputs, <strong>P</strong>rocess, <strong>O</strong>utputs and <strong>C</strong>ustomers. The process column has only five to seven high-level steps. Its value is agreement: it shows where the project starts and stops, and who supplies and receives what.</p>
<table><thead><tr><th>Suppliers</th><th>Inputs</th><th>Process</th><th>Outputs</th><th>Customers</th></tr></thead><tbody>
<tr><td>Customer, sales rep, price list</td><td>Purchase order, quote, stock data</td><td>Receive PO → enter order → check credit and stock → confirm → release to warehouse</td><td>Confirmed order, confirmation email</td><td>Customer, warehouse, finance</td></tr>
</tbody></table>
<p>Build the SIPOC with the team in under an hour. Disagreement about where the process starts is common and useful: settle it now, not halfway through Analyze.</p>
""", ["Translate vague customer comments into measurable CTQs.", "Give each CTQ an operational definition of a defect.", "A SIPOC frames the scope in five to seven steps on one page."],
 "Pick one complaint you hear often. Translate it into a need and a measurable CTQ, then write the operational definition of a defect for it.",
 "What is the main purpose of an operational definition?", ["To make sure everyone counts defects the same way", "To assign blame for defects", "To list all process steps in detail", "To set the project budget"], 0,
 "An operational definition removes ambiguity so that different people measuring the same items get the same result."),
step("Process mapping and the value stream", 8, """
<p>The SIPOC shows the big picture. A <strong>process map</strong> shows how the work really flows, step by step, including decisions, handoffs, loops and waits. Map the process as it is today, not as the procedure says it should be. The best way is to walk it with the people who do the work.</p>
<p>A <strong>swim-lane map</strong> puts each role or department in its own lane. It makes handoffs visible, and handoffs are where delays and errors gather. Every time work crosses a lane line, ask: does it wait here, can information be lost, and does anyone own the handoff?</p>
<h3>Value stream mapping</h3>
<p>A <strong>value stream map (VSM)</strong> adds time and flow data to the steps. For each step record the process time (hands-on work) and the waiting time before it. Two summary numbers come out of a VSM:</p>
<ul><li><strong>Lead time:</strong> the total elapsed time from start to finish, for example from purchase order received to order shipped.</li>
<li><strong>Process cycle efficiency:</strong> value-added time divided by lead time.</li></ul>
<p>Suppose an order takes 5 working days from receipt to shipment, but the actual hands-on work is 50 minutes. Almost all of the lead time is queue time: orders waiting in inboxes, for approvals, for stock checks or for a pick wave. That tells the team to attack waiting and batching first, rather than making each step faster.</p>
<h3>Find the constraint</h3>
<p>In any flow, one step limits the output of the whole process: the <strong>bottleneck</strong> or constraint. Work piles up in front of it and steps after it wait. Improving any other step does little until the bottleneck improves. Look for the step with the biggest queue in front of it and the highest workload relative to capacity.</p>
""", ["Map the process as it really is, with the people who do it.", "Handoffs between lanes are where delays and errors gather.", "Lead time is mostly waiting; find and fix the bottleneck first."],
 "Draw a swim-lane map of one process in your area with its main roles. Mark each handoff and estimate how long work waits there.",
 "An order takes 5 days end to end, but hands-on work totals under an hour. Where should the team look first?", ["Making each step's hands-on work faster", "Hiring more staff for every step", "Waiting, queues and batching between steps", "Buying faster computers"], 2,
 "When almost all lead time is waiting, reducing queues, approvals and batching gives far bigger gains than speeding up the work itself."),
step("Collecting good data: plans, sampling and measurement", 8, """
<p>Decisions are only as good as the data behind them. Before collecting, write a short <strong>data collection plan</strong>: what you will measure, the operational definition, where and how it will be recorded, who records it, how many data points and over what period, and which factors to record alongside (shift, product, customer, machine, operator). Those extra factors, called stratification factors, are what let you find causes later.</p>
<h3>Types of data</h3>
<table><thead><tr><th>Type</th><th>Examples</th><th>Notes</th></tr></thead><tbody>
<tr><td>Continuous (variable)</td><td>Time, weight, length, temperature, cost</td><td>More information per data point; preferred when available</td></tr>
<tr><td>Discrete (attribute)</td><td>Pass/fail, number of errors, defect type</td><td>Easy to collect but needs larger samples</td></tr>
</tbody></table>
<p>If you can measure "minutes late" instead of just "late or on time", do it. Continuous data shows how far off target you are, not just whether you missed.</p>
<h3>Sampling</h3>
<p>You rarely need every record. Take a sample that represents the process: across all shifts, days, products and people involved, not just the convenient Tuesday morning. Pull records from the system where possible, since manual tallies drift when people are busy.</p>
<h3>Is the measurement system trustworthy?</h3>
<p><strong>Measurement system analysis (MSA)</strong> checks that the way you measure is reliable before you trust the numbers. For continuous gauges, a <em>gauge R&amp;R</em> study measures how much variation comes from the gauge (repeatability) and from different people (reproducibility). For pass/fail judgements, an <em>attribute agreement</em> check has several inspectors classify the same items, including known good and bad ones, and compares their answers. If two inspectors disagree on a third of the items, fix the definition and training before measuring the process.</p>
""", ["Write a data collection plan, including stratification factors.", "Prefer continuous data; sample across all conditions.", "Check the measurement system before trusting the data."],
 "Write a five-line data collection plan for your project measure: what, definition, source, who and when, and two stratification factors to record.",
 "Three inspectors classify the same 30 parts and disagree on 10 of them. What should the team do first?", ["Start analyzing the defect data anyway", "Clarify the defect definition and retrain before collecting data", "Replace the production machine", "Use only the most senior inspector's results"], 1,
 "Poor agreement means the measurement system is unreliable; fixing the definition and training comes before analyzing the process."),
step("Baseline performance: yield, DPMO and sigma level", 8, """
<p>With reliable data, establish the <strong>baseline</strong>: how the process performs before any change. The baseline is what you will compare your results against at the end, so record how and when it was measured.</p>
<h3>Measures for defects</h3>
<ul><li><strong>Defects per unit (DPU):</strong> total defects divided by units. 46 defects on 2,000 orders is a DPU of 0.023.</li>
<li><strong>Opportunities:</strong> the number of ways one unit can be wrong that matter to the customer. An order line might have four: product, quantity, price and delivery address.</li>
<li><strong>DPMO:</strong> defects per million opportunities = defects ÷ (units × opportunities) × 1,000,000. Here 46 ÷ (2,000 × 4) × 1,000,000 = 5,750 DPMO.</li>
<li><strong>Sigma level:</strong> a conversion of DPMO to a single number using the normal distribution. By convention it includes a 1.5 sigma shift for long-term drift, which is why "six sigma" corresponds to 3.4 DPMO. 5,750 DPMO is about 4.0 sigma.</li></ul>
<p>Be honest about opportunities. Counting trivial ones inflates the denominator and makes performance look better than the customer experiences it. Many teams report DPU or percentage defective to managers and keep DPMO for comparing very different processes.</p>
<h3>Capability for continuous data</h3>
<p>For continuous CTQs with specification limits, <strong>process capability</strong> compares the spread of the process with the width of the specification. <strong>Cp</strong> looks at spread only. <strong>Cpk</strong> also accounts for how well centred the process is, using the distance from the mean to the nearer specification limit, divided by three standard deviations. A Cpk of 1.33 or higher is a common target; below 1.0 means the process routinely produces output outside specification. Capability only means something if the process is stable, which the control chart lesson covers.</p>
<p>Use the lab after this lesson to calculate DPU, DPMO and sigma level from your own counts.</p>
""", ["Record the baseline carefully; you will compare against it.", "DPMO = defects ÷ (units × opportunities) × 1,000,000.", "Cpk compares spread and centring with the specification; 1.33 is a common target."],
 "Calculate the DPU and percentage defective for your project measure from last month's data. Write down the period and data source you used.",
 "A process has 30 defects in 1,000 units with 3 opportunities per unit. What is the DPMO?", ["30,000", "3,000", "10,000", "90,000"], 2,
 "DPMO = 30 ÷ (1,000 × 3) × 1,000,000 = 10,000."),
]

M3 = [
step("Pareto charts and fishbone diagrams", 7, """
<p>Analyze begins by narrowing the problem. A <strong>Pareto chart</strong> sorts defect categories from most to least frequent, with a line showing the cumulative percentage. It applies the Pareto principle: a few categories usually account for most of the problem. The team then focuses on the tallest bars.</p>
<p>Suppose a distributor logs 200 order errors over a quarter: wrong quantity 84, wrong item 52, wrong price 30, wrong address 20, other 14. The first two categories make up 68% of errors, so they become the focus. Two tips: chart by cost or customer impact as well as by count, because a rare error can be the most expensive; and break a large bar down further, for example wrong quantity by product family or by order channel.</p>
<h3>The fishbone (cause-and-effect) diagram</h3>
<p>Once the focus is clear, the team brainstorms possible causes on a <strong>fishbone diagram</strong>. The problem sits at the head. Causes branch off categories, often the 6 Ms for manufacturing:</p>
<table><thead><tr><th>Category</th><th>Questions to ask</th></tr></thead><tbody>
<tr><td>Methods</td><td>Is there a standard? Is it followed? Is it clear?</td></tr>
<tr><td>Machines</td><td>Are equipment and systems capable, maintained, set up correctly?</td></tr>
<tr><td>Materials</td><td>Do inputs vary by supplier, lot or storage?</td></tr>
<tr><td>Measurements</td><td>Are gauges, data and definitions reliable?</td></tr>
<tr><td>Manpower (people)</td><td>Training, workload, handoffs, experience?</td></tr>
<tr><td>Mother Nature (environment)</td><td>Temperature, humidity, layout, noise, time of day?</td></tr>
</tbody></table>
<p>For office processes, categories such as Policies, Procedures, People, Systems and Information often fit better. Keep in mind that a fishbone lists <em>possible</em> causes. It is a map of ideas to test, not a conclusion. The team then picks the most likely causes, by vote or by data, to verify.</p>
""", ["A Pareto chart shows the few categories that cause most of the problem.", "Chart by cost or impact too, and drill into large bars.", "A fishbone lists possible causes to test, not proven ones."],
 "Tally last month's defects or complaints in your area by type and sort them into a Pareto list. Which two categories make up most of the total?",
 "What does a completed fishbone diagram tell the team?", ["The verified root cause of the problem", "The best solution to implement", "The cost of each defect", "A structured list of possible causes to investigate"], 3,
 "A fishbone organizes brainstormed possible causes; each still has to be verified with data or observation."),
step("5 Whys and verifying root causes", 7, """
<p><strong>5 Whys</strong> is a simple way to dig below a symptom. Ask why the problem happened, then ask why that answer happened, and keep going until you reach a cause you can act on, often around five levels.</p>
<p>Example: <em>Orders shipped with the wrong quantity.</em> Why? The picker picked the quantity in eaches instead of cases. Why? The pick ticket shows a quantity without a unit. Why? The ERP field for unit of measure is not printed on the ticket template. Why? The template was set up for a product range that was sold only in eaches. Why? Nobody owns the ticket template, so it was never updated when case products were added. The action is to fix the template and give it an owner, not to "remind pickers to be careful".</p>
<p>Two rules keep 5 Whys honest. First, each answer must be a fact you can check, not a guess. Second, if you reach "human error" or "they didn't follow the procedure", ask why once more: what made the error easy to make?</p>
<h3>Verify before you act</h3>
<p>A cause is only a <em>root</em> cause when evidence supports it. Ways to verify:</p>
<ul><li><strong>Stratify the data:</strong> if the cause is real, defects should concentrate where it is present, for example on case-pack products or on the night shift.</li>
<li><strong>Observe:</strong> watch the process at the gemba and see the cause happen.</li>
<li><strong>Turn it on and off:</strong> where safe, test whether removing the cause removes the defect and restoring it brings the defect back.</li>
<li><strong>Check the timing:</strong> did the problem start when the suspected cause appeared?</li></ul>
<p>Record each suspected cause with its evidence and a verdict: verified, rejected or not yet tested. This table is the main output of the Analyze phase and the bridge to Improve.</p>
""", ["Ask why until you reach a cause you can act on.", "Never stop at human error; ask what made the error easy.", "Verify causes with stratified data, observation or on/off tests."],
 "Run a 5 Whys on one recent problem with a colleague. At each level, note the evidence for the answer. Where you lack evidence, write how you would check it.",
 "A 5 Whys ends at 'the operator did not follow the procedure'. What should the team do?", ["Ask why the procedure was not followed or was easy to miss", "Retrain the operator and close the project", "Stop, because the root cause is found", "Discipline the operator"], 0,
 "Human error is rarely a root cause; asking what made the error easy usually reveals a fixable process or system cause."),
step("Graphical analysis: histograms, run charts and scatter plots", 8, """
<p>Pictures of data reveal patterns that tables hide. Four graphs cover most of what an SME project needs.</p>
<table><thead><tr><th>Graph</th><th>Shows</th><th>Use it to ask</th></tr></thead><tbody>
<tr><td>Histogram</td><td>The shape and spread of continuous data</td><td>Is it centred on target? Is it skewed? Are there two humps (two processes mixed)?</td></tr>
<tr><td>Run chart</td><td>Data in time order</td><td>Is there a trend, a shift or a cycle?</td></tr>
<tr><td>Box plot</td><td>Median, spread and outliers for several groups side by side</td><td>Does one shift, machine or supplier differ from the others?</td></tr>
<tr><td>Scatter plot</td><td>The relationship between two continuous variables</td><td>Does Y change when X changes?</td></tr>
</tbody></table>
<h3>Reading them well</h3>
<p>A histogram with two peaks often means the data mixes two different conditions, such as two machines or two order types. Split the data and look again. Box plots are the quickest way to compare groups: if the night shift's box sits well above the day shift's for cycle time, you have a lead worth verifying.</p>
<p>Scatter plots need care. A pattern shows <strong>correlation</strong>, not <strong>causation</strong>. Ice cream sales and sunburns rise together because both follow hot weather. In a plant, scrap and overtime may rise together because both follow high volume. Confirm the mechanism through observation or a controlled test before acting.</p>
<h3>Example</h3>
<p>A food packer finds fill weights vary more than expected. A histogram shows two humps. Box plots by filling head show that one of six heads runs consistently heavy. A check of that head finds a worn seal. The fix is maintenance on one head, not tighter control of all six. Total analysis time: an afternoon with a spreadsheet.</p>
""", ["Use histograms for shape, run charts for time, box plots for groups, scatter plots for relationships.", "Two humps in a histogram usually mean two conditions mixed together.", "Correlation is not causation; confirm the mechanism."],
 "Take one continuous measure from your process and make a histogram and a box plot by one grouping factor, such as shift or product. Note any group that stands out.",
 "Scrap and overtime both rise in busy months. What can the team conclude from a scatter plot alone?", ["Overtime causes scrap", "Scrap causes overtime", "The two are related, but the cause has not been shown", "There is no relationship"], 2,
 "A scatter plot shows correlation; both may be driven by a third factor such as volume, so causation needs separate evidence."),
step("Statistical tests in plain language", 8, """
<p>Sometimes the graphs are not conclusive. Is the new supplier's material really better, or did we just have a lucky week? <strong>Hypothesis testing</strong> answers that question with a known risk of being wrong.</p>
<h3>The logic</h3>
<p>Every test starts with a <strong>null hypothesis</strong>: there is no difference or no effect. The test calculates a <strong>p-value</strong>, the probability of seeing a difference at least as large as the one observed if the null hypothesis were true. A small p-value, commonly below 0.05, means the observed difference would be unlikely if there were really no effect, so you reject the null hypothesis and treat the difference as real.</p>
<p>Two cautions. A p-value is not the probability that your conclusion is right. And "statistically significant" does not mean "important": with enough data, a difference too small to matter can be significant. Always ask whether the size of the difference matters to the customer or the business.</p>
<h3>Choosing a test</h3>
<table><thead><tr><th>Question</th><th>Data</th><th>Common test</th></tr></thead><tbody>
<tr><td>Do two groups have different averages?</td><td>Continuous</td><td>Two-sample t-test</td></tr>
<tr><td>Do three or more groups differ?</td><td>Continuous</td><td>ANOVA</td></tr>
<tr><td>Did the same items change before and after?</td><td>Continuous, paired</td><td>Paired t-test</td></tr>
<tr><td>Do defect rates differ between groups?</td><td>Pass/fail counts</td><td>Two-proportion or chi-square test</td></tr>
<tr><td>Does Y change with X?</td><td>Two continuous variables</td><td>Correlation and regression</td></tr>
</tbody></table>
<p>Spreadsheet tools and statistics packages run these in seconds. The skill is in setting up the question, collecting enough representative data and interpreting the result alongside the graphs. If your project hinges on a subtle difference or many interacting factors, such as setting several process parameters at once, bring in a Black Belt or statistician; designed experiments (DOE) are the right tool there.</p>
""", ["Tests check whether a difference is likely real or just noise.", "p below 0.05 is a common cut-off, but significance is not importance.", "Match the test to the question and data type; get help for complex cases."],
 "Write one question from your project as a null hypothesis, such as 'average cycle time is the same on both shifts'. Note which data and test would answer it.",
 "A test comparing two suppliers gives p = 0.01, but the difference in average strength is 0.2%, well inside specification. What is the best conclusion?", ["The difference is probably real but may not matter in practice", "Supplier B must be dropped immediately", "The test is wrong because p is too small", "There is no difference between suppliers"], 0,
 "A small p-value suggests a real difference, but its practical importance depends on its size relative to customer needs."),
]

M4 = [
step("Generating and selecting solutions", 7, """
<p>Improve starts with the verified root causes from Analyze. Each solution should remove or weaken a verified cause. A solution that does not link to a cause is a guess.</p>
<h3>Generating ideas</h3>
<p>Involve the people who do the work. Brainstorm many options before judging any. Useful prompts: <em>How would we eliminate this step? Combine it with another? Change the sequence? Simplify it? Make the error impossible?</em> Look at how other teams or industries solve the same problem, and at simple low-cost fixes before technology.</p>
<h3>Mistake-proofing (poka-yoke)</h3>
<p>The strongest solutions make errors impossible or immediately obvious rather than relying on attention. In order of strength:</p>
<ol><li><strong>Eliminate</strong> the step where the error can happen.</li>
<li><strong>Prevent</strong>: design so the error cannot be made, such as a connector that fits only one way or a required system field with a drop-down list.</li>
<li><strong>Detect</strong>: catch the error at once, such as a scale that alarms on a short pick or a system check that blocks an invoice price that differs from the quote.</li>
<li><strong>Mitigate</strong>: reduce the impact when it slips through.</li></ol>
<p>Training and reminders are the weakest controls. Use them, but not alone.</p>
<h3>Selecting solutions</h3>
<p>Score options on <strong>impact</strong> on the CTQ and <strong>effort</strong> (cost, time, risk). Plot them on an impact/effort matrix: high-impact, low-effort ideas are quick wins to do first; high-impact, high-effort ideas need planning and a business case; low-impact ideas are parked. For bigger decisions, a weighted criteria matrix scores each option against agreed criteria such as cost, time to implement, customer impact and risk. Use the lab after this lesson to practise.</p>
""", ["Every solution should link to a verified root cause.", "Prefer eliminating or preventing errors over training and reminders.", "Rank options by impact and effort; do quick wins first."],
 "List three possible solutions for one verified cause in your area. Classify each as eliminate, prevent, detect or mitigate, and estimate its impact and effort.",
 "Which solution is the strongest mistake-proofing for wrong prices on invoices?", ["A reminder email to the billing team", "Extra training on the price list", "A system rule that blocks invoices whose price differs from the quote", "A monthly audit of invoices"], 2,
 "A system check that blocks the error at the point it would occur prevents or immediately detects it, which is stronger than training or after-the-fact audits."),
step("Lean tools for flow", 8, """
<p>Many verified causes point to how work flows. Lean offers a toolbox for that.</p>
<table><thead><tr><th>Tool</th><th>What it does</th><th>Typical use</th></tr></thead><tbody>
<tr><td>5S</td><td>Sort, Set in order, Shine, Standardize, Sustain</td><td>Cut searching, walking and hidden problems</td></tr>
<tr><td>Standard work</td><td>Documents the current best way: sequence, timing, key points</td><td>Reduce person-to-person variation</td></tr>
<tr><td>Smaller batches and one-piece flow</td><td>Moves work on as soon as each unit is done</td><td>Shorten lead time and expose defects sooner</td></tr>
<tr><td>Pull and kanban</td><td>Replenishes only what was used, signalled by a card or bin</td><td>Stop overproduction and control inventory</td></tr>
<tr><td>SMED (quick changeover)</td><td>Moves setup work to while the machine is running and simplifies the rest</td><td>Make small batches economical</td></tr>
<tr><td>Visual management</td><td>Shows status and abnormalities at a glance</td><td>Make problems obvious within minutes</td></tr>
<tr><td>Load levelling (heijunka)</td><td>Spreads volume and mix evenly over time</td><td>Avoid peaks that cause overtime and errors</td></tr>
</tbody></table>
<h3>Batching: the hidden cause of long lead times</h3>
<p>Batching feels efficient: approve all quotes on Friday, run all of one product before switching, release picks in two waves a day. But every item in a batch waits for the whole batch. If quotes are approved once a week, the average quote waits two and a half days just for approval. Approving twice a day, or giving a clear authority limit so most quotes need no approval at all, can cut quote turnaround dramatically without anyone working harder.</p>
<h3>SMED in brief</h3>
<p>Film a changeover. Separate <em>internal</em> tasks (machine must be stopped) from <em>external</em> tasks (can be done while it runs, such as fetching tools and pre-heating dies). Move external tasks out, then simplify internal ones with quick clamps, standard heights and pre-set settings. Shorter changeovers let you run smaller batches, which reduces inventory and lead time.</p>
""", ["Lean tools target flow: 5S, standard work, pull, SMED, visual management.", "Every item in a batch waits for the whole batch.", "Quick changeovers make small batches economical."],
 "Find one place in your process where work is batched, such as approvals, releases or production runs. Estimate how long the average item waits for its batch and what a smaller batch would require.",
 "What is the first step in SMED?", ["Buy faster machines", "Separate internal setup tasks from external ones", "Run larger batches to reduce changeovers", "Train operators to work faster"], 1,
 "SMED starts by identifying which setup tasks can be done while the machine is still running and moving them out of the downtime."),
step("Piloting changes and managing risk with FMEA", 8, """
<p>Before rolling a solution out everywhere, <strong>pilot</strong> it: one line, one shift, one product family or one customer segment, for long enough to see normal variation. A pilot tests whether the solution works, uncovers side effects and builds confidence among the people who will use it.</p>
<p>Plan the pilot like a small experiment: what you will change, where and when, the measure you will track (the same one as the baseline), what result would count as success, and what you will do if it fails. Keep a log of anything unusual during the pilot.</p>
<h3>FMEA: think about what could go wrong</h3>
<p>A <strong>failure mode and effects analysis (FMEA)</strong> looks ahead at how the new process could fail. For each step, the team lists possible failure modes, their effects and causes, and rates three things, usually from 1 to 10:</p>
<ul><li><strong>Severity:</strong> how bad the effect is for the customer or safety.</li>
<li><strong>Occurrence:</strong> how likely the cause is.</li>
<li><strong>Detection:</strong> how likely the current controls are to catch it before it reaches the customer (10 = almost certainly not caught).</li></ul>
<p>Multiplying the three gives a risk priority number (RPN). Many teams now also use an action-priority approach that gives severity extra weight, because a rare but severe failure can deserve action even with a modest RPN. Either way, the team adds actions for the highest risks and re-rates them after the actions are done.</p>
<table><thead><tr><th>Step</th><th>Failure mode</th><th>Effect</th><th>S</th><th>O</th><th>D</th><th>Action</th></tr></thead><tbody>
<tr><td>New pick-to-scale check</td><td>Scale not calibrated</td><td>Short picks pass</td><td>7</td><td>4</td><td>8</td><td>Daily check weight; calibration on schedule</td></tr>
</tbody></table>
<h3>Change is about people too</h3>
<p>Explain why the change is needed, involve users in designing it, train before go-live and make it easy to raise problems during the pilot. Most failed improvements fail on adoption, not on technical merit.</p>
""", ["Pilot changes on a small scale and measure against the baseline.", "FMEA rates severity, occurrence and detection to rank risks.", "Plan for adoption: explain, involve, train and listen."],
 "For one planned change, write a one-paragraph pilot plan: scope, duration, success measure and fallback. Then list two ways the change could fail.",
 "In an FMEA, what does a high detection rating (for example 9) usually mean?", ["The failure is very severe", "The failure happens often", "The failure is easy to catch", "Current controls are unlikely to catch the failure"], 3,
 "Detection is rated so that a high number means the failure is unlikely to be caught before it reaches the customer."),
step("Proving the improvement", 7, """
<p>At the end of Improve, the team must show that the change worked. That means comparing <strong>after</strong> data with the <strong>baseline</strong>, collected the same way: same definition, same source, similar conditions and a long enough period to include normal variation.</p>
<h3>Ways to show the change</h3>
<ul><li><strong>Before-and-after run chart:</strong> plot the measure in time order with a marker where the change went in. A lasting shift after the marker is strong evidence.</li>
<li><strong>Before-and-after histograms or box plots:</strong> show changes in spread and centring, not just the average.</li>
<li><strong>A statistical test:</strong> where the change is modest, a two-sample or two-proportion test confirms it is more than noise.</li></ul>
<h3>Quantifying the benefit</h3>
<p>Translate the improvement into money and customer terms the sponsor recognizes. Separate <strong>hard savings</strong> that reach the financial statements, such as less scrap, lower overtime, fewer credit notes or freight savings, from <strong>soft benefits</strong> such as freed capacity or better customer experience. Freed capacity is only cash if it is used: to take on more work, avoid a hire or reduce overtime. Ask finance to review the savings method; a credible number protects the project's reputation.</p>
<h3>Example</h3>
<p>A fabricator's quote error rate was 8.2% over 12 weeks before the project. After adding a quote template with required fields and an automatic price check, it averaged 2.1% over the following 12 weeks, with no week above 3.5%. Fewer errors meant fewer credit notes and less rework of quotes; finance agreed the method for valuing both. The run chart and the savings summary went into the project report for the sponsor's sign-off.</p>
""", ["Compare after data with the baseline, measured the same way.", "Run charts with a change marker are the clearest evidence.", "Separate hard savings from soft benefits and have finance review them."],
 "Decide how you will show the result of your project: which chart, which period and which money measure. Ask finance how they would like savings calculated.",
 "Which is the best evidence that an improvement worked?", ["The team feels the process is better", "One good week after the change", "A run chart showing a lasting shift after the change, measured as the baseline was", "The supplier says the new material is better"], 2,
 "Data collected the same way as the baseline, showing a sustained shift over time, is the most convincing evidence."),
]

M5 = [
step("Control plans and standard work", 7, """
<p>Most improvements fade. People drift back to old habits, new staff are trained the old way, and a system change quietly removes a check. The Control phase builds the habits and safeguards that keep the gain.</p>
<h3>The control plan</h3>
<p>A control plan is a table that the process owner keeps. For each critical step or CTQ it states:</p>
<table><thead><tr><th>What to control</th><th>Specification or standard</th><th>How measured</th><th>How often and by whom</th><th>Reaction plan</th></tr></thead><tbody>
<tr><td>Quote price matches price list</td><td>100% of lines</td><td>System check report</td><td>Daily, sales coordinator</td><td>Correct quote; if more than 2 in a day, review with sales lead</td></tr>
<tr><td>Fill weight</td><td>500 g, minimum 495 g</td><td>Checkweigher, 5 samples per hour</td><td>Hourly, line operator</td><td>Stop and adjust; quarantine product since last good check</td></tr>
</tbody></table>
<p>The <strong>reaction plan</strong> is the part most often missing. It says exactly what to do when the measure goes out of bounds, so problems are handled the same way every time.</p>
<h3>Standard work</h3>
<p>Standard work captures the current best way to do a task: the steps in order, key points for quality and safety, and the time each takes. Write it with the people who do the work, keep it short and visual (photos beat paragraphs), and post it at the point of use. Standard work is not frozen. It is the baseline for the next improvement: when someone finds a better way, test it and update the standard.</p>
<h3>Training and onboarding</h3>
<p>Update training materials and onboarding checklists so new people learn the new method from day one. Many gains are lost at the first staff change.</p>
""", ["Improvements fade unless the Control phase builds habits and safeguards.", "A control plan states what, how, how often, who and the reaction plan.", "Standard work is the current best way and the baseline for the next improvement."],
 "Draft a control plan row for the most important measure in your project, including a specific reaction plan for when it goes out of bounds.",
 "Which part of a control plan says what to do when a measure goes out of bounds?", ["The reaction plan", "The specification", "The measurement method", "The frequency"], 0,
 "The reaction plan defines the agreed response when a measure is outside its limits, so issues are handled consistently."),
step("Control charts: separating signal from noise", 9, """
<p>A <strong>control chart</strong> is a run chart with a centre line and control limits calculated from the process's own data, usually at three standard deviations of short-term variation either side of the average. Points inside the limits, with no unusual patterns, reflect common-cause variation. Points outside the limits or certain patterns signal a special cause worth investigating.</p>
<p>Control limits come from the process; specification limits come from the customer. Never draw specification limits as control limits. A process can be in control and still not capable of meeting the specification, which is a job for a DMAIC project, not for daily reaction.</p>
<h3>Choosing a chart</h3>
<table><thead><tr><th>Data</th><th>Chart</th><th>Example</th></tr></thead><tbody>
<tr><td>Continuous, one value at a time</td><td>I-MR (individuals and moving range)</td><td>Daily quote turnaround, batch yield</td></tr>
<tr><td>Continuous, small subgroups</td><td>X-bar and R</td><td>Five fill weights sampled each hour</td></tr>
<tr><td>Proportion defective, varying sample size</td><td>p-chart</td><td>Percentage of orders with errors per day</td></tr>
<tr><td>Count of defects per unit or area</td><td>c-chart or u-chart</td><td>Scratches per panel, errors per invoice</td></tr>
</tbody></table>
<h3>Common signals of a special cause</h3>
<ul><li>One point outside a control limit.</li>
<li>A run of eight or so points in a row on one side of the centre line.</li>
<li>A steady trend of six or so points rising or falling.</li>
<li>Patterns that repeat, such as every Monday.</li></ul>
<p>Rule sets vary slightly between references; pick one set, write it on the chart and use it consistently. When a signal appears, follow the reaction plan, find the cause and note it on the chart. When there is no signal, do not adjust the process; that is tampering.</p>
<p>Recalculate control limits only after a deliberate, verified change to the process, not every month.</p>
""", ["Control limits come from the process; specification limits come from the customer.", "Pick the chart by data type: I-MR, X-bar R, p, c or u.", "React to signals with the reaction plan; leave common-cause noise alone."],
 "Choose the right control chart for your project measure. Calculate a first set of limits from 20 or more stable data points, or ask a colleague with a spreadsheet template to help.",
 "On an I-MR chart, nine points in a row fall above the centre line, all inside the control limits. What does this suggest?", ["Nothing; all points are inside the limits", "The process is not capable", "The control limits are wrong and must be widened", "A possible special cause, such as a shift in the process"], 3,
 "A long run on one side of the centre line is a common signal of a process shift even when no point is outside the limits."),
step("Handover, visual management and sustaining the gain", 7, """
<p>A DMAIC project ends with a formal <strong>handover</strong> to the process owner. The project lead does not keep running the new process; the owner does. The handover meeting confirms:</p>
<ul><li>Results against the goal, with the before-and-after evidence.</li>
<li>The control plan, standard work and updated training, all in their permanent home.</li>
<li>Who reviews the key measure, how often, and at which meeting.</li>
<li>Open actions, owners and dates.</li>
<li>Lessons learned and ideas for the next project.</li></ul>
<p>The sponsor signs off the project and the savings method. Celebrate the team's work; recognition is one of the cheapest ways to build an improvement culture.</p>
<h3>Visual management</h3>
<p>Make the key measure visible where the work happens: a whiteboard, a screen or a simple chart updated daily. Good visual management lets anyone see within seconds whether the process is on track and what is being done about problems. Pair it with a short daily or weekly team huddle that reviews the board, logs issues and assigns actions.</p>
<h3>Check that it held</h3>
<p>Schedule follow-up reviews, for example at 30, 60 and 90 days after handover, comparing performance with the improved level. If performance slips, use the reaction plan and find out why: often a new person, a new product or a system change has bypassed a control. The 90-day review is also a good time to confirm the savings with finance.</p>
<h3>From project to habit</h3>
<p>One successful project proves the method. A habit forms when leaders ask about data and root causes at regular meetings, when staff ideas are welcomed and acted on, and when each project's lessons feed the next selection of problems.</p>
""", ["Hand the process over formally to its owner with the control plan and evidence.", "Visual management and short huddles keep the measure in view.", "Review at 30, 60 and 90 days to confirm the gain held."],
 "Decide where your project's key measure will be displayed and at which regular meeting it will be reviewed. Put the 30-, 60- and 90-day reviews in the calendar now.",
 "Who should run the improved process day to day after a DMAIC project?", ["The process owner", "The project lead", "The sponsor", "An external consultant"], 0,
 "The process owner runs the process and keeps the gain; the project lead hands over and moves on."),
step("Your first DMAIC project: a 12-week plan", 7, """
<p>A first DMAIC project in an SME typically takes 8 to 16 weeks of part-time effort, depending on how fast data can be collected and how big the changes are. A 12-week plan is a good starting shape.</p>
<table><thead><tr><th>Weeks</th><th>Phase</th><th>Key activities</th><th>Gate review</th></tr></thead><tbody>
<tr><td>1–2</td><td>Define</td><td>Charter, SIPOC, VOC to CTQ, team kickoff</td><td>Sponsor approves charter</td></tr>
<tr><td>3–5</td><td>Measure</td><td>Process map, data collection plan, measurement check, baseline</td><td>Baseline agreed</td></tr>
<tr><td>6–7</td><td>Analyze</td><td>Pareto, fishbone, 5 Whys, graphs, verify root causes</td><td>Verified causes agreed</td></tr>
<tr><td>8–10</td><td>Improve</td><td>Generate and select solutions, FMEA, pilot, measure results</td><td>Pilot results approved</td></tr>
<tr><td>11–12</td><td>Control</td><td>Control plan, standard work, training, handover</td><td>Project closed, savings signed off</td></tr>
</tbody></table>
<h3>Habits of successful first projects</h3>
<ul><li><strong>Keep scope tight.</strong> It is better to fix one product family or one order type well than all of them halfway.</li>
<li><strong>Meet weekly for 45 to 60 minutes</strong> with a short action log, and hold a brief gate review with the sponsor at the end of each phase.</li>
<li><strong>Collect data early.</strong> Data collection is the most common cause of delay; start it in week 2 or 3.</li>
<li><strong>Do safe quick wins as you go.</strong> If the team finds an obvious, low-risk fix, implement it and note it, rather than holding it for Improve.</li>
<li><strong>Tell the story simply.</strong> A one-page summary, often called an A3, shows the problem, baseline, causes, actions and results on one sheet.</li></ul>
<p>After your first project, take stock: what worked, what slowed you down and which problem should come next? Practice tests on the Training page can help you and your team check your understanding as you build skills.</p>
""", ["Plan around 12 weeks with a gate review at the end of each phase.", "Keep scope tight and start data collection early.", "Summarize the project on one page for the sponsor and the team."],
 "Put your first project into the 12-week table: write the dates of each gate review and who attends, and name the data you will start collecting in week 2.",
 "What is the most common cause of delay in a first DMAIC project?", ["Choosing the project sponsor", "Collecting reliable data", "Writing the charter", "Holding the handover meeting"], 1,
 "Getting reliable data often takes longer than expected, so it should start as early as possible."),
]

course = dict(
 id="lean-six-sigma-foundations",
 title="Lean Six Sigma Foundations: Problem Solving with DMAIC",
 tagline="Use the DMAIC roadmap and core Lean and Six Sigma tools to solve a real process problem and make the fix stick.",
 summary="A practical introduction to Lean Six Sigma for supervisors, managers and improvement leads in small and mid-sized businesses. You will learn the eight wastes and why variation matters, then work through the DMAIC roadmap: chartering a project, measuring a reliable baseline, finding and verifying root causes, piloting and proving solutions, and holding the gain with control plans and control charts. It covers the foundations a Green Belt uses on a project; it is not a certification.",
 audience=["Supervisors, team leads and managers who want to fix recurring process problems",
           "Improvement, quality and operations staff starting their first DMAIC project",
           "SME owners and general managers who sponsor improvement work",
           "Anyone preparing for Green Belt training who wants a practical grounding first"],
 outcomes=["Explain how Lean and Six Sigma work together and spot the eight wastes in any process",
           "Write a project charter with a measurable problem and goal, and frame scope with a SIPOC",
           "Build a reliable baseline with good data collection, measurement checks, DPMO and capability",
           "Find and verify root causes with Pareto charts, fishbones, 5 Whys, graphs and basic tests",
           "Select, pilot and prove mistake-proof solutions using impact/effort and FMEA",
           "Hold the gain with control plans, standard work, control charts and a clean handover"],
 modules=[
  dict(title="Lean Six Sigma Foundations", summary="How Lean and Six Sigma fit together, the eight wastes, why variation matters more than averages, and how to choose and charter a project.", steps=M1),
  dict(title="Define and Measure", summary="Turning customer needs into measurable CTQs, mapping the real process and value stream, collecting trustworthy data and setting the baseline.", steps=M2),
  dict(title="Analyze", summary="Narrowing the problem with Pareto charts, listing causes with a fishbone, digging with 5 Whys and verifying causes with graphs and simple tests.", steps=M3),
  dict(title="Improve", summary="Generating and selecting mistake-proof solutions, Lean tools for flow, piloting with FMEA and proving the result against the baseline.", steps=M4),
  dict(title="Control", summary="Control plans, standard work, control charts, handover to the process owner and a 12-week plan for your first project.", steps=M5)],
 labs=[
  dict(id="lss-value-or-waste", type="classify", title="Value, necessary or waste?", after_step=2,
       intro="Sort twelve activities from an order-to-delivery process into value-added, business-necessary or waste, then check your answers. It trains your eye for waste before you map your own process.",
       config=dict(categories=["Value-added", "Business-necessary", "Waste"], items=[
        dict(text="Machining the part to the customer's drawing", answer=0, why="It changes the product in a way the customer specified and pays for."),
        dict(text="Assembling the customer's order kit", answer=0, why="It physically creates what the customer ordered."),
        dict(text="Packing the order securely for shipment", answer=0, why="Protecting the goods so they arrive undamaged is part of what the customer pays for."),
        dict(text="Recording lot numbers required for food-safety traceability", answer=1, why="It adds no value the customer sees but is required by regulation, so keep it and make it efficient."),
        dict(text="Running the year-end inventory count for the auditors", answer=1, why="Required for financial reporting today, though better inventory control can reduce the effort."),
        dict(text="Safety lockout before machine maintenance", answer=1, why="Essential and required; never a target for removal, only for making it smooth."),
        dict(text="Re-keying order details from email into the ERP", answer=2, why="Over-processing: the same data is entered twice instead of captured once."),
        dict(text="Orders waiting two days for a manager's approval", answer=2, why="Waiting adds lead time without adding value."),
        dict(text="Moving pallets to a temporary area and back again", answer=2, why="Unnecessary transportation."),
        dict(text="Reworking welds that failed inspection", answer=2, why="Defects and the rework they cause are waste."),
        dict(text="Making extra parts in case the next order comes", answer=2, why="Overproduction creates inventory, handling and obsolescence risk."),
        dict(text="Walking to a shared printer in another building", answer=2, why="Motion waste caused by layout."),
       ])),
  dict(id="lss-sigma-calculator", type="calc", title="Baseline calculator: DPU, DPMO and sigma level", after_step=8,
       intro="Enter the units checked, defect opportunities per unit and defects found to calculate DPU, yield, DPMO and process sigma for your baseline.",
       config=dict(calc="sigma", note="Count only opportunities that matter to the customer; counting trivial ones makes performance look better than it is. Sigma level uses the conventional 1.5 sigma shift.")),
  dict(id="lss-solution-matrix", type="matrix", title="Impact and effort: choosing solutions", after_step=13,
       intro="Place seven possible solutions for an order-error project on an impact/effort grid to see which to do first, which need a plan and which to park.",
       config=dict(x="Effort and cost", y="Impact on order errors", x_low="Low effort", x_high="High effort", y_low="Low impact", y_high="High impact",
        quadrants=dict(top_left="Quick wins", top_right="Plan carefully", bottom_left="Maybe later", bottom_right="Avoid for now"),
        items=[dict(name="Required unit-of-measure field on pick tickets", x=1, y=5),
               dict(name="Automatic price check against the quote", x=2, y=5),
               dict(name="New warehouse management system", x=5, y=4),
               dict(name="Barcode scan at packing", x=3, y=4),
               dict(name="Reminder poster in the warehouse", x=1, y=1),
               dict(name="Second person checks every order", x=4, y=3),
               dict(name="Redesign the order entry screen", x=3, y=3)])),
 ],
 exam=[],
 figures=[
  dict(step=1, type="cycle", title="The DMAIC roadmap", caption="Click each phase to see the question it answers. Control feeds the next round of improvement.",
       config=dict(center="DMAIC", stages=[
        dict(label="Define", text="Agree the problem, customer, goal and scope in a one-page charter."),
        dict(label="Measure", text="Map the process, check the measurement system and set a reliable baseline."),
        dict(label="Analyze", text="Narrow the problem and verify root causes with data and observation."),
        dict(label="Improve", text="Select, pilot and prove solutions that remove the verified causes."),
        dict(label="Control", text="Hold the gain with a control plan, standard work and a control chart.")])),
  dict(step=6, type="flow", title="Where an order's lead time goes", caption="Watch orders move through the steps, then click 'Fix the bottleneck' to see why the approval queue limits the whole flow.",
       config=dict(steps=[
        dict(label="Receive PO", text="Purchase order arrives by email and waits in a shared inbox."),
        dict(label="Enter order", text="Order details are keyed into the ERP."),
        dict(label="Credit approval", text="Orders over the limit wait for one manager, who approves in batches."),
        dict(label="Pick and pack", text="Orders are released to the warehouse in two waves a day."),
        dict(label="Ship", text="Carrier collects at the end of the day.")], bottleneck=2,
        fix_text="Giving staff a clear approval limit and approving the rest twice a day removes most of the queue, so orders flow to the warehouse the same day.")),
  dict(step=9, type="bars", title="Pareto of order errors in one quarter", caption="Example counts for 200 order errors. The two tallest bars make up 68% of the total, so they become the project focus.",
       config=dict(unit="errors", items=[dict(label="Wrong quantity", value=84, highlight=True), dict(label="Wrong item", value=52, highlight=True), dict(label="Wrong price", value=30), dict(label="Wrong address", value=20), dict(label="Other", value=14)],
        note="In this example, wrong quantity and wrong item cause two thirds of all errors.")),
  dict(step=14, type="compare", title="Batch-and-queue vs flow", caption="Toggle between the two ways of running the same process and notice what happens to waiting and to problems.",
       config=dict(left=dict(title="Batch and queue", points=["Quotes approved once a week", "Large production runs between changeovers", "Problems found only when the batch is inspected", "Long, unpredictable lead times"]),
                   right=dict(title="Flow", points=["Clear approval limits; the rest approved twice a day", "Short changeovers make small runs economical", "Problems show up on the next unit, not days later", "Shorter, steadier lead times"]))),
  dict(step=17, type="stack", title="What keeps an improvement in place", caption="Click each layer, from the bottom up, to see how each control builds on the one below.",
       config=dict(top_label="A gain that lasts", layers=[
        dict(label="Mistake-proofing", text="Design so the error cannot happen or is caught at once."),
        dict(label="Standard work", text="The current best way, written with the team and posted at the point of use."),
        dict(label="Control plan", text="What is measured, how often, by whom, and the reaction plan."),
        dict(label="Control chart", text="Separates signals from noise so people react only when they should."),
        dict(label="Leader routines", text="The measure is reviewed at a regular meeting and staff ideas are acted on.")])),
  dict(step=20, type="timeline", title="A 12-week first DMAIC project", caption="Click each phase to see its main activities and the gate review that closes it.",
       config=dict(phases=[
        dict(label="Weeks 1–2", title="Define", items=["Charter and SIPOC", "Voice of the customer to CTQ", "Sponsor approves charter"]),
        dict(label="Weeks 3–5", title="Measure", items=["Process map", "Data collection plan and measurement check", "Baseline agreed"]),
        dict(label="Weeks 6–7", title="Analyze", items=["Pareto and fishbone", "5 Whys and graphs", "Root causes verified"]),
        dict(label="Weeks 8–10", title="Improve", items=["Select solutions", "FMEA and pilot", "Results proved against baseline"]),
        dict(label="Weeks 11–12", title="Control", items=["Control plan and standard work", "Training and handover", "Savings signed off"])])),
 ],
)

E = lambda q, opts, a, why: dict(q=q, opts=opts, a=a, why=why)
course["exam"] = [
 E("Which pairing best describes the focus of Lean and of Six Sigma?", ["Lean: waste and flow; Six Sigma: variation and defects", "Lean: statistics; Six Sigma: 5S", "Lean: cost cutting by headcount; Six Sigma: software", "Lean: marketing; Six Sigma: finance"], 0, "Lean removes waste and improves flow; Six Sigma reduces variation and defects."),
 E("What is the correct order of the DMAIC phases?", ["Design, Measure, Analyze, Implement, Close", "Define, Measure, Analyze, Improve, Control", "Define, Map, Analyze, Improve, Check", "Discover, Measure, Act, Improve, Control"], 1, "DMAIC stands for Define, Measure, Analyze, Improve and Control."),
 E("Staff ideas for fixing a recurring problem are never asked for. Which of the eight wastes is this?", ["Motion", "Inventory", "Skills (unused talent)", "Over-processing"], 2, "Not using people's knowledge and ideas is the waste of unused skills."),
 E("Two shipping teams both average three days, but one ranges from one to nine days. Why does the customer of that team complain more?", ["Its average is higher", "It ships fewer orders", "It uses a different carrier", "Customers feel the variation, and more of its orders are late"], 3, "Equal averages can hide very different variation; customers experience the late orders."),
 E("A broken scanner causes one bad day of picking errors. What type of variation is this, and what is the right response?", ["Special cause; find and fix the specific cause", "Common cause; redesign the whole process", "Common cause; ignore it", "Special cause; widen the control limits"], 0, "An unusual event outside the normal pattern is a special cause and needs a specific fix."),
 E("Which goal statement is best for a project charter?", ["Improve invoice accuracy", "Make customers happier with billing", "Reduce invoice price errors from 6% to below 2% by September 30", "Implement the new billing module"], 2, "A good goal is measurable, has a target and a date, and does not prescribe a solution."),
 E("What does the P in SIPOC stand for, and how detailed should it be?", ["Process; five to seven high-level steps", "People; every person involved", "Price; the cost of each input", "Procedure; the full written procedure"], 0, "The SIPOC process column has five to seven high-level steps to frame scope."),
 E("A customer says 'your deliveries are always late'. Which is a good CTQ?", ["Customers feel positive about delivery", "Trucks leave the yard early", "The warehouse works faster", "Order delivered on or before the promised date"], 3, "A CTQ turns the customer's comment into a measurable requirement."),
 E("An order takes six working days end to end, but hands-on work is about an hour. What is the main opportunity?", ["Speed up each task", "Reduce waiting and queues between steps", "Add a quality inspection", "Buy faster computers"], 1, "When lead time is mostly waiting, cutting queues, batching and approvals gives the biggest gain."),
 E("Why record stratification factors such as shift, product and operator with your data?", ["To identify individuals for discipline", "To make the data set larger", "So the data can later be split to find where problems concentrate", "Because auditors require it"], 2, "Stratification factors let the team see whether defects concentrate in particular conditions, pointing to causes."),
 E("What does a gauge R&R or attribute agreement study check?", ["Whether the measurement system is reliable", "Whether the process meets specification", "Whether the project saves money", "Whether the team is trained"], 0, "These studies check that variation in the data comes from the process, not the measurement."),
 E("A process has 50 defects in 5,000 units with 2 opportunities per unit. What is the DPMO?", ["10,000", "1,000", "2,500", "5,000"], 3, "DPMO = 50 ÷ (5,000 × 2) × 1,000,000 = 5,000."),
 E("What does a Cpk below 1.0 indicate for a stable process?", ["The process is perfectly centred", "The process routinely produces output outside specification", "The control limits are too wide", "The measurement system is unreliable"], 1, "Cpk below 1.0 means the spread and centring do not fit within the specification limits."),
 E("What is the main purpose of a Pareto chart?", ["To prove the root cause", "To show the few categories that cause most of the problem", "To show data in time order", "To calculate process capability"], 1, "A Pareto chart ranks categories so the team can focus on the biggest contributors."),
 E("A 5 Whys ends at 'the clerk made a typing mistake'. What should the team do next?", ["Close the analysis", "Retrain the clerk", "Ask why the system made that mistake easy to make", "Add a second clerk"], 2, "Human error should prompt one more why: what in the process or system made the error easy?"),
 E("A histogram of fill weights shows two distinct peaks. What is the most likely explanation?", ["The process is perfectly capable", "The sample is too small", "The specification is wrong", "Data from two different conditions, such as two machines, is mixed together"], 3, "A two-humped histogram usually means two conditions or processes are mixed in the data."),
 E("A test gives p = 0.03 when comparing two shifts' cycle times. With a 0.05 cut-off, what do you conclude?", ["The difference is likely real, so check whether it is large enough to matter", "The shifts are identical", "The test is invalid", "The night shift is definitely to blame"], 0, "p below 0.05 suggests a real difference; its practical importance still needs judging."),
 E("Which mistake-proofing approach is strongest?", ["Training and reminders", "Detecting the error at final inspection", "Designing the step so the error cannot be made", "Auditing a sample each month"], 2, "Preventing the error by design is stronger than detection, audits or reminders."),
 E("In an FMEA, which three ratings are combined to prioritize risks?", ["Cost, time and quality", "Severity, occurrence and detection", "Impact, effort and urgency", "Probability, budget and scope"], 1, "FMEA rates severity, occurrence and detection; their product is the risk priority number."),
 E("On a control chart with no signals, what should the operator do?", ["Adjust the process toward target after each reading", "Recalculate the limits", "Stop the line", "Leave the process alone and keep monitoring"], 3, "Without a signal, variation is common cause; adjusting would be tampering."),
]

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(here), "lean-six-sigma.json")
    json.dump(course, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    print("lessons", sum(len(m["steps"]) for m in course["modules"]), "exam", len(course["exam"]), Counter(q["a"] for q in course["exam"]),
          "checks", Counter(s["check"]["a"] for m in course["modules"] for s in m["steps"]))
