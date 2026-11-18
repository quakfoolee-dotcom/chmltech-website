"""Choosing the pump arrangement under uncertainty - Chmltech Online Journal (Vol. 106, Issue 9 draft). V1.

Same reactor feed service, plant and 20,000 operating cases as Issue 8 (pumpvalve_model.py). Compares arrangements:
  A   1 x 100% running + 1 x 100% spare, fixed speed, control valve FCV-101 (the Issue 8 P95 design)
  B   1 x 100% + 1 x 100% spare, a variable-speed drive (VFD) on each, no control valve
  C3  2 x 50% running + 1 x 50% spare, fixed speed, control valve, second pump staged on and off with flow
  C2  2 x 50% running, no installed spare, otherwise as C3
  E3  2 x 50% + 1 x 50% spare, VFD on every pump, no control valve, pumps staged and run at equal speed
  E2  2 x 50%, no installed spare, otherwise as E3
  D   (variant, not ranked) 2 x 50%, VFD on the lead pump, lag pump fixed speed, no valve: shows the flow gap.
Two layers: (1) 20,000 operating cases (normal) + the same cases at 50% turndown -> hydraulics, efficiency, power,
coverage; (2) 5,000 economic scenarios (electricity price, turndown share, efficiencies, reliability, repair cost,
product margin, capital cost) with a discrete-event failure simulation over 20 years -> life-cycle cost per option,
probability each option is cheapest, and regret. Writes arr_results.json and arr_figdata.json."""
import json
import numpy as np
import pumpvalve_model as M          # Issue 8 model (pumpvalve_model.py), same folder

N, NS, SEED = 20000, 5000, 1
YEARS, HOURS, RATE = 20, M.HOURS, 0.08
PVF = (1 - (1 + RATE) ** -YEARS) / RATE
ETA_MOTOR, ETA_VFD = 0.92, 0.97
ETA100, ETA50 = 0.40, 0.34                  # baseline best efficiencies; scenario layer rescales (power ~ 1/eta_bep)
MOTORS = [1.5, 2.2, 3.0, 4.0, 5.5, 7.5, 11.0, 15.0]
MOTORS_ALL = MOTORS + [18.5, 22.0, 30.0, 37.0, 45.0, 55.0, 75.0, 90.0, 110.0, 132.0, 160.0, 200.0]
CV_RATED, BORE = 34.0, 38.1                  # FCV-101 from Issue 8 (1.5-inch, Cv 34)
ESC = 810.0 / 532.9 * 1.38                   # Towler & Sinnott 2010 US$ -> 2025 C$ (CEPCI, 1.38 C$/US$)
HAND_PUMP, HAND_VALVE, INST_VFD = 4.0, 2.5, 1.5   # Hand installation factors (pumps 4.0, miscellaneous 2.5); VFD assumed
MCSF = 0.30                                  # minimum continuous stable flow, fraction of BEP flow (at speed)


class Pump:
    """Generic radial pump curve through its rated point: H = Hr (S n^2 - (S - 1)(Q/Qr)^2); BEP at 1.05 Qr;
    eta = eta_bep (2x - x^2) with x = Q / (Qbep n)."""
    def __init__(self, Qr, Hr, shut=1.20, eta_bep=ETA100):
        self.Qr, self.Hr, self.S, self.eta_bep, self.Qbep = Qr, Hr, shut, eta_bep, 1.05 * Qr
    def head(self, q, n=1.0): return self.Hr * (self.S * n ** 2 - (self.S - 1) * (q / self.Qr) ** 2)
    def eta(self, q, n=1.0):
        x = q / (self.Qbep * n); return np.clip(self.eta_bep * (2 * x - x ** 2), 0.05, None)
    def npshr(self, q, n=1.0):
        x = q / (self.Qbep * n); return 2.0 * n ** 2 * (0.5 + 0.5 * x ** 2)
    def speed(self, q, H):                    # speed ratio at which the pump delivers q at head H
        return np.sqrt((H / self.Hr + (self.S - 1) * (q / self.Qr) ** 2) / self.S)
    def q_at(self, H, n=1.0):                 # flow at head H and speed n (nan where H above shutoff)
        a = (self.S * n ** 2 - H / self.Hr) / (self.S - 1)
        return np.where(a > 0, self.Qr * np.sqrt(np.clip(a, 0, None)), np.nan)


def rated_point(X, shut=1.20, p=95):
    """Issue 8 rule: Qr = P(p) of demand flow; Hr = P(p) of the rated head each case needs with 0.7 bar across the valve."""
    s = M.system(X); Qr = np.percentile(s["Q"], p)
    need = s["H_sys"] + M.DP_VALVE_MIN * 1e5 / (s["rho"] * M.G)
    return float(Qr), float(np.percentile(need / (shut - (shut - 1) * (s["Q"] / Qr) ** 2), p))


# ---------------- hydraulics of each control scheme over a set of cases ----------------
def throttled(s, pump, k):
    """k identical fixed-speed pumps share flow equally; the valve takes the rest of the head. Below the minimum
    continuous stable flow a recirculation line returns the difference to the tank."""
    q = np.maximum(s["Q"] / k, MCSF * pump.Qbep); Hp = pump.head(q)
    dpv = (Hp - s["H_sys"]) * s["rho"] * M.G / 1e5
    wide = M.wide_open_dp(s["Q"], s["rho"], CV_RATED, BORE)
    P = k * q / 3600 * s["rho"] * M.G * Hp / pump.eta(q) / 1000
    return dict(q=q, n=np.ones_like(q), dpv=dpv, ok=dpv >= M.DP_VALVE_MIN, deliv=dpv >= wide, recirc=k * q - s["Q"],
                P_el=P / ETA_MOTOR, P_valve=s["Q"] / 3600 * np.clip(dpv, 0, None) * 1e5 / 1000)


def vfd(s, pump, k):
    """k identical pumps on drives at equal speed, no control valve; feasible where speed <= 100%."""
    q = s["Q"] / k; n = pump.speed(q, s["H_sys"])
    low = q < MCSF * pump.Qbep * n                      # below stable flow at this speed: hold MCSF, recirculate
    n_low = np.sqrt(s["H_sys"] / (pump.Hr * (pump.S - (pump.S - 1) * (MCSF * 1.05) ** 2)))
    n = np.where(low, n_low, n); q = np.where(low, MCSF * pump.Qbep * n_low, q)
    P = k * q / 3600 * s["rho"] * M.G * s["H_sys"] / pump.eta(q, n) / 1000
    ok = n <= 1.0
    return dict(q=q, n=n, dpv=np.zeros_like(q), ok=ok, deliv=ok, P_el=P / (ETA_MOTOR * ETA_VFD), P_valve=np.zeros_like(q),
                recirc=k * q - s["Q"])


def pick(a, b, use_b):
    return {k: np.where(use_b, b[k], a[k]) for k in a}


def run_option(opt, s, p100, p50):
    """Operating point of every case for one arrangement. Returns per-case arrays + number of pumps running."""
    if opt == "A":
        r = throttled(s, p100, 1); r["k"] = np.ones_like(s["Q"]); r["pump"] = p100
    elif opt == "B":
        r = vfd(s, p100, 1); r["k"] = np.ones_like(s["Q"]); r["pump"] = p100
    elif opt.startswith("C"):              # stage: one pump if it keeps the minimum valve drop, else two
        one, two = throttled(s, p50, 1), throttled(s, p50, 2)
        use2 = ~one["ok"]; r = pick(one, two, use2); r["k"] = np.where(use2, 2, 1); r["pump"] = p50
    elif opt.startswith("E"):              # stage on lower power among feasible configurations (min-flow respected)
        one, two = vfd(s, p50, 1), vfd(s, p50, 2)
        two_ok = two["ok"] & (two["q"] >= MCSF * p50.Qbep * two["n"])
        use2 = ~one["ok"] | (two_ok & (two["P_el"] < one["P_el"]))
        r = pick(one, two, use2); r["k"] = np.where(use2, 2, 1); r["pump"] = p50
    elif opt == "D":                       # lead on VFD, lag fixed speed, no valve; lead held at MCSF with recirculation
        one = vfd(s, p50, 1)
        H = s["H_sys"]; q_lag = np.nan_to_num(p50.q_at(H)); q_lead = s["Q"] - q_lag
        q_lead_run = np.maximum(q_lead, MCSF * p50.Qbep)
        for _ in range(20):                # minimum stable flow at the lead pump's own speed
            n_lead = p50.speed(q_lead_run, H); q_lead_run = np.maximum(q_lead, MCSF * p50.Qbep * n_lead)
        n_lead = p50.speed(q_lead_run, H); recirc = np.clip(q_lead_run - q_lead, 0, None)
        P = (q_lag / p50.eta(q_lag) + q_lead_run / p50.eta(q_lead_run, n_lead)) / 3600 * s["rho"] * M.G * H / 1000
        P_el = q_lag / 3600 * s["rho"] * M.G * H / p50.eta(q_lag) / 1000 / ETA_MOTOR + \
            q_lead_run / 3600 * s["rho"] * M.G * H / p50.eta(q_lead_run, n_lead) / 1000 / (ETA_MOTOR * ETA_VFD)
        two = dict(q=q_lead_run, n=n_lead, dpv=np.zeros_like(H), ok=(n_lead <= 1), deliv=(n_lead <= 1), P_el=P_el,
                   P_valve=np.zeros_like(H), recirc=recirc)
        use2 = ~one["ok"]; r = pick(one, two, use2); r["k"] = np.where(use2, 2, 1); r["pump"] = p50
        r["recirc"] = np.where(use2, recirc, 0.0); r["P_shaft_check"] = P
        r["lag_x"] = np.where(use2, q_lag / p50.Qbep, np.nan)
    return r


def summarise(r, s):
    p = r["pump"]; x = r["q"] / (p.Qbep * r["n"])
    return dict(control=float(np.mean(r["ok"])), deliver=float(np.mean(r["deliv"])), P_el=float(np.mean(r["P_el"])),
                eta=float(np.mean(p.eta(r["q"], r["n"]))), two_running=float(np.mean(r["k"] == 2)),
                por=float(np.mean((x >= 0.70) & (x <= 1.20))), below_mcsf=float(np.mean(x < MCSF)),
                bep_p50=float(np.median(x)), bep_p1=float(np.percentile(x, 1)), bep_p99=float(np.percentile(x, 99)),
                speed_p1=float(np.percentile(r["n"], 1)), speed_p99=float(np.percentile(r["n"], 99)),
                npsh_min=float(np.min(s["npsha"] - p.npshr(r["q"], r["n"]))), P_valve=float(np.mean(r["P_valve"])),
                recirc_share=float(np.mean(r["recirc"] > 1e-9)), recirc_mean=float(np.mean(r["recirc"])))


def api_margin(P):                         # API 610 driver margin on rated power: 125% to 22 kW, 115% to 55 kW, 110% above
    return 1.25 if P <= 22.0 else (1.15 if P <= 55.0 else 1.10)


def motor_for(pump):
    rmax = M.rho(5.0)
    P_rated = pump.Qr / 3600 * rmax * M.G * pump.Hr / pump.eta(pump.Qr) / 1000
    Qe = 1.2 * pump.Qbep
    P_eoc = Qe / 3600 * rmax * M.G * pump.head(Qe) / pump.eta(Qe) / 1000
    need = max(P_rated * api_margin(P_rated), P_eoc)
    return next(m for m in MOTORS if m >= need), P_rated, P_eoc


OPTIONS = {  # installed pumps, running at normal flow (max), drives, valve
    "A": dict(n=2, k=1, vfd=0, valve=True, size=100), "B": dict(n=2, k=1, vfd=2, valve=False, size=100),
    "C3": dict(n=3, k=2, vfd=0, valve=True, size=50), "C2": dict(n=2, k=2, vfd=0, valve=True, size=50),
    "E3": dict(n=3, k=2, vfd=3, valve=False, size=50), "E2": dict(n=2, k=2, vfd=2, valve=False, size=50)}
LABEL = {"A": "A: 1 x 100% + spare, valve", "B": "B: 1 x 100% + spare, VFD", "C3": "C3: 2 x 50% + spare, valve",
         "C2": "C2: 2 x 50%, no spare, valve", "E3": "E3: 2 x 50% + spare, VFDs", "E2": "E2: 2 x 50%, no spare, VFDs"}


def capex(o, pump, motor_kw, s_dut=1.0):
    """Installed cost, C$: purchased (Towler & Sinnott pump and explosion-proof motor correlations, escalated) times Hand
    factors; valve and drives budget prices (Issue 8) times installation allowances."""
    S = pump.Qr / 3.6
    train = ((8000 + 240 * S ** 0.9) + (-1100 + 2100 * motor_kw ** 0.6)) * ESC
    trains = o["n"] * train * HAND_PUMP
    valve = 11000 * s_dut ** 0.5 * HAND_VALVE if o["valve"] else 0.0
    drives = o["vfd"] * (2500 + 300 * motor_kw) * INST_VFD
    return dict(trains=trains, valve=valve, drives=drives)


# ---------------- reliability: discrete-event simulation of one option over its life ----------------
def simulate(o, cap1, lam, mttr, fts, lsw, tman, trest, T, rng):
    """Failures of running trains (exponential), repairs (gamma, shape 2), auto-start of a standby with probability of
    failure to start. Returns (lost production in full-rate hours, number of train failures)."""
    k, n = o["k"], o["n"]
    def short(run): return 0.0 if run >= k else (1.0 if run == 0 else 1.0 - cap1)
    t, lost, nf, run, idle, reps = 0.0, 0.0, 0, k, n - k, []
    while True:
        tf = t + rng.exponential(1.0 / (run * lam)) if run > 0 else np.inf
        tr = min(reps) if reps else np.inf
        tn = min(tf, tr)
        if tn >= T:
            lost += short(run) * (T - t); break
        lost += short(run) * (tn - t); t = tn
        if tr <= tf:
            reps.remove(tr)
            if run < k: run += 1
            else: idle += 1
        else:
            nf += 1; run -= 1; reps.append(t + rng.gamma(2.0, mttr / 2.0))
            if idle > 0:
                idle -= 1
                if rng.random() < fts:
                    lost += short(run) * tman + (trest if run == 0 else 0.0)
                else:
                    lost += lsw * short(run)
                run += 1
            elif run == 0:
                lost += trest
    return lost, nf


def tri(rng, a, m, b, n): return rng.triangular(a, m, b, n)


if __name__ == "__main__":
    R, F = {}, {}
    X = M.sample(N, seed=SEED)
    Qr, Hr = rated_point(X)
    p100, p50 = Pump(Qr, Hr), Pump(Qr / 2, Hr, eta_bep=ETA50)
    sN = M.system(X); sT = M.system(X, M.TURNDOWN * M.flow(X))
    R["rated"] = dict(Qr=Qr, Hr=Hr, q50=Qr / 2, eta100=ETA100, eta50=ETA50)

    # ---- layer 1: hydraulics (normal cases and the same cases at turndown) ----
    def hydraulics(td, keep_fig=False):
        sT_ = M.system(X, td * M.flow(X)); out = {}
        for opt in list(OPTIONS) + ["D"]:
            key = opt if opt in ("A", "B", "D") else opt[0]
            if key in out: continue
            rn, rt = run_option(opt, sN, p100, p50), run_option(opt, sT_, p100, p50)
            out[key] = dict(normal=summarise(rn, sN), turndown=summarise(rt, sT_))
            if keep_fig:
                F[key] = dict(qN=rn["q"][:2500].round(3).tolist(), kN=rn["k"][:2500].astype(int).tolist(),
                              xN=(rn["q"] / (rn["pump"].Qbep * rn["n"]))[:4000].round(3).tolist(),
                              xT=(rt["q"] / (rt["pump"].Qbep * rt["n"]))[:4000].round(3).tolist())
        return out
    hyd = hydraulics(M.TURNDOWN, keep_fig=True)
    sT0 = M.system(X, M.TURNDOWN * M.flow(X))
    F["cloud"] = dict(QN=sN["Q"][:2500].round(3).tolist(), HN=sN["H_sys"][:2500].round(2).tolist(),
                      QT=sT0["Q"][:2500].round(3).tolist(), HT=sT0["H_sys"][:2500].round(2).tolist(), Qr=Qr, Hr=Hr)
    hyd25 = hydraulics(0.25)
    R["hyd25"] = hyd25
    R["hyd"] = hyd
    # capacity with one 50% pump alone (valve wide open / full speed) at each normal case, as a share of demand
    q1 = np.nan_to_num(p50.q_at(sN["H_sys"]))
    cap1 = float(np.mean(np.minimum(q1 / sN["Q"], 1.0)))
    R["cap_one_50"] = cap1

    # ---- verification ----
    a = run_option("A", sN, p100, p50); c2 = throttled(sN, p50, 2)
    R["check"] = dict(
        issue8_Qr=Qr, issue8_Hr=Hr, issue8_Pel=hyd["A"]["normal"]["P_el"] * ETA50 / ETA50,
        parallel_same_head=float(np.max(np.abs(p50.head(sN["Q"] / 2) - p100.head(sN["Q"])))),
        energy_closure=float(np.max(np.abs(a["P_el"] * ETA_MOTOR * p100.eta(a["q"]) -
                                           sN["Q"] / 3600 * sN["rho"] * M.G * p100.head(sN["Q"]) / 1000))),
        valve_plus_system=float(np.max(np.abs(p100.head(sN["Q"]) - sN["H_sys"] - a["dpv"] * 1e5 / (sN["rho"] * M.G)))))
    mk100, Pr100, Pe100 = motor_for(p100); mk50, Pr50, Pe50 = motor_for(p50)
    R["motors"] = dict(m100=mk100, P_rated100=Pr100, P_eoc100=Pe100, m50=mk50, P_rated50=Pr50, P_eoc50=Pe50)

    # ---- layer 2: economic scenarios (reliability simulated once; costs then scaled to any duty size) ----
    rng = np.random.default_rng(SEED + 1)
    sc = dict(price=tri(rng, 0.07, 0.09, 0.13, NS), ftd=rng.uniform(0.0, 0.25, NS),
              f_eta=tri(rng, 0.90, 1.00, 1.12, NS), f_small=tri(rng, 0.93, 1.00, 1.10, NS),
              mtbf=tri(rng, 1.5, 2.5, 4.5, NS), mttr=tri(rng, 24, 72, 168, NS), fts=tri(rng, 0.002, 0.01, 0.03, NS),
              crep=tri(rng, 6000, 10000, 20000, NS), margin=tri(rng, 150, 300, 500, NS), trest=tri(rng, 4, 8, 16, NS),
              mtbf_vfd=tri(rng, 8, 15, 25, NS), kcap=rng.lognormal(0, 0.15, NS), kvfd=tri(rng, 0.7, 1.0, 1.5, NS),
              f_bep=tri(rng, 1.0, 1.5, 2.0, NS))
    LSW, TMAN, CREP_VFD = 0.25, 1.0, 3000.0
    T = YEARS * HOURS
    rate_th = M.PRODUCT_KGH / 1000                         # t/h of product at design rate
    def out_por(H, key, ftd):                              # share of running hours outside 70-120% of BEP
        return (1 - ftd) * (1 - H[key]["normal"]["por"]) + ftd * (1 - H[key]["turndown"]["por"])

    def simulate_all(H):
        sim = {}
        for o, d in OPTIONS.items():
            key = o if o in ("A", "B") else o[0]
            lh, nf, fv = np.zeros(NS), np.zeros(NS), np.zeros(NS)
            pen = 1 + (sc["f_bep"] - 1) * out_por(H, key, sc["ftd"])
            for j in range(NS):
                lam_p = pen[j] / (sc["mtbf"][j] * 8760.0)
                lam_v = (1.0 / (sc["mtbf_vfd"][j] * 8760.0)) if d["vfd"] else 0.0
                lh[j], nf[j] = simulate(d, cap1, lam_p + lam_v, sc["mttr"][j], sc["fts"][j], LSW, TMAN, sc["trest"][j], T,
                                        np.random.default_rng(1000 + j))
                fv[j] = lam_v / (lam_p + lam_v)
            sim[o] = dict(lost_h=lh / YEARS, nfail=nf / YEARS, frac_v=fv, pen=pen)
        return sim
    sim = simulate_all(hyd)

    ETA_TAB_Q = np.array([5.34, 10.68, 20.0, 40.0, 80.0, 160.0, 320.0, 640.0])    # m3/h at about 82 m head
    ETA_TAB_E = np.array([0.34, 0.40, 0.50, 0.60, 0.68, 0.74, 0.78, 0.80])       # illustrative, shaped after HI charts (H-01)
    def eta_size(q):                                     # best efficiency vs flow at this head, log-linear in flow
        return np.interp(np.log(q), np.log(ETA_TAB_Q), ETA_TAB_E)

    TD_FAIL = {"A": 0.0, "B": 0.0, "C3": 0.5, "C2": 0.5, "E3": 0.5, "E2": 0.5}
    TD_LOST = {"A": 0.0, "B": 0.0, "C3": 0.5, "C2": 1.0, "E3": 0.5, "E2": 1.0}
    R["td_factors"] = dict(fail=TD_FAIL, lost=TD_LOST)

    def econ(s_dut, ftd=None, med=False, H=None, SIM=None):
        """Life-cycle cost of every option in every scenario for a duty s_dut times this one (same head, same plant
        layout). Energy scales with flow and efficiency; capital through the cost correlations; repairs with size^0.4;
        lost production with the size of the plant the service feeds."""
        H = hyd if H is None else H; SIM = sim if SIM is None else SIM
        scn = {k: (np.full(1, np.median(v)) if med else v) for k, v in sc.items()}
        if ftd is not None: scn["ftd"] = np.full_like(scn["ftd"], ftd)
        out = {}
        for o, d in OPTIONS.items():
            key = o if o in ("A", "B") else o[0]
            big = d["size"] == 100
            q_pump = (Qr if big else Qr / 2) * s_dut
            eta_b = eta_size(q_pump) * scn["f_eta"] * (1.0 if big else scn["f_small"])
            base_eta = ETA100 if big else ETA50
            Pn, Pt = H[key]["normal"]["P_el"], H[key]["turndown"]["P_el"]
            kwh = HOURS * s_dut * ((1 - scn["ftd"]) * Pn + scn["ftd"] * Pt) * base_eta / eta_b
            pr = (Pr100 if big else Pr50) * s_dut * base_eta / eta_size(q_pump)
            mk = next((m for m in MOTORS_ALL if m >= max(api_margin(pr) * pr, (Pe100 if big else Pe50) * s_dut * base_eta / eta_size(q_pump))), MOTORS_ALL[-1])
            cx = capex(d, Pump(q_pump, Hr), mk, s_dut)
            cap = (cx["trains"] + cx["valve"]) * scn["kcap"] + cx["drives"] * scn["kvfd"]
            sm = dict(SIM[o]) if not med else {k: np.full(1, np.mean(v)) for k, v in SIM[o].items()}
            pen_new = 1 + (scn["f_bep"] - 1) * out_por(H, key, scn["ftd"])
            adj = pen_new / sm["pen"]                        # failures and outage time scale with the failure rate
            af, al = TD_FAIL[o], TD_LOST[o]                  # only one 50% pump runs at turndown (hours-weighted)
            sm["nfail"] = sm["nfail"] * adj * (1 - af * scn["ftd"])
            sm["lost_h"] = sm["lost_h"] * adj * (1 - al * scn["ftd"])
            rep = sm["nfail"] * ((1 - sm["frac_v"]) * scn["crep"] * (s_dut * d["size"] / 100) ** 0.4
                                 + sm["frac_v"] * CREP_VFD * s_dut ** 0.6)
            lost = sm["lost_h"] * rate_th * s_dut * scn["margin"]
            e = kwh * scn["price"]
            out[o] = dict(lcc=cap + PVF * (e + rep + lost), cap=cap, nfail=sm["nfail"], lost_h=sm["lost_h"], energy=e, repair=rep, lost=lost, motor=mk,
                          kwh=kwh, eta=eta_b)
        return out

    res = econ(1.0)
    names = list(OPTIONS)
    L = np.vstack([res[o]["lcc"] for o in names]); best = L.min(axis=0); win = np.argmin(L, axis=0)
    R["econ"] = {}
    for i, o in enumerate(names):
        reg = L[i] - best; r_ = res[o]
        R["econ"][o] = dict(lcc_mean=float(L[i].mean()), lcc_p5=float(np.percentile(L[i], 5)), lcc_p95=float(np.percentile(L[i], 95)),
                            cap=float(r_["cap"].mean()), energy_y=float(r_["energy"].mean()), repair_y=float(r_["repair"].mean()),
                            lost_y=float(r_["lost"].mean()), lost_h_y=float(r_["lost_h"].mean()),
                            lost_h_p95=float(np.percentile(r_["lost_h"], 95)), fail_y=float(r_["nfail"].mean()),
                            p_cheapest=float(np.mean(win == i)), regret_mean=float(reg.mean()),
                            regret_p95=float(np.percentile(reg, 95)), regret_max=float(reg.max()), motor=r_["motor"])
    R["capex_base"] = {o: {k: float(v) for k, v in capex(d, Pump((Qr if d["size"] == 100 else Qr / 2), Hr),
                                                         (mk100 if d["size"] == 100 else mk50), 1.0).items()} for o, d in OPTIONS.items()}
    F["lcc"] = {o: np.percentile(res[o]["lcc"], np.arange(1, 100)).round(0).tolist() for o in names}
    # where does the ranking turn? duty size x share of time at turndown (median scenario), and P(cheapest) by size
    sizes = np.geomspace(1, 50, 18); ftds = np.linspace(0, 0.8, 17)
    grid = [[names[int(np.argmin([econ(sd, fd, med=True)[o]["lcc"][0] for o in names]))] for fd in ftds] for sd in sizes]
    R["map"] = dict(sizes=sizes.tolist(), ftds=ftds.tolist(), cheapest=grid)
    R["by_size"] = {}
    sim25 = simulate_all(hyd25)
    grid25 = [[names[int(np.argmin([econ(sd, fd, med=True, H=hyd25, SIM=sim25)[o]["lcc"][0] for o in names]))] for fd in ftds] for sd in sizes]
    R["map25"] = dict(sizes=sizes.tolist(), ftds=ftds.tolist(), cheapest=grid25)
    for sd in (1, 10, 30, 50):
        rr = econ(float(sd), 0.5, H=hyd25, SIM=sim25); Ls = np.vstack([rr[o]["lcc"] for o in names]); w = np.argmin(Ls, axis=0)
        R["by_size"][f"{sd}_td25_0.5"] = {o: dict(p=float(np.mean(w == i)), lcc=float(Ls[i].mean()), kw=float(rr[o]["kwh"].mean() / HOURS),
                                                  motor=rr[o]["motor"]) for i, o in enumerate(names)}
    for sd in (1, 3, 10, 30, 50):
        for fd in (None, 0.5):
            rr = econ(float(sd), fd); Ls = np.vstack([rr[o]["lcc"] for o in names]); w = np.argmin(Ls, axis=0)
            R["by_size"][f"{sd}_{'base' if fd is None else fd}"] = {o: dict(p=float(np.mean(w == i)), lcc=float(Ls[i].mean()),
                                                                             kw=float(rr[o]["kwh"].mean() / HOURS), motor=rr[o]["motor"])
                                                                     for i, o in enumerate(names)}
    # B with the control valve kept (for fast response or a simple failure mode)
    vcap = 11000 * HAND_VALVE * sc["kcap"]
    LBv = res["B"]["lcc"] + vcap
    R["B_valve"] = dict(lcc_mean=float(LBv.mean()), p_beats_A=float(np.mean(LBv < res["A"]["lcc"])),
                        diff_mean=float((LBv - res["A"]["lcc"]).mean()))
    # probability each option is cheapest against duty size, at the base turndown share and at 50% of hours
    R["p_by_size"] = {}
    for fd in (None, 0.5):
        rows = {o: [] for o in names}; sz = np.geomspace(1, 50, 49).tolist()
        for sd in sz:
            rr = econ(sd, fd); Ls = np.vstack([rr[o]["lcc"] for o in names]); w = np.argmin(Ls, axis=0)
            for i, o in enumerate(names): rows[o].append(float(np.mean(w == i)))
        R["p_by_size"]["base" if fd is None else str(fd)] = dict(size=sz, p=rows,
            kw=[float(econ(sd, fd)["B"]["kwh"].mean() / HOURS) for sd in sz])
    from scipy.stats import spearmanr
    R["drivers"] = {}
    for pair in (("B", "A"), ("E3", "B"), ("C3", "A"), ("E2", "E3")):
        dlt = res[pair[0]]["lcc"] - res[pair[1]]["lcc"]
        R["drivers"]["-".join(pair)] = {k: float(spearmanr(dlt, sc[k])[0]) for k in sc}

    # ---- curve shape: rated head and key results for flatter and steeper curves ----
    R["shape"] = {}
    for shut in (1.10, 1.20, 1.35):
        Qs, Hs = rated_point(X, shut)
        P1, P2 = Pump(Qs, Hs, shut), Pump(Qs / 2, Hs, shut, ETA50)
        row = {}
        for opt in ("A", "B", "C3", "E3"):
            k = opt if opt in ("A", "B") else opt[0]
            rn, rt = run_option(opt, sN, P1, P2), run_option(opt, sT, P1, P2)
            row[k] = dict(Pn=float(np.mean(rn["P_el"])), Pt=float(np.mean(rt["P_el"])), two=float(np.mean(rn["k"] == 2)),
                          porT=float(np.mean(((rt["q"] / (rt["pump"].Qbep * rt["n"])) >= 0.7))))
        R["shape"][str(shut)] = dict(Hr=Hs, shutoff=Hs * shut, **row)
    # ranking with flatter and steeper curves: full scenario set, hydraulics re-solved, reliability reused
    for shut in (1.10, 1.35):
        Qs, Hs = rated_point(X, shut)
        P1, P2 = Pump(Qs, Hs, shut), Pump(Qs / 2, Hs, shut, ETA50)
        Hsh = {}
        for opt in ("A", "B", "C3", "E3"):
            k = opt if opt in ("A", "B") else opt[0]
            Hsh[k] = dict(normal=summarise(run_option(opt, sN, P1, P2), sN), turndown=summarise(run_option(opt, sT, P1, P2), sT))
        rr = econ(1.0, H=Hsh); Ls = np.vstack([rr[o]["lcc"] for o in names]); w = np.argmin(Ls, axis=0)
        R["shape"][str(shut)]["p_cheapest"] = {o: float(np.mean(w == i)) for i, o in enumerate(names)}
        R["shape"][str(shut)]["lcc_mean"] = {o: float(Ls[i].mean()) for i, o in enumerate(names)}
    # full scenario distribution with long turndown
    R["ftd_full"] = {}
    for fd in (0.5, 0.8):
        rr = econ(1.0, fd); Ls = np.vstack([rr[o]["lcc"] for o in names]); w = np.argmin(Ls, axis=0)
        R["ftd_full"][str(fd)] = {o: float(np.mean(w == i)) for i, o in enumerate(names)}
    # installed drive cost at which B stops beating A on average, and P(B cheapest) with drives at 2x
    capB = R["capex_base"]["B"]["drives"]
    gap = float((res["A"]["lcc"] - res["B"]["lcc"]).mean())
    R["drive_breakeven"] = dict(drive_cost_each=capB / 2, gap=gap, mult=float(1 + gap / capB),
                                each_at_breakeven=float(capB / 2 * (1 + gap / capB)))
    for mlt in (2.0, 3.0):
        LBm = res["B"]["lcc"] + (mlt - 1) * capB * sc["kvfd"]; LEm = res["E3"]["lcc"] + (mlt - 1) * R["capex_base"]["E3"]["drives"] * sc["kvfd"]
        Lall = np.vstack([res["A"]["lcc"], LBm, res["C3"]["lcc"], res["C2"]["lcc"], LEm, res["E2"]["lcc"]])
        R["drive_breakeven"][f"pB_{mlt}"] = float(np.mean(np.argmin(Lall, axis=0) == 1))
    # option D: lag pump operating region; energy closure for every arrangement
    rD = run_option("D", sN, p100, p50); lx = rD["lag_x"][~np.isnan(rD["lag_x"])]
    R["D_lag"] = dict(two_share=float(np.mean(rD["k"] == 2)), lag_bep_p50=float(np.median(lx)),
                      lag_por=float(np.mean((lx >= 0.7) & (lx <= 1.2))))
    clos = {}
    for opt in ("A", "B", "C3", "E3"):
        r_ = run_option(opt, sN, p100, p50); pmp = r_["pump"]; vf = ETA_VFD if opt in ("B", "E3") else 1.0
        hyd_kw = r_["k"] * r_["q"] / 3600 * sN["rho"] * M.G * pmp.head(r_["q"], r_["n"]) / pmp.eta(r_["q"], r_["n"]) / 1000
        clos[opt] = float(np.max(np.abs(r_["P_el"] * ETA_MOTOR * vf - hyd_kw - 0 * r_["recirc"])))
    R["check"]["closure_all"] = clos
    R["scen_inputs"] = {k: dict(p5=float(np.percentile(v, 5)), p50=float(np.median(v)), p95=float(np.percentile(v, 95))) for k, v in sc.items()}
    R["const"] = dict(LSW=LSW, TMAN=TMAN, CREP_VFD=CREP_VFD, PVF=PVF, HAND_PUMP=HAND_PUMP, HAND_VALVE=HAND_VALVE, INST_VFD=INST_VFD)
    np.savez_compressed("arr_scenarios.npz", **{f"sc_{k}": v for k, v in sc.items()},
                        **{f"{o}_{k}": sim[o][k] for o in OPTIONS for k in ("nfail", "lost_h", "frac_v", "pen")},
                        **{f"{o}_lcc": res[o]["lcc"] for o in OPTIONS})
    json.dump(R, open("arr_results.json", "w"), indent=1, default=float)
    json.dump(F, open("arr_figdata.json", "w"), default=float)
    print(json.dumps({k: R[k] for k in ("rated", "check", "motors", "cap_one_50")}, indent=1, default=float))
    for k, v in hyd.items(): print(k, {a: {b: round(c, 3) for b, c in v[a].items()} for a in ("normal", "turndown")}, {x: v[x] for x in v if x not in ("normal", "turndown")})
    for o, v in R["econ"].items(): print(o, {a: round(b, 3) for a, b in v.items()})
