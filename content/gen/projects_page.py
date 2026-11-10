"""Projects page (V4.24): engineering projects and the Digital Adoption Plan track record.

Clients are described by sector only, as agreed with the owner. The breakdown of the 300+ plans
(sector, province, year) is not published yet; when data/dap_stats.json exists it is rendered as a chart.
"""
import json, os
from service_pages import fig, esc
from industry_art import industry_art

HERE = os.path.dirname(os.path.abspath(__file__))
STATS = os.path.join(HERE, "..", "data", "dap_stats.json")

ENGINEERING = [
    dict(sector="Advanced materials producer, BC", title="Commercial-scale front-end engineering design (FEED)", status="In progress",
         summary="Taking a new advanced-materials process from pilot plant to a commercial-scale design, area by area, from raw-material preparation to finished product.",
         scope=["Process design basis and process flow diagrams for every plant area",
                "Mass and energy balances and stream tables",
                "Equipment sizing and FEED-level equipment datasheets",
                "Capital and operating cost estimates to AACE Class 4 and Class 3",
                "Materials of construction and corrosion review",
                "Safety, HAZOP-style and management-of-change reviews",
                "Computational fluid dynamics (CFD) studies of key equipment"],
         services=[("Process engineering and scale-up", "energy-and-chemicals.html"), ("Engineering CAPEX and OPEX", "post/engineering-capex-and-opex-estimation-for-process-plants.html")]),
    dict(sector="Biodiesel producer", title="Plant review: economics, HAZOP and P&ID assessment", status="In progress",
         summary="An independent review of an operating biodiesel plant, covering its economics, its process safety and the quality of its engineering drawings.",
         scope=["Economic analysis of plant operations and improvement options",
                "Hazard and operability study (HAZOP) of the process",
                "Assessment of piping and instrumentation diagrams (P&IDs) against the plant as built and good practice",
                "Prioritized recommendations for safety, reliability and cost"],
         services=[("Energy and chemicals", "energy-and-chemicals.html"), ("Process improvement", "process-improvement.html")]),
]

AREAS = [("grid", "ERP and accounting", "Choosing and planning business systems that connect finance, inventory and operations."),
         ("users", "CRM and sales", "Customer records, quoting and pipeline management in one place."),
         ("layers", "Inventory and warehouse", "Stock control, barcode scanning and warehouse management."),
         ("trend", "E-commerce and digital marketing", "Online sales channels, websites and customer reach."),
         ("flow", "Workflow automation and AI", "Removing manual re-keying and approvals, and practical AI use cases."),
         ("shield", "Cybersecurity and data", "Backups, access control and safe handling of business data.")]

DAP_FIG = {"type": "timeline", "title": "What a Digital Adoption Plan covers", "caption": "Each plan follows the same structure. Click each phase to see the work.",
           "config": {"phases": [
               {"label": "Phase 1", "title": "Discover", "items": ["Business goals and constraints", "Interviews with owners and staff", "Current systems and data"]},
               {"label": "Phase 2", "title": "Map", "items": ["Current-state process maps", "Pain points and manual work", "Information flows between systems"]},
               {"label": "Phase 3", "title": "Recommend", "items": ["Technology options by process", "Vendor shortlist and indicative costs", "Quick wins"]},
               {"label": "Phase 4", "title": "Roadmap", "items": ["Phased implementation plan", "Budget, risks and change management", "Measures of success"]}]}}


def stats_chart():
    """Horizontal bar list of plans by sector, from data/dap_stats.json (added when the owner supplies the data)."""
    if not os.path.exists(STATS): return ""
    S = json.load(open(STATS))
    rows = sorted(S.get("by_sector", {}).items(), key=lambda kv: -kv[1])
    if not rows: return ""
    top = max(v for _, v in rows)
    bars = "".join(f'<div class="pj-bar"><span class="pj-bar-l">{esc(k)}</span><span class="pj-bar-t"><span style="width:{100 * v / top:.1f}%"></span></span><span class="pj-bar-v">{v}</span></div>' for k, v in rows)
    return f'''<div class="card" style="padding:28px;margin-top:28px"><h3 style="font-size:20px">Plans by sector</h3><div class="pj-bars">{bars}</div>{f'<p class="count" style="margin-top:12px">{esc(S["note"])}</p>' if S.get("note") else ""}</div>'''


def eng_card(P):
    return f'''<article class="card pj-card">
  <div class="pj-head"><span class="tag">{esc(P["sector"])}</span><span class="tag tag-green">{esc(P["status"])}</span></div>
  <h3 style="font-size:24px">{esc(P["title"])}</h3>
  <p class="muted" style="font-size:17px">{esc(P["summary"])}</p>
  <h4 class="pj-sub">Scope</h4><ul class="list-check">{"".join(f"<li>{esc(x)}</li>" for x in P["scope"])}</ul>
  <p class="pj-links">Related: {" · ".join(f'<a href="{u}">{esc(t)}</a>' for t, u in P["services"])}</p>
</article>'''


CSS = """<style>
.pj-chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.pj-chips a{display:inline-flex;align-items:center;padding:8px 16px;border-radius:999px;border:1px solid rgba(255,255,255,.35);color:#fff;text-decoration:none;font-weight:600;font-size:14px}
.pj-chips a:hover{background:rgba(255,255,255,.12)}
.pj-card{padding:32px}
.pj-head{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px}
.pj-sub{font-size:15px;text-transform:uppercase;letter-spacing:.06em;color:var(--blue,#0B6FA4);margin:18px 0 6px}
.pj-links{margin-top:16px;font-size:15px}
.pj-bars{display:grid;gap:10px;margin-top:14px}
.pj-bar{display:grid;grid-template-columns:minmax(120px,220px) 1fr 48px;gap:12px;align-items:center;font-size:15px}
.pj-bar-t{height:12px;background:#E7EEF6;border-radius:6px;overflow:hidden}
.pj-bar-t span{display:block;height:100%;background:#0B6FA4;border-radius:6px}
.pj-bar-v{font-weight:700;text-align:right}
@media (max-width:640px){.pj-bar{grid-template-columns:1fr 40px}.pj-bar-t{grid-column:1/-1;grid-row:2}}
</style>"""


def build(ns):
    page, icon, OUT = ns["page"], ns["icon"], ns["OUT"]
    b = f'''{CSS}<section class="page-hero dark course-hero"><div class="container course-hero-grid"><div class="stack-lg">
  <p class="crumbs"><a href="index.html">Home</a> / Projects</p>
  <p class="eyebrow">Projects</p><h1 class="h-xl" style="font-size:clamp(34px,4.4vw,56px)">Engineering depth. Digital adoption at scale.</h1>
  <p class="lead">Chmltech works at both ends of operational improvement: front-end engineering and plant reviews for process industries, and practical digital adoption plans for Canadian small and medium-sized businesses.</p>
  <div class="stat-row"><div><strong>300+</strong><span>Digital Adoption Plans for Canadian SMEs</span></div><div><strong>FEED</strong><span>commercial-scale engineering in progress</span></div><div><strong>HAZOP</strong><span>plant reviews and P&amp;ID assessments</span></div></div>
  <div class="pj-chips"><a href="#engineering">Process engineering</a><a href="#digital">Digital adoption</a><a href="#next">Work with us</a></div>
</div>{industry_art("energy-and-chemicals", "Projects")}</div></section>

<section class="section" id="engineering" style="scroll-margin-top:84px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Process engineering</p><h2 class="h-lg">From pilot plant to commercial design.</h2></div>
  <p class="lead" style="font-size:16px">Clients are described by sector to protect their confidentiality.</p></div>
  <div class="grid grid-2" style="align-items:start">{"".join(eng_card(P) for P in ENGINEERING)}</div>
</div></section>

<section class="section sand" id="digital" style="scroll-margin-top:84px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Digital adoption</p><h2 class="h-lg">300+ Digital Adoption Plans for Canadian SMEs.</h2></div>
  <p class="lead" style="font-size:16px">Each plan gives a business a clear, costed roadmap for the technology that will make the biggest difference to how it operates.</p></div>
  <div class="fig-col">{fig(DAP_FIG)}</div>
  {stats_chart()}
</div></section>

<section class="section"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Technology areas</p><h2 class="h-lg">What the plans address.</h2></div></div>
  <div class="grid grid-3">{"".join(f'<article class="card">{icon(ic)}<h3 style="font-size:20px">{esc(t)}</h3><p class="muted">{esc(d)}</p></article>' for ic, t, d in AREAS)}</div>
</div></section>

<section class="section dark" id="next" style="scroll-margin-top:84px"><div class="container feature-split">
  <div class="stack-lg"><p class="eyebrow">Work with us</p><h2 class="h-lg">From plan to results.</h2>
  <p class="lead">A plan is only the start. We also help clients carry it out: mapping and redesigning processes, selecting systems, automating workflows and building AI into daily operations.</p>
  <div class="btn-row"><a class="btn" href="book.html">Book a Strategy Call</a><a class="btn btn-ghost-dark" href="solutions.html">See all solutions</a></div></div>
  <div class="card card-dark" style="background:#11335F;border-color:#234A80;padding:30px"><h3 style="font-size:20px">Related</h3><ul class="list-check">
    <li><a href="business-process-optimization.html" style="color:#fff">Business Process Optimization</a></li>
    <li><a href="process-mapping.html" style="color:#fff">Process Mapping</a></li>
    <li><a href="ai-operating-system.html" style="color:#fff">AI Operating System</a></li>
    <li><a href="challenge-page/digital-automation-for-smes.html" style="color:#fff">Free course: Digital Automation for SMEs</a></li>
    <li><a href="energy-and-chemicals.html" style="color:#fff">Energy and chemicals</a></li></ul></div>
</div></section>'''
    page("projects.html", "Projects", "Chmltech projects: commercial-scale FEED engineering, plant reviews with HAZOP and P&ID assessment, and 300+ Digital Adoption Plans for Canadian SMEs.", b)
    fp = os.path.join(OUT, "projects.html"); s = open(fp).read()
    s = s.replace("</head>", '<link rel="stylesheet" href="assets/css/course.css">\n</head>', 1)
    s = s.replace('<script src="assets/js/main.js" defer></script>', '<script src="assets/js/main.js" defer></script>\n<script src="assets/js/figures.js" defer></script>\n<script src="assets/js/svc.js" defer></script>', 1)
    open(fp, "w").write(s)
