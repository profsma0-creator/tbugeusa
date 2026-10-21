"""A deliberately small markup parser for the textbook source files.

The source dialect is line based and intentionally restrictive so that the
typesetter, and not the author, controls presentation:

    # CHAPTER 1|Chapter Title              chapter opening (new page)
    ## 1.1|Section Title                   numbered first-level heading
    ## Chapter Summary                     unnumbered first-level heading
    ### Run-in or display subheading        second-level heading
    - bullet item
    1. numbered item
    > block quotation
    [FIG 1.1|caption|node one ; node two ; node three]
    :::panel Panel title
    ... paragraphs ...
    :::
    :::table 1.1|Caption text
    Head A | Head B
    Head C | Head D
    --
    cell | cell
    %%
    cell | cell
    :::
"""

import re

INLINE_ESCAPES = (("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"))


def inline(text):
    """Convert the small inline markup used in the source into RML-ish tags."""
    for a, b in INLINE_ESCAPES:
        text = text.replace(a, b)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?![\*\w])", r"<i>\1</i>", text)
    return text


def plain(text):
    """Strip markup for TOC / index / outline text."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


class Block:
    def __init__(self, kind, **kw):
        self.kind = kind
        self.__dict__.update(kw)

    def __repr__(self):
        return f"<Block {self.kind} {getattr(self, 'text', '')[:40]!r}>"


def parse(text):
    """Return a flat list of Block objects."""
    blocks = []
    lines = text.split("\n")
    i = 0
    para = []
    list_mode = None          # 'ul' | 'ol' | None
    table = None

    def flush_para():
        nonlocal para
        if para:
            blocks.append(Block("para", text=" ".join(para).strip()))
            para = []

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        # ---------------------------------------------------- fenced blocks
        if stripped.startswith(":::table") and table is None:
            flush_para()
            head = stripped[8:].strip()
            if "|" in head:
                num, cap = head.split("|", 1)
            else:
                num, cap = "", head
            table = {"num": num.strip(), "caption": cap.strip(),
                     "rows": [], "rules": []}
            i += 1
            continue
        if table is not None:
            if stripped == ":::":
                blocks.append(Block("table", **table))
                table = None
                i += 1
                continue
            if stripped in ("--", "%%"):
                table["rules"].append(len(table["rows"]))
                i += 1
                continue
            if stripped:
                cells = [c.strip() for c in stripped.split("|")]
                table["rows"].append(cells)
            i += 1
            continue

        if stripped.startswith(":::panel") or stripped.startswith(":::box"):
            flush_para()
            title = stripped.split(None, 1)[1].strip() if " " in stripped else ""
            body = []
            i += 1
            depth = 1
            while i < len(lines):
                s = lines[i].strip()
                if s.startswith(":::") and s not in (":::",):
                    depth += 1
                if s == ":::":
                    depth -= 1
                    if depth == 0:
                        break
                body.append(lines[i])
                i += 1
            i += 1
            blocks.append(Block("panel", title=title,
                                blocks=parse_body("\n".join(body))))
            continue

        if stripped == ":::":          # stray fence
            flush_para()
            i += 1
            continue

        # ------------------------------------------------------- headings
        if stripped.startswith("# "):
            flush_para()
            payload = stripped[2:]
            parts = [p.strip() for p in payload.split("|")]
            num = parts[0] if len(parts) > 1 else ""
            title = parts[1] if len(parts) > 1 else parts[0]
            toc = parts[2] if len(parts) > 2 else ""
            blocks.append(Block("chapter", num=num, title=title, toc=toc))
            i += 1
            continue
        if stripped.startswith("## "):
            flush_para()
            payload = stripped[3:]
            if "|" in payload:
                num, title = payload.split("|", 1)
            else:
                num, title = "", payload
            blocks.append(Block("h1", num=num.strip(), title=title.strip()))
            i += 1
            continue
        if stripped.startswith("### "):
            flush_para()
            blocks.append(Block("h2", title=stripped[4:].strip()))
            i += 1
            continue

        # --------------------------------------------------------- figures
        if stripped.lstrip("!").startswith("[FIG"):
            flush_para()
            stripped = stripped.lstrip("!")
            inner = stripped[1:stripped.rindex("]")] if "]" in stripped else stripped[1:]
            parts = [p.strip() for p in inner.split("|")]
            num = parts[0].replace("FIG", "").strip()
            caption = parts[1] if len(parts) > 1 else ""
            nodes = [n.strip() for n in parts[2].split(";")] if len(parts) > 2 else []
            note = parts[3] if len(parts) > 3 else ""
            blocks.append(Block("figure", num=num, caption=caption,
                                nodes=nodes, note=note))
            i += 1
            continue

        # ---------------------------------------------------------- lists
        m = re.match(r"^(\s*)[-•]\s+(.*)$", line)
        mnum = re.match(r"^(\s*)(\d+[.)])\s+(.*)$", line)
        if m:
            flush_para()
            blocks.append(Block("bullet", text=m.group(2).strip(),
                                indent=len(m.group(1))))
            i += 1
            continue
        if mnum:
            flush_para()
            blocks.append(Block("numbered", label=mnum.group(2),
                                text=mnum.group(3).strip()))
            i += 1
            continue

        # -------------------------------------------------- quotes / misc
        if stripped.startswith("> "):
            flush_para()
            blocks.append(Block("quote", text=stripped[2:].strip()))
            i += 1
            continue
        if stripped == "<<PAGEBREAK>>":
            flush_para()
            blocks.append(Block("pagebreak"))
            i += 1
            continue
        if stripped == "<<CLEARPAGE>>":
            flush_para()
            blocks.append(Block("clearpage"))
            i += 1
            continue

        if not stripped:
            flush_para()
            i += 1
            continue

        para.append(stripped)
        i += 1

    flush_para()
    return blocks


def parse_body(text):
    """Parse the inside of a panel, line by line."""
    out = []
    para = []

    def flush():
        nonlocal para
        if para:
            out.append(Block("para", text=" ".join(para).strip()))
            para = []

    for line in text.split("\n"):
        t = line.strip()
        if not t:
            flush()
            continue
        m = re.match(r"^[-•]\s+(.*)$", t)
        if m:
            flush()
            out.append(Block("bullet", text=m.group(1).strip(), indent=0))
            continue
        mn = re.match(r"^(\d+[.)])\s+(.*)$", t)
        if mn:
            flush()
            out.append(Block("numbered", label=mn.group(1), text=mn.group(2).strip()))
            continue
        if t.startswith("> "):
            flush()
            out.append(Block("quote", text=t[2:].strip()))
            continue
        para.append(t)
    flush()
    return out
