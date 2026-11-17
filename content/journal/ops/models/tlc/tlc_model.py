"""Total landed cost sourcing model (composite windows-and-doors plant, BC). V2.

Mixed-integer program: choose one supplier/freight-mode/order-frequency option per part (or a 70/30 dual-source pair),
with China full-container (FCL) shipments consolidated across parts (integer containers per year, volume and weight limits),
supplier-region fixed costs, and total landed cost = purchase + duty/surtax + freight + brokerage + quality
+ carrying cost of pipeline, cycle and safety stock. Solved with PuLP + CBC (bundled with PuLP 2.9).
All money in CAD per year. Parameters are illustrative assumptions for a composite case.
"""
import math, itertools, json
import pulp

FX = 1.38              # CAD per USD (assumption)
H = 0.25               # carrying cost, share of landed value per year
Z = 1.645              # 95% cycle service
CV_DAY = 1.2           # coefficient of variation of daily demand
FEU_USD = 7500.0       # Shanghai -> US West Coast spot, late Oct 2026 (Drewry WCI ~US$7,514), proxy for Vancouver
FEU_LOCAL = 2200.0     # origin + destination charges, drayage to plant, CAD per container
FEU_M3, FEU_KG = 58.0, 24000.0
LCL_RT, LCL_SHIP = 160.0, 450.0          # CAD per revenue tonne (max m3, t) and per shipment
AIR_KG, AIR_SHIP = 7.5, 300.0            # CAD per chargeable kg (max kg, 167 kg/m3) and per shipment
TRUCK = {"MX": (300.0, 0.45), "US": (180.0, 0.30), "CA": (60.0, 0.0)}   # per shipment, per kg
BROKER = {"CN": 180.0, "MX": 90.0, "US": 90.0, "CA": 0.0}               # per import entry
FIXED = {"CN": 8000.0, "MX": 5000.0, "US": 3000.0, "CA": 1500.0}        # supplier management per region used, per year
DEFECT = {"CN": 0.015, "MX": 0.010, "US": 0.005, "CA": 0.004}
RCAP = 0.10            # cost of capital for payment timing, per year
DEPOSIT, DEPOSIT_DAYS, NET_DAYS = 0.30, 35, 30   # China: 30% deposit ~35 days before shipment, balance at shipment; others net 30
REWORK = 15.0                                                            # handling per defective unit, CAD
LT = {("CN", "FCL"): (45, 8), ("CN", "LCL"): (55, 12), ("CN", "AIR"): (10, 3),
      ("MX", "TRK"): (10, 3), ("US", "TRK"): (6, 2), ("CA", "TRK"): (3, 1)}   # calendar days, mean and SD
FREQS = [1, 2, 3, 4, 6, 8, 12, 26, 52]

# part: annual qty, m3/unit, kg/unit, class, MOQ per order (China), prices CAD/unit (FOB origin; CA delivered)
PARTS = {
    "operator":  dict(D=6400, m3=0.0012, kg=0.6, cls="hardware", moq=1000, p={"CN": 9.6, "MX": 12.6, "US": 14.0, "CA": 14.8}, name="Casement operator"),
    "lock":      dict(D=2600, m3=0.0025, kg=1.4, cls="hardware", moq=500,  p={"CN": 19.5, "US": 29.5, "CA": 31.0}, name="Multipoint lock"),
    "reinforce": dict(D=9000, m3=0.0040, kg=9.0, cls="steel",    moq=2000, p={"CN": 12.2, "US": 13.4, "CA": 14.0}, name="Steel reinforcement bar"),
    "screen":    dict(D=3300, m3=0.0060, kg=0.9, cls="aluminum", moq=1000, p={"CN": 6.8, "MX": 7.5, "US": 8.2, "CA": 8.6}, name="Aluminum screen frame kit"),
    "weather":   dict(D=1400, m3=0.0300, kg=6.0, cls="plastic",  moq=300,  p={"CN": 44.0, "MX": 48.0, "US": 53.0, "CA": 56.0}, name="Weatherstrip roll"),
    "spacer":    dict(D=900,  m3=0.0400, kg=12.0, cls="plastic", moq=200,  p={"CN": 132.0, "US": 150.0, "CA": 158.0}, name="Warm-edge spacer box"),
    "roller":    dict(D=1500, m3=0.0008, kg=0.5, cls="hardware", moq=500,  p={"CN": 7.0, "MX": 9.3, "US": 10.4, "CA": 10.9}, name="Patio door roller set"),
    "handle":    dict(D=950,  m3=0.0040, kg=1.6, cls="hardware", moq=300,  p={"CN": 22.0, "MX": 29.0, "US": 33.0, "CA": 35.0}, name="Entry door handleset"),
}
MFN_CN = {"hardware": 0.05, "steel": 0.0, "aluminum": 0.03, "plastic": 0.065}   # illustrative MFN duty on China origin

SCENARIOS = {
    "base":        dict(cn_surtax={"steel": 0.25, "aluminum": 0.25}, us_surtax={}, label="Nov 2026: China steel/aluminum surtax; US inputs remitted"),
    "us_noremit":  dict(cn_surtax={"steel": 0.25, "aluminum": 0.25}, us_surtax={"hardware": 0.25, "steel": 0.25, "aluminum": 0.25, "plastic": 0.25},
                        label="US manufacturing remission ends (25% on US inputs)"),
    "cn_broad":    dict(cn_surtax={"steel": 0.25, "aluminum": 0.25, "hardware": 0.25, "plastic": 0.25}, us_surtax={}, label="25% surtax on all China-origin parts"),
    "none":        dict(cn_surtax={}, us_surtax={}, label="No surtaxes (MFN only)"),
}


def duty_rate(part, region, sc):
    c = part["cls"]
    if region == "CN":
        return MFN_CN[c] + sc["cn_surtax"].get(c, 0.0)
    if region == "US":
        return sc["us_surtax"].get(c, 0.0)
    return 0.0


def stream_cost(k, region, mode, n, share=1.0, sc=None, feu_cad=None, alloc_feu=None):
    """Annual cost of supplying `share` of part k from region by mode with n orders a year.
    For FCL the container cost is handled at plan level; `alloc_feu` gives this part's share (for reporting)."""
    P = PARTS[k]; D = P["D"] * share; p = P["p"][region]
    Q = D / n
    duty = duty_rate(P, region, sc)
    purchase = D * p
    duties = D * p * duty
    if mode == "FCL":
        freight = alloc_feu or 0.0
    elif mode == "LCL":
        rt = max(Q * P["m3"], Q * P["kg"] / 1000)
        freight = n * (LCL_SHIP + LCL_RT * rt)
    elif mode == "AIR":
        ch = max(Q * P["kg"], Q * P["m3"] * 167)
        freight = n * (AIR_SHIP + AIR_KG * ch)
    else:
        a, b = TRUCK[region]
        freight = n * (a + b * Q * P["kg"])
    broker = n * BROKER[region]
    quality = DEFECT[region] * D * (p + REWORK)
    unit_landed = p * (1 + duty) + (freight + broker) / D
    L, sL = LT[(region, mode)]
    d = D / 365; sd = CV_DAY * d
    pipeline = d * L
    cycle = Q / 2
    ss = Z * math.sqrt(L * sd ** 2 + d ** 2 * sL ** 2)
    carry = H * unit_landed * (pipeline + cycle + ss)
    # payment timing: China deposit paid before shipment; balance paid at shipment (pipeline already carried);
    # North American suppliers give net 30 after receipt (a credit against carrying cost)
    terms = RCAP * purchase * (DEPOSIT * DEPOSIT_DAYS / 365 if region == "CN" else -NET_DAYS / 365)
    return dict(purchase=purchase, duty=duties, freight=freight, broker=broker, quality=quality, carry=carry, terms=terms,
                pipeline=pipeline, cycle=cycle, ss=ss, unit_landed=unit_landed, Q=Q)


def options(k, sc, allow_air=False):
    """Single-source options (region, mode, n). FCL options have n = containers/yr (set at plan level)."""
    P = PARTS[k]; out = []
    for r in P["p"]:
        modes = ["FCL", "LCL"] + (["AIR"] if allow_air else []) if r == "CN" else ["TRK"]
        for m in modes:
            for n in FREQS:
                if r == "CN" and P["D"] / n < P["moq"]:
                    continue
                out.append((r, m, n))
    return out


def solve(sc_name="base", feu_usd=FEU_USD, policy="optimal", dual=None, max_cn_share=None, verbose=False):
    """policy: 'optimal' (total landed cost MIP). dual: dict part -> backup region forced at 30% (70/30 split)."""
    sc = SCENARIOS[sc_name]
    feu_cad = feu_usd * FX + FEU_LOCAL
    prob = pulp.LpProblem("tlc", pulp.LpMinimize)
    x = {}; cost = {}; meta = {}
    for k in PARTS:
        shares = [(1.0, None)] if not (dual and k in dual) else [(0.7, "main"), (0.3, dual[k])]
        for (r, m, n) in options(k, sc):
            for share, role in shares:
                if role not in (None, "main"):
                    continue
                if dual and k in dual and r == dual[k]:
                    continue
                c = stream_cost(k, r, m, n, share, sc)
                tot = sum(c[i] for i in ("purchase", "duty", "freight", "broker", "quality", "carry", "terms"))
                v = pulp.LpVariable(f"x_{k}_{r}_{m}_{n}_{int(share*100)}", cat="Binary")
                x[(k, r, m, n, share)] = v; cost[v] = tot; meta[v] = (k, r, m, n, share, c)
        if dual and k in dual:
            b = dual[k]
            for (r, m, n) in options(k, sc):
                if r != b:
                    continue
                c = stream_cost(k, r, m, n, 0.3, sc)
                tot = sum(c[i] for i in ("purchase", "duty", "freight", "broker", "quality", "carry", "terms"))
                v = pulp.LpVariable(f"x_{k}_{r}_{m}_{n}_30b", cat="Binary")
                x[(k, r, m, n, "b")] = v; cost[v] = tot; meta[v] = (k, r, m, n, 0.3, c)
    # each part: one main stream (+ one backup stream if dual)
    for k in PARTS:
        main = [v for key, v in x.items() if key[0] == k and key[4] != "b"]
        prob += pulp.lpSum(main) == 1
        if dual and k in dual:
            prob += pulp.lpSum(v for key, v in x.items() if key[0] == k and key[4] == "b") == 1
    # FCL consolidation: choose N containers/yr; FCL parts ship N times a year
    Ns = [n for n in FREQS if n <= 26]
    y = {N: pulp.LpVariable(f"y_{N}", cat="Binary") for N in Ns}
    prob += pulp.lpSum(y.values()) <= 1
    for key, v in x.items():
        k, r, m, n, s = key
        if m == "FCL":
            prob += v <= y.get(n, 0)
    for N in Ns:
        fcl = [(key, v) for key, v in x.items() if key[2] == "FCL" and key[3] == N]
        sh = lambda key: 0.3 if key[4] == "b" else key[4]
        prob += pulp.lpSum(v * PARTS[key[0]]["D"] * sh(key) * PARTS[key[0]]["m3"] for key, v in fcl) <= FEU_M3 * N
        prob += pulp.lpSum(v * PARTS[key[0]]["D"] * sh(key) * PARTS[key[0]]["kg"] for key, v in fcl) <= FEU_KG * N
    # region fixed costs
    regions = ["CN", "MX", "US", "CA"]
    u = {r: pulp.LpVariable(f"u_{r}", cat="Binary") for r in regions}
    for key, v in x.items():
        prob += v <= u[key[1]]
    if max_cn_share is not None:
        spend = lambda key: PARTS[key[0]]["D"] * (0.3 if key[4] == "b" else key[4]) * PARTS[key[0]]["p"][key[1]]
        tot_spend = pulp.lpSum(v * spend(key) for key, v in x.items())
        prob += pulp.lpSum(v * spend(key) for key, v in x.items() if key[1] == "CN") <= max_cn_share * tot_spend
    prob += (pulp.lpSum(cost[v] * v for v in x.values()) + pulp.lpSum(FIXED[r] * u[r] for r in regions)
             + pulp.lpSum(N * feu_cad * y[N] for N in Ns))
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    assert pulp.LpStatus[prob.status] == "Optimal", pulp.LpStatus[prob.status]
    return report(prob, x, meta, y, u, feu_cad, sc_name)


def report(prob, x, meta, y, u, feu_cad, sc_name):
    chosen = [meta[v] for v in x.values() if v.value() > 0.5]
    N = next((n for n, v in y.items() if v.value() > 0.5), 0)
    regions = [r for r, v in u.items() if v.value() > 0.5]
    fcl_vol = sum(PARTS[k]["D"] * s * PARTS[k]["m3"] for (k, r, m, n, s, c) in chosen if m == "FCL")
    lines = []
    tot = dict(purchase=0, duty=0, freight=N * feu_cad, broker=0, quality=0, carry=0, terms=0)
    for (k, r, m, n, s, c) in chosen:
        for i in ("purchase", "duty", "freight", "broker", "quality", "carry", "terms"):
            tot[i] += c[i]
        lines.append(dict(part=k, region=r, mode=m, orders=n, share=s, **{i: round(c[i]) for i in ("purchase", "duty", "freight", "broker", "quality", "carry", "terms")},
                          ss=round(c["ss"]), pipeline=round(c["pipeline"]), cycle=round(c["cycle"])))
    tot["fixed"] = sum(FIXED[r] for r in regions)
    tot["total"] = sum(tot.values())
    return dict(scenario=sc_name, containers=N, regions=regions, lines=lines, totals={k: round(v) for k, v in tot.items()},
                fcl_m3=round(fcl_vol, 1))


def evaluate_fixed(plan_lines, sc_name="base", feu_usd=FEU_USD, containers=None):
    """Annual total landed cost of a given plan (list of (part, region, mode, n, share)) under a scenario."""
    sc = SCENARIOS[sc_name]; feu_cad = feu_usd * FX + FEU_LOCAL
    tot = dict(purchase=0, duty=0, freight=0, broker=0, quality=0, carry=0, terms=0)
    regions = set(); fcl = []
    for (k, r, m, n, s) in plan_lines:
        c = stream_cost(k, r, m, n, s, sc)
        for i in tot:
            tot[i] += c[i]
        regions.add(r)
        if m == "FCL":
            fcl.append((k, s, n))
    if fcl:
        N = fcl[0][2]
        tot["freight"] += N * feu_cad
    tot["fixed"] = sum(FIXED[r] for r in regions)
    tot["total"] = sum(tot.values())
    return {k: round(v) for k, v in tot.items()}


def price_only_plan(sc_name="base"):
    """Buyer's rule: lowest unit price, shipped LCL (China) or truck, ordered monthly-ish: n=12 (or largest feasible <= 12)."""
    sc = SCENARIOS[sc_name]; plan = []
    for k, P in PARTS.items():
        r = min(P["p"], key=P["p"].get)
        m = "LCL" if r == "CN" else "TRK"
        n = max(f for f in FREQS if f <= 12 and (r != "CN" or P["D"] / f >= P["moq"]))
        plan.append((k, r, m, n, 1.0))
    return plan


def landed_price_plan(sc_name="base"):
    """Buyer's rule 2: lowest landed price per unit (price + duty + freight + brokerage), ignoring inventory, quality, overheads.
    Each region evaluated at its cheapest shipping option per unit."""
    sc = SCENARIOS[sc_name]; plan = []
    for k, P in PARTS.items():
        best = None
        for (r, m, n) in options(k, sc):
            if m == "FCL" or n != max(f for f in FREQS if f <= 4 and (r != "CN" or P["D"] / f >= P["moq"])):
                continue
            c = stream_cost(k, r, m, n, 1.0, sc)
            per_unit = (c["purchase"] + c["duty"] + c["freight"] + c["broker"]) / P["D"]
            if best is None or per_unit < best[0]:
                best = (per_unit, (k, r, m, n, 1.0))
        plan.append(best[1])
    return plan


if __name__ == "__main__":
    for sc in SCENARIOS:
        res = solve(sc)
        print(sc, res["totals"], res["containers"], res["regions"], res["fcl_m3"])
        for l in res["lines"]:
            print("   ", l["part"], l["region"], l["mode"], l["orders"], l["share"])
    for nm, f in (("price-only", price_only_plan), ("landed-price", landed_price_plan)):
        pl = f("base"); print(nm, [(a, b, c, d) for a, b, c, d, e in pl]); print("   ", evaluate_fixed(pl, "base"))
