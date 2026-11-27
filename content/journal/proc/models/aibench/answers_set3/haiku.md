## Task 41

**Duty.** Q = 8,690 kg/h x 2.0 kJ/kg.K x (80 - 22) K = 1.008 GJ/h = 280 kW.
Steam at 3.0 barg (4.0 bara) condenses at about 143.6 C with hfg of about 2,134 kJ/kg, so steam use is about 470 kg/h at the design point.

**Area (22 C feed).** Steam condensing at constant temperature gives LMTD = (121.6 - 63.6)/ln(121.6/63.6) = 89.5 K.
- Clean: A = 280,000 / (800 x 89.5) = 3.9 m2.
- Design U of about 500 W/m2.K for organic-side fouling: A = 6.3 m2.

**Design case.** A 22 C average is not the design point. At an assumed winter minimum of 5 C (confirm with site data), Q = 362 kW and LMTD = 96 K, so A = 7.5 m2 at U = 500.

**Recommendation.** Size on the cold case and specify about 8.5 m2 (about 10 to 15% margin).

**Other items for the design:**
- **50% rate.** Steam is fixed at 3 barg, so the steam control valve lowers the condensing temperature to hold outlet temperature. Check valve rangeability and low-load stability, and whether a split-range or bypass arrangement is needed.
- **Steam trap.** Size for about 2x the cold-case condensate (about 610 kg/h, so about 1,200 kg/h) with 3 bar differential to atmosphere. Include a thermostatic air vent for start-up.
- **Flash on the atmospheric return.** Condensate flashes about 8% (4.2 x 43.6 / 2,257) at 100 C, so size the return line and the vent for flash.
- **Wall temperature.** Tube wall sits near 144 C. Check the film temperature against the organic's thermal stability, coking and autoignition temperature.
- **Overpressure.** Relieve the cold side for blocked-in thermal expansion, and the steam side to the 3 barg header.

## Task 42

**Inputs.** Atmospheric pressure 101.3 kPa plus 3 kPa blanket gives Pa = 104.3 kPa(a). The operating liquid temperature is not stated, so I take 40 C (Pv = 8 kPa) as the conservative case and check 20 C. One kPa is 1,000 / (880 x 9.81) = 0.116 m of liquid.

**NPSHa at low-low level, 40 C.**
- Pressure term: (104.3 - 8) kPa = 96.3 kPa, which is 11.2 m.
- Static head at low-low level: +1.0 m.
- Suction friction: -0.5 m.
- NPSHa = 11.2 + 1.0 - 0.5 = **11.7 m**.

At 20 C the same case gives 12.1 m. At normal level and 40 C it gives 14.7 m.

**Margin.** NPSHa / NPSHr = 11.7 / 3.5 = 3.3, and NPSHa - NPSHr = 8.2 m. I would require NPSHa of at least the greater of 1.3 x NPSHr (4.6 m) and NPSHr + 1 m (4.5 m), so the pump passes with room to spare.

**Recommendation.** Accept P-101 for NPSH.

**Points to note:**
- The low-low level is not the NPSH constraint, because NPSHa stays above the requirement well below the low-low trip. The sensitive variable is liquid temperature, so confirm the actual tank temperature.
- A lost blanket drops Pa by about 3 kPa, which costs about 0.35 m. The pump still passes.
- Check NPSHr at the maximum flow on the vendor curve, since NPSHr rises with flow.
- Keep the strainer clean and alarm its differential pressure, since a dirty strainer costs suction head.

## Task 43

**Verdict.** I would not accept a blocked-outlet-only basis.

**Why.**
- **Other causes govern.** For an exothermic batch reactor the usual governing case is a runaway. Screen cooling failure (cooling water loss, valve or pump failure), loss of agitation, reagent overcharge or dosing error, nitrogen regulator failure (high-pressure padding gas), and external fire. Take the largest credible load.
- **Blocked outlet needs a source.** It is only credible if a pressurised source feeds the line that blocks. Show the source before using it.
- **Vent valve.** A manual valve in the relief path that can be left closed is not acceptable. Either car-seal or lock it open under administrative control, or remove the isolation. Check the scrubber's built-up back pressure at the relief flow, and use a balanced valve if it is too high.
- **Two-phase relief.** A runaway usually discharges vapour and liquid together, so gas-only sizing is not valid. Size with the DIERS approach using the gas generation rate and vapour-liquid behaviour from reaction calorimetry (adiabatic temperature rise, TMRad, gas generation rate).
- **Set pressure and accumulation.** Set at or below 6 barg. Accumulation is 10% for non-fire cases and 21% for fire (single valve, ASME VIII).
- **Jacket.** Check the jacket's own relief, in case cooling-water pressure exceeds the jacket design pressure.

**What to tell them.** Run a HAZOP or LOPA screen of all credible causes, size each one, and document the largest as the basis. Then decide on the vent-path arrangement.

## Task 44

**Sizing.** Kv = Q x sqrt(SG / dP) = 12 x sqrt(0.87 / 1.5) = 9.14 (m3/h, bar). Cv = 1.156 x Kv = **10.6** (US units). Specify Cv about 10.6 at the normal point.

**Valve size.** Size on the maximum flow and check the minimum. For example, at 1.25 x normal, Cv is about 13.2. Choose a valve whose rated Cv at full travel is about 1.3 to 1.5 times the required Cv, so the normal point sits near 60 to 80% opening. That points to a DN25 (1 in) characterised valve with a rated Cv of about 14 to 16, or a DN40 valve with reduced trim. Confirm both against vendor data. Line velocity at 12 m3/h is about 2.9 m/s in DN40, which is acceptable.

**Check or know before buying:**
- Minimum, normal and maximum flows, with the operating and minimum pressures at each.
- Whether 1.5 bar is a sensible share of the total loss (about 20 to 50% of the system loss from pump to point of use).
- Cavitation or flashing: compare dP with FL squared times (P1 - FF x Pv), using the vapour pressure at the maximum temperature.
- Viscosity at operating temperature (a Reynolds correction is needed if viscous).
- SG at operating temperature (0.87 is not stated as a temperature).
- Noise limit, shutoff class, fail position on air or power loss.
- Pressure class, body and seat materials for the organic, and actuator and positioner sizing.
