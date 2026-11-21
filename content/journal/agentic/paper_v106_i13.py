"""Chmltech Online Journal, Vol. 106, Issue 13 (Multi-Agent AI Engineering series, Article 5). Figure 3 is interactive (live/mae5.html)."""

SLUG = 'harness-engineering-designing-validating-and-operating-reliable-multi-agent-ai-systems'
META = dict(
    volume=106,
    issue=13,
    title='Harness Engineering: Designing, Validating, and Operating Reliable Multi-Agent AI Systems',
    short_title='Harness Engineering for Multi-Agent AI Systems',
    meta='A seven-stage harness engineering lifecycle for multi-agent AI: control, execution and evidence boundaries, action state machines, tests, release gates and operations.',
    keywords=['agent harness', 'harness engineering', 'multi-agent AI', 'workflow runtime', 'tool governance', 'human-in-the-loop', 'observability', 'AI risk management'],
)
ABSTRACT = 'Multi-agent AI systems can divide complex work among planners, researchers, analysts, reviewers, and tool-using executors. Yet a collection of capable agents is not a dependable application. Reliable performance depends on a harness: the runtime and engineering controls that supply context, schedule and resume work, broker tool access, validate outputs, enforce authorization, and record what actually occurred. This paper develops a seven-stage Harness Engineering lifecycle—Define & Discover, Design & Architect, Build & Integrate, Test & Validate, Deploy & Release, Operate & Monitor, and Improve & Evolve—as a proposed Chmltech method for developing and governing such systems. It distinguishes the harness from models, agents, skills, orchestration graphs, and enterprise policy; proposes a reference architecture with separate control, execution, and evidence boundaries; and specifies state transitions, risk controls, test suites, observability, release gates, and operational metrics. An explicitly hypothetical small-business warehouse-management-system (WMS) evaluation illustrates controlled agent delegation, evidence verification, staged approval, and safe external communications. The key engineering principle is that agent-generated decisions do not constitute operational authorization: safety-critical transitions and external side effects require independently enforced policy, validated state, and, when needed, accountable human approval. This paper is a practical architecture proposal informed by contemporary framework guidance, not a claim of certified compliance or measured field performance.'

REFS = {
    'r1': ('Lee, Q. F. (2026, November 9). Multi-agent AI systems: Architectures, coordination patterns and failure modes. <em>Chmltech Online Journal</em>, 104(2).',
           'https://www.chmltech.com/post/multi-agent-ai-systems-architectures-coordination-and-failure-modes.html'),
    'r2': ('Microsoft. (n.d.). <em>Agent Harness.</em> Microsoft Agent Framework documentation.',
           'https://learn.microsoft.com/agent-framework/agents/harness'),
    'r3': ('Microsoft. (n.d.). <em>Workflow Capabilities.</em> Microsoft Agent Framework documentation.',
           'https://learn.microsoft.com/en-us/agent-framework/workflows'),
    'r4': ('OpenAI. (n.d.). <em>Guardrails and human review</em>. OpenAI API documentation.',
           'https://developers.openai.com/api/docs/guides/agents/guardrails-approvals'),
    'r5': ('OpenAI. (n.d.). <em>Running Agents.</em> OpenAI Agents SDK documentation.',
           'https://developers.openai.com/api/docs/guides/agents/running-agents'),
    'r6': ('OpenAI. (n.d.). <em>Evaluate Agent Workflows.</em> OpenAI Platform documentation.',
           'https://developers.openai.com/api/docs/guides/agent-evals'),
    'r7': ('OpenAI. (n.d.). <em>Integrations and Observability.</em> OpenAI API documentation.',
           'https://developers.openai.com/api/docs/guides/agents/integrations-observability'),
    'r8': ('Microsoft. (2026). <em>Microsoft Agent Framework workflows: Observability</em>. Microsoft Learn.',
           'https://learn.microsoft.com/en-us/agent-framework/workflows/observability'),
    'r9': ('Schluntz, E., &amp; Zhang, B. (2024, December 19). <em>Building effective agents</em>. Anthropic.',
           'https://www.anthropic.com/research/building-effective-agents'),
    'r10': ('LangChain. (n.d.). <em>LangGraph Graph API — Re-execution and Idempotency.</em>',
           'https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/graph-api.mdx'),
    'r11': ('LangChain. (n.d.). <em>LangGraph Functional API — Idempotency.</em>',
           'https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/functional-api.mdx'),
    'r12': ('Model Context Protocol. (2025). <em>Authorization — MCP Specification (2025-11-25).</em>',
           'https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/authorization.mdx'),
    'r13': ('Autio, C., Schwartz, R., Dunietz, J., Jain, S., Stanley, M., Tabassi, E., Hall, P., &amp; Roberts, K. (2024, July 26). <em>Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile</em> (NIST AI 600-1). National Institute of Standards and Technology.',
           'https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence'),
    'r14': ('OWASP Agentic Security Initiative. (2025). <em>Agentic AI — Threats and Mitigations.</em>',
           'https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/'),
    'r15': ('Microsoft. (n.d.). <em>Agent Framework Overview.</em>',
           'https://learn.microsoft.com/agent-framework/overview'),
    'r16': ('OpenAI. (n.d.). <em>Safety in Building Agents.</em>',
           'https://developers.openai.com/api/docs/guides/agent-builder-safety'),
    'r17': ('OpenAI. (n.d.). <em>Tracing — OpenAI Agents SDK.</em>',
           'https://openai.github.io/openai-agents-python/tracing/'),
}

CODE = {
    'contract': '{\n  "case_id": "WMS-042",\n  "workflow_version": "5.1.0",\n  "task_id": "verify-integration-claim",\n  "agent_role": "EvidenceReviewer",\n  "input_refs": ["artifact://wms-042/vendor-claims.json"],\n  "allowed_tools": ["document_retrieval", "claim_checker"],\n  "output_schema": "verified_claims/v2",\n  "limits": {"max_attempts": 2, "deadline_sec": 240},\n  "risk_class": "advisory_read_only",\n  "status": "VALIDATING",\n  "next_allowed": ["ACCEPT", "REWORK", "ESCALATE", "STOP"],\n  "external_write_authorized": false,\n  "evidence_refs": ["source:vendor-manual-2026-07"],\n  "policy_version": "policy-4.2"\n}\n',
    'process': 'def process_action(case, proposal):\n    validate_contract(case, proposal)\n    check_scope_and_policy(case.actor, proposal.tool, proposal.args)\n    if not evidence_gate_passes(case):\n        return bounded_rework_or_escalate(case, "EVIDENCE_GAP")\n    if proposal.has_external_side_effect:\n        approval = require_action_specific_approval(\n            case, proposal, recipient=proposal.recipient)\n        if approval != "APPROVED":\n            return pause_or_stop(case)\n    key = stable_idempotency_key(case, proposal)\n    receipt = execute_once_or_reconcile(key, proposal)\n    if not verify_receipt(receipt):\n        return escalate_for_reconciliation(case)\n    record_trace_and_checkpoint(case, receipt)\n    return release_or_continue(case)\n',
}

BODY = r"""
## Introduction: Why Multi-Agent Systems Need a Harness

A multi-agent prototype can appear successful when one model asks another to research a question, a third produces an analysis, and a fourth writes a report. This is a demonstration of cooperation, not yet an engineered operating system. A production workload must answer additional questions: What evidence was available to each agent? Can a failed call be retried without sending a duplicate email? Does approval apply to this exact action and recipient? Which artifact was reviewed? What happens when a model, tool, network, or reviewer is unavailable? How does an operator reconstruct the run after a complaint or incident?

The **agent harness** is the application-side machinery that makes those questions answerable. Microsoft's Agent Framework describes it as runtime scaffolding that connects the chat client, function invocation, history persistence, context providers, approval-handling middleware, and observability [@r2]. OpenAI documents related runtime functions through runs and resumable state, guardrails, approval interruptions, and traces of model and tool activity [@r4, @r5, @r6, @r7, @r17]. A harness is therefore **broader than a planner or workflow diagram**. It owns the engineered boundary between probabilistic proposals and authorized effects.

This paper uses *harness engineering* for the design, construction, validation, deployment, and continuous improvement of that operating boundary. It extends an earlier paper in this journal on multi-agent coordination and failure modes [@r1]. The proposed lifecycle is an author-developed engineering synthesis; its seven labels are not claimed to be a formal industry standard. The appropriate design may use one agent, several agents, a deterministic workflow with embedded LLM steps, or a hybrid. Complexity should be justified by measured requirements rather than the number of agents [@r9].

**Scope and limits.** The discussion targets business and engineering knowledge workflows with external data, documents, and tools. It is not a substitute for domain-specific safety engineering, privacy assessments, professional review, cybersecurity assurance, or regulatory compliance. A model's own statements of confidence or successful completion are not independent verification.

## System Definition: Agents, Skills, Workflows, and Harnesses

Four related concepts are often conflated. An **agent** is a task-oriented component that uses a model and authorized capabilities to select or perform actions. A **skill** is a reusable, versioned capability or procedure invoked by an agent; it may combine instructions, scripts, and tools. A **workflow** defines dependencies and legal handoffs between work steps. A **harness** drives model and tool calls, manages state and context, applies approval policies and emits telemetry [@r2], while workflow features add checkpointing, resumption and human-in-the-loop pauses [@r3]. Microsoft's framework also separates agents, for open-ended tasks, from workflows, for processes with well-defined steps [@r15]. A tool or API is a callable interface; it is not intrinsically a skill, an agent, or a trusted authority.

TABLE Functional distinctions. || Products may combine these responsibilities in one library or service; the control obligations remain even when the software packages do not map one-to-one.
| Component | Core responsibility | Typical artifact | Must not be trusted to do alone |
| Agent | Interpret a scoped task and propose or perform bounded work | Research findings, draft, tool-use proposal | Grant its own permissions or attest independent correctness |
| Skill / tool | Provide a reusable capability with an input/output contract | Query result, calculation, generated file | Redefine authorization scope or invent source provenance |
| Workflow | Specify step dependencies, routing, fan-out/fan-in, and gates | Versioned task graph and transition rules | Guarantee side-effect safety without runtime enforcement |
| Harness | Enforce budgets, policies, state, routing, checkpoints, approvals, and logs | Run record, receipts, decisions, validated artifact | Replace human accountability or domain-specific controls |

Table 1 summarizes what each component may and may not be trusted to do. A useful reference implementation separates five concerns. The **experience layer** receives goals and presents status, uncertainty, and approval requests. The **coordination layer** decomposes and routes tasks. The **execution layer** runs agents, tools, and deterministic computations. The **assurance layer** validates schemas, evidence, policy, and release readiness. The **operations layer** records state, traces, performance, incidents, versions, and recovery actions. Some functions cross layers; conceptual separation prevents a language-model instruction from masquerading as a security control.

## Seven Stages of the Harness Engineering Lifecycle

Figure 1 sets out the seven stages, the work package and output of each, and the controls that apply across all of them.

FIG fig1-lifecycle || The proposed seven-stage Harness Engineering lifecycle. The stages form an engineering lifecycle rather than a single agent run; governance, authorization, test evidence and observability cut across all of them. Stage 7 returns measured findings to earlier stages through change control and does not authorize automatic production changes. || Seven colored stage columns from Define and Discover to Improve and Evolve, each listing its work package and stage output, a dashed improvement loop returning from stage 7 to stage 1, and a band of five cross-cutting controls below. || 

### 3.1 Stage 1 — Define & Discover

Start from a **bounded business or engineering outcome**, not from the aspiration to deploy a team of agents. Inventory source systems, data classes, workflow owners, current baseline performance, failure consequences, approvers, dependencies, and available tools. Define which actions are read-only, reversible, externally visible, financially consequential, or safety relevant. The minimum design-basis record should include use case, success criteria, non-goals, information boundaries, safety/privacy classification, cost envelope, acceptance thresholds, and named business owner.

An effective discovery exercise also establishes a non-agent baseline: a scripted process, a retrieval-augmented single agent, or a human-supported workflow. If a fixed procedure can meet the requirements, adding subagents may increase cost and coordination risk without improving the outcome [@r9]. **Deliverables:** problem statement, capability inventory, requirements register, initial risk assessment, benchmark and success metrics.

### 3.2 Stage 2 — Design & Architect

Decompose the request into **typed tasks and evidence-bearing interfaces**. Identify specialist roles only where they add independently testable value, design serial or parallel dependencies, select a tool-broker pattern, decide where state is stored, and specify the trust boundary around each data source. Draw both the happy path and the exception paths. Define a state machine with explicit PASS, REWORK, ESCALATE, and STOP outcomes and an owner for each transition. Separate a quality check from permission to perform an external write.

Architecture decisions should record: context-scoping rules, agent/tool allowlists, memory retention, checkpoint granularity, idempotency strategy, redaction and trace retention, model versioning, rework budget, approval authority, rollback plan, and recovery objectives. **Deliverables:** architecture diagram, agent/skill register, workflow/state model, policy matrix, acceptance-test design, threat model, observability specification.

### 3.3 Stage 3 — Build & Integrate

Build the harness **before** attempting unrestricted autonomy. Implement structured contracts and schema validation, versioned prompts and skills, tool wrappers with least-privilege credentials, a shared artifact index, checkpoints, and a policy service that is independent of the model. Isolate externally retrieved instructions and data from trusted system configuration. Apply deterministic checks at tool execution boundaries; a friendly-looking instruction asking an agent to “be careful” is not an access-control mechanism [@r4, @r14].

Use structured error classes rather than allowing every failure to become another model prompt. Examples include TRANSIENT_TOOL_FAILURE, INVALID_SCHEMA, EVIDENCE_GAP, POLICY_DENIED, and APPROVAL_REQUIRED. Each class maps to a permitted next state. **Deliverables:** runnable workflow, typed contracts, tool integrations, policy rules, secrets configuration, reproducible build and initial test fixtures.

### 3.4 Stage 4 — Test & Validate

Test the **whole workflow**, not just the underlying model's ability to answer questions. Separate unit tests for skill functions, contract tests for tool schemas, integration tests for handoffs and storage, security adversarial tests, fault-injection tests, evaluation datasets, and user acceptance tests. OpenAI's agent evaluation guidance emphasizes traces, graders, datasets, and repeatable evaluation runs as tools for identifying workflow-level regressions [@r6].

Important negative cases include stale memory, prompt-injected source text, revoked credentials, duplicate job delivery, a time-out after an external write, wrong-recipient emails, unsupported citations, interrupted approval, and concurrent edits to shared state. Test STOP and ESCALATE as legitimate outcomes—not as failures to produce a polished answer. **Deliverables:** evaluation suite, defect log, red-team results, signed test record, risk exceptions and approval to release.

### 3.5 Stage 5 — Deploy & Release

Release a **versioned system**, not merely a revised prompt. Record configuration hashes for the orchestrator, agent definitions, skill registry, model/provider selection, tool schemas, permissions, and policy. Use a staged path such as offline testing → shadow mode → low-risk pilot → controlled production. Release gates should evaluate evidence of safe operation, security review, budget controls, rollback feasibility, trained operators, and production monitoring.

A *model or prompt change* can alter behavior even if application code is unchanged; therefore it requires evaluation proportionate to risk. Deploy approval is different from individual transaction approval. **Deliverables:** release manifest, change record, rollback package, monitoring alerts, operational runbook, owner acceptance.

### 3.6 Stage 6 — Operate & Monitor

Observe both **system health** and **decision quality**. Trace run IDs, task and tool IDs, state transitions, latency, cost, evidence provenance, guardrail trips, approvals, retries, and actual external side effects. Redact sensitive payloads and govern access to telemetry; observability itself can create a privacy exposure. Microsoft's workflow observability guidance describes span, log, metric, and event structures and warns against enabling sensitive-data capture indiscriminately [@r8].

Operational procedures should cover incident detection, case quarantine, credential revocation, manual takeover, safe restart, artifact correction, and client notification when warranted. Human approval queues need timeouts and escalation ownership; a paused workflow should not silently release because its reviewer is absent. **Deliverables:** live dashboards, alerts, audit trail, incident log, cost and quality trends, recovery evidence.

### 3.7 Stage 7 — Improve & Evolve

Use measured failures and reviewer feedback to propose improvements to decomposition, prompting, tool contracts, policies, or skills. Distinguish an **in-run retry** from a **governed version change**. A single surprising output is a useful incident signal but not enough evidence to rewrite general policy. Collect representative cases, diagnose root cause, build regression tests, seek approval, deploy to a cohort, and monitor for unintended changes. Memory entries and reusable lessons require provenance, owner, version, scope, and retirement criteria.

The improvement loop closes with a change-control record: problem, evidence, proposed modification, evaluation outcomes, decision, release version, and rollback trigger. **Deliverables:** updated tests and runbooks, approved change request, new release, refreshed metrics and documented lessons learned.

## Runtime Architecture: Control, Execution, and Evidence Boundaries

Figure 2 shows the reference runtime: where untrusted inputs enter, where the harness decides, where workers act and where evidence is kept.

FIG fig2-runtime || Harness reference architecture. Agent proposals pass through typed task contracts; the application-owned policy service and tool broker enforce permissions, approvals and argument checks before any external effect. State and evidence stores provide versioned recovery, and telemetry observes the whole path. A logical architecture, not a framework's documented internals. || Request and sources on the left feed a harness control plane holding task routing, state and checkpoints, policy and approvals, and a tool broker; isolated workers on the right; below, durable state and evidence, traces and evaluation, and an operator or human gate. || 

A robust harness distinguishes **control signals** (trusted policies, roles, allowed transitions), **work data** (documents, retrieved text, tool results), and **evidence** (source references, computed values, approved artifacts, tool receipts). An agent reading a vendor PDF may summarize its contents but must not inherit instructions inside that PDF. When agents share a workspace, write access should be limited to designated artifacts, with provenance and version checks. Sensitive context is supplied according to least need, not broadcast to all workers.

The execution graph can combine deterministic tasks, LLM agents, and external services. The designer may use sequential or parallel paths, but shared-state updates must be coherent and checkable. A manager-agent's conclusion that a delegated job “is complete” is not a substitute for the worker's validated result or tool receipt. The harness should preserve enough structured state to reconstruct the path from user request to released output.

### 4.1 Tool brokerage and policy enforcement

Every tool call should identify the actor, approved scope, target system, action, validated arguments, risk classification, permission basis, and correlation ID. Read-only retrieval may be allowed within a preapproved scope; external writes and sensitive operations should pass a separate authorization path. OpenAI differentiates automatic input/output/tool guardrails from approvals that pause a run before a side effect [@r4]. Its documentation also highlights that the scope of a guardrail depends on its attachment point; placing one input guardrail at the beginning is not equivalent to enforcing every subsequent tool call.

A tool wrapper should not trust its caller to declare whether permission exists. Security boundaries belong in application code, identity permissions, network/file-system restrictions, and approval services. Integrations based on Model Context Protocol (MCP) require the same distinction: MCP defines authorization at the transport level and makes it optional [@r12], so transport authorization does not by itself authorize particular tool effects, which the application must still check.

### 4.2 Durable state and safe replay

Agent workflows are frequently interrupted by limits, network failures, application restarts, or human approval. LangGraph documentation warns that re-execution may replay code around a checkpoint and recommends idempotent operations for side effects [@r10, @r11]. A harness should therefore checkpoint **logical progress**, persist tool results and action IDs, and reconcile uncertain outcomes before attempting another external call.

For example, a vendor-outreach request with action key case-042:vendor-A:email-v1 should check whether a message was already sent before retrying. If the send service times out after accepting the message, the system should query receipt status or escalate rather than blindly resend. A transactional outbox, provider deduplication token, or read-before-write protocol can implement this contract, depending on the external system.

## Execution Contracts, State Machine, and Stage Gates

A harness should store the **next legal action** separately from an agent's prose. A minimal task record contains task ID, case ID, purpose, assigned role, input references, expected output schema, source/evidence requirements, tool and data permissions, deadline, retry budget, risk class, and acceptance owner. The case record also identifies model and skill versions so a reviewer knows which code and instructions produced the artifact. Example 1 shows such a record.

CODE contract || Example 1. Illustrative case and task contract, not a framework-specific API. The artifact and source IDs are fictional; authorization and policy version are issued or verified by the harness, never self-assigned by an agent.

A case lifecycle may be expressed as INTAKE → PLANNED → EXECUTING → VALIDATING → REVIEW_REQUIRED → APPROVED → COMMITTED → COMPLETE, with alternate transitions to REWORK, ESCALATED, FAILED, or STOPPED. Gate conditions include typed schema validity; evidence coverage; correct classification; allowed tool/action; replay and idempotency status; reviewer identity; and action-specific approval. The harness should reject impossible transitions even when an agent recommends them. Figure 3 runs the state machine through five scenarios.

FIG fig3-action-states || The action state machine run as five scenarios. The figure plays each scenario in turn: a normal run, a bounded rework, an approval that is refused, a timeout after an external write that must be reconciled, and an injected instruction that is blocked; select a scenario to jump to it, or <em>All scenarios</em> to compare them. A model can draft an action but cannot move an unapproved write into COMMITTED, and STOP is a completed, controlled outcome. || Six states in a row, propose, validate, authorize, execute, reconcile and commit, with an agent above, an evidence store below, an approver beside the authorize state and an external system beside execute, each scenario shown with its outcome and the control that decides it. || 

The pseudocode in Example 2 demonstrates the boundary, deliberately independent of a specific AI platform.

CODE process || Example 2. Framework-neutral action boundary: validation and policy before execution, approval for side effects, execute once or reconcile, then record.

The order is intentional: schema and policy validation precede consequential execution; a result is committed only after a receipt or reconciliation evidence. An LLM may assist with review, but an LLM-generated approval token is never accepted as identity-backed authorization.

## Test and Validation: An Assurance Case, Not a Demo

**End-to-end evaluation** requires both expected-success and expected-failure cases. A benchmark that scores only the final answer can miss unauthorized tool calls, leaked data, unbounded loops, or duplicate side effects. Build tests around claims the system must satisfy: “all released figures have a source or calculation,” “a rejected action cannot execute,” “resuming a run cannot duplicate a send,” and “a missing reviewer results in PAUSED, not APPROVED.” Trace-level evaluation can test tool selection, handoffs, policy violations, and routing decisions [@r6].

TABLE Recommended harness validation matrix. || Thresholds should follow business impact and risk classification. “Zero tolerance” identifies an acceptance rule, not proof that residual cybersecurity risk is literally zero.
| Test layer | Representative test | Required evidence | Release consequence if failed |
| Unit / contract | Malformed skill payload or bad enum | Validator rejects and logs exact field | Block affected release |
| Integration | Worker handoff loses source ID | Lineage test detects missing input reference | Block affected workflow |
| Factuality / provenance | Vendor compatibility claim lacks primary source | Claim withheld or labeled unverified | Rework or escalate |
| Security | Injected instructions inside retrieved document | No change to tools, scope, or policy | Security release blocker |
| Authorization | Agent proposes sending an unapproved email | Tool remains uncalled; approval pause logged | Zero tolerance for bypass |
| Resilience | Network timeout after external write | Reconciliation avoids duplicate action | Rollback / containment |
| Operations | Trace exporter unavailable | Local durable event queue, alert, safe degradation | Risk-based go/no-go |
| Human factors | Reviewer rejects request or misses deadline | STOP/PAUSED with auditable ownership | Require reviewed runbook |

Table 2 sets out the validation matrix. Testing should use multiple cases and seeded variations, not a single hand-curated success. Establish a baseline and version-locked evaluation set, with holdout tasks to discourage overfitting to examples. Report failure rates with denominators and uncertainty where sample size permits. A “100% pass rate” over ten easy examples should never be advertised as general reliability.

### 6.1 Risk-based release evidence

A lightweight assurance case connects **claim → evidence → owner → decision**. For example: the claim “no unauthorised external email is sent” is supported by integration tests, audit events, identity controls, and approval-path tests; the owner is the application/service operator; and the release reviewer accepts or rejects the evidence. A standard such as NIST's Generative AI Profile offers risk management principles and suggested actions, but it does not certify this particular harness or prescribe a single architecture [@r13].

## Reliability Engineering: Recovery, Concurrency, and Cost Budgets

Several distinct failure categories require distinct remedies, and Table 3 lists the harness response to each. **Transient infrastructure errors** may justify bounded retries with exponential backoff. **Semantic defects** (unsupported claims or wrong unit conversions) require more evidence or a corrected method, not just another attempt with the same prompt. **Permission denials** require a changed legitimate authorization, never reworded tool arguments. **Unsafe requests** terminate or escalate. A system should retain evidence of rejected proposals so reviewers can investigate attempted policy crossings.

Concurrent agents can reduce wall-clock time, but they introduce fan-in barriers and the possibility of inconsistent shared writes. Adopt versioned artifacts and optimistic concurrency or locking where needed. Set task-specific deadlines, concurrency ceilings, token/tool budgets, maximum depth of delegation, and a total case budget. When one parallel branch fails, decide explicitly whether the case can produce a partial answer, must rework, or must stop; do not let the aggregator invent a missing branch result.

A useful planning model is Eq. (1), evaluated at the accepted-case level rather than per generated message:

TEX C_{\text{case}} = C_{\text{model}} + C_{\text{tool}} + C_{\text{infra}} + C_{\text{review}} + C_{\text{rework}}

In a simplified parallel execution stage, the stage latency follows Eq. (2), where the maximum runs over the branches *b*:

TEX T_{\text{stage}} \approx \max_b T_b + T_{\text{orch}} + T_{\text{valid}}

Real production latency also includes queueing, rate limits, approval waits, and retries. Both expressions are **engineering planning identities**, not empirical benchmark laws.

TABLE Failure handling matrix for controlled, recoverable agent execution. || 
| Failure condition | Harness response | Why retry alone is insufficient |
| Timeout before a read-only query result | Retry within limit; reuse cached result if valid | Excessive retries can overload vendor APIs |
| Timeout after a write request | Reconcile using action ID; do not blind-resend | Side effect may already have occurred |
| Agent output lacks required sources | REWORK with specific evidence request | A second answer may merely repeat the claim |
| Source contains prompt-injected instructions | Quarantine text as untrusted data; policy unchanged | Model may obey repeated malicious instructions |
| Conflicting parallel artifacts | Validate version and ownership; resolve conflict | Last-write-wins may silently lose evidence |
| Approver unavailable | PAUSE / ESCALATE by deadline | Approval cannot be inferred from silence |

## Security, Privacy, and Operational Governance

Agent systems are exposed to **indirect prompt injection**, tool misuse, credential overreach, sensitive-information leakage, uncontrolled delegation, and unverified memory. OWASP's Agentic AI Threats and Mitigations initiative organizes these into a threat-model-based perspective [@r14], and OpenAI recommends passing untrusted inputs through user messages, constraining data flow with structured outputs, and keeping tool approvals enabled [@r16]. The central defence is **separation of trust and authority**: retrieved content and agent text are evidence candidates, not operating instructions; a policy engine determines whether an action is allowed; and the target system independently authenticates and authorizes it.

A practical protection stack includes source classification, untrusted-content labeling, least-privilege service identities, explicit network and filesystem scopes, tool argument validation, secret isolation, immutable audit events, data minimization, encrypted state, retention controls, and approved response channels. For multi-client advisory settings, case-specific data boundaries must prevent one client's material from being retrieved in another client's workflow. The harness should distinguish shared general engineering know-how from protected client-specific records.

Document approvals for **deployment** (release version), **case execution** (workflow initiation), and **external side effects** (message, transaction, configuration edit) separately. One approval does not imply the others. Controls also need compensating processes: manual review, audit sampling, exception reporting, root-cause analysis, and incident response. Framework features simplify implementation, but builders must add review and enforcement in their own harness [@r4], and NIST notes that implementation of its suggested actions will vary with the organization [@r13]; accountability therefore remains with the deploying organization.

### 8.1 What the harness must not claim

An AI reviewer that agrees with another agent is not automatically independent ground truth. A trace is evidence of what the system recorded, not proof the underlying claim is correct. A policy written only in natural-language instructions is not an enforced access boundary. Saving feedback does not train model weights. And an apparently green dashboard does not establish low residual risk if rare severe failures were excluded from testing.

## Worked Example: A Hypothetical SME WMS Evaluation Harness

Consider an invented Vancouver importer/distributor evaluating warehouse management software. It has a legacy accounting application, spreadsheet inventory records, multilingual operations, and a requirement to avoid automatic vendor outreach. The exercise is **illustrative only**; the stated facts, numbers, and results below are not findings from a client engagement.

**Step 1 — Scope and plan.** A human owner supplies approved requirements: inventory control, barcode picking, accounting integration, and a bilingual operator workflow. The Intake Agent labels the source documents; the Planner produces a task graph. The harness permits retrieval from vendor product pages and approved internal files, but blocks writes to accounting systems and external messages.

**Step 2 — Execute independent research.** Vendor Research Agents collect official descriptions and integration manuals in parallel, each in its own scoped context. The Data Analyst compares coverage against a requirements matrix. The Drafting Agent prepares a comparison with citations and “unknown” fields. Every claim stores a source ID, retrieval time, version, and confidence basis; public marketing text is not treated as authoritative proof of tested compatibility.

**Step 3 — Assure.** The Evidence Reviewer checks 20 illustrative integration and functionality claims. Suppose **16** are supported by available documentation, **3** remain unresolved, and **1** contradicts a dated technical source. The harness reports 80% verified coverage (16/20); it does not mark all 20 claims confirmed. The contradicted claim is corrected or withheld, and the three unresolved items become explicit vendor questions.

**Step 4 — Decision and authorization.** A Strategy Agent proposes a shortlist and drafts vendor inquiry emails. The harness can approve the *internal draft* after QA while leaving each external message in PENDING_HUMAN_APPROVAL. A named reviewer must approve the exact recipients and text. If no approval arrives, the system retains the draft without sending anything. A later approval is linked to the relevant email version, not to all subsequent messages.

**Step 5 — Release and learn.** The final report includes verified features, unsupported claims, implementation dependencies, constraints, assumptions, and next decisions. The operations team reviews false positives, total spend, review time, and evidence defects. Only validated, generalized findings may be proposed as improvements to the vendor-research skill; private client content is not automatically placed into a cross-client memory store.

For a deliberately **hypothetical cost illustration**, assume this pilot requires 120 minutes per case manually versus 75 minutes with the harness, *including* 20 minutes of reviewer time and 10 minutes for exception handling. Gross labor time saved is 45 minutes (37.5% of the manual baseline). At 40 cases per month, gross time saved would be 30 hours. This is **not** net ROI: token/API/hosting charges, integration maintenance, audit burden, and variance in case complexity must also be included before claiming economic benefit.

## Performance Engineering and Production Acceptance

Measure the **entire accepted-case path**, not the count of invoked agents. Separate throughput from quality and compliance. A work product that finishes quickly while missing evidence or bypassing approval is a failure regardless of token efficiency.

TABLE Suggested operating scorecard. || Metrics and targets are proposals to be tailored and risk-weighted; they are not universal external benchmarks.
| Measure | Definition / denominator | Suggested review question |
| Verified completion rate | Cases meeting all acceptance gates / all attempted cases | Are escalations and stops visible in the denominator? |
| Provenance coverage | Supported material claims / material claims assessed | Is a cited marketing claim truly relevant evidence? |
| Unauthorized side-effect rate | Unauthorized writes / all side-effect attempts | Were denied actions captured, not hidden? |
| Duplicate-action rate | Duplicate consequential actions / all consequential actions | Is replay safe after ambiguous timeouts? |
| Approval processing time | Time from approval request to disposition | Does the queue have an owner and escalation SLA? |
| p95 end-to-end latency | 95th percentile case completion time | Are wait states and retries included? |
| Fully loaded cost per accepted case | Total run, tool, infrastructure and review cost / accepted cases | Is it better than a simpler baseline? |
| Regression escape rate | Confirmed post-release defects not detected pre-release / total confirmed defects | Are failure-mode tests being updated? |

Table 4 proposes an operating scorecard. A useful pilot dashboard separates **ACCEPTED**, **ACCEPTED_AFTER_REWORK**, **ESCALATED**, and **STOPPED**. Consider a fictional 100-case test set: 82 accepted first pass, 12 accepted after one rework, 4 escalated, and 2 stopped. The verified completion proportion is **94/100 = 94%**, whereas first-pass completion is **82%**. Both figures are valid only if the rubric is externally checked and sample selection is disclosed. A 94% acceptance rate says nothing about the severity of any missed unauthorized operation; gate bypasses require a separate near-zero-tolerance assessment.

## Implementation Roadmap: Smallest Safe Harness First

A practical deployment can proceed in four increments rather than a large autonomous rollout:

1. **Baseline and read-only prototype:** Document the business task, manual benchmark, relevant source permissions, and evaluation cases. Implement one agent or deterministic workflow that produces structured artifacts without external writes.
2. **Typed workflow and assurance gates:** Add role-based handoffs, schema validation, evidence pack, bounded retry, decision record, and independent review. Verify the system correctly stops on unsupported claims.
3. **Durable integration and approval:** Add checkpointing, idempotent tool wrappers, per-action approval, secrets segregation, telemetry, and rollback. Fault-inject a timeout after an external action and demonstrate safe reconciliation.
4. **Controlled production and improvement:** Release to a restricted cohort, monitor accepted-case quality/cost/latency and incidents, review defects, and version prompts, skills, and policies through change control.

**Minimum go-live checklist:** named system and business owner; documented data and tool scope; version-locked evaluation suite; tested approvals and STOP path; protected credentials; trace and artifact retention controls; backup/recovery; manual fallback; cost caps; incident escalation; and an agreed monitoring review cadence. For consequential domains, add required professional, safety, legal, and compliance signoffs before operational use.

## Conclusion: Engineer the Boundaries, Not Just the Agents

The central design decision in multi-agent AI is not how many specialist models can be assembled. It is how the application proves that a proposed action is **supported, permitted, repeatable, recoverable, and accountable**. A well-designed harness turns agent outputs into typed evidence, controls the step transitions, isolates tools behind enforceable boundaries, and records the difference between a model's suggestion, a reviewer decision, and an actual external result.

The seven-stage Harness Engineering lifecycle provides a repeatable way to work from requirements through architecture, implementation, validation, release, monitoring, and governed improvement. It is intentionally compatible with multiple frameworks and organizational risk tolerances. The practical engineering rule is simple: **make autonomy conditional on verified capability and constrained authority; increase it only when the evidence warrants doing so.**
"""
