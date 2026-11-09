import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from insert import apply
P = __file__.rsplit("/", 2)[0] + "/journal/multi-agent-ai-systems-architectures-coordination-and-failure-modes.json"
apply(P, [
 dict(sec="3", after=0, ref=("3", 0), sentence="Figure 1 draws the five patterns side by side; the main differences to notice are where control sits and whether agents read each other's output directly, through a shared workspace, or only through a lead agent.",
      fig=dict(n=1, id="fig1-topologies", caption="The five coordination topologies of Table 1: (a) orchestrator–worker, (b) hierarchical, (c) peer and debate with an optional judge, (d) blackboard and (e) sequential pipeline with an optional verifier stage. Arrows show the direction of messages or hand-offs; dashed elements are optional.",
               alt="Five small node-and-arrow diagrams. (a) A lead agent sends tasks to three workers, which return results only to the lead. (b) A manager supervises two sub-managers, each with two workers. (c) Three peer agents are connected to each other by two-way arrows, with an optional judge. (d) Four agents read from and write to a central shared workspace. (e) Four agents in a chain pass hand-off artifacts forward, with an optional verifier between the third and fourth stages.",
               source="Drawn by the author from Table 1 and the works cited there.")),
 dict(sec="7", after=3, ref=("7", 3), sentence="Figure 2 plots Eq. (2) for these parameters: the cross-reading term already supplies half of the tokens at N = 3 and dominates as agents are added, which is the term that isolated worker contexts remove.",
      fig=dict(n=2, id="fig2-token-growth", caption="Token multiplication in broadcast debate from Eq. (2) with T<sub>0</sub> = 1,000 and L = 500 tokens. (a) Total tokens against the number of agents N for R = 2, 3 and 4 rounds, with the linear terms alone for R = 3 shown dashed. (b) Share of each term of Eq. (2) at R = 3.",
               alt="Two-panel chart. Left: total tokens in thousands against number of agents from 1 to 10; curves for 2, 3 and 4 rounds rise quadratically, reaching about 80, 195 and 360 thousand tokens at 10 agents, while the linear-terms-only line for 3 rounds reaches only 45 thousand. The worked example of 27,000 tokens at 3 agents and 3 rounds is marked. Right: stacked bars for 1 to 8 agents showing the cross-reading term growing from 25% to over 70% of the total.",
               source="Author's calculation from Eq. (2).")),
 dict(sec="7", after=13, ref=("7", 13), sentence="Figure 3 extends these examples to longer pipelines and shows that the benefit of a verifier grows with the number of stages.",
      fig=dict(n=3, id="fig3-compounding-error", caption="End-to-end success probability of a sequential pipeline from Eq. (4) for per-stage reliabilities of 0.99, 0.95 and 0.90, and for p = 0.95 with a verifier (δ = 0.8, ρ = 0.7) from Eq. (5). Marked points are the worked values of Section 7.3. Errors are assumed independent and verifier false alarms are ignored.",
               alt="Line chart of end-to-end success probability against number of pipeline stages from 1 to 20. Without verification, success falls to 0.82, 0.36 and 0.12 at 20 stages for per-stage reliabilities of 0.99, 0.95 and 0.90. With a verifier, the 0.95 case falls only to 0.64 at 20 stages. Points mark 0.774 at 5 stages, 0.599 at 10 stages and 0.895 at 5 stages with verification.",
               source="Author's calculation from Eqs. (4) and (5).")),
])
print("placed")
