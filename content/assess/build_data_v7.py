"""Digital Assessment data, Draft V7: V5 data plus red-team corrections (2026-11-19).

Runs build_data_v5.py, then applies the corrections accepted from the independent red-team review
(4 reviewers: ERP/WMS, operations, front office, IT/AI + scoring logic). Accepted = high or medium
confidence with evidence. Claims the reviewers could not verify are kept but flagged ("unv").
Writes content/assess/assess_data.json and content/assess/redteam_v7_log.json.

Run from the repo root:  python3 content/assess/build_data_v7.py
"""
import json, pathlib, runpy

ROOT = pathlib.Path(__file__).resolve().parents[2]
runpy.run_path(str(ROOT / 'content/assess/build_data_v5.py'), run_name='__main__')
OUT = ROOT / 'content/assess/assess_data.json'
D = json.loads(OUT.read_text())
D['version'] = 'Draft V7'
LOG = []
# evidence links from the reviewers' own findings take precedence over any default link below
EV = {}
for f in ('findings_A.json', 'findings_B.json', 'findings_C.json'):
    fp = pathlib.Path('/home/claude/redteam') / f
    if fp.exists():
        for x in json.loads(fp.read_text())['findings']:
            if x.get('evidence_url'):
                key = (x.get('workflow_or_field') or x.get('field') or '').split(':')[-1].strip().lower()
                EV[(x['product_id'], key)] = x['evidence_url']
fp = pathlib.Path('/home/claude/redteam/findings_D.json')
if fp.exists():
    for x in json.loads(fp.read_text())['data_findings']:
        if x.get('evidence_url'): EV[(x['product_id'], '*')] = x['evidence_url']
def ev(pid, key, default):
    return EV.get((pid, key.lower()), EV.get((pid, '*'), default))

CAT = {c['id']: c for c in D['categories']}
WF = {w['id']: w for w in D['erp']['workflows']}
def find(pid, scope):
    if scope == 'erp': return next(v for v in D['erp']['vendors'] if v['id'] == pid)
    if scope == 'wms': return next(v for v in D['wms']['vendors'] if v['id'] == pid)
    return next(p for p in D['products'] if p['id'] == pid and p['cat'] == scope)
def capidx(scope, wf, capname):
    caps = WF[wf]['caps'] if scope == 'erp' else (CAT['wms']['caps'] if scope == 'wms' else CAT[scope]['caps'])
    return next(i for i, c in enumerate(caps) if c['n'] == capname)
def score(pid, scope, capname, new, why, src, wf=None, rev=''):
    p = find(pid, scope); i = capidx(scope, wf, capname)
    arr = p['s'][wf] if scope == 'erp' else (p['s']['wm'] if scope == 'wms' else p['s'])
    old = arr[i]; arr[i] = new
    LOG.append({'product': p['name'], 'where': (WF[wf]['name'] if wf else CAT.get(scope, {}).get('name', scope)) + ': ' + capname, 'from': old, 'to': new, 'why': why, 'evidence': ev(pid, capname, src), 'reviewer': rev})
def field(pid, scope, key, new, why, src, rev=''):
    p = find(pid, scope); old = p.get(key); p[key] = new
    LOG.append({'product': p['name'], 'where': key, 'from': old, 'to': new, 'why': why, 'evidence': ev(pid, key, src), 'reviewer': rev})
def rc_add(pid, scope, text, why, src, rev='', replace=False):
    p = find(pid, scope)
    if isinstance(p['rc'], dict):
        old = p['rc']['hidden']; p['rc']['hidden'] = text if replace else old.rstrip('.') + '. ' + text
        new = p['rc']['hidden']
    else:
        old = p['rc']; p['rc'] = text if replace else old.rstrip('.') + '. ' + text; new = p['rc']
    LOG.append({'product': p['name'], 'where': 'Reality Check', 'from': old, 'to': new, 'why': why, 'evidence': ev(pid, 'rc', src), 'reviewer': rev})
def unv(pid, scope, capname, rev=''):
    p = find(pid, scope); p.setdefault('unv', []).append(capname)

# ---------------- Reviewer A: ERP and WMS ----------------
A = 'A ERP/WMS'
field('odoo', 'erp', 'price', 2, 'First-year licence plus implementation is about CAD 19–41K at 10 users and 80–180K at 50 users.', 'https://octurasolutions.com/resources/odoo-pricing-2026-complete-transparent-breakdown-us-canada', A)
score('odoo', 'erp', 'Canadian tax and payroll links', 2, 'Odoo has no official Canadian payroll localization (v18/v19).', 'https://www.odoo.com/documentation/18.0/th/applications/hr/payroll/payroll_localizations.html', 'core', A)
score('odoo', 'erp', 'Marketplace and store orders', 2, 'Shopify connectors are third-party apps.', 'https://apps.odoo.com/apps/modules/19.0/shopify', 'om', A)
field('invera', 'erp', 'name', 'Invera INVEX (formerly stratixERP)', 'A June 2026 release calls Invera "the provider of the INVEX metal ERP platform"; confirm which product new customers receive.', 'https://www.prweb.com/releases/invex-ai-introducing-ivy-the-intelligence-layer-for-metal-erp-302790550.html', A)
field('m1', 'erp', 'deploy', ['Cloud', 'On-premise'], 'ECI M1 is also offered on-premise.', 'https://www.ecisolutions.com/products/m1/', A)
field('infor-csi', 'erp', 'name', 'Infor SyteLine (CloudSuite Industrial)', 'Infor now markets the product as SyteLine; on-premise is for existing customers.', 'https://www.infor.com/products/syteline', A)
score('ifs', 'erp', 'Nesting and CAD link', 1, 'Nesting is an external tool; CAD links are partner apps.', 'https://ifs.com/industries/manufacturing', 'mf', A)
score('sagex3', 'erp', 'Route sales and delivery', 1, 'Route delivery is not a native strength (independent review).', 'https://www.sage.com/en-ca/sage-business-cloud/sage-x3/', 'fd', A)
score('sagex3', 'erp', 'Nutrition and label data', 1, 'Nutrition labelling is done through partner tools such as LabelCalc.', 'https://www.sage.com/en-ca/sage-business-cloud/sage-x3/', 'fb', A)
for wfid, cap in (('fd', 'Catch weight'), ('fb', 'Catch weight')):
    score('bc', 'erp', cap, 1, 'Catch weight in Business Central comes from AppSource ISV apps.', 'https://appsource.microsoft.com/en-us/marketplace/apps?product=dynamics-365-business-central&search=catch%20weight', wfid, A)
    score('sapb1', 'erp', cap, 1, 'Catch weight in SAP Business One comes from the Produmex add-on.', 'https://www.boyum-it.com/produmex/', wfid, A)
score('bc', 'erp', 'Canadian tax and payroll links', 2, 'The Canadian localization has no payroll; payroll comes from partners.', 'https://learn.microsoft.com/en-us/dynamics365/business-central/localfunctionality/canada/canada-local-functionality', 'core', A)
score('intacct-erp', 'erp', 'Equipment costing', 1, 'Equipment costing is documented in the companion Sage Construction Management product.', 'https://www.intacct.com/ia/docs/en_US/releasenotes/2025/2025_Release_4/Construction/2025-R4-construction-all-changes.htm', 'cx', A)
score('deacom', 'erp', 'Nutrition and label data', 2, 'Nutrition panels are available but need configuration.', 'https://www.deacom.com/', 'fb', A)
score('mecalux', 'wms', 'Packing and carrier integration', 3, 'Multi-carrier shipping is a native Easy WMS module.', 'https://www.mecalux.com/software/easy-wms', None, A)
field('brightpearl', 'erp', 'months', '3–5', 'Average go-live is about 120 days.', 'https://brightpearl.com/', A)
field('restaurant365', 'erp', 'canada', 'US company (Irvine); listed for Canadian buyers', 'The cited page does not mention Canada; the Capterra Canada listing does.', 'https://www.capterra.ca/software/139768/restaurant365', A)
field('restaurant365', 'erp', 'src', 'https://www.capterra.ca/software/139768/restaurant365', 'Source replaced with a page that covers the Canadian market.', 'https://www.capterra.ca/software/139768/restaurant365', A)
for pid, wfid, cap in (('odoo', 'om', '3PL connections'), ('odoo', 'rp', 'Line and rate scheduling'), ('sagex3', 'fd', 'Temperature zones'), ('netsuite', 'om', '3PL connections'),
                       ('netsuite', 'lg', 'Multi-client inventory'), ('intacct-erp', 'hc', 'Practitioner compensation'), ('intacct-erp', 'hs', 'Franchise and royalties'),
                       ('acumatica', 'om', '3PL connections'), ('syspro', 'fd', 'Temperature zones'), ('epicor', 'fs', 'Technician pay and commissions'), ('epicor', 'fs', 'Field invoicing and payments')):
    unv(pid, 'erp', WF[wfid]['name'] + ': ' + cap, A)

# ---------------- Reviewer B: operations ----------------
B = 'B Operations'
field('inflow', 'inv', 'canada', 'Canadian company (Toronto)', 'inFlow (Archon Systems) is based in Toronto, not Winnipeg.', 'https://www.inflowinventory.com/about', B)
field('craftybase', 'mrp', 'name', 'Stocksmith (formerly Craftybase)', 'Rebranded 1 Jul 2026; craftybase.com redirects to stocksmith.io.', 'https://stocksmith.io/', B)
score('craftybase', 'mrp', 'QuickBooks or Xero link', 1, 'QuickBooks sync only on the top Growth plan; no Xero.', 'https://stocksmith.io/pricing', rev=B)
score('craftybase', 'mrp', 'Production scheduling', 2, 'Production runs can be scheduled.', 'https://stocksmith.io/pricing', rev=B)
score('craftybase', 'mrp', 'Lot and serial', 3, 'Batch and lot tracking is native.', 'https://stocksmith.io/pricing', rev=B)
rc_add('katana', 'mrp', 'Katana now sells a Free plan and a custom-quoted Advantage contract; routings are included in both. Model the custom quote and the integrations you need.', 'Pricing model changed; routings are no longer a paid add-on.', 'https://katanamrp.com/pricing-plans/', B, replace=True)
score('fishbowlmfg', 'mrp', 'Material planning (MRP)', 3, 'Advanced Manufacturing includes MRP.', 'https://www.fishbowlinventory.com/news/', rev=B)
score('fishbowlmfg', 'mrp', 'Production scheduling', 2, 'Advanced Manufacturing includes production scheduling.', 'https://www.fishbowlinventory.com/news/', rev=B)
field('fishbowlmfg', 'mrp', 'price', 2, 'From US$675/month plus a mandatory implementation package and 6–8 weeks of training.', 'https://www.fishbowlinventory.com/pricing', B)
rc_add('fishbowlmfg', 'mrp', 'Advanced Manufacturing includes MRP and production scheduling; AI manufacturing features launched Feb–Mar 2026. Budget for the mandatory implementation package and 6–8 weeks of training.', 'Previous text understated planning features.', 'https://www.fishbowlinventory.com/news/', B, replace=True)
score('buildertrend', 'cpm', 'RFIs and submittals', 3, 'RFIs and submittals are built in.', 'https://buildertrend.com/project-management/rfis/', rev=B)
score('fieldwire', 'cpm', 'Change orders', 3, 'Change orders built in since Nov 2023.', 'https://www.fieldwire.com/change-orders/', rev=B)
score('fieldwire', 'cpm', 'RFIs and submittals', 3, 'RFIs and submittals on the Business Plus plan.', 'https://www.fieldwire.com/pricing/', rev=B)
TC = 'https://tc.canada.ca/en/road-transportation/electronic-logging-devices/list-electronic-logging-devices'
field('samsara', 'tms', 'canada', 'Serves Canadian fleets; Transport Canada-certified ELD (current certificates)', 'Active certificates on the Transport Canada list.', TC, B)
rc_add('samsara', 'tms', "Samsara's original Canadian ELD certificates were revoked in Mar–Apr 2026 and replaced; confirm your device's ELD ID is on the active list.", 'Device-specific certification caveat.', TC, B)
rc_add('isaac', 'tms', 'Older ISAAC certificate numbers show as revoked (Jun 2026) while current InMetrics devices are active; confirm the exact device and ELD ID.', 'Device-specific certification caveat.', TC, B)
score('geotab', 'tms', 'Fuel and IFTA', 3, 'The IFTA report is built into MyGeotab.', 'https://www.geotab.com/fleet-management-solutions/ifta-reporting/', rev=B)
rc_add('geotab', 'tms', 'Active Transport Canada certificates include GOELD1/GOELD2 and GO10 (Android/iOS, May 2026); many features come from Marketplace partners.', 'Sharper certification detail.', TC, B, replace=True)
score('servicetitan', 'fsm', 'GPS and routing', 1, 'GPS comes through Fleet Pro, sold separately.', 'https://www.servicetitan.com/features/fleet-pro', rev=B)
rc_add('servicetitan', 'fsm', 'GPS/fleet (Fleet Pro), marketing and other Pro modules are priced separately.', 'Scores implied everything was included.', 'https://www.servicetitan.com/features/fleet-pro', B)
score('cin7', 'inv', 'Barcode scanning', 3, 'Scanning is included in all plans.', 'https://cin7.com/pricing/', rev=B)
rc_add('cin7', 'inv', 'MRP is an add-on on the Standard plan and advanced production is an add-on on all tiers.', 'Helps model cost.', 'https://cin7.com/pricing/', B)
score('zohoinv', 'inv', 'Kits and light assembly', 3, 'Composite items and assemblies are native.', 'https://www.zoho.com/inventory/features/', rev=B)
score('zohoinv', 'inv', 'Lot and serial', 3, 'Batch and serial tracking are native.', 'https://www.zoho.com/inventory/features/', rev=B)
field('mrpeasy', 'mrp', 'size', ['s', 'm'], 'Plans scale beyond 25 users.', 'https://www.mrpeasy.com/pricing/', B)
score('jobber', 'fsm', 'Job costing', 3, 'Job costing is built in.', 'https://getjobber.com/features/job-costing/', rev=B)
field('buildium', 'prop', 'canada', 'Canadian GST automation and EFT rent payments; tenant screening in Canada unconfirmed', 'The cited source showed no Canadian features; GST and EFT confirmed elsewhere.', 'https://learn.buildium.com/ca/gst/', B)
field('buildium', 'prop', 'src', 'https://learn.buildium.com/ca/gst/', 'Source replaced with a Canadian page.', 'https://learn.buildium.com/ca/gst/', B)
score('buildium', 'prop', 'Leasing and screening', 2, 'Screening runs through TransUnion US; no source confirms it works in Canada.', 'https://learn.buildium.com/ca/gst/', rev=B)
score('buildium', 'prop', 'Online rent collection', 2, 'EFT ePay in Canada; fewer payment options than the US version.', 'https://learn.buildium.com/ca/gst/', rev=B)
rc_add('yardibreeze', 'prop', 'In Canada it is marketed as Yardi Breeze Premier (yardibreeze.ca); Canadian pricing is not published, so get a Canadian quote.', '"Higher monthly minimum" was an inference.', 'https://www.yardibreeze.ca/', B, replace=True)
score('yardibreeze', 'prop', 'Canadian set-up', 3, 'Canadian site and edition.', 'https://www.yardibreeze.ca/', rev=B)
score('yardibreeze', 'prop', 'Leasing and screening', 2, 'Screening options differ in Canada.', 'https://www.yardibreeze.ca/', rev=B)
field('juvonno', 'clinic', 'canada', 'Canadian company (Oak Bluff, Manitoba)', 'Head office is in Oak Bluff, near Winnipeg.', 'https://juvonno.com/', B)
score('juvonno', 'clinic', 'Telehealth', 3, 'Telehealth is built in.', 'https://juvonno.com/', rev=B)
score('oscarpro', 'clinic', 'Online booking', 1, 'Online booking is through add-ons.', 'https://well.company/oscar-pro/', rev=B)
field('oscarpro', 'clinic', 'canada', 'Canadian (WELL Health, Vancouver); OntarioMD-certified, confirm certification in your province', 'The vendor page cites only OntarioMD certification.', 'https://well.company/oscar-pro/', B)
field('procore', 'cpm', 'canada', 'Canadian office (Toronto) and Canadian customers', 'Toronto office confirmed.', 'https://www.procore.com/en-ca', B)
unv('oscarpro', 'clinic', 'Canadian data hosting', B); unv('oscarpro', 'clinic', 'Telehealth', B)

# ---------------- Reviewer C: front office ----------------
C = 'C Front office'
score('wagepoint', 'payroll', 'Quebec support', 3, 'Revenu Québec remittances, QPP/QPIP/CNESST/HSF and French are supported.', 'https://www.wagepoint.com/quebec-payroll/', rev=C)
score('wagepoint', 'payroll', 'Time tracking', 2, 'Timesheets come standard.', 'https://www.wagepoint.com/', rev=C)
rc_add('wagepoint', 'payroll', 'Payroll-first: timesheets and time off are included, and Quebec payroll is supported. HR records, onboarding and benefits still need other tools.', 'Previous text was outdated.', 'https://www.wagepoint.com/quebec-payroll/', C, replace=True)
field('emphero', 'payroll', 'canada', 'Australian-owned (acquired Toronto-based Humi in 2025); Humi is hosted in Canada; on the main platform, HR data is held in Canada and Australia', '"Built in Canada; Canadian data hosting" overstated it.', 'https://employmenthero.com/en-ca/about-humi/', C)
score('emphero', 'payroll', 'Quebec support', 3, 'Humi by Employment Hero handles QPP/QPIP and French RL-1 slips.', 'https://employmenthero.com/en-ca/about-humi/', rev=C)
for pid in ('bamboo', '7shifts'):
    score(pid, 'payroll', 'Canadian payroll', 1, 'Canadian payroll through partner integrations (legend: 1 = partner app).', 'https://www.bamboohr.com/integrations/' if pid == 'bamboo' else 'https://www.7shifts.com/integrations/', rev=C)
score('bamboo', 'payroll', 'T4s and ROEs', 1, 'Through the partner payroll provider.', 'https://www.bamboohr.com/integrations/', rev=C)
score('pipedrive', 'crm', 'Email and sequences', 3, 'Sequences are built in on Growth and higher plans.', 'https://www.pipedrive.com/en/features/sequences', rev=C)
rc_add('pipedrive', 'crm', 'Simple pipeline tool. Quotes from the product catalogue (Smart Docs) are included on the higher plans and an add-on on the entry plans.', 'Previous text was partly wrong.', 'https://www.pipedrive.com/en/features/smart-docs', C, replace=True)
score('hubspot', 'crm', 'Quotes', 3, 'Quotes from the product library are native.', 'https://www.hubspot.com/products/sales/quotes', rev=C)
field('zohocrm', 'crm', 'canada', 'Canadian data centres (Toronto and Montreal, since 2023)', 'Canadian data residency was missing.', 'https://www.businesswire.com/news/home/20231102557441/en/Zoho-Launches-New-Data-Centers-in-Canada-Offering-Local-Businesses-Fast-Reliable-and-Secure-Access-to-their-Data', C)
score('mailchimp', 'mkt', 'Social scheduling', 2, 'Schedules Facebook, Instagram and X posts.', 'https://mailchimp.com/features/social-media-scheduling/', rev=C)
field('bigcommerce', 'ecom', 'name', 'BigCommerce B2B Edition', 'Parent company renamed Commerce.com in Aug 2025.', 'https://www.bigcommerce.com/b2b-ecommerce/', C)
field('shopify', 'ecom', 'size', ['s', 'm'], 'Customer-specific B2B pricing and larger firms need Shopify Plus (about US$2,300/month).', 'https://help.shopify.com/en/manual/b2b/getting-started/plan-features', C)
rc_add('shopify', 'ecom', 'Customer-specific B2B price lists and larger operations need Shopify Plus (from about US$2,300/month).', 'Price band only holds for small and mid-size use.', 'https://help.shopify.com/en/manual/b2b/getting-started/plan-features', C)
score('square', 'pos', 'Tables and menus', 3, 'Square for Restaurants (Canada) has tables, modifiers and kitchen displays.', 'https://squareup.com/ca/en/point-of-sale/restaurants/pricing', rev=C)
score('square', 'pos', 'Multi-location', 3, 'Multi-location management is native.', 'https://squareup.com/ca/en/point-of-sale/restaurants/pricing', rev=C)
rc_add('square', 'pos', "Not compatible with Quebec's mandatory WEB-SRM restaurant billing: Quebec restaurants need a certified partner integration.", 'Compliance blocker for Quebec restaurants.', 'https://squareup.com/ca/en/point-of-sale/restaurants/pricing', C)
field('lsretail', 'pos', 'price', 1, 'Published plans US$89–289/month.', 'https://www.lightspeedhq.com/pos/retail/pricing/', C)
score('lsresto', 'pos', 'Online store link', 2, 'First-party Order Anywhere online ordering.', 'https://lightspeedhq.com/pos/restaurant/order-anywhere/', rev=C)
rc_add('lsresto', 'pos', "Lightspeed Restaurant (K-Series) is certified for Quebec's WEB-SRM restaurant billing.", 'Positive compliance fact.', 'https://www.revenuquebec.ca/fr/partenaires/produits-autorises/systemes-denregistrement-des-ventes-certifies/sev-compatibles-avec-le-mev-web-restauration/details/lightspeed-restaurant-pos-k/26420/', C)
field('mindbody', 'booking', 'price', 1, 'Starter plan US$79/month.', 'https://www.mindbodyonline.com/business/pricing', C)
rc_add('mindbody', 'booking', 'Now part of Playlist (Mindbody, ClassPass, Booker), which agreed to merge with EGYM in Jan 2026.', 'Ownership change.', 'https://www.playlist.com/press/playlist-and-egym-announce-agreement-merge-and-785-million-new-equity-investments-bringing', C)
score('intacct', 'acct', 'Inventory', 2, "Sage's own inventory module.", 'https://www.sage.com/en-ca/sage-business-cloud/intacct/', rev=C)
score('freshbooks', 'acct', 'Inventory', 1, 'Basic stock tracking exists.', 'https://www.freshbooks.com/en-ca/', rev=C)
field('sage50', 'acct', 'deploy', ['On-premise'], 'Desktop software; cloud access is an add-on.', 'https://www.sage.com/en-ca/products/sage-50/', C)
score('monday', 'psa', 'Time tracking', 2, 'Time tracking built in on Pro.', 'https://monday.com/pricing', rev=C)
rc_add('dayforce', 'payroll', 'Privately owned by Thoma Bravo since Feb 2026.', 'Ownership change.', 'https://www.thomabravo.com/press-releases/thoma-bravo-completes-acquisition-of-dayforce', C)
rc_add('clio', 'psa', 'Priced per user, so larger firms land in a higher cost band. Still independent; completed the vLex acquisition in Nov 2025.', 'Price band 1 only holds for small firms (reviewer inference from per-user pricing).', 'https://www.clio.com/about/press/clio-completes-landmark-1b-vlex-acquisition-series-g-5b-valuation/', C)

# ---------------- Reviewer D: IT and AI data ----------------
DR = 'D IT/AI'
field('gws', 'collab', 'canada', 'No Canadian data region (Workspace data regions are US or EU only)', 'Previous claim was false.', 'https://workspaceupdates.googleblog.com/2026/06/gemini-app-data-regions-support.html', DR)
score('gws', 'collab', 'Canadian data residency', 0, 'No Canadian region.', 'https://workspaceupdates.googleblog.com/2026/06/gemini-app-data-regions-support.html', rev=DR)
field('dropbox', 'collab', 'canada', 'Data stored in the US (EU, UK, Australia, Japan for eligible teams); no Canadian region', 'Previous claim was false.', 'https://help.dropbox.com/security/physical-location-data-storage', DR)
score('dropbox', 'collab', 'Canadian data residency', 0, 'No Canadian region.', 'https://help.dropbox.com/security/physical-location-data-storage', rev=DR)
field('looker', 'bi', 'name', 'Data Studio (formerly Looker Studio)', 'Renamed in April 2026.', 'https://cloud.google.com/blog/products/data-analytics/looker-studio-is-data-studio', DR)
field('copilot', 'ai', 'src', 'https://www.microsoft.com/microsoft-365/try-copilot/business', 'Vendor page confirms the promotion runs to Dec 31, 2026 (old source said June 30).', 'https://www.microsoft.com/microsoft-365/try-copilot/business', DR)
field('copilot', 'ai', 'canada', 'Data at rest in Canadian Microsoft 365 data centres; in-country Copilot processing for Canada announced for 2027', 'Canada facts instead of a plan name.', 'https://www.microsoft.com/en-us/microsoft-365/blog/2025/11/04/microsoft-offers-in-country-data-processing-to-15-countries-to-strengthen-sovereign-controls-for-microsoft-365-copilot/', DR)
field('chatgpt', 'ai', 'src', 'https://openai.com/index/premium-seats-chatgpt-business', 'Vendor source replaces a third-party blog.', 'https://openai.com/index/premium-seats-chatgpt-business', DR)
field('chatgpt', 'ai', 'canada', 'No Canadian data residency on Business (available on Enterprise and Edu)', 'Canada facts instead of a plan name.', 'https://openai.com/index/expanding-data-residency-access-to-business-customers-worldwide', DR)
field('claude', 'ai', 'src', 'https://support.claude.com/en/articles/9266767-what-is-the-team-plan', 'Vendor source replaces a third-party guide.', 'https://support.claude.com/en/articles/9266767-what-is-the-team-plan', DR)
field('claude', 'ai', 'canada', 'No Canadian data residency option published for Team', 'Canada facts instead of a plan name.', 'https://support.claude.com/en/articles/9266767-what-is-the-team-plan', DR)
rc_add('claude', 'ai', 'Two-seat minimum, up to 150 seats; Standard and Premium seats for heavier users.', 'Plan facts from the vendor page.', 'https://support.claude.com/en/articles/9266767-what-is-the-team-plan', DR, replace=True)
field('gemini', 'ai', 'src', 'https://workspaceupdates.googleblog.com/2025/01/expanding-google-ai-to-more-of-google-workspace.html', 'Vendor source replaces a third-party blog.', 'https://workspaceupdates.googleblog.com/2025/01/expanding-google-ai-to-more-of-google-workspace.html', DR)
field('gemini', 'ai', 'canada', 'Included with Workspace; Workspace data regions are US or EU only', 'Canada facts instead of a plan name.', 'https://workspaceupdates.googleblog.com/2026/06/gemini-app-data-regions-support.html', DR)
for pid in ('copilot', 'chatgpt', 'claude', 'gemini'):
    rc_add(pid, 'ai', 'For patient, client-confidential or Quebec Law 25 data, check where data is stored and sign a data processing agreement before use.', 'Privacy caution was missing.', 'https://openai.com/index/expanding-data-residency-access-to-business-customers-worldwide', DR)
field('zohoanalytics', 'bi', 'canada', 'Zoho has Canadian data centres (Toronto and Montreal); confirm Analytics is hosted there', 'Canada fact added.', 'https://www.businesswire.com/news/home/20231102557441/en/Zoho-Launches-New-Data-Centers-in-Canada-Offering-Local-Businesses-Fast-Reliable-and-Secure-Access-to-their-Data', DR)
field('knowbe4', 'sec', 'canada', 'Canadian data hosting option (AWS Montreal)', 'Canada fact added.', 'https://support.knowbe4.com/hc/en-us/articles/45880984844179-KnowBe4-Data-Storage-Locations', DR)
score('knowbe4', 'sec', 'Email protection', 1, 'PhishER/Defend are separate products.', 'https://support.knowbe4.com/hc/en-us/articles/45880984844179-KnowBe4-Data-Storage-Locations', rev=DR)
field('1password', 'sec', 'canada', 'Canadian company (Toronto); Canadian data hosting on 1Password.ca', 'Canada fact added.', 'https://support.1password.com/regions', DR)
score('1password', 'sec', 'Multi-factor sign-in', 1, 'Stores one-time codes and passkeys; not an MFA provider for your apps.', 'https://support.1password.com/regions', rev=DR)
rc_add('m365bp', 'sec', 'Microsoft 365 Backup is a separate pay-as-you-go service; Business Premium does not back up servers or PCs.', 'Prevents it looking like a backup product.', 'https://learn.microsoft.com/en-us/microsoft-365/backup/', DR)

# ---------------- Logic-related data fixes (reviewer D, L5–L7, L13) ----------------
P = {p['t']: p for p in D['problems']}
def prob(text, c=None, w=None, why=''):
    p = P[text]
    if c is not None: LOG.append({'product': '(problem) ' + text, 'where': 'maps to', 'from': p['c'], 'to': c, 'why': why, 'evidence': '', 'reviewer': 'D logic'}); p['c'] = c
    if w is not None: p['w'] = w
prob('Union payroll and remittances take days each period', ['payroll', 'consys'], why='Union payroll is a payroll problem first (L5).')
prob('Practitioner splits and associate pay are calculated by hand', ['clinic', 'payroll'], why='Clinic systems handle compensation splits (L5).')
prob("Our systems don't talk to each other, so we re-type data", ['bi'], why='Integration is not an accounting problem (L13).')
# capability weights so options rank by fit to the stated problem (L9)
prob('We have no tested backup or ransomware plan', w={'sec': {'backup': 3, 'train': 1}})
prob('Staff use AI tools with no rules on what data goes in', w={'ai': {'privacy': 3, 'admin': 3}, 'sec': {'train': 2}})
prob('Repetitive writing and admin (emails, quotes, reports) eats our time', w={'ai': {'chat': 3, 'files': 2, 'suite': 2}})
prob('Timesheets and payroll take hours each pay period', w={'payroll': {'pay': 3, 'time': 3}})
prob('Leads and follow-ups fall through the cracks', w={'crm': {'pipe': 3, 'email': 3, 'auto': 2}})
prob('Inventory counts are wrong or we run out of stock', w={'inv': {'scan': 3, 'po': 2}})
prob('Hours-of-service and ELD compliance worries us', w={'tms': {'eld': 3}})
prob('Insurance billing and claims are slow and manual', w={'clinic': {'claims': 3}})
prob("We chase tenants for rent every month", w={'prop': {'rent': 3}})
prob('Field records are on paper or in our heads', w={'farm': {'field': 3, 'mobile': 2}})
prob('No-shows and manual appointment reminders', w={'clinic': {'book': 3, 'intake': 1}, 'booking': {'remind': 3}})
prob('Change orders and RFIs get lost', w={'cpm': {'co': 3, 'rfi': 3}})
prob("We don't know our food cost and waste", w={'inv': {'po': 2}, 'pos': {'stock': 3}})
# PSA and booking scope (L6, L7)
for p in D['products']:
    if p['id'] == 'monday': p['inds'] = ['prof', 'con', 'mfg']
    if p['id'] == 'clio': p['only'] = ['sv_legal']
    if p['id'] == 'karbon': p['only'] = ['sv_acct']
    if p['cat'] == 'booking' and p['id'] in ('fresha', 'vagaro', 'mindbody'): p['only'] = ['svc_salon']
    if p['id'] in ('jobber', 'hcp') : p['only'] = ['svc_home', 'fs']
D['subtypes']['prof'] = {'q': 'What kind of professional firm are you?', 'o': [['sv_legal', 'Law firm'], ['sv_acct', 'Accounting or bookkeeping firm'], ['sv', 'Engineering, architecture or consulting'], ['sv_it', 'IT, marketing or creative agency']],
                         'wf': {'sv_legal': 'sv', 'sv_acct': 'sv', 'sv': 'sv', 'sv_it': 'sv'}}
D['subtypes']['svc'] = {'q': 'What kind of service business are you?', 'o': [['svc_salon', 'Salon, spa, fitness or wellness studio'], ['svc_auto', 'Auto or equipment repair shop'], ['svc_home', 'Cleaning, landscaping or home services']],
                        'wf': {'svc_salon': 'core', 'svc_auto': 'fs', 'svc_home': 'fs'}}
D['subtypes']['con'] = {'q': 'What kind of contractor are you?', 'o': [['cx', 'General or project-based contractor'], ['fs', 'Service and maintenance contractor (HVAC, plumbing, electrical)']]}
D['gaps'] = {'svc_auto': 'Auto-repair shop management software (estimates, parts, vehicle history) is not listed yet.'}

OUT.write_text(json.dumps(D, ensure_ascii=False, indent=1))
(ROOT / 'content/assess/redteam_v7_log.json').write_text(json.dumps(LOG, ensure_ascii=False, indent=1))
nunv = sum(len(p.get('unv', [])) for p in D['products'] + D['erp']['vendors'])
print('V7 corrections applied:', len(LOG), '| flagged unverified:', nunv)
