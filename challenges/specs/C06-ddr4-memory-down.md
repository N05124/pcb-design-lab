# C06 — SoC + 2× DDR4 x16 memory-down ★★★★☆

**Goal:** a 32-bit DDR4 interface (two x16 devices) running at DDR4-2400 or faster between an SoC or FPGA and soldered-down memory, passing the controller's memory training and a 24-hour memory test.

## Why it's hard

DDR4 at 2400 MT/s has a bit time of ~417 ps, and the timing budget left for the board is a fraction of that. The address/command/control bus is routed in **fly-by** topology (daisy-chained past each device, then terminated to Vtt) while data is point-to-point, each byte lane matched to its strobe. On top of the timing you need continuous reference planes for ~70 nets, Vtt and Vref rails with their own noise limits, and all of it fanning out from two BGAs.

## Suggested blocks

- SoC/FPGA with a DDR4 controller (i.MX8M/RK35xx/Zynq US+-class)
- 2× DDR4 x16 in 96-ball 0.8 mm FBGA
- VDDQ 1.2 V, VPP 2.5 V, Vtt tracking regulator (sink/source), Vref
- 36–40 Ω Vtt terminations at the end of the fly-by chain (per controller guide)

## Board budget

| Item | Budget |
|---|---|
| Layers | 8: Sig / GND / Sig / PWR / GND / Sig / GND / Sig (or vendor stackup) |
| Single-ended impedance | 40 Ω ±10 % (or as the controller guide requires) |
| Differential (CK, DQS) | 80 Ω ±10 % (or as required) |

## Pass / fail

1. Manufacturable: DRC clean, fully routed.
2. Constraints ([`C06.yaml`](../constraints/C06.yaml)) — example targets; **replace with your controller vendor's numbers**, which take precedence:
   - DQ and DM within each byte lane matched to that lane's DQS within ±0.5 mm (after adding package pin delay)
   - DQS and CK pairs: intra-pair skew ≤ 0.13 mm
   - Address/command/control matched to CK within ±2.5 mm at each device in the fly-by chain
   - Each byte lane routed on one layer (or the same layer pair), no lane splits layers mid-route
3. Electrically sound: no DDR net crosses a split; Vtt island placed at the end of the chain with ≥ 1 decoupling cap per 4 terminations; Vref decoupled at every device.
4. Measured (if built): controller training passes; 24 h memtest at rated speed with zero errors.

> The included `check_constraints.py` sums track length only. For DDR4 sign-off, also add via-barrel length and the vendor's package (pin) delay tables — most controller guides publish them.

## Stretch

- DDR4-3200.
- Replace with LPDDR4/4X in a single package (point-to-point, but tighter).

## Read first

- Your memory controller's PCB design guide (DDR routing chapter)
- Antmicro's open DDR test boards — see [`references/hard-open-boards.md`](../../references/hard-open-boards.md)
- MIT 6.111 (timing), 6.630/6.976 (transmission lines) — [curriculum](../../curriculum/mit-ocw.md)
