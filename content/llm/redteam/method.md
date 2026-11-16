# Red-team review B: LLM leaderboard refresh (data as of 2026-11-16)

Reviewed on 2026-11-16. I did not build this refresh.

**Files reviewed:**
- content/llm/{catalog.py, match.py, build_dataset.py, llm.json, raw/*}
- content/gen/llm_page.py
- assets/js/llm.js and assets/css/llm.css
- the built llm-leaderboard.html
- the previous llm.json (`git show HEAD:content/llm/llm.json`, as_of 2026-11-12)

**What I ran.** I ran `match()` over every `model_as_listed` on the 19 boards in use. I also ran it over the token board "Artificial Analysis output tokens per Index task" and over all 644 rows in vendor.scores.json. That came to 2,242 board rows.

**What I re-derived.** From both llm.json files I rebuilt:
- the top five for every board
- the blended-price frontier
- the cost-per-task frontier (every `alt` setting plotted as its own point, as llm.js does)

I diffed every model spec and score against HEAD.

**Read-only lookups.** I read the Epoch download the research agent left on disk (/home/claude/llmrefresh/dl/index/epoch/x/model_metadata.csv and gpqa_diamond.csv). I only read it.

**Where I edited.** I edited no repo files. I did not run build_dataset.py in the repo. I tested the proposed fixes in a scratch copy only (/home/claude/llmrefresh/rtb/fix/). I also regenerated the page in a second copy (/home/claude/llmrefresh/rtb/site/).

Severity: **B** = blocker, **S** = should-fix, **m** = minor.

Last review's fixes were checked and still hold:
- Terminal-Bench "Opus 5.5" and "Sonnet 5.5" match.
- "Muse Wonder Full" is excluded on every board, including the token board.
- Mistral Large 4 Preview is excluded on Epoch.
- Snapshot allow-lists work for DeepSeek: ARC-AGI-2 and the Arena boards use 1017, not 0910.

---

## A. Name matching

### 1. [B] Ling 3.1 Flash: the 1019 snapshot's score is plotted at the original snapshot's price, as the first point on the default chart
- **Evidence:**
  - The only board result is AA "Ling 3.1 Flash 1019" (29.57). It matches `ling-3-1-flash` because the entry has no `snapshots` list, and the 4-digit token is accepted silently.
  - The 1019 token is also not shown (`show_snapshot` is not set).
  - raw/vendor.models.json, record "Ling-3.1-flash-1019", notes: *"Upgraded snapshot of Ling-3.1-flash … OpenRouter inclusionai/ling-3.1-flash points to the original 20261002 snapshot, not 1019, so no price is recorded for 1019."*
  - Even so, the entry takes its price ($0.045 / $0.135, Novita via OpenRouter) and its spec URL from the original-snapshot records.
- **Further mismatches:**
  - The release date (2026-10-22) and the token figure both come from AA's 1019 record.
  - The 6 developer claims come from the 1019 model card.
- **Effect:** Ling 3.1 Flash is the cheapest point on the AA Intelligence Index blended-price frontier, the page's default view ($0.0675, 29.57). No page lists that price for the model that earned that score. This is the same class of error as last time's B2 (Muse Wonder Full plotted at the API price).
- **Fix (catalog.py):** change the entry to
  `vendor=["Ling-3.1-flash-1019", "Ling-3.1-flash"], snapshots=["1019"], show_snapshot=True`.
  This drops the OpenRouter price record from `vendor`.
- **Fix (build_dataset.py MODEL_NOTES):** add
  `"ling-3-1-flash": ("Results are for the 1019 snapshot. OpenRouter lists a price only for the original Oct 2, 2026 snapshot, so no price is shown.", False)`.
- **Tested in the scratch copy:**
  - Ling leaves the price charts, and the AA blended frontier now starts Granite 4.2 8B, then Nemotron 3.5 Lightning, then Claude Haiku 5.5.
  - The aa_index result and the token row are labelled "1019 snapshot".
  - The spec URL is now the 1019 repo.
  - List prices drop from 51 to 50, and the hero and method counts update by themselves.

### 2. [B] Terminal-Bench "Mistral Large 4" is the Preview build, merged into the GA model
- **Evidence:**
  - This row is new this refresh: 27.58%, Claude Code, max, $718.40, result_date 2026-10-06.
  - Terminal-Bench's row date is the model's release date. Opus 5.5 is 09-22, Fable 5.2 11-09, Gemini 4 Hydrogen 11-12 and "DeepSeek V4.1 Flash 1017" 10-17, each equal to that model's release.
  - Epoch model_metadata.csv dates the builds: `mistral-large-4-0_high`, "Mistral Large 4 Preview", **2026-10-06**; `mistral-large-4-0-oss_high`, "Mistral Large 4", **2026-10-29**. Mistral's docs give GA as 2026-11-05.
  - So this row is the Preview, which the page says is "kept apart".
- **Effect:** the Terminal-Bench result shown for Mistral Large 4 is a Preview result. It is not on a frontier or in a card's top five.
- **Fix (match.py):** add `("Terminal-Bench 4.1", "Mistral Large 4")` to `EXCLUDE_BOARD`. Tested: tbench drops to 29 − 1 + 1 (with finding 4) = 29 models.

### 3. [S] Epoch's new "with fallback" runs are merged silently and change GPQA
- **Evidence:**
  - New GPQA rows this refresh are `claude-fable-5-2-fallback_max` (0.9602) and `claude-opus-5-5-fallback_max` (0.9407).
  - In Epoch's model_metadata.csv they are a separate model version, display name **"Claude Fable 5.2 (with fallback, max)"**. Their run ids are `manual_gpqa_diamond_fallback_…`.
  - Epoch also has its normal runs, `claude-fable-5-2_max` (0.9388) and `claude-opus-5-5_max` (0.9059).
  - match.py drops "fallback" from the label, so the page shows both as plain "Max". index.notes.md does not mention fallback at all, and the research agent's new notes dropped the "Display name in Epoch metadata" text that would have shown it.
- **Effect:** GPQA Fable 5.2 goes from 93.88 to 96.02 and moves to #3 in the top five. Opus 5.5 goes from 90.59 to 94.07. Both are presented as like-for-like with other models' standard runs.
- **Fix (match.py):** `if QUANT.search(name) or "-fallback_" in name: return None, None`, so Epoch's fallback variants are kept apart until someone confirms what "with fallback" means.
  - This leaves AA's "(…, Default Fallback)" rows alone. On AA that is the only configuration listed for Claude models.
  - Tested: GPQA reverts to 93.876 / 90.593, and the top five becomes Carbon, Argon, Astra, Sonnet 5.5, GPT-6.1 Sol.
- **Fix (index.notes.md, research agent):** record what Epoch's "with fallback" configuration is.

### 4. [S] Terminal-Bench "Inkling Small 2" should match Inkling 2 Small
- **Evidence:** the Terminal-Bench 4.1 row is "Inkling Small 2": Thinking Machines Lab, mini-swe-agent, xhigh, 13.03% ± 2.85, $963.65, date **2026-11-05**.
  - The date is Inkling 2 Small's release date on AA (index.models.json).
  - ARC lists "Inkling 2 Small (XHigh)" on the same date.
  - The first-generation "Inkling Small" is a separate row on the same board (0.91%, dated 2026-07-30).
  - agentic.notes.md leaves the decision to the merge step. match() returns (None, None) because "small" is not a SETTING word.
- **Fix (match.py):** add a board-scoped alias,
  `BOARD_ALIAS = {("Terminal-Bench 4.1", "Inkling Small 2"): "Inkling 2 Small"}`,
  and apply it in `match()` before the QUANT check: `name = BOARD_ALIAS.get((board, name), name)`. A global alias would risk catching other boards.
- **Fix (build_dataset.py MODEL_NOTES):** for inkling-2-small, add "Terminal-Bench lists this model as 'Inkling Small 2'."
- **Tested:** tbench gains Inkling 2 Small at 13.03%, Mini-swe-agent, X-high, $2.92 per trial. It is not on any frontier.

### 5. [S] Developer claims ignore the snapshot rule, and three models miss theirs
- The claims loop calls `match(r["model_as_listed"])` with no snapshot preference and no other fallback, so three problems follow.
- **Mixed DeepSeek snapshots.** DeepSeek V4.1 Flash shows 30 claims. 11 come from the 1017 card. 19 come from the earlier `deepseek-ai/DeepSeek-V4.1-Flash` card ("DS-V4.1-Flash"). The panel therefore shows "Terminal-Bench 4.0 42.3" and "Terminal-Bench 4.0 (Pass@1) 31.2" side by side, unlabelled.
- **Missed NVIDIA and IBM claims.** These are unmatched although their source URL is the catalogue model's own card:
  - "N-3-Ultra 550B-A55B" (35 rows): nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16
  - "Nemotron 3.5 SuperGA BF16" (43 rows): nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-BF16
  - "8B Dense" (21 rows): ibm-granite/granite-4.2-8b
- **Ling.** Ling's 6 claims are from 1019 (fixed by finding 1).
- **Fix (build_dataset.py claims loop):**
  1. If the entry has `snapshots` and any claim row names one, drop the undated claim rows, as the board loop already does.
  2. If `match()` fails, match on `source_url` against the URLs of the entry's `vendor` records.
  3. Otherwise add the three names as aliases in catalog.py: "N-3-Ultra 550B-A55B" to nemotron-3-ultra, "Nemotron 3.5 SuperGA BF16" to nemotron-3-5-super-vl, "8B Dense" to granite-4-2-8b.
- **Confirmed:** claims never reach ranks or frontiers. build_dataset.py keeps them in `m.claims`; the board loop reads only arena, index and agentic rows and skips `self_reported`; llm.js uses `m.claims` only in `claimsBlock()`.

### 6. [m] Correctly kept apart (no action needed)
- Claude Fable 5.1, Fable 5, Opus 5, Sonnet 5 (all spellings, including Terminal-Bench "Fable 5.1", "Opus 5" and Epoch `claude-fable-5-1_max`).
- Qwen3.7, Qwen3.6, Qwen3.5 and "-Max-Preview" rows. "Qwen4-Max" spelled four ways all match, and nothing from Qwen3.8 merges into Qwen4.
- "Inkling Small" and "Inkling-Small" (first generation).
- Gemini 3.5/3.7 Flash, GPT-5.6 and GPT-6 Sol.
- NVFP4 builds; "Hy4 preview"; "alibaba/qwen3.8-max-internal".
- "Claude Opus 5.5 Max + GPT-6 Luna High" (Devin Fusion).
- K2 Horizon and JT-4.1 Flash (not in the catalogue).
- No "Gemini 4 Hydrogen" variants other than effort labels exist in any raw file.

---

## B. Specs, prices, tiers

### 7. [S] AA cost per task for Gemini 4 Carbon and Argon dropped with unchanged scores; the cause is not noted
- **Evidence:** compared with HEAD, the raw AA Index rows changed cost only:

  | Row | Score | Cost per task before | Cost per task now |
  |---|---|---|---|
  | Argon (High) | 50.41 (unchanged) | 9.9466 | 4.9733 (exactly ×0.5000) |
  | Carbon (High) | 60.03 (unchanged) | 7.756 | 5.485 |
  | Carbon (Medium) | unchanged | 6.586 | 4.678 |
  | Carbon (Low) | unchanged | 7.187 | 5.221 |

  - AA Coding moved the same way (Argon 11.73 to 6.84).
  - The exact halving matches a switch from $4/$20 to the $2/$10 introductory price, which ends on Nov 30.
  - index.notes.md says the method is "unchanged" and does not mention this.
- **Effect:** on the AA cost-per-task frontier, Claude Opus 5.5 (X-high, $6.05, 57.4) is no longer a frontier point; Carbon Medium at $4.68 now beats it. These costs will be wrong from Dec 1.
- **Fix:**
  - Ask the index agent to confirm on AA.
  - In build_dataset.py, append to the MODEL_NOTES text for gemini-4-carbon and gemini-4-argon: "Artificial Analysis's cost per task uses the introductory price."
  - Add to the aa_index and aa_coding caveats: "Costs follow the developer's current list price, including introductory prices."

### 8. [S] Qwen3.8-Max no longer fits the Frontier definition
- **Evidence:**
  - catalog.py defines Frontier as "the developer's most capable generally offered model(s)".
  - Alibaba's page calls Qwen4-Max the "next-generation flagship" and lists it above qwen3.8-max (vendor.models.json).
  - Qwen4-Max beats Qwen3.8-Max everywhere both appear: AA 42.9 vs 33.7, Arena WebDev 1749.8 vs 1675.6, Arena Agent 7.5 vs −0.9.
  - Qwen4-Max is also cheaper ($1.50/$4.50 vs $2/$6).
  - "Mid-size" (a cheaper model one step down) does not fit either.
- **Fix:** keep Qwen3.8-Max in the catalogue; it is still a current offering, so SPEC rule 8 keeps it in scope. Then:
  - Add to MODEL_NOTES: "Superseded as Alibaba's flagship by Qwen4-Max (Nov 2026); still offered at $2 / $6."
  - Either add a "Previous flagship" tier or note the exception in the tier filter's note text in llm_page.py.

### 9. [m] The three new entries: tier, developer, aliases
- **Gemini 4 Hydrogen** (Mid-size, Google): supported.
  - $1.50/$7.50, GA (aistudio.google.com).
  - Google says it was "adapted from Gemini 4 Carbon", so Mid-size is a line-up label. It outscores Frontier Argon on AA (53.9 vs 50.4) and Vending, so the tier note matters here.
  - Index raw slip: index.models.json "Gemini 4 Hydrogen (High)" says its details came from `artificialanalysis.ai/models/claude-fable-5-2`. It is unused because the vendor record wins, but it should be corrected in raw.
- **Qwen4-Max** (Frontier, "Alibaba (Qwen)"): tier and aliases are fine.
  - The release date 2026-11-16 is from AA, but Arena and Vals results are dated 2026-11-15, and OpenRouter's endpoint is `qwen4-max-20261115`.
  - Fix: `RELEASE["qwen4-max"] = ("2026-11", "Release month: Artificial Analysis lists Nov 16, 2026; benchmark results are dated Nov 15.")`.
- **Inkling 2 Small** (Small and fast, Thinking Machines Lab): the name supports the tier, but there are two oddities.
  - It has 594B total parameters and outscores the Frontier "Inkling" (AA 30.6 vs 12.5).
  - `reasoning` is null, so it drops out of the "Reasoning mode" filter, although AA counts 88K reasoning tokens per task and ARC and Terminal-Bench run it at xhigh.
  - Fix: add the alias "Inkling Small 2" through finding 4. Set `reasoning="Yes"` with the note "Reasoning effort settings as run by ARC Prize and Terminal-Bench". The price is OpenRouter's (secondary), as labelled.

### 10. [m] Scope: K2 Horizon 375B A23B and JT-4.1 Flash should not be added now
- **K2 Horizon:**
  - Open weights, Apache 2.0, 375B/23B.
  - AA 17.8 would put it 16th of 27 open-weight models, about level with Beam 1.0 (17.7). So it is arguably "leading open-weight" under SPEC rule 8.
  - However, it is on AA only. It has no price: AA's cost and price are 0/0 placeholders, and no API or OpenRouter listing was found. Its developer ("IFM", link to MBZUAI/LLM360 unconfirmed) is unverified.
  - Add it later if a second board or a price appears. If added, treat AA's $0 cost as null, which build_dataset.py already does.
- **JT-4.1 Flash 236B A21B:**
  - China Mobile, proprietary API, no price, released 2026-11-11, AA only.
  - It is not a major developer's flagship or sibling, so it is out of scope.

### 11. [m] Open-weight "list prices" move with OpenRouter's default endpoint
- Examples:
  - gpt-oss-20b went from $0.03/$0.13 to $0.075/$0.30.
  - Gemma 4 26B A4B went from $0.08/$0.10 to $0.0675/$0.225.
  - vendor.notes.md: "These changes reflect which provider is the default, not a developer price change".
- **Effect:** gpt-oss-20b drops off the Arena Text, ECI and GPQA blended frontiers, and Granite 4.2 8B joins the Arena Text frontier.
- **Fix:** use one rule for all open-weight prices, as PRICE_FIX already does for Granite: the lowest full-precision host listed. Alternatively, say in the price note that the default host can change between snapshots.

---

## C. New features

### 12. [S] "What changed": comparing coding-agent leaders across an index change is misleading
- **What the page says:** the news card lists "Coding agents: Claude Fable 5.2 (was Claude Opus 5.5)".
- **Why that is not like for like:**
  - The "before" leader (Opus 5.5, 61.65) was measured with FrontierCode v1.1.
  - The "now" leader (Fable 5.2, 58.47) uses FrontierCode-AA 2.0.
  - Fable 5.2 was not on aa_coding at all in the previous snapshot; it is new.
  - On the current index Opus 5.5 is 0.3 points behind (58.16).
- The caveat sits in the next card, but this line reads as "Fable overtook Opus".
- **Fix (build_dataset.py):**
  - Add `COMPOSITION_CHANGED = {"aa_coding"}`.
  - In the leaders loop, for those boards, emit `dict(group=…, before=None, now=b2, note="index components changed; not comparable")`.
  - In llm_page.py news(), render that as "Coding agents: Claude Fable 5.2 leads the revised index (0.3 points ahead of Claude Opus 5.5; not comparable with the Nov 12 snapshot)".
  - Or drop the line.

### 13. [S] "What changed" goes stale if build_dataset.py is re-run on the same day
- **Cause:** `changes` is recomputed only when `P["as_of"] != AS_OF`. On a re-run, such as after applying this review's fixes, it copies the old `changes`: the old `added`, `leaders` and `results_before`. `n_now` in llm_page.py is live.
- **Confirmed** in the scratch copy: after the fixes the leaders block is the pre-fix one.
- **Fix:** read the baseline from a frozen file instead of the file being overwritten. Either:
  - write `content/llm/llm.prev.json` once per AS_OF change and always diff against it, or
  - diff against `git show HEAD:content/llm/llm.json`.

### 14. [S] Developer-claim units print as long text in the number column
- **Evidence:** 240 of 425 claims have the unit "score as reported (no unit given; mostly % accuracy/pass rate)". claimsBlock() renders this as `42.6 score as reported (no unit given; mostly % accuracy/pass rate)`. Two more claims have the unit "score as reported (no unit given)".
- **Fix (assets/js/llm.js claimsBlock):** treat any unit starting with "score as reported" as unitless:
  `var u = /^score as reported/.test(c.unit || "") ? "" : (c.unit || "");`

### 15. Token figure (`tok`): correct
- All 44 models with token data have `tok.set` equal to their aa_index `set`, including the snapshot label for Qwen3.8-Max and None for unlabelled rows.
- Gemma 4 31B has no token row, as index.notes.md says.
- "Muse Wonder Full (Max)" and "Claude Fable 5.1" token rows are correctly unmatched.
- One minor gap: when a model has no aa_index result, the "largest total" fallback contradicts the page's "at the setting ranked above". No current model is affected. Fix: skip `tok` when `want` is missing.

### 16. Board news: every statement checked against raw/*.notes.md
- **AA Coding component change.** True: FrontierCode v1.1 Main replaced by FrontierCode-AA 2.0, same name, 29 pairs (index.notes.md). The caveat text on the board is accurate.
- **Terminal-Bench "24 results on Nov 13-14, including Gemini 4 Hydrogen (56.4%) and Claude Fable 5.2".** True: 24 rows added, created 11-13 or 11-14 (agentic raw notes), and Hydrogen is 56.36%.
- **Board update dates.** All true per arena.notes.md and index.notes.md:
  - Arena WebDev and Agent: 2026-11-15
  - Vals: 2026-11-15
  - Epoch hub: Nov 16
  - LiveBench: 20261106 updated in place, Hydrogen added
  - Vectara: Oct 22
- **Small omissions (m):**
  - Arena Text also moved (Nov 9 to Nov 11).
  - Vending-Bench added Hydrogen (#3) and Fable 5.2.
  - Two aa_coding results disappeared: Gemini 3.8 Flash and Muse Spark Open are no longer on the revised index. Add one line: "Gemini 3.8 Flash and Muse Spark Open are not on the revised AA Coding Agent Index."

---

## D. Rankings and frontiers re-derived (compared with HEAD)

### 17. Changes that follow from the new data (expected)
- **New models on frontiers:**
  - Gemini 4 Hydrogen on aa_index, vals, tbench, arena_agent, lb_long, vending and lb_data.
  - Qwen4-Max on vals and arena_webdev.
  - Inkling 2 Small on arena_webdev, arena_agent and arc2.
- **Card top fives:** Fable 5.2 is new at #1 on aa_coding and arena_agent. Hydrogen is #3 on Vending and LiveBench Data.
- **Terminal-Bench:** grows from 11 to 29 models.
- **Arena:** small Elo moves throughout, as expected after the Nov 11 and Nov 15 republishes.
- **Card leaders:** unchanged except Coding (see finding 12).
- **Frontier code:** the Python re-implementation of `frontier()` agrees with llm.js on every board.

### 18. Changes not explained by the notes
- AA Carbon and Argon costs: finding 7.
- GPQA Fable 5.2 and Opus 5.5: finding 3.
- Open-weight price swaps: finding 11.
- **Release dates newly filled from AA.** Nemotron 3 Ultra (2026-06-04), Step 5 Preview (2026-09-18), Hy4 (2026-11-03) and Ling (2026-10-22, the 1019 date) were null before. They are labelled "as listed by Artificial Analysis", which is fine apart from Ling (finding 1).

### 19. [m] Ties are shown as distinct ranks
- Terminal-Bench #1: Fable 5.2 and Opus 5.5 are both 65.76% (217/330 trials each); the card order is just catalogue order.
- FrontierMath #2 and #3: GPT-6 Astra and GPT-6.1 Sol are both 93.7%.
- **Fix (llm_page.py type_card):** give equal values the same rank number.

---

## E. Page text

### 20. [m] The committed llm-leaderboard.html is older than llm_page.py
- The built page shows "$1.5 / $7.5", but current news() formats with `:.2f`. Regenerating the page in a copy changes only those three lines ("$1.50 / $7.50" etc.).
- **Fix:** re-run content/gen/llm_page.py after the data fixes.
- In the same news line, Inkling 2 Small's "$0.30 / $1.00" is OpenRouter's price. Add "(OpenRouter)" when `pprov` contains "secondary".

### 21. Hero, method text and disclaimer
- **Hero and counts:** correct against llm.json.
  - 53 models, 19 benchmarks, 22 developers, 29 open-weight models
  - 515 results, up from 473
  - 51 list prices (50 after finding 1)
- **Board date lines:** all match raw dates.
  - Terminal-Bench says "latest result Nov 12", which is true. The board record was updated Nov 14 (m: could say "board updated Nov 14, 2026").
- **Disclaimer:** still accurate. Catalogue coverage of the unused boards now:

  | Board | Catalogue models |
  |---|---|
  | SWE-bench variants | 1 each |
  | SWE-Bench Pro | 1 |
  | OSWorld-Verified | 1 |
  | OSWorld 2.0 | 2 (MiniMax M3 and M3.1 Flash) |
  | τ³-Banking | 2 |
  | BFCL | 0 |
  | Aider | 1 |
  | METR | no longer updated since Sep 8, 2026 |

- **"Match names carefully" step:** says earlier snapshots and previews are kept apart. This is untrue until findings 1–3 are fixed.
- **"Red-team before publishing" step:** says errors found are fixed before publication. This needs findings 1–3 fixed first.

---

## Summary

**Blockers**
1. Ling 3.1 Flash: the 1019 score is plotted at the price of a different snapshot, as the first point on the default chart.
2. Terminal-Bench "Mistral Large 4" is the Preview build (dated 2026-10-06), merged into GA.

**Should-fix**
- Matching: 3 Epoch "with fallback" runs merged into GPQA; 4 "Inkling Small 2" unmatched; 5 claims mix DeepSeek snapshots and miss 99 NVIDIA and IBM rows.
- Data: 7 AA costs now use the introductory Gemini price, with no note; 8 Qwen3.8-Max no longer fits "Frontier".
- Features: 12 the leader comparison on the coding card spans an index change; 13 `changes` goes stale on re-run; 14 claim units clutter the table.

**Minor:** 9, 10, 11, 15, 16, 19, 20, 21.

All three matching fixes (1, 2–4 and the fallback rule) were tested together in /home/claude/llmrefresh/rtb/fix/. That build has 53 models and 515 results.
