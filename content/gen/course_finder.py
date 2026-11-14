"""Course finder: adds the "Find your course" quiz, level/topic filters and
course tags to courses.html.

Data: content/courses/finder.json (levels, topics, paths, questions) plus each
course's own JSON in content/courses/ (title, tagline, lesson count).
Script and styles: assets/js/course-finder.js, assets/css/course-finder.css.

Run from the site root:  python3 content/gen/course_finder.py .
then run content/gen/seo_pass.py as usual. Safe to run any number of times.
"""
import html
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
PAGE = os.path.join(ROOT, "courses.html")
CDIR = os.path.join(ROOT, "content", "courses")

fd = json.load(open(os.path.join(CDIR, "finder.json")))
s = open(PAGE, encoding="utf-8").read()

# ---- course catalogue -------------------------------------------------------
cards = re.findall(r'href="challenge-page/([^".]+)\.html"', s)
catalog = {}
for key, meta in fd["courses"].items():
    d = json.load(open(os.path.join(CDIR, key + ".json")))
    if d["id"] not in cards:
        sys.exit(f"course {key} ({d['id']}) has no card on courses.html")
    catalog[key] = dict(
        id=d["id"], title=d["title"], tagline=d.get("tagline", ""),
        lessons=sum(len(m["steps"]) for m in d["modules"]),
        level=meta["level"], topic=meta["topic"],
        url="challenge-page/%s.html" % d["id"])
for p in fd["paths"].values():
    for k in p["courses"]:
        assert k in catalog, f"path course {k} not in finder.json courses"
missing = set(cards) - {c["id"] for c in catalog.values()}
if missing:
    sys.exit(f"cards without finder tags: {missing}")

data = {k: fd[k] for k in ("levels", "topics", "paths", "goal_path", "beginner_intro",
                           "industry_extra", "industry_names", "questions")}
data["courses"] = catalog
data_js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

# ---- 1. quiz section after the hero ----------------------------------------
FINDER = f"""<!-- finder:start -->
<section class="section finder-section" id="finder" hidden style="scroll-margin-top:84px"><div class="container">
  <div class="finder card" data-state="intro">
    <div class="finder-intro">
      <div class="stack">
        <p class="eyebrow">Find your course</p>
        <h2 class="h-lg">Not sure where to start?</h2>
        <p class="lead">Answer 5 quick questions and we'll suggest a starting course and a learning path. It takes about a minute, and nothing is sent or stored outside your browser.</p>
      </div>
      <div class="btn-row"><button type="button" class="btn" data-finder="start">Take the 1-minute quiz</button><a class="btn btn-ghost" href="#programs">Browse all courses</a></div>
    </div>
    <div class="finder-quiz" hidden>
      <div class="finder-progress"><span class="finder-step" aria-live="polite"></span><div class="finder-bar" aria-hidden="true"><span></span></div></div>
      <fieldset class="finder-q"><legend class="sr-only"></legend><p class="finder-qtext h-md" aria-hidden="true"></p><div class="finder-opts"></div></fieldset>
      <div class="finder-nav"><button type="button" class="btn btn-ghost" data-finder="back">← Back</button><button type="button" class="btn" data-finder="next" disabled>Next →</button></div>
    </div>
    <div class="finder-result" hidden tabindex="-1"></div>
  </div>
</div></section>
<script type="application/json" id="finder-data">{data_js}</script>
<!-- finder:end -->"""
s = re.sub(r"<!-- finder:start -->.*?<!-- finder:end -->\n?", "", s, flags=re.S)
i = s.index('<section class="page-hero')
j = s.index("</section>", i) + len("</section>\n")
s = s[:j] + FINDER + "\n" + s[j:]

# ---- 2. hero button ---------------------------------------------------------
s = s.replace('<a class="btn" href="#programs">See the courses</a>',
              '<a class="btn" href="#finder" data-finder="hero">Find your course</a>'
              '<a class="btn btn-ghost-dark" href="#programs">See all courses</a>')

# ---- 3. filter chips above the course grid ---------------------------------
def chips(group, label, items):
    b = [f'<button type="button" class="chip" data-{group}="all" aria-pressed="true">All</button>']
    b += [f'<button type="button" class="chip" data-{group}="{k}" aria-pressed="false">{html.escape(v)}</button>'
          for k, v in items]
    return (f'<div class="filter-row" role="group" aria-label="{label}"><span class="filter-label">{label}</span>'
            + "".join(b) + "</div>")

FILTERS = ("<!-- cfilter:start --><div class=\"course-filters\" hidden>"
           + chips("level", "Level", fd["levels"].items())
           + chips("topic", "Topic", fd["topics"].items())
           + '<p class="filter-count muted" aria-live="polite"></p></div><!-- cfilter:end -->')
s = re.sub(r"<!-- cfilter:start -->.*?<!-- cfilter:end -->", "", s, flags=re.S)
s = re.sub(r"\n  (?=<div class=\"grid grid-3\" id=\"course-grid\">)", "", s)
p0 = s.index('id="programs"')
m = re.compile(r'<div class="grid grid-3"(?: id="course-grid")?>').search(s, p0)
s = s[:m.start()] + FILTERS + "\n  " + '<div class="grid grid-3" id="course-grid">' + s[m.end():]

# ---- 4. level/topic data and a level tag on each card ----------------------
by_id = {c["id"]: (k, c) for k, c in catalog.items()}
def tag_card(m):
    art = m.group(0)
    cid = re.search(r'href="challenge-page/([^".]+)\.html"', art).group(1)
    k, c = by_id[cid]
    art = re.sub(r'<article class="program"[^>]*>',
                 f'<article class="program" data-key="{k}" data-level="{c["level"]}" data-topic="{c["topic"]}">', art, count=1)
    art = re.sub(r'<span class="tag tag-level[^"]*">[^<]*</span>', "", art)
    lvl = fd["levels"][str(c["level"])]
    art = art.replace('<span class="tag tag-green">Free</span>',
                      f'<span class="tag tag-green">Free</span><span class="tag tag-level lv{c["level"]}">{lvl}</span>', 1)
    return art
grid_end = s.index('</section>', p0)
block = s[p0:grid_end]
block = re.sub(r'<article class="program"[^>]*>.*?</article>', tag_card, block, flags=re.S)
s = s[:p0] + block + s[grid_end:]

# ---- 5. stylesheet and script ----------------------------------------------
if "course-finder.css" not in s:
    s = re.sub(r'(<link rel="stylesheet" href="assets/css/styles\.css[^"]*">)',
               r'\1\n<link rel="stylesheet" href="assets/css/course-finder.css">', s, count=1)
if "course-finder.js" not in s:
    s = re.sub(r'(<script src="assets/js/main\.js[^"]*" defer></script>)',
               r'\1\n<script src="assets/js/course-finder.js" defer></script>', s, count=1)

open(PAGE, "w", encoding="utf-8").write(s)
print(f"course finder: {len(catalog)} courses, {len(fd['paths'])} paths written to courses.html")
