# Chmltech Ltd. website

A static website for Chmltech Ltd. (AI, Digital Transformation & Operational Excellence for Canadian SMEs).
Version: **V4.67** (see `CHANGELOG.md`).

Plain HTML, CSS and JavaScript. It has no build step and no dependencies, and runs on any static host.

## Pages

| File | Page |
|---|---|
| `index.html` | Home |
| `industries.html` | Industries overview, linking to the 8 industry pages (content: `content/industries/*.json`) |
| `solutions.html` | Core services and an overview of the 11 solution pages |
| `training.html` | Free practice-exam library (search and filters) plus self-hosted mock exams |
| `insights.html` | All articles with search, category filters and email subscription |
| `courses.html` | Free online courses and paid one-hour sessions |
| `book.html` | Book Online: free strategy call or paid session request |
| `funding.html` | Funding finder: filterable directory of federal, provincial and territorial business funding programs (data: `content/grants.json`; script: `assets/js/grants.js`) |
| `llm-leaderboard.html` | LLM leaderboard (menu: AI Models): searchable database of current large language models with benchmark leaderboards, best-model-by-agent-type cards and a score-versus-cost Pareto chart. Data: `content/llm/llm.json`, built by `content/llm/build_dataset.py` from the research files in `content/llm/raw/` (method: `content/llm/SPEC.md`); page: `content/gen/llm_page.py`; script and styles: `assets/js/llm.js`, `assets/css/llm.css` |
| `contact.html` | Contact form, details and FAQs |
| `about.html` | About Chmltech and its CEO, with portrait, biography, career timeline and qualifications (script: `content/gen/about_page.py`) |
| `404.html` | Not-found page |
| `post/*.html` | Insights articles (one file per article, same address as on Wix). The Chmltech Online Journal papers use a research-paper layout (`assets/css/journal.css`; content: `content/journal/*.json`). |
| `<industry>.html`, `<solution>.html` | Industry and solution detail pages (for example `manufacturing.html`, `scaling-up.html`) |
| `challenge-page/*.html` | The 12 free interactive courses: lessons, labs, exam and certificate (player: `assets/js/course.js`, `assets/css/course.css`; content: `content/courses/*.json`) |
| `exams/*.html` + `<exam-slug>.html` | Self-hosted mock exams and tools migrated from Wix |
| `assets/media/` | All images migrated from Wix (`thumbs/` holds card-sized versions) |
| `assets/css/oee.css`, `assets/js/oee.js` | Styles and the three slider calculators (with live charts) used by the OEE article series. The FEED series (`content/articles/feed_articles.py`) reuses the table and layout styles from `oee.css` |
| `assets/js/scaleup.js` | The cooling-capacity calculator and chart in Part 1 of the scale-up series (source: `content/articles/process_eng_articles.py`) |
| `assets/js/runaway.js` | The cooling failure (MTSR) calculator in Part 1 of the process safety series (source: `content/articles/safety_articles.py`) |
| `assets/media/pfd-pid/` | The example PFD and P&ID drawings (SVG) used in the "How to read a PFD and a P&ID" article |
| `assets/downloads/` | Files offered for download from articles (for example the inventory template workbook) |

Shared files: `assets/css/styles.css` (all styling, with brand colours as CSS variables at the top), `assets/js/main.js` (mobile menu, forms, insights filter) and `assets/img/` (logo, mark and icons).

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
5. The home page "Latest insights" section is not updated by the script. To feature the new article, copy its card from `insights.html` into `index.html` and update the "All N articles" button there.

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
