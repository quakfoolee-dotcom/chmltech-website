"""Warehouse operations series, Part 7: when does an SME need a warehouse management system? (V5.37)

The Parts 1 to 6 distributor, at any volume from 50 to 1,200 orders a day (about 3 lines an order, 250 days a year),
run four ways:
  sheet   paper pick lists and a spreadsheet (or the accounting package's stock list), no barcodes
  erp     the ERP's inventory module with bin locations and handheld barcode scanning
  cloud   a cloud WMS: directed put-away, batch and wave picking, scan at pick and pack, cycle counts, labour reports
  tier1   an enterprise (Tier 1) WMS, licensed and implemented by a systems integrator
Each option's yearly cost is software and hardware (implementation spread over five years, devices over four), floor
labour, office labour (keying, reconciling, answering "where is it?"), counting, errors that reach the customer
(Part 5's $75 each) and the cost of wrong stock records (searches, short shipments and rush orders).
Floor time an order grows with volume when people rely on memory and paper: more SKUs, more locations and more
people make "I know where it is" stop working. The rates are illustrative and stated below; the figure, the tables
and the 3D model all read them from here.
"""
import math

DAYS, LINES, WAGE = 250, 3.0, 40.0
PROD = 7.0                                     # productive hours a person a day (Part 6)
COST_ESC = 75.0                                # $ an error that reaches the customer (Part 5)
REC_HIT, REC_COST = 0.10, 30.0                 # share of wrong records that bite an order; $ each time (search, short ship, rush)
VOLS = [50, 75, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]
STEPS = [50, 150, 300, 500, 900]               # orders a day shown by the 3D figure's buttons; 300 is the example today
TODAY = 300
OPTS = ["sheet", "erp", "cloud", "tier1"]
ONAME = {"sheet": "Paper and spreadsheet", "erp": "ERP module + scanners", "cloud": "Cloud WMS", "tier1": "Enterprise WMS"}

O = {  # floor h an order at low volume, growth with volume (per 1,000 orders a day), office min an order,
       # errors reaching customers an order, location accuracy, count labour, software
    "sheet": dict(h=0.150, grow=0.50, office=1.0, err=0.0075, acc=0.92, count=("wall", 2), base=0, user=0, impl=0, dev=0, it=1200,
                  lag="end of shift", lag_h=8.0),
    "erp":   dict(h=0.154, grow=0.12, office=0.6, err=0.0025, acc=0.97, count=("wall", 1), base=600, user=100, impl=25000, dev=1600, it=0,
                  lag="a few minutes", lag_h=0.1),
    "cloud": dict(h=0.150, grow=0.03, office=0.30, err=0.0012, acc=0.990, count=("cycle", 0.15), base=2000, user=150, impl=45000, dev=1800, it=0,
                  lag="seconds", lag_h=0.0),
    "tier1": dict(h=0.146, grow=0.02, office=0.30, err=0.0010, acc=0.995, count=("cycle", 0.15), base=6000, user=250, impl=320000, dev=2500, it=55000,
                  lag="seconds", lag_h=0.0),
}
IMPL_YEARS, DEV_YEARS, OFFICE_USERS = 5, 4, 2
LIVE = {"sheet": 0, "erp": 2, "cloud": 3, "tier1": 9}      # months from signing to go-live
DIP = {"sheet": 0, "erp": 4, "cloud": 6, "tier1": 10}      # weeks after go-live at 80% of normal floor pace
DIP_LOSS = 0.20


def run(opt, v):
    """Yearly cost of one option at v orders a day."""
    o = O[opt]; orders = v * DAYS
    h = o["h"] * (1 + o["grow"] * v / 1000)                     # floor hours an order
    floor_n = math.ceil(v * h / PROD)                            # floor people
    office_h = orders * o["office"] / 60
    if o["count"][0] == "wall": count_h = o["count"][1] * 8 * (floor_n + OFFICE_USERS)
    else: count_h = orders * o["count"][1] / 60
    users = floor_n + OFFICE_USERS
    sw = 12 * (o["base"] + o["user"] * users) + o["impl"] / IMPL_YEARS + floor_n * o["dev"] / DEV_YEARS + o["it"]
    cost = dict(software=sw, floor=orders * h * WAGE, office=office_h * WAGE, count=count_h * WAGE,
                errors=orders * o["err"] * COST_ESC, records=orders * LINES * (1 - o["acc"]) * REC_HIT * REC_COST)
    tot = sum(cost.values())
    first_year = o["impl"] + floor_n * o["dev"] + 12 * (o["base"] + o["user"] * users)
    return dict(opt=opt, v=v, h=h, floor_n=floor_n, users=users, cost=cost, total=tot, per_order=tot / orders, first_year=first_year,
                err_pct=o["err"] * 100, acc=o["acc"], lag=o["lag"])


def table():
    return {opt: [run(opt, v) for v in VOLS] for opt in OPTS}


def cheapest(v): return min(OPTS, key=lambda o: run(o, v)["total"])


def crossover(a, b, lo=40, hi=3000):
    """Lowest volume at which option b becomes cheaper than option a, or None."""
    for v in range(lo, hi + 1, 5):
        if run(b, v)["total"] < run(a, v)["total"]: return v
    return None


def one_time(opt, v=TODAY):
    """Implementation, devices and the go-live productivity dip."""
    r = run(opt, v)
    return O[opt]["impl"] + r["floor_n"] * O[opt]["dev"] + DIP[opt] / 52 * r["cost"]["floor"] * DIP_LOSS


def payback(opt, base="sheet", v=TODAY):
    """Months from signing until the yearly saving against base has repaid the one-time cost (none if no saving)."""
    r, b = run(opt, v), run(base, v)
    yearly = lambda x, o: x["total"] - O[o]["impl"] / IMPL_YEARS - x["floor_n"] * O[o]["dev"] / DEV_YEARS
    save = yearly(b, base) - yearly(r, opt)
    return None if save <= 0 else LIVE[opt] + 12 * one_time(opt, v) / save


if __name__ == "__main__":
    for v in (50, 100, 150, 200, 300, 500, 900, 1200, 2000):
        print(v, {o: round(run(o, v)["total"] / 1000) for o in OPTS}, cheapest(v))
    for a, b in (("sheet", "erp"), ("erp", "cloud"), ("cloud", "tier1"), ("sheet", "cloud")): print(a, b, crossover(a, b))
    for o in OPTS: r = run(o, TODAY); print(o, r["floor_n"], round(r["per_order"], 2), {k: round(x) for k, x in r["cost"].items()}, payback(o))
