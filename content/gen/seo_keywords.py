"""Search keywords for the main pages (V4.59). Applied by seo_pass.py.

For each page: title (shown in search results), H1 (the page's main heading, carrying the
search phrase), and meta description. The page's previous heading (the slogan) is kept as
the line just below the new H1 (set slogan="" to drop it, or slogan="..." to replace it). Edit here, then run:  python3 content/gen/seo_pass.py .

Phrasing follows how Canadian buyers and competitors search: "consulting/consultant",
"small businesses", and the location (Vancouver, BC / Canada). Keep titles under ~65
characters so they show in full; descriptions under ~155.
"""

KEYWORDS = {
    "index.html": dict(
        title="AI & Operations Consulting in Vancouver, BC | Chmltech",
        h1="AI and operations consulting for Canadian small businesses",
        eyebrow="Vancouver, BC · Serving businesses across Canada",
        desc="Vancouver consulting firm helping Canadian small businesses adopt AI, improve processes, choose systems and automate work. Book a free strategy call."),
    "solutions.html": dict(
        title="Business Consulting Services for Small Businesses | Chmltech",
        h1="Business consulting services for small and mid-sized businesses",
        desc="AI consulting, process improvement, ISO 9001, Lean Six Sigma training and growth advisory "
             "for Canadian small businesses, from our Vancouver, BC office."),
    "industries.html": dict(
        title="Industry Consulting: Manufacturing, Energy & More | Chmltech",
        h1="Operations consulting for manufacturing, energy, distribution and more",
        desc="Process improvement and AI consulting for Canadian manufacturers, energy and chemical plants, distributors, health care and the public sector."),
    "artificial-intelligence.html": dict(
        title="AI Consulting for Small Businesses | Vancouver, BC | Chmltech",
        h1="AI consulting for small and mid-sized businesses",
        desc="Practical AI consulting in Vancouver and across Canada: AI assessment and strategy, "
             "vendor selection, governance, assistants, integration and team training."),
    "ai-operating-system.html": dict(
        title="AI Operating System Design & Build | Chmltech",
        h1="AI Operating System design and build for small businesses",
        desc="We design and build your company's AI Operating System: connected data, company knowledge, AI agents and workflows, with governance."),
    "business-process-optimization.html": dict(
        title="Business Process Optimization Consulting | Vancouver | Chmltech",
        h1="Business process optimization consulting",
        desc="Business process optimization for small businesses: find, fix and monitor better processes with Lean, Six Sigma and change management."),
    "iso9001.html": dict(
        title="ISO 9001 Consultant for Small Businesses | BC & Canada | Chmltech",
        h1="ISO 9001 consulting for small businesses",
        desc="ISO 9001 consulting for small businesses in BC and across Canada: a quality management "
             "system that runs your business better and passes certification."),
    "leadership-operating-system.html": dict(
        title="Leadership Operating System for Small Businesses | Chmltech",
        h1="A leadership operating system for small business teams",
        desc="Help for small business leadership teams: a clear plan, 90-day priorities, a weekly scorecard and meeting rhythm, clear roles and issue solving."),
    "lean-six-sigma-training.html": dict(
        title="Lean Six Sigma Training for Teams | Vancouver, BC | Chmltech",
        h1="Lean Six Sigma training for your team",
        desc="Lean Six Sigma training in Vancouver and online, built around your own processes so your "
             "team applies the tools to real improvement projects."),
    "operational-efficiency.html": dict(
        title="Operational Efficiency Consulting | Vancouver, BC | Chmltech",
        h1="Operational efficiency consulting",
        desc="Operational efficiency consulting for Canadian small businesses: get more output from the "
             "people, equipment and space you already have."),
    "process-improvement.html": dict(
        title="Process Improvement Consultant | Vancouver, BC | Chmltech",
        h1="Process improvement consulting for small businesses",
        desc="Process improvement consultant in Vancouver, BC: Lean and Six Sigma methods, KPIs and change management your team owns. Serving all of Canada."),
    "process-mapping.html": dict(
        title="Process Mapping Consultant | Vancouver, BC | Chmltech",
        h1="Business process mapping services",
        desc="Business process mapping with the people who do the work: every step, hand-off, system and decision, and where time and errors creep in."),
    "project-portfolio-management.html": dict(
        title="Project Portfolio Management Consulting | Chmltech",
        h1="Project portfolio management consulting",
        desc="Project portfolio management consulting for Canadian businesses: choose the right "
             "projects, balance resources and deliver them on time."),
    "rapid-lean-assessment.html": dict(
        title="Lean Assessment of Your Operation in Two Weeks | Chmltech",
        h1="Rapid Lean assessment: a two-week operations review",
        desc="A two-week Lean assessment of your operation: interviews, process walk-throughs and financial analysis, ending in prioritized quick wins."),
    "scaling-up.html": dict(
        title="Growth Consulting for Small Businesses | Vancouver | Chmltech",
        h1="Growth consulting for small businesses",
        desc="Growth advisory for Canadian small businesses: the processes, systems, team structure and cash discipline to grow without losing control."),
    "manufacturing.html": dict(
        title="Manufacturing Consulting | BC & Canada | Chmltech",
        h1="Manufacturing consulting: Lean operations and productivity",
        desc="Manufacturing consulting for Canadian manufacturers: improve margins, reduce overhead and "
             "free up capital with a practical Lean method your team owns."),
    "energy-and-chemicals.html": dict(
        title="Energy & Chemical Plant Consulting | Chmltech",
        h1="Operations and process consulting for energy and chemical plants",
        desc="Operational excellence and process engineering support for Canadian energy and chemical operators: KPIs, Lean improvement and change management."),
    "distribution-and-warehousing.html": dict(
        title="Warehouse & Distribution Operations Consulting | Chmltech",
        h1="Warehouse and distribution operations consulting",
        desc="Process improvement for Canadian distributors and warehouses: better inventory turns and accuracy, freed-up cash flow and room to grow."),
    "consumer-goods.html": dict(
        title="Consumer Goods Operations Consulting | Chmltech",
        h1="Operations consulting for consumer goods companies",
        desc="Lean and process improvement for Canadian consumer goods companies: protect product margins, "
             "cut non-value-added time and serve customers better."),
    "health-care.html": dict(
        title="Health Care Process Improvement Consulting | Chmltech",
        h1="Process improvement consulting for health care",
        desc="Process improvement for Canadian health care organizations: better patient flow, shorter "
             "wait times and practical KPIs, built with staff and union partners."),
    "natural-resources.html": dict(
        title="Mining & Forestry Operations Consulting | Chmltech",
        h1="Operations consulting for mining, forestry and resource companies",
        desc="Lean and continuous improvement for Canadian mining, forestry and resource companies: cut costs, clear maintenance backlogs, improve margins."),
    "professional-services.html": dict(
        title="Consulting for Professional Services Firms | Chmltech",
        h1="Operations consulting for professional services firms",
        desc="Operational excellence for Canadian professional services firms: lift utilization and "
             "realization, tighten delivery and build continuous improvement."),
    "public-sector.html": dict(
        title="Public Sector Process Improvement Consulting | Chmltech",
        h1="Process improvement consulting for the public sector",
        desc="Process improvement and KPIs for Canadian public sector organizations: higher productivity, "
             "service standards met and more value from every budget dollar."),
    "about.html": dict(
        title="About Chmltech: Vancouver Business & Process Consulting Firm",
        h1="About Chmltech, a Vancouver consulting firm",
        desc="Chmltech Ltd. is a Vancouver, BC consulting firm led by Quak Foo Lee, helping Canadian small businesses improve operations with process work and AI."),
    "training.html": dict(
        title="Free Practice Exams: PMP, Lean Six Sigma, ISO 9001 | Chmltech",
        h1="Free practice exams: PMP, Lean Six Sigma, ISO 9001 and more",
        slogan="For technical and professional growth.",
        desc="Free interactive practice exams with thousands of questions: PMP, Lean Six Sigma, ISO 9001, "
             "NPPE, Kaizen, AI, process engineering and project management."),
    "courses.html": dict(
        title="Free Online Courses: AI, Lean & Operations | Chmltech",
        h1="Free online courses in AI, Lean and operational excellence",
        slogan="",
        desc="Free interactive online courses on AI for business, LLMs, AI agents, Lean Six Sigma, ISO 9001, S&OP, ERP selection, cybersecurity and FEED, with labs, exams and certificates."),
    "insights.html": dict(
        title="Articles on AI, Lean & Process Engineering | Chmltech",
        h1="Articles on AI, Lean, process engineering and operations",
        desc="Free articles and research papers on AI, digital transformation, Lean, Six Sigma, ISO 9001, "
             "process engineering, ERP and strategy for Canadian businesses."),
    "llm-leaderboard.html": dict(
        title="LLM Leaderboard: Compare AI Models by Score and Cost | Chmltech",
        h1="LLM leaderboard: compare AI models by score and cost",
        desc=None),
    "contact.html": dict(
        title="Contact Chmltech | Business Consultant in Vancouver, BC",
        h1="Contact our Vancouver consulting team",
        desc=None),
    "book.html": dict(
        title="Book a Free Strategy Call | Chmltech, Vancouver BC",
        h1="Book a free strategy call",
        slogan="",
        desc="Book a free strategy call or a paid expert session with Chmltech Ltd., a Vancouver "
             "consulting firm for AI, process improvement and operations."),
    "projects.html": dict(
        title="Consulting & Engineering Projects | Chmltech",
        h1=None,
        desc=None),
}
