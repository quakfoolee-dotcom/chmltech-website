Chmltech Online Journal, Vol. 106, Issue 23
Hybrid Digital Twins for Heat Exchanger Fouling: Physics, Machine Learning and the Combination Tested on a Steam Preheater
Quak Foo Lee, Chmltech Ltd., Vancouver, BC

Files
  twin_model.py       Full model: synthetic plant histories of the steam preheater E-101 (three two-year runs of
                      4-hourly records with seasonal feed temperature, turndown campaigns, instrument noise and drift,
                      true Kern-Seaton fouling), the four monitors (physics only, constant correction, hybrid,
                      gradient-boosted machine learning), fouling-estimate errors, cleaning forecasts and shell
                      pressure at turndown. Writes twin_results.json.
  twin_summary.py     Summarises the histories in twin_results.json (medians, P90, forecasts within 20%) and
                      writes twin_summary.json: the numbers in Table 2 and Figures 3 and 4 of the paper.
  twin_appendix.py    Short script in the paper's appendix: the hybrid monitor on its own. Prints a learned
                      correction of 0.863 at Reynolds number 18,000 and a forecast limit of about 1,650 h.
  twin_results.json   Results of the 20 histories used in the paper.
  twin_summary.json   Summary used in the paper.

Run (Python 3 with NumPy, SciPy and scikit-learn), from this folder:
  python3 twin_model.py 20      (20 histories, about 5 minutes)
  python3 twin_summary.py
  python3 twin_appendix.py

The plant is synthetic. Replace the synthetic histories with the four instrument tags of a real exchanger (feed flow,
inlet and outlet temperature, shell pressure) and your own geometry and correlations before using the result for a
decision.
