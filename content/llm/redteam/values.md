# Red-team A: llm.json values (prices, scores, costs, dates, tokens, claims)

Audited file: `/home/claude/quakfoolee-dotcom/chmltech-website/content/llm/llm.json`, **md5 bb4483db… (rebuilt 2026-11-16 04:43 UTC)**.
The audit started on the 04:31 build (md5 089750e4…). The repo was rebuilt at 04:43, with build_dataset.py, catalog.py and match.py changed. I diffed the two builds and re-checked every changed field. The findings below are against the 04:43 build. Live sources were fetched 2026-11-16 between 04:35 and 05:10 UTC with curl (HTTP 200 unless stated). I edited no repo file and did not run build_dataset.py. For the old/new diff I ran a copy whose output path pointed to `/home/claude/llmrefresh/redteam/scratch_llm.json`.

Severity: **B** = blocker (a wrong value would be published), **S** = should fix before publishing, **m** = minor (traceability or wording).

## Summary
| Check | Items checked | PASS | Findings |
|---|---|---|---|
| 1 List prices + URLs | 48 of 50 priced models (Nova 2 Pro/Lite not re-read: AWS page fills prices by JS) | 48 values correct | S1 (unlabelled discount), m1-m3 (URL / tier note) |
| 2 Benchmark values + costs | **515 of 515** stored results, all 19 boards. llm.json re-derived exactly from raw; the raw rows used were checked against the live source on every board. Every agent-card leader and all values for the 3 new models are included. | 515 | 0 transcription errors; m5 (deliberate Epoch rule change, verified) |
| 3 Release dates/status, new models | Hydrogen, Qwen4-Max, Inkling 2 Small; "Inkling Small 2"; ARC-AGI-2 81.667% | 3 dates OK | m6, m7 (Qwen4-Max preview / max output) |
| 4 tok (AA output tokens per Index task) | 13 models vs AA model pages | 13 values | m4 (2 wrong page URLs) |
| 5 Developer claims | 37 sampled against source pages (14 Hydrogen + 23 random), plus a column check of all 145 claims on 4 cards | 114 of 145 card claims correct; sampled 37 OK | **B1** (31 Gemma 4 31B claims belong to other models) |

## Findings

**1. B1: Gemma 4 31B shows 31 developer claims that belong to two other models.**
`gemma-4-31b.claims` has 46 entries. 15 are Gemma 4 31B's own. The other 31 are the "Gemma 4 12B Unified" (16) and "Gemma 4 E4B" (15) columns of the same Hugging Face card. Examples: Codeforces ELO 1659 (12B) and 940 (E4B), next to the real 31B figure of 2150. BigBench Extra Hard 53.0 and 33.1, next to 74.4.
Cause: the new fallback `mid = match(r["model_as_listed"])[0] or VURL.get(r["source_url"])` in build_dataset.py (claims block, about lines 319-327). It assigns every unmatched column on a card to the model that owns the card URL. Only this card is affected today: I listed every fallback-attributed row.
Evidence: https://huggingface.co/google/gemma-4-31B-it (family table, separate 12B Unified and E4B columns).
Fix: remove the `VURL` fallback, or apply it only when `r["model_as_listed"]` is a column header of the owning model. Expected result: gemma-4-31b has 15 claims with Codeforces 2150, and no 1659 or 940. gemma-4-26b-a4b stays at 15 claims; its claims from the 31B card are correct, from its own column.

**2. S1: Gemma 4 26B A4B price $0.0675/$0.225 includes an unlabelled 25% promotional discount.**
The OpenRouter default endpoint is NextBit, at 0.0675/0.225 with `"discount": 0.25`. Without the discount that is $0.09/$0.30. This is the same pattern as the hy4 PRICE_FIX.
Evidence: https://openrouter.ai/api/v1/models/google/gemma-4-26b-a4b-it/endpoints
Fix: either add `"gemma-4-26b-a4b": dict(pin=0.09, pout=0.30, pprov="NextBit via OpenRouter, before its current 25% discount; secondary source", purl=OR_EP.format("google/gemma-4-26b-a4b-it"), pnote="NextBit's endpoint currently shows a 25% discount ($0.0675 input / $0.225 output).")` to PRICE_FIX, or keep the current price and add that pnote.

**3. m1: Gemini 4 Hydrogen purl points to a page with no price.**
`purl` = https://aistudio.google.com/docs/models/gemini-4-hydrogen, which has specs only. The $1.50/$7.50 price (flat, "Free of charge" on the free tier) is on https://aistudio.google.com/docs/pricing#gemini-4-hydrogen.
Fix: add `"gemini-4-hydrogen": dict(purl="https://aistudio.google.com/docs/pricing#gemini-4-hydrogen")` to PRICE_FIX, as was done for the other Gemini models.

**4. m2: The three Muse purls point to model pages with no price.**
dev.meta.ai/docs/muse-wonder, /muse-spark and /muse-ember have no $ figures (checked the `.md` versions). The prices are correct and are on https://dev.meta.ai/docs/pricing-rate-limits: Wonder $4/$20 Standard mode, Spark $1.25/$4.25 Standard mode, Ember $0.10/$0.50 up to 200K input.
Fix: set purl to https://dev.meta.ai/docs/pricing-rate-limits for muse-wonder, muse-spark-1-3 and muse-ember.

**5. m3: Muse Ember needs a tier note.**
Requests with more than 200K input tokens are billed at $0.30/$1.50 "in full, not only for the tokens past 200K" (pricing-rate-limits page).
Fix: add a MODEL_NOTES entry, with the price flag set to True: "Price shown is for requests up to 200,000 input tokens; longer requests cost $0.30 input / $1.50 output for the whole request."

**6. m4: Wrong tok source URLs.**
- nemotron-3-ultra `tok.url` and step-5-preview `tok.url` = https://artificialanalysis.ai/models/command-a-plus. Each model has its own page with the same values: /models/nemotron-3-ultra-550b-a55b (51,468 / 20,714 / 30,753) and /models/step-5-preview (113,473 / 79,907 / 33,566). Fix: point to the model's own page.
- qwen3-8-max `tok.url` and `s.aa_index.url` = the AA home page. AA's home data marks "Qwen3.8 Max (0902)" `deprecated: true`, which is why it is missing from /leaderboards/models. The values are correct (33.655, $10.02, 170,794 tokens). Fix: optionally add "Artificial Analysis lists the 0902 snapshot as deprecated" to the notes.

**7. m5: Epoch "-fallback" runs are now excluded (deliberate change; values verified).**
New values: claude-fable-5-2 gpqa 93.876 (was 96.023 from `claude-fable-5-2-fallback_max`) and claude-opus-5-5 gpqa 90.593 (was 94.066). Both equal the `_max` rows in the live gpqa_diamond.csv. FrontierMath was unaffected.
Consistency note: every AA Index, AA Coding and token row used for Claude models is a "(…, Default Fallback)" variant, because AA publishes no other. Fix: say in the method or notes that Epoch's separate fallback configuration is not used, so a reader does not see a contradiction.

**8. m6: Qwen4-Max release and build.**
- Released `2026-11` with the note "AA lists Nov 16; results dated Nov 15". This is acceptable.
- QwenCloud docs (https://docs.qwencloud.com/developer-guides/getting-started/latest-model.md) describe pay-as-you-go `qwen4-max` and a separate `qwen4-max-preview` model.
- Secondary reports citing those docs (https://ai-tldr.dev/releases/qwen-qwen4-max-preview/, https://magica.com/news/alibaba-qwen4-max-preview-token-plan) give the preview as Token Plan only, Nov 11 10:00 to Nov 25 24:00 UTC+8.
- The OpenRouter listing was created 2026-11-16 02:18 UTC, endpoint `qwen4-max-20261115`.
- The Vals and Arena results (Nov 15) predate the paid listing, and neither board says which build it ran.
Fix: extend the note: "A time-limited qwen4-max-preview ran from Nov 11; the boards do not say which build they tested."

**9. m7: Qwen4-Max max output is 393,000 in llm.json, but the developer's own pages conflict.**
The QwenCloud model page says "Max Output 393K". The QwenCloud docs table says "Maximum output (non-thinking) 131,072 tokens" and "Maximum thinking + final answer 262,144 tokens". 393K looks like the two added together.
Fix: set maxout 262,144 with a note, or keep 393K with the note "docs give 131,072 non-thinking / 262,144 thinking + answer".

**10. m8: Mistral Large 4 identity (carried over from the Nov 12 review, still open).**
The new EXCLUDE_BOARD drops the tbench row (Oct 6, 27.58%), which is consistent with Epoch: model_metadata.csv calls `mistral-large-4-0` (2026-10-06) "Mistral Large 4 Preview" and `mistral-large-4-0-oss` (2026-10-29) "Mistral Large 4". However, the tbench row links to openrouter.ai/mistralai/mistral-large-4-0, whose canonical slug is `mistral-large-4-0-20261006`. That is the same API id as the docs page used for the $0.70/$2.10 price and the Nov 5 release date.
Fix: decide once whether the catalogue entry is the API model (mistral-large-4-0) or the open-weight build, and apply that choice to price, release date and boards. No number changes are needed today.

**11. m9: Arena Agent now publishes cost.** (Optional, not an error.)
The lmarena-ai/leaderboard-dataset `agent` split now has `cost_per_task_p50` and `output_tokens_per_task_p50`, which could fill arena_agent cost.

Already fixed by the 04:43 rebuild, verified:
- tbench "Inkling Small 2" is now matched to inkling-2-small: 13.03%, "Mini-swe-agent, X-high", $963.65/330 = $2.920 per trial. The tbench label links to https://thinkingmachines.ai/news/inkling-2-small/, so it is the same model.
- ling-3-1-flash price removed. It had been $0.045/$0.135, which carries Novita's `"discount": 0.85` (85% promotion) on OpenRouter.

## Check 1: prices (all live)
| Model(s) | Stored | Live | Result |
|---|---|---|---|
| gpt-6-astra / 6.1-sol / 6.1-terra / 6-luna | 10/50, 2/10, 1/5, 0.1/0.5 | same (developers.openai.com model pages) | PASS |
| claude fable-5-2, mythos-5-2, opus-5-5, sonnet-5-5, haiku-5-5 | 8/40, 8/40, 4/20, 2/10, 0.1/0.5 | same (platform.claude.com; Haiku tier note correct) | PASS |
| gemini-4-carbon / argon | 2/10 + intro note | "$2.00 through November 30, 2026. $4.00 starting December 1, 2026" (output $10, then $20) | PASS (note correct; expires in 14 days) |
| gemini-4-hydrogen (new) | 1.5/7.5 | $1.50/$7.50, no intro date (aistudio.google.com/docs/pricing) | PASS (m1 URL) |
| gemini-3-8-flash, 3-5-flash-lite | 0.75/3.75 + note, 0.3/2.5 | same | PASS |
| grok-4-7, grok-build-0-1 | 2/6, 1/2 | same (docs.x.ai) | PASS |
| muse-wonder, spark-1-3, ember | 4/20, 1.25/4.25, 0.1/0.5 | same (pricing-rate-limits.md) | PASS (m2, m3) |
| mistral-large-4, small-4 | 0.7/2.1, 0.15/0.6 | same (docs.mistral.ai) | PASS |
| command-a-plus | 2.5/10 + note | card unchanged (id web3Model.command-a, $2.50/$10); OpenRouter Cohere endpoint 0.30/1.50 | PASS (existing note still accurate) |
| deepseek-v4-pro, v4-1-flash | 1.32/3.96, 0.3/1.2 (peak) | same, off-peak half | PASS |
| qwen4-max (new) | 1.5/4.5 | $1.5/$4.5 Singapore (qwencloud model page, docs pricing #qwen4-max-pricing, Alibaba Model Studio) | PASS |
| qwen3-8-max, qwen3-8-27b | 2/6, 0.5/3 | same | PASS |
| kimi-k3-1-pro | 2/10 | $2.00/$10.00 | PASS |
| glm-5-3, glm-5-3-flash | 1.4/4.4, 0.15/0.5 | same | PASS |
| minimax-m3-1-flash, m3 | 0.15/0.6, 0.3/1.2 | same ("Permanent 50% off") | PASS |
| OpenRouter defaults: gpt-oss-120b 0.15/0.6, **gpt-oss-20b 0.075/0.3**, gemma-4-31b 0.2/0.4, **gemma-4-26b 0.0675/0.225**, muse-spark-open 1.25/4.25, muse-glimmer 0.3/1.2, nemotron-3-ultra 0.6/2.4, **nemotron-3-5-super-vl 0.15/0.5**, nemotron-3-5-lightning 0.07/0.2, mimo 0.435/0.87, step-5 1.0/2.7, inkling 1.0/4.05, **inkling-2-small (new) 0.3/1.0**, beam 0.3/1.0 | as listed | all equal the live /api/v1/models defaults; the 4 vendor-reported default changes (bold, plus granite) are confirmed | PASS except S1 (gemma-26b discount) |
| PRICE_FIX granite-4-2-8b | 0.06/0.15 | CoreWeave 0.06/0.15 is still the default and the lowest full-precision endpoint | PASS (not stale) |
| PRICE_FIX hy4 | 0.834/2.501 + note | the only endpoint (Tencent) is still 0.417/1.2505 with discount 0.5 | PASS (not stale) |
| nova-2-pro, nova-2-lite | 1.25/10, 0.3/2.5 | not re-read (aws.amazon.com/nova/pricing fills prices by JS from a JSON) | not checked |

## Check 2: benchmark values (all 515)
Method:
1. Re-derive every (model, board) result from raw/*.json with the repo's own match/selection logic (`scripts/rt_rederive.py`; scratch build identical to llm.json).
2. Compare each raw row used against a fresh download of the live source (`scripts/cmp_*.py`).
| Board(s) | Live source | Raw rows checked | Result |
|---|---|---|---|
| AA Index (45 models) | artificialanalysis.ai/leaderboards/models flight data; 2 home-only rows from artificialanalysis.ai | 113 + 2 | all score+cost equal |
| AA Coding Agent (21) | /agents/coding-agents | 29 | all indexScore + costUsd equal |
| Vals (31) | vals.ai/benchmarks/vals_index page data | 38 | all equal (Hydrogen 68.492/$9.838; Qwen4 63.197/$9.3304; Inkling 2 Small 56.081/$3.509) |
| Arena Text/Vision/WebDev/Agent (34/18/38/34) | HF lmarena-ai/leaderboard-dataset, commit 8013e3f0 (arena.ai itself returns 403 to curl; not bypassed) | 810 (124 used) | all equal |
| Epoch ECI / FrontierMath / GPQA (32/23/28) | epoch.ai/data/benchmark_data.zip (files dated 2026-11-16 04:17) | 127/107/208 | all equal |
| Vectara (9) | GitHub README ("Last updated on October 22, 2026") | 111 | all equal |
| LiveBench x5 (27 each) | livebench.ai/data/20261106/table.csv + cost.csv | 245 (score, total cost, nq) | all equal |
| Terminal-Bench 4.1 (29 + Inkling 2 Small) | tbench.ai flight (updated_at 2026-11-14) | 59 (accuracy, total_cost, n_trials) | all equal |
| ARC-AGI-2 (21) | arcprize.org/leaderboard flight | 254 (score + costPerTask) | all equal |
| Vending-Bench 2 (17) | andonlabs.com chunks Bl9fFL93.js + nodes/26.CDA-0jog.js | 76 (final_value + mean_cost) | all equal |

Derived costs recomputed by hand from live files:
- LiveBench: Sol browser 2.804, Terra browser 1.950, Fable research 13.27, Carbon data 0.7056, Hydrogen coding 6.192, Hydrogen long 7.152.
- tbench: Opus 5.5 14.30, Fable 5.2 49.98, Inkling 2 Small 2.920, Hydrogen 2.376.
All equal llm.json.

Agent-card leaders (all verified live):

| Card | Leader and runner-up |
|---|---|
| Coding | Fable 5.2 58.472 vs Opus 5.5 58.159 (gap 0.31 correct) |
| WebDev | Fable 5.2 1825.962 |
| Browser | GPT-6.1 Sol 93.3 |
| Research | Fable 5.2 94.5 |
| Long-running | Gemini 4 Carbon 16,484.21 |
| Business | Fable 5.2 71.309 |
| Data | Carbon 86.5 |
| Assistant | Carbon 1526.182 |
| Reasoning | Fable 5.2 FrontierMath 95.088 |

New-model results (all verified):
- **Hydrogen (12):** aa_index 53.919 X-high $3.16 (plus 4 alt), arena_text 1490.428, vals 68.492, tbench 56.36 $2.376, webdev 1703.905, lb_coding 78.5, agent 14.907, lb_browser 77.1, lb_research 86.8, lb_long 61.8, vending 14,549.49 $162.1, lb_data 83.2.
- **Qwen4-Max (4):** aa_index 42.891 $3.268, vals 63.197, webdev 1749.815, agent 7.461.
- **Inkling 2 Small (7):** aa_index 30.629 $1.178, arena_text 1411.781, vals 56.081, webdev 1644.676, agent 2.512, arc2 81.667 $0.2719, tbench 13.03.
- Hydrogen and Qwen4-Max are not yet on Epoch, ARC, Vectara or AA Coding; there are no missed matches for them.

## Check 3: dates and identity
- Gemini 4 Hydrogen 2026-11-12, GA. Correct: the model card says "Published 12 November 2026", the tbench display_date is Nov 12, AA gives 2026-11-12, and the aistudio model page says "Latest update November 2026". The model page also shows computer use and thinking low/medium/high/xhigh.
- Qwen4-Max: now `2026-11`. See m6.
- Inkling 2 Small 2026-11-05. Correct: the developer model card (https://thinkingmachines.ai/model-card/inkling-2-small/) says "Date of release Nov 5, 2026", and ARC, AA and tbench agree. Weights were posted Nov 12 ("Nov 12, 2026 Update" on the news page). The note could cite the model card instead of AA.
- "Inkling Small 2" on tbench is Inkling 2 Small. The model_display link is thinkingmachines.ai/news/inkling-2-small/. The older, different "Inkling Small" (Jul 30) has its own rows. Now matched (see above).
- ARC-AGI-2 for Inkling 2 Small: 81.667% is correct. ARC row `thinky-inkling-2-small-xhigh`: v2_Semi_Private score 0.81667, costPerTask 0.27194635, notes "standard harness". The developer card also reports "ARC-AGI v1 / v2 96.5/81.7%". It is unusually high for its AA Index (30.6), but it is the maintainer's published value.

## Check 4: tok (13 models)
All 13 equal the variant at the model's AA Index setting on its own AA page:

| Model | Total tokens |
|---|---|
| GPT-6 Astra Max | 51,973 |
| Opus 5.5 Max | 173,313 |
| Sonnet 5.5 Max | 285,387 |
| Hydrogen X-high | 154,406 |
| Qwen4 Max | 104,940 |
| Inkling 2 Small | 149,778 |
| Nemotron 3 Ultra | 51,468 |
| Step 5 Preview | 113,473 |
| DeepSeek V4.1 Flash 1017 Max | 138,962 |
| Hy4 | 78,058 |
| Granite 4.2 8B | 51,515 |
| Command A+ | 35,630 |
| Muse Glimmer High | 26,067 |

The reasoning/answer splits are also equal. URL issues are in m4.

## Check 5: developer claims
- Sampled 37 claims against their sources:
  - All 14 Hydrogen claims (DeepMind model card + Google blog), including AA Index 51 high / 54 xhigh and Vals Tax 52.3 / Legal 55.8.
  - 23 random claims across the Inkling 2 Small, Qwen3.8-2.4T-A95B, Beam, Kimi K3.1 Pro, GLM-5.3, DeepSeek V4.1 Flash 1017 and Gemma cards.
  - Every value appears in its benchmark row. The Qwen3.8 Max claims come from the open 2.4T-A95B card, whose column is headed "Qwen3.8-Max". The card says Qwen3.8-Max "is the official version based on Qwen3.8-2.4T-A95B", so the attribution is acceptable.
- Column check of all claims on 4 cards:

| Card | Claims in the model's own column |
|---|---|
| Granite 4.2 8B ("8B Dense") | 21 of 21 |
| Nemotron 3 Ultra ("N-3-Ultra 550B-A55B") | 35 of 35 (7 flagged by the parser were indented sub-rows; values correct) |
| Nemotron 3.5 Super VL ("Nemotron 3.5 SuperGA BF16") | 43 of 43 |
| Gemma 4 31B | **15 of 46** (B1) |

Downloads: /home/claude/llmrefresh/redteam/dl/. Scripts: /home/claude/llmrefresh/redteam/scripts/.
