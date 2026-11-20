"""Build digital-assessment.html (Digital Needs Assessment + Software Finder).

Draft V13 to V2 (2026-11-19). Replaces the ERP Matrix Draft V1 page (erp-matrix.html). The ERP workflow
matrix is kept as the "ERP, MRP and WMS" category of the Software Finder.
Data: content/assess/assess_data.json (assessment + starter software categories) and
      content/erp/erp_data.json (ERP/MRP/WMS vendors and workflow capability scores).
Launched 2026-11-20 (V23): indexable; Digital Assessment is in the site menu on every page.

Run from the repo root:  python3 content/gen/assessment_page.py
"""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
A = json.loads((ROOT / 'content/assess/assess_data.json').read_text())
SRC = (ROOT / 'llm-leaderboard.html').read_text()
OUT = ROOT / 'digital-assessment.html'

header = re.search(r'<a class="skip".*?</header>', SRC, re.S).group(0).replace(' aria-current="page"', '')
if '<a href="digital-assessment.html">Digital Assessment</a>' in header:   # site menu already carries the link: mark it current
    header = header.replace('<a href="digital-assessment.html">Digital Assessment</a>', '<a href="digital-assessment.html" aria-current="page">Digital Assessment</a>')
else:
    header = header.replace('<a href="llm-leaderboard.html">AI Models</a>',
                            '<a href="llm-leaderboard.html">AI Models</a>\n      <a href="digital-assessment.html" aria-current="page">Digital Assessment</a>')
footer = re.search(r'<footer class="site-footer">.*?</footer>', SRC, re.S).group(0)
clarity = re.search(r'<script>\(function\(c,l,a,r,i,t,y\).*?</script>', SRC, re.S).group(0)
mainjs = re.search(r'<script src="assets/js/main\.js[^"]*" defer></script>', SRC).group(0)

def js_json(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")

n_ind, n_prob, n_cat = len(A['industries']), len(A['problems']), len(A['categories'])
n_prod = len(A['products']) + len(A['erp']['vendors']) + len({v['id'] for v in A['wms']['vendors']} - {v['id'] for v in A['erp']['vendors']})
RT = A['rt10']; n_rt_fix = RT['applied']; n_rt_rm = RT['removed_dir'] + RT['removed_ai']; n_rt_chk = RT['checked_dir'] + RT['checked_ai']
n_dir = len(A['dir']); n_dirca = sum(1 for e in A['dir'] if e['ca']); n_ai = len(A['ai_tools']); n_aic = len(A['ai_cats'])
n_ver = sum(p.get('v', 0) for p in A['products']) + sum(v.get('v', 0) for v in A['erp']['vendors'])
LOG = json.loads((ROOT / 'content/assess/redteam_v7_log.json').read_text())
n_fix = len(LOG)
n_unv = sum(len(p.get('unv', [])) for p in A['products'] + A['erp']['vendors'])
n_wf = len(A['erp']['workflows'])
n_smes = sum(i['smes'] for i in A['industries'])
as_of = 'November 19, 2026'
title = 'Free Digital Needs Assessment for Canadian SMEs | Chmltech'
descr = ('Assess your digital maturity in 8 minutes. Get a prioritized digital roadmap, a quick win '
         'and software options that fit Canadian small and medium-sized businesses.')
ind_chips = '<button type="button" class="chip" data-ind="" aria-pressed="true">All industries</button>' + ''.join(
    f'<button type="button" class="chip" data-ind="{i["id"]}" aria-pressed="false">{html.escape(i["name"])}</button>' for i in A['industries'])

page = f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title}</title>
<meta name="description" content="{descr}">
<link rel="canonical" href="https://www.chmltech.com/digital-assessment">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Chmltech Ltd.">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{descr}">
<meta property="og:image" content="https://www.chmltech.com/assets/img/chmltech-mark.png">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="assets/img/favicon-64.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Space+Grotesk:wght@500;600;700&amp;display=swap">
<link rel="stylesheet" href="assets/css/styles.css">
<link rel="stylesheet" href="assets/css/course-finder.css">
<link rel="stylesheet" href="assets/css/erp.css">
<link rel="stylesheet" href="assets/css/assess.css">
{clarity}
</head>
<body>
{header}
<main id="main">
<section class="page-hero dark course-hero"><div class="container"><div class="stack-lg">
  <p class="crumbs"><a href="index.html">Home</a> / Digital Assessment</p>
  <p class="eyebrow">Digital needs assessment</p>
  <h1 class="h-xl" style="font-size:clamp(34px,4.4vw,56px)">Free digital needs assessment for Canadian SMEs</h1>
  <p class="hero-slogan">Find where technology pays off first, and which software fits.</p>
  <p class="lead">Answer a few questions about your business. Get your top three technology priorities, one quick win, and software that suits Canadian firms your size.</p>
  <div class="stat-row"><div><strong>{n_prod}</strong><span>products compared</span></div><div><strong>{n_dir}</strong><span>vendors listed</span></div><div><strong>5 min</strong><span>free, no sign-up</span></div></div>
  <div class="btn-row as-hero-cta"><a class="btn" href="#assessment" data-as="start">Start the free assessment</a><a class="as-textlink" href="#finder">or browse software →</a></div>
</div></div></section>


<section class="section finder-section" id="assessment" style="scroll-margin-top:84px;padding-top:72px"><div class="container">
  <div class="panel finder stack" id="shortlist">
    <div class="finder-intro" id="as-intro">
      <div class="stack"><p class="eyebrow">How it works</p><h2 class="h-lg">Five quick steps to your roadmap.</h2>
      <ol class="as-stepline"><li>Your business</li><li>Priorities</li><li>Challenges</li><li>Digital maturity</li><li>Budget</li></ol>
      <p class="muted">Your roadmap appears straight away. No sign-up.</p></div>
      <div class="btn-row"><button type="button" class="btn" data-as="start">Start</button></div>
    </div>
    <div class="finder-quiz" id="as-quiz" hidden>
      <ol class="as-steps" id="as-steps"></ol>
      <div class="finder-progress"><div class="finder-bar"><span id="as-bar"></span></div></div>
      <p class="as-qcount muted" id="as-qcount"></p>
      <fieldset class="finder-q" id="as-qbox"></fieldset>
      <div class="finder-nav"><button type="button" class="btn btn-ghost" id="as-back">← Back</button><button type="button" class="btn" id="as-next" disabled>Next →</button></div>
    </div>
    <div class="stack" id="as-result" hidden tabindex="-1" style="gap:28px">
      <div class="finder-intro"><div class="stack"><p class="eyebrow">Your digital roadmap</p><h2 class="h-lg">Where technology will pay off first</h2><p class="lead" id="as-res-lead"></p></div>
        <div class="btn-row"><button type="button" class="btn btn-ghost" data-as="print">Download PDF</button><button type="button" class="btn btn-ghost" data-as="restart">Start again</button></div></div>
      <div class="as-res-top">
        <div class="as-card as-radar"><h3>Digital maturity</h3><div id="as-radar"></div></div>
        <div class="as-card"><h3>Gaps by function</h3><p class="as-gapsum" id="as-gapsum"></p><details class="as-gapsd"><summary>Show the numbers</summary><table class="as-gaps" id="as-gaps"></table>
          <p class="muted" style="font-size:13.5px;margin-top:10px">Levels: Manual, Digitized, Connected, Optimized. The gap is how far today is from your two-year target.</p></details></div>
      </div>
      <div><h3 class="h-md" style="font-size:24px;margin-bottom:14px">Your top three technology priorities</h3><div class="as-prios" id="as-prios"></div></div>
      <div id="as-notes"></div>
      <div class="as-qw" id="as-qw"></div>
      <div><h3 class="h-md" style="font-size:24px;margin-bottom:14px" id="as-opts-h"></h3><div class="erp-results" id="as-opts"></div>
        <p class="muted" style="font-size:13.5px;margin-top:12px">Ranked by fit to your answers. Use them to plan demos. No vendor pays to be listed. <a href="#method">How we rank</a></p></div>
      <div id="as-more"></div>
      <div id="as-aitools"></div>
      <div class="erp-lead">
        <form class="panel form" data-endpoint="https://api.web3forms.com/submit" data-subject="Digital assessment report" data-success="Thank you. We have your results and will email your full report within one business day." novalidate>
          <h3 class="h-md" style="font-size:22px">Get the full report</h3>
          <p class="muted" style="font-size:14.5px">Action plan, demo questions, more vendors, AI tools and funding. We email it within one business day.</p>
          <input class="hp" type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">
          <input type="hidden" name="form" value="Digital assessment">
          <div class="row">
            <div class="field"><label for="as-name">Full name</label><input id="as-name" name="name" autocomplete="name" required></div>
            <div class="field"><label for="as-email">Work email</label><input id="as-email" name="email" type="email" autocomplete="email" required></div>
          </div>
          <div class="field"><label for="as-co">Company <span class="hint">(optional)</span></label><input id="as-co" name="company" autocomplete="organization"></div>
          <label class="check"><input type="checkbox" name="consent" value="yes" required> I agree that Chmltech Ltd. may email me my report and contact me about it. I can unsubscribe at any time.</label>
          <div id="as-f-report" hidden></div>
          <div><button class="btn" type="submit">Request my full report</button></div>
          <p class="form-status" role="status" tabindex="-1"></p>
        </form>
        <div class="erp-audit">
          <p class="eyebrow">Free 30-minute roadmap review</p>
          <h3 class="h-md" style="font-size:24px">Turn the roadmap into a plan</h3>
          <p>We walk through your results and turn the quick win into a project you can start.</p>
          <ul><li>Check the priorities against how your team works</li><li>Shortlist and demo questions</li><li>Hidden costs and funding</li></ul>
          <div class="btn-row"><a class="btn" href="book.html">Book my free 30-minute review</a></div>
        </div>
      </div>
    </div>
  </div>
</div></section>

<section class="section sand" id="finder" style="scroll-margin-top:84px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Software Finder</p><h2 class="h-lg">Software that fits Canadian SMEs.</h2></div>
  <p>Pick a category. Tap a product for details and our honest take.</p></div>
  <div class="as-ftool">
    <label class="as-sel">Category <select id="as-catsel"></select></label>
    <label class="as-sel">Industry <select id="as-indsel"></select></label>
    <label class="as-sel" id="as-wfwrap" hidden>Type of business <select id="as-wf"></select></label>
  </div>
  <p class="as-catdesc" id="as-catdesc"></p>
  <p class="erp-count" id="as-fcount" role="status" aria-live="polite"></p>
  <div id="as-fbody"></div>
</div></section>

<section class="section" id="vendors" style="scroll-margin-top:84px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Vendor Directory</p><h2 class="h-lg">{n_dir} vendors, {n_dirca} Canadian.</h2></div>
  <p>More options, including Canadian specialists and implementation partners. Not scored: check fit in a demo. Prices as published by vendors (usually US dollars), checked November 2026.</p></div>
  <div class="vd-tools">
    <input type="search" id="vd-q" placeholder="Search vendors (e.g. 3PL, Quebec)" aria-label="Search vendors">
    <select id="vd-g" aria-label="Category"></select>
    <select id="vd-ind" aria-label="Industry"></select>
    <select id="vd-size" aria-label="Company size"><option value="">Any size</option><option value="s">Small</option><option value="m">Mid-market</option><option value="l">Large</option></select>
    <label class="check vd-ca"><input type="checkbox" id="vd-ca"> 🍁 Canadian only</label>
  </div>
  <p class="erp-count" id="vd-count" role="status" aria-live="polite"></p>
  <div id="vd-body"></div>
  <div class="btn-row" style="justify-content:center;margin-top:16px"><button type="button" class="btn btn-ghost" id="vd-more">Show more</button></div>
</div></section>

<section class="section sand" id="ai-tools" style="scroll-margin-top:84px"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">AI Tools</p><h2 class="h-lg">AI tools by job.</h2></div>
  <p>Most have a free trial. For company-wide assistants, compare <button type="button" class="as-goto" data-goto="ai" style="display:inline">AI assistants</button>.</p></div>
  <div class="ai-bar">
    <label class="ai-sel"><span class="ai-lbl">Job</span><select id="ai-cats" aria-label="Choose a job"></select></label>
    <label class="ai-search"><span class="visually-hidden">Search AI tools</span><input type="search" id="ai-q" placeholder="Search, e.g. meeting notes" autocomplete="off"></label>
    <p class="ai-count" id="ai-count" role="status" aria-live="polite"></p>
  </div>
  <div id="ai-body"></div>
  <div class="ai-more-row"><button type="button" class="ai-more" id="ai-more">Show more</button></div>
  <p class="muted" style="font-size:13.5px;margin-top:14px">Prices checked November 2026, in US dollars unless marked. They change often; check the vendor's site. Set rules on what company data staff may put into AI tools.</p>
</div></section>

<section class="section" id="method"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Method</p><h2 class="h-lg">How we rank and stay independent.</h2></div></div>
  <div class="erp-method as-method3">
    <div class="card"><h3>How we rank</h3><p>Your problems point to software categories; your priorities and maturity gaps set the order. Products are ranked by fit to your answers, then sized to your team and budget.</p></div>
    <div class="card"><h3>Where the data comes from</h3><p>Vendor documentation and public sources. Scores are our analyst rating: confirm them in a demo. Prices were checked in November 2026 and are in US dollars unless marked.</p></div>
    <div class="card"><h3>Independence</h3><p>Chmltech does not resell software, takes no referral fees and accepts no paid placement. <a href="https://www.chmltech.com/contact?service=Vendor%20product%20submission&amp;topic=vendor">Vendors can submit product information</a>.</p></div>
  </div>
  <details class="as-guide as-fullmethod"><summary>Full method</summary>
    <dl>
      <dt>Your business</dt><dd>Industry, size and current tools filter the problems and software to what fits your type of business.</dd>
      <dt>Digital maturity</dt><dd>Five functions rated Manual, Digitized, Connected or Optimized, today and in two years. The gaps show where to invest.</dd>
      <dt>Roadmap and quick win</dt><dd>Categories are ranked Must, Should and Could. The quick win can go live in weeks within your budget. ERP and systems you already own are never quick wins.</dd>
      <dt>Right-sized</dt><dd>Smaller firms see lighter tools; larger firms see ERP or warehouse systems.</dd>
      <dt>Capability scores</dt><dd>Built in, set up without code, add-on, or not offered. Company facts are checked against a source linked in each profile.</dd>
      <dt>AI tools</dt><dd>For each job, six tools (five for automation) are compared on four Canadian essentials (free plan, Microsoft 365 or Google, French, data privacy) and four job features, from vendor information checked by an independent reviewer. Other AI tools are listed, not scored.</dd>
      <dt>Vendor directory</dt><dd>Listings widen a shortlist; they are not scored and never change a product's score.</dd>
    </dl>
  </details>
</div></section>

</main>
<dialog class="erp-dlg" id="erp-dlg" aria-labelledby="erp-dlg-title">
  <div class="erp-dlg-head"><div><h3 id="erp-dlg-title"></h3><p id="erp-dlg-sub"></p></div><button type="button" class="erp-dlg-close" data-close-dlg aria-label="Close">✕</button></div>
  <div class="erp-dlg-body" id="erp-dlg-body"></div>
</dialog>
{footer}
<script type="application/json" id="assess-data">{js_json(A)}</script>
{mainjs}
<script src="assets/js/assess.js" defer></script>
</body>
</html>
'''
OUT.write_text(page)
print('wrote', OUT, len(page), 'bytes')
