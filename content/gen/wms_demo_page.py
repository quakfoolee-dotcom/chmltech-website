"""Chmltech WMS demo showcase page (wms-demo.html, V5.73).

The indexable entry point for the browser demo in WMS_demo/ (an app built from the
harbor-wms repository, noindex). Explains what visitors can try, a complete workflow with
deep links into the demo, and how the demo stores data in the browser.

Stand-alone: run `python3 content/gen/wms_demo_page.py`, then `python3 content/gen/seo_pass.py .`
It takes the shared header from contact.html and the call-to-action and footer from
ai-operating-system.html (as about_page.py does), so rerun it after menu or footer changes.
Screenshots: assets/media/wms-demo/ (taken from the demo at 1440x900 and 390x844).
"""
import html, json, os, re
import assetver

site = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..") + os.sep
TITLE = "Free WMS Demo: Try a Warehouse Management System | Chmltech"
DESC = "Try a free WMS demo in your browser: receive, pick, pack and ship sample orders. No sign-up, and the sample data stays in your browser."
H1 = "Try a warehouse management system (WMS) demo in your browser"
SLOGAN = "Receive, pick, pack and ship, with no sign-up."
DEMO = "WMS_demo/"
MEDIA = "assets/media/wms-demo/"
PART7 = "post/do-we-need-a-wms-yet-when-spreadsheets-stop-scaling.html"
WH1 = "post/were-out-of-space-or-are-we-warehouse-cube-utilization-and-slotting.html"
WL1 = "post/good-layout-bad-layout-what-travel-and-congestion-cost-an-sme-warehouse.html"
esc = lambda s: html.escape(s, quote=True)

MODULES = [
    ("Inventory and units", "Stock by location and lot, FIFO cost layers, reorder rules, transfers, cycle counts and traceability. Sample products come in Each, Pack of 3, Carton of 12 and Pallet of 480."),
    ("Purchasing and receiving", "Purchase orders, receiving with quality inspection holds, directed putaway, supplier returns and purchase cost reconciliation."),
    ("Sales and fulfilment", "Quotes, sales orders, kits, picking, packing and shipping, with customer returns and packing slips."),
    ("Manufacturing", "Multi-level bills of materials, manufacture orders, material issue, labour approval and a production schedule."),
    ("Accounting views", "Invoices, supplier bills, credits, payments, inventory journals, stock reconciliation and historical valuation."),
    ("Dashboards and reports", "Business and warehouse dashboards, demand forecasting and a report centre built from the same records."),
    ("Phone scanning screens", "Mobile pages for lookup, receive, move, pick, pack, ship and count, plus a document scanner that opens records by barcode."),
    ("Two layouts, four languages", "A classic record-and-tab layout or a modern layout, in English, French, Simplified Chinese or Traditional Chinese."),
]

STEPS = [
    ("Receive stock", "Open Purchasing and receive the sample purchase order: two cartons of the insulated travel bottle, which is 24 bottles.", "#purchasing", "Open Purchasing"),
    ("Check units of measure", "In Inventory, see how Each, Pack of 3, Carton of 12 and Pallet of 480 convert, and edit a unit if you like.", "#inventory", "Open Inventory"),
    ("Issue a sales order", "Open the draft sales order for two packs (6 bottles) and issue it. The order now needs stock reserved and picked.", "#orders", "Open Sales orders"),
    ("Pick the order", "In Picking, reserve (commit) the stock and work the pick through to Finished. A shipment is created.", "#picking", "Open Picking"),
    ("Pack and ship", "In Shipping, confirm packing and ship. On-hand stock falls by 6 bottles and the order is fulfilled.", "#shipping", "Open Shipping"),
    ("Start again", "Use Reset demo at the top of the demo whenever you want the original sample warehouse back.", "#overview", "Open the demo"),
]

STORAGE = [
    "Your warehouse records are saved in this browser on this device, not on a server.",
    "Other browsers, devices and visitors never see your changes, and devices do not sync.",
    "Reset demo restores the sample warehouse at any time. Clearing your browser data also removes it.",
    "You can download the demo data as a JSON file, or the product catalog as a CSV file.",
    "There are no accounts, passwords or automatic backups. Every visitor uses the Demo visitor role with full access.",
    "QuickBooks, EDI, carrier, email and payment connections are switched off. Please do not enter real customer data.",
    "Like the rest of the site, the demo uses Microsoft Clarity analytics to see which screens visitors use, with record details masked.",
]

FAQ = [
    ("Is the WMS demo free?", "Yes. It runs in your browser with no sign-up, download or payment."),
    ("Where is my demo data stored?", "Only in your browser's storage on the device you are using; your records are not saved on any server. Clearing your browser data or pressing Reset demo removes them. Like the rest of chmltech.com, the demo uses Microsoft Clarity analytics, with record details masked; see our Privacy page."),
    ("Can I try it on a phone or tablet?", "Yes. The main screens work on a phone, and the demo includes phone pages for scanning, receiving, picking, packing and counting. Each device keeps its own separate sample warehouse."),
    ("Can I use Chmltech WMS for my own warehouse?", "The demo runs on fictional records saved in your browser, so it is not set up for live operations. If you would like to talk about using Chmltech WMS in your business, or you are choosing between WMS options, book a call and we will help you work out what fits."),
    ("Which languages does it support?", "English, French, Simplified Chinese and Traditional Chinese. Choose the language at the top of the demo."),
]


def page():
    c = open(site + "contact.html", encoding="utf-8").read()
    a = open(site + "ai-operating-system.html", encoding="utf-8").read()
    head = assetver.strip(c[:c.index('<main id="main">')])
    tail = assetver.strip(a[a.index('<section class="cta">'):])
    # seo_pass.py rebuilds the canonical URL, og:url and structured data for this page.
    head = re.sub(r'<script type="application/ld\+json" data-seo="v1">.*?</script>\n?', "", head, flags=re.S)
    head = re.sub(r'<link rel="canonical"[^>]*>\n?', "", head)
    head = re.sub(r'<meta property="og:url"[^>]*>\n?', "", head)
    head = re.sub(r"<title>[^<]*</title>", f"<title>{esc(TITLE)}</title>", head)
    head = re.sub(r'(name="description" content=")[^"]*', lambda m: m.group(1) + esc(DESC), head)
    head = re.sub(r'(og:description" content=")[^"]*', lambda m: m.group(1) + esc(DESC), head)
    head = re.sub(r'(og:title" content=")[^"]*', lambda m: m.group(1) + esc(TITLE), head)
    head = re.sub(r'(twitter:title" content=")[^"]*', lambda m: m.group(1) + esc(TITLE), head)
    head = re.sub(r'(twitter:description" content=")[^"]*', lambda m: m.group(1) + esc(DESC), head)
    head = head.replace("https://www.chmltech.com/assets/img/chmltech-mark.png", f"https://www.chmltech.com/{MEDIA}chmltech-wms-og.jpg")
    head = head.replace(' aria-current="page"', "")
    app = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Chmltech WMS demo",
           "applicationCategory": "BusinessApplication", "operatingSystem": "Web browser",
           "url": "https://www.chmltech.com/WMS_demo/", "image": f"https://www.chmltech.com/{MEDIA}chmltech-wms-overview.webp",
           "description": DESC, "inLanguage": ["en", "fr", "zh-Hans", "zh-Hant"],
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CAD"},
           "publisher": {"@id": "https://www.chmltech.com/#organization"}}
    head = head.replace("</head>", '<script type="application/ld+json">' + json.dumps(app, ensure_ascii=False) + "</script>\n</head>", 1)

    modules = "".join(f'<article class="card wd-mod"><h3>{esc(t)}</h3><p class="muted">{esc(d)}</p></article>' for t, d in MODULES)
    steps = "".join(f'<li><b>{i:02d}</b><h3>{esc(t)}</h3><p>{esc(d)}</p><a class="more" href="{DEMO}{h}">{esc(l)} →</a></li>' for i, (t, d, h, l) in enumerate(STEPS, 1))
    storage = "".join(f"<li>{esc(x)}</li>" for x in STORAGE)
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(x)}</p></details>" for q, x in FAQ)
    main = f'''<main id="main">
<style>
.wd-hero{{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:56px;align-items:center}}
.wd-shot{{margin:0;border-radius:12px;overflow:hidden;box-shadow:0 30px 60px -28px rgba(0,0,0,.75);border:1px solid #234A80;background:#0E2C55}}
.wd-shot img{{display:block;width:100%;height:auto}}
.wd-facts{{display:flex;flex-wrap:wrap;gap:8px 18px;margin:0;padding:0;list-style:none;font-size:14.5px;color:var(--on-dark)}}
.wd-facts li::before{{content:"✓ ";color:var(--green);font-weight:700}}
.wd-mod h3{{font-size:19px}}
.wd-steps{{grid-template-columns:repeat(3,1fr)}}
.wd-steps li .more{{display:inline-block;margin-top:10px;font-weight:600}}
.wd-gallery{{display:grid;grid-template-columns:1fr 1fr .5fr;gap:20px;align-items:start}}
.wd-gallery figure{{margin:0}}
.wd-gallery img{{display:block;width:100%;height:auto;border-radius:10px;border:1px solid var(--line);box-shadow:0 18px 40px -26px rgba(7,28,61,.55)}}
.wd-gallery figcaption{{font-size:14px;color:var(--muted);margin-top:8px}}
@media (max-width:900px){{.wd-hero{{grid-template-columns:1fr;gap:36px}}.wd-steps{{grid-template-columns:1fr}}.wd-gallery{{grid-template-columns:1fr}}.wd-gallery figure:last-child{{max-width:300px}}}}
</style>
<section class="page-hero dark">
  <div class="container wd-hero">
    <div class="stack-lg">
      <p class="crumbs"><a href="index.html">Home</a> / <a href="solutions.html">Solutions</a> / WMS demo</p>
      <p class="eyebrow">Free interactive demo · Chmltech WMS</p>
      <h1 class="h-xl" data-kw="1">{esc(H1)}</h1><p class="hero-slogan">{esc(SLOGAN)}</p>
      <p class="lead">Chmltech WMS is a working warehouse management system with fictional sample data. Receive a purchase order, pick and ship a sales order, and watch stock, locations and costs update as you go.</p>
      <div class="btn-row"><a class="btn" href="{DEMO}">Launch the WMS demo</a><a class="btn btn-ghost-dark" href="#workflow">See a 10-minute workflow</a></div>
      <ul class="wd-facts"><li>No sign-up</li><li>Fictional sample data</li><li>Saved only in your browser</li><li>Works on a phone</li></ul>
    </div>
    <figure class="wd-shot"><img src="{MEDIA}chmltech-wms-overview.webp" width="1440" height="900" alt="Chmltech WMS demo overview screen: on-hand quantity, open orders, items ready to ship and low-stock items for the sample Vancouver warehouse" fetchpriority="high"></figure>
  </div>
</section>
<section class="section"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">What you can try</p><h2 class="h-lg">A full warehouse system, not a slideshow.</h2></div><p>Every screen works with the same sample records, so a change in one module shows up everywhere else.</p></div>
  <div class="grid grid-4">{modules}</div>
</div></section>
<section class="section sand" id="workflow" style="scroll-margin-top:84px"><div class="container">
  <div class="stack" style="max-width:760px;margin-bottom:48px"><p class="eyebrow">Try it in 10 minutes</p><h2 class="h-lg">Follow one order from the dock to the customer.</h2><p class="muted" style="font-size:17px">Each link opens the demo at that screen. The demo's help button (?) shows the same walkthrough.</p></div>
  <ol class="steps wd-steps">{steps}</ol>
</div></section>
<section class="section"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Screens</p><h2 class="h-lg">On a desktop and on the warehouse floor.</h2></div></div>
  <div class="wd-gallery">
    <figure><img src="{MEDIA}chmltech-wms-inventory.webp" width="1200" height="750" loading="lazy" alt="Chmltech WMS inventory screen in the modern layout, listing sample products with on-hand, allocated, reserved and available quantities"><figcaption>Inventory in the modern layout.</figcaption></figure>
    <figure><img src="{MEDIA}chmltech-wms-orders.webp" width="1200" height="750" loading="lazy" alt="Chmltech WMS sales order in the classic layout, with order items, status steps and workflow guidance"><figcaption>A sales order in the classic layout.</figcaption></figure>
    <figure><img src="{MEDIA}chmltech-wms-mobile.webp" width="585" height="1266" loading="lazy" alt="Chmltech WMS phone screen for warehouse scanning, with lookup, move, receive, pick, pack, ship and count buttons"><figcaption>Phone scanning screen.</figcaption></figure>
  </div>
</div></section>
<section class="section dark"><div class="container feature-split">
  <div class="stack-lg"><p class="eyebrow">Your data</p><h2 class="h-lg">The demo runs entirely in your browser.</h2>
  <p class="lead">The demo app has no server. Your sample warehouse lives in your own browser, so you can experiment freely. <a href="privacy.html" style="color:inherit">Privacy</a>.</p>
  <div class="btn-row"><a class="btn" href="{DEMO}">Launch the WMS demo</a></div></div>
  <ul class="list-check" style="font-size:16.5px">{storage}</ul>
</div></section>
<section class="section"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Is it time for a WMS?</p><h2 class="h-lg">Work out whether you need one.</h2></div></div>
  <div class="grid grid-3">
    <article class="card"><span class="tag tag-green">Article</span><h3 style="font-size:20px">Do we need a WMS yet?</h3><p class="muted">When paper, an ERP module, a cloud WMS or an enterprise system pays, costed from 50 to 1,200 orders a day.</p><a class="more" href="{PART7}">Read Part 7 →</a></article>
    <article class="card"><span class="tag tag-green">Free tool</span><h3 style="font-size:20px">Digital Assessment</h3><p class="muted">Answer a few questions about your business and see which software categories, including WMS, fit your needs.</p><a class="more" href="digital-assessment.html">Start the assessment →</a></article>
    <article class="card"><span class="tag tag-green">Free course</span><h3 style="font-size:20px">Choosing ERP and business software</h3><p class="muted">Requirements, shortlists, scripted demos, scoring and total cost of ownership, in 16 short lessons.</p><a class="more" href="challenge-page/choosing-erp-and-business-software.html">Start the course →</a></article>
  </div>
  <p class="muted" style="margin-top:22px">More on running a better warehouse: the <a href="{WH1}">warehouse operations series</a> and the <a href="{WL1}">warehouse layout series</a>, or our <a href="distribution-and-warehousing.html">distribution and warehousing</a> services.</p>
</div></section>
<section class="section sand"><div class="container">
  <div class="section-head"><div class="stack"><p class="eyebrow">Questions</p><h2 class="h-lg">Frequently asked</h2></div></div>
  <div class="faq">{faq}</div>
</div></section>
'''
    out = head + main + tail
    open(site + "wms-demo.html", "w", encoding="utf-8").write(out)
    print("wrote wms-demo.html", len(out))


if __name__ == "__main__":
    page()
