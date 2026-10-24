# Tools

| Script | What it does | Runs with |
|---|---|---|
| [`check_constraints.py`](check_constraints.py) | Grades a routed board against a YAML file of high-speed rules: diff-pair skew, length-matched groups (optionally against a reference strobe/clock), max vias, allowed widths, allowed layers, "everything routed". Exit code 0 = all pass, so it drops into CI. | KiCad's Python (`import pcbnew`) + PyYAML |

## Example

```bash
python3 tools/check_constraints.py /usr/share/kicad/demos/video/video.kicad_pcb tools/examples/video_demo_constraints.yaml
```

Output on KiCad's own `video` demo (a 4-layer FPGA + 32-bit video RAM board that was never designed to modern length rules):

```
[FAIL] Data bus DQ0-7 length-matched within 10 mm (match_group)
        8 nets, target 332.52 mm, worst /DQ2 off by 21.45 mm
[FAIL] Data bus DQ0-31 length-matched within 25 mm (match_group)
        32 nets, target 332.52 mm, worst /DQ25 off by 291.12 mm
[FAIL] Data bus uses at most 4 vias per net (max_vias)
        /DQ3: 7 vias  ...
[FAIL] Data bus stays on outer signal layers (layers)
        /DQ0: on VCC_layer  ...
[PASS] Every signal net has copper (routed)
1/5 rules passed
```

Note what it caught: the data bus is routed across the **power plane layer**, which is legitimate on a slow board but would break the return path of a fast one.

## Limitations

Lengths are summed track and arc lengths. Via barrels and in-package pin delay are not included — add them for DDR4/PCIe sign-off, or use KiCad's own length tuner with "include stackup height" enabled.

Templates for every challenge live in [`../challenges/constraints/`](../challenges/constraints/).
