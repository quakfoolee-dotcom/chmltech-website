"""Render a free course page (challenge-page/<id>.html) from its JSON in content/courses/.

Rebuilt in V4.94 (the original renderer lived outside the repository). It reproduces the
existing course pages exactly from their JSON, so new courses look and behave the same:
lessons, knowledge checks, figures (assets/js/figures.js), labs and exam (assets/js/course.js),
certificate and the "More free courses" list.

usage (site root):
  python3 content/gen/course_page.py . <course-json-name> [<course-json-name> ...]
  python3 content/gen/course_page.py . --check llms-for-business   # compare with the live page
The hero illustration comes from content/courses/art/<course-json-name>.svg if present,
otherwise it is kept from the existing page.
Afterwards run content/gen/add_course.py (cards, lists) and content/gen/seo_pass.py.
"""
import html as H
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
CDIR = os.path.join(ROOT, "content", "courses")
SHELL = os.path.join(ROOT, "challenge-page", "llms-for-business-leaders.html")
esc = lambda s: H.escape(s or "", quote=True)

FIG_KICKER = {"compare": "Before and after", "stack": "Building blocks", "flow": "Process flow",
              "bars": "Visual comparison", "cycle": "Interactive cycle", "timeline": "Roadmap"}


def fig_static(f):
    c, t = f["config"], f["type"]
    if t == "compare":
        items = [f'{c[s]["title"]}: ' + "; ".join(c[s]["points"]) for s in ("left", "right")]
    elif t == "stack":
        items = [f'{x["label"]}: {x["text"]}' for x in c["layers"]]
    elif t == "flow":
        items = [f'{x["label"]}: {x["text"]}' for x in c["steps"]]
    elif t == "bars":
        items = [f'{x["label"]}: {fmtnum(x["value"])} {c.get("unit", "")}'.rstrip() for x in c["items"]]
    elif t == "cycle":
        items = [f'{x["label"]}: {x["text"]}' for x in c["stages"]]
    elif t == "timeline":
        items = [f'{x["label"]} ({x["title"]}): ' + "; ".join(x["items"]) for x in c["phases"]]
    else:
        items = []
    return "".join(f"<li>{esc(i)}</li>" for i in items)


def fmtnum(v):
    return str(int(v)) if float(v).is_integer() else str(v)


def figure(f, i):
    return (f'<figure class="cfig" data-fig="{i}"><figcaption><span class="fig-kicker">{FIG_KICKER[f["type"]]}</span>'
            f'<strong>{esc(f["title"])}</strong><span class="fig-cap">{esc(f["caption"])}</span></figcaption>'
            f'<div class="fig-host"></div><ul class="fig-static">{fig_static(f)}</ul></figure>')


def render_main(c, others, hero_svg):
    steps = [(mi, m, s) for mi, m in enumerate(c["modules"]) for s in m["steps"]]
    N, labs, figs = len(steps), c["labs"], c.get("figures", [])
    mins = sum(s["minutes"] for _, _, s in steps)
    hours = max(4, round(mins / 60))  # lessons + labs + exam; the live pages all show ~4 h
    lab_after = {}
    for L in labs:
        lab_after.setdefault(L["after_step"], []).append(L)
    fig_at = {}
    for i, f in enumerate(figs):
        fig_at.setdefault(f["step"], []).append((i, f))
    # sequence of views for prev/next
    seq = ["overview"]
    for n in range(1, N + 1):
        seq.append(f"step-{n}")
        seq += [f'lab-{L["id"]}' for L in lab_after.get(n, [])]
    seq.append("exam")

    o = []
    o.append(f'''<main id="main">
<section class="page-hero dark course-hero">
  <div class="container course-hero-grid"><div class="stack-lg">
    <p class="crumbs"><a href="../index.html">Home</a> / <a href="../courses.html">Courses</a> / {esc(c["title"])}</p>
    <p class="eyebrow">Free course · Self-paced</p>
    <h1 class="h-xl">{esc(c["title"])}</h1>
    <p class="lead">{esc(c["tagline"])}</p>
    <div class="stat-row"><div><strong>{N}</strong><span>lessons</span></div><div><strong>{len(labs)}</strong><span>interactive labs</span></div><div><strong>{len(c["exam"])}</strong><span>exam questions</span></div><div><strong>~{hours} h</strong><span>self-paced</span></div></div>
<div class="stack" style="gap:8px"><div class="progress" aria-hidden="true"><span data-progress-bar></span></div><p class="progress-text" data-progress-text>0 of {N} lessons complete</p></div>
<div class="btn-row"><a class="btn" href="#step-1" data-continue>Start the course</a><a class="btn btn-ghost-dark" href="#overview">Course overview</a></div>
  </div><div class="hero-art">{hero_svg}</div></div>
</section>
''')
    # outline
    nav = ['<a href="#overview" data-goto="overview">Course overview</a>']
    n = 0
    for mi, m in enumerate(c["modules"]):
        nav.append(f'<div class="ol-mod">Module {mi + 1} · {esc(m["title"])}</div>')
        for s in m["steps"]:
            n += 1
            nav.append(f'<a href="#step-{n}" data-goto="step-{n}">{n}. {esc(s["title"])}</a>')
            for L in lab_after.get(n, []):
                nav.append(f'<a href="#lab-{L["id"]}" data-goto="lab-{L["id"]}" class="ol-lab">{esc(L["title"])}<span class="ol-tag">Lab</span></a>')
    nav.append(f'<div class="ol-mod">Finish</div><a href="#exam" data-goto="exam" class="ol-exam">Final exam<span class="ol-tag">{len(c["exam"])} Q</span></a><a href="#certificate" data-goto="certificate">Certificate of completion</a>')
    o.append(f'''<section class="section" style="padding-top:56px"><div class="container course-layout" data-course>
  <aside class="course-outline" aria-label="Course outline"><details open><summary>Course outline</summary><nav>{"".join(nav)}</nav>
  <p style="padding:14px 12px 0;font-size:12.5px;color:var(--muted)">Progress is saved in this browser. <button type="button" data-reset style="background:none;border:0;padding:0;color:var(--blue);text-decoration:underline;cursor:pointer;font:inherit">Reset progress</button></p></details></aside>
  <div class="course-view">
''')
    # overview
    li = lambda xs: "".join(f"<li>{esc(x)}</li>" for x in xs)
    mods = "".join(f'<li><strong>Module {i + 1}: {esc(m["title"])}</strong> ({len(m["steps"])} lessons). {esc(m["summary"])}</li>' for i, m in enumerate(c["modules"]))
    labli = "".join(f'<li><strong>{esc(L["title"])}</strong>: {esc(L["intro"])}</li>' for L in labs)
    o.append(f'''<section data-view="overview" aria-labelledby="h-overview">
  <div class="view-head"><p class="view-meta">Course overview</p><h2 id="h-overview">About this course</h2></div>
  <div class="prose"><p>{esc(c["summary"])}</p></div>
  <div class="grid grid-2" style="margin-top:28px">
    <div class="card" style="padding:26px"><h3 style="font-size:19px">Who it is for</h3><ul class="list-check">{li(c["audience"])}</ul></div>
    <div class="card" style="padding:26px"><h3 style="font-size:19px">What you will be able to do</h3><ul class="list-check">{li(c["outcomes"])}</ul></div>
  </div>
  <div class="prose" style="margin-top:32px;max-width:none">
    <h3>Course structure</h3><ul>{mods}</ul>
    <h3>Interactive labs</h3><ul>{labli}</ul>
    <h3>How it works</h3>
    <ul><li>Work through {N} short lessons at your own pace. Each has key takeaways, an exercise for your own workplace and a quick knowledge check.</li>
    <li>Try the {num_word(len(labs))} interactive labs as you reach them in the course.</li>
    <li>Pass the {len(c["exam"])}-question final exam (70% or higher, unlimited retakes) to unlock your Chmltech certificate of completion.</li>
    <li>Free, with no sign-up. Your progress is saved in this browser.</li></ul>
  </div>
  <div class="btn-row" style="margin-top:28px"><a class="btn" href="#step-1" data-continue>Start the course</a><a class="btn btn-ghost" href="#exam">Go to the final exam</a></div>
</section>
''')
    # lessons and labs
    n = 0
    for mi, m in enumerate(c["modules"]):
        for s in m["steps"]:
            n += 1
            v = f"step-{n}"
            k = seq.index(v)
            prev, nxt = seq[k - 1], seq[k + 1]
            if nxt == "exam":
                ntxt = "Complete and take the final exam →"
            elif nxt.startswith("lab-"):
                ntxt = "Complete and go to the lab →"
            else:
                ntxt = "Complete and continue →"
            ch = s["check"]
            opts = "".join(f'<label><input type="radio" name="kc-{n}" value="{j}"> <span>{esc(x)}</span></label>' for j, x in enumerate(ch["opts"]))
            figs_html = "".join(figure(f, i) for i, f in fig_at.get(n, []))  # several figures in one lesson: see below
            o.append(f'''<section data-view="{v}" aria-labelledby="h-{v}">
  <div class="view-head"><p class="view-meta">Module {mi + 1} · Lesson {n} of {N} · {s["minutes"]} min</p><h2 id="h-{v}">{esc(s["title"])}</h2></div>
  <div class="prose">{s["body"]}</div>
  {figs_html}
  <div class="lesson-box box-takeaways"><h3>Key takeaways</h3><ul class="list-check">{li(s["takeaways"])}</ul></div>
  <div class="lesson-box box-apply"><h3>Apply it at work</h3><p>{esc(s["apply"])}</p></div>
  <div class="kcheck" data-answer="{ch["a"]}" data-why="{esc(ch["why"])}"><fieldset><legend>Check your understanding: {esc(ch["q"])}</legend>{opts}</fieldset>
    <div class="btn-row" style="margin-top:14px"><button type="button" class="btn btn-ghost">Check answer</button></div><p class="kcheck-feedback" aria-live="polite"></p></div>
  <nav class="lesson-nav" aria-label="Lesson navigation"><a class="btn btn-ghost" href="#{prev}">← Previous</a><a class="btn" href="#{nxt}" data-complete="{n}">{ntxt}</a></nav>
</section>
''')
    for n in range(1, N + 1):
        for L in lab_after.get(n, []):
            v = f'lab-{L["id"]}'
            k = seq.index(v)
            nxt = seq[k + 1]
            wide = " lab-wide" if L["type"] in ("classify", "matrix") else ""
            ntxt = "Continue to the final exam →" if nxt == "exam" else (f"Continue to lesson {n + 1} →" if nxt.startswith("step-") else "Continue to the next lab →")
            o.append(f'''<section data-view="{v}" aria-labelledby="h-{v}">
  <div class="view-head"><p class="view-meta">Interactive lab · after lesson {n}</p><h2 id="h-{v}">{esc(L["title"])}</h2><p class="muted" style="font-size:17px;max-width:760px">{esc(L["intro"])}</p></div>
  <div class="lab-shell{wide}" data-lab-host><noscript><p>This interactive lab needs JavaScript enabled.</p></noscript></div>
  <nav class="lesson-nav" aria-label="Lab navigation"><a class="btn btn-ghost" href="#step-{n}">← Back to lesson {n}</a><a class="btn" href="#{nxt}">{ntxt}</a></nav>
</section>
''')
    o.append(f'''<section data-view="exam" aria-labelledby="h-exam">
  <div class="view-head"><p class="view-meta">Final exam</p><h2 id="h-exam">Final exam: {esc(c["title"])}</h2>
  <p class="muted" style="font-size:17px;max-width:760px">{len(c["exam"])} questions covering the whole course. Score 70% or higher to pass and unlock your certificate of completion. You can retake it as often as you like, and wrong answers come with explanations.</p></div>
  <div data-exam-host><noscript><p>The exam needs JavaScript enabled.</p></noscript></div>
</section>
<section data-view="certificate" aria-labelledby="h-cert">
  <div class="view-head"><p class="view-meta">Certificate</p><h2 id="h-cert">Your certificate of completion</h2><p class="muted">Enter your name as you want it to appear, then print or save it as a PDF.</p></div>
  <div class="cert-tools"><div class="field"><label for="cert-name">Name on certificate</label><input id="cert-name" type="text" autocomplete="name" data-cert-name></div><button type="button" class="btn" data-print>Print or save as PDF</button></div>
  <div class="certificate">
    <img src="../assets/img/chmltech-logo.png" alt="Chmltech">
    <p class="cert-kicker">Certificate of completion</p>
    <p>This certifies that</p>
    <p class="cert-name" data-cert-out-name>Your name</p>
    <p>has successfully completed the Chmltech course</p>
    <p class="cert-course">{esc(c["title"])}</p>
    <p class="muted" style="font-size:14px">{N} lessons · {len(labs)} interactive labs · final exam passed</p>
    <div class="cert-foot"><span class="cert-col"><strong data-cert-date></strong>Date completed<br>&nbsp;</span><span class="cert-col cert-sign"><img class="cert-sig-img" src="../assets/img/signature-quak-foo-lee.svg" alt="Signature of Quak Foo Lee" width="240" height="66"><strong>Quak Foo Lee</strong>CEO and Principal Consultant<br>Chmltech Ltd.</span><span class="cert-col"><strong data-cert-id>CHM-0000</strong>Certificate no.<br>www.chmltech.com</span></div>
  </div>
</section>
  </div>
</div></section>
<section class="section sand"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Keep learning</p><h2 class="h-lg">More free courses</h2></div><a class="btn btn-ghost" href="../training.html">Free practice exams</a></div>
  <div class="index">{"".join(f'<a href="../challenge-page/{q[0]}.html">{esc(q[1])}<span aria-hidden="true">→</span></a>' for q in others)}</div>
</div></section>
''')
    data = {"id": c["id"], "total_steps": N, "labs": labs, "exam": c["exam"], "figures": figs}
    o.append('<script type="application/json" id="course-data">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>\n\n")
    return "".join(o)


def num_word(n):
    return {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}.get(n, str(n))


def course_order():
    """Course ids in the order of the cards on courses.html."""
    s = open(os.path.join(ROOT, "courses.html"), encoding="utf-8").read()
    p0 = s.index('id="programs"')
    blk = s[p0:s.index("</section>", p0)]
    ids = re.findall(r'href="challenge-page/([^".]+)\.html"', blk)
    titles = {}
    for f in os.listdir(CDIR):
        if f.endswith(".json") and f != "finder.json":
            d = json.load(open(os.path.join(CDIR, f)))
            if "modules" in d:
                titles[d["id"]] = d["title"]
    return ids, titles


def build(name, check=False):
    c = json.load(open(os.path.join(CDIR, name + ".json")))
    out = os.path.join(ROOT, "challenge-page", c["id"] + ".html")
    ids, titles = course_order()
    if c["id"] not in ids:
        ids.append(c["id"])
    others = [(i, titles[i]) for i in ids if i != c["id"] and i in titles]
    art = os.path.join(CDIR, "art", name + ".svg")
    if os.path.exists(art):
        svg = open(art, encoding="utf-8").read().strip()
    else:
        svg = re.search(r'<div class="hero-art">(.*?)</div></div>\s*</section>', open(out, encoding="utf-8").read(), re.S).group(1)
    main = render_main(c, others, svg)
    src = open(out if os.path.exists(out) else SHELL, encoding="utf-8").read()
    if check:
        old = src[src.index('<main id="main">'):src.index("</main>")]
        if old == main:
            print(f"{name}: identical to the live page")
            return True
        import difflib
        d = list(difflib.unified_diff(old.splitlines(), main.splitlines(), lineterm="", n=0))
        print(f"{name}: {len(d)} diff lines"); print("\n".join(x[:300] for x in d[:40]))
        return False
    s = src[:src.index('<main id="main">')] + main + src[src.index("</main>"):]
    desc = esc(c["summary"][:155])
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(c['title'])}</title>", s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(c["title"])}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', s, count=1)
    s = re.sub(r'(<link rel="canonical" href="https://www\.chmltech\.com/challenge-page/)[^"]*(">)', rf'\g<1>{c["id"]}\2', s, count=1)
    s = re.sub(r'(<meta property="og:url" content="https://www\.chmltech\.com/challenge-page/)[^"]*(">)', rf'\g<1>{c["id"]}\2', s, count=1)
    s = re.sub(r'<script type="application/ld\+json" data-seo="v1">.*?</script>\n?', "", s, flags=re.S)
    open(out, "w", encoding="utf-8").write(s)
    print(f"wrote challenge-page/{c['id']}.html")
    return True


if __name__ == "__main__":
    args = sys.argv[2:]
    check = "--check" in args
    names = [a for a in args if a != "--check"]
    ok = all([build(n, check) for n in names])
    sys.exit(0 if ok else 1)
