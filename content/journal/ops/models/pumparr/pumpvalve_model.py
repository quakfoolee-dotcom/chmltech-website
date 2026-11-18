"""Monte Carlo sizing of a feed pump and flow control valve for a chemical plant equipment list - Chmltech Online Journal. V4.

V4 (second red team): FCV-101 moved upstream of the preheater E-101, so it handles feed at tank temperature (5-40 C,
the range of the property correlations) and its outlet pressure includes the E-101 drop; pump best efficiency 40%
(typical for nq ~ 6) instead of 55%; module renamed from mcfeed.py.
V3: wording only (chemical-plant framing).

V2 (red-team fixes): Fp iterated on the required Cv; choked limit uses (FLP/Fp)^2; valve selection reports the pooled
normal + turndown rule; wide-open valve modelled at its rated Cv; tank relief set pressure for design pressure.

System (a 50,000 t/y chemical plant, design rate 6,250 kg/h of product):
  TK-101 feed tank (N2 blanket) -> suction strainer -> P-101A/B centrifugal pump -> FE-101 Coriolis meter
  -> FCV-101 flow control valve -> E-101 feed preheater (tube side) -> R-101 reactor at 4 barg, nozzle 14 m above pump.
Hydraulics: Darcy-Weisbach with Colebrook friction factor, K-method fittings, equipment pressure drops scaled with flow.
Control valve: IEC 60534-2-1 liquid sizing (Cv units), piping geometry factor Fp, choked-flow and cavitation checks.
Inputs: correlated by a Gaussian copula (production rate with reactor pressure; temperature drives density,
viscosity and vapour pressure). Pump curves are illustrative generic shapes, not a vendor's curve (hold H-01).
"""
import numpy as np
from scipy import stats, optimize

G = 9.81
PA_PER_BAR = 1e5
# ---------- design basis ----------
PRODUCT_KGH = 6250.0          # design rate (Chmltech design basis post)
YIELD = 0.85                  # kg product per kg fresh feed
HOURS = 8000.0                # operating hours a year
TURNDOWN = 0.5                # plant must run at 50% of design rate
D_SUC, D_DIS = 0.0779, 0.0525  # m, 3" and 2" Sch 40
L_SUC, K_SUC = 12.0, 2.0      # suction line: entrance, two elbows, gate valve
Z_TANK_BOTTOM = 1.0           # m, tank bottom above pump centreline
Z_REACTOR = 14.0              # m, reactor feed nozzle above pump centreline
P_ATM = 101.325e3


# ---------- fluid: organic feed blend, properties as functions of temperature (deg C) ----------
def rho(T): return 900.0 - 0.95 * (T - 20.0)                    # kg/m3
def mu(T): return 1.6e-3 * np.exp(-0.018 * (T - 20.0))           # Pa.s
def pv(T): return 3.2e3 * np.exp(0.046 * (T - 20.0))             # Pa abs


# ---------- uncertain inputs: name -> (kind, args); the base case uses the most likely value ----------
INPUTS = {
    "rate":     ("tri", (0.85, 1.00, 1.10)),    # production rate / design rate (operations)
    "recycle":  ("uni", (0.15, 0.25)),          # recycle / fresh feed
    "T":        ("uni", (5.0, 40.0)),           # feed temperature, deg C (outdoor tank, BC seasons)
    "p_rx":     ("nor", (4.0, 0.15)),           # reactor pressure, barg
    "level":    ("uni", (0.5, 7.5)),            # liquid level above tank bottom, m
    "blanket":  ("uni", (0.02, 0.05)),          # N2 blanket, barg
    "L_dis":    ("tri", (120.0, 140.0, 180.0)), # discharge equivalent route length, m (route not final)
    "K_dis":    ("tri", (6.0, 8.0, 12.0)),      # discharge fittings, sum of K
    "eps":      ("uni", (0.045e-3, 0.15e-3)),   # pipe roughness, m (new to aged carbon steel)
    "foul":     ("uni", (1.0, 1.5)),            # E-101 tube-side pressure-drop multiplier (clean to fouled)
    "strainer": ("uni", (1.0, 5.0)),            # suction strainer clogging multiplier
}
BASE = {"rate": 1.0, "recycle": 0.20, "T": 20.0, "p_rx": 4.0, "level": 4.0, "blanket": 0.035, "L_dis": 140.0,
        "K_dis": 8.0, "eps": 0.045e-3, "foul": 1.0, "strainer": 1.0}
WORST = {"rate": 1.10, "recycle": 0.25, "T": 5.0, "p_rx": 4.45, "level": 0.5, "blanket": 0.02, "L_dis": 180.0,
         "K_dis": 12.0, "eps": 0.15e-3, "foul": 1.5, "strainer": 5.0}
CORR = {("rate", "p_rx"): 0.5, ("rate", "recycle"): 0.3}        # Gaussian-copula rank correlations


def ppf(kind, a, u):
    if kind == "uni": return a[0] + (a[1] - a[0]) * u
    if kind == "nor": return stats.norm.ppf(u, a[0], a[1])
    lo, mode, hi = a
    return stats.triang.ppf(u, (mode - lo) / (hi - lo), lo, hi - lo)


def sample(n, seed=1):
    names = list(INPUTS)
    C = np.eye(len(names))
    for (a, b), r in CORR.items():
        i, j = names.index(a), names.index(b)
        C[i, j] = C[j, i] = 2 * np.sin(np.pi * r / 6)            # Spearman -> Pearson for normal scores
    z = np.random.default_rng(seed).multivariate_normal(np.zeros(len(names)), C, size=n)
    u = np.clip(stats.norm.cdf(z), 1e-9, 1 - 1e-9)
    return {k: ppf(*INPUTS[k], u[:, i]) for i, k in enumerate(names)}


# ---------- hydraulics ----------
def colebrook(Re, rel):
    """Darcy friction factor, Colebrook-White solved by fixed-point iteration (laminar below Re 2,300)."""
    Re = np.asarray(Re, float); f = np.full_like(Re, 0.02)
    for _ in range(30):
        f = (-2.0 * np.log10(rel / 3.7 + 2.51 / (Re * np.sqrt(f)))) ** -2
    return np.where(Re < 2300, 64 / Re, f)


def line_dp(Q, D, L, K, eps, r, m):
    """Pa, for Q in m3/h."""
    v = Q / 3600 / (np.pi * D ** 2 / 4)
    Re = r * v * D / m
    return (colebrook(Re, eps / D) * L / D + K) * r * v ** 2 / 2


def flow(x):
    """Feed flow, m3/h."""
    return PRODUCT_KGH * x["rate"] / YIELD * (1 + x["recycle"]) / rho(x["T"])


def system(x, Q=None):
    """Return dict of pressures (Pa) and heads at flow Q (default: the case's own demand flow), valve excluded."""
    T = x["T"]; r, m = rho(T), mu(T)
    Q = flow(x) if Q is None else Q
    q10 = Q / 10.0
    dp_suc = line_dp(Q, D_SUC, L_SUC, K_SUC, x["eps"], r, m)
    dp_str = 0.02e5 * x["strainer"] * q10 ** 2
    dp_dis = line_dp(Q, D_DIS, x["L_dis"], x["K_dis"], x["eps"], r, m)
    dp_meter = 0.15e5 * q10 ** 2
    dp_hx = 0.30e5 * x["foul"] * q10 ** 1.8 * (m / mu(20.0)) ** 0.2
    dp_nozzle = 0.20e5 * q10 ** 2
    p_suc = P_ATM + x["blanket"] * 1e5 + r * G * (Z_TANK_BOTTOM + x["level"]) - dp_suc - dp_str      # Pa abs at pump
    p_end = P_ATM + x["p_rx"] * 1e5 + r * G * Z_REACTOR + dp_nozzle                                   # Pa abs needed after FCV...
    p_up_valve_need = p_end                                                                          # (valve sits just before nozzle)
    H_sys = (p_end + dp_dis + dp_meter + dp_hx - p_suc) / (r * G)    # pump head needed with zero valve drop, m
    npsha = (p_suc - pv(T)) / (r * G)
    return dict(Q=Q, rho=r, mu=m, H_sys=H_sys, p_suc=p_suc, p_end=p_end, dp_hx=dp_hx, dp_dis=dp_dis + dp_meter + dp_hx,
                npsha=npsha, pv=pv(T), parts=dict(static=(p_end - P_ATM - x["p_rx"] * 1e5 - dp_nozzle) / (r * G),
                rx=x["p_rx"] * 1e5 / (r * G), pipe=(dp_dis + dp_suc) / (r * G), hx=dp_hx / (r * G),
                meter=dp_meter / (r * G), strainer=dp_str / (r * G), nozzle=dp_nozzle / (r * G),
                suction_static=-(x["blanket"] * 1e5 + r * G * (Z_TANK_BOTTOM + x["level"])) / (r * G)))


# ---------- pump: illustrative generic curve through the rated point ----------
class Pump:
    """H = Hr (1.20 - 0.20 (Q/Qr)^2) at rated speed; BEP at 1.05 Qr; eta = eta_bep (2x - x^2), x = Q / Qbep.
    NPSHr = 2.0 m at BEP rising with flow. Speed ratio n scales by the affinity laws."""
    SHUT = 1.20

    def __init__(self, Qr, Hr, eta_bep=0.40, npshr_bep=2.0):
        self.Qr, self.Hr, self.eta_bep, self.npshr_bep = Qr, Hr, eta_bep, npshr_bep
        self.Qbep = 1.05 * Qr

    def head(self, Q, n=1.0):
        return self.Hr * (self.SHUT * n ** 2 - (self.SHUT - 1) * (Q / self.Qr) ** 2)

    def eta(self, Q, n=1.0):
        x = Q / (self.Qbep * n)
        return np.clip(self.eta_bep * (2 * x - x ** 2), 0.05, None)

    def npshr(self, Q, n=1.0):
        x = Q / (self.Qbep * n)
        return self.npshr_bep * n ** 2 * (0.5 + 0.5 * x ** 2)

    def shutoff(self, n=1.0): return self.Hr * self.SHUT * n ** 2


# ---------- control valve: IEC 60534-2-1, liquids, Cv units (N1 = 0.865 for m3/h and bar) ----------
N1, N2 = 0.865, 0.00214
VALVES = [  # size (in), body bore (mm), rated Cv of the trims offered (illustrative globe valve family)
    (1.0, 25.4, [6.0, 10.0, 16.0]), (1.5, 38.1, [16.0, 25.0, 34.0]), (2.0, 50.8, [34.0, 46.0, 60.0])]
FL, R_EQ = 0.90, 50.0       # liquid pressure recovery factor (globe, flow to open); equal-% inherent rangeability
XFZ = 0.60                  # incipient-cavitation pressure differential ratio (typical small globe trim)


def Fp(Cv, d_valve_mm, D_pipe_mm=52.5):
    """Piping geometry factor for concentric reducers (IEC 60534-2-1, eq. for sum of K)."""
    if d_valve_mm >= D_pipe_mm - 1: return np.ones_like(np.asarray(Cv, float))
    beta2 = (d_valve_mm / D_pipe_mm) ** 2
    sumK = 1.5 * (1 - beta2) ** 2          # K1 + K2 for inlet and outlet reducers
    return (1 + sumK / N2 * (np.asarray(Cv) / d_valve_mm ** 2) ** 2) ** -0.5


def cv_required(Q, rho_, dp_bar, Fp_=1.0):
    return Q / (N1 * Fp_) * np.sqrt((rho_ / 1000.0) / np.maximum(dp_bar, 1e-6))


def ff(pv_pa, pc_pa=4.1e6):
    return 0.96 - 0.28 * np.sqrt(pv_pa / pc_pa)


def opening(cv_req, cv_rated):
    """Equal-percentage inherent characteristic: Cv/Cv_rated = R^(x-1)."""
    return 1 + np.log(np.maximum(cv_req, 1e-9) / cv_rated) / np.log(R_EQ)


# ---------- case evaluation with a chosen pump (throttling control) ----------
def operate(x, pump, Q=None, n=1.0):
    s = system(x, Q)
    Hp = pump.head(s["Q"], n)
    dp_valve = (Hp - s["H_sys"]) * s["rho"] * G / PA_PER_BAR                       # bar available across FCV-101
    p1 = (s["p_end"] + s["dp_hx"]) / PA_PER_BAR + dp_valve                          # bar abs at valve inlet (E-101 downstream)
    eta = pump.eta(s["Q"], n)
    P_shaft = s["Q"] / 3600 * s["rho"] * G * Hp / eta / 1000                         # kW
    P_throttle = s["Q"] / 3600 * dp_valve * PA_PER_BAR / 1000                        # hydraulic kW lost in valve
    return dict(s, Hp=Hp, dp_valve=dp_valve, p1=p1, eta=eta, P_shaft=P_shaft, P_throttle=P_throttle,
                npsh_margin=s["npsha"] - pump.npshr(s["Q"], n))


def fp_iter(Q, rho_, dp_bar, bore):
    """Required Cv with the piping geometry factor evaluated at that Cv (IEC 60534-2-1 iteration)."""
    cv = cv_required(Q, rho_, dp_bar)
    for _ in range(15):
        fp = Fp(cv, bore); cv = cv_required(Q, rho_, dp_bar, fp)
    return cv, Fp(cv, bore)


def flp(cv, bore, D_pipe_mm=52.5):
    """Combined liquid pressure recovery and piping geometry factor FLP (inlet reducer only)."""
    if bore >= D_pipe_mm - 1: return np.full_like(np.asarray(cv, float), FL)
    beta2 = (bore / D_pipe_mm) ** 2
    K1 = 0.5 * (1 - beta2) ** 2 + (1 - beta2 ** 2)          # inlet reducer + Bernoulli coefficient
    return FL / np.sqrt(1 + FL ** 2 / N2 * K1 * (np.asarray(cv) / bore ** 2) ** 2)


def size_valve(Q, rho_, dp_bar, p1_bar, pv_pa, open_max=0.85):
    """Smallest valve and trim in the family whose 99th-percentile case, over the pooled normal and turndown cases,
    is at most open_max open (equal-percentage characteristic)."""
    for size, bore, trims in VALVES:
        for cv_r in trims:
            cvq, fp = fp_iter(Q, rho_, dp_bar, bore)
            if np.percentile(cvq, 99) <= cv_r * R_EQ ** (open_max - 1):
                x_open = opening(cvq, cv_r)
                fl_eff = flp(cvq, bore) / fp
                return dict(size=size, bore=bore, cv=cv_r, fp=float(np.median(fp)), cv_req=cvq, open=x_open,
                            choked=float(np.mean(dp_bar >= fl_eff ** 2 * (p1_bar - ff(pv_pa) * pv_pa / 1e5))),
                            xF=dp_bar / (p1_bar - pv_pa / 1e5))
    raise ValueError("no valve in the family fits")


def wide_open_dp(Q, rho_, cv_rated, bore):
    """Pressure drop (bar) across the valve fully open at flow Q."""
    fp = Fp(cv_rated, bore)
    return (Q / (N1 * fp * cv_rated)) ** 2 * (rho_ / 1000.0)


# ---------- rated points ----------
DP_VALVE_MIN = 0.7          # bar the control valve keeps at the case's own flow (control authority)


def rated_mc(X, p=95, q_p=None):
    """Rated flow = P(p) of demand flow; rated head = smallest Hr such that a p-percent share of cases still has
    DP_VALVE_MIN across the valve at their own flow on a curve of this shape."""
    s = system(X)
    Qr = np.percentile(s["Q"], p if q_p is None else q_p)
    need = s["H_sys"] + DP_VALVE_MIN * PA_PER_BAR / (s["rho"] * G)
    Hr_i = need / (Pump.SHUT - (Pump.SHUT - 1) * (s["Q"] / Qr) ** 2)
    return Qr, float(np.percentile(Hr_i, p)), s


def rated_stacked(flow_margin=1.20, head_margin=1.10):
    """Common design practice: rated flow 120% of normal; every input at its worst value at once; valve allowance
    of the larger of 0.7 bar and 25% of the dynamic loss; then 10% on head."""
    Qn = flow(BASE)
    Qr = flow_margin * Qn
    w = dict(WORST); s = system(w, Qr)
    dyn = s["dp_dis"] / PA_PER_BAR
    allow = max(DP_VALVE_MIN, 0.25 * dyn)
    Hr = head_margin * (s["H_sys"] + allow * PA_PER_BAR / (s["rho"] * G))
    return float(Qr), float(Hr), dict(Qn=float(Qn), allowance_bar=allow, H_sys_worst=float(s["H_sys"]))


if __name__ == "__main__":
    X = sample(20000)
    print("normal flow %.2f m3/h, base system head %.1f m" % (flow(BASE), system(BASE)["H_sys"]))
    for p in (90, 95, 99):
        Qr, Hr, _ = rated_mc(X, p); print(f"MC P{p}: {Qr:.2f} m3/h at {Hr:.1f} m")
    print("stacked:", rated_stacked())
