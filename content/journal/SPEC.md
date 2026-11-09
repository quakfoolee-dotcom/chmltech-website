# Chmltech Online Journal paper spec (V4.12)

One JSON file per paper: `journal/<slug>.json`. Must pass `python3 -I journal/validate.py journal/<slug>.json`.

## Fields
- `slug` (string, unchanged from the existing URL)
- `volume` (int), `issue` (int), `published` (YYYY-MM-DD, keep original), `revised` ("2026-11-09")
- `title` (the paper's real title, not "Chmltech Online Journal, Volume…"), `short_title` (<= 60 chars, for cards)
- `meta` (120-170 chars, plain text)
- `author`: {"name": "Quak Foo Lee", "role": "Chief Technology Officer", "org": "Chmltech Ltd.", "division": "<as in original>", "location": "Burnaby, BC, Canada"}
- `abstract` (150-250 words, one paragraph, structured as background, scope, main points, conclusion)
- `keywords` (5-8)
- `sections`: list of {"num": "1", "title": "...", "blocks": [...]} — numbered 1..n; typically Introduction … Conclusion
- `references`: list of {"text": "Author, A., & Author, B. (Year). Title. Journal, vol(issue), pages.", "url": "https://doi.org/... or https://arxiv.org/abs/..."}; 12-30 entries
- `corrections`: list of strings (NOT rendered) — every technical error in the original and how it was fixed
- `figures_note` optional string (not rendered)

## Blocks (inside sections)
- {"p": "text with inline citations like [1] or [2, 5]"}
- {"h3": "1.1 Subsection title"}  (numbered "<sec>.<n> Title")
- {"eq": "η<sub>V</sub> = E<sub>rev</sub> / V<sub>cell</sub>", "n": 1}  equations numbered 1..n across the paper; refer to them as "Eq. (1)"
- {"list": ["...", "..."], "ordered": false}
- {"table": {"n": 1, "caption": "...", "head": ["...", "..."], "rows": [["...", "..."]], "note": "Source: [3], [7]."}}  tables numbered 1..n, cited in text as "Table 1"
- {"callout": "Key point or practical implication (1-3 sentences)"}  max 3 per paper

Allowed inline HTML in any text: <sub> <sup> <em> <strong> <i> <b>. No other HTML. Use Unicode for symbols (η, Δ, →, ⇌, ≈, ×, °C, wt%).

## Writing rules
- Formal academic register, third person, Canadian/American spelling consistent (use American "-ize").
- 3,000-4,500 words of body text. Keep the original paper's scope and structure, expand with depth, correct errors.
- Every factual or numerical claim from literature is cited. Every reference must be REAL and verified (found via search/DOI/arXiv) — never invent authors, titles, volumes or DOIs. If you cannot verify a source, do not use it.
- Cite each reference at least once; number references in order of first citation.
- No marketing language, no "guaranteed", no claims about Chmltech clients. No "As an AI".
- Numbers must be physically/technically correct (check thermodynamics, units, stoichiometry).
