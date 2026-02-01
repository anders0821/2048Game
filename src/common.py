"""Common imports for the 2048 game.

This module consolidates all imports used across the project.
Use 'from common import *' to import all commonly used modules.
"""

# Standard library imports
import random
import sys
from enum import Enum, auto

# Third-party imports - PySide6
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import (
    Qt,
    QPoint,
    QPropertyAnimation,
    QEasingCurve,
    QRect,
    QTimer,
)
from PySide6.QtGui import (
    QFont,
    QIcon,
    QKeyEvent,
    QPixmap,
)

# Type hints
from typing import (
    List,
    Tuple,
    Optional,
    Dict,
    Callable,
)

# Local module imports - these will be available but may cause circular imports
# if used directly in common.py. Import them in the specific files that need them.
# from game2048 import Game2048
# from tile_widget import TileWidget
# from game_board_widget import GameBoardWidget
# from main_window import MainWindow

__all__ = [
    # Standard library
    'random',
    'sys',
    'Enum',
    'auto',
    # PySide6 - QtWidgets
    'QApplication',
    'QFrame',
    'QGridLayout',
    'QHBoxLayout',
    'QLabel',
    'QMainWindow',
    'QMessageBox',
    'QPushButton',
    'QVBoxLayout',
    'QWidget',
    # PySide6 - QtCore
    'Qt',
    'QPoint',
    'QPropertyAnimation',
    'QEasingCurve',
    'QRect',
    'QTimer',
    # PySide6 - QtGui
    'QFont',
    'QIcon',
    'QKeyEvent',
    'QPixmap',
    # Typing
    'List',
    'Tuple',
    'Optional',
    'Dict',
    'Callable',
]
