"""Main window for the 2048 game."""
from PySide6.QtWidgets import (
    QWidget, QApplication, QMainWindow, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from typing import Optional

from game2048 import Game2048
from widgets import GameBoardWidget


class MainWindow(QMainWindow):
    """Main window for the 2048 game."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.game = Game2048()
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self) -> None:
        """Setup the main window UI."""
        self.setWindowTitle("2048 Game")
        self.setFixedSize(500, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("2048")
        title_label.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #776e65;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Score and controls
        controls_layout = QHBoxLayout()

        self.score_label = QLabel(f"Score: {self.game.get_score()}")
        self.score_label.setFont(QFont("Arial", 16))
        self.score_label.setStyleSheet("color: #776e65;")

        self.new_game_button = QPushButton("New Game")
        self.new_game_button.setFont(QFont("Arial", 12))
        self.new_game_button.setStyleSheet("""
            QPushButton {
                background-color: #8f7a66;
                color: #f9f6f2;
                border: none;
                border-radius: 3px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #9f8a76;
            }
        """)

        controls_layout.addWidget(self.score_label)
        controls_layout.addStretch()
        controls_layout.addWidget(self.new_game_button)
        main_layout.addLayout(controls_layout)

        # Game board
        self.game_board = GameBoardWidget(self.game)
        main_layout.addWidget(self.game_board, alignment=Qt.AlignmentFlag.AlignCenter)

        # Instructions
        instructions = QLabel("Use arrow keys to play")
        instructions.setFont(QFont("Arial", 12))
        instructions.setStyleSheet("color: #776e65;")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(instructions)

        self.setStyleSheet("QMainWindow { background-color: #faf8ef; }")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _setup_connections(self) -> None:
        """Setup signal connections."""
        self.new_game_button.clicked.connect(self._new_game)

    def _new_game(self) -> None:
        """Start a new game."""
        self.game.reset()
        self.game_board.previous_board = None
        self._update_display()

    def _update_display(self, animate: bool = False) -> None:
        """Update the display."""
        self.score_label.setText(f"Score: {self.game.get_score()}")
        self.game_board.update_board(animate=animate)

        if self.game.won:
            QMessageBox.information(self, "Congratulations!", "You reached 2048! You won!")
        elif self.game.game_over:
            reply = QMessageBox.question(
                self, "Game Over",
                "Game Over! Would you like to play again?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._new_game()

    def keyPressEvent(self, event) -> None:
        """Handle keyboard input."""
        key_map = {
            Qt.Key.Key_Left: "left",
            Qt.Key.Key_Right: "right",
            Qt.Key.Key_Up: "up",
            Qt.Key.Key.Down: "down"
        }

        direction = key_map.get(event.key())
        if direction:
            moved = self.game.move(direction)
            if moved:
                self._update_display(animate=True)
            event.accept()
        else:
            super().keyPressEvent(event)
