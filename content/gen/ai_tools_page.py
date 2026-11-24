"""AI Tools Landscape page (ai-tools.html): an interactive map of current AI tools with filters, a list view,
cost-per-output comparison, side-by-side compare and PNG export.

Data: assets/data/ai-tools.json, built by content/aitools/build_data.py from content/aitools/source/ai_tools_V9.json
(research + red-team method: content/aitools/SCHEMA.md and content/aitools/CHANGELOG_AI_Tools.md).
The landscape tiles are written into the HTML (so search engines and no-JS readers see every tool); assets/js/ai-tools.js
loads the data file and adds filters, the detail panel, the list, the cost view and compare; assets/js/ai-tools-charts.js
(bubble, spread, open vs paid, flow + shared chart helpers) and assets/js/ai-tools-decide.js (price ladder, category scorecard,
Canada check, vendor risk) draw the charts. Page order (V5): hero, checked banner, What it costs, Compare categories, Canada check,
landscape map (collapsed until asked for), Vendor risk + recently retired, Method/FAQ. Every caption and finding-style heading is
computed below from the data with the same rules the scripts use. Styles: assets/css/ai-tools.css
plus the gr- filter classes in assets/css/grants.css.
Logos: assets/img/ai-tools/logos/<domain>.webp, listed in logos/manifest.json (fetched by scripts/fetch_ai_logos.py);
a tool without a logo shows a monogram tile.

The page shell (header, navigation, footer) is copied from funding.html; its "AI" dropdown (content/gen/nav_ai_dropdown.py)
is re-marked with AI Tools Landscape as the current page.

Run: python3 content/gen/ai_tools_page.py   (from the site root), then content/gen/seo_pass.py .
"""
import json, os, re, html as H
import assetver

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "assets", "data", "ai-tools.json")
LOGOS = os.path.join(ROOT, "assets", "img", "ai-tools", "logos", "manifest.json")
FNAME = "ai-tools.html"
SITE = "https://www.chmltech.com"
esc = lambda s: H.escape(str(s if s is not None else ""), quote=True)

def initials(name):
    w = re.findall(r"[A-Za-z0-9]+", re.sub(r"\(.*?\)", "", name))
    if not w:
        return "?"
    return (w[0][:2] if len(w) == 1 else w[0][0] + w[1][0]).upper() if not w[0][:1].isdigit() else w[0][:2]


def shell(n):
    s = open(os.path.join(ROOT, "funding.html"), encoding="utf-8").read(); s = assetver.strip(s)
    head, rest = s.split('<main id="main">', 1)
    foot = rest.split("</main>", 1)[1]
    head = head.replace(' aria-current="page"', "")
    head = re.sub(r'<script type="application/ld\+json" data-seo="v1">.*?</script>\n?', '', head, flags=re.S)  # seo_pass writes this page's own
    import nav_ai_dropdown  # the site-wide "AI" dropdown; mark AI Tools Landscape as the current page
    head = nav_ai_dropdown.OLD_DD.sub(lambda m: nav_ai_dropdown.markup("", "tools", n), head, count=1)
    for css in ("course-finder", "erp", "assess", "funding-match"):
        head = head.replace(f'<link rel="stylesheet" href="assets/css/{css}.css">\n', '')
    head = head.replace('<link rel="stylesheet" href="assets/css/grants.css">',
                        '<link rel="stylesheet" href="assets/css/grants.css">\n<link rel="stylesheet" href="assets/css/llm.css">\n<link rel="stylesheet" href="assets/css/ai-tools.css">')
    foot = re.sub(r'<script src="assets/js/grants\.js" defer></script>\s*', '', foot)
    foot = re.sub(r'<script src="assets/js/funding-match\.js" defer></script>\s*', '', foot)
    foot = re.sub(r'<script src="https://challenges\.cloudflare\.com[^>]*></script>\s*', '', foot)
    foot = foot.replace('<script src="assets/js/main.js" defer></script>',
                        '<script src="assets/js/main.js" defer></script>\n<script src="assets/js/ai-tools-charts.js" defer></script>\n<script src="assets/js/ai-tools-decide.js" defer></script>\n<script src="assets/js/ai-tools.js" defer></script>')
    return head, foot


def meta(head, title, desc):
    full = f"{title} | Chmltech Ltd."
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(full)}</title>", head, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        head = re.sub(rf'(<meta {prop} content=")[^"]*', lambda m: m.group(1) + esc(desc), head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(full), head, count=1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + f"{SITE}/ai-tools", head, count=1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + f"{SITE}/ai-tools", head, count=1)
    return head


def group(key, legend, items, open_=False, note=""):
    opts = "".join(f'<label class="gr-opt"><input type="checkbox" name="{key}" value="{esc(v)}"><span class="gr-opt-l">{esc(l)}</span>'
                   f'<span class="gr-opt-n" data-n>{c}</span></label>' for v, l, c in items)
    return (f'<details class="gr-group" data-group="{key}"{" open" if open_ else ""}><summary><span>{legend}</span><span class="gr-group-n" data-sel hidden></span></summary>'
            f'<fieldset><legend class="visually-hidden">{legend}</legend>{note}<div class="gr-opts">{opts}</div></fieldset></details>')


PNG_ICON = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>')


def chart(cid, title, cap, wide=True, ctl="", fig="", after="", nojs="The interactive chart needs JavaScript; the caption above gives its main finding."):
    """A chart card. ctl: controls above the figure; fig: extra static markup inside .at-fig (HTML charts); after: markup after the footnote.
    The PNG button shows its label on wide cards and only the icon on narrow ones (container query in ai-tools.css); its accessible name always says what it does."""
    return (f'<figure class="ll-chartcard at-chart{" at-wide-ch" if wide else ""}" id="at-ch-{cid}"><div class="at-chhead"><div><h3>{esc(title)}</h3>'
            f'<p class="at-cap">{esc(cap)}</p></div><button type="button" class="btn btn-ghost at-pngbtn" data-png aria-label="Download PNG: {esc(title)}" title="Download PNG">'
            f'{PNG_ICON}<span class="at-pngl">Download PNG</span></button></div>{ctl}'
            f'<div class="at-fig"><div class="ll-chartnote at-chwait">{nojs}</div>{fig}</div><div class="at-figfoot"></div>{after}<div class="at-tip" hidden></div></figure>')


def build():
    D = json.load(open(DATA, encoding="utf-8"))
    T, L, C = D["tools"], D["layers"], D["categories"]
    logos = set(json.load(open(LOGOS))) if os.path.exists(LOGOS) else set()
    n = len(T)
    import hashlib
    dv = hashlib.sha1(open(DATA, 'rb').read()).hexdigest()[:8]
    n_cmp = sum(t.get("cmp") for t in T)
    n_ca = sum(1 for t in T if t.get("ca") == "yes")
    n_self = sum(1 for t in T if t.get("ca") == "self-host")
    n_cav = sum(1 for t in T if t.get("cav"))
    n_oss = sum(1 for t in T if t.get("oss"))
    cnt = lambda f: {k: sum(1 for t in T if f(t, k)) for k in []}

    # ---------- captions and headings: computed from the data with the same rules as the page scripts ----------
    # (assets/js/ai-tools-decide.js and ai-tools-charts.js recompute these in the browser; the numbers must match)
    import math, statistics as st
    rnd = lambda v: int(math.floor(v + 0.5))  # JavaScript Math.round (Python's round() rounds halves to even)
    def usd(v):
        if v >= 10: return f"${rnd(v):,}"
        c = math.floor(v * 100 + 0.5) / 100
        return f"${c:.2f}" if c % 1 else f"${int(c)}"
    def quant(a, p):
        a = sorted(a); i = (len(a) - 1) * p; lo, hi = math.floor(i), math.ceil(i)
        return a[lo] + (a[hi] - a[lo]) * (i - lo)
    def and_list(a): return a[0] if len(a) < 2 else ", ".join(a[:-1]) + " and " + a[-1]
    def pct(k, n): return rnd(100 * k / n) if n else 0
    def share(ts, f): return pct(sum(1 for t in ts if f(t)), len(ts))
    priced = lambda t: (t.get("ep") or 0) > 0 and (t.get("cur") or "USD") == "USD"
    lay = {l["id"]: [t for t in T if t["l"] == l["id"]] for l in L}
    by_cat = {c["c"]: [t for t in T if t["c"] == c["c"]] for c in C}
    # price ladder (categories with >= 6 published US-dollar prices)
    LADDER_MIN, MED_MIN, RISK_MIN = 6, 4, 8
    lad = []
    for c in C:
        ps = [t["ep"] for t in by_cat[c["c"]] if priced(t)]
        if len(ps) >= LADDER_MIN: lad.append((st.median(ps), c["c"]))
    lad.sort(key=lambda x: (x[0], x[1]))
    all_p = [t["ep"] for t in T if priced(t)]
    med_all = st.median(all_p)
    los = [c for m_, c in lad if usd(m_) == usd(lad[0][0])]; his = [c for m_, c in lad if usd(m_) == usd(lad[-1][0])]
    cap_ladder = (f"Half of the {len(all_p)} tools with a published price start at {usd(med_all)} a month or less. "
                  f"The typical plan (median of at least {LADDER_MIN} published prices) runs from {usd(lad[0][0])} ({and_list(los)}) to {usd(lad[-1][0])} ({and_list(his)}).")
    # cost-per-output spread
    ratios = []
    for c in C:
        u = {}
        for t in by_cat[c["c"]]:
            if t.get("cmp") and (t.get("cpu") or 0) > 0: u.setdefault(t["unit"], []).append(t["cpu"])
        if not u: continue
        top = sorted(u, key=lambda k: (-len(u[k]), k))[0]
        if top != "per seat per month" and len(u[top]) >= 4: ratios.append(max(u[top]) / min(u[top]))
    cap_spread = (f"In {sum(r >= 10 for r in ratios)} of {len(ratios)} categories, the dearest tool costs 10 times or more the cheapest per unit of output. "
                  "Vendors count units a little differently, so open each tool for its basis.")
    # churn per category: market events only (list clean-ups excluded)
    R = D["retired"]
    def churn(cat):
        ts = by_cat[cat]; gone = [r for r in R if r.get("ev") and r.get("cc") == cat]
        k = sum(1 for t in ts if t.get("b") in ("Acquired", "Acquisition pending", "Renamed", "Merged", "Sunsetting")) + len(gone)
        return k, len(ts) + len(gone)
    # category scorecard
    sc_open = sum(1 for c in C if sum(1 for t in by_cat[c["c"]] if "self-hosted" in t.get("dep", [])) / c["n"] >= 0.5)
    hid = sorted([c for c in C if sum(1 for t in by_cat[c["c"]] if t.get("pm") == "enterprise") / c["n"] > 0.5],
                 key=lambda c: (-sum(1 for t in by_cat[c["c"]] if t.get("pm") == "enterprise") / c["n"], c["c"]))
    hidn = [c["c"] for c in hid]
    cap_score = (f"{sc_open} of {len(C)} categories let you self-host at least half their tools; " +
                 (f"in {len(hidn)} ({', '.join(hidn[:3])}{' and ' + str(len(hidn) - 3) + ' more' if len(hidn) > 3 else ''}) most vendors hide the price behind a sales call."
                  if hidn else "in none of them do most vendors hide the price behind a sales call."))
    h_compare = f"{sc_open} of {len(C)} categories let you self-host at least half their tools; in {len(hidn)}, most prices are hidden."
    # open source vs paid, bubble
    cap_open = (f"{share(lay['L2'], lambda t: t.get('pm') in ('open-source', 'open-core'))}% of the builder stack is open source or open core; "
                f"{share(lay['L4'], lambda t: t.get('pm') == 'enterprise')}% of business-function tools only quote through sales.")
    cap_bubble = (f"Builder-stack tools are mostly free to start ({share(lay['L2'], lambda t: t.get('free'))}% have a free plan); "
                  f"business software much less so ({share(lay['L4'], lambda t: t.get('free'))}%).")
    # Canada check
    n_no = sum(1 for t in T if t.get("ca") == "no")
    n_chk = n_ca + n_self + n_no
    n_cap = sum(1 for t in T if t.get("cap"))
    cap_canada = (f"{n_ca} tools confirm Canadian data residency ({n_cap} of them only on some plans, often enterprise) and {n_self} more can be self-hosted on Canadian servers. {n_cav} tools come from Canadian companies. "
                  f"Hosting has been checked for {n_chk} of {n:,} tools so far, mostly the ones SMEs use most.")
    h_canada = f"{n_ca + n_self} of the {n_chk} tools checked so far can keep your data in Canada, on at least one plan."
    # vendor risk (categories with >= 8 current tools)
    risk = sorted([(c["c"],) + churn(c["c"]) for c in C if c["n"] >= RISK_MIN], key=lambda r: (-(r[1] / r[2]), -r[1], r[0]))
    top_share = risk[0][1] / risk[0][2]
    tops = [r for r in risk if r[1] / r[2] == top_share]
    med_share = st.median([r[1] / r[2] for r in risk])
    cap_risk = (f"{and_list([r[0] for r in tops])}: {tops[0][1]} of {tops[0][2]} tools ({pct(tops[0][1], tops[0][2])}%) saw a vendor change (acquired, renamed or merged, sunsetting, or shut down or folded in), "
                f"the highest share of the {len(risk)} categories shown; the middle category is at {rnd(100 * med_share)}%. "
                "In fast-churning categories, prefer tools that let you export your data.")
    h_risk = f"In {tops[0][0]}, {tops[0][1]} of {tops[0][2]} tools saw a vendor change: acquired, renamed, sunsetting or shut down."
    F = D["flow"]
    cap_flow = (f"{F['kept']} of the previous {F['prev_total']} tools were unchanged, {F['updated']} needed updates and {F['prev_removed']} were removed "
                f"({F['prev_removed_ev']} retired products, {F['prev_removed'] - F['prev_removed_ev']} duplicates or list clean-ups); {F['new']} new tools make up {pct(F['new'], F['total'])}% of this list.")
    n_ev = sum(1 for r in R if r.get("ev"))
    n_clean = len(R) - n_ev

    # ---------- landscape map (static, crawlable) ----------
    lay_html = []
    for lay in L:
        cards = []
        for c in [c for c in C if c["l"] == lay["id"]]:
            tiles = []
            for t in [t for t in T if t["c"] == c["c"]]:
                logo = (f'<img src="assets/img/ai-tools/logos/{esc(t["dom"])}.webp" alt="" width="28" height="28" loading="lazy" decoding="async">'
                        if t.get("logo") and t.get("dom") in logos else f'<span class="at-mono" aria-hidden="true">{esc(initials(t["n"]))}</span>')
                badge = (f'<span class="at-tb at-tb-{esc(t["b"].split()[0].lower())}" aria-hidden="true"></span><span class="visually-hidden"> ({esc(t["b"])})</span>'
                         if t.get("b") else "")
                tiles.append(f'<li><button type="button" class="at-tile" data-id="{t["id"]}" title="{esc(t["n"])} – {esc(t["d"])}">{logo}'
                             f'<span class="at-tn">{esc(t["n"])}</span>{badge}</button></li>')
            slug = re.sub(r"[^a-z0-9]+", "-", c["c"].lower()).strip("-")
            cards.append(f'<section class="at-cat{" at-wide" if c["n"] > 18 else ""}" data-cat="{esc(c["c"])}" id="cat-{slug}"><h4><span>{esc(c["c"])}</span>'
                         f'<span class="at-cn" data-catn>{c["n"]}</span></h4><ul class="at-tiles">{"".join(tiles)}</ul></section>')
        lay_html.append(f'<section class="at-layer at-{lay["id"].lower()}" data-layer="{lay["id"]}"><header class="at-lh"><span class="at-lid">{lay["id"]}</span>'
                        f'<div><h3>{esc(lay["name"])}</h3><p>{esc(lay["desc"])}</p></div></header>'
                        f'<div class="at-cats">{"".join(cards)}</div></section>')
    landscape = "".join(lay_html)

    # ---------- filters ----------
    def items(vals, f, labels=None):
        return [(v, (labels or {}).get(v, v), sum(1 for t in T if f(t, v))) for v in vals if any(f(t, v) for t in T)]
    filt = "".join([
        group("l", "Layer", [(x["id"], x["name"], sum(1 for t in T if t["l"] == x["id"])) for x in L], True),
        group("c", "Category", [(c["c"], c["c"], sum(1 for t in T if t["c"] == c["c"] or c["c"] in t.get("c2", []))) for c in C], False,
              '<p class="gr-hint">Counts include tools listed under the category as a secondary use.</p>'),
        group("pm", "Pricing", items(list(D["pm"]), lambda t, v: t.get("pm") == v, D["pm"]), True),
        group("x", "Quick picks", [
            ("free", "Has a free plan", sum(t.get("free", False) for t in T)),
            ("oss", "Open source", n_oss),
            ("cmp", "Cost per output comparable", n_cmp),
            ("self", "Can self-host", sum(1 for t in T if "self-hosted" in t.get("dep", []))),
        ], True),
        group("ca", "Canada", [
            ("ca-yes", "Data can stay in Canada (vendor cloud)", sum(1 for t in T if t.get("ca") == "yes")),
            ("ca-self", "Data in Canada if self-hosted", sum(1 for t in T if t.get("ca") == "self-host")),
            ("fr", "French interface", sum(1 for t in T if t.get("fr") == "yes")),
            ("cav", "Canadian company", n_cav),
        ], True, '<p class="gr-hint">Researched for the most-used tools; a tool not ticked here may simply be unconfirmed.</p>'),
        group("dep", "How it runs", items(list(D["dep"]), lambda t, v: v in t.get("dep", []), D["dep"])),
        group("b", "Status", [("none", "No change", sum(1 for t in T if not t.get("b"))),
                              ("Acquired", "Acquired", sum(1 for t in T if t.get("b") == "Acquired")),
                              ("Acquisition pending", "Acquisition pending", sum(1 for t in T if t.get("b") == "Acquisition pending")),
                              ("Renamed", "Renamed", sum(1 for t in T if t.get("b") in ("Renamed", "Merged"))),
                              ("Sunsetting", "Sunsetting", sum(1 for t in T if t.get("b") == "Sunsetting"))]),
    ])
    cat_opts = "".join(f'<optgroup label="{esc(l["name"])}">' + "".join(
        f'<option value="{esc(c["c"])}">{esc(c["c"])}</option>' for c in C if c["l"] == l["id"]) + "</optgroup>" for l in L)
    search_svg = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
                  '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>')
    # only real retired products, under their public names and current categories (duplicates and list clean-ups are counted, not listed)
    retired = "".join(f'<li><strong>{esc(r["pn"])}</strong> <span>{esc(r.get("cc") or "")}</span> – {esc(r.get("reason") or "")}</li>'
                      for r in sorted([r for r in R if r.get("ev")], key=lambda r: r["pn"].lower()))
    faq = [
        ("How current is this list?", f"Every tool was checked against its vendor's own website and pricing page in {D['checked']}. Prices are list prices in US dollars unless marked, and vendors change them often, so confirm on the vendor's page before you buy."),
        ("What does cost per output mean?", "For each category we picked the unit the work is paid in: a seat per month for most business software, an image, a minute of video, a million tokens, an hour of transcription, a resolved support conversation. The cost is the entry paid plan's price divided by what that plan includes, or the vendor's metered rate. Where credits are opaque, the price is contact-sales, or the plan's units are unclear, we say \"Not comparable\" instead of guessing. Prices that were promotions at check time are marked as such."),
        ("How was the list checked?", "The list was rebuilt category by category from vendors' own pages, with AI-assisted research. Two independent reviews then re-checked every website, every acquisition and shutdown claim, prices for the best-known and flagged tools, a random sample of entries, newly added tools and the Canada claims. Errors found were corrected before publishing."),
        ("What do the Canada filters mean?", "\"Data can stay in Canada\" means the vendor documents a Canadian hosting region or data-residency option for the product, sometimes only on certain plans (see the note on each tool). \"Data in Canada if self-hosted\" means you can run it on your own Canadian servers or cloud account. These were researched for the most-used tools; Unknown means not confirmed, not no."),
        ("Is Chmltech paid to list these tools?", "No. No vendor paid to be listed, and listing is not an endorsement. Product names and logos belong to their owners and are shown only to identify the products."),
        ("Which tool should my business use?", "Start with the problem, not the tool. The free Digital Assessment asks about your industry and pain points and suggests where software and AI can help; then use this map to compare options."),
    ]
    faq_html = "".join(f'<details class="at-faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Dataset", "name": "AI Tools Landscape (Chmltech)", "description": f"{n} AI tools in {len(C)} categories with pricing, cost per output and Canada data-residency notes, checked {D['checked']}.",
         "url": f"{SITE}/ai-tools", "creator": {"@type": "Organization", "name": "Chmltech Ltd."}, "dateModified": D["as_of"], 
         "variableMeasured": ["entry price (USD per month)", "cost per output unit (USD)", "free plan", "open source", "Canadian data residency", "French interface"]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}

    lay_opts = '<option value="">All layers</option>' + "".join(f'<option value="{l["id"]}">{esc(l["name"])}</option>' for l in L)
    ladder_ctl = (f'<div class="at-ctl"><label class="at-sel"><span>Layer</span><select id="atl-layer">{lay_opts}</select></label>'
                  '<div class="at-seg" role="group" aria-label="Highlight tools that"><span class="at-seg-h">Highlight:</span>'
                  '<button type="button" data-atl-h="free" aria-pressed="true">Free plan</button><button type="button" data-atl-h="oss" aria-pressed="false">Open source</button>'
                  '<button type="button" data-atl-h="cav" aria-pressed="false">Canadian company</button><button type="button" data-atl-h="" aria-pressed="false">None</button></div></div>'
                  '<div class="atl-legend"></div>')
    score_ctl = (f'<div class="at-ctl"><label class="at-sel"><span>Layer</span><select id="ats-layer">{lay_opts}</select></label><div class="ats-scale"></div>'
                 '<p class="at-ctl-hint">Select a column heading to sort, or a category to see its tools on the map.</p></div>')
    score_fig = '<div class="ats-tw" role="region" aria-label="Category scorecard (scrolls sideways)" tabindex="0"><table class="ats-t"></table></div>'
    score_after = ('<p class="ll-chartnote">Shares are of each category\'s current tools, except Vendor changes, which is a share of current plus gone tools. Typical entry is the median cheapest paid plan where at least '
                   f'{MED_MIN} tools publish a US-dollar price; medians from fewer than {LADDER_MIN} prices are in italics with the number of prices. <strong>Canada hosting</strong> counts the tools that can keep data in Canada (in the vendor\'s Canadian cloud, or self-hosted on your own '
                   'Canadian servers) out of the tools checked so far; most tools have not been checked yet, so a low number or "not checked" does not mean "not available". '
                   '<strong>Vendor changes</strong> counts current tools marked acquired, acquisition pending, renamed, merged or sunsetting, plus tools that shut down, were folded in, acquired, renamed or are being retired and are now gone; '
                   'each product counts once, and duplicates and list clean-ups are not counted.</p>')
    area_opts = '<option value="">All areas</option>' + "".join(f'<option value="{l["id"]}">{esc(l["name"])}</option>' for l in L)
    canada_ctl = ('<div class="atc-cov"></div>'
                  f'<div class="at-ctl"><label class="at-sel"><span>Area</span><select id="atc-area">{area_opts}</select></label>'
                  '<div class="atc-chips" role="group" aria-label="Show tools that are (filters combine)">'
                  '<button type="button" class="atc-chip" data-atc-f="host" aria-pressed="true">Hosted in Canada (incl. self-host)</button>'
                  '<button type="button" class="atc-chip" data-atc-f="cav" aria-pressed="false">Canadian company</button>'
                  '<button type="button" class="atc-chip" data-atc-f="fr" aria-pressed="false">French interface</button>'
                  '<button type="button" class="atc-chip" data-atc-f="free" aria-pressed="false">Free plan</button></div></div>'
                  '<div class="atc-keys"></div>')
    canada_fig = '<p class="atc-count" id="atc-count" role="status" aria-live="polite"></p><div class="atc-tw"><table class="atc-t"></table></div>'
    canada_after = ('<p class="ll-chartnote">Filters combine (a tool must meet all of the selected ones). "Hosted in Canada" means the vendor documents Canadian data residency for at least one plan, '
                    'often only enterprise plans: read the note in the tool\'s details. "Self-host" means you can run it on Canadian servers yourself. '
                    'A star marks hosting that applies only to some plans, tiers or tenants. <strong>A dash means the point has not been checked yet; it is not a "no".</strong> A blank Canadian company cell means the vendor is not Canadian. Shown: every tool with Canadian hosting, French interface or Canadian-company information.</p>'
                    '<div class="atc-cta"><p>Need data to stay in Canada for privacy rules or clients?</p><a class="btn" href="digital-assessment">Take the free Digital Assessment</a>'
                    '<p class="atc-cta-sub">We\'ll look at your industry and processes and suggest a stack that keeps your data in Canada.</p></div>')
    ca_list = sorted([t for t in T if t.get("ca") in ("yes", "self-host")], key=lambda t: t["n"].lower())
    canada_nojs = (f'<p>With JavaScript off, the {len(ca_list)} tools that can keep data in Canada are listed here (* only on some plans; '
                   '"self-host" means only if you run it yourself). Turn on JavaScript to filter them and see French-interface and Canadian-company details.</p><ul class="at-nojs-list">' +
                   "".join(f'<li>{esc(t["n"])}{" *" if t.get("cap") else ""}{" (self-host)" if t.get("ca") == "self-host" else ""}</li>' for t in ca_list) + "</ul>")
    body = f'''<section class="page-hero dark course-hero gr-hero at-hero"><div class="container"><div class="stack-lg">
  <p class="crumbs"><a href="./">Home</a> / AI tools landscape</p>
  <p class="eyebrow">AI tools landscape · {esc(D["checked"])}</p>
  <h1 class="h-xl" style="font-size:clamp(34px,4.4vw,56px)">The AI tools landscape, mapped and priced.</h1>
  <p class="lead">{n:,} current AI tools in {len(C)} categories, from the assistants and model platforms to the builder stack, agents and the business and creative apps on top. See what each kind of tool costs, compare categories, check which tools can keep your data in Canada, and put up to three tools side by side.</p>
  <div class="stat-row"><div><strong>{n:,}</strong><span>tools</span></div><div><strong>{usd(med_all)}</strong><span>typical cheapest paid plan a month</span></div><div><strong>{n_cmp}</strong><span>with comparable cost per output</span></div><div><a class="at-statlink" href="#canada"><strong>{n_ca}</strong><span>offer hosting in Canada on at least one plan (+{n_self} if self-hosted)</span></a></div></div>
  <div class="btn-row"><a class="btn" href="#costs">What it costs</a><a class="btn btn-ghost-dark" href="#canada">Canada check</a><a class="btn btn-ghost-dark" href="#map">Explore the map</a></div>
</div></div></section>

<div class="at-banner"><div class="container"><p><strong>Checked {esc(D["checked"])}.</strong> Every tool was re-checked against its vendor's own site, then by an independent reviewer. {F["new"]} of the {n:,} tools ({pct(F["new"], F["total"])}%) are new since the previous list (<a href="#at-ch-flow">how the list changed</a>). {n_ev} earlier tools have shut down, been folded in, acquired, renamed or are being retired: <a href="#retired">see which</a>.</p></div></div>

<section class="section at-sec" id="costs" aria-labelledby="at-costs-h"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">What it costs</p><h2 class="h-lg" id="at-costs-h">Half of priced AI tools start at {usd(med_all)} a month or less.</h2></div>
  <p>The price ladder shows every published entry price by category; the spread shows how far apart tools doing the same job are; the calculator turns that into a monthly estimate. Select any dot to open the tool.</p></div>
  <div class="at-chgrid">
  {chart("ladder", "What a paid plan costs in each category", cap_ladder, True, ladder_ctl)}
  {chart("spread", "Same job, very different cost", cap_spread)}
  </div>
  <div class="at-costwrap" id="cost">
  <h3 class="at-subh" id="at-cost-h">What will the work cost each month?</h3>
  <p class="at-subp">Pick a category and enter how much work you expect. Tools are ranked on their entry plan's cost per unit, scaled to your volume. Plans have minimums and caps, so treat this as a first cut and check the shortlisted vendors' pricing pages.</p>
  <div class="ll-chartcard at-costcard" role="region" aria-labelledby="at-cost-h">
    <div class="at-costctl">
      <label class="gr-sort"><span>Category</span><select id="at-cost-cat">{cat_opts}</select></label>
      <label class="gr-sort" hidden><span>Priced</span><select id="at-cost-usel"></select></label>
      <label class="gr-sort at-vol"><span id="at-cost-unit">Volume per month</span><input type="number" id="at-cost-vol" min="0" max="1000000000" step="any" inputmode="decimal" value="10"></label>
      <label class="gr-toggle"><input type="checkbox" id="at-cost-free"> Only tools with a free plan</label>
    </div>
    <p class="ls-cap" id="at-cost-cap" aria-live="polite"></p>
    <div class="at-bars" id="at-cost-bars"></div>
    <p class="ll-chartnote" id="at-cost-note"></p>
  </div>
  </div>
</div></section>

<section class="section sand at-sec" id="compare" aria-labelledby="at-cmp-sec-h"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Compare categories</p><h2 class="h-lg" id="at-cmp-sec-h">{esc(h_compare)}</h2></div>
  <p>Before you shortlist, see what kind of market you are shopping in: free to try, open source, self-hostable, sales-led, Canadian, stable. Drawn from the same data as the map.</p></div>
  <div class="at-chgrid at-cmpgrid">
  {chart("score", "Category scorecard: how free, open and Canadian each market is", cap_score, True, score_ctl, score_fig, score_after)}
  {chart("open", "Open source versus paid, by layer", cap_open, False)}
  {chart("bubble", "Where each category sits on price and free access", cap_bubble, False)}
  </div>
</div></section>

<section class="section at-sec" id="canada" aria-labelledby="at-ca-h"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Canada check</p><h2 class="h-lg" id="at-ca-h">{esc(h_canada)}</h2></div>
  <p>If privacy rules, a client contract or public-sector work mean data must stay in Canada, start here. Hosting has been checked for the most-used tools first; the bar shows how far the checks go.</p></div>
  {chart("canada", "Which AI tools can keep your data in Canada?", cap_canada, True, canada_ctl, canada_fig, canada_after, canada_nojs)}
</div></section>

<section class="section sand gr-section" id="map" style="scroll-margin-top:84px" aria-labelledby="at-h"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Landscape map</p><h2 class="h-lg" id="at-h">Five layers, {len(C)} categories, {n:,} tools.</h2></div>
  <p>Browse every tool. Start with the foundation models and work down to the business and creative apps, or jump to the layer you need. Select any tool for its price, cost per output, Canada notes and sources. Use the filters to narrow the map; switch to the list to sort by price.</p></div>
  <div class="gr-finder at-root" id="at-root" data-src="assets/data/ai-tools.json?v={dv}">
    <div class="gr-mobilebar"><button type="button" class="btn btn-ghost gr-filter-btn" aria-expanded="false" aria-controls="gr-filters">Filters<span class="gr-badge" data-active-n hidden></span></button></div>
    <aside class="gr-filters" id="gr-filters" aria-label="Filters">
      <form class="gr-form">
        <div class="gr-filters-head"><h3>Filters</h3><button type="button" class="gr-link" data-clear>Clear all filters</button></div>
        {filt}
        <button type="button" class="btn gr-apply" data-close>Show <span data-close-n>{n}</span> tools</button>
      </form>
    </aside>
    <div class="gr-results">
      <div class="gr-toolbar">
        <label class="search gr-search"><span class="visually-hidden">Search tools</span>{search_svg}<input type="search" id="at-q" placeholder="Search a tool, company or task (e.g. transcription, invoices)" autocomplete="off"></label>
      </div>
      <div class="at-controls">
        <div class="ll-tabs at-tabs" role="group" aria-label="View"><button type="button" class="ll-tab" data-view="map" aria-pressed="true" aria-controls="at-panel-map">Map</button><button type="button" class="ll-tab" data-view="list" aria-pressed="false" aria-controls="at-panel-list">List</button></div>
        <button type="button" class="btn btn-ghost at-png" id="at-png">Download map as PNG</button>
      </div>
      <div class="gr-statusbar"><p class="gr-count" id="at-count" role="status" aria-live="polite">{n:,} tools</p>
        <button type="button" class="gr-link" data-clear hidden>Clear all filters</button></div>
      <ul class="gr-chips" aria-label="Active filters" hidden></ul>
      <p class="at-maplegend" id="at-maplegend"><span><span class="at-tb at-tb-acquired" aria-hidden="true"></span> Acquired, acquisition pending or renamed</span><span><span class="at-tb at-tb-sunsetting" aria-hidden="true"></span> Sunsetting</span><span>Select any tile for details</span></p>
      <div id="at-panel-map" class="at-map">{landscape}</div>
      <div class="at-mapmore" id="at-mapmore-wrap" hidden><button type="button" class="btn btn-ghost" id="at-mapmore" aria-controls="at-panel-map" aria-expanded="false">Show the full map ({n:,} tools)</button></div>
      <div id="at-panel-list" hidden><div class="ll-tablewrap"><table class="ll-table at-table"><thead><tr>
        <th scope="col"><button type="button" class="ll-th" data-sort="n">Tool</button></th>
        <th scope="col" class="at-hide-m"><button type="button" class="ll-th" data-sort="c">Category</button></th>
        <th scope="col" class="num"><button type="button" class="ll-th" data-sort="ep">From (USD/mo)</button></th>
        <th scope="col" class="num"><button type="button" class="ll-th" data-sort="cpu">Cost per output</button></th>
        <th scope="col"><span class="at-hide-m">Free · Open · Canada · </span>Compare</th>
      </tr></thead><tbody id="at-tbody"></tbody></table></div>
      <p class="ll-chartnote" id="at-cpu-note" hidden>Sorting by cost per output groups tools by their unit (per seat, per image, per 1M tokens…), because costs on different units can't be ranked against each other.</p>
      <p class="ll-chartnote">Prices are list prices in US dollars as published in {esc(D["checked"])}; "From" is the cheapest paid plan (some are billed annually; see each tool). Cost per output compares like with like only within a category.</p></div>
      <div class="gr-empty" id="at-empty" hidden><h3>No tools match these filters.</h3><p>Try removing a filter or a broader search term.</p><button type="button" class="btn btn-ghost" data-clear>Clear all filters</button></div>
    </div>
  </div>
</div></section>

<section class="section at-sec" id="risk" aria-labelledby="at-risk-h"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Vendor risk</p><h2 class="h-lg" id="at-risk-h">{esc(h_risk)}</h2></div>
  <p>AI vendors are bought, renamed and shut down often. Check how much a category has moved before you build a process on one tool, and keep a way to export your data.</p></div>
  <div class="atr-grid">
  {chart("risk", "Vendor changes by category: acquired, renamed, sunsetting or shut down", cap_risk, True)}
  <div class="ll-chartcard atr-retired" id="retired" aria-labelledby="atr-ret-h"><h3 id="atr-ret-h">Recently retired</h3>
  <p class="at-cap">{n_ev} tools from earlier versions of this list have shut down, been folded into another product, acquired, renamed or are being retired. Not listed: {n_clean} more entries removed in {esc(D["checked"])} as duplicates of other entries or in list clean-up (not AI products, out of scope). Of all {len(R)} removed entries, {F["prev_removed"]} were on the previous list.</p>
  <div class="atr-list" role="region" aria-label="Retired tools" tabindex="0"><ul>{retired}</ul></div></div>
  </div>
</div></section>

<section class="section sand" id="faq"><div class="container at-faqwrap">
  <div class="section-head"><div class="stack"><p class="eyebrow">Method and FAQ</p><h2 class="h-lg">How this map is built.</h2></div></div>
  {chart("flow", "How this list changed from the previous one", cap_flow)}
  {faq_html}
  <div class="at-cta card"><div><h3>Not sure which tools your business needs?</h3><p>The free Digital Assessment looks at your industry and problems first, then suggests where software and AI can help. For model choices behind these tools, see the AI Models leaderboard.</p></div>
  <div class="btn-row"><a class="btn" href="digital-assessment">Start the free assessment</a><a class="btn btn-ghost" href="llm-leaderboard">AI Models leaderboard</a></div></div>
  <p class="at-legal">Product names, logos and trademarks belong to their owners and are used only to identify the products. Listing is not an endorsement, and no vendor paid to be listed.</p>
</div></section>

<div class="at-tray" id="at-tray" hidden><div class="container"><span id="at-tray-list"></span><button type="button" class="btn" id="at-tray-go">Compare</button><button type="button" class="gr-link" id="at-tray-clear">Clear</button></div></div>
<dialog class="at-drawer" id="at-drawer" aria-labelledby="at-d-name"><div class="at-d-in" id="at-d-body"></div></dialog>
<dialog class="at-cmp" id="at-cmp" aria-labelledby="at-cmp-h"><div class="at-d-in"><div class="at-d-top"><h2 id="at-cmp-h">Compare</h2><button type="button" class="at-x" data-x aria-label="Close">×</button></div><div id="at-cmp-body"></div></div></dialog>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")}</script>'''

    head, foot = shell(n)
    desc = (f"Interactive map of {n:,} current AI tools in {len(C)} categories, checked {D['checked']}: assistants, agents, builder stack, business and creative apps. "
            "Filter by price, open source and Canadian data residency; compare cost per output.")
    head = meta(head, "AI Tools Landscape 2026: Map, Prices and Cost per Output", desc)
    open(os.path.join(ROOT, FNAME), "w", encoding="utf-8").write(head + '<main id="main">\n' + body + "\n</main>" + foot)
    print(f"wrote {FNAME}: {n} tools, logos {len(logos)}")


if __name__ == "__main__":
    build()
