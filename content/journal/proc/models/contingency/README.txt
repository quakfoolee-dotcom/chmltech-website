Chmltech Online Journal, Vol. 106, Issue 20
Setting Cost Contingency by Monte Carlo: P50, P80 and the Risks Behind Them for a C$100 Million Process Plant
Quak Foo Lee, Chmltech Ltd., Vancouver, BC

Files
  contingency_model.py      Full model: the Class 3 estimate of the C$100M, 50,000 t/y plant in 12 cost accounts with
                            skewed triangular ranges correlated by driver group (Gaussian copula), the 8-event risk
                            register with delays priced at the burn rate, and the escalation and exchange-rate reserve.
                            Runs 50,000 iterations for the P50/P80/P90, the build-up of the contingency, the drivers
                            (accounts fixed at their mean, risks removed or set at expected value), the correlation,
                            range-width and market-correlation cases, the estimate classes and first-of-a-kind case.
                            Writes contingency_results.json.
  contingency_appendix.py   Short script in the paper's appendix: P50, P80 and P90 at base-date prices, the chance of
                            overrunning flat contingencies of 10% and 15%, and the escalation reserve.
  contingency_results.json  Results used in the paper.

Run (Python 3 with NumPy and SciPy), from this folder:
  python3 contingency_model.py
  python3 contingency_appendix.py

The ranges and risk register are illustrative. Replace them with your own estimate, ranges and risks before using the
result for a budget decision.
