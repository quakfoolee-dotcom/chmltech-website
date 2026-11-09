# Chmltech Ltd. website

A static website for Chmltech Ltd. (AI, Digital Transformation & Operational Excellence for Canadian SMEs).
Version: **V3.4** (see `CHANGELOG.md`).

Plain HTML, CSS and JavaScript. It has no build step and no dependencies, and runs on any static host.

## Pages

| File | Page |
|---|---|
| `index.html` | Home |
| `industries.html` | Industries overview, linking to the 8 industry pages |
| `solutions.html` | Core services and an overview of the 11 solution pages |
| `training.html` | Free practice-exam library (search and filters) plus self-hosted mock exams |
| `insights.html` | All articles with search, category filters and email subscription |
| `courses.html` | Free online courses and paid one-hour sessions |
| `book.html` | Book Online: free strategy call or paid session request |
| `contact.html` | Contact form, details and FAQs |
| `404.html` | Not-found page |
| `post/*.html` | Insights articles (one file per article, same address as on Wix) |
| `<industry>.html`, `<solution>.html` | Industry and solution detail pages (for example `manufacturing.html`, `scaling-up.html`) |
| `challenge-page/*.html` | Free course pages |
| `exams/*.html` + `<exam-slug>.html` | Self-hosted mock exams and tools migrated from Wix |
| `assets/media/` | All images migrated from Wix (`thumbs/` holds card-sized versions) |

Shared files: `assets/css/styles.css` (all styling, with brand colours as CSS variables at the top), `assets/js/main.js` (mobile menu, forms, insights filter) and `assets/img/` (logo, mark and icons).

## Preview locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Make the forms send email (5 minutes)

The Contact, Book Online and Insights forms post to a form service. Until one is configured, submitting a form opens the visitor's email app with the message addressed to info@chmltech.com.

1. Create a free form at https://formspree.io (or any service that accepts a standard form POST and returns JSON).
2. Copy the endpoint, which looks like `https://formspree.io/f/abcdwxyz`.
3. Replace `https://formspree.io/f/YOUR_FORM_ID` in `contact.html`, `book.html` and `insights.html`.

Each form includes a hidden spam honeypot field (`_gotcha`).

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
2. Set up Formspree (see above) so the forms deliver email.
3. Done: `www.chmltech.com` points to GitHub Pages. Next, set `chmltech-consulting.com` to forward to it while keeping page paths (Cloudflare redirect rule, or registrar forwarding if it keeps paths).
4. Check a few old addresses, for example `/post/...`, `/scaling-up` and `/challenges`.
5. Cancel the Wix premium plan. If Wix is also the domain registrar, transfer the domain before cancelling.

## Before going live

Search the code for `TODO`:

- **Social links:** the footer links point to the platforms' home pages. Replace them with Chmltech profile URLs.
- **Booking:** you can replace the request form in `book.html` with an embedded scheduler such as Calendly or Microsoft Bookings.
- **Free courses:** the step-by-step lessons of the 6 free programs were behind a Wix member login and are not in this repository. Course pages offer "Request access" until the lessons are added.
