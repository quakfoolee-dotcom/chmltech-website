"""Equipment sizing series, Part 7: sizing an agitator (R-101): impeller types, flow patterns and power.

The reactor is the 10,000 L R-101 of the scale-up series and of Part 6 (jacket). All numbers are computed here.

Usage:  python3 content/articles/sizing_agitator_article.py
        python3 content/gen/add_article.py sizing-an-agitator-impeller-types-flow-patterns-and-power
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import (fig3d, js3d, nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, MUTED, LINE, PALE,
                             GREENF, NOTE, Z1, Z2, Z3, Z4, Z5, Z6, Z7, RUN, f0, f1, f2, eq, im, tn, mathjs)
from process_eng_articles import geom, U1

DATE = "2026-11-14"
SER7 = {"name": "Equipment sizing series", "part": 7, "of": 7}

V_B, RHO, MU = 10.0, 1000.0, 0.001                     # m3, kg/m3, Pa.s (thin liquid)
T_D = geom(V_B)[0]                                      # tank diameter, liquid depth = diameter
D_I = 0.88                                              # impeller diameter, m
RPM = 84.0; N = RPM / 60
# turbulent power number, flow number
IMP = [("Pitched blade turbine", 1.27, 0.79), ("Hydrofoil", 0.30, 0.56), ("Rushton turbine", 5.0, 0.72)]
RE = RHO * N * D_I ** 2 / MU


def run(np_, nq, n):
    p = np_ * RHO * n ** 3 * D_I ** 5 / 1000            # kW
    q = nq * n * D_I ** 3                               # m3/s
    ntheta = 5.2 / np_ ** (1 / 3) * (T_D / D_I) ** 2    # turbulent blend time correlation
    return dict(n=n, rpm=n * 60, p=p, pv=p / V_B, q=q, turn=V_B / q, tip=math.pi * D_I * n, blend=ntheta / n)


BASE = run(IMP[0][1], IMP[0][2], N)
ROWS = []
for name, np_, nq in IMP:
    n = (BASE["p"] * 1000 / (np_ * RHO * D_I ** 5)) ** (1 / 3)      # speed for the same power
    r = run(np_, nq, n); r.update(name=name, np=np_, nq=nq); ROWS.append(r)
PBT, HYD, RUS = ROWS
P_DOUBLE = (1.2 ** 3 - 1) * 100
MOTOR = next(m for m in (1.5, 2.2, 3.0, 4.0, 5.5) if m >= BASE["p"] / 0.85 * 1.2)


def fig_patterns():
    s = f'<defs><marker id="fa" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker></defs>'
    titles = ["Axial flow", "Radial flow", "Tangential flow"]; subs = ["Pitched blade turbine, hydrofoil", "Rushton turbine", "Anchor, or any impeller without baffles"]
    for k in range(3):
        x0 = 30 + k * 230; w, h, top = 170, 190, 44; cx = x0 + w / 2
        s += txt(cx, 20, titles[k], "middle", NAVY, 13.5, True) + txt(cx, 36, subs[k], "middle", MUTED, 11.5)
        s += f'<path d="M{x0},{top} L{x0},{top + h - 30} Q{x0},{top + h} {cx},{top + h} Q{x0 + w},{top + h} {x0 + w},{top + h - 30} L{x0 + w},{top}" fill="{PALE}" stroke="{NAVY}" stroke-width="2"/>'
        s += f'<line x1="{x0}" y1="{top + 18}" x2="{x0 + w}" y2="{top + 18}" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="5 3"/>'
        s += f'<line x1="{cx}" y1="{top - 4}" x2="{cx}" y2="{top + (160 if k == 2 else 132)}" stroke="{NAVY}" stroke-width="3"/>'
        A = f'fill="none" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#fa)"'
        if k == 0:
            s += f'<path d="M{cx - 26},{top + 126} L{cx + 26},{top + 138}" stroke="{NAVY}" stroke-width="5"/>'
            for sg in (-1, 1):
                ex = cx + sg * 44
                s += f'<path d="M{cx + sg * 14},{top + 40} L{cx + sg * 14},{top + 150} Q{cx + sg * 16},{top + 172} {ex + sg * 14},{top + 170} Q{ex + sg * 30},{top + 166} {ex + sg * 30},{top + 140} L{ex + sg * 30},{top + 50} Q{ex + sg * 28},{top + 32} {cx + sg * 30},{top + 32}" {A}/>'
        elif k == 1:
            s += f'<line x1="{cx - 28}" y1="{top + 132}" x2="{cx + 28}" y2="{top + 132}" stroke="{NAVY}" stroke-width="3"/>'
            s += f'<rect x="{cx - 30}" y="{top + 124}" width="6" height="16" fill="{NAVY}"/><rect x="{cx + 24}" y="{top + 124}" width="6" height="16" fill="{NAVY}"/>'
            for sg in (-1, 1):
                s += f'<path d="M{cx + sg * 34},{top + 128} L{cx + sg * 66},{top + 128} Q{cx + sg * 76},{top + 126} {cx + sg * 76},{top + 110} L{cx + sg * 76},{top + 52} Q{cx + sg * 74},{top + 34} {cx + sg * 40},{top + 34} Q{cx + sg * 14},{top + 36} {cx + sg * 14},{top + 60} L{cx + sg * 14},{top + 112}" {A}/>'
                s += f'<path d="M{cx + sg * 34},{top + 137} L{cx + sg * 64},{top + 137} Q{cx + sg * 74},{top + 140} {cx + sg * 70},{top + 156} Q{cx + sg * 52},{top + 178} {cx + sg * 24},{top + 174} Q{cx + sg * 12},{top + 168} {cx + sg * 13},{top + 150}" {A}/>'
        else:
            s += f'<path d="M{cx - 72},{top + 50} L{cx - 72},{top + 150} Q{cx - 70},{top + 178} {cx},{top + 180} Q{cx + 70},{top + 178} {cx + 72},{top + 150} L{cx + 72},{top + 50}" fill="none" stroke="{NAVY}" stroke-width="5"/>'
            for yy in (70, 100, 130):
                s += f'<path d="M{cx - 52},{top + yy} Q{cx},{top + yy + 22} {cx + 52},{top + yy}" {A}/>'
                s += f'<path d="M{cx + 52},{top + yy - 4} Q{cx},{top + yy - 22} {cx - 52},{top + yy - 4}" fill="none" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="4 3"/>'
    return svg("Three sketches of a stirred tank seen from the side. Axial flow: the impeller pushes liquid down the centre, and it returns up the wall in one loop on each side. "
               "Radial flow: the impeller throws liquid sideways to the wall, where it splits into one loop above the impeller and one below. "
               "Tangential flow: the liquid goes round with the impeller, with little movement between top and bottom.", 720, 250, s, 600, x0=0)


def part7():
    rows = "".join(f'<tr><td>{r["name"]}</td><td class="num">{r["np"]:g}</td><td class="num">{f0(r["rpm"])}</td><td class="num">{f1(r["tip"])}</td><td class="num">{f2(r["q"])}</td><td class="num">{f0(r["turn"])}</td><td class="num">{f0(r["blend"])}</td></tr>' for r in ROWS)
    body = f"""{CSS}
<p>Two reactors with the same volume, the same motor and the same recipe can behave quite differently, and the reason is often the shape of a piece of metal on the end of the shaft. The impeller decides where the liquid goes: straight down, out to the wall, or simply round and round. That pattern decides how fast a reactant is blended in, whether solids stay off the bottom, and how well the jacket of <a href="{Z6}.html">Part&nbsp;6</a> can take heat out.</p>
<p>This part chooses and sizes the agitator for reactor R-101, the 10,000&nbsp;L vessel of the <a href="{U1}.html">scale-up series</a>. It is {f2(T_D)}&nbsp;m across, with the liquid as deep as it is wide.</p>
<h2>Step 1: state what the agitator is for</h2>
<p>"Mixing" covers several different jobs, and an impeller that is good at one can be poor at another.</p>
<table>
<tr><th>Duty</th><th>What matters</th><th>Typical choice</th></tr>
<tr><td>Blending thin liquids</td><td>Moving the whole contents round quickly: flow</td><td>Hydrofoil or pitched blade turbine</td></tr>
<tr><td>Suspending solids</td><td>Flow sweeping the bottom</td><td>Hydrofoil or pitched blade, pumping down</td></tr>
<tr><td>Dispersing gas, or one liquid in another</td><td>Intense turbulence near the impeller: shear</td><td>Rushton turbine or a concave-blade disc turbine</td></tr>
<tr><td>Heat transfer to a jacket</td><td>Liquid moving fast along the wall</td><td>Any turbine in thin liquids. Anchor or helical ribbon in thick ones</td></tr>
<tr><td>Blending thick liquids</td><td>Reaching every part of the vessel</td><td>Helical ribbon or anchor, close to the wall</td></tr>
</table>
<p>R-101 has two jobs: blend the reactant in as it is added, so that it reacts instead of building up, and keep the liquid moving past the wall so the jacket can remove the heat. Both are flow duties in a thin liquid.</p>
<h2>Step 2: know the three flow patterns</h2>
<p>Every impeller produces one of three basic patterns, or a mixture of them.</p>
{fig(fig_patterns(), 1, "The three basic flow patterns in a stirred tank, seen from the side.")}
<ul>
<li><strong>Axial flow.</strong> The blades are angled, like a propeller, and push the liquid along the shaft, usually downward. It sweeps the bottom, turns outward, rises along the wall and returns down the middle: one large loop on each side. This moves the most liquid for the least power.</li>
<li><strong>Radial flow.</strong> The blades are flat and vertical and throw the liquid sideways as a jet. The jet hits the wall and splits, giving one loop above the impeller and one below. The jet is highly turbulent, which is what breaks up bubbles and droplets, but the two loops exchange liquid slowly.</li>
<li><strong>Tangential flow.</strong> The liquid simply goes round with the impeller. Little moves from top to bottom. This is what an anchor produces, and what any impeller produces in a tank with no baffles.</li>
</ul>
<h2>Step 3: fit baffles</h2>
<p>In a plain round tank a turbine sets a thin liquid spinning as one body. The surface dips into a vortex, the impeller is turning in liquid that is already moving with it, and very little mixing happens. Four flat <strong>baffles</strong> on the wall, each about a twelfth of the tank diameter wide, stop the spin and turn it into the top-to-bottom circulation of Figure&nbsp;1. For R-101 that is four baffles about {f0(T_D / 12 * 1000)}&nbsp;mm wide. Baffles are left out only in thick liquids, where they do no good and leave dead corners.</p>
<h2>Step 4: check the flow regime</h2>
<p>As in a pipe, a Reynolds number tells whether the flow is turbulent or laminar. For an impeller of diameter {im("D")} turning at {im("N")} revolutions per second:</p>
{eq(r"Re = \dfrac{\rho\, N\, D^{2}}{\mu}")}
<p>Above about 10,000 the tank is fully turbulent. Below about 10 it is laminar. R-101 has a pitched blade turbine {f2(D_I)}&nbsp;m across, a little over a third of the tank diameter, turning at {f0(RPM)}&nbsp;rpm, which is {f1(N)} revolutions per second. With a density of {tn(f0(RHO)).replace("{,}", ",")}&nbsp;kg/m³ and a viscosity of {f0(MU * 1000)}&nbsp;mPa·s:</p>
{eq(r"Re = \dfrac{%s \times %s \times %s^{2}}{%s} \approx %s" % (tn(f0(RHO)), f1(N), f2(D_I), f"{MU:g}", tn(f0(round(RE, -4)))))}
<p>That is far into the turbulent range, as it will be for any water-like liquid in a plant-sized vessel.</p>
<h2>Step 5: calculate power and pumping</h2>
<p>Each impeller shape has two numbers that stay constant in turbulent flow. The <strong>power number</strong> {im("N_p")} gives the power it draws and the <strong>flow number</strong> {im("N_q")} gives the liquid it pumps:</p>
{eq(r"P = N_p\, \rho\, N^{3} D^{5} \qquad\qquad Q = N_q\, N\, D^{3}")}
<p>For the pitched blade turbine, {im("N_p = %s" % IMP[0][1])} and {im("N_q = %s" % IMP[0][2])}:</p>
{eq(r"P = %s \times %s \times %s^{3} \times %s^{5} = %s\ \text{W} \approx %s\ \text{kW}" % (IMP[0][1], tn(f0(RHO)), f1(N), f2(D_I), tn(f0(round(BASE["p"] * 1000, -1))), f2(BASE["p"])))}
{eq(r"Q = %s \times %s \times %s^{3} = %s\ \text{m}^3/\text{s}" % (IMP[0][2], f1(N), f2(D_I), f2(BASE["q"])))}
<p>The power is {f2(BASE["pv"])}&nbsp;kW for each cubic metre, a moderate level of agitation. The impeller pumps the whole {f0(V_B)}&nbsp;m³ batch through itself every {f0(BASE["turn"])}&nbsp;seconds. The blade tips move at {f1(BASE["tip"])}&nbsp;m/s. Allowing for the gearbox and seal and a margin, a {MOTOR:g}&nbsp;kW motor is a reasonable selection.</p>
<p>The exponents carry the warnings. Power goes with the cube of speed and the fifth power of diameter. Running 20% faster needs {f0(P_DOUBLE)}% more power. That is why agitators are usually tuned by changing the diameter a little, not by fitting a bigger motor.</p>
<h2>Step 6: estimate the blend time</h2>
<p>For a thin liquid in a baffled tank, the time to blend an addition to within 5% of uniform is well described by one correlation, with {im("T")} the tank diameter:</p>
{eq(r"N\,\theta = \dfrac{5.2}{N_p^{1/3}} \left(\dfrac{T}{D}\right)^{2}")}
<p>For R-101 this gives a blend time {im(r"\theta")} of about <strong>{f0(BASE["blend"])}&nbsp;seconds</strong>. The reactant is added over three hours, so each drop is mixed in almost at once compared with the time it takes to add. That is the condition for the heat release to follow the feed, which the runaway assessment in <a href="{RUN}.html">What Happens If the Cooling Fails</a> depends on.</p>
<h2>Step 7: compare the impellers</h2>
<p>The fair comparison is at the same power in the same tank. Each impeller, {f2(D_I)}&nbsp;m across, is run at the speed that draws {f2(BASE["p"])}&nbsp;kW:</p>
<table>
<tr><th>Impeller</th><th class="num">Np</th><th class="num">rpm</th><th class="num">Tip, m/s</th><th class="num">Pumping, m³/s</th><th class="num">Turnover, s</th><th class="num">Blend, s</th></tr>
{rows}
</table>
<p>Three things stand out. The hydrofoil pumps about twice what the Rushton turbine does for the same power, which is why it is the modern choice for blending and solids suspension. The Rushton turbine spends its power in a slow, wide blade that tears at the liquid, which is why it is used for gas dispersion. And the blend time is the same for all three. In turbulent flow, at the same power and the same diameter, the impeller type does not change how long blending takes. It changes where the energy goes on the way.</p>
<p>For R-101 the pitched blade turbine is a sound choice: good flow down the centre and up the wall, where the jacket is, at a modest tip speed. A hydrofoil would do the same job at a higher speed and lower torque, which means a smaller gearbox.</p>
<h2>Step 8: when the liquid is thick</h2>
<p>Everything above assumes a thin liquid. As viscosity rises the Reynolds number falls, and below a few hundred a turbine stops reaching the wall. It stirs a pocket of liquid around itself, called a cavern, while the rest of the batch sits still. More speed makes the cavern a little larger and the power bill much larger.</p>
<p>The answer is a different impeller. An <strong>anchor</strong> sweeps close to the wall, which keeps the heat transfer surface moving, but it mixes poorly from top to bottom. A <strong>helical ribbon</strong> also lifts the liquid at the wall and returns it down the centre, and is the standard for thick liquids. Both turn slowly and nearly fill the tank. A process whose viscosity climbs during the batch, such as a polymerisation, has to be designed for the end of the batch, not the start.</p>
{fig3d("agitator")}<h2>The data sheet</h2>
<table>
<tr><th>Item</th><th>R-101 agitator</th></tr>
<tr><td>Vessel</td><td>{f0(V_B * 1000)}&nbsp;L batch, {f2(T_D)}&nbsp;m diameter, liquid depth {f2(T_D)}&nbsp;m, four baffles {f0(T_D / 12 * 1000)}&nbsp;mm wide</td></tr>
<tr><td>Liquid</td><td>{tn(f0(RHO)).replace("{,}", ",")}&nbsp;kg/m³, {f0(MU * 1000)}&nbsp;mPa·s</td></tr>
<tr><td>Duty</td><td>Blend the addition, heat transfer to the jacket</td></tr>
<tr><td>Impeller</td><td>Pitched blade turbine, four blades at 45°, pumping down, {f2(D_I)}&nbsp;m diameter</td></tr>
<tr><td>Speed / tip speed</td><td>{f0(RPM)}&nbsp;rpm / {f1(BASE["tip"])}&nbsp;m/s</td></tr>
<tr><td>Reynolds number</td><td>About {tn(f0(round(RE, -4))).replace("{,}", ",")} (turbulent)</td></tr>
<tr><td>Power / power per volume</td><td>{f2(BASE["p"])}&nbsp;kW / {f2(BASE["pv"])}&nbsp;kW/m³</td></tr>
<tr><td>Pumping rate / turnover</td><td>{f2(BASE["q"])}&nbsp;m³/s / {f0(BASE["turn"])}&nbsp;s</td></tr>
<tr><td>Blend time</td><td>About {f0(BASE["blend"])}&nbsp;s</td></tr>
<tr><td>Motor</td><td>{MOTOR:g}&nbsp;kW</td></tr>
</table>
<h2>Common mistakes</h2>
<ul>
<li><strong>Choosing the impeller before the duty.</strong> Decide whether the job needs flow or shear first.</li>
<li><strong>Leaving out the baffles.</strong> A swirling tank with a vortex looks busy and mixes badly.</li>
<li><strong>Scaling up at constant speed.</strong> The same rpm in a tank ten times wider is a vast increase in power. Scale-up holds something else constant, such as power per volume or tip speed, and the choice depends on the duty.</li>
<li><strong>Trusting a turbine in a thick liquid.</strong> Check the Reynolds number at the highest viscosity in the batch.</li>
<li><strong>Forgetting the liquid level.</strong> During a fed batch the level rises past the impeller. Tall vessels need a second impeller higher on the shaft.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>Impellers give axial, radial or tangential flow. Axial moves the most liquid, radial gives the most shear, tangential mixes least.</li>
<li>Baffles turn swirl into top-to-bottom circulation in thin liquids.</li>
<li>{im(r"P = N_p \rho N^3 D^5")} and {im(r"Q = N_q N D^3")}, with {im("N_p")} and {im("N_q")} constant for each impeller in turbulent flow.</li>
<li>At the same power and diameter, turbulent blend time is the same for every impeller. Pumping and shear are what differ.</li>
<li>In thick liquids a turbine stirs only a cavern. Use an anchor or a helical ribbon.</li>
</ul>
<p>Earlier in this series: <a href="{Z1}.html">Part&nbsp;1</a> sized the pump, <a href="{Z2}.html">Part&nbsp;2</a> the heater, <a href="{Z3}.html">Part&nbsp;3</a> the feed tank, <a href="{Z4}.html">Part&nbsp;4</a> the control valve, <a href="{Z5}.html">Part&nbsp;5</a> the lines and <a href="{Z6}.html">Part&nbsp;6</a> the reactor jacket. This completes the series.</p>
{NOTE}{js3d("ag3d")}{mathjs()}"""
    body = nowrap(body, [(3, 0, 30)])
    return dict(slug=Z7, title="Sizing an Agitator: Impeller Types, Flow Patterns and Power",
                desc="How a reactor agitator is chosen and sized: axial, radial and tangential flow, baffles, Reynolds number, power, pumping and blend time.",
                cats=["process-engineering"], tags=["agitator sizing", "impeller types", "flow pattern", "power number", "blend time", "process design"],
                body=body, date=DATE, author="Quak Foo Lee", read="10 min read", series=SER7, cover_label="Equipment sizing",
                related=[Z6, U1, RUN])


if __name__ == "__main__":
    a = part7()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} {len(a['desc'])}\nRe={RE:.0f} base={ {k: round(v, 3) for k, v in BASE.items()} } motor={MOTOR}\n" + "\n".join(str({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()}) for r in ROWS) + "\n")
