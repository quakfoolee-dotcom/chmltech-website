"""Rewrite an existing Insights article in place, or retire one into a redirect (V4.66).

Usage:
  python3 content/gen/refresh_article.py <slug>            rewrite: keep the address, rebuild the page from
                                                            content/articles/<slug>.json, move its card to the
                                                            top of Insights and refresh its card on every page
  python3 content/gen/refresh_article.py --retire <old> <new>
                                                            retire: turn post/<old>.html into a redirect stub to
                                                            post/<new>.html, remove its card everywhere, lower the
                                                            article counts, drop it from sitemap.xml and point
                                                            links on other pages to the new address

Use the first form for an old (migrated) article that has been rewritten under the same address, so links and
search rankings are kept. Both forms are safe to run twice. Run seo_pass.py afterwards, as for any build.
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_article as A
import assetver

CARD_RE = r'<article class="article"(?:(?!</article>).)*?href="(?:\.\./)?post/{slug}\.html".*?</article>'


def pages():
    return glob.glob(os.path.join(A.ROOT, "*.html")) + glob.glob(os.path.join(A.ROOT, "post", "*.html"))


def counts(s, cats, n):
    """Raise (n=1) or lower (n=-1) the article counts in insights.html for one article."""
    s = A.bump(s, r"(>All \()(\d+)(\)<)", n)
    for c in cats:
        s = A.bump(s, r'(data-cat="' + c + r'" aria-pressed="false">[^<(]*\()(\d+)(\)<)', n)
    s = A.bump(s, r'(content=")(\d+)( articles from Chmltech)', n)
    s = A.bump(s, r'(<p class="lead">)(\d+)( articles on)', n)
    s = A.bump(s, r'(placeholder="Search )(\d+)( articles")', n)
    s = A.bump(s, r'(data-count aria-live="polite">)(\d+)( articles<)', n)
    return s


def take_card(s, slug):
    m = re.search(CARD_RE.format(slug=re.escape(slug)), s, re.S)
    if not m: return s, None
    cats = re.search(r'data-cats="([^"]*)"', m.group(0)).group(1).split()
    return s[:m.start()] + s[m.end():], cats


def rewrite(slug):
    a = json.load(open(os.path.join(A.ROOT, "content", "articles", slug + ".json"), encoding="utf-8"))
    p = os.path.join(A.ROOT, "insights.html")
    s = assetver.strip(open(p, encoding="utf-8").read())
    first = re.search(r'<div class="grid grid-3" data-items>\s*<article class="article".*?</article>', s, re.S).group(0)
    if f'href="post/{slug}.html"' in first and A.card(a) in first:
        print(f"{slug}: already at the top of Insights")
    else:
        s, cats = take_card(s, slug)
        if cats: s = counts(s, cats, -1)
        open(p, "w", encoding="utf-8").write(s)
    sys.argv = ["add_article.py", slug]
    A.main()                                                  # writes the page and cover, adds the card on top
    new = A.card(a, "../"); n = 0
    for f in pages():
        if f.endswith(os.sep + "insights.html"): continue
        h = open(f, encoding="utf-8").read()
        pre = "../" if os.sep + "post" + os.sep in f else ""
        t = re.sub(CARD_RE.format(slug=re.escape(slug)), lambda m: A.card(a, pre), h, flags=re.S)
        if t != h: open(f, "w", encoding="utf-8").write(t); n += 1
    print(f"{slug}: card refreshed on {n} other pages")


STUB = ('<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><title>{title} | Chmltech Ltd.</title>\n'
        '<meta name="robots" content="noindex"><link rel="canonical" href="{site}/post/{new}">\n'
        '<meta http-equiv="refresh" content="0; url={new}.html"><script>location.replace("{new}.html"+location.search+location.hash)</script></head>\n'
        '<body><p>This article has moved to <a href="{new}.html">{title}</a>.</p></body></html>')


def retire(old, new):
    na = json.load(open(os.path.join(A.ROOT, "content", "articles", new + ".json"), encoding="utf-8"))
    p = os.path.join(A.ROOT, "insights.html")
    s = assetver.strip(open(p, encoding="utf-8").read())
    s, cats = take_card(s, old)
    if cats:
        s = counts(s, cats, -1); open(p, "w", encoding="utf-8").write(s)
    total = int(re.search(r">All \((\d+)\)<", s).group(1))
    n = 0
    for f in pages():
        if f.endswith(os.sep + "insights.html") or f.endswith(old + ".html"): continue
        h = open(f, encoding="utf-8").read()
        t = re.sub(CARD_RE.format(slug=re.escape(old)), "", h, flags=re.S)
        t = t.replace(f"post/{old}.html", f"post/{new}.html").replace(f'href="{old}.html"', f'href="{new}.html"')
        t = re.sub(r"All \d+ articles", f"All {total} articles", t)
        if t != h: open(f, "w", encoding="utf-8").write(t); n += 1
    open(os.path.join(A.ROOT, "post", old + ".html"), "w", encoding="utf-8").write(
        STUB.format(title=A.E(na["title"]), site=A.SITE, new=new))
    sm = os.path.join(A.ROOT, "sitemap.xml"); x = open(sm, encoding="utf-8").read()
    x = re.sub(r"\s*<url><loc>" + re.escape(f"{A.SITE}/post/{old}") + r"</loc>.*?</url>", "", x, flags=re.S)
    open(sm, "w", encoding="utf-8").write(x)
    print(f"{old}: retired to {new}; {n} pages updated; Insights now lists {total} articles")


if __name__ == "__main__":
    if sys.argv[1] == "--retire": retire(sys.argv[2], sys.argv[3])
    else: rewrite(sys.argv[1])
