"""
bookkit.bibleref — detect and canonicalise scripture references in prose.

Used to build the Scripture Index automatically from the manuscript, so the
index always matches the text.
"""
from __future__ import annotations

import re

CANON = [
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

ABBREV = {
    "Gen": "Genesis", "Ge": "Genesis", "Gn": "Genesis", "Exod": "Exodus",
    "Exo": "Exodus", "Ex": "Exodus", "Lev": "Leviticus", "Lv": "Leviticus",
    "Num": "Numbers", "Nu": "Numbers", "Deut": "Deuteronomy", "Deu": "Deuteronomy",
    "Dt": "Deuteronomy", "Josh": "Joshua", "Judg": "Judges", "Jdg": "Judges",
    "Ruth": "Ruth", "Ru": "Ruth", "1 Sam": "1 Samuel", "2 Sam": "2 Samuel",
    "1Sam": "1 Samuel", "2Sam": "2 Samuel", "1 Kgs": "1 Kings", "2 Kgs": "2 Kings",
    "1 Ki": "1 Kings", "2 Ki": "2 Kings", "1 Chr": "1 Chronicles",
    "2 Chr": "2 Chronicles", "Ezra": "Ezra", "Neh": "Nehemiah", "Ne": "Nehemiah",
    "Esth": "Esther", "Est": "Esther", "Job": "Job", "Ps": "Psalms",
    "Psa": "Psalms", "Psalm": "Psalms", "Psalms": "Psalms", "Prov": "Proverbs",
    "Pr": "Proverbs", "Eccl": "Ecclesiastes", "Ec": "Ecclesiastes",
    "Song": "Song of Solomon", "Isa": "Isaiah", "Is": "Isaiah",
    "Jer": "Jeremiah", "Lam": "Lamentations", "Ezek": "Ezekiel",
    "Eze": "Ezekiel", "Dan": "Daniel", "Da": "Daniel", "Hos": "Hosea",
    "Joel": "Joel", "Amos": "Amos", "Am": "Amos", "Obad": "Obadiah",
    "Jonah": "Jonah", "Jon": "Jonah", "Mic": "Micah", "Nah": "Nahum",
    "Hab": "Habakkuk", "Zeph": "Zephaniah", "Zep": "Zephaniah",
    "Hag": "Haggai", "Zech": "Zechariah", "Zec": "Zechariah", "Mal": "Malachi",
    "Matt": "Matthew", "Mat": "Matthew", "Mt": "Matthew", "Mark": "Mark",
    "Mk": "Mark", "Mrk": "Mark", "Luke": "Luke", "Lk": "Luke", "Lu": "Luke",
    "John": "John", "Jn": "John", "Jhn": "John", "Acts": "Acts", "Ac": "Acts",
    "Rom": "Romans", "Ro": "Romans", "Rm": "Romans", "1 Cor": "1 Corinthians",
    "2 Cor": "2 Corinthians", "1Co": "1 Corinthians", "2Co": "2 Corinthians",
    "Gal": "Galatians", "Ga": "Galatians", "Eph": "Ephesians", "Phil": "Philippians",
    "Php": "Philippians", "Col": "Colossians", "1 Thess": "1 Thessalonians",
    "2 Thess": "2 Thessalonians", "1 Thes": "1 Thessalonians",
    "2 Thes": "2 Thessalonians", "1 Tim": "1 Timothy", "2 Tim": "2 Timothy",
    "1Tim": "1 Timothy", "2Tim": "2 Timothy", "Tit": "Titus",
    "Phlm": "Philemon", "Phm": "Philemon", "Heb": "Hebrews",
    "Jas": "James", "Jam": "James", "1 Pet": "1 Peter", "2 Pet": "2 Peter",
    "1Pet": "1 Peter", "2Pet": "2 Peter", "1 John": "1 John", "2 John": "2 John",
    "3 John": "3 John", "1 Jn": "1 John", "2 Jn": "2 John", "3 Jn": "3 John",
    "Jude": "Jude", "Rev": "Revelation", "Re": "Revelation",
}

# longest-first alternation so "1 Corinthians" beats "1 Cor"
_TOKENS = sorted(set(list(ABBREV.keys()) + CANON), key=len, reverse=True)
BOOK_ALT = "|".join(re.escape(t) for t in _TOKENS)

_DASH = r"[\u2013\u2014\-]"
REF_RE = re.compile(
    r"(?<![\w])(?P<book>" + BOOK_ALT + r")\.?\s+"
    r"(?P<ch>\d{1,3})"
    r"(?:\s*[:.]\s*(?P<v1>\d{1,3})"
    r"(?:\s*" + _DASH + r"\s*(?P<v2>\d{1,3}))?"
    r"(?:\s*,\s*(?P<extra>\d{1,3}(?:\s*" + _DASH + r"\s*\d{1,3})?))?"
    r")?"
)


def canonical(book: str) -> str:
    b = book.strip().rstrip(".")
    if b in CANON:
        return b
    if b in ABBREV:
        return ABBREV[b]
    key = b.replace(" ", "")
    for k, v in ABBREV.items():
        if k.replace(" ", "") == key:
            return v
    return b


def display(book: str, ch: str, v1: str | None, v2: str | None) -> str:
    name = "Psalm" if book == "Psalms" else book
    if not v1:
        return f"{name} {ch}"
    if v2 and v2 != v1:
        return f"{name} {ch}:{v1}\u2013{v2}"
    return f"{name} {ch}:{v1}"


def find_refs(text: str) -> list[str]:
    """Return canonical, deduplicated, display-ready references found in text."""
    plain = re.sub(r"<[^>]+>", " ", text)
    out, seen = [], set()
    for m in REF_RE.finditer(plain):
        book = canonical(m.group("book"))
        d = display(book, m.group("ch"), m.group("v1"), m.group("v2"))
        key = (book, m.group("ch"), m.group("v1") or "", m.group("v2") or "")
        if key in seen:
            continue
        seen.add(key)
        out.append(d)
    return out


BOOK_ORDER = {b: i for i, b in enumerate(CANON)}

_SORT_CH = re.compile(r"^(?:(?P<book>.+?)\s+(?P<ch>\d+)(?::(?P<v>\d+))?)$")


def sort_key(ref: str):
    """Order index entries in biblical order, then chapter, then verse."""
    m = _SORT_CH.match(ref)
    if not m:
        return (999, 0, ref)
    book = m.group("book")
    if book == "Psalm":
        book = "Psalms"
    order = BOOK_ORDER.get(book, 998)
    return (order, int(m.group("ch")), int(m.group("v") or 0), ref)
