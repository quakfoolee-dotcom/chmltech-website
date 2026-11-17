# index: composite / independent evaluation sources (retrieved 2026-11-17)

Downloads: /home/claude/llmrefresh2/dl/index2/ (aa, aa/m = 62 per-model pages, epoch, vals, vectara, lb). Scripts: /home/claude/llmrefresh2/scripts/index_*.py (build: index_build.py; per-model page parser: index_aa_pages.py). All fetched with curl (HTTP 200); WebFetch not used. Benchmark names identical to the Nov 16 raw/index.scores.json (checked by script: no new or missing names).

## VERSION / UPDATE STATUS (read first)
- AA Intelligence Index: still **v5.0.1**. Coding Agent Index: same 3-component set as Nov 16 (FrontierCode-AA 2.0, SWE-Atlas-QnA, Terminal-Bench v4); 30 agent+model pairs (was 29; added Antigravity CLI - Gemini 4 Hydrogen (Xhigh) 0.523, $4.45/task). All 29 old scores unchanged. No GPT-6.2 pair yet.
- Epoch: hub and /eci show "Updated Nov. 17, 2026". **The live ECI CSV (https://epoch.ai/data/eci_scores.csv) is newer than benchmark_data.zip**: it adds GPT-6.2 Astra and re-estimates 222 other models slightly (e.g. Claude Fable 5.2 173.62 -> 173.5). ECI rows now come from the live CSV (source_url changed); zip value kept in notes where different. FrontierMath/GPQA/SWE-bench rows still from the zip.
- Vals Index: still **v2.2**, updated **2026-11-16**, 41 models (was 38). No score changes for existing models.
- Vectara: unchanged file ("Last updated on October 22, 2026"), 111 rows.
- LiveBench 2.0: still release 20261106 (20261107-20261117 all 404; JS release list ends at 20261106; new JS bundle main.f14f89ca.js). Files updated in place (last-modified 2026-11-16 22:39 GMT): Qwen4-Max added (36 models). Site still says "Last updated 11 November 2026". No GPT-6.2.

## DEPRECATED MODELS ON ARTIFICIAL ANALYSIS (rows kept)
AA now flags these `deprecated: true` and they are absent from /leaderboards/models (not even as deprecated entries). All their rows (Index, cost per task, Time per Task, Output Speed, output tokens, and their index.models.json records) were taken from the deprecated entries embedded in their own per-model pages, and every such row says "DEPRECATED ON AA" in notes, with the page as source_url:
- GPT-6 Astra (Low/Medium/High/Xhigh/Max) - https://artificialanalysis.ai/models/gpt-6-astra (AA deprecatedTo: gpt-6-2-astra)
- GPT-6.1 Sol (Low/Medium/High/Xhigh/Max) - https://artificialanalysis.ai/models/gpt-6-1-sol (deprecatedTo: gpt-6-2-sol)
- Gemini 3.8 Flash (Low/Medium/High) - https://artificialanalysis.ai/models/gemini-3-8-flash (deprecatedTo: gemini-4-hydrogen)
- Inkling Small - https://artificialanalysis.ai/models/inkling-small (deprecatedTo: inkling-2-small)
Index scores and cost per task are identical to the Nov 16 values (27 rows checked). Time per Task and Output Speed are AA's current page values and differ a little from Nov 16 (e.g. GPT-6 Astra (Xhigh) speed 39.18 -> 41.19 tok/s); speed = page "headline".outputSpeed, the same field the leaderboard uses (identical for all 91 current models compared). Gemini 3.8 Flash (Low) still has no cost, time or token data.
Also: Qwen3.8 Max (0902) (33.65) is again only in home-page chart data (one embedded copy carries deprecated: true); kept with the home page as source. Claude Fable 5.1 (Max, Default Fallback) is no longer in any Intelligence Index data (only in the Coding Agent and Cyber arrays), so its Index and token rows are gone. DeepSeek V4 Pro 0813 (High) has no Time per Task / Output Speed any more.

## Artificial Analysis (artificialanalysis.ai)
- Intelligence Index v5.0.1 (method: https://artificialanalysis.ai/methodology/intelligence-benchmarking): 9 evals, 4 categories at 25%. 126 rows = 111 current leaderboard models + 14 deprecated (above) + 1 home-only.
- Cost per Task = weighted average USD per index task, contestant calls only, measured cache-hit rates. Time per Task in seconds (table shows minutes). Output Speed tokens/s.
- Output tokens per Index task (field intelligenceIndexOutputTokensPerTask): score = total output, reasoning/answer split in notes; 124 rows from the 62 per-model pages + home (no conflicts between pages).
- **GPT-6.2 (released 2026-11-17)**: Astra Low 45.65 ($0.662), Medium 57.00 ($1.618), High 60.09 ($2.074), Xhigh 61.56 ($2.521), Max 62.14 ($3.998); price $8/$40 per 1M, cache hit $0.4. Sol Low 40.55, Medium 52.68, High 54.89, Xhigh 55.74 - **no cost per task and no price listed**; Sol Max 57.26 ($1.014; price $2/$10). No Time per Task or Output Speed for any GPT-6.2 setting yet. Output tokens: Astra 5.2k/13.2k/17.8k/22.2k/41.0k, Sol 6.0k/13.7k/20.2k/24.3k/40.4k (Low..Max).
- Also new on AA: A.X-K2, Gemma 4 E4B (Reasoning).
- index.models.json: 125 AA records (secondary); details from per-model pages as before.

## Epoch AI (https://epoch.ai/benchmarks; https://epoch.ai/data/benchmark_data.zip; https://epoch.ai/data/eci_scores.csv)
- ECI (Bayesian since Nov 4) with credible interval; Epoch-run FrontierMath Tiers 1-3 v2, Tier 4 v2, GPQA Diamond, SWE-bench Verified (mean_score 0-1, stderr). Models released on/after 2025-05-01. No cost data.
- **GPT-6.2 Astra**: ECI 174.17 (170.29-178.58), new top (hub card "174 top ECI: GPT-6.2 Astra"); gpt-6.2-astra_max FrontierMath T1-3 0.926, Tier 4 **1.0 (stderr 0)**, GPQA 0.968. All three runs "Started at" 2026-10-27, before the 2026-11-17 release = pre-launch testing (rows say so). Epoch has no news post on GPT-6.2 yet (latest is the Nov 9 Fable 5.2 "pre-launch testing" item). No GPT-6.2 Sol and no GPT-6.2 SWE-bench Verified in Epoch data.

## Vals AI (https://www.vals.ai/benchmarks/vals_index)
- Vals Index v2.2, finance/coding/legal/tax agent tasks weighted by U.S. GDP share; cost_per_task_usd = cost_per_test. New: openai/gpt-6.2-astra 67.656% $10.681415 (#7, reasoning_effort=max); openai/gpt-6.2-sol 66.059% $3.179284 (#9, max); tencent/hy4-flash 50.779% $0.069937 (#35).

## Vectara Hallucination Leaderboard (raw README) - unchanged since Oct 22, 2026; 111 rows.

## LiveBench 2.0 (https://livebench.ai/data/20261106/)
- table.csv (mean task score 0-100), cost.csv (total USD per suite + nq_* task counts; cost_per_task_usd left null), llm_time.csv in notes. All 7 suites as before. New: qwen4-max ("Qwen4-Max"). Overall score is client-side, not output.

## Not reached / not used
- AA Cyber and Decision indexes skipped as before. Nothing unreachable.

## Facts I am unsure about
- Whether Epoch's zip will adopt the live ECI values (zip and live CSV disagree for 222 models today).
- Why AA lists no cost/price for GPT-6.2 Sol except at Max (Vals does give Sol a cost per test).
- GPT-6.2 Astra FrontierMath Tier 4 = 1.0 with stderr 0 (as published; looks like a perfect or small-sample score).
- AA "parameters" unit; AA "Cost per Task" weighting; LiveBench suite weighting (as noted Nov 16).
- AA, Vals and LiveBench cost figures use different task sets and harnesses and are not comparable.
