"""Source for content/courses/iso9001.json (run: python3 content/courses/src/iso9001.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import step, E, write

M1 = [
step("What ISO 9001 is and why SMEs adopt it", 6, """
<p><strong>ISO 9001</strong> is the international standard for quality management systems (QMS). It sets out requirements for how an organization plans, runs, checks and improves its work so it consistently meets customer and regulatory requirements and improves over time. It applies to any organization, of any size, in any sector, whether it makes products or provides services.</p>
<h3>Why SMEs adopt it</h3>
<ul><li><strong>Customer requirements:</strong> many manufacturers, distributors, government buyers and large companies require or prefer ISO 9001-certified suppliers.</li>
<li><strong>Consistency:</strong> clear processes reduce errors, rework and dependence on a few experienced people.</li>
<li><strong>Growth:</strong> a documented, working system makes it easier to train new staff, add shifts or sites, and win larger contracts.</li>
<li><strong>Improvement:</strong> audits, measures and corrective action create a habit of finding and fixing problems.</li></ul>
<h3>Certification versus conformity</h3>
<p>An organization can build its QMS to ISO 9001 without being certified. <strong>Certification</strong> means an independent certification body (also called a registrar) has audited the system and confirmed it meets the standard. Certification is what customers usually ask for.</p>
<h3>A useful system, not paperwork</h3>
<p>ISO 9001 has a reputation for binders of procedures nobody reads. The current standard is far more flexible: it asks for documented information where it is needed, and focuses on results, risk and the process approach. A good QMS describes how the business already works well, fixes the gaps and is used every day. Built that way, it pays for itself.</p>
<p>The current edition is ISO 9001:2015, amended in 2024 to ask organizations to consider whether climate change is relevant to their context. A revised edition is being developed; check which edition applies and any transition period when you plan certification. This course covers the concepts that carry across editions. It is an introduction, not a substitute for the standard itself, which you can buy from ISO or national standards bodies.</p>
""", ["ISO 9001 sets requirements for a quality management system for any organization.", "Certification is an independent audit against the standard, often required by customers.", "Build a useful system that reflects how you work, not paperwork."],
 "List the customers or tenders that have asked for ISO 9001, and the three quality problems that cost your business the most today.",
 "What does ISO 9001 certification mean?", ["The products are guaranteed defect-free", "An independent certification body has audited the QMS against the standard", "The company wrote its own quality manual", "The government inspected the factory"], 1,
 "Certification is an independent confirmation that the QMS meets ISO 9001."),
step("The seven quality management principles", 7, """
<p>ISO 9001 is built on seven quality management principles, described in the companion standard ISO 9000. They explain the thinking behind the requirements.</p>
<table><thead><tr><th>Principle</th><th>What it means in practice</th></tr></thead><tbody>
<tr><td>Customer focus</td><td>Understand and meet customer needs, and aim to exceed expectations</td></tr>
<tr><td>Leadership</td><td>Leaders set direction and create conditions for people to achieve quality objectives</td></tr>
<tr><td>Engagement of people</td><td>Competent, empowered people at all levels contribute to quality</td></tr>
<tr><td>Process approach</td><td>Manage activities as connected processes that produce consistent results</td></tr>
<tr><td>Improvement</td><td>Continual improvement is an ongoing objective</td></tr>
<tr><td>Evidence-based decision making</td><td>Decisions are based on data and analysis</td></tr>
<tr><td>Relationship management</td><td>Manage relationships with suppliers and partners for mutual benefit</td></tr>
</tbody></table>
<h3>Why they matter</h3>
<p>When a requirement seems unclear, the principles explain its purpose. For example, the requirement to monitor customer satisfaction follows from customer focus; the requirement for management review follows from leadership and evidence-based decisions.</p>
<h3>Familiar ideas</h3>
<p>The principles overlap closely with Lean, Six Sigma and operational excellence: customer focus, process thinking, data-driven decisions and continual improvement. A company already practising these has a head start on ISO 9001, and ISO 9001 gives those practices a structure that holds them in place.</p>
""", ["Seven principles underpin ISO 9001: customer focus, leadership, engagement, process approach, improvement, evidence-based decisions, relationship management.", "The principles explain the purpose behind requirements.", "They overlap closely with Lean and operational excellence."],
 "Rate your business from 1 to 5 on each of the seven principles and note one example of each in practice today.",
 "Which principle is behind the requirement to base decisions on data?", ["Relationship management", "Evidence-based decision making", "Engagement of people", "Customer focus"], 1,
 "Evidence-based decision making calls for data and analysis."),
step("How the standard is structured: PDCA and the process approach", 8, """
<p>ISO 9001 follows a common structure used by many ISO management system standards, which makes it easier to combine with others such as ISO 14001 (environment) and ISO 45001 (health and safety).</p>
<table><thead><tr><th>Clause</th><th>Topic</th><th>PDCA</th></tr></thead><tbody>
<tr><td>4</td><td>Context of the organization</td><td>Plan</td></tr>
<tr><td>5</td><td>Leadership</td><td>Plan</td></tr>
<tr><td>6</td><td>Planning: risks, opportunities, objectives</td><td>Plan</td></tr>
<tr><td>7</td><td>Support: resources, competence, communication, documents</td><td>Do</td></tr>
<tr><td>8</td><td>Operation: customer requirements, design, purchasing, production, release, nonconformity</td><td>Do</td></tr>
<tr><td>9</td><td>Performance evaluation: monitoring, internal audit, management review</td><td>Check</td></tr>
<tr><td>10</td><td>Improvement: nonconformity, corrective action, continual improvement</td><td>Act</td></tr>
</tbody></table>
<p>Clauses 1 to 3 cover scope, references and terms; the requirements start at clause 4.</p>
<h3>Plan-Do-Check-Act</h3>
<p>PDCA is a cycle for managing any process: plan what you will do and how, do it, check the results against the plan, and act to improve. ISO 9001 applies it to the whole system and to each process.</p>
<h3>The process approach</h3>
<p>Rather than managing departments in isolation, identify the processes that deliver value to customers, such as quote to order, design, purchasing, production, delivery and service, and how they connect. For each process, define inputs, outputs, owner, resources, controls, measures and risks. A simple process map showing the main processes and their interactions is a useful starting point for any QMS.</p>
<h3>Risk-based thinking</h3>
<p>Throughout the standard, organizations are asked to consider what could go wrong or right and to act in proportion. This replaces the old idea of a separate "preventive action" procedure. The lab after this lesson asks you to place everyday activities in the PDCA cycle.</p>
""", ["Clauses 4 to 10 contain the requirements and follow Plan-Do-Check-Act.", "Manage connected processes with owners, inputs, outputs, controls and measures.", "Apply risk-based thinking throughout, in proportion to the risk."],
 "Draw a one-page map of your main processes from customer enquiry to delivery and service, showing how they connect. Name an owner for each.",
 "Which clause of ISO 9001 covers internal audit and management review?", ["Clause 4", "Clause 7", "Clause 9", "Clause 10"], 2,
 "Clause 9, performance evaluation, covers monitoring, internal audit and management review."),
step("Context, interested parties and scope", 7, """
<p>Clause 4 asks the organization to understand its situation before designing its QMS.</p>
<h3>Context</h3>
<p>Identify the internal and external issues relevant to your purpose and ability to achieve quality results. Internal issues include your capabilities, people, culture and systems; external issues include markets, competition, regulation, technology, economic conditions and, since the 2024 amendment, whether climate change is relevant. A SWOT analysis is a common, practical way to record them.</p>
<h3>Interested parties</h3>
<p>List the interested parties relevant to the QMS, such as customers, regulators, suppliers, employees, owners and the community, and their relevant requirements. A simple table works well:</p>
<table><thead><tr><th>Interested party</th><th>Relevant requirements</th></tr></thead><tbody>
<tr><td>Customers</td><td>Product specifications, on-time delivery, certificates of conformity, responsiveness</td></tr>
<tr><td>Regulators</td><td>Product safety, labelling, pressure equipment or food safety rules as applicable</td></tr>
<tr><td>Employees</td><td>Clear instructions, training, safe workplace</td></tr>
<tr><td>Suppliers</td><td>Clear purchase orders and specifications, fair payment</td></tr>
</tbody></table>
<h3>Scope</h3>
<p>Define the boundaries of the QMS: which products, services, sites and activities it covers. The scope appears on the certificate, so word it carefully, for example "Design, fabrication and installation of stainless steel process piping systems at the Burnaby facility". If a requirement cannot apply to you, for example design and development for a company that only makes to customer drawings, state it and justify why in the scope.</p>
<h3>Keep it current</h3>
<p>Review context and interested parties at least yearly, usually in management review. They feed the risks and objectives in the next clauses.</p>
""", ["Record internal and external issues, including whether climate change is relevant.", "List interested parties and their relevant requirements.", "Define and justify the scope, which appears on the certificate."],
 "Write a draft scope statement for your QMS and a table of five interested parties with their relevant requirements.",
 "A company only manufactures to customer drawings and does no design. How should design requirements be handled?", ["Ignore them silently", "State in the scope that they don't apply and justify why", "Invent a design process", "Certification is impossible"], 1,
 "Requirements that cannot apply must be identified with justification."),
]

M2 = [
step("Leadership, quality policy and objectives", 7, """
<p>ISO 9001 places clear responsibility on top management. Quality cannot be delegated entirely to a quality manager.</p>
<h3>What top management must do</h3>
<ul><li>Take accountability for the effectiveness of the QMS.</li>
<li>Set a quality policy and quality objectives that fit the business strategy.</li>
<li>Integrate QMS requirements into business processes rather than running them in parallel.</li>
<li>Provide resources, communicate the importance of quality and support people.</li>
<li>Promote the process approach, risk-based thinking, customer focus and improvement.</li>
<li>Assign roles, responsibilities and authorities.</li></ul>
<h3>The quality policy</h3>
<p>A short statement of the organization's commitment to quality: meeting requirements, customer focus and continual improvement, in words that fit the business. It should be communicated, understood and available. Avoid generic wording that could belong to any company; staff should recognize their own business in it.</p>
<h3>Quality objectives</h3>
<p>Objectives turn the policy into measurable targets. Good objectives are specific, measurable, owned and time-bound, with a plan for achieving them:</p>
<table><thead><tr><th>Objective</th><th>Measure</th><th>Target</th><th>Owner</th></tr></thead><tbody>
<tr><td>Improve on-time delivery</td><td>Order lines delivered by promised date</td><td>95% by year-end</td><td>Operations manager</td></tr>
<tr><td>Reduce customer complaints</td><td>Complaints per 1,000 orders</td><td>Below 3 by Q4</td><td>Quality lead</td></tr>
<tr><td>Reduce internal scrap</td><td>Scrap cost as % of material cost</td><td>Below 2%</td><td>Production supervisor</td></tr>
</tbody></table>
<p>Review progress at management review and use the same measures in regular management meetings, so quality objectives are part of running the business, not a separate exercise.</p>
""", ["Top management is accountable for the QMS and must integrate it into the business.", "Write a short, specific quality policy staff recognize.", "Set measurable, owned quality objectives with plans and review them regularly."],
 "Draft a quality policy of no more than five sentences and three measurable quality objectives with owners and targets.",
 "Who is accountable for the effectiveness of the QMS under ISO 9001?", ["Only the quality manager", "Top management", "The certification body", "Each customer"], 1,
 "ISO 9001 assigns accountability for the QMS to top management."),
step("Risks and opportunities", 7, """
<p>Clause 6.1 asks the organization to determine the risks and opportunities that could affect its ability to deliver conforming products and services and to satisfy customers, and to plan actions in proportion.</p>
<h3>A practical approach</h3>
<ol><li>Start from context and interested parties (clause 4) and your process map.</li>
<li>For each main process, ask what could go wrong (risks) and what could be done better (opportunities).</li>
<li>Rate each risk for likelihood and impact on a simple scale, such as 1 to 5.</li>
<li>Decide actions for the higher risks: prevent, reduce, transfer, monitor or accept.</li>
<li>Assign owners and dates, and check that actions worked.</li></ol>
<h3>Examples</h3>
<table><thead><tr><th>Process</th><th>Risk or opportunity</th><th>Action</th></tr></thead><tbody>
<tr><td>Purchasing</td><td>Single supplier for a critical component</td><td>Qualify a second source</td></tr>
<tr><td>Production</td><td>Only one person can set up the key machine</td><td>Cross-train two operators; write setup standard work</td></tr>
<tr><td>Quote to order</td><td>Customer specifications missed at order entry</td><td>Contract review checklist</td></tr>
<tr><td>Sales</td><td>Opportunity: certification opens a new market segment</td><td>Target three prospects in that segment</td></tr>
</tbody></table>
<h3>Keep it proportionate</h3>
<p>ISO 9001 does not require a formal risk management method or a risk register, though many SMEs find a simple register the easiest way to show their thinking. Focus on risks that matter to quality and customers; a long list of trivial risks adds paperwork without value. The lab after this lesson asks you to place risks on a likelihood and impact grid.</p>
""", ["Identify risks and opportunities by process, starting from context.", "Rate likelihood and impact and act in proportion.", "A simple register is enough; focus on risks that matter to quality and customers."],
 "For your three main processes, list two risks and one opportunity each, rate the risks and choose actions for the highest two.",
 "Does ISO 9001 require a formal risk management method?", ["Yes, a specific certified method", "No; it requires addressing risks and opportunities in proportion, and a simple register is often enough", "Only for large companies", "Only for medical devices"], 1,
 "ISO 9001 asks for proportionate risk-based thinking without prescribing a method."),
step("Support: resources, competence, awareness and communication", 7, """
<p>Clause 7 covers what people and processes need to work well.</p>
<h3>Resources</h3>
<ul><li><strong>People and infrastructure:</strong> enough staff, suitable buildings, equipment, IT and transport.</li>
<li><strong>Work environment:</strong> conditions needed for quality, such as cleanliness, temperature or lighting where they matter.</li>
<li><strong>Monitoring and measuring resources:</strong> gauges and instruments fit for purpose and, where measurement traceability is required, calibrated against recognized standards, identified with their status and protected from damage.</li>
<li><strong>Organizational knowledge:</strong> knowledge needed to run processes, captured so it is not lost when people leave.</li></ul>
<h3>Competence</h3>
<p>Determine the competence needed for each role that affects quality, ensure people are competent through education, training or experience, act to close gaps and keep evidence. A simple training matrix showing roles, required skills and who is qualified is a common and practical tool.</p>
<h3>Awareness</h3>
<p>People should know the quality policy, the objectives relevant to them, how their work contributes, and the consequences of not following requirements. A quick test: ask an operator what quality means in their job and what to do if something goes wrong.</p>
<h3>Communication</h3>
<p>Decide what to communicate about the QMS, when, with whom and how: team huddles, notice boards, toolbox talks, newsletters, customer and supplier communication.</p>
""", ["Provide people, infrastructure, environment and calibrated measuring equipment.", "Define competence by role, close gaps and keep evidence, for example in a training matrix.", "Make sure people know the policy, their objectives and their contribution."],
 "Build a simple training matrix for one department: roles across the top, key skills down the side, and who is qualified for each.",
 "What is a practical way to show competence for roles affecting quality?", ["A training matrix showing roles, required skills and who is qualified", "A list of employees' birthdays", "Asking the certification body", "A single annual memo"], 0,
 "A training matrix makes required skills and qualified people visible."),
step("Documented information: keep it lean", 7, """
<p>Clause 7.5 covers <strong>documented information</strong>: the documents you maintain to describe how things are done, and the records you retain as evidence of what was done.</p>
<h3>What the standard requires</h3>
<p>ISO 9001 explicitly requires some documented information, including:</p>
<ul><li>The scope of the QMS.</li>
<li>The quality policy and quality objectives.</li>
<li>Records such as evidence of competence, calibration, design and development where applicable, supplier evaluation, product release, nonconformities and corrective actions, internal audit results and management review results.</li></ul>
<p>Beyond these, the organization decides what is needed for effective processes. A quality manual is no longer mandatory, though some organizations keep a short one as an overview.</p>
<h3>Decide what to document</h3>
<p>Document a process when its absence could cause errors, when tasks are infrequent or complex, when several people do it, or when customers or regulations require it. Keep documents short, visual and at the point of use: flowcharts, checklists, photos and short work instructions beat long narrative procedures.</p>
<h3>Control</h3>
<ul><li>Documents are reviewed and approved before use and when changed.</li>
<li>Current versions are available where needed; obsolete versions are removed or marked.</li>
<li>Records are legible, identifiable, protected and kept for a defined period.</li></ul>
<p>Cloud document systems with version control, approval workflows and access rights make this much easier than paper. Many SMEs run their entire QMS in shared drives or simple QMS software.</p>
""", ["Some documented information is required; the rest depends on what processes need.", "Prefer short, visual documents at the point of use.", "Control approval, versions, availability and record retention."],
 "List the documents your business uses to run its main processes. Mark any that are outdated, duplicated or never used, and any process that needs one but has none.",
 "Is a quality manual mandatory under ISO 9001:2015?", ["Yes, always", "No; the organization decides what documented information is needed beyond the specific requirements", "Only for service companies", "Only for the first certification"], 1,
 "The quality manual is optional; required documented information is specified elsewhere."),
]

M3 = [
step("Customer requirements and operational planning", 7, """
<p>Clause 8 covers operations: how products and services are planned, made and delivered. It starts with understanding what the customer needs.</p>
<h3>Operational planning</h3>
<p>For each product or service, plan the requirements, the processes, acceptance criteria, resources and records needed, and control planned changes. For many SMEs this means a clear workflow from order to delivery, with checkpoints where quality is confirmed.</p>
<h3>Customer communication</h3>
<p>Provide information about products and services, handle enquiries, orders and changes, obtain customer feedback including complaints, handle customer property and set contingency actions where relevant.</p>
<h3>Review before you commit</h3>
<p>Before accepting an order, review that you can meet its requirements: stated requirements (specifications, quantities, delivery dates), requirements the customer didn't state but are necessary, legal and regulatory requirements, and your own requirements. Resolve differences before accepting. Keep a record of the review and of any changes.</p>
<p>A simple order review checklist prevents many problems:</p>
<ul><li>Specification and drawing revision confirmed?</li>
<li>Materials, certifications and testing requirements understood?</li>
<li>Delivery date feasible with current capacity?</li>
<li>Special packaging, labelling or documentation?</li>
<li>Price and terms agreed?</li></ul>
<h3>Changes</h3>
<p>When a customer changes an order, update all affected documents and tell everyone involved. Unclear or uncommunicated changes are a common cause of nonconformities.</p>
""", ["Plan operations with requirements, processes, acceptance criteria and records.", "Review orders before accepting them and resolve differences.", "Control changes and tell everyone affected."],
 "Draft a one-page order review checklist for your business and test it on your next five orders.",
 "When should an organization review its ability to meet a customer's requirements?", ["After delivery", "Before committing to supply", "Only after a complaint", "Once a year"], 1,
 "Requirements must be reviewed before accepting the order."),
step("Design and development, and external providers", 7, """
<h3>Design and development (clause 8.3)</h3>
<p>If you design products or services, the standard asks for a controlled design process:</p>
<ul><li><strong>Planning:</strong> stages, responsibilities, reviews, verification and validation.</li>
<li><strong>Inputs:</strong> functional and performance requirements, standards, regulations, lessons from previous designs.</li>
<li><strong>Controls:</strong> reviews at key stages, verification that outputs meet inputs, validation that the result works for its intended use.</li>
<li><strong>Outputs:</strong> drawings, specifications, instructions and acceptance criteria.</li>
<li><strong>Changes:</strong> reviewed, controlled and recorded.</li></ul>
<p>Companies that build only to customer designs can usually exclude this clause, with justification.</p>
<h3>Control of externally provided processes, products and services (clause 8.4)</h3>
<p>Suppliers and subcontractors affect your quality directly. The standard asks you to:</p>
<ol><li>Set criteria to evaluate, select, monitor and re-evaluate external providers, based on their ability to supply to requirements.</li>
<li>Decide the controls needed, such as incoming inspection, certificates of conformity or audits, in proportion to the risk.</li>
<li>Communicate requirements clearly on purchase orders: specifications, quantities, approvals, competence and verification activities.</li>
<li>Keep records of evaluations.</li></ol>
<h3>A simple supplier programme</h3>
<table><thead><tr><th>Step</th><th>Example</th></tr></thead><tbody>
<tr><td>Approved supplier list</td><td>Critical suppliers approved by questionnaire, sample or audit</td></tr>
<tr><td>Performance monitoring</td><td>On-time delivery and rejection rate reviewed quarterly</td></tr>
<tr><td>Feedback</td><td>Share results; raise corrective action requests for repeated problems</td></tr>
<tr><td>Re-evaluation</td><td>Yearly review of critical suppliers</td></tr>
</tbody></table>
""", ["If you design, control planning, inputs, reviews, verification, validation and changes.", "Evaluate, select and monitor suppliers in proportion to their impact on quality.", "Put clear requirements on purchase orders and keep evaluation records."],
 "List your ten most important suppliers, the criteria you would use to approve them and how you will monitor their performance.",
 "How should controls on suppliers be set under ISO 9001?", ["The same heavy controls for every supplier", "In proportion to the risk the supplier poses to quality", "Only for overseas suppliers", "Not at all; suppliers are responsible"], 1,
 "Controls should reflect each provider's effect on conformity."),
step("Production, traceability and release", 7, """
<p>Clause 8.5 and 8.6 cover how products are made or services delivered under controlled conditions, and how they are released.</p>
<h3>Controlled conditions</h3>
<ul><li>Documented information describing the product and the activities, such as drawings, specifications and work instructions.</li>
<li>Suitable equipment and monitoring and measuring resources.</li>
<li>Monitoring and measurement at appropriate stages.</li>
<li>Competent people.</li>
<li>Validation of processes whose results can't be fully verified afterwards, such as welding, heat treatment or sterilization.</li>
<li>Actions to prevent human error, such as checklists and mistake-proofing.</li></ul>
<h3>Identification and traceability</h3>
<p>Identify outputs and their inspection status throughout the process, for example with labels, tags or system status. Where traceability is required by customers or regulations, control and record the unique identification of outputs, such as lot or serial numbers, so you can trace materials and processes and recall if needed.</p>
<h3>Customer property and preservation</h3>
<p>Take care of property belonging to customers or suppliers, such as customer-supplied materials, tooling or data. Preserve products through handling, storage, packaging and delivery.</p>
<h3>Release</h3>
<p>Products and services are released only when planned checks show requirements are met, unless a relevant authority or the customer approves otherwise. Keep records showing conformity and who authorized release.</p>
""", ["Produce under controlled conditions with instructions, suitable equipment, competent people and checks.", "Identify status and maintain traceability where required.", "Release only after planned checks, with records of conformity and authorization."],
 "Walk one product or service through your process and note where its status is identified, what checks are done and who authorizes release.",
 "What must happen before a product is released to the customer?", ["It must be photographed", "Planned checks must confirm requirements are met, with records of who authorized release", "The customer must visit", "Nothing; release is automatic"], 1,
 "Release requires evidence of conformity and authorization."),
step("Nonconformities and corrective action", 8, """
<p>Problems happen. What matters is controlling them and stopping them from recurring.</p>
<h3>Control of nonconforming outputs (clause 8.7)</h3>
<p>When a product or service doesn't meet requirements, identify and control it so it isn't used or delivered by mistake. Options include correction (rework or repair), segregation, return to supplier, informing the customer, obtaining a concession or scrapping. Record the nonconformity, the action taken and who decided.</p>
<h3>Corrective action (clause 10.2)</h3>
<p>For significant or recurring nonconformities, including customer complaints and audit findings:</p>
<ol><li><strong>React:</strong> control and correct the immediate problem and deal with consequences.</li>
<li><strong>Find the root cause:</strong> use tools such as 5 Whys or a fishbone diagram. Check whether similar problems exist or could occur elsewhere.</li>
<li><strong>Act on the cause:</strong> implement actions that remove the root cause, not just the symptom.</li>
<li><strong>Verify effectiveness:</strong> check later that the problem hasn't recurred.</li>
<li><strong>Update the system:</strong> change risks, documents, training or processes as needed.</li></ol>
<h3>Correction versus corrective action</h3>
<table><thead><tr><th></th><th>Correction</th><th>Corrective action</th></tr></thead><tbody>
<tr><td>Purpose</td><td>Fix this instance</td><td>Prevent recurrence</td></tr>
<tr><td>Example</td><td>Rework the mislabelled cartons</td><td>Add a label check at packing and fix the template that caused the error</td></tr>
</tbody></table>
<p>"Retrain the operator" is rarely a sufficient corrective action on its own. Ask what in the process made the error possible. The Lean Six Sigma Foundations course covers root cause analysis in depth.</p>
""", ["Identify and control nonconforming outputs so they aren't used by mistake.", "Corrective action finds and removes the root cause, then verifies effectiveness.", "Correction fixes this instance; corrective action prevents recurrence."],
 "Take one recent customer complaint and work through the five corrective action steps. Write down how you will verify the action worked.",
 "Which is a corrective action rather than a correction?", ["Reworking the defective parts", "Fixing the label template that caused wrong labels and adding a check at packing", "Shipping the parts anyway", "Apologizing to the customer"], 1,
 "Corrective action removes the cause to prevent recurrence."),
]

M4 = [
step("Monitoring, measurement and customer satisfaction", 7, """
<p>Clause 9.1 asks what you need to monitor and measure, how, when, and when results are analyzed and evaluated.</p>
<h3>Typical QMS measures</h3>
<table><thead><tr><th>Area</th><th>Measures</th></tr></thead><tbody>
<tr><td>Customers</td><td>On-time delivery, complaints, returns, satisfaction ratings</td></tr>
<tr><td>Products and processes</td><td>First-pass yield, scrap, rework, process capability</td></tr>
<tr><td>Suppliers</td><td>On-time delivery, rejection rate</td></tr>
<tr><td>QMS</td><td>Objectives progress, corrective actions open and overdue, audit findings</td></tr>
</tbody></table>
<h3>Customer satisfaction</h3>
<p>Monitor customers' perception of how well their needs and expectations are met. Methods range from simple to detailed: complaint and compliment trends, short surveys after delivery, periodic customer interviews, warranty claims, repeat orders and lost-customer reviews. Choose methods that suit your customers and act on what you learn.</p>
<h3>Analysis and evaluation</h3>
<p>Data is only useful if it is analyzed. Review trends, compare with objectives and targets, look for patterns using tools such as Pareto charts, and use results to decide where to improve. Keep analysis results as input to management review.</p>
<h3>Use the same data to run the business</h3>
<p>The best QMS measures are the ones managers already use. If quality measures sit in a separate report reviewed only before audits, the QMS is not integrated. Put the key quality measures on the management dashboard.</p>
""", ["Decide what to measure, how, when and when to analyze.", "Monitor customer satisfaction with methods that suit your customers.", "Analyze trends and put quality measures on the management dashboard."],
 "List the five quality measures that matter most to your customers and check whether they appear on your management dashboard.",
 "What is the main point of analyzing quality data?", ["To fill the file before an audit", "To find trends and decide where to improve", "To satisfy the certification body only", "To replace customer feedback"], 1,
 "Analysis turns data into improvement decisions."),
step("Internal audit and management review", 8, """
<h3>Internal audit (clause 9.2)</h3>
<p>Internal audits check whether the QMS conforms to your own requirements and ISO 9001, and whether it is effectively implemented and maintained.</p>
<ul><li>Plan an audit programme covering all processes and clauses, usually over a year, with more frequent audits of important or problem areas.</li>
<li>Define the criteria and scope of each audit.</li>
<li>Use auditors who are objective and impartial: they should not audit their own work.</li>
<li>Audit by following processes: talk to people, observe the work and sample records.</li>
<li>Report findings to the relevant managers and track corrections and corrective actions.</li></ul>
<p>Small companies can train two or three staff as internal auditors who audit each other's areas, or use an outside auditor for some audits.</p>
<h3>Management review (clause 9.3)</h3>
<p>Top management reviews the QMS at planned intervals, at least once a year and often quarterly. Inputs include:</p>
<ul><li>Status of actions from previous reviews.</li>
<li>Changes in context and interested parties.</li>
<li>Performance: customer satisfaction, objectives, process performance, nonconformities and corrective actions, monitoring results, audit results, supplier performance.</li>
<li>Adequacy of resources.</li>
<li>Effectiveness of actions on risks and opportunities.</li>
<li>Opportunities for improvement.</li></ul>
<p>Outputs are decisions and actions on improvement, changes to the QMS and resource needs, recorded with owners. Many SMEs combine management review with a regular leadership or business review meeting, using a standing agenda, which keeps it practical rather than a once-a-year formality.</p>
""", ["Plan internal audits of all processes with impartial auditors and follow up findings.", "Hold management reviews at planned intervals with the required inputs.", "Record decisions and actions; combine review with regular leadership meetings."],
 "Draft a 12-month internal audit plan covering your main processes, and a standing management review agenda with the inputs listed.",
 "Why should internal auditors not audit their own work?", ["It takes too long", "To keep audits objective and impartial", "It is forbidden to audit any colleague", "Certification bodies do it instead"], 1,
 "Impartiality ensures audit findings are credible."),
step("Continual improvement", 7, """
<p>Clause 10 asks the organization to determine and select opportunities for improvement and to continually improve the suitability, adequacy and effectiveness of the QMS.</p>
<h3>Where improvement ideas come from</h3>
<ul><li>Analysis of data: trends in complaints, scrap, delivery.</li>
<li>Internal audits and management reviews.</li>
<li>Customer feedback and complaints.</li>
<li>Risks and opportunities.</li>
<li>Staff suggestions.</li>
<li>Supplier feedback and benchmarking.</li></ul>
<h3>Improvement tools</h3>
<p>ISO 9001 doesn't prescribe methods. Common choices:</p>
<table><thead><tr><th>Approach</th><th>Fits</th></tr></thead><tbody>
<tr><td>PDCA cycles</td><td>Small, everyday improvements</td></tr>
<tr><td>Kaizen events</td><td>Focused improvement of one area in a few days</td></tr>
<tr><td>Lean tools: 5S, standard work, flow</td><td>Waste and lead time</td></tr>
<tr><td>Six Sigma DMAIC</td><td>Complex, recurring defects with unclear causes</td></tr>
</tbody></table>
<h3>Keep an improvement list</h3>
<p>Track improvement projects with owners, status and results. Review the list at management review. Celebrate successes and share them, so staff see that raising problems leads to change.</p>
<h3>ISO 9001 and Lean Six Sigma together</h3>
<p>ISO 9001 provides the system: defined processes, measures, audits and reviews. Lean and Six Sigma provide the methods to improve. Together they create a cycle where the QMS reveals problems and improvement methods solve them, with standards and controls holding the gains.</p>
""", ["Draw improvement ideas from data, audits, customers, risks and staff.", "Use PDCA, kaizen, Lean and Six Sigma as fits the problem.", "Track improvements, review them and share successes."],
 "Start an improvement list with five ideas from recent complaints, scrap data or staff suggestions. Assign owners and target dates.",
 "How do ISO 9001 and Lean Six Sigma relate?", ["They conflict and can't be used together", "ISO 9001 provides the management system; Lean Six Sigma provides improvement methods", "Lean Six Sigma replaces ISO 9001", "ISO 9001 forbids improvement projects"], 1,
 "The QMS reveals problems; improvement methods solve them."),
step("Getting certified", 8, """
<p>Certification typically takes 6 to 12 months for an SME starting with basic processes in place, depending on size, complexity and how much staff time is available.</p>
<h3>A typical path</h3>
<table><thead><tr><th>Phase</th><th>Activities</th></tr></thead><tbody>
<tr><td>Commit and plan</td><td>Leadership commitment, project lead, scope, budget, timeline</td></tr>
<tr><td>Gap assessment</td><td>Compare current practice with ISO 9001 requirements, clause by clause</td></tr>
<tr><td>Build the QMS</td><td>Process map, policy, objectives, risks, documents, records, training matrix, supplier controls</td></tr>
<tr><td>Run it</td><td>Use the system for at least a few months to generate records: corrective actions, measures, supplier reviews</td></tr>
<tr><td>Internal audit and management review</td><td>Complete a full internal audit cycle and at least one management review</td></tr>
<tr><td>Certification audit</td><td>Stage 1 (documentation and readiness) and Stage 2 (implementation and effectiveness)</td></tr>
</tbody></table>
<h3>Choosing a certification body</h3>
<p>Choose an <strong>accredited</strong> certification body. In Canada, the Standards Council of Canada accredits certification bodies; others are accredited by members of the International Accreditation Forum. Customers generally expect accredited certification. Compare quotes on audit days, auditor experience in your industry, scheduling and travel costs.</p>
<h3>After certification</h3>
<p>Certificates are typically valid for three years, with surveillance audits at least yearly and a recertification audit before the certificate expires. The system must keep working between audits. Organizations that only prepare just before audits struggle; those that use the QMS to run the business find audits routine.</p>
<h3>Costs</h3>
<p>Costs include the certification body's audit fees, any consultant support, staff time, training, and possibly QMS software and calibration. Staff time is often the largest cost. Some government programmes support certification projects; check the Funding page and confirm eligibility with each programme.</p>
<p>Use the self-assessment lab after this lesson to see your readiness clause by clause.</p>
""", ["Certification usually takes 6 to 12 months: plan, gap assess, build, run, audit, certify.", "Choose an accredited certification body; in Canada, SCC accredits certification bodies.", "Certificates last three years with yearly surveillance; keep the system working between audits."],
 "Complete the readiness self-assessment after this lesson and draft a certification timeline with phases, owners and target dates.",
 "What is checked in a Stage 2 certification audit?", ["Only the quality manual", "Implementation and effectiveness of the QMS in practice", "The company's financial statements", "Employee holiday schedules"], 1,
 "Stage 2 confirms the system is implemented and effective."),
]

course = dict(
 id="iso-9001-quality-management-basics",
 title="ISO 9001 and Quality Management Basics",
 tagline="Build a practical quality management system that customers trust, auditors accept and your team actually uses.",
 summary="An introduction to ISO 9001 and quality management for owners, managers and quality leads in small and mid-sized businesses. You will learn the seven quality principles, the structure of the standard, PDCA, the process approach and risk-based thinking, then work through context and scope, leadership and objectives, risks, resources and competence, documented information, operations, suppliers, production and release, nonconformity and corrective action, monitoring, internal audit, management review, continual improvement and the path to certification. It is an introduction, not a substitute for the standard itself.",
 audience=["Owners and managers whose customers ask for ISO 9001",
           "Quality leads and coordinators building or maintaining a QMS",
           "Supervisors and staff who will take part in audits and corrective actions",
           "Companies wanting a lean, practical QMS rather than paperwork"],
 outcomes=["Explain ISO 9001, certification and the seven quality management principles",
           "Use the clause structure, PDCA, the process approach and risk-based thinking",
           "Define context, scope, quality policy, objectives, risks and documented information",
           "Control customer requirements, design, suppliers, production, release and nonconformity",
           "Plan internal audits, management reviews and continual improvement",
           "Plan a realistic path to certification and choose an accredited certification body"],
 modules=[
  dict(title="Foundations", summary="What ISO 9001 is, the seven quality principles, the structure of the standard and context, interested parties and scope.", steps=M1),
  dict(title="Leadership, Planning and Support", summary="Leadership, quality policy and objectives, risks and opportunities, resources and competence, and documented information.", steps=M2),
  dict(title="Operation", summary="Customer requirements, design and suppliers, production, traceability and release, and nonconformity and corrective action.", steps=M3),
  dict(title="Evaluate, Improve and Certify", summary="Monitoring and customer satisfaction, internal audit and management review, continual improvement and getting certified.", steps=M4)],
 labs=[
  dict(id="iso-pdca-sort", type="classify", title="Where does it fit in Plan-Do-Check-Act?", after_step=3,
       intro="Place twelve everyday quality activities in the PDCA cycle, then check your answers.",
       config=dict(categories=["Plan", "Do", "Check", "Act"], items=[
        dict(text="Setting a quality objective to reach 95% on-time delivery", answer=0, why="Setting objectives is planning (clause 6)."),
        dict(text="Identifying the risk of a single supplier for a critical part", answer=0, why="Determining risks and opportunities is planning (clause 6.1)."),
        dict(text="Defining the scope of the QMS", answer=0, why="Scope is set in context and planning (clause 4)."),
        dict(text="Training a new operator on the work instruction", answer=1, why="Competence and training support doing the work (clause 7)."),
        dict(text="Reviewing a customer order before accepting it", answer=1, why="Order review is part of operation (clause 8.2)."),
        dict(text="Making the product according to the drawing", answer=1, why="Production under controlled conditions is doing (clause 8.5)."),
        dict(text="Running an internal audit of purchasing", answer=2, why="Internal audit is performance evaluation (clause 9.2)."),
        dict(text="Analyzing complaint trends for the last quarter", answer=2, why="Analysis and evaluation is checking (clause 9.1)."),
        dict(text="Holding the quarterly management review", answer=2, why="Management review evaluates the QMS (clause 9.3)."),
        dict(text="Fixing the root cause of repeated labelling errors", answer=3, why="Corrective action is improvement (clause 10.2)."),
        dict(text="Updating a work instruction after a corrective action", answer=3, why="Changing the system to prevent recurrence is acting on results."),
        dict(text="Launching an improvement project to cut scrap", answer=3, why="Continual improvement is acting (clause 10.3)."),
       ])),
  dict(id="iso-risk-matrix", type="matrix", title="Rating quality risks", after_step=6,
       intro="Place seven quality risks from a small manufacturer on a likelihood and impact grid to decide which need action first.",
       config=dict(x="Likelihood", y="Impact on customers", x_low="Rare", x_high="Likely", y_low="Minor", y_high="Severe",
        quadrants=dict(top_left="Plan contingency", top_right="Act now", bottom_left="Accept and monitor", bottom_right="Reduce when practical"),
        items=[dict(name="Wrong drawing revision used in production", x=3, y=5),
               dict(name="Only one person can set up the key machine", x=4, y=4),
               dict(name="Single supplier for a critical component", x=2, y=5),
               dict(name="Gauge out of calibration", x=3, y=4),
               dict(name="Minor cosmetic marks on internal parts", x=4, y=1),
               dict(name="Late delivery of office supplies", x=4, y=1),
               dict(name="Customer specification missed at order entry", x=3, y=4)])),
  dict(id="iso-readiness-check", type="assessment", title="ISO 9001 readiness self-assessment", after_step=16,
       intro="Rate your organization against eight areas of ISO 9001. The radar chart shows strengths and gaps, with a next step for each. Retake it before your certification audit.",
       config=dict(scale=["Not started", "Ad hoc", "Defined", "Managed", "Optimized"], dimensions=[
        dict(name="Context and scope", question="Have you recorded context, interested parties and a justified QMS scope?", low="Run a SWOT, list interested parties and draft the scope.", high="Review context and interested parties at each management review."),
        dict(name="Leadership and objectives", question="Is there a specific quality policy and measurable, owned quality objectives?", low="Draft a short policy and three measurable objectives with owners.", high="Track objectives on the management dashboard and review them regularly."),
        dict(name="Risks and opportunities", question="Have risks and opportunities been identified by process with proportionate actions?", low="List risks for your main processes and act on the top two.", high="Review risk actions for effectiveness at management review."),
        dict(name="Competence and documents", question="Do you have a training matrix and controlled, current documents at the point of use?", low="Build a training matrix and remove outdated documents.", high="Use version-controlled, visual documents and review them on schedule."),
        dict(name="Customer requirements and suppliers", question="Do you review orders before accepting them and evaluate and monitor critical suppliers?", low="Introduce an order review checklist and an approved supplier list.", high="Share supplier performance results and raise corrective action requests."),
        dict(name="Production and release", question="Do you produce under controlled conditions with traceability and authorized release?", low="Map checks and release authority for one product.", high="Validate special processes and mistake-proof critical steps."),
        dict(name="Nonconformity and corrective action", question="Are nonconformities controlled and corrective actions root-caused and verified?", low="Use a simple corrective action form with root cause and verification steps.", high="Trend nonconformities and check corrective actions for effectiveness."),
        dict(name="Audit, review and improvement", question="Do you run internal audits, management reviews and an improvement list?", low="Draft a 12-month audit plan and a management review agenda.", high="Integrate management review into regular leadership meetings."),
       ])),
 ],
 figures=[
  dict(step=1, type="compare", title="Paperwork QMS vs useful QMS", caption="Toggle between the two and see why one helps the business and the other only passes audits.",
       config=dict(left=dict(title="Paperwork QMS", points=["Thick manual written for the auditor", "Procedures nobody reads", "Records created just before audits", "Quality seen as the quality manager's job"]),
                   right=dict(title="Useful QMS", points=["Short, visual documents at the point of use", "Processes that reflect how work is done", "Measures used in regular management meetings", "Leaders own quality; staff raise problems"]))),
  dict(step=3, type="cycle", title="Plan-Do-Check-Act and the clauses", caption="Click each stage to see which clauses of ISO 9001 belong to it.",
       config=dict(center="PDCA", stages=[
        dict(label="Plan", text="Clauses 4–6: context, leadership, risks, objectives."),
        dict(label="Do", text="Clauses 7–8: support and operation."),
        dict(label="Check", text="Clause 9: monitoring, internal audit, management review."),
        dict(label="Act", text="Clause 10: corrective action and continual improvement.")])),
  dict(step=8, type="stack", title="What to document", caption="Click each layer, from the bottom up, to see the documented information a lean QMS typically needs.",
       config=dict(top_label="A lean, controlled QMS", layers=[
        dict(label="Required documents", text="Scope, quality policy, quality objectives."),
        dict(label="Process map", text="Main processes, owners and how they connect."),
        dict(label="Work instructions and checklists", text="Where errors are likely, tasks are complex or customers require them."),
        dict(label="Required records", text="Competence, calibration, supplier evaluation, release, nonconformity, audits, reviews."),
        dict(label="Control", text="Approval, versions, availability and retention.")])),
  dict(step=12, type="flow", title="From nonconformity to lasting fix", caption="Click each step in the corrective action process.",
       config=dict(steps=[
        dict(label="Contain", text="Identify, segregate and correct the nonconforming output."),
        dict(label="Root cause", text="Use 5 Whys or a fishbone; look for similar problems elsewhere."),
        dict(label="Act on the cause", text="Change the process, not just the person."),
        dict(label="Verify", text="Check later that the problem has not recurred."),
        dict(label="Update the system", text="Revise risks, documents and training as needed.")])),
  dict(step=13, type="bars", title="Example: customer complaints by cause", caption="Illustrative complaints over 12 months at a small fabricator. Two causes account for most complaints.",
       config=dict(unit="complaints", items=[dict(label="Late delivery", value=18, highlight=True), dict(label="Wrong revision built", value=11, highlight=True), dict(label="Damaged in transit", value=6), dict(label="Missing paperwork", value=4), dict(label="Other", value=3)],
        note="In this example, late delivery and wrong revisions make up about 70% of complaints and become the first corrective action priorities.")),
  dict(step=16, type="timeline", title="A typical path to certification", caption="Click each phase. Most SMEs take 6 to 12 months.",
       config=dict(phases=[
        dict(label="Month 1", title="Commit and assess", items=["Leadership commitment", "Scope and plan", "Gap assessment"]),
        dict(label="Months 2–5", title="Build", items=["Process map, policy, objectives", "Risks, documents, training matrix", "Supplier and release controls"]),
        dict(label="Months 4–8", title="Run and check", items=["Generate records", "Full internal audit cycle", "Management review"]),
        dict(label="Months 7–12", title="Certify", items=["Stage 1 audit", "Close findings", "Stage 2 audit"])])),
 ],
 exam=[
  E("What does ISO 9001 specify?", ["Requirements for a quality management system", "Product designs", "Prices for quality audits", "Safety rules for factories"], 0, "ISO 9001 sets QMS requirements."),
  E("What is ISO 9001 certification?", ["Self-declaration by the company", "An independent audit confirming the QMS meets the standard", "A government licence", "A product warranty"], 1, "Certification bodies audit and certify conformity."),
  E("Which is one of the seven quality management principles?", ["Lowest price", "Maximum documentation", "Process approach", "Annual inspection"], 2, "The process approach is a core principle."),
  E("Which clauses contain the requirements of ISO 9001?", ["Clauses 1–3", "Clauses 1–10 equally", "Annexes only", "Clauses 4–10"], 3, "Requirements begin at clause 4."),
  E("Which PDCA stage do clauses 7 and 8 correspond to?", ["Do", "Plan", "Check", "Act"], 0, "Support and operation are 'Do'."),
  E("What did the 2024 amendment add to ISO 9001:2015?", ["A requirement for a quality manual", "Consideration of whether climate change is relevant to the organization's context", "A ban on outsourcing", "New product test methods"], 1, "The amendment added climate change considerations to clause 4."),
  E("What must be justified in the QMS scope?", ["Employee salaries", "Office locations only", "Any requirement that cannot be applied", "The number of customers"], 2, "Non-applicable requirements need justification."),
  E("Who is accountable for the effectiveness of the QMS?", ["The certification body", "Customers", "The quality manager alone", "Top management"], 3, "Top management holds accountability."),
  E("What makes a good quality objective?", ["Specific, measurable, owned and time-bound", "Vague and inspiring", "Set by the auditor", "Kept confidential"], 0, "Measurable objectives can be tracked."),
  E("Does ISO 9001 require a specific risk management method?", ["Yes, a certified method", "No; proportionate risk-based thinking is required", "Only for service firms", "Only after certification"], 1, "The method is up to the organization."),
  E("What must be true of monitoring and measuring equipment where traceability is required?", ["It must be new", "It must be imported", "It must be calibrated against recognized standards and identified with its status", "It must be owned by the customer"], 2, "Calibration and status identification are required."),
  E("Is a quality manual mandatory under ISO 9001:2015?", ["Yes", "Only for certification", "Only for manufacturers", "No"], 3, "The manual is optional."),
  E("When should customer requirements be reviewed?", ["Before committing to supply", "After delivery", "Only after complaints", "At management review only"], 0, "Review before accepting the order."),
  E("How should supplier controls be set?", ["Identically for all suppliers", "In proportion to their effect on quality", "Only by price", "Not at all"], 1, "Controls are risk-based."),
  E("Which process typically needs validation because results can't be fully verified afterwards?", ["Filing", "Shipping labels", "Welding or heat treatment", "Answering phones"], 2, "Special processes need validation."),
  E("What is the difference between correction and corrective action?", ["They are the same", "Correction prevents recurrence; corrective action fixes this case", "Corrective action is optional", "Correction fixes this case; corrective action removes the root cause"], 3, "Corrective action prevents recurrence."),
  E("Why should internal auditors not audit their own work?", ["To keep audits objective and impartial", "It is too slow", "Auditors must be external", "To save money"], 0, "Impartiality makes findings credible."),
  E("How often must management review take place?", ["Never", "At planned intervals", "Only after complaints", "Only during certification audits"], 1, "Management review happens at planned intervals."),
  E("Which body accredits certification bodies in Canada?", ["ISO itself", "The provincial government", "The Standards Council of Canada", "The certification bodies accredit themselves"], 2, "SCC is Canada's accreditation body."),
  E("How long is an ISO 9001 certificate typically valid?", ["One month", "One year with no audits", "Ten years", "Three years, with surveillance audits at least yearly"], 3, "Three-year cycles with yearly surveillance are typical."),
 ],
)

if __name__ == "__main__":
    write(course, "iso9001", __file__, balance=True)
