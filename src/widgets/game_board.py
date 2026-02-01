"""Game board widget for the 2048 game."""
from PySide6.QtWidgets import QFrame, QGridLayout, QWidget
from PySide6.QtCore import Qt, QPoint, QTimer
from typing import List, Optional, Tuple
from game2048 import Game2048


class GameBoardWidget(QFrame):
    """Game board widget containing all tiles."""
    
    def __init__(self, game: Game2048, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.game = game
        self.previous_board: Optional[List[List[int]]] = None
        self._setup_ui()
        self.update_board()
    
    def _setup_ui(self) -> None:
        """Setup the game board UI."""
        from widgets.tile_widget import TileWidget
        
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.tiles: List[List[TileWidget]] = []
        for row in range(self.game.size):
            tile_row = []
            for col in range(self.game.size):
                tile = TileWidget(0, self)
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
            self._animate_update(current_board)
        else:
            self._update_immediate(current_board)
        
        self.previous_board = [row[:] for row in current_board]
    
    def _update_immediate(self, board: List[List[int]]) -> None:
        """Update board without animation."""
        for row in range(self.game.size):
            for col in range(self.game.size):
                tile = self.tiles[row][col]
                expected_pos = self._get_tile_position(row, col)
                tile.move(expected_pos.x(), expected_pos.y())
                tile.update_value(board[row][col])
    
    def _animate_update(self, new_board: List[List[int]]) -> None:
        """Animate board changes."""
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
                        if new_value in [2, 4]:
                            new_tiles.append((new_row, new_col))
                        else:
                            merge_tiles.append((new_row, new_col))
                    elif new_value != 0:
                        source = self._find_source(new_value, old_board)
                        if source:
                            moved_tiles[(new_row, new_col)] = (source, new_value)
        
        # Update tiles
        for row in range(self.game.size):
            for col in range(self.game.size):
                is_new = (row, col) in new_tiles
                is_merge = (row, col) in merge_tiles
                
                if is_merge:
                    self.tiles[row][col].update_value(new_board[row][col], animate=True)
                elif is_new:
                    self.tiles[row][col].update_value(new_board[row][col], animate=True)
                    self.tiles[row][col].hide()
                else:
                    self.tiles[row][col].update_value(new_board[row][col])
        
        # Animate movements
        for (new_row, new_col), ((old_row, old_col), value) in moved_tiles.items():
            if (old_row, old_col) != (new_row, new_col):
                target_pos = self._get_tile_position(new_row, new_col)
                self.tiles[new_row][new_col].animate_move_to(target_pos)
        
        # Show new tiles after delay
        if new_tiles:
            QTimer.singleShot(50, lambda: self._show_new_tiles(new_tiles))
    
    def _find_source(self, value: int, old_board: List[List[int]]) -> Optional[Tuple[int, int]]:
        """Find the source position of a tile."""
        for row in range(self.game.size):
            for col in range(self.game.size):
                if old_board[row][col] == value:
                    return (row, col)
        return None
    
    def _get_tile_position(self, row: int, col: int) -> QPoint:
        """Get the screen position for a tile."""
        layout = self.layout()
        if layout:
            rect = layout.cellRect(row, col)
            return QPoint(rect.x(), rect.y())
        return QPoint(0, 0)
    
    def _show_new_tiles(self, new_tiles: List[Tuple[int, int]]) -> None:
        """Show and animate new tiles."""
        for row, col in new_tiles:
            self.tiles[row][col].show()
            self.tiles[row][col].animate_appearance()
