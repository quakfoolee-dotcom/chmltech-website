"""Warehouse operations series, Part 5: mis-picks, mis-ships and what each error costs (V5.35).

The Part 2 distributor ships 300 orders a day of about 3 lines from the rack zone, 250 days a year. Each line can be
picked wrong in three ways: the wrong item, the wrong quantity, or the right item put in the wrong order's tote (batch
picking, Part 2). Checkpoints between picking and the truck catch a share of each kind. Whatever gets past them
reaches the customer.

Steps, cumulative (each keeps the ones before it unless it replaces them):
  0 As-is           paper pick list, no check before shipping
  1 Pack check      the packer compares the cases with the packing slip
  2 Scan at pick    a handheld confirms the location and item at each pick, and the tote at each put
  3 Scan at pack    the packer scans every case against the order (replaces the visual check)
  4 Weigh at ship   the packed parcel is weighed against its expected weight
The cost of an error rises with how late it is found, roughly 1-10-100: a few cents at the pick face, a few dollars at
packing, and $75 once it reaches the customer (returns, reshipping, handling, credits and some lost customers).
"""
ORDERS_DAY, LINES_ORDER, DAYS = 300, 3.0, 250
ORDERS = ORDERS_DAY * DAYS
LINES = ORDERS * LINES_ORDER
WAGE = 40.0                                           # $ an hour, loaded
P_ERR = {"item": 0.0027, "qty": 0.0024, "tote": 0.0009}   # errors made per line, paper pick list (0.6% of lines)
SCAN_PICK = {"item": 0.05, "qty": 0.6, "tote": 0.1}       # share of errors still made with scan at pick
CATCH = {                                                 # share of the remaining errors each checkpoint catches
    "visual": {"item": 0.60, "qty": 0.50, "tote": 0.60},
    "scan": {"item": 0.99, "qty": 0.90, "tote": 0.99},
    "weigh": {"item": 0.40, "qty": 0.80, "tote": 0.40},
}
COST_PICK, COST_PACK = 0.50, 4.0                      # $ an error caught at the pick face (scan warns), at packing (re-pick)
COST_CUST = dict(return_freight=15.0, reship_freight=15.0, handling=20.0, service_credit=10.0, lost_customers=15.0)
COST_ESC = sum(COST_CUST.values())                    # $75 an error that reaches the customer
T_VISUAL, T_SCAN_PICK, T_SCAN_PACK, T_WEIGH = 20.0, 2.0, 4.0, 6.0   # s per order, per line, per line, per order
EQUIP = {2: (4 * 1800.0, 3000.0), 4: (2500.0, 0.0)}   # one-time $, yearly $ (handhelds and mobile licence; a check scale)
LIFE = 3                                               # years to spread equipment over
STEPS = ["As-is", "Pack check", "Scan at pick", "Scan at pack", "Weigh at ship"]


def step(n):
    made = {k: LINES * P_ERR[k] * (SCAN_PICK[k] if n >= 2 else 1.0) for k in P_ERR}
    caught_pick = {k: LINES * P_ERR[k] - made[k] if n >= 2 else 0.0 for k in P_ERR}   # stopped by the scanner at the pick face
    rem = dict(made); caught_pack = {k: 0.0 for k in P_ERR}; caught_weigh = {k: 0.0 for k in P_ERR}
    pack = "scan" if n >= 3 else "visual" if n >= 1 else None
    if pack:
        for k in rem: c = rem[k] * CATCH[pack][k]; caught_pack[k] = c; rem[k] -= c
    if n >= 4:
        for k in rem: c = rem[k] * CATCH["weigh"][k]; caught_weigh[k] = c; rem[k] -= c
    esc = sum(rem.values())
    labour_h = 0.0
    if n >= 1 and n < 3: labour_h += ORDERS * T_VISUAL / 3600
    if n >= 2: labour_h += LINES * T_SCAN_PICK / 3600
    if n >= 3: labour_h += LINES * T_SCAN_PACK / 3600
    if n >= 4: labour_h += ORDERS * T_WEIGH / 3600
    equip_year = sum(one / LIFE + yr for s, (one, yr) in EQUIP.items() if n >= s)
    cp = sum(caught_pick.values()); ck = sum(caught_pack.values()) + sum(caught_weigh.values())
    made_total = LINES * sum(P_ERR.values())
    cost_esc = esc * COST_ESC; cost_fix = cp * COST_PICK + ck * COST_PACK; cost_check = labour_h * WAGE + equip_year
    return dict(n=n, made=made_total, made_after_scan=sum(made.values()), caught_pick=cp, caught_pack=sum(caught_pack.values()),
                caught_weigh=sum(caught_weigh.values()), esc=esc, esc_by=rem,
                picked_right=1 - sum(made.values()) / ORDERS,       # orders picked right (one error spoils an order)
                shipped_right=1 - esc / ORDERS,
                cost_esc=cost_esc, cost_fix=cost_fix, labour_h=labour_h, equip_year=equip_year, cost_check=cost_check,
                total=cost_esc + cost_fix + cost_check)


def all_steps():
    out = [step(n) for n in range(5)]
    for s in out: s["saving"] = out[0]["total"] - s["total"]
    return out


def detection_probs(n):
    """For the 3D figure: per error kind, the chance it is made, then caught at pick, pack, weigh or escapes."""
    out = {}
    for k in P_ERR:
        p_made = P_ERR[k] * LINES_ORDER                      # per order
        stop_pick = (1 - SCAN_PICK[k]) if n >= 2 else 0.0
        pack = "scan" if n >= 3 else "visual" if n >= 1 else None
        c_pack = CATCH[pack][k] if pack else 0.0
        c_weigh = CATCH["weigh"][k] if n >= 4 else 0.0
        out[k] = [round(p_made, 5), stop_pick, c_pack, c_weigh]
    return out


if __name__ == "__main__":
    for s in all_steps():
        print(STEPS[s["n"]], f"made {s['made']:.0f} caught pick {s['caught_pick']:.0f} pack {s['caught_pack']:.0f} weigh {s['caught_weigh']:.0f} esc {s['esc']:.0f} "
              f"picked right {s['picked_right']*100:.2f} shipped right {s['shipped_right']*100:.2f} esc$ {s['cost_esc']:.0f} fix$ {s['cost_fix']:.0f} "
              f"check$ {s['cost_check']:.0f} ({s['labour_h']:.0f} h) total {s['total']:.0f} saving {s['saving']:.0f}")
