"""Total landed cost supplier and freight-mode selection - Chmltech Online Journal (pip install pulp==2.9.0)."""
import math
import pulp

FX, H, Z, CV, RCAP = 1.38, 0.25, 1.645, 1.2, 0.10      # C$/US$, carrying rate, 95% service, daily demand CV, cost of capital
FEU = 7500 * FX + 2200                                   # one 40 ft container from China, C$
LT = {"CN-FCL": (45, 8), "CN-LCL": (55, 12), "MX-TRK": (10, 3), "US-TRK": (6, 2), "CA-TRK": (3, 1)}
TRUCK = {"MX": (300, 0.45), "US": (180, 0.30), "CA": (60, 0)}
BROKER = {"CN": 180, "MX": 90, "US": 90, "CA": 0}
FIXED = {"CN": 8000, "MX": 5000, "US": 3000, "CA": 1500}
DEFECT = {"CN": 0.015, "MX": 0.010, "US": 0.005, "CA": 0.004}
DUTY = {"hardware": 0.05, "steel": 0.25, "aluminum": 0.28, "plastic": 0.065}   # China only: MFN + 25% steel/aluminum surtax
FREQS = [1, 2, 3, 4, 6, 8, 12, 26, 52]
PARTS = {  # qty/yr, m3/unit, kg/unit, class, China MOQ, prices C$/unit
    "operator":  (6400, 0.0012, 0.6, "hardware", 1000, {"CN": 9.6, "MX": 12.6, "US": 14.0, "CA": 14.8}),
    "lock":      (2600, 0.0025, 1.4, "hardware", 500, {"CN": 19.5, "US": 29.5, "CA": 31.0}),
    "reinforce": (9000, 0.0040, 9.0, "steel", 2000, {"CN": 12.2, "US": 13.4, "CA": 14.0}),
    "screen":    (3300, 0.0060, 0.9, "aluminum", 1000, {"CN": 6.8, "MX": 7.5, "US": 8.2, "CA": 8.6}),
    "weather":   (1400, 0.0300, 6.0, "plastic", 300, {"CN": 44.0, "MX": 48.0, "US": 53.0, "CA": 56.0}),
    "spacer":    (900, 0.0400, 12.0, "plastic", 200, {"CN": 132.0, "US": 150.0, "CA": 158.0}),
    "roller":    (1500, 0.0008, 0.5, "hardware", 500, {"CN": 7.0, "MX": 9.3, "US": 10.4, "CA": 10.9}),
    "handle":    (950, 0.0040, 1.6, "hardware", 300, {"CN": 22.0, "MX": 29.0, "US": 33.0, "CA": 35.0}),
}


def cost(k, r, m, n):
    """Annual total landed cost of part k from region r by mode m, n orders a year (FCL container cost added at plan level)."""
    D, m3, kg, cls, moq, p = PARTS[k]; price = p[r]; Q = D / n
    duty = DUTY[cls] if r == "CN" else 0.0
    if m == "FCL":   freight = 0.0
    elif m == "LCL": freight = n * (450 + 160 * max(Q * m3, Q * kg / 1000))
    else:            freight = n * (TRUCK[r][0] + TRUCK[r][1] * Q * kg)
    landed = price * (1 + duty) + (freight + n * BROKER[r]) / D
    L, sL = LT[f"{r}-{m}"]; d = D / 365
    stock = d * L + Q / 2 + Z * math.sqrt(L * (CV * d) ** 2 + d ** 2 * sL ** 2)     # pipeline + cycle + safety
    terms = RCAP * D * price * (0.30 * 35 / 365 if r == "CN" else -30 / 365)        # deposit vs net 30
    return (D * price * (1 + duty) + freight + n * BROKER[r] + DEFECT[r] * D * (price + 15)
            + H * landed * stock + terms)


def options(k):
    D, *_, moq, p = PARTS[k]
    for r in p:
        for m in (["FCL", "LCL"] if r == "CN" else ["TRK"]):
            for n in FREQS:
                if r != "CN" or D / n >= moq:
                    yield (r, m, n)


prob = pulp.LpProblem("total_landed_cost", pulp.LpMinimize)
x = {(k, o): pulp.LpVariable(f"x_{k}_{o[0]}_{o[1]}_{o[2]}", cat="Binary") for k in PARTS for o in options(k)}
y = {N: pulp.LpVariable(f"containers_{N}", cat="Binary") for N in FREQS if N <= 26}   # N full containers a year
u = {r: pulp.LpVariable(f"region_{r}", cat="Binary") for r in FIXED}
for k in PARTS:
    prob += pulp.lpSum(v for (kk, o), v in x.items() if kk == k) == 1                   # one option per part
prob += pulp.lpSum(y.values()) <= 1
for (k, (r, m, n)), v in x.items():
    prob += v <= u[r]
    if m == "FCL":
        prob += v <= y.get(n, 0)                                                          # FCL parts ship with each container
for N in y:
    fcl = [(k, v) for (k, (r, m, n)), v in x.items() if m == "FCL" and n == N]
    prob += pulp.lpSum(v * PARTS[k][0] * PARTS[k][1] for k, v in fcl) <= 58 * N           # m3
    prob += pulp.lpSum(v * PARTS[k][0] * PARTS[k][2] for k, v in fcl) <= 24000 * N        # kg
prob += (pulp.lpSum(cost(k, *o) * v for (k, o), v in x.items()) + pulp.lpSum(FIXED[r] * u[r] for r in u)
         + pulp.lpSum(N * FEU * y[N] for N in y))
prob.solve(pulp.PULP_CBC_CMD(msg=False))

print(f"Total landed cost plan: C${pulp.value(prob.objective):,.0f} a year")
for (k, o), v in x.items():
    if v.value() > 0.5:
        print(f"  {k:10s} {o[0]} {o[1]} {o[2]:>2} orders/yr  C${cost(k, *o):,.0f}")

# Lowest-price rule for comparison: cheapest region, LCL from China, up to 12 orders a year
low = 0.0
for k, (D, m3, kg, cls, moq, p) in PARTS.items():
    r = min(p, key=p.get); n = max(f for f in FREQS if f <= 12 and (r != "CN" or D / f >= moq))
    low += cost(k, r, "LCL" if r == "CN" else "TRK", n)
low += sum(FIXED[r] for r in {min(P[5], key=P[5].get) for P in PARTS.values()})
print(f"Lowest-price plan:      C${low:,.0f} a year")
