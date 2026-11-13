"""V4.82: replace the last old (Wix) cover photos with covers in the subject-family style (covers.py).

For every Insights card whose thumbnail is not in assets/media/covers/thumbs/, this script
  - draws assets/media/covers/<slug>.jpg and thumbs/<slug>.jpg,
  - points the card's thumbnail to it on every page that shows the card,
  - points the post's cover image, og:image, twitter:image and JSON-LD image to it.
Safe to run twice. Usage: python3 -I content/gen/v482_covers.py
"""
import glob, html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import covers, add_article as aa
R = covers.ROOT
CARD = r'<article class="article"(?:(?!</article>).)*?href="(?:\.\./)?post/{slug}\.html".*?</article>'


def main():
    listing = open(os.path.join(R, "insights.html"), encoding="utf-8").read()
    todo = []
    for cats, body in re.findall(r'<article class="article" data-cats="([^"]*)"[^>]*>(.*?)</article>', listing, re.S):
        if "covers/thumbs/" in body: continue
        slug = re.search(r'href="post/([^"]+)\.html"', body).group(1)
        title = html.unescape(re.sub("<[^>]+>", "", re.search(r"<h3[^>]*>(.*?)</h3>", body, re.S).group(1))).strip()
        label = re.search(r'<p class="cat-label">([^<]*)</p>', body)
        todo.append((slug, title, cats.split(), html.unescape(label.group(1)) if label else aa.CAT_NAMES[cats.split()[0]]))
    pages = glob.glob(os.path.join(R, "*.html")) + glob.glob(os.path.join(R, "post", "*.html"))
    for slug, title, cats, label in todo:
        covers.cover(slug, title, cats, label)
        for p in pages:
            s = open(p, encoding="utf-8").read()
            t = re.sub(CARD.format(slug=re.escape(slug)),
                       lambda m: re.sub(r'(<img src="(?:\.\./)?)assets/media/(?:thumbs/)?[^"]+"', r'\1assets/media/covers/thumbs/' + slug + '.jpg"', m.group(0), count=1),
                       s, flags=re.S)
            if p.endswith(os.path.join("post", slug + ".html")):
                t = re.sub(r'(<meta (?:property|name)="(?:og|twitter):image" content=")[^"]+"', r'\1https://www.chmltech.com/assets/media/covers/' + slug + '.jpg"', t)
                t = re.sub(r'("image": ")https://www\.chmltech\.com/assets/media/[^"]+"', r'\1https://www.chmltech.com/assets/media/covers/' + slug + '.jpg"', t)
                # the old photo banner goes: rewritten posts show no banner, and the new cover is the share image
                t = re.sub(r'<div class="container post-cover"><img fetchpriority="high" src="[^"]+" alt="[^"]*" width="\d+" height="\d+"></div>\n?', "", t)
            if t != s: open(p, "w", encoding="utf-8").write(t)
        print("cover", slug[:60], "|", label)
    print(len(todo), "covers drawn")


if __name__ == "__main__":
    main()
