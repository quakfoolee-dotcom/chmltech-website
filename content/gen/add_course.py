"""Add (or refresh) free courses on the site after writing their JSON in content/courses/.

For each course name given (its JSON file name without .json) this:
  1. renders challenge-page/<id>.html (content/gen/course_page.py),
  2. adds its card to courses.html (after the card named in CARDS[name]["after"]),
  3. updates the course counts on courses.html, index.html and README.md,
  4. re-renders every course page so the "More free courses" lists include it,
  5. rebuilds the course finder (content/gen/course_finder.py; the course needs an entry
     in content/courses/finder.json and a place in one or more paths).
Then run content/gen/seo_pass.py as usual.

usage (site root): python3 content/gen/add_course.py . lean-six-sigma [inventory-management ...]
"""
import html as H
import json
import os
import re
import subprocess
import sys

ROOT = sys.argv[1]
NAMES = sys.argv[2:]
HERE = os.path.dirname(os.path.abspath(__file__))
CDIR = os.path.join(ROOT, "content", "courses")
sys.path.insert(0, HERE)
import course_page  # noqa: E402

course_page.ROOT, course_page.CDIR = ROOT, CDIR
esc = lambda s: H.escape(s or "", quote=True)

SVG = ('<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>')
# Card icon and position for courses written for the new site. "after" = id of the card it follows.
CARDS = {
    "lean-six-sigma": dict(after="25c5f60e-3f55-43a1-9c15-345dfc5b8f7f",
                           icon='<path d="M3 20h18"/><path d="M5 20V10M10 20V6M15 20v-8M20 20V4"/>'),
    "inventory-management": dict(after="lean-six-sigma-foundations",
                                 icon='<path d="M3 8l9-5 9 5v10l-9 5-9-5z"/><path d="M3 8l9 5 9-5M12 13v10"/>'),
    "oee-equipment-effectiveness": dict(after="inventory-management-for-smes",
                                        icon='<circle cx="12" cy="13" r="8"/><path d="M12 13l4-4M12 3v2M4 13H2M22 13h-2"/>'),
    "cybersecurity-ransomware": dict(after="e385a42b-5aaf-457f-9957-e8d19fee8cc0",
                                     icon='<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>'),
    "prompting-ai-productivity": dict(after="ai-awareness-for-everyone",
                                      icon='<path d="M4 5h16v11H8l-4 4z"/><path d="M8 9h8M8 12h5"/>'),
    "local-ai": dict(after="building-your-ai-operating-system",
                     icon='<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/><path d="M9 10l2 2 4-4"/>'),
    "data-dashboards": dict(after="digital-automation-for-smes",
                            icon='<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 16v-4M12 16V8M17 16v-6"/>'),
    "erp-selection": dict(after="data-and-dashboards-for-smes",
                          icon='<rect x="3" y="4" width="7" height="7" rx="1"/><rect x="14" y="4" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M17.5 14v7M14 17.5h7"/>'),
    "business-basics": dict(after="cybersecurity-and-ransomware-basics-for-smes",
                            icon='<path d="M3 21h18"/><path d="M5 21V10l7-5 7 5v11"/><path d="M9 21v-6h6v6"/>'),
    "sop": dict(after="inventory-management-for-smes",
                icon='<path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3"/><path d="M18 3v4h-4M6 21v-4h4"/>'),
    "iso9001": dict(after="lean-six-sigma-foundations",
                    icon='<circle cx="12" cy="9" r="6"/><path d="M9 9l2 2 4-4"/><path d="M8.5 14L7 21l5-3 5 3-1.5-7"/>'),
    "feed-process-design": dict(after="oee-equipment-effectiveness",
                                icon='<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-9V3"/><path d="M7.5 15h9"/>'),
}


def card(c):
    n = sum(len(m["steps"]) for m in c["modules"])
    return (f'<article class="program">{SVG.format(CARDS[c["_name"]]["icon"])}<div class="facts"><span class="tag tag-green">Free</span>'
            f'<span class="tag">{n} lessons</span><span class="tag">{len(c["labs"])} labs</span><span class="tag">Final exam + certificate</span></div>'
            f'<h3 class="h-md" style="font-size:24px">{esc(c["title"])}</h3><p class="muted">{esc(c["tagline"])}</p>'
            f'<a class="more" style="margin-top:auto;font-weight:600" href="challenge-page/{c["id"]}.html">Start free course →</a></article>')


cp = os.path.join(ROOT, "courses.html")
s = open(cp, encoding="utf-8").read()
for name in NAMES:
    c = json.load(open(os.path.join(CDIR, name + ".json")))
    c["_name"] = name
    if f'href="challenge-page/{c["id"]}.html"' not in s:
        after = CARDS[name]["after"]
        i = s.index(f'href="challenge-page/{after}.html"')
        j = s.index("</article>", i) + len("</article>")
        s = s[:j] + card(c) + s[j:]
    else:  # refresh the card (title, tagline, counts)
        s = re.sub(r'<article class="program"[^>]*>(?:(?!</article>).)*href="challenge-page/%s\.html".*?</article>' % re.escape(c["id"]),
                   lambda m: card(c), s, count=1, flags=re.S)
p0 = s.index('id="programs"')
total = len(re.findall(r'href="challenge-page/', s[p0:s.index("</section>", p0)]))
s = re.sub(r'<h2 class="h-lg">\d+ free courses</h2>', f'<h2 class="h-lg">{total} free courses</h2>', s)
open(cp, "w", encoding="utf-8").write(s)

for f, pat, rep in [("index.html", r"\d+ free online courses\.", f"{total} free online courses."),
                    ("README.md", r"The \d+ free interactive courses", f"The {total} free interactive courses")]:
    p = os.path.join(ROOT, f)
    t = open(p, encoding="utf-8").read()
    open(p, "w", encoding="utf-8").write(re.sub(pat, rep, t))

for f in sorted(os.listdir(CDIR)):
    if f.endswith(".json") and f != "finder.json":
        course_page.build(f[:-5])
subprocess.run([sys.executable, os.path.join(HERE, "course_finder.py"), ROOT], check=True)
print(f"courses on the site: {total}")
