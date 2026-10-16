#!/usr/bin/env python3
"""
diagrams.py — render every figure in the catalogue to vector SVG.

    python3 tools/diagrams.py              # render all
    python3 tools/diagrams.py --list       # show the catalogue
    python3 tools/diagrams.py --only fig-01-1 fig-01-2
    python3 tools/diagrams.py --chapter 5  # only chapter 5's figures
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from bookkit.diagrams import catalogue, engine, layouts  # noqa: E402

OUT = ROOT / "figures" / "out"
MANIFEST = ROOT / "figures" / "figures.json"
FONT_DIR = ROOT / "assets" / "fonts"


LAYOUT_FN = {
    "chain": engine.chain,
    "vchain": engine.vchain,
    "twocol": engine.two_col,
    "timeline": engine.timeline,
    "tree": engine.tree,
    "cycle": engine.cycle,
    "pyramid": engine.pyramid,
    "layers": engine.layers,
    "matrix": engine.matrix,
    "balance": engine.balance,
    "radial": engine.radial,
    "stages": layouts.stages,
    "spectrum": layouts.spectrum,
    "quadrant": layouts.quadrant,
    "funnel": layouts.funnel,
    "bridge": layouts.bridge,
    "arch": layouts.arch,
    "before_after": layouts.before_after,
}


def render(fig_id: str, spec: dict) -> tuple[Path, dict]:
    layout = spec["layout"]
    h = spec.get("height") or catalogue.HEIGHT.get(layout, 2.4)
    fig, ax = engine.canvas(h=h)
    has_title = bool(spec.get("title"))
    has_note = bool(spec.get("footnote"))
    band_b = engine.band(has_title, has_note)
    if has_title:
        engine.heading(ax, spec["title"])
    LAYOUT_FN[layout](ax, fig=fig, band_b=band_b, **dict(spec["data"]))
    if has_note:
        engine.footnote(ax, spec["footnote"])
    path = engine.save(fig, ax, fig_id, OUT)
    parts = fig_id.split("-")
    entry = {
        "label": spec.get("label") or f"Figure {int(parts[1])}.{int(parts[2])}",
        "file": f"out/{path.name}",
        "width": spec.get("width", 1.0),
        "caption": spec.get("caption", ""),
        "source": spec.get("source", ""),
        "chapter": spec.get("chapter", 0),
    }
    return path, entry


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--chapter", type=int)
    args = ap.parse_args()

    cat = catalogue.CATALOGUE

    if args.list:
        for fid, spec in cat.items():
            print(f"{fid:12s} ch{spec.get('chapter', 0):>3}  {spec['layout']:14s} "
                  f"{spec.get('title','')[:52]}")
        print(f"\n{len(cat)} figures defined")
        return 0

    engine.setup_fonts(FONT_DIR)

    manifest = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    todo = list(cat.keys())
    if args.only:
        todo = [f for f in todo if f in set(args.only)]
    if args.chapter is not None:
        todo = [f for f in todo if cat[f].get("chapter") == args.chapter]

    ok = failures = 0
    for fid in todo:
        try:
            path, entry = render(fid, cat[fid])
            manifest[fid] = entry
            ok += 1
            print(f"  {fid:12s} -> {path.name:22s} {path.stat().st_size/1024:6.1f} kB")
        except Exception as exc:  # keep rendering the rest
            failures += 1
            print(f"  {fid:12s} !! {type(exc).__name__}: {exc}")

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"\n{ok} rendered, {failures} failed; manifest holds {len(manifest)} figures")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
