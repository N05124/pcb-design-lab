# C10 — Edge-AI module baseboard (Jetson-class) ★★★★★

**Goal:** a carrier board for a high-end system-on-module (Jetson Orin / Kria / CM-class) exposing PCIe Gen4 x4 (M.2), 2× USB 3.2, 10GBASE-T or 2× 2.5GbE, 4× MIPI CSI-2 camera ports, HDMI 2.0 and a 9–20 V input power tree.

## Why it's hard

Every previous challenge at once, on one board, under one stackup. Thirty-plus high-speed differential pairs at four different impedances leave a 699-pin (or similar) module connector and have to share layers without crosstalk. The power tree feeds a module drawing tens of watts. Mechanical constraints (module keep-outs, connector edges, mounting holes, heatsink) fix half the placement before you start.

## Suggested blocks

- SoM connector per the module's carrier design guide
- M.2 M-key (NVMe), M.2 E-key (Wi-Fi), USB 3.2 Gen2 Type-C + Type-A, 10GBASE-T PHY + magjack (or 2.5GbE PHYs), HDMI with retimer/redriver, 4× 22-pin CSI-2 FPC
- 9–20 V input, buck converters, power sequencing, fan controller

## Board budget

| Item | Budget |
|---|---|
| Layers | 10–12 |
| Impedances | 85 Ω (PCIe), 90 Ω (USB), 100 Ω (Ethernet, HDMI, CSI-2), 50 Ω single-ended — all ±10 % on one stackup |
| Size | Match the module vendor's reference carrier footprint or smaller |

## Pass / fail

1. Manufacturable: DRC clean, fully routed.
2. Constraints ([`C10.yaml`](../constraints/C10.yaml)): every interface's skew and length limits from the module's carrier design guide.
3. Electrically sound: each impedance class verified against the stackup; aggressor/victim spacing ≥ 3× dielectric height between unrelated high-speed pairs; return-path stitching at every layer change.
4. Measured (if built): every interface links at full speed; board boots the vendor's reference OS image.

## Read first

- The module vendor's carrier board design guide
- Antmicro's open Jetson/Kria baseboards — [`references/hard-open-boards.md`](../../references/hard-open-boards.md)
