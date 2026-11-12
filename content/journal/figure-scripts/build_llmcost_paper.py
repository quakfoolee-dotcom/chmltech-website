"""Build the journal paper JSON for Vol. 104(7): Score Versus Cost Per Task.
Text uses [@key] citations; they are numbered in order of first use. Tables are computed from data/llmcost/*.csv.
Run: python3 -I build_llmcost_paper.py"""
import csv, json, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data", "llmcost")
SLUG = "score-versus-cost-per-task-returns-to-reasoning-effort-in-frontier-language-models"
OUT = os.path.join(HERE, "..", SLUG + ".json")
rd = lambda n: list(csv.DictReader(open(os.path.join(D, n + ".csv"), encoding="utf-8")))
BENCH, IDX, PRICE, REFS = rd("benchmarks"), rd("indexes"), rd("pricing"), rd("references")
EORD = ["none", "minimal", "low", "medium", "high", "xhigh", "max"]
ENAME = {"minimal": "Minimal", "low": "Low", "medium": "Medium", "high": "High", "xhigh": "Xhigh", "max": "Max"}
eff = lambda s: s.lower().split(" ")[0].strip(",")
se = lambda p, n: 100 * math.sqrt(p / 100 * (1 - p / 100) / n)
money = lambda v: f"${v:,.2f}"

# ---------------- references ----------------
def apa_authors(a):
    xs = [x.strip() for x in a.split(";")]
    if len(xs) > 7: return ", ".join(xs[:6]) + ", … " + xs[-1]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + ", & " + xs[-1]
LIT = {r["url"]: r for r in REFS}
def lit(url, venue=None):
    r = LIT[url]
    v = venue or r["venue"].split(";")[0].replace(" (per arXiv comment field)", "")
    return dict(text=f'{apa_authors(r["authors"])} ({r["year"]}). {r["title"]}. <em>{v}</em>.', url=url)
REF = {
 "cop": lit("https://arxiv.org/abs/2504.13359", "arXiv preprint arXiv:2504.13359"),
 "matter": lit("https://arxiv.org/abs/2407.01502", "arXiv preprint arXiv:2407.01502"),
 "hal": lit("https://arxiv.org/abs/2510.11977", "arXiv preprint arXiv:2510.11977"),
 "frugal": lit("https://arxiv.org/abs/2305.05176", "arXiv preprint arXiv:2305.05176"),
 "progress": lit("https://arxiv.org/abs/2511.23455", "arXiv preprint arXiv:2511.23455"),
 "epoch": dict(text="Cottier, B., Snodin, B., Owen, D., & Adamczewski, T. (2025, March 12). LLM inference prices have fallen rapidly but unequally across tasks. <em>Epoch AI Data Insights</em>.", url="https://epoch.ai/data-insights/llm-inference-price-trends"),
 "aiindex": dict(text="Maslej, N., Fattorini, L., Perrault, R., Gil, Y., Parli, V., Kariuki, N., … Oak, S. (2025). <em>Artificial Intelligence Index Report 2025</em>. AI Index Steering Committee, Stanford Institute for Human-Centered AI.", url="https://hai.stanford.edu/ai-index/2025-ai-index-report"),
 "inverse": lit("https://arxiv.org/abs/2507.14417", "Transactions on Machine Learning Research"),
 "hassid": lit("https://arxiv.org/abs/2505.17813", "arXiv preprint arXiv:2505.17813"),
 "illusion": lit("https://arxiv.org/abs/2506.06941", "Advances in Neural Information Processing Systems (NeurIPS 2025)"),
 "longhorizon": lit("https://arxiv.org/abs/2509.09677", "International Conference on Learning Representations (ICLR 2026)"),
 "overthink": lit("https://arxiv.org/abs/2412.21187", "arXiv preprint arXiv:2412.21187"),
 "nothink": lit("https://arxiv.org/abs/2504.09858", "arXiv preprint arXiv:2504.09858"),
 "inflaws": lit("https://arxiv.org/abs/2408.00724", "arXiv preprint arXiv:2408.00724"),
 "monkeys": lit("https://arxiv.org/abs/2407.21787", "arXiv preprint arXiv:2407.21787"),
 "arc2024": lit("https://arxiv.org/abs/2412.04604", "arXiv preprint arXiv:2412.04604"),
 "aa": dict(text="Artificial Analysis. (2026). <em>Benchmarking methodology</em>. Retrieved November 11, 2026.", url="https://artificialanalysis.ai/methodology"),
 "aaidx": dict(text="Artificial Analysis. (2026). <em>Intelligence benchmarking methodology (Intelligence Index v5.0.1)</em>. Retrieved November 11, 2026.", url="https://artificialanalysis.ai/methodology/intelligence-benchmarking"),
 "valsblog": dict(text="Liang, D. (2026, November 3). How much does reasoning effort affect score and cost? <em>Vals AI Research</em>.", url="https://www.vals.ai/blogs/reasoning-effort"),
 "valsidx": dict(text="Vals AI. (2026). <em>Vals Index (v2.2): Leaderboard and methodology</em>. Retrieved November 11, 2026.", url="https://www.vals.ai/benchmarks/vals_index"),
 "cognition": dict(text="Cognition. (2026). <em>FrontierCode 2.0</em> [Benchmark results and data file]. Retrieved November 11, 2026.", url="https://cognition.com/frontiercode"),
 "arclb": dict(text="ARC Prize Foundation. (2026). <em>ARC-AGI leaderboard</em> [Evaluation data]. Retrieved November 11, 2026.", url="https://arcprize.org/leaderboard"),
 "arc2": dict(text="ARC Prize Foundation. (2026). <em>ARC-AGI-2</em>. Retrieved November 11, 2026.", url="https://arcprize.org/arc-agi/2/"),
 "arcpolicy": dict(text="ARC Prize Foundation. (2026). <em>Testing policy</em>. Retrieved November 11, 2026.", url="https://arcprize.org/policy"),
 "card": dict(text="Anthropic. (2026, November 9). <em>System card: Claude Fable 5.2 &amp; Claude Mythos 5.2</em>.", url="https://assets.claude.com/27d60918d218125e7504bc7354c4b4626ec56b11.pdf"),
 "launch": dict(text="Anthropic. (2026, November 9). <em>Claude Fable and Mythos 5.2</em> [Product announcement].", url="https://www.anthropic.com/claude-fable-and-mythos-5-2"),
 "anthprice": dict(text="Anthropic. (2026). <em>Pricing</em>. Claude Platform documentation. Retrieved November 11, 2026.", url="https://platform.claude.com/docs/en/about-claude/pricing"),
 "oaiprice": dict(text="OpenAI. (2026). <em>Pricing</em>. OpenAI Platform documentation. Retrieved November 11, 2026.", url="https://platform.openai.com/docs/pricing"),
 "gprice": dict(text="Google. (2026). <em>Gemini Developer API pricing</em>. Retrieved November 11, 2026.", url="https://ai.google.dev/gemini-api/docs/pricing"),
 "arena": dict(text="LMArena. (2026). <em>leaderboard-dataset</em> [Data set, revision 4217986]. Hugging Face. Retrieved November 11, 2026.", url="https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset"),
}

# ---------------- data ----------------
VALS = []
for x in IDX:
    if x["source"] == "Vals AI (reasoning-effort study)":
        VALS.append(dict(model=x["model"], effort=eff(x["variant_or_effort"]), acc=float(x["quality_value"]), cost=float(x["cost_value_usd"]),
                         se=float(re.search(r"standard error ([\d.]+)", x["notes"]).group(1))))
VMODELS = list(dict.fromkeys(v["model"] for v in VALS))
srt = lambda pts: sorted(pts, key=lambda p: EORD.index(p["effort"]))
LEAD = ["Claude Fable 5.2", "Claude Opus 5.5", "GPT-6 Astra", "Gemini 4 Carbon", "Claude Fable 5.1"]
FC = {}
for x in BENCH:
    if x["benchmark"] == "FrontierCode" and x["model"] in LEAD:
        e = eff(x["variant_or_effort"])
        if e not in EORD: continue
        k = (x["model"], e); FC.setdefault(k, {})
        FC[k]["vendor" if x["reported_by"] == "vendor" else "op"] = (float(x["score_pct"]), float(x["cost_per_task_usd"]))
def fc_cost(m, e):
    s, c = FC[(m, e)]["op"]
    return round(c / 1.25, 3) if m == "Claude Fable 5.2" else c

# Table 3: Vals results with cost per correct answer
t3 = []
for m in VMODELS:
    for p in srt([v for v in VALS if v["model"] == m]):
        t3.append([m, ENAME[p["effort"]], f'{p["acc"]:.1f} ± {1.96 * p["se"]:.1f}', money(p["cost"]), money(p["cost"] / (p["acc"] / 100))])
# Table 4: Vals steps
t4 = []; vsig = 0; vlast_noise = 0
for m in VMODELS:
    pts = srt([v for v in VALS if v["model"] == m])
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        d = b["acc"] - a["acc"]; z = d / math.hypot(a["se"], b["se"]); sig = abs(z) >= 1.96; vsig += sig
        if i == len(pts) - 2 and not sig: vlast_noise += 1
        t4.append([m, f'{ENAME[a["effort"]]} → {ENAME[b["effort"]]}', f"{d:+.1f}", f'{b["cost"] / a["cost"]:.2f}×', f"{z:+.2f}", "Yes" if sig else "No"])
# Table 5: Fable 5.2 two cost series
t5 = []
for e in ["low", "medium", "high", "xhigh", "max"]:
    s_op, c_op = FC[("Claude Fable 5.2", e)]["op"]; s_v, c_v = FC[("Claude Fable 5.2", e)]["vendor"]
    t5.append([ENAME[e], f"{s_v:.1f}", f"{s_op:.2f}", money(c_v), money(c_op), f"{c_op / c_v:.3f}"])
# Table 6: FrontierCode steps, lead models
t6 = []; fsig_t = fsig_a = 0
for m in LEAD:
    es = [e for e in EORD if (m, e) in FC and "op" in FC[(m, e)]]
    for a, b in zip(es, es[1:]):
        sa, sb = FC[(m, a)]["op"][0], FC[(m, b)]["op"][0]; d = sb - sa
        zt = d / math.hypot(se(sa, 132), se(sb, 132)); za = d / math.hypot(se(sa, 660), se(sb, 660))
        verdict = "Distinguishable" if abs(zt) >= 1.96 else ("Attempt bound only" if abs(za) >= 1.96 else "Within noise")
        fsig_t += abs(zt) >= 1.96; fsig_a += abs(za) >= 1.96
        t6.append([m.replace("Claude ", ""), f"{ENAME[a]} → {ENAME[b]}", f"{d:+.1f}", f"{fc_cost(m, b) / fc_cost(m, a):.2f}×", f"{zt:+.2f} / {za:+.2f}", verdict])
# Table 7: list prices (selected)
SEL = ["Claude Fable 5.2", "Claude Opus 5.5", "Claude Haiku 5.5", "Claude Fable 5.1", "GPT-6 Astra", "GPT-6.1 Sol", "GPT-6 Luna", "GPT-5.6 Sol",
       "Gemini 4 Carbon", "Gemini 3.8 Flash", "Grok 4.7", "DeepSeek V4 Pro", "GLM-5.3", "Mistral Large 4"]
NOTE = {"Gemini 4 Carbon": "Introductory; $4 / $20 from Dec 1, 2026", "Gemini 3.8 Flash": "Introductory; doubles from Jan 1, 2027",
        "GPT-5.6 Sol": "Promotional until Nov 30, 2026", "DeepSeek V4 Pro": "Peak rate; off-peak is half", "Claude Fable 5.1": "Legacy model",
        "Claude Haiku 5.5": "$0.50 / $2.50 above 100K-token prompts", "GPT-6 Astra": "Higher rates above 272K input tokens",
        "Grok 4.7": "Doubles at 200K prompt tokens or more"}
t7 = []
for m in SEL:
    r = next(x for x in PRICE if x["model"] == m and x["hosted_by"].lower().startswith("official"))
    v = r["vendor"].split(" (")[0]
    fmt = lambda s: ("$" + (f"{float(s):.2f}".rstrip("0").rstrip(".") if float(s) >= 1 else f"{float(s):.2f}")) if s else "—"
    t7.append([m, v, f'{fmt(r["input_per_mtok"])} / {fmt(r["output_per_mtok"])}', NOTE.get(m, "")])

# ---------------- text ----------------
ABSTRACT = ("Current large language models let the user choose a reasoning-effort setting, from low to maximum, and the setting changes how many tokens a task consumes. "
 "The price per million tokens is therefore a poor guide to what a task costs. This paper compares benchmark score with measured cost per task for current frontier and lower-cost models as of November 11, 2026. "
 "It draws on four sources that publish both quantities: a Vals AI study that ran seven models on the same tasks at three effort settings, Cognition's FrontierCode 2.0 coding benchmark, the ARC-AGI-2 reasoning benchmark and the Artificial Analysis Intelligence Index, with official list prices and Arena preference ratings as context. "
 "All values were collected from primary sources and re-checked field by field by an independent verifier. Uncertainty is estimated with binomial intervals, and each effort step is tested for a distinguishable change in score. "
 "Moving from the lowest to the highest setting typically multiplies cost per task by three to five. The lower steps often buy large, distinguishable gains, while the final step was within noise for six of seven models in the controlled study at 1.2 to 2.6 times the cost. "
 "On ARC-AGI-2, frontier models cluster between 90 and 95 percent and cannot be ranked. The paper concludes that effort should be treated as a tunable cost parameter, set by testing on a firm's own tasks rather than by default to the maximum.")

S = []
def sec(num, title, *blocks): S.append(dict(num=str(num), title=title, blocks=list(blocks)))
P = lambda t: {"p": t}
H = lambda t: {"h3": t}
EQ = lambda t, n: {"eq": t, "n": n}
L = lambda xs, o=False: {"list": xs, "ordered": o}
T = lambda n, cap, head, rows, note: {"table": {"n": n, "caption": cap, "head": head, "rows": rows, "note": note}}
C = lambda t: {"callout": t}
FIG = lambda n, fid, cap, alt, src: {"fig": {"n": n, "id": fid, "caption": cap, "alt": alt, "source": src}}

sec(1, "Introduction",
 P("For most of the period since large language models (LLMs) became commercial products, their cost was discussed in terms of a single number: the price per million tokens of input and output. That number has fallen quickly. The 2025 AI Index reported that the inference cost of reaching GPT-3.5-level performance fell more than 280-fold between November 2022 and October 2024 [@aiindex], and Epoch AI measured declines of up to 40-fold per year in the price of reaching fixed benchmark milestones, at rates that differ widely between tasks [@epoch]. A later analysis using the same kinds of data found that while the price of a given level of performance falls by roughly 5 to 10 times per year, the price of running the newest frontier models has risen [@progress]."),
 P("The reason the two trends diverge is that the amount of work a model does on a task is no longer fixed. Current models from every major developer can reason at length before they answer, and the user can choose how long, through settings named low, medium, high, xhigh or max. Each step up generates more reasoning tokens, which are billed at the output price. The relevant economic quantity for a business is therefore not the price per token but the cost per task, and how that cost trades against the quality of the result. Kapoor et al. argued that agent benchmarks should report cost alongside accuracy for exactly this reason [@matter], and Erol et al. formalized the expected cost of obtaining one correct answer as an evaluation metric [@cop]."),
 P("This paper asks a narrow, practical question: when a firm pays for more reasoning effort, how much better does the model get? In economic terms, it measures the returns to reasoning effort. It does not attempt to rank models overall, to predict future prices, or to evaluate safety or latency. Its readers are assumed to be managers and engineers in small and medium-sized enterprises who must choose a model and a setting for a defined workload."),
 P("The paper is organized as follows. Section 2 explains how cost per task arises and how effort settings differ by vendor. Section 3 describes the data, the cost definition and the treatment of uncertainty. Section 4 presents results from a controlled effort study, a coding benchmark, a reasoning benchmark near its ceiling, and an index that links list prices to task costs. Section 5 discusses where extra effort pays, how vendor charts should be read, and the limitations of the evidence. Section 6 turns the findings into a procedure for firms, and Section 7 concludes."),
)

sec(2, "Background",
 H("2.1 From token prices to cost per task"),
 P("Vendors price input and output tokens separately, usually with a discount for input that is served from a cache. Reasoning is billed as output: Anthropic states that thinking tokens are billed as output tokens [@anthprice], OpenAI bills reasoning tokens as output tokens [@oaiprice], and Google's output price for Gemini models includes thinking tokens [@gprice]. The cost of one task is the sum over token types of the tokens consumed multiplied by their price:"),
 EQ("C<sub>task</sub> = N<sub>in</sub>·p<sub>in</sub> + N<sub>cache</sub>·p<sub>cache</sub> + (N<sub>reason</sub> + N<sub>ans</sub>)·p<sub>out</sub>", 1),
 P("where N are token counts per task and p are prices per token. A higher effort setting mainly raises N<sub>reason</sub>; the prompt and the answer change much less. Because p<sub>out</sub> is typically three to five times p<sub>in</sub> for the models in this study (Section 4.4), reasoning tokens quickly dominate the bill. Figure 1 illustrates the mechanism schematically."),
 P("Two consequences follow from Eq. (1). First, two models with identical list prices can differ several-fold in cost per task, because they spend different numbers of tokens on the same work. Second, tokens are not a common unit: tokenizers differ between vendors, and Anthropic states that its newer models produce approximately 30% more tokens for the same text than earlier ones [@anthprice]. Per-token prices can therefore mislead even within one vendor's product line."),
 H("2.2 Reasoning-effort settings across vendors"),
 P("Every vendor in this study exposes some control over reasoning, but the names and number of levels differ (Table 2). Anthropic and OpenAI offer five levels from low to max; Google offers three for its Gemini 4 models; DeepSeek, Moonshot and Zhipu offer low, high and max; and Meta adds a minimal level. Defaults also differ: a model called through its default setting may already be at medium, high or max. A setting with the same name is not the same amount of work across vendors, so comparisons in this paper are made between steps within one model, not between equally named settings of different models."),
 H("2.3 Prior work on cost-aware evaluation"),
 P("The idea of trading cost against quality is not new. FrugalGPT showed that cascading queries from cheaper to more expensive models could match a strong model's accuracy at much lower cost [@frugal]. Studies of inference scaling found that spending more computation at inference time, by sampling repeatedly or generating longer solutions, can raise accuracy along a predictable curve [@monkeys, @inflaws]. The Holistic Agent Leaderboard standardized agent evaluation across models and scaffolds so that cost and accuracy could be compared on equal terms [@hal]."),
 P("Other work points to limits. Reasoning models can spend many tokens on trivial problems with little benefit [@overthink], shorter reasoning chains can be more accurate than longer ones for the same question [@hassid], disabling explicit thinking can remain competitive at matched token budgets [@nothink], and on some tasks longer reasoning lowers accuracy [@inverse]. Accuracy and token use also change in different ways as problems become harder [@illusion]. A counterpoint is that small gains in per-step accuracy compound over long, multi-step tasks, so a gain that looks negligible on a single-answer benchmark may matter for long-running agents [@longhorizon]. This paper adds current, cross-vendor measurements to that discussion."),
)

TABLE2 = T(2, "Reasoning-effort settings offered by selected models, as listed by each vendor on November 11, 2026.",
 ["Developer", "Model", "Settings offered", "Default"],
 [["Anthropic", "Claude Fable 5.2", "Low, Medium, High, Xhigh, Max", "High"],
  ["Anthropic", "Claude Opus 5.5", "Low, Medium, High, Xhigh, Max", "Medium"],
  ["OpenAI", "GPT-6 Astra", "Low, Medium, High, Xhigh, Max", "Not stated"],
  ["OpenAI", "GPT-6.1 Terra", "None, Low, Medium, High, Xhigh, Max", "Medium"],
  ["Google", "Gemini 4 Carbon", "Low, Medium, High", "Medium"],
  ["xAI", "Grok 4.7", "Low, Medium, High, Xhigh", "High"],
  ["Meta", "Muse Spark 1.3", "Minimal, Low, Medium, High, Xhigh, Max", "High"],
  ["DeepSeek", "DeepSeek V4 Pro", "None, Low, High, Max", "High"],
  ["Moonshot", "Kimi K3.1 Pro", "Low, High, Max", "Max"],
  ["Zhipu", "GLM-5.3", "Low, High, Max", "Max"]],
 "Source: vendor documentation and price pages [@anthprice, @oaiprice, @gprice]; other vendors' pages are listed in the accompanying dataset. Equally named settings are not equivalent across vendors.")
S[1]["blocks"].insert(10, TABLE2)
S[1]["blocks"][9]["p"] += " Table 2 summarizes the settings as published."

TABLE1 = T(1, "Data sources used in this paper.",
 ["Source", "Operator", "What is measured", "Cost measure", "Operator sells models?"],
 [["Vals AI reasoning-effort study", "Vals AI", "Seven models on the same Vals Index tasks at three effort settings", "Cost per test at list prices", "No"],
  ["FrontierCode 2.0", "Cognition", "Coding tasks scored by rubric; 132 tasks, up to five attempts each", "Mean cost per attempt at list prices, including public discounts", "Yes; its own models appear on the board"],
  ["ARC-AGI-2 (semi-private)", "ARC Prize Foundation", "Abstract reasoning puzzles; 120 tasks", "Cost per task at retail prices", "No"],
  ["Intelligence Index v5.0.1", "Artificial Analysis", "Composite index of four categories", "Weighted cost per index task", "No"],
  ["List prices", "Each developer", "Price per million tokens by type", "Not a task cost", "Yes"],
  ["Arena", "LMArena", "Pairwise human preference ratings", "None published", "No"]],
 "Sources: [@valsblog, @valsidx, @cognition, @arclb, @arc2, @arcpolicy, @aa, @aaidx, @arena]. All values were retrieved on November 11, 2026.")

sec(3, "Data and Method",
 H("3.1 Sources"),
 P("The analysis uses only sources that publish both a quality measure and a measured cost for each model and effort setting, and that make the underlying values available (Table 1). The primary source for the effort question is a study by Vals AI, which ran seven models on the same tasks from its Vals Index at three effort settings and published accuracy, standard errors and cost per test [@valsblog, @valsidx]. Vals AI does not sell models, and because the tasks are identical across settings, differences between settings are not confounded by task selection. The study used about half of the tasks in each Vals Index benchmark, so its scores differ slightly from the main leaderboard."),
 P("For comparison across models, the paper uses FrontierCode 2.0, a coding benchmark run by Cognition, which publishes a data file with scores and cost per attempt for 29 models at their available settings [@cognition]. ARC-AGI-2, run by the non-profit ARC Prize Foundation on a 120-task semi-private set, provides a reasoning benchmark at retail prices [@arclb, @arc2, @arcpolicy]. The Artificial Analysis Intelligence Index supplies cost per index task and blended list prices for 27 models [@aa, @aaidx]. Official price pages supply list prices [@anthprice, @oaiprice, @gprice], and Arena supplies human-preference ratings, which measure preference rather than correctness and carry no cost data [@arena]."),
 TABLE1,
 H("3.2 Defining cost per task"),
 P("The cost per task in this paper is the operator's own figure, computed in each case from tokens consumed and list prices as in Eq. (1). The operators differ in detail: Cognition reports mean spend per attempt including public discounts [@cognition], ARC Prize uses retail pricing [@arcpolicy], and Artificial Analysis weights task costs by the same weights as its index [@aa]. Because these definitions are not identical, costs from different sources are never placed on the same axis; each figure and table uses one source. Where an accuracy rate is available, the paper also reports cost per correct answer, following Erol et al. [@cop]:"),
 EQ("C<sub>correct</sub> = C<sub>task</sub> / a", 2),
 P("where a is the fraction of tasks answered correctly. Eq. (2) is applied only to the Vals data, whose score is an accuracy. FrontierCode scores are rubric averages, and dividing cost by them would not give a cost per success."),
 H("3.3 Uncertainty"),
 P("None of the operators except Vals AI publishes an uncertainty interval, and none publishes task-level results. The paper therefore approximates the standard error of a score s (in percent) on n independent tasks by the binomial formula:"),
 EQ("SE(s) = 100 · √( (s/100)·(1 − s/100) / n )", 3),
 P("with a 95% interval of ±1.96 SE. For ARC-AGI-2, n = 120. FrontierCode runs each of its 132 tasks up to five times; the paper reports two bounds, a conservative one with n = 132 tasks and an optimistic one with n = 660 attempts, since attempts on the same task are not independent. For Vals AI, the published standard errors are used directly. Figure 6 shows how the interval narrows with the number of tasks: near a score of 50% on 132 tasks, the 95% interval is about ±8.5 points, so only large differences can be detected. A change between two effort settings is treated as distinguishable when"),
 EQ("|z| = |s<sub>2</sub> − s<sub>1</sub>| / √( SE<sub>1</sub><sup>2</sup> + SE<sub>2</sub><sup>2</sup> ) ≥ 1.96", 4),
 P("Eq. (4) treats the two settings as independent samples, which is conservative because the same tasks are used at each setting; a paired test on task-level data would detect smaller differences. Vals AI reports such paired tests in its own analysis [@valsblog]. The cost multiple of a step is the ratio of the costs per task at the two settings, r = C<sub>2</sub> / C<sub>1</sub>."),
 H("3.4 Collection and verification"),
 P("Data were collected on November 11, 2026, in four independent streams: Arena ratings, benchmarks that publish cost per task, official vendor prices, and independent indexes. Each recorded value carries the address of the page or data file it was read from. Values were taken from operators' data files by script wherever these existed, and no value was read off a chart image. A separate verifier, who had not seen the collectors' notes, then re-fetched the primary sources and compared 3,573 fields one by one. It found four errors, all in price metadata and one reference title, which were corrected; all benchmark and rating values matched their sources. A second reviewer examined the method, and its findings shaped the choice of anchor benchmarks and the treatment of uncertainty described above. The full dataset, with sources, corrections and both reviews, accompanies this paper."),
)

sec(4, "Results",
 H("4.1 The same tasks at three effort settings"),
 P("Figure 2 and Table 3 show the Vals AI study. For every model, accuracy rises from the lowest setting tested to the next, and cost rises with it. The size of the gain differs greatly. Opus 5.5 rose 12.2 points from low to high, Muse Spark 1.3 rose 13.1 points from minimal to high, and GLM-5.3 rose 10.7 points from low to high; each of these gains is distinguishable at 95%. The next step bought much less: Opus 5.5 gained 1.5 points from high to max while its cost per test rose 2.46 times, from $10.76 to $26.49, and GLM-5.3 gained 1.1 points for 1.31 times the cost."),
 P("Table 4 lists all fourteen steps. Five are distinguishable at 95%. The final step, from the second-highest to the highest setting tested, was within noise for six of the seven models; the exception was Grok 4.7, which gained 5.8 points from high to xhigh. Two final steps lowered the score slightly (Muse Spark 1.3 and Gemini 4 Argon), and in both cases the change is well within noise. Vals AI's own paired analysis reaches a consistent conclusion: in 22 of 56 combinations of model and benchmark, a lower setting scored as high as the leaderboard setting at lower cost [@valsblog]."),
 P("Cost per correct answer, Eq. (2), makes the trade-off concrete. For Opus 5.5 it rises from $7.62 at low to $15.81 at high and $38.06 at max. At its lowest setting Opus 5.5 retained 80% of its maximum-setting accuracy at 16% of the cost. DeepSeek V4.1 Flash, the cheapest model in the study, reached 61.3% at max for $0.59 per test, about one forty-fifth of the cost of Opus 5.5 at max for an accuracy 8.3 points lower."),
 P("Figure 3 plots every step in the two controlled data sets by its cost multiple and score change. In both, most steps cost 1.2 to 2.7 times the previous setting, and the distinguishable gains are concentrated in the lower steps of each model."),
 H("4.2 Comparison across models on FrontierCode 2.0"),
 P("Figure 4 shows FrontierCode 2.0 for five models. Claude Fable 5.2 reached the highest score of any configuration, 49.1% at xhigh, at a cost of $14.19 per task. Its max setting scored 45.7% at $44.70, 3.15 times the cost of xhigh. The fall of 3.5 points is not distinguishable: z is −0.56 on the task bound and −1.26 on the attempt bound. Anthropic's system card also notes that 22 of the 660 attempts at max timed out and that the score would be 44.4% if those attempts were counted as zero [@card]. The supportable conclusion is that max bought no measurable gain over xhigh at three times the cost, not that it performed worse."),
 P("Table 6 tests the eighteen steps of the five models. Only one is distinguishable on the conservative bound, Opus 5.5 from low to medium (+15.4 points for 2.28 times the cost). Five more are distinguishable only on the optimistic attempt bound. Across all 29 models in the data file, 5 of 89 adjacent steps are distinguishable on the task bound and 32 on the attempt bound, and 12 steps lowered the score, none of them distinguishably on the task bound. Between generations, the difference is large: Fable 5.2 at xhigh scored 16.7 points above Fable 5.1 at xhigh (z = 2.8), at 1.63 times the cost per task."),
 P("Gemini 4 Carbon shows how a price change moves a model's position. Its price of $2 / $10 per million tokens is introductory and rises to $4 / $20 on December 1, 2026 [@gprice]. Because every token price doubles, its cost per task on the same workload doubles too, which moves its best configuration from $4.04 to about $8.09 per task (hollow markers in Figure 4)."),
 H("4.3 A benchmark near its ceiling: ARC-AGI-2"),
 P("ARC-AGI-2 was designed to be hard for AI systems [@arc2024], but current frontier models now score above 90% on its semi-private set: 18 of the 86 configurations in the data do so. At those scores the 95% interval on 120 tasks is about ±3.9 to ±5.4 points, so the remaining differences cannot be resolved. Figure 5 plots error rate rather than score, on a logarithmic axis, to make the last few points visible. GPT-6 Astra at max scored 95.0% at $1.12 per task, while GPT-6.1 Sol at high scored 91.7% at $0.13; the difference of 3.3 points (z ≈ 1.0) cost 8.3 times as much. In addition, 27 of the 86 costs are lower bounds, because ARC Prize notes that they include recorded usage only [@arclb]. ARC-AGI-2 remains informative for smaller models, whose steps are large, but it cannot locate a point of diminishing returns for frontier models."),
 H("4.4 What list prices hide"),
 P("Figure 7 places each model's blended list price, as computed by Artificial Analysis from a 7:2:1 mix of cached, input and output tokens [@aa], against its cost per index task at each effort setting. Price and cost are correlated, but within a single model the cost per task varies widely with effort: across the 17 models with two or more settings, the highest setting cost a median of 3.2 times the lowest, and up to 29.8 times. Claude Fable 5.2 cost $3.10 per task at low and $26.54 at max on this index, for scores of 53.9 and 64.6. Gemini 4 Carbon cost more at low ($7.19) than at medium ($6.59) while scoring lower, so cost is not always monotonic in effort."),
 P("List prices also carry conditions that a comparison must record (Table 7). Several are temporary: Gemini 4 Carbon and Gemini 3.8 Flash are at introductory prices, and GPT-5.6 Sol at a promotional price until November 30, 2026 [@gprice, @oaiprice]. Some double above a prompt-length threshold, and DeepSeek charges half its peak rate off-peak. A cost comparison is therefore valid only at a stated price date."),
)

FIGS = {
 "2.1": FIG(1, "fig1-cost-anatomy", "How the effort setting changes cost per task, Eq. (1). Input and cached-input costs are largely fixed by the prompt; reasoning tokens, billed at the output price, grow with effort. Proportions are illustrative.",
            "Schematic stacked bar chart of cost per task at low, medium, high and max effort. Each bar has the same input and cached-input segments at the bottom, a reasoning segment that grows from small at low effort to dominant at max, and a thin answer segment on top. Labels above the bars read 1.0, 1.3, 1.8 and 3.1 times.", "Schematic drawn by the author from Eq. (1)."),
 "4.1a": FIG(2, "fig2-vals-effort", "Accuracy against cost per test for seven models at three effort settings on the same Vals Index tasks. Bars are 95% intervals from Vals AI's standard errors; the cost axis is logarithmic.",
             "Line chart of Vals Index accuracy from about 43 to 70 percent against cost per test from about 30 cents to 26 dollars on a logarithmic axis. Each of seven models has three connected points. DeepSeek V4.1 Flash rises from 54.6 to 61.3 percent below 60 cents. Opus 5.5 rises from 55.9 percent at 4.26 dollars to 68.1 at 10.76 and 69.6 at 26.49. Gemini 4 Argon's three points cluster near 68 percent and 9 to 11 dollars.", "Data from Vals AI [@valsblog, @valsidx]."),
 "4.1b": FIG(3, "fig3-step-returns", "Score change against cost multiple for each step between adjacent effort settings. (a) Vals AI effort study, seven models. (b) FrontierCode 2.0, five models, conservative task-level bound. Filled markers are distinguishable at 95% by Eq. (4).",
             "Two scatter panels with cost multiple from 0.8 to 5 times on a logarithmic horizontal axis and score change in points on the vertical axis. In panel a, five of fourteen points are filled, with gains of 4.7 to 13.1 points; the open points lie between minus 1 and plus 4 points. In panel b, one of eighteen points is filled, at plus 15.4 points and 2.3 times; the others lie between minus 3.5 and plus 8.9 points.", "Author's calculation from Tables 4 and 6."),
 "4.2": FIG(4, "fig4-frontiercode", "FrontierCode 2.0 score against cost per task for five models at each effort setting. Bars are conservative 95% intervals (n = 132). Hollow markers show Claude Fable 5.2 as costed in Cognition's data file and Gemini 4 Carbon at its price from December 1, 2026.",
            "Line chart of score from about 15 to 49 percent against cost per task from about 75 cents to 56 dollars on a logarithmic axis. Claude Fable 5.2 rises from 34.2 percent at 2.10 dollars to 49.1 percent at 14.19, then falls to 45.7 percent at 44.70. Opus 5.5 rises from 14.7 percent at 75 cents to 45.5 percent at 12.82. GPT-6 Astra rises from 31.1 to 42.8 percent between 2.44 and 6.68 dollars. Gemini 4 Carbon's three points lie between 31.9 and 40.0 percent near 4 to 4.5 dollars. Claude Fable 5.1 rises from 20.6 to 32.4 percent. Most error bars overlap.", "Data from Cognition [@cognition]; Fable 5.2 costs per [@card]."),
 "4.3": FIG(5, "fig5-arc-ceiling", "ARC-AGI-2 error rate (100 minus score) against cost per task, both on logarithmic axes, with better scores higher. The shaded band marks scores of 90% and above. Hollow markers indicate costs that ARC Prize reports as lower bounds.",
            "Chart with cost per task from 10 cents to 5 dollars and error rate from 50 percent at the bottom to about 2 percent at the top. Gemini 4 Carbon falls from 50 percent error at 10 cents to 5.8 percent at 38 cents. Opus 5.5, GPT-6 Astra, Fable 5.2 and Gemini 4 Carbon all reach the shaded band between 5 and 10 percent error, with overlapping intervals. Fable 5.1 approaches 10 percent error at 3 to 4.50 dollars.", "Data from ARC Prize [@arclb]."),
 "3.3": FIG(6, "fig6-interval-width", "Half-width of the 95% interval for a benchmark score against the number of independent tasks, from Eq. (3), for true scores of 50% and 90%. Dashed lines mark the task counts of ARC-AGI-2, FrontierCode 2.0 and 500 tasks.",
            "Line chart on a logarithmic horizontal axis of number of tasks from 20 to 2000, with interval half-width in points on the vertical axis. The 50 percent curve falls from about 22 points at 20 tasks to 2.2 at 2000; the 90 percent curve from 13 to 1.3. Marked points show plus or minus 8.5 points at 132 tasks for a 50 percent score and 5.4 points at 120 tasks for a 90 percent score.", "Author's calculation from Eq. (3)."),
 "4.4": FIG(7, "fig7-price-vs-task-cost", "Blended list price against cost per Intelligence Index task for 27 models; each vertical column is one model and its dots are its effort settings. Both axes are logarithmic.",
            "Log-log scatter of blended list price from about 7 cents to 7 dollars per million tokens against cost per index task from half a cent to about 27 dollars. Prices and costs rise together, but most models form vertical columns spanning a factor of 3 to 30 in cost. Claude Fable 5.2 spans about 3 to 27 dollars, Claude Haiku 5.5 about 4 cents to 41 cents, and Gemini 4 Argon and Carbon share one price.", "Data from Artificial Analysis [@aa]."),
}

TABLE3 = T(3, "Vals AI effort study: accuracy, cost per test and cost per correct answer by model and setting.",
 ["Model", "Setting", "Accuracy (%) ± 95% CI", "Cost per test", "Cost per correct answer"], t3,
 "Source: [@valsblog, @valsidx]; cost per correct answer from Eq. (2). Costs at list prices on November 11, 2026.")
TABLE4 = T(4, "Each step between adjacent settings in the Vals AI study.",
 ["Model", "Step", "Score change (points)", "Cost multiple", "z, Eq. (4)", "Distinguishable at 95%"], t4,
 "Author's calculation from Table 3. z uses independent standard errors and is conservative.")
TABLE6 = T(6, "Steps between adjacent settings on FrontierCode 2.0 for five models.",
 ["Model", "Step", "Score change (points)", "Cost multiple", "z (task / attempt bound)", "Verdict"], t6,
 "Author's calculation from Cognition's data file [@cognition]; Fable 5.2 costs per [@card]. Task bound n = 132; attempt bound n = 660.")
TABLE7 = T(7, "List prices of selected models (USD per million input / output tokens) on November 11, 2026, with conditions that affect comparisons.",
 ["Model", "Developer", "Input / output", "Condition"], t7,
 "Sources: vendor price pages [@anthprice, @oaiprice, @gprice] and the accompanying dataset. Tokenizers differ between vendors, so per-token prices are not directly comparable.")
# insert figures and tables into section 4 blocks and 2/3
S4 = S[3]["blocks"]
def after(blocks, startswith, item):
    i = next(k for k, b in enumerate(blocks) if "p" in b and b["p"].startswith(startswith)); blocks.insert(i + 1, item)
after(S4, "Figure 2 and Table 3", FIGS["4.1a"]); after(S4, "Figure 2 and Table 3", TABLE3)
after(S4, "Table 4 lists all", TABLE4)
after(S4, "Figure 3 plots", FIGS["4.1b"])
after(S4, "Figure 4 shows", FIGS["4.2"])
after(S4, "Table 6 tests", TABLE6)
after(S4, "ARC-AGI-2 was designed", FIGS["4.3"])
after(S4, "Figure 7 places", FIGS["4.4"])
after(S4, "List prices also carry", TABLE7)
after(S[1]["blocks"], "where N are token counts", FIGS["2.1"])
after(S[2]["blocks"], "with a 95% interval", FIGS["3.3"])
S4.insert(next(k for k, b in enumerate(S4) if "fig" in b and b["fig"]["n"] == 3) + 1,
          C("Across both controlled data sets, the lower effort steps produced most of the distinguishable gains. The final step usually cost 1.1 to 3.2 times more and bought a change in score that could not be told apart from chance."))

TABLE5 = T(5, "Claude Fable 5.2 on FrontierCode 2.0: the two published cost series.",
 ["Setting", "Score (%), system card", "Score (%), data file", "Cost per task, system card", "Cost per task, data file", "Ratio"], t5,
 "Sources: [@card, @cognition]. The ratio is 1.25 at every setting, equal to the ratio of the Fable 5.1 and Fable 5.2 list prices ($10 / $50 and $8 / $40) [@anthprice].")
TABLE8 = T(8, "Claims in the Claude Fable 5.2 announcement compared with the published data.",
 ["Claim", "System card costs", "Cognition data file", "Assessment"],
 [["Fable 5.2 high matches Opus 5.5's best score (45.3% vs 45.5%) at roughly half the cost", "$6.72 vs $12.82 (0.52×)", "$8.40 vs $12.82 (0.66×)", "Equal score at lower cost is supported; the size of the saving depends on the cost series"],
  ["Ahead of GPT-6 Astra (42.8%) at about the same cost", "$6.72 vs $6.68 (1.01×)", "$8.40 vs $6.68 (1.26×)", "Score lead of 2.5 points is within noise (z ≈ 0.4)"],
  ["Gemini 4 Carbon (medium) scores 41.1%", "—", "40.0% (different harness)", "Two runs with different harnesses; not directly comparable"]],
 "Claims from [@launch]; data from [@card, @cognition]. z from Eq. (4) with the task bound.")

sec(5, "Discussion",
 H("5.1 Where extra effort pays and where it does not"),
 P("The evidence supports a consistent pattern. Moving up from the lowest setting often produces a large and distinguishable gain, especially for models whose lowest setting reasons very little; the gains of 10 to 15 points for Opus 5.5, Muse Spark 1.3 and GLM-5.3 in the Vals study, and of 15.4 points for Opus 5.5 on FrontierCode, are of this kind. The highest settings rarely produce a gain that can be measured on benchmarks of this size, yet they multiply cost. Across sources, the highest setting cost a median of 2.9 to 4.6 times the lowest (2.9 on FrontierCode, 3.2 on the Artificial Analysis index, 3.4 in the Vals study and 4.6 on ARC-AGI-2)."),
 P("This pattern is consistent with the literature on overthinking and on tasks where longer reasoning does not help [@overthink, @hassid, @inverse], but it should not be read as a general law. The size of the benchmarks limits what can be detected: a real gain of two or three points is invisible at n = 132. Grok 4.7's distinguishable gain at its highest setting shows that the last step can pay for some models. Gains that are small on single-answer benchmarks may also compound over long agentic tasks [@longhorizon]. The safe conclusion is that the return to the highest setting is uncertain and must be measured, not assumed."),
 H("5.2 Reading vendor charts: the Fable 5.2 case"),
 P("The chart that prompted this study, a score-against-cost plot for FrontierCode 2.0, circulated on social media without attribution. It was traced to Figure 8.4.A of Anthropic's system card for Claude Fable 5.2, which states that Cognition ran the evaluation for every model and that each score is a single result without an uncertainty interval [@card]. Two features of the published data deserve attention."),
 P("First, there are two cost series for Fable 5.2 (Table 5). Cognition's data file lists costs exactly 1.25 times those in the system card at every setting, while the costs of other models agree between the two sources. The ratio equals the ratio of the list prices of Fable 5.1 and Fable 5.2 [@anthprice], which suggests, but does not establish, that the data file was priced at the older rate. This paper uses the system-card costs, which match the current price, and shows the alternative in Figure 4."),
 TABLE5,
 P("Second, launch claims depend on which series is used (Table 8). The claim that Fable 5.2 at high matches the best score of Opus 5.5 at roughly half the cost holds on the system-card costs (0.52 times) but becomes about two-thirds on the data file (0.66 times) [@launch]. The claimed lead over GPT-6 Astra at similar cost is 2.5 points, well within the interval. Neither claim is wrong on its own terms, but both are more precise than the data allow. Readers should treat single-run benchmark charts from any vendor as indicative and look for the operator's own data."),
 TABLE8,
 H("5.3 Limitations"),
 L(["<strong>Comparability.</strong> Each operator defines cost per task differently, applies prices at different dates, and runs each vendor's models in a different harness. FrontierCode runs Anthropic, OpenAI and Google models in different tools, so cross-model differences mix model and harness effects.",
    "<strong>Independence.</strong> Cognition, which runs FrontierCode, lists its own models on the same benchmark. Artificial Analysis includes a FrontierCode-derived component in its index [@aaidx], so the two are not independent confirmations.",
    "<strong>Noise.</strong> Without task-level data, the intervals here are approximations, and paired tests could detect smaller differences than Eq. (4).",
    "<strong>Coverage.</strong> Low-cost and open-weight models are thinly represented on the cost-reporting benchmarks, and models are tested at different settings in different sources.",
    "<strong>Transfer.</strong> Benchmark cost per task is a lower bound for a business deployment, which adds retries, longer contexts, tool calls and human review. Caching also differs: in Artificial Analysis's run for Fable 5.2 at max, cache reads and writes accounted for about half of the total cost."]),
)

sec(6, "Practical Guidance for Small and Medium-Sized Enterprises",
 P("The results suggest that the effort setting should be managed as a cost parameter, chosen by measurement on the firm's own work. Figure 8 sets out a procedure that a small team can run in a few days."),
 FIG(8, "fig8-procedure", "A procedure for choosing a model and effort setting. Each step up is kept only if the gain exceeds the 95% interval and is worth its cost.",
     "Flow diagram with four boxes in a row: build a test set of 100 to 300 of your own tasks; run two or three candidate models at a low effort setting; step one setting up and re-run the same tasks; and a decision box asking whether the gain is larger than the 95 percent interval and worth the cost. A yes arrow loops back to step three. A no arrow leads down to a box reading stop, use the previous setting and budget from measured tokens, which leads to a box reading record cost per task and cost per correct answer at a dated price sheet.", "Drawn by the author from Sections 3 and 4."),
 L(["<strong>Build a test set from real work.</strong> Public benchmarks indicate direction, not the size of a gain on a particular workload. A set of 100 to 300 representative tasks with known answers gives an interval of roughly ±5 to ±10 points (Figure 6), enough to detect large effects.",
    "<strong>Start low and step up.</strong> Run two or three candidate models, including at least one low-cost model, at a low setting, then raise the setting one step at a time on the same tasks.",
    "<strong>Keep a step only if it pays.</strong> Accept a step when the gain exceeds the interval and its value exceeds the extra cost per task. Compare cost per correct answer, Eq. (2), not price per token.",
    "<strong>Budget from measured tokens.</strong> Record tokens by type for each task and multiply by a dated price sheet, Eq. (1). A price change then becomes a recalculation rather than a new test.",
    "<strong>Watch price dates.</strong> Note introductory and promotional prices and their end dates, and repeat the comparison when they expire or a new model is released."], True),
 C("For most business tasks, the default or a middle setting is a better starting point than the maximum. Raise it only where your own tests show a gain that is larger than the noise and worth the extra cost."),
 P("Firms that use the AI Models page on this site to shortlist candidates should note that it is a separate, dated snapshot built from overlapping but not identical sources; the procedure above applies whichever shortlist is used."),
)

sec(7, "Conclusion",
 P("Reasoning effort has made the cost of using a language model a variable that the user controls. On current evidence, moving from the lowest to the highest setting multiplies cost per task by about three to five, and much more for some models. The lower steps often buy large, measurable improvements; the highest steps usually buy improvements too small to detect on public benchmarks, at 1.1 to 3.2 times the cost of the step below. Frontier models now cluster so closely on some benchmarks that they cannot be ranked, and list prices, which are often temporary and differ in tokenization, are a weak guide to task cost."),
 P("These conclusions are bounded by the data: benchmarks of 120 to 132 tasks cannot detect small gains, operators define cost differently, and vendor charts rest on single runs. For a firm, the practical implication is straightforward. The effort setting should be chosen by testing on representative tasks, kept at the lowest level whose results are good enough, and revisited when prices or models change. Future work should use task-level data with paired tests and a single dated price sheet, and should extend the comparison to the low-cost and open-weight models that matter most to smaller firms."),
)

# ---------------- citations: number in order of first use ----------------
order = []
def collect(t):
    for grp in re.findall(r"\[(@[^\]]+)\]", t):
        for k in re.findall(r"@(\w+)", grp):
            if k not in order: order.append(k)
def walk(f):
    for s in S:
        for b in s["blocks"]:
            for k in ("p", "callout"):
                if k in b: b[k] = f(b[k])
            if "list" in b: b["list"] = [f(x) for x in b["list"]]
            if "table" in b:
                t = b["table"]; t["note"] = f(t["note"]); t["caption"] = f(t["caption"]); t["rows"] = [[f(c) for c in r] for r in t["rows"]]
            if "fig" in b:
                b["fig"]["source"] = f(b["fig"]["source"]); b["fig"]["caption"] = f(b["fig"]["caption"])
walk(lambda t: (collect(t), t)[1])
missing = [k for k in REF if k not in order]
assert not missing, ("uncited references", missing)
def fmt(m):
    nums = sorted(order.index(k) + 1 for k in re.findall(r"@(\w+)", m.group(1)))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        out.append(f"{nums[i]}–{nums[j]}" if j - i >= 2 else ", ".join(str(x) for x in nums[i:j + 1])); i = j + 1
    return "[" + ", ".join(out) + "]"
walk(lambda t: re.sub(r"\[(@[^\]]+)\]", fmt, t))

doc = dict(slug=SLUG, volume=104, issue=7, published="2026-11-12", revised="2026-11-12",
           title="Score Versus Cost Per Task: Measuring the Returns to Reasoning Effort in Frontier Language Models",
           short_title="Score Versus Cost Per Task in Frontier LLMs",
           meta="How much better do language models get when you pay for more reasoning? Score against measured cost per task for current models, as of November 2026.",
           author={"name": "Quak Foo Lee", "role": "Chief Technology Officer", "org": "Chmltech Ltd.", "division": "Division of Artificial Intelligence and Machine Learning", "location": "Vancouver, BC, Canada"},
           abstract=ABSTRACT,
           keywords=["large language models", "reasoning effort", "cost per task", "test-time compute", "benchmark evaluation", "LLM pricing", "cost-performance trade-off"],
           corrections=[], sections=S, references=[REF[k] for k in order])
# renumber tables and figures in order of appearance (written with working numbers above)
TMAP = {2: 1, 1: 2, 3: 3, 4: 4, 6: 5, 7: 6, 5: 7, 8: 8}
FMAP = {1: 1, 6: 2, 2: 3, 3: 4, 4: 5, 5: 6, 7: 7, 8: 8}
def remap(t):
    t = re.sub(r"\bTables (\d+) and (\d+)", lambda m: f"Tables @T{m.group(1)}@ and @T{m.group(2)}@", t)
    t = re.sub(r"\bTable (\d+)", lambda m: f"Table @T{m.group(1)}@", t)
    t = re.sub(r"\bFigures? (\d+)", lambda m: m.group(0).split()[0] + f" @F{m.group(1)}@", t)
    t = re.sub(r"@T(\d+)@", lambda m: str(TMAP[int(m.group(1))]), t)
    return re.sub(r"@F(\d+)@", lambda m: str(FMAP[int(m.group(1))]), t)
walk(remap)
for s_ in S:
    for b in s_["blocks"]:
        if "table" in b: b["table"]["n"] = TMAP[b["table"]["n"]]
        if "fig" in b: b["fig"]["n"] = FMAP[b["fig"]["n"]]
seq_t = [b["table"]["n"] for s_ in S for b in s_["blocks"] if "table" in b]; seq_f = [b["fig"]["n"] for s_ in S for b in s_["blocks"] if "fig" in b]
assert seq_t == sorted(seq_t) == list(range(1, 9)), seq_t
assert seq_f == sorted(seq_f) == list(range(1, 9)), seq_f
json.dump(doc, open(OUT, "w"), indent=1, ensure_ascii=False)
# report
import sys; sys.path.insert(0, os.path.join(HERE, "..", "..", "gen"))
words = sum(len(re.sub("<[^>]+>", "", b.get("p", "") + " " + b.get("callout", "")).split()) + sum(len(x.split()) for x in b.get("list", [])) for s in S for b in s["blocks"]) + len(ABSTRACT.split())
print("wrote", OUT, "| refs", len(order), "| words", words, "| abstract words", len(ABSTRACT.split()), "| meta chars", len(doc["meta"]))
print("vals distinguishable steps", vsig, "of", len(t4), "| final-step noise", vlast_noise, "| FC lead task-sig", fsig_t, "attempt-sig", fsig_a)
