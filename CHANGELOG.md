# Changelog

## V4.13 — 2026-11-09
- **Repeated pictures in Insights articles: full review.** All 122 articles were checked. Each cover was compared with every image in the article body, and each body image with the others. The check uses visual similarity, so it also catches the same picture saved as a different file or crop, which the V3.3 exact-file check missed.
  - **How to Reduce Costs with Proven Process Improvement Strategies:** removed the "Cost Reduction Strategy" image under the cover. It was a second copy of the cover picture.
  - **Change Management Toolkit: The Top 10 Models…:** removed 9 repeats of the same gear icon. The first one stays.
  - No other article repeats a picture. The 20 closest remaining cover/body pairs were checked by eye and are different pictures.
- New post-build step `gen/dedupe_images.py` removes these repeats automatically on every build. It is safe to run twice.

## V4.12 — 2026-11-09
- **Chmltech Online Journal:** all four journal articles were rewritten as full research papers, keeping their original URLs.

| Vol./Issue | Title | Words | Equations | Tables | References |
|---|---|---|---|---|---|
| 103(1) | FrugalGPT and MultiModal-GPT: Advancements in Language Modeling | 3,800 | 8 | 2 | 24 |
| 103(2) | Advancements in Machine Learning and Deep Learning for Intelligent Systems | 3,250 | 7 | 2 | 30 |
| 102(1) | Process Intensification and Efficiency Enhancement in Hydrogen Electrolysis Plants: A Deeper Look | 3,500 | 17 | 2 | 18 |
| 101(1) | Advancements and Challenges in Solid-State Hydrogen Absorption: A Comprehensive Review | 3,950 | 13 | 2 | 27 |

- **New journal layout:**
  - Masthead (journal, volume, issue, "Research article"), the paper title, and an author and affiliation block.
  - Published and revised dates.
  - Abstract box and keywords.
  - Numbered sections and subsections, numbered equations, captioned tables and callouts.
  - Clickable citations that jump to a numbered reference list with DOI or arXiv links.
  - "How to cite this article", a contents sidebar, and a "Print or save as PDF" button with a clean print layout.
  - Scholarly metadata (citation_* meta tags and ScholarlyArticle structured data).
  - A "More from the journal" section.
- **References:** every reference is a real, verified source. A spot check of 12 DOIs through Crossref and 8 arXiv IDs found no mismatches.
- **Technical corrections to the originals** (each paper notes that it is a revised edition):
  - Wrong reactions for LiAlH4, ammonia borane and graphene.
  - The magnesium hydride capacity (7.6 wt%, not 1.2 wt%).
  - The van 't Hoff interpretation.
  - Unsupported nanostructure and graphene figures.
  - Mixed-up alkaline and PEM electrode reactions.
  - The definition of "energy intensification" and the title that used it.
  - The claim that pressurized electrolysis raises production rate.
  - Waste heat recovered "for power".
  - How FrugalGPT and MultiModal-GPT actually work.
  - AlphaGo's training.
  - Random forest interpretability.
  - Overstated "human-level" claims.
- **Insights cards:** the journal cards show the real paper title plus the volume and issue in place of the "Chmltech Online Journal, Volume…" title.
- **Duplicate title covers removed:** the 13 articles whose cover image only repeated the title (including the journal articles) no longer show that image under the page heading. It is still used for social sharing and on the cards.
- **Source files:** paper content is in `content/journal/*.json`, with the format described in `content/journal/SPEC.md`.

## V4.11 — 2026-11-09
- **Email address protection.** The address no longer appears in the page source on any page, so bots that harvest addresses for spam and phishing lists can't scrape it. It used to appear 683 times across 189 pages.
  - Visitors still see and click the real address: the site script rebuilds it in the browser.
  - Without JavaScript, the link reads "info [at] chmltech [dot] com" and opens the contact form.
  - The form email fallback builds the address in code.
  - The Contact page's search description no longer includes the address.
  - The address is spelled out in the README and changelog as well, because the repository is public.

## V4.10 — 2026-11-09
- Rebuilt the Lean Six Sigma Training page (`lean-six-sigma-training.html`) with new writing and design, in the same style as the other rebuilt solution pages.
- **Animated header:** the DMAIC phases light up in turn. During Improve, the process curve narrows inside its spec limits and the out-of-spec defects disappear; Control holds the gain.
- **Two interactive diagrams:**
  - A DMAIC cycle: click each phase to see what participants do and which tools they use.
  - A Lean vs. Six Sigma comparison.
- **New sections:**
  - Overview, and "Signs your team is ready"
  - What the training includes: needs assessment, in-house belt training, live projects, coaching, KPIs, sustaining the gains
  - The toolkit
  - Training levels: White, Yellow, Green and Black Belt; Leadership and Champions; and a link to the free practice exams
  - Typical training projects (illustrative before and after), outcomes, method, and learning by doing
  - Why Chmltech, FAQs, related free courses and related Six Sigma articles
- **Corrections to the old copy:**
  - Removed four references to "Propel", another firm's name left over in the original text.
  - Removed wording written for professional services firms, and the "manufacturing capacity" line.
  - "3:1 return. Guaranteed." now uses the agreed ROI wording, with the results note.
- Solution page section headings can now be set per page (toolkit, training levels, examples, outcomes, method).

## V4.9.4 — 2026-11-09
- Natural Resources header animation: the haul truck now stops under the stockpile bin and takes the whole load before it leaves.
  - Ore falls from the chute into the truck, the bin empties, and the load heaps up in the truck bed in three stages.
  - Once loading is done, the truck drives off forward. The bin refills from the conveyor while the truck is away (12-second loop).
- The "Stockpile" label moved above the bin so the falling ore doesn't cover it.

## V4.9.3 — 2026-11-09
- Cycle diagrams: the green arc is now synchronized with the highlighted (dark blue) stage. It used to spin on its own timer.
  - The arc always spans from the previous stage to the active one.
  - When the cycle advances, the arc slides forward to the next stage, and that stage highlights as the arc arrives.
  - Clicking a stage moves the arc to it and stops the auto-advance.
- This applies to every cycle diagram on the site: AI, Business Process Optimization, Manufacturing, Professional Services and the cycle diagrams in all 12 free courses.

## V4.9.2 — 2026-11-09
- Consumer Goods header animation: the delivery truck now waits at the end of the conveyor while all three parcels are loaded. Each parcel drops into the truck and lights up a parcel icon on its side. When loading is complete, the truck drives off forward and a new truck pulls up for the next cycle (10-second loop).

## V4.9.1 — 2026-11-09
- Natural Resources header animation: the haul truck now drives forward, cab first, from left to right. It used to move backwards.

## V4.9 — 2026-11-09
- Every industry page now has an interactive swim lane process with a fixable bottleneck. It is the first diagram on each page, shown full width.

| Industry | Process | Bottleneck | Rework loop | Fix |
|---|---|---|---|---|
| Energy & Chemicals | Corrective maintenance, request to return to service | Plan and scope job | Clarify the request (incomplete notification) | Notification checklist, standard job plans, priority rules, weekly schedule |
| Natural Resources | Haul truck repair, breakdown to production | Find and issue parts | Expedite missing part (stock-out) | Critical spares with min/max, parts kitting, planned change-outs |
| Manufacturing | A customer order through the plant | Change over the line | First-piece approval (first piece fails) | SMED, standard settings, changeover checklist |
| Health Care | Inpatient discharge, ready to next admission | Write discharge order | Page for the order | Expected discharge date at admission, morning huddle |
| Professional Services | From proposal to paid invoice | Partner review | Rework and resubmit | Review criteria at kickoff, check-ins, delegated sign-off |
| Consumer Goods | A retailer order, from PO to invoice | Confirm available stock | Rush production run | Shared demand plan, SKU rationalization, safety stock |
| Distribution & Warehousing | Order flow through the DC (V4.8) | Pick | Replenish pick face | Velocity slotting, batch picking, min/max replenishment |
| Public Sector | A permit application, start to finish | Department reviews | Request missing info | Completeness checklist, parallel reviews, status visibility |

- The swim lanes replace the single-row process flows on Energy & Chemicals, Health Care, Professional Services and Public Sector. Natural Resources, Manufacturing and Consumer Goods keep their two existing diagrams, shown side by side below the swim lane.
- Status chips use descriptive labels, not numbers.
- Swim lane content is generated by `indgen/swimlanes.py` (not shipped). A layout check stops any connector from running through another step, and the bottleneck's rework step must sit directly above or below it.

## V4.8 — 2026-11-09
- Distribution & Warehousing: the order-flow diagram is now an interactive **swim lane process**.
  - Five lanes show who does each step: Customer, Customer service, Inventory control (WMS), Warehouse floor, and Suppliers and carriers.
  - The 12 steps run from inbound delivery and putaway, through order entry, stock allocation, picking, packing and shipping, to delivery.
- **Before:** orders queue at Pick, which is marked as the bottleneck. A dashed orange "short pick" rework loop runs up to "Replenish pick face" in inventory control and back. Order dots slow down after picking.
- **Fix the bottleneck:** Pick turns green and is marked Fixed, the queue and the rework loop disappear, and the replenish step shows as "Stocked ahead". Orders flow at full speed through packing and shipping. The status chips and the note panel explain the fix: velocity slotting, batch picking by zone, and min/max replenishment. "Show the original process" switches back.
- Click any step to see what happens there.
- On narrow screens, the diagram becomes an ordered list with a lane tag on each step, and the rework loop is indented under Pick.
- Motion is off for visitors who choose reduced motion.
- New reusable `swimlane` diagram type in `assets/js/figures.js`, configured from page data (`content/industries/*.json`), so other pages can use it later.

## V4.7.2 — 2026-11-09
- Fixed doubled labels in the "Typical scenarios" cards on all 8 industry pages. Cards showed "Before: Before: …" and "After: After: …"; each label now appears once. The page builder now strips a repeated label automatically.

## V4.7.1 — 2026-11-09
- Fixed process-flow diagrams where step names touched the box edges (for example "Department reviews" and "Notification" on Public Sector). This affected 6 pages: Public Sector, Energy & Chemicals, Health Care, Professional Services, Distribution & Warehousing and Business Process Optimization.
- On those pages, the flow diagram now gets the full width of the section, with the second diagram below it, instead of sharing a half-width column. Flow boxes have a little more inner room, and long words wrap cleanly.
- Checked every flow step on desktop (1366, 1100 and 900 px) and phone (390 px): all text stays at least 4 px inside its box.

## V4.7 — 2026-11-09
- Redesigned all 8 industry pages with new writing built on the original Chmltech content: Energy & Chemicals, Natural Resources, Manufacturing, Health Care, Professional Services, Consumer Goods, Distribution & Warehousing, and Public Sector.
- Each page has an animated header scene:
  - **Energy & Chemicals:** a process plant with a column, a reactor, flowing pipes and a flare.
  - **Natural Resources:** a mine site with a headframe, an ore conveyor and a haul truck.
  - **Manufacturing:** a production line with a robotic arm, gears and an OEE gauge.
  - **Health Care:** patient flow from check-in to discharge, with a heartbeat line.
  - **Professional Services:** work moving from intake to delivery to billing, with utilization and realization bars.
  - **Consumer Goods:** an order moving through pick, pack and ship to a delivery van.
  - **Distribution & Warehousing:** warehouse racks with a moving forklift and a dock.
  - **Public Sector:** service requests moving from request to review to resolved.
- Each page also has two interactive diagrams (for example, a plant work-order flow with a fixable bottleneck, an OEE loss chart, and a PDCA cycle).
- New sections on each page: overview, signs it's time to act, industry challenges, services, before/after scenarios, outcomes, why Chmltech, FAQs, related free courses, related articles and links to the other industries.
- Claims refined:
  - "3:1 return. Guaranteed." becomes "We aim for a return of at least 3:1 … we agree an ROI target with you", with the results note. This applies to Energy & Chemicals, Natural Resources, Health Care, Professional Services and Public Sector. The one-year timeframe on Natural Resources is removed.
  - Manufacturing's "40% average increase in productivity" becomes measurable productivity gains tracked against your baseline KPIs.
  - "Best in class", "top notch", "proven results", "powerful methodology" and claims about past clients are removed or reworded.
  - Example figures are labelled as examples.

## V4.6 — 2026-11-09
- Fixed headings that showed "&amp;" instead of "&": Energy & Chemicals, and Distribution & Warehousing. The Wix heading text is now decoded before it is re-encoded, and the site was checked for any other double-escaped text.

## V4.5 — 2026-11-09
- Process Improvement page has a new "Why Chmltech" section with refined claims:
  - "Canada's leading Operations Improvement Firm" becomes "A Canadian operations improvement firm".
  - "3:1 ROI, guaranteed" becomes "Built to pay for itself: we aim for a return of at least 3:1". An ROI target is agreed per engagement and tracked on KPIs, with a results disclaimer.

## V4.4 — 2026-11-09
- Rebuilt three solution pages with stronger writeups, each built on the original Chmltech content: Artificial Intelligence, Business Process Optimization and Process Improvement.
- Animated header illustrations:
  - **AI:** a neural network feeding a chat assistant.
  - **BPO:** a tangled process path straightening into a clean flow, with Identify → Analyze → Implement → Monitor.
  - **Process Improvement:** a continuous-improvement staircase with a rising KPI gauge.
- Two interactive diagrams per page:
  - **AI:** idea-to-value cycle and AI foundations stack.
  - **BPO:** 4-step method cycle and a purchase-order approval flow with a fixable bottleneck.
  - **Process Improvement:** Lean program timeline and a report-and-leave vs. embedded-team comparison.
- New sections: overview, signs you need this, services and deliverables, AI use cases and ways to start, before/after real examples, outcomes, Lean and people approach, FAQs, related free courses and related articles.
- New `assets/js/svc.js` renders the diagrams on solution pages.

## V4.3 — 2026-11-09
- Three more free interactive courses:
  - **AI Awareness for Everyone:** 21 lessons, entry level for all staff. Labs: "Fact, myth or it depends?", "Is it safe to share?", AI awareness check.
  - **Digital Automation for SMEs: Building Your Digital Automation Plan:** 23 lessons. Labs: maturity by function, opportunity matrix, business-case calculator. Ends with a written plan.
  - **Multi-Agent Systems for Business:** 22 lessons. Labs: design-fit sort, use-case matrix, token-cost calculator.
- Each has 6 interactive diagrams, an animated header, a 20-question exam and a certificate.
- The site now has 12 free courses, 268 lessons and 36 labs. Courses are listed from entry level (AI Awareness) to advanced, and the Courses and home page descriptions are updated.

## V4.2 — 2026-11-09
- Three new free interactive courses, built the same way as the first six:
  - **AI Agents for Business Operations:** 22 lessons. Labs: agent-fit sort, use-case risk/value matrix, agent readiness assessment.
  - **Building Your AI Operating System:** 24 lessons. Labs: AI OS maturity assessment, prioritization matrix, value calculator.
  - **Large Language Models (LLMs) for Business Leaders:** 21 lessons. Labs: LLM task sort, LLM cost calculator (new), responsible-use readiness assessment.
- Each new course has 6 interactive diagrams, an animated header, a 20-question exam and a certificate. The site now has 9 free courses, 202 lessons and 27 labs.
- New `llm_cost` calculator: requests, tokens and prices give monthly tokens, cost per request and monthly cost. Prices are entered by the learner.
- The AI Operating System solution page links to the new AI OS course. Course lists are ordered with the AI courses first, and each course has its own icon.

## V4.1 — 2026-11-09
- Animated header illustration on each of the six course pages: readiness radar, digital layers, turning gears with a trend line, Gantt chart, automation loop, 5S staircase.
- 37 interactive illustrations inside lessons (6–7 per course), of six types:
  - **Cycle:** auto-advancing stages; click a stage for details.
  - **Process flow:** moving work items, with a queue at the bottleneck and a "Fix the bottleneck" toggle.
  - **Stack:** a layered foundation that builds up; click a layer.
  - **Compare:** a before/after toggle.
  - **Timeline:** a roadmap that reveals phases in sequence.
  - **Bars:** animated comparisons.
- Illustrations are driven by a `figures` list in each course JSON (`content/courses/`) and rendered by `assets/js/figures.js`. A text version is included for search engines and visitors without JavaScript.
- Motion is disabled for visitors who choose reduced motion; flows stack vertically on phones.

## V4.0 — 2026-11-09
- **Six free interactive courses**, rebuilt from scratch: AI Readiness; Digital Transformation & AI Readiness Strategy; Operational Excellence; Project Leadership; Workflow Automation; 5S Mastery. 135 lessons in total (about 48,000 words), keeping each original course's step count.
- Each lesson has key takeaways, an "Apply it at work" exercise and a knowledge check with explanation.
- 18 interactive labs (three per course): self-assessments with radar charts and tailored next steps, 2x2 prioritization and stakeholder matrices, sorting exercises with feedback, and calculators (automation ROI, OEE, earned value, cost of searching).
- 20-question final exam per course (70% pass, unlimited retakes, explanations for wrong answers), unlocking a printable Chmltech certificate of completion.
- Course player: outline sidebar, progress saved in the browser, resume where you left off, mobile-friendly. Course URLs are unchanged (`challenge-page/<id>`).
- Course content is kept as JSON in `content/courses/` for future edits.
- Money values in calculators show negatives as -$X.

## V3.8 — 2026-11-09
- Forms switched from FormSubmit to Web3Forms (fixed access key, no per-page activation). Contact, Book Online and the Insights subscription all deliver through one key.
- Submissions are sent as a simple FormData request (no CORS preflight); the honeypot field is renamed to `botcheck`.

## V3.7 — 2026-11-09
- Forms: always send the page origin (`referrerPolicy` plus a `<meta name="referrer">` tag on every page). FormSubmit rejects submissions without it, which caused "could not be sent" in some browsers.
- Clearer message when a browser's privacy settings block sending, or when a page is opened from a local file.

## V3.6 — 2026-11-09
- Fixed the Insights category filters, search and "Show more", and the same controls on the Training exam library. Filtered-out cards were marked hidden but stayed visible because the card styles overrode the browser's hiding; a global `[hidden]{display:none}` rule fixes it.

## V3.5 — 2026-11-08
- Forms now deliver by email: Contact, Book Online and the Insights subscription post to FormSubmit, which emails info [at] chmltech [dot] com. They no longer depend on the visitor's email app.
- Submission emails use a table layout and a clear subject, with Reply-To set to the visitor's email. The spam honeypot field is renamed to `_honey`.
- Clear on-page messages for sent, not-yet-activated and failed cases; the email draft is offered only when online sending fails.

## V3.4 — 2026-11-08
- New solution: **AI Operating System** (`ai-operating-system.html`). Covers what an AI OS is, the six building blocks, the five-phase build approach, benefits, FAQs and related reading.
- Animated SVG illustration: systems and data flow into the AI OS core, which delivers assistants, automations, KPIs and decisions under a governance layer. Motion is disabled for visitors who choose reduced motion.
- New featured AI OS section on the Solutions page; AI OS added to the solutions grid, the home page solution list, the solution sidebars and the contact form topics.

## V3.3 — 2026-11-08
- Removed duplicate images in 21 articles where the cover photo was repeated inside the article body. No picture now appears twice in an article.

## V3.2 — 2026-11-08
- The 13 Insights articles without a usable photo each get a unique branded cover (logo-ring, dot-grid or circuit pattern, with category and title) in place of the shared placeholder icon. Files are in `assets/media/covers/`.
- Every article now has its own social-sharing image (`og:image`, large Twitter card) instead of the generic logo.

## V3.1 — 2026-11-08
- Primary address is now www.chmltech.com (DNS at IONOS points to GitHub Pages). Added a `CNAME` file.
- Canonical URLs, Open Graph tags, sitemap.xml and robots.txt updated to www.chmltech.com.
- chmltech-consulting.com becomes a forwarding domain (path-preserving redirect to www.chmltech.com).

## V3 — 2026-11-08
- Full migration off Wix: all site content now lives in this repository. Nothing loads from Wix.
- Insights: every published article migrated to `post/<slug>.html`, with images, publish dates, authors, tags, related articles and BlogPosting structured data. The Insights page has search, category filters and "show more".
- Original Wix web addresses preserved. GitHub Pages serves `post/x.html` at `/post/x`, so old links and search results keep working. Retired addresses (`/challenges`, `/book-online`, `/plans-pricing`, `/insights/categories/*`, `/service-page/*`) redirect to their new pages.
- Industries (8) and Solutions (11, including EOS) now have their own pages, using the original Wix page text in place of the V2 placeholder copy.
- Training: the full free practice-exam library (146 exams, 10 categories) with search and filters. Wix-hosted mock exams and tools are self-hosted under `exams/`.
- Courses: the 6 free online programs (`challenge-page/<id>`) and 3 paid one-hour sessions (Corporate Strategy CA$450, Operational Consulting CA$350, Project Management CA$250).
- Book Online lists the paid sessions. Home shows the latest articles plus the free exam and course counts.
- New Projects page. Wix free-library stock images (licensed for Wix sites only) removed.

## V2 — 2026-11-08
- Full multi-page site: Home, Industries, Solutions, Training, Insights, Courses, Book Online, Contact and 404.
- Shared stylesheet with brand tokens (logo navy, blue and green) and a shared script.
- Responsive header with a mobile menu, a sticky top bar and the current page highlighted.
- Contact, booking and newsletter forms ready for Formspree, with an email fallback and a spam honeypot.
- Topic filter on the Insights page.
- Detail sections for all 8 industries and all 10 solutions, linked from the Home page.
- SEO basics: unique titles and descriptions, canonical URLs, Open Graph tags, sitemap.xml and robots.txt.
- Accessibility: skip link, visible focus states, labelled form fields and accessible colour contrast.

## V1 — 2026-11-08
- Single landing page (Chmltech_Landing_Page_V1.html) with the logo and brand palette.
