"""Equipment sizing series, Part 6: sizing a reactor jacket (R-101, the 10,000 L reactor of the scale-up series).

The reactor, the reaction heat and the jacket duty are the ones in process_eng_articles.py (scale-up series) and the
runaway article: 10 m3 batch, 150 kJ/kg, added over three hours, U = 300 W/m2.K and a 30 K mean difference for the
plain jacket. All numbers are computed here.

Usage:  python3 content/articles/sizing_jacket_article.py
        python3 content/gen/add_article.py sizing-a-reactor-jacket-jacket-types-area-and-cooling-capacity
        python3 content/gen/series_labels.py
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import (fig3d, js3d, nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, MUTED, LINE, PALE,
                             GREENF, NOTE, Z1, Z2, Z3, Z4, Z5, Z6, Z7, RLF, RUN, PFDPID, f0, f1, f2, eq, im, tn, mathjs)
from process_eng_articles import geom, U1, U3

DATE = "2026-11-14"
SER6 = {"name": "Equipment sizing series", "part": 6, "of": 7}

# ───────────────────────── reactor and duty (scale-up series) ─────────────────────────
V_B, M_B, CP_B, DH = 10.0, 10000.0, 2.0, 150.0          # m3, kg, kJ/kg.K, kJ/kg of batch
D_R, A_J, _, _ = geom(V_B)                               # diameter m (liquid depth = diameter), wetted wall area m2
T_B, T_BOIL = 60.0, 110.0                                # process temperature, boiling point (runaway article)
Q_RXN = M_B * DH / 1e6                                   # GJ per batch
T_ADD = 3.0                                              # h, addition time
Q_GEN = M_B * DH / (T_ADD * 3600)                        # kW average over the addition
# cooling water
T_IN, T_OUT, CP_W = 25.0, 34.5, 4.18
DT1, DT2 = T_B - T_IN, T_B - T_OUT
LMTD = (DT1 - DT2) / math.log(DT1 / DT2)
# thermal resistances, m2.K/W
H_I = 800.0                                              # process side, agitated organic liquid
WALL_T, WALL_K = 0.012, 16.0                             # 12 mm stainless steel
R_WALL = WALL_T / WALL_K
R_FOUL = 1 / 300.0 - 1 / H_I - R_WALL - 1 / 1000.0       # both sides together; set so the plain jacket gives the series' 300 W/m2.K
JACKETS = [("Plain jacket", 1000.0, 0.3), ("Dimple jacket", 2500.0, 0.9), ("Half-pipe coil jacket", 5000.0, 1.6)]   # name, jacket-side coefficient, water velocity m/s


def u_of(hj): return 1 / (1 / H_I + R_WALL + R_FOUL + 1 / hj)


W_FLOW = 300.0 * A_J * LMTD / 1000 / (CP_W * (T_OUT - T_IN)) * 3.6      # m3/h of cooling water, from the plain jacket's duty
MCP = W_FLOW / 3.6 * CP_W                                # kW/K


def cap(ua):
    """kW removed at the process temperature with the design water flow: the water warms more as UA (W/K) rises."""
    return MCP * (1 - math.exp(-ua / 1000 / MCP)) * (T_B - T_IN)


ROWS = []
for name, hj, vel in JACKETS:
    u = u_of(hj); q = cap(u * A_J)
    ROWS.append(dict(name=name, hj=hj, vel=vel, u=u, q=q, t=Q_RXN * 1e6 / q / 3600, out=T_IN + q / MCP))
PLAIN, DIMPLE, HALF = ROWS
# internal coil: 2 in. pipe, 9 turns of 1.6 m diameter
C_OD, C_DIA, C_TURNS, C_WALL = 0.0603, 1.6, 9, 0.0039
A_C = math.pi * C_OD * math.pi * C_DIA * C_TURNS
U_C = 1 / (1 / H_I + C_WALL / WALL_K + R_FOUL + 1 / 5000.0)
Q_PC = cap(PLAIN["u"] * A_J + U_C * A_C); T_PC = Q_RXN * 1e6 / Q_PC / 3600      # water shared between jacket and coil
Q_HC = cap(HALF["u"] * A_J + U_C * A_C); T_HC = Q_RXN * 1e6 / Q_HC / 3600
Q_C = Q_PC - PLAIN["q"]
Q_1H = M_B * DH / 3600                                   # kW if added in one hour
RISE_1H = (Q_1H - PLAIN["q"]) / (M_B * CP_B / 3600)      # K per hour with the plain jacket


def fig_resist():
    x0, w, bh = 190, 380, 34
    tot = max(1 / r["u"] for r in ROWS); X = lambda r: r / tot * w
    cols = [(BLUE, "Batch side film"), ("#7FB2CF", "Vessel wall"), ("#B9C4CF", "Fouling"), (ORANGE, "Jacket side film")]
    s = ""
    for i, (c, lab) in enumerate(cols):
        s += f'<rect x="{x0 + i * 132}" y="14" width="14" height="14" rx="2" fill="{c}"/>' + txt(x0 + i * 132 + 20, 26, lab, fill=NAVY, fs=12)
    for k, r in enumerate(ROWS):
        y = 52 + k * 58; x = x0
        s += txt(x0 - 12, y + bh / 2 + 4, r["name"], "end", NAVY, 12.5, True)
        for (c, _), val in zip(cols, (1 / H_I, R_WALL, R_FOUL, 1 / r["hj"])):
            s += f'<rect x="{x:.1f}" y="{y}" width="{X(val):.1f}" height="{bh}" fill="{c}"/>'
            if X(val) > 34: s += txt(x + X(val) / 2, y + bh / 2 + 4, f"{val / (1 / r['u']) * 100:.0f}%", "middle", "#fff", 12, True)
            x += X(val)
        s += txt(x + 10, y + bh / 2 + 4, f'U = {f0(r["u"])} W/m²·K', fill=NAVY, fs=12.5, bold=True)
    s += txt(x0, 52 + 3 * 58 + 6, "Total resistance to heat flow (shorter is better)", fill=MUTED, fs=12)
    return svg("Stacked bars of the resistance to heat flow for three jacket types on reactor R-101. The batch side film, the vessel wall and fouling are the same in each. "
               f"The jacket side film is {1 / PLAIN['hj'] * PLAIN['u'] * 100:.0f} percent of the total for the plain jacket, {1 / DIMPLE['hj'] * DIMPLE['u'] * 100:.0f} percent for the dimple jacket and "
               f"{1 / HALF['hj'] * HALF['u'] * 100:.0f} percent for the half-pipe jacket, so the overall coefficient rises from {f0(PLAIN['u'])} to {f0(DIMPLE['u'])} and {f0(HALF['u'])} watts per square metre kelvin.",
               720, 240, s, 600, x0=0)


def part6():
    jrows = "".join(f'<tr><td>{r["name"]}</td><td class="num">{f0(r["hj"])}</td><td class="num">{f0(r["u"])}</td><td class="num">{f0(r["q"])}</td><td class="num">{f1(r["t"])}</td></tr>' for r in ROWS)
    body = f"""{CSS}
<p>A stirred reactor is a pot with a lid until the reaction starts giving off heat. From then on it is a heat exchanger with a very awkward shape, and the jacket around it decides how fast the plant can run. The <a href="{U1}.html">scale-up series</a> showed that the 10,000&nbsp;L reactor R-101 has so little wall for its volume that a one-hour laboratory reaction has to be stretched to about three hours. This part of the sizing series looks at what can be done about that: which kinds of jacket exist, how to calculate what each can remove, and when a jacket is not enough.</p>
<h2>Step 1: state the duty</h2>
<p>A reactor jacket usually has three jobs in every batch: heat the charge to reaction temperature, remove the heat of reaction, and cool the product down afterwards. The energy balance in <a href="{U3}.html">From Pilot Data to a Mass and Energy Balance</a> sets them out for R-101. The one that fixes the jacket is the heat of reaction, because it cannot be made to wait.</p>
<p>R-101 holds a {f0(M_B)}&nbsp;kg batch that releases {f0(DH)}&nbsp;kJ/kg, or {f1(Q_RXN)}&nbsp;GJ in all. One reactant is added over {f0(T_ADD)} hours and reacts almost as it arrives, so the heat appears at an average rate of:</p>
{eq(r"Q_{\text{gen}} = \dfrac{%s\ \text{kg} \times %s\ \text{kJ/kg}}{%s\ \text{h} \times 3{,}600\ \text{s/h}} = %s\ \text{kW}" % (tn(f0(M_B)), f0(DH), f0(T_ADD), f0(Q_GEN)))}
<p>The batch is held at {f0(T_B)}&nbsp;°C. Cooling water enters the jacket at {f0(T_IN)}&nbsp;°C. The jacket must remove at least {f0(Q_GEN)}&nbsp;kW across that temperature difference, with something in hand.</p>
<h2>Step 2: know the jacket types</h2>
<p>There are three common ways to wrap a heating or cooling fluid around a vessel, and two ways to add area when the wall is not enough.</p>
<table>
<tr><th>Type</th><th>How it is built</th><th>Strengths</th><th>Limits</th></tr>
<tr><td>Plain (conventional) jacket</td><td>A second shell around the vessel, leaving a gap of 50 to 100&nbsp;mm. A spiral baffle or inlet nozzles are often added to make the fluid swirl</td><td>Simple and cheap. Ideal for steam, which needs no velocity. The usual choice on glass-lined vessels</td><td>Liquids move slowly, so heat transfer on the jacket side is poor. The jacket pressure pushes inward on the vessel wall, which limits the pressure and thickens the shell</td></tr>
<tr><td>Dimple jacket</td><td>A thin outer sheet pressed into a pattern of dimples and spot-welded to the vessel wall</td><td>Light and economical on large vessels. The dimples stir the fluid and stiffen the wall</td><td>Higher pressure drop. Narrow passages foul and are hard to clean. Moderate pressure only</td></tr>
<tr><td>Half-pipe coil jacket</td><td>Pipe split lengthwise and welded in a spiral around the shell</td><td>High velocity and good heat transfer with liquids. Holds high pressure, so it suits hot oil and high-pressure steam</td><td>A great deal of welding, so it costs more. Not practical on glass-lined vessels</td></tr>
<tr><td>Internal coil</td><td>A coil of pipe inside the vessel, in the liquid</td><td>Adds area without a bigger vessel, and has no thick vessel wall in the way</td><td>Hard to clean, takes up volume and gets in the way of mixing. A leak goes into the batch</td></tr>
<tr><td>External loop</td><td>The batch is pumped through a heat exchanger outside the vessel and back</td><td>The area is no longer limited by the size of the vessel</td><td>Needs a pump and more hold-up outside the reactor. Unsuitable for slurries and shear-sensitive products</td></tr>
</table>
<h2>Step 3: measure the area</h2>
<p>The jacket only works where there is liquid on the other side of the wall. With the liquid depth equal to the diameter, as in the scale-up series, R-101 is {f2(D_R)}&nbsp;m across and the wetted wall is:</p>
{eq(r"A = \pi\, D\, H = \pi \times %s \times %s = %s\ \text{m}^2" % (f2(D_R), f2(D_R), f1(A_J)))}
<p>That is {f1(A_J / V_B)}&nbsp;m² for each cubic metre of batch. The 100&nbsp;L pilot reactor had about 8&nbsp;m² per cubic metre. A jacket on the bottom head would add some area. A jacket above the liquid level adds none, which matters early in a fed batch when the vessel is only part full.</p>
<h2>Step 4: build the overall coefficient</h2>
<p>Heat leaving the batch has to cross four resistances in a row: the film of liquid on the inside of the wall, the wall itself, any fouling, and the film of cooling water on the jacket side. The overall coefficient {im("U")} is the reciprocal of their sum:</p>
{eq(r"\dfrac{1}{U} = \dfrac{1}{h_{\text{batch}}} + \dfrac{t_{\text{wall}}}{k_{\text{wall}}} + R_{\text{fouling}} + \dfrac{1}{h_{\text{jacket}}}")}
<p>For R-101 the batch side coefficient is taken as {f0(H_I)}&nbsp;W/m²·K, typical of a thin organic liquid with a well-sized agitator. The wall is {f0(WALL_T * 1000)}&nbsp;mm of stainless steel with a conductivity of {f0(WALL_K)}&nbsp;W/m·K. Fouling on both sides together is {R_FOUL:.5f}&nbsp;m²·K/W. Only the last term depends on the jacket. With cooling water, typical jacket side coefficients are about {f0(PLAIN["hj"])}&nbsp;W/m²·K for a plain jacket with a spiral baffle, {f0(DIMPLE["hj"])} for a dimple jacket and {f0(HALF["hj"])} for a half-pipe coil, because the water moves at roughly {PLAIN["vel"]:g}, {DIMPLE["vel"]:g} and {HALF["vel"]:g}&nbsp;m/s. For the plain jacket:</p>
{eq(r"\dfrac{1}{U} = \dfrac{1}{%s} + \dfrac{%.3f}{%s} + %.5f + \dfrac{1}{%s} = %.5f \quad\Rightarrow\quad U = %s\ \text{W/m}^2\!\cdot\!\text{K}" % (f0(H_I), WALL_T, f0(WALL_K), R_FOUL, tn(f0(PLAIN["hj"])), 1 / PLAIN["u"], f0(PLAIN["u"])))}
{fig(fig_resist(), 1, "Where the resistance to heat flow sits for three jacket types on R-101. A better jacket shrinks only the last block.")}
<p>Figure 1 is the lesson of this step. Going from a plain jacket to a half-pipe coil makes the jacket side five times better, yet {im("U")} rises only from {f0(PLAIN["u"])} to {f0(HALF["u"])}&nbsp;W/m²·K, about {f0((HALF["u"] / PLAIN["u"] - 1) * 100)}%. Once the jacket side is good, the batch film and the wall are in charge, and money spent on the jacket buys little. On a glass-lined reactor the glass and the thick steel behind it dominate even more, and the jacket type hardly matters.</p>
<h2>Step 5: calculate the cooling capacity</h2>
<p>The heat a jacket removes is the overall coefficient times the area times the mean temperature difference:</p>
{eq(r"Q = U\, A\, \Delta T_{\text{mean}}")}
<p>The water warms as it goes round, so the mean is a log mean, as for the heater in <a href="{Z2}.html">Part&nbsp;2</a>. With the batch at {f0(T_B)}&nbsp;°C and water entering at {f0(T_IN)}&nbsp;°C and leaving at {f1(T_OUT)}&nbsp;°C, the differences at the two ends are {f0(DT1)}&nbsp;K and {f1(DT2)}&nbsp;K and the log mean is {f0(LMTD)}&nbsp;K. For the plain jacket:</p>
{eq(r"Q = %s \times %s \times %s = %s\ \text{W} \approx %s\ \text{kW}" % (f0(PLAIN["u"]), f1(A_J), f0(LMTD), tn(f0(round(PLAIN["q"] * 1000, -2))), f0(PLAIN["q"])))}
<p>That is the {f0(PLAIN["q"])}&nbsp;kW quoted in the mass and energy balance, against the {f0(Q_GEN)}&nbsp;kW the reaction releases, so about {f0((1 - Q_GEN / PLAIN["q"]) * 100)}% of the capacity is in hand. Carrying that heat away with a {f1(T_OUT - T_IN)}&nbsp;K rise takes about {f0(W_FLOW)}&nbsp;m³/h of cooling water. The same calculation for each jacket, with the same {f0(W_FLOW)}&nbsp;m³/h of water, gives the table below. The coefficients are in W/m²·K.</p>
<table>
<tr><th>Jacket on R-101</th><th class="num">Jacket side</th><th class="num">Overall U</th><th class="num">Capacity, kW</th><th class="num">Addition, h</th></tr>
{jrows}
<tr><td>Plain jacket plus internal coil</td><td class="num"></td><td class="num"></td><td class="num">{f0(Q_PC)}</td><td class="num">{f1(T_PC)}</td></tr>
<tr><td>Half-pipe jacket plus internal coil</td><td class="num"></td><td class="num"></td><td class="num">{f0(Q_HC)}</td><td class="num">{f1(T_HC)}</td></tr>
</table>
<p>The last column is the {f1(Q_RXN)}&nbsp;GJ of reaction heat divided by the capacity: the shortest time over which the reactant can be added without the batch warming up. The better jackets shorten the addition from {f1(PLAIN["t"])} to about {f1(HALF["t"])} hours. The gain is a little less than the rise in {im("U")}, because water that picks up more heat leaves warmer, at {f1(HALF["out"])}&nbsp;°C from the half-pipe jacket, and that trims the mean temperature difference. It is worth having, but it is not a different plant.</p>
<h2>Step 6: add area when the wall is not enough</h2>
<p>The larger gains come from more area. An internal coil of 2-inch pipe, {C_TURNS} turns at {C_DIA:g}&nbsp;m diameter, adds {f1(A_C)}&nbsp;m². It also works better per square metre than the jacket, because its wall is only {C_WALL * 1000:.1f}&nbsp;mm thick and water runs fast inside it: about {f0(U_C)}&nbsp;W/m²·K. With the same {f0(W_FLOW)}&nbsp;m³/h of water shared between jacket and coil, the coil adds {f0(Q_C)}&nbsp;kW, which takes the plain-jacketed reactor to {f0(Q_PC)}&nbsp;kW and the addition down to {f1(T_PC)}&nbsp;hours. More water would raise it further.</p>
<p>The price is paid elsewhere. A coil is hard to clean between products, it disturbs the flow pattern the agitator was chosen for, and a pinhole puts cooling water into the batch. Where those matter, the alternative is an external loop: the batch is pumped through a heat exchanger whose area can be whatever the duty needs. Either way, the choice between jacket, coil and loop is made at the design basis stage, because it changes the vessel, the agitator and the layout.</p>
<h2>Step 7: check the worst case</h2>
<p>The capacity has to be compared with what happens when things go wrong, not only with the design rate. If the whole charge were added in one hour, as in the laboratory procedure, the heat would arrive at {f0(Q_1H)}&nbsp;kW. The plain jacket removes {f0(PLAIN["q"])}&nbsp;kW. The difference starts warming the batch at about {f0(RISE_1H)}&nbsp;K an hour, and it heads for the boiling point of {f0(T_BOIL)}&nbsp;°C. No jacket in the table would hold that rate. The protection is the addition rate itself, a high-temperature trip on the feed, and the analysis in <a href="{RUN}.html">What Happens If the Cooling Fails</a>.</p>
<p>Two other cases belong in the check: cooling water at its summer temperature, which shrinks the temperature difference, and the start of the addition, when the level is low and only part of the jacket is doing anything.</p>
{fig3d("jacket")}<h2>The data sheet</h2>
<table>
<tr><th>Item</th><th>R-101 jacket, base case</th></tr>
<tr><td>Vessel</td><td>{f0(V_B * 1000)}&nbsp;L batch, {f2(D_R)}&nbsp;m diameter, stainless steel, {f0(WALL_T * 1000)}&nbsp;mm wall</td></tr>
<tr><td>Jacket type</td><td>Plain jacket with spiral baffle, on the cylindrical wall</td></tr>
<tr><td>Heat transfer area (wetted)</td><td>{f1(A_J)}&nbsp;m²</td></tr>
<tr><td>Batch temperature</td><td>{f0(T_B)}&nbsp;°C</td></tr>
<tr><td>Cooling water in / out</td><td>{f0(T_IN)} / {f1(T_OUT)}&nbsp;°C, {f0(W_FLOW)}&nbsp;m³/h</td></tr>
<tr><td>Overall coefficient</td><td>{f0(PLAIN["u"])}&nbsp;W/m²·K</td></tr>
<tr><td>Heat of reaction to remove</td><td>{f0(Q_GEN)}&nbsp;kW average over a {f0(T_ADD)}-hour addition</td></tr>
<tr><td>Cooling capacity</td><td>{f0(PLAIN["q"])}&nbsp;kW</td></tr>
</table>
<h2>Common mistakes</h2>
<ul>
<li><strong>Carrying the pilot coefficient to full scale.</strong> The wall is thicker, the agitator turns more slowly and the jacket is a different design. Build {im("U")} from its parts.</li>
<li><strong>Counting jacket that is not wetted.</strong> Area above the liquid level does almost nothing.</li>
<li><strong>Upgrading the jacket when the batch side controls.</strong> Check which resistance is largest before paying for half-pipe.</li>
<li><strong>Sizing on the average.</strong> Heat release is rarely even through the addition. Calorimetry gives the peak.</li>
<li><strong>Forgetting the jacket's own pressure.</strong> A plain jacket puts external pressure on the vessel wall, and that can decide the shell thickness.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>The duty that sizes a reactor jacket is the heat of reaction at its highest rate.</li>
<li>Plain, dimple and half-pipe jackets differ mainly in the jacket side coefficient, cost and pressure rating.</li>
<li>The overall coefficient is set by the largest resistance. On R-101 that is the batch side, so a better jacket raises {im("U")} by only about {f0((HALF["u"] / PLAIN["u"] - 1) * 100)}%.</li>
<li>{im(r"Q = U A\, \Delta T_{\text{mean}}")}, with the wetted area only.</li>
<li>When the wall is not enough, add area with an internal coil or an external loop, and control the heat release with the addition rate.</li>
</ul>
<p>Earlier in this series: <a href="{Z1}.html">Part&nbsp;1</a> sized the pump, <a href="{Z2}.html">Part&nbsp;2</a> the heater, <a href="{Z3}.html">Part&nbsp;3</a> the feed tank, <a href="{Z4}.html">Part&nbsp;4</a> the control valve and <a href="{Z5}.html">Part&nbsp;5</a> the lines. Next: <a href="{Z7}.html">Part&nbsp;7</a> sizes the agitator that keeps the liquid moving past this jacket.</p>
{NOTE}{js3d("rx3d")}{mathjs()}"""
    body = nowrap(body, [(3, 0, 30)])
    return dict(slug=Z6, title="Sizing a Reactor Jacket: Jacket Types, Heat Transfer Area and Cooling Capacity",
                desc="How a reactor jacket is sized: plain, dimple and half-pipe jackets compared, overall coefficient, cooling capacity, coils and the worst case.",
                cats=["process-engineering"], tags=["reactor jacket", "half-pipe jacket", "dimple jacket", "heat transfer coefficient", "cooling capacity", "process design"],
                body=body, date=DATE, author="Quak Foo Lee", read="10 min read", series=SER6, cover_label="Equipment sizing",
                related=[U1, RUN, Z2])


if __name__ == "__main__":
    a = part6()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} {len(a['desc'])}\nD={D_R:.3f} A={A_J:.2f} LMTD={LMTD:.2f} Rf={R_FOUL:.6f} rows={[(r['name'], round(r['u'],1), round(r['q'],1), round(r['t'],2)) for r in ROWS]}\n"
                     f"water={W_FLOW:.2f} coil A={A_C:.2f} U={U_C:.0f} Q={Q_C:.1f} PC={Q_PC:.1f} {T_PC:.2f} HC={Q_HC:.0f} {T_HC:.2f} 1h={Q_1H:.0f} rise={RISE_1H:.1f}\n")
