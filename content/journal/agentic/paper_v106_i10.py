"""Chmltech Online Journal, Vol. 106, Issue 10 (Multi-Agent AI Engineering series, Article 2). Figure 1 is interactive (live/mae2.html)."""

SLUG = 'sequential-and-parallel-multi-agent-workflows-four-execution-patterns-and-their-engineering-trade-offs'
META = dict(
    volume=106,
    issue=10,
    title='Sequential and Parallel Multi-Agent Workflows: Four Execution Patterns and Their Engineering Trade-offs',
    short_title='Sequential and Parallel Multi-Agent Workflows',
    meta='Sequence, parallel, series–parallel and parallel–series workflows for LLM agents compared: dependencies, critical paths, join rules, failure handling and an SME example.',
    keywords=['multi-agent AI', 'agent workflows', 'parallel execution', 'fan-out fan-in', 'critical path', 'workflow orchestration', 'DAG scheduling', 'LLM agents'],
)
ABSTRACT = 'Multi-agent AI systems are often compared by the number of agents they employ or the sophistication of their orchestration frameworks. For production engineering, however, a more fundamental question is which tasks depend on which others, and when may they run? This paper examines four practical execution patterns: sequence, parallel, series–parallel, and parallel–series. It distinguishes execution order from organizational topology; models workflows as dependency graphs; explains fan-out, fan-in, barriers, and branch-level state; and derives latency and resource implications using simple critical-path calculations. A worked SME warehouse-management-system (WMS) assessment illustrates how the same tasks yield different completion times when their dependencies change. The analysis also covers context isolation, structured handoffs, bounded concurrency, stragglers, failure containment, observability, and authorization. The central recommendation is to choose the simplest dependency graph that preserves correctness, and to add parallelism only when independent work, reliable aggregation, and adequate operational controls justify the added complexity. A selection method and a minimum evaluation suite are proposed for teams choosing between the patterns.'

REFS = {
    'r1': ('Lee, Q. F. (2026). <em>Multi-Agent AI Systems: Architectures, Coordination Patterns and Failure Modes.</em> Chmltech Online Journal.',
           'https://www.chmltech.com/post/multi-agent-ai-systems-architectures-coordination-and-failure-modes.html'),
    'r2': ('OpenAI. (n.d.). <em>Agents SDK: Agent orchestration.</em>',
           'https://openai.github.io/openai-agents-python/multi_agent/'),
    'r3': ('Microsoft. (n.d.). <em>Agent Framework: Sequential orchestration.</em>',
           'https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/sequential'),
    'r4': ('Microsoft. (n.d.). <em>Agent Framework: Concurrent orchestration.</em>',
           'https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/concurrent'),
    'r5': ('Microsoft. (n.d.). <em>Agent Framework: Workflow concepts.</em>',
           'https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/'),
    'r6': ('LangChain. (n.d.). <em>Graph API overview</em>. LangGraph documentation.',
           'https://docs.langchain.com/oss/python/langgraph/graph-api'),
    'r7': ('Hadfield, J., Zhang, B., Lien, K., Scholz, F., Fox, J., &amp; Ford, D. (2025, June 13). <em>How we built our multi-agent research system</em>. Anthropic Engineering.',
           'https://www.anthropic.com/engineering/multi-agent-research-system'),
    'r8': ('Amazon Web Services. (n.d.). <em>Step Functions: Parallel workflow state.</em>',
           'https://docs.aws.amazon.com/step-functions/latest/dg/state-parallel.html'),
    'r9': ('Amazon Web Services. (n.d.). <em>Step Functions: Handling errors in workflows.</em>',
           'https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html'),
    'r10': ('Google Cloud. (n.d.). <em>Workflows: Parallel steps.</em>',
           'https://docs.cloud.google.com/workflows/docs/reference/syntax/parallel-steps'),
    'r11': ('OpenTelemetry. (n.d.). <em>Traces</em>. OpenTelemetry documentation.',
           'https://opentelemetry.io/docs/concepts/signals/traces/'),
    'r12': ('OpenAI. (n.d.). <em>Agents SDK: Tracing.</em>',
           'https://openai.github.io/openai-agents-python/tracing/'),
    'r13': ('Dean, J. &amp; Barroso, L. A. (2013). <em>The Tail at Scale.</em> Communications of the ACM 56, 74–80.',
           'https://research.google/pubs/the-tail-at-scale/'),
    'r14': ('National Institute of Standards and Technology. (2023). <em>AI RMF Core</em> (AI RMF 1.0, NIST AI 100-1 excerpt). NIST Trustworthy and Responsible AI Resource Center.',
           'https://airc.nist.gov/airmf-resources/airmf/5-sec-core/'),
    'r15': ('OWASP. (n.d.). <em>LLM06:2025 — Excessive Agency.</em>',
           'https://genai.owasp.org/llmrisk/llm062025-excessive-agency/'),
}

CODE = {
    'wms': 'import asyncio\n\nasync def assess_wms(request):\n    scope = await intake_agent(request)\n    validate_scope(scope)\n\n    # Independent specialists share an approved, read-only scope.\n    async with asyncio.timeout(90):\n        vendor, integration, operations = await asyncio.gather(\n            vendor_agent(scope),\n            integration_agent(scope),\n            operations_agent(scope),\n        )\n\n    # The join is a validation point, not just string concatenation.\n    for artifact in (vendor, integration, operations):\n        validate_schema_sources_and_scope(artifact, scope)\n\n    draft = await synthesis_agent(scope, vendor, integration, operations)\n    review = await verifier_agent(scope, draft)\n    if not review.passed:\n        return {"status": "needs_revision", "issues": review.issues}\n\n    return {"status": "ready_for_human_approval", "draft": draft}\n',
}

BODY = r"""
## Introduction: Execution Order Is an Architecture Decision

It is tempting to equate more concurrent AI agents with a faster or more capable AI system. That conclusion ignores the character of the work. Some operations cannot begin until a prior result exists. Others can be researched independently and combined later. Still others contain several specialized chains that may execute together but must remain sequential internally. The engineering challenge is to expose genuine independence while preserving necessary dependencies, evidence provenance, permissions, and quality checks.

Contemporary frameworks explicitly support sequential and concurrent execution. Microsoft's Agent Framework describes sequential orchestration as a pipeline in which each agent receives work from its predecessor, and concurrent orchestration as independent agents whose results are aggregated [@r3, @r4]. OpenAI's Agents SDK documents both agent chaining and parallel execution under code-controlled orchestration [@r2]. LangGraph expresses the same fundamental ideas through state, nodes, edges, parallel super-steps, and reducers [@r6]. These abstractions are useful because the scheduling problem is not exclusive to any particular model provider.

This paper focuses on the four patterns shown in Figure 1: **(1) sequence; (2) parallel; (3) series–parallel; and (4) parallel–series**. The latter two are practical descriptive names for hybrid dependency shapes, not universally standardized product features. Their interpretation must therefore be made explicit in every architecture document. All four may operate within a centralized orchestrator, a hierarchy, or a more distributed agent architecture; the control topology and execution graph are separate choices [@r1].

The evaluation uses four questions: *What must finish before another task starts? Where does information cross agent boundaries? What is the critical path for completion? What happens when a branch is wrong, late, or unavailable?* The answers determine both speed and trustworthiness more reliably than the agent count alone.

## Foundations: Tasks, Dependencies, and Data Contracts

### 2.1 Model the workflow as a directed graph

Represent each unit of work as a node and each required handoff as a directed edge. A node may be an LLM agent, deterministic function, database query, human review, or external service; a graph does not require every node to be autonomous. An edge indicates that an output, approval, or dependency must be available before the downstream node can proceed. When there are no intentional cycles, the workflow is a **directed acyclic graph (DAG)**; deliberate review loops need explicit stopping rules, and LangGraph caps each run with a recursion limit on super-steps [@r6].

The graph distinguishes two kinds of dependency. A **data dependency** means that a downstream task needs a specific artifact or fact. A **control dependency** means that policy requires a task or gate to complete first, even if the later work could otherwise begin. For example, a WMS vendor investigation may run in parallel with process mapping, but a recommendation may require both outputs and an explicit validation step.

### 2.2 Define the handoff before choosing the scheduler

Each task should have a contract: task ID, objective, accepted input types, allowed tools, output schema, evidence requirements, deadline, retry budget, data classification, and owner. A structured contract prevents a parallel worker from returning an attractive narrative that the aggregation step cannot reliably use. A common execution ledger should distinguish *queued, running, completed, failed, skipped,* and *approved* states. A final answer is an artifact that passes its acceptance criteria, not merely the last message generated.

**Execution parallelism is not the same as independent judgment.** Two agents using the same model, same evidence, and nearly identical prompts may produce correlated mistakes even if they execute at the same time. Parallel work can shorten latency without increasing epistemic diversity. Conversely, a sequential reviewer may add valuable independent verification if it checks primary evidence rather than paraphrasing the previous agent.

FIG fig1-patterns || The four execution patterns. The figure plays through each pattern in turn, showing which tasks wait for which results; select a pattern to jump to it, or <em>All patterns</em> to compare them side by side. Speed and cost depend on the workload and the controls described in this paper, so no pattern is rated faster or slower in general. || Four small dependency diagrams: a sequential chain of agents, a fan-out to parallel agents and a merge, an ordered pipeline with one parallel stage, and parallel lanes each holding an ordered chain, each labelled with when it fits and its main risk. || 

## Pattern 1 — Sequence: A Controlled Chain

A sequential workflow runs tasks in a defined order, usually A → B → C → D. Each stage consumes a validated artifact from its predecessor. A research agent might gather sources, an analyst normalize evidence, a writer prepare a draft, and a reviewer evaluate it. The main benefit is unambiguous ordering. The main limitation is that independent subtasks remain idle while the chain advances.

**Appropriate conditions.** A later step genuinely needs a previous result; stages have different data privileges; auditability matters; or the work is a deterministic transformation pipeline. Sequential flows are a useful baseline because they are easy to reason about and easy to compare with more complex designs. Microsoft's sequential guidance also highlights a subtle implementation choice: the next agent may receive the *full previous conversation* rather than only the predecessor's final response, depending on configuration [@r3]. That choice affects context growth, information exposure, and reproducibility.

**Failure mechanisms.** An upstream error propagates downstream; a slow stage delays every later one; and cumulative context may bury important instructions or source details. Agent-to-agent text transfer can also turn a malicious or incorrect upstream output into a new downstream instruction. Good handoffs use typed output, source references, and explicit separation of data from commands.

**Engineering controls.** Validate outputs at each boundary; retain the original artifact rather than only a summary; set clear retry versus rework policies; and reject silent substitutions when an upstream dependency is absent. A sequential reviewer should independently check claims against authoritative sources. If task B fails, task C should not begin under a false impression that B succeeded.

## Pattern 2 — Parallel: Fan-Out and Fan-In

A parallel workflow starts two or more independent tasks after a shared input is ready. The scheduler fans work out to separate agents, and an aggregation function fans results back in. In notation, Start → {A, B, C} → Merge. This is particularly useful for retrieving distinct sources, translating into unrelated languages, analyzing independent datasets, or comparing alternative proposals. Microsoft documents a concurrent agent workflow with fan-out/fan-in edges and an aggregation barrier; OpenAI also describes parallel execution through ordinary Python primitives [@r2, @r4].

The key condition is **safe independence**. Workers may share a read-only brief, but one branch should not quietly edit another branch's assumptions. Where branches update shared state, the system needs explicit merge rules. LangGraph, for example, uses reducers to define how concurrent node updates combine [@r6]. An aggregator should check required branch coverage, schema compliance, conflicts, provenance, and whether an incomplete result is acceptable.

**Latency is constrained by the slowest required branch, not by the average worker.** Parallel starts are not always simultaneous in practice: model API limits, tool quotas, queueing, or unavailable resources can serialize work. Tail latency also matters because large fan-outs increase the chance that at least one worker responds unusually slowly, a general distributed-systems issue examined by Dean and Barroso [@r13]. Anthropic reports using parallel subagents and parallel tool calls for complex research, while also noting that poor delegation can duplicate work and waste resources [@r7].

**Engineering controls.** Set maximum concurrency and per-branch deadlines. Keep the shared brief immutable during a run. Define whether the join is *all required*, *minimum quorum*, or *best-effort*, with different policies for safety-critical and optional outputs. Record partial failures explicitly; do not silently interpret a missing branch as a negative finding. Google Cloud Workflows documents concurrency limits and careful handling of shared variables as part of parallel workflow design [@r10].

## Pattern 3 — Series–Parallel: Ordered Stages with Parallel Work Inside

The term **series–parallel** is used here for a workflow that has a serial structure at the top level, with one or more stages containing independent parallel tasks. A typical shape is Intake → {Research, Technical Assessment, Risk Review} → Synthesis → Approval. The initial stage establishes a common baseline. A fan-out stage then distributes distinct work packages. A barrier requires selected outputs before downstream synthesis proceeds.

This shape is common in business and engineering analysis because it preserves an accountable end-to-end process while shortening its broad investigation phase. A single intake package can establish the client objectives, scope, constraints, and source inventory. Specialist agents work from that package, produce artifacts, and return evidence to a lead that reconciles contradictions and prepares the result. The orchestrator may remain centralized throughout; it is the **execution graph** that contains parallelism.

The difficult point is the **join**. Suppose vendor screening finishes quickly, but integration risk assessment identifies an unknown data-migration interface. Should the recommendation be blocked, published with a limitation, or sent for additional evidence? The join policy must answer that before execution. A barrier that treats all branch outputs as equivalent can falsely imply that an uncertain branch has passed. AWS Step Functions models a Parallel state and documents its failure semantics: an unhandled failure in any branch fails the entire Parallel state; the underlying external task may still need its own cancellation or cleanup logic [@r8].

**Advantages.** A clean global sequence; local concurrency only where dependencies permit; natural synthesis points; easier review of shared assumptions. **Limitations.** Barrier-induced waiting, duplicated searches, mismatched evidence quality, and possible overloading of the aggregation agent. A late or flawed branch can become the critical path even when most specialists have completed useful work.

## Pattern 4 — Parallel–Series: Concurrent Specialist Pipelines

The term **parallel–series** is used here for two or more parallel lanes, each containing an internally sequential chain. A schematic form is Start → {A1 → A2; B1 → B2; C1 → C2} → Merge. For example, a commercial lane may research vendors and then score business fit; a technical lane may inspect system interfaces and then assess implementation risk; an operational lane may map processes and then test workflow scenarios. All lanes begin from the same approved scope, but the steps inside each lane have meaningful dependencies.

This configuration is valuable when specialist work packages naturally contain several ordered activities. It isolates each lane's context, tool permissions, and intermediate artifacts. It also allows a technical supervisor to improve a lane without redesigning every other lane. But lane construction imposes constraints: assigning two independent tasks to one serial lane can unnecessarily increase the completion time, while dividing a genuinely dependent task across lanes can create a race or a hidden cross-lane dependency.

**Advantages.** Dedicated domain pipelines, predictable ownership within each lane, and opportunities for parallel throughput at the program level. **Limitations.** Branch-level error propagation, more complicated scheduling and progress tracking, and the risk that a critical dependency is discovered too late. A lane may appear finished while its assumptions conflict with another lane. The final merge therefore needs explicit conflict detection and issue ownership.

Unlike a staged series–parallel workflow, a parallel–series design can preserve multiple independent chains over the lifetime of the work. These are descriptive models, not mutually exclusive categories: a large application can nest both shapes at different levels. Figure 2 makes the dependency difference explicit. The companion paper on stage-gate orchestration (Vol. 106, Issue 11) treats **feedback loops** in greater depth; loops should be added with pass/fail conditions and maximum iteration budgets, not as open-ended self-correction.

FIG fig2-hybrid-dags || Two hybrid dependency graphs with different scheduling meaning. Series–parallel places concurrent tasks inside an ordered stage; parallel–series places ordered steps inside concurrent lanes. Arrows show required dependencies; task names and layouts are illustrative. || Two flow diagrams: in the first, intake fans out to research and technical-check branches that join at a synthesis barrier before a quality gate; in the second, two lanes of two ordered steps each run side by side and merge into a cross-lane check before the verified output. || 

## Performance Engineering: Latency, Cost, and Critical Paths

### 7.1 Idealized latency equations

Let *t*<sub>i</sub> be the processing time of task *i*, *o* the orchestration and communication overhead, and *t*<sub>m</sub> the time required to reconcile concurrent results. Under a simplifying assumption of deterministic runtimes, unlimited capacity, and no failures, the patterns have useful lower-bound relationships:

for a sequential chain, Eq. (1); for a single parallel block, Eq. (2); for series–parallel, summing over stages *s*, Eq. (3); and for parallel–series, taking the slowest lane *ℓ*, Eq. (4):

TEX T_{\text{seq}} = \sum_i t_i + o

TEX T_{\text{par}} = \max(t_1, t_2, \ldots, t_n) + t_m + o

TEX T_{\text{SP}} = \sum_{s} \max_{i \in s} t_i + o

TEX T_{\text{PS}} = \max_{\ell} \sum_{i \in \ell} t_i + t_m + o

These are **illustrative scheduling equations**, not measured benchmarks or provider-specific guarantees. For a general DAG, the minimum completion time under unlimited resources is the duration of its **critical path**, the longest directed sequence of dependent tasks. Actual latency exceeds the idealized value when model calls queue, context transfer consumes time, external tools throttle, branches retry, or a reviewer rejects an artifact. Two workflows with identical tasks can have very different completion times depending on which edges are necessary.

### 7.2 Speedup is not free

Define *speedup* relative to a correct sequential baseline as in Eq. (5):

TEX S = \frac{T_{\text{seq}}}{T_{\text{candidate}}}

where *T*<sub>candidate</sub> is the completion time of the schedule being compared. A value above 1 indicates reduced elapsed time in that illustrative scenario. It does not necessarily mean lower cost: parallel agents may each consume model tokens, repeat retrievals, maintain separate contexts, or require more coordination. Likewise, a faster response is not better when it bypasses verification or uses incomplete evidence. Report **both latency and accepted-output quality**, preferably with a cost-per-accepted-artifact measure.

### 7.3 Stragglers, tails, and saturation

A parallel join often waits for the slowest required branch. Adding workers can reduce average processing time for a divided workload, yet increase exposure to a late straggler or rate limit. Dean and Barroso described how tail behavior becomes significant as distributed requests touch more components [@r13]. In agent workflows, repeated web searches, heterogeneous model speeds, tool unavailability, and slow human approvals can all create tails. Controls include per-branch deadline budgets, queuing, conservative fan-out, preapproved fallback paths, and separating mandatory outputs from optional enhancements.

## Worked Example: SME WMS Assessment Using the Same Work Packages

Consider a hypothetical Vancouver SME preparing to select a warehouse-management system. The engineering objective is a source-backed recommendation, not an automatic purchasing decision. Six work packages are estimated with **illustrative elapsed times** (Table 1). The numbers are chosen for clarity and are **not measurements from a client, product, benchmark, or deployed agent system**.

TABLE Hypothetical work-package inventory. || These task dependencies are assumed for the case study. Durations omit dispatch, queueing, communication, retries, model cost, and human waiting time.
| Task | Work package | Duration (minutes) | Must follow |
| A | Intake and requirement normalization | 4 | Start |
| B | Vendor capability analysis | 10 | A |
| C | Integration and migration assessment | 8 | A |
| D | Operations and risk review | 6 | A |
| E | Evidence synthesis and option scoring | 5 | B, C, D |
| F | Independent recommendation verification | 4 | E |

A purely sequential schedule executes A–B–C–D–E–F in **37 minutes**. A series–parallel design executes A, fans out B/C/D, waits for all three, then runs E and F: **4 + max(10, 8, 6) + 5 + 4 = 23 minutes**. A parallel–series design can preserve the same logical requirements but place B→D within one technical/commercial lane and C in another lane, followed by E and F: **4 + max(10 + 6, 8) + 5 + 4 = 29 minutes**. This second hybrid intentionally serializes B and D for workflow ownership; the constraint is a design choice, not an intrinsic requirement of the task. Table 2 compares the three schedules and Figure 3 draws them on a common time axis.

TABLE Ideal completion time of one schedule per pattern. || Derived from the Table 1 assumptions with zero orchestration overhead. The comparison describes one plausible schedule for each pattern, not a universal ranking.
| Scheduling choice | Ideal completion time | Relative speedup | Principal trade-off |
| All tasks in sequence | 37 min | 1.00× | Simple, but independent activities wait |
| Series–parallel (B, C, D concurrent) | 23 min | 1.61× | Faster; join waits for the 10-minute branch |
| Parallel–series (B→D in lane 1; C in lane 2) | 29 min | 1.28× | Clear lane ownership, but extra serial dependency |

**Interpretation.** The lowest theoretical latency comes from the schedule that removes unnecessary dependencies. The optimal production design may still choose a slower path if it improves source control, independent review, or accountability. In every case, E must verify that the vendor, integration, and operations findings use the same scope and currency; F must check evidence completeness, unsupported claims, and decision constraints. No procurement action is authorized by this workflow alone.

FIG fig3-schedules || The same six work packages scheduled three ways. Completion times follow from the dependency assumptions in Table 1 and exclude runtime overhead and failures; colour marks the work package, not a rating. || Three horizontal timelines of six colored task bars on a common minutes scale: a sequential schedule ending at 37 minutes, a series–parallel schedule ending at 23 minutes, and a parallel–series schedule ending at 29 minutes. || 

## Reliability, Security, and Failure Handling

**Branch-level state and retries.** Every parallel unit should have a durable identity and result status. Retrying a report-generation task may be harmless, while retrying a real email send, database write, or payment may cause duplicates unless the action is idempotent or guarded with a transaction key. AWS Step Functions documents retriers, catch handlers, backoff, and error propagation; equivalent controls must be designed when using raw Python or custom orchestrators [@r9].

Table 3 summarizes the failure modes and their controls. **Join contracts.** Specify whether the merge requires every output, a subset, or a policy-defined quorum. Check that each input is a complete, valid artifact rather than a partial chat response. A branch can be *completed* but *unacceptable* because it lacks evidence, exceeds scope, or conflicts with required constraints. The aggregation agent should not infer missing data from a successful sibling branch.

**Context and prompt-injection boundaries.** Source documents, web pages, and other agents' outputs can carry instructions masquerading as evidence. Treat such text as data, restrict tool permissions by branch, and enforce authorization in the downstream service rather than relying on a model to police itself. OWASP's Excessive Agency guidance specifically calls for minimum functionality, minimum privileges, and approval for high-impact actions [@r15]. A concurrent system often expands the number of untrusted inputs the lead agent reads, making this discipline particularly important.

**Recovery and human review.** Persist a run ID, task ledger, artifact versions, and the set of completed dependencies. On resume, re-run only what is safe or necessary, and preserve the source context for audits. Reserve human approval for externally consequential actions such as procurement commitments, public publication, client outreach, or changes to plant operations. NIST's AI RMF emphasizes testing, documented evaluation measures, production monitoring, and recovery planning [@r14].

TABLE Failure modes and recommended controls. || Engineering recommendations adapted from workflow, security, and operational guidance [@r6, @r8, @r9, @r10, @r14, @r15].
| Failure or ambiguity | Where it appears | Recommended response |
| Upstream error is reused as a fact | Sequential chain | Validate stage outputs; preserve original evidence |
| One branch is missing at the join | Parallel / series–parallel | Block or publish explicit incompleteness under a defined policy |
| Two branches write conflicting values | Shared-state parallelism | Use typed reducers, version checks, or issue resolution |
| Slow branch governs all completion | Parallel join | Budget deadlines; label required vs optional work |
| External action repeats after retry | Any pattern | Enforce idempotency, transaction keys, and tool-specific safeguards |
| Agents exchange malicious instructions | Any multi-agent handoff | Treat peer output as untrusted data; enforce least privilege |

## Implementation Blueprint: A Bounded Series–Parallel Workflow

Example 1 is **illustrative pseudocode** in Python. It shows execution shape, validation, and bounded waiting without claiming to implement a specific framework's complete production API. It deliberately separates work execution from approval of side effects.

CODE wms || Example 1. Illustrative bounded series–parallel workflow in Python: shape, validation and bounded waiting, not a framework's production API.

The example assumes the caller also handles cancellations, retries, tool authentication, data classification, persistent state, rate limits, and observability. <em>asyncio.gather</em> is not an authorization or reliability framework; it is a concurrency primitive. A production service should make its failure semantics explicit and avoid assuming that cancellation of a waiting coroutine guarantees termination of external side effects. Graph-based frameworks can express the fan-out/fan-in dependencies explicitly and can checkpoint state at defined boundaries [@r5, @r6, @r8].

### 10.1 Handoff contract and trace structure

A useful branch output might include task ID, scope version, status, claim, evidence references, confidence basis, known gaps, runtime, and cost. A join operation should reject an artifact with a mismatched scope version, absent evidence, or an unsupported status. Use a trace ID across the whole request, with span IDs for each agent/tool call and a separate event for each validation result. OpenTelemetry describes spans, trace IDs, and parent–child relationships; the OpenAI Agents SDK also provides workflow and agent tracing [@r11, @r12].

### 10.2 A minimum evaluation suite

Before releasing a workflow, evaluate it on representative inputs with easy, ambiguous, conflicting, and incomplete evidence. Record (a) accepted-output rate, (b) p50 and p95 end-to-end latency, (c) tokens and tool spend per accepted output, (d) branch failure and retry rate, (e) evidence traceability, and (f) reviewer intervention. A schedule should not be declared superior on latency alone. Compare to a single-agent or deterministic baseline, because additional agents are not automatically necessary [@r1, @r7].

## Pattern-Selection Method

Start by drawing the true dependency graph without assigning agent names. Remove dependencies that are conveniences rather than requirements; keep those imposed by source validity, safety, approval, and data availability. Estimate each node's runtime, variability, tool cost, permissions, and failure probability. Mark which outputs are **mandatory** for synthesis. Table 4 turns these questions into a selection heuristic. Only then choose how many agents to instantiate and whether to implement the graph with code, a workflow engine, or an agent platform.

TABLE Practical selection heuristic. || Hybrid shapes can be nested and adjusted as task dependencies become better understood.
| Engineering question | Pattern that may fit | Avoid this mistake |
| Must every stage consume a predecessor's result? | Sequence | Passing unchecked full transcripts as facts |
| Can independent tasks use one stable brief? | Parallel | Spawning workers without a merge/acceptance rule |
| Is there a clear initial gate, parallel investigation, then synthesis? | Series–parallel | Treating partial branch outputs as complete |
| Do specialist domains need multi-step internal pipelines? | Parallel–series | Creating artificial serial lanes for independent tasks |
| Are results consequential or disputed? | Add an explicit review gate | Assuming more agents means better assurance |

**Engineering recommendation.** For source-based SME advisory or technical research, a series–parallel workflow is often a strong initial design: a common scoping step; independent specialist investigation; explicit synthesis; and an independent quality gate. Use parallel–series when specialist work naturally contains several dependent steps that can be owned and tested together. Preserve a sequential baseline for benchmarking and keep a single-agent option for simple tasks. These recommendations are design judgments, not measured claims of universal superiority.

## Conclusion

Multi-agent workflow design begins with dependencies, not agent count. Sequence creates a straightforward chain; parallel execution shortens truly independent work through fan-out and fan-in; series–parallel combines controlled stages with concurrent work; and parallel–series coordinates multiple specialist pipelines. The hybrid names are valuable only when the architecture specifies precisely what they mean.

Engineering performance is governed by critical-path duration, queueing, synchronization and error handling—not by the nominal degree of parallelism. Reliability depends on structured handoffs, validated joins, bounded retries, source provenance, observability, and appropriately placed human approvals. The practical goal is a workflow that produces a **verifiably acceptable result** with reasonable latency and cost. The companion paper on stage-gate orchestration (Vol. 106, Issue 11) extends these principles with formal stage-gate loops, rework paths, acceptance criteria, and termination conditions.
"""
