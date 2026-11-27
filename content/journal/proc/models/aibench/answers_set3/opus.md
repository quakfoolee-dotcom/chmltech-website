# Answers, set 3

## Task 41

**Duty.** m = 2.414 kg/s, cp 2.0 kJ/kg.K.
- Average case (22 to 80 C): 280 kW, about 470 kg/h of steam (hfg about 2,130 kJ/kg).
- Design case: the feed comes from an outdoor tank, so size for a winter feed of about 5 C (confirm against site data). That gives 362 kW and about 610 kg/h of steam. Sizing on the 22 C average would leave the heater short all winter.

**Area.** Allow about 1 bar across the steam control valve, so the shell runs at about 2 barg (Tsat about 134 C, against 144 C at 3 barg).
- Winter, clean (U 800): LMTD 85.8 K, A = 5.3 m2.
- With fouling on the organic side (service U about 600, i.e. Rf about 0.0004 m2K/W): A = 7.0 m2.
- **Recommend about 7 m2 effective area.** Do not add a further margin on top of that.

**The real design problem is stall.** With 7 m2 and clean tubes, the shell pressure needed to meet the duty is:
- 100% rate, 22 C feed: about 1.3 bara (106 C).
- 50% rate: about 0.65 bara (86 C), which is a vacuum.
- Winter design case: about 3.0 bara.

The condensate return is atmospheric, so the trap has little or no differential across it for most of the operating range. Condensate will back up into the shell. The results are waterlogging, temperature cycling, water hammer, corrosion from carbonic acid, and tube or tube-sheet damage. Bigger area makes this worse.

**What the design must address:**
1. Draw a stall chart over the full envelope: 50 to 100% rate, winter to summer feed, clean to fouled.
2. Pick a remedy:
   - (a) Pressure-powered pump-trap (pump plus trap) with a vacuum breaker and balance line. This is the usual choice.
   - (b) Condensate-side control, where a flooded shell is level-controlled. It gives smooth turndown but slow response.
   - (c) A lower-pressure steam supply, so the valve operates further open.
3. Fit a vacuum breaker on the shell, an air vent, and a strainer, and use a float-thermostatic trap rather than a thermodynamic one. Fall the condensate line to the trap.
4. Size the control valve for 610 kg/h at about a 1 bar drop, checked against 50% summer turndown (about 140 kg/h). The duty spans about 4.4:1, so check valve rangeability.
5. Mechanical: steam on the shell side, design to 3.0 barg plus margin, and a PSV if the shell is below steam header design pressure. Allow for thermal expansion (fixed tubesheet versus U-tube).
6. Organic side: check the feed against high-temperature limits such as fouling, degradation and flash at the steam-off-valve-open condition. Add a high-temperature trip.

## Task 42

**NPSHa** = (Psurface - Pv)/(rho g) + static head - friction. rho g = 8.63 kPa/m.

- Use the worst case: low-low level (1 m) and the maximum liquid temperature. I assumed 40 C (Pv 8 kPa), since the tank is outdoors and probably sun-exposed. Confirm the maximum temperature.
- Do not credit the nitrogen blanket. The tank's breather/vacuum valve can let the tank go slightly below atmospheric, so take Psurface = 101.3 kPa (adjust for site altitude).
- Pressure head: (101.3 - 8)/8.63 = 10.8 m.
- Friction: 0.5 m at normal flow becomes about 0.6 m at rated flow (rated is about 110% of normal, and friction goes with flow squared). Double it for a partly blocked strainer, giving about 1.2 m.
- **NPSHa (worst case) = 10.8 + 1.0 - 1.2 = about 10.6 m.** For reference, normal level with the blanket at 20 C gives about 15.9 m.

**Margin required:** the larger of NPSHa - NPSHr ≥ 1.0 m, or NPSHa/NPSHr ≥ 1.3. Use 1.5 or more if the suction energy is high (ANSI/HI 9.6.1).

**Result:** margin about 7.1 m, ratio about 3.0. **The pump is acceptable** with a good margin.

Conditions:
- NPSHr is quoted at a 3% head drop and at rated flow. Get the NPSHr curve and check at the maximum operating or run-out flow, since NPSHr rises steeply there.
- Confirm that the suction pressure drop does not include an undersized strainer or a long line. Add a strainer ΔP alarm, or specify a cleaning interval.
- Check for dissolved nitrogen or volatile light ends that would raise the effective vapour pressure.
- Check vortexing at low-low level (1 m submergence is probably adequate, but check against the nozzle velocity), or fit a vortex breaker.
- Record the basis on the pump datasheet.

## Task 43

**I would not accept this basis.** It sizes the wrong scenario and it does not deal with the actual hazard.

1. **The closed manual valve is a design error to fix, not a case to size for.** A manual valve in a relief path must be car-sealed or locked open under an administrative procedure (API 520/521, ASME VIII). Better still, remove it. If the PSV discharges through it to the scrubber, a closed valve defeats any relief device, whatever its size.
2. **"Blocked outlet" barely applies to a batch reactor.** There is no continuous outflow to block. The pressure sources are the reaction itself, nitrogen and fire.
3. **The governing case is almost certainly runaway reaction.** Triggers include loss of cooling water, agitator failure, overcharge or wrong charge sequence, accumulation of unreacted reagent, contamination, and wrong temperature. The relief will usually be two-phase (foamy liquid swell), so a gas-only sizing will be undersized, often by a factor of 10 or more. This needs:
   - adiabatic calorimetry (ARC, VSP2 or Phi-TEC) to classify the system as vapour-pressure, gassy or hybrid and to get dT/dt and dP/dt at set pressure;
   - DIERS/Leung or HEM two-phase sizing;
   - often a bursting disc, alone or ahead of the PSV, rather than a spring PSV alone.
4. **Other cases to evaluate (API 521):**
   - external fire on 10 m3 (21% accumulation);
   - nitrogen regulator failing open, sized on the maximum N2 flow through the failed regulator or restriction orifice;
   - cooling-water ingress from a jacket leak, if the reaction is water-sensitive;
   - thermal expansion of the liquid-full vessel;
   - the jacket needs its own relief: blocked-in CW thermal relief, and the steam case if the jacket is also heated.
5. **Disposal:** the scrubber is unlikely to take a two-phase runaway discharge. Provide a catch tank or quench and size it. Check backpressure and inlet loss (3% rule).
6. **Prevention:** a dosing-controlled (semi-batch) recipe, high-temperature and loss-of-agitation interlocks, cooling-failure detection, and a SIL assessment via HAZOP/LOPA.

Return the basis with this scenario list, and get the calorimetry done before anything is sized.

## Task 44

**Required Cv at normal flow:** Kv = Q·√(SG/ΔP) = 12·√(0.87/1.5) = 9.14. **Cv = 1.156 Kv = 10.6.**

**Specify at maximum flow, not normal.**
- I assumed a maximum of 130% of normal (15.6 m3/h).
- At that flow the valve ΔP falls (system friction rises, pump head falls), say to about 1.1 bar. Cv required = 15.6/0.865·√(0.87/1.1) = **about 16.0**. Minimum flow (say 30%, at about 1.8 bar ΔP) gives Cv about 2.9.
- **Specify rated Cv about 20 to 25**, so that maximum flow is at about 80% open and normal flow is around 55 to 65% open.

**Size:** a globe valve with equal-percentage trim. Either:
- a **1.5 in body, full trim** (Cv about 25 to 30); or
- a **2 in body with reduced trim**, to match a 2 in line (about 1.5 m/s at 12 m3/h).

I would choose the 2 in reduced-trim body, which avoids reducers and allows re-trimming later. Do not put full Cv 50 trim in 2 in: normal flow would sit near 30% open.

**Needed before purchase:**
1. Real maximum, normal and minimum flows, and the system curve (pump curve plus line losses), so the valve ΔP at each flow is known, not assumed.
2. Inlet pressure P1, vapour pressure at maximum temperature, and FL. Check choked flow (ΔPmax = FL²(P1 - FF·Pv)) and the cavitation index σ. At 1.5 bar ΔP and low P1, anti-cavitation trim may be needed.
3. Viscosity, for the Reynolds correction if the fluid is viscous.
4. Fail action (FC or FO) from the hazard review, shutoff class (ANSI IV or V), and actuator sizing against the maximum shutoff ΔP (pump shut-off head).
5. Materials and corrosion, pressure/temperature rating, noise, and solids or erosion.
6. Rangeability and positioner. Confirm that the installed characteristic stays near linear over the operating range.

The final Cv and trim should come from the vendor's IEC 60534 calculation using these data.
