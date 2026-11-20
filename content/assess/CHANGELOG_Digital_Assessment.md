# Digital Assessment page (formerly ERP Matrix) — changelog

## Draft V6 — 2026-11-19 (not published)
- **Legend added above every capability matrix** in the Software Finder (all 22 categories and all ERP workflows): Native (3), Configurable (2), Add-on or partner app (1), Not supported or custom (0), plus what Fit, the $–$$$$ cost band, ✓ (company facts checked) and 🍁 (Canadian company) mean. The legend was lost in V3 when every category became a matrix; previously the meaning was only in hover tooltips.

## Draft V5 — 2026-11-19 (not published)
- **Consistent ERP view for every industry:** the Workflow dropdown now appears for all 11 industries; the "ERP workflows are not set up…" message no longer appears for any industry.
- **New "General business ERP (any industry)" workflow** (multi-entity financials, payables automation, billing, inventory, CRM, projects, reporting, Canadian tax and payroll links), scored for 12 ERPs.
- **5 new industry workflows** (17 in total): Logistics and 3PL (transportation), Multi-location hospitality (restaurants), Multi-site clinics and health services (health), Real estate and property ERP (real estate), Field service businesses (personal and repair services; also construction). Each has 8 capabilities with a scoring guide. When an industry is selected, the dropdown opens on that industry's own workflow; "General" stays available.
- **5 new ERP products, company facts checked 2026-11-19:** Restaurant365 (per-location pricing), Magaya Supply Chain (Canada eManifest with CBSA), Yardi Voyager (CAM reconciliation for larger portfolios), MRI Software (Canadian cloud hosting in Toronto and Quebec), ServiceTitan (serves Canadian contractors). Existing ERPs scored on the new workflows where they apply. 28 ERP products in total.
- **Assessment:** transportation, restaurants, clinics, real estate and personal services map automatically to their workflow; farms map to General. 7 new problems (3PL billing, location P&L, multi-clinic consolidation, practitioner splits, CAM reconciliation, service agreements, multi-company consolidation) with right-sizing (small firms → WMS, accounting, property management or field service tools; larger → ERP). 95 problems in total.
- Data builder now `content/assess/build_data_v5.py`.
- Still preliminary: capability scores, cost bands and Reality Checks.

## Draft V4 — 2026-11-19 (not published)
- **ERP workflows: 4 → 11.** Added repetitive and make-to-stock, engineer-to-order and project manufacturing, food and beverage processing, food distribution, omnichannel brands, construction ERP and services ERP. Each has 8 capabilities.
- **Scoring guide:** every ERP capability now states what "native" means (e.g. holdback: progress draws with holdback withheld and released, tracked by job). Shown under the matrix ("How these capabilities are scored") and in each product profile.
- **Workflow list follows the industry:** the dropdown shows only workflows that fit the selected industry, grouped (Manufacturing; Food; Distribution and commerce; Construction; Professional services). Industries without ERP workflows get an explanation and a "Show ERP for all industries" button instead of "0 products". Other empty categories show a "Show all industries" button.
- **7 new ERP products, company facts checked 2026-11-19:** Jonas Construction Software (Canadian), Maestro*ERP (Varennes, Quebec; JDM Technology Group since 2020), Sage Intacct Construction and Projects (available in Canada), Aptean Food & Beverage ERP (on Business Central), IFS Cloud, Deltek Vantagepoint, Brightpearl by Sage. Acumatica renamed to cover all editions; its Construction Edition retainage/holdback support checked. 23 ERP products in total, scored on every workflow they serve.
- **Assessment picks the workflow automatically:** new follow-up questions for manufacturing (6 production types), distribution (wholesale, food, omnichannel brand) and agriculture (farm or food processing); retail, construction and professional services map automatically.
- **Problem library: 88** (13 new), incl. workflow-specific problems shown only for the matching business type (e.g. CFIA recall, OEM EDI releases, engineering changes, holdbacks, union payroll, revenue recognition).
- **Right-sizing extended:** construction (small → construction project management; larger → construction ERP), professional services (small → practice management; larger → services ERP), omnichannel (small → inventory; larger → ERP). Small food processors are offered MRP products with lot tracking.
- Data builder now `content/assess/build_data_v4.py` (V3 builder kept for history). Fixed: WMS listings copied from ERPs now carry industry tags.
- Still preliminary: capability scores, cost bands and Reality Checks.

## Draft V3 — 2026-11-19 (not published)
- **Capability matrix in every category** (as in the V1 ERP view): fit score, 6–8 capability dots, deployment and cost band; product profiles list each capability with its rating. One consistent layout; the industry filter applies to all categories; ERP adds a "Workflow" dropdown instead of large tabs.
- **ERP, MRP and WMS split** into separate categories. New MRP capability set (BOMs, routings, MRP, scheduling, shop floor, costing, lot/serial, QuickBooks/Xero link). New ERP "Wholesale distribution" workflow (multi-warehouse, pricing and rebates, replenishment, landed cost, EDI, drop-ship, lot/serial, returns). WMS lists standalone WMS and ERPs with strong warehouse modules, tagged.
- **Right-sized recommendations:** problems point to "manufacturing system", "warehouse system" or "distribution system", resolved by staff size and budget (small → MRP or inventory software; larger → ERP or WMS). ERP is never the quick win.
- **11 industries** with Canadian SME counts from ISED Key Small Business Statistics 2025 (Table 3, Dec 2024): manufacturing; construction and trades; wholesale and distribution; retail and e-commerce; professional services; health and wellness clinics; restaurants and hospitality; transportation and logistics; real estate and property management; agriculture and agri-food; personal and repair services. Together 966,000+ employer SMEs.
- **Problem library: 75 problems** (15 common to all industries plus industry-specific sets), incl. AI use and AI governance problems.
- **22 categories** (was 11): added email and marketing, point of sale, online booking, clinic management and EMR, practice and project management, MRP, WMS, fleet and transportation, property management, farm management, AI assistants.
- **111 product entries** (80 category products + 16 ERP + 15 WMS listings). Company facts for 23 products checked against current sources on 2026-11-19 and marked ✓ with the source link in the profile, including: Employment Hero (formerly Humi), Jane, Juvonno, OSCAR Pro (WELL Health), Clio, Lightspeed, TouchBistro, 7shifts, MarketMan, Katana pricing model, Fishbowl, Geotab, ISAAC (Transport Canada-certified ELD), Rose Rocket, Buildium (Canadian GST), Yardi Breeze (Canadian version), AgExpert (FCC), and the business AI plans (Microsoft 365 Copilot Business, ChatGPT Business, Claude Team, Gemini in Workspace).
- Fit scores for options capped at 95%. New "Sources" section on the page.
- Data source of truth is now `content/assess/build_data_v3.py` (writes `assess_data.json`); `content/erp/erp_data.json` is read by it for ERP and WMS vendors.
- Still preliminary: capability scores, cost bands and Reality Checks.

## Draft V2 — 2026-11-19 (not published)
- **Renamed** from "ERP Matrix" (`erp-matrix.html`) to "Digital Assessment" (`digital-assessment.html`). Menu label "Digital Assessment" after AI Models, shown on this page only until approval. `erp-matrix.html`, `assets/js/erp.js` and `content/gen/erp_page.py` are superseded; `assets/css/erp.css` and `content/erp/erp_data.json` are reused.
- **New five-step needs assessment** (`assets/js/assess.js`, data in `content/assess/assess_data.json`):
  1. Your business: industry, production type (manufacturing only), staff, current tools
  2. Priorities: up to 3 of 8 business priorities, each weighting the five functions
  3. Challenges: up to 5 problems, filtered by industry and grouped by function (24 in the starter library)
  4. Digital maturity: finance, sales and marketing, operations, people and HR, IT/data/security, each rated today and in two years on Manual → Digitized → Connected → Optimized, with examples per function
  5. Budget for the first project
- **Digital roadmap results:** maturity radar chart, gap table, top 3 technology priorities (Must/Should/Could) with reasons and "Compare products" links, one quick win (time to value, risk, cost, function; never an ERP project), three software options with fit score, Canada note, cost band, Reality Check and warnings, links to related courses and posts and the Funding finder.
- **Report and lead capture:** Download PDF (roadmap only), and "Email me the full roadmap report" via Web3Forms to info@chmltech.com with roadmap summary and answers, CASL consent, and an optional free 30-minute roadmap review.
- **Software Finder:** 11 categories (accounting, payroll/HR, CRM, field service, construction PM, inventory, ERP/MRP/WMS, e-commerce/B2B, collaboration, reporting, backup/security) with industry filter and product profiles. The ERP, MRP and WMS category keeps the V1 capability matrix with its four workflow sub-tabs.
- **Starter data:** 3 industries (manufacturing, construction and trades, wholesale and distribution), 36 products in 10 categories plus 23 ERP/WMS products. All marked draft and unverified.
- Your own method wording and maturity scale names (not the CDAP toolkit's).

## Draft V1 — 2026-11-19 (not published)
- ERP Matrix page: 23 ERP/WMS products, 4 workflows × 8 capabilities, shortlist wizard, scorecard PDF and email form.

## V24 — 2026-11-20 — Full report in the email
- The report request email now carries the full report as plain text, in 12 numbered sections: your business (with report date, size, budget, tools, priorities), challenges, digital maturity (today → target, gaps), technology priorities with reasons, first project (time, risk, cost, free resources), software options (fit, best for, year-one cost, Canada, reality check, website), demo questions, action plan, more vendors, AI tools, funding, next step. Replaces the one-line "roadmap" and coded "answers" fields.
- AI suggestions (on screen and in the email) now come from the compared shortlist for each job, best fit first, grouped by job; "Compare … tools" jumps to that job.
- Form wording made honest: "Request my full report"; "We email it within one business day"; success message updated. The visitor does not receive an automatic email (Web3Forms free plan); Chmltech forwards the report.

## V23 — 2026-11-20 — Launch
- Page made indexable (robots noindex removed); added to sitemap.xml (priority 0.9).
- "Digital Assessment" added to the site menu on every page (top level, post/ and challenge-page/); "About" removed from the top menu site-wide (footer link kept).
- Menu spacing tightened for 981–1260px so the header fits; asset version stamps refreshed (assetver.py).
- Results booking button points to book.html (book-online.html is a redirect).
- Not published: the superseded ERP Matrix V1 draft (erp-matrix.html, erp.js, erp_page.py) and the source Excel master lists (repository is public). Builders expect the lists in content/assess/sources/ when rebuilding locally.

## V22 — 2026-11-20 — Pre-publication confirmation pass
- Removed the claim that data comes from "our implementation experience with Canadian SMEs"; Method now says vendor documentation and public sources.
- Price notes added: AI tools and Method ("checked November 2026, in US dollars unless marked"); Vendor Directory ("as published by vendors, usually US dollars").
- Research agents (3) confirmed open items with vendor sources (build_data_v22.py, confirm_v22/):
  - AI comparison: 45 scores confirmed, 14 corrected (e.g., Apollo, Klaviyo, Intercom, Tidio French → 3; MailMaestro shared templates → 0; 1Password suite 3 → 2 by editorial rule); 7 of 424 remain unconfirmed and flagged.
  - Software Finder: 12 capability scores lowered to match vendor sources (e.g., Odoo and Acumatica 3PL connections 3 → 1; Sage X3 and SYSPRO temperature zones 3 → 2; OSCAR Pro telehealth 2 → 1); 5 low-confidence items stay flagged (lower score applied, never overstated).
  - Vendor Directory: 40 fixes (TCS iON removed; 8 duplicates removed; ~20 category moves such as ShipStation, ShipMonk, FBA → shipping and Katana → MRP; CRM Dynamics → HSO, iLobby → FacilityOS).

## V21 — 2026-11-20 — AI tools comparison (capability matrix per job)
- Research agents (3) picked 6 tools per job for Canadian SMEs and scored 8 columns from vendor pages: 4 shared (free plan or trial, works in Microsoft 365 or Google, French language, data stays private) + 4 job-specific. Developer tools stay a plain list.
- Independent review (2 reviewers): 13 corrections applied (e.g., Otter, Klaviyo, QuickBooks privacy to 0; KnowBe4 privacy 3→1; Zoho Analytics French 3→1; Workable and BambooHR French up; Claude Team voice 3→2), 76 scores confirmed, Relay.app removed (shut down Sept 2026; also removed from the AI list). 65 of 424 scores remain unconfirmed and are flagged in each tool profile.
- Layout: job view shows "Compared: 6 tools" matrix (fit, dots, short price tag) then "More tools (not compared)"; mobile cards; tool profile with price, Canadian note, Reality Check, each capability with note and source link; overview cards link "Compare the top 6"; shared columns use their own wording (e.g., Full French / English only).
- Files: ai_matrix_spec.json, ai_research/research_{A,B,C}.json, verify_R{1,2}.json, review_log_v21.json, build_data_v21.py.

## V20 — 2026-11-20 — Full method rows aligned
- "Full method" fold-out: label and description now sit on the same line in each row (shared padding and divider, baseline-aligned); stacked on mobile.

## V19 — 2026-11-20 — AI tools section redesign (UI agent)
- One control bar: Job dropdown, search with icon, live count (replaces 11 chips).
- "All jobs" shows an overview card per job (count, top 3 picks, "See all N … tools"); developer tools behind a small "For IT staff" link.
- Single-job and search views: compact rows (name, 2-line description, price); "← All jobs"; "Show 12 more (8 of 51 shown)".
- Short price badges ("Free plan" + "Paid from $12/mo", "From $19/user/mo", "Price on request"); full vendor price text in a tooltip.
- No arrow after tool names; US-focused tools (e.g., Brex) listed after others; reviewer notes removed from two price fields (Elpass, Hostinger Horizons).

## V18 — 2026-11-20 — Arrow removed from website link
- Profile website link shows the product name only (no ↗).

## V17 — 2026-11-20 — Website link shows the product name
- Profile website link now reads the product name (e.g., "FreshBooks ↗") and wraps inside its box; removed the no-wrap rule that pushed the domain outside.

## V16 — 2026-11-20 — Website link in product profile
- Profile shows the domain only (e.g., "sage.com ↗"); the link still opens the full product page. CSS keeps any long value inside its box.

## V15 — 2026-11-20 — UI clean-up (UI QC review, 45 findings)
- Hero: one primary button + "or browse software" link; 3 stats instead of 6; shorter intro. Draft banner removed.
- Assessment: compact 5-step intro; "Question N of 8" counter; industry options without statistics; option text aligned.
- Software Finder: category and industry dropdowns replace 34 chips; one-line legend; "Year-one cost" column (Deployment moved to profile); top 8 products with "Show all"; mobile card view; ERP "Type of business" helper text; acronym-safe labels ("ERP", "WMS").
- Vendor Directory: 10 rows by default (+20); rows show name, description, category, based in, price; "Compare →" replaces the pill; "Checked", "Update" and "Built for" lists removed from rows; descriptions cleaned (no "Canada: …" or city prefixes, 166 rows); duplicate scored-vendor listings merged (11, e.g., Invera); mobile card view.
- AI Tools: 10 owner-facing groups replace 26 categories and the use-case filter; developer tools only when chosen or searched; 8 cards by default (+12); cards show name, description, price.
- Results: no horizontal scroll on mobile; gap table folds away on mobile; "Priority 1 · Must" labels; "fit", "In Canada", "Year-one cost"; shorter notes; AI suggestions exclude developer and professional-firm tools for other industries; booking button added and checkbox removed from the email form; "Email my report".
- Product profile: Reality Check before capabilities; plain capability levels (Built in, Set up without code, Add-on, Not offered); no "Draft" pills; short source note; icon close button.
- Method: 3 cards (How we rank, Where the data comes from, Independence) plus a "Full method" fold-out.
- Global: scroll offset for the sticky header; consistent buttons.
- build_data_v15.py (data tidy + AI groups).

## V14 — 2026-11-20 — Page trimmed; vendor submission link
- Removed from the page: Independent review section, Sources section and What changed (snapshot history). Full history stays in this changelog and the review reports.
- "Vendors can submit product information" now links to https://www.chmltech.com/contact?service=Vendor%20product%20submission&topic=vendor (absolute, so it also works from the preview file).
- contact.html: new service option "Vendor product submission (Digital Assessment)". main.js: ?topic=vendor pre-fills the message with a product-information template (company, product, category, website, Canadian presence, customer size, industries, pricing, documentation links).

## V13 — 2026-11-20 — Website links for every listing
- User report: no website link on QuickBooks Online, Sage 50 and other scored products.
- scored_urls_v13.json: official website for all 90 scored products (product profiles and their directory listings); each loaded on 2026-11-20 (bot-blocking 403/429 counted as live).
- Full link check of all 1,192 unique URLs on the page: 1,117 load or are bot-blocked; 24 links fixed: moved or 404 pages replaced with the vendor homepage, and wrong domains corrected (Riva → rivaengine.com, Camelot → 3plsoftware.com, Cadence WMS → cadretech.com, Clearword → clearword.com, Skustack → sellercloud.com) via url_fixes_v13.json.
- Not confirmable from the build server (sites block automated checks or the server's network): about 30 links, mostly small Canadian partners; left in place.
- build_data_v13.py; result: 0 listings, products or AI tools without a website.

## V12 — 2026-11-20 — Plain wording
- "✓ Red-team checked Nov 2026" is now "✓ Checked Nov 2026" (tooltip: confirmed against the vendor's own website by an independent reviewer).
- Other visitor-facing "red team" wording replaced with "independent review" (validation heading, method card, What changed, product profile note). Internal file names and reports keep the term.

## V11 — 2026-11-20 — Directory search and industry filter
- User report: industry filter did nothing within a category (e.g., CRM + Restaurants); search for "Quick" returned only a description match.
- build_data_v11.py: adds the 88 scored products that were missing from the directory (e.g., QuickBooks Online, HubSpot, Square); tags every listing with the industries it is built for (scored products use their scored industry fit; other listings use keyword rules with vertical-group fallbacks); untagged = general.
- assess.js: industry filter keeps listings built for that industry plus general ones and hides those built for other industries; industry-specific first with a "Built for" label and a count; search ranks name-start, then name, then description matches; shows "N more name matches hidden by your filters: clear filters"; "More vendors" in results uses the same industry logic.

## V10 — 2026-11-20 — Red-team review of directory and AI tools
- Five independent reviewers (A–E) checked all 781 directory listings and 475 AI tools; findings in content/assess/redteam_v10/.
- build_data_v10.py applies 323 evidence-backed corrections (log: redteam_v10_log.json); removes 51 directory listings and 21 AI tools; adds acquisition "Update" notes and ✓ on 441 confirmed listings.
- assess.js: size-honest "More vendors" (confirmed size first, "size not stated", priority lead-in, AI category skipped); AI suggestions limited to free or low published price and one category per problem; revised problem→AI map; safeUrl on all data links; JSON embed escapes U+2028/2029.
- Page: banner Draft V10, second red-team block in the validation section, updated method text.
- Report: REDTEAM_V10_REPORT.md.

## V9 — 2026-11-20 — Vendor directory and AI tools
- Sources: ERP Master List 2025 v2, WMS Master List 2025 V2, WMS Canada 2026 V1, Canadian Software/IT/AI Companies 2026 V2, Canadian Technology Companies V5, AI Tools Master List v8 (copied to content/assess/sources/).
- New build_dir_v9.py: extracts all lists, de-duplicates by name and website, maps each listing to an assessment category, a specialist-software group (MES, CMMS, quality, supply chain, shipping, automation, payments, learning, IT ops, energy) or a service-partner group (implementation, managed IT, web agencies, AI specialists). 781 listings, 564 Canadian; 36 linked to scored products. Hand overrides for 12 misread entries.
- New build_data_v9.py: V7 data + directory + 475 AI tools in 26 categories + problem-to-AI-category map for 37 problems; adds vendor websites to 33 scored products (no other field changed; red-team corrections untouched).
- Page: new Vendor Directory section (search, category, industry, size, Canadian-only, show more); new AI Tools section (category chips, use-case filter, search); results show "More vendors to consider" sized to the business and "AI tools that can help with your challenges"; Software Finder links to the directory; product profiles show the website.
- Directory listings and AI tools are not scored and were not part of the V7 red-team review; the page says so.

## V8 — 2026-11-20 — Report form fix
- "Send my report" appeared to do nothing when a field was empty or consent unticked, because the browser's validation pop-up does not show in every viewer. assets/js/main.js now shows an on-page message listing what is missing and highlights the fields (applies to all site forms).
- When sending fails inside a preview or a local file, the message says sending is blocked in the preview and offers the email fallback.
- Note: Web3Forms only accepts submissions from a browser on a real web page; it cannot be tested from the preview panel.

## V7 — 2026-11-20 — Red-team validation
- Four independent reviewers checked data and logic (A 35 findings, B 50, C 29, D 13 data + 17 logic).
- 115 evidence-backed data corrections applied via build_data_v7.py (log: redteam_v7_log.json); 13 scores flagged unconfirmed and shown on product profiles.
- Logic fixes L1–L17 in assess.js: no ERP quick win, "First project" label, budget check, right-sizing, owned-tool handling, problem-weighted fit, raw-score ranking, suite-aware AI picks, fallback routing.
- New follow-up questions: professional firms (legal/accounting/other), service businesses (salon/auto/home), contractors (construction/field service); coverage-gap notices.
- New "Red-team validation" section on the page; method wording updated; banner Draft V7.
- Report: REDTEAM_V7_REPORT.md.

