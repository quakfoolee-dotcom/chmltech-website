# Red-team review: LLM leaderboard method, matching and page text

Reviewed on 2026-11-12. Files: content/llm/{llm.json, build_dataset.py, catalog.py, match.py, raw/*}, content/gen/llm_page.py and assets/js/llm.js.
Method: I ran `match()` over every `model_as_listed` on the 19 boards in use. I re-derived the frontiers from llm.json. I checked each board description against raw/*.notes.md. I made 3 live checks: the Mistral docs page `docs.mistral.ai/models/mistral-large-4-0.md`, the HF API and README for `mistralai/Mistral-Large-4-1T-A52B`, and cohere.com/pricing. I edited no repo files. I did not run build_dataset.py, because it overwrites llm.json.

Severity: **B** = blocker, **S** = should-fix, **m** = minor.

---

## A. Name matching

### 1. [B] Terminal-Bench misses its #1 and #2 rows (Opus 5.5, Sonnet 5.5)
- Evidence: raw/agentic.scores.json, Terminal-Bench 4.1. Rank 1 is "Opus 5.5" (Anthropic, Claude Code, max, 65.76%, total cost $4,718.65 over 330 trials). Rank 2 is "Sonnet 5.5" (63.94%, $7,333.64). `match()` returns (None, None) for both because the catalogue aliases all begin with "Claude".
- Effect: llm.json shows GPT-6.1 Sol as #1 on Terminal-Bench (n = 9 instead of 11). The Coding agents card's "Also see: Terminal-Bench" and the Terminal-Bench frontier are both wrong. Opus 5.5 would sit at the top of the frontier at $14.30 per trial.
- Fix (catalog.py):
  - Add `"Opus 5.5"` to claude-opus-5-5's aliases.
  - Add `"Sonnet 5.5"` to claude-sonnet-5-5's aliases.
  - Also add `"Haiku 5.5"`, `"Fable 5.2"` and `"Mythos 5.2"` to their entries, for future rows.

### 2. [B] "Muse Wonder Full" (not on the API) is merged into "Muse Wonder" (API, $4/$20)
- Evidence that it is a separate product: raw/vendor.models.json, record "Muse Wonder", notes: *"Higher-capability 'Muse Wonder Full' only in Muse Code (not API)."* The two have different scores on every board:

  | Board | Muse Wonder Full | Muse Wonder |
  |---|---|---|
  | AA Index | 50.08 (no cost) | 43.57 ($6.95) |
  | Vals | 66.79 ($6.81, meta/muse-wonder-full) | 64.88 ($10.65) |
  | AA Coding | 0.5888 (no cost) | 0.5198 ($8.05) |
  | WebDev | 1723.4 | 1648.6 |
  | Arena Agent | 0.0909 | 0.0193 |
  | Vending | $12,292 (no cost) | $9,432 ($329) |

- Effect in llm.json: muse-wonder carries the Full score on aa_index, vals, aa_coding, arena_webdev, arena_agent and vending, all under the API price.
  - On the Vals cost-per-task chart, Muse Wonder is a frontier point at $6.81 / 66.79. Nobody can buy that model at that price.
  - On AA Index, AA Coding and Vending it drops off the cost-per-task chart, because the Full row has no cost.
- The cause is twofold:
  - catalog.py lists "Muse Wonder Full" as an alias.
  - match.SETTING contains "full", so it would merge even without the alias.
- Fix:
  - Remove "Muse Wonder Full" from the aliases.
  - Remove "full" from SETTING.
  - Then either add a separate entry (id muse-wonder-full, access "Muse Code only (no API)", no price) or leave those rows unmatched and list them in the notes.

### 3. [B] Mistral Large 4 Preview is merged with Mistral Large 4 (GA)
- Evidence:
  - In the Epoch rows, `mistral-large-4-0_high` has the display name **"Mistral Large 4 Preview (high)"**, released 2026-10-06.
  - `mistral-large-4-0-oss_high` has the display name "Mistral Large 4 (high)", released 2026-10-29.
  - catalog.py has the alias `"mistral-large-4-0"`, so the Preview's FrontierMath 58.6 and GPQA 88.07 are published as Mistral Large 4. The GA GPQA result (90.15) goes **unmatched**.
  - Vals `mistralai/mistral-large-4-oss` (56.53, $3.72) is also unmatched, so the GA model is missing from Vals.
  - LiveBench has two different entries:
    - "Mistral Large 4 1029" (id mistral-large-4-0): coding 79.4, browser 17.4, research 80.3.
    - "Mistral Large 4" (id mistral-large-4): coding 44.4, browser 0.6, research 30.8.
    - The matcher drops the "1029" token (4-digit rule) and takes the better of the two. Which LiveBench id is the GA model is unresolved: "1029" matches the AA/Epoch GA date, but Epoch uses `-0` for the Preview.
  - The Mistral docs list both `mistral-large-4` and `mistral-large-4-0` as GA API names. So the "-0" id means different things on different boards.
- Fix:
  - Remove alias `mistral-large-4-0`.
  - Add `mistral-large-4-0-oss` and `mistral-large-4-oss`.
  - Add "Mistral Large 4 Preview" to an exclude list.
  - For LiveBench, map only the entry whose release in LiveBench's model map equals 2026-10-29. If that cannot be confirmed, publish neither.

### 4. [S] Snapshot dates are swallowed, so different snapshots are mixed on one card
- Cause: `match.ok_rest` accepts any token of 4 or more digits, and `rest` then deletes it. The snapshot never shows up in `set`.
- Qwen3.8 Max: Epoch gives the base model a release date of 2026-08-02 and "Qwen3.8 Max (0902)" 2026-09-01, so they are separate snapshots. In llm.json:
  - arena_webdev uses 0902 (1675.8; the base model scores 1670.3).
  - frontiermath and gpqa use the base model (74.7 against 0902's 65.6).
  - aa_index and tbench have only 0902.
  - So one card mixes two snapshots without saying so.
- DeepSeek V4.1 Flash: the price, specs and release date (2026-10-17) are for **1017**. But:
  - arena_text and arena_vision come only from **DeepSeek-V4.1-Flash-20260910**, the September snapshot.
  - aa_coding uses "Codex - DeepSeek V4.1 Flash (Max)", the older snapshot (0.473), over the 1017 row (0.463).
  - ARC, LiveBench and Vals use 1017.
- Fix:
  - Keep date tokens in the setting label, e.g. "Max, 0902 snapshot".
  - Prefer rows whose snapshot matches the vendor's current API version.
  - Rows from an older snapshot should either be dropped or carry a visible "earlier snapshot" label.
  - Add a per-entry `snapshots` allow-list, e.g. deepseek-v4-1-flash: ["1017", "20261017", None].

### 5. [S] Other misses
- Vectara `amazon/nova-2-lite-v1:0` is unmatched, so Nova 2 Lite has **no results at all**. Fix: add the alias `nova-2-lite-v1:0`.
- Vals `baseten/nemotron-3.5-super-vl-120b-a12b` (hosted) is unmatched, while `kimi-k3.1-pro-together` (hosted) is matched by an explicit alias. Fix: make the hosted-endpoint policy consistent (see 6).
- These are correctly unmatched: "Hy4 preview", "tencent/hy4-preview", "alibaba/qwen3.8-max-internal", "Inkling 2 Small", "Mistral Large 4 Preview" on ECI, and the dual-model AA Coding rows ("Claude Opus 5.5 Max + GPT-6 Luna High", "GPT-6 Astra XHigh + SWE-2 Medium").

### 6. [S] The policy on quantized and hosted builds is inconsistent
- "bf16" merges: it splits to "bf" + "16", both allowed. "fp8" and "nvfp4" never merge: they split to "fp" / "nvfp" + digit, and neither "fp" nor "nvfp" is in SETTING. So the "fp8" and "fp4" entries in SETTING are dead code.
- Kimi's Epoch FrontierMath and GPQA rows are **Together-hosted** runs ("Kimi K3.1 Pro (Together, max)"). The page shows them as Kimi K3.1 Pro with no host label.
- Fix:
  - Write down one rule. Suggested: accept the BF16 reference and named hosts, put the host in `set` ("Max, via Together"), and exclude NVFP4/FP8/FP4 quantizations.
  - Implement the rule as an explicit token list rather than by accident.

### 7. [m] Bug in the match.py prefix regex
- `lambda m: "" if m.group(1) in PREFIX or True else ...` removes **any** prefix before "/" or ":". `PREFIX` is never used.
- It is harmless today (baseten/ and fireworks/ are stripped), but it will strip real name parts that contain ":".
- Fix: remove `or True`, and add the hosts you want stripped (baseten, together, fireworks) to PREFIX.

---

## B. Specs, prices, access, tiers

### 8. [m] Mistral Large 4 access and licence are correct; one note needed
- Confirmed on 2026-11-12:
  - docs.mistral.ai: "Type: Open", "Licenses: Mistral Ecosystem Open Weight License", release date 2026-11-05.
  - HF card: `license: other`. The README says the licence is *"a modified version of the MIT license, for both commercial and non-commercial use — operating a Model-as-a-Service business requires a separate commercial license with Mistral."*
- "Open weights" is right. The other sources differ only in wording: Arena says "Modified MIT", Epoch says "restricted use".
- Fix:
  - Add to notes: "Hosting as a paid service needs a Mistral commercial licence."
  - Note that the release date is 2026-11-05 on the vendor page but 2026-10-29 on AA and Epoch. The HF repo was created 2026-09-30.

### 9. [m] Command A+ price confirmed
- cohere.com/pricing (fetched 2026-11-12): the `pricingRows` inside the Command A+ card are "Input $2.50 / 1M" and "Output $10.00 / 1M", ahead of the next card (Command R7B). So the adjacency doubt in vendor.notes.md is resolved.
- OpenRouter's Cohere endpoint lists $0.30/$1.50. Keep that as a price note.

### 10. [S] Introductory and time-limited prices drive the frontier
- Gemini 4 Carbon and Argon cost $2/$10 only until 2026-11-30, then $4/$20. Gemini 3.8 Flash costs $0.75/$3.75 until 2026-12-31.
- Gemini 4 Carbon is a frontier point on aa_index, aa_coding and lb_coding by blended price. The note is in `m.notes`, but neither the chart tooltip nor the frontier table shows it.
- Fix: add an `intro_until` field to the model record. Show "introductory price until Nov 30" in the tooltip and frontier table, or plot the post-intro price.

### 11. [S] Price provenance is described wrongly on the page
- llm_page.py says the price comes "from the developer's own price list (or, for open-weight models, a named host)".
- Hy4 is **Proprietary API** but priced from an OpenRouter endpoint listing (secondary). Step 5 Preview and MiMo-V2.6-Pro also use OpenRouter endpoint data.
- Fix: say "or, where the developer publishes no price list we could read, the price its own endpoint lists on OpenRouter". Show "secondary" in the detail panel.

### 12. [m] Release dates
- OpenAI, xAI and Google dates come from AA (secondary). They carry the note "Release date as listed by Artificial Analysis", which is good.
- Two AA dates look wrong:
  - Qwen3.8 Max (2026-08-03) is taken from AA's **0902** record, but Epoch dates 0902 to 2026-09-01.
  - Beam (2026-10-16 on AA) is 2026-10-05 on Epoch.
- Fix: when AA and Epoch disagree by more than 3 days, show the month only, or both dates.

### 13. [m] Missing licence and tier oddities
- Muse Spark Open: the licence shows nothing, but the vendor note gives the gated licence "muse-model-license". Show "muse-model-license (gated; terms not read)".
- Grok Build 0.1 (alias grok-code-fast-1) is a coding-specialist model but is tiered "Mid-size" as a general model. Note that it is a coding model.
- DeepSeek V4.1 Flash is "Mid-size" yet beats V4 Pro (Frontier) on Vals (61.3 vs 53.0), FrontierMath and Vending. That is defensible as its place in the line-up, but the tier chip reads like a capability label. Add the tier definition to the filter tooltip.

---

## C. Method

### 14. [S] The best-scoring row can lack a cost, so the model vanishes from the cost-per-task chart
- Muse Wonder on aa_index, aa_coding and vending: the chosen (Full) row has no cost, while other matched rows do. This goes away once 2 is fixed, but the rule stays fragile.
- Fix: for benchmarks with cost mode set, store `cost_row` = the best-scoring row **with** a cost, used only by the task-cost chart. Or plot each costed setting as its own point (see 15).

### 15. [S] "Best setting per model" biases the Pareto chart against cheaper settings
- On the cost-per-task axis, the cost does belong to the plotted variant, which is consistent. But only the highest-scoring setting is plotted, so a model's cheaper effort levels can never appear on the frontier.
- Example, GPT-6 Astra on Terminal-Bench:
  - Max: 60.3%, $9.90
  - High: 60.0%, $6.88
  - Low: 50.9%, $4.72
- On the price-per-token axes, a "Max" score is set against a per-token price that ignores how many tokens Max uses.
- Fix: in task-cost mode, plot every (model, setting) point and draw the frontier over those. Add to the chart note: "Per-token price ignores how many tokens each setting uses."

### 16. [S] Derived costs are labelled "as published by the benchmark"
- llm.js XLABEL.task reads "Cost per task, US$ (as published by the benchmark)". For LiveBench and Terminal-Bench the figure is computed in build_dataset.py.
- For Terminal-Bench it is per **trial** (330 trials), not per task. The AA notes say Terminal-Bench v4 has 66 tasks, so this is probably 5 trials per task; that is not confirmed for 4.1.
- Fix:
  - Change the axis label to "Cost per task, US$ (published, or derived from the published total)".
  - Rename the Terminal-Bench caveat to "Cost per trial (total ÷ 330 trials)".

### 17. [S] LiveBench suites are tiny single runs, yet two agent cards rank on them
- votes_or_n per suite: coding 24, browser 25, research 22, long_agentic 18, data_analysis 150. The notes say "Single run".
- The Research agents card's top 3 (94.5 / 93.0 / 92.5) are 1–2 tasks apart.
- Fix: add "n tasks, single run" to each LiveBench caveat. Show tied ranks for gaps smaller than one task (100/n points).

### 18. [S] Rankings ignore confidence intervals
- Arena Text: Gemini 4 Carbon 1525.95 (CI 1516.4–1535.6) is #1 and Argon 1522.4 is #2, but the two overlap. Terminal-Bench, Vals, Epoch and Vending all publish CI or stderr, and llm.json keeps none of them.
- Fix: carry `score_ci` into llm.json. Show "±" in tables, and mark ranks as tied when the intervals overlap. At minimum, add to the card text: "Gaps of a few points are often within the margin of error."

### 19. [m] The frontier() algorithm is correct; one tidy-up
- Checked cases:
  - Sort by x ascending, then the better score first.
  - A point is kept only if it is strictly better than the best so far.
  - Equal x: the better one is kept. Equal y at higher x: the weakly dominated point is dropped.
  - Lower-is-better (Vectara) is handled through `better()` and the flipped Y axis.
  - Zero and negative costs are dropped by `x > 0`.
- On an exact (x, y) tie the comparator returns 1 both ways. That is harmless but non-transitive. Fix: `return p.x - r.x || (p.y === r.y ? 0 : better(...) ? -1 : 1)`.
- A Vending score below 0 (gpt-oss-120b, −$21.5) plots fine.

### 20. [S] A pre-launch result tops the reasoning card
- Fable 5.2's Epoch record is pre-launch testing that Epoch says "may change" (index.notes.md). It is FrontierMath #1 (95.09) on the "Hard reasoning" card, with no caveat.
- Fix: add a per-result note or flag ("pre-launch evaluation; may change") and show it in the card and table.

### 21. [m] "Updated" dates overstate freshness
- The aa_index, aa_coding and vending dates are the **retrieval** date, but the page shows "results as of Nov 11, 2026".
- The Terminal-Bench date is the record's updated_at, while its newest result is 2026-09-29.
- Fix: label these "retrieved Nov 11, 2026". For Terminal-Bench, show "latest result Sep 29, 2026".

### 22. Board descriptions checked against the notes
Supported by a note:
- AA "nine evaluations": the 9 components are listed in index.notes.md.
- AA Coding Agent "three evaluations: FrontierCode, SWE-Atlas QnA, Terminal-Bench v4".
- Vals: finance, legal, tax and coding, weighted by GDP share. The components are in the row notes.
- Vending-Bench "start: $500" and "mean cost per full run".
- Arena style control as the default view.
- Arena Agent as net improvement over a baseline.

Not supported by any note [S]. Cite each one or soften it:
- **ECI**: "fitted across many benchmarks so models tested on different sets can be compared". The notes only say "Bayesian model since Nov 4". Suggested: "Epoch AI's single capability score combining many benchmarks."
- **FrontierMath**: "Hundreds of … problems that take specialists hours to solve". The notes give no problem count or solve time. The scores imply a denominator of 285 (95.088% = 271/285), but that is inference. Suggested: "Unpublished, expert-written research-level maths problems, run by Epoch AI."
- **GPQA**: "written to resist web search". Not in the notes.
- **LiveBench**: "released after model training cut-offs", plus each suite's task description (browser "filling forms", data "joins", research and long-agentic wording). None of this is in index.notes.md.
- **Terminal-Bench**: "building software, configuring systems, fixing environments". The notes only say "terminal tasks".
- **ARC-AGI-2**: "easy for people". Not in the notes.
- **AA Index**: "reasoning, knowledge, coding and agentic work". The notes give the categories as Knowledge Work, Coding, Science, General. Fix: "knowledge work, coding, science and general knowledge".

---

## D. Coverage and bias

### 23. [S] Arena boards are cut to the top 60 rows although the full data is published
- The dataset's latest split holds 421 Text, 167 Vision and 156 WebDev models (arena.notes.md). Only the top 60 rows were kept, so arena_text has 16 catalogue models, arena_vision 14 and arena_webdev 28.
- The **Everyday assistant** card therefore ranks only large models. Haiku 5.5, GPT-6 Luna, Gemma 4, Nova 2 and Fable 5.2 are all absent, which reads as "not good at chat".
- Fix: re-extract every catalogue model from the latest split of `text_style_control`, `vision_style_control` and `webdev`, and drop the "top 60" caveat. If that cannot be done, switch the assistant card to aa_index (42 models) and keep Arena Text under "Also see".

### 24. [S] Agent cards show no sample size
- Ranking boards per card: Coding = aa_coding (21 models), Apps = arena_webdev (28), Browser = lb_browser (27 models, 25 tasks), Research = lb_research (27, 22 tasks), Long = vending (15), Business = vals (26), Data = lb_data (27), Assistant = arena_text (16), Reasoning = frontiermath (24).
- Fix: print "n models ranked" on each card (type_card in llm_page.py).
- Research card: "Also see: FrontierMath" is a maths test, not a research-agent test. Replace it with lb_long or drop it.
- Long-running card: consider ranking by arena_agent (29 models, real sessions) with Vending in "Also see". Vending has 15 models and contained the non-API Muse Wonder Full.

### 25. [m] The excluded boards are described correctly; two wording fixes
- Catalogue coverage of each excluded board, from matching their raw rows:

  | Board | Catalogue models | Note |
  |---|---|---|
  | SWE-bench | 0–1 | latest result Feb 2026 |
  | SWE-Bench Pro | 0–1 | latest result Jul 2026; not named in the disclaimer |
  | OSWorld-Verified and OSWorld 2.0 | 1 each | MiniMax-M3 only |
  | τ²-bench | 0 | |
  | τ³-Banking | 2 | |
  | BFCL | 0 | last updated Apr 12, 2026 |
  | METR | 0 | |
  | Aider | 1 | stale since Nov 2025 |

- Fix:
  - Say METR is "no longer updated (last update Sep 8, 2026)", not that it has "not yet published".
  - Add SWE-Bench Pro to the list.
- Boards that do cover current models but are not used, which may be worth a mention: ARC-AGI-1 (20 models), ARC-AGI-3 (12), FrontierMath Tier 4 (24), LiveBench reasoning (27).

---

## E. Page text (llm_page.py; STEPS, DISCLAIMER and GROUPS in build_dataset.py)

### 26. [S] The meta description promises a card that does not exist
"Find the best model for coding, research, browser and **customer-service** agents". There is no customer-service group, and tau-bench is excluded. Fix: replace it with "business and knowledge-work".

### 27. [S] The STEPS "Red-team the result" card claims fixes already made
"Errors found were fixed or the value was removed." That is only true once the blockers above are fixed. Fix: publish only after 1–3 are fixed, or reword to "Errors found are fixed or the value removed before publication".

### 28. [S] The STEPS "Use independent results only" card overstates
- Terminal-Bench "does not mark verified vs submitted" (agentic.notes.md), so its rows may have been run by the agent's developer.
- AA Coding Agent scores are inside the developers' own tools (Claude Code, Codex, Muse Code, Mistral Vibe).
- Fix: add "Terminal-Bench does not say which results it verified".

### 29. [m] "Every score and price links to its source" is not quite true
Release dates taken from AA have no link, and derived costs are not on any source page. Fix: "Every score and price links to the page it came from; derived costs are marked."

### 30. [m] The no-JavaScript fallback points to a list that is not there
"The full list is in the methodology section below." The methodology section lists benchmarks, not models. Fix: render a static model list, or remove the sentence.

---

## Summary of blockers and should-fix items

**Blockers**
1. Terminal-Bench misses Opus 5.5 and Sonnet 5.5 (its #1 and #2).
2. The non-API Muse Wonder Full is merged into Muse Wonder and priced at the API rate.
3. Mistral Large 4 Preview is merged with GA, and the GA rows on Vals and GPQA are unmatched.

**Should-fix**
- Matching: snapshot mixing for Qwen 0902 and DeepSeek 0910/1017 (4); Nova 2 Lite and Baseten misses (5); quantized and hosted policy (6).
- Prices and access: introductory prices (10); price provenance text (11).
- Method: best row without a cost (14); best-setting bias (15); derived-cost label (16); LiveBench n (17); CIs (18); Fable 5.2 pre-launch (20).
- Text and coverage: unsupported descriptions (22); Arena top-60 cut (23); card n and choices (24); customer-service text (26); red-team claim (27); independence claim (28).
