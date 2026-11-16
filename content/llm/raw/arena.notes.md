# Arena (formerly LMArena) leaderboard — notes (refresh)

Retrieved 2026-11-16. Pages: https://arena.ai/leaderboard/{text,webdev,vision,search,document,agent}.
Data source: official Hugging Face dataset **lmarena-ai/leaderboard-dataset** (https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset, CC-BY-4.0). HF API lastModified 2026-11-16T04:02:23Z (commit 8013e3f0). All rows from the `latest` split, category `overall`, filtered to the max leaderboard_publish_date; each row's `notes` names its config. Build script: /home/claude/llmrefresh/scripts/arena_build.py; full-board rows (arena_full.scores.json) from a copy of content/llm/arena_full.py at /home/claude/llmrefresh/scripts/arena_full.py (only output path and retrieved_date changed). Parquets in /home/claude/llmrefresh/dl/arena/.

## Board update dates (leaderboard_publish_date)
| Board (config) | Date | Models | Rows kept |
|---|---|---|---|
| Text (text_style_control / text) | 2026-11-11 | 421 | top 60 each (all 421 style-control in arena_full) |
| WebDev / Code Arena (webdev) | 2026-11-15 | 157 | top 60 (all 157 in arena_full) |
| Vision (vision_style_control / vision) | 2026-11-09 (unchanged) | 167 | top 60 each (all 167 in arena_full) |
| Search (both) | 2026-11-09 (unchanged) | 42 | all |
| Document (both) | 2026-11-09 (unchanged) | 46 | all |
| Agent aggregate + 5 current signals | 2026-11-15 | 65 | all |
| Agent bash_recovery_steps (retired) | 2026-10-08 | 52 | all |

Totals: arena.scores.json 918 rows; arena_full.scores.json 745 rows; arena.models.json 184 records (developer + licence only).

## Method (unchanged from previous notes)
Text/Vision/Search/Document/WebDev: crowdsourced anonymous pairwise votes, Bradley-Terry ratings on an Elo-like scale with 95% CI; style control (default view for Text and Vision since 16 May 2025 per dataset README) adjusts for length/markdown. Scales differ across boards. Agent Arena: models as orchestrator in Arena's Agent Mode, in-the-wild sessions, causal IPS net-improvement estimate vs a baseline mix (0 = baseline); aggregate = average of per-signal boards (Confirmed Success, Praise vs Complaint, Steerability, Bash Reliability, Tool Hallucination). Methodology: https://arena.ai/blog/agent-arena-methodology/ (not re-read this session). Limitations stated by maintainers: orchestrators only, signals may change, Arena's harness may not transfer; pairwise boards reflect Arena's voter population.

## New since 2026-11-11 refresh
- **Gemini 4 Hydrogen (High)** (google): Text SC #15 1490.43 (CI 1481.42-1499.44, 4,741 votes); Text raw #8 1502.12; WebDev #11 1703.90 (2,046 votes); Agent aggregate **#5** 0.1491 (CI 0.1302-0.1679, 8,639 sessions); Steerability #2; Praise #4; Confirmed Success #5; Bash Reliability #46; Tool Hallucination #36. Not on Vision/Search/Document (those boards not republished since 11-09).
- **Qwen4-Max (xHigh)** (alibaba): WebDev **#6 1749.81** (CI 1734.35-1765.28, 1,814 votes) — consistent with Alibaba's "1750" claim when rounded; Agent aggregate #14 **0.0746** (CI 0.0612-0.0880; displayed on arena.ai as ~7.46%, i.e. consistent with a claimed "7.5"). NOT on the Text board (2026-11-11) nor Vision/Search/Document.
- Other new Qwen: none besides Qwen4-Max. Qwen3.6-Max-Preview dropped out of the Text top 60 (still in the full board).
- **Inkling 2 Small**: WebDev #24 1644.68 (1,077 votes); Agent aggregate #23 0.0251; Text SC #152 1411.78 (only in arena_full). (Distinct from older "Inkling" and "Inkling-Small".)
- **K2 Horizon 375B A23B** and **Ling 3.1 Flash 1019**: NOT found in any downloaded config (searched for Horizon/375B/Ling 3/1019). Only Ling-flash-2.0 (Text SC #236) exists.
- Also new to the kept rows: Claude Fable 5.2 (Max) (Agent #1, 0.2861), GPT-6.1 Sol (Medium), GPT-6.1 Terra (Medium).

## Top 5 (current)
- Text SC (11-11): Gemini 4 Carbon (High) 1526.18; Gemini 4 Argon (High) 1521.69; Muse Wonder (Max) 1510.86; Claude Opus 5.5 (High) 1506.78; Claude Fable 5 (High) 1503.98.
- WebDev (11-15): Claude Fable 5.2 (xHigh) 1825.96; Claude Opus 5.5 (Max) 1815.57; Claude Sonnet 5.5 (xHigh) 1772.23; Gemini 4 Carbon (High) 1768.34; GPT-6 Astra (Max) 1762.88.
- Agent aggregate (11-15): Claude Fable 5.2 (Max) 0.2861; Claude Opus 5.5 (Max) 0.1819; Gemini 4 Carbon (High) 0.1645; Claude Sonnet 5.5 (Max) 0.1529; Gemini 4 Hydrogen (High) 0.1491.

## Live-page check — dataset is NEWER than any page copy I could read
- curl arena.ai/leaderboard/{text,webdev,agent}: HTTP 403 (Cloudflare challenge). Not bypassed.
- WebFetch /webdev: failed (client_error).
- WebFetch /text: returned a table without model names (provider/licence only): #1 Anthropic 1507 ±5 27,189 votes; #2 1505 ±4 72,099; #3 1504 ±11 2,906 ... These match the **2026-09-02** text_style_control snapshot in the `full` split (claude-fable-5 1507.16, 27,189; claude-opus-4-6-high 72,099; claude-fable-5.1-max 2,906) — a stale cache.
- WebFetch /agent: table without names/headers; session counts 10,551 / 13,168 / 16,374 / 30,489 match the **2026-10-16** agent snapshot (Claude Opus 5.5 (Max), GPT-6 Astra (Max), Claude Fable 5.1 (Max), Gemini 4 Argon (High)) — stale cache. That page shows a cost column formatted in dollars (e.g. "$6.13") and a list-price column ("$4 / $20"), suggesting cost_per_task_p50 is USD, but the full split has no cost values for 2026-10-16 so I could not tie the "$" figure to the dataset column. cost_per_task_usd stays null; raw values remain in aggregate-row notes.
- So November values come from the dataset only.

## Not extracted
Category sub-boards, factuality boards, image/video arenas.

## Facts I am unsure about
- Whether the live page currently shows these exact numbers (not verifiable).
- Unit of cost_per_task_p50 (dollar sign seen on stale page copy; not confirmed against the column).
- Search/Document default view (style control or raw) not stated.
- Tool Hallucination top ranks share an identical floor value; ranks among them arbitrary.
- Text board count is still 421 though Gemini 4 Hydrogen was added (some other model presumably removed; not investigated).
