# index: composite / independent evaluation sources (retrieved 2026-11-16)

Downloads: /home/claude/llmrefresh/dl/index/ (aa, epoch, vals, vectara, lb). Scripts: /home/claude/llmrefresh/scripts/idx_*.py (build: idx_build.py). All fetched with curl (HTTP 200); WebFetch not used.

## VERSION / COMPOSITION CHANGES (read first)
- **AA Coding Agent Index: component set changed.** It is now the simple average of FrontierCode-AA 2.0, SWE-Atlas-QnA(-AA) and Terminal-Bench v4. On Nov 11 it used FrontierCode v1.1 Main. AA shows no version number, so the benchmark name is kept as "Artificial Analysis Coding Agent Index", but scores are NOT comparable with the Nov 11 rows (e.g. Mirror - Beam 1.0 went from 0.205 to 0.155). AA's own text: "comparability is best interpreted within the published benchmark suite and its current component set". It now has 29 agent+model pairs (36 before). Source: https://artificialanalysis.ai/agents/coding-agents (same 29 ids as on the home page).
- AA Intelligence Index: still **v5.0.1** (no change). Vals Index: still **v2.2**, but updated **2026-11-15** (38 models, was 36). Epoch: hub "Updated Nov. 16, 2026". Vectara: unchanged, "Last updated on October 22, 2026". LiveBench 2.0: no release newer than 20261106 (20261107-20261116 all 404; JS release list still ends at 20261106), but the 20261106 files were updated in place (35 models, was 34; Gemini 4 Hydrogen added) and the site says "Last updated 11 November 2026".

## Artificial Analysis (artificialanalysis.ai)
- **Intelligence Index v5.0.1** (method unchanged from Nov 11; see https://artificialanalysis.ai/methodology/intelligence-benchmarking): 9 evals, 4 categories at 25%. Rows: 113 non-deprecated models with an index score from the flight data of https://artificialanalysis.ai/leaderboards/models, plus 2 models that appear only in the home-page chart data (Claude Fable 5.1 (Max, Default Fallback) 49.16; Qwen3.8 Max (0902) 33.65). These 2 are NOT in the leaderboard list (not even as deprecated); their source_url is the home page.
- Cost per Task = weighted average USD per index task, contestant calls only, measured cache-hit rates. K2 Horizon 375B A23B has cost 0 and price 0/0 in page data.
- Time per Task (seconds; table shows minutes) and Output Speed (tokens/s) as before.
- **NEW: "Artificial Analysis output tokens per Index task"** (113 rows, unit tokens): field `intelligenceIndexOutputTokensPerTask` {reasoning, answer, output}; score = output (total), reasoning/answer split in notes. AA describes it as "Weighted average number of output tokens used to run one task in the Artificial Analysis Intelligence Index". The home chart shows only 29 models, so the full set came from the 58 per-model pages https://artificialanalysis.ai/models/<slug> (each embeds its variants and comparison models; values were identical across pages, 0 conflicts). source_url = the model's own page where it held the record. No token data for Gemma 4 31B (Reasoning) and Gemini 3.8 Flash (Low).
- index.models.json: 113 AA records (secondary). Prices/context/reasoning from the leaderboard; release date, licence, parameter fields, modalities and knowledge cutoff from the per-model page detail record (named in notes). AA's "parameters" field is copied raw with the active-parameter field (billions) - unit of "parameters" not stated.
- New on AA since Nov 11: Gemini 4 Hydrogen (Xhigh 53.92, High 50.79, Medium 41.23, Low 26.89; release 2026-11-12; $1.5/$7.5 per 1M), Qwen4 Max 42.89, Gemini 4 Argon (Medium), JT-4.1 Flash 236B A21B (China Mobile), DeepSeek V4 Pro 0813 (High). xAI is labelled "SpaceXAI" by AA (and Vals).

## Epoch AI (https://epoch.ai/benchmarks; https://epoch.ai/data/benchmark_data.zip)
- Same method as Nov 11: ECI (Bayesian since Nov 4) with credible interval; Epoch-run FrontierMath Tiers 1-3 v2, Tier 4 v2, GPQA Diamond, SWE-bench Verified (mean_score 0-1, stderr). Only models released on/after 2025-05-01. No cost data.
- No Gemini 4 Hydrogen or Qwen4 Max in any Epoch file yet. Newest ECI entry still Claude Fable 5.2 (2026-11-09). GPQA rows 208 (was 205).

## Vals AI (https://www.vals.ai/benchmarks/vals_index)
- Vals Index v2.2, updated 2026-11-15, 38 models; finance, coding, legal, tax agent tasks weighted by U.S. GDP share. cost_per_task_usd = `cost_per_test` ("Cost / Test"). Rank = position in the page's overall ranked list (display names in notes). Beam 1.0 cost null.
- New: google/gemini-4-hydrogen 68.492% $9.838059 (#6, reasoning_effort=xhigh); alibaba/qwen4-max 63.197% $9.3304 (#11, xhigh).

## Vectara Hallucination Leaderboard (raw README)
- Unchanged since Oct 22, 2026; 111 rows; no Hydrogen/Qwen4.

## LiveBench 2.0 (https://livebench.ai/data/20261106/)
- table.csv (mean task score 0-100, single run), cost.csv (total USD per suite + nq_* task counts; cost_per_task_usd left null, no own division), llm_time.csv (seconds in LLM calls per task, in notes). All 7 suites output with the previous names. Display names/orgs/effort from the JS model map (main.8a7822ea.js); "inkling" has no map entry.
- Gemini 4 Hydrogen listed at effort "xhigh". Overall score is client-side, not output.

## Not reached / not used
- AA Cyber Index array and Decision Index skipped as before. Qwen primary pages were not part of this task.

## Cross-check against user screenshots
- AA index bars (28 models) all match the rounded page data; Hydrogen (xhigh) cost per task $3.16, Qwen4 Max $3.27, consistent with the scatter. Output-token totals match the chart (Hydrogen 154k, Qwen4 Max 105k, Sonnet 5.5 285k). Vals top 11 match exactly (Hydrogen 68.49% $9.84 #6; Qwen 4 Max 63.20% $9.33 #11). No mismatches.

## Facts I am unsure about
- Why Claude Fable 5.1 (Max) and Qwen3.8 Max (0902) are in AA home charts but absent from the leaderboard list.
- AA Coding Agent attempt counts (396/372/197) are attempts, not task counts; the task counts per eval were not found.
- AA "parameters" unit; AA "Cost per Task" weighting ("weighted average", assumed index weights).
- LiveBench "every suite counts equally" vs `_overall_weights` (Long Agentic 2.0, Coding 1.5, Design 1.5) - conflict persists.
- AA, Vals and LiveBench cost figures use different task sets and harnesses and are not comparable.
