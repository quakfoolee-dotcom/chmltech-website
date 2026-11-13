"""V4.76: 2021–2023 merges, all rewritten in our own words (audit plan V8). Each target keeps its address and its
original publish date (content/articles/original_dates.json); the merged posts are retired to it.

1. decoding-the-mysteries-of-api-architecture-a-software-designer-s-guide        APIs for small businesses
     retired into it: how-apis-can-revolutionize-your-marketing-and-sales-efforts, api-integration-tips-and-best-practices,
                      apis-and-artificial-intelligence-enhancing-business-operations
2. harnessing-the-power-of-prompt-engineering-transforming-businesses-with-chatgpt   prompting for business, 2026
     retired into it: mastering-prompt-engineering-for-natural-language-processing,
                      chain-of-thought-prompting-with-chatgpt-best-practices-for-enhancing-ai-interaction
3. what-are-the-core-values-of-process-improvement-part-i                         the ten core values, applied
     retired into it: what-are-the-core-values-of-process-improvement-part-ii
4. the-power-of-data-how-analytics-is-revolutionizing-healthcare                  analytics and patient flow
     retired into it: revolutionizing-healthcare-with-digital-process-improvement
5. understanding-the-power-of-tofu-mofu-and-bofu-in-your-digital-marketing-strategy   the funnel with numbers
     retired into it: from-strangers-to-customers-a-guide-to-understanding-the-different-stages-of-the-marketing-funnel
6. effective-communication-of-goals-and-performance                               scorecards and meeting rhythm
     retired into it: 3-simple-steps-to-solve-your-team-communication-gaps
7. how-to-perform-a-successful-business-process-optimization                      map, measure, redesign
     retired into it: how-to-streamline-business-processes-and-workflows-to-improve-efficiency

Two more posts are retired into existing articles with a short new section (v476_inplace.py).

Usage:  python3 content/articles/v476_articles.py
        python3 content/gen/refresh_article.py <slug>                 (each of the seven)
        python3 content/gen/refresh_article.py --retire <old> <new>   (each retired post)
"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import svg, fig, box, txt, arrow, DEFS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, MUTED, LINE, SAND, PALE, GREENF, ORANGEF

DATE = "2026-11-13"            # the 'Updated' date; the original publish date comes from original_dates.json
API = "decoding-the-mysteries-of-api-architecture-a-software-designer-s-guide"
PRM = "harnessing-the-power-of-prompt-engineering-transforming-businesses-with-chatgpt"
CV = "what-are-the-core-values-of-process-improvement-part-i"
HC = "the-power-of-data-how-analytics-is-revolutionizing-healthcare"
FUN = "understanding-the-power-of-tofu-mofu-and-bofu-in-your-digital-marketing-strategy"
COM = "effective-communication-of-goals-and-performance"
OPT = "how-to-perform-a-successful-business-process-optimization"
RETIRE = {
    API: ["how-apis-can-revolutionize-your-marketing-and-sales-efforts", "api-integration-tips-and-best-practices",
          "apis-and-artificial-intelligence-enhancing-business-operations"],
    PRM: ["mastering-prompt-engineering-for-natural-language-processing",
          "chain-of-thought-prompting-with-chatgpt-best-practices-for-enhancing-ai-interaction"],
    CV: ["what-are-the-core-values-of-process-improvement-part-ii"],
    HC: ["revolutionizing-healthcare-with-digital-process-improvement"],
    FUN: ["from-strangers-to-customers-a-guide-to-understanding-the-different-stages-of-the-marketing-funnel"],
    COM: ["3-simple-steps-to-solve-your-team-communication-gaps"],
    OPT: ["how-to-streamline-business-processes-and-workflows-to-improve-efficiency"],
}
ORIGINAL = {API: "2023-06-25", PRM: "2023-06-11", CV: "2021-09-09", HC: "2023-01-18", FUN: "2023-04-02", COM: "2022-03-20", OPT: "2022-04-09"}


def src(items):
    return "<h2>Sources</h2><ul>" + "".join(
        f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in items) + "</ul>"


def rel(items):
    return "<h2>Related reading</h2><ul>" + "".join(f'<li><a href="../post/{s}.html">{t}</a></li>' for s, t in items) + "</ul>"


def money(x):
    return f"${x:,.0f}"


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table>\n<tr>{h}</tr>\n{b}\n</table>"


def art(slug, title, desc, cats, tags, body, read, label, related):
    return dict(slug=slug, title=title, desc=desc, cats=cats, tags=tags, body=body.strip(), date=DATE, author="Quak Foo Lee",
                read=read, cover_label=label, related=related)


# ═════════════════════════ 1. APIs ═════════════════════════
def fig_api():
    s = DEFS
    s += box(14, 96, 150, 58, ["Your system", "(shop, ERP, CRM)"], fill=NAVY, stroke=NAVY, tc="#fff", fs=13)
    s += box(578, 96, 150, 58, ["Other system", "(carrier, bank, AI)"], fill=NAVY, stroke=NAVY, tc="#fff", fs=13)
    styles = [("REST: ask for data when you need it", BLUE, PALE, 18), ("Webhook: be told when something happens", GREEND, GREENF, 70),
              ("Events or WebSocket: a live stream", PURPLE, "#E7E7F8", 122), ("Batch file: once a day, many records", ORANGE, ORANGEF, 174)]
    for t, c, f, y in styles:
        s += f'<rect x="196" y="{y}" width="350" height="38" rx="8" fill="{f}" stroke="{c}"/>' + txt(371, y + 24, t, "middle", NAVY, 12.8, True)
        s += f'<line x1="166" y1="125" x2="194" y2="{y + 19}" stroke="{c}" stroke-width="1.4"/>'
        s += arrow(548, y + 19, 576, 125, c)
    s += txt(371, 236, "Pick the pattern by how fresh the data must be and how often it changes", "middle", MUTED, 12)
    return svg("Four ways two systems exchange data. REST: one system asks the other for data when it needs it. Webhook: the other "
               "system sends a message when something happens. Events or WebSocket: a live stream of updates. Batch file: once a day, "
               "many records at a time. Pick the pattern by how fresh the data must be and how often it changes.", 742, 246, s, 600)


ORDERS_DAY, MIN_EACH, RATE, DAYS = 40, 4, 35, 250
BUILD, RUN_MO = 8_000, 100
HOURS_YR = ORDERS_DAY * MIN_EACH / 60 * DAYS
SAVE_API = HOURS_YR * RATE
NET_API = SAVE_API - RUN_MO * 12
PAY_API = BUILD / (NET_API / 12)


def api():
    styles = [
        ("REST", "Ask for or send one record at a time over the web, usually as JSON", "Most business software: accounting, e-commerce, CRM, shipping"),
        ("GraphQL", "Ask for exactly the fields you need in one request", "Apps that pull data from several sources into one screen"),
        ("Webhooks", "The other system calls you when something happens", "Order placed, payment received, shipment delivered"),
        ("WebSocket and event streams", "A connection that stays open for live updates", "Live dashboards, chat, machine data"),
        ("gRPC", "Fast, compact calls between services", "Internal systems built by a software team"),
        ("SOAP", "An older, stricter XML standard", "Banks, government and older enterprise systems"),
        ("File transfer (SFTP, EDI)", "Batches of records on a schedule", "Large retailers, distributors, payroll"),
    ]
    checks = [
        ("Authentication", "Use the vendor's recommended method (usually OAuth 2.0 or an API key); keep keys out of spreadsheets and email; one key per integration so you can revoke it."),
        ("Least access", "Give each integration only the data and actions it needs. Broken object-level authorization, where an API lets one user read another's records, tops the OWASP API Security Top 10."),
        ("Errors and retries", "Decide what happens when the other system is down: queue and retry, alert someone, never lose the record silently."),
        ("Duplicates", "Make each call safe to repeat, so a retry does not create a second order or payment."),
        ("Limits", "Check rate limits and plan for peaks such as month-end or a sale."),
        ("Monitoring", "A daily check that counts match on both sides catches problems before customers do."),
        ("Ownership", "Name who owns each integration and keep a one-page record of what it moves, how often, and the credentials it uses."),
    ]
    body = f"""
<p>An API (application programming interface) is the way one piece of software asks another for data or tells it to do something. Every time an online order appears in your accounting system, a shipping label prints from your order screen, or a chatbot looks up an order status, an API is doing the work. This guide replaces four earlier articles on this site about API styles, API integration tips, APIs in marketing and sales, and APIs with AI. It is written for owners and managers who need to make decisions about integrations, not for developers.</p>
<h2>Four ways systems talk to each other</h2>
{fig(fig_api(), 1, "The four common patterns for moving data between two systems.")}
<p>The right pattern depends on how fresh the data needs to be. Stock levels for a web shop need to be close to live; a daily file is fine for payroll hours. Many integrations use two patterns together: a webhook says "a new order arrived", and a REST call then fetches the order details.</p>
<h2>API styles you will hear about</h2>
{table(["Style", "What it does", "Where you meet it"], styles)}
<p>For most small and mid-sized businesses the practical question is not which style to use, since the vendor has already chosen, but whether the two systems you want to connect have a ready-made connector, an integration platform (such as Zapier, Make or Microsoft Power Automate) that supports both, or only a raw API that needs a developer.</p>
<h2>Where APIs pay off</h2>
<ul>
<li><strong>Sales and marketing:</strong> web forms that create leads in the CRM, quote tools that pull prices from the ERP, and email tools that update contacts automatically.</li>
<li><strong>Orders and fulfilment:</strong> e-commerce orders into the ERP, shipping rates and labels from carriers, tracking numbers back to the customer.</li>
<li><strong>Finance:</strong> bank feeds, payment processors and expense apps into accounting.</li>
<li><strong>Operations:</strong> machine and sensor data into a dashboard, maintenance requests into a work order system.</li>
<li><strong>AI tools:</strong> an AI assistant or agent is only as useful as the systems it can reach, and it reaches them through APIs. The Model Context Protocol (MCP) has become a common way to give AI tools controlled access to business systems; our paper on <a href="../post/agent-interoperability-standards-mcp-a2a-erp-crm-plant-systems.html">agent interoperability standards</a> explains how it works.</li>
</ul>
<h2>Worked example: is an order integration worth it?</h2>
<p>A distributor keys {ORDERS_DAY} web orders a day into its ERP by hand, at about {MIN_EACH} minutes each, with occasional typing errors. That is {HOURS_YR:,.0f} hours a year; at {money(RATE)} an hour including benefits, about {money(SAVE_API)}. A connector or integration platform costs {money(BUILD)} to set up and test and {money(RUN_MO)} a month to run. The net saving is about {money(NET_API)} a year, so the set-up cost pays back in about {PAY_API:.0f} months, before counting fewer errors and faster shipping. The figures are illustrative; replace them with your own volumes.</p>
<h2>An integration checklist</h2>
{table(["Check", "What to do"], checks)}
""" + src([
        ("OWASP API Security Top 10 (2023)", "https://owasp.org/API-Security/editions/2023/en/0x11-t10/"),
        ("Model Context Protocol: introduction", "https://modelcontextprotocol.io/introduction"),
    ]) + rel([
        ("agent-interoperability-standards-mcp-a2a-erp-crm-plant-systems", "Agent interoperability: MCP, A2A and connecting to ERP, CRM and plant systems"),
        ("agent-security-and-identity-prompt-injection-least-privilege-credentials-audit", "Agent security and identity: prompt injection, least privilege and credentials"),
        ("the-ultimate-guide-to-choosing-the-right-erp-for-your-business", "Choosing and implementing an ERP"),
    ])
    return art(API, "APIs for Small Businesses: How Systems Connect, Where It Pays and What to Check",
               "What an API is, the four ways systems exchange data, the API styles you will meet, a worked payback example and an integration checklist.",
               ["digital-technology", "artificial-intelligence"], ["API", "integration", "REST", "webhooks", "MCP", "API security", "automation"],
               body, "6 min read", "APIs",
               ["agent-interoperability-standards-mcp-a2a-erp-crm-plant-systems", "agent-security-and-identity-prompt-injection-least-privilege-credentials-audit",
                "the-ultimate-guide-to-choosing-the-right-erp-for-your-business"])


# ═════════════════════════ 2. Prompting ═════════════════════════
def fig_prompt():
    s = DEFS
    parts = [("Task", "What you want done, in one sentence", BLUE, PALE), ("Context", "Who it is for, background, the source material", GREEND, GREENF),
             ("Constraints", "Length, tone, what to avoid, what to do if unsure", PURPLE, "#E7E7F8"), ("Output", "Format, headings, a table or template", ORANGE, ORANGEF),
             ("Examples", "One good example, if format matters", MUTED, "#EFEFEF")]
    for i, (h, d, c, f) in enumerate(parts):
        y = 14 + i * 44
        s += f'<rect x="14" y="{y}" width="150" height="36" rx="8" fill="{c}"/>' + txt(89, y + 23, h, "middle", "#fff", 13.5, True)
        s += f'<rect x="172" y="{y}" width="556" height="36" rx="8" fill="{f}" stroke="{c}"/>' + txt(186, y + 23, d, "start", NAVY, 12.8)
    return svg("The five parts of a business prompt. Task: what you want done, in one sentence. Context: who it is for, background, "
               "and the source material. Constraints: length, tone, what to avoid and what to do if unsure. Output: the format, headings, "
               "a table or template. Examples: one good example, if the format matters.", 742, 236, s, 600)


def prm():
    before = "Write a summary of this customer complaint."
    after = ("You are helping our customer service lead. Summarize the complaint below for the weekly quality meeting.<br>"
             "Context: we make stainless steel tanks; the reader knows our products but not this customer.<br>"
             "Constraints: under 120 words; facts only, no apology wording; if the order number or date is missing, say so.<br>"
             "Output: three headings: What happened, What the customer wants, Open questions.<br>"
             "&lt;complaint&gt; …pasted email… &lt;/complaint&gt;")
    body = f"""
<p>A prompt is the instruction you give an AI model. This guide replaces three earlier articles on this site about prompt engineering, chain-of-thought prompting and prompting ChatGPT for business. Much of the 2023 advice has aged: today's models follow plain instructions far better, several now reason through a problem before answering, and some old tricks now make results worse. What still matters is being clear about the task, giving the model the right material, and checking the output.</p>
<h2>The five parts of a good business prompt</h2>
{fig(fig_prompt(), 1, "Most business prompts need the first four parts; add an example only when the format matters.")}
<h2>Before and after</h2>
{table(["Version", "Prompt"], [("Before", before), ("After", after)])}
<p>The second prompt takes a minute longer to write and saves several rounds of editing. Putting the pasted material between simple tags, like the &lt;complaint&gt; markers above, helps the model separate your instructions from the text it is working on. Both OpenAI and Anthropic recommend this kind of structure for longer prompts.</p>
<h2>What changed since 2023</h2>
<ul>
<li><strong>"Think step by step" is often unnecessary.</strong> Chain-of-thought prompting, asking a model to reason in steps before answering, was a major finding in 2022 and helped older models with arithmetic and logic. Reasoning models now do this on their own before they answer. OpenAI's guidance for its reasoning models is to keep prompts simple and direct and to avoid telling them to think step by step, which can hurt rather than help. With a standard chat model, asking for the reasoning can still help on multi-step problems.</li>
<li><strong>Role-play matters less than context.</strong> "You are a world-class marketer" adds little. Saying who the reader is and what they already know adds a lot.</li>
<li><strong>Settings like temperature are rarely needed in chat.</strong> They matter when you build prompts into software; in a chat window, wording does the work.</li>
<li><strong>Long documents are fine.</strong> Current models can read long reports and contracts in one go. Put the document first and the question last.</li>
</ul>
<h2>Habits that make prompts reliable</h2>
<ol>
<li><strong>Write the prompt once, then save it.</strong> A team library of tested prompts for recurring jobs (quote summaries, meeting notes, supplier emails) is worth more than clever one-off wording.</li>
<li><strong>Tell the model what to do when it is unsure.</strong> "If the information is not in the document, say so" reduces made-up answers.</li>
<li><strong>Ask for a format you can check.</strong> Tables, fixed headings and quoted sources are easier to verify than flowing prose.</li>
<li><strong>Test on real cases.</strong> Try a new prompt on five real examples, including a difficult one, before the team relies on it.</li>
<li><strong>Keep sensitive data in approved tools.</strong> Customer and employee information should only go into tools your business has approved for it.</li>
</ol>
<h2>When a better prompt is not the answer</h2>
<p>If a task needs your company's own data, a sequence of steps across systems, or the same output hundreds of times, the answer is usually a workflow or an agent connected to your systems rather than a longer prompt. <a href="../post/ai-agents-101-and-how-to-use-them-to-improve-efficiency.html">AI agents for small businesses</a> explains where that line sits.</p>
""" + src([
        ("Anthropic: Prompt engineering overview", "https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview"),
        ("OpenAI: Reasoning best practices", "https://platform.openai.com/docs/guides/reasoning-best-practices"),
        ("Wei et al. (2022): Chain-of-thought prompting elicits reasoning in large language models", "https://arxiv.org/abs/2201.11903"),
    ]) + rel([
        ("ai-agents-101-and-how-to-use-them-to-improve-efficiency", "AI agents for small businesses"),
        ("private-ai-assistant-on-your-own-pc-anythingllm-and-ollama", "A private AI assistant on your own PC"),
        ("ai-readiness-preparing-your-organization-for-successful-ai-adoption", "AI readiness: preparing your organization"),
    ])
    return art(PRM, "Prompting AI Models for Business Work: What Still Works in 2026",
               "The five parts of a good business prompt, a before-and-after example, what changed with reasoning models, and habits that make prompts reliable.",
               ["artificial-intelligence"], ["prompt engineering", "ChatGPT", "Claude", "chain of thought", "reasoning models", "AI at work"],
               body, "5 min read", "Prompting",
               ["ai-agents-101-and-how-to-use-them-to-improve-efficiency", "private-ai-assistant-on-your-own-pc-anythingllm-and-ollama",
                "ai-readiness-preparing-your-organization-for-successful-ai-adoption"])


# ═════════════════════════ 3. Core values ═════════════════════════
VALUES = [
    ("Agility", "Improve in small steps and adjust as you learn", "Changes are trialled for weeks, not planned for a year"),
    ("Quality", "Build quality into the process, people and technology from the start", "Defects are traced to a step, not blamed on a person"),
    ("Leadership", "Leaders set a clear direction and stay open to ideas", "The owner or manager attends the improvement review"),
    ("Communication", "Involve the people affected in decisions", "Front-line staff help map the process before it is changed"),
    ("Respect", "Keep working relationships safe and cooperative", "People raise problems without fear of blame"),
    ("Discipline", "Run processes the same way every time and follow through", "Agreed changes become the written standard"),
    ("Whole-business view", "Decide what is best for the company, not one department", "A fix in sales is checked for its effect on operations"),
    ("Service", "Improvement work serves customers and colleagues", "Each project names the customer it helps"),
    ("Continuous learning", "Train people in improvement methods and share lessons", "Each project ends with a short lessons-learned note"),
    ("Human-centred design", "Design processes around the people who use them", "New forms and screens are tested with real users"),
]


def cv():
    rows = [(f"<strong>{v}</strong>", m, e) for v, m, e in VALUES]
    body = f"""
<p>Process improvement methods such as Lean, Six Sigma and business process management give you tools. Core values decide whether the tools stick. A team that maps a process brilliantly but blames people for errors, or fixes one department at another's expense, will be back where it started within a year. This article replaces a two-part series first published on this site in 2021.</p>
<p>The ten values below follow the "process improvement manifesto" set out by Tristan Boutros and Tim Purdie in <cite>The Process Improvement Handbook</cite> (McGraw-Hill, 2014). The wording and the examples here are ours; read the book for the authors' full treatment.</p>
<h2>The ten values and what they look like in practice</h2>
{table(["Value", "What it means", "What you see when it is working"], rows)}
<h2>Why values matter more in a small business</h2>
<p>In a large company, a process office and formal governance can keep improvement going even when the culture is uneven. A business with 20 or 80 people has no such structure: the habits of the owner and two or three managers are the system. That makes the values above less a poster and more a description of how the leadership team behaves when a problem is found.</p>
<h2>A ten-minute self-check</h2>
<p>Score each value from 1 (rarely true) to 5 (consistently true) for the last improvement your business made. Then look at the two lowest scores.</p>
<ul>
<li><strong>Low on respect or communication:</strong> start meetings about problems with the process, not the person, and invite the people who do the work.</li>
<li><strong>Low on discipline:</strong> finish one change properly, with the new standard written down, before starting the next. <a href="../post/essentials-of-effective-process-documentation.html">Process documentation that people use</a> shows how.</li>
<li><strong>Low on whole-business view:</strong> map the process across departments, not inside one. A swim lane map makes the hand-offs visible.</li>
<li><strong>Low on learning:</strong> after each change, hold a 15-minute review: what worked, what did not, what we will do differently.</li>
</ul>
<h2>Putting the values into a project</h2>
<p>A practical way to use them is as a short charter checklist at the start of each improvement project: who is the customer (service), who from each affected team is involved (communication, whole-business view), how the change will be trialled (agility), how it will become the standard (discipline), and what the team will learn (learning). The two-part series on <a href="../post/implement-process-improvements-part-1.html">how to implement process improvements</a> walks through a full project.</p>
""" + src([
        ("Boutros, T. and Purdie, T. (2014). The Process Improvement Handbook: A Blueprint for Managing Change and Increasing Organizational Performance. McGraw-Hill", "https://www.qualitymag.com/products/680-the-process-improvement-handbook-a-blueprint-for-managing-change-and-increasing-organizational-performance"),
    ]) + rel([
        ("implement-process-improvements-part-1", "How to implement process improvements, Part 1"),
        ("how-to-perform-a-successful-business-process-optimization", "Business process optimization: map, measure, redesign"),
        ("essentials-of-effective-process-documentation", "Process documentation that people use"),
    ])
    return art(CV, "The Core Values of Process Improvement: Ten Principles and How to Apply Them",
               "Ten core values that make process improvement stick, what each looks like in practice, a ten-minute self-check, and how to use them in a project.",
               ["process-improvement"], ["process improvement", "continuous improvement", "core values", "culture", "Lean", "operational excellence"],
               body, "4 min read", "Process", ["implement-process-improvements-part-1", "how-to-perform-a-successful-business-process-optimization",
                                               "essentials-of-effective-process-documentation"])


# ═════════════════════════ 4. Healthcare ═════════════════════════
def fig_flow():
    s = DEFS
    steps = [["Arrive and", "triage"], ["Assessment", "and tests"], ["Decide: admit", "or discharge"], ["Wait for an", "inpatient bed"],
             ["Inpatient", "stay"], ["Discharge home,", "to home care", "or LTC"]]
    xs = [10, 132, 254, 376, 498, 620]
    for i, (x, l) in enumerate(zip(xs, steps)):
        hot = i in (3, 5)
        s += box(x, 40, 106, 64, l, fill=ORANGEF if hot else PALE, stroke=ORANGE if hot else "#9AB0C8", fs=12)
        if i < 5: s += arrow(x + 107, 72, x + 130, 72)
    s += f'<path d="M673,106 C673,170 429,170 429,108" fill="none" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#ah)"/>'
    s += txt(554, 178, "No long-term care or home care place: the bed stays full,", "middle", ORANGE, 12, True)
    s += txt(554, 194, "so the next patient waits in emergency", "middle", ORANGE, 12, True)
    s += txt(10, 24, "Patient flow through a hospital", "start", MUTED, 12)
    return svg("Patient flow through a hospital: arrive and triage, assessment and tests, decision to admit or discharge, wait for an "
               "inpatient bed, inpatient stay, and discharge to home, home care or long-term care. The wait for a bed and the discharge "
               "step are highlighted: when there is no long-term care or home care place, the bed stays full, so the next patient waits "
               "in emergency.", 742, 206, s, 600)


CLINIC_APPTS, NOSHOW_A, NOSHOW_B, VISIT_VALUE, CLINIC_DAYS = 60, 0.10, 0.07, 90, 240
RECOVERED = CLINIC_APPTS * (NOSHOW_A - NOSHOW_B) * CLINIC_DAYS


def hc():
    uses = [
        ("Patient flow", "Arrivals by hour, time to bed, discharge times, bed occupancy", "Match staffing to demand; plan discharges earlier in the day"),
        ("Scheduling", "No-shows, cancellations, appointment length by type", "Reminders, overbooking rules, right-sized slots"),
        ("Quality and safety", "Readmissions, infections, falls, medication errors", "Find the steps where harm starts"),
        ("Supplies and pharmacy", "Usage by unit, expiry, stock-outs", "Par levels and reorder points instead of guesswork"),
        ("Revenue and billing", "Claim rejections, days to payment", "Fix the intake step that causes most rejections"),
    ]
    body = f"""
<p>Health care produces large amounts of data, but the improvements that matter most usually come from using it to see how patients, staff and supplies move through a process. This article replaces two short 2023 articles on this site, one on healthcare analytics and one on digital process improvement in healthcare, and adds current Canadian data and a worked example.</p>
<h2>The problem is often flow, not effort</h2>
<p>The Canadian Institute for Health Information (CIHI) reported in June 2026 that emergency departments had about 16.1 million visits in 2024–25, and that one in 10 patients admitted through emergency, around 180,000 people, waited more than 48 hours for an inpatient bed. CIHI's analysts stressed that the causes lie largely outside the emergency department: limited access to primary care, and shortages of long-term care and home care places that keep hospital beds occupied by patients ready to leave.</p>
{fig(fig_flow(), 1, "A delay at the end of the process shows up as a wait at the front.")}
<p>That is a classic process problem. A queue forms in front of the step with the least capacity, not where the staff are working hardest. Data helps by showing where the queue really starts: time stamps from arrival to triage, decision to admit, bed request, bed assigned and discharge make the bottleneck visible.</p>
<h2>Five places analytics helps</h2>
{table(["Area", "What to measure", "What it lets you change"], uses)}
<h2>Worked example: no-shows in a clinic</h2>
<p>A physiotherapy clinic books {CLINIC_APPTS} appointments a day and loses {NOSHOW_A:.0%} to no-shows. Its booking data shows most no-shows are first appointments booked more than two weeks ahead. The clinic adds a text reminder two days before and a waitlist for short-notice openings. If no-shows fall to {NOSHOW_B:.0%}, it recovers about {RECOVERED:,.0f} appointments a year over {CLINIC_DAYS} working days, worth about {money(RECOVERED * VISIT_VALUE)} at {money(VISIT_VALUE)} a visit. The figures are illustrative; the method is to find the pattern in the data first, then change the step that causes it.</p>
<h2>Making it work in a clinic or care organization</h2>
<ol>
<li><strong>Start with one flow and one measure,</strong> such as time from referral to first appointment.</li>
<li><strong>Use the data you already record.</strong> Scheduling and electronic medical record systems hold time stamps that are rarely analysed.</li>
<li><strong>Map the process with the staff who run it,</strong> including the hand-offs to other organizations.</li>
<li><strong>Protect privacy.</strong> Use de-identified or aggregated data for analysis, and follow your province's health privacy law and your custodian's policies.</li>
<li><strong>Review weekly,</strong> so the data drives small changes rather than an annual report.</li>
</ol>
<p>Our <a href="../health-care.html">health care</a> page describes how we support clinics and care organizations with process mapping and improvement.</p>
""" + src([
        ("Global News: One in 10 patients admitted through emergency waited more than 48 hours for a bed (CIHI, June 2026)", "https://globalnews.ca/news/11938222/emergency-room-wait-times-cihi-report/"),
        ("CP24: What a new CIHI report reveals about the causes of emergency wait times (June 2026)", "https://www.cp24.com/news/canada/2026/06/25/what-a-new-report-reveals-about-the-true-cause-of-canadas-massive-emergency-wait-times/"),
    ]) + rel([
        ("how-to-perform-a-successful-business-process-optimization", "Business process optimization: map, measure, redesign"),
        ("things-you-need-to-know-about-the-theory-of-constraints-toc", "The theory of constraints"),
        ("boost-performance-with-effective-dashboard-strategies-for-entrepreneurs", "Dashboard strategies"),
    ])
    return art(HC, "Healthcare Analytics and Patient Flow: Using Data to Improve Care Processes",
               "How data shows where patient flow breaks down, five places analytics helps clinics and hospitals, Canadian 2026 data, and a no-show example.",
               ["digital-technology"], ["healthcare", "data analytics", "patient flow", "process improvement", "CIHI", "clinic scheduling"],
               body, "5 min read", "Healthcare", ["how-to-perform-a-successful-business-process-optimization",
                                                  "things-you-need-to-know-about-the-theory-of-constraints-toc",
                                                  "boost-performance-with-effective-dashboard-strategies-for-entrepreneurs"])


# ═════════════════════════ 5. Funnel ═════════════════════════
FUNNEL = [("Website visits", 6000), ("Enquiries and downloads", 180), ("Qualified leads", 54), ("Proposals", 18), ("Won", 6)]


def fig_funnel():
    s = DEFS
    bands = [("TOFU", "Awareness", BLUE, 0, 1), ("MOFU", "Consideration", GREEND, 1, 3), ("BOFU", "Decision", ORANGE, 3, 5)]
    W = 420
    for i, (name, n) in enumerate(FUNNEL):
        w = W - i * 70; x = 230 + (W - w) / 2; y = 14 + i * 44
        c = BLUE if i == 0 else GREEND if i < 3 else ORANGE
        s += f'<rect x="{x}" y="{y}" width="{w}" height="36" rx="6" fill="{c}" opacity=".9"/>'
        s += txt(440, y + 23, f"{name}: {n:,}", "middle", "#fff", 13, True)
        if i: s += txt(700, y + 4, f"{n / FUNNEL[i - 1][1]:.0%}", "start", MUTED, 12, True)
    for tag, stage, c, a, b in bands:
        y0 = 14 + a * 44; y1 = 14 + b * 44 - 8
        s += f'<line x1="200" y1="{y0}" x2="200" y2="{y1}" stroke="{c}" stroke-width="4"/>'
        s += txt(190, (y0 + y1) / 2 + 2, tag, "end", c, 14, True) + txt(190, (y0 + y1) / 2 + 18, stage, "end", MUTED, 11.5)
    s += txt(700, 236, "step conversion", "start", MUTED, 11)
    return svg("A B2B marketing funnel with illustrative numbers. Top of funnel, awareness: 6,000 website visits. Middle of funnel, "
               "consideration: 180 enquiries and downloads (3% of visits) and 54 qualified leads (30%). Bottom of funnel, decision: 18 "
               "proposals (33%) and 6 won (33%).", 790, 246, s, 600)


def fun():
    stages = [
        ("TOFU: awareness", "People who have a problem but do not know you", "Useful articles, guides, short videos, search and social posts", "Visits from search, new visitors, time on page"),
        ("MOFU: consideration", "People comparing ways to solve it", "Checklists, templates, case studies, webinars, comparison pages", "Enquiries, downloads, newsletter sign-ups, qualified leads"),
        ("BOFU: decision", "People choosing a supplier", "Pricing guidance, proposals, references, demos, a fast reply", "Proposals sent, win rate, time to close"),
    ]
    rates = [FUNNEL[i][1] / FUNNEL[i - 1][1] for i in range(1, len(FUNNEL))]
    new_q = round(FUNNEL[1][1] * 0.40); new_won = round(new_q * rates[2] * rates[3])
    body = f"""
<p>A marketing funnel describes how people move from first hearing about you to becoming a customer. TOFU, MOFU and BOFU are shorthand for the top, middle and bottom of the funnel. This article replaces two earlier ones on this site about funnel stages and adds a worked example, because the funnel is most useful when you put numbers on it.</p>
<h2>The three stages</h2>
{table(["Stage", "Who is there", "What helps them", "What to measure"], stages)}
<p>The funnel is a simplification. Real buyers loop back, skip stages, and talk to colleagues you never see. In business-to-business sales several people usually take part in a decision, and a buyer may read your articles for months before getting in touch. The funnel is still useful because it makes you ask, at each stage, what the buyer needs next and whether you are offering it.</p>
<h2>Worked example: where is the funnel leaking?</h2>
<p>An engineering services firm tracks a year of numbers. They are illustrative.</p>
{fig(fig_funnel(), 1, "A year of funnel numbers for an engineering services firm, with the conversion at each step.")}
<p>Visits convert to enquiries at {rates[0]:.0%}, which is reasonable for a technical site. The weak step is the middle: only {rates[1]:.0%} of enquiries become qualified leads, because many enquiries are students, job seekers or out-of-scope requests, and real prospects wait days for a reply. Two changes target that step: a short qualifying question on the enquiry form, and a reply within one working day with a relevant case study. If qualified leads rise to 40% of enquiries, the same traffic gives about {new_q} qualified leads and, at the same later conversion rates, about {new_won} wins instead of {FUNNEL[-1][1]}. More traffic would have been the expensive way to get the same result.</p>
<h2>Making the funnel work</h2>
<ol>
<li><strong>Put one number on each stage</strong> and review them monthly. <a href="../post/how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide.html">Google Analytics 4</a> covers the top; your CRM covers the rest.</li>
<li><strong>Fix the weakest step first.</strong> Doubling traffic into a leaking middle doubles the leak.</li>
<li><strong>Give each piece of content a next step.</strong> An article should point to a related checklist; a checklist should point to a conversation.</li>
<li><strong>Agree what a qualified lead is</strong> between whoever does marketing and whoever sells, so both count the same thing.</li>
<li><strong>Speed matters at the bottom.</strong> A fast, specific reply often decides a deal more than the price does.</li>
</ol>
""" + rel([
        ("how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide", "How to measure your website with Google Analytics 4"),
        ("from-creation-to-conversion-measuring-the-success-of-your-content-marketing-strategy", "Measuring the success of your content"),
        ("6-essential-steps-to-streamline-and-enhance-your-sales-process", "Six steps to streamline your sales process"),
    ])
    return art(FUN, "TOFU, MOFU and BOFU: Using the Marketing Funnel with Real Numbers",
               "The three stages of the marketing funnel, what buyers need at each, and a worked B2B example showing how to find and fix the weakest step.",
               ["marketing"], ["marketing funnel", "TOFU", "MOFU", "BOFU", "lead generation", "B2B marketing", "conversion rate"],
               body, "4 min read", "Marketing", ["how-to-measure-your-website-s-performance-using-google-analytics-a-comprehensive-guide",
                                                 "from-creation-to-conversion-measuring-the-success-of-your-content-marketing-strategy",
                                                 "6-essential-steps-to-streamline-and-enhance-your-sales-process"])


# ═════════════════════════ 6. Communicating goals ═════════════════════════
def fig_rhythm():
    s = DEFS
    rows = [("Yearly", "Goals for the year: 3 to 5, each with an owner", BLUE, PALE), ("Quarterly", "Priorities for 90 days that move the yearly goals", GREEND, GREENF),
            ("Weekly", "Scorecard review and issues list: 60 to 90 minutes", PURPLE, "#E7E7F8"), ("Daily", "10-minute huddle: today's plan and blockers", ORANGE, ORANGEF)]
    for i, (h, d, c, f) in enumerate(rows):
        y = 14 + i * 46
        s += f'<rect x="14" y="{y}" width="130" height="38" rx="8" fill="{c}"/>' + txt(79, y + 24, h, "middle", "#fff", 13.5, True)
        s += f'<rect x="152" y="{y}" width="576" height="38" rx="8" fill="{f}" stroke="{c}"/>' + txt(166, y + 24, d, "start", NAVY, 12.8)
    return svg("A communication rhythm. Yearly: 3 to 5 goals, each with an owner. Quarterly: priorities for 90 days that move the yearly "
               "goals. Weekly: a 60 to 90 minute review of the scorecard and the issues list. Daily: a 10-minute huddle on today's plan "
               "and blockers.", 742, 200, s, 600)


SCORE = [("New quotes sent", "Sales lead", 12, 14, True), ("Quote win rate (4-week rolling)", "Sales lead", "30%", "27%", False),
         ("Orders shipped on time", "Operations", "95%", "96%", True), ("Jobs needing rework", "Operations", "≤ 2", "3", False),
         ("Cash collected ($ thousands)", "Office manager", 85, 91, True), ("Customer issues open more than 5 days", "Office manager", 0, 1, False)]


def com():
    from v479_articles import COM_SECTION   # V4.79: absorbs the alignment and OPS posts
    rows = [(m, o, str(t), str(a), "On track" if ok else "<strong>Off track</strong>") for m, o, t, a, ok in SCORE]
    body = f"""
<p>Most communication problems in a growing business are not about people talking too little. They come from too many things being tracked in too many places, so nobody is sure what matters this week or whether the team is on track. This article replaces two earlier ones on this site, on communicating goals and performance and on closing team communication gaps, with one practical approach: a short list of goals, a weekly scorecard, and a regular meeting rhythm.</p>
<h2>Step 1: agree a few goals, each with one owner</h2>
<p>Three to five goals for the year are enough. Each needs a number, a date and one named owner. Ten goals with shared ownership produce activity but little progress. Break each yearly goal into a few 90-day priorities, because a quarter is long enough to finish something and short enough to stay focused.</p>
<h2>Step 2: a weekly scorecard</h2>
<p>A scorecard is a one-page table of five to fifteen numbers that tell you, each week, whether the business is on track. Each number has an owner and a target. The example below is for a small fabrication shop; the figures are illustrative.</p>
{table(["Measure", "Owner", "Weekly target", "This week", "Status"], rows)}
<p>The value of the scorecard is in what happens next: the two off-track numbers go on the issues list for the weekly meeting. Nobody needs to defend the others. <a href="../post/50-must-track-kpis-for-business-success-from-finance-to-product-development.html">50 KPIs with formulas</a> has ideas for which measures to choose.</p>
<h2>Step 3: a meeting rhythm people can rely on</h2>
{fig(fig_rhythm(), 1, "Four meeting levels, each with a fixed purpose and length.")}
<p>The weekly meeting does most of the work. Keep the same day, time and agenda every week: a quick check of the scorecard and quarterly priorities, updates on customer and staff issues, then most of the time spent solving the issues on the list, one at a time. Each solved issue ends with an action, an owner and a date. This structure follows the Entrepreneurial Operating System (EOS), which we describe on our <a href="../eos.html">EOS page</a>, but the same idea works with OKRs or any simple framework.</p>
<h2>Step 4: make results visible</h2>
<ul>
<li>Share the scorecard with everyone it affects, not only managers. People work better when they can see the score.</li>
<li>Show trends, not just this week's figure, so one bad week does not cause panic.</li>
<li>Keep one source of truth: one scorecard, one issues list, one place for priorities.</li>
<li>Celebrate finished priorities at the end of each quarter.</li>
</ul>
{COM_SECTION}<h2>Common mistakes</h2>
<ul>
<li>Measures nobody controls, or that change only monthly.</li>
<li>Meetings that report status but never solve anything.</li>
<li>Skipping the meeting in busy weeks, which are the weeks it matters most.</li>
</ul>
""" + rel([
        ("50-must-track-kpis-for-business-success-from-finance-to-product-development", "50 KPIs for business success, with formulas"),
        ("boost-performance-with-effective-dashboard-strategies-for-entrepreneurs", "Dashboard strategies for entrepreneurs"),
        ("how-to-increase-operational-efficiency-for-small-business", "Operational efficiency for small businesses"),
    ])
    return art(COM, "Communicating Goals and Performance: Scorecards and a Meeting Rhythm That Work",
               "How a growing team stays aligned: a few goals with owners, a weekly scorecard with a worked example, a meeting rhythm, and common mistakes.",
               ["operational-efficiency"], ["team communication", "goals", "scorecard", "KPIs", "meeting rhythm", "EOS", "accountability"],
               body, "5 min read", "Teams", ["50-must-track-kpis-for-business-success-from-finance-to-product-development",
                                             "boost-performance-with-effective-dashboard-strategies-for-entrepreneurs",
                                             "how-to-increase-operational-efficiency-for-small-business"])


# ═════════════════════════ 7. Process optimization ═════════════════════════
BEFORE = [("Order arrives by email", 0.5, False), ("Re-keyed into a spreadsheet", 6, False), ("Credit check by owner", 240, False),
          ("Entered into accounting", 5, False), ("Printed and walked to warehouse", 120, False), ("Pick and pack", 25, True), ("Ship and invoice", 10, True)]
AFTER = [("Order arrives through web form", 0.5, False), ("Auto-created in accounting", 0, False), ("Credit rule: owner sees exceptions only", 15, False),
         ("Pick list on warehouse screen", 5, False), ("Pick and pack", 25, True), ("Ship and invoice", 10, True)]
T_B, T_A = sum(m for _, m, _ in BEFORE), sum(m for _, m, _ in AFTER)
VA = sum(m for _, m, v in BEFORE if v)


def fig_opt():
    s = DEFS
    X = lambda m: 150 + m * 1.35
    for lab, steps, y in (("Before", BEFORE, 30), ("After", AFTER, 104)):
        s += txt(14, y + 24, lab, "start", NAVY, 14, True)
        x = X(0)
        for name, m, va in steps:
            w = max(m * 1.35, 1.5)
            s += f'<rect x="{x}" y="{y}" width="{w}" height="38" fill="{GREEND if va else ORANGE}" opacity="{1 if va else .75}" stroke="#fff"/>'
            x += w
        tot = sum(m for _, m, _ in steps)
        s += txt(x + 8, y + 24, f"{tot / 60:.1f} h", "start", NAVY, 13, True)
    s += f'<rect x="150" y="162" width="14" height="14" fill="{ORANGE}" opacity=".75"/>' + txt(170, 174, "Waiting, re-keying, walking (no value to the customer)", "start", MUTED, 12)
    s += f'<rect x="150" y="184" width="14" height="14" fill="{GREEND}"/>' + txt(170, 196, "Work the customer pays for", "start", MUTED, 12)
    return svg(f"Elapsed time to process one order, before and after. Before: {T_B / 60:.1f} hours, of which only {VA} minutes of pick, "
               f"pack, ship and invoice add value; the rest is re-keying, waiting for a credit check and walking paper to the warehouse. "
               f"After: {T_A / 60:.1f} hours, with the same {VA} minutes of value-adding work.", 742, 210, s, 600)


def opt():
    steps = [(n, f"{m:g} min", "Yes" if v else "No") for n, m, v in BEFORE]
    body = f"""
<p>Business process optimization means changing how work flows so that it takes less time, costs less and goes wrong less often, from the customer's point of view. This article replaces two earlier ones on this site, on process optimization and on streamlining workflows, with a single method and a worked example.</p>
<h2>The method in five steps</h2>
<ol>
<li><strong>Pick one process and define its start and end,</strong> for example "order received" to "order shipped". Choose a process that customers notice or that costs real time.</li>
<li><strong>Map it as it really runs,</strong> with the people who do the work, step by step. A swim lane map shows each role and every hand-off; see <a href="../post/essentials-of-effective-process-documentation.html">process documentation that people use</a> for an example.</li>
<li><strong>Measure it.</strong> For each step, record the working time and the waiting time. Add two or three measures for the whole process: elapsed time, error rate and cost per transaction.</li>
<li><strong>Redesign.</strong> For each step, ask: can we remove it, combine it with another, automate it, or move it so work flows without waiting? Remove before you automate; automating a needless step only makes it faster.</li>
<li><strong>Trial, standardize and review.</strong> Run the new process for a few weeks, write it down as the new standard, and check the measures monthly.</li>
</ol>
<h2>Running the mapping workshop</h2>
<ul>
<li>Invite one person from each role in the process and keep the group under eight.</li>
<li>Use sticky notes on a wall or a shared whiteboard; it is faster than drawing software and everyone can move things.</li>
<li>Walk one real, recent transaction from start to end, then ask what happens when things go wrong.</li>
<li>Note waits, re-keying, approvals and rework as you go; these are where the time hides.</li>
<li>Keep the discussion on the process, not on who made which mistake.</li>
</ul>
<h2>Worked example: order handling at a small distributor</h2>
<p>The team mapped one typical order and timed each step. The times are illustrative.</p>
{table(["Step", "Elapsed time", "Adds value for the customer?"], steps)}
<p>The order took {T_B / 60:.1f} hours from arrival to shipping, but only {VA} minutes of that was work the customer would pay for. The rest was re-keying, waiting for the owner to approve credit, and walking paper to the warehouse. The redesign removed the spreadsheet, connected the web form to accounting, replaced the owner's approval of every order with a credit rule so the owner only sees exceptions, and put the pick list on a warehouse screen.</p>
{fig(fig_opt(), 1, "Elapsed time for one order before and after the redesign. The value-adding work is unchanged.")}
<p>Elapsed time fell from {T_B / 60:.1f} hours to {T_A / 60:.1f} hours, so same-day shipping became normal, and two error-prone typing steps disappeared. Nothing about picking or packing changed. Our <a href="../post/how-to-increase-operational-efficiency-for-small-business.html">operational efficiency guide</a> shows how to put a dollar value on gains like this.</p>
<h2>Common mistakes</h2>
<ul>
<li>Buying software before mapping the process.</li>
<li>Mapping the process as it should run instead of as it runs.</li>
<li>Optimizing one department and moving the problem to the next.</li>
<li>Not writing down the new process, so it drifts back.</li>
</ul>
<p>Our <a href="../process-mapping.html">process mapping</a> and <a href="../business-process-optimization.html">business process optimization</a> services follow this method.</p>
""" + rel([
        ("essentials-of-effective-process-documentation", "Process documentation that people use"),
        ("how-to-increase-operational-efficiency-for-small-business", "Operational efficiency for small businesses"),
        ("how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations", "How to use Lean to eliminate waste"),
    ])
    return art(OPT, "Business Process Optimization: Map, Measure and Redesign a Process",
               "A five-step method for optimizing a business process, how to run a mapping workshop, and a worked order-handling example with before and after times.",
               ["process-improvement", "operational-efficiency"], ["process optimization", "process mapping", "workflow", "value-added", "automation", "lead time"],
               body, "5 min read", "Process", ["essentials-of-effective-process-documentation", "how-to-increase-operational-efficiency-for-small-business",
                                                "how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations"])


ALL = (api, prm, cv, hc, fun, com, opt)

if __name__ == "__main__":
    # keep the original publish dates on record for add_article.apply_dates
    op = os.path.join(HERE, "original_dates.json")
    od = json.load(open(op, encoding="utf-8")); od.update(ORIGINAL)
    note = od.pop("_note"); json.dump({"_note": note, **dict(sorted(od.items()))}, open(op, "w", encoding="utf-8"), indent=1)
    for f in ALL:
        a = f()
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(a["slug"][:50], len(re.sub(r"<svg.*?</svg>|<[^>]+>", " ", a["body"], flags=re.S).split()), "words")
    print(f"API: {HOURS_YR:.0f} h/yr, save {SAVE_API:,.0f}, net {NET_API:,.0f}, payback {PAY_API:.1f} mo")
    print(f"HC: recovered {RECOVERED:.0f} appts, {RECOVERED * VISIT_VALUE:,.0f}")
    print(f"OPT: before {T_B} min ({T_B / 60:.2f} h), after {T_A} min ({T_A / 60:.2f} h), VA {VA}")
