"""Funding Match page builder (V5.58): adds the guided funding match to funding.html.

Patches funding.html built by content/gen/grants_page.py (or the committed copy) in place: hero CTA, #match wizard
section, rules JSON (#fm-rules), assets, and refreshes the directory cards, filter counts and #grants-data from
content/grants.json. Run after any change to content/grants.json or content/funding/*.json:
    python3 content/funding/enrich_v1.py && python3 content/funding/funding_match_page.py && python3 content/gen/seo_pass.py .
The patch is applied to a clean page: pass --from-git to start from the last committed funding.html without the wizard
is not needed; the script strips an earlier Funding Match patch itself.
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
FP = os.path.join(ROOT, "funding.html")
RULES = os.path.join(HERE, "rules_v1.json")

HERO_OLD = re.compile(r'(?:<p class="hero-slogan">Find the grants[^<]*</p>\s*)?<p class="lead">.*?<div class="btn-row[^"]*">.*?</div>', re.S)


def strip(s):
    """Remove an earlier Funding Match patch so the script can run any number of times."""
    s = s.replace('<section class="section sand gr-section" id="finder"', '<section class="section gr-section" id="finder"')
    s = s.replace('<section class="section" id="before"', '<section class="section sand" id="before"')
    s = re.sub(r'\n<section class="section finder-section" id="match".*?</div></section>\n(?=\n<section class="section gr-section" id="finder")', '', s, flags=re.S)
    s = re.sub(r'<script type="application/json" id="fm-rules">.*?</script>\n', '', s, flags=re.S)
    s = re.sub(r'<link rel="stylesheet" href="assets/css/(?:course-finder|erp|assess|funding-match)\.css[^"]*">\n', '', s)
    s = re.sub(r'\n<script src="assets/js/funding-match\.js[^"]*" defer></script>', '', s)
    s = re.sub(r'\n<script src="https://challenges\.cloudflare\.com/turnstile/v0/api\.js" async defer></script>', '', s)
    return s

def hero(n):
    return (f'<p class="hero-slogan">Find the grants, tax credits and loans your business can apply for.</p>\n'
            f'  <p class="lead">Answer a few questions about your business and your project. Get your best-fit programs from {n} federal, provincial and territorial programs, '
            'a funding stack to explore, the near misses to plan for, and a readiness checklist.</p>\n'
            f'  <div class="stat-row"><div><strong>{n}</strong><span>programs checked</span></div><div><strong>14</strong><span>jurisdictions covered</span></div>'
            '<div><strong>3 min</strong><span>free, no sign-up</span></div><div><strong class="gr-stat-sm">November 2026</strong><span>last reviewed</span></div></div>\n'
            f'  <div class="btn-row as-hero-cta"><a class="btn" href="#match" data-fm="start">Start the free funding match</a><a class="as-textlink" href="#finder">or browse the program directory →</a></div>')

SECTION = '''
<section class="section finder-section" id="match" style="scroll-margin-top:84px;padding-top:72px"><div class="container">
  <div class="panel finder stack" id="fm">
    <div class="finder-intro" id="fm-intro">
      <div class="stack"><p class="eyebrow">How it works</p><h2 class="h-lg">Five quick steps to your funding shortlist.</h2>
      <ol class="as-stepline"><li>Your business</li><li>Your project</li><li>About you</li><li>Funding type</li><li>Readiness</li></ol>
      <p class="muted">Your matches appear straight away. No sign-up.</p></div>
      <div class="btn-row"><button type="button" class="btn" data-fm="start">Start</button></div>
    </div>
    <div class="finder-quiz" id="fm-quiz" hidden>
      <ol class="as-steps" id="fm-steps"></ol>
      <div class="finder-progress"><div class="finder-bar"><span id="fm-bar"></span></div></div>
      <p class="as-qcount muted" id="fm-qcount" aria-live="polite"></p>
      <fieldset class="finder-q" id="fm-qbox"></fieldset>
      <div class="finder-nav"><button type="button" class="btn btn-ghost" id="fm-back">← Back</button><button type="button" class="btn" id="fm-next" disabled>Next →</button></div>
    </div>
    <div class="stack" id="fm-result" hidden tabindex="-1" aria-labelledby="fm-res-h" style="gap:28px">
      <div class="finder-intro"><div class="stack"><p class="eyebrow">Your funding match</p><h2 class="h-lg" id="fm-res-h">Programs that fit your business</h2><p class="lead" id="fm-res-lead"></p><p class="fm-jump"><a href="#fm-report">Get this as a PDF in your inbox →</a></p></div>
        <div class="btn-row"><button type="button" class="btn btn-ghost" data-fm="restart">Start again</button></div></div>
      <div class="fm-tiles" id="fm-tiles"></div>
      <div id="fm-stack"></div>
      <div id="fm-groups" class="stack" style="gap:30px"></div>
      <div class="fm-two"><div id="fm-near"></div><div id="fm-watch"></div></div>
      <div id="fm-ready"></div>
      <div class="erp-lead" id="fm-report" style="scroll-margin-top:96px">
        <form class="panel form" data-endpoint="https://api.web3forms.com/submit" data-report-endpoint="https://chmltech-report.quakfoo-lee.workers.dev/" data-report-kind="funding" data-success-report="Thank you. Your Funding Match PDF is on its way to your inbox from reports@mail.chmltech.com. If you do not see it in a few minutes, check your junk folder." data-subject="Funding match report" data-success="Thank you. We have your results and will email your full report within one business day." novalidate>
          <h3 class="h-md" style="font-size:22px">Get the full report</h3>
          <p class="muted" style="font-size:14.5px">Your Funding Match as a PDF: best-fit programs with links, the funding stack, near misses and your readiness checklist. Sent to your inbox in a minute.</p>
          <input class="hp" type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">
          <input type="hidden" name="form" value="Funding match">
          <div class="row">
            <div class="field"><label for="fm-name">Full name</label><input id="fm-name" name="name" autocomplete="name" required></div>
            <div class="field"><label for="fm-email">Work email</label><input id="fm-email" name="email" type="email" autocomplete="email" required></div>
          </div>
          <div class="field"><label for="fm-co">Company <span class="hint">(optional)</span></label><input id="fm-co" name="company" autocomplete="organization"></div>
          <label class="check"><input type="checkbox" name="consent" value="yes" required> I agree that Chmltech Ltd. may email me my report and contact me about it. I can unsubscribe at any time.</label>
          <div><div class="cf-turnstile" data-sitekey="0x4AAAAAAGKoiNXbfnTG_CId" data-size="flexible" data-theme="light" style="margin:4px 0 12px"></div>
          <button class="btn" type="submit">Email me my report</button></div>
          <p class="form-status" role="status" tabindex="-1"></p>
        </form>
        <div class="erp-audit">
          <p class="eyebrow">Free 30-minute funding review</p>
          <h3 class="h-md" style="font-size:24px">Turn the matches into an application plan</h3>
          <p>We walk through your matches and shape the project so it fits the best program.</p>
          <ul><li>Check eligibility and eligible costs</li><li>Order and stack the programs</li><li>Scope, budget and timeline funders ask for</li></ul>
          <div class="btn-row"><a class="btn" href="book.html">Book my free 30-minute review</a></div>
        </div>
      </div>
      <p class="fm-note">Results are a starting point, not a decision on eligibility. Each program sets its own rules and decides every application; confirm the details on the official program page before you apply. Programs checked November 2026. Chmltech is not affiliated with any government program and takes no fee from funders.</p>
    </div>
  </div>
</div></section>
'''

def main():
    s = open(FP, encoding="utf-8").read()
    n = s.count('<article class="gr-card"')
    s = strip(s)
    s, k = HERO_OLD.subn(hero(n), s, count=1); assert k == 1
    s = s.replace('<section class="section gr-section" id="finder"', SECTION + '\n<section class="section gr-section" id="finder"', 1)
    # V5.61: alternate backgrounds like the Digital Assessment (wizard on paper, directory on sand, "Before you apply" on paper)
    s = s.replace('<section class="section gr-section" id="finder"', '<section class="section sand gr-section" id="finder"', 1)
    s = s.replace('<section class="section sand" id="before"', '<section class="section" id="before"', 1)
    s = s.replace('<p class="eyebrow">Program directory</p>', '<p class="eyebrow">Program directory</p>', 1)
    # refresh the directory data and cards from content/grants.json (Phase 1 status updates)
    import sys; sys.path.insert(0, os.path.join(ROOT, "content", "gen"))
    import grants_page as G
    recs = json.load(open(os.path.join(ROOT, "content", "grants.json"), encoding="utf-8"))
    recs = [r for r in recs if r.get("id") and r.get("name") and r.get("url")]; recs.sort(key=lambda r: r["name"].lower())
    for r in recs:
        s = re.sub(r'<article class="gr-card" id="p-' + re.escape(r["id"]) + r'".*?</article>', lambda m: G.card(r), s, count=1, flags=re.S)
    dj = json.dumps(recs, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    s = re.sub(r'(<script type="application/json" id="grants-data">).*?(</script>)', lambda m: m.group(1) + dj + m.group(2), s, count=1, flags=re.S)
    ct = {f: G.counts(recs, f) for f in ("jurisdiction", "funding_types", "applicant_types", "industries", "purposes", "status")}
    cj, ctt, ca, ci, cp, cs = (ct[f] for f in ("jurisdiction", "funding_types", "applicant_types", "industries", "purposes", "status"))
    filters = "".join([
        G.group("j", "Jurisdiction", G.JURISDICTIONS, cj, True,
                '<label class="gr-toggle"><input type="checkbox" id="gr-fed" checked> Include federal programs</label>'
                '<p class="gr-hint">When you pick a province or territory, federal programs available there are also shown.</p>'),
        G.group("t", "Funding type", G.present(G.FUNDING_TYPES, ctt), ctt, True),
        G.group("a", "Who can apply", G.present(G.APPLICANTS, ca), ca),
        G.group("i", "Industry", G.present(G.INDUSTRIES, ci), ci, False, '<p class="gr-hint">Programs open to all industries are always included.</p>'),
        G.group("p", "Purpose", G.present(G.PURPOSES, cp), cp),
        G.group("s", "Status", G.present(G.STATUSES, cs), cs, False,
                f'<label class="gr-toggle"><input type="checkbox" id="gr-closed"> Show closed programs ({cs.get(G.CLOSED, 0)})</label>'),
    ])
    shown = sum(1 for r in recs if r.get("status") != G.CLOSED)
    s, k = re.subn(r'(<div class="gr-filters-head">.*?</div>).*?(<button type="button" class="btn gr-apply" data-close>Show <span data-close-n>)\d+(</span>)',
                   lambda m: m.group(1) + "\n        " + filters + "\n        " + m.group(2) + str(shown) + m.group(3), s, count=1, flags=re.S)
    assert k == 1, "filter block not found"
    rules = json.load(open(RULES, encoding="utf-8"))
    rj = json.dumps(rules, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    s = s.replace('<script type="application/json" id="grants-data">', f'<script type="application/json" id="fm-rules">{rj}</script>\n<script type="application/json" id="grants-data">', 1)
    import hashlib
    def ver(path): return hashlib.md5(open(os.path.join(ROOT, path), "rb").read()).hexdigest()[:8]
    css = ''.join(f'<link rel="stylesheet" href="assets/css/{c}.css">\n' for c in ("course-finder", "erp", "assess", "funding-match"))
    s = s.replace('<link rel="stylesheet" href="assets/css/grants.css', css + '<link rel="stylesheet" href="assets/css/grants.css', 1)
    s = re.sub(r'(<script src="assets/js/grants\.js[^"]*" defer></script>)', r'\1\n<script src="assets/js/funding-match.js" defer></script>\n<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>', s, count=1)
    open(FP, "w", encoding="utf-8").write(s)
    print("funding.html patched:", n, "programs")

if __name__ == "__main__":
    main()
