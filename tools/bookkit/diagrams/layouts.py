"""Additional layout primitives built on the diagram engine."""
from __future__ import annotations

from .engine import (GOLD, GOLD_L, GOLD_P, CREAM, CREAM_D, GRAY, INK, INK_SOFT,
                     PAPER, RULE, RULE_D, _pair, arrow, box, badge, band,
                     centre, fit, fit_lines, hrule, label, measure, panel,
                     vrule)


def stages(ax, items, band_b, fig=None, x_spine=0.055, tsize=6.4, bsize=5.3,
           box_h=None):
    """Numbered stages hanging off a vertical spine — the process diagram."""
    bb, bt = band_b
    n = len(items)
    step = (bt - bb) / n
    box_h = box_h or min(step * 0.82, 0.42)
    vrule(ax, x_spine, bb + step * 0.25, bt - step * 0.25, color=GOLD_L, lw=1.0)
    for i, it in enumerate(items):
        title, body = _pair(it)
        cy = bt - step * (i + 0.5)
        badge(ax, x_spine, cy, i + 1, r=0.019)
        bx = x_spine + 0.042
        bw = 0.985 - bx
        box(ax, bx, cy - box_h / 2, bw, box_h, title, body, fig=fig,
            tsize=tsize, bsize=bsize)


def spectrum(ax, left_pole, right_pole, marks, band_b, fig=None, x0=0.035,
             x1=0.965, tsize=6.0, bsize=5.2, note=None):
    """A continuum between two poles with labelled positions along it."""
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap
    bb, bt = band_b
    slot = (x1 - x0) / len(marks)
    _, th = measure(ax, fig, "Ag", tsize)
    _, bh = measure(ax, fig, "Ag", bsize)
    need = 0.055 + bh * 2 * 1.45 + 0.02 + th + 0.05
    top = bt - 0.02
    y = top - need + 0.045
    grad = np.linspace(0, 1, 256).reshape(1, -1)
    cmap = LinearSegmentedColormap.from_list("bookkit", [CREAM_D, GOLD_P, CREAM_D])
    ax.imshow(grad, extent=[x0, x1, y - 0.030, y + 0.030], aspect="auto",
              cmap=cmap, zorder=1)
    vrule(ax, x0, y - 0.030, y + 0.030, color=GOLD, lw=0.9)
    vrule(ax, x1, y - 0.030, y + 0.030, color=GOLD, lw=0.9)
    lsz = fit(left_pole, ax, fig, 0.44, tsize, weight="bold")
    ax.text(x0, y + 0.048, left_pole, ha="left", va="bottom", color=INK,
            fontsize=lsz, fontweight="bold")
    rsz = fit(right_pole, ax, fig, 0.44, tsize, weight="bold")
    ax.text(x1, y + 0.048, right_pole, ha="right", va="bottom", color=INK,
            fontsize=rsz, fontweight="bold")
    for i, mk in enumerate(marks):
        title, body = _pair(mk)
        x = x0 + slot * (i + 0.5)
        ax.add_patch(__import__("matplotlib.patches", fromlist=["Circle"]).Circle(
            (x, y), 0.011, facecolor=GOLD, edgecolor=PAPER, linewidth=0.7, zorder=5))
        vrule(ax, x, y - 0.030, y - 0.046, color=RULE_D, lw=0.6, ls=(0, (1, 1.4)))
        tsz = fit(title, ax, fig, slot * 0.94, bsize, weight="bold")
        ax.text(x, y - 0.052, title, ha="center", va="top", color=INK,
                fontsize=tsz, fontweight="bold", zorder=6)
        if body:
            bsz = fit(body, ax, fig, slot * 0.94, bsize - 0.4)
            ax.text(x, y - 0.052 - bh * 1.45, body, ha="center", va="top",
                    color=GRAY, fontsize=bsz, zorder=6, linespacing=1.4)


def quadrant(ax, x_label, y_label, cells, band_b, fig=None, x0=0.115, x1=0.965,
             tsize=6.0, bsize=5.2, lo=None):
    """A 2x2 field. `cells` is (top-left, top-right, bottom-left, bottom-right)."""
    bb, bt = band_b
    y1 = bt - 0.055
    y0 = bb + 0.055
    cw = (x1 - x0) / 2
    ch = (y1 - y0) / 2
    order = [(0, 1), (1, 1), (0, 0), (1, 0)]
    for (col, row), cell in zip(order, cells):
        title, body = _pair(cell)
        cx = x0 + col * cw
        cy = y0 + row * ch
        panel(ax, cx + 0.004, cy + 0.004, cw - 0.008, ch - 0.008,
              fc=CREAM if (col + row) % 2 else CREAM_D, ec=RULE, lw=0.7)
        tsz = fit(title, ax, fig, cw * 0.86, tsize, weight="bold")
        ax.text(cx + cw / 2, cy + ch * 0.70, title, ha="center", va="center",
                color=INK, fontsize=tsz, fontweight="bold", zorder=4)
        if body:
            lines = body.split("\n")
            bsz = fit_lines(lines, ax, fig, cw * 0.84, bsize)
            ax.text(cx + cw / 2, cy + ch * 0.34, body, ha="center", va="center",
                    color=GRAY, fontsize=bsz, zorder=4, linespacing=1.4)
    hrule(ax, x0, x1, (y0 + y1) / 2, color=GOLD_L, lw=0.8)
    vrule(ax, (x0 + x1) / 2, y0, y1, color=GOLD_L, lw=0.8)
    ax.text((x0 + x1) / 2, y1 + 0.030, x_label, ha="center", va="center",
            color=INK, fontsize=tsize, fontweight="bold")
    ax.text(x0 - 0.088, (y0 + y1) / 2, y_label, ha="center", va="center",
            color=INK, fontsize=tsize, fontweight="bold", rotation=90)
    if lo:
        ax.text(x0 - 0.006, y1 + 0.030, lo[0], ha="right", va="center",
                color=GOLD, fontsize=bsize - 0.6, fontweight="bold")
        ax.text(x0 - 0.006, y0 - 0.010, lo[1], ha="right", va="center",
                color=GOLD, fontsize=bsize - 0.6, fontweight="bold")


def funnel(ax, stages_list, band_b, fig=None, x0=0.10, x1=0.90, tsize=6.2,
           bsize=5.3):
    """Narrowing filter, first stage at the top."""
    from matplotlib.patches import Polygon
    bb, bt = band_b
    n = len(stages_list)
    th = (bt - bb) / n
    widths = [1.0 - 0.60 * i / max(1, n - 1) for i in range(n)]
    cx = (x0 + x1) / 2
    half = (x1 - x0) / 2
    for i, st in enumerate(stages_list):
        title, body = _pair(st)
        w_hi = widths[i]
        w_lo = widths[i + 1] if i + 1 < n else widths[-1] * 0.88
        yt = bt - th * i
        yb = yt - th
        pts = [(cx - half * w_hi, yt), (cx + half * w_hi, yt),
               (cx + half * w_lo, yb), (cx - half * w_lo, yb)]
        ax.add_patch(Polygon(pts, closed=True,
                             facecolor=CREAM if i % 2 == 0 else CREAM_D,
                             edgecolor=GOLD_L, linewidth=0.8, zorder=2))
        inner = half * min(w_hi, w_lo) * 1.9
        tsz = fit(title, ax, fig, inner, tsize, weight="bold")
        ax.text(cx, yb + th * 0.64, title, ha="center", va="center", color=INK,
                fontsize=tsz, fontweight="bold", zorder=4)
        if body:
            bsz = fit(body, ax, fig, inner, bsize)
            ax.text(cx, yb + th * 0.28, body, ha="center", va="center",
                    color=GRAY, fontsize=bsz, zorder=4)


def bridge(ax, left, right, spans, band_b, fig=None, h=None, tsize=6.1,
           bsize=5.3, label_size=5.5):
    """Two banks joined by a multi-lane bridge — transmission across a gap."""
    bb, bt = band_b
    h = h or (bt - bb) * 0.88
    y0 = band_centre = bb + (bt - bb - h) / 2.0
    lw_ = rw_ = 0.215
    panel(ax, 0.02, y0, lw_, h, fc=CREAM_D, ec=GOLD_L, lw=0.9)
    panel(ax, 0.98 - rw_, y0, rw_, h, fc=CREAM_D, ec=GOLD_L, lw=0.9)
    for (x, w, title) in ((0.02, lw_, left), (0.98 - rw_, rw_, right)):
        tsz = fit_lines(title.split("\n"), ax, fig, w * 0.86, tsize)
        ax.text(x + w / 2, y0 + h / 2, title, ha="center", va="center",
                color=INK, fontsize=tsz, fontweight="bold", zorder=4,
                linespacing=1.4)
    n = len(spans)
    lane = h / n
    for i, sp in enumerate(spans):
        title, body = _pair(sp)
        cy = y0 + h - lane * (i + 0.5)
        arrow(ax, 0.02 + lw_ + 0.005, cy, 0.98 - rw_ - 0.005, cy,
              color=GOLD_L, lw=0.9, ms=6)
        ax.text(0.5, cy + 0.028, title, ha="center", va="bottom", color=INK,
                fontsize=label_size, fontweight="bold", zorder=6)
        if body:
            ax.text(0.5, cy - 0.028, body, ha="center", va="top", color=GRAY,
                    fontsize=label_size - 0.3, zorder=6, linespacing=1.35)


def arch(ax, keystone, pillars, band_b, fig=None, tsize=6.2, bsize=5.3):
    """A keystone held by pillars — a truth sustained by several supports."""
    from matplotlib.patches import Wedge
    bb, bt = band_b
    n = len(pillars)
    ph = 0.36
    y0 = bb
    pw = (0.90 - 0.025 * (n - 1)) / n
    for i, p in enumerate(pillars):
        title, body = _pair(p)
        x = 0.05 + i * (pw + 0.025)
        box(ax, x, y0, pw, ph, title, body, fig=fig, tsize=tsize, bsize=bsize)
    ax.add_patch(Wedge((0.5, y0 + ph - 0.01), 0.40, 18, 162, width=0.075,
                       facecolor=CREAM_D, edgecolor=GOLD_L, linewidth=0.9,
                       zorder=3))
    ax.text(0.5, y0 + ph + 0.145, keystone, ha="center", va="center", color=INK,
            fontsize=tsize + 0.5, fontweight="bold", zorder=5)


def before_after(ax, before, after, band_b, fig=None, h=None, tsize=6.1,
                 bsize=5.2, arrow_text=None):
    """A single decisive transition, with the pivot named on the arrow."""
    bb, bt = band_b
    h = h or (bt - bb) * 0.90
    y = centre(band_b, h)
    w = 0.375
    box(ax, 0.015, y, w, h, before[0], before[1], fig=fig, tsize=tsize,
        bsize=bsize, fc=CREAM_D, ec=RULE_D)
    box(ax, 0.985 - w, y, w, h, after[0], after[1], fig=fig, tsize=tsize,
        bsize=bsize, fc=CREAM, ec=GOLD_L)
    x0, x1 = 0.015 + w + 0.02, 0.985 - w - 0.02
    arrow(ax, x0, y + h / 2, x1, y + h / 2, lw=1.4, ms=8)
    if arrow_text:
        lines = arrow_text.split("\n")
        bsz = min(5.0, fit_lines(lines, ax, fig, (x1 - x0) * 1.9, 5.0))
        ax.text((x0 + x1) / 2, y + h / 2 + 0.030, arrow_text, ha="center",
                va="bottom", color=GOLD, fontsize=bsz, fontweight="bold",
                zorder=6, linespacing=1.35)
