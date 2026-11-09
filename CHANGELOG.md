# Changelog

## V3.6 — 2026-11-09
- Fixed the Insights category filters, search and "Show more", and the same controls on the Training exam library. Filtered-out cards were marked hidden but stayed visible because the card styles overrode the browser's hiding; a global `[hidden]{display:none}` rule fixes it.

## V3.5 — 2026-11-08
- Forms now deliver by email: Contact, Book Online and the Insights subscription post to FormSubmit, which emails info@chmltech.com. They no longer depend on the visitor's email app.
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
