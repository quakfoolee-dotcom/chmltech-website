# Journal figures — how to add them (V4.15 conventions)

Pilot to copy: `capex.py` (draws figures) and `place_capex.py` (puts them into the paper JSON). Look at both first.

## Drawing
- Write `jfigs/<name>.py`. Import `from style import *` (palette NAVY, BLUE, BRIGHT, GREEN, GREEN_D, ORANGE, GREY, LIGHT, SERIES; rcParams preset) and save each figure with `save(fig, SLUG, "figN-short-id")`. It writes `journal/figures/<slug>/<id>.svg`.
- Plots: use matplotlib. Diagrams (architectures, flows, topologies): matplotlib patches/annotations (FancyBboxPatch, FancyArrowPatch) on an axis with `ax.axis("off")` work well; keep the same palette and fonts. Navy text on light fills; avoid pure black.
- Typical size: figsize ≈ (6.6–9.2, 3.5–4.6). Text ≥ 9 pt. Use mathtext for subscripts (r"$\Delta T_{\min}$").
- Numbers in a plot must come from the paper (its equations, tables or worked examples) or from a cited source. If a plot is only qualitative, label axes "relative units", hide numeric ticks and say "schematic" in the caption.
- Diagrams that follow a published figure: redraw in our own style and credit "Adapted from [n]". Never copy a figure.
- Run with: `cd jfigs && python3 -I -c "import sys; sys.path.insert(0,'.'); exec(open('<name>.py').read())"`

## Placing
- Write `jfigs/place_<name>.py` using `insert.apply(path, specs)` (see place_capex.py). Each spec: `sec` (section num string), `after` (block index in the paper WITHOUT figures, i.e. as currently listed with figures removed), `ref` = (section, block index of a paragraph) that receives `sentence`, and `fig` = {n, id, caption, alt, source}. It is idempotent (removes old figures, adds each sentence once).
- The sentence must contain "Figure N" and say what the reader should notice. Captions: one or two sentences, may use <sub>/<sup>/<em>. Alt text: describe what the figure shows, 40+ characters. Source: e.g. "Drawn by the author from Table 2.", "Author's calculation from Eq. (4).", "Adapted from [12]." — citation numbers must match the paper's reference list.
- To list block indices: print each section's blocks with their index after removing existing "fig" blocks.
- Then run `python3 -I journal/validate.py journal/<slug>.json` — it must print OK (figures numbered 1..n, each referenced in text, alt text present, svg file exists, body words ≤ 4800).

## Visual check (required)
Render every SVG in a white page at 780 px and at 540 px wide with Playwright (chromium is preinstalled; require('playwright')), screenshot, and LOOK at each image with the Read tool. Fix any overlapping or clipped labels, legends covering data, or unreadable text before finishing.
