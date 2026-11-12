"""Chmltech Online Journal papers in research-paper format (V4.12). Content: journal/<slug>.json (see journal/SPEC.md)."""
import datetime, glob, json, os, re

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "journal")
JOURNAL = "Chmltech Online Journal"


def load():
    out = {}
    for f in sorted(glob.glob(os.path.join(SRC, "*.json"))):
        d = json.load(open(f))
        out[d["slug"]] = d
    return out


def words(d):
    n = 0
    for s in d["sections"]:
        for b in s["blocks"]:
            for k in ("p", "callout"):
                if k in b: n += len(re.sub("<[^>]+>", "", b[k]).split())
            if "list" in b: n += sum(len(x.split()) for x in b["list"])
    return n + len(d["abstract"].split())


def add_new_posts(POSTS, cat="chmltech-online-journal"):
    """Journal papers written directly for this site (no Wix original) become Insights posts too."""
    have = {p["slug"] for p in POSTS}
    for slug, d in load().items():
        if slug in have: continue
        POSTS.append(dict(slug=slug, title=d["title"], date=d["published"][:10], author=d["author"]["name"], read="",
                          desc=d["meta"], cover=None, body="", cats=[cat], tags=d["keywords"][:10]))
    J = load()   # same-day papers: newest volume and issue first (V4.19)
    rank = lambda p: (p["date"], (J[p["slug"]]["volume"], J[p["slug"]]["issue"]) if p["slug"] in J else (0, 0))
    POSTS.sort(key=rank, reverse=True)


JOURNAL_CAT = "chmltech-online-journal"
# Each paper is listed under the journal and under its subject category (V4.18).
# Process plant papers are also listed under Process Engineering (V4.40).
TOPIC = {
    "chmltech-online-journal-volume-103-issue-1": "artificial-intelligence",
    "copy-of-chmltech-online-journal-volume-103-issue-2": "artificial-intelligence",
    "ai-operating-systems-architecture-and-governance-for-enterprise-ai": "artificial-intelligence",
    "multi-agent-ai-systems-architectures-coordination-and-failure-modes": "artificial-intelligence",
    "retrieval-augmented-generation-design-evaluation-and-failure-analysis": "artificial-intelligence",
    "designing-machine-learning-systems-from-problem-framing-to-production": "artificial-intelligence",
    "advancements-and-challenges-in-solid-state-hydrogen-absorption-a-comprehensive-review": ["process-engineering", "esg"],
    "chmltech-online-journal-volume-102-issue-1": ["process-engineering", "esg"],
    "engineering-capex-and-opex-estimation-for-process-plants": ["process-engineering", "operational-efficiency"],
    "digital-twins-in-chemical-process-plants-architecture-modeling-and-applications": ["process-engineering", "digital-technology"],
    # Volume 105: Physical AI (V4.19). A list files the paper under more than one subject.
    "physical-ai-foundations-architectures-and-the-sim-to-real-gap": "artificial-intelligence",
    "physical-ai-in-process-plants-and-factories-inspection-manipulation-and-control": ["artificial-intelligence", "digital-technology", "process-engineering"],
    "safety-reliability-and-economics-of-deploying-physical-ai": "artificial-intelligence",
    # Volume 104, Issue 7 (V4.53)
    "score-versus-cost-per-task-returns-to-reasoning-effort-in-frontier-language-models": "artificial-intelligence",
    # Volume 105, Issues 4-6: agentic AI (V4.61)
    "agent-interoperability-standards-mcp-a2a-erp-crm-plant-systems": ["artificial-intelligence", "digital-technology"],
    "agent-security-and-identity-prompt-injection-least-privilege-credentials-audit": "artificial-intelligence",
    "agent-readiness-for-small-and-mid-sized-firms-data-process-staged-adoption": ["artificial-intelligence", "digital-technology"],
}


def apply_to_posts(POSTS):
    """Use each paper's real title, description and read time on cards and listings."""
    J = load()
    for p in POSTS:
        d = J.get(p["slug"])
        if not d: continue
        p["title"] = d["title"]; p["desc"] = d["meta"]
        p["read"] = f"{max(1, round(words(d) / 220))} min read"
        p["journal"] = f"Vol. {d['volume']}, Issue {d['issue']}"
        t = TOPIC.get(p["slug"], [])
        p["cats"] = [JOURNAL_CAT] + ([t] if isinstance(t, str) else list(t))
    return J


def pdf_name(d):
    """Published file name of the paper's PDF (served from assets/journal/pdf/, not indexed)."""
    return f"chmltech-journal-vol{d['volume']}-issue{d['issue']}.pdf"


def _date(s, fmt="%B %-d, %Y"):
    return datetime.date.fromisoformat(s[:10]).strftime(fmt)


def _sid(num, title):
    return "sec-" + str(num)


FIG_DIR = os.path.join(SRC, "figures")


def render_fig(slug, F, esc):
    svg = open(os.path.join(FIG_DIR, slug, F["id"] + ".svg")).read()
    svg = svg.replace("<svg ", f'<svg role="img" aria-labelledby="fig-{F["n"]}-t" ', 1)
    svg = re.sub(r"(<svg[^>]*>)", lambda m: m.group(1) + f'<title id="fig-{F["n"]}-t">{esc(F["alt"])}</title>', svg, count=1)
    src = f' <span class="j-fig-src">{F["source"]}</span>' if F.get("source") else ""
    return (f'<figure class="j-fig" id="figure-{F["n"]}"><div class="j-fig-art">{svg}</div>'
            f'<figcaption><strong>Figure {F["n"]}.</strong> {F["caption"]}{src}</figcaption></figure>')


def render_blocks(blocks, esc_ok, slug=""):
    h = ""
    ul_open = False
    for b in blocks:
        if "p" in b: h += f"<p>{b['p']}</p>"
        elif "h3" in b: h += f"<h3>{b['h3']}</h3>"
        elif "eq" in b: h += f'<div class="j-eq" role="math"><span class="j-eq-body">{b["eq"]}</span><span class="j-eq-n">({b["n"]})</span></div>'
        elif "list" in b:
            tag = "ol" if b.get("ordered") else "ul"
            h += f"<{tag}>" + "".join(f"<li>{x}</li>" for x in b["list"]) + f"</{tag}>"
        elif "table" in b:
            t = b["table"]
            h += (f'<figure class="j-table" id="table-{t["n"]}"><figcaption><strong>Table {t["n"]}.</strong> {t["caption"]}</figcaption>'
                  f'<div class="j-table-scroll"><table><thead><tr>' + "".join(f"<th>{c}</th>" for c in t["head"]) + "</tr></thead><tbody>"
                  + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in t["rows"]) + "</tbody></table></div>"
                  + (f'<p class="j-table-note">{t["note"]}</p>' if t.get("note") else "") + "</figure>")
        elif "callout" in b: h += f'<aside class="j-callout"><p>{b["callout"]}</p></aside>'
        elif "fig" in b: h += render_fig(slug, b["fig"], esc_ok)
    return h


def link_citations(html):
    def one(m):
        inner = m.group(1)
        parts = re.split(r"(\d+)", inner)
        return "[" + "".join(f'<a href="#ref-{x}" class="j-cite">{x}</a>' if x.isdigit() else x for x in parts) + "]"
    return re.sub(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\]", one, html)


def build(ns):
    sub_page, esc, card, POSTS, SITE_URL, OUT = ns["sub_page"], ns["esc"], ns["card"], ns["POSTS"], ns["SITE_URL"], ns["OUT"]
    J = load()
    jposts = [p for p in POSTS if p["slug"] in J]
    for slug, d in J.items():
        A = d["author"]; is_rev = d["revised"][:10] != d["published"][:10]
        cite_txt = (f'{A["name"].split()[-1]}, {". ".join(x[0] for x in A["name"].split()[:-1])}. ({d["published"][:4]}). {d["title"]}. '
                    f'<em>{JOURNAL}</em>, <em>{d["volume"]}</em>({d["issue"]}).{" Revised " + _date(d["revised"]) + "." if d["revised"][:10] != d["published"][:10] else ""} {SITE_URL}/post/{slug}')
        toc = "".join(f'<li><a href="#{_sid(s["num"], s["title"])}">{s["num"]}. {esc(re.sub("<[^>]+>", "", s["title"]))}</a></li>' for s in d["sections"])
        toc = '<li><a href="#abstract">Abstract</a></li>' + toc + '<li><a href="#references">References</a></li>'
        secs = "".join(f'<section class="j-sec" id="{_sid(s["num"], s["title"])}"><h2><span class="j-num">{s["num"]}.</span> {s["title"]}</h2>{render_blocks(s["blocks"], esc, slug)}</section>' for s in d["sections"])
        secs = link_citations(secs)
        refs = "".join(f'<li id="ref-{i}">{r["text"]} <a href="{esc(r["url"])}" rel="noopener" target="_blank">{esc(re.sub(r"^https://(doi.org/)?", "", r["url"]))[:80]}</a></li>'
                       for i, r in enumerate(d["references"], 1))
        mins = max(1, round(words(d) / 220))
        others = [q for q in jposts if q["slug"] != slug][:3]
        ld = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": re.sub("<[^>]+>", "", d["title"]),
              "name": re.sub("<[^>]+>", "", d["title"]), "abstract": re.sub("<[^>]+>", "", d["abstract"]), "keywords": ", ".join(d["keywords"]),
              "datePublished": d["published"][:10], "dateModified": d["revised"],
              "author": {"@type": "Person", "name": A["name"], "jobTitle": A["role"], "affiliation": {"@type": "Organization", "name": A["org"]}},
              "publisher": {"@type": "Organization", "name": "Chmltech Ltd."},
              "isPartOf": {"@type": "PublicationIssue", "issueNumber": str(d["issue"]),
                           "isPartOf": {"@type": "PublicationVolume", "volumeNumber": str(d["volume"]), "isPartOf": {"@type": "Periodical", "name": JOURNAL}}},
              "mainEntityOfPage": f"{SITE_URL}/post/{slug}", "citation": [re.sub("<[^>]+>", "", r["text"]) for r in d["references"]]}
        body = f'''<section class="page-hero dark j-hero">
  <div class="container stack-lg">
    <p class="crumbs"><a href="index.html">Home</a> / <a href="insights.html">Insights</a> / <a href="insights.html#cat=chmltech-online-journal">{JOURNAL}</a></p>
    <p class="j-masthead"><span>{JOURNAL}</span><span>Volume {d["volume"]}, Issue {d["issue"]}</span><span>Research article</span></p>
    <h1 class="h-xl j-title">{d["title"]}</h1>
    <div class="j-author"><strong>{esc(A["name"])}</strong><span>{esc(A["role"])}, {esc(A["org"])}</span><span>{esc(A["division"])} · {esc(A.get("location", ""))}</span></div>
    <p class="post-meta"><span>Published {_date(d["published"])}</span>{f'<span>Revised {_date(d["revised"])}</span>' if is_rev else ''}<span>{mins} min read</span></p>
  </div>
</section>
<section class="section j-wrap"><div class="container layout-aside">
  <article class="prose j-paper">
    <section class="j-abstract" id="abstract"><h2>Abstract</h2><p>{d["abstract"]}</p>
      <p class="j-keywords"><strong>Keywords:</strong> {"; ".join(esc(k) for k in d["keywords"])}</p></section>
    <aside class="j-dl-box"><div><strong>Download this paper as a PDF</strong><span>Free. Formatted for printing, with all figures and references.</span></div>
      <button type="button" class="btn" data-jdl>Download PDF</button></aside>
    {secs}
    <section class="j-sec j-refs" id="references"><h2>References</h2><ol>{refs}</ol></section>
    <section class="j-cite-box"><h2>How to cite this article</h2><p>{cite_txt}</p>
      {f'<p class="j-revnote">This article was first published on {_date(d["published"])}. The revised edition of {_date(d["revised"])} expands the original, corrects technical errors and adds verified references.</p>' if is_rev else ''}</section>
  </article>
  <aside class="aside-sticky j-aside">
    <nav class="card j-toc" aria-label="Contents"><p class="eyebrow">Contents</p><ol>{toc}</ol></nav>
    <div class="card" style="padding:22px"><p class="eyebrow">Article</p><p style="font-size:14.5px;margin:6px 0 14px">{JOURNAL}<br>Volume {d["volume"]}, Issue {d["issue"]}</p>
      <button type="button" class="btn btn-ghost" data-jdl>Download PDF</button></div>
    <div class="card card-dark" style="padding:24px"><p class="eyebrow">Work with Chmltech</p><h3 style="font-size:20px">Discuss this research</h3><p>Talk to us about applying it in your organization.</p><a class="btn" href="contact.html" style="align-self:flex-start">Contact us</a></div>
  </aside>
</div></section>
<section class="section sand j-related"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">{JOURNAL}</p><h2 class="h-lg">More from the journal</h2></div><a class="btn btn-ghost" href="insights.html#cat=chmltech-online-journal">All journal articles</a></div>
  <div class="grid grid-3">{"".join(card(q) for q in others)}</div>
</div></section>
<dialog class="j-dialog" id="jdl" aria-labelledby="jdl-title" data-pdf="../assets/journal/pdf/{pdf_name(d)}" data-fname="Chmltech-Journal-Vol{d["volume"]}-Issue{d["issue"]}.pdf" data-title="{esc(re.sub("<[^>]+>", "", d["title"]))}" data-ref="Vol. {d["volume"]}, Issue {d["issue"]}">
  <form method="dialog" class="form j-dl-form" novalidate>
    <button type="button" class="j-dl-close" aria-label="Close">×</button>
    <p class="eyebrow">{JOURNAL} · Vol. {d["volume"]}, Issue {d["issue"]}</p>
    <h2 class="h-md" id="jdl-title">Download the PDF</h2>
    <p class="muted j-dl-paper">{d["title"]}</p>
    <input class="hp" type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="field"><label for="jdl-name">Full name</label><input id="jdl-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="jdl-email">Work email</label><input id="jdl-email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="jdl-company">Company <span class="hint">(optional)</span></label><input id="jdl-company" name="company" autocomplete="organization"></div>
    <label class="j-dl-consent"><input type="checkbox" name="updates" value="Yes"> Send me occasional updates on new Chmltech research and services. I can unsubscribe at any time.</label>
    <p class="j-dl-note">We use your details to record this request and may follow up about it. See our <a href="privacy.html" target="_blank" rel="noopener">privacy notice</a>.</p>
    <button type="submit" class="btn">Download PDF</button>
    <p class="form-status" role="status" tabindex="-1"></p>
  </form>
</dialog>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'''
        title_txt = re.sub("<[^>]+>", "", d["title"])
        sub_page(f"post/{slug}.html", title_txt, esc(d["meta"]), body)
        fp = os.path.join(OUT, "post", slug + ".html"); h = open(fp).read()
        h = h.replace(f'<meta property="og:image" content="{SITE_URL}/assets/img/chmltech-mark.png">',
                      f'<meta property="og:image" content="{SITE_URL}/assets/media/covers/{slug}.jpg">\n<meta name="twitter:card" content="summary_large_image">', 1)
        h = h.replace("</head>", '<link rel="stylesheet" href="../assets/css/journal.css">\n</head>', 1)
        h = h.replace("</body>", '<script src="../assets/js/journal.js" defer></script>\n</body>', 1)
        h = h.replace("</head>", f'<meta name="citation_title" content="{esc(title_txt)}">\n<meta name="citation_author" content="{esc(A["name"])}">\n'
                      f'<meta name="citation_publication_date" content="{d["published"][:10].replace("-", "/")}">\n<meta name="citation_journal_title" content="{JOURNAL}">\n'
                      f'<meta name="citation_volume" content="{d["volume"]}">\n<meta name="citation_issue" content="{d["issue"]}">\n</head>', 1)
        open(fp, "w").write(h)
