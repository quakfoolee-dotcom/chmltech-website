"""Links to the Chmltech WMS demo showcase page (wms-demo.html), V5.73.

One source for the three placements, used by the generators and by apply() for the
rendered pages:
  * Solutions (build_v3.py): a section before "All solutions".
  * Distribution & Warehousing (industry_pages.py, when the industry JSON has "wms_demo": true):
    a section after the interactive demo.
  * Warehouse series Part 7 (content/articles/wh7_articles.py): a box before "Key points".
Styles: the "V5.73 WMS demo links" block in assets/css/styles.css.

apply() is idempotent (it looks for data-wms-demo):  python3 content/gen/wms_demo_links.py
"""
import os, sys

MARK = 'data-wms-demo="1"'
SHOT = "assets/media/wms-demo/chmltech-wms-overview.webp"


def section(prefix="", eyebrow="Free interactive demo", title="See a warehouse management system at work.",
            text="Receive a purchase order, pick and ship a sales order, and watch stock and locations update in Chmltech WMS. "
                 "It runs in your browser with fictional data and no sign-up."):
    return (f'<section class="section wms-demo-strip" {MARK}><div class="container feature-split">'
            f'<div class="stack-lg"><p class="eyebrow">{eyebrow}</p><h2 class="h-lg">{title}</h2>'
            f'<p class="muted" style="font-size:17px">{text}</p>'
            f'<div class="btn-row"><a class="btn" href="{prefix}wms-demo.html">Explore the WMS demo</a>'
            f'<a class="btn btn-ghost" href="{prefix}WMS_demo/">Launch it now</a></div></div>'
            f'<figure class="wms-demo-shot"><a href="{prefix}wms-demo.html" tabindex="-1" aria-hidden="true">'
            f'<img src="{prefix}{SHOT}" width="1440" height="900" loading="lazy" alt=""></a></figure>'
            f'</div></section>\n')


SOLUTIONS = section()
INDUSTRY = section(eyebrow="Try it yourself", title="Try a working WMS in your browser.",
                   text="Not sure what a warehouse management system would change on your floor? Receive, pick, pack and ship "
                        "sample orders in Chmltech WMS, with fictional data that stays in your browser.")
ARTICLE = (f'<aside class="wms-cta" {MARK}><div><p class="wms-cta-eyebrow">Try it yourself</p>'
           '<p class="wms-cta-title">See what a WMS knows and directs</p>'
           '<p>Receive a carton, pick and ship an order, and watch stock and locations update in the free Chmltech WMS demo. '
           'No sign-up; the sample data stays in your browser.</p></div>'
           '<a class="btn" href="../wms-demo.html">Explore the WMS demo</a></aside>\n')

SOL_ANCHOR = '<section class="section sand" id="all-solutions"'
ART_ANCHOR = "<h2>Key points</h2>"
IND_EYEBROW = '<p class="eyebrow">Interactive demo</p>'


def add_to_solutions(s):
    if MARK in s: return s
    assert SOL_ANCHOR in s, "Solutions anchor missing"
    return s.replace(SOL_ANCHOR, SOLUTIONS + SOL_ANCHOR, 1)


def add_to_industry(s):
    """Insert after the industry page's interactive demo section."""
    if MARK in s: return s
    i = s.find(IND_EYEBROW); assert i >= 0, "Industry anchor missing"
    j = s.find("</div></section>", i) + len("</div></section>")
    return s[:j] + "\n" + INDUSTRY.rstrip("\n") + s[j:]


BLOCK = __import__("re").compile(r'\n?<section class="section wms-demo-strip" data-wms-demo="1">.*?</div></section>\n?', __import__("re").S)


def apply(root):
    """Insert the current blocks, replacing any earlier version of them."""
    changed = []
    for rel, fn in (("solutions.html", add_to_solutions), ("distribution-and-warehousing.html", add_to_industry)):
        p = os.path.join(root, rel); s = open(p, encoding="utf-8").read(); t = fn(BLOCK.sub("\n", s, count=1) if MARK in s else s)
        if t != s: open(p, "w", encoding="utf-8").write(t); changed.append(rel)
    return changed


if __name__ == "__main__":
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    print("WMS demo links added to:", ", ".join(apply(root)) or "nothing (already in place)")
