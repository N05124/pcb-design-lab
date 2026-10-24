#!/usr/bin/env python3
"""Measure a human-routed board, strip its routing, export Specctra DSN.

Usage (KiCad's Python):
    python3 prepare.py <board.kicad_pcb> <out_dir>

Writes into out_dir:
    original.json        stats + DRC summary of the human-routed board
    original_drc.rpt     KiCad DRC report of the original
    stripped.kicad_pcb   same board with every track/via deleted
    board.dsn            Specctra DSN of the stripped board (autorouter input)
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pcbnew  # noqa: E402
import pcbbench as pb  # noqa: E402


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)

    board = pcbnew.LoadBoard(str(src))
    pb.refill_zones(board)
    stats = pb.board_stats(board)
    original_unconnected = pb.unconnected_count(board)
    drc = pb.run_drc(board, out / "original_drc.rpt")

    removed = pb.strip_routing(board)
    pb.refill_zones(board)
    stripped_drc = pb.run_drc(board, out / "stripped_drc.rpt")
    pcbnew.SaveBoard(str(out / "stripped.kicad_pcb"), board)
    pb.attach_project_files(out / "stripped.kicad_pcb", src)

    t0 = time.time()
    ok = pcbnew.ExportSpecctraDSN(board, str(out / "board.dsn"))
    if not ok:
        raise SystemExit("DSN export failed")

    result = {
        "source": str(src),
        "stats": stats,
        "drc": drc,
        "removed_items": removed,
        "original_unconnected": original_unconnected,
        "unrouted_after_strip": stripped_drc["unconnected"],
        "dsn_export_s": round(time.time() - t0, 2),
    }
    (out / "original.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({"stats": stats, "drc": {k: drc[k] for k in ("violations", "unconnected")},
                      "unrouted_after_strip": stripped_drc["unconnected"]}))


if __name__ == "__main__":
    main()
