"""Clean-up of the older (Wix-era and 2025) Insights articles (V4.71).

Usage:  python3 content/gen/legacy_fixes.py

The migrated articles have no JSON source; their built HTML is the source. This script edits that HTML and is
safe to run again (every change checks whether it has already been made).

What it does, for articles published before November 2026 (not the journal papers):
  1. TEXT_FIXES: visible errors found in the November 2026 audit (leftover AI writing instructions, a misspelled
     product name). Applied to the article and to its card on every page.
  2. Headings: articles with no <h2> get real headings. A paragraph that holds only bold text becomes an <h2>
     (an <h3> when it ends in a colon, e.g. "Pros:"). Where an article has <h3> headings but no <h2>, the <h3>s are
     promoted to <h2>.
  3. "Read next": a short paragraph at the end of the article text with links to three related articles and the
     matching Chmltech service page (marked data-readnext, replaced on each run). The "Related articles" cards
     below the article show the same three articles.
Related articles are picked by text similarity (TF-IDF of title, description and body), skipping articles that
are due to be merged or retired (SKIP) so the links do not point at addresses that will soon redirect.
"""
import glob, html, json, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
POST = os.path.join(ROOT, "post")
CUTOFF = "2026-11-01"

TEXT_FIXES = {
    # The first paragraph was the AI writing prompt left in by mistake (2023).
    "top-10-inventory-management-software-a-comprehensive-comparison-guide": [
        (re.compile(r"<p>\s*In this post, you could list and compare.*?</p>", re.S), ""),
    ],
    # The product is Katana MRP (katanamrp.com). The address keeps the old spelling so links still work.
    "optimize-your-production-schedule-with-kanata-mrp": [
        (re.compile(r"Kanata"), "Katana"),
        (re.compile(r"kanata(?= )"), "katana"),
    ],
}

# Articles to leave out of related links: due to be merged into another article or retired (audit V1, Nov 2026).
SKIP = {
    "identifying-non-value-added", "what-are-the-core-values-of-process-improvement-part-ii",
    "3-simple-steps-to-solve-your-team-communication-gaps", "how-to-streamline-business-processes-and-workflows-to-improve-efficiency",
    "do-you-have-the-right-kpis-set-for-each-team-member", "esg-2022-the-transformation-of-the-c-suite-and-boardroom",
    "understanding-12-types-of-key-performance-indicators", "revolutionizing-healthcare-with-digital-process-improvement",
    "from-strangers-to-customers-a-guide-to-understanding-the-different-stages-of-the-marketing-funnel",
    "how-apis-can-revolutionize-your-marketing-and-sales-efforts", "navigating-the-challenges-of-erp-implementation-common-pitfalls-and-how-to-avoid-them",
    "7-ways-operational-efficiency-can-help-reduce-costs-in-your-business", "boosting-business-success-with-operations-efficiency-tips-and-strategies",
    "revolutionizing-business-operations-how-ai-is-streamlining-efficiency-and-boosting-performance",
    "api-integration-tips-and-best-practices", "apis-and-artificial-intelligence-enhancing-business-operations",
    "improving-operational-efficiency-technology-kpis-and-integration-for-small-businesses",
    "mastering-prompt-engineering-for-natural-language-processing", "the-ultimate-guide-to-seo-and-google-search-expert-tips-and-case-studies",
    "chain-of-thought-prompting-with-chatgpt-best-practices-for-enhancing-ai-interaction",
    "the-driving-force-behind-tesla-s-operational-efficiency-under-elon-musk-s-leadership",
    "5-change-models-every-ai-data-leader-should-know", "how-to-effectively-use-social-media-to-improve-business-visibility-and-attract-customers",
    "maximizing-business-efficiency-with-ai-agents", "unlocking-the-power-of-agentic-ai-for-small-business-growth-and-efficiency",
    "how-ai-agents-are-revolutionizing-business-and-impacting-daily-life", "boost-your-search-rankings-with-ai-powered-seo-strategies",
    "why-a-strong-sales-process-is-essential-and-how-it-helps-increase-revenue",
    # retired in V4.71
    "case-study-two-pf-the-keys-to-walmart-s-success", "five-ways-that-esg-creates-value",
    # retired in V4.73
    "optimize-your-production-schedule-with-kanata-mrp",
}

# Book reviews with a matching exam page.
EXAM = {
    "atomic-habits-by-james-clear-a-deep-dive-review-and-guide-to-habit-transformation": ("atomic-habits.html", "Atomic Habits"),
    "the-psychology-of-money-by-morgan-housel-a-thought-provoking-review-on-wealth-behavior-and-happin": ("psychology-of-money.html", "The Psychology of Money"),
}

# Service page for an article's first category with one (ESG, case studies and book reviews have none).
SERVICE = {
    "process-improvement": ("process-improvement.html", "process improvement consulting"),
    "operational-efficiency": ("operational-efficiency.html", "operational efficiency consulting"),
    "lean": ("lean-six-sigma-training.html", "Lean Six Sigma training"),
    "six-sigma": ("lean-six-sigma-training.html", "Lean Six Sigma training"),
    "artificial-intelligence": ("artificial-intelligence.html", "AI consulting for small and mid-sized businesses"),
    "digital-technology": ("ai-operating-system.html", "AI Operating System design and build"),
    "erp": ("business-process-optimization.html", "business process optimization consulting"),
    "inventory-management": ("operational-efficiency.html", "operational efficiency consulting"),
    "project-management": ("project-portfolio-management.html", "project portfolio management consulting"),
    "agile": ("project-portfolio-management.html", "project portfolio management consulting"),
    "change-management": ("leadership-operating-system.html", "leadership operating system"),
    "strategy": ("scaling-up.html", "growth consulting"),
    "iso": ("iso9001.html", "ISO 9001 consulting"),
    "marketing": ("scaling-up.html", "growth consulting"),
}


def body_of(s):
    m = re.search(r'(<article class="prose[^"]*">)(.*?)(</article>)', s, re.S)
    return m


def plain(x):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|svg)[\s\S]*?</\1>", " ", x))))


def load():
    arts = {}
    for p in sorted(glob.glob(os.path.join(POST, "*.html"))):
        s = open(p, encoding="utf-8").read()
        if 'http-equiv="refresh"' in s: continue
        slug = os.path.basename(p)[:-5]
        m = body_of(s)
        if not m: continue
        pub = re.search(r'published_time" content="([^"]+)', s)
        title = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1)).replace(" | Chmltech Ltd.", "")
        desc = re.search(r'name="description" content="([^"]*)', s)
        arts[slug] = dict(path=p, s=s, pub=pub.group(1) if pub else "", title=title,
                          desc=html.unescape(desc.group(1)) if desc else "", text=plain(re.sub(r'<p data-readnext>.*?</p>|<details class="a-toc-m".*?</details>', "", m.group(2), flags=re.S)),
                          journal="j-paper" in s,
                          built=os.path.exists(os.path.join(ROOT, "content", "articles", slug + ".json")),   # rewritten from JSON: not edited here (V4.76)
                          cats=re.findall(r'insights\.html#cat=([\w-]+)', s[:m.start()]))
    return arts


def caps(t):
    """Normal capitals for an ALL-CAPS heading, keeping acronyms."""
    keep = {"ESG", "KPI", "KPIS", "ERP", "MRP", "AI", "API", "SEO", "ISO", "CRM", "SME", "SMES", "OEE", "5S", "TOC", "DMAIC"}
    small = {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to", "vs", "with"}
    w = [x if x.strip("?:!.,") in keep else (x.lower() if i and x.lower() in small else x.capitalize())
         for i, x in enumerate(t.split())]
    return " ".join(w).replace("KPIS", "KPIs").replace("SMES", "SMEs")


def headings(b):
    b = re.sub(r"<h2>([^<a-z]{4,})</h2>", lambda m: f"<h2>{caps(m.group(1))}</h2>" if re.search(r"[A-Z]{3}", m.group(1)) else m.group(0), b)
    if "<h2" in b: return b, 0
    n = 0
    def rep(m):
        nonlocal n
        t = re.sub(r"\s+", " ", m.group(1)).strip()
        if len(t) > 110 or t.endswith((".", "?", "!")) and len(t) > 70: return m.group(0)
        n += 1
        if t.isupper(): t = caps(t)
        if t.endswith(":"): return f"<h3>{t[:-1].strip()}</h3>"
        return f"<h2>{t}</h2>"
    b = re.sub(r"<p>\s*(?:<strong>\s*)+([^<]{2,120}?)\s*(?:</strong>\s*)+</p>", rep, b)
    if n == 0 and "<h3" in b:
        n = len(re.findall(r"<h3", b))
        b = re.sub(r"<h3([^>]*)>", r"<h2\1>", b).replace("</h3>", "</h2>")
    return b, n


def orphan_captions(b):
    """Remove <figcaption> elements that are not inside a <figure>: the migration dropped the images but kept their captions."""
    parts = re.split(r'(<figure\b.*?</figure>)', b, flags=re.S)
    return "".join(x if x.startswith("<figure") else re.sub(r'<figcaption>[^<]*</figcaption>', "", x) for x in parts)


def related(arts):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    slugs = list(arts)
    docs = [(arts[x]["title"] + " ") * 3 + (arts[x]["desc"] + " ") * 2 + arts[x]["text"] for x in slugs]
    M = TfidfVectorizer(stop_words="english", sublinear_tf=True, max_df=0.5, ngram_range=(1, 2), min_df=2).fit_transform(docs)
    S = cosine_similarity(M)
    out = {}
    for i, x in enumerate(slugs):
        ranked = [j for j in sorted(range(len(slugs)), key=lambda j: -S[i, j]) if slugs[j] != x and slugs[j] not in SKIP]
        mine = set(arts[x]["cats"]) - {"chmltech-online-journal"}
        same = [j for j in ranked if mine & set(arts[slugs[j]]["cats"]) and S[i, j] > 0.05]
        pick = [slugs[j] for j in (same + [j for j in ranked if j not in same])][:3]   # same category first
        out[x] = pick
    return out


def card(insights, slug):
    m = re.search(r'<article class="article"(?:(?!</article>).)*?href="post/' + re.escape(slug) + r'\.html".*?</article>', insights, re.S)
    if not m: return None
    return m.group(0).replace('href="post/', 'href="../post/').replace('src="assets/', 'src="../assets/')


def main():
    arts = load()
    insights = open(os.path.join(ROOT, "insights.html"), encoding="utf-8").read()
    # 1. text fixes: article page and cards on every page
    pages = glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(POST, "*.html"))
    for slug, subs in TEXT_FIXES.items():
        for p in pages:
            s = open(p, encoding="utf-8").read()
            t = s
            if os.path.basename(p) == slug + ".html":
                for rx, new in subs: t = rx.sub(new, t)
            else:
                cm = re.search(r'<article class="article"(?:(?!</article>).)*?post/' + re.escape(slug) + r'\.html".*?</article>', t, re.S)
                if cm:
                    c = cm.group(0)
                    for rx, new in subs:
                        if rx.pattern.startswith("<p>"): continue
                        c = rx.sub(new, c)   # the address keeps "kanata-mrp" (lower case, then a hyphen)
                    t = t[:cm.start()] + c + t[cm.end():]
            if t != s:
                open(p, "w", encoding="utf-8").write(t); print("text fix:", slug, "->", os.path.relpath(p, ROOT))
    arts = load()
    insights = open(os.path.join(ROOT, "insights.html"), encoding="utf-8").read()   # re-read: cards now fixed
    rel = related(arts)
    nh = nr = 0
    for slug, a in arts.items():
        if a["journal"] or a["built"] or not a["pub"] or a["pub"] >= CUTOFF: continue
        s = a["s"]; m = body_of(s)
        b, n = headings(m.group(2))
        # 2b. captions left behind when stock photos were dropped in the migration (V4.73)
        b = orphan_captions(b)
        if n: nh += 1; print(f"headings: {slug} ({n})")
        # 3. read-next paragraph
        b = re.sub(r'\s*<p data-readnext>.*?</p>', "", b, flags=re.S)
        links = "; ".join(f'<a href="{x}.html">{html.escape(arts[x]["title"])}</a>' for x in rel[slug])
        svc = next((SERVICE[c] for c in a["cats"] if c in SERVICE), None)
        extra = f' If you want help putting this into practice, see our <a href="../{svc[0]}">{svc[1]}</a>.' if svc else ""
        if slug in EXAM: extra += f' Test what you remember with our free <a href="../{EXAM[slug][0]}">{EXAM[slug][1]} exam</a>.'
        b = b.rstrip() + f'\n<p data-readnext><strong>Read next:</strong> {links}.{extra}</p>\n'
        s = s[:m.start(2)] + b + s[m.end(2):]
        # related cards below the article
        cards = [card(insights, x) for x in rel[slug]]
        if all(cards):
            rm = re.search(r'(Related articles</h2>.*?<div class="grid grid-3">)(.*?)(</div>\s*</div></section>)', s, re.S)
            if rm: s = s[:rm.start(2)] + "".join(cards) + s[rm.end(2):]
        if s != a["s"]:
            open(a["path"], "w", encoding="utf-8").write(s); nr += 1
    print(f"{nh} articles given headings; {nr} articles updated")


if __name__ == "__main__":
    main()
