# Agentic benchmarks: source notes (prefix `agentic`)

Retrieved 2026-11-11/12. `agentic.models.json` is empty because these boards don't publish model specs. All 1,399 rows are in `agentic.scores.json`.
WebFetch was refused for every URL I tried (tbench.ai/leaderboard, os-world.github.io, gorilla.cs.berkeley.edu/leaderboard.html, swebench.com): "permission request not answered". I confirmed every public URL with `curl` instead (HTTP 200, final URL recorded). I also re-downloaded the OSWorld-Verified xlsx and the BFCL csv, and both were byte-identical to the supplied files.
Scaffold/harness and setting (effort) are kept in separate fields. A model with several scaffolds or efforts appears once per row on the board.

## SWE-bench (Verified, Multilingual): https://www.swebench.com/
- **What it measures:** the % of real GitHub issues resolved, checked by hidden tests. Verified has 500 human-validated instances.
- **Data:** the leaderboard JSON embedded in index.html (`swebench_data.json`). The page has no "last updated" date. The newest entry is 2026-02-26 (Verified) and 2026-02-20 (Multilingual), so the board looks stale relative to Nov 2026.
- **Bash-only view:** this is the Verified/Multilingual board filtered to agent = mini-SWE-agent. It is the most model-comparable view: every LM runs in the same minimal bash ReAct loop. `swebench.com/bash-only.html` returns 404. The page says mini-SWE-agent 1.x and 2.x results "are not necessarily comparable" (2.x uses tool calling; 1.x temperature is 0).
- **Rows kept:** the Verified top 50 by score plus all mini-SWE-agent rows dated 2025-07 or later; all 13 Multilingual rows. Lite, Test and Multimodal were skipped because their newest entries are 2025 and pre-frontier.
- **Self-reported flag:** `self_reported=true` for full-leaderboard systems whose `checked` flag is not True. mini-SWE-agent rows are runs by the SWE-bench team.
- **Cost:** `cost_per_task_usd` = data field `instance_cost` (average USD per instance). `cost_total_usd` = field `cost` (mini-SWE-agent rows only). A value of 0 was treated as unknown.

## SWE-Bench Pro (Scale): https://labs.scale.com/leaderboard/swe_bench_pro
- **What it measures:** long-horizon SWE tasks from copyleft and private repos. Public set = 731 tasks; private (commercial) set = 276 tasks.
- **Rows:** 25 public + 14 private, each with its rank and ± CI. No update date is shown; entry `createdAt` values run up to 2026-07-09.
- **Scaffold:** `*` = mini-swe-agent harness (page legend). The methodology text says other frontier models were run with SWE-Agent, so I recorded SWE-Agent for those, but that is an inference from the text, not a per-row label.
- **Limits:** grey rows were capped at 50 turns; others were uncapped cost with 250 turns. The page shows no cost.

## Terminal-Bench 4.1: https://www.tbench.ai/ (/leaderboard redirects here)
- **What it measures:** agent + model resolution rate on terminal tasks, with a 95% CI.
- **Rows:** 35 rows from `tbench_rows.json`, matching the page flight data. Leaderboard `updated_at` is 2026-11-11.
- **Fields:** `n_trials`=330 for every row. `cost_total_usd` = `total_cost_usd` for the whole run, as shown in the COST column. Muse Spark 1.3 shows $0, so I left its cost null.
- **Verification:** the board does not mark verified vs submitted rows, so I set `self_reported=false` with a caveat.

## OSWorld 2.0: https://osworld-v2.xlang.ai/
- **What it measures:** 108 long-horizon computer-use workflows (human median about 1.6 h), scored as binary completion and partial score.
- **Data:** `static/data/leaderboard/official-results.json`, `updatedAt` 2026-10-15. Task releases are v2026.06.24 (default), v2026.08.08 and v2.1, plus a full vs offline task set. Each combination is a separate row, with release, set and step budget in `notes`/`setting`.
- **Scaffold:** e2e rows are labelled "Foundation E2E GUI (tool setting)"; agent rows are named frameworks (Sai, Darwinx).
- **Self-reported flag:** `self_reported=true` where the `official` flag is missing.
- **Cost:** `cost_total_usd` = `estimatedCostUsd`. The page displays per-task cost as total/108; I did not compute that. `costPerTaskUsd` was stated only for Sai.

## OSWorld-Verified: https://os-world.github.io/ (now redirects to http://osworld-v1.xlang.ai/)
- **What it measures:** 369 (361 without Google Drive) desktop tasks.
- **Data:** the verified xlsx (results run or verified by maintainers): top 60 rows by success rate. The xlsx has Excel-serial dates, which I converted. The newest entries are about 2026-07-31.
- **News:** the page reports "2026-06-26: OSWorld 2.0 is now available".
- **Self-reported table:** I took only the 3 recent entries (AskUI, Turix, GTA1) and set `self_reported=true`.

## τ-bench / τ²-bench / τ³: https://taubench.com/
- **What it measures:** tool-agent-user conversations under policy. pass^1 per domain: Retail, Airline, Telecom (τ²) and τ³ Banking (knowledge retrieval).
- **Data:** each submission's JSON in the public S3 bucket the site reads (`.../submissions/<id>/submission.json`; the manifest lists 30 current + 16 legacy submissions). I kept those submitted 2025-07 or later.
- **Banking-only submissions:** most 2026-05 and 2026-08 Sierra runs cover banking only (AllTools retrieval; GPT-5.2 user simulator).
- **τ² overall:** the site averages the three τ² domains. I recorded only the homepage top 3 as displayed (87.9 / 85.4 / 85.3).
- **Self-reported flag:** `self_reported=true` when the submitter is not Sierra, unless the details say "Verified by Sierra" (Cortex).
- **Cost:** `cost_per_task_usd` = the per-domain `cost` field, shown on the site as "Avg Cost". I assume it is average agent cost per task, but the site does not define it.
- **Not extracted:** the τ³-Voice leaderboards (voice-leaderboard.json).

## BFCL V4: https://gorilla.cs.berkeley.edu/leaderboard.html
- **Data:** `data_overall.csv`. "Last Updated: 2026-04-12".
- **Rows:** top 60 ranks, with Overall, Multi Turn and Web Search accuracy. Overall is the unweighted average of subcategories.
- **Cost:** `cost_total_usd` = "Total Cost ($)", stated as an estimate for the entire benchmark (on Overall rows only).
- **Model labels:** FC = native tool calling; Prompt = prompt-based workaround.
- **Staleness:** the board is stale and lacks most 2026 models.

## Aider Polyglot: https://aider.chat/docs/leaderboards/
- **What it measures:** 225 Exercism exercises in 6 languages, scored as % solved after 2 attempts.
- **Update date:** "last updated November 20, 2025". The newest entry is 2025-10-03, so the board is stale.
- **Rows:** all entries dated 2025 (56 rows).
- **Cost:** `cost_total_usd` = `total_cost` for the full run. 0 was treated as unknown, because several free/preview endpoints show 0.

## METR Time Horizons 1.1: https://metr.org/time-horizons/
- **What it measures:** the human-expert task duration at which the agent succeeds 50% (or 80%) of the time, in minutes, with a CI.
- **Status:** "This page is no longer actively updated. LAST UPDATED September 8, 2026". The newest model in the data is Claude Mythos Preview (early), released 2026-04-07.
- **Rows:** 2025+ models only. Display names come from the page's task data; numbers come from `benchmark_results_1_1.yaml`.
- **Caveats stated by METR:** measurements above 16 h are unreliable; the tasks are mostly SWE/ML/cyber; some models were skipped.

## ARC-AGI (1, 2, 3): https://arcprize.org/leaderboard
- **Data:** the page's RSC data, from `arc_groups.json` (121 model groups). Testing policy: https://arcprize.org/policy.
- **Rows:** models released 2025-06 or later, with every effort level. Score is recorded as a fraction (0-1) exactly as in the data; the page shows it ×100.
- **Cost:** for ARC-AGI-1 and 2, `cost_per_task_usd` = `costPerTask` (ARC-measured). For ARC-AGI-3, the data has a `cost` field shown in the page's Cost column (for example, "$7.2K"). I recorded it as `cost_total_usd`, but its definition is not stated.
- **ARC-AGI-3 harnesses:** Standard (minimal, provider-neutral) and Provider Adapter (provider context management) are reported separately, so they are separate benchmarks here.
- **Verification:** these are Verified-leaderboard runs on the Semi-Private sets, so `self_reported=false`.
- **Competition status:** ARC Prize 2026 results will be announced Dec 4, 2026.

## Vending-Bench 2 (Andon Labs): https://andonlabs.com/evals/vending-bench-2
- **What it measures:** money balance after one simulated year running a vending business, starting from $500; arithmetic mean ± SEM across runs.
- **Data:** the page's JS bundle, which holds the full 74-model list (the HTML shows the top 10). No update date is shown.
- **Cost:** `cost_per_task_usd` = `mean_cost` per full run (1 run = 1 task), from the "Score vs. cost per run" data. That data uses list token prices without caching. The page's assumed per-Mtok prices are in `notes`, not in models.json.

## Facts I'm unsure about
- **ARC-AGI-3 Provider Adapter scores of 0.95-0.9995** (GPT-6 Astra, Gemini 4, Fable 5.2) against Standard scores of 0.4-0.8. These are surprisingly high, so recheck them on the site.
- **ARC-AGI-3 `cost` values above $10,000** (up to about $49.8K) contradict the policy's "$10,000 per run" cap. So either the field is not per-run cost or the cap was relaxed.
- **SWE-bench data stops at Feb 2026.** The site may have moved its live data elsewhere, and I couldn't check the GitHub repo (no access).
- **OSWorld 2.0 Opus 5 effort ordering is non-monotonic** (xhigh 33.33 < high 36.89 on v2.1 full). This is as published.
- **τ-bench "Avg Cost" units** (per task vs per trial) are not defined.
- **SWE-Bench Pro scaffold for unstarred rows** is inferred from the methodology text.
- **Names that differ across boards for the same model:** e.g. "Opus 5.5" (tbench), "Claude Opus 5.5 (Max)" (ARC), "claude-opus-5[1m]" (OSWorld-Verified). Matching them is left to the merge step.
