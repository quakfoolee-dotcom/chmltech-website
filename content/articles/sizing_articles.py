"""Equipment sizing series (3 parts) and the relief systems article for Insights (V4.68).

Part 1  Sizing a pump: P-101
Part 2  Sizing a heat exchanger: E-101
Part 3  Sizing a tank: T-101 holdup, levels and wall thickness
Single  Pressure relief basics: what a PSV protects against and how the relief case is chosen (R-101)

The example is the feed section from "How to read a PFD and a P&ID" and the HAZOP post: tank T-101, pump P-101,
steam heater E-101 and the 10,000 L reactor R-101 of the scale-up series. All numbers are computed here.

Usage:  python3 content/articles/sizing_articles.py
        python3 content/gen/add_article.py <slug>   (each)
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))


def fig3d(name):
    """Interactive 3D figure (V5.17): the markup lives in content/articles/fig3d/<name>.html."""
    return open(os.path.join(HERE, "fig3d", name + ".html"), encoding="utf-8").read().rstrip("\n") + "\n"


def js3d(script):
    """Script tags for a 3D figure: the vendored three.js build, then the figure's own script."""
    return ('\n<script src="../assets/js/vendor/three-r128.min.js" defer></script>'
            f'\n<script src="../assets/js/{script}.js" defer></script>')
sys.path.insert(0, HERE)
from feed_articles import (nowrap, svg, fig, box, txt, arrow, DEFS, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, RED,
                           MUTED, LINE, SAND, PALE, GREENF, ORANGEF)
from process_eng_articles import geom, PF as PFDPID

Z1 = "sizing-a-pump-head-npsh-and-power"
Z2 = "sizing-a-heat-exchanger-duty-lmtd-and-area"
Z3 = "sizing-a-tank-holdup-levels-and-wall-thickness"
RLF = "pressure-relief-basics-what-a-psv-protects-against"
HAZOP = "a-worked-hazop-the-feed-heater-node-by-node"
RUN = "what-happens-if-the-cooling-fails-runaway-reactions"
DB = "the-design-basis-ten-decisions-to-fix-before-engineering-starts"
DATE = "2026-11-13"
L = {1: f'<a href="{Z1}.html">Part&nbsp;1</a>', 2: f'<a href="{Z2}.html">Part&nbsp;2</a>', 3: f'<a href="{Z3}.html">Part&nbsp;3</a>'}
NOTE = ('<p class="oee-note"><em>The plant, fluid properties and equipment in this series are an illustrative example. The calculations '
        'are preliminary sizing estimates. Final sizing needs vendor data, the applicable codes and a qualified engineer.</em></p>')
SER = lambda n: {"name": "Equipment sizing series", "part": n, "of": 3}
G = 9.81

# ───────────────────────── shared fluid and duty ─────────────────────────
M = 6250.0            # kg/h feed
RHO, MU, CP = 850.0, 0.0006, 2.0      # kg/m3, Pa.s, kJ/kg.K
PV = 2900.0           # Pa vapour pressure at 20 C
Q_N = M / RHO         # m3/h normal
Q_R = Q_N * 1.10      # rated flow with 10 % margin


def darcy(Q_m3h, D, Lm, eps=0.045e-3):
    A = math.pi * D * D / 4; v = Q_m3h / 3600 / A
    Re = RHO * v * D / MU
    f = 0.25 / (math.log10(eps / (3.7 * D) + 5.74 / Re ** 0.9)) ** 2          # Swamee-Jain
    dp = f * Lm / D * RHO * v * v / 2
    return v, Re, f, dp


# discharge line: 1.5" sch 40, 60 m equivalent; suction 2" sch 40, 8 m equivalent
D_DIS, L_DIS, D_SUC, L_SUC = 0.0409, 60.0, 0.0525, 8.0
V_D, RE_D, F_D, DP_D = darcy(Q_R, D_DIS, L_DIS)
V_S, RE_S, F_S, DP_S = darcy(Q_R, D_SUC, L_SUC)
P_R, Z_R, DP_E, DP_CV, DP_MISC = 1.0e5, 8.0, 0.5e5, 1.2e5, 0.2e5            # reactor barg, elevation m, heater, valve, meter+strainer
Z_SUC_MIN = 1.0                                                              # m liquid above pump centreline at low level
P_DIS = P_R + RHO * G * Z_R + DP_D + DP_E + DP_CV + DP_MISC                  # Pa(g) at pump discharge
P_SUC = RHO * G * Z_SUC_MIN - DP_S                                           # Pa(g) at pump suction
H_TDH = (P_DIS - P_SUC) / (RHO * G)
NPSHA = (101325 - PV) / (RHO * G) + Z_SUC_MIN - DP_S / (RHO * G)
NPSHR = 2.5
ETA = 0.45
P_HYD = RHO * G * Q_R / 3600 * H_TDH / 1000
P_SHAFT = P_HYD / ETA
MOTOR = next(m for m in (0.75, 1.1, 1.5, 2.2, 3.0, 4.0, 5.5, 7.5) if m >= 1.25 * P_SHAFT)

# ───────────────────────── heat exchanger ─────────────────────────
T_IN, T_OUT, T_ST = 20.0, 80.0, 143.6         # C; saturated steam at 3.0 barg
DUTY = M * CP * (T_OUT - T_IN) / 3600         # kW
DT1, DT2 = T_ST - T_IN, T_ST - T_OUT
LMTD = (DT1 - DT2) / math.log(DT1 / DT2)
U_CL = 500.0                                  # W/m2K clean-ish, steam condensing / light organic in tubes
A_REQ = DUTY * 1000 / (U_CL * LMTD)
OVERS = 0.20
A_DES = A_REQ * (1 + OVERS)
DO, DI = 0.01905, 0.01575                     # 3/4" OD tube, 16 BWG
V_TUBE = 1.0
N_PASS_T = math.ceil(Q_N / 3600 / (V_TUBE * math.pi * DI ** 2 / 4))
N_TUBES = 2 * N_PASS_T
L_TUBE = A_DES / (N_TUBES * math.pi * DO)
LAMBDA_ST = 2133.0
M_ST = DUTY * 3600 / LAMBDA_ST

# ───────────────────────── tank ─────────────────────────
HOLD_H = 8.0
V_WORK = M * HOLD_H / RHO
FILL = 0.80
V_TANK = V_WORK / FILL
D_T = 4.0
H_T = V_TANK / (math.pi * D_T ** 2 / 4)
H_T_SEL = math.ceil(H_T * 2) / 2
SD, CA, GS = 137.0, 1.5, RHO / 1000          # MPa allowable (A36-like, API 650 design), mm corrosion, specific gravity
T_SHELL = 4.9 * D_T * (H_T_SEL - 0.3) * GS / SD + CA
T_MIN = 5.0

# ───────────────────────── reactor fire case ─────────────────────────
VR = 10.0
DR, AR, _, _ = geom(VR)                       # diameter m (H = D vessel), total area
HR = DR                                       # geom assumes height = diameter
FILLR = 0.80
A_WET = math.pi * DR * HR * FILLR + math.pi * DR ** 2 / 4    # wetted wall + bottom (flat-bottom approximation)
F_ENV = 1.0
Q_FIRE = 43200 * F_ENV * A_WET ** 0.82 / 1000                # kW, API 521, adequate drainage and fire fighting
LAT = 360.0                                                   # kJ/kg latent heat of the solvent at relief conditions
W_FIRE = Q_FIRE * 3600 / LAT


def f0(x): return f"{x:,.0f}"
def f1(x): return f"{x:,.1f}"
def f2(x): return f"{x:,.2f}"


# ───────────────────────── figures ─────────────────────────
def fig_pump_curve():
    def sys_h(q):
        _, _, _, dpd = darcy(q, D_DIS, L_DIS); _, _, _, dps = darcy(q, D_SUC, L_SUC)
        pd = P_R + RHO * G * Z_R + dpd + DP_E * (q / Q_R) ** 2 + DP_CV + DP_MISC * (q / Q_R) ** 2
        return (pd - (RHO * G * Z_SUC_MIN - dps)) / (RHO * G)
    shut = H_TDH * 1.22
    pump = lambda q: shut - (shut - H_TDH) * (q / Q_R) ** 2
    X = lambda q: 80 + q / 12 * 600; Y = lambda h: 250 - h / 70 * 220
    s = ""
    for h in range(0, 71, 10):
        s += f'<line x1="80" y1="{Y(h):.1f}" x2="680" y2="{Y(h):.1f}" stroke="{LINE}"/>' + txt(72, Y(h) + 4, str(h), "end", MUTED, 12)
    for q in range(0, 13, 2):
        s += txt(X(q), 268, str(q), "middle", MUTED, 12)
    s += txt(380, 290, "Flow (m³/h)", "middle", NAVY, 12.5, True) + txt(14, 20, "Head (m)", fill=NAVY, fs=12.5, bold=True)
    qs = [i * 0.1 for i in range(1, 121)]
    s += '<polyline fill="none" stroke="' + BLUE + '" stroke-width="2.5" points="' + " ".join(f"{X(q):.1f},{Y(sys_h(q)):.1f}" for q in qs) + '"/>'
    s += '<polyline fill="none" stroke="' + ORANGE + '" stroke-width="2.5" points="' + " ".join(f"{X(q):.1f},{Y(pump(q)):.1f}" for q in qs if pump(q) > 0) + '"/>'
    s += f'<circle cx="{X(Q_R):.1f}" cy="{Y(H_TDH):.1f}" r="6" fill="{NAVY}"/>'
    s += f'<line x1="{X(Q_R):.1f}" y1="{Y(H_TDH) + 8:.1f}" x2="{X(Q_R):.1f}" y2="{Y(24):.1f}" stroke="{NAVY}" stroke-width="1.2" stroke-dasharray="4 3"/>'
    s += txt(X(Q_R), Y(20), f"Rated point: {f1(Q_R)} m³/h at {f0(H_TDH)} m", "middle", NAVY, 12.5, True)
    s += txt(X(11.6), Y(sys_h(11.6)) - 8, "System curve", "end", BLUE, 12.5, True)
    s += txt(X(1.0), Y(pump(1.0)) - 8, "Pump curve (illustrative)", fill=ORANGE, fs=12.5, bold=True)
    return svg(f"Chart of head against flow. The system curve starts at about {f0(sys_h(0.1))} metres at zero flow, mostly static head and fixed pressure drops, and rises with flow. "
               f"An illustrative pump curve falls from about {f0(shut)} metres at shutoff. They cross at the rated point of {f1(Q_R)} cubic metres per hour and {f0(H_TDH)} metres.",
               700, 300, s, 600, x0=0)


def fig_hx_profile():
    X = lambda f: 90 + f * 560; Y = lambda t: 240 - (t - 0) / 160 * 210
    s = ""
    for t in range(0, 161, 40):
        s += f'<line x1="90" y1="{Y(t):.1f}" x2="650" y2="{Y(t):.1f}" stroke="{LINE}"/>' + txt(82, Y(t) + 4, f"{t} °C", "end", MUTED, 12)
    s += f'<line x1="{X(0)}" y1="{Y(T_ST)}" x2="{X(1)}" y2="{Y(T_ST)}" stroke="{ORANGE}" stroke-width="2.6"/>'
    s += txt(X(0.5), Y(T_ST) - 10, f"Condensing steam at 3.0 barg: {T_ST} °C", "middle", ORANGE, 12.5, True)
    pts = []
    for i in range(0, 101):
        f = i / 100; t = T_ST - DT1 * (DT2 / DT1) ** f; pts.append(f"{X(f):.1f},{Y(t):.1f}")
    s += '<polyline fill="none" stroke="' + BLUE + '" stroke-width="2.6" points="' + " ".join(pts) + '"/>'
    s += txt(X(0.62), Y(62) + 22, "Feed: 20 → 80 °C", "middle", BLUE, 12.5, True)
    for f, dt, lab in ((0, DT1, f"ΔT₁ = {f1(DT1)} K"), (1, DT2, f"ΔT₂ = {f1(DT2)} K")):
        t = T_ST - dt
        s += f'<line x1="{X(f) + (8 if f == 0 else -8)}" y1="{Y(T_ST)}" x2="{X(f) + (8 if f == 0 else -8)}" y2="{Y(t)}" stroke="{NAVY}" stroke-width="1.4" stroke-dasharray="4 3"/>'
        s += txt(X(f) + (14 if f == 0 else -14), (Y(T_ST) + Y(t)) / 2, lab, "start" if f == 0 else "end", NAVY, 12.5, True)
    s += txt(370, 268, "Position along the exchanger (feed inlet → outlet)", "middle", NAVY, 12.5, True)
    return svg(f"Temperature against position along the heater. Steam condenses at a constant {T_ST} degrees Celsius. The feed rises from 20 to 80 degrees along a curve. "
               f"The temperature difference is {f1(DT1)} kelvin at the feed inlet and {f1(DT2)} kelvin at the outlet, giving a log mean of {f1(LMTD)} kelvin.",
               700, 280, s, 600, x0=0)


def fig_tank():
    s = DEFS
    x0, w, ytop, ybot = 220, 220, 30, 270
    Hs = H_T_SEL
    Y = lambda h: ybot - h / Hs * (ybot - ytop)
    s += f'<rect x="{x0}" y="{ytop}" width="{w}" height="{ybot - ytop}" fill="{PALE}" stroke="{NAVY}" stroke-width="2"/>'
    hll = H_T * FILL + 0.0
    levels = [("HHLL: high-high trip", H_T * 0.90, RED), ("HLL: high alarm", H_T * 0.85, ORANGE), ("NLL: normal", H_T * 0.55, BLUE),
              ("LLL: low alarm", 1.2, ORANGE), ("LLLL: low-low trip, pump stops", 0.8, RED)]
    s += f'<rect x="{x0 + 2}" y="{Y(H_T * 0.55):.1f}" width="{w - 4}" height="{ybot - Y(H_T * 0.55) - 2:.1f}" fill="{BLUE}" opacity=".18"/>'
    nudge = {"HHLL: high-high trip": -4, "HLL: high alarm": 5, "LLL: low alarm": -4, "LLLL: low-low trip, pump stops": 5}
    for lab, h, col in levels:
        s += f'<line x1="{x0 - 14}" y1="{Y(h):.1f}" x2="{x0 + w + 14}" y2="{Y(h):.1f}" stroke="{col}" stroke-width="1.6" stroke-dasharray="6 4"/>'
        s += txt(x0 + w + 22, Y(h) + 4 + nudge.get(lab, 0), f"{lab}  {f1(h)} m", fill=col, fs=12.5, bold=True)
    s += txt(x0 + w / 2, ybot + 22, f"T-101: {f1(D_T)} m diameter × {f1(Hs)} m shell", "middle", NAVY, 13, True)
    s += f'<line x1="{x0 - 40}" y1="{Y(0.8):.1f}" x2="{x0 - 40}" y2="{Y(H_T * 0.85):.1f}" stroke="{GREEND}" stroke-width="2"/>'
    s += txt(x0 - 48, (Y(0.8) + Y(H_T * 0.85)) / 2, "working", "end", GREEND, 12.5, True)
    s += txt(x0 - 48, (Y(0.8) + Y(H_T * 0.85)) / 2 + 16, "volume", "end", GREEND, 12.5, True)
    return svg(f"Vertical tank T-101, {f1(D_T)} metres in diameter with a {f1(Hs)} metre shell, with five level settings marked from bottom to top: low-low trip at 0.8 metres, "
               f"low alarm at 1.2 metres, normal level at {f1(H_T * 0.55)} metres, high alarm at {f1(H_T * 0.85)} metres and high-high trip at {f1(H_T * 0.90)} metres. "
               "The working volume lies between the low-low and high levels.", 720, 300, s, 600, x0=40)


def fig_relief():
    rows = [("Normal operating pressure", 1.0, BLUE), ("Set pressure = MAWP", 3.0, NAVY), ("Max. while relieving: single device (+10%)", 3.3, ORANGE),
            ("Max. while relieving: multiple devices (+16%)", 3.48, PURPLE), ("Max. while relieving: fire case (+21%)", 3.63, RED)]
    X = lambda p: 330 + p / 4.0 * 360; s = ""
    for p in (0, 1, 2, 3, 4):
        s += f'<line x1="{X(p):.1f}" y1="14" x2="{X(p):.1f}" y2="{20 + len(rows) * 34}" stroke="{LINE}"/>' + txt(X(p), 34 + len(rows) * 34, f"{p} barg", "middle", MUTED, 11.5)
    for i, (lab, p, col) in enumerate(rows):
        y = 20 + i * 34
        s += txt(320, y + 17, lab, "end", col, 12.5, True)
        s += f'<rect x="{X(0)}" y="{y + 4}" width="{X(p) - X(0):.1f}" height="20" rx="3" fill="{col}" opacity=".85"/>'
        s += txt(X(p) + 6, y + 19, f"{p:.2f}".rstrip("0").rstrip(".") + " barg", fill=col, fs=12, bold=True)
    s += f'<line x1="{X(3.0):.1f}" y1="14" x2="{X(3.0):.1f}" y2="{20 + len(rows) * 34}" stroke="{NAVY}" stroke-width="1.4" stroke-dasharray="5 4"/>'
    return svg("Horizontal bars for reactor R-101. Normal operating pressure 1.0 barg. Relief valve set pressure equal to the MAWP, 3.0 barg. "
               "Maximum pressure while relieving: 3.3 barg for a single relief device (10 percent accumulation), 3.48 barg for multiple devices (16 percent) and 3.63 barg for a fire case (21 percent).",
               740, 38 + len(rows) * 34, s, 620, x0=0)


# ───────────────────────── Part 1: pump ─────────────────────────
def part1():
    body = f"""{CSS}
<p>Every process plant is full of pumps, and most of them were sized from the same handful of numbers: how much flow, against how much head, with how much suction margin, using how much power. Get one wrong and the pump runs off its curve, cavitates or trips its motor. This three-part series sizes the main equipment in the feed section you met in <a href="{PFDPID}.html">How to Read a PFD and a P&amp;ID</a>: pump P-101 here, heater E-101 in {L[2]} and feed tank T-101 in {L[3]}.</p>
<p>The aim is not to replace the engineer who specifies the pump. It is to show owners and managers where the numbers on a pump data sheet come from, so that they can check them and ask the right questions.</p>
<h2>Step 1: set the flow</h2>
<p>P-101 moves the feed from T-101 through E-101 to reactor R-101 at {f0(M)}&nbsp;kg/h. With a density of {f0(RHO)}&nbsp;kg/m³ that is {f2(Q_N)}&nbsp;m³/h at normal flow. Pumps are specified at a <strong>rated flow</strong> above normal, to cover uncertainty and control. A 10% margin gives {f2(Q_R)}&nbsp;m³/h. Margins belong in the <a href="{DB}.html">design basis</a>, stated once, not added again by each discipline.</p>
<h2>Step 2: add up the head</h2>
<p>The pump must lift the liquid, overcome every pressure drop on the way and deliver it at the pressure the reactor needs. Work out the pressure the pump must produce at its discharge, subtract what it already has at its suction, and convert the difference to metres of liquid.</p>
<table>
<tr><th>Discharge side, at rated flow</th><th class="num">kPa</th><th>Basis</th></tr>
<tr><td>Reactor operating pressure</td><td class="num">{f0(P_R / 1000)}</td><td>1.0&nbsp;barg</td></tr>
<tr><td>Static lift to the reactor nozzle</td><td class="num">{f0(RHO * G * Z_R / 1000)}</td><td>{f0(Z_R)}&nbsp;m above the pump</td></tr>
<tr><td>Pipe friction, discharge</td><td class="num">{f0(DP_D / 1000)}</td><td>1½" pipe, {f0(L_DIS)}&nbsp;m equivalent length</td></tr>
<tr><td>Heater E-101, tube side</td><td class="num">{f0(DP_E / 1000)}</td><td>Allowance; checked in {L[2]}</td></tr>
<tr><td>Flow control valve</td><td class="num">{f0(DP_CV / 1000)}</td><td>Enough drop to control well</td></tr>
<tr><td>Flow meter and strainer</td><td class="num">{f0(DP_MISC / 1000)}</td><td>Allowance</td></tr>
<tr><td><strong>Required discharge pressure</strong></td><td class="num"><strong>{f0(P_DIS / 1000)}</strong></td><td><strong>{f2(P_DIS / 1e5)}&nbsp;barg</strong></td></tr>
<tr><td>Less: suction pressure at low tank level</td><td class="num">{f0(P_SUC / 1000)}</td><td>{f1(Z_SUC_MIN)}&nbsp;m of liquid, less suction friction</td></tr>
<tr><td><strong>Differential pressure</strong></td><td class="num"><strong>{f0((P_DIS - P_SUC) / 1000)}</strong></td><td><strong>Total head {f1(H_TDH)}&nbsp;m</strong></td></tr>
</table>
<p>Pipe friction comes from the Darcy–Weisbach equation, ΔP = <em>f</em> × (L/D) × ρv²/2. In the discharge line the velocity is {f2(V_D)}&nbsp;m/s, the Reynolds number is about {f0(RE_D)} (fully turbulent) and the friction factor is {F_D:.4f}. The control valve is often the term people want to cut. Don't: a valve with too little pressure drop cannot control the flow.</p>
<p>The head is converted from pressure with H = ΔP / (ρg). Head in metres is the natural unit for pumps because a centrifugal pump produces the same head whatever the liquid's density; the pressure it produces scales with density.</p>
<h2>Step 3: check the system curve</h2>
<p>Static lift and fixed pressures do not change with flow. Friction rises roughly with the square of flow. Plotting the total against flow gives the <strong>system curve</strong>. The pump's own curve falls as flow rises. The pump runs where the two cross.</p>
{fig(fig_pump_curve(), 1, "System curve for P-101 and an illustrative pump curve. Most of the head is static lift and fixed pressure drops, so the system curve is fairly flat.")}
<p>Two things follow from the shape. First, because most of the head here does not depend on flow, a small error in the friction estimate barely moves the operating point. Second, a pump with a curve that is too flat in this region will hunt as the control valve moves. Pick a pump whose rated point sits near its best efficiency point.</p>
<h2>Step 4: check the suction (NPSH)</h2>
<p>If the pressure at the pump inlet falls below the liquid's vapour pressure, bubbles form and collapse inside the impeller. That is cavitation: noise, vibration, lost head and eroded impellers. The check compares the <strong>net positive suction head available</strong> from the system with the <strong>NPSH required</strong> by the pump, from the vendor's curve.</p>
<p>NPSHa = (P<sub>atm</sub> − P<sub>vap</sub>) / (ρg) + liquid height above the pump − suction friction</p>
<p>With the tank open to atmosphere, a vapour pressure of {f1(PV / 1000)}&nbsp;kPa at 20&nbsp;°C, {f1(Z_SUC_MIN)}&nbsp;m of liquid at low level and {f2(DP_S / (RHO * G))}&nbsp;m of suction friction, NPSHa is about <strong>{f1(NPSHA)}&nbsp;m</strong>. A small pump of this kind typically needs {f1(NPSHR)}&nbsp;m. The margin is ample. It shrinks quickly if the liquid is hot or volatile, which is why NPSH is checked at the worst case: lowest tank level, highest liquid temperature, highest flow.</p>
<h2>Step 5: power and motor</h2>
<p>Hydraulic power is P = ρ g Q H. At rated flow and head that is {f2(P_HYD)}&nbsp;kW. Small centrifugal pumps are not very efficient. At {f0(ETA * 100)}%, the shaft power is about {f2(P_SHAFT)}&nbsp;kW. The motor is sized for the end of the pump curve, not the rated point. Allowing about 25% for that and a margin, the next standard size, {MOTOR:g}&nbsp;kW, is a reasonable selection. The PFD in the earlier article shows P-101 delivering 4.0&nbsp;barg; the build-up above arrives at {f2(P_DIS / 1e5)}&nbsp;barg, which is how a number on a PFD is checked.</p>
{fig3d("pump")}<h2>The data sheet</h2>
<table>
<tr><th>Item</th><th>P-101 value</th></tr>
<tr><td>Service</td><td>Reactor feed, T-101 to R-101 via E-101</td></tr>
<tr><td>Normal / rated flow</td><td>{f2(Q_N)} / {f2(Q_R)}&nbsp;m³/h</td></tr>
<tr><td>Liquid density / viscosity</td><td>{f0(RHO)}&nbsp;kg/m³ / {f2(MU * 1000)}&nbsp;mPa·s at 20&nbsp;°C</td></tr>
<tr><td>Suction / discharge pressure (rated)</td><td>{f2(P_SUC / 1e5)} / {f2(P_DIS / 1e5)}&nbsp;barg</td></tr>
<tr><td>Differential head</td><td>{f1(H_TDH)}&nbsp;m</td></tr>
<tr><td>NPSH available</td><td>{f1(NPSHA)}&nbsp;m</td></tr>
<tr><td>Estimated shaft power</td><td>{f2(P_SHAFT)}&nbsp;kW; motor {MOTOR:g}&nbsp;kW</td></tr>
</table>
<p>The data sheet goes to vendors, who return their curves. The engineer then checks each offer against the system curve, the NPSH margin and the motor size, and confirms that the shutoff head does not exceed the design pressure of the discharge piping and E-101. That last check links pump sizing to <a href="{RLF}.html">pressure relief</a>.</p>
<h2>Key points</h2>
<ul>
<li>Size at a rated flow above normal, with the margin set once in the design basis.</li>
<li>Head is the discharge pressure needed minus the suction pressure available, converted to metres of liquid.</li>
<li>Most of the head in a typical plant is static lift and fixed pressure drops, not pipe friction.</li>
<li>Check NPSH at the worst case: lowest level, hottest liquid, highest flow.</li>
<li>Size the motor for the end of the pump curve, and check shutoff head against the design pressure downstream.</li>
</ul>
<p>Next: {L[2]} sizes the heater, E-101.</p>
{NOTE}{js3d("pm3d")}"""
    body = nowrap(body, [(1, 0, 34), (1, 1, 6), (2, 0, 34)])
    return dict(slug=Z1, title="Sizing a Pump: Head, NPSH and Power, Worked Step by Step",
                desc="How a centrifugal pump is sized: rated flow, head from the pressure build-up, system curve, NPSH check, power and motor, on a worked example.",
                cats=["process-engineering"], tags=["pump sizing", "total dynamic head", "NPSH", "system curve", "centrifugal pump", "process design"],
                body=body, date=DATE, author="Quak Foo Lee", read="7 min read", series=SER(1), cover_label="Equipment sizing",
                related=[Z2, Z3, PFDPID])


# ───────────────────────── Part 2: heat exchanger ─────────────────────────
def part2():
    body = f"""{CSS}
<p>{L[1]} sized pump P-101. This part sizes the heater it feeds: E-101, a shell-and-tube exchanger that uses low-pressure steam to warm the reactor feed. The method is the same for most heaters and coolers: find the duty, find the temperature driving force, choose an overall heat transfer coefficient, and calculate the area.</p>
<h2>Step 1: the duty</h2>
<p>The feed of {f0(M)}&nbsp;kg/h is heated from {f0(T_IN)}&nbsp;°C to {f0(T_OUT)}&nbsp;°C with a heat capacity of {f1(CP)}&nbsp;kJ/kg·K:</p>
<p>Q = ṁ × c<sub>p</sub> × ΔT = {f0(M)} × {f1(CP)} × {f0(T_OUT - T_IN)} / 3,600 = <strong>{f0(DUTY)}&nbsp;kW</strong></p>
<p>That matches the stream table in <a href="{PFDPID}.html">How to Read a PFD and a P&amp;ID</a>. The steam needed is the duty divided by the latent heat of steam at 3.0&nbsp;barg, about {f0(LAMBDA_ST)}&nbsp;kJ/kg: roughly {f0(M_ST)}&nbsp;kg/h.</p>
<h2>Step 2: the driving force (LMTD)</h2>
<p>Heat flows because the steam is hotter than the feed. The difference is not constant along the exchanger, so the design uses the <strong>log mean temperature difference</strong>:</p>
<p>LMTD = (ΔT<sub>1</sub> − ΔT<sub>2</sub>) / ln(ΔT<sub>1</sub> / ΔT<sub>2</sub>)</p>
<p>Steam at 3.0&nbsp;barg condenses at about {T_ST}&nbsp;°C. At the feed inlet the difference is {f1(DT1)}&nbsp;K; at the outlet it is {f1(DT2)}&nbsp;K. The LMTD is <strong>{f1(LMTD)}&nbsp;K</strong>. Because the steam condenses at one temperature, flow direction does not matter and no correction factor is needed. For two liquids, a multi-pass exchanger needs a correction factor, F, applied to the LMTD.</p>
{fig(fig_hx_profile(), 1, "Temperature profiles in E-101. The steam stays at its condensing temperature; the feed approaches it along a curve, so the driving force shrinks toward the outlet.")}
<h2>Step 3: the overall coefficient (U)</h2>
<p>U combines every resistance between the steam and the feed: the condensing film, the tube wall, the liquid film inside the tubes and any fouling. For preliminary sizing, engineers use typical values for the service. For condensing steam heating a light organic liquid in a shell-and-tube exchanger, a few hundred W/m²·K is typical; this example uses <strong>{f0(U_CL)}&nbsp;W/m²·K</strong>. The liquid side controls, so tube velocity matters more than the steam side.</p>
<h2>Step 4: the area</h2>
<p>From Q = U × A × LMTD:</p>
<p>A = {f0(DUTY * 1000)} / ({f0(U_CL)} × {f1(LMTD)}) = <strong>{f2(A_REQ)}&nbsp;m²</strong></p>
<p>Add a margin for fouling and uncertainty in U. With {f0(OVERS * 100)}%, the design area is {f2(A_DES)}&nbsp;m². Margins are better stated as a fouling factor in the U calculation, which makes the reason visible; a flat percentage is acceptable at this stage if the design basis says so.</p>
<h2>Step 5: lay out the tubes</h2>
<p>The area has to fit a geometry that also gives a sensible tube velocity. With ¾" tubes (inside diameter {f1(DI * 1000)}&nbsp;mm) and a target of about {f1(V_TUBE)}&nbsp;m/s, the feed needs {N_PASS_T} tubes per pass. With two tube passes that is {N_TUBES} tubes, and the area requires a tube length of about <strong>{f1(L_TUBE)}&nbsp;m</strong>. A standard length of {math.ceil(L_TUBE * 2) / 2:.1f}&nbsp;m gives a little more area.</p>
<table>
<tr><th>Item</th><th>E-101 value</th></tr>
<tr><td>Type</td><td>Shell and tube; steam in shell, feed in tubes</td></tr>
<tr><td>Duty</td><td>{f0(DUTY)}&nbsp;kW</td></tr>
<tr><td>Steam</td><td>{f0(M_ST)}&nbsp;kg/h at 3.0&nbsp;barg ({T_ST}&nbsp;°C)</td></tr>
<tr><td>Feed in / out</td><td>{f0(T_IN)} / {f0(T_OUT)}&nbsp;°C</td></tr>
<tr><td>LMTD</td><td>{f1(LMTD)}&nbsp;K</td></tr>
<tr><td>U assumed</td><td>{f0(U_CL)}&nbsp;W/m²·K</td></tr>
<tr><td>Area, required / design</td><td>{f2(A_REQ)} / {f2(A_DES)}&nbsp;m²</td></tr>
<tr><td>Tubes</td><td>{N_TUBES} × ¾" OD, 2 passes, {math.ceil(L_TUBE * 2) / 2:.1f}&nbsp;m long</td></tr>
</table>
{fig3d("hx")}<h2>What to check next</h2>
<ul>
<li><strong>Tube-side pressure drop.</strong> {L[1]} allowed 50&nbsp;kPa. At about 1&nbsp;m/s in two short passes the real figure will be well under that; the vendor's rating confirms it.</li>
<li><strong>Control.</strong> Steam flow is controlled by a valve on the steam inlet, as on the <a href="{HAZOP}.html">HAZOP's P&amp;ID</a>. At low load, the shell pressure can fall below the condensate return pressure and the exchanger floods with condensate (stall). The condensate system must be designed for it.</li>
<li><strong>Overpressure.</strong> The tube side runs at about 3.5&nbsp;barg and the shell at 3.0&nbsp;barg. A burst tube would push feed into the shell. Whether that needs a relief device is one of the cases in <a href="{RLF}.html">pressure relief basics</a>.</li>
<li><strong>Rating by the vendor.</strong> Preliminary sizing gives the area and layout to request quotes. The vendor's thermal rating, with actual film coefficients, is what the purchase order is based on.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>Duty first: Q = ṁ c<sub>p</sub> ΔT, and check it against the stream table.</li>
<li>The driving force is the log mean temperature difference, corrected for flow arrangement where needed.</li>
<li>U is the uncertain number. Use typical values to start and state the fouling allowance explicitly.</li>
<li>The area must fit a layout that gives a sensible tube velocity.</li>
</ul>
<p>Next: {L[3]} sizes the feed tank, T-101.</p>
{NOTE}{js3d("hx3d")}"""
    body = nowrap(body, [(1, 0, 26)])
    return dict(slug=Z2, title="Sizing a Heat Exchanger: Duty, LMTD and Area, Worked Step by Step",
                desc="How a shell-and-tube heater is sized: duty, log mean temperature difference, overall coefficient, area and tube layout, on a worked steam heater.",
                cats=["process-engineering"], tags=["heat exchanger sizing", "LMTD", "overall heat transfer coefficient", "shell and tube", "steam heater", "process design"],
                body=body, date=DATE, author="Quak Foo Lee", read="7 min read", series=SER(2), cover_label="Equipment sizing",
                related=[Z1, Z3, HAZOP])


# ───────────────────────── Part 3: tank ─────────────────────────
def part3():
    body = f"""{CSS}
<p>{L[1]} and {L[2]} sized the pump and heater in the feed section. This part sizes the tank they draw from: T-101, an atmospheric storage tank that holds the feed and decouples the reactor from deliveries. A tank seems simple, but its size, its level settings and its wall thickness each come from a different question.</p>
<h2>Step 1: how much holdup?</h2>
<p>Holdup is set by what the tank has to absorb. For a feed tank, the usual questions are: how long must the plant keep running if a delivery is late, how big is a delivery, and how much time do operators need to respond to an alarm. This example takes {f0(HOLD_H)} hours of feed at full rate:</p>
<p>Working volume = {f0(M)}&nbsp;kg/h × {f0(HOLD_H)}&nbsp;h / {f0(RHO)}&nbsp;kg/m³ = <strong>{f1(V_WORK)}&nbsp;m³</strong></p>
<p>Not all of a tank is usable. The bottom is below the pump suction, and the top is reserved for alarms, trips and vapour space. Allowing for {f0(FILL * 100)}% of the total volume to be usable, the tank needs about <strong>{f1(V_TANK)}&nbsp;m³</strong>. If deliveries arrive by tanker, also check that one full delivery fits above the normal level; that can govern instead.</p>
<h2>Step 2: shape</h2>
<p>For a vertical tank, the diameter is often fixed by the space available and the height follows. With a {f1(D_T)}&nbsp;m diameter, the height needed is {f2(H_T)}&nbsp;m, rounded up to a {f1(H_T_SEL)}&nbsp;m shell. A height of one to two diameters is common for tanks of this size.</p>
<h2>Step 3: level settings</h2>
<p>A tank's levels are as much a part of its design as its volume. Each one has a job, and the gaps between them give operators time to act.</p>
{fig(fig_tank(), 1, f"Level settings for T-101. The gaps between levels give time to respond; at {f0(M)}&nbsp;kg/h, each metre of level in this tank is about {f0(math.pi * D_T ** 2 / 4 * RHO / M * 60)} minutes of feed.")}
<table>
<tr><th>Level</th><th>Height</th><th>Purpose</th></tr>
<tr><td>High-high (HHLL)</td><td>{f1(H_T * 0.90)}&nbsp;m</td><td>Trip: closes the inlet valve to prevent overfill</td></tr>
<tr><td>High (HLL)</td><td>{f1(H_T * 0.85)}&nbsp;m</td><td>Alarm: stop filling</td></tr>
<tr><td>Normal (NLL)</td><td>{f1(H_T * 0.55)}&nbsp;m</td><td>Typical operating level</td></tr>
<tr><td>Low (LLL)</td><td>1.2&nbsp;m</td><td>Alarm: arrange a delivery or reduce rate</td></tr>
<tr><td>Low-low (LLLL)</td><td>0.8&nbsp;m</td><td>Trip: stops P-101 before it loses suction</td></tr>
</table>
<p>The low-low trip protects the pump from running dry, and its height must keep enough liquid above the pump for the NPSH calculated in {L[1]}. The high-high trip protects against overfill, which is one of the most common causes of tank incidents. Both are candidates for the independent protection layers examined in a <a href="{HAZOP}.html">HAZOP</a>.</p>
<h2>Step 4: wall thickness</h2>
<p>Atmospheric storage tanks in North America are commonly designed to API 650, which sets the shell thickness of each course from the liquid head it has to hold. The one-foot method gives the required thickness of the bottom course as:</p>
<p>t = 4.9 × D × (H − 0.3) × G / S<sub>d</sub> + CA</p>
<p>with t in mm, D the diameter and H the liquid height in metres, G the specific gravity, S<sub>d</sub> the allowable stress in MPa and CA the corrosion allowance. For T-101, with G = {f2(GS)}, S<sub>d</sub> = {f0(SD)}&nbsp;MPa and a {f1(CA)}&nbsp;mm corrosion allowance:</p>
<p>t = 4.9 × {f1(D_T)} × ({f1(H_T_SEL)} − 0.3) × {f2(GS)} / {f0(SD)} + {f1(CA)} = <strong>{f1(T_SHELL)}&nbsp;mm</strong></p>
<p>That is less than the minimum shell thickness the standard sets for a tank of this diameter, {f0(T_MIN)}&nbsp;mm, so the minimum governs. For small tanks this is usual: the walls are thicker than the liquid pressure needs, for handling, welding and stiffness. Pressure vessels, such as reactor R-101, are designed to a different code, ASME Section VIII, which uses a different formula based on the internal design pressure.</p>
{fig3d("tank")}<h2>What else the tank needs</h2>
<ul>
<li><strong>Venting.</strong> An atmospheric tank breathes as it fills, empties and warms. Vents are sized for normal breathing and for emergency venting in a fire, so the tank is not pressurized or pulled into vacuum.</li>
<li><strong>Containment.</strong> A bund or dike sized to hold the tank's contents, with allowance for rainfall, as local regulations require.</li>
<li><strong>Inerting.</strong> A flammable feed may need a nitrogen blanket so that the vapour space never contains an ignitable mixture.</li>
<li><strong>Nozzles.</strong> Inlet, outlet, drain, vent, level instruments, temperature and a manway, each located and sized on the tank drawing.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>Holdup comes from what the tank must absorb: late deliveries, delivery size and operator response time.</li>
<li>Usable volume is less than total volume; allow for the space below the pump suction and above the high levels.</li>
<li>Level settings are design decisions; the gaps between them buy operators time.</li>
<li>For small atmospheric tanks, the code minimum often sets the wall thickness, not the liquid head.</li>
</ul>
<p>This completes the series. For what protects this equipment if things go wrong, see <a href="{RLF}.html">pressure relief basics</a>.</p>
{NOTE}{js3d("tk3d")}"""
    body = nowrap(body, [(1, 0, 18), (1, 1, 8)])
    return dict(slug=Z3, title="Sizing a Tank: Holdup, Level Settings and Wall Thickness",
                desc="How a process storage tank is sized: holdup from what it must absorb, shape, level alarms and trips, and API 650 shell thickness, on a worked feed tank.",
                cats=["process-engineering"], tags=["tank sizing", "level alarms", "API 650", "storage tank", "holdup", "process design"],
                body=body, date=DATE, author="Quak Foo Lee", read="7 min read", series=SER(3), cover_label="Equipment sizing",
                related=[Z1, Z2, RLF])


# ───────────────────────── Relief article ─────────────────────────
def relief():
    body = f"""{CSS}
<p>A pressure relief valve sits quietly on a vessel for years and may never lift. It is still one of the most important pieces of equipment in a plant, because it is the last line of defence when everything else has failed. Owners and managers see relief valves on every P&amp;ID and in every inspection report. This article explains what they protect against, how engineers decide which scenario sets their size, and where the common mistakes are.</p>
<h2>What a relief device does</h2>
<p>Every pressure vessel has a <strong>maximum allowable working pressure</strong> (MAWP), set by its design code. A relief device opens before the pressure goes much above it, and releases enough fluid to stop the pressure rising further. Codes allow the pressure to rise a little above the MAWP while the device is relieving. That rise is called accumulation, and its limit depends on the case.</p>
{fig(fig_relief(), 1, "Pressure levels for reactor R-101, from normal operation to the allowable accumulation for each case. The relief valve is set at the vessel's MAWP.")}
<table>
<tr><th>Case</th><th>Allowed accumulation above MAWP</th></tr>
<tr><td>Single relief device</td><td>10%</td></tr>
<tr><td>Multiple relief devices</td><td>16%</td></tr>
<tr><td>Fire exposure</td><td>21%</td></tr>
</table>
<p>These are the limits used with the ASME pressure vessel code and API Standard 521, the main guide to relief and depressuring systems for process plants. Your jurisdiction's pressure equipment regulator adopts the code and inspects against it.</p>
{fig3d("psv")}
<h2>What can cause overpressure</h2>
<p>API 521 lists the causes an engineer must consider for each piece of equipment. The main ones:</p>
<table>
<tr><th>Cause</th><th>What happens</th><th>Example in the feed section</th></tr>
<tr><td>Blocked outlet</td><td>A valve closes downstream while a pump or compressor keeps pushing</td><td>Reactor inlet valve closes with P-101 running</td></tr>
<tr><td>Fire</td><td>Heat from a pool fire boils the liquid inside</td><td>Spill fire around R-101 or T-101</td></tr>
<tr><td>Control valve failure</td><td>A valve fails wide open and lets in more than downstream can take</td><td>Steam valve on E-101 fails open</td></tr>
<tr><td>Loss of cooling</td><td>Heat that was being removed stays in</td><td>Jacket cooling fails on R-101</td></tr>
<tr><td>Runaway reaction</td><td>Reaction heat and gas generation accelerate</td><td>See <a href="{RUN}.html">what happens if the cooling fails</a></td></tr>
<tr><td>Tube rupture</td><td>High-pressure fluid enters the low-pressure side of an exchanger</td><td>Feed at 3.5&nbsp;barg into the E-101 steam shell at 3.0&nbsp;barg</td></tr>
<tr><td>Thermal expansion</td><td>Liquid blocked in a line or exchanger is heated and expands</td><td>Feed trapped in E-101 with steam still on; PSV-102 covers it</td></tr>
<tr><td>Utility failure</td><td>Power, air or cooling water fails and several of the above happen together</td><td>Plant-wide power failure</td></tr>
</table>
<p>Not every cause is credible for every item. A tube rupture into a shell whose design pressure is high enough to contain the tube-side pressure, for example, does not need a relief device. API 521 sets criteria for that judgement. The point is that each cause is considered and the reasoning written down, usually in a relief load summary for each device.</p>
<h2>Choosing the governing case</h2>
<p>For each device, the engineer calculates the relief load, in kg/h, for every credible cause. The largest sets the size of the valve. That is the <strong>governing case</strong>. For a vessel full of liquid that can boil, the fire case often governs. Here is the calculation for R-101.</p>
<h3>Fire case for R-101</h3>
<p>R-101 is the {f0(VR)}&nbsp;m³ reactor from the <a href="scale-up-what-changes-from-lab-to-pilot-to-commercial.html">scale-up series</a>, about {f2(DR)}&nbsp;m in diameter. API 521 estimates the heat absorbed from a pool fire, where there is adequate drainage and fire-fighting, as:</p>
<p>Q = 43,200 × F × A<sub>ws</sub><sup>0.82</sup></p>
<p>with Q in watts, A<sub>ws</sub> the wetted surface area in m² (counted up to 7.6&nbsp;m above the fire), and F an environment factor, 1.0 for a bare vessel and lower for insulated ones. At {f0(FILLR * 100)}% full, the wetted area of R-101 is about {f1(A_WET)}&nbsp;m², so the fire heat input is about <strong>{f0(Q_FIRE)}&nbsp;kW</strong>. If all of it boils solvent with a latent heat of {f0(LAT)}&nbsp;kJ/kg, the relief load is about <strong>{f0(W_FIRE)}&nbsp;kg/h</strong> of vapour.</p>
<p>Insulation that stays in place in a fire lowers F and the relief load. Draining the vessel to a safe location, or depressuring it, can also reduce what the relief device has to handle. These are design choices that the relief study should record.</p>
<h3>Why the fire case may not govern</h3>
<p>For R-101, the runaway case may be worse. A runaway reaction generates heat much faster than a fire and may also generate gas, and the vented stream is often a two-phase mixture of liquid and vapour, which needs a much larger device than vapour alone. Sizing for runaway reactions uses specialist methods based on calorimetry data, developed largely through the Design Institute for Emergency Relief Systems. That is why the <a href="{RUN}.html">runaway reaction post</a> treats prevention as the first priority: a relief system sized for a runaway is large, expensive and still a last resort.</p>
<h2>Set pressure and where the relief goes</h2>
<ul>
<li><strong>Set pressure</strong> is normally at or below the MAWP. The gap between the normal operating pressure and the set pressure must be large enough that the valve does not simmer or lift during normal swings. A ratio of operating to set pressure of about 90% or less is a common guide for spring-loaded valves.</li>
<li><strong>Discharge.</strong> Relief from flammable or toxic service goes to a closed system: a knock-out drum, then a flare or a scrubber. Steam or air may vent to a safe location. The discharge piping and its back pressure must be checked, because back pressure changes how much a valve can pass.</li>
<li><strong>Inlet piping.</strong> The pressure loss in the line from the vessel to the valve must be small, typically no more than 3% of the set pressure, or the valve can chatter and fail to relieve.</li>
</ul>
<h2>Common mistakes</h2>
<ol>
<li><strong>The relief study is not updated.</strong> A new pump with a higher shutoff head, a larger control valve or a new feed can create a case the device was never sized for. Every <a href="management-of-change-for-small-plants.html">management of change</a> should ask whether relief loads change.</li>
<li><strong>Isolation valves left closed.</strong> Block valves under relief devices are allowed only with administrative controls, such as car-sealed open. A closed block valve removes the protection entirely.</li>
<li><strong>Thermal relief forgotten.</strong> A small, cheap valve on a line or exchanger that can be blocked in and heated is easy to leave off.</li>
<li><strong>No inspection.</strong> Relief valves must be tested and overhauled at intervals set by the jurisdiction and the service. A valve stuck by corrosion or polymer will not open.</li>
</ol>
<h2>Key points</h2>
<ul>
<li>A relief device is set at or below the vessel's MAWP, and the code allows 10%, 16% or 21% accumulation above it depending on the case.</li>
<li>Every credible cause of overpressure is considered and the largest relief load sets the size: the governing case.</li>
<li>For vessels holding boiling liquids, fire often governs. For reactive systems, a runaway can be far worse and needs specialist methods.</li>
<li>Keep the relief study current through management of change, and keep the devices inspected.</li>
</ul>
<p><strong>Need a relief study reviewed?</strong> Chmltech's process engineers prepare design bases, HAZOPs and relief load summaries for small and mid-sized plants. <a href="../book.html">Book a strategy call</a>.</p>
<p class="oee-note"><em>The vessel and numbers in this article are an illustrative example. Relief systems must be designed by a qualified engineer to the applicable codes and the requirements of your jurisdiction.</em></p>{js3d("psv3d")}"""
    body = nowrap(body, [(1, 0, 26), (2, 0, 20)])
    return dict(slug=RLF, title="Pressure Relief Basics: What a PSV Protects Against and How the Relief Case Is Chosen",
                desc="What a pressure relief valve protects against, the causes of overpressure, how the governing case is chosen, a worked fire case, and common mistakes.",
                cats=["process-engineering"], tags=["pressure relief", "PSV", "API 521", "fire case", "overpressure", "process safety"],
                body=body, date=DATE, author="Quak Foo Lee", read="8 min read", cover_label="Process safety",
                related=[RUN, HAZOP, "management-of-change-for-small-plants"])


if __name__ == "__main__":
    for a in (part1(), part2(), part3(), relief()):
        json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("wrote", a["slug"], len(a["desc"]))
    print(f"Q_R={Q_R:.2f} H={H_TDH:.1f} Pdis={P_DIS/1e5:.2f} Psuc={P_SUC/1e5:.2f} NPSHa={NPSHA:.1f} f={F_D:.4f} Re={RE_D:.0f} v={V_D:.2f} P={P_SHAFT:.2f}kW")
    print(f"duty={DUTY:.0f} LMTD={LMTD:.1f} A={A_REQ:.2f}/{A_DES:.2f} tubes={N_TUBES} L={L_TUBE:.2f} steam={M_ST:.0f}")
    print(f"Vwork={V_WORK:.1f} Vtank={V_TANK:.1f} H={H_T:.2f}->{H_T_SEL} t={T_SHELL:.2f}")
    print(f"DR={DR:.2f} Awet={A_WET:.1f} Q={Q_FIRE:.0f} W={W_FIRE:.0f}")
