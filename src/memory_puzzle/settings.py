#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Memory Puzzle Game
File: settings.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=====================================================================================================

Description:
Central configuration for UI and game behavior.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LevelConfig:
    name: str
    rows: int
    cols: int


# Board sizes per level
EASY = LevelConfig("Easy", rows=4, cols=4)
MEDIUM = LevelConfig("Medium", rows=4, cols=6)
HARD = LevelConfig("Hard", rows=6, cols=6)

LEVELS = (EASY, MEDIUM, HARD)

# UI metrics
TILE_SIZE = 80
TILE_GAP = 10
PADDING = 20
HUD_HEIGHT = 60

# Delays (ms)
MISMATCH_HIDE_DELAY = 650

# Colors
BG_COLOR = "#0f172a"  # slate-900
CANVAS_BG = "#111827"  # gray-900
TILE_BG = "#1f2937"  # gray-800
TILE_HOVER = "#334155"  # slate-700
TILE_REVEALED = "#0ea5e9"  # sky-500
TILE_MATCHED = "#22c55e"  # green-500
HUD_FG = "#e5e7eb"  # gray-200

# Fonts
FONT_HUD = ("Segoe UI", 12, "bold")

# RNG default seed (None → random). Tests may override.
DEFAULT_SEED = None
