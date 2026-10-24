#!/usr/bin/env python3
"""Autorouter benchmark orchestrator.

For every board in the manifest and every router config:
    prepare (strip + DSN)  ->  autoroute (DSN -> SES)  ->  evaluate (SES -> KiCad DRC)

Usage:
    python3 run_benchmark.py --manifest ../boards.json --out ../results \
        [--boards id1,id2] [--configs fr25-default,fr21-default] [--timeout-min 15] [--jobs 2]

Needs: KiCad 7.x with its Python module (KICAD_PY below), Java 21 and 25,
and the Freerouting jars (see ../README.md for setup).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import re
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KICAD_PY = os.environ.get("KICAD_PY", "/usr/bin/python3")
JAVA21 = os.environ.get("JAVA21", "/usr/lib/jvm/java-21-openjdk-amd64/bin/java")
JAVA25 = os.environ.get("JAVA25", "/usr/lib/jvm/java-25-openjdk-amd64/bin/java")
JARS = Path(os.environ.get("FREEROUTING_DIR", HERE.parent / "tools"))

CONFIGS = {
    # name: (java, jar, extra args)
    "fr25-default": (JAVA25, "freerouting-2.5.0.jar", []),
    "fr25-fanout": (JAVA25, "freerouting-2.5.0.jar", ["--router.fanout.enabled=true"]),
    "fr21-default": (JAVA21, "freerouting-2.1.0.jar", []),
}

NOISE = ("memory leak", "stdpbase", "JAVA_TOOL_OPTIONS")


def run(cmd, log_path: Path, timeout_s: float | None = None, env=None) -> tuple[int, float, str]:
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, env=env)
        rc, out = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as e:
        rc = -9
        out = (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        out += "\n[benchmark] killed by outer timeout\n"
    dt = time.time() - t0
    clean = "\n".join(l for l in out.splitlines() if not any(n in l for n in NOISE))
    log_path.write_text(clean)
    return rc, dt, clean


_PASS = re.compile(r"Auto-rout(?:ing|er) pass #(\d+).*?\((\d+) unrouted(?: and (\d+) violation)?")
_STAGE = re.compile(r"Auto-routing stage completed: started with (\d+) unrouted nets, completed in ([\d.]+) seconds.*?\((\d+) unrouted and (\d+) violation")
_HEAP = re.compile(r"([\d.]+) MB peak heap")
_STATE = re.compile(r"finished with state: (\w+)")


def parse_freerouting_log(text: str) -> dict:
    passes = [(int(a), int(b), int(c) if c else None) for a, b, c in _PASS.findall(text)]
    stage = _STAGE.search(text)
    state = _STATE.search(text)
    heaps = [float(h) for h in _HEAP.findall(text)]
    return {
        "passes": passes[-1][0] if passes else 0,
        "fr_start_unrouted": int(stage.group(1)) if stage else None,
        "fr_route_s": float(stage.group(2)) if stage else None,
        "fr_unrouted": int(stage.group(3)) if stage else (passes[-1][1] if passes else None),
        "fr_violations": int(stage.group(4)) if stage else (passes[-1][2] if passes else None),
        "fr_state": state.group(1) if state else "UNKNOWN",
        "fr_peak_heap_mb": max(heaps) if heaps else None,
    }


def run_kicad(cmd, log_path: Path) -> tuple[int, str, bool]:
    """Run a KiCad-Python step, retrying on KiCad 7's intermittent SIGTRAP
    (exit 133). The last attempt skips zone refills. Returns (rc, log, refilled)."""
    for attempt in range(3):
        env = dict(os.environ)
        no_refill = attempt == 2
        if no_refill:
            env["PCBBENCH_NO_REFILL"] = "1"
        rc, _, log = run(cmd, log_path, env=env)
        if rc == 0:
            return rc, log, not no_refill
    return rc, log, False


def prepare(board: dict, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    cache = out / "original.json"
    if cache.exists() and (out / "board.dsn").exists():
        return json.loads(cache.read_text())
    rc, log, refilled = run_kicad([KICAD_PY, str(HERE / "prepare.py"), board["path"], str(out)], out / "prepare.log")
    if rc != 0 or not cache.exists():
        raise RuntimeError(f"prepare failed for {board['id']} (exit {rc}):\n{log[-1500:]}")
    data = json.loads(cache.read_text())
    data["zones_refilled"] = refilled
    cache.write_text(json.dumps(data, indent=2))
    return data


def route_and_eval(board: dict, cfg: str, prep_dir: Path, timeout_min: int, reuse: bool = False) -> dict:
    java, jar, extra = CONFIGS[cfg]
    out = prep_dir / cfg
    out.mkdir(parents=True, exist_ok=True)
    ses = out / "result.ses"
    hh, mm = divmod(timeout_min, 60)
    cmd = [java, "-Xmx3g", "-jar", str(JARS / jar),
           "-de", str(prep_dir / "board.dsn"), "-do", str(ses),
           "-mp", "100",
           "--gui.enabled=false",
           f"--router.job_timeout={hh:02d}:{mm:02d}:00",
           "--usage_and_diagnostic_data.disable_analytics=true",
           "--profile.allow_telemetry=false",
           *extra]
    flog = out / "freerouting.log"
    if reuse and ses.exists() and flog.exists() and (out / "meta.json").exists():
        meta = json.loads((out / "meta.json").read_text())
        rc, wall, log = meta["fr_exit"], meta["wall_s"], flog.read_text()
    else:
        if ses.exists():
            ses.unlink()
        rc, wall, log = run(cmd, flog, timeout_s=timeout_min * 60 + 600)
        (out / "meta.json").write_text(json.dumps({"fr_exit": rc, "wall_s": round(wall, 1),
                                                   "timeout_min": timeout_min, "cmd": cmd}))
    rec = {"board": board["id"], "config": cfg, "fr_exit": rc, "wall_s": round(wall, 1)}
    rec.update(parse_freerouting_log(log))
    if not ses.exists():
        rec["error"] = "no SES produced"
        return rec
    rc, elog, refilled = run_kicad([KICAD_PY, str(HERE / "evaluate.py"), str(prep_dir / "stripped.kicad_pcb"),
                                    str(prep_dir / "board.dsn"), str(ses), str(out)], out / "evaluate.log")
    rec["eval_zones_refilled"] = refilled
    rj = out / "routed.json"
    if rc != 0 or not rj.exists():
        rec["error"] = "evaluate failed: " + elog[-500:]
        return rec
    routed = json.loads(rj.read_text())
    rec["routed"] = routed
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=str(HERE.parent / "boards.json"))
    ap.add_argument("--out", default=str(HERE.parent / "results"))
    ap.add_argument("--work", default=str(HERE.parent / "work"))
    ap.add_argument("--boards", default="")
    ap.add_argument("--configs", default="fr25-default")
    ap.add_argument("--timeout-min", type=int, default=15)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--reuse", action="store_true",
                    help="skip routing when a previous SES + log exist; only re-evaluate")
    args = ap.parse_args()

    manifest = json.loads(Path(args.manifest).read_text())
    boards = manifest["boards"]
    base = Path(args.manifest).resolve().parent
    for b in boards:
        if not Path(b["path"]).is_absolute():
            b["path"] = str(base / b["path"])
    if args.boards:
        keep = set(args.boards.split(","))
        boards = [b for b in boards if b["id"] in keep]
    configs = args.configs.split(",")
    work, out = Path(args.work), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    runs_path = out / "runs.jsonl"
    if args.reuse and runs_path.exists():
        runs_path.unlink()

    preps = {}
    for b in boards:
        print(f"[prepare] {b['id']}", flush=True)
        try:
            preps[b["id"]] = prepare(b, work / b["id"])
        except Exception as e:  # keep going with the other boards
            print(f"  ! {e}", flush=True)

    jobs = [(b, c) for b in boards if b["id"] in preps for c in configs]
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = {ex.submit(route_and_eval, b, c, work / b["id"], args.timeout_min, args.reuse): (b, c) for b, c in jobs}
        for f in cf.as_completed(futs):
            b, c = futs[f]
            try:
                rec = f.result()
            except Exception as e:
                rec = {"board": b["id"], "config": c, "error": repr(e)}
            rec["original"] = preps[b["id"]]
            with runs_path.open("a") as fh:
                fh.write(json.dumps(rec) + "\n")
            r = rec.get("routed", {})
            print(f"[done] {b['id']:<28} {c:<14} fr_unrouted={rec.get('fr_unrouted')} "
                  f"kicad_unconnected={r.get('drc', {}).get('unconnected')} wall={rec.get('wall_s')}s "
                  f"{rec.get('error', '')}", flush=True)


if __name__ == "__main__":
    main()
