# C02 — USB-C 3.2 Gen 1 four-port hub ★★☆☆☆

**Goal:** a bus- or self-powered hub with one USB-C upstream port and four USB-A or USB-C downstream ports, all running 5 Gb/s SuperSpeed.

## Why it's hard

Your first controlled-impedance board. Ten SuperSpeed differential pairs (TX/RX for 5 ports) plus five USB 2.0 pairs must hold 90 Ω, stay length-matched inside each pair, keep a continuous reference plane, and break out of a reversible USB-C connector whose pins cross over.

## Suggested blocks

- 4-port USB 3.x hub controller (e.g. VL817/GL3523/TUSB8041-class)
- USB-C receptacles, CC logic, ESD arrays on every external pair
- 100 nF AC-coupling capacitors on the SuperSpeed TX pairs, placed per the hub vendor's guide
- 25 MHz crystal, 3.3 V and 1.1–1.2 V core regulators, per-port power switches

## Board budget

| Item | Budget |
|---|---|
| Layers | 4: Sig / GND / PWR / Sig |
| Size | ≤ 80 × 40 mm |
| Impedance | 90 Ω ±10 % differential for SS and USB 2.0 pairs; compute widths for your fab's actual stackup |

## Pass / fail

1. Manufacturable: DRC clean, fully routed.
2. Constraints ([`C02.yaml`](../constraints/C02.yaml)):
   - Intra-pair skew ≤ 0.13 mm (5 mil) on every SuperSpeed pair, ≤ 1.3 mm on USB 2.0 pairs
   - ≤ 2 vias per SuperSpeed net
   - SuperSpeed pairs ≤ 100 mm long
3. Electrically sound: every SS pair over unbroken GND; ground stitching via beside each signal via; ESD array between connector and everything else; AC caps symmetric on both legs.
4. Efficiency score: area, via count.

## Stretch

- Add USB Power Delivery (a PD controller and a 20 V input) on the upstream port.
- Simulate one SS pair's insertion and return loss with openEMS and report it.

## Read first

- Your hub controller's layout guide (most vendors publish one)
- MIT 6.630 transmission-line notes; 6.776 Smith chart handout — [curriculum](../../curriculum/mit-ocw.md)
- Open references in [`references/hard-open-boards.md`](../../references/hard-open-boards.md)
