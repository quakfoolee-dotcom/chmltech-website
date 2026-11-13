"""Add a dated "update" note at the top of older articles whose subject has moved on (V4.66; GA4 note V4.71).

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
    "how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide": (
        "ga4",
        '<strong>Written in 2023 for Universal Analytics.</strong> Google stopped processing data in standard Universal Analytics '
        'properties on 1 July 2023 and removed access in July 2024; Google Analytics 4 (GA4) is now the only version. The ideas below '
        'still apply, but some names have changed: GA4 records everything as events, goals are now <em>key events</em> (called '
        'conversions until March 2024), and engagement rate is the main measure in place of bounce rate. For how to be found in '
        'search and AI answers, see <a href="the-key-differences-between-seo-and-geo-for-enhancing-your-online-presence.html">SEO vs GEO</a>.'),
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
