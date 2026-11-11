# Changelog

## V4.38 — 2026-11-11
- **Projects page: track record revised** against the full list of past projects (372 project folders, 343 completed).
  - The key figures are now 313 completed plans, 340+ completed projects in total, 15 sectors and 6 provinces. The "2022–2025 delivery period" figure was removed.
  - **Plans by sector:** Food & Beverage Manufacturing (8 plans) is now counted under Manufacturing, which rises from 27 to 35. "Other" is now 5 sectors and 37 plans.
  - **"Plans by year" chart removed.** Most plans were delivered in 2023 and 2024, so the chart read as a decline.
  - **"Plans by province" chart replaced with a list of the six provinces, without counts.** The location is known for fewer than half of the plans, so the counts were not reliable.
  - **New card, "Beyond digital adoption":** 29 more completed advisory projects in sales and marketing, leadership and strategic planning. Leadership and Strategic planning link to their solution pages.
- `content/dap_stats.json` now holds only the figures the page shows. `content/gen/projects_page.py` matches the published page.

## V4.37 — 2026-11-11
- **New page: About (`about.html`).** It introduces Chmltech and its CEO and Principal Consultant, Quak Foo Lee:
  - a portrait, a fact list (title, education, credentials, languages, location) and a short biography;
  - four key figures: founded 2008, 300+ Digital Adoption Plans, 1,000+ days without a safety incident at a pilot plant he managed, five publications and one patent;
  - a career timeline of seven entries from 2000 to today. Past employers are described by sector, not by name; only the University of British Columbia is named;
  - education, certifications, publications and the patent;
  - three areas of work and how we work, then the standard call to action.
- **Portrait:** `assets/img/quak-foo-lee.jpg` (864×1080) and `assets/img/quak-foo-lee-432.jpg` for small screens. The background of the original photo was replaced with a defocused brick wall, the colours were warmed and the shirt was darkened.
- **"About" added to the main menu** (before Contact) on all 218 pages that have the menu, and "About Chmltech" added to the footer. The address is in the sitemap.
- **Menu fit:** with nine links, the "Book Online" button wrapped onto two lines on screens between 981 and about 1060 pixels wide. The button now stays on one line, and the menu spacing is slightly tighter between 981 and 1120 pixels (`assets/css/styles.css`).
- New source file `content/gen/about_page.py` writes the page. It copies the header from `contact.html` and the call to action and footer from `ai-operating-system.html`, so run it again after any change to the menu or footer. `content/gen/build_v3.py` now includes About in the menu, footer and sitemap.

## V4.36 — 2026-11-11
- **OEE articles: the links at the foot of each article now follow reading order.** Links back to earlier articles sit on the left and the link to the next article sits on the right.
  - Article 1: "Next: Post 2" moved from the left to the right.
  - Article 3 (the last): "Back to Post 1" was on the right, where a reader expects "next". Both links back now sit together on the left.
- The articles load `oee.css?v=4.36`, so returning visitors get the new layout without a manual refresh.

## V4.35 — 2026-11-11
- **New Insights series: Overall Equipment Effectiveness (three articles).** Insights now lists 148 articles.
  - `post/what-oee-really-measures`: the three OEE factors, the six big losses and a worked example of one day on a packaging line (OEE 73.4%).
  - `post/what-oee-losses-cost`: the same losses in dollars on a $3.0M line, ranked two ways (share of the total loss, and the gain from fixing one factor alone), and what one OEE point is worth.
  - `post/oee-project-payback`: the business case for a $1M project, with payback (3.6 years), ten-year net present value and cash flow after loan payments, plus a table testing margin and OEE gain.
- **Each article has a slider calculator and a live chart** (hours cascade, revenue waterfall, cumulative cash). They run in the visitor's browser with no libraries. Without JavaScript, the tables still show the worked example and a short note explains what is missing.
- Every mention of another article in the series links to it, and each article links to the next. Filed under Operational Efficiency and Process Improvement.
- The example line, its revenue and the project are illustrative, and each article says so. Extra revenue is counted at a 50% contribution margin, not in full.
- New files: `assets/css/oee.css`, `assets/js/oee.js` and the three source files in `content/articles/`, built with `content/gen/add_article.py`.

## V4.34 — 2026-11-11
- **Inventory articles: short table labels stay on one line.** Labels such as "3. Desirable", "Raw material" and "Reorder when 2 remain" no longer break across two lines. The rule covers every table in the four articles: cells of up to 22 characters, and row labels of up to 30 characters in tables with four columns or fewer.
- The three widest tables (the two ranked item lists and the five-item results table) use slightly smaller type and tighter cells so everything fits the page width without sideways scrolling on a desktop screen. On narrow screens they scroll sideways, as before.
- "Post 1" to "Post 4" links no longer split between the word and the number.
- New file `assets/css/article-tables.css`, linked from the four articles.

## V4.33 — 2026-11-11
- **Inventory articles: quantities stay on one line in tables.** A figure and its unit, such as "180,000 kg", no longer breaks across two lines. The same applies to money, percentages and other numeric cells in the four articles.

## V4.32 — 2026-11-11
- **Fixed: the template download box and form could appear unstyled.** A browser that had visited the site before V4.31 kept its saved copy of `styles.css`, which lacked the new form styles: the box text ran together and the form filled the screen with a full-width close button.
- The styles now live in their own file, `assets/css/download.css`, linked from the four inventory articles, so they load whatever copy of `styles.css` the browser holds. They are removed from `styles.css`.

## V4.31 — 2026-11-11
- **The inventory template now downloads through a short form**, like the journal PDFs. The four inventory articles show a "Free Excel template" box; its button asks for name, work email, company (optional) and an updates checkbox, then starts the download.
  - Leads arrive by email with the subject "Inventory template download — Name".
  - Details are remembered in the visitor's own browser, shared with the journal form, so a returning reader downloads in one click. Nothing is stored in the page, and other visitors see empty fields.
  - If the form service can't be reached, the download still starts. Without JavaScript, the button is a plain download link.
- New file `assets/js/download.js`. The form's styles moved into `assets/css/styles.css` so article pages can use them.
- `robots.txt` now excludes `/assets/downloads/` from search engines, as it does the journal PDFs.
- Privacy notice updated to cover template downloads as well as journal downloads.

## V4.30 — 2026-11-11
- **New Insights series: inventory control (four articles).** Insights now lists 145 articles.
  - `post/abc-inventory-analysis`: ABC analysis explained, with a 20-item distributor example and a Pareto chart.
  - `post/setting-safety-stock`: three safety stock methods, reorder points and service levels by ABC class, using three items from the first article.
  - `post/abc-analysis-for-manufacturers`: adds a criticality rating to ABC for raw materials, packaging and spare parts, with a 20-item manufacturer example.
  - `post/safety-stock-for-manufacturers`: safety stock for raw materials (lead time driven) and for spare parts (Poisson method).
- Every mention of another article in the series links to it, and each article links to the next. Filed under Operational Efficiency and Process Improvement.
- **Free Excel template:** `assets/downloads/Chmltech_Inventory_ABC_SafetyStock_Template.xlsx` (workbook V3), linked from all four articles. It holds both worked examples, an ABC classifier, a safety stock calculator and a spare parts calculator. Its figures match the articles.
- The example companies (Northshore Supply and Ridgeline Coatings) are fictional, and each chart caption says the data is illustrative.
- New source file `content/articles/inventory_articles.py`: it computes every table, chart and figure from the example data and writes the four article JSON files, which `content/gen/add_article.py` then builds.

## V4.29 — 2026-11-11
- **New page: Funding finder (`funding.html`).** A searchable directory of 408 government funding programs for Canadian businesses, covering federal programs and all 13 provinces and territories:
  - grants, repayable contributions, loans, tax credits, wage subsidies, vouchers, equity, rebates and advisory services;
  - filters for jurisdiction (choosing a province also shows the federal programs available there, with a toggle), funding type, who can apply, industry, purpose and status (closed programs hidden unless "Show closed programs" is ticked), plus search and three sort orders;
  - filter choices are saved in the page address, so a filtered view can be shared; on phones the filters open in a panel;
  - every program card links to the official program page and shows when it was last checked.
- **How the data was built:** research agents split by jurisdiction collected each program from its official government or agency page. A separate red team then re-checked every record against the official page: 419 records reviewed, 109 corrected and 11 dropped (no official confirmation that they are current, or businesses cannot apply). The data is in `content/grants.json`, last checked November 11, 2026.
- The page carries a disclaimer: information only, confirm on the official page, Chmltech is not affiliated with any program.
- "Funding" added to the main menu, and "Funding finder" to the footer and sitemap.
- New files: `assets/css/grants.css`, `assets/js/grants.js` (no libraries, works without a server), `content/gen/grants_page.py`.

## V4.28 — 2026-11-11
- **Shorter address for the BDC LIFT article.** It moved from `/post/bdc-lift-program-who-qualifies-and-how-to-prepare` to `/post/bdc-lift-program`. The Insights card, the sitemap, the cover files and the source file in `content/articles/` use the new name.
- The old address redirects to the new one, so links shared earlier still work.

## V4.27 — 2026-11-11
- **New Insights article: BDC's LIFT Program: Who Qualifies and How to Prepare.** It covers the two LIFT paths (digital transformation and AI; productivity and digitally enabled equipment), the minimum requirements for each, the Canadian supplier rule, what each plan must contain, how to apply and how to prepare. It includes a decision diagram and four tables. Filed under Digital Technology and Artificial Intelligence. Insights now lists 141 articles.
- **Facts about LIFT** (revenue thresholds, eligible sectors, loan sizes, terms) come from BDC's three program pages as read on 11 November 2026. The launch date, program size and the 2.25% rate come from BetaKit's launch report; BDC's pages do not publish a rate. The article says so and tells readers to confirm terms with BDC.
- The article carries a note that it is general information, that Chmltech does not speak for BDC, and that BDC decides eligibility and approval.
- New build step `content/gen/add_article.py <slug>`: adds one article from `content/articles/<slug>.json` without a full rebuild. It writes the post page, draws the cover and thumbnail, adds the card to `insights.html`, raises the article counts and updates `sitemap.xml`.

## V4.26 — 2026-11-09
- Projects page: removed the footnote under the track-record charts (data basis and the advisory project count). The province chart keeps its "where the location is known" label.
- Commits are now authored as Quak Foo Lee with the GitHub private noreply address.

## V4.25 — 2026-11-09
- **Track record added to the Projects page**, built from the owner's project register:
  - 313 completed Digital Adoption Plans, 2022–2025, across 16 sectors and 6 provinces;
  - charts of plans by sector (top 10, plus "Other"), by year, and by province (shown only where the location is known, 132 plans);
  - a note on how sector and province were assigned, and a line on the 29 completed operations and strategy advisory projects.
- Only aggregate counts are published (`content/dap_stats.json`). No client names, project IDs or advisor names are published.

## V4.24 — 2026-11-09
- **Projects page rebuilt.** The Wix version only held template placeholders: four project names with "I'm a paragraph" text. The new page has:
  - a hero with three figures: 300+ Digital Adoption Plans for Canadian SMEs, FEED engineering in progress, and plant reviews with HAZOP;
  - two featured engineering projects, with clients named by sector only: a commercial-scale FEED study for an advanced materials producer in BC, and an economics, HAZOP and P&ID review for a biodiesel producer;
  - a Digital Adoption section with an interactive timeline of what a plan covers, and six technology areas;
  - a "from plan to results" section that links to related services.
- **Ready for the 300+ plan data:** adding `data/dap_stats.json` (`{"by_sector": {"Manufacturing": 85, ...}, "note": "..."}`) makes the page show a "Plans by sector" chart.

## V4.23 — 2026-11-09
Fixes from the November 2026 site audit.
- **Trademarked methods removed.** The EOS page is replaced by a new Leadership Operating System page built on general management practice. eos.html now redirects to it. The Scaling Up page is rewritten in our own words as "Scaling Your Business", and the coach claims are gone. The EOS practice exam is removed from the training library, which now lists 145 exams.
- **Seven Wix-era solution pages rewritten:** ISO 9001, Leadership Operating System, Scaling Your Business, Project Portfolio Management, Operational Efficiency, Rapid Lean Assessment and Process Mapping. They now match the layout of the other solution pages and include interactive figures (a timeline, a comparison, a cycle, a stack, a flow and a swim lane).
- **Unsupported claims removed:**
  - "Guaranteed" (ISO 9001)
  - "often in excess of 30% improvement to the bottom line" (Rapid Lean Assessment)
  - "maps within 5 days" (Process Mapping)
  - "proven Strategy Realization Model" and "world-class team on Day One" (Project Portfolio Management)
  - The "3:1" return badge is replaced by "Results agreed up front" on all solution and industry pages.
- **Testimonial removed:** the "Dora Bridges, CEO" quote carried over from the Wix template, which appeared on 15 pages, is gone.
- **Bylines:** 22 posts credited to Sophie Maren, Aaron Blake, Lucas Grant or "ESG Consultant" are now credited to Quak Foo Lee.
- **Location:** journal papers now give Vancouver, BC, matching the rest of the site.
- **Typo:** process mapping now names BPMN correctly (Business Process Model and Notation).
- **HTTPS:** HTTPS is now enforced in GitHub Pages, so all http addresses redirect to https.

## V4.22 — 2026-11-09
- **Fixed:** "How APIs Can Revolutionize Your Marketing and Sales Efforts" no longer appears under Book Review. It had no category from Wix, and the automatic keyword rule for Book Review matched a "by Firstname Lastname" phrase in its description. That rule now looks at the title only. The article stays in Sales & Marketing and Digital Technology. Book Review now lists its 5 real book reviews.

## V4.21 — 2026-11-09
- **New ISO 9001 article: Document and Revision Control Under ISO 9001: Keeping the Right Version in Use.** It covers clause 7.5 requirements, documents compared with records, revision schemes, one master copy, documents from customers and other outside sources, records retention, a minimum setup for small businesses, and what auditors check. It includes a document life cycle diagram and four tables. The ISO category now has 10 articles.
- The "More in this series" list on every ISO article now links to it.

## V4.20 — 2026-11-09
- **Eight new ISO 9001 articles in Insights.** The ISO category grows from 1 to 9 articles. Each has a diagram, tables, sources and links to the rest of the series.
  1. ISO 9001:2026: What Changed from 2015 and What It Means for You
  2. Your ISO 9001:2026 Transition Plan: A Step-by-Step Roadmap
  3. ISO 9001 for Small and Mid-Sized Businesses: Getting Certified Without the Paperwork Burden
  4. Internal Audits That Find Real Problems (also in Process Improvement)
  5. Risk-Based Thinking in Practice: Risks, Opportunities and a Register People Use
  6. ISO 9001 and AI: Using AI Tools Inside a Quality System (also in Artificial Intelligence)
  7. One System, Three Standards: Integrating ISO 9001, ISO 14001 and ISO 45001 (also in ESG)
  8. Management Review That Leadership Finds Useful
- **The 2015 article now opens with an update note** pointing to the 2026 edition and the transition plan. Its original text is unchanged.
- **Facts about ISO 9001:2026** (published 16 September 2026; 2015 certificates valid until 30 September 2029; clause changes) come from summaries by DNV, DQS and SGS, cited in each article. The articles say so and advise readers to check the standard and their certification body.
- New source folder `content/articles/` (article JSON, `iso_articles.py`, `iso_figs.py`) and build step `gen/new_articles.py`.

## V4.19 — 2026-11-09
- **Three new Chmltech Online Journal papers on Physical AI (Volume 105).** Each follows the journal format: abstract, numbered sections, equations, tables, three figures, 30 checked references, and a PDF download.

| Issue | Paper | Figures |
|---|---|---|
| 105(1) | Physical AI: Foundations, Architectures and the Simulation-to-Reality Gap | The control stack and its update rates; growth of error with task length; domain randomization (schematic) |
| 105(2) | Physical AI in Process Plants and Factories: Autonomous Inspection, Manipulation and Control | Where each application sits in the plant hierarchy; detection probability against inspection rounds; readiness by use case |
| 105(3) | Safety, Reliability and Economics of Deploying Physical AI | Safety architecture for a learned component; task success against number of steps; NPV against intervention rate |

- **References:** every DOI was checked against Crossref and every arXiv ID against arXiv. Standards and regulations link to the ISO, IEC and EUR-Lex pages.
- **Worked numbers are the author's calculations** and are labelled as illustrative: the inspection-frequency model in 105(2), and the separation distance and cost model (payback 2.5 years, NPV about 235,000 USD in the base case) in 105(3). The readiness levels in 105(2) are the author's assessment.
- **Categories:** all three are in Chmltech Online Journal and Artificial Intelligence; 105(2) is also in Digital Technology. A paper can now be filed under more than one subject.
- **Ordering:** papers published on the same day now list newest volume and issue first.
- Sources: `content/journal/*.json`, figure scripts `content/journal/figure-scripts/physai.py` and `place_physai.py`.

## V4.18 — 2026-11-09
- **Journal has its own category.** The Chmltech Online Journal filter is now `insights.html#cat=chmltech-online-journal` (10 papers). Wix had stored it under the slug `clean-energy`, which didn't fit the AI papers.
  - Old links keep working: `#cat=clean-energy` and `insights/categories/clean-energy.html` both open the journal filter.
  - The paper breadcrumb and "All journal articles" links point to the new category.
- **Each paper is also filed under its subject**, so readers browsing a topic find it:
  - Artificial Intelligence: 103(1), 103(2), 104(1) AI OS, 104(2) multi-agent, 104(3) RAG, 104(6) ML systems
  - ESG: 101(1) solid-state hydrogen, 102(1) electrolysis
  - Operational Efficiency: 104(4) CAPEX and OPEX
  - Digital Technology: 104(5) digital twins

## V4.17 — 2026-11-09
- **Journal PDF downloads with lead capture.** Each Chmltech Online Journal paper has a "Download PDF" button under the abstract and another in the sidebar.
  - The button opens a short form: full name, work email, company (optional), and an unticked "Send me occasional updates" box.
  - On submit, Web3Forms emails the lead to Chmltech with the subject "Journal PDF download — Vol. X, Issue Y — Name". The email lists name, email, company, updates choice, paper and page. The PDF then downloads straight away.
  - The reader's details are remembered in their browser, so the next paper takes one click; each download is still sent as a lead.
  - If the form service can't be reached, the download goes ahead anyway, so a reader is never blocked.
  - The "Print or save as PDF" button is removed. The web version of every paper stays fully public.
- **PDFs:** `gen/journal_pdfs.js` prints each paper to `assets/journal/pdf/chmltech-journal-vol<V>-issue<I>.pdf`, with a running footer showing the journal, volume and issue, and page numbers. `robots.txt` keeps the PDF folder out of search engines.
- **New privacy notice** (`privacy.html`), linked from every page footer and from the download form. It covers the forms, journal downloads, service providers (Web3Forms, GitHub Pages, Google Fonts), browser storage, and how to ask for access, correction or deletion.

## V4.16 — 2026-11-09
- **Figures in all Chmltech Online Journal papers.** After the CAPEX/OPEX pilot (V4.15), the other nine papers now have figures too: 30 across the journal. Each is numbered, captioned, referenced in the text, credited with a source line, and given alt text.

| Paper | Figures |
|---|---|
| 101(1) Solid-state hydrogen | PCT isotherms (schematic); van 't Hoff plot with the DOE delivery window; gravimetric vs volumetric capacity map against DOE targets |
| 102(1) Electrolysis | Polarization curve with stacked losses (representative parameters, passes through the DOE stack point); specific energy consumption vs cell voltage with reference values; plant block diagram with balance of plant |
| 103(1) FrugalGPT / MultiModal-GPT | LLM cascade flow; cost and accuracy results from the paper's Table 2 and HEADLINES case; MultiModal-GPT architecture with LoRA |
| 103(2) ML and DL | Milestone timeline; CNN, LSTM and Transformer block diagrams |
| 104(1) AI Operating Systems | Reference architecture stack; maturity staircase; governed invoice workflow with cost and reliability per step |
| 104(2) Multi-agent AI | Five coordination topologies; token growth from Eq. (2); compounding error with and without a verifier |
| 104(3) RAG | End-to-end pipeline with failure points; worked reciprocal rank fusion example; recall@k and nDCG@k before and after re-ranking |
| 104(4) CAPEX/OPEX | AACE accuracy ranges; six-tenths scaling; CAPEX–OPEX trade-off; Monte Carlo FCI and NPV (V4.15) |
| 104(5) Digital twins | Digital model / shadow / twin; layered twin architecture; data-reconciliation adjustments for both cases in Table 3 |
| 104(6) ML systems design | Life-cycle loop; precision/recall/F<sub>1</sub> vs threshold and PR curve (synthetic data); PSI drift monitoring against alert thresholds (synthetic data) |

- **Sources of the numbers:** every plotted number comes from the paper's own equations, tables or worked examples, or from its cited sources. Qualitative plots are labelled as schematic, and synthetic examples are labelled as synthetic. Diagrams that follow published work are redrawn in the site's style and credited "Adapted from [n]".
- **Scripts:** the drawing and placement scripts are in `content/journal/figure-scripts/` (see its README).

## V4.15 — 2026-11-09
- **Figures in journal papers (pilot).** Journal papers can now include numbered figures. Each one has a caption, a source line, alt text for screen readers, and a reference in the text. The figures are SVG graphics with live text in the site fonts and colours, so they stay sharp at any size and print cleanly in the PDF version. On phones, wide figures keep a readable size and scroll sideways.
- **Engineering CAPEX and OPEX Estimation for Process Plants (Vol. 104, Issue 4)** now has four figures:
  1. AACE estimate-class accuracy ranges (from Table 1).
  2. Capacity-exponent scaling for n = 0.4–1.0, with the worked-example point.
  3. Schematic CAPEX–OPEX trade-off with the optimum ΔT<sub>min</sub>.
  4. Monte Carlo FCI and NPV distributions. The simulation was rebuilt from the paper's stated model and reproduces its published results exactly (NPV $43.0M, IRR 13.6%, FCI P50/P90 182/217, NPV P10/P50/P90 −69/11/87).
- The checker now requires figures to be numbered in order, referred to in the text, given alt text, and backed by their SVG file. Figure sources and the scripts that draw them are in `content/journal/figures/` and `content/journal/figure-scripts/`.

## V4.14 — 2026-11-09
- **Chmltech Online Journal, Volume 104:** six new research papers, published November 9, 2026, in the same research-paper format as the existing four.

| Issue | Title | Words | Equations | Tables | References |
|---|---|---|---|---|---|
| 104(1) | AI Operating Systems: A Reference Architecture and Governance Model for Enterprise AI | 4,100 | 4 | 3 | 26 |
| 104(2) | Multi-Agent AI Systems: Architectures, Coordination Patterns and Failure Modes | 3,550 | 5 | 3 | 28 |
| 104(3) | Retrieval-Augmented Generation: Design, Evaluation and Failure Analysis for Enterprise Knowledge Systems | 3,850 | 8 | 3 | 28 |
| 104(4) | Engineering CAPEX and OPEX Estimation for Process Plants: Methods, Accuracy and Trade-offs | 4,350 | 10 | 3 | 21 |
| 104(5) | Digital Twins in Chemical Process Plants: Architecture, Modeling Approaches and Applications | 3,900 | 8 | 3 | 29 |
| 104(6) | Designing Machine Learning Systems: From Problem Framing to Production Operations | 3,650 | 6 | 3 | 30 |

- **References:** all 162 references were verified against Crossref, arXiv, or the publisher or standards page. An independent spot check of 18 found no mismatches. The worked examples in 104(1), 104(4) and 104(5) use hypothetical data and are labelled as such. The figures in 104(4) and 104(5) were computed in Python.
- **Where they appear:** the new papers show in Insights under "Chmltech Online Journal", on the home page's latest articles, in related-article lists and in the sitemap. Each has a branded Volume 104 cover for cards and social sharing.
- **Builder changes:**
  - `gen/journal_pages.py` now publishes journal papers written directly for this site, not only papers migrated from Wix.
  - New papers show no "Revised" line or revision note.

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
