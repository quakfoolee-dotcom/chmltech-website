"""Chmltech Online Journal, Vol. 106, Issue 12 (Multi-Agent AI Engineering series, Article 4). Figure 1 is interactive (live/mae4.html)."""

SLUG = 'agents-skills-and-harnesses-a-reference-architecture-for-reliable-agentic-ai'
META = dict(
    volume=106,
    issue=12,
    title='Agents, Skills, and Harnesses: A Reference Architecture for Reliable Agentic AI',
    short_title='Agents, Skills and Harnesses: A Reference Architecture',
    meta='What an AI agent decides, what a skill packages, what tools do and what the harness enforces: a reference architecture with controls, metrics and an SME example.',
    keywords=['agentic AI', 'AI agents', 'agent skills', 'agent harness', 'reference architecture', 'tool governance', 'multi-agent systems', 'LLM applications'],
)
ABSTRACT = 'Agentic AI systems are often described as a collection of agents equipped with tools. This description is incomplete for engineering purposes. An agent supplies goal-directed reasoning and task-level decisions; a skill packages reusable procedural knowledge and, optionally, scripts and supporting resources; a harness supplies the runtime and control mechanisms that allow agents to execute work under defined constraints. The three concepts overlap in vendor terminology, yet treating them as separate design responsibilities makes multi-agent systems easier to test, secure, maintain and scale. This paper develops a practical reference architecture, distinguishes skills from ordinary tools, and describes the control path from a user request through agent reasoning, skill selection, tool execution, validation and human approval. A hypothetical warehouse-management-system (WMS) selection project demonstrates the boundaries in an SME advisory workflow. The article concludes with an engineering checklist, evaluation metrics and common failure modes. The proposed architecture is a Chmltech synthesis of publicly documented techniques, not a claimed universal industry standard.'

REFS = {
    'r1': ('OpenAI. (2026). <em>OpenAI Agents SDK: Agents</em>.',
           'https://openai.github.io/openai-agents-python/agents/'),
    'r2': ('OpenAI. (2026). <em>OpenAI Agents SDK: Agent orchestration</em>.',
           'https://openai.github.io/openai-agents-python/multi_agent/'),
    'r3': ('Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., &amp; Cao, Y. (2023). <em>ReAct: Synergizing reasoning and acting in language models</em>. ICLR.',
           'https://arxiv.org/abs/2210.03629'),
    'r4': ('Anthropic. (2026). <em>Agent Skills: Overview</em>.',
           'https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview'),
    'r5': ('OpenAI. (2026). <em>Skills — API documentation</em>.',
           'https://developers.openai.com/api/docs/guides/tools-skills'),
    'r6': ('OpenAI. (2026). <em>Agents API: Architecture</em>.',
           'https://developers.openai.com/api/docs/guides/agents-api/architecture'),
    'r7': ('Lopopolo, R. (2026, February 11). <em>Harness engineering: Leveraging Codex in an agent-first world</em>. OpenAI.',
           'https://openai.com/index/harness-engineering/'),
    'r8': ('Kundel, D., &amp; Chua, G. (2026, January 22). <em>Testing Agent Skills systematically with evals</em>. OpenAI Developers.',
           'https://developers.openai.com/blog/eval-skills'),
    'r9': ('OpenAI. (2026). <em>OpenAI Agents SDK: Tracing</em>.',
           'https://openai.github.io/openai-agents-python/tracing/'),
    'r10': ('OpenAI. (2026). <em>OpenAI Agents SDK: Human-in-the-loop</em>.',
           'https://openai.github.io/openai-agents-python/human_in_the_loop/'),
    'r11': ('OWASP Foundation. (2025). <em>OWASP Top 10 for LLM Applications 2025</em>.',
           'https://genai.owasp.org/llm-top-10/'),
    'r12': ('Lee, Q. F. (2026, November 9). <em>Multi-Agent AI Systems: Architectures, Coordination Patterns and Failure Modes</em>. Chmltech Online Journal.',
           'https://www.chmltech.com/post/multi-agent-ai-systems-architectures-coordination-and-failure-modes.html'),
    'r13': ('Lee, Q. F. (2026, November 9). <em>AI Operating Systems: A Reference Architecture and Governance Model for Enterprise AI</em>. Chmltech Online Journal.',
           'https://www.chmltech.com/post/ai-operating-systems-architecture-and-governance-for-enterprise-ai.html'),
    'r14': ('Autio, C., Schwartz, R., Dunietz, J., Jain, S., Stanley, M., Tabassi, E., Hall, P., &amp; Roberts, K. (2024). <em>Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)</em>. NIST.',
           'https://doi.org/10.6028/NIST.AI.600-1'),
    'a1': ('Lee, Q. F. (2026). Multi-agent AI orchestration architectures: Five coordination models compared. <em>Chmltech Online Journal</em>, 106(1).',
           'https://www.chmltech.com/post/multi-agent-ai-orchestration-architectures-five-coordination-models-compared'),
}

BODY = r"""
## Introduction

Building a useful demonstration of an AI agent can require little more than a language model, instructions and access to a search or coding tool. Building a dependable production system is a different problem. An enterprise workflow must preserve the boundary between what an AI component may **decide**, what a reusable capability is designed to **perform**, and what the surrounding system must **authorize, monitor and recover**. When these responsibilities are blurred, teams struggle to determine whether a failure originated in a prompt, a tool integration, a workflow transition or the runtime itself.

The distinction matters particularly in multi-agent systems. A researcher may gather evidence, an analyst may calculate trade-offs, and a reviewer may test the draft. Each agent can invoke shared skills and tools, but none should receive unrestricted access merely because its role sounds specialized. The application must still specify delegation, data access, evaluation, interruption and termination. Contemporary agent frameworks provide many of these controls, but they package them differently [@r1, @r2], and most build on the interleaved reasoning-and-acting loop popularized by ReAct [@r3].

This paper uses **agent**, **skill** and **harness** as engineering concepts rather than product names. Section 2 defines them; Section 3 presents their architectural relationship; Sections 4–7 explain execution and implementation; Section 8 provides a worked example; Sections 9–10 treat metrics and failure modes; and Section 11 concludes. It extends earlier papers in this journal on multi-agent coordination and enterprise AI operating systems [@r12, @r13].

## Three Concepts, Three Engineering Responsibilities

### 2.1 Agent: the decision-making actor

An **agent** is an AI-driven component configured to pursue a goal within a bounded task environment. In common LLM implementations, it combines a model with role instructions, available tools, context and optional handoff or output constraints. The agent interprets observations, selects next steps, calls permitted capabilities and produces an answer or structured artifact. The OpenAI Agents SDK, for example, defines agents in terms of an LLM configured with instructions, tools and optional runtime behavior [@r1].

An agent need not be persistent, self-improving or fully autonomous. Some agents live for a single request; others retain state through a session or external memory. A model does **not** learn new weights merely because an agent receives feedback. Retained knowledge and genuine model learning are separate design choices. A planning agent, research agent and review agent may even share the same underlying model; the role boundaries arise from configuration and workflow, not necessarily from different neural networks.

### 2.2 Skill: a reusable procedure or capability package

A **skill** is a reusable, discoverable package that describes how to carry out a class of tasks. In modern agent platforms, skills commonly include metadata, instructions and optional scripts, templates, examples or reference files. The agent or harness can load the relevant package on demand. Anthropic describes Agent Skills as modular resources with staged, or *progressive*, loading; OpenAI documents discoverable SKILL.md directories in agent environments [@r4, @r5].

A skill is **not synonymous with a tool**. A tool is typically a callable operation—such as executing SQL, retrieving a URL, generating a chart or writing a document. A skill may teach an agent *when and how* to combine several tools, apply domain rules and validate an output. Some platforms use “skill” more loosely to describe individual capabilities; engineering specifications should therefore state the actual contract rather than rely on the label.

For example, an *Evaluate WMS Vendors* skill could carry a scoring rubric, source-quality rules, output template and verification steps. It may invoke search, spreadsheet, arithmetic and document-generation tools. The skill defines repeatable procedure; the tool performs a concrete operation.

### 2.3 Harness: the execution and control system

A **harness** is the supporting structure around the model that makes agent execution possible and governed. Depending on the platform, it can encompass the model-and-tool loop, session and context management, routing, state persistence, environment isolation, retries, validation, human approvals, traces and budgets. Recent platform documentation explicitly separates the harness from the environment in which code and files are operated on [@r6], while OpenAI's harness-engineering discussion emphasizes the importance of legible environments, feedback loops and architectural constraints [@r7].

**Orchestration is one responsibility of a harness, not its entire definition.** Orchestration determines which agent runs next and how results move between stages. The harness also determines whether a tool call is allowed, how a failure is recorded, whether an interruption can be resumed and when a run must stop. The precise boundaries vary: some systems place part of this responsibility in a workflow engine, sandbox, API gateway or external governance service.

### 2.4 A useful fourth concept: tools and resources

Tools, APIs, databases and documents are resources that agents use through authorized interfaces. They are not themselves agents. Tools may be embedded in skills, exposed directly to agents or mediated through a runtime broker. This additional category prevents the misleading three-way simplification that “skills execute everything”: in practice, execution may occur in a program, external service or sandbox, under harness-enforced permissions.

## Reference Architecture: How the Pieces Fit Together

Figure 1 shows the recommended separation of a *decision plane*, a *capability plane* and a *control plane*, and follows one request through it. The agent decides what work is needed; the skill offers a reusable method; tools operate on resources; and the harness mediates each transition. The figure's side-by-side view compares the four concepts by purpose, state, owner and main risk. Three stricter engineering distinctions apply throughout: agents are not necessarily long-lived; skills may be procedural packages rather than individual tools; and harnesses are not limited to orchestration.

FIG fig1-roles || Agents, skills, tools and the harness in one run. The figure plays through each concept in turn, following a WMS vendor-assessment request: the harness admits and routes it, agents decide, skills supply methods, tools act on resources, and every transition returns through the harness; select a concept to jump to it, or <em>All four</em> to compare them side by side. Conceptual reference architecture, not a single vendor's implementation. || A layered diagram: a request enters a harness control plane at the top; below it three agents (research, analysis, reviewer), then three skills (evidence rules, scoring method, QA checklist), then three tools (retrieval, calculation, document store), with an approver beside the harness. || 

TABLE Functional separation proposed for engineering design. || These categories are conceptual; a software framework may combine them inside one product.
| Dimension | Agent | Skill | Harness |
| Core question | What should happen next? | How is this kind of task performed? | Under what conditions may execution proceed? |
| Main function | Goal-directed reasoning, delegation, synthesis | Repeatable guidance, workflow and optional scripts | Runtime coordination, constraints and operational recovery |
| Typical inputs | Goal, context, observations | Task arguments, referenced data, domain rules | Requests, policies, identities, events, state |
| Typical outputs | Decisions, actions, drafts, judgments | Validated result or procedure-specific artifact | Controlled execution record and final run state |
| State | Ephemeral or persisted by design | Often versioned instructions; sometimes execution state | Session, checkpoints, logs and policy state |
| Primary risk | Hallucinated reasoning or incorrect delegation | Bad instructions, unsafe scripts or stale procedures | Permission bypass, failed recovery or missing audit trail |
| Evaluation | Task accuracy, decision quality | Trigger accuracy, validity and reproducibility | Reliability, authorization, tracing and recovery |

Table 1 sets out the functional separation in more detail. The three concepts are **complementary, not interchangeable**. A skill can improve consistency without becoming an independent actor. An agent can perform work without a separate skill package. A harness can execute a single agent or a fleet of agents; it remains important even when no inter-agent communication is needed.

## The End-to-End Execution Path

A reliable workflow has an explicit sequence of control decisions, even when agent work itself runs in parallel. A practical path is:

1. **Intake and policy check.** Authenticate the requester, classify the task, validate inputs and establish the data-access scope and execution budget.
2. **Task planning.** The orchestrating agent, or deterministic workflow code, decomposes the request into bounded tasks and selects agent roles.
3. **Skill discovery.** The runtime exposes skills relevant to the task. The selected agent reads skill instructions only as needed, avoiding unnecessary context expansion [@r4, @r5].
4. **Execution through authorized tools.** A skill's procedure may direct search, calculation, file operations or database queries. The harness enforces tool allowlists, identity context, input validation and execution limits.
5. **Result validation and handoff.** Intermediate artifacts are checked against schema and evidence requirements before the next agent consumes them.
6. **Quality gate and human intervention.** A reviewer or deterministic validator checks completeness and safety. Sensitive external writes or publication actions can be suspended for human approval [@r10].
7. **Delivery, persistence and feedback.** The final artifact is released with provenance. Approved lessons can update a knowledge base or future skill version; feedback is not presumed to update model weights.

The approach supports sequential workflows, parallel research, series–parallel designs and stage-gate loops. Frameworks support both model-driven orchestration, through agents as tools and handoffs, and code-driven orchestration, through chaining and parallel runs [@r2]; in either case the order of work changes, but authorization and validation must still be applied at every stage. A well-designed harness separates **control flow** from **content generated by agents**: an instruction hidden in an untrusted web page should not be able to rewrite the system's permission policy.

## Engineering Agents: Roles, Context and Boundaries

Agent design begins with a narrow statement of responsibility. For example, a Research Agent locates evidence and records provenance; an Analysis Agent evaluates structured inputs; a Reviewer Agent challenges claims against criteria. Naming agents is insufficient. Each should also have an **input contract**, **output schema**, permitted skills, permitted tools, context policy and escalation path.

Role-specific prompts should explain what counts as success, when to stop and which uncertainties must be surfaced. For the Research Agent, a useful output is not merely a paragraph of prose but a set of claims linked to primary sources, publication dates and confidence notes. For an Analysis Agent, calculations should expose assumptions and units; for a Reviewer, an approval verdict must be connected to testable acceptance criteria. Structured handoffs reduce information loss and limit the spread of unsupported assertions.

A multi-agent architecture is not automatically better than a strong single agent. Additional actors create coordination cost, more intermediate data and new ways for errors to propagate. A separate agent is justified when the task benefits from specialist context, different permissions, independent evidence gathering or an independent verification responsibility. Otherwise, a single agent using well-designed skills and tools may be simpler and more reliable [@r12].

## Engineering Skills: Reusability Without Hidden Complexity

A production skill should behave like a versioned engineering procedure. Its specification should declare: **name and purpose; triggering conditions; prerequisites; approved data sources; input/output contracts; allowed tools; validation rules; known limitations; ownership; and version**. Where skills contain scripts, the scripts must be inspected, dependency-pinned where practicable, and tested within an appropriate execution environment.

Skill discovery quality matters. A description that is too broad can trigger the wrong procedure; a description that is too narrow can leave a relevant skill unused. Skills should state clearly what they do and when to use them, include concrete usage examples, and rely on progressive loading so that detailed instructions enter context only when needed [@r4]; examples of invalid invocation are a further useful addition. Reusable templates, terminology and structured outputs are often more valuable than making a skill elaborate.

A good skill test suite should cover **activation**, **execution**, **output quality** and **non-regression**. For a vendor-comparison skill, this means checking whether it is selected for the right requests; whether it processes required inputs; whether source links, scoring weights and calculations survive execution; and whether a new version performs at least as well on representative cases. OpenAI's guidance on skill evaluation recommends systematic, repeatable evaluation rather than judging a changed skill by impression [@r8].

Separating skills from agents has an operational benefit: one validated *Source Verification* skill can support a research agent, a reviewer and a report-writing agent without duplicating its procedure in three prompts. It also creates a governance obligation: because multiple agents may depend on that shared skill, a change needs versioning, ownership and regression testing.

## Harness Engineering: Reliability Is a Runtime Property

The harness is where architectural intentions become enforceable behavior. Its responsibilities can be grouped into the six engineering control areas of Table 2.

TABLE A proposed minimum harness-control checklist for production systems. || 
| Control area | Required capability | Practical evidence |
| Execution control | Routing, dependencies, timeouts, retries and termination | Workflow trace with stage transitions |
| Security and identity | Tool authorization, scoped credentials, sandboxing | Denied-action and access-control test records |
| State and recovery | Checkpointing, resumable runs, idempotent actions | Successful restart after interruption |
| Quality gates | Schema checks, factual checks, approval requirements | Rejected and accepted test cases |
| Observability | Events, tool traces, model usage, failure taxonomy | End-to-end run trace and dashboards |
| Cost discipline | Token limits, concurrency, tool budgets, stop conditions | Cost per accepted task and latency distribution |

These controls should not exist only in a model's natural-language instructions. Permission enforcement belongs in executable services and properly scoped credentials. Approval for an external action should be verified by the runtime, not inferred from the agent's claim that approval was obtained. OpenAI's Agents SDK describes explicit human-in-the-loop interruptions for sensitive tool calls, while its tracing support records model generations, tools, guardrails and handoffs [@r9, @r10].

Reliability also requires **failure containment**. Suppose a research tool times out: the harness should retry according to a bounded policy or return a visible partial state; it should not quietly invent a result. If a model produces malformed JSON, the validator should reject it or request a limited repair. If the reviewer rejects a draft twice, a stage-gate workflow should escalate or terminate rather than enter an unbounded loop.

Finally, harness behavior affects how agent performance is measured. A model backed by good retrieval, tools, checkpoints and validators may appear substantially more capable than the same model in a weak setup. Because agent reliability depends on the environment, feedback loops and constraints around the model [@r7], evaluations should record the harness configuration, not only the model name. A comparison between two models run under different harnesses, or between two harness versions run with different models, says little about either component on its own; change one at a time and keep the evaluation set fixed.

## Worked Example: An SME WMS Selection Advisory Workflow

Consider a **hypothetical Vancouver SME** preparing to replace spreadsheet-based warehouse processes with a warehouse management system. The organization requests a shortlist of three vendors, an integration assessment and a costed recommendation. The example is illustrative, not a report about a named client.

**Agent design.** A Research Agent searches approved vendor documentation and records feature evidence. An Analysis Agent evaluates requirements, integrations and cost assumptions. A Reviewer Agent checks source quality, arithmetic, omissions and unsupported claims. The orchestrator assigns tasks, reconciles conflicting findings and prepares the final output.

**Shared skills.** A *Requirements Extraction* skill transforms notes into a controlled requirements matrix. A *Vendor Evidence Check* skill requires vendor-primary citations and dates. A *Weighted Scoring* skill applies approved criteria and displays scoring sensitivity. A *Report Assembly* skill produces a consistent deliverable. Each skill can use narrow tools—document parsing, web retrieval, spreadsheet calculation or report rendering—without receiving independent access to customer systems.

**Harness controls.** The runtime restricts access to the client's project workspace, separates research from external write permissions, records provenance for each scored feature and validates totals before publication. It pauses before sending the final recommendation externally. A reviewer gate rejects any mandatory requirement marked “met” without supporting evidence. When source material is missing, the system outputs “not verified” rather than filling a gap from general model knowledge.

**Execution pattern.** Requirements extraction runs first. Vendor research can proceed in parallel for several providers. Analysis follows once the evidence set is complete; the reviewer applies a stage-gate check. A rejection returns only the deficient items for revision, with a maximum retry count. The orchestrator then issues an approved final comparison and records lessons for the next project.

The same structure also makes failures diagnosable. If a vendor is scored on a feature its documentation does not mention, the trace shows whether the Research Agent misread a source, the *Vendor Evidence Check* skill failed to require a citation, or the harness let an unvalidated artifact through the reviewer gate. Each answer points to a different owner and a different fix.

This example shows why the layers should remain distinct. The agents contribute specialized judgments; the skills standardize methods; and the harness defines data access, dependencies, checkpoints, audit and release. More agents would add value only if the increased coverage or independence justified their extra cost and coordination complexity.

## How to Measure a Well-Engineered System

A practical evaluation set should include **task success**, **first-pass acceptance**, **evidence completeness**, **unauthorized action rate**, **end-to-end latency**, **cost per accepted task**, **recovery success** and **human intervention rate**. Not every metric is relevant to every application; organizations should select thresholds that reflect task risk and operating economics.

Let *C*<sub>run</sub> be the average cost per attempted run and *p*<sub>accept</sub> the proportion of runs accepted under a specified evaluation rubric. A simple estimate of the expected cost per accepted result is Eq. (1):

TEX C_{\text{accepted}} = \frac{C_{\text{run}}}{p_{\text{accept}}}

Eq. (1) assumes each attempt has approximately the same cost and that retry policies do not materially change the distribution. For an **illustrative, not measured** scenario, $1.20 per run at an 80% acceptance rate produces $1.50 per accepted result. A revised harness costing $1.35 per run at 95% acceptance produces about $1.42 per accepted result. Higher per-run expenditure can therefore coexist with lower cost for usable output.

Parallelism similarly requires end-to-end accounting. Because independent agents can run in parallel [@r2], the critical-path latency for two independent research tasks is approximately planning time plus the **longer** of the two research times, followed by review and synthesis—not the sum of both research times. This approximation breaks when shared API limits, serial dependencies or contention dominate. Evaluate with measured latency percentiles rather than architecture diagrams alone.

Quality should be verified against evidence outside the generating agent. Agreement between two agents using the same model or sources is not proof of correctness. For consequential decisions, validators need independent tests, primary-source checks or human review. An agent that reports its own success without a separate acceptance check creates an unreliable metric.

## Failure Modes and Security Boundaries

TABLE Representative failures and the layer best positioned to mitigate them. || 
| Failure mode | Likely layer | Engineering response |
| Unsupported facts or wrong delegation | Agent | Structured evidence, narrow role, independent review |
| Wrong skill activation | Skill discovery | Better descriptions, negative examples, activation evals |
| Outdated procedure or compromised script | Skill package | Versioning, code review, provenance and sandboxing |
| Prompt injection through retrieved text | Agent/tool boundary | Treat external content as data; restrict authority of tool output |
| Excessive tool privileges | Harness/identity | Least privilege, credential scoping, approvals and audit |
| Duplicate external action after retry | Harness/workflow | Idempotency keys, checkpointing, side-effect controls |
| Infinite review loop | Orchestration | Retry budgets, escalation and explicit stop conditions |
| Silent context contamination | Memory and shared state | Source provenance, access control, retention and review |

Table 3 assigns representative failures to the layer best placed to mitigate them. The OWASP Top 10 for LLM Applications identifies prompt injection and excessive agency among its major risk categories [@r11]. In multi-agent systems, those risks can cross agent boundaries when one agent consumes untrusted material generated or retrieved by another. The harness should limit the consequences of such mistakes through permissions, validation and supervised actions rather than presume that perfect prompting will prevent them.

Governance should follow a risk-based lifecycle. The NIST Generative AI Profile organizes suggested actions around Govern, Map, Measure and Manage [@r14]. In engineering terms, these functions map to defining ownership and policy, identifying task and data risks, measuring outcomes and failure modes, and controlling operation and improvement. Compliance claims require assessment against applicable requirements; the existence of a harness alone is not evidence of compliance.

## Practical Implementation Checklist and Conclusion

Before a pilot moves into production, the engineering team should be able to answer the following questions:

- **Agents:** Are roles bounded? Are inputs, outputs, permitted capabilities and escalation routes documented? Is there a credible single-agent baseline?
- **Skills:** Are procedures versioned, discoverable, testable and reusable? Do they distinguish instructions from executable tools and privileged actions?
- **Harness:** Can the runtime enforce permissions, log important events, resume or terminate interrupted work, reject bad outputs and obtain human approval for sensitive actions?
- **Evidence:** Does the evaluation measure accepted outcomes and failure modes across repeated cases, not just attractive demonstrations?
- **Ownership:** Is somebody accountable for each agent, skill, integration, policy and shared memory store?

The central design principle is simple: **agents decide within bounded goals; skills package reusable methods; tools perform operations; the harness governs and records execution.** These responsibilities can be implemented by different products, by one integrated framework or through custom code. The architecture matters more than the labels. Engineering discipline—explicit contracts, least privilege, validated handoffs, bounded iteration, observability and measurable acceptance—turns a promising agent demonstration into a maintainable business system.

Companion papers in this series examine orchestration architectures [@a1], execution patterns (Vol. 106, Issue 10), stage-gate control (Issue 11), harness engineering (Issue 13) and skills engineering (Issue 14) in greater depth. For an enterprise-wide view, the earlier paper on AI operating systems treats common data, identity, governance and cost layers around these components [@r13].
"""
