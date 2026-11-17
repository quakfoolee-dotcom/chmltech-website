"""All results for the paper: rated points, pump and valve checks, sensitivity, convergence, energy and cost. V4.
V4: moderate case at the most likely route (140 m); coverage with design unknowns at minimum and the 400-draw
maximum; operating-plant cases; efficiency sensitivity (55% best efficiency); imports pumpvalve_model.
V2 (red-team fixes): conditional coverage given design unknowns; route-length sensitivity; moderate deterministic
baseline; design pressure with tank relief set pressure and API 610 5% head increase; valve out-of-band shares and
wide-open valve at rated Cv; motor factor 115% for 22-55 kW; 200 repeats for convergence; VFD turndown checks.
Writes results.json (numbers quoted in the paper) and figdata.json (data for the figures)."""
import json
import numpy as np
from scipy import optimize, stats
import pumpvalve_model as M

N = 20000
X = M.sample(N, seed=1)
S = M.system(X)
Qn = M.flow(M.BASE)
MOTORS = [3.0, 4.0, 5.5, 7.5, 11.0, 15.0, 18.5, 22.0, 30.0, 37.0]
ETA_MOTOR, ETA_VFD = 0.92, 0.97
PRICE, LIFE, RATE = 0.09, 20, 0.08                    # C$/kWh (hold H-02), years, discount rate
PVF = (1 - (1 + RATE) ** -LIFE) / RATE
CEPCI_2025 = 810.0
TANK_RELIEF = 0.10                                   # barg, TK-101 pressure-vacuum relief set (hold H-05)                                   # approximate 2025 annual average (1.6% above 2024)
R = {"N": N, "Qn": Qn}


def motor_for(pump):
    """API 610: motor at least 125% of rated power below 22 kW (110% above); also covers end of curve at max density."""
    rmax = M.rho(5.0)
    P_rated = pump.Qr / 3600 * rmax * M.G * pump.Hr / pump.eta(pump.Qr) / 1000
    Qe = 1.2 * pump.Qbep
    P_eoc = Qe / 3600 * rmax * M.G * pump.head(Qe) / pump.eta(Qe) / 1000
    need = max(P_rated * (1.25 if P_rated < 22 else 1.15 if P_rated <= 55 else 1.10), P_eoc)
    return next(m for m in MOTORS if m >= need), P_rated, P_eoc


def design_pressure(pump):
    """Max discharge pressure = max suction pressure (full tank at the tank relief set pressure) + shutoff head with the
    API 610 5% head increase at max density (barg); design pressure = +10%, rounded up to 0.5 bar."""
    w = dict(M.BASE, level=7.5, blanket=TANK_RELIEF, T=5.0)
    s = M.system(w, 0.001)
    pmax = (s["p_suc"] - M.P_ATM) / 1e5 + 1.05 * pump.shutoff() * M.rho(5.0) * M.G / 1e5
    return pmax, np.ceil(pmax * 1.10 * 2) / 2


def throttle(pump, X, Q=None):
    o = M.operate(X, pump, Q)
    o["P_el"] = o["P_shaft"] / ETA_MOTOR
    return o


def vfd(pump, X, Q=None):
    """No control valve: solve the speed at which the pump curve meets the system curve (plus the 0.0 bar valve)."""
    s = M.system(X, Q)
    Hr, Qr, sh = pump.Hr, pump.Qr, M.Pump.SHUT
    n = np.sqrt((s["H_sys"] / Hr + (sh - 1) * (s["Q"] / Qr) ** 2) / sh)
    eta = pump.eta(s["Q"], n)
    P_shaft = s["Q"] / 3600 * s["rho"] * M.G * s["H_sys"] / eta / 1000
    return dict(s, n=n, eta=eta, P_shaft=P_shaft, P_el=P_shaft / (ETA_MOTOR * ETA_VFD))


def capex(pump, motor_kw, valve, with_vfd):
    """Purchased cost, C$ 2026. Towler & Sinnott (2nd ed., US Gulf Coast, Jan 2010, CEPCI 532.9) for pump and
    explosion-proof motor, escalated with CEPCI and converted at 1.38 C$/US$; valve and VFD are budget prices (hold H-03)."""
    esc = CEPCI_2025 / 532.9 * 1.38
    S = pump.Qr / 3.6                                       # L/s
    pump_c = (8000 + 240 * S ** 0.9) * esc
    motor_c = (-1100 + 2100 * motor_kw ** 0.6) * esc
    valve_c = {1.0: 9000, 1.5: 11000, 2.0: 13500}[valve["size"]] if valve else 0.0
    vfd_c = (2500 + 300 * motor_kw) if with_vfd else 0.0
    return dict(pumps=2 * pump_c, motors=2 * motor_c, valve=valve_c, vfd=2 * vfd_c if with_vfd else 0.0)


def design(name, Qr, Hr, use_vfd=False):
    pump = M.Pump(Qr, Hr)
    mk, P_rated, P_eoc = motor_for(pump)
    pmax, pdes = design_pressure(pump)
    d = dict(name=name, Qr=Qr, Hr=Hr, shutoff=pump.shutoff(), motor=mk, P_rated=P_rated, P_eoc=P_eoc,
             p_dis_max=pmax, p_design=pdes)
    if use_vfd:
        o = vfd(pump, X); lo = vfd(pump, X, Q=M.TURNDOWN * S["Q"])
        d.update(speed_p1=float(np.percentile(o["n"], 1)), speed_p99=float(np.percentile(o["n"], 99)),
                 speed_turndown_p1=float(np.percentile(lo["n"], 1)), valve=None, deliver_share=float(np.mean(o["n"] <= 1.0)))
    else:
        o = throttle(pump, X); lo = throttle(pump, X, Q=M.TURNDOWN * S["Q"])
        dpb = np.concatenate([o["dp_valve"], lo["dp_valve"]])
        v = M.size_valve(np.concatenate([o["Q"], lo["Q"]]), np.concatenate([o["rho"], lo["rho"]]), dpb,
                         np.concatenate([o["p1"], lo["p1"]]), np.concatenate([o["pv"], lo["pv"]]))
        n = len(o["Q"]); op, opl = v["open"][:n], v["open"][n:]
        d.update(valve=dict(size=v["size"], cv=v["cv"], fp=v["fp"], cv_req_p50=float(np.median(v["cv_req"][:n])),
                            cv_req_p99=float(np.percentile(v["cv_req"][:n], 99)),
                            open_p1=float(np.percentile(op, 1)), open_p50=float(np.median(op)), open_p99=float(np.percentile(op, 99)),
                            open_turndown_p1=float(np.percentile(opl, 1)), open_turndown_p50=float(np.median(opl)),
                            share_above_85=float(np.mean(op > 0.85)), share_above_90=float(np.mean(op > 0.90)),
                            share_full=float(np.mean(op >= 1.0)), share_below_10=float(np.mean(np.concatenate([op, opl]) < 0.10)),
                            xF_p99=float(np.percentile(v["xF"], 99)), choked_share=v["choked"],
                            cav_share=float(np.mean(v["xF"] >= M.XFZ)), dp_p50=float(np.median(o["dp_valve"])),
                            dp_p99=float(np.percentile(o["dp_valve"], 99)), deliver_share=float(np.mean(o["dp_valve"] > 0))),
                 P_throttle_mean=float(np.mean(o["P_throttle"])))
        d["_open"] = op; d["_open_lo"] = opl
    d.update(eta_mean=float(np.mean(o["eta"])), P_el_mean=float(np.mean(o["P_el"])),
             bep_ratio_p50=float(np.median(o["Q"] / pump.Qbep)), bep_ratio_turndown=float(np.median(lo["Q"] / pump.Qbep)),
             npsh_margin_min=float(np.min(M.operate(X, pump)["npsh_margin"])),
             npsh_ratio_min=float(np.min(M.system(X)["npsha"] / pump.npshr(M.system(X)["Q"]))),
             mcsf_ok=bool(np.all(lo["Q"] >= 0.30 * pump.Qbep)),
             bep_ratio_turndown_p1=float(np.percentile(lo["Q"] / pump.Qbep, 1)))
    d["energy_cy"] = d["P_el_mean"] * M.HOURS * PRICE
    c = capex(pump, mk, d["valve"], use_vfd); d["capex"] = c; d["capex_total"] = sum(c.values())
    d["lcc"] = d["capex_total"] + d["energy_cy"] * PVF
    return d, pump


# ---------- rated points ----------
Qs, Hs, info = M.rated_stacked()
R["stacked"] = dict(Qr=Qs, Hr=Hs, **info)
for p in (90, 95, 99):
    Qr, Hr, _ = M.rated_mc(X, p); R[f"mc{p}"] = dict(Qr=Qr, Hr=Hr)
R["base_head"] = float(M.system(M.BASE)["H_sys"])
R["base_parts"] = {k: float(v) for k, v in M.system(M.BASE)["parts"].items()}
R["H_sys_pct"] = {p: float(np.percentile(S["H_sys"], p)) for p in (1, 5, 50, 95, 99)}
R["Q_pct"] = {p: float(np.percentile(S["Q"], p)) for p in (1, 5, 50, 95, 99)}
R["npsha_min"] = float(S["npsha"].min()); R["npsha_p1"] = float(np.percentile(S["npsha"], 1))

designs = {}
for key, (Qr, Hr, v) in {"stacked": (Qs, Hs, False), "mc90": (*M.rated_mc(X, 90)[:2], False),
                          "mc95": (*M.rated_mc(X, 95)[:2], False), "mc99": (*M.rated_mc(X, 99)[:2], False),
                          "stacked_vfd": (Qs, Hs, True), "mc95_vfd": (*M.rated_mc(X, 95)[:2], True)}.items():
    designs[key], _ = design(key, Qr, Hr, v)
fig_open = {k: (designs[k].pop("_open").tolist()[:4000], designs[k].pop("_open_lo").tolist()[:4000])
            for k in ("stacked", "mc95")}
for k in designs: designs[k].pop("_open", None); designs[k].pop("_open_lo", None)
R["designs"] = designs

# ---------- upset: can the P95 pump deliver the stacked worst case? ----------
p95 = M.Pump(R["mc95"]["Qr"], R["mc95"]["Hr"])
w = dict(M.WORST)
def short(Q, pump, dpv=M.DP_VALVE_MIN): s = M.system(w, Q); return pump.head(Q) - s["H_sys"] - dpv * 1e5 / (s["rho"] * M.G)
Qmax = optimize.brentq(short, 1.0, 20.0, args=(p95,))
VBORE, VCV = 38.1, R["designs"]["mc95"]["valve"]["cv"]
def short_open(Q, pump):                                           # valve fully open at its rated Cv
    s = M.system(w, Q); return pump.head(Q) - s["H_sys"] - M.wide_open_dp(Q, s["rho"], VCV, VBORE) * 1e5 / (s["rho"] * M.G)
Qmax0 = optimize.brentq(short_open, 1.0, 20.0, args=(p95,))
p95b = M.Pump(R["mc95"]["Qr"], R["mc95"]["Hr"] * 1.05)              # API 610: 5% head increase by a new impeller
Qmax_imp = optimize.brentq(short, 1.0, 20.0, args=(p95b,))
Qmax_imp0 = optimize.brentq(short_open, 1.0, 20.0, args=(p95b,))
R["upset"] = dict(Q_worst=float(M.flow(w)), Q_stacked_rated=Qs, Qmax_P95_with_valve=Qmax, Qmax_P95_valve_open=Qmax0,
                  Qmax_P95_bigger_impeller=Qmax_imp, Qmax_P95_bigger_impeller_valve_open=Qmax_imp0, share_cases_short=float(np.mean(M.operate(X, p95)["dp_valve"] < M.DP_VALVE_MIN)),
                  share_cases_undeliverable=float(np.mean(M.operate(X, p95)["dp_valve"] < 0)))

# ---------- sensitivity: one at a time (P5 and P95 of each input, others at base) and Spearman ----------
need = S["H_sys"] + M.DP_VALVE_MIN * 1e5 / (S["rho"] * M.G)
tor = []
for k, (kind, a) in M.INPUTS.items():
    lo, hi = M.ppf(kind, a, 0.05), M.ppf(kind, a, 0.95)
    def h(v):
        x = dict(M.BASE); x[k] = v
        if k == "rate" or k == "recycle": pass
        s = M.system(x); return float(s["H_sys"] + M.DP_VALVE_MIN * 1e5 / (s["rho"] * M.G))
    rs = stats.spearmanr(X[k], need).statistic
    tor.append(dict(name=k, lo=float(lo), hi=float(hi), h_lo=h(lo), h_hi=h(hi), spearman=float(rs)))
base_need = float(M.system(M.BASE)["H_sys"] + M.DP_VALVE_MIN * 1e5 / (M.rho(20) * M.G))
R["tornado_base"] = base_need; R["tornado"] = sorted(tor, key=lambda t: -abs(t["h_hi"] - t["h_lo"]))

# ---------- convergence of the P95 rated head ----------
conv = []
rng = np.random.default_rng(5)
for n in [100, 200, 500, 1000, 2000, 5000, 10000, 20000]:
    reps = [M.rated_mc(M.sample(n, seed=1000 + r), 95)[1] for r in range(200)]
    conv.append(dict(n=n, mean=float(np.mean(reps)), lo=float(np.percentile(reps, 2.5)), hi=float(np.percentile(reps, 97.5))))
R["convergence"] = conv

# ---------- correlation effect: same inputs, independent ----------
saved = dict(M.CORR); M.CORR.clear()
R["mc95_independent"] = M.rated_mc(M.sample(N, seed=1), 95)[1]
M.CORR.update(saved)


# ---------- moderate deterministic baseline: 110% flow, worst equipment drops, 10% on friction only ----------
mod = dict(M.BASE, p_rx=4.25, level=0.5, T=5.0, blanket=0.02, L_dis=140.0, K_dis=8.0, eps=0.15e-3, foul=1.5, strainer=5.0)
Qm = 1.10 * Qn; sm = M.system(mod, Qm)
fric = sm["dp_dis"] / (sm["rho"] * M.G) - (0.30e5 * 1.5 * (Qm / 10) ** 1.8 * (sm["mu"] / M.mu(20.0)) ** 0.2 + 0.15e5 * (Qm / 10) ** 2) / (sm["rho"] * M.G)
Hm = sm["H_sys"] + 0.10 * fric + M.DP_VALVE_MIN * 1e5 / (sm["rho"] * M.G)
R["moderate"] = dict(Qr=float(Qm), Hr=float(Hm), friction=float(fric))
designs["moderate"], _ = design("moderate", float(Qm), float(Hm), False)
designs["moderate"].pop("_open", None); designs["moderate"].pop("_open_lo", None)

# ---------- coverage of the P95 pump once the design unknowns are fixed ----------
DESIGN = ["L_dis", "K_dis", "eps", "foul", "strainer"]
def coverage(fix, n=20000, seed=7):
    Y = M.sample(n, seed=seed)
    for k, v in fix.items(): Y[k] = np.full(n, v)
    o = M.operate(Y, p95)
    return float(np.mean(o["dp_valve"] >= M.DP_VALVE_MIN)), float(np.mean(o["dp_valve"] < M.wide_open_dp(o["Q"], o["rho"], VCV, VBORE)))
cov = {"all_random": coverage({})}
cov["unknowns_at_P95"] = coverage({k: float(M.ppf(*M.INPUTS[k], 0.95)) for k in DESIGN})
cov["route_fittings_roughness_max"] = coverage({k: M.WORST[k] for k in ("L_dis", "K_dis", "eps")})
cov["all_unknowns_max"] = coverage({k: M.WORST[k] for k in DESIGN})
rng = np.random.default_rng(11); draws = []
for i in range(400):
    fix = {k: float(M.ppf(*M.INPUTS[k], rng.random())) for k in DESIGN}
    draws.append(coverage(fix, n=4000, seed=100 + i)[0])
cov["over_400_draws"] = dict(mean=float(np.mean(draws)), p5=float(np.percentile(draws, 5)), min=float(np.min(draws)), p95=float(np.percentile(draws, 95)), max=float(np.max(draws)))
cov["all_unknowns_min"] = coverage({k: float(M.ppf(*M.INPUTS[k], 0.0)) for k in DESIGN})
cov["unknowns_at_P5"] = coverage({k: float(M.ppf(*M.INPUTS[k], 0.05)) for k in DESIGN})
# operating plant: route, fittings and roughness measured (taken at their P95), fouling and clogging still drift
meas = {k: float(M.ppf(*M.INPUTS[k], 0.95)) for k in ("L_dis", "K_dis", "eps")}
cov["existing_P95_pump_measured_route"] = coverage(meas)
Ym = M.sample(N, seed=1)
for k, v in meas.items(): Ym[k] = np.full(N, v)
Qrm, Hrm, _ = M.rated_mc(Ym, 95)
p95_saved = p95; p95 = M.Pump(Qrm, Hrm)
cov["rerated_measured_route"] = dict(Qr=float(Qrm), Hr=float(Hrm), coverage=coverage(meas))
p95 = p95_saved
cov["hours_short_all_random"] = cov["all_random"][1] * M.HOURS
R["coverage"] = cov

# ---------- route-length sensitivity ----------
sens = {}
for lab, rng_ in {"100-160-300": (100.0, 160.0, 300.0), "120-200-400": (120.0, 200.0, 400.0)}.items():
    saved_L = M.INPUTS["L_dis"]; M.INPUTS["L_dis"] = ("tri", rng_)
    Y = M.sample(N, seed=1); Ys = M.system(Y); nd = Ys["H_sys"] + M.DP_VALVE_MIN * 1e5 / (Ys["rho"] * M.G)
    lo_, hi_ = M.ppf("tri", rng_, 0.05), M.ppf("tri", rng_, 0.95)
    def hL(v):
        x = dict(M.BASE); x["L_dis"] = v; s_ = M.system(x); return float(s_["H_sys"] + M.DP_VALVE_MIN * 1e5 / (s_["rho"] * M.G))
    sens[lab] = dict(P95=M.rated_mc(Y, 95)[1], swing=hL(hi_) - hL(lo_), spearman=float(stats.spearmanr(Y["L_dis"], nd).statistic))
    M.INPUTS["L_dis"] = saved_L
R["route_sensitivity"] = sens

# ---------- VFD at turndown ----------
lo = vfd(p95, X, Q=M.TURNDOWN * S["Q"])
st = M.system(X, M.TURNDOWN * S["Q"])
R["vfd_turndown"] = dict(head_over_shutoff_p50=float(np.median(st["H_sys"] / (p95.shutoff() * lo["n"] ** 2))),
                         static_share_p50=float(np.median((st["H_sys"] - (st["dp_dis"]) / (st["rho"] * M.G)) / st["H_sys"])),
                         eta_p50=float(np.median(lo["eta"])), speed_min=float(lo["n"].min()))
R["tank_working_m3"] = float(8 * Qn)
# ---------- efficiency sensitivity: the same rated points with a 55% best-efficiency curve ----------
sens55 = {}
for key in ("stacked", "moderate", "mc95"):
    Qr_, Hr_ = designs[key]["Qr"], designs[key]["Hr"]
    pmp = M.Pump(Qr_, Hr_, eta_bep=0.55); mk_, Pr_, _ = motor_for(pmp)
    sens55[key] = dict(motor=mk_, P_rated=float(Pr_), P_el_mean=float(np.mean(throttle(pmp, X)["P_el"])))
R["eff55"] = sens55
json.dump(R, open("results.json", "w"), indent=1, default=float)
fig = dict(need=need[:6000].tolist(), Q=S["Q"][:6000].tolist(), H_sys=S["H_sys"][:6000].tolist(), open=fig_open)
json.dump(fig, open("figdata.json", "w"))
for k, d in designs.items():
    v = d["valve"]
    print(f"{k:12s} Qr {d['Qr']:.2f} Hr {d['Hr']:.1f} shut {d['shutoff']:.0f} motor {d['motor']} Pdes {d['p_design']} eta {d['eta_mean']:.2f} "
          f"Pel {d['P_el_mean']:.2f} kW E C${d['energy_cy']:,.0f} capex C${d['capex_total']:,.0f} LCC C${d['lcc']:,.0f} "
          + (f"valve {v['size']}in Cv{v['cv']} open {v['open_p1']:.2f}-{v['open_p99']:.2f} td {v['open_turndown_p1']:.2f} dp50 {v['dp_p50']:.2f} xF99 {v['xF_p99']:.2f} cav {v['cav_share']:.3f}" if v else
             f"speed {d['speed_p1']:.2f}-{d['speed_p99']:.2f} td {d['speed_turndown_p1']:.2f}"))
print(json.dumps({k: R[k] for k in ("upset", "H_sys_pct", "Q_pct", "npsha_min", "mc95_independent", "base_parts")}, indent=0, default=float))
print([(t["name"], round(t["h_lo"], 1), round(t["h_hi"], 1), round(t["spearman"], 2)) for t in R["tornado"]])
print([(c["n"], round(c["lo"], 2), round(c["hi"], 2)) for c in conv])
