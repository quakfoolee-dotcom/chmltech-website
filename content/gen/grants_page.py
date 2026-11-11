"""Funding finder page (funding.html): a searchable, filterable directory of Canadian government funding programs.

Data: data/grants.json (array of records per grants/SCHEMA.md); falls back to grants/sample.json.
The full program list is server-rendered (crawlable, works without JavaScript) and the dataset is embedded as
<script type="application/json" id="grants-data"> for assets/js/grants.js, which filters by toggling the cards.
Page styles: assets/css/grants.css (gr- prefix).

Integration (build_v3.py): import grants_page; grants_page.build(globals())
"""
import json, os, datetime, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "grants.json")
SAMPLE = os.path.join(HERE, "..", "grants", "sample.json")
FNAME = "funding.html"

JURISDICTIONS = ["Federal", "British Columbia", "Alberta", "Saskatchewan", "Manitoba", "Ontario", "Quebec", "New Brunswick", "Nova Scotia",
                 "Prince Edward Island", "Newfoundland and Labrador", "Yukon", "Northwest Territories", "Nunavut"]
FUNDING_TYPES = ["Grant", "Repayable contribution", "Loan", "Tax credit", "Wage subsidy", "Equity investment", "Voucher", "Advisory service",
                 "Loan guarantee", "Rebate/Incentive"]
PURPOSES = ["Research & development", "Innovation & commercialization", "Hiring & wages", "Training & skills", "Export & trade",
            "Equipment & capital investment", "Digital adoption & technology", "Clean technology & energy efficiency", "Business expansion",
            "Startup & early stage", "Agriculture & agri-food", "Fisheries & ocean", "Tourism", "Arts, culture & media", "Manufacturing",
            "Regional & community development", "Indigenous business", "Productivity & operations"]
INDUSTRIES = ["Agriculture & agri-food", "Fisheries & aquaculture", "Forestry", "Mining & energy", "Clean technology", "Manufacturing", "Construction",
              "Retail & wholesale", "Tourism & hospitality", "Technology & digital", "Life sciences & health", "Arts, culture & media",
              "Transportation & logistics", "Professional services", "Aerospace & defence", "Automotive"]
APPLICANTS = ["Small & medium business", "Startup", "Large business", "Non-profit", "Indigenous-owned business", "Women-owned business",
              "Black-owned business", "Youth entrepreneur", "Newcomer entrepreneur", "Rural business", "Exporter", "Co-operative", "Social enterprise"]
STATUSES = ["Open", "Continuous intake", "Periodic intake", "Paused"]   # "Closed to new applications" is handled by the "Show closed" checkbox
CLOSED = "Closed to new applications"
OPEN_LIKE = {"Open", "Continuous intake"}   # periodic programs may be between intakes, so they are not counted as open
STATUS_CLS = {"Open": "open", "Continuous intake": "open", "Periodic intake": "periodic", "Paused": "periodic", CLOSED: "closed"}

esc = lambda s: H.escape(str(s or ""), quote=True)


def load():
    src = DATA if os.path.exists(DATA) else SAMPLE
    recs = json.load(open(src, encoding="utf-8"))
    recs = [r for r in recs if r.get("id") and r.get("name") and r.get("url")]
    recs.sort(key=lambda r: r["name"].lower())
    return recs, src


def _ext():
    return ('<svg class="gr-ext" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>')


def card(r):
    provs = [p for p in r.get("provinces") or [] if p != "All"]
    where = ""
    if r["jurisdiction"] == "Federal" and provs:
        where = f'<p class="gr-where">Available in: {esc(", ".join(provs))}</p>'
    types = "".join(f'<span class="gr-type">{esc(t)}</span>' for t in r.get("funding_types") or [])
    st = r.get("status") or ""
    rows = [("Eligibility", r.get("eligibility")), ("Cost share", r.get("cost_share")), ("Deadline", r.get("deadline")),
            ("Industries", ", ".join(r.get("industries") or [])), ("Who can apply", ", ".join(r.get("applicant_types") or [])),
            ("Purpose", ", ".join(r.get("purposes") or []))]
    dl = "".join(f"<div><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in rows if v)
    return f'''<article class="gr-card" id="p-{esc(r["id"])}" data-id="{esc(r["id"])}">
  <div class="gr-card-top"><span class="tag gr-jur">{esc(r["jurisdiction"])}</span><span class="gr-status gr-st-{STATUS_CLS.get(st, "closed")}">{esc(st)}</span></div>
  <h3 class="gr-name"><a href="{esc(r["url"])}" target="_blank" rel="noopener" aria-label="{esc(r["name"])} (official program page, opens in a new tab)">{esc(r["name"])}{_ext()}</a></h3>
  <p class="gr-admin">{esc(r.get("administrator"))}</p>{where}
  <div class="gr-types">{types}</div>
  <p class="gr-amount">{esc(r.get("amount_text") or "Varies")}</p>
  <p class="gr-summary">{esc(r.get("summary"))}</p>
  <details class="gr-more"><summary>Eligibility and details</summary>
    <dl>{dl}</dl>
    <p class="gr-checked">Last checked: <time datetime="{esc(r.get("source_checked"))}">{esc(r.get("source_checked"))}</time></p>
  </details>
</article>'''


def group(key, legend, values, recs_count, open_=False, note=""):
    opts = "".join(
        f'<label class="gr-opt"><input type="checkbox" name="{key}" value="{esc(v)}"><span class="gr-opt-l">{esc(v)}</span>'
        f'<span class="gr-opt-n" data-n>{recs_count.get(v, 0)}</span></label>' for v in values)
    return f'''<details class="gr-group" data-group="{key}"{" open" if open_ else ""}>
  <summary><span>{legend}</span><span class="gr-group-n" data-sel hidden></span></summary>
  <fieldset><legend class="visually-hidden">{legend}</legend>{note}<div class="gr-opts">{opts}</div></fieldset>
</details>'''


def counts(recs, field):
    c = {}
    for r in recs:
        v = r.get(field)
        for x in (v if isinstance(v, list) else [v]):
            c[x] = c.get(x, 0) + 1
    return c


def present(values, c):
    return [v for v in values if c.get(v)]


def build(ns):
    page, OUT = ns["page"], ns["OUT"]
    recs, src = load()
    n = len(recs)
    n_jur = len({r["jurisdiction"] for r in recs})
    n_open = sum(1 for r in recs if r.get("status") in OPEN_LIKE)
    latest = max((r.get("source_checked") or "" for r in recs), default="")
    try:
        reviewed = datetime.date.fromisoformat(latest).strftime("%B %Y")
    except ValueError:
        reviewed = "2026"

    cj, ct, ca, ci, cp, cs = (counts(recs, f) for f in ("jurisdiction", "funding_types", "applicant_types", "industries", "purposes", "status"))
    filters = "".join([
        group("j", "Jurisdiction", JURISDICTIONS, cj, True,
              '<label class="gr-toggle"><input type="checkbox" id="gr-fed" checked> Include federal programs</label>'
              '<p class="gr-hint">When you pick a province or territory, federal programs available there are also shown.</p>'),
        group("t", "Funding type", present(FUNDING_TYPES, ct), ct, True),
        group("a", "Who can apply", present(APPLICANTS, ca), ca),
        group("i", "Industry", present(INDUSTRIES, ci), ci, False,
              '<p class="gr-hint">Programs open to all industries are always included.</p>'),
        group("p", "Purpose", present(PURPOSES, cp), cp),
        group("s", "Status", present(STATUSES, cs), cs, False,
              f'<label class="gr-toggle"><input type="checkbox" id="gr-closed"> Show closed programs ({cs.get(CLOSED, 0)})</label>'),
    ])

    data_json = json.dumps(recs, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    site = ns.get("SITE_URL", "https://www.chmltech.com")
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Government funding programs for Canadian businesses",
          "numberOfItems": n, "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": r["name"], "url": r["url"]} for i, r in enumerate(recs)]}
    ld_json = json.dumps(ld, ensure_ascii=False).replace("<", "\\u003c")
    shown = sum(1 for r in recs if r.get("status") != CLOSED)

    search_svg = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
                  '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>')
    tips = [("Check eligibility on the official page", "Each card links to the program's official page. Read the eligibility rules, eligible costs and the application guide there before you plan around a program."),
            ("Apply before you spend", "Most grants and contributions only cover costs incurred after your application is approved. Spending first can make a cost ineligible."),
            ("Know the stacking limits", "Many programs cap the total government funding on one project, often at 50% to 75% of eligible costs. Disclose all other public funding you receive."),
            ("Keep good records", "Approved projects usually need receipts, timesheets and progress reports before claims are paid. Set up tracking from day one.")]
    tip_icons = ["shield", "calendar", "layers", "book"]
    icon = ns["icon"]

    b = f'''<section class="page-hero dark course-hero gr-hero"><div class="container"><div class="stack-lg">
  <p class="crumbs"><a href="index.html">Home</a> / Funding finder</p>
  <p class="eyebrow">Funding finder</p>
  <h1 class="h-xl" style="font-size:clamp(34px,4.4vw,56px)">Government funding for Canadian businesses</h1>
  <p class="lead">A directory of federal, provincial and territorial grants, loans, tax credits and wage subsidies for Canadian businesses. Filter by where you operate, what you need funding for and who can apply, then check the details on the official program page.</p>
  <div class="stat-row"><div><strong>{n}</strong><span>programs listed</span></div><div><strong>{n_jur}</strong><span>jurisdictions covered</span></div><div><strong>{n_open}</strong><span>open now or accepting year-round</span></div><div><strong class="gr-stat-sm">{reviewed}</strong><span>last reviewed</span></div></div>
  <div class="btn-row"><a class="btn" href="#finder">Find funding</a><a class="btn btn-ghost-dark" href="#before">Before you apply</a></div>
</div></div></section>

<section class="section gr-section" id="finder" aria-labelledby="gr-h"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Program directory</p><h2 class="h-lg" id="gr-h">Find programs that fit your business.</h2></div>
  <p>Programs closed to new applications are hidden unless you choose to show them.</p></div>
  <div class="gr-finder" id="gr-finder">
    <div class="gr-mobilebar"><button type="button" class="btn btn-ghost gr-filter-btn" aria-expanded="false" aria-controls="gr-filters">Filters<span class="gr-badge" data-active-n hidden></span></button></div>
    <aside class="gr-filters" id="gr-filters" aria-label="Filters">
      <form class="gr-form">
        <div class="gr-filters-head"><h3>Filters</h3><button type="button" class="gr-link" data-clear>Clear all filters</button></div>
        {filters}
        <button type="button" class="btn gr-apply" data-close>Show <span data-close-n>{shown}</span> programs</button>
      </form>
    </aside>
    <div class="gr-results">
      <div class="gr-toolbar">
        <label class="search gr-search"><span class="visually-hidden">Search programs</span>{search_svg}<input type="search" id="gr-q" placeholder="Search name, agency, eligibility" autocomplete="off"></label>
        <label class="gr-sort"><span>Sort by</span><select id="gr-sort"><option value="az">A to Z</option><option value="amount">Largest maximum amount</option><option value="recent">Recently verified</option></select></label>
      </div>
      <div class="gr-statusbar"><p class="gr-count" id="gr-count" role="status" aria-live="polite">{n} programs</p><button type="button" class="gr-link" data-clear hidden>Clear all filters</button></div>
      <ul class="gr-chips" aria-label="Active filters" hidden></ul>
      <div class="gr-list">
{"".join(card(r) for r in recs)}
      </div>
      <div class="gr-empty" hidden><h3>No programs match these filters.</h3><p>Try removing a filter or searching for a broader term.</p><button type="button" class="btn btn-ghost" data-clear>Clear all filters</button></div>
    </div>
  </div>
</div></section>

<section class="section sand" id="before" style="scroll-margin-top:84px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">How to use this list</p><h2 class="h-lg">Before you apply.</h2></div>
  <p>A few rules apply to most government funding programs in Canada.</p></div>
  <div class="grid grid-4">{"".join(f'<article class="card gr-tip">{icon(ic)}<h3>{esc(t)}</h3><p class="muted">{esc(d)}</p></article>' for (t, d), ic in zip(tips, tip_icons))}</div>
  <div class="card gr-disclaimer" role="note" aria-label="Disclaimer">
    <h3>Disclaimer</h3>
    <p>This directory is for general information only. Programs, amounts and deadlines change often. Always confirm details on the official program page before you apply. Chmltech is not affiliated with any government program and does not decide funding applications.</p>
    <p>Spotted an error or a program we missed? <a href="contact.html">Let us know</a> and we will review it.</p>
  </div>
</div></section>

<section class="section dark" id="next" style="scroll-margin-top:84px"><div class="container feature-split gr-cta">
  <div class="stack-lg"><p class="eyebrow">Work with us</p><h2 class="h-lg">Get your project ready for funding.</h2>
  <p class="lead">Most programs ask for a clear plan: what you will do, what it costs and what it will change. Chmltech can help you prepare a project plan, a digital adoption plan or a funding-ready business case. You remain the applicant, and funding decisions rest with each program.</p>
  <div class="btn-row"><a class="btn" href="book.html">Book a Strategy Call</a><a class="btn btn-ghost-dark" href="solutions.html">See all solutions</a></div></div>
  <div class="card card-dark gr-cta-card"><h3 style="font-size:20px">Where we can help</h3><ul class="list-check">
    <li>Project scope, budget and timeline</li>
    <li>Digital adoption plans and technology roadmaps</li>
    <li>Business cases with costs, benefits and risks</li>
    <li>Process mapping to show where the investment pays off</li></ul></div>
</div></section>
<script type="application/json" id="grants-data">{data_json}</script>
<script type="application/ld+json">{ld_json}</script>'''

    desc = ("Search and filter federal, provincial and territorial government funding for Canadian businesses: grants, loans, "
            "tax credits and wage subsidies, with eligibility, amounts and links to official program pages.")
    page(FNAME, "Funding and Grants for Canadian Businesses", desc, b, cta=False)
    fp = os.path.join(OUT, FNAME)
    s = open(fp, encoding="utf-8").read()
    s = s.replace("</head>", '<link rel="stylesheet" href="assets/css/grants.css">\n</head>', 1)
    s = s.replace('<script src="assets/js/main.js" defer></script>', '<script src="assets/js/main.js" defer></script>\n<script src="assets/js/grants.js" defer></script>', 1)
    open(fp, "w", encoding="utf-8").write(s)
    if isinstance(ns.get("ALL_PAGES"), list) and FNAME not in ns["ALL_PAGES"]:
        ns["ALL_PAGES"].append(FNAME)
    print(f"funding.html: {n} programs from {os.path.relpath(src, os.path.join(HERE, '..'))}")
