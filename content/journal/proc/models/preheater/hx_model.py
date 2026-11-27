"""Feed preheater E-101 under fouling uncertainty - Chmltech Online Journal (preheater paper).
Steam-heated shell-and-tube preheater for the reactor feed of Issues 8 and 9: feed on the tube side, heated to 80 C,
low-pressure steam condensing on the shell side, its pressure set by a control valve. Fouling on the tube side
grows over the run (Kern-Seaton). For each candidate area and scenario the model follows the run month by month
over the Issue 8 operating cases and finds (a) the hours the plant must cut rate because the steam cannot reach the
required temperature and (b) the hours the shell would need to run below atmospheric pressure (condensate stall).
Python 3 with NumPy and SciPy; imports the Issue 8 model for the operating cases."""
import json, math
import numpy as np
from scipy import stats
import pumpvalve_model as M

CP, KF = 2000.0, 0.13                       # J/kg.K and W/m.K of the feed
T_OUT = 80.0                                # C, reactor feed temperature
OD, ID, LT = 0.01905, 0.01575, 4.88         # m: 3/4 in tube, 16 BWG, 16 ft
A_TUBE = math.pi * OD * LT                  # outside area per tube, m2
R_WALL = OD * math.log(OD / ID) / (2 * 45.0)  # carbon steel wall, OD basis
HOURS, MARGIN0, RATE_TH = 8000.0, 300.0, 6.25
EUR = 2.0975                                # C$ per 2010 US$ cost-correlation dollar (as Issue 9)
CRF = 0.08 / (1 - 1.08 ** -20)              # capital recovery, 8%, 20 years
TD_SHARE = 0.125                            # most likely share of hours at 50% turndown (Issue 9 mid-range)


def tsat(p_barg):                           # saturation temperature of steam, C (Antoine, water, 100-180 C)
    P_mmhg = (p_barg + 1.01325) * 750.062
    return 1810.94 / (8.14019 - np.log10(P_mmhg)) - 244.485


def psat_barg(T):
    return 10 ** (8.14019 - 1810.94 / (T + 244.485)) / 750.062 - 1.01325


TPP = 12                                    # tubes per pass: about 1.2 m/s at the median design flow
def geometry(A):
    """Tubes per pass fixed for velocity; tube length sets the area (2 passes up to 6.1 m tubes, then 4 passes)."""
    p = 2 if A / (2 * TPP * math.pi * OD) <= 6.1 else 4
    L = A / (p * TPP * math.pi * OD)
    return p * TPP, p, A, L


def h_tube(m_kgh, T, n, p, f_hi=1.0, L=4.88):
    """Tube-side coefficient, W/m2.K on the inside area: Gnielinski above Re 2300, Sieder-Tate laminar below."""
    r, mu = M.rho(T), M.mu(T)
    v = m_kgh / 3600 / r / (n / p * math.pi * ID ** 2 / 4)
    Re = r * v * ID / mu; Pr = CP * mu / KF
    f = (0.79 * np.log(np.maximum(Re, 2300)) - 1.64) ** -2
    nu_t = (f / 8) * (Re - 1000) * Pr / (1 + 12.7 * np.sqrt(f / 8) * (Pr ** (2 / 3) - 1))
    nu_l = np.maximum(3.66, 1.86 * (Re * Pr * ID / L) ** (1 / 3))
    nu = np.where(Re >= 2300, np.maximum(nu_t, nu_l), nu_l)
    return f_hi * nu * KF / ID, Re


def U_of(m_kgh, T, n, p, f_hi, h_o, rf_i, rf_o=0.0001, L=4.88):
    hi, Re = h_tube(m_kgh, T, n, p, f_hi, L)
    return 1.0 / (1 / (hi * ID / OD) + R_WALL + 1 / h_o + rf_i * OD / ID + rf_o), Re


def operate(A, m, Tin, f_hi, h_o, rf_i, ts_max):
    """For arrays of cases: required steam temperature, lost production fraction, stall flag."""
    n, p, Aact, L = geometry(A)
    Tm = (Tin + T_OUT) / 2
    U, Re = U_of(m, Tm, n, p, f_hi, h_o, rf_i, L=L)
    E = np.exp(-U * Aact / (m / 3600 * CP))
    ts_req = (T_OUT - Tin * E) / (1 - E)
    short = ts_req > ts_max
    # rate the exchanger can heat to 80 C at the highest steam temperature (iterate: U depends on flow)
    Lstar = np.log((ts_max - Tin) / (ts_max - T_OUT))
    mm = m.copy()
    for _ in range(8):
        Ui, _ = U_of(mm, Tm, n, p, f_hi, h_o, rf_i, L=L)
        mm = np.minimum(m, Ui * Aact / (CP * Lstar) * 3600)
    lost = np.where(short, 1 - mm / m, 0.0)
    stall = ts_req < 100.0
    return ts_req, lost, stall, Re


SCEN = dict(f_hi=("logn", 0.15), h_o=("tri", (5000, 8000, 12000)), rinf=("tri", (1.0e-4, 3.0e-4, 8.0e-4)),
            tau=("tri", (1000, 3000, 8000)), p_hdr=("tri", (2.6, 3.0, 3.2)), margin=("tri", (150, 300, 500)),
            td=("uni", (0.0, 0.25)))
DP_VALVE = 0.3                              # bar across the steam control valve at full opening


def scenarios(n, seed=21):
    rng = np.random.default_rng(seed); sc = {}
    for k, (kind, a) in SCEN.items():
        if kind == "logn": sc[k] = rng.lognormal(-a ** 2 / 2, a, n)
        elif kind == "tri": sc[k] = rng.triangular(*a, n)
        else: sc[k] = rng.uniform(*a, n)
    return sc


def cases(n=300, seed=3):
    X = M.sample(n, seed=seed)
    m = M.PRODUCT_KGH * X["rate"] / M.YIELD * (1 + X["recycle"])
    return m, X["T"]


CLEAN_COST = 25000.0                        # C$ per unplanned cleaning: channel and floating-head covers off, hydroblast straight tubes, labour
CLEAN_H = 36.0                              # h of lost production per unplanned cleaning, incl. restart
CUT_TRIGGER = 0.01                          # clean when the plant loses more than 1% of production


def season_buckets(Tin, nb=24):
    """Cases sorted by tank temperature into nb buckets; step k of the year uses the bucket matching the season
    (coldest at the start of the calendar year), so the run follows the seasons."""
    order = np.argsort(Tin); B = np.array_split(order, nb)
    phase = (1 - np.cos(2 * np.pi * (np.arange(nb) + 0.5) / nb)) / 2          # 0 in winter, 1 in summer
    return [B[min(nb - 1, int(ph * nb))] for ph in phase]


STALL_BP = 0.0                              # barg: condensate back pressure at the trap outlet (atmospheric return)


def run(areas, n_scen=500, run_months=24, seed=21, linear=False, sc=None, on_demand=True, seasonal=True, stall_bp=None):
    """Half-month steps over a run between turnarounds, following the seasons; unplanned cleaning when the
    expected rate cut in a step exceeds 1%. A 'rate cut' is any step with expected lost production above 0.1%."""
    sc = sc or scenarios(n_scen, seed); mN, Tin = cases()
    bp = STALL_BP if stall_bp is None else stall_bp; ts_stall = float(tsat(bp))
    nb = 24; dt = HOURS / nb; nst = run_months * 2
    buckets = season_buckets(Tin, nb) if seasonal else [np.arange(len(mN))] * nb
    start = np.random.default_rng(seed + 7).integers(0, nb, n_scen)           # turnaround month varies by scenario
    out = {}
    for A in areas:
        lost = np.zeros(n_scen); stallN = np.zeros(n_scen); stallT = np.zeros(n_scen); cleans = np.zeros(n_scen)
        first_cut = np.full(n_scen, np.inf)
        for i in range(n_scen):
            ts_max = tsat(sc["p_hdr"][i] - DP_VALVE); td = sc["td"][i]; since = 0.0; L_ = 0.0; sN_ = 0.0; sT_ = 0.0
            for k in range(nst):
                b = buckets[(start[i] + k) % nb]; m_, T_ = mN[b], Tin[b]
                tmid = since + dt / 2
                rf = sc["rinf"][i] * (tmid / sc["tau"][i] if linear else (1 - math.exp(-tmid / sc["tau"][i])))
                tsN, lN, _, _ = operate(A, m_, T_, sc["f_hi"][i], sc["h_o"][i], rf, ts_max)
                tsT, lT, _, _ = operate(A, 0.5 * m_, T_, sc["f_hi"][i], sc["h_o"][i], rf, ts_max)
                lf = (1 - td) * lN.mean() + td * 0.5 * lT.mean()                 # turndown loss is on half the rate
                if lf > 0.001 and not np.isfinite(first_cut[i]): first_cut[i] = k * dt
                if on_demand and lf > CUT_TRIGGER:
                    cleans[i] += 1; L_ += lf * dt / 2; since = dt / 2          # half the step at the cut, then clean
                    tsN0, _, _, _ = operate(A, m_, T_, sc["f_hi"][i], sc["h_o"][i], 0.0, ts_max)
                    tsT0, _, _, _ = operate(A, 0.5 * m_, T_, sc["f_hi"][i], sc["h_o"][i], 0.0, ts_max)
                    sN_ += 0.5 * ((tsN < ts_stall).mean() + (tsN0 < ts_stall).mean()) / nst
                    sT_ += 0.5 * ((tsT < ts_stall).mean() + (tsT0 < ts_stall).mean()) / nst
                else:
                    L_ += lf * dt; since += dt
                    sN_ += (tsN < ts_stall).mean() / nst; sT_ += (tsT < ts_stall).mean() / nst
            lost[i] = L_ / (nst * dt); stallN[i] = sN_; stallT[i] = sT_
        yrs = run_months / 12
        out[A] = dict(lost=lost, stallN=stallN, stallT=stallT, first_cut=first_cut, cleans_y=cleans / yrs,
                      lost_cost=lost * RATE_TH * sc["margin"] * HOURS,
                      clean_cost=cleans / yrs * (CLEAN_COST + CLEAN_H * RATE_TH * sc["margin"]))
    return out, sc


def installed_cost(A):
    """Shell-and-tube, floating head (straight tubes, cleanable tube side), carbon steel (Towler & Sinnott, 2010 US
    Gulf Coast), times Hand factor 3.5, in C$; linear in area below the correlation's 10 m2 lower limit."""
    return (32000 + 70 * max(A, 10) ** 1.2 * (A / max(A, 10))) * EUR * 3.5


if __name__ == "__main__":
    import time; t0 = time.time()
    # design points
    X = M.sample(20000, seed=1); m = M.PRODUCT_KGH * X["rate"] / M.YIELD * (1 + X["recycle"]); Tin = X["T"]
    R = {"cases": dict(m_p50=float(np.median(m)), m_p95=float(np.percentile(m, 95)), Tin_p5=float(np.percentile(Tin, 5)),
                       Q_p50=float(np.median(m / 3600 * CP * (T_OUT - Tin)) / 1000), Q_p95=float(np.percentile(m / 3600 * CP * (T_OUT - Tin), 95)) / 1000)}
    print(R["cases"])
    areas = [4, 5, 5.42, 6, 6.5, 7, 8, 9, 10, 11, 12, 14]
    out, sc = run(areas)
    R["areas"] = areas; R["by_area"] = {}
    for A in areas:
        o = out[A]; n, p, Aact, L = geometry(A)
        tot = installed_cost(Aact) * CRF + o["lost_cost"] + o["clean_cost"]
        R["by_area"][str(A)] = dict(tubes=n, passes=p, A_act=Aact, L=L, cost=installed_cost(Aact),
            cleans_y=float(o["cleans_y"].mean()), clean_cost=float(o["clean_cost"].mean()), total=float(tot.mean()), total_p95=float(np.percentile(tot, 95)),
            lost_mean=float(o["lost"].mean()), lost_cost=float(o["lost_cost"].mean()), lost_cost_p95=float(np.percentile(o["lost_cost"], 95)),
            p_cut_in_run=float(np.mean(np.isfinite(o["first_cut"]))), p_cut_12=float(np.mean(o["first_cut"] <= HOURS)),
            stallN=float(o["stallN"].mean()), stallT=float(o["stallT"].mean()))
        print(A, n, p, round(Aact, 2), round(installed_cost(Aact)), {k: round(v, 4) for k, v in R["by_area"][str(A)].items() if k not in ("tubes", "passes", "A_act", "cost", "L")})
    # design points at the design case: P95 flow, P5 inlet temperature, steam at 3.0 barg less the valve drop
    mD, TD = R["cases"]["m_p95"], R["cases"]["Tin_p5"]; tsD = float(tsat(3.0 - DP_VALVE))
    def area_for(Ufun):
        A = 5.0
        for _ in range(40):
            n, p, _, L = geometry(A); U = Ufun(n, p, L)
            A = (mD / 3600 * CP) / U * math.log((tsD - TD) / (tsD - T_OUT))
        return A, U
    Tm = (TD + T_OUT) / 2
    A_clean, U_clean = area_for(lambda n, p, L: float(U_of(np.array([mD]), Tm, n, p, 1.0, 8000, 0.0, 0.0, L)[0][0]))
    A_tema, U_tema = area_for(lambda n, p, L: float(U_of(np.array([mD]), Tm, n, p, 1.0, 8000, 1.76e-4, 0.88e-4, L)[0][0]))
    R["Re_min_turndown"] = float(min(h_tube(0.5 * m[i:i+1], (Tin[i:i+1] + T_OUT) / 2, *geometry(8)[:2], 1.0, geometry(8)[3])[1][0] for i in np.argsort(Tin)[:50]))
    R["design"] = dict(A_clean=A_clean, U_clean=U_clean, A_tema=A_tema, U_tema=U_tema, A_tema20=1.2 * A_tema, ts=tsD, post_A=4.61)
    print("design", R["design"])
    # drivers of total cost at 7 m2
    o = out[7]; tot = installed_cost(7) * CRF + o["lost_cost"] + o["clean_cost"]
    R["drivers7"] = {k: float(stats.spearmanr(sc[k], tot)[0]) for k in SCEN}
    print("drivers", {k: round(v, 2) for k, v in R["drivers7"].items()})
    # fouling resistance and clean/fouled U over a run for the figure, at 8 m2 and median flow
    tgrid = np.linspace(0, 2 * HOURS, 49); n, p, _, L = geometry(8)
    rf = np.array([sc["rinf"] * (1 - np.exp(-tk / sc["tau"])) for tk in tgrid])   # (t, scen)
    R["foul_curve"] = dict(t=tgrid.tolist(), p10=np.percentile(rf, 10, axis=1).tolist(), p50=np.percentile(rf, 50, axis=1).tolist(),
                           p90=np.percentile(rf, 90, axis=1).tolist())
    # median scenario: required steam pressure over the run at 6, 8 and 10 m2, median case and turndown
    i50 = int(np.argsort(sc["rinf"] / sc["tau"] * 0 + sc["rinf"])[len(sc["rinf"]) // 2])
    R["steam_path"] = {}
    for A in (6, 8, 10):
        pn, pt = [], []
        for tk in tgrid:
            rfk = sc["rinf"][i50] * (1 - math.exp(-tk / sc["tau"][i50]))
            tsn, _, _, _ = operate(A, np.array([R["cases"]["m_p50"]]), np.array([22.5]), sc["f_hi"][i50], sc["h_o"][i50], rfk, 999)
            tst, _, _, _ = operate(A, np.array([R["cases"]["m_p50"] / 2]), np.array([22.5]), sc["f_hi"][i50], sc["h_o"][i50], rfk, 999)
            pn.append(float(psat_barg(tsn[0]))); pt.append(float(psat_barg(tst[0])))
        R["steam_path"][str(A)] = dict(normal=pn, turndown=pt)
    R["steam_max_barg"] = 3.0 - DP_VALVE
    json.dump(R, open("hx_results.json", "w"), indent=1, default=float)
    print("time", round(time.time() - t0, 1))
