# index: composite / independent evaluation sources (retrieved 2026-11-11)

Build script: /tmp/claude-0/-home-claude/d3bf24a8-f4d5-58c8-80f2-561c5348c5f5/scratchpad/work_index_build.py
WebFetch was refused for every URL in this session (the permission prompt timed out). All pages were fetched with curl or came from the pre-downloaded files, and each public URL returned HTTP 200 to curl.

## Artificial Analysis (artificialanalysis.ai)
- **What it measures.** The Intelligence Index **v5.0.1** ("November 2026 to current"; v5.0 ran Oct to Nov 2026) is a weighted average of 4 categories at 25% each:
  - Knowledge Work: AA-Briefcase v1.1 15%, AutomationBench-AA 5%, GDP.pdf 5%
  - Coding: FrontierCode-AA 2.0 15%, Terminal-Bench 4.0 10%
  - Science: Terminal-Bench-Science 0.1 15%, CritPt v2 Hard 10%
  - General: AA-Omniscience v1.1 15% (Accuracy 10% plus 1 minus Hallucination 5%), HLE-Diamond 10%
  - Source: https://artificialanalysis.ai/methodology/intelligence-benchmarking
- **Cost per Task.** "Weighted average cost (USD) per Intelligence Index task". It covers contestant model calls only: no judge calls, PDF preparation or OCR. It uses token counts reported by the provider, combined with live cache-hit rates.
- **Time per Task.** Estimated from output tokens and output speed. It is not end-to-end timing. Page data is in seconds; the table shows minutes.
- **Source of the rows.** All rows come from the Next.js flight data on https://artificialanalysis.ai/leaderboards/models. I took the 106 non-deprecated models that have an index score. Those values are full precision; the table rounds them (for example 64.56 is shown as 65 and $26.5386 as $26.54).
- **Model specs.** Prices, context window and reasoning flags in index.models.json come from AA. They are secondary, and the page does not say which provider each price belongs to. Release dates are filled only where an AA release record has the same slug (50 of 106).
- **Coding Agent Index (36 agent+model pairs).** Taken from the home page https://artificialanalysis.ai/.
  - The score is on a 0-1 scale and covers 3 evals: FrontierCode v1.1 Main, SWE-Atlas QnA and Terminal-Bench v4.
  - The cost is the "average pay-per-token API cost per task". The Muse Code (Meta) entries have a null cost.
- **Output speed** is in tokens/s, from the same leaderboard data.
- **Not used.** The home page has a 26-model array with fields `score`, `refusalRate`, `mitigationStatus` and `costPerTask` and no title I could find. It is probably the Cyber Index, but I could not confirm that, so it was not output. The Decision Index contestant list was also skipped because it is not an LLM general index.
- **Last updated.** The page shows no explicit date beyond the version history.

## Epoch AI Benchmarking Hub (https://epoch.ai/benchmarks; data at https://epoch.ai/data/benchmark_data.zip)
- **Last updated.** The hub shows "Updated Nov. 11, 2026". The ECI moved to a Bayesian model on Nov 4, 2026. The Claude Fable 5.2 record (Nov 9) comes from pre-launch testing on Epoch's own benchmarks only, and Epoch says it "may change".
- **Rows output.**
  - ECI, with its credible interval.
  - Epoch-run FrontierMath Tiers 1-3 v2, FrontierMath Tier 4 v2, GPQA Diamond and SWE-bench Verified. These are mean_score on a 0-1 scale with stderr.
  - Only models released on or after 2025-05-01 are included (the 18-month scope rule, applied by the release date in the file).
- **Naming.** `model_as_listed` is Epoch's model-version id (for example `claude-fable-5-2_max`). The display name is in notes.
- **No cost data** in these files.
- **Not used.** External-benchmark CSVs (hle_external, metr, etc.) were left out because the task named only Epoch's own composites.

## Vals AI (https://www.vals.ai/benchmarks/vals_index)
- **What it measures.** Vals Index **v2.2**, updated 2026-11-09, 36 models. It is agentic finance, coding, legal and tax tasks weighted by each sector's share of U.S. GDP. The component sets are listed in the notes of each row.
- **Cost.** `cost_per_task_usd` is Vals' `cost_per_test` field from the page's embedded props. The page shows it as "Cost / Test". Beam 1.0 has a null cost.
- **Naming.** Models are listed by Vals id (for example `anthropic/claude-fable-5-2`).

## Vectara Hallucination Leaderboard (https://raw.githubusercontent.com/vectara/hallucination-leaderboard/main/README.md)
- **What it measures.** The hallucination rate when summarizing documents, judged by HHEM. "Last updated on October 22, 2026".
- **Rows output.** All 111 table rows. The leaderboard gives no release dates, so older models are included and should be filtered downstream.
- **Access.** github.com returned 403 to curl; the raw README matched the downloaded copy exactly.

## LiveBench 2.0 (https://livebench.ai/, data https://livebench.ai/data/20261106/)
- **How the source was identified.** The lb/*.csv files are LiveBench. The JS bundle attributes them to "LiveBench 2.0", fetches `./data/<release>/table.csv|cost.csv|llm_time.csv`, and lists the 2.0 releases 20261014, 20261025 and 20261106. The live files are byte-identical to the downloads. The 2026-06-25 "files" are GitHub Pages 404 pages, and v1_table.csv is old LiveBench v1, so neither was output.
- **What the columns are.**
  - table.csv holds scores: the mean task score (0-100) per suite, from a single run.
  - llm_time.csv holds **seconds in LLM calls per task**, per the site tooltip. It is put in the notes of each row.
  - cost.csv holds the **total USD per suite**, with `nq_*` task counts. The site computes cost per task as total ÷ tasks. I did not do that division (no own arithmetic), so `cost_per_task_usd` is null and `cost_total_usd` is the cell value.
- **Overall score** is computed client-side, so it was not output.
- **Naming.** Display names, organisations and effort labels come from the JS model map. One model, "inkling", has no entry.

## Humanity's Last Exam (https://lastexam.ai)
- The live results load client-side ("Loading HLE results..."). The static fallback table is stale: "Dataset Updated: April 3rd, 2025", with models such as GPT-5 and Gemini 3 Pro. **No rows output.** HLE-Diamond was released on 09/22/2026.

## OpenRouter rankings (https://openrouter.ai/rankings)
- The page renders client-side, and the text holds only navigation. Usage share is not a capability score. **No rows output.**

## Facts I am unsure about
- The AA "Cost per Task" weighting: the page says "weighted average", which I take to mean weighted like the index. I did not confirm that.
- The AA Coding Agent Index has no update date, and I could not see an index version.
- In Vals, `cost_per_test` is assumed to be USD per test, based on the "Cost / Test" label. Some rows have a compute_effort setting and others a reasoning_effort setting.
- LiveBench's notes say "every suite counts equally", but categories.json has `_overall_weights` (Long Agentic 2.0, Coding 1.5, Design 1.5). The two conflict.
- LiveBench's notes say Claude Fable 5.2 is shown at xhigh, while table.csv keeps the id `claude-fable-5.2`.
- AA and Vals cost-per-task figures are not comparable: they use different task sets and harnesses.
