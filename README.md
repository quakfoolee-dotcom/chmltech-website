# Chmltech Ltd. website

A static website for Chmltech Ltd. (AI, Digital Transformation & Operational Excellence for Canadian SMEs).
Version: **V4.15** (see `CHANGELOG.md`).

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
| `contact.html` | Contact form, details and FAQs |
| `404.html` | Not-found page |
| `post/*.html` | Insights articles (one file per article, same address as on Wix). The 10 Chmltech Online Journal papers use a research-paper layout (`assets/css/journal.css`; content: `content/journal/*.json`). |
| `<industry>.html`, `<solution>.html` | Industry and solution detail pages (for example `manufacturing.html`, `scaling-up.html`) |
| `challenge-page/*.html` | The 12 free interactive courses: lessons, labs, exam and certificate (player: `assets/js/course.js`, `assets/css/course.css`; content: `content/courses/*.json`) |
| `exams/*.html` + `<exam-slug>.html` | Self-hosted mock exams and tools migrated from Wix |
| `assets/media/` | All images migrated from Wix (`thumbs/` holds card-sized versions) |

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
- After each build, run `python3 gen/dedupe_images.py <site_dir>` (removes repeated pictures in articles), then `python3 gen/protect_email.py <site_dir>`. It is safe to run twice. It reports any page that still contains the plain address.

## Deploy

- **GitHub Pages:** go to Settings → Pages, set the source to the `main` branch and the `/ (root)` folder.
- **Netlify or Cloudflare Pages:** drag and drop the folder, or connect the repository. Leave the build command empty and set the publish directory to `/`.
- **Custom domain:** the site is served at `www.chmltech.com`, set by the `CNAME` file. DNS is at IONOS: four A records for `@` (185.199.108–111.153) and a CNAME for `www` pointing to `quakfoolee-dotcom.github.io`. Keep the MX, SPF, DKIM and DMARC records unchanged, because they carry email.
- **Forwarding domain:** `chmltech-consulting.com` should redirect to `https://www.chmltech.com/` and keep the page path, so old `/post/...` links still land on the same article.

## Adding a new article

1. Copy any file in `post/` and rename it with the new article's slug.
2. Replace the title, date, body and meta description.
3. Add a card for it at the top of the list in `insights.html` (copy an existing `<article class="article">` block).

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
