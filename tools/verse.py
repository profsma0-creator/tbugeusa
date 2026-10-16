#!/usr/bin/env python3
"""
verse.py — King James Version lookup for manuscript work.

The full KJV (public domain, 1769 text) lives gzipped at
assets/scripture/kjv.json.gz and is loaded on demand.

Usage
-----
    python3 tools/verse.py "Psalm 78:1-7"
    python3 tools/verse.py "Gen 12:1-3" "1 Cor 1:26-29"
    python3 tools/verse.py --inline "Ps 78:1-7"      # one-line, quote-ready
    python3 tools/verse.py --markdown "Acts 2:17-18" # markdown block quote
    python3 tools/verse.py --check                     # integrity report
"""
from __future__ import annotations

import gzip
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "assets" / "scripture" / "kjv.json.gz"

# --- book name handling ------------------------------------------------------
BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges",
    "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles",
    "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah",
    "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians",
    "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians",
    "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus",
    "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John",
    "3 John", "Jude", "Revelation",
]

ALIASES = {
    "gen": "Genesis", "ge": "Genesis", "gn": "Genesis",
    "ex": "Exodus", "exod": "Exodus", "exo": "Exodus",
    "lev": "Leviticus", "lv": "Leviticus",
    "num": "Numbers", "nu": "Numbers", "nm": "Numbers",
    "deut": "Deuteronomy", "deu": "Deuteronomy", "dt": "Deuteronomy",
    "josh": "Joshua", "jos": "Joshua",
    "judg": "Judges", "jdg": "Judges", "jg": "Judges",
    "rut": "Ruth", "rth": "Ruth",
    "1sam": "1 Samuel", "1sa": "1 Samuel", "1sa": "1 Samuel", "1sm": "1 Samuel",
    "2sam": "2 Samuel", "2sa": "2 Samuel", "2sm": "2 Samuel",
    "1kgs": "1 Kings", "1ki": "1 Kings", "1kg": "1 Kings", "1k": "1 Kings",
    "2kgs": "2 Kings", "2ki": "2 Kings", "2kg": "2 Kings", "2k": "2 Kings",
    "1chr": "1 Chronicles", "1ch": "1 Chronicles",
    "2chr": "2 Chronicles", "2ch": "2 Chronicles",
    "ezr": "Ezra", "neh": "Nehemiah", "est": "Esther", "est": "Esther",
    "job": "Job", "ps": "Psalms", "psa": "Psalms", "psalm": "Psalms",
    "psalms": "Psalms", "psm": "Psalms",
    "prov": "Proverbs", "pro": "Proverbs", "prv": "Proverbs",
    "eccl": "Ecclesiastes", "ecc": "Ecclesiastes", "ec": "Ecclesiastes",
    "song": "Song of Solomon", "sos": "Song of Solomon", "ss": "Song of Solomon",
    "isa": "Isaiah", "is": "Isaiah",
    "jer": "Jeremiah", "je": "Jeremiah",
    "lam": "Lamentations", "la": "Lamentations",
    "ezek": "Ezekiel", "eze": "Ezekiel", "ezk": "Ezekiel",
    "dan": "Daniel", "dn": "Daniel", "da": "Daniel",
    "hos": "Hosea", "ho": "Hosea",
    "joe": "Joel", "jl": "Joel",
    "amo": "Amos", "am": "Amos",
    "oba": "Obadiah", "ob": "Obadiah",
    "jon": "Jonah", "jnh": "Jonah",
    "mic": "Micah", "mi": "Micah",
    "nah": "Nahum", "na": "Nahum",
    "hab": "Habakkuk", "hb": "Habakkuk",
    "zeph": "Zephaniah", "zep": "Zephaniah", "zp": "Zephaniah",
    "hag": "Haggai", "hg": "Haggai",
    "zech": "Zechariah", "zec": "Zechariah", "zc": "Zechariah",
    "mal": "Malachi", "ml": "Malachi",
    "matt": "Matthew", "mat": "Matthew", "mt": "Matthew",
    "mark": "Mark", "mk": "Mark", "mrk": "Mark",
    "luke": "Luke", "lk": "Luke", "luk": "Luke",
    "john": "John", "jhn": "John", "jn": "John",
    "acts": "Acts", "act": "Acts", "ac": "Acts",
    "rom": "Romans", "ro": "Romans", "rm": "Romans",
    "1cor": "1 Corinthians", "1co": "1 Corinthians",
    "2cor": "2 Corinthians", "2co": "2 Corinthians",
    "gal": "Galatians", "ga": "Galatians",
    "eph": "Ephesians", "ep": "Ephesians",
    "phil": "Philippians", "php": "Philippians", "philip": "Philippians",
    "col": "Colossians",
    "1thess": "1 Thessalonians", "1th": "1 Thessalonians", "1thes": "1 Thessalonians",
    "2thess": "2 Thessalonians", "2th": "2 Thessalonians", "2thes": "2 Thessalonians",
    "1tim": "1 Timothy", "1ti": "1 Timothy", "1tm": "1 Timothy",
    "2tim": "2 Timothy", "2ti": "2 Timothy", "2tm": "2 Timothy",
    "tit": "Titus", "ti": "Titus",
    "phlm": "Philemon", "phm": "Philemon",
    "heb": "Hebrews", "he": "Hebrews",
    "jas": "James", "jam": "James", "jm": "James",
    "1pet": "1 Peter", "1pe": "1 Peter", "1pt": "1 Peter",
    "2pet": "2 Peter", "2pe": "2 Peter", "2pt": "2 Peter",
    "1john": "1 John", "1jn": "1 John", "1jo": "1 John",
    "2john": "2 John", "2jn": "2 John", "2jo": "2 John",
    "3john": "3 John", "3jn": "3 John", "3jo": "3 John",
    "jude": "Jude", "jud": "Jude",
    "rev": "Revelation", "re": "Revelation", "apocalypse": "Revelation",
}

_store: dict | None = None


def load() -> dict:
    global _store
    if _store is None:
        if not STORE.exists():
            raise SystemExit(
                f"Scripture store not found at {STORE}.\n"
                "Run tools/bootstrap.sh, or rebuild it from the KJV source."
            )
        with gzip.open(STORE, "rt", encoding="utf-8") as fh:
            _store = json.load(fh)
    return _store


def resolve_book(raw: str) -> str:
    """Map an abbreviated book name to its canonical form."""
    s = raw.strip().rstrip(".")
    s = re.sub(r"\s+", "", s).lower()
    exact = {b.lower().replace(" ", ""): b for b in BOOKS}
    if s in exact:
        return exact[s]
    if s in ALIASES:
        return ALIASES[s]
    # ordinal spelled out, e.g. "firstsamuel"
    s2 = (s.replace("first", "1").replace("second", "2")
            .replace("third", "3").replace("i", "1", 1) if s.startswith("i") else s)
    if s2 in exact:
        return exact[s2]
    for b in BOOKS:
        if b.lower().replace(" ", "").startswith(s) and len(s) >= 3:
            return b
    raise SystemExit(f"Unrecognised book: {raw!r}")


REF_RE = re.compile(
    r"^\s*(?P<book>(?:[1-3]\s*)?[A-Za-z][A-Za-z ]*?)\.?\s*"
    r"(?P<ch>\d+)(?::(?P<v1>\d+)(?:\s*[-–—]\s*(?P<v2>\d+))?)?\s*$"
)


def parse_ref(ref: str) -> tuple[str, int, int | None, int | None]:
    m = REF_RE.match(ref)
    if not m:
        raise SystemExit(f"Could not parse reference: {ref!r}")
    book = resolve_book(m.group("book"))
    ch = int(m.group("ch"))
    v1 = int(m.group("v1")) if m.group("v1") else None
    v2 = int(m.group("v2")) if m.group("v2") else v1
    return book, ch, v1, v2


def verses(ref: str) -> list[tuple[int, str]]:
    book, ch, v1, v2 = parse_ref(ref)
    store = load()
    if book not in store:
        raise SystemExit(f"Book not in store: {book}")
    if str(ch) not in store[book]:
        raise SystemExit(f"{book} has no chapter {ch}")
    chap = store[book][str(ch)]
    if v1 is None:
        return [(int(k), chap[k]) for k in sorted(chap, key=int)]
    hi = max(v1, v2 or v1)
    out = []
    for n in range(v1, hi + 1):
        if str(n) in chap:
            out.append((n, chap[str(n)]))
    if not out:
        raise SystemExit(f"No verses found for {ref!r}")
    return out


def _display_ref(ref: str) -> str:
    book, ch, v1, v2 = parse_ref(ref)
    if book == "Psalms":
        book = "Psalm"
    if v1 is None:
        return f"{book} {ch}"
    if v2 and v2 != v1:
        return f"{book} {ch}:{v1}\u2013{v2}"
    return f"{book} {ch}:{v1}"


def show(ref: str, mode: str = "plain") -> str:
    rows = verses(ref)
    label = _display_ref(ref)
    if mode == "inline":
        return " ".join(t for _, t in rows)
    if mode == "markdown":
        body = " ".join(f"<sup>{n}</sup> {t}" for n, t in rows) if len(rows) > 1 \
               else " ".join(t for _, t in rows)
        return f":::verse\n{body}\n\u2014 {label}\n:::"
    if mode == "json":
        return json.dumps({"ref": label, "verses": [{"v": n, "text": t} for n, t in rows]},
                          ensure_ascii=False, indent=2)
    lines = [f"--- {label} (KJV) " + "-" * max(0, 46 - len(label))]
    for n, t in rows:
        lines.append(f"  {n:>3}  {t}")
    return "\n".join(lines)


def integrity_report() -> str:
    store = load()
    nv = sum(len(c) for b in store.values() for c in b.values())
    out = [f"books: {len(store)}", f"verses: {nv:,}"]
    for probe in ["Genesis 1:1", "Psalm 78:7", "Isaiah 59:21", "Malachi 4:6",
                  "Acts 2:17", "2 Timothy 2:2", "Revelation 22:21"]:
        try:
            rows = verses(probe)
            ok = rows and all(t.strip() for _, t in rows)
            out.append(f"  {'OK ' if ok else 'BAD'} {_display_ref(probe)}: {rows[0][1][:58]}...")
        except SystemExit as exc:
            out.append(f"  BAD {probe}: {exc}")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 0
    mode = "plain"
    args = []
    for a in argv:
        if a.startswith("--"):
            key = a[2:]
            if key == "check":
                print(integrity_report())
                return 0
            if key in ("inline", "markdown", "json", "plain"):
                mode = key
            else:
                print(f"unknown option {a}")
                return 2
        else:
            args.append(a)
    for ref in args:
        print(show(ref, mode))
        if len(args) > 1:
            print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
