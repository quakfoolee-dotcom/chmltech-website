"""ISO category article (V4.67): ISO/IEC 42001 alongside ISO 9001.

Usage:  python3 content/articles/iso42001_article.py
        python3 content/gen/add_article.py iso-iec-42001-alongside-iso-9001-adding-ai-governance
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import (nowrap, svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, RED,
                           MUTED, LINE, SAND, PALE, GREENF, ORANGEF)
from refresh_articles import src, rel

SLUG = "iso-iec-42001-alongside-iso-9001-adding-ai-governance"
EUAI = "the-eu-ai-act-for-canadian-businesses-scope-obligations-and-a-compliance-path"


def fig_plan():
    rows = [("1. Inventory AI and set scope", 0, 4), ("2. AI policy and roles", 2, 4), ("3. Risk and impact assessment", 4, 8),
            ("4. Statement of Applicability", 7, 3), ("5. Lifecycle, data and supplier controls", 8, 10),
            ("6. Training and awareness", 10, 6), ("7. Internal audit", 17, 3), ("8. Management review", 20, 2),
            ("Certification audit, stages 1 and 2", 22, 4)]
    X = lambda w: 250 + w * 17.5; s = ""
    for w in range(0, 27, 4):
        s += f'<line x1="{X(w)}" y1="16" x2="{X(w)}" y2="{24 + len(rows) * 30}" stroke="{LINE}"/>' + txt(X(w), 12, f"Wk {w}", "middle", MUTED, 11.5)
    for i, (lab, a, d) in enumerate(rows):
        y = 24 + i * 30; cert = i == len(rows) - 1
        s += txt(240, y + 16, lab, "end", NAVY, 12.5, cert)
        s += f'<rect x="{X(a)}" y="{y + 4}" width="{d * 17.5}" height="18" rx="4" fill="{GREEND if cert else BLUE}" opacity="{1 if cert else .8}"/>'
    return svg("Gantt chart of a 26-week plan to add ISO/IEC 42001 to an ISO 9001 system. Inventory and scope in weeks 0 to 4; AI policy and roles weeks 2 to 6; "
               "risk and impact assessment weeks 4 to 12; Statement of Applicability weeks 7 to 10; lifecycle, data and supplier controls weeks 8 to 18; "
               "training weeks 10 to 16; internal audit weeks 17 to 20; management review weeks 20 to 22; certification audit weeks 22 to 26.",
               730, 24 + len(rows) * 30 + 6, s, 600, x0=0)


def article():
    body = f"""<p>Most small and mid-sized businesses now use AI somewhere: a chatbot on the website, an assistant that drafts quotes, a model that forecasts demand, an AI feature inside the ERP. Few have written down who is responsible for it, how it was checked, or what happens when it gets something wrong. Customers are starting to ask. So are auditors, insurers and, for firms that sell into Europe, regulators.</p>
<p>ISO/IEC 42001 is the international standard for answering those questions in a structured way. For a business that already runs an ISO 9001 quality system, it is not a second system to build from scratch. It uses the same structure, and much of the work extends what is already in place. This article explains what the standard requires, what an ISO 9001 business already has, what it needs to add, and a realistic plan to get there.</p>
<h2>What ISO/IEC 42001 is</h2>
<p>ISO and IEC published ISO/IEC 42001:2023 in December 2023 as the first international standard for an artificial intelligence management system (AIMS). It sets requirements for how an organization governs the AI it develops, provides or uses, and it is certifiable: an accredited certification body can audit the management system and issue a certificate, as for ISO 9001 or ISO/IEC 27001.</p>
<ul>
<li><strong>Clauses 4 to 10</strong> follow ISO's harmonized structure for management system standards, the same structure as ISO 9001: context, leadership, planning, support, operation, performance evaluation and improvement.</li>
<li><strong>Annex A</strong> lists 38 reference controls grouped under nine control objectives, numbered A.2 to A.10. An organization selects the controls that apply and justifies any exclusions in a Statement of Applicability, as in ISO/IEC 27001.</li>
<li><strong>Annex B</strong> gives implementation guidance for each control. Annexes C and D are informative, covering AI-related objectives and risk sources, and use across sectors.</li>
</ul>
<p>The standard certifies the management system, not a particular AI model or product. A certificate says that the organization governs its AI in a controlled, documented and improving way.</p>
<h2>What your ISO 9001 system already gives you</h2>
<p>Because both standards share the harmonized structure, an ISO 9001 business has the skeleton of an AI management system already. The table shows what carries over and what ISO/IEC 42001 adds at each clause.</p>
<table>
<tr><th>Clause</th><th>Already in ISO 9001</th><th>What ISO/IEC 42001 adds</th></tr>
<tr><td>4 Context</td><td>Internal and external issues, interested parties, scope</td><td>Your role for each AI system (developer, provider, user), and AI-specific issues such as legal requirements and the intended use</td></tr>
<tr><td>5 Leadership</td><td>Quality policy, roles and responsibilities</td><td>An AI policy and named accountability for AI</td></tr>
<tr><td>6 Planning</td><td>Risks and opportunities, quality objectives</td><td>AI risk assessment and treatment, and an <strong>AI system impact assessment</strong> covering effects on individuals, groups and society</td></tr>
<tr><td>7 Support</td><td>Resources, competence, awareness, documented information</td><td>Competence in AI, and resources such as data, tools and computing</td></tr>
<tr><td>8 Operation</td><td>Operational planning and control, outsourced processes</td><td>Operating the risk treatment, impact assessments and lifecycle controls from Annex A</td></tr>
<tr><td>9 Performance evaluation</td><td>Monitoring, internal audit, management review</td><td>Monitoring AI system performance and the effectiveness of AI controls</td></tr>
<tr><td>10 Improvement</td><td>Nonconformity and corrective action, continual improvement</td><td>The same processes, applied to AI incidents and failures</td></tr>
</table>
<p>The practical consequence: an ISO 9001 business keeps one management system. Document control, internal audit, management review and corrective action are extended to cover AI, not duplicated. Our article on <a href="integrated-management-system-iso-9001-14001-45001.html">integrating ISO 9001, 14001 and 45001</a> describes the same approach for environment and safety.</p>
<h2>What is genuinely new: the Annex A controls</h2>
<p>The new work sits mostly in Annex A. The nine control objectives are:</p>
<table>
<tr><th>Objective</th><th>What it covers</th><th>Typical evidence for an SME</th></tr>
<tr><td>A.2 Policies related to AI</td><td>An AI policy aligned with other policies, and its review</td><td>A two-page AI policy approved by management</td></tr>
<tr><td>A.3 Internal organization</td><td>Roles, responsibilities and a way to report concerns</td><td>A named AI owner; a route for staff to raise problems</td></tr>
<tr><td>A.4 Resources for AI systems</td><td>Data, tools, computing and people the AI depends on</td><td>An inventory of AI systems and what each uses</td></tr>
<tr><td>A.5 Assessing impacts of AI systems</td><td>Effects on individuals, groups and society</td><td>A short impact assessment for each significant AI use</td></tr>
<tr><td>A.6 AI system life cycle</td><td>Requirements, design, verification, deployment, operation and monitoring</td><td>Test results before release; monitoring after</td></tr>
<tr><td>A.7 Data for AI systems</td><td>Data quality, provenance and preparation</td><td>Where training or reference data comes from and how it is checked</td></tr>
<tr><td>A.8 Information for interested parties</td><td>What users and others are told about the AI</td><td>User guidance; disclosure that a chatbot is AI</td></tr>
<tr><td>A.9 Use of AI systems</td><td>Responsible use within intended purposes</td><td>Acceptable use rules for staff; human review where needed</td></tr>
<tr><td>A.10 Third-party and customer relationships</td><td>Suppliers of AI and customers who use your AI</td><td>Supplier questions on AI; contract terms; what customers are told</td></tr>
</table>
<p>The control most ISO 9001 businesses have not done before is the <strong>impact assessment</strong> (A.5). A quality risk assessment asks what could go wrong for the business and its customers. An AI impact assessment also asks what could go wrong for the people affected by the AI's output: a job applicant screened out, a customer given wrong advice, a supplier wrongly flagged. For most SME uses the answer is short. Writing it down is what matters.</p>
<p>Many SMEs use AI rather than build it. Their focus will be on A.9 and A.10: rules for how staff use AI tools, and what they ask of the suppliers whose AI they rely on. Our article on <a href="iso-9001-and-ai-using-ai-tools-inside-a-quality-system.html">using AI tools inside a quality system</a> covers the ISO 9001 side of that work.</p>
<h2>ISO/IEC 42001 and the EU AI Act</h2>
<p>ISO/IEC 42001 is voluntary, and certification to it does not by itself mean compliance with the EU Artificial Intelligence Act. It is not one of the harmonized standards whose use gives a presumption of conformity with the Act. It does produce much of the evidence the Act asks for: an inventory of AI systems, documented risk assessment, human oversight arrangements, records of testing and monitoring, and a process for incidents and corrective action. For a Canadian business with European customers, it is a sensible way to organize that work. Our journal paper on <a href="{EUAI}.html">the EU AI Act for Canadian businesses</a> explains when the Act applies and what it requires.</p>
<h2>Certification: how it works</h2>
<p>Certification follows the same path as ISO 9001. A stage 1 audit reviews the documented system and readiness. A stage 2 audit checks that the system works in practice. A certificate is issued for three years, with surveillance audits in between. ISO/IEC 42006:2025 sets the requirements for bodies that certify AI management systems, so check that your certification body is accredited for ISO/IEC 42001.</p>
<p>Costs vary widely with size, scope and how much of the system already exists. Published estimates run from under $10,000 in audit fees for a small organization with existing ISO infrastructure to well over $100,000 for a full program in a larger one. The largest saving comes from building on an existing ISO 9001 or ISO/IEC 27001 system rather than starting a separate one. Many SMEs do not need a certificate at all: aligning with the standard and keeping the evidence is enough until a customer asks for one.</p>
<h2>A 26-week plan for an ISO 9001 business</h2>
{fig(fig_plan(), 1, "A realistic plan for adding ISO/IEC 42001 to an existing ISO 9001 system in a small or mid-sized business. Steps overlap.")}
<ol>
<li><strong>Inventory AI and set the scope.</strong> List every AI system you build, sell or use, including AI features inside purchased software. Decide which are in scope.</li>
<li><strong>Write the AI policy and name the roles.</strong> Keep the policy short. Name one accountable owner and a route for staff to raise concerns.</li>
<li><strong>Assess risks and impacts.</strong> Extend your existing risk register to AI, and write a short impact assessment for each significant use.</li>
<li><strong>Prepare the Statement of Applicability.</strong> Go through the 38 Annex A controls, mark which apply and say why any do not.</li>
<li><strong>Put the controls in place.</strong> For most SMEs: testing before release, monitoring after, data source records, supplier questions and contract terms, and user disclosure.</li>
<li><strong>Train people.</strong> Short, role-based training on the AI policy and acceptable use.</li>
<li><strong>Audit internally.</strong> Add AI to your internal audit programme. Our article on <a href="iso-9001-internal-audits-that-find-real-problems.html">internal audits that find real problems</a> applies directly.</li>
<li><strong>Review with management.</strong> Add AI performance, incidents and changes to the <a href="iso-9001-management-review-that-leadership-finds-useful.html">management review</a> agenda.</li>
</ol>
<p>Then book the certification audit if you want a certificate. A firm transitioning to ISO 9001:2026 at the same time can combine the work, since the new edition also strengthens leadership and planning. See <a href="iso-9001-2026-transition-plan.html">our ISO 9001:2026 transition plan</a>.</p>
<h2>Key points</h2>
<ul>
<li>ISO/IEC 42001 is the certifiable international standard for governing AI, with the same structure as ISO 9001.</li>
<li>An ISO 9001 business already has most of the management system. The new work is in the 38 Annex A controls, especially impact assessment.</li>
<li>SMEs that use rather than build AI should focus on acceptable use (A.9) and suppliers (A.10).</li>
<li>Certification does not by itself mean compliance with the EU AI Act, but it produces much of the evidence the Act asks for.</li>
<li>Extend your existing system rather than building a second one. About six months is realistic.</li>
</ul>
<p><strong>Want help adding AI governance to your quality system?</strong> Chmltech helps small and mid-sized businesses build and maintain ISO 9001 systems and extend them to new requirements. <a href="../book.html">Book a strategy call</a>.</p>
{src([("ISO: ISO/IEC 42001:2023 Information technology – Artificial intelligence – Management system", "https://www.iso.org/standard/81230.html"),
      ("Advisori: ISO 42001 certification, a complete guide (Annex A structure; status under the EU AI Act)", "https://www.advisori.de/en/blog/iso-42001-certification-a-complete-guide-to-the-ai-management-system-standard"),
      ("Openlayer: ISO 42001, a complete guide to AI management systems (June 2026)", "https://www.openlayer.com/blog/iso-42001-ai-management-systems-guide.md"),
      ("Elevate: ISO 42001 certification vs compliance, cost differences in 2026", "https://elevateconsult.com/insights/iso-42001-certification-vs-compliance-understanding-the-cost-differences-in-2026/"),
      ("SOC 2 Auditors: ISO 42001 (certification, ISO/IEC 42006:2025)", "https://soc2auditors.org/frameworks/iso-42001/")])}
{rel([(EUAI, "The EU AI Act for Canadian businesses"),
      ("iso-9001-and-ai-using-ai-tools-inside-a-quality-system", "ISO 9001 and AI: using AI tools inside a quality system"),
      ("integrated-management-system-iso-9001-14001-45001", "One system, three standards: integrating ISO 9001, 14001 and 45001")])}"""
    body = nowrap(body, [(1, 0, 24), (2, 0, 36)])
    return dict(slug=SLUG, title="ISO/IEC 42001 Alongside ISO 9001: Adding AI Governance to the Quality System You Already Have",
                desc="What ISO/IEC 42001 requires, what an ISO 9001 business already has, the 38 Annex A controls, the EU AI Act link, and a 26-week plan.",
                cats=["iso", "artificial-intelligence"],
                tags=["ISO/IEC 42001", "ISO 9001", "AI management system", "AI governance", "Annex A", "EU AI Act", "certification"],
                body=body, date="2026-11-13", author="Quak Foo Lee", read="8 min read", cover_label="ISO/IEC 42001",
                related=["iso-9001-and-ai-using-ai-tools-inside-a-quality-system", "integrated-management-system-iso-9001-14001-45001",
                         "iso-9001-2026-what-changed-from-2015"])


if __name__ == "__main__":
    a = article()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", a["slug"], len(a["desc"]))
