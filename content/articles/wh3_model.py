"""Warehouse operations series, Part 3: the receiving dock of the Part 1 warehouse, simulated for one day (V5.33).

Trucks arrive, wait for a door and one of the two dock staff, who unload each pallet and check it against the packing
slip into the staging lanes; and a forklift puts it away into a free rack position of the Part 1 layout. A
cross-dock pallet (already allocated to a customer order) skips put-away and goes to the outbound lanes. The forklift
is busy loading outbound trucks from 13:30 to 15:00.

Four fixes, each on or off (16 scenarios):
  appt   delivery appointments: carriers book slots spread over the day instead of arriving when they like
  scan   receive by scanning the supplier's labels against an advance ship notice (ASN) instead of a paper check
  xdock  cross-dock: 25% of inbound pallets are already allocated to orders and go straight to the outbound lanes
  fork   a second forklift (or the pick team's) puts away during the morning peak, 8:00 to 12:00
Times are minutes after 06:00.
"""
import random
import wh_model as W

SEED = 21
DAY0 = 6 * 60
FTL, LTL = 5, 9                          # full and part loads a day
T_UNLOAD = 2.5                           # min a pallet to unload with a pallet jack
T_CHECK, T_SCAN = 2.0, 0.8               # min a pallet: paper check against the packing slip, or scan against the ASN
T_PUT = 4.0                              # min a pallet: forklift trip to a rack position and back
T_XD = 1.0                               # min to move a cross-dock pallet to the outbound lanes
DOORS, UNLOADERS = 3, 2                  # inbound doors; dock staff unloading
STAGE_LANES, STAGE_DEPTH = 4, 12         # inbound staging: 48 pallet spots; the rest overflows into the aisles
XD_SHARE = 0.25
LOAD_BLOCK = (13.5 * 60 - DAY0, 15 * 60 - DAY0)   # forklift loading outbound trucks
SHIFT_END = 14.5 * 60 - DAY0             # dock shift ends at 14:30
FREE_MIN, DET_RATE = 120, 65.0           # detention after two hours on site, $ an hour (close to the industry average)
DAYS_YEAR = 250
FIXES = ["appt", "scan", "xdock", "fork"]


def trucks(appt, rnd):
    t = []
    for k in range(FTL + LTL):
        n = 24 if k < FTL else rnd.randint(4, 10)
        t.append(dict(id=k, pallets=n, ftl=k < FTL))
    rnd.shuffle(t)
    for i, tr in enumerate(t):
        if appt:
            slot = 30 + i * (360 / len(t))                       # 06:30 to 12:30, evenly, so receiving ends by mid-afternoon
            tr["arr"] = slot + rnd.uniform(-15, 20)
        else:
            tr["arr"] = min(7 * 60, max(30, rnd.gauss(150, 60)))   # bunched around 08:30
    return sorted(t, key=lambda x: x["arr"])


def simulate(appt=False, scan=False, xdock=False, fork=False, seed=SEED):
    rnd = random.Random(seed)
    T = trucks(appt, random.Random(seed + 1))
    door_free = [0.0] * DOORS; crew_free = [0.0] * UNLOADERS
    pallets = []
    for tr in T:
        d = min(range(DOORS), key=lambda i: door_free[i]); c = min(range(UNLOADERS), key=lambda i: crew_free[i])
        start = max(tr["arr"], door_free[d], crew_free[c])
        per = T_UNLOAD + (T_SCAN if scan else T_CHECK)            # the dock staff unload and check each pallet
        end = start + tr["pallets"] * per
        door_free[d] = end; crew_free[c] = end
        tr.update(door=d, start=start, end=end, wait=start - tr["arr"])
        for j in range(tr["pallets"]):
            xd = xdock and tr["ftl"] and rnd.random() < XD_SHARE * (FTL * 24 + LTL * 7) / (FTL * 24)
            pallets.append(dict(truck=tr["id"], door=d, enter=start + (j + 1) * per, xd=xd))
    for p in pallets: p["checked"] = p["enter"]                 # checked at the door as it comes off the truck
    # put-away: one forklift all day; a second one 08:00 to 12:00 when "fork" is on
    lifts = [dict(free=0.0, on=(0, 1e9))] + ([dict(free=0.0, on=(120, 360))] if fork else [])
    for p in sorted(pallets, key=lambda p: p["checked"]):
        if p["xd"]:
            p["out"] = p["checked"] + T_XD; p["put0"] = p["out"]; p["put1"] = p["out"]; continue
        best = None
        for L in lifts:
            s = max(p["checked"], L["free"], L["on"][0])
            if LOAD_BLOCK[0] <= s < LOAD_BLOCK[1] and L is lifts[0]: s = LOAD_BLOCK[1]
            if s + T_PUT > L["on"][1]: continue
            if best is None or s < best[0]: best = (s, L)
        s, L = best; L["free"] = s + T_PUT; p["put0"] = s; p["put1"] = s + T_PUT; p["out"] = s
    # staging occupancy: a pallet holds a spot from unloading until it leaves for the rack or the outbound lanes
    ev = sorted([(p["enter"], 1) for p in pallets] + [(p["out"], -1) for p in pallets])
    occ, peak, curve, over_min, lastt = 0, 0, [], 0.0, 0.0
    cap = STAGE_LANES * STAGE_DEPTH
    for t, d in ev:
        over_min += max(0, occ - cap) * (t - lastt); lastt = t
        occ += d; peak = max(peak, occ); curve.append((round(t, 1), occ))
    # spot assignment for the 3D figure: lowest free spot; spots past the lanes are overflow in the aisles
    taken = {}
    for p in sorted(pallets, key=lambda p: p["enter"]):
        for k in list(taken):
            if taken[k] <= p["enter"]: del taken[k]
        s = 0
        while s in taken: s += 1
        p["spot"] = s; taken[s] = p["out"]
    by = {}
    for p in pallets: by.setdefault(p["truck"], []).append(p)
    dts = []
    for tr in T:
        lst = by[tr["id"]]; tr["done"] = max(p["put1"] for p in lst)
        dts.append((tr["done"] - tr["arr"]) / 60)
    det = sum(max(0, (tr["end"] - tr["arr"]) - FREE_MIN) / 60 * DET_RATE for tr in T)
    last = max(p["put1"] for p in pallets)
    return dict(trucks=T, pallets=pallets, curve=curve, peak=peak, cap=cap, over_ph=over_min / 60,
                wait=sum(t["wait"] for t in T) / len(T), wait_max=max(t["wait"] for t in T),
                over2=sum(1 for t in T if t["end"] - t["arr"] > FREE_MIN), det=det, det_year=det * DAYS_YEAR,
                dts=sum(dts) / len(dts), dts_max=max(dts), last=last, ot=max(0, last - SHIFT_END) / 60,
                n_pal=len(pallets), n_xd=sum(1 for p in pallets if p["xd"]))


def averaged(flags, n=20):
    """The headline numbers averaged over n simulated days (the 3D figure replays day 0)."""
    keys = ["peak", "over_ph", "wait", "wait_max", "over2", "det", "det_year", "dts", "dts_max", "last", "ot", "n_xd", "n_pal"]
    acc = {k: 0.0 for k in keys}
    for d in range(n):
        r = simulate(**flags, seed=SEED + d * 97)
        for k in keys: acc[k] += r[k]
    return {k: v / n for k, v in acc.items()}


def combos():
    out = []
    for m in range(16):
        out.append({f: bool(m >> i & 1) for i, f in enumerate(FIXES)})
    return out


def hm(t):
    t = DAY0 + t; return f"{int(t // 60):02d}:{int(round(t % 60)) % 60:02d}"


if __name__ == "__main__":
    steps = [{}, dict(appt=True), dict(appt=True, scan=True), dict(appt=True, scan=True, xdock=True), dict(appt=True, scan=True, xdock=True, fork=True)]
    for f in steps:
        a = averaged(f)
        print(f, f"wait {a['wait']:.0f} max {a['wait_max']:.0f} >2h {a['over2']:.1f} det/yr {a['det_year']:.0f} dts {a['dts']:.1f}h peak {a['peak']:.0f} over {a['over_ph']:.0f}ph last {hm(a['last'])} ot {a['ot']:.1f} pal {a['n_pal']:.0f} xd {a['n_xd']:.0f}")
