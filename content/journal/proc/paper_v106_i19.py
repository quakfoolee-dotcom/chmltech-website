"""Chmltech Online Journal, Vol. 106, Issue 19: Stocking Critical Spare Parts Under Uncertainty: When ABC Analysis and Safety Stock Formulas Fail (Nov 27 2026).

Worked case: 13 critical spares of the 50,000 t/y plant of Issues 8 and 9, (S-1, S) one-for-one stocking, discrete-event
simulation over 2,000 scenarios with uncertain Poisson failure rates, installed spares, buffers and partial capacity loss.
Model: content/journal/proc/models/spares/."""

SLUG = "stocking-critical-spare-parts-under-uncertainty-when-abc-analysis-and-safety-stock-formulas-fail"
META = dict(
    volume=106, issue=19,
    title='Stocking Critical Spare Parts Under Uncertainty: When ABC Analysis and Safety Stock Formulas Fail',
    short_title='Stocking Critical Spare Parts Under Uncertainty',
    meta='How many critical spares to hold? A simulation of 13 spares shows service-level and ABC rules miss the downtime-cost optimum by more than C$1M a year.',
    keywords=['critical spare parts', 'spare parts inventory', 'ABC analysis', 'safety stock', "Palm's theorem", 'Monte Carlo simulation', 'installed spare', 'maintenance planning'],
)
DIVISION = "Division of Operational Excellence"
ABSTRACT = "Critical spare parts break the usual inventory rules. A gearbox or a compressor motor fails once in decades, takes months to replace and stops the plant while it is missing. ABC analysis ranks such a part by its low annual usage, and a service-level rule never asks what a shortage costs. This paper sets the stock of 13 critical spares for a 50,000-tonne-a-year plant by minimising holding cost plus expected lost production. A discrete-event simulation of one-for-one replenishment, with uncertain Poisson failure rates over 2,000 scenarios, accounts for installed spare equipment, buffers and partial capacity loss. The cost optimum holds 13 parts worth C$336,000 and costs C$152,000 a year, with 24 lost full-rate hours. The usual rules land far from it in both directions. A 95% ready-rate rule holds two parts and leaves C$1.3 million a year of expected lost production; purging the slow movers leaves C$2.3 million. A 95% fill-rate rule, the textbook reorder-point formula and 'one of each' cost 10% to 35% more than the optimum, overstocking parts protected by redundancy and understocking the parts that fail most often on single equipment. An installed spare pump cuts the expected cost of the feed pump seal eightfold; a quick repair agreement or a spare shared among three plants cuts the cost of expensive spares by up to almost 60%. A one-line screening index predicts whether the first spare pays to within about 12% for single equipment. A decision map, guide, Python model and Excel template are provided."

REFS = {
    'feeney': ('Feeney, G. J., &amp; Sherbrooke, C. C. (1966). The (S − 1, S) inventory policy under compound Poisson demand. <em>Management Science, 12</em>(5), 391–411.',
        'https://doi.org/10.1287/mnsc.12.5.391'),
    'hu': ('Hu, Q., Boylan, J. E., Chen, H., &amp; Labib, A. (2018). OR in spare parts management: A review. <em>European Journal of Operational Research, 266</em>(2), 395–414.',
        'https://doi.org/10.1016/j.ejor.2017.07.058'),
    'iec61511': ('International Electrotechnical Commission. (2016). <em>Functional safety — Safety instrumented systems for the process industry sector — Part 1: Framework, definitions, system, hardware and application programming requirements</em> (IEC 61511-1:2016). IEC.',
        ''),
    'iso14224': ('International Organization for Standardization. (2016). <em>Petroleum, petrochemical and natural gas industries — Collection and exchange of reliability and maintenance data for equipment</em> (ISO 14224:2016). ISO.',
        ''),
    'kennedy': ('Kennedy, W. J., Patterson, J. W., &amp; Fredendall, L. D. (2002). An overview of recent literature on spare parts inventories. <em>International Journal of Production Economics, 76</em>(2), 201–215.',
        'https://doi.org/10.1016/S0925-5273(01)00174-8'),
    'kranenburg': ('Kranenburg, A. A., &amp; van Houtum, G. J. (2009). A new partial pooling structure for spare parts networks. <em>European Journal of Operational Research, 199</em>(3), 908–921.',
        'https://doi.org/10.1016/j.ejor.2009.01.057'),
    'croston': ('Lee, Q. F. (2026). Forecasting lumpy demand: Does Croston beat a moving average? <em>Chmltech Online Journal, 106</em>(7).',
        'https://www.chmltech.com/post/forecasting-lumpy-demand-does-croston-beat-a-moving-average.html'),
    'mcss': ('Lee, Q. F. (2026). Beyond the formula: Setting safety stock with Monte Carlo simulation. <em>Chmltech Online Journal, 106</em>(3).',
        'https://www.chmltech.com/post/beyond-the-formula-setting-safety-stock-with-monte-carlo-simulation.html'),
    'abc': ('Lee, Q. F. (2026). ABC analysis for manufacturers: Why dollar value is not enough. <em>Chmltech Insights</em>.',
        'https://www.chmltech.com/post/abc-analysis-for-manufacturers.html'),
    'pv': ('Lee, Q. F. (2026). Sizing pumps and control valves under uncertainty: Monte Carlo design points for chemical plants. <em>Chmltech Online Journal, 106</em>(8).',
        'https://www.chmltech.com/post/sizing-pumps-and-control-valves-under-uncertainty-monte-carlo-design-points-for-chemical-plants.html'),
    'arr': ('Lee, Q. F. (2026). Choosing the pump arrangement under uncertainty: Monte Carlo comparison of single, parallel and variable-speed options. <em>Chmltech Online Journal, 106</em>(9).',
        'https://www.chmltech.com/post/choosing-the-pump-arrangement-under-uncertainty-monte-carlo-comparison-of-single-parallel-and-variable-speed-options.html'),
    'molenaers': ('Molenaers, A., Baets, H., Pintelon, L., &amp; Waeyenbergh, G. (2012). Criticality classification of spare parts: A case study. <em>International Journal of Production Economics, 140</em>(2), 570–578.',
        'https://doi.org/10.1016/j.ijpe.2011.08.013'),
    'palm': ('Palm, C. (1938). Analysis of the Erlang traffic formula for busy-signal arrangements. <em>Ericsson Technics, 5</em>, 39–58.',
        ''),
    'metric': ('Sherbrooke, C. C. (1968). METRIC: A multi-echelon technique for recoverable item control. <em>Operations Research, 16</em>(1), 122–141.',
        'https://doi.org/10.1287/opre.16.1.122'),
    'sherb04': ('Sherbrooke, C. C. (2004). <em>Optimal inventory modeling of systems: Multi-echelon techniques</em> (2nd ed.). Kluwer Academic Publishers.',
        'https://doi.org/10.1007/b109856'),
    'silver': ('Silver, E. A., Pyke, D. F., &amp; Thomas, D. J. (2017). <em>Inventory and production management in supply chains</em> (4th ed.). CRC Press.',
        'https://doi.org/10.1201/9781315374406'),
    'oreda': ('SINTEF. (2015). <em>OREDA offshore and onshore reliability data handbook</em> (6th ed.). OREDA Participants.',
        ''),
    'syntetos': ('Syntetos, A. A., Babai, M. Z., &amp; Altay, N. (2012). On the demand distributions of spare parts. <em>International Journal of Production Research, 50</em>(8), 2101–2117.',
        'https://doi.org/10.1080/00207543.2011.562561'),
    'jaarsveld': ('van Jaarsveld, W., &amp; Dekker, R. (2011). Spare parts stock control for redundant systems using reliability centered maintenance data. <em>Reliability Engineering &amp; System Safety, 96</em>(11), 1576–1586.',
        'https://doi.org/10.1016/j.ress.2011.06.015'),
    'wong': ('Wong, H., van Houtum, G. J., Cattrysse, D., &amp; Van Oudheusden, D. (2006). Multi-item spare parts systems with lateral transshipments and waiting time constraints. <em>European Journal of Operational Research, 171</em>(3), 1071–1093.',
        'https://doi.org/10.1016/j.ejor.2005.01.018'),
}

CODE = {"appendix": open(__file__.replace("paper_v106_i19.py", "models/spares/spares_appendix.py"), encoding="utf-8").read().rstrip()}

DOWNLOADS = [  # served from assets/journal/code/
    dict(file='spares_appendix.py', label='Appendix script', note='Cost-optimal stock of single-equipment spares and screening indices for all 13 parts (Python 3, SciPy)'),
    dict(file='chmltech-critical-spares-model.zip', label='Full model', note='Discrete-event simulation of 13 spares over 2,000 scenarios, stocking rules, sensitivity, redundancy, repair and pooling, README'),
    dict(file='chmltech-critical-spares-template.xlsx', label='Excel template', note='Live Palm calculator, screening indices, stocking rules, decision map and the stored simulation results'),
]

BODY = r"""
## Introduction

A plant keeps two kinds of inventory that behave nothing alike. Raw materials and packaging are used every day, their demand is steady enough to forecast, and the usual tools work: ABC analysis to decide where control matters, and a safety stock set from the variation in demand over the lead time [@silver]. Spare parts are used when something breaks. A mechanical seal may be needed twice a year, a gearbox once in twenty, a compressor motor once in fifty. Demand is rare, lumpy and driven by failures [@syntetos], and the cost of being short has nothing to do with the price of the part.

The usual tools struggle with these parts in predictable ways. ABC analysis ranks items by annual usage value, so a C$90,000 motor that fails once in fifty years ranks below everyday consumables, and a periodic clean-up of slow-moving stock can remove it altogether. A service level sounds safer, but the answer depends on which service measure is chosen: when the expected demand in a lead time is a few hundredths of a part, a 95% chance that no part is owed at a random moment is met with no stock at all, while a 95% chance that a failure finds a part on the shelf needs one of everything. Neither asks what a shortage costs. Earlier Chmltech papers showed the same problem from two sides: intermittent demand defeats the forecast [@croston], and a safety stock should come from the cost of running out, not from a service-level table [@mcss]. A companion post added a criticality rating to ABC for this reason [@abc], but a rating still does not say how many parts to hold.

The right number depends on a few quantities: how often the equipment fails, how long a replacement takes to arrive, how much production is lost while it is missing, whether an installed spare carries the load in the meantime, and what it costs to keep a part on the shelf. Most of them are uncertain when the stock is set, especially the failure rate, which for a single gearbox rests on a handful of records at best [@hu]. This paper takes the plant of the earlier pump papers [@pv, @arr], lists 13 of its critical spares, and asks how many of each to hold, how sure that answer is, and which simple rule gets close to it.

## The Plant and Its Spares

The plant is the one used throughout this series: a continuous organic process making 50,000 tonnes a year, or 6.25 tonnes an hour over 8,000 operating hours [@pv]. At a product margin of C$300 a tonne, an hour of lost full-rate production costs about C$1,875, and a total loss of feed also costs a reactor restart of several hours. Table 1 lists the 13 critical spares studied. They cover the reactor feed pumps of the earlier papers, the product transfer and cooling water pumps, the reactor agitator, the recycle compressor, the feed preheater, the feed control valve, the pump drives and the reactor trip transmitters.

TABLE Critical spares of the 50,000-tonne-a-year plant, with most likely values; lead times in calendar weeks.
| Part | Equipment | Units installed / needed | Failures per running unit a year | Lead time (weeks) | Unit cost (C$) | Capacity lost while short | Expected failures in a lead time |
| P1 Mechanical seal cartridge | Reactor feed pumps P-101A/B | 2 / 1 | 0.20 | 6 | 4,500 | 100% | 0.023 |
| P2 Bearing set | Reactor feed pumps P-101A/B | 2 / 1 | 0.10 | 2 | 600 | 100% | 0.004 |
| P3 Mechanical seal cartridge | Product transfer pumps P-201A/B | 2 / 1 | 0.20 | 6 | 4,000 | 100% after 12 h buffer | 0.023 |
| P4 Motor, 7.5 kW explosion-proof | Reactor feed pumps P-101A/B | 2 / 1 | 0.03 | 10 | 6,000 | 100% | 0.006 |
| P5 Rotating assembly | Cooling water pumps P-301A/B/C | 3 / 2 | 0.15 | 12 | 18,000 | 100% | 0.069 |
| P6 Gearbox | Reactor agitator A-101 | 1 / 1 | 0.05 | 20 | 45,000 | 100% | 0.019 |
| P7 Double mechanical seal | Reactor agitator A-101 | 1 / 1 | 0.25 | 8 | 15,000 | 100% | 0.038 |
| P8 Valve set | Recycle compressor K-101 | 1 / 1 | 0.80 | 4 | 8,000 | 100% | 0.061 |
| P9 Motor, 250 kW | Recycle compressor K-101 | 1 / 1 | 0.02 | 26 | 90,000 | 100% | 0.010 |
| P10 Tube bundle | Feed preheater E-101 | 1 / 1 | 0.02 | 30 | 120,000 | 30% (tubes plugged) | 0.012 |
| P11 Valve trim kit | Flow control valve FCV-101 | 1 / 1 | 0.10 | 8 | 5,000 | 10% (on bypass) | 0.015 |
| P12 Drive power module | Pump drives | 2 / 1 | 0.07 | 8 | 3,000 | 100% | 0.011 |
| P13 Pressure transmitter | Reactor trip, 2-out-of-3 | 3 / 2 | 0.05 | 3 | 3,500 | 100% (trip) | 0.009 |

The parts span the range a maintenance planner meets. Some sit on equipment with an installed spare, so a failure costs nothing unless the spare also fails before the part arrives (P1 to P4, P12). Some sit on single equipment that stops the plant (P6 to P9). Two leave the plant running at reduced rate while the part is missing: the preheater can run with plugged tubes at 70% of rate, and the control valve can be bypassed under manual control at 90%. The product transfer pumps have 12 hours of tank buffer before the reactor must slow down. Losing a second cooling water pump is taken as a full stop, because the reactor's cooling margin trips the plant before a controlled cut to half rate is possible. The reactor trip transmitters vote 2-out-of-3 and all three are live, so any of them can fail. Failure rates are of the order found for process plant equipment in reliability databases such as OREDA and in ISO 14224 practice [@oreda, @iso14224], not taken from a specific table, and are treated as uncertain; lead times and prices are budget figures. Every one of the 13 parts has less than a 7% chance of being needed even once during a replenishment lead time, which is what makes them hard for the usual tools.

## Method

Each part is stocked with a one-for-one policy: every time a part is taken from the shelf, a replacement is ordered. This is the natural policy for expensive, slow-moving spares, and it reduces the decision to one number per part, the stock level S [@feeney, @sherb04].

**The classical result.** If failures occur as a Poisson process at rate λ per running unit and K units run, Palm's theorem says the number of parts on order follows a Poisson distribution with mean m, the expected failures in one lead time L, whatever the distribution of the lead time. The expected number of parts owed to the plant at any moment, the expected backorders, follows from it as Eq. (1) [@palm, @metric]:

TEX EBO(S) = \sum_{x > S} (x - S)\,\frac{e^{-m} m^x}{x!}, \qquad m = \lambda K L_h / 8000

For a single piece of equipment with no buffer, every backorder is equipment down. The expected annual cost of holding S parts is then Eq. (2), where r is the carrying rate, Cu the unit cost, ch the cost of an hour of lost full-rate production, f the share of capacity lost and tr the repair time once the part is on hand. All times are in operating hours, 8,000 a year, because equipment only fails, and production is only lost, while the plant runs:

TEX C(S) = r\,C_u\,S + c_h\,f \left[ \lambda K\,t_r + 8000\,EBO(S) \right]

Equation (2) is exact enough for single equipment, but it cannot handle an installed spare, a buffer tank or a 2-out-of-3 voting system, and it treats every input as known.

**The simulation.** A discrete-event simulation follows each part over a 200-year horizon for each scenario and each stock level from 0 to 4, with the same random failures for every stock level. Running units fail at random. A failure takes a part from the shelf if there is one, and the unit is repaired in tr hours; if the shelf is empty, the unit waits for the next part to arrive. Each failure triggers an order whose lead time varies by about 20% from order to order. Where units are installed in excess of those needed, the standby takes over and does not fail while idle; the exception is the trip transmitters, where all three are live and any can fail. Time runs in operating hours, and lead times and repair times quoted in calendar weeks and hours are converted to operating time. Production is lost only while fewer units work than the plant needs, and only after any buffer is used up; a total loss also costs a restart.

**The scenarios.** Table 2 lists the uncertain inputs. The failure rate of each part is multiplied by its own lognormal factor with a spread of 50%, because a plant rarely has more than a few failure records for one part and published rates vary by a factor of two or more [@hu, @oreda]. For each part, the stock level chosen is the one with the lowest expected annual cost over 2,000 scenarios, the holding cost plus the lost production.

TABLE Uncertain inputs of the scenarios.
| Input | Range used (min, most likely, max) | Basis |
| Product margin | C$150, 300, 500 per tonne | As in [@arr] |
| Carrying rate, including capital, storage, insurance and obsolescence | 15%, 25%, 35% of unit cost a year | [@silver] |
| Lead time factor | 0.8, 1.0, 1.5 times the most likely lead time | Supplier quotes |
| Order-to-order lead time variation | Lognormal, 20% | Supplier history |
| Failure rate factor, each part | Lognormal, mean 1, spread 50% | Few records per part |
| Restart after a total loss | 4, 8, 16 h of production | Plant practice |

**Two screening rules.** A hand calculation helps before any simulation. The first spare saves roughly the downtime of waiting a whole lead time for each failure, so for single equipment its value divided by its holding cost is the index of Eq. (3), with Lh the lead time in operating hours:

TEX I_1 = \frac{\lambda K\,L_h\,c_h\,f}{r\,C_u}

With one installed spare, a stocked part only matters if the standby also fails before the replacement arrives, so the value falls with the square of the failure rate and the lead time, Eq. (4):

TEX I_2 = \frac{(\lambda K)^2\,L_h^2\,c_h\,f}{2 \times 8000\,r\,C_u}

An index above 1 says the first spare pays for itself. Section 8 tests both indices against the simulation.

**The usual rules, for comparison.** All are written as a base stock S, with a replacement ordered whenever the stock position falls to S − 1 [@feeney]. The safety stock formula sets the reorder point at m plus 1.645 times the square root of m for a 95% service level, rounded to the nearest whole part, and holds one more than the reorder point. Two Poisson rules use the right distribution but different service measures [@sherb04]: a 95% ready rate holds the smallest S that leaves no part owed at a random moment with 95% probability, and a 95% fill rate the smallest S that lets 95% of failures find a part on the shelf. 'One of each' holds a single part of every kind. 'No spares' stands for a stock clean-up that removes items with no usage for several years.

**Verification.** For single equipment at the most likely values, the simulated lost hours agree with Eq. (2) to within 10% at every stock level of the gearbox, the compressor valves and the compressor motor: for example 3.5 against 3.7 h a year for the gearbox with one spare and 9.0 against 9.1 for the compressor valves with two. With no spare the simulation is 1% to 6% lower, partly because a unit cannot fail again while it is already down waiting for its part.

## Results: How Many to Hold

The cost optimum holds one of most parts, two of the parts that fail most often on single equipment, and none of two parts protected by installed redundancy. Table 3 gives the stock level of each part under each rule and the expected cost at the optimum.

TABLE Stock level of each part under each rule, and the expected annual cost and lost hours at the cost optimum (means over 2,000 scenarios).
| Part | Safety stock formula, 95% | Poisson, 95% ready rate | Poisson, 95% fill rate | Cost optimum | Cost at optimum (C$/year) | Cost with no spare (C$/year) | Lost full-rate hours at optimum (h/year) |
| P1 Feed pump seal | 1 | 0 | 1 | 1 | 1,210 | 6,540 | 0.04 |
| P2 Feed pump bearings | 1 | 0 | 1 | 1 | 150 | 200 | 0.00 |
| P3 Transfer pump seal | 1 | 0 | 1 | 1 | 1,070 | 6,200 | 0.04 |
| P4 Feed pump motor | 1 | 0 | 1 | 0 | 480 | 480 | 0.24 |
| P5 Cooling water pump assembly | 2 | 1 | 2 | 1 | 6,960 | 56,200 | 1.22 |
| P6 Agitator gearbox | 1 | 0 | 1 | 1 | 20,400 | 322,000 | 4.25 |
| P7 Agitator double seal | 1 | 0 | 1 | 2 | 22,900 | 634,000 | 5.58 |
| P8 Compressor valve set | 1 | 1 | 2 | 2 | 37,300 | 1,009,000 | 9.49 |
| P9 Compressor motor | 1 | 0 | 1 | 1 | 26,800 | 168,000 | 2.03 |
| P10 Preheater tube bundle | 1 | 0 | 1 | 1 | 31,500 | 59,400 | 0.77 |
| P11 Control valve trim | 1 | 0 | 1 | 1 | 1,660 | 25,500 | 0.21 |
| P12 Drive power module | 1 | 0 | 1 | 1 | 750 | 1,400 | 0.00 |
| P13 Trip transmitter | 1 | 0 | 1 | 0 (1 for safety, Section 8) | 690 | 690 | 0.34 |

Figure 1 shows why. For the compressor valve set, the first spare cuts the expected cost from C$1.0 million to C$75,000 a year, because without it every failure stops the plant for the four-week lead time, and the valves fail almost once a year. The second spare halves that again, because a second failure within the month the replacement is on order is not rare. A third adds holding cost and saves almost nothing. The agitator seal behaves the same way at a smaller scale. The preheater tube bundle is the expensive marginal case: a C$120,000 bundle that is needed once in fifty years still pays, because the plant would run at 70% of rate for 30 weeks without it, but only by C$28,000 a year at the most likely values. The trip transmitters need no spare on cost alone: with three installed and two needed, a failure costs nothing unless a second follows within the three-week lead time.

FIG fig1-cost-against-stock || Expected annual cost against the number of spares held for four parts: holding cost and expected lost production, means over 2,000 scenarios; the lowest total is marked in green. || Four bar charts of holding cost and expected lost production against spares held: compressor valve set lowest at two spares, agitator seal at two, tube bundle at one, trip transmitter at none ||

The optimum for the whole set holds 13 parts worth C$336,100. It costs C$152,000 a year on average, C$84,000 of it holding cost and C$68,000 expected lost production, and loses 24 full-rate hours a year plus about one restart, roughly 10 hours more. Most of the remaining loss is the repair time itself, which no stock can remove. Some choices are close: for the feed pump bearings and the drive power module, one spare and none differ by less than C$700 a year, and either is defensible.

## Why ABC and Service Levels Get It Wrong

The usual rules miss the optimum in both directions, depending on which one is used. Figure 2 compares the whole set of spares under each rule.

FIG fig2-policies || Expected annual cost, value of spares held and lost full-rate hours for the 13 spares under six stocking rules, means over 2,000 scenarios. || Three bar charts comparing six stocking rules: expected cost C$2.29M with slow movers purged, C$1.31M for a 95% ready rate, C$205k for the reorder-point formula, C$202k for one of each, C$167k for a 95% fill rate and C$152k for the cost optimum ||

**Too little: the ready rate and the stock clean-up.** A 95% ready rate, the share of time with no part owed, holds two parts, a cooling water pump assembly and a compressor valve set, worth C$26,000. Its expected cost is C$1.31 million a year, almost all of it lost production, with 653 full-rate hours lost, 8% of the operating year. The reason is that the measure is met by the calendar, not by the failures: when a part fails once in twenty years, the plant spends more than 95% of its time with nothing owed whether or not a spare is on the shelf. A periodic clean-up of slow-moving stock does worse still. Removing every part with no usage for several years, which all 13 are likely to show, leaves C$2.29 million a year of expected lost production and 1,158 hours.

**About right by accident: the fill rate, the formula and one of each.** A 95% fill rate, the share of failures that find a part, needs one of everything when failures in a lead time are rare, and two of the cooling water pump assemblies and compressor valve sets. It costs C$167,000 a year, 10% above the optimum. The textbook reorder point, m + 1.645√m rounded, is zero for 12 of the 13 parts, so with one part more than the reorder point the formula also holds one of everything, plus a second cooling water pump assembly whose reorder point rounds up only because it sits at 0.502; it costs C$205,000. 'One of each' costs C$202,000, 33% above the optimum. These rules land near the right total because, for parts this rare, one spare is often the right answer, not because they weigh what a shortage costs. They overstock the feed pump motor and the trip transmitters, which redundancy already protects, and they understock the agitator seal and, except for the fill rate, the compressor valves, where a second spare saves C$12,000 to C$38,000 a year each.

**ABC analysis cannot see downtime.** All 13 parts together use about C$25,000 of stock a year at their expected failure rates, a trace of the plant's raw material spend, so in a plant-wide ranking they all fall into class C, the class most likely to be thinned in a clean-up. Ranked among themselves, the compressor motor (C$1,800 a year) comes sixth and the gearbox fifth, behind the cooling water pump assembly, although either of them would stop the plant for months [@kennedy, @molenaers]. Adding a criticality rating fixes the ranking but not the quantity: criticality says the motor is vital, not whether one spare is enough or whether the bundle is worth C$120,000.

The lesson is not that the usual rules are always far off. It is that their answer depends on a choice of service measure that has nothing to do with the plant, and that none of them can tell a second compressor valve set worth C$38,000 a year from a feed pump motor that is better left on the supplier's shelf.

## Installed Spares, Repair and Pooling

Three choices outside the storeroom change the answer more than any stocking rule: whether the equipment has an installed spare, whether a failed part can be repaired quickly, and whether the stock is shared with other sites. Figure 3 shows their effect on four parts.

FIG fig3-redundancy-repair-pooling || Expected annual cost at the best stock level for four parts: with and without an installed spare pump, buying new against repairing, and holding a spare at each plant against sharing a pooled stock among three plants 48 hours apart. || Bar chart of expected annual cost at the best stock level: feed pump seal C$1.2k with an installed spare pump and C$10.1k without; gearbox, compressor motor and tube bundle cheaper when repaired quickly or shared by three plants ||

**An installed spare does most of the work.** With the standby feed pump, one stocked seal costs C$1,210 a year in total. Without the standby, the same seal needs two on the shelf and still costs C$10,100 a year, eight times as much, because every seal failure would stop the plant for its repair and any second failure in six weeks would stop it for weeks. Measured as the value of the first spare, the saving it makes over holding none, the difference is about seventyfold: C$5,300 a year with the standby, C$372,000 without. This is the other half of the result of the pump arrangement paper, where one 100% pump and an installed spare was the cheapest arrangement [@arr]: the installed spare also cuts the storeroom. The same logic is why the feed pump motors and, on cost alone, the trip transmitters in a 2-out-of-3 system need no spare [@jaarsveld].

**Repair shortens the lead time, and the lead time drives the cost.** If the agitator gearbox can be repaired in six weeks instead of bought new in twenty, its best cost falls from C$20,400 to C$16,700 a year, still with one spare held. A compressor motor rewound in four weeks instead of bought new in 26 still justifies one spare, because a four-week stop would cost about C$1.2 million even if it comes only once in fifty years, but its cost falls only from C$26,800 to C$25,400 a year; the spare's holding cost dominates. A tube bundle that can be retubed in eight weeks no longer justifies a C$120,000 spare: holding none costs C$16,800 a year against C$31,500 for one new bundle on the shelf. These comparisons change only the lead time; the repair bill per event, against the price of a new part, is a separate saving or cost to add. A firm repair agreement with a turnaround time in it is worth negotiating before the spare is bought.

**Pooling spreads an expensive spare across plants.** If three sister plants, or a supplier's consignment stock, share one compressor motor that can reach any of them in 48 hours, each plant's cost falls from C$26,800 to C$15,600 a year, and for the tube bundle from C$31,500 to C$13,000. For the gearbox the best pooled stock is two for three plants, at C$17,300 a year per plant against C$20,400 alone. Pooling works best for parts that are expensive and rarely needed, where a plant's own spare sits idle almost all the time; it adds the transfer time to every repair and needs an agreement on who gets the part when two plants need it at once [@wong, @kranenburg].

## What Changes the Answer

The stock levels are robust to most of the uncertainty. Choosing each part's stock at the most likely values instead of over all 2,000 scenarios changes only the feed pump bearings, from one to none, and changes the expected cost by less than C$100 a year. Over the scenarios, the expected regret of the chosen stock levels against the best set for each scenario is C$16,300 a year. That figure overstates what could be gained in practice: the best set for each scenario is picked with hindsight on the same simulated failures, so it includes luck that no stocking rule could capture.

**Failure rate uncertainty.** If the failure rates were known exactly, the choice would not change at all. If they were twice as uncertain, with a spread of 100% instead of 50%, the optimum would add a second cooling water pump assembly, a third compressor valve set and one trip transmitter. A poorly known failure rate argues for more stock, not less, because the expected downtime is dominated by the scenarios where the rate is high. Each failure the plant records narrows this spread, and the stock should be reviewed as the records build up.

**Margin and carrying rate.** At the unfavourable end of both ranges, a margin of C$150 a tonne and a carrying rate of 35%, the optimum drops the feed pump bearings, the drive power module and the tube bundle. The bundle is the part most sensitive to the plant's economics: it pays for itself at the most likely values with a ratio of about two (Section 8), and a halved margin with a higher carrying rate removes that.

**Lead time.** Lead time enters twice: in how long the plant waits without a spare, and in how likely a second failure is while a part is on order. A 50% longer lead time than quoted is within the range already sampled; a supplier that quotes four weeks and delivers in twelve would move the compressor valve set toward three spares. Lead times should be checked against what suppliers actually delivered, not what they quoted.

## Decision Guide

A planner does not need a simulation for every part. The screening indices of Eqs. (3) and (4) sort most parts by hand, and Figure 4 tests them against the simulation.

FIG fig4-screening-index || Screening index from Eqs. (3) and (4), at most likely values, against the same ratio from the simulation, which averages over the scenarios: the value of the first spare divided by its holding cost. || Log-log scatter of the screening index against the simulated ratio for 13 parts; single-equipment parts lie on the diagonal from about 2 to 460, parts with installed spares 1.5 to 2 times above it ||

For single equipment, Eq. (3) agrees with the simulation to within about 12% for every part, from the tube bundle at about 2 to the compressor valves at about 460, and runs slightly low because the simulation averages over margins and lead times whose means sit above their most likely values. For equipment with an installed spare, Eq. (4) ranks the parts correctly but comes out low by a factor of 1.5 to 2; for the transmitters, whose three units are all live, the first failure rate is 3λ and the second 2λ, so (λK)² becomes 6λ². The value of a spare on spared equipment rises with the square of the failure rate and of the lead time, so the spread in both counts double: a 50% spread in the failure rate raises the mean of its square by 28%, and the lead time factor, with a mean of 1.1, raises the mean of its square by more than 20%. Treat an Eq. (4) index above 0.5 as worth a spare. Only the feed pump motor (0.17) and the trip transmitters (0.43) fall below the line.

For single equipment the whole decision fits on one chart. Figure 5 gives the cost-optimal stock from Eq. (2) for any combination of the expected failures in a lead time and the ratio of a year of downtime to the holding cost of one part. The parts of this plant sit in the region of one or two spares. The boundary for a second spare depends on both axes: at a ratio of about 1,000 it lies near 0.05 expected failures in a lead time, at about 10,000 near 0.015, which is why the agitator seal and the compressor valves need two and the gearbox one.

FIG fig5-decision-map || Cost-optimal number of spares for single equipment with no buffer, from Eq. (2), against the expected failures in one lead time and the ratio of a year of downtime cost to the holding cost of one part; points are this plant's single-equipment parts at most likely values. || Decision map of optimal spares from 0 to 5 or more against expected failures in a lead time and the ratio of a year of downtime to holding cost, with six parts of the plant in the one- and two-spare regions ||

Table 4 turns the results into a guide.

TABLE Stocking guide for critical spares.
| Situation | Start from | Why |
| Single equipment that stops the plant, index of Eq. (3) above 1 | At least one spare; read Figure 5 for more | Each failure without a spare costs a whole lead time of production |
| High downtime ratio and frequent failures: above about 0.05 failures in a lead time at a ratio of 1,000, or 0.015 at 10,000 | A second spare (Figure 5) | A second failure while the replacement is on order becomes costly enough to cover |
| Installed spare equipment, index of Eq. (4) above 0.5 | One spare | Protects against the standby failing while the part is on order |
| Installed spare equipment, index of Eq. (4) well below 0.5 | No spare on cost; keep a supplier agreement | Redundancy already carries the risk |
| Safety-instrumented or other safety-critical parts | A minimum stock set by the safety case, usually at least one | The repair time assumed in the safety integrity calculation must be achievable |
| Expensive part, rarely needed, sister plants or a supplier stock nearby | Share the spare | Cut the cost per plant by up to about 60% here |
| Expensive part that can be repaired quickly | Price a repair agreement before buying the spare | A short turnaround can remove the need for the spare |
| Few failure records for the part | Lean toward the higher stock | Uncertain failure rates raise the expected downtime |

**Safety-critical parts are set differently.** The trip transmitters show why cost optimisation is not the whole answer. On cost alone they need no spare, but they belong to a safety-instrumented function whose integrity calculation assumes that a failed channel is repaired within a stated time [@iec61511]. If a replacement takes three weeks, the function runs on two channels with no margin for that time. Parts like these get a minimum stock from the safety case, usually one, and the cost model is used only above that minimum; holding one transmitter adds about C$190 a year here.

Five steps turn the guide into a stocking decision for a plant.

1. **List parts by equipment, not by value.** Record for each part the units installed and needed, the buffer and the share of capacity lost while it is missing.
2. **Get the failure rate from records, with its uncertainty.** Use the plant's own maintenance history where it exists and a reliability database where it does not, and keep the spread.
3. **Use delivered lead times and repair turnarounds.** Quotes are optimistic, and the lead time is the input that matters most.
4. **Screen with Eqs. (3) and (4), then simulate the borderline parts.** Most parts are clearly in or out; the simulation is for the ones near the line and for redundant or buffered equipment.
5. **Review after each failure.** A new failure record, a changed lead time or a new installed spare can change the right stock.

### 8.1 Pitfalls

- **Using a service level for spares.** A service level ignores what a shortage costs; set stock from the cost of downtime instead.
- **Rounding the reorder point.** For parts with tiny expected demand, the normal formula rounds to zero whatever service level is chosen.
- **Counting the spare's price as the cost of holding it.** The decision rests on the carrying cost a year, not the purchase price, which is spent at the first failure either way.
- **Ignoring installed redundancy.** Parts on spared equipment need far less stock than parts on single equipment.
- **Trusting one quoted lead time.** Lead times stretch exactly when the market is busy; use what suppliers delivered.

## Conclusions

Critical spares should be stocked from the cost of downtime, not from a service level or a value ranking. For the 13 critical spares of a 50,000-tonne-a-year chemical plant:

- The cost optimum holds 13 parts worth C$336,000 and costs C$152,000 a year, with 24 lost full-rate hours, most of them repair time no stock can remove.
- The usual rules miss in both directions. A 95% ready rate holds two parts and leaves C$1.3 million a year of expected lost production; a clean-up of slow movers leaves C$2.3 million. A 95% fill rate, the reorder-point formula and one of each hold one of nearly everything and cost 10% to 35% more than the optimum.
- None of the usual rules sees what a shortage costs: they overstock parts protected by redundancy and understock the parts that fail most often on single equipment, where a second spare is worth up to C$38,000 a year.
- An installed spare pump cuts the expected cost of the feed pump seal eightfold. A quick repair agreement or a spare shared among three plants cuts the cost of expensive, rarely needed spares by up to almost 60%, and can remove the need for a C$120,000 tube bundle.
- A one-line screening index predicts whether the first spare pays to within about 12% for single equipment, and ranks parts on spared equipment correctly when given a lower threshold. Safety-critical parts need a minimum stock from the safety case before any cost rule applies.

The case has limits. The failure rates are generic, the lead times are budget figures and the plant is a single site; parts shared among several pieces of equipment, parts that age, and multi-level repair networks are outside the model. Several practical factors would lower the stock: buying a part at a premium or borrowing one when a failure happens, rather than waiting the full lead time, and condition monitoring that gives warning of a failing gearbox, motor or valve before it stops. Others would raise it: a standby that fails to start or fails while idle, shelf-life limits on elastomer seals and stored motors, and a contract penalty or safety consequence beyond the product margin. Insurance spares are usually capitalised and depreciated rather than expensed, which changes how the holding cost appears in the accounts but not the economics. The method transfers to any plant: the Python model and an Excel template can be downloaded from this paper's page.

## Appendix: Setting Spare Stock for Your Own Plant

Table 5 sets out the method in steps, with what this paper did and where the downloadable model does it. The script below applies Eqs. (1) to (4) to the 13 parts at their most likely values: for the six single-equipment parts it gives the same stock as the simulation, and for the parts on spared equipment it gives the screening index. The full model adds the simulation of installed spares and buffers, the 2,000 scenarios, repair and pooling.

TABLE Steps of the method, with this paper's choices and the model function that does each.
| Step | What to do | In this paper | In the model |
| 1. List the parts by equipment | Units installed and needed, buffer, capacity lost while short | 13 parts (Table 1) | PARTS |
| 2. Describe the uncertainty | Failure rate spread, lead time, margin, carrying rate, restart | Table 2 | SCEN, LAM_SIGMA |
| 3. Screen | Indices of Eqs. (3) and (4) | Figure 4 | analyse.py |
| 4. Simulate each stock level | Failures, orders, repairs, downtime after the buffer | 2,000 scenarios, 200 years each | simulate(), evaluate() |
| 5. Choose and compare | Lowest expected cost; the usual rules for comparison | Table 3, Figure 2 | spares_model.py, analyse.py |
| 6. Test the choice | Failure-rate spread, economics, redundancy, repair, pooling | Sections 6 and 7 | extras.py |

CODE appendix || Cost-optimal stock of the single-equipment spares from Eqs. (1) and (2), and the screening indices of Eqs. (3) and (4) for all 13 parts at most likely values (Python 3 with SciPy).
"""
