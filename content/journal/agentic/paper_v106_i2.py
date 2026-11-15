"""Chmltech Online Journal, Vol. 106, Issue 2: Research, Analyze, Draft, Review, Finalize (draft, Nov 14 2026).

Series: Multi-Agent AI Engineering, article 9. Figure 1 is interactive (content/journal/live/rad5.html, drawn by figure-scripts/rad5.py)."""

SLUG = "research-analyze-draft-review-finalize-engineering-a-reliable-five-agent-ai-workflow"
META = dict(
    volume=106, issue=2,
    title="Research, Analyze, Draft, Review, Finalize: Engineering a Reliable Five-Agent AI Workflow",
    short_title="Research to Finalize: A Five-Agent AI Workflow",
    meta="A controlled five-agent AI workflow for research, analysis, drafting, independent review and approved release, with source tracking and an SME example.",
    keywords=["multi-agent AI", "research automation", "evidence provenance", "LLM orchestration", "structured handoff", "quality assurance", "human-in-the-loop", "digital adoption planning"],
)
ABSTRACT = 'Research-intensive advisory work depends on a sequence of transformations: raw information becomes evidence, evidence becomes analysis, analysis becomes a draft, and a reviewed draft becomes an authorized deliverable. Large language model (LLM) agents can assist at each transition, but separating work into five named agents does not itself establish accuracy. This paper develops Research → Analyze → Draft → Review → Finalize (RADRF) as a controlled multi-agent workflow for technical reporting, business consulting, digital adoption planning and other evidence-led tasks. It defines responsibilities, handoff contracts, source provenance, state transitions, quality gates, retry boundaries and release permissions. A hypothetical Canadian small and medium-sized enterprise (SME) Digital Adoption Plan shows how the system should distinguish supplied facts from assumptions, verify financial calculations, challenge unsupported recommendations and preserve human accountability. The proposed architecture treats source references, versioned artifacts, independent tests and authorization records as core workflow data, not optional additions to a chat transcript. The paper argues for specialized agents only when the expected benefits of separation outweigh coordination, evaluation and operating costs.'

REFS = {
    'r1': ('Lee, Q. F. (2026). Multi-agent AI systems: Architectures, coordination patterns and failure modes. <em>Chmltech Online Journal</em>, 104(2).',
           'https://www.chmltech.com/post/multi-agent-ai-systems-architectures-coordination-and-failure-modes'),
    'a1': ('Lee, Q. F. (2026). Multi-agent AI orchestration architectures: Five coordination models compared. <em>Chmltech Online Journal</em>, 106(1).',
           'https://www.chmltech.com/post/multi-agent-ai-orchestration-architectures-five-coordination-models-compared'),
    'r2': ('Schluntz, E., &amp; Zhang, B. (2024, December 19). <em>Building effective agents</em>. Anthropic.',
           'https://www.anthropic.com/research/building-effective-agents'),
    'r3': ('Microsoft. (2026). <em>Microsoft Agent Framework: Workflows</em>. Microsoft Learn.',
           'https://learn.microsoft.com/en-us/agent-framework/journey/workflows'),
    'r4': ('Microsoft. (2026). <em>Microsoft Agent Framework workflows: Handoff orchestration</em>. Microsoft Learn.',
           'https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff'),
    'r5': ('LangChain. (n.d.). <em>LangGraph: Persistence</em>.',
           'https://docs.langchain.com/oss/python/langgraph/persistence'),
    'r6': ('OWASP. (2025). <em>LLM01:2025 Prompt injection</em>. OWASP Top 10 for LLM Applications.',
           'https://genai.owasp.org/llmrisk/llm01-prompt-injection/'),
    'r7': ('OpenAI. (n.d.). <em>Guardrails — OpenAI Agents SDK</em>.',
           'https://openai.github.io/openai-agents-python/guardrails/'),
    'r8': ('OpenAI. (n.d.). <em>Human-in-the-loop — OpenAI Agents SDK</em>.',
           'https://openai.github.io/openai-agents-python/human_in_the_loop/'),
    'r9': ('OpenAI. (n.d.). <em>Tracing — OpenAI Agents SDK</em>.',
           'https://openai.github.io/openai-agents-python/tracing/'),
    'r10': ('National Institute of Standards and Technology. (2023). <em>Artificial Intelligence Risk Management Framework (AI RMF 1.0)</em> (NIST AI 100-1).',
           'https://www.nist.gov/itl/ai-risk-management-framework'),
    'r11': ('OpenAI. (n.d.). <em>Building agents</em>. OpenAI Developers.',
           'https://developers.openai.com/tracks/building-agents'),
    'r12': ('OpenAI. (n.d.). <em>Handoffs — OpenAI Agents SDK</em>.',
           'https://openai.github.io/openai-agents-python/handoffs/'),
    'r13': ('Grace, M., Hadfield, J., Olivares, R., &amp; De Jonghe, J. (2026, January 9). <em>Demystifying evals for AI agents</em>. Anthropic.',
           'https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents'),
    'r14': ('OWASP. (2025). <em>LLM06:2025 Excessive agency</em>. OWASP Top 10 for LLM Applications.',
           'https://genai.owasp.org/llmrisk/llm062025-excessive-agency/'),
}

BODY = r"""
## Introduction: From a Prompt to an Accountable Deliverable

A single prompt may be able to produce a plausible business report. Yet professional use asks harder questions: Which sources support the important claims? Did the analysis distinguish observations from assumptions? Were figures recomputed rather than accepted from a narrative? What changed between the reviewed version and the released one? Who authorized release, and was sending the document within the permitted scope? These questions concern **the workflow around an LLM**, not simply its writing ability.

A five-stage **Research → Analyze → Draft → Review → Finalize** pattern makes those responsibilities visible (Figure 1). The Research Agent collects and qualifies material; the Analysis Agent interprets it; the Drafting Agent communicates the findings; the Reviewer Agent tests them; and the Finalization Agent resolves accepted changes and packages the approved artifact. A workflow controller—not an agent's self-description—owns state transitions, resource limits, and authorization. An earlier paper in this journal identified structured handoffs, externally grounded verification, and bounded loops as important design practices [@r1], and its companion compared the orchestration models within which such a workflow can run [@a1].

This pattern should not be confused with proof that five separate models are necessary. Several roles could be bounded calls to the same model, and deterministic validators may perform many review checks more reliably. Anthropic distinguishes predefined **workflows** from systems where agents dynamically choose how to act and recommends beginning with the simplest approach that meets the task [@r2]. The five-agent design is justified where auditability, distinct skills or tools, independent checks, and artifact ownership offer practical value. OpenAI likewise describes orchestration as management of multi-step tool use, handoffs, guardrails, and context, not a requirement to multiply agents [@r11].

**Scope and status.** This paper proposes an engineering reference workflow, not a validated benchmark or mandatory industry standard. Its SME example is entirely illustrative: it does not describe a particular client, actual measured savings, or approval under any government funding program.

## Architecture: Five Specialized Roles, One Accountable Controller

The orchestrator receives the business objective, checks constraints and permissions, assigns work, and decides when an artifact may advance. Agents execute bounded tasks with role-specific inputs, tool access, and expected outputs. A shared, access-controlled workspace stores sources, claim records, analysis files, review findings, and version history. Agents should not infer that a previous role's polished narrative is correct merely because it appears in shared memory. Table 1 sets out each stage's responsibility, inputs, output and advancement condition.

TABLE Five-agent responsibility and handoff matrix. || The gates are proposed engineering controls; actual thresholds depend on the task's risk and context.
| Stage | Primary responsibility | Required input | Controlled output | Advancement condition |
| Research | Find, classify, date, and verify source material | Scope, source policy, document set | Evidence manifest and fact register | Required source categories covered; unknowns identified |
| Analyze | Derive findings, test alternatives, quantify trade-offs | Versioned evidence, assumptions | Analysis workbook, insight and assumption register | Methods and critical calculations reproducible |
| Draft | Translate supported findings into a readable deliverable | Accepted analysis, audience, template | Versioned draft with claim references | Material claims linked to evidence or labeled inference |
| Review | Challenge accuracy, completeness, risks, and limitations | Draft, sources, analysis, review rubric | Issue register and decision: pass, rework, escalate, stop | No unresolved blocking issue; review independent enough for risk |
| Finalize | Incorporate authorized edits, lock version, prepare release | Reviewed draft, resolved issues, release permissions | Final artifact and change log | Exact artifact approved for specified destination/action |

FIG fig1-workflow || The Research → Analyze → Draft → Review → Finalize workflow. The figure plays through each stage in turn, showing the artifact moving between the controller, the stage agents and the shared workspace, including a targeted rework from Review to Analyze; select a stage to jump to it, or <em>All stages</em> to see the five side by side. Agents never approve their own work: the controller owns every transition. || Five stage agents in a row under a controller, with a shared versioned workspace below and an approver beside the controller; each stage is shown with its responsibility, output, gate and main failure to watch. || 

### 2.1 Control topology versus stage order

A sequential *logical dependency* does not require all work to be serial. Research can fan out to independent source investigators, then join at an evidence gate. Analysis may run alternative options concurrently, and the reviewer may perform source, numerical, and privacy checks in parallel. The **five-stage order** describes the maturity of the artifact; the **execution graph** determines which subtasks can run concurrently. Microsoft Agent Framework documents sequential, concurrent, and handoff orchestrations, with important differences between retaining central ownership and transferring it to another agent [@r3, @r4]. OpenAI documents a similar distinction between transferring control through a handoff and invoking a specialist as a bounded tool [@r12].

### 2.2 Identity, memory, and ownership

The controller owns the case identifier, artifact versions, work queue, approved tool set, and durable state. Individual agents own bounded deliverables, not the whole application. Short-term context can hold current work, while a knowledge store retains approved evidence and reusable templates. The storage mechanism must distinguish **retrievable information** from **instructions with authority**; storing source text does not elevate it to system policy. LangGraph's documented separation between checkpointed thread state and long-term stores illustrates this architectural distinction [@r5].

## Research: Build an Evidence Pack, Not a Pile of Links

The Research Agent begins by turning an ambiguous request into a documented research plan. The plan identifies the subject, audience, jurisdiction, decision horizon, evidence cutoff date, required inputs, confidentiality limits, and explicitly excluded tasks. If a required client document is unavailable, the research state must report that gap rather than invent the missing process data.

A useful evidence register records a **source ID**, precise locator, source owner, publication or measurement date, retrieval date, source type, relevant excerpt or finding, permitted use, confidence notes, and claims to which it relates. Distinguish four categories: (i) **client-supplied assertions** not yet independently verified; (ii) **observations** such as system exports or timed process measurements; (iii) **external primary evidence** such as vendor documentation or official specifications; and (iv) **inferences and assumptions** introduced by the analytical team. The category should travel with the fact through later stages, and it determines how the report may phrase the fact (Table 2).

TABLE Evidence-status language. || A source register helps downstream agents keep evidence, assertion and modeled assumption apart.
| Evidence class | Example in an SME systems assessment | Appropriate language in the report | Verification needed |
| Observed / measured | A dated order export shows duplicate entry events | “In the sampled export…” | Reproduce sampling method and confirm system timestamps |
| Client-reported | Operations manager estimates 19 hours/week of manual reconciliation | “Management estimates…” | Time study or representative sample before claiming actual savings |
| Vendor-stated | Product documentation lists an accounting connector | “Vendor documentation states…” | Verify edition, supported direction, current API, and contract limits |
| Analyst assumption | Automation captures 70% of avoidable effort | “Under a 70% realization scenario…” | Sensitivity analysis and pilot validation |

A source is not validated merely because it has a URL. The researcher checks the authoritative issuer, recency, applicability, contradictory statements, and whether the cited source actually supports the proposition. The output is a **source pack plus an exception list**: missing data, unresolved differences, and facts that must not be represented as established. The Research gate should reject an evidence pack that lacks mandatory inputs or contains undocumented access to restricted material.

### 3.1 Defend the evidence boundary

External pages, attachments, and retrieved passages are **untrusted data**, not instructions to the system. A page could contain text telling an agent to disregard prior rules or send confidential files. OWASP describes this as indirect prompt injection and notes that retrieval-augmented generation does not, by itself, solve the problem [@r6]. Research agents should receive read-only tools where possible. Downloaded content must not grant write permissions, change destinations, or rewrite the scope contract.

## Analyze: Turn Evidence into Reproducible Reasoning

The Analysis Agent transforms the evidence pack into hypotheses, causal explanations, option comparisons, calculations, and decision-relevant findings. A responsible analysis maintains three separate layers: **inputs** (observed or reported values), **methods** (formulas, assumptions, model choices), and **conclusions** (inferences conditional on those inputs and methods). If the numbers are important, a spreadsheet or calculation script should generate them instead of relying exclusively on a text-only answer.

For process improvement, the agent could map the current-state quote-to-cash flow, identify duplicated data entry, quantify handoffs, and evaluate both software integration and process standardization. For software selection, it could construct a requirements-to-feature matrix, mark vendor evidence quality, weigh implementation complexity, and calculate total cost of ownership. Alternatives should include the possibility that **no additional AI agent or software product is justified**.

A simple annual benefit model is given by Eq. (1):

EQ V<sub>gross</sub> = H<sub>w</sub> × W<sub>y</sub> × C<sub>h</sub> × ρ

where <em>V</em><sub>gross</sub> is the annual gross time-value, <em>H</em><sub>w</sub> the hours saved per week, <em>W</em><sub>y</sub> the productive weeks per year, <em>C</em><sub>h</sub> the loaded labour cost per hour and <em>ρ</em> the realization factor.

The **realization factor** is a scenario assumption, not a measured prediction. Annual net operating benefit is gross time-value less incremental annual recurring costs <em>C</em><sub>r</sub>; first-year net benefit also deducts one-time implementation spending <em>C</em><sub>1</sub>, as in Eq. (2).

EQ V<sub>net,1</sub> = V<sub>gross</sub> − C<sub>r</sub> − C<sub>1</sub>

Any claim of cash savings requires an additional test: released staff capacity is not automatically a reduction in payroll expense. A better description may be *capacity value* or *opportunity for redeployment* until finance validates the benefit mechanism.

### 4.1 Analytical acceptance tests

At a minimum, (a) every material input has a provenance record, (b) formulas and units reconcile, (c) options use a consistent decision horizon, (d) uncertainty is explicitly represented, and (e) conclusions do not exceed the strength of the evidence. If the inputs change, the controller should invalidate dependent analysis and drafts. The agent may propose a recommendation, but it cannot make an unmeasured scenario into an observed result.

## Draft: Communicate Findings Without Laundering Uncertainty

The Drafting Agent takes **accepted analysis**, not all available chat history, as its controlled input. It receives the intended audience, required sections, citation style, confidentiality designation, and document template. Its principal responsibility is to communicate findings coherently while retaining evidence status, caveats, alternatives, and required actions.

A defensible advisory report should distinguish what the organization currently does, what it wants to achieve, what was established from data, what remains uncertain, and what action is recommended subject to approval. That distinction is often lost when a drafting agent optimizes only for fluency. One solution is a **claim ledger**: each material statement is assigned a claim ID, linked source/analysis IDs, a status such as supported, qualified, inference, or unverified, and an owner. A draft can cite CLAIM-014 internally even if the client-facing document renders a conventional footnote.

The agent must not manufacture references, add numerical precision unsupported by inputs, or substitute generic vendor descriptions for a verified requirements assessment. A well-written executive summary should identify unresolved issues rather than conceal them in an appendix. If the draft cannot support a critical claim, it should label it as a hypothesis, remove it, or route the gap to Research or Analyze.

## Review: Independent Challenge, Not Cosmetic Editing

Review is a distinct **assurance function**. The Reviewer Agent checks the draft against the original scope and the underlying source pack, not simply against its own preferred wording. A strong review uses methods different from the methods that generated the output: re-fetching a source, recomputing a calculation, comparing figures against a structured data file, validating against a known schema, and checking permissions. An LLM reviewer can prioritize and explain problems, but should not replace deterministic tests or a qualified reviewer for consequential decisions.

Table 3 shows how typical defects are routed. A practical rubric scores evidence fidelity, analytical correctness, factual completeness, instruction/scope compliance, communication quality, and privacy/security. **Blocking defects are not averaged away**. A mathematically correct business case with one prohibited disclosure is not acceptable because the other categories scored highly.

TABLE Defect classification and targeted rework. || Human approval remains separate from automated quality assessment.
| Review class | Example failure | Corrective route | Release impact |
| Evidence | A WMS integration feature lacks vendor-primary confirmation | Return specific claim to Research | Block that claim or qualify it |
| Analysis | Labour benefit uses 52 weeks but the input assumes 50 | Return calculation to Analyze; invalidate downstream figures | Block affected recommendation |
| Document | Executive summary contradicts the financial table | Return to Draft with source-of-truth data | Block until reconciled |
| Confidentiality | Draft includes client-identifiable detail without authorization | Quarantine/redact; escalate to owner | Stop external release |
| Authorization | Reviewer requests sending the report without approval | Pause for designated approver | No sending or publishing |

The reviewer records issues with severity, source reference, affected artifact version, owner, and reproducible acceptance condition. A PASS means the required checks have succeeded for a **specific version**. REWORK returns actionable defects to named stages. ESCALATE pauses for a human decision, and STOP ends or quarantines prohibited work. Agent runtimes provide guardrail and approval primitives, but these have documented coverage limits (for example, tool guardrails do not apply to handoffs), so their presence alone does not ensure a policy is enforced correctly [@r7, @r8].

## Finalize: Version Locking, Approval, and Release

The Finalization Agent implements approved edits, checks that reviewer issues are resolved, and assembles the final document, exhibits, assumptions register, and source inventory. It should provide a **change summary** from the reviewed draft to the release candidate. Material edits invalidate prior approval if they affect claims, calculations, recommendations, destinations, or sensitive information.

The **authorization gate** is separate from the quality gate. A report may be suitable for internal review but not authorized for an external email, website publication, purchase order, or system change. The approved action record should bind the exact artifact/version (preferably a file hash), destination, approver identity, permissions, and validity window. The application controls delivery; a model should not be able to assert “approved” merely by emitting that word. Figure 2 shows how each stage's artifact, gate and rework path fit together.

FIG fig2-artifact-architecture || Artifact-led architecture. Each stage produces a versioned artifact and passes a gate (G0 scope to G4 authority); review sends defects back to the stage that owns them rather than restarting the run. The bottom band lists the cross-cutting controls: source provenance, structured handoff, durable workflow and release control. || Five colored stage boxes from Research to Finalize, each naming its output artifact and gate, a dashed rework arrow from Review back to Analyze, and a band of four cross-cutting controls below. || 

After release, the system retains a versioned manifest, sources allowed by the retention policy, review evidence, and permitted traces. Sensitive input should not be reproduced unnecessarily in logs or long-term memory. OpenAI's SDK tracing records model generations, handoffs, tool calls, and guardrail events; because spans may capture sensitive inputs and outputs, which are included by default, capture settings should be configured deliberately [@r9].

## Workflow Contracts and Runtime Execution

### 8.1 A minimal state and handoff contract

A handoff is not just a summary in natural language. Table 5 lists the fields of an illustrative review-to-analysis handoff; stable identifiers let each agent retrieve the correct versioned inputs and let the controller route failures deterministically.

TABLE Illustrative review-to-analysis handoff record. || A data-contract example, not a configuration for a named framework.
| Field | Example value | Purpose |
| Run and artifact | DAP-DEMO-009; DRAFT-003, version 3 | Identifies the case and the exact version reviewed |
| Stage | review | Tells the controller which transitions are allowed |
| Source manifest | SRC-001, SRC-004 | Evidence the draft relies on |
| Analysis references | ANL-002 | Calculations behind the figures |
| Material claims | CLAIM-014, CLAIM-018 | Statements that must be supported |
| Required checks | citations, math, privacy | Checks the gate must see passed |
| Decision | REWORK | One of pass, rework, escalate, stop |
| Issue | owner analyze; CLAIM-018; annual work weeks inconsistent | Routes the defect to the stage that owns it |
| Attempt | 1 of a maximum of 2 | Bounds the rework loop |

The controller enforces required fields, type checking, stage permissions, and permitted transitions. If the handoff schema fails validation, the workflow must not silently advance. Artifacts should be immutable by version so that a later edit cannot overwrite the object to which an earlier review record referred.

### 8.2 A bounded execution outline

The controller runs the stages in order, and each stage loops at most a fixed number of times (Table 6).

TABLE Bounded execution of the five-stage workflow. || Production orchestration also needs idempotent external actions, checkpoint recovery, concurrency joins, source-permission checks and approved destinations.
| Step | Controller action | Outcome |
| 1. Intake | Authorize the request and create the run state | Run starts, or stops before any agent works |
| 2. Run stage | Execute the stage with its permitted inputs and tools | A new artifact version |
| 3. Gate | Validate the artifact and save a checkpoint | PASS, REWORK, ESCALATE or STOP |
| 4. Pass | Accept the version and move to the next stage | Next stage begins |
| 5. Stop or escalate | Halt, or pause for a human decision | No further automatic work |
| 6. Rework | Route the defect to its owning stage while attempts remain | Targeted correction |
| 7. Budget exceeded | Escalate for human review | No silent retry loop |
| 8. Release | Deliver only if separately authorized | Approved artifact to an approved destination |

This simple loop is useful for reasoning about gates, but targeted rework can invalidate earlier stages: a corrected source may trigger re-analysis and then re-drafting. The controller therefore tracks **dependency lineage**, not just a single loop counter. Frameworks with explicit workflows and persistence can help implement these controls [@r3, @r5].

## Worked Example: A Hypothetical SME Digital Adoption Plan

Consider an invented Canadian wholesale distributor with two warehouses. Management requests a Digital Adoption Plan to improve its order-to-invoice process and evaluate whether a warehouse management system (WMS) and accounting integration would reduce repeated entry. The example does not represent a real client or funding eligibility assessment.

**Research.** The team collects process walkthrough notes, a list of current systems, a sample of orders, and primary vendor material. Management *reports*, but has not yet proven in a time study, that staff spend 14 hours per week re-keying data and five hours correcting status inconsistencies. The evidence pack marks these as client estimates and flags the lack of a representative measurement period. It also records which vendor capabilities are confirmed, unconfirmed, or dependent on licensing.

**Analyze.** An analyst converts the reported workload to a scenario. Assuming 50 productive weeks annually and a loaded labour-value rate of CAD $38/hour, the theoretical full-realization value of 19 hours/week is **19 × 50 × $38 = CAD $36,100/year**. Assume a recurring system-and-support cost of CAD $15,000/year and a one-time integration/change-management cost of CAD $20,000. These are illustrative inputs, not current vendor quotations. At a 70% realization factor, gross annual capacity value is **$25,270**, recurring net value is **$10,270**, and simple first-year net value after one-time cost is **−$9,730**. At 100% realization, recurring net value is **$21,100**, and first-year net value is **$1,100**. No payroll cash savings have yet been demonstrated. Figure 3 sets the two scenarios side by side.

FIG fig3-sme-sensitivity || Sensitivity of the hypothetical SME case to realization. All values are hypothetical Canadian dollars. At 70% realization the recurring net value is positive but the first-year result is negative; at full realization both are positive. Neither is a return estimate or a vendor quotation. || Two columns comparing 70 percent and 100 percent realization of a 19 hour per week workload: gross capacity value, recurring cost, recurring net value, one-time cost and first-year net value. || 

**Draft.** The drafting agent creates a current-state assessment, recommended process improvements, options matrix, staged deployment plan, change-management requirements, financial sensitivity, and clearly labeled dependencies. It cannot write “the WMS will save $36,100 annually” as an unconditional fact. A defensible statement is: “Under management's unverified workload estimate, theoretical annual capacity value is $36,100 before realization, recurring costs, and implementation expenses.”

**Review.** An independent reviewer verifies the formulas and checks that management-reported times are identified as estimates. It challenges an initially unsupported claim that a proposed vendor has bidirectional integration with the client's accounting edition; the claim is removed or held for vendor confirmation. The reviewer also requires confirmation of privacy obligations and data migration complexity before any procurement recommendation.

**Finalize.** The report packages a low-regret process-mapping and pilot-measurement phase, a conditional WMS shortlist, an implementation-risk register, and a measurement plan. A designated human reviews the **specific release candidate** before client delivery. The recommendations do not authorize the agents to purchase software, contact vendors, or migrate live customer records. A pilot would be needed to replace the assumed benefit rate with observed results.

### 9.1 The decision is about evidence, not confidence of prose

At 70% realization, the recurring annual modeled benefit remains positive, while the first-year result is negative. This supports a **phased pilot and evidence-gathering recommendation**, not an unqualified “buy now.” A higher realization factor changes the economics, but without timed baseline data the scenario does not establish probability. In a real advisory engagement, the evidence required to justify investment includes actual throughput, labour impacts, implementation scope, vendor quotes, integration tests, and accountable financial approval.

## Performance Measures and Cost of Assurance

Evaluate the full chain, not each agent in isolation (Table 4). Suggested measures include: **material-claim support rate**, defined as supported material claims divided by total material claims; **critical-defect escape rate**, defined as critical defects discovered after release divided by releases reviewed; **first-pass acceptance rate**; **rework iterations per accepted artifact**; **cost per accepted deliverable** (LLM, tools, human review, and infrastructure); end-to-end latency (median and 95th percentile); and percentage of releases with a valid human authorization record. These are definitions proposed for this workflow; their thresholds require validation in the organization.

TABLE Proposed scorecard. || Metrics should be validated against actual outcomes and human judgment; an evaluator model alone is not a reliable ground truth.
| Metric | Practical test | Typical failure signal | Engineering response |
| Claim support | Independently sample claims and check exact source links | Citation exists but does not support the text | Tighten source-to-claim mapping |
| Numerical reproducibility | Recompute material figures from recorded inputs | Different totals between sections | Use one source-of-truth model |
| First-pass acceptance | Track reviewed versions accepted without rework | Rising retries or vague reviewer comments | Improve stage contracts and rubrics |
| Escalation effectiveness | Audit critical issues and human decisions | Approval without issue resolution | Require explicit risk owner and record |
| Cost per accepted artifact | Sum compute, tools, rework and review | Low token cost but high human correction | Simplify stages or strengthen earlier checks |
| Release integrity | Match approved hash to delivered artifact | Delivered version differs from approved one | Block and re-authorize release |

For instance, 27 supported claims out of 30 yields a **90% claim-support rate**. Yet if the three unsupported claims include the recommendation's economic premise, the report must not pass. The correct gate design uses mandatory claim-level requirements for high-impact findings in addition to aggregate metrics. Adding more reviewer agents is not automatically beneficial; redundant, correlated evaluation may increase cost without increasing truthfulness. Evaluation suites should include unambiguous, representative tasks with reference solutions and explicit pass/fail conditions [@r13]. Anthropic's evaluator–optimizer pattern is most effective when evaluation criteria are clear and iterative feedback demonstrably improves the output [@r2].

## Failure Modes, Security, and Operational Controls

Five stages create more handoff surfaces. **Source drift** occurs when the Research Agent treats an old product page as current; **analysis drift** when a reported estimate becomes an observed value; **citation laundering** when the Drafting Agent assigns a source to a claim the source does not support; **review correlation** when the reviewer repeats the same model's error; and **release drift** when a final artifact changes after approval. Tool errors, expired credentials, partial batch results, and silent timeouts can cause additional defects.

Control these risks through versioned source manifests, independent calculation tools, a claim ledger, narrow tool permissions, explicit stage states, bounded rework, and checkpoints. Protect confidential client information through data-minimization, permission-filtered retrieval, retention limits, and controlled sharing. Treat retrieved instructions as untrusted and require explicit, authenticated human approval for external actions. The NIST AI Risk Management Framework provides a general risk-governance structure, while OWASP documents prompt-injection and excessive-agency risks specific to LLM-integrated applications [@r6, @r10, @r14].

A small, read-only assignment may be better served by **one capable agent with a source check**. The five-stage design becomes appropriate when source accuracy, quantitative analysis, reusable templates, approval, and traceability have sufficient value to offset orchestration cost. The choice should be made from benchmarked task outcomes rather than from the number of agents in a diagram.

## Implementation Roadmap and Conclusion

**Pilot design.** Begin with one recurring, low-risk deliverable such as an internal technology-assessment brief. First define its scope, source constraints, acceptance rubric, review owner, and release policy. Then build the source/claim register, calculation check, review issue tracker, and versioned artifact store. Add separately scoped agents only where a single-agent baseline cannot meet agreed quality, latency, or audit requirements.

**Acceptance before scaling.** Test missing-source behavior, contradictory vendor information, poisoned document text, invalid handoff JSON, wrong-unit arithmetic, reviewer disagreement, retries beyond the budget, interruption recovery, and delivery after an artifact changed. Inspect traces for sensitive-data leakage and verify that an approval of one document cannot authorize another. Measure the cost of rework and human review, not just model tokens.

The **Research → Analyze → Draft → Review → Finalize** workflow is useful because it creates explicit ownership for the transformations that professional knowledge work demands. Research establishes provenance; analysis exposes assumptions; drafting preserves the evidence chain; review challenges important conclusions; and finalization binds the approved artifact to a permitted release. Its central design principle is **a claim should become more defensible as it moves forward, never merely more fluent**.
"""
