# Red-team A: llm.json values, refresh of 2026-11-17 (site V5.45)

Audited file: `/home/claude/chmltech-website/content/llm/llm.json`, md5 46925c2c… (built 2026-11-17 18:46 UTC), compared with `llm.prev.json` (md5 31f57c5c…).
Live sources were fetched 2026-11-17 between 18:48 and 18:55 UTC with curl. All returned HTTP 200. Downloads are in `/home/claude/llmrefresh2/redteam/dlA/` and my parsers in `/home/claude/llmrefresh2/redteam/scriptsA/`. I edited no repo file and did not run build_dataset.py.

Severity: **B** = blocker (a wrong value would be published), **S** = should fix before publishing, **m** = minor (wording, consistency or traceability).

## Summary
| Check | Items checked | Result |
|---|---|---|
| 1 GPT-6.2 Astra / Sol fields | price, context, max output, max input, cutoff, modalities, computer use, release date, >272K price note (2 models, OpenAI model pages, pricing.md, changelog) | all correct |
| 1 GPT-6.2 benchmarks | AA Index 10 settings (score, cost, tokens, reasoning/answer split), Vals 2, ARC-AGI-2 10 settings, ECI 1, FrontierMath 1, GPQA 1 | all correct; S1 (note), m4 |
| 2 AA-deprecated models | GPT-6 Astra (5 settings), GPT-6.1 Sol (5), Gemini 3.8 Flash (3): Index, cost, tokens, time; deprecated flag and deprecatedTo; OpenAI / Google status | all correct; m3 |
| 3 Diffs vs prev | 30 ECI values + 33 CIs; 5 Qwen4-Max LiveBench rows (score, cost, setting); Hydrogen AA Coding row; all aa time changes on 3 models (spot-checked); 4 price changes and 4 max-output changes; Qwen4-Max max output and note; Gemma note | all correct; m2, m6 |
| 4 Prices | 4 changed (gpt-oss-20b, Muse Glimmer 30B, Nemotron 3 Ultra, Gemma 4 26B A4B) + 6 OpenAI + 39 others (17 OpenRouter, 22 first-party) = 49 of 52 priced models | all correct; m5 |
| 5 board_news (5 items, 11 claims) and `changes` (added, removed, results_before, 9 leaders) | every claim | all true except m1; leaders recomputed, all 9 match |

No blockers. 1 should-fix, 6 minor.

## Findings

**1. S1: The GPT-6.2 Astra note says Epoch itself said these results "may change". Epoch has not said that about GPT-6.2.**
`gpt-6-2-astra.notes`: "Epoch AI's results come from pre-launch testing, which Epoch says may change."
The only such statement on the Epoch hub belongs to the Nov 9 post about Claude Fable 5.2: "This is based on pre-launch testing using only our own benchmarks, and may change as more results become available." Epoch has published no post on GPT-6.2. "Pre-launch" is our own inference from the run dates: gpt-6.2-astra_max FrontierMath, GPQA and Tier 4 runs all have "Started at" 2026-10-27, before the Nov 17 release.
Evidence: https://epoch.ai/benchmarks (Latest activity list), https://epoch.ai/data/benchmark_data.zip (`gpqa_diamond.csv`, `frontiermath_tiers_1_3_v2.csv`, column "Started at").
Fix: in MODEL_NOTES["gpt-6-2-astra"], replace the last sentence with "Epoch AI's runs are dated Oct 27, 2026, before the public release, and Epoch has not yet published results from other benchmarks for this model."

**2. m1: board_news item 1 implies that both new models are on Epoch AI. Only Astra is.**
Text: "Early results: on Artificial Analysis, Vals, ARC-AGI and Epoch AI so far". GPT-6.2 Sol has no row in eci_scores.csv or in any Epoch file in the zip.
Evidence: https://epoch.ai/data/eci_scores.csv
Fix: "Early results: on Artificial Analysis, Vals and ARC-AGI so far (Astra also on Epoch AI), not yet on Arena, LiveBench, Terminal-Bench or Vending-Bench."

**3. m2: The new max-output values for three OpenRouter-priced models are the default host's limit, not the model's.**
OpenRouter's top_provider values match exactly: gpt-oss-20b 117,964; Muse Glimmer 30B 117,964; Nemotron 3 Ultra 16,384. For Nemotron 3 Ultra, 16,384 is DeepInfra's cap. KT serves it at the same $0.50 / $2.20 with 235,929, and BaseTen with 182,520. The field now changes whenever OpenRouter's default host changes, as it did today for all three.
Evidence: https://openrouter.ai/api/v1/models/nvidia/nemotron-3-ultra-550b-a55b/endpoints (and the same path for openai/gpt-oss-20b and meta/muse-glimmer-30b).
Fix: either set `maxout` to null when its only source is OpenRouter, or add the note "Maximum output shown is the default OpenRouter host's limit; other hosts allow more." to these three models (and the other OpenRouter-sourced rows).

**4. m3: Gemini 3.8 Flash's AA-deprecation sentence now appears in the price note.**
MODEL_NOTES["gemini-3-8-flash"] has price_flag True, so `pnote` reads "...from Jan 1, 2027. Artificial Analysis now lists it as deprecated (Google does not); its Index results are taken from its Artificial Analysis model page." That second sentence is not about price. The facts are correct: AA flags `deprecated: true` with deprecatedTo gemini-4-hydrogen, and Google's deprecations page lists gemini-3.8-flash with "No shutdown date announced". The $0.75 / $3.75 to $1.50 / $7.50 schedule is correct.
Evidence: https://artificialanalysis.ai/models/gemini-3-8-flash, https://ai.google.dev/gemini-api/docs/deprecations (redirects to aistudio.google.com/docs/deprecations).
Fix: keep only the price sentence in MODEL_NOTES["gemini-3-8-flash"] (flag True). Add the deprecation sentence to `notes` only, e.g. after the PRICE_FIX loop: `if c["id"] == "gemini-3-8-flash": m["notes"] = m["notes"].replace("Release date", "Artificial Analysis now lists it as deprecated (Google does not); its Index results are taken from its Artificial Analysis model page. Release date")`.

**5. m4: Two of GPT-6.2 Sol's ARC-AGI-2 settings carry ARC's partial-coverage warning, and it is not shown.**
The Sol (Max) and Sol (Medium) rows note "Partial dataset coverage: scores use full catalog denominators; costs include recorded usage only, excluding unrecorded attempts." So the Max $0.2611 and Medium $0.1032 costs in `s.arc2.alt` may be too low. The headline High row (85.833%, $0.1326) has no such note. All 10 GPT-6.2 ARC-AGI-2 values and costs are otherwise correct.
Evidence: https://arcprize.org/leaderboard (RSC groups, model notes for openai-gpt-6-2-sol-max and -medium).
Fix: append to MODEL_NOTES["gpt-6-2-sol"]: "ARC Prize marks its Max and Medium ARC-AGI-2 runs as partial coverage; their costs exclude unrecorded attempts."

**6. m5: Only the two new models have a long-context price note. The older OpenAI models have the same rule.**
OpenAI's pricing page applies 2x input / 1.5x output above 272K input tokens to GPT-6 Astra ($20 / $75), GPT-6.1 Sol ($4 / $15), GPT-6.1 Terra ($2 / $7.50) and GPT-6 Luna ($0.20 / $0.75), not only to GPT-6.2. Grok 4.7 also has a tier: $4 / $12 at 200K or more. The note also leaves out that the higher rate applies to the full request.
Evidence: https://developers.openai.com/api/docs/pricing (Standard table, long-context columns), https://docs.x.ai/developers/models/grok-4.7
Fix: add "Price above 272K input tokens: $X input / $Y output for the whole request." to gpt-6-astra, gpt-6-1-sol, gpt-6-1-terra and gpt-6-luna, and the equivalent 200K note to grok-4-7. Also add "for the whole request" to both GPT-6.2 notes.

**7. m6 (method): Switching ECI to the live CSV is correct. Record the version and re-fetch before publishing.**
https://epoch.ai/eci shows "Updated Nov. 17, 2026" and links `/data/eci_scores.csv`. The hub card says "174 top ECI: GPT-6.2 Astra", which matches the CSV. benchmark_data.zip was rebuilt at 2026-11-17 18:31 UTC, but its `epoch_capabilities_index/eci_scores.csv` still has no GPT-6.2 Astra (256 rows against 257). It also differs from the live CSV by up to 0.12 points (Claude Fable 5.2: 173.62 in the zip, 173.5 live). So the live CSV is the one the site displays, and the zip is behind. All 33 llm.json ECI values and CIs equal the live CSV, which had etag e88aedac98d555d4411ef0e896ba9f69 at 18:50 UTC. FrontierMath and GPQA are still taken from the zip, and their Astra values (92.632, 96.843, with stderrs) equal the 18:31 zip.
Fix: add to the method or ECI caveat: "ECI is taken from Epoch's live eci_scores.csv, which is updated before its benchmark_data.zip." Re-fetch the CSV just before publishing, because the zip and CSV disagree today and Epoch may republish either one.

## Verified (PASS)
- **GPT-6.2 Astra:** $8 / $40; context 1,050,000; max output 128,000; cutoff May 18, 2026; text and image input; computer_use tool listed. The >272K rule gives $16 / $60, which matches the pricing table. Changelog entry dated Nov 17.
- **GPT-6.2 Sol:** $2 / $10; same context and max output; cutoff Jun 01, 2026; >272K price $4 / $15.
- **AA (models/gpt-6-2-astra, gpt-6-2-sol, leaderboards/models):**
  - Astra Low to Max: 45.650 / 56.999 / 60.088 / 61.560 / 62.139, at $0.6617 / 1.618 / 2.074 / 2.521 / 3.998.
  - Astra tokens: 5,216 / 13,165 / 17,828 / 22,238 / 41,029. Max split 26,150 reasoning / 14,880 answer.
  - Sol Low to Max: 40.553 / 52.678 / 54.890 / 55.735 / 57.258. AA gives no cost for Low to X-high (no price on those entries) and $1.014 at Max.
  - Sol tokens: 5,980 / 13,651 / 20,160 / 24,323 / 40,360. Max split 22,800 / 17,561.
  - No time per task yet, which matches llm.json.
- **Vals (vals_index, updated 2026-11-16):** Astra 67.656% at $10.681415, stderr 0.935, effort max. Sol 66.059% at $3.179284, stderr 0.91.
- **ARC-AGI-2:** Astra 91.667 / 93.333 / 94.583 / 95.833 / 95.833 at $0.2749 / 0.3089 / 0.4083 / 0.4996 / 0.9695. Sol 57.917 / 82.917 / 85.833 / 85.833 / 85.833 at $0.07576 / 0.1032 / 0.1326 / 0.1742 / 0.2611. The headline is the cheapest of the tied top settings, the same rule as other models.
- **Deprecated on AA:** GPT-6 Astra, GPT-6.1 Sol and Gemini 3.8 Flash all have `deprecated: true` (deprecatedTo gpt-6-2-astra, gpt-6-2-sol and gemini-4-hydrogen) and are absent from /leaderboards/models.
  - All 13 Index values, 12 costs and 12 token totals match their model pages, e.g. GPT-6 Astra Max 56.854 at $6.245 and 51,973 tokens; GPT-6.1 Sol Max 54.609 at $1.272 and 67,824 tokens; Gemini 3.8 Flash High 30.847 at $7.766 and 98,940 tokens. Gemini 3.8 Flash Low has no cost on AA either.
  - Time values checked: 1225.73 s = 20.43 min, 1386.66 s = 23.11 min, 847.35 s = 14.12 min.
- **"Superseded, still offered":** GPT-6 Astra ($10 / $50) and GPT-6.1 Sol ($2 / $10) are still on their model pages and the pricing page, now under the full list and not under the flagship list. Neither is on https://developers.openai.com/api/docs/deprecations.
- **Qwen4-Max LiveBench:** table.csv and cost.csv (20261106, last-modified Nov 16 22:39 GMT) give coding 69.8 (23.364/24 = 0.9735), browser 80.7 (1.506), research 84.7 (1.493), long agentic 47.5 (5.628) and data 83.4 (0.1439). The "X-high" label comes from LiveBench's own JS (main.f14f89ca.js, `effort:"xhigh"`).
- **Qwen4-Max model page:** the QwenCloud page says Max Output 131K and Max Output (Thinking) 262K. This matches maxout 131,000 and the note. Price $1.5 / $4.5.
- **Gemini 4 Hydrogen AA Coding Agent:** Antigravity CLI, Xhigh, 0.523167, $4.4528/task.
- **Prices:**
  - gpt-oss-20b $0.018 / $0.09 (AkashML, Darkbloom), Muse Glimmer 30B $0.35 / $1.50 (Together) and Nemotron 3 Ultra $0.50 / $2.20 (DeepInfra, KT) are all the OpenRouter listed price.
  - **Gemma 4 26B A4B:** NextBit is now $0.09 / $0.30 with `discount: 0`, so the promotion has ended. Removing the discount note is correct.
  - 17 OpenRouter rows checked: gpt-oss-120b, Gemma 4 31B, Muse Spark Open, Nemotron 3.5 Super VL and Lightning, Granite 4.2 8B, MiMo V2.6 Pro, Step 5 Preview, Hy4 (0.417 / 1.2505 at 50% discount, so 0.834 / 2.501), Inkling, Inkling 2 Small and Beam 1.0, plus the 4 changed models and Qwen4 Max.
  - 22 first-party prices checked: Claude Fable, Mythos, Opus, Sonnet and Haiku 5.x (Haiku up to 100K), Gemini 4 Carbon / Argon ($2 / $10 to Nov 30), Hydrogen, 3.8 Flash, 3.5 Flash-Lite, Grok 4.7, Grok Build 0.1, Mistral Large 4, DeepSeek V4 Pro and V4.1 Flash (peak), Kimi K3.1 Pro, GLM-5.3 and Flash, MiniMax-M3 (after the permanent 50% off) and M3.1 Flash, Qwen4-Max, Qwen3.8-Max, and Muse Wonder / Spark / Ember. GPT-6.1 Terra and GPT-6 Luna were checked with the OpenAI group.
  - Not re-read: Nova 2 Pro and Lite (prices filled by JS), Command A+, Qwen3.8 27B.
- **board_news:**
  - 20% less: $8 is 0.8 x $10. Correct.
  - Copilot Fusion: rank 1 on tbench.ai at 71.21%, dated Nov 17. Its model link is docs.github.com/…/copilot-fusion. No model in llm.json carries 71.21.
  - Arena: the HF dataset was last modified 2026-11-16 04:02 UTC (commit 8013e3f0), and there has been no commit since.
  - No GPT-6.2 on LiveBench table.csv, Vending-Bench 2 chunk Bl9fFL93.js, Terminal-Bench or Arena.
- **changes:** added = the 2 GPT-6.2 models; removed = none. results_before 515 = sum of s in prev. All 9 leaders recomputed from llm.json match. llm.json now holds 530 results.
