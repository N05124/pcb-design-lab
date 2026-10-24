# C08 — 800 V SiC half-bridge isolated gate driver ★★★★☆

**Goal:** a gate-driver board for a half-bridge of SiC MOSFETs on an 800 V DC bus, with reinforced isolation between the low-voltage controller side and both high-voltage gate-drive domains.

## Why it's hard

Safety and physics fight for the same millimetres. Reinforced insulation at 800 V working voltage needs large creepage and clearance distances, but the gate loops need to be tiny to switch SiC at 50–100 V/ns without ringing. That same dV/dt pushes common-mode current through every parasitic capacitance across the barrier, so isolated supplies and digital isolators must have low barrier capacitance, and copper overlapping the barrier on inner layers is forbidden.

## Suggested blocks

- Two reinforced isolated gate drivers with Miller clamp and desaturation detection (UCC21750/1ED34xx-class)
- Two isolated DC-DC modules (+18 V / −4 V) with low barrier capacitance
- Gate resistors (separate turn-on/turn-off), Kelvin-source connection to each MOSFET
- Logic-side connector with PWM, fault and enable

## Board budget

| Item | Budget |
|---|---|
| Layers | 4 |
| Creepage / clearance | Derive from IEC 60664-1 (or IEC 62368-1 / IEC 61800-5-1) for your pollution degree, material group and working voltage. As a sanity check, reinforced insulation at 800 V DC commonly lands in the ~8–16 mm creepage range depending on material group. **Document your calculation.** |
| Slots | Routed slots allowed under the isolators to increase creepage |

## Pass / fail

1. Manufacturable: DRC clean, fully routed.
2. Constraints ([`C08.yaml`](../constraints/C08.yaml)): gate-drive nets on outer layers only and ≤ 0 vias between driver output and MOSFET gate pin where possible; KiCad custom DRC rules (`.kicad_dru`) enforcing creepage-domain clearance between net classes.
3. Electrically sound:
   - **No copper on any layer** crosses the isolation barrier except inside the isolator packages
   - Gate loop (driver out → gate → Kelvin source → driver return) area ≤ 50 mm² per switch
   - Each isolated domain has its own local plane; no high-voltage domain overlaps another on adjacent layers
4. Measured (if built): hipot at the rating your calculation requires; gate waveform overshoot ≤ 10 % at full dV/dt.

## Stretch

- Add a fast overcurrent trip via desaturation with a measured response under 1.5 µs.
- Two-layer version with the same isolation rating.

## Read first

- MIT 6.622 and 6.334 power electronics — [curriculum](../../curriculum/mit-ocw.md)
- Gate-driver vendor application notes on isolation layout
