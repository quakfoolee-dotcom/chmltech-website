"""Submit changed sitemap URLs to IndexNow (V5.77). Run by .github/workflows/indexnow.yml."""
import json, os, re, subprocess, sys, urllib.request

SITE = "https://www.chmltech.com"
KEY = "c3bf155879376468e8bf014cf323cbef"

sitemap = set(re.findall(r"<loc>([^<]+)</loc>", open("sitemap.xml", encoding="utf-8").read()))

def url_for(rel):
    u = rel[:-5] if rel.endswith(".html") else rel
    return SITE + "/" if u == "index" else f"{SITE}/{u}"

before = os.environ.get("BEFORE", "")
if os.environ.get("ALL") == "true" or not before or set(before) == {"0"}:
    urls = sorted(sitemap)
else:
    out = subprocess.run(["git", "diff", "--name-only", before, "HEAD"], capture_output=True, text=True, check=True).stdout
    urls = sorted({url_for(f) for f in out.split() if f.endswith(".html")} & sitemap)

if not urls:
    print("No indexable pages changed."); sys.exit(0)

body = json.dumps({"host": "www.chmltech.com", "key": KEY,
                   "keyLocation": f"{SITE}/{KEY}.txt", "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print(f"IndexNow HTTP {r.status}: submitted {len(urls)} URLs")
    for u in urls[:20]: print(" ", u)
