# C07 — PCIe Gen4 x4 M.2 carrier ★★★★☆

**Goal:** a carrier that takes PCIe Gen4 x4 from a host connector (x4 edge fingers or a high-speed board-to-board connector) to an M.2 M-key socket, with link training at Gen4 and a clean loss budget.

## Why it's hard

Gen4 runs 16 GT/s with a Nyquist frequency of 8 GHz. At 8 GHz, ordinary FR-4 loses roughly 1 dB per inch of trace, connectors and vias add reflections, and the via stubs left from through-hole vias resonate. You have to budget insertion loss end to end, minimise and back-drill (or avoid) stubs, place AC-coupling capacitors with voided reference planes beneath their pads, and choose a lower-loss laminate if the route is long.

## Suggested blocks

- PCIe x4 host interface: edge fingers or a high-speed mezzanine connector
- M.2 2280 M-key socket
- 100 MHz HCSL reference clock buffer, PERST#/CLKREQ# logic
- 3.3 V / 3 A supply for the SSD

## Board budget

| Item | Budget |
|---|---|
| Layers | 6–8 |
| Differential impedance | 85 Ω ±10 % (common choice for PCIe; check your connector and host) |
| Laminate | Standard FR-4 allowed if total route ≤ 75 mm; otherwise mid-loss |

## Pass / fail

1. Manufacturable: DRC clean, fully routed.
2. Constraints ([`C07.yaml`](../constraints/C07.yaml)):
   - Intra-pair skew ≤ 0.13 mm for every TX/RX pair and REFCLK
   - ≤ 2 vias per lane net; no vias on the RX side between connector and socket if avoidable
   - TX/RX lane length ≤ 75 mm
3. Electrically sound: AC caps (220 nF class, check spec) on TX only, placed symmetrically; reference-plane void under cap pads; ground via next to every signal via; pairs never cross splits.
4. Simulated: insertion loss of the longest lane ≤ the M.2/CEM channel allocation you document (use openEMS or a vendor tool).
5. Measured (if built): `lspci -vv` shows link at 16 GT/s x4; sustained SSD throughput ≥ 6 GB/s.

## Stretch

- PCIe Gen5 (32 GT/s, Nyquist 16 GHz) with a low-loss laminate and back-drilled vias.
- Add a PCIe switch and two M.2 sockets.

## Read first

- PCI-SIG / connector vendor layout notes
- MIT 6.976 transmission-line lecture — [curriculum](../../curriculum/mit-ocw.md)
- Antmicro's open baseboards (PCIe routing) — [`references/hard-open-boards.md`](../../references/hard-open-boards.md)
