## Task 41

**Duty (normal):** 8,690 kg/h = 2.414 kg/s x 2.0 x 58 K = 280 kW. Steam at 3 barg (4.0 bara): Tsat about 144 C, latent heat about 2,130 kJ/kg, so about 0.13 kg/s (470 kg/h).

**Area:** LMTD = (121.6 - 63.6)/ln(121.6/63.6) = 89.5 K. A(clean) = 280,000/(800 x 89.5) = 3.9 m2.

The 22 C average is not the design case. At a winter design feed of -10 C (I assumed this; confirm site data), Q = 435 kW, LMTD about 102 K, and clean area = 5.3 m2. Allow about 20% for fouling and margin, giving **about 6.5 to 7 m2 (one shell-and-tube unit, specify ~7 m2 installed)**. Clean U is also optimistic for an organic liquid. Confirm it with the viscosity and a tube-side film calculation. A fouled U of about 500 to 600 would push the area higher.

**Turndown is the real problem.** At 50% rate and 22 C feed, Q = 140 kW. With 7 m2 installed, the steam temperature needed is only about 86 C, which is about 0.6 bara. The steam-side pressure falls below atmospheric. The trap then cannot discharge to an atmospheric return, and condensate floods the exchanger. Flooding causes cycling, poor control, water hammer and corrosion. Mitigations:
- Use a pumping trap or condensate pump, or a vacuum-capable return.
- Use a split-range arrangement with two smaller shells in parallel.
- Reduce the steam supply pressure with a PRV so the exchanger operates at a controllable pressure.
- Control by condensate level instead of steam throttling.

**Also address:**
- Tube-wall temperature of about 140 C against the organic's thermal stability and flash point. Add a high-temperature trip and consider lower-pressure steam.
- Process-side thermal-expansion relief when the unit is blocked in.
- Tube-leak and steam-side design pressure.
- Freezing, pour point and viscosity at low feed temperature.
- Trap sizing for the maximum condensate load, and a drain/vent arrangement.
- Control-valve sizing on the steam line.
- Whether fouling or hot-spot degradation needs a spare or cleanable design.

## Task 42

**NPSHa = (P_tank - Pv)/(rho g) + static - friction.**

Assumptions: the liquid is at 40 C at worst (Pv = 8 kPa), which is conservative against the 20 C datum. Tank pressure is 0.03 barg, so 104.3 kPa(a). To be conservative I take no credit for the pad (101.3 kPa), since the regulator could fail or the breather could open.

- Pressure term: (101.3 - 8)/(880 x 9.81) = 10.8 m.
- At low-low level: 10.8 + 1.0 - 0.5 = **about 11.3 m**.
- At normal level: 10.8 + 4.0 - 0.5 = about 14.3 m.
- Including the pad credit, add about 0.35 m.

Against NPSHr = 3.5 m, the margin is about 7.8 m at low-low, a ratio of about 3.2. **The pump is acceptable.**

**Margin to require:** a minimum of 1 m or a ratio of 1.3 (use the larger; HI 9.6.1 gives guidance, and 1.1 to 1.3 is typical for a process pump). The calculated margin comfortably exceeds both.

**Caveats to confirm:**
- Vapour pressure at the actual maximum tank and suction temperature (summer sun on an outdoor tank, or recycle/hot returns). Even at 60 C (Pv roughly 15 to 20 kPa by extrapolation) NPSHa stays above 10 m.
- NPSHr at maximum or run-out flow, not only the rated point. Check the basis (3% head drop), and that the 3.5 m is for this liquid.
- Strainer friction at the fouled differential pressure alarm point (say 2 to 3 m). The margin still holds.
- Suction nozzle and fittings losses, inlet velocity head, and a vortex breaker at low-low level.
- Entrained or dissolved nitrogen and vapour at start-up.
- Minimum continuous flow protection and a lower tank vacuum case if the blanket or breather fails.

## Task 43

I would reject this basis. Three problems.

**1. Blocked outlet is rarely the governing case for a jacketed batch reactor.** A relief device is sized for the worst credible scenario. I would expect these to be evaluated (API 520/521, DIERS):
- **Runaway reaction or loss of cooling.** This is likely governing and may be two-phase, with gas generation and foaming, so it needs vent-sizing calorimetry data (ARC or VSP, DIERS methods). Gas-only sizing will undersize the device.
- **External fire**, using the wetted area of the 10 m3 vessel.
- **Nitrogen regulator or supply failure**, with the full N2 header pressure applied to the reactor. Check that the N2 header pressure and regulator capacity do not exceed the 6 barg design.
- **Jacket and utility cases.** Cooling-water-side overpressure if the jacket is blocked in or heated, and a jacket leak.
- Overfilling, and heating or thermal expansion of liquid blocked in the jacket.
- Charge-pump deadhead, which is the real "blocked outlet" source.

**2. The manual valve is the real defect.** The relief path to the scrubber must not have a block valve that can be left closed. If a valve is unavoidable it must be locked or car-sealed open with an administrative procedure, ideally interlocked, and ideally the PRV should discharge independently. Do not use a design assumption to excuse a valve that can defeat the protection.

**3. Discharge.** Check the relief load against scrubber capacity, the back-pressure and two-phase flow in the vent line, and the effluent to a safe location (catch tank or quench). A rupture disk in series or parallel may suit a runaway case with polymer or fouling risk.

I would ask for a documented relief scenario review (HAZOP/LOPA), the runaway data, and the PRV sizing before sign-off.

## Task 44

**Calculated Cv (normal):**
Kv = Q sqrt(SG/dP) = 12 x sqrt(0.87/1.5) = 9.1 m3/h.
Cv = 1.156 x Kv = **about 10.6** (US units check: 52.8 gpm x sqrt(0.87/21.8) = 10.6).

That is the required Cv at normal flow, not the figure to buy. To keep the valve controlling at about 60 to 70% opening at normal flow, with room for maximum flow, I would specify a **rated Cv of about 16 to 20** (for example Cv 17, which gives roughly 65% opening at normal). On a globe valve this means a **1 inch (DN25)** body with a reduced or full trim. The line is probably 1.5 or 2 inch (DN40 or DN50), so I would use reducers and apply the piping-geometry factor Fp. That reduces the effective Cv a few percent.

**Before buying, I need:**
- Minimum, normal and maximum flows with the valve dP at each, and whether 1.5 bar is the available dP or just a guess. The valve should take at least about 25 to 33% of the total system drop, or the characteristic will be distorted.
- Inlet and outlet pressure, temperature, vapour pressure and critical pressure, to check for flashing and cavitation (compare dP with FL squared x (P1 - FF x Pv)).
- Viscosity, to correct Cv if Reynolds number is low.
- Fail position (fail-closed or fail-open) from the process safety review.
- Characteristic (equal percentage if dP varies, linear otherwise), and rangeability.
- Shutoff class and leakage, actuator and positioner, hand wheel, and body and trim materials.
- Noise and velocity, and whether a bypass or isolation valves are needed.
