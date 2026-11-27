#!/usr/bin/env python3
"""Sitemap <lastmod> dates that follow real content changes (V5.80).

Before V5.80, seo_pass.py gave every page other than articles the date of its last git
commit. A sitewide edit (menu, footer, analytics, the V5.77 link clean-up) therefore moved
the date of every page at once, telling Google that ~390 pages had changed. Google answers
that by re-crawling pages it already has (62% of crawl requests were "Refresh" in
November 2026) instead of fetching the pages still waiting to be indexed.

Now the date moves only when the page's own content changes. fingerprint() hashes the page
with the shared parts taken out:
  - the <head> (titles, meta, canonical, JSON-LD, analytics, asset links)
  - <header>, <nav> and <footer> (the site menu and footer)
  - <script> blocks that are JSON-LD or the Clarity loader
  - the email link, whichever form it takes (V5.82)
  - asset version stamps (?v=...) and the ".html" ending of links, with index.html and ./
    treated alike (the V5.77 link clean-up)
content/gen/lastmod.json keeps {page: [fingerprint, date]}. seo_pass.py calls date_for():
same fingerprint keeps the stored date; a new or changed fingerprint gets today's date.

Articles (post/*.html) keep using their own dateModified, which the article generators set.

Seed or rebuild the store from git history (finds, for each page, the oldest commit since
which its content is unchanged):
    python3 content/gen/lastmod.py seed .
"""
import datetime, hashlib, json, os, re, subprocess, sys

STORE = os.path.join("content", "gen", "lastmod.json")

_STRIP = [
    re.compile(r"<head\b.*?</head>", re.S | re.I),
    re.compile(r"<header\b.*?</header>", re.S | re.I),
    re.compile(r"<nav\b.*?</nav>", re.S | re.I),
    re.compile(r"<footer\b.*?</footer>", re.S | re.I),
    re.compile(r'<script type="application/ld\+json"[^>]*>.*?</script>', re.S | re.I),
    re.compile(r"<script>\(function\(c,l,a,r,i,t,y\).*?</script>", re.S),
    re.compile(r"<!--.*?-->", re.S),
]
_VER = re.compile(r"\?v=[0-9A-Za-z._-]+")
# V5.82: the email link changed form sitewide (js-mail "[at]" link -> plain mailto); both count as the same
_MAIL = re.compile(r'<a (?:class="js-mail" href="[^"]*" data-u="[^"]*" data-d="[^"]*"[^>]*|href="mailto:[^"]*")>[^<]*</a>')
_HTML_LINK = re.compile(r'((?:href|src|action)=["\'][^"\'#?]*?)(?:index)?\.html(?=["\'#?])', re.I)
_DOT = re.compile(r'(=["\'])\./(?=["\'#?])')  # V5.77 wrote index.html as ./
_WS = re.compile(r"\s+")


def fingerprint(text):
    s = text
    for pat in _STRIP:
        s = pat.sub(" ", s)
    s = _VER.sub("", s)
    s = _MAIL.sub("<a>email</a>", s)
    s = _HTML_LINK.sub(r"\1", s)
    s = _DOT.sub(r"\1", s)
    s = _WS.sub(" ", s).strip()
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:16]


def load(root):
    p = os.path.join(root, STORE)
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save(root, store):
    p = os.path.join(root, STORE)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(store.items())), f, indent=0, separators=(",", ":"))
        f.write("\n")


def date_for(store, rel, text, today=None):
    """Return the lastmod date for a page and update the store in place."""
    today = today or datetime.date.today().isoformat()
    fp = fingerprint(text)
    old = store.get(rel)
    if old and old[0] == fp:
        return old[1]
    store[rel] = [fp, today]
    return today


def _git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True,
                          text=True, errors="replace").stdout


def seed(root, rels):
    """Rebuild the store from git history for the given pages."""
    store = {}
    for rel in rels:
        cur = open(os.path.join(root, rel), encoding="utf-8", errors="replace").read()
        fp = fingerprint(cur)
        date = None
        for line in _git(root, "log", "--follow", "--format=%H %cs", "--", rel).splitlines():
            sha, d = line.split()
            # path at that commit (handles renames via --follow)
            names = _git(root, "show", "--name-only", "--format=", sha, "--", rel).split()
            blob = _git(root, "show", f"{sha}:{names[0] if names else rel}")
            if not blob or fingerprint(blob) != fp:
                break
            date = d
        store[rel] = [fp, date or datetime.date.today().isoformat()]
    return store


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "seed":
        root = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else ".")
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        sys.argv = [sys.argv[0], root]
        import seo_pass
        rels = [r for r in seo_pass.pages() if not r.startswith(("post/", "WMS_demo/"))]
        st = seed(root, rels)
        save(root, st)
        print(f"lastmod.json: {len(st)} pages seeded from git history")
    else:
        print(__doc__)
