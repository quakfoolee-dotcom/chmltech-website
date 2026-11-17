# Agentic benchmarks: source notes (prefix `agentic`), refresh 2026-11-17

Retrieved 2026-11-17 with `curl` (HTTPS proxy, TLS verified) into a fresh directory /home/claude/llmrefresh2/dl/agentic2/. Parser scripts: /home/claude/llmrefresh2/scripts/agentic2_*.py (run with `python3 -I`), adapted from the 2026-11-16 scripts. Assembly and diff: agentic2_assemble.py. Same sources, endpoints and selection rules as the previous collection. All 26 previous benchmark names are kept exactly (checked by script: none missing, none extra). `agentic.models.json` is empty because these boards publish no model specs. **1,483 score rows** (previously 1,427).
I rebuilt every board from fresh downloads and diffed the result against content/llm/raw/agentic.scores.json. **Only Terminal-Bench 4.1 and ARC-AGI changed.** Every other board came out identical. Most of their data files are byte-identical to the 2026-11-16 downloads (OSWorld 2.0 JSON, BFCL CSV, Aider YAML, METR YAML, τ manifest and all 46 submissions, Vending-Bench 2 JS chunks, SWE-bench embedded JSON).

## SWE-bench (Verified, Multilingual): https://www.swebench.com/
- **Data:** embedded `leaderboard-data` JSON. It is identical to before.
- **Newest entries:** Verified 2026-02-26, Multilingual 2026-02-20. The board is stale and shows no "last updated" date.
- **Selection:** unchanged: the Verified top 50 by score (non-mini rows go to the full-leaderboard benchmark), mini-SWE-agent rows from 2025-07 on, and all Multilingual rows.
- **Cost:** `cost_per_task_usd` = instance_cost; `cost_total_usd` = cost. A value of 0 means unknown.
- **Rows:** 34 + 47 + 13.

## SWE-Bench Pro (Scale): https://labs.scale.com/leaderboard/swe_bench_pro
- **Data:** RSC flight `variants`: Public 731 tasks (25 rows) and Private 276 tasks (14 rows). Numbers are unchanged; newest createdAt is 2026-07-09.
- **Changed:** the page tab labels are now just "Public" and "Private" (were "SWE-Bench Pro (Public Dataset)" / "(Private Dataset)"). I kept the previous benchmark names. The parser also had to be adjusted because `variants` is no longer the first key of its object.
- **Scaffold:** `*` = mini-swe-agent; SWE-Agent for unstarred rows is inferred from the methodology text.
- **Cost:** none shown.

## Terminal-Bench 4.1: https://www.tbench.ai/
- **Data:** RSC flight rows of leaderboard 947c0b13 ("Terminal-Bench 4.1"), record updated_at 2026-11-17T17:27. 63 rows (was 59), all with n_trials 330.
- **Score and cost:** accuracy with 95% CI half-width; `cost_total_usd` = total_cost_usd for the whole run. Effort = reasoning_effort; scaffold = agent_display.
- **New rows (created 2026-11-16):**
  - **Copilot Fusion** (GitHub Copilot, max): 71.21% ± 2.88, $1,987.33, date Nov 17, 2026. It is now **rank 1**. **This is a router/product, not a model.** Its link goes to docs.github.com/en/copilot/concepts/models/copilot-fusion (retrieved). That page says: "Copilot Fusion is an intelligent runtime model router and orchestrator". It picks models and a single/cascade/critique pattern for each task, and its model pool changes over time. "max" means Fusion Max. Flagged in the row notes; the merge step should probably keep it out of model rankings.
  - **Ember-1** (Fireworks, mini-swe-agent, none): 21.82%, $4,718.49, dated 2026-09-24.
  - **Hy4 Preview** (Tencent, Claude Code, max): 19.09%, $658.09, dated 2026-08-28.
  - **Gemini 3.1 Pro** (Antigravity CLI, high): 2.73%, $3,651.15, dated 2026-02-19 (an older model newly posted).
- **Re-ranking:** every older row moved down 1 to 4 places; their scores and costs are unchanged. Opus 5.5 and Fable 5.2 are now tied at rank 2.
- **Other agent names:** Claude Code, Codex, Antigravity CLI, Grok Build, Muse Code and mini-swe-agent are agent harnesses and sit in `scaffold`. The models in those rows are real models.
- **Cost exception:** Muse Spark 1.3 shows $0, so its cost is null.
- **GPT-6.2:** none of these rows are GPT-6.2 Astra or Sol.
- **Verification:** the board does not mark verified vs submitted rows (self_reported=false, with a caveat).

## OSWorld 2.0: https://osworld-v2.xlang.ai/
- **Data:** `static/data/leaderboard/official-results.json`. It is byte-identical; updatedAt 2026-11-14.
- **Task releases:** v2026.06.24 (default), v2026.08.08 and v2.1, recorded in `notes`.
- **Cost:** `cost_total_usd` = estimatedCostUsd.
- **Rows:** 56 + 56. No GPT-6.2 and no Gemini rows.

## OSWorld-Verified: https://os-world.github.io/ (redirects to osworld-v1.xlang.ai)
- **Data:** the verified xlsx and self-reported xlsx are unchanged (same sheets and row counts, identical rows). Newest verified date is 2026-08-01.
- **Rows:** top 60 plus 3 self-reported Screenshot entries.

## τ-bench / τ²-bench / τ³: https://taubench.com/
- **Data:** S3 manifest `submissions/manifest.json`: 30 current + 16 legacy submissions. It and all 46 submission.json files are byte-identical.
- **Newest submission:** 2026-10-20 (Cortex 0.1).
- **Overall:** the τ² overall top 3 is taken from the homepage as before.
- **Cost:** `cost_per_task_usd` = per-domain "cost" ("Avg Cost"). Its unit is undefined except in Cortex's own methodology note.
- **Not extracted:** voice boards.

## BFCL V4: https://gorilla.cs.berkeley.edu/leaderboard.html
- **Data:** `data_overall.csv` is identical; "Last Updated: 2026-04-12".
- **Rows:** top 60 Overall / Multi Turn / Web Search. `cost_total_usd` = Total Cost ($). The board is stale.

## Aider Polyglot: https://aider.chat/docs/leaderboards/
- **Status:** the page says "last updated November 20, 2025". The newest entry is 2025-10-03 (stale).
- **Data:** the GitHub YAML (raw.githubusercontent.com/Aider-AI/aider/main/aider/website/_data/polyglot_leaderboard.yml) is identical. 56 rows.

## METR Time Horizons 1.1: https://metr.org/time-horizons/
- **Status:** the page still says "no longer actively updated", LAST UPDATED September 8, 2026.
- **Data:** `assets/benchmark_results_1_1.yaml` is identical. 14 models × p50/p80; display names were re-checked against the page.

## ARC-AGI (1, 2, 3): https://arcprize.org/leaderboard
- **Data:** RSC `groups` with `$` references resolved; entries with display=false are skipped (unchanged rule). 125 groups (was 121). Newest release date is **2026-11-17**.
- **New rows: GPT-6.2 Astra and GPT-6.2 Sol (OpenAI, release 2026-11-17).** Each has 5 efforts (Low, Medium, High, XHigh, Max) on ARC-AGI-1, ARC-AGI-2, ARC-AGI-3 Standard and ARC-AGI-3 Provider Adapter: 40 rows. These match the same-day openai62 lead rows exactly.
- **Cost for GPT-6.2:**
  - ARC-AGI-1/2: `cost_per_task_usd` = costPerTask, given at every setting.
  - ARC-AGI-3: only `cost` is given, recorded as `cost_total_usd`.
  - The Sol entries carry the board note "Partial dataset coverage: scores use full catalog denominators; costs include recorded usage only, excluding unrecorded attempts", copied into notes.
- **Selected GPT-6.2 values:**
  - Astra (Max): ARC-AGI-1 0.985 at $0.3505/task; ARC-AGI-2 0.9583 at $0.9695/task; ARC-AGI-3 Standard 0.7031 at cost $24,168.91; Provider Adapter 0.9980 at $4,106.96.
  - Sol (Max): ARC-AGI-1 0.975 at $0.1060/task; ARC-AGI-2 0.8583 at $0.2611/task; ARC-AGI-3 Standard 0.5493 at $5,466.21; Provider Adapter 0.9821 at $1,494.19.
- **Mercury 3 Preview (Inception, release 2026-10-19), newly listed:**
  - ARC-AGI-1/2 at four efforts: Instant, Low, Medium, High.
  - ARC-AGI-3 Standard and Provider Adapter at High only.
  - 12 rows in all.
- **Inkling 2 Small (XHigh):** its ARC-AGI-1 and ARC-AGI-2 rows were **already present** (unchanged). Its **ARC-AGI-3 Standard (0.00297, cost $857.92) and Provider Adapter (0.0255, $703.94) rows are new.** Release date 2026-11-05.
- **Developer:** the provider displayName.

## Vending-Bench 2 (Andon Labs): https://andonlabs.com/evals/vending-bench-2
- **Data:** runs data from JS chunk Bl9fFL93.js and the cost table and "New" list from nodes/26.CDA-0jog.js. Both are byte-identical to the 2026-11-16 downloads (same chunk hashes on the page). 76 models.
- **New list:** "New" = Gemini 4 Argon, Gemini 4 Carbon, Gemini 4 Hydrogen, GPT-6.1 Terra, GPT-6.1 Sol, Claude Fable 5.2. No GPT-6.2 entry.
- **Cost:** `cost_per_task_usd` = mean cost per full run (list prices, no caching). The board shows no update date.

## Leads checked (2026-11-17)
- **GPT-6.2 Astra / Sol:** present only on ARC-AGI (40 rows). They are not on Terminal-Bench 4.1, SWE-bench, SWE-Bench Pro, OSWorld 2.0/Verified, τ, BFCL, Aider, METR or Vending-Bench 2 (searched all downloads).
- **Inkling:** the Terminal-Bench "Inkling Small 2" row (xhigh, 13.03%) is unchanged. Whether it is the same model as ARC's "Inkling 2 Small" is left to the merge step.

## Facts I'm unsure about
- **Copilot Fusion:** a router whose underlying models vary. Its 71.21% is not attributable to any single model.
- **ARC-AGI-3 "cost":** the definition is not stated. GPT-6.2 Astra Standard-harness costs ($24K–$29K) exceed the $10K per-run cap mentioned in ARC policy, as some earlier rows already did.
- **ARC-AGI-3 Provider Adapter scores:** GPT-6.2 Astra scores 0.95–1.0 (XHigh = 1). These are reported as shown.
- **GPT-6.2 Sol coverage:** costs cover recorded usage only, per the board's note (partial coverage).
- **Terminal-Bench ranks:** they shift each time rows are inserted. They are recorded as shown on 2026-11-17.
- **Unchanged caveats:** undefined τ "Avg Cost" units; SWE-Bench Pro scaffold for unstarred rows is inferred; τ² overall Gemini 3.0 Pro self_reported kept true; SWE-bench, BFCL, Aider and METR are stale.
