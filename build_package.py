# PyInstaller 打包配置
# 安装依赖
pip install pyinstaller

# 打包命令
pyinstaller --name="2048Game" --windowed --onefile --clean --paths=src --distpath=. src/main.py

# 详细选项说明：
# --name="2048Game"           # 生成的可执行文件名
# --windowed                  # 无控制台窗口（GUI应用）
# --onefile                   # 打包为单个可执行文件
# --clean                     # 清理临时文件
# --add-data="src"            # 可选：包含源码
# --icon=icon.ico             # 可选：指定图标

# 开发模式打包（更快，包含调试信息）
# pyinstaller --name="2048Game_Dev" --windowed --onedir --debug=all src/main.py