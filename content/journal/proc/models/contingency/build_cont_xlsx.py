"""Builds Cost_Contingency_Monte_Carlo_Template_V1.xlsx: a live Monte Carlo (RAND formulas, common-factor
correlation) of the C$100M Class 3 estimate, with results, S-curve and the stored 50,000-iteration model output."""
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.chart import ScatterChart, Reference, Series

import contingency_model as M
R = json.load(open("/home/claude/cont/contingency_results.json"))
NIT = 5000

AR = Font(name="Arial", size=10); B = Font(name="Arial", size=10, bold=True); BL = Font(name="Arial", size=10, color="0000FF")
GR = Font(name="Arial", size=10, color="008000"); T1 = Font(name="Arial", size=14, bold=True); IT = Font(name="Arial", size=9, italic=True)
HDR = PatternFill("solid", fgColor="1F3864"); HF = Font(name="Arial", size=10, bold=True, color="FFFFFF")
YEL = PatternFill("solid", fgColor="FFFF00"); GRY = PatternFill("solid", fgColor="F2F2F2"); OK = PatternFill("solid", fgColor="E2EFDA")
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

# ---------------- README ----------------
ws = sheet("README", True); ws.column_dimensions["A"].width = 22; ws.column_dimensions["B"].width = 105
put(ws, "A1", "Cost Contingency by Monte Carlo - Template V1", T1)
rows = [
 ("Paper", "Setting Cost Contingency by Monte Carlo: P50, P80 and the Risks Behind Them for a C$100 Million Process Plant (Chmltech Online Journal, Vol. 106). Author: Quak Foo Lee, Chmltech Ltd., Vancouver, BC."),
 ("What it does", f"Runs the paper's Monte Carlo live in Excel with {NIT:,} iterations: 12 cost accounts with triangular ranges, correlated through common drivers; an 8-event risk register with cost and delay; and a separate escalation and exchange-rate reserve. Results gives the P50, P80 and P90 cost and contingency, the chance of overrunning a flat percentage, the escalation reserve and an S-curve."),
 ("Live parts", "Everything. Inputs feed the Simulation sheet through RAND() formulas. Press F9 (or edit any input) to draw a new set of iterations; percentiles move by about C$0.2M between draws at 5,000 iterations. For a quieter answer, copy the Simulation rows down (the Results ranges use whole columns up to row 20,001)."),
 ("Correlation", "Each account's normal score is z = sqrt(rho_between) Z0 + sqrt(rho_group - rho_between) Zg + sqrt(1 - rho_group) e, where Z0 is common to all accounts, Zg to its group and e its own. This reproduces the paper's correlation matrix exactly (0.5 materials and engineering, 0.7 labour, 0.3 between groups) and needs rho_group >= rho_between."),
 ("Sheet guide", "Inputs: accounts, ranges, correlation, risk register, escalation.  Simulation: one row per iteration (formulas).  Results: percentiles, contingency, overrun chances, checks, S-curve chart.  Model_Results: the paper's 50,000-iteration Python results for comparison (values).  Changelog."),
 ("Legend", "Blue text = input you may change. Yellow fill = key assumption to replace with project data. Black = formula. Green = link to another sheet. Grey fill = stored model output (values)."),
 ("Example", "Inputs come filled with the paper's C$100M Class 3 estimate and risk register."),
 ("Units", "C$ million at base-date prices; delays in weeks; escalation in % a year."),
 ("Limits", "Line-item ranging tends to understate the spread of real outcomes; systemic risks (new technology, weak definition) are not modelled parametrically. Risk events are independent of each other and of the line items. Calculation is volatile: large copies slow Excel; switch to manual calculation (Formulas > Calculation Options) if needed."),
]
for i, (k, v) in enumerate(rows, start=3):
    put(ws, f"A{i}", k, B).alignment = WRAP; c = put(ws, f"B{i}", v); c.alignment = WRAP
    ws.row_dimensions[i].height = max(15, 14 * (len(v) // 100 + 1))

# ---------------- Inputs ----------------
wi = sheet("Inputs")
for col, w in zip("ABCDEFGHI", (40, 11, 11, 11, 11, 14, 12, 12, 44)): wi.column_dimensions[col].width = w
put(wi, "A1", "Inputs (C$ million, base-date prices)", T1)
hdr(wi, 3, ["Account", "Base (C$M)", "Low multiple", "Most likely", "High multiple", "Correlation group", "Mean multiple", "Mode share Fc", "Basis"])
GROUPS = {"mat": "Materials", "lab": "Labour", "eng": "Engineering", "site": "Site"}
for i, (name, base, (a, m, b), g) in enumerate(M.ACCOUNTS):
    r = 4 + i
    for j, (v, f) in enumerate(zip([name, base, a, m, b, GROUPS[g]], [None, "0.0", "0.00", "0.00", "0.00", None])):
        c = wi.cell(r, 1 + j, v); c.font = BL if j else AR; c.border = BOX
        if f: c.number_format = f
        if j in (3, 4): c.fill = YEL
    put(wi, f"G{r}", f"=(C{r}+D{r}+E{r})/3", AR, "0.000", box=True)
    put(wi, f"H{r}", f"=(D{r}-C{r})/(E{r}-C{r})", AR, "0.000", box=True)
    put(wi, f"I{r}", "Paper, Table 1", AR, box=True)
put(wi, "A16", "Total base", B); put(wi, "B16", "=SUM(B4:B15)", B, "0.0")
put(wi, "A17", "Expected line-item cost (analytic)", AR); put(wi, "B17", "=SUMPRODUCT(B4:B15,G4:G15)", AR, "0.00")

hdr(wi, 19, ["Correlation of normal scores", "Value", "", "", "", "", "", "", "Basis"], h=20)
corr = [("Materials (within group)", 0.5), ("Labour (within group)", 0.7), ("Engineering (within group)", 0.5), ("Site (single account)", 1.0), ("Between groups", 0.3)]
for i, (k, v) in enumerate(corr):
    r = 20 + i; put(wi, f"A{r}", k, box=True); put(wi, f"B{r}", v, BL, "0.00", box=True)
    put(wi, f"I{r}", "Paper, Section 2; must be >= between-group value" if i < 4 else "Paper, Section 2", box=True)
CORR_ROW = {"Materials": 20, "Labour": 21, "Engineering": 22, "Site": 23}

hdr(wi, 26, ["Risk event", "Probability", "Cost low", "Cost ML", "Cost high", "Delay low (wk)", "Delay ML", "Delay high", "Expected cost incl. delay (C$M)"])
for i, (name, p, cst, dl) in enumerate(M.RISKS):
    r = 27 + i; c0 = cst or (0, 0, 0); d0 = dl or (0, 0, 0)
    vals = [name, p, *c0, *d0]
    for j, v in enumerate(vals):
        c = wi.cell(r, 1 + j, v); c.font = BL if j else AR; c.border = BOX
        c.number_format = "0%" if j == 1 else ("0.0" if j < 5 else "0")
        if j == 1: c.fill = YEL
    put(wi, f"I{r}", f"=B{r}*((C{r}+D{r}+E{r})/3+$B$36*(F{r}+G{r}+H{r})/3)", AR, "0.000", box=True)
put(wi, "A35", "Risk register total expected cost (analytic)", B); put(wi, "I35", "=SUM(I27:I34)", B, "0.00")
put(wi, "A36", "Burn rate of time-dependent cost (C$M/week)", AR, box=True); put(wi, "B36", M.BURN, BL, "0.00", YEL, True)
put(wi, "A37", "A risk with no cost or no delay: leave the three values at 0.", IT)

hdr(wi, 39, ["Escalation and exchange rate (separate reserve)", "Value", "", "", "", "", "", "", "Basis"], h=20)
esc = [("Escalation rate low (/y)", 0.02, "0.0%"), ("Escalation rate most likely (/y)", 0.03, "0.0%"), ("Escalation rate high (/y)", 0.06, "0.0%"),
       ("Escalation carried in the base, e0 (/y)", 0.03, "0.0%"), ("Years to middle of spending, t", 1.5, "0.0"),
       ("Share of major equipment bought in US$", 0.40, "0%"), ("Exchange-rate change low", -0.12, "0%"), ("Exchange-rate change most likely", 0.0, "0%"),
       ("Exchange-rate change high", 0.12, "0%"), ("Accounts subject to escalation (first n rows)", 9, "0")]
for i, (k, v, f) in enumerate(esc):
    r = 40 + i; put(wi, f"A{r}", k, box=True); put(wi, f"B{r}", v, BL, f, box=True); put(wi, f"I{r}", "Paper, Section 2 and Eq. (2)", box=True)
put(wi, "A51", "Flat contingencies to test", B)
put(wi, "A52", "Flat contingency 1", box=True); put(wi, "B52", 0.10, BL, "0%", box=True)
put(wi, "A53", "Flat contingency 2", box=True); put(wi, "B53", 0.15, BL, "0%", box=True)
wi.freeze_panes = "A4"

# ---------------- Simulation ----------------
wsim = sheet("Simulation")
cols = ["Iter", "Z0 common", "Z materials", "Z labour", "Z engineering", "Z site"]
cols += [f"u {n}" for n, *_ in M.ACCOUNTS]
cols += [f"{n} (C$M)" for n, *_ in M.ACCOUNTS]
for n, *_ in M.RISKS: cols += [f"{n}: u hit", "u cost", "u delay", f"{n} (C$M)"]
cols += ["Line items (C$M)", "Risk events (C$M)", "Core cost (C$M)", "u escalation", "u FX", "Escalation factor Ef", "Escalation reserve (C$M)", "Total incl. reserve (C$M)"]
hdr(wsim, 1, cols, h=66); wsim.freeze_panes = "B2"
ZC = {"Materials": "C", "Labour": "D", "Engineering": "E", "Site": "F"}
def tri_expr(u, a, m, b):
    return (f"IF({b}={a},{a},IF({u}<({m}-{a})/({b}-{a}),{a}+SQRT({u}*({b}-{a})*({m}-{a})),"
            f"{b}-SQRT((1-{u})*({b}-{a})*({b}-{m}))))")
U0 = 7; A0 = U0 + 12; K0 = A0 + 12; T0 = K0 + 32
LI, RK, CORE, UE, UF, EF, ESC, TOT = (CL(T0 + i) for i in range(8))
for it in range(NIT):
    r = it + 2
    wsim.cell(r, 1, it + 1)
    for k in range(2, 7): wsim.cell(r, k, "=NORMSINV(RAND())")
    for j, (name, base, _, g) in enumerate(M.ACCOUNTS):
        ir = 4 + j; gname = GROUPS[g]; cr = CORR_ROW[gname]
        wsim.cell(r, U0 + j, f"=NORMSDIST(SQRT(Inputs!$B$24)*$B{r}+SQRT(Inputs!$B${cr}-Inputs!$B$24)*${ZC[gname]}{r}"
                             f"+SQRT(1-Inputs!$B${cr})*NORMSINV(RAND()))")
        u = f"{CL(U0 + j)}{r}"
        wsim.cell(r, A0 + j, f"=Inputs!$B${ir}*" + tri_expr(u, f"Inputs!$C${ir}", f"Inputs!$D${ir}", f"Inputs!$E${ir}"))
    for k in range(8):
        c0 = K0 + 4 * k; ir = 27 + k
        for t in range(3): wsim.cell(r, c0 + t, "=RAND()")
        uh, uc, ud = (f"{CL(c0 + t)}{r}" for t in range(3))
        cost = tri_expr(uc, f"Inputs!$C${ir}", f"Inputs!$D${ir}", f"Inputs!$E${ir}")
        dly = tri_expr(ud, f"Inputs!$F${ir}", f"Inputs!$G${ir}", f"Inputs!$H${ir}")
        wsim.cell(r, c0 + 3, f"=IF({uh}<Inputs!$B${ir},{cost}+Inputs!$B$36*{dly},0)")
    wsim[f"{LI}{r}"] = f"=SUM({CL(A0)}{r}:{CL(A0 + 11)}{r})"
    wsim[f"{RK}{r}"] = "=" + "+".join(f"{CL(K0 + 4 * k + 3)}{r}" for k in range(8))
    wsim[f"{CORE}{r}"] = f"={LI}{r}+{RK}{r}"
    wsim[f"{UE}{r}"] = "=RAND()"; wsim[f"{UF}{r}"] = "=RAND()"
    wsim[f"{EF}{r}"] = f"=((1+{tri_expr(f'{UE}{r}', 'Inputs!$B$40', 'Inputs!$B$41', 'Inputs!$B$42')})/(1+Inputs!$B$43))^Inputs!$B$44"
    wsim[f"{ESC}{r}"] = (f"=({EF}{r}-1)*SUM(OFFSET({CL(A0)}{r},0,0,1,Inputs!$B$49))"
                         f"+{EF}{r}*Inputs!$B$4*Inputs!$B$45*{tri_expr(f'{UF}{r}', 'Inputs!$B$46', 'Inputs!$B$47', 'Inputs!$B$48')}")
    wsim[f"{TOT}{r}"] = f"={CORE}{r}+{ESC}{r}"
for i in range(1, len(cols) + 1): wsim.column_dimensions[CL(i)].width = 11
LAST = 20001
rng = lambda col: f"Simulation!${col}$2:${col}${LAST}"

# ---------------- Results ----------------
wr = sheet("Results")
for col, w in zip("ABCDEFGH", (46, 14, 14, 3, 40, 14, 14, 14)): wr.column_dimensions[col].width = w
put(wr, "A1", "Results (live; press F9 for a new draw)", T1)
put(wr, "A2", '=TEXT(COUNT(' + rng(CORE) + '),"#,##0")&" iterations on the Simulation sheet"', IT)
hdr(wr, 4, ["Measure", "Value", "Paper (50,000 it.)"], h=20)
pp = R["main"]; tt = R["total"]; ee = R["escfx"]
meas = [("Base estimate (C$M)", "=Inputs!B16", 100.0, "0.0"),
        ("P50 core cost (C$M)", f"=PERCENTILE({rng(CORE)},0.5)", pp["P50"], "0.0"),
        ("P80 core cost (C$M)", f"=PERCENTILE({rng(CORE)},0.8)", pp["P80"], "0.0"),
        ("P90 core cost (C$M)", f"=PERCENTILE({rng(CORE)},0.9)", pp["P90"], "0.0"),
        ("Mean core cost (C$M)", f"=AVERAGE({rng(CORE)})", pp["mean"], "0.0"),
        ("P50 contingency (% of base)", "=B6/B5-1", pp["P50"] / 100 - 1, "0.0%"),
        ("P80 contingency (% of base)", "=B7/B5-1", pp["P80"] / 100 - 1, "0.0%"),
        ("P90 contingency (% of base)", "=B8/B5-1", pp["P90"] / 100 - 1, "0.0%"),
        ("Chance the base alone is enough", f"=COUNTIF({rng(CORE)},\"<=\"&B5)/COUNT({rng(CORE)})", pp["p_under_base"], "0.0%"),
        ("Chance of overrunning flat contingency 1", f"=COUNTIF({rng(CORE)},\">\"&B5*(1+Inputs!B52))/COUNT({rng(CORE)})", pp["p_over_110"], "0.0%"),
        ("Chance of overrunning flat contingency 2", f"=COUNTIF({rng(CORE)},\">\"&B5*(1+Inputs!B53))/COUNT({rng(CORE)})", pp["p_over_115"], "0.0%"),
        ("Escalation reserve P50 (C$M)", f"=PERCENTILE({rng(ESC)},0.5)", ee["P50"], "0.00"),
        ("Escalation reserve P80 (C$M)", f"=PERCENTILE({rng(ESC)},0.8)", ee["P80"], "0.00"),
        ("Total incl. reserve P50 (C$M)", f"=PERCENTILE({rng(TOT)},0.5)", tt["P50"], "0.0"),
        ("Total incl. reserve P80 (C$M)", f"=PERCENTILE({rng(TOT)},0.8)", tt["P80"], "0.0"),
        ("Total incl. reserve P90 (C$M)", f"=PERCENTILE({rng(TOT)},0.9)", tt["P90"], "0.0")]
for i, (k, f, ref, fm) in enumerate(meas):
    r = 5 + i; put(wr, f"A{r}", k, box=True); put(wr, f"B{r}", f, AR, fm, OK if i in (2, 6) else None, True); put(wr, f"C{r}", ref, AR, fm, GRY, True)

put(wr, "E4", "Build-up of the P80 (C$M)", B)
bu = [("Base", "=B5"), ("Skew of line-item ranges", f"=AVERAGE({rng(LI)})-B5"), ("Expected cost of risk events", f"=AVERAGE({rng(RK)})"),
      ("Mean", "=B9"), ("Margin from mean to P80", "=B7-B9"), ("P80 budget", "=B7")]
for i, (k, f) in enumerate(bu):
    r = 5 + i; put(wr, f"E{r}", k, box=True); put(wr, f"F{r}", f, AR, "0.00", box=True)
put(wr, "E12", "Checks", B)
chk = [("Line-item mean: simulated vs analytic", f"=AVERAGE({rng(LI)})", "=Inputs!B17"),
       ("Risk events mean: simulated vs analytic", f"=AVERAGE({rng(RK)})", "=Inputs!I35")]
hdr(wr, 13, ["Check", "Simulated", "Analytic", "Difference"], col=5, h=20)
for i, (k, a, b) in enumerate(chk):
    r = 14 + i; put(wr, f"E{r}", k, box=True); put(wr, f"F{r}", a, AR, "0.00", box=True); put(wr, f"G{r}", b, GR, "0.00", box=True)
    put(wr, f"H{r}", f"=F{r}/G{r}-1", AR, "0.0%", box=True)
put(wr, "E16", "Differences within about 1% are sampling error at 5,000 iterations.", IT)

put(wr, "A23", "S-curve: core cost percentiles", B)
hdr(wr, 24, ["Probability of not exceeding", "Core cost (C$M)", "Total incl. reserve (C$M)"], h=32)
for i, q in enumerate(range(1, 20)):
    r = 25 + i; p = q * 0.05
    put(wr, f"A{r}", p, AR, "0%", box=True)
    put(wr, f"B{r}", f"=PERCENTILE({rng(CORE)},A{r})", AR, "0.0", box=True)
    put(wr, f"C{r}", f"=PERCENTILE({rng(TOT)},A{r})", AR, "0.0", box=True)
ch = ScatterChart(); ch.title = "S-curve of final cost (base-date prices)"; ch.style = 13
ch.x_axis.title = "Final cost (C$ million)"; ch.y_axis.title = "Probability of not exceeding"
ch.y_axis.number_format = "0%"; ch.y_axis.scaling.min = 0; ch.y_axis.scaling.max = 1
s1 = Series(Reference(wr, min_col=1, min_row=25, max_row=43), Reference(wr, min_col=2, min_row=25, max_row=43), title="Core cost")
s2 = Series(Reference(wr, min_col=1, min_row=25, max_row=43), Reference(wr, min_col=3, min_row=25, max_row=43), title="Including escalation reserve")
for s in (s1, s2): s.marker.symbol = "none"; s.smooth = True; ch.series.append(s)
ch.roundedCorners = False; ch.legend.position = "b"; ch.legend.overlay = False; ch.title.overlay = False
ch.x_axis.title.overlay = False; ch.y_axis.title.overlay = False; ch.x_axis.delete = False; ch.y_axis.delete = False
ch.width = 18; ch.height = 10
wr.add_chart(ch, "E23")

# ---------------- Model_Results ----------------
wm = sheet("Model_Results")
wm.column_dimensions["A"].width = 48
for c in "BCDEF": wm.column_dimensions[c].width = 13
put(wm, "A1", "Paper's Python model, 50,000 iterations (values)", T1)
r = 3
def table(title, header, rows_):
    global r
    put(wm, f"A{r}", title, B); r += 1; hdr(wm, r, header, h=32); r += 1
    for row in rows_:
        for j, v in enumerate(row):
            c = wm.cell(r, 1 + j, v); c.font = AR; c.border = BOX
            if j: c.fill = GRY; c.number_format = "0.00" if isinstance(v, float) else "General"
        r += 1
    r += 1
table("Correlation and range width (P80 contingency, C$M)", ["Ranges", "Line items independent", "Correlated"],
      [("Class 3", R["corr"]["0.0"]["P80"] - 100, R["corr"]["1.0"]["P80"] - 100),
       ("1.5 times wider", R["wide"]["1.5_0.0"]["P80"] - 100, R["wide"]["1.5_1.0"]["P80"] - 100),
       ("2 times wider", R["wide"]["2.0_0.0"]["P80"] - 100, R["wide"]["2.0_1.0"]["P80"] - 100)])
table("Risk events: fall in P80 (C$M)", ["Risk", "Eliminated", "At expected value"],
      [(n, R["risk_p80"][n],
        R["risk_p80_ev"][n]) for n, *_ in M.RISKS])
table("Estimate classes (core cost, C$M)", ["Class", "P50", "P80", "P90"],
      [(k, v["P50"], v["P80"], v["P90"]) for k, v in R["classes"].items()])
table("First-of-a-kind scale-up risk (core cost, C$M)", ["Case", "P50", "P80"], [("FOAK", R["foak"]["P50"], R["foak"]["P80"])])

# ---------------- Changelog ----------------
wc = sheet("Changelog"); wc.column_dimensions["A"].width = 10; wc.column_dimensions["B"].width = 14; wc.column_dimensions["C"].width = 100
hdr(wc, 1, ["Version", "Date", "Change"], h=20)
for j, v in enumerate(["V1", "2026-11-27", f"First release with the journal paper: live Monte Carlo with {NIT:,} iterations (RAND formulas, common-factor correlation), escalation reserve, results with checks and S-curve, stored model results."]):
    c = wc.cell(2, 1 + j, v); c.font = AR; c.alignment = WRAP

out = "/mnt/user-data/outputs/Cost_Contingency_Monte_Carlo_Template_V1.xlsx"
wb.save(out); print(out)
