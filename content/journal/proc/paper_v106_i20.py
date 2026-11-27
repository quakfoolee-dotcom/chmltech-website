"""Chmltech Online Journal, Vol. 106, Issue 20: Setting Cost Contingency by Monte Carlo: P50, P80 and the Risks Behind Them for a C$100 Million Process Plant (Nov 27 2026).

Worked case: the C$100M, 50,000 t/y plant of the FEED series at Class 3, 12 correlated cost accounts, an eight-event
risk register and a separate escalation reserve, 50,000 iterations. Model: content/journal/proc/models/contingency/."""

SLUG = "setting-cost-contingency-by-monte-carlo-p50-p80-and-the-risks-behind-them-for-a-100-million-process-plant"
META = dict(
    volume=106, issue=20,
    title='Setting Cost Contingency by Monte Carlo: P50, P80 and the Risks Behind Them for a C$100 Million Process Plant',
    short_title='Setting Cost Contingency by Monte Carlo',
    meta='Monte Carlo contingency for a C$100M Class 3 process plant estimate: P50 C$110.7M, P80 C$116.4M, the risks behind them, and why flat 10% or 15% falls short.',
    keywords=['cost contingency', 'Monte Carlo simulation', 'P50 and P80', 'Class 3 estimate', 'risk register', 'estimate ranging', 'correlation', 'AACE'],
)
DIVISION = "Division of Clean Energy Technology Innovation"
ABSTRACT = "Most capital estimates for small and mid-sized process plants still carry a flat contingency of 10% or 15%, chosen by habit. This paper sets the contingency for the C$100 million, 50,000-tonne-a-year plant of the Chmltech FEED series by Monte Carlo simulation of its Class 3 estimate. Twelve cost accounts carry skewed estimating ranges around a most likely base, correlated through common drivers for materials, labour and engineering. Eight risk events, such as poor soil, a late reactor, a scale-up problem and a labour shortage, add cost and delay, with each week of delay priced at the time-dependent indirect burn rate. Escalation and exchange rate are carried in a separate reserve. Over 50,000 iterations the P50 cost at base-date prices is C$110.7 million and the P80 C$116.4 million, contingencies of 11% and 16% of the base. A flat 10% has about a 54% chance of being overrun and a flat 15% a 26% chance. About two-thirds of the P80 contingency is cost the estimate already expects: C$5.2 million from the upward skew of the ranges and C$5.9 million from the expected cost of the risk events. Field labour and major equipment are the largest estimating uncertainties; eliminating the scale-up or soil risk would cut the P80 most. Treating line items as independent understates the P80 contingency by 8%, and by 14% with ranges twice as wide. Even so, the model's spread is narrower than AACE's indicative ranges. The Python model and a live Excel template accompany the paper."

REFS = {
    'aace08': ('AACE International. (2008). <em>Contingency estimating — General principles</em> (Recommended Practice 40R-08). AACE International.',
        ''),
    'aace11': ('AACE International. (2011). <em>Risk analysis and contingency determination using parametric estimating</em> (Recommended Practice 42R-08). AACE International.',
        ''),
    'aace19': ('AACE International. (2019). <em>Integrated cost and schedule risk analysis using risk drivers and Monte Carlo simulation of a CPM model</em> (Recommended Practice 57R-09, rev.). AACE International.',
        ''),
    'aace20': ('AACE International. (2020). <em>Cost estimate classification system — As applied in engineering, procurement, and construction for the process industries</em> (Recommended Practice 18R-97, rev.). AACE International.',
        ''),
    'aace21': ('AACE International. (2021). <em>Risk analysis and contingency determination using expected value</em> (Recommended Practice 44R-08, rev.). AACE International.',
        ''),
    'aace22b': ('AACE International. (2022). <em>Cost risk analysis and contingency determination using estimate ranging for inherent risks with Monte Carlo simulation</em> (Recommended Practice 118R-21). AACE International.',
        ''),
    'aace23': ('AACE International. (2023). <em>Integrated cost and schedule risk analysis and contingency determination using estimate ranging and expected value with Monte Carlo simulation</em> (Recommended Practice 123R-22). AACE International.',
        ''),
    'burroughs': ('Burroughs, S. E., &amp; Juntima, G. (2004). Exploring techniques for contingency setting. <em>AACE International Transactions</em>, EST.03.',
        ''),
    'flyvbjerg': ('Flyvbjerg, B. (2014). What you should know about megaprojects and why: An overview. <em>Project Management Journal, 45</em>(2), 6–19.',
        'https://doi.org/10.1002/pmj.21409'),
    'hollmann': ("Hollmann, J. K. (2016). <em>Project risk quantification: A practitioner's guide to realistic cost and schedule risk management</em>. Probabilistic Publishing.",
        ''),
    'iman': ('Iman, R. L., &amp; Conover, W. J. (1982). A distribution-free approach to inducing rank correlation among input variables. <em>Communications in Statistics — Simulation and Computation, 11</em>(3), 311–334.',
        'https://doi.org/10.1080/03610918208812265'),
    'capex': ('Lee, Q. F. (2026). Engineering CAPEX and OPEX estimation for process plants: Methods, accuracy and trade-offs. <em>Chmltech Online Journal, 104</em>(4).',
        'https://www.chmltech.com/post/engineering-capex-and-opex-estimation-for-process-plants.html'),
    'feedpkg': ('Lee, Q. F. (2026). What a FEED package contains, and what each document decides. <em>Chmltech Insights</em>.',
        'https://www.chmltech.com/post/what-a-feed-package-contains-and-what-each-document-decides.html'),
    'stages': ('Lee, Q. F. (2026). From concept to construction: The five stages of a process plant project. <em>Chmltech Insights</em>.',
        'https://www.chmltech.com/post/from-concept-to-construction-five-stages-of-a-process-plant-project.html'),
    'scaleup': ('Lee, Q. F. (2026). Lab to pilot to commercial: What changes when you scale up. <em>Chmltech Insights</em>.',
        'https://www.chmltech.com/post/scale-up-what-changes-from-lab-to-pilot-to-commercial.html'),
    'commissioning': ('Lee, Q. F. (2026). From mechanical completion to handover: The commissioning sequence. <em>Chmltech Insights</em>.',
        'https://www.chmltech.com/post/from-mechanical-completion-to-handover-the-commissioning-sequence.html'),
    'merrow11': ('Merrow, E. W. (2011). <em>Industrial megaprojects: Concepts, strategies, and practices for success</em>. Wiley.',
        ''),
    'merrow81': ('Merrow, E. W., Phillips, K. E., &amp; Myers, C. W. (1981). <em>Understanding cost growth and performance shortfalls in pioneer process plants</em> (R-2569-DOE). RAND Corporation.',
        'https://www.rand.org/pubs/reports/R2569.html'),
    'gao': ('US Government Accountability Office. (2020). <em>Cost estimating and assessment guide: Best practices for developing and managing program costs</em> (GAO-20-195G).',
        'https://www.gao.gov/products/gao-20-195g'),
    'vose': ('Vose, D. (2008). <em>Risk analysis: A quantitative guide</em> (3rd ed.). Wiley.',
        ''),
}

CODE = {"appendix": open(__file__.replace("paper_v106_i20.py", "models/contingency/contingency_appendix.py"), encoding="utf-8").read().rstrip()}

DOWNLOADS = [  # served from assets/journal/code/
    dict(file='contingency_appendix.py', label='Appendix script', note='P50, P80 and P90, chance of overrunning a flat 10% or 15%, escalation reserve (Python 3, NumPy, SciPy)'),
    dict(file='chmltech-cost-contingency-model.zip', label='Full model', note='Correlated cost accounts, risk register, escalation reserve, drivers, correlation, range-width and estimate-class cases, results, README'),
    dict(file='chmltech-cost-contingency-template.xlsx', label='Excel template', note='Live simulation of the estimate, risk register and escalation reserve with 5,000 iterations, S-curve percentiles, the paper results (about 7.5 MB)'),
]

BODY = r"""
## Introduction

Every capital estimate is a forecast of a cost that will not be known until the plant is built. Contingency is the amount added to the base estimate for the cost the estimator expects but cannot yet place in a line item: growth in quantities, productivity worse than assumed, prices that move, and events that may or may not happen [@aace08]. It is not a reserve for changes in scope, and it is expected to be spent.

On large projects, contingency is usually set by risk analysis. On the small and mid-sized process plants where Chmltech works, it is still often a flat percentage, 10% or 15% of the base [@burroughs]. A flat percentage says nothing about how likely the budget is to be enough, and the evidence on process plant cost growth is not reassuring: pioneer plants and projects with poor definition overrun their estimates far more often than their contingency allows [@merrow81, @merrow11].

The earlier Chmltech paper on capital and operating cost estimation set out the estimate classes and described Monte Carlo analysis in general terms [@capex]. This paper applies it to one estimate: the C$100 million, 50,000-tonne-a-year plant of the FEED series [@feedpkg, @stages], at the end of FEED. It asks how much contingency the estimate needs for a 50% and an 80% chance of not being overrun, where that contingency comes from, which risks drive it, and how much the answer depends on modelling choices that are often skipped, such as correlation between line items.

## The Estimate and Its Uncertainty

The base estimate is the fixed capital of the plant at the end of FEED, a Class 3 estimate in the AACE classification [@aace20]. It totals C$100.0 million before contingency, at base-date prices, and every account is set at its most likely value, so that the base carries no hidden allowance or deliberate optimism. Table 1 lists its 12 accounts with the range assigned to each. Escalation to the middle of spending, about 18 months away, and the exchange rate on imported equipment are treated separately, as AACE terminology expects: contingency covers the uncertainty in the defined scope at base-date prices, and escalation is a reserve of its own [@aace08].

TABLE Cost accounts of the base estimate and their ranges at Class 3.
| Account | Base (C$M) | Range as a multiple of base (low, most likely, high) | Correlation group |
| Major equipment | 24.0 | 0.92, 1.00, 1.15 | Materials |
| Piping (bulk materials) | 9.0 | 0.88, 1.00, 1.27 | Materials |
| Instruments and controls | 5.0 | 0.90, 1.00, 1.25 | Materials |
| Electrical | 5.0 | 0.90, 1.00, 1.25 | Materials |
| Civil, structural and buildings | 8.0 | 0.90, 1.00, 1.35 | Site |
| Insulation, painting, fireproofing | 2.0 | 0.90, 1.00, 1.30 | Materials |
| Direct field labour | 17.0 | 0.86, 1.00, 1.33 | Labour |
| Construction indirects | 8.0 | 0.90, 1.00, 1.30 | Labour |
| Engineering, procurement and construction management | 13.0 | 0.95, 1.00, 1.20 | Engineering |
| Owner's costs | 4.0 | 0.95, 1.00, 1.25 | Engineering |
| Start-up and commissioning | 3.0 | 0.90, 1.00, 1.40 | Labour |
| Freight and duties | 2.0 | 0.90, 1.00, 1.20 | Materials |
| Total | 100.0 |  |  |

The ranges are skewed upward, as experience says they should be. Quantities of piping, cable and concrete grow as design develops; field labour productivity is more often worse than estimated than better; and most of the equipment has firm or budget quotes, so its range is the narrowest. Accounts in the same group move together: a busy market raises all material prices, poor productivity hits labour and the indirects that depend on time. The correlations are set on the normal scores used to draw the samples: 0.5 within the materials and engineering groups, 0.7 within labour, 0.3 between groups, which give rank correlations of about 0.48, 0.68 and 0.29. The site group has a single account.

For the escalation reserve, the escalation rate varies from 2% to 6% a year around the 3% most likely, which is also what the base assumes, applied over 1.5 years to the direct and contractor accounts; 40% of the major equipment is bought in US dollars, with an exchange rate range of ±12%.

The second kind of uncertainty is the risk event: something that may or may not happen and is not in the base at all. Table 2 lists the risk register. Each event has a probability, a cost if it happens and, for some, a delay. A delay costs C$0.2 million a week in time-dependent costs: construction indirects, construction management and the owner's team. Each event is defined to lie outside what the ranges cover, so the two do not count the same cost twice: the labour shortage is a shortage severe enough to need premium crews or a camp, beyond the productivity range of the labour accounts; the HAZOP or code change adds equipment, beyond the quantity growth in the piping and electrical ranges; and the vendor failure forces a new purchase order, beyond the price range of the equipment account.

TABLE Risk register.
| Risk event | Probability | Cost if it happens (C$M: low, most likely, high) | Delay if it happens (weeks: low, most likely, high) |
| Poor soil: piling needed | 25% | 1.5, 2.5, 5.0 | 2, 4, 8 |
| Reactor delivered late | 30% | none | 4, 8, 16 |
| Scale-up issue forces a process change | 20% | 2.0, 4.0, 8.0 | 4, 8, 12 |
| HAZOP or code change adds equipment | 40% | 0.5, 1.5, 3.0 | none |
| Permit delayed | 15% | none | 4, 10, 20 |
| Labour shortage: premium crews needed | 30% | 1.0, 2.5, 5.0 | none |
| Key vendor fails: re-procurement | 10% | 0.5, 1.5, 3.0 | 6, 10, 16 |
| Commissioning problems | 25% | 0.5, 1.5, 4.0 | 2, 6, 12 |

The register is typical of a small chemical plant with some new process technology. The scale-up issue reflects what the earlier post on scale-up warned about: a pilot that did not reproduce one feature of the full-scale plant [@scaleup]. The events are drawn independently, which is not conservative: in a hot market the labour shortage, the vendor failure and high escalation tend to come together. Section 6 tests what happens when they do.

## Method

The simulation combines two of AACE's recommended treatments: estimate ranging of the line items for the inherent uncertainty of a well-defined estimate, and an expected-value treatment of discrete risk events, run together in one Monte Carlo model so that their sum has a distribution [@aace22b, @aace21, @aace23]. AACE warns that estimate ranging on its own tends to understate contingency when systemic risks, such as new technology or weak definition, are significant, and refers them to parametric models [@aace22b, @aace11, @hollmann]. This paper does not model systemic risk parametrically; Sections 6 and 7 show what that omission is likely to cost.

**Total cost.** In each iteration the final cost at base-date prices is Eq. (1), where Bj is the base of account j and Xj its sampled multiple; Ik is 1 if risk event k happens and 0 if not, ck its cost, dk its delay in weeks and b the burn rate of C$0.2 million a week:

TEX C = \sum_{j} B_j X_j + \sum_{k} I_k \left( c_k + b\,d_k \right)

**Escalation reserve.** The escalation and exchange-rate effect beyond what the base carries is Eq. (2), applied to the first nine accounts, the direct and contractor costs, where e is the sampled escalation rate, e0 the 3% carried in the base, t the 1.5 years to the middle of spending, B1 the major equipment base, sUS its share bought in US dollars and xFX the change in exchange rate. One mid-spend factor is a simplification: engineering is spent earlier and firmly quoted equipment later, which would narrow the reserve slightly:

TEX E = \left( E_f - 1 \right) \sum_{j \le 9} B_j X_j + E_f\,B_1\,s_{US}\,x_{FX}, \qquad E_f = \left( \frac{1 + e}{1 + e_0} \right)^{t}

**Correlation.** The account multiples are drawn together through a Gaussian copula: a vector of correlated standard normal numbers is drawn with the correlation matrix Σ of Section 2, and each is turned into a multiple through the inverse of that account's triangular distribution, Eq. (3). The matrix is positive definite. In the Excel template the same correlations are built from common factors, z = √ρ_b Z₀ + √(ρ_g − ρ_b) Z_g + √(1 − ρ_g) ε, which requires each within-group correlation to be at least the between-group value. The approach is close in effect to the rank-correlation method of Iman and Conover [@iman, @vose]:

TEX X_j = F_j^{-1}\!\left( \Phi(z_j) \right), \qquad \mathbf{z} \sim N(\mathbf{0}, \boldsymbol{\Sigma})

**Risk events.** Each event happens with its probability, independently of the others and of the line items, and its cost and delay are drawn from their triangular ranges. The delays are added, not overlapped, which is conservative for events on different paths of the schedule and right for events on the same one; the independence of the events is not conservative, as Section 2 notes.

**Contingency.** The contingency for a confidence level p is the difference between the p-th percentile of the final cost and the base, Eq. (4):

TEX K_p = C_p - \sum_j B_j

The simulation runs 50,000 iterations; with five other random seeds the P80 stays within C$0.1 million. The same iterations are rerun with each account fixed at its mean or each risk removed or replaced by its expected value, to show how much of the P80 each one carries, and with the correlation removed, the ranges widened, the market-driven items correlated, and the ranges and risks scaled to earlier estimate classes.

**Verification.** With every range collapsed to its most likely value and the risks switched off, the model returns exactly the C$100.0 million base. The mean cost of the risk events in the simulation, C$5.88 million, matches the expected value calculated by hand from Table 2, C$5.87 million.

## Results: How Much Contingency

The estimate needs a contingency of C$10.7 million for an even chance of being enough, and C$16.4 million for an 80% chance, at base-date prices. Figure 1 shows the distribution of the final cost as an S-curve.

FIG fig1-s-curve || Distribution of the final fixed capital cost at base-date prices over 50,000 iterations, with the P50, P80 and P90 values and the chance of overrun for flat contingencies of 10% and 15%. || S-curve of final cost with P50, P80 and P90 ||

The base estimate alone has only a 3% chance of being enough. A flat 10% contingency, a budget of C$110 million, has about a 54% chance of being overrun, so it sits just below the P50; a flat 15% has a 26% chance, so it sits at about P74. The P90 is C$119.5 million, 19.5% above the base, and the P95 C$122.2 million. The distribution is skewed to the right: the P80 is C$5.7 million above the P50, while the P20 is C$5.2 million below it.

The escalation reserve comes on top. With escalation of 2% to 6% a year against the 3% carried in the base, and the exchange rate on imported equipment, it has a P50 of C$0.8 million and a P80 of C$2.1 million. Simulated together with the contingency, the total P80 is C$117.5 million; the two P80s do not simply add, because escalation and the cost uncertainties are unlikely to be at their worst together.

Figure 2 shows where the contingency comes from. The mean final cost is C$111.1 million. Of the C$11.1 million between the base and the mean, C$5.2 million comes from the upward skew of the line-item ranges: with the base at the most likely value of every account, each account still has a longer tail upward than downward, so its mean sits above its most likely value. The other C$5.9 million is the expected cost of the risk events, of which C$2.0 million is the cost of ten weeks of expected delay. The margin from the mean to the P80 adds C$5.4 million. In other words, about two-thirds of a P80 contingency is not a safety margin at all; it is cost the estimate already expects but has not placed in a line item.

FIG fig2-contingency-build-up || Build-up of the P80 budget from the base estimate at base-date prices: skew of the line-item ranges, expected cost of the risk events, and the margin from the mean to the P80; the escalation reserve is held separately. || Build-up of the P80 budget from the base estimate ||

Run separately, the line-item uncertainty alone gives a P80 of C$109.3 million and the risk events alone also C$109.3 million. Neither half is negligible, and their P80 contingencies do not simply add: together they need C$16.4 million, not the C$18.7 million of the sum, because the two are unlikely to be at their worst together.

## What Drives the Contingency

Figure 3 shows how much of the P80 each item carries, measured in the way that suits it. For an estimating account the question is what its spread costs, so the account is fixed at its mean and the fall in the P80 recorded. For a risk event there are two questions: what the event is worth if it can be eliminated, by a survey or a design decision, and how much of the P80 is due to its all-or-nothing nature, which shows when it is replaced by its expected value.

FIG fig3-drivers || Fall in the P80 cost: left, if each estimating account were fixed at its mean (eight largest); right, if each risk event were eliminated, or replaced by its expected value. || Fall in P80 by estimating account and by risk event ||

Among the estimating accounts, direct field labour carries the most, C$0.7 million of the P80, followed by major equipment at C$0.5 million and piping and construction indirects at about C$0.3 million each. Labour is the largest account with one of the widest ranges; equipment is large but already mostly quoted. A better productivity basis, from the contractor's own records on similar work, would narrow the largest of them.

Among the risk events, eliminating the scale-up problem would cut the P80 by C$1.7 million and eliminating the poor-soil risk by C$1.2 million; commissioning problems and the labour shortage are each worth about C$1.0 million. Each has a clear way to reduce it before the budget is fixed: a further pilot campaign or an independent technology review for the scale-up risk, a geotechnical survey for the soil, a commissioning plan with vendor support for start-up [@commissioning], and a labour plan with early contractor engagement for the labour market. Replacing each event by its expected value instead removes much less, C$0.4 million for the scale-up risk and C$0.2 million or less for the others: most of an event's weight in the P80 is its expected cost, which stays whether or not it is managed as a separate allowance.

These effects do not add up to the contingency. Fixing or removing one item leaves the others, and the effects of correlated items overlap. The figure ranks where to look, not how to divide the budget.

**Expected value is not enough for risks.** A common short-cut adds the expected values of the risk events, probability times impact, to the estimate. For this register that is C$5.9 million, which matches the mean in the simulation. But the risk events alone give a P80 C$9.3 million above the base, because a 20% chance of a C$5 million problem is either nothing or C$5 million, never C$1 million [@aace21]. An expected-value allowance is the right P50 contribution and too little for a P80 budget.

## Correlation and Range Width

A line-item model treats the estimate as many small uncertainties. If they are independent, they cancel: a high piping account is offset by a low electrical account, and the total ends up narrower than any of its parts. In a real project they are not independent. A hot construction market raises every material price at once; a contractor with poor productivity is poor on every discipline; slow engineering delays every package. Figure 4 shows what ignoring this does.

FIG fig4-correlation || P80 contingency with the line items independent and correlated through common drivers, for the Class 3 ranges and for ranges 1.5 and 2 times wider. || P80 contingency with independent and correlated line items ||

With the Class 3 ranges, treating the accounts as independent gives a P80 contingency of C$15.2 million instead of C$16.4 million, 8% too low. The understatement grows with the ranges: with ranges twice as wide it is C$3.5 million, or 14%. The P50 hardly changes, because correlation widens the distribution without moving its middle; it is the high percentiles a budget is set at that suffer.

The market can also tie the line items to the risk events and to escalation. Correlating escalation with the material and labour accounts, and the labour shortage with the labour accounts and escalation, at 0.5 each, leaves the P80 contingency almost unchanged at C$16.3 million and raises the total P80 including the escalation reserve from C$117.5 million to C$117.7 million. In this register the market-driven items are small next to the site and technology risks; in a register dominated by market risks the effect would be larger.

Correlation is one reason line-item models have a poor record; narrow ranges are the other. Research on completed projects finds that the ranges estimators assign to line items are too narrow, and that actual outcomes spread wider than the models predict, especially on projects with new technology or poor definition [@hollmann, @merrow11]; AACE now says the same of estimate ranging when systemic risks are significant [@aace22b]. Optimism in the base estimate itself adds to the problem [@flyvbjerg]. This model is no exception. Its P10 to P90 range around the P50, including the escalation reserve, is −7% to +8%, narrower than even the narrow end of the AACE Class 3 range of −10% to −20% and +10% to +30% (Table 3). Two defences help: correlate the line items through their common drivers, as here, and model the big uncertainties as explicit risk events rather than hiding them in wider line-item ranges, so that each can be discussed and reduced. For a plant with significant new technology, a parametric model of systemic risk should be added [@aace11].

## Estimate Class and First-of-a-Kind Technology

The same plant estimated earlier, with less definition, needs far more contingency. To show how much, the line-item ranges are widened two and three times and the risk probabilities raised by 30% and 60%, standing for a Class 4 estimate at the feasibility stage and a Class 5 estimate at concept. These scaling factors are the author's assumption, chosen to resemble the loss of definition between project stages [@stages], not values from a standard. AACE does not recommend estimate ranging at Class 4 or 5 or for new technology, so these cases illustrate the trend rather than give usable Class 4 and 5 contingencies [@aace22b]. Table 3 and Figure 5 give the results.

TABLE Final cost and contingency of the same plant at three estimate classes (C$ million at base-date prices, base C$100 million), and the spread around the P50, including the escalation reserve, against the AACE indicative ranges.
| Estimate class | P50 | P80 | P90 | P80 contingency | Model P10 / P50 and P90 / P50 | AACE indicative range (low, high) |
| Class 5 (concept) | 124.1 | 138.0 | 145.4 | 38% | −15% / +17% | −20% to −50%, +30% to +100% |
| Class 4 (feasibility) | 117.5 | 127.1 | 132.2 | 27% | −11% / +13% | −15% to −30%, +20% to +50% |
| Class 3 (end of FEED) | 110.7 | 116.4 | 119.5 | 16% | −7% / +8% | −10% to −20%, +10% to +30% |

FIG fig5-estimate-class || Distribution of the final cost of the same plant at Class 5, Class 4 and Class 3, with the P80 of each marked (the lower tail below C$90 million, 0.4% of Class 5 iterations, is not shown). || Cost distributions at estimate classes 3, 4 and 5 ||

The contingency grows from 16% at Class 3 to 27% at Class 4 and 38% at Class 5, but the model's spread at every class is narrower than the narrowest AACE range for that class. That supports the point of Section 6 rather than the model: line-item ranging understates the spread, and more so as definition falls. The point for an owner is the decision each stage supports. A Class 5 estimate with a P50 of C$124 million and a P80 of C$138 million can screen the project, not fund it; at Class 3, where the P50 to P80 gap has shrunk from C$14 million to C$6 million, it can [@aace20].

**First-of-a-kind technology.** For a plant built on a process not yet run at full scale, the scale-up risk is not a 20% event. Raising its probability to 50% and its cost and delay by half moves the P50 from C$110.7 million to C$114.3 million and the P80 from C$116.4 million to C$121.1 million, a P80 contingency of 21%. This matches the long-standing finding that cost growth in pioneer plants increases with the share of the plant that uses new technology [@merrow81], and it is probably still an understatement, for the parametric reasons above. For such a plant, the cheapest contingency reduction is usually a better pilot programme, not a better estimate.

## Decision Guide

The choice of confidence level is the owner's, not the estimator's. Table 4 sets out how the result should be used.

TABLE Using the contingency analysis.
| Decision | Use | Why |
| Project budget and contingency held by the project manager | P50 to P80 of the combined model, about C$111 to C$116 million here at base-date prices | Covers the expected growth and most of the risk events |
| Escalation | A separate escalation reserve, about C$2 million at P80 here | Escalation is a price effect, not a scope uncertainty, and is managed against indices |
| Funding approval by a board or lender | P80 or P90 of the total, with the S-curve shown | The question is the chance of needing more money |
| Low-probability, high-impact risks such as poor soil and a scale-up problem | Either keep them in the contingency, or move them to a management reserve held above the project; here that lowers the project P80 to about C$113.5 million | They are better managed as decisions than spent as contingency |
| Choosing between projects | P50, with the P80 to P50 gap as a measure of risk | Comparable across projects |
| A flat percentage required by policy | Report its confidence level from the S-curve | Here 10% is about P46 and 15% about P74 |
| First-of-a-kind technology | Model the scale-up risk explicitly, add a parametric check, and fund pilot work first | It is the largest single risk and the hardest to range |

Five steps produce a contingency an owner can defend.

1. **Range only what matters.** Put ranges on the dozen accounts that make up the estimate, skewed as experience says, not on hundreds of line items.
2. **Correlate through drivers.** Group accounts by the market, productivity and engineering drivers they share.
3. **Write a risk register with numbers.** Probabilities, cost and delay ranges, and a burn rate for delay.
4. **Simulate and read the S-curve.** Report the P50, P80 and P90 and the chance of overrunning any proposed budget [@gao].
5. **Act on the drivers, then rerun.** A survey, a pilot or a labour plan that removes a top risk reduces the contingency more than any argument about percentages.

### 8.1 Pitfalls

- **A flat percentage.** It hides a confidence level that can easily fall below 50% for a 10% allowance, as it does here.
- **Independent line items.** They understate the high percentiles, more so as ranges widen.
- **Expected values for risks.** They give the right mean but too little for a P80 budget.
- **Symmetric ranges, or a base set below the most likely values.** Most estimating errors are skewed upward; a symmetric range or an optimistic base puts the P50 too low.
- **Escalation and scope changes inside contingency.** Contingency covers the defined scope at base-date prices; escalation needs its own reserve, and a change in what is built needs its own approval and money.

## Conclusions

Contingency should be set from a probability distribution of the final cost, not from habit. For the Class 3 estimate of a C$100 million, 50,000-tonne-a-year chemical plant:

- At base-date prices the P50 is C$110.7 million and the P80 C$116.4 million: contingencies of 11% and 16% of the base, plus an escalation reserve of about C$2 million at P80. A flat 10% has about a 54% chance of being overrun; a flat 15% a 26% chance.
- About two-thirds of the P80 contingency is cost the estimate already expects: C$5.2 million from the upward skew of the line-item ranges and C$5.9 million from the expected cost of the risk events.
- Field labour productivity and major equipment are the largest estimating uncertainties. Eliminating the scale-up risk would cut the P80 by C$1.7 million and the soil risk by C$1.2 million, both through actions available before the budget is fixed.
- Treating line items as independent understates the P80 contingency by 8% here and by 14% with ranges twice as wide; an expected-value allowance for risks gives the right mean but too little for a P80.
- The same plant needs P80 contingencies of 27% at Class 4 and 38% at Class 5, and 21% at Class 3 if its process is first of a kind; even so, the model's spread is narrower than AACE's indicative ranges at every class.

The case has limits. The ranges and the risk register are illustrative, not drawn from this plant's own history, and line-item models tend to understate the spread of real outcomes; systemic risks are not modelled parametrically. The schedule is represented only by the delays of the risk events, priced at a fixed burn rate, not by an integrated cost and schedule risk analysis [@aace19]. Escalation uses a single mid-spend factor, risk-event costs are not escalated, the exchange-rate effect is applied to the base cost of imported equipment, and the exchange rate range of ±12% is a judgement that decides how little the exchange rate matters here. The plant's lost revenue during a delay is outside the capital cost. The method transfers to any estimate: the Python model and an Excel template that runs the simulation live can be downloaded from this paper's page.

## Appendix: Setting Contingency for Your Own Estimate

Table 5 sets out the method in steps, with what this paper did and where the downloadable model does it. The script below reproduces the P50, P80 and P90 of Section 4 at base-date prices, the chance of overrunning flat contingencies of 10% and 15% to within sampling error, and the escalation reserve. The full model adds the drivers, the correlation, range-width and market cases and the estimate classes; the Excel template runs the same simulation live with 5,000 iterations.

TABLE Steps of the method, with this paper's choices and the model function that does each.
| Step | What to do | In this paper | In the model |
| 1. Structure the estimate | A dozen accounts at their most likely values, at base-date prices | Table 1 | ACCOUNTS |
| 2. Range and correlate | Skewed triangular ranges; correlation by driver group | Table 1, Eq. (3) | ACCOUNTS, RHO, corr_matrix() |
| 3. Write the risk register | Probability, cost and delay ranges, burn rate; events outside the ranges | Table 2 | RISKS, BURN |
| 4. Simulate | 50,000 iterations of Eq. (1) | Figures 1 and 2 | simulate() |
| 5. Set the escalation reserve | Escalation and exchange-rate ranges against what the base carries | Eq. (2) | ESC, FX |
| 6. Find the drivers and test the model | Fix accounts at mean; remove risks or set them at expected value; remove correlation; widen ranges; correlate market items; earlier classes | Figures 3 to 5, Table 3 | swing_accounts(), main block |

CODE appendix || P50, P80 and P90 of the final cost at base-date prices, the chance of overrunning flat contingencies of 10% and 15%, and the escalation reserve (Python 3 with NumPy and SciPy).
"""
