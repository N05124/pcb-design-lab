#!/usr/bin/env python3
"""Render human vs. autorouted copper side by side as a PNG.

    python3 render_compare.py <work/board_id> <config> <out.png> [--layers F.Cu,B.Cu]

Needs kicad-cli, rsvg-convert (librsvg2-bin) and Pillow.
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def svg_png(board: Path, layers: str, png: Path, width: int):
    svg = png.with_suffix(".svg")
    subprocess.run(["kicad-cli", "pcb", "export", "svg", "--layers", layers, "--page-size-mode", "2",
                    "--exclude-drawing-sheet", "--drill-shape-opt", "1",
                    "-o", str(svg), str(board)], check=True, capture_output=True)
    subprocess.run(["rsvg-convert", "-w", str(width), "-b", "white", "-o", str(png), str(svg)],
                   check=True, capture_output=True)
    img = Image.open(png).convert("RGB")
    # trim white margins left by text/frame items outside the board
    bbox = ImageOps.invert(img).getbbox()
    return img.crop(bbox) if bbox else img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir")
    ap.add_argument("config")
    ap.add_argument("out")
    ap.add_argument("--layers", default="F.Cu,B.Cu,Edge.Cuts")
    ap.add_argument("--width", type=int, default=900)
    a = ap.parse_args()
    wd = Path(a.workdir)
    src = Path(json.loads((wd / "original.json").read_text())["source"])
    routed = wd / a.config / "routed.kicad_pcb"
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        left = svg_png(src, a.layers, td / "human.png", a.width)
        right = svg_png(routed, a.layers, td / "auto.png", a.width)
    h = max(left.height, right.height) + 40
    canvas = Image.new("RGB", (left.width + right.width + 20, h), "white")
    canvas.paste(left, (0, 40))
    canvas.paste(right, (left.width + 20, 40))
    d = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    d.text((10, 8), "Human-routed (original)", fill="black", font=font)
    d.text((left.width + 30, 8), f"Autorouted ({a.config})", fill="black", font=font)
    canvas.save(a.out, optimize=True)
    print(a.out, canvas.size)


if __name__ == "__main__":
    main()
