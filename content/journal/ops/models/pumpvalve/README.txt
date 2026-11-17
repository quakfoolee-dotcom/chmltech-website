Sizing Pumps and Control Valves Under Uncertainty: Monte Carlo Design Points for Chemical Plants
Chmltech Online Journal, Vol. 106, Issue 8 (Quak Foo Lee, Chmltech Ltd.)

Files
  pumpvalve_model.py     The model: 11 correlated inputs (Gaussian copula), system head (Darcy-Weisbach, Colebrook),
                         generic pump curve, IEC 60534-2-1 control valve sizing (Fp iterated, FLP, choked and xF checks),
                         API 610 motor and design-pressure checks, variable-speed drive. Run it alone for a quick check.
  analyze.py             Every result in the paper: rated points (P90/P95/P99, moderate and stacked margins), pump and valve
                         checks, coverage once the design unknowns are fixed, sensitivity, convergence (200 repeats), VFD,
                         energy and 20-year life-cycle cost. Writes results.json and figdata.json. Takes a few minutes.
  pumpvalve_appendix.py  The short script printed in the paper's Appendix B (P90/P95/P99 and stacked rated points).
  make_template.py       Builds the Excel equipment-list template from the model (needs openpyxl and results.json).
  results.json           Output of analyze.py, included so make_template.py runs without rerunning the analysis.

Requirements
  Python 3.10+ with NumPy and SciPy (pip install numpy scipy); openpyxl for the template.

Use
  python3 pumpvalve_appendix.py     -> P90 10.48 m3/h at 81.4 m, P95 10.68 at 82.5, P99 10.99 at 84.7, stacked 11.76 at 106.6
  python3 analyze.py                -> results.json (numbers in Tables 3 to 5 and the text)
  python3 make_template.py          -> chmltech-equipment-list-template.xlsx in the current folder

To size your own pump, edit INPUTS, CORR, BASE and WORST and the fixed parameters at the top of pumpvalve_model.py, then
rerun analyze.py. The pump curve, efficiency and NPSHr are generic: replace them with the vendor's curve when you have it.
