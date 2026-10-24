#!/usr/bin/env python3
"""Check a routed KiCad board against high-speed layout constraints.

KiCad's own DRC checks clearances and (from v8) some length rules, but it is
handy to have a scriptable, version-independent report for challenge grading
and CI. Run it with KiCad's Python (the interpreter that can `import pcbnew`):

    python3 check_constraints.py board.kicad_pcb constraints.yaml [--json out.json]

Constraint file (YAML):

    rules:
      - name: USB3 TX pair
        type: diff_pair            # length skew between two nets
        pos: /USB_SSTX_P
        neg: /USB_SSTX_N
        max_skew_mm: 0.13
        max_length_mm: 120         # optional
      - name: DDR byte lane 0
        type: match_group          # every net within tolerance of the group max
        nets: '^/DQ[0-7]$'         # regex, or a list of names
        tolerance_mm: 2.5
        reference: /DQS0_P         # optional: match against this net instead
      - name: Clock vias
        type: max_vias
        nets: '^/CLK'
        max: 2
      - name: 50 ohm RF trace width
        type: width
        nets: '^/RF_'
        min_mm: 0.30
        max_mm: 0.34
      - name: Keep DQ on inner layers
        type: layers
        nets: '^/DQ'
        allowed: [In1.Cu, In2.Cu, F.Cu]   # standard or user layer names
      - name: Everything routed
        type: routed                 # every net with >=2 pads has copper
        nets: '.*'

Lengths are the sum of track and arc lengths on each net. Via barrel length
and in-package (pin) delay are NOT included; add them yourself for DDR4/PCIe
sign-off.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict

import pcbnew
import yaml

NM = 1_000_000


def collect(board):
    length = defaultdict(float)
    vias = defaultdict(int)
    widths = defaultdict(set)
    layers = defaultdict(set)
    for t in board.GetTracks():
        net = t.GetNetname()
        if t.GetClass() == "PCB_VIA":
            vias[net] += 1
            continue
        length[net] += t.GetLength() / NM
        widths[net].add(round(t.GetWidth() / NM, 4))
        layers[net].add(t.GetLayer())
    pads = defaultdict(int)
    for p in board.GetPads():
        pads[p.GetNetname()] += 1
    return length, vias, widths, layers, pads


def select(names, spec):
    if isinstance(spec, list):
        return [n for n in spec if n in names]
    rx = re.compile(spec)
    return sorted(n for n in names if rx.search(n))


def layer_names(board, ids):
    out = set()
    for i in ids:
        out.add(board.GetLayerName(i))
        out.add(pcbnew.BOARD.GetStandardLayerName(i))
    return out


def check(board, rules):
    length, vias, widths, layers, pads = collect(board)
    names = set(pads) | set(length)
    names.discard("")
    results = []
    for r in rules:
        kind, name = r["type"], r.get("name", r["type"])
        res = {"name": name, "type": kind, "pass": True, "details": []}
        if kind == "diff_pair":
            lp, ln = length.get(r["pos"], 0.0), length.get(r["neg"], 0.0)
            skew = abs(lp - ln)
            res["details"].append(f"P={lp:.3f} mm N={ln:.3f} mm skew={skew:.3f} mm")
            if lp == 0 or ln == 0:
                res["pass"] = False
                res["details"].append("one side unrouted or net not found")
            if skew > r["max_skew_mm"]:
                res["pass"] = False
            if "max_length_mm" in r and max(lp, ln) > r["max_length_mm"]:
                res["pass"] = False
                res["details"].append(f"exceeds max length {r['max_length_mm']} mm")
        elif kind == "match_group":
            nets = select(names, r["nets"])
            if not nets:
                res["pass"] = False
                res["details"].append("no nets matched")
            else:
                ref = length.get(r["reference"], None) if r.get("reference") else max(length.get(n, 0) for n in nets)
                worst = max(nets, key=lambda n: abs(length.get(n, 0) - ref))
                dev = abs(length.get(worst, 0) - ref)
                res["details"].append(f"{len(nets)} nets, target {ref:.2f} mm, worst {worst} off by {dev:.2f} mm")
                res["pass"] = dev <= r["tolerance_mm"]
        elif kind == "max_vias":
            bad = [(n, vias[n]) for n in select(names, r["nets"]) if vias[n] > r["max"]]
            res["pass"] = not bad
            res["details"] += [f"{n}: {v} vias" for n, v in bad[:20]]
        elif kind == "width":
            bad = []
            for n in select(names, r["nets"]):
                for w in widths.get(n, ()):
                    if w < r.get("min_mm", 0) - 1e-6 or w > r.get("max_mm", 1e9) + 1e-6:
                        bad.append((n, w))
            res["pass"] = not bad
            res["details"] += [f"{n}: width {w} mm" for n, w in bad[:20]]
        elif kind == "layers":
            allowed = set(r["allowed"])
            bad = []
            for n in select(names, r["nets"]):
                for lid in layers.get(n, ()):
                    if not (layer_names(board, [lid]) & allowed):
                        bad.append((n, board.GetLayerName(lid)))
            res["pass"] = not bad
            res["details"] += [f"{n}: on {l}" for n, l in sorted(set(bad))[:20]]
        elif kind == "routed":
            bad = [n for n in select(names, r["nets"]) if pads.get(n, 0) >= 2 and length.get(n, 0) == 0]
            res["pass"] = not bad
            res["details"].append(f"{len(bad)} multi-pad nets with no copper (zone-only nets count as unrouted here)")
            res["details"] += bad[:20]
        else:
            res["pass"] = False
            res["details"].append(f"unknown rule type {kind}")
        results.append(res)
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("board")
    ap.add_argument("constraints")
    ap.add_argument("--json")
    a = ap.parse_args()
    board = pcbnew.LoadBoard(a.board)
    rules = yaml.safe_load(open(a.constraints))["rules"]
    results = check(board, rules)
    for r in results:
        mark = "PASS" if r["pass"] else "FAIL"
        print(f"[{mark}] {r['name']} ({r['type']})")
        for d in r["details"]:
            print(f"        {d}")
    passed = sum(r["pass"] for r in results)
    print(f"\n{passed}/{len(results)} rules passed")
    if a.json:
        json.dump(results, open(a.json, "w"), indent=2)
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
