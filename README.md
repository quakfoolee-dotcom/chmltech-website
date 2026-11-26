# Chmltech Ltd. website

A static website for Chmltech Ltd. (AI, Digital Transformation & Operational Excellence for Canadian SMEs).
Version: **V5.80** (see `CHANGELOG.md`).

Plain HTML, CSS and JavaScript. It has no build step and no dependencies, and runs on any static host.

## Pages

| File | Page |
|---|---|
| `index.html` | Home, with the 3D animated hero (script: `assets/js/hero3d.js`; styles: the "V5.3 homepage 3D hero" block in `assets/css/styles.css`) |
| `industries.html` | Industries overview, linking to the 8 industry pages (content: `content/industries/*.json`) |
| `solutions.html` | Core services and an overview of the 11 solution pages |
| `training.html` | Free practice-exam library (search and filters). Every exam opens on chmltech.com (`exams/<category>/`) |
| `insights.html` | All articles with search, category filters and email subscription, and the "Start here" panel above them: priority buttons that open short reading lists, and a shelf of the article series (lists: `content/insights/finder.json`; run `content/gen/insights_finder.py .` after changing it; script and styles: `assets/js/insights-finder.js`, `assets/css/insights-finder.css`) |
| `courses.html` | Free online courses and paid one-hour sessions, with the "Find your course" quiz and level/topic filters (data: `content/courses/finder.json`; run `content/gen/course_finder.py .` after changing it or adding a course; script and styles: `assets/js/course-finder.js`, `assets/css/course-finder.css`) |
| `book.html` | Book Online: free strategy call or paid session request |
| `funding.html` | Funding finder: Funding Match wizard (`#match`: 14 questions, ranked matches, funding stack, near misses, PDF report emailed through the `chmltech-report` worker; script `assets/js/funding-match.js`, styles `assets/css/funding-match.css`) above a filterable directory of federal, provincial and territorial business funding programs (data: `content/grants.json`; script: `assets/js/grants.js`). Eligibility rules: `content/funding/` (`phase1_rules_v1.json`, `redteam_corrections_v2.json`, built into `rules_v1.json` by `enrich_v1.py`). After changing the data or rules run `python3 content/funding/enrich_v1.py && python3 content/funding/funding_match_page.py`, then `seo_pass.py`. Changelog: `content/funding/CHANGELOG_Funding_Match.md` |
| `wms-demo.html` | Chmltech WMS demo showcase (V5.73, renamed from Harbor WMS in V5.74): the indexable page for the browser demo, with modules, a deep-linked 10-minute workflow, screenshots (`assets/media/wms-demo/`), data storage notes and FAQ. Source: `content/gen/wms_demo_page.py`. Links to it from Solutions, Distribution & Warehousing and warehouse series Part 7 come from `content/gen/wms_demo_links.py` |
| `WMS_demo/` | The Chmltech WMS browser demo (noindex app). Built in the harbor-wms repository (`node scripts/build-browser-demo.mjs`, patches in `scripts/browser-demo-patches.mjs`); copy `browser-demo-public/` here, keep `source.json`, then run `seo_pass.py` to add Clarity. `wms_demo/` is a redirect for the lowercase address. Tests: `node --test scripts/wms-demo.test.mjs` |
| `llm-leaderboard.html` | LLM leaderboard (menu: AI Models): searchable database of current large language models with benchmark leaderboards, best-model-by-agent-type cards and a score-versus-cost Pareto chart. Data: `content/llm/llm.json`, built by `content/llm/build_dataset.py` from the research files in `content/llm/raw/` (method: `content/llm/SPEC.md`); page: `content/gen/llm_page.py`; script and styles: `assets/js/llm.js`, `assets/css/llm.css` |
| `ai-tools.html` | AI Tools Landscape (menu: AI ▸ AI Tools Landscape): 988 current AI tools in 50 categories and 5 layers, checked November 2026. Sections: what it costs (price ladder, cost-per-output spread, cost calculator), compare categories (scorecard, open source vs paid, price/free bubble chart), Canada check (Canadian hosting, French interface, Canadian companies), a collapsible landscape map with filters, list view, tool drawer and 3-way compare, vendor changes by category with the recently retired tools, and method/FAQ with the list-change flow. Every chart has a PNG download and a data table. Data: `assets/data/ai-tools.json`, built by `content/aitools/build_data.py` from `content/aitools/source/ai_tools_V9.json` (research and red-team method: `content/aitools/SCHEMA.md`; public wording fixes: `content/aitools/public_text_overrides.json`; the build fails if internal research wording reaches the public file). Page: `content/gen/ai_tools_page.py`; scripts `assets/js/ai-tools.js`, `ai-tools-charts.js`, `ai-tools-decide.js`; styles `assets/css/ai-tools.css`. Page changelog: `content/aitools/CHANGELOG_AI_Tools.md`. After changing the data run `python3 -I content/aitools/build_data.py && (cd content/gen && python3 ai_tools_page.py)`, then `seo_pass.py`. Logos: run the **AI tools logos** workflow (Actions tab; `scripts/fetch_ai_logos.py`), which fetches each tool's icon from its own website into `assets/img/ai-tools/logos/` and opens a pull request; it needs Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests". Tools on shared hosts (github.com, huggingface.co…) keep a monogram |
| `contact.html` | Contact form, details and FAQs |
| `about.html` | About Chmltech and its CEO, with portrait, biography, career timeline and qualifications (script: `content/gen/about_page.py`) |
| `404.html` | Not-found page |
| `post/*.html` | Insights articles (one file per article, same address as on Wix). The Chmltech Online Journal papers use a research-paper layout (`assets/css/journal.css`; content: `content/journal/*.json`). |
| `<industry>.html`, `<solution>.html` | Industry and solution detail pages (for example `manufacturing.html`, `scaling-up.html`) |
| `challenge-page/*.html` | The 24 free interactive courses: lessons, labs, exam and certificate (player: `assets/js/course.js`, `assets/css/course.css`; content: `content/courses/*.json`, newer courses written in `content/courses/src/*.py`; page renderer: `content/gen/course_page.py`; to add a course: write its JSON, add it to `content/courses/finder.json` and `CARDS` in `content/gen/add_course.py`, then run `python3 content/gen/add_course.py . <name>` and `seo_pass.py`) |
| `<exam-slug>.html` (25 pages, for example `iso-9001-case-study-exam.html`) | Redirects only (V5.9). These were the mock-exam pages migrated from Wix; each now forwards to its exam in the library. The map is `content/gen/exam_redirects.json`. Keep the files so old links and search results keep working. `content/gen/build_v3.py` is a legacy generator that would recreate the old pages; do not rerun it for these |
| `exams/<category>/*.html` | The practice-exam library (147 standalone exams in 10 category folders), moved here in V5.8 from the `exam-library` repository. Catalog: `content/gen/exam_cats.json`. To add an exam: put the file in its category folder, add it to `exam_cats.json` and its card to `training.html`, then run `seo_pass.py` (adds the canonical URL, description, analytics and sitemap entry). The old `quakfoolee-dotcom.github.io/exam-library/` addresses redirect here |
| `assets/media/` | All images migrated from Wix (`thumbs/` holds card-sized versions) |
| `assets/css/oee.css`, `assets/js/oee.js` | Styles and the three slider calculators (with live charts) used by the OEE article series. The FEED series (`content/articles/feed_articles.py`) reuses the table and layout styles from `oee.css` |
| `assets/js/oee3d.js` | The 3D "OEE as a volume" box (Figure 2 of `post/what-oee-really-measures.html`); follows that article's sliders. Styles are in `assets/css/oee.css`. |
| `assets/js/psv3d.js`, `hx3d.js`, `pm3d.js`, `tk3d.js` | Interactive 3D models (Figure 2) in the pressure relief, heat exchanger, pump and tank articles. They need `assets/js/vendor/three-r128.min.js`. Figure markup: `content/articles/fig3d/`, inserted by `content/articles/sizing_articles.py`; styles: the V5.17 blocks in `assets/css/oee.css`. |
| `assets/js/cv3d.js`, `ln3d.js` | Interactive 3D models (Figure 2) in the control valve and line sizing articles (sources: `content/articles/sizing_valve_article.py`, `sizing_line_article.py`; figure markup in `content/articles/fig3d/valve.html`, `line.html`). They need `assets/js/vendor/three-r128.min.js`. |
| `assets/js/rx3d.js`, `ag3d.js` | Interactive 3D models (Figure 2) in the reactor jacket and agitator articles (sources: `content/articles/sizing_jacket_article.py`, `sizing_agitator_article.py`; figure markup in `content/articles/fig3d/jacket.html`, `agitator.html`). CFD-style colour fields with particles carried by a schematic velocity field. They need `assets/js/vendor/three-r128.min.js`. |
| `assets/js/orch5.js` | The interactive Figure 1 of journal Vol. 106, Issue 1 (looping five-model orchestration explorer with a Compare all view). Data and markup: `content/journal/live/orch5.html`, written with the static print SVG by `content/journal/figure-scripts/orch5.py`, which any paper can reuse with its own models and labels (Vol. 106, Issue 2 does, via `rad5.py` → `content/journal/live/rad5.html`); styles: the "Vol. 106 orch5" block in `assets/css/journal.css`. A journal figure block with `"live": "<name>"` inserts `content/journal/live/<name>.html`. |
| `assets/js/math.js`, `assets/js/vendor/katex/` | Typeset equations. Article sources write LaTeX with `eq()` (display) and `im()` (inline) from `content/articles/sizing_articles.py` and end the body with `mathjs()`, which loads the vendored KaTeX 0.16.11 only on that page. |
| `assets/sim/q2c-factory.html`, `assets/js/q2c.js`, `assets/js/vendor/` | The quote-to-cash series (source: `content/articles/q2c_articles.py`). `assets/sim/q2c-factory.html` is the 3D factory simulator: one self-contained page holding the simulation model and the 3D scene, not indexed on its own. Part 2 embeds it in a frame with `#embed` on the address (no header; it reports its height to the article). `q2c.js` sizes that frame and runs the payback calculator in Part 3. `vendor/` holds Three.js r128 and its OrbitControls (MIT licence, `three-LICENSE.txt`), used only by the simulator. The figures quoted in the three articles are the simulator's results at its starting settings (`DAYS` and `RESULTS` in `q2c_articles.py`); if the model's defaults change, rerun it and update them. |
| `assets/js/wh3d.js` … `wh3d8.js` | The warehouse operations series (8 parts, source: `content/articles/wh_articles.py`, `wh2_articles.py` … `wh8_articles.py`, each with its model `wh_model.py`, `wh2_model.py` … `wh8_model.py`, which feeds both the article numbers and the 3D figure data). One script per part, Figure 2 of each: Part 1 pallet racks and slotting, Part 2 pick routes, Part 3 receiving day replay, Part 4 stock-record accuracy, Part 5 packing line, Part 6 labour heat map, Part 7 what the system knows, Part 8 automation. They need `assets/js/vendor/three-r128.min.js`; styles are the `.wh3d*` blocks (V5.31–V5.38) in `assets/css/oee.css`. Each figure tours its states on its own with a countdown bar, stops when the reader picks one and resumes after a minute without clicks. |
| `assets/sim/layout-lab.html`, `assets/js/wl-engine.js`, `wl-lab.js`, `wl1.js` | The Warehouse Layout Lab, Figure 1 of the warehouse layout series Part 1 (source: `content/articles/wl1_articles.py`). `wl-engine.js` is the simulation (one shift, two layouts, 1 m grid, pickers, forklifts, pallet jack, trucks; runs in Node and the browser); `wl-lab.js` draws it (2D canvas plan, 3D view with Three.js r128 and OrbitControls from `vendor/`, one shared camera), with the sliders and the KPI table. The article embeds the page with `#embed` (it reports its height; `wl1.js` sizes the frame). `content/articles/wl1_model.js` runs the engine and writes `wl1_results.json`, the numbers the article quotes: rerun it and `wl1_articles.py` after any engine change. `?jump=SECONDS` on the Lab's address starts the replay later in the shift (for testing). One Lab serves the whole warehouse layout series: `s=p2` (`#embed&s=p2` in an article, `window.WL_SCENE` in a self-contained preview) opens Part 2's three flow patterns (`redesign` U-shape, `thru`, `lshape`), numbers from `content/articles/wl2_model.js` → `wl2_results.json` → `wl2_articles.py`. `s=p3` opens Part 3's three aisle widths (`wide` 4 m, `redesign` 3 m, `vna` 2 m with an aisle lock), numbers and the cost model from `content/articles/wl3_model.js` → `wl3_results.json` → `wl3_articles.py`. `s=p4` opens Part 4's manufacturer (`mstore`, `mside`, `mkanban`: central store, line-side supermarket, kanban milk run feeding two filling lines), numbers from `content/articles/wl4_model.js` → `wl4_results.json` → `wl4_articles.py`. Part 5 (no new Lab scenario) has a payback calculator, `assets/js/wl5.js`, whose presets come from `content/articles/wl5_model.js` → `wl5_results.json` → `wl5_articles.py` (it reads the Parts 1 and 4 results and runs the engine with `inTrucks` and `forks`). A new part adds its layouts to `makeLayout` and a scenario to `SETS` in `wl-lab.js`; keep Part 1 (`asis`, `redesign`) unchanged so its published numbers hold. |
| `assets/js/fp.js` | The yield-gap payback calculator in the first principles thinking article (source: `content/articles/first_principles_article.py`) |
| `assets/js/bets.js`, `assets/js/stress.js` | The small-tests portfolio calculator (innovation article) and the profit stress-test calculator (uncertain economy article); source: `content/articles/v527_articles.py` |
| `assets/js/scaleup.js` | The cooling-capacity calculator and chart in Part 1 of the scale-up series (source: `content/articles/process_eng_articles.py`) |
| `assets/js/runaway.js` | The cooling failure (MTSR) calculator in Part 1 of the process safety series (source: `content/articles/safety_articles.py`) |
| `assets/media/pfd-pid/` | The example PFD and P&ID drawings (SVG) used in the "How to read a PFD and a P&ID" article |
| `assets/downloads/` | Files offered for download from articles (for example the inventory template workbook) |

Shared files: `assets/css/styles.css` (all styling, with brand colours as CSS variables at the top), `assets/js/main.js` (mobile menu, the "AI" menu dropdown, forms, insights filter) and `assets/img/` (logo, mark and icons).

## Preview locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Forms (email delivery)

The Contact, Book Online and Insights subscription forms send submissions by email through [Web3Forms](https://web3forms.com) (free plan, 250 submissions a month).

- **Account:** the form "Chmltech Website" lives in the Web3Forms account of the owner's Gmail account. Submissions go to that account's recipient email; change it in the Web3Forms dashboard.
- **Access key:** `WEB3FORMS_KEY` in `assets/js/main.js`. The key is designed to be public. To rotate it, create a new key in Web3Forms and replace it there.
- **Emails:** the subject names the form and the sender, for example "Strategy call booking request — Name". The visitor's email is included, so you can reply directly.
- **Spam:** a hidden honeypot checkbox (`botcheck`) blocks simple bots. You can turn on extra spam filtering in the Web3Forms dashboard.
- **Fallback:** if the service can't be reached, the visitor is offered an email draft to info [at] chmltech [dot] com.
- Web3Forms only accepts submissions from real browsers, so test from the live site.

## Email address protection

The email address is never written into the page source, so address-harvesting bots can't scrape it.

- Email links are written as `<a class="js-mail" data-u="info" data-d="chmltech.com" href="contact.html">info [at] chmltech [dot] com</a>`.
- `assets/js/main.js` rebuilds the real address and `mailto:` link in the visitor's browser.
- Without JavaScript, the link shows the spelled-out form and opens the contact form.
- After each build, run `node gen/journal_pdfs.js <site_dir> <journal_json_dir>` (journal PDFs), `python3 gen/dedupe_images.py <site_dir>` (removes repeated pictures in articles), then `python3 gen/protect_email.py <site_dir>`. It is safe to run twice. It reports any page that still contains the plain address.
- **Main menu "AI" dropdown** (AI Models, AI Tools Landscape): `python3 content/gen/nav_ai_dropdown.py .` writes it into every page header and adds "AI tools landscape" to the footer; new pages copy their header from existing pages, so they inherit it.
- **Last step after any build or new article:** run `python3 content/gen/seo_pass.py .` from the site root. It sets clean canonical URLs, social-sharing tags and structured data on every page, and rebuilds `sitemap.xml` and `llms.txt`. It is safe to run any number of times. It also stamps every stylesheet and script link with a content hash (`?v=…`, `content/gen/assetver.py`) so browsers fetch changed files at once; never add `?v=` by hand.

## Journal PDF downloads (leads)

- Each journal paper's "Download PDF" form posts to Web3Forms with the same key as the other forms, so leads arrive by email with the subject "Journal PDF download — Vol. X, Issue Y — Name".
- The free Web3Forms plan allows 250 submissions a month across all forms. Watch the count in the Web3Forms dashboard.
- PDFs live in `assets/journal/pdf/` and are excluded from search engines by `robots.txt`. A determined visitor can still find the link: the form is for lead capture, not access control.

## Article downloads (leads)

- A download offered from an article (for example the inventory template in `assets/downloads/`) uses the same form as the journal PDFs: `assets/js/download.js`, `assets/css/download.css` and a `<dialog id="dl">` in the article body. Leads arrive with the subject "<data-ref> download — Name".
- To change the wording or the file, edit `DL_FORM` and `tpl_box` in `content/articles/inventory_articles.py` and rebuild the articles.
- These submissions count toward the same Web3Forms monthly limit.

## Search (SEO)

- `content/gen/seo_pass.py` owns the canonical URLs (clean form, without `.html`), Open Graph and Twitter tags, JSON-LD structured data, `sitemap.xml` (with `lastmod`) and `llms.txt`. Edit it rather than the pages for site-wide SEO changes.
- Sitemap `lastmod` (V5.80): articles use their own `dateModified`; every other page gets its date from `content/gen/lastmod.py`, which fingerprints the page's own content (not the head, menu, footer, analytics or link forms) and keeps the dates in `content/gen/lastmod.json`. Commit that file with each release. A sitewide template change therefore leaves the dates alone; a real content change gets the day `seo_pass.py` runs. To rebuild the dates from git history: `python3 content/gen/lastmod.py seed .`
- **Search keywords:** `content/gen/seo_keywords.py` sets the title, main heading (H1) and meta description of the ~30 main pages (home, solutions, industries, About, Training, Courses, Insights and others). The old heading stays as the line just under the new H1 (style `.hero-slogan`). Edit the table there, never the pages, then run `seo_pass.py`.
- The raw exam apps in `exams/` carry `noindex, indexifembedded`, so search engines rank the exam pages that embed them, not the bare apps.
- **Analytics:** Microsoft Clarity (project `zcd5uqw2cz`, dashboard at clarity.microsoft.com) is added to every indexable page by `seo_pass.py` (`CLARITY_ID`). The privacy page names it. **Owner opt-out:** open any page with `?notrack=on` once per browser/device and Clarity no longer loads there (`?notrack=off` undoes it; stored in that browser's localStorage).
- Search engine verification: Google Search Console uses a DNS TXT record at IONOS (keep it); Bing Webmaster Tools uses a DNS CNAME record at IONOS (keep it); the `msvalidate.01` meta tag in `index.html` is a backup.
- Redirect stubs (old Wix addresses) carry `noindex` and are left out of the sitemap.

## Deploy

- **GitHub Pages:** go to Settings → Pages, set the source to the `main` branch and the `/ (root)` folder.
- **Netlify or Cloudflare Pages:** drag and drop the folder, or connect the repository. Leave the build command empty and set the publish directory to `/`.
- **Custom domain:** the site is served at `www.chmltech.com`, set by the `CNAME` file. DNS is at IONOS: four A records for `@` (185.199.108–111.153) and a CNAME for `www` pointing to `quakfoolee-dotcom.github.io`. Keep the MX, SPF, DKIM and DMARC records unchanged, because they carry email.
- **Forwarding domain:** `chmltech-consulting.com` should redirect to `https://www.chmltech.com/` and keep the page path, so old `/post/...` links still land on the same article.

## Adding a new article

1. Write `content/articles/<slug>.json` (copy an existing one: title, description, categories, tags, body HTML, date, author, read time).
2. Run `python3 content/gen/add_article.py <slug>`. It writes `post/<slug>.html`, draws the cover, adds the card at the top of `insights.html`, raises the article counts and updates `sitemap.xml`.
3. Add an entry to `CHANGELOG.md`.
4. For an article in a series, add `"series": {"name": "FEED series", "part": 1, "of": 3}` to its file before step 2, then run `python3 content/gen/series_labels.py` so every card shows the label. Update `of` in the other parts when a series grows.
5. If the article belongs in a "Start here" reading list, add its slug to `content/insights/finder.json`. Then run `python3 content/gen/insights_finder.py .` (always run it for a series article, so the series shelf shows the new part; a new series also needs a one-line description in `finder.json`).
6. The home page "Latest insights" section is not updated by the script. To feature the new article, copy its card from `insights.html` into `index.html` and update the "All N articles" button there.

Categories are slugs such as `process-engineering` or `operational-efficiency`; the full list is `CAT_NAMES` in `content/gen/add_article.py`. A card shows the first two categories as tags, so put the main subject first.

To do it by hand instead: copy any file in `post/`, replace the title, date, body and meta description, then add a card at the top of the list in `insights.html`.

## Leaving Wix: checklist

1. Deploy this repository (GitHub Pages: Settings → Pages → `main` / root).
2. Done: forms deliver by email via Web3Forms (see Forms above).
3. Done: `www.chmltech.com` points to GitHub Pages. Next, set `chmltech-consulting.com` to forward to it while keeping page paths (Cloudflare redirect rule, or registrar forwarding if it keeps paths).
4. Check a few old addresses, for example `/post/...`, `/scaling-up` and `/challenges`.
5. Cancel the Wix premium plan. If Wix is also the domain registrar, transfer the domain before cancelling.

## Before going live

Search the code for `TODO`:

- **Social links:** the footer links point to the platforms' home pages. Replace them with Chmltech profile URLs.
- **Booking:** you can replace the request form in `book.html` with an embedded scheduler such as Calendly or Microsoft Bookings.

## Updating the LLM leaderboard

1. Refresh the research files in `content/llm/raw/` (one set per source; schema in `content/llm/SPEC.md`). For the Arena Text, Vision and WebDev boards, run `python3 content/llm/arena_full.py <folder with Arena *.latest.parquet files>`.
2. Add or change models and name aliases in `content/llm/catalog.py`. Matching rules are in `content/llm/match.py`.
3. `python3 content/llm/build_dataset.py`, then `python3 content/gen/llm_page.py`.
4. Have the result checked against the sources (red team) before publishing, and update the "data as of" date (`AS_OF` in `build_dataset.py`).

## WMS browser demo

The full browser-only Chmltech WMS demo lives in `WMS_demo/` and is served at `https://www.chmltech.com/WMS_demo/` after this change is deployed. It uses fictional English sample records and browser-local storage; no backend or login is required. See [WMS_demo/README.md](WMS_demo/README.md) for developer handoff, storage/reset behavior and the canonical build source. Run `node --test scripts/wms-demo.test.mjs` to verify the packaged workflows and asset graph. The dedicated workflow runs these checks on pull requests and main.

