"""Fetch each AI tool's official icon for the AI Tools Landscape page (ai-tools.html).

For every website domain in assets/data/ai-tools.json it tries, on that domain only:
  1. the largest <link rel="apple-touch-icon" | "icon"> declared on the homepage (same site or its own CDN subdomain),
  2. /apple-touch-icon.png,
  3. /favicon.ico.
The image is resized to 64x64 (transparent padding, aspect kept) and saved as
assets/img/ai-tools/logos/<domain>.webp. assets/img/ai-tools/logos/manifest.json lists the domains that have a logo;
the page generator (content/gen/ai_tools_page.py) uses it, and tools without a logo keep their monogram tile.

Logos are shown as supplied (never recoloured or redrawn), only to identify the product; the page carries a trademark note.
Never fetches from third-party icon services; refuses redirects to other hosts, non-https URLs, private or local IP
addresses, non-image responses and files over 2 MB. Hosts shared by many products (github.com, huggingface.co ...) are skipped. Existing files are kept unless --refresh is given.

Run (needs Pillow; done by .github/workflows/ai-logos.yml):
  python3 scripts/fetch_ai_logos.py [--refresh] [--limit N]
then: python3 content/gen/ai_tools_page.py && python3 content/gen/seo_pass.py .
"""
import io, json, os, re, sys, socket, ipaddress, urllib.request, urllib.parse, concurrent.futures as cf
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "assets", "data", "ai-tools.json")
OUT = os.path.join(ROOT, "assets", "img", "ai-tools", "logos")
UA = "Mozilla/5.0 (compatible; ChmltechLogoBot/1.0; +https://www.chmltech.com/ai-tools)"
SIZE = 64
MAX_BYTES = 2_000_000


def public_host(host):
    """True only if every address the host resolves to is a public (global) IP."""
    try:
        infos = socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
    except OSError:
        return False
    return bool(infos) and all(ipaddress.ip_address(i[4][0]).is_global for i in infos)


class SameSiteRedirect(urllib.request.HTTPRedirectHandler):
    """Follow redirects only to https URLs on the tool's own domain (or its subdomains) that resolve to public IPs."""
    def __init__(self, dom):
        super().__init__(); self.dom = dom

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        u = urllib.parse.urlparse(newurl)
        if u.scheme != "https" or not same_site(newurl, self.dom) or not public_host(u.hostname):
            raise urllib.error.HTTPError(newurl, code, "redirect off-site refused", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class Icons(HTMLParser):
    def __init__(self):
        super().__init__(); self.found = []

    def handle_starttag(self, tag, a):
        if tag != "link":
            return
        a = dict(a); rel = (a.get("rel") or "").lower(); href = a.get("href")
        if not href or not any(k in rel.split() for k in ("icon", "apple-touch-icon", "apple-touch-icon-precomposed")):
            return
        m = re.findall(r"(\d+)x(\d+)", a.get("sizes") or "")
        size = max((int(w) for w, _ in m), default=180 if "apple" in rel else 32)
        if (a.get("type") or "").endswith("svg") or href.lower().split("?")[0].endswith(".svg"):
            size = 0  # SVG needs a renderer; prefer bitmaps
        self.found.append((size, href))


def get(url, dom, image=False):
    u = urllib.parse.urlparse(url)
    if u.scheme != "https" or not same_site(url, dom) or not public_host(u.hostname):
        raise ValueError("refused: " + url)
    opener = urllib.request.build_opener(SameSiteRedirect(dom))
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "image/*" if image else "text/html"})
    with opener.open(req, timeout=15) as r:
        ctype = (r.headers.get("Content-Type") or "").lower()
        if image and not (ctype.startswith("image/") or "octet-stream" in ctype):
            raise ValueError("not an image: " + ctype)
        body = r.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError("too large")
        return r.geturl(), body


def same_site(url, dom):
    """The tool's own host, a subdomain of it, or (for www-less entries) its www. form. No sibling or parent domains."""
    h = (urllib.parse.urlparse(url).hostname or "").lower()
    return h == dom or h.endswith("." + dom) or h == "www." + dom


def to_webp(raw, path):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = 4096 * 4096
    im = Image.open(io.BytesIO(raw))
    if getattr(im, "n_frames", 1) > 1:
        im.seek(0)
    if im.format == "ICO":
        im = max((Image.open(io.BytesIO(raw)).ico.getimage(s) for s in im.ico.sizes()), key=lambda i: i.size[0])
    im = im.convert("RGBA")
    if im.size[0] < 16:
        raise ValueError("too small")
    im.thumbnail((SIZE, SIZE), Image.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    canvas.paste(im, ((SIZE - im.size[0]) // 2, (SIZE - im.size[1]) // 2), im)
    canvas.save(path, "WEBP", quality=88, method=6)


def fetch(dom, refresh):
    path = os.path.join(OUT, f"{dom}.webp")
    if os.path.exists(path) and not refresh:
        return dom, "kept"
    tried = []
    try:
        final, html = get(f"https://{dom}/", dom)
        p = Icons(); p.feed(html.decode("utf-8", "ignore"))
        for size, href in sorted(p.found, reverse=True):
            u = urllib.parse.urljoin(final, href)
            if size and same_site(u, dom):
                tried.append(u)
    except Exception:
        pass
    tried += [f"https://{dom}/apple-touch-icon.png", f"https://{dom}/favicon.ico"]
    for u in tried:
        try:
            _, raw = get(u, dom, image=True)
            to_webp(raw, path)
            return dom, "ok"
        except Exception:
            continue
    return dom, "none"


def main():
    refresh = "--refresh" in sys.argv
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    os.makedirs(OUT, exist_ok=True)
    # only domains that belong to one product's vendor (the data marks shared hosts such as github.com with logo=false)
    doms = sorted({t["dom"] for t in json.load(open(DATA, encoding="utf-8"))["tools"] if t.get("dom") and t.get("logo")})[:limit]
    res = {}
    with cf.ThreadPoolExecutor(12) as ex:
        for dom, st in ex.map(lambda d: fetch(d, refresh), doms):
            res[dom] = st
    have = sorted(d for d in doms if os.path.exists(os.path.join(OUT, f"{d}.webp")))
    json.dump(have, open(os.path.join(OUT, "manifest.json"), "w"), indent=0)
    miss = [d for d, s in res.items() if s == "none"]
    print(f"{len(have)} of {len(doms)} domains have a logo ({sum(s == 'ok' for s in res.values())} fetched now); {len(miss)} without")
    if miss:
        print("no logo:", ", ".join(miss))


if __name__ == "__main__":
    main()
