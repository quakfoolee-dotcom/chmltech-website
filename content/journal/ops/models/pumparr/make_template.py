"""Builds Pump_Arrangement_Comparison_Template_V1.xlsx from the arrangement model outputs."""
import json, numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.comments import Comment

import os
SRC = os.path.dirname(os.path.abspath(__file__)) + "/"
R = json.load(open(SRC + "arr_results.json")); D = np.load(SRC + "arr_scenarios.npz")
# hydraulic cases from the appendix script (same 20,000 cases)
src = open(SRC + "pump_arrangement_appendix.py").read().split("X = sample(20000)")[0]
g = {}; exec(src, g)
X = g["sample"](20000); Qn = 6250 * X["rate"] / 0.85 * (1 + X["recycle"]) / g["rho"](X["T"])
HY = {}
for lab, Q in (("N", Qn), ("T", 0.5 * Qn)):
    H, r = g["system_head"](X, Q); HY[lab + "Q"], HY[lab + "H"] = Q, H
    HY[lab + "A"], _ = g["valve"](Q, H, r, 1, 100); HY[lab + "B"], _ = g["drive"](Q, H, r, 1, 100)
    P1, dp1 = g["valve"](Q, H, r, 1, 50); P2, _ = g["valve"](Q, H, r, 2, 50); HY[lab + "C"] = np.where(dp1 >= 0.7, P1, P2)
    E1, n1 = g["drive"](Q, H, r, 1, 50); E2, n2 = g["drive"](Q, H, r, 2, 50); HY[lab + "E"] = np.where((n1 <= 1) & (E1 <= E2), E1, E2)
    HY[lab + "rho"] = r

AR = Font(name="Arial", size=10); B = Font(name="Arial", size=10, bold=True); BL = Font(name="Arial", size=10, color="0000FF")
GR = Font(name="Arial", size=10, color="008000"); T1 = Font(name="Arial", size=14, bold=True)
HDR = PatternFill("solid", fgColor="1F3864"); HF = Font(name="Arial", size=10, bold=True, color="FFFFFF")
YEL = PatternFill("solid", fgColor="FFFF00"); GRY = PatternFill("solid", fgColor="F2F2F2")
thin = Side(style="thin", color="BFBFBF"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")

wb = Workbook()
def sheet(name, first=False):
    ws = wb.active if first else wb.create_sheet(name); ws.title = name; ws.sheet_view.showGridLines = False; return ws
def hdr(ws, row, labels, col=1):
    for i, t in enumerate(labels):
        c = ws.cell(row, col + i, t); c.font = HF; c.fill = HDR; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = BOX
def put(ws, ref, v, font=AR, fmt=None, fill=None):
    c = ws[ref]; c.value = v; c.font = font
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    return c

OPTS = ["A", "B", "C3", "C2", "E3", "E2"]
DESC = {"A": "1 x 100% + spare, control valve", "B": "1 x 100% + spare, VFDs, no valve",
        "C3": "2 x 50% + spare, control valve, staged", "C2": "2 x 50%, no spare, control valve, staged",
        "E3": "2 x 50% + spare, VFDs, staged", "E2": "2 x 50%, no spare, VFDs, staged"}
Qr = R["rated"]["Qr"]; eta_size = lambda q: float(np.interp(np.log(q), np.log([5.34, 10.68, 20.0, 40.0, 80.0, 160.0, 320.0, 640.0]),
                                     [0.34, 0.40, 0.50, 0.60, 0.68, 0.74, 0.78, 0.80]))   # as in the model

# ---------------- README ----------------
ws = sheet("README", True)
ws.column_dimensions["A"].width = 26; ws.column_dimensions["B"].width = 100
put(ws, "A1", "Pump Arrangement Comparison Under Uncertainty - Template V1", T1)
rows = [
 ("Paper", "Choosing the Pump Arrangement Under Uncertainty: Monte Carlo Comparison of Single, Parallel and Variable-Speed Options (Chmltech Online Journal). Author: Quak Foo Lee, Chmltech Ltd., Vancouver, BC."),
 ("What it does", "Compares six pump arrangements (A, B, C3, C2, E3, E2) for one service on 20-year life-cycle cost: installed capital plus present value of electricity, repairs and lost production. It holds the full Monte Carlo record of the paper: 5,000 economic scenarios (sampled inputs, simulated failures and outages) and 20,000 hydraulic operating cases."),
 ("Live parts", "Inputs (blue cells) drive the life-cycle cost of every scenario, the cheapest option, the regret and all summary statistics through formulas. Change an electricity price range basis, an installed cost, a power figure or the discount rate and every result updates."),
 ("Not live", "The sampled scenario inputs, the simulated failures and lost hours (discrete-event simulation) and the hydraulic case solutions (non-linear speed and staging solves) are stored as values from the Python model. To resample or re-simulate, run pump_arrangements_model.py and paste the new columns. The off-region failure penalty is applied live: failures and outage hours are rescaled from the simulated penalty to the one implied by the current inputs."),
 ("Sheet guide", "Inputs: constants, option data, ranges used.  Calculator: one deterministic scenario you set by hand.  Scenarios: 5,000 Monte Carlo scenarios with live LCC, cheapest option and regret.  Results: summary statistics (formulas) checked against the paper.  Hydraulic_Cases: 20,000 operating cases with electrical power of A, B, C and E at normal rate and 50% turndown.  Sensitivity: rank-correlation drivers, duty-size results, valve-kept case, curve shape.  Changelog."),
 ("Legend", "Blue text = input you may change. Yellow fill = key assumption to replace with plant data. Black = formula. Green = link to another sheet. Grey fill = stored model output (values)."),
 ("Example", "Calculator sheet comes filled with the most likely value of every input; it gives the base-case life-cycle cost of each option."),
 ("Units", "Costs in Canadian dollars (C$, 2025 basis). Power in kW, flow in m3/h, head in m, time in hours or years."),
 ("Limits", "Generic pump curves, efficiencies and cost correlations; reliability inputs are industry benchmarks, not plant records; lost production valued at product margin only. Replace yellow cells with your own data."),
]
for i, (k, v) in enumerate(rows, start=3):
    put(ws, f"A{i}", k, B).alignment = WRAP; c = put(ws, f"B{i}", v); c.alignment = WRAP
    ws.row_dimensions[i].height = max(15, 15 * (len(v) // 95 + 1))

# ---------------- Inputs ----------------
wi = sheet("Inputs")
for col, w in zip("ABCDEFGHIJKLMNO", (38, 14, 12, 14, 14, 12, 12, 12, 16, 14, 12, 12, 12, 12, 40)): wi.column_dimensions[col].width = w
put(wi, "A1", "Inputs and ranges used", T1)
hdr(wi, 3, ["Constant", "Value", "Unit", "Basis"])
consts = [("Operating hours a year", 8000, "h/y", "Issue 8 design basis", "0"),
          ("Product rate at design", 6.25, "t/h", "50,000 t/y plant at 8,000 h/y", "0.00"),
          ("Discount rate", 0.08, "-", "Owner's rate", "0.0%"),
          ("Life", 20, "years", "Evaluation period", "0"),
          ("Present-value factor", "=(1-(1+B6)^-B7)/B6", "-", "Eq. (4)", "0.000"),
          ("Repair cost per drive failure", 3000, "C$", "Budget allowance", "#,##0"),
          ("Rated flow of the 100% pump (P95)", Qr, "m3/h", "Issue 8", "0.000"),
          ("Rated head (P95)", R["rated"]["Hr"], "m", "Issue 8", "0.000"),
          ("Switchover dip on standby start", R["const"]["LSW"], "h", "Used in simulation", "0.00"),
          ("Manual start after fail-to-start", R["const"]["TMAN"], "h", "Used in simulation", "0.00")]
for i, (k, v, u, b, f) in enumerate(consts, start=4):
    put(wi, f"A{i}", k); put(wi, f"B{i}", v, AR if str(v).startswith("=") else BL, f); put(wi, f"C{i}", u); put(wi, f"D{i}", b)
for r_ in (4, 6, 7): wi[f"B{r_}"].fill = YEL
# option table
r0 = 16
hdr(wi, r0, ["Option", "Description", "Pump size (%)", "Power normal (kW)", "Power at 50% turndown (kW)",
             "Share in pref. region, normal", "Share in pref. region, turndown", "Efficiency size factor",
             "Pump trains + valve, installed (C$)", "Drives, installed (C$)", "Uses f_small (1=yes)",
             "Failure reduction at turndown", "Outage reduction at turndown", "Repair cost factor", "Basis"])
for i, o in enumerate(OPTS):
    r = r0 + 1 + i; key = o if o in ("A", "B") else o[0]; Hk = R["hyd"][key]; big = o in ("A", "B")
    q = Qr if big else Qr / 2; k = (0.40 if big else 0.34) / eta_size(q); cx = R["capex_base"][o]
    vals = [o, DESC[o], 100 if big else 50, Hk["normal"]["P_el"], Hk["turndown"]["P_el"], Hk["normal"]["por"],
            Hk["turndown"]["por"], k, cx["trains"] + cx["valve"], cx["drives"], 0 if big else 1,
            R["td_factors"]["fail"][o], R["td_factors"]["lost"][o], 1.0 if big else 0.5 ** 0.4,
            "Hydraulic layer means over 20,000 cases; Towler & Sinnott with Hand factors"]
    fm = [None, None, "0", "0.000", "0.000", "0%", "0%", "0.0000", "#,##0", "#,##0", "0", "0.00", "0.00", "0.000", None]
    for j, (v, f) in enumerate(zip(vals, fm)):
        c = wi.cell(r, 1 + j, v); c.font = BL if 3 <= j <= 13 else AR; c.border = BOX
        if f: c.number_format = f
    for j in (8, 9): wi.cell(r, 1 + j).fill = YEL
wi.cell(r0 + 8, 1, "Power includes motor (92%) and drive (97%) losses. Efficiency size factor = baseline efficiency / size correlation (1 at this duty). Turndown reductions: share of failures / outage hours removed for the hours at turndown, when only one 50% pump runs. Repair cost factor: 50% pump = 0.5^0.4.").font = Font(name="Arial", size=9, italic=True)
OPT_ROW = {o: r0 + 1 + i for i, o in enumerate(OPTS)}
# ranges used
r1 = r0 + 10
hdr(wi, r1, ["Uncertain input (scenario layer)", "Min", "Most likely", "Max", "Distribution", "Unit", "Sampled P5", "Sampled P50", "Sampled P95", "", "", "Basis"])
RANGES = [("price", "Electricity price", 0.07, 0.09, 0.13, "Triangular", "C$/kWh", "Industrial tariffs; hold H-02", "0.000"),
          ("ftd", "Share of hours at 50% turndown", 0.0, None, 0.25, "Uniform", "-", "Operating plan", "0%"),
          ("f_eta", "Pump efficiency factor (all pumps)", 0.90, 1.00, 1.12, "Triangular", "-", "Generic curves; hold H-01", "0.000"),
          ("f_small", "Extra factor, 50% pumps", 0.93, 1.00, 1.10, "Triangular", "-", "Smaller pump efficiency", "0.000"),
          ("mtbf", "Pump MTBF, running", 1.5, 2.5, 4.5, "Triangular", "years", "ASME B73.1 benchmarks (Budris, 2017)", "0.00"),
          ("mttr", "Mean time to repair", 24, 72, 168, "Triangular", "h", "Plant practice", "0"),
          ("fts", "Standby failure to start", 0.002, 0.01, 0.03, "Triangular", "per demand", "INL (2009) as lower bound", "0.000"),
          ("crep", "Repair cost per pump failure", 6000, 10000, 20000, "Triangular", "C$", "Bloch & Budris (2004)", "#,##0"),
          ("margin", "Product margin", 150, 300, 500, "Triangular", "C$/t", "Plant economics", "#,##0"),
          ("trest", "Restart after total loss of feed", 4, 8, 16, "Triangular", "h", "Plant practice", "0.0"),
          ("mtbf_vfd", "Drive MTBF", 8, 15, 25, "Triangular", "years", "TMEIC fleet data", "0.0"),
          ("kcap", "Installed cost factor, pumps and valve", None, 1.0, None, "Lognormal, sigma 0.15", "-", "Factored estimate", "0.000"),
          ("kvfd", "Installed cost factor, drives", 0.7, 1.0, 1.5, "Triangular", "-", "Budget prices", "0.000"),
          ("f_bep", "Off-region failure penalty", 1.0, 1.5, 2.0, "Triangular", "-", "Barringer curve (Hardee, 2026)", "0.00")]
for i, (key, name, a, m, b, dist, u, basis, f) in enumerate(RANGES):
    r = r1 + 1 + i; s = R["scen_inputs"].get(key, {})
    for j, (v, ff) in enumerate(zip([name, a, m, b, dist, u, s.get("p5"), s.get("p50"), s.get("p95"), None, None, basis],
                                     [None, f, f, f, None, None, f, f, f, None, None, None])):
        c = wi.cell(r, 1 + j, v); c.font = AR; c.border = BOX
        if ff: c.number_format = ff
        if j in (6, 7, 8): c.fill = GRY
wi.cell(r1 + 16, 1, "Ranges are documentation of the sampling; the stored scenarios were drawn from them (seeded). Edit the scenario columns or rerun the model to change them.").font = Font(name="Arial", size=9, italic=True)
wi.freeze_panes = "A4"

# ---------------- Scenarios ----------------
wsx = sheet("Scenarios")
NS = len(D["sc_price"]); SC = [k for k, *_ in RANGES]
cols = ["Scenario"] + [n for _, n, *_ in RANGES]
simc = []
for o in OPTS:
    simc += [f"{o} failures/y (sim)", f"{o} lost h/y (sim)", f"{o} drive share of failures", f"{o} penalty used in sim"]
lccc = [f"{o} LCC (C$)" for o in OPTS]; regc = [f"{o} regret (C$)" for o in OPTS]
allc = cols + simc + lccc + ["Cheapest"] + regc
hdr(wsx, 1, allc); wsx.row_dimensions[1].height = 54; wsx.freeze_panes = "B2"
ci = {name: i + 1 for i, name in enumerate(allc)}
inp_col = {k: CL(2 + i) for i, k in enumerate(SC)}
FM = {k: f for k, *_, f in RANGES}
for j in range(NS):
    r = j + 2; wsx.cell(r, 1, j + 1).font = AR
    for i, k in enumerate(SC):
        c = wsx.cell(r, 2 + i, float(D["sc_" + k][j])); c.number_format = FM[k]; c.fill = GRY; c.font = AR
    base = 2 + len(SC)
    for oi, o in enumerate(OPTS):
        for kk, nm in enumerate(("nfail", "lost_h", "frac_v", "pen")):
            c = wsx.cell(r, base + 4 * oi + kk, float(D[f"{o}_{nm}"][j])); c.fill = GRY; c.font = AR
            c.number_format = "0.000" if nm != "lost_h" else "0.000"
LCC0 = ci[lccc[0]]; CH = ci["Cheapest"]; REG0 = ci[regc[0]]
sim0 = 2 + len(SC)
ip = lambda k, r: f"{inp_col[k]}{r}"
for oi, o in enumerate(OPTS):
    orow = OPT_ROW[o]; s0 = sim0 + 4 * oi
    nf, lh, fv, pn = (CL(s0 + t) for t in range(4))
    I = lambda col: f"Inputs!${col}${orow}"
    for j in range(NS):
        r = j + 2
        ftd = ip("ftd", r)
        adj = f"(1+({ip('f_bep', r)}-1)*((1-{ftd})*(1-{I('F')})+{ftd}*(1-{I('G')})))/{pn}{r}"
        energy = (f"Inputs!$B$4*((1-{ftd})*{I('D')}+{ftd}*{I('E')})*{I('H')}/({ip('f_eta', r)}*IF({I('K')}=1,{ip('f_small', r)},1))*{ip('price', r)}")
        rep = f"{nf}{r}*{adj}*(1-{I('L')}*{ftd})*((1-{fv}{r})*{ip('crep', r)}*{I('N')}+{fv}{r}*Inputs!$B$9)"
        lost = f"{lh}{r}*{adj}*(1-{I('M')}*{ftd})*Inputs!$B$5*{ip('margin', r)}"
        cap = f"{I('I')}*{ip('kcap', r)}+{I('J')}*{ip('kvfd', r)}"
        c = wsx.cell(r, LCC0 + oi, f"={cap}+Inputs!$B$8*({energy}+{rep}+{lost})"); c.number_format = "#,##0"; c.font = AR
L1, L6 = CL(LCC0), CL(LCC0 + 5)
for j in range(NS):
    r = j + 2
    c = wsx.cell(r, CH, f'=INDEX({{"A","B","C3","C2","E3","E2"}},MATCH(MIN({L1}{r}:{L6}{r}),{L1}{r}:{L6}{r},0))'); c.font = AR
    for oi in range(6):
        c = wsx.cell(r, REG0 + oi, f"={CL(LCC0 + oi)}{r}-MIN(${L1}{r}:${L6}{r})"); c.number_format = "#,##0"; c.font = AR
for i in range(1, len(allc) + 1): wsx.column_dimensions[CL(i)].width = 12
wsx.column_dimensions[CL(CH)].width = 14
LAST = NS + 1

# ---------------- Results ----------------
wr = sheet("Results")
for col, w in zip("ABCDEFGHIJKL", (34, 14, 14, 14, 14, 14, 14, 3, 30, 14, 14, 14)): wr.column_dimensions[col].width = w
put(wr, "A1", f"Results over {NS:,} scenarios (formulas on the Scenarios sheet)", T1)
hdr(wr, 3, ["Statistic"] + OPTS)
stats = [("Mean LCC (C$)", "AVERAGE({c})", "#,##0"), ("P5 LCC (C$)", "PERCENTILE({c},0.05)", "#,##0"),
         ("P50 LCC (C$)", "MEDIAN({c})", "#,##0"), ("P95 LCC (C$)", "PERCENTILE({c},0.95)", "#,##0"),
         ("Probability cheapest", None, "0.0%"), ("Mean regret (C$)", "AVERAGE({g})", "#,##0"),
         ("P95 regret (C$)", "PERCENTILE({g},0.95)", "#,##0"), ("Max regret (C$)", "MAX({g})", "#,##0")]
for i, (lab, f, fm) in enumerate(stats):
    r = 4 + i; put(wr, f"A{r}", lab)
    for oi, o in enumerate(OPTS):
        rng = f"Scenarios!${CL(LCC0 + oi)}$2:${CL(LCC0 + oi)}${LAST}"; rg = f"Scenarios!${CL(REG0 + oi)}$2:${CL(REG0 + oi)}${LAST}"
        if f is None: fx = f'=COUNTIF(Scenarios!${CL(CH)}$2:${CL(CH)}${LAST},"{o}")/{NS}'
        else: fx = "=" + f.format(c=rng, g=rg)
        c = wr.cell(r, 2 + oi, fx); c.number_format = fm; c.font = AR; c.border = BOX
# mean components (live)
put(wr, "A13", "Mean components (live)", B)
hdr(wr, 14, ["Component"] + OPTS)
comp = [("Installed capital (C$)", "I", "J", "kcap", "kvfd")]
for oi, o in enumerate(OPTS):
    orow = OPT_ROW[o]
    wr.cell(15, 2 + oi, f"=Inputs!$I${orow}*AVERAGE(Scenarios!${inp_col['kcap']}$2:${inp_col['kcap']}${LAST})+Inputs!$J${orow}*AVERAGE(Scenarios!${inp_col['kvfd']}$2:${inp_col['kvfd']}${LAST})").number_format = "#,##0"
    wr.cell(16, 2 + oi, f"=({CL(2+oi)}4-{CL(2+oi)}15)/Inputs!$B$8").number_format = "#,##0"
put(wr, "A15", "Installed capital (C$)"); put(wr, "A16", "Operating cost: electricity + repairs + lost production (C$/year)")
for oi in range(6):
    for rr in (15, 16): wr.cell(rr, 2 + oi).font = AR; wr.cell(rr, 2 + oi).border = BOX
# check vs paper
put(wr, "A19", "Check against the paper (model output)", B)
hdr(wr, 20, ["Statistic"] + OPTS)
paper = [("Mean LCC (C$)", "lcc_mean", "#,##0", 4), ("Probability cheapest", "p_cheapest", "0.0%", 8), ("Mean regret (C$)", "regret_mean", "#,##0", 9)]
for i, (lab, k, fm, srow) in enumerate(paper):
    r = 21 + 2 * i; put(wr, f"A{r}", lab + " - paper"); put(wr, f"A{r+1}", lab + " - difference (sheet minus paper)")
    for oi, o in enumerate(OPTS):
        c = wr.cell(r, 2 + oi, R["econ"][o][k]); c.number_format = fm; c.fill = GRY; c.font = AR; c.border = BOX
        c = wr.cell(r + 1, 2 + oi, f"={CL(2+oi)}{srow}-{CL(2+oi)}{r}"); c.number_format = fm; c.font = AR; c.border = BOX
put(wr, "A28", "Differences are zero to rounding until an input is changed. Model also reports: lost production and failures a year:", Font(name="Arial", size=9, italic=True))
hdr(wr, 29, ["Simulated (mean)"] + OPTS)
for i, (lab, k, fm) in enumerate([("Failures a year", "fail_y", "0.00"), ("Lost full-rate hours a year", "lost_h_y", "0.00"),
                                   ("Electricity (C$/year)", "energy_y", "#,##0"), ("Repairs (C$/year)", "repair_y", "#,##0"),
                                   ("Lost production (C$/year)", "lost_y", "#,##0")]):
    r = 30 + i; put(wr, f"A{r}", lab)
    for oi, o in enumerate(OPTS):
        c = wr.cell(r, 2 + oi, R["econ"][o][k]); c.number_format = fm; c.fill = GRY; c.font = AR; c.border = BOX

# ---------------- Calculator ----------------
wc = sheet("Calculator")
for col, w in zip("ABCDEFGH", (40, 14, 14, 14, 14, 14, 14, 14)): wc.column_dimensions[col].width = w
put(wc, "A1", "Single-scenario calculator (set every input by hand)", T1)
put(wc, "A2", "Filled with the most likely value of each range (example). Failures and lost hours are the simulated means; change them for your plant.", Font(name="Arial", size=9, italic=True))
hdr(wc, 4, ["Scenario input", "Value"])
CAL = {}
calv = [("price", 0.09), ("ftd", 0.125), ("f_eta", 1.0), ("f_small", 1.0), ("crep", 10000), ("margin", 300), ("kcap", 1.0), ("kvfd", 1.0), ("f_bep", 1.5)]
for i, (k, v) in enumerate(calv):
    r = 5 + i; nm = dict((a, b) for a, b, *_ in RANGES)[k]; put(wc, f"A{r}", nm); c = put(wc, f"B{r}", v, BL, FM[k], YEL); c.border = BOX; CAL[k] = f"$B${r}"
r = 16; hdr(wc, r, ["Per option"] + OPTS)
labels = ["Failures a year (simulation, both pumps running)", "Lost full-rate hours a year (simulation)", "Drive share of failures", "Penalty used in simulation (mean)",
          "Installed capital (C$)", "Electricity (C$/year)", "Repairs (C$/year)", "Lost production (C$/year)", "20-year life-cycle cost (C$)", "Rank (1 = cheapest)"]
for i, lab in enumerate(labels): put(wc, f"A{r+1+i}", lab)
for oi, o in enumerate(OPTS):
    col = CL(2 + oi); orow = OPT_ROW[o]; I = lambda c: f"Inputs!${c}${orow}"
    vals = [float(D[f"{o}_nfail"].mean()), float(D[f"{o}_lost_h"].mean()), float(D[f"{o}_frac_v"].mean()), float(D[f"{o}_pen"].mean())]
    for k, v in enumerate(vals):
        c = wc.cell(r + 1 + k, 2 + oi, v); c.font = BL; c.number_format = "0.000"; c.border = BOX
    adj = f"(1+({CAL['f_bep']}-1)*((1-{CAL['ftd']})*(1-{I('F')})+{CAL['ftd']}*(1-{I('G')})))/{col}{r+4}"
    f_cap = f"={I('I')}*{CAL['kcap']}+{I('J')}*{CAL['kvfd']}"
    f_e = f"=Inputs!$B$4*((1-{CAL['ftd']})*{I('D')}+{CAL['ftd']}*{I('E')})*{I('H')}/({CAL['f_eta']}*IF({I('K')}=1,{CAL['f_small']},1))*{CAL['price']}"
    f_r = f"={col}{r+1}*{adj}*(1-{I('L')}*{CAL['ftd']})*((1-{col}{r+3})*{CAL['crep']}*{I('N')}+{col}{r+3}*Inputs!$B$9)"
    f_l = f"={col}{r+2}*{adj}*(1-{I('M')}*{CAL['ftd']})*Inputs!$B$5*{CAL['margin']}"
    f_lcc = f"={col}{r+5}+Inputs!$B$8*({col}{r+6}+{col}{r+7}+{col}{r+8})"
    for k, fx in enumerate([f_cap, f_e, f_r, f_l, f_lcc]):
        c = wc.cell(r + 5 + k, 2 + oi, fx); c.number_format = "#,##0"; c.font = AR; c.border = BOX
    c = wc.cell(r + 10, 2 + oi, f"=RANK({col}{r+9},$B${r+9}:$G${r+9},1)"); c.font = B; c.border = BOX
put(wc, f"A{r+12}", "Cheapest option", B)
put(wc, f"B{r+12}", f'=INDEX($B${r}:$G${r},MATCH(MIN($B${r+9}:$G${r+9}),$B${r+9}:$G${r+9},0))', B)

# ---------------- Hydraulic cases ----------------
wh = sheet("Hydraulic_Cases")
names = list(X)
hc = ["Case"] + names + ["Flow, normal (m3/h)", "System head, normal (m)", "Density (kg/m3)",
      "A kW normal", "B kW normal", "C kW normal", "E kW normal", "A kW turndown", "B kW turndown", "C kW turndown", "E kW turndown"]
put(wh, "A1", "20,000 correlated operating cases (Issue 8) with electrical power of each arrangement - from the appendix script", B)
hdr(wh, 3, hc); wh.row_dimensions[3].height = 40; wh.freeze_panes = "B4"
put(wh, "A2", "Means:"); 
for j in range(20000):
    r = 4 + j; row = [j + 1] + [float(X[k][j]) for k in names] + [float(HY["NQ"][j]), float(HY["NH"][j]), float(HY["Nrho"][j])] + \
        [float(HY[f"N{o}"][j]) for o in "ABCE"] + [float(HY[f"T{o}"][j]) for o in "ABCE"]
    for i, v in enumerate(row):
        c = wh.cell(r, 1 + i, v)
        if i: c.number_format = "0.000"
for i in range(2 + len(names), len(hc) + 1):
    c = wh.cell(2, i, f"=AVERAGE({CL(i)}4:{CL(i)}20003)"); c.number_format = "0.00"; c.font = B
for i in range(1, len(hc) + 1): wh.column_dimensions[CL(i)].width = 12

# ---------------- Sensitivity ----------------
wsn = sheet("Sensitivity")
wsn.column_dimensions["A"].width = 40
for i in range(2, 16): wsn.column_dimensions[CL(i)].width = 12
put(wsn, "A1", "Sensitivity results (model output)", T1)
pairs = list(R["drivers"]); keys = list(R["drivers"][pairs[0]])
put(wsn, "A3", "Spearman rank correlation with the LCC difference between two options", B)
hdr(wsn, 4, ["Input"] + pairs)
nm = dict((a, b) for a, b, *_ in RANGES)
for i, k in enumerate(keys):
    put(wsn, f"A{5+i}", nm.get(k, k))
    for j, p in enumerate(pairs):
        c = wsn.cell(5 + i, 2 + j, R["drivers"][p][k]); c.number_format = "0.00"; c.fill = GRY
r = 6 + len(keys)
put(wsn, f"A{r}", "Probability cheapest against duty size (size factor x this service; same head)", B)
for blk, lab in (("base", "turndown share 0-25%"), ("0.5", "half the hours at turndown")):
    if blk not in R["p_by_size"]: blk = [k for k in R["p_by_size"] if k != "base"][0]
    pb = R["p_by_size"][blk]; r += 1; put(wsn, f"A{r}", lab, B); r += 1
    hdr(wsn, r, ["Size factor"] + [f"{s:.2f}" for s in pb["size"]])
    if "kw" in pb:
        r += 1; put(wsn, f"A{r}", "Mean power of B (kW)")
        for j, v in enumerate(pb["kw"]): wsn.cell(r, 2 + j, v).number_format = "0.0"
    for o in OPTS:
        r += 1; put(wsn, f"A{r}", o)
        for j, v in enumerate(pb["p"][o]): c = wsn.cell(r, 2 + j, v); c.number_format = "0.0%"; c.fill = GRY
    r += 1
r += 1; put(wsn, f"A{r}", "Option B with the control valve kept", B); r += 1
for k, lab, fm in (("lcc_mean", "Mean LCC (C$)", "#,##0"), ("p_beats_A", "Probability it beats A", "0.0%"), ("diff_mean", "Mean difference from A (C$)", "#,##0")):
    put(wsn, f"A{r}", lab); c = wsn.cell(r, 2, R["B_valve"][k]); c.number_format = fm; c.fill = GRY; r += 1
r += 1; put(wsn, f"A{r}", "Installed drive cost", B); r += 1
db = R["drive_breakeven"]
for lab, v, fm in (("Drive cost each, base (C$)", db["drive_cost_each"], "#,##0"), ("Mean LCC gap A minus B (C$)", db["gap"], "#,##0"),
                   ("Drive cost each at which B = A on average (C$)", db["each_at_breakeven"], "#,##0"),
                   ("Probability B cheapest, drives at 2x", db["pB_2.0"], "0.0%"), ("Probability B cheapest, drives at 3x", db["pB_3.0"], "0.0%")):
    put(wsn, f"A{r}", lab); c = wsn.cell(r, 2, v); c.number_format = fm; c.fill = GRY; r += 1
r += 1; put(wsn, f"A{r}", "Probability cheapest, full scenario set, share of hours at turndown fixed", B); r += 1
hdr(wsn, r, ["Share at turndown"] + OPTS); r += 1
for fd, row in R["ftd_full"].items():
    put(wsn, f"A{r}", f"{float(fd):.0%}")
    for j, o in enumerate(OPTS): c = wsn.cell(r, 2 + j, row[o]); c.number_format = "0.0%"; c.fill = GRY
    r += 1
r += 1; put(wsn, f"A{r}", "Pump curve shape (shutoff ratio)", B); r += 1
hdr(wsn, r, ["Shutoff / rated head", "Rated head (m)", "A kW normal", "A kW turndown", "C kW normal", "P(B cheapest)"]); r += 1
for k, v in R["shape"].items():
    vals = [float(k), v["Hr"], v["A"]["Pn"], v["A"]["Pt"], v["C"]["Pn"], v.get("p_cheapest", {}).get("B", R["econ"]["B"]["p_cheapest"])]
    for j, (x, fm) in enumerate(zip(vals, ["0.00", "0.00", "0.00", "0.00", "0.00", "0.0%"])):
        c = wsn.cell(r, 1 + j, x); c.number_format = fm
    r += 1

# ---------------- Changelog ----------------
wl = sheet("Changelog"); wl.column_dimensions["A"].width = 10; wl.column_dimensions["B"].width = 14; wl.column_dimensions["C"].width = 100
hdr(wl, 1, ["Version", "Date", "Change"])
wl["A2"], wl["B2"], wl["C2"] = "V1", "2026-11-18", "First issue (after red-team fixes to the model): inputs and ranges, 5,000 live scenarios, results with paper check, calculator, 20,000 hydraulic cases, sensitivity incl. drive cost break-even, curve shape and long turndown."
for c in ("A2", "B2", "C2"): wl[c].font = AR
for w in wb.worksheets:
    for row in w.iter_rows():
        for c in row:
            if c.font is None or c.font.name != "Arial": c.font = Font(name="Arial", size=10, bold=c.font.bold if c.font else False)
wb.save(SRC + "chmltech-pump-arrangement-template.xlsx")
print("saved", NS)
