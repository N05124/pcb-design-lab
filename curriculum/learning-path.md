# Learning path: from first board to 10-layer baseboards

Five stages. Each pairs theory (mostly MIT OpenCourseWare — see [mit-ocw.md](mit-ocw.md)) with practice (free tools and talks — see [open resources](../references/open-resources.md)) and ends with a challenge from the [challenge suite](../challenges/README.md) you should be able to pass before moving on.

Time estimates assume ~8 hours a week.

---

## Stage 0 — Tools and bench skills (2–3 weeks)

**Theory:** MIT 6.091 (lab skills), EC.S06 Practical Electronics.
**Practice:**
- Install KiCad (see [docs/02-kicad-workflow.md](../docs/02-kicad-workflow.md)) and do the official Getting Started tutorial end to end.
- Work through pcb.mit.edu's IAP labs — the closest thing MIT has to a PCB course.
- Order one tiny 2-layer board (an LED/regulator breakout) just to learn the fab and assembly loop.

**Done when:** you can go schematic → layout → Gerbers → a board in your hand without looking anything up.

## Stage 1 — Circuits you can trust (6–8 weeks)

**Theory:** MIT 6.002 (whole course), 6.101 labs, 6.003 frequency response and sampling.
**Practice:** read the Layout section of every datasheet you use; study one vendor evaluation board's layout per week and explain to yourself why each capacitor is where it is.
**Read:** [handbook §1 (currents)](../docs/01-design-handbook.md#1-think-in-currents-not-wires) and [§5 (power)](../docs/01-design-handbook.md#5-power-delivery-and-decoupling).

**Challenge:** [C01 precision ADC logger](../challenges/specs/C01-precision-adc.md).

## Stage 2 — Transmission lines and controlled impedance (6–8 weeks)

**Theory:** MIT 6.013 (with the free textbook) chapters on transmission lines and waves, 6.630 matching handout, 6.976 transmission-line lecture, 6.776 Smith chart handout.
**Practice:** use the KiCad impedance calculator and Saturn PCB Toolkit on your fab's real stackup; reproduce one result with openEMS.
**Read:** [handbook §2–4](../docs/01-design-handbook.md#2-when-is-a-trace-a-transmission-line).

**Challenges:** [C02 USB-C hub](../challenges/specs/C02-usb-c-hub.md), [C03 2.4 GHz radio](../challenges/specs/C03-rf-2g4.md).

## Stage 3 — Power and density (6–8 weeks)

**Theory:** MIT 6.622 (especially Lecture 38 on layout), 6.334 chapters on magnetics, thermal and EMI filters; RES.6-010 for regulator stability.
**Practice:** route a BGA escape by hand; then run this repo's [benchmark](../benchmark/README.md) on one board and compare the autorouter's escape to the human's.

**Challenges:** [C04 multiphase regulator](../challenges/specs/C04-multiphase-vrm.md), [C05 FPGA BGA fanout](../challenges/specs/C05-fpga-bga-fanout.md).

## Stage 4 — Memory and multi-gigabit serial (8–12 weeks)

**Theory:** MIT 6.111 (timing and clocking), 6.776 (high-speed circuits), 6.641 (coupling/crosstalk).
**Practice:** study an open DDR board line by line (Antmicro's are the best open examples — see [hard open boards](../references/hard-open-boards.md)); write a constraint file for it and run [`tools/check_constraints.py`](../tools/check_constraints.py) to see how close the real board comes.

**Challenges:** [C06 DDR4 memory-down](../challenges/specs/C06-ddr4-memory-down.md), [C07 PCIe Gen4 M.2](../challenges/specs/C07-pcie-m2.md).

## Stage 5 — Safety, HDI, and whole systems (ongoing)

**Theory:** IEC 60664-1 concepts for creepage and clearance (via vendor app notes), fab HDI design guides, module vendors' carrier-board design guides.

**Challenges:** [C08 isolated gate driver](../challenges/specs/C08-isolated-gate-driver.md), [C09 HDI 0.4 mm BGA](../challenges/specs/C09-hdi-0p4-bga.md), [C10 edge-AI baseboard](../challenges/specs/C10-edge-ai-baseboard.md).

---

## Going pro

At Stage 3 you can take paid review and small-layout work; by Stage 4 you can credibly enter the design contests listed in [bounties](../bounties/README.md). Keep every challenge solution in this repo — a graded, reproducible portfolio is worth more than a résumé line.
