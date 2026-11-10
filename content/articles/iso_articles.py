"""ISO 9001 article series (V4.20). Writes articles/<slug>.json for gen/new_articles.py."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "articles"); FIGS = os.path.join(OUT, "figs")
DATE = "2026-11-09"

S_CHANGED = "iso-9001-2026-what-changed-from-2015"
S_PLAN = "iso-9001-2026-transition-plan"
S_SMB = "iso-9001-for-small-and-mid-sized-businesses"
S_AUDIT = "iso-9001-internal-audits-that-find-real-problems"
S_RISK = "iso-9001-risk-based-thinking-in-practice"
S_AI = "iso-9001-and-ai-using-ai-tools-inside-a-quality-system"
S_IMS = "integrated-management-system-iso-9001-14001-45001"
S_MR = "iso-9001-management-review-that-leadership-finds-useful"

SRC = {
 "iso": ("ISO: ISO 9001:2026, what businesses need to know", "https://www.iso.org/quality-management/iso-9001-2026"),
 "dnv": ("DNV: ISO 9001:2026 standard revision", "https://www.dnv.us/assurance/Management-Systems/new-iso/transition/iso-9001-revision/"),
 "dnvnews": ("DNV: The new edition of ISO 9001 is released", "https://www.dnv.com/ca/news/2026/ba_new-edition-of-the-quality-management-system-standard-iso-9001-released/"),
 "dqs": ("DQS: ISO 9001:2026, key changes, timeline and transition checklist", "https://www.dqsglobal.com/en/explore/blog/iso-9001-2026-changes-timeline-transition"),
 "dqst": ("DQS: ISO 9001:2026 is here (transition)", "https://www.dqsglobal.com/en/explore/blog/iso-9001-2026-transition"),
 "sgs": ("SGS: ISO 9001:2026 key updates and transition guidance", "https://www.sgs.com/en-gb/showcases/iso-9001-2026-key-updates-and-transition-guidance"),
 "qa19011": ("Quality Austria: ISO 19011:2026, new impulses for auditing management systems", "https://www.qualityaustria.com/en/news/iso-190112026-new-impulses-for-auditing-management-systems/"),
 "dqs14001": ("DQS: ISO 14001:2026 transition guide", "https://www.dqsglobal.com/en/explore/blog/iso-14001-2026-transition-guide"),
 "sgs45001": ("SGS: ISO 45001:2027 key updates and transition guidance", "https://www.sgs.com/en/showcases/iso-45001-2027-key-updates-and-transition-guidance"),
 "dnv45001": ("DNV: Draft version of ISO 45001 released", "https://www.dnv.com/ca/news/2026/draft-version-of-iso-45001-released/"),
 "iso42001": ("ISO: ISO/IEC 42001:2023, AI management systems", "https://www.iso.org/standard/42001"),
}


def fig(slug, caption, alt):
    svg = open(os.path.join(FIGS, slug + ".svg"), encoding="utf-8").read()
    svg = svg[svg.index("<svg"):]
    svg = re.sub(r'<svg ', f'<svg role="img" aria-label="{alt}" style="max-width:100%;height:auto;display:block;margin:0 auto" ', svg, count=1)
    svg = re.sub(r'\s(width|height)="[\d.]+pt"', "", svg, count=2)
    return f'<figure style="overflow-x:auto">{svg}<figcaption>{caption}</figcaption></figure>'


def sources(keys):
    return "<h2>Sources</h2><ul>" + "".join(f'<li><a href="{SRC[k][1]}" rel="noopener" target="_blank">{SRC[k][0]}</a></li>' for k in keys) + "</ul>"


def note(t):
    return f'<blockquote style="font-size:16.5px">{t}</blockquote>'


def link(slug, text):
    return f'<a href="post/{slug}.html">{text}</a>'   # sub_page() adds ../ for the post/ folder


CAVEAT = note("This article is based on ISO's announcement and on summaries published by certification bodies. It is not a substitute for the standard. Buy a copy of ISO 9001:2026 and confirm the requirements and your transition dates with your certification body.")
SERIES = lambda me: "<h2>More in this series</h2><ul>" + "".join(f"<li>{link(s, t)}</li>" for s, t in [
    (S_CHANGED, "ISO 9001:2026: what changed from 2015"), (S_PLAN, "Your ISO 9001:2026 transition plan"), (S_SMB, "ISO 9001 for small and mid-sized businesses"),
    (S_AUDIT, "Internal audits that find real problems"), (S_RISK, "Risk-based thinking in practice"), (S_AI, "ISO 9001 and AI"),
    (S_IMS, "Integrating ISO 9001, ISO 14001 and ISO 45001"), (S_MR, "Management review that leadership finds useful")] if s != me) + "</ul>"
CTA = '<p><strong>Want a second pair of eyes?</strong> Chmltech helps Canadian organizations build, simplify and audit quality management systems. <a href="../book.html">Book a strategy call</a> or <a href="../contact.html">ask a question</a>.</p>'

A = []

# ------------------------------------------------------------------ 1
A.append(dict(slug=S_CHANGED, title="ISO 9001:2026: What Changed from 2015 and What It Means for You",
 desc="ISO 9001:2026 replaced the 2015 edition in September 2026. A clause-by-clause look at what changed, what did not, and who needs to act by September 2029.",
 cats=["iso"], tags=["ISO 9001:2026", "quality management", "transition", "quality culture", "risk and opportunity"],
 body=f'''
<p>ISO published the sixth edition of ISO 9001 on 16 September 2026. It replaces ISO 9001:2015, the edition that most certified organizations have worked to for a decade. If you hold a certificate, you have until 30 September 2029 to move to the new edition. If you are planning to get certified, you will soon be audited against it.</p>
<p>The short version: this is an update, not a rebuild. Certification bodies describe the changes as evolutionary. The structure, the process approach, the plan-do-check-act cycle and risk-based thinking all stay. The new material is concentrated in leadership and planning.</p>
{CAVEAT}
<h2>What changed, clause by clause</h2>
{fig(S_CHANGED, "Where ISO 9001:2026 differs from ISO 9001:2015. Compiled from summaries by DNV, DQS and SGS.", "Table-style diagram of ISO 9001 clauses 3 to 10 and Annex A, shaded by amount of change. Main changes are in clause 5 Leadership, clause 6 Planning and Annex A. Smaller changes are in clauses 3, 4, 7 and 10. Clauses 8 and 9 are largely unchanged.")}
<table>
<tr><th>Clause</th><th>What changed</th><th>What to check in your system</th></tr>
<tr><td>3 Terms</td><td>The terms shared by all ISO management system standards are now listed in the standard, with less reliance on ISO 9000.</td><td>Nothing to change. Use the new definitions when you train auditors.</td></tr>
<tr><td>4.1, 4.2 Context</td><td>The climate change wording added by the 2024 amendment is now part of the text.</td><td>Your context review should record whether climate change is a relevant issue, and why or why not.</td></tr>
<tr><td>5.1.1 Leadership</td><td>Top management must promote quality culture and ethical behaviour.</td><td>How do leaders show this in practice? An auditor will ask them directly.</td></tr>
<tr><td>5.2 Quality policy</td><td>The policy must reflect the organization's context and support its strategic direction more explicitly.</td><td>Read the policy next to your strategy. Does one follow from the other?</td></tr>
<tr><td>6.1 Risks and opportunities</td><td>Split into subclauses 6.1.1 to 6.1.3, with actions for risks and actions for opportunities addressed separately.</td><td>If your register lists only threats, add opportunities and the actions tied to each.</td></tr>
<tr><td>6.3 Planning of changes</td><td>Requirements reinforced, with more emphasis on communicating, monitoring and reviewing changes.</td><td>Pick two recent changes and trace how they were planned and followed up.</td></tr>
<tr><td>7.1.4, 7.3 Support</td><td>The work environment and awareness clauses now refer to quality culture and ethical behaviour.</td><td>Update induction and refresher training, and keep a record that people received it.</td></tr>
<tr><td>8 Operation, 9 Performance evaluation</td><td>Minimal change: wording and layout.</td><td>Renumber references if clause numbers moved.</td></tr>
<tr><td>10 Improvement</td><td>Continual improvement requirements consolidated.</td><td>Renumber references.</td></tr>
<tr><td>Annex A</td><td>Rewritten and expanded to explain the intent of clauses 4 to 10. It is guidance and adds no requirements.</td><td>Read it. It is the best free explanation of what auditors will look for.</td></tr>
</table>
<h2>The two changes that need real work</h2>
<h3>Quality culture and ethical behaviour</h3>
<p>These are now explicit requirements on top management, and people across the organization must be aware of them. This is the change most likely to produce audit findings, because it cannot be met with a document alone. An auditor will look for evidence in behaviour: what happens when someone reports a problem, how a missed shipment date is weighed against releasing product that is not right, and what leaders talk about when they walk the floor.</p>
<p>Practical evidence includes a short statement of expected conduct that people recognize, leaders who can describe how they reinforce it, a way to raise concerns without penalty, and examples of decisions where quality or honesty came before convenience.</p>
<h3>Risks and opportunities, separately</h3>
<p>The 2015 edition asked for "risks and opportunities" in one breath, and many organizations responded with a risk register and nothing else. The new edition separates the two. You will need to show that you look for opportunities, such as a new market, a better process or a new technology, and that you plan actions for them as deliberately as for threats. Our article on {link(S_RISK, "risk-based thinking in practice")} gives a worked example.</p>
<h2>What did not change</h2>
<ul>
<li>The ten-clause structure shared with ISO 14001 and ISO 45001.</li>
<li>The process approach and the plan-do-check-act cycle.</li>
<li>Clause 8, where most of your operating procedures sit.</li>
<li>The standard remains technology-neutral. It adds no specific requirement about artificial intelligence or digital tools.</li>
</ul>
<h2>Who needs to do what</h2>
<table>
<tr><th>Your situation</th><th>What to do</th></tr>
<tr><td>Certified to ISO 9001:2015</td><td>Plan your transition for a scheduled surveillance or recertification audit before 30 September 2029. Do not leave it to the final year.</td></tr>
<tr><td>Working toward first certification</td><td>Build to the 2026 edition now. Certification bodies report that new certificates to the 2015 edition stop being issued in spring 2028, and a certificate issued to the old edition would expire with the transition period.</td></tr>
<tr><td>Not certified, but customers ask for conformance</td><td>Use the 2026 edition as your reference and tell customers which edition your system follows.</td></tr>
</table>
<p>The transition rules are set by the international accreditation community, now called Global ACI, and applied by your certification body. Our {link(S_PLAN, "step-by-step transition plan")} sets out the work in order.</p>
<h2>Key points</h2>
<ul>
<li>ISO 9001:2026 was published on 16 September 2026. ISO 9001:2015 certificates stop being valid after 30 September 2029.</li>
<li>Most of your system stays as it is. The work is in leadership (culture, ethics, policy) and planning (risks, opportunities, changes).</li>
<li>Culture and ethics need evidence in behaviour, so start with your leadership team.</li>
</ul>
{CTA}
{sources(["iso", "dnv", "dqs", "dqst", "sgs"])}
{SERIES(S_CHANGED)}'''))

# ------------------------------------------------------------------ 2
A.append(dict(slug=S_PLAN, title="Your ISO 9001:2026 Transition Plan: A Step-by-Step Roadmap",
 desc="A practical roadmap for moving a certified quality system from ISO 9001:2015 to ISO 9001:2026 before the September 2029 deadline, with a checklist.",
 cats=["iso"], tags=["ISO 9001:2026", "transition plan", "gap assessment", "internal audit", "certification"],
 body=f'''
<p>Organizations certified to ISO 9001:2015 have until 30 September 2029 to move to ISO 9001:2026. Three years sounds generous. In practice the window is shorter, because your certification body has to become accredited for the new edition first, and because the sensible moment to transition is at an audit you already have scheduled. This roadmap sets out the work in the order that causes the least disruption.</p>
{CAVEAT}
<h2>The timeline you are working within</h2>
{fig(S_PLAN, "Transition milestones reported by certification bodies, with the five steps of your own work below. Confirm dates with your certification body.", "Timeline from 16 September 2026, when ISO 9001:2026 was published, through 2027 when certification bodies become accredited, spring 2028 when new certificates are issued to the 2026 edition only, to 30 September 2029 when 2015 certificates stop being valid. Below are five steps: gap assessment, update policy and planning, training, internal audit and management review, and the transition audit.")}
<p>Count your audits. A three-year certificate has two surveillance audits and one recertification audit. Find which of them fall between mid-2027 and mid-2029, and pick one as your transition audit. If your recertification audit falls in that period, it is usually the natural choice, since the auditor reviews the whole system anyway. Leave at least one audit cycle in reserve in case findings need to be closed.</p>
<h2>Step 1: Read the standard and run a gap assessment</h2>
<p>Buy the standard and read Annex A first, since it explains the intent of each clause. Then compare your system to the changed clauses. For most organizations the gap assessment takes a day or two, because the changes are limited. Our article on {link(S_CHANGED, "what changed from 2015")} lists them.</p>
<table>
<tr><th>Question</th><th>Where to look</th></tr>
<tr><td>Does our context review say whether climate change is relevant to us?</td><td>Context and interested-parties record (4.1, 4.2)</td></tr>
<tr><td>Can each member of top management explain how they promote quality culture and ethical behaviour?</td><td>Interview them (5.1.1)</td></tr>
<tr><td>Does the quality policy follow from our strategy and context?</td><td>Policy next to the strategic plan (5.2)</td></tr>
<tr><td>Do we plan actions for opportunities as well as for risks?</td><td>Risk and opportunity register (6.1)</td></tr>
<tr><td>When we change a process, do we communicate, monitor and review the change?</td><td>Two or three recent changes (6.3)</td></tr>
<tr><td>Do people know what quality culture and ethical behaviour mean here?</td><td>Induction and training records; ask a few employees (7.3)</td></tr>
<tr><td>Do our documents cite clause numbers that have moved?</td><td>Manual, procedures, audit checklists</td></tr>
</table>
<h2>Step 2: Update policy, risk and change planning</h2>
<p>Close the gaps with the smallest change that works. Resist the urge to rewrite the manual.</p>
<ul>
<li><strong>Policy:</strong> revise it only if it does not connect to your strategy. One or two sentences usually do it.</li>
<li><strong>Risks and opportunities:</strong> add an opportunities section to your register, with an owner and action for each entry.</li>
<li><strong>Change planning:</strong> add three lines to your change form or procedure: who needs to be told, how the change will be monitored, and when it will be reviewed.</li>
<li><strong>Culture and ethics:</strong> agree with top management a short description of expected conduct and how leaders will reinforce it. If you already have a code of conduct, link it to the quality system.</li>
<li><strong>References:</strong> update clause numbers in documents and audit checklists.</li>
</ul>
<h2>Step 3: Train leaders, staff and internal auditors</h2>
<p>Three groups need three different things. Top management needs an hour on what is now expected of them personally. All staff need a short awareness session on quality culture and ethical behaviour, recorded. Internal auditors need training on the new edition before they audit to it. The auditing guideline, ISO 19011, was itself revised in 2026, so this is a good moment to refresh auditor training more broadly; see {link(S_AUDIT, "internal audits that find real problems")}.</p>
<h2>Step 4: Internal audit and management review to the new edition</h2>
<p>Your certification body will expect to see that you have audited your own system against ISO 9001:2026 and that top management has reviewed the result. Run a full internal audit to the new edition, raise and close any findings, and hold a {link(S_MR, "management review")} that covers the transition explicitly. Keep the records. They are the first thing the transition auditor will ask for.</p>
<h2>Step 5: The transition audit</h2>
<p>Agree the date and format with your certification body early. Transition can take place at a surveillance audit, at a recertification audit, or at a separate audit. Ask whether extra audit time will be added and what it will cost. After a successful audit and closure of any findings, your certificate is reissued to ISO 9001:2026.</p>
<h2>Checklist</h2>
<ol>
<li>Copy of ISO 9001:2026 purchased and read.</li>
<li>Transition audit date agreed with the certification body.</li>
<li>Gap assessment completed and actions assigned.</li>
<li>Context review updated, including climate change.</li>
<li>Quality policy checked against strategy.</li>
<li>Risk register extended to opportunities.</li>
<li>Change planning updated.</li>
<li>Culture and ethics expectations agreed and communicated.</li>
<li>Top management, staff and internal auditors trained, with records.</li>
<li>Internal audit to the 2026 edition completed and findings closed.</li>
<li>Management review held, covering the transition.</li>
<li>Transition audit passed and certificate reissued.</li>
</ol>
<h2>Three mistakes to avoid</h2>
<ul>
<li><strong>Waiting until 2029.</strong> Auditor availability tightens near a deadline, and you lose your margin to close findings.</li>
<li><strong>Rewriting everything.</strong> Clauses 8 and 9 barely changed. A full rewrite adds cost and introduces errors.</li>
<li><strong>Treating culture as a document.</strong> An auditor will test it by talking to people.</li>
</ul>
{CTA}
{sources(["iso", "dnv", "dqst", "sgs"])}
{SERIES(S_PLAN)}'''))

# ------------------------------------------------------------------ 3
A.append(dict(slug=S_SMB, title="ISO 9001 for Small and Mid-Sized Businesses: Getting Certified Without the Paperwork Burden",
 desc="What ISO 9001 requires of a small or mid-sized business, what it does not, how certification works in Canada, and how to keep the system lean.",
 cats=["iso"], tags=["ISO 9001", "small business", "certification", "quality management system", "documentation"],
 body=f'''
<p>Many owners of small and mid-sized businesses approach ISO 9001 expecting a wall of binders. A customer or a tender has asked for a certificate, and the fear is that getting one means hiring a quality department and writing a procedure for everything. It does not. The standard asks for far less documentation than its reputation suggests, and a system built around how you already work is easier to certify and far more useful afterwards.</p>
<h2>What ISO 9001 asks for</h2>
<p>ISO 9001 sets out requirements for a quality management system: the way an organization makes sure it consistently provides what customers and regulations require, and improves over time. In plain terms, it asks you to do seven things.</p>
<ol>
<li>Understand your customers, your obligations and the conditions you operate in.</li>
<li>Have leaders who set direction for quality and take responsibility for it.</li>
<li>Plan: set objectives, and deal with the risks and opportunities that affect them.</li>
<li>Provide competent people, suitable equipment and controlled information.</li>
<li>Control how you sell, design, buy, produce and deliver.</li>
<li>Check results through measurement, internal audit and management review.</li>
<li>Fix problems at their cause and keep improving.</li>
</ol>
<p>The standard applies to any organization, whatever its size. It says what must be achieved and leaves the method to you.</p>
<h2>What it does not ask for</h2>
<p>Much of the paperwork people associate with ISO 9001 comes from older editions or from habit. The 2015 edition removed the requirement for a quality manual and for a fixed list of written procedures, and nothing in the published summaries of the 2026 edition brings them back.</p>
<table>
<tr><th>Common belief</th><th>What the standard requires</th></tr>
<tr><td>You need a quality manual.</td><td>Not required. You need a defined scope, a quality policy and quality objectives.</td></tr>
<tr><td>Every process needs a written procedure.</td><td>You decide what to document, based on what is needed for the process to run reliably. A simple, stable task done by trained people may need none.</td></tr>
<tr><td>You need a full-time quality manager.</td><td>Responsibilities must be assigned. In a small firm they are usually part of existing roles.</td></tr>
<tr><td>You need a formal risk management system.</td><td>You must consider risks and opportunities and act on them. The method can be simple; see {link(S_RISK, "risk-based thinking in practice")}.</td></tr>
<tr><td>You need special software.</td><td>Not required. Shared folders with version control and a spreadsheet are enough to start.</td></tr>
</table>
<p>What you do need to keep are records that show the system works: evidence of competence, calibration where measurement matters, supplier evaluations, checks before release, nonconformities and corrective actions, internal audits and management reviews.</p>
<h2>How certification works</h2>
{fig(S_SMB, "The path to certification and the three-year cycle that follows.", "Two-row flow diagram. Top row, your preparation: decide scope and who leads; gap assessment; close the gaps; run the system and keep records for two to three months; internal audit and management review. Bottom row, certification body: stage 1 audit of readiness and documents; stage 2 audit of the system in use; certificate valid three years; surveillance audits in years one and two; recertification audit in year three.")}
<p>Certification is carried out by an independent certification body. In Canada, look for one accredited by the Standards Council of Canada or by another accreditation body recognized internationally, because customers may not accept a certificate from a body that is not accredited. The audit has two stages. Stage 1 checks that the system is designed and ready. Stage 2 checks that it is in use and effective. The certificate is valid for three years, with a shorter surveillance audit each year and a recertification audit in the third year.</p>
<p>Build to ISO 9001:2026. It was published in September 2026 and replaces the 2015 edition; {link(S_CHANGED, "this article explains what changed")}.</p>
<h2>How long it takes and what drives the cost</h2>
<p>For a business with fewer than 50 people and reasonably orderly operations, six to nine months from decision to certificate is a realistic plan. Most of that time is spent running the system and collecting records, since an auditor needs to see it working over a period.</p>
<p>There are three kinds of cost. The certification body's fees depend mainly on headcount, the number of sites and the complexity of what you do, so ask two or three accredited bodies for quotes. Internal time is usually the largest cost, mostly from the person leading the project and from process owners. Outside help is optional. It is worth paying for a gap assessment, internal auditor training and a pre-audit check; it is rarely worth paying someone to write your system for you, because a system written by an outsider tends to describe a company that does not exist.</p>
<h2>A lean way to build it</h2>
<ol>
<li><strong>Define the scope.</strong> State which products, services and sites the certificate will cover.</li>
<li><strong>Map your main processes on one page.</strong> From enquiry to delivery, with the support processes around them. Name an owner for each.</li>
<li><strong>Compare with the standard.</strong> Note where you already meet a requirement and where you do not. Most businesses find they meet more than they expected.</li>
<li><strong>Close the gaps with the lightest fix.</strong> A checklist, a form or a short visual instruction is often better than a procedure.</li>
<li><strong>Set three to five objectives you already care about.</strong> On-time delivery, complaints, scrap or rework are common choices.</li>
<li><strong>Run it and keep records.</strong> Two to three months of evidence is typical before the stage 2 audit.</li>
<li><strong>Audit yourself and hold a management review.</strong> See {link(S_AUDIT, "internal audits that find real problems")} and {link(S_MR, "management review that leadership finds useful")}.</li>
</ol>
<h2>Is it worth it?</h2>
<p>If a customer requires the certificate, the commercial answer is simple. The longer-term value depends on how the system is built. A system that describes how you really work gives you clearer responsibilities, fewer repeated problems and a regular, fact-based review of the business. A system built only to pass the audit gives you a certificate and an annual chore. The standard is the same in both cases. The difference is in the choices you make while building it.</p>
{CTA}
{sources(["iso", "dqs", "sgs"])}
{SERIES(S_SMB)}'''))

# ------------------------------------------------------------------ 4
A.append(dict(slug=S_AUDIT, title="Internal Audits That Find Real Problems",
 desc="How to plan and run ISO 9001 internal audits that go beyond checking paperwork: risk-based programmes, better questions, well-written findings and corrective action.",
 cats=["iso", "process-improvement"], tags=["internal audit", "ISO 9001", "ISO 19011", "corrective action", "root cause"],
 body=f'''
<p>In many organizations the internal audit is the least valued part of the quality system. Once a year someone walks round with a checklist, confirms that procedures exist and forms are signed, and files a report that changes nothing. The certification auditor then arrives and finds the problems the internal audit missed.</p>
<p>It does not have to work that way. An internal audit is the one activity in which you examine your own processes with fresh eyes and with authority to ask awkward questions. Done well, it is the cheapest source of improvement you have.</p>
<h2>What the standard asks for</h2>
<p>ISO 9001 clause 9.2 requires internal audits at planned intervals to find out whether the quality system conforms to your own requirements and to the standard, and whether it is effectively implemented and maintained. You must plan an audit programme that takes account of the importance of the processes, changes affecting the organization and the results of earlier audits. Each audit needs defined criteria and scope, auditors who are objective and impartial, a report to the relevant managers, and correction and corrective action without undue delay. You keep records as evidence.</p>
<p>Two things are worth noticing. The clause asks whether the system is <em>effective</em>, which is a stronger test than whether it is followed. And it expects the programme to be weighted toward what matters, which means you do not have to audit everything equally.</p>
<h2>Plan by risk, not by calendar</h2>
<p>Auditing every process once a year, in the same order, spreads effort evenly over areas that do not need it. Rank your processes instead.</p>
<table>
<tr><th>Factor</th><th>Audit more often or in more depth when</th></tr>
<tr><td>Consequence of failure</td><td>A failure reaches the customer or affects safety or compliance</td></tr>
<tr><td>Recent performance</td><td>Complaints, rework or missed targets are rising</td></tr>
<tr><td>Change</td><td>New people, equipment, software, products or suppliers</td></tr>
<tr><td>Previous findings</td><td>Earlier findings were serious or have recurred</td></tr>
<tr><td>Time since last audit</td><td>The process has not been looked at for more than a year</td></tr>
</table>
<p>A process that scores high on several factors might be audited two or three times a year. A stable, low-consequence one might be audited every second year. Record the reasoning, and your programme meets the clause.</p>
<h2>Audit the process, not the document</h2>
<p>A checklist built by turning each sentence of a procedure into a yes-or-no question tests whether the paperwork matches the paperwork. Follow the work instead. Pick a real order, job or batch and trace it from start to finish, forwards or backwards. At each step ask the person doing it:</p>
<ul>
<li>What do you receive, and how do you know it is right?</li>
<li>How do you know what to do, and what do you do when the instruction does not fit?</li>
<li>How do you know your result is good before you pass it on?</li>
<li>What goes wrong most often, and what happens then?</li>
<li>What would you change?</li>
</ul>
<p>Then check what you were told against the records. The interesting findings sit in the gaps between the procedure, what people say and what the records show, and at the handovers between departments.</p>
<h2>Write findings that can be acted on</h2>
{fig(S_AUDIT, "A complete finding has six parts. The auditor supplies the first three; the process owner supplies the rest.", "Six linked boxes. The auditor writes three: the requirement, the evidence observed, and the gap stated as fact. The process owner completes three: the cause, the corrective action with owner and date, and later verification that the problem has not recurred.")}
<p>Compare two versions of the same finding.</p>
<table>
<tr><th>Weak</th><th>Useful</th></tr>
<tr><td>Calibration procedure not followed.</td><td>Procedure QP-07 requires torque wrenches to be calibrated every 12 months. On 3 November, wrenches TW-04 and TW-09 at assembly cell 2 carried labels showing calibration due in June. Both were in use on customer orders.</td></tr>
</table>
<p>The second version states the requirement, the evidence and the gap. The process owner can verify it in minutes and cannot dispute it. It also invites the right next question: which jobs were assembled with those wrenches since June?</p>
<h2>From finding to corrective action</h2>
<p>Clause 10.2 separates two responses. <strong>Correction</strong> deals with the instance: calibrate the two wrenches and assess the product made with them. <strong>Corrective action</strong> deals with the cause, so that it does not happen again. Finding the cause means asking why the process allowed the gap. In this example, perhaps the recall list is kept by one person who was away, with no backup and no visible reminder. The corrective action then changes the process, such as a shared calendar with alerts and a monthly check by the cell leader. "Retrain the operator" is seldom a real cause.</p>
<p>Close the loop. Set a date to verify that the action worked, and check it. Repeated findings in the same area are a signal for {link(S_MR, "management review")}.</p>
<h2>Choose and develop auditors</h2>
<p>Auditors must not audit their own work. In a small company, the simplest answer is for departments to audit each other, which also spreads understanding of how the business fits together. Good auditors are curious, fair and persistent; knowledge of the standard can be taught. Give them a day of training, let them shadow an experienced auditor, and review their first reports with them.</p>
<p>The guideline for auditing management systems, ISO 19011, was revised in 2026. According to published summaries, the new edition gives more attention to remote and hybrid audits, to the use of digital tools and data analysis in auditing, and to the competence auditors need to use them. If you plan to use AI tools to prepare audits, see {link(S_AI, "ISO 9001 and AI")}.</p>
<h2>Six signs your audits are working</h2>
<ul>
<li>Findings refer to specific evidence and can be verified.</li>
<li>Some findings surprise the process owner.</li>
<li>Corrective actions change the process and not only the person.</li>
<li>The same finding does not come back the following year.</li>
<li>The certification auditor finds little that you had not already found.</li>
<li>Managers ask for audits of areas that worry them.</li>
</ul>
{CTA}
{sources(["qa19011", "dnv"])}
{SERIES(S_AUDIT)}'''))

# ------------------------------------------------------------------ 5
A.append(dict(slug=S_RISK, title="Risk-Based Thinking in Practice: Risks, Opportunities and a Register People Use",
 desc="What ISO 9001 means by risk-based thinking, how the 2026 edition separates risks from opportunities, and a worked example of a simple register.",
 cats=["iso"], tags=["risk-based thinking", "ISO 9001:2026", "risk register", "opportunities", "planning"],
 body=f'''
<p>Risk-based thinking is the part of ISO 9001 that people find hardest to pin down. The standard asks you to "determine the risks and opportunities that need to be addressed" but prescribes no method, and so organizations tend toward one of two extremes: an elaborate scoring spreadsheet that is updated the week before the audit, or a single sentence in the manual saying that risk is considered. Neither helps anyone make a decision.</p>
<p>The idea behind the clause is simple. Before something goes wrong, ask what could stop you from delivering what you promised, and do something about the answers that matter. This article shows a way to do that which fits on one page.</p>
<h2>What the standard requires</h2>
<p>Clause 6.1 asks you to consider your context and the needs of interested parties, determine the risks and opportunities that bear on the quality system achieving its intended results, plan actions to address them, build those actions into your processes, and evaluate whether they worked. Actions should be in proportion to the potential effect on products and services.</p>
<p>The standard does not require a formal risk management process or a documented risk register. A register is nonetheless the easiest way to show an auditor what you did, and to keep track yourself.</p>
<h2>What changed in 2026</h2>
<p>According to certification bodies' summaries, ISO 9001:2026 divides clause 6.1 into three subclauses, with actions to address risks and actions to address opportunities treated separately, and with expanded guidance in Annex A. The practical consequence is that a register containing only threats will no longer be enough. You will be expected to show that you looked for opportunities and planned for them. See {link(S_CHANGED, "what changed from 2015")} for the other changes.</p>
<h2>Step 1: Find the risks that matter</h2>
<p>Start from your processes and objectives. For each main process, ask the owner and two or three people who do the work:</p>
<ul>
<li>What could stop this process from delivering what the next step or the customer needs?</li>
<li>What has gone wrong before, here or at a competitor?</li>
<li>What are we dependent on: one supplier, one person, one machine, one system?</li>
<li>What is changing in the next year?</li>
</ul>
<p>You will collect more items than you need. Keep those that could affect customers, compliance or your objectives, and drop the rest. Ten to twenty risks is plenty for a small or mid-sized business.</p>
<h2>Step 2: Rank them simply</h2>
<p>Rate likelihood and impact as low, medium or high, and agree in a sentence what each level means for you. Three levels are enough. Five-point scales multiplied into scores from 1 to 25 give an appearance of precision that the underlying judgments do not support, and people spend the meeting arguing about whether something is a 3 or a 4.</p>
{fig(S_RISK, "Five example risks for a small plastics moulder, placed on a three-by-three grid. Items toward the upper right get action first.", "Three-by-three risk grid with likelihood on the vertical axis and impact on the horizontal axis. R1, single-source resin supplier, is high likelihood and high impact. R2, calibration overdue, is high likelihood and medium impact. R3, key setter retires, is medium likelihood and high impact. R4, drawing revision mix-up, is medium likelihood and low impact. R5, late customer specification changes, is low likelihood and medium impact.")}
<h2>Step 3: Decide what to do</h2>
<p>For each risk in the upper right of the grid, choose a response: avoid it, reduce its likelihood, reduce its impact, share it through a contract or insurance, or accept it knowingly. Give each action an owner and a date, and put it where the work is done, in a procedure, a checklist or a purchase specification. A risk whose only action is "monitor" has not been addressed.</p>
<table>
<tr><th>Ref</th><th>Risk</th><th>Rating</th><th>Action</th><th>Owner</th><th>How we will know it worked</th></tr>
<tr><td>R1</td><td>One approved supplier for the main resin grade; a stoppage halts three product lines</td><td>High / High</td><td>Qualify a second supplier; hold four weeks of stock until then</td><td>Purchasing</td><td>Second source approved; no line stoppage for lack of resin</td></tr>
<tr><td>R2</td><td>Gauges used past their calibration date</td><td>High / Medium</td><td>Shared recall calendar with alerts; monthly check by cell leader</td><td>Quality</td><td>No overdue gauges at monthly check</td></tr>
<tr><td>R3</td><td>The only setter who can run the large press retires next year</td><td>Medium / High</td><td>Train two setters; write setup sheets with photographs</td><td>Production</td><td>Two people signed off before retirement date</td></tr>
<tr><td>R4</td><td>Job run to a superseded drawing</td><td>Medium / Low</td><td>Drawing revision shown on the job traveller and checked at first-off</td><td>Engineering</td><td>No rework from revision errors</td></tr>
<tr><td>R5</td><td>Customer changes a specification after tooling is ordered</td><td>Low / Medium</td><td>Accept; contract terms cover the cost of change</td><td>Sales</td><td>Change costs recovered</td></tr>
</table>
<h2>Step 4: Do the same for opportunities</h2>
<p>An opportunity is a condition you could use to improve results. The questions are the mirror image of those for risks: what could we do better, faster or for someone new, and what is changing that we could take advantage of? Rate each by benefit and by effort, and plan the good ones in the same way.</p>
<table>
<tr><th>Ref</th><th>Opportunity</th><th>Benefit / Effort</th><th>Action</th><th>Owner</th><th>How we will know it worked</th></tr>
<tr><td>O1</td><td>Customers ask for recycled-content parts</td><td>High / Medium</td><td>Trial two recycled grades; offer to three customers</td><td>Sales, Engineering</td><td>First order for a recycled-content part</td></tr>
<tr><td>O2</td><td>In-mould sensors could detect short shots automatically</td><td>Medium / Medium</td><td>Pilot on one press for three months</td><td>Production</td><td>Scrap rate on pilot press compared with baseline</td></tr>
<tr><td>O3</td><td>Complaint data is recorded but never analyzed</td><td>Medium / Low</td><td>Monthly Pareto chart reviewed at the production meeting</td><td>Quality</td><td>Top complaint cause reduced</td></tr>
</table>
<h2>Step 5: Keep it alive</h2>
<p>A register is useful only if it changes as the business changes. Three habits keep it current:</p>
<ul>
<li>Review it at every {link(S_MR, "management review")}: what happened, which actions are done, what is new.</li>
<li>Add to it when something changes, such as a new product, customer, supplier, system or regulation.</li>
<li>Feed it from experience. A serious nonconformity or complaint often reveals a risk that was missing.</li>
</ul>
<p>Evaluate effectiveness honestly. If a risk you rated low came true, or an action did not prevent a problem, record that and adjust. Auditors are reassured by a register that shows learning, and suspicious of one in which every action is "complete" and every risk has fallen.</p>
<h2>Common mistakes</h2>
<ul>
<li><strong>Listing generic risks.</strong> "Loss of key customer" appears in every register and prompts no action. Name the customer, the cause and the consequence.</li>
<li><strong>Scoring without acting.</strong> The value is in the action column.</li>
<li><strong>Keeping risk separate from the work.</strong> If the action is not in a procedure, plan or budget, it will not happen.</li>
<li><strong>Ignoring opportunities.</strong> Under the 2026 edition this will be a visible gap.</li>
</ul>
{CTA}
{sources(["dnv", "dqs", "sgs"])}
{SERIES(S_RISK)}'''))

# ------------------------------------------------------------------ 6
A.append(dict(slug=S_AI, title="ISO 9001 and AI: Using AI Tools Inside a Quality System",
 desc="Where AI tools help in an ISO 9001 quality system (document control, audit preparation, nonconformity trends) and the controls that keep their use auditable.",
 cats=["iso", "artificial-intelligence"], tags=["ISO 9001", "artificial intelligence", "document control", "internal audit", "nonconformity analysis"],
 body=f'''
<p>Quality systems run on text: procedures, work instructions, audit reports, complaints, nonconformity reports and meeting minutes. Language models are good at exactly this kind of material. They can draft, summarize, compare and classify it in seconds. For a quality team that is usually short of time, that is a real opportunity.</p>
<p>It also raises a fair question from auditors and customers: if an AI tool wrote part of your procedure or sorted your complaints, how do you know the result is right? This article sets out where AI tools help, where they do not, and the controls that keep their use consistent with ISO 9001.</p>
<h2>What the standard says about AI</h2>
<p>Nothing specific. ISO 9001:2026 remains technology-neutral; according to certification bodies' summaries, it adds no requirement about artificial intelligence. That cuts both ways. You are free to use AI tools, and the existing requirements apply to whatever they produce. A procedure drafted by a model must still be reviewed and approved. An analysis produced by a model is still your analysis, and you are accountable for decisions based on it.</p>
<p>Two related standards are worth knowing. ISO 19011, the auditing guideline, was revised in 2026, and published summaries say it now addresses digital audit tools and AI-supported procedures, with attention to confidentiality and information security. ISO/IEC 42001:2023 is a separate management system standard for organizations that develop or use AI systems. It is not required for ISO 9001, but it shares the same clause structure and is a useful reference if AI becomes central to your operations.</p>
<h2>Four uses that pay off</h2>
{fig(S_AI, "AI tools prepare material in four areas of the quality system. A named person reviews and approves before anything becomes a controlled result.", "Diagram. Four boxes on the left list uses of AI with their ISO 9001 clauses: document control, clause 7.5; audit preparation, clause 9.2; nonconformity trends, clauses 9.1 and 10.2; training and answers, clauses 7.2 and 7.3. Arrows lead to a central box, human review and approval by a named owner, and then to a controlled result in the quality system. Controls on the AI tool itself are listed above: risk assessment, supplier control, competence, confidentiality and a record of use.")}
<h3>1. Document control</h3>
<p>Models are useful for turning a rough process description into a clear draft, simplifying wording for the people who use the instruction, comparing two versions and listing what changed, and checking a set of documents for contradictions and broken cross-references. They are also good at mapping a procedure against the clauses of the standard to show where a requirement is not addressed.</p>
<p>The control is the one clause 7.5 already requires: review and approval for suitability and adequacy by an authorized person before release. The reviewer should be someone who knows the process, and should check the draft against how the work is really done.</p>
<h3>2. Audit preparation</h3>
<p>Given a procedure and the relevant clause, a model can propose audit questions, suggest what records to sample, and summarize previous audit reports and open actions for the area. After the audit it can help turn notes into a clearly worded finding. This saves preparation time, which is often what limits the depth of {link(S_AUDIT, "internal audits")}.</p>
<p>The control: the auditor stays responsible for the plan, the evidence and the conclusion. A model has not seen the shop floor. It must never be the source of audit evidence.</p>
<h3>3. Nonconformity and complaint trends</h3>
<p>Most organizations record nonconformities and complaints as free text and rarely analyze them, because reading and coding hundreds of entries is tedious. A model can assign each entry to a category such as product, defect type, process step or likely cause, group similar entries and draft a summary. That turns a pile of reports into a Pareto chart for {link(S_MR, "management review")}.</p>
<p>The control: check a sample. Have a person code 30 to 50 entries independently and compare. If agreement is poor, tighten the category definitions and repeat. Keep the categories stable from period to period, or trends will reflect the tool and not the process.</p>
<h3>4. Training and answers from your own documents</h3>
<p>An assistant that answers employees' questions from your approved procedures, with a link to the source paragraph, makes the quality system easier to use than a folder of files. This is retrieval-augmented generation; our journal paper on <a href="post/retrieval-augmented-generation-design-evaluation-and-failure-analysis.html">its design and failure modes</a> explains how it works and where it goes wrong.</p>
<p>The control: the assistant must draw only on current, approved documents, show its sources, and say when it does not know. Test it with questions whose answers you know before releasing it.</p>
<h2>Where to be careful</h2>
<table>
<tr><th>Risk</th><th>What it looks like</th><th>Control</th></tr>
<tr><td>Confident errors</td><td>A plausible clause reference, tolerance or step that is wrong</td><td>Human review against the source; never release unreviewed output</td></tr>
<tr><td>Confidentiality</td><td>Customer drawings or personal data pasted into a public tool</td><td>Approved tools only; rules on what may be entered; contract terms on data use</td></tr>
<tr><td>Uncontrolled change</td><td>The vendor updates the model and results shift</td><td>Record the tool and version; re-check after updates</td></tr>
<tr><td>Loss of ownership</td><td>Procedures nobody in the company has really read</td><td>Named process owner approves every document</td></tr>
<tr><td>Decisions on product</td><td>A model decides whether product is released</td><td>Treat as a process requiring validation, with defined criteria and monitoring</td></tr>
</table>
<p>The last row deserves emphasis. Using a model to help write a procedure is low risk, because a person reviews the result. Using a model to accept or reject product is a different matter. It becomes part of the production and release process and needs the validation, monitoring and records you would apply to any automated inspection.</p>
<h2>Controls that keep an auditor comfortable</h2>
<ul>
<li><strong>A short policy on AI use</strong> in the quality system: which tools are approved, for what tasks, and what may not be entered.</li>
<li><strong>Risk assessment</strong> of each use, recorded in your {link(S_RISK, "risk register")} (clause 6.1).</li>
<li><strong>Supplier control</strong> of the AI provider, as for any external provider whose service affects your system (clause 8.4).</li>
<li><strong>Competence:</strong> train users in what the tools can and cannot do (clause 7.2).</li>
<li><strong>Human approval</strong> of every controlled document and record (clause 7.5).</li>
<li><strong>A record</strong> that AI assistance was used, where it matters, so that results can be traced.</li>
</ul>
<h2>How to start</h2>
<p>Choose one low-risk use, such as a monthly summary of complaints or drafts of revised work instructions. Define how a person will check the output. Run it for two or three months and measure the time saved and the errors caught at review. Then decide whether to extend it. This is the plan-do-check-act cycle applied to the tool, and it produces the evidence an auditor will want to see.</p>
<p>Chmltech works at this junction of quality systems and AI. If you would like help choosing a first use or setting up the controls, <a href="../artificial-intelligence.html">see our AI services</a> or <a href="../book.html">book a strategy call</a>.</p>
{sources(["dqs", "qa19011", "iso42001"])}
{SERIES(S_AI)}'''))

# ------------------------------------------------------------------ 7
A.append(dict(slug=S_IMS, title="One System, Three Standards: Integrating ISO 9001, ISO 14001 and ISO 45001",
 desc="How to run quality, environmental and health and safety management as one integrated system: what to share, what to keep separate, and how to phase the work.",
 cats=["iso", "esg"], tags=["integrated management system", "ISO 9001", "ISO 14001", "ISO 45001", "harmonized structure"],
 body=f'''
<p>Many organizations that hold ISO 9001 are later asked for ISO 14001 (environmental management) or ISO 45001 (occupational health and safety). The common mistake is to build each as a separate system, with its own manual, its own audits, its own review meeting and often its own coordinator. The result is three sets of paperwork describing one business.</p>
<p>The standards were designed to avoid this. All three follow the same ten-clause layout, called the Harmonized Structure, with much of the text in common. That makes it practical to run one management system that meets all three.</p>
<h2>What the three standards share</h2>
{fig(S_IMS, "The shared core is built once and serves all three standards. Each standard adds its own subject-specific requirements.", "Diagram with three columns above a shared base. The columns are ISO 9001 Quality, with customer requirements, design and development, external providers, and release and nonconforming outputs; ISO 14001 Environment, with environmental aspects, compliance obligations, life cycle perspective and emergency preparedness; and ISO 45001 Health and safety, with hazard identification, worker consultation and participation, emergency preparedness and incident investigation. The shared base lists context and interested parties, leadership and policy, objectives, risks and opportunities, competence and awareness, communication, documented information, internal audit, management review, and corrective action and improvement.")}
<table>
<tr><th>Clause</th><th>Shared element</th><th>How to integrate it</th></tr>
<tr><td>4</td><td>Context, interested parties, scope</td><td>One context review covering customers, regulators, neighbours and workers</td></tr>
<tr><td>5</td><td>Leadership, policy, roles</td><td>One policy statement, or three short ones on a page; one responsibility chart</td></tr>
<tr><td>6</td><td>Risks, opportunities, objectives</td><td>One register with a column for the type of risk; one set of objectives</td></tr>
<tr><td>7</td><td>Competence, awareness, communication, documents</td><td>One training matrix; one document control process</td></tr>
<tr><td>9</td><td>Monitoring, internal audit, management review</td><td>One audit programme; one review meeting with a combined agenda</td></tr>
<tr><td>10</td><td>Nonconformity, corrective action, improvement</td><td>One process and one log for quality problems, environmental incidents and safety incidents</td></tr>
</table>
<h2>What stays specific</h2>
<p>Integration does not mean blending everything. Each standard has requirements with no equivalent in the others, mostly in clauses 6 and 8, and these need people with the right knowledge.</p>
<ul>
<li><strong>ISO 9001:</strong> customer requirements, design and development, control of external providers, production and service provision, release, and nonconforming outputs.</li>
<li><strong>ISO 14001:</strong> environmental aspects and impacts, compliance obligations, a life cycle perspective, and emergency preparedness and response.</li>
<li><strong>ISO 45001:</strong> hazard identification and assessment of health and safety risks, consultation and participation of workers, emergency preparedness, and incident investigation.</li>
</ul>
<p>Legal requirements deserve particular care. Environmental and health and safety law imposes obligations with penalties attached, and the register of those obligations must be kept by someone competent to interpret them.</p>
<h2>Where the standards stand in 2026</h2>
<p>All three are being renewed, which makes this a good time to integrate.</p>
<table>
<tr><th>Standard</th><th>Status</th></tr>
<tr><td>ISO 9001</td><td>New edition published on 16 September 2026; transition by 30 September 2029. See {link(S_CHANGED, "what changed")}.</td></tr>
<tr><td>ISO 14001</td><td>New edition published in April 2026. Certification bodies expect a three-year transition; confirm the date with yours.</td></tr>
<tr><td>ISO 45001</td><td>Under revision. A draft was released in 2026 and certification bodies expect the new edition in 2027.</td></tr>
</table>
<p>If you hold two or three certificates, plan the transitions together. Updating the shared core once, to the new wording, is far less work than doing it three times.</p>
<h2>How to integrate in five steps</h2>
<ol>
<li><strong>Map what you have.</strong> List the documents, records, meetings and audits of each system side by side. Duplication will be obvious.</li>
<li><strong>Merge the core.</strong> Combine document control, training, internal audit, corrective action and management review first. These give the largest saving for the least risk.</li>
<li><strong>Combine risk and objectives.</strong> One register with quality, environmental and safety entries lets management see priorities across all three. Our article on {link(S_RISK, "risk-based thinking")} describes a simple format.</li>
<li><strong>Integrate at process level.</strong> Add environmental and safety controls to the operating procedure for each process, so that a work instruction covers how to do the job correctly, safely and without harm to the environment.</li>
<li><strong>Align the audits.</strong> Train internal auditors to audit a process against all three standards in one visit, and ask your certification body for a combined audit.</li>
</ol>
<h2>Benefits and trade-offs</h2>
<table>
<tr><th>Benefits</th><th>Trade-offs</th></tr>
<tr><td>Less duplication of documents, meetings and audits</td><td>Auditors and coordinators need broader competence</td></tr>
<tr><td>One picture of risk for management</td><td>A weakness in a shared process, such as corrective action, affects all three certificates</td></tr>
<tr><td>Fewer conflicting instructions for employees</td><td>Specialist topics can be diluted if no one owns them</td></tr>
<tr><td>Combined certification audits can take less total time than separate ones</td><td>Combined audits are longer single events and need more preparation</td></tr>
</table>
<p>The trade-offs are manageable if you keep a named owner for each discipline inside the integrated system. Integration removes duplicate administration. It should not remove expertise.</p>
<h2>Is integration right for you?</h2>
<p>It is the sensible default if you hold, or expect to need, two or more of the standards, and if the same managers are responsible for the activities they cover. It is less attractive if the certificates cover different sites or business units with separate management, or if one discipline is so heavily regulated that it needs its own governance. If you hold ISO 9001 only and expect to add another standard within two years, build your system now so that the shared core is ready to extend.</p>
{CTA}
{sources(["iso", "dqs14001", "sgs45001", "dnv45001"])}
{SERIES(S_IMS)}'''))

# ------------------------------------------------------------------ 8
A.append(dict(slug=S_MR, title="Management Review That Leadership Finds Useful",
 desc="How to turn the ISO 9001 management review from an annual formality into a decision meeting: required inputs and outputs, a one-page agenda and common pitfalls.",
 cats=["iso"], tags=["management review", "ISO 9001", "leadership", "quality objectives", "continual improvement"],
 body=f'''
<p>Ask a leadership team what they think of the ISO 9001 management review and the usual answer is a polite grimace. Once a year the quality manager presents forty slides, everyone agrees the system is "suitable, adequate and effective", the minutes are filed for the auditor, and nothing changes.</p>
<p>That is a wasted opportunity. The review is the one point at which the standard requires top management to look at how the organization is performing and to decide what to do about it. Run as a decision meeting, it is among the most useful hours leaders spend.</p>
<h2>What the standard requires</h2>
<p>Clause 9.3 requires top management to review the quality management system at planned intervals, to ensure that it remains suitable, adequate, effective and aligned with the organization's strategic direction. The clause lists what the review must consider and what it must produce. Certification bodies report that this clause changed very little in the 2026 edition.</p>
<table>
<tr><th>Required inputs</th><th>Question it answers for leaders</th></tr>
<tr><td>Status of actions from previous reviews</td><td>Did we do what we decided?</td></tr>
<tr><td>Changes in external and internal issues</td><td>What has changed around us and inside the business?</td></tr>
<tr><td>Customer satisfaction and feedback from interested parties</td><td>What do customers and others think of us?</td></tr>
<tr><td>Extent to which quality objectives have been met</td><td>Are we hitting our targets?</td></tr>
<tr><td>Process performance and conformity of products and services</td><td>Are our processes delivering?</td></tr>
<tr><td>Nonconformities and corrective actions</td><td>What went wrong, and has it stopped?</td></tr>
<tr><td>Monitoring and measurement results</td><td>What do the numbers show?</td></tr>
<tr><td>Audit results</td><td>What did internal and external audits find?</td></tr>
<tr><td>Performance of external providers</td><td>Are our suppliers reliable?</td></tr>
<tr><td>Adequacy of resources</td><td>Do we have the people, equipment and budget we need?</td></tr>
<tr><td>Effectiveness of actions on risks and opportunities</td><td>Did our precautions and initiatives work?</td></tr>
<tr><td>Opportunities for improvement</td><td>What should we do next?</td></tr>
</table>
<p>The required outputs are decisions and actions on three things: opportunities for improvement, any need for changes to the quality management system, and resource needs. You must keep a record of the results.</p>
<h2>Why most reviews fail</h2>
<ul>
<li><strong>They report and do not decide.</strong> Data is presented and noted. No one is asked to choose anything.</li>
<li><strong>They happen once a year.</strong> By then the data is stale and the list is too long to discuss properly.</li>
<li><strong>They belong to the quality manager.</strong> Leaders attend as an audience and not as owners.</li>
<li><strong>They are separate from running the business.</strong> The same people discuss the same performance in a different meeting the following week.</li>
</ul>
<h2>Turn it into a decision meeting</h2>
{fig(S_MR, "The review takes five groups of inputs and must produce three kinds of output. The meeting itself is for deciding.", "Diagram. Five input boxes on the left: actions from last review; changes in context, customers and regulations; performance of objectives, processes, customers and suppliers; audits and nonconformities; and resources, risks and opportunities. Arrows lead to a central box, the review meeting of 60 to 90 minutes with data sent in advance and decisions recorded in the room. Three output boxes on the right: improvement actions with owner and date; changes to the quality system; and resources approved or reallocated.")}
<p><strong>Send the data beforehand.</strong> A one- or two-page pack with trends, issued a week ahead, lets the meeting start from questions. Show each measure as a trend against its target, and mark the items that need a decision.</p>
<p><strong>Have process owners present their own results.</strong> The sales manager speaks to customer feedback, the production manager to process performance, the purchasing manager to suppliers. The quality manager coordinates and presents audit results.</p>
<p><strong>Frame each item as a decision.</strong> "On-time delivery fell from 94% to 88% in the quarter; the main cause is late material from two suppliers. Options: dual-source, or hold more stock. Recommendation: dual-source." Leaders then choose.</p>
<p><strong>Record decisions in the room.</strong> Each action gets an owner and a date before the meeting ends. That record is the evidence the standard asks for.</p>
<p><strong>Review more often.</strong> "Planned intervals" does not mean annually. A quarterly review of 60 to 90 minutes works better than an annual half-day. You can also cover the inputs across your existing monthly management meetings, provided every input is addressed over the year and you keep records.</p>
<h2>A one-page agenda</h2>
<table>
<tr><th>Time</th><th>Item</th><th>Lead</th><th>Decision sought</th></tr>
<tr><td>10 min</td><td>Actions from last review</td><td>Chair</td><td>Close, extend or escalate each open action</td></tr>
<tr><td>10 min</td><td>What has changed: customers, market, regulations, people, systems</td><td>General manager</td><td>Any change to scope, policy or objectives?</td></tr>
<tr><td>15 min</td><td>Customers: satisfaction, complaints, returns</td><td>Sales</td><td>Top one or two issues to act on</td></tr>
<tr><td>20 min</td><td>Performance: objectives, process measures, product conformity, suppliers</td><td>Process owners</td><td>Action on any measure off target</td></tr>
<tr><td>10 min</td><td>Audits, nonconformities and corrective actions</td><td>Quality</td><td>Recurring problems that need resources</td></tr>
<tr><td>10 min</td><td>Risks and opportunities: what happened, what is new</td><td>All</td><td>Update the register; approve new actions</td></tr>
<tr><td>10 min</td><td>Resources and improvement priorities</td><td>General manager</td><td>Approve people, equipment, training or budget</td></tr>
<tr><td>5 min</td><td>Summary of decisions</td><td>Chair</td><td>Confirm owners and dates</td></tr>
</table>
<p>The agenda covers every required input in 90 minutes. If you are moving to the 2026 edition, add an item on transition progress; see the {link(S_PLAN, "transition plan")}. Quality culture and ethical behaviour, which the new edition makes a responsibility of top management, also belong on this agenda once or twice a year.</p>
<h2>What good minutes look like</h2>
<p>Keep them to one page: date and attendees, the data pack attached, and a table of decisions with owner and date. An auditor will look for three things: that the required inputs were considered, that decisions were made, and that actions from the previous review were followed up. A long narrative adds nothing.</p>
<h2>Signs the review is working</h2>
<ul>
<li>Leaders ask for the data pack when it is late.</li>
<li>Each review produces a small number of decisions that would not otherwise have been made.</li>
<li>Actions are closed by the next review.</li>
<li>Resource requests are argued from data and are sometimes approved.</li>
<li>The findings of {link(S_AUDIT, "internal audits")} and the {link(S_RISK, "risk register")} change as a result of the discussion.</li>
</ul>
{CTA}
{sources(["sgs", "dnv"])}
{SERIES(S_MR)}'''))

os.makedirs(OUT, exist_ok=True)
for n, a in enumerate(A):
    words = len(re.sub(r"<svg.*?</svg>", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<svg.*?</svg>", " ", a["body"], flags=re.S)), flags=re.S).split())
    a.update(date=DATE, author="Quak Foo Lee", read=f"{max(1, round(words / 220))} min read", order=n, body=a["body"].strip())
    json.dump(a, open(os.path.join(OUT, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{words:5d} words  {a['slug']}")
