"""Game board widget for the 2048 game."""
from PySide6.QtWidgets import QFrame, QGridLayout, QWidget
from PySide6.QtCore import Qt, QPoint, QTimer
from typing import List, Optional, Tuple, Dict
from game2048 import Game2048


class GameBoardWidget(QFrame):
    """
    Game board widget containing all tiles.

    Displays the game board with 4x4 grid of tiles and handles
    updates and animations.
    """

    # Animation timing constants
    ANIMATION_DELAY_MS: int = 50
    TILE_SPACING: int = 10
    BOARD_PADDING: int = 10

    def __init__(
        self, game: Game2048, parent: Optional[QWidget] = None
    ):
        """
        Initialize the game board widget.

        Args:
            game: Game2048 instance to display
            parent: Parent widget
        """
        super().__init__(parent)
        self.game: Game2048 = game
        self._previous_board: Optional[List[List[int]]] = None
        self._tiles: List[List["TileWidget"]] = []  # type: ignore
        self._setup_ui()
        self.update_board()

    def _setup_ui(self) -> None:
        """Setup the game board UI and layout."""
        from tile_widget import TileWidget

        layout = QGridLayout()
        layout.setSpacing(self.TILE_SPACING)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create tile grid
        for row in range(self.game.size):
            tile_row: List[TileWidget] = []
            for col in range(self.game.size):
                tile = TileWidget(0, self)
                tile_row.append(tile)
                layout.addWidget(tile, row, col)
            self._tiles.append(tile_row)

        self.setLayout(layout)
        self._apply_styles()

    def _apply_styles(self) -> None:
        """Apply CSS styles to the board."""
        self.setStyleSheet("""
            QFrame {
                background-color: #bbada0;
                border-radius: 6px;
                padding: 10px;
            }
        """)

    def update_board(self, animate: bool = False) -> None:
        """
        Update all tiles to match the current game state.

        Args:
            animate: Whether to play animations for changes
        """
        current_board = self.game.get_board()

        if animate and self._previous_board:
            self._animate_update(current_board)
        else:
            self._update_immediate(current_board)

        self._previous_board = [row[:] for row in current_board]

    def _update_immediate(self, board: List[List[int]]) -> None:
        """
        Update board without animation.

        Args:
            board: Current board state
        """
        for row in range(self.game.size):
            for col in range(self.game.size):
                tile = self._tiles[row][col]
                expected_pos = self._get_tile_position(row, col)
                if tile.pos() != expected_pos:
                    tile.move(expected_pos)
                tile.update_value(board[row][col])

    def _animate_update(self, new_board: List[List[int]]) -> None:
        """
        Animate board changes with movement and appearance effects.

        Args:
            new_board: New board state after move
        """
        old_board = self._previous_board or [
            [0] * self.game.size for _ in range(self.game.size)
        ]

        # Categorize tile changes
        new_tiles: List[Tuple[int, int]] = []
        merge_tiles: List[Tuple[int, int]] = []

        for row in range(self.game.size):
            for col in range(self.game.size):
                new_val = new_board[row][col]
                old_val = old_board[row][col]

                if new_val != old_val:
                    if new_val in (2, 4) and old_val == 0:
                        new_tiles.append((row, col))
                    elif new_val > old_val and old_val != 0:
                        merge_tiles.append((row, col))

        # Update all tiles
        for row in range(self.game.size):
            for col in range(self.game.size):
                is_new = (row, col) in new_tiles
                is_merge = (row, col) in merge_tiles

                tile = self._tiles[row][col]
                value = new_board[row][col]

                if is_merge:
                    tile.update_value(value, animate=True)
                elif is_new:
                    tile.update_value(value, animate=False)
                    tile.hide()
                else:
                    tile.update_value(value, animate=False)

        # Show and animate new tiles after a short delay
        if new_tiles:
            QTimer.singleShot(
                self.ANIMATION_DELAY_MS,
                lambda: self._show_new_tiles(new_tiles)
            )

    def _show_new_tiles(
        self, new_tiles: List[Tuple[int, int]]
    ) -> None:
        """
        Show and animate appearance of new tiles.

        Args:
            new_tiles: List of (row, col) positions of new tiles
        """
        for row, col in new_tiles:
            tile = self._tiles[row][col]
            tile.show()
            tile._animate_appearance()

    def _get_tile_position(self, row: int, col: int) -> QPoint:
        """
        Get the screen position for a tile at given grid position.

        Args:
            row: Row index
            col: Column index

        Returns:
            Position as QPoint
        """
        layout = self.layout()
        if layout and isinstance(layout, QGridLayout):
            rect = layout.cellRect(row, col)
            return QPoint(rect.x(), rect.y())
        return QPoint(0, 0)

    def reset_board(self) -> None:
        """Reset the board display for a new game."""
        self._previous_board = None
        self.update_board()

    def get_tile(self, row: int, col: int) -> Optional["TileWidget"]:  # type: ignore
        """
        Get tile widget at specified position.

        Args:
            row: Row index
            col: Column index

        Returns:
            TileWidget at position or None if out of bounds
        """
        if 0 <= row < self.game.size and 0 <= col < self.game.size:
            return self._tiles[row][col]
        return None
