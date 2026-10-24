# Hard open-source boards worth studying

Real, published KiCad designs that solve the problems in the [challenge suite](../challenges/README.md). Studying how experienced engineers routed DDR, BGA escape or PCIe is the fastest way to learn it.

"K7" means the file opens in KiCad 7 at the listed ref (needed for this repo's [benchmark](../benchmark/README.md)); newer KiCad opens all of them. Net/via counts are approximate.

## Ranked from moderate to extreme

| Board | Layers | Nets / vias | What to study | Ref (K7-readable) | Licence |
|---|---|---|---|---|---|
| [KiCad demo StickHub](https://github.com/KiCad/kicad-source-mirror/tree/7.0.11/demos/stickhub) | 2 | 48 / 88 | Small USB hub; pours and diff pairs on 2 layers | tag `7.0.11` | GPL |
| [STRF](https://github.com/pms67/STRF-Kicad) | 4 | 50 / 70 | Tiny RF + MCU module at 0.5 mm pitch | HEAD | see repo |
| [PocketBeagle](https://github.com/beagleboard/pocketbeagle) | 4 | 188 / 171 | OSD3358 system-in-package BGA on a 55 × 35 mm board; also ships EAGLE files — a real EAGLE→KiCad example | HEAD | CC BY-SA |
| [BeagleConnect Freedom](https://github.com/beagleboard/beagleconnect-freedom) | 4 | 162 / 399 | Sub-GHz + 2.4 GHz radio, RF layout | HEAD | see repo |
| [Glasgow revC3](https://github.com/GlasgowEmbedded/glasgow) | 4 | 252 / 417 | iCE40 0.8 mm BGA-121 + USB HS, compact 4-layer | `main` (revC3 folder) | see repo |
| [ULX3S](https://github.com/emard/ulx3s) | 4 | 330 / 555 | ECP5 BGA-381 escaped on **only 4 layers**, SDRAM, 0.127 mm traces | `master` | modified MIT |
| [HackRF One](https://github.com/greatscottgadgets/hackrf) | 4 | 380 / 499 | Mixed RF/digital, RF switches, impedance-controlled RF paths | `main` | GPL-2 |
| [Antmicro LPDDR4 testbed](https://github.com/antmicro/lpddr4-testbed) | 6 | 262 / 249 | LPDDR4 BGA-200 at 0.8 × 0.65 mm pitch to an edge connector, length matching | `75e82c1` | Apache-2.0 |
| [ThunderScope FPGA module Rev2](https://github.com/EEVengers/ThunderScope) | 6 | 390 / 670 | Artix-7 CSG325 on a 40 × 50 mm module with a fast ADC interface | `98cfa16` | MIT |
| [Cynthion](https://github.com/greatscottgadgets/cynthion-hardware) | 6 | 376 / — | ECP5 + three USB HS PHYs | HEAD | CERN-OHL-P |
| [ButterStick r1.0](https://github.com/gregdavill/ButterStick) | 8 | 350 / 1164 | ECP5 + 2× DDR3L, Gigabit Ethernet, ~40 diff pairs | `main` | CERN-OHL 1.2 |
| [Olimex iMX8MP SOM Rev B](https://github.com/OLIMEX/iMX8MP-SOM) | 6 | 423 / 1007 | **0.5 mm FCBGA-548** + LPDDR4, 0.08 mm traces — extremely dense without HDI | `main` | GPL |
| [Antmicro Jetson Orin baseboard](https://github.com/antmicro/jetson-orin-baseboard) | 8 | 776 / 1268 | ~100 diff pairs: PCIe, USB 3, CSI-2, HDMI, GbE + PoE (reference for [C10](../challenges/specs/C10-edge-ai-baseboard.md)) | tag `rev.1.1.6-ch` | Apache-2.0 |
| [Antmicro Kria K26 devboard](https://github.com/antmicro/kria-k26-devboard) | 8 | 805 / 1902 | SoM connectors, 4× USB 3.2, DisplayPort, 2× 4-lane MIPI | `main` | Apache-2.0 |
| [Antmicro RDIMM DDR4 tester](https://github.com/antmicro/rdimm-ddr4-tester) | **12** | 920 / 2484 | Kintex-7 FFG676 driving a DDR4 RDIMM slot, **289 blind vias** (reference for [C06](../challenges/specs/C06-ddr4-memory-down.md)) | `main` | Apache-2.0 |

## Also worth a look

- Antmicro: [lpddr4-test-board](https://github.com/antmicro/lpddr4-test-board) (8 layers, Kintex-7, blind vias), [sodimm-ddr5-tester](https://github.com/antmicro/sodimm-ddr5-tester) (12 layers, PCIe x4 edge), [ddr5-testbed](https://github.com/antmicro/ddr5-testbed), [jetson-nano-baseboard](https://github.com/antmicro/jetson-nano-baseboard), [snapdragon-845-baseboard](https://github.com/antmicro/snapdragon-845-baseboard). Antmicro publishes more complex open hardware than anyone else; most current HEADs need KiCad 9+.
- [Olimex A64-OLinuXino](https://github.com/OLIMEX/OLINUXINO) — FBGA-396 + 2× DDR3 on 6 layers.
- KiCad 10's **vme-wren** demo (`demos/vme-wren/` in [kicad-source-mirror](https://github.com/KiCad/kicad-source-mirror)) — 12 layers, ~1,800 nets, the largest open KiCad board found. KiCad 9+ format.
- [Antmicro Jetson AGX Thor baseboard](https://github.com/antmicro/jetson-agx-thor-baseboard), [Kintex-410T devboard](https://github.com/antmicro/kintex-410t-devboard), [HaasoscopePro](https://github.com/drandyhaas/HaasoscopePro) — 10 layers, KiCad 9 format.

## Not KiCad / not reachable

LimeSDR Mini and Precursor are Altium. MNT Reform lives on source.mnt.re (KiCad, CERN-OHL-S) — worth studying but not mirrored on GitHub.
