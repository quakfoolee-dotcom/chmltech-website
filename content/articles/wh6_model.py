"""Warehouse operations series, Part 6: labour planning through the year (V5.36).

The Part 1-5 distributor averages 300 orders a day but its demand swings with the seasons: quiet in January, a spring
building season, and a holiday peak about 1.7 times the average in late November. The work each order brings comes from
the earlier parts (after their fixes): receiving and scanning, put-away, batch picking, scan-and-pack, and shipping.
Each zone has its own pattern through the shift, so even a crew big enough for the day can be short in one zone and
idle in another at the same hour.

Plans
  ot      a lean core crew sized for the average day; peaks are met with overtime, and what overtime cannot cover ships late
  peak    a crew big enough for the holiday peak, all year
  temps   the lean core crew plus agency temps hired two weeks before they are needed, with a learning curve
  flex    temps as above, plus a cross-trained core that moves to the busiest zone each hour
The day is 06:00 to 14:30: eight paid hours, seven of them productive. Overtime is paid at 1.5 times (BC: after 8 hours
a day) and is less productive the longer it runs.
"""
import math

DAYS_WEEK, WEEKS = 5, 52
AVG_ORDERS = 300
ZONES = ["receive", "putaway", "pick", "pack", "ship"]
ZNAME = {"receive": "Receiving", "putaway": "Put-away", "pick": "Picking", "pack": "Packing", "ship": "Shipping"}
H_ORDER = {"receive": 0.61 * 3.3 / 60,           # 0.61 inbound pallets an order, unloaded and scanned (Part 3)
           "putaway": 0.61 * 0.75 * 4.0 / 60,    # three in four pallets put away, the rest cross-docked (Part 3)
           "pick": 9.1 / 300,                     # batch picking in the re-slotted racks (Part 2)
           "pack": 2.5 / 60,                      # scan every case and pack (Part 5)
           "ship": 1.0 / 60}                      # stage, load and paperwork
PROFILE = {                                       # share of each zone's daily work in each hour from 06:00
    "receive": [0.18, 0.20, 0.20, 0.16, 0.12, 0.08, 0.04, 0.02],
    "putaway": [0.04, 0.10, 0.15, 0.17, 0.17, 0.15, 0.12, 0.10],
    "pick":    [0.10, 0.16, 0.16, 0.14, 0.14, 0.12, 0.10, 0.08],
    "pack":    [0.04, 0.08, 0.13, 0.15, 0.16, 0.16, 0.15, 0.13],
    "ship":    [0.02, 0.03, 0.05, 0.08, 0.12, 0.18, 0.26, 0.26],
}
HOURS = 8
PROD = 7.0 / 8                                   # productive share of each paid hour
WAGE, OT_X, TEMP_RATE = 40.0, 1.5, 36.0          # $ an hour loaded; overtime premium; agency bill rate an hour
OT_CAP = 2.0                                     # overtime hours a person a day (a 10-hour day)
OT_PROD = 0.8                                    # productive share of an overtime hour (fatigue)
TRAIN_H, SUP_H = 8.0, 2.0                        # paid training hours a temp; supervisor hours a temp
RAMP = [0.6, 0.85]                               # temp productivity in their first and second week, then full
LEAD = 2                                         # weeks before the need that temps start
LATE_COST = 15.0                                 # $ an order shipped a day late (expediting, service, some lost sales)
FLEX_SHARE = 0.6                                 # share of the core crew cross-trained to move between zones


def season():
    """Demand multiplier for each week, normalized to an average of 1."""
    m = []
    for w in range(1, WEEKS + 1):
        if w <= 6: x = 0.75
        elif w <= 12: x = 0.9
        elif w <= 22: x = 1.15
        elif w <= 34: x = 0.95
        elif w <= 43: x = 1.05
        elif w <= 50: x = [1.25, 1.4, 1.55, 1.7, 1.7, 1.5, 1.3][w - 44]
        else: x = 0.8
        m.append(x)
    avg = sum(m) / len(m)
    return [x / avg for x in m]


SEASON = season()
ORDERS = [AVG_ORDERS * s for s in SEASON]
H_PER_ORDER = sum(H_ORDER.values())


def load(orders):
    """Productive hours of work for one day, by zone and hour."""
    return {z: [orders * H_ORDER[z] * f for f in PROFILE[z]] for z in ZONES}


def split(n, weights):
    """Split n people across zones in proportion to weights (largest remainder, at least one each when n >= zones)."""
    tot = sum(weights.values()); raw = {z: n * weights[z] / tot for z in ZONES}
    out = {z: int(raw[z]) for z in ZONES}
    if n >= len(ZONES):
        for z in ZONES:
            if out[z] == 0: out[z] = 1
    while sum(out.values()) < n:
        z = max(ZONES, key=lambda z: raw[z] - out[z]); out[z] += 1
    while sum(out.values()) > n:
        z = max(ZONES, key=lambda z: out[z] - raw[z]); out[z] -= 1
    return out


AVG_DAY = sum(sum(v) for v in load(AVG_ORDERS).values())
PEAK_DAY = sum(sum(v) for v in load(max(ORDERS)).values())
CORE = math.ceil(AVG_DAY / (HOURS * PROD))
PEAK_CREW = math.ceil(PEAK_DAY / (HOURS * PROD))
ZONE_W = {z: H_ORDER[z] for z in ZONES}


def _place(n, deficit):
    """Place n temps (fewer than the zones) on the zones with the largest deficits."""
    out = dict.fromkeys(ZONES, 0); d = dict(deficit)
    for _ in range(n):
        z = max(ZONES, key=lambda z: d[z]); out[z] += 1; d[z] -= 1
    return out


def day(orders, staff, flex):
    """One day: staff is {zone: effective people}; flex moves FLEX_SHARE of them to wherever the load is each hour.
    Returns per-hour per-zone load and capacity, unmet work, idle capacity."""
    L = load(orders); unmet = 0.0; idle = 0.0; cap_zh = {z: [0.0] * HOURS for z in ZONES}
    for h in range(HOURS):
        if flex:
            fixed = {z: staff[z] * (1 - FLEX_SHARE) * PROD for z in ZONES}
            pool = sum(staff.values()) * FLEX_SHARE * PROD
            need = {z: max(0.0, L[z][h] - fixed[z]) for z in ZONES}; tn = sum(need.values())
            for z in ZONES:
                cap_zh[z][h] = fixed[z] + (pool * need[z] / tn if tn > 0 else pool / len(ZONES))
        else:
            for z in ZONES: cap_zh[z][h] = staff[z] * PROD
        for z in ZONES:
            unmet += max(0.0, L[z][h] - cap_zh[z][h]); idle += max(0.0, cap_zh[z][h] - L[z][h])
    return L, cap_zh, unmet, idle


def plan(name):
    flex = name == "flex"
    core_n = PEAK_CREW if name == "peak" else CORE
    core = split(core_n, ZONE_W)
    # temps: people needed beyond the core in each week, by zone (pooled when the crew is flexible)
    temps_need = [dict.fromkeys(ZONES, 0) for _ in range(WEEKS)]
    if name in ("temps", "flex"):
        for w in range(WEEKS):
            L = load(ORDERS[w]); day_need = {z: sum(L[z]) / (HOURS * PROD) for z in ZONES}   # people-days of work by zone
            if not flex:                       # temps sized zone by zone to the day's work; peak hours fall to overtime
                for z in ZONES: temps_need[w][z] = max(0, math.ceil(day_need[z] - core[z] - 0.25))
            else:                              # a flexible crew pools the work: size temps to the total, place them where the gap is
                gap = sum(day_need.values()) - sum(core.values())
                n = max(0, math.ceil(gap - 0.25))
                deficit = {z: max(0.0, day_need[z] - core[z]) for z in ZONES}
                if n and sum(deficit.values()) > 0:
                    temps_need[w] = split(n, {z: deficit[z] + 1e-6 for z in ZONES}) if n >= len(ZONES) else _place(n, deficit)
    # each temp position runs from LEAD weeks before its first week of need to its last week of need
    weeks = []
    tot = dict(core_h=0.0, ot_h=0.0, temp_h=0.0, train=0.0, late=0.0, idle=0.0, burn=0, max_ot_pp=0.0, temps_hired=0)
    for z in ZONES:
        mx = max(t[z] for t in temps_need)
        for k in range(1, mx + 1):
            need_w = [w for w in range(WEEKS) if temps_need[w][z] >= k]
            if need_w: tot["temps_hired"] += 1
    for w in range(WEEKS):
        staff = {}; temp_n = {}
        for z in ZONES:
            eff = float(core[z]); n_t = 0
            mx = max(t[z] for t in temps_need)
            for k in range(1, mx + 1):
                need_w = [x for x in range(WEEKS) if temps_need[x][z] >= k]
                if not need_w: continue
                start, end = need_w[0] - LEAD, need_w[-1]
                if start <= w <= end:
                    age = w - start; n_t += 1
                    eff += RAMP[age] if age < len(RAMP) else 1.0
            staff[z] = eff; temp_n[z] = n_t
        L, cap, unmet, idle = day(ORDERS[w], staff, flex)
        people = sum(core.values()) + sum(temp_n.values())
        ot_cap = OT_CAP * people * OT_PROD
        ot_prod = min(unmet, ot_cap); ot_paid = ot_prod / OT_PROD; late_h = unmet - ot_prod
        late_orders = late_h / H_PER_ORDER
        ot_pp_week = ot_paid / people * DAYS_WEEK
        tot["core_h"] += sum(core.values()) * HOURS * DAYS_WEEK
        tot["temp_h"] += sum(temp_n.values()) * HOURS * DAYS_WEEK
        tot["ot_h"] += ot_paid * DAYS_WEEK; tot["late"] += late_orders * DAYS_WEEK; tot["idle"] += idle * DAYS_WEEK
        tot["burn"] += 1 if ot_pp_week > 8 else 0; tot["max_ot_pp"] = max(tot["max_ot_pp"], ot_pp_week)
        weeks.append(dict(orders=ORDERS[w], core=dict(core), temps=temp_n, eff=staff, load=L, cap=cap, unmet=unmet, ot=ot_paid,
                          late=late_orders * DAYS_WEEK, idle=idle, people=people, ot_pp=ot_pp_week,
                          cap_day=sum(staff.values()) * HOURS * PROD, need_day=sum(sum(v) for v in L.values())))
    tot["train"] = tot["temps_hired"] * (TRAIN_H * TEMP_RATE + SUP_H * WAGE)
    cost = dict(core=tot["core_h"] * WAGE, ot=tot["ot_h"] * WAGE * OT_X, temps=tot["temp_h"] * TEMP_RATE + tot["train"], late=tot["late"] * LATE_COST)
    cost["total"] = sum(cost.values())
    orders_year = sum(ORDERS) * DAYS_WEEK
    tot["idle_share"] = tot["idle"] / (tot["core_h"] * PROD + tot["temp_h"] * PROD)
    return dict(name=name, core=core, core_n=core_n, weeks=weeks, tot=tot, cost=cost, per_order=cost["total"] / orders_year, flex=flex)


PLANS = ["ot", "peak", "temps", "flex"]
PNAME = {"ot": "Lean crew + overtime", "peak": "Crew sized for the peak", "temps": "Core crew + planned temps", "flex": "Temps + cross-trained crew"}


if __name__ == "__main__":
    print("orders peak", round(max(ORDERS)), "low", round(min(ORDERS)), "h/order", round(H_PER_ORDER, 4), "avg day h", round(AVG_DAY, 1), "core", CORE, "peak crew", PEAK_CREW, split(CORE, ZONE_W))
    for p in PLANS:
        r = plan(p); t = r["tot"]; c = r["cost"]
        print(p, f"total ${c['total']:,.0f} core ${c['core']:,.0f} ot ${c['ot']:,.0f} temps ${c['temps']:,.0f} late ${c['late']:,.0f} | ot h {t['ot_h']:.0f} late {t['late']:.0f} "
              f"idle {t['idle_share']*100:.0f}% burn wks {t['burn']} max ot/pp/wk {t['max_ot_pp']:.1f} temps hired {t['temps_hired']} $/order {r['per_order']:.2f}")
