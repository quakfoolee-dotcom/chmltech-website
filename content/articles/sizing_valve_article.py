"""Equipment sizing series, Part 4: sizing a control valve (FV-104 on the discharge of P-101).

Uses the fluid, the pump curve and the pressure build-up of Part 1 (sizing_articles.py). All numbers are computed here.

Usage:  python3 content/articles/sizing_valve_article.py
        python3 content/gen/add_article.py sizing-a-control-valve-cv-pressure-drop-and-cavitation
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import (fig3d, js3d, nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, MUTED, LINE, PALE,
                             GREENF, NOTE, G, M, RHO, MU, PV, Q_N, Q_R, darcy, D_DIS, L_DIS, D_SUC, L_SUC, P_R, Z_R, DP_E,
                             DP_CV, DP_MISC, Z_SUC_MIN, H_TDH, V_D, Z1, Z2, Z3, Z4, Z5, RLF, PFDPID, DB, f0, f1, f2, eq, im, mathjs)

DATE = "2026-11-14"
SER4 = {"name": "Equipment sizing series", "part": 4, "of": 5}
P1L = f'<a href="{Z1}.html">Part&nbsp;1</a>'
TAG = "FV-104"

# ───────────────────────── the valve in its system ─────────────────────────
SG = RHO / 1000
SHUT = H_TDH * 1.22                                   # pump shutoff head, as in Part 1, Figure 1
L_UP = 10.0                                           # m of the 60 m discharge line upstream of the valve
P_ATM = 101.325                                       # kPa
N1 = 0.865                                            # Cv equation constant for m3/h and bar
Q_MIN = 3.0                                           # m3/h, minimum controlled flow (start-up and turndown)
CV_R, RANGE = 25.0, 50.0                              # selected valve: rated Cv and rangeability
FL, PC = 0.90, 4100.0                                 # liquid pressure recovery factor (globe); critical pressure, kPa abs


def pump(q): return SHUT - (SHUT - H_TDH) * (q / Q_R) ** 2
def p_suc(q): return RHO * G * Z_SUC_MIN - darcy(q, D_SUC, L_SUC)[3]


def p1(q):
    """Pa(g) at the valve inlet: pump discharge less the strainer, the meter and the pipe upstream of the valve."""
    return p_suc(q) + RHO * G * pump(q) - DP_MISC * (q / Q_R) ** 2 - darcy(q, D_DIS, L_UP)[3]


def p2(q):
    """Pa(g) the valve outlet must hold: reactor pressure, static lift, heater and the rest of the pipe."""
    return P_R + RHO * G * Z_R + DP_E * (q / Q_R) ** 2 + darcy(q, D_DIS, L_DIS - L_UP)[3]


def cv_req(q): return q / (N1 * math.sqrt((p1(q) - p2(q)) / 1e5 / SG))
def travel_eq(cv): return 1 + math.log(cv / CV_R) / math.log(RANGE)
def travel_lin(cv): return cv / CV_R
def cv_eq(x): return CV_R * RANGE ** (x - 1)
def cv_lin(x): return CV_R * x


def flow_at(cv):
    """Flow the system settles at with the valve held at this Cv."""
    lo, hi = 1e-6, 14.0
    for _ in range(60):
        m = (lo + hi) / 2
        if p1(m) - p2(m) > SG * (m / (N1 * cv)) ** 2 * 1e5: lo = m
        else: hi = m
    return (lo + hi) / 2


CASES = [("Minimum", Q_MIN), ("Normal", Q_N), ("Rated", Q_R)]
ROWS = []
for name, q in CASES:
    cv = cv_req(q)
    ROWS.append(dict(name=name, q=q, p1=p1(q) / 1000, p2=p2(q) / 1000, dp=(p1(q) - p2(q)) / 1000, cv=cv, xe=travel_eq(cv), xl=travel_lin(cv)))
RMIN, RNOR, RRAT = ROWS
Q_OPEN = flow_at(CV_R)
FF = 0.96 - 0.28 * math.sqrt(PV / 1000 / PC)


def cav(r):
    p1a = r["p1"] + P_ATM
    return dict(p1a=p1a, pvc=p1a - r["dp"] / FL ** 2, dpch=FL ** 2 * (p1a - FF * PV / 1000))


CRAT, CMIN = cav(RRAT), cav(RMIN)
P_SHUT = (RHO * G * Z_SUC_MIN + RHO * G * SHUT) / 1e5            # barg upstream with the valve shut and the pump running


def fig_installed():
    X = lambda x: 80 + x * 600; Y = lambda q: 250 - q / 12 * 220
    s = f'<rect x="{X(0.2):.1f}" y="{Y(12):.1f}" width="{X(0.8) - X(0.2):.1f}" height="{Y(0) - Y(12):.1f}" fill="{GREENF}" opacity=".7"/>'
    for q in range(0, 13, 2):
        s += f'<line x1="80" y1="{Y(q):.1f}" x2="680" y2="{Y(q):.1f}" stroke="{LINE}"/>' + txt(72, Y(q) + 4, str(q), "end", MUTED, 12)
    for x in range(0, 101, 20):
        s += txt(X(x / 100), 268, f"{x}%", "middle", MUTED, 12)
    s += txt(380, 290, "Valve travel (% open)", "middle", NAVY, 12.5, True) + txt(14, 20, "Flow (m³/h)", fill=NAVY, fs=12.5, bold=True)
    s += txt(X(0.5), Y(12) + 16, "Preferred working range, 20% to 80% open", "middle", GREEND, 12, True)
    xs = [i / 100 for i in range(0, 101)]
    s += '<polyline fill="none" stroke="' + ORANGE + '" stroke-width="2.5" points="' + " ".join(f"{X(x):.1f},{Y(flow_at(max(cv_lin(x), 0.01))):.1f}" for x in xs) + '"/>'
    s += '<polyline fill="none" stroke="' + BLUE + '" stroke-width="2.5" points="' + " ".join(f"{X(x):.1f},{Y(flow_at(cv_eq(x))):.1f}" for x in xs) + '"/>'
    for r, lab, dx, dy, anc in ((RMIN, "Minimum", 10, 16, "start"), (RNOR, "Normal", -12, -8, "end"), (RRAT, "Rated", 10, 14, "start")):
        s += f'<circle cx="{X(r["xe"]):.1f}" cy="{Y(r["q"]):.1f}" r="5.5" fill="{NAVY}"/>' + txt(X(r["xe"]) + dx, Y(r["q"]) + dy, lab, anc, NAVY, 12.5, True)
        s += f'<circle cx="{X(r["xl"]):.1f}" cy="{Y(r["q"]):.1f}" r="4.5" fill="#fff" stroke="{ORANGE}" stroke-width="2"/>'
    s += txt(X(0.30), Y(flow_at(cv_lin(0.30))) - 12, "Linear trim", "end", ORANGE, 12.5, True)
    s += txt(X(0.50), Y(flow_at(cv_eq(0.50))) + 22, "Equal percentage trim", "start", BLUE, 12.5, True)
    return svg(f"Chart of flow against valve travel for a valve with a rated Cv of {CV_R:g} installed in the P-101 system. With linear trim the flow shoots up in the first third of the travel "
               f"and flattens: the minimum flow sits at {f0(RMIN['xl'] * 100)} percent open and the rated flow at {f0(RRAT['xl'] * 100)} percent. With equal percentage trim the flow rises steadily: "
               f"minimum at {f0(RMIN['xe'] * 100)} percent, normal at {f0(RNOR['xe'] * 100)} percent and rated at {f0(RRAT['xe'] * 100)} percent, all inside the preferred range of 20 to 80 percent open.",
               700, 300, s, 600, x0=0)


def part4():
    pct = lambda x: f0(x * 100)
    case_rows = "".join(f'<tr><td>{r["name"]}</td><td class="num">{f2(r["q"])}</td><td class="num">{f0(r["p1"])}</td><td class="num">{f0(r["p2"])}</td>'
                        f'<td class="num">{f0(r["dp"])}</td><td class="num">{f2(r["cv"])}</td></tr>' for r in ROWS)
    trav_rows = "".join(f'<tr><td>{r["name"]}</td><td class="num">{f2(r["cv"])}</td><td class="num">{pct(r["xl"])}%</td><td class="num">{pct(r["xe"])}%</td></tr>' for r in ROWS)
    body = f"""{CSS}
<p>A pump pushes, a heater heats, a tank holds. The control valve is the one piece of equipment in the feed section that makes a decision many times a minute: how much to let through. If it is too big it works barely cracked open and the flow hunts. If it is too small the plant cannot reach its rated flow. If the pressure inside it falls too low the liquid boils in the valve and eats the trim.</p>
<p>{P1L} of this series sized pump P-101 and set aside 120&nbsp;kPa of its head for the flow control valve. This part sizes that valve, called {TAG} here. It sits on the pump discharge, upstream of heater E-101, and holds the feed to reactor R-101 at {f0(M)}&nbsp;kg/h. The steps are the same for any liquid control valve: fix the flows and pressures, calculate the flow coefficient, pick a valve and trim, check for cavitation, and settle the failure position.</p>
<h2>Step 1: fix the flows and the pressures at the valve</h2>
<p>A control valve is sized for a range, not a point. Three cases cover it: the <strong>minimum</strong> flow it must still control, here {f1(Q_MIN)}&nbsp;m³/h for start-up and turndown; the <strong>normal</strong> flow of {f2(Q_N)}&nbsp;m³/h; and the <strong>rated</strong> flow of {f2(Q_R)}&nbsp;m³/h, 10% above normal, the same margin the pump was sized for.</p>
<p>For each case the valve's pressure drop is whatever is left over. The inlet pressure is what the pump delivers at that flow, less the strainer, the flow meter and the short run of pipe before the valve. The outlet pressure is what the rest of the system needs: reactor pressure, static lift, the heater and the remaining pipe.</p>
<table>
<tr><th>Case</th><th class="num">Flow, m³/h</th><th class="num">Inlet P1, kPa(g)</th><th class="num">Outlet P2, kPa(g)</th><th class="num">Valve ΔP, kPa</th><th class="num">Required Cv</th></tr>
{case_rows}
</table>
<p>The pattern matters more than the numbers. At low flow the pump runs back up its curve and delivers more pressure, while the heater and the pipes need less, so the valve must absorb {f0(RMIN["dp"])}&nbsp;kPa. At rated flow it has only {f0(RRAT["dp"])}&nbsp;kPa to work with, the allowance from {P1L}. The valve has to pass the most flow exactly when it has the least pressure drop available.</p>
<h2>Step 2: calculate the flow coefficient</h2>
<p>Valve capacity is expressed as the <strong>flow coefficient, Cv</strong>: the flow of water in US gallons per minute that passes through the valve with a pressure drop of 1&nbsp;psi. For a liquid in turbulent flow, with the flow Q in m³/h, the pressure drop ΔP in bar and the specific gravity SG, the sizing equation of IEC&nbsp;60534 and ISA-75.01 reduces to:</p>
{eq(r"C_v = \dfrac{Q}{0.865\,\sqrt{\dfrac{\Delta P}{\mathrm{SG}}}}")}
<p>At rated flow, with SG&nbsp;=&nbsp;{f2(SG)}:</p>
{eq(r"C_v = \dfrac{%s}{0.865\,\sqrt{\dfrac{%s}{%s}}} = %s" % (f2(Q_R), f2(RRAT["dp"] / 100), f2(SG), f2(RRAT["cv"])))}
<p>The same equation gives {f2(RNOR["cv"])} at normal flow and {f2(RMIN["cv"])} at minimum flow. The valve must cover a Cv range of about {RRAT["cv"] / RMIN["cv"]:.1f} to 1, although the flow range is only {Q_R / Q_MIN:.1f} to 1. The falling pressure drop is the reason.</p>
<p>Two corrections are left out because they do not apply here. The feed is thin ({f2(MU * 1000)}&nbsp;mPa·s), so the flow is fully turbulent and needs no viscosity correction. The valve is the same size as the line, so there are no reducers and no piping geometry factor.</p>
<h2>Step 3: choose the valve and the trim</h2>
<p>The required Cv is not the valve's Cv. A valve is picked so that the largest required Cv falls at about 70% to 80% of its travel and the smallest stays above about 20%. Below that the plug works close to the seat, where control is coarse and wear is fast.</p>
<p>A 1½-inch globe valve, the same size as the line, with a rated Cv of {CV_R:g} is a typical catalogue choice. Its <strong>trim</strong>, the shape of the plug and seat, sets how Cv changes with travel. The two common shapes are:</p>
<ul>
<li><strong>Linear:</strong> Cv rises in proportion to travel. Half open gives half the rated Cv.</li>
<li><strong>Equal percentage:</strong> each step of travel raises Cv by the same percentage. With a rangeability of {RANGE:g} to 1, {im(r"C_v = %g \times %g^{\,(x-1)}" % (CV_R, RANGE))}, where {im("x")} is the travel as a fraction. It opens slowly at first and quickly at the end.</li>
</ul>
<table>
<tr><th>Case</th><th class="num">Required Cv</th><th class="num">Travel, linear trim</th><th class="num">Travel, equal percentage trim</th></tr>
{trav_rows}
</table>
<p>With linear trim the whole operating range is squeezed into the first third of the travel, and the minimum flow sits at {pct(RMIN["xl"])}% open. With equal percentage trim the three cases fall at {pct(RMIN["xe"])}%, {pct(RNOR["xe"])}% and {pct(RRAT["xe"])}% open. The equal percentage trim is selected.</p>
{fig(fig_installed(), 1, f"Flow against valve travel for {TAG} installed in the P-101 system, with a rated Cv of {CV_R:g}. Solid points are the three cases on equal percentage trim; open points are the same cases on linear trim.")}
<p>Figure 1 shows why. What the trim gives on a test bench at constant pressure drop is its <strong>inherent</strong> characteristic. What the plant sees is the <strong>installed</strong> characteristic, after the changing pressure drop has had its say. Here the pressure drop falls as the flow rises, which bends a linear trim into a quick-opening curve and straightens an equal percentage trim into something much closer to a straight line across the working range. A straight installed curve means the flow controller behaves the same at low and high flow. The rule of thumb: when the valve's pressure drop falls by more than about half across the flow range, choose equal percentage. Here it falls from {f0(RMIN["dp"])} to {f0(RRAT["dp"])}&nbsp;kPa.</p>
<p>Fully open, this valve would pass about {f1(Q_OPEN)}&nbsp;m³/h, {f0((Q_OPEN / Q_R - 1) * 100)}% above rated. That is enough reserve. A larger valve would add nothing except a working point closer to the seat.</p>
<h2>Step 4: check for choked flow, cavitation and flashing</h2>
<p>Liquid speeds up to squeeze through the gap between the plug and the seat, and its pressure falls as it does. Just past the seat, at the narrowest point of the jet, the pressure is lower than at the outlet. Then the liquid slows down and part of the pressure comes back. How much comes back is described by the valve's <strong>liquid pressure recovery factor, {im("F_L")}</strong>, about {FL:.2f} for a globe valve. The lowest pressure inside the valve is roughly:</p>
{eq(r"P_{\text{lowest}} = P_1 - \dfrac{\Delta P}{F_L^{\,2}}")}
<p>Compare it with the liquid's vapour pressure, in absolute units:</p>
<ul>
<li><strong>Cavitation:</strong> the lowest pressure dips below the vapour pressure but the outlet pressure is above it. Bubbles form at the seat and collapse a moment later. The collapse is violent: noise like gravel, vibration and pitted trim.</li>
<li><strong>Flashing:</strong> the outlet pressure itself is below the vapour pressure. The bubbles do not collapse, and a mixture of liquid and vapour leaves the valve at high speed and erodes it.</li>
<li><strong>Choked flow:</strong> once the liquid is boiling at the seat, lowering the outlet pressure further passes no more flow. The pressure drop at which this starts is given below, where {im(r"P_v")} is the vapour pressure and {im(r"P_c")} is the liquid's critical pressure.</li>
</ul>
{eq(r"\Delta P_{\text{choked}} = F_L^{\,2}\,\bigl(P_1 - F_F\,P_v\bigr)")}
{eq(r"F_F = 0.96 - 0.28\,\sqrt{\dfrac{P_v}{P_c}}")}
<p>For {TAG} at rated flow, P1 is {f0(RRAT["p1"])}&nbsp;kPa(g), or {f0(CRAT["p1a"])}&nbsp;kPa absolute. The lowest pressure is:</p>
{eq(r"P_{\text{lowest}} = %s - \dfrac{%s}{%.2f^{2}} = %s\ \text{kPa abs}" % (f0(CRAT["p1a"]), f0(RRAT["dp"]), FL, f0(CRAT["pvc"])))}
<p>The feed's vapour pressure at 20&nbsp;°C is {f1(PV / 1000)}&nbsp;kPa. The choked pressure drop is {f0(CRAT["dpch"])}&nbsp;kPa against an actual {f0(RRAT["dp"])}&nbsp;kPa. The minimum flow case is the more demanding one, because the pressure drop is highest: the lowest pressure there is {f0(CMIN["pvc"])}&nbsp;kPa absolute, and the choked pressure drop is {f0(CMIN["dpch"])}&nbsp;kPa against {f0(RMIN["dp"])}&nbsp;kPa. A cold, stable liquid at a modest pressure drop is nowhere near cavitation.</p>
<p>The check earns its place on other services: hot condensate, boiler feed water, light hydrocarbons near their boiling point, and any valve letting down from high pressure to a tank. There the answer can be a different valve style, hardened trim, an anti-cavitation trim that takes the drop in stages, or moving the valve to a point of higher pressure. Damage can begin before the flow chokes, so vendors also quote a cavitation coefficient for each valve, and it should be used for the final check.</p>
<h2>Step 5: settle the failure position and the actuator</h2>
<p>A control valve is moved by an actuator, usually a diaphragm pushed one way by instrument air and the other way by a spring. When the air or the signal is lost, the spring wins. Which way it pushes is a process safety decision, not a purchasing detail.</p>
<p>{TAG} feeds a reactor. Losing the feed is an upset; an uncontrolled feed is a hazard. So the valve is <strong>fail closed</strong>: air opens it, the spring closes it. The same reasoning made the steam valve TV-101 fail closed in <a href="{PFDPID}.html">How to Read a PFD and a P&amp;ID</a>. The actuator must also be strong enough to close and stay closed against the highest pressure it can see. With the valve shut and P-101 still running, that is the pump's shutoff pressure, about {f1(P_SHUT)}&nbsp;barg.</p>
{fig3d("valve")}<h2>The data sheet</h2>
<table>
<tr><th>Item</th><th>{TAG} value</th></tr>
<tr><td>Service</td><td>Reactor feed flow control, P-101 discharge to E-101</td></tr>
<tr><td>Liquid density / viscosity</td><td>{f0(RHO)}&nbsp;kg/m³ / {f2(MU * 1000)}&nbsp;mPa·s at 20&nbsp;°C</td></tr>
<tr><td>Vapour pressure / critical pressure</td><td>{f1(PV / 1000)}&nbsp;kPa abs at 20&nbsp;°C / about {f0(PC / 100)}&nbsp;bar abs</td></tr>
<tr><td>Flow: minimum / normal / rated</td><td>{f1(Q_MIN)} / {f2(Q_N)} / {f2(Q_R)}&nbsp;m³/h</td></tr>
<tr><td>Inlet pressure: minimum / normal / rated</td><td>{f2(RMIN["p1"] / 100)} / {f2(RNOR["p1"] / 100)} / {f2(RRAT["p1"] / 100)}&nbsp;barg</td></tr>
<tr><td>Pressure drop: minimum / normal / rated</td><td>{f0(RMIN["dp"])} / {f0(RNOR["dp"])} / {f0(RRAT["dp"])}&nbsp;kPa</td></tr>
<tr><td>Required Cv: minimum / normal / rated</td><td>{f2(RMIN["cv"])} / {f2(RNOR["cv"])} / {f2(RRAT["cv"])}</td></tr>
<tr><td>Valve</td><td>1½-inch globe, rated Cv {CV_R:g}, equal percentage trim</td></tr>
<tr><td>Travel: minimum / normal / rated</td><td>{pct(RMIN["xe"])}% / {pct(RNOR["xe"])}% / {pct(RRAT["xe"])}% open</td></tr>
<tr><td>Failure position</td><td>Fail closed (air to open)</td></tr>
<tr><td>Shutoff pressure for actuator sizing</td><td>{f1(P_SHUT)}&nbsp;barg</td></tr>
</table>
<p>The vendor returns a sizing sheet with the calculated Cv, the travel, the noise level and the cavitation check for each case, using the real coefficients of the valve offered. The engineer's job is to check that the three cases on that sheet are the same three cases as on the data sheet.</p>
<h2>Common mistakes</h2>
<ul>
<li><strong>Oversizing.</strong> A margin on the flow, another on the pressure drop and then the next valve size up. The result controls the plant from 10% open. Take the margin once, in the rated flow.</li>
<li><strong>Starving the valve of pressure drop.</strong> Cutting the valve's allowance saves pump head on paper and leaves a valve that is wide open with nothing in hand.</li>
<li><strong>Sizing for one case.</strong> The rated case sets the capacity. The minimum case sets the turndown and is usually the worst for cavitation and noise.</li>
<li><strong>Choosing the trim by habit.</strong> Work out how the pressure drop changes across the flow range before choosing linear or equal percentage.</li>
<li><strong>Leaving the failure position to the vendor.</strong> It belongs on the P&amp;ID and comes out of the hazard review.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>Size a control valve for three cases: minimum, normal and rated flow, each with its own pressure drop.</li>
<li>The valve's pressure drop is what the pump delivers less what the system needs. It is highest at low flow and lowest at high flow.</li>
<li>{im(r"C_v = Q \,/\, \bigl(0.865\sqrt{\Delta P / \mathrm{SG}}\bigr)")} for liquids, with Q in m³/h and ΔP in bar.</li>
<li>Pick the rated Cv and the trim so that all three cases sit between about 20% and 80% of travel.</li>
<li>Check the lowest pressure inside the valve against the vapour pressure, and set the failure position from the process hazard.</li>
</ul>
<p>Earlier in this series: {P1L} sized the pump, <a href="{Z2}.html">Part&nbsp;2</a> the heater and <a href="{Z3}.html">Part&nbsp;3</a> the feed tank. Next: <a href="{Z5}.html">Part&nbsp;5</a> sizes the lines that connect them.</p>
{NOTE}{js3d("cv3d")}{mathjs()}"""
    body = nowrap(body, [(1, 0, 10), (2, 0, 10), (3, 0, 40)])
    return dict(slug=Z4, title="Sizing a Control Valve: Cv, Pressure Drop and Cavitation, Worked Step by Step",
                desc="How a liquid control valve is sized: flow cases, pressure drop, Cv, trim and travel, cavitation check and failure position, on a worked example.",
                cats=["process-engineering"], tags=["control valve sizing", "Cv", "flow coefficient", "cavitation", "equal percentage trim", "process design"],
                body=body, date=DATE, author="Quak Foo Lee", read="9 min read", series=SER4, cover_label="Equipment sizing",
                related=[Z1, Z2, PFDPID])


if __name__ == "__main__":
    a = part4()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", a["slug"], len(a["desc"]))
    for r in ROWS: print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
    print(f"Q_open={Q_OPEN:.2f} FF={FF:.3f} rated {CRAT} min {CMIN} Pshut={P_SHUT:.2f} SHUT={SHUT:.2f}")
