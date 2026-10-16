"""
bookkit.figures — load diagrams and illustrations into the page.

Vector SVG is preferred (scaled by svglib into a reportlab Drawing so it stays
sharp at any size); raster PNG is supported for painted illustrations.
"""
from __future__ import annotations

import json
from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Flowable, Image, KeepTogether, Paragraph, Spacer

from . import theme as T

ROOT = Path(__file__).resolve().parent.parent.parent
FIG_DIR = ROOT / "figures"
MANIFEST = FIG_DIR / "figures.json"


def load_manifest() -> dict:
    if not MANIFEST.exists():
        return {}
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


class ScaledDrawing(Flowable):
    """Centres a vector drawing at a given fraction of the text measure."""

    def __init__(self, drawing: Drawing, width: float):
        super().__init__()
        self.d = drawing
        self.target_w = width

    def wrap(self, aw, ah):
        d = self.d
        scale = self.target_w / float(d.width)
        self.width = self.target_w
        self.height = float(d.height) * scale
        self._scale = scale
        return self.width, self.height

    def draw(self):
        c = self.canv
        d = self.d
        c.saveState()
        c.translate(0, 0)
        c.scale(self._scale, self._scale)
        d.drawOn(c, 0, 0)
        c.restoreState()


def load_figure(fig_id: str, manifest: dict, text_width: float):
    """Build the flowable list for one figure: art, caption, source."""
    meta = manifest.get(fig_id)
    if not meta:
        raise KeyError(f"Figure {fig_id!r} is not in figures/figures.json")
    path = FIG_DIR / meta["file"]
    if not path.exists():
        raise FileNotFoundError(f"Missing artwork for {fig_id}: {path}")

    width_frac = float(meta.get("width", 0.92))
    target_w = text_width * width_frac

    if path.suffix.lower() == ".svg":
        from svglib.svglib import svg2rlg
        d = svg2rlg(str(path))
        if d is None:
            raise RuntimeError(f"svglib could not read {path}")
        art = ScaledDrawing(d, target_w)
    else:
        img = ImageReader(str(path))
        iw, ih = img.getSize()
        art = Image(str(path), width=target_w, height=target_w * ih / iw)

    out = [Spacer(1, 9), art, Spacer(1, 5)]
    if meta.get("label"):
        out.append(Paragraph(meta["label"].upper(), T.STYLES["fig_number"]))
    if meta.get("caption"):
        out.append(Paragraph(meta["caption"], T.STYLES["fig_caption"]))
    if meta.get("source"):
        out.append(Paragraph(meta["source"], T.STYLES["fig_source"]))
    out.append(Spacer(1, 10))
    return out


def build_figure(fig_id: str, manifest: dict, text_width: float):
    """Figure kept together with its caption."""
    from .indexes import FigureMarker
    flows = load_figure(fig_id, manifest, text_width)
    return [FigureMarker(fig_id)] + [KeepTogether(flows)]


def is_captioned_illustration(meta: dict) -> bool:
    return bool(meta.get("plate"))
