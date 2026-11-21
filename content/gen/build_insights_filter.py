"""Insights filter (sidebar facets) — V2, 2026-11-21; first published in site V5.62.

Replaces the Insights search toolbar and 19 category chips with the sidebar filter (assets/js/insights-filter.js,
assets/css/insights-filter.css). The article cards are left exactly as they are: the script reads format, date,
read time, series, part and journal division from the card text, so add_article.py, add_journal_paper.py,
refresh_article.py and insights_finder.py keep working on the page.

Markup kept for the build scripts:  <div class="grid grid-3" data-items>, placeholder="Search N articles",
data-count aria-live="polite">N articles<, and data-total="N" (the article total; add_article.py reads and raises it).

  python3 content/gen/build_insights_filter.py --publish        rewrite insights.html in place (safe to re-run)
  python3 content/gen/build_insights_filter.py --draft OUT      noindex draft page with a banner, for review
  python3 content/gen/build_insights_filter.py --preview OUT    one self-contained file (CSS, JS, images inside)

After --publish run assetver.py so the new files get version strings, as for any page change.
Replaces content/gen/build_insights_filter_draft.py (Draft V1).
"""
import argparse, base64, io, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = "https://www.chmltech.com/"


def shell(n, grid):
    sel = lambda k: f'<span class="ifl-n" data-seln="{k}" hidden></span>'
    return f'''<section class="section" style="padding-top:64px" id="browse"><div class="container" data-ifl data-total="{n}">
  <h2 style="margin:0 0 24px">Browse all articles</h2>
  <div class="ifl">
    <div class="ifl-bd" data-bd></div>
    <div class="ifl-side" id="ifl-side" role="complementary" aria-label="Filter articles" data-side>
      <div class="ifl-sheet-head"><h2 id="ifl-sheet-title">Filters</h2><button type="button" class="ifl-link" data-close>Close</button></div>
      <div class="ifl-body">
        <div class="ifl-head"><h2>Filters</h2><button type="button" class="ifl-link" data-clear hidden>Clear all</button></div>
        <details class="ifl-group" open><summary>Format{sel("f")}</summary><div class="ifl-opts" role="radiogroup" aria-label="Format" data-f></div></details>
        <details class="ifl-group" open data-dvwrap hidden><summary>Journal division{sel("dv")}</summary><div class="ifl-opts" role="radiogroup" aria-label="Journal division" data-dv></div></details>
        <details class="ifl-group" open><summary>Topic{sel("t")}</summary><div class="ifl-opts" role="group" aria-label="Topic" data-t></div></details>
        <details class="ifl-group" data-swrap><summary>Series{sel("s")}</summary><div class="ifl-opts" role="radiogroup" aria-label="Series" data-s></div></details>
        <details class="ifl-group" data-rtwrap><summary>Reading time{sel("rt")}</summary><div class="ifl-opts" role="radiogroup" aria-label="Reading time" data-rt></div></details>
        <details class="ifl-group" data-ywrap><summary>Published{sel("y")}</summary><div class="ifl-opts" role="radiogroup" aria-label="Published" data-y></div></details>
      </div>
      <div class="ifl-sheet-foot"><button type="button" class="btn btn-ghost" data-clear>Clear all</button><button type="button" class="btn" data-close data-showbtn>Show articles</button></div>
    </div>
    <div>
      <div class="ifl-mbar"><button type="button" class="btn btn-ghost" data-open aria-expanded="false" aria-controls="ifl-side">Filters<span class="ifl-badge" data-badge hidden></span></button></div>
      <div class="ifl-tools">
        <label class="search"><span class="visually-hidden">Search articles</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><input type="search" placeholder="Search {n} articles" maxlength="200" data-q></label>
        <label class="ifl-sort"><span>Sort</span><select data-sort></select></label>
      </div>
      <div class="ifl-res" data-res>
        <p class="ifl-count" role="status" data-count aria-live="polite">{n} articles</p>
        <ul class="ifl-act" data-act aria-label="Active filters"></ul>
        <button type="button" class="ifl-link" data-clear hidden>Clear all</button>
        <span class="sp"></span>
        <button type="button" class="ifl-link" data-copy>Copy link to this view</button><span class="ifl-copied" data-copied role="status" hidden>Link copied</span>
      </div>
      <div class="ifl-sintro" data-sintro hidden></div>
{grid}
      <div class="ifl-empty" data-empty><b data-emptytitle>No articles match these filters.</b><span data-emptyhint></span> <button type="button" class="ifl-link" data-clear>Clear all filters</button></div>
      <div class="ifl-morewrap" data-morewrap><button type="button" class="btn btn-ghost" data-more>Show more articles</button><small data-moreinfo></small></div>
    </div>
  </div>
</div></section>'''


def section_bounds(src):
    for marker in ('<section class="section" style="padding-top:64px" id="browse">',
                   '<section class="section" style="padding-top:64px"><div class="container" data-list="posts"'):
        if marker in src:
            start = src.index(marker)
            return start, src.index("</div></section>", src.index("<div class=\"grid grid-3\" data-items>", start)) + len("</div></section>")
    raise SystemExit("insights.html: article list section not found")


def grid_block(section):
    """The card grid, copied verbatim (whitespace included, so add_article.py still finds its insertion point)."""
    g0 = section.index('<div class="grid grid-3" data-items>')
    line0 = section.rfind("\n", 0, g0) + 1
    last = section.rindex("</article>") + len("</article>")
    end = section.index("</div>", last) + len("</div>")
    return section[line0:end], section[g0:end].count('<article class="article"')


def build(src):
    start, end = section_bounds(src)
    grid, n = grid_block(src[start:end])
    page = src[:start] + shell(n, grid) + src[end:]
    if 'assets/css/insights-filter.css' not in page:
        page = page.replace('<link rel="stylesheet" href="assets/css/insights-finder.css',
                            '<link rel="stylesheet" href="assets/css/insights-filter.css">\n<link rel="stylesheet" href="assets/css/insights-finder.css', 1)
    if 'assets/js/insights-filter.js' not in page:
        page = page.replace('<script src="assets/js/insights-finder.js',
                            '<script src="assets/js/insights-filter.js" defer></script>\n<script src="assets/js/insights-finder.js', 1)
    return page, n


DRAFT_BAR = ('<div style="background:#FFF4D6;border-bottom:1px solid #E9D49A;color:#5B4708;font-size:14px;padding:9px 0" role="note">'
             '<div class="container"><b style="color:#3d2f04">{label}</b> — preview only, not linked from the site. '
             'Same articles, cards and "Start here" panel as the live page; only the filter changes.</div></div>\n')


def draft(page, label):
    page = page.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
    return page.replace('<main id="main">', DRAFT_BAR.format(label=label) + '<main id="main">', 1)


def self_contained(page):
    """Everything in one file, because sandboxed previewers block files from other sites.
    Order matters (red team M5): page links are rewritten BEFORE the scripts are inlined."""
    from PIL import Image
    page = re.sub(r'<link rel="(?:icon|apple-touch-icon|preconnect)"[^>]*>\n?', "", page)
    page = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*">\n?', "", page)
    page = re.sub(r'<script>\(function\(c,l,a,r,i,t,y\).*?</script>\n?', "", page, flags=re.S)       # no analytics in a preview
    page = re.sub(r'href="(?!https?:|#|mailto:|tel:|data:|//|assets/css/)([^"]+)"',
                  lambda m: f'href="{SITE}{m.group(1)}" target="_blank" rel="noopener"', page)
    cache = {}
    def img(m):
        path = re.sub(r"\?.*$", "", m.group(1))
        if path not in cache:
            f = ROOT / path
            if path.endswith(".png"):
                cache[path] = "data:image/png;base64," + base64.b64encode(f.read_bytes()).decode()
            else:
                im = Image.open(f).convert("RGB"); im.thumbnail((480, 480))
                buf = io.BytesIO(); im.save(buf, "JPEG", quality=72, optimize=True, progressive=True)
                cache[path] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        return 'src="' + cache[path] + '"'
    page = re.sub(r'src="(assets/(?:img|media)/[^"]+\.(?:png|jpe?g)(?:\?[^"]*)?)"', img, page)
    page = re.sub(r'<link rel="stylesheet" href="(assets/css/[^"?]+)[^"]*">',
                  lambda m: "<style>\n" + (ROOT / m.group(1)).read_text(encoding="utf-8") + "\n</style>", page)
    page = re.sub(r'<script src="(assets/js/[^"?]+)[^"]*" defer></script>',
                  lambda m: "<script>\n" + (ROOT / m.group(1)).read_text(encoding="utf-8").replace("</script", "<\\/script") + "\n</script>", page)
    return page


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--publish", action="store_true", help="rewrite insights.html in place")
    ap.add_argument("--draft", help="write a noindex draft page")
    ap.add_argument("--preview", help="write a self-contained preview file")
    ap.add_argument("--label", default="Draft · Insights filter (sidebar)")
    a = ap.parse_args()
    src = (ROOT / "insights.html").read_text(encoding="utf-8")
    page, n = build(src)
    if a.publish:
        (ROOT / "insights.html").write_text(page, encoding="utf-8"); print(f"insights.html: filter in place, {n} cards")
    if a.draft:
        pathlib.Path(a.draft).write_text(draft(page, a.label), encoding="utf-8"); print("draft:", a.draft)
    if a.preview:
        pathlib.Path(a.preview).write_text(self_contained(draft(page, a.label)), encoding="utf-8"); print("preview:", a.preview)
