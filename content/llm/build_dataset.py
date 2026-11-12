"""Build content/llm/llm.json for llm-leaderboard.html from the research files in content/llm/raw/.

Research files (one set per research agent, spec in content/llm/SPEC.md):
  vendor.*  developer model pages and price lists (specs, prices)
  arena.*   Arena (arena.ai) leaderboards, from Arena's published dataset
  index.*   Artificial Analysis, Epoch AI, Vals AI, Vectara, LiveBench
  agentic.* SWE-bench, Terminal-Bench, OSWorld, tau-bench, BFCL, Aider, METR, ARC-AGI, Vending-Bench
Rules applied here (also stated on the page):
  - Only maintainer-run results are ranked; developer self-reported scores are not used.
  - A model listed at several reasoning-effort settings is ranked on its best setting; the setting is shown.
  - Fractions (0-1) are shown as percentages. No other change is made to any score.
  - Cost per task is the benchmark's own figure, except where a board publishes only a total (LiveBench, Terminal-Bench):
    there it is total cost / number of tasks (or trials), marked "derived" in the benchmark notes.
Run: python3 content/llm/build_dataset.py   (from the site root)
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from catalog import CATALOG
from match import match

RAW = os.path.join(HERE, "raw")
AS_OF = "2026-11-11"
load = lambda p: json.load(open(os.path.join(RAW, p), encoding="utf-8"))

# id, board name in the research file, display name, short name, section, unit, higher-is-better, scale, cost mode, what, caveat, source label
B = [
 ("aa_index", "Artificial Analysis Intelligence Index v5.0.1", "Artificial Analysis Intelligence Index", "AA Intelligence Index", "General capability", "points", True, 1, "task",
  "A combined score from nine independent evaluations of reasoning, knowledge, coding and agentic work, run by Artificial Analysis on each model.",
  "Cost per task is Artificial Analysis's weighted average API cost per Index task.", "Artificial Analysis", "https://artificialanalysis.ai/leaderboards/models"),
 ("arena_text", "Arena Text (style control, default view)", "Arena Text", "Arena Text", "General capability", "Elo", True, 1, None,
  "Human preference: people compare two anonymous answers to their own prompts and pick the better one. Ratings on an Elo-like scale; style control adjusts for answer length and formatting.",
  "Only the top 60 of the board are recorded, so smaller models may be missing.", "Arena (arena.ai)", "https://arena.ai/leaderboard/text"),
 ("eci", "Epoch Capabilities Index (ECI)", "Epoch Capabilities Index", "Epoch ECI", "General capability", "points", True, 1, None,
  "Epoch AI's single capability score, fitted across many benchmarks so models tested on different sets can be compared.", None, "Epoch AI", "https://epoch.ai/benchmarks"),
 ("vals", "Vals Index v2.2", "Vals Index", "Vals Index", "Business and knowledge work", "%", True, 1, "task",
  "Agentic tasks in finance, law, tax and software, weighted by each sector's share of US GDP, run by Vals AI.",
  "Cost per task is Vals's published cost per test.", "Vals AI", "https://www.vals.ai/benchmarks/vals_index"),
 ("aa_coding", "Artificial Analysis Coding Agent Index", "Artificial Analysis Coding Agent Index", "AA Coding Agent", "Coding and software", "%", True, 100, "task",
  "Models run inside coding-agent tools on three evaluations: FrontierCode, SWE-Atlas QnA and Terminal-Bench v4. The tool used is shown with each score.",
  "Cost per task is Artificial Analysis's average API cost per task.", "Artificial Analysis", "https://artificialanalysis.ai/"),
 ("tbench", "Terminal-Bench 4.1", "Terminal-Bench 4.1", "Terminal-Bench", "Coding and software", "%", True, 1, "trials",
  "Real tasks in a computer terminal: building software, configuring systems, fixing environments. Share of tasks solved, run in named agent tools.",
  "Cost per task is derived: the board's total cost divided by its number of trials.", "Terminal-Bench (tbench.ai)", "https://www.tbench.ai/"),
 ("arena_webdev", "Arena WebDev / Code Arena", "Arena WebDev", "Arena WebDev", "Coding and software", "Elo", True, 1, None,
  "Human preference for web apps the models build from a prompt, judged side by side.", "Only the top 60 of the board are recorded.", "Arena (arena.ai)", "https://arena.ai/leaderboard/webdev"),
 ("lb_coding", "LiveBench 2.0 - coding", "LiveBench Coding", "LiveBench Coding", "Coding and software", "points", True, 1, "suite",
  "Fresh coding tasks released after model training cut-offs, scored automatically (0 to 100).", "Cost per task is derived: LiveBench's total suite cost divided by its task count, as the LiveBench site itself does.", "LiveBench", "https://livebench.ai/"),
 ("arena_agent", "Arena Agent (aggregate)", "Arena Agent", "Arena Agent", "Agents", "%", True, 100, None,
  "Real agent sessions on arena.ai: how much better each model does than a baseline at finishing users' multi-step tasks, from task outcomes and user feedback.",
  None, "Arena (arena.ai)", "https://arena.ai/leaderboard/agent"),
 ("lb_browser", "LiveBench 2.0 - browser", "LiveBench Browser", "LiveBench Browser", "Agents", "points", True, 1, "suite",
  "Tasks completed by operating a web browser: navigating, filling forms and extracting information (0 to 100).", "Cost per task is derived: total suite cost divided by task count.", "LiveBench", "https://livebench.ai/"),
 ("lb_research", "LiveBench 2.0 - research", "LiveBench Research", "LiveBench Research", "Agents", "points", True, 1, "suite",
  "Multi-step research tasks that need searching, reading and combining sources (0 to 100).", "Cost per task is derived: total suite cost divided by task count.", "LiveBench", "https://livebench.ai/"),
 ("lb_long", "LiveBench 2.0 - long_agentic", "LiveBench Long Agentic", "LiveBench Long Agentic", "Agents", "points", True, 1, "suite",
  "Long tasks with many steps and tool calls, testing whether an agent stays on track (0 to 100).", "Cost per task is derived: total suite cost divided by task count.", "LiveBench", "https://livebench.ai/"),
 ("vending", "Vending-Bench 2", "Vending-Bench 2", "Vending-Bench", "Agents", "USD", True, 1, "task",
  "A simulated year running a vending-machine business: ordering stock, setting prices, dealing with suppliers. Score is the money left at the end (start: $500).",
  "Cost per task is the mean API cost of one full simulated year.", "Andon Labs", "https://andonlabs.com/evals/vending-bench-2"),
 ("lb_data", "LiveBench 2.0 - data_analysis", "LiveBench Data Analysis", "LiveBench Data", "Documents and data", "points", True, 1, "suite",
  "Table manipulation, joins and analysis questions on real data (0 to 100).", "Cost per task is derived: total suite cost divided by task count.", "LiveBench", "https://livebench.ai/"),
 ("arena_vision", "Arena Vision (style control, default view)", "Arena Vision", "Arena Vision", "Documents and data", "Elo", True, 1, None,
  "Human preference on prompts that include images, such as charts, photos and screenshots.", "Only the top 60 of the board are recorded.", "Arena (arena.ai)", "https://arena.ai/leaderboard/vision"),
 ("vectara", "Vectara Hallucination Leaderboard (HHEM)", "Vectara Hallucination Rate", "Hallucination rate", "Documents and data", "%", False, 1, None,
  "How often a model adds facts that are not in a document it is asked to summarise. Lower is better.", None, "Vectara", "https://github.com/vectara/hallucination-leaderboard"),
 ("frontiermath", "FrontierMath Tiers 1-3 v2 (Epoch AI)", "FrontierMath (Tiers 1-3)", "FrontierMath", "Reasoning, maths and science", "%", True, 100, None,
  "Hundreds of unpublished, expert-written maths problems that take specialists hours to solve, run by Epoch AI.", None, "Epoch AI", "https://epoch.ai/benchmarks"),
 ("gpqa", "GPQA Diamond (Epoch AI run)", "GPQA Diamond", "GPQA Diamond", "Reasoning, maths and science", "%", True, 100, None,
  "Graduate-level biology, chemistry and physics questions written to resist web search, run by Epoch AI.", "Top models are close to the ceiling, so small gaps mean little.", "Epoch AI", "https://epoch.ai/benchmarks"),
 ("arc2", "ARC-AGI-2 (Semi-Private)", "ARC-AGI-2", "ARC-AGI-2", "Reasoning, maths and science", "%", True, 100, "task",
  "Visual puzzles that are easy for people but need new reasoning for each task, run by the ARC Prize Foundation.", "Cost per task is ARC Prize's measured cost per task.", "ARC Prize", "https://arcprize.org/leaderboard"),
]

GROUPS = [
 dict(id="coding", name="Coding agents", bench="aa_coding", also=["tbench", "lb_coding"],
      desc="Agents that read a codebase, write and test changes, and work in the terminal, as in Claude Code, Codex or Cursor."),
 dict(id="apps", name="Web and app builders", bench="arena_webdev", also=["lb_coding"],
      desc="Tools that turn a description into a working web page or small app, judged by the people who asked for it."),
 dict(id="browser", name="Browser and computer use", bench="lb_browser", also=["arena_agent"],
      desc="Agents that operate a browser for you: navigating sites, filling forms and pulling information out."),
 dict(id="research", name="Research agents", bench="lb_research", also=["frontiermath"],
      desc="Agents that search, read many sources and pull the findings together into a cited answer."),
 dict(id="long", name="Long-running autonomous agents", bench="vending", also=["lb_long", "arena_agent"],
      desc="Agents trusted with a goal over hours or days, making many decisions without a person checking each one."),
 dict(id="business", name="Business and knowledge work", bench="vals", also=["aa_index"],
      desc="Finance, legal, tax and analysis tasks of the kind office teams hand to an AI assistant."),
 dict(id="data", name="Documents and data analysis", bench="lb_data", also=["vectara", "arena_vision"],
      desc="Working with spreadsheets, tables, reports and scanned documents, and staying faithful to the source."),
 dict(id="assistant", name="Everyday assistant and chat", bench="arena_text", also=["aa_index"],
      desc="Drafting, explaining and answering questions in conversation: what most staff use AI for day to day."),
 dict(id="reasoning", name="Hard reasoning, maths and science", bench="frontiermath", also=["gpqa", "arc2"],
      desc="Problems that need long, careful reasoning: engineering calculations, proofs and technical analysis."),
]

STEPS = [
 ("Gather from the source", "Four research agents read each benchmark's own leaderboard or data file and each developer's model and price pages. Every value was copied as published, with the address it came from."),
 ("Use independent results only", "Rankings use results run by the benchmark maintainers. Scores that developers report about their own models are not used, because settings and comparisons vary."),
 ("Match names carefully", "Benchmarks spell model names differently. Names are matched to one entry per model. When a model appears at several reasoning-effort settings, it is ranked on its best setting, which is shown next to the score."),
 ("Red-team the result", "A separate team of agents, which did not collect the data, re-checked values against the source pages and challenged name matches, prices and the frontier. Errors found were fixed or the value was removed."),
]

DISCLAIMER = ("Benchmarks measure narrow tasks under one set of conditions, and results move quickly as models and harnesses change. "
              "A model that ranks first here may not be the best on your own documents, processes or data. List prices change and some are introductory; "
              "open-weight prices depend on the host. Several well-known boards (SWE-bench, OSWorld, tau-bench, BFCL, METR and Aider) have not yet published "
              "results for most of the models listed, so they are not used to rank. This page is general information, not purchasing advice. "
              "Chmltech has no commercial relationship with any model developer or benchmark listed.")


def tidy(setl):
    """'compute_effort=high' / 'xhigh' / 'Max' -> 'High' / 'X-high' / 'Max' (labels only; scores untouched)."""
    if not setl: return None
    setl = ", ".join(x for x in (y.strip() for y in str(setl).split(",")) if x and x not in ("None", "—", "-") and not re.fullmatch(r"[\d.]+", x))
    if not setl: return None
    t = re.sub(r"\b(compute|reasoning)_effort=", "", setl).replace("_", " ").strip()
    t = re.sub(r"\bx-?high\b", "X-high", t, flags=re.I)
    return t[:1].upper() + t[1:] if t else None


def money_round(x):
    return None if x is None else float(f"{x:.4g}")


def pick_vendor(names, V):
    recs = []
    for n in names:
        recs += [r for r in V if r["model_as_listed"] == n]
    return recs


def first(recs, key):
    for r in recs:
        if r.get(key) not in (None, "", []):
            return r[key], r
    return None, None


def build():
    V = load("vendor.models.json")
    IM = load("index.models.json")
    rows = load("arena.scores.json") + load("index.scores.json") + load("agentic.scores.json")
    by_board = {}
    for r in rows:
        by_board.setdefault(r["benchmark"], []).append(r)

    models = []
    for c in CATALOG:
        recs = pick_vendor(c["vendor"], V)
        prim = [r for r in recs if r["source_type"] == "primary"] + [r for r in recs if r["source_type"] != "primary"]
        priced = [r for r in prim if r.get("price_input_usd_per_mtok") is not None]
        pr = priced[0] if priced else None
        im = [r for r in IM if match(r["model_as_listed"])[0] == c["id"]]
        access = first(prim, "access")[0] or first(im, "access")[0]
        released, rsrc = first(prim, "release_date")
        if not released:
            released, rsrc = first(im, "release_date")
        ctx = first(prim, "context_window_tokens")[0]
        inp = first(prim, "input_modalities")[0] or []
        reasoning = first(prim, "reasoning")[0]
        status = first(prim, "status")[0]
        spec_rec = prim[0] if prim else None
        caps = []
        if reasoning in ("Yes", "Configurable"): caps.append("Reasoning mode")
        for k, lab in (("image", "Image input"), ("audio", "Audio input"), ("video", "Video input")):
            if k in inp: caps.append(lab)
        if any(r.get("computer_use") for r in prim): caps.append("Computer use")
        if ctx and ctx >= 1_000_000: caps.append("1M+ token context")
        notes = []
        if pr and pr.get("price_notes"): notes.append("Price: " + pr["price_notes"])
        if rsrc is not None and rsrc in im: notes.append("Release date as listed by Artificial Analysis.")
        m = dict(id=c["id"], name=c["name"], dev=c["dev"], tier=c["tier"], access=access or "Proprietary API",
                 license=first(prim, "license")[0], params=first(prim, "parameters")[0], released=released, status=status,
                 ctx=ctx, maxout=first(prim, "max_output_tokens")[0], inp=[x for x in inp if x in ("text", "image", "audio", "video", "pdf")],
                 reasoning=reasoning, cutoff=first(prim, "knowledge_cutoff")[0], caps=caps,
                 pin=pr["price_input_usd_per_mtok"] if pr else None, pout=pr["price_output_usd_per_mtok"] if pr else None,
                 pprov=pr["price_provider"] if pr else None, purl=pr["source_url"] if pr else None,
                 surl=spec_rec["source_url"] if spec_rec else None, notes=" ".join(notes) or None, s={})
        models.append(m)
    M = {m["id"]: m for m in models}

    benches, unmatched = [], {}
    for (bid, board, name, short, section, unit, hb, scale, costmode, what, caveat, src, url) in B:
        rs = by_board.get(board, [])
        dates = sorted({r["result_date"][:10] for r in rs if r.get("result_date") and re.match(r"\d{4}-\d{2}-\d{2}", r["result_date"])})
        has_cost = False
        for r in rs:
            if r.get("self_reported"):
                continue
            mid, setting = match(r["model_as_listed"])
            if not mid:
                unmatched.setdefault(bid, []).append(r["model_as_listed"]); continue
            v = r["score"] * scale
            cost = r.get("cost_per_task_usd")
            if costmode in ("trials", "suite") and r.get("cost_total_usd") is not None and r.get("votes_or_n"):
                cost = r["cost_total_usd"] / r["votes_or_n"]
            if costmode is None:
                cost = None
            setl = tidy(setting or (r.get("setting") or None))
            if r.get("scaffold") and bid in ("aa_coding", "tbench"):
                setl = (r["scaffold"] + (", " + setl if setl else ""))
            cur = M[mid]["s"].get(bid)
            if cur is None or (v > cur["v"] if hb else v < cur["v"]):
                M[mid]["s"][bid] = dict(v=round(v, 3), set=setl, cost=money_round(cost), url=r["source_url"])
            has_cost = has_cost or cost is not None
        upd = dates[-1] if dates else None
        if bid == "eci": upd = "2026-11-11"
        if bid.startswith("lb_"): upd = "2026-11-06"
        if bid in ("aa_index", "aa_coding", "vending"): upd = AS_OF  # boards show no update date; date retrieved
        if bid == "tbench": upd = "2026-11-11"  # leaderboard record updated_at (latest result 2026-09-29)
        benches.append(dict(id=bid, name=name, short=short, section=section, unit=unit, hb=hb, cost=has_cost, what=what, caveat=caveat,
                            src=src, url=url, updated=fmt_date(upd), n=sum(1 for m in models if bid in m["s"])))

    for m in models:
        m["s"] = {k: v for k, v in m["s"].items()}
    out = dict(as_of=AS_OF, default_benchmark="aa_index", models=models, benchmarks=benches, groups=GROUPS, method_steps=STEPS, disclaimer=DISCLAIMER)
    json.dump(out, open(os.path.join(HERE, "llm.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"llm.json: {len(models)} models, {len(benches)} benchmarks, {sum(len(m['s']) for m in models)} results")
    for b in benches: print(f"  {b['id']:13} {b['n']:3} models  cost={b['cost']}  updated={b['updated']}")
    print("  no price:", [m["name"] for m in models if m["pin"] is None])
    print("  no results:", [m["name"] for m in models if not m["s"]])


def fmt_date(d):
    if not d: return None
    import datetime
    return datetime.date.fromisoformat(d).strftime("%b %-d, %Y")


if __name__ == "__main__":
    build()
