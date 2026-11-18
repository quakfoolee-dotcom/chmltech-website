"""Chmltech Online Journal, Vol. 106, Issue 9: Choosing the Pump Arrangement Under Uncertainty: Monte Carlo Comparison of Single, Parallel and Variable-Speed Options (Nov 18 2026).

Worked case: the reactor feed service of Issue 8 (20,000 operating cases) with six arrangements (A, B, C3, C2, E3, E2) and
variant D, 5,000 economic scenarios and a 20-year discrete-event failure simulation. Model:
content/journal/ops/models/pumparr/. Red-teamed (model audit, engineering and references) before publication."""

SLUG = "choosing-the-pump-arrangement-under-uncertainty-monte-carlo-comparison-of-single-parallel-and-variable-speed-options"
META = dict(
    volume=106, issue=9,
    title='Choosing the Pump Arrangement Under Uncertainty: Monte Carlo Comparison of Single, Parallel and Variable-Speed Options',
    short_title='Choosing the Pump Arrangement Under Uncertainty',
    meta='Single, parallel or variable-speed pumps? A Monte Carlo life-cycle comparison: one pump and a spare on drives is cheapest in 96% of scenarios.',
    keywords=['pump arrangement', 'parallel pumps', 'variable speed drive', 'Monte Carlo simulation', 'life-cycle cost', 'reliability', 'installed spare', 'API 610'],
)
PUBLISHED = "2026-11-18"
DIVISION = "Division of Clean Energy Technology Innovation"   # process plant papers (as Issue 8)
ABSTRACT = "Engineers choose a pump arrangement, one duty pump with a spare or two half-size pumps in parallel, a control valve or a variable-speed drive, mostly by habit. Six arrangements are compared under uncertainty for the reactor feed service of an earlier Chmltech paper. Its 20,000 correlated operating cases are solved for each arrangement's hydraulics, efficiency and operating region at normal rate and at 50% turndown. Then 5,000 economic scenarios add uncertain electricity price, time at turndown, pump efficiency, reliability, repair cost, product margin and installed cost, and a 20-year failure simulation. For this small service, about 5 kW, one 100% pump with an installed spare, both on variable-speed drives without a control valve, has the lowest 20-year life-cycle cost in 96% of scenarios: C$344,000 on average against C$363,000 with a control valve. Two 50% pumps with a spare cost C$452,000 to C$465,000. They run nearer their best-efficiency point at turndown, but need a third installed train and fail almost twice as often. Without the spare, they lose 13 to 15 full-rate hours of production a year and cost the most. The ranking holds for flat or steep pump curves and for turndown up to half the hours. The drives pay only if they replace the control valve and cost less than about twice the budget price. Parallel pumps on drives compete above about 30 kW with long periods at reduced rate. A screening guide, the Python model and an Excel template are included."

REFS = {
    'api610': ('American Petroleum Institute. (2021). <em>Centrifugal pumps for petroleum, petrochemical and natural gas industries</em> (API Standard 610, 12th ed.). API.',
        'https://www.api.org/products-and-services/standards'),
    'bloch': ("Bloch, H. P., &amp; Budris, A. R. (2004). <em>Pump user's handbook: Life extension</em>. Fairmont Press.",
        'https://doi.org/10.4324/9780203021743'),
    'budris': ('Budris, A. R. (2017, March 1). Improving pump component reliability to optimize mean time between failure. <em>WaterWorld</em>.',
        'https://www.waterworld.com/wastewater/treatment/article/16191867/improving-pump-component-reliability-to-optimize-mean-time-between-failure'),
    'gulich': ('Gülich, J. F. (2020). <em>Centrifugal pumps</em> (4th ed.). Springer.',
        'https://doi.org/10.1007/978-3-030-14788-4'),
    'hardee': ('Hardee, R. (2026, August). How to tell if your pump operation is shortening equipment life. <em>Pumps &amp; Systems</em>.',
        'https://cahaba-media-group.foleon.com/pumpssystems/2026-august8/columns'),
    'hi': ('Hydraulic Institute. (2022, June 15). <em>Five keys to understanding parallel pump optimization</em>.',
        'https://pumps.org/2022/06/15/five-keys-to-understanding-parallel-pump-optimization'),
    'lcc': ('Hydraulic Institute &amp; Europump. (2001). <em>Pump life cycle costs: A guide to LCC analysis for pumping systems</em>. Hydraulic Institute.',
        ''),
    'vsd': ('Hydraulic Institute &amp; Europump. (2004). <em>Variable speed pumping: A guide to successful applications</em>. Elsevier.',
        ''),
    'inl': ('Idaho National Laboratory. (2009). <em>Component performance study: Motor-driven pumps, 1998–2008 (2008 update)</em>. US Nuclear Regulatory Commission.',
        'https://nrcoe.inl.gov/publicdocs/CompPerf/mdp-2008.pdf'),
    'pv': ('Lee, Q. F. (2026). Sizing pumps and control valves under uncertainty: Monte Carlo design points for chemical plants. <em>Chmltech Online Journal, 106</em>(8).',
        'https://www.chmltech.com/post/sizing-pumps-and-control-valves-under-uncertainty-monte-carlo-design-points-for-chemical-plants.html'),
    'db': ('Lee, Q. F. (2026). The design basis: Ten decisions to fix before engineering starts. <em>Chmltech Insights</em>.',
        'https://www.chmltech.com/post/the-design-basis-ten-decisions-to-fix-before-engineering-starts.html'),
    'savage': ('Savage, L. J. (1951). The theory of statistical decision. <em>Journal of the American Statistical Association, 46</em>(253), 55–67.',
        'https://doi.org/10.1080/01621459.1951.10500768'),
    'tmeic': ('TMEIC. (2017). <em>Variable frequency drive reliability</em> (Application Edge, Vol. 1, Issue 6). TMEIC Corporation.',
        'https://www.tmeic.com/sites/default/files/assets/files/library/TMC_VFDReliability_WP.pdf'),
    'towler': ('Towler, G., &amp; Sinnott, R. (2013). <em>Chemical engineering design: Principles, practice and economics of plant and process design</em> (2nd ed.). Butterworth-Heinemann.',
        ''),
    'doe': ('US Department of Energy. (2006). <em>Optimize parallel pumping systems</em> (Pumping Systems Tip Sheet 8). Industrial Technologies Program.',
        'https://webarchive.library.unt.edu/web/20120916063025/http://www1.eere.energy.gov/manufacturing/tech_deployment/pdfs/38945.pdf'),
}

CODE = {"appendix": open(__file__.replace("paper_v106_i9.py", "models/pumparr/pump_arrangement_appendix.py"), encoding="utf-8").read().rstrip()}

DOWNLOADS = [  # served from assets/journal/code/
    dict(file='pump_arrangement_appendix.py', label='Appendix script', note='Average power of A, B, C and E over 20,000 cases (Python 3, NumPy, SciPy)'),
    dict(file='chmltech-pump-arrangement-model.zip', label='Full model', note='Hydraulics, failure simulation, life-cycle cost, sensitivity and the Issue 8 model it builds on, README'),
    dict(file='chmltech-pump-arrangement-template.xlsx', label='Excel template', note='All 5,000 scenarios with live life-cycle cost, cheapest option and regret, calculator, 20,000 cases (about 10 MB)'),
]

BODY = r"""
## Introduction

Every pump service on a new chemical plant needs two decisions besides the rated point. How many pumps share the duty, and how is the flow controlled? The usual answers come from habit. One running pump with an installed spare is the default for continuous service. Two half-size pumps are chosen when someone remembers a wide turndown or wants to keep running when one pump trips. A variable-speed drive is added when energy is on someone's mind, often on top of a control valve that stays in the line.

Each habit has a sound argument behind it, and each argument is incomplete. Two 50% pumps keep the running pump near its best-efficiency point at low flow, where Barringer's field data show reliability falling steeply, by nearly half at moderate deviation [@hardee]. But two running pumps also mean two sets of seals and bearings to fail, and a third installed train. A drive removes the throttling loss, but it costs money and can fail too. Which effect wins depends on numbers that are uncertain when the choice is made: how much time the plant will spend at reduced rate, what electricity will cost, how often pumps fail and how long they take to repair, and what an hour of lost production is worth.

The earlier paper in this series sized one pump and control valve under uncertainty [@pv]. This paper keeps that service, the reactor feed of a chemical plant making 50,000 tonnes a year [@db], and its 20,000 operating cases, and changes only the arrangement. It asks which arrangement has the lowest 20-year life-cycle cost, how sure that answer is, and what would change it.

## The Service and the Options

The service is the reactor feed system of the earlier paper. A nitrogen-blanketed tank feeds the pumps, which deliver an organic feed blend through a flow meter, the flow control valve FCV-101 and a preheater to a reactor at 4.0 barg, 14 m above the pumps. Normal flow is 9.8 m³/h, and the plant must run at 50% of design rate. Eleven inputs vary between cases: production rate, recycle, temperature, reactor pressure, tank level and blanket pressure, and the design unknowns of route length, fittings, roughness, fouling and strainer clogging [@pv].

That paper rated the pump at the 95th percentile of the cases: 10.68 m³/h at 82.5 m, which keeps at least 0.7 bar across the control valve in 95% of operating states. Every arrangement here meets the same standard. The 50% pumps are rated at half the flow and the same head, so two of them in parallel have exactly the curve of the 100% pump. The comparison is therefore at equal coverage, not between a generous and a lean design.

Table 1 lists the six arrangements compared. A seventh, D, is analysed but not ranked, for a reason Section 5 shows.

TABLE The arrangements compared.
| Option | Pumps installed | Running at normal flow | Flow control | Drives |
| A | 2 × 100% (one spare) | 1 | Control valve | None |
| B | 2 × 100% (one spare) | 1 | Pump speed, no control valve | 2 |
| C3 | 3 × 50% (one spare) | 2, one at low flow | Control valve; second pump staged on and off | None |
| C2 | 2 × 50% (no spare) | 2, one at low flow | As C3 | None |
| E3 | 3 × 50% (one spare) | 2, one at low flow | Pump speed; pumps staged and run at equal speed | 3 |
| E2 | 2 × 50% (no spare) | 2, one at low flow | As E3 | 2 |
| D (not ranked) | 2 × 50% | 2, one at low flow | Lead pump on a drive, lag pump at fixed speed, no valve | 1 |

All pumps follow the generic curve of the earlier paper, with shutoff head 1.2 times rated head and best-efficiency flow 1.05 times rated flow. The 100% pump has a best efficiency of 40%. A pump of half the flow at the same head has a lower specific speed and a lower efficiency [@gulich]; the 50% pumps are taken at 34%, and both values are treated as uncertain. Each pump train has an explosion-proof motor: 7.5 kW for the 100% pump and 5.5 kW for each 50% pump, sized to API 610 on rated and end-of-curve power [@api610]. The 50% pump just misses a 4 kW motor: with the 125% margin on its rated power it needs 4.05 kW, so each 50% train carries a 5.5 kW motor.

## Method

The comparison runs in two layers. The first solves the hydraulics of every arrangement for every operating case. The second puts costs, failures and their uncertainty on top.

**Parallel pumps.** Identical pumps in parallel share the flow equally at a common head, so k pumps of rated flow Qr,p deliver total flow Q at the head of Eq. (1) [@hi]:

TEX H = H_r \left[ S\,n^2 - (S - 1) \left( \frac{Q}{k\,Q_{r,p}} \right)^2 \right]

where Hr is the rated head, S the shutoff ratio (1.2) and n the speed as a fraction of full speed (1 for fixed-speed pumps). With a control valve, the valve takes the difference between this head and the system head of each case. With drives and no valve, the speed is solved so that the pump head equals the system head, Eq. (2):

TEX n = \sqrt{ \frac{ H_{sys}/H_r + (S - 1) \left( Q / k Q_{r,p} \right)^2 }{ S } }

**Staging.** In C, the second pump runs only when one pump alone cannot keep 0.7 bar across the valve. In E, the controller runs the number of pumps that draws less power, provided neither pump falls below its minimum continuous stable flow, taken as 30% of best-efficiency flow at its speed. Where a pump would fall below that flow, a recirculation line holds it there and returns the excess to the tank. These are the rules a sound control system would follow: operate the fewest pumps the demand needs [@hi, @doe].

**Operating cases.** The 20,000 normal cases of the earlier paper are solved for every arrangement, and so is the same set at 50% of each case's flow, to represent turndown. Each solution gives the pump flow as a share of its best-efficiency flow, its efficiency, its speed, the valve drop and the electrical power, with motor efficiency 92% and drive efficiency 97%.

**Failures and outages.** Each arrangement is run through a 20-year discrete-event simulation. Running pump trains fail at random. A failed train goes to repair. A standby train, where there is one, is started automatically, and fails to start with a given probability, in which case an operator starts it after an hour. While fewer pumps run than the demand needs, production is lost: all of it with no pump running, and 25% of it with one 50% pump running, because one 50% pump alone delivers on average 75% of the normal demand. A total loss of feed also costs a reactor restart. The simulation runs both 50% pumps in every hour; at turndown only one runs, so for the share of hours at turndown the failures of the parallel arrangements are halved, and their outage hours are halved with a spare and removed without one. A repair of a 50% pump costs 0.76 times that of a 100% pump, following the 0.4 power of size used for larger duties. Pumps fail faster when they run outside their preferred operating region of 70% to 120% of best-efficiency flow; the failure rate is multiplied by an uncertain factor of 1.0 to 2.0 for the share of running hours spent outside it, Eq. (3):

TEX \lambda = \lambda_0 \left[ 1 + (f_{BEP} - 1)\,\phi_{out} \right]

where λ0 is the base failure rate, fBEP the penalty factor and φout the share of running hours outside the preferred region.

**Life-cycle cost.** Each scenario's 20-year life-cycle cost is the installed capital plus the present value of electricity, repairs and lost production, Eq. (4), discounted at 8% over 20 years (a present-value factor of 9.82) [@lcc]:

TEX LCC = C_{inst} + \frac{1 - (1 + i)^{-n}}{i} \left( E + R + L \right)

Installed capital uses the pump and explosion-proof motor cost correlations of Towler and Sinnott, escalated to 2025, multiplied by Hand's installation factor of 4.0 for pumps; the control valve and drives use budget prices with installation allowances [@towler]. Table 2 lists the uncertain inputs. For each scenario, the regret of an option is its life-cycle cost minus that of the cheapest option in the same scenario [@savage].

TABLE Uncertain inputs of the economic scenarios and fixed constants of the failure simulation.
| Input | Range used (min, most likely, max) | Basis |
| Electricity price | C$0.07, 0.09, 0.13/kWh | Industrial tariffs; hold H-02 |
| Share of hours at 50% turndown | 0% to 25%, uniform | Operating plan |
| Pump efficiency factor | 0.90, 1.00, 1.12 on 40%; 50% pumps a further 0.93 to 1.10 | Generic curves; hold H-01 |
| Pump mean time between failures, running | 1.5, 2.5, 4.5 years | ANSI process pump benchmarks [@budris] |
| Off-region failure penalty | 1.0, 1.5, 2.0 | Barringer's curve [@hardee] |
| Mean time to repair | 24, 72, 168 h | Plant practice |
| Standby failure to start | 0.002, 0.01, 0.03 per demand | Above the nuclear-industry mean of 0.0015 [@inl] |
| Repair cost per pump failure | C$6,000, 10,000, 20,000 | About US$10,000 per repair [@bloch] |
| Drive mean time between failures | 8, 15, 25 years | Fleet data, mostly medium-voltage drives [@tmeic]; lower bound assumed |
| Product margin | C$150, 300, 500 per tonne | Plant economics |
| Restart after total loss of feed | 4, 8, 16 h of production | Plant practice |
| Installed cost factors | Pumps, lognormal ±15%; drives 0.7, 1.0, 1.5 | Factored estimate |
| Switchover dip on a standby start (fixed) | 0.25 h at the shortfall in flow | Plant practice |
| Manual start after failure to start (fixed) | 1 h | Plant practice |
| Repair cost per drive failure (fixed) | C$3,000 | Budget allowance |

**Verification.** Three checks do not depend on the arrangement model. For option A it reproduces the earlier paper exactly: 10.68 m³/h at 82.5 m and 5.60 kW average power. Two 50% pumps at full speed give the same head as the 100% pump at every flow, to machine precision, as Eq. (1) requires. In every case of A, B, C3 and E3, the electrical power times the motor, drive and pump efficiencies equals the flow times the pump head, and for A the pump head equals the system head plus the valve drop.

## Results: Where Each Arrangement Runs

All arrangements deliver the demand in practically every case. The valve arrangements, A and C, keep at least 0.7 bar across the valve in 95% of normal cases by design. The drive arrangements, B and E, reach every demand below full speed, needing 85% to 98% of full speed in normal operation. Figure 1 shows why the two families behave so differently at turndown: the demand at half rate sits far to the left of the 100% pump's curve, but close to the best-efficiency point of one 50% pump.

FIG fig1-curves-and-demand || Pump curves of the arrangements against the system head of 2,500 sampled normal cases and the same cases at 50% turndown; dashed lines are the 100% pump at reduced speed. || Pump curves of a 100% pump, a 50% pump and two in parallel, with the 100% pump at 85% and 75% speed, against clouds of 2,500 normal demands around 9 to 11 m3/h and 70 to 90 m and the same demands at half flow. ||

Figure 2 and Table 3 show where each running pump sits on its curve. In normal operation every ranked arrangement keeps its pumps in the preferred region, with the 1st to 99th percentiles between 74% and 103% of best-efficiency flow. At turndown they separate. The 100% pump on a valve falls to 43% of its best-efficiency flow, and on a drive to 55%. A single 50% pump, which is what C and E run at turndown, stays at 86% on a valve and at 101% on a drive.

FIG fig2-share-of-bep || Flow of each running pump as a share of its best-efficiency flow at its speed, in normal operation and at 50% turndown; boxes span the 25th to 75th percentiles, whiskers the 1st to 99th. || Box plots of each running pump's flow as a share of its best-efficiency flow for options A, B, C, E and D: all ranked options within 74% to 103% in normal operation; at turndown A falls to 43%, B to 55%, while C and E stay at 86% and 101%. ||

TABLE Operating region, efficiency and motor of each arrangement over the 20,000 cases (median and percentiles).
|  | A | B | C | E |
| Pumps running, normal / turndown | 1 / 1 | 1 / 1 | 2 / 1 | 2 / 1 |
| Share of best-efficiency flow, normal (median) | 86% | 94% | 86% | 94% |
| Share of best-efficiency flow, turndown (median) | 43% | 55% | 86% | 101% |
| Pump efficiency, normal / turndown | 39% / 27% | 40% / 32% | 33% / 33% | 34% / 34% |
| Speed at turndown (1st to 99th percentile) | 100% | 74% to 83% | 100% | 80% to 90% |
| Hours outside the preferred region | Turndown hours | Turndown hours | None | None |
| Lowest NPSH margin (m) | 9.6 | 9.6 | 9.6 | 9.6 |
| Motor per pump (kW) | 7.5 | 7.5 | 5.5 | 5.5 |

None of the arrangements is short of suction head; the lowest margin, 9.6 m, is the same for all because it occurs at the highest flow. The design pressure is the same for all, too: the 50% pumps have the same shutoff head as the 100% pump, and drives cannot run above full speed.

## Energy and Turndown

The drive saves energy in both operating states; the second pump saves it only at turndown. Figure 3 gives the average electrical power. In normal operation the single pump on a drive, B, draws 4.61 kW against 5.60 kW on a valve, A, because no head is burned in the valve [@vsd]. Two 50% pumps draw more than one 100% pump in normal operation, 6.59 kW on a valve and 5.42 kW on drives, because the smaller pumps are less efficient. At turndown the order changes: one 50% pump on a drive draws 2.27 kW, one 100% pump on a drive 2.43 kW, and one 100% pump on a valve 4.54 kW.

FIG fig3-power || Average electrical power of each arrangement in normal operation and at 50% turndown, including motor and drive losses. || Bar chart of average electrical power: normal operation A 5.60, B 4.61, C 6.59, E 5.42, D 6.10 kW; at 50% turndown A 4.54, B 2.43, C 3.30, E 2.27 kW. ||

For this service the plant spends at most a quarter of its hours at turndown, so the normal-rate figures dominate. At C$0.09/kWh and the average time at turndown, B uses the least electricity, about C$3,120 a year, E about C$3,620, A about C$3,940 and C about C$4,450. Even if the plant ran half its hours at turndown, E would draw 3.8 kW on average against B's 3.5 kW.

**Option D shows a flow gap.** With a drive on the lead pump and the lag pump at fixed speed, the lead pump handles low demand alone, as the Hydraulic Institute suggests [@hi]. But once the fixed-speed lag pump joins, it delivers almost the whole demand at the system head, and the lead pump is pushed towards zero flow. In 14% of normal cases the lead pump would fall below its minimum stable flow at its speed and needs recirculation. The lead pump spends only 16% of its hours in the preferred region, and the lag pump, at a median 128% of its best-efficiency flow, also only 16%. D draws 6.10 kW, 12% more than E. It works only where the lag pump's share is small, which needs a much flatter system curve than this one. It is left out of the ranking.

**Deeper turndown makes the gap between the families larger.** If the plant had to run at 25% of design rate, the 100% pump on a valve would need recirculation in every case and the 100% pump on a drive in 77% of them, because the static head stops the drive from slowing enough. A single 50% pump on a drive would need none, and would draw 1.33 kW against 1.88 kW for B and 4.27 kW for A.

## Availability: What a Pump Trip Costs

With an installed spare, every arrangement loses less than an hour of full-rate production a year; without one, two 50% pumps lose 13 to 15. Figure 4 shows the simulated lost production and repairs.

FIG fig4-availability || Lost production in full-rate hours a year (mean, with the bar to the 95th percentile, log scale) and pump or drive failures a year, from 5,000 scenarios of a 20-year simulation. || Two bar charts: lost production a year on a log scale, 0.11 to 0.30 h for arrangements with a spare and 13 to 15 h without; failures a year, 0.36 and 0.42 for single-pump and 0.63 to 0.75 for two-pump arrangements. ||

With a spare, losses come from the short dip while the standby starts, from the occasional standby that fails to start, and from the rare second failure during a repair. The single-pump arrangements lose 0.24 h a year on a valve and 0.30 h on drives, the extra coming from drive failures. Two 50% pumps with a spare lose slightly less, 0.11 to 0.14 h, because a trip leaves the other pump running at three-quarters of the demand.

The price of that resilience is repairs. Two running pumps fail almost twice as often as one: 0.64 failures a year for C against 0.36 for A, and 0.75 for E with its three drives against 0.42 for B. The off-region penalty narrows the gap only slightly, because the single pumps spend at most a quarter of their hours outside the preferred region. At about C$10,000 a repair for a 100% pump [@bloch], and 0.76 times that for a 50% pump, the extra repairs cost about C$1,500 a year, three times the difference in electricity between the two families.

Without a spare, C2 and E2 save one pump train but lose a quarter of production for the length of every repair at normal rate, and a repair averages almost four days. That costs C$25,000 to C$29,000 a year at a margin of C$300 a tonne, about two and a half times the yearly capital charge of the pump train they save. Whether a plant can run at 75% for days without other costs, such as off-specification product or a missed delivery, is outside the model; here the answer is already clear without them.

## Life-Cycle Cost and the Probability Each Option Is Cheapest

Option B, one 100% pump and a spare on drives, is the cheapest arrangement in 96% of the 5,000 scenarios, with an average 20-year life-cycle cost of C$344,000. Table 4 and Figure 5 give the results.

TABLE Twenty-year life-cycle cost of each arrangement over 5,000 scenarios (means, C$).
| Option | Installed capital (C$) | Electricity (C$/year) | Repairs (C$/year) | Lost production (C$/year) | 20-year life-cycle cost, mean (P5 to P95) (C$) | Cheapest in | Mean regret (C$) |
| B | 261,500 | 3,340 | 4,510 | 600 | 344,000 (276,000 to 424,000) | 96.5% | 700 |
| A | 274,000 | 4,220 | 4,340 | 480 | 363,000 (289,000 to 449,000) | 3.0% | 19,000 |
| E3 | 351,600 | 3,840 | 6,120 | 280 | 452,000 (366,000 to 550,000) | 0.3% | 108,000 |
| C3 | 359,400 | 4,720 | 5,800 | 210 | 465,000 (373,000 to 570,000) | 0% | 121,000 |
| C2 | 248,800 | 4,720 | 5,780 | 26,100 | 609,000 (387,000 to 946,000) | 0.1% | 265,000 |
| E2 | 234,400 | 3,840 | 6,100 | 30,700 | 634,000 (392,000 to 1,000,000) | 0.1% | 290,000 |

FIG fig5-life-cycle-cost || Twenty-year life-cycle cost of each arrangement: mean components stacked, the spread from the 5th to the 95th percentile of 5,000 scenarios, and the share of scenarios in which each is cheapest. || Stacked bars of 20-year life-cycle cost for six arrangements with whiskers from P5 to P95: B C$344,000 and cheapest in 96% of scenarios, A C$363,000, E3 and C3 C$452,000 and C$465,000, C2 and E2 above C$600,000. ||

Installed capital decides the ranking. A pump train, with its foundation, piping, valves, motor and wiring, costs about C$122,000 installed for a 100% pump and C$110,000 for a 50% pump; the smaller pump saves little, because much of a train's cost does not depend on its size. Three 50% trains therefore cost about C$85,000 more than two 100% trains. The parallel arrangements' energy savings at turndown do not recover it, and their extra repairs add another C$15,000 in present value.

Between the two single-pump options, the drives beat the valve because they replace it: two drives cost about C$14,000 installed against C$27,500 for a control valve with its block and bypass valves, and they save about C$900 a year of electricity. The mean regret, the expected cost of having chosen an arrangement other than the best, is C$700 for B, C$19,000 for A and C$108,000 or more for the parallel arrangements.

## What Changes the Answer

For this service, little does. Rank correlations between the uncertain inputs and the cost difference between options show what moves it. Between E3 and B, the installed cost factor (0.60) dominates, followed by the share of time at turndown (−0.21), the repair cost (0.18) and the pump failure rate (−0.13 against mean time between failures); electricity price hardly registers. Between B and A, the installed cost factors of pumps and drives dominate (−0.51 and 0.29).

**Keeping the control valve.** Many owners keep a control valve with a drive, for faster response or a simpler failure mode. Then B carries both costs, averages C$372,000, and beats A in only 8% of scenarios. The drive pays here because it replaces the valve; added to a valve, it does not.

**Drive cost and what the model leaves out.** Each drive is costed at about C$7,100 installed. B stays cheaper than A on average until a drive costs about C$16,300 installed, 2.3 times the estimate; at twice the estimate B is cheapest in 66% of scenarios, and at three times in 14%. Drives in a hazardous area can cost that much: the motor must be certified for converter duty with thermal protection, the cable is shielded, and a large site may need harmonic filtering. The model also leaves out drive trips on voltage dips, which can stop both drives at once, and the trip or isolation valve that may still be needed once the control valve goes. Price the drives with these in before removing the valve.

**Time at turndown.** In the median scenario, raising the share of hours at turndown from 0% to 75% does not change the cheapest arrangement for this duty. Over the full set of scenarios, B is cheapest in 92% with half the hours at turndown and in 58% with 80%, where E2 takes 36%: at turndown one 50% pump carries the whole demand, so the missing spare costs little. Even with half the hours at turndown, E3 still draws 0.3 kW more than B on average, and C3 only 0.1 kW less than A. A third train costs about C$8,600 a year in capital charges alone.

**Pump curve shape.** A flatter curve, shutoff at 1.10 times rated head, and a steeper one, at 1.35 times, change the rated head by less than 0.4 m. They change the electrical power of A at turndown, from 4.25 kW to 4.99 kW, and the shutoff head, from 91 m to 111 m, which moves the design pressure. They change the drive results by less than 0.1 kW and those of C by up to 0.14 kW. Re-run over all 5,000 scenarios, B is cheapest in 96% with the flatter curve and in 97% with the steeper one.

**Duty size.** The answer changes for a much larger service. Figure 6 scales the flow at the same head up to 50 times. Pump efficiency rises with size along an illustrative curve shaped after Hydraulic Institute charts (40% at this duty, 74% at 160 m³/h and 78% at 320 m³/h), motors are sized to API 610 at each size, capital follows the cost correlations, repairs grow with size to the power 0.4 and lost production with the size of the plant. With turndown for up to a quarter of the hours, B remains cheapest in at least 86% of scenarios up to about 35 kW; above about 40 kW, E3 is cheapest in 10% to 40% of them. With half the hours at turndown, E3 overtakes B above about 30 kW. The lines step up and down because a pump size can just miss a motor frame, so read them as a band. Larger pumps are nearly as efficient at half size as at full size, their energy is worth more, and a train's fixed cost matters less.

FIG fig6-probability-by-size || Probability that B, E3 and A are cheapest against the size of the duty, shown as the average electrical power of option B over the year in the base case, with turndown for up to 25% of hours and for half the hours. || Lines of probability cheapest against duty size from 4 to 110 kW: B above 86% up to about 35 kW, then stepping between 30% and 86%; with half the hours at turndown E3 is cheapest in most scenarios above about 30 kW. ||

A deeper turndown, to 25% of design rate for half the hours, where the single pumps need recirculation, still leaves B cheapest in 95% of scenarios at this duty, but from about 65 kW E3 is cheapest in three-quarters of them. Recirculation costs energy; at a few kilowatts it costs far less than a third pump train, at a large duty it does not.

## Decision Guide

For small, continuous, high-static pump services with a cost structure like this one, start from one 100% pump and an installed spare, and add drives only if they let you remove the control valve. Table 5 is screening guidance: it sets out when another arrangement deserves a full comparison.

TABLE When to test another arrangement against option B (screening guidance).
| Situation | Arrangement to test against B | Why |
| Duty above about 30 kW with long periods at reduced rate, or above about 40 kW | E3: 2 × 50% with spare, drives | Energy at turndown starts to outweigh the third train |
| Turndown below the single pump's stable flow for long periods | E3, or B with recirculation | Recirculation is cheap at small duties and costly at large ones |
| Fast flow response, or a valve needed to isolate or trip | A: 1 × 100% with spare, valve | A drive added to a valve does not pay |
| Losing the service stops the plant and restart is very costly | B or E3 with a spare; never a no-spare option | Both keep losses under an hour a year |
| No room or budget for a spare, and 75% capacity is acceptable for days | C2 or E2, with a cost for running at reduced rate | Only if lost production is worth little |
| One lead pump on a drive with fixed-speed lag pumps | Check the minimum flow of the lead pump first | It falls into a flow gap unless the system curve is very flat |
| Installed drive cost more than about twice the budget price | A: 1 × 100% with spare, valve | B's advantage over A is gone at about 2.3 times |

Five steps turn the guide into a decision for a particular service.

1. **Reuse the rated point.** Size the duty with the Monte Carlo method of the earlier paper, so every arrangement is compared at the same coverage.
2. **Solve each arrangement over the operating cases.** Include the turndown cases, the staging rule and the minimum stable flow of every pump.
3. **Count trains, not just pumps.** Installed cost per train, including its foundation, piping, valves and electrical work, decides most comparisons at small duties.
4. **Simulate failures with the plant's own data.** Use the maintenance records of similar pumps for failure and repair times, and price a lost hour of production with the plant's margin.
5. **Report the probability each option is cheapest and its regret.** A mean life-cycle cost hides how often the choice would be wrong.

### 9.1 Pitfalls

- **Comparing arrangements at different coverage.** A 2 × 50% design sized with extra margin is not comparable with a lean 1 × 100% design. Rate both to the same percentile.
- **Counting the efficiency gain at turndown and not the loss at normal rate.** Smaller pumps are less efficient, and normal operation usually has most of the hours.
- **Forgetting that two running pumps fail ****almost ****twice as often.** Redundancy reduces the cost of each failure but increases how many there are.
- **Leaving the valve in.** A drive that does not replace the control valve adds cost without removing the larger one.
- **Mixing fixed-speed and variable-speed pumps without checking the lead pump's flow.** The variable-speed pump can be pushed below its minimum flow.

## Conclusions

For the small reactor feed service of a 50,000-tonne-a-year chemical plant, about 5 kW, one 100% pump with an installed spare, both on variable-speed drives and with no control valve, is the arrangement to choose.

- It has the lowest 20-year life-cycle cost in 96% of 5,000 scenarios, C$344,000 on average, and its mean regret is C$700.
- One 100% pump on a control valve costs about C$18,000 more. If the valve is kept beside the drives, or the drives cost more than about twice the budget price, the drives no longer pay.
- Two 50% pumps keep the running pump near its best-efficiency point at turndown and lose the least production, but they need a third installed train and fail almost twice as often. With a spare they cost C$452,000 to C$465,000; without one, C$609,000 to C$634,000.
- Turndown up to half the hours, electricity price and pump curve shape do not change the ranking for this duty. Installed cost, repair cost and failure rate move the margins most.
- Two 50% pumps on drives begin to compete above about 30 kW with long periods at reduced rate. A drive on the lead pump only, with fixed-speed lag pumps, falls into a flow gap.

The case has limits. The pump curves, the efficiencies and the cost correlations are generic, the reliability inputs are industry benchmarks rather than this plant's records, and the scaling to larger duties keeps the head and layout of this service. The drive costs leave out converter-duty motor premiums, harmonic filtering and trips on voltage dips. The off-region failure penalty is the same however far from the preferred region a pump runs, which slightly favours the single pumps, and the capacity of one 50% pump ignores the drop across the wide-open valve. Lost production is valued at the product margin only. The method transfers to any pump service: the Python model and an Excel template can be downloaded from this paper's page.

## Appendix: Running the Comparison for Your Own Service

Table 6 sets out the comparison in steps, with what this paper did and where the downloadable model does it. The script below reproduces the average powers of Figure 3 for A, B, C and E from the same 20,000 cases; the full model adds the reliability simulation, the economic scenarios and the scaling to other duties.

TABLE Steps of the comparison, with this paper's choices and the model function that does each.
| Step | What to do | In this paper | In the model |
| 1. Rate the duty | Size the 100% pump to a chosen percentile of the operating cases | P95: 10.68 m³/h at 82.5 m | rated_point() |
| 2. Define the arrangements | Number of pumps, spares, control by valve or speed, staging rule | Six ranked, one variant (Table 1) | OPTIONS |
| 3. Solve every case | Operating point, efficiency, share of best-efficiency flow, recirculation | Normal and 50% turndown, Eq. (1) and (2) | run_option() |
| 4. Simulate failures | Failure rates with the off-region penalty, repairs, standby starts, lost production | 20 years, 5,000 scenarios, Eq. (3) | simulate() |
| 5. Cost every scenario | Installed capital and present value of electricity, repairs and lost production | Eq. (4), Table 2 | econ() |
| 6. Rank and test | Probability cheapest, regret, the inputs that move the margins, duty size | Sections 7 and 8 | R["econ"], R["drivers"], R["p_by_size"] |

CODE appendix || Average electrical power of arrangements A, B, C and E over the 20,000 operating cases at normal rate and at 50% turndown (Python 3 with NumPy and SciPy)."""
