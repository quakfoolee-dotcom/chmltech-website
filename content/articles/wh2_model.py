"""Warehouse operations series, Part 2: pick methods and pick paths in the Part 1 warehouse (V5.32).

Uses the pallet-rack zone and the two layouts of wh_model.py: as-is (state 0) and after the four fixes (state 4).
Every case pick comes from a SKU's open pallet, so its location is that pallet's position in the layout.

Methods
  single   single-order picking: one picker, one order per trip
  batch    batch picking: one trip picks BATCH orders onto a cart of totes, each line put to its order's tote
  zone     zone picking: one picker per aisle picks that aisle's lines for BATCH orders; totes meet at packing
  wave     wave picking: orders released in WAVES timed to the carrier pickups; each zone picker sweeps the aisle
           once per wave (in trips of at most CART lines), so trips get denser as volume rises
Routes (single and batch; a zone picker works one aisle and always walks to the farthest pick and back)
  return   into each aisle with picks as far as the farthest pick, and back out the same end
  sshape   right through each aisle with picks, snaking; an odd last aisle is a return trip
"""
import math, random
import wh_model as W

SEED = 11
ORDERS, LINES = 300, 3.0                 # orders a day, average rack-zone lines an order (900 case picks a day)
VOLUMES = list(range(150, 601, 25))       # orders a day for the volume slider
BATCH, WAVES, CART = 8, 3, 40
SPEED = 0.9                               # m/s walking with a cart
T_PICK, T_TOTE = 20.0, 4.0                # s per case pick; s to put a line in the right tote (batch, wave)
T_SETUP, T_ZSET = 60.0, 30.0              # s per trip: print or load the list, get the cart; zone trip
T_CONS = 15.0                             # s per order to bring totes from several zones together at packing
SHIFT_H = 7.0                             # productive picking hours per picker a day
FX = W.RACK_X0 - 0.8                      # front cross-aisle (x)
BX = W.RACK_X0 + W.BAYS * W.BAY_W + 0.8   # back cross-aisle (x)
DEPOT = (10.0, 41.0)                      # pack stations, where single and batch trips start and end
NA = len(W.AISLE_Z)

M = W.run()
LAYOUT = {0: M["locs"][0], 4: M["locs"][4]}
POS = {0: M["P0"], 4: M["P1"]}
ALIVE = {0: M["pallets"], 4: [p for p in M["pallets"] if p["id"] in M["locs"][4]]}


def pick_points(st):
    """(weight, aisle, x) of every picked pallet in layout st; pick weights after Part 1's merges."""
    pts = []
    for p in ALIVE[st]:
        w = p["pick"] if st == 0 else M["p2"][p["id"]]["pick"] if p["id"] in M["p2"] else 0
        if w <= 0: continue
        q = POS[st][LAYOUT[st][p["id"]]]
        x = W.RACK_X0 + q["b"] * W.BAY_W + (q["s"] + 0.5) * W.BAY_W / 2
        pts.append((w, W.ROW_AISLE[q["r"]], x, q["k"]))
    return pts


def sampler(st, rnd):
    pts = pick_points(st); cum = []; t = 0
    for w, a, x, k in pts: t += w; cum.append(t)
    import bisect
    def line(): return pts[bisect.bisect_left(cum, rnd.random() * t)][1:]
    return line


def make_orders(n, st, rnd):
    line = sampler(st, rnd); out = []
    for _ in range(n):
        k = 1 + min(7, int(rnd.expovariate(1 / (LINES - 1)) + 0.5))       # 1 to 8 lines, mean about 3
        out.append([line() for _ in range(k)])
    return out


def tour(lines, route):
    """Polyline of one single or batch trip from the pack stations through the picks and back, and its pick stops."""
    by = {}
    for a, x, k in lines: by.setdefault(a, []).append(x)
    aisles = sorted(by, key=lambda a: -W.AISLE_Z[a])             # nearest the pack stations first
    pts = [DEPOT, (FX, DEPOT[1])]; end = "F"
    for i, a in enumerate(aisles):
        z = W.AISLE_Z[a]; last = i == len(aisles) - 1
        pts.append((FX if end == "F" else BX, z))
        if route == "sshape" and not (last and end == "F"):
            pts.append((BX if end == "F" else FX, z)); end = "B" if end == "F" else "F"
        elif end == "F": pts += [(max(by[a]), z), (FX, z)]
        else: pts += [(min(by[a]), z), (BX, z)]
    if end == "B":                                               # back to the front round the end of the racks
        zt = W.ROW_Z[-1] + 1.6; pts += [(BX, zt), (FX, zt)]
    pts += [(FX, DEPOT[1]), DEPOT]
    return pts, [(x, W.AISLE_Z[a]) for a, x, k in lines]


def plen(pts): return sum(abs(pts[i + 1][0] - pts[i][0]) + abs(pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))


def zone_trip(xs):
    return 2 * (max(xs) - FX) if xs else 0.0


def metrics(method, st, route, vol, rnd, reps=1):
    """Metres walked and picker-seconds for vol orders a day; returns per-day totals."""
    orders = make_orders(vol, st, rnd)
    lines = sum(len(o) for o in orders)
    walk = 0.0; trips = 0; extra = 0.0
    if method == "single":
        for o in orders: walk += plen(tour(o, route)[0]); trips += 1
    elif method == "batch":
        for i in range(0, len(orders), BATCH):
            ls = [l for o in orders[i:i + BATCH] for l in o]; walk += plen(tour(ls, route)[0]); trips += 1
        extra += lines * T_TOTE
    elif method == "zone":
        for i in range(0, len(orders), BATCH):
            grp = orders[i:i + BATCH]
            for a in range(NA):
                xs = [x for o in grp for (aa, x, k) in o if aa == a]
                if xs: walk += zone_trip(xs); trips += 1
        extra += vol * T_CONS
    else:  # wave
        per = math.ceil(vol / WAVES)
        for i in range(0, len(orders), per):
            grp = orders[i:i + per]
            for a in range(NA):
                xs = [x for o in grp for (aa, x, k) in o if aa == a]
                for j in range(0, len(xs), CART):
                    walk += zone_trip(xs[j:j + CART]); trips += 1
        extra += vol * T_CONS + lines * T_TOTE
    setup = trips * (T_SETUP if method in ("single", "batch") else T_ZSET)
    t_walk = walk / SPEED; t_pick = lines * T_PICK
    total = t_walk + t_pick + setup + extra
    return dict(walk=walk, lines=lines, orders=vol, t_walk=t_walk, t_pick=t_pick, t_setup=setup, t_extra=extra, total=total,
                m_order=walk / vol, lph=lines / (total / 3600), pickers=total / 3600 / SHIFT_H, share_walk=t_walk / total)


METHODS = ["single", "batch", "zone", "wave"]
NAMES = {"single": "Single-order", "batch": "Batch", "zone": "Zone", "wave": "Wave"}


def grid():
    """Averaged over several order samples, for each layout, method, route and volume."""
    out = {}
    for st in (0, 4):
        for m in METHODS:
            for r in ("return", "sshape"):
                if m in ("zone", "wave") and r == "sshape": continue
                row = []
                for v in VOLUMES:
                    acc = None
                    for rep in range(6):
                        x = metrics(m, st, r, v, random.Random(SEED * 1000 + rep * 37 + v))
                        acc = x if acc is None else {k: acc[k] + x[k] for k in acc}
                    row.append({k: acc[k] / 6 for k in acc})
                out[(st, m, r)] = row
    return out


def best_route(G, st, m, v_ix):
    if m in ("zone", "wave"): return "return"
    return min(("return", "sshape"), key=lambda r: G[(st, m, r)][v_ix]["total"])


def example_trips(st, route, rnd):
    """Paths for the 3D figure: a few trips for each method at 300 orders a day."""
    orders = make_orders(48, st, rnd); ex = {}
    ex["single"] = [tour(o, route) for o in orders[:3]]
    ex["batch"] = [tour([l for o in orders[i:i + BATCH] for l in o], route) for i in (8, 16)]
    z = []
    grp = orders[24:24 + BATCH]
    for a in range(NA):
        xs = [x for o in grp for (aa, x, k) in o if aa == a]
        if xs: z.append(([(FX, W.AISLE_Z[a]), (max(xs), W.AISLE_Z[a]), (FX, W.AISLE_Z[a])], [(x, W.AISLE_Z[a]) for x in xs]))
    ex["zone"] = z
    wv = []; per = math.ceil(ORDERS / WAVES); grp = make_orders(per, st, rnd)
    for a in range(NA):
        xs = [x for o in grp for (aa, x, k) in o if aa == a][:CART]
        if xs: wv.append(([(FX, W.AISLE_Z[a]), (max(xs), W.AISLE_Z[a]), (FX, W.AISLE_Z[a])], [(x, W.AISLE_Z[a]) for x in xs]))
    ex["wave"] = wv
    return ex


if __name__ == "__main__":
    G = grid(); i300 = VOLUMES.index(300)
    for st in (0, 4):
        for m in METHODS:
            for r in ("return", "sshape"):
                if (st, m, r) not in G: continue
                g = G[(st, m, r)][i300]
                print(st, m, r, f"m/order {g['m_order']:.0f} lph {g['lph']:.0f} pickers {g['pickers']:.2f} walk% {g['share_walk']*100:.0f}")
