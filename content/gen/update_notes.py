"""Add a dated "update" note at the top of older articles whose subject has moved on (V4.66; the V4.71 GA4 note was dropped in V4.73 when the article was rewritten).

Usage:  python3 content/gen/update_notes.py

Each note sits as the first block of the article text and carries data-note="<id>", so running the script
again replaces the note instead of adding a second one. Edit NOTES to add, change or remove a note
(a note with text None is removed).
"""
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
STYLE = 'style="font-size:16.5px"'

NOTES = {
    "everything-you-need-to-know-about-iso-9001-2015-quality-management-system": (
        "iso2026",
        '<strong>Updated November 2026.</strong> ISO published ISO 9001:2026 on 16 September 2026, replacing the 2015 edition '
        'described below. Certified organizations have until 30 September 2029 to transition. Read '
        '<a href="iso-9001-2026-what-changed-from-2015.html">what changed from 2015</a> and the '
        '<a href="iso-9001-2026-transition-plan.html">step-by-step transition plan</a>.'),
    "tariffs-and-how-they-affect-economies-a-2025-perspective": (
        "dated2025",
        '<strong>Written in 2025.</strong> The general explanation of tariffs below still holds, but the trade measures and '
        'figures are those of early 2025. For what Canadian businesses can do now, see '
        '<a href="canada-budget-2026-what-manufacturers-and-process-plants-should-know.html">Budget 2026: what manufacturers and process plants should know</a>.'),
    "navigating-the-global-economy-in-2025-why-operational-efficiency-matters-more-than-ever": (
        "dated2025",
        '<strong>Written in 2025.</strong> The operating advice below still applies; the economic outlook is that of early 2025. '
        'For the 2026 tax measures that reward productivity investment, see '
        '<a href="canada-budget-2026-what-manufacturers-and-process-plants-should-know.html">Budget 2026: what manufacturers and process plants should know</a>.'),
    "change-management-toolkit-the-top-10-models-and-how-to-choose-the-right-one-for-your-organization": (
        "v473",
        '<strong>Updated November 2026.</strong> Added a comparison table of the ten models and a section on '
        '<a href="#ai-and-data">change in AI and data projects</a>, which replaces our separate article on change models for AI and data leaders.'),
    "building-effective-quality-management-systems": (
        "v473",
        '<strong>Updated November 2026.</strong> Added links to our ISO 9001 series, including '
        '<a href="iso-9001-2026-what-changed-from-2015.html">what changed in ISO 9001:2026</a>.'),
}


def main():
    only = set(sys.argv[1:])
    for slug, (nid, text) in NOTES.items():
        if only and slug not in only: continue
        p = os.path.join(ROOT, "post", slug + ".html")
        s = open(p, encoding="utf-8").read()
        s = re.sub(r'\s*<blockquote data-note="[^"]*".*?</blockquote>', "", s, count=1, flags=re.S)
        if text:
            s = s.replace('<article class="prose">', f'<article class="prose">\n<blockquote data-note="{nid}" {STYLE}>{text}</blockquote>', 1)
        open(p, "w", encoding="utf-8").write(s)
        print(slug, "note", nid if text else "removed")


if __name__ == "__main__":
    main()
