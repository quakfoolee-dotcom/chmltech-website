"""Chmltech Online Journal, Vol. 106, Issue 1: Multi-Agent AI Orchestration Architectures (draft, Nov 14 2026).

Series: Multi-Agent AI Engineering, article 1. Figure 1 is interactive (content/journal/live/orch5.html); fig1-five-models.svg is its print and no-script version."""

SLUG = "multi-agent-ai-orchestration-architectures-five-coordination-models-compared"
META = dict(
    volume=106, issue=1,
    title="Multi-Agent AI Orchestration Architectures: Five Coordination Models Compared",
    short_title="Multi-Agent Orchestration: Five Models Compared",
    meta="How centralized, hierarchical, mesh, blackboard and contract-net orchestration compare for LLM agents, with a selection method, metrics and governance controls.",
    keywords=["multi-agent AI", "agent orchestration", "hierarchical agents", "decentralized mesh", "blackboard systems", "contract net", "task allocation", "agent governance"],
)
ABSTRACT = 'Choosing a multi-agent architecture is not simply a matter of adding more language-model agents. The architect must decide who owns a task, how work is assigned, where intermediate state is kept, which agents may communicate, and who is authorized to release the outcome. This paper compares five practical models (centralized orchestrator, hierarchical orchestration, decentralized mesh, shared blackboard, and market-based contract net) through their control paths, communication mechanisms, engineering trade-offs, and failure modes. A key distinction is that these labels describe different architectural dimensions: the first three principally describe control topology, whereas blackboard and contract net specify information sharing and task allocation mechanisms. Therefore, real deployments often combine them. The paper introduces a selection method, illustrative latency and coordination models, two advisory and engineering examples, and a deployment checklist. It makes no universal claim that distributed or bidding architectures are inherently more scalable or reliable; those properties must be demonstrated by workload-specific evaluation, persistence, access control, recovery, and governance.'

REFS = {
    'r1': ('Lee, Q. F. (2026). <em>Multi-Agent AI Systems: Architectures, Coordination Patterns and Failure Modes</em>. Chmltech Online Journal, Volume 104, Issue 2.',
           'https://www.chmltech.com/post/multi-agent-ai-systems-architectures-coordination-and-failure-modes.html'),
    'r2': ('OpenAI. (2026). <em>Agent orchestration — OpenAI Agents SDK</em>.',
           'https://openai.github.io/openai-agents-python/multi_agent/'),
    'r3': ('Anthropic. (2024). <em>Building effective agents</em>.',
           'https://www.anthropic.com/engineering/building-effective-agents'),
    'r4': ('Anthropic. (2025). <em>How we built our multi-agent research system</em>.',
           'https://www.anthropic.com/engineering/multi-agent-research-system'),
    'r5': ('Microsoft. (2026). <em>AI agent orchestration patterns — Azure Architecture Center</em>.',
           'https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns'),
    'r6': ('Amazon Web Services. (2026). <em>Use multi-agent collaboration with Amazon Bedrock Agents Classic</em>.',
           'https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html'),
    'r7': ('Google Developers. (2025). <em>Announcing the Agent2Agent protocol (A2A)</em>.',
           'https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/'),
    'r8': ('Nii, H. P. (1986). <em>The Blackboard Model of Problem Solving and the Evolution of Blackboard Architectures</em>. AI Magazine, 7(2), 38–53.',
           'https://doi.org/10.1609/aimag.v7i2.537'),
    'r9': ('NATS. (2026). <em>JetStream — concepts and delivery semantics</em>.',
           'https://docs.nats.io/concepts/jetstream'),
    'r10': ('Smith, R. G. (1980). <em>The Contract Net Protocol: High-Level Communication and Control in a Distributed Problem Solver</em>. IEEE Transactions on Computers, C-29(12), 1104–1113.',
           'https://cse-robotics.engr.tamu.edu/dshell/cs631/papers/smith80contract.pdf'),
    'r11': ('OWASP. (2025). <em>Top 10 for Large Language Model Applications: Prompt Injection and Excessive Agency</em>.',
           'https://genai.owasp.org/llm-top-10/'),
    'r12': ('Microsoft. (2026). <em>Microsoft Agent Framework — Workflow orchestrations</em>.',
           'https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/'),
    'r13': ('OpenAI. (2026). <em>Handoffs — OpenAI Agents SDK</em>.',
           'https://openai.github.io/openai-agents-python/handoffs/'),
    'r14': ('Hayes-Roth, B. (1985). <em>A blackboard architecture for control</em>. Artificial Intelligence, 26(3), 251–321.',
           'https://doi.org/10.1016/0004-3702(85)90063-3'),
    'r15': ('Microsoft. (2026). <em>Microsoft Agent Framework — Magentic orchestration</em>.',
           'https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/magentic/'),
}

BODY = r"""
## Introduction: Architecture Is a Control Decision

Modern agent platforms make it relatively easy to invoke several specialized agents for research, analysis, drafting, coding, validation, or action. The real engineering challenge begins when those agents must cooperate under latency, cost, security, and accuracy constraints. A weak design may duplicate research, lose evidence through repeated summaries, expose excessive tool permissions, or fail to terminate a debate. An elaborate topology is not automatically better than a capable single agent with a few tools.

An earlier paper in this journal, *Multi-Agent AI Systems: Architectures, Coordination Patterns and Failure Modes*, reviewed the foundational literature, empirical evidence, and broader failure taxonomy [@r1]. This companion paper narrows the focus to a practical question: **How should an engineer select and implement the orchestration and coordination model for a specific workload?** It follows the five approaches in Figure 1, then identifies the conditions under which each creates value and the controls necessary to make the design production-worthy.

The five labels are not a mutually exclusive set of software products. An orchestrator can assign tasks through a bidding mechanism; a hierarchy can publish artifacts to a shared blackboard; a mesh of agents can still require human approval for consequential actions. The chosen architecture should be expressed as an explicit combination of decisions, not inferred from a single marketing diagram.

## Five Models, Four Architectural Dimensions

Orchestration determines which actor runs next, what it may do, and how work transitions to a finished result. Four separate design questions are especially important (Table 1).

TABLE Four separable dimensions of a multi-agent architecture. || A production system may combine several choices from different rows.
| Dimension | Architectural question | Illustrative design choices |
| Control | Who can create, route, stop, or approve a task? | Lead orchestrator; nested supervisors; peer-to-peer agreements |
| Communication | How are instructions and results exchanged? | Star or tree messages; direct peer messages; publish–subscribe |
| Shared state | Where is the authoritative problem record? | Manager-owned ledger; isolated worker artifacts; versioned blackboard |
| Allocation | How is an available agent chosen for work? | Fixed ownership; rule-based routing; capability bidding and award |

FIG fig1-five-models || Five ways to coordinate LLM agents. The figure plays through each model in turn, showing how one task moves through it step by step; select a model to jump to it, or <em>Compare all</em> to see the five side by side and which architectural decision it settles. Centralized, hierarchical and mesh describe <em>control topology</em>; blackboard and contract net describe <em>information sharing</em> and <em>task allocation</em>, and can run inside any of the three. Properties are summarized from Tables 2 and 3; no model is rated high or low, because scalability and fault tolerance depend on how each is implemented. || Five small network diagrams side by side: a star with one orchestrator and three workers, a two-level tree of supervisors and agents, a fully connected mesh of four peers, four agents writing to a shared blackboard, and a manager announcing a task to three bidders, each labeled with its control style and chief hazard. || Drawn by the author from Sections 3 and 4.

Figure 1 places the five models side by side and steps through how a task moves in each. To avoid misleading comparisons, this paper treats **control location**, **state ownership**, **communication volume**, and **failure recovery** separately. This aligns with modern frameworks that distinguish manager-style delegation, agent-to-agent handoffs, deterministic workflow routing, concurrent execution, and adaptive planners [@r2, @r3, @r4, @r5, @r12].

## The Five Approaches in Engineering Detail

### 3.1 Centralized orchestrator: one accountable coordinator

A lead orchestrator receives the user's goal, decomposes it into subtasks, selects specialists, monitors the work, and produces or authorizes a synthesis. Worker agents generally return results to the lead rather than contacting one another directly. This creates a **star-shaped control path**, often with parallel worker execution. OpenAI documents manager-style agent-as-tool orchestration, and Anthropic reports an orchestrator–worker architecture for open-ended research [@r2, @r4].

**Advantages.** The architecture has an unambiguous owner for task completion, a clear location for validation, and straightforward routing and auditability. Worker contexts can remain narrow, reducing irrelevant instructions and limiting inadvertent information sharing. It is a strong starting point for SME advisory, regulated reporting, and research synthesis.

**Risks.** The lead can become a throughput bottleneck or an information-loss point if every result is condensed into its context. A mistaken decomposition can cause all specialists to work on the wrong objective. A failure of the lead process can strand work unless the task ledger, artifacts, and permissions are recoverable.

**Design controls.** Use typed task contracts, a durable work ledger, timeouts and retry budgets, artifact references rather than long transcript replays, independent quality checks, and a separately enforced authorization layer. A logical single leader need not be a physical single point of failure if control state is checkpointed and workers are idempotent.

### 3.2 Hierarchical orchestration: nested responsibility at scale

A hierarchy adds supervisors for work domains or organizational tiers. For example, a top-level program orchestrator can delegate a technical workstream to an Engineering Supervisor and a financial workstream to a Commercial Supervisor; each supervises its own specialist agents. Amazon Bedrock Agents Classic documents a supervisor-and-collaborator form, while Microsoft describes adaptive manager-based orchestration [@r5, @r15]. **Implementation status matters:** at the time of writing, Amazon states that Bedrock Agents Classic is not open to new customers, so it should not be assumed to be a current greenfield choice [@r6].

**Advantages.** Subdomain expertise, permissions, and budget limits can be localized. A manager can shield the upper tier from routine operational details. The model is useful when distinct teams require different validation rules or when a project naturally decomposes into separate accountable domains.

**Risks.** Each layer adds routing overhead, possibly another LLM call, and opportunities for context compression errors. Role ambiguity can produce conflicting orders; a deeply nested structure can hide the origin of unsupported claims.

**Design controls.** Set an explicit maximum delegation depth; assign one owner to each work package; preserve source artifacts across layers; require trace identifiers and structured summaries; and test both cross-domain disagreements and supervisor failures. Hierarchy should be justified by genuine domain boundaries, not by the mere size of an agent roster.

### 3.3 Decentralized mesh: direct peer coordination

In a mesh, authorized peers may send work or evidence directly to one another and coordinate through a common protocol. This differs from a manager retaining all control. Peer handoffs in the OpenAI SDK transfer active responsibility to another specialist, although handoff-based routing is **not necessarily a full mesh** [@r2, @r13]. At larger scale, interoperation standards such as the Agent2Agent (A2A) protocol address communication across agent implementations and vendors [@r7].

**Advantages.** Meshes can support locally informed decisions, dynamic routing, and heterogeneous specialists. They may suit distributed monitoring, agent-to-agent service collaboration, and environments where there is no natural central decision-maker.

**Risks.** Unrestricted peer communication causes high message volume, ambiguous ownership, circular delegation, contradictory state, and difficult provenance. A logical lack of central leader does **not** by itself guarantee availability: peers may still share a database, model API, identity provider, or network dependency.

**Design controls.** Enforce authenticated agent identity, capability discovery, message schemas, correlation IDs, bounded hop counts, global termination rules, conflict resolution, and a system of record. Where decisions have safety or commercial consequences, separate peer recommendations from authorized external actions.

### 3.4 Blackboard coordination: agents collaborate through shared state

A blackboard is a versioned workspace that contains hypotheses, facts, partial results, tasks, and evidence. Rather than sending every result directly to every peer, a specialist reads relevant state, contributes an artifact or update, and notifies other subscribers. The concept predates LLM agents: Nii's account of blackboard systems traces the architecture to Hearsay-II and the independent knowledge sources that cooperatively solved problems through a shared workspace [@r8]. Later work treated the control problem, deciding which knowledge source acts next, as a blackboard problem in its own right [@r14].

**Advantages.** A shared evidence ledger improves discoverability and avoids repeatedly copying the same source across messages. It can integrate heterogeneous agents whose execution order is opportunistic. This makes it suitable for long-running research, engineering design reviews, and multidisciplinary knowledge work.

**Risks.** The blackboard can become a shared failure and contamination point. Stale records, conflicting writes, poisoned evidence, weak provenance, and accidental cross-project disclosure can propagate rapidly. Publish–subscribe notifications do not automatically make the state consistent or durable; for example, NATS distinguishes transient Core NATS messaging from persisted JetStream delivery [@r9].

**Design controls.** Use versioned schemas, immutable evidence references, optimistic concurrency or locking where necessary, role-based write permissions, data classification, retention rules, event ordering, and retraction/correction procedures. Treat retrieved documents and peer notes as untrusted data until verified.

### 3.5 Market-based or contract-net allocation: agents bid for work

Contract-net coordination distributes tasks through an explicit negotiation: a manager or announcing agent advertises a work package; prospective contractors assess their capability and availability; one or more bids are evaluated; and the task is awarded. Reid G. Smith formalized this mechanism in the 1980 contract net protocol as a way to coordinate nodes in distributed problem solving [@r10].

**Advantages.** Bidding can be useful when agents differ in skill, tool access, cost, queue length, geographic location, or resource availability. It permits dynamic assignment instead of hard-coded ownership and may improve allocation under changing workloads—**if** the bids reflect meaningful performance and cost information.

**Risks.** The auction itself adds delay, messages, and decision rules. Self-reported cost and confidence may be unreliable; a bidder might accept work it cannot complete. Task awards can be duplicated or abandoned, while unconstrained bids can optimize price at the expense of quality and safety. A contract-net mechanism can still have a central announcer, so it is not automatically decentralized or fault-tolerant.

**Design controls.** Specify task requirements and objective bid fields; validate eligibility before comparing bids; use deadlines and reserve options; record award decisions; constrain budget and tool authority; and provide reassignment and dispute paths. Treat bidding as an **allocation protocol**, not as a guarantee of autonomous intelligence or resilience.

## Comparing Practical Trade-Offs

The summary below gives conditional engineering observations rather than universal rankings. The meaning of *high* scalability or fault tolerance depends on state management, fault isolation, workload shape, network architecture, and recovery procedures.

TABLE Classification by dominant engineering mechanism. || Blackboard and contract net can be combined with any of several control patterns.
| Pattern | Primary control | Communication and state | Most attractive condition | Chief operating hazard |
| Centralized orchestrator | One accountable lead | Star; worker artifacts returned to lead | Controlled delivery and source-based synthesis | Lead bottleneck; misdelegation |
| Hierarchical | Supervisors at several levels | Tree; tiered state and summaries | Several distinct domains or teams | Summary loss; management overhead |
| Decentralized mesh | Distributed peers and protocol | Direct messages; federated or shared state | Dynamic, heterogeneous peer collaboration | Cycles, conflicting owners, uncontrolled chatter |
| Blackboard | Separate scheduler or event-driven coordination | Shared versioned workspace | Knowledge-intensive collaboration | Stale or corrupted shared state |
| Contract net | Task announcer plus eligible bidders | Announce → bid → award → execute | Scarce or variable specialist resources | Auction overhead; poor bid signals |

The comparison in Table 2 summarizes these observations.

A **centralized orchestrator plus blackboard** is frequently more practical than a pure mesh: the orchestrator keeps final accountability while specialists write directly to a governed evidence store. A **hierarchical orchestrator plus contract-net allocation** can reserve bidding for an expensive specialist pool while retaining domain-specific approvals. These hybrids are often more precise descriptions than a single topology label; Figure 2 treats each axis as its own decision.

FIG fig2-decision-map || An architecture decision map. Control topology, information sharing, task allocation and workflow execution are independent decisions. The example hybrid combines a responsible supervisor, a versioned blackboard, selective capability bidding and bounded parallel work; it is an engineering illustration, not an industry standard. || Four horizontal bands, one per architectural axis (control topology, information exchange, task allocation, workflow scheduling), each listing its options, with arrows converging on an example hybrid design at the bottom. || Drawn by the author.

## A Practical Architecture Selection Method

Begin with the **single-agent baseline**. Use one agent plus tools and a deterministic workflow when tasks are short, role boundaries are artificial, source material is limited, or the output can be verified without multiple independent specialties. Anthropic recommends introducing complexity only when a simpler design falls short, and OpenAI's orchestration guidance explicitly distinguishes code-defined control flow from LLM-decided routing [@r2, @r3].

If multi-agent work is justified, apply the following gates:

1. **Accountability.** Is there one owner for the final deliverable and one authority for release? For regulated or advisory work, default to an explicit lead.
2. **Decomposition.** Are there genuinely distinct domains with different inputs, methods, or permissions? If yes, bounded specialists help; nested management is justified only where subdomains need their own coordination.
3. **State.** Do multiple specialists need to inspect and revise the same hypotheses, records, or calculation artifacts? If yes, add a governed blackboard rather than broadcasting full transcripts.
4. **Allocation.** Does specialist availability or cost vary enough to warrant bidding? If not, fixed routing is easier to test and operate.
5. **Concurrency.** Are tasks independent enough to run simultaneously? Prefer parallel execution for independent work and sequential or gated stages for dependent work.
6. **Consequence.** Can agents write records, spend money, send messages, or affect safety-related operations? Use independent enforcement and human approval where required, regardless of topology.

**Suggested default:** For a professional services or SME analysis workflow, start with **a single accountable orchestrator, two to four narrowly scoped specialists, a shared evidence repository, and an independent verification/release gate**. Add a hierarchy, mesh or bidding mechanism only after measurement demonstrates a need. This is a design recommendation, not an experimentally established optimum.

## Latency, Message Volume, and Reliability Models

Topology changes the *critical path* more reliably than it predicts intelligence. Consider three independent specialists with observed execution times of 8, 10, and 12 seconds, plus 3 seconds of planning and 4 seconds of synthesis. With no queueing, contention, retries, or rate-limit delay, a serial workflow would take approximately **37 seconds**, whereas parallel workers would finish in **19 seconds**. The improvement comes from overlapping independent tasks, not simply from having multiple agents.

EQ T<sub>serial</sub> ≈ T<sub>plan</sub> + Σ T<sub>worker,i</sub> + T<sub>synth</sub>

EQ T<sub>parallel</sub> ≈ T<sub>plan</sub> + max(T<sub>worker,i</sub>) + T<sub>synth</sub> + T<sub>coordination</sub>

Applying Eq. (1) and Eq. (2) to the three workers, with coordination time neglected, gives 3 + 8 + 10 + 12 + 4 = 37 seconds serial versus 3 + 12 + 4 = 19 seconds parallel. In real operation, total time may be longer due to tool quotas, network costs, wait-for-all joins, validation, and straggler handling.

Communication cost requires separate treatment. A fully connected **directed** mesh of *N* agents has up to *N(N − 1)* potential one-to-one communication links; the equivalent undirected count is *N(N − 1)/2*. This counts possible relationships, **not** the number of messages actually exchanged. A lead-to-worker star has *O(N)* direct relationships, but messages can still proliferate if the orchestrator repeatedly broadcasts instructions or gathers iterative responses. Publish–subscribe may reduce explicit point-to-point coupling while increasing event fan-out if topics are poorly scoped.

Reliability is not a topology label. If every required stage in a series must independently succeed with probability *p*, an idealized *k*-stage chain has success probability *p<sup>k</sup>*. Real agent errors are correlated; external verification, replay and retry alter the result. A system with a physically replicated coordinator and durable state may recover better than a nominally decentralized mesh that depends on one unavailable datastore. Architecture must be measured by **accepted-result rate, recovery time and controlled failure behavior**, not by the count of agent nodes.

## Governance and Failure Modes Across All Models

A useful architecture review asks how the system behaves when a member produces incorrect information, a tool times out, an external document contains adversarial instructions, or one agent refuses to yield control. Framework routing by itself is not a security boundary. OWASP flags prompt injection and excessive agency as major LLM application risks; those risks can propagate through peer messages or shared knowledge stores [@r11].

TABLE Typical failure modes and compensating engineering controls. || No row implies that the other patterns are immune.
| Failure scenario | Most exposed patterns | Required controls and recovery |
| Lead agent unavailable mid-task | Centralized, hierarchical | Durable checkpoints, leader failover, idempotent worker tasks |
| Early evidence distorted through summaries | Hierarchical, centralized | Direct artifact references, source traceability, independent reviewer |
| Circular handoffs and runaway messaging | Mesh, group coordination | Maximum hop/turn budget, owner ledger, stopping rules |
| Blackboard receives untrusted or stale content | Blackboard, hybrids | Provenance, content validation, access control, versions, rollback |
| False bid or contractor no-show | Contract net | Eligibility checks, auditable scoring, timeouts, re-award |
| Unauthorized side effect | All models | Least privilege, policy engine, human approval, action audit |

Table 3 lists the failure scenarios a review should rehearse and the controls that contain them.

In particular, **the decision to perform a tool action must be separated from the authority to perform it**. For instance, an agent may recommend sending a supplier request, but an application-level policy and approval gate should determine whether any email is actually sent. Likewise, a design-review agent may recommend a process setpoint change, but should not have permission to modify control equipment. A trustworthy multi-agent harness maintains access rules, stable identity, telemetry, budgets, state transition controls, and recoverable side-effect records regardless of the communication graph.

## Two Worked Architecture Examples

### 8.1 SME ERP/WMS vendor selection: controlled research and comparison

Consider a hypothetical wholesale distributor selecting an inventory and warehouse management system. The project involves requirements discovery, vendor research, integration analysis, total-cost-of-ownership estimates, and a final recommendation. Evidence and approval are more important than unconstrained agent-to-agent negotiation.

**Recommended hybrid:** a centralized project orchestrator owns task definitions and the client-facing result; Research, Integration, Financial Analysis, and Risk Review agents operate on bounded subtasks; and a **versioned evidence blackboard** holds vendor claims, source links, assumptions, and evaluation tables. Independent vendor checks can run in parallel, but final scoring follows a deterministic rubric. A Review Agent verifies material claims, and a human consultant approves release. Contract-net bidding would add little if the four roles and resource pool are stable.

**Testable acceptance criteria** include complete source links for material vendor claims, a reconciled three-year cost table, explicit integration unknowns, and a final shortlist that does not silently convert an undocumented claim into an endorsed capability. This illustrates why central accountability and shared evidence often coexist.

### 8.2 Process-engineering feasibility review: specialists with release gates

For a hypothetical process plant feasibility study, assign specialists to mass and energy balances, equipment sizing, process-safety review, and cost assumptions. An Engineering Supervisor owns engineering consistency; a Commercial Supervisor handles cost estimation; both report to a Program Orchestrator. Shared artifacts are tagged with units, versions, calculation basis, and evidence status.

This is **hierarchical control with shared-state coordination**, not simply a tree of chat messages. A safety reviewer can flag a disputed temperature or materials constraint, but the final decision must pass a documented engineering approval gate. Unknown thermophysical data and unsupported vendor ratings remain open issues. No agent is authorized to alter plant operations. A mesh could be useful for communicating observations among monitoring agents, but is not necessary for approving a design basis.

Both examples are **illustrative architecture scenarios**, not descriptions of deployed client systems or measured case-study outcomes.

## Implementation Blueprint: From Diagram to Governed System

A diagram becomes an operating architecture only when its runtime contract is explicit. Recommended minimum artifacts are: a role-and-permission registry; a task schema; a routing policy; a versioned artifact/evidence store; a workflow-state ledger; an approval matrix; evaluation datasets; and logs that connect every action to the initiating request.

Table 5 sets out the control loop of a governed orchestrator as language-independent steps, not as an executable library interface.

TABLE Control loop of a governed orchestrator. || Step 3 uses a fixed route or a validated bid; the loop is the same for both.
| Step | Orchestrator action | Control enforced |
| 1. Receive | Check the requester's authorization | Identity and access policy |
| 2. Plan | Create a bounded plan; assign an owner and a budget to every task | Delegation depth and budget limits |
| 3. Assign | Choose a specialist for each runnable task | Routing policy; bid eligibility |
| 4. Execute | Run each task with a timeout and save the result as a versioned artifact | Timeouts; artifact store |
| 5. Verify | Check each result against its task contract and provenance | Schema and evidence checks |
| 6. Synthesize | Combine only verified artifacts into a candidate result | Source traceability |
| 7. Gate | An independent quality gate returns pass, revise or stop | Independent reviewer |
| 8. Release or escalate | Return rework to its owner while retry budget remains; publish only if release is authorized; otherwise stop and escalate with a trace | Retry budget; release authority; audit trail |

To move toward production, run a four-step pilot. **First**, measure a single-agent baseline against representative real tasks. **Second**, implement centralized routing with one or two true specialist boundaries and compare accepted-result quality. **Third**, add blackboard state, concurrency, or hierarchy only for demonstrated bottlenecks. **Fourth**, inject failures—timeouts, missing vendor data, contradictory evidence, duplicate messages, and malicious instructions—before enabling any high-impact external actions.

Each task needs a contract, and each coordination mechanism adds fields to it (Table 6). These fields are **proposed engineering controls**, not universal schemas imposed by a particular framework.

TABLE Proposed task contract fields. || Field names are illustrative.
| Contract | Fields |
| Every task | task ID, owner, input artifact IDs, expected output schema, allowed tools, deadline, maximum retries, evidence requirements, release status |
| Added for contract net | bid ID, capability evidence, estimated cost, estimated duration, award decision, expiry |
| Added for a blackboard | artifact version, origin, integrity check, access policy, supersedes reference |

## Evaluation: Decide with Data, Not Architecture Labels

Before declaring a topology better, evaluate it against the same task set, datasets, quality rubrics, model configuration, and external-tool conditions. Include difficult and adversarial tasks; report failed, escalated, and partially completed runs rather than suppressing them. Anthropic's production research account emphasizes end-state evaluation, robust prompt and tool design, and operational discipline [@r4].

TABLE Recommended evaluation measures. || Priorities and thresholds should reflect business criticality and failure consequences.
| Metric | Operational definition | Decision relevance |
| Accepted-result rate | Results passing required evidence and quality gates / attempted tasks | Most important outcome measure |
| End-to-end latency | Request to authorized, completed delivery, including queueing and review | Customer experience and SLA |
| Total run cost | Model, tools, infrastructure, reviewer time and retries | Economic viability |
| Coordination overhead | Agent messages, LLM turns and duplicate work per accepted result | Detects unnecessary complexity |
| Recovery success | Fault-injection cases completed without duplicate side effects / recovery attempts | Operational resilience |
| Traceability and permission compliance | Verified material claims and correctly authorized actions / sampled items | Auditability and safety |

Table 4 defines the measures; each is a ratio or total over the same task set.

Compare cost and quality jointly. A faster workflow that produces an unverified recommendation may be worse than a slower one that passes evidence and approval gates. A market-based scheduler that finds a cheaper worker is not beneficial if bidding overhead or rework costs exceed the savings. A blackboard that enables strong team collaboration still requires ownership, correction, and retention policies. Architecture selection is therefore an **empirical systems-engineering decision** with an explicit operating envelope.

## Conclusion and Engineering Checklist

The five-model framework is useful because it exposes different ways agents can cooperate, but the models operate on overlapping design axes. **Centralized orchestration** emphasizes accountability; **hierarchy** organizes multiple domains; **mesh** enables peer communication; **blackboard** coordinates through shared state; and **contract net** negotiates task allocation. None independently ensures intelligence, scalability, reliability, or safe autonomy.

For most early enterprise and SME deployments, begin with the smallest architecture that provides measurable value: a responsible lead, constrained specialists, a durable evidence store, and a real verification/release gate. Introduce decentralized routing, deeper hierarchy, or bids only when workload testing demonstrates their benefit. Prefer interoperable and inspectable artifacts to long, unstructured conversational handoffs. Keep permissions, replay, provenance, observability, and human oversight outside the discretion of individual agents.

**Pre-release checklist:** (1) responsibility and stop conditions documented; (2) task schemas and artifact provenance validated; (3) state and external side effects recoverable; (4) agent identities and tool permissions least-privileged; (5) bounded retries and conflict rules tested; (6) quality metrics compared with a single-agent baseline; and (7) all high-consequence external actions gated by appropriate authorization. These controls matter more than the number of boxes in an architecture diagram.
"""
