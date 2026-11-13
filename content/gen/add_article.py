"""Add one Insights article to the built site without a full rebuild (V4.27).

Usage:  python3 content/gen/add_article.py <slug> [--fonts DIR]

Reads content/articles/<slug>.json and:
  - writes post/<slug>.html (page shell taken from an existing article),
  - draws the cover and thumbnail in assets/media/covers/,
  - adds the card at the top of insights.html and raises the article counts,
  - adds the address to sitemap.xml.
It is safe to run twice: the second run rewrites the post and cover and leaves the counts alone.
The cover uses Space Grotesk. Pass --fonts with a folder holding SpaceGrotesk-SemiBold.ttf and
SpaceGrotesk-Medium.ttf; without it the cover falls back to Inter or DejaVu.
"""
import glob, html, json, os, re, sys
import assetver
from datetime import date, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SITE = "https://www.chmltech.com"
SHELL = "iso-9001-document-and-revision-control"      # an existing article used as the page shell
CAT_NAMES = {"process-improvement": "Process Improvement", "operational-efficiency": "Operational Efficiency",
             "artificial-intelligence": "Artificial Intelligence", "digital-technology": "Digital Technology",
             "marketing": "Sales & Marketing", "lean": "Lean", "chmltech-online-journal": "Chmltech Online Journal",
             "change-management": "Change Management", "iso": "ISO", "six-sigma": "Six Sigma", "process-engineering": "Process Engineering", "esg": "ESG",
             "strategy": "Strategy", "erp": "ERP", "project-management": "Project Management",
             "book-review": "Book Review", "agile": "Agile", "case-study": "Case Study", "inventory-management": "Inventory Management"}
E = lambda s: html.escape(s, quote=True)


def rd(p): return assetver.strip(open(os.path.join(ROOT, p), encoding="utf-8").read())
def wr(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def nice_date(d):
    y, m, dd = map(int, d.split("-"))
    return f"{date(y, m, dd):%b} {dd}, {y}"


def series_label(a):
    """'FEED series · Part 1 of 3' for an article with a "series" field (name, part, of); empty otherwise."""
    sr = a.get("series")
    return f'{sr["name"]} · Part {sr["part"]} of {sr["of"]}' if sr else ""


CARD_SERIES = '<p class="series" style="margin:0;font-size:13px;font-weight:600;color:var(--green-dark)">'
HERO_SERIES = '<p class="series" style="margin:0;font-size:15px;font-weight:600;letter-spacing:.03em;color:var(--green)">'


def card(a, prefix=""):
    search = E(" ".join([a["title"], a["desc"], " ".join(a["tags"])]).lower())
    main = next((c for c in a["cats"] if c != "chmltech-online-journal"), a["cats"][0])
    cats = f'<p class="cat-label">{E(CAT_NAMES[main])}</p>'
    ser = CARD_SERIES + E(series_label(a)) + "</p>" if a.get("series") else ""
    return (f'<article class="article" data-cats="{" ".join(a["cats"])}" data-search="{search}"><div class="thumb">'
            f'<img src="{prefix}assets/media/covers/thumbs/{a["slug"]}.jpg" alt="" loading="lazy" decoding="async" width="600" height="338"></div>'
            f'<div class="body">{cats}{ser}<h3><a href="{prefix}post/{a["slug"]}.html">{E(a["title"])}</a></h3>'
            f'<p class="muted">{E(a["desc"])}</p><p class="meta">{nice_date(a["date"])} · {a["read"]}</p></div></article>')


def existing_card(slug, listing):
    m = re.search(r'<article class="article"(?:(?!</article>).)*?href="post/' + re.escape(slug) + r'\.html".*?</article>', listing, re.S)
    return m.group(0).replace('src="assets/', 'src="../assets/').replace('href="post/', 'href="../post/') if m else ""


_ORIG = None


def apply_dates(a):
    """An older post rewritten at its old address keeps its original publish date (content/articles/original_dates.json,
    V4.76); the date in its JSON becomes the 'Updated' date. Returns a for chaining."""
    global _ORIG
    if _ORIG is None:
        fp = os.path.join(ROOT, "content", "articles", "original_dates.json")
        _ORIG = json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else {}
    o = _ORIG.get(a["slug"])
    if o and a["date"] != o:
        a["updated"] = a.get("updated") or a["date"]
        a["date"] = o
    return a


def post_page(a, listing, total):
    s = rd(f"post/{SHELL}.html")
    old = json.load(open(os.path.join(ROOT, "content", "articles", SHELL + ".json"), encoding="utf-8"))
    head, rest = s.split('<article class="prose">', 1)
    _, tail = rest.split("</article>\n  <aside", 1)
    tail = "</article>\n  <aside" + tail
    for part in ("head", "tail"):
        t = head if part == "head" else tail
        t = t.replace(E(old["title"]), E(a["title"])).replace(old["title"], E(a["title"]))
        t = t.replace(E(old["desc"]), E(a["desc"])).replace(old["desc"], E(a["desc"]))
        t = t.replace(SHELL, a["slug"])
        if part == "head": head = t
        else: tail = t
    head = re.sub(r'<div class="tags">.*?</div>',
                  '<div class="tags">' + "".join(f'<a href="../insights.html#cat={c}">{E(CAT_NAMES[c])}</a>' for c in a["cats"]) + "</div>", head, count=1)
    if a.get("series"):                                    # series label between the category tags and the headline
        head = head.replace('</div>\n    <h1', '</div>\n    ' + HERO_SERIES + E(series_label(a)) + '</p>\n    <h1', 1)
        assert HERO_SERIES in head
    head = re.sub(r'<p class="post-meta">.*?</p>',
                  f'<p class="post-meta"><span>{E(a["author"])}</span><span>{nice_date(a["date"])}</span>'
                  + (f'<span>Updated {nice_date(a["updated"])}</span>' if a.get("updated") else "") + f'<span>{a["read"]}</span></p>', head, count=1)
    tail = re.sub(r'(<p class="eyebrow">Tags</p><div class="tags">).*?(</div>)',
                  lambda m: m.group(1) + "".join(f"<span>{E(t)}</span>" for t in a["tags"]) + m.group(2), tail, count=1)
    rel = "".join(existing_card(sl, listing) for sl in a.get("related", []))
    tail = re.sub(r'(<div class="grid grid-3">).*?(</div>\n</div></section>\n<script type="application/ld\+json">)',
                  lambda m: m.group(1) + rel + m.group(2), tail, count=1, flags=re.S)
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["title"], "datePublished": a["date"],
          **({"dateModified": a["updated"]} if a.get("updated") else {}),
          "author": {"@type": "Person", "name": a["author"]}, "publisher": {"@type": "Organization", "name": "Chmltech Ltd."},
          "mainEntityOfPage": f"{SITE}/post/{a['slug']}", "description": a["desc"]}
    tail = re.sub(r'<script type="application/ld\+json">.*?</script>',
                  lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", tail, count=1, flags=re.S)
    tail = re.sub(r"All \d+ articles", f"All {total} articles", tail)
    wr(f"post/{a['slug']}.html", head + '<article class="prose">\n' + a["body"].rstrip("\n") + "\n  " + tail)


def bump(s, pat, n=1):
    return re.sub(pat, lambda m: m.group(1) + str(int(m.group(2)) + n) + m.group(3), s)


def listing_page(a):
    s = rd("insights.html")
    if f'href="post/{a["slug"]}.html"' in s:
        return s, int(re.search(r">All \((\d+)\)<", s).group(1)), False
    s = bump(s, r"(>All \()(\d+)(\)<)")
    for c in a["cats"]:
        s = bump(s, r'(data-cat="' + c + r'" aria-pressed="false">[^<(]*\()(\d+)(\)<)')
    s = bump(s, r'(content=")(\d+)( articles from Chmltech)')
    s = bump(s, r'(<p class="lead">)(\d+)( articles on)')
    s = bump(s, r'(placeholder="Search )(\d+)( articles")')
    s = bump(s, r'(data-count aria-live="polite">)(\d+)( articles<)')
    # newest first: place the card before the first card with an older date (an old post rewritten keeps its place)
    grid = s.index('<div class="grid grid-3" data-items>')
    at = None
    for m in re.finditer(r'<article class="article".*?<p class="meta">([A-Z][a-z]{2}) (\d+), (\d{4})', s[grid:], re.S):
        d = datetime.strptime(" ".join(m.groups()), "%b %d %Y").strftime("%Y-%m-%d")
        if d < a["date"]:
            at = grid + m.start(); break
    if at is None:
        s = s.replace('<div class="grid grid-3" data-items>\n  ', '<div class="grid grid-3" data-items>\n  ' + card(a), 1)
    else:
        s = s[:at] + card(a) + s[at:]
    return s, int(re.search(r">All \((\d+)\)<", s).group(1)), True


def cover(a, fonts=None):
    """Cover image for an Insights article; drawn by covers.py (one motif per subject family, V4.63). `fonts` is unused."""
    import covers
    covers.cover(a["slug"], a["title"], a["cats"], a.get("cover_label", CAT_NAMES[a["cats"][0]]))

def main():
    slug = sys.argv[1]
    fonts = sys.argv[sys.argv.index("--fonts") + 1] if "--fonts" in sys.argv else None
    a = apply_dates(json.load(open(os.path.join(ROOT, "content", "articles", slug + ".json"), encoding="utf-8")))
    listing, total, added = listing_page(a)
    post_page(a, rd("insights.html"), total)
    cover(a, fonts)
    if added:
        wr("insights.html", listing)
        for f in glob.glob(os.path.join(ROOT, "post", "*.html")):   # "All N articles" button on every article
            s = open(f, encoding="utf-8").read(); t = re.sub(r"All \d+ articles", f"All {total} articles", s)
            if t != s: open(f, "w", encoding="utf-8").write(t)
        sm = rd("sitemap.xml"); loc = f"  <url><loc>{SITE}/post/{slug}</loc></url>\n"
        if loc not in sm:
            i = sm.index(f"  <url><loc>{SITE}/post/")
            wr("sitemap.xml", sm[:i] + loc + sm[i:])
    print(f"{slug}: post written, cover drawn, listing {'updated' if added else 'unchanged'} ({total} articles)")


if __name__ == "__main__":
    main()
