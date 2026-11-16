"""Warehouse operations series, Part 8: when does automation pay for an SME warehouse? (V5.38)

The Parts 1 to 7 distributor, now on a cloud WMS (Part 7, which every option below needs), at 150 to 900 orders a
day of about 3 lines, one shift, 250 days a year. Lines split between cases picked from the pallet racks and small
items ("eaches") picked from the shelving area at the back. Three automations, each aimed at one kind of work:
  ptl    pick-to-light on the fastest-moving shelving locations
  vlm    vertical lift modules replace the shelving: goods come to the picker, and the shelving floor is freed
  amr    collaborative mobile robots carry the totes in the rack aisles; pickers stay in their zone
Payback = one-time cost / (yearly labour, error and space saving - yearly running cost). Prices sit inside published
ranges; the labour times come from Parts 2 and 6.
"""
import math

DAYS, LINES, HOURS = 250, 3.0, 8.0
WAGE = 40.0                                     # $ an hour, loaded (Parts 5 and 6)
CASE_SHARE = 0.50                               # lines picked as cases from the racks; the rest are eaches from shelving
T_CASE, T_EACH = 1.00, 1.10                     # minutes a line, manual with scanners (walk, find, pick, confirm)
ERR_LINE, COST_ERR = 0.0004, 75.0               # errors reaching customers a line with scan at pick and pack (Part 5); $ each
RENT_FT2 = 14.77                                # $ a sq ft a year, Canadian industrial net rent (Part 1)
SHELF_M2 = 560.0                                # floor taken by the shelving area (7 rows x 40 m, with aisles)
VOLS = [150, 200, 300, 400, 500, 600, 700, 800, 900]
STEPS = [150, 300, 600, 900]
TODAY = 300
OPTS = ["base", "ptl", "vlm", "amr"]
ONAME = {"base": "Manual with scanners", "ptl": "Pick-to-light", "vlm": "Vertical lift modules", "amr": "Mobile robots"}

PTL = dict(locs=300, per_loc=200.0, software=25000.0, maint=0.08, a_share=0.65, cut=0.35, err_cut=0.5, life=8)
VLM = dict(units=2, height_ft=25, per_ft=7500.0, install=30000.0, maint=6000.0, cut=0.45, err_cut=0.5, footprint=0.15, trays_h=120, life=12)
AMR = dict(fee=2500.0, setup=40000.0, lines_h=70.0, min_fleet=3, cut=0.50, life=5)
SPACE_VALUED = True                              # the freed floor is worth rent only if it saves a move or an extension


def lines(v):
    n = v * LINES
    return n * CASE_SHARE, n * (1 - CASE_SHARE)


def run(opt, v, space=SPACE_VALUED):
    case, each = lines(v)
    r = dict(opt=opt, v=v, one=0.0, run=0.0, labour_h=0.0, err=0.0, space=0.0, freed=0.0, units=0, note="")
    if opt == "ptl":
        p = PTL; r["one"] = p["locs"] * p["per_loc"] + p["software"]; r["run"] = r["one"] * p["maint"]
        r["labour_h"] = each * p["a_share"] * T_EACH * p["cut"] / 60
        r["err"] = each * p["a_share"] * ERR_LINE * p["err_cut"] * COST_ERR * DAYS; r["units"] = p["locs"]
    elif opt == "vlm":
        p = VLM; r["one"] = p["units"] * p["height_ft"] * p["per_ft"] + p["install"]; r["run"] = p["units"] * p["maint"]
        r["labour_h"] = each * T_EACH * p["cut"] / 60
        r["err"] = each * ERR_LINE * p["err_cut"] * COST_ERR * DAYS; r["units"] = p["units"]
        r["freed"] = SHELF_M2 * (1 - p["footprint"]); r["space"] = r["freed"] * 10.764 * RENT_FT2 if space else 0.0
        r["tray_load"] = each / HOURS / (p["units"] * p["trays_h"])
    elif opt == "amr":
        p = AMR; n = max(p["min_fleet"], math.ceil(case / HOURS / p["lines_h"])); r["units"] = n
        r["one"] = p["setup"]; r["run"] = n * p["fee"] * 12
        r["labour_h"] = case * T_CASE * p["cut"] / 60
        r["util"] = case / HOURS / (n * p["lines_h"])
    r["labour"] = r["labour_h"] * WAGE * DAYS
    r["saving"] = r["labour"] + r["err"] + r["space"]
    r["net"] = r["saving"] - r["run"]
    r["payback"] = r["one"] / r["net"] if r["net"] > 0 else None
    r["people"] = r["labour_h"] / 7.0                         # floor people's worth of work a day (7 productive hours)
    return r


def payback_volume(opt, years=3.0, space=SPACE_VALUED):
    """Lowest volume (orders a day) at which the option pays back within `years`, or None up to 3,000."""
    for v in range(50, 3001, 10):
        p = run(opt, v, space)["payback"]
        if p is not None and p <= years: return v
    return None


if __name__ == "__main__":
    for v in VOLS:
        print(v, {o: (round(run(o, v)["payback"], 1) if run(o, v)["payback"] else None) for o in OPTS[1:]}, "vlm no space", run("vlm", v, False)["payback"])
    for o in OPTS[1:]:
        r = run(o, TODAY); print(o, round(r["one"]), round(r["run"]), round(r["saving"]), round(r["labour_h"], 1), r["units"], payback_volume(o), payback_volume(o, space=False) if o == "vlm" else "")
