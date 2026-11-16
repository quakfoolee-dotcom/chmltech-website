# vendor: model specs and list prices from developers' own pages (refresh, retrieved 2026-11-16)

Files: `vendor.models.json` (122 records: the 112 from 2026-11-11, all re-checked, plus 10 new), `vendor.scores.json` (644 self-reported rows: 537 re-checked plus 107 new, all `self_reported: true`).
Scripts: /tmp/vw/scripts/build_models.py, build_scores.py, verify.py (downloads are in /tmp/vw/dl, /tmp/vw/hf, /tmp/vw/orp).

## Method for this refresh
- I fetched every source page from the 2026-11-11 file again today (94 URLs, plus new pages). Records were carried forward only after an automated check. The check confirmed that the price, context window, max output and licence values still appear on today's copy of the same page, or on the price page or JSON the value originally came from. Every mismatch was then checked by hand. None was a real change on first-party pages. The mismatches were Gemini model pages, which carry no prices (the prices come from the pricing page), Gemma context written as "256K", and a parser artefact. `model_as_listed` spellings are unchanged.
- OpenRouter rows were rebuilt from today's `api/v1/models` and `/endpoints` data.
- Score rows: each of the 537 old rows was re-checked against today's copy of its HF model card. Both the score string and the benchmark name are present for all 537. New rows cover the developer's own model only. Competitor columns were not recorded, and cells with two values were skipped (8 in the Inkling 2 Small table).

## Sources (changes since 2026-11-11 in bold)
| Source | Result | Last updated shown | Limits / not read |
|---|---|---|---|
| OpenAI `developers.openai.com/api/docs/pricing.md`, `/models/<id>.md`, changelog, deprecations | Prices unchanged. Changelog has no new text model after the Nov 5 GPT-6 Cyber entry. | none | No release dates. |
| Anthropic `platform.claude.com/docs/en/models/*.md`, overview | Unchanged. Fable 5.2 / Mythos 5.2 released Nov 9, 2026. | release dates on pages | — |
| Google: **docs moved to `aistudio.google.com/docs/...`** (ai.google.dev redirects; read via `.md`) | **New: Gemini 4 Hydrogen** ($1.50/$7.50 flat, 1,048,576 context, thinking low/medium/high/xhigh, knowledge cutoff March 2026 per model card). Carbon/Argon are still **$2/$10 introductory through 2026-11-30, then $4/$20 from 2026-12-01**. 3.8/3.6 Flash are $0.75/$3.75 through 2026-12-31, then $1.50/$7.50. **Gemini 2.5 Pro and 2.5 Flash are deprecated; their requests auto-route to 3.8 Flash and 3.5 Flash-Lite from 2026-12-01.** | "Latest update: November 2026" | No release dates on docs pages. Hydrogen's release date comes from the model card and blog (2026-11-12). The Hydrogen model card's Safety report is "available in the coming days". |
| Hydrogen model card `deepmind.google/models/model-cards/gemini-4-hydrogen/` + evals PDF (methodology URL redirects to `storage.googleapis.com/deepmind-media/gemini/gemini_4_hydrogen_model_evaluation.pdf`) | 10 self-reported benchmark rows, plus 4 blog claims (AA Index 51 high / 54 xhigh, Vals Tax 52.3%, Vals Legal 55.8%) | Published 12 Nov 2026 | Competitor values are Google's citations; not recorded. |
| xAI `docs.x.ai/developers/models/<id>` | Prices unchanged. Docs still title the company **"SpaceXSI"**. **OpenRouter labels the same models "SpaceXAI"**. x.ai returned a Cloudflare block. | none | Developer kept as "xAI" with a note. |
| Mistral `docs.mistral.ai/models/<slug>.md`, `/inference/pricing.md` | Unchanged. Medium 3.5 is deprecated (2026-10-31), retiring 2027-04-30. Large 3 is deprecated. | dates on pages | — |
| Cohere `docs.cohere.com/docs/models`, `cohere.com/pricing` | **Command A+ $2.50/$10 confirmed inside the "Command A+" card object** (adjacency concern resolved). The OpenRouter Cohere endpoint still shows $0.30/$1.50 (conflict). | — | The docs page doesn't state a licence, so it's now null on that record. |
| Amazon `aws.amazon.com/nova/pricing/` + AWS price JSON | Unchanged (Nova 2 Lite $0.30/$2.50, Pro Preview $1.25/$10, Omni Preview $0.30/$2.50) | JSON publication date still 2026-11-11 | — |
| DeepSeek pricing | Unchanged (peak $0.30/$1.20 and $1.32/$3.96; off-peak half). | — | — |
| Alibaba Model Studio pricing + QwenCloud | **New: qwen4-max / Qwen4-Max, $1.5/$4.5** (International), 1M context, 393K max output. qwen3.8-max and qwen3.8-max-0902 are still $2/$6. qwen3.7-plus is still a list price with "limited-time 20% off". | Nov 16, 2026 | **I found no retrievable developer page with Qwen4-Max benchmark claims.** qwen.ai is client-rendered, x.com is blocked, HF Qwen/Qwen4-* returns 401, and the QwenLM GitHub org can't be listed from this session. Search results were secondary sites only, so no Qwen4-Max scores were recorded. Effort levels (low/high/xhigh) are not stated on the pricing pages. OpenRouter's endpoint name `qwen4-max-20261115` suggests a 2026-11-15 snapshot. |
| Moonshot, Z.ai, MiniMax pricing | Unchanged. Kimi K2 series is closed to new users from 2026-10-31, with retirement planned. | — | — |
| Meta `dev.meta.ai/docs/*` | Unchanged. Muse Wonder is still preview. | — | — |
| Hugging Face cards/API | **New:** Inkling-2-Small (Thinking Machines, Apache 2.0, 594B/17B, 1M), Ling-3.1-flash-1019 (MIT, 560B/25B, 1M), K2-Horizon-375B-A23B (org "IFM", Apache 2.0, 375B/23B, 512K). | repo dates not used as release dates | `inclusionAI/Ling-3.2-flash` returned 401. The ifm.ai blog returned 403, so K2-Horizon's link to MBZUAI/LLM360 is not confirmed. The only clue is that its W&B logs sit under "llm360". |
| OpenRouter (secondary) | **Listed-price changes:** gpt-oss-20b $0.03/$0.13 → $0.075/$0.30 (now matches Groq). Gemma 4 26B A4B $0.08/$0.10 → $0.0675/$0.225 (NextBit). Nemotron 3.5 Super VL $0.15/$0.47 → $0.15/$0.50. Granite 4.2 8B $0.06/$0.25 → $0.06/$0.15. **New:** Qwen4 Max, Inkling 2 Small ($0.30/$1.00), Ling 3.2 Flash (free only, 2026-11-13). | — | The model-level price is the default listed endpoint. These changes reflect which provider is the default, not a developer price change. |

## Status changes
- New GA: Gemini 4 Hydrogen (Google, 2026-11-12).
- New: Qwen4-Max (Alibaba), Inkling 2 Small (Thinking Machines, open weights), Ling-3.1-flash-1019 (inclusionAI snapshot), Ling 3.2 Flash (free preview on OpenRouter only).
- Deprecations seen: Gemini 2.5 Pro/Flash (auto-route 2026-12-01); OpenAI gpt-5/o3 family shutdown Dec 11, 2026 (already listed); Mistral Medium 3.5 and Large 3 (deprecated 2026-10-31).
- Expiring prices: Gemini 4 Carbon/Argon intro price ends 2026-11-30; Gemini 3.8/3.6 Flash intro price ends 2026-12-31; GPT-6 Astra for Law promotional pricing runs "at least through December 31, 2026"; qwen3.7-plus is limited-time 20% off.
- No renames on first-party pages. The xAI/"SpaceXSI"/"SpaceXAI" naming is unresolved.

## Things I am unsure about
1. The developer behind K2-Horizon ("IFM"; MBZUAI/LLM360 unconfirmed).
2. Qwen4-Max release date and effort levels (not on the pages I read).
3. Whether Gemini 4 Carbon/Argon should switch to the 2026-12-01 price ($4/$20) for the site. Recorded: current $2/$10.
4. The Cohere price conflict between cohere.com and OpenRouter persists.
5. The 537 carried-over score rows were re-checked only by string presence (score and benchmark name in the card), not by full table re-parse.
6. Inkling 2 Small context: the card says "up to 1M tokens" (recorded 1,000,000). OpenRouter says 1,048,576.
7. The old open questions (DeepSeek peak vs off-peak, Beam context, MiniMax parameters) are unchanged.
