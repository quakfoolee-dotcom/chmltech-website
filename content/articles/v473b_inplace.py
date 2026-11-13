"""V4.73 (second half): in-place upgrades to two older articles that have no JSON source.

1. post/change-management-toolkit-...   contents links repaired (the old Wix anchors went nowhere), a comparison table
                                       of the ten models, and a section on change in AI and data projects that absorbs
                                       the retired post 5-change-models-every-ai-data-leader-should-know
2. post/building-effective-quality-management-systems
                                       a section pointing to the ISO 9001 series, and a dated update note

Safe to run twice: each inserted block carries data-v473b="<id>" and is replaced, not duplicated.
Run before legacy_fixes.py (which rebuilds the "Read next" paragraph) and seo_pass.py.
"""
import os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
TOOLKIT = "change-management-toolkit-the-top-10-models-and-how-to-choose-the-right-one-for-your-organization"
QMS = "building-effective-quality-management-systems"


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table>\n<tr>{h}</tr>\n{b}\n</table>"


MODELS = [
    ("Lewin", "Organization", "Three stages: unfreeze, change, refreeze", "A clear, one-off change such as a new process", "Too simple for continuous change"),
    ("Kotter's 8 steps", "Organization", "Leadership-led sequence from urgency to anchoring", "Large transformations that need visible sponsorship", "Top-down; slow for small changes"),
    ("ADKAR", "Individual", "Awareness, desire, knowledge, ability, reinforcement", "System rollouts where people must change how they work", "Needs a wider plan around it"),
    ("Bridges' transition", "Individual", "Endings, the neutral zone, new beginnings", "Restructures and mergers with a strong emotional impact", "Not a project plan"),
    ("Prosci process", "Project", "Prepare, manage, sustain, using ADKAR for people", "Formal change management on defined projects", "Can feel heavy for a small business"),
    ("McKinsey 7-S", "Organization", "Aligns strategy, structure, systems, shared values, style, staff, skills", "Diagnosing why a strategy is not taking hold", "Diagnostic, not a step-by-step method"),
    ("Satir", "Team", "Performance dips during change, then rises if supported", "Preparing teams for a temporary productivity drop", "Little guidance on actions"),
    ("Kübler-Ross curve", "Individual", "Emotional stages from denial to acceptance", "Supporting people through loss, such as closures", "Stages are not linear; use with care"),
    ("Action research", "Team", "Repeated cycles of diagnose, act, evaluate with staff", "Problems where the people doing the work hold the answers", "Takes time and facilitation"),
    ("Agile change", "Team", "Small, frequent changes with feedback", "Digital and software change; continuous improvement", "Needs a stable direction to iterate toward"),
]

AI_SECTION = f"""<h2 id="ai-and-data">Change in AI and data projects</h2>
<p>AI tools and data projects fail more often from adoption than from technology. People worry about being replaced, do not trust outputs they cannot check, or simply carry on with the spreadsheet they know. The models above still apply; these five are the most useful for AI and data work, and two of them, the McKinsey Influence Model and Nudge theory, are not in the list of ten.</p>
{table(["Model", "Use it to", "What it looks like in an AI or data project"], [
    ("ADKAR", "Build each person's readiness", "Explain the business reason; show that the tool removes tedious work rather than jobs; train on real cases; recognise people who use it well"),
    ("Kotter's 8 steps", "Move from pilot to company-wide use", "A sponsor and a small guiding team, one or two quick wins with measured results, then process and policy changes that make the new way normal"),
    ("Lewin", "Make data-driven decisions a habit", "Unfreeze by showing where gut feel cost money; change with dashboards and new meeting routines; refreeze by building them into reviews"),
    ("McKinsey Influence Model", "Change behaviour through four levers", "Leaders who visibly use the data (role modelling); a clear story of why (understanding); skills training (capability); targets and reviews that expect it (reinforcement)"),
    ("Nudge theory", "Make the right choice the easy one", "Default reports in the meeting pack, a standing question of 'what does the data say?', and one-click access to the approved AI tool"),
])}
<p>Two practical points matter more than the choice of model. First, decide early which decisions an AI tool may make and which it only supports, and write that down; people adopt tools faster when the boundary is clear. Second, track adoption as well as accuracy: how many people use the tool each week, and for what. <a href="iso-iec-42001-alongside-iso-9001-adding-ai-governance.html">ISO/IEC 42001 alongside ISO 9001</a> shows how to put the controls into your management system.</p>
<p><em>The McKinsey Influence Model is described in McKinsey's work on the four building blocks of change. Nudge theory comes from Richard Thaler and Cass Sunstein's book <cite>Nudge</cite> (2008).</em></p>
"""

QMS_SECTION = """<h2>Taking it further: ISO 9001</h2>
<p>Many businesses build their quality management system around ISO 9001, which a certification body can audit and certify. The sixth edition, ISO 9001:2026, was published in September 2026. These articles go deeper into each part of the system described above:</p>
<ul>
<li><a href="iso-9001-for-small-and-mid-sized-businesses.html">ISO 9001 for small and mid-sized businesses</a>: getting certified without the paperwork burden</li>
<li><a href="iso-9001-2026-what-changed-from-2015.html">ISO 9001:2026: what changed from 2015</a> and the <a href="iso-9001-2026-transition-plan.html">transition plan</a></li>
<li><a href="iso-9001-document-and-revision-control.html">Document and revision control</a>, for the procedures and records in step 2</li>
<li><a href="iso-9001-risk-based-thinking-in-practice.html">Risk-based thinking in practice</a>, for quality planning</li>
<li><a href="iso-9001-internal-audits-that-find-real-problems.html">Internal audits that find real problems</a> and <a href="iso-9001-management-review-that-leadership-finds-useful.html">management reviews that leadership finds useful</a>, for step 5</li>
<li><a href="integrated-management-system-iso-9001-14001-45001.html">Integrating ISO 9001, 14001 and 45001</a>, if you also manage environment or safety</li>
</ul>
"""


def put(b, nid, html, before):
    """Remove any earlier copy of block nid, then insert html before the first match of regex `before`."""
    b = re.sub(r'<section data-v473b="' + nid + r'">.*?</section>\s*', "", b, flags=re.S)
    m = re.search(before, b)
    assert m, (nid, before)
    return b[:m.start()] + f'<section data-v473b="{nid}">\n{html}</section>\n' + b[m.start():]


def edit(slug, fn):
    p = os.path.join(ROOT, "post", slug + ".html")
    s = open(p, encoding="utf-8").read()
    m = re.search(r'(<article class="prose">)(.*?)(</article>)', s, re.S)
    b = fn(m.group(2))
    t = s[:m.start(2)] + b + s[m.end(2):]
    if t != s:
        open(p, "w", encoding="utf-8").write(t); print("updated", slug)
    else:
        print("unchanged", slug)


def toolkit(b):
    # 1. ids on the ten model headings, and the contents links pointed at them
    for i in range(1, 11):
        b = re.sub(r'<h2(?: id="model-\d+")?>' + str(i) + r'\. ', f'<h2 id="model-{i}">{i}. ', b, count=1)
    olds = re.findall(r'href="#viewer-[^"]+"', b)
    for i, o in enumerate(olds[:10], 1):
        b = b.replace(o, f'href="#model-{i}"', 1)
    # 2. one extra contents entry for the new section
    b = re.sub(r'<li><a href="#ai-and-data">[^<]*</a></li>', "", b)
    b = b.replace('Agile Change Management Model </a> </li></ol>',
                  'Agile Change Management Model </a> </li><li><a href="#ai-and-data">Change in AI and data projects</a></li></ol>', 1)
    # 3. comparison table before model 1, AI section before the conclusion
    cmp_html = ("<h2>The ten models at a glance</h2>\n<p>Use this table to shortlist one or two models, then read the detail below. "
                "Most real projects combine an organization-level model, such as Kotter, with an individual-level one, such as ADKAR.</p>\n"
                + table(["Model", "Focus", "Core idea", "Best for", "Watch for"], MODELS) + "\n")
    b = put(b, "compare", cmp_html, r'<h2 id="model-1">')
    b = put(b, "ai", AI_SECTION, r'<h2>Conclusion</h2>')
    return b


def qms(b):
    b = re.sub(r'<figcaption>[^<]*</figcaption>', "", b)        # captions left behind when the stock photos were removed
    return put(b, "iso", QMS_SECTION, r'<h2>Driving Operational Excellence')


if __name__ == "__main__":
    edit(TOOLKIT, toolkit)
    edit(QMS, qms)
