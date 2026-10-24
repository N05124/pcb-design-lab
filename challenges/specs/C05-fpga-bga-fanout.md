# C05 — FPGA in a 0.8 mm-pitch, 484-ball BGA ★★★☆☆

**Goal:** a development board for a mid-range FPGA in a 484-ball, 0.8 mm-pitch BGA with every user I/O bank brought out to connectors, plus configuration flash, JTAG, oscillators and the full power tree.

## Why it's hard

BGA escape routing is a geometry puzzle. With 0.8 mm pitch you get exactly one trace between adjacent via pads at JLC-standard rules, so each signal layer can escape roughly two rows of balls. A 22 × 22 array needs enough layers to get the inner rows out while leaving room for power and ground planes — and every power rail wants its own decoupling under the BGA, competing for the same via sites.

## Suggested blocks

- FPGA in a 484-ball 0.8 mm BGA (Artix-7/Spartan-7/ECP5/Cyclone-class); obey its pin-planning guide
- QSPI configuration flash, JTAG header, 2 oscillators
- 4–6 regulators (core, aux, I/O banks, transceiver if present)
- Two high-density board-to-board connectors carrying all user I/O

## Board budget

| Item | Budget |
|---|---|
| Layers | 6 (target) — 8 allowed with a score penalty |
| Via | 0.20 / 0.40 mm through-hole only — **no HDI** |
| Trace / space in fanout | 0.09 / 0.09 mm allowed |

## Pass / fail

1. Manufacturable: DRC clean; **100 % of connected balls escaped and routed**.
2. Constraints ([`C05.yaml`](../constraints/C05.yaml)): each I/O bank's nets within its connector group match to ±5 mm; clocks use ≤ 2 vias.
3. Electrically sound: every power ball has a via to its plane; ≥ 1 decoupling capacitor per 4 power balls on the underside; no plane split crossing under a clock.
4. Efficiency: layer count and via count.

## Stretch

- Do it in 4 layers by giving up some outer-row I/O (state how many).
- Add a 4-lane transceiver bank routed to an SFP+ cage at 10 Gb/s.

## Read first

- Your FPGA vendor's PCB design guide (all major vendors publish one, including BGA escape tables)
- Open reference boards in [`references/hard-open-boards.md`](../../references/hard-open-boards.md)
