"""'About the book' box on book reviews (V4.89): cover, title, author, publisher, year, a link to the book page and a
credit line, plus schema.org Review/Book markup. Run by seo_pass.py after article_toc, so every build keeps it.

The box goes at the top of the article (after the mobile contents list, if any). Re-running replaces it, so edit
BOOKS here and rebuild. Covers live in assets/media/books/ (supplied by Quak Foo Lee; sources in the V4.89 changelog).
"""
import glob, html, json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SITE = "https://www.chmltech.com"
E = lambda s: html.escape(s, quote=True)

B = lambda **k: k
CLEAR = B(file="clear-thinking.jpg", title="Clear Thinking: Turning Ordinary Moments into Extraordinary Results", author="Shane Parrish",
          publisher="Portfolio / Penguin", year="2023", credit="Cover: Portfolio / Penguin",
          url="https://www.penguinrandomhouse.com/books/611709/clear-thinking-by-shane-parrish/9780593086117", link="Publisher's page")
ATOMIC = B(file="atomic-habits.jpg", title="Atomic Habits", author="James Clear", publisher="Avery / Penguin Random House", year="2018",
           credit="Cover: Penguin Random House", url="https://www.penguinrandomhouse.com/books/543993/atomic-habits-by-james-clear/", link="Publisher's page")
EMYTH = B(file="e-myth-revisited.jpg", title="The E-Myth Revisited", author="Michael E. Gerber", publisher="HarperBusiness", year="1995",
          credit="Cover: HarperBusiness, via Indigo", url="https://www.indigo.ca/products/the-e-myth-revisited", link="Book page (Indigo)")
ONE = B(file="the-one-thing.jpg", title="The ONE Thing", author="Gary Keller and Jay Papasan", publisher="Bard Press", year="2013",
        credit="Cover: Bard Press, via Indigo", url="https://www.indigo.ca/products/the-one-thing", link="Book page (Indigo)")
FAST = B(file="millionaire-fastlane.jpg", title="The Millionaire Fastlane", author="MJ DeMarco", publisher="Viperion Publishing", year="2011",
         credit="Cover: Viperion Publishing (10th anniversary edition)", url="https://viperionpublishing.com/products/tmf-book-1", link="Publisher's page")
MONEY = B(file="psychology-of-money.jpg", title="The Psychology of Money", author="Morgan Housel", publisher="Harriman House", year="2020",
          credit="Cover: Harriman House", url="https://harriman.house/books/the-psychology-of-money/", link="Publisher's page")
NVIDIA = B(file="nvidia-way.jpg", title="The Nvidia Way: Jensen Huang and the Making of a Tech Giant", author="Tae Kim", publisher="W. W. Norton",
           year="2024", credit="Cover: W. W. Norton", url="https://wwnorton.co.uk/books/9781324086710-the-nvidia-way", link="Publisher's page")
PREDICT = B(file="predictable-revenue.jpg", title="Predictable Revenue", author="Aaron Ross and Marylou Tyler", publisher="PebbleStorm Press",
            year="2011", credit="Cover: PebbleStorm Press, via Indigo", url="https://www.indigo.ca/products/predictable-revenue", link="Book page (Indigo)")
DEAL = B(file="art-of-the-deal.jpg", title="The Art of the Deal", author="Donald J. Trump with Tony Schwartz", publisher="Random House", year="1987",
         credit="Cover: Penguin Random House", url="https://penguinrandomhousehighereducation.com/book/?isbn=9780394555287", link="Publisher's page")
WAR = B(file="art-of-war.jpg", title="The Art of War", author="Sun Tzu (translated by John Minford)", publisher="Penguin Classics", year="",
        credit="Cover: Penguin Classics edition", url="https://www.penguinrandomhouse.com/books/668918/the-art-of-war-by-sun-tzu-edited-translated-and-with-an-introduction-by-john-minford/",
        link="Publisher's page")

BOOKS = {
    "clear-thinking-by-shane-parrish-book-review-lessons-and-how-to-apply-them": [CLEAR],
    "atomic-habits-by-james-clear-a-deep-dive-review-and-guide-to-habit-transformation": [ATOMIC],
    "the-e-myth-revisited-by-michael-e-gerber-a-comprehensive-book-review-for-small-business-owners": [EMYTH],
    "the-one-thing-by-gary-keller-and-jay-papasan-a-deep-dive-review-for-achieving-extraordinary-results": [ONE],
    "the-millionaire-fastlane-by-mj-demarco-a-bold-blueprint-for-rapid-wealth-creation": [FAST],
    "the-psychology-of-money-by-morgan-housel-a-thought-provoking-review-on-wealth-behavior-and-happin": [MONEY],
    "unlocking-success-with-the-nvidia-way-strategies-for-innovation-and-growth": [NVIDIA],
    "how-to-build-a-predictable-and-scalable-sales-model-lessons-from-predictable-revenue-by-aaron-ros": [PREDICT],
    "the-art-of-the-deal-vs-the-art-of-war-a-strategic-comparison-through-economics-philosophy-and-et": [DEAL, WAR],
}

BOX_RE = r'<div class="book-box".*?<!--/book-box-->\n?'
LD_RE = r'<script type="application/ld\+json" data-book="1">.*?</script>\n?'


def size(f):
    from PIL import Image
    w, h = Image.open(os.path.join(ROOT, "assets/media/books", f)).size
    return 120, round(h * 120 / w)


def box(books):
    rows = ""
    for b in books:
        w, h = size(b["file"])
        pub = E(b["publisher"]) + (f', {b["year"]}' if b["year"] else "")
        rows += (f'<div class="bb-row"><figure><img src="../assets/media/books/{b["file"]}" alt="Cover of {E(b["title"].split(":")[0])} by {E(b["author"])}" '
                 f'width="{w}" height="{h}" decoding="async"><figcaption>{E(b["credit"])}</figcaption></figure>'
                 f'<div class="bb-text"><p class="bb-title"><em>{E(b["title"])}</em></p><p>{E(b["author"])}</p><p class="bb-muted">{pub}</p>'
                 f'<p><a href="{E(b["url"])}" rel="noopener" target="_blank">{E(b["link"])}</a></p></div></div>')
    label = "About the books" if len(books) > 1 else "About the book"
    return f'<div class="book-box" data-book-box><p class="eyebrow">{label}</p>{rows}</div><!--/book-box-->\n'


def ld(slug, books):
    url = f"{SITE}/post/{slug}"
    items = [{"@type": "Review", "url": url, "author": {"@type": "Person", "name": "Quak Foo Lee"},
              "itemReviewed": {"@type": "Book", "name": b["title"], "author": {"@type": "Person", "name": b["author"]},
                               "publisher": {"@type": "Organization", "name": b["publisher"]},
                               **({"datePublished": b["year"]} if b["year"] else {}),
                               "image": f"{SITE}/assets/media/books/{b['file']}", "sameAs": b["url"]}} for b in books]
    data = {"@context": "https://schema.org", "@graph": items}
    return '<script type="application/ld+json" data-book="1">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"


def build(s, slug):
    s = re.sub(BOX_RE, "", s, flags=re.S)
    s = re.sub(LD_RE, "", s, flags=re.S)
    books = BOOKS.get(slug)
    if not books:
        return s
    m = re.search(r'<article class="prose">(\s*<details class="a-toc-m" data-toc.*?</details>\n?)?', s, re.S)
    s = s[:m.end()] + box(books) + s[m.end():]
    return s.replace("</head>", ld(slug, books) + "</head>", 1)


def run(root=ROOT):
    n = 0
    for p in sorted(glob.glob(os.path.join(root, "post", "*.html"))):
        slug = os.path.basename(p)[:-5]
        s = open(p, encoding="utf-8").read()
        if slug not in BOOKS and "book-box" not in s:
            continue
        t = build(s, slug)
        n += slug in BOOKS
        if t != s: open(p, "w", encoding="utf-8").write(t)
    return n


if __name__ == "__main__":
    print(run(), "book boxes")
