#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Memory Puzzle Game
File: assets.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=====================================================================================================

Description:
Shape factory and drawing helpers. We generate a palette of distinct visual symbols
(circle, square, triangle, diamond, star, plus, cross, hexagon, etc.) that are drawn
on a Tkinter Canvas. No external image assets required.

Usage:
- Each shape type is represented by a callable: draw_shape(canvas, x, y, size)
- Identity of a tile is (shape_name, color_name).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Tuple


DrawFn = Callable[["Canvas", float, float, float, str], None]


@dataclass(frozen=True)
class Glyph:
    name: str
    draw: DrawFn


# --- Drawing primitives -----------------------------------------------------------------------------

def _draw_circle(canvas, cx, cy, s, fill):
    r = s * 0.34
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=fill, width=0)


def _draw_square(canvas, cx, cy, s, fill):
    r = s * 0.34
    canvas.create_rectangle(cx - r, cy - r, cx + r, cy + r, fill=fill, width=0)


def _draw_diamond(canvas, cx, cy, s, fill):
    r = s * 0.42
    pts = [cx, cy - r, cx + r, cy, cx, cy + r, cx - r, cy]
    canvas.create_polygon(pts, fill=fill, width=0)


def _draw_triangle(canvas, cx, cy, s, fill):
    r = s * 0.42
    pts = [cx, cy - r, cx + r, cy + r, cx - r, cy + r]
    canvas.create_polygon(pts, fill=fill, width=0)


def _draw_star(canvas, cx, cy, s, fill):
    r1 = s * 0.42
    r2 = r1 * 0.5
    pts = []
    for i in range(10):
        from math import cos, sin, pi

        ang = -pi / 2 + i * pi / 5
        r = r1 if i % 2 == 0 else r2
        pts.extend([cx + r * cos(ang), cy + r * sin(ang)])
    canvas.create_polygon(pts, fill=fill, width=0)


def _draw_plus(canvas, cx, cy, s, fill):
    w = s * 0.18
    r = s * 0.42
    canvas.create_rectangle(cx - w, cy - r, cx + w, cy + r, fill=fill, width=0)
    canvas.create_rectangle(cx - r, cy - w, cx + r, cy + w, fill=fill, width=0)


def _draw_cross(canvas, cx, cy, s, fill):
    w = s * 0.18
    r = s * 0.42
    # Diagonal rectangles for an X
    canvas.create_polygon(
        cx - r, cy - r + w, cx - r + w, cy - r, cx + r, cy + r - w, cx + r - w, cy + r, fill=fill, width=0
    )
    canvas.create_polygon(
        cx + r, cy - r + w, cx + r - w, cy - r, cx - r, cy + r - w, cx - r + w, cy + r, fill=fill, width=0
    )


def _draw_hexagon(canvas, cx, cy, s, fill):
    from math import cos, sin, pi

    r = s * 0.42
    pts = []
    for k in range(6):
        ang = pi / 6 + k * pi / 3
        pts.extend([cx + r * cos(ang), cy + r * sin(ang)])
    canvas.create_polygon(pts, fill=fill, width=0)


GLYPHS = [
    Glyph("circle", _draw_circle),
    Glyph("square", _draw_square),
    Glyph("diamond", _draw_diamond),
    Glyph("triangle", _draw_triangle),
    Glyph("star", _draw_star),
    Glyph("plus", _draw_plus),
    Glyph("cross", _draw_cross),
    Glyph("hexagon", _draw_hexagon),
]

# A small set of visually distinct colors (for glyphs only)
PALETTE = [
    "#f43f5e",  # rose-500
    "#f97316",  # orange-500
    "#eab308",  # yellow-500
    "#84cc16",  # lime-500
    "#10b981",  # emerald-500
    "#06b6d4",  # cyan-500
    "#3b82f6",  # blue-500
    "#8b5cf6",  # violet-500
    "#ec4899",  # pink-500
]


def available_identities():
    """Return a list of (glyph_name, color_hex) identities."""
    return [(g.name, c) for g in GLYPHS for c in PALETTE]


def draw_identity(canvas, cx, cy, size, identity):
    """Draw a given identity (shape_name, color) centered at (cx, cy)."""
    name, color = identity
    glyph = next(g for g in GLYPHS if g.name == name)
    glyph.draw(canvas, cx, cy, size, color)
