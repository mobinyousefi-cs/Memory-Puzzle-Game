#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Memory Puzzle Game
File: main.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=====================================================================================================

Description:
Module entry point. Creates the Tkinter application and runs the UI.

Usage:
python -m memory_puzzle
memory-puzzle  # via console_script entry point
"""
from __future__ import annotations

import argparse

from .ui import MemoryApp


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Tkinter Memory Puzzle Game")
    p.add_argument("--level", choices=["easy", "medium", "hard"], default="easy", help="Board difficulty")
    p.add_argument("--seed", type=int, default=None, help="Deterministic RNG seed (for testing)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    level_map = {"easy": 0, "medium": 1, "hard": 2}
    app = MemoryApp(level_index=level_map[args.level], seed=args.seed)
    app.mainloop()


if __name__ == "__main__":
    main()
