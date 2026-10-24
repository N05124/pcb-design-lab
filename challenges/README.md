# Hard-board challenge suite

Ten board-design challenges, ordered from "first serious board" to "what a senior hardware team ships". Each one names the electrical problem that makes it hard, a layer and fab budget, and **pass/fail criteria you can check with a script** rather than by eye.

Use them three ways:

- **As a curriculum.** Do them in order; each adds one new class of problem.
- **As a benchmark for tools.** Feed the same netlist and placement to a human, an autorouter, or an AI layout tool and grade the result with the same rules.
- **As a portfolio.** A clean C05 or C07 is a credible thing to show a client or hiring manager.

## How grading works

Every challenge is graded on four gates, in order. Fail an earlier gate and later ones don't count.

| Gate | What is checked | How |
|---|---|---|
| 1. Manufacturable | Zero DRC errors against the fab rule set you declared; zero unrouted connections | KiCad DRC (`kicad-cli pcb drc` in KiCad 8+, or `pcbnew.WriteDRCReport` in 7) |
| 2. Constraint-clean | Every rule in the challenge's constraint file passes | [`tools/check_constraints.py`](../tools/check_constraints.py) |
| 3. Electrically sound | Stackup impedance within ±10 % of target; return paths continuous under every high-speed net; decoupling within the stated distance | Stackup calculator (Saturn PCB Toolkit, KiCad's calculator, or openEMS) + review checklist below |
| 4. Efficient | Layer count, board area, via count and cost vs. the reference budget | Numbers from the benchmark scripts' `board_stats()` |

Gates 1 and 2 are fully automatic. Gate 3 is half automatic (impedance) and half review. Gate 4 is a score, not a pass/fail.

### Default fab rule set ("JLC-standard multilayer")

Unless a challenge says otherwise, design to these. They sit comfortably inside JLCPCB's published multilayer capabilities as of Oct 2026 (0.09 mm trace/space minimum, 0.15 mm minimum via hole, 0.25 mm minimum via pad, ±10 % impedance) — always re-check your fab's current page before ordering.

| Rule | Value |
|---|---|
| Min trace / space | 0.10 mm / 0.10 mm (0.09 mm allowed inside BGA fanout) |
| Via (drill / pad) | 0.20 mm / 0.40 mm preferred; 0.15 / 0.30 mm minimum |
| Copper to board edge | 0.30 mm |
| Annular ring (PTH) | 0.15 mm minimum |
| Impedance tolerance | ±10 % |
| Board thickness | 1.6 mm unless stated |

### Review checklist (gate 3)

- [ ] Every high-speed net has an unbroken reference plane directly under it, including at layer changes (stitching via within ~1 mm of each signal via that changes reference)
- [ ] No high-speed net crosses a plane split or a slot
- [ ] Each IC power pin has a decoupling capacitor whose loop (pin → cap → via → plane) is as short as the package allows
- [ ] Switching power loops (input cap → switch → return) are minimised and on one layer
- [ ] Crystal / oscillator traces are short, guarded, and have nothing routed underneath
- [ ] Connectors that leave the box have ESD protection placed at the connector, before anything else
- [ ] Test points exist for every rail and every bus you'll need to debug

---

## The challenges

| ID | Board | What makes it hard | Layers | Difficulty |
|---|---|---|---|---|
| [C01](specs/C01-precision-adc.md) | 24-bit ADC data logger | Mixed-signal grounding, µV noise floor | 2–4 | ★☆☆☆☆ |
| [C02](specs/C02-usb-c-hub.md) | USB-C 3.2 Gen 1 hub | 90 Ω differential pairs, intra-pair skew, connector breakout | 4 | ★★☆☆☆ |
| [C03](specs/C03-rf-2g4.md) | 2.4 GHz radio module with PCB antenna | 50 Ω coplanar waveguide, matching network, antenna keep-out | 4 | ★★☆☆☆ |
| [C04](specs/C04-multiphase-vrm.md) | 12 V → 0.9 V / 40 A multiphase regulator | Current density, thermal vias, switching-loop inductance | 6 | ★★★☆☆ |
| [C05](specs/C05-fpga-bga-fanout.md) | FPGA in 0.8 mm BGA (484 balls) | Escape routing every ball within 6 layers | 6 | ★★★☆☆ |
| [C06](specs/C06-ddr4-memory-down.md) | SoC + 2× DDR4 x16 memory-down | Fly-by topology, byte-lane matching, Vtt termination | 8 | ★★★★☆ |
| [C07](specs/C07-pcie-m2.md) | PCIe Gen4 x4 M.2 carrier | 85 Ω pairs, AC caps, insertion-loss budget at 8 GHz | 6–8 | ★★★★☆ |
| [C08](specs/C08-isolated-gate-driver.md) | 800 V SiC half-bridge gate driver | Creepage/clearance, isolation barrier, dV/dt coupling | 4 | ★★★★☆ |
| [C09](specs/C09-hdi-0p4-bga.md) | Phone-class SoC, 0.4 mm-pitch BGA | Needs HDI: laser microvias, via-in-pad, any-layer or 2+N+2 | 8–10 HDI | ★★★★★ |
| [C10](specs/C10-edge-ai-baseboard.md) | Edge-AI module baseboard (Jetson-class) | Everything at once: PCIe, USB 3, 10GbE, MIPI CSI-2, HDMI, power | 10–12 | ★★★★★ |

Each spec file links to open-source reference boards where real engineers solved the same problem. Study those before you start.

## Submitting a solution

Put your KiCad project in `solutions/<challenge-id>/<your-handle>/`, include the filled-in constraint file, and run:

```bash
python3 tools/check_constraints.py solutions/C02/you/hub.kicad_pcb challenges/constraints/C02.yaml
```

Paste the output into your PR description.
