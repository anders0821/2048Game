# 🎮 2048 Game

A 2048 puzzle game implemented with PySide6, featuring smooth animations and beautiful interface design.

![2048 Game](https://img.shields.io/badge/Version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.12+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.0+-blue.svg)

## ✨ Features

### 🎮 Game Features
- Classic 2048 game rules
- Keyboard arrow key controls (↑↓←→)
- Real-time score tracking with best score persistence
- Game win/loss detection
- New game reset functionality

### 🎨 Visual Effects
- Beautiful interface design and color schemes
- Smooth animation system:
  - Smooth tile movement
  - Multi-stage scaling animations on merge
  - Golden highlight and flash effects
  - New tile elastic appearance animation
- Responsive design and shadow effects

### 🛠️ Technical Features
- Object-oriented architecture design
- Complete animation framework with smooth tile merge effects
- Centralized import management via common.py
- Modular code structure with reusable UI components
- Comprehensive error handling

## Installation

### Requirements

- Python 3.12+
- PySide6

### Installation Steps

1. Clone or download the project
2. Install dependencies:

```bash
# Install runtime dependencies only (for deployment)
pip install -r requirements.txt

# Or install development dependencies (includes testing tools)
pip install -r requirements-dev.txt

# Or install PySide6 directly
pip install PySide6>=6.0.0
```

## Usage

### Run Directly

```bash
# Run in PyCharm
python src/main.py

# Or run in command line
python src/main.py
```

### Run as Package

```bash
# Install as development package
pip install -e .

# Run
python -m src.main
```

### Package as Executable

```bash
# Automated packaging (recommended)
python package_game.py

# Or use PyInstaller directly
pyinstaller 2048Game.spec

# Simple packaging
pyinstaller --name="2048Game" --windowed --onefile src/main.py
```

After packaging is complete, the executable file is located at:
- `dist/2048Game.exe` - Standalone executable file

### Game Controls

- **Arrow keys** (↑ ↓ ← →): Move tiles
- **New Game button**: Start a new game
- **Goal**: Reach 2048 by merging identical numbers

## 📁 Project Structure

```
2048-game/
├── 📂 src/                    # Source code directory
│   ├── __init__.py            # Package initialization
│   ├── main.py               # Main program entry
│   ├── main_window.py        # Main window and UI components
│   ├── game2048.py           # Game logic core
│   ├── common.py             # Common imports
│   ├── tile_widget.py        # Tile UI component
│   └── game_board_widget.py  # Game board widget
├── 📂 tests/                  # Test files
│   ├── __init__.py
│   └── test_game.py          # Unit tests
├── 🔧 package_game.py         # Automated packaging script
├── 🔧 2048Game.spec          # PyInstaller configuration
├── 🧪 run_tests.py           # Test suite
├── 📄 setup.py              # Installation configuration
├── 📄 pyproject.toml         # Project configuration
├── 📄 requirements.txt       # Runtime dependencies
├── 📄 requirements-dev.txt   # Development dependencies
└── 📖 README.md              # Project documentation
```

## 🛠️ Development Guide

### Environment Setup

```bash
# Clone the project
git clone <repository-url>
cd 2048-game

# Install development dependencies
pip install -r requirements-dev.txt

# Or install manually
pip install PySide6>=6.0.0 pytest black mypy flake8 isort
```

### Development Tools

```bash
# Code formatting
black src/ --line-length 88

# Import sorting
isort src/

# Type checking
mypy src/ --python-version 3.12

# Code style checking
flake8 src/

# Run tests
pytest tests/ -v

# Complete test suite
python run_tests.py
```

### Testing

The project includes a complete testing system:

```bash
# Run all tests
python run_tests.py

# Unit tests only
pytest tests/ -v

# Run specific test file
pytest tests/test_game.py -v

# Run specific test function
pytest tests/test_game.py::TestGame2048::test_initial_score -v
```

### Code Quality

- ✅ **Black** - Code formatting
- ✅ **MyPy** - Static type checking  
- ✅ **Flake8** - Code style checking
- ✅ **iSort** - Import statement sorting
- ✅ **Unit Tests** - Component testing with pytest

## 🎯 Game Rules

### Basic Gameplay
1. **Move**: Use arrow keys (↑↓←→) to move all tiles
2. **Merge**: Tiles with identical numbers merge into their sum when colliding
3. **New tile**: A new 2 or 4 appears randomly after each move
4. **Win**: Game is won when a 2048 tile appears
5. **Loss**: Game is over when the board is full and no moves are possible

### Strategy Tips
- Keep large numbers in corners when possible
- Avoid separating large numbers with small ones
- Build increasing number sequences
- Maintain consistent movement patterns

## 🏗️ Technical Architecture

### Core Components

| Component | Function | Features |
|------|------|------|
| **Game2048** | Game logic core | Move algorithm, merge detection, state management |
| **MainWindow** | Main window controller | Event handling, UI layout, game flow |
| **TileWidget** | Number tile component | Animation system, style management, interaction feedback |
| **GameBoardWidget** | Game board management | Grid layout, animation coordination, state synchronization |

### Animation Engine

- **🎬 Position Animation**: `QPropertyAnimation` for smooth movement
- **🎭 Scaling Animation**: `QSequentialAnimationGroup` for multi-stage effects
- **🌈 Color Transition**: Dynamic style changes enhance visual feedback
- **⚡ Performance Optimization**: Smart animation queue prevents overlap and lag

### Design Patterns

- **MVC Architecture**: Clear separation of Model-View-Controller
- **Component-based Design**: Reusable UI components
- **Event-driven**: Responsive user interactions
- **State Management**: Centralized game state control

## 📦 Distribution and Deployment

### Executable File

The project supports multiple distribution methods:

```bash
# Automated packaging (recommended)
python package_game.py
```

Packaging features:
- ✅ Single file executable (~15-20MB)
- ✅ No Python environment required
- ✅ Cross-Windows version compatible
- ✅ Includes complete dependency libraries

### Release Version

After packaging is complete:
```
📁 dist/
└── 📄 2048Game.exe           # Main executable file
```

## 🤝 Contributing Guidelines

Welcome contributions and improvement suggestions!

### Ways to Contribute
1. 🐛 **Report Issues**: Submit an Issue describing a bug
2. 💡 **Feature Suggestions**: Propose new feature ideas
3. 🔧 **Code Contributions**: Submit a Pull Request
4. 📖 **Documentation Improvements**: Improve documentation and instructions

### Development Workflow
1. Fork the project repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

### Code Standards
- Follow PEP 8 code style
- Use Black for code formatting
- Add appropriate type annotations
- Write unit tests
- Update related documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

### License Highlights
- ✅ Commercial use
- ✅ Modification and distribution
- ✅ Private use
- ⚠️ Must include license and copyright notice
- ⚠️ No liability warranty provided

---

## 🙏 Acknowledgments

Thanks to all developers and users who have contributed to this project!

**Tech Stack**:
- [PySide6](https://doc.qt.io/qtforpython/) - Qt for Python GUI Framework
- [Python](https://www.python.org/) - Programming Language
- [PyInstaller](https://pyinstaller.org/) - Packaging Tool

**Inspiration Sources**:
- [2048 Original Game](https://play2048.co/) by Gabriele Cirulli
- PySide6 official documentation and community

---

<div align="center">

**🎮 Enjoy the game, enjoy coding!**

Made with ❤️ by [Your Name]

</div>
