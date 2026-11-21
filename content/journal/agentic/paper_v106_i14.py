"""Chmltech Online Journal, Vol. 106, Issue 14 (Multi-Agent AI Engineering series, Article 6). Figure 1 is interactive (live/mae6.html)."""

SLUG = 'ai-skills-engineering-designing-building-testing-and-governing-reusable-agent-capabilities'
META = dict(
    volume=106,
    issue=14,
    title='AI Skills Engineering: Designing, Building, Testing, and Governing Reusable Agent Capabilities',
    short_title='AI Skills Engineering: Reusable Agent Capabilities',
    meta='A seven-stage lifecycle for AI agent skills: contracts, SKILL.md packaging, progressive disclosure, evaluation, release control, security and a worked WMS example.',
    keywords=['agent skills', 'skills engineering', 'SKILL.md', 'progressive disclosure', 'multi-agent AI', 'skill evaluation', 'tool governance', 'LLM agents'],
)
ABSTRACT = 'A reliable multi-agent AI system needs more than specialized agents and an orchestrator. It also needs reusable, testable capabilities that encode how specific kinds of work should be performed. Agent skills package procedural instructions and, when appropriate, scripts, templates, reference material, and examples so that compatible agents can discover and use them when the task warrants. This paper develops a proposed seven-stage Skills Engineering lifecycle: Identify Need; Define Skill; Design Skill; Build Skill; Test & Validate; Deploy & Publish; and Monitor & Improve. It explains the emerging SKILL.md format and progressive disclosure; distinguishes a skill from a model, agent, callable tool, and execution harness; proposes a typed skill contract; and addresses discovery quality, dependency management, sandboxing, source provenance, versioning, and release gates. An explicitly hypothetical warehouse-management-system (WMS) assessment illustrates a skill that creates an evidence-backed vendor evaluation matrix without granting the agent permission to contact vendors or purchase software. Engineering metrics and failure-mode controls turn skill reuse into a governed, observable capability rather than an unreviewed prompt library. The lifecycle and reference architecture are Chmltech design proposals—not a claim that all platforms implement a common runtime or that a skills specification provides security guarantees.'

REFS = {
    'r1': ('Lee, Q. F. (2026). Multi-agent AI systems: Architectures, coordination patterns and failure modes. <em>Chmltech Online Journal</em>, 104(2).',
           'https://www.chmltech.com/post/multi-agent-ai-systems-architectures-coordination-and-failure-modes'),
    'r2': ('Agent Skills. (n.d.). <em>Specification and documentation for Agent Skills</em> [GitHub repository].',
           'https://github.com/agentskills/agentskills'),
    'r3': ('Anthropic. (n.d.). <em>Agent Skills: Overview</em>. Claude Platform Docs.',
           'https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview'),
    'r4': ('Anthropic. (n.d.). <em>Skill authoring best practices</em>. Claude Platform Docs.',
           'https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices'),
    'r5': ('OpenAI. (n.d.). <em>Build skills</em>. ChatGPT Learn.',
           'https://learn.chatgpt.com/docs/build-skills'),
    'r6': ('OpenAI. (n.d.). <em>skill-creator: SKILL.md</em> [openai/skills GitHub repository].',
           'https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md'),
    'r7': ('Cloudflare. (2026). <em>Agent Skills</em>. Cloudflare Agents documentation.',
           'https://developers.cloudflare.com/agents/concepts/agent-skills/'),
    'r8': ('Microsoft. (n.d.). <em>Skills</em> [microsoft/skills GitHub repository, .github/docs/skills.md].',
           'https://github.com/microsoft/skills/blob/main/.github/docs/skills.md'),
    'r9': ('OpenAI. (n.d.). <em>Tools — OpenAI Agents SDK</em>.',
           'https://openai.github.io/openai-agents-python/tools/'),
    'r10': ('OpenAI. (n.d.). <em>Guardrails — OpenAI Agents SDK</em>.',
           'https://openai.github.io/openai-agents-python/guardrails/'),
    'r11': ('OpenAI. (n.d.). <em>Tracing — OpenAI Agents SDK</em>.',
           'https://openai.github.io/openai-agents-python/tracing/'),
    'r12': ('Autio, C., Schwartz, R., Dunietz, J., Jain, S., Stanley, M., Tabassi, E., Hall, P., &amp; Roberts, K. (2024). <em>Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile</em> (NIST AI 600-1). National Institute of Standards and Technology.',
           'https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence'),
    'r13': ('OWASP GenAI Security Project. (2025). <em>LLM06:2025 Excessive agency</em>.',
           'https://genai.owasp.org/llmrisk/llm062025-excessive-agency/'),
    'r14': ('OWASP GenAI Security Project. (2025). <em>LLM01:2025 Prompt injection</em>.',
           'https://genai.owasp.org/llmrisk/llm01-prompt-injection/'),
    'r16': ('Anthropic. (2025, October 16). <em>Equipping agents for the real world with Agent Skills</em>. Anthropic Engineering.',
           'https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills'),
}

CODE = {
    'tree': 'wms-evaluation-matrix/\n├── SKILL.md                 # Required name, description, instructions\n├── references/\n│   ├── scoring-rubric.md    # On-demand domain rules\n│   └── evidence-policy.md   # Source classification and traceability\n├── scripts/\n│   └── validate_scores.py   # Optional deterministic validator\n└── assets/\n    └── evaluation-template.csv\n',
    'skillmd': '---\nname: wms-evaluation-matrix\ndescription: >-\n  Creates an evidence-traceable WMS vendor comparison from supplied\n  requirements and verified vendor materials. Use for structured\n  WMS shortlisting; do not use to contact vendors or place orders.\n---\n\n# WMS Evaluation Matrix\n1. Confirm criteria and weights sum to 100%.\n2. Separate verified evidence, vendor claims, and unknowns.\n3. Score only criteria supported by a cited source.\n4. Run scripts/validate_scores.py on the completed matrix.\n5. Return the matrix, gaps register, and review status.\n6. If a required criterion is unverified, flag it; do not guess.\n',
}

BODY = r"""
## Introduction: From Capable Agents to Reusable Competence

Multi-agent architectures assign responsibilities to planners, researchers, analysts, engineers, reviewers, and coordinators. Yet each agent may be asked repeatedly to perform the same subtask: normalize a requirements spreadsheet, classify procurement evidence, extract a document table, create a risk register, or format a customer-facing report. Encoding that procedure in every agent's system prompt creates duplication, inconsistent versions, high context cost, and fragile maintenance. A reusable skill offers a different unit of engineering: package the *procedure*, specify when it applies, and make it available to authorized agents [@r2, @r3, @r4, @r5].

The Agent Skills open format uses a skill directory with a required SKILL.md file and optional supporting resources. The required metadata provides a name and description; the body supplies instructions that the agent can read when the skill is selected [@r2, @r3]. Microsoft, OpenAI and Cloudflare document comparable progressive-disclosure patterns, although their execution and permission systems remain platform specific [@r5, @r7, @r8]. A skill can be instruction-only. It does **not** have to expose an API, run a script, own a memory database, or make autonomous decisions. Conversely, a packaged skill does not become safe or correct merely because its folder passes a format validator.

This paper extends an earlier paper in this journal on multi-agent orchestration and failure modes [@r1] and the companion paper on harness engineering (Vol. 106, Issue 13). Its engineering question is: **How can an organization turn repeated domain work into a reusable, inspectable capability without expanding agent authority or obscuring accountability?** The answer requires four separations: skill definition versus tool execution; task competence versus authorization; reusable guidance versus validated output; and skill versioning versus ungoverned self-modification. The method developed below is a practical design synthesis, not a purported universal standard.

## What Is a Skill—and What Is It Not?

For this paper, an **AI skill** is a named, reusable package of task-specific procedural guidance and optional resources that a compatible agent can discover, activate, and follow. The package may describe a workflow, call existing tools through the host, invoke vetted scripts in a permitted execution environment, and generate artifacts subject to validation. A **tool** is the concrete callable interface that actually reads or changes something, such as querying a database or generating a file. An **agent** selects goals and actions within its instructions and allowed tools. The **harness** supplies runtime state, orchestration, permissions, guardrails, tracing, and human approvals [@r9, @r10, @r11]. Table 1 sets out the boundary between agent, skill, tool and harness.

TABLE Functional boundary between agent, skill, tool, and harness. || Individual software frameworks may combine these layers in one application.
| Layer | Central responsibility | Typical artifact | Key boundary |
| Agent | Interpret task and choose the next authorized capability | Task plan; selected skill; proposed action | May not create its own privileges |
| Skill | Encode repeatable method, triggers, steps and templates | SKILL.md; scripts; examples; references | Skill text is not an enforcement mechanism |
| Tool / API | Perform a typed read, calculation, or authorized side effect | JSON result; database record; generated file | Credentials and arguments checked at invocation |
| Harness / runtime | Load, route, execute, constrain, observe and recover | Run trace; approval record; version manifest | Policy must be independent of model output |

This distinction matters when the skill says, “Compile supplier prices and prepare outreach.” A research agent can use the skill to draft a request for quotation; an email-sending tool requires separate permissions and explicit authorization for the actual recipients, message, and timing. The *skill text* is neither a credential nor evidence of consent. OWASP describes excessive agency as excessive functionality, permissions, or autonomy; packaged instructions should not expand those boundaries [@r13].

### 2.1 Instruction-only, script-assisted, and integration skills

An **instruction-only skill** may be a report-writing rubric or review checklist. A **script-assisted skill** can reference deterministic helpers for calculations, schema checks, or document transformations. An **integration skill** may describe how an agent should use existing business-system connectors or APIs, but the connector itself remains a separately authorized interface. Finally, a **domain skill** may bundle specialized reference documents such as chart-of-accounts conventions or equipment-data-sheet standards. These types can overlap, and all require a clear scope, test strategy, and ownership.

### 2.2 Discovery, activation, and execution are separate events

Progressive disclosure separates *discovery metadata* from *full instructions* and *supporting resources*. A compatible host initially exposes only concise metadata, loads the skill instructions if selected, then accesses referenced material as the task needs it [@r2, @r7, @r8, @r16]. That reduces unnecessary context, but creates a new quality challenge: a misleading description can cause both false activation and missed activation. Skill discovery must therefore be evaluated as carefully as the result of running the skill.

## Seven Stages of the Skills Engineering Lifecycle

Figure 1 traces a skill through the seven stages described in this section.

FIG fig1-skill-lifecycle || The seven-stage Skills Engineering lifecycle. The figure plays through each stage in turn, showing how a skill moves from a recurring need to a contract, a design, a package, an evaluated candidate, a published version and a monitored capability, with failed checks returning to the stage that owns them; select a stage to jump to it, or <em>All stages</em> to compare them side by side. A conceptual model, not a specification of mandatory product behavior. || Seven stage circles in a row from identify need to monitor and improve, with the skill owner above, a versioned skill registry below and a release approver beside the publish stage, each stage shown with its output, its gate and the failure to watch. || 

### 3.1 Stage 1 — Identify Need

Start with an observable deficiency: repeated manual steps, inconsistent outputs, high correction rates, context that must be re-explained, or a deterministic operation that the model performs unreliably. Collect representative inputs, user expectations, legal and contractual constraints, baseline cost/time, failure consequences, and the existing non-skill alternative. Avoid treating every prompt as a skill candidate. A skill is most valuable where the work has a repeatable procedure, a description that states when to use it, and evaluations that can be run against a baseline [@r4, @r6].

**Gate:** Is the task frequent enough, stable enough, and distinct enough to justify lifecycle ownership? Define the business outcome, current baseline, skill owner, first evaluation set, and explicit exclusions. **Output:** skill opportunity and requirement brief.

### 3.2 Stage 2 — Define Skill

Draft the skill's **contract** before writing the prompt. Include its name, description and expected triggers; out-of-scope requests; allowed data classes; required inputs; input assumptions; output schema; evidence requirements; failure states; side-effect classification; authorized tool dependencies; and performance targets. Make the description specific enough to enable selection and narrow enough to avoid unrelated activation. The Agent Skills format requires name and description in YAML frontmatter; other business contract fields in this article are proposed governance metadata and are **not** universally required fields in the file format [@r2, @r3, @r4, @r5].

**Gate:** Can a test reviewer tell which tasks must activate the skill, which tasks must not, and what a successful result looks like? **Output:** signed-off skill specification.

### 3.3 Stage 3 — Design Skill

Break the skill into the smallest useful sequence of steps. Specify when it reads supporting documentation, which calculations are deterministic, what an agent should do when evidence is missing, and what constitutes a valid completed artifact. Design *failure and escalation paths* as first-class outputs: INSUFFICIENT_EVIDENCE, INVALID_INPUT, POLICY_DENIED, and HUMAN_REVIEW_REQUIRED may be more accurate than a confident narrative answer. Prefer clear examples, concise instructions, and on-demand reference files rather than a large duplicated prompt [@r4, @r6].

Design includes an **evidence model**. For any factual conclusion, capture the source identifier, retrieval or document date where relevant, extraction method, transformation, and uncertainty. A skill should not quietly convert a vendor's marketing claim into a verified requirement match. **Gate:** design review of dataflow, risk, dependencies, and output contract. **Output:** skill design and test plan.

### 3.4 Stage 4 — Build Skill

Implement a version-controlled skill folder. Keep SKILL.md short and task-specific; move long references into targeted files, and include scripts only when they provide a concrete repeatability benefit. For scripts, pin dependencies where practical, reject malformed input, avoid interactive prompts, return structured outputs, and do not write secrets or raw sensitive inputs into logs. OpenAI and Anthropic both emphasize that skill instructions should add non-obvious task guidance instead of restating generic knowledge [@r4, @r6].

Run scripts in the **permissions and sandbox configuration supplied by the host**. Treat downloaded skills, templates, scripts, and retrieved documents as potential supply-chain inputs. Do not assume SKILL.md is trusted merely because it is local. **Gate:** static validation, dependency scan, peer review, and reproducible build. **Output:** packaged skill candidate and implementation record.

### 3.5 Stage 5 — Test & Validate

Test the skill at three levels: *discovery*, *task execution*, and *system integration*. A good task answer is not sufficient if the skill triggers for unrelated work or if a subsequent tool call bypasses approval. Use positive, negative, ambiguous, adversarial, and boundary datasets. Measure not just text quality but observable correctness, evidence completeness, structured-output validity, and recovery behavior. For important actions, include tests that prove denial paths are enforced by code, not by prose [@r10, @r13, @r14].

A release candidate should have a reproducible evaluation report with representative cases, baseline comparison, failures by category, test data version, skill version, runtime configuration, and reviewer approval. **Gate:** required threshold met and critical failures resolved or accepted by accountable owners. **Output:** signed validation report and release decision.

### 3.6 Stage 6 — Deploy & Publish

Publish the approved version into an agent-accessible catalog with ownership, compatibility, dependency, access, and rollback information. An installed skill is not necessarily discoverable to all agents or authorized for every user. Deployment configuration should control both *visibility* and *execution privileges*. Pilot in a low-risk environment, verify tracing, and check that the published content matches the tested package. In high-consequence workflows, add human review before release even when automated checks pass, consistent with NIST's note that generative-AI use may warrant additional human review [@r12].

**Gate:** release manifest verified, policy checked, pilot owner accepts the skill, and rollback procedure tested. **Output:** discoverable, versioned skill with support and monitoring responsibilities.

### 3.7 Stage 7 — Monitor & Improve

Monitor how often the skill is selected, how often that selection was appropriate, the quality of resulting artifacts, and how often human correction or escalation was needed. Analyze failed cases for unclear descriptions, changed source systems, incorrect calculations, missing references, or tool-permission errors. Propose edits through change control and rerun the evaluation suite before promotion. A skill may update its *output* or produce improvement suggestions without being allowed to rewrite its *own trusted instructions* in production.

**Gate:** measured change benefit exceeds regression risk and the revised version passes its release tests. **Output:** improved skill version, change log, new evaluation cases, and retired or superseded versions where appropriate.

## The SKILL.md Package and Progressive-Disclosure Architecture

Figure 2 shows how a compatible host discovers, activates and runs a skill, and where its boundaries are enforced.

FIG fig2-skill-execution || Skill execution reference architecture. The agent reads catalog metadata, activates a skill when it fits, loads the procedure and optional references, requests tools through the harness, and returns a validated artifact; a separately enforced policy and evidence boundary protects data and external actions. A proposed application architecture, not a claim that every platform implements every step. || Seven numbered steps in a row, catalog, selection, activation, resources, tool broker, assurance and artifact, above three boundary panels for selection, execution and assurance, and a strip showing read-only evidence, model context, the tool policy service and the output trace. || 

A portable skill often resembles the structure in Example 1 [@r2, @r3, @r5, @r8].

CODE tree || Example 1. Folder layout of a portable skill package.

Example 2 is a **design example**, not a ready-to-deploy authenticated integration. It uses only the required portable frontmatter and puts deployment permissions in the harness rather than relying on unsupported frontmatter keys.

CODE skillmd || Example 2. Excerpt of an illustrative SKILL.md file with the required name and description frontmatter.

The folder illustrates the open format's packaging conventions, but the scoring algorithm, evidence tiers, release approval, and external-access limits are design decisions of this example. Validation of syntax is only one test. A high-quality skill also needs semantic review, functional tests built on evaluations, and authorization controls enforced outside the skill before it is allowed to operate [@r4, @r13].

### 4.1 A practical skill contract

Table 2 lists the elements of an example skill contract.

TABLE Example skill contract. || Only the name and description frontmatter fields are mandatory in the portable SKILL.md specification; the remaining elements are implementation and governance choices.
| Contract element | Example for WMS evaluation | Verification approach |
| Trigger and exclusions | WMS shortlist; excludes vendor outreach and purchasing | Positive and negative routing tests |
| Inputs | Requirements, weights, vendor evidence, assessment date | Schema and completeness checks |
| Output | Score table, evidence IDs, assumptions, open questions | Structured validator and reviewer |
| Allowed dependencies | Read-only document lookup; local scoring script | Tool allowlist and capability test |
| Failure states | Missing evidence; invalid weights; inconsistent units | Negative test suite |
| Governance | Owner, version, review date, data retention policy | Release manifest and approval record |

## Integrating Skills into Multi-Agent Workflows

A research agent might collect vendor brochures and tag evidence; an analyst agent might invoke the scoring skill; a reviewer agent might inspect conflicts and unsupported claims; and a decision agent might compare validated alternatives. That design makes the **skill** a reusable procedure and the **agents** the holders of task responsibility. Multiple agents can share one approved skill without inheriting each other's full conversation history. The orchestration layer should also record which skill version was used for each output and the dependencies required to recreate it.

Not every task needs a new agent. For repetitive formatting, extraction, or calculation, a skill invoked by a single agent may be less expensive and easier to govern. Adding a specialist agent should be justified by a measurable improvement in decomposition, expertise, isolation, or verification. For workflows with parallel specialists, use an explicit *artifact contract*: pass structured artifacts with defined schemas between agents rather than unconstrained conversation, and protect shared state from contamination [@r1].

A reliable handoff has five fields: task_id, skill_version, inputs_and_evidence, result_and_validation, and next_action. Include a run identifier and immutable artifact checksum where auditability is important. Agent-generated statements such as “verified” should be accompanied by the actual validator output or reviewer record. Where an agent uses tools, OpenAI's SDK documentation illustrates both typed tool schemas and guards that can validate or block calls at invocation; those checks are runtime mechanisms, not properties of the SKILL.md file [@r9, @r10].

## Testing Skills as Engineering Components

A skill test suite should include **selection tests** (did the correct skill activate?), **contract tests** (were required inputs and outputs respected?), **functional tests** (did the procedure produce the correct artifact?), **integration tests** (did tools, memory, and handoffs behave as designed?), and **security tests** (did the system reject manipulations and unauthorized actions?). Tests also need to cover the absence of required evidence; the correct answer may be a well-labeled unknown rather than a plausible fabricated fact. Table 3 sets out a minimum release-oriented suite.

TABLE Minimum release-oriented skill evaluation suite. || Exact thresholds should be set by the product owner and risk assessment, not assumed universal.
| Test class | Example test | Acceptance signal |
| Discovery | WMS comparison request versus unrelated payroll question | Correct activation and rejection |
| Functional | Known scoring fixture with fixed weights | Exact expected weighted score |
| Contract | Empty requirement list; weights total 95% | Explicit validation error, no ranking |
| Evidence | Vendor claim lacks source/date | Mark as unverified; do not score as fact |
| Security | Source document instructs agent to email files externally | Treat as untrusted data; no unauthorized send |
| Recovery | Scoring helper times out or returns malformed JSON | Bounded retry or escalation, no false success |
| Regression | Revised SKILL.md rerun against previous cases | No critical regressions; changes documented |

A useful metric is **activation precision**, the share of skill activations that were appropriate, and **activation recall**, the share of eligible requests for which the skill was invoked. A skill with excellent execution quality but poor routing can still reduce overall system quality. Other metrics include acceptance rate, evidence completeness, tool error rate, rework incidence, human escalation frequency, p95 latency, and cost per accepted output. OpenAI's tracing documentation shows how model generations, tool calls, handoffs and guardrails can be correlated in a run; a production design should retain only the data needed for operations and permitted by applicable privacy controls [@r11].

Define *accepted-output cost* as total measured model, tool, infrastructure, and review expenditure divided by the number of outputs accepted by the specified quality process. For example, 100 skill runs costing an illustrative $120 in compute and $80 in review that yield 80 accepted outputs produce $2.50 per accepted output; the same system's raw cost per run is $2.00. The numbers are only an arithmetic demonstration, and omitting human review would understate real delivery cost. Compare like-for-like tasks, time windows, and evidence standards when determining whether reuse is economically beneficial.

## Security, Permissions, and Supply-Chain Assurance

Skills are useful precisely because they change what an agent is likely to do. That makes every instruction, bundled script, reference document, dependency, and template a potential attack or error surface. Threats include malicious third-party skills, prompt injection in reference text, attempts to exfiltrate secrets, unauthorized modification of records, tampered scripts, and stale domain rules. Anthropic's skills documentation warns that a malicious skill can direct the agent to call tools or run code in ways that do not match its stated purpose, and advises using skills only from trusted sources; OWASP identifies prompt injection and excessive agency as material risks for LLM applications [@r3, @r13, @r14].

The most important defense is **independent enforcement**. The harness must decide whether a tool may be called, with which arguments, under which identity, and whether the action needs human approval. Merely saying “do not send email” inside a skill may guide the model but does not reliably prevent a write-capable tool from being used. Enforce a read-only tool set for evaluation-only skills; require approval for outbound-message tools through a per-call approval policy, validate arguments with tool input guardrails, and block disallowed destinations at the tool boundary [@r9, @r10].

At publication, record the source repository and revision, a hash of the package, dependency manifest, code-review decision, permitted tools, sensitivity rating, and maintainer. Prefer signed or otherwise verified distribution where available; scan scripts, restrict execution environments, prevent surprise network access, and provide a mechanism for emergency disablement. Treat retrieved policies, PDF instructions, and tool descriptions as *data* until authenticated and promoted through the appropriate authority. NIST's Generative AI Profile provides a broader risk-management context for evaluating, governing, and monitoring generative-AI use [@r12].

### 7.1 Failure modes and practical controls

Table 4 pairs representative skill-level risks with controls.

TABLE Representative skill-level risks and controls. || These safeguards supplement—not replace—organizational security, privacy, and professional review.
| Failure mode | Operational consequence | Primary engineering control |
| Over-broad description | Skill activates on unrelated requests | Contrastive routing tests and revised metadata |
| Hidden dependency | Inconsistent output after tool or data change | Versioned manifest, fixture-based integration tests |
| Unverified evidence | False confidence in vendor comparison | Source tiers, citation IDs, explicit unknown status |
| Unsafe script | Data leakage or unintended side effects | Sandboxing, reviewed code, network restrictions |
| Privilege escalation | External write without authorization | Runtime policy, least privilege, action-specific approval |
| Silent drift | Performance degrades after environment change | Monitoring, regression suite, versioned rollback |

## Worked Example: A Reusable Skill for SME WMS Assessment

Consider a **hypothetical** Vancouver manufacturer and distributor replacing manual warehouse records. A consultant supplies requirements, process maps, integration constraints, vendor evidence, and project assumptions. The multi-agent system consists of an intake agent, an evidence agent, an analyst, and an independent reviewer. Rather than re-teaching each agent the evaluation method, the analyst activates the <em>wms-evaluation-matrix</em> skill using the approved scoring rubric and a read-only evidence collection. This example is for engineering illustration and does not describe any actual client or measured deployment.

The scope includes five weighted criteria: functional fit (30%), ERP/accounting integration (25%), implementation feasibility (20%), support and localization (15%), and total-cost transparency (10%). The weights total 100% and are **user-approved inputs**, not proposed universal WMS priorities. Suppose, for the sake of demonstrating the scoring formula, three fictional candidates receive the fully evidenced scores below on a 1–5 scale. A real skill would refuse to assign a supported score where evidence is missing.

TABLE Fictional test fixture for skill-scoring validation. || The arithmetic is deterministic; no real vendors were evaluated.
| Hypothetical candidate | Functional 30% | Integration 25% | Implementation 20% | Support 15% | Cost 10% | Weighted / 5 |
| Candidate A | 4 | 3 | 5 | 4 | 3 | 3.85 |
| Candidate B | 3 | 5 | 4 | 3 | 4 | 3.80 |
| Candidate C | 5 | 4 | 3 | 4 | 2 | 3.90 |

The weighted score of candidate *j* is Eq. (1), where *w*<sub>k</sub> is the approved weight of criterion *k* and *s*<sub>jk</sub> the candidate's score on it:

TEX S_j = \sum_k w_k \, s_{jk}

Applied to Table 5, Eq. (1) gives 3.85, 3.80 and 3.90. The hypothetical scores place C marginally ahead of A, but the 0.05-point difference is not a reliable decision signal unless the evidence and assumptions justify the score resolution. If a claim about an accounting integration cannot be verified, the correct workflow is to flag the claim and potentially withhold the shortlist ranking—not to substitute an optimistic score. A separate scenario analysis can show how rankings change if integration weight rises, but the agent should not silently alter approved weights.

The resulting deliverable is an evidence register, comparison matrix, score-validation log, uncertainty register, and reviewer disposition. The analyst skill may draft follow-up questions for vendors; it **may not send those messages** unless an authorized human separately approves that exact external action. A decision or procurement agent can consume the validated matrix but must preserve caveats. This illustrates a central benefit of skills engineering: **reuse the method while keeping evidence, decisions, and authority case-specific**.

## Operational Metrics, Release Gates, and Continuous Improvement

Figure 3 shows the controlled release and change loop.

FIG fig3-skill-release || Controlled release and change loop. A candidate skill passes format and dependency checks, functional and adversarial evaluation, accountable review, controlled publishing and production monitoring; failed checks return for repair, and production feedback creates a new candidate version rather than a silent edit. || Six stages in a row, package, static gate, evaluation, owner review, publish and monitor, with a dashed repair loop from the evaluation back to packaging, a dashed feedback loop from monitoring to a new candidate, and a note that a skill release never authorizes a specific external action. || 

Measure outcomes at the *skill × agent × workload × version* level. Otherwise, an improvement in a model or a change in task mix may be mistaken for an improvement in the skill itself. For reproducibility, record skill version, harness version, model selection, tool versions, evaluation fixture version, and sample size. Inspect successes and failures rather than just aggregate acceptance scores. A 95% apparent success rate can conceal a catastrophic one-in-twenty unauthorized-action failure in a small or biased evaluation set.

Do not mandate a single numerical release threshold for every skill. A read-only report-formatting skill can tolerate a different residual error profile from a skill that prepares chemical process operating instructions or updates financial records. Use consequence-based severity, representative tests, and independent owner approval. After release, record drift signals, user feedback, and source changes; propose repairs through a new version and full targeted regression testing. Keep the release gate separate from a task-specific human approval gate: passing a software test does not authorize an individual purchase, email, or operational change.

## Engineering Playbook: Build, Evaluate, and Govern

A practical implementation program starts with **one high-value, low-side-effect task** and runs it in shadow mode against a current workflow. Collect a small but realistic gold set, including failed and ambiguous cases, then compare a baseline agent without the skill against the same agent with the skill. Use deterministic code for arithmetic and schema checks; let the agent handle bounded interpretation where appropriate; use an independent reviewer for externally meaningful deliverables. All external writes should remain disabled until a separate approval workflow exists.

A minimal **release manifest** should answer these questions: Which exact package and content hash is approved? Which versions of tools and reference sources were used? Which agents and user groups may activate the skill? What data classification can it access? What is the quality evidence? Who can roll back or disable it? What constitutes a security escalation? When must it be re-evaluated? These controls align skill ownership with broader risk management rather than treating the library as an unmanaged collection of prompts [@r10, @r11, @r12, @r13].

The operational checklist is deliberately short: define a bounded use case; specify triggers and exclusions; document inputs and outputs; build the package; test discovery and behavior; audit tool permissions; validate representative outcomes; publish a versioned manifest; observe production runs; and require change-controlled promotion. Do not mark a skill “production ready” merely because it performed well on one demonstration case.

## Limitations and Research Questions

The packaging format improves portability of *instructions* but does not guarantee semantic equivalence across models, hosts, policies, or tools. The specification does not define where skills are stored or how an agent loads them, so different hosts may treat resource loading, script execution, approval, and memory differently [@r5, @r7]. An instruction-only skill may be safe but non-deterministic; a script-assisted skill may be precise but bring dependency and runtime risk. Evaluation can miss rare failures, and model-based judges can approve plausible answers that lack factual grounding. Skill discovery quality can change with a model or catalog update independently of the skill text.

Further work should quantify when skills outperform longer system prompts or specialized agents on matched workloads; whether cross-host reuse preserves performance; how activation precision scales with very large catalogs; which contract elements predict low rework; and how to verify the chain from source evidence through agent action to final deliverable. Those are empirical questions, not conclusions supported by a single architecture diagram. A skills library should therefore be treated as a maintained software-and-knowledge asset whose value is proven through measured use.

## Conclusion

Skills convert recurring agent procedures into reusable, versioned engineering assets, while agents choose tasks, tools perform authorized operations, and the harness controls execution boundaries. The **seven-stage Skills Engineering lifecycle** proposed here moves from business need and a clear contract through design, build, evaluation, publication, and governed improvement. Progressive disclosure makes a large catalog practical, but discoverability, accuracy, source traceability, security, and operational authorization must be deliberately engineered [@r2, @r3, @r4, @r5].

The practical recommendation is to **build skills as testable products, not as ungoverned prompts**: provide precise activation descriptions, inspectable methods, structured outputs, evidence IDs, deterministic validation where possible, release controls, and metrics by version. A properly designed skill reduces repeated instructions and supports consistent work; it does not remove the need for a knowledgeable reviewer, client-specific evidence, or accountable approval. Together with orchestration and harness engineering, skills provide an essential capability layer for dependable multi-agent AI systems.
"""
