"""Contents list for long Insights articles (V4.75).

Any post page with an Insights article layout (<article class="prose"> and <aside class="aside-sticky">) and at least
MIN_SECTIONS main section headings and MIN_WORDS words gets:
  - a "Contents" card at the top of the right-hand sidebar (sticky on desktop, like the journal papers), and
  - a collapsed "Contents" link list at the top of the article, shown only below 1000 px wide, where the sidebar
    stops being sticky and moves under the article.
The list is built from the article's <h2> headings; headings without an id get one. Journal papers keep their own
contents card and are skipped. Safe to run twice: both blocks carry data-toc and are rebuilt each time.

Runs from seo_pass.py on every build, so rebuilt pages (add_article, refresh_article) always get it back.
Usage on its own:  python3 content/gen/article_toc.py
"""
import glob, html, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
MIN_SECTIONS = 5
MIN_WORDS = 1200          # shorter posts are quick to scroll and do not need one
SKIP = {"contents", "related reading", "related articles"}          # never listed
TAIL = {"sources", "references", "list of references"}             # listed, but not counted toward MIN_SECTIONS
H2 = re.compile(r'<h2(\s[^>]*)?>(.*?)</h2>', re.S)


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60] or "section"


def text(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()


def build(s):
    s = re.sub(r'\s*<div class="card a-toc" data-toc.*?</ol></div>', "", s, flags=re.S)
    s = re.sub(r'\s*<details class="a-toc-m" data-toc.*?</details>', "", s, flags=re.S)
    m = re.search(r'(<article class="prose">)(.*?)(</article>)', s, re.S)
    if not m or '<aside class="aside-sticky">' not in s:
        return s, 0
    body, used, items = m.group(2), set(re.findall(r'\sid="([^"]+)"', s)), []

    def rep(h):
        attrs, inner = h.group(1) or "", h.group(2)
        t = text(inner)
        if t.lower() in SKIP or not t:
            return h.group(0)
        idm = re.search(r'\sid="([^"]+)"', attrs)
        if idm:
            hid = idm.group(1)
        else:
            base = hid = slug(t); k = 2
            while hid in used: hid = f"{base}-{k}"; k += 1
            used.add(hid); attrs = f' id="{hid}"' + attrs
        lab = re.search(r'\sdata-toc-label="([^"]+)"', attrs)
        items.append((hid, html.unescape(lab.group(1)) if lab else t))
        return f"<h2{attrs}>{inner}</h2>"

    new = H2.sub(rep, body)
    words = len(re.sub(r"<svg.*?</svg>|<[^>]+>", " ", body, flags=re.S).split())
    if sum(t.lower() not in TAIL for _, t in items) < MIN_SECTIONS or words < MIN_WORDS:
        return s, 0
    ol = "<ol>" + "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in items) + "</ol>"
    card = f'\n    <div class="card a-toc" data-toc aria-label="Contents"><p class="eyebrow">Contents</p>{ol}</div>'
    mob = f'<details class="a-toc-m" data-toc><summary>Contents</summary>{ol}</details>\n'
    # mobile list after a dated update note, if the article opens with one
    note = re.match(r'\s*<blockquote data-note=.*?</blockquote>\s*', new, re.S)
    at = note.end() if note else 0
    new = new[:at] + mob + new[at:]
    s = s[:m.start(2)] + new + s[m.end(2):]
    s = s.replace('<aside class="aside-sticky">', '<aside class="aside-sticky">' + card, 1)
    return s, len(items)


def run(root=ROOT):
    n = 0
    for p in sorted(glob.glob(os.path.join(root, "post", "*.html"))):
        s = open(p, encoding="utf-8").read()
        t, k = build(s)
        if k: n += 1
        if t != s: open(p, "w", encoding="utf-8").write(t)
    return n


if __name__ == "__main__":
    print(f"contents lists on {run()} articles")
