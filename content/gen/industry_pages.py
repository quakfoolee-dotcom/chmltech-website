"""Rich industry pages with animated scenes and interactive figures (V4.7). Content: industries/<slug>.json."""
import json, os, re
import assetver
clean = lambda x, w: re.sub(rf"^\s*{w}:\s*", "", x)
from service_pages import fig, esc
from industry_art import industry_art

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "industries")
ORDER = ["energy-and-chemicals", "natural-resources", "manufacturing", "health-care", "professional-services",
         "consumer-goods", "distribution-and-warehousing", "public-sector"]
DARK = 'style="background:#11335F;border-color:#234A80"'


def build(ns):
    page, icon, related_posts_html, QUOTE, progs, OUT = ns["page"], ns["icon"], ns["related_posts_html"], ns["QUOTE"], ns["progs"], ns["OUT"]
    titles = {p["id"]: p["title"] for p in progs}
    for slug in ORDER:
        P = json.load(open(os.path.join(SRC, slug + ".json")))
        others = [s for s in ORDER if s != slug]
        b = f'''<section class="page-hero dark course-hero"><div class="container course-hero-grid"><div class="stack-lg">
  <p class="crumbs"><a href="index.html">Home</a> / <a href="industries.html">Industries</a> / {esc(P["title"])}</p>
  <p class="eyebrow">{esc(P["eyebrow"])}</p><h1 class="h-xl" style="font-size:clamp(32px,4.2vw,54px)">{esc(P["h1"])}</h1>
  <p class="lead">{esc(P["lead"])}</p>
  <div class="btn-row"><a class="btn" href="book.html">Book a Strategy Call</a><a class="btn btn-ghost-dark" href="contact.html?service={esc(P["title"]).replace(" ", "%20").replace("&amp;", "%26")}">Ask a question</a></div>
</div>{industry_art(slug, esc(P["title"]))}</div></section>
<section class="section"><div class="container feature-split">
  <div class="stack-lg"><p class="eyebrow">Overview</p><h2 class="h-lg">{esc(P["intro"][0])}</h2><p class="muted" style="font-size:17.5px">{esc(P["intro"][1])}</p></div>
  <div class="card" style="padding:30px"><h3 style="font-size:20px">Signs it's time to act</h3><ul class="list-check">{"".join(f"<li>{esc(x)}</li>" for x in P["signs"])}</ul></div>
</div></section>
<section class="section dark"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Industry challenges</p><h2 class="h-lg">What we see in {esc(P["title"].lower())}.</h2></div></div>
  <div class="grid grid-2">{"".join(f'<div class="card card-dark" {DARK}><h3 style="font-size:20px">{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in P["challenges"])}</div>
</div></section>
<section class="section sand"><div class="container">
  <div class="stack" style="max-width:720px;margin-bottom:28px"><p class="eyebrow">Interactive demo</p><h2 class="h-lg">See how it works.</h2><p class="muted">Click the diagrams to explore each step.</p></div>
  <div class="fig-col">{"".join(fig(F) for F in P["figs"] if F["type"] == "swimlane")}{(lambda R: '<div class="grid grid-2" style="align-items:start">' + "".join(fig(F) for F in R) + '</div>' if len(R) > 1 else "".join(fig(F) for F in R))([F for F in P["figs"] if F["type"] != "swimlane"])}</div>
</div></section>
<section class="section"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">How we help</p><h2 class="h-lg">{esc(P["services_title"])}</h2></div></div>
  <div class="grid grid-3">{"".join(f'<article class="card">{icon(ic)}<h3 style="font-size:21px">{esc(t)}</h3><p class="muted">{esc(d)}</p></article>' for ic, t, d in P["services"])}</div>
</div></section>
<section class="section dark"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Typical scenarios</p><h2 class="h-lg">What improvement looks like.</h2></div><p class="lead" style="font-size:16px">Illustrative examples of the kind of change we work on.</p></div>
  <div class="grid grid-3">{"".join(f'<div class="card card-dark" {DARK}><h3 style="font-size:20px">{esc(t)}</h3><p><strong style="color:#F7B58A">Before:</strong> {esc(clean(bf, "Before"))}</p><p><strong style="color:var(--green)">After:</strong> {esc(clean(af, "After"))}</p></div>' for t, bf, af in P["examples"])}</div>
</div></section>
<section class="section"><div class="container grid grid-2" style="align-items:center">
  <div class="stack"><p class="eyebrow">Outcomes</p><h2 class="h-lg">What you can expect.</h2></div>
  <ul class="list-check" style="font-size:17px">{"".join(f"<li>{esc(x)}</li>" for x in P["outcomes"])}</ul>
</div></section>'''
        W = P["why"]
        badge = lambda i, t: "ROI" if t.lower().startswith("results agreed") else f"0{i + 1}"
        b += f'''
<section class="section sand"><div class="container">
  <div class="stack" style="max-width:820px;margin-bottom:36px"><p class="eyebrow">Why Chmltech</p><h2 class="h-lg">{esc(W["title"])}</h2><p class="muted" style="font-size:17.5px">{esc(W["text"])}</p></div>
  <div class="grid grid-3">{"".join(f'<article class="card"><span class="price" style="font-size:22px">{badge(i, t)}</span><h3 style="font-size:21px">{esc(t)}</h3><p class="muted">{esc(d)}</p></article>' for i, (t, d) in enumerate(W["points"]))}</div>
  {f'<p class="count" style="margin-top:16px">{esc(W["note"])}</p>' if W.get("note") else ""}
</div></section>
<section class="section"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Questions</p><h2 class="h-lg">Frequently asked</h2></div></div>
  <div class="faq">{"".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in P["faq"])}</div>
</div></section>
<section class="section sand"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Free learning</p><h2 class="h-lg">Related free courses</h2></div><a class="btn btn-ghost" href="courses.html">All free courses</a></div>
  <div class="grid grid-4">{"".join(f'<a class="card" style="text-decoration:none;padding:24px" href="challenge-page/{c}.html"><span class="tag tag-green">Free course</span><h3 style="font-size:18px">{esc(titles.get(c, ""))}</h3><span class="more" style="font-weight:600">Start →</span></a>' for c in P["courses"] if c in titles)}</div>
</div></section>
{related_posts_html(P["cats"])}
<section class="section"><div class="container"><p class="eyebrow">Other industries</p>
  <div class="chips" style="margin-top:12px">{"".join(f'<a class="chip" style="text-decoration:none;display:inline-flex;align-items:center" href="{s}.html">{esc(json.load(open(os.path.join(SRC, s + ".json")))["title"])}</a>' for s in others)}</div>
</div></section>
{QUOTE}'''
        page(f"{slug}.html", P["title"], esc(P["meta"]), b)
        fp = os.path.join(OUT, f"{slug}.html"); s = open(fp).read(); s = assetver.strip(s)
        s = s.replace("</head>", '<link rel="stylesheet" href="assets/css/course.css">\n</head>', 1)
        s = s.replace('<script src="assets/js/main.js" defer></script>', '<script src="assets/js/main.js" defer></script>\n<script src="assets/js/figures.js" defer></script>\n<script src="assets/js/svc.js" defer></script>', 1)
        open(fp, "w").write(s)
