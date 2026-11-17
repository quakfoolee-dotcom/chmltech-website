"""Chmltech Online Journal, Vol. 106, Issue 7: Forecasting Lumpy Demand: Does Croston Beat a Moving Average? (Nov 17 2026).

Simulated item populations (five x 1,000 items, weekly demand, SBC classes). Model: content/journal/ops/models/forecast/
(weekly order-up-to policy, six methods plus long-history benchmarks, level-shift and obsolescence scenarios).
Red-team checked (model audit and references) before publication; the bootstrap finding was reframed after the red team's benchmark test."""

SLUG = "forecasting-lumpy-demand-does-croston-beat-a-moving-average"
META = dict(
    volume=106, issue=7,
    title='Forecasting Lumpy Demand: Does Croston Beat a Moving Average?',
    short_title='Forecasting Lumpy Demand: Croston vs Moving Average',
    meta='Six forecasting methods for slow-moving items, scored on the stock needed for 95% fill: Croston saves 6%, a year of history saves 14%.',
    keywords=['intermittent demand', "Croston's method", 'TSB', 'bootstrapping', 'safety stock', 'fill rate', 'inventory obsolescence', 'demand forecasting'],
)
ABSTRACT = "Most SME inventories are full of items that sell only some weeks, yet many ERP systems forecast them with a moving average. This paper compares six methods on 5,000 simulated items: a 13-week moving average, simple exponential smoothing (SES), Croston's method, its bias-corrected version (SBA), the TSB method and a simple bootstrap. Each method sets the order-up-to level of a weekly-review policy and is scored on the stock it needs to fill 95% of demand from the shelf, not on forecast error. Croston, SBA and TSB need 5% to 6% less stock than the moving average; SES saves under 2%. The bootstrap needs 14% less, but because it uses a long history, not because it handles skewed demand: a normal formula using the last 52 weeks saves as much, and a 26-week bootstrap saves nothing. How demand variability is estimated matters more than the forecast, though these gains are an upper bound for stable demand. Accuracy measures point the wrong way: on intermittent and lumpy items a zero forecast scores best on mean absolute error, and percentage errors cannot be computed. When an item stops selling, every method leaves about three months of former demand on the shelf; the moving average, SES and TSB with a fast probability update lower the reorder level within 25 to 30 weeks, while Croston and SBA never do and keep placing small orders. SMEs should estimate variability from a year of history and pair any method with a no-sale alert."

REFS = {
    'croston': ('Croston, J. D. (1972). Forecasting and stock control for intermittent demands. <em>Operational Research Quarterly</em>, 23(3), 289–303.',
        'https://doi.org/10.1057/jors.1972.50'),
    'hk': ('Hyndman, R. J., &amp; Koehler, A. B. (2006). Another look at measures of forecast accuracy. <em>International Journal of Forecasting</em>, 22(4), 679–688.',
        'https://doi.org/10.1016/j.ijforecast.2006.03.001'),
    'kour': ('Kourentzes, N. (2014). On intermittent demand model optimisation and selection. <em>International Journal of Production Economics</em>, 156, 180–190.',
        'https://doi.org/10.1016/j.ijpe.2014.06.007'),
    'abc': ('Lee, Q. F. (2026). ABC inventory analysis: How to, with a worked example. <em>Chmltech Insights</em>.',
        'https://www.chmltech.com/post/abc-inventory-analysis.html'),
    'ss': ('Lee, Q. F. (2026). Beyond the formula: Setting safety stock with Monte Carlo simulation. <em>Chmltech Online Journal</em>, 106(3).',
        'https://www.chmltech.com/post/beyond-the-formula-setting-safety-stock-with-monte-carlo-simulation.html'),
    'sb01': ('Syntetos, A. A., &amp; Boylan, J. E. (2001). On the bias of intermittent demand estimates. <em>International Journal of Production Economics</em>, 71(1–3), 457–466.',
        'https://doi.org/10.1016/S0925-5273(00)00143-2'),
    'sb05': ('Syntetos, A. A., &amp; Boylan, J. E. (2005). The accuracy of intermittent demand estimates. <em>International Journal of Forecasting</em>, 21(2), 303–314.',
        'https://doi.org/10.1016/j.ijforecast.2004.10.001'),
    'sb06': ('Syntetos, A. A., &amp; Boylan, J. E. (2006). On the stock control performance of intermittent demand estimators. <em>International Journal of Production Economics</em>, 103(1), 36–47.',
        'https://doi.org/10.1016/j.ijpe.2005.04.004'),
    'sbg': ('Syntetos, A. A., Babai, M. Z., &amp; Gardner, E. S. (2015). Forecasting intermittent inventory demands: Simple parametric methods vs. bootstrapping. <em>Journal of Business Research</em>, 68(8), 1746–1752.',
        'https://doi.org/10.1016/j.jbusres.2015.03.034'),
    'sbc': ('Syntetos, A. A., Boylan, J. E., &amp; Croston, J. D. (2005). On the categorization of demand patterns. <em>Journal of the Operational Research Society</em>, 56(5), 495–503.',
        'https://doi.org/10.1057/palgrave.jors.2601841'),
    'td': ('Teunter, R. H., &amp; Duncan, L. (2009). Forecasting intermittent demand: A comparative study. <em>Journal of the Operational Research Society</em>, 60(3), 321–329.',
        'https://doi.org/10.1057/palgrave.jors.2602569'),
    'tsb': ('Teunter, R. H., Syntetos, A. A., &amp; Babai, M. Z. (2011). Intermittent demand: Linking forecasting to inventory obsolescence. <em>European Journal of Operational Research</em>, 214(3), 606–615.',
        'https://doi.org/10.1016/j.ejor.2011.05.018'),
    'wss': ('Willemain, T. R., Smart, C. N., &amp; Schwarz, H. F. (2004). A new approach to forecasting intermittent demand for service parts inventories. <em>International Journal of Forecasting</em>, 20(3), 375–387.',
        'https://doi.org/10.1016/S0169-2070(03)00013-X'),
}

CODE = {"appendix": open(__file__.replace("paper_v106_i7.py", "models/forecast/croston_appendix.py"), encoding="utf-8").read().rstrip()}

DOWNLOADS = [  # served from assets/journal/code/ (V5.42)
    dict(file='croston_appendix.py', label='Appendix script', note='Six methods on one population of 1,000 items (Python 3, NumPy)'),
    dict(file='chmltech-intermittent-demand-model.zip', label='Full model', note='Five populations, long-history benchmarks, obsolescence and accuracy tests, README'),
]

BODY = r"""
## Introduction

In a typical SME inventory, most items do not sell every week, and the forecasting method in the ERP was designed for items that do. Spare parts, specialty chemicals, fittings, packaging and slow-moving finished goods sell in occasional orders separated by weeks of nothing. Many planning tools forecast them with a moving average or simple exponential smoothing, then add safety stock from a normal-distribution formula. The Chmltech safety stock paper showed how that formula misleads when demand is lumpy [@ss]; this paper looks one step earlier, at the forecast itself.

Croston proposed forecasting intermittent demand in two parts: the size of an order when one comes, and the interval between orders [@croston]. Later work corrected a bias in Croston's method [@sb01, @sb05], added a version that can follow an item into obsolescence [@tsb], and proposed bootstrapping from past demand instead of fitting a forecast at all [@wss]. Comparative studies have found that which method wins depends on how methods are scored [@td, @sbg].

This paper asks the question an SME owner would ask: for the same service to customers, which method needs the least stock? It answers with a simulation of 5,000 items run through a weekly-review inventory policy, and checks how the answer changes when demand shifts or an item stops selling.

## The Six Methods

The methods differ in what they update and when: averaging methods update every week, Croston-type methods update only when a sale happens, and bootstrapping skips the forecast and samples history directly (Table 1).

TABLE The six forecasting methods.
| Method | What it does | Updates | Availability (author's experience) |
| Moving average (13 weeks) | Average of the last quarter's weekly demand | Every week | Very common |
| Simple exponential smoothing (SES) | Weighted average, recent weeks weighted more (α = 0.1) | Every week | Common |
| Croston | Smooths order size and interval between orders separately; forecast = size ÷ interval | Only in weeks with demand | Some ERP and planning add-ons |
| SBA | Croston's forecast × (1 − α/2) to remove its upward bias | Only in weeks with demand | Rare |
| TSB | Smooths order size and the probability of a sale each week; forecast = probability × size | Size in weeks with demand; probability every week | Rare |
| Bootstrapping | Resamples past weeks to build the demand distribution over the lead time | Monthly, from full history | Rare; easy in a spreadsheet |

Croston's method keeps two smoothed estimates: ẑ, the average size of a non-zero order, and p̂, the average number of weeks between orders. Both are updated only in a week with demand, and the forecast of demand per week is given by Eq. (1):

TEX \hat{d}_t = \frac{\hat{z}_t}{\hat{p}_t}, \qquad \hat{z}_t = \hat{z}_{t-1} + \alpha\,(d_t - \hat{z}_{t-1}), \qquad \hat{p}_t = \hat{p}_{t-1} + \alpha\,(q_t - \hat{p}_{t-1}) \quad \text{if } d_t > 0

Here dₜ is demand in week t, qₜ is the number of weeks since the previous demand, and α is the smoothing constant. Croston's forecast is biased upward [@sb01]; SBA multiplies it by (1 − α/2) to correct this [@sb05]. Because Croston and SBA update only when a sale happens, their forecasts never fall while an item is not selling. TSB fixes this by smoothing the probability of a sale every week, so the forecast drifts down through a run of zeros [@tsb].

All five forecasting methods feed the same reorder rule: the order-up-to level equals forecast demand over the lead time plus review period, plus a safety factor times the smoothed forecast error, scaled to that period. The bootstrap instead resamples single past weeks of demand to build the distribution of demand over the same period, and sets the order-up-to level at a chosen percentile of it. This is a simplified version of the method of Willemain, Smart and Schwarz, which also models runs of demand [@wss]. To separate the effect of the forecast from that of the history used, two further benchmarks are run: the bootstrap limited to the last 52 or 26 weeks, and a normal formula fed with the mean and variance of weekly demand over the last 52 weeks or the full history.

## Simulation Method

Every method is scored on the same 5,000 items, the same demand and the same inventory policy, so the only difference is the forecast.

**Items.** Five populations of 1,000 items each. For each item, demand occurs in a week with a fixed probability, from every week to one week in four on average, and order sizes follow a lognormal distribution with a mean of 2 to 60 units and a coefficient of variation of 0.2 to 1.3. Each item has 156 weeks of demand: 52 weeks of history, then 104 weeks scored.

**Demand classes.** Items are classified from their first year of history by the Syntetos–Boylan–Croston scheme, using the average interval between demands (ADI) and the squared coefficient of variation of order sizes (CV²), with cut-offs of 1.32 and 0.49 [@sbc]: smooth (frequent, steady sizes), erratic (frequent, variable sizes), intermittent (infrequent, steady sizes) and lumpy (infrequent, variable sizes). The populations average 12% smooth, 10% erratic, 46% intermittent and 32% lumpy items, a mix weighted toward slow movers.

**Inventory policy.** Stock is reviewed weekly and replenished to an order-up-to level, with a four-week lead time; unfilled demand is backordered. The fill rate is the share of units shipped from stock in the week they are demanded. Stock is measured as weeks of supply: average end-of-week units on hand divided by average weekly demand, both pooled over all items.

**Scoring.** For each method, the safety factor (or, for the bootstrap, the percentile) is varied to trace a curve of fill rate against stock, with one value for all items. Methods are compared at the stock each needs to reach 90% and 95% fill, interpolated between points. Percentage changes compare pooled weeks of stock; the ± values are 95% t intervals of the change across the five populations.

**Two further scenarios** test robustness: a level shift, in which every item's frequency of demand rises by half (capped at a sale every week) or falls by half at a random week, with order sizes unchanged, and obsolescence, in which 20% of items stop selling at a random week.

## Results: Stock Needed for 95% Fill

Croston-type methods need about 6% less stock than a moving average for the same 95% fill rate, and the bootstrap needs 14% less (Figure 1), though most of the bootstrap's gain comes from the length of history it uses, not from the method.

FIG fig1-stock-at-95 || Weeks of stock each method needs for a 95% fill rate across all 5,000 items, with the change against the 13-week moving average (dashed line); the hatched bar is the 52-week normal-formula benchmark of Table 3. || Horizontal bars of weeks of stock: moving average 8.13, SES 7.98, SBA 7.72, TSB 7.64, Croston 7.63, bootstrap on the full history 7.01 and the 52-week normal formula 6.95, a saving of 14.4%. ||

Across all 5,000 items, the 13-week moving average needs 8.1 weeks of stock to fill 95% of demand from the shelf. SES needs 8.0 weeks, 1.8% less (±0.1 points). Croston needs 7.6 weeks (6.1% less, ±0.4), TSB 7.6 (5.9% less, ±0.4) and SBA 7.7 (5.0% less, ±0.3). Croston and TSB differ by only 0.01 weeks, which is no practical difference. The bootstrap needs 7.0 weeks, 13.7% less (±1.9). At 90% fill the order is the same and the savings slightly larger: 2.7% for SES, 7.6% for Croston, 6.6% for SBA, 7.5% for TSB and 15.3% for the bootstrap. For an SME holding C$500,000 of slow-moving stock with similar unit costs across items, 6% is C$30,000 of cash, with no loss of service.

The broad order, with the bootstrap below the Croston-type methods and those below SES and the moving average, holds in every demand class (Table 2); what changes is the size of the gap.

TABLE Weeks of stock needed for 95% fill, by demand class.
| Demand class (share of items) | Moving average | SES | Croston | SBA | TSB | Bootstrapping |
| Smooth (12%) | 3.1 | 3.0 | 3.0 | 3.0 | 3.0 | 2.6 |
| Erratic (10%) | 7.6 | 7.4 | 7.3 | 7.4 | 7.3 | 6.2 |
| Intermittent (46%) | 7.7 | 7.5 | 7.1 | 7.1 | 7.1 | 6.5 |
| Lumpy (32%) | 13.5 | 13.5 | 12.8 | 12.9 | 12.8 | 11.5 |

Table 2 gives the weeks of stock each method needs for 95% fill, by demand class. Three points stand out:

- **Croston-type methods beat SES mainly on intermittent and lumpy items.** Against SES, Croston saves about 1% on smooth and erratic items but about 5% on intermittent and lumpy items. Against the moving average the gain is 3% to 8% in every class, because a 13-week average reacts to noise wherever it is used. TSB edges Croston on smooth items.
- **SBA's bias correction does not pay here.** SBA is Croston's forecast scaled by 0.95. Because each method's safety factor is tuned to reach 95% fill, a constant bias is largely absorbed: SBA simply needs a larger safety factor (2.54 against 2.43), and the trade-off between its lower forecast and its larger safety stock works out slightly worse across items. Measured on total units, SBA under-forecasts by about 3% and Croston over-forecasts by about 2%; on the average item the two biases are similar in size, so bias alone does not explain the gap.
- **The bootstrap's lead comes from its long history, not from the shape of the distribution.** The parametric methods estimate variability from a smoothed forecast error, which with α = 0.1 mostly reflects the last 20 weeks or so. The bootstrap reads the whole history, one to three years. Table 3 separates the two effects.

A normal formula fed with the mean and variance of the last 52 weeks, refreshed monthly, needs 14.4% less stock than the moving average, slightly more saving than the bootstrap on its full history (Table 3). Limiting the bootstrap to the last 52 weeks cuts its saving to 10.6%, and limiting it to 26 weeks removes it. The bootstrap's largest savings are also on erratic and smooth items (18% and 16%), not on lumpy items (15%), the opposite of what a skewness explanation would predict. This fits the finding that, on real demand data, the bootstrap did not beat simple parametric methods such as SBA [@sbg]: real demand is less stable than simulated demand, so a long history is less of an advantage.

TABLE Weeks of stock needed for 95% fill, by reorder-level rule and the history it uses.
| Reorder-level rule | History used | Weeks of stock, 95% fill | Change vs moving average | Change vs moving average, level-shift scenario |
| Moving average + smoothed error | 13 weeks; error about 20 | 8.1 | — | — |
| Croston + smoothed error | About 20 weeks | 7.6 | −6.1% | −5.0% |
| Bootstrap, full history | 52 to 155 weeks | 7.0 | −13.7% | −7.5% |
| Bootstrap, last 52 weeks | 52 weeks | 7.3 | −10.6% | −8.3% |
| Bootstrap, last 26 weeks | 26 weeks | 8.2 | +0.6% | +2.8% |
| Normal formula, last 52 weeks | 52 weeks | 7.0 | −14.4% | −13.0% |
| Normal formula, full history | 52 to 155 weeks | 6.6 | −18.6% | −13.1% |

Table 3 gives the stock each reorder-level rule needs for 95% fill, all items. The normal formulas set the order-up-to level at five times the window's mean weekly demand plus a safety factor times its standard deviation times √5, refreshed monthly; the full history grows from 52 to 155 weeks over the scored period. Demand here is independent from week to week, which flatters long windows.

Long histories carry a cost when demand changes. In the level-shift scenario, where each item's frequency of demand rose or fell by half partway through, the full-history bootstrap's saving fell from 13.7% to 7.5% (±1.0), and on intermittent items it lost its lead over Croston (7.2 weeks for both). The 52-week normal formula held up better, at 13.0% (±0.6), because its window forgets the old level within a year. Croston (5.0%) and TSB (4.5%) kept most of their advantage, while SBA's fell from 5.0% to 3.0%. The shift changes only how often items sell, not order sizes, so it is a mild test.

## Why Accuracy Scores Mislead

On intermittent and lumpy items, the forecast with the best mean absolute error is one that predicts zero every week, the one forecast that would leave the shelf empty (Table 4).

TABLE One-week-ahead forecast error on intermittent and lumpy items, scaled by each item's mean weekly demand.
| Forecast | Intermittent: MAE | Intermittent: RMSE | Lumpy: MAE | Lumpy: RMSE |
| Zero every week | 1.00 | 1.80 | 1.00 | 2.08 |
| Moving average | 1.17 | 1.54 | 1.23 | 1.89 |
| SES | 1.16 | 1.52 | 1.22 | 1.87 |
| Croston | 1.16 | 1.50 | 1.22 | 1.84 |
| SBA | 1.15 | 1.50 | 1.20 | 1.84 |
| TSB | 1.16 | 1.50 | 1.21 | 1.84 |

Errors are one-week-ahead, over the 104 scored weeks, divided by each item's mean weekly demand and averaged over items. Mean absolute error (MAE) rewards a forecast close to the median week, and when an item sells in fewer than about half of weeks, the median week is zero or close to it. Root mean squared error (RMSE) ranks the methods more sensibly, but its differences between methods are only 1% to 3%, while their stock needs differ by 5% to 7%. Percentage errors such as MAPE, the measure many ERP dashboards show, cannot be computed at all: 45% of the scored weeks have no demand, and a percentage of zero is undefined [@hk].

The practical rule follows from the inventory results: judge a forecasting method by the stock and service it delivers, measured as in Section 4, not by its error score [@sb06, @kour]. SBA illustrates the gap. It has the lowest MAE of the five forecasting methods, but MAE rewards under-forecasting; on RMSE it ties with Croston and TSB. It still needs more stock than either for the same fill rate.

## Obsolescence: When an Item Stops Selling

When an item stops selling, every method leaves about three months of its former demand on the shelf; what differs is whether the reorder level comes down and whether buying continues.

In the obsolescence scenario, 20% of items stopped selling at a random week during the scored period. Every method still replaces the last sale at the next review, so the stock left is roughly the order-up-to level at the last sale: 12.1 to 12.8 weeks of the item's former demand, with no meaningful difference between methods (±0.4 to ±0.6 weeks). TSB leaves slightly less than Croston because its probability of a sale starts falling straight after the last sale; the bootstrap leaves slightly less because it held less to begin with.

The methods differ in what they signal and buy afterwards (Table 5).

TABLE After the last sale: how fast each method lowers its reorder level, and how much it keeps buying.
| Method | Weeks after the last sale until the reorder level falls below a fifth of its old value | Orders placed after the last sale (300 items, 64 weeks) | Weeks of stock for 95% fill, stable demand |
| Moving average | 26 | 242 | 8.1 |
| SES | 29 | 206 | 8.0 |
| TSB, β = 0.05 | 41 | 264 | 7.6 |
| TSB, β = 0.10 | 29 | 223 | 7.7 |
| TSB, β = 0.20 | 24 | 207 | 7.8 |
| Normal formula, last 52 weeks | 52 | 339 | 7.0 |
| Bootstrap, full history | Never (more than 64) | 462 | 7.0 |
| Croston | Never (more than 64) | 5,517 | 7.6 |
| SBA | Never (more than 64) | 4,934 | 7.7 |

Medians over 300 items that stop selling at week 104, each method at the safety factor that gives 95% fill under stable demand; the test runs 64 weeks after the stop, and β is TSB's smoothing constant for the probability of a sale. Croston and SBA update only when a sale happens, so their forecast never falls. Their smoothed error also keeps growing through the zero weeks, because each week's error is the whole forecast, so the reorder level rises for 27% to 30% of items and they keep placing small orders long after the last sale. The bootstrap keeps sampling from a history that is mostly from the selling years, and a 52-week window takes a year to forget. TSB lowers its forecast every week without a sale [@tsb], but with β = 0.05 more slowly than the moving average; with β = 0.20 it matches the moving average's speed and still needs 4.3% less stock under stable demand.

Under a pure order-up-to policy, leftover stock is limited to about three months of former demand, but Croston and SBA keep adding to it, and any method adds to it when a minimum order quantity forces a large buy or a planner trusts the system's reorder level. The practical defence is the same whichever method is used: an alert that flags any item with no sale in a set number of weeks, say twice its usual interval between orders, for review before anything more is bought.

## Implementation Guide for SMEs

An SME can move its slow movers off the moving average in four steps, using two years of weekly sales from the ERP and a spreadsheet.

1. **Classify the items.** For each item, compute ADI (weeks in the period ÷ weeks with any demand) and CV² of the non-zero order sizes, then sort items into smooth, erratic, intermittent and lumpy with the 1.32 and 0.49 cut-offs. Combine with ABC value classes from the Chmltech ABC series [@abc], so effort goes to high-value lumpy items first.
2. **Set reorder levels from a year of history.** For items whose demand is roughly stable, set the order-up-to level from the mean and standard deviation of weekly demand over the last 52 weeks: 5 × mean + k × standard deviation × √5, for a four-week lead time plus one-week review, refreshed monthly. Tune k per class for the target fill rate. A bootstrap over the same window (sample 400 sets of five weeks, sum each set, take the percentile) needs no normal assumption but saved less here. Keep the window at about a year: 26 weeks lost the gain, and the full history responded slowly when demand shifted.
3. **Use Croston or TSB where demand is changing or ending.** For items with trends, new items and parts for products being phased out, a forecast that adapts is worth more than a long window. Both methods are a few spreadsheet columns: smoothed order size, smoothed interval (Croston) or probability of a sale (TSB), and their ratio or product, with α = 0.1. For items at risk of obsolescence, use TSB with a faster probability update (β around 0.2) and avoid Croston and SBA, which never bring the reorder level down.
4. **Check stock against service, not error scores.** Each quarter, compare the fill rate and weeks of stock achieved for each class against target. Retune the safety factor or percentile; ignore MAPE for these items.

### 7.1 Pitfalls

- **Weekly versus monthly buckets.** Monthly buckets hide intermittency and make every item look smooth. Classify on weekly or daily data.
- **Too short a window.** With 26 weeks of history the bootstrap lost its gain entirely, and new items have too little history for any window. Use a full year where possible, and Croston-type forecasts until the history builds up.
- **Stockouts in the history.** Weeks with zero sales because the shelf was empty are not weeks of zero demand. Flag and exclude them, or the forecast learns to expect less.
- **Assuming the safety factor carries across methods.** A safety factor tuned for the moving average gives a different fill rate with Croston. Retune it when the method changes.
- **Forgetting dead items.** No forecasting method removes stock that is already on the shelf. Pair the method with a no-sale alert (Section 6).

## Conclusions

For the slow-moving items that fill most SME inventories, replacing the moving average saves stock without hurting service, and how demand variability is estimated matters more than which forecast is used.

- At 95% fill, Croston and TSB needed about 6% less stock than a 13-week moving average, SBA 5% less and SES under 2% less; at 90% fill the savings were slightly larger.
- Estimating variability from a long history saved far more: a normal formula on the last 52 weeks needed 14% less stock, as did a bootstrap on the full history. The bootstrap's advantage came from its history length, not from modelling skewed demand; limited to 26 weeks, it saved nothing. These savings assume stable demand and are an upper bound.
- When demand frequency shifted, the 52-week formula kept a 13% saving, while the full-history bootstrap's fell to 7.5%.
- Forecast error scores misled: a zero forecast had the best mean absolute error on intermittent and lumpy items, percentage errors could not be computed, and the lowest-MAE method (SBA) did not need the least stock.
- When items stopped selling, every method left about three months of former demand on the shelf. The moving average, SES and TSB with β around 0.2 brought their reorder levels down within 25 to 30 weeks; Croston and SBA never did and kept placing small orders. A no-sale alert is needed whichever method is used.

The items are simulated, with demand that is independent from week to week and does not change unless a scenario says so. This favours long-history methods; real items that trend, have seasons or suffer stockouts that hide demand will show smaller gains. Fill rate and weeks of stock are pooled over all units with one safety factor per method, so high-volume items weigh most: at a pooled 95%, the median item reached about 96% fill and one item in ten fell below about 87%. Each method's safety factor was chosen with hindsight to hit the target exactly; in practice it must be tuned on past data. The bootstrap is a simple resample of single weeks, simplified from the method of Willemain, Smart and Schwarz [@wss]. An SME can run the same comparison on its own sales history with the code in the Appendix before switching methods; the full model, with the long-history benchmarks and scenario tests, can be downloaded from this paper's page.

## Appendix: Python Code

The script below runs one population of 1,000 items with all six methods and prints the weeks of stock each needs for 95% fill. It gives 8.05 weeks for the moving average, 7.87 for SES, 7.54 for Croston, 7.62 for SBA, 7.55 for TSB and 6.80 for bootstrapping: the same ranking, and savings of 2% to 16%, as the five-population results in Section 4. Its population is a separate random draw, not one of the five. The long-history benchmarks of Table 3 and the scenario tests are in the full model, which can be downloaded from this paper's page. It needs Python 3 and NumPy and runs in about a minute.

CODE appendix || One population of 1,000 simulated items: six methods scored on the weeks of stock needed for 95% fill (Python 3 with NumPy).
"""
