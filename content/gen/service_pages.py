"""Rich solution pages with animated heroes and interactive figures (V4.4). Called from build_v3.py with its namespace."""
import json, os, html as H
import assetver
from service_art import svc_art

esc = lambda s: H.escape(s or "", quote=True)


def fig(F):
    data = esc(json.dumps({"type": F["type"], "config": F["config"]}, ensure_ascii=False))
    kind = {"cycle": "Interactive cycle", "flow": "Process flow", "stack": "Building blocks", "compare": "Before and after", "timeline": "Roadmap", "bars": "Visual comparison", "swimlane": "Swim lane process"}[F["type"]]
    return (f'<figure class="cfig" data-svc-fig="{data}"><figcaption><span class="fig-kicker">{kind}</span><strong>{esc(F["title"])}</strong>'
            f'<span class="fig-cap">{esc(F["caption"])}</span></figcaption><div class="fig-host"></div></figure>')


PAGES = {
 "artificial-intelligence": dict(
  title="Artificial Intelligence Solutions",
  meta="Practical AI consulting for Canadian SMEs: AI opportunity assessment, strategy, vendor selection, governance, chatbots and assistants, integration, training and measurable results.",
  eyebrow="Solutions · Artificial Intelligence",
  h1="AI that works in your operations, not just in a demo.",
  lead="We help you find where AI genuinely improves efficiency and reduces cost, choose the right tools, implement them safely and make sure your team actually uses them, from first assessment to measurable results.",
  intro=("Are you looking to integrate AI into your business but don't know where to start?",
         "Most SMEs don't lack AI tools. They lack a clear view of where AI pays off, data they can trust, and a safe way to roll it out. Chmltech brings an operations-first approach: we start from your processes and goals, then apply AI where it removes real work, improves decisions or serves customers better."),
  signs=["You have tried a few AI tools, but nothing has scaled beyond individual use",
         "Staff spend hours searching for information, re-keying data or writing routine documents",
         "Customer questions pile up in inboxes and phone queues",
         "You are unsure what data is safe to use with AI, or who is accountable",
         "Vendors pitch AI features, and you can't tell which ones are worth paying for"],
  services_title="How we help",
  services=[("target", "AI opportunity assessment", "Identify where AI can improve efficiency and reduce costs across your processes, and assess your current AI capabilities and data readiness."),
            ("map", "AI strategy and roadmap", "A prioritized, phased plan that ties AI initiatives to business goals, with clear owners, budgets and success measures."),
            ("grid", "Vendor and technology selection", "Help selecting the right vendors and technologies for your specific needs, model-agnostic and without lock-in."),
            ("shield", "Ethics, legal and governance", "Guidance on the ethical and legal considerations of AI, including privacy (PIPEDA), acceptable-use policies, human oversight and risk controls."),
            ("users", "Chatbots and AI assistants", "Design and implementation of chatbots and assistants that enhance customer service and support, grounded in your own knowledge base."),
            ("flow", "Integration with your systems", "Connect AI to your ERP, CRM, documents and other tools so it works inside your workflows, not beside them."),
            ("book", "Training and adoption", "Training and support so your employees can use, trust and maintain AI systems effectively."),
            ("gauge", "Measure and optimize", "Measure and evaluate the success of your AI initiatives, then monitor and optimize performance over time.")],
  figs=[{"type": "cycle", "title": "From AI idea to measurable value", "caption": "Click each stage to see how we take an AI idea from opportunity to results.",
         "config": {"center": "AI value", "stages": [
           {"label": "Discover", "text": "Map goals, processes, data and pain points to find where AI could remove real work or improve decisions."},
           {"label": "Prioritize", "text": "Score opportunities on value, feasibility and risk, and pick a small number to start with."},
           {"label": "Pilot", "text": "Prove the use case with real users and real data, with clear success measures agreed up front."},
           {"label": "Integrate", "text": "Connect the solution to your systems, add guardrails and human review where it matters, and train the team."},
           {"label": "Measure", "text": "Track adoption, quality and business results, then improve the solution or scale it to the next area."}]}},
        {"type": "stack", "title": "What successful AI rests on", "caption": "AI results depend on the layers underneath. Click a layer for details.",
         "config": {"top_label": "AI results you can measure", "layers": [
           {"label": "Clear business goals", "text": "Every AI initiative starts from a business problem and a measurable target, not from a tool."},
           {"label": "Trusted, accessible data", "text": "Accurate, well-organized data and documents that the AI can access securely."},
           {"label": "Connected systems", "text": "Integrations with your ERP, CRM and other tools so AI works inside real workflows."},
           {"label": "Governance and safety", "text": "Policies, permissions, privacy safeguards and human oversight that keep AI use safe and accountable."},
           {"label": "Skilled, confident people", "text": "Teams who understand AI, use it well and help improve it over time."}]}}],
  uses=[("Document processing", "Extract data from invoices, purchase orders, forms and contracts, and route it into your systems."),
        ("Customer service", "Chatbots and assistants that answer common questions, triage requests and hand off to people."),
        ("Knowledge search", "Find answers in SOPs, specifications and past projects in seconds, with sources."),
        ("Writing and reporting", "Draft quotes, reports, emails and summaries faster, with a person reviewing the output."),
        ("Forecasting and planning", "Better demand, inventory and capacity planning from your historical data."),
        ("AI agents and automation", "Agents that carry out multi-step tasks across systems, with approvals built in.")],
  options=[("AI Readiness Assessment", "A structured review of your goals, data, systems, skills and risks, with a prioritized list of AI opportunities.", "e676eeeb-ed5f-40e1-b4c7-e287da77981b"),
           ("Focused AI pilot", "Prove one high-value use case end to end, with success measures, guardrails and a scale-up plan.", None),
           ("AI Operating System", "One connected, governed AI layer across your data, knowledge, assistants and workflows.", "ai-operating-system.html")],
  faq=[("Do we need a lot of data to start with AI?", "Not always. Many valuable uses, such as document processing, knowledge search and drafting, work with the documents and records you already have. We assess data readiness first so you know what is realistic."),
       ("Will AI replace our staff?", "Our focus is removing repetitive work so people can spend time on judgement, customers and improvement. We design human review into any process where decisions matter."),
       ("How do you handle privacy and security?", "We follow privacy-by-design: data minimisation, approved tools, access controls and audit trails, aligned with Canadian privacy requirements such as PIPEDA."),
       ("Can you help us build chatbots?", "Yes. We design, build and implement chatbots and assistants grounded in your own knowledge base, with clear hand-off to your team.")],
  courses=["ai-awareness-for-everyone", "llms-for-business-leaders", "ai-agents-for-business-operations", "e676eeeb-ed5f-40e1-b4c7-e287da77981b"],
  cats=["artificial-intelligence", "digital-technology"],
 ),
 "business-process-optimization": dict(
  title="Business Process Optimization (BPO)",
  meta="Business Process Optimization from Chmltech: identify, analyze, implement and monitor better processes using Lean, Six Sigma, BPM and change management to raise quality, engagement and profitability.",
  eyebrow="Solutions · Business Process Optimization",
  h1="Increase employee engagement, accelerate growth and profitability.",
  lead="Business Process Optimization (BPO) increases organizational efficiency by improving processes. We make your processes simple, clear and consistently applied, and align them with your strategic goals so every activity adds value.",
  intro=("What is Business Process Optimization?",
         "BPO is part of the discipline of Business Process Management (BPM). Optimized processes lead to optimized business goals. Your organization faces constant competition, disruptive technologies and changing norms. Optimizing how work actually flows, end to end and across departments, helps you stay ahead of that change instead of reacting to it."),
  signs=["Work waits in inboxes for approvals or hand-offs between departments",
         "The same data is typed into several systems or spreadsheets",
         "Errors, rework and exceptions consume a large share of the team's time",
         "Results depend on who is working that day, not on a defined process",
         "New systems were introduced, but the underlying process never changed"],
  services_title="What we deliver",
  services=[("map", "Current-state process maps", "We characterize how work really happens today, including information flows, roles, systems and decision points."),
            ("target", "Gap and opportunity analysis", "We identify waste, bottlenecks, control gaps and opportunities to improve quality, safety, throughput and cost."),
            ("flow", "Future-state (to-be) design", "Redesigned processes that are simple, clear and aligned with your strategic goals, with roles and controls defined."),
            ("chip", "Automation where it fits", "Once unnecessary steps are removed, we automate the revised process in its new form, not the old one."),
            ("users", "Change management", "Stakeholder engagement, communication and training that secure buy-in, so new processes are adopted and sustained."),
            ("gauge", "Monitoring and KPIs", "Measures and routines to look at performance at micro and macro levels and fine-tune until you get the desired results.")],
  figs=[{"type": "cycle", "title": "Our four-step BPO method", "caption": "Click each step to see what it involves. The cycle repeats as part of continuous improvement.",
         "config": {"center": "BPO", "stages": [
           {"label": "Identify", "text": "Select a problematic process to optimize, and define its purpose, scope and goals."},
           {"label": "Analyze", "text": "Is the process meeting its goals? Measure performance and find the waste, delays and errors to cut."},
           {"label": "Implement", "text": "Remove unnecessary steps, redesign the process, then automate the revised process in its new form."},
           {"label": "Monitor", "text": "Look at process performance from micro and macro views and fine-tune it until you get the desired results."}]}},
        {"type": "flow", "title": "Example: purchase orders stuck in email approvals", "caption": "Watch requests queue at the approval step, then click \"Fix the bottleneck\".",
         "config": {"steps": [
           {"label": "Employee request", "text": "An employee needs an item and raises a purchase request."},
           {"label": "Email approval", "text": "Requests sit in managers' inboxes. Approvals are slow, inconsistent and hard to track, so purchase orders clog the queue."},
           {"label": "PO created", "text": "Purchasing creates the purchase order once approval finally arrives."},
           {"label": "Order placed", "text": "The order goes to the supplier, often later than the business needed."}],
           "bottleneck": 1, "fix_text": "A dedicated workflow system lets employees choose the item and send it for approval automatically, with rules, reminders and a full audit trail."}}],
  examples=[("Purchase orders", "Multiple purchase orders clogged the purchasing queue because approvals happened by email.", "A dedicated workflow system now lets employees choose the item and send it for approval automatically."),
            ("Travel reimbursement", "A paper-based process meant finance misread numbers and reimbursed the wrong amounts.", "Employees now enter amounts in a digital form, which removes the misreading errors."),
            ("Employee onboarding", "HR manually emailed IT after each signed agreement to provision laptops and access.", "An automatic trigger now notifies IT as soon as the employee signs the agreement.")],
  outcomes=["Increase the strategic value of your business process efforts", "Improve the quality of products or services", "Improve morale and resource utilization",
            "Achieve consistent results", "Enhance your organization's ability to change", "Strengthen your company's bottom line"],
  methods="We apply continuous improvement methods including Lean, Six Sigma and other analytical tools, document processes using industry-standard notation, and combine them with change management. Too often, processes are redesigned only to be partially adopted or never implemented. Integrating the human side is what turns a better design into sustained performance.",
  faq=[("How is BPO different from process improvement?", "Process improvement often targets a specific area or problem. BPO looks at end-to-end processes across departments, such as order-to-cash or procure-to-pay, and aligns them with strategy, systems and controls."),
       ("Do we need new software?", "Not necessarily. We optimize the process first. Sometimes existing systems are enough once the process is fixed; where automation helps, we automate the improved process, not the old one."),
       ("How do you make changes stick?", "We involve the people who do the work, define clear roles and measures, and build change management and monitoring into the project so teams don't revert to old habits."),
       ("Which processes should we start with?", "Usually a process that is visibly painful, frequent and important to customers or cash flow. We help you choose using value, effort and risk.")],
  courses=["digital-automation-for-smes", "e385a42b-5aaf-457f-9957-e8d19fee8cc0", "91ca0386-ec82-483d-8ec7-d6b13f02a0b5", "b4b6581a-31f8-43f9-8796-268c83448b9f"],
  cats=["process-improvement", "lean"],
 ),
 "process-improvement": dict(
  title="Process Improvement",
  meta="Lean process improvement from Chmltech: KPIs, BPMN process mapping, value-added analysis, management tools and coaching that make improvements stick, delivered with your team.",
  eyebrow="Solutions · Process Improvement",
  h1="We believe in the power of being and doing better.",
  lead="Respond to threats and opportunities with agility. We work directly with your team to see your processes, extract the value-added activities and put KPIs in place, so you get results you can grow with.",
  intro=("Results you can grow with",
         "We transform your operating structure so you can make bold moves with confidence. Our approach goes beyond process to examine products, accountability structures, staff performance, management behaviour and use of technology. We don't leave you with a report of recommendations: we engage your people through every step and train them in continuous improvement methods that pay dividends long after our consultants have left."),
  signs=["Capacity seems maxed out, yet much of the day is spent waiting, searching or reworking",
         "Supervisors spend most of their time firefighting instead of managing",
         "KPIs are missing, unclear or not used in daily decisions",
         "Improvements happen, then fade within weeks",
         "Growth is held back by how the work is done, not by demand"],
  services_title="Key activities during the project",
  services=[("gauge", "Key performance metrics (KPIs)", "A framework of key metrics for service level, productivity, speed and quality for key processes, used to set the baseline and measure success."),
            ("map", "Mapping of key processes", "Process maps using industry-standard BPMN 2.0, built by interviewing managers and key employees, including information flows, roles and system touch points."),
            ("book", "Review of current practices and tools", "A thorough as-is analysis: process mapping, financial and operating data, direct observation and review of management tools."),
            ("trend", "Value-added analysis", "Process observations that quantify customer value-added and non-value-added activities and reveal hidden capacity."),
            ("users", "Team lead roles and responsibilities", "Time with team leads to understand their responsibilities and increase active management time."),
            ("grid", "Management tools", "Tools that measure and display KPIs so managers can run day-to-day operations with facts."),
            ("target", "Implemented method changes", "Quick wins and longer-term changes that make processes scalable, cost-effective and quality oriented, implemented with you.")],
  figs=[{"type": "timeline", "title": "How a Lean improvement program unfolds", "caption": "Our Lean programs typically run 15–25 weeks. Click each phase to see the activities.",
         "config": {"phases": [
           {"label": "Phase 1", "title": "Diagnose", "items": ["Set up the KPI framework and baseline", "Map key processes in BPMN 2.0", "Review current practices, data and tools"]},
           {"label": "Phase 2", "title": "Analyze", "items": ["Observe processes and quantify value-added vs non-value-added work", "Assess team lead roles and management time", "Agree priorities with leadership"]},
           {"label": "Phase 3", "title": "Implement", "items": ["Deliver quick wins", "Implement method and layout changes", "Install management tools and KPI boards"]},
           {"label": "Phase 4", "title": "Coach and sustain", "items": ["Coach managers to run daily operations with KPIs", "Train teams in continuous improvement", "Hand over a self-sustaining improvement routine"]}]}},
        {"type": "compare", "title": "Report-and-leave vs. working with your team", "caption": "Toggle to compare a typical recommendations report with Chmltech's embedded approach.",
         "config": {"left": {"title": "Report and leave", "points": ["Consultants observe, then deliver a report", "Recommendations are left for busy managers to implement", "Staff see change as something done to them", "Gains fade when attention moves on"]},
                    "right": {"title": "Chmltech: embedded with your team", "points": ["Your team maps processes and develops the ideas", "We stay through implementation, the hardest part", "Managers are coached to run with KPIs day to day", "Continuous improvement skills stay after we leave"]}}}],
  engagement=("Your team are the key drivers of change", "Your people are mentored every step of the way: through interviews, process mapping, observing processes and developing ideas for improvement. This engaging approach moves the organization through the change management cycle and makes sure the improvements stick. We provide the kick-start to your Lean journey."),
  lean=("Powerful Lean methodology", "Our Lean process improvement delivers real and sustained results, typically in 15–25 weeks. We embed ourselves in your organization and customize our improvement toolkit to go beyond one-time fixes. We know the hardest part is implementation, so we stay with you through it, coaching your managers to use the management tools and KPIs to improve day-to-day operations in their areas."),
  why=dict(title="A Canadian operations improvement firm that measures its work by your results.",
           text="Chmltech is a Canadian operations improvement firm that combines hands-on process engineering with Lean and Six Sigma methods. We measure our work by the results that show up in your KPIs and financial statements, not by the size of the report.",
           points=[("Results agreed up front", "Before the project starts, we agree with you the results it should deliver and how they will be measured, and we report against them."),
                   ("Measured on your numbers", "We set a KPI baseline at the start and track service level, productivity, speed, quality and cost savings through the program."),
                   ("Capability that stays", "Your managers and teams are trained in continuous improvement, so gains keep growing after our consultants leave.")],
           note="ROI targets are set for each engagement based on scope and baseline data. Actual results depend on scope, implementation and operating conditions."),
  faq=[("How long does a process improvement program take?", "Our Lean programs typically deliver results in 15–25 weeks, depending on scope. Quick wins usually come much earlier, during the first phases."),
       ("Will our operations be disrupted?", "We work alongside your team and plan changes around operating needs. Most work happens through observation, workshops and small, tested changes."),
       ("What will our people learn?", "Process mapping, waste identification, problem solving, standard work and running operations with KPIs. These skills remain after the project."),
       ("How do we know it worked?", "We set a KPI baseline at the start and track service level, productivity, speed and quality through the program, so results are measurable.")],
  courses=["b4b6581a-31f8-43f9-8796-268c83448b9f", "ac58bd83-591d-4c25-9aac-71755f469d3c", "25c5f60e-3f55-43a1-9c15-345dfc5b8f7f", "e385a42b-5aaf-457f-9957-e8d19fee8cc0"],
  cats=["process-improvement", "lean", "six-sigma"],
 ),
 "lean-six-sigma-training": dict(
  title="Lean Six Sigma Training",
  meta="In-house Lean Six Sigma training from Chmltech: White, Yellow, Green and Black Belt programs taught on your own processes, with live improvement projects, coaching and measurable results.",
  eyebrow="Solutions · Lean Six Sigma Training",
  h1="Lean Six Sigma training your team applies to its own work.",
  lead="In-house Lean Six Sigma training for Canadian organizations. Your people learn DMAIC and the Lean toolkit on their own processes, then lead real improvement projects with our coaching, so the training pays back in results, not just certificates.",
  intro=("Build a team that fixes problems for good.",
         "Lean removes waste from your processes. Six Sigma reduces the variation that causes defects, rework and delays. Together they give your people a shared, practical method for improving how work gets done. We teach it in-house, using your processes, your data and your problems, so every training day connects to the work your team does tomorrow."),
  signs_title="Signs your team is ready",
  signs=["The same problems keep coming back after quick fixes",
         "Rework, errors or customer complaints are eating into margin",
         "Improvement depends on one or two people who are always busy",
         "Teams argue about causes because the data isn't clear",
         "You want a common improvement language across departments"],
  services_title="What the training includes",
  services=[("target", "Training needs assessment", "We start with your goals, current skills and problem areas, then recommend the right mix of belt levels and who should attend."),
            ("book", "In-house belt training", "Practical sessions built around your processes and examples, from White Belt awareness to Green and Black Belt."),
            ("flow", "Live improvement projects", "Each Green and Black Belt participant leads a real project, chosen with management for its value to your organization."),
            ("users", "Project coaching", "We coach project leads through each DMAIC phase with regular reviews, so projects keep moving and reach measurable results."),
            ("gauge", "KPIs and visual management", "Teams learn to measure baseline performance, track improvement and make results visible on simple boards and dashboards."),
            ("shield", "Sustaining the gains", "Standard work, control plans and leader routines keep improvements in place after each project closes.")],
  uses_eyebrow="The toolkit",
  uses_title="Tools your team will use from day one",
  uses_lead="Every tool is practised on your own processes and data, not textbook cases.",
  uses=[("Process and value stream mapping", "SIPOC, swim lane maps and value stream maps show how work really flows and where time is lost."),
        ("The eight wastes", "Spot waiting, rework, motion, overprocessing and the other wastes that add cost without adding value."),
        ("Root cause analysis", "5 Whys, fishbone diagrams and Pareto charts move teams from opinions to proven causes."),
        ("Data and statistics", "Measurement checks, control charts and process capability show whether a process is stable and able to meet its target."),
        ("Error-proofing and standard work", "Simple checks and agreed methods stop defects at the source and make the best way the normal way."),
        ("Control plans", "Clear owners, measures and response plans keep each improvement from slipping back.")],
  options_eyebrow="Training levels",
  options_title="Choose the right belt for each role.",
  options_lead="Program length and content are tailored to your team. Typical formats are shown.",
  options=[("White Belt", "Awareness for all staff, typically a half day. The basics of waste, variation and DMAIC, so everyone can support improvement work.", ""),
           ("Yellow Belt", "Typically one to two days for team members who join projects. Process mapping, data collection and root cause tools.", ""),
           ("Green Belt", "Typically spread over several weeks alongside a live project. Participants lead an improvement project through all five DMAIC phases with our coaching.", ""),
           ("Black Belt", "Advanced statistics, larger cross-functional projects and coaching others. For people who will lead your improvement program.", ""),
           ("Leadership and Champions", "A short session for managers who sponsor projects: choosing the right projects, removing roadblocks and sustaining results.", ""),
           ("Free practice exams", "Try our free Lean Six Sigma Green Belt, Black Belt and case-study practice exams in the training library.", "training.html")],
  examples_eyebrow="Typical training projects",
  examples_title="What a training project looks like.",
  examples_lead="Illustrative examples of projects participants lead during their training.",
  examples=[("Invoice errors in finance", "Many invoices needed correction, delaying payment and tying up staff in follow-up.", "A Green Belt team traced most errors to order entry, added a simple checklist and system prompts, and corrections dropped sharply."),
            ("Changeover time on a packing line", "Long, inconsistent changeovers pushed the line toward large batches and late orders.", "Using SMED, the team moved setup work offline and standardized settings, freeing capacity for smaller, more frequent runs."),
            ("Customer call-backs in service", "Customers often had to call twice because their first request wasn't resolved.", "Root cause analysis showed missing information at intake; a short script and knowledge base raised first-contact resolution.")],
  outcomes_title="What your organization gains.",
  outcomes=["A shared, practical method for solving problems across departments",
            "Completed projects with measured savings and service improvements",
            "Fewer errors, less rework and more consistent processes",
            "Managers who lead with data and coach their teams",
            "Internal capability, so improvement continues after training ends",
            "Staff who are more engaged because they fix the problems that frustrate them"],
  figs=[{"type": "cycle", "title": "DMAIC: the Six Sigma improvement cycle", "caption": "Click each phase to see what participants do and which tools they use.",
         "config": {"center": "DMAIC", "stages": [
           {"label": "Define", "text": "Agree the problem, the customer requirement, the goal and the project scope. Tools: project charter, SIPOC, voice of the customer."},
           {"label": "Measure", "text": "Map the current process and collect reliable baseline data. Tools: process maps, data collection plans, measurement checks."},
           {"label": "Analyze", "text": "Find and prove the root causes of the problem. Tools: Pareto charts, fishbone diagrams, 5 Whys, basic statistics."},
           {"label": "Improve", "text": "Develop, test and implement solutions that remove the root causes. Tools: pilots, error-proofing, standard work, SMED."},
           {"label": "Control", "text": "Lock in the gains and hand the process back to its owner. Tools: control charts, control plans, visual management."}]}},
        {"type": "compare", "title": "Lean and Six Sigma: how they fit together", "caption": "Toggle to compare what each method focuses on. Your team learns both.",
         "config": {"left": {"title": "Lean: remove waste", "points": ["Focuses on speed and flow", "Finds steps that add no value for the customer", "Tools: value stream mapping, 5S, kanban, SMED", "Quick, visible wins on the floor or in the office"]},
                    "right": {"title": "Six Sigma: reduce variation", "points": ["Focuses on quality and consistency", "Finds the root causes of defects with data", "Tools: DMAIC, control charts, capability analysis", "Lasting fixes for complex, recurring problems"]}}}],
  lean_eyebrow="Method",
  lean=("Lean removes waste. Six Sigma reduces variation.", "Lean makes processes faster by removing steps that add no value. Six Sigma makes them more reliable by finding and fixing the causes of defects. Our training combines both, so your team can choose the right tool for each problem, from a quick waste walk to a data-driven DMAIC project."),
  engagement_eyebrow="Learning by doing",
  engagement=("Your people learn by improving real work", "We don't teach from generic case studies alone. Participants map their own processes, analyze their own data and lead projects their managers care about, with coaching at every phase. That is how new skills stick, and how the training starts paying back while it is still running."),
  why=dict(title="Training measured by the results it produces.",
           text="Chmltech combines hands-on process engineering with Lean and Six Sigma. We judge our training by the improvements your team delivers, not by the number of certificates issued.",
           points=[("Results agreed up front", "Before the program starts, we agree with you the results it should deliver and how they will be measured, and we report against them."),
                   ("Measured on your numbers", "Each project sets a KPI baseline and tracks the change in quality, speed, productivity or cost."),
                   ("Capability that stays", "Your Belts become internal coaches, so continuous improvement keeps going after the program ends.")],
           note="ROI targets are set for each program based on scope and baseline data. Actual results depend on project selection, implementation and operating conditions."),
  faq=[("Do participants need a statistics background?", "No. White and Yellow Belt need no statistics at all. Green and Black Belt introduce the statistics step by step, using your own data and simple tools."),
       ("How are improvement projects chosen?", "We work with your leaders to pick projects that matter to the business, have a clear owner and can show measurable results within the training period."),
       ("Do participants receive a certificate?", "Participants who complete their training receive a certificate of completion from Chmltech. If you need certification from an external body, we can help you plan for it."),
       ("What is the difference between the belt levels?", "White and Yellow Belts build awareness and support projects. Green Belts lead projects in their own area. Black Belts lead larger, cross-functional projects and coach others."),
       ("Can we combine training with a process improvement project?", "Yes. Many clients train a team while we work alongside them on a priority process, so learning and results happen together.")],
  courses=["b4b6581a-31f8-43f9-8796-268c83448b9f", "ac58bd83-591d-4c25-9aac-71755f469d3c", "25c5f60e-3f55-43a1-9c15-345dfc5b8f7f", "e385a42b-5aaf-457f-9957-e8d19fee8cc0"],
  cats=["six-sigma"],
),
}
from service_pages_v2 import PAGES as _V2   # V4.23: rewritten Wix-era solution pages
PAGES.update(_V2)


def build(ns):
    page, icon, related_posts_html, QUOTE, progs, OUT = ns["page"], ns["icon"], ns["related_posts_html"], ns["QUOTE"], ns["progs"], ns["OUT"]
    titles = {p["id"]: p["title"] for p in progs}
    for slug, P in PAGES.items():
        art = svc_art(slug, esc(P["title"]))
        hero = f'''<section class="page-hero dark course-hero"><div class="container course-hero-grid"><div class="stack-lg">
  <p class="crumbs"><a href="index.html">Home</a> / <a href="solutions.html">Solutions</a> / {esc(P["title"])}</p>
  <p class="eyebrow">{esc(P["eyebrow"])}</p><h1 class="h-xl" style="font-size:clamp(34px,4.4vw,56px)">{esc(P["h1"])}</h1>
  <p class="lead">{esc(P["lead"])}</p>
  <div class="btn-row"><a class="btn" href="book.html">Book a Strategy Call</a><a class="btn btn-ghost-dark" href="contact.html?service={esc(P["title"].split(" (")[0]).replace(" ", "%20")}">Ask a question</a></div>
</div>{art}</div></section>'''
        b = hero
        b += f'''
<section class="section"><div class="container feature-split">
  <div class="stack-lg"><p class="eyebrow">Overview</p><h2 class="h-lg">{esc(P["intro"][0])}</h2><p class="muted" style="font-size:17.5px">{esc(P["intro"][1])}</p>
  {f'<p class="muted" style="font-size:17.5px">{esc(P["methods"])}</p>' if P.get("methods") else ""}</div>
  <div class="card" style="padding:30px"><h3 style="font-size:20px">{esc(P.get("signs_title", "Signs you need this"))}</h3><ul class="list-check">{"".join(f"<li>{esc(x)}</li>" for x in P["signs"])}</ul></div>
</div></section>'''
        b += f'''
<section class="section sand"><div class="container">
  <div class="stack" style="max-width:720px;margin-bottom:28px"><p class="eyebrow">Our approach</p><h2 class="h-lg">See how it works.</h2></div>
  <div class="{'fig-col' if any(F["type"] in ("flow", "swimlane") for F in P["figs"]) else 'grid grid-2'}" style="align-items:start">{"".join(fig(F) for F in sorted(P["figs"], key=lambda F: F["type"] not in ("flow", "swimlane")))}</div>
</div></section>'''
        b += f'''
<section class="section"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Services</p><h2 class="h-lg">{esc(P["services_title"])}</h2></div></div>
  <div class="grid grid-3">{"".join(f'<article class="card">{icon(ic)}<h3 style="font-size:21px">{esc(t)}</h3><p class="muted">{esc(d)}</p></article>' for ic, t, d in P["services"])}</div>
</div></section>'''
        if P.get("uses"):
            b += f'''
<section class="section dark"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">{esc(P.get("uses_eyebrow", "Where AI helps"))}</p><h2 class="h-lg">{esc(P.get("uses_title", "Practical AI use cases for SMEs"))}</h2></div><p class="lead" style="font-size:17px">{esc(P.get("uses_lead", "Start where the work is repetitive, information-heavy or customer-facing."))}</p></div>
  <div class="grid grid-3">{"".join(f'<div class="card card-dark" style="background:#11335F;border-color:#234A80"><h3 style="font-size:19px">{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in P["uses"])}</div>
</div></section>'''
        if P.get("options"):
            def opt_link(x):
                if not x: return "contact.html"
                return x if x.endswith(".html") else f"challenge-page/{x}.html"
            b += f'''
<section class="section"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">{esc(P.get("options_eyebrow", "Ways to start"))}</p><h2 class="h-lg">{esc(P.get("options_title", "Choose your starting point."))}</h2></div>{f'<p class="muted" style="max-width:420px">{esc(P["options_lead"])}</p>' if P.get("options_lead") else ""}</div>
  <div class="grid grid-3">{"".join(f'<article class="card"><h3 style="font-size:21px">{esc(t)}</h3><p class="muted">{esc(d)}</p><a class="more" href="{opt_link(l)}">{"Learn more →" if l else "Enquire →"}</a></article>' for t, d, l in P["options"])}</div>
</div></section>'''
        if P.get("examples"):
            b += f'''
<section class="section dark"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">{esc(P.get("examples_eyebrow", "Real examples"))}</p><h2 class="h-lg">{esc(P.get("examples_title", "How optimization increases efficiency."))}</h2></div>{f'<p class="lead" style="font-size:16px">{esc(P["examples_lead"])}</p>' if P.get("examples_lead") else ""}</div>
  <div class="grid grid-3">{"".join(f'<div class="card card-dark" style="background:#11335F;border-color:#234A80"><h3 style="font-size:20px">{esc(t)}</h3><p><strong style="color:#F7B58A">Before:</strong> {esc(bf)}</p><p><strong style="color:var(--green)">After:</strong> {esc(af)}</p></div>' for t, bf, af in P["examples"])}</div>
</div></section>
<section class="section"><div class="container grid grid-2" style="align-items:center">
  <div class="stack"><p class="eyebrow">Outcomes</p><h2 class="h-lg">{esc(P.get("outcomes_title", "What optimized processes deliver."))}</h2></div>
  <ul class="list-check" style="font-size:17px">{"".join(f"<li>{esc(x)}</li>" for x in P["outcomes"])}</ul>
</div></section>'''
        if P.get("lean"):
            b += f'''
<section class="section dark"><div class="container grid grid-2">
  <div class="stack"><p class="eyebrow">{esc(P.get("lean_eyebrow", "Lean"))}</p><h2 class="h-md">{esc(P["lean"][0])}</h2><p class="lead" style="font-size:17px">{esc(P["lean"][1])}</p></div>
  <div class="stack"><p class="eyebrow">{esc(P.get("engagement_eyebrow", "People"))}</p><h2 class="h-md">{esc(P["engagement"][0])}</h2><p class="lead" style="font-size:17px">{esc(P["engagement"][1])}</p></div>
</div></section>'''
        if P.get("why"):
            W = P["why"]
            b += f'''
<section class="section"><div class="container">
  <div class="stack" style="max-width:820px;margin-bottom:36px"><p class="eyebrow">Why Chmltech</p><h2 class="h-lg">{esc(W["title"])}</h2><p class="muted" style="font-size:17.5px">{esc(W["text"])}</p></div>
  <div class="grid grid-3">{"".join(f'<article class="card"><span class="price" style="font-size:22px">{"ROI" if i == 0 else ("KPI" if i == 1 else "CI")}</span><h3 style="font-size:21px">{esc(t)}</h3><p class="muted">{esc(d)}</p></article>' for i, (t, d) in enumerate(W["points"]))}</div>
  <p class="count" style="margin-top:16px">{esc(W["note"])}</p>
</div></section>'''
        b += f'''
<section class="section sand"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Questions</p><h2 class="h-lg">Frequently asked</h2></div></div>
  <div class="faq">{"".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in P["faq"])}</div>
</div></section>
<section class="section"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Free learning</p><h2 class="h-lg">Related free courses</h2></div><a class="btn btn-ghost" href="courses.html">All free courses</a></div>
  <div class="grid grid-4">{"".join(f'<a class="card" style="text-decoration:none;padding:24px" href="challenge-page/{c}.html"><span class="tag tag-green">Free course</span><h3 style="font-size:18px">{esc(titles.get(c, ""))}</h3><span class="more" style="font-weight:600">Start →</span></a>' for c in P["courses"] if c in titles)}</div>
</div></section>
{related_posts_html(P["cats"])}
{QUOTE}'''
        page(f"{slug}.html", P["title"], esc(P["meta"]), b)
        fp = os.path.join(OUT, f"{slug}.html"); s = open(fp).read(); s = assetver.strip(s)
        s = s.replace("</head>", '<link rel="stylesheet" href="assets/css/course.css">\n</head>', 1)
        s = s.replace('<script src="assets/js/main.js" defer></script>', '<script src="assets/js/main.js" defer></script>\n<script src="assets/js/figures.js" defer></script>\n<script src="assets/js/svc.js" defer></script>', 1)
        open(fp, "w").write(s)
