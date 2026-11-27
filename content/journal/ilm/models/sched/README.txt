Chmltech Online Journal, Vol. 106, Issue 18 - LLM-written scheduling models: error-injection study (V2)
llm_sched.py      : Monday snapshots of the Vol. 106, Issue 4 plant (12 weeks of MDD operation first), reference CP-SAT model,
                    five dispatching rules, hand-injected faults F1-F8, right-shift and non-delay repair, gates G1-G4.
                    Each model is solved with a warm start from the best rule (main) and without one (sensitivity).
                    pip install ortools numpy ; python3 llm_sched.py 30 1   -> results.json (about 70 minutes on 2 cores)
                    The solver uses a deterministic work limit with interleaved workers, so results repeat exactly.
summarize.py      : results.json -> summary.json (tables and figures in the paper)
gates_appendix.py : compact gates G1-G4, dispatching baseline and right-shift repair (standard library only)
