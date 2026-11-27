# Process engineering calculation tasks

Answer every task. For each, give the numeric answers under the keys listed. Use SI or the units stated.

## Task 1
A centrifugal pump handles a liquid of density 870 kg/m3. Suction pressure is 1.2 barg and discharge pressure is 6.8 barg at the pump nozzles, which are at the same elevation; velocity heads are negligible. What is the pump differential head in metres of liquid?
Answer keys: head_m [m]

## Task 2
A pump takes suction from a nitrogen-blanketed tank held at 0.035 barg; atmospheric pressure is 101.325 kPa. The liquid is at 40 C, where its vapour pressure is 8.01 kPa(a) and its density is 881 kg/m3. The lowest liquid level is 1.5 m above the pump centreline, and suction line friction at the design flow is 0.6 m of liquid. Calculate the NPSH available in metres.
Answer keys: npsha_m [m]

## Task 3
A pump delivers 12.0 m3/h of liquid of density 870 kg/m3 against a differential head of 75 m. Pump efficiency is 62% and motor efficiency 92%. Give the shaft power and the electrical power drawn, both in kW.
Answer keys: shaft_kW [kW], electrical_kW [kW]

## Task 4
Liquid (density 870 kg/m3, viscosity 1.2 mPa.s) flows at 12.0 m3/h through 140 m of straight pipe with inside diameter 52.5 mm and absolute roughness 0.045 mm. Using the Darcy-Weisbach equation with the Colebrook-White friction factor, what is the frictional pressure drop in kPa?
Answer keys: dp_kPa [kPa]

## Task 5
A control valve passes 12.0 m3/h of liquid with specific gravity 0.87 at a pressure drop of 1.5 bar (non-choked, turbulent). Calculate the required Kv (m3/h at 1 bar) and the corresponding Cv (US gpm at 1 psi).
Answer keys: Kv [m3/h], Cv [US gpm/psi^0.5]

## Task 6
A globe valve (liquid pressure recovery factor FL = 0.90) has an upstream pressure of 6.0 barg; atmospheric pressure is 1.01325 bar. The liquid is water at a temperature where its vapour pressure is 0.90 bar(a); critical pressure 221.2 bar(a). Using the IEC 60534 / ISA method with FF = 0.96 - 0.28 sqrt(Pv/Pc), what is the maximum pressure drop for non-choked flow, in bar? Would a pressure drop of 5.2 bar be choked (answer 1 for yes, 0 for no)?
Answer keys: dp_choked_bar [bar], choked_at_5.2 [1/0]

## Task 7
A liquid feed of 6,250 kg/h (cp 2.0 kJ/kg.K) is heated from 20 C to 80 C by steam condensing at 143.7 C. With an overall coefficient of 500 W/m2.K, find the duty (kW), the LMTD (K) and the area required (m2).
Answer keys: duty_kW [kW], lmtd_K [K], area_m2 [m2]

## Task 8
An existing exchanger has 6.0 m2 of area and, when fouled, an overall coefficient of 900 W/m2.K. It heats 8,690 kg/h of liquid (cp 2.0 kJ/kg.K) entering at 15 C with steam condensing at 143.7 C. What outlet temperature does it reach (C)?
Answer keys: T_out_C [C]

## Task 9
Low-pressure saturated steam at 3.0 barg (atmospheric 1.01325 bar) supplies a duty of 208.3 kW, leaving as saturated condensate. Using steam tables, what steam flow is required in kg/h? Also state the saturation temperature in C.
Answer keys: steam_kgh [kg/h], Tsat_C [C]

## Task 10
Fresh feed of 100 kmol/h of reactant A enters a process. The reactor converts 60% of the A it receives per pass. A separator after the reactor recovers 98% of the unreacted A and recycles it to the reactor inlet; the remaining 2% of unreacted A leaves with the product. At steady state, what are the recycle flow of A (kmol/h) and the overall conversion of the fresh A (as a fraction)?
Answer keys: recycle_kmolh [kmol/h], overall_conversion [-]

## Task 11
A liquid-phase first-order reaction with rate constant 0.15 min-1 runs in a single CSTR at constant density. Feed is 8.0 m3/h. What reactor liquid volume (m3) gives 90% conversion?
Answer keys: volume_m3 [m3]

## Task 12
A feed containing 2.0 kmol/m3 of reactant (density 900 kg/m3, cp 2.1 kJ/kg.K) undergoes an exothermic reaction with heat of reaction -85 kJ/mol. If 95% of the reactant converts with no heat removal, what is the adiabatic temperature rise (K)?
Answer keys: dT_K [K]

## Task 13
Using the API 521 fire-case equation for a vessel with adequate drainage and prompt fire-fighting (Q = 21,000 F A^0.82, Q in BTU/h, A in ft2), find the heat input to a bare vessel (F = 1.0) with 450 ft2 of wetted area, and the relieving rate in lb/h if the liquid's latent heat at relieving conditions is 140 BTU/lb.
Answer keys: Q_BTUh [BTU/h], W_lbh [lb/h]

## Task 14
Size a relief valve for critical vapour flow per API 520 Part I (SI units): A = W/(C Kd P1 Kb Kc) x sqrt(T Z / M), with A in mm2, W in kg/h, P1 in kPa(a), T in K, and C = 0.03948 sqrt(k (2/(k+1))^((k+1)/(k-1))). Relieving rate 2,500 kg/h; set pressure 10.0 barg with 10% overpressure (atmospheric 101.325 kPa); relieving temperature 400 K; Z = 0.95; M = 58.1; k = 1.12; Kd = 0.975; Kb = Kc = 1.0. What effective orifice area (mm2) is required?
Answer keys: area_mm2 [mm2]

## Task 15
A feed with mole fractions z = (0.30, 0.50, 0.20) is flashed at conditions where the K-values are (3.5, 0.9, 0.12). Solve the Rachford-Rice equation for the vapour fraction V/F, and give the liquid mole fraction of the first component.
Answer keys: V_over_F [-], x1 [-]

## Task 16
50 US gpm of liquid (density 870 kg/m3, viscosity 1.2 cP) flows in 2-inch Schedule 40 pipe (ID 2.067 in). What are the velocity in m/s and the Reynolds number?
Answer keys: velocity_ms [m/s], Re [-]

## Task 17
A well-mixed batch of 8,000 kg (cp 2.2 kJ/kg.K) is heated in a jacketed vessel from 20 C to 90 C with steam condensing at 143.7 C in the jacket. U = 400 W/m2.K and the jacket area is 12 m2. Heat losses are negligible. How long does the heating take, in hours?
Answer keys: time_h [h]

## Task 18
A pump develops a differential pressure of 35 psi on a liquid with specific gravity 0.87. What is its head in feet? A valve on the same line passes 50 US gpm at a 12 psi drop: what is its Cv?
Answer keys: head_ft [ft], Cv [-]

## Task 19
A 5.0 m3 reactor cost US$1.20 million when the cost index was 600. Using the six-tenths rule, estimate the cost of an 8.0 m3 reactor today, with the index at 800.
Answer keys: cost_USD [US$]

## Task 20
An energy-saving project costs C$250,000 now and saves C$60,000 a year for 10 years (end-of-year), with no salvage value. At an 8% discount rate, what is its NPV (C$), and what is the simple payback (years)?
Answer keys: npv_CAD [C$], payback_y [y]
