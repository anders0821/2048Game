from PySide6.QtWidgets import (
    QWidget, QApplication, QMainWindow, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QGridLayout,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect, QPoint, QTimer, QParallelAnimationGroup, QSequentialAnimationGroup
from PySide6.QtGui import QFont, QPalette, QColor
from typing import Optional, List, Tuple

from game2048 import Game2048


class TileWidget(QLabel):
    """Single tile widget for the 2048 game."""
    
    def __init__(self, value: int = 0, parent: Optional[QWidget] = None):
        super().__init__(str(value) if value != 0 else "", parent)
        self.value = value
        self.target_pos: Optional[QPoint] = None
        self.is_new = False
        self.is_merged = False
        
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(100, 100)
        self.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.setStyleSheet(self._get_tile_style(value))
        
        # Setup animations
        self.pos_animation = QPropertyAnimation(self, b"geometry")
        self.pos_animation.setDuration(150)
        self.pos_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(200)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        
        # Merge specific animations
        self.merge_scale_animation = QPropertyAnimation(self, b"geometry")
        self.merge_scale_animation.setDuration(300)
        self.merge_scale_animation.setEasingCurve(QEasingCurve.Type.OutElastic)
        
        # Color transition animation
        self.color_animation = QPropertyAnimation(self, b"stylesheet")
        self.color_animation.setDuration(250)
        self.color_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
    
    def update_value(self, value: int, animate: bool = False) -> None:
        """Update tile value and appearance."""
        # Detect merge before updating value
        old_value = self.value
        is_merge = (old_value != 0 and value != 0 and value > old_value)
        
        print(f"🔍 Tile update: {old_value} -> {value}, animate: {animate}, is_merge: {is_merge}")
        
        self.value = value
        self.setText(str(value) if value != 0 else "")
        self.setStyleSheet(self._get_tile_style(value))
        
        # Animate appearance of new tiles
        if animate and self.value != 0 and self.value in [2, 4]:
            print(f"🎱 New tile animation: {self.value}")
            self.animate_appearance()
        # Enhanced merge animation
        elif animate and is_merge:
            print(f"🔥 Merge animation triggered: {old_value} -> {value}")
            self.animate_merge()
        else:
            print(f"📝 No animation: value={value}, animate={animate}, old_value={old_value}")
    
    def animate_appearance(self) -> None:
        """Animate new tile appearance."""
        current_geo = self.geometry()
        
        # Ensure correct position before animation
        row, col = self._find_my_position()
        correct_pos = self.parent()._get_tile_position(row, col)
        if current_geo.x() != correct_pos.x() or current_geo.y() != correct_pos.y():
            current_geo.moveTo(correct_pos.x(), correct_pos.y())
            self.setGeometry(current_geo)
        
        center = current_geo.center()
        small_size = int(current_geo.width() * 0.6)
        
        start_geo = QRect(
            center.x() - small_size // 2,
            center.y() - small_size // 2,
            small_size,
            small_size
        )
        
        # Reset animation
        self.scale_animation.stop()
        self.scale_animation.setStartValue(start_geo)
        self.scale_animation.setEndValue(current_geo)
        self.scale_animation.start()
    
    def _find_my_position(self) -> Tuple[int, int]:
        """Find this tile's grid position."""
        if hasattr(self.parent(), 'tiles'):
            tiles = self.parent().tiles
            for row in range(len(tiles)):
                for col in range(len(tiles[row])):
                    if tiles[row][col] is self:
                        return row, col
        return 0, 0  # Fallback
    
    def animate_merge(self) -> None:
        """Animate merged tile with enhanced effects."""
        # Ensure correct position before animation
        row, col = self._find_my_position()
        correct_pos = self.parent()._get_tile_position(row, col)
        current_geo = self.geometry()
        
        if current_geo.x() != correct_pos.x() or current_geo.y() != correct_pos.y():
            current_geo.moveTo(correct_pos.x(), correct_pos.y())
            self.setGeometry(current_geo)
        
        center = current_geo.center()
        
        # Multiple scale stages for better effect
        original_size = current_geo.width()
        medium_size = int(original_size * 1.15)
        large_size = int(original_size * 1.25)
        
        start_geo = QRect(
            center.x() - original_size // 2,
            center.y() - original_size // 2,
            original_size,
            original_size
        )
        
        medium_geo = QRect(
            center.x() - medium_size // 2,
            center.y() - medium_size // 2,
            medium_size,
            medium_size
        )
        
        large_geo = QRect(
            center.x() - large_size // 2,
            center.y() - large_size // 2,
            large_size,
            large_size
        )
        
        end_geo = current_geo
        
        # Create sequential animation group
        merge_group = QSequentialAnimationGroup()
        
        # First expansion
        expand1 = QPropertyAnimation(self, b"geometry")
        expand1.setDuration(120)
        expand1.setEasingCurve(QEasingCurve.Type.OutQuad)
        expand1.setStartValue(start_geo)
        expand1.setEndValue(medium_geo)
        
        # Second expansion with elastic effect
        expand2 = QPropertyAnimation(self, b"geometry")
        expand2.setDuration(150)
        expand2.setEasingCurve(QEasingCurve.Type.OutElastic)
        expand2.setStartValue(medium_geo)
        expand2.setEndValue(large_geo)
        
        # Contraction with bounce
        contract = QPropertyAnimation(self, b"geometry")
        contract.setDuration(200)
        contract.setEasingCurve(QEasingCurve.Type.InOutBack)
        contract.setStartValue(large_geo)
        contract.setEndValue(end_geo)
        
        merge_group.addAnimation(expand1)
        merge_group.addAnimation(expand2)
        merge_group.addAnimation(contract)
        
        # Animate color change
        self._animate_color_transition()
        
        # Start animations
        merge_group.start()
        
        # Flash effect on completion - ensure final position
        merge_group.finished.connect(lambda: self._ensure_final_position(end_geo))
        merge_group.finished.connect(self._flash_effect)
    
    def _animate_color_transition(self) -> None:
        """Animate color transition during merge."""
        original_style = self.styleSheet()
        
        # Create highlight style
        highlight_style = original_style.replace("background-color:", "background-color: #FFD700;")
        
        # Animate to highlight and back
        self.color_animation.setStartValue(original_style)
        self.color_animation.setEndValue(highlight_style)
        self.color_animation.start()
        
        # Animate back to original color
        QTimer.singleShot(100, lambda: self._animate_color_back(original_style))
    
    def _animate_color_back(self, original_style: str) -> None:
        """Animate back to original color."""
        back_animation = QPropertyAnimation(self, b"stylesheet")
        back_animation.setDuration(150)
        back_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        back_animation.setStartValue(self.styleSheet())
        back_animation.setEndValue(original_style)
        back_animation.start()
    
    def _flash_effect(self) -> None:
        """Create a flash effect after merge animation."""
        # Create temporary overlay effect
        original_style = self.styleSheet()
        
        # Add glow effect
        glow_style = original_style.replace("}", """
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
            border: 2px solid #FFD700;
        }""")
        
        self.setStyleSheet(glow_style)
        
        # Remove glow effect after short delay
        QTimer.singleShot(200, lambda: self.setStyleSheet(original_style))
    
    def animate_move_to(self, target_pos: QPoint) -> None:
        """Animate tile movement to target position."""
        # Ensure we get the correct current position
        current_geo = self.geometry()
        target_geo = QRect(
            target_pos.x(), target_pos.y(),
            current_geo.width(), current_geo.height()
        )
        
        print(f"🎯 Moving tile from ({current_geo.x()}, {current_geo.y()}) to ({target_pos.x()}, {target_pos.y()})")
        
        # Stop any existing animation
        self.pos_animation.stop()
        
        # Set animation properties
        self.pos_animation.setStartValue(current_geo)
        self.pos_animation.setEndValue(target_geo)
        
        # Start animation
        self.pos_animation.start()
        
        # Ensure final position is correct after animation
        self.pos_animation.finished.connect(
            lambda: self._ensure_final_position(target_geo)
        )
    
    def _ensure_final_position(self, target_geo: QRect) -> None:
        """Ensure tile ends up at exactly the right position."""
        self.pos_animation.finished.disconnect()
        self.setGeometry(target_geo)
    
    def _get_tile_style(self, value: int) -> str:
        """Get tile style based on value with enhanced effects."""
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
        
        # Enhanced shadow for better merge effect visibility
        shadow_style = """
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        """ if value > 0 else ""
        
        return f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 6px;
                font-size: {font_size}px;
                font-weight: bold;
                {shadow_style}
                transition: all 0.3s ease;
            }}
        """


class GameBoardWidget(QFrame):
    """Game board widget containing all tiles."""
    
    def __init__(self, game: Game2048, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.game = game
        self.previous_board = None
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
    
    def update_board(self, animate: bool = False) -> None:
        """Update all tiles to match the game state."""
        current_board = self.game.get_board()
        
        if animate and self.previous_board:
            self._animate_board_update(current_board)
        else:
            self._update_board_immediate(current_board)
        
        self.previous_board = [row[:] for row in current_board]
    
    def _update_board_immediate(self, board: List[List[int]]) -> None:
        """Update board without animation."""
        for row in range(self.game.size):
            for col in range(self.game.size):
                # Reset tile position to ensure correct placement
                tile = self.tiles[row][col]
                expected_pos = self._get_tile_position(row, col)
                tile.move(expected_pos.x(), expected_pos.y())
                self.tiles[row][col].update_value(board[row][col])
    
    def _animate_board_update(self, new_board: List[List[int]]) -> None:
        """Animate board changes with movement, appearance, and merge effects."""
        old_board = self.previous_board or [[0] * self.game.size for _ in range(self.game.size)]
        moved_tiles = {}
        new_tiles = []
        merge_tiles = []
        
        # Track tile movements and new tiles
        for new_row in range(self.game.size):
            for new_col in range(self.game.size):
                new_value = new_board[new_row][new_col]
                old_value = old_board[new_row][new_col]
                
                if new_value != old_value:
                    if new_value != 0 and old_value == 0:
                        # Check if this is a new tile (2 or 4) or a merge result
                        if new_value in [2, 4]:
                            # New tile appeared
                            new_tiles.append((new_row, new_col))
                        else:
                            # This is a merge result (value > 4)
                            merge_tiles.append((new_row, new_col))
                    elif new_value != 0:
                        # Tile moved or merged - find its source
                        source = self._find_tile_source(new_value, old_board)
                        if source:
                            moved_tiles[(new_row, new_col)] = (source, new_value)
        
        # First, update all tiles to their new values
        for row in range(self.game.size):
            for col in range(self.game.size):
                old_value = old_board[row][col]
                new_value = new_board[row][col]
                
                # Determine animation type
                is_new = (row, col) in new_tiles
                is_merge = (row, col) in merge_tiles
                
                print(f"📍 Cell ({row},{col}): old={old_value}, new={new_value}, is_new={is_new}, is_merge={is_merge}")
                
                # Update tile with appropriate animation - always animate for testing
                if is_merge:
                    print(f"🔥 Merge detected at ({row}, {col}): {old_value} -> {new_value}")
                    self.tiles[row][col].update_value(new_board[row][col], animate=True)
                elif is_new:
                    print(f"🎱 New tile at ({row}, {col}): {new_value}")
                    self.tiles[row][col].update_value(new_board[row][col], animate=True)
                    self.tiles[row][col].hide()
                else:
                    # For testing, always animate to see what happens
                    self.tiles[row][col].update_value(new_board[row][col], animate=True)
        
        # Animate movements
        for (new_row, new_col), ((old_row, old_col), value) in moved_tiles.items():
            target_pos = self._get_tile_position(new_row, new_col)
            if (old_row, old_col) != (new_row, new_col):
                # Move tile from old position to new position
                self.tiles[new_row][new_col].move(target_pos)
                self.tiles[new_row][new_col].animate_move_to(target_pos)
        
        # Show and animate new tiles after a short delay
        if new_tiles:
            QTimer.singleShot(50, lambda: self._show_new_tiles(new_tiles))
    
    def _find_tile_source(self, value: int, old_board: List[List[int]]) -> Optional[Tuple[int, int]]:
        """Find the source position of a tile value in the old board."""
        for row in range(self.game.size):
            for col in range(self.game.size):
                if old_board[row][col] == value:
                    return (row, col)
        return None
    
    def _get_tile_position(self, row: int, col: int) -> QPoint:
        """Get the screen position for a tile at given grid position."""
        # Calculate position based on grid layout to avoid cumulative errors
        if hasattr(self, 'tiles') and len(self.tiles) > row and len(self.tiles[row]) > col:
            tile = self.tiles[row][col]
            # Get the layout's intended position
            layout = self.layout()
            if layout:
                rect = layout.cellRect(row, col)
                return QPoint(rect.x(), rect.y())
        
        # Fallback to tile's current position
        tile = self.tiles[row][col]
        return QPoint(tile.x(), tile.y())
    
    def _show_new_tiles(self, new_tiles: List[Tuple[int, int]]) -> None:
        """Show and animate new tiles."""
        for row, col in new_tiles:
            self.tiles[row][col].show()
            self.tiles[row][col].animate_appearance()


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
        
        # Ensure the window can receive keyboard focus
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    
    def setup_connections(self) -> None:
        """Setup signal connections."""
        self.new_game_button.clicked.connect(self.new_game)
    
    def new_game(self) -> None:
        """Start a new game."""
        self.game.reset()
        self.game_board.previous_board = None
        self.update_display()
    
    def update_display(self, animate: bool = False) -> None:
        """Update the display with current game state."""
        self.score_label.setText(f"Score: {self.game.get_score()}")
        self.game_board.update_board(animate=animate)
        
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
                self.update_display(animate=True)
            event.accept()
        else:
            super().keyPressEvent(event)