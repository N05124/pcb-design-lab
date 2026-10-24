#!/usr/bin/env python3
"""Import an autorouter's SES result onto the stripped board and measure it.

Usage (KiCad's Python):
    python3 evaluate.py <stripped.kicad_pcb> <board.dsn> <result.ses> <out_dir>

Writes into out_dir:
    routed.kicad_pcb   stripped board + autorouted copper, zones refilled
    routed_drc.rpt     KiCad DRC report
    routed.json        stats + DRC summary
"""
import json
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
# KiCad's distro builds turn some internal asserts (e.g. coordinate overflow
# warnings on boards with far-away graphics) into SIGTRAP; ignore them.
signal.signal(signal.SIGTRAP, signal.SIG_IGN)
import pcbnew  # noqa: E402
import pcbbench as pb  # noqa: E402


def main():
    stripped, dsn, ses, out = map(Path, sys.argv[1:5])
    out.mkdir(parents=True, exist_ok=True)

    # KiCad keeps net classes and design rules in the .kicad_pro (and custom
    # rules in .kicad_dru) next to the board. Make sure the stripped board is
    # graded against the same rules as the original.
    pb.attach_project_files(stripped)

    board = pcbnew.LoadBoard(str(stripped))
    pb.refill_zones(board)
    unconnected_before = pb.unconnected_count(board)
    imported = pb.import_ses(board, ses, dsn)
    pb.refill_zones(board)
    stats = pb.board_stats(board)
    unconnected_after = pb.unconnected_count(board)
    drc = pb.run_drc(board, out / "routed_drc.rpt")
    pcbnew.SaveBoard(str(out / "routed.kicad_pcb"), board)

    result = {"stats": stats, "drc": drc, "import": imported,
              "unconnected_before": unconnected_before,
              "unconnected_after": unconnected_after}
    (out / "routed.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({"stats": stats, "drc": {k: drc[k] for k in ("violations", "unconnected")},
                      "import": imported,
                      "unconnected": [unconnected_before, unconnected_after]}))


if __name__ == "__main__":
    main()
