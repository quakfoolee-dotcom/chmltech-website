"""Source for content/courses/erp-selection.json (run: python3 content/courses/src/erp_selection.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import step, E, write

M1 = [
step("Signs you have outgrown your systems", 6, """
<p>Most SMEs start with accounting software, spreadsheets and email. That works until growth, complexity or customer expectations outpace it. Knowing the warning signs helps you decide when new software is worth the cost and disruption.</p>
<h3>Common signs</h3>
<ul><li><strong>Re-keying:</strong> the same order, customer or product is typed into several systems or spreadsheets.</li>
<li><strong>No single view:</strong> nobody can quickly say what is in stock, what is on order or what a customer owes.</li>
<li><strong>Reporting takes days:</strong> month-end and management reports are assembled by hand.</li>
<li><strong>Errors and rework:</strong> wrong prices, missed orders, shipping mistakes and inventory that never matches.</li>
<li><strong>Key-person dependence:</strong> critical processes live in one person's spreadsheet or head.</li>
<li><strong>Growth limits:</strong> new locations, product lines, e-commerce or customer requirements, such as lot traceability or EDI, can't be supported.</li>
<li><strong>Unsupported software:</strong> the current system is old, unsupported or no longer secure.</li></ul>
<h3>Software is not always the answer</h3>
<p>Some problems come from unclear processes, untrained staff or poor data rather than the software itself. A new system on top of a broken process automates the mess. Before shopping, ask whether better use of current tools, cleaner data or a fixed process would solve the problem.</p>
<h3>What this course covers</h3>
<p>This course walks through the full path: understanding needs, building a business case, writing requirements, shortlisting, running scripted demonstrations, scoring, comparing total cost, negotiating contracts, choosing an implementation partner and preparing for a successful go-live. It applies to ERP and to other major business software, such as CRM and warehouse management systems.</p>
""", ["Re-keying, no single view, slow reporting and errors are signs of outgrown systems.", "Growth needs such as traceability or e-commerce can force a change.", "Check whether process, data or training fixes would solve the problem first."],
 "List the five biggest system frustrations in your business, with an example and an estimate of hours lost per week for each.",
 "Which is a strong sign a business has outgrown its systems?", ["Staff take lunch breaks", "The same order is re-keyed into several systems and spreadsheets", "The office has Wi-Fi", "Reports are reviewed monthly"], 1,
 "Re-keying shows systems aren't connected and creates errors and wasted time."),
step("Types of business software", 7, """
<p>Before choosing, understand what each type of system does and how they fit together.</p>
<table><thead><tr><th>System</th><th>Main job</th><th>Typical functions</th></tr></thead><tbody>
<tr><td>Accounting</td><td>Financial records</td><td>General ledger, invoicing, payables, receivables, bank reconciliation, financial statements</td></tr>
<tr><td>ERP (enterprise resource planning)</td><td>Run operations and finance on one database</td><td>Sales orders, purchasing, inventory, manufacturing, costing, plus accounting</td></tr>
<tr><td>CRM (customer relationship management)</td><td>Manage customers and sales</td><td>Contacts, leads, opportunities, quotes, activities, marketing, service cases</td></tr>
<tr><td>WMS (warehouse management system)</td><td>Run the warehouse in detail</td><td>Bin locations, directed picking, scanning, cycle counts, shipping</td></tr>
<tr><td>MES (manufacturing execution system)</td><td>Run the shop floor</td><td>Work orders, scheduling, machine data, quality and labour tracking</td></tr>
<tr><td>E-commerce and EDI</td><td>Online and electronic ordering</td><td>Web store, customer portals, electronic orders and invoices with large customers</td></tr>
</tbody></table>
<h3>Suite versus best of breed</h3>
<p>A <strong>suite</strong> offers many functions from one vendor on one database: fewer integrations and one source of truth, but some modules may be weaker than specialists. <strong>Best of breed</strong> combines specialist systems, such as an ERP with a separate CRM and WMS: deeper functions where you need them, but more integrations to build and maintain. Many SMEs choose an ERP suite and add one or two specialist systems where their needs are demanding.</p>
<h3>Cloud versus on-premises</h3>
<p>Most new SME software is cloud-based (software as a service): subscription pricing, vendor-managed updates and security, and access from anywhere. On-premises software runs on your own servers: more control and possibly lower long-term licence cost, but you handle hardware, updates and security. Cloud is the default for most SMEs today unless there is a specific reason otherwise.</p>
<p>Examples of SME-focused systems include QuickBooks, Sage, Xero, Acumatica, Microsoft Dynamics 365 Business Central, Oracle NetSuite, Odoo and SAP Business One; there are many others, including industry-specific options. These are examples, not recommendations. The lab after this lesson asks you to match functions to systems.</p>
""", ["Accounting, ERP, CRM, WMS, MES and e-commerce systems each have a distinct job.", "Suites reduce integrations; best of breed gives depth where you need it.", "Cloud is the usual default for SMEs; on-premises suits specific needs."],
 "Draw your current systems as boxes with arrows showing where data is passed by hand or by integration. Circle the biggest gap.",
 "What is the main advantage of an ERP suite over separate systems?", ["It is always cheaper", "Many functions share one database, reducing integrations and duplicate data", "It needs no training", "It replaces the need for staff"], 1,
 "A shared database gives one source of truth with fewer integrations."),
step("Map your processes before shopping for software", 8, """
<p>The most common selection mistake is shopping for software before understanding the business's own processes. Vendors then lead the conversation with their features rather than your needs.</p>
<h3>Map the core processes</h3>
<p>Map the main end-to-end processes as they work today, with the people who do them:</p>
<ul><li><strong>Quote to cash:</strong> enquiry, quote, order, fulfilment, invoice, payment.</li>
<li><strong>Procure to pay:</strong> requisition, purchase order, receipt, supplier invoice, payment.</li>
<li><strong>Plan to produce</strong> (for manufacturers): forecast, plan, materials, production, quality.</li>
<li><strong>Inventory:</strong> receiving, put-away, storage, counting, picking, shipping.</li>
<li><strong>Record to report:</strong> month-end close and management reporting.</li></ul>
<p>Swim-lane maps work well: one lane per role or department, showing handoffs, systems used, spreadsheets, approvals and waiting.</p>
<h3>Mark pain points and improvements</h3>
<p>On each map, mark re-keying, delays, errors, workarounds and missing information. Then sketch the future process: what should happen, with which system doing what. Some improvements need no software at all; others become clear requirements.</p>
<h3>What makes you different</h3>
<p>Identify the few processes that are genuinely unusual or give you an advantage, such as complex product configuration, special pricing or unique compliance needs. These deserve the closest attention in selection. For standard processes like payables, adopting the software's standard way of working is usually cheaper and easier than customizing it.</p>
<p>Process maps also become the backbone of your requirements and the scripts for vendor demonstrations, covered later in the course.</p>
""", ["Map end-to-end processes before talking to vendors.", "Mark pain points and sketch the future process.", "Focus selection on what makes you different; adopt standard ways for standard processes."],
 "Map your quote-to-cash process as a swim lane with your team. Mark every re-keying step, delay and spreadsheet.",
 "For a standard process such as paying supplier invoices, what is usually the best approach in a new system?", ["Customize the software to match your current way exactly", "Adopt the software's standard way of working", "Keep doing it in a spreadsheet", "Skip it"], 1,
 "Standard processes are usually best handled by the software's standard approach, avoiding costly customization."),
step("The business case and budget", 7, """
<p>New business software is a significant investment of money and staff time. A business case clarifies why you are doing it, what success looks like and what you can afford.</p>
<h3>What the business case covers</h3>
<table><thead><tr><th>Section</th><th>Content</th></tr></thead><tbody>
<tr><td>Problem and goals</td><td>The pain points and the measurable outcomes you want</td></tr>
<tr><td>Scope</td><td>Which processes, sites and users are included</td></tr>
<tr><td>Benefits</td><td>Hours saved, errors reduced, inventory lowered, faster close, growth enabled</td></tr>
<tr><td>Costs</td><td>Subscriptions or licences, implementation, data migration, integrations, training, internal time, hardware</td></tr>
<tr><td>Risks</td><td>Disruption at go-live, staff capacity, data quality, partner capability</td></tr>
<tr><td>Timeline</td><td>Selection, implementation and stabilization</td></tr>
</tbody></table>
<h3>Measurable goals</h3>
<p>Write goals you can check after go-live: "month-end close in 5 working days instead of 12", "inventory accuracy above 95%", "eliminate re-keying of orders", "same-day order confirmation". They guide every decision during selection and implementation.</p>
<h3>Budget realistically</h3>
<p>The subscription is often not the largest cost in the first years. Implementation services, data migration, integrations, training and the time your own staff spend can each be substantial. Internal time is the most underestimated cost: key users may spend a large share of their week on the project for several months.</p>
<h3>Funding</h3>
<p>Some government programs support technology adoption by SMEs, including planning and implementation. Check the Funding page on this site, and confirm current eligibility and terms directly with each program before relying on them.</p>
""", ["Write a business case with goals, scope, benefits, costs, risks and timeline.", "Set measurable goals you can check after go-live.", "Budget for implementation, data, integration, training and internal time, not just subscriptions."],
 "Write three measurable goals for a new system and list every cost category you will need to estimate, including internal staff time.",
 "Which cost is most often underestimated in software projects?", ["The vendor's logo design", "Internal staff time spent on the project", "Office rent", "The first month's subscription"], 1,
 "Key users spend significant time on design, testing, data and training."),
]

M2 = [
step("Writing requirements that matter", 8, """
<p>Requirements describe what the software must do for your business. Good requirements make vendors show what matters and make comparisons fair.</p>
<h3>Prioritize</h3>
<ul><li><strong>Must have:</strong> essential; a system without it is unacceptable (for example, lot traceability for a food distributor).</li>
<li><strong>Should have:</strong> important but workable without, or with a workaround.</li>
<li><strong>Could have:</strong> nice to have.</li></ul>
<p>Keep must-haves genuinely essential. A list of 300 must-haves makes every vendor look the same and hides the few requirements that decide success.</p>
<h3>Write scenarios, not just features</h3>
<p>A feature list ("supports units of measure: yes/no") invites every vendor to tick yes. A scenario shows how it really works:</p>
<p><em>"A customer orders 10 cases of product A. We buy it by the pallet of 40 cases and sell it by the case or by the each. Show how the order is entered, how inventory is reduced in the right unit, and how the invoice shows the correct unit price."</em></p>
<h3>Cover all requirement types</h3>
<table><thead><tr><th>Type</th><th>Examples</th></tr></thead><tbody>
<tr><td>Functional</td><td>Order entry, pricing rules, inventory, production, accounting</td></tr>
<tr><td>Reporting</td><td>Key reports and dashboards needed on day one</td></tr>
<tr><td>Integration</td><td>E-commerce, EDI, payroll, banking, shipping carriers, CRM</td></tr>
<tr><td>Technical</td><td>Cloud hosting, security, multi-factor authentication, data residency, backups</td></tr>
<tr><td>Vendor and support</td><td>Local partner, support hours, upgrade approach, industry experience</td></tr>
<tr><td>Commercial</td><td>Pricing model, contract terms, exit and data ownership</td></tr>
</tbody></table>
<p>Build requirements from your process maps and pain points, with input from each department.</p>
""", ["Prioritize as must, should and could; keep must-haves few.", "Write scenarios that show how the system handles your real work.", "Cover functional, reporting, integration, technical, vendor and commercial needs."],
 "Write ten must-have requirements for your business, at least three of them as scenarios based on your process maps.",
 "Why are scenarios better than yes/no feature lists?", ["They are shorter", "They show how the system handles your real situations, not just whether a feature exists", "Vendors prefer them", "They avoid demonstrations"], 1,
 "Scenarios reveal how well a system actually fits your work."),
step("Finding and shortlisting vendors and partners", 7, """
<p>With requirements in hand, build a long list of possible systems and narrow it to a shortlist of three or four for detailed evaluation.</p>
<h3>Building the long list</h3>
<ul><li>Systems used by similar businesses in your industry and size range.</li>
<li>Recommendations from peers, industry associations, your accountant and advisers.</li>
<li>Industry-specific systems, which may fit unusual needs better than general ERPs.</li>
<li>Review sites and analyst reports, read with some skepticism.</li></ul>
<h3>Narrowing to a shortlist</h3>
<p>Screen the long list against a few knock-out criteria:</p>
<ul><li>Covers all must-have requirements, at least on paper.</li>
<li>Suits your size and complexity: neither too basic nor built for much larger companies.</li>
<li>Has a capable implementation partner or vendor team in your region or time zone.</li>
<li>Fits your budget range.</li>
<li>Has references in your industry.</li></ul>
<h3>The partner matters as much as the software</h3>
<p>Many ERP systems are sold and implemented by partners (resellers) rather than the vendor directly. The same software can succeed or fail depending on the partner's industry knowledge, team quality and approach. Evaluate the partner alongside the product, and meet the people who would actually work on your project, not only the sales team.</p>
<h3>Check references early</h3>
<p>Ask each shortlisted vendor or partner for two or three references from similar companies that went live in the past few years. Call them and ask what went well, what they would do differently, how the partner handled problems and whether the project stayed on budget.</p>
""", ["Build a long list from peers, industry systems and advisers.", "Shortlist three or four using knock-out criteria.", "Evaluate the implementation partner as carefully as the software, and call references."],
 "Build a long list of six to ten possible systems and screen them against five knock-out criteria to reach a shortlist of three or four.",
 "Why must the implementation partner be evaluated alongside the software?", ["Partners set the software's price list", "The same software can succeed or fail depending on the partner's knowledge, team and approach", "Partners write the source code", "Partners are not involved after the sale"], 1,
 "Partner capability strongly affects implementation success."),
step("Requests for information and proposals", 7, """
<p>A structured request helps you compare vendors on the same basis. For SMEs it should be proportionate: clear and focused rather than a hundred-page document.</p>
<h3>Request for information (RFI) or proposal (RFP)</h3>
<p>An <strong>RFI</strong> is a short questionnaire to narrow a long list. An <strong>RFP</strong> asks shortlisted vendors for a detailed proposal and price. Many SMEs combine them into one focused document.</p>
<h3>What to include</h3>
<ul><li>Company overview: what you do, size, sites, users, growth plans.</li>
<li>Current systems and the problems you want to solve.</li>
<li>Scope: processes, modules, integrations and data migration.</li>
<li>Requirements, with must-haves highlighted and key scenarios.</li>
<li>What you need back: how each requirement is met (standard, configuration, customization, add-on or not available), implementation approach, team, timeline, pricing for software and services, support model and references.</li>
<li>Your timeline and how you will evaluate responses.</li></ul>
<h3>Ask how, not just whether</h3>
<p>Ask vendors to classify each requirement as standard, configured, customized, third-party add-on or not met. A requirement met only through customization or an add-on carries more cost and risk than one met as standard.</p>
<h3>Pricing in a comparable format</h3>
<p>Give a pricing template: users by type, modules, subscription per year, implementation services by phase, data migration, integrations, training and support. Without a template, proposals price different scopes and can't be compared.</p>
""", ["Use a focused RFI or RFP proportionate to the project.", "Ask how each requirement is met: standard, configured, customized, add-on or not.", "Provide a pricing template so proposals can be compared."],
 "Draft the outline of a focused RFP for your project using the headings in this lesson, including a pricing template.",
 "A vendor meets a key requirement only through customization. What does this usually mean?", ["No extra cost or risk", "More cost and risk to build, test and maintain through upgrades", "The requirement is unimportant", "The vendor is the best choice"], 1,
 "Customizations add build cost and can complicate future upgrades."),
step("Scripted demonstrations", 8, """
<p>A standard vendor demo shows the software's best features with perfect sample data. A <strong>scripted demonstration</strong> makes vendors show how their system handles your processes, using your scenarios and, ideally, your data.</p>
<h3>Preparing the script</h3>
<ul><li>Pick 6 to 10 key scenarios from your process maps and must-haves.</li>
<li>Provide sample data: a few real products, customers, prices and orders.</li>
<li>Specify what you want to see step by step, including reports and exceptions, such as a partial shipment, a return, a price change or a backorder.</li>
<li>Send the script two to three weeks ahead so vendors can prepare.</li></ul>
<h3>Running the demonstrations</h3>
<ul><li>Give each vendor the same script and time.</li>
<li>Involve the people who will use the system: sales, purchasing, warehouse, finance.</li>
<li>Ask "show me", not "can it?". If they say it can, ask them to show it now or in a follow-up.</li>
<li>Note whether each scenario was shown as standard, configured or "we would customize that".</li>
<li>Score each scenario immediately after it is shown, using a common scorecard.</li></ul>
<h3>Watch for</h3>
<ul><li>Screens that switch to different products or add-ons not in the proposal.</li>
<li>Workarounds that look simple in a demo but would be tedious daily.</li>
<li>How easily users could find their way: count the clicks for common tasks.</li></ul>
<p>The lab after this lesson asks you to compare shortlisted options by fit and cost.</p>
""", ["Use scripted demonstrations with your scenarios and data.", "Involve real users, ask 'show me' and score each scenario immediately.", "Watch for add-ons, awkward workarounds and usability."],
 "Write a demonstration script with six scenarios from your process maps, including at least two exceptions such as a return or partial shipment.",
 "During a demo, a vendor says 'yes, it can do that'. What should you ask?", ["Nothing; accept it", "To show it now or in a follow-up session", "For a discount", "To skip the next scenario"], 1,
 "Seeing it done reveals how well it really works."),
]

M3 = [
step("Scoring and selecting", 7, """
<p>A structured scorecard turns many opinions into a defensible decision.</p>
<h3>A weighted scorecard</h3>
<table><thead><tr><th>Criterion</th><th>Weight</th><th>System A (1–5)</th><th>System B (1–5)</th></tr></thead><tbody>
<tr><td>Fit to must-have scenarios</td><td>35%</td><td>4</td><td>5</td></tr>
<tr><td>Usability for daily users</td><td>15%</td><td>4</td><td>3</td></tr>
<tr><td>Partner capability and references</td><td>20%</td><td>3</td><td>4</td></tr>
<tr><td>Total cost of ownership (5 years)</td><td>20%</td><td>4</td><td>3</td></tr>
<tr><td>Technology, integration and security</td><td>10%</td><td>4</td><td>4</td></tr>
<tr><td><strong>Weighted score</strong></td><td>100%</td><td><strong>3.80</strong></td><td><strong>4.00</strong></td></tr>
</tbody></table>
<p>Agree the criteria and weights before the demonstrations, so they are not adjusted to favour a preferred option afterwards.</p>
<h3>Who scores</h3>
<p>Each evaluation team member scores the areas they know. Discuss large differences between scorers: they often reveal a misunderstanding or an important concern.</p>
<h3>Beyond the numbers</h3>
<p>Use the scorecard to inform the decision, not to make it mechanically. Close scores call for a final round: a follow-up demonstration of the weakest areas, a site visit to a reference customer or a short paid workshop to test a critical scenario in more depth.</p>
<h3>Due diligence on the winner</h3>
<ul><li>Check the vendor's and partner's financial stability and how long they have supported the product.</li>
<li>Confirm the product roadmap and how upgrades work.</li>
<li>Review security certifications and where your data will be hosted.</li>
<li>Call at least two more references.</li></ul>
""", ["Use a weighted scorecard agreed before demonstrations.", "Have each person score what they know and discuss differences.", "Use scores to inform, not replace, judgment, and do due diligence on the winner."],
 "Draft your scorecard criteria and weights now, before any demonstrations, and agree them with the evaluation team.",
 "When should scorecard criteria and weights be agreed?", ["After seeing which vendor the team likes", "Before the demonstrations", "After signing the contract", "Never; scoring should be informal"], 1,
 "Agreeing first prevents bias toward a preferred option."),
step("Total cost of ownership", 7, """
<p>Comparing first-year subscription prices can mislead. <strong>Total cost of ownership (TCO)</strong> adds up every cost over a realistic period, usually five years.</p>
<h3>TCO components</h3>
<table><thead><tr><th>Category</th><th>Examples</th></tr></thead><tbody>
<tr><td>Software</td><td>Subscriptions or licences by user type and module; add-ons; annual price increases</td></tr>
<tr><td>Implementation</td><td>Partner services for design, configuration, project management</td></tr>
<tr><td>Data migration</td><td>Cleaning, mapping and loading data</td></tr>
<tr><td>Integrations</td><td>E-commerce, EDI, payroll, banking, carriers; build and ongoing maintenance</td></tr>
<tr><td>Customizations</td><td>Build, testing and maintenance through upgrades</td></tr>
<tr><td>Training</td><td>Initial and ongoing, including new hires</td></tr>
<tr><td>Internal time</td><td>Staff time on the project and backfill</td></tr>
<tr><td>Support and hosting</td><td>Support plans, any hosting, hardware such as scanners and printers</td></tr>
</tbody></table>
<h3>Example</h3>
<p>Twenty-five users at $110 per user per month is $33,000 a year. Add $60,000 of partner fees, $25,000 of internal time and $6,000 a year for add-ons and support. Over five years, TCO is about $280,000, or about $190 per user per month: much more than the subscription alone suggests. The lab after this lesson calculates TCO for your options.</p>
<h3>Questions to ask about pricing</h3>
<ul><li>What are the user types, and which roles need full versus limited licences?</li>
<li>How much can the subscription rise at renewal?</li>
<li>What is included in support, and what costs extra?</li>
<li>What happens to price if users or modules are added or removed?</li></ul>
""", ["Compare total cost over about five years, not first-year price.", "Include implementation, data, integrations, customization, training and internal time.", "Ask about user types, renewal increases and what support includes."],
 "Build a five-year TCO table for your shortlisted options using the categories in this lesson.",
 "Why is comparing only first-year subscription prices misleading?", ["Subscriptions never change", "Implementation, integration, training and internal time can exceed the subscription", "Vendors don't charge subscriptions", "Year one is always free"], 1,
 "Total cost includes many costs beyond the subscription."),
step("Contracts and negotiation", 7, """
<p>The contract sets your rights for years. Review it carefully, ideally with a lawyer experienced in technology contracts.</p>
<h3>Software subscription terms</h3>
<ul><li><strong>Term and renewal:</strong> length, automatic renewal and notice periods.</li>
<li><strong>Price protection:</strong> caps on increases at renewal.</li>
<li><strong>Users and modules:</strong> how to add or reduce them, and minimums.</li>
<li><strong>Service levels:</strong> uptime commitments, support response times and remedies.</li>
<li><strong>Data:</strong> you own your data; where it is hosted; backups; security obligations and breach notification.</li>
<li><strong>Exit:</strong> how you get your data back in a usable format, and for how long after termination.</li></ul>
<h3>Implementation services terms</h3>
<ul><li><strong>Scope:</strong> a clear statement of work listing deliverables, assumptions and what is excluded.</li>
<li><strong>Pricing model:</strong> fixed price, time and materials, or a cap; how changes are priced.</li>
<li><strong>Team:</strong> named key people and how replacements are handled.</li>
<li><strong>Acceptance:</strong> how deliverables and go-live readiness are accepted.</li>
<li><strong>Payment milestones</strong> tied to delivered results, not just elapsed time.</li></ul>
<h3>Negotiating</h3>
<p>Leverage is highest before you sign. Common negotiable items include multi-year price caps, implementation discounts, extra training, a ramp-up of user licences during implementation, and favourable payment timing. Be wary of deep first-year discounts that disappear at renewal. A fair deal that keeps the partner motivated is worth more than squeezing the last dollar.</p>
""", ["Check term, renewal, price caps, service levels, data ownership and exit.", "Make implementation scope, team, acceptance and payment milestones clear.", "Negotiate before signing and watch for discounts that vanish at renewal."],
 "List the ten contract points in this lesson and note your position on each before you receive a draft contract.",
 "Why is an exit clause important in a software subscription?", ["It lets the vendor leave", "It ensures you can get your data back in a usable form if you leave", "It sets the price of training", "It is only for large companies"], 1,
 "Exit terms protect access to your data when the relationship ends."),
step("Choosing the implementation approach and partner", 7, """
<p>How the system is implemented matters as much as which system you choose. Settle the approach and the partner's role before signing.</p>
<h3>Implementation approaches</h3>
<table><thead><tr><th>Approach</th><th>How it works</th><th>Suits</th></tr></thead><tbody>
<tr><td>Big bang</td><td>All modules and sites go live at once</td><td>Smaller, simpler businesses with good preparation</td></tr>
<tr><td>Phased</td><td>Modules or sites go live in stages, such as finance first, then operations</td><td>More complex businesses or several sites</td></tr>
<tr><td>Pilot</td><td>One site or business unit first, then roll out</td><td>Multi-site businesses with similar operations</td></tr>
</tbody></table>
<h3>Methodology</h3>
<p>Many partners use a structured method: discovery and design, configuration in iterations, testing, training, data migration, go-live and support. Ask to see the plan, the deliverables of each phase and how decisions are documented. Look for a method that shows you working software early, rather than only documents.</p>
<h3>What a good partner brings</h3>
<ul><li>Experience in your industry and with businesses your size.</li>
<li>A named, stable team including a project manager and functional consultants.</li>
<li>Willingness to challenge requests for customization and recommend standard practice.</li>
<li>Clear communication about risks and changes.</li>
<li>Post-go-live support and ongoing improvement.</li></ul>
<h3>Your side of the bargain</h3>
<p>Partners configure software; your team owns the processes, decisions, data and adoption. Projects fail most often on the customer side: key users without time, slow decisions and poor data. Commit your people before you start.</p>
""", ["Choose big bang, phased or pilot based on size and complexity.", "Look for a structured method that shows working software early.", "A good partner challenges customization; your team owns decisions, data and adoption."],
 "Decide whether a big-bang, phased or pilot approach suits your business and write down why. List the key users who must be freed up for the project.",
 "What is a common reason ERP projects fail on the customer's side?", ["The software has too many features", "Key users lack time, decisions are slow and data is poor", "The partner is too experienced", "The project starts too early"], 1,
 "Customer commitment of people, decisions and data is critical."),
]

M4 = [
step("Project team and governance", 7, """
<p>A software implementation is a business change project, not an IT project. Its structure should reflect that.</p>
<h3>Key roles</h3>
<table><thead><tr><th>Role</th><th>Responsibility</th></tr></thead><tbody>
<tr><td>Executive sponsor</td><td>Owns the business case, makes final decisions, removes obstacles</td></tr>
<tr><td>Internal project manager</td><td>Coordinates your side: plan, people, decisions, issues</td></tr>
<tr><td>Key users (process owners)</td><td>Design processes for their area, test, train colleagues and champion adoption</td></tr>
<tr><td>Partner project manager and consultants</td><td>Configure, advise on best practice, manage their deliverables</td></tr>
<tr><td>IT or technical lead</td><td>Integrations, security, devices, data</td></tr>
</tbody></table>
<h3>Free up key users</h3>
<p>Key users are usually your most knowledgeable staff, which is exactly why they are busy. Plan backfill, temporary help or reduced responsibilities so they can spend real time on the project. Without them, the system is designed by people who don't do the work.</p>
<h3>Governance</h3>
<ul><li>Weekly project meetings with the partner: progress, issues, decisions.</li>
<li>A monthly steering meeting with the sponsor: budget, timeline, risks and major decisions.</li>
<li>A decision log and a change request process, so scope changes are deliberate and costed.</li>
<li>A risk and issue register with owners.</li></ul>
<h3>Resist customization creep</h3>
<p>Each request to make the new system work exactly like the old one adds cost and complexity. Ask "what business result does this deliver?" and prefer changing the process to changing the software, unless the requirement is truly what makes you different.</p>
""", ["Treat implementation as a business change project with a sponsor and key users.", "Free up key users with backfill or reduced duties.", "Govern with weekly meetings, a steering group, a decision log and change control."],
 "Name your executive sponsor, internal project manager and key users, and estimate how much of each key user's week the project will need.",
 "Who should design how each business area will work in the new system?", ["Only the software vendor", "Key users who know the work, supported by the partner", "The newest employee", "Nobody; use the defaults blindly"], 1,
 "Key users bring process knowledge; the partner advises on how the software supports it."),
step("Data migration", 7, """
<p>Moving data from old systems into the new one is often underestimated. Bad data in a new system undermines trust from day one.</p>
<h3>What to migrate</h3>
<ul><li><strong>Master data:</strong> customers, suppliers, products, prices, bills of materials, chart of accounts.</li>
<li><strong>Open transactions:</strong> open sales and purchase orders, open invoices, inventory balances.</li>
<li><strong>History:</strong> decide how much is needed. Often summary balances or a few years of history are enough, with older data kept accessible in an archive.</li></ul>
<h3>The migration cycle</h3>
<ol><li><strong>Extract</strong> data from old systems and spreadsheets.</li>
<li><strong>Cleanse:</strong> remove duplicates and inactive records, fix errors, standardize formats.</li>
<li><strong>Map</strong> old fields and codes to the new system's structure.</li>
<li><strong>Load</strong> into a test environment.</li>
<li><strong>Validate:</strong> check record counts, totals and samples with key users.</li></ol>
<p>Repeat the cycle in two or three trial runs before the final load at go-live.</p>
<h3>Start cleansing early</h3>
<p>Data cleansing is business work, not IT work: someone must decide which customers are inactive, which products are obsolete and which prices are correct. Start months before go-live. It is the best time to clean up years of accumulated clutter.</p>
<h3>Reconcile at go-live</h3>
<p>Plan a cut-over: when old systems stop taking transactions, how final balances are loaded and how inventory is counted. Reconcile opening balances, open orders and inventory against the old system and have finance sign off before trading starts in the new one.</p>
""", ["Migrate master data and open transactions; limit history to what you need.", "Run extract, cleanse, map, load and validate cycles several times.", "Start cleansing early and reconcile balances at cut-over."],
 "List your master data types and estimate how many records of each are inactive or duplicated. Assign an owner to clean each type.",
 "Who should decide which old customer and product records are inactive before migration?", ["The software vendor", "Business data owners in each area", "Nobody; migrate everything", "A random sample"], 1,
 "Cleansing requires business judgment from data owners."),
step("Testing, training and go-live", 8, """
<p>The weeks before go-live decide whether the first month is smooth or chaotic.</p>
<h3>Testing</h3>
<table><thead><tr><th>Test type</th><th>Purpose</th></tr></thead><tbody>
<tr><td>Unit or configuration testing</td><td>Each function works as configured</td></tr>
<tr><td>Integration testing</td><td>Data flows correctly between systems</td></tr>
<tr><td>End-to-end scenario testing</td><td>Complete processes work with realistic data: quote to cash, procure to pay</td></tr>
<tr><td>User acceptance testing</td><td>Key users confirm the system supports their work</td></tr>
<tr><td>Cut-over rehearsal</td><td>The go-live steps and data load work in the time available</td></tr>
</tbody></table>
<p>Test exceptions as well as the normal path: returns, credits, partial shipments, price overrides, month-end.</p>
<h3>Training</h3>
<ul><li>Train by role, using your processes and data, close to go-live.</li>
<li>Provide short reference guides and recorded walkthroughs for common tasks.</li>
<li>Have key users act as first-line support for their colleagues.</li></ul>
<h3>Go-live readiness</h3>
<p>Hold a go/no-go decision with the sponsor against clear criteria: critical tests passed, data validated, users trained, support in place, cut-over plan rehearsed. If key criteria aren't met, a short delay is usually cheaper than a failed go-live.</p>
<h3>Hypercare</h3>
<p>Plan intensive support for the first weeks: partner consultants available, daily issue meetings, quick fixes and extra staff for slower processing. Expect productivity to dip temporarily while people learn.</p>
""", ["Test configuration, integrations, end-to-end scenarios and exceptions, then rehearse cut-over.", "Train by role with your own processes and data, close to go-live.", "Use a go/no-go decision and plan intensive support after go-live."],
 "Draft your go/no-go criteria and a list of ten end-to-end test scenarios, including at least three exceptions.",
 "What should happen if key go-live criteria aren't met?", ["Go live anyway to keep the date", "Consider a short delay; it is usually cheaper than a failed go-live", "Cancel the project", "Skip training"], 1,
 "Going live unprepared risks disruption that costs far more than a short delay."),
step("After go-live, and your selection roadmap", 7, """
<p>Go-live is the start of getting value, not the end of the project.</p>
<h3>The first months after go-live</h3>
<ul><li><strong>Stabilize:</strong> resolve issues, fix data errors, refine reports.</li>
<li><strong>Measure:</strong> check results against the business case goals, such as close time, accuracy and order cycle time.</li>
<li><strong>Adopt:</strong> retire old spreadsheets and workarounds; check that people use the system as designed.</li>
<li><strong>Improve:</strong> plan a second phase for features deferred from the first, such as advanced planning, portals or automation.</li></ul>
<h3>A typical SME roadmap</h3>
<table><thead><tr><th>Phase</th><th>Typical duration</th><th>Key outputs</th></tr></thead><tbody>
<tr><td>Prepare</td><td>1–2 months</td><td>Process maps, pain points, business case, requirements</td></tr>
<tr><td>Select</td><td>2–3 months</td><td>Shortlist, RFP, scripted demos, scoring, TCO, references, contract</td></tr>
<tr><td>Implement</td><td>4–9 months, depending on scope</td><td>Design, configuration, data migration, testing, training, go-live</td></tr>
<tr><td>Stabilize and improve</td><td>3–6 months</td><td>Hypercare, adoption, measured benefits, phase-two plan</td></tr>
</tbody></table>
<p>Durations vary widely with scope, complexity and how much time your team can commit.</p>
<h3>Selection checklist</h3>
<ul><li>Processes mapped and pain points agreed.</li>
<li>Business case with measurable goals and full-cost budget.</li>
<li>Prioritized requirements with scenarios.</li>
<li>Shortlist of three or four, with partners evaluated.</li>
<li>Scripted demos with users and a pre-agreed scorecard.</li>
<li>Five-year TCO, references called, contract reviewed.</li>
<li>Key users committed and project governance in place.</li></ul>
<p>The Digital Automation for SMEs course helps place software selection within a wider digital plan, and Data and Dashboards for SMEs helps you get value from the data the new system collects.</p>
""", ["After go-live: stabilize, measure, adopt and improve.", "A typical roadmap runs prepare, select, implement, stabilize.", "Use the checklist to confirm each step before moving on."],
 "Put the four roadmap phases into a calendar for your business with realistic durations, and check your progress against the selection checklist.",
 "After go-live, how should success be judged?", ["By whether the system is switched on", "Against the measurable goals in the business case", "By the number of features used", "By the partner's opinion"], 1,
 "Measuring against business case goals shows whether the investment delivered."),
]

course = dict(
 id="choosing-erp-and-business-software",
 title="Choosing ERP and Business Software",
 tagline="Select the right ERP, CRM or warehouse system with clear requirements, scripted demos, total cost comparisons and a realistic implementation plan.",
 summary="A practical course for owners, managers and project leads in small and mid-sized businesses who are choosing major business software. You will learn to recognize when you have outgrown your systems, understand the main types of software, map processes, build a business case, write scenario-based requirements, shortlist vendors and partners, run scripted demonstrations, score options, compare total cost of ownership and negotiate contracts. It closes with implementation governance, data migration, testing, training, go-live and a selection roadmap.",
 audience=["Owners and general managers considering a new ERP or business system",
           "Finance, operations and IT leads running a software selection",
           "Key users who will help choose and implement a new system",
           "Advisers helping SMEs plan technology investments"],
 outcomes=["Recognize when systems are outgrown and understand ERP, CRM, WMS and MES",
           "Map processes and build a business case with measurable goals and full costs",
           "Write prioritized, scenario-based requirements and shortlist vendors and partners",
           "Run scripted demonstrations and score options with a weighted scorecard",
           "Compare five-year total cost of ownership and negotiate key contract terms",
           "Plan implementation governance, data migration, testing, training and go-live"],
 modules=[
  dict(title="Do You Need New Software?", summary="Signs you've outgrown your systems, types of business software, process mapping and the business case.", steps=M1),
  dict(title="Requirements and the Market", summary="Writing requirements, shortlisting vendors and partners, focused RFPs and scripted demonstrations.", steps=M2),
  dict(title="Decide and Contract", summary="Scoring and selection, total cost of ownership, contracts and negotiation, and the implementation approach and partner.", steps=M3),
  dict(title="Implement and Get Value", summary="Project team and governance, data migration, testing, training and go-live, and the roadmap after go-live.", steps=M4)],
 labs=[
  dict(id="erp-which-system", type="classify", title="Which system usually handles it?", after_step=2,
       intro="Match twelve business functions to the type of system that usually handles them in an SME: accounting or ERP, CRM, or a warehouse management system. Then check your answers.",
       config=dict(categories=["Accounting or ERP", "CRM", "Warehouse management (WMS)"], items=[
        dict(text="Posting supplier invoices and paying them", answer=0, why="Payables are core accounting and ERP functions."),
        dict(text="Producing the monthly income statement", answer=0, why="Financial statements come from the general ledger in accounting or ERP."),
        dict(text="Calculating material requirements from a production plan", answer=0, why="MRP is an ERP manufacturing function."),
        dict(text="Entering and confirming sales orders with pricing", answer=0, why="Sales order processing is a core ERP function (some CRMs pass orders to the ERP)."),
        dict(text="Tracking leads and sales opportunities by stage", answer=1, why="Pipeline management is the core job of a CRM."),
        dict(text="Logging calls, emails and meetings with customers", answer=1, why="Activity history lives in the CRM."),
        dict(text="Running email marketing campaigns to segments", answer=1, why="Marketing automation is usually part of or linked to CRM."),
        dict(text="Managing customer service cases", answer=1, why="Service case management is a common CRM function."),
        dict(text="Directing pickers to bins in the most efficient sequence", answer=2, why="Directed picking is a WMS function."),
        dict(text="Scanning items at receiving and put-away into bin locations", answer=2, why="Detailed location control and scanning are WMS strengths."),
        dict(text="Planning wave picking across many orders", answer=2, why="Wave planning is a warehouse management function."),
        dict(text="Generating cycle counts by bin location", answer=2, why="Location-level counting is a WMS function (basic ERPs offer simpler counting)."),
       ])),
  dict(id="erp-option-matrix", type="matrix", title="Comparing shortlisted options", after_step=8,
       intro="Place seven options from a fictional software selection on a grid of fit to requirements against total cost, to see which deserve the final round.",
       config=dict(x="Five-year total cost", y="Fit to must-have scenarios", x_low="Lower cost", x_high="Higher cost", y_low="Poor fit", y_high="Strong fit",
        quadrants=dict(top_left="Best value: final round", top_right="Strong but costly: negotiate", bottom_left="Cheap but risky", bottom_right="Avoid"),
        items=[dict(name="Mid-market ERP with strong local partner", x=3, y=5),
               dict(name="Industry-specific system", x=2, y=4),
               dict(name="Large enterprise ERP", x=5, y=4),
               dict(name="Upgraded accounting package plus add-ons", x=1, y=2),
               dict(name="Heavily customized option", x=5, y=2),
               dict(name="Suite missing two must-haves", x=2, y=2),
               dict(name="Best-of-breed ERP + WMS combination", x=4, y=4)])),
  dict(id="erp-tco-calculator", type="calc", title="Five-year total cost of ownership", after_step=10,
       intro="Enter users, subscription price, implementation fees, internal time and other annual costs to see one-time costs, recurring costs, year-1 cost and total cost of ownership.",
       config=dict(calc="tco", note="Ask each vendor for the same scope so totals are comparable. Include price increases at renewal if the contract allows them.")),
 ],
 figures=[
  dict(step=2, type="compare", title="Suite vs best of breed", caption="Toggle between the two approaches and compare their trade-offs.",
       config=dict(left=dict(title="ERP suite", points=["One vendor, one database", "Fewer integrations to build and maintain", "One source of truth for reporting", "Some modules may be less deep than specialists"]),
                   right=dict(title="Best of breed", points=["Specialist systems for demanding areas", "Deeper functions where you need them", "More integrations and vendors to manage", "Data may need reconciling between systems"]))),
  dict(step=5, type="flow", title="The selection process", caption="Click each step to see its main output.",
       config=dict(steps=[
        dict(label="Map processes", text="Current processes, pain points and future state."),
        dict(label="Requirements", text="Must, should and could, with scenarios."),
        dict(label="Shortlist", text="Three or four systems and partners, references checked."),
        dict(label="Scripted demos", text="Your scenarios and data, scored immediately."),
        dict(label="Decide", text="Weighted score, five-year TCO, contract and due diligence.")])),
  dict(step=10, type="bars", title="Example: five-year TCO by category", caption="Illustrative 25-user cloud ERP. The subscription is the largest item, but one-time and other costs add about 70% more.",
       config=dict(unit="CA$", items=[dict(label="Subscriptions (5 years)", value=165000, highlight=True), dict(label="Implementation partner", value=60000), dict(label="Other annual costs (5 years)", value=30000), dict(label="Internal staff time", value=25000)],
        note="Total about $280,000, or roughly $190 per user per month over five years.")),
  dict(step=13, type="stack", title="What makes an implementation succeed", caption="Click each layer, from the bottom up.",
       config=dict(top_label="A system people use", layers=[
        dict(label="Committed sponsor", text="Owns the business case and makes timely decisions."),
        dict(label="Key users with time", text="Design, test and champion their areas."),
        dict(label="Clean data", text="Master data cleansed and validated before go-live."),
        dict(label="Standard processes", text="Customize only what truly makes you different."),
        dict(label="Testing and training", text="End-to-end tests, role-based training, go/no-go decision.")])),
  dict(step=14, type="cycle", title="The data migration cycle", caption="Click each stage. Run the cycle two or three times before the final load.",
       config=dict(center="Trial runs", stages=[
        dict(label="Extract", text="Pull data from old systems and spreadsheets."),
        dict(label="Cleanse", text="Remove duplicates and inactive records; fix errors."),
        dict(label="Map", text="Match old fields and codes to the new structure."),
        dict(label="Load", text="Load into a test environment."),
        dict(label="Validate", text="Check counts, totals and samples with key users.")])),
  dict(step=16, type="timeline", title="A typical SME software roadmap", caption="Click each phase. Durations vary with scope and team time.",
       config=dict(phases=[
        dict(label="1–2 months", title="Prepare", items=["Process maps", "Business case", "Requirements"]),
        dict(label="2–3 months", title="Select", items=["Shortlist and RFP", "Scripted demos", "Scoring, TCO, contract"]),
        dict(label="4–9 months", title="Implement", items=["Design and configuration", "Data migration", "Testing, training, go-live"]),
        dict(label="3–6 months", title="Stabilize", items=["Hypercare", "Adoption", "Measured benefits", "Phase-two plan"])])),
 ],
 exam=[
  E("Which is a strong sign a business has outgrown its systems?", ["Orders are re-keyed into several systems and spreadsheets", "Staff use email", "Reports are reviewed monthly", "The business has a website"], 0, "Re-keying signals disconnected systems."),
  E("What does an ERP system mainly do?", ["Manage only marketing campaigns", "Run operations and finance on one shared database", "Replace email", "Host the website"], 1, "ERP integrates operations and finance."),
  E("What is a key trade-off of a best-of-breed approach?", ["No integrations needed", "Lower depth of function", "Deeper specialist functions but more integrations to manage", "Only one vendor"], 2, "Specialist systems bring depth and integration work."),
  E("Why map processes before talking to vendors?", ["Vendors require it by law", "To make demos shorter", "To avoid buying anything", "So your needs, not vendor features, lead the selection"], 3, "Process maps keep the selection focused on your needs."),
  E("For a standard process such as payables, what is usually best?", ["Adopt the software's standard way", "Customize to match the old system exactly", "Keep it in spreadsheets", "Outsource it"], 0, "Standard processes rarely justify customization."),
  E("Which goal is best for a business case?", ["Get better software", "Close the books in 5 working days instead of 12", "Be more modern", "Make staff happier"], 1, "Measurable goals can be checked after go-live."),
  E("What makes a requirement a 'must have'?", ["Any feature a vendor mentions", "Anything nice to have", "A system without it is unacceptable for the business", "It appears in every brochure"], 2, "Must-haves are truly essential and should be few."),
  E("Why use scenarios in requirements?", ["They are shorter than feature lists", "Vendors cannot answer them", "They avoid demonstrations", "They show how the system handles your real work"], 3, "Scenarios test real fit."),
  E("Why evaluate the implementation partner alongside the software?", ["Partner capability strongly affects success", "Partners set the software code", "Partners are only involved in sales", "It is a legal requirement"], 0, "The same software can succeed or fail depending on the partner."),
  E("A requirement is met only by customization. What does that imply?", ["No additional cost", "More build cost and upgrade risk", "The requirement is unimportant", "It will be free in the next version"], 1, "Customizations add cost and complicate upgrades."),
  E("What is the purpose of a scripted demonstration?", ["To see the vendor's best features", "To shorten the selection", "To make vendors show how they handle your scenarios and data", "To negotiate price"], 2, "Scripts reveal real fit."),
  E("When should scorecard weights be agreed?", ["After choosing a favourite", "After the contract", "Never", "Before the demonstrations"], 3, "Agreeing first avoids bias."),
  E("Why compare five-year total cost of ownership?", ["Implementation, integrations, training and internal time add to the subscription", "Subscriptions never change", "Year one is free", "Vendors require it"], 0, "TCO captures all costs."),
  E("25 users at $100 per user per month. What is the annual subscription?", ["$2,500", "$30,000", "$25,000", "$300,000"], 1, "25 × $100 × 12 = $30,000."),
  E("Which contract term protects access to your data if you leave?", ["Logo usage", "Training schedule", "Exit and data return terms", "Office hours"], 2, "Exit terms set how you get your data back."),
  E("Which implementation approach puts all modules live at once?", ["Pilot", "Phased", "Hybrid only", "Big bang"], 3, "Big bang goes live all at once."),
  E("What is a common customer-side cause of failed implementations?", ["Key users without time, slow decisions and poor data", "Too much training", "Too few features", "An experienced partner"], 0, "Customer commitment is critical."),
  E("Who should decide which records are inactive before data migration?", ["The vendor's sales rep", "Business data owners", "Nobody; migrate everything", "The newest employee"], 1, "Cleansing needs business judgment."),
  E("What should happen if go-live criteria aren't met?", ["Go live anyway", "Cancel the project", "Consider a short delay", "Skip testing"], 2, "A short delay is usually cheaper than a failed go-live."),
  E("After go-live, how should success be judged?", ["By the number of screens", "By the partner's opinion", "By whether the system is switched on", "Against the measurable goals in the business case"], 3, "Business case goals define success."),
 ],
)

if __name__ == "__main__":
    write(course, "erp-selection", __file__, balance=True)
