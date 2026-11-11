"""Add one Insights article to the built site without a full rebuild (V4.27).

Usage:  python3 content/gen/add_article.py <slug> [--fonts DIR]

Reads content/articles/<slug>.json and:
  - writes post/<slug>.html (page shell taken from an existing article),
  - draws the cover and thumbnail in assets/media/covers/,
  - adds the card at the top of insights.html and raises the article counts,
  - adds the address to sitemap.xml.
It is safe to run twice: the second run rewrites the post and cover and leaves the counts alone.
The cover uses Space Grotesk. Pass --fonts with a folder holding SpaceGrotesk-SemiBold.ttf and
SpaceGrotesk-Medium.ttf; without it the cover falls back to Inter or DejaVu.
"""
import glob, html, json, os, re, sys
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SITE = "https://www.chmltech.com"
SHELL = "iso-9001-document-and-revision-control"      # an existing article used as the page shell
CAT_NAMES = {"process-improvement": "Process Improvement", "operational-efficiency": "Operational Efficiency",
             "artificial-intelligence": "Artificial Intelligence", "digital-technology": "Digital Technology",
             "marketing": "Sales & Marketing", "lean": "Lean", "chmltech-online-journal": "Chmltech Online Journal",
             "change-management": "Change Management", "iso": "ISO", "six-sigma": "Six Sigma", "process-engineering": "Process Engineering", "esg": "ESG",
             "strategy": "Strategy", "erp": "ERP", "project-management": "Project Management",
             "book-review": "Book Review", "agile": "Agile", "case-study": "Case Study"}
E = lambda s: html.escape(s, quote=True)


def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def nice_date(d):
    y, m, dd = map(int, d.split("-"))
    return f"{date(y, m, dd):%b} {dd}, {y}"


def series_label(a):
    """'FEED series · Part 1 of 3' for an article with a "series" field (name, part, of); empty otherwise."""
    sr = a.get("series")
    return f'{sr["name"]} · Part {sr["part"]} of {sr["of"]}' if sr else ""


CARD_SERIES = '<p class="series" style="margin:0;font-size:13px;font-weight:600;color:var(--green-dark)">'
HERO_SERIES = '<p class="series" style="margin:0;font-size:15px;font-weight:600;letter-spacing:.03em;color:var(--green)">'


def card(a, prefix=""):
    search = E(" ".join([a["title"], a["desc"], " ".join(a["tags"])]).lower())
    cats = "".join(f'<span class="tag">{E(CAT_NAMES[c])}</span>' for c in a["cats"])
    ser = CARD_SERIES + E(series_label(a)) + "</p>" if a.get("series") else ""
    return (f'<article class="article" data-cats="{" ".join(a["cats"])}" data-search="{search}"><div class="thumb">'
            f'<img src="{prefix}assets/media/covers/thumbs/{a["slug"]}.jpg" alt="" loading="lazy" decoding="async" width="600" height="338"></div>'
            f'<div class="body"><div class="cats">{cats}</div>{ser}<h3><a href="{prefix}post/{a["slug"]}.html">{E(a["title"])}</a></h3>'
            f'<p class="muted">{E(a["desc"])}</p><p class="meta">{nice_date(a["date"])} · {a["read"]}</p></div></article>')


def existing_card(slug, listing):
    m = re.search(r'<article class="article"(?:(?!</article>).)*?href="post/' + re.escape(slug) + r'\.html".*?</article>', listing, re.S)
    return m.group(0).replace('src="assets/', 'src="../assets/').replace('href="post/', 'href="../post/') if m else ""


def post_page(a, listing, total):
    s = rd(f"post/{SHELL}.html")
    old = json.load(open(os.path.join(ROOT, "content", "articles", SHELL + ".json"), encoding="utf-8"))
    head, rest = s.split('<article class="prose">', 1)
    _, tail = rest.split("</article>\n  <aside", 1)
    tail = "</article>\n  <aside" + tail
    for part in ("head", "tail"):
        t = head if part == "head" else tail
        t = t.replace(E(old["title"]), E(a["title"])).replace(old["title"], E(a["title"]))
        t = t.replace(E(old["desc"]), E(a["desc"])).replace(old["desc"], E(a["desc"]))
        t = t.replace(SHELL, a["slug"])
        if part == "head": head = t
        else: tail = t
    head = re.sub(r'<div class="tags">.*?</div>',
                  '<div class="tags">' + "".join(f'<a href="../insights.html#cat={c}">{E(CAT_NAMES[c])}</a>' for c in a["cats"]) + "</div>", head, count=1)
    if a.get("series"):                                    # series label between the category tags and the headline
        head = head.replace('</div>\n    <h1', '</div>\n    ' + HERO_SERIES + E(series_label(a)) + '</p>\n    <h1', 1)
        assert HERO_SERIES in head
    head = re.sub(r'<p class="post-meta">.*?</p>',
                  f'<p class="post-meta"><span>{E(a["author"])}</span><span>{nice_date(a["date"])}</span><span>{a["read"]}</span></p>', head, count=1)
    tail = re.sub(r'(<p class="eyebrow">Tags</p><div class="tags">).*?(</div>)',
                  lambda m: m.group(1) + "".join(f"<span>{E(t)}</span>" for t in a["tags"]) + m.group(2), tail, count=1)
    rel = "".join(existing_card(sl, listing) for sl in a.get("related", []))
    tail = re.sub(r'(<div class="grid grid-3">).*?(</div>\n</div></section>\n<script type="application/ld\+json">)',
                  lambda m: m.group(1) + rel + m.group(2), tail, count=1, flags=re.S)
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["title"], "datePublished": a["date"],
          "author": {"@type": "Person", "name": a["author"]}, "publisher": {"@type": "Organization", "name": "Chmltech Ltd."},
          "mainEntityOfPage": f"{SITE}/post/{a['slug']}", "description": a["desc"]}
    tail = re.sub(r'<script type="application/ld\+json">.*?</script>',
                  lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", tail, count=1, flags=re.S)
    tail = re.sub(r"All \d+ articles", f"All {total} articles", tail)
    wr(f"post/{a['slug']}.html", head + '<article class="prose">\n' + a["body"].rstrip("\n") + "\n  " + tail)


def bump(s, pat, n=1):
    return re.sub(pat, lambda m: m.group(1) + str(int(m.group(2)) + n) + m.group(3), s)


def listing_page(a):
    s = rd("insights.html")
    if f'href="post/{a["slug"]}.html"' in s:
        return s, int(re.search(r">All \((\d+)\)<", s).group(1)), False
    s = bump(s, r"(>All \()(\d+)(\)<)")
    for c in a["cats"]:
        s = bump(s, r'(data-cat="' + c + r'" aria-pressed="false">[^<(]*\()(\d+)(\)<)')
    s = bump(s, r'(content=")(\d+)( articles from Chmltech)')
    s = bump(s, r'(<p class="lead">)(\d+)( articles on)')
    s = bump(s, r'(placeholder="Search )(\d+)( articles")')
    s = bump(s, r'(data-count aria-live="polite">)(\d+)( articles<)')
    s = s.replace('<div class="grid grid-3" data-items>\n  ', '<div class="grid grid-3" data-items>\n  ' + card(a), 1)
    return s, int(re.search(r">All \((\d+)\)<", s).group(1)), True


def cover(a, fonts):
    from PIL import Image, ImageDraw, ImageFont
    def font(names, size):
        for n in names:
            for d in [fonts, "/usr/share/fonts/opentype/inter", "/usr/share/fonts/truetype/dejavu"]:
                if d and os.path.exists(os.path.join(d, n)): return ImageFont.truetype(os.path.join(d, n), size)
        return ImageFont.load_default(size)
    K = 2; W, H = 1200 * K, 675 * K
    im = Image.new("RGB", (W, H), (11, 42, 89)); d = ImageDraw.Draw(im, "RGBA")
    for gx in range(706, 1200, 34):                       # dot grid, brighter toward the ring centre
        for gy in range(28, 675, 34):
            r2 = ((gx - 995) ** 2 + (gy - 338) ** 2) ** 0.5
            al = max(0.0, 1 - r2 / 330)
            rad = (1.2 + 2.6 * al) * K
            d.ellipse([gx * K - rad, gy * K - rad, gx * K + rad, gy * K + rad], fill=(10, 111, 164, int(40 + 150 * al)))
    d.ellipse([(995 - 207) * K, (338 - 207) * K, (995 + 207) * K, (338 + 207) * K], outline=(141, 198, 63, 120), width=7 * K)
    d.rounded_rectangle([80 * K, 64 * K, 152 * K, 70 * K], radius=3 * K, fill=(141, 198, 63, 255))
    eye = font(["SpaceGrotesk-Medium.ttf", "Inter-Medium.otf", "DejaVuSans.ttf"], 22 * K)
    x = 80 * K
    for ch in a.get("cover_label", CAT_NAMES[a["cats"][0]]).upper():
        d.text((x, 198 * K), ch, font=eye, fill=(141, 198, 63, 255)); x += d.textlength(ch, font=eye) + 4 * K
    size = 62
    while True:                                            # shrink the title until it fits in five lines
        f = font(["SpaceGrotesk-SemiBold.ttf", "Inter-SemiBold.otf", "DejaVuSans-Bold.ttf"], size * K)
        lines, cur = [], ""
        for w in a["title"].split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= 640 * K: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
        if len(lines) <= 5 or size <= 40: break
        size -= 4
    y = 248 * K
    for ln in lines:
        d.text((80 * K, y), ln, font=f, fill=(255, 255, 255, 255)); y += int(size * 1.16) * K
    mark = Image.open(os.path.join(ROOT, "assets/img/chmltech-mark.png")).convert("RGBA").resize((46 * K, 46 * K), Image.LANCZOS)
    im.paste(mark, (80 * K, 578 * K), mark)
    d = ImageDraw.Draw(im, "RGBA")
    d.text((140 * K, 587 * K), "Chmltech Insights", font=font(["SpaceGrotesk-SemiBold.ttf", "Inter-SemiBold.otf", "DejaVuSans-Bold.ttf"], 23 * K), fill=(214, 224, 240, 255))
    os.makedirs(os.path.join(ROOT, "assets/media/covers/thumbs"), exist_ok=True)
    im.resize((1200, 675), Image.LANCZOS).save(os.path.join(ROOT, f"assets/media/covers/{a['slug']}.jpg"), quality=88, optimize=True)
    im.resize((640, 360), Image.LANCZOS).save(os.path.join(ROOT, f"assets/media/covers/thumbs/{a['slug']}.jpg"), quality=84, optimize=True)


def main():
    slug = sys.argv[1]
    fonts = sys.argv[sys.argv.index("--fonts") + 1] if "--fonts" in sys.argv else None
    a = json.load(open(os.path.join(ROOT, "content", "articles", slug + ".json"), encoding="utf-8"))
    listing, total, added = listing_page(a)
    post_page(a, rd("insights.html"), total)
    cover(a, fonts)
    if added:
        wr("insights.html", listing)
        for f in glob.glob(os.path.join(ROOT, "post", "*.html")):   # "All N articles" button on every article
            s = open(f, encoding="utf-8").read(); t = re.sub(r"All \d+ articles", f"All {total} articles", s)
            if t != s: open(f, "w", encoding="utf-8").write(t)
        sm = rd("sitemap.xml"); loc = f"  <url><loc>{SITE}/post/{slug}</loc></url>\n"
        if loc not in sm:
            i = sm.index(f"  <url><loc>{SITE}/post/")
            wr("sitemap.xml", sm[:i] + loc + sm[i:])
    print(f"{slug}: post written, cover drawn, listing {'updated' if added else 'unchanged'} ({total} articles)")


if __name__ == "__main__":
    main()
