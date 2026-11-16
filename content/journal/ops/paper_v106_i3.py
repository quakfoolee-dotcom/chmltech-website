"""Chmltech Online Journal, Vol. 106, Issue 3: Beyond the Formula: Setting Safety Stock with Monte Carlo Simulation (Nov 16 2026).

Composite case (imported epoxy resin at a BC distributor). Model: content/journal/ops/models/safety_stock/ (lead-time-demand Monte Carlo,
40 x 200-year (s, Q) policy runs, sensitivity). Red-team checked (model audit and references) before publication."""

SLUG = "beyond-the-formula-setting-safety-stock-with-monte-carlo-simulation"
META = dict(
    volume=106, issue=3,
    title="Beyond the Formula: Setting Safety Stock with Monte Carlo Simulation",
    short_title="Setting Safety Stock with Monte Carlo Simulation",
    meta="Why the textbook safety stock formula misses its target for lumpy demand and late imports, and how Monte Carlo simulation sets a reorder point that holds.",
    keywords=["safety stock", "Monte Carlo simulation", "reorder point", "lead-time demand", "cycle service level", "fill rate", "undershoot", "inventory policy"],
)
ABSTRACT = ("The textbook safety stock formula assumes that demand over the replenishment lead time is normal, that daily demand is independent "
            "and that lead time is stable. Many small and mid-sized distributors break these assumptions: customer orders are lumpy, and imported "
            "supply occasionally arrives weeks late. This paper shows how Monte Carlo simulation sets the reorder point directly from the simulated "
            "distribution of lead-time demand, then validates it with a day-by-day policy simulation. In a composite case for an imported specialty "
            "resin, the full formula targets 95% cycle service but covers 92.9% of simulated cycles, and a common shortcut that uses the supplier's "
            "quoted lead time covers 82%. The 95th percentile of simulated lead-time demand gives a reorder point of about 759 pails, 44 above the "
            "formula. A policy simulation over 40 independent 200-year runs adds one further correction: lumpy daily demand carries inventory below "
            "the reorder point before an order is placed, by about 18 pails on average, so the reorder point that delivers 95% cycle service is about "
            "777. The cost curve is flat near its minimum at roughly 690 pails, and 95% cycle service costs about $1,100 a year more. Supplier "
            "disruption is the largest single driver of safety stock.")

W = "https://search.worldcat.org/search?q="
REFS = {
    "series": ("Lee, Q. F. (2026). Setting safety stock without guessing: Three methods and a worked example. <em>Chmltech Insights</em>.",
               "https://www.chmltech.com/post/setting-safety-stock.html"),
    "silver": ("Silver, E. A., Pyke, D. F., &amp; Thomas, D. J. (2017). <em>Inventory and production management in supply chains</em> (4th ed.). CRC Press.",
               "https://doi.org/10.1201/9781315374406"),
    "chopra": ("Chopra, S. (2019). <em>Supply chain management: Strategy, planning, and operation</em> (7th ed.). Pearson.",
               W + "Chopra+Supply+Chain+Management+Strategy+Planning+and+Operation+7th+edition"),
    "eppen": ("Eppen, G. D., &amp; Martin, R. K. (1988). Determining safety stock in the presence of stochastic lead time and demand. <em>Management Science</em>, 34(11), 1380–1390.",
              "https://doi.org/10.1287/mnsc.34.11.1380"),
    "crd": ("Chopra, S., Reinhardt, G., &amp; Dada, M. (2004). The effect of lead time uncertainty on safety stocks. <em>Decision Sciences</em>, 35(1), 1–24.",
            "https://doi.org/10.1111/j.1540-5414.2004.02332.x"),
    "tyworth": ("Tyworth, J. E., &amp; O'Neill, L. (1997). Robustness of the normal approximation of lead-time demand in a distribution setting. <em>Naval Research Logistics</em>, 44(2), 165–186.",
                "https://econpapers.repec.org/RePEc:wly:navres:v:44:y:1997:i:2:p:165-186"),
    "burgin": ("Burgin, T. A. (1975). The gamma distribution and inventory control. <em>Operational Research Quarterly</em>, 26, 507–525.",
               "https://portal.mardi4nfdi.de/wiki/Item:Q4091684"),
    "disney": ("Disney, S. M., Maltz, A., Wang, X., &amp; Warburton, R. D. H. (2016). Inventory management for stochastic lead times with order crossovers. <em>European Journal of Operational Research</em>, 248(2), 473–486.",
               "https://doi.org/10.1016/j.ejor.2015.07.047"),
    "hayya": ("Hayya, J. C., Bagchi, U., Kim, J. G., &amp; Sun, D. (2008). On static stochastic order crossover. <em>International Journal of Production Economics</em>, 114(1), 404–413.",
              "https://econpapers.repec.org/RePEc:eee:proeco:v:114:y:2008:i:1:p:404-413"),
    "croston": ("Croston, J. D. (1972). Forecasting and stock control for intermittent demands. <em>Operational Research Quarterly</em>, 23(3), 289–303.",
                "https://econbiz.de/Record/forecasting-and-stock-control-for-intermittent-demands-croston/10002044036"),
    "axsater": ("Axsäter, S. (2015). <em>Inventory control</em> (3rd ed.). Springer.",
                "https://doi.org/10.1007/978-3-319-15729-0"),
    "law": ("Law, A. M. (2015). <em>Simulation modeling and analysis</em> (5th ed.). McGraw-Hill Education.",
            W + "Law+Simulation+Modeling+and+Analysis+5th+edition"),
    "sbc": ("Syntetos, A. A., Boylan, J. E., &amp; Croston, J. D. (2005). On the categorization of demand patterns. <em>Journal of the Operational Research Society</em>, 56(5), 495–503.",
            "https://doi.org/10.1057/palgrave.jors.2601841"),
}

CODE = {"appendix": open(__file__.replace("paper_v106_i3.py", "models/safety_stock/mc_safety_stock.py"), encoding="utf-8").read().rstrip()}

BODY = r"""
## Introduction

Safety stock is cash held against uncertainty. Set too low, it leaves customers waiting; set too high, it ties up working capital on the shelf. For a distributor carrying $650,000 a year of one imported item, an error of 100 units in safety stock is worth $18,000 of inventory.

The standard approach ranks items by value and sets safety stock with a formula based on the normal distribution [@series, @silver]. The formula works well when demand is steady and suppliers are reliable. It works poorly in three situations common to Canadian small and mid-sized enterprises (SMEs):

- **Lumpy demand.** A few large contractor or plant orders make up much of the volume, with many days of no sales at all.
- **Long, skewed import lead times.** Ocean freight usually arrives close to plan but sometimes arrives two to five weeks late. Lateness has a long right tail; earliness does not.
- **A service promise the formula cannot test.** The formula sets a cycle service level, but customers experience the fill rate, and management pays the cost of both.

Monte Carlo simulation addresses all three. It replaces the normal-distribution assumption with thousands of simulated replenishment cycles built from the item's own demand and lead-time behaviour, reads the reorder point directly from the simulated distribution, and then tests the reorder rule day by day. This paper explains the method, applies it to a composite case, validates the answer with a policy simulation, and gives a practical guide for implementation in a spreadsheet or a short script.

## The Classical Formula and Its Hidden Assumptions

Under continuous review, a replenishment order is placed when the inventory position falls to the reorder point. The reorder point covers expected demand during the lead time plus a safety stock, as in Eq. (1):

TEX ROP = \bar{d}\,\bar{L} + SS

When both daily demand and lead time vary, the standard textbook safety stock is given by Eq. (2) [@silver, @chopra]:

TEX SS = z_{\alpha}\sqrt{\bar{L}\,\sigma_d^{2} + \bar{d}^{2}\,\sigma_L^{2}}

Here d̄ and σ<sub>d</sub> are the mean and standard deviation of daily demand, L̄ and σ<sub>L</sub> are the mean and standard deviation of lead time, and z<sub>α</sub> is the standard normal value for the target cycle service level (1.645 for 95%). Many spreadsheets use the shorter Eq. (3), which drops lead-time variability and uses the supplier's quoted lead time L<sub>p</sub>:

TEX SS_{\text{short}} = z_{\alpha}\,\sigma_d\sqrt{L_p}

Both versions rest on assumptions that are rarely checked (Table 1).

TABLE Assumptions behind the safety stock formula and where SMEs break them.
| Assumption | What it requires | Where SMEs break it |
| Normal lead-time demand | Demand over the lead time is symmetric and bell-shaped | Lumpy orders and late shipments create a long right tail |
| Independent days | Each day's demand is unrelated to the next | Project-driven and seasonal buying come in runs |
| Stable lead time | Lead time has one well-behaved distribution | Port congestion and rolled sailings add occasional large delays |
| Continuous review, no undershoot | Stock is reviewed continuously and an order is placed exactly at the reorder point | Daily review and large orders carry stock below the reorder point before an order is placed |
| Orders arrive in sequence | Each order arrives before the next one is placed, or at least in order | Long, variable lead times overlap and can cross |
| Cycle service is the goal | Probability of no stockout per cycle is what matters | Customers judge the fill rate, the share of units shipped on time |

Eppen and Martin showed that the widely used procedure, which treats lead-time demand as normal with the combined mean and variance, can give results far from the intended service level, and they gave corrected procedures, including for parameters estimated from data [@eppen]. Lead-time demand is a random sum whose shape depends on the lead-time distribution, so it is generally not normal [@crd]. The evidence is not one-sided: for fast-moving finished goods the normal approximation has been found robust with respect to cost and service [@tyworth], and analytical alternatives such as the gamma distribution have long been available [@burgin]. The formula also assumes orders arrive in the sequence they were placed, an assumption that long and variable lead times violate [@hayya, @disney]. Monte Carlo avoids the normal approximation entirely, and a policy simulation captures undershoot and overlapping orders.

## The Monte Carlo Method, Step by Step

The method simulates what the reorder point must protect against: total demand between placing an order and receiving it. Each iteration is one possible replenishment cycle.

1. **Model demand from history.** Split daily demand into how many orders arrive (a Poisson count) and how large each order is (a lognormal or empirical size distribution). This two-part model, often called compound or stuttering Poisson, reproduces zero-demand days and occasional large orders [@croston].
2. **Model lead time from receipts.** Fit the normal transit time, then add a separate disruption term: a probability that a shipment is delayed, and the range of extra days when it is. Fit the disruption tail to actual receipt dates; the reorder point is sensitive to it.
3. **Draw one lead time.** Sample a lead time L from the lead-time model.
4. **Draw L days of demand and add them up.** The sum is one sample of lead-time demand.
5. **Repeat 10,000 to 100,000 times.** The samples form the empirical distribution of lead-time demand, whatever its shape.
6. **Read the reorder point as a percentile.** For 95% cycle service, take the 95th percentile of the samples.
7. **Add the undershoot.** With daily review and lumpy demand, inventory position is usually already below the reorder point on the day an order is triggered. Add the expected undershoot, about E[D²]/(2E[D]) for daily demand D [@axsater, @silver]. Safety stock is the corrected reorder point minus mean lead-time demand.
8. **Validate with a policy simulation.** Run the actual reorder rule day by day, with orders in transit, to measure cycle service, fill rate and cost.

In symbols, for iteration i with sampled lead time L<sub>i</sub> and daily demands d<sub>i,t</sub>, the method computes Eq. (4):

TEX LTD_i = \sum_{t=1}^{L_i} d_{i,t}, \qquad ROP_{\alpha} \approx F_{LTD}^{-1}(\alpha) + \frac{\sigma_d^{2} + \bar{d}^{2}}{2\bar{d}}, \qquad SS = ROP_{\alpha} - \overline{LTD}

Steps 1 to 7 need only a spreadsheet. Step 8 needs a short script, given in the Appendix.

## Worked Case: An Imported Specialty Resin

The case is a composite built for this paper. A Lower Mainland industrial distributor stocks a two-part epoxy resin in 20 kg pails, imported from an Asian manufacturer through the Port of Vancouver. It sells about 3,600 pails a year at a landed cost of $180, roughly $650,000 a year. Demand comes from flooring contractors and two maintenance shops; most orders are small and a few are very large. Table 2 lists the inputs.

TABLE Case inputs.
| Input | Model | Value |
| Customer orders per day | Poisson | mean 1.2 |
| Pails per order | Lognormal | mean 12, CV 0.9 |
| Normal supplier lead time | Lognormal | mean 30 working days, SD 4 |
| Shipment disruption | Bernoulli × uniform delay | 15% chance of 10 to 25 extra working days |
| Order quantity Q | Fixed | 500 pails (about 7 orders a year) |
| Landed unit cost | Fixed | $180 per pail |
| Holding cost | 25% a year | $45 per pail-year |
| Target cycle service level | Policy | 95% |

These inputs give mean daily demand of 14.4 pails with a standard deviation of 17.7 (CV 1.23), and no sales on 30% of days. Lead time averages 32.6 working days with a standard deviation of 7.6.

### 4.1 Results

One hundred thousand simulated replenishment cycles give a lead-time demand averaging 470 pails, with a median of 446 and a right skew of 0.92 (Figure 1). The distribution is not normal: its right tail is longer than its left, and the tail is where stockouts happen. Most of that tail comes from the 15% of shipments that arrive late. Each lead time spans about 40 customer orders, so lumpy order sizes largely average out over a lead time; the late shipments do not.

FIG fig1-ltd-distribution || Simulated lead-time demand over 100,000 replenishment cycles, with the reorder points from the shortcut formula, the full formula and the Monte Carlo 95th percentile, and the share of cycles each covers. || Histogram of lead-time demand from about 150 to 1,200 pails, peaking near 425, with a long right tail; dashed lines at 591 and 715 pails and a solid line at 759 pails. ||

TABLE Reorder points by method. || Repeated runs put the Monte Carlo 95th percentile between 755 and 760 pails; 759 is the base run.
| Method | Reorder point (pails) | Safety stock (pails) | Share of simulated cycles covered |
| Shortcut formula (quoted 30-day lead time, demand variability only) | 591 | 160 | 81.8% |
| Full textbook formula | 715 | 245 | 92.9% |
| Monte Carlo 95th percentile | 759 | 290 | 95.0% |

The shortcut misses badly for two reasons (Table 3). Its mean is wrong: 30 quoted days at 14.4 pails a day is 432 pails, while delays stretch the true average lead time to 32.6 days and mean lead-time demand to 470. It also ignores lead-time variability altogether, which in this case contributes more variance than demand does. The full formula gets both the mean and the variance right: a normal curve with the true simulated mean and standard deviation covers the same 92.9%. Its error is entirely about shape. A normal curve places too little probability in the long right tail; Monte Carlo reads the tail directly.

The extra 44 pails over the full formula cost $7,920 of inventory, or about $1,980 a year in holding cost. Against the shortcut, the gap is 168 pails and $30,240 of inventory: money many SMEs believe they are saving while running well below their stated service level.

### 4.2 How many iterations are enough

The 95th percentile settles quickly. Over 30 repeated runs, its standard deviation was about 24 pails at 500 iterations, 5 pails at 10,000 and 1.4 pails at 100,000. At 10,000 iterations the reorder point is precise to about ±10 pails, equivalent to roughly ±0.4 points of cycle service [@law]. Runs of 50,000 to 100,000 iterations take seconds in Python and remove any doubt.

## Validating the Answer with a Policy Simulation

Running the reorder rule itself confirms the Monte Carlo reorder point to within one point of cycle service and shows the last correction it needs: at 759 pails the rule delivers 94.1% cycle service, and at about 777 pails it delivers 95% (Figure 2).

The lead-time demand method treats each cycle on its own. Real inventory has overlapping orders: with an average lead time of 33 working days and an order about every 35, about 40% of orders are placed while another is still in transit, though only about 0.5% arrive out of sequence. The policy simulation captures this. It runs the (s, Q) rule day by day, with backorders, for 200 simulated years after a one-year warm-up. An order placed at the end of day t arrives at the start of day t + L + 1, so it faces exactly L days of demand, as in the lead-time demand model. Each reorder point is run 40 times with independent random streams, and the same customer and supplier behaviour is replayed at every reorder point, so differences between reorder points are not luck.

FIG fig2-service-vs-rop || Cycle service level and fill rate against reorder point, mean of 40 runs of 200 years per reorder point. Markers show the formula (715), the Monte Carlo 95th percentile (759) and the undershoot-corrected reorder point (777). || Two rising lines from 600 to 900 pails: fill rate from 95% to almost 100%, and cycle service from 80% to 98.5%, crossing the 95% target near 777 pails. ||

Two service measures tell different stories. Cycle service level is the share of replenishment cycles with no stockout at all; fill rate is the share of pails shipped from stock, counted in units rather than order lines [@chopra]. At a reorder point of 600 pails, only 80% of cycles avoid a stockout, yet 95% of pails still ship on time, because most stockouts are short and shallow. A distributor that promises customers 98% of pails on time needs a fill-rate target, not a cycle target; here that is reached near 700 pails.

The policy simulation also exposes undershoot. Inventory is checked once a day, and a single day's orders can carry inventory position well below the reorder point, by about 18 pails on average in this case. The replenishment order is therefore placed with less stock in hand than the reorder point assumes. The formula and the lead-time demand percentile both ignore this. At the formula's 715 pails, cycle service is 91.6%; at Monte Carlo's 759 pails, 94.1% (±0.2); adding the expected undershoot gives about 777 pails and 95% (94.9% at 775). The correction in Eq. (4) needs only the mean and standard deviation of daily demand.

### 5.1 The cost trade-off

Service targets are policy choices; the cost curve shows what each choice costs (Figure 3). Holding cost is $45 per pail-year on average on-hand inventory. The shortage cost assumes $60 per pail backordered, regardless of how long the backorder lasts, covering lost margin, expediting and customer goodwill. That figure is an assumption to replace with the distributor's own.

FIG fig3-cost-vs-rop || Annual holding, shortage and total cost against reorder point, mean of 40 runs of 200 years per reorder point. The shortage cost of $60 per pail is an assumption. || A falling dashed shortage-cost line, a rising holding-cost line and a shallow U-shaped total-cost line with its minimum near 700 pails and a second marker at 775 pails. ||

Total cost reaches its minimum of about $25,400 a year near 690 pails (between 675 and 700 across runs), which gives about 89% to 91% cycle service and a 98% fill rate. The curve is flat near the bottom: the Monte Carlo reorder point of 759 pails costs about $730 a year more, and the undershoot-corrected 777 pails for 95% cycle service about $1,100 more. The premium is worth weighing because the $60 shortage cost is the least certain number in the model. If a stockout costs a key account, the true figure is far higher and the 95% target is inexpensive insurance. Monte Carlo turns a z-value into a price tag that management can weigh.

## Sensitivity: What Drives Safety Stock

Supplier disruption drives safety stock more than any other input in this case, order frequency comes second, and the variability of order sizes moves it least of the variability inputs tested (Figure 4).

Each input was set to a plausible low and high value with all other inputs at base case, and the safety stock (95th percentile of lead-time demand minus its mean) was recomputed over 20 independent runs of 60,000 cycles each. The base-case safety stock is 287 pails, with run-to-run noise of about 1 pail. Safety stock is the right measure here: inputs that change average demand, such as the normal lead time, also move the reorder point through its mean, but that is cycle stock, not protection.

FIG fig4-ss-sensitivity || Safety stock for 95% of cycles with one input at its low or high value and all others at base case; mean of 20 runs of 60,000 cycles per case. || Tornado chart with five horizontal bars around a base case of 287 pails; disruption probability spans 199 to 321 and orders per day 247 to 327, the two widest. ||

Five findings matter for practice:

- **Supplier disruption is worth managing directly.** Taking the disruption probability from 15% to zero cuts safety stock by 88 pails and the reorder point by 126 pails, about $22,700 of inventory. A second supplier, a domestic buffer or a freight forwarder with better sailing reliability may cost less than the stock it removes.
- **The shape of the disruption tail matters.** Replacing the base disruption with rarer but longer delays (a 10% chance of 20 to 40 extra days) raises the Monte Carlo reorder point by about 100 pails, while the textbook formula barely moves. The disruption term should be fitted to actual late receipts rather than guessed.
- **Demand growth needs a reorder point review.** A 17% rise in order frequency adds 40 pails of safety stock and about 118 pails to the reorder point, most of it extra average demand. Reorder points set once a year fall behind growing items.
- **Lead-time spread matters less than lead-time disruption.** Doubling the normal lead-time standard deviation from 4 to 8 days adds 48 pails of safety stock; the occasional large delay adds more.
- **Streaky demand needs more protection.** The model assumes each day's demand is independent. In a test where busy and quiet periods persist, the formula covered only 91% of cycles and the Monte Carlo reorder point rose by up to 80 pails.

## Implementation Guide for SMEs

An SME can run this method on its A items with 12 to 24 months of ERP history and a spreadsheet; the policy simulation needs a short script. Table 4 lists the data required.

TABLE Data required.
| Data | Source | Minimum history |
| Sales order lines (date, item, quantity) | ERP or accounting system | 12 months, 24 if seasonal |
| Purchase orders (order date, promised date, receipt date) | ERP purchasing and receiving | 15 to 20 receipts per supplier |
| Landed unit cost and holding rate | Finance | Current |
| Cost of a stockout (lost margin, expediting) | Sales and finance estimate | Current |

### 7.1 Building it in a spreadsheet

Excel can run lead-time demand simulation without add-ins, with one iteration per row and 10,000 rows:

1. Compute the lognormal parameters of the normal lead time once. Excel's LOGNORM.INV takes the mean and standard deviation of ln(lead time), not of the lead time itself. For mean m = 30 days and standard deviation s = 4 days: σ = √ln(1 + (s/m)²) = 0.133 and μ = ln(m) − σ²/2 = 3.392.
2. Draw the lead time: =MAX(1, ROUND(LOGNORM.INV(RAND(), 3.392, 0.133) + IF(RAND()&lt;0.15, 10+15*RAND(), 0), 0)).
3. Approximate lead-time demand: draw the number of orders over the lead time with a Poisson inverse built from a lookup table, or sample whole historical days with INDEX and RANDBETWEEN, then sum.
4. Read the reorder point with =PERCENTILE.INC(LTD_column, 0.95), then add the undershoot from the daily demand history: =(VAR.P(daily)+AVERAGE(daily)^2)/(2*AVERAGE(daily)).
5. Freeze results with Copy and Paste Values before reviewing, because RAND recalculates on every edit.

Sampling whole historical days (bootstrapping) is often the best choice for an SME: it needs no distribution fitting and keeps real zero-demand days and real large orders. If demand runs in streaks, blocks of consecutive weeks should be sampled instead of single days.

### 7.2 Pitfalls

- **Using promised lead time instead of actual.** Lead time should be measured from purchase order date to receipt date, not taken from the supplier's quote.
- **Mixing working and calendar days.** Demand and lead time must use the same clock.
- **Fitting one distribution to everything.** Normal transit and disruption are best kept as separate terms, with the disruption tail fitted to actual late receipts.
- **Forgetting undershoot.** With lumpy daily demand, the term E[D²]/(2E[D]) belongs on top of the percentile, or the policy falls about a point short of target.
- **Using raw demand history for a trending item.** For growing or seasonal items, variability should be measured as forecast error, not spread around a fixed average [@eppen].
- **Treating the shortage cost as known.** The cost curve should be run at two or three shortage costs so that management sees the range.
- **Running it once.** Reorder points for A items need a quarterly refresh, and a fresh run after any change of supplier or freight lane.
- **Applying it to every SKU.** Monte Carlo suits A items and erratic B items. Steady C items, with low variability and demand on most days, are well served by the formula; slow or intermittent C items need a Poisson or negative binomial model, or bootstrapping [@sbc].

## Conclusions

For items with disruption-prone imports and lumpy demand, Monte Carlo simulation sets a reorder point that delivers the service level it promises, once undershoot is added. The textbook formula does not.

- In the resin case, the full formula's 95% target covered 92.9% of cycles and the common shortcut 82%. Monte Carlo set the reorder point at about 759 pails; adding the expected undershoot of about 18 pails gave 777, which delivered 95% cycle service across 40 independent 200-year runs.
- The formula's error is about shape, not variance: late shipments create a long right tail that a normal curve cannot represent.
- Cycle service and fill rate differ widely, 80% against 95% at the same reorder point. The service target should match what customers are promised.
- The cost curve is flat near its minimum, about 690 pails here, so the service target is a management choice with a visible price: about $1,100 a year for 95% cycle service on this item.
- Supplier disruption drives safety stock most, and the shape of the delay tail matters. Investment in supplier reliability, and in clean receipt data, can release more cash than any refinement of the formula.

The method needs no special software. A spreadsheet handles the reorder point; a short script handles validation. The case is a composite, and its numbers depend on the assumed disruption pattern and on independent daily demand; both should be checked against the distributor's own history. The scarce input is clean receipt data, and that is where an SME should start.

## Appendix: Python Code

The script below reproduces the method in about 70 lines and runs in a few seconds. With 20,000 iterations it gives a reorder point of 748 pails, lower than the paper's 759 because a smaller sample estimates the 95th percentile less precisely. Its policy check gives 94.1% cycle service at 748 pails, and 95.2% once the undershoot correction of about 18 pails is added. An order placed at the end of a day arrives L full days later, matching the lead-time demand model.

CODE appendix || Monte Carlo reorder point with undershoot correction and (s, Q) policy check (Python 3 with NumPy).
"""
