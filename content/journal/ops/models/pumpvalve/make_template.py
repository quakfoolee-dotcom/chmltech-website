"""Equipment list template with Monte Carlo basis columns (Chmltech Online Journal). V5.
V5 (second red team): pump best-efficiency flow, end-of-curve power and motor size are live formulas (follow the
P90/P95/P99 selector); efficiency 40%; FCV-101 upstream of E-101 with valve cases recomputed from the model;
choked limit uses (FLP/Fp)^2; valve rows labelled as sized for P95 with the model's valve per level; hold H-05 on
the pump; model renamed pumpvalve_model.py; Python column aligned with Excel case set.
V4: adds the full Monte Carlo record: MC inputs (distributions, correlations, fixed parameters), MC data (all 20,000
cases with per-case hydraulics and live formulas for rated head, valve pressure drop, Cv and opening) and MC results
(percentiles and rated points recalculated in Excel, checked against the Python model). MC summary now links to them.
V2: end-of-curve motor check, 115% motor factor for 22-55 kW, design pressure with tank relief set and 5% impeller head
increase, valve Fp per case and case labels, tank basis, hold links corrected."""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter

F = "Arial"
H = Font(name=F, bold=True, color="FFFFFF", size=10); HF = PatternFill("solid", fgColor="1B2A41")
IN = Font(name=F, color="0000FF", size=10); CALC = Font(name=F, color="000000", size=10); LINK = Font(name=F, color="008000", size=10)
YEL = PatternFill("solid", fgColor="FFF2CC"); B = Font(name=F, bold=True, size=10); T = Font(name=F, bold=True, size=14, color="1B2A41")
thin = Side(style="thin", color="C9D3E0"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WR = Alignment(wrap_text=True, vertical="top")
wb = Workbook()


def header(ws, row, cols, widths):
    for j, (c, w) in enumerate(zip(cols, widths), 1):
        x = ws.cell(row, j, c); x.font = H; x.fill = HF; x.alignment = Alignment(wrap_text=True, vertical="center"); x.border = BOX
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.row_dimensions[row].height = 48


def put(ws, r, c, v, kind="in", fmt=None):
    x = ws.cell(r, c, v); x.border = BOX; x.alignment = WR
    x.font = {"in": IN, "calc": CALC, "link": LINK}[kind]
    if kind == "in": x.fill = YEL
    if fmt: x.number_format = fmt
    return x


# ---------------- Legend ----------------
ws = wb.active; ws.title = "Legend"
rows = [("Equipment list template with Monte Carlo basis", T),
        ("Companion to: Lee, Q. F. (2026). Sizing pumps and control valves under uncertainty: Monte Carlo design points for chemical plants. Chmltech Online Journal.", None),
        ("", None),
        ("How to use", B),
        ("1. Yellow cells with blue text are inputs: type your own values over the example rows (one example row per sheet, from the paper's feed system).", None),
        ("2. Black cells are formulas; green cells link to another sheet. Do not type over them.", None),
        ("3. Choose the confidence level in 'MC summary' (P90, P95 or P99); the Pumps sheet picks up the rated point. For the example pump the percentiles come live from 'MC results'; for your own pumps paste the model's percentiles over them.", None),
        ("4. Every rated number needs an entry in the 'Basis' column, and every open input a hold number (H-xx) listed in 'Holds'.", None),
        ("5. Rerun the model and update 'MC summary' at each revision of the PFD, line list or vendor data; log the change in 'Revision log'.", None),
        ("", None),
        ("Monte Carlo record (example pump P-101A/B)", B),
        ("MC inputs: the eleven uncertain inputs with their distributions, ranges, base, stacked and moderate values and basis; the rank correlations; every fixed parameter of the model. Yellow cells there (minimum valve drop, curve shape, valve Cv and rangeability) feed live formulas.", None),
        ("MC data: all 20,000 simulated cases (seed 1): sampled inputs, fluid properties, demand flow, suction and delivery pressures, system head and NPSHa from the Python model, then live formulas for the head each case needs, the rated head it implies at P90/P95/P99, and, for the selected pump, the valve pressure drop, control and delivery flags, Cv required and opening.", None),
        ("MC results: percentiles of flow and head, rated points and the selected pump's coverage and valve opening, recalculated in Excel from MC data and compared with the Python model; plus the model results Excel cannot rerun (deterministic baselines, designs, sensitivity, convergence, conditional coverage).", None),
        ("To change an input range or correlation, edit pumpvalve_model.py and rerun it; Excel cannot resample. The data sheet then needs the new cases pasted in.", None),
        ("The P90/P95/P99 selector drives the Pumps sheet (rated point, BEP flow, end-of-curve power, motor) and MC data. FCV-101, the Control valves sheet and the valve rows of MC results are for the valve as sized for the P95 pump (1.5-inch, Cv 34); at P90 or P99 the model selects a different valve (MC results lists it).", None),
        ("", None),
        ("Checks built in", B),
        ("Pumps: motor at least 125% of rated power below 22 kW, 115% for 22-55 kW and 110% above (API 610, where the owner specifies it) and not less than the end-of-curve power; NPSH margin at least 1 m; rated flow inside 80-110% of best-efficiency flow; design pressure from shutoff head with a 5% larger impeller at maximum density plus the maximum suction pressure (full tank at its relief set pressure), +10%, rounded up to 0.5 bar.", None),
        ("Control valves (IEC 60534-2-1, liquids): opening from an equal-percentage characteristic; choked flow when the pressure drop reaches FL^2 (p1 - FF pv) (use (FLP/Fp)^2 when reducers are fitted); cavitation warning when xF = dp/(p1 - pv) reaches xFz (IEC 60534-8-4; assumed trim value).", None),
        ("", None),
        ("Units: flow m3/h, head m, pressure bar (barg or bara as labelled), power kW, temperature deg C.", None),
        ("Template V5, Nov 2026. Illustrative values; confirm every rated point against vendor data.", None)]
for i, (t, f) in enumerate(rows, 1):
    c = ws.cell(i, 1, t); c.font = f or Font(name=F, size=10); c.alignment = Alignment(wrap_text=True, vertical="top")
ws.column_dimensions["A"].width = 120

# ---------------- MC summary ----------------
ms = wb.create_sheet("MC summary")
ms["A1"] = "Monte Carlo summary per pump (paste from the model)"; ms["A1"].font = T
header(ms, 3, ["Tag", "Cases", "Confidence level used", "P50 flow (m3/h)", "P90 rated flow", "P95 rated flow", "P99 rated flow",
               "P90 rated head (m)", "P95 rated head (m)", "P99 rated head (m)", "Stacked-margin rated flow", "Stacked-margin rated head",
               "Rated flow chosen", "Rated head chosen", "Head saved vs stacked"], [12, 9, 13, 11, 11, 11, 11, 12, 12, 12, 13, 13, 12, 12, 12])
vals = ["P-101A/B", 20000, "P95", 9.68, 10.48, 10.68, 10.99, 81.4, 82.5, 84.7, 11.76, 106.6]
for j, v in enumerate(vals, 1):
    put(ms, 4, j, v, "in", "0.00" if isinstance(v, float) and j < 8 else ("0.0" if isinstance(v, float) else None))
for j, ref in zip([2, 4, 5, 6, 7, 8, 9, 10], ["N_cases", "Q_P50", "Qr_P90", "Qr_P95", "Qr_P99", "Hr_P90", "Hr_P95", "Hr_P99"]):
    put(ms, 4, j, "=" + ref, "link", "#,##0" if j == 2 else ("0.00" if j < 8 else "0.0"))
ms.cell(4, 5).comment = Comment("Example row links live to 'MC results'. For your own pumps, type the model's percentiles here.", "Chmltech")
put(ms, 4, 13, '=INDEX(E4:G4,MATCH(C4,{"P90","P95","P99"},0))', "calc", "0.00")
put(ms, 4, 14, '=INDEX(H4:J4,MATCH(C4,{"P90","P95","P99"},0))', "calc", "0.0")
put(ms, 4, 15, "=IF(L4>0,1-N4/L4,0)", "calc", "0.0%")
dv = DataValidation(type="list", formula1='"P90,P95,P99"', allow_blank=False); ms.add_data_validation(dv); dv.add("C4:C40")
ms["A6"] = "Rated flow = the chosen percentile of demand flow. Rated head = the lowest head at rated flow on the expected curve shape that keeps the minimum control valve pressure drop in that share of cases (paper, Section 3)."
ms["A6"].font = Font(name=F, size=9, italic=True)

# ---------------- Pumps ----------------
ps = wb.create_sheet("Pumps")
ps["A1"] = "Equipment list: pumps"; ps["A1"].font = T
ps["A2"] = "Project: <project>   Document: <doc no. (provisional)>   Rev: A   Date: <date>"; ps["A2"].font = Font(name=F, size=10)
cols = ["Tag", "Service", "Type", "Number (duty + spare)", "Fluid", "Normal flow (m3/h)", "Rated flow (m3/h)", "Rated / normal flow",
        "Normal head (m)", "Rated head (m)", "Rated / normal head", "Basis of rated point", "Best-efficiency flow (m3/h)", "Rated flow / BEP flow",
        "Shutoff head (m)", "Max SG", "Max suction pressure (barg)", "Max discharge pressure (barg)", "Design pressure (barg)",
        "Pump efficiency at rated", "Rated power at max SG (kW)", "Motor (kW)", "Motor / rated power", "Motor check (API 610)",
        "NPSHa min (m)", "NPSHr at rated (m)", "NPSH margin (m)", "NPSH check", "Holds", "Rev", "End-of-curve power at max SG (kW)"]
header(ps, 4, cols, [11, 18, 14, 10, 14, 10, 10, 10, 10, 10, 10, 30, 11, 10, 10, 8, 11, 11, 11, 10, 11, 9, 10, 12, 10, 10, 10, 10, 14, 6, 12])
r = 5
for j, v in enumerate(["P-101A/B", "Reactor feed pump", "Centrifugal, end suction (ASME B73.1 / ISO 5199; API 610 OH2 if specified)", "1 + 1", "Organic feed blend", 9.80], 1):
    put(ps, r, j, v, "in", "0.00" if j == 6 else None)
put(ps, r, 7, "='MC summary'!M4", "link", "0.00"); put(ps, r, 8, "=G5/F5", "calc", "0.00")
put(ps, r, 9, 75.2, "in", "0.0"); put(ps, r, 10, "='MC summary'!N4", "link", "0.0"); put(ps, r, 11, "=J5/I5", "calc", "0.00")
put(ps, r, 12, '="Monte Carlo "&\'MC summary\'!C4&" of "&TEXT(\'MC summary\'!B4,"#,##0")&" correlated cases; 0.7 bar kept across FCV-101"', "calc")
put(ps, r, 13, "=1.05*G5", "calc", "0.00"); put(ps, r, 14, "=G5/M5", "calc", "0.00")
ps.cell(r, 13).comment = Comment("Generic curve: best efficiency at 1.05 x rated flow. Replace with the vendor curve (H-01).", "Chmltech")
put(ps, r, 15, "=1.2*J5", "calc", "0.0"); ps.cell(r, 15).comment = Comment("Replace with the vendor's shutoff head once a pump is quoted (hold H-01). 1.2 x rated head is a typical radial-impeller value.", "Chmltech")
put(ps, r, 16, 0.914, "in", "0.000"); put(ps, r, 17, 0.86, "in", "0.00")
ps.cell(r, 17).comment = Comment("Full tank at the tank relief set pressure (0.10 barg assumed, hold H-05).", "Chmltech")
put(ps, r, 18, "=Q5+1.05*O5*P5*9.81/100", "calc", "0.00")
ps.cell(r, 18).comment = Comment("Includes the 5% head increase from a larger impeller (API 610).", "Chmltech")
put(ps, r, 19, "=CEILING(R5*1.1*2,1)/2", "calc", "0.0")
put(ps, r, 20, 0.40, "in", "0%")
ps.cell(r, 20).comment = Comment("40% best efficiency, typical of a pump this small (specific speed about 6). Vendor curve replaces it (H-01).", "Chmltech")
put(ps, r, 21, "=G5/3600*P5*1000*9.81*J5/T5/1000", "calc", "0.00")
put(ps, r, 22, '=_xlfn.MINIFS($AH$5:$AH$20,$AH$5:$AH$20,">="&MAX(U5*IF(U5<22,1.25,IF(U5<=55,1.15,1.1)),AE5))', "calc", "0.0"); put(ps, r, 23, "=V5/U5", "calc", "0.00")
ps.cell(r, 22).comment = Comment("Smallest standard motor (column AH) covering the API 610 factor on rated power and the end-of-curve power. Type over it to check another size.", "Chmltech")
put(ps, r, 24, '=IF(AND(V5>=U5*IF(U5<22,1.25,IF(U5<=55,1.15,1.1)),V5>=AE5),"OK","Too small")', "calc")
put(ps, r, 25, 11.5, "in", "0.0"); put(ps, r, 26, 1.9, "in", "0.0"); put(ps, r, 27, "=Y5-Z5", "calc", "0.0")
put(ps, r, 28, '=IF(AND(AA5>=1,Y5/Z5>=1.1),"OK","Check")', "calc")
put(ps, r, 29, "H-01, H-04, H-05", "in"); put(ps, r, 30, "A", "in")
put(ps, r, 31, "=1.2*M5/3600*P5*1000*9.81*J5*(1.2-0.2*(1.2*M5/G5)^2)/(T5*(2*1.2-1.2^2))/1000", "calc", "0.00")
ps.cell(r, 31).comment = Comment("Power at 120% of best-efficiency flow, maximum density, on the generic curve (efficiency 0.8 x best at that flow).", "Chmltech")
ps.cell(4, 34, "Standard motor sizes (kW)").font = H; ps.cell(4, 34).fill = HF; ps.column_dimensions["AH"].width = 12
for i_, kw in enumerate([0.75, 1.1, 1.5, 2.2, 3.0, 4.0, 5.5, 7.5, 11.0, 15.0, 18.5, 22.0, 30.0, 37.0, 45.0, 55.0]):
    put(ps, 5 + i_, 34, kw, "in", "0.0#")
ps.freeze_panes = "C5"

# ---------------- Control valves ----------------
cs = wb.create_sheet("Control valves")
cs["A1"] = "Equipment list: control valves (IEC 60534-2-1, liquids)"; cs["A1"].font = T
cols = ["Tag", "Service", "Line size (in)", "Body size (in)", "Trim / characteristic", "Rated Cv", "Rangeability R", "FL",
        "Critical pressure pc (bara)", "Case", "Flow (m3/h)", "SG", "p1 (bara)", "Valve dp (bar)", "pv (kPa abs)", "Fp",
        "Cv required", "Opening (%)", "FF", "Choked-flow dp limit (bar)", "Choked?", "xF", "xFz", "Cavitation", "Opening check", "Basis", "Holds", "FLP / Fp (with reducers)"]
header(cs, 3, cols, [10, 16, 8, 8, 14, 8, 9, 6, 10, 12, 9, 7, 9, 9, 9, 7, 9, 9, 7, 11, 9, 7, 7, 11, 11, 30, 10, 11])
import numpy as _np, json as _json
import pumpvalve_model as _M
_R = _json.load(open("results.json")); _d = _R["designs"]["mc95"]
_X = _M.sample(20000, seed=1); _pp = _M.Pump(_d["Qr"], _d["Hr"])
cases = []
for _lab, _o, _q in (("Median Cv case", _M.operate(_X, _pp), 50), ("99th-percentile Cv case", _M.operate(_X, _pp), 99),
                      ("Turndown, 1st-percentile Cv", _M.operate(_X, _pp, Q=_M.TURNDOWN * _M.flow(_X)), 1)):
    _cv, _fp = _M.fp_iter(_o["Q"], _o["rho"], _o["dp_valve"], 38.1)
    _ok = _o["dp_valve"] > 0; _idx = _np.where(_ok)[0]
    _k = _idx[_np.argmin(_np.abs(_cv[_ok] - _np.percentile(_cv[_ok], _q)))]
    cases.append((_lab, float(_o["Q"][_k]), float(_o["rho"][_k] / 1000), float(_o["p1"][_k]), float(_o["dp_valve"][_k]),
                  float(_o["pv"][_k] / 1000), float(_fp[_k]), float(_M.flp(_cv[_k], 38.1) / _fp[_k])))
for i, (case, q, sg, p1, dp, pvv, fpv, flpfp) in enumerate(cases):
    r = 4 + i
    if i == 0:
        for j, v in enumerate(["FCV-101", "Reactor feed flow control", 2.0, 1.5, "Globe, equal %", 34.0, 50.0, 0.90, 41.0], 1):
            put(cs, r, j, v, "in")
    else:
        for j in range(1, 10): put(cs, r, j, f"={get_column_letter(j)}4", "calc")
    put(cs, r, 10, case, "in"); put(cs, r, 11, q, "in", "0.00"); put(cs, r, 12, sg, "in", "0.000"); put(cs, r, 13, p1, "in", "0.00")
    put(cs, r, 14, dp, "in", "0.00"); put(cs, r, 15, pvv, "in", "0.0"); put(cs, r, 16, fpv, "in", "0.000")
    put(cs, r, 17, f"=K{r}/(0.865*P{r})*SQRT(L{r}/N{r})", "calc", "0.00")
    put(cs, r, 18, f"=1+LN(Q{r}/F{r})/LN(G{r})", "calc", "0%")
    put(cs, r, 19, f"=0.96-0.28*SQRT(O{r}/100/I{r})", "calc", "0.000")
    put(cs, r, 20, f"=AB{r}^2*(M{r}-S{r}*O{r}/100)", "calc", "0.00"); put(cs, r, 28, flpfp, "in", "0.000")
    put(cs, r, 21, f'=IF(N{r}>=T{r},"Choked","No")', "calc")
    put(cs, r, 22, f"=N{r}/(M{r}-O{r}/100)", "calc", "0.00")
    put(cs, r, 23, 0.60, "in", "0.00")
    put(cs, r, 24, f'=IF(V{r}>=W{r},"Expect cavitation","No")', "calc")
    put(cs, r, 25, f'=IF(AND(R{r}>=0.1,R{r}<=0.9),"OK","Outside 10-90%")', "calc")
    put(cs, r, 26, "Sized for the P95 pump (Monte Carlo cases); valve upstream of E-101; Fp and FLP for 2-inch reducers" if i == 0 else f"=Z4", "in" if i == 0 else "calc")
    put(cs, r, 27, "H-03" if i == 0 else "=AA4", "in" if i == 0 else "calc")
cs["A8"] = "Fp and FLP/Fp: piping geometry factors for reducers, from the paper's model or the vendor's sizing program (FLP/Fp = FL with no reducers). Cv uses N1 = 0.865 (m3/h, bar). This valve is sized for the P95 pump; at P90 or P99 the model selects another valve (MC results)."
cs["A8"].font = Font(name=F, size=9, italic=True)

# ---------------- Other equipment ----------------
os_ = wb.create_sheet("Other equipment")
os_["A1"] = "Equipment list: vessels and exchangers"; os_["A1"].font = T
cols = ["Tag", "Service", "Type", "Key size (normal)", "Key size (rated)", "Unit", "Basis of rated size", "Operating P (barg)",
        "Design P (barg)", "Operating T (C)", "Design T (C)", "Material", "Holds", "Rev"]
header(os_, 3, cols, [10, 20, 16, 11, 11, 8, 34, 10, 10, 10, 10, 12, 10, 6])
rows = [("TK-101", "Feed tank", "Vertical, N2 blanket", 78.4, 80.0, "m3 working", "8 hours of normal feed (operating philosophy); level band 0.5-7.5 m", 0.035, 0.35, 20, 60, "CS", "H-05"),
        ("E-101", "Feed preheater", "Shell and tube, feed in tubes", 0.30, 0.45, "bar dp", "Tube-side dp at normal flow, clean to fouled x1.5", 7.0, "='Pumps'!S5", "5-40 inlet", 120, "CS", "H-01, H-04"),
        ("R-101", "Reactor", "Agitated vessel", 4.0, 4.45, "barg", "Operating pressure; +3 standard deviations of reactor pressure", 4.0, 7.0, 150, 180, "SS316L", "")]
for i, row in enumerate(rows):
    for j, v in enumerate(row, 1):
        put(os_, 4 + i, j, v, "link" if isinstance(v, str) and v.startswith("=") else "in")

# ---------------- Holds ----------------
hs = wb.create_sheet("Holds")
hs["A1"] = "Hold register"; hs["A1"].font = T
header(hs, 3, ["Hold", "What is open", "Affects", "Owner", "Needed by", "Status"], [8, 60, 18, 14, 12, 10])
holds = [("H-01", "Vendor pump curve: shutoff head, efficiency and NPSHr replace the generic curve", "P-101A/B, design pressure", "Process", "<date>", "Open"),
         ("H-02", "Electricity price for the life-cycle cost (C$0.09/kWh used)", "Pump and drive choice", "Owner", "<date>", "Open"),
         ("H-03", "Valve and VFD budget prices; vendor sizing of FCV-101", "FCV-101", "Instrument", "<date>", "Open"),
         ("H-04", "Piping route and fitting count from the 3D model (route length range 120-180 m used)", "P-101A/B rated head", "Piping", "<date>", "Open"),
         ("H-05", "Feed tank level band, working volume and relief set pressure from the operating philosophy", "TK-101, P-101 NPSH and design pressure", "Operations", "<date>", "Open")]
for i, row in enumerate(holds):
    for j, v in enumerate(row, 1): put(hs, 4 + i, j, v, "in")

# ---------------- Revision log ----------------
rs = wb.create_sheet("Revision log")
rs["A1"] = "Revision log"; rs["A1"].font = T
header(rs, 3, ["Rev", "Date", "What changed", "Model rerun?", "Rated points changed", "By"], [6, 12, 60, 12, 30, 10])
for j, v in enumerate(["A", "<date>", "Issued for design review; Monte Carlo P95 basis for P-101A/B and FCV-101", "Yes, 20,000 cases", "P-101A/B 10.68 m3/h at 82.5 m", "<initials>"], 1):
    put(rs, 4, j, v, "in")

# ================= Monte Carlo record: MC inputs, MC data, MC results (V4) =================
import json
import numpy as np
import pumpvalve_model as M
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.chart import BarChart, Reference
from openpyxl.worksheet.formula import ArrayFormula

NCASE, SEED, FIRST = 20000, 1, 6
LAST = FIRST + NCASE - 1
BORE, CV_RATED = 38.1, 34.0
R = json.load(open("results.json"))
SMALL = Font(name=F, size=9, italic=True)


def name(nm, sheet, cell):
    col = "".join(ch for ch in cell if ch.isalpha()); row = "".join(ch for ch in cell if ch.isdigit())
    wb.defined_names[nm] = DefinedName(nm, attr_text=f"'{sheet}'!${col}${row}")


# ---------- the simulation itself (identical to analyze.py: seed 1, 20,000 cases) ----------
X = M.sample(NCASE, seed=SEED)
S = M.system(X)
Qr95, Hr95, _ = M.rated_mc(X, 95)
p95 = M.Pump(Qr95, Hr95)
O = M.operate(X, p95)
CVQ, FPC = M.fp_iter(O["Q"], O["rho"], O["dp_valve"], BORE)
FP_RATED = float(M.Fp(CV_RATED, BORE))
WIDE = M.wide_open_dp(O["Q"], O["rho"], CV_RATED, BORE)

# ---------------- MC inputs ----------------
mi = wb.create_sheet("MC inputs", 2)
mi["A1"] = "Monte Carlo inputs: what was sampled, how, and every fixed parameter"; mi["A1"].font = T
mi["A2"] = ("Record of the run in 'MC data' (Python model pumpvalve_model.py V4, seed 1, 20,000 cases). The distributions are documentation: "
            "Excel cannot resample, so to change a range edit INPUTS in pumpvalve_model.py and rerun. Yellow cells further down feed live formulas.")
mi["A2"].font = SMALL
header(mi, 4, ["Key (model)", "Input", "Group", "Unit", "Distribution", "Min / mean", "Mode / sd", "Max", "Base case",
               "Stacked worst case", "Moderate case", "Basis of the range"], [11, 30, 16, 9, 22, 10, 10, 10, 10, 11, 11, 54])
DIST = {"tri": "Triangular (min, mode, max)", "uni": "Uniform (min, max)", "nor": "Normal (mean, sd)"}
META = {  # label, group, unit, display scale, moderate value, basis
    "rate": ("Production rate / design rate", "Operating variable", "-", 1, "110% of normal flow", "Operations: 85% to 110% of design, most often at design"),
    "recycle": ("Recycle / fresh feed", "Operating variable", "-", 1, 0.20, "Process: recycle ratio band from the heat and material balance"),
    "T": ("Feed temperature", "Operating variable", "deg C", 1, 5.0, "Outdoor tank, seasonal range; drives density, viscosity and vapour pressure"),
    "p_rx": ("Reactor pressure", "Operating variable", "barg", 1, 4.25, "Reactor control band around 4.0 barg"),
    "level": ("Liquid level above tank bottom", "Operating variable", "m", 1, 0.5, "Operating philosophy level band (low to high alarm)"),
    "blanket": ("Nitrogen blanket pressure", "Operating variable", "barg", 1, 0.02, "Blanket regulator band"),
    "L_dis": ("Discharge equivalent route length", "Design unknown", "m", 1, 160.0, "Plot plan estimate; fixed once the pipe is routed (hold H-04)"),
    "K_dis": ("Discharge fittings, sum of K", "Design unknown", "-", 1, 8.0, "Fitting count estimate; fixed once the pipe is routed (hold H-04)"),
    "eps": ("Pipe roughness", "Design unknown", "mm", 1000, 0.15, "New to aged carbon steel"),
    "foul": ("E-101 tube-side dp multiplier", "Design unknown", "-", 1, 1.5, "Clean to fouled, exchanger datasheet"),
    "strainer": ("Suction strainer clogging multiplier", "Design unknown", "-", 1, 5.0, "Clean to dirty strainer"),
}
r = 5
for k, (kind, a) in M.INPUTS.items():
    lab, grp, unit, sc, mod, basis = META[k]
    p = [v * sc for v in a] + [None] * (3 - len(a))
    if kind == "uni": p = [a[0] * sc, None, a[1] * sc]
    row = [k, lab, grp, unit, DIST[kind], p[0], p[1], p[2], M.BASE[k] * sc, M.WORST[k] * sc, mod, basis]
    for j, v in enumerate(row, 1):
        c = put(mi, r, j, v, "calc"); c.font = IN if j >= 6 and j <= 11 else CALC
        if isinstance(v, float): c.number_format = "0.000" if abs(v) < 1 else "0.00"
    r += 1
mi.cell(r, 1, "Stacked worst case: every input at its worst at once, flow 120% of normal, 10% on head. Moderate case: 110% of normal flow, the values shown, 0.7 bar for the valve and 10% on friction only.").font = SMALL

r += 2
mi.cell(r, 1, "Correlations (Gaussian copula)").font = B; r += 1
header(mi, r, ["Input A", "Input B", "Rank correlation (Spearman)", "Normal-score correlation 2 sin(pi r / 6)", "Basis"], [11, 30, 16, 9, 22])
mi.row_dimensions[r].height = 48
for (a, b), rho_s in M.CORR.items():
    r += 1
    put(mi, r, 1, a, "calc"); put(mi, r, 2, b, "calc"); put(mi, r, 3, rho_s, "calc", "0.00").font = IN
    put(mi, r, 4, f"=2*SIN(PI()*C{r}/6)", "calc", "0.000")
    put(mi, r, 5, "Higher rate runs at higher reactor pressure" if b == "p_rx" else "Higher rate runs with slightly more recycle", "calc")
r += 1
mi.cell(r, 1, "Temperature also sets density, viscosity and vapour pressure in every case (functional dependence, not sampled). All other pairs are independent.").font = SMALL

r += 2
mi.cell(r, 1, "Sampling").font = B; r += 1
for lab, v, note in [("Cases", NCASE, "Convergence: P95 rated head within +/-0.1 m at 20,000 cases (MC results)"),
                     ("Random seed", SEED, "numpy default_rng; rerun with the same seed reproduces 'MC data' exactly"),
                     ("Method", "Gaussian copula, inverse-CDF transform", "Correlated standard normals -> uniform -> each input's distribution")]:
    put(mi, r, 1, lab, "calc"); put(mi, r, 2, v, "calc").font = IN; put(mi, r, 3, note, "calc"); mi.merge_cells(start_row=r, start_column=3, end_row=r, end_column=12); r += 1

r += 1
mi.cell(r, 1, "Fixed parameters").font = B; r += 1
header(mi, r, ["Parameter", "Value", "Unit", "Note"], [11, 30, 16, 9]); mi.row_dimensions[r].height = 24
FIXED = [  # (label, value, unit, note, defined name or None, live-editable)
    ("Minimum control valve drop", M.DP_VALVE_MIN, "bar", "Control authority kept at each case's own flow; sets the head each case needs", "dpmin", True),
    ("Pump curve shutoff / rated head", M.Pump.SHUT, "-", "Generic curve H = Hr (S - (S-1)(Q/Qr)^2); replace with vendor curve (H-01)", "SHUT", True),
    ("FCV-101 rated Cv", CV_RATED, "Cv", "1.5-inch globe, equal percentage, selected trim", "CvR", True),
    ("FCV-101 inherent rangeability", M.R_EQ, "-", "Equal-percentage characteristic Cv/CvR = R^(x-1)", "Rng", True),
    ("FCV-101 body bore", BORE, "mm", "Used for the piping geometry factor", "Bore", True),
    ("Line bore at the valve", 52.5, "mm", "2-inch Sch 40", "Dpipe", True),
    ("Fp at rated Cv", "=(1+1.5*(1-(Bore/Dpipe)^2)^2/0.00214*(CvR/Bore^2)^2)^-0.5", "-", "IEC 60534-2-1, inlet and outlet reducers", "FpR", False),
    ("N1 (m3/h, bar)", M.N1, "-", "IEC 60534-2-1 numerical constant", "N1c", False),
    ("Gravity", M.G, "m/s2", "", "G_acc", False),
    ("Design product rate", M.PRODUCT_KGH, "kg/h", "50,000 t/y in 8,000 h (Chmltech design basis post)", None, False),
    ("Yield", M.YIELD, "kg/kg", "Product per kg fresh feed", None, False),
    ("Operating hours", M.HOURS, "h/y", "", None, False),
    ("Turndown", M.TURNDOWN, "-", "Plant must run at 50% of design rate", None, False),
    ("Tank bottom above pump", M.Z_TANK_BOTTOM, "m", "", None, False),
    ("Reactor nozzle above pump", M.Z_REACTOR, "m", "", None, False),
    ("Atmospheric pressure", M.P_ATM / 1e5, "bara", "", None, False),
    ("Suction line", "3-inch Sch 40, 77.9 mm bore, 12 m, sum K = 2", "", "Entrance, two elbows, gate valve", None, False),
    ("Discharge line", "2-inch Sch 40, 52.5 mm bore", "", "Length and K sampled (MC inputs above)", None, False),
    ("Friction", "Darcy-Weisbach, Colebrook friction factor", "", "Laminar 64/Re below Re 2,300", None, False),
    ("Density", "900 - 0.95 (T - 20)", "kg/m3", "Organic feed blend", None, False),
    ("Viscosity", "1.6 exp(-0.018 (T - 20))", "mPa s", "", None, False),
    ("Vapour pressure", "3.2 exp(0.046 (T - 20))", "kPa abs", "", None, False),
    ("Strainer dp", "0.02 x clogging x (Q/10)^2", "bar", "Q in m3/h", None, False),
    ("Coriolis meter dp", "0.15 x (Q/10)^2", "bar", "", None, False),
    ("E-101 tube-side dp", "0.30 x fouling x (Q/10)^1.8 x (mu/mu20)^0.2", "bar", "", None, False),
    ("Reactor nozzle and dip pipe dp", "0.20 x (Q/10)^2", "bar", "", None, False),
    ("Pump efficiency", "0.40 (2x - x^2), x = Q / (1.05 Qr)", "-", "Best efficiency 40% at 1.05 x rated flow (generic, nq ~ 6, H-01)", None, False),
    ("FCV-101 location", "Upstream of E-101", "", "Valve outlet pressure includes the E-101 drop; valve sees feed at tank temperature", None, False),
    ("NPSHr", "2.0 (0.5 + 0.5 x^2)", "m", "Generic, H-01", None, False),
    ("FCV-101 FL / xFz / pc", "0.90 / 0.60 / 41 bara", "", "xFz assumed trim value (IEC 60534-8-4)", None, False),
]
for lab, v, unit, note, nm, live in FIXED:
    r += 1
    put(mi, r, 1, lab, "calc")
    c = put(mi, r, 2, v, "in" if live else "calc")
    if not live and not (isinstance(v, str) and v.startswith("=")): c.font = IN
    if isinstance(v, float): c.number_format = "0.000" if v < 10 else "#,##0.0"
    if isinstance(v, str) and v.startswith("="): c.number_format = "0.0000"
    put(mi, r, 3, unit, "calc"); put(mi, r, 4, note, "calc")
    mi.merge_cells(start_row=r, start_column=4, end_row=r, end_column=12)
    if nm: name(nm, "MC inputs", f"B{r}")
mi.freeze_panes = "A5"

# ---------------- MC data ----------------
md = wb.create_sheet("MC data", 3)
md["A1"] = f"Monte Carlo data: all {NCASE:,} cases"; md["A1"].font = T
md["A2"] = ("Columns B-U (blue) are the Python model's sampled inputs and hydraulics for each case. Columns V-AG (black) are live formulas: "
            "the head each case needs, the rated head it implies, and the selected pump's valve pressure drop, flags, Cv and opening "
            "(pump chosen by the confidence level in 'MC summary'). Fp in AE is the model's iterated value for the P95 pump.")
md["A2"].font = SMALL
md["A3"] = "Group:"; md["A3"].font = B
for col, txt in [("B", "Sampled inputs"), ("M", "Fluid properties"), ("P", "Model hydraulics (valve excluded)"), ("V", "Rated-head requirement (live)"), ("Z", "Selected pump with FCV-101 as sized for P95 (live)")]:
    md[f"{col}3"] = txt; md[f"{col}3"].font = B
cols = ["Case", "Rate / design (-)", "Recycle / fresh (-)", "Feed T (deg C)", "Reactor p (barg)", "Tank level (m)", "N2 blanket (barg)",
        "Route length (m)", "Fittings sum K (-)", "Roughness (mm)", "E-101 fouling x (-)", "Strainer x (-)",
        "Density (kg/m3)", "Viscosity (mPa s)", "Vapour p (kPa abs)", "Demand flow (m3/h)", "Pump suction p (bara)",
        "Pressure needed at FCV outlet (bara)", "Discharge dynamic loss (bar)", "System head, no valve (m)", "NPSHa (m)",
        "Head needed incl. min valve drop (m)", "Rated head needed at P90 Qr (m)", "Rated head needed at P95 Qr (m)",
        "Rated head needed at P99 Qr (m)", "Pump head at case flow (m)", "Valve dp available (bar)", "Keeps min valve dp (1/0)",
        "Valve dp fully open (bar)", "Delivers flow (1/0)", "Fp (P95 pump)", "Cv required", "Valve opening (%)"]
header(md, 5, cols, [7] + [9] * 32)
md.row_dimensions[5].height = 60
arrs = [X["rate"], X["recycle"], X["T"], X["p_rx"], X["level"], X["blanket"], X["L_dis"], X["K_dis"], X["eps"] * 1000, X["foul"], X["strainer"],
        S["rho"], S["mu"] * 1000, S["pv"] / 1000, S["Q"], S["p_suc"] / 1e5, (S["p_end"] + S["dp_hx"]) / 1e5, S["dp_dis"] / 1e5, S["H_sys"], S["npsha"]]
fmts = ["0.000", "0.000", "0.0", "0.000", "0.00", "0.000", "0.0", "0.00", "0.000", "0.000", "0.00", "0.0", "0.000", "0.00", "0.000",
        "0.000", "0.000", "0.000", "0.00", "0.00"]
cols_np = np.column_stack(arrs)
f_in = IN
for i in range(NCASE):
    rr = FIRST + i
    md.cell(rr, 1, i + 1)
    for j in range(20):
        c = md.cell(rr, 2 + j, float(cols_np[i, j])); c.font = f_in; c.number_format = fmts[j]
    f = {
        22: (f"=T{rr}+dpmin*100000/(M{rr}*G_acc)", "0.00"),
        23: (f"=V{rr}/(SHUT-(SHUT-1)*(P{rr}/Qr_P90)^2)", "0.00"),
        24: (f"=V{rr}/(SHUT-(SHUT-1)*(P{rr}/Qr_P95)^2)", "0.00"),
        25: (f"=V{rr}/(SHUT-(SHUT-1)*(P{rr}/Qr_P99)^2)", "0.00"),
        26: (f"=Hr_sel*(SHUT-(SHUT-1)*(P{rr}/Qr_sel)^2)", "0.00"),
        27: (f"=(Z{rr}-T{rr})*M{rr}*G_acc/100000", "0.000"),
        28: (f"=IF(AA{rr}>=dpmin,1,0)", "0"),
        29: (f"=(P{rr}/(N1c*FpR*CvR))^2*M{rr}/1000", "0.000"),
        30: (f"=IF(AA{rr}>=AC{rr},1,0)", "0"),
        32: (f'=IF(AA{rr}>0,P{rr}/(N1c*AE{rr})*SQRT(M{rr}/1000/AA{rr}),"")', "0.00"),
        33: (f'=IF(AF{rr}="","",1+LN(AF{rr}/CvR)/LN(Rng))', "0.0%"),
    }
    for j, (fx, fm) in f.items():
        c = md.cell(rr, j, fx); c.number_format = fm
    c = md.cell(rr, 31, float(FPC[i])); c.font = f_in; c.number_format = "0.0000"
md.freeze_panes = "B6"


# ---------------- MC results ----------------
mr = wb.create_sheet("MC results", 4)
mr["A1"] = "Monte Carlo results"; mr["A1"].font = T
mr["A2"] = ("Column C recalculates from 'MC data'; column D is the Python model for the same 20,000 cases (P95 pump where a pump is involved). "
            "Change the confidence level in 'MC summary' or a yellow cell in 'MC inputs' and column C follows.")
mr["A2"].font = SMALL
header(mr, 4, ["Quantity", "Unit", "Excel (live)", "Python model", "Excel - Python", "Note"], [46, 9, 13, 13, 12, 60])
rng = lambda col: f"'MC data'!${col}${FIRST}:${col}${LAST}"
pct = lambda a, p: float(np.percentile(a, p))
op_py = M.opening(CVQ, CV_RATED); ok = O["dp_valve"] > 0
rows = [("Cases", "-", f"=COUNT({rng('P')})", NCASE, "N_cases", "#,##0", "")]
for p in (1, 5, 50, 90, 95, 99):
    rows.append((f"Demand flow P{p}", "m3/h", f"=PERCENTILE({rng('P')},{p/100})", pct(S["Q"], p), f"Q_P{p}", "0.00", "Normal flow at base inputs 9.80 m3/h" if p == 50 else ""))
for p in (1, 5, 50, 95, 99):
    rows.append((f"System head, no valve, P{p}", "m", f"=PERCENTILE({rng('T')},{p/100})", pct(S["H_sys"], p), None, "0.0", "Base case 67.3 m" if p == 50 else ""))
rows.append(("NPSHa minimum", "m", f"=MIN({rng('U')})", float(S["npsha"].min()), None, "0.0", "Low level, warm feed, dirty strainer"))
for p in (90, 95, 99):
    rows.append((f"Rated flow P{p}", "m3/h", f"=PERCENTILE({rng('P')},{p/100})", R[f"mc{p}"]["Qr"], f"Qr_P{p}", "0.00", "Rated flow = percentile of demand flow"))
for p in (90, 95, 99):
    rows.append((f"Rated head P{p}", "m", f"ARRAY:=PERCENTILE({rng('V')}/(SHUT-(SHUT-1)*({rng('P')}/Qr_P{p})^2),{p/100})", R[f"mc{p}"]["Hr"], f"Hr_P{p}", "0.0",
                 "Lowest rated head on the curve shape that keeps the minimum valve drop in this share of cases (array formula over MC data)"))
rows += [("Stacked worst-case rated point", "m3/h / m", None, f"{R['stacked']['Qr']:.2f} at {R['stacked']['Hr']:.1f}", None, None, "Deterministic, every input at its worst (MC inputs)"),
         ("Moderate deterministic rated point", "m3/h / m", None, f"{R['moderate']['Qr']:.2f} at {R['moderate']['Hr']:.1f}", None, None, "110% flow, moderate inputs, 10% on friction only")]
rows.append(("SELECTED PUMP (confidence level in 'MC summary'); valve rows are for FCV-101 as sized for P95 (1.5-inch, Cv 34)", None, None, None, None, None, None))
rows += [("Confidence level", "-", "='MC summary'!C4", "P95", None, None, "Python column always shows P95"),
         ("Rated flow", "m3/h", "='MC summary'!M4", Qr95, "Qr_sel", "0.00", ""),
         ("Rated head", "m", "='MC summary'!N4", Hr95, "Hr_sel", "0.0", ""),
         ("Shutoff head (generic curve)", "m", "=SHUT*Hr_sel", p95.shutoff(), None, "0.0", "Vendor curve replaces this (H-01)"),
         ("Share of cases keeping the minimum valve drop", "-", f"=AVERAGE({rng('AB')})", float(np.mean(O["dp_valve"] >= M.DP_VALVE_MIN)), None, "0.0%",
          "Averaged over operating states and design unknowns; as built 81% to 95% (below)"),
         ("Share of cases where the flow is delivered, valve fully open", "-", f"=AVERAGE({rng('AD')})", float(np.mean(O["dp_valve"] >= WIDE)), None, "0.00%", ""),
         ("Valve dp available P50", "bar", f"=PERCENTILE({rng('AA')},0.5)", pct(O["dp_valve"], 50), None, "0.00", ""),
         ("Valve dp available P99", "bar", f"=PERCENTILE({rng('AA')},0.99)", pct(O["dp_valve"], 99), None, "0.00", ""),
         ("Cv required P50", "Cv", f"=PERCENTILE({rng('AF')},0.5)", pct(CVQ[ok], 50), None, "0.00", "Cases with dp > 0"),
         ("Cv required P99", "Cv", f"=PERCENTILE({rng('AF')},0.99)", pct(CVQ[ok], 99), None, "0.00", "Both columns use the cases with dp > 0; the paper's Table 4 also counts the 0.04% with dp <= 0, so reads 18.4"),
         ("Valve opening P1", "%", f"=PERCENTILE({rng('AG')},0.01)", pct(op_py[ok], 1), None, "0.0%", "Equal percentage, rated Cv 34"),
         ("Valve opening P50", "%", f"=PERCENTILE({rng('AG')},0.5)", pct(op_py[ok], 50), None, "0.0%", ""),
         ("Valve opening P99", "%", f"=PERCENTILE({rng('AG')},0.99)", pct(op_py[ok], 99), None, "0.0%", ""),
         ("Share of cases above 85% open", "-", f'=COUNTIF({rng("AG")},">0.85")/COUNT({rng("AG")})', float(np.mean(op_py[ok] > 0.85)), None, "0.00%", ""),
         ("Share of cases above 90% open", "-", f'=COUNTIF({rng("AG")},">0.9")/COUNT({rng("AG")})', float(np.mean(op_py[ok] > 0.90)), None, "0.00%", "")]
r = 5
for lab, unit, fx, py, nm, fm, note in rows:
    if unit is None:
        r += 1; mr.cell(r, 1, lab).font = B; r += 1; continue
    put(mr, r, 1, lab, "calc"); put(mr, r, 2, unit, "calc")
    if fx and fx.startswith("ARRAY:"):
        c = put(mr, r, 3, None, "calc", fm); mr[f"C{r}"] = ArrayFormula(f"C{r}", fx[6:])
    elif fx: c = put(mr, r, 3, fx, "link" if "MC summary" in fx else "calc", fm)
    else: put(mr, r, 3, "", "calc")
    c = put(mr, r, 4, py, "calc", fm); c.font = IN
    if fx and not isinstance(py, str): put(mr, r, 5, f"=IF(ISNUMBER(C{r}),C{r}-D{r},\"\")", "calc", fm)
    else: put(mr, r, 5, "", "calc")
    put(mr, r, 6, note, "calc")
    if nm: name(nm, "MC results", f"C{r}")
    r += 1

# --- histogram of the head each case needs ---
r += 1; mr.cell(r, 1, "Distribution of the head each case needs (incl. minimum valve drop), live").font = B; r += 1
header(mr, r, ["Bin upper edge (m)", "", "Cases", "Share"], [46, 9, 13, 13]); mr.row_dimensions[r].height = 24
h0 = r + 1; edges = np.arange(64, 96, 1.0)
for i, e in enumerate(edges):
    rr = h0 + i
    put(mr, rr, 1, float(e), "calc", "0")
    lo = f"A{rr-1}" if i else "-1E9"
    put(mr, rr, 3, f'=COUNTIFS({rng("V")},">"&{lo},{rng("V")},"<="&A{rr})', "calc", "#,##0")
    put(mr, rr, 4, f"=C{rr}/N_cases", "calc", "0.0%")
h1 = h0 + len(edges) - 1
ch = BarChart(); ch.type = "col"; ch.title = "Head needed per case (m)"; ch.y_axis.title = "Cases"; ch.x_axis.title = "Head needed, bin upper edge (m)"
ch.add_data(Reference(mr, min_col=3, min_row=h0 - 1, max_row=h1), titles_from_data=True)
ch.set_categories(Reference(mr, min_col=1, min_row=h0, max_row=h1)); ch.gapWidth = 10; ch.legend = None
ch.roundedCorners = False; ch.x_axis.delete = False; ch.y_axis.delete = False
for t in (ch.title, ch.x_axis.title, ch.y_axis.title): t.overlay = False
ch.width, ch.height = 22, 9
mr.add_chart(ch, f"H{h0}")
r = h1 + 2

# --- model results Excel cannot rerun ---
mr.cell(r, 1, "MODEL RESULTS NOT RECALCULATED IN EXCEL (Python model, analyze.py)").font = B; r += 1
mr.cell(r, 1, "These need the pump and valve selection loop, VFD speed solution, repeated sampling or resampling, which Excel cannot do. Values are the paper's.").font = SMALL; r += 2
D = R["designs"]
header(mr, r, ["Design", "Rated flow (m3/h)", "Rated head (m)", "Shutoff (m)", "Motor (kW)", "Design pressure (barg)",
               "Mean electric power (kW)", "Energy (C$/y)", "Purchased cost (C$)", "Life-cycle cost, 20 y (C$)", "Valve selected"], [46, 13, 13, 13, 12, 60])
mr.column_dimensions["K"].width = 22
for j, w in zip(range(7, 11), [13, 13, 14, 15]): mr.column_dimensions[get_column_letter(j)].width = w
lab = {"stacked": "Stacked margins, throttled", "mc90": "Monte Carlo P90, throttled", "mc95": "Monte Carlo P95, throttled",
       "mc99": "Monte Carlo P99, throttled", "stacked_vfd": "Stacked margins, VFD", "mc95_vfd": "Monte Carlo P95, VFD", "moderate": "Moderate margins, throttled"}
for k in ("stacked", "moderate", "mc90", "mc95", "mc99", "stacked_vfd", "mc95_vfd"):
    r += 1; d = D[k]
    vv = d.get("valve"); c = put(mr, r, 11, f"{vv['size']:g}-inch, Cv {vv['cv']:g}" if vv else "None (drive)", "calc"); c.font = IN
    for j, (v, fm) in enumerate([(lab[k], None), (d["Qr"], "0.00"), (d["Hr"], "0.0"), (d["shutoff"], "0.0"), (d["motor"], "0.0"), (d["p_design"], "0.0"),
                                 (d["P_el_mean"], "0.00"), (d["energy_cy"], "#,##0"), (d["capex_total"], "#,##0"), (d["lcc"], "#,##0")], 1):
        c = put(mr, r, j, v, "calc", fm); c.font = IN if j > 1 else CALC
r += 2
header(mr, r, ["Coverage of the P95 pump once the design unknowns are fixed", "", "Keeps min valve dp", "Cannot deliver"], [46, 9, 13, 13])
covlab = {"all_random": "Design unknowns random (as simulated)", "unknowns_at_P95": "All five design unknowns at their P95",
          "route_fittings_roughness_max": "Route, fittings and roughness at maximum", "all_unknowns_max": "All five design unknowns at maximum",
          "all_unknowns_min": "All five design unknowns at minimum", "unknowns_at_P5": "All five design unknowns at their P5",
          "existing_P95_pump_measured_route": "Operating plant: route, fittings, roughness measured (at P95), fouling and clogging random"}
for k, t in covlab.items():
    r += 1; put(mr, r, 1, t, "calc"); put(mr, r, 2, "", "calc")
    for j, v in ((3, R["coverage"][k][0]), (4, R["coverage"][k][1])): c = put(mr, r, j, v, "calc", "0.0%"); c.font = IN
o4 = R["coverage"]["over_400_draws"]; r += 1
put(mr, r, 1, "400 random draws of the design unknowns: mean / 5th pct / 95th pct / min / max", "calc"); put(mr, r, 2, "", "calc")
c = put(mr, r, 3, f"{o4['mean']:.1%} / {o4['p5']:.1%} / {o4['p95']:.1%} / {o4['min']:.1%} / {o4['max']:.1%}", "calc"); c.font = IN
rr_ = R["coverage"]["rerated_measured_route"]; r += 1
put(mr, r, 1, "Operating plant, pump re-rated with the measured route: rated point / coverage", "calc"); put(mr, r, 2, "", "calc")
c = put(mr, r, 3, f"{rr_['Qr']:.2f} m3/h at {rr_['Hr']:.1f} m / {rr_['coverage'][0]:.1%}", "calc"); c.font = IN
e55 = R["eff55"]; r += 1
put(mr, r, 1, "Efficiency sensitivity, 55% best efficiency: motor kW (stacked / moderate / P95)", "calc"); put(mr, r, 2, "", "calc")
c = put(mr, r, 3, f"{e55['stacked']['motor']:g} / {e55['moderate']['motor']:g} / {e55['mc95']['motor']:g}", "calc"); c.font = IN
r += 2
header(mr, r, ["Sensitivity: input (P5 and P95, others at base)", "P5 value", "P95 value", "Head at P5 (m)", "Head at P95 (m)", "Swing (m)", "Spearman with head"],
       [46, 9, 13, 13, 12, 60])
for t in R["tornado"]:
    r += 1; sc = 1000 if t["name"] == "eps" else 1
    vals = [(f"{META[t['name']][0]} ({t['name']})", None), (t["lo"] * sc, "0.000"), (t["hi"] * sc, "0.000"), (t["h_lo"], "0.0"), (t["h_hi"], "0.0"),
            (abs(t["h_hi"] - t["h_lo"]), "0.0"), (t["spearman"], "0.00")]
    for j, (v, fm) in enumerate(vals, 1):
        c = put(mr, r, j, v, "calc", fm); c.font = IN if j > 1 else CALC
r += 1; mr.cell(r, 1, f"Base case head needed incl. minimum valve drop: {R['tornado_base']:.1f} m").font = SMALL
r += 2
header(mr, r, ["Convergence of the P95 rated head (200 repeats per size)", "Cases", "Mean (m)", "2.5th pct (m)", "97.5th pct (m)", "Half-width (m)"], [46, 9, 13, 13, 12, 60])
for cv in R["convergence"]:
    r += 1; put(mr, r, 1, "", "calc")
    for j, (v, fm) in enumerate([(cv["n"], "#,##0"), (cv["mean"], "0.00"), (cv["lo"], "0.00"), (cv["hi"], "0.00"), ((cv["hi"] - cv["lo"]) / 2, "0.00")], 2):
        c = put(mr, r, j, v, "calc", fm); c.font = IN
r += 2
mr.cell(r, 1, "Other model results").font = B
other = [("Moderate deterministic rated point: flow", R["moderate"]["Qr"], "m3/h", "0.00"), ("Moderate deterministic rated point: head (most likely route 140 m)", R["moderate"]["Hr"], "m", "0.0"),
         ("P95 rated head with the correlations removed", R["mc95_independent"], "m", "0.0"),
         ("P95 rated head, route length 100-300 m, most likely 160 m", R["route_sensitivity"]["100-160-300"]["P95"], "m", "0.0"),
         ("P95 rated head, route length 120-400 m, most likely 200 m", R["route_sensitivity"]["120-200-400"]["P95"], "m", "0.0"),
         ("Stacked worst-case flow the P95 pump can deliver, valve fully open", R["upset"]["Qmax_P95_valve_open"], "m3/h", "0.00"),
         ("Same with the 5% larger impeller", R["upset"]["Qmax_P95_bigger_impeller_valve_open"], "m3/h", "0.00"),
         ("Worst-case demand flow", R["upset"]["Q_worst"], "m3/h", "0.00")]
for t, v, u, fm in other:
    r += 1; put(mr, r, 1, t, "calc"); put(mr, r, 2, u, "calc"); c = put(mr, r, 4, v, "calc", fm); c.font = IN
mr.freeze_panes = "A5"


out = os.environ.get("TEMPLATE_OUT", "chmltech-equipment-list-template.xlsx")
wb.save(out); print(out)
