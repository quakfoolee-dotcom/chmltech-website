import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from insert import apply
P = __file__.rsplit("/", 2)[0] + "/journal/engineering-capex-and-opex-estimation-for-process-plants.json"
apply(P, [
 dict(sec="3", after=1, ref=("3", 2), sentence="Figure 1 shows the same ranges graphically: the band narrows sharply from Class 5 to Class 1, and at every class the upside is larger than the downside.",
      fig=dict(n=1, id="fig1-aace-accuracy", caption="Expected accuracy ranges of AACE estimate classes 5 to 1. The dark bar spans the narrowest and the light bar the widest range given for each class in Table 1.",
               alt="Horizontal bar chart of expected estimate accuracy for AACE classes 5 to 1. Class 5 spans from minus 50% to plus 100% at its widest and minus 20% to plus 30% at its narrowest; the ranges narrow class by class to Class 1 at minus 10% to plus 15% widest and minus 3% to plus 3% narrowest.",
               source="Drawn by the author from the ranges in [7].")),
 dict(sec="4", after=2, ref=("4", 3), sentence="Figure 2 plots Eq. (2) for typical exponents and shows how strongly the choice of n affects the result when the capacity ratio departs from one.",
      fig=dict(n=2, id="fig2-scaling", caption="Capacity-exponent scaling, Eq. (2), on logarithmic axes for n = 0.4, 0.6, 0.8 and 1.0. The marked point is the scale-up used in the worked example of Section 9.",
               alt="Log-log line chart of cost ratio against capacity ratio from 0.25 to 4 for exponents 0.4, 0.6, 0.8 and 1.0. Lower exponents give flatter lines. A marked point at capacity ratio 1.6 and cost ratio 1.326 shows the worked example.",
               source="Author's calculation from Eq. (2).")),
 dict(sec="8", after=1, ref=("8", 2), sentence="Figure 3 illustrates the shape of this trade-off: total annualized cost has a broad minimum, so moderate departures from the optimum cost little, while very small approach temperatures are heavily penalized.",
      fig=dict(n=3, id="fig3-tradeoff", caption="Schematic CAPEX–OPEX trade-off of Eq. (10) for heat recovery. Annualized capital rises steeply as ΔT<sub>min</sub> falls, utility cost rises with ΔT<sub>min</sub>, and total annualized cost has a minimum at the economic optimum. Curves are illustrative and not to scale.",
               alt="Schematic line chart of annual cost against minimum approach temperature. The annualized capital curve falls as approach temperature increases, the operating cost line rises, and the total annualized cost curve has a marked minimum labelled optimum delta T min.",
               source="Schematic by the author after the approach of [20, 21].")),
 dict(sec="9", after=2, ref=("9", 3), sentence="Figure 4 shows the simulated distributions of FCI and NPV.",
      fig=dict(n=4, id="fig4-monte-carlo", caption="Monte Carlo results of the illustrative example (20,000 trials, hypothetical data). (a) Cumulative distribution of FCI with the base estimate and the P50 and P90 values. (b) Distribution of NPV at 10%, with the P10, P50 and P90 values and the deterministic NPV; trials with negative NPV are shaded.",
               alt="Two-panel chart. Left: S-shaped cumulative probability curve of fixed capital investment, with the base estimate of 175, P50 of 182 and P90 of 217 million dollars marked. Right: histogram of net present value from about minus 150 to plus 150 million dollars, with P10 of minus 69, P50 of 11, P90 of 87 and the deterministic value of 43 marked; about 43% of trials are below zero.",
               source="Author's simulation using the inputs stated in the text.")),
])
print("placed")
