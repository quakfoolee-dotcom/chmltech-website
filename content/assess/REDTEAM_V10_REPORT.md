# Red-Team Validation Report — Vendor Directory and AI Tools (Draft V10)

Review date: November 20, 2026 · Scope: 781 directory listings and 475 AI tools added in Draft V9, plus the directory and AI-suggestion logic

## Method

Five independent reviewers, none of whom built the data. Every listing was desk-checked; web verification went first to listings shown in user results (217), then to anything flagged, then to samples. Reviewers A and C also loaded every website in their slices to check status, redirects and address.

| Reviewer | Scope | Findings | Applied | Not applied (desk-only or low confidence) | Confirmed correct |
|---|---|---|---|---|---|
| A | Directory: software in assessment categories (295) | 83 | 80 | 3 | 48 |
| B | Directory: WMS and specialist software (286) | 72 | 42 | 30 | 32 |
| C | Directory: service partners (200) | 102 | 83 | 18 | 111 |
| D | AI tools, categories 1–13 (262) | 77 | 61 | 16 | 26 |
| E | AI tools, categories 14–26 (213) + logic and security review | 66 | 57 | 9 | 29 |

Rule: applied only when confidence is high or medium and the evidence is a URL. Every applied change is logged with reviewer, before/after, reason and source in `redteam_v10_log.json`.

## Results

- **323 corrections applied** (removed: 72, website: 59, pricing: 43, status: 39, group: 38, desc: 22, hq: 20, note: 14, canadian: 10, category: 4, price: 2).
- **51 directory listings and 21 AI tools removed**: closed, non-existent, consumer or deep-tech companies outside the SME scope, and duplicates.
- **302 directory listings and 139 AI tools marked ✓** (confirmed or corrected with a source).
- Directory now 730 listings (525 Canadian); AI tools now 454.

## Most material findings

- Global WMS list contained padded or non-existent entries (Fishtech/TempoWMS, WHSControl, Hopscotch, Wharehouser, Grocy, TechniCare ERP) — removed.
- Körber and HighJump entries are all Infios now (March 2025 rebrand) — duplicates removed; 3PL Central and Skubana are Extensiv; DEAR is Cin7 Core; Stitch Labs shut down.
- Dayforce is headquartered in Minneapolis (not Canadian); Versapay moved its HQ to Miami; several HQ cities corrected.
- Many Canadian IT partners have been acquired or renamed (CloudKettle → Ateko/Bell, Logient → Wepoint, Softlanding and Groupe Access → MSP Corp, Difenda → Quorum Cyber, Softchoice → WWT); each listing now carries an "Update" note.
- AI tools shut down or folded: Google Project Mariner, Tome, Height, Clockwise, Limitless/Rewind, Adept, Botkeeper, Phind, AgentGPT, Flowrite, Drift; renames such as Operator → ChatGPT agent, Phrasee → Jacquard, CodeWhisperer → Amazon Q Developer, Windsurf → Devin Desktop.
- Stale AI pricing corrected on most tools shown in results (e.g., Fyxer, Shortwave, Jasper, Instantly, Klaviyo, Power BI).

## Logic and security fixes

| Issue (reviewer) | Fix |
|---|---|
| "More vendors" filled slots with unsized listings and called them "sized for your business" (E-L1, E-L11) | Size-confirmed listings first; unsized only to fill, labelled "size not stated"; small firms never see unsized Custom/Enterprise-priced listings; label conditional |
| Fallback to another category was silent (E-L6) | Lead-in "For your priority: …" |
| AI category in "More vendors" showed developer platforms | AI category skipped; AI needs are covered by AI tool suggestions |
| "See all N" count did not match the directory (E-L4) | Button no longer quotes a number; the directory opens with the business size applied |
| Directory showed blank size for unknown (E-L5) | "Not stated"; confirmed-size listings sort first when a size is chosen |
| AI suggestions took the first 3 listed tools, including enterprise-only ones, under a "low-cost" heading (E-L7) | Only tools with a free tier or published price ≤ $60/mo, free first; enterprise/custom/waitlist tools never suggested |
| AI categories: one problem could take all slots; only first problem shown (E-L8) | One category per problem first; every matching problem listed |
| Problem map (D logic) | p6 marketing only; p9 meeting notes + writing; no-show reminders → automation; p27 adds sales; p44 adds presentation; clinical charting (p48), backup (p11) and AI rules (p15) no longer suggest generic AI tools |
| Links could carry javascript: URLs (E-L9) | safeUrl() on every data-driven link; JSON embed escapes </ and U+2028/2029; one unescaped link escaped |

## Not applied (needs manual review)

76 findings were desk-only or low confidence, mainly suspected category moves and duplicates in the WMS list. They are listed in the findings files under `redteam_v10/` for a manual pass.

## Remaining limits

- Directory listings and AI tools are listed, not scored; not every listing was individually web-verified (the ✓ shows which were).
- About a third of directory listings have no size in the source lists.
- AI tool pricing changes monthly; re-check before client use.

## Removed listings

- Fusebill (dir): Fusebill was acquired by Stax (2021) and renamed Stax Bill; fusebill.com now redirects to staxbill.com. Same product as 
- Wave Financial (dir): Same company and same website (waveapps.com) as idx 196 Wave; it is also wrongly flagged canadian=false (Wave is Toronto
- Lightspeed Retail (dir): Lightspeed Retail is a product of Lightspeed Commerce (idx 23); same website lightspeedhq.com.
- Infor LN / M3 (dir): Same product (Infor LN) and same URL as idx 573 (Baan / Infor LN). If you keep a separate M3 row, point it to https://ww
- Spectrum Construction ERP (dir): Trimble acquired Viewpoint, and "Spectrum Construction ERP" is the same Trimble Viewpoint Spectrum product as idx 657. T
- Uberflip (dir): Uberflip is now "A PathFactory Company" (per the uberflip.com page title). Its capabilities are already folded into the 
- Salesfloor (dir): Tulip and Salesfloor merged (March 2026); salesfloor.net now redirects to tulip.com. Same product as idx 287 Tulip.
- Convictional (dir): Convictional announced it is shutting down (essay by the CEO, Aug 3, 2026). Its B2B dropship product is no longer offere
- CoConstruct (dir): Buildertrend (which acquired CoConstruct in 2021) is retiring CoConstruct and migrating its users to Buildertrend (alrea
- Fonolo (dir): Fonolo is now part of Verint (US); fonolo.com redirects to verint.com/callback-support ("Fonolo is now part of Verint").
- Plum (dir): Plum was acquired by Phenom (US); plum.io redirects to Phenom's "Phenom Acquires Plum" page. It is no longer a standalon
- Constellation Software (dir): Constellation Software is a holding company that acquires vertical-software firms, not an ERP product an SME can buy. It
- Maves International Software (dir): Maves International Software and ViewPoint Logistics are the same vendor/product (same Markham address, VPL site uses bo
- 3PL Central (Extensiv legacy) (dir): 3PL Central rebranded as Extensiv; row duplicates Extensiv 3PL Warehouse Manager (same URL).
- Skubana (Extensiv OMS) (dir): Skubana became Extensiv Order Manager; same URL as idx 765.
- Tecsys WMS (dir): Tecsys WMS is the same product as Tecsys Elite WMS (idx 0); also flagged non-Canadian although Tecsys is Montreal-based 
- Körber WMS (dir): Körber Supply Chain Software rebranded as Infios on 4 Mar 2025; row duplicates idx 678 Infios WMS Suite.
- Highjump (Körber Edge) (dir): HighJump -> Körber -> Infios (rebrand Mar 2025); duplicates Infios WMS Suite. Name "Körber Edge" is dated.
- HighJump (Körber) Cold WMS (dir): HighJump/Körber cold-chain variant is not a separate product; Körber supply chain software is now Infios.
- Körber WMS Cold Chain Edition (dir): "Körber WMS Cold Chain Edition" is a vertical page, not a distinct product; brand is now Infios.
- Synergy Logistics 3PL WMS (dir): Synergy Logistics is the maker of SnapFulfil; snapfulfil.com now redirects to synergylogistics.ai which sells "SnapFulfi
- Stitch Labs / Linnworks Cloud (dir): Stitch Labs was acquired by Square (2020), stopped taking new customers and was sunset (existing customers until Spring 
- Ware2Go WMS (dir): Stord acquired Ware2Go from UPS (May 2025); "UPS-backed" description outdated.
- Fishtech / TempoWMS (dir): fishtech.com is a parked domain (JS redirect to /lander); Fishtech is a cybersecurity brand; no "TempoWMS" product could
- TempoWMS Cold Chain (dir): No evidence a "TempoWMS" product exists (web search returns nothing; tempowms.com unreachable). Pairs with fabricated id
- WHSControl WMS (dir): whscontrol.com redirects to whscontrol.com.au, an Australian work-health-and-safety clearance tool ("know who's clear to
- TechniCare ERP (dir): technicarecorp.com is a surgical-instrument manufacturer (Techni Care), not an ERP for long-term care. Listing appears f
- Hopscotch WMS (dir): No product "Hopscotch WMS" found; searches only return Hopstack WMS (hopstack.io). hopscotchwms.com unreachable. Likely 
- Wharehouser WMS (dir): No evidence "Wharehouser WMS"/warehouser.io exists (search returns nothing; domain unreachable).
- Grocy WMS (dir): Grocy is a self-hosted household grocery/pantry app ("ERP beyond your fridge"), not a business WMS for SMEs.
- nventive (dir): nventive.com redirects to Wepoint; nventive, Logient and Onepoint NA teams combined into Wepoint
- XRM Vision (dir): xrmvision.com redirects to alithya.com; Alithya acquired XRM Vision
- Nubik (dir): No longer an independent SME-reachable partner; site down
- Converge Technology Solutions (dir): Converge Technology Solutions was taken private by H.I.G. and merged into Pellera (April 2025)
- Myplanet (dir): myplanet.com redirects to orium.com; Myplanet renamed to Orium; also wrong group (msp)
- Dynamix Solutions (dir): dynamixsolutions.com redirects to f12.net (F12 Canada); Dynamix appears absorbed by F12
- FCV (dir): fcv.ca is a parked domain for sale on Spaceship.com
- Digital Echidna (dir): Northern Commerce acquired Digital Echidna (2020); digitalechidna.com now serves a parked /lander redirect
- Pragmatica (dir): listing points to an unrelated speech-therapy VR product
- Hopper (dir): Hopper is a consumer travel-booking app, not an SME vendor or AI service partner
- Private AI (dir): private-ai.com redirects to getlimina.ai
- CentML (dir): CentML acquired by Nvidia; centml.ai unreachable
- Tenstorrent (dir): AI accelerator chip maker; not an SME vendor or service partner
- Moonvalley (dir): Generative cinematic video models for filmmakers; not an SME vendor/partner
- Spellbook (dir): Same company listed twice; spellbook.legal redirects to spellbook.com
- Ada (dir): Ada is a customer-service AI product, already listed as a product
- Waabi (dir): Waabi builds autonomous trucks/robotaxis; not an SME vendor or service partner
- Xanadu (dir): Xanadu is a photonic quantum-computing company; not an SME vendor
- Deep Genomics (dir): Deep Genomics is a drug-discovery biotech, not an SME vendor
- ProteinQure (dir): ProteinQure is a peptide-therapeutics biotech, not an SME vendor
- NorthStar Earth & Space (dir): NorthStar is a space-situational-awareness satellite company (SPAC listing 2026); not an SME vendor
- Google Project Mariner (ai): Google shut down Project Mariner on May 4, 2026; tech moved into Gemini Agent and Chrome auto-browse. It was also US-onl
- Cognosys / Ottogrid (ai): ottogrid.ai now redirects to a GoDaddy domain-for-sale page; product appears defunct.
- AgentGPT (ai): Reworkd archived the AgentGPT repo on Jan 28, 2026 (no fixes or security patches since v1.0.0, Nov 2023); hosted site on
- Lightfern (ai): Lightfern (lightfern.com) is now a beta desktop workspace for people and AI agents with a waitlist - no longer a Gmail a
- Flowrite (ai): Maestro Labs acquired Flowrite (Jan 2025) and folded it into MailMaestro.
- Tome (ai): Tome sunset its presentation product on April 30, 2025 (pivoted to sales CRM).
- Wepik AI (ai): Wepik became Freepik Designer; the old Wepik doc now redirects to magnific.com design editor (Freepik rebranded as Magni
- Drift (Salesloft) (ai): Salesloft announced a gradual sunset of standalone Drift in March 2026; features moving into Salesloft.
- Phind (ai): phind.com shut down Jan 29, 2026 (community report; site no longer responds).
- Drift (ai): Duplicate and being sunset by Salesloft.
- Botkeeper (ai): Botkeeper shut down in Feb 2026.
- Height AI (ai): Height announced it would shut down in Sept 2025.
- Duolingo Max (ai): The same product and URL appear twice. It is a learning app, not translation.
- Synthesia Language (ai): This is the third Synthesia row (idx 110, 357, 361), all with the same URL.
- Socratic (Google) (ai): Socratic is discontinued and was merged into Google Lens. socratic.org redirects to search.google/ways-to-search/lens (c
- Limitless AI (ai): Meta's purchase of Limitless ended sales to new customers.
- Rewind AI (Limitless) (ai): Rewind was already folded into Limitless, and Meta's purchase ended it.
- Clockwise AI (ai): getclockwise.com now shows only a 'Clockwise's Next Chapter' shutdown page.
- Adept AI (ai): Adept sells no product today.
- Phind (ai): Phind closed abruptly and deleted user data on 30 Jan 2026.
- Mentat (ai): The AbanteAI/mentat repo is marked ARCHIVED.
