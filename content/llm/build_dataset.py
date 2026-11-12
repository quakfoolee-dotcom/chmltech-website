"""Build content/llm/llm.json for llm-leaderboard.html from the research files in content/llm/raw/.

Research files (one set per research agent; spec in content/llm/SPEC.md):
  vendor.*      developer model pages and price lists (specs, prices)
  arena.*       Arena (arena.ai) leaderboards, from Arena's published dataset
  arena_full.*  every model on the Arena Text, Vision and WebDev boards (content/llm/arena_full.py), used in place of
                the top-60 extract in arena.* for those three boards
  index.*       Artificial Analysis, Epoch AI, Vals AI, Vectara, LiveBench
  agentic.*     SWE-bench, Terminal-Bench, OSWorld, tau-bench, BFCL, Aider, METR, ARC-AGI, Vending-Bench
Rules applied here (also stated on the page):
  - Results are taken from the benchmark maintainers' boards; developers' own claims about their models are not used.
  - A model listed at several settings is ranked on its best one; the setting is shown. Every setting that has a published
    cost is kept (`alt`) so the cost-per-task chart can plot each one.
  - Fractions (0-1) are shown as percentages. No other change is made to any score.
  - Cost per task is the benchmark's own figure, except where a board publishes only a total (LiveBench: total / tasks,
    as LiveBench's site does; Terminal-Bench: total / trials). Those are marked "derived".
Run: python3 content/llm/build_dataset.py   (from the site root)
"""
import json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from catalog import CATALOG
from match import match

RAW = os.path.join(HERE, "raw")
AS_OF = "2026-11-12"
load = lambda p: json.load(open(os.path.join(RAW, p), encoding="utf-8"))


def d(s):
    return datetime.date.fromisoformat(s).strftime("%b %-d, %Y")


# id, board name in the research files, display name, short name, section, unit, higher-is-better, scale, cost mode,
# what it measures, caveat, source label, source url, date text
B = [
 ("aa_index", "Artificial Analysis Intelligence Index v5.0.1", "Artificial Analysis Intelligence Index", "AA Intelligence Index", "General capability", "points", True, 1, "task",
  "A combined score from nine evaluations covering knowledge work, coding, science and general knowledge, run by Artificial Analysis on each model.",
  "Cost per task is Artificial Analysis's weighted average API cost per Index task.", "Artificial Analysis", "https://artificialanalysis.ai/leaderboards/models",
  "Index v5.0.1; board shows no update date, retrieved " + d("2026-11-11")),
 ("arena_text", "Arena Text (style control, default view)", "Arena Text", "Arena Text", "General capability", "Elo", True, 1, None,
  "Human preference: people compare two anonymous answers to their own prompts and pick the better one. Ratings on an Elo-like scale; style control adjusts for answer length and formatting.",
  "Neighbouring models often have overlapping confidence intervals; see the ± range in each model's details.", "Arena (arena.ai)", "https://arena.ai/leaderboard/text", None),
 ("eci", "Epoch Capabilities Index (ECI)", "Epoch Capabilities Index", "Epoch ECI", "General capability", "points", True, 1, None,
  "Epoch AI's single capability score, combining results from many benchmarks.", None, "Epoch AI", "https://epoch.ai/benchmarks", "hub updated " + d("2026-11-11")),
 ("vals", "Vals Index v2.2", "Vals Index", "Vals Index", "Business and knowledge work", "%", True, 1, "task",
  "Agentic tasks in finance, law, tax and software, weighted by each sector's share of US GDP, run by Vals AI.",
  "Cost per task is Vals's published cost per test.", "Vals AI", "https://www.vals.ai/benchmarks/vals_index", None),
 ("aa_coding", "Artificial Analysis Coding Agent Index", "Artificial Analysis Coding Agent Index", "AA Coding Agent", "Coding and software", "%", True, 100, "task",
  "Models run inside coding-agent tools on three evaluations: FrontierCode, SWE-Atlas QnA and Terminal-Bench v4. The tool used is shown with each score; several are the developer's own tool.",
  "Cost per task is Artificial Analysis's average API cost per task.", "Artificial Analysis", "https://artificialanalysis.ai/",
  "board shows no update date, retrieved " + d("2026-11-11")),
 ("tbench", "Terminal-Bench 4.1", "Terminal-Bench 4.1", "Terminal-Bench", "Coding and software", "%", True, 1, "trials",
  "Tasks carried out in a computer terminal, run inside named agent tools. Share of trials solved.",
  "Cost here is derived: the board's total cost divided by its number of trials (cost per trial). The board does not say which results it verified.",
  "Terminal-Bench (tbench.ai)", "https://www.tbench.ai/", "latest result " + d("2026-09-29") + ", board retrieved " + d("2026-11-11")),
 ("arena_webdev", "Arena WebDev / Code Arena", "Arena WebDev", "Arena WebDev", "Coding and software", "Elo", True, 1, None,
  "Human preference for web apps the models build from a prompt, judged side by side.", None, "Arena (arena.ai)", "https://arena.ai/leaderboard/webdev", None),
 ("lb_coding", "LiveBench 2.0 - coding", "LiveBench Coding", "LiveBench Coding", "Coding and software", "points", True, 1, "suite",
  "LiveBench's coding suite, scored automatically from 0 to 100.", "LB", "LiveBench", "https://livebench.ai/", "release " + d("2026-11-06")),
 ("arena_agent", "Arena Agent (aggregate)", "Arena Agent", "Arena Agent", "Agents", "%", True, 100, None,
  "Real agent sessions on arena.ai: how much better each model does than a baseline at finishing users' multi-step tasks, from task outcomes and user feedback.",
  None, "Arena (arena.ai)", "https://arena.ai/leaderboard/agent", None),
 ("lb_browser", "LiveBench 2.0 - browser", "LiveBench Browser", "LiveBench Browser", "Agents", "points", True, 1, "suite",
  "LiveBench's browser-agent suite: tasks completed by operating a web browser, scored from 0 to 100.", "LB", "LiveBench", "https://livebench.ai/", "release " + d("2026-11-06")),
 ("lb_research", "LiveBench 2.0 - research", "LiveBench Research", "LiveBench Research", "Agents", "points", True, 1, "suite",
  "LiveBench's research suite, scored from 0 to 100.", "LB", "LiveBench", "https://livebench.ai/", "release " + d("2026-11-06")),
 ("lb_long", "LiveBench 2.0 - long_agentic", "LiveBench Long Agentic", "LiveBench Long Agentic", "Agents", "points", True, 1, "suite",
  "LiveBench's long agentic suite: long, multi-step agent tasks, scored from 0 to 100.", "LB", "LiveBench", "https://livebench.ai/", "release " + d("2026-11-06")),
 ("vending", "Vending-Bench 2", "Vending-Bench 2", "Vending-Bench", "Agents", "USD", True, 1, "task",
  "A simulated year running a vending-machine business: ordering stock, setting prices, dealing with suppliers. Score is the money left at the end (start: $500).",
  "Cost per task is the mean API cost of one full simulated year.", "Andon Labs", "https://andonlabs.com/evals/vending-bench-2",
  "board shows no update date, retrieved " + d("2026-11-11")),
 ("lb_data", "LiveBench 2.0 - data_analysis", "LiveBench Data Analysis", "LiveBench Data", "Documents and data", "points", True, 1, "suite",
  "LiveBench's data-analysis suite, scored from 0 to 100.", "LB", "LiveBench", "https://livebench.ai/", "release " + d("2026-11-06")),
 ("arena_vision", "Arena Vision (style control, default view)", "Arena Vision", "Arena Vision", "Documents and data", "Elo", True, 1, None,
  "Human preference on prompts that include images, such as charts, photos and screenshots.", None, "Arena (arena.ai)", "https://arena.ai/leaderboard/vision", None),
 ("vectara", "Vectara Hallucination Leaderboard (HHEM)", "Vectara Hallucination Rate", "Hallucination rate", "Documents and data", "%", False, 1, None,
  "How often a model adds facts that are not in a document it is asked to summarise. Lower is better.", None, "Vectara", "https://github.com/vectara/hallucination-leaderboard", None),
 ("frontiermath", "FrontierMath Tiers 1-3 v2 (Epoch AI)", "FrontierMath (Tiers 1-3)", "FrontierMath", "Reasoning, maths and science", "%", True, 100, None,
  "Unpublished, expert-written research-level maths problems, run by Epoch AI.", None, "Epoch AI", "https://epoch.ai/benchmarks", None),
 ("gpqa", "GPQA Diamond (Epoch AI run)", "GPQA Diamond", "GPQA Diamond", "Reasoning, maths and science", "%", True, 100, None,
  "Graduate-level multiple-choice questions in biology, chemistry and physics, run by Epoch AI.", "Top models are close to the ceiling, so small gaps mean little.", "Epoch AI", "https://epoch.ai/benchmarks", None),
 ("arc2", "ARC-AGI-2 (Semi-Private)", "ARC-AGI-2", "ARC-AGI-2", "Reasoning, maths and science", "%", True, 100, "task",
  "Visual grid puzzles where each task needs a new rule to be worked out, run by the ARC Prize Foundation.", "Cost per task is ARC Prize's measured cost per task.", "ARC Prize", "https://arcprize.org/leaderboard", None),
]
FULL_ARENA = {"Arena Text (style control, default view)", "Arena Vision (style control, default view)", "Arena WebDev / Code Arena"}
EPOCH = {"eci", "frontiermath", "gpqa"}

GROUPS = [
 dict(id="coding", name="Coding agents", bench="aa_coding", also=["tbench", "lb_coding"],
      desc="Agents that read a codebase, write and test changes, and work in the terminal, as in Claude Code, Codex or Cursor."),
 dict(id="apps", name="Web and app builders", bench="arena_webdev", also=["lb_coding"],
      desc="Tools that turn a description into a working web page or small app, judged by the people who asked for it."),
 dict(id="browser", name="Browser and computer use", bench="lb_browser", also=["arena_agent"],
      desc="Agents that operate a browser for you: navigating sites, filling forms and pulling information out."),
 dict(id="research", name="Research agents", bench="lb_research", also=["lb_long"],
      desc="Agents that search, read many sources and pull the findings together into a cited answer."),
 dict(id="long", name="Long-running autonomous agents", bench="vending", also=["lb_long", "arena_agent"],
      desc="Agents trusted with a goal over a long period, making many decisions without a person checking each one."),
 dict(id="business", name="Business and knowledge work", bench="vals", also=["aa_index"],
      desc="Finance, legal, tax and analysis tasks of the kind office teams hand to an AI assistant."),
 dict(id="data", name="Documents and data analysis", bench="lb_data", also=["vectara", "arena_vision"],
      desc="Working with spreadsheets, tables, reports and images of documents, and staying faithful to the source."),
 dict(id="assistant", name="Everyday assistant and chat", bench="arena_text", also=["aa_index"],
      desc="Drafting, explaining and answering questions in conversation: what most staff use AI for day to day."),
 dict(id="reasoning", name="Hard reasoning, maths and science", bench="frontiermath", also=["gpqa", "arc2"],
      desc="Problems that need long, careful reasoning: engineering calculations, proofs and technical analysis."),
]

STEPS = [
 ("Gather from the source", "Four research agents read each benchmark's own leaderboard or data file and each developer's model and price pages. Every value was copied as published, with the address it came from."),
 ("Use maintainers' results", "Rankings use the results each benchmark publishes on its own board. Scores that developers report about their own models in announcements or model cards are not used. Some boards accept submitted runs; their notes say so."),
 ("Match names carefully", "Benchmarks spell model names differently. Each name is matched to one entry. Earlier snapshots, previews, quantised builds and products not sold through the API are kept apart. When a model appears at several reasoning-effort settings, it is ranked on its best setting, which is shown with the score."),
 ("Red-team before publishing", "Two further agents that did not collect the data re-checked values against the source pages and challenged the name matches, prices, costs and wording. Errors they found are fixed, or the value is removed, before publication."),
]

DISCLAIMER = ("Benchmarks measure narrow tasks under one set of conditions, and results move quickly as models and agent tools change. "
              "Gaps of a few points are often within the margin of error. A model that ranks first here may not be the best on your own documents, "
              "processes or data. List prices change and some are introductory; open-weight prices depend on the host. "
              "Several well-known boards are not used to rank: SWE-bench, SWE-Bench Pro, OSWorld, tau-bench, BFCL and Aider have results for few or none "
              "of the models listed here, and METR's time-horizon board is no longer updated. This page is general information, not purchasing advice. "
              "Chmltech has no commercial relationship with any model developer or benchmark listed.")

# Facts from the research notes that a reader needs next to the number (vendor.notes.md, index.notes.md, red-team review).
# (text, applies to the price)
MODEL_NOTES = {
 "gemini-4-carbon": ("Introductory price until Nov 30, 2026; $4.00 input / $20.00 output from Dec 1, 2026.", True),
 "gemini-4-argon": ("Introductory price until Nov 30, 2026; $4.00 input / $20.00 output from Dec 1, 2026.", True),
 "gemini-3-8-flash": ("Introductory price until Dec 31, 2026; $1.50 input / $7.50 output from Jan 1, 2027.", True),
 "deepseek-v4-1-flash": ("Peak-hour price shown; DeepSeek charges half outside peak hours.", True),
 "deepseek-v4-pro": ("Peak-hour price shown; DeepSeek charges half outside peak hours.", True),
 "minimax-m3": ("Price shown is after MiniMax's listed permanent 50% discount.", True),
 "claude-haiku-5-5": ("Price shown is for prompts up to 100,000 tokens; longer prompts cost $0.50 input / $2.50 output.", True),
 "command-a-plus": ("Price from the Command A+ card on cohere.com/pricing (the card's internal id is 'command-a', so it may still carry the earlier Command A price). OpenRouter lists Cohere's own endpoint at $0.30 input / $1.50 output.", True),
 "mistral-large-4": ("Open weights under the Mistral Ecosystem Open Weight Licence; offering the model as a paid hosted service needs a commercial licence from Mistral. Release date from Mistral's documentation (Artificial Analysis and Epoch list Oct 29, 2026).", False),
 "muse-wonder": ("Results are for Muse Wonder on Meta's API. A higher-capability 'Muse Wonder Full', available only inside Muse Code, scores higher on several boards and is not listed here.", False),
 "muse-spark-open": ("Weights are gated on Hugging Face under the muse-model-license; the licence terms could not be read.", False),
 "grok-build-0-1": ("A coding-focused model (API alias grok-code-fast-1).", False),
 "qwen3-8-max": ("Some boards test the 0902 snapshot, others the original release; the snapshot is shown with each score.", False),
 "claude-fable-5-2": ("Epoch AI's results come from pre-launch testing, which Epoch says may change.", False),
 "claude-mythos-5-2": ("Limited access: offered to selected organisations only.", False),
 "kimi-k3-1-pro": ("Epoch AI ran this model through the Together API; those results are labelled.", False),
}
# Price corrections from the red-team values check (live OpenRouter endpoint API and Google pricing page, 2026-11-12).
OR_EP = "https://openrouter.ai/api/v1/models/{}/endpoints"
GPRICE = "https://ai.google.dev/gemini-api/docs/pricing#{}"
PRICE_FIX = {
 "granite-4-2-8b": dict(pin=0.06, pout=0.15, pprov="CoreWeave via OpenRouter (lowest full-precision host listed); secondary source", purl=OR_EP.format("ibm-granite/granite-4.2-8b")),
 "hy4": dict(pin=0.834, pout=2.501, pprov="Tencent's own endpoint on OpenRouter, before its current 50% discount; secondary source", purl=OR_EP.format("tencent/hy4"),
             pnote="Tencent's endpoint currently shows a 50% discount ($0.417 input / $1.25 output)."),
 "gemini-4-carbon": dict(purl=GPRICE.format("gemini-4-carbon")),
 "gemini-4-argon": dict(purl=GPRICE.format("gemini-4-argon")),
 "gemini-3-8-flash": dict(purl=GPRICE.format("gemini-3.8-flash")),
 "gemini-3-5-flash-lite": dict(purl=GPRICE.format("gemini-3.5-flash-lite")),
}
LICENCE = {"muse-spark-open": "muse-model-license (gated)"}
RELEASE = {"qwen3-8-max": ("2026-08", "Release month: Epoch AI dates the original release Aug 2, 2026 and the 0902 snapshot Sep 1, 2026."),
           "beam-1-0": ("2026-10", "Release month: Artificial Analysis gives Oct 16, 2026 and Epoch AI Oct 5, 2026.")}


def tidy(setl):
    """'compute_effort=high' / 'xhigh' / 'reasoning_effort=0.99' -> 'High' / 'X-high' / 'Effort 0.99' (labels only; scores untouched)."""
    if not setl: return None
    parts = []
    for x in (y.strip() for y in str(setl).split(",")):
        if not x or x in ("None", "—", "-"): continue
        x = re.sub(r"\b(compute|reasoning)_effort=", "", x).replace("_", " ").strip()
        if re.fullmatch(r"[\d.]+", x): x = "Effort " + x
        x = re.sub(r"\bx-?high\b", "X-high", x, flags=re.I)
        parts.append(x if x.lower().startswith("via ") else x[:1].upper() + x[1:])
    return ", ".join(parts) or None


def money_round(x):
    return None if x is None else float(f"{x:.4g}")


def first(recs, key):
    for r in recs:
        if r.get(key) not in (None, "", []):
            return r[key], r
    return None, None


def build():
    V = load("vendor.models.json")
    IM = load("index.models.json")
    rows = [r for r in load("arena.scores.json") if r["benchmark"] not in FULL_ARENA] + load("arena_full.scores.json") + \
        load("index.scores.json") + load("agentic.scores.json")
    by_board = {}
    for r in rows:
        by_board.setdefault(r["benchmark"], []).append(r)

    models = []
    for c in CATALOG:
        recs = [r for n in c["vendor"] for r in V if r["model_as_listed"] == n]
        prim = [r for r in recs if r["source_type"] == "primary"] + [r for r in recs if r["source_type"] != "primary"]
        priced = [r for r in prim if r.get("price_input_usd_per_mtok") is not None]
        pr = priced[0] if priced else None
        im = [r for r in IM if match(r["model_as_listed"])[0] == c["id"]]
        access = first(prim, "access")[0] or first(im, "access")[0]
        released, _ = first(prim, "release_date")
        rel_note = None
        if not released:
            released, _ = first(im, "release_date")
            if released: rel_note = "Release date as listed by Artificial Analysis."
        if c["id"] in RELEASE:
            released, rel_note = RELEASE[c["id"]]
        ctx = first(prim, "context_window_tokens")[0]
        inp = first(prim, "input_modalities")[0] or []
        reasoning = first(prim, "reasoning")[0]
        spec_rec = prim[0] if prim else None
        caps = []
        if reasoning in ("Yes", "Configurable"): caps.append("Reasoning mode")
        for k, lab in (("image", "Image input"), ("audio", "Audio input"), ("video", "Video input")):
            if k in inp: caps.append(lab)
        if any(r.get("computer_use") for r in prim): caps.append("Computer use")
        if ctx and ctx >= 1_000_000: caps.append("1M+ token context")
        note, price_flag = MODEL_NOTES.get(c["id"], (None, False))
        notes = [x for x in (note, rel_note) if x]
        pprov = pr["price_provider"] if pr else None
        if pr and pr["source_type"] != "primary":
            pprov = (pprov or "") + "; secondary source: no developer price list could be read"
        m = dict(id=c["id"], name=c["name"], dev=c["dev"], tier=c["tier"], access=access or "Proprietary API",
                 license=LICENCE.get(c["id"]) or first(prim, "license")[0], params=first(prim, "parameters")[0], released=released,
                 status=first(prim, "status")[0], ctx=ctx, maxout=first(prim, "max_output_tokens")[0],
                 inp=[x for x in inp if x in ("text", "image", "audio", "video", "pdf")], reasoning=reasoning, cutoff=first(prim, "knowledge_cutoff")[0],
                 caps=caps, pin=pr["price_input_usd_per_mtok"] if pr else None, pout=pr["price_output_usd_per_mtok"] if pr else None,
                 pprov=pprov, purl=pr["source_url"] if pr else None, pnote=note if price_flag else None,
                 surl=spec_rec["source_url"] if spec_rec else None, notes=" ".join(notes) or None, s={})
        for k, v in PRICE_FIX.get(c["id"], {}).items():
            m[k] = v
        if c["id"] == "hy4": m["notes"] = " ".join(x for x in (m["notes"], m["pnote"]) if x)
        models.append(m)
    M = {m["id"]: m for m in models}
    snapshot_of = {c["id"]: c.get("snapshots") for c in CATALOG}

    benches = []
    for (bid, board, name, short, section, unit, hb, scale, costmode, what, caveat, src, url, datetext) in B:
        rs = by_board.get(board, [])
        dates = sorted({r["result_date"][:10] for r in rs if r.get("result_date") and re.match(r"\d{4}-\d{2}-\d{2}", r["result_date"])})
        cand = {}
        for r in rs:
            if r.get("self_reported"):
                continue
            mid, setting = match(r["model_as_listed"], board)
            if mid:
                cand.setdefault(mid, []).append((r, setting))
        n_tasks = set()
        for mid, lst in cand.items():
            snaps = snapshot_of.get(mid)
            if snaps:  # prefer rows that name the current snapshot over undated rows
                dated = [x for x in lst if any(s in x[0]["model_as_listed"] for s in snaps)]
                if dated: lst = dated
            best, alts = None, []
            for r, setting in lst:
                v = r["score"] * scale
                cost = r.get("cost_per_task_usd") or None  # a $0 cost is a placeholder price on the source (red-team finding)
                if costmode in ("trials", "suite"):
                    cost = r["cost_total_usd"] / r["votes_or_n"] if r.get("cost_total_usd") is not None and r.get("votes_or_n") else None
                    if r.get("votes_or_n"): n_tasks.add(r["votes_or_n"])
                if costmode is None:
                    cost = None
                setl = tidy(setting or r.get("setting"))
                host = re.search(r"via \w+", setting or "")
                if host and "via " not in (setl or "").lower():
                    setl = (setl + ", " if setl else "") + host.group(0)
                if r.get("scaffold") and bid in ("aa_coding", "tbench"):
                    setl = tidy(r["scaffold"] + (", " + setl if setl else ""))
                rec = dict(v=round(v, 3), set=setl, cost=money_round(cost), url=r["source_url"])
                if r.get("score_ci"): rec["ci"] = r["score_ci"]
                if bid in EPOCH and mid == "claude-fable-5-2": rec["flag"] = "Pre-launch evaluation; Epoch AI says it may change."
                if cost is not None: alts.append([rec["v"], rec["cost"], setl])
                if best is None or (v > best["v"] if hb else v < best["v"]):
                    best = rec
            if len(alts) > 1: best["alt"] = sorted(alts, key=lambda a: a[1])
            M[mid]["s"][bid] = best
        cav = caveat
        if caveat == "LB":
            n = " or ".join(str(x) for x in sorted(n_tasks)) or "?"
            cav = (f"A single run of {n} tasks per model, so a difference of a few points can be one task. Cost here is derived: LiveBench's total suite cost "
                   "divided by its task count, as the LiveBench site itself does.")
        upd = datetext or ("results as of " + d(dates[-1]) if dates else None)
        benches.append(dict(id=bid, name=name, short=short, section=section, unit=unit, hb=hb,
                            cost=any(bid in m["s"] and m["s"][bid]["cost"] is not None for m in models),
                            derived=costmode in ("trials", "suite"), what=what, caveat=cav, src=src, url=url, updated=upd,
                            n=sum(1 for m in models if bid in m["s"])))

    out = dict(as_of=AS_OF, default_benchmark="aa_index", models=models, benchmarks=benches, groups=GROUPS, method_steps=STEPS, disclaimer=DISCLAIMER)
    json.dump(out, open(os.path.join(HERE, "llm.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"llm.json: {len(models)} models, {len(benches)} benchmarks, {sum(len(m['s']) for m in models)} results")
    for b in benches: print(f"  {b['id']:13} {b['n']:3} models  cost={b['cost']}  {b['updated']}")
    print("  no price:", [m["name"] for m in models if m["pin"] is None])
    print("  no results:", [m["name"] for m in models if not m["s"]])


if __name__ == "__main__":
    build()
