#!/usr/bin/env python3
"""Look up KJV verses.  usage: python3 tools/kjv.py "II Kings 22:13" "1 John 4:4" """
import gzip, json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
_D = json.load(gzip.open(ROOT / "assets/scripture/kjv.json.gz", "rt"))

def _norm(name):
    n = name.strip()
    n = re.sub(r"^(I{1,3})\s+", lambda m: str(len(m.group(1))) + " ", n, flags=re.I)
    return n.lower()

BOOKS = {_norm(k): k for k in _D}

def verses(ref):
    m = re.match(r"^\s*(.+?)\s+(\d+):([\d,\-\s]+)$", ref)
    if not m:
        raise SystemExit(f"bad ref: {ref}")
    book, ch, spec = _norm(m.group(1)), int(m.group(2)), m.group(3)
    key = BOOKS.get(book)
    if not key:
        raise SystemExit(f"unknown book {book!r}; have {sorted(BOOKS)[:5]} …")
    chap = _D[key].get(str(ch))
    if chap is None:
        raise SystemExit(f"no chapter {ch} in {key}")
    out = []
    for part in spec.split(","):
        part = part.strip()
        rng = range(*(int(x) for x in part.split("-"))) if "-" in part else [int(part)]
        if "-" in part:
            a, b = (int(x) for x in part.split("-"))
            rng = range(a, b + 1)
        for n in rng:
            t = chap.get(str(n))
            if t:
                out.append((n, " ".join(t.split())))
    return key, ch, out

if __name__ == "__main__":
    for ref in sys.argv[1:]:
        key, ch, vs = verses(ref)
        for n, t in vs:
            print(f"{key} {ch}:{n} — {t}\n")
