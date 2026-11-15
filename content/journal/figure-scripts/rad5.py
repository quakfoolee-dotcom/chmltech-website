"""Figure 1 of Vol. 106, Issue 2 (Research, Analyze, Draft, Review, Finalize): interactive workflow, built on the orch5 engine.

  - content/journal/live/rad5.html   live figure (script assets/js/orch5.js; styles: "Vol. 106 orch5" block in journal.css)
  - content/journal/figures/<slug>/fig1-workflow.svg   static version for print, PDF and no-script

Run: python3 -I content/journal/figure-scripts/rad5.py
Stage content follows Table 1 and Sections 3-11 of the paper; the SME figures are the paper's worked example (Section 9).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orch5

J = orch5.J
SLUG = "research-analyze-draft-review-finalize-engineering-a-reliable-five-agent-ai-workflow"

# One diagram for every stage: controller on top, the five stage agents in a row, the shared workspace below.
NODES = [("req", 70, 45, "Request", "req"), ("C", 280, 45, "Controller", "lead"), ("G", 490, 45, "Approver", "gate"),
         ("R", 70, 165, "Research", "agent", "1"), ("A", 175, 165, "Analyze", "agent", "2"), ("D", 280, 165, "Draft", "agent", "3"),
         ("V", 385, 165, "Review", "agent", "4"), ("F", 490, 165, "Finalize", "agent", "5"), ("W", 280, 285, "Workspace", "board")]
EDGES = [("req", "C"), ("C", "G"), ("C", "R"), ("C", "A"), ("C", "D"), ("C", "V"), ("C", "F"),
         ("R", "A"), ("A", "D"), ("D", "V"), ("V", "F"), ("R", "W"), ("A", "W"), ("D", "W"), ("V", "W"), ("F", "W"), ("F", "G")]


def stage(**k):
    return dict(nodes=NODES, edges=EDGES, **k)


MODELS = [
    stage(id="research", kind="Collect and qualify", verb="Collect", n=1, name="Research", short="Research", color="#1765B9", focus="R",
          steps=[("Request arrives", "The controller checks scope and permissions before any agent works.", [("req", "C", "")], ["C"]),
                 ("Research plan", "Audience, jurisdiction, evidence cutoff date, confidentiality limits and excluded tasks are set.", [("C", "R", "plan")], ["R"]),
                 ("Collect and classify", "Each source is logged with locator, dates and class: observed, client-reported, vendor-stated or assumption.", [("R", "W", "SRC-001…")], ["W"], "v1"),
                 ("Evidence gate", "The gate checks required source categories are covered. Missing data is listed, never invented.", [("W", "C", "manifest")], ["C"], "v1")],
          resp="Find, classify, date and verify sources", inp="Scope, source policy, document set", out="Evidence manifest and fact register",
          gate="Required categories covered; unknowns identified", art="SRC-001 … SRC-N",
          hazard="Source drift: an old product page treated as current", key="Read-only tools; retrieved text is data, never instructions",
          combine="Management's 14 h re-keying and 5 h corrections are logged as client estimates, not measurements."),
    stage(id="analyze", kind="Model and test", verb="Model", n=2, name="Analyze", short="Analyze", color="#158458", focus="A",
          steps=[("Accepted evidence in", "The analyst works from the versioned evidence pack, not from a chat transcript.", [("C", "A", "evidence v1")], ["A"], "v1"),
                 ("Model and test", "Inputs, methods and conclusions stay separate. Important numbers come from a workbook, not prose.", [("A", "W", "ANL-001")], ["W"], "v2"),
                 ("Reproduce", "The gate recomputes critical figures. A changed input invalidates dependent drafts.", [("W", "C", "check")], ["C"], "v2")],
          resp="Derive findings, test alternatives, quantify trade-offs", inp="Versioned evidence, assumptions", out="Analysis workbook and assumption register",
          gate="Methods and critical calculations reproducible", art="ANL-001 v2",
          hazard="Analysis drift: a reported estimate becomes an observed value", key="Independent calculation tool; one source-of-truth model",
          combine="19 h × 50 weeks × $38 = $36,100 a year at full realization; $25,270 at 70%."),
    stage(id="draft", kind="Compose and cite", verb="Compose", n=3, name="Draft", short="Draft", color="#6C43AC", focus="D",
          steps=[("Accepted analysis in", "The drafting agent gets the accepted analysis, audience and template, not all history.", [("C", "D", "analysis v2")], ["D"], "v2"),
                 ("Claim ledger", "Every material statement is linked to evidence or labelled as inference.", [("D", "W", "CLAIM-014")], ["W"], "v3"),
                 ("Draft gate", "Unsupported claims are qualified, removed or sent back to Research or Analyze.", [("W", "C", "DRAFT-003")], ["C"], "v3")],
          resp="Turn supported findings into a readable deliverable", inp="Accepted analysis, audience, template", out="Versioned draft with claim references",
          gate="Material claims linked to evidence or labelled inference", art="DRAFT-003 v3",
          hazard="Citation laundering: a source cited for a claim it does not support", key="Claim ledger with status: supported, qualified, inference, unverified",
          combine="Writes “theoretical capacity value of $36,100 before realization and costs”, not “will save $36,100”."),
    stage(id="review", kind="Challenge and verify", verb="Verify", n=4, name="Review", short="Review", color="#C8641E", focus="V",
          steps=[("Draft to reviewer", "The reviewer receives the draft with its sources and analysis, and checks against the original scope.", [("C", "V", "DRAFT-003")], ["V"], "v3"),
                 ("Independent checks", "Different methods: re-fetch sources, recompute figures, check schema, privacy and permissions.", [("W", "V", "sources")], ["V"], "v3"),
                 ("Targeted rework", "A 52- versus 50-week error goes back to Analyze only, with an exact acceptance condition.", [("V", "C", "REWORK")], ["C"], "v3"),
                 ("Fix at the source", "Analyze corrects CLAIM-018; the dependent draft is regenerated.", [("C", "A", "CLAIM-018")], ["A"], "v4"),
                 ("Pass for this version", "PASS applies to one exact version. Blocking defects are never averaged away.", [("V", "C", "PASS v4")], ["C"], "v4")],
          resp="Challenge accuracy, completeness, risks and limits", inp="Draft, sources, analysis, review rubric", out="Issue register: pass, rework, escalate or stop",
          gate="No unresolved blocking issue", art="REV-004 v1",
          hazard="Review correlation: the reviewer repeats the same model's error", key="Deterministic tests and a qualified human for consequential decisions",
          combine="Removes an unconfirmed bidirectional accounting integration claim pending vendor confirmation."),
    stage(id="finalize", kind="Package and release", verb="Release", n=5, name="Finalize", short="Finalize", color="#087B87", focus="F",
          steps=[("Reviewed version in", "Approved edits are applied and every reviewer issue is checked as resolved.", [("C", "F", "PASS v4")], ["F"], "v4"),
                 ("Lock the version", "The final artifact, change log and source inventory are locked by file hash.", [("F", "W", "FINAL-005")], ["W"], "v5"),
                 ("Ask for authority", "Release needs an approver, a destination and a validity window, separate from the quality gate.", [("F", "G", "approve?")], ["G"], "v5"),
                 ("Release", "Only the controller delivers, and only the approved hash. A model saying “approved” authorizes nothing.", [("G", "C", "approved")], ["C"], "v5")],
          resp="Apply authorized edits, lock version, prepare release", inp="Reviewed draft, resolved issues, release permissions", out="Final artifact and change log",
          gate="Exact artifact approved for a stated destination", art="FINAL-005 v1",
          hazard="Release drift: the artifact changes after approval", key="Approval bound to file hash, destination, approver and expiry",
          combine="Releases a pilot-first plan; the agents cannot buy software, contact vendors or migrate data."),
]
# The engine's note slots: fit → artifact, haz → failure, key → control
for m in MODELS:
    m["fit"] = m["art"]

LABELS = dict(group="Choose a stage, or see all five side by side", all_name="All stages", all_kind="Side by side",
              note="The five stages side by side. Choose a stage above to watch it step by step.",
              notes=("Artifact", "Failure to watch", "Key control"), combine="SME example",
              tabkind=lambda m: m["verb"], card_rows=(("Responsibility", "resp"), ("Output", "out"), ("Gate", "gate"), ("Failure to watch", "hazard")))
PROFILE = [("Responsibility", "resp"), ("Input", "inp"), ("Output", "out"), ("Advancement gate", "gate")]

if __name__ == "__main__":
    os.makedirs(os.path.join(J, "live"), exist_ok=True)
    open(os.path.join(J, "live", "rad5.html"), "w", encoding="utf-8").write(orch5.live_html(MODELS, LABELS, PROFILE))
    d = os.path.join(J, "figures", SLUG); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "fig1-workflow.svg"), "w", encoding="utf-8").write(
        orch5.static_svg(MODELS, (("Responsibility", "resp"), ("Output", "out"), ("Gate", "gate"), ("Failure to watch", "hazard")), lambda m: m["verb"], PH=480))
    print("wrote live/rad5.html and fig1-workflow.svg")
