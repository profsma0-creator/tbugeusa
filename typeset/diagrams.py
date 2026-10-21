"""Vector figures for the textbook, drawn with ReportLab primitives.

Every chapter opens with one conceptual map (Figure n.1). The maps are drawn
from the same specification so that the visual language of the book stays
consistent: numbered nodes on a two-column ladder joined by elbow connectors,
ending in the integrative outcome of the chapter.
"""

import math

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Flowable

from style import ACCENT, INK, PANEL, RULE_LIGHT, TEXT_W


def wrap(text, font, size, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if stringWidth(trial, font, size) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class ConceptualMap(Flowable):
    """A numbered ladder of conceptual steps.

    ``nodes`` is a list of short phrases (two to six words each); the final
    node is drawn as the integrative outcome of the sequence.
    """

    BOX_W = TEXT_W * 0.455
    BOX_H = 42.0
    GAP_Y = 24.0
    ROW_H = BOX_H + GAP_Y
    PAD = 2.0

    def __init__(self, nodes, width=TEXT_W):
        Flowable.__init__(self)
        self.nodes = nodes
        self.width = width
        self._compute_height()

    def _compute_height(self):
        rows = math.ceil(len(self.nodes) / 2.0)
        self.height = rows * self.ROW_H - self.GAP_Y + 2 * self.PAD + 6

    # ------------------------------------------------------------------ draw
    def draw(self):
        c = self.canv
        c.saveState()
        n = len(self.nodes)
        box_w, box_h = self.BOX_W, self.BOX_H
        left_x = 0.0
        right_x = self.width - box_w
        y_top = self.height - self.PAD

        pos = []
        for idx, label in enumerate(self.nodes):
            row, col = divmod(idx, 2)
            if idx == n - 1 and n % 2 == 1:
                # a single closing node is centred across the measure
                x = (self.width - box_w) / 2.0
            else:
                x = left_x if col == 0 else right_x
            y = y_top - box_h - row * self.ROW_H
            pos.append((x, y))
            self._node(c, x, y, box_w, box_h, idx + 1, label,
                       idx == n - 1)

        for i in range(n - 1):
            self._elbow(c, pos[i], pos[i + 1], box_w, box_h)
        c.restoreState()

    # --------------------------------------------------------------- helpers
    def _node(self, c, x, y, w, h, number, label, final):
        edge = ACCENT if final else colors.HexColor("#4A4A4A")
        c.setLineWidth(0.6)
        c.setStrokeColor(edge)
        c.setFillColor(colors.white)
        c.rect(x, y, w, h, stroke=1, fill=1)

        # roundel with the step number, set inside the box
        cx, cy, r = x + 14.0, y + h / 2.0, 7.6
        c.setFillColor(ACCENT if final else colors.white)
        c.setStrokeColor(edge)
        c.circle(cx, cy, r, stroke=1, fill=1)
        c.setFillColor(colors.white if final else ACCENT)
        c.setFont("Body-Semi", 7.2)
        c.drawCentredString(cx, cy - 2.5, str(number))

        # label
        font = "Body-Med" if final else "Body"
        c.setFillColor(INK)
        c.setFont(font, 8.3)
        lines = wrap(label, font, 8.3, w - 34)
        step = 9.6
        first = cy + (len(lines) - 1) * step / 2.0 - 3.1
        for ln in lines:
            c.drawString(x + 27, first, ln)
            first -= step

    def _elbow(self, c, src, dst, w, h):
        """Connector between consecutive nodes: horizontal within a row,
        an elbow between rows."""
        colour = colors.HexColor("#5A5A5A")
        c.setStrokeColor(colour)
        c.setFillColor(colour)
        c.setLineWidth(0.6)
        sx, sy = src
        dx, dy = dst
        if abs(sy - dy) < 0.5:                      # same row: straight across
            y = sy + h / 2.0
            x0, x1 = sx + w, dx
            c.line(x0, y, x1 - 4.6, y)
            self._arrow(c, x1, y, "right")
        else:                                       # next row: down, across, down
            mid = sy - self.GAP_Y / 2.0
            x0, x1 = sx + w / 2.0, dx + w / 2.0
            top = dy + h
            p = c.beginPath()
            p.moveTo(x0, sy)
            p.lineTo(x0, mid)
            p.lineTo(x1, mid)
            p.lineTo(x1, top + 4.6)
            c.drawPath(p)
            self._arrow(c, x1, top, "down")

    def _arrow(self, c, x, y, direction):
        s = 4.6
        p = c.beginPath()
        if direction == "right":
            p.moveTo(x, y)
            p.lineTo(x - s, y + s * 0.58)
            p.lineTo(x - s, y - s * 0.58)
        else:
            p.moveTo(x, y)
            p.lineTo(x - s * 0.58, y + s)
            p.lineTo(x + s * 0.58, y + s)
        p.close()
        c.drawPath(p, stroke=0, fill=1)


class CurveFigure(Flowable):
    """Small companion figure: predictive values as a function of prevalence.

    Used in Chapter 3 to show that a test's positive predictive value depends
    on base rate. The curves are computed from Bayes' theorem with fixed
    sensitivity and specificity, stated in the caption.
    """

    def __init__(self, sens, spec, width=TEXT_W * 0.86, height=150):
        Flowable.__init__(self)
        self.sens, self.spec = sens, spec
        self.width, self.height = width, height

    def draw(self):
        c = self.canv
        c.saveState()
        pad_l, pad_b, pad_r, pad_t = 34, 26, 12, 12
        w = self.width - pad_l - pad_r
        h = self.height - pad_b - pad_t
        ox, oy = pad_l, pad_b

        # axes
        c.setStrokeColor(colors.HexColor("#4A4A4A"))
        c.setLineWidth(0.55)
        c.line(ox, oy, ox, oy + h)
        c.line(ox, oy, ox + w, oy)

        # gridlines
        c.setStrokeColor(RULE_LIGHT)
        c.setLineWidth(0.35)
        c.setDash(1.2, 2.4)
        for frac in (0.25, 0.5, 0.75, 1.0):
            y = oy + h * frac
            c.line(ox, y, ox + w, y)
            c.setFont("Body", 6.6)
            c.setFillColor(colors.HexColor("#4A4A4A"))
            c.drawRightString(ox - 3, y - 2.2, f"{int(frac*100)}")
        for frac in (0, 0.25, 0.5, 0.75, 1.0):
            x = ox + w * frac
            c.line(x, oy, x, oy + h)
            c.drawCentredString(x, oy - 9, f"{int(frac*100)}")
        c.setDash()

        # PPV and NPV curves
        for label, fn, colour, dash in (
            ("PPV", lambda p: (self.sens * p) / (self.sens * p + (1 - self.spec) * (1 - p)), ACCENT, None),
            ("NPV", lambda p: (self.spec * (1 - p)) / (self.spec * (1 - p) + (1 - self.sens) * p), colors.HexColor("#8A5A44"), (3, 2)),
        ):
            c.setStrokeColor(colour)
            c.setLineWidth(0.9)
            if dash:
                c.setDash(*dash)
            p = c.beginPath()
            first = True
            for i in range(0, 101):
                prev = i / 100.0
                val = fn(prev)
                x = ox + w * prev
                y = oy + h * val
                if first:
                    p.moveTo(x, y)
                    first = False
                else:
                    p.lineTo(x, y)
            c.drawPath(p)
            c.setDash()

        # axis labels
        c.setFillColor(INK)
        c.setFont("Body", 7.4)
        c.drawCentredString(ox + w / 2.0, oy - 19, "Prevalence of the condition in the setting (%)")
        c.saveState()
        c.translate(12, oy + h / 2.0)
        c.rotate(90)
        c.drawCentredString(0, 0, "Posterior probability (%)")
        c.restoreState()

        # legend
        c.setFont("Body", 7.2)
        lx, ly = ox + w - 62, oy + h - 12
        c.setStrokeColor(ACCENT)
        c.setLineWidth(0.9)
        c.line(lx, ly + 2.4, lx + 14, ly + 2.4)
        c.setFillColor(INK)
        c.drawString(lx + 17, ly, "Positive predictive value")
        c.setStrokeColor(colors.HexColor("#8A5A44"))
        c.setDash(3, 2)
        c.line(lx, ly - 8.2, lx + 14, ly - 8.2)
        c.setDash()
        c.setFillColor(INK)
        c.drawString(lx + 17, ly - 10.6, "Negative predictive value")
        c.restoreState()
