"""Article and journal cover images (V4.63): one motif per subject family, so readers recognise a subject at a glance.

Family = the article's first category that is not the journal category. Journal papers keep their subject's motif;
the eyebrow reads "Chmltech Online Journal" and the footer "Chmltech Online Journal · Vol. N, Issue M".
Fonts: content/gen/fonts (Space Grotesk, SIL Open Font License).
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

GEN = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(GEN, "..", ".."))
FONTS = os.path.join(GEN, "fonts")
K = 2
NAVY, GREEN, BLUE = (11, 42, 89), (141, 198, 63), (30, 140, 200)
JOURNAL_CAT = "chmltech-online-journal"


def _p(x, y): return (x * K, y * K)


def m_circuit(d):                     # Artificial intelligence
    for i, y in enumerate([70, 128, 186, 244, 302, 360, 418, 476, 534, 592]):
        c = GREEN if i % 3 == 0 else BLUE; a = 150 if i % 2 else 110
        x1 = 760 + (i * 37) % 120; x2 = x1 + 140 + (i * 53) % 90; dy = 29 if i % 2 else -29
        d.line([_p(x1, y), _p(x2, y), _p(x2 + 29, y + dy), _p(1200, y + dy)], fill=c + (a,), width=3 * K, joint="curve")
        d.ellipse([_p(x1 - 6, y - 6), _p(x1 + 6, y + 6)], outline=c + (210,), width=3 * K)


def m_process(d):                     # Process engineering, ESG
    c, g = BLUE + (170,), GREEN + (190,)
    d.rounded_rectangle([_p(800, 110), _p(870, 560)], radius=35 * K, outline=c, width=4 * K)
    for y in range(170, 520, 45): d.line([_p(808, y), _p(862, y)], fill=c, width=2 * K)
    d.rounded_rectangle([_p(960, 330), _p(1110, 420)], radius=45 * K, outline=c, width=4 * K)
    d.ellipse([_p(980, 150), _p(1060, 230)], outline=g, width=4 * K)
    d.line([_p(990, 200), _p(1005, 172), _p(1020, 205), _p(1035, 175), _p(1050, 200)], fill=g, width=3 * K)
    for seg in ([(870, 140), (1020, 140), (1020, 150)], [(870, 520), (930, 520), (930, 375), (960, 375)],
                [(1020, 230), (1020, 330)], [(1110, 375), (1200, 375)], [(835, 560), (835, 640)], [(740, 300), (800, 300)]):
        d.line([_p(*q) for q in seg], fill=g, width=3 * K)
    for (x, y, dx, dy) in ((1200, 375, 1, 0), (960, 375, 1, 0), (800, 300, 1, 0), (1020, 330, 0, 1)):
        d.polygon([_p(x, y), _p(x - 14 * dx - 7 * dy, y - 14 * dy - 7 * dx), _p(x - 14 * dx + 7 * dy, y - 14 * dy + 7 * dx)], fill=g)


def m_gauge(d):                       # Operational efficiency, process improvement, lean, six sigma
    cx, cy = 1010, 420
    for i, r in enumerate((230, 185, 140, 95)):
        d.arc([_p(cx - r, cy - r), _p(cx + r, cy + r)], 180, 360, fill=(BLUE if i % 2 else GREEN) + (70,), width=5 * K)
        end = 180 + (0.55 + 0.12 * i) * 180
        col = GREEN if i % 2 else BLUE
        d.arc([_p(cx - r, cy - r), _p(cx + r, cy + r)], 180, end, fill=col + (220,), width=5 * K)
        ex, ey = cx + r * math.cos(math.radians(end)), cy + r * math.sin(math.radians(end))
        d.ellipse([_p(ex - 8, ey - 8), _p(ex + 8, ey + 8)], outline=col + (255,), width=3 * K, fill=NAVY)
    for t in range(7):
        a = math.radians(180 + t * 30)
        d.line([_p(cx + 248 * math.cos(a), cy + 248 * math.sin(a)), _p(cx + 266 * math.cos(a), cy + 266 * math.sin(a))], fill=(214, 224, 240, 120), width=2 * K)


def m_target(d):                      # ISO, quality, change and project management
    for gx in range(706, 1200, 34):
        for gy in range(28, 675, 34):
            al = max(0.0, 1 - ((gx - 995) ** 2 + (gy - 338) ** 2) ** 0.5 / 330); rad = (1.2 + 2.6 * al) * K
            d.ellipse([gx * K - rad, gy * K - rad, gx * K + rad, gy * K + rad], fill=(10, 111, 164, int(40 + 150 * al)))
    d.ellipse([_p(788, 131), _p(1202, 545)], outline=GREEN + (120,), width=7 * K)
    d.line([_p(930, 345), _p(980, 395), _p(1070, 290)], fill=GREEN + (200,), width=8 * K, joint="curve")


def m_network(d):                     # Digital technology, ERP
    rnd = random.Random(7)
    nodes = [(760 + 95 * i + rnd.randint(-25, 25), 80 + 105 * j + rnd.randint(-25, 25)) for i in range(5) for j in range(6)]
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            if math.dist(a, b) < 150: d.line([_p(*a), _p(*b)], fill=BLUE + (90,), width=2 * K)
    for i, (x, y) in enumerate(nodes):
        r = 9 if i % 4 == 0 else 5
        d.ellipse([_p(x - r, y - r), _p(x + r, y + r)], fill=(GREEN if i % 4 == 0 else BLUE) + (230,))


def m_bars(d):                        # Strategy, sales and marketing, case studies, book reviews
    for i, h in enumerate((140, 200, 180, 270, 330, 420)):
        x = 790 + i * 62
        d.rounded_rectangle([_p(x, 560 - h), _p(x + 36, 560)], radius=6 * K, fill=(BLUE if i < 5 else GREEN) + (80 if i < 5 else 200,))
    pts = [(808 + i * 62, 540 - h) for i, h in enumerate((150, 210, 190, 290, 350, 450))]
    d.line([_p(*q) for q in pts], fill=GREEN + (220,), width=4 * K, joint="curve")
    for q in pts: d.ellipse([_p(q[0] - 7, q[1] - 7), _p(q[0] + 7, q[1] + 7)], fill=NAVY, outline=GREEN + (255,), width=3 * K)


FAMILIES = {
    "ai": (m_circuit, ["artificial-intelligence"]),
    "process": (m_process, ["process-engineering", "esg"]),
    "ops": (m_gauge, ["operational-efficiency", "process-improvement", "lean", "six-sigma"]),
    "quality": (m_target, ["iso", "change-management", "project-management"]),
    "digital": (m_network, ["digital-technology", "erp"]),
    "business": (m_bars, ["strategy", "marketing", "case-study", "book-review", "agile"]),
}
CAT_FAMILY = {c: f for f, (_, cats) in FAMILIES.items() for c in cats}


def family(cats):
    for c in cats:
        if c != JOURNAL_CAT and c in CAT_FAMILY: return CAT_FAMILY[c]
    return "business"


def cover(slug, title, cats, label, journal_ref=None):
    """Write assets/media/covers/<slug>.jpg (1200x675) and thumbs/<slug>.jpg (640x360)."""
    F = lambda n, s: ImageFont.truetype(os.path.join(FONTS, n), s * K)
    im = Image.new("RGB", (1200 * K, 675 * K), NAVY); d = ImageDraw.Draw(im, "RGBA")
    FAMILIES[family(cats)][0](d)
    d.rounded_rectangle([_p(80, 64), _p(152, 70)], radius=3 * K, fill=GREEN + (255,))
    x, eye = 80 * K, F("SpaceGrotesk-Medium.woff", 22)
    for ch in label.upper():
        d.text((x, 198 * K), ch, font=eye, fill=GREEN + (255,)); x += d.textlength(ch, font=eye) + 4 * K
    size = 62
    while True:                       # shrink until the title fits above the footer
        f = F("SpaceGrotesk-SemiBold.woff", size); lines, cur = [], ""
        for w in title.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= 640 * K: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
        if 248 + len(lines) * size * 1.16 <= 560 or size <= 36: break
        size -= 4
    y = 248 * K
    for ln in lines:
        d.text((80 * K, y), ln, font=f, fill=(255, 255, 255, 255)); y += int(size * 1.16) * K
    mark = Image.open(os.path.join(ROOT, "assets/img/chmltech-mark.png")).convert("RGBA").resize((46 * K, 46 * K), Image.LANCZOS)
    im.paste(mark, (80 * K, 578 * K), mark); d = ImageDraw.Draw(im, "RGBA")
    footer = f"Chmltech Online Journal · {journal_ref}" if journal_ref else "Chmltech Insights"
    d.text((140 * K, 587 * K), footer, font=F("SpaceGrotesk-SemiBold.woff", 23), fill=(214, 224, 240, 255))
    os.makedirs(os.path.join(ROOT, "assets/media/covers/thumbs"), exist_ok=True)
    im.resize((1200, 675), Image.LANCZOS).save(os.path.join(ROOT, f"assets/media/covers/{slug}.jpg"), quality=88, optimize=True)
    im.resize((640, 360), Image.LANCZOS).save(os.path.join(ROOT, f"assets/media/covers/thumbs/{slug}.jpg"), quality=84, optimize=True)
