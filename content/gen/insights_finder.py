"""Insights "Start here" panel: goal buttons that open short reading lists, and a shelf of the article series.

Data: content/insights/finder.json (goals with their article slugs in reading order, series descriptions).
Titles, read times, categories and series labels are read from the article cards already on insights.html,
so the panel always matches the listing. Script and styles: assets/js/insights-finder.js, assets/css/insights-finder.css.

Run from the site root:  python3 content/gen/insights_finder.py .
then run content/gen/seo_pass.py as usual. Safe to run any number of times: the panel sits between
<!-- insights-finder:start --> and <!-- insights-finder:end --> and is rebuilt each time.
Run it again after adding an article that belongs in a list or a series.
"""
import html
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
PAGE = os.path.join(ROOT, "insights.html")
E = lambda t: html.escape(t, quote=True)

fd = json.load(open(os.path.join(ROOT, "content", "insights", "finder.json"), encoding="utf-8"))
s = open(PAGE, encoding="utf-8").read()
s = re.sub(r"<!-- insights-finder:start -->.*?<!-- insights-finder:end -->\n?", "", s, flags=re.S)

# ---- article cards on the page ----------------------------------------------
cards = {}
for cats, body in re.findall(r'<article class="article" data-cats="([^"]*)".*?<div class="body">(.*?)</div></article>', s, flags=re.S):
    slug = re.search(r'href="post/([^"]+)\.html"', body).group(1)
    ser = re.search(r'class="series"[^>]*>(.*?)</p>', body)
    meta = re.search(r'class="meta">(.*?)</p>', body).group(1)
    cards[slug] = dict(
        slug=slug,
        title=re.sub(r"<[^>]+>", "", re.search(r"<h3>(.*?)</h3>", body, flags=re.S).group(1)).strip(),   # already escaped
        cat=re.sub(r"<[^>]+>", "", re.search(r'class="cat-label">(.*?)</p>', body).group(1)),
        series=html.unescape(ser.group(1)) if ser else "",
        read=meta.split("·")[-1].strip(),
        mins=int(re.search(r"(\d+)", meta.split("·")[-1]).group(1)))


def item(a):
    ser = f' · <b>{E(a["series"].replace(" · ", ", "))}</b>' if a["series"] else ""
    return (f'<li><a href="post/{a["slug"]}.html">{a["title"]}</a>'
            f'<span class="if-meta">{a["read"]} · {a["cat"]}{ser}</span></li>')


def course_title(key):
    p = os.path.join(ROOT, "challenge-page", key + ".html")
    if not os.path.exists(p):
        sys.exit(f"course page challenge-page/{key}.html not found")
    return re.search(r"<h1[^>]*>(.*?)</h1>", open(p, encoding="utf-8").read(), flags=re.S).group(1).strip()


# ---- goals ------------------------------------------------------------------
buttons, panels = [], []
for g in fd["goals"]:
    missing = [x for x in g["articles"] if x not in cards]
    if missing:
        sys.exit(f'goal {g["id"]}: no card on insights.html for {missing}')
    arts = [cards[x] for x in g["articles"]]
    n = len(arts)
    buttons.append(f'<button class="if-goal" type="button" data-goal="{g["id"]}" aria-pressed="false" aria-controls="goal-{g["id"]}">'
                   f'<span>{E(g["label"])}</span><small>{n} articles</small></button>')
    foot = []
    if g.get("course"):
        foot.append(f'<a href="challenge-page/{g["course"]}.html">Free course: {course_title(g["course"])} →</a>')
    if g.get("page"):
        foot.append(f'<a href="{g["page"]}">{E(g["page_name"])} →</a>')
    if g.get("cat"):
        foot.append(f'<a href="#cat={g["cat"]}" data-cat="{g["cat"]}">All {E(g["cat_name"])} articles ↓</a>')
    panels.append(f'<div class="if-panel" id="goal-{g["id"]}" tabindex="-1" hidden>'
                  f'<h3>{E(g["label"])}</h3><p>{E(g["blurb"])} Read these {n} in order, about {sum(a["mins"] for a in arts)} minutes in all.</p>'
                  f'<ol class="if-list">{"".join(item(a) for a in arts)}</ol>'
                  f'<p class="if-foot">{"".join(foot)}</p></div>')

# ---- series -----------------------------------------------------------------
groups = {}
for a in cards.values():
    m = re.match(r"(.+?) · Part (\d+) of (\d+)", a["series"])
    if m:
        groups.setdefault(m.group(1), []).append((int(m.group(2)), a))
unknown = [k for k in groups if k not in fd["series"]]
if unknown:
    sys.exit(f"series without a description in finder.json: {unknown}")
shelf = []
for name in fd["series_order"]:
    parts = sorted(groups.get(name, []), key=lambda x: x[0])
    if not parts:
        continue
    first = parts[0][1]
    shelf.append(f'<div class="if-ser"><h4>{E(name[0].upper() + name[1:])}</h4>'
                 f'<span class="if-meta">{len(parts)} parts · {sum(a["mins"] for _, a in parts)} min</span>'
                 f'<p>{E(fd["series"][name])}</p><a href="post/{first["slug"]}.html">Start at Part 1 →</a></div>')

block = f'''<!-- insights-finder:start -->
<section class="section if-section"><div class="container">
  <div class="if">
    <div class="if-head"><p class="eyebrow">Start here</p><h2 class="h-md">What is your next business priority?</h2><p>Choose a priority and we will suggest what to read, in order.</p></div>
    <div class="if-goals" role="group" aria-label="Reading lists by goal">{"".join(buttons)}</div>
    {"".join(panels)}
    <h3 class="if-sub">Or follow a series from Part 1</h3>
    <div class="if-series">{"".join(shelf)}</div>
  </div>
</div></section>
<!-- insights-finder:end -->
'''

anchor = re.search(r'<section class="section"[^>]*><div class="container" data-list="posts"', s)
if not anchor:
    sys.exit("insights.html: article list section not found")
s = s[:anchor.start()] + block + s[anchor.start():]

# ---- stylesheet and script (added once) ---------------------------------------
if "insights-finder.css" not in s:
    s = re.sub(r'(<link rel="stylesheet" href="assets/css/styles\.css[^"]*">)', r'\1\n<link rel="stylesheet" href="assets/css/insights-finder.css">', s, count=1)
if "insights-finder.js" not in s:
    s = re.sub(r'(<script src="assets/js/main\.js[^"]*" defer></script>)', r'\1\n<script src="assets/js/insights-finder.js" defer></script>', s, count=1)
if "insights-finder.css" not in s or "insights-finder.js" not in s:
    sys.exit("insights.html: could not add the stylesheet or script link")

open(PAGE, "w", encoding="utf-8").write(s)
print(f'insights finder: {len(buttons)} goals, {sum(len(g["articles"]) for g in fd["goals"])} list entries, {len(shelf)} series')
