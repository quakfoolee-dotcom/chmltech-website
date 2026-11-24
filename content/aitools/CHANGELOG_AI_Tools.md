# AI Tools Landscape page (ai-tools.html): changelog of page drafts

Data: `content/aitools/source/ai_tools_V9.json` → `content/aitools/build_data.py` → `assets/data/ai-tools.json`.
Page: `content/gen/ai_tools_page.py` → `ai-tools.html`. Scripts: `assets/js/ai-tools.js`, `assets/js/ai-tools-charts.js`,
`assets/js/ai-tools-decide.js` (from V5). Styles: `assets/css/ai-tools.css` (plus the shared `styles.css`, `grants.css`, `llm.css`).
Each draft was reviewed as a self-contained preview, `ai-tools_Draft_V<n>.html`.

## V5.2 – live-site fixes (site V5.79)
- List view: the "Free · Open · Canada / Compare" header no longer gets cut off. Units wrap under the price, flag chips wrap, the tool column narrows, Category is hidden at 901–980 px, and phones show the checkbox only (each has a screen-reader name).
- Bubble chart: coloured by layer with the map's layer colours (L1 #0B2A5A, L2 #0B6FA4, L3 #B04A12, L4 #2F6B3A, L5 #6A3D8F); highlighting a layer greys the others (#8C95A1).

## V5.1 – red-team fixes to V5 (28 findings)

**Data (`build_data.py`, new `public_text_overrides.json`)**
- Vendor changes are counted once per product (V5-02). A retired entry whose base name (lower case, brackets removed) matches a
  current tool or an earlier-counted retired entry, or whose name carries a duplicate or listing marker, is not a market event. This
  covers the Moveworks, Phind, Wordtune, Drift and Claude Code duplicates. Market events went from 64 to 60. Enterprise Search went
  from 4 of 17 to 3 of 16, and Prompt-to-App from 6 of 23 to 5 of 22. Writing & Copy left the top 15, and the middle category is
  now 11%.
- Public wording (V5-03, V5-09, V5-24):
  - `public_text()` now drops internal sentences and bracketed asides anywhere. It strips every `SELF-HOST…:` prefix and turns
    pipe-joined cost notes into one reader sentence ("Hobby $19 / 5,000 pages: about $3.80 per 1,000 pages at full use of the
    plan."). It no longer writes "our previous list showed" or "not rechecked".
  - `public_text_overrides.json` (tool id → field → text, or null to drop) rewrites the 52 strings that no general rule can fix.
    It is applied last.
  - Status notes are exported only for tools with a badge.
  - A final scan fails the build if any internal term reaches the public file (red team, gap list, prior knowledge, not
    rechecked, previous list showed, in this check, as read, inferred by, "see … row", separate or combined row, bot check, not
    verified here, prices from news, v8 anywhere). Budget, fetch, curl, "row" and repo/prior knowledge are banned in the note
    fields; product names and descriptions can legitimately say "budgets", "Fetch" or "AI red teaming".
- Public keys: `v8_row` became `prev`; `flow.v8_total`, `retired_v8` and `v9_total` became `prev_total`, `prev_removed` and
  `total`, and `prev_removed_ev` was added. The `version` key was dropped. Retired entries carry `pn` (the public name, without
  duplicate or listing markers) and `cc` (the current category) instead of the old category name.
- `cap` marks Canadian hosting that applies only to some plans, tiers or tenants (9 tools), using the same rule as the drawer
  (V5-06). Coveo and Tali AI have public Canada notes written from their evidence.

**Page**
- "Vendor changes" is the term everywhere (V5-01): headline, card title, tooltip, scorecard column ("Vendor changes · acquired,
  renamed, sunsetting, gone") and notes. The definition always lists acquired (including pending), renamed or merged, sunsetting,
  and shut down or folded in.
- Counts reconcile (V5-04, V5-15):
  - Recently retired lists only the 60 real retired products, under public names and current categories.
  - The 83 duplicates and list clean-ups are counted but not listed.
  - The caption says that 108 of all 143 removed entries were on the previous list.
  - The flow chart labels that step "Removed" and splits it into 43 retired products and 65 duplicates or clean-ups.
  - The banner and the vendor-change footnote use the same numbers.
- Canada check (V5-06, V5-10, V5-11):
  - A "Yes, on some plans only" mark (dot with a star) is used in the matrix, legend, tooltip, drawer, compare view and PNG.
  - The heading reads "… can keep your data in Canada, on at least one plan", and the caption gives the count.
  - The Price column names the pricing model (see pricing, priced in EUR, open source + paid cloud, usage-based).
  - Non-Canadian vendors get a blank cell, not a dash.
- Map: the full-map button is hidden in List view (V5-07). The bubble and spread SVGs use `role="group"` (V5-08).
- Ladder (V5-12, V5-13, V5-14, V5-27):
  - The caption names the "median of at least 6 published prices", and reads cleanly when one layer has only one row.
  - Phone rows show "· N prices · median $X", the footnote wording follows, and dots have smaller hit areas.
  - The axis starts at $2, with ‹ › overflow markers.
- Scorecard (V5-12, V5-16, V5-17, V5-20, V5-25):
  - Medians from fewer than 6 prices are in italics with "from N prices".
  - The note explains the current-plus-gone base used for vendor changes.
  - The PNG carries a three-line footnote.
  - Cells are no longer tab stops; the counts are in visually hidden text.
  - Group rows use `scope="rowgroup"`, with one `tbody` per group.
- Vendor risk is a full-width card with untruncated labels (V5-21). Recently retired sits below it in two columns. Keyboard focus
  on a category name shows its breakdown tooltip (V5-20). The narrow layouts of the spread, flow and risk charts have left padding.
- PNG export (V5-05, V5-23): titles wrap. The footer reads "checked November 2026" with no internal version, and it wraps on
  narrow charts.
- Reduced motion turns off smooth scrolling on this page (V5-18).
- Contrast (V5-19): dim text is #5A6475; the grey "other" dots, the bubble greys and the Canada "not checked" dash are #868E9A
  (3.3:1); the Canada × is #5A6475.
- No-JS (V5-22): each chart has a short fallback line, and the Canada check lists the 50 tools that can keep data in Canada.
- Wording (V5-23, V5-26, V5-28):
  - The banner reads "checked by an independent reviewer". The FAQ describes AI-assisted research and two independent reviews,
    using "entries" rather than "rows".
  - The compare heading says "at least half".
  - The hero Canada stat reads "on at least one plan".
  - List-view headers wrap.

## V5 – design-review release

Implements the chart design review (price ladder, category scorecard and Canada check prototypes, plus the page-level fixes).

**New page order:** hero → "Checked" banner → What it costs → Compare categories → Canada check → landscape map → Vendor risk
and recently retired → Method and FAQ. Section headings state the finding, and the numbers in them come from the data (for example
"Half of priced AI tools start at $20 a month or less."). The hero buttons now go to What it costs, Canada check and the map. The
hero's Canada stat links to the Canada check, and a new hero stat gives the typical cheapest paid plan.

**Data (`build_data.py`)**
- Adds `pp`, the pro (next paid tier) price in USD per month. Like the entry price, it is exported only for US-dollar prices; it
  is shown in the price-ladder tooltip.
- Retired rows get `ev` (true for market events: acquired, renamed, sunsetting, shut down, merged) and `cc` (their current
  category; three renamed categories are mapped). Retired rows with status "active" are list clean-ups, not market events, and are
  never counted as churn.

**New charts (`ai-tools-decide.js`)**
- **Price ladder** ("What a paid plan costs in each category"): every tool's cheapest paid plan, by category, on a log scale. It
  has a median tick and a middle-half band, and it includes categories with at least 6 published USD prices. A layer select filters
  it. The highlight options are free plan, open source, Canadian company or none, with the highlighted tools in brand blue and
  the rest in grey. Dots can be focused with the keyboard and open the tool. Category names open the category on the map. It has a
  data table and a PNG export with its legend.
- **Category scorecard**: a sortable heatmap table with a layer filter. Sorting goes descending, then ascending, then back to
  grouped, and `aria-sort` is set on each heading. It uses one blue ramp, and the mid-tones are skipped so the text keeps 4.5:1
  contrast; the step falls at 50%. Canada hosting shows "N of M checked" with "x cloud · y self-host" underneath, or "not
  checked". The note says that "not checked" does not mean "not available". Cells can be focused and have tooltips. The PNG export
  draws an SVG twin of the visible rows.
- **Canada check**: a coverage bar (hosted in Canada, self-host only, checked: no, not checked yet), an area select, filter chips
  that combine, and a matrix that uses icons and labels rather than colour alone. "A dash means not checked; it is not a no." Each
  tool name is a button that opens the tool. There is an empty state, a Digital Assessment call to action, and a PNG export (an
  SVG twin of the filtered list).
- **Vendor risk by category** replaces "The market in motion". It is a ranked bar chart of the share of each category's tools that
  were acquired (including pending), renamed or merged, sunsetting, or shut down or folded in. Only market events are counted;
  list clean-ups are left out and counted in the footnote. It covers categories with at least 8 current tools, shows the top 15
  with a "Show all" option, and prints "k of n (p%)" at each bar. Tooltips give the breakdown, and it has a data table. The
  "Recently retired" list sits next to it and tags list clean-ups.

**Changed charts (`ai-tools-charts.js`)**
- Bubble chart (now in Compare categories): colour-blind-safe single highlight. The layer buttons pick one layer in brand blue
  (#0B6FA4) with the rest light grey, and "All layers" shows one neutral colour. Bubbles no longer encode size; they have a uniform
  radius, with the tool count in the tooltip and table. Labels show only the highlighted layer and the 8 categories farthest from
  the crowd. Bubbles can be focused with the keyboard. Under 600px the plot is hidden and a one-line pointer to the price ladder
  shows instead; the data table stays, and the PNG export still works.
- Cost-per-output spread: the cheapest and dearest tool in each row are named, all costs are rounded to two significant figures,
  it uses one hue, and dots can be focused and opened from the keyboard.
- Open source vs paid: moved into Compare categories. Its footnote no longer repeats the caption.
- The list-change flow (Sankey) moved into Method and FAQ. Its headline stat is now in the "Checked" banner.
- Shared helpers are exposed as `window.ATCharts`. PNG export also takes an SVG twin for HTML charts, and it copies each legend
  swatch as drawn. Tooltips also show on keyboard focus.
- Narrow cards (container width 560px or less) show a compact icon-only Download PNG button that does not wrap under the title.
  Its accessible name is still "Download PNG: <chart title>".

**Map and layout (`ai-tools.js`, `ai-tools.css`, `ai_tools_page.py`)**
- The landscape map is collapsed by default: it shows a limited height with a fade and a "Show the full map (N tools)" button.
  The map expands by itself when the reader searches or filters, when the page opens with `?q`, `?c` or `?l`, when
  `ATools.showCategory` runs, and when keyboard focus moves past the fold. Without JavaScript the full map shows.
- The cost calculator now sits under What it costs (its anchor `#cost` is kept).
- New CSS is scoped with the `atl-`, `ats-`, `atc-` and `atr-` prefixes and uses the shared tokens; no new `:root` block.
- Every caption and heading is computed from the data, in Python for the static page and in the browser for filtered views. The
  numbers were checked to match.

## V4 – red-team fixes
Fixes from the independent page QC (`redteam/page_qc.md`). These include no sideways scroll at 390px, correct cost-view
minimums, and churn that excludes list clean-ups. Other fixes: an honest bubble caption, the Canada hosting stat split into
vendor cloud and self-host with plan caveats, a legend in chart PNG exports, the logo pipeline (no logo for domains shared by several
vendors; the workflow installs into a virtualenv and checks out full history so sitemap dates stay right), and a number of minor
and nit items.

## V3 – bubble layer toggles
The category bubble chart got layer toggle buttons (select to hide or show a layer, double-click to isolate one), which
re-render the chart and its table.

## V2 – five charts
Added "What the data shows": the category bubble map, the cost-per-output spread, open source vs paid by layer, the market in
motion and the previous list → this list flow (Sankey). Each has tooltips, a data table and a Download PNG button.

## V1 – first page
The landscape map (five layers, every tool as a tile, crawlable without JavaScript), filters (layer, category, pricing, quick
picks, Canada, how it runs, status), search, a list view with sorting, the tool detail drawer, side-by-side compare of up to three
tools, the cost-per-output calculator, the map PNG export, the "AI" menu dropdown, the FAQ and the retired-tools list.
