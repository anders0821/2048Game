# PyInstaller packaging configuration
# Install dependencies
pip install pyinstaller

# Packaging command
pyinstaller --name="2048Game" --windowed --onefile --clean --paths=src --distpath=. src/main.py

# Detailed option descriptions:
# --name="2048Game"           # Generated executable filename
# --windowed                  # No console window (GUI application)
# --onefile                   # Package as single executable
# --clean                     # Clean temporary files
# --add-data="src"            # Optional: include source code
# --icon=icon.ico             # Optional: specify icon

# Development mode packaging (faster, includes debug info)
# pyinstaller --name="2048Game_Dev" --windowed --onedir --debug=all src/main.py