import sys
from PySide6.QtWidgets import QApplication

from .main_window import MainWindow


def main() -> None:
    """Main entry point for the 2048 game application."""
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()