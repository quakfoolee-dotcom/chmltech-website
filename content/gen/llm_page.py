"""LLM Leaderboard page (llm-leaderboard.html): a searchable database of current large language models with a leaderboard,
best-model-by-agent-type rankings and a score-versus-cost Pareto frontier.

Data: content/llm/llm.json (built by content/llm/build_dataset.py from research files; every score and price carries its source URL).
The page shell (header, navigation, footer) is copied from funding.html so the page matches the rest of the site.
The dataset is embedded as <script type="application/json" id="llm-data"> for assets/js/llm.js. Styles: assets/css/llm.css
plus the gr- filter classes in assets/css/grants.css.

Run: python3 content/gen/llm_page.py   (from the site root)
"""
import json, os, re, html as H, datetime
import assetver

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "content", "llm", "llm.json")
FNAME = "llm-leaderboard.html"
SITE = "https://www.chmltech.com"
esc = lambda s: H.escape(str(s if s is not None else ""), quote=True)

TIERS = ["Frontier", "Mid-size", "Small and fast"]
ACCESS = ["Proprietary API", "Open weights"]
CAPS = ["Reasoning mode", "Image input", "Audio input", "Video input", "Computer use", "1M+ token context"]


def fmt(v, unit):
    if v is None:
        return "–"
    if unit == "%":
        return f"{v:.1f}%"
    if unit == "USD":
        return f"${round(v):,}"
    if abs(v) >= 100:
        return f"{round(v):,}"
    return f"{round(v, 1)}"


def group(key, legend, values, counts, open_=False, note=""):
    opts = "".join(f'<label class="gr-opt"><input type="checkbox" name="{key}" value="{esc(v)}"><span class="gr-opt-l">{esc(v)}</span>'
                   f'<span class="gr-opt-n" data-n>{counts.get(v, 0)}</span></label>' for v in values)
    return (f'<details class="gr-group" data-group="{key}"{" open" if open_ else ""}><summary><span>{legend}</span><span class="gr-group-n" data-sel hidden></span></summary>'
            f'<fieldset><legend class="visually-hidden">{legend}</legend>{note}<div class="gr-opts">{opts}</div></fieldset></details>')


def radios(name, legend, opts):
    r = "".join(f'<label class="ll-radio"><input type="radio" name="{name}" value="{v}"{" checked" if not v else ""}>{esc(l)}</label>' for v, l in opts)
    return (f'<details class="gr-group" data-group="{name}"><summary><span>{legend}</span></summary>'
            f'<fieldset><legend class="visually-hidden">{legend}</legend><div class="gr-opts">{r}</div></fieldset></details>')


def count(models, f):
    c = {}
    for m in models:
        v = f(m)
        for x in (v if isinstance(v, list) else [v]):
            if x:
                c[x] = c.get(x, 0) + 1
    return c


def shell():
    """Header and footer from funding.html, so navigation and footer stay identical to the rest of the site."""
    s = open(os.path.join(ROOT, "funding.html"), encoding="utf-8").read(); s = assetver.strip(s)
    head, rest = s.split('<main id="main">', 1)
    foot = rest.split("</main>", 1)[1]
    head = head.replace(' aria-current="page"', "")
    head = head.replace('<link rel="stylesheet" href="assets/css/grants.css">', '<link rel="stylesheet" href="assets/css/grants.css">\n<link rel="stylesheet" href="assets/css/llm.css">')
    foot = foot.replace('<script src="assets/js/grants.js" defer></script>', '<script src="assets/js/llm.js" defer></script>')
    return head, foot


def meta(head, title, desc):
    full = f"{title} | Chmltech Ltd."
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(full)}</title>", head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(desc), head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(full), head, count=1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + esc(desc), head, count=1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + f"{SITE}/{FNAME}", head, count=1)
    head = head.replace(f'<a href="{FNAME}">', f'<a href="{FNAME}" aria-current="page">', 1)
    return head


def type_card(g, D):
    by = {b["id"]: b for b in D["benchmarks"]}
    b = by[g["bench"]]
    hb = b.get("hb", True)
    rows = [(m, m["s"][b["id"]]) for m in D["models"] if b["id"] in m.get("s", {})]
    rows.sort(key=lambda r: -r[1]["v"] if hb else r[1]["v"])
    top = "".join(f'<li><b>{i + 1}</b><span>{esc(m["name"])}{"<small class=ll-pre title=\"" + esc(r["flag"]) + "\"> pre-launch</small>" if r.get("flag") else ""}</span>'
                  f'<em>{fmt(r["v"], b.get("unit"))}</em></li>' for i, (m, r) in enumerate(rows[:5]))
    also = ", ".join(by[x]["short"] for x in g.get("also", []) if x in by)
    return (f'<article class="ll-type"><h3>{esc(g["name"])}</h3><p class="ll-type-desc">{esc(g["desc"])}</p>'
            f'<ol aria-label="Top five on {esc(b["name"])}">{top}</ol>'
            f'<p class="ll-type-src">Ranked by {esc(b["name"])} ({esc(b["src"])}; {esc(b.get("updated") or "")}). {len(rows)} of the listed models have a result.'
            f'{" Also see: " + esc(also) + "." if also else ""}</p>'
            f'<button type="button" class="gr-link" data-bench="{esc(b["id"])}">See the full ranking</button></article>')


def build():
    D = json.load(open(DATA, encoding="utf-8"))
    M, B = D["models"], D["benchmarks"]
    n, n_dev = len(M), len({m["dev"] for m in M})
    n_open = sum(1 for m in M if m["access"] == "Open weights")
    n_scores = sum(len(m.get("s", {})) for m in M)
    asof = datetime.date.fromisoformat(D["as_of"]).strftime("%B %-d, %Y")

    devs = sorted({m["dev"] for m in M}, key=lambda d: (-sum(1 for m in M if m["dev"] == d), d))
    cd, ca, ct, cc = count(M, lambda m: m["dev"]), count(M, lambda m: m["access"]), count(M, lambda m: m["tier"]), count(M, lambda m: m.get("caps") or [])
    filters = "".join([
        group("t", "Model type", [t for t in TIERS if ct.get(t)], ct, True,
              '<p class="gr-hint">The model\'s place in its developer\'s line-up (flagship, one step down, or small), not a capability score.</p>'),
        group("a", "Access", [a for a in ACCESS if ca.get(a)], ca, True),
        group("c", "Capability", [c for c in CAPS if cc.get(c)], cc),
        group("d", "Developer", devs, cd),
        radios("price", "Blended price", [("", "Any price"), ("1", "Up to $1 per 1M tokens"), ("5", "Up to $5 per 1M tokens"), ("15", "Up to $15 per 1M tokens")]),
        radios("ctx", "Context window", [("", "Any size"), ("128000", "At least 128K tokens"), ("400000", "At least 400K tokens"), ("1000000", "At least 1M tokens")]),
    ])
    sections = {}
    for b in B:
        sections.setdefault(b["section"], []).append(b)
    bench_opts = "".join(f'<optgroup label="{esc(sec)}">' + "".join(
        f'<option value="{esc(b["id"])}"{" selected" if b["id"] == D["default_benchmark"] else ""}>{esc(b["name"])}</option>' for b in bs) + "</optgroup>"
        for sec, bs in sections.items())

    types = "".join(type_card(g, D) for g in D["groups"])
    gloss = "".join(f'<tr><td>{esc(b["name"])}</td><td>{esc(b["what"])}{(" " + esc(b["caveat"])) if b.get("caveat") else ""}</td>'
                    f'<td><a href="{esc(b["url"])}" target="_blank" rel="noopener">{esc(b["src"])}</a><span class="ll-sub">{esc(b.get("updated") or "")}</span></td></tr>' for b in B)
    search_svg = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
                  '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>')
    steps = D["method_steps"]
    stepcards = "".join(f'<article class="card ll-step"><h3>{esc(t)}</h3><p>{esc(d)}</p></article>' for t, d in steps)

    body = f'''<section class="page-hero dark course-hero gr-hero ll-hero"><div class="container"><div class="stack-lg">
  <p class="crumbs"><a href="index.html">Home</a> / LLM leaderboard</p>
  <p class="eyebrow">LLM leaderboard</p>
  <h1 class="h-xl" style="font-size:clamp(34px,4.4vw,56px)">Which AI model fits the job, and what does it cost?</h1>
  <p class="lead">A searchable database of current large language models from {n_dev} developers. Compare them on independent benchmarks, find the strongest model for each kind of AI agent, and see which models give the most capability for the money. Every score and price links to the page it came from.</p>
  <div class="stat-row"><div><strong>{n}</strong><span>models</span></div><div><strong>{len(B)}</strong><span>benchmarks</span></div><div><strong>{n_open}</strong><span>open-weight models</span></div><div><strong class="ll-stat-sm">{asof}</strong><span>data as of</span></div></div>
  <div class="btn-row"><a class="btn" href="#explorer">Search the models</a><a class="btn btn-ghost-dark" href="#agents">Best by agent type</a></div>
</div></div></section>

<section class="section" id="agents" style="scroll-margin-top:84px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Best by agent type</p><h2 class="h-lg">The strongest models for each kind of agent.</h2></div>
  <p>Each card ranks models on the independent benchmark closest to that job. A high score is a starting point for your own trial, not a guarantee on your tasks.</p></div>
  <div class="ll-types">{types}</div>
</div></section>

<section class="section sand gr-section" id="explorer" style="scroll-margin-top:84px" aria-labelledby="ll-h"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Model explorer</p><h2 class="h-lg" id="ll-h">Search, filter and rank {n} models.</h2></div>
  <p>Pick a benchmark to rank by. Switch to the chart to see the Pareto frontier: the models that no cheaper model beats.</p></div>
  <div class="gr-finder ll-root" id="ll-root">
    <div class="gr-mobilebar"><button type="button" class="btn btn-ghost gr-filter-btn" aria-expanded="false" aria-controls="gr-filters">Filters<span class="gr-badge" data-active-n hidden></span></button></div>
    <aside class="gr-filters" id="gr-filters" aria-label="Filters">
      <form class="gr-form">
        <div class="gr-filters-head"><h3>Filters</h3><button type="button" class="gr-link" data-clear>Clear all filters</button></div>
        {filters}
        <button type="button" class="btn gr-apply" data-close>Show <span data-close-n>{n}</span> models</button>
      </form>
    </aside>
    <div class="gr-results">
      <div class="gr-toolbar">
        <label class="search gr-search"><span class="visually-hidden">Search models</span>{search_svg}<input type="search" id="ll-q" placeholder="Search model, developer or licence" autocomplete="off"></label>
      </div>
      <div class="ll-controls">
        <label class="gr-sort"><span>Rank by</span><select id="ll-bench">{bench_opts}</select></label>
        <div class="ll-tabs" role="tablist" aria-label="View"><button type="button" class="ll-tab" role="tab" data-view="table" aria-selected="true">Leaderboard</button><button type="button" class="ll-tab" role="tab" data-view="chart" aria-selected="false">Score vs cost</button></div>
      </div>
      <div class="ll-bench" id="ll-benchbox" aria-live="polite"></div>
      <div class="gr-statusbar"><p class="gr-count" id="ll-count" role="status" aria-live="polite">{n} models</p>
        <label class="gr-toggle"><input type="checkbox" id="ll-untested" checked> Only models with a result</label>
        <button type="button" class="gr-link" data-clear hidden>Clear all filters</button></div>
      <ul class="gr-chips" aria-label="Active filters" hidden></ul>
      <div id="ll-panel-table"><div class="ll-tablewrap"><table class="ll-table"><thead><tr>
        <th scope="col">#</th>
        <th scope="col"><button type="button" class="ll-th" data-sort="name">Model</button></th>
        <th scope="col" class="num"><button type="button" class="ll-th" data-sort="score" aria-sort="descending"><span id="ll-score-th">Score</span></button></th>
        <th scope="col" class="num"><button type="button" class="ll-th" data-sort="blend">Price per 1M tokens</button></th>
        <th scope="col" class="num ll-hide-m"><button type="button" class="ll-th" data-sort="ctx">Context</button></th>
        <th scope="col" class="num ll-hide-m"><button type="button" class="ll-th" data-sort="released">Released</button></th>
      </tr></thead><tbody id="ll-tbody"><tr><td colspan="6">Turn on JavaScript to search and rank the models.</td></tr></tbody></table></div>
      <p class="ll-chartnote">Price is the blended list price per million tokens, weighted 3 input to 1 output. It comes from the developer's own price list; for open-weight models, and where no developer price list could be read, it is the price a named host lists on OpenRouter (shown as a secondary source in the details). Select a row for specifications and every benchmark result with its source.</p></div>
      <div id="ll-panel-chart" hidden><div class="ll-chartcard">
        <div class="ll-charthead"><h3 id="ll-chart-title">Score versus cost</h3>
          <label class="gr-sort"><span>Cost measure</span><select id="ll-axis"><option value="blend">Blended price per 1M tokens</option><option value="in">Input price per 1M tokens</option><option value="out">Output price per 1M tokens</option><option value="task">Cost per task (where published)</option></select></label></div>
        <ul class="ll-legend"><li><svg width="12" height="12" aria-hidden="true"><circle cx="6" cy="6" r="5" fill="#0B6FA4"/></svg>Proprietary API</li><li><svg width="12" height="12" aria-hidden="true"><rect x="2" y="2" width="8" height="8" transform="rotate(45 6 6)" fill="#C2571A"/></svg>Open weights</li><li><svg width="22" height="12" aria-hidden="true"><path d="M1 10H11V3H21" fill="none" stroke="#0B2A5A" stroke-width="2"/></svg>Pareto frontier</li><li>Faded points are beaten by a cheaper model</li></ul>
        <div class="ll-chart" id="ll-chart"></div></div>
        <div class="ll-front" id="ll-front"></div></div>
      <div class="gr-empty" id="ll-empty" hidden><h3>No models match these filters.</h3><p>Try removing a filter or searching for a broader term.</p><button type="button" class="btn btn-ghost" data-clear>Clear all filters</button></div>
    </div>
  </div>
</div></section>

<section class="section" id="method" style="scroll-margin-top:84px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Methodology</p><h2 class="h-lg">How this database is built and checked.</h2></div>
  <p>Data as of {asof}. {n_scores} benchmark results and {sum(1 for m in M if m.get("pin") is not None)} list prices, each linked to the page it came from.</p></div>
  <div class="ll-steps">{stepcards}</div>
  <div class="ll-gloss"><h3>The benchmarks</h3><div class="ll-tablewrap"><table class="ll-table"><thead><tr><th>Benchmark</th><th>What it measures</th><th>Source</th></tr></thead><tbody>{gloss}</tbody></table></div></div>
  <div class="card gr-disclaimer" role="note" aria-label="Disclaimer" style="margin-top:28px">
    <h3>Read the numbers with care</h3>
    <p>{esc(D["disclaimer"])}</p>
    <p>Spotted an error or a model we missed? <a href="contact.html">Let us know</a> and we will review it.</p>
  </div>
</div></section>

<section class="section dark" id="next" style="scroll-margin-top:84px"><div class="container feature-split gr-cta">
  <div class="stack-lg"><p class="eyebrow">Work with us</p><h2 class="h-lg">Choose models on your own work, not on leaderboards alone.</h2>
  <p class="lead">Benchmarks narrow the field. The decision comes from testing two or three candidates on your own documents, processes and data, with cost, privacy and reliability in the scorecard. Chmltech helps Canadian businesses run that evaluation and build the agents that follow.</p>
  <div class="btn-row"><a class="btn" href="book.html">Book a Strategy Call</a><a class="btn btn-ghost-dark" href="ai-operating-system.html">AI Operating System</a></div></div>
  <div class="card card-dark gr-cta-card"><h3 style="font-size:20px">Where we can help</h3><ul class="list-check">
    <li>Short-list models for a use case and test them on your tasks</li>
    <li>Estimate running cost per task and per month</li>
    <li>Choose between hosted APIs and open-weight models you run yourself</li>
    <li>Design, build and govern AI agents for operations</li></ul></div>
</div></section>
<script type="application/json" id="llm-data">{json.dumps(D, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")}</script>'''

    ld = {"@context": "https://schema.org", "@type": "Dataset", "name": "Chmltech LLM leaderboard", "description": "Specifications, list prices and independent benchmark results for current large language models, with sources.",
          "dateModified": D["as_of"], "creator": {"@type": "Organization", "name": "Chmltech Ltd."}, "url": f"{SITE}/{FNAME}"}
    body += f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    desc = (f"Compare {n} current large language models on independent benchmarks and price. Find the best model for coding, research, "
            "browser and business agents, and see the score-versus-cost Pareto frontier. Every number links to its source.")
    head, foot = shell()
    head = meta(head, "LLM Leaderboard: Compare AI Models by Score and Cost", desc)
    open(os.path.join(ROOT, FNAME), "w", encoding="utf-8").write(head + '<main id="main">\n' + body + "\n</main>" + foot)
    print(f"{FNAME}: {n} models, {len(B)} benchmarks, {n_scores} results")


if __name__ == "__main__":
    build()
