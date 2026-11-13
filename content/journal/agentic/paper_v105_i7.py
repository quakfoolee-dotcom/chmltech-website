"""Chmltech Online Journal, Vol. 105, Issue 7 (V4.67): Levels of Autonomy and Human-in-the-Loop Design for AI Agents."""

SLUG = "levels-of-autonomy-and-human-in-the-loop-design-for-ai-agents"
META = dict(
    volume=105, issue=7,
    title="Levels of Autonomy and Human-in-the-Loop Design for AI Agents: Matching Oversight to Risk and Earning Autonomy with Evidence",
    short_title="Levels of Autonomy and Human-in-the-Loop Design",
    meta="How much should an AI agent do on its own? Levels of autonomy, the failure modes of human review, a per-action risk rule and evidence-based promotion.",
    keywords=["AI agents", "levels of autonomy", "human-in-the-loop", "human oversight", "automation bias", "approval workflows",
              "risk management", "EU AI Act"],
)

ABSTRACT = (
    "AI agents now complete multi-step tasks that once required a person at every step, and the length of task they can complete has been "
    "doubling roughly every seven months. How much an agent is allowed to do without a person is therefore a design decision rather than a "
    "property of the model. This paper reviews the levels-of-automation literature, from Sheridan and Verplank's ten levels and the four-stage "
    "model of Parasuraman, Sheridan and Wickens to SAE J3016 and a recent five-level framework for AI agents defined by the role of the user. "
    "It then summarizes why human oversight often fails in practice: the ironies of automation, loss of situation awareness, automation bias "
    "and approval fatigue. Building on that evidence, it proposes that autonomy be set per action rather than per agent, using four properties "
    "of the action: reversibility, impact, detectability and novelty. A simple expected-loss rule shows when an approval step pays for itself, "
    "and a capacity check shows when it will be rubber-stamped. The paper sets out what a reviewer must see, and how sampling, escalation "
    "and stop controls complement approval. It closes with an evidence-based promotion path in which an agent earns each level of autonomy "
    "through shadow-mode trials, with a statistical bound on the error rate, and loses it on defined triggers."
)

REFS = {
    "metr": ("Kwa, T., West, B., Becker, J., Deng, A., Garcia, K., Hasin, M., et al. (2025). Measuring AI ability to complete long tasks. arXiv:2503.14499.",
             "https://arxiv.org/abs/2503.14499"),
    "feng": ("Feng, K. J. K., McDonald, D. W., &amp; Zhang, A. X. (2025). Levels of autonomy for AI agents. arXiv:2506.12469. Knight First Amendment Institute, AI and Democratic Freedoms series.",
             "https://arxiv.org/abs/2506.12469"),
    "sheridan": ("Sheridan, T. B., &amp; Verplank, W. L. (1978). Human and computer control of undersea teleoperators (Technical report). MIT Man-Machine Systems Laboratory.",
                 "https://apps.dtic.mil/sti/citations/ADA057655"),
    "para2000": ("Parasuraman, R., Sheridan, T. B., &amp; Wickens, C. D. (2000). A model for types and levels of human interaction with automation. <em>IEEE Transactions on Systems, Man, and Cybernetics, Part A</em>, 30(3), 286–297.",
                 "https://doi.org/10.1109/3468.844354"),
    "sae": ("SAE International. (2021). Taxonomy and definitions for terms related to driving automation systems for on-road motor vehicles (SAE J3016_202104).",
            "https://www.sae.org/standards/content/j3016_202104/"),
    "bain": ("Bainbridge, L. (1983). Ironies of automation. <em>Automatica</em>, 19(6), 775–779.",
             "https://doi.org/10.1016/0005-1098(83)90046-8"),
    "endsley": ("Endsley, M. R., &amp; Kiris, E. O. (1995). The out-of-the-loop performance problem and level of control in automation. <em>Human Factors</em>, 37(2), 381–394.",
                "https://doi.org/10.1518/001872095779064555"),
    "pararil": ("Parasuraman, R., &amp; Riley, V. (1997). Humans and automation: Use, misuse, disuse, abuse. <em>Human Factors</em>, 39(2), 230–253.",
                "https://doi.org/10.1518/001872097778543886"),
    "goddard": ("Goddard, K., Roudsari, A., &amp; Wyatt, J. C. (2012). Automation bias: A systematic review of frequency, effect mediators, and mitigators. <em>Journal of the American Medical Informatics Association</em>, 19(1), 121–127.",
                "https://doi.org/10.1136/amiajnl-2011-000089"),
    "leesee": ("Lee, J. D., &amp; See, K. A. (2004). Trust in automation: Designing for appropriate reliance. <em>Human Factors</em>, 46(1), 50–80.",
               "https://doi.org/10.1518/hfes.46.1.50_30392"),
    "euaia": ("European Parliament and Council of the European Union. (2024). Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). <em>Official Journal of the European Union</em>, L series.",
              "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"),
    "nist": ("National Institute of Standards and Technology. (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0) (NIST AI 100-1).",
             "https://doi.org/10.6028/NIST.AI.100-1"),
    "anth": ("Schluntz, E., &amp; Zhang, B. (2024, December 19). Building effective agents. Anthropic.",
             "https://www.anthropic.com/engineering/building-effective-agents"),
    "tau": ("Yao, S., Shinn, N., Razavi, P., &amp; Narasimhan, K. (2024). τ-bench: A benchmark for tool-agent-user interaction in real-world domains. arXiv:2406.12045.",
            "https://arxiv.org/abs/2406.12045"),
    "hanley": ("Hanley, J. A., &amp; Lippman-Hand, A. (1983). If nothing goes wrong, is everything all right? Interpreting zero numerators. <em>JAMA</em>, 249(13), 1743–1745.",
               "https://doi.org/10.1001/jama.1983.03330370053031"),
    "sec": ("Lee, Q. F. (2026). Agent security and identity: Prompt injection, least-privilege tool access, agent credentials and audit trails. <em>Chmltech Online Journal</em>, 105(5).",
            "https://www.chmltech.com/post/agent-security-and-identity-prompt-injection-least-privilege-credentials-audit"),
}

BODY = r"""
## Introduction

Until recently, the question of how much an AI system should do on its own had a simple answer for most businesses: very little. A language model drafted text and a person decided what to do with it. AI agents change that. An agent plans a sequence of steps, calls tools, reads the results and continues until the task is done, and it can post an invoice, send an email or change a record without anyone pressing a button. The capability behind this is growing quickly. Researchers at METR measured the length of software and research tasks, in human working time, that frontier models complete with 50 percent reliability, and found that this time horizon has been doubling roughly every seven months since 2019 [@metr].

Capability, however, does not decide autonomy. Feng, McDonald and Zhang argue that the level of autonomy at which an agent operates is a deliberate design choice, separate from what the agent is able to do and from the environment it works in [@feng]. A highly capable agent can be deployed as an assistant that proposes and waits, and a modest one can be allowed to act alone on narrow, low-risk tasks. The question for a business is not "how good is the model?" but "which actions may this agent take without a person, and how do we know?"

This paper addresses that question. Section 2 reviews the levels-of-automation literature and maps it to agents. Section 3 summarizes the evidence on why human oversight often fails in practice. Section 4 proposes setting autonomy per action using four properties of the action, with a simple cost rule for when an approval step is worth its cost. Section 5 describes how to design the human checkpoint so that oversight is real. Section 6 sets out an evidence-based path for promoting an agent from one level to the next, and for demoting it.

## Levels of automation: from teleoperators to agents

### 2.1 Classic scales

The idea that automation comes in degrees is old. Sheridan and Verplank, studying the remote control of undersea vehicles, described ten levels running from a computer that offers no assistance, through one that suggests alternatives or executes a choice if the human approves, to one that acts entirely on its own and informs the human only if it decides to [@sheridan]. Their scale introduced the distinctions that still matter for agents: who generates the options, who selects one, who executes it, and whether the human is told.

Parasuraman, Sheridan and Wickens refined this into a two-dimensional model [@para2000]. They separated four functions that a system can automate (information acquisition, information analysis, decision selection and action implementation) and argued that each can be automated to a different level. A system can gather and analyze information with high autonomy while leaving the decision to a person. Their central recommendation was that the right level for each function should be set by the consequences of errors and by human performance, not by what the technology makes possible.

The best-known scale today is SAE J3016 for driving automation, with six levels from no automation (Level 0) to full automation in all conditions (Level 5) [@sae]. Its key contribution is the notion of an operational design domain: a Level 4 vehicle drives itself without a human fallback, but only within defined conditions such as a mapped area or certain weather. Outside them the system must hand over or reach a safe state.

### 2.2 A scale for AI agents

Feng and colleagues propose five levels for AI agents defined by the role the user plays [@feng]. At Level 1 the user is an operator who directs the work and makes the decisions while the agent acts on command. At Level 2 the user is a collaborator who shares planning and execution with the agent. At Level 3 the user is a consultant whom the agent asks for input and preferences. At Level 4 the user is an approver whose consent is needed for certain actions, such as high-risk ones. At Level 5 the user is an observer who can monitor the agent and stop it but does not intervene in normal operation. Table 1 aligns these scales.

TABLE Correspondence between automation scales, as interpreted by the author. Levels are approximate equivalents rather than exact matches. || Sources: [@sheridan], [@para2000], [@sae], [@feng].
Agent level (user role) | Who decides and acts | Sheridan–Verplank level | SAE J3016 analogue
L1 Operator | Human decides; agent executes on command | 2–3: computer offers or narrows options | Level 0–1
L2 Collaborator | Human and agent share planning and execution | 4: computer suggests one alternative | Level 1–2
L3 Consultant | Agent leads; asks the human for input and preferences | 5: executes if the human approves | Level 2
L4 Approver | Agent acts; human approval required for defined actions | 6: human has limited time to veto | Level 3
L5 Observer | Agent acts alone; human monitors and can stop it | 7–10: informs the human after acting, or not at all | Level 4–5, within a design domain

The analogy with driving should not be pushed too far. A vehicle performs one task, driving, so a single level describes the system. An agent in a business performs many different actions with very different consequences: reading a record, drafting a reply, issuing a refund, deleting a file. A single autonomy level for the agent as a whole is therefore too coarse. The Parasuraman model, which assigns levels per function, is closer to what agents need, and Section 4 extends it to per-action levels.

## Why human oversight fails

The default response to agent risk is to put a human in the loop. Decades of research on automation show that this is necessary but not sufficient: a human in the loop provides real protection only under specific conditions.

### 3.1 The ironies of automation

Bainbridge observed that automation creates two ironies [@bain]. First, designers automate the tasks they can and leave the human to handle what they cannot, so the human is left with the hardest and rarest situations. Second, the human's role becomes monitoring, a task people perform poorly over long periods, and the skills needed to take over decay precisely because the automation usually works. Both apply to agents. If an agent handles routine invoices and escalates only the unusual ones, the clerk who reviews escalations sees only difficult cases while losing the daily practice that built their judgment.

### 3.2 Out of the loop

Endsley and Kiris showed experimentally that operators who monitored full automation were slower and less accurate when they had to take over than operators who had been working at an intermediate level of automation [@endsley]. The cause was reduced situation awareness: the monitoring operator had not been building a model of the situation. For agents, the lesson is that a person who is asked to approve a single action at the end of a long chain, with no view of how the agent got there, cannot judge it well.

### 3.3 Automation bias and complacency

Parasuraman and Riley distinguished use, misuse, disuse and abuse of automation, where misuse means relying on automation when it should not be relied on [@pararil]. A systematic review of automation bias in clinical decision support found that users frequently accepted incorrect advice, that errors of commission (following wrong advice) and omission (missing a problem the system did not flag) both occurred, and that the effect was stronger when workload was high and when users had greater trust in the system [@goddard]. Lee and See framed the design goal as appropriate reliance: trust should match the automation's actual reliability in the situation at hand, which requires that the system make its reliability visible [@leesee].

### 3.4 Approval fatigue

These findings combine in a pattern familiar to anyone who has deployed an approval workflow. When an agent is usually right, approvals become a formality. The reviewer sees a long queue of similar requests, the first hundred are correct, and the hundred-and-first is approved without being read. The approval step then adds delay and cost while providing little protection, and it creates a record that suggests oversight took place.

CALLOUT A human in the loop is a control only if the human has the information, the time and the incentive to say no. An approval step that is never declined is not evidence that the agent is safe; it may be evidence that the step is not working.

The EU Artificial Intelligence Act reflects this research. For high-risk systems, Article 14 requires that the people assigned to oversight be able to understand the system's capacities and limitations, remain aware of the tendency to rely too much on its output, which the Act calls automation bias, correctly interpret the output, decide not to use it or override it, and interrupt the system through a stop button or similar procedure [@euaia]. These are useful design requirements even where the Act does not apply.

## Setting autonomy per action

### 4.1 Four properties of an action

The appropriate level of autonomy depends on the action, not the agent. This paper proposes four properties for classifying each action an agent can take.

1. **Reversibility.** Can the action be undone fully and cheaply? A draft can be deleted; a payment to a third party, an email to a customer or a deleted record without a backup cannot.
2. **Impact.** What is the worst plausible consequence, in money, safety, legal exposure or reputation? Impact can be bounded by limits, for example a maximum refund value.
3. **Detectability.** If the action is wrong, how likely is the error to be caught before it causes harm, by a downstream check, a reconciliation or the recipient?
4. **Novelty.** Is the situation within the range of cases on which the agent has been tested, or outside it? This is the agent equivalent of SAE's operational design domain [@sae].

Table 2 applies these properties to common agent actions and gives a default level.

TABLE Example classification of agent actions and default autonomy level, proposed by the author for a typical small or mid-sized business. Levels refer to Table 1. || Defaults are starting points; a business should adjust them to its own risk tolerance.
Action | Reversible | Impact | Default level
Search records, summarize documents, answer internal questions | Yes (no change) | Low | L5 Observer
Draft an email, quote or work order for a person to send | Yes | Low | L4–L5
Update a non-financial field, such as a contact or a status | Mostly, with history | Low–medium | L4 with logging
Send a routine message to a customer or supplier | No | Medium | L3–L4, sampled
Post an invoice or issue a refund under a set limit | Partly, via reversal | Medium, bounded | L4; L5 below limit after promotion
Pay a new supplier, change bank details, approve a contract | No | High | L1–L2 with two-person rule
Change a production setpoint or a safety system | No | High, safety | Not delegated to the agent

The table encodes a few principles. Read-only actions can run with high autonomy because their only risk is a wrong answer, which is controlled by evaluation and by the reader. Actions with external effects need more oversight than internal ones. Impact can be capped by limits, which turns a high-impact action class into a bounded one. And some actions, notably those affecting physical safety, should not be delegated at all; an agent can advise on them through the systems people already use.

### 4.2 When an approval step pays for itself

An approval step has a cost: the reviewer's time and the delay. It also has a benefit: the errors it catches. A simple expected-loss comparison makes the trade-off explicit. Let *p* be the probability that the agent's action is wrong, *C* the cost of an error that reaches the world, *d*<sub>a</sub> the probability that an error is caught without a reviewer (for example, by a downstream reconciliation), *d*<sub>h</sub> the probability that it is caught with a reviewer, and *c*<sub>r</sub> the cost of one review. Approval is worthwhile when the loss it avoids exceeds its cost:

EQ p · C · (d<sub>h</sub> − d<sub>a</sub>) &gt; c<sub>r</sub>

Consider refunds. Suppose the agent is wrong on 2 percent of refunds, an uncaught wrong refund costs $300 on average, a monthly reconciliation would catch 30 percent of errors anyway, and an attentive reviewer catches 90 percent. The left side of Eq. (1) is 0.02 × 300 × 0.6 = $3.60 per refund. If a review takes two minutes of a clerk's time at $40 per hour, the cost is about $1.33, so approval pays. If the error rate falls to 0.5 percent after improvements, the benefit drops to $0.90 and approval no longer pays for small refunds; a sample review is better. The same arithmetic shows why limits matter: for a refund above $2,000 the benefit of approval is large even at a low error rate.

### 4.3 Can the reviewers keep up?

Eq. (1) assumes the reviewer's detection rate *d*<sub>h</sub>. The research in Section 3 suggests that this rate falls when reviewers are overloaded or when nearly every request is correct [@goddard]. A second check is therefore a capacity constraint. If an agent generates *N* approval requests per day, each needing *t* minutes of genuine attention, and the reviewers can give *T* minutes a day to approvals, then:

EQ N · t ≤ T

When Eq. (2) is violated, reviews will be rushed and *d*<sub>h</sub> in Eq. (1) will fall toward *d*<sub>a</sub>, eliminating the benefit. The remedies are to reduce *N* by raising autonomy for low-risk actions, to reduce *t* by presenting better evidence, or to replace blanket approval with sampling. Figure 1 shows the resulting regions.

FIG fig1-oversight-regions || Where each form of oversight fits, as a function of the agent's error rate and the impact of an error. Approval pays above the curve given by Eq. (1); below it, sampling or monitoring is cheaper. The shaded band marks where the approval volume would exceed reviewer capacity under Eq. (2). Illustrative parameters from the refund example. || Chart with the agent's error rate on the horizontal axis, from 0.1 to 10 percent on a log scale, and the cost of an uncaught error on the vertical axis, from 10 to 10,000 dollars on a log scale. A downward-sloping line marks the break-even point of Eq. (1). Above the line the region is labelled approval pays; below it, sample and monitor. A band at high error rates is labelled approval queue exceeds capacity, fix the agent first. || Author's calculation from Eq. (1) and Eq. (2), with c<sub>r</sub> = $1.33, d<sub>h</sub> = 0.9 and d<sub>a</sub> = 0.3.

## Designing the human checkpoint

If approval is required, it should be designed so that the reviewer can actually exercise judgment. Five design elements follow from the research in Section 3.

### 5.1 Show the evidence, not just the action

The reviewer should see what the agent proposes to do, the inputs it used, the rule or precedent it relied on, and anything unusual about the case. For a change to a record, this means a before-and-after comparison. For a payment, it means the invoice, the purchase order and the receipt side by side, with discrepancies highlighted. This addresses the situation awareness problem identified by Endsley and Kiris [@endsley] and lets the reviewer calibrate trust to the case at hand rather than to the agent in general [@leesee].

### 5.2 Ask for a decision, not a click

Interfaces that default to approval encourage automation bias. Requiring the reviewer to confirm the specific value that matters (the amount, the recipient) or to choose between approve, edit and reject with no default makes it harder to approve without reading. Recording the reason for each rejection gives the data needed to improve the agent.

### 5.3 Sample what is not approved

Actions that run without approval should be sampled. A daily random sample of autonomous actions, reviewed with the same care as an approval, measures the agent's real error rate and keeps reviewers familiar with normal cases, which counters Bainbridge's second irony [@bain]. Sampling can be weighted toward higher-value or more novel cases.

### 5.4 Escalate on signals, not only on categories

The agent should escalate to a person when it meets conditions it was not tested on: a missing document, a value outside the historical range, conflicting instructions, a counterparty it has not seen, or low confidence in its own output. Anthropic's guidance on building agents recommends this kind of explicit stopping condition and human checkpoint, together with starting from the simplest design that works [@anth].

### 5.5 Make stopping easy and logging complete

Every agent should have a stop control that takes effect immediately, a way to roll back recent actions where they are reversible, and an audit log that records each action, its inputs, the identity under which it ran and who approved it. These are the operational counterpart of the oversight requirements in Article 14 of the EU AI Act [@euaia] and of the MANAGE function in the NIST AI Risk Management Framework, which calls for mechanisms to supersede, disengage or deactivate AI systems that perform outside their intended use [@nist]. The identity and logging design is covered in detail in a companion paper [@sec].

## Earning autonomy with evidence

### 6.1 Reliability is not a single number

An agent that completes a task correctly once may not complete it correctly every time. Yao and colleagues introduced the pass^k metric, the probability that an agent succeeds on all of *k* independent attempts at the same task, and found that even strong agents were inconsistent: in a simulated retail customer-service domain, a leading model succeeded on all eight attempts in fewer than 25 percent of tasks [@tau]. For autonomy decisions, consistency matters more than peak performance, because an autonomous agent repeats the same kind of action thousands of times.

### 6.2 How many clean trials are enough?

Promotion to a higher level of autonomy should rest on observed performance in conditions close to production. The most practical method is a shadow-mode trial, in which the agent prepares each action, a person does the work as usual, and the two are compared. A useful statistical guide is the rule of three [@hanley]: if *n* independent trials produce no errors, the upper bound of the 95 percent confidence interval on the true error rate is approximately

EQ p<sub>95</sub> ≈ 3 / n

For example, 300 shadow-mode invoices with no material error support a claim that the error rate is below about 1 percent with 95 percent confidence. Thirty clean trials support only a claim below 10 percent. Eq. (3) gives a minimum trial size for any target error rate and makes plain why a short pilot cannot justify full autonomy. Figure 2 plots the bound.

FIG fig2-rule-of-three || Upper 95 percent confidence bound on the error rate after a run of trials with no errors, from Eq. (3). Thirty clean trials bound the error rate below about 10 percent; three hundred, below about 1 percent. || Line chart with the number of consecutive error-free trials on the horizontal axis, from 10 to 1,000 on a log scale, and the 95 percent upper bound on the error rate on the vertical axis, from 0.3 to 30 percent on a log scale. The line falls steadily. Marked points: 30 trials gives 10 percent, 100 gives 3 percent, 300 gives 1 percent and 1,000 gives 0.3 percent. || Author's calculation from Eq. (3) [@hanley].

Two cautions apply. Eq. (3) assumes the trials are independent and representative; a month of trials in a quiet season may not represent year-end. And errors are not equally serious, so the trial should count material errors against the target and track minor ones separately.

### 6.3 A promotion and demotion path

Combining these elements gives a promotion path for each action class (Figure 3). An action starts at the level in Table 2 or one level lower. It is promoted when three conditions hold: the number of trials meets the bound from Eq. (3) for the target error rate, the errors that did occur were minor and have been fixed, and the business owner of the process signs off. Promotion is one level at a time.

FIG fig3-promotion-path || Evidence-based promotion path for one action class. The agent moves up one level at a time when the gate criteria are met, and moves down automatically on any demotion trigger. Gate criteria are the author's proposed defaults. || Staircase diagram with four steps from left to right: shadow mode, where the agent drafts and a person does the work; approve, where the agent acts after approval; act and sample, where the agent acts and a sample is reviewed; and act and monitor. Each step up is labelled with its gate: enough clean trials for the target error rate, all approval rejections explained, sample error rate on target for a set period. A return arrow from the top back down is labelled demotion triggers: material error, input outside the tested range, model or tool change, process change. || Drawn by the author.

Demotion should be automatic. An agent returns to the previous level when a material error occurs, when its inputs move outside the range it was tested on, or when anything in its configuration changes: a new model version, a changed tool, revised instructions or a change to the business process. Each of these invalidates the evidence that justified the current level, much as a change outside its operational design domain requires a driving system to hand back control [@sae]. Treating changes as demotion triggers also gives a natural place for regression testing.

TABLE Example promotion record for an accounts payable agent posting supplier invoices. Figures are illustrative. || Trial sizes follow Eq. (3).
Stage | Duration | Volume | Material errors | Decision
Shadow mode | 6 weeks | 340 invoices | 0 (3 minor coding differences) | Promote to approve; error rate bound ≈ 0.9%
Approve | 8 weeks | 610 invoices | 1 (duplicate invoice, caught by reviewer) | Fix duplicate check; extend trial
Approve, after fix | 6 weeks | 450 invoices | 0 | Promote to act and sample for invoices under $5,000 matched to a purchase order
Act and sample | Ongoing | 10% weekly sample | Tracked monthly | Above $5,000 and unmatched invoices stay at approve

Table 3 illustrates the path for an accounts payable agent. The record it produces is also the evidence an auditor, a customer or a regulator will want to see: what the agent was allowed to do, on what basis, and how that changed over time.

## Conclusion

Autonomy is a design decision, and it should be made per action rather than per agent. The levels-of-automation literature offers a vocabulary for that decision, and the research on human oversight explains why the default answer, a human in the loop, so often fails: reviewers lose situation awareness, defer to the system and fall behind the queue.

The approach proposed here has four parts. Classify each action by reversibility, impact, detectability and novelty, and set a default level. Require approval only where Eq. (1) shows it pays for itself and Eq. (2) shows reviewers can keep up, and use sampling and monitoring elsewhere. Design the checkpoint so the reviewer sees evidence and makes a real decision. And let the agent earn autonomy through trials sized by the rule of three, one level at a time, with automatic demotion when the evidence no longer holds. Together these make oversight proportionate, keep people in the loops where they add value, and produce a record that shows why an agent is trusted to do what it does.
"""
