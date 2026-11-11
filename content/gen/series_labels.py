"""Show the series label ("FEED series · Part 1 of 3") on every card of a series article (V4.47).

Usage:  python3 content/gen/series_labels.py

Reads the "series" field (name, part, of) of each content/articles/*.json and adds or refreshes the label
above the title on that article's cards, on every page of the site (Insights, home, related articles,
solution and industry pages). It is safe to run twice. Run it after adding an article to a series or
changing the number of parts. The label above the headline on the article page itself is written by
add_article.py.
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from add_article import ROOT, CARD_SERIES, E, series_label

LABELS = {}
for f in glob.glob(os.path.join(ROOT, "content", "articles", "*.json")):
    a = json.load(open(f, encoding="utf-8"))
    if a.get("series"): LABELS[a["slug"]] = CARD_SERIES + E(series_label(a)) + "</p>"


def fix(m):
    blk = m.group(0)
    s = re.search(r'href="(?:\.\./)?post/([^"]+)\.html"', blk)
    if not s or s.group(1) not in LABELS: return blk
    blk = re.sub(r'<p class="series"[^>]*>.*?</p>', "", blk, count=1, flags=re.S)
    return blk.replace("<h3>", LABELS[s.group(1)] + "<h3>", 1)


n = 0
for f in glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "post", "*.html")):
    h = open(f, encoding="utf-8").read()
    t = re.sub(r'<article class="article".*?</article>', fix, h, flags=re.S)
    if t != h:
        open(f, "w", encoding="utf-8").write(t); n += 1
print(f"{len(LABELS)} series articles, cards updated on {n} pages")
