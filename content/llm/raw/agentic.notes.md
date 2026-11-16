# Agentic benchmarks: source notes (prefix `agentic`), refresh

Retrieved 2026-11-16 with `curl` (HTTPS proxy, TLS verified). Downloads are in /home/claude/llmrefresh/dl/agentic/, parser scripts in /home/claude/llmrefresh/scripts/agentic_*.py. Same sources, endpoints and selection rules as the 2026-11-11 collection. I kept the benchmark names exactly; all 26 previous benchmark names are present and none were added. `agentic.models.json` is empty because these boards publish no model specs. 1,427 score rows (previously 1,399).
For every board I rebuilt the rows from fresh data and diffed them against the previous raw file. Only Terminal-Bench 4.1, OSWorld 2.0 and Vending-Bench 2 changed. Every other board's numbers came out identical.

## SWE-bench (Verified, Multilingual): https://www.swebench.com/
- **Data:** embedded `<script id="leaderboard-data">` JSON (five boards). Unchanged since last time.
- **Newest entries:** Verified 2026-02-26, Multilingual 2026-02-20. No "last updated" date is shown, so the board is stale.
- **Selection:** same as before: the Verified top 50 by score (non-mini rows go to the full-leaderboard benchmark), mini-SWE-agent rows from 2025-07 on, and all Multilingual rows.
- **Cost:** `cost_per_task_usd` = `instance_cost`; `cost_total_usd` = `cost`. A value of 0 means unknown.
- **Self-reported flag:** set when `checked` is not True. mini-SWE-agent rows are maintainer runs.
- **Rows:** 34 + 47 + 13.

## SWE-Bench Pro (Scale): https://labs.scale.com/leaderboard/swe_bench_pro
- **Data:** RSC flight `variants`: Public 731 tasks (25 rows) and Private/commercial 276 tasks (14 rows). Unchanged; newest `createdAt` is 2026-07-09.
- **Scaffold:** `*` = mini-swe-agent (page legend). SWE-Agent for unstarred rows is inferred from the methodology text.
- **Cost:** none shown.

## Terminal-Bench 4.1: https://www.tbench.ai/ (/leaderboard redirects here)
- **Data:** RSC flight rows from leaderboard id 947c0b13 ("Terminal-Bench 4.1", record updated_at 2026-11-14). 59 rows, up from 35.
- **New rows:** the 24 new rows were all created 2026-11-13/14, including several older models newly posted (e.g. Gemini 4 Carbon, Gemini 4 Argon, Kimi K3). The page mentions no other Terminal-Bench version (only 4.1).
- **Score and cost:** accuracy with 95% CI half-width; `votes_or_n` = n_trials (330 on every row); `cost_total_usd` = total_cost_usd (whole run). Muse Spark 1.3 shows $0, so its cost is null.
- **Fields:** effort = `reasoning_effort`; agent = agent_display. `result_date` = row metadata date. Previously ranked rows moved down because new rows were inserted; their scores are unchanged.
- **Gemini 4 Hydrogen** is listed as 56.36% ± 2.97 (Antigravity CLI, high, $784.24, date Nov 12, 2026). The board does not show Google's claimed 57.0% "cheating-adjusted" figure, so I did not record it.
- **Verification:** the board does not mark verified vs submitted rows, so `self_reported=false` with a caveat.

## OSWorld 2.0: https://osworld-v2.xlang.ai/
- **Data:** `static/data/leaderboard/official-results.json` (updatedAt now 2026-11-14; was 2026-10-15). benchmarkVersion "OSWorld 2.0"; task releases v2026.06.24 (default), v2026.08.08 and v2.1.
- **v2.1 is a task release inside OSWorld 2.0**, not a separate board. Its rows stay under the existing benchmark names, with the release in `notes`.
- **New row:** MiniMax M3.1 Flash (v2026.08.08, full set, adaptive, 500 steps): 26.85 binary / 62.01 partial. `official`=False, so `self_reported`=true; runCount 2.
- **No Gemini rows.** No 77.6% figure appears on the page or in the data, so the OSWorld-2.1 77.6% claim is not recorded.
- **Cost:** `cost_total_usd` = estimatedCostUsd. `costPerTaskUsd` is stated only for Sai.
- **Rows:** 56 + 56.

## OSWorld-Verified: https://os-world.github.io/ (redirects to http://osworld-v1.xlang.ai/)
- **Data:** the verified xlsx, top 60 by success rate (newest date 2026-08-01), plus the 3 recent self-reported Screenshot entries. Unchanged.
- **News:** the page still shows "2026-06-26: OSWorld 2.0 is now available".

## τ-bench / τ²-bench / τ³: https://taubench.com/
- **Data:** S3 manifest `submissions/manifest.json`: 30 current + 16 legacy submissions, the same lists as before. I re-downloaded all 46 submission.json files and kept those dated 2025-07 or later.
- **Overall:** the τ² overall top 3 (87.9 / 85.4 / 85.3) is static in the homepage HTML.
- **Homepage τ³-Banking top 3:** Qwen 3.8 Max 55.2%, Claude Opus 5 48.7%, Grok 4.5 47.9%. These match the submissions.
- **Changes:** none in numbers. The Cortex submission's methodology says "Cost is the average agent spend per trajectory, excluding the user simulator"; I added this to its notes.
- **Not extracted:** voice boards (voice, voice_v2).
- **Cost:** `cost_per_task_usd` = per-domain `cost` ("Avg Cost"). Its unit is not defined except in Cortex's own notes.

## BFCL V4: https://gorilla.cs.berkeley.edu/leaderboard.html
- **Data:** `data_overall.csv`, still "Last Updated: 2026-04-12". Identical to before. Top 60 ranks: Overall / Multi Turn / Web Search.
- **Cost:** `cost_total_usd` = Total Cost ($) (Overall rows only). The board is stale.

## Aider Polyglot: https://aider.chat/docs/leaderboards/
- **Status:** "last updated November 20, 2025"; the newest entry is 2025-10-03, so the board is stale.
- **Data:** I read the records from the site's GitHub YAML (raw.githubusercontent.com/Aider-AI/aider/main/aider/website/_data/polyglot_leaderboard.yml), which the page renders. 56 rows dated 2025. Identical to before.

## METR Time Horizons 1.1: https://metr.org/time-horizons/
- **Status:** "This page is no longer actively updated. LAST UPDATED September 8, 2026".
- **Data:** `assets/benchmark_results_1_1.yaml` is unchanged. 14 models × p50/p80, with display names checked against the page.

## ARC-AGI (1, 2, 3): https://arcprize.org/leaderboard
- **Data:** RSC `groups` (121 groups, unchanged). I resolved RSC `$` references and skipped entries with display=false (the previous rule).
- **Newest release date:** 2026-11-10 (Gemini 4 Carbon). **No Gemini 4 Hydrogen and no new Qwen entry.** Inkling 2 Small (XHigh) was already present.
- **Cost:** ARC-AGI-1/2 `cost_per_task_usd` = costPerTask. ARC-AGI-3 `cost` → `cost_total_usd` (definition not stated).
- **Developer:** now the provider displayName (e.g. "Johan Land" instead of "johan_land").

## Vending-Bench 2 (Andon Labs): https://andonlabs.com/evals/vending-bench-2
- **Data:** runs data (`runs.vb2`) from the JS chunk Bl9fFL93.js; the cost-per-run table and the "New" list from nodes/26.CDA-0jog.js. 76 models (was 74). No update date is shown.
- **New rows:** Gemini 4 Hydrogen, rank 3, $14,549.49 ± $495 SEM, n=6, mean cost per run $162.14 at $1.5/$7.5 per Mtok. The board lists this, so it matches Google's $14,549 claim. Claude Fable 5.2, rank 12, $9,628.48, mean cost $731.42. Page release dates: Hydrogen 2026-11-12, Fable 5.2 2026-11-09.
- **Cost:** `cost_per_task_usd` = mean_cost per full run (list prices, no caching).
- **Setting:** now holds the effort suffix from names such as "Claude Fable 5 - High", as in the previous file.

## Leads checked on every board (2026-11-16)
- **Qwen4-Max, K2 Horizon 375B A23B, Ling 3.1 Flash 1019:** not listed on any of these boards.
- **"Inkling 2 Small":** on ARC-AGI-1/2 as "Inkling 2 Small (XHigh)" (already there). Terminal-Bench lists "Inkling Small 2" (xhigh, 13.03%), named exactly as shown. Whether the two are the same model is left to the merge step.
- **Gemini 4 Hydrogen:** on Terminal-Bench 4.1 and Vending-Bench 2 only.
- **Newest Qwen rows:** Terminal-Bench Qwen3.8-Max-0902; τ³ Qwen 3.8 Max; OSWorld 2.0 Qwen 3.7-Plus.

## Facts I'm unsure about
- **Terminal-Bench Hydrogen:** the board says 56.36% while Google claims 57.0% "cheating-adjusted". The board does not say whether any adjustment was applied.
- **Terminal-Bench re-ranking:** 24 rows were bulk-added on 2026-11-13/14, so ranks shifted. Ranks are as shown today.
- **Unchanged items from the previous notes:** ARC-AGI-3 Provider Adapter scores of 0.95+; ARC-AGI-3 costs above $10K versus the $10K per-run cap in the policy; undefined τ "Avg Cost" units; SWE-Bench Pro scaffold for unstarred rows (inferred); the non-monotonic Opus 5 effort ordering on OSWorld 2.0.
- **τ² overall Gemini 3.0 Pro:** `self_reported` was kept true as before. Its domain rows say "Submitted by Sierra", which is inconsistent.
- **SWE-bench, BFCL, Aider and METR** are stale relative to Nov 2026.
