#!/usr/bin/env python3
"""
preview.py — visual QA helpers.

    python3 tools/preview.py fig figures/out/fig-01-1.svg   # SVG -> PNG
    python3 tools/preview.py page book.pdf 12               # PDF page -> PNG
    python3 tools/preview.py pages book.pdf 12-16           # range, tiled
"""
from __future__ import annotations

import sys
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image


def svg_to_png(svg: str, out: str, scale: float = 3.0) -> str:
    """Vector-convert SVG to PDF, then rasterise — avoids the renderPM backend."""
    import tempfile
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    d = svg2rlg(svg)
    tmp = Path(tempfile.mkdtemp()) / "fig.pdf"
    renderPDF.drawToFile(d, str(tmp), autoSize=1)
    doc = pdfium.PdfDocument(str(tmp))
    doc[0].render(scale=scale).to_pil().save(out)
    return out


def page_to_png(pdf: str, page: int, out: str, dpi: int = 130) -> str:
    doc = pdfium.PdfDocument(pdf)
    pg = doc[page - 1]
    img = pg.render(scale=dpi / 72.0).to_pil()
    img.save(out)
    return out


def page_range_to_png(pdf: str, a: int, b: int, out: str, cols: int = 5,
                      dpi: int = 80) -> str:
    doc = pdfium.PdfDocument(pdf)
    imgs = []
    for p in range(a, min(b, len(doc)) + 1):
        imgs.append(doc[p - 1].render(scale=dpi / 72.0).to_pil())
    if not imgs:
        raise SystemExit("no pages")
    w, h = imgs[0].size
    rows = (len(imgs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + 8) + 8, rows * (h + 8) + 8), "#8a8a8a")
    for i, im in enumerate(imgs):
        r, c = divmod(i, cols)
        sheet.paste(im, (8 + c * (w + 8), 8 + r * (h + 8)))
    sheet.save(out)
    return out


def main(argv):
    if not argv:
        print(__doc__)
        return 0
    mode = argv[0]
    if mode == "fig":
        out = str(Path(argv[1]).with_suffix(".png"))
        print(svg_to_png(argv[1], out))
    elif mode == "page":
        out = f"/tmp/page-{argv[2]}.png"
        print(page_to_png(argv[1], int(argv[2]), out))
    elif mode == "pages":
        rng = argv[2]
        a, b = (rng.split("-") + [rng])[:2] if "-" in rng else (int(rng), int(rng))
        out = f"/tmp/pages-{rng}.png"
        print(page_range_to_png(argv[1], int(a), int(b), out,
                                dpi=int(argv[3]) if len(argv) > 3 else 80))
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
