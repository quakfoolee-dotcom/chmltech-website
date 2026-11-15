"""Write and check Vol. 106, Issue 1 (Multi-Agent AI Engineering series, article 1).

Usage: python3 -I content/journal/agentic/build_v106.py
Figure 1 is interactive: its fig block gets "live": "orch5" (markup content/journal/live/orch5.html, drawn by
content/journal/figure-scripts/orch5.py, which also writes the static SVG used for print and the PDF).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build, jmark

LIVE = {"fig1-five-models": "orch5"}
_parse = jmark.parse


def parse(src):
    secs = _parse(src)
    for s in secs:
        for b in s["blocks"]:
            if "fig" in b and b["fig"]["id"] in LIVE: b["fig"]["live"] = LIVE[b["fig"]["id"]]
    return secs


jmark.parse = parse
build.PAPERS = ["paper_v106_i1"]
build.DATE = "2026-11-14"
build.main()
