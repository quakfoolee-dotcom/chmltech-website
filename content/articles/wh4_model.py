"""Warehouse operations series, Part 4: inventory record accuracy in the Part 1 warehouse over one year (V5.34).

Every occupied rack location of the Part 1 layout (after the four fixes) has a system record: a SKU, a quantity and a
location. Each week a location's record can go wrong through receiving miscounts, mis-picks, put-away to the wrong
location or unrecorded damage. Busy locations go wrong more often, so the weekly chance depends on the SKU's class.
A wrong record is either a quantity variance (the shelf holds a different quantity) or phantom stock (the system
shows stock that is not there). Phantom stock on a busy location is usually found when a picker goes for it: that
pick is short, the order line is late, and the record is corrected.

Strategies
  annual   one wall-to-wall count at the end of the year, with the warehouse closed for two days
  cycle    ABC cycle counting: A locations every 4 weeks, B every 13, C every 26; no annual count
  fixed    cycle counting plus the causes fixed: scan to receive and put away (Part 3) and scan at pick (Part 5);
           with fewer errors, B and C locations are counted half as often
"""
import random
import wh_model as W

SEED = 41
WEEKS = 52
HAZ = {"A": 0.022, "B": 0.009, "C": 0.004}           # weekly chance a location's record goes wrong, as-is
FIX_FACTOR = 0.3                                      # with the causes fixed
PHANTOM = 0.35                                        # share of errors that leave the system showing stock that is not there
FIND = {"A": 0.45, "B": 0.18, "C": 0.05}              # weekly chance a phantom is found by a picker (a short pick)
PERIOD = {"A": 4, "B": 13, "C": 26}                   # weeks between cycle counts
PERIOD_F = {"A": 4, "B": 26, "C": 52}                 # once the causes are fixed, B and C are counted half as often
COUNT_FIX = 0.97                                      # a count corrects an error it meets (blind count, recount on variance)
ANNUAL_FIX = 0.95                                     # the year-end wall-to-wall count, done fast with temporary help
T_COUNT, T_ANNUAL = 3.0, 4.0                          # minutes a location: a cycle count; the annual count, with set-up and recounts
START_ACC = 0.95                                      # records right at the start of the year, after last year's count
SHORT_COST = 45.0                                     # $ a short pick: expediting, a split shipment or a lost line (assumed)
T_SEARCH = 15.0                                       # minutes to search for missing stock and correct the record after a short pick
STRATS = ["annual", "cycle", "fixed"]
NAMES = {"annual": "Annual count only", "cycle": "ABC cycle counting", "fixed": "Cycle counting + causes fixed"}


def locations():
    """(class, rack position index, height) of every pallet in the Part 1 layout after the fixes."""
    M = W.run(); out = []
    for p in M["pallets"]:
        if p["id"] not in M["locs"][4]: continue
        h = M["p2"][p["id"]]["h"] if p["id"] in M["p2"] else p["h"]
        out.append((p["cls"], M["locs"][4][p["id"]], h))
    return out


LOCS = locations()
N = len(LOCS)


def offset(i, cls, per): return (i * 7919) % per[cls]


def run(strat, seed=SEED, events=False):
    """One simulated year. Status per location: 0 right, 1 quantity variance, 2 phantom.
    Returns weekly accuracy, totals, and (optionally) the status changes for the 3D figure."""
    rnd = random.Random(seed)
    st = [0 if rnd.random() < START_ACC else (2 if rnd.random() < PHANTOM else 1) for _ in range(N)]
    ev = [[(0, s)] if s else [] for s in st]
    acc = [sum(1 for s in st if s == 0) / N]; short = 0; counts = 0; hours = 0.0; found_by_count = 0
    k = FIX_FACTOR if strat == "fixed" else 1.0; per = PERIOD_F if strat == "fixed" else PERIOD
    for w in range(1, WEEKS + 1):
        for i, (c, ix, h) in enumerate(LOCS):
            s0 = st[i]
            if st[i] == 0 and rnd.random() < HAZ[c] * k:
                st[i] = 2 if rnd.random() < PHANTOM else 1
            elif st[i] == 2 and rnd.random() < FIND[c]:
                st[i] = 0; short += 1                    # found the hard way: a short pick, then corrected
            elif st[i] == 1 and rnd.random() < 0.15 * HAZ[c] * k:
                st[i] = 2                                # a variance that runs out becomes phantom
            if strat in ("cycle", "fixed") and w % per[c] == offset(i, c, per):
                counts += 1; hours += T_COUNT / 60
                if st[i] and rnd.random() < COUNT_FIX: st[i] = 0; found_by_count += 1
            if events and st[i] != s0: ev[i].append((w, st[i]))
        if strat == "annual" and w == WEEKS:
            for i in range(N):
                s0 = st[i]; counts += 1; hours += T_ANNUAL / 60
                if st[i] and rnd.random() < ANNUAL_FIX: st[i] = 0; found_by_count += 1
                if events and st[i] != s0: ev[i].append((w, st[i]))
        acc.append(sum(1 for s in st if s == 0) / N)
    search = short * T_SEARCH / 60
    return dict(acc=acc, avg=sum(acc[1:WEEKS]) / (WEEKS - 1), low=min(acc), end=acc[-1], short=short, short_cost=short * SHORT_COST,
                counts=counts, hours=hours, search=search, total_h=hours + search, closed=2 if strat == "annual" else 0, found=found_by_count, ev=ev if events else None)


def averaged(strat, n=20):
    keys = ["avg", "low", "end", "short", "short_cost", "counts", "hours", "search", "total_h", "closed", "found"]
    acc = {k: 0.0 for k in keys}; curve = [0.0] * (WEEKS + 1)
    for r in range(n):
        x = run(strat, SEED + r * 101)
        for k in keys: acc[k] += x[k] / n
        for w in range(WEEKS + 1): curve[w] += x["acc"][w] / n
    acc["curve"] = curve
    return acc


def class_counts():
    out = {}
    for c, ix, h in LOCS: out[c] = out.get(c, 0) + 1
    return out


if __name__ == "__main__":
    print(N, class_counts())
    for s in STRATS:
        a = averaged(s)
        print(s, f"avg {a['avg']*100:.1f} low {a['low']*100:.1f} end {a['end']*100:.1f} short {a['short']:.0f} ${a['short_cost']:.0f} counts {a['counts']:.0f} hours {a['hours']:.0f} search {a['search']:.0f} total {a['total_h']:.0f} closed {a['closed']}")
