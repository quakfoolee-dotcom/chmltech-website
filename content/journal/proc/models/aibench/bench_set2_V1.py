"""Tier 2 of the benchmark: tasks with missing properties, hidden traps, infeasible or inconsistent data,
standard-size choices, iteration and checking someone else's calculation. Writes tasks2.md and reference2.json."""
import json, math
from scipy.optimize import brentq
from iapws import IAPWS97
from iapws.iapws95 import IAPWS95

g = 9.80665; T = []
def add(i, cat, diff, prompt, ans): T.append(dict(id=i, category=cat, difficulty=diff, prompt=prompt, answers=ans))

# 21 property: toluene vapour pressure (NIST Antoine, 308-384 K)
pv = 10 ** (4.07827 - 1343.943 / (353.15 - 53.773)) * 100
add(21, "Properties", "medium", "No property data are given. What is the vapour pressure of toluene at 80 C, in kPa(a)?", {"pv_kPa": (pv, "kPa", 0.05)})
# 22 water properties at 60 C
w = IAPWS95(T=333.15, P=0.101325)
add(22, "Properties", "easy", "No property data are given. What are the density (kg/m3) and dynamic viscosity (mPa.s) of liquid water at 60 C and atmospheric pressure?",
    {"rho_kgm3": (w.rho, "kg/m3", 0.005), "mu_mPas": (w.mu * 1e3, "mPa.s", 0.05)})
# 23 steam at 10 barg
s = IAPWS97(P=1.101325, x=1); l = IAPWS97(P=1.101325, x=0)
add(23, "Properties", "medium", "No property data are given. For saturated steam at 10 barg (atmospheric 1.01325 bar), what are the saturation temperature (C) and the latent heat of condensation (kJ/kg)?",
    {"Tsat_C": (s.T - 273.15, "C", -0.5), "hfg_kJkg": (s.h - l.h, "kJ/kg", 0.01)})
# 24 infeasible duty
add(24, "Judgement", "medium", "A feed of 6,250 kg/h (cp 2.0 kJ/kg.K) must be heated from 20 C to 150 C in a shell-and-tube exchanger using saturated steam at 3.0 barg as the only heating medium. With U = 500 W/m2.K, what area is required? Give feasible = 1 if the duty can be met, 0 if not, and the area in m2 (give 0 if infeasible).",
    {"feasible": (0.0, "1/0", 0.0), "area_m2": (0.0, "m2", 0.0)})
# 25 inconsistent test data
hyd = 870 * g * (12 / 3600) * 75 / 1000
add(25, "Judgement", "medium", "A pump test sheet records: flow 12.0 m3/h, differential head 75 m, liquid density 870 kg/m3, measured shaft power 1.0 kW. What pump efficiency do these figures imply (as a fraction), and are the data physically consistent (1 = yes, 0 = no)?",
    {"efficiency": (hyd / 1.0, "-", 0.02), "consistent": (0.0, "1/0", 0.0)})
# 26 standard pipe size
add(26, "Lines", "medium", "A liquid line carries 25 m3/h. The velocity must not exceed 2.0 m/s. Choose the smallest standard ASME B36.10 Schedule 40 nominal pipe size that meets the limit (no pipe data are given). Give the nominal size in inches and the resulting velocity in m/s.",
    {"nps_in": (3.0, "in", 0.0), "velocity_ms": ((25 / 3600) / (math.pi * 0.07793 ** 2 / 4), "m/s", 0.02)})
# 27 iteration: maximum flow with a flow-dependent coefficient
def tout(m):
    hi = 1500 * (m / 8690) ** 0.8; U = 1 / (1 / hi + 1 / 8000 + 3e-4)
    return 143.7 - (143.7 - 15) * math.exp(-U * 6.0 / (m / 3600 * 2000))
mmax = brentq(lambda m: tout(m) - 80, 1000, 60000)
add(27, "Heat transfer", "hard", "A steam-heated exchanger (steam condensing at 143.7 C) has 6.0 m2 of area. Its tube-side coefficient is 1,500 W/m2.K at 8,690 kg/h and varies with flow to the power 0.8; the condensing coefficient is 8,000 W/m2.K and the fouling resistance 3.0e-4 m2K/W (treat all on one area basis: 1/U = 1/hi + 1/ho + Rf). Liquid cp is 2.0 kJ/kg.K and the inlet is 15 C. What is the largest feed flow (kg/h) that can still be heated to 80 C?",
    {"m_max_kgh": (mmax, "kg/h", 0.02)})
# 28 unit traps
P_tank = 101325 + 2.0 * 6894.757; pv28 = 150 * 133.322; rho28 = 0.80 * 999.0
npsha = (P_tank - pv28) / (rho28 * g) + 6.0 * 0.3048 - 2.5 * 0.3048
add(28, "Pumps", "medium", "A pump draws from a tank at 2.0 psig (atmospheric 101.325 kPa). The liquid has a specific gravity of 0.80 and a vapour pressure of 150 mmHg(a) at pumping temperature. The minimum liquid level is 6.0 ft above the pump centreline and suction friction is 2.5 ft of liquid. What is the NPSH available, in metres?",
    {"npsha_m": (npsha, "m", 0.015)})
# 29 under-specified
add(29, "Judgement", "medium", "Size the control valve for 12 m3/h of a hydrocarbon liquid in the reactor feed line. Give the required Cv, or, if the information given is not enough to size it, give missing_data = 1 and Cv = 0.",
    {"missing_data": (1.0, "1/0", 0.0), "Cv": (0.0, "-", 0.0)})
# 30 real-gas density
from CoolProp.CoolProp import PropsSI                       # Setzmann-Wagner reference equation of state
rho30 = PropsSI("D", "T", 298.15, "P", 51.01325e5, "Methane")
add(30, "Properties", "hard", "No property data are given. Estimate the density of pure methane at 50 barg (atmospheric 1.01325 bar) and 25 C, accounting for non-ideal behaviour, in kg/m3.",
    {"rho_kgm3": (rho30, "kg/m3", 0.05)})
# 31 check a calculation
corr = (101325 + 3500 - 8010) / (881 * g) + 1.5 - 0.6
add(31, "Checking", "medium", "A colleague computed NPSH available as follows: 'Tank pressure 0.035 barg = 3,500 Pa; vapour pressure 8,010 Pa(a); density 881 kg/m3. NPSHa = (3,500 - 8,010)/(881 x 9.81) + 1.5 - 0.6 = 0.38 m. The pump needs NPSHr 3 m, so it will cavitate.' Is the calculation correct (1 = yes, 0 = no)? Give the correct NPSHa in metres.",
    {"correct": (0.0, "1/0", 0.0), "npsha_m": (corr, "m", 0.01)})

ref = {t["id"]: dict(category=t["category"], difficulty=t["difficulty"], answers={k: dict(value=v[0], unit=v[1], tol=v[2]) for k, v in t["answers"].items()}) for t in T}
json.dump(ref, open("reference_set2.json", "w"), indent=1)
lines = ["# Process engineering calculation tasks, set 2", "", "Answer every task. For each, give the numeric answers under the keys listed. Where a task gives no data for a property, use your own engineering knowledge. Use 1/0 for yes/no keys.", ""]
for t in T:
    lines += [f"## Task {t['id']}", t["prompt"], "Answer keys: " + ", ".join(f"{k} [{v[1]}]" for k, v in t["answers"].items()), ""]
open("tasks_set2.md", "w").write("\n".join(lines))
for t in T: print(t["id"], {k: round(v[0], 4) for k, v in t["answers"].items()})
