# C01 — 24-bit precision ADC data logger ★☆☆☆☆

**Goal:** a USB-powered logger that digitises 4 differential sensor channels with a 24-bit delta-sigma ADC and keeps the measured noise floor close to the ADC's datasheet figure.

## Why it's hard

Nothing here is fast. What's hard is that a 24-bit converter resolves well under a microvolt, so every millivolt of ground bounce from the MCU and USB shows up in your data. This is the challenge that teaches return-current thinking before you ever see a GHz edge.

## Suggested blocks

- 24-bit ΔΣ ADC with PGA (ADS1262/ADS124S08/AD7124-class), external low-noise reference
- MCU with USB (STM32/RP2040-class)
- Input protection + RC anti-alias filters on each channel
- LDOs: separate analog and digital rails, ferrite or RC isolation between them
- USB-C receptacle (USB 2.0 only)

## Board budget

| Item | Budget |
|---|---|
| Layers | 2 (stretch) or 4 |
| Size | ≤ 60 × 40 mm |
| Fab rules | [JLC-standard](../README.md#default-fab-rule-set-jlc-standard-multilayer) |

## Pass / fail

1. Manufacturable: DRC clean, fully routed.
2. Constraints ([`C01.yaml`](../constraints/C01.yaml)): each channel's P/N input traces matched within 1 mm; analog nets stay out of the digital region (checked by the `layers` rule against a dedicated analog net class, plus review).
3. Electrically sound:
   - One solid ground plane (4-layer) or one unbroken ground pour (2-layer) — **no split ground** under the ADC. Partition by placement, not by cutting copper.
   - No digital trace runs under the ADC input pins, reference, or anti-alias capacitors.
   - Reference and AVDD decoupling within 2 mm of their pins.
4. Measured (if built): input-shorted noise at your chosen data rate within 1.5× the datasheet's typical value.

## Stretch

- Route it on 2 layers and still hit the noise target.
- Add a thermocouple cold-junction sensor thermally coupled to the input terminals.

## Read first

- MIT 6.101 and 6.002 lumped-circuit lectures — [curriculum](../../curriculum/mit-ocw.md)
- Your ADC's datasheet "Layout" section and evaluation-board layout files
