# PCB design handbook — the rules that matter on hard boards

This is a working reference, not a textbook. Each section says what the rule is, why it exists, and where to read more. Numbers marked *typical* are common starting points; your silicon vendor's layout guide and your fab's capability page always win.

---

## 1. Think in currents, not wires

Every signal current returns to its source. At low frequency the return spreads out along the path of least **resistance**; above a few hundred kHz it flows along the path of least **inductance**, which is the copper directly beneath (or beside) the signal trace. Almost every layout rule for fast or sensitive circuits is a consequence of that one fact:

- **Solid reference planes.** A plane under a trace lets the return current hug the trace, keeping the loop — and therefore inductance, radiation and crosstalk — small.
- **Don't route across splits or slots.** The return current has to detour around the gap, creating a big loop: an antenna and a source of ringing.
- **Stitch references at layer changes.** When a signal via moves from a layer referenced to GND to one referenced to another plane, put a ground via (or a capacitor between the planes) right beside it so the return current can follow.
- **Don't split ground to "isolate" analog from digital.** Partition by *placement* instead and keep one solid ground. Splits are a 1980s fix that usually makes modern mixed-signal boards worse.

Read: MIT 6.013 (fields), 6.641 (coupling) — see [curriculum](../curriculum/mit-ocw.md). Henry Ott and Rick Hartley's free talks and articles are the best plain-language treatment (see [references](../references/open-resources.md)).

## 2. When is a trace a transmission line?

Treat a trace as a transmission line (controlled impedance, termination, no stubs) once its delay is more than roughly 1/6 of the signal's rise time.

| Quantity | Rule of thumb |
|---|---|
| Signal speed in FR-4 stripline (εr ≈ 4) | ≈ 150 mm/ns ≈ 6.7 ps/mm |
| Signal speed in FR-4 microstrip | ≈ 170–180 mm/ns |
| Bandwidth of an edge | BW ≈ 0.35 / t_rise |
| Critical length | L_crit ≈ t_rise × v / 6. A 1 ns edge → ~25 mm; 100 ps → ~2.5 mm |

So a "slow" 3.3 V MCU GPIO with a 2 ns edge already needs care on traces longer than ~5 cm. It's the **edge rate**, not the clock frequency, that matters.

## 3. Stackups

Choose the stackup before placement. It sets every impedance and how many routing layers have a good reference.

**Good default stackups** (*typical*; confirm with your fab's real dielectric thicknesses):

| Layers | Arrangement | Notes |
|---|---|---|
| 2 | Sig+pour / GND+sig | Keep the bottom as unbroken GND as possible. No controlled impedance in practice. |
| 4 | Sig / **GND** / PWR / Sig | The workhorse. Both outer layers reference a plane. Route fast signals on top over GND. |
| 6 | Sig / GND / Sig / PWR / GND / Sig | Inner signal layer is stripline between planes: low crosstalk, low emissions. |
| 8 | Sig / GND / Sig / PWR / GND / Sig / GND / Sig | Common for DDR and SoC boards. Every signal layer adjacent to a ground. |
| 10–12 | Add signal/GND pairs | Jetson-class baseboards, FPGA boards with transceivers. |

Keep the stackup symmetric (copper and dielectric mirrored around the centre) so the board doesn't warp in reflow.

Impedance tools: KiCad's built-in calculator (Transmission line tab), [Saturn PCB Toolkit](https://saturnpcb.com/saturn-pcb-toolkit/) (free), your fab's online calculator, and [openEMS](https://openems.de/) for field-solved verification.

## 4. Differential pairs

| Rule | Why |
|---|---|
| Route the two legs together with constant spacing | Keeps differential impedance constant and the pair's common-mode noise rejection high |
| Match lengths inside the pair (intra-pair skew) | Skew converts differential signal into common-mode noise (EMI) and closes the eye |
| Match in short bumps near the mismatch, not one big serpentine at the end | The mismatch should be corrected where it's created |
| Keep ≥ 3× the dielectric height between unrelated pairs (*typical*) | Crosstalk falls off quickly with distance from the reference plane |
| Symmetric breakouts and vias | Asymmetry is skew |

### Interface cheat-sheet (*typical* values — use the spec / vendor guide for sign-off)

| Interface | Data rate | Diff. impedance | Intra-pair skew | Notes |
|---|---|---|---|---|
| USB 2.0 HS | 480 Mb/s | 90 Ω | ~1 mm | ESD at connector |
| USB 3.2 Gen 1/2 | 5 / 10 Gb/s | 90 Ω | ≤ 0.13 mm | AC caps on TX |
| PCIe Gen3 / Gen4 / Gen5 | 8 / 16 / 32 GT/s | 85 Ω (often) | ≤ 0.13 mm | AC caps on TX, minimise via stubs; Gen5 usually needs low-loss laminate |
| Ethernet 1000BASE-T MDI | 4 × 250 Mb/s | 100 Ω | ~1 mm | Keep magnetics area clear of planes per PHY guide |
| HDMI 2.0 TMDS | 6 Gb/s/lane | 100 Ω | ≤ 0.13 mm | |
| MIPI CSI-2 / DSI D-PHY | up to ~2.5 Gb/s/lane | 100 Ω | tight; lane-to-clock matched | |
| DDR4 | 1600–3200 MT/s | 40 Ω SE / 80 Ω diff (common) | DQS/CK ≤ 0.13 mm | Fly-by CA, byte-lane matching to DQS |
| LPDDR4/4X | up to 4266 MT/s | ~40 Ω SE (vendor-specific) | tight | Point-to-point, usually needs HDI |

## 5. Power delivery and decoupling

- **Every capacitor has inductance.** A 0402 MLCC plus its vias is ~0.5–1 nH. The loop from IC pin to capacitor to plane matters more than the capacitance value.
- Put the smallest-value, smallest-package capacitors closest to the pins, with vias *inside* or immediately next to the pads. Shared vias between caps defeat the purpose.
- Use tightly coupled power/ground plane pairs (thin dielectric between them) on high-current, high-speed boards — the plane pair is itself a low-inductance capacitor.
- Size copper for current: an external 1 oz trace carries ~1 A per 0.3–0.5 mm of width for a ~10 °C rise (*typical*; use an IPC-2152 calculator like Saturn's). Planes and polygons for anything above a few amps.
- Switching regulators: identify the **hot loop** (where current changes abruptly — input cap and switches in a buck) and make it as small as possible, on one layer, over its own ground.

Read: MIT 6.622 Lecture 38 (layout), 6.334 chapters 13–14 (thermal, EMI).

## 6. BGA escape routing

- At a given pitch, count how many traces fit between two via pads: `(pitch − via_pad − 2×space) / (trace + space)`. At 0.8 mm pitch with 0.40 mm pads and 0.10/0.10 rules that's exactly one.
- With one trace per channel, each signal layer escapes about two rows. Rows needed ÷ 2 ≈ signal layers needed. Power and ground balls escape straight down to planes and free up layers.
- Below ~0.65 mm pitch through-hole vias no longer fit between balls → **via-in-pad** (filled and capped) or **HDI microvias**. Both cost money; check before choosing the part.

## 7. Design for manufacture (DFM)

- Read your fab's capability page and set those numbers as KiCad's board design rules **before** you route. Example: JLCPCB's multilayer minimums are 0.09 mm trace/space and 0.15 mm via drill (Oct 2026) — design comfortably above minimums when you can.
- Panelisation, fiducials, tooling holes and component-to-edge spacing are the assembler's concerns — ask them.
- Teardrops on small vias and pads, copper balancing on outer layers, and thermal reliefs on hand-soldered ground pads.
- Generate fab outputs from the command line so they're reproducible: `kicad-cli pcb export gerbers`, `... drill`, `... pos`, and (KiCad 8+) `kicad-cli pcb drc` in CI.

## 8. Before you order

- [ ] DRC and ERC clean with fab rules loaded
- [ ] Every high-speed net checked against its constraint file
- [ ] Stackup and impedances confirmed in writing by the fab
- [ ] 3D view: connectors at the edge, nothing colliding, mounting holes clear
- [ ] Test points for every rail; a current-limited first power-up plan
- [ ] Gerbers re-opened in a separate viewer (KiCad's Gerber viewer or the fab's) and inspected layer by layer
