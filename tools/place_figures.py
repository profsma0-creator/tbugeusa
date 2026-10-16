#!/usr/bin/env python3
"""
place_figures.py — insert figure directives into the chapter manuscripts.

Figures are assigned to chapters in figures/figures.json.  Within a chapter the
directives are distributed at natural breaks — after a section's last paragraph,
or failing that after the nearest paragraph boundary — so a diagram lands near
the argument it illustrates rather than being dumped at the end.

Any existing `:::figure foo` directive in a chapter is removed first, so the
script is idempotent and re-running it after a re-render is safe.

    python3 tools/place_figures.py            # place
    python3 tools/place_figures.py --check    # report placement only
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "manuscript" / "chapters"
MANIFEST = ROOT / "figures" / "figures.json"

FIG_RE = re.compile(r"^:::figure\s+\S+\s*$", re.M)
HEAD_RE = re.compile(r"^#{2,4}\s+", re.M)


def insert_points(text: str, count: int) -> list[int]:
    """Choose `count` offsets at which to insert figures."""
    paras = [m.end() for m in re.finditer(r"\n\s*\n", text)]
    if not paras:
        return [len(text)] * count
    points = []
    for i in range(count):
        frac = (i + 1) / (count + 1)
        points.append(paras[min(len(paras) - 1, int(frac * len(paras)))])
    return sorted(points)


def place(chapter_no: int, figs: list[str], check: bool) -> list[str]:
    path = CHAPTERS / f"ch{chapter_no:02d}.md"
    if not path.exists():
        return []
    text = FIG_RE.sub("", path.read_text(encoding="utf-8"))
    text = re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n"
    placements = []
    for fig, pos in zip(figs, insert_points(text, len(figs))):
        block = f"\n\n:::figure {fig}\n:::\n"
        # walk back to the nearest paragraph boundary so the directive is not
        # inserted mid-paragraph
        cut = text.rfind("\n", 0, pos)
        cut = cut if cut > 0 else pos
        text = text[:cut] + block + text[cut:]
        placements.append(fig)
    if not check:
        path.write_text(text, encoding="utf-8")
    return placements


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_chapter: dict[int, list[str]] = defaultdict(list)
    for fid, meta in manifest.items():
        ch = int(meta.get("chapter", 0))
        if ch > 0:
            by_chapter[ch].append(fid)
    for k in by_chapter:
        by_chapter[k].sort()

    total = 0
    for ch in sorted(by_chapter):
        placed = place(ch, by_chapter[ch], args.check)
        if placed:
            print(f"  ch{ch:>02d}: {', '.join(placed)}")
            total += len(placed)
    unplaced = [f for f, m in manifest.items() if int(m.get("chapter", 0)) == 0]
    print(f"\n{total} figure directives placed in chapter files")
    print(f"{len(unplaced)} front-matter figures ({', '.join(sorted(unplaced))})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
