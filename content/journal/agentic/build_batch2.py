"""Write and check the November 13 batch of journal papers, Vol. 105, Issues 7-11 (V4.67).

Usage: python3 -I content/journal/agentic/build_batch2.py
Uses build.py (same checks as Issues 4-6) with a different paper list and date.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build

build.PAPERS = [p for p in ["paper_v105_i7", "paper_v105_i8", "paper_v105_i9", "paper_v105_i10", "paper_v105_i11"]
                if os.path.exists(os.path.join(build.HERE, p + ".py"))]
build.DATE = "2026-11-13"
if len(sys.argv) > 1: build.PAPERS = sys.argv[1:]
build.main()
