"""Builds Preheater_Fouling_Sizing_Template_V1.xlsx: live design-area and shell-pressure calculator for a
steam-heated feed preheater (Eqs. 1-3 of the paper), fouling curve, and the stored Monte Carlo results."""
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL

R = json.load(open("/home/claude/hx/hx_results.json")); X = json.load(open("/home/claude/hx/hx_extras.json"))
AR = Font(name="Arial", size=10); B = Font(name="Arial", size=10, bold=True); BL = Font(name="Arial", size=10, color="0000FF")
GR = Font(name="Arial", size=10, color="008000"); T1 = Font(name="Arial", size=14, bold=True); IT = Font(name="Arial", size=9, italic=True)
HDR = PatternFill("solid", fgColor="1F3864"); HF = Font(name="Arial", size=10, bold=True, color="FFFFFF")
YEL = PatternFill("solid", fgColor="FFFF00"); GRY = PatternFill("solid", fgColor="F2F2F2"); OK = PatternFill("solid", fgColor="E2EFDA")
RED = PatternFill("solid", fgColor="F8CBAD")
thin = Side(style="thin", color="BFBFBF"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
wb = Workbook()
def sheet(name, first=False):
    ws = wb.active if first else wb.create_sheet(name); ws.title = name; ws.sheet_view.showGridLines = False; return ws
def hdr(ws, row, labels, col=1, h=42):
    for i, t in enumerate(labels):
        c = ws.cell(row, col + i, t); c.font = HF; c.fill = HDR; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = BOX
    ws.row_dimensions[row].height = h
def put(ws, ref, v, font=AR, fmt=None, fill=None, box=False):
    c = ws[ref]; c.value = v; c.font = font
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if box: c.border = BOX
    return c

ws = sheet("README", True); ws.column_dimensions["A"].width = 22; ws.column_dimensions["B"].width = 105
put(ws, "A1", "Feed Preheater Sizing Under Fouling - Template V1", T1)
rows = [
 ("Paper", "Sizing the Feed Preheater Under Fouling Uncertainty: Area Margin, Cleaning and Condensate Stall (Chmltech Online Journal, Vol. 106). Author: Quak Foo Lee, Chmltech Ltd., Vancouver, BC."),
 ("What it does", "For a steam-heated shell-and-tube preheater with steam-side control, it computes live: the tube-side coefficient (Gnielinski), the overall coefficient (Eq. 1), the clean and TEMA design areas at a design case, and, for each candidate area, the shell pressure needed (Eq. 2) clean and at three fouling levels (Eq. 3 asymptote), at normal rate and at turndown. Cells turn red where the steam runs out (rate cut) and orange where the shell is below the condensate back pressure (stall)."),
 ("Live parts", "Inputs, Calculator and Fouling_Curve are formulas. Change the feed, steam, tubes or fouling levels and every result updates."),
 ("Not live", "MC_Results holds the paper's Monte Carlo output (500 fouling scenarios x 300 operating cases x 24 months with clean-on-demand): cleanings, costs, chance of a rate cut and stall shares by area. Rerun hx_model.py to change it."),
 ("Sheet guide", "Inputs.  Calculator: design areas and the area-by-case pressure grid.  Fouling_Curve: Kern-Seaton resistance over a run at P10/P50/P90 levels.  MC_Results.  Changelog."),
 ("Legend", "Blue text = input. Yellow fill = key assumption to replace with plant data. Black = formula. Grey fill = stored model output. Red fill = rate cut. Orange fill = stall."),
 ("Example", "Inputs come filled with E-101 of the paper (8,690 kg/h median feed, 3.0 barg steam, 3/4 in tubes, 12 per pass)."),
 ("Limits", "Turbulent tube-side flow assumed in the grid (laminar correction not applied; check Re > 2,300 shown). Uniform condensing temperature in the shell; stall judged against the condensate back pressure entered. Steam properties from an Antoine fit valid 100-180 C; shell pressures below 0 barg are extrapolated."),
]
for i, (k, v) in enumerate(rows, start=3):
    put(ws, f"A{i}", k, B).alignment = WRAP; c = put(ws, f"B{i}", v); c.alignment = WRAP
    ws.row_dimensions[i].height = max(15, 14 * (len(v) // 100 + 1))

wi = sheet("Inputs")
for col, w in zip("ABCD", (46, 14, 12, 56)): wi.column_dimensions[col].width = w
put(wi, "A1", "Inputs", T1); hdr(wi, 3, ["Input", "Value", "Unit", "Basis"], h=20)
inp = [("Feed rate, normal (median)", 8690, "kg/h", "Issue 8 cases", "#,##0", True),      # B4
       ("Feed rate, design case (P95)", 9569, "kg/h", "Issue 8 cases", "#,##0", True),      # B5
       ("Turndown fraction of normal rate", 0.5, "-", "Plant must run at 50%", "0%", False),  # B6
       ("Feed inlet temperature, median", 22.5, "C", "Outdoor tank", "0.0", False),           # B7
       ("Feed inlet temperature, design case (P5)", 6.8, "C", "Winter", "0.0", True),         # B8
       ("Outlet temperature", 80, "C", "Design basis", "0.0", False),                          # B9
       ("Feed cp", 2000, "J/kg.K", "Fluid model", "#,##0", False),                             # B10
       ("Feed thermal conductivity", 0.13, "W/m.K", "Fluid model", "0.000", False),            # B11
       ("Feed density at 20 C (falls 0.95 kg/m3 per K)", 900.0, "kg/m3", "Fluid model", "0.0", False),   # B12
       ("Feed viscosity at 20 C (x exp(-0.018(T-20)))", 0.0016, "Pa.s", "Fluid model", "0.000000", False),  # B13
       ("Tube OD", 0.01905, "m", "3/4 in", "0.00000", False),                                  # B14
       ("Tube ID", 0.01575, "m", "16 BWG", "0.00000", False),                                  # B15
       ("Tubes per pass", 12, "-", "About 1.2 m/s at median flow", "0", True),                 # B16
       ("Tube wall conductivity", 45, "W/m.K", "Carbon steel", "0", False),                    # B17
       ("Condensing coefficient", 8000, "W/m2.K", "Most likely", "#,##0", False),              # B18
       ("Steam-side fouling resistance", 0.0001, "m2K/W", "Held fixed", "0.00000", False),     # B19
       ("Steam header pressure", 3.0, "barg", "Design basis", "0.00", False),                  # B20
       ("Pressure drop across the steam control valve", 0.3, "bar", "At full opening", "0.00", True),  # B21
       ("Condensate back pressure at the trap outlet", 0.0, "barg", "Atmospheric return", "0.00", True),   # B22
       ("Tube-side fouling, P10 level at 24 months (used as asymptote)", 0.00021, "m2K/W", "Paper scenarios (P10 at 24 months)", "0.00000", True),  # B23
       ("Tube-side fouling, P50 level at 24 months (used as asymptote)", 0.00037, "m2K/W", "Paper scenarios (median at 24 months)", "0.00000", True),  # B24
       ("Tube-side fouling, P90 level at 24 months (used as asymptote)", 0.0006, "m2K/W", "Paper scenarios (P90 at 24 months)", "0.00000", True),   # B25
       ("TEMA tube-side fouling (design)", 0.000176, "m2K/W", "TEMA, organic process liquid", "0.00000", False),     # B26
       ("TEMA shell-side fouling (design)", 0.000088, "m2K/W", "TEMA, steam", "0.00000", False),                       # B27
       ("Fouling time constant", 3000, "h", "Most likely", "#,##0", False)]                    # B28
for i, (k, v, u, b, f, y) in enumerate(inp, start=4):
    put(wi, f"A{i}", k, box=True); put(wi, f"B{i}", v, BL, f, YEL if y else None, True); put(wi, f"C{i}", u, box=True); put(wi, f"D{i}", b, box=True)

wc = sheet("Calculator")
for col, w in zip("ABCDEFGHIJKLMN", (40, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12)): wc.column_dimensions[col].width = w
put(wc, "A1", "Calculator (Eqs. 1-3)", T1)
I = lambda r: f"Inputs!$B${r}"
put(wc, "A3", "Steam and wall", B)
calc = [("Highest shell temperature, Ts,max (C)", f"=1810.94/(8.14019-LOG10(({I(20)}-{I(21)}+1.01325)*750.062))-244.485", "0.0"),   # B4
        ("Stall temperature at back pressure (C)", f"=1810.94/(8.14019-LOG10(({I(22)}+1.01325)*750.062))-244.485", "0.0"),           # B5
        ("Wall resistance on OD (m2K/W)", f"={I(14)}*LN({I(14)}/{I(15)})/(2*{I(17)})", "0.000000"),                                    # B6
        ("(Properties are evaluated at each case mean temperature below)", None, None)]                                                                       # B7
for i, (k, f, fm) in enumerate(calc, start=4):
    put(wc, f"A{i}", k, box=True); put(wc, f"B{i}", f, AR, fm, box=True)
put(wc, "A9", "Tube side (Gnielinski) at each flow", B)
hdr(wc, 10, ["Case", "Flow (kg/h)", "Velocity (m/s)", "Re", "Friction f", "Nu", "hi (W/m2K)", "U clean (W/m2K)", "Mean T (C)", "Density", "Viscosity (Pa.s)", "Pr"], h=30)
cases = [("Normal rate", f"={I(4)}"), ("Design case", f"={I(5)}"), ("Turndown", f"={I(4)}*{I(6)}")]
for k, (lab, fl) in enumerate(cases):
    r = 11 + k
    put(wc, f"A{r}", lab, box=True); put(wc, f"B{r}", fl, GR, "#,##0", box=True)
    tin_ = I(8) if k == 1 else I(7)
    put(wc, f"I{r}", f"=({tin_}+{I(9)})/2", AR, "0.0", box=True)
    put(wc, f"J{r}", f"={I(12)}-0.95*(I{r}-20)", AR, "0.0", box=True)
    put(wc, f"K{r}", f"={I(13)}*EXP(-0.018*(I{r}-20))", AR, "0.000000", box=True)
    put(wc, f"L{r}", f"={I(10)}*K{r}/{I(11)}", AR, "0.00", box=True)
    put(wc, f"C{r}", f"=B{r}/3600/J{r}/({I(16)}*PI()*{I(15)}^2/4)", AR, "0.00", box=True)
    put(wc, f"D{r}", f"=J{r}*C{r}*{I(15)}/K{r}", AR, "#,##0", box=True)
    put(wc, f"E{r}", f"=(0.79*LN(D{r})-1.64)^-2", AR, "0.0000", box=True)
    put(wc, f"F{r}", f"=(E{r}/8)*(D{r}-1000)*L{r}/(1+12.7*SQRT(E{r}/8)*(L{r}^(2/3)-1))", AR, "0.0", box=True)
    put(wc, f"G{r}", f"=F{r}*{I(11)}/{I(15)}", AR, "#,##0", box=True)
    put(wc, f"H{r}", f"=1/({I(14)}/(G{r}*{I(15)})+$B$6+1/{I(18)}+{I(19)})", AR, "#,##0", box=True)
put(wc, "A15", "Design areas at the design case (flow row 12, inlet B8, shell at Ts,max)", B)
put(wc, "A16", "Clean area, no fouling either side (m2)", box=True)
put(wc, "B16", f"={I(5)}/3600*{I(10)}*(1/H12-{I(19)})*LN(($B$4-{I(8)})/($B$4-{I(9)}))", AR, "0.00", OK, True)
put(wc, "A17", "U with TEMA fouling (W/m2K)", box=True)
put(wc, "B17", f"=1/(1/H12+{I(26)}*{I(14)}/{I(15)}+{I(27)}-{I(19)})", AR, "#,##0", box=True)
put(wc, "A18", "TEMA area (m2)", box=True)
put(wc, "B18", f"={I(5)}/3600*{I(10)}/B17*LN(($B$4-{I(8)})/($B$4-{I(9)}))", AR, "0.00", OK, True)
put(wc, "A19", "TEMA + 20% (m2)", box=True); put(wc, "B19", "=1.2*B18", AR, "0.00", box=True)
put(wc, "C17", "TEMA replaces the steam-side fouling held on Inputs with the TEMA value.", IT)

put(wc, "A21", "Shell pressure needed (barg), median inlet temperature; red = steam runs out (rate cut), orange = below back pressure (stall)", B)
areas = [4, 5, 6, 7, 8, 9, 10, 12]
hdr(wc, 22, ["Case \\ area (m2)"] + areas, h=30)
for j, a in enumerate(areas):
    c = wc.cell(22, 2 + j, a); c.font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
grid = [("Normal, clean", 11, None), ("Normal, P10 fouling", 11, 23), ("Normal, P50 fouling", 11, 24), ("Normal, P90 fouling", 11, 25),
        ("Turndown, clean", 13, None), ("Turndown, P10 fouling", 13, 23), ("Turndown, P50 fouling", 13, 24), ("Turndown, P90 fouling", 13, 25),
        ("Design case, P90 fouling", 12, 25)]
from openpyxl.formatting.rule import FormulaRule
for k, (lab, fr, rf) in enumerate(grid):
    r = 23 + k; put(wc, f"A{r}", lab, box=True)
    tin = I(8) if fr == 12 else I(7)
    for j in range(len(areas)):
        col = CL(2 + j)
        U = f"$H${fr}" if rf is None else f"(1/(1/$H${fr}+{I(rf)}*{I(14)}/{I(15)}))"
        ntu = f"({U}*{col}$22/($B${fr}/3600*{I(10)}))"
        ts = f"(({I(9)}-{tin}*EXP(-{ntu}))/(1-EXP(-{ntu})))"
        f = f"=10^(8.14019-1810.94/({ts}+244.485))/750.062-1.01325"
        c = wc.cell(r, 2 + j, f); c.font = AR; c.number_format = "0.00"; c.border = BOX
rng = f"B23:{CL(1 + len(areas))}31"
wc.conditional_formatting.add(rng, FormulaRule(formula=[f"B23>Inputs!$B$20-Inputs!$B$21"], fill=RED))
wc.conditional_formatting.add(rng, FormulaRule(formula=[f"B23<Inputs!$B$22"], fill=PatternFill("solid", fgColor="FFC000")))
put(wc, "A33", "Read across a row: an area is safe from rate cuts if the fouled rows stay white, and safe from stall if the clean and turndown rows stay white. In most cases no area is both: size for fouling and design the condensate system for stall (paper, Section 7).", IT)

wf = sheet("Fouling_Curve")
put(wf, "A1", "Kern-Seaton fouling over a run: Rf(t) = Rinf (1 - exp(-t/tau))", T1)
hdr(wf, 3, ["Months", "Hours", "P10 level (m2K/W)", "P50 level", "P90 level", "TEMA value"], h=30)
for i in range(25):
    r = 4 + i
    put(wf, f"A{r}", i, AR, "0", box=True); put(wf, f"B{r}", f"=A{r}*8000/12", AR, "#,##0", box=True)
    for j, ir in enumerate((23, 24, 25)):
        put(wf, f"{CL(3 + j)}{r}", f"={I(ir)}*(1-EXP(-B{r}/{I(28)}))", AR, "0.000000", box=True)
    put(wf, f"F{r}", f"={I(26)}", GR, "0.000000", box=True)
for col in "ABCDEF": wf.column_dimensions[col].width = 16
from openpyxl.chart import LineChart, Reference
ch = LineChart(); ch.title = "Tube-side fouling resistance over a run"; ch.y_axis.title = "m2K/W"; ch.x_axis.title = "Months"
ch.add_data(Reference(wf, min_col=3, max_col=6, min_row=3, max_row=28), titles_from_data=True)
ch.set_categories(Reference(wf, min_col=1, min_row=4, max_row=28))
ch.roundedCorners = False; ch.legend.position = "b"; ch.legend.overlay = False; ch.title.overlay = False
ch.x_axis.title.overlay = False; ch.y_axis.title.overlay = False; ch.x_axis.delete = False; ch.y_axis.delete = False
ch.width = 18; ch.height = 9; wf.add_chart(ch, "H3")

wm = sheet("MC_Results")
put(wm, "A1", "Stored Monte Carlo results of the paper (values): 500 scenarios, 24-month run, clean on demand", T1)
hdr(wm, 3, ["Area (m2)", "Tubes", "Passes", "Tube length (m)", "Installed cost (C$)", "Unplanned cleanings a year", "Chance of a rate cut in the run",
            "Mean total annual cost (C$)", "P95 total annual cost (C$)", "Stall share, normal hours", "Stall share, turndown hours"], h=56)
rows_ = [(a, R["by_area"][str(a)]) for a in R["areas"]]
for k, (a, d) in enumerate(rows_):
    r = 4 + k
    vals = [a, d["tubes"], d["passes"], d["L"], d["cost"], d["cleans_y"], d["p_cut_in_run"], d["total"], d["total_p95"], d["stallN"], d["stallT"]]
    fm = ["0", "0", "0", "0.00", "#,##0", "0.000", "0.0%", "#,##0", "#,##0", "0.0%", "0.0%"]
    for j, (v, f) in enumerate(zip(vals, fm)):
        c = wm.cell(r, 1 + j, v); c.font = AR; c.border = BOX; c.fill = GRY; c.number_format = f
for i in range(1, 12): wm.column_dimensions[CL(i)].width = 14
r0 = 6 + len(rows_)
put(wm, f"A{r0}", "Sensitivity (paper, Section 6)", B)
hdr(wm, r0 + 1, ["Area (m2)", "Linear fouling: cleanings/y", "Linear: chance of cut", "Linear: mean cost (C$)", "12-month run: cleanings/y", "12-month: chance of cut", "12-month: mean cost (C$)"], h=42)
for k, a in enumerate(["6", "7", "8", "9", "10"]):
    r = r0 + 2 + k; lin = X["linear"][a]; r12 = X["run12"][a]
    for j, (v, f) in enumerate(zip([int(a), lin["cleans_y"], lin["p_cut"], lin["total"], r12["cleans_y"], r12["p_cut"], r12["total"]],
                                   ["0", "0.000", "0%", "#,##0", "0.000", "0%", "#,##0"])):
        c = wm.cell(r, 1 + j, v); c.font = AR; c.border = BOX; c.fill = GRY; c.number_format = f

wl = sheet("Changelog"); wl.column_dimensions["A"].width = 10; wl.column_dimensions["B"].width = 14; wl.column_dimensions["C"].width = 100
hdr(wl, 1, ["Version", "Date", "Change"], h=20)
for j, v in enumerate(["V1", "2026-11-27", "First release with the journal paper: live design-area and shell-pressure calculator with rate-cut and stall flags, fouling curve, stored Monte Carlo and sensitivity results."]):
    c = wl.cell(2, 1 + j, v); c.font = AR; c.alignment = WRAP
out = "/mnt/user-data/outputs/Preheater_Fouling_Sizing_Template_V1.xlsx"; wb.save(out); print(out)
