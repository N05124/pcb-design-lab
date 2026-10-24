"""
pcbbench — helpers for the autorouter benchmark.

Runs under KiCad's bundled Python (the interpreter that can `import pcbnew`).
Tested with KiCad 7.0.11 on Ubuntu 24.04.

Pipeline per board:
  1. load the human-routed original and measure it
  2. delete every track, arc and via (zones, footprints, outline untouched)
  3. export a Specctra DSN
  4. (caller) run an autorouter that reads DSN and writes SES
  5. import the SES back onto the stripped board, refill zones, measure again
"""
from __future__ import annotations

import math
import re
from pathlib import Path

import pcbnew

NM_PER_MM = 1_000_000


# --------------------------------------------------------------------------
# Minimal S-expression reader (enough for Specctra DSN / SES)
# --------------------------------------------------------------------------
_TOKEN = re.compile(r'\s*(?:(\()|(\))|"((?:[^"\\]|\\.)*)"|([^\s()"]+))')


def parse_sexpr(text: str):
    """Parse an s-expression into nested Python lists of strings."""
    # Specctra allows a (string_quote ") directive whose bare quote would
    # otherwise confuse the tokenizer; neutralise it first.
    text = text.replace('(string_quote ")', "(string_quote dq)")
    stack: list[list] = [[]]
    pos = 0
    n = len(text)
    while pos < n:
        m = _TOKEN.match(text, pos)
        if not m:
            pos += 1
            continue
        pos = m.end()
        if m.group(1):
            stack.append([])
        elif m.group(2):
            done = stack.pop()
            stack[-1].append(done)
        elif m.group(3) is not None:
            stack[-1].append(m.group(3))
        elif m.group(4) is not None:
            stack[-1].append(m.group(4))
    return stack[0][0] if stack[0] else []


def find_all(node, key):
    """Yield every sub-list whose head is `key` (depth-first)."""
    if isinstance(node, list):
        if node and node[0] == key:
            yield node
        for child in node:
            if isinstance(child, list):
                yield from find_all(child, key)


def find_first(node, key):
    return next(find_all(node, key), None)


# --------------------------------------------------------------------------
# Board measurement
# --------------------------------------------------------------------------
def copper_stack(board):
    return list(board.GetEnabledLayers().CuStack())


def board_stats(board) -> dict:
    tracks = vias = arcs = 0
    length_nm = 0.0
    blind_vias = micro_vias = 0
    for item in board.GetTracks():
        cls = item.GetClass()
        if cls == "PCB_VIA":
            vias += 1
            vt = item.GetViaType()
            if vt == pcbnew.VIATYPE_BLIND_BURIED:
                blind_vias += 1
            elif vt == pcbnew.VIATYPE_MICROVIA:
                micro_vias += 1
        elif cls == "PCB_ARC":
            arcs += 1
            length_nm += item.GetLength()
        else:
            tracks += 1
            length_nm += item.GetLength()

    bbox = board.GetBoardEdgesBoundingBox()
    w_mm = bbox.GetWidth() / NM_PER_MM
    h_mm = bbox.GetHeight() / NM_PER_MM
    pads = board.GetPads()
    smd = sum(1 for p in pads if p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD)
    min_pitch = _min_pad_pitch_mm(board)

    return {
        "copper_layers": board.GetCopperLayerCount(),
        "footprints": len(board.GetFootprints()),
        "pads": len(pads),
        "smd_pads": smd,
        "nets": board.GetNetCount(),
        "zones": len(list(board.Zones())),
        "board_w_mm": round(w_mm, 2),
        "board_h_mm": round(h_mm, 2),
        "pad_density_per_cm2": round(len(pads) / max(w_mm * h_mm / 100, 1e-9), 2),
        "min_pad_pitch_mm": min_pitch,
        "track_segments": tracks,
        "track_arcs": arcs,
        "vias": vias,
        "blind_buried_vias": blind_vias,
        "micro_vias": micro_vias,
        "track_length_mm": round(length_nm / NM_PER_MM, 1),
    }


def _min_pad_pitch_mm(board):
    """Smallest centre-to-centre distance between pads of the same footprint."""
    best = math.inf
    for fp in board.GetFootprints():
        pts = [(p.GetPosition().x, p.GetPosition().y) for p in fp.Pads()
               if p.GetNetCode() > 0]
        if len(pts) < 2 or len(pts) > 2000:
            continue
        pts.sort()
        for i, (x1, y1) in enumerate(pts):
            for x2, y2 in pts[i + 1:i + 12]:
                d = math.hypot(x2 - x1, y2 - y1)
                if 0 < d < best:
                    best = d
    return None if best is math.inf else round(best / NM_PER_MM, 3)


def attach_project_files(board_path: Path, source: Path | None = None) -> None:
    """Copy the original board's .kicad_pro/.kicad_dru next to `board_path`.

    `source` defaults to the "source" recorded in original.json beside it.
    """
    import json
    import shutil
    board_path = Path(board_path)
    if source is None:
        meta = board_path.parent / "original.json"
        if not meta.exists():
            return
        source = Path(json.loads(meta.read_text())["source"])
    for ext in (".kicad_pro", ".kicad_dru"):
        src = source.with_suffix(ext)
        if src.exists():
            shutil.copyfile(src, board_path.with_suffix(ext))


def strip_routing(board) -> int:
    """Delete every track, arc and via. Returns the number of items removed."""
    items = list(board.GetTracks())
    for item in items:
        board.Delete(item)
    return len(items)


def refill_zones(board) -> bool:
    zones = board.Zones()
    if len(list(zones)) == 0:
        return True
    return pcbnew.ZONE_FILLER(board).Fill(board.Zones())


def unconnected_count(board) -> int:
    """Unrouted connections (ratsnest edges) after a zone refill.

    KiCad's DRC report caps unconnected items (at 499 in 7.0), so large boards
    need the connectivity engine's own count instead.
    """
    board.BuildConnectivity()
    return int(board.GetConnectivity().GetUnconnectedCount(False))


_DRC_TYPE = re.compile(r"^\[([a-z_]+)\]")
_DRC_FOUND = re.compile(r"\*\* Found (\d+) (DRC violations|unconnected pads|Footprint errors)")


def run_drc(board, report_path: Path) -> dict:
    pcbnew.WriteDRCReport(board, str(report_path), pcbnew.EDA_UNITS_MILLIMETRES, False)
    text = report_path.read_text(errors="replace")
    out = {"violations": None, "unconnected": None, "footprint_errors": None,
           "by_type": {}}
    for m in _DRC_FOUND.finditer(text):
        n = int(m.group(1))
        key = {"DRC violations": "violations", "unconnected pads": "unconnected",
               "Footprint errors": "footprint_errors"}[m.group(2)]
        out[key] = n
    section = None
    for line in text.splitlines():
        if line.startswith("** Found") and "DRC violations" in line:
            section = "drc"
        elif line.startswith("** Found") and "unconnected" in line:
            section = "unconnected"
        elif line.startswith("** Found"):
            section = None
        m = _DRC_TYPE.match(line)
        if m and section == "drc":
            out["by_type"][m.group(1)] = out["by_type"].get(m.group(1), 0) + 1
    return out


# --------------------------------------------------------------------------
# Specctra session (SES) import
# --------------------------------------------------------------------------
_VIA_NAME = re.compile(r"Via\[(\d+)-(\d+)\]_(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)_um")


def _dsn_layer_names(dsn_tree) -> list[str]:
    structure = find_first(dsn_tree, "structure")
    names = []
    for layer in structure:
        if isinstance(layer, list) and layer and layer[0] == "layer":
            names.append(layer[1])
    return names


def import_ses(board, ses_path: Path, dsn_path: Path) -> dict:
    """Add the wires and vias from an SES file onto `board`.

    KiCad 7's own ImportSpecctraSES() needs the GUI editor frame, so this is a
    standalone re-implementation of the parts the benchmark needs: straight
    wire paths and through/blind vias.
    """
    dsn = parse_sexpr(dsn_path.read_text(errors="replace"))
    ses = parse_sexpr(ses_path.read_text(errors="replace"))

    dsn_layers = _dsn_layer_names(dsn)
    cu = copper_stack(board)
    if len(dsn_layers) != len(cu):
        raise RuntimeError(f"layer count mismatch DSN={len(dsn_layers)} board={len(cu)}")
    name_to_layer = {n: cu[i] for i, n in enumerate(dsn_layers)}

    routes = find_first(ses, "routes")
    if routes is None:
        raise RuntimeError("SES has no (routes ...) section")
    res = find_first(routes, "resolution")
    unit, per = res[1].lower(), float(res[2])
    unit_nm = {"um": 1000.0, "mm": 1e6, "mil": 25400.0, "inch": 25.4e6}[unit]
    scale = unit_nm / per  # nm per SES coordinate unit

    def xy(x, y):
        return pcbnew.VECTOR2I(int(round(float(x) * scale)),
                               int(round(-float(y) * scale)))

    # padstacks from library_out: name -> (diam_nm, drill_nm, first_idx, last_idx)
    padstacks = {}
    lib = find_first(routes, "library_out")
    for ps in (find_all(lib, "padstack") if lib else []):
        name = ps[1]
        m = _VIA_NAME.match(name)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            padstacks[name] = (float(m.group(3)) * 1000, float(m.group(4)) * 1000, a, b)
        else:
            circle = find_first(ps, "circle")
            idx = [dsn_layers.index(s[1][1]) for s in ps if isinstance(s, list)
                   and s and s[0] == "shape" and isinstance(s[1], list)
                   and s[1][1] in dsn_layers]
            d = float(circle[2]) * scale if circle else 600_000
            padstacks[name] = (d, d / 2, min(idx or [0]), max(idx or [len(cu) - 1]))

    # Fallback via geometry from the DSN's default via
    added_tracks = added_vias = missing_nets = 0
    net_out = find_first(routes, "network_out")
    for net in (net_out[1:] if net_out else []):
        if not (isinstance(net, list) and net and net[0] == "net"):
            continue
        netinfo = board.FindNet(net[1])
        if netinfo is None:
            missing_nets += 1
            continue
        for child in net[2:]:
            if not isinstance(child, list) or not child:
                continue
            if child[0] == "wire":
                path = find_first(child, "path")
                if path is None:
                    continue
                layer = name_to_layer.get(path[1])
                width = float(path[2]) * scale
                coords = path[3:]
                coords = [c for c in coords if not isinstance(c, list)]
                pts = [xy(coords[i], coords[i + 1]) for i in range(0, len(coords) - 1, 2)]
                for p0, p1 in zip(pts, pts[1:]):
                    if p0.x == p1.x and p0.y == p1.y:
                        continue
                    t = pcbnew.PCB_TRACK(board)
                    t.SetStart(p0)
                    t.SetEnd(p1)
                    t.SetWidth(int(width))
                    t.SetLayer(layer)
                    t.SetNet(netinfo)
                    board.Add(t)
                    added_tracks += 1
            elif child[0] == "via":
                ps_name, x, y = child[1], child[2], child[3]
                diam, drill, a, b = padstacks.get(ps_name, (600_000, 300_000, 0, len(cu) - 1))
                v = pcbnew.PCB_VIA(board)
                v.SetPosition(xy(x, y))
                v.SetWidth(int(diam))
                v.SetDrill(int(drill))
                if a == 0 and b == len(cu) - 1:
                    v.SetViaType(pcbnew.VIATYPE_THROUGH)
                    v.SetLayerPair(cu[0], cu[-1])
                else:
                    v.SetViaType(pcbnew.VIATYPE_BLIND_BURIED)
                    v.SetLayerPair(cu[a], cu[b])
                v.SetNet(netinfo)
                board.Add(v)
                added_vias += 1
    return {"added_tracks": added_tracks, "added_vias": added_vias,
            "missing_nets": missing_nets}
