"""Tile widget for the 2048 game."""
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QPoint
from PySide6.QtGui import QFont
from typing import Optional, Tuple


class TileWidget(QLabel):
    """
    Single tile widget with smooth animations.

    Displays a tile with appropriate colors and animations for
    appearance, movement, and merging.
    """

    # Color schemes for different tile values
    COLORS: dict[int, str] = {
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

    TEXT_COLORS: dict[int, str] = {
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

    # Default tile size
    TILE_SIZE: int = 100

    def __init__(
        self,
        value: int = 0,
        parent: Optional["GameBoardWidget"] = None,  # type: ignore
    ):
        """
        Initialize a tile widget.

        Args:
            value: Initial tile value (0 for empty)
            parent: Parent widget (GameBoardWidget)
        """
        super().__init__(str(value) if value != 0 else "", parent)
        self.value: int = value
        self._setup_ui()
        self._setup_animations()

    def _setup_ui(self) -> None:
        """Setup the tile UI components."""
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(self.TILE_SIZE, self.TILE_SIZE)
        self.setStyleSheet(self._get_style(self.value))
        self._update_font()

    def _update_font(self) -> None:
        """Update font size based on value."""
        font_size = self._get_font_size(self.value)
        self.setFont(QFont("Arial", font_size, QFont.Weight.Bold))

    def _setup_animations(self) -> None:
        """Setup animation objects for movement and scaling."""
        # Movement animation
        self.move_animation = QPropertyAnimation(self, b"geometry")
        self.move_animation.setDuration(120)
        self.move_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Scale animation for appearance
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(150)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutBack)

        # Merge animation
        self.merge_animation = QPropertyAnimation(self, b"geometry")
        self.merge_animation.setDuration(200)
        self.merge_animation.setEasingCurve(QEasingCurve.Type.OutElastic)

    def _get_font_size(self, value: int) -> int:
        """
        Get appropriate font size based on tile value.

        Args:
            value: Tile value

        Returns:
            Font size in points
        """
        if value < 100:
            return 28
        elif value < 1000:
            return 24
        else:
            return 20

    def update_value(self, value: int, animate: bool = False) -> None:
        """
        Update tile value and appearance.

        Args:
            value: New tile value
            animate: Whether to play animation
        """
        is_new_tile = self.value == 0 and value in (2, 4)
        is_merge = self.value != 0 and value > self.value and value == self.value * 2

        self.value = value
        self.setText(str(value) if value != 0 else "")
        self.setStyleSheet(self._get_style(value))
        self._update_font()

        if animate:
            if is_new_tile:
                self._animate_appearance()
            elif is_merge:
                self._animate_merge()

    def _animate_appearance(self) -> None:
        """Animate new tile appearance with scale effect."""
        current_geo = self.geometry()
        center = current_geo.center()
        small_size = int(current_geo.width() * 0.5)

        start_geo = QRect(
            center.x() - small_size // 2,
            center.y() - small_size // 2,
            small_size,
            small_size,
        )

        self.scale_animation.stop()
        self.scale_animation.setStartValue(start_geo)
        self.scale_animation.setEndValue(current_geo)
        self.scale_animation.start()

    def _animate_merge(self) -> None:
        """Animate merged tile with bounce effect."""
        current_geo = self.geometry()
        center = current_geo.center()
        size = current_geo.width()

        # Expand phase
        expand_size = int(size * 1.15)
        expand_geo = QRect(
            center.x() - expand_size // 2,
            center.y() - expand_size // 2,
            expand_size,
            expand_size,
        )

        self.merge_animation.stop()
        self.merge_animation.setStartValue(current_geo)
        self.merge_animation.setEndValue(expand_geo)
        self.merge_animation.start()
        self.merge_animation.finished.connect(
            lambda: self._animate_merge_contract(expand_geo, current_geo)
        )

    def _animate_merge_contract(
        self, expand_geo: QRect, final_geo: QRect
    ) -> None:
        """Complete merge animation by contracting back to normal size."""
        contract_animation = QPropertyAnimation(self, b"geometry")
        contract_animation.setDuration(150)
        contract_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        contract_animation.setStartValue(expand_geo)
        contract_animation.setEndValue(final_geo)
        contract_animation.start()

    def animate_move_to(self, target_pos: QPoint) -> None:
        """
        Animate tile movement to target position.

        Args:
            target_pos: Target position as QPoint
        """
        current_geo = self.geometry()
        target_geo = QRect(
            target_pos.x(),
            target_pos.y(),
            current_geo.width(),
            current_geo.height(),
        )

        self.move_animation.stop()
        self.move_animation.setStartValue(current_geo)
        self.move_animation.setEndValue(target_geo)
        self.move_animation.start()

    def _get_style(self, value: int) -> str:
        """
        Get CSS style for tile based on value.

        Args:
            value: Tile value

        Returns:
            CSS style string
        """
        bg_color = self.COLORS.get(value, "#3c3a32")
        text_color = self.TEXT_COLORS.get(value, "#f9f6f2")

        return f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 6px;
                font-weight: bold;
            }}
        """

    def get_value(self) -> int:
        """Get current tile value."""
        return self.value

    def is_empty(self) -> bool:
        """Check if tile is empty (value is 0)."""
        return self.value == 0
