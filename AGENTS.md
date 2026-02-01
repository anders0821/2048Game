# Agent Guidelines for 2048 Game

This file contains guidelines for AI agents working on this PySide6-based 2048 game repository.

## Build / Lint / Test Commands

### Running Tests
```bash
# Using virtual environment (recommended)
C:\Documents\Develop\venv\hswl312\Scripts\python.exe -m pytest tests/ -v

# Run all tests
python -m pytest tests/ -v

# Run a single specific test file
python -m pytest tests/test_game.py -v

# Run a single specific test class
python -m pytest tests/test_game.py::TestGame2048 -v

# Run a single specific test function
python -m pytest tests/test_game.py::TestGame2048::test_initial_score -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Code Quality & Linting
```bash
# Using virtual environment (recommended)
C:\Documents\Develop\venv\hswl312\Scripts\python.exe -m black src/ tests/ --line-length 88

# Format code with Black (line length: 88)
black src/ tests/ --line-length 88

# Sort imports with isort
isort src/ tests/

# Type check with mypy (strict mode enabled)
mypy src/ --python-version 3.12

# Lint with flake8
flake8 src/ tests/

# Run all quality checks
python run_tests.py
```

### Building & Packaging
```bash
# Package the game as executable
python package_game.py

# Or use PyInstaller directly
pyinstaller --name="2048Game" --windowed --onefile --clean src/main.py
```

### Running the Application
```bash
# Using virtual environment (recommended)
C:\Documents\Develop\venv\hswl312\Scripts\python.exe src/main.py

# Run the game directly
python src/main.py

# Or as a module
python -m src.main
```

## Code Style Guidelines

### Python Version
- **Python 3.12+** is required
- Use modern Python features (type hints, walrus operator where appropriate)

### Formatting (Black)
- Line length: **88 characters**
- Use Black for all Python files
- Target Python version: 3.12
- Trailing commas for multi-line imports/calls

### Import Style (isort)
- Profile: **black**
- Multi-line output: 3 (vertical hanging indent)
- Order: stdlib → third-party → first-party (src)
- Use `from typing import ...` for type hints

### Type Hints (Strict MyPy)
- **All functions must have type hints** (disallow_untyped_defs = true)
- Use `Optional[Type]` instead of `Type | None` for compatibility
- Use `List[Type]`, `Dict[Key, Value]` from typing module
- Return type `-> None` for procedures
- Always annotate class attributes with types

### Naming Conventions
- **Classes**: PascalCase (e.g., `Game2048`, `MainWindow`, `TileWidget`)
- **Functions/Methods**: snake_case (e.g., `move_left`, `animate_move_to`)
- **Variables**: snake_case (e.g., `game_over`, `current_score`)
- **Constants**: UPPER_SNAKE_CASE for module-level constants
- **Private methods**: prefix with underscore (e.g., `_add_random_tile`)

### Error Handling
- Use try/except for external dependencies (PySide6 imports)
- Print user-friendly error messages with ❌ emoji for failures
- Return boolean success indicators from test functions
- Don't suppress exceptions silently - log or re-raise them

### Documentation
- All modules should have a docstring describing their purpose
- All public classes need class docstrings
- All public methods need docstrings explaining what they do
- Use imperative mood (e.g., "Run smoke test" not "Runs smoke test")

### Qt/PySide6 Specifics
- Use `Qt.Key_Left` (not `Qt.Key.Key_Left`) for key enums
- Always call `app.exec()` not `exec_()` (Python 3 only)
- Use type hints for QWidget parameters: `parent: Optional[QWidget] = None`
- Connect signals with modern syntax: `obj.signal.connect(slot)`

### Testing
- Tests are in `tests/` directory
- Test files named `test_*.py`
- Test functions named `test_*`
- Use pytest for unit tests
- Test classes should group related functionality (e.g., `TestGame2048`, `TestTileMerging`)

### Project Structure
```
2048-game/
- src/                 # Source code
  - main.py           # Application entry point
  - main_window.py    # Main window and UI
  - game2048.py       # Game logic
  - widgets/          # UI components
    - __init__.py
    - tile_widget.py
    - game_board.py
- tests/              # Unit tests
  - test_game.py      # Game logic tests
- package_game.py     # Build script
- pyproject.toml      # Tool configurations
```

### Dependencies
- **GUI**: PySide6 >= 6.0.0
- **Testing**: pytest >= 7.0.0
- **Linting**: black, flake8, mypy, isort
- No external build tools needed beyond Python + pip

### Pre-commit Checklist
Before committing, ensure:
1. ✅ Code passes `black src/ tests/ --line-length 88`
2. ✅ Imports sorted with `isort src/ tests/`
3. ✅ Type checks pass with `mypy src/`
4. ✅ Tests pass with `pytest tests/ -v`
5. ✅ Smoke test passes with `python smoke_test.py`

### Common Patterns
- Game logic is separate from UI (MVC pattern)
- Animations use QPropertyAnimation with custom easing curves
- UI updates trigger from game state changes
- Print statements use emojis for visual feedback (✅ ❌ 🚀 🧪)
