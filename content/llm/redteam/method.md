# Red-team review B: LLM leaderboard refresh (data as of 2026-11-17, release V5.45)

Reviewed on 2026-11-17. I did not build this refresh.

**Files reviewed:** content/llm/{catalog.py, match.py, build_dataset.py, SPEC.md, llm.json, llm.prev.json, raw/*}, content/gen/llm_page.py, assets/js/llm.js, assets/js/llm-studio.js, llm-leaderboard.html.

**What I ran.**
- Copied the repo to /home/claude/llmrefresh2/rtb/site/ and re-ran build_dataset.py there. The output is byte-identical to the repo's llm.json, and the JSON embedded in llm-leaderboard.html equals llm.json.
- `match()` over every `model_as_listed` on every board (4,415 rows from arena, arena_full, index and agentic, including the token, time and speed boards) plus vendor.scores.json (644), vendor.models.json (129), index.models.json (125) and arena.models.json (184). Scripts: /home/claude/llmrefresh2/rtb/scripts/names2.py, dep.py.
- Re-derived every agent card's top five, every board's top five, the blended-price frontier and the cost-per-task frontier (each `alt` setting as its own point, as llm.js does) from llm.json and llm.prev.json (scripts/derive.py, ties.py).
- Loaded the page from `python3 -m http.server` in the copy with headless Chrome (playwright, /usr/bin/google-chrome) and drove the chart studio (scripts/page.py). Screenshots: /home/claude/llmrefresh2/rtb/shots/.
- Proposed fixes 1 and 4 were tested in a scratch copy, /home/claude/llmrefresh2/rtb/fix/.

**Where I edited.** No repo files. build_dataset.py was not run in the repo.

Severity: **B** = blocker, **S** = should-fix, **m** = minor.

---

## A. Name matching

### 1. Name matching for GPT-6.2 Astra and GPT-6.2 Sol: correct
- **gpt-6-2-astra matched 41 rows:** ARC-AGI-1, ARC-AGI-2, ARC-AGI-3 Standard and Provider Adapter (5 efforts each); AA Index and AA output tokens (5 each); Epoch ECI, FrontierMath T1-3, FrontierMath T4 and GPQA (1 each, `gpt-6.2-astra_max` / "GPT-6.2 Astra"); Vals (`openai/gpt-6.2-astra`).
- **gpt-6-2-sol matched 31 rows:** the same four ARC boards, AA Index and tokens (5 each), and Vals. Sol has no Epoch rows, which is correct.
- **Vendor records:** "GPT-6.2 Astra", "OpenAI: GPT-6.2 Astra", "GPT-6.2 Sol" and "OpenAI: GPT-6.2 Sol" match. "OpenAI: GPT-6.2 Astra Pro" and "OpenAI: GPT-6.2 Sol Pro" return None, because "pro" is not a SETTING word.
- **gpt-6.2-astra-law:** it appears only inside the price_notes of the "GPT-6.2 Astra" vendor record and in vendor.notes.md. It is never a `model_as_listed`, so nothing can merge it.
- **Kept apart, as they should be:**
  - "GPT-6 Astra …" and `gpt-6-astra_*` go to gpt-6-astra. "6 astra" does not prefix-match "6 2 astra".
  - "GPT-6.1 Sol …" goes to gpt-6-1-sol.
  - "GPT-6 Sol", "GPT 6 Sol (Max)", `gpt-6-sol_max` and `openai/gpt-6-sol` are unmatched (not in the catalogue).
  - All GPT-5.6 Sol spellings are unmatched.
  - "Claude Opus 5.5 Max + GPT-6 Luna High" is unmatched.
- **No other GPT-6.2 spelling exists in any raw file.** I checked every `model_as_listed` for "6.2", "6-2", "astra" and "sol".
- **Token rows:** both models have `tok.set == "Max"`, the same as their aa_index setting.
- No action needed.

### 2. AA-deprecated rows (taken from AA model pages): correct
- **Matched as expected:**
  - GPT-6 Astra (Low/Medium/High/Xhigh/Max) and GPT-6.1 Sol (5 settings): Index, Time per Task, Output Speed and tokens.
  - Gemini 3.8 Flash (High/Medium/Low).
  - Each has the model page as `source_url`. The Index scores and costs equal the Nov 16 values.
- **Correctly unmatched:** "Inkling Small". It is not merged into "Inkling" or "Inkling 2 Small".
- **Snapshot label:** "Qwen3.8 Max (0902)" matches with "0902 snapshot".
- No action needed.

### 3. [m] Terminal-Bench "Copilot Fusion" matches nothing, but only by luck
- **Evidence:** `match("Copilot Fusion", "Terminal-Bench 4.1")` returns (None, None) because no alias starts with "copilot". Nothing in match.py records that it is a router. Its date (Nov 17) is the only reason the Terminal-Bench card says "latest result Nov 17". The newest row for a listed model is Gemini 4 Hydrogen, Nov 12.
- **Fix (match.py):** add `"Copilot Fusion"` to `EXCLUDE` with the comment `# GitHub's model router (agentic.notes.md, 2026-11-17)`.
- **Fix (build_dataset.py, B entry "tbench", date text):** change it to `"board updated " + d("2026-11-17") + "; newest result for a listed model " + d("2026-11-12")`.

---

## B. Tier

### 4. [S] Is "Frontier" right for GPT-6.2 Sol? Reported, not decided
- **Where the definitions are:** SPEC.md has no tier definitions. They are in the catalog.py docstring:
  - Frontier = "the developer's most capable generally offered model(s)".
  - Mid-size = "a cheaper general model one step down".
- **Against Frontier:**
  - GPT-6.2 Astra beats Sol on every shared board: AA 62.1 vs 57.3, Vals 67.7 vs 66.1, ARC-AGI-2 95.8 vs 85.8.
  - Sol costs a quarter as much ($2/$10 vs $8/$40).
  - OpenAI calls Sol "Our go-to model for everyday work, from coding to powering agents at scale" and calls Astra "Our most capable model". The vendor note on GPT-6.1 Sol says "GPT-6.2 Sol is now the recommended balance model".
  - **The same price point gets a different tier at another developer.** Claude Sonnet 5.5 ($2/$10, a quarter of Fable 5.2's price) is Mid-size. GPT-6.2 Sol ($2/$10, a quarter of Astra's price) is Frontier.
- **For Frontier:**
  - Precedent: GPT-6.1 Sol is Frontier.
  - OpenAI's "Flagship models" list includes 6.2 Sol. It also lists 6.1 Terra and 6 Luna, though, so that list does not settle the tier.
  - "model(s)" allows more than one Frontier model, as with Gemini 4 Carbon and Argon.
- **Superseded models still show the Frontier chip.** GPT-6 Astra, GPT-6.1 Sol and Qwen3.8-Max now all carry "Frontier" in the table and in the filter. Only the expandable notes say "Superseded". Board news says they "are marked superseded", but only the details panel marks them. Last review's finding 8 (a "Previous flagship" tier, or a note in the filter hint) was not done.
- **Options for the owner:**
  - (a) Keep both Sols as Frontier. Reword the Frontier definition in catalog.py to "the developer's flagship line (OpenAI lists two flagship sizes)", and say in the filter hint (llm_page.py, `gr-hint`) that OpenAI's Sol is grouped with Astra.
  - (b) Move gpt-6-2-sol and gpt-6-1-sol to Mid-size, in line with Sonnet. Terra then sits under them as a second Mid-size model.
  - Either way: set `status` for gpt-6-astra, gpt-6-1-sol and qwen3-8-max to "Superseded (still offered)" in build_dataset.py, for example `STATUS = {...}` applied after PRICE_FIX, so the Status row shows it. Otherwise change the board-news wording to "their details note they are superseded".

---

## C. Rankings and frontiers (re-derived, Nov 16 to Nov 17)

### 5. Every ranking and frontier change is explained by new data
- **Agent cards (main board top five):**
  - Only "Documents and data analysis" changed (lb_data). Qwen4-Max is now #3 (83.4, X-high). Hydrogen moves to #4, GPT-6 Astra to #5, and GPT-6.1 Sol drops out. Cause: LiveBench added Qwen4-Max in place on Nov 16 (index.notes.md).
  - All nine leaders are unchanged, so "The leader of every agent card is unchanged" is correct.
  - **Hard reasoning (FrontierMath):** GPT-6.2 Astra enters at #4 (92.6%), and Opus 5.5 moves to #5. This needs finding 6.
- **Board top fives:**

  | Board | Change |
  |---|---|
  | aa_index | GPT-6.2 Astra #2 (62.14 Max), GPT-6.2 Sol #5 (57.26 Max); GPT-6 Astra and GPT-6.1 Sol drop out |
  | eci | GPT-6.2 Astra #1 (174.17). Live-CSV re-estimates: Fable 173.44→173.50, Carbon 169.76→169.78, GPT-6 Astra 169.0→169.2, Opus 168.54→168.7 |
  | gpqa | GPT-6.2 Astra #1 (96.84); GPT-6.1 Sol drops out |
  | arc2 | GPT-6.2 Astra #1 (95.83, X-high); Opus 5.5 drops out |
  | frontiermath | GPT-6.2 Astra #4 |
  | lb_data | as above |

  All of these are new rows recorded in index.notes.md and agentic.notes.md.
- **Cost-per-task frontiers:**
  - aa_index: added GPT-6.2 Astra High/X-high/Max and GPT-6.2 Sol Max. Removed Fable High/Medium, GPT-6 Astra High/X-high, GPT-6.1 Sol Max and Carbon High/Medium. All are dominated by the new points.
  - vals: GPT-6.2 Sol Max ($3.18, 66.06) replaces GPT-6.1 Sol Max.
  - arc2: GPT-6.2 Astra High and X-high replace GPT-6 Astra Max.
  - lb_browser, lb_long and lb_data: Qwen4-Max added (lb_data replaces GPT-6.1 Sol).
- **Blended-price frontiers:**
  - eci: GPT-6.2 Astra replaces Fable 5.2 at $16; the other points only re-estimate.
  - gpqa and arc2: GPT-6.2 Astra added (arc2 replaces GPT-6 Astra).
  - aa_coding: Gemini 4 Hydrogen added (new AA Coding pair, Antigravity CLI X-high, 52.3).
  - lb_data: Qwen4-Max replaces Hydrogen.
  - arena_text, eci and gpqa: the gpt-oss-20b point moved from $0.131 to $0.036, and Granite 4.2 8B left the Arena Text frontier. See finding 9.
- **Results count:** 515 → 530 (+9 GPT-6.2, +5 Qwen4-Max LiveBench, +1 Hydrogen AA Coding). This matches the "What changed" text.

### 6. [B] GPT-6.2 Astra's Epoch results are pre-launch but are not flagged; Fable 5.2's are
- **Evidence:**
  - index.scores.json `gpt-6.2-astra_max` FrontierMath and GPQA notes say: "Run started 2026-10-27…, before the model release date (pre-launch testing)". ECI is built from those runs.
  - build_dataset.py sets `rec["flag"]` only when `mid == "claude-fable-5-2"`.
  - **On the page:** the Hard reasoning card shows "Claude Fable 5.2 pre-launch" at #1, but "GPT-6.2 Astra" at #4 has no flag. The table rows on ECI and GPQA, where Astra is the new #1, carry no "Pre-launch result" tag. The flag exists only in the model's notes text.
  - Board news says "GPT-6.2 Astra is the new top at 174.2" without the caveat.
- **Fix (build_dataset.py):**
  - Add `PRELAUNCH = {"claude-fable-5-2", "gpt-6-2-astra"}  # Epoch runs started before release` and use `if bid in EPOCH and mid in PRELAUNCH:`.
  - In BOARD_NEWS[3], change "…GPT-6.2 Astra is the new top at 174.2." to "…GPT-6.2 Astra is the new top at 174.2, from Epoch's pre-launch testing."
- **Tested in scratch:** only the eci, frontiermath and gpqa records of GPT-6.2 Astra gain the flag. Nothing else changes.

### 7. [S] FrontierMath and GPQA say "results as of Nov 6, 2026", but their newest results were published Nov 17
- **Evidence:**
  - The date text is the newest `result_date`, and for Epoch that is the run start date. GPT-6.2 Astra's runs started Oct 27, so the label stayed at Nov 6.
  - The rows were not in the Nov 16 snapshot. They came from today's benchmark_data.zip, and ECI says "hub updated Nov 17".
  - Readers will take "results as of Nov 6" to mean nothing newer is included.
- **Fix (build_dataset.py, B entries "frontiermath" and "gpqa", last field):** replace `None` with `"Epoch data retrieved " + d("2026-11-17") + "; newest run started " + d("2026-11-06")`.

### 8. [S] ARC-AGI-2: GPT-6.2 Astra "X-high" (and Sol "High") is chosen by a rounding accident, not a rule
- **Evidence:**
  - ARC lists Astra Max and XHigh at the same 0.958333 ($0.9695 vs $0.4996). It lists Sol Max, XHigh and High at the same 0.858333.
  - build_dataset.py compares the unrounded `v` with the rounded `best["v"]` (`round(v, 3)`). 95.83333 > 95.833, so the **last** tied row in raw order wins.
  - ARC lists efforts Max-first, so the cheapest tied setting happens to win. With a strict comparison, Max would be shown (tested: Astra arc2 Max, Sol arc2 Max).
  - No model in llm.prev.json had a tie, so there is no earlier rule to be consistent with. The method text says only "ranked on its best setting".
  - The same bug lets a later row that is up to 0.0005 lower beat an earlier one.
- **Effect:** the score, rank and frontier membership are unaffected, because `alt` has every point. Only the setting label and cost shown with the best result change.
- **Fix (build_dataset.py board loop):** keep `_raw=v` in `rec`, compare against `best["_raw"]`, and break ties on cost:
  ```python
  if best is None or (v > best["_raw"] if hb else v < best["_raw"]) or \
          (v == best["_raw"] and rec["cost"] is not None and (best["cost"] is None or rec["cost"] < best["cost"])):
      best = rec  # equal scores: the cheaper setting is shown
  ...
  best.pop("_raw"); M[mid]["s"][bid] = best
  ```
  - Add to STEPS[2]: "If two settings score the same, the cheaper one is shown."
  - Tested in scratch: the output is identical to the current llm.json (Astra X-high, Sol High), now by rule.

---

## D. "What changed" and board news

### 9. [S] Changes not mentioned that move a card or a frontier
- **LiveBench added Qwen4-Max (Nov 16 in-place update).** This changes the Documents-and-data card's top five and three cost frontiers. Board news is silent, and its first line says "not yet on … LiveBench" about GPT-6.2 only.
  - **Add:** "LiveBench added Qwen4-Max to its Nov 6 release on Nov 16; it is #3 on LiveBench Data Analysis."
- **AA Coding Agent Index added Gemini 4 Hydrogen (Antigravity CLI, X-high, 52.3%).** It now sits on that board's blended-price frontier.
  - **Add:** "Artificial Analysis added Gemini 4 Hydrogen to its Coding Agent Index (52.3%)."
- **gpt-oss-20b's list price moved from $0.075/$0.30 to $0.018/$0.09** because OpenRouter's default endpoint changed. The new price matches Darkbloom (fp8) and AkashML (fp4) (/tmp/vw2/orp/openai_gpt-oss-20b.json). This moves the gpt-oss-20b point on three blended frontiers, and Granite 4.2 8B leaves the Arena Text frontier.
  - It also breaks the rule used for Granite (PRICE_FIX: "lowest full-precision host"). The lowest bf16 endpoint is DeepInfra, $0.024 / $0.112.
  - **Fix (build_dataset.py PRICE_FIX):** add `"gpt-oss-20b": dict(pin=0.024, pout=0.112, pprov="DeepInfra (bf16) via OpenRouter (lowest full-precision host listed); secondary source", purl=OR_EP.format("openai/gpt-oss-20b"))`, after the owner confirms gpt-oss's native precision. Frontier membership is unchanged at that price; I checked Arena Text, where Granite stays off.
  - Muse Glimmer 30B ($0.30/$1.20 → $0.35/$1.50) and Nemotron 3 Ultra ($0.60/$2.40 → $0.50/$2.20) also moved for the same reason. Nemotron 3 Ultra's "maximum output" fell from 182,520 to 16,384, OpenRouter's top-provider value, which is not a model spec.
  - **Fix:** one board-news line: "Open-weight list prices follow OpenRouter's default host, which changed for gpt-oss-20b, Muse Glimmer 30B and Nemotron 3 Ultra." Also drop the OpenRouter maxout for nemotron-3-ultra (set `maxout=None` via PRICE_FIX-style override).

### 10. [m] Board news wording
- **Line 1:** "Early results: on Artificial Analysis, Vals, ARC-AGI and Epoch AI so far". Epoch has only Astra; Sol is not on Epoch. Neither model is on the AA Coding Agent Index, which a reader may count as "Artificial Analysis".
  - **Change to:** "Both are on the Artificial Analysis Intelligence Index, Vals and ARC-AGI; GPT-6.2 Astra also on Epoch AI (pre-launch runs). Neither is yet on the AA Coding Agent Index, Arena, LiveBench, Terminal-Bench or Vending-Bench."
  - "Early results" itself is fair. The model notes say the same.
- **Line 5:** "Arena has not published since Nov 16".
  - arena.notes.md: the dataset was last modified 2026-11-16T04:02Z, and its newest board date is **Nov 15**. The live arena.ai pages returned 403, so they were not checked.
  - **Change to:** "Arena's published dataset has not changed since Nov 16 (newest board Nov 15)."
- **Line 2:** "20% less" is correct ($8/$40 vs $10/$50).
- **Line 3:** the deprecated list is correct. Inkling Small is also deprecated on AA, but it is not in the catalogue.
- **"New leaders on the agent cards":** correct ("unchanged"). It is not misleading, because no card leader moved. `COMPOSITION_CHANGED` is empty, which is right for Nov 16 → Nov 17.

### 11. [m] The ARC-AGI-2 caveat does not mention "partial dataset coverage"
- 29 ARC-AGI-2 rows carry ARC's note "Partial dataset coverage: scores use full catalog denominators; costs include recorded usage only". They include GPT-6.2 Sol Max and Medium, Opus 5.5 Max, Fable 5.2 Max, and Carbon and Argon. Their costs are lower bounds.
- **Fix (build_dataset.py, B entry "arc2", caveat):** append " ARC Prize marks some runs as partial coverage: unattempted tasks count as failures and the cost covers recorded usage only."

---

## E. Page (headless Chrome)

### 12. Page loads cleanly; counts correct; effort curves render without overlaps
- **Console:** no console messages, page errors, failed requests or HTTP ≥ 400.
- **Hero:** 55 models | 19 benchmarks | 29 open-weight | November 17, 2026. These match llm.json.
- **Explorer:** "47 models · 8 more match but have no result" (aa_index n = 47).
- **Effort curves:** I checked every SVG text bounding box pairwise and against the 5-px markers. There were no overlaps and no labels on markers in any of these views:
  - AA Index vs cost with defaults + GPT-6.2 Astra + GPT-6.2 Sol, linear and log
  - AA vs output tokens
  - AA vs time
  - ARC-AGI-2 vs cost: defaults (GPT-6.2 Astra, GPT-6 Astra, GPT-6.1 Sol, Gemini 4 Carbon) + GPT-6.2 Sol, linear and log
- **Screenshots:** shots/curve_aa_index_cost_0_only.png and curve_arc2_cost_0.png.
- **GPT-6.2 Sol on AA vs cost:** one "Max" dot at $1.01, with no line.
- **GPT-6.2 Astra and Sol on "time per task":** not offered in the picker, because AA has no time data for them. Correct.

### 13. [m] Effort-curve note says "one dot means one published setting", but AA publishes five settings for GPT-6.2 Sol and costs only at Max
- **Fix (assets/js/llm-studio.js, drawCurves note):** when any selected model has AA points with `cost == null` on the cost axis, append " Settings without a published cost (for example GPT-6.2 Sol below Max) are not plotted; switch to output tokens to see them." The tokens view already shows all five Sol settings.

### 14. [m] Legend overflows with six long names (existing issue)
- AA vs cost with six models (Hydrogen, Sonnet 5.5, Terra, GPT-6 Astra, GPT-6.1 Sol, Fable 5.2) puts "Claude Fable 5.2" past the 860-px viewBox. The cause is that `lx += 40 + name.length * 7.4` never wraps. It does not happen with the GPT-6.2 additions (five series fit).
- **Fix (llm-studio.js):** when `lx + 40 + name.length * 7.4 > W - mr`, start a second legend row (y = 34) and raise `mt` by 18.

---

## Summary of fixes by file
- **build_dataset.py:**
  - PRELAUNCH flag for gpt-6-2-astra (6)
  - Epoch date text (7)
  - tie rule with `_raw` (8)
  - BOARD_NEWS lines 1, 4 and 5 plus the LiveBench / AA Coding / open-weight price lines (6, 9, 10)
  - gpt-oss-20b PRICE_FIX and the nemotron-3-ultra maxout (9)
  - arc2 caveat (11)
  - tbench date text (3)
  - superseded `status` (4)
- **match.py:** EXCLUDE "Copilot Fusion" (3).
- **catalog.py / llm_page.py:** tier decision for GPT-6.2 Sol and GPT-6.1 Sol, and the definition or hint text (4).
- **llm-studio.js:** effort-curve note (13) and legend wrap (14).
