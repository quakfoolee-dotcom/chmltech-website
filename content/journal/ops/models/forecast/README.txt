Forecasting Lumpy Demand: Does Croston Beat a Moving Average?
Chmltech Online Journal, Vol. 106, Issue 7 (2026). Model files.

Requirements: Python 3.10+, NumPy; SciPy for fanalyze2.py (pip install numpy scipy).

Files
  croston_appendix.py  Short stand-alone version from the paper's Appendix: one population of 1,000 items, six methods.
  fsim.py              Item generator, demand classes, the forecasting methods, reorder-level rules (including the
                       long-history benchmarks) and the weekly order-up-to inventory policy.
  frun.py              Five populations of 1,000 items; sweeps each method's safety factor (Figure 1, Tables 2 and 3).
  fanalyze.py          Interpolates the stock needed for a target fill rate.
  fanalyze2.py         Results at 90% and 95% fill with t intervals across populations.
  fobs.py              Obsolescence test (Table 5): reorder-level lag and orders after the last sale.
  facc.py              Forecast error on intermittent and lumpy items (Table 4).
  fitem.py             Spread of fill rate across items at the pooled 95% setting.

Run
  python3 frun.py 0                                 stable demand -> frun2_stop0.json
  python3 frun.py -1                                level-shift scenario -> frun2_shift.json
  METHODS=tsb10,tsb20 TAG=frun_tsbb python3 frun.py 0   TSB with faster probability updates
  python3 fanalyze2.py; python3 fobs.py; python3 fitem.py; python3 facc.py
frun.py uses two processes and takes about 20 minutes per scenario.
Licence: free to use and adapt with attribution to the paper.
