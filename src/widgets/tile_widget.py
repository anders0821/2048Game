"""Tile widget for the 2048 game."""
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QPoint, QTimer, QSequentialAnimationGroup
from PySide6.QtGui import QFont
from typing import Optional, Tuple


class TileWidget(QLabel):
    """Single tile widget with animations."""
    
    # Color schemes for different tile values
    COLORS = {
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
    
    TEXT_COLORS = {
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
    
    def __init__(self, value: int = 0, parent: Optional['GameBoardWidget'] = None):
        super().__init__(str(value) if value != 0 else "", parent)
        self.value = value
        self._setup_ui()
        self._setup_animations()
    
    def _setup_ui(self) -> None:
        """Setup the tile UI."""
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(100, 100)
        self.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.setStyleSheet(self._get_style(self.value))
    
    def _setup_animations(self) -> None:
        """Setup animation objects."""
        self.pos_animation = QPropertyAnimation(self, b"geometry")
        self.pos_animation.setDuration(150)
        self.pos_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(200)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        
        self.merge_scale_animation = QPropertyAnimation(self, b"geometry")
        self.merge_scale_animation.setDuration(300)
        self.merge_scale_animation.setEasingCurve(QEasingCurve.Type.OutElastic)
    
    def update_value(self, value: int, animate: bool = False) -> None:
        """Update tile value and appearance."""
        old_value = self.value
        is_merge = (old_value != 0 and value != 0 and value > old_value)
        
        self.value = value
        self.setText(str(value) if value != 0 else "")
        self.setStyleSheet(self._get_style(value))
        
        if animate and value != 0 and value in [2, 4]:
            self.animate_appearance()
        elif animate and is_merge:
            self.animate_merge()
    
    def animate_appearance(self) -> None:
        """Animate new tile appearance."""
        current_geo = self.geometry()
        center = current_geo.center()
        small_size = int(current_geo.width() * 0.6)
        
        start_geo = QRect(
            center.x() - small_size // 2,
            center.y() - small_size // 2,
            small_size, small_size
        )
        
        self.scale_animation.stop()
        self.scale_animation.setStartValue(start_geo)
        self.scale_animation.setEndValue(current_geo)
        self.scale_animation.start()
    
    def animate_merge(self) -> None:
        """Animate merged tile with enhanced effects."""
        current_geo = self.geometry()
        center = current_geo.center()
        original_size = current_geo.width()
        
        medium_size = int(original_size * 1.15)
        large_size = int(original_size * 1.25)
        
        start_geo = QRect(center.x() - original_size // 2, center.y() - original_size // 2, original_size, original_size)
        medium_geo = QRect(center.x() - medium_size // 2, center.y() - medium_size // 2, medium_size, medium_size)
        large_geo = QRect(center.x() - large_size // 2, center.y() - large_size // 2, large_size, large_size)
        end_geo = current_geo
        
        merge_group = QSequentialAnimationGroup()
        
        expand1 = QPropertyAnimation(self, b"geometry")
        expand1.setDuration(120)
        expand1.setEasingCurve(QEasingCurve.Type.OutQuad)
        expand1.setStartValue(start_geo)
        expand1.setEndValue(medium_geo)
        
        expand2 = QPropertyAnimation(self, b"geometry")
        expand2.setDuration(150)
        expand2.setEasingCurve(QEasingCurve.Type.OutElastic)
        expand2.setStartValue(medium_geo)
        expand2.setEndValue(large_geo)
        
        contract = QPropertyAnimation(self, b"geometry")
        contract.setDuration(200)
        contract.setEasingCurve(QEasingCurve.Type.InOutBack)
        contract.setStartValue(large_geo)
        contract.setEndValue(end_geo)
        
        merge_group.addAnimation(expand1)
        merge_group.addAnimation(expand2)
        merge_group.addAnimation(contract)
        merge_group.start()
        merge_group.finished.connect(lambda: self.setGeometry(end_geo))
    
    def animate_move_to(self, target_pos: QPoint) -> None:
        """Animate tile movement to target position."""
        current_geo = self.geometry()
        target_geo = QRect(target_pos.x(), target_pos.y(), current_geo.width(), current_geo.height())
        
        self.pos_animation.stop()
        self.pos_animation.setStartValue(current_geo)
        self.pos_animation.setEndValue(target_geo)
        self.pos_animation.start()
        self.pos_animation.finished.connect(lambda: self.setGeometry(target_geo))
    
    def _get_style(self, value: int) -> str:
        """Get tile style based on value."""
        bg_color = self.COLORS.get(value, "#3c3a32")
        text_color = self.TEXT_COLORS.get(value, "#f9f6f2")
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
