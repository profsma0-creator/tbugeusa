#!/usr/bin/env python3
"""
split_chapters.py — split drafted part files into per-chapter manuscripts.

Drafts are written per part as a single file with chapter fences:

    <<<CHAPTER 1
    ## First section heading
    body...
    <<<CHAPTER 2
    ...

This script writes manuscript/chapters/chNN.md for each fence, so the build
pipeline sees one file per chapter.

    python3 tools/split_chapters.py            # all draft files
    python3 tools/split_chapters.py --check    # report only
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "manuscript" / "drafts"
OUT = ROOT / "manuscript" / "chapters"
FENCE = re.compile(r"^<<<CHAPTER\s+(\d+)\s*$", re.M)


def words(text: str) -> int:
    body = re.sub(r"^:::.*$", "", text, flags=re.M)
    body = re.sub(r"^#+.*$", "", body, flags=re.M)
    return len(re.findall(r"[A-Za-z\u2019'-]+", body))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--drafts", default=str(DRAFTS))
    args = ap.parse_args()

    draft_dir = Path(args.drafts)
    files = sorted(draft_dir.glob("*.md")) if draft_dir.exists() else []
    if not files:
        print(f"no draft files in {draft_dir}")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    written = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        marks = list(FENCE.finditer(text))
        if not marks:
            print(f"  {f.name}: no chapter fences")
            continue
        for i, m in enumerate(marks):
            n = int(m.group(1))
            start = m.end()
            end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
            body = text[start:end].strip() + "\n"
            w = words(body)
            total += w
            written.append((n, f.name, w))
            if not args.check:
                (OUT / f"ch{n:02d}.md").write_text(body, encoding="utf-8")

    print(f"{'chapter':>8}  {'words':>7}  source")
    for n, name, w in written:
        flag = "  <-- short" if w < 5000 else ""
        print(f"{n:>8}  {w:>7,}  {name}{flag}")
    print(f"\n{len(written)} chapters, {total:,} words")
    short = [n for n, _, w in written if w < 5000]
    if short:
        print(f"below 5,000 words ({len(short)}): {short}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
