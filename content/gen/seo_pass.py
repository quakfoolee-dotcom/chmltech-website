#!/usr/bin/env python3
"""SEO pass for the Chmltech static site (V4.56).

Run from the site root after any build step:  python3 content/gen/seo_pass.py .
Safe to run any number of times: every change checks whether it is already in place.

What it does on every indexable page (pages with <meta name="robots" content="noindex">
are redirect stubs and are left alone):
  1. Canonical URL uses the clean address without ".html" (the form the sitemap and the
     old Wix links use; GitHub Pages serves both forms). Adds og:url to match.
  2. Articles: og:type "article" with published/modified times; twitter:card on every page.
  3. <title> over 60 characters: drops the " | Chmltech Ltd." suffix so the subject shows
     in full in search results (Google shows the site name separately, from the WebSite data).
  4. Meta descriptions over 160 characters are cut at the last full sentence (or word) that fits.
  5. Structured data (JSON-LD): WebSite + ProfessionalService on the home page, richer
     BlogPosting on articles (image, dates, author page, publisher logo), Service on solution
     and industry pages, Course on the free courses, Quiz on practice exams, FAQPage on
     Contact, AboutPage + Person on About, BreadcrumbList everywhere below the home page.
  6. Article cover image: alt text = article title, fetchpriority="high" (it is the largest
     image in view, so it should load first).
  7. exams/*.html (the raw exam apps shown inside the exam pages): noindex, indexifembedded,
     with a canonical to the page that embeds them, so search engines rank the full page.
  9. Microsoft Clarity analytics on every indexable page (CLARITY_ID below).
  8. Rebuilds sitemap.xml from the files (indexable pages only, clean URLs, lastmod) and
     writes llms.txt (a plain-text guide to the site for AI search tools).
"""
import html, json, os, re, subprocess, sys, datetime
import assetver
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_keywords import KEYWORDS

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
SITE = "https://www.chmltech.com"
BRAND = " | Chmltech Ltd."
LOGO = f"{SITE}/assets/img/chmltech-logo.png"
LINKEDIN = "https://www.linkedin.com/in/quak-foo-lee"
ORG_ID = f"{SITE}/#organization"
PERSON_ID = f"{SITE}/about#quak-foo-lee"
HOME_TITLE = "AI & Operations Consulting for Canadian SMEs | Chmltech Ltd."
CLARITY_ID = "zcd5uqw2cz"  # Microsoft Clarity project (analytics); set to "" to remove from every page
CLARITY = ('<script>(function(c,l,a,r,i,t,y){'
           # Owner opt-out: visit any page with ?notrack=on once per browser to stop analytics there
           # (?notrack=off turns it back on). Stored in this browser only.
           'try{var q=new URLSearchParams(l.location.search).get("notrack");'
           'if(q==="on")localStorage.setItem("chm_notrack","1");'
           'if(q==="off")localStorage.removeItem("chm_notrack");'
           'if(q)alert("Chmltech analytics "+(q==="on"?"OFF":"ON")+" for this browser.");'
           'if(localStorage.getItem("chm_notrack")==="1")return;}catch(e){}'
           'c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};'
           't=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;'
           'y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})'
           f'(window,document,"clarity","script","{CLARITY_ID}");</script>') if CLARITY_ID else ""

SOLUTIONS = """ai-operating-system artificial-intelligence business-process-optimization iso9001
leadership-operating-system lean-six-sigma-training operational-efficiency process-improvement
process-mapping project-portfolio-management rapid-lean-assessment scaling-up""".split()
INDUSTRIES = """consumer-goods distribution-and-warehousing energy-and-chemicals health-care
manufacturing natural-resources professional-services public-sector""".split()
SECTION = {"post": ("Insights", "insights"), "challenge-page": ("Courses", "courses")}

stats = {}
def bump(k): stats[k] = stats.get(k, 0) + 1

def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)
def esc(s): return html.escape(s, quote=True)
def g(pat, s): m = re.search(pat, s, re.S | re.I); return html.unescape(m.group(1)).strip() if m else ""

def clean_url(rel):
    u = rel[:-5] if rel.endswith(".html") else rel
    if u == "index": return SITE + "/"
    return f"{SITE}/{u}"

def pages():
    out = []
    for d, dirs, fs in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in (".git", "assets", "content", "node_modules")]
        for f in fs:
            if f.endswith(".html"):
                out.append(os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, "/"))
    return sorted(out)

def git_date(rel):
    try:
        d = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%cs", "--", rel],
                           capture_output=True, text=True).stdout.strip()
        return d or None
    except Exception:
        return None

def set_meta(head, attr, key, val):
    """Set <meta attr="key" content="val">, adding it before </head> if missing."""
    tag = f'<meta {attr}="{key}" content="{esc(val)}">'
    pat = re.compile(rf'<meta\s+{attr}="{re.escape(key)}"\s+content="[^"]*">')
    if pat.search(head):
        return pat.sub(lambda m: tag, head, count=1)
    return head + tag + "\n"

def trim_desc(d, limit=160):
    if len(d) <= limit: return d
    cut = d[:limit]
    m = list(re.finditer(r"[.!?](?=\s|$)", cut))
    if m and m[-1].end() >= 90:
        return cut[:m[-1].end()].strip()
    cut = d[:limit - 1].rsplit(" ", 1)[0].rstrip(",;:—– ")
    return cut + "…"

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def ld_block(objs):
    data = {"@context": "https://schema.org", "@graph": objs}
    return ('<script type="application/ld+json" data-seo="v1">'
            + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
            + "</script>")

ORG = {"@type": "ProfessionalService", "@id": ORG_ID, "name": "Chmltech Ltd.", "alternateName": "Chmltech",
       "url": SITE + "/", "logo": LOGO, "image": LOGO,
       "description": "Chmltech Ltd. helps Canadian SMEs redesign processes, adopt AI, select the right systems, "
                      "automate workflows and build KPI-driven operations, and provides process engineering support.",
       "email": "info@chmltech.com",
       "address": {"@type": "PostalAddress", "addressLocality": "Vancouver", "addressRegion": "BC", "addressCountry": "CA"},
       "areaServed": {"@type": "Country", "name": "Canada"},
       "founder": {"@id": PERSON_ID},
       "knowsAbout": ["Artificial intelligence adoption", "AI operating systems", "Digital transformation",
                      "Business process improvement", "Lean Six Sigma", "ISO 9001", "Operational efficiency",
                      "Chemical process engineering", "FEED studies", "Scale-up"]}
PERSON = {"@type": "Person", "@id": PERSON_ID, "name": "Quak Foo Lee",
          "jobTitle": "CEO and Principal Consultant", "worksFor": {"@id": ORG_ID},
          "url": f"{SITE}/about", "sameAs": [LINKEDIN]}
ORG_REF = {"@type": "Organization", "@id": ORG_ID, "name": "Chmltech Ltd.",
           "logo": {"@type": "ImageObject", "url": LOGO}}
AUTHOR_REF = {"@type": "Person", "@id": PERSON_ID, "name": "Quak Foo Lee", "url": f"{SITE}/about"}

def build_ld(rel, s, title, desc, url, image):
    h1 = re.sub(r"<[^>]+>", "", g(r"<h1[^>]*>(.*?)</h1>", s)) or title
    name = title.replace(BRAND, "").strip()
    base = rel.split("/")[0] if "/" in rel else ""
    slug = rel.rsplit("/", 1)[-1][:-5]
    home = ("Home", SITE + "/")
    objs = []
    if rel == "index.html":
        objs += [{"@type": "WebSite", "@id": f"{SITE}/#website", "name": "Chmltech", "alternateName": "Chmltech Ltd.",
                  "url": SITE + "/", "publisher": {"@id": ORG_ID}, "inLanguage": "en-CA"}, ORG, PERSON]
        return objs
    if base in SECTION:
        sec = SECTION[base]
        objs.append(crumbs([home, (sec[0], f"{SITE}/{sec[1]}"), (name, url)]))
    else:
        objs.append(crumbs([home, (name, url)]))
    if base == "post":
        return objs  # BlogPosting/ScholarlyArticle already on the page; enriched in place
    if rel == "about.html":
        objs += [{"@type": "AboutPage", "url": url, "name": name, "about": {"@id": ORG_ID},
                  "mainEntity": {"@id": PERSON_ID}}, PERSON, ORG]
    elif rel == "contact.html":
        faqs = re.findall(r"<details><summary>(.*?)</summary>(.*?)</details>", s, re.S)
        objs.append({"@type": "ContactPage", "url": url, "name": name, "about": {"@id": ORG_ID}})
        if faqs:
            objs.append({"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": html.unescape(re.sub(r"<[^>]+>", "", q)).strip(),
                 "acceptedAnswer": {"@type": "Answer",
                                    "text": " ".join(html.unescape(re.sub(r"<[^>]+>", " ", a)).split())}}
                for q, a in faqs]})
    elif slug in SOLUTIONS or slug in INDUSTRIES:
        svc = {"@type": "Service", "name": name, "description": desc, "url": url, "provider": {"@id": ORG_ID},
               "areaServed": {"@type": "Country", "name": "Canada"}}
        if slug in INDUSTRIES:
            svc["name"] = f"Consulting for {name}"
            svc["audience"] = {"@type": "BusinessAudience", "name": name}
        else:
            svc["serviceType"] = name
        objs.append(svc)
    elif base == "challenge-page":
        objs.append({"@type": "Course", "name": h1, "description": desc, "url": url,
                     "provider": {"@type": "Organization", "@id": ORG_ID, "name": "Chmltech Ltd.", "sameAs": SITE + "/"},
                     "isAccessibleForFree": True, "inLanguage": "en",
                     "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Online",
                                           "courseWorkload": "PT2H"},
                     "offers": {"@type": "Offer", "price": 0, "priceCurrency": "CAD", "category": "Free"}})
    elif re.search(r'class="embed-frame"[^>]*src="exams/', s):
        objs.append({"@type": "Quiz", "name": name, "description": desc, "url": url,
                     "isAccessibleForFree": True, "provider": {"@id": ORG_ID}, "educationalLevel": "Professional"})
    elif rel in ("insights.html", "training.html", "courses.html"):
        objs.append({"@type": "CollectionPage", "name": name, "description": desc, "url": url,
                     "publisher": {"@id": ORG_ID}})
    elif rel == "llm-leaderboard.html":
        pass  # page already carries Dataset data
    return objs

def enrich_article(s, url, image, title, rel):
    """Add image, dateModified, author url and publisher logo to the existing article JSON-LD."""
    def fix(m):
        raw = m.group(1)
        try: d = json.loads(raw)
        except Exception: return m.group(0)
        items = d if isinstance(d, list) else [d]
        changed = False
        for it in items:
            if it.get("@type") not in ("BlogPosting", "ScholarlyArticle", "Article"): continue
            if image and "image" not in it: it["image"] = image; changed = True
            if "datePublished" in it and "dateModified" not in it:
                it["dateModified"] = it["datePublished"]; changed = True
            a = it.get("author")
            if isinstance(a, dict) and a.get("name") == "Quak Foo Lee" and "url" not in a:
                it["author"] = AUTHOR_REF; changed = True
            p = it.get("publisher")
            if isinstance(p, dict) and "logo" not in p:
                it["publisher"] = ORG_REF; changed = True
            if it.get("mainEntityOfPage") != url: it["mainEntityOfPage"] = url; changed = True
        if not changed: return m.group(0)
        bump("article schema enriched")
        out = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
        return f'<script type="application/ld+json">{out}</script>'
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)

def article_dates(s):
    pub = g(r'"datePublished":\s*"([^"]+)"', s)
    mod = g(r'"dateModified":\s*"([^"]+)"', s) or pub
    return pub, mod

def process(rel, sitemap, llms):
    s = rd(rel)
    orig = s
    if re.search(r'<meta name="robots" content="noindex', s) and not rel.startswith("exams/"):
        return
    if rel == "404.html":
        return
    # 7. embedded exam apps
    if rel.startswith("exams/"):
        parent = rel.split("/", 1)[1]
        canon = clean_url(parent)
        head_end = s.find("</head>")
        add = ""
        if 'name="robots"' not in s[:head_end]:
            add += '<meta name="robots" content="noindex, indexifembedded">\n'
        if 'rel="canonical"' not in s[:head_end]:
            add += f'<link rel="canonical" href="{canon}">\n'
        if add:
            s = s[:head_end] + add + s[head_end:]; bump("exam apps noindex+canonical")
        if s != orig: wr(rel, s)
        return

    head_end = s.find("</head>")
    head, body = s[:head_end], s[head_end:]
    url = clean_url(rel)
    is_post = rel.startswith("post/")

    # 1. canonical + og:url
    new = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head, count=1)
    if new != head: bump("canonical -> clean URL"); head = new
    if 'rel="canonical"' not in head:
        head += f'<link rel="canonical" href="{url}">\n'; bump("canonical added")

    # 3. title (keyword table first, then the long-title rule)
    kw = KEYWORDS.get(rel, {})
    title = g(r"<title>(.*?)</title>", head)
    if kw.get("title"): newt = kw["title"]
    elif rel == "index.html": newt = HOME_TITLE
    elif len(title) > 60 and title.endswith(BRAND): newt = title[: -len(BRAND)]
    else: newt = title
    if newt != title:
        head = re.sub(r"<title>.*?</title>", lambda m: f"<title>{esc(newt)}</title>", head, count=1, flags=re.S)
        bump("title changed"); title = newt
    head = set_meta(head, "property", "og:title", title.replace(BRAND, ""))

    # 4. description
    desc = g(r'<meta name="description" content="([^"]*)"', head)
    if kw.get("desc") and desc != kw["desc"]:
        desc = kw["desc"]
        head = set_meta(head, "name", "description", desc)
        head = set_meta(head, "property", "og:description", desc); bump("keyword description")
    if desc and len(desc) > 160:
        nd = trim_desc(desc)
        head = set_meta(head, "name", "description", nd)
        head = set_meta(head, "property", "og:description", nd)
        bump("description trimmed"); desc = nd

    image = g(r'<meta property="og:image" content="([^"]*)"', head)
    if not image:
        image = f"{SITE}/assets/img/chmltech-mark.png"
        head = set_meta(head, "property", "og:image", image); bump("og:image added")
    if 'property="og:title"' not in head:
        head = set_meta(head, "property", "og:title", title.replace(BRAND, ""))
    if 'property="og:description"' not in head and desc:
        head = set_meta(head, "property", "og:description", desc)
    if 'property="og:site_name"' not in head:
        head = set_meta(head, "property", "og:site_name", "Chmltech Ltd.")
    if 'property="og:url"' not in head:
        head = set_meta(head, "property", "og:url", url); bump("og:url added")
    else:
        head = set_meta(head, "property", "og:url", url)
    if 'property="og:locale"' not in head:
        head = set_meta(head, "property", "og:locale", "en_CA")

    # 2. article metadata + twitter
    pub, mod = article_dates(s)
    if is_post:
        head = set_meta(head, "property", "og:type", "article")
        if pub:
            head = set_meta(head, "property", "article:published_time", pub)
            head = set_meta(head, "property", "article:modified_time", mod)
        if 'property="article:author"' not in head:
            head = set_meta(head, "property", "article:author", f"{SITE}/about")
    if 'name="twitter:card"' not in head:
        head = set_meta(head, "name", "twitter:card", "summary_large_image"); bump("twitter:card added")

    # 6. article cover image
    if is_post:
        h1 = re.sub(r"<[^>]+>", "", g(r"<h1[^>]*>(.*?)</h1>", body)) or title
        def cover(m):
            tag = m.group(0)
            if 'alt=""' in tag: tag = tag.replace('alt=""', f'alt="{esc(h1)}"', 1)
            if "fetchpriority" not in tag: tag = tag.replace("<img ", '<img fetchpriority="high" ', 1)
            return tag
        nb = re.sub(r'(?<=<div class="container post-cover">)<img\b[^>]*>', cover, body, count=1)
        if nb != body: bump("cover image alt/priority"); body = nb

    # 10. keyword H1: search phrase as the H1, the old heading (slogan) kept just below it
    if kw.get("h1"):
        m = re.search(r"<h1\b([^>]*)>(.*?)</h1>", body, re.S)
        if m and "data-kw" not in m.group(1):
            old_h1 = m.group(2).strip()
            slogan = kw.get("slogan", None)
            slogan_html = esc(slogan) if slogan else (old_h1 if slogan is None else "")
            rep = f'<h1{m.group(1)} data-kw="1">{esc(kw["h1"])}</h1>'
            if slogan_html:
                rep += f'<p class="hero-slogan">{slogan_html}</p>'
            body = body[:m.start()] + rep + body[m.end():]; bump("keyword H1")
    if kw.get("eyebrow"):
        body = re.sub(r'<p class="eyebrow">[^<]*</p>', lambda m: f'<p class="eyebrow">{esc(kw["eyebrow"])}</p>', body, count=1)

    s = head + body
    # 5. structured data
    if is_post:
        s = enrich_article(s, url, image, title, rel)
    objs = build_ld(rel, s, title, desc, url, image)
    block = ld_block(objs) if objs else ""
    if 'data-seo="v1"' in s:
        s = re.sub(r'<script type="application/ld\+json" data-seo="v1">.*?</script>\n?',
                   lambda m: block + "\n" if block else "", s, count=1, flags=re.S)
    elif block:
        i = s.find("</head>"); s = s[:i] + block + "\n" + s[i:]; bump("JSON-LD added")

    # 9. analytics (Microsoft Clarity), on indexable pages only
    s = re.sub(r'<script>\(function\(c,l,a,r,i,t,y\).*?</script>\n?', "", s, flags=re.S)
    if CLARITY:
        i = s.find("</head>"); s = s[:i] + CLARITY + "\n" + s[i:]
    if s != orig: wr(rel, s); bump("pages changed")

    lastmod = mod if (is_post and mod) else git_date(rel)
    pri = sitemap_priority(rel)
    sitemap.append((url, lastmod, pri))
    llms.append((rel, title.replace(BRAND, ""), desc, url))

def sitemap_priority(rel):
    if rel == "index.html": return "1.0"
    if "/" not in rel and rel in ("solutions.html", "insights.html", "training.html", "courses.html",
                                   "about.html", "contact.html", "book.html", "industries.html",
                                   "llm-leaderboard.html", "funding.html", "projects.html"): return "0.9"
    if rel.startswith("post/"): return "0.7"
    return "0.6"

def write_sitemap(entries):
    entries.sort(key=lambda e: (-float(e[2]), e[0]))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lm, pri in entries:
        lmx = f"<lastmod>{lm}</lastmod>" if lm else ""
        lines.append(f"  <url><loc>{u}</loc>{lmx}<priority>{pri}</priority></url>")
    lines.append("</urlset>")
    wr("sitemap.xml", "\n".join(lines) + "\n")

def write_llms(entries):
    by = {"core": [], "solutions": [], "industries": [], "post": [], "courses": [], "exams": []}
    for rel, t, d, u in entries:
        slug = rel.rsplit("/", 1)[-1][:-5]
        if rel.startswith("post/"): by["post"].append((t, d, u))
        elif rel.startswith("challenge-page/"): by["courses"].append((t, d, u))
        elif slug in SOLUTIONS: by["solutions"].append((t, d, u))
        elif slug in INDUSTRIES: by["industries"].append((t, d, u))
        elif "exam" in slug or slug in ("atomic-habits", "psychology-of-money", "100-days-efficient-operations-guide"):
            by["exams"].append((t, d, u))
        else: by["core"].append((t, d, u))
    out = ["# Chmltech Ltd.", "",
           "> Vancouver-based consultancy helping Canadian small and medium-sized businesses adopt AI, "
           "redesign processes, select and automate systems, and build KPI-driven operations, with "
           "chemical process engineering support (FEED, scale-up, pilot plants). The site also offers "
           "free articles, research papers, interactive courses, practice exams and an LLM leaderboard.", "",
           "Author of the articles: Quak Foo Lee, CEO and Principal Consultant. Contact: https://www.chmltech.com/contact", ""]
    for key, head in [("core", "Main pages"), ("solutions", "Solutions"), ("industries", "Industries"),
                      ("courses", "Free courses"), ("exams", "Free practice exams"), ("post", "Insights articles and journal papers")]:
        if not by[key]: continue
        out.append(f"## {head}"); out.append("")
        for t, d, u in sorted(by[key]):
            out.append(f"- [{t}]({u})" + (f": {d}" if d else ""))
        out.append("")
    wr("llms.txt", "\n".join(out))

def main():
    sm, ll = [], []
    for rel in pages():
        process(rel, sm, ll)
    write_sitemap(sm); write_llms(ll)
    print(f"asset versions: {assetver.stamp_all(ROOT)} pages updated")
    print(f"sitemap.xml: {len(sm)} URLs; llms.txt written")
    for k, v in sorted(stats.items()): print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
