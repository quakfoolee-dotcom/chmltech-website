"""Process-engineering calculation benchmark for the AI-agent paper (Chmltech Online Journal).
Defines 20 tasks with full input data, computes reference answers in code, writes tasks.md (what the agents see)
and reference.json (answers and tolerances). Python 3 with NumPy, SciPy and iapws."""
import json, math
import numpy as np
from scipy.optimize import brentq
from iapws import IAPWS97

g = 9.80665
T = []   # (id, category, difficulty, prompt, answers: {key: (value, unit, rel_tol)})


def add(i, cat, diff, prompt, ans):
    T.append(dict(id=i, category=cat, difficulty=diff, prompt=prompt, answers=ans))


# 1 pump differential head
rho = 870.0; Ps, Pd = 1.2e5, 6.8e5   # Pa g
H = (Pd - Ps) / (rho * g)
add(1, "Pumps", "easy", "A centrifugal pump handles a liquid of density 870 kg/m3. Suction pressure is 1.2 barg and discharge pressure is 6.8 barg at the pump nozzles, which are at the same elevation; velocity heads are negligible. What is the pump differential head in metres of liquid?",
    {"head_m": (H, "m", 0.01)})

# 2 NPSHa
P_tank = 101325 + 0.035e5; pv = 3.2e3 * math.exp(0.046 * (40 - 20)); rho2 = 900 - 0.95 * 20; z = 1.0 + 0.5; hf = 0.6
npsha = (P_tank - pv) / (rho2 * g) + z - hf
add(2, "Pumps", "medium", "A pump takes suction from a nitrogen-blanketed tank held at 0.035 barg; atmospheric pressure is 101.325 kPa. The liquid is at 40 C, where its vapour pressure is 8.01 kPa(a) and its density is 881 kg/m3. The lowest liquid level is 1.5 m above the pump centreline, and suction line friction at the design flow is 0.6 m of liquid. Calculate the NPSH available in metres.",
    {"npsha_m": ((P_tank - 8.01e3) / (881 * g) + 1.5 - 0.6, "m", 0.01)})

# 3 pump power
Q = 12.0 / 3600; H3 = 75.0; rho3 = 870; eff = 0.62; meff = 0.92
Pshaft = rho3 * g * Q * H3 / eff / 1000; Pel = Pshaft / meff
add(3, "Pumps", "easy", "A pump delivers 12.0 m3/h of liquid of density 870 kg/m3 against a differential head of 75 m. Pump efficiency is 62% and motor efficiency 92%. Give the shaft power and the electrical power drawn, both in kW.",
    {"shaft_kW": (Pshaft, "kW", 0.01), "electrical_kW": (Pel, "kW", 0.01)})

# 4 line pressure drop, Colebrook
D = 0.0525; L = 140.0; eps = 0.045e-3; Qm = 12.0 / 3600; rho4 = 870; mu4 = 1.2e-3
v = Qm / (math.pi * D ** 2 / 4); Re = rho4 * v * D / mu4
f = brentq(lambda f: 1 / math.sqrt(f) + 2 * math.log10(eps / D / 3.7 + 2.51 / (Re * math.sqrt(f))), 1e-4, 0.2)
dp = f * L / D * rho4 * v ** 2 / 2 / 1000
add(4, "Lines", "medium", "Liquid (density 870 kg/m3, viscosity 1.2 mPa.s) flows at 12.0 m3/h through 140 m of straight pipe with inside diameter 52.5 mm and absolute roughness 0.045 mm. Using the Darcy-Weisbach equation with the Colebrook-White friction factor, what is the frictional pressure drop in kPa?",
    {"dp_kPa": (dp, "kPa", 0.02)})

# 5 liquid Kv/Cv
Q5 = 12.0; dp5 = 1.5; sg = 0.87
Kv = Q5 * math.sqrt(sg / dp5); Cv = Kv * 1.156
add(5, "Valves", "easy", "A control valve passes 12.0 m3/h of liquid with specific gravity 0.87 at a pressure drop of 1.5 bar (non-choked, turbulent). Calculate the required Kv (m3/h at 1 bar) and the corresponding Cv (US gpm at 1 psi).",
    {"Kv": (Kv, "m3/h", 0.01), "Cv": (Cv, "US gpm/psi^0.5", 0.01)})

# 6 choked flow check (IEC 60534 / ISA)
P1 = 6.0e5 + 101325; Pv6 = 0.9e5; Pc = 221.2e5; FL = 0.9
FF = 0.96 - 0.28 * math.sqrt(Pv6 / Pc); dpmax = FL ** 2 * (P1 - FF * Pv6) / 1e5
add(6, "Valves", "medium", "A globe valve (liquid pressure recovery factor FL = 0.90) has an upstream pressure of 6.0 barg; atmospheric pressure is 1.01325 bar. The liquid is water at a temperature where its vapour pressure is 0.90 bar(a); critical pressure 221.2 bar(a). Using the IEC 60534 / ISA method with FF = 0.96 - 0.28 sqrt(Pv/Pc), what is the maximum pressure drop for non-choked flow, in bar? Would a pressure drop of 5.2 bar be choked (answer 1 for yes, 0 for no)?",
    {"dp_choked_bar": (dpmax, "bar", 0.01), "choked_at_5.2": (1.0 if 5.2 > dpmax else 0.0, "1/0", 0.0)})

# 7 LMTD and area, condensing steam
m7 = 6250 / 3600; cp = 2.0; Tin, Tout = 20.0, 80.0; Ts = 143.7; U7 = 500.0
Qkw = m7 * cp * (Tout - Tin); lmtd = ((Ts - Tin) - (Ts - Tout)) / math.log((Ts - Tin) / (Ts - Tout)); A7 = Qkw * 1000 / (U7 * lmtd)
add(7, "Heat transfer", "easy", "A liquid feed of 6,250 kg/h (cp 2.0 kJ/kg.K) is heated from 20 C to 80 C by steam condensing at 143.7 C. With an overall coefficient of 500 W/m2.K, find the duty (kW), the LMTD (K) and the area required (m2).",
    {"duty_kW": (Qkw, "kW", 0.01), "lmtd_K": (lmtd, "K", 0.01), "area_m2": (A7, "m2", 0.01)})

# 8 outlet temperature from UA (effectiveness)
UA = 900 * 6.0; m8 = 8690 / 3600; C = m8 * 2000; NTU = UA / C; T8 = 143.7 - (143.7 - 15) * math.exp(-NTU)
add(8, "Heat transfer", "medium", "An existing exchanger has 6.0 m2 of area and, when fouled, an overall coefficient of 900 W/m2.K. It heats 8,690 kg/h of liquid (cp 2.0 kJ/kg.K) entering at 15 C with steam condensing at 143.7 C. What outlet temperature does it reach (C)?",
    {"T_out_C": (T8, "C", -0.5)})

# 9 steam rate
s = IAPWS97(P=(3.0 + 1.01325) / 10, x=1); w = IAPWS97(P=(3.0 + 1.01325) / 10, x=0); hfg = s.h - w.h
ms = Qkw / hfg * 3600
add(9, "Heat transfer", "medium", "Low-pressure saturated steam at 3.0 barg (atmospheric 1.01325 bar) supplies a duty of 208.3 kW, leaving as saturated condensate. Using steam tables, what steam flow is required in kg/h? Also state the saturation temperature in C.",
    {"steam_kgh": (208.3 / hfg * 3600, "kg/h", 0.01), "Tsat_C": (s.T - 273.15, "C", -0.5)})

# 10 recycle mass balance
F = 100.0; Xp = 0.60; rec = 0.98   # kmol/h A fresh, single-pass conversion, separator recovers 98% of unreacted A to recycle
# steady state: reactor feed R0 = F + Rc; unreacted = R0 (1-X); Rc = rec * R0 (1-X)
R0 = F / (1 - rec * (1 - Xp)); Rc = R0 - F; overall = (R0 * Xp) / F
add(10, "Balances", "medium", "Fresh feed of 100 kmol/h of reactant A enters a process. The reactor converts 60% of the A it receives per pass. A separator after the reactor recovers 98% of the unreacted A and recycles it to the reactor inlet; the remaining 2% of unreacted A leaves with the product. At steady state, what are the recycle flow of A (kmol/h) and the overall conversion of the fresh A (as a fraction)?",
    {"recycle_kmolh": (Rc, "kmol/h", 0.01), "overall_conversion": (overall, "-", -0.001)})

# 11 CSTR volume
k = 0.15 / 60; X = 0.9; v0 = 8.0 / 3600
V = v0 * X / (k * (1 - X))
add(11, "Reactors", "easy", "A liquid-phase first-order reaction with rate constant 0.15 min-1 runs in a single CSTR at constant density. Feed is 8.0 m3/h. What reactor liquid volume (m3) gives 90% conversion?",
    {"volume_m3": (V, "m3", 0.01)})

# 12 adiabatic temperature rise
dH = 85.0e3; cA = 2.0; rho12 = 900; cp12 = 2.1e3; X12 = 0.95
dT = cA * 1000 * X12 * dH / (rho12 * cp12)
add(12, "Reactors", "easy", "A feed containing 2.0 kmol/m3 of reactant (density 900 kg/m3, cp 2.1 kJ/kg.K) undergoes an exothermic reaction with heat of reaction -85 kJ/mol. If 95% of the reactant converts with no heat removal, what is the adiabatic temperature rise (K)?",
    {"dT_K": (dT, "K", 0.01)})

# 13 API 521 fire case (US units)
A13 = 450.0; F13 = 1.0; Q13 = 21000 * F13 * A13 ** 0.82; lam = 140.0; W = Q13 / lam
add(13, "Relief", "medium", "Using the API 521 fire-case equation for a vessel with adequate drainage and prompt fire-fighting (Q = 21,000 F A^0.82, Q in BTU/h, A in ft2), find the heat input to a bare vessel (F = 1.0) with 450 ft2 of wetted area, and the relieving rate in lb/h if the liquid's latent heat at relieving conditions is 140 BTU/lb.",
    {"Q_BTUh": (Q13, "BTU/h", 0.01), "W_lbh": (W, "lb/h", 0.01)})

# 14 API 520 vapour orifice (SI)
W14 = 2500.0; Tk = 400.0; Z = 0.95; M = 58.1; P1a = 10.0e2 * 1.1 + 101.325; k14 = 1.12; Kd = 0.975; Kb = 1.0; Kc = 1.0
Ck = 0.03948 * math.sqrt(k14 * (2 / (k14 + 1)) ** ((k14 + 1) / (k14 - 1)))
A14 = W14 / (Ck * Kd * P1a * Kb * Kc) * math.sqrt(Tk * Z / M)
add(14, "Relief", "hard", "Size a relief valve for critical vapour flow per API 520 Part I (SI units): A = W/(C Kd P1 Kb Kc) x sqrt(T Z / M), with A in mm2, W in kg/h, P1 in kPa(a), T in K, and C = 0.03948 sqrt(k (2/(k+1))^((k+1)/(k-1))). Relieving rate 2,500 kg/h; set pressure 10.0 barg with 10% overpressure (atmospheric 101.325 kPa); relieving temperature 400 K; Z = 0.95; M = 58.1; k = 1.12; Kd = 0.975; Kb = Kc = 1.0. What effective orifice area (mm2) is required?",
    {"area_mm2": (A14, "mm2", 0.02)})

# 15 Rachford-Rice flash
z15 = np.array([0.3, 0.5, 0.2]); K15 = np.array([3.5, 0.9, 0.12])
rr = lambda V: np.sum(z15 * (K15 - 1) / (1 + V * (K15 - 1)))
Vf = brentq(rr, 1e-9, 1 - 1e-9); x15 = z15 / (1 + Vf * (K15 - 1))
add(15, "Separation", "medium", "A feed with mole fractions z = (0.30, 0.50, 0.20) is flashed at conditions where the K-values are (3.5, 0.9, 0.12). Solve the Rachford-Rice equation for the vapour fraction V/F, and give the liquid mole fraction of the first component.",
    {"V_over_F": (Vf, "-", 0.01), "x1": (x15[0], "-", 0.01)})

# 16 velocity and Reynolds number in US units
gpm = 50.0; Din = 2.067; Qs = gpm * 3.785411784e-3 / 60; Dm = Din * 0.0254
v16 = Qs / (math.pi * Dm ** 2 / 4); Re16 = 870 * v16 * Dm / 1.2e-3
add(16, "Lines", "easy", "50 US gpm of liquid (density 870 kg/m3, viscosity 1.2 cP) flows in 2-inch Schedule 40 pipe (ID 2.067 in). What are the velocity in m/s and the Reynolds number?",
    {"velocity_ms": (v16, "m/s", 0.01), "Re": (Re16, "-", 0.01)})

# 17 batch heating time with steam jacket
M17 = 8000.0; cp17 = 2.2e3; U17 = 400.0; A17 = 12.0; Ts17 = 143.7; T0, Tf = 20.0, 90.0
t17 = M17 * cp17 / (U17 * A17) * math.log((Ts17 - T0) / (Ts17 - Tf)) / 3600
add(17, "Heat transfer", "medium", "A well-mixed batch of 8,000 kg (cp 2.2 kJ/kg.K) is heated in a jacketed vessel from 20 C to 90 C with steam condensing at 143.7 C in the jacket. U = 400 W/m2.K and the jacket area is 12 m2. Heat losses are negligible. How long does the heating take, in hours?",
    {"time_h": (t17, "h", 0.01)})

# 18 head from psi and gpm Cv (US units)
psi = 35.0; sg18 = 0.87; head_ft = psi * 2.31 / sg18; Cv18 = 50.0 * math.sqrt(sg18 / 12.0)
add(18, "Units", "easy", "A pump develops a differential pressure of 35 psi on a liquid with specific gravity 0.87. What is its head in feet? A valve on the same line passes 50 US gpm at a 12 psi drop: what is its Cv?",
    {"head_ft": (head_ft, "ft", 0.01), "Cv": (Cv18, "-", 0.01)})

# 19 cost scaling
C19 = 1.20e6 * (8.0 / 5.0) ** 0.6 * (800.0 / 600.0)
add(19, "Cost", "easy", "A 5.0 m3 reactor cost US$1.20 million when the cost index was 600. Using the six-tenths rule, estimate the cost of an 8.0 m3 reactor today, with the index at 800.",
    {"cost_USD": (C19, "US$", 0.01)})

# 20 NPV of an energy project
cap = 250000.0; save = 60000.0; r = 0.08; n = 10
npv = -cap + save * (1 - (1 + r) ** -n) / r; pb = cap / save
add(20, "Cost", "easy", "An energy-saving project costs C$250,000 now and saves C$60,000 a year for 10 years (end-of-year), with no salvage value. At an 8% discount rate, what is its NPV (C$), and what is the simple payback (years)?",
    {"npv_CAD": (npv, "C$", 0.01), "payback_y": (pb, "y", 0.01)})

ref = {t["id"]: dict(category=t["category"], difficulty=t["difficulty"], answers={k: dict(value=v[0], unit=v[1], tol=v[2]) for k, v in t["answers"].items()}) for t in T}
json.dump(ref, open("reference_set1.json", "w"), indent=1)
lines = ["# Process engineering calculation tasks", "", "Answer every task. For each, give the numeric answers under the keys listed. Use SI or the units stated.", ""]
for t in T:
    keys = ", ".join(f"{k} [{v[1]}]" for k, v in t["answers"].items())
    lines += [f"## Task {t['id']}", t["prompt"], f"Answer keys: {keys}", ""]
open("tasks_set1.md", "w").write("\n".join(lines))
for t in T: print(t["id"], {k: round(v[0], 4) for k, v in t["answers"].items()})
