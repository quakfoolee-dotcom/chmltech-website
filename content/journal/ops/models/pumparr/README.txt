Chmltech Online Journal, Vol. 106, Issue 9
Choosing the Pump Arrangement Under Uncertainty: Monte Carlo Comparison of Single, Parallel and Variable-Speed Options
Quak Foo Lee, Chmltech Ltd., Vancouver, BC

Files
  pump_arrangements_model.py   Full model: hydraulics of arrangements A, B, C3, C2, E3, E2 and variant D over the 20,000
                               operating cases of Issue 8 (normal and 50% turndown), 20-year discrete-event failure
                               simulation, 5,000 economic scenarios, life-cycle cost, regret, drivers, duty-size scan,
                               curve shape, long turndown and drive-cost break-even. Writes arr_results.json,
                               arr_figdata.json and arr_scenarios.npz. About 10 s.
  pumpvalve_model.py           The Issue 8 model (operating cases, system head, rated point); imported by the model.
  pump_arrangement_appendix.py Short script in the paper's appendix: average power of A, B, C and E.
  make_template.py             Builds the Excel template from the model's outputs (run the model first).
  results.json                 Results used in the paper.

Run (Python 3 with NumPy and SciPy; openpyxl for the template), from this folder:
  python3 pump_arrangements_model.py
  python3 pump_arrangement_appendix.py
  python3 make_template.py

Replace the generic inputs (pump curves, efficiencies, costs, failure and repair data, margin) with your own plant
data before using the result for a decision.
