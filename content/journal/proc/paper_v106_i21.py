"""Chmltech Online Journal, Vol. 106, Issue 21: Sizing the Feed Preheater Under Fouling Uncertainty: Area Margin, Cleaning and Condensate Stall (Nov 27 2026).

Worked case: the feed preheater E-101 of Issues 8 and 9, 500 fouling scenarios (Kern-Seaton, uncertain level and speed)
followed through a 24-month run over the 300 Issue 8 operating cases, areas 4 to 12 m2, rate cuts, unplanned cleanings
and condensate stall. Model: content/journal/proc/models/preheater/."""

SLUG = "sizing-the-feed-preheater-under-fouling-uncertainty-area-margin-cleaning-and-condensate-stall"
META = dict(
    volume=106, issue=21,
    title='Sizing the Feed Preheater Under Fouling Uncertainty: Area Margin, Cleaning and Condensate Stall',
    short_title='Sizing the Feed Preheater Under Fouling Uncertainty',
    meta='A Monte Carlo sizing of a steam feed preheater under fouling: TEMA plus 20% still needs cleaning; 8 to 9 m² stops it but the clean shell stalls at low load.',
    keywords=['heat exchanger design', 'fouling', 'Monte Carlo simulation', 'condensate stall', 'steam heater', 'TEMA fouling factor', 'Kern–Seaton model', 'life-cycle cost'],
)
DIVISION = "Division of Clean Energy Technology Innovation"
ABSTRACT = "A steam-heated feed preheater is usually sized for one design case with a TEMA fouling factor and a margin of 10% to 20%. This paper sizes the preheater E-101 of the Chmltech 50,000-tonne-a-year plant under uncertainty instead. A Monte Carlo model follows 500 fouling scenarios, with Kern–Seaton fouling of uncertain level and speed, through a 24-month run over 300 operating cases that follow the seasons. For each area it finds the rate cuts when the steam cannot reach the temperature needed, the unplanned cleanings that follow, and the hours the shell would need to run below atmospheric pressure, when condensate stops draining through the trap. With an asymptotic fouling resistance judged at 1 to 8 × 10⁻⁴ m²K/W, against TEMA's 1.76 × 10⁻⁴, the TEMA area of 5.4 m² needs about two unplanned cleanings a year, at an expected cost near C$300,000 a year; TEMA plus 20% needs one every two years. At 8 to 9 m² rate cuts become rare, and the extra area costs about C$3,000, because a small exchanger's cost is mostly fixed. The price is stall: with a free-draining atmospheric return, the 8 m² shell runs below atmospheric pressure for a quarter of the hours at normal rate and two-thirds at turndown. The fouling level and the tube-side coefficient decide most of the outcome. The paper recommends sizing for fouling and designing the condensate system for sub-atmospheric operation."

REFS = {
    'badar': ('Badar, M. A., Zubair, S. M., &amp; Sheikh, A. K. (1993). Uncertainty analysis of heat-exchanger thermal designs using the Monte Carlo simulation technique. <em>Energy, 18</em>(8), 859–866.',
        'https://doi.org/10.1016/0360-5442(93)90063-J'),
    'bergman': ('Bergman, T. L., Lavine, A. S., Incropera, F. P., &amp; DeWitt, D. P. (2011). <em>Fundamentals of heat and mass transfer</em> (7th ed.). Wiley.',
        ''),
    'bott': ('Bott, T. R. (1995). <em>Fouling of heat exchangers</em>. Elsevier.',
        ''),
    'gnielinski': ('Gnielinski, V. (1976). New equations for heat and mass transfer in turbulent pipe and channel flow. <em>International Chemical Engineering, 16</em>(2), 359–368.',
        ''),
    'hand': ('Hand, W. E. (1958). From flow sheet to cost estimate. <em>Petroleum Refiner, 37</em>(9), 331–334.',
        ''),
    'kern': ('Kern, D. Q. (1966). Heat exchanger design for fouling services. In <em>Proceedings of the Third International Heat Transfer Conference</em> (pp. 170–178), Chicago.',
        'https://doi.org/10.1615/IHTC3.830'),
    'kernseaton': ('Kern, D. Q., &amp; Seaton, R. E. (1959). A theoretical analysis of thermal surface fouling. <em>British Chemical Engineering, 4</em>(5), 258–262.',
        ''),
    'hxpost': ('Lee, Q. F. (2026). Sizing a heat exchanger: Duty, LMTD and area, worked step by step. <em>Chmltech Insights</em>.',
        'https://www.chmltech.com/post/sizing-a-heat-exchanger-duty-lmtd-and-area.html'),
    'hazop': ('Lee, Q. F. (2026). A worked HAZOP: The feed heater, node by node. <em>Chmltech Insights</em>.',
        'https://www.chmltech.com/post/a-worked-hazop-the-feed-heater-node-by-node.html'),
    'pv': ('Lee, Q. F. (2026). Sizing pumps and control valves under uncertainty: Monte Carlo design points for chemical plants. <em>Chmltech Online Journal, 106</em>(8).',
        'https://www.chmltech.com/post/sizing-pumps-and-control-valves-under-uncertainty-monte-carlo-design-points-for-chemical-plants.html'),
    'arr': ('Lee, Q. F. (2026). Choosing the pump arrangement under uncertainty: Monte Carlo comparison of single, parallel and variable-speed options. <em>Chmltech Online Journal, 106</em>(9).',
        'https://www.chmltech.com/post/choosing-the-pump-arrangement-under-uncertainty-monte-carlo-comparison-of-single-parallel-and-variable-speed-options.html'),
    'ms': ('Müller-Steinhagen, H. (2011). Heat transfer fouling: 50 years after the Kern and Seaton model. <em>Heat Transfer Engineering, 32</em>(1), 1–13.',
        'https://doi.org/10.1080/01457632.2010.505127'),
    'msm': ('Müller-Steinhagen, H., Malayeri, M. R., &amp; Watkinson, A. P. (2011). Heat exchanger fouling: Mitigation and cleaning strategies. <em>Heat Transfer Engineering, 32</em>(3–4), 189–196.',
        'https://doi.org/10.1080/01457632.2010.503108'),
    'nesta': ('Nesta, J. M., &amp; Bennett, C. A. (2005). Fouling mitigation by design. In <em>Heat Exchanger Fouling and Cleaning – Challenges and Opportunities</em> (ECI Symposium Series, Vol. RP2), Kloster Irsee, Germany. Engineering Conferences International.',
        ''),
    'shah': ('Shah, R. K., &amp; Sekulić, D. P. (2003). <em>Fundamentals of heat exchanger design</em>. Wiley.',
        ''),
    'sieder': ('Sieder, E. N., &amp; Tate, G. E. (1936). Heat transfer and pressure drop of liquids in tubes. <em>Industrial &amp; Engineering Chemistry, 28</em>(12), 1429–1435.',
        'https://doi.org/10.1021/ie50324a027'),
    'ssa': ('Spirax Sarco. (n.d.-a). Heat exchangers and stall. <em>Learn about steam</em>.',
        'https://www.spiraxsarco.com/learn-about-steam/condensate-removal/heat-exchangers-and-stall'),
    'ssb': ('Spirax Sarco. (n.d.-b). Oversized heat exchangers. <em>Learn about steam</em>.',
        'https://www.spiraxsarco.com/learn-about-steam/condensate-removal/oversized-heat-exchangers'),
    'ssc': ('Spirax Sarco. (n.d.-c). Practical methods of preventing stall. <em>Learn about steam</em>.',
        'https://www.spiraxsarco.com/learn-about-steam/condensate-removal/practical-methods-of-preventing-stall'),
    'tema': ('Tubular Exchanger Manufacturers Association. (2019). <em>Standards of the Tubular Exchanger Manufacturers Association</em> (10th ed.). TEMA.',
        ''),
    'towler': ('Towler, G., &amp; Sinnott, R. (2013). <em>Chemical engineering design: Principles, practice and economics of plant and process design</em> (2nd ed.). Butterworth-Heinemann.',
        ''),
    'zubair92': ('Zubair, S. M., Sheikh, A. K., &amp; Shaik, M. N. (1992). A probabilistic approach to the maintenance of heat-transfer equipment subject to fouling. <em>Energy, 17</em>(8), 769–776.',
        'https://doi.org/10.1016/0360-5442(92)90120-O'),
    'zubair00': ('Zubair, S. M., Sheikh, A. K., Younas, M., &amp; Budair, M. O. (2000). A risk based heat exchanger analysis subject to fouling: Part I: Performance evaluation. <em>Energy, 25</em>(5), 427–443.',
        ''),
}

CODE = {"appendix": open(__file__.replace("paper_v106_i21.py", "models/preheater/hx_appendix.py"), encoding="utf-8").read().rstrip()}

DOWNLOADS = [  # served from assets/journal/code/
    dict(file='preheater_appendix.py', label='Appendix script', note='Clean and TEMA design areas and the shell pressure needed clean and fouled (Python 3, NumPy)'),
    dict(file='chmltech-preheater-fouling-model.zip', label='Full model', note='Fouling run simulation, rate cuts, cleanings, stall, costs, sensitivity runs and the Issue 8 model it builds on, README'),
    dict(file='chmltech-preheater-fouling-template.xlsx', label='Excel template', note='Live calculator: design areas, Kern-Seaton fouling curve and shell pressure by area and load with rate-cut and stall flags; stored Monte Carlo results'),
]

BODY = r"""
## Introduction

The feed preheater E-101 heats the reactor feed of the Chmltech plant from tank temperature to 80 °C with low-pressure steam. The earlier Insights post sized it in the usual way: the duty at the design flow, the log-mean temperature difference against steam at 3.0 barg, an assumed overall coefficient, and 20% on top for fouling [@hxpost]. The HAZOP of the same heater then asked what happens on loss of steam, high steam pressure and a blocked condensate line [@hazop]. Neither asked how the heater behaves over a run as its tubes foul, or at the low loads it will spend part of its life at.

Those two questions pull the area in opposite directions. Fouling builds up on the tube side over months; when the steam can no longer reach the temperature needed, the plant must cut rate or take the exchanger out for cleaning. More area delays that day. But a steam heater controlled by a valve on the steam line runs its shell at whatever pressure the load needs, and a large, clean exchanger at low load needs very little. When the shell pressure falls to the condensate back pressure, condensate stops draining through the trap, floods the bottom of the shell and the control becomes erratic, a condition called stall [@ssa]. More area brings that day closer.

Fouling factors were never meant to carry this much. The TEMA values are a fixed resistance for one design point, the subject of decades of criticism because they hide a time-dependent process in a single number [@kern, @ms]. Probabilistic treatments of fouling in design and maintenance go back to the work of Zubair and colleagues [@zubair92, @badar, @zubair00], but they rarely reach the small exchangers of a small plant, and they seldom count stall as a cost of oversizing.

This paper follows the earlier Monte Carlo papers of the series, which sized the feed pump and control valve [@pv] and chose the pump arrangement [@arr] under uncertainty. It asks four questions about E-101: how much area the uncertain fouling calls for, what an undersized exchanger costs in rate cuts and cleaning, how often a larger one would stall, and which uncertainties drive the answer. It then sets out how the condensate system can be designed so that the margin the fouling needs does no harm.

## The Preheater and Its Uncertainties

E-101 is a shell-and-tube exchanger with the feed on the tube side and low-pressure steam condensing on the shell side. A control valve on the steam line holds the feed outlet at 80 °C; condensate leaves through a trap to an atmospheric return. Table 1 gives the fixed design data. The tubes are 3/4-inch, 16 BWG carbon steel, 12 to a pass, which gives about 1.2 m/s at the median feed rate; the area is set by the tube length, with two passes up to 6.1 m tubes and four passes above that, so that the tube-side velocity, and with it the clean coefficient, is the same for every area studied.

TABLE Design data of E-101.
| Item | Value | Source |
| Feed | Organic blend, cp 2.0 kJ/kg·K, k 0.13 W/m·K, viscosity 1.6 mPa·s at 20 °C | Issue 8 fluid model |
| Feed rate | Median 8,690 kg/h, P95 9,570 kg/h, half that at turndown | Issue 8 operating cases |
| Feed inlet temperature | 5 to 40 °C, outdoor tank (P5 6.8 °C) | Issue 8 |
| Outlet temperature | 80 °C | Design basis |
| Duty | Median 277 kW, P95 362 kW | Issue 8 cases |
| Steam | 3.0 barg header, 0.3 bar across the control valve at full opening | Design basis |
| Condensate | Trap to an atmospheric return | Design basis |
| Tubes | 19.05 mm OD, 15.75 mm ID, carbon steel, 12 per pass | Common practice |
| Run between turnarounds | 24 months, 8,000 operating hours a year | Plant plan |

The feed cases come from the earlier pump and control valve paper, Issue 8 of this volume [@pv]. Its 300 sampled cases carry the uncertainty in production rate, recycle ratio and tank temperature, and they set the flow and inlet temperature the heater sees. The feed flow there, 8,690 kg/h at the median, is larger than the 6,250 kg/h used in the Insights post because it includes the recycle and the reactor yield; the median duty is 277 kW instead of 208 kW.

The uncertainties of the exchanger itself are in Table 2. The most important is fouling. The feed is a light organic blend with traces of polymerising and particulate matter, and its fouling is expected to follow the asymptotic shape described by Kern and Seaton, rising quickly at first and levelling off as removal balances deposition [@kernseaton, @bott]. Neither the level nor the speed is known before the plant runs. The asymptotic resistance ranges from 1 to 8 × 10⁻⁴ m²K/W with a most likely 3 × 10⁻⁴, against the TEMA value of 0.001 h·ft²·°F/Btu (1.76 × 10⁻⁴ m²K/W) typical of organic process liquids [@tema]; the time constant ranges from 1,000 to 8,000 operating hours. The clean tube-side coefficient carries the scatter of the Gnielinski correlation [@gnielinski], and the condensing coefficient the usual spread for steam with some non-condensable gas.

TABLE Uncertain inputs (triangular unless stated).
| Input | Low | Most likely | High | Basis |
| Asymptotic fouling resistance, tube side (10⁻⁴ m²K/W) | 1.0 | 3.0 | 8.0 | Organic feed with polymer traces; TEMA value 1.76 |
| Fouling time constant (operating hours) | 1,000 | 3,000 | 8,000 | Asymptotic fouling of organics |
| Tube-side coefficient factor | Lognormal, mean 1.0, σ 0.15 |  |  | Correlation scatter |
| Condensing coefficient (W/m²K) | 5,000 | 8,000 | 12,000 | Steam with some non-condensables |
| Steam header pressure (barg) | 2.6 | 3.0 | 3.2 | Utility variation |
| Product margin (C$/t) | 150 | 300 | 500 | Plant economics, as Issue 9 [@arr] |
| Share of hours at 50% turndown | Uniform 0 |  | 0.25 | Operating plan, as Issue 9 |

A steam-side fouling resistance of 1 × 10⁻⁴ m²K/W is held fixed. Each scenario draws one value of every input and keeps it for the whole run; the 300 feed cases are then run through it month by month.

## Method

**Heat transfer.** The overall coefficient on the outside tube area is Eq. (1), where hi is the tube-side coefficient on the inside area, Do and Di the tube diameters, Rw the wall resistance, ho the condensing coefficient and Rfi and Rfo the fouling resistances inside and outside. The tube-side coefficient comes from the Gnielinski correlation [@gnielinski]; the lowest Reynolds number, at turndown with the coldest feed, is about 6,500, so no case is laminar:

TEX \frac{1}{U} = \frac{D_o}{h_i D_i} + R_w + \frac{1}{h_o} + R_{fi}\frac{D_o}{D_i} + R_{fo}

**Steam temperature needed.** With the shell at a uniform condensing temperature, the steam temperature that just heats the feed to its set point is Eq. (2), where NTU = UA/(ṁ cp) [@shah]; the control valve sets the shell pressure to the saturation pressure at that temperature:

TEX T_{s,req} = \frac{T_{out} - T_{in}\,e^{-NTU}}{1 - e^{-NTU}}, \qquad NTU = \frac{U A}{\dot m\,c_p}

**Fouling.** The tube-side fouling resistance grows over the run as Eq. (3), with t the operating time since the last cleaning, R∞ the asymptotic resistance and τ the time constant [@kernseaton]. Section 6 replaces it with linear growth at the same initial rate to test the shape:

TEX R_{fi}(t) = R_\infty \left( 1 - e^{-t/\tau} \right)

**Rate cut.** The highest steam temperature available is the saturation temperature at the header pressure less the 0.3 bar the control valve needs. When Eq. (2) asks for more, the plant must cut its feed rate to what the exchanger can heat to 80 °C at full steam, Eq. (4), found by iteration because U falls with the flow:

TEX \dot m_{max} = \frac{U(\dot m_{max})\,A}{c_p \ln\!\left[ (T_{s,max} - T_{in}) / (T_{s,max} - T_{out}) \right]}

The production lost is the fraction 1 − ṁmax/ṁ for that case.

**Stall.** When Eq. (2) asks for a steam temperature below the saturation temperature at the condensate back pressure, the trap has no pressure difference to discharge into the return, and condensate backs up [@ssa]. In the base case the return is atmospheric and free-draining, so the threshold is 0 barg, 100 °C. This ignores the back pressure of the return line and the trap's own differential, which raise the shell pressure at which stall begins, and any static head under the trap, which lowers it; Section 6 tests back pressures of 0.1 and 0.3 bar. The model counts the share of operating hours in stall, separately at normal rate and at turndown. It does not model what follows, the flooding of the shell and its effect on control; Section 7 deals with that.

**The run.** Each scenario is followed in half-month steps through a 24-month run between turnarounds, at normal rate and at 50% turndown. The 300 feed cases are sorted by tank temperature into 24 groups, and each step uses the group that matches its season, so the run passes through a cold and a warm season each year; the month of the turnaround varies between scenarios. A rate cut is counted when the expected lost production in a step exceeds 0.1%. When it exceeds 1%, the operators take the exchanger out for an unplanned cleaning: the plant loses half a step at the reduced rate, then 36 hours of production to remove the channel and floating-head covers, hydroblast the straight tubes and restart, at a direct cost of C$25,000, and the fouling starts again from zero. Lost production is valued at the scenario's product margin on 6.25 t/h, on half that rate during turndown. The half-month step limits the model to 24 cleanings a year, far above any area of interest.

**Cost.** A fouling tube-side fluid needs straight tubes that can be cleaned mechanically, so the exchanger is costed as a carbon steel floating-head unit with the Towler and Sinnott correlation, whose January 2010 US Gulf Coast basis is escalated to 2025 with a CEPCI of about 810 and converted at 1.38 C$/US$ (a factor of 2.10, as in Issue 8), then multiplied by a Hand installation factor of 3.5 [@towler, @hand], as in the earlier papers. The correlation's lower limit is 10 m²; below it the cost is scaled linearly, which keeps the fixed part of the cost. It is annualised at 8% over 20 years. The total annual cost of an area is that capital charge plus the rate-cut losses and the unplanned cleanings, averaged over the scenarios.

**Design points.** For comparison, the conventional design is worked at a single design case: the P95 feed rate, the P5 inlet temperature and 2.7 barg in the shell. The clean area at that case is 4.16 m² with U of 1,006 W/m²K; with the TEMA fouling resistances of 1.76 × 10⁻⁴ on the tube side and 0.88 × 10⁻⁴ on the shell side it is 5.42 m² with U of 772 W/m²K, and 6.50 m² with 20% added. The Insights post, with an assumed U of 500 W/m²K and the lower flow, found 4.61 m² [@hxpost].

**Verification.** At the median feed case the Gnielinski coefficient, 1,443 W/m²K, is 5% above the Dittus–Boelter value of 1,375 W/m²K [@bergman], within the scatter of the two correlations. The appendix script reproduces the design areas to within 0.01 m² from the equations alone, and the pattern of Figure 3: the clean 8 m² shell below atmospheric at both loads, the fouled one well within the steam available. With 500 scenarios the chance of a rate cut at 8 m² carries a standard error of about 1 percentage point.

## Results: Fouling Sets the Area

Figure 1 shows the fouling the model expects. In the median scenario the tube-side resistance passes the TEMA value of 1.76 × 10⁻⁴ m²K/W within four months and levels off near 3.7 × 10⁻⁴ by the end of a two-year run; in one scenario in ten it reaches 6 × 10⁻⁴. The TEMA value is a fair estimate of the fouling a few months into the run, not of what the exchanger will carry for most of it.

FIG fig1-fouling-over-a-run || Tube-side fouling resistance over a 24-month run: median and P10 to P90 band of the 500 scenarios, with the TEMA design value. || Tube-side fouling resistance over a 24-month run: the median of 500 scenarios passes the TEMA value of 1.76 × 10⁻⁴ m²K/W within four months and levels off near 3.7 × 10⁻⁴; the P90 reaches about 6 × 10⁻⁴. ||

Table 3 and Figure 2 give the consequences for each area. An exchanger of 4 m², just under the clean design area, would be out for cleaning about once a month. At the TEMA area of 5.42 m² there is a 90% chance of a rate cut within the run and 2.1 unplanned cleanings a year on average, at an expected cost of C$298,000 a year once the lost production is counted; the P95 is C$1.1 million. Adding 20%, the margin many designers apply, brings the expected cost to C$77,000 a year, still three times the capital charge of the exchanger, with one cleaning every two years and an even chance of a rate cut in each run. The cost falls steeply until about 8 m², where a rate cut happens in one run in sixteen and the expected cost is within C$3,500 of its floor. At 9 m² one scenario in 500 needs a rate cut and none needs a cleaning.

TABLE Results by heat-transfer area over a 24-month run (means of 500 scenarios unless stated).
| Area (m²) | Tubes, passes, length (m) | Installed cost (C$k) | Unplanned cleanings a year | Chance of a rate cut in the run | Total annual cost, mean (C$k) | Total annual cost, P95 (C$k) | Stall share, normal-rate hours | Stall share, turndown hours |
| 4 | 24, 2, 2.8 | 238 | 10.9 | 100% | 2,151 | 4,251 | 0% | 0.2% |
| 5 | 24, 2, 3.5 | 239 | 3.8 | 98% | 561 | 1,781 | 0.1% | 7% |
| 5.42 (TEMA) | 24, 2, 3.8 | 239 | 2.1 | 90% | 298 | 1,074 | 0.6% | 14% |
| 6 | 24, 2, 4.2 | 240 | 0.93 | 73% | 135 | 390 | 2.3% | 27% |
| 6.5 (TEMA + 20%) | 24, 2, 4.5 | 240 | 0.46 | 52% | 77 | 192 | 5.5% | 38% |
| 7 | 24, 2, 4.9 | 241 | 0.23 | 33% | 50 | 149 | 11% | 48% |
| 8 | 24, 2, 5.6 | 241 | 0.03 | 6.4% | 28.1 | 62.5 | 25% | 67% |
| 9 | 48, 4, 3.1 | 242 | 0 | 0.2% | 24.7 | 24.7 | 42% | 83% |
| 10 | 48, 4, 3.5 | 243 | 0 | 0% | 24.8 | 24.8 | 59% | 94% |
| 12 | 48, 4, 4.2 | 245 | 0 | 0% | 25.0 | 25.0 | 85% | 99.7% |

The reason the answer is so lopsided is the shape of the cost. Under the cost correlation, extra area is almost free on an exchanger this small: going from 5.4 to 9 m² adds about C$3,000 to an installed cost of C$240,000, because the shell, heads, nozzles and installation cost the same and only the tubes grow longer. Even with the cost of area ten times what the correlation gives, 9 m² remains the cheapest area. A cleaning, on the other hand, costs C$25,000 plus 36 hours of a plant earning about C$1,900 an hour, some C$90,000 at the most likely margin, more than a third of the price of the exchanger. With the cost of area this low, the area is set not by an optimum but by the point where cleaning stops: for this feed's assumed fouling range, 8 to 9 m², 1.5 to 1.7 times the TEMA area. A feed judged to foul less would need less; the method, not the ratio, is what transfers.

FIG fig2-annual-cost-against-area || Expected annual cost against heat-transfer area, with its parts and the P95 total, and the clean, TEMA and TEMA plus 20% design areas. || Expected annual cost against heat-transfer area from 4 to 12 m², split into capital charge, cleanings and lost production, with the P95 total: steep fall from C$2.2 million at 4 m² to about C$25,000 from 9 m², with the clean, TEMA and TEMA plus 20% areas marked. ||

## The Other Side of the Margin: Condensate Stall

Area that the fouled exchanger needs is area the clean exchanger does not. The control valve answers by throttling the steam, and the shell pressure falls. Figure 3 follows the shell pressure the median scenario needs over a run. A 6 m² exchanger starts at 0.2 barg and climbs to 1.3 barg as it fouls, always above atmospheric at normal rate. An 8 m² exchanger starts at −0.17 barg, crosses atmospheric pressure after three months and ends at 0.35 barg. A 10 m² exchanger stays below atmospheric for the whole run. At turndown, half the flow needs much less steam: even the 6 m² exchanger starts below atmospheric, and the 8 and 10 m² exchangers never leave it.

FIG fig3-steam-pressure-over-a-run || Shell-side steam pressure needed over a 24-month run for 6, 8 and 10 m², at normal rate and at 50% turndown, against the highest pressure available and atmospheric pressure (the scenario with the median asymptotic fouling resistance: R∞ 3.8 × 10⁻⁴ m²K/W, τ 4,100 h, tube-side factor 1.08; median feed case, 8,690 kg/h at 22.5 °C). || Shell-side steam pressure needed over a 24-month run for 6, 8 and 10 m², at normal rate and at turndown: 6 m² climbs from 0.2 to 1.3 barg, 8 m² starts below atmospheric and crosses it after three months, 10 m² stays below atmospheric; at turndown 8 and 10 m² never leave it. ||

Below atmospheric pressure the trap has no pressure difference to push condensate into an atmospheric return, so condensate backs up into the shell [@ssa]. The flooded tubes stop condensing, the effective area falls, and the outlet temperature drops until the control valve opens far enough to raise the shell pressure and blow the condensate out; then the cycle repeats. The symptoms are familiar to anyone who has run a steam heater at low load: a hunting outlet temperature, water hammer in the shell and the condensate line, carbonic acid corrosion where condensate stands, and thermal cycling of the tubesheet and the lower tubes [@ssb, @ssc].

Figure 4 sets the two failures against each other across the range of areas. The chance of a rate cut within a run falls from certainty at 4 m² to 6% at 8 m² and nil from 10 m². The share of hours in stall rises the other way: at normal rate from nothing below 5 m² to 25% at 8 m² and 59% at 10 m², and at turndown from 14% at the TEMA area to 67% at 8 m² and nearly all the time from 10 m². No area avoids both. Even the TEMA area, which fouls out within months, stalls for one turndown hour in seven, because every run starts with clean tubes. With any back pressure on the return the stall shares are larger (Section 6).

FIG fig4-rate-cut-against-stall || Chance of a rate cut within a 24-month run, with asymptotic and linear fouling, and share of operating hours in stall at normal rate and at turndown, against heat-transfer area. || Chance of a rate cut within a run falling from 100% at 4 m² to 6% at 8 m² and nil from 10 m² (much higher with linear fouling), while the share of hours in stall rises to 25% at normal rate and 67% at turndown at 8 m². ||

This is the result a single design case cannot show. Sizing for the fouled design case makes the clean exchanger too big for its load; sizing to keep the clean exchanger out of stall makes the fouled one too small. The conventional margin of 10% to 20% sits in the worst place: too small to stop cleaning, large enough to stall at low load. The two cannot be traded against each other by area alone; one of them has to be removed by design.

## What Drives the Result

Figure 5 ranks the inputs by their rank correlation with the total annual cost at 7 m², an area where both cleaning and stall are live. The asymptotic fouling resistance dominates, at +0.64. The factor on the tube-side coefficient comes next, at −0.42: the ordinary scatter of a heat-transfer correlation, about ±15%, carries two-thirds of the weight of the whole fouling range. The steam header pressure and the fouling time constant follow at −0.13 and −0.11; the product margin and the condensing coefficient matter little; and the share of hours at turndown not at all for cost, though it decides how much of the year the exchanger stalls.

FIG fig5-drivers || Rank correlation of each uncertain input with the total annual cost at 7 m². || Bar chart of rank correlation with total annual cost at 7 m²: asymptotic fouling resistance +0.64, tube-side coefficient factor −0.42, steam header pressure −0.13, fouling time constant −0.11, the other inputs near zero. ||

The ranking says where better information pays. The fouling level of this feed is the first unknown, and it can be measured before the design is frozen: a fouling probe or a heated test section on the pilot plant, or the record of a similar heater on the same feed, would narrow it far more than a better correlation would narrow the clean coefficient [@bott, @nesta]. Tube-side velocity is the lever the designer controls; the 1.2 m/s used here is at the low end of what is recommended for fouling organic service, and a higher velocity both raises the coefficient and lowers the asymptotic fouling, at the cost of pressure drop on the feed pump [@msm].

**The shape of fouling.** The model assumes fouling levels off. If instead the resistance keeps growing at its initial Kern–Seaton rate, the picture changes (Figure 4, dashed). This is a severe bound: by the end of a two-year run the median scenario reaches about 1.5 to 1.6 × 10⁻³ m²K/W, several times its asymptote. At 8 m² the chance of a rate cut in a run rises from 6% to 89%, with 0.7 unplanned cleanings a year and an expected cost of C$106,000 a year; even 10 m² needs a cleaning every two and a half years. Within the range studied, up to 10 m², linear fouling never stops cleaning; extra area only lengthens the interval. That case calls for a planned cleaning interval, with the area chosen to reach the next turnaround, and for the means to clean without a shutdown, such as a spare bundle or a second exchanger.

**Back pressure on the condensate.** Stall begins when the shell pressure falls to the back pressure the trap discharges against, not to atmospheric. With a net back pressure of 0.1 bar, from a modest lift or a long return line, the stall share at 8 m² rises from 25% to 36% at normal rate and from 67% to 77% at turndown; with 0.3 bar, to 53% and 90%. Even the TEMA area then stalls for 43% of the turndown hours. The more back pressure, the stronger the case for a pump-trap.

**The length of the run.** With turnarounds every 12 months instead of 24, the exchanger is cleaned before the fouling reaches its asymptote. At 7 m² the expected cost falls from C$50,000 to C$41,000 a year and the unplanned cleanings from 0.23 to 0.14 a year; at 8 m² the cost is C$26,000. (The chance of a rate cut per run, 16% instead of 33% at 7 m², is not directly comparable, because the shorter run has half the exposure.) A shorter run lowers the cost of a given area but hardly moves the area at which cleaning stops, 9 m² in both cases; it also raises the share of hours in stall, since the tubes are cleaner on average: at 8 m² from 25% to 33% at normal rate and from 67% to 73% at turndown.

## Designing Out Stall

Since area cannot remove both failures, the sensible design takes the area the fouling needs and removes stall by the arrangement of the steam and condensate side. Four arrangements are common; each has its own price [@ssc].

- **A pump-trap with a vacuum breaker.** Condensate drains by gravity from the shell into a pressure-powered pump that uses motive steam to push it into the return, whatever the shell pressure. A vacuum breaker on the shell lets the pressure fall to atmospheric rather than below it, so the condensate can always drain to the pump; the air it admits must be vented from the shell, or it blankets the tubes and adds oxygen corrosion. The exchanger and its control stay as they are; the cost is a packaged unit, the motive steam and enough height below the shell for the pump to fill. For E-101 this is the first choice: it keeps steam-side control, which responds fast, and it works at every area and load in Table 3.
- **A vacuum breaker and a gravity drain.** Where the condensate can fall freely to a vented receiver below the exchanger, a vacuum breaker and a trap with enough static head clear the condensate at any shell pressure down to atmospheric. It is cheap, but it cannot lift condensate into an overhead or pressurised return, and the air must be vented in the same way.
- **Control on the condensate side.** The control valve moves from the steam inlet to the condensate outlet. The shell runs at full steam pressure and the condensate level in it rises and falls to cover more or fewer tubes, so the exposed area follows the load. Stall cannot occur, but control is slower, the condensate leaves subcooled, and the shell must be designed to run partly flooded. Like bypass control below, it exposes the tubes above the condensate level to full steam temperature.
- **Bypass control on the feed side.** The steam is held at constant pressure and a three-way valve, or a bypass with a control valve, mixes heated and unheated feed to hold 80 °C. The exchanger never stalls. Two drawbacks matter for this feed: the tube wall runs hotter, and chemical reaction fouling of organics rises with surface temperature [@bott]; and the bypassed flow lowers the tube velocity, which raises fouling. The exchanger may foul faster than this model assumes, and the fouling inputs should be revisited if this arrangement, or condensate-side control, is chosen.

Two other options manage the problem rather than solve it. Two half-size exchangers in parallel, one taken out of service at turndown, bring the turndown stall down to the normal-rate share (about 25% instead of 67% at 8 m² in total) and allow cleaning on line, at the cost of a second shell, which on an exchanger this small roughly doubles the installed cost. A smaller exchanger with a spare bundle kept for a quick change accepts the cleanings of Table 3 and shortens each one, but it does not remove the stall at turndown.

Whichever is chosen, the HAZOP of the heater needs revisiting: a vacuum breaker, a pump-trap and a condensate-side valve each add deviations that the earlier study did not consider [@hazop].

## Decision Guide

Table 4 turns the results into rules for a steam-heated process preheater of this kind.

TABLE Sizing rules for a steam-heated preheater in fouling service.
| Situation | Do this | Why |
| Small exchanger, fouling service, area cheap next to a cleaning | Size for the area at which cleaning stops over the fouling range you expect, not for a TEMA factor plus a percentage: here 8 to 9 m² for this feed's assumed range | An unplanned cleaning costs more than a third of the exchanger; area costs almost nothing |
| Steam control on the inlet, wide load range | Add a pump-trap and vacuum breaker | The margin the fouling needs puts the clean shell below atmospheric at low load |
| Any back pressure on the condensate return | Expect stall in most hours at low load; design for it from the start | Stall begins at the return pressure, not at atmospheric |
| Fouling believed to level off, but its level unknown | Measure it before freezing the design: fouling probe, pilot test section, records of a similar heater | The asymptotic level is the largest single driver of cost |
| Fouling that may keep growing | Plan a cleaning interval, size for the run to the next turnaround, provide a spare bundle or second exchanger | No area studied stops cleaning |
| Feed that fouls faster on hot surfaces | Avoid bypass or condensate-side control at full steam pressure; keep tube velocity up | Higher wall temperature and lower velocity raise fouling |
| Fouling fluid on the tube side | Straight tubes: floating head or fixed tubesheet with removable channel covers | U-bends cannot be cleaned mechanically |
| A large exchanger, where area is expensive | Optimise the area against the cost of cleaning and lost production, as here, but expect a smaller margin | The flat cost curve of Figure 2 is a feature of small exchangers |

Five steps size a preheater in fouling service:

1. **Take the operating cases, not one design case.** Flow and inlet temperature come from the plant's own range, including turndown.
2. **Describe fouling as a curve with uncertain level and speed.** A single fouling factor hides both.
3. **Follow the run.** Find, month by month, when the steam runs out and when the shell drops below the condensate back pressure.
4. **Price the area, the cleanings and the lost production together.** On a small exchanger the cleaning side dominates.
5. **Design the condensate system for the area chosen.** Stall is a design choice, not a property of the exchanger.

### 8.1 Pitfalls

- **A TEMA fouling factor as the design margin.** It is a resistance for one point in time; this feed passes it within months.
- **A percentage margin on top.** It is too little to stop cleaning and enough to stall at low load.
- **Checking only the design case.** Stall happens at the opposite corner: clean tubes, low flow, warm feed.
- **A trap sized for full load only.** At low load the pressure across it falls to nothing; trap selection must follow the stall analysis [@ssa].
- **Assuming the fouling levels off without evidence.** If it does not, the area needed has no ceiling.

## Conclusions

The feed preheater of a small chemical plant was sized under uncertainty in its fouling, its heat-transfer coefficients, its steam supply and its operating range, following each fouling scenario through a two-year run:

- With an asymptotic fouling resistance judged at 1 to 8 × 10⁻⁴ m²K/W, the conventional area, TEMA fouling with 20% added, would leave the plant with an unplanned cleaning about every two years and an even chance of a rate cut in each run; the TEMA area alone, 2.1 cleanings a year and an expected cost of C$298,000 a year.
- At 8 to 9 m², 1.5 to 1.7 times the TEMA area, rate cuts become rare and the expected annual cost falls to its floor of about C$25,000, almost all of it the capital charge. Under the cost correlation the extra area costs about C$3,000, because a small exchanger's cost is mostly fixed; 9 m² stays cheapest even if area costs ten times more.
- With a free-draining atmospheric return, the same margin puts the shell below atmospheric pressure for 25% of the hours at normal rate and 67% at turndown at 8 m², and more with any back pressure. No area avoids both the rate cut and the stall; the condensate system must be designed for sub-atmospheric operation, with a pump-trap and vacuum breaker as the first choice for this heater.
- The asymptotic fouling resistance and the tube-side coefficient decide most of the outcome. If fouling keeps growing at its initial rate, no area studied avoids cleaning, and the design should be built around a planned cleaning interval.

The case has limits. The fouling ranges are judgement for an organic feed with polymer traces, not measurements on this feed, and the headline ratio of area to TEMA area follows from that judgement; fouling is applied uniformly to every tube, without the dependence on wall temperature and velocity that real fouling shows. The model counts the hours in stall but not their consequences for control or corrosion, and its stall threshold ignores static head under the trap. The 300 operating cases follow the seasons only through tank temperature; production rate and recycle are sampled within each step. The steam-side fouling is held at 1.0 × 10⁻⁴ m²K/W in the simulation, against TEMA's 0.88 × 10⁻⁴ at the design point, a difference of under 1% in U. The shell-side pressure drop, the feed pump head and the cost of the condensate equipment are not included; the installed-cost correlation is extrapolated below its 10 m² lower limit, although the conclusion holds for any cost of area within a factor of ten. At 12 tubes a pass (24 tubes) the 8 m² option is a long, thin shell, 5.6 m tubes in a shell of about 0.2 m; a hairpin exchanger or two shells in series would be the practical form. The Python model and an Excel template that applies the method to another exchanger can be downloaded from this paper's page.

## Appendix: Sizing Your Own Preheater for Fouling

Table 5 sets out the method in steps, with what this paper did and where the downloadable model does it. The script below applies Eqs. (1) and (2) with the fouling at its asymptote, the limit of Eq. (3): it finds the clean and TEMA design areas at the design case, and, for a chosen area, the shell pressure needed clean and fully fouled at the median feed case over 2,000 sampled fouling levels. For 8 m² it shows that the fully fouled exchanger never runs out of steam at the median case, while the clean one is below atmospheric at both loads, the pattern of Figure 3. Its numbers differ from Figure 3, which follows one scenario with its own coefficients through the run; the full model adds the 300 feed cases, the run in half-month steps through the seasons, the cleanings and the costs.

TABLE Steps of the method, with this paper's choices and the model function that does each.
| Step | What to do | In this paper | In the model |
| 1. Operating cases | Flow and inlet temperature over the plant's range, with turndown and the seasons | 300 Issue 8 cases in 24 seasonal groups; 50% turndown | cases(), season_buckets() |
| 2. Heat transfer | Clean coefficients from correlations, with their scatter | Eq. (1); Gnielinski, with Sieder–Tate in the code for laminar flow [@sieder] | h_tube(), U_of() |
| 3. Fouling | Asymptotic curve with uncertain level and speed | Eq. (3); Table 2 | scenarios(), SCEN |
| 4. Follow the run | Steam needed, rate cut, stall, step by step; clean on demand | Eqs. (2) and (4); 24 months in half-month steps | operate(), run() |
| 5. Cost | Annualised installed cost, cleanings, lost production | Towler and Sinnott floating head with Hand factor | installed_cost() |
| 6. Drivers and cases | Rank correlation; linear fouling; shorter run; condensate back pressure; area cost | Figures 4 and 5 | main block, hx_extras.py |

CODE appendix || Clean and TEMA design areas of E-101 at the design case, and the shell pressure needed clean and fully fouled at a chosen area over 2,000 sampled fouling levels (Python 3 with NumPy).
"""
