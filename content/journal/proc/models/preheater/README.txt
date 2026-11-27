Chmltech Online Journal, Vol. 106, Issue 21
Sizing the Feed Preheater Under Fouling Uncertainty: Area Margin, Cleaning and Condensate Stall
Quak Foo Lee, Chmltech Ltd., Vancouver, BC

Files
  hx_model.py         Full model: steam-heated preheater E-101 with Kern-Seaton tube-side fouling of uncertain level
                      and speed. Follows 500 fouling scenarios through a 24-month run in half-month steps over the 300
                      Issue 8 operating cases (seasonal groups, normal rate and 50% turndown); finds rate cuts,
                      unplanned cleanings, hours in condensate stall, installed and annual cost by area, and the rank
                      correlation of the inputs. Writes hx_results.json.
  hx_extras.py        Sensitivity runs: linear fouling, a 12-month run, condensate back pressure of 0.1 and 0.3 bar,
                      and area costing ten times the correlation. Reads hx_results.json; writes hx_extras.json.
  pumpvalve_model.py  The Issue 8 model (operating cases of the reactor feed); imported by hx_model.py.
  hx_appendix.py      Short script in the paper's appendix: clean and TEMA design areas at the design case, and the
                      shell pressure needed clean and fully fouled at a chosen area over 2,000 sampled fouling levels.
  hx_results.json     Results used in the paper.
  hx_extras.json      Sensitivity results used in the paper.

Run (Python 3 with NumPy and SciPy), from this folder:
  python3 hx_appendix.py
  python3 hx_model.py
  python3 hx_extras.py

Replace the generic inputs (feed properties, fouling ranges, coefficients, steam pressure, costs, margin) with your own
plant data before using the result for a decision.
