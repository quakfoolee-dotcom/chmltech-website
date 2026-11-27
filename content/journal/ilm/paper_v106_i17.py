"""Chmltech Online Journal, Vol. 106, Issue 17: The LLM Should Not Do the Arithmetic (draft V1, Nov 27 2026).

Model: content/journal/ilm/models/oee/ (oee_reference.py builds the dataset, reference results, error study and the
24-question test set; grade.py scores a model's answers; oee_appendix.py is the compact calculator).
"""

SLUG = "the-llm-should-not-do-the-arithmetic-a-tool-grounded-architecture-for-oee-and-kpi-analysis"
META = dict(
    volume=106, issue=17,
    title='The LLM Should Not Do the Arithmetic: A Tool-Grounded Architecture for OEE and KPI Analysis',
    short_title='LLMs and OEE: A Tool-Grounded KPI Architecture',
    meta='Eight plausible OEE calculation errors tested on four weeks of plant data, and an architecture in which the language model asks and explains but code computes.',
    keywords=['overall equipment effectiveness', 'large language models', 'tool use', 'ISO 22400', 'KPI definitions',
              'semantic layer', 'smart manufacturing', 'evaluation'],
)
ABSTRACT = "Plant managers increasingly ask chat assistants for OEE and expect a reliable number. Overall equipment effectiveness looks like simple arithmetic, but a correct answer depends on definitions that the data rarely states: which downtime is planned, which ideal rate applies to each product, whether reworked units count as good, how overlapping stop records are merged and how shifts are aggregated. This paper builds a four-week extract from a composite three-line bottling plant (104 shift records, 772 stop records) and computes OEE the reference way, following the element definitions of ISO 22400-2, and with eight plausible errors. Aggregation errors such as averaging shift OEE values moved plant OEE by at most 0.4 points here, though by 1.9 points in one narrow slice. Definition errors were much larger: one ideal rate for all products cut plant OEE from 77.6% to 59.4% and made the best line look the worst, another choice of rate gave 142.5%, and counting planned downtime as a loss cost 6.0 points. Summing overlapping stop records left OEE unchanged but moved one line's largest loss from speed to downtime, which would send an improvement team to the wrong problem. Because each error is a silent choice or an algorithmic step, the paper proposes an architecture in which the language model chooses filters and explains results while versioned KPI definitions and tested tools compute every number, and it releases the dataset and a 24-question test set so a plant can check any assistant before trusting it."

REFS = {
    'nakajima': ('Nakajima, S. (1988). <em>Introduction to TPM: Total productive maintenance</em>. Productivity Press.',
        'https://search.worldcat.org/search?q=Nakajima+Introduction+to+TPM+1988'),
    'iso': ('International Organization for Standardization. (2014). <em>ISO 22400-2:2014 Automation systems and integration — Key performance indicators (KPIs) for manufacturing operations management — Part 2: Definitions and descriptions</em>. ISO.',
        'https://www.iso.org/standard/54497.html'),
    'muchiri': ('Muchiri, P., &amp; Pintelon, L. (2008). Performance measurement using overall equipment effectiveness (OEE): Literature review and practical application discussion. <em>International Journal of Production Research</em>, 46(13), 3517–3535.',
        'https://doi.org/10.1080/00207540601142645'),
    'oee1': ('Lee, Q. F. (2026). What OEE really measures: Where your production hours go (OEE series, Part 1). <em>Chmltech Insights</em>.',
        'https://www.chmltech.com/post/what-oee-really-measures.html'),
    'oee2': ('Lee, Q. F. (2026). What OEE losses cost: Putting dollars on downtime, speed and scrap (OEE series, Part 2). <em>Chmltech Insights</em>.',
        'https://www.chmltech.com/post/what-oee-losses-cost.html'),
    'sadeqi': ('Sadeqi Bajestani, M., Mun, D., &amp; Kim, D. B. (2026). Human-in-the-loop and large language models in smart manufacturing: Current applications, challenges, and perspectives. <em>Journal of Manufacturing Systems</em>, 86, 913–941.',
        'https://doi.org/10.1016/j.jmsy.2026.04.027'),
    'dziri': ('Dziri, N., Lu, X., Sclar, M., Li, X. L., Jiang, L., Lin, B. Y., Welleck, S., West, P., Bhagavatula, C., Le Bras, R., Hwang, J. D., Sanyal, S., Ren, X., Ettinger, A., Harchaoui, Z., &amp; Choi, Y. (2023). Faith and fate: Limits of transformers on compositionality. <em>Advances in Neural Information Processing Systems</em>, 36.',
        'https://arxiv.org/abs/2305.18654'),
    'gsm': ('Mirzadeh, I., Alizadeh, K., Shahrokhi, H., Tuzel, O., Bengio, S., &amp; Farajtabar, M. (2025). GSM-Symbolic: Understanding the limitations of mathematical reasoning in large language models. <em>International Conference on Learning Representations</em>.',
        'https://arxiv.org/abs/2410.05229'),
    'lostmid': ('Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., &amp; Liang, P. (2024). Lost in the middle: How language models use long contexts. <em>Transactions of the Association for Computational Linguistics</em>, 12, 157–173.',
        'https://doi.org/10.1162/tacl_a_00638'),
    'ji': ('Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y. J., Madotto, A., &amp; Fung, P. (2023). Survey of hallucination in natural language generation. <em>ACM Computing Surveys</em>, 55(12), 1–38.',
        'https://doi.org/10.1145/3571730'),
    'toolformer': ('Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Hambro, E., Zettlemoyer, L., Cancedda, N., &amp; Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. <em>Advances in Neural Information Processing Systems</em>, 36.',
        'https://arxiv.org/abs/2302.04761'),
    'pal': ('Gao, L., Madaan, A., Zhou, S., Alon, U., Liu, P., Yang, Y., Callan, J., &amp; Neubig, G. (2023). PAL: Program-aided language models. <em>Proceedings of the 40th International Conference on Machine Learning</em>, PMLR 202, 10764–10799.',
        'https://arxiv.org/abs/2211.10435'),
    'pot': ('Chen, W., Ma, X., Wang, X., &amp; Cohen, W. W. (2023). Program of thoughts prompting: Disentangling computation from reasoning for numerical reasoning tasks. <em>Transactions on Machine Learning Research</em>.',
        'https://arxiv.org/abs/2211.12588'),
    'react': ('Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., &amp; Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. <em>International Conference on Learning Representations</em>.',
        'https://arxiv.org/abs/2210.03629'),
    'mcp': ('Anthropic. (2024, November 25). Introducing the Model Context Protocol.',
        'https://www.anthropic.com/news/model-context-protocol'),
    'interop': ('Lee, Q. F. (2026). Agent interoperability standards: The Model Context Protocol, agent-to-agent protocols and integration with ERP, CRM and plant systems. <em>Chmltech Online Journal</em>, 105(4).',
        'https://www.chmltech.com/post/agent-interoperability-standards-mcp-a2a-erp-crm-plant-systems.html'),
    'bird': ('Li, J., Hui, B., Qu, G., Yang, J., Li, B., Li, B., Wang, B., Qin, B., Geng, R., Huo, N., Zhou, X., Ma, C., Li, G., Chang, K. C. C., Huang, F., Cheng, R., &amp; Li, Y. (2023). Can LLM already serve as a database interface? A big bench for large-scale database grounded text-to-SQLs. <em>Advances in Neural Information Processing Systems</em>, 36.',
        'https://arxiv.org/abs/2305.03111'),
    'llmcost': ('Lee, Q. F. (2026). Score versus cost per task: Measuring the returns to reasoning effort in frontier language models. <em>Chmltech Online Journal</em>, 104(7).',
        'https://www.chmltech.com/post/score-versus-cost-per-task-returns-to-reasoning-effort-in-frontier-language-models.html'),
    'evalag': ('Lee, Q. F. (2026). Evaluating AI agents: Why public benchmarks mislead and how to build your own evaluation. <em>Chmltech Online Journal</em>, 105(10).',
        'https://www.chmltech.com/post/evaluating-ai-agents-why-benchmarks-mislead-and-how-to-build-your-own-evaluation.html'),
    'selfcons': ('Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., &amp; Zhou, D. (2023). Self-consistency improves chain of thought reasoning in language models. <em>International Conference on Learning Representations</em>.',
        'https://arxiv.org/abs/2203.11171'),
    'agmfg': ('Lee, Q. F. (2026). Agentic AI in manufacturing operations: Use cases, architecture and safety boundaries. <em>Chmltech Online Journal</em>, 105(9).',
        'https://www.chmltech.com/post/agentic-ai-in-manufacturing-operations-use-cases-architecture-and-safety-boundaries.html'),
}

CODE = {"appendix": open(__file__.replace("paper_v106_i17.py", "models/oee/oee_appendix.py"), encoding="utf-8").read().rstrip()}

DOWNLOADS = [
    dict(file='oee_appendix.py', label='Appendix script', note='Reference OEE calculator (Python 3, standard library); needs the data files in the full package'),
    dict(file='chmltech-oee-llm-testset.zip', label='Dataset and test set', note='Four-week plant extract (CSV), reference and error study, 24 questions with answers, grader, README'),
]

BODY = r"""
## Introduction

A plant manager types "Which line lost the most last month, and on what?" into a chat assistant connected to the plant's production data, and gets a confident answer with one decimal place. Whether that number is right depends less on the language model's reasoning than on a chain of definitions the data does not state. Overall equipment effectiveness (OEE) multiplies availability, performance and quality [@nakajima], and the Chmltech OEE series showed how the three factors turn production hours into money [@oee1, @oee2]. Behind each factor sit choices: which stops were planned, which ideal rate applies to each product, whether a reworked unit is good, how two records of the same stop are combined and how shifts are added up. Reviews of OEE practice have long noted that plants apply these choices differently [@muchiri], which is why ISO 22400-2 defines the elements of each indicator [@iso].

Large language models (LLMs) are now being put between people and these data. A 2026 review of LLMs in smart manufacturing found applications from maintenance to production planning, and stressed human oversight and verification [@sadeqi]. The weak point for KPI questions is well documented: transformer models make errors on multi-step arithmetic that grow with the number of steps [@dziri], their mathematical answers change when irrelevant details of a problem change [@gsm], in 2023 evaluations they used information in the middle of a long context less reliably than information at its ends [@lostmid], and they can state unsupported content fluently [@ji]. A shift table of a hundred rows and a stop log of several hundred records is exactly that kind of input.

This paper asks three practical questions:

- Which OEE calculation errors matter most for the number and for the decisions taken from it?
- What architecture keeps an LLM useful for KPI questions without letting it compute the KPI?
- How can a plant test an assistant before trusting it?

It answers them with a four-week data extract from a composite bottling plant, a reference calculation, eight deliberate errors, and a 24-question test set released with the paper. It does not report scores for particular language models: such scores go stale within months [@llmcost], and a plant learns more by testing its own assistant on its own definitions [@evalag].

## OEE, Defined Precisely

OEE is the share of planned production time that turned into good product at the ideal rate. ISO 22400-2 builds it from time and quantity elements [@iso]. The **planned busy time** t<sub>PBT</sub> is the shift time less planned downtime such as breaks, scheduled maintenance and periods with no orders. The **actual production time** t<sub>APT</sub> is t<sub>PBT</sub> less unplanned downtime. Availability is their ratio, Eq. (1):

TEX A = \frac{t_{\mathrm{APT}}}{t_{\mathrm{PBT}}}

Performance compares the ideal time for the units actually made with the time the line ran, Eq. (2), where n<sub>k</sub> units of product k were made at an ideal rate r<sub>k</sub>:

TEX P = \frac{\sum_k n_k / r_k}{t_{\mathrm{APT}}}

Quality is the first-pass share of good output, Eq. (3); units that were rejected or reworked are not good at the first pass. With several products, each unit is weighted by its ideal time, so that a 2 L bottle counts for more than a 500 mL bottle; with one product this is simply good units over units produced:

TEX Q = \frac{\sum_k n_{\mathrm{good},k} / r_k}{\sum_k n_k / r_k}

The product of the three, Eq. (4), cancels the run time: OEE is the ideal time of the good output divided by the planned busy time.

TEX \mathrm{OEE} = A \cdot P \cdot Q = \frac{\sum_k n_{\mathrm{good},k} / r_k}{t_{\mathrm{PBT}}}

ISO 22400-2 calls the speed factor effectiveness and counts quality in units [@iso]; this paper uses the common term performance and weights units by ideal time so that Eq. (4) holds exactly for a multi-product line and the losses add up.

For a line over several shifts, or a plant over several lines, each element is summed first and the ratios are taken afterwards, Eq. (5). Averaging shift OEE values instead gives each shift the same weight whatever its length:

TEX A_{\mathrm{plant}} = \frac{\sum_s t_{\mathrm{APT},s}}{\sum_s t_{\mathrm{PBT},s}}, \quad P_{\mathrm{plant}} = \frac{\sum_s \sum_k n_{k,s}/r_k}{\sum_s t_{\mathrm{APT},s}}, \quad Q_{\mathrm{plant}} = \frac{\sum_s \sum_k n_{\mathrm{good},k,s}/r_k}{\sum_s \sum_k n_{k,s}/r_k}

The gap between the plain average and the time-weighted value of any ratio x<sub>s</sub> with weights w<sub>s</sub> (here t<sub>PBT,s</sub>) is minus the covariance between weight and value divided by the mean weight, Eq. (6), with the covariance taken over the n shifts (divisor n). It is zero when all shifts are equally long, and large when short shifts perform differently from long ones.

TEX \frac{1}{n}\sum_s x_s - \frac{\sum_s w_s x_s}{\sum_s w_s} = -\frac{\operatorname{Cov}(w, x)}{\bar{w}}

## The Test Plant and Its Data

The plant is a composite built for this paper: a bottling plant in Vancouver with three filling lines and three bottle sizes, ideal rates of 120, 80 and 50 bottles per minute for 500 mL, 1 L and 2 L bottles (Table 1). The extract covers four weeks, Monday to Saturday.

TABLE The three lines. || Ideal rates: 500 mL 120, 1 L 80, 2 L 50 bottles per minute. All values are design inputs of the composite plant. For simplicity, changeovers are placed inside planned downtime.
| Line | Share of run time | Shifts | Planned downtime besides breaks |
| L1 | 80% 500 mL, 20% 1 L | Day and evening, Monday to Friday; short Saturday day shift | None |
| L2 | 35% 500 mL, 40% 1 L, 25% 2 L | Day and evening, Monday to Friday | One evening with no orders (240 min) |
| L3 | 25% 1 L, 75% 2 L | Day shift only, Monday to Friday | Weekly planned maintenance (120 min) |

The extract has the three files a manufacturing execution system typically exports: a shift table with 104 rows (shift length, planned downtime, and units produced, rejected and reworked by product), a stop log with 772 unplanned stop records, and an item table with the ideal rates. Overlapping records are common: in 146 cases an operator logged on the line display (HMI) a stop that the controller (PLC) had already recorded, a minute or so apart, as often happens when two systems record downtime. Rejects run at 0.8% to 1.8% and rework at 0.4% to 2.5% depending on the line. Table 2 gives the reference results.

TABLE Reference results over four weeks. || Computed with Eqs. (1)–(5); overlapping stop records merged; reworked units counted as not good at the first pass. Plant planned busy time is 757 h; the three losses and the good output add up to it.
| | Availability | Performance | Quality | OEE | Downtime lost (h) | Speed lost (h) | Quality lost (h) |
| L1 | 89.0% | 90.0% | 98.6% | 78.9% | 35.2 | 28.4 | 3.6 |
| L2 | 89.6% | 86.1% | 97.0% | 74.9% | 30.7 | 36.8 | 6.8 |
| L3 | 89.0% | 93.1% | 96.7% | 80.1% | 15.6 | 8.8 | 3.8 |
| Plant | 89.2% | 89.1% | 97.6% | 77.6% | 81.5 | 74.0 | 14.2 |

Two facts in Table 2 drive decisions. L2 has the lowest OEE, and its largest loss is speed, not downtime, so the improvement project for L2 is a performance project (minor stops and reduced speed, especially on the 2 L product). On L1 and L3 the largest loss is downtime.

## Eight Ways to Get OEE Wrong

Each error below is a choice that a person, a spreadsheet, a database query or a language model can make when the definition is not pinned down. Each was applied alone to the same data (Table 3, Figure 1). The study shows how sensitive OEE is to each choice; it does not measure how often any assistant makes them.

TABLE Plant and line OEE under each calculation error. || Each error applied alone; all other elements as in the reference. Changes are computed from unrounded values. "Largest loss on L2" is not defined for the aggregation errors, which do not change the loss hours.
| Error | Plant OEE | Change (points) | L1 | L2 | L3 | Lowest line | Largest loss on L2 |
| Reference | 77.6% | — | 78.9% | 74.9% | 80.1% | L2 | Speed |
| E1 Average of shift OEE values | 77.5% | −0.04 | 79.0% | 74.6% | 80.1% | L2 | — |
| E2 Product of averaged A, P and Q | 77.5% | −0.04 | 79.0% | 74.6% | 80.1% | L2 | — |
| E3 One ideal rate, fastest product | 59.4% | −18.2 | 73.7% | 54.1% | 38.4% | **L3** | Speed |
| E3b One ideal rate, slowest product | 142.5% | +64.9 | 176.8% | 129.8% | 92.1% | **L3** | Downtime |
| E4 Planned downtime counted as loss | 71.6% | −6.0 | 74.1% | 69.3% | 71.1% | L2 | **Downtime** |
| E5 Overlapping stop records summed | 77.6% | 0.0 | 78.9% | 74.9% | 80.1% | L2 | **Downtime** |
| E6 Rework counted as good | 78.5% | +0.9 | 79.3% | 75.8% | 82.2% | L2 | Speed |
| E7 Unweighted mean of line OEEs | 78.0% | +0.4 | 78.9% | 74.9% | 80.1% | L2 | — |

FIG fig1-oee-by-error || Plant OEE over four weeks under the reference calculation and each of the eight errors; orange bars move the result by two points or more. || Horizontal bars of plant OEE: reference 77.6%; aggregation errors between 77.5% and 78.0%; rework counted as good 78.5%; planned downtime counted as loss 71.6%; one rate for the fastest product 59.4%; one rate for the slowest product 142.5%. ||

Figure 1 shows that the errors fall into two groups of very different size.

### 4.1 Aggregation errors were small here

Averaging shift OEE values (E1), multiplying averaged factors (E2) and averaging the three line values (E7) moved plant OEE by 0.04 to 0.4 points. Eq. (6) explains why: 95 of the 104 shifts have the same planned busy time (450 minutes), so the weights hardly vary; the few short shifts (Saturdays, maintenance days and the no-order evening) produce the small gaps seen. The unweighted line average (E7) is slightly high because L3, the line with the highest OEE, runs half as many hours as the others and gets a third of the weight. In a narrow slice the same error is large: on L2's evening shifts in week 3, which include the no-order evening, averaging shift values gives 71.3% against 73.3%. These errors grow in a plant whose shifts or lines differ more in length, or whose short shifts perform differently, but they did not change any ranking here.

### 4.2 Definition errors were large

**One ideal rate for all products (E3, E3b)** was the largest error. Using the 500 mL rate for every bottle made each 2 L bottle look as if it should have taken 0.5 seconds instead of 1.2, so performance on L3 fell to 44.6% and L3, the best line, appeared to be the worst. Using the slowest rate gave performance above 200% on L1 and an OEE of 142.5%, a value no reader should accept but a chat answer might still report. Ideal rates belong to the product, not the line, and must come from the item master.

**Planned downtime counted as a loss (E4)** turned breaks, planned maintenance and the no-order evening into availability losses and cut plant OEE by 6.0 points; L3, with its weekly maintenance, dropped from the best line to the middle. It also moved the largest loss on every line to downtime. That number measures something different (closer to overall operations effectiveness, which uses shift time as its base); it is not wrong in itself, but it is wrong when reported as OEE or compared with an OEE target.

**Rework counted as good (E6)** raised OEE by 0.9 points overall and by 2.1 points on L3, the line with the most rework. The difference is the cost of the rework loop, which OEE is meant to show.

### 4.3 A correct OEE can still point to the wrong project

Summing overlapping stop records instead of merging them (E5) left every OEE value unchanged, because run time cancels in Eq. (4) when it is derived as planned busy time minus stops; if run time is measured independently, for example from a PLC run signal, duplicated stops do change OEE. It still did damage. Summing all 772 records added 21.9 hours of downtime that did not happen (19.6 hours from the 146 HMI duplicates, 2.3 hours from controller records that overlap each other); availability fell by about three points and performance rose by the same amount, since the same output now appeared to come from fewer running hours. On L2 the largest loss moved from speed to downtime (Figure 2). A team reading that answer would start a downtime project on L2 when the reference data point to speed.

FIG fig2-loss-allocation || Hours lost to downtime, speed and quality on each line over four weeks: reference calculation, with overlapping stop records summed (E5), and with one ideal rate for all products (E3). The triangle marks each line's largest loss. || Three panels of grouped bars. Reference: L2's largest loss is speed. With duplicates summed, downtime becomes the largest loss on every line. With one ideal rate, speed losses on L2 and L3 grow to 100 and 70 hours. ||

CALLOUT The errors that matter are not slips of arithmetic but silent choices: which rate, which downtime counts, what is good and how records are merged. A tool can make each choice once, correctly and visibly; a fluent answer cannot show which one it made.

## Why the Language Model Should Not Compute the Number

Each error in Section 4 is either a definition choice or an algorithm. Neither is a good task for free text generation.

1. **Definition choices are made silently.** When a question says only "OEE", the model must pick a definition. The data rarely say which downtime codes are planned or whether reworked units count, and a fluent answer does not say which choice was made. Errors E3, E4 and E6 are plausible defaults when the definition is not supplied.
2. **Some steps are algorithms, not reading.** Merging overlapping stop intervals (E5) and weighting ratios by time (E1, E2, E7) are procedures over hundreds of rows. Accuracy on such compositional procedures falls as the number of steps grows [@dziri], and the 772 stop records and 104 shift rows of this small extract already exceed what can be checked by eye in a chat window, where information in the middle of a long context is the least reliably used [@lostmid].
3. **The answer looks the same whether it is right or wrong.** A wrong OEE of 59.4% reads exactly like a right one, and a model's answer can change when an irrelevant detail of the question changes [@gsm]. Without provenance, a user cannot tell a computed number from a plausible one [@ji].

The research response has been to let models call tools: models that learn when to call a calculator or search engine [@toolformer], prompting methods in which the model writes a program and an interpreter computes the answer [@pal, @pot], and agent loops that alternate reasoning with actions [@react]. Writing database queries from questions is a related approach, and a 2023 benchmark found it error-prone on large real databases [@bird]. Against raw tables it has a specific weakness for KPIs: a query that averages shift OEE values runs without error and returns E1. Text-to-SQL against governed views, or a semantic (metrics) layer that encodes the KPI definitions, is a valid form of the architecture below; the failure is generating SQL against raw tables. Generated code moves the arithmetic out of the model but leaves the definition choices in it. The architecture below moves both.

## A Tool-Grounded Architecture

The principle is a division of labour: the language model understands the question, chooses what to compute and explains the result; deterministic code holds the definitions and computes every number (Figure 3).

FIG fig3-architecture || Tool-grounded KPI architecture. The language model plans and explains; versioned KPI definitions and tested tools, inside the dashed boundary, compute every number from the plant data and return it with its provenance. || Flow diagram: a question goes to an LLM planner, which calls KPI tools; the tools read KPI definitions as code and the plant data, and return a result with provenance (rows, filter, definition id) to the LLM, which writes the answer subject to a number-echo check. ||

Table 4 lists the five components and the failure each one prevents.

TABLE Components of the architecture. || Tools are read-only and enforce the user's data permissions.
| Component | What it does | Prevents |
| KPI definitions as code | One versioned module states the ISO 22400 elements: planned downtime codes, ideal rate per product from the item master, rework rule, stop-merge rule, aggregation from sums | E3, E3b, E4, E6; two departments reporting different OEE |
| KPI tools | A few functions with typed inputs: compute_oee(lines, dates, shifts), loss_tree(...), merge_stops(...), compare(...); they return a data-quality error instead of a number when A, P or Q falls outside 0–100% or stops fall outside the shift | E1, E2, E5, E7; arithmetic in text; impossible values such as 142.5% |
| Planner (the LLM) | Turns the question into tool calls and filters; asks when the question is ambiguous ("All shifts, or day shifts only?") | Silent definition choices |
| Provenance | Every result carries the filter used, row counts and the definition version | Unverifiable answers; mixing old and new definitions |
| Number-echo check | Software confirms that every number in the answer matches a tool result for the same line, KPI and unit; differences come from the compare() tool, not the text. A stronger option: the model writes placeholders such as {oee.L2} that code fills in | Numbers the model made up, changed or attached to the wrong line |

The tools are exposed to the model through function calling or the Model Context Protocol, the open standard for connecting assistants to data and tools [@mcp, @interop]. The tools and definitions are ordinary software: they are written once, reviewed by the person who owns the KPI, and tested against a reference dataset like the one in this paper. The language model never sees raw shift rows when computing a KPI, which also keeps the context short and the cost low.

### 6.1 A worked exchange

Consider the question from the introduction, asked of the test plant: "Which line lost the most last month, and on what?" The planner does not read the shift table. It recognizes two requests and makes two tool calls: compute_oee for each line over the four weeks, and loss_tree for each line over the same period. The tools return, for each line, availability, performance, quality and OEE, the hours lost to downtime, speed and quality, the number of shift rows and stop records used (104 and 772, of which 199 overlapping records, including the 146 HMI duplicates, were merged), and the definition version.

The model then writes the answer from those results: L2 had the lowest OEE at 74.9%, and its largest loss was speed, 36.8 hours over the month, ahead of 30.7 hours of downtime; on L1 and L3 downtime was the largest loss. Before the answer is shown, the number-echo check confirms that 74.9 is L2's OEE and 36.8 and 30.7 are L2's speed and downtime losses in the tool output. The answer ends with its provenance line: lines L1 to L3, four weeks, 104 shifts, definition version 3.

Two things did not happen. The model did not decide whether the no-order evening on L2 counts against availability, because the definitions module had already classed it as planned. And the model did not add up stop durations, so the overlapping records could not inflate L2's downtime and redirect the answer toward a downtime project. If the user follows up with "and if we count the no-order evening?", the planner can call the same tool with a named alternative definition and say clearly that the result is no longer OEE as the plant defines it.

The same pattern answers questions the tools were not built for, within limits. "Was week 3 worse than week 1 on L2?" needs only filters. "Why was L2 slow?" needs data the tools do not have, such as minor stops below the logging threshold or line speed by product, and the right answer is to say so and name the data that would answer it.

The design follows the safety boundary set out for agentic AI in manufacturing operations [@agmfg]: the model may read and explain, while anything that becomes a plant record or a decision input is produced by deterministic, testable components.

## Testing an Assistant Before Trusting It

The paper's dataset comes with 24 questions and reference answers (Table 5). They are chosen so that each calculation error in Section 4 produces at least one wrong answer, and so that the ranking questions test decisions, not just numbers.

TABLE The 24-question test set. || Numeric answers must be within 0.1 percentage points or 0.1 hours; counts must be exact; ranking answers must match. Reference answers are in questions.json in the download package.
| Type | Questions | Example | Errors it exposes |
| Aggregate | 4 | What was line L2 OEE over the four weeks? | E1, E2, E3, E3b, E4, E6, E7 |
| Factor | 5 | What was line L3 quality (first-pass good share)? | E3, E3b, E4, E5, E6 |
| Filter | 4 | What was L2 OEE on evening shifts in week 3? | Wrong filters; planned no-order time; E1, E2, E3, E4, E6 |
| Stops | 2 | How many hours of unplanned downtime did L3 have? | E5 |
| Loss | 2 | How many hours were lost to speed on L1? | E3, E3b, E5, E6 |
| Count | 2 | How many bottles were reworked on L2? | Wrong columns |
| Rank | 5 | Which line had the lowest OEE? Which loss cost L2 the most hours? | E3, E3b, E4, E5 |

The test protocol is short:

1. Load only the three data files into the assistant's environment, the way production data would arrive; keep questions.json and results.json out of its reach. Give it the written definitions if you are testing the full system, and withhold them if you are testing whether it asks.
2. Ask each question in a fresh conversation, three times. Repeated runs expose answers that change from run to run; sampling several answers and comparing them is itself a known way to improve reasoning reliability [@selfcons].
3. Score with the grader in the package. Accept the assistant only if all 24 answers are within tolerance in all three runs.
4. For every miss, find the layer that failed: a wrong tool call (planner), a wrong definition (KPI module), a wrong number in the text (number-echo check).

Because a public test set may enter future training data, the real test is a plant's own. A plant should replace the composite data with a month of its own, compute the reference answers with its own definitions module, and keep the test as a regression check that is run whenever the model, the prompt or the definitions change [@evalag].

## Implementation Guide for SMEs

A small or mid-sized plant can put this architecture in place in an estimated six weeks with its existing MES or spreadsheet exports.

1. **Write the definitions down (week 1).** List the planned downtime codes, take ideal rates per product from the item master (not the line nameplate), decide how rework is counted, and state that stops are merged and KPIs aggregated from sums. Use ISO 22400 names so that the document survives staff changes [@iso].
2. **Build the reference calculator (weeks 2–3).** A script like the one in the Appendix, or SQL views, that computes Table 2 for any filter. Check it against a month the team already knows.
3. **Wrap it as four or five tools (week 4).** Typed inputs (lines, dates, shifts), outputs with the filter, row counts and the definition version.
4. **Connect the assistant (week 5).** Give it the tools, a short instruction that every number must come from a tool, and permission to ask when a question is ambiguous. Add the number-echo check to the output step.
5. **Test and monitor (week 6 onward).** Run the 24-question protocol on the composite data, then on the plant's own data. Log every question, tool call and answer.

### 8.1 Pitfalls

- **Nameplate rates.** A line's nameplate rate is usually its fastest product's rate, which is E3 in disguise. Rates belong to products.
- **Two downtime sources.** If the controller and the operator display both log stops, decide which is the record or merge them; never add them.
- **Changing the definition without a version.** A new rule for planned downtime makes last month's OEE incomparable. Version the definitions and show the version in every answer.
- **Letting the model fill gaps.** If a product has no ideal rate, the tool should return an error, not a guess, and the assistant should say what is missing.
- **Impossible values.** A performance or OEE above 100% means a wrong rate or a data error. The tool should refuse to return it.
- **Testing once.** Model updates change behaviour. Rerun the test set after every change of model, prompt or definitions.

## Conclusions

OEE questions look like arithmetic but are mostly definitions. On four weeks of data from a composite three-line plant:

- Averaging errors moved plant OEE by at most 0.4 points, because planned busy times hardly varied, but by 1.9 points in one narrow slice; they grow with the covariance between planned busy time and shift OEE.
- Definition errors were far larger: one ideal rate for all products gave 59.4% or 142.5% against a reference of 77.6% and made the best line look the worst; counting planned downtime as a loss cost 6.0 points and made downtime the largest loss on every line; counting rework as good added 0.9 points overall and 2.1 on the line with the most rework.
- Summing overlapping stop records left every OEE value unchanged but moved L2's largest loss from speed to downtime, which would send the improvement team to the wrong problem.
- Each error is a silent choice or an algorithmic step, so the language model should choose filters and explain results while versioned definitions and tested tools compute every number, with provenance and a number-echo check on the final text.

The study uses one composite plant and does not measure particular language models. The released dataset, test set and grader let any plant measure its own assistant against its own definitions, and the same pattern applies to other KPIs whose definitions carry choices, such as first-pass yield, schedule adherence and mean time between failures.

## Appendix: Python Code

The compact calculator below reproduces Table 2 from the three data files in the download package. It uses only the Python standard library.

CODE appendix || Reference OEE calculator (compact version).
"""
