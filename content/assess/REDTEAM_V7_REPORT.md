# Red-Team Validation Report — Digital Needs Assessment and Software Finder (Draft V7)

Review date: November 20, 2026 · Data as of November 19, 2026 · Page: digital-assessment.html (draft, noindex, not pushed)

## Method

Four independent reviewers, none of whom built the data, each took a slice and checked it against vendor documentation, pricing pages and official sources:

| Reviewer | Scope | Findings | Confirmed as correct |
|---|---|---|---|
| A | ERP and WMS vendors, workflow scores | 35 | 18 |
| B | Operations categories (MRP, inventory, field service, construction, clinic, POS, property, farm) | 50 | 20 |
| C | Front office (accounting, payroll, CRM, e-commerce, booking, practice management) | 29 | 15 |
| D | IT, security, AI, collaboration; plus scoring-logic stress test with simulated businesses | 13 data + 17 logic | 7 |

Triage rule: a correction was applied only where the reviewer gave a source and confidence was high or medium. Claims that could not be confirmed either way were left in place and flagged as unconfirmed on the product profile.

## Results

- **115 data corrections applied**, each logged with old value, new value, reason and source in `redteam_v7_log.json`.
- **13 capability scores flagged unconfirmed** across 8 products.
- **17 scoring-logic issues fixed** in `assets/js/assess.js`.

Corrections by reviewer: A ERP/WMS: 20, B Operations: 38, C Front office: 30, D IT/AI: 24, D logic: 3

## Most material data corrections

- Google Workspace and Dropbox: Canadian data-residency claims removed (no Canadian region for these plans).
- Wagepoint: Quebec payroll and timesheets now supported.
- Square for Restaurants: not compatible with Quebec WEB-SRM mandatory billing; flagged for Quebec restaurants.
- inFlow: headquarters corrected to Toronto. Craftybase: renamed Stocksmith.
- Odoo: no official Canadian payroll localization (score lowered); first-year price band raised.
- Catch weight in Business Central and SAP Business One: native → add-on.
- Problem library: union payroll now points to payroll plus construction systems; practitioner splits to clinic plus payroll; "systems don't talk" to reporting.

## Scoring-logic fixes (L1–L17)

| # | Issue found | Fix |
|---|---|---|
| L1 | ERP could be offered as a "quick win" | ERP and owned systems never qualify; if nothing qualifies, show "Start with an ERP readiness review" |
| L2 | Quick win ignored time-to-value and budget | Prefer go-live-in-weeks projects (≥40% of top score); otherwise label "First project"; exclude options above budget |
| L3 | Small-business rule too broad | Small = under 10 staff, or 10–49 staff with budget under $100K |
| L4 | Problems could route to categories with no products | Fallback chain per category; unmatched problems are listed openly |
| L5 | Small service and logistics firms sent to PSA / WMS | Small service → accounting-led; small logistics → TMS |
| L6–L7 | Professional, service and contractor firms got wrong workflow/products | New follow-up questions (legal, accounting, other professional; salon, auto, home service; construction vs field service); niche products shown only to the matching type; coverage gaps stated (auto repair) |
| L8 | Owned tools re-recommended | Owned categories down-weighted and labelled "You have this: optimise it"; Microsoft 365 and Google Workspace split |
| L9 | Fit ignored which problem was picked | Capability weights per problem |
| L10 | Display cap at 95% hid ranking differences | Rank on raw score; tie-break Canadian, then price |
| L11 | Size bands mismatched to staff counts | 10–49 staff see small and mid products; 50–199 see mid |
| L12 | Filler priority cards | Only categories with a real score and a stated reason |
| L14 | AI/collaboration ignored current office suite | Copilot preferred for Microsoft 365, Gemini for Google Workspace |
| L15 | Priorities did not lift problem-driven categories | Small priority term added |
| L16 | Method text promised "cheapest" | Wording changed to time-to-value within budget |
| L17 | Warehouse problems sent small firms to full WMS | WMS only for 50+ staff with budget ≥ $25K; otherwise inventory |

L13 (cosmetic) was merged into L12.

## Unconfirmed scores (left in place, flagged on profile)

- **OSCAR Pro (WELL Health)**: Canadian data hosting; Telehealth
- **Epicor Kinetic**: Field service businesses: Technician pay and commissions; Field service businesses: Field invoicing and payments
- **Acumatica**: Omnichannel brands (online plus wholesale): 3PL connections
- **Oracle NetSuite**: Omnichannel brands (online plus wholesale): 3PL connections; Logistics and 3PL: Multi-client inventory
- **SYSPRO**: Food distribution: Temperature zones
- **Sage X3**: Food distribution: Temperature zones
- **Odoo**: Omnichannel brands (online plus wholesale): 3PL connections; Repetitive and make-to-stock: Line and rate scheduling
- **Sage Intacct (Construction and Projects)**: Multi-site clinics and health services: Practitioner compensation; Multi-location hospitality: Franchise and royalties

## Test evidence

- 12 reviewer personas re-run after the fixes (3PL, trucking, job shop, clinic, firms, salon, auto repair, HVAC, food distributor): all now land on a sensible first step; none receives ERP as a quick win.
- 75 assessment runs across every industry, subtype and three size/budget profiles: every run produced priority cards and a first step; no script errors.
- Software Finder: every category × industry combination shows either products or a clear empty-state message.

## Remaining limits

- Capability scores are desk research, not hands-on testing. Unconfirmed scores should be checked in vendor demos.
- Auto-repair shop management software is not yet in the database.
- Prices are first-year bands and change often; re-check before client use.
