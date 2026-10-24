# Autorouter benchmark: strip-and-reroute on real boards

**Question:** how close can a free, open-source autorouter get to what a human did on real boards — and where does it fail?

**Method:** take human-routed KiCad boards, delete every track and via, hand the bare placement to the autorouter, then put the result back into KiCad and grade it with **KiCad's own DRC** against the board's original rules. Comparing against the human's routing on the same placement keeps the test honest: placement is the same, only routing changes.

Results: **[RESULTS.md](RESULTS.md)** · raw data: [`results/results.csv`](results/results.csv), [`results/runs.jsonl`](results/runs.jsonl)

## Pipeline

```
original.kicad_pcb ──prepare.py──▶ stripped.kicad_pcb + board.dsn
                                          │
                              Freerouting (DSN ▶ SES)
                                          │
stripped.kicad_pcb + result.ses ──evaluate.py──▶ routed.kicad_pcb + KiCad DRC report
```

| Step | Script | What it does |
|---|---|---|
| Prepare | [`scripts/prepare.py`](scripts/prepare.py) | Refill zones, measure the original (layers, pads, nets, vias, track length, min pad pitch, DRC), delete all tracks/arcs/vias, export Specctra DSN |
| Route | Freerouting CLI | Headless, `-mp 100`, per-board job timeout |
| Evaluate | [`scripts/evaluate.py`](scripts/evaluate.py) | Import the SES (standalone importer in [`scripts/pcbbench.py`](scripts/pcbbench.py) — KiCad 7's built-in one needs the GUI), refill zones, run KiCad DRC with the original project's rules |
| Report | [`scripts/make_report.py`](scripts/make_report.py) | Aggregate into CSV and markdown tables |

### Metrics

| Metric | Meaning |
|---|---|
| **To route** | Unrouted connections (ratsnest edges) reported by KiCad's connectivity engine after stripping and refilling zones — so pads already joined by a pour don't count |
| **Left unrouted** | The same count after the autorouter's copper is imported and zones are refilled. This is the honest completion number — it is often higher than the router's own count (see [RESULTS](RESULTS.md)). We use the connectivity engine rather than the DRC report because KiCad 7's DRC report caps unconnected items at 499 |
| **Completion** | `(to_route − left) / to_route` |
| **New DRC errors** | DRC violations in the routed board minus those already in the original, by type, excluding unconnected items |
| **Vias / length** | Autorouter vs. the human's original routing on the same placement |

### Router configurations

| Config | Version | Notes |
|---|---|---|
| `fr25-default` | Freerouting 2.5.0 (Oct 2026) | Defaults; needs Java 25 |
| `fr25-fanout` | Freerouting 2.5.0 | `router.fanout.enabled=true` (fan out SMD pads before routing) |
| `fr21-default` | Freerouting 2.1.0 (Apr 2025) | Previous generation, for regression comparison; Java 21 |
| `fr25-noneckdown` | Freerouting 2.5.0 | `router.automatic_neckdown=false` — avoids sub-minimum trace widths near pins |

## Reproduce

Tested on Ubuntu 24.04, 2 vCPU, 7 GB RAM.

```bash
sudo apt-get install -y --no-install-recommends kicad kicad-demos openjdk-21-jre-headless openjdk-25-jre-headless
bash benchmark/scripts/fetch_tools.sh          # downloads Freerouting jars into benchmark/tools/
bash benchmark/scripts/fetch_boards.sh         # clones the GitHub boards listed in boards.json
cd benchmark
python3 scripts/run_benchmark.py --configs fr25-default,fr25-fanout,fr21-default --timeout-min 12 --jobs 2
python3 scripts/run_benchmark.py --reuse ...   # re-grade existing routes without re-routing
python3 scripts/make_report.py
python3 scripts/plot_results.py
python3 scripts/render_compare.py work/<board-id> fr25-default images/<board-id>.png
```

Environment variables `KICAD_PY`, `JAVA21`, `JAVA25`, `FREEROUTING_DIR` override the default paths.

## Limitations

- **KiCad 7.0.11 quirks handled by the scripts:** duplicate reference designators (logo footprints such as `REF**`) block DSN export, so they are renamed first; DRC leaves markers that crash later edits, so the board is reloaded before stripping; intermittent internal-assert traps are retried, with a no-zone-refill fallback. One board (ThunderScope) still crashes KiCad 7 and is excluded.
- **KiCad 7.0.11** is what Ubuntu 24.04 ships; boards saved by KiCad 8/9/10 can't be opened, which limits which open-source boards are usable. The scripts use only APIs that also exist in KiCad 8–9.
- Routing is graded on connectivity and clearance only. Impedance, length matching and return paths are **not** checked here — run [`tools/check_constraints.py`](../tools/check_constraints.py) on a routed board for that, and expect an autorouter to fail it.
- Placement is the human's. Real autorouting quality depends heavily on placement; this benchmark isolates the routing step.
- Wall-clock times are from a small 2-vCPU cloud VM with two jobs in parallel; expect a desktop to be 2–4× faster.
