# Memory Puzzle Game (Python, Tkinter)

A clean, testable, and extensible **Memory / Concentration** game implemented with **Tkinter**. Three difficulty levels (Easy, Medium, Hard), animated tile reveals, move counter, elapsed time, and a polished architecture following a modern Python project layout (PEP 621 `pyproject.toml`, `src/` layout, tests, CI with Ruff/Black/Pytest).

---

## ✨ Features
- **Three levels:** Easy (4×4), Medium (6×4), Hard (6×6)
- **Crisp visuals** rendered directly on a Tkinter `Canvas` (no external assets)
- **Scoring HUD:** moves, matched pairs, and elapsed time
- **Smooth UX:** click-to-reveal, match/highlight, automatic reshuffle on New Game
- **Keyboard shortcuts:** `N` (New Game), `E/M/H` (switch level), `Esc` (quit)
- **Robust design:** deterministic board generation with seed (for testing/repro)
- **CI-ready:** GitHub Actions workflow (Ruff + Black + Pytest)

---

## 🧱 Project Structure
```
memory-puzzle-game/
├─ .editorconfig
├─ .gitignore
├─ LICENSE
├─ pyproject.toml
├─ README.md
├─ requirements.txt
├─ src/
│  └─ memory_puzzle/
│     ├─ __init__.py
│     ├─ settings.py
│     ├─ assets.py
│     ├─ game.py
│     ├─ ui.py
│     └─ main.py
├─ tests/
│  └─ test_game.py
└─ .github/
   └─ workflows/
      └─ ci.yml
```

---

## 🚀 Run Locally
```bash
# (Optional) create a venv
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install tooling for dev/test (game uses stdlib only)
pip install -r requirements.txt

# Run the game
python -m memory_puzzle
```

Or run the module directly from `src/` root if not installing.

---

## 🔧 Development
- Lint & format:
  ```bash
  ruff check src tests
  black src tests
  ```
- Tests:
  ```bash
  pytest -q
  ```

---

## 🧪 Testing Philosophy
Core logic is isolated in `game.py` and does not depend on Tkinter. Unit tests cover:
- Board generation (pair counts, uniqueness, dimensions)
- Matching mechanics & move counting
- Game completion detection

---

## 🕹️ Controls & Gameplay
- **Click** a hidden tile to reveal it
- Reveal a **second tile**:
  - If matched → they stay revealed
  - If not → they flip back after a brief delay
- **HUD** shows: level, moves, matched pairs, time
- When all pairs are matched, a dialog summarizes your performance

**Shortcuts**
- `N` → New Game
- `E` / `M` / `H` → Switch level
- `Esc` → Quit

---

## ⚙️ Configuration
Tune defaults in `settings.py` (tile size, spacing, colors, delays). Board sizes per level are defined there as well.

---

## 📦 Packaging
This project uses the `src/` layout and PEP 621 metadata in `pyproject.toml`. You can install it in editable mode:
```bash
pip install -e .
python -m memory_puzzle
```

---

## 📜 License
MIT — see [LICENSE](LICENSE).

---

## 🙌 Credits
Designed for a polished, educational codebase suitable for a Master’s-level portfolio.

