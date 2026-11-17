Beyond the Unit Price: Total Landed Cost Optimization for SME Sourcing
Chmltech Online Journal, Vol. 106, Issue 5 (2026). Model files.

Requirements: Python 3.10+, NumPy, PuLP 2.9 (pip install numpy pulp==2.9.0; PuLP 2.9 includes the CBC solver).

Files
  tlc_appendix.py  Short stand-alone version from the paper's Appendix: base-case plans only (C$573,614 and C$630,082).
  tlc_model.py     Full model: parts, prices, freight, tariff scenarios, the mixed-integer program (solve) and plan costing.
  tlc_risk.py      Monte Carlo risk layer: freight rate, exchange rate, tariff scenario and China-lane disruptions.
  run_tlc.py       Section 5 and 6 results for the five plans (deterministic costs and 20,000 simulated years each).
  sweeps.py        Figure 2 (container-rate sweep) and Figure 4 (shortage-cost sweep).

Run
  python3 tlc_appendix.py
  python3 run_tlc.py        writes results_v1.json and mc_*.npy (a few minutes)
  python3 sweeps.py         writes feu_sweep.json and short_sweep.json

The case is a composite and its prices, tariff rates and risk weights are illustrative. Confirm tariff classifications
and surtaxes for real parts with a customs broker. Licence: free to use and adapt with attribution to the paper.
