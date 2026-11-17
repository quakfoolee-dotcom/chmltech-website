# Arena (formerly LMArena) leaderboard — notes (refresh 2026-11-17)

Retrieved 2026-11-17. Pages: https://arena.ai/leaderboard/{text,webdev,vision,search,document,agent}.
Data source: official Hugging Face dataset **lmarena-ai/leaderboard-dataset** (https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset, CC-BY-4.0). **HF API lastModified 2026-11-16T04:02:23Z (commit 8013e3f0, "Update agent_tool_hallucination for 2026-11-15") — unchanged since the 2026-11-16 refresh.** All 16 `latest`-split parquets were re-downloaded fresh into /home/claude/llmrefresh2/dl/arena2/ (with api.json); every file is byte-identical to the 2026-11-16 download. Rows: category `overall`, max leaderboard_publish_date per config; each row's `notes` names its config.
Scripts: /home/claude/llmrefresh2/scripts/arena_build.py (copy of the 11-16 build, only retrieved_date changed) and /home/claude/llmrefresh2/scripts/arena_full.py (copy of content/llm/arena_full.py; only output path -> raw2/arena_full.scores.json and retrieved_date -> 2026-11-17 changed). Run with python3 -I, parquet folder as argument.

## Board update dates (leaderboard_publish_date) — no board republished since 2026-11-15
| Board (config) | Date | Models | Rows kept |
|---|---|---|---|
| Text (text_style_control / text) | 2026-11-11 | 421 | top 60 each (all 421 style-control in arena_full) |
| WebDev / Code Arena (webdev) | 2026-11-15 | 157 | top 60 (all 157 in arena_full) |
| Vision (vision_style_control / vision) | 2026-11-09 | 167 | top 60 each (all 167 in arena_full) |
| Search (both) | 2026-11-09 | 42 | all |
| Document (both) | 2026-11-09 | 46 | all |
| Agent aggregate + 5 current signals | 2026-11-15 | 65 | all |
| Agent bash_recovery_steps (retired) | 2026-10-08 | 52 | all |

Totals: arena.scores.json 918 rows; arena_full.scores.json 745 rows; arena.models.json 184 records (developer + licence only). Benchmark names identical to the previous raw/arena.scores.json (checked by script, including "Arena Agent (aggregate)"); benchmark/model/score/rank tuples identical to the previous files.

## GPT-6.2 Astra / GPT-6.2 Sol
**Not present on any board.** Searched model_name in all 16 downloaded configs for "6.2", "astra", "sol": only GPT-6 Astra (Max), GPT-6 Sol (Max), GPT-6.1 Sol (Max/Medium), GPT-5.6 Sol, Solar models. Expected: the dataset was last updated 2026-11-16, before the 2026-11-17 release. Live arena.ai pages (text, webdev, agent) return HTTP 403 (Cloudflare challenge) to curl; not bypassed, so the live page could not be checked either.

## Method (unchanged from previous notes)
Text/Vision/Search/Document/WebDev: crowdsourced anonymous pairwise votes, Bradley-Terry ratings on an Elo-like scale with 95% CI; style control (default view for Text and Vision since 16 May 2025 per dataset README) adjusts for length/markdown. Scales differ across boards. Agent Arena: models as orchestrator in Arena's Agent Mode, in-the-wild sessions, causal IPS net-improvement estimate vs a baseline mix (0 = baseline); aggregate = average of per-signal boards (Confirmed Success, Praise vs Complaint, Steerability, Bash Reliability, Tool Hallucination). Methodology: https://arena.ai/blog/agent-arena-methodology/ (not re-read this session). Limitations stated by maintainers: orchestrators only, signals may change, Arena's harness may not transfer; pairwise boards reflect Arena's voter population.

## Changes since 2026-11-16 refresh
None — the dataset has not changed. Notes from the previous refresh on Gemini 4 Hydrogen (High), Qwen4-Max (xHigh), Inkling 2 Small, K2 Horizon / Ling 3.1 Flash (absent) still apply.

## Top 5 (current)
- Text SC (11-11): Gemini 4 Carbon (High) 1526.18; Gemini 4 Argon (High) 1521.69; Muse Wonder (Max) 1510.86; Claude Opus 5.5 (High) 1506.78; Claude Fable 5 (High) 1503.98.
- WebDev (11-15): Claude Fable 5.2 (xHigh) 1825.96; Claude Opus 5.5 (Max) 1815.57; Claude Sonnet 5.5 (xHigh) 1772.23; Gemini 4 Carbon (High) 1768.34; GPT-6 Astra (Max) 1762.88.
- Agent aggregate (11-15): Claude Fable 5.2 (Max) 0.2861; Claude Opus 5.5 (Max) 0.1819; Gemini 4 Carbon (High) 0.1645; Claude Sonnet 5.5 (Max) 0.1529; Gemini 4 Hydrogen (High) 0.1491.

## Live-page check
- curl arena.ai/leaderboard/{text,webdev,agent} on 2026-11-17: HTTP 403 (Cloudflare challenge). Not bypassed. Values come from the dataset only.
- Previous session's WebFetch copies were stale (Sept/Oct snapshots); not repeated.

## Not extracted
Category sub-boards, factuality boards, image/video arenas.

## Facts I am unsure about
- Whether the live page currently shows these exact numbers, or already lists GPT-6.2 models (not verifiable: 403).
- Unit of cost_per_task_p50 (dollar sign seen on a stale page copy in an earlier session; not confirmed against the column). cost_per_task_usd stays null.
- Search/Document default view (style control or raw) not stated.
- Tool Hallucination top ranks share an identical floor value; ranks among them arbitrary.
