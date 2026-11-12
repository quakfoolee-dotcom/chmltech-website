# Arena (formerly LMArena) leaderboard — notes

Retrieved 2026-11-11. Public pages: https://arena.ai/leaderboard (boards at /leaderboard/text, /webdev, /vision, /search, /document, /agent).
Data source: the official Hugging Face dataset **lmarena-ai/leaderboard-dataset** (https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset, CC-BY-4.0, published by lmarena-ai; HF API shows lastModified 2026-11-11T04:01Z). Its README says it holds "Historical snapshots of the Arena (https://arena.ai/leaderboard) leaderboard". Each board is a config with a `latest` split (the current published board) and a `full` split (all history). Every row in arena.scores.json names its config in `notes`; all rows use the `latest` split, category `overall`.

## Board update dates (leaderboard_publish_date in the latest split)
| Board (config) | Date | Models in board | Rows kept |
|---|---|---|---|
| Text (text_style_control / text) | 2026-11-09 | 421 | top 60 each |
| WebDev / Code Arena (webdev) | 2026-11-10 | 156 | top 60 |
| Vision (vision_style_control / vision) | 2026-11-09 | 167 | top 60 each |
| Search (search_style_control / search) | 2026-11-09 | 42 | all |
| Document (document_style_control / document) | 2026-11-09 | 46 | all |
| Agent aggregate + 5 current signals | 2026-11-08 | 57 | all |
| Agent bash_recovery_steps (retired signal) | 2026-10-08 | 52 | all |

## Which Text board is the default on arena.ai
The **style-controlled** board (`text_style_control`) is the default. Evidence: (1) README: "On May 16, 2025, style control was made the default for text and vision arenas and the offset was adjusted to put the style control leaderboard on the same rating scale as non style control." (2) Cross-check: the only copy of https://arena.ai/leaderboard/text I could read (WebFetch, page dated "Mar 5, 2026") shows #1 1504 ±7 (8,945 votes), #2 1500 ±9 (4,042), #3 1500 ±7 (8,073), #4 xAI 1493 ±8 (5,071), #5 1485 ±4 (39,673). These match `text_style_control` 2026-03-05 exactly (claude-opus-4-6 1503.95, gemini-3.1-pro-preview 1500.14, claude-opus-4-6-thinking 1500.04, grok-4.20-beta1 1492.55, gemini-3-pro 1485.38) and do NOT match raw `text` (where grok-4.20-beta1 is 6th at 1464.56). The same applies to Vision. For Search and Document the default view is not stated; both variants are included.
Current #1 Text (style control): Gemini 4 Carbon (High) 1525.95 (CI 1516.36–1535.55, 4,282 votes).

## Live-page cross-check — could NOT verify current numbers
- curl of arena.ai/leaderboard/text and lmarena.ai/leaderboard/text: HTTP 403 Cloudflare "Just a moment..." challenge (also saved dl/arena/live.html is the same challenge page). Not bypassed per rules.
- WebFetch returns stale cached copies: arena.ai/leaderboard (rank-only table, early 2026 models), lmarena.ai/leaderboard (2025 models), arena.ai/leaderboard/text dated Mar 5, 2026, arena.ai/leaderboard/agent dated Jul 12, 2026.
- Those stale pages match the dataset's historical snapshots (Text 2026-03-05 as above; Agent page top rows Claude Fable 5 (High) 13.94% ±1.56%, 16,059; GPT 5.6 Sol (xHigh) 10.94%; match `agent` full split 2026-07-13: 0.139412, CI 0.12386–0.154964, 16,059 sessions; 0.109384). This confirms the dataset is the page's own data and that agent scores are displayed as score×100 %.
- One mismatch: the Mar 5 Text page shows a #7 OpenAI model 1480 ±12 with 2,290 votes that I could not find in the 2026-03-05 snapshot (possibly a model added to the page between dataset publishes, or a later-removed entry).
- So the November 2026 values are from the dataset only, not checked against the live page.

## What each board measures (method)
- **Text / Vision / Search / Document / WebDev**: crowdsourced anonymous pairwise battles; users vote for the better response. Scores are Bradley-Terry ratings on an Elo-like scale (Elo replaced by Bradley-Terry Jan 9, 2024; frequency re-weighting since Jul 23, 2025). `rating_lower/upper` = confidence bounds; `vote_count` = battles for the model. Style control adjusts for response length/markdown formatting so ratings reflect substance rather than style. Vision = prompts with images; Search = search-grounded answers (models with web search, e.g. "(Search)", "(Grounding)"); Document = prompts with uploaded documents; WebDev (Code Arena, launched on the site Nov 12, 2025) = building web apps; its `overall` and `webdev` categories are identical. Rank in the dataset is a plain sequential rank (the raw `text` config stores it as float).
- Scores on different boards are not on a common scale (Text ~1500, Vision ~1300, Search ~1250, WebDev ~1800).
- **Agent Arena** (launched Jun 4, 2026; methodology https://arena.ai/blog/agent-arena-methodology/ published 4 Jun 2026, updated 15 Oct 2026; signal definitions https://arena.ai/resources/agent-arena-signals): ranks models acting as the **orchestrator** in Arena's own Agent Mode (arena.ai/agent) using millions of in-the-wild user sessions, not a synthetic benchmark. Configurations are randomised and each model's effect is estimated causally with a self-normalised inverse-propensity-score (IPS) estimator: score τ̂ = estimated net improvement in an outcome relative to a baseline (roughly uniform) mix of models; 0 ≈ baseline, negative = worse than baseline. 95% CI = τ̂ ± 1.96·SE. Time-decaying weights favour recent data. "We compute the per-signal leaderboards separately, then average them at the end" (weights not stated). Signals:
  - *Confirmed Success (task_outcome_explicit)*: share of tasks where the user explicitly answers yes to "Did this complete your task?".
  - *Praise vs Complaint*: task succeeds if unprompted praise outnumbers complaints; ties/no sentiment not scored.
  - *Steerability*: how much user correction each assistant turn needs (None/Low/High); less steering is better (the dataset score is a net improvement where higher = better).
  - *Bash Reliability*: share of agent-caused bash failures (mistyped flags, bugs in its own scripts); outside errors exempt. Replaced *Bash Recovery* on Oct 12, 2026 — the `agent_bash_recovery_steps` config is the retired signal, last published 2026-10-08, included for reference only.
  - *Tool Hallucination*: calls to tools not registered in the agent's toolset, or claims of capabilities it lacks.
  - Aggregate config also has `session_count`, `cost_per_task_p50` and `output_tokens_per_task_p50`. Methodology says realised per-session cost is used "to assess Pareto optimality" and that some models cost more in practice than list price suggests. The **currency/unit of cost_per_task_p50 is not stated anywhere I could read**, so `cost_per_task_usd` is null; the raw value is in each aggregate row's notes (e.g. Claude Opus 5.5 (Max) 6.305717, GPT-6 Luna (Max) 0.085786).
- Limitations stated by maintainers: Agent leaderboards currently evaluate orchestrators only; signal set is "a starting point" and may change; signals come from Arena's own harness, so results may not transfer to other agent tools. Pairwise boards reflect preferences of Arena's voting population.

## models.json
181 records: one per distinct model in the rows kept, with only developer (dataset `organization`, lowercase as listed) and licence. access = "Proprietary API" when licence is "Proprietary", otherwise "Open weights" with the licence name ("Non-commercial" left null). All other fields null — Arena gives no prices/specs.

## Not extracted
Category sub-boards (coding, math, hard_prompts, languages, industries…), text/search factuality boards, image/video arenas (not downloaded / out of scope).

## Facts I am unsure about
- That the current (Nov 2026) live page shows exactly these numbers — not verifiable (Cloudflare 403).
- Whether Search and Document default to style control on the site.
- Unit of `cost_per_task_p50` (very likely USD median per task, but not stated).
- Agent Tool Hallucination: the top several models share an identical score and CI (0.009222, CI 0.008434–0.010011) — looks like a floor/pooled value; ranks among them are arbitrary.
- Sign convention of aggregate vs signals beyond "higher rank = better".
- Dates: the agent page said "Jul 12, 2026" while the matching dataset snapshot is 2026-07-13 (likely timezone/publish lag).
- Some models have the same name with different variants on different boards (e.g. Qwen3.8-Max vs Qwen3.8-Max (0902) on WebDev; Claude Opus 5.5 (High) on Text vs (Max) on Agent/WebDev) — kept exactly as listed.
