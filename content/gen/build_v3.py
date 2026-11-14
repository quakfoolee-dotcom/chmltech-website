"""Chmltech website V3 builder: V2 base pages + all content migrated from Wix.
usage: python3 build_v3.py <out_dir> <wix_data_dir>
"""
import os, sys, re, json, glob, html as H, datetime
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aios import aios_svg, AIOS_CSS, COMPONENTS, PHASES, BENEFITS, FAQ as AIOS_FAQ
from courses_build import render_course, finalize_course_file, course_stats
import service_pages, industry_pages, journal_pages, privacy_page, new_articles, projects_page, grants_page

OUT, DATA = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
WIX = os.path.dirname(DATA.rstrip('/'))
WIX_HOST = "https://www.chmltech-consulting.com"

# ---------------------------------------------------------------- base (V2) pages, with slugs aligned to Wix URLs
src = open(os.path.join(HERE, "build.py")).read()
for a, b in [
    ('("energy-chemicals",', '("energy-and-chemicals",'),
    ('("distribution-warehousing",', '("distribution-and-warehousing",'),
    ('("iso-9001",', '("iso9001",'),
    # V4.23: no trademarked growth method; the unverifiable Wix-template testimonial is removed
    ('("scaling-up","Scaling Up","layers","Grow without the growing pains. We help leadership teams align strategy, people, execution and cash so the business can scale with control."',
     '("scaling-up","Scaling Your Business","layers","Grow without the growing pains. We help you build the processes, systems, roles and cash discipline to scale with control."'),
    ("QUOTE = '''", "QUOTE = '' and '''"),
    ('("ai-solutions",', '("artificial-intelligence",'),
    ("industries.html#{s}", "{s}.html"),
    ('solutions.html#{s}">{t}<span', '{s}.html">{t}<span'),
    ("        <!-- TODO: confirm exact testimonial wording from the current site -->\n", ""),
    ('SERVICE_OPTIONS = ["AI Readiness &amp; AI Strategy"', 'SERVICE_OPTIONS = ["Corporate Strategy session (1 hr, CA$450)","Operational Consulting session (1 hr, CA$350)","Project Management session (1 hr, CA$250)","AI Readiness &amp; AI Strategy"'),
    ('<span>© <span data-year>2026</span> Chmltech Ltd. All rights reserved.</span>', '<span>© <span data-year>2026</span> Chmltech Ltd. All rights reserved. · <a href="privacy.html">Privacy</a></span>'),
    (r'f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")', r'f.write(f"User-agent: *\nAllow: /\nDisallow: /assets/journal/pdf/\nSitemap: {SITE_URL}/sitemap.xml\n")'),
    ('<a href="courses.html">Courses</a>\n      <a href="insights.html">Insights</a>', '<a href="courses.html">Free courses</a>\n      <a href="training.html">Free practice exams</a>\n      <a href="insights.html">Insights</a>\n      <a href="funding.html">Funding finder</a>\n      <a href="projects.html">Projects</a>\n      <a href="about.html">About Chmltech</a>'),
    # V4.27: funding finder in the primary navigation
    ('("courses.html","Courses"),("contact.html","Contact")]', '("courses.html","Courses"),("llm-leaderboard.html","AI Models"),("funding.html","Funding"),("about.html","About"),("contact.html","Contact")]'),  # V4.37: About in the menu
]:
    assert a in src, a
    src = src.replace(a, b)
ns = {"__name__": "base"}
sys.argv = [sys.argv[0], OUT]
exec(compile(src, "build.py", "exec"), ns)
page, page_hero, icon, CTA, QUOTE = ns["page"], ns["page_hero"], ns["icon"], ns["CTA"], ns["QUOTE"]
INDUSTRIES, SOLUTIONS, CORE, steps_html = ns["INDUSTRIES"], ns["SOLUTIONS"], ns["CORE"], ns["steps_html"]
FORM_ENDPOINT, SITE_URL = ns["FORM_ENDPOINT"], ns["SITE_URL"]
esc = lambda s: H.escape(s or "", quote=True)

ALL_PAGES = ["", "industries.html", "solutions.html", "training.html", "insights.html", "courses.html", "book.html", "contact.html", "about.html"]

def sub_page(fname, *a, **kw):
    """page() for files in sub-folders: rewrite relative links with ../ prefixes."""
    os.makedirs(os.path.dirname(os.path.join(OUT, fname)), exist_ok=True)
    page(fname, *a, **kw)
    depth = fname.count("/")
    if depth:
        p = os.path.join(OUT, fname); s = open(p).read(); pre = "../" * depth
        s = re.sub(r'(\s(?:href|src))="(?!https?:|mailto:|tel:|#|data:|/|\.\./)([^"]*)"', lambda m: f'{m.group(1)}="{pre}{m.group(2)}"', s)
        open(p, "w").write(s)
    ALL_PAGES.append(fname)

def redirect(fname, target, title="Moved"):
    depth = fname.count("/"); pre = "../" * depth
    os.makedirs(os.path.dirname(os.path.join(OUT, fname)) or OUT, exist_ok=True)
    open(os.path.join(OUT, fname), "w").write(f'''<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><title>{title} | Chmltech Ltd.</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{SITE_URL}/{target}">
<meta http-equiv="refresh" content="0; url={pre}{target}"><script>location.replace("{pre}{target}"+location.search+location.hash)</script></head>
<body><p>This page has moved to <a href="{pre}{target}">{pre}{target}</a>.</p></body></html>''')

# ---------------------------------------------------------------- media handling
MEDIA_RE = re.compile(r'https://static\.wixstatic\.com/media/([^"\'\s/?#]+)')
STOCK_PREFIXES = ("11062b_",)            # Wix free media library: licensed for Wix sites only
needed_media, dropped_media = set(), Counter()

def media_local(mid, prefix):
    mid = mid.replace("%7E", "~")
    if not mid.startswith(("33d8e3_", "nsplsh_")):   # keep only Chmltech's own uploads and Unsplash photos
        dropped_media[mid] += 1; return None
    needed_media.add(mid)
    base, ext = os.path.splitext(mid)
    ext = ext.lower() if ext.lower() in (".jpg", ".jpeg", ".png", ".gif", ".webp") else ".jpg"
    if ext == ".jpeg": ext = ".jpg"
    if ext in (".gif",): ext = ".gif"
    return f"{prefix}assets/media/{local_name(mid)}"

def local_name(mid):
    base, ext = os.path.splitext(mid.replace("%7E", "~"))
    e = ext.lower()
    e = ".jpg" if e in (".jpeg", ".jfif", "") else e
    if e not in (".jpg", ".png", ".gif", ".webp"): e = ".jpg"
    return re.sub(r"[^A-Za-z0-9_.-]", "-", base.replace("~mv2", "")) + e

def fix_links(s, prefix, post_slugs):
    def repl(m):
        h = m.group(1)
        mm = re.match(r'https?://(?:www\.)?chmltech-consulting\.com(/[^"#?]*)?([?#][^"]*)?$', h)
        if not mm: return m.group(0)
        path = (mm.group(1) or "/").strip("/")
        if path.startswith("post/"):
            slug = path[5:]
            return f'href="{prefix}post/{slug}.html"' if slug in post_slugs else f'href="{prefix}insights.html"'
        if path.startswith(("insights/hashtags", "insights/tags", "blog", "insights")) and not path.startswith("insights/categories/"): return f'href="{prefix}insights.html"'
        if path.startswith("insights/categories/"): return f'href="{prefix}insights.html#cat={path.split("/")[-1]}"'
        if path in ("", "home"): return f'href="{prefix}index.html"'
        if path in ("challenges", "plans-pricing"): return f'href="{prefix}courses.html"'
        if path == "book-online": return f'href="{prefix}book.html"'
        return f'href="{prefix}{path}.html"'
    return re.sub(r'href="([^"]+)"', repl, s)

def clean_html(s, prefix, post_slugs, demote_h1=True):
    s = s.replace("​", "").replace("﻿", "")
    for _ in range(4):
        s = re.sub(r"<strong>\s*<strong>(.*?)</strong>\s*</strong>", r"<strong>\1</strong>", s, flags=re.S)
        s = re.sub(r"<em>\s*<em>(.*?)</em>\s*</em>", r"<em>\1</em>", s, flags=re.S)
    s = re.sub(r"<(strong|em)>\s*</\1>", " ", s)
    s = re.sub(r"<p>(\s|&nbsp;|<br>)*</p>", "", s)
    s = re.sub(r"(<br>\s*){2,}", "<br>", s)
    s = re.sub(r"(^|>)\s*<br>", r"\1", s)
    s = re.sub(r"<li>\s*<p>(.*?)</p>\s*</li>", r"<li>\1</li>", s, flags=re.S)
    if demote_h1:
        s = re.sub(r"<(/?)h1>", r"<\1h2>", s)
    # images
    def img(m):
        tag = m.group(0); mm = MEDIA_RE.search(tag)
        if not mm:
            return "" if 'src="quality_auto' in tag or 'src=""' in tag else tag
        loc = media_local(mm.group(1), prefix)
        if not loc: return ""
        alt = re.search(r'alt="([^"]*)"', tag); alt = alt.group(1) if alt else ""
        alt = "" if re.search(r"\.(png|jpe?g|jfif|webp)$", alt, re.I) else alt
        return f'<img src="{loc}" alt="{alt}" loading="lazy" decoding="async">'
    s = re.sub(r"<img [^>]*>", img, s)
    s = re.sub(r"<figure>\s*</figure>", "", s)
    s = fix_links(s, prefix, post_slugs)
    s = re.sub(r'<a href="([^"]+)">', lambda m: f'<a href="{m.group(1)}" rel="noopener" target="_blank">' if m.group(1).startswith("http") else m.group(0), s)
    s = re.sub(r"\n{2,}", "\n", s)
    return s.strip()

def text_excerpt(html_s, n=180):
    t = re.sub(r"<[^>]+>", " ", html_s); t = H.unescape(re.sub(r"\s+", " ", t)).strip()
    return (t[:n].rsplit(" ", 1)[0] + "…") if len(t) > n else t

# ---------------------------------------------------------------- load Wix data
def load(kind):
    out = {}
    for f in sorted(glob.glob(os.path.join(DATA, kind, "*.json"))):
        d = json.load(open(f)); out[d["slug"]] = d
    return out
posts_raw, pages_raw, programs_raw, services_raw = load("post"), load("page"), load("program"), load("service")

cat_map = json.load(open(os.path.join(WIX, "categories.json"))) if os.path.exists(os.path.join(WIX, "categories.json")) else {}
CAT_NAMES = {"esg": "ESG", "lean": "Lean", "six-sigma": "Six Sigma", "process-engineering": "Process Engineering", "process-improvement": "Process Improvement", "agile": "Agile", "iso": "ISO",
             "change-management": "Change Management", "project-management": "Project Management", "case-study": "Case Study", "inventory-management": "Inventory Management",
             "operational-efficiency": "Operational Efficiency", "marketing": "Sales & Marketing", "artificial-intelligence": "Artificial Intelligence",
             "artificial-intelligence-1": "Artificial Intelligence", "erp": "ERP", "digital-technology": "Digital Technology",
             "clean-energy": "Chmltech Online Journal", "chmltech-online-journal": "Chmltech Online Journal", "strategy": "Strategy", "book-review": "Book Review"}
# Wix category slugs that are shown under another key (V4.18: the journal was stored by Wix as "clean-energy")
CAT_ALIAS = {"artificial-intelligence-1": "artificial-intelligence", "clean-energy": "chmltech-online-journal"}
post_cats = defaultdict(list)
for cslug, info in cat_map.items():
    if cslug not in CAT_NAMES: continue
    key = CAT_ALIAS.get(cslug, cslug)
    for ps in info.get("posts", []):
        if key not in post_cats[ps]: post_cats[ps].append(key)

def ld_of(d, typ):
    for x in d.get("ld", []):
        if isinstance(x, dict) and x.get("@type") == typ: return x
    return {}

POSTS = []
post_slugs = set(posts_raw)
for slug, d in posts_raw.items():
    if len(d.get("html", "")) < 200: continue
    ld = ld_of(d, "BlogPosting")
    title = d.get("h1") or ld.get("headline") or d["title"].split(" | ")[0]
    date = (d.get("published") or ld.get("datePublished") or "")[:10]
    img = ld.get("image", {}); img = img.get("url") if isinstance(img, dict) else (img if isinstance(img, str) else "")
    cover = None
    m = MEDIA_RE.search(img or d.get("ogImage", "") or "")
    if m: cover = m.group(1)
    if not cover or not cover.replace("%7E", "~").startswith(("33d8e3_", "nsplsh_")):
        cover = next((x for x in MEDIA_RE.findall(d["html"]) if x.replace("%7E", "~").startswith(("33d8e3_", "nsplsh_"))), None)
    body = clean_html(d["html"], "../", post_slugs)
    if cover:  # don't repeat the cover: drop the article's first image when it is the cover photo
        ln = local_name(cover)
        body = re.sub(r'<figure><img src="\.\./assets/media/' + re.escape(ln) + r'"[^>]*></figure>', "", body, count=1)
    if not cover:
        m2 = re.search(r'src="\.\./assets/media/([^"]+)"', body)
    POSTS.append(dict(slug=slug, title=title, date=date, author="Quak Foo Lee",  # V4.23: Wix bylines (template names and "ESG Consultant") re-credited to the author
                      read=d.get("readTime", ""), desc=d.get("description", ""), cover=cover, body=body,
                      cats=post_cats.get(slug, []), tags=d.get("tags", [])[:10]))
POSTS.sort(key=lambda p: p["date"], reverse=True)
new_articles.add_posts(POSTS)  # Insights articles written for this site (V4.20)
journal_pages.add_new_posts(POSTS)  # journal papers written for this site (V4.14)

# fallback categories from keywords when the category map is incomplete
KW = [("artificial-intelligence", r"\bAI\b|artificial intelligence|machine learning|agent|LLM|GPT"), ("lean", r"\blean\b|kaizen|5S|waste|value stream"),
      ("six-sigma", r"six sigma|DMAIC"), ("marketing", r"\bSEO\b|marketing|sales|brand|social media|content|instagram|GEO\b"),
      ("project-management", r"project management|portfolio|PPM|\bPMP\b|agile|scrum"), ("erp", r"\bERP\b|\bMRP\b|inventory management software|WMS"),
      ("iso", r"\bISO\b|quality management"), ("change-management", r"change management|change model"), ("book-review", r"book review|deep dive review|\bby [A-Z][a-z]+ [A-Z]"),
      ("esg", r"\bESG\b|sustainab|hydrogen|clean energy|carbon"), ("strategy", r"strategy|strategic"), ("digital-technology", r"digital|automation|software|data")]
for p in POSTS:
    if not p["cats"]:
        hay = p["title"] + " " + p["desc"] + " " + " ".join(p["tags"])
        # Book Review is decided from the title only: "by Firstname Lastname" in a description wrongly matched (V4.22)
        p["cats"] = [k for k, rx in KW if re.search(rx, p["title"] if k == "book-review" else hay, re.I)][:3] or ["operational-efficiency"]
CAT_COUNT = Counter(c for p in POSTS for c in p["cats"])
for p in POSTS:
    p["gen"] = not (p["cover"] and p["cover"].replace("%7E", "~").startswith(("33d8e3_", "nsplsh_")))
json.dump([{"slug": p["slug"], "title": p["title"], "cat": CAT_NAMES[p["cats"][0]]} for p in POSTS if p["gen"]],
          open(os.path.join(WIX, "gen_covers.json"), "w"), indent=1)
JOURNAL = journal_pages.apply_to_posts(POSTS)  # real paper titles, descriptions and read times (V4.12)
CAT_COUNT = Counter(c for p in POSTS for c in p["cats"])  # journal papers get journal + subject categories (V4.18)

def nice_date(d):
    try: return datetime.date.fromisoformat(d).strftime("%b %-d, %Y")
    except Exception: return d

def thumb(p, prefix):
    if p.get("gen"): return f"{prefix}assets/media/covers/thumbs/{p['slug']}.jpg"
    if p["cover"]:
        loc = media_local(p["cover"], prefix)
        if loc: return loc.replace("assets/media/", "assets/media/thumbs/")
    return None

def card(p, prefix=""):
    t = thumb(p, prefix)
    art = f'<div class="thumb"><img src="{t}" alt="" loading="lazy" decoding="async" width="600" height="338"></div>' if t else f'<div class="art">{icon("book", "")}</div>'
    main = next((c for c in p["cats"] if c != "chmltech-online-journal"), p["cats"][0])
    cats = f'<p class="cat-label">{esc(CAT_NAMES[main])}</p>'
    return (f'<article class="article" data-cats="{" ".join(p["cats"])}" data-search="{esc((p["title"] + " " + p["desc"] + " " + " ".join(p["tags"])).lower())}">{art}'
            f'<div class="body">{cats}<h3><a href="{prefix}post/{p["slug"]}.html">{esc(p["title"])}</a></h3>'
            f'<p class="muted">{esc(text_excerpt(p["desc"] or p["body"], 150))}</p><p class="meta">{esc(p["journal"]) + " · " if p.get("journal") else ""}{nice_date(p["date"])}{" · " + esc(p["read"]) if p["read"] else ""}</p></div></article>')

SEARCH_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'

# ---------------------------------------------------------------- INSIGHTS index
cat_order = sorted(CAT_COUNT, key=lambda c: -CAT_COUNT[c])
chips = '<button class="chip" type="button" data-cat="all" aria-pressed="true">All (' + str(len(POSTS)) + ')</button>' + "".join(
    f'<button class="chip" type="button" data-cat="{c}" aria-pressed="false">{esc(CAT_NAMES[c])} ({CAT_COUNT[c]})</button>' for c in cat_order)
ins = page_hero("Insights", "Insights", "Ideas on AI, systems and operational excellence.",
                f"{len(POSTS)} articles on AI, digital transformation, Lean, Six Sigma, project management, ERP, strategy and more, written for owners and leadership teams of Canadian SMEs.")
ins += f'''
<section class="section" style="padding-top:64px"><div class="container" data-list="posts" data-page-size="24">
  <div class="toolbar">
    <label class="search"><span class="visually-hidden">Search articles</span>{SEARCH_SVG}<input type="search" placeholder="Search {len(POSTS)} articles" data-search-input></label>
    <span class="count" data-count aria-live="polite">{len(POSTS)} articles</span>
  </div>
  <div class="chips" role="group" aria-label="Filter by category">{chips}</div>
  <div class="grid grid-3" data-items>
  {"".join(card(p) for p in POSTS)}
  </div>
  <p class="empty" data-empty>No articles match your search.</p>
  <div class="more-wrap"><button class="btn btn-ghost" type="button" data-more>Show more articles</button></div>
</div></section>
<section class="section sand"><div class="container grid grid-2" style="align-items:center">
  <div class="stack"><p class="eyebrow">Stay informed</p><h2 class="h-lg">Get new insights by email.</h2><p class="muted">Occasional articles on AI, digital transformation and operational excellence. No spam; unsubscribe any time.</p></div>
  <form class="panel form" data-endpoint="{FORM_ENDPOINT}" data-subject="Insights subscription" data-success="Thanks for subscribing. You will hear from us when new insights are published." novalidate>
    <input class="hp" type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">
    <input type="hidden" name="form" value="Insights subscription">
    <div class="field"><label for="sub-name">Name</label><input id="sub-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="sub-email">Work email</label><input id="sub-email" name="email" type="email" autocomplete="email" required></div>
    <label class="check"><input type="checkbox" name="consent" value="yes" required> I agree to receive emails from Chmltech Ltd.</label>
    <div><button class="btn" type="submit">Subscribe</button></div>
    <p class="form-status" role="status" tabindex="-1"></p>
  </form>
</div></section>'''
page("insights.html", "Insights", f"{len(POSTS)} articles from Chmltech Ltd. on AI, digital transformation, Lean, Six Sigma, project management, ERP and strategy for Canadian SMEs.", ins)

# category URLs from Wix -> filtered insights page
for c in CAT_NAMES:
    redirect(f"insights/categories/{c}.html", f"insights.html#cat={CAT_ALIAS.get(c, c)}", CAT_NAMES[c])

# ---------------------------------------------------------------- ARTICLE pages
by_cat = defaultdict(list)
for p in POSTS:
    for c in p["cats"]: by_cat[c].append(p)
for i, p in enumerate(POSTS):
    rel = []
    for c in p["cats"]:
        rel += [q for q in by_cat[c] if q["slug"] != p["slug"] and q not in rel]
    rel = (rel + [q for q in POSTS if q["slug"] != p["slug"] and q not in rel])[:3]
    cover = f"../assets/media/covers/{p['slug']}.jpg" if p.get("gen") else (media_local(p["cover"], "../") if p["cover"] else None)
    cats = "".join(f'<a href="../insights.html#cat={c}">{esc(CAT_NAMES[c])}</a>' for c in p["cats"])
    tags = "".join(f'<span>{esc(t)}</span>' for t in p["tags"])
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "datePublished": p["date"],
          "author": {"@type": "Person", "name": p["author"]}, "publisher": {"@type": "Organization", "name": "Chmltech Ltd."},
          "mainEntityOfPage": f"{SITE_URL}/post/{p['slug']}", "description": p["desc"]}
    body = f'''<section class="page-hero dark" style="padding-bottom:{'110px' if cover and not p.get("gen") else '72px'}">
  <div class="container stack-lg">
    <p class="crumbs"><a href="index.html">Home</a> / <a href="insights.html">Insights</a></p>
    <div class="tags">{cats}</div>
    <h1 class="h-xl" style="font-size:clamp(34px,4.4vw,54px)">{esc(p["title"])}</h1>
    <p class="post-meta"><span>{esc(p["author"])}</span><span>{nice_date(p["date"])}</span>{f'<span>{esc(p["read"])}</span>' if p["read"] else ''}</p>
  </div>
</section>
{f'<div class="container post-cover"><img src="{cover}" alt="" width="1200" height="520"></div>' if cover and not p.get("gen") else ''}
<section class="section" style="padding-top:56px"><div class="container layout-aside">
  <article class="prose">
{p["body"]}
  </article>
  <aside class="aside-sticky">
    <div class="card card-dark" style="padding:28px"><p class="eyebrow">Work with Chmltech</p><h3 style="font-size:22px">Want help applying this?</h3><p>Book a strategy call to talk through your goals and where to start.</p><a class="btn" href="book.html" style="align-self:flex-start">Book a Strategy Call</a></div>
    {f'<div class="card" style="padding:24px"><p class="eyebrow">Tags</p><div class="tags">{tags}</div></div>' if tags else ''}
  </aside>
</div></section>
<section class="section sand"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Keep reading</p><h2 class="h-lg">Related articles</h2></div><a class="btn btn-ghost" href="insights.html">All {len(POSTS)} articles</a></div>
  <div class="grid grid-3">{"".join(card(q) for q in rel)}</div>
</div></section>
<script type="application/ld+json">{json.dumps(ld)}</script>'''
    sub_page(f"post/{p['slug']}.html", p["title"], esc(p["desc"] or text_excerpt(p["body"], 155)), body)
    if cover:
        fp = os.path.join(OUT, "post", p["slug"] + ".html"); h = open(fp).read()
        h = h.replace(f'<meta property="og:image" content="{SITE_URL}/assets/img/chmltech-mark.png">',
                      f'<meta property="og:image" content="{SITE_URL}/{cover[3:]}">\n<meta name="twitter:card" content="summary_large_image">', 1)
        open(fp, "w").write(h)
    # card() inside sub_page body used prefix "" -> sub_page rewrites to ../ automatically
journal_pages.build(globals())  # research-paper layout for the journal articles (V4.12)

# ---------------------------------------------------------------- WIX CONTENT PAGES (industries, solutions, others)
def content_page(slug, crumb_html, eyebrow_default, aside_html="", extra_after=""):
    d = pages_raw.get(slug)
    if not d: return False
    raw = d["html"]
    h1 = re.search(r"<h1>(.*?)</h1>", raw, re.S)
    title = H.unescape(re.sub(r"<[^>]+>", "", h1.group(1)).strip()) if h1 else H.unescape(d["title"].split(" | ")[0])
    raw = raw.replace(h1.group(0), "", 1) if h1 else raw
    eyebrow = eyebrow_default
    lead = ""
    m = re.match(r"\s*<h5>(.*?)</h5>", raw, re.S)
    if m:
        lead = H.unescape(re.sub(r"<[^>]+>", "", m.group(1)).strip()); raw = raw[m.end():]
    m = re.match(r"\s*<h3>(.*?)</h3>", raw, re.S)
    sub = ""
    if m:
        sub = H.unescape(re.sub(r"<[^>]+>", "", m.group(1)).strip()); raw = raw[m.end():]
    body = clean_html(raw, "", post_slugs)
    body = re.sub(r"<h6>(.*?)</h6>", r"<h2>\1</h2>", body, flags=re.S)
    body = re.sub(r"<h5>(.*?)</h5>", r"<h3>\1</h3>", body, flags=re.S)
    def tc(s):  # tame ALL-CAPS headings
        t = re.sub(r"<[^>]+>", "", s)
        return s if not (t.isupper() and len(t) > 3) else t.capitalize().replace("Chmltech", "Chmltech").replace(" ai ", " AI ").replace("Kpi", "KPI").replace("Iso", "ISO").replace("Eos", "EOS")
    body = re.sub(r"<(h2|h3)>(.*?)</\1>", lambda m: f"<{m.group(1)}>{tc(m.group(2))}</{m.group(1)}>", body, flags=re.S)
    body = re.sub(r"<p><strong>([^<]{4,120})</strong></p>", lambda m: f"<h3>{tc(m.group(1))}</h3>" if m.group(1).isupper() else m.group(0), body)
    display = title.title() if title.isupper() else title
    for a, b in [("Eos", "EOS"), ("(Eos)", "(EOS)"), ("Iso", "ISO"), ("Ai ", "AI ")]: display = display.replace(a, b)
    lead_t = lead.capitalize() if lead.isupper() else lead
    sub_t = sub
    hero = page_hero(crumb_html, eyebrow, esc(display), esc(sub_t or lead_t),
                     '<div class="btn-row"><a class="btn" href="book.html">Book a Strategy Call</a><a class="btn btn-ghost-dark" href="contact.html">Ask a question</a></div>')
    if sub_t and lead_t:
        hero = hero.replace(f'<p class="eyebrow">{eyebrow}</p>', f'<p class="eyebrow">{esc(lead_t)}</p>', 1)
    aside = aside_html or '''<div class="card card-dark" style="padding:28px"><p class="eyebrow">Next step</p><h3 style="font-size:22px">Talk to Chmltech</h3><p>Tell us about your operation and we will suggest where to start.</p><a class="btn" href="book.html" style="align-self:flex-start">Book a Strategy Call</a></div>'''
    out = hero + f'''
<section class="section"><div class="container layout-aside">
  <div class="prose">
{body}
  </div>
  <aside class="aside-sticky">{aside}</aside>
</div></section>{extra_after}'''
    page(f"{slug}.html", display, esc(d.get("description") or text_excerpt(body, 155)), out)
    ALL_PAGES.append(f"{slug}.html")
    return True

def related_posts_html(keys, n=3):
    picks = [p for p in POSTS if set(p["cats"]) & set(keys)][:n]
    if not picks: return ""
    return f'''
<section class="section sand"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">From our insights</p><h2 class="h-lg">Related reading</h2></div><a class="btn btn-ghost" href="insights.html">All articles</a></div>
  <div class="grid grid-3">{"".join(card(p) for p in picks)}</div>
</div></section>'''

IND_KEYS = {"energy-and-chemicals": ["esg", "operational-efficiency"], "natural-resources": ["esg", "operational-efficiency"], "manufacturing": ["lean", "erp"],
            "health-care": ["digital-technology", "process-improvement"], "professional-services": ["strategy", "digital-technology"],
            "consumer-goods": ["marketing", "erp"], "distribution-and-warehousing": ["erp", "lean"], "public-sector": ["change-management", "project-management"]}
ind_list = "".join(f'<a href="{s}.html">{n}</a>' for s, n, *_ in INDUSTRIES)
for s, n, ic, d, *_ in INDUSTRIES:
    aside = f'''<div class="card card-dark" style="padding:28px"><p class="eyebrow">Next step</p><h3 style="font-size:22px">Talk to Chmltech</h3><p>Tell us about your operation and we will suggest where to start.</p><a class="btn" href="book.html" style="align-self:flex-start">Book a Strategy Call</a></div>
    <div class="card" style="padding:24px"><p class="eyebrow">Other industries</p><div class="index" style="grid-template-columns:1fr;border-top:0">{"".join(f'<a href="{s2}.html">{n2}<span aria-hidden="true">→</span></a>' for s2, n2, *_ in INDUSTRIES if s2 != s)}</div></div>'''
    content_page(s, f'<a href="industries.html">Industries</a> / {n}', "Industries", aside, related_posts_html(IND_KEYS.get(s, [])))

SOL_KEYS = {"scaling-up": ["strategy"], "business-process-optimization": ["process-improvement", "lean"], "operational-efficiency": ["operational-efficiency"],
            "process-mapping": ["process-improvement"], "process-improvement": ["process-improvement", "six-sigma"], "rapid-lean-assessment": ["lean"],
            "project-portfolio-management": ["project-management", "agile"], "iso9001": ["iso"], "lean-six-sigma-training": ["six-sigma", "lean"],
            "artificial-intelligence": ["artificial-intelligence"]}
SOL_ALL = [(s, t) for s, t, *_ in SOLUTIONS]
for s, t in SOL_ALL:
    aside = f'''<div class="card card-dark" style="padding:28px"><p class="eyebrow">Next step</p><h3 style="font-size:22px">Discuss {esc(t)}</h3><p>Book a strategy call and we will scope the right first step.</p><a class="btn" href="contact.html?service={t.replace("&amp;", "%26").replace(" ", "%20")}" style="align-self:flex-start">Enquire</a></div>
    <div class="card" style="padding:24px"><p class="eyebrow">All solutions</p><div class="index" style="grid-template-columns:1fr;border-top:0">{"".join(f'<a href="{s2}.html">{t2}<span aria-hidden="true">→</span></a>' for s2, t2 in SOL_ALL if s2 != s)}</div></div>'''
    content_page(s, f'<a href="solutions.html">Solutions</a> / {t}', "Solutions", aside, related_posts_html(SOL_KEYS.get(s, [])))

# ---------------------------------------------------------------- INDUSTRIES overview
ind = page_hero("Industries", "Industries", "Deep process know-how across the sectors that keep Canada running.",
                "Every industry has its own constraints. We bring a common improvement method and adapt it to the realities of your operation, your regulations and your people.",
                '<div class="btn-row"><a class="btn" href="book.html">Discuss your operation</a></div>')
ind += f'''
<section class="section"><div class="container">
  <div class="grid grid-3">
  {"".join(f'<article class="card">{icon(ic)}<h3>{n}</h3><p class="muted">{d}</p><a class="more" href="{s}.html">Explore {n} →</a></article>' for s, n, ic, d, *_ in INDUSTRIES)}
  </div>
</div></section>
<section class="section sand"><div class="container">
  <div class="stack" style="max-width:680px;margin-bottom:56px"><p class="eyebrow">How we work</p><h2 class="h-lg">One method, applied to your context.</h2></div>
  {steps_html()}
</div></section>
{QUOTE}'''
page("industries.html", "Industries", "Chmltech supports energy and chemicals, natural resources, manufacturing, health care, professional services, consumer goods, distribution and warehousing, and the public sector.", ind)

# ---------------------------------------------------------------- SOLUTIONS overview
sol = page_hero("Solutions", "Solutions", "From AI strategy to the shop floor.",
                "Three core services, delivered through a focused set of solutions. Each one follows the same practical approach: discover, map, prioritise, implement and measure.",
                '<div class="btn-row"><a class="btn" href="book.html">Book a Strategy Call</a><a class="btn btn-ghost-dark" href="#all-solutions">See all solutions</a></div>')
CORE_LINK = {"ai-strategy": "artificial-intelligence.html", "digital-transformation": "business-process-optimization.html", "business-process-improvement": "process-improvement.html"}
sol += f'''
<section class="section"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Core services</p><h2 class="h-lg">Where most engagements start.</h2></div></div>
  <div class="grid grid-3">
  {"".join(f'<article class="card" id="{s}" style="scroll-margin-top:100px">{icon(ic)}<h3>{t}</h3><p class="muted">{d}</p><ul class="list-check">{"".join(f"<li>{x}</li>" for x in li)}</ul><a class="more" href="{CORE_LINK[s]}">Learn more →</a></article>' for s, t, ic, d, li in CORE)}
  </div>
</div></section>
<section class="section sand" id="all-solutions" style="scroll-margin-top:84px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">All solutions</p><h2 class="h-lg">Focused solutions for specific problems.</h2></div><p>Not sure which fits? Book a call and we will point you to the right starting place.</p></div>
  <div class="grid grid-3">
  {"".join(f'<article class="card">{icon(ic)}<h3>{t}</h3><p class="muted">{d}</p><a class="more" href="{s}.html">Learn more →</a></article>' for s, t, ic, d, li in SOLUTIONS)}
  <article class="card">{icon("users")}<h3>Leadership Operating System</h3><p class="muted">A simple plan, 90-day priorities, a weekly scorecard and meeting rhythm, and clear roles, so the leadership team runs the business on one shared routine.</p><a class="more" href="leadership-operating-system.html">Learn more →</a></article>
  </div>
</div></section>
<section class="section"><div class="container">
  <div class="stack" style="max-width:680px;margin-bottom:56px"><p class="eyebrow">How we work</p><h2 class="h-lg">One method, applied to your context.</h2></div>
  {steps_html()}
</div></section>
{QUOTE}'''
sol = sol.replace('<section class="section sand" id="all-solutions"', f'''<section class="section dark"><div class="container feature-split">
  <div class="stack-lg"><p class="eyebrow">New · AI Operating System</p><h2 class="h-lg">Build your company's AI Operating System.</h2>
  <p class="lead">One connected layer that links your data, company knowledge, AI agents and workflows, so AI works across the whole business instead of in scattered tools.</p>
  <ul class="list-check">{"".join(f"<li>{t}</li>" for _, t, _ in COMPONENTS[:4])}</ul>
  <div class="btn-row"><a class="btn" href="ai-operating-system.html">Explore AI Operating System</a><a class="btn btn-ghost-dark" href="contact.html?service=AI%20Operating%20System">Enquire</a></div></div>
  {aios_svg(compact=True)}
</div></section>
<section class="section sand" id="all-solutions"''', 1)
page("solutions.html", "Solutions", "AI readiness and strategy, digital transformation advisory, business process improvement, Lean Six Sigma, ISO 9001, process mapping, leadership operating systems and more from Chmltech Ltd.", sol)

# ---------------------------------------------------------------- TRAINING: free practice exam library
EXAM_BASE = "exams/"
exam_cats = json.load(open(os.path.join(HERE, "exam_cats.json")))
LEAD_ORDER = ["quality_lean", "operations", "ai_agents", "ai_use_cases", "process_chemeng", "project_agile", "software_data", "cybersecurity", "business_finance", "decision_thinking"]
exam_cats.sort(key=lambda c: LEAD_ORDER.index(c["id"]) if c["id"] in LEAD_ORDER else 99)
n_exams = sum(len(c["exams"]) for c in exam_cats)
n_q = 0
for c in exam_cats:
    for e in c["exams"]:
        m = re.match(r"(\d+)", e[2] or ""); n_q += int(m.group(1)) if m else 0
from urllib.parse import quote
exam_cards = []
for c in exam_cats:
    for e in c["exams"]:
        title, file, count, ver = e[0], e[1], e[2], e[3]; summ = e[4] if len(e) > 4 else ""
        url = EXAM_BASE + quote(re.sub(r"^(\.\./)+", "", file))
        exam_cards.append(f'<article class="exam" data-cats="{c["id"]}" data-search="{esc((title + " " + summ + " " + c["name"]).lower())}"><span class="tag">{esc(c["name"])}</span>'
                          f'<h3><a href="{url}" target="_blank" rel="noopener">{esc(title)}</a></h3><p>{esc(summ)}</p>'
                          f'<div class="foot"><span>{(re.match(r"(\d+)", count or "").group(1) + " questions") if re.match(r"\d+", count or "") else "Interactive"}</span><span>Start →</span></div></article>')
ex_chips = f'<button class="chip" type="button" data-cat="all" aria-pressed="true">All ({n_exams})</button>' + "".join(
    f'<button class="chip" type="button" data-cat="{c["id"]}" aria-pressed="false">{esc(c["name"])} ({len(c["exams"])})</button>' for c in exam_cats)

# migrated Wix tool/exam pages (self-hosted copies of the embedded HTML)
embeds = json.load(open(os.path.join(WIX, "embeds.json"))) if os.path.exists(os.path.join(WIX, "embeds.json")) else {}
EMBED_PAGES = []
for slug in sorted(k for k in embeds if not k.endswith("__title")):
    local = os.path.join(OUT, "exams", slug + ".html")
    if not os.path.exists(local): continue
    t = embeds.get(slug + "__title", slug).split(" | ")[0].strip() or slug.replace("-", " ").title()
    EMBED_PAGES.append((slug, t))
    body = page_hero(f'<a href="training.html">Training</a> / {esc(t)}', "Free practice", esc(t), "Free interactive practice from Chmltech. Works best on a laptop or tablet.",
                     f'<div class="btn-row"><a class="btn btn-ghost-dark" href="exams/{slug}.html" target="_blank" rel="noopener">Open full screen</a><a class="btn btn-ghost-dark" href="training.html">All practice exams</a></div>')
    body += f'''<section class="section-sm"><div class="container"><iframe class="embed-frame" src="exams/{slug}.html" title="{esc(t)}" loading="lazy"></iframe></div></section>'''
    page(f"{slug}.html", t, f"Free {esc(t)} from Chmltech Ltd.: interactive practice questions.", body, cta=False)
    ALL_PAGES.append(f"{slug}.html")

tr = page_hero("Training", "Free training", "Free practice exams for technical and professional growth.",
               "Test and build your knowledge with Chmltech's free interactive practice exams, from Lean Six Sigma, ISO 9001 and Kaizen to AI, process engineering, project management and more.",
               f'<div class="btn-row"><a class="btn" href="#library">Browse the library</a><a class="btn btn-ghost-dark" href="courses.html">Free courses</a></div><div class="stat-row"><div><strong>{n_exams}</strong><span>practice exams</span></div><div><strong>{n_q:,}+</strong><span>questions</span></div><div><strong>{len(exam_cats)}</strong><span>categories</span></div><div><strong>$0</strong><span>always free</span></div></div>')
tr += f'''
<section class="section" id="library" style="scroll-margin-top:84px;padding-top:64px"><div class="container" data-list="exams" data-page-size="30">
  <div class="toolbar">
    <label class="search"><span class="visually-hidden">Search practice exams</span>{SEARCH_SVG}<input type="search" placeholder="Search {n_exams} exams" data-search-input></label>
    <span class="count" data-count aria-live="polite">{n_exams} exams</span>
  </div>
  <div class="chips" role="group" aria-label="Filter by category">{ex_chips}</div>
  <div class="grid grid-4" data-items>
  {"".join(exam_cards)}
  </div>
  <p class="empty" data-empty>No exams match your search.</p>
  <div class="more-wrap"><button class="btn btn-ghost" type="button" data-more>Show more exams</button></div>
  <p class="count" style="margin-top:24px;text-align:center">Exams open in a new tab from the Chmltech exam library.</p>
</div></section>'''
if EMBED_PAGES:
    tr += f'''
<section class="section sand"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">More free practice</p><h2 class="h-lg">Mock exams, guides and quizzes</h2></div><p>Interactive practice hosted right here on chmltech.com.</p></div>
  <div class="index">{"".join(f'<a href="{s}.html">{esc(t)}<span aria-hidden="true">→</span></a>' for s, t in EMBED_PAGES)}</div>
</div></section>'''
tr += f'''
<section class="section"><div class="container grid grid-2">
  <div class="card card-dark" style="padding:44px 40px"><p class="eyebrow">Lean Six Sigma</p><h3 class="h-md">Lean Six Sigma training for your team</h3><p>In-house programmes that create a culture of continuous improvement, built around your own processes.</p><div class="btn-row" style="margin-top:8px"><a class="btn btn-ghost-dark" href="lean-six-sigma-training.html">Learn more</a></div></div>
  <div class="card" style="padding:44px 40px"><p class="eyebrow">Free courses</p><h3 class="h-md">Structured, step-by-step programs</h3><p class="muted">Free online programs on AI readiness, workflow automation, 5S, project leadership and operational excellence.</p><div class="btn-row" style="margin-top:8px"><a class="btn btn-ghost" href="courses.html">View free courses</a></div></div>
</div></section>'''
page("training.html", "Free Training & Practice Exams", f"{n_exams} free interactive practice exams from Chmltech: Lean Six Sigma, ISO 9001, Kaizen, AI, process engineering, PMP, Agile and more.", tr)

# ---------------------------------------------------------------- COURSES: free online programs + paid sessions
PROG_ICON = ["chip", "gauge", "flow", "grid", "users", "target"]
PROG_ICON_ID = {"ai-awareness-for-everyone": "target", "digital-automation-for-smes": "screen", "multi-agent-systems-for-business": "users", "ai-agents-for-business-operations": "spark", "building-your-ai-operating-system": "os", "llms-for-business-leaders": "book",
                "e676eeeb-ed5f-40e1-b4c7-e287da77981b": "chip", "91ca0386-ec82-483d-8ec7-d6b13f02a0b5": "layers", "e385a42b-5aaf-457f-9957-e8d19fee8cc0": "flow",
                "b4b6581a-31f8-43f9-8796-268c83448b9f": "gauge", "25c5f60e-3f55-43a1-9c15-345dfc5b8f7f": "grid", "ac58bd83-591d-4c25-9aac-71755f469d3c": "shield"}
progs = []
for pid, d in programs_raw.items():
    t = d["title"].split(" | ")[0].strip()
    steps = re.search(r"(\d+)\s*\n\s*Steps", d["text"]); steps = steps.group(1) if steps else ""
    about = re.search(r"About\s*\n(.*?)\n\s*(?:You can also join|Price)", d["text"], re.S); about = about.group(1).strip() if about else ""
    progs.append(dict(id=pid, title=t, steps=steps, about=about, slug=re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")))
progs.sort(key=lambda x: x["title"])
COURSE_DIR = os.path.join(os.path.dirname(HERE), "courses")
for p in progs:
    fp = None
    for f in glob.glob(os.path.join(COURSE_DIR, "*.json")):
        try:
            cj = json.load(open(f))
        except Exception:
            continue
        if isinstance(cj, dict) and cj.get("id") == p["id"]:
            p["course"] = cj; break
# courses written for the new site (no Wix program behind them)
_known = {p["id"] for p in progs}
for f in sorted(glob.glob(os.path.join(COURSE_DIR, "*.json"))):
    try:
        cj = json.load(open(f))
    except Exception:
        continue
    if isinstance(cj, dict) and cj.get("modules") and cj.get("id") not in _known:
        progs.append(dict(id=cj["id"], title=cj["title"], steps=str(sum(len(m["steps"]) for m in cj["modules"])), about=cj["summary"], slug=cj["id"], course=cj))
        _known.add(cj["id"])
COURSE_ORDER = ["ai-awareness-for-everyone", "llms-for-business-leaders", "ai-agents-for-business-operations", "multi-agent-systems-for-business", "building-your-ai-operating-system", "digital-automation-for-smes",
                "e676eeeb-ed5f-40e1-b4c7-e287da77981b", "91ca0386-ec82-483d-8ec7-d6b13f02a0b5", "e385a42b-5aaf-457f-9957-e8d19fee8cc0",
                "b4b6581a-31f8-43f9-8796-268c83448b9f", "25c5f60e-3f55-43a1-9c15-345dfc5b8f7f", "ac58bd83-591d-4c25-9aac-71755f469d3c"]
progs.sort(key=lambda p: COURSE_ORDER.index(p["id"]) if p["id"] in COURSE_ORDER else 99)
def prog_card(p, i):
    c = p.get("course")
    if c:
        stt = course_stats(c)
        facts = f'<span class="tag tag-green">Free</span><span class="tag">{stt["steps"]} lessons</span><span class="tag">{stt["labs"]} labs</span><span class="tag">Final exam + certificate</span>'
        blurb, cta = c["tagline"], "Start free course →"
    else:
        facts = f'<span class="tag tag-green">Free</span>{f"<span class=tag>{p["steps"]} steps</span>" if p["steps"] else ""}<span class="tag">Self-paced</span>'
        blurb, cta = text_excerpt(p["about"], 230), "Course details →"
    return (f'<article class="program">{icon(PROG_ICON_ID.get(p["id"], PROG_ICON[i % len(PROG_ICON)]))}<div class="facts">{facts}</div>'
            f'<h3 class="h-md" style="font-size:24px">{esc(p["title"])}</h3><p class="muted">{esc(blurb)}</p>'
            f'<a class="more" style="margin-top:auto;font-weight:600" href="challenge-page/{p["id"]}.html">{cta}</a></article>')
SERVICES = []
for s, d in sorted(services_raw.items()):
    t = d["title"].split(" | ")[0].strip().title()
    price = re.search(r"([\d,]+)\s*Canadian dollars", d["text"]) or re.search(r"CA\$\s*([\d,]+)", d["text"]); dur = re.search(r"(\d+)\s*hr", d["text"])
    SERVICES.append(dict(slug=s, title=t, price=price.group(1) if price else {"project-management": "250", "corporate-strategy": "450", "operational-consulting": "350"}.get(s, ""), dur=(dur.group(1) + " hour") if dur else "1 hour"))
SERVICE_DESC = {"corporate-strategy": "A focused working session on growth strategy, priorities, planning and the decisions in front of your leadership team.",
                "operational-consulting": "A practical session on operational bottlenecks, process improvement, systems and KPIs.",
                "project-management": "Expert input on planning, governance, risk and delivery for a project or portfolio."}
def svc_card(s):
    return (f'<article class="program" id="{s["slug"]}" style="scroll-margin-top:100px"><div class="facts"><span class="tag">{s["dur"]}</span><span class="tag">Online meeting</span></div>'
            f'<h3 class="h-md" style="font-size:24px">{esc(s["title"])} session</h3><p class="muted">{SERVICE_DESC.get(s["slug"], "")}</p>'
            f'<p class="price">CA${s["price"]} <small>/ session</small></p><a class="btn" style="align-self:flex-start" href="book.html?service={quote(s["title"] + " session")}">Book this session</a></article>')
co = page_hero("Courses", "Free courses", "Free online courses for operational excellence.",
               "Interactive, self-paced courses on AI (from prompting and LLMs to agents and private AI), business basics, data and dashboards, ERP selection, cybersecurity, operational excellence, Lean Six Sigma, ISO 9001, OEE, inventory, S&amp;OP, project leadership, 5S and FEED for process plants. Each has hands-on labs, a final exam and a certificate of completion. Free, no sign-up.",
               '<div class="btn-row"><a class="btn" href="#programs">See the courses</a><a class="btn btn-ghost-dark" href="training.html">Free practice exams</a></div>')
co += f'''
<section class="section" id="programs" style="scroll-margin-top:84px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Free programs</p><h2 class="h-lg">{len(progs)} free courses</h2></div><p>Each course combines short lessons, knowledge checks, three interactive labs and a final exam. Pass it to earn a Chmltech certificate of completion.</p></div>
  <div class="grid grid-3">{"".join(prog_card(p, i) for i, p in enumerate(progs))}</div>
</div></section>
<section class="section sand" id="sessions" style="scroll-margin-top:84px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Expert sessions</p><h2 class="h-lg">Book a one-hour session</h2></div><p>Need focused expert input? Book a paid one-hour online session.</p></div>
  <div class="grid grid-3">{"".join(svc_card(s) for s in SERVICES)}</div>
</div></section>
<section class="section"><div class="container grid grid-2">
  <div class="card card-dark" style="padding:44px 40px"><p class="eyebrow">In-house training</p><h3 class="h-md">Lean Six Sigma training for your team</h3><p>Programmes built around your own processes and improvement projects.</p><div class="btn-row" style="margin-top:8px"><a class="btn btn-ghost-dark" href="lean-six-sigma-training.html">Learn more</a></div></div>
  <div class="card" style="padding:44px 40px"><p class="eyebrow">Practice</p><h3 class="h-md">{n_exams} free practice exams</h3><p class="muted">Test your knowledge in Lean Six Sigma, ISO 9001, AI, process engineering, PMP and more.</p><div class="btn-row" style="margin-top:8px"><a class="btn btn-ghost" href="training.html">Browse exams</a></div></div>
</div></section>'''
page("courses.html", "Free Courses", "Free interactive courses from Chmltech Ltd. on AI awareness, LLMs, AI agents, multi-agent systems, AI operating systems, AI readiness, digital transformation and automation, operational excellence, project leadership and 5S, plus bookable expert sessions.", co)

for p in progs:
    others = [q for q in progs if q["id"] != p["id"]]
    if p.get("course"):
        cbody, _, _ = render_course(p["course"], page_hero, others)
        sub_page(f"challenge-page/{p['id']}.html", p["title"], esc(p["course"]["summary"][:155]), cbody, cta=False)
        finalize_course_file(os.path.join(OUT, "challenge-page", p["id"] + ".html"))
        continue
    body = page_hero(f'<a href="courses.html">Courses</a> / {esc(p["title"])}', "Free course", esc(p["title"]), "Free · " + (p["steps"] + " steps · " if p["steps"] else "") + "Self-paced",
                     f'<div class="btn-row"><a class="btn" href="contact.html?service=Training%20or%20courses&course={quote(p["title"])}">Request access</a><a class="btn btn-ghost-dark" href="courses.html">All courses</a></div>')
    body += f'''
<section class="section"><div class="container layout-aside">
  <div class="prose"><h2>About this course</h2><p>{esc(p["about"])}</p>
  <h2>What it includes</h2><ul><li>{p["steps"] or "Multiple"} guided steps you complete at your own pace</li><li>Practical frameworks and tools you can apply at work</li><li>Free of charge</li></ul>
  <p>To join, request access and we will send you the course materials.</p></div>
  <aside class="aside-sticky"><div class="card card-dark" style="padding:28px"><p class="eyebrow">Free</p><h3 style="font-size:22px">Join this course</h3><p>Request access and we will send you the course materials.</p><a class="btn" href="contact.html?service=Training%20or%20courses&course={quote(p["title"])}" style="align-self:flex-start">Request access</a></div>
  <div class="card" style="padding:24px"><p class="eyebrow">More free courses</p><div class="index" style="grid-template-columns:1fr;border-top:0">{"".join(f'<a href="challenge-page/{q["id"]}.html">{esc(q["title"])}<span aria-hidden="true">→</span></a>' for q in others)}</div></div></aside>
</div></section>'''
    sub_page(f"challenge-page/{p['id']}.html", p["title"], esc(text_excerpt(p["about"], 155)), body)

for s in SERVICES:
    redirect(f"service-page/{s['slug']}.html", f"courses.html#{s['slug']}", s["title"])

# ---------------------------------------------------------------- BOOK: add bookable sessions
bk = ns["bk_body"]
svc_strip = f'''
<section class="section-sm white" style="border-bottom:1px solid var(--line)"><div class="container">
  <div class="section-head" style="margin-bottom:28px"><div class="stack"><p class="eyebrow">Paid expert sessions</p><h2 class="h-md">Or book a one-hour session</h2></div><p>The strategy call is free. For focused expert input, choose a paid session in the form below.</p></div>
  <div class="grid grid-3">{"".join(f'<div class="card" style="padding:24px"><h3 style="font-size:20px">{esc(s["title"])}</h3><p class="price" style="font-size:24px">CA${s["price"]} <small>/ {s["dur"]}, online</small></p></div>' for s in SERVICES)}</div>
</div></section>'''
bk = bk.replace('<section class="section"><div class="container split">', svc_strip + '\n<section class="section"><div class="container split">', 1)
bk = bk.replace('Tell us a little about your business and pick a time that works.', 'The first strategy call is free. Tell us a little about your business and pick a time that works.')
page("book.html", "Book Online", "Book a free strategy call or a paid expert session with Chmltech Ltd.", bk, cta=False)

# ---------------------------------------------------------------- PROJECTS
pj = pages_raw.get("projects")
if pj:
    imgs = re.findall(r'<figure><img src="([^"]+)"[^>]*></figure>\s*<h2>(.*?)</h2>', pj["html"])
    cards = []
    for src_u, name in imgs:
        m = MEDIA_RE.search(src_u); loc = media_local(m.group(1), "") if m else None
        nm = re.sub(r"<[^>]+>", "", name).strip().title()
        cards.append(f'<article class="article">{f"<div class=thumb><img src={chr(34)}{loc}{chr(34)} alt={chr(34)}{esc(nm)}{chr(34)} loading=lazy></div>" if loc else ""}<div class="body"><h3>{esc(nm)}</h3></div></article>')
    body = page_hero("Projects", "Projects", "Selected projects.", "A selection of process engineering, scale-up and operations projects delivered by Chmltech.")
    body += f'<section class="section"><div class="container"><div class="grid grid-2">{"".join(cards)}</div></div></section>'
    ALL_PAGES.append("projects.html")
projects_page.build(globals())  # V4.24: rebuilt Projects page (the Wix version held template placeholders)

# ---------------------------------------------------------------- HOME: latest insights + training teaser
home = open(os.path.join(OUT, "index.html")).read()
latest = "".join(card(p) for p in POSTS[:3])
teaser_old = home[home.index('<section style="padding-bottom:112px">'):home.index("</main>")]
teaser_new = f'''<section class="section" style="padding-top:0"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Latest insights</p><h2 class="h-lg">From the Chmltech journal</h2></div><a class="btn btn-ghost" href="insights.html">All {len(POSTS)} articles</a></div>
  <div class="grid grid-3">{latest}</div>
</div></section>
<section style="padding-bottom:112px">
  <div class="container grid grid-2">
    <div class="card card-dark" style="padding:44px 40px">
      <p class="eyebrow">Free training</p>
      <h3 class="h-md">{n_exams} free practice exams.</h3>
      <p>Lean Six Sigma, ISO 9001, Kaizen, AI, process engineering, PMP and more, with {n_q:,}+ questions, free.</p>
      <div class="btn-row" style="margin-top:8px"><a class="btn btn-ghost-dark" href="training.html">Browse practice exams</a></div>
    </div>
    <div class="card" style="padding:44px 40px">
      <p class="eyebrow">Free courses</p>
      <h3 class="h-md">{len(progs)} free online courses.</h3>
      <p class="muted">Interactive courses from AI awareness, LLMs and multi-agent systems to digital automation, operational excellence and 5S, with labs, exams and certificates.</p>
      <div class="btn-row" style="margin-top:8px"><a class="btn btn-ghost" href="courses.html">View free courses</a></div>
    </div>
  </div>
</section>
'''
# re-insert CTA that lived inside teaser_old tail
cta_part = teaser_old[teaser_old.index('<section class="cta">'):] if '<section class="cta">' in teaser_old else ""
home = home.replace(teaser_old, teaser_new + cta_part)
open(os.path.join(OUT, "index.html"), "w").write(home)

# ---------------------------------------------------------------- AI OPERATING SYSTEM page
aios_body = page_hero('<a href="solutions.html">Solutions</a> / AI Operating System', "Solutions · AI Operating System",
    "Build your company&#39;s AI Operating System.",
    "We design and build an AI Operating System for your business: one connected layer that links your data, company knowledge, AI agents and workflows, so AI works across the whole company, not in scattered tools.",
    '<div class="btn-row"><a class="btn" href="book.html">Book a Strategy Call</a><a class="btn btn-ghost-dark" href="#what-we-build">What we build</a></div>')
aios_body += f'''
<section class="section" style="padding-top:64px"><div class="container feature-split">
  <div class="stack-lg"><p class="eyebrow">What is an AI OS?</p><h2 class="h-lg">The foundation that makes AI work across your business.</h2>
  <p class="muted" style="font-size:17.5px">Most companies adopt AI one tool at a time: a chatbot here, a writing assistant there. Each one works alone, without your data or context. An AI Operating System changes that. It connects your systems and knowledge into one secure core, then puts AI assistants, agents and automations on top, all governed by your rules.</p>
  <p class="muted" style="font-size:17.5px">The result is AI that knows your business, works inside your processes and keeps improving as you use it.</p></div>
  {aios_svg()}
</div></section>
<section class="section sand" id="what-we-build" style="scroll-margin-top:84px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">What we build</p><h2 class="h-lg">Six building blocks of your AI OS.</h2></div><p>Each block is designed around your processes, data and team, and delivered in phases.</p></div>
  <div class="grid grid-3">{"".join(f'<article class="card">{icon(ic)}<h3>{t}</h3><p class="muted">{d}</p></article>' for ic, t, d in COMPONENTS)}</div>
</div></section>
<section class="section"><div class="container">
  <div class="stack" style="max-width:720px;margin-bottom:56px"><p class="eyebrow">How we build it</p><h2 class="h-lg">From AI readiness to a working AI OS, step by step.</h2></div>
  <ol class="steps">{"".join(f"<li><b>{i + 1:02d}</b><h3>{t}</h3><p>{d}</p></li>" for i, (t, d) in enumerate(PHASES))}</ol>
</div></section>
<section class="section dark"><div class="container grid grid-2" style="align-items:center">
  <div class="stack"><p class="eyebrow">Why it matters</p><h2 class="h-lg">What changes for your team.</h2><p class="lead">An AI OS turns AI from individual experiments into a shared capability that compounds over time.</p></div>
  <ul class="list-check" style="font-size:17px">{"".join(f"<li>{b}</li>" for b in BENEFITS)}</ul>
</div></section>
<section class="section-sm sand"><div class="container grid grid-2" style="align-items:center">
  <div class="stack"><p class="eyebrow">Free course</p><h2 class="h-md">Learn to plan your own AI OS</h2><p class="muted">Our free, self-paced course <strong>Building Your AI Operating System</strong> walks through the building blocks, architecture, data and knowledge, assistants and agents, governance and a 90-day plan, with interactive labs and a certificate.</p></div>
  <div class="btn-row"><a class="btn" href="challenge-page/building-your-ai-operating-system.html">Start the free course</a><a class="btn btn-ghost" href="courses.html">All free courses</a></div>
</div></section>
<section class="section"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Questions</p><h2 class="h-lg">AI Operating System FAQs</h2></div><a class="btn btn-ghost" href="artificial-intelligence.html">AI solutions overview</a></div>
  <div class="faq">{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in AIOS_FAQ)}</div>
</div></section>
{related_posts_html(["artificial-intelligence", "digital-technology"])}'''
page("ai-operating-system.html", "AI Operating System", "Chmltech designs and builds AI Operating Systems for Canadian SMEs: a connected layer of data, company knowledge, AI agents and workflows with governance built in.", aios_body)
ALL_PAGES.append("ai-operating-system.html")
css_p = os.path.join(OUT, "assets/css/styles.css"); css = open(css_p).read()
mk = "\n/* ===== AI Operating System illustration"
if mk in css: css = css[:css.index(mk)]
open(css_p, "w").write(css.rstrip("\n") + "\n" + AIOS_CSS)

# ---------------------------------------------------------------- redirects for retired Wix URLs
redirect("challenges.html", "courses.html", "Courses")
redirect("plans-pricing.html", "courses.html", "Courses")
redirect("book-online.html", "book.html", "Book Online")
redirect("home.html", "index.html", "Home")

service_pages.build(globals())
redirect("eos.html", "leadership-operating-system.html", "Leadership Operating System")  # V4.23: EOS page withdrawn (trademark)
privacy_page.build(globals())
industry_pages.build(globals())
grants_page.build(globals())  # V4.27: funding finder (data/grants.json, red-team verified)

# ---------------------------------------------------------------- sitemap
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p in dict.fromkeys(ALL_PAGES):
        loc = p[:-5] if p.endswith(".html") else p
        f.write(f"  <url><loc>{SITE_URL}/{loc}</loc></url>\n")
    f.write("</urlset>\n")

json.dump(sorted(needed_media), open(os.path.join(WIX, "needed_media.json"), "w"), indent=0)
json.dump(dict(dropped_media), open(os.path.join(WIX, "dropped_media.json"), "w"), indent=0)
json.dump([p["cover"] for p in POSTS if p["cover"] and p["cover"].startswith(("33d8e3_", "nsplsh_"))], open(os.path.join(WIX, "thumb_media.json"), "w"))
print(f"posts {len(POSTS)} | pages {len(ALL_PAGES)} | media needed {len(needed_media)} | stock dropped {len(dropped_media)} | embeds {len(EMBED_PAGES)} | programs {len(progs)}")
print("category coverage from map:", sum(1 for p in POSTS if p["slug"] in post_cats), "of", len(POSTS))
