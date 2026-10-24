# KiCad workflow for complex boards

KiCad is free, open source (GPL), runs on Windows/macOS/Linux, has no licence-imposed layer or size limits (up to 32 copper layers), and is scriptable from Python and the command line. It's what this repo uses throughout. Latest stable at the time of writing is **KiCad 10.0.7** ([download](https://www.kicad.org/download/)); the benchmark runs on 7.0.11 because that's what Ubuntu 24.04 packages. Menu names below are from KiCad 8–10.

## 1. Project setup (do this before drawing anything)

1. **Pick the fab first.** Copy its capability numbers into *Board Setup → Design Rules → Constraints* (min track, clearance, via drill/diameter, annular ring, hole-to-hole, copper-to-edge).
2. **Define the stackup** in *Board Setup → Board Stackup* using the fab's real dielectric thicknesses. Ask the fab for its controlled-impedance stackup sheet.
3. **Create net classes** for every impedance/current class (e.g. `Default`, `Power_2A`, `USB_90R`, `PCIe_85R`, `DDR_SE_40R`), with track width, clearance, diff-pair width and gap computed from the stackup (*Tools → Calculator Tools → Transmission Lines*).
4. **Assign nets to classes by pattern** (*Net Classes → Netclass assignments*, e.g. `/USB_SS*` → `USB_90R`) so new nets get the right rules automatically.
5. **Custom rules** for anything the dialog can't express go in a `.kicad_dru` file — clearance between HV and LV net classes, length windows, via counts, keep-outs. Example:

```lisp
(version 1)
(rule "PCIe intra-pair skew"
  (condition "A.inDiffPair('/PCIE_*')")
  (constraint skew (max 0.13mm)))
(rule "HV to LV creepage"
  (condition "A.NetClass == 'HV' && B.NetClass == 'LV'")
  (constraint clearance (min 8mm)))
(rule "DDR byte 0 length window"
  (condition "A.NetName == '/DDR_DQ0' || A.NetName == '/DDR_DQ1'")
  (constraint length (min 30mm) (max 31mm)))
```

## 2. Schematic

- Use hierarchical sheets per functional block (power, MCU, memory, each interface). Hard boards are only reviewable when each sheet fits on a page.
- Name every net that matters (`/USB_SSTX_P` not `Net-(U3-Pad12)`) — names drive net-class patterns, constraint files and review.
- Diff pairs are recognised by suffix: `_P`/`_N` or `+`/`-`.
- Run ERC until it's clean. Set pin types correctly on custom symbols or ERC is meaningless.

## 3. Placement (≈ 60 % of the quality of the final board)

Order: mechanical (connectors, holes, keep-outs) → the big ICs → whatever sits between them on the critical paths (memory, PHYs, retimers) → power stages → decoupling → everything else. Route critical nets *as you place* to prove they fit; don't place everything and then discover the DDR can't escape.

## 4. Routing

| Tool | Shortcut | Use for |
|---|---|---|
| Interactive router (walkaround / shove) | `X` | Everything |
| Differential pair router | `6` | Any `_P`/`_N` pair |
| Length tuning (single / pair / skew) | `7` / `8` / `9` | Matching to the net class or `.kicad_dru` length rules |
| Via stitching / via fence | Place → Add Vias; or plugins | Ground stitching along RF and high-speed edges |
| Teardrops | Edit → Add Teardrops | Mechanical reliability on small pads/vias |

Enable *Board Setup → Constraints → "Include stackup height in track length calculations"* so via barrels count toward matched lengths, and keep the net inspector (*Inspect → Net Inspector*) open to watch lengths and via counts live.

### Autorouting

KiCad has no built-in autorouter. The standard route is **Freerouting** via Specctra DSN:

1. *File → Export → Specctra DSN*
2. Run Freerouting (GUI, or headless: `java -jar freerouting.jar -de board.dsn -do board.ses -mp 100 --gui.enabled=false`)
3. *File → Import → Specctra Session*

Freerouting (and every autorouter) knows nothing about impedance, return paths, length matching beyond basics, or which nets are sensitive. Use it for the low-speed remainder **after** you've hand-routed critical nets and locked them. The [benchmark](../benchmark/README.md) shows exactly where it falls short — including one trap: it treats copper pours as always-connected planes, but once its tracks chop up a pour KiCad's refill can leave pads isolated.

## 5. Checks

- DRC with *"Test for parity between PCB and schematic"* on.
- Net inspector: sort by length and via count for each high-speed class.
- [`tools/check_constraints.py`](../tools/check_constraints.py) for a scripted pass/fail report (CI-friendly).
- 3D viewer: connector overhangs, tall parts under heatsinks, mounting holes.

## 6. Outputs and automation

KiCad ships `kicad-cli`, so outputs can be reproducible and run in CI:

```bash
kicad-cli pcb export gerbers -o fab/ board.kicad_pcb
kicad-cli pcb export drill   -o fab/ board.kicad_pcb
kicad-cli pcb export pos     -o fab/board-pos.csv board.kicad_pcb
kicad-cli sch export bom     -o fab/board-bom.csv board.kicad_sch   # KiCad 8+
kicad-cli pcb export step    -o mech/board.step board.kicad_pcb
kicad-cli pcb drc            -o drc.rpt --exit-code-violations board.kicad_pcb   # KiCad 8+
kicad-cli sch erc            -o erc.rpt --exit-code-violations board.kicad_sch   # KiCad 8+
```

For full release automation, [KiBot](https://github.com/INTI-CMNB/KiBot) wraps all of this plus interactive BOMs, panelisation and PDF schematics in one YAML file.

### Python

`import pcbnew` gives full board access (the [benchmark scripts](../benchmark/scripts/pcbbench.py) are a worked example: loading, measuring, deleting and adding tracks/vias, refilling zones, running DRC, exporting DSN). From KiCad 9, the newer **IPC API** (`kicad-python` package) talks to a running KiCad instance and is the long-term direction; the SWIG `pcbnew` module is being phased out.
