"""Main window for the 2048 game."""
from common import *
from game2048 import Game2048
from game_board_widget import GameBoardWidget


class MainWindow(QMainWindow):
    """
    Main window for the 2048 game.

    Provides the main UI with score display, game controls,
    game board, and keyboard handling.
    """

    # Window dimensions
    WINDOW_WIDTH: int = 500
    WINDOW_HEIGHT: int = 600

    # Color scheme
    BG_COLOR: str = "#faf8ef"
    TEXT_COLOR: str = "#776e65"
    BUTTON_BG: str = "#8f7a66"
    BUTTON_HOVER: str = "#9f8a76"

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the main window.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.game: Game2048 = Game2048()
        self._setup_ui()
        self._setup_connections()
        self._setup_shortcuts()

    def _setup_ui(self) -> None:
        """Setup the main window UI components."""
        self.setWindowTitle("2048 Game")
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Build UI sections
        self._build_header(main_layout)
        self._build_controls(main_layout)
        self._build_game_board(main_layout)
        self._build_footer(main_layout)

        # Apply styles
        self.setStyleSheet(f"QMainWindow {{ background-color: {self.BG_COLOR}; }}")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _build_header(self, layout: QVBoxLayout) -> None:
        """Build header section with title."""
        title_label = QLabel("2048")
        title_label.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {self.TEXT_COLOR};")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

    def _build_controls(self, layout: QVBoxLayout) -> None:
        """Build controls section with score and buttons."""
        controls_layout = QHBoxLayout()

        # Score display
        self.score_label = QLabel(f"Score: {self.game.get_score()}")
        self.score_label.setFont(QFont("Arial", 16))
        self.score_label.setStyleSheet(f"color: {self.TEXT_COLOR};")

        # Best score display
        self.best_score_label = QLabel("Best: 0")
        self.best_score_label.setFont(QFont("Arial", 16))
        self.best_score_label.setStyleSheet(f"color: {self.TEXT_COLOR};")

        # New game button
        self.new_game_button = QPushButton("New Game")
        self.new_game_button.setFont(QFont("Arial", 12))
        self.new_game_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.BUTTON_BG};
                color: #f9f6f2;
                border: none;
                border-radius: 3px;
                padding: 10px 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.BUTTON_HOVER};
            }}
        """)

        controls_layout.addWidget(self.score_label)
        controls_layout.addWidget(self.best_score_label)
        controls_layout.addStretch()
        controls_layout.addWidget(self.new_game_button)
        layout.addLayout(controls_layout)

    def _build_game_board(self, layout: QVBoxLayout) -> None:
        """Build game board section."""
        self.game_board = GameBoardWidget(self.game)
        layout.addWidget(self.game_board, alignment=Qt.AlignmentFlag.AlignCenter)

    def _build_footer(self, layout: QVBoxLayout) -> None:
        """Build footer section with instructions."""
        instructions = QLabel("Use arrow keys to play")
        instructions.setFont(QFont("Arial", 11))
        instructions.setStyleSheet(f"color: {self.TEXT_COLOR};")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)

    def _setup_connections(self) -> None:
        """Setup signal connections for UI elements."""
        self.new_game_button.clicked.connect(self._start_new_game)

    def _setup_shortcuts(self) -> None:
        """Setup keyboard shortcuts."""
        self._best_score: int = 0

    def _start_new_game(self) -> None:
        """Start a new game and reset the display."""
        self._update_best_score()
        self.game.reset()
        self.game_board.reset_board()
        self._update_display()

    def _update_best_score(self) -> None:
        """Update best score if current score is higher."""
        current_score = self.game.get_score()
        if current_score > self._best_score:
            self._best_score = current_score
            self.best_score_label.setText(f"Best: {self._best_score}")

    def _update_display(self, animate: bool = False) -> None:
        """
        Update the display to reflect current game state.

        Args:
            animate: Whether to animate tile changes
        """
        self.score_label.setText(f"Score: {self.game.get_score()}")
        self.game_board.update_board(animate=animate)

        # Check game end conditions
        if self.game.won:
            self._show_win_message()
        elif self.game.game_over:
            self._show_game_over_message()

    def _show_win_message(self) -> None:
        """Display win message."""
        QTimer.singleShot(
            300,
            lambda: QMessageBox.information(
                self,
                "Congratulations!",
                "You reached 2048! You won!\n\n"
                "Continue playing to reach higher tiles!"
            )
        )

    def _show_game_over_message(self) -> None:
        """Display game over message with restart option."""
        self._update_best_score()

        reply = QMessageBox.question(
            self,
            "Game Over",
            f"Game Over! Final Score: {self.game.get_score()}\n\n"
            f"Best Score: {self._best_score}\n\n"
            "Would you like to play again?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self._start_new_game()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handle keyboard input for game controls.

        Args:
            event: Key press event
        """
        key = event.key()

        # Movement keys
        direction_map: Dict[int, str] = {
            Qt.Key_Left: "left",
            Qt.Key_Right: "right",
            Qt.Key_Up: "up",
            Qt.Key_Down: "down",
        }

        if key in direction_map:
            direction = direction_map[key]
            moved = self.game.move(direction)
            if moved:
                self._update_display(animate=True)
            event.accept()
            return

        # Shortcut keys
        if key in (Qt.Key_N, Qt.Key_R):
            self._start_new_game()
            event.accept()
            return

        # Let parent handle other keys
        super().keyPressEvent(event)

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        self._update_best_score()
        event.accept()
