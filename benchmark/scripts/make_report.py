#!/usr/bin/env python3
"""Turn results/runs.jsonl into results/results.csv and results/REPORT_TABLES.md."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "results"
MANIFEST = json.loads((HERE.parent / "boards.json").read_text())
NAMES = {b["id"]: b for b in MANIFEST["boards"]}

rows = []
for line in (RES / "runs.jsonl").read_text().splitlines():
    if not line.strip():
        continue
    r = json.loads(line)
    o = r.get("original", {})
    os_, od = o.get("stats", {}), o.get("drc", {})
    rt = r.get("routed", {})
    rs, rd = rt.get("stats", {}), rt.get("drc", {})
    start = rt.get("unconnected_before", o.get("unrouted_after_strip"))
    left = rt.get("unconnected_after", rd.get("unconnected"))
    # New DRC violations = routed minus original, ignoring 'unconnected_items' (counted separately)
    o_types = dict(od.get("by_type", {}))
    r_types = dict(rd.get("by_type", {}))
    o_types.pop("unconnected_items", None)
    r_types.pop("unconnected_items", None)
    new_viol = {k: r_types.get(k, 0) - o_types.get(k, 0) for k in set(o_types) | set(r_types)}
    new_viol = {k: v for k, v in new_viol.items() if v > 0}
    completion = None
    if start and left is not None:
        completion = round(100.0 * (start - left) / start, 1)
    rows.append({
        "board": r["board"],
        "board_name": NAMES.get(r["board"], {}).get("name", r["board"]),
        "config": r["config"],
        "layers": os_.get("copper_layers"),
        "pads": os_.get("pads"),
        "nets": os_.get("nets"),
        "pad_density_cm2": os_.get("pad_density_per_cm2"),
        "min_pitch_mm": os_.get("min_pad_pitch_mm"),
        "connections_to_route": start,
        "fr_reported_unrouted": r.get("fr_unrouted"),
        "kicad_unconnected": left,
        "completion_pct": completion,
        "new_drc_violations": sum(new_viol.values()) if rt else None,
        "new_drc_by_type": ";".join(f"{k}={v}" for k, v in sorted(new_viol.items())),
        "human_vias": os_.get("vias"),
        "auto_vias": rs.get("vias"),
        "human_length_mm": os_.get("track_length_mm"),
        "auto_length_mm": rs.get("track_length_mm"),
        "wall_s": r.get("wall_s"),
        "fr_state": r.get("fr_state"),
        "fr_passes": r.get("passes"),
        "fr_peak_heap_mb": r.get("fr_peak_heap_mb"),
        "error": r.get("error", ""),
    })

order = {b["id"]: i for i, b in enumerate(MANIFEST["boards"])}
cfg_order = {"fr25-default": 0, "fr25-fanout": 1, "fr21-default": 2}
rows.sort(key=lambda x: (order.get(x["board"], 99), cfg_order.get(x["config"], 9)))

with (RES / "results.csv").open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)


def f(v, nd=0):
    if v is None or v == "":
        return "—"
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


lines = ["| Board | Layers | Pads | To route | Router | Completion | Left unrouted (KiCad) | New DRC errors | Vias human → auto | Length human → auto (m) | Wall time |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
for x in rows:
    ratio_len = ""
    if x["human_length_mm"] and x["auto_length_mm"]:
        ratio_len = f"{x['human_length_mm']/1000:.2f} → {x['auto_length_mm']/1000:.2f}"
    vias = f"{f(x['human_vias'])} → {f(x['auto_vias'])}" if x["auto_vias"] is not None else "—"
    comp = f"{x['completion_pct']:.1f} %" if x["completion_pct"] is not None else (x["error"][:30] or "—")
    wall = f"{x['wall_s']/60:.1f} min" if x["wall_s"] else "—"
    lines.append(f"| {x['board_name']} | {f(x['layers'])} | {f(x['pads'])} | {f(x['connections_to_route'])} | "
                 f"{x['config']} | {comp} | {f(x['kicad_unconnected'])} | {f(x['new_drc_violations'])} | "
                 f"{vias} | {ratio_len or '—'} | {wall} |")
(RES / "REPORT_TABLES.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
