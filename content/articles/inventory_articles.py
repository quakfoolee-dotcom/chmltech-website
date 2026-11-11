"""Inventory control series (V4.30): four Insights articles on ABC analysis and safety stock.

Usage:  python3 content/articles/inventory_articles.py
Writes content/articles/<slug>.json for the four articles. Then run
content/gen/add_article.py <slug> for each one (see CHANGELOG V4.30).

All figures are computed here from the example data, so tables, charts and text stay in step
with the companion workbook in assets/downloads/.
"""
import html, json, math, os, re
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
E = lambda s: html.escape(str(s), quote=True)
S1, S2, S3, S4 = ("abc-inventory-analysis", "setting-safety-stock",
                  "abc-analysis-for-manufacturers", "safety-stock-for-manufacturers")
T1 = "ABC Inventory Analysis: What It Is, How to Do It, and a Worked Example"
T2 = "Setting Safety Stock Without Guessing: Three Methods and a Worked Example"
T3 = "ABC Analysis for Manufacturers: Why Dollar Value Is Not Enough"
T4 = "Safety Stock for Manufacturers: Raw Materials and Spare Parts"
P = {1: f'<a href="{S1}.html">Post&nbsp;1</a>', 2: f'<a href="{S2}.html">Post&nbsp;2</a>',
     3: f'<a href="{S3}.html">Post&nbsp;3</a>', 4: f'<a href="{S4}.html">Post&nbsp;4</a>'}
TPL = "../assets/downloads/Chmltech_Inventory_ABC_SafetyStock_Template.xlsx"
TPL_NAME = "Chmltech_Inventory_ABC_SafetyStock_Template.xlsx"


def tpl_box(line):
    """Download box for the template. The button opens the lead-capture form (assets/js/download.js);
    without JavaScript it is a plain download link."""
    return ('<link rel="stylesheet" href="../assets/css/download.css">'
            '<div class="j-dl-box"><div><strong>Free Excel template</strong>'
            f'<span>{line}</span></div><a class="btn" href="{TPL}" data-dl download>Download template</a></div>')


DL_FORM = f'''<dialog class="j-dialog" id="dl" aria-labelledby="dl-title" data-file="{TPL}" data-fname="{TPL_NAME}" data-title="Inventory ABC and Safety Stock Template (Excel)" data-ref="Inventory template">
  <form method="dialog" class="form j-dl-form" novalidate>
    <button type="button" class="j-dl-close" aria-label="Close">×</button>
    <p class="eyebrow">Chmltech Insights · Free template</p>
    <h2 class="h-md" id="dl-title">Download the template</h2>
    <p class="muted j-dl-paper">Inventory ABC and Safety Stock Template (Excel workbook)</p>
    <input class="hp" type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="field"><label for="dl-name">Full name</label><input id="dl-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="dl-email">Work email</label><input id="dl-email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="dl-company">Company <span class="hint">(optional)</span></label><input id="dl-company" name="company" autocomplete="organization"></div>
    <label class="j-dl-consent"><input type="checkbox" name="updates" value="Yes"> Send me occasional updates on new Chmltech articles and services. I can unsubscribe at any time.</label>
    <p class="j-dl-note">We use your details to record this request and may follow up about it. See our <a href="../privacy.html" target="_blank" rel="noopener">privacy notice</a>.</p>
    <button type="submit" class="btn">Download template</button>
    <p class="form-status" role="status" tabindex="-1"></p>
  </form>
</dialog>
<script src="../assets/js/download.js" defer></script>'''
NAVY, BLUE, INK, MUTED, GRID, GREY, LIGHT, AXIS = ("#0B2A5A", "#0B6FA4", "#26324A", "#5A6475", "#E3E6EC",
                                                    "#A9B2C0", "#D3D9E2", "#8A93A3")
Z = lambda sl: NormalDist().inv_cdf(sl)
money = lambda v: f"${v:,.0f}"


# ---------- small HTML helpers ----------
NUM = re.compile(r"^(<strong>)?\$?[\d][\d,.]*%?(\s?(kg|L|units|weeks))?(</strong>)?$")


def plain(c): return html.unescape(re.sub(r"<[^>]+>", "", str(c)))


def td(c, tag="td", limit=22):
    """Quantities, money, percentages and short labels stay on one line (180,000 kg; 3. Desirable)."""
    keep = NUM.match(str(c)) or len(plain(c)) <= limit
    return f'<{tag} style="white-space:nowrap">{c}</{tag}>' if keep else f"<{tag}>{c}</{tag}>"


def tbl(rows, wide=False, first=None):
    """Short cells never break across lines. In tables of up to four columns the row labels in the first
    column get a longer allowance. wide=True marks a many-column table: smaller type and tighter cells
    (assets/css/article-tables.css), and its headers may wrap. first overrides the first-column allowance
    where the default would push the table wider than the page."""
    first = first or (30 if len(rows[0]) <= 4 else 22)
    cell = lambda c, i, tag="td": td(c, tag, first if i == 0 else 22)
    head = "".join(f"<th>{c}</th>" if wide else cell(c, i, "th") for i, c in enumerate(rows[0]))
    out = ['<table class="t-wide">' if wide else "<table>", "<tr>" + head + "</tr>"]
    out += ["<tr>" + "".join(cell(c, i) for i, c in enumerate(r)) + "</tr>" for r in rows[1:]]
    return "\n".join(out + ["</table>"])


def ul(items): return "<ul>\n" + "\n".join(f"<li>{i}</li>" for i in items) + "\n</ul>"
def ol(items): return "<ol>\n" + "\n".join(f"<li>{i}</li>" for i in items) + "\n</ol>"


def formula(s):
    return ('<p style="background:var(--sand);padding:14px 18px;border-radius:8px;font-family:Georgia,serif;'
            f'font-size:17px;overflow-x:auto;white-space:nowrap">{s}</p>')


def part(n):
    return ('<link rel="stylesheet" href="../assets/css/article-tables.css">'
            f'<p><em>Part {n} of 4 in the inventory control series.</em></p>')


CLOSE = ('<p><em>Chmltech Ltd. helps small and mid-sized businesses improve operations and adopt digital tools. '
         'If you would like help applying this to your own inventory, <a href="../contact.html">get in touch</a>.</em></p>')


# ---------- charts (static inline SVG) ----------
def fig(w, h, label, inner, caption):
    return (f'<figure style="overflow-x:auto"><svg role="img" aria-label="{E(label)}" viewBox="0 0 {w} {h}" width="{w}" '
            'style="max-width:100%;height:auto;display:block;margin:0 auto;min-width:560px" '
            'xmlns="http://www.w3.org/2000/svg" font-family="Inter,system-ui,sans-serif" font-size="12">'
            + inner + f'</svg><figcaption>{E(caption)}</figcaption></figure>')


def rank(items, a_cut=80, b_cut=95):
    """items: dicts with sku, item, units, cost. Returns ranked dicts with v, pct, cum, cls, i."""
    total = sum(round(r["units"] * r["cost"], 2) for r in items)
    out, run = [], 0
    for i, r in enumerate(sorted(items, key=lambda r: -r["units"] * r["cost"])):
        v = round(r["units"] * r["cost"], 2); run += v; cum = run / total * 100
        out.append(dict(r, v=v, i=i, pct=v / total * 100, cum=cum, cls="A" if cum <= a_cut else "B" if cum <= b_cut else "C"))
    return out, total


def pareto(pts, total, title, ticks, label, caption, accent, note=None, callouts=()):
    W, H, left, y0, base = 720, 400, 58, 104, 330
    pw = 596; band = pw / len(pts); h = base - y0; vmax = max(p["v"] for p in pts)
    x = lambda i: left + i * band; cx = lambda i: left + i * band + band / 2
    yv = lambda v: base - v / vmax * h; yc = lambda c: base - c / 100 * h
    s = [f'<text x="{left}" y="26" font-size="16" font-weight="600" fill="{NAVY}">{E(title)}</text>',
         f'<text x="{left}" y="46" fill="{MUTED}">Bars: annual value per item, ranked. Line: cumulative share of the {money(total)} total.</text>']
    if note: s.append(f'<text x="{left}" y="63" fill="{BLUE}" font-weight="600">{E(note)}</text>')
    for t in ticks:
        s.append(f'<line x1="{left}" x2="{left + pw}" y1="{yv(t):.1f}" y2="{yv(t):.1f}" stroke="{GRID}"/>'
                 f'<text x="{left - 8}" y="{yv(t) + 4:.1f}" text-anchor="end" fill="{MUTED}">{"$%dk" % (t / 1000) if t else "$0"}</text>')
    for t in (80, 95):
        s.append(f'<line x1="{left}" x2="{left + pw}" y1="{yc(t):.1f}" y2="{yc(t):.1f}" stroke="{AXIS}" stroke-dasharray="4 4"/>'
                 f'<text x="{left + pw + 6}" y="{yc(t) + 4:.1f}" fill="{MUTED}">{t}%</text>')
    for p in pts:
        bh = max(2, p["v"] / vmax * h); col = accent(p)
        s.append(f'<rect x="{x(p["i"]) + 4:.1f}" y="{base - bh:.1f}" width="{band - 8:.1f}" height="{bh:.1f}" fill="{col}">'
                 f'<title>{E(p["sku"])} {E(p["item"])}: {money(p["v"])} a year, class {p["cls"]}</title></rect>')
        strong = col == BLUE and note
        s.append(f'<text transform="rotate(-45 {cx(p["i"]) + 4:.1f} {base + 14})" x="{cx(p["i"]) + 4:.1f}" y="{base + 14}" text-anchor="end" '
                 f'font-size="10" fill="{BLUE if strong else MUTED}"{" font-weight=\"600\"" if strong else ""}>{E(p["sku"])}</text>')
    s.append(f'<line x1="{left}" x2="{left + pw}" y1="{base}" y2="{base}" stroke="{AXIS}"/>')
    for c in "ABC":
        g = [p for p in pts if p["cls"] == c]
        share = sum(p["v"] for p in g) / total * 100
        mid = (x(g[0]["i"]) + x(g[-1]["i"]) + band) / 2
        s.append(f'<text x="{mid:.1f}" y="{y0 - 14}" text-anchor="middle" font-weight="600" fill="{NAVY}">{c}: {len(g)} items, {share:.1f}%</text>')
        if c != "C":
            xs = x(g[-1]["i"]) + band
            s.append(f'<line x1="{xs:.1f}" x2="{xs:.1f}" y1="{y0 - 6}" y2="{base}" stroke="{AXIS}"/>'
                     f'<text x="{xs + 6:.1f}" y="{yc(g[-1]["cum"]) + 22:.1f}" fill="{INK}">{g[-1]["cum"]:.1f}%</text>')
    s.append(f'<polyline points="{" ".join(f"{cx(p["i"]):.1f},{yc(p["cum"]):.1f}" for p in pts)}" fill="none" stroke="{NAVY}" stroke-width="1.5"/>')
    s += [f'<circle cx="{cx(p["i"]):.1f}" cy="{yc(p["cum"]):.1f}" r="2.5" fill="{NAVY}"><title>{E(p["sku"])}: cumulative {p["cum"]:.1f}%</title></circle>' for p in pts]
    for k, p in enumerate(callouts):
        yl = 206 + k * 38; bh = max(2, p["v"] / vmax * h)
        s.append(f'<line x1="{cx(p["i"]):.1f}" x2="{cx(p["i"]):.1f}" y1="{yl + 22}" y2="{base - bh - 10:.1f}" stroke="{BLUE}" stroke-opacity=".6"/>'
                 f'<circle cx="{cx(p["i"]):.1f}" cy="{base - bh - 6:.1f}" r="3" fill="{BLUE}"/>'
                 f'<text x="{cx(p["i"]) + 20:.1f}" y="{yl}" text-anchor="middle" font-weight="600" fill="{BLUE}">{E(p["sku"])} {E(p["short"])}</text>'
                 f'<text x="{cx(p["i"]) + 20:.1f}" y="{yl + 15}" text-anchor="middle" fill="{MUTED}">{money(p["v"])} a year</text>')
    return fig(W, H, label, "".join(s), caption)


def bars(rows, title, sub, label, caption, target=None):
    """rows: dicts with top (label above bar), v (bar height value), x1, x2 (labels under), hi (accent)."""
    W, H, left, y0, base = 720, 340, 40, 92, 276
    pw = 640; band = pw / len(rows); bw = min(64, band * 0.56); vmax = max(r["v"] for r in rows) if not target else 100
    s = [f'<text x="{left}" y="26" font-size="16" font-weight="600" fill="{NAVY}">{E(title)}</text>',
         f'<text x="{left}" y="46" fill="{MUTED}">{E(sub)}</text>']
    y = lambda v: base - v / vmax * (base - y0)
    if target:
        s.append(f'<line x1="{left}" x2="{left + pw}" y1="{y(target):.1f}" y2="{y(target):.1f}" stroke="{AXIS}" stroke-dasharray="4 4"/>'
                 f'<text x="{left}" y="{y(target) - 6:.1f}" fill="{MUTED}">{target}% target</text>')
    for i, r in enumerate(rows):
        xx = left + i * band + (band - bw) / 2
        s.append(f'<rect x="{xx:.1f}" y="{y(r["v"]):.1f}" width="{bw:.1f}" height="{base - y(r["v"]):.1f}" fill="{BLUE if r.get("hi") else GREY}"/>'
                 f'<text x="{xx + bw / 2:.1f}" y="{y(r["v"]) - 8:.1f}" text-anchor="middle" fill="{INK}"{" font-weight=\"600\"" if r.get("hi") else ""}>{E(r["top"])}</text>'
                 f'<text x="{xx + bw / 2:.1f}" y="{base + 18}" text-anchor="middle" fill="{INK}">{E(r["x1"])}</text>'
                 f'<text x="{xx + bw / 2:.1f}" y="{base + 34}" text-anchor="middle" font-size="11" fill="{MUTED}">{E(r["x2"])}</text>')
    s.append(f'<line x1="{left}" x2="{left + pw}" y1="{base}" y2="{base}" stroke="{AXIS}"/>')
    return fig(W, H, label, "".join(s), caption)


# ---------- example data ----------
def I(sku, item, units, cost, **k): return dict(sku=sku, item=item, units=units, cost=cost, **k)

NORTH = [I("NS-101", "Nitrile gloves, case of 1,000", 5200, 62), I("NS-102", "Stretch wrap, 18 in x 1,500 ft", 9800, 24.5),
         I("NS-103", "Corrugated box, 18x12x12, bundle of 25", 7400, 28), I("NS-104", "Safety glasses, box of 12", 3100, 54),
         I("NS-105", "Packing tape, case of 36", 2600, 38), I("NS-106", "Degreaser, 20 L pail", 820, 96),
         I("NS-107", "Pallet strapping kit", 410, 165), I("NS-108", "Hi-vis vest, pack of 10", 900, 68),
         I("NS-109", "Absorbent pads, bale of 100", 760, 72), I("NS-110", "Hand cleaner, 4 L, case of 4", 640, 58),
         I("NS-111", "Shop towels, case of 12 rolls", 520, 44), I("NS-112", "Bubble wrap, 24 in x 250 ft", 300, 36),
         I("NS-113", "Ear plugs, box of 200", 260, 32), I("NS-114", "Utility knife, pack of 10", 190, 41),
         I("NS-115", "Shipping labels, roll of 1,000", 420, 17.5), I("NS-116", "Dust masks, box of 50", 330, 19),
         I("NS-117", "Floor marking tape, roll", 240, 22), I("NS-118", "Zip ties, bag of 1,000", 180, 24),
         I("NS-119", "Spray bottles, case of 12", 110, 27), I("NS-120", "Replacement blades, pack of 100", 95, 18)]

RIDGE = [I("RM-01", "Epoxy resin", 180000, 4.2, pool="Raw material", u=" kg", crit=1, short="epoxy resin"),
         I("RM-02", "Titanium dioxide pigment", 95000, 3.8, pool="Raw material", u=" kg", crit=1, short="pigment"),
         I("RM-03", "Xylene solvent", 210000, 1.35, pool="Raw material", u=" L", crit=2, short="xylene"),
         I("RM-04", "Polyamine hardener", 42000, 6.1, pool="Raw material", u=" kg", crit=1, short="hardener"),
         I("RM-05", "Acrylic resin", 38000, 3.5, pool="Raw material", u=" kg", crit=2, short="acrylic resin"),
         I("RM-06", "Calcium carbonate extender", 160000, 0.45, pool="Raw material", u=" kg", crit=3, short="extender"),
         I("RM-07", "Iron oxide red pigment", 9000, 5.2, pool="Raw material", u=" kg", crit=2, short="red pigment"),
         I("RM-08", "Dispersant additive", 2400, 14, pool="Raw material", u=" kg", crit=1, short="dispersant"),
         I("RM-09", "Defoamer additive", 1100, 11.5, pool="Raw material", u=" kg", crit=2, short="defoamer"),
         I("RM-10", "Thickener", 900, 9, pool="Raw material", u=" kg", crit=2, short="thickener"),
         I("PK-01", "20 L steel pail with lid", 48000, 5.6, pool="Packaging", u="", crit=2, short="steel pail"),
         I("PK-02", "4 L can with lid", 60000, 1.9, pool="Packaging", u="", crit=2, short="4 L can"),
         I("PK-03", "Product labels, per 1,000", 120, 85, pool="Packaging", u="", crit=2, short="labels"),
         I("PK-04", "Pallets", 2600, 14, pool="Packaging", u="", crit=3, short="pallets"),
         I("SP-01", "Disperser mechanical seal", 4, 1850, pool="Spare part", u="", crit=1, short="mechanical seal"),
         I("SP-02", "Filling line gasket set", 60, 40, pool="Spare part", u="", crit=1, short="gasket set"),
         I("SP-03", "Filter bags, box of 50", 90, 120, pool="Spare part", u="", crit=2, short="filter bags"),
         I("SP-04", "Pump diaphragm kit", 12, 310, pool="Spare part", u="", crit=2, short="diaphragm kit"),
         I("SP-05", "Drive belt", 20, 65, pool="Spare part", u="", crit=3, short="drive belt"),
         I("SP-06", "Dispersion blade", 6, 480, pool="Spare part", u="", crit=2, short="dispersion blade")]


def cls_sum(pts, total, c):
    g = [p for p in pts if p["cls"] == c]; v = sum(p["v"] for p in g)
    return len(g), v, v / total * 100


def ss3(d, sd, L, sL, sl):
    return math.ceil(Z(sl) * math.sqrt(L * sd * sd + d * d * sL * sL) - 1e-9)


# ================= Post 1 =================
def post1():
    pts, total = rank(NORTH)
    (na, va, pa), (nb, vb, pb), (nc, vc, pc) = (cls_sum(pts, total, c) for c in "ABC")
    assert (na, nb, nc, total) == (6, 4, 10, 1413000)
    rows = [["Rank", "SKU", "Item", "Annual units", "Unit cost", "Annual usage", "% of total", "Cumulative %", "Class"]]
    rows += [[p["i"] + 1, p["sku"], E(p["item"]), f'{p["units"]:,}', f'${p["cost"]:,.2f}', money(p["v"]), f'{p["pct"]:.1f}%',
              f'{p["cum"]:.1f}%', p["cls"]] for p in pts]
    chart = pareto(pts, total, f"{na} of {len(pts)} items carry {pa:.0f}% of annual dollar usage", [0, 100000, 200000, 300000],
                   "Pareto chart of 20 items ranked by annual dollar usage. Six class A items carry 78.9% of the total, four class B items "
                   "carry 15.6% and ten class C items carry 5.5%. The cumulative line crosses 80% after the sixth item and 95% after the tenth.",
                   "Illustrative data for a fictional distributor: 20 SKUs, 12 months of usage.",
                   lambda p: BLUE if p["cls"] == "A" else GREY if p["cls"] == "B" else LIGHT)
    bottom4 = sum(p["v"] for p in pts[-4:]); assert 0.05 * pts[0]["v"] > bottom4
    return "\n".join([
        part(1),
        "<p>Most warehouses manage every item the same way. The $62 case of gloves that sells 100 times a week gets the same count schedule, the same reorder routine and the same attention as the box of blades that sells twice a week.</p>",
        "<p>That feels fair, but it is expensive. The buyer's time is spread thin across hundreds of items, so the few that drive the business get no more care than the many that barely matter. The usual result is stockouts on the fast movers and cash tied up in the slow ones.</p>",
        "<p>ABC analysis fixes this with one afternoon of spreadsheet work. It sorts your inventory into three classes, so you can put tight control where the money is and simple rules everywhere else. This post explains the method and walks through a full example for a distributor.</p>",
        "<h2>What ABC analysis is</h2>",
        "<p>ABC analysis ranks inventory items by how much money flows through each one in a year, then splits the ranked list into three classes. It applies the Pareto principle: a small share of items accounts for a large share of the value.</p>",
        "<p>The measure is <strong>annual dollar usage</strong>: units sold or consumed in a year, multiplied by unit cost. A cheap item that moves in huge volume can outrank an expensive item that rarely moves.</p>",
        tbl([["Class", "Share of items", "Share of annual dollar usage", "In plain terms"],
             ["A", "10 to 20%", "70 to 80%", "The few items that carry the business"],
             ["B", "About 30%", "15 to 25%", "The middle: important, but not critical"],
             ["C", "50 to 60%", "About 5%", "The long tail of low-value items"]]),
        "<p>These ranges are guides, not rules. Your own split depends on your product mix, and the goal is a useful grouping, not a perfect 80/20.</p>",
        "<h2>How to do it in five steps</h2>",
        "<p>You need a spreadsheet and two numbers per item: units used in the last 12 months, and unit cost.</p>",
        ol(["<strong>Pull the data.</strong> Export every stocked item with its 12-month usage and current unit cost. Use a full year so seasonal items are not misjudged.",
            "<strong>Calculate annual dollar usage.</strong> Multiply usage by unit cost for each item.",
            "<strong>Rank.</strong> Sort the list from highest annual dollar usage to lowest.",
            "<strong>Add the cumulative percentage.</strong> Work out each item's share of the total, then add a running total down the list.",
            "<strong>Assign classes.</strong> Set your cut-offs and label each item. A common starting point is A up to 80% of cumulative value, B from 80% to 95%, and C for the rest."]),
        "<p>Use cost, not selling price, because the aim is to manage money tied up in stock. If your costs are unreliable, fix the worst of them first; the ranking is only as good as the data behind it.</p>",
        "<h2>A worked example: a 20-item distributor</h2>",
        f"<p>Northshore Supply is a fictional distributor of packaging and safety products. It stocks 20 items with a combined annual usage of {money(total)} at cost. The table shows all five steps completed: usage and cost pulled, dollar usage calculated, items ranked, cumulative share added, and classes assigned.</p>",
        tbl(rows, wide=True),
        "<p>The cut-offs used are 80% and 95% of cumulative value. Plotted as a Pareto chart, the pattern is easy to see.</p>",
        chart,
        "<p>Three things stand out:</p>",
        ul([f"<strong>Six A items carry {money(va)}, or {pa:.1f}% of the total.</strong> These are 30% of the items. A 5% ordering error on gloves alone is worth more than the entire yearly usage of the bottom four items combined.",
            f"<strong>Four B items carry {money(vb)}, or {pb:.1f}%.</strong> They matter, but a standard reorder routine is enough.",
            f"<strong>Ten C items carry {money(vc)}, or {pc:.1f}%.</strong> Half the item list, and half the counting and ordering effort, is spent on one-twentieth of the value."]),
        "<p>Notice that rank and unit cost are not the same thing. The pallet strapping kit is the most expensive item at $165, yet it lands in class B. Stretch wrap costs $24.50 and ranks second, because volume counts as much as price.</p>",
        "<h2>What to do with each class</h2>",
        "<p>The classes only pay off when each one gets a different level of control. The table below is a practical starting policy.</p>",
        tbl([["Practice", "A items", "B items", "C items"],
             ["Cycle count", "Monthly", "Quarterly", "Once or twice a year"],
             ["Reorder review", "Weekly", "Every two weeks or monthly", "Quarterly, or only when the minimum is hit"],
             ["Ordering method", "Forecast-based, smaller and more frequent orders", "Reorder point with a standard order quantity", "Simple min/max or two-bin, larger and less frequent orders"],
             ["Supplier attention", "Negotiated pricing, a backup source, lead times tracked", "Standard terms, reviewed yearly", "Consolidate with one supplier to cut paperwork"],
             ["Who decides", "Buyer or manager reviews each order", "Buyer approves system suggestions", "Automatic, or delegated to the warehouse"]]),
        "<p>The logic is simple. A items justify a person's attention because a small error costs real money. C items do not, so the cheapest control that prevents stockouts is the right one. Holding a little extra of a C item costs almost nothing; spending an hour a week managing it costs more than the item is worth.</p>",
        "<h2>Common mistakes</h2>",
        "<p><strong>Classifying on dollar value alone.</strong> Some low-value items are critical. If one customer buys their A items from you only because you also stock a particular C item, running out of it costs far more than its ranking suggests. Review the C list by hand and flag the exceptions.</p>",
        "<p><strong>Running it once.</strong> Products rise and fade, costs change, and customers come and go. Re-run the analysis at least once a year, and every six months if your range changes quickly.</p>",
        "<p><strong>Using too short a period.</strong> Three months of data will misclassify anything seasonal. Use 12 months, and for new items use a forecast until they have a history.</p>",
        "<p><strong>Changing the labels but not the behaviour.</strong> The analysis is worth nothing if every item is still counted and reordered the same way afterwards. Write the class policies down and build them into the routine.</p>",
        f'<p><strong>Ignoring how steady the demand is.</strong> Two A items with the same annual value can behave very differently. One sells the same amount every week; the other swings between nothing and a truckload. ABC tells you which items matter. It does not tell you how much buffer each one needs. That depends on demand variability and supplier lead time, which is the subject of <a href="{S2}.html">the next post</a> on safety stock.</p>',
        "<h2>Your checklist</h2>",
        ul(["Export 12 months of usage and current unit cost for every stocked item", "Calculate annual dollar usage and rank the list",
            "Add cumulative percentages and assign A, B and C classes", "Review the C list by hand for critical items",
            "Write a count, review and ordering policy for each class", "Put a date in the calendar to re-run the analysis"]),
        tpl_box("A workbook accompanies this series. It ranks and classifies your items automatically and includes the example data from this post."),
        f"<p><strong>Next in the series:</strong> {P[2]} takes three items from this example and sets a safety stock and reorder point for each.</p>",
        CLOSE, DL_FORM])


# ================= Post 2 =================
EX2 = [dict(sku="NS-101", name="Nitrile gloves", cls="A", u=5200, cost=62, sd=20, mx=140, L=4, sL=1.0, mxL=6, sl=0.98),
       dict(sku="NS-108", name="Hi-vis vest", cls="B", u=900, cost=68, sd=6, mx=30, L=3, sL=0.5, mxL=4, sl=0.95),
       dict(sku="NS-111", name="Shop towels", cls="C", u=520, cost=44, sd=5, mx=22, L=2, sL=0.5, mxL=3, sl=0.90)]


def post2():
    for e in EX2:
        e["d"] = e["u"] / 52
        e["m1"] = math.ceil(max(0, e["mx"] * e["mxL"] - e["d"] * e["L"]) - 1e-9)
        e["m2"] = math.ceil(Z(e["sl"]) * e["sd"] * math.sqrt(e["L"]) - 1e-9)
        e["m3"] = ss3(e["d"], e["sd"], e["L"], e["sL"], e["sl"])
        e["rop"] = math.ceil(e["d"] * e["L"] + e["m3"] - 1e-9); e["val"] = e["m3"] * e["cost"]; e["two"] = round(2 * e["d"])
    g, v, t = EX2
    assert (g["m1"], g["m2"], g["m3"], g["rop"]) == (440, 83, 222, 622) and (v["m3"], v["rop"], t["m3"], t["rop"]) == (23, 75, 12, 32)
    tot3 = sum(e["val"] for e in EX2); tot2 = sum(e["two"] * e["cost"] for e in EX2)
    levels = [(0.85, "85%"), (0.90, "90%"), (0.95, "95%"), (0.97, "97%"), (0.98, "98%"), (0.99, "99%"), (0.995, "99.5%"), (0.999, "99.9%")]
    lv = {lab: ss3(g["d"], g["sd"], g["L"], g["sL"], sl) for sl, lab in levels}
    chart = bars([dict(top=money(lv[lab] * g["cost"]), v=lv[lab] * g["cost"], x1=lab, x2=f"{lv[lab]} units", hi=lab == "98%") for _, lab in levels],
                 "Each extra point of service costs more than the last",
                 "Safety stock value for NS-101 nitrile gloves at each service level, Method 3",
                 "Bar chart of safety stock value for nitrile gloves at eight service levels, rising from "
                 f"{money(lv['85%'] * g['cost'])} at 85% to {money(lv['99.9%'] * g['cost'])} at 99.9%. The 98% target used in the example is {money(lv['98%'] * g['cost'])}.",
                 "Illustrative data for a fictional distributor: NS-101, $62 unit cost. The blue bar is the 98% target used in the example.")
    t99 = ss3(t["d"], t["sd"], t["L"], t["sL"], 0.99)
    hdr = ["", "NS-101 Nitrile gloves (A)", "NS-108 Hi-vis vest (B)", "NS-111 Shop towels (C)"]
    return "\n".join([
        part(2),
        "<p>Ask how a business sets its safety stock and the usual answer is a rule of thumb: \"we keep two weeks of everything.\" It is easy to remember and easy to apply. It is also wrong for most items.</p>",
        "<p>A flat rule ignores the two things that create the need for a buffer: how much demand swings, and how reliable the supplier is. An item with steady sales and a dependable supplier needs very little. An item with erratic sales and a supplier who is sometimes two weeks late needs a lot. \"Two weeks\" gives both the same cover.</p>",
        f"<p>In {P[1]} we used ABC analysis to find which items matter most at Northshore Supply, a fictional distributor. This post sets a safety stock and reorder point for three of those items, one from each class, and shows what the flat rule gets wrong.</p>",
        "<h2>What safety stock is</h2>",
        "<p>Safety stock is the extra inventory you hold to cover the gap between what you expected and what actually happened during a supplier's lead time. It is not the stock you plan to sell; it is the cushion underneath it.</p>",
        "<p>It feeds directly into the <strong>reorder point</strong>, the stock level at which you place the next order:</p>",
        formula("Reorder point = (average demand &times; lead time) + safety stock"),
        "<p>Three things decide how big the cushion needs to be:</p>",
        tbl([["Driver", "The question it answers", "Where to find it"],
             ["Demand variability", "How far does weekly demand stray from its average?", "Standard deviation of weekly sales over the last 12 months"],
             ["Lead time and its variability", "How long does the supplier take, and how often are they late?", "Purchase order date to receipt date, for the last 10 to 20 orders"],
             ["Target service level", "How often are you willing to run out?", "A business decision, set by ABC class"]]),
        "<p>A 95% service level means that in 95 out of 100 replenishment cycles, stock lasts until the next delivery arrives. The other five times, you run short. Service level is a choice, and a higher one always costs more stock.</p>",
        "<h2>Three methods, from simple to rigorous</h2>",
        "<h3>Method 1: Average-max</h3>",
        "<p>This needs no statistics. Take your worst realistic case and subtract the normal case.</p>",
        formula("SS = (max weekly demand &times; max lead time) &minus; (average weekly demand &times; average lead time)"),
        "<p>It is quick and works with very little data. Its weakness is that it assumes the busiest week and the latest delivery happen together, so it usually overstates the buffer. One freak week in your history can inflate it badly.</p>",
        "<h3>Method 2: Statistical, demand variability only</h3>",
        "<p>This is the standard textbook formula. It sizes the buffer from how much demand actually varies and the service level you choose.</p>",
        formula("SS = Z &times; &sigma;<sub>d</sub> &times; &radic;L"),
        "<p>Here Z is the service factor, &sigma;<sub>d</sub> is the standard deviation of weekly demand, and L is the lead time in weeks. Use it when your supplier delivers on time, every time.</p>",
        "<h3>Method 3: Statistical, demand and lead time variability</h3>",
        "<p>Most suppliers are not perfectly reliable. This version adds the lead time's own variability.</p>",
        formula("SS = Z &times; &radic;( L &times; &sigma;<sub>d</sub>&sup2; + d&sup2; &times; &sigma;<sub>L</sub>&sup2; )"),
        "<p>Here d is average weekly demand and &sigma;<sub>L</sub> is the standard deviation of lead time in weeks. This is the method to use for A and B items whenever you have the lead time history.</p>",
        "<h3>The service factor Z</h3>",
        "<p>Z converts a service level into a number of standard deviations. In Excel it is <code>=NORM.S.INV(service level)</code>.</p>",
        tbl([["Service level", "90%", "95%", "98%", "99%", "99.9%"], ["Z"] + [f"{Z(s):.2f}" for s in (0.90, 0.95, 0.98, 0.99, 0.999)]]),
        "<p>Keep the units consistent. If demand is measured per week, lead time must be in weeks too.</p>",
        "<h2>A worked example: three items from Northshore Supply</h2>",
        f'<p>We take one item from each ABC class in {P[1]}. Average weekly demand is the annual usage divided by 52. The other figures come from Northshore\'s sales and purchase order history.</p>',
        tbl([["Input"] + hdr[1:],
             ["Average weekly demand (units)"] + [f'{e["d"]:.1f}'.rstrip("0").rstrip(".") for e in EX2],
             ["Standard deviation of weekly demand"] + [e["sd"] for e in EX2],
             ["Maximum weekly demand"] + [e["mx"] for e in EX2],
             ["Average lead time (weeks)"] + [e["L"] for e in EX2],
             ["Standard deviation of lead time (weeks)"] + [f'{e["sL"]:.1f}' for e in EX2],
             ["Maximum lead time (weeks)"] + [e["mxL"] for e in EX2],
             ["Target service level"] + [f'{e["sl"]:.0%}' for e in EX2],
             ["Unit cost"] + [money(e["cost"]) for e in EX2]]),
        "<h3>Step by step for the gloves, using Method 3</h3>",
        ol(["Demand part: L &times; &sigma;<sub>d</sub>&sup2; = 4 &times; 20&sup2; = 1,600",
            "Lead time part: d&sup2; &times; &sigma;<sub>L</sub>&sup2; = 100&sup2; &times; 1&sup2; = 10,000",
            "Add and take the square root: &radic;11,600 = 107.7 units",
            f"Multiply by Z for 98%: {Z(0.98):.3f} &times; 107.7 = 221.2, rounded up to <strong>{g['m3']} units</strong>",
            f"Reorder point: (100 &times; 4) + {g['m3']} = <strong>{g['rop']} units</strong>"]),
        f"<p>When stock on hand plus stock on order falls to {g['rop']} cases, Northshore places the next order.</p>",
        "<h3>Results for all three items</h3>",
        tbl([["Result (units)", "NS-101 Gloves (A)", "NS-108 Vest (B)", "NS-111 Towels (C)"],
             ["Method 1: Average-max"] + [e["m1"] for e in EX2],
             ["Method 2: Demand variability only"] + [e["m2"] for e in EX2],
             ["<strong>Method 3: Demand and lead time</strong>"] + [f'<strong>{e["m3"]}</strong>' for e in EX2],
             ["Reorder point (Method 3)"] + [e["rop"] for e in EX2],
             ["Safety stock value (Method 3)"] + [money(e["val"]) for e in EX2],
             ["\"Two weeks of everything\" rule"] + [e["two"] for e in EX2]]),
        "<p>Four lessons come out of this table.</p>",
        ul([f"<strong>Lead time variability can matter more than demand variability.</strong> For the gloves, the lead time part (10,000) is six times the demand part (1,600). Method 2 ignores it and gives {g['m2']} units, well under half of what is needed.",
            "<strong>Average-max overshoots.</strong> It asks for two to four times the Method 3 figure, because it plans for the worst week and the latest delivery arriving together.",
            f"<strong>The flat rule puts stock in the wrong place.</strong> Two weeks is {1 - g['two'] / g['m3']:.0%} too little for the gloves, about 50% too much for the vests and {t['two'] / t['m3'] - 1:.0%} too much for the towels.",
            f"<strong>The right buffers do not cost more.</strong> Method 3 holds {money(tot3)} across the three items; the flat rule holds {money(tot2)}. The money is nearly the same, but it now sits where the risk is."]),
        "<h2>Choosing a service level for each class</h2>",
        "<p>Service level is where ABC analysis and safety stock meet. A common starting policy looks like this.</p>",
        tbl([["Class", "Typical target", "Reasoning"],
             ["A", "97 to 99%", "A stockout loses the most revenue, so aim high, but calculate carefully because the buffer is expensive"],
             ["B", "95%", "A solid default for items that matter but are not critical"],
             ["C", "90 to 95%", "A stockout costs little, and a simple generous buffer is often enough"]]),
        "<p>The catch is that service gets more expensive the higher you go. The chart shows the safety stock value for the gloves at eight service levels.</p>",
        chart,
        f"<p>Moving from 95% to 99.9% nearly doubles the buffer, from {money(lv['95%'] * 62)} to {money(lv['99.9%'] * 62)}. The last step alone, from 99% to 99.9%, costs {money((lv['99.9%'] - lv['99%']) * 62)} for less than one point of service. No level reaches 100%, because the formula has no upper limit.</p>",
        f"<p>The same step is cheap on a C item. Raising the shop towels from 90% to 99% adds {t99 - t['m3']} cases, or {money((t99 - t['m3']) * t['cost'])}. That is why many businesses do the careful calculation only for A and B items, and give C items a generous flat buffer. The effort goes where a wrong answer costs real money.</p>",
        "<h2>Practical cautions</h2>",
        "<p><strong>Lumpy demand breaks the formula.</strong> Methods 2 and 3 assume demand is spread roughly evenly around its average. An item that sells nothing for five weeks and then 40 in one week does not behave that way. As a rough test, if the standard deviation is larger than the average, do not trust the statistical result. Use average-max or a simple min/max instead.</p>",
        "<p><strong>Measure real lead time.</strong> Use the date the goods were received, not the date the supplier promised. Count from the day you placed the order, and include your own receiving and put-away time.</p>",
        "<p><strong>Remove one-off events.</strong> A single project order or a one-time promotion inflates the standard deviation for a year. Take it out before you calculate, and note that you did.</p>",
        "<p><strong>Safety stock does not fix a biased forecast.</strong> If demand is consistently above forecast, the problem is the forecast. Safety stock covers random swings, not a steady error in one direction.</p>",
        "<p><strong>Compare the reorder point to the right number.</strong> Use stock on hand plus stock already on order, less any customer backorders. Checking on-hand alone leads to double ordering.</p>",
        "<p><strong>Review on a schedule.</strong> Recalculate A items every quarter, B items twice a year and C items once a year. Recalculate immediately when you change supplier or a lead time shifts.</p>",
        "<h2>Your checklist</h2>",
        ul(["Pull 12 months of weekly demand for your A and B items", "Pull order and receipt dates for the last 10 to 20 purchase orders per item",
            "Calculate the average and standard deviation of demand and of lead time", "Set a target service level for each ABC class",
            "Calculate safety stock with Method 3, and the reorder point", "Use average-max or min/max for C items and for lumpy demand",
            "Load the reorder points into your system and set a review date"]),
        tpl_box("The workbook for this series includes a safety stock calculator with all three methods, preloaded with the Northshore example."),
        f"<p><strong>Next in the series:</strong> {P[3]} applies ABC analysis to a manufacturer, where raw materials, work in progress and spare parts each need their own treatment.</p>",
        CLOSE, DL_FORM])


# ================= Post 3 =================
def post3():
    pts, total = rank(RIDGE)
    (na, va, pa), (nb, vb, pb), (nc, vc, pc) = (cls_sum(pts, total, c) for c in "ABC")
    assert (na, nb, nc, total) == (5, 4, 11, 2420750)
    vital = [p for p in pts if p["crit"] == 1]; hidden = [p for p in vital if p["cls"] == "C"]
    assert len(vital) == 6 and [p["sku"] for p in hidden] == ["RM-08", "SP-01", "SP-02"]
    spares = sum(p["v"] for p in pts if p["pool"] == "Spare part"); assert all(p["cls"] == "C" for p in pts if p["pool"] == "Spare part")
    hv = sum(p["v"] for p in hidden)
    rows = [["Rank", "Item", "Pool", "Annual usage", "Unit cost", "Annual value", "Cumulative %", "Class"]]
    rows += [[p["i"] + 1, f'{p["sku"]} {E(p["item"])}', p["pool"], f'{p["units"]:,}{p["u"].replace(" ", "&nbsp;")}', f'${p["cost"]:,.2f}', money(p["v"]),
              f'{p["cum"]:.1f}%', p["cls"]] for p in pts]
    chart = pareto(pts, total, "Three of the six line-stopping items sit in the C tail", [0, 250000, 500000, 750000],
                   "Pareto chart of 20 purchased items ranked by annual value, with the six vital items highlighted. Epoxy resin, titanium dioxide "
                   "pigment and hardener are class A. The dispersant additive at $33,600 a year, the mechanical seal at $7,400 and the gasket set at "
                   "$2,400 are all in class C.",
                   "Illustrative data for a fictional manufacturer: 20 purchased items, 12 months of consumption.",
                   lambda p: BLUE if p["crit"] == 1 else GREY, note="Blue: vital items, where a stockout stops production.", callouts=hidden)
    seal = next(p for p in pts if p["sku"] == "SP-01"); gasket = next(p for p in pts if p["sku"] == "SP-02"); disp = next(p for p in pts if p["sku"] == "RM-08")
    protect = 2 * seal["cost"] + 10 * gasket["cost"] + 600 * disp["cost"]; assert protect == 12500
    return "\n".join([
        part(3),
        "<p>A $40 gasket set can shut down a filling line. On an ABC report it sits at the very bottom of class C, next to the drive belts, and gets the least attention of anything in the plant.</p>",
        f"<p>That is the problem with applying standard ABC analysis in a factory. The method in {P[1]} ranks items by annual dollar usage, and for a distributor that works well: when an item runs out, you lose that item's sales. In a plant, running out of one input can stop everything that depends on it. The cost of a stockout has little to do with the price of the part.</p>",
        f"<p>This post keeps the ABC method and adds one thing to it: a criticality rating. If you have not read {P[1]}, start there for the five steps. Here we cover only what changes for a manufacturer.</p>",
        "<h2>Three pools of inventory, three behaviours</h2>",
        "<p>A distributor holds one kind of inventory: finished goods for sale. A manufacturer holds several, and each follows different rules.</p>",
        tbl([["Pool", "What drives its demand", "What a stockout costs", "How to classify it"],
             ["Raw materials and packaging", "The production schedule. Usage follows what you plan to make.", "A delayed or cancelled batch, idle labour, late customer orders", "ABC by annual value consumed, plus criticality"],
             ["Spare parts and maintenance supplies", "Equipment wear and failure. Usage is low and irregular.", "Downtime on the equipment, and everything downstream of it", "Criticality first; value is almost irrelevant"],
             ["Work in progress", "Your own process and batch sizes", "Rarely a stockout; the cost is cash and floor space", "Leave out of ABC. Control it through scheduling."],
             ["Finished goods", "Customer orders", "A lost or late sale", f"Standard ABC by sales, as in {P[1]}"]], first=22),
        "<p>Two practical points follow. First, use <strong>consumption</strong>, the quantity issued to production or maintenance, not purchases. Purchases reflect when you bought, not what you used. Second, keep the unit of measure consistent. If resin is bought by the drum and issued by the kilogram, convert before you multiply.</p>",
        "<h2>A worked example: a coatings manufacturer</h2>",
        f"<p>Ridgeline Coatings is a fictional maker of industrial coatings. The list below covers 20 purchased items across raw materials, packaging and spare parts, with a combined annual usage of {money(total)}. It is ranked exactly as in {P[1]}, with cut-offs at 80% and 95% of cumulative value.</p>",
        tbl(rows, wide=True),
        f"<p>The split looks familiar: {na} A items carry {pa:.1f}% of the value, {nb} B items carry {pb:.1f}%, and {nc} C items carry {pc:.1f}%. By the usual logic, the plant would now manage five items closely and put the bottom eleven on autopilot.</p>",
        "<h2>What the value ranking misses</h2>",
        "<p>Now mark the items that would stop production if they ran out. The plant's production and maintenance leads identify six.</p>",
        chart,
        "<p>Three of the six are A items: epoxy resin, titanium dioxide and hardener. Value-based ABC already gives them attention. The other three are buried in class C:</p>",
        ul([f"<strong>RM-08 Dispersant additive</strong>, {money(disp['v'])} a year. Every batch needs it, it comes from a single supplier, and the lead time is eight weeks.",
            f"<strong>SP-01 Disperser mechanical seal</strong>, {money(seal['v'])} a year. The plant uses about four a year, and a replacement takes ten weeks to arrive.",
            f"<strong>SP-02 Filling line gasket set</strong>, {money(gasket['v'])} a year. The $40 part from the opening paragraph."]),
        f"<p>Together these three are worth {money(hv)} a year, under 2% of the total. Managed as ordinary C items, they would be counted once a year and reordered when someone noticed the bin was empty.</p>",
        f"<p>The ranking misleads in the other direction too. All six spare parts fall in class C, with a combined value of {money(spares)}. A value-only view says spares do not matter. Any maintenance manager will tell you otherwise.</p>",
        "<h2>Add a criticality rating</h2>",
        "<p>The fix is a second label on every item. Ask three questions: if we ran out today, would a line stop? Is there a substitute or a second supplier? How long would it take to get more?</p>",
        tbl([["Rating", "Meaning"],
             ["1. Vital", "Production stops. There is no substitute, and resupply takes weeks."],
             ["2. Essential", "Production is disrupted, but a substitute, second supplier or workaround is available within days."],
             ["3. Desirable", "No effect on output. Available locally the same day or week."]]),
        "<p>Production and maintenance staff should set these ratings, not purchasing alone. They know which parts have no workaround.</p>",
        "<p>The two labels together decide the control policy. Value sets how tightly you manage the item; criticality sets how much protection it gets.</p>",
        tbl([["Class", "Vital (1)", "Essential (2)", "Desirable (3)"],
             ["<strong>A</strong>", "Tight control and protected supply: forecast-driven orders, a supply agreement or second source, high service level", "Tight control with lean stock: frequent orders, no excess buffer", "Tight control with minimum stock: buy close to need"],
             ["<strong>B</strong>", "Standard reorder point with a raised service level", "Standard reorder point", "Standard reorder point with a lower service level"],
             ["<strong>C</strong>", "Never run out: hold a generous fixed minimum and check it on a schedule", "Simple min/max or two-bin", "Buy on demand, or hold a token quantity"]]),
        "<h3>What changes at Ridgeline</h3>",
        ul([f"<strong>The three vital C items get protection.</strong> Two spare mechanical seals on the shelf cost {money(2 * seal['cost'])} and ten gasket sets cost {money(10 * gasket['cost'])}. A three-month minimum of dispersant, 600 kg, costs {money(600 * disp['cost'])}. That is {money(protect)} in total to cover three items that can each stop the plant.",
            "<strong>The non-vital A items get leaner.</strong> Xylene and steel pails are high in value but available from several local suppliers. They need frequent orders and close tracking, not a large buffer.",
            f'<strong>The vital A items get both.</strong> Epoxy resin, titanium dioxide and hardener are expensive and irreplaceable. These justify supply agreements, a qualified second source and the careful safety stock calculation covered in <a href="{S4}.html">the next post</a>.']),
        "<h2>Pitfalls specific to manufacturers</h2>",
        "<p><strong>One year is too short for spare parts.</strong> A seal that fails every three years shows zero usage in most years. Use three to five years of history for spares, and never delete a vital part because it did not move last year.</p>",
        "<p><strong>Shelf life caps the buffer.</strong> \"Hold plenty of the cheap items\" works for gaskets. It does not work for a catalyst or additive with a six-month shelf life. Set the maximum stock below what you will use before it expires.</p>",
        "<p><strong>History misleads when the product mix is changing.</strong> Raw material usage follows the production plan. If you are launching a product or dropping one, rank materials on planned usage for the next 12 months, not on the last 12.</p>",
        "<p><strong>Dead stock is invisible to ABC.</strong> The analysis ranks by usage, so an item with stock on the shelf and no usage never appears. Run a separate report of items with no movement in 12 months.</p>",
        "<p><strong>Report by pool.</strong> A single list is fine for ranking. For review meetings, show raw materials, packaging and spares separately, because different people own each one.</p>",
        "<p><strong>Re-rate after equipment changes.</strong> A new filling line or a decommissioned mixer changes which spares are vital. Review criticality whenever the equipment list changes, and at least once a year.</p>",
        "<h2>Your checklist</h2>",
        ul(["List purchased items by pool: raw materials, packaging, spare parts", "Pull 12 months of consumption for materials, and three to five years for spares",
            "Run the ABC ranking by annual value", "Rate every item for criticality with production and maintenance",
            "Flag every vital item in class C and set a fixed minimum for it", "Check shelf life before raising any buffer", "Run a no-movement report for dead stock"]),
        tpl_box("The workbook for this series includes the Ridgeline example, with a criticality column and the combined policy for each item."),
        f"<p><strong>Next in the series:</strong> {P[4]} sets safety stock for a manufacturer, where raw material demand comes from the production schedule and spare parts need a different method altogether.</p>",
        CLOSE, DL_FORM])


# ================= Post 4 =================
def poisson_cdf(k, m):
    return sum(math.exp(-m) * m ** i / math.factorial(i) for i in range(k + 1))


def post4():
    M = [dict(sku="RM-01", name="Epoxy resin", lab="A, vital", u=180000, unit="kg", cost=4.2, sd=600, L=6, sL=1.5, sl=0.99),
         dict(sku="RM-03", name="Xylene solvent", lab="A, essential", u=210000, unit="L", cost=1.35, sd=700, L=1, sL=0.2, sl=0.95),
         dict(sku="RM-08", name="Dispersant additive", lab="C, vital", u=2400, unit="kg", cost=14, sd=12, L=8, sL=2, sl=0.99)]
    for e in M:
        e["d"] = e["u"] / 52; e["ss"] = ss3(e["d"], e["sd"], e["L"], e["sL"], e["sl"])
        e["rop"] = math.ceil(e["d"] * e["L"] + e["ss"] - 1e-9); e["val"] = round(e["ss"] * e["cost"]); e["wk"] = e["ss"] / e["d"]
    ep, xy, di = M
    assert (ep["ss"], ep["rop"], xy["ss"], xy["rop"], di["ss"], di["rop"]) == (12554, 33324, 1759, 5798, 229, 599)
    ratio = (ep["d"] ** 2 * ep["sL"] ** 2) / (ep["L"] * ep["sd"] ** 2); assert 12 < ratio < 13
    di_min = 600; di_rop = math.ceil(di["d"] * di["L"] + di_min - 1e-9); extra = (di_min - di["ss"]) * di["cost"]
    m_seal = 4 * 10 / 52; cov = [poisson_cdf(k, m_seal) * 100 for k in range(5)]
    assert cov[1] < 95 <= cov[2]
    m_gas = 60 * 2 / 52; gas_rop = next(k for k in range(30) if poisson_cdf(k, m_gas) >= 0.99); assert gas_rop == 6
    fmt = lambda v: f"{v:.0f}%" if v < 99 else f"{v:.1f}%"
    chart = bars([dict(top=fmt(cov[k]), v=cov[k], x1=f"{k} on hand", x2=money(k * 1850), hi=k == 2) for k in range(5)],
                 f"Two spare seals cover {cov[2]:.0f}% of lead times; one covers {cov[1]:.0f}%",
                 "Chance that stock lasts through a 10-week lead time, by number of SP-01 seals on hand when the order is placed",
                 "Bar chart of coverage by number of spare mechanical seals on hand: " + ", ".join(f"{k} gives {fmt(cov[k])}" for k in range(5)) + ". The target is 95%.",
                 "Illustrative data for a fictional manufacturer: SP-01, 4 used a year, 10-week lead time, $1,850 each. Poisson distribution.", target=95)
    vals = [ep["val"], xy["val"], di_min * di["cost"], 2 * 1850, 10 * 40]; tot = sum(vals)
    q = lambda e, v: f'{v:,} {e["unit"]}'
    return "\n".join([
        part(4),
        "<p>A distributor does not know what customers will order next week. A manufacturer usually does know what the plant will consume next week, because the production schedule says so. That one difference changes where the risk sits, and so where the buffer belongs.</p>",
        f"<p>In {P[2]} we set safety stock for a distributor using demand variability, lead time variability and a service level. In {P[3]} we classified 20 items at Ridgeline Coatings, a fictional manufacturer, by value and by criticality.</p>",
        f"<p>This post sets buffers for five of those items. For raw materials, the {P[2]} formula still works, but the supplier becomes the main source of risk. For spare parts, the formula does not work at all, and we need a different method.</p>",
        "<h2>What is uncertain, pool by pool</h2>",
        "<p>Safety stock exists to cover uncertainty. So the first question for each pool is: what do we not know?</p>",
        tbl([["Pool", "What is known", "What is uncertain", "Method that fits"],
             ["Raw materials and packaging", "Planned consumption, from the production schedule", "Schedule changes, supplier lead time, rejected lots", f"The {P[2]} formula (Method 3), with attention on lead time"],
             ["Spare parts", "Very little. Usage is a handful of units a year.", "When the next failure happens", "Poisson method, based on expected usage during one lead time"],
             ["Finished goods", "Order history", "Customer demand", f"The {P[2]} formula, exactly as for a distributor"]]),
        "<p>For raw materials, measure demand variability as the week-to-week swing in <strong>actual consumption</strong>. That captures schedule changes, rush orders and rework in one number.</p>",
        "<h2>Raw materials: three Ridgeline examples</h2>",
        f"<p>We use Method 3 from {P[2]}:</p>",
        formula("SS = Z &times; &radic;( L &times; &sigma;<sub>d</sub>&sup2; + d&sup2; &times; &sigma;<sub>L</sub>&sup2; )"),
        f"<p>The three materials were chosen because {P[3]} gave each a different policy.</p>",
        tbl([["Input"] + [f'{e["sku"]} {e["name"]}' for e in M],
             ["Class and criticality"] + [e["lab"] for e in M],
             ["Average weekly consumption"] + [q(e, round(e["d"])) for e in M],
             ["Standard deviation of weekly consumption"] + [q(e, e["sd"]) for e in M],
             ["Average lead time (weeks)"] + [e["L"] for e in M],
             ["Standard deviation of lead time (weeks)"] + [e["sL"] for e in M],
             ["Target service level"] + [f'{e["sl"]:.0%}' for e in M],
             ["Unit cost"] + [f'${e["cost"]:.2f}' for e in M],
             ["<strong>Safety stock</strong>"] + [f'<strong>{q(e, e["ss"])}</strong>' for e in M],
             ["Safety stock in weeks of use"] + [f'{e["wk"]:.1f}' for e in M],
             ["Safety stock value"] + [money(e["val"]) for e in M],
             ["Reorder point"] + [q(e, e["rop"]) for e in M]]),
        "<h3>What the numbers show</h3>",
        "<p><strong>Lead time drives the buffer, not consumption.</strong> For epoxy resin, the lead time term in the formula is more than twelve times the demand term. Consumption is steady; the supplier is not. A delivery that slips from six weeks to nine does far more damage than a busy week in the plant.</p>",
        f"<p><strong>A short lead time is worth more than a large buffer.</strong> Xylene and epoxy resin are both A items with similar weekly volumes. Xylene comes from a local supplier in one week and needs less than half a week of cover. Epoxy resin needs {ep['wk']:.1f} weeks. Shortening or stabilising a lead time is often cheaper than holding stock against it.</p>",
        f"<p><strong>Judgement still sits on top of the formula.</strong> The calculation gives {di['ss']} kg for the dispersant. Ridgeline holds a fixed minimum of {di_min} kg instead, as set out in {P[3]}. The reason is that the additive has a single supplier, and a plant shutdown at that supplier would not show up in any lead time history. The extra {di_min - di['ss']} kg costs {money(extra)}, and {di_min} kg is still only three months of use, well inside the product's shelf life.</p>",
        "<h2>Spare parts: a different method</h2>",
        f"<p>Ridgeline uses about four disperser mechanical seals a year. In most weeks the usage is zero; now and then it is one. There is no meaningful average week and no useful standard deviation, so the {P[2]} formula has nothing to work with.</p>",
        "<p>The question to ask instead is: <strong>how many could we need before a replacement arrives?</strong> The Poisson distribution answers it, and Excel has it built in.</p>",
        ol([f"<strong>Work out expected usage during one lead time.</strong> Annual usage &times; lead time in weeks &divide; 52. For the seal: 4 &times; 10 &divide; 52 = {m_seal:.2f}.",
            f"<strong>Find the coverage for each stock level.</strong> In Excel, <code>=POISSON.DIST(n, {m_seal:.2f}, TRUE)</code> gives the chance that usage during the lead time is n or fewer.",
            "<strong>Pick the smallest number that meets your target.</strong> That number is the reorder point."]),
        chart,
        f"<p>Ridgeline should reorder when two seals remain. One spare feels safe, but it fails in nearly one lead time out of five, and each failure means up to ten weeks with a disperser out of service. A third seal lifts coverage to {cov[3]:.1f}% for another $1,850. Whether that is worth it depends on what a week of lost production costs.</p>",
        f"<p>The gasket set works the same way. Usage is 60 a year with a two-week lead time, so expected usage per lead time is {m_gas:.1f} sets. A reorder point of six gives 99% coverage. Ridgeline rounds up to ten, because the extra four sets cost $160.</p>",
        "<h3>When the percentage misleads</h3>",
        "<p>Some vital spares fail once in ten years. The Poisson method will report that holding zero gives 95% coverage or better. Do not follow it. For these insurance spares, compare two numbers directly: the price of the part, and the cost of the outage if it fails with none on the shelf. If the outage costs more, hold one.</p>",
        "<h2>The five items together</h2>",
        tbl([["Item", f"Policy from {P[3]}", "Method", "Result", "Value held"],
             ["RM-01 Epoxy resin", "Tight control, protected supply", "Method 3 at 99%", f"Safety stock {q(ep, ep['ss'])}; reorder at {q(ep, ep['rop'])}", money(vals[0])],
             ["RM-03 Xylene solvent", "Tight control, lean stock", "Method 3 at 95%", f"Safety stock {q(xy, xy['ss'])}; reorder at {q(xy, xy['rop'])}", money(vals[1])],
             ["RM-08 Dispersant additive", "Never run out", "Fixed minimum, set above the Method 3 result", f"Minimum {di_min} kg; reorder at {di_rop} kg", money(vals[2])],
             ["SP-01 Mechanical seal", "Never run out", "Poisson at 95%", "Reorder when 2 remain", money(vals[3])],
             ["SP-02 Gasket set", "Never run out", "Poisson at 99%, rounded up", "Reorder when 10 remain", money(vals[4])]], wide=True),
        f"<p>The buffers total about {money(round(tot, -2))}. The epoxy resin accounts for {vals[0] / tot:.0%} of that, which is where a careful calculation earns its keep. The three vital C items are fully protected for {money(sum(vals[2:]))}.</p>",
        "<h3>Buffers that are not stock</h3>",
        "<p>Inventory is one way to cover risk, and often the most expensive. Before adding stock to an A item, consider the alternatives.</p>",
        ul(["<strong>Safety lead time.</strong> Schedule the delivery a week or two before the material is needed. This is simple to set in most planning systems and suits materials whose main risk is a late truck.",
            "<strong>A second qualified source.</strong> Qualifying a backup supplier for a vital material can remove weeks of lead time risk for the cost of some trial batches.",
            "<strong>Supplier-held stock.</strong> Ask the supplier to hold a reserve for you, or to place consignment stock on your site that you pay for as you use it.",
            "<strong>Shared spares.</strong> For expensive spares, check whether the equipment vendor stocks the part locally, or whether a sister plant holds one you can borrow."]),
        "<h2>Cautions for the plant floor</h2>",
        "<p><strong>Shelf life sets a ceiling.</strong> The most you will ever hold is roughly the reorder point plus one order quantity. Check that the plant will use that amount before it expires, and issue the oldest lot first.</p>",
        "<p><strong>Storage sets a ceiling too.</strong> A bulk solvent tank holds what it holds. Safety stock plus a full delivery has to fit in the tank, the silo or the rated flammables storage. If it does not, the answer is smaller and more frequent deliveries, not a bigger buffer.</p>",
        "<p><strong>Count rejected lots as late deliveries.</strong> If a resin lot fails incoming inspection, the usable material arrives when the replacement does. Record that as the lead time. Otherwise the history flatters the supplier and the buffer comes out too small.</p>",
        "<p><strong>Do not buffer the same risk four times.</strong> Purchasing adds safety stock, planning adds safety lead time, production pads the schedule and sales asks for finished goods cover. Each is reasonable alone. Together they tie up cash against one risk. Decide where the buffer sits and remove the others.</p>",
        "<p><strong>Take spare parts usage from maintenance records.</strong> Purchase history shows when spares were bought, not when they were fitted. Work orders give the true usage rate, and they also show which failures are becoming more frequent.</p>",
        "<h2>Your checklist</h2>",
        ul(["Pull weekly consumption and receipt history for every vital and class A material", "Calculate safety stock with Method 3, and note whether demand or lead time dominates",
            "Where lead time dominates, look at shortening or stabilising it before adding stock",
            "For each vital spare, work out expected usage during one lead time and apply the Poisson method",
            "Check every buffer against shelf life and storage capacity", "Agree where each buffer sits, and remove duplicates"]),
        tpl_box("The workbook for this series includes the Ridgeline materials and a spare parts calculator using the Poisson method."),
        "<h2>The series in one place</h2>",
        ol([f'<a href="{S1}.html">{T1}</a>', f'<a href="{S2}.html">{T2}</a>', f'<a href="{S3}.html">{T3}</a>', f"{T4} (this post)"]),
        "<p>The thread through all four is the same. Find out which items matter, work out what is uncertain about each one, and put the buffer where the risk is.</p>",
        CLOSE, DL_FORM])


ARTICLES = [
    dict(slug=S1, title=T1, body=post1, order=10, cover_label="Inventory",
         desc="ABC analysis ranks inventory by annual dollar usage so control goes where the money is. The five steps, a 20-item worked example and a free template.",
         tags=["ABC analysis", "inventory management", "Pareto analysis", "inventory classification", "cycle counting"], related=[S2, S3, S4]),
    dict(slug=S2, title=T2, body=post2, order=11, cover_label="Inventory",
         desc="Why \"two weeks of everything\" is the wrong buffer. Three ways to set safety stock and reorder points, with a worked example and a free Excel template.",
         tags=["safety stock", "reorder point", "service level", "lead time", "inventory management"], related=[S1, S3, S4]),
    dict(slug=S3, title=T3, body=post3, order=12, cover_label="Inventory",
         desc="In a plant, a $40 part can stop a line. How to add a criticality rating to ABC analysis for raw materials, packaging and spare parts, with an example.",
         tags=["ABC analysis", "criticality", "spare parts", "raw materials", "manufacturing inventory"], related=[S1, S2, S4]),
    dict(slug=S4, title=T4, body=post4, order=13, cover_label="Inventory",
         desc="Safety stock for raw materials, where supplier lead time drives the buffer, and for spare parts, where the Poisson method replaces the usual formula.",
         tags=["safety stock", "spare parts", "Poisson method", "raw materials", "lead time"], related=[S1, S2, S3]),
]


def main():
    for a in ARTICLES:
        body = a["body"]()
        words = len(re.sub(r"<svg.*?</svg>", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<svg.*?</svg>|<dialog.*?</dialog>", " ", body, flags=re.S))).split())
        out = dict(slug=a["slug"], title=a["title"], desc=a["desc"], cats=["operational-efficiency", "process-improvement"], tags=a["tags"],
                   body=body, date="2026-11-11", author="Quak Foo Lee", read=f"{max(1, round(words / 230))} min read", order=a["order"],
                   cover_label=a["cover_label"], related=a["related"])
        assert len(a["desc"]) <= 165, (a["slug"], len(a["desc"]))
        json.dump(out, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"], words, "words,", out["read"])


if __name__ == "__main__":
    main()
