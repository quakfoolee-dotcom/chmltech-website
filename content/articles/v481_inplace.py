"""V4.81 in-place upgrade: the AI five-steps post gains a worked example and a link to the agent-readiness guide.
Idempotent: re-running leaves the page unchanged."""
import os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AISTEPS = "5-proven-steps-to-integrate-ai-into-your-operations-workflow-for-smarter-faster-results"

AI_EXAMPLE = """<h2 id="worked-example">Worked example: the five steps in a distributor</h2>
<p>A regional industrial distributor receives about 60 customer orders a day by email, many as PDF purchase orders. Two staff key each one into the ERP, which takes about six minutes per order, and keying errors cause a handful of wrong shipments each month.</p>
<table>
<tr><th>Step</th><th>What the distributor did</th></tr>
<tr><td>1. Identify the area</td><td>Order entry: high volume, repetitive, measurable and a known source of errors</td></tr>
<tr><td>2. Set the goal</td><td>Cut keying time by half and wrong shipments by two-thirds within six months, without adding staff</td></tr>
<tr><td>3. Fix the data</td><td>Cleaned the customer part-number cross-reference in the ERP, the main reason documents could not be matched</td></tr>
<tr><td>4. Implement and improve</td><td>An AI document-extraction tool reads each PO and drafts the ERP order; staff check and release it. Mismatches are logged and fixed weekly</td></tr>
<tr><td>5. Measure and scale</td><td>Tracked minutes per order, share of orders needing correction and wrong shipments; after three months, extended the same tool to supplier invoices</td></tr>
</table>
<p>Keeping a person to check and release each order was deliberate: it protects customers while the tool learns the firm's documents, and it builds trust before any step is fully automated. The figures are illustrative. For a deeper look at what needs to be in place before AI tools act on their own, see <a href="agent-readiness-for-small-and-mid-sized-firms-data-process-staged-adoption.html">agent readiness for small and mid-sized firms</a>.</p>
"""


def run():
    p = os.path.join(ROOT, "post", AISTEPS + ".html")
    s = open(p, encoding="utf-8").read()
    if 'data-v481="ai-example"' in s: print("unchanged", AISTEPS); return
    m = re.search(r'<h2(?: id="[^"]*")?>Your Next Step Toward', s)
    assert m
    s = s[:m.start()] + f'<section data-v481="ai-example">\n{AI_EXAMPLE}</section>\n' + s[m.start():]
    open(p, "w", encoding="utf-8").write(s); print("updated", AISTEPS)


if __name__ == "__main__":
    run()
