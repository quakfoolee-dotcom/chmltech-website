"""Chmltech Online Journal, Vol. 106, Issue 23: Hybrid Digital Twins for Heat Exchanger Fouling: Physics, Machine Learning and the Combination Tested on a Steam Preheater (Nov 27 2026).

Worked case: the steam-heated feed preheater E-101 of Issue 21 at 6 m2, 20 synthetic histories of three two-year runs with known
fouling, four monitors (physics only, constant correction, hybrid, gradient boosting). Model: content/journal/proc/models/twin/."""

SLUG = "hybrid-digital-twins-for-heat-exchanger-fouling-physics-machine-learning-and-the-combination-tested-on-a-steam-preheater"
META = dict(
    volume=106, issue=23,
    title='Hybrid Digital Twins for Heat Exchanger Fouling: Physics, Machine Learning and the Combination Tested on a Steam Preheater',
    short_title='Hybrid Digital Twins for Heat Exchanger Fouling',
    meta='Physics, machine learning or a hybrid? Four fouling monitors tested on a steam preheater: the hybrid forecasts cleaning within 20% in 14 of 20 runs after a month.',
    keywords=['digital twin', 'hybrid modelling', 'heat exchanger fouling', 'physics-informed machine learning', 'Kern-Seaton', 'condition monitoring', 'gradient boosting', 'steam preheater'],
)
DIVISION = "Division of Clean Energy Technology Innovation"
ABSTRACT = "A digital twin of a fouling heat exchanger can be built from first principles, from data alone, or from both. This paper compares the three on the steam-heated feed preheater E-101, using synthetic histories with known truth. Each history holds three two-year runs of 4-hourly records with seasonal feed temperature, turndown campaigns, instrument noise and drift, a true tube-side coefficient that falls below the published correlation as a power law in Reynolds number, and Kern–Seaton fouling that differs from run to run. Four monitors are trained on the first two runs and tested on the third: physics only; physics with a constant correction learned from the days after each cleaning; a hybrid whose correction is a power law in Reynolds number; and gradient-boosted machine learning on flow, inlet temperature and time since cleaning. Over 20 histories the physics-only fouling estimate is biased by 1.8 × 10⁻⁴ m²K/W, about the TEMA design value; the hybrid's median RMS error is 0.25 × 10⁻⁴. One month into a run the hybrid forecasts when the exchanger can no longer heat the design case to within 20% in 14 of 20 histories, against 9 for the constant correction and none for machine learning. At turndown in the test run, which adds turndown in the coldest weeks, unseen in training, the hybrid predicts shell pressure to a median 0.07 bar, against 0.24 bar for machine learning and 0.47 bar for physics alone. The advantage is partly built into the test."

REFS = {
    'bergman': ('Bergman, T. L., Lavine, A. S., Incropera, F. P., &amp; DeWitt, D. P. (2011). <em>Fundamentals of heat and mass transfer</em> (7th ed.). Wiley.',
        ''),
    'bradley': ('Bradley, W., et al. (2022). Perspectives on the integration between first-principles and data-driven modeling. <em>Computers &amp; Chemical Engineering, 166</em>, 107898.',
        'https://doi.org/10.1016/j.compchemeng.2022.107898'),
    'friedman': ('Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. <em>Annals of Statistics, 29</em>(5), 1189–1232.',
        'https://doi.org/10.1214/aos/1013203451'),
    'gnielinski': ('Gnielinski, V. (1976). New equations for heat and mass transfer in turbulent pipe and channel flow. <em>International Chemical Engineering, 16</em>(2), 359–368.',
        ''),
    'karniadakis': ('Karniadakis, G. E., Kevrekidis, I. G., Lu, L., Perdikaris, P., Wang, S., &amp; Yang, L. (2021). Physics-informed machine learning. <em>Nature Reviews Physics, 3</em>, 422–440.',
        'https://doi.org/10.1038/s42254-021-00314-5'),
    'kern': ('Kern, D. Q., &amp; Seaton, R. E. (1959). A theoretical analysis of thermal surface fouling. <em>British Chemical Engineering, 4</em>(5), 258–262.',
        ''),
    'preheater': ('Lee, Q. F. (2026). Sizing the feed preheater under fouling uncertainty: Area margin, cleaning and condensate stall. <em>Chmltech Online Journal, 106</em>(21).',
        'https://www.chmltech.com/post/sizing-the-feed-preheater-under-fouling-uncertainty-area-margin-cleaning-and-condensate-stall.html'),
    'dtwin': ('Lee, Q. F. (2026). Digital twins in chemical process plants: Architecture, modeling approaches and applications. <em>Chmltech Online Journal</em>.',
        'https://www.chmltech.com/post/digital-twins-in-chemical-process-plants-architecture-modeling-and-applications.html'),
    'pv': ('Lee, Q. F. (2026). Sizing pumps and control valves under uncertainty: Monte Carlo design points for chemical plants. <em>Chmltech Online Journal, 106</em>(8).',
        'https://www.chmltech.com/post/sizing-pumps-and-control-valves-under-uncertainty-monte-carlo-design-points-for-chemical-plants.html'),
    'muller': ('Müller-Steinhagen, H. (2011). Heat transfer fouling: 50 years after the Kern and Seaton model. <em>Heat Transfer Engineering, 32</em>(1), 1–13.',
        'https://doi.org/10.1080/01457632.2010.505127'),
    'sklearn': ('Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. (2011). Scikit-learn: Machine learning in Python. <em>Journal of Machine Learning Research, 12</em>, 2825–2830.',
        ''),
    'psichogios': ('Psichogios, D. C., &amp; Ungar, L. H. (1992). A hybrid neural network–first principles approach to process modeling. <em>AIChE Journal, 38</em>(10), 1499–1511.',
        'https://doi.org/10.1002/aic.690381003'),
    'rasheed': ('Rasheed, A., San, O., &amp; Kvamsdal, T. (2020). Digital twin: Values, challenges and enablers from a modeling perspective. <em>IEEE Access, 8</em>, 21980–22012.',
        'https://doi.org/10.1109/ACCESS.2020.2970143'),
    'sundar': ('Sundar, S., Rajagopal, M. C., Zhao, H., Kuntumalla, G., et al. (2020). Fouling modeling and prediction approach for heat exchangers using deep learning. <em>International Journal of Heat and Mass Transfer, 159</em>, 120112.',
        'https://doi.org/10.1016/j.ijheatmasstransfer.2020.120112'),
    'thompson': ('Thompson, M. L., &amp; Kramer, M. A. (1994). Modeling chemical processes using prior knowledge and neural networks. <em>AIChE Journal, 40</em>(8), 1328–1340.',
        'https://doi.org/10.1002/aic.690400806'),
    'ujevic': ('Ujević Andrijić, Ž., &amp; Rimac, N. (2025). Data-driven fouling detection in refinery preheat train heat exchangers using neural networks and gradient boosting. <em>Sensors, 25</em>(16), 4936.',
        'https://doi.org/10.3390/s25164936'),
    'vonstosch': ('von Stosch, M., Oliveira, R., Peres, J., &amp; Feyo de Azevedo, S. (2014). Hybrid semi-parametric modeling in process systems engineering: Past, present and future. <em>Computers &amp; Chemical Engineering, 60</em>, 86–101.',
        'https://doi.org/10.1016/j.compchemeng.2013.08.008'),
    'zubair': ('Zubair, S. M., Sheikh, A. K., Younas, M., &amp; Budair, M. O. (2000). A risk based heat exchanger analysis subject to fouling: Part I: Performance evaluation. <em>Energy, 25</em>(5), 427–443.',
        ''),
}

CODE = {"appendix": open(__file__.replace("paper_v106_i23.py", "models/twin/twin_appendix.py"), encoding="utf-8").read().rstrip()}

DOWNLOADS = [  # served from assets/journal/code/
    dict(file='twin_appendix.py', label='Appendix script', note='Hybrid fouling monitor: learned correction, fouling estimate and cleaning forecast (Python 3, NumPy, SciPy)'),
    dict(file='chmltech-hybrid-twin-model.zip', label='Full model', note='Synthetic plant histories, the four monitors, summary over 20 histories, results JSON, README'),
]

BODY = r"""
## Introduction

The companion paper sized E-101 for fouling it could only estimate: an asymptotic resistance judged at 1 to 8 × 10⁻⁴ m²K/W, and a tube-side coefficient carrying the ±15% scatter of its correlation, the two inputs that decided most of the outcome [@preheater]. Once the plant runs, both can be measured. The monitor that measures them, and forecasts when the exchanger will need cleaning, is a simple example of what is now called a digital twin: a model kept in step with the plant by its own data [@rasheed, @dtwin].

There are three ways to build it. A physics model computes the overall coefficient from the measured duty and temperatures, compares it with the clean coefficient from correlations, and calls the difference fouling. It needs no training data, but it inherits every error in the correlations. A machine-learning model learns the plant's behaviour from its history; it needs no correlations, but it knows only the conditions it has seen [@sundar, @ujevic]. A hybrid model keeps the physics structure and learns only what the physics gets wrong, an idea with a long history in process engineering [@psichogios, @thompson, @vonstosch] and now often called physics-informed machine learning [@karniadakis, @bradley].

The arguments for the hybrid are well rehearsed, and probabilistic treatments of fouling have long fed exchanger maintenance [@zubair]; quantitative comparisons of monitors on a plant where the truth is known are rarer. This paper builds synthetic histories of E-101 in which the true fouling and the true coefficients are known, gives the same data to four monitors, and measures three things an operator cares about: how well each estimates the fouling, how early and how accurately each forecasts the cleaning, and how each behaves in operating conditions it was not trained on.

## The Plant and Its Data

The test bed is E-101 as built at 6 m², an area the companion paper showed to foul out within months, so that every run reaches the point where the steam runs out and the forecast has something to predict [@preheater]. The feed is heated from tank temperature to 80 °C with steam at up to 2.7 barg in the shell; the steam valve holds the outlet temperature until the steam runs out, after which the outlet falls below 80 °C. Table 1 lists what the synthetic plant contains and what the monitors can see.

TABLE The synthetic plant.
| Element | In the plant (true, hidden) | Seen by the monitors |
| Records | 4-hourly, three runs of 24 months each, 4,000 records a run | Same |
| Feed flow | 8,690 kg/h ± 5% at normal rate; 50% during four random turndown campaigns a run; in the test run, also turndown for the first 50 days of each year, a regime absent from the training runs | Measured with ±2% noise and a slow drift of ±1.5% |
| Feed inlet temperature | Seasonal, 8.5 to 36.5 °C with daily scatter | Measured with ±0.3 K noise |
| Outlet temperature | 80 °C, or lower when the steam runs out | Measured with ±0.3 K noise |
| Shell pressure | Set by the steam valve; at most 2.7 barg | Measured with ±0.015 bar noise |
| Tube-side coefficient | 0.88 (Re/17,800)<sup>0.15</sup> times the Gnielinski correlation: 12% low at normal rate, 20% low at turndown | Not seen; the correlation is known |
| Condensing coefficient | 7,000 W/m²K | Assumed 8,000 W/m²K |
| Shell-side fouling | 1 × 10⁻⁴ m²K/W, constant | Assumed, correctly |
| Fouling | Kern–Seaton, a new level (1.5 to 6 × 10⁻⁴ m²K/W) and time constant (1,000 to 6,000 h) drawn for every run | Not seen |

The tube-side deviation is the key to the comparison. It stands for what real plants show: a correlation that fits the average of laboratory data is rarely exact for a given exchanger, and its error usually depends on flow [@bergman]. In the plant here the error is 12% at normal rate and grows to about 20% at turndown, and the assumed condensing coefficient is also optimistic. None of the monitors is told this; each has to cope with it from the data.

Twenty such histories are generated, each with its own noise and its own fouling in each run. In every history the first two runs are the training data and the third is the test. The task each monitor faces is the one an operator faces at the start of a new run: estimate the fouling as it builds, forecast when the exchanger will no longer heat the design case, the P95 feed at the P5 inlet temperature of the companion paper and of the pump study before it [@pv], and predict the shell pressure at operating conditions not yet seen.

## Four Monitors

**Physics only (P).** From each record the monitor computes the duty from the measured flow and temperatures, the steam temperature from the measured shell pressure, and the overall coefficient, based on the outside tube area A, from the log-mean temperature difference, Eq. (1). It computes the clean coefficient U₀ from the Gnielinski correlation [@gnielinski] and the assumed condensing coefficient, and takes the fouling resistance as the difference of the reciprocals on the inside area, Eq. (2). Records with the shell at or below 0.05 barg are dropped, since stalled condensate breaks the assumption of uniform condensing:

TEX U_m = \frac{\dot m\,c_p\,(T_{out} - T_{in})}{A\,\Delta T_{lm}}

TEX R_f = \left( \frac{1}{U_m} - \frac{1}{U_0} \right) \frac{D_i}{D_o}

**Physics with a constant correction (O).** The same, but the correlation is first corrected by one factor learned from data. In the first 120 operating hours after each cleaning, when fouling has reached only 2% to 11% of its asymptote, the measured coefficient is taken as clean, and the ratio of the tube-side coefficient it implies to the correlation's is averaged over the two training runs. A longer window would let more of the early fouling into the calibration; a 300-hour window, tried first, biased the learned correction low and weakened the hybrid's early forecasts.

**Hybrid (H).** The same clean-period data, but the correction is learned as a function of the tube-side Reynolds number, Eq. (3), by regression of the logarithm of the ratio on the logarithm of Reynolds number. The physics fixes the structure, the energy balance, the resistances in series and the dependence on flow and temperature through the correlation; the data supply only the part the correlation gets wrong. The learned factor also absorbs the error in the assumed condensing coefficient:

TEX h_i = f(Re)\,h_{i,\mathrm{Gnielinski}}, \qquad f(Re) = a\,Re^{\,b}

**Machine learning only (M).** A gradient-boosted regression [@friedman, @sklearn] maps three inputs available on any plant historian, feed flow, inlet temperature and time since cleaning, to the shell pressure. It is trained on the two training runs and retrained as the test run's data arrive.

**Forecasting.** For P, O and H, the fouling estimates are reduced to daily medians and the Kern–Seaton curve, Eq. (4), is fitted to them by robust least squares [@kern, @muller]. The fitted curve is then carried forward with each monitor's own clean coefficient at the design case, and the forecast is the time at which the design case would need more than 2.7 barg in the shell. For M, the forecast is the time at which the model's predicted shell pressure at the design case first exceeds 2.69 barg. Forecasts are made after 0.5, 1, 1.5, 2 and 3 months of the test run, counting only forecasts made before the true limit is reached:

TEX R_f(t) = R_\infty \left( 1 - e^{-t/\tau} \right)

## Results: Estimating Fouling

Figure 1 shows what each monitor learned about the clean exchanger. The plant's tube-side coefficient runs from 77% of the correlation at turndown to 91% at the top of the normal range. Physics only assumes 100% everywhere. The constant correction, learned from the clean days, settles at 85%, between the plant's values at the two ends but wrong at both. The hybrid's learned curve follows the plant's slope, with a median exponent of 0.157 against the plant's 0.15, and sits one to two points below it: it absorbs the optimistic condensing coefficient, which the plant's own data cannot separate from the tube side, and the little fouling already present in the calibration window.

FIG fig1-learned-correction || Ratio of the tube-side coefficient to the Gnielinski correlation against Reynolds number: the plant, the hybrid's learned correction, the constant correction and the uncorrected correlation, with the operating ranges and the range of the calibration data (the illustrative history, with fixed fouling parameters). || Learned tube-side correction against Reynolds number ||

Those differences become fouling errors, as Figure 2 shows for one test run. Physics only starts the run with an apparent fouling of about 1 × 10⁻⁴ m²K/W on clean tubes and stays about that much too high, the deficit of the correlation read as dirt; at every turndown campaign it jumps to 5 or 6 × 10⁻⁴, because the correlation's error is largest at low flow. The constant correction removes the offset at normal rate but still jumps at turndown. The hybrid follows the true curve through the whole run, with small dips at turndown, where its learned curve is extrapolated.

FIG fig2-fouling-estimates || Fouling resistance estimated by three monitors over the test run of the illustrative history, against the true value; daily medians of 4-hourly records. || Fouling resistance estimated by three monitors over the test run ||

Table 2 gives the errors over all 20 histories. The physics-only bias, 1.8 × 10⁻⁴ m²K/W, is about the TEMA design allowance for this service, 0.001 h·ft²·°F/Btu or 1.8 × 10⁻⁴ m²K/W: a monitor of this kind would report an exchanger as carrying more than half its fouling allowance on the day it came back from cleaning, and several times the allowance at turndown. The constant correction cuts the error by two-thirds, the hybrid by nine-tenths, and the absolute gap between them doubles at turndown.

TABLE Error of the fouling estimate on the test run (medians of 20 histories, 10⁻⁴ m²K/W).
| Monitor | Bias, daily medians | RMS error, daily medians | RMS error, turndown records (4-hourly) |
| Physics only | +1.80 | 2.19 | 3.95 |
| Physics, constant correction | +0.24 | 0.74 | 1.46 |
| Hybrid | −0.10 | 0.25 | 0.50 |

## Results: Forecasting the Cleaning

The question an operator asks of the twin is when the exchanger will stop heating the design case, so that a cleaning can be planned rather than forced. Figure 3 shows how the forecast error falls as the test run's data accumulate.

FIG fig3-forecast-error || Forecast of the time at which the exchanger can no longer heat the design case, against months of data on the test run (20 histories; forecasts are counted only before the true limit, so 20, 20, 19, 16 and 12 histories contribute): median error, left, and share of forecasts within 20% of the truth, right. Errors are capped at 100%, which also scores a forecast that the limit is never reached; at 3 months physics only forecasts no limit in 10 of 12 histories. || Forecast error against months of data on the test run for physics only, constant correction, hybrid and machine learning: median error and share of forecasts within 20% of the truth ||

Two weeks of data are too few for any monitor except the hybrid, which is already within 20% in 9 of 20 histories; the start of a Kern–Seaton curve says little about where it will level off unless the estimate is unbiased from the first day. After one month the hybrid's median error is 15%, with 14 of 20 forecasts within 20%; after six weeks 8%, and after two months 9%, with 14 of 16 within 20%. The constant correction is slower to become useful, with 9 of 20 within 20% at one month, but from six weeks it matches the hybrid, and at two months its median error is slightly lower, 7% against 9%; at three months the hybrid has 10 of 12 within 20% and the constant correction 9. The hybrid failed to forecast a limit once, at two weeks, in one slow-fouling history. Physics only never forecasts within 20%. Its fouling estimate carries the offset from the first day, and a curve forced through zero at the start of the run cannot fit it, so it predicts the limit far too early, by a median of 44% at two months, and at three months its fitted curve levels off below the limit in most histories. That failure is partly the fit rather than the physics: a curve with a free intercept, or fouling measured from the start-of-run value, would recover much of it, and the constant correction is in effect that remedy.

The machine-learning monitor never forecasts within 20%, and the reason is instructive. Its target, shell pressure, saturates at 2.7 barg once the steam runs out, so the data say little about how far past the limit the exchanger is, and the design case, at the top of the flow range and the bottom of the temperature range, lies at the edge of its training data. With only two training runs, both starting in winter, time since cleaning is also confounded with season: the model learned that cold feed and high shell pressure arrive about 8,000 hours after cleaning, when the training runs met their second winter, and forecast the limit there in most histories. Across the 20 histories its forecasts clustered at 7,200 to 7,900 hours, whatever the run's true limit, which ranged from 950 to 5,400 hours. This is a failure of feature and target design with too little history, the normal situation for a new exchanger, more than an inherent limit of machine learning; but it is exactly the failure a model with no physics has no way to notice.

## Results: Outside the Training Data

The test run contains one regime the training runs did not: turndown during the first 50 calendar days of each year, when the feed is also coldest. Turndown itself appears in the training runs' random campaigns; turndown in the coldest weeks does not. For this test the machine-learning model is retrained on the two training runs plus every test-run record outside the scored turndown records, so it sees the test run's fouling; the physics monitors use their Kern–Seaton fit to the test run. Figure 4 gives each monitor's error in predicting the shell pressure over all turndown records of the test run, a quantity that decides whether the shell stalls; between 44% and 70% of them, depending on the history, fall in the winter windows, and the rest in random campaigns like those in training, so the test mixes the new regime with a familiar one.

FIG fig4-turndown-extrapolation || Mean absolute error of the shell pressure predicted at turndown records of the test run: median and P90 over 20 histories. || Shell pressure error at turndown in the test run ||

The hybrid's median error is 0.07 bar. Machine learning's median is 0.24 bar, but its P90 is 0.59 bar: in some histories it does tolerably by interpolating nearby training data, in others it is badly wrong, with nothing to warn the user which. Physics only is consistently wrong by about 0.47 bar, the effect of its biased coefficient at low flow, and the constant correction by 0.28 bar.

The difference is in what each monitor carries into the new regime. The machine-learning model carries only correlations between its inputs and outputs, which may not hold where it has little data. The physics models carry the energy balance and the way heat transfer changes with flow, which hold everywhere; the hybrid adds the plant's own correction to that change. In the scored records the true shell pressure ranged from about 0 to 2.7 barg across the 20 histories (0.2 to 1.9 barg in the illustrative history), so some records sat at or near stall and some at the steam limit; an error of 0.2 bar near atmospheric pressure is the difference between a shell that drains its condensate and one that stalls, and the companion paper showed how much of the year a well-sized E-101 spends near that line [@preheater].

### 6.1 How fair is the comparison?

Three features of the test favour the hybrid and should be read with the results. First, the plant's deviation from the correlation is itself a power law in Reynolds number, the form the hybrid fits. The hybrid recovered the exponent closely, 0.157 in the median history against 0.15, and could therefore extrapolate from the clean-day Reynolds numbers of about 14,000 to 18,500 down to turndown at 7,000 to 11,500; in a few histories the calibration window overlapped a turndown campaign, giving it some low-flow clean data. A plant whose deviation changes shape at low flow, for example near transition, would not be followed so closely, and the remedy is to calibrate on clean data at low flow as well, which a planned turndown after a cleaning can provide.

Second, the machine-learning monitor was given three raw inputs and a censored target. A model given outlet temperature, physics-derived features such as the measured overall coefficient, or many more runs would do better; the comparison shows what happens when a data-only model is used early in a plant's life, not the best that machine learning can do. Third, the 6 m² area was chosen so that every test run reaches its limit, between 950 and 5,400 hours after cleaning, which keeps the forecasting horizon short; for a well-sized exchanger whose limit is years away, every forecast would be harder and the gap between the monitors in absolute hours larger.

One feature works the other way. The plant's run lengths are counted in operating hours, 8,000 a year, while the seasons and the 50-day winter windows run on calendar days; a run of "24 months" is about 22 calendar months. This shifts the seasons against the fouling slightly from run to run, which is realistic and makes the forecasting task a little harder for every monitor.

## Building a Hybrid Twin

A fouling twin of this kind needs little: four instruments the exchanger already has, a correlation, and a few days of clean operation after each cleaning. Table 3 sets out the choices.

TABLE Building a fouling twin for a heat exchanger.
| Decision | Recommendation | Why |
| Instruments | Feed flow, inlet and outlet temperature, shell pressure or steam temperature; 4-hourly records were enough here, hourly gives more margin | Enough for the duty and the driving force; the twin is only as good as the flow meter |
| Model structure | Energy balance and resistances in series, with the tube-side correlation | Holds at any load, including ones not yet seen |
| What to learn from data | A correction to the clean coefficient as a function of Reynolds number, from the first few days after each cleaning, at more than one load if possible | The correlation's error is the largest source of bias, and it may depend on flow |
| What not to learn from data | The fouling curve of a new run | It differs run to run; fit it to the run's own estimates instead |
| Fouling model for forecasting | Kern–Seaton fitted to daily medians by robust least squares; a linear fit beside it is suggested | Captures levelling off; a linear fit is the warning case |
| When to trust a forecast | After about a month of a run for the hybrid; reporting the range from a few fits is suggested | Earlier forecasts are dominated by noise in the early curve |
| Data to exclude | Stalled-shell records, start-ups and transients; steam-limited records can stay if the outlet temperature is measured | They break the steady, uniform-condensing assumptions |
| Recalibration | Refit the correction after every cleaning, from a short window; watch for drift in the flow meter | The clean days are free calibration data; drift and early fouling both look like a lower clean coefficient |
| Role of pure machine learning | Detecting anomalies and instrument faults, filling gaps; physics-derived features if used for forecasting | Good at interpolation; poor at forecasting a new run from little history |

Three cautions apply. The clean-period calibration assumes the tubes really are clean after each cleaning and that the window is short enough for fouling not to have begun; a cleaning that leaves a residue will be learned as a lower clean coefficient and the fouling of the next run underestimated. The correction absorbs every error that varies with flow, so a slowly drifting flow meter will be learned too; a second, independent check such as a periodic duty test is worth having. And the forecast is only as good as the fouling model: if fouling does not level off, a Kern–Seaton fit will forecast too late, so the twin should report a linear fit beside it, and the gap between them, as the companion paper's linear-fouling case argues [@preheater].

## Conclusions

Four monitors of the same steam preheater, given the same synthetic plant data, were compared where the truth was known:

- A physics-only monitor that trusts the published correlation reads the correlation's error as fouling. Here its bias, 1.8 × 10⁻⁴ m²K/W, was about the TEMA design allowance, and at turndown its error nearly doubled.
- A hybrid that learns only the correlation's error, as a function of flow, from the first days after each cleaning, estimated fouling with a median RMS error of 0.25 × 10⁻⁴ m²K/W and forecast the cleaning to within 20% in 14 of 20 runs after one month. A constant correction matched it from about six weeks but was slower to become useful and two to four times as wrong at turndown.
- A machine-learning model of the raw operating data could not forecast the cleaning of a new run, because with two training runs its time since cleaning was confounded with season and the design case lay at the edge of its data; at turndown in the test run, including turndown in the coldest weeks it had not seen, its errors were erratic, a median of 0.24 bar but a P90 of 0.59 bar, against 0.07 and 0.18 bar for the hybrid.
- The parts of a twin that physics knows, the energy balance and how heat transfer changes with flow, should be built in; the parts it does not know, the plant's own deviation from the correlation, should be learned; and quantities that change from run to run, such as the fouling itself, should be fitted to each run as it happens.

The study has limits. The plant is synthetic, and the hybrid's advantage at turndown is partly built in: the plant's deviation from the correlation follows a power law that the hybrid's regression can represent exactly, real plants will be less tidy, and the noise and drift are idealised. Only one hybrid structure and one machine-learning model were tried; a machine-learning model given physics-derived features or more history would do better than the one here. The design case flow, 9,569 kg/h, sits at the very top of the plant's flow range; the illustrative history of Figures 1 and 2 uses fixed fouling parameters rather than randomly drawn ones. Stall, start-ups and cleaning residues are excluded or idealised. The Python model, which generates the plant histories and runs all four monitors, can be downloaded from this paper's page.

## Appendix: A Hybrid Fouling Twin in About 50 Lines of Code

Table 4 maps the method to the downloadable model. The script below is the hybrid monitor on its own: it learns the Reynolds-number correction from clean records, estimates the fouling of a new run, fits Kern–Seaton to two months of daily medians and forecasts when the design case runs out of steam. A small synthetic plant stands in for historian data; replace it with the four instrument tags of a real exchanger. On its own synthetic data it learns a correction of 0.86 at Reynolds number 18,000 and forecasts the limit at 1,650 hours after cleaning, the true value, although the fitted asymptote and time constant are off by a fifth and almost a third, a reminder that the forecast is better determined than the curve's parameters.

TABLE Steps of the method and where the model does them.
| Step | What to do | In this paper | In the downloadable model (printed script) |
| 1. Data | Flow, inlet and outlet temperature, shell pressure; drop stalled and transient records | 4-hourly, three runs per history; shell &gt; 0.05 barg | plant(), u_measured() (plant(), u_measured()) |
| 2. Learn the correction | Regress the clean-period coefficient on Reynolds number | First 120 h after each cleaning, runs 1 and 2 | calibrate_clean(), calibrate_offset() (calibrate()) |
| 3. Estimate fouling | Eq. (2) with the corrected clean coefficient; daily medians | Every test-run record | estimate_rf(), daily() (fouling()) |
| 4. Forecast | Fit Eq. (4); carry forward to the design case | After 0.5 to 3 months | ks_fit(), time_to_limit() (forecast()) |
| 5. Compare | Physics only, constant correction, hybrid, machine learning; 20 histories | Table 2, Figures 1 to 4 | evaluate(), twin_summary.py |

CODE appendix || The hybrid monitor on its own: learn the Reynolds-number correction from clean records, estimate fouling, fit Kern–Seaton to two months of daily medians and forecast the limit (Python 3 with NumPy and SciPy)."""
