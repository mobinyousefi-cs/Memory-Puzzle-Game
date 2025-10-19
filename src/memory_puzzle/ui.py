#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Memory Puzzle Game
File: ui.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=====================================================================================================

Description:
Tkinter UI for the Memory Puzzle Game. Draws the board, handles input, HUD, and dialogs.
"""
from __future__ import annotations

import time
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Tuple

from .assets import draw_identity
from .game import Board, Tile
from .settings import (
    BG_COLOR,
    CANVAS_BG,
    FONT_HUD,
    HUD_HEIGHT,
    LEVELS,
    MISMATCH_HIDE_DELAY,
    PADDING,
    TILE_BG,
    TILE_GAP,
    TILE_HOVER,
    TILE_MATCHED,
    TILE_REVEALED,
    TILE_SIZE,
)


class MemoryApp(tk.Tk):
    def __init__(self, level_index: int = 0, seed: Optional[int] = None) -> None:
        super().__init__()
        self.title("Memory Puzzle — Tkinter")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        self.level_index = level_index
        self.board: Board = Board(LEVELS[self.level_index], seed=seed)
        self.start_time = time.time()

        # Compute canvas size
        self.canvas_width = PADDING * 2 + self.board.cols * TILE_SIZE + (self.board.cols - 1) * TILE_GAP
        self.canvas_height = HUD_HEIGHT + PADDING * 2 + self.board.rows * TILE_SIZE + (self.board.rows - 1) * TILE_GAP

        # Widgets
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg=CANVAS_BG, highlightthickness=0)
        self.canvas.pack()

        self._hover_tile: Optional[Tuple[int, int]] = None
        self._pending_hide: Optional[Tuple[Tile, Tile]] = None

        self._bind_keys()
        self._draw_static()
        self._redraw_all()
        self._tick()

    # --- Input -----------------------------------------------------------------------
    def _bind_keys(self) -> None:
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Motion>", self._on_motion)
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Key-n>", lambda e: self.new_game(self.level_index))
        self.bind("<Key-e>", lambda e: self.new_game(0))
        self.bind("<Key-m>", lambda e: self.new_game(1))
        self.bind("<Key-h>", lambda e: self.new_game(2))

    # --- Layout & drawing ------------------------------------------------------------
    def _tile_rect(self, r: int, c: int) -> Tuple[int, int, int, int]:
        x0 = PADDING + c * (TILE_SIZE + TILE_GAP)
        y0 = HUD_HEIGHT + PADDING + r * (TILE_SIZE + TILE_GAP)
        return x0, y0, x0 + TILE_SIZE, y0 + TILE_SIZE

    def _tile_center(self, r: int, c: int) -> Tuple[int, int]:
        x0, y0, x1, y1 = self._tile_rect(r, c)
        return (x0 + x1) // 2, (y0 + y1) // 2

    def _draw_static(self) -> None:
        # HUD background
        self.canvas.create_rectangle(0, 0, self.canvas_width, HUD_HEIGHT, fill=BG_COLOR, width=0)
        # HUD texts
        self.hud_level = self.canvas.create_text(10, HUD_HEIGHT // 2, anchor="w", fill="white", font=FONT_HUD, text="")
        self.hud_moves = self.canvas.create_text(self.canvas_width // 2, HUD_HEIGHT // 2, anchor="center", fill="white", font=FONT_HUD, text="")
        self.hud_time = self.canvas.create_text(self.canvas_width - 10, HUD_HEIGHT // 2, anchor="e", fill="white", font=FONT_HUD, text="")

    def _redraw_all(self) -> None:
        self.canvas.delete("tile")
        # Tiles
        for t in self.board.for_each():
            x0, y0, x1, y1 = self._tile_rect(t.row, t.col)
            # background
            fill = TILE_BG
            if t.matched:
                fill = TILE_MATCHED
            elif t.revealed:
                fill = TILE_REVEALED
            elif self._hover_tile == (t.row, t.col):
                fill = TILE_HOVER
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=0, tags=("tile", f"tile-{t.row}-{t.col}"))

            # glyph if revealed or matched
            if t.revealed or t.matched:
                cx, cy = self._tile_center(t.row, t.col)
                draw_identity(self.canvas, cx, cy, TILE_SIZE, t.identity)

        # HUD data
        level_name = f"Level: {self.board.level.name}  ({self.board.rows}×{self.board.cols})"
        self.canvas.itemconfigure(self.hud_level, text=level_name)
        self.canvas.itemconfigure(self.hud_moves, text=f"Moves: {self.board.moves}")
        elapsed = int(time.time() - self.start_time)
        self.canvas.itemconfigure(self.hud_time, text=f"Time: {elapsed}s")

    # --- Game flow -------------------------------------------------------------------
    def _on_motion(self, event) -> None:
        r, c = self._hit_test(event.x, event.y)
        prev = self._hover_tile
        self._hover_tile = (r, c) if r is not None else None
        if self._hover_tile != prev:
            self._redraw_all()

    def _on_click(self, event) -> None:
        if self._pending_hide is not None:
            return  # wait for unmatched hide
        hit = self._hit_test(event.x, event.y)
        if hit[0] is None:
            return
        r, c = hit
        first, second, matched = self.board.reveal(r, c)
        if second is None:
            self._redraw_all()
            return
        # second selected
        self._redraw_all()
        if matched:
            self._maybe_finish()
        else:
            self._pending_hide = (first, second)
            self.after(MISMATCH_HIDE_DELAY, self._hide_pending)

    def _hide_pending(self) -> None:
        if self._pending_hide is None:
            return
        a, b = self._pending_hide
        self._pending_hide = None
        self.board.hide_unmatched(a, b)
        self._redraw_all()

    def _hit_test(self, x: int, y: int) -> Tuple[Optional[int], Optional[int]]:
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                x0, y0, x1, y1 = self._tile_rect(r, c)
                if x0 <= x <= x1 and y0 <= y <= y1:
                    return r, c
        return None, None

    def _maybe_finish(self) -> None:
        if not self.board.all_revealed():
            return
        elapsed = int(time.time() - self.start_time)
        messagebox.showinfo(
            "Congratulations!",
            f"You completed {self.board.level.name} in {self.board.moves} moves and {elapsed} seconds.",
        )
        self.new_game(self.level_index)

    # --- Session management -----------------------------------------------------------
    def new_game(self, level_index: int) -> None:
        self.level_index = level_index
        self.board = Board(LEVELS[self.level_index])
        self.start_time = time.time()
        self._pending_hide = None
        self._hover_tile = None
        # Resize canvas if needed
        self.canvas_width = PADDING * 2 + self.board.cols * TILE_SIZE + (self.board.cols - 1) * TILE_GAP
        self.canvas_height = HUD_HEIGHT + PADDING * 2 + self.board.rows * TILE_SIZE + (self.board.rows - 1) * TILE_GAP
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)
        self.canvas.delete("all")
        self._draw_static()
        self._redraw_all()

    def _tick(self):
        # Update only the HUD time every 250ms
        elapsed = int(time.time() - self.start_time)
        self.canvas.itemconfigure(self.hud_time, text=f"Time: {elapsed}s")
        self.after(250, self._tick)
