#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Memory Puzzle Game
File: test_game.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=====================================================================================================

Description:
Unit tests for pure game logic (no GUI dependencies).
"""
from __future__ import annotations

import itertools

import pytest

from memory_puzzle.game import Board
from memory_puzzle.settings import EASY, MEDIUM, HARD


@pytest.mark.parametrize("level", [EASY, MEDIUM, HARD])
def test_board_pairing(level):
    b = Board(level, seed=42)
    identities = [(t.identity) for t in b.for_each()]
    assert len(identities) == level.rows * level.cols
    # Each identity appears exactly twice
    counts = {k: identities.count(k) for k in set(identities)}
    assert all(v == 2 for v in counts.values())


def test_moves_and_matching():
    b = Board(EASY, seed=123)
    # Build lookup from identity to positions
    pos = {}
    for t in b.for_each():
        pos.setdefault(t.identity, []).append((t.row, t.col))
    # Flip all pairs correctly
    for positions in pos.values():
        (r1, c1), (r2, c2) = positions
        first, second, matched = b.reveal(r1, c1)
        assert second is None and not matched
        first, second, matched = b.reveal(r2, c2)
        assert matched
    assert b.all_revealed()
    # Number of moves equals number of pairs
    assert b.moves == (b.rows * b.cols) // 2


def test_mismatch_then_hide():
    b = Board(EASY, seed=7)
    # Find two tiles with different identities
    pairs = {}
    all_tiles = list(b.for_each())
    a, btile = None, None
    for t in all_tiles:
        pairs.setdefault(t.identity, []).append(t)
    ids = list(pairs.keys())
    a = pairs[ids[0]][0]
    btile = pairs[ids[1]][0]

    first, second, matched = b.reveal(a.row, a.col)
    assert second is None and not matched
    first, second, matched = b.reveal(btile.row, btile.col)
    assert second is not None and not matched
    b.hide_unmatched(first, second)
    assert not first.revealed and not second.revealed
