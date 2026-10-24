# C04 — 12 V → 0.9 V / 40 A multiphase regulator ★★★☆☆

**Goal:** a 3- or 4-phase synchronous buck delivering 40 A at 0.9 V to a load connector, with ≤ 30 mV ripple, ≤ 3 % droop on a 20 A load step, and no hotspot above 85 °C at full load in 25 °C still air.

## Why it's hard

Low voltage and high current flip the usual problems: copper resistance and current density matter more than signal timing, a few nanohenries in the switching loop produce ringing that kills efficiency and EMI, and heat has to get out through vias and planes. The current-sense lines are tiny analog signals living beside 40 A of switching current.

## Suggested blocks

- Multiphase controller + smart power stages (DrMOS-class) or a multiphase module
- One inductor per phase, bulk + MLCC output bank, input MLCCs per phase
- Remote differential voltage sense from the load connector back to the controller
- Test load connector with Kelvin sense points

## Board budget

| Item | Budget |
|---|---|
| Layers | 6, with 2 oz copper on the outer power layers |
| Size | ≤ 70 × 50 mm |
| Copper | Current density ≤ 35 A/mm² in any plane neck at 40 A |

## Pass / fail

1. Manufacturable: DRC clean, fully routed.
2. Constraints ([`C04.yaml`](../constraints/C04.yaml)): differential sense pair matched within 2 mm and routed on an inner layer away from switch nodes; phase switch-node nets stay on the top layer.
3. Electrically sound:
   - Each phase's hot loop (input cap → high-side FET → low-side FET → GND) on the top layer with the return plane directly beneath; loop area ≤ 20 mm²
   - ≥ 1 thermal via per ampere under each power stage
   - Switch-node copper no larger than needed to carry current (it is an antenna)
   - Run KiCad's or an external IR-drop / thermal estimate and include the result
4. Measured (if built): ripple, load-step droop and thermal image vs. targets above.

## Stretch

- Reach 85 % efficiency at full load.
- Put the regulator on the back of a board directly under its load (the way server VRMs are done).

## Read first

- MIT 6.622 Lecture 38 (layout) and 6.334 chapters on thermal and EMI — [curriculum](../../curriculum/mit-ocw.md)
- Power-stage vendor's layout guide
