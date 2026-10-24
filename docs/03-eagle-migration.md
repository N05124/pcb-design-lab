# EAGLE: end of life and how to migrate

## Status (checked 2026-10-23)

- Autodesk **announced EAGLE's retirement on 7 June 2023** ([Autodesk blog](https://www.autodesk.com/products/fusion-360/blog/future-of-autodesk-eagle-fusion-360-electronics/)) and **ended it on 7 June 2026** ([Autodesk FAQ](https://autodesk.com/eagleannouncement)). Sales, support, subscription licensing, downloads and the free tier have stopped.
- Perpetual licences bought before Autodesk's acquisition still run, but get no updates.
- **Practical upshot:** don't start new work in EAGLE. Existing `.sch`/`.brd` files still matter — a lot of open hardware (Arduino, SparkFun, Adafruit, early BeagleBoard designs) was published in EAGLE format — so you need a way to read and convert them.

## Option 1 — KiCad (free, recommended)

KiCad imports EAGLE 6.x and newer XML files (schematic and board together) via **File → Import → Non-KiCad Project** in the project manager, or board-only via the PCB editor's import menu. It maps EAGLE layers to KiCad layers and converts libraries into project-local symbol and footprint libraries.

Workflow that works well:

1. Put the `.sch` and `.brd` with the same base name in one folder and import the *project*, not the board alone — that keeps schematic ↔ board links so you can keep editing both.
2. When the layer-mapping dialog appears, check every non-standard EAGLE layer (tStop/bStop, tCream, user layers) lands where you expect.
3. Immediately run ERC and DRC. Expect noise from EAGLE's different defaults (thermal reliefs, polygon pour rank, restrict layers). Re-pour all zones.
4. Re-create net classes and design rules from the EAGLE DRU — they don't carry over completely.
5. Compare Gerbers from the original (if you have them) against KiCad's in a Gerber viewer before trusting the conversion.

Known issues:
- A [KiCad forum report](https://forum.kicad.info/t/howto-importing-eagle-boards-use-legacy-7-x-format/51767) describes KiCad 8.0.3 silently failing on boards saved by EAGLE 9.6; the workaround there was saving a copy in EAGLE 7.x format first (only possible if you still have a working EAGLE).
- The importer is interactive (it asks for layer mapping). In this repo's headless test, KiCad 7.0.11's Python `LoadBoard(path, IO_MGR.EAGLE)` on PocketBeagle's EAGLE board failed with an undefined-layer error — so plan to do EAGLE conversions once, in the GUI, and commit the resulting KiCad files.

## Option 2 — Autodesk Fusion (Electronics workspace)

Autodesk's official path. Fusion opens EAGLE files directly and keeps the EAGLE-style workflow and scripting (ULPs). The free personal-use tier is limited (2 signal layers, 2 schematic sheets, 80 cm² board at time of writing), so complex boards need a paid subscription.

## Option 3 — Other tools

Altium, OrCAD/Allegro and most commercial tools import EAGLE XML. Of the free alternatives, Horizon EDA and LibrePCB have no general EAGLE importer comparable to KiCad's.

## If you're an EAGLE user learning KiCad

| EAGLE | KiCad |
|---|---|
| Library (.lbr) with symbol + package + device | Separate symbol libraries and footprint libraries; the link lives on the schematic symbol's *Footprint* field |
| ULP scripts | Python (`pcbnew` module / IPC API from KiCad 9) and `kicad-cli` |
| DRU file | Board Setup → Design Rules, plus `.kicad_dru` custom rules (more expressive) |
| Polygon rank | Zone priority |
| Ratsnest command | Automatic; zones refill with `B` |
| Autorouter (built in) | None built in; use Freerouting via Specctra DSN/SES (see [workflow](02-kicad-workflow.md#autorouting)) |
| Layers 1–16 | F.Cu, In1.Cu…In30.Cu, B.Cu |
