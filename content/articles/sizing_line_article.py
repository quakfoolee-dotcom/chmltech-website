"""Equipment sizing series, Part 5: sizing a line (the discharge and suction lines of P-101).

Uses the fluid, the flows and the pipe data of Part 1 (sizing_articles.py). All numbers are computed here.

Usage:  python3 content/articles/sizing_line_article.py
        python3 content/gen/add_article.py sizing-a-line-velocity-pressure-drop-and-pipe-schedule
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import (fig3d, js3d, nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, MUTED, LINE, PALE,
                             GREENF, NOTE, G, M, RHO, MU, Q_N, Q_R, darcy, D_DIS, L_DIS, D_SUC, L_SUC, ETA, Z1, Z2, Z3, PFDPID, DB,
                             f0, f1, f2)
from sizing_articles import eq, im, mathjs, Z4, Z5, Z6
from sizing_valve_article import P_SHUT

DATE = "2026-11-14"
SER5 = {"name": "Equipment sizing series", "part": 5, "of": 7}
P1L = f'<a href="{Z1}.html">Part&nbsp;1</a>'
P4L = f'<a href="{Z4}.html">Part&nbsp;4</a>'
EPS = 0.045                                            # mm, commercial steel

# NPS, DN, outside diameter, schedule 40 wall, schedule 80 wall (mm), ASME B36.10
PIPES = [("1", 25, 33.4, 3.38, 4.55), ("1½", 40, 48.3, 3.68, 5.08), ("2", 50, 60.3, 3.91, 5.54), ("3", 80, 88.9, 5.49, 7.62)]


def line(q, id_mm, length):
    v, re, f, dp = darcy(q, id_mm / 1000, length)
    return dict(v=v, re=re, f=f, dp=dp / 1000)


ROWS = []
for nps, dn, od, t40, t80 in PIPES:
    idm = od - 2 * t40
    r = line(Q_R, idm, 100.0); r.update(nps=nps, dn=dn, od=od, t=t40, id=idm, dpl=r["dp"] * L_DIS / 100, head=r["dp"] * L_DIS / 100 * 1000 / (RHO * G))
    ROWS.append(r)
R1, R15, R2, R3 = ROWS
SUC = line(Q_R, R2["id"], 100.0); SUC_DP = SUC["dp"] * L_SUC / 100
SUC3 = line(Q_R, R3["id"], 100.0)
ID80 = PIPES[1][2] - 2 * PIPES[1][4]; S80 = line(Q_R, ID80, 100.0)

# equivalent length of the discharge line: fittings as length-to-diameter ratios
D15 = R15["id"] / 1000
FITS = [("90° elbows", 10, 30), ("Gate valves, open", 2, 8), ("Check valve", 1, 100), ("Tee, flow through the branch", 1, 60)]
FIT_ROWS = [(n, c, ld, c * ld * D15) for n, c, ld in FITS]
EXIT_L = 1.0 / R15["f"] * D15                         # exit loss, K = 1, as an equivalent length
L_FIT = sum(x[3] for x in FIT_ROWS) + EXIT_L
L_STR = L_DIS - L_FIT

# energy saved by going one size up: 2 in. against 1.5 in.
DP_SAVE = R15["dpl"] - R2["dpl"]
KW_SAVE = Q_R / 3600 * DP_SAVE / ETA
KWH_SAVE = KW_SAVE * 8000

# wall thickness, ASME B31.3 straight pipe under internal pressure
P_DES, S_ALLOW, E_Q, W_F, Y_C, CA, MILL = 1.0, 138.0, 1.0, 1.0, 0.4, 1.5, 0.125     # MPa(g), MPa, -, -, -, mm, -
T_P = P_DES * R15["od"] / (2 * (S_ALLOW * E_Q * W_F + P_DES * Y_C))
T_MIN = (T_P + CA) / (1 - MILL)


def fig_sizes():
    x0, w, ybot, ytop = 90, 590, 262, 42
    lo, hi = math.log10(1), math.log10(3000)
    Y = lambda p: ybot - (math.log10(p) - lo) / (hi - lo) * (ybot - ytop)
    s = f'<rect x="{x0}" y="{Y(90):.1f}" width="{w}" height="{Y(20) - Y(90):.1f}" fill="{GREENF}" opacity=".8"/>'
    for p in (1, 10, 100, 1000):
        s += f'<line x1="{x0}" y1="{Y(p):.1f}" x2="{x0 + w}" y2="{Y(p):.1f}" stroke="{LINE}"/>' + txt(x0 - 8, Y(p) + 4, f"{p:,}", "end", MUTED, 12)
    s += txt(14, 18, "Pressure drop (kPa per 100 m, log scale)", fill=NAVY, fs=12.5, bold=True)
    s += txt(x0 + w - 8, ytop + 16, "Green band: guideline for pump discharge lines,", "end", GREEND, 12, True) + txt(x0 + w - 8, ytop + 32, "20 to 90 kPa per 100 m", "end", GREEND, 12, True)
    bw = 84
    for i, r in enumerate(ROWS):
        cx = x0 + w * (i + 0.5) / len(ROWS); sel = r is R15
        s += f'<rect x="{cx - bw / 2:.1f}" y="{Y(r["dp"]):.1f}" width="{bw}" height="{ybot - Y(r["dp"]):.1f}" rx="4" fill="{BLUE if sel else "#9DB7CC"}"/>'
        s += txt(cx, Y(r["dp"]) - 22, f'{f1(r["dp"]) if r["dp"] < 100 else f0(r["dp"])} kPa', "middle", NAVY, 13, True)
        s += txt(cx, Y(r["dp"]) - 7, f'{f2(r["v"])} m/s', "middle", MUTED, 12)
        s += txt(cx, ybot + 18, f'{r["nps"]} in.', "middle", NAVY, 13, True) + txt(cx, ybot + 34, f'ID {f1(r["id"])} mm', "middle", MUTED, 12)
    s += txt(x0 + w * 1.5 / 4, ybot + 50, "Selected", "middle", BLUE, 12.5, True)
    return svg("Bar chart of pressure drop per 100 metres at the rated flow for four schedule 40 pipe sizes, on a log scale. "
               f"The 1 inch pipe loses {f0(R1['dp'])} kilopascals at {f2(R1['v'])} metres per second, far above the guideline. "
               f"The 1½ inch pipe loses {f0(R15['dp'])} kilopascals at {f2(R15['v'])} metres per second, inside the guideline band of 20 to 90, and is selected. "
               f"The 2 inch pipe loses {f0(R2['dp'])} kilopascals at {f2(R2['v'])} metres per second and the 3 inch pipe {f1(R3['dp'])} kilopascals at {f2(R3['v'])} metres per second.",
               700, 318, s, 600, x0=0)


def part5():
    size_rows = "".join(f'<tr><td>{r["nps"]}&nbsp;in. (DN&nbsp;{r["dn"]})</td><td class="num">{f1(r["id"])}</td><td class="num">{f2(r["v"])}</td><td class="num">{f0(r["re"])}</td>'
                        f'<td class="num">{r["f"]:.4f}</td><td class="num">{f1(r["dp"]) if r["dp"] < 100 else f0(r["dp"])}</td><td class="num">{f1(r["dpl"]) if r["dpl"] < 100 else f0(r["dpl"])}</td></tr>' for r in ROWS)
    fit_rows = "".join(f'<tr><td>{n}</td><td class="num">{c}</td><td class="num">{ld}</td><td class="num">{f1(l)}</td></tr>' for n, c, ld, l in FIT_ROWS)
    body = f"""{CSS}
<p>Pipe is the least glamorous item on a plant and the one there is most of. Each line is a small trade: a thin pipe is cheap to buy and expensive to pump through for the next twenty years, and a fat pipe is the reverse. Line sizing is how that trade is settled, one line at a time, with three numbers: the velocity, the pressure drop and the wall thickness.</p>
<p>{P1L} of this series sized pump P-101 and simply stated that its discharge line was 1½-inch and its suction line 2-inch. This part shows where those sizes come from. The example is the discharge line from P-101 through the control valve of {P4L} and heater E-101 to reactor R-101, carrying {f0(M)}&nbsp;kg/h of feed.</p>
<h2>Step 1: start from the flow and the fluid</h2>
<p>Lines are sized at the same rated flow as the equipment they connect: {f2(Q_R)}&nbsp;m³/h, 10% above the normal {f2(Q_N)}&nbsp;m³/h. The feed has a density of {f0(RHO)}&nbsp;kg/m³ and a viscosity of {f2(MU * 1000)}&nbsp;mPa·s. Those four numbers and a pipe table are all the calculation needs.</p>
<p>One trap comes first. A pipe's nominal size is a name, not a dimension. A 1½-inch schedule&nbsp;40 pipe has an outside diameter of {f1(R15["od"])}&nbsp;mm, a wall of {f2(R15["t"])}&nbsp;mm and an inside diameter of {f1(R15["id"])}&nbsp;mm. The liquid only knows about the inside diameter, so that is the one to use.</p>
<h2>Step 2: set the criteria</h2>
<p>Most companies size liquid lines against two guidelines at once, a velocity range and a pressure drop per 100&nbsp;m of pipe. Typical values for a thin liquid are:</p>
<table>
<tr><th>Service</th><th>Velocity</th><th>Pressure drop</th><th>Why</th></tr>
<tr><td>Pump suction</td><td>0.5 to 1.5&nbsp;m/s</td><td>Under about 10&nbsp;kPa per 100&nbsp;m</td><td>Protects NPSH; every kilopascal lost here is taken from the pump's suction margin</td></tr>
<tr><td>Pump discharge</td><td>1.5 to 3&nbsp;m/s</td><td>20 to 90&nbsp;kPa per 100&nbsp;m</td><td>Balances pipe cost against pump head and energy</td></tr>
<tr><td>Gravity flow and drains</td><td>Under 1&nbsp;m/s</td><td>Set by the head available</td><td>Only the height difference drives the flow</td></tr>
</table>
<p>Too fast, and the line wastes pump head, erodes at elbows, makes noise and hammers when a valve shuts. Too slow, and the plant pays for steel it does not need, and anything that can settle will settle. The ranges are guidelines, not law, and they shift for slurries, corrosive liquids and very large pipe.</p>
<h2>Step 3: try the standard sizes</h2>
<p>Pipe comes in fixed sizes, so the method is trial: take each candidate, work out the velocity, then the pressure drop. Velocity is the flow divided by the bore area:</p>
{eq(r"v = \dfrac{Q}{A} = \dfrac{4Q}{\pi D^{2}}")}
<p>The <strong>Reynolds number</strong> then says what kind of flow it is. Below about 2,100 the flow is laminar and slides in smooth layers. Above about 4,000 it is turbulent and full of eddies. Almost every line carrying a thin liquid in a plant is turbulent.</p>
{eq(r"Re = \dfrac{\rho\, v\, D}{\mu}")}
<p>The <strong>friction factor</strong> {im("f")} depends on the Reynolds number and on the roughness of the pipe wall {im(r"\varepsilon")}, here {EPS:g}&nbsp;mm for commercial steel. For laminar flow it is simply {im(r"f = 64 / Re")}. For turbulent flow the Swamee–Jain equation gives it directly, within a few percent of the Moody chart:</p>
{eq(r"f = \dfrac{0.25}{\left[\log_{10}\!\left(\dfrac{\varepsilon}{3.7\,D} + \dfrac{5.74}{Re^{0.9}}\right)\right]^{2}}")}
<p>The pressure drop over a length {im("L")} then follows from the Darcy–Weisbach equation:</p>
{eq(r"\Delta P = f\,\dfrac{L}{D}\,\dfrac{\rho\, v^{2}}{2}")}
<p>For the 1½-inch pipe: {im(r"v = %s" % f2(R15["v"]))}&nbsp;m/s, {im(r"Re \approx %s" % f0(round(R15["re"], -2)).replace(",", r"{,}"))} and {im(r"f = %.4f" % R15["f"])}, so over 100&nbsp;m:</p>
{eq(r"\Delta P = %.4f \times \dfrac{100}{%.4f} \times \dfrac{%s \times %s^{2}}{2} = %s\ \text{kPa}" % (R15["f"], D15, f0(RHO), f2(R15["v"]), f0(R15["dp"])))}
<p>Repeating that for the neighbouring sizes, all in schedule&nbsp;40:</p>
<table>
<tr><th>Size</th><th class="num">Bore, mm</th><th class="num">Velocity, m/s</th><th class="num">Re</th><th class="num">f</th><th class="num">kPa per 100&nbsp;m</th><th class="num">kPa over line</th></tr>
{size_rows}
</table>
{fig(fig_sizes(), 1, f"Pressure drop per 100 m and velocity at {f2(Q_R)} m³/h for four schedule 40 pipe sizes. Each step down in size multiplies the pressure drop several times.")}
<p>The 1-inch pipe is out at once: {f2(R1["v"])}&nbsp;m/s and {f0(R1["dpl"])}&nbsp;kPa over the line, almost as much as the pump's whole differential pressure. The <strong>1½-inch</strong> pipe meets both guidelines at {f2(R15["v"])}&nbsp;m/s and {f0(R15["dp"])}&nbsp;kPa per 100&nbsp;m. The 2-inch pipe would also work, slowly, and the 3-inch pipe is steel for nothing.</p>
<p>Notice how sharply the pressure drop moves. For the same flow in turbulent conditions it varies roughly with the inverse fifth power of the diameter. Going from 1½ to 1&nbsp;inch cuts the diameter by a third and multiplies the pressure drop by {R1["dp"] / R15["dp"]:.0f}. That is why one size too small is a serious mistake and one size too large is only an expensive one.</p>
<h2>Step 4: count the fittings</h2>
<p>A line is not just straight pipe. Every elbow, tee and valve adds turbulence and loses pressure. The usual shortcut is to convert each fitting to the length of straight pipe that would lose the same pressure, using a length-to-diameter ratio, and add them up. The total is the <strong>equivalent length</strong>, and it goes into the Darcy–Weisbach equation in place of {im("L")}.</p>
<table>
<tr><th>Item, 1½-inch discharge line</th><th class="num">Number</th><th class="num">L/D each</th><th class="num">Equivalent length, m</th></tr>
<tr><td>Straight pipe</td><td class="num"></td><td class="num"></td><td class="num">{f1(L_STR)}</td></tr>
{fit_rows}
<tr><td>Exit into the reactor</td><td class="num">1</td><td class="num">{f0(1.0 / R15["f"])}</td><td class="num">{f1(EXIT_L)}</td></tr>
<tr><td><strong>Equivalent length</strong></td><td class="num"></td><td class="num"></td><td class="num"><strong>{f0(L_DIS)}</strong></td></tr>
</table>
<p>About a third of this line's resistance is fittings, which is typical of the short, crooked runs inside a plant. Over {f0(L_DIS)}&nbsp;m the line loses {f0(R15["dpl"])}&nbsp;kPa, the figure used in the pump's head build-up in {P1L}. The control valve, the heater, the flow meter and the strainer are not fittings in this sense. They have their own pressure drops and were counted separately.</p>
<p>At the layout stage nobody knows the real number of elbows. A common allowance is to add 30% to 100% to the straight length, more for short runs, and to recheck when the piping drawings exist.</p>
<h2>Step 5: size the suction line more gently</h2>
<p>The pump's suction line is sized against the stricter guideline, because pressure lost there comes straight out of the NPSH margin. The usual result is a suction line one size larger than the discharge. Here that is 2-inch: {f2(SUC["v"])}&nbsp;m/s and {f0(SUC["dp"])}&nbsp;kPa per 100&nbsp;m, so the {f0(L_SUC)}&nbsp;m suction line loses only {f1(SUC_DP)}&nbsp;kPa. That is above the 10&nbsp;kPa per 100&nbsp;m guideline, but the line is so short and the NPSH margin in {P1L} so large that the next size up would buy nothing. With a hot or volatile liquid the same check would push it to 3-inch.</p>
<h2>Step 6: check whether a larger pipe pays</h2>
<p>The 2-inch discharge line would save {f0(DP_SAVE)}&nbsp;kPa of pump head. At {f2(Q_R)}&nbsp;m³/h and the pump's {f0(ETA * 100)}% efficiency that is about {KW_SAVE:.2f}&nbsp;kW at the shaft, or roughly {f0(round(KWH_SAVE, -2))}&nbsp;kWh in a year of continuous running. That is a small saving to set against a larger pipe, larger valves and a larger control valve body. For a line this size the 1½-inch choice stands. The balance tips the other way on big flows and long distances, where the energy runs to megawatt-hours and an economic pipe diameter study is worth doing.</p>
<h2>Step 7: choose the schedule</h2>
<p>The <strong>schedule</strong> is the wall thickness. For a given nominal size the outside diameter is fixed, so a heavier schedule means a thicker wall and a smaller bore. The wall has to hold the design pressure. For straight pipe, ASME&nbsp;B31.3 gives the pressure design thickness as:</p>
{eq(r"t = \dfrac{P\,D}{2\,(S\,E\,W + P\,Y)}")}
<p>Here {im("P")} is the design pressure, {im("D")} the outside diameter, {im("S")} the allowable stress of the pipe material, {im("E")} the weld quality factor, {im("W")} the weld strength reduction factor and {im("Y")} a coefficient from the code. The line's design pressure is set at {f0(P_DES * 10)}&nbsp;barg, comfortably above the {f1(P_SHUT)}&nbsp;barg the pump can reach against a closed valve. For seamless carbon steel pipe at ambient temperature, {im("S = %g" % S_ALLOW)}&nbsp;MPa, {im("E = W = 1")} and {im("Y = %g" % Y_C)}:</p>
{eq(r"t = \dfrac{%.1f \times %.1f}{2\,(%g \times 1 \times 1 + %.1f \times %g)} = %.2f\ \text{mm}" % (P_DES, R15["od"], S_ALLOW, P_DES, Y_C, T_P))}
<p>Pressure alone needs a wall of {T_P:.2f}&nbsp;mm. Add a corrosion allowance of {CA:g}&nbsp;mm, then allow for the mill tolerance, since pipe may be delivered up to 12.5% thinner than nominal:</p>
{eq(r"t_{\min} = \dfrac{%.2f + %.1f}{1 - 0.125} = %.2f\ \text{mm}" % (T_P, CA, T_MIN))}
<p>Schedule&nbsp;40 has a wall of {f2(R15["t"])}&nbsp;mm, almost twice what is needed. This is the normal result for small pipe at modest pressure: the wall is chosen for mechanical strength, so that the line survives being stepped on, vibrated and threaded, and the pressure check simply confirms it. In practice the schedule comes from the project's <strong>piping class</strong>, which fixes material, schedule, flange rating and valve types for each service. Many classes call for schedule&nbsp;80 on small threaded or socket-welded lines. That changes the bore: 1½-inch schedule&nbsp;80 has an inside diameter of {f1(ID80)}&nbsp;mm, which raises the velocity to {f2(S80["v"])}&nbsp;m/s and the pressure drop to {f0(S80["dp"])}&nbsp;kPa per 100&nbsp;m. The hydraulics have to be done on the schedule that will actually be bought.</p>
{fig3d("line")}<h2>The line list entry</h2>
<table>
<tr><th>Item</th><th>P-101 discharge line</th></tr>
<tr><td>Line number</td><td>40-P-1002 (DN&nbsp;40, process, line 1002)</td></tr>
<tr><td>From / to</td><td>P-101 discharge / R-101 feed nozzle, via FV-104 and E-101</td></tr>
<tr><td>Fluid</td><td>Reactor feed, liquid, {f0(RHO)}&nbsp;kg/m³, {f2(MU * 1000)}&nbsp;mPa·s</td></tr>
<tr><td>Normal / rated flow</td><td>{f2(Q_N)} / {f2(Q_R)}&nbsp;m³/h</td></tr>
<tr><td>Size and schedule</td><td>1½-inch schedule&nbsp;40, inside diameter {f1(R15["id"])}&nbsp;mm</td></tr>
<tr><td>Velocity at rated flow</td><td>{f2(R15["v"])}&nbsp;m/s</td></tr>
<tr><td>Pressure drop</td><td>{f0(R15["dp"])}&nbsp;kPa per 100&nbsp;m; {f0(R15["dpl"])}&nbsp;kPa over {f0(L_DIS)}&nbsp;m equivalent length</td></tr>
<tr><td>Design pressure</td><td>{f0(P_DES * 10)}&nbsp;barg</td></tr>
<tr><td>Required / selected wall</td><td>{T_MIN:.2f}&nbsp;mm / {f2(R15["t"])}&nbsp;mm</td></tr>
</table>
<p>Every line on the P&amp;ID gets a row like this in the <strong>line list</strong>. The line number ties the row to the drawing, as described in <a href="{PFDPID}.html">How to Read a PFD and a P&amp;ID</a>, and the list is what the piping designers, the stress engineers and the estimators all work from.</p>
<h2>Common mistakes</h2>
<ul>
<li><strong>Using the nominal size as the diameter.</strong> A 1½-inch pipe is not 38&nbsp;mm inside. Use the inside diameter for the schedule chosen.</li>
<li><strong>Forgetting the fittings.</strong> In plant piping they are often a third to a half of the resistance.</li>
<li><strong>Sizing the suction like the discharge.</strong> Suction lines are short, large and gentle for a reason.</li>
<li><strong>Sizing at normal flow.</strong> The line must pass the rated flow, and pressure drop rises almost with the square of the flow.</li>
<li><strong>Applying liquid rules to other flows.</strong> Gases, steam, two-phase mixtures and slurries each have their own criteria and methods.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>Size liquid lines against a velocity range and a pressure drop per 100&nbsp;m, at the rated flow.</li>
<li>Use the inside diameter. Velocity is flow over bore area, and the Reynolds number says whether the flow is laminar or turbulent.</li>
<li>Pressure drop comes from the Darcy–Weisbach equation with the equivalent length, which includes the fittings.</li>
<li>In turbulent flow, pressure drop varies roughly with the inverse fifth power of diameter: one size down is a large step.</li>
<li>Small-bore wall thickness is usually set by the piping class and mechanical strength. The pressure calculation confirms it.</li>
</ul>
<p>Earlier in this series: {P1L} sized the pump, <a href="{Z2}.html">Part&nbsp;2</a> the heater, <a href="{Z3}.html">Part&nbsp;3</a> the feed tank and {P4L} the control valve. Next: <a href="{Z6}.html">Part&nbsp;6</a> sizes the jacket of the reactor this line feeds.</p>
{NOTE}{js3d("ln3d")}{mathjs()}"""
    body = nowrap(body, [(1, 0, 24), (1, 1, 16), (2, 0, 20), (3, 0, 30), (4, 0, 30)])
    return dict(slug=Z5, title="Sizing a Line: Velocity, Pressure Drop and Pipe Schedule, Worked Step by Step",
                desc="How a liquid line is sized: velocity and pressure drop criteria, Reynolds number, friction factor, fittings, suction lines and wall thickness.",
                cats=["process-engineering"], tags=["line sizing", "pipe sizing", "pressure drop", "Reynolds number", "pipe schedule", "process design"],
                body=body, date=DATE, author="Quak Foo Lee", read="10 min read", series=SER5, cover_label="Equipment sizing",
                related=[Z1, Z4, PFDPID])


if __name__ == "__main__":
    a = part5()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", a["slug"], len(a["desc"]))
    for r in ROWS: print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
    print(f"L_str={L_STR:.1f} L_fit={L_FIT:.1f} exit={EXIT_L:.2f} suc={SUC} {SUC_DP:.2f} save={DP_SAVE:.1f} kW={KW_SAVE:.3f} kWh={KWH_SAVE:.0f} t={T_P:.3f} tmin={T_MIN:.2f} id80={ID80:.1f} {S80}")
