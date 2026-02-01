"""Main entry point for the 2048 game."""
from common import *
from main_window import MainWindow


def main() -> None:
    """Main entry point for the 2048 game application."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.activateWindow()
    window.raise_()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
