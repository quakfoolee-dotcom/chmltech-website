"""Chmltech Online Journal, Vol. 106, Issue 11 (Multi-Agent AI Engineering series, Article 3). Figure 1 is interactive (live/mae3.html)."""

SLUG = 'stage-gate-orchestration-building-reliable-multi-agent-workflows-with-feedback-loops'
META = dict(
    volume=106,
    issue=11,
    title='Stage-Gate Orchestration: Building Reliable Multi-Agent Workflows with Feedback Loops',
    short_title='Stage-Gate Orchestration for Multi-Agent Workflows',
    meta='Stage gates for LLM agent workflows: PASS, REWORK, ESCALATE and STOP transitions, five reference gates, bounded rework loops, approval binding and a worked SME example.',
    keywords=['multi-agent AI', 'stage gates', 'workflow orchestration', 'feedback loops', 'human-in-the-loop', 'quality assurance', 'LLM agents', 'agent governance'],
)
ABSTRACT = 'A multi-agent workflow can execute every assigned task and still deliver an unacceptable outcome. Research agents can rely on weak evidence, analyst agents can propagate incompatible assumptions, and drafting agents can turn provisional findings into confident recommendations. Stage-gate orchestration introduces explicit decision points that determine whether an artifact may proceed, must be revised, requires human review, or should be stopped. This paper treats stage gates as engineering controls layered over sequential, parallel, and hybrid multi-agent workflows. It proposes a state-and-evidence model for gates; distinguishes deterministic checks, independent AI review, and human authorization; and shows how targeted feedback loops, checkpoints, retry budgets, and audit records change reliability, latency, and cost. A hypothetical SME warehouse-management-system (WMS) advisory assessment illustrates a five-gate design, including a revision loop and an intentionally withheld recommendation. The result is a practical blueprint for bounded, observable, evidence-led multi-agent execution—not a claim that additional reviewing agents automatically make systems correct.'

REFS = {
    'r1': ('Lee, Q. F. (2026). <em>Multi-Agent AI Systems: Architectures, Coordination Patterns and Failure Modes.</em> Chmltech Online Journal.',
           'https://www.chmltech.com/post/multi-agent-ai-systems-architectures-coordination-and-failure-modes.html'),
    'r2': ('Microsoft. (2026). <em>Workflows</em> (section: Choosing the right pattern). Microsoft Agent Framework documentation.',
           'https://learn.microsoft.com/en-us/agent-framework/journey/workflows'),
    'r3': ('LangChain. (n.d.). <em>LangGraph: Interrupts and human-in-the-loop execution.</em>',
           'https://docs.langchain.com/oss/python/langgraph/interrupts'),
    'r4': ('OpenAI. (n.d.). <em>Agents SDK: Human-in-the-loop approvals and durable run state.</em>',
           'https://openai.github.io/openai-agents-python/human_in_the_loop/'),
    'r5': ('Microsoft. (n.d.). <em>Agent Framework: Human-in-the-loop requests and checkpoints.</em>',
           'https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop'),
    'r6': ('OpenAI. (n.d.). <em>Agents SDK: Guardrails and tripwires.</em>',
           'https://openai.github.io/openai-agents-python/guardrails/'),
    'r7': ('OpenAI. (n.d.). <em>Agents SDK: Tracing.</em>',
           'https://openai.github.io/openai-agents-python/tracing/'),
    'r8': ('Amazon Web Services. (n.d.). <em>AWS Step Functions: Choice workflow state.</em>',
           'https://docs.aws.amazon.com/step-functions/latest/dg/state-choice.html'),
    'r9': ('Amazon Web Services. (n.d.). <em>Handling errors in Step Functions workflows</em>. AWS Step Functions Developer Guide.',
           'https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html'),
    'r10': ('Google. (n.d.). <em>Agent Development Kit: Loop workflow.</em>',
           'https://adk.dev/agents/workflow-agents/loop-agents/'),
    'r11': ('OWASP. (n.d.). <em>LLM06:2025—Excessive Agency.</em>',
           'https://genai.owasp.org/llmrisk/llm062025-excessive-agency/'),
    'r12': ('National Institute of Standards and Technology. (2023). <em>AI RMF Core</em> (AI RMF 1.0). NIST Trustworthy and Responsible AI Resource Center.',
           'https://airc.nist.gov/airmf-resources/airmf/5-sec-core/'),
    'r13': ('OWASP. (n.d.). <em>Prompt Injection: Security Glossary.</em>',
           'https://genai.owasp.org/glossary/prompt-injection/'),
    'r14': ('Microsoft. (n.d.). <em>Agent Framework: Workflow checkpoints and restoration.</em>',
           'https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints'),
    'a9': ('Lee, Q. F. (2026). Research, Analyze, Draft, Review, Finalize: Engineering a reliable five-agent AI workflow. <em>Chmltech Online Journal</em>, 106(2).',
           'https://www.chmltech.com/post/research-analyze-draft-review-finalize-engineering-a-reliable-five-agent-ai-workflow'),
}

CODE = {
    'gate': 'MAX_REVISIONS = 2   # revisions after first submission\n\nwhile workflow.has_next_stage():\n    stage = workflow.next_stage()\n    artifact = execute_stage(stage, validated_inputs=True)\n    save_artifact_version(artifact)\n\n    while True:\n        decision = evaluate_gate(stage.gate, artifact)\n        record_gate_decision(decision, artifact.version)\n\n        if decision.kind == "PASS":\n            workflow.advance(artifact.version)\n            break\n\n        if decision.kind == "STOP":\n            workflow.quarantine(decision.reason)\n            raise WorkflowStopped(decision.reason)\n\n        if decision.kind == "ESCALATE":\n            request_authorized_review(\n                artifact.version, decision, stage.gate\n            )\n            # Return control to the event handler: no busy-loop polling.\n            workflow.persist_wait_state(artifact.version, decision)\n            return "WAITING_FOR_HUMAN"\n\n        if decision.kind == "REWORK":\n            if stage.revisions_used >= MAX_REVISIONS:\n                workflow.hold_for_review()\n                raise WorkflowHeld("Revision budget exhausted")\n            artifact = rework_targeted_defects(\n                owner=decision.owner,\n                issues=decision.issues,\n                prior_version=artifact.version\n            )\n            stage.revisions_used += 1\n            invalidate_downstream_dependents(artifact)\n            save_artifact_version(artifact)\n\n# External actions require a separate final authorization and idempotency.\nauthorized_release = verify_release_scope_and_version(workflow)\nexecute_external_action_once_or_reconcile(authorized_release)\n',
}

BODY = r"""
## Introduction: Completion Is Not Acceptance

A typical multi-agent workflow hands work from one specialist to another: a research agent gathers sources, an analyst evaluates evidence, a drafting agent prepares a recommendation, and a reviewer inspects the result. The existence of a final message, however, establishes only that the execution path reached its end. It does not establish that the sources are trustworthy, the calculations reproducible, the recommendation authorized, or the output fit for a particular decision.

A **stage gate** is an explicit decision boundary between stages. It evaluates a defined artifact against predefined acceptance criteria, then selects a controlled transition: **PASS**, **REWORK**, **ESCALATE**, or **STOP**. A gate may be a deterministic validator, an independent review agent, a qualified human, or a combination. This is distinct from merely asking the same model to “check its work,” a practice that can reproduce the original error without adding independent evidence. An earlier paper in this journal recommends bounded loops, structured handoffs, and externally grounded verification [@r1].

Contemporary agent runtimes make these controls implementable. Microsoft Agent Framework documents explicit workflow edges and human-in-the-loop interactions; LangGraph supports persistence-backed interruptions; OpenAI's Agents SDK supports tool approvals, guardrails, and run-state restoration. These are framework capabilities, not a guarantee that a configured gate will reach the right decision [@r2, @r3, @r4, @r5]. The engineering task is to specify what a gate checks, what evidence it uses, and what happens if it disagrees with the upstream agent.

**Scope.** This paper addresses review-oriented knowledge work, enterprise software assessments, and technical engineering documentation. In safety-critical applications, stage gates support—but do not replace—qualified engineering review, formal management of change, or authorized operating procedures. The proposed five-gate structure is an illustrative design pattern, not a formal industry standard.

## The Stage-Gate Principle: Separate Work from Authorization

### 2.1 Four distinct layers

A reliable agentic workflow separates four functions. **Execution** produces an artifact; **validation** tests schema, arithmetic, consistency, and other machine-checkable properties; **assurance** challenges the substantive reasoning and evidence; and **authorization** grants permission for an external effect. These functions can run in the same application, but they should not be silently collapsed into one successful model message.

For example, a vendor-comparison report may pass formatting and arithmetic checks while using an obsolete product description. An independent reviewer could flag that weakness without having permission to approve a procurement decision. A human could approve the report for internal discussion without authorizing contact with a supplier. The gates must represent those outcomes as different states. Table 1 separates the four kinds of control and what each must not be taken to imply.

TABLE Four kinds of controls. || A workflow may have more than one controller at a gate; each controller retains a distinct responsibility.
| Layer | Typical controller | What it tests or decides | What it must not imply |
| Technical validation | Schema validator, code, test harness | Required fields, types, totals, links, task completeness | Evidence is necessarily true |
| Substantive assurance | Independent reviewer, domain expert | Provenance, assumptions, risks, contradictions, recommendation logic | Final authority to commit resources |
| Risk and policy control | Access-control service, rule engine, risk owner | Data classification, allowed destinations, tool scopes | A model's confidence is permission |
| External authorization | Named accountable human or delegated policy owner | Whether an action may be taken now | Permission for later or different actions |

### 2.2 Why one model's self-review is insufficient

Reviewing the same output with the same evidence and nearly identical prompts can yield correlated mistakes. A stronger assurance step uses **different tests**: a source-retrieval check rather than another summary; arithmetic recomputation rather than agreement with a narrative; a policy service rather than a model-authored approval sentence; or an accountable human for a high-impact release. Use evaluator agents as *assistance to assurance*, not as proof of independent correctness. As a design recommendation, traces should record which reviewer, tests, source set, and version supported each gate result; the OpenAI Agents SDK already traces guardrail checks as spans [@r7].

## State Machine and Gate Contract

### 3.1 A gate is a state transition, not a suggestion

The controller should track a workflow as structured state, not reconstruct the entire history from chat text. A useful state model includes run ID, stage, artifact version, evidence manifest, gate ID, gate result, issue list, attempt count, approval scope, deadline, and event log. The **artifact version** matters: approval of draft v2 must not silently authorize delivery of edited draft v3.

A gate evaluates a specific artifact and returns a **machine-readable decision record**. Example fields include decision, criteria results, severity, required rework, reviewer identity, evidence references, expiry time, and a signature or record ID. This record is stored separately from the agent's explanation. The platform—not the language model—enforces whether a transition is allowed. Table 2 gives the recommended meaning of each gate result.

TABLE Recommended gate-result semantics. || A real system may add CANCELLED, EXPIRED, or SUPERSEDED states, but it should never treat an unknown decision as PASS.
| Gate result | Meaning | Permitted next step | Control requirement |
| PASS | All mandatory criteria satisfied | Advance to the authorized next stage | Bind decision to artifact version |
| REWORK | Correctable deficiency identified | Return to named owner with explicit defect list | Bound retry count and time budget |
| ESCALATE | Ambiguous or high-impact issue | Pause for accountable reviewer or policy owner | Durable checkpoint; authenticated reviewer |
| STOP | Prohibited or unrecoverable condition | End or quarantine the run | Preserve evidence; block side effects |

### 3.2 Three acceptance criteria, three different mechanisms

A gate specification should distinguish **hard predicates** (e.g., every mandatory vendor field is populated), **evidence-based judgments** (e.g., a migration risk is adequately supported), and **discretionary authorization** (e.g., a client-facing report may be sent). Hard predicates belong in code when possible; OpenAI's guardrails, for example, halt a run by raising a tripwire exception when a check fails [@r6]. Evidence judgments should reference an explicit rubric and source manifest. Authorization belongs to a named user, a role-backed workflow service, or a separately approved policy; a reviewer agent cannot grant itself new privileges.

AWS Step Functions describes Choice routing, retry/catch behavior, and explicit error handling. These conventional workflow concepts remain useful for agentic designs: an undefined choice branch, unhandled timeout, or unbounded retry is an application defect, regardless of how capable the agent appears [@r8, @r9].

## A Five-Gate Reference Architecture

The proposed design uses **G0 Intake, G1 Evidence, G2 Analysis, G3 Assurance, and G4 Release**. Each gate is placed where a wrong assumption would otherwise become more expensive to correct. Between gates, agents may execute sequentially or concurrently, depending on dependencies. Figure 1 shows the required distinction between the forward PASS path and the backward REWORK path.

FIG fig1-gates || The five-gate reference pattern. The figure plays through each gate in turn: the artifact advances on PASS, returns to the stage that owns the defect on REWORK, pauses for an accountable person on ESCALATE, and is quarantined on STOP; select a gate to jump to it, or <em>All gates</em> to see the five side by side. The gate is a policy-enforced transition, not simply the reply of a reviewer agent. || Five gates in a row, G0 intake, G1 evidence, G2 analysis, G3 assurance and G4 release, with a controller above, a versioned artifact store below, a reviewer beside the last gate, and each gate shown with what it checks, what it hands on and how it fails. || 

### G0 — Intake and scope acceptance

Before research begins, verify the request's owner, objective, success criteria, source restrictions, deadline, data sensitivity, permitted tools, and forbidden actions. Ambiguous project scope is a rework item; an unauthorized request for client information is a STOP or policy escalation. **Output:** signed-off scope and an execution contract.

### G1 — Evidence sufficiency

Research agents may fan out to gather sources, but G1 requires provenance, publication dates, conflicting evidence, and unresolved gaps. Missing mandatory evidence blocks claims that depend on it. G1 may ask a specific research branch to repeat a source check while retaining completed independent branches. **Output:** evidence pack, assumptions register, source manifest, and explicit unknowns.

### G2 — Analytical validity

Analysis and drafting are evaluated for consistent assumptions, reproducible calculations, supported comparisons, and transparent treatment of unknowns. Numerical totals should be recomputed by code where practical. G2 does not approve the business recommendation; it establishes that the analysis is sufficiently coherent and inspectable to merit assurance. **Output:** validated analysis package or itemized defects.

### G3 — Independent assurance

A reviewer agent or expert evaluates contrary evidence, alternative interpretations, security, methodological limitations, material omissions, and alignment with the original scope. A single serious unresolved defect can block release even when an average quality score appears high. **Output:** accepted artifact version, residual-risk register, and independent review record.

### G4 — Human-authorized release

The final stage checks who is permitted to send, publish, purchase, change a record, or operate an external system. Human approval is required when the task or policy calls for it. The approval must identify the exact action, destination, payload/version, reviewer, and validity period. G4 can authorize publication of a report without authorizing any recommendations in that report to be executed automatically. **Output:** released artifact and auditable authorization receipt.

## Feedback Loops: Bounded Rework, Not Infinite Self-Correction

### 5.1 Targeted repair beats restarting the entire workflow

If a source is missing at G1, rerun the affected research branch rather than restarting every agent. If G2 finds arithmetic inconsistency, return the incorrect calculations and affected downstream sections for regeneration. If G3 identifies a new scope issue, the correct destination may be G0 rather than G2. This requires a **dependency-aware invalidation rule**: when an upstream fact changes, every downstream artifact depending on that fact is marked stale and must be revalidated.

A meaningful feedback message states the failed criterion, severity, failing evidence, target owner, requested correction, and re-evaluation deadline. “Improve the answer” is not a satisfactory rework contract because the next attempt cannot know whether the defect was resolved.

### 5.2 Bound the loop at three levels

An agentic stage-gate loop should have **(1) a maximum revision count, (2) a time or token/cost budget, and (3) an escalation or stop condition**. Google ADK's loop-workflow guidance explicitly provides iteration limits and ways to terminate a repeating agent workflow; AWS's retry policies use bounded attempts and backoff for recoverable errors [@r10, @r9]. Retries for network timeouts and revisions for factual defects should be separate counters and policies.

For example, permit up to **two revisions after the initial draft**, not two indefinite cycles per reviewer. If the same material defect remains, escalate to a human or stop the run with an incomplete-result disclosure. A new prompt phrasing is not, by itself, new evidence. High-severity policy breaches, source fabrication, prohibited tool calls, or uncertain external side effects may demand immediate STOP rather than another model attempt.

### 5.3 Rework and external side effects

Approval to send a message, modify a database, or trigger purchasing is not proof that the action occurred exactly once. A resumed workflow can re-enter a previously approved tool path after a crash. Use destination-side idempotency keys where available, persist action receipts, and reconcile ambiguous outcomes before retrying. OpenAI's human-in-the-loop guidance explicitly warns that approved consequential actions can be duplicated after crash recovery without such protections [@r4].

## Combining Gates with Sequential and Parallel Execution

Stage gates can guard **sequential chains** between each dependent task, or they can sit at **fan-in barriers** where concurrent branches are reconciled. In a series–parallel arrangement, the common pattern is intake → G0 → parallel investigation → G1 → synthesis → G2 → assurance → G3 → G4. In a parallel–series arrangement, each specialist lane can have internal checks while one shared cross-lane gate verifies that assumptions and evidence are compatible.

The most important design choice is whether a gate has **ALL**, **CONDITIONAL**, or **QUORUM** joining semantics. A financial risk check may be mandatory even if four other branches are complete; a noncritical appendix may be omitted with an explicit warning. A quorum is appropriate only when the task's risk policy allows it. Treating “three out of four agents agreed” as sufficient evidence can be especially misleading when the agents share prompts or sources. Table 3 sets out where gates naturally sit in each execution pattern.

Gate placement also follows the cost of late discovery. A defect found at G1 costs one research branch; the same defect found at G4 can invalidate the evidence pack, the analysis, the draft and the review record, and may already have consumed a reviewer's time. A practical rule is to place a gate immediately before any step whose output many later steps depend on, and immediately before any step that is expensive or impossible to undo. Conversely, a gate between two cheap, reversible steps mostly adds latency, and its checks can usually move to the next gate without loss.

TABLE Gate placement in each execution pattern. || Stage gates are composable with execution patterns; their placement depends on the type of error and the cost of discovering it late.
| Workflow pattern | Natural gate placement | Common failure | Suggested mitigation |
| Sequential | Every significant handoff | An early factual error spreads through all later stages | Versioned outputs and upstream-source validation |
| Parallel | Fan-in / aggregation point | Fast branches mask one missing or stale result | Mandatory-branch manifest and timeout policy |
| Series–parallel | End of each major stage | Barrier waits forever for a stalled branch | Deadline, fallback, and explicit incomplete-state routing |
| Parallel–series | Within each lane and at final merge | Specialist lanes use incompatible assumptions | Shared scope baseline and cross-lane consistency gate |
| Iterative stage-gate | After an artifact is produced | Reviewer/revision loop never converges | Revision budget, changed-evidence requirement, escalation |

## Worked Example: A Hypothetical SME WMS Recommendation

Consider a fictional Vancouver distributor evaluating warehouse-management software. The requested deliverable is a **shortlist recommendation with integration, bilingual-operation, and cost considerations**. No actual client details, private vendor records, or procurement authority are assumed. The workflow uses specialists for process mapping, vendor research, integration analysis, commercial modeling, writing, and independent review.

At G0, the intake agent records five mandatory decision criteria: functional fit, accounting integration, bilingual usability, total cost, and implementation support. At G1, the research bundle lists product claims and provenance. At G2, the analyst checks normalized cost assumptions and the consistency of evaluation weights. At G3, the reviewer searches for unsupported assertions and conflicting findings. At G4, the named human approves only the **distribution of a draft advisory report**, not supplier selection or a purchase order.

### 7.1 A revision loop with a withheld claim

Assume an initial draft contains **24 material claims**: 20 have acceptable support, four do not. The G3 gate rejects the draft because the publication policy requires all material claims to be sourced or explicitly identified as unverified. After one targeted research-and-draft revision, **23 claims** have acceptable support, while the remaining claim cannot be substantiated. The unsupported claim is **removed or disclosed as unknown**, not carried into the final recommendation as fact (Figure 2). The published set consequently contains 23 supported material claims; the record retains the excluded question for follow-up.

FIG fig2-claim-rework || A targeted evidence rework at G3 (illustrative, not measured performance). An assumed 24-claim draft moves from 20 of 24 claims supported to 23 of 24 after one revision; the final report excludes the last unverified claim. PASS applies to the included claims and all other mandatory criteria, not to an average score. || Three panels left to right: draft version 1 with 20 of 24 claims supported and a G3 fail, revised version 2 with 23 of 24 supported and a G3 hold, and the final candidate with 23 of 23 supported and a G3 pass, above a review-logic strip leading to a separate human release gate. || 

### 7.2 Example gate register

TABLE Illustrative WMS gate register. || Actual thresholds, review roles, and evidence standards must be defined for the specific project.
| Gate | Example acceptance condition | Outcome if unmet | Who owns resolution |
| G0 Intake | Mandatory objectives and constraints confirmed | Return to sponsor for scope correction | Planner / sponsor |
| G1 Evidence | Mandatory product and integration assertions have dated sources | Targeted research rework or explicit exclusion | Research agent |
| G2 Analysis | Cost assumptions, comparison weights and arithmetic validated | Recompute affected outputs and invalidate dependent draft sections | Analyst agent |
| G3 Assurance | No unsupported material claim in the publishable text; high-severity risks disclosed | Revise with issue list; escalate unresolved material items | Independent reviewer |
| G4 Release | Named authorized human approves exact report version and destination | Hold publication; no external action | Accountable human |

Table 4 records the acceptance condition, outcome and owner at each gate. The example illustrates why a gate should be **defect-driven rather than score-driven**. A report with excellent wording and 96% supported claims may still be inappropriate if the missing 4% concerns migration feasibility or a binding commercial commitment. The workflow must preserve the excluded assertion as an open issue rather than quietly inventing a workaround.

## Reliability and Performance Engineering

### 8.1 The cost of rejected work

If stage *i* has execution cost *c*<sub>i</sub> per attempt and gate cost *g*<sub>i</sub> per evaluation, with *a*<sub>i</sub> attempts and *e*<sub>i</sub> evaluations, a simple accounting identity is Eq. (1), where *C*<sub>human</sub> is review time and *C*<sub>shared</sub> shared infrastructure:

TEX C_{\text{total}} = \sum_i \left( c_i a_i + g_i e_i \right) + C_{\text{human}} + C_{\text{shared}}

It is a cost ledger, not a predictive law: tokens, tool calls, human time, and infrastructure should be measured separately. A gate can increase per-run latency but **reduce cost per accepted deliverable** if it prevents costly downstream rework or incorrect external actions.

A useful scenario calculation treats each independent validation attempt as having probability p of success. If there are *m* total attempts, the probability of at least one pass is Eq. (2):

TEX P_{\text{pass}} = 1 - (1 - p)^m

At *p* = 0.75 and *m* = 3, Eq. (2) gives 98.44%. **This is not a real-world agent reliability estimate.** Attempts after feedback are rarely independent, and a gate that falsely accepts bad work invalidates the assumed probability. The calculation is useful mainly for explaining why retries alone cannot substitute for better evidence and test design.

### 8.2 Operational metrics

Measure (a) **first-pass acceptance rate**; (b) **accepted artifact rate**; (c) **false-pass rate** measured against independent adjudication; (d) **revisions per accepted artifact**; (e) **gate dwell time**; (f) **time and cost per accepted artifact**; (g) **high-severity escape count**; and (h) **number of actions executed without valid authorization**. The last two should normally have zero-tolerance or risk-governed thresholds. OpenAI tracing records model generations, tool calls, handoffs, and guardrail events; equivalent instrumentation should correlate every gate result with the relevant run and artifact versions [@r7].

False-pass rate deserves particular attention because it cannot be read from the workflow's own logs. It requires a sample of accepted artifacts to be re-examined by an adjudicator who took no part in the run, using the same rubric and source set. A small regular sample, stratified by gate and by task type, is usually enough to show whether a gate is drifting toward rubber-stamping or toward excessive rejection, and it gives the team evidence for tightening or relaxing a rubric instead of relying on impressions.

Be careful with a misleading optimization target: increasing the pass rate by weakening the rubric can make the metric look better while worsening the system. Similarly, a high rejection rate can signal either poor upstream quality **or** a miscalibrated reviewer. Compare gate decisions with independent case reviews, not only with downstream model satisfaction.

## Security, Governance, and Human Oversight

Stage gates become security boundaries only when a **separate enforcement component** controls execution. A prompt that tells an agent not to send data is not an access-control rule. The tool adapter must enforce an allowlist of destinations, per-agent credentials, least privilege, and approval requirements. OWASP's Excessive Agency guidance identifies excessive functionality, permissions, and autonomy as core pathways to agentic harm; NIST's AI Risk Management Framework provides a wider govern–map–measure–manage context for risk controls [@r11, @r12].

**Prompt-injection risk** grows when research agents consume websites, tickets, retrieved documents, and prior agent messages. Treat all source content and peer outputs as potentially untrusted. Never allow a retrieved instruction to redefine G4 authority, rewrite the permitted tool list, or suppress an issue from the audit record. Store the decision policy outside editable agent context. OWASP also documents how malicious instructions embedded in data can redirect model behavior [@r13].

A safe human-in-the-loop process authenticates the reviewer, verifies their authority for **that particular action**, displays the exact payload and supporting evidence, records the decision, and resumes only the authorized transition. Durable pause/resume facilities exist in LangGraph, Microsoft Agent Framework, and OpenAI's Agents SDK, but applications still need to protect serialized state and guard against replay and duplicated side effects [@r3, @r4, @r14]; approval expiry is an additional application-level control. **Approval of a report is not approval of the actions recommended inside it.**

## Engineering Blueprint: A Bounded Gate Controller

The pseudocode in Example 1 is intentionally framework-neutral. It shows the control structure, not a production-ready authorization or durable-transaction implementation. In deployment, state transitions and side-effect receipts must be stored durably, with a concurrency-safe claim on each pending approval.

CODE gate || Example 1. Framework-neutral gate controller with bounded rework, escalation to a durable waiting state, and a separate release authorization.

A minimal implementation also needs timeout handling, cancellation, locking, exception classification, artifact storage, reviewer authentication, resource quotas, data-retention rules, and a test suite covering every transition. The **ESCALATE branch returns to a durable waiting state**. A separate authenticated event handler must verify reviewer identity, permission scope, artifact version, approval expiry, and disposition before resuming the run; it must never turn reviewer acceptance into a waiver of hard validation failures. The pseudocode illustrates state separation but does not implement the full storage and event infrastructure [@r4, @r8, @r9].

## Failure Modes and Engineering Checklist

TABLE Failure-mode register for stage-gated multi-agent systems. || Controls are engineering recommendations; effectiveness must be tested in the deployed environment.
| Failure mode | Observable symptom | Proposed control |
| Infinite reviewer–writer loop | Same issue repeats with growing token spend | Max revisions; convergence check; escalation |
| Rubber-stamp gate | Near-universal passes, unsupported claims remain | Independent adjudication and adversarial evaluations |
| Stale approval | Draft modified after reviewer signs off | Bind approval to version/hash and destination |
| Gate bypass | Tool sends content before final authorization | Policy enforcement at tool/service boundary |
| Cascading invalidation | Revised assumption leaves downstream sections unchanged | Dependency ledger and downstream revalidation |
| Parallel partial success | Merge presents incomplete branch output as full result | Explicit required-branch join policy |
| Approval replay / duplicate effect | Message or transaction occurs twice after restore | Destination idempotency and authoritative reconciliation |
| Evidence injection | Source text changes routing or tool permissions | Trusted/untrusted separation; allowlists; least privilege |

Table 5 lists the failure modes to rehearse before release. **Implementation checklist.** Define success criteria before agent roles; publish a gate register; distinguish quality checks from authorization; require artifact versions and provenance; route defects to owners; bound revision attempts and cost; add durable checkpoints; validate negative branches and timeouts; secure all tool permissions independently of prompts; and monitor **cost per accepted artifact** rather than only response time. Before enabling any external action, test the exact failure path after approval but before completion logging.

### Where a stage gate is not warranted

Not every small task needs five gates. A read-only classification or low-risk draft may be better handled by a single agent and a deterministic validator. Gates impose latency, storage, and review cost, and poor rubrics can create false confidence. Use the smallest set that addresses **material failure consequences**; add controls when uncertainty, impact, regulation, or external side effects demand them. Framework capabilities should not drive governance complexity by default [@r2].

## Conclusion

A well-engineered multi-agent system should not treat “task completed” as equivalent to “result accepted.” Stage-gate orchestration adds explicit acceptance criteria, versioned artifacts, targeted rework, stopping rules, independent assurance, and human authorization to otherwise ordinary execution graphs. It is particularly valuable when agent outputs become the basis for advisory recommendations, technical decisions, or external actions.

The design principle is **assurance by evidence and enforceable transitions, not by agent agreement**. Keep retries bounded; distinguish a failed quality test from a transient tool failure; make escalation an expected outcome rather than a system embarrassment; and ensure that approval of a document never silently authorizes operational side effects. A companion paper applies these principles to a concrete **Research → Analyze → Draft → Review → Finalize** workflow [@a9].
"""
