Chmltech Online Journal, Vol. 106, Issue 19
Stocking Critical Spare Parts Under Uncertainty: When ABC Analysis and Safety Stock Formulas Fail
Quak Foo Lee, Chmltech Ltd., Vancouver, BC

Files
  spares_model.py       Full model: the 13 critical spares (PARTS), uncertain inputs (SCEN, LAM_SIGMA), discrete-event
                        simulation of (S-1, S) one-for-one stocking with installed spares, buffers, partial capacity
                        loss and restarts (simulate()), 2,000 scenarios at stock levels 0 to 4 (evaluate()), and the
                        usual rules for comparison (safety stock formula, Poisson 95% ready rate and fill rate, one of
                        each). Writes spares_results.json.
  analyse.py            Whole-set comparison of the stocking rules (Table 3, Figure 2), regret of the chosen stock
                        levels and the screening indices of Eqs. (3) and (4) against the simulation (Figure 4).
                        Imports spares_model.py and adds its results to spares_results.json.
  extras.py             Failure-rate spread, unfavourable margin and carrying rate, installed spare pump, repair,
                        pooling among three plants and the decision map (Sections 6 to 8, Figures 3 and 5). Adds its
                        results to spares_results.json.
  spares_appendix.py    Short script in the paper's appendix: Eqs. (1) to (4) at most likely values, no simulation.
  spares_results.json   Results used in the paper.

Run (Python 3 with NumPy and SciPy), from this folder, in this order:
  python3 spares_model.py
  python3 analyse.py
  python3 extras.py
  python3 spares_appendix.py
spares_model.py takes about 20 s, analyse.py about 40 s and extras.py about 75 s; the appendix script runs in about a
second. analyse.py and extras.py read and rewrite spares_results.json, so run spares_model.py first.

Replace the generic inputs (failure rates, lead times, unit costs, repair times, capacity lost, margin and carrying
rate) with your own plant data before using the result for a decision.
