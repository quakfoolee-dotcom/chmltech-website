"""Insights articles written for this site (no Wix original), stored as articles/<slug>.json (V4.20)."""
import glob, json, os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "articles")
OLD_ISO = "everything-you-need-to-know-about-iso-9001-2015-quality-management-system"
OLD_ISO_NOTE = ('<blockquote style="font-size:16.5px"><strong>Update, November 2026:</strong> ISO 9001:2015 has been replaced by '
                'ISO 9001:2026, published on 16 September 2026. Certified organizations have until 30 September 2029 to transition. '
                'See <a href="../post/iso-9001-2026-what-changed-from-2015.html">ISO 9001:2026: what changed from 2015</a> and '
                '<a href="../post/iso-9001-2026-transition-plan.html">your transition plan</a>.</blockquote>')


def load():
    A = [json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(SRC, "*.json"))]
    return sorted(A, key=lambda a: a.get("order", 0))


def add_posts(POSTS):
    have = {p["slug"] for p in POSTS}
    for a in load():
        if a["slug"] in have: continue
        POSTS.append(dict(slug=a["slug"], title=a["title"], date=a["date"], author=a["author"], read=a["read"], desc=a["desc"],
                          cover=None, body=a["body"], cats=list(a["cats"]), tags=a["tags"][:10]))
    for p in POSTS:   # point the 2015 article at the new edition
        if p["slug"] == OLD_ISO and "Update, November 2026" not in p["body"]:
            p["body"] = OLD_ISO_NOTE + p["body"]
