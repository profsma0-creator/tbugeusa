#!/usr/bin/env python3
"""
progress.py — manuscript progress against the book's acceptance criteria.

Acceptance criteria (as briefed):
    * every chapter  >= 5,000 words
    * body total     >= 500,000 words   (front matter and back matter excluded)

Because 68 chapters x 5,000 = 340,000, the *total* target implies an average of
about 7,350 words per chapter.  The working target column reports against that.

    python3 tools/progress.py            # summary + shortfall table
    python3 tools/progress.py --all      # one line per chapter
    python3 tools/progress.py --json     # machine-readable
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "manuscript" / "drafts"
CHAPTERS = ROOT / "manuscript" / "chapters"
BOOK = ROOT / "manuscript" / "book.json"

FENCE = re.compile(r"^<<<CHAPTER\s+(\d+)\s*$", re.M)
FLOOR = 5_000
TOTAL_TARGET = 500_000


def words(text: str) -> int:
    body = re.sub(r"^:::.*$", "", text, flags=re.M)
    body = re.sub(r"^#+.*$", "", body, flags=re.M)
    return len(re.findall(r"[A-Za-z\u2019'-]+", body))


def collect() -> dict[int, int]:
    """chapter number -> word count.  Prefers the split chapters, falls back to drafts."""
    out: dict[int, int] = {}
    if any(CHAPTERS.glob("ch*.md")):
        for path in sorted(CHAPTERS.glob("ch*.md")):
            m = re.match(r"ch(\d+)\.md$", path.name)
            if m:
                out[int(m.group(1))] = words(path.read_text(encoding="utf-8"))
        return out
    src = DRAFTS
    for path in sorted(src.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fences = list(FENCE.finditer(text))
        for i, m in enumerate(fences):
            end = fences[i + 1].start() if i + 1 < len(fences) else len(text)
            n = int(m.group(1))
            out[n] = out.get(n, 0) + words(text[m.end():end])
    return out


def titles() -> dict[int, str]:
    if not BOOK.exists():
        return {}
    book = json.loads(BOOK.read_text(encoding="utf-8"))
    t: dict[int, str] = {}
    for part in book.get("parts", []):
        for ch in part.get("chapters", []):
            t[int(ch["number"])] = ch["title"]
    return t


def main(argv: list[str]) -> int:
    counts = collect()
    if "--json" in argv:
        print(json.dumps(counts, indent=2, sort_keys=True))
        return 0

    ttl = titles()
    n_chapters = len(ttl) or 68
    per_target = -(-TOTAL_TARGET // n_chapters)  # ceil

    body = sum(v for k, v in counts.items() if k >= 1)
    front = counts.get(0, 0)

    print(f"chapters drafted : {len([k for k in counts if k >= 1])} / {n_chapters}")
    print(f"body words        : {body:,}   (target {TOTAL_TARGET:,})")
    print(f"front matter      : {front:,}   (excluded from the target)")
    print(f"chapter floor     : {FLOOR:,}   |  per-chapter target for the total: {per_target:,}")
    print(f"body still needed : {max(0, TOTAL_TARGET - body):,}")
    print(f"at {per_target:,}/chapter, remaining chapters owe "
          f"{max(0, (n_chapters - len([k for k in counts if k >= 1])) * per_target):,}")
    print()

    do_all = "--all" in argv
    rows = [(k, counts.get(k, 0)) for k in sorted(set(ttl) | set(counts)) if k >= 1]
    short = [(k, w) for k, w in rows if w < per_target]
    show = rows if do_all else short
    label = "all chapters" if do_all else f"below {per_target:,} words ({len(short)})"
    print(label)
    for k, w in show:
        flag = " " if w >= FLOOR else "!"
        print(f"  {flag} {k:>3}  {w:>7,}  {ttl.get(k, '')[:58]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
