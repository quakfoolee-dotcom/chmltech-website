"""Practice-exam category hubs and the links to them (V5.81). Run by seo_pass.py on every build.

Why: in November 2026 Search Console listed 119 of the 147 library exams as "Discovered - currently
not indexed". Nearly all of them had a single link pointing at them (the Training page), so Google
saw them as low priority. This module gives every exam more paths in:

1. One hub page per exam category at the site root (e.g. /chemical-engineering-practice-exams):
   an introduction, every exam in the category with its description, related free courses,
   related articles and links to the other nine hubs. Built from content/gen/exam_cats.json, so a
   new exam added there appears on its hub at the next build.
2. Training: a "Browse by category" row linking the ten hubs.
3. Free courses: a "Practice exams for this course" block (the hub plus three matching exams).
4. Articles: a "Test what you have read" block (the matching hub plus three matching exams),
   chosen from the article's Insights category and title words.

Every block is wrapped in markers and replaced on each run, so edit the maps here and rebuild.
The exam files themselves are not touched.
"""
import html, json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
E = lambda s: html.escape(s, quote=True)

# category id -> (hub slug, page heading, short label, introduction)
HUBS = {
    "ai_agents": ("ai-practice-exams", "AI and agentic AI practice exams", "AI & Agents",
        "Free practice exams for people who design, build or buy AI systems: machine learning foundations, "
        "agent architecture and orchestration, retrieval-augmented generation, LLM evaluation, harness engineering, "
        "AI product management and physical AI. Most exams are 100 scenario questions with an explanation for every answer, "
        "so you can use them to check your judgment as well as your vocabulary."),
    "ai_use_cases": ("ai-use-case-practice-exams", "AI use case practice exams", "AI Use Cases",
        "Practice exams on where AI pays off in each business function: finance and accounting, human resources, "
        "manufacturing, product development, retail and ecommerce, and sales and marketing. Each one asks you to pick the right "
        "use case, data, controls and success measure for realistic situations in a small or mid-sized business."),
    "software_data": ("software-and-sql-practice-exams", "Software, SQL and testing practice exams", "Software & Data",
        "Practice exams for developers, testers and analysts: core and applied SQL, front-end and full-stack engineering, "
        "Git and GitHub, debugging, software and acceptance testing, and AI-assisted development workflows with Codex and vibe coding."),
    "cybersecurity": ("cybersecurity-practice-exams", "Cybersecurity practice exams", "Cybersecurity",
        "Practice exams on protecting a small or mid-sized business: security fundamentals, the OWASP web application risks, "
        "ransomware risk management and two long case-study exams that walk through real incidents from detection to recovery."),
    "quality_lean": ("lean-six-sigma-and-iso-9001-practice-exams", "Lean Six Sigma, ISO 9001 and quality practice exams", "Quality & Lean",
        "Practice exams for quality and continuous-improvement work: ISO 9001 case studies, Lean Six Sigma, Kaizen, "
        "root cause analysis and 5S. The questions are built around situations a quality lead or improvement team meets on the shop floor and in the office."),
    "process_chemeng": ("chemical-engineering-practice-exams", "Chemical and process engineering practice exams", "Process / ChemEng",
        "The largest part of the library: practice exams for chemical and process engineers on heat transfer, reactor design, "
        "separations, process control, thermodynamics, scale-up from bench to commercial plant, CapEx and OpEx, techno-economic analysis, "
        "corrosion and materials, piping, pump and tank farm design to Canadian codes, and graphene oxide synthesis. Many are 150-question "
        "case studies with calculations."),
    "business_finance": ("business-and-economics-practice-exams", "Business, economics and investing practice exams", "Business & Finance",
        "Practice exams on business strategy, micro- and macroeconomics, managerial and public-policy economics, and value investing "
        "from The Intelligent Investor to professional valuation."),
    "operations": ("operations-practice-exams", "Operations and process mapping practice exams", "Operations",
        "Practice exams on running operations efficiently: business process mapping, operations efficiency and the 100-day "
        "efficient-operations plan. Pair them with the free inventory, OEE and sales and operations planning courses."),
    "decision_thinking": ("critical-thinking-practice-exams", "Critical thinking and decision-making practice exams", "Decision-Making & Thinking",
        "Practice exams on how people decide: critical thinking for business and philosophy, cognitive biases, behavioural "
        "economics and finance, and the ideas in Thinking, Fast and Slow, Atomic Habits, The Psychology of Money and Think and Grow Rich."),
    "project_agile": ("pmp-and-agile-practice-exams", "PMP, Agile, Scrum and NPPE practice exams", "Project & Agile",
        "Practice exams for project professionals and engineers: the PMP exam in its 2026 formats, Agile Certified Practitioner, "
        "Certified ScrumMaster, leadership scenarios and the NPPE (National Professional Practice Examination) for engineers in Canada."),
}

# browser-tab titles, kept under 60 characters so they show in full in search results
TITLES = {
    "ai_agents": "Free AI and agentic AI practice exams | Chmltech",
    "ai_use_cases": "Free AI use case practice exams | Chmltech",
    "software_data": "Free software, SQL and testing practice exams | Chmltech",
    "cybersecurity": "Free cybersecurity practice exams | Chmltech",
    "quality_lean": "Free Lean Six Sigma and ISO 9001 practice exams | Chmltech",
    "process_chemeng": "Free chemical engineering practice exams | Chmltech",
    "business_finance": "Free business and economics practice exams | Chmltech",
    "operations": "Free operations practice exams | Chmltech",
    "decision_thinking": "Free critical thinking practice exams | Chmltech",
    "project_agile": "Free PMP, Agile and NPPE practice exams | Chmltech",
}

COURSES = {
    "25c5f60e-3f55-43a1-9c15-345dfc5b8f7f": "project_agile",
    "91ca0386-ec82-483d-8ec7-d6b13f02a0b5": "ai_agents",
    "ac58bd83-591d-4c25-9aac-71755f469d3c": "quality_lean",
    "ai-agents-for-business-operations": "ai_agents",
    "ai-awareness-for-everyone": "ai_use_cases",
    "b4b6581a-31f8-43f9-8796-268c83448b9f": "operations",
    "building-your-ai-operating-system": "ai_agents",
    "business-basics-for-owners": "business_finance",
    "choosing-erp-and-business-software": "software_data",
    "cybersecurity-and-ransomware-basics-for-smes": "cybersecurity",
    "data-and-dashboards-for-smes": "software_data",
    "digital-automation-for-smes": "ai_use_cases",
    "e385a42b-5aaf-457f-9957-e8d19fee8cc0": "operations",
    "e676eeeb-ed5f-40e1-b4c7-e287da77981b": "ai_agents",
    "feed-and-process-design": "process_chemeng",
    "inventory-management-for-smes": "operations",
    "iso-9001-quality-management-basics": "quality_lean",
    "lean-six-sigma-foundations": "quality_lean",
    "llms-for-business-leaders": "ai_agents",
    "multi-agent-systems-for-business": "ai_agents",
    "oee-equipment-effectiveness": "operations",
    "private-and-local-ai-for-smes": "ai_agents",
    "prompting-and-ai-productivity": "ai_use_cases",
    "sales-and-operations-planning": "operations",
}

# Insights category -> exam category, in priority order (first match wins)
POST_CATS = [
    ("process-engineering", "process_chemeng"),
    ("iso", "quality_lean"), ("lean", "quality_lean"), ("six-sigma", "quality_lean"),
    ("artificial-intelligence", "ai_agents"),
    ("project-management", "project_agile"), ("change-management", "project_agile"),
    ("book-review", "decision_thinking"),
    ("process-improvement", "quality_lean"),
    ("operational-efficiency", "operations"), ("inventory-management", "operations"), ("erp", "operations"),
    ("digital-technology", "software_data"),
    ("strategy", "business_finance"), ("marketing", "business_finance"), ("esg", "business_finance"),
    ("case-study", "business_finance"),
]
STOP = set("a an and the of for to in on with your you from how what why is are be by at or as it its our we this that "
           "exam exams practice guide part case study 100q 150q v1 v2 v3 v4 v5 v6 i ii iii iv v smes sme business businesses "
           "small mid sized using use into vs".split())

M = lambda name: (f"<!--exam-hub:{name}-->", f"<!--/exam-hub:{name}-->")


def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def words(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower().replace("_", " ")) if w not in STOP and len(w) > 2}


def cats():
    return {c["id"]: c for c in json.load(open(os.path.join(ROOT, "content/gen/exam_cats.json"), encoding="utf-8"))}


def exam_url(path, prefix=""):
    return prefix + "exams/" + path[:-5]


def pick(cat, text, n=3):
    """Three exams from the category that best match the text (title words), keeping catalogue order on ties."""
    w = words(text)
    scored = [(-len(w & words(e[0] + " " + e[4])), i, e) for i, e in enumerate(cat["exams"])]
    return [e for _, _, e in sorted(scored)[:n]]


def qcount(e):
    m = re.match(r"(\d+)", e[2] or "")
    return f"{m.group(1)} questions" if m else "Practice exam"


def post_index():
    """slug -> (title, insights categories) from the Insights page cards."""
    s = rd("insights.html"); out = {}
    for m in re.finditer(r'<article class="article" data-cats="([^"]*)"(.*?)</article>', s, re.S):
        h = re.search(r'href="(?:\.\./)?post/([^"#?]+?)(?:\.html)?"', m.group(2))
        t = re.search(r"<h3[^>]*>(?:<a[^>]*>)?(.*?)<", m.group(2), re.S)
        if h:
            out[h.group(1)] = (html.unescape(t.group(1)).strip() if t else h.group(1), m.group(1).split())
    return out


def post_cat(slug, tags):
    if "cyber" in slug or "ransomware" in slug:
        return "cybersecurity"
    for tag, c in POST_CATS:
        if tag in tags:
            return c
    return None


# ---------- hub pages ----------

def hub_page(cid, cat, all_cats, posts, tpl_head, tpl_top, tpl_foot):
    slug, h1, label, intro = HUBS[cid]
    n = len(cat["exams"])
    qs = sum(int(m.group(1)) for e in cat["exams"] for m in [re.match(r"(\d+)", e[2] or "")] if m)
    title = TITLES.get(cid) or f"Free {h1} | Chmltech"
    subj = h1.replace(" practice exams", "")
    subj = subj[0].lower() + subj[1:] if subj[1:2].islower() and not subj.startswith("Lean") else subj
    desc = f"{n} free {subj} practice exams with explanations. " + cat["description"]
    desc = desc if len(desc) <= 158 else desc[:155].rsplit(" ", 1)[0] + "…"
    head = tpl_head
    head = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", head, flags=re.S)
    for k, v in (("description", desc),):
        head = re.sub(rf'<meta name="{k}" content="[^"]*">', f'<meta name="{k}" content="{E(v)}">', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{E(desc)}">', head)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', rf"\g<1>https://www.chmltech.com/{slug}", head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', rf"\g<1>https://www.chmltech.com/{slug}", head)
    head = re.sub(r'<script type="application/ld\+json" data-seo="v1">.*?</script>\n?', "", head, flags=re.S)

    cards = "".join(
        f'<article class="exam"><span class="tag">{E(label)}</span><h3><a href="{exam_url(e[1])}">{E(e[0])}</a></h3>'
        f'<p>{E(e[4])}</p><div class="foot"><span>{qcount(e)}</span><span>Start →</span></div></article>'
        for e in cat["exams"])
    crs = [s for s, c in COURSES.items() if c == cid]
    course_links = "".join(
        f'<a href="challenge-page/{s}">{E(course_title(s))}<span aria-hidden="true">→</span></a>' for s in crs)
    rel = [(s, t) for s, (t, tags) in posts.items() if post_cat(s, tags) == cid][:6]
    post_links = "".join(f'<a href="post/{s}">{E(t)}<span aria-hidden="true">→</span></a>' for s, t in rel)
    others = "".join(f'<a class="chip" style="text-decoration:none" href="{HUBS[o][0]}">{E(HUBS[o][2])} ({len(all_cats[o]["exams"])})</a>'
                     for o in HUBS if o != cid and o in all_cats)
    qline = f"<div><strong>{qs:,}+</strong><span>questions</span></div>" if qs else ""
    body = f'''<section class="page-hero dark">
  <div class="container stack-lg">
    <p class="crumbs"><a href="./">Home</a> / <a href="training">Training</a> / {E(label)}</p>
    <p class="eyebrow">Free practice exams</p>
    <h1 class="h-xl">{E(h1[0].upper() + h1[1:])}</h1>
    <p class="lead">{E(intro)}</p>
    <div class="btn-row"><a class="btn" href="#exams">See the {n} exams</a><a class="btn btn-ghost-dark" href="training">All 10 categories</a></div><div class="stat-row"><div><strong>{n}</strong><span>practice exams</span></div>{qline}<div><strong>$0</strong><span>always free</span></div></div>
  </div>
</section>
<section class="section" id="exams" style="scroll-margin-top:84px;padding-top:64px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">{E(label)}</p><h2 class="h-lg">All {n} {E(label)} exams</h2></div></div>
  <div class="grid grid-4">{cards}</div>
  <p class="count" style="margin-top:24px">Each exam runs in your browser: no sign-up, and your answers stay on your device.</p>
</div></section>
''' + (f'''<section class="section sand"><div class="container grid grid-2">
  <div class="stack">{f'<p class="eyebrow">Learn first</p><h2 class="h-md">Related free courses</h2><div class="index">{course_links}</div>' if course_links else ''}</div>
  <div class="stack">{f'<p class="eyebrow">Read</p><h2 class="h-md">Related articles</h2><div class="index">{post_links}</div>' if post_links else ''}</div>
</div></section>
''' if (course_links or post_links) else "") + f'''<section class="section"><div class="container stack">
  <p class="eyebrow">More practice</p><h2 class="h-md">Other exam categories</h2>
  <div class="chips" role="list">{others}</div>
</div></section>
'''
    return head + tpl_top + body + tpl_foot


_ctitles = {}
def course_title(slug):
    if slug not in _ctitles:
        t = re.search(r"<title>(.*?)</title>", rd(f"challenge-page/{slug}.html"), re.S)
        _ctitles[slug] = html.unescape(t.group(1)).split(" | ")[0].strip() if t else slug
    return _ctitles[slug]


def build_hubs(all_cats, posts):
    t = rd("training.html")
    head = t[:t.index("</head>")]
    top = t[t.index("</head>"):t.index('<section class="page-hero dark">')]
    foot = t[t.index('<section class="cta">'):]
    n = 0
    for cid, cat in all_cats.items():
        if cid not in HUBS:
            continue
        page = hub_page(cid, cat, all_cats, posts, head, top, foot)
        f = HUBS[cid][0] + ".html"
        if not os.path.exists(os.path.join(ROOT, f)) or rd(f) != page:
            # keep the build-stamped parts (canonical, JSON-LD, asset versions) from the last run stable:
            # seo_pass re-adds them, so only rewrite when the generated content differs
            old = rd(f) if os.path.exists(os.path.join(ROOT, f)) else ""
            if strip_build(old) != strip_build(page):
                wr(f, page); n += 1
    return n


def strip_build(s):
    s = re.sub(r'<script type="application/ld\+json".*?</script>\n?', "", s, flags=re.S)
    s = re.sub(r"\?v=[0-9a-f]+", "", s)
    return s


# ---------- link blocks ----------

def put(s, name, block, before):
    a, b = M(name)
    s = re.sub(re.escape(a) + r".*?" + re.escape(b) + r"\n?", "", s, flags=re.S)
    if not block:
        return s
    for anchor in before:
        i = s.find(anchor)
        if i >= 0:
            return s[:i] + a + block + b + "\n" + s[i:]
    return s


def mini(cid, cat, exams, prefix, eyebrow, heading, lead):
    slug, h1, label, _ = HUBS[cid]
    items = "".join(f'<a href="{exam_url(e[1], prefix)}">{E(e[0])}<span aria-hidden="true">→</span></a>' for e in exams)
    return (f'<section class="section"><div class="container stack"><p class="eyebrow">{E(eyebrow)}</p>'
            f'<h2 class="h-md">{E(heading)}</h2><p class="muted">{lead}</p><div class="index">{items}'
            f'<a href="{prefix}{slug}"><strong>All {len(cat["exams"])} {E(label)} practice exams</strong><span aria-hidden="true">→</span></a>'
            f'</div></div></section>\n')


def link_training(all_cats):
    s = rd("training.html")
    chips = "".join(f'<a class="chip" style="text-decoration:none" href="{HUBS[c][0]}">{E(HUBS[c][2])} ({len(all_cats[c]["exams"])})</a>'
                    for c in HUBS if c in all_cats)
    block = (f'<section class="section" style="padding-top:0"><div class="container stack"><p class="eyebrow">Browse by category</p>'
             f'<h2 class="h-md">Practice exams by subject</h2><div class="chips" role="list">{chips}</div></div></section>\n')
    new = put(s, "training", block, ['<section class="section"><div class="container grid grid-2">', '<section class="cta">'])
    if new != s:
        wr("training.html", new); return 1
    return 0


def link_courses(all_cats):
    n = 0
    for slug, cid in COURSES.items():
        f = f"challenge-page/{slug}.html"
        if not os.path.exists(os.path.join(ROOT, f)) or cid not in all_cats:
            continue
        s = rd(f)
        exams = pick(all_cats[cid], course_title(slug))
        block = mini(cid, all_cats[cid], exams, "../", "Practice exams", "Practice exams for this course",
                     "Check what you have learned with these free practice exams.")
        new = put(s, "course", block, ['<section class="section sand">', "</main>"])
        if new != s:
            wr(f, new); n += 1
    return n


def link_posts(all_cats, posts):
    n = 0
    for slug, (title, tags) in posts.items():
        f = f"post/{slug}.html"
        if not os.path.exists(os.path.join(ROOT, f)):
            continue
        s = rd(f)
        if re.search(r'name="robots" content="noindex', s[:6000]):
            continue
        cid = post_cat(slug, tags)
        block = ""
        if cid and cid in all_cats:
            block = mini(cid, all_cats[cid], pick(all_cats[cid], title), "../", "Test what you have read",
                         f"Free {HUBS[cid][2]} practice exams", "Interactive exams with an explanation for every answer. No sign-up.")
        new = put(s, "post", block, ['<section class="section sand">', '<section class="cta">', "</main>"])
        if new != s:
            wr(f, new); n += 1
    return n


def run(root=None):
    all_cats = cats()
    posts = post_index()
    return {"hubs": build_hubs(all_cats, posts), "training": link_training(all_cats),
            "courses": link_courses(all_cats), "posts": link_posts(all_cats, posts)}


if __name__ == "__main__":
    print(run())
