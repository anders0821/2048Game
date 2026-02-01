from PySide6.QtWidgets import (
    QWidget, QApplication, QMainWindow, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QGridLayout,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPalette, QColor
from typing import Optional

from .game2048 import Game2048


class TileWidget(QLabel):
    """Single tile widget for the 2048 game."""
    
    def __init__(self, value: int = 0, parent: Optional[QWidget] = None):
        super().__init__(str(value) if value != 0 else "", parent)
        self.value = value
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(100, 100)
        self.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.setStyleSheet(self._get_tile_style(value))
    
    def update_value(self, value: int) -> None:
        """Update tile value and appearance."""
        self.value = value
        self.setText(str(value) if value != 0 else "")
        self.setStyleSheet(self._get_tile_style(value))
    
    def _get_tile_style(self, value: int) -> str:
        """Get tile style based on value."""
        colors = {
            0: "#cdc1b4",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
        }
        
        text_colors = {
            0: "#776e65",
            2: "#776e65",
            4: "#776e65",
            8: "#f9f6f2",
            16: "#f9f6f2",
            32: "#f9f6f2",
            64: "#f9f6f2",
            128: "#f9f6f2",
            256: "#f9f6f2",
            512: "#f9f6f2",
            1024: "#f9f6f2",
            2048: "#f9f6f2",
        }
        
        bg_color = colors.get(value, "#3c3a32")
        text_color = text_colors.get(value, "#f9f6f2")
        
        font_size = 48 if value < 100 else 36 if value < 1000 else 28
        
        return f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 6px;
                font-size: {font_size}px;
                font-weight: bold;
            }}
        """


class GameBoardWidget(QFrame):
    """Game board widget containing all tiles."""
    
    def __init__(self, game: Game2048, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.game = game
        self.setup_ui()
        self.update_board()
    
    def setup_ui(self) -> None:
        """Setup the game board UI."""
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.tiles = []
        for row in range(self.game.size):
            tile_row = []
            for col in range(self.game.size):
                tile = TileWidget(0)
                tile_row.append(tile)
                layout.addWidget(tile, row, col)
            self.tiles.append(tile_row)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QFrame {
                background-color: #bbada0;
                border-radius: 6px;
                padding: 10px;
            }
        """)
    
    def update_board(self) -> None:
        """Update all tiles to match the game state."""
        board = self.game.get_board()
        for row in range(self.game.size):
            for col in range(self.game.size):
                self.tiles[row][col].update_value(board[row][col])


class MainWindow(QMainWindow):
    """Main window for the 2048 game."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.game = Game2048()
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self) -> None:
        """Setup the main window UI."""
        self.setWindowTitle("2048 Game")
        self.setFixedSize(500, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
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
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #faf8ef;
            }
        """)
    
    def setup_connections(self) -> None:
        """Setup signal connections."""
        self.new_game_button.clicked.connect(self.new_game)
    
    def new_game(self) -> None:
        """Start a new game."""
        self.game.reset()
        self.update_display()
    
    def update_display(self) -> None:
        """Update the display with current game state."""
        self.score_label.setText(f"Score: {self.game.get_score()}")
        self.game_board.update_board()
        
        # Check game state
        if self.game.won:
            QMessageBox.information(self, "Congratulations!", 
                                  "You reached 2048! You won!")
        elif self.game.game_over:
            reply = QMessageBox.question(self, "Game Over", 
                                       "Game Over! Would you like to play again?",
                                       QMessageBox.StandardButton.Yes | 
                                       QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.new_game()
    
    def keyPressEvent(self, event) -> None:
        """Handle keyboard input."""
        key_map = {
            Qt.Key.Key_Left: "left",
            Qt.Key.Key_Right: "right", 
            Qt.Key.Key_Up: "up",
            Qt.Key.Key_Down: "down"
        }
        
        direction = key_map.get(event.key())
        if direction:
            moved = self.game.move(direction)
            if moved:
                self.update_display()