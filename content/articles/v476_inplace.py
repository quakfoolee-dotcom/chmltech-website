"""V4.76: two 2021–2023 posts retired into existing articles, each of which gains a short new section in our own words.

1. identifying-non-value-added  ->  how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations
     new section: "Value-added or not: a three-question test", after "Identifying Waste in Processes"
2. revolutionizing-business-operations-how-ai-is-streamlining-efficiency-and-boosting-performance
     ->  5-proven-steps-to-integrate-ai-into-your-operations-workflow-for-smarter-faster-results
     new section: "Where AI helps in operations, and the data it needs", after Step 1

Safe to run twice: each block carries data-v476="<id>" and is replaced, not duplicated.
Run before legacy_fixes.py and seo_pass.py.
"""
import os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
LEAN = "how-to-use-lean-methodology-to-eliminate-waste-and-streamline-operations"
AISTEPS = "5-proven-steps-to-integrate-ai-into-your-operations-workflow-for-smarter-faster-results"
RETIRE = {LEAN: ["identifying-non-value-added"],
          AISTEPS: ["revolutionizing-business-operations-how-ai-is-streamlining-efficiency-and-boosting-performance"]}


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table>\n<tr>{h}</tr>\n{b}\n</table>"


LEAN_HTML = f"""<h2 id="value-added-test">Value-added or not: a three-question test</h2>
<p>Before you can remove waste you have to see it, and most of it hides inside ordinary-looking work. A step adds value only if all three of these are true:</p>
<ol>
<li><strong>The customer would pay for it</strong> if they could see it being done.</li>
<li><strong>It changes the product or service</strong> in a way the customer cares about: shape, content, information or condition.</li>
<li><strong>It is done right the first time.</strong> Fixing an error is never value-adding, however necessary.</li>
</ol>
<p>Steps that fail the test fall into two groups. Some are pure waste and can go: re-keying data, waiting for an approval nobody uses, searching for tools. Others are necessary but not value-adding, such as regulatory records, safety checks and invoicing; the aim there is to make them as quick and simple as possible, not to remove them.</p>
{table(["Step in an order process", "Value-added?", "What to do"], [
    ("Cutting and welding the customer's part", "Yes", "Protect and improve"),
    ("Entering the order a second time in another system", "No: waste", "Remove with an integration"),
    ("Waiting two days for a manager's sign-off", "No: waste", "Replace with a rule; sign off exceptions only"),
    ("Recording material heat numbers for traceability", "No, but required", "Keep; capture by scanning, not typing"),
    ("Reworking a weld that failed inspection", "No: waste", "Find and fix the cause"),
])}
<p>When teams time a process this way, the value-adding steps are usually a small share of the total elapsed time; the rest is waiting and hand-offs. Our <a href="how-to-perform-a-successful-business-process-optimization.html">process optimization guide</a> has a worked example.</p>
"""

AI_HTML = f"""<h2 id="where-ai-helps">Where AI helps in operations, and the data it needs</h2>
<p>A use case is only realistic if the data behind it already exists or can be collected cheaply. This table pairs common operations uses with the data each one depends on.</p>
{table(["Use", "What AI does", "Data it needs"], [
    ("Predictive maintenance", "Flags equipment likely to fail before it stops", "Sensor readings (vibration, temperature, current) and a history of failures"),
    ("Demand forecasting", "Predicts orders by item and week", "Two or more years of sales history, promotions, seasonality"),
    ("Visual quality inspection", "Spots defects in camera images", "Hundreds of labelled images of good and bad parts"),
    ("Document and data entry", "Reads orders, invoices and forms into your systems", "Sample documents and a clear target format"),
    ("Customer service", "Answers routine questions and drafts replies", "Your policies, product information and past tickets"),
    ("Fraud and anomaly detection", "Flags unusual payments or transactions", "Transaction history with known problem cases"),
])}
<p>If the data column is a problem, start there: a few months of clean data collection often does more for the eventual result than the choice of AI tool.</p>
"""


def put(b, nid, html, before):
    b = re.sub(r'<section data-v476="' + nid + r'">.*?</section>\s*', "", b, flags=re.S)
    m = re.search(before, b)
    assert m, (nid, before)
    return b[:m.start()] + f'<section data-v476="{nid}">\n{html}</section>\n' + b[m.start():]


def edit(slug, nid, html, before):
    p = os.path.join(ROOT, "post", slug + ".html")
    s = open(p, encoding="utf-8").read()
    m = re.search(r'(<article class="prose">)(.*?)(</article>)', s, re.S)
    t = s[:m.start(2)] + put(m.group(2), nid, html, before) + s[m.end(2):]
    if t != s: open(p, "w", encoding="utf-8").write(t); print("updated", slug)
    else: print("unchanged", slug)


if __name__ == "__main__":
    edit(LEAN, "va", LEAN_HTML, r'<h2 id="tools-and-techniques-for-lean-implementation">')
    edit(AISTEPS, "ai", AI_HTML, r'<h2 id="step-2-')
