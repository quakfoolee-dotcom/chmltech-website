# Chmltech Ltd. website

A static website for Chmltech Ltd. (AI, Digital Transformation & Operational Excellence for Canadian SMEs).
Version: **V2** (see `CHANGELOG.md`).

Plain HTML, CSS and JavaScript. It has no build step and no dependencies, and runs on any static host.

## Pages

| File | Page |
|---|---|
| `index.html` | Home |
| `industries.html` | Industries (8 sectors, with anchors such as `#manufacturing`) |
| `solutions.html` | Core services and all 10 solutions (anchors such as `#rapid-lean-assessment`) |
| `training.html` | Training areas and delivery formats |
| `insights.html` | Insight topics with a topic filter and an email subscription form |
| `courses.html` | Course catalogue and FAQs |
| `book.html` | Book Online: strategy-call request form |
| `contact.html` | Contact form, details and FAQs |
| `404.html` | Not-found page |

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
- **Custom domain:** point `www.chmltech-consulting.com` at the host. Canonical URLs and `sitemap.xml` already use that domain.

## Before going live

Search the code for `TODO`:

- **Social links:** the footer links point to the platforms' home pages. Replace them with Chmltech profile URLs.
- **Testimonial:** confirm the exact quote from Dora Bridges (`index.html`, `solutions.html`).
- **Insights:** the article cards are topic previews marked "Article coming soon". Link them to published articles when they are ready.
- **Booking:** you can replace the request form in `book.html` with an embedded scheduler (Wix Bookings, Calendly or Microsoft Bookings).
- **Course fees:** these show "On request". Add fees and dates if you want to publish them.
