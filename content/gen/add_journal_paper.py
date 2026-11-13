"""Add one Chmltech Online Journal paper to the built site without a full rebuild (V4.53).

Usage:  python3 content/gen/add_journal_paper.py <slug>

Reads content/journal/<slug>.json (format: content/journal/SPEC.md) and:
  - writes post/<slug>.html with the journal renderer (journal_pages.build), using an existing paper page as the shell,
  - adds the card at the top of insights.html (journal + subject categories) and raises the article counts,
  - updates "All N articles" on every article page, and adds the address to sitemap.xml.
The cover (assets/media/covers/<slug>.jpg and thumbs/) must already exist. Safe to run twice.
Add the slug to TOPIC in journal_pages.py first so the paper is filed under its subject.
"""
import glob, html, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import journal_pages as jp
import add_article as aa

SITE = "https://www.chmltech.com"
SHELL = "multi-agent-ai-systems-architectures-coordination-and-failure-modes"   # an existing journal page used as the shell
E = lambda s: html.escape(s, quote=True)
rd, wr = aa.rd, aa.wr


def shell_parts():
    s = rd(f"post/{SHELL}.html")
    head, rest = s.split('<main id="main">\n', 1)
    _, tail = rest.split("</main>", 1)
    d = json.load(open(os.path.join(jp.SRC, SHELL + ".json"), encoding="utf-8"))
    head = head.replace('<link rel="stylesheet" href="../assets/css/journal.css">\n', "")
    head = re.sub(r'<meta name="citation_[a-z_]+" content="[^"]*">\n', "", head)
    head = head.replace('<meta name="twitter:card" content="summary_large_image">\n', "")
    head = head.replace(f'<meta property="og:image" content="{SITE}/assets/media/covers/{SHELL}.jpg">', f'<meta property="og:image" content="{SITE}/assets/img/chmltech-mark.png">')
    tail = tail.replace('<script src="../assets/js/journal.js" defer></script>\n', "")
    return head, tail, d


def main():
    slug = sys.argv[1]
    d = json.load(open(os.path.join(jp.SRC, slug + ".json"), encoding="utf-8"))
    head, tail, old = shell_parts()
    old_title = re.sub("<[^>]+>", "", old["title"])
    listing = rd("insights.html")

    def sub_page(path, title, desc, body):
        h = head.replace(E(old_title), E(title)).replace(old_title, E(title)).replace(E(old["meta"]), desc).replace(old["meta"], desc).replace(SHELL, slug)
        # page links in the body are written root-relative; this page lives in post/, so they need "../" (V4.63 fix:
        # the breadcrumb Home / Insights / Chmltech Online Journal links went to post/index.html and gave a 404)
        body = re.sub(r'href="(?!\.\./|https?:|#|mailto:|/)([A-Za-z0-9_-]+\.html[^"]*)"', r'href="../\1"', body)
        wr(path, h + '<main id="main">\n' + body + "\n</main>" + tail)

    a = dict(slug=slug, title=re.sub("<[^>]+>", "", d["title"]), desc=d["meta"], tags=d["keywords"], date=d["published"][:10],
             read=f"{max(1, round(jp.words(d) / 220))} min read")
    t = jp.TOPIC.get(slug, [])
    a["cats"] = [jp.JOURNAL_CAT] + ([t] if isinstance(t, str) else list(t))
    new_listing, total, added = aa.listing_page(a)
    if added:   # journal cards show the volume and issue before the date
        new_listing = new_listing.replace(f'<p class="meta">{aa.nice_date(a["date"])} · {a["read"]}</p></div></article>',
                                          f'<p class="meta">Vol. {d["volume"]}, Issue {d["issue"]} · {aa.nice_date(a["date"])} · {a["read"]}</p></div></article>', 1)
    # related cards: the three newest other journal papers, as listed on insights.html
    J = jp.load()
    others = sorted((x for x in J.values() if x["slug"] != slug), key=lambda x: (x["published"], x["volume"], x["issue"]), reverse=True)[:3]
    POSTS = [dict(slug=slug)] + [dict(slug=x["slug"]) for x in others]
    ns = dict(sub_page=sub_page, esc=E, card=lambda q: aa.existing_card(q["slug"], listing), POSTS=POSTS, SITE_URL=SITE, OUT=ROOT)
    real_load = jp.load
    jp.load = lambda: {slug: d}
    try:
        jp.build(ns)
    finally:
        jp.load = real_load
    fp = os.path.join(ROOT, "post", slug + ".html")
    s = open(fp, encoding="utf-8").read()
    s = s.replace('<div class="grid grid-3"></div>', '<div class="grid grid-3">' + "".join(aa.existing_card(x["slug"], listing) for x in others) + "</div>", 1)
    s = re.sub(r"All \d+ articles", f"All {total} articles", s)
    open(fp, "w", encoding="utf-8").write(s)
    if added:
        wr("insights.html", new_listing)
        for f in glob.glob(os.path.join(ROOT, "post", "*.html")):
            x = open(f, encoding="utf-8").read(); y = re.sub(r"All \d+ articles", f"All {total} articles", x)
            if y != x: open(f, "w", encoding="utf-8").write(y)
        sm = rd("sitemap.xml"); loc = f"  <url><loc>{SITE}/post/{slug}</loc></url>\n"
        if loc not in sm:
            i = sm.index(f"  <url><loc>{SITE}/post/"); wr("sitemap.xml", sm[:i] + loc + sm[i:])
    import covers   # cover in the subject's motif, footer naming the volume and issue (V4.63)
    covers.cover(slug, a["title"], a["cats"], jp.JOURNAL, f"Vol. {d['volume']}, Issue {d['issue']}")
    print(f"{slug}: page written, listing {'updated' if added else 'unchanged'} ({total} articles)")


if __name__ == "__main__":
    main()
