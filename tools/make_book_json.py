#!/usr/bin/env python3
"""
make_book_json.py — turn the locked table of contents into manuscript/book.json.

The TOC file stays the single source of truth for structure: parts, chapters,
subtitles and key scriptures are parsed straight out of it so the manifest can
never drift from the outline.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOC = ROOT / "manuscript" / "01-table-of-contents.md"
OUT = ROOT / "manuscript" / "book.json"

PART_RE = re.compile(r"^##\s+PART\s+([IVXL]+)\s*\u2014\s*(.+?)\s*$")
CH_RE = re.compile(r"^-\s+\*\*Chapter\s+(\d+)\s*\u2014\s*(.+?)\*\*\s*$")
SUB_RE = re.compile(r"^\s+\*(.+?)\*\s*$")
SCR_RE = re.compile(r"^\s+Key Scriptures:\s*(.+?)\s*$")
FM_RE = re.compile(r"^\*\*([IVX]+)\s*\u2014\s*(.+?)\*\*\s*$")

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
         "VIII": 8, "IX": 9, "X": 10, "XI": 11}


def main() -> int:
    text = TOC.read_text(encoding="utf-8")
    parts, cur_part, cur_ch = [], None, None
    in_appendix = False

    for raw in text.splitlines():
        line = raw.rstrip()
        m = PART_RE.match(line)
        if m:
            cur_part = {"number": ROMAN[m.group(1)], "roman": m.group(1),
                        "title": m.group(2), "chapters": []}
            parts.append(cur_part)
            in_appendix = False
            continue
        if line.startswith("- **Appendix"):
            in_appendix = True
            continue
        m = CH_RE.match(line)
        if m and cur_part is not None:
            cur_ch = {"number": int(m.group(1)), "title": m.group(2),
                      "subtitle": "", "scriptures": "", "part": cur_part["number"]}
            cur_part["chapters"].append(cur_ch)
            continue
        if cur_ch is not None:
            m = SUB_RE.match(line)
            if m and not cur_ch["subtitle"]:
                cur_ch["subtitle"] = m.group(1)
                continue
            m = SCR_RE.match(line)
            if m:
                cur_ch["scriptures"] = m.group(1)
                cur_ch = None
                continue

    chapters = [c for p in parts for c in p["chapters"]]
    cfg = {
        "title": "Why God Left It to the Young",
        "subtitle": "The Mystics, the Fathers and the Hidden Architecture of Generational Revelation",
        "author": "Revd Prof Adeleke Daniel Durojaiye (PhD)",
        "author_short": "A. D. Durojaiye",
        "year": "2026",
        "place": "Ibadan, Nigeria",
        "publisher_line": "Ibadan \u00b7 Nigeria",
        "isbn": "978-\u200bXXX-\u200bXXXX-\u200bX (to be assigned)",
        "trim": '6" \u00d7 9"',
        "parts": parts,
        "chapters": chapters,
    }
    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"  parts: {len(parts)}   chapters: {len(chapters)}")
    for p in parts:
        print(f"  Part {p['number']:>2} ({p['roman']:>4}) {p['title'][:44]:<44} "
              f"{len(p['chapters'])} ch")
    print(f"  first: {chapters[0]['title']}")
    print(f"  last : {chapters[-1]['number']}. {chapters[-1]['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
