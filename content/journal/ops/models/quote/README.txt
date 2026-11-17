Quoting Lead Times You Can Keep: Due-Date Setting for Make-to-Order Manufacturers
Chmltech Online Journal, Vol. 106, Issue 6 (2026). Model files.

Requirements: Python 3.10+ and NumPy.

Files
  quote_appendix.py  Short stand-alone version from the paper's Appendix (routing and backlog-plus-work quotes, FIFO and
                     load-based release with MDD); about 15 seconds.
  shop.py, tune.py   The windows-and-doors job shop of Vol. 106, Issue 4 (stations, product families, calibration).
  qsim.py            The shop simulation with a quote hook and the five quoting rules.
  qfit.py            Fits the regression ("fitted") rule on 50 training years (seeds 2000-2049); writes qfit.json.
  qsweep.py          Margin sweeps for every rule and both scheduling policies (Figure 1, Tables 2 and 3); writes qsweep.json.
  qsweep2.py         Extra margin points added to qsweep.json.
  qstress.py         Order spike and load-range stress tests (Figure 2, Table 4); writes qstress.json.
  qsize.py           Quotes and on-time delivery by order size; writes qsize.json.

Run in this order: python3 qfit.py; python3 qsweep.py; python3 qsweep2.py; python3 qstress.py; python3 qsize.py
Each experiment runs 100 simulated years per setting and uses all CPU cores; the full set takes about an hour.
Licence: free to use and adapt with attribution to the paper.
