# C09 — Phone-class SoC in a 0.4 mm-pitch BGA (HDI) ★★★★★

**Goal:** a compact compute module around an application processor in a 0.4–0.5 mm-pitch BGA with LPDDR4X in a stacked or adjacent package, eMMC/UFS, PMIC and MIPI DSI/CSI connectors — sized like a phone mainboard.

## Why it's hard

At 0.4 mm pitch there is no room for a through-hole via between balls. You must use **HDI**: laser-drilled microvias in the pads (via-in-pad, filled and capped), stacked or staggered across build-up layers, with traces of ~0.05–0.075 mm. The stackup itself becomes a design decision (1+N+1, 2+N+2, any-layer), and fab cost roughly doubles with each extra lamination cycle. LPDDR4X at 4266 MT/s and MIPI at multi-Gb/s run inside this density.

## Suggested blocks

- Application processor in ≤ 0.5 mm-pitch BGA
- LPDDR4X (adjacent package), eMMC or UFS
- PMIC, buck/LDO array, battery charger
- MIPI DSI and CSI-2 FPC connectors, USB-C

## Board budget

| Item | Budget |
|---|---|
| Layers | 8–10 HDI (2+N+2 target) |
| Microvia | Laser 0.10 mm drill / 0.25 mm pad, via-in-pad filled & capped |
| Trace / space | 0.075 / 0.075 mm under the SoC; 0.10 / 0.10 elsewhere |
| Size | ≤ 50 × 35 mm |

## Pass / fail

1. Manufacturable: DRC clean against a **named fab's published HDI rules** (attach them), fully routed.
2. Constraints ([`C09.yaml`](../constraints/C09.yaml)): LPDDR4X byte lanes matched per the SoC guide; MIPI lanes matched to their clock within ±0.2 mm; diff pairs intra-pair ≤ 0.05 mm.
3. Electrically sound: stacked microvias only where the fab permits; no microvia lands on another without a fill/cap step; PDN impedance target met for the SoC core rail (simulate or estimate).
4. Efficiency: lamination cycles, layer count, area.

## Stretch

- Any-layer HDI at ≤ 40 × 30 mm.

## Read first

- SoC vendor hardware design guide (HDI stackup chapter)
- Fab HDI design guides (JLCPCB, PCBWay, Sierra Circuits all publish one)
