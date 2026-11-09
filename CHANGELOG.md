# Changelog

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
