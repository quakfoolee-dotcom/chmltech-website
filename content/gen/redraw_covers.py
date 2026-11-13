"""Redraw every generated cover in the subject-family style (V4.63). Usage: python3 -I content/gen/redraw_covers.py

Covers to redraw = Insights cards whose image is in assets/media/covers/. Title, categories and volume/issue come from
insights.html and the journal JSON; eyebrow labels from the articles' "cover_label" (else the first category's name).
"""
import glob, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import covers, add_article as aa, journal_pages as jp
R = covers.ROOT

labels = {}
for f in glob.glob(os.path.join(R, "content/articles/*.json")) + glob.glob(os.path.join(R, "content/articles/*.py")):
    t = open(f, encoding="utf-8").read()
    for m in re.finditer(r'["\']slug["\']\s*[:=]\s*["\']([a-z0-9-]+)["\']', t):
        nxt = re.search(r'["\']slug["\']\s*[:=]', t[m.end():]); seg = t[m.end(): m.end() + (nxt.start() if nxt else len(t))]
        lab = re.search(r'["\']cover_label["\']\s*[:=]\s*["\']([^"\']+)["\']', seg)
        if lab: labels[m.group(1)] = lab.group(1)
J = {d["slug"]: d for d in jp.load().values()}
listing = open(os.path.join(R, "insights.html"), encoding="utf-8").read()
n = fam_count = 0; fams = {}
for cats, body in re.findall(r'<article[^>]*data-cats="([^"]*)"[^>]*>(.*?)</article>', listing, re.S):
    m = re.search(r'covers/thumbs/([a-z0-9-]+)\.jpg', body)
    if not m: continue
    slug = m.group(1); cats = cats.split()
    if slug in J:
        d = J[slug]; title = re.sub("<[^>]+>", "", d["title"])
        covers.cover(slug, title, cats, jp.JOURNAL, f"Vol. {d['volume']}, Issue {d['issue']}")
    else:
        title = html.unescape(re.sub("<[^>]+>", "", re.search(r"<h3[^>]*>(.*?)</h3>", body, re.S).group(1))).strip()
        covers.cover(slug, title, cats, labels.get(slug, aa.CAT_NAMES[cats[0]]))
    f = covers.family(cats); fams[f] = fams.get(f, 0) + 1; n += 1
print(n, "covers redrawn:", fams)
