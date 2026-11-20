"""Source of truth for the Digital Assessment data (Draft V3). Writes content/assess/assess_data.json.

Run from the repo root:  python3 content/assess/build_data_v3.py
Capability scores: 3 native, 2 configurable, 1 add-on or partner app, 0 not supported.
Scores are a preliminary analyst rating. "v": 1 marks products whose company facts (name, owner,
headquarters, Canadian status, certification or published price) were checked on the date in AS_OF
against the source in "src". Capability scores are not part of that check.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
ERP = json.loads((ROOT / 'content/erp/erp_data.json').read_text())
AS_OF = '2026-11-19'
ALL = ['mfg', 'con', 'dist', 'retail', 'prof', 'health', 'food', 'trans', 're', 'agri', 'svc']

industries = [
  ('mfg', 'Manufacturing', 'You make products: job shop, fabrication, assembly, process or food production.', 46793),
  ('con', 'Construction and trades', 'Contractors, specialty trades, renovation, installation and service crews.', 155565),
  ('dist', 'Wholesale and distribution', 'You buy, stock and resell products to other businesses.', 38992),
  ('retail', 'Retail and e-commerce', 'Stores and online sellers serving consumers.', 98592),
  ('prof', 'Professional services', 'Accounting, legal, engineering, consulting, design and IT services.', 151263),
  ('health', 'Health and wellness clinics', 'Physio, chiro, massage, dental, medical and other clinics.', 121697),
  ('food', 'Restaurants and hospitality', 'Restaurants, cafés, bars, catering and accommodation.', 77026),
  ('trans', 'Transportation and logistics', 'Trucking, courier, freight brokerage and warehousing services.', 69686),
  ('re', 'Real estate and property management', 'Landlords, property managers and rental businesses.', 50694),
  ('agri', 'Agriculture and agri-food', 'Farms, ranches, greenhouses and primary producers.', 47146),
  ('svc', 'Personal and repair services', 'Salons, fitness, auto repair, cleaning and other local services.', 104186),
]

# ---------------- categories: id, name, function, ease, time, desc, benefit, caps, links ----------------
C = []
def cat(i, n, fn, ease, weeks, desc, ben, caps, links=()):
    C.append({'id': i, 'name': n, 'fn': fn, 'ease': ease, 'weeks': weeks, 'desc': desc, 'benefit': ben,
              'caps': [{'k': k, 'n': nm, 'd': d} for k, nm, d in caps], 'links': [list(l) for l in links]})

cat('acct', 'Accounting and finance', 'fin', 3, '2–6 weeks', 'Cloud bookkeeping with bank feeds, invoicing, bills and Canadian sales tax.', 'Faster month-end, same-day invoices and a live view of cash.', [
  ('banks', 'Bank feeds', 'Automatic import and matching of bank and card transactions.'),
  ('invoice', 'Invoicing and payments', 'Branded invoices with online card or bank payment.'),
  ('tax', 'GST/HST/PST/QST', 'Canadian sales tax rates and filing reports built in.'),
  ('bills', 'Bills and receipts', 'Capture supplier bills and receipts, approve and pay them.'),
  ('jobs', 'Job or class tracking', 'Track income and cost by job, project, location or department.'),
  ('inv', 'Inventory', 'Track stock quantities and cost.'),
  ('reports', 'Reporting', 'Financial statements, cash flow and custom reports.'),
  ('apps', 'App ecosystem', 'Connectors to payroll, CRM, inventory and other apps.')],
  [('post/boost-performance-with-effective-dashboard-strategies-for-entrepreneurs.html', 'Dashboard strategies for entrepreneurs'), ('challenge-page/business-basics-for-owners.html', 'Free course: Business basics for owners')])
cat('payroll', 'Payroll, time and HR', 'people', 3, '2–4 weeks', 'Canadian payroll with remittances, time tracking, scheduling and employee records.', 'Hours saved each pay period and fewer payroll errors.', [
  ('pay', 'Canadian payroll', 'Pay runs with CPP, EI and tax deductions and CRA remittances.'),
  ('roe', 'T4s and ROEs', 'Year-end slips and Records of Employment filed electronically.'),
  ('time', 'Time tracking', 'Clock-in by app or kiosk feeding payroll.'),
  ('sched', 'Shift scheduling', 'Build and share staff schedules.'),
  ('hr', 'HR records and onboarding', 'Employee files, documents and digital onboarding.'),
  ('ben', 'Benefits', 'Group benefits administration.'),
  ('qc', 'Quebec support', 'Quebec payroll (QPP, QPIP, RL-1) and French.'),
  ('app', 'Employee self-serve app', 'Pay stubs, time off and schedules on a phone.')])
cat('crm', 'CRM and sales pipeline', 'sales', 2, '4–8 weeks', 'One place for contacts, opportunities, quotes and follow-ups.', 'No lost leads, a visible pipeline and faster quotes.', [
  ('pipe', 'Contacts and pipeline', 'Contact records and visual deal stages.'),
  ('quote', 'Quotes', 'Quotes from a product or service catalogue.'),
  ('email', 'Email and sequences', 'Two-way email and automated follow-up.'),
  ('auto', 'Workflow automation', 'Tasks and rules triggered by deal changes.'),
  ('rep', 'Sales reporting', 'Forecasts and pipeline dashboards.'),
  ('mobile', 'Mobile app', 'Full use on phone for field sales.'),
  ('integ', 'Accounting link', 'Sync customers, quotes and invoices with accounting.'),
  ('easy', 'Ease of set-up', 'Usable by a small team without an administrator.')],
  [('post/choosing-the-right-crm-system-how-to-make-the-best-choice-for-your-business.html', 'Choosing the right CRM system')])
cat('mkt', 'Email and marketing', 'sales', 3, '2–4 weeks', 'Email newsletters, automated campaigns and simple landing pages.', 'Repeat business from your customer list without manual effort.', [
  ('camp', 'Email campaigns', 'Design and send newsletters.'),
  ('journey', 'Automated journeys', 'Welcome, follow-up and win-back sequences.'),
  ('seg', 'Segmentation', 'Target by behaviour, purchases or tags.'),
  ('forms', 'Forms and landing pages', 'Sign-up forms and simple pages.'),
  ('social', 'Social scheduling', 'Plan and publish social posts.'),
  ('shop', 'E-commerce link', 'Purchase data from your online store.')])
cat('ecom', 'E-commerce and B2B ordering', 'sales', 2, '1–3 months', 'Online store or B2B portal with customer pricing and live stock.', 'Customers order 24/7 and staff stop re-typing orders.', [
  ('store', 'Online store', 'Themes, product pages and checkout.'),
  ('b2b', 'B2B portal and pricing', 'Customer-specific price lists, terms and reorder.'),
  ('sync', 'Inventory sync', 'Live stock from your inventory or ERP system.'),
  ('pay', 'Canadian payments', 'CAD checkout, Interac and Canadian tax.'),
  ('ship', 'Shipping', 'Carrier rates and labels, incl. Canada Post.'),
  ('mkt', 'Marketplaces', 'Sell on Amazon and other marketplaces.'),
  ('apps', 'App ecosystem', 'Add-ons for reviews, subscriptions and more.')])
cat('pos', 'Point of sale', 'sales', 3, '2–6 weeks', 'In-store and restaurant checkout with inventory, payments and customer data.', 'Faster checkout, accurate stock and sales data by item.', [
  ('checkout', 'Checkout and hardware', 'Fast checkout on iPad or terminals.'),
  ('stock', 'Inventory', 'Stock levels and purchasing by store.'),
  ('loyalty', 'Customers and loyalty', 'Customer profiles, gift cards and loyalty.'),
  ('omni', 'Online store link', 'Shared stock and orders with e-commerce.'),
  ('table', 'Tables and menus', 'Floor plans, modifiers and kitchen display.'),
  ('multi', 'Multi-location', 'Central control of several stores.'),
  ('pay', 'Integrated payments', 'Card and tap payments in Canada.')])
cat('booking', 'Online booking and scheduling', 'sales', 3, '1–3 weeks', 'Online appointment booking with reminders, deposits and client records.', 'Fewer no-shows and no more phone tag to book appointments.', [
  ('book', 'Online booking', 'Customers book themselves from your website.'),
  ('remind', 'Reminders', 'Email and text reminders to cut no-shows.'),
  ('pay', 'Deposits and payments', 'Take deposits or full payment when booking.'),
  ('staff', 'Staff calendars', 'Several staff, rooms or resources.'),
  ('clients', 'Client records', 'History, notes and forms per client.'),
  ('mkt', 'Reviews and marketing', 'Review requests and promotions.')])
cat('clinic', 'Clinic management and EMR', 'ops', 2, '1–2 months', 'Booking, charting, insurance billing and patient records for clinics.', 'Less front-desk admin, faster billing and complete records.', [
  ('book', 'Online booking', 'Patients book and reschedule online.'),
  ('chart', 'Charting', 'Templates for SOAP notes and assessments.'),
  ('claims', 'Insurance billing', 'Direct billing to Canadian insurers and provincial plans.'),
  ('intake', 'Intake and portal', 'Digital intake forms and patient portal.'),
  ('tele', 'Telehealth', 'Video visits.'),
  ('pay', 'Payments', 'Card on file and integrated payments.'),
  ('rep', 'Reporting', 'Practitioner, revenue and retention reports.'),
  ('host', 'Canadian data hosting', 'Patient data stored in Canada.')])
cat('psa', 'Practice and project management', 'ops', 2, '4–8 weeks', 'Time, billing, projects and client files for professional-service firms.', 'Every billable hour captured and invoices out faster.', [
  ('time', 'Time tracking', 'Timers and timesheets by client and task.'),
  ('bill', 'Billing', 'Hourly, fixed-fee and retainer invoicing.'),
  ('budget', 'Project budgets', 'Budget versus actual by project.'),
  ('resource', 'Resource planning', 'Who is working on what, and capacity.'),
  ('docs', 'Document management', 'Client files and templates.'),
  ('portal', 'Client portal', 'Secure sharing and requests with clients.'),
  ('trust', 'Industry features', 'E.g. trust accounting for law, workflows for accounting firms.')])
cat('fsm', 'Field service and job management', 'ops', 2, '3–8 weeks', 'Scheduling, dispatch, mobile job tickets, quotes and invoicing for crews.', 'Crews know where to go, and jobs are invoiced from the field.', [
  ('dispatch', 'Scheduling and dispatch', 'Drag-and-drop crew schedule.'),
  ('mobile', 'Mobile job app', 'Job details, checklists and photos on site.'),
  ('quote', 'Quotes', 'Quotes customers approve online.'),
  ('invoice', 'Invoicing and payments', 'Invoice and take payment on site.'),
  ('gps', 'GPS and routing', 'Crew location and route planning.'),
  ('portal', 'Customer portal', 'Booking requests and job history for clients.'),
  ('cost', 'Job costing', 'Labour and material cost per job.'),
  ('acct', 'Accounting sync', 'Sync with QuickBooks or Xero.')])
cat('cpm', 'Construction project management', 'ops', 2, '1–3 months', 'Drawings, RFIs, change orders, daily logs and job costing for projects.', 'Fewer lost change orders and a clear record on every project.', [
  ('draw', 'Drawings', 'Current drawings and markups on site.'),
  ('rfi', 'RFIs and submittals', 'Track questions and approvals.'),
  ('co', 'Change orders', 'Price, approve and track changes.'),
  ('daily', 'Daily logs and photos', 'Site reports with photos.'),
  ('sched', 'Scheduling', 'Project schedule and look-ahead.'),
  ('cost', 'Budgets and job costing', 'Budget, commitments and actual cost.'),
  ('client', 'Client portal', 'Owner updates and selections.'),
  ('acct', 'Accounting link', 'Sync with your accounting system.')])
cat('inv', 'Inventory and order management', 'ops', 2, '1–3 months', 'Stock levels, purchasing, barcode scanning and sales orders across channels.', 'Accurate stock, fewer stock-outs and faster order processing.', [
  ('loc', 'Multi-location stock', 'Stock by warehouse, store or van.'),
  ('scan', 'Barcode scanning', 'Scan to receive, move and pick.'),
  ('po', 'Purchasing and reorder', 'Reorder points and purchase orders.'),
  ('so', 'Sales orders', 'Quotes, orders and fulfilment.'),
  ('lot', 'Lot and serial', 'Lot, batch, expiry or serial tracking.'),
  ('kit', 'Kits and light assembly', 'Bundles and simple assembly.'),
  ('chan', 'Sales channel sync', 'Shopify, Amazon and B2B orders.'),
  ('acct', 'Accounting sync', 'Sync with QuickBooks or Xero.')],
  [('post/phantom-stock-inventory-accuracy-and-cycle-counting.html', 'Phantom stock and cycle counting'), ('challenge-page/inventory-management-for-smes.html', 'Free course: Inventory management for SMEs')])
cat('mrp', 'MRP (production planning)', 'ops', 2, '1–3 months', 'Production planning on top of your accounting software: BOMs, routings, material planning and costing.', 'A real production schedule, materials ordered on time and true product costs.', [
  ('bom', 'Multi-level BOMs', 'Nested bills of materials with sub-assemblies.'),
  ('route', 'Routings and work centres', 'Operations, times and work centres per product.'),
  ('plan', 'Material planning (MRP)', 'Calculates what to buy and make, and when.'),
  ('sched', 'Production scheduling', 'Schedule orders against capacity.'),
  ('floor', 'Shop-floor reporting', 'Operators record progress and time on tablets.'),
  ('cost', 'Product costing', 'Material, labour and overhead cost per product.'),
  ('lot', 'Lot and serial', 'Lot, batch or serial traceability.'),
  ('acct', 'QuickBooks or Xero link', 'Keeps your accounting system.')],
  [('challenge-page/choosing-erp-and-business-software.html', 'Free course: Choosing ERP and business software')])
cat('erp', 'ERP', 'ops', 1, '3–12 months', 'One system for finance, sales, purchasing, inventory and production or distribution.', 'Data entered once, true job or product costs, and a base to scale on.', [],
  [('challenge-page/choosing-erp-and-business-software.html', 'Free course: Choosing ERP and business software'), ('post/10-best-erp-systems-for-small-and-medium-sized-enterprises.html', '10 best ERP systems for SMEs')])
cat('wms', 'Warehouse management (WMS)', 'ops', 2, '2–6 months', 'Warehouse execution: bins, scanning, put-away, picking, counting and shipping.', 'Fewer picking errors, accurate stock and more orders shipped per hour.', [],
  [('post/do-we-need-a-wms-yet-when-spreadsheets-stop-scaling.html', 'Do we need a WMS yet?'), ('post/pickers-walk-half-the-day-pick-methods-and-pick-paths.html', 'Pick methods and pick paths')])
cat('tms', 'Fleet and transportation management', 'ops', 2, '1–3 months', 'Vehicle tracking, Canadian ELD compliance, dispatch, maintenance and freight billing.', 'Compliant drivers, fewer check calls and loads invoiced faster.', [
  ('gps', 'GPS tracking', 'Live vehicle location and trip history.'),
  ('eld', 'Canadian ELD and hours of service', 'Electronic logs certified for Canada.'),
  ('dispatch', 'Dispatch and load planning', 'Assign loads and plan trips.'),
  ('driver', 'Driver app', 'Messages, documents and proof of delivery.'),
  ('maint', 'Maintenance', 'Inspections and service schedules.'),
  ('fuel', 'Fuel and IFTA', 'Fuel tax reporting by jurisdiction.'),
  ('bill', 'Freight billing', 'Rate, invoice and settle loads.'),
  ('track', 'Customer tracking', 'Shipment status for customers.')])
cat('prop', 'Property management', 'ops', 2, '3–8 weeks', 'Rent collection, leasing, maintenance and owner reporting.', 'Rent collected on time and fewer late-night maintenance calls.', [
  ('rent', 'Online rent collection', 'Pre-authorized debit and online payments.'),
  ('lease', 'Leasing and screening', 'Listings, applications and tenant screening.'),
  ('maint', 'Maintenance requests', 'Tenant requests and work orders.'),
  ('owner', 'Owner statements', 'Statements and owner portal.'),
  ('acct', 'Property accounting', 'Trust and property-level accounting.'),
  ('portal', 'Tenant portal', 'Tenant app for payments and requests.'),
  ('ca', 'Canadian set-up', 'GST and Canadian payment methods.')])
cat('farm', 'Farm management', 'ops', 2, '1–2 months', 'Farm accounting, field records, crop planning and inventory.', 'Cost of production by field and records ready for lenders and programs.', [
  ('acct', 'Farm accounting', 'Accounting built for farm terms and Canadian tax.'),
  ('field', 'Field records', 'Seeding, spraying and harvest records.'),
  ('plan', 'Crop planning', 'Budgets and scenarios by crop and field.'),
  ('inv', 'Grain and input inventory', 'Bins, inputs and contracts.'),
  ('live', 'Livestock', 'Animal records and production.'),
  ('mobile', 'Mobile app', 'Record work from the field.'),
  ('ca', 'Canadian reporting', 'Canadian tax and program reporting.')])
cat('collab', 'Collaboration and documents', 'it', 3, '2–6 weeks', 'Shared email, files, chat and document control in the cloud.', 'One source of truth for files and less knowledge locked in inboxes.', [
  ('mail', 'Email and calendar', 'Business email on your domain.'),
  ('files', 'File storage and sharing', 'Shared drives and external sharing.'),
  ('chat', 'Chat and meetings', 'Team chat and video calls.'),
  ('ver', 'Document control', 'Versioning, permissions and retention.'),
  ('office', 'Office apps', 'Documents, spreadsheets and slides.'),
  ('ca', 'Canadian data residency', 'Option to store data in Canada.')],
  [('post/physical-servers-vs-cloud-servers-which-is-better-for-digitizing-your-data.html', 'Physical servers vs cloud servers')])
cat('bi', 'Reporting and dashboards', 'it', 2, '4–8 weeks', 'Live dashboards built from accounting, sales and operations data.', 'Decisions from current numbers instead of hand-built spreadsheets.', [
  ('dash', 'Dashboards', 'Interactive charts and KPIs.'),
  ('acct', 'Accounting connectors', 'Ready links to QuickBooks, Xero and Sage.'),
  ('ops', 'Sales and operations connectors', 'Links to CRM, ERP, databases and files.'),
  ('fc', 'Forecasting', 'Cash-flow and trend forecasts.'),
  ('easy', 'Ease of use', 'Built by a business user, not a developer.'),
  ('share', 'Sharing', 'Share and schedule reports.')],
  [('challenge-page/data-and-dashboards-for-smes.html', 'Free course: Data and dashboards for SMEs'), ('post/50-must-track-kpis-for-business-success-from-finance-to-product-development.html', '50 KPIs to track')])
cat('sec', 'Backup and cybersecurity', 'it', 3, '2–4 weeks', 'Backups, multi-factor sign-in, device management, password management and staff training.', 'Lower risk of a ransomware shutdown, and insurer requirements met.', [
  ('backup', 'Backup and restore', 'Copies of servers, PCs and cloud data.'),
  ('mfa', 'Multi-factor sign-in', 'Identity and access control.'),
  ('device', 'Device management', 'Manage and wipe laptops and phones.'),
  ('mail', 'Email protection', 'Phishing and malware filtering.'),
  ('pw', 'Password management', 'Shared vaults for teams.'),
  ('train', 'Staff training', 'Phishing tests and awareness training.')],
  [('challenge-page/cybersecurity-and-ransomware-basics-for-smes.html', 'Free course: Cybersecurity and ransomware basics'), ('post/cybersecurity-for-small-businesses-tips-and-best-practices.html', 'Cybersecurity tips for small businesses')])
cat('ai', 'AI assistants', 'it', 3, '1–4 weeks', 'Business AI assistants for drafting, analysis and automating routine work.', 'Hours back each week on emails, documents, research and reports.', [
  ('chat', 'Drafting and analysis', 'Write, summarize and analyse.'),
  ('files', 'Works with your files', 'Reads documents and spreadsheets you provide.'),
  ('apps', 'Connects to business apps', 'Connectors to email, drives, CRM and more.'),
  ('suite', 'Office suite built in', 'Works inside Microsoft 365 or Google Workspace.'),
  ('privacy', 'Business data terms', 'Business plan with no training on your data by default.'),
  ('admin', 'Admin controls', 'Central billing, users and policies.'),
  ('agents', 'Agents and automation', 'Multi-step tasks and automations.')],
  [('challenge-page/prompting-and-ai-productivity.html', 'Free course: Prompting and AI productivity'), ('post/ai-readiness-preparing-your-organization-for-successful-ai-adoption.html', 'AI readiness for your organization')])

# ---------------- products ----------------
P = []
def prod(i, c, n, s, inds, size, price, deploy, canada, best, rc, ca=False, v=0, src='', note=''):
    P.append({'id': i, 'cat': c, 'name': n, 's': [int(x) for x in s], 'inds': inds, 'size': size, 'price': price, 'deploy': deploy,
              'canada': canada, 'ca': ca, 'best': best, 'rc': rc, 'v': v, 'src': src, 'note': note})
G = ALL  # general-purpose
prod('qbo', 'acct', 'QuickBooks Online', '33332223', G, ['s'], 1, ['Cloud'], 'Canadian edition (GST/HST)', 'Small businesses wanting the widest accountant support', 'Inventory and job costing are basic; growing manufacturers usually outgrow it first.')
prod('xero', 'acct', 'Xero', '33332223', G, ['s'], 1, ['Cloud'], 'Canadian tax settings', 'Small businesses wanting a large app marketplace', 'Canadian payroll needs a separate app; check your accountant uses Xero.')
prod('sage50', 'acct', 'Sage 50 (Canadian edition)', '23322322', G, ['s'], 1, ['On-premise', 'Cloud'], 'Canadian edition with payroll', 'Firms that prefer desktop accounting', 'Desktop roots make remote access and integrations harder than cloud-native tools.')
prod('freshbooks', 'acct', 'FreshBooks', '33332022', ['prof', 'con', 'svc', 'health'], ['s'], 1, ['Cloud'], 'Canadian company', 'Service businesses that bill time and projects', 'Built for services; not suited to stock-heavy businesses.', ca=True)
prod('intacct', 'acct', 'Sage Intacct', '32333133', G, ['m', 'l'], 2, ['Cloud'], 'Canadian partners', 'Multi-entity firms outgrowing small-business accounting', 'A finance system, not an ERP: operations still need their own system.')

prod('wagepoint', 'payroll', 'Wagepoint', '33001012', G, ['s'], 1, ['Cloud'], 'Canadian company', 'Simple Canadian payroll for small teams', 'Payroll only; time tracking and HR records need other tools.', ca=True)
prod('emphero', 'payroll', 'Employment Hero (formerly Humi)', '33223323', G, ['s', 'm'], 1, ['Cloud'], 'Built in Canada; Canadian data hosting', 'Payroll, HR and benefits in one Canadian platform', 'Humi moved to the Employment Hero platform in 2025; Quebec businesses are served by Humi by Employment Hero.', v=1, src='https://employmenthero.com/en-ca/about-us/')
prod('adp', 'payroll', 'ADP Workforce Now', '33213332', G, ['m', 'l'], 2, ['Cloud'], 'Canadian payroll service', 'Mid-size firms wanting payroll, HR and benefits together', 'Contracts and add-on pricing need careful reading.')
prod('dayforce', 'payroll', 'Dayforce', '33333333', G, ['m', 'l'], 3, ['Cloud'], 'Built-in Canadian payroll', 'Larger hourly workforces with complex scheduling', 'Powerful but heavy for firms under about 100 staff.')
prod('bamboo', 'payroll', 'BambooHR', '00213203', G, ['s', 'm'], 1, ['Cloud'], 'HR records; pair with Canadian payroll', 'HR records, onboarding and time off', 'Its built-in payroll is US-focused; Canadian firms pair it with a Canadian payroll provider.')
prod('7shifts', 'payroll', '7shifts', '00332013', ['food'], ['s', 'm'], 1, ['Cloud'], 'Canadian company', 'Restaurant scheduling, time clock and tips', 'Scheduling and labour control first; run Canadian payroll through your payroll provider.', ca=True, v=1, src='https://www.capterra.ca/software/123038/7shifts-restaurant-scheduling')

prod('hubspot', 'crm', 'HubSpot', '32333333', G, ['s', 'm'], 1, ['Cloud'], 'Canadian customers supported', 'Teams that want marketing and sales in one tool', 'Free start, but costs climb quickly with seats and marketing contacts.')
prod('pipedrive', 'crm', 'Pipedrive', '32122323', G, ['s'], 1, ['Cloud'], 'Canadian customers supported', 'Small sales teams focused on deals', 'Simple pipeline tool; quoting from a product catalogue needs add-ons.')
prod('zohocrm', 'crm', 'Zoho CRM', '32232332', G, ['s', 'm'], 1, ['Cloud'], 'Canadian customers supported', 'Cost-conscious firms wanting a wide suite', 'Very configurable; set-up quality decides adoption.')
prod('sfdc', 'crm', 'Salesforce Sales Cloud', '32233331', G, ['m', 'l'], 2, ['Cloud'], 'Canadian data centres available', 'Larger sales teams with complex processes', 'Usually needs a partner or in-house admin to get value.')

prod('mailchimp', 'mkt', 'Mailchimp', '322213', G, ['s', 'm'], 1, ['Cloud'], 'Serves Canadian businesses', 'Newsletters and simple automations', 'Pricing rises with contacts; clean your list before importing. Canadian anti-spam law (CASL) consent is your responsibility.')
prod('cc', 'mkt', 'Constant Contact', '322222', G, ['s'], 1, ['Cloud'], 'Serves Canadian businesses', 'Local businesses and events', 'Simple to use; automation is lighter than specialist tools.')
prod('klaviyo', 'mkt', 'Klaviyo', '333213', ['retail', 'dist', 'mfg'], ['s', 'm'], 1, ['Cloud'], 'Serves Canadian businesses', 'Online stores using purchase data', 'Best with Shopify; costs scale with profiles.')
prod('brevo', 'mkt', 'Brevo', '322212', G, ['s'], 1, ['Cloud'], 'Serves Canadian businesses', 'Low-cost email and SMS', 'Priced by emails sent, not contacts; check deliverability set-up.')

prod('shopify', 'ecom', 'Shopify (incl. B2B)', '3223333', ['retail', 'dist', 'mfg', 'food', 'agri'], ['s', 'm', 'l'], 1, ['Cloud'], 'Canadian company', 'Online and B2B ordering with a large app ecosystem', 'Check which plan includes the B2B features you need; inventory sync to your ERP needs a connector.', ca=True)
prod('bigcommerce', 'ecom', 'BigCommerce B2B', '3322232', ['dist', 'mfg', 'retail'], ['s', 'm'], 2, ['Cloud'], 'Serves Canadian businesses', 'Distributors with customer-specific price lists', 'Strong B2B features; integration to your ERP is the main project.')
prod('woo', 'ecom', 'WooCommerce', '3122213', ['retail', 'dist', 'mfg', 'svc'], ['s'], 1, ['Self-hosted'], 'Open source', 'Firms already on WordPress', 'Low licence cost; hosting, security and plugin updates are on you.')

prod('shopifypos', 'pos', 'Shopify POS', '3323023', ['retail'], ['s', 'm'], 1, ['Cloud'], 'Canadian company', 'Retailers selling in store and online', 'Strongest when your online store is also on Shopify.', ca=True)
prod('lsretail', 'pos', 'Lightspeed Retail', '3322033', ['retail'], ['s', 'm', 'l'], 2, ['Cloud'], 'Canadian company (Montreal)', 'Specialty and multi-store retailers', 'Deep inventory features; budget for payment processing terms.', ca=True, v=1, src='https://www.cbinsights.com/company/lightspeed-retail')
prod('lsresto', 'pos', 'Lightspeed Restaurant', '3221333', ['food'], ['s', 'm', 'l'], 2, ['Cloud'], 'Canadian company (Montreal)', 'Restaurants and multi-location groups', 'Compare payment rates and hardware costs, not only the monthly fee.', ca=True, v=1, src='https://www.cbinsights.com/company/lightspeed-retail')
prod('touchbistro', 'pos', 'TouchBistro', '3221323', ['food'], ['s', 'm'], 1, ['Cloud'], 'Canadian company (Toronto)', 'Full- and quick-service restaurants', 'Restaurant-only focus; inventory and reservations are add-ons.', ca=True, v=1, src='https://www.cbinsights.com/company/touchbistro')
prod('square', 'pos', 'Square', '3222123', ['retail', 'food', 'svc'], ['s'], 1, ['Cloud'], 'Available in Canada', 'Small shops, cafés and service businesses', 'Easy start; check that the Canadian version has the features you need.')

prod('acuity', 'booking', 'Acuity Scheduling', '332221', ['svc', 'prof', 'health'], ['s'], 1, ['Cloud'], 'Serves Canadian businesses', 'Solo and small appointment-based businesses', 'Booking only; client records are light.')
prod('fresha', 'booking', 'Fresha', '333332', ['svc'], ['s', 'm'], 1, ['Cloud'], 'Serves Canadian businesses', 'Salons, spas and barbers', 'Low subscription cost; fees are on payments and new-client bookings.')
prod('mindbody', 'booking', 'Mindbody', '333333', ['svc', 'health'], ['s', 'm'], 2, ['Cloud'], 'Serves Canadian businesses', 'Fitness studios and wellness businesses', 'Feature-rich; check contract length and payment terms.')
prod('vagaro', 'booking', 'Vagaro', '333332', ['svc'], ['s', 'm'], 1, ['Cloud'], 'Serves Canadian businesses', 'Salons, spas and fitness', 'Many add-ons are priced separately.')

prod('jane', 'clinic', 'Jane', '33333323', ['health'], ['s', 'm'], 1, ['Cloud'], 'Canadian company (North Vancouver)', 'Allied health clinics: physio, chiro, massage, counselling', 'Easy for front desk and practitioners; payroll and websites are paid add-ons.', ca=True, v=1, src='https://www.cbinsights.com/company/jane-software/')
prod('juvonno', 'clinic', 'Juvonno', '33332333', ['health'], ['s', 'm', 'l'], 1, ['Cloud'], 'Canadian company (Winnipeg)', 'Multi-disciplinary and multi-location clinics', 'Strong Canadian billing; plan time to set up insurers and templates.', ca=True, v=1, src='https://slashdot.org/software/p/Juvonno')
prod('oscarpro', 'clinic', 'OSCAR Pro (WELL Health)', '23312123', ['health'], ['s', 'm'], 2, ['Cloud'], 'Canadian (WELL Health, Vancouver)', 'Physician and primary-care clinics', 'Provincial EMR certification matters; moving off it later is a real project.', ca=True, v=1, src='https://well.company/oscar-pro/')

prod('clio', 'psa', 'Clio', '3321333', ['prof'], ['s', 'm', 'l'], 1, ['Cloud'], 'Canadian company (Burnaby)', 'Law firms of all sizes', 'Legal-specific with trust accounting; accounting firms and consultancies need other tools.', ca=True, v=1, src='https://www.clio.com/en-ca/about/')
prod('karbon', 'psa', 'Karbon', '2222232', ['prof'], ['s', 'm'], 1, ['Cloud'], 'Serves Canadian firms', 'Accounting and bookkeeping firms', 'Workflow and email-centric; billing depth depends on plan.')
prod('harvest', 'psa', 'Harvest', '3221000', ['prof', 'con'], ['s'], 1, ['Cloud'], 'Serves Canadian businesses', 'Simple time tracking and invoicing', 'Time and invoices only; no resource planning or documents.')
prod('bigtime', 'psa', 'BigTime', '3333111', ['prof'], ['s', 'm'], 2, ['Cloud'], 'Serves Canadian firms', 'Engineering, consulting and IT services firms', 'Strong project accounting; set up billing rules carefully.')
prod('monday', 'psa', 'monday.com Work Management', '1023211', G, ['s', 'm', 'l'], 1, ['Cloud'], 'Serves Canadian businesses', 'Teams managing projects and workflows visually', 'Flexible boards; billing and time need integrations.')

prod('jobber', 'fsm', 'Jobber', '33332323', ['con', 'svc'], ['s'], 1, ['Cloud'], 'Canadian company (Edmonton)', 'Home-service and small trade crews', 'Great for scheduling and invoicing; not built for large construction projects.', ca=True)
prod('servicetitan', 'fsm', 'ServiceTitan', '33333333', ['con'], ['m', 'l'], 3, ['Cloud'], 'Serves Canadian contractors', 'Larger HVAC, plumbing and electrical service firms', 'Implementation and per-technician pricing add up; plan a proper rollout.')
prod('hcp', 'fsm', 'Housecall Pro', '33332323', ['con', 'svc'], ['s'], 1, ['Cloud'], 'Serves Canadian contractors', 'Owner-operators and small service teams', 'Check Canadian payment processing and tax handling before signing.')
prod('simpro', 'fsm', 'Simpro', '33332233', ['con'], ['s', 'm'], 2, ['Cloud'], 'Serves Canadian contractors', 'Trade contractors with projects and service work', 'Covers quoting to invoicing; set-up of job costing takes time.')

prod('procore', 'cpm', 'Procore', '33332323', ['con'], ['m', 'l'], 3, ['Cloud'], 'Canadian customers and partners', 'General contractors running commercial projects', 'Priced on construction volume; strong but large for small trades.')
prod('buildertrend', 'cpm', 'Buildertrend', '21333333', ['con'], ['s', 'm'], 2, ['Cloud'], 'Serves Canadian builders', 'Residential builders and renovators', 'Strong client portal; accounting still runs in your accounting system.')
prod('fieldwire', 'cpm', 'Fieldwire', '32132101', ['con'], ['s', 'm'], 1, ['Cloud'], 'Serves Canadian contractors', 'Site teams needing drawings, tasks and punch lists', 'Field execution tool; job costing and financials are elsewhere.')

prod('cin7', 'inv', 'Cin7 Core', '32333333', ['dist', 'mfg', 'retail'], ['s', 'm'], 2, ['Cloud'], 'Serves Canadian businesses', 'Multichannel sellers with light assembly', 'Strong channel links; test landed-cost and assembly set-up.')
prod('zohoinv', 'inv', 'Zoho Inventory', '32332233', ['dist', 'retail'], ['s'], 1, ['Cloud'], 'Serves Canadian businesses', 'Small distributors and online sellers', 'Affordable start; limited for warehouses with many bins.')
prod('inflow', 'inv', 'inFlow Inventory', '33332222', ['dist', 'mfg', 'retail'], ['s'], 1, ['Cloud'], 'Canadian company (Winnipeg)', 'Small businesses moving inventory off spreadsheets', 'Easy to adopt; plan the next step if order volume grows fast.', ca=True)
prod('fishbowl', 'inv', 'Fishbowl', '33333323', ['dist', 'mfg'], ['s', 'm'], 1, ['Cloud', 'On-premise'], 'Serves Canadian businesses', 'QuickBooks and Xero users needing barcode inventory', 'Extends QuickBooks or Xero rather than replacing them; check the Canadian version you run.', v=1, src='https://www.fishbowlinventory.com/news/')
prod('marketman', 'inv', 'MarketMan', '22300103', ['food'], ['s', 'm'], 1, ['Cloud'], 'Listed for Canadian restaurants', 'Restaurant food cost, ordering and inventory', 'Works best when connected to your POS and supplier catalogues.', v=1, src='https://www.capterra.ca/software/136439/marketman-restaurant-inventory')

prod('katana', 'mrp', 'Katana', '32332233', ['mfg'], ['s', 'm'], 2, ['Cloud'], 'Serves Canadian manufacturers', 'Small discrete makers selling online', 'Routings sit in a paid manufacturing add-on; model the full plan cost, not the entry price.', v=1, src='https://resources.rework.com/tools/inventory-supply-chain/best-katana-alternatives')
prod('mrpeasy', 'mrp', 'MRPeasy', '33332333', ['mfg'], ['s'], 1, ['Cloud'], 'Serves Canadian manufacturers', 'Small manufacturers moving off spreadsheets', 'Good value for 5–50 staff; limited for multi-site or complex job shops.')
prod('fishbowlmfg', 'mrp', 'Fishbowl Manufacturing', '31211233', ['mfg'], ['s', 'm'], 1, ['Cloud', 'On-premise'], 'Serves Canadian businesses', 'QuickBooks or Xero users adding work orders', 'Work orders and BOMs rather than full planning; Fishbowl launched new AI manufacturing features in 2026.', v=1, src='https://www.fishbowlinventory.com/news/')
prod('odoomrp', 'mrp', 'Odoo Manufacturing', '33332231', ['mfg'], ['s', 'm'], 1, ['Cloud', 'On-premise'], 'Canadian partners', 'Makers wanting MRP with room to grow into a full ERP', 'Uses Odoo accounting rather than QuickBooks; partner quality decides the outcome.')
prod('craftybase', 'mrp', 'Craftybase', '20110323', ['mfg'], ['s'], 1, ['Cloud'], 'Serves Canadian makers', 'Very small makers and craft producers', 'Strong cost tracking for small batches; not for job shops.')

prod('geotab', 'tms', 'Geotab', '32233201', ['trans', 'con', 'dist', 'svc', 'agri'], ['s', 'm', 'l'], 1, ['Cloud'], 'Canadian company (Oakville)', 'Fleet tracking from a few vans to large fleets', 'Check that the exact ELD device is on Transport Canada\'s certified list; many features come from Marketplace partners.', ca=True, v=1, src='https://en.wikipedia.org/wiki/Geotab')
prod('isaac', 'tms', 'ISAAC Instruments', '33232301', ['trans'], ['m', 'l'], 2, ['Cloud'], 'Canadian company (Quebec); Transport Canada-certified ELD', 'For-hire and private trucking fleets', 'Built for heavy trucks; less suited to light service vans.', ca=True, v=1, src='https://tc.canada.ca/en/road-transportation/electronic-logging-devices/list-electronic-logging-devices')
prod('samsara', 'tms', 'Samsara', '32233301', ['trans', 'con', 'dist', 'food'], ['m', 'l'], 2, ['Cloud'], 'Serves Canadian fleets', 'Mixed fleets wanting cameras, telematics and safety', 'Multi-year contracts are common; check Transport Canada ELD certification for your devices.')
prod('roserocket', 'tms', 'Rose Rocket', '10330133', ['trans'], ['s', 'm'], 2, ['Cloud'], 'Canadian company (Toronto)', 'Carriers, brokers and 3PLs needing a TMS', 'Quote-to-cash TMS; pair it with a telematics/ELD provider.', ca=True, v=1, src='https://www.cbinsights.com/company/rose-rocket')

prod('buildium', 'prop', 'Buildium', '3333333', ['re'], ['s', 'm'], 1, ['Cloud'], 'Canadian edition with GST', 'Residential property managers', 'Check Canadian payment options for rent collection in your province.', v=1, src='https://buildium.com/sales-demo-canada')
prod('yardibreeze', 'prop', 'Yardi Breeze', '3333332', ['re'], ['s', 'm'], 2, ['Cloud'], 'Canadian version with Canadian support team', 'Smaller residential and commercial portfolios', 'In Canada it is sold as Breeze Premier, with a higher monthly minimum than the US version.', v=1, src='https://www.yardibreeze.com/?p=11376')

prod('agexpert', 'farm', 'AgExpert (Farm Credit Canada)', '3332133', ['agri'], ['s', 'm'], 1, ['Cloud', 'On-premise'], 'Canadian (Farm Credit Canada)', 'Canadian farms wanting accounting and field records', 'Built for Canadian farm accounting; precision-ag data comes from partner integrations.', ca=True, v=1, src='https://www.fcc-fac.ca/en/about-fcc/media-centre/news-releases/2026/agexpert-feature-next-seasons-advantage')
prod('fieldview', 'farm', 'Climate FieldView', '0320030', ['agri'], ['s', 'm', 'l'], 1, ['Cloud'], 'Available in Canada', 'Grain farms using equipment data', 'Agronomy data, not accounting; pair with farm accounting.')
prod('farmbrite', 'farm', 'Farmbrite', '2322331', ['agri'], ['s'], 1, ['Cloud'], 'Serves Canadian farms', 'Small mixed and livestock farms', 'Simple and affordable; accounting is not Canadian-specific.')

prod('m365', 'collab', 'Microsoft 365 Business', '333333', G, ['s', 'm', 'l'], 1, ['Cloud'], 'Canadian data centres', 'Email, Teams, SharePoint and Office in one subscription', 'SharePoint needs a planned folder structure, or it becomes another mess.')
prod('gws', 'collab', 'Google Workspace', '333232', G, ['s', 'm'], 1, ['Cloud'], 'Canadian data region options', 'Browser-first teams', 'Excel-heavy finance teams may still need Microsoft Office.')
prod('dropbox', 'collab', 'Dropbox Business', '030212', ['con', 'mfg', 'prof'], ['s', 'm'], 1, ['Cloud'], 'Canadian data storage option', 'Large drawing and photo files shared with outside parties', 'File sharing only; email and chat stay elsewhere.')

prod('powerbi', 'bi', 'Microsoft Power BI', '323213', G, ['s', 'm', 'l'], 1, ['Cloud'], 'Canadian data centres', 'Firms on Microsoft 365 wanting live dashboards', 'Licences are cheap; the real work is clean data and someone to build reports.')
prod('zohoanalytics', 'bi', 'Zoho Analytics', '333223', G, ['s', 'm'], 1, ['Cloud'], 'Serves Canadian businesses', 'Ready connectors to common SME apps', 'Fast start with templates; check connectors for your exact systems.')
prod('fathom', 'bi', 'Fathom', '230333', G, ['s', 'm'], 1, ['Cloud'], 'Works with Canadian accounting files', 'Financial KPIs and cash-flow forecasts from accounting data', 'Finance-only view; operations data needs another tool.')
prod('looker', 'bi', 'Looker Studio', '212123', G, ['s'], 1, ['Cloud'], 'Free Google tool', 'Free dashboards from Google Sheets and Google data', 'Free, but accounting connectors usually need a paid third-party connector.')

prod('m365bp', 'sec', 'Microsoft 365 Business Premium', '133301', G, ['s', 'm'], 1, ['Cloud'], 'Canadian data centres', 'Device management, threat protection and MFA in one plan', 'Security features only help once switched on; most firms need an IT partner to configure them.')
prod('acronis', 'sec', 'Acronis Cyber Protect', '302100', G, ['s', 'm'], 1, ['Cloud', 'On-premise'], 'Canadian data centre options', 'Backup of servers, PCs and Microsoft 365', 'Test a full restore at least twice a year.')
prod('1password', 'sec', '1Password Business', '020030', G, ['s', 'm', 'l'], 1, ['Cloud'], 'Canadian company (Toronto)', 'Shared passwords and MFA for teams', 'Adoption depends on removing old password spreadsheets.', ca=True)
prod('knowbe4', 'sec', 'KnowBe4', '000203', G, ['s', 'm', 'l'], 1, ['Cloud'], 'Serves Canadian businesses', 'Phishing tests and staff security training', 'Training works when results are reviewed with staff, not just sent.')

prod('copilot', 'ai', 'Microsoft 365 Copilot Business', '3323332', G, ['s', 'm'], 1, ['Cloud'], 'Microsoft 365 add-on', 'Firms already working in Microsoft 365', 'An add-on to an eligible Microsoft 365 plan; promotional first-year pricing ends Dec 31, 2026.', v=1, src='https://www.microsoft.com/en-us/microsoft-365/blog/2025/12/02/microsoft-365-copilot-business-the-future-of-work-for-small-businesses/')
prod('chatgpt', 'ai', 'ChatGPT Business', '3331333', G, ['s', 'm'], 1, ['Cloud'], 'Business plan', 'A standalone AI workspace for teams', 'Separate from Office apps, so adoption needs deliberate habits; two-seat minimum.', v=1, src='https://coworker.ai/blog/chatgpt-enterprise-pricing')
prod('claude', 'ai', 'Claude Team', '3332333', G, ['s', 'm'], 1, ['Cloud'], 'Business plan', 'Teams working with long documents, analysis and automation', 'Team plans have a seat minimum; heavy users may need the higher-usage seats.', v=1, src='https://www.layer3labs.io/guides/ai-subscription-plans-for-business')
prod('gemini', 'ai', 'Gemini in Google Workspace', '3323332', G, ['s', 'm'], 1, ['Cloud'], 'Included in Workspace plans', 'Firms already on Google Workspace', 'Included with Workspace, with usage limits by plan.', v=1, src='https://ecorpit.com/copilot-vs-gemini-vs-chatgpt-vs-claude-business-pricing-2027/')

# ---------------- ERP and WMS from erp_data.json ----------------
DI = {  # distribution workflow scores for ERP vendors
  'epicor': '32322333', 'gss': '22221232', 'm1': '11211222', 'proshop': '11200121', 'infor-csi': '32322333', 'bc': '32321333',
  'acumatica': '33332333', 'netsuite': '33322333', 'sapb1': '22221232', 'syspro': '33332333', 'invera': '32322232',
  'deacom': '22322232', 'batchmaster': '11210131', 'aptean-pm': '22322232', 'sagex3': '33332333', 'odoo': '32321333'}
ERPIND = {'invera': ['mfg', 'dist'], 'deacom': ['mfg', 'agri'], 'batchmaster': ['mfg'], 'aptean-pm': ['mfg', 'agri'], 'proshop': ['mfg'], 'm1': ['mfg'], 'gss': ['mfg']}
erp_v, wms_v = [], []
for v in ERP['vendors']:
    if v['id'] in ('katana', 'mrpeasy', 'fishbowl'):
        continue
    base = dict(v)
    if v['type'] == 'Standalone WMS':
        base['inds'] = ['dist', 'retail', 'trans', 'mfg']
        wms_v.append({**base, 'tag': 'Standalone WMS'})
        continue
    base['inds'] = ERPIND.get(v['id'], ['mfg', 'dist'])
    if v['id'] == 'invera': base['ca'] = True
    s = dict(v['s']); s['di'] = [int(x) for x in DI[v['id']]]
    base['s'] = s
    erp_v.append(base)
    if s.get('wm') and sum(s['wm']) >= 15:
        wms_v.append({**base, 'tag': 'ERP with warehouse module'})
wf = [w for w in ERP['workflows'] if w['id'] != 'wm']
wf.append({'id': 'di', 'name': 'Wholesale distribution', 'short': 'Distribution',
           'desc': 'Distributors buying, stocking and reselling: pricing, purchasing, landed cost, EDI and multiple warehouses.',
           'caps': [{'k': 'whse', 'n': 'Multi-warehouse', 'd': 'Stock and transfers across warehouses.'},
                    {'k': 'price', 'n': 'Pricing and rebates', 'd': 'Customer price lists, contracts and rebates.'},
                    {'k': 'repl', 'n': 'Purchasing and replenishment', 'd': 'Reorder suggestions and supplier management.'},
                    {'k': 'landed', 'n': 'Landed cost', 'd': 'Freight, duty and brokerage added to item cost.'},
                    {'k': 'edi', 'n': 'EDI', 'd': 'Electronic orders, ASNs and invoices with large customers.'},
                    {'k': 'drop', 'n': 'Drop-ship and back-orders', 'd': 'Ship direct from suppliers; manage back-orders.'},
                    {'k': 'lot', 'n': 'Lot and serial', 'd': 'Lot, expiry and serial tracking.'},
                    {'k': 'rma', 'n': 'Returns (RMA)', 'd': 'Customer returns and credits.'}]})
wms_caps = [w for w in ERP['workflows'] if w['id'] == 'wm'][0]['caps']
for c in C:
    if c['id'] == 'wms':
        c['caps'] = wms_caps

# ---------------- functions, levels, priorities, problems ----------------
functions = [{'id': 'fin', 'name': 'Finance', 'short': 'Finance'}, {'id': 'sales', 'name': 'Sales and marketing', 'short': 'Sales'},
             {'id': 'ops', 'name': 'Operations', 'short': 'Operations'}, {'id': 'people', 'name': 'People and HR', 'short': 'People'},
             {'id': 'it', 'name': 'IT, data and security', 'short': 'IT and data'}]
levels = [{'n': 'Manual', 'd': 'Paper, whiteboards, phone and memory.'}, {'n': 'Digitized', 'd': 'Spreadsheets and stand-alone apps; data is re-typed between them.'},
          {'n': 'Connected', 'd': 'One main system per area, linked so data is entered once.'}, {'n': 'Optimized', 'd': 'Automated workflows and live dashboards drive decisions.'}]
level_examples = {
  'fin': ['Shoebox receipts, manual invoices', 'Bookkeeping software, spreadsheet budgets', 'Accounting linked to sales, payroll and bank feeds', 'Automated close, live cash-flow and margin dashboards'],
  'sales': ['Referrals and phone; no customer list', 'Contacts in Outlook or a spreadsheet', 'CRM, store or booking system linked to accounting', 'Automated follow-up, marketing and sales forecasting'],
  'ops': ['Paper tickets, whiteboard schedule', 'Spreadsheets for schedules, jobs or stock', 'One system for jobs, stock and purchasing', 'Real-time tracking, scanning and capacity planning'],
  'people': ['Paper timesheets, manual payroll', 'Online payroll; HR records in folders', 'Time tracking, payroll and HR in one place', 'Self-serve onboarding, scheduling and training records'],
  'it': ['Personal devices and email; no backups', 'Shared drives; some cloud apps', 'Managed accounts, backups and multi-factor sign-in', 'Security monitoring, data warehouse and AI tools in use']}
priorities = [
  {'id': 'grow', 'name': 'Grow sales', 'w': {'sales': 3, 'fin': 1, 'ops': 1}},
  {'id': 'margin', 'name': 'Protect margins and control costs', 'w': {'fin': 3, 'ops': 2}},
  {'id': 'scale', 'name': 'Grow without adding staff', 'w': {'ops': 3, 'people': 1, 'it': 1}},
  {'id': 'admin', 'name': 'Cut admin and paperwork time', 'w': {'fin': 2, 'people': 2, 'ops': 1, 'it': 1}},
  {'id': 'cx', 'name': 'Deliver on time and keep customers happy', 'w': {'ops': 2, 'sales': 2}},
  {'id': 'quality', 'name': 'Improve quality and compliance', 'w': {'ops': 2, 'it': 1}},
  {'id': 'data', 'name': 'Make decisions with better data', 'w': {'it': 2, 'fin': 2}},
  {'id': 'risk', 'name': 'Reduce risk (cyber, key-person, cash)', 'w': {'it': 3, 'people': 1, 'fin': 1}}]
# category tokens: mfgsys -> MRP for small firms, ERP for larger; whsys -> inventory for small, WMS for larger; distsys -> inventory for small, ERP for larger
PR = []
def pb(fn, ind, t, c):
    PR.append({'id': 'p%d' % (len(PR) + 1), 'fn': fn, 'ind': ind, 't': t, 'c': c})
# common
pb('fin', G, 'Month-end takes too long and the numbers come late', ['acct', 'bi'])
pb('fin', G, 'Invoicing is slow and customers pay late', ['acct', 'fsm', 'psa'])
pb('fin', G, 'Cash flow surprises us', ['acct', 'bi'])
pb('sales', G, 'Leads and follow-ups fall through the cracks', ['crm'])
pb('sales', G, 'We have no clear view of the sales pipeline', ['crm', 'bi'])
pb('sales', G, 'Marketing is ad hoc and we don\'t stay in touch with past customers', ['mkt', 'crm'])
pb('people', G, 'Timesheets and payroll take hours each pay period', ['payroll'])
pb('people', G, 'Onboarding and training records are on paper', ['payroll', 'collab'])
pb('people', G, 'Too much knowledge sits with one or two people', ['collab', 'ai'])
pb('it', G, 'Files live on personal laptops or one old server', ['collab', 'sec'])
pb('it', G, 'We have no tested backup or ransomware plan', ['sec'])
pb('it', G, 'Reports are built by hand in Excel', ['bi'])
pb('it', G, 'Our systems don\'t talk to each other, so we re-type data', ['acct', 'bi'])
pb('it', G, 'Repetitive writing and admin (emails, quotes, reports) eats our time', ['ai'])
pb('it', G, 'Staff use AI tools with no rules on what data goes in', ['ai', 'sec'])
# manufacturing
pb('fin', ['mfg'], 'We don\'t know which jobs or products actually make money', ['mfgsys', 'bi'])
pb('sales', ['mfg'], 'Quotes take too long or miss costs', ['mfgsys', 'crm'])
pb('ops', ['mfg'], 'Production scheduling lives on a whiteboard', ['mfgsys'])
pb('ops', ['mfg'], 'We run out of materials or hold too much stock', ['mfgsys', 'inv'])
pb('ops', ['mfg'], 'We can\'t trace lots, heats or serial numbers quickly', ['mfgsys', 'inv'])
pb('ops', ['mfg'], 'We don\'t know real-time job status on the shop floor', ['mfgsys'])
pb('ops', ['mfg'], 'Quality records and non-conformances are on paper', ['mfgsys', 'collab'])
# construction
pb('ops', ['con'], 'Crews, jobs and schedules are juggled by phone and text', ['fsm'])
pb('ops', ['con'], 'Change orders and RFIs get lost', ['cpm'])
pb('ops', ['con'], 'Site photos, drawings and daily reports are scattered', ['cpm', 'collab'])
pb('fin', ['con'], 'We only know a job\'s profit after it is finished', ['cpm', 'fsm', 'acct'])
pb('sales', ['con'], 'Estimates and quotes take too long', ['fsm', 'cpm', 'crm'])
pb('ops', ['con', 'svc', 'dist'], 'We don\'t know where our vehicles and crews are', ['tms', 'fsm'])
# distribution
pb('ops', ['dist'], 'Inventory counts are wrong or we run out of stock', ['whsys', 'inv'])
pb('ops', ['dist'], 'Picking and shipping errors', ['whsys'])
pb('sales', ['dist'], 'Customers can\'t order or check stock online', ['ecom', 'inv'])
pb('sales', ['dist'], 'Big customers send EDI or PDF orders that we re-type', ['distsys'])
pb('fin', ['dist'], 'Customer pricing and landed costs live in spreadsheets', ['distsys'])
pb('ops', ['dist'], 'Purchasing is reactive and suppliers are chased by email', ['distsys', 'inv'])
# retail
pb('ops', ['retail'], 'Store and online stock don\'t match', ['pos', 'inv', 'ecom'])
pb('sales', ['retail'], 'Checkout is slow or our POS is outdated', ['pos'])
pb('fin', ['retail'], 'We don\'t know our best sellers and margins by item', ['pos', 'bi'])
pb('sales', ['retail'], 'We have no loyalty program or repeat-customer marketing', ['pos', 'mkt'])
pb('sales', ['retail'], 'We want to sell online but don\'t have a store', ['ecom'])
pb('ops', ['retail'], 'Order fulfilment and returns are slow', ['whsys', 'ecom'])
# professional services
pb('fin', ['prof'], 'Billable hours slip through and aren\'t invoiced', ['psa'])
pb('ops', ['prof'], 'We can\'t see who has capacity for new work', ['psa'])
pb('ops', ['prof'], 'Client files and document versions are scattered', ['collab', 'psa'])
pb('sales', ['prof'], 'Proposals and engagement letters are built by hand', ['crm', 'ai'])
pb('fin', ['prof'], 'Projects go over budget before we notice', ['psa', 'bi'])
# health
pb('ops', ['health'], 'No-shows and manual appointment reminders', ['clinic', 'booking'])
pb('fin', ['health'], 'Insurance billing and claims are slow and manual', ['clinic'])
pb('ops', ['health'], 'Paper intake forms and charting', ['clinic'])
pb('it', ['health'], 'We worry about patient privacy and where data is stored', ['clinic', 'sec'])
pb('sales', ['health'], 'Patients can\'t book online', ['clinic', 'booking'])
# food
pb('people', ['food'], 'Staff scheduling and labour costs are hard to control', ['payroll'])
pb('fin', ['food'], 'We don\'t know our food cost and waste', ['inv', 'pos'])
pb('sales', ['food'], 'Delivery-app and online orders are re-keyed into the POS', ['pos'])
pb('sales', ['food'], 'Reservations and online ordering are clumsy', ['pos', 'booking'])
pb('fin', ['food'], 'Daily sales and tips reconciliation takes too long', ['pos', 'acct'])
# transportation
pb('ops', ['trans'], 'Hours-of-service and ELD compliance worries us', ['tms'])
pb('ops', ['trans'], 'Dispatch runs on phone calls and a whiteboard', ['tms'])
pb('sales', ['trans'], 'Customers keep calling to ask where their load is', ['tms'])
pb('fin', ['trans'], 'Proofs of delivery are paper and loads are invoiced late', ['tms', 'acct'])
pb('ops', ['trans'], 'Fuel tax (IFTA) and maintenance records are manual', ['tms'])
pb('ops', ['trans'], 'Warehouse stock for clients is tracked in spreadsheets', ['whsys'])
# real estate
pb('fin', ['re'], 'We chase tenants for rent every month', ['prop'])
pb('ops', ['re'], 'Maintenance requests arrive by text and get lost', ['prop'])
pb('fin', ['re'], 'Owner statements are built in Excel', ['prop', 'acct'])
pb('sales', ['re'], 'Leasing, applications and screening are manual', ['prop'])
# agriculture
pb('ops', ['agri'], 'Field records are on paper or in our heads', ['farm'])
pb('fin', ['agri'], 'We don\'t know cost of production by field or crop', ['farm', 'bi'])
pb('ops', ['agri'], 'Grain and input inventory isn\'t tracked', ['farm', 'inv'])
pb('fin', ['agri'], 'Our accounting isn\'t built for farming', ['farm', 'acct'])
pb('sales', ['agri'], 'We want to sell direct to customers online', ['ecom'])
# personal and repair services
pb('sales', ['svc'], 'Bookings happen by phone; no online booking', ['booking'])
pb('ops', ['svc'], 'No-shows and last-minute cancellations', ['booking'])
pb('ops', ['svc'], 'Technician or crew scheduling is chaotic', ['fsm'])
pb('sales', ['svc'], 'We don\'t market to repeat customers', ['mkt', 'booking'])
pb('fin', ['svc'], 'Payments and deposits are collected manually', ['booking', 'pos'])

data = {'as_of': AS_OF, 'version': 'Draft V3',
        'industries': [{'id': i, 'name': n, 'desc': d, 'smes': k} for i, n, d, k in industries],
        'industry_source': 'ISED, Key Small Business Statistics 2025, Table 3 (employer businesses with 1–499 employees, December 2024)',
        'industry_source_url': 'https://ised-isde.canada.ca/site/sme-research-statistics/en/node/439',
        'mfg_types': [{'id': 'mf', 'name': 'Make-to-order, job shop or fabrication'}, {'id': 'co', 'name': 'Coil, sheet or bar processing'},
                      {'id': 'bp', 'name': 'Batch, formula or chemical production'}, {'id': 'mf2', 'name': 'Repetitive assembly or make-to-stock', 'wf': 'mf'}],
        'functions': functions, 'levels': levels, 'level_examples': level_examples, 'priorities': priorities,
        'problems': PR, 'categories': C, 'products': P,
        'erp': {'workflows': wf, 'vendors': erp_v}, 'wms': {'vendors': wms_v}}
out = ROOT / 'content/assess/assess_data.json'
out.write_text(json.dumps(data, ensure_ascii=False, indent=1))
nv = sum(p['v'] for p in P)
print('industries', len(industries), 'problems', len(PR), 'categories', len(C), 'products', len(P), '+ erp', len(erp_v), '+ wms', len(wms_v), 'verified', nv)
for c in C:
    if c['id'] not in ('erp', 'wms'):
        for p in P:
            if p['cat'] == c['id'] and len(p['s']) != len(c['caps']):
                print('LEN MISMATCH', p['id'], len(p['s']), len(c['caps']))
