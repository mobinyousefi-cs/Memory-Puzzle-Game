#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Memory Puzzle Game
File: game.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=====================================================================================================

Description:
Pure game logic (no Tkinter). Board generation, reveal/match mechanics, move counting.

This isolation allows unit tests to validate core behavior without a GUI.
"""
from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import List, Optional, Sequence, Tuple

from . import __version__
from .assets import available_identities
from .settings import LevelConfig, DEFAULT_SEED

Identity = Tuple[str, str]  # (shape_name, color_hex)


@dataclass
class Tile:
    row: int
    col: int
    identity: Identity
    revealed: bool = False
    matched: bool = False


class Board:
    def __init__(self, level: LevelConfig, seed: Optional[int] = DEFAULT_SEED):
        self.level = level
        self.rows, self.cols = level.rows, level.cols
        self.rng = Random(seed)
        self.grid: List[List[Tile]] = []
        self.moves = 0
        self.matched_pairs = 0
        self._first_selection: Optional[Tile] = None
        self._build()

    # --- Board setup ------------------------------------------------------------------
    def _build(self) -> None:
        num_tiles = self.rows * self.cols
        assert num_tiles % 2 == 0, "Board must have an even number of tiles"
        needed_pairs = num_tiles // 2

        ids = available_identities()
        if needed_pairs > len(ids):
            raise ValueError("Not enough unique identities for the requested board size.")

        # Pick identities and duplicate to make pairs
        chosen = self.rng.sample(ids, needed_pairs)
        pool: List[Identity] = [*chosen, *chosen]
        self.rng.shuffle(pool)

        # Fill the grid
        self.grid = []
        k = 0
        for r in range(self.rows):
            row_tiles: List[Tile] = []
            for c in range(self.cols):
                row_tiles.append(Tile(r, c, pool[k]))
                k += 1
            self.grid.append(row_tiles)

    # --- Queries ----------------------------------------------------------------------
    def tile(self, row: int, col: int) -> Tile:
        return self.grid[row][col]

    def all_revealed(self) -> bool:
        return self.matched_pairs * 2 == self.rows * self.cols

    # --- Actions ----------------------------------------------------------------------
    def reveal(self, row: int, col: int) -> Tuple[Optional[Tile], Optional[Tile], bool]:
        """
        Reveal tile at (row, col).

        Returns (first_tile, second_tile, matched).
        - If this is the first selection of a pair, second_tile is None, matched is False.
        - If this is the second selection, returns both tiles and whether they matched.
        """
        t = self.tile(row, col)
        if t.revealed or t.matched:
            # Ignore clicks on already revealed/matched tiles
            return None, None, False

        t.revealed = True

        if self._first_selection is None:
            self._first_selection = t
            return t, None, False

        # Second selection
        first = self._first_selection
        self._first_selection = None
        self.moves += 1

        matched = first.identity == t.identity
        if matched:
            first.matched = t.matched = True
            self.matched_pairs += 1
        else:
            # Caller (UI) will hide them after a delay
            pass
        return first, t, matched

    def hide_unmatched(self, a: Tile, b: Tile) -> None:
        if a.matched or b.matched:
            return
        a.revealed = False
        b.revealed = False

    def for_each(self) -> Sequence[Tile]:
        for r in range(self.rows):
            for c in range(self.cols):
                yield self.grid[r][c]


__all__ = ["Board", "Tile", "Identity"]
