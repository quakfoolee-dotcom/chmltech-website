# vendor — model specs and list prices from developers' own pages (retrieved 2026-11-11)

Files: `vendor.models.json` (112 records, ~70 distinct models from 26 developers), `vendor.scores.json` (537 self-reported benchmark rows, all `self_reported: true`).
Build script: `scratchpad/llm/vdl/build_vendor.py` (table parser `vdl/tables.py`).

Method: one record per model per source page. Open-weight models usually have two records, a Hugging Face model-card record (licence, parameters, context) and a pricing record (developer API page, or OpenRouter). Nothing is merged across pages. Prices are standard, non-batch, non-cached list prices per 1M tokens. Tiering, cache, peak/off-peak and promotional terms are in `price_notes`.

## Sources

| Source | What it gives | Last updated shown | Limitations / what I could not read |
|---|---|---|---|
| OpenAI model pages `developers.openai.com/api/docs/models/<id>` and `/api/docs/pricing` | Specs and price for GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna, GPT-6 Sol, GPT-6-Cyber; pricing-page-only rows for gpt-5.6-sol/terra/luna, gpt-5.5, gpt-5.5-pro | none shown | No release dates on the model pages. `llms.txt` returned 404. Prompts over 272K tokens are priced 2x input / 1.5x output. |
| Anthropic `platform.claude.com/docs/en/models/<m>/overview`, models overview, pricing | Fable 5.2, Opus 5.5, Sonnet 5.5, Haiku 5.5, Mythos 5.2 (limited), plus Opus 5 / Sonnet 5 / Fable 5.1 from the All-models table | release dates on pages | Computer use is only explicitly mentioned for Opus 5.5; left null for the others. Haiku 5.5 price is "From" ($0.10/$0.50 for prompts up to 100K tokens; $0.50/$2.50 above). |
| Google `ai.google.dev/gemini-api/docs/models/<id>`, `/pricing` | Gemini 4 Carbon, 4 Argon, 3.8 Flash, 3.6 Flash, 3.5 Flash-Lite, 3.1 Flash-Lite, 3.1 Pro preview | "Latest update" month per model (kept in notes, not used as release date) | **Introductory pricing:** Gemini 4 Carbon/Argon $2/$10 through 2026-11-30, then $4/$20 from 2026-12-01; 3.8/3.6 Flash $0.75/$3.75 through 2026-12-31, then $1.50/$7.50. I recorded the current price. No knowledge cutoffs on the pages. |
| Gemma 4 (HF cards `google/gemma-4-*`) | Licence (Apache 2.0), params, context | — | Gemini API lists Gemma 4 as free tier only. Paid prices for 31B and 26B-A4B come from OpenRouter; 12B and E4B have no price. |
| xAI `docs.x.ai/developers/models` and `/models/<id>` | Grok 4.7, 4.6, 4.5, 4.3, Build 0.1, 4.20 Multi-Agent Beta | none | The docs call the developer **"SpaceXSI"**, so I recorded the developer as xAI with that note. No release dates. Grok 4.7 knowledge cutoff May 2026. |
| Mistral `docs.mistral.ai/models/<slug>.md`, `/inference/pricing.md` (fetched with curl) | Large 4 (released 2026-11-05), Medium 3.5 (deprecated), Small 4, Ministral 3 14B | dates on pages | mistral.ai/pricing (the HTML in vc_dl) has no API price table. Its FAQ example says "Mistral Large $0.5/$1.5", which conflicts with the docs price of $0.7/$2.1 for Large 4 (probably an old example for Large 3). |
| Cohere `docs.cohere.com/docs/models`, `cohere.com/pricing` | Command A+ (command-a-plus-05-2026, Apache 2.0, 218B/25B), North Mini Code | — | cohere.com/pricing is client-rendered. I took the $2.50/$10 from the embedded page data next to the Command A+ card, and that adjacency should be re-checked. OpenRouter's Cohere endpoint lists $0.30/$1.50, which **conflicts**. |
| Amazon `aws.amazon.com/nova/pricing/`, Nova 2 user guide | Nova 2 Lite, Nova 2 Pro (Preview), Nova 2 Omni (Preview) | AWS price JSON published 2026-11-11 | The page fills prices from placeholders. I resolved them from the AWS price JSON (`b0.p.awsstatic.com`, US East N. Virginia, Standard tier). No Nova 2 Pro spec page was read. |
| DeepSeek `api-docs.deepseek.com/quick_start/pricing` | deepseek-flash (= V4.1-Flash-1017), deepseek-v4-pro (= V4-Pro-0813) | — | **Peak vs off-peak:** I recorded the PEAK price ($0.30/$1.20 and $1.32/$3.96). Off-peak is half. |
| Alibaba `alibabacloud.com/help/en/model-studio/model-pricing`, QwenCloud model page | qwen3.8-max, qwen3.8-flash, qwen3.8-2.4t-a95b, qwen3.8-27b, qwen3.7-plus | Nov 07, 2026 | I used International (Singapore) prices; China (Beijing) prices are lower. OpenRouter's Alibaba endpoint for qwen3.8-27b shows $0.425/$2.55, against $0.5/$3 on the page. |
| Moonshot `platform.moonshot.ai/docs/pricing/chat` | kimi-k3.1-pro $2/$10, kimi-k3 $3/$15 | — | Table read from the page's embedded JSX. |
| Z.ai `docs.z.ai/guides/overview/pricing` | GLM-5.3, GLM-5.3-Flash, GLM-5.3-FlashX | — | — |
| MiniMax `platform.minimax.io/docs/guides/pricing` | MiniMax-M3.1-Flash $0.15/$0.60; MiniMax-M3 | — | M3 shows list $0.60/$2.40 with "Permanent 50% off", so I recorded the charged $0.30/$1.20. OpenRouter's MiniMax endpoint lists M3.1-Flash at $0.075/$0.30, which **conflicts**. |
| Meta `dev.meta.ai/docs/models`, `/muse-wonder`, `/muse-spark`, `/muse-ember`, `/pricing-rate-limits` | Muse Wonder (preview) $4/$20, Muse Spark 1.3 $1.25/$4.25, Muse Ember $0.10/$0.50; Muse Spark Open (816B/42B) and Muse Glimmer-30B (open weights) | — | The HF card for Muse-Spark-Open is gated (licence not read). Muse Spark also has a Contributor mode ($0.10/$0.20) where your content is used for training. |
| Hugging Face cards (work/hf, work/readme) | Licence, params, context, card dates for open models (DeepSeek, Qwen, Kimi, GLM, MiniMax, NVIDIA Nemotron 3 Ultra / 3.5 Super-VL / 3.5 Lightning, IBM Granite 4.2 8B, Microsoft Phi-4-reasoning-vision-15B, Ling-3.1-flash, MiMo-V2.6-Pro-RL, Step-5-Preview, Inkling, Beam, Nex-N2.6, LFM3-1.7B, gpt-oss) | repo createdAt (not used as a release date) | **Tencent Hy4 and Baidu ERNIE-5.5-Flash-Preview HF JSON returned an auth error**, so their specs come only from OpenRouter. Parameters were taken from card text, not from safetensors totals. |
| OpenRouter `api/v1/models` plus `api/v1/models/<id>/endpoints` | Prices for open-weight models with no first-party price read; context and modalities for Tencent and Baidu | — | **Secondary.** The model-level price is the default listed endpoint, not always the cheapest. Some listings are quantized fp4 endpoints at odd prices (DeepSeek V4.1 Flash 1017 lists $0.006 input). Where the developer runs its own endpoint (Tencent, StepFun, Xiaomi, Nex AGI, Liquid, Baidu), I used that endpoint and named it in `price_provider`. Otherwise `price_provider` says "OpenRouter listed price (matches X endpoint)" and `price_notes` gives the lowest listed endpoint. |

## Scores (vendor.scores.json)
- Every row is the developer's own number from its HF model card, for its own model only. Competitor columns in the same tables were not recorded, because those numbers are the developer's claims about rivals.
- Settings and harnesses are in each card's footnotes and are not normalised. Many cards use the Claude Code harness. Values in parentheses such as "42.6 (44.0†)" were reduced to the first number, and the alternate is kept in notes.
- Cells with two values, such as "43.5 / 56.0" or "Pass@1 20.4 Score 42.9", were skipped (21 cells).
- Units are mostly unlabelled in the cards. I marked them "score as reported (mostly %)", "%" where shown, "Elo" for GDPval / AA-Briefcase / internal arena Elo rows, and "rating" for Codeforces.
- The model pages for closed models (OpenAI, Anthropic, Google, xAI) state no benchmark scores, so there are no closed-model self-reported rows. Announcement pages and system cards were not fetched.

## Things I am unsure about
1. Cohere Command A+ price ($2.50/$10 on cohere.com, against $0.30/$1.50 for Cohere on OpenRouter).
2. Mistral Large 4 price ($0.7/$2.1 in the docs, against the FAQ example of $0.5/$1.5).
3. Whether DeepSeek's peak or off-peak price should count as the "list" price (I used peak).
4. Whether Gemini 4 introductory prices should be replaced by the 2026-12-01 prices ($4/$20).
5. Beam context: the card says 152K, OpenRouter says 1,048,576.
6. MiniMax-M3.1-Flash parameters: the card says ~428B total, the HF safetensors metadata ~220B.
7. The xAI developer name "SpaceXSI" in the docs (rebrand, or a page artefact?).
8. GLM-5.3 AutomationBench is 48.2 on its own card, but DeepSeek's and MiniMax's cards cite 48.8 for GLM-5.3. Cross-card numbers for rival models differ in general.
9. Kimi K3 "ProgramBench" 77.8 against Kimi K3.1 Pro "Program Bench" 31.5, so the metric probably differs between cards.
10. OpenAI status fields are null because the pages state no GA/preview status. No release dates are available for OpenAI, xAI or Google models.
