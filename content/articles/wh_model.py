"""Warehouse operations series: the example distributor and its pallet-rack zone (V5.31).

One model feeds both the article text and the 3D figure (assets/js/wh3d.js), so every number quoted in Part 1 is
the model's result. The distributor is illustrative: a 40,000 sq ft building, 3,000 SKUs, of which 520 are stored on
pallets in a selective pallet-rack zone of 10 rows x 20 bays x 2 pallets per bay.

States (cumulative, the order used in Part 1 and in Figure 2):
  0 As-is                  4 beam levels, 2.0 m openings; partial pallets and dead stock in place; random putaway
  1 Re-set beam heights    5 levels: floor level kept 2.0 m high for tall loads, then 1.7 m beam pitch
  2 Combine partials       two partial pallets of the same SKU become one
  3 Clear dead stock       pallets with no picks in 12 months leave the racks (sold, returned or scrapped)
  4 Re-slot fast movers    pallets ranked by picks per day go to the closest, lowest positions
"""
import json, math, random

SEED = 7
# ───────────────────────── building and racks ─────────────────────────
BLD_X, BLD_Z, CLEAR_H = 72.0, 52.0, 9.1             # m; 72 x 52 m = 3,744 m2 = about 40,300 sq ft; 30 ft clear
SPRINK = 0.45                                       # m clearance below the sprinkler deflectors (18 in)
ROWS, BAYS, PER_BAY = 10, 20, 2
BAY_W, ROW_D, AISLE = 2.7, 1.1, 3.6                 # m; two 1.0 m wide pallets per 2.7 m bay; 3.6 m counterbalance aisles
RACK_X0 = 15.0                                      # m from the dock wall to the first bay (staging and cross-aisle)
PAL_L, PAL_W = 1.2, 1.0                             # m pallet footprint (deep x wide)
BEAM = 0.13                                         # m beam depth
LEVELS_ASIS = [0.0, 2.0, 4.0, 6.0]                  # top of floor / beam for each level, m
LEVELS_NEW = [0.0, 2.0, 3.7, 5.4, 7.1]
MAX_LOAD_TOP = CLEAR_H - SPRINK                     # 8.65 m: top of the highest load


def opening(levels, k):
    """Clear height of beam level k (the top level is limited by the sprinkler clearance)."""
    top = levels[k + 1] - BEAM if k + 1 < len(levels) else MAX_LOAD_TOP
    return top - levels[k]


# rows across the building (z): single row on the wall, four back-to-back pairs, single row; five aisles
def row_layout():
    z, rows, aisles = 2.0, [], []
    pattern = ["S", "A", "D", "D", "A", "D", "D", "A", "D", "D", "A", "D", "D", "A", "S"]
    for p in pattern:
        if p == "A": aisles.append(z + AISLE / 2); z += AISLE
        else: rows.append(z + ROW_D / 2); z += ROW_D
    return rows, aisles


ROW_Z, AISLE_Z = row_layout()
ROW_AISLE = [min(range(len(AISLE_Z)), key=lambda a: abs(AISLE_Z[a] - z)) for z in ROW_Z]
DOCK_Z = (ROW_Z[0] + ROW_Z[-1]) / 2                 # pick-up and drop-off point at the front cross-aisle
RACK_ZONE_M2 = (BAYS * BAY_W) * (ROW_Z[-1] - ROW_Z[0] + ROW_D)


def positions(levels):
    """Every pallet position: (row, bay, slot, level) with its walking distance and opening."""
    out = []
    for r in range(ROWS):
        for b in range(BAYS):
            for s in range(PER_BAY):
                for k in range(len(levels)):
                    x = RACK_X0 + b * BAY_W + (s + 0.5) * BAY_W / 2
                    walk = 2 * (abs(AISLE_Z[ROW_AISLE[r]] - DOCK_Z) + x)          # round trip from the front P&D point
                    out.append(dict(r=r, b=b, s=s, k=k, walk=walk, open=opening(levels, k)))
    return out


# ───────────────────────── SKUs and pallets ─────────────────────────
N_SKU, N_DEAD = 520, 62                             # pallet SKUs; SKUs with no picks in 12 months
PICKS_DAY = 900                                     # case picks a day from the rack zone


def build():
    rnd = random.Random(SEED)
    live = N_SKU - N_DEAD
    w = [1 / (i + 1) ** 1.05 for i in range(live)]
    tot = sum(w); picks = [PICKS_DAY * x / tot for x in w] + [0.0] * N_DEAD
    cum, cls = 0.0, []
    for p in picks:
        cum += p
        cls.append("D" if p == 0 else "A" if cum <= 0.8 * PICKS_DAY + 1e-9 else "B" if cum <= 0.95 * PICKS_DAY + 1e-9 else "C")
    pallets = []
    for i in range(N_SKU):
        c = cls[i]
        n = {"A": rnd.choice([3, 4, 5]), "B": rnd.choice([1, 2, 2, 3]), "C": rnd.choice([1, 1, 2]), "D": rnd.choice([1, 2, 2, 3])}[c]
        full_h = 1.75 if rnd.random() < 0.06 else round(rnd.uniform(1.05, 1.42), 2)
        for j in range(n):
            pallets.append(dict(sku=i, cls=c, full=full_h, h=full_h, part=False))
        if c != "A" and rnd.random() < 0.45:                     # a broken pallet or two left from picking
            for _ in range(rnd.choice([1, 2, 2])):
                pallets.append(dict(sku=i, cls=c, full=full_h, h=round(full_h * rnd.uniform(0.2, 0.55), 2), part=True))
        elif c == "A" and rnd.random() < 0.35:
            pallets.append(dict(sku=i, cls=c, full=full_h, h=round(full_h * rnd.uniform(0.25, 0.6), 2), part=True))
    for k, p in enumerate(pallets):
        p["id"] = k
        p["pick"] = picks[p["sku"]]
    # picks split over a SKU's pallets: only the open pallet is picked from, so weight the partial (open) one
    by = {}
    for p in pallets: by.setdefault(p["sku"], []).append(p)
    for lst in by.values():
        open_ = [p for p in lst if p["part"]] or lst[:1]
        for p in lst: p["pick"] = 0.0
        share = lst[0]["sku"] < len(picks) and picks[lst[0]["sku"]] / len(open_)
        for p in open_: p["pick"] = share
    return pallets, rnd


def assign_random(pallets, pos, rnd, keep=None):
    """Put-away to the nearest free slot of whoever arrived first: in practice close to random. Tall loads need the
    tallest openings. keep: {pallet id: position index} to leave in place."""
    free = set(range(len(pos))); loc = {}
    if keep:
        for pid, ix in keep.items(): loc[pid] = ix; free.discard(ix)
    order = [p for p in pallets if p["id"] not in loc]; rnd.shuffle(order)
    order.sort(key=lambda p: -p["h"])                             # tall first, so they find a tall opening
    for p in order:
        cand = sorted(i for i in free if pos[i]["open"] >= p["h"] + 0.1)
        ix = rnd.choice(cand); loc[p["id"]] = ix; free.discard(ix)
    return loc


def stats(pallets, pos, loc, levels):
    occ = len(loc); n = len(pos)
    inv = sum(PAL_L * PAL_W * p["h"] for p in pallets if p["id"] in loc)
    cap = sum(PAL_L * PAL_W * pos[i]["open"] for i in range(n))
    cap_occ = sum(PAL_L * PAL_W * pos[loc[p["id"]]]["open"] for p in pallets if p["id"] in loc)
    picks = sum(p["pick"] for p in pallets if p["id"] in loc)
    walk = sum(p["pick"] * pos[loc[p["id"]]]["walk"] for p in pallets if p["id"] in loc) / picks
    easy = sum(p["pick"] for p in pallets if p["id"] in loc and pos[loc[p["id"]]]["k"] <= 1 and pos[loc[p["id"]]]["b"] < 7) / picks
    return dict(positions=n, occupied=occ, free=n - occ, loc_util=occ / n, cube_util=inv / cap, cube_occ=inv / cap_occ,
                walk=walk, easy=easy, levels=len(levels))


def run():
    pallets, rnd = build()
    P0 = positions(LEVELS_ASIS); P1 = positions(LEVELS_NEW)
    states, pal_sets = [], []
    # 0 as-is
    loc0 = assign_random(pallets, P0, rnd)
    # 1 beams re-set: same row, bay, slot and level; the new top level is empty. A load too tall for its new opening
    #   moves to a free floor-level slot in the same row.
    loc1 = {}
    idx1 = {(q["r"], q["b"], q["s"], q["k"]): i for i, q in enumerate(P1)}
    used = set()
    for p in pallets:
        q = P0[loc0[p["id"]]]; i = idx1[(q["r"], q["b"], q["s"], q["k"])]
        loc1[p["id"]] = i; used.add(i)
    moved_tall = 0
    at = {i: pid for pid, i in loc1.items()}; hh = {p["id"]: p["h"] for p in pallets}
    for p in sorted(pallets, key=lambda p: -p["h"]):              # a load too tall for its new opening swaps with a
        i = loc1[p["id"]]                                         # short load on the floor level nearby
        if P1[i]["open"] < p["h"] + 0.1:
            cand = [j for j, q in enumerate(P1) if q["open"] >= p["h"] + 0.1 and (j not in at or hh[at[j]] + 0.1 <= P1[i]["open"])]
            cand.sort(key=lambda j: (j in at, P1[j]["r"] != P1[i]["r"], abs(P1[j]["b"] - P1[i]["b"])))
            j = cand[0]; other = at.get(j)
            if other is not None: loc1[other] = i; at[i] = other
            else: at.pop(i, None)
            loc1[p["id"]] = j; at[j] = p["id"]; moved_tall += 1 + (other is not None)
    # 2 combine partial pallets of the same SKU (pairs, while the sum fits one pallet)
    merged = {}
    by = {}
    for p in pallets:
        if p["part"]: by.setdefault(p["sku"], []).append(p)
    pal2 = {p["id"]: dict(p) for p in pallets}
    for sku, lst in by.items():
        lst = sorted(lst, key=lambda p: p["h"])
        while len(lst) >= 2:
            a, b = lst[0], lst[1]
            if a["h"] + b["h"] > a["full"] + 1e-9: break
            keep = pal2[b["id"]]; keep["h"] = round(a["h"] + b["h"], 2); keep["part"] = keep["h"] < keep["full"] - 0.05
            merged[a["id"]] = b["id"]; del pal2[a["id"]]
            lst = sorted([pal2[b["id"]]] + lst[2:], key=lambda p: p["h"])
            if not pal2[b["id"]]["part"]: lst = [x for x in lst if x["id"] != b["id"]]
    for pid, into in merged.items():
        if pal2[into]["pick"] or pallets[pid]["pick"]: pal2[into]["pick"] = pal2[into]["pick"] + pallets[pid]["pick"]
    p2 = list(pal2.values())
    loc2 = {p["id"]: loc1[p["id"]] for p in p2}
    # 3 clear dead stock
    dead = [p["id"] for p in p2 if p["cls"] == "D"]
    p3 = [p for p in p2 if p["cls"] != "D"]
    loc3 = {p["id"]: loc2[p["id"]] for p in p3}
    # 4 re-slot: the open (picked) pallets of A and B SKUs, busiest first, take the best positions (short walk, floor or
    #   first beam).
    def cost(i):
        q = P1[i]; return q["walk"] + (0 if q["k"] <= 1 else 30 + 12 * q["k"])
    order = sorted(range(len(P1)), key=cost)
    ranked = sorted([p for p in p3 if p["pick"] > 0 and p["cls"] in "AB"], key=lambda p: -p["pick"])
    loc4 = {}; rset = {p["id"] for p in ranked}
    best = []
    for p in ranked:                                              # choose the target slots
        for i in order:
            if i not in best and P1[i]["open"] >= p["h"] + 0.1:
                best.append(i); p["_t"] = i; break
    bset = set(best)
    for p in ranked: loc4[p["id"]] = p["_t"]
    # the rest (reserve pallets, and all C pallets) fill the remaining positions by class, nearest first, so each
    # class's reserve sits above and behind its pick faces: A, then B, then C
    rest = sorted([p for p in p3 if p["id"] not in rset], key=lambda p: ("ABC".index(p["cls"]), -p["pick"], p["sku"]))
    left = sorted([i for i in range(len(P1)) if i not in bset], key=lambda i: (P1[i]["walk"], P1[i]["k"]))
    used4 = set()
    for p in rest:
        for i in left:
            if i not in used4 and P1[i]["open"] >= p["h"] + 0.1:
                used4.add(i); loc4[p["id"]] = i; break
    moves4 = sum(1 for pid in loc4 if loc4[pid] != loc3[pid])
    sets = [(pallets, P0, loc0, LEVELS_ASIS), (pallets, P1, loc1, LEVELS_NEW), (p2, P1, loc2, LEVELS_NEW),
            (p3, P1, loc3, LEVELS_NEW), (p3, P1, loc4, LEVELS_NEW)]
    S = [stats(*s) for s in sets]
    info = dict(moved_tall=moved_tall, merged=len(merged), dead=len(dead), moves4=moves4,
                n_pal=len(pallets), partial=sum(1 for p in pallets if p["part"]),
                cls_count={c: sum(1 for i in range(N_SKU) if [p for p in pallets if p["sku"] == i][0]["cls"] == c) for c in "ABCD"},
                cls_pal={c: sum(1 for p in pallets if p["cls"] == c) for c in "ABCD"})
    return dict(pallets=pallets, p2={p["id"]: p for p in p2}, P0=P0, P1=P1, locs=[loc0, loc1, loc2, loc3, loc4],
                merged=merged, dead=dead, S=S, info=info)


def figure_data(m):
    """Compact JSON for wh3d.js. Per pallet: class, height per state, position index per state (-1 = gone),
    and for a merged pallet the id it joined."""
    out = []
    for p in m["pallets"]:
        pid = p["id"]; h = []; ix = []
        for st, loc in enumerate(m["locs"]):
            alive = pid in loc
            ix.append(loc[pid] if alive else -1)
            h.append(p["h"] if st < 2 else (m["p2"][pid]["h"] if pid in m["p2"] else p["h"]))
        out.append([p["cls"], h[0], h[2], ix, m["merged"].get(pid, -1)])
    return dict(
        bld=[BLD_X, BLD_Z, CLEAR_H], rows=ROW_Z, aisles=AISLE_Z, bays=BAYS, bayW=BAY_W, rowD=ROW_D, x0=RACK_X0, perBay=PER_BAY,
        pal=[PAL_L, PAL_W], beam=BEAM, levels=[LEVELS_ASIS, LEVELS_NEW], dock=DOCK_Z, maxTop=MAX_LOAD_TOP,
        stats=[{k: (round(v, 4) if isinstance(v, float) else v) for k, v in s.items()} for s in m["S"]],
        p=out)


if __name__ == "__main__":
    m = run()
    for i, s in enumerate(m["S"]): print(i, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in s.items()})
    print(m["info"]); print("rack zone m2", RACK_ZONE_M2, "rows", ROW_Z[-1])
    print(len(json.dumps(figure_data(m), separators=(",", ":"))))
