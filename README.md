# 2048 Game

一个使用 PySide6 实现的 2048 益智游戏，具有流畅的动画效果。

![2048 Game](https://img.shields.io/badge/Version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.12+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 特性

- 🎮 经典的 2048 游戏规则
- 🎨 美观的界面设计和配色
- ✨ 流畅的动画效果：
  - 数字块移动动画
  - 合并时的缩放动画
  - 新块出现动画
- ⌨️ 键盘方向键控制
- 📊 实时分数显示
- 🏆 游戏胜利/失败检测
- 🔄 新游戏按钮

## 安装

### 环境要求

- Python 3.12+
- PySide6

### 安装步骤

1. 克隆或下载项目
2. 安装依赖：

```bash
# 安装应用依赖
pip install -r requirements-dev.txt

# 或者直接安装 PySide6
pip install PySide6>=6.0.0
```

## 使用方法

### 直接运行

```bash
# 在 PyCharm 中直接运行
python src/main.py

# 或者在命令行中运行
python src/main.py
```

### 作为包运行

```bash
# 安装为开发包
pip install -e .

# 运行
python -m src.main
```

### 打包为可执行文件

```bash
# 自动化打包（推荐）
python package_game.py

# 或使用 PyInstaller 直接打包
pyinstaller 2048Game.spec

# 简单打包
pyinstaller --name="2048Game" --windowed --onefile src/main.py
```

打包完成后，可执行文件位于：
- `dist/2048Game.exe` - 单独的可执行文件
- `release/` - 包含说明文档的便携版本

### 游戏控制

- **方向键** (↑ ↓ ← →): 移动数字块
- **New Game 按钮**: 开始新游戏
- **目标**: 通过相同数字合并达到 2048

## 项目结构

```
project/
├── src/
│   ├── __init__.py          # 包初始化
│   ├── main.py             # 主程序入口
│   ├── main_window.py      # 主窗口和UI组件
│   └── game2048.py         # 游戏逻辑实现
├── tests/                  # 测试文件
├── setup.py               # 安装配置
├── pyproject.toml         # 项目配置
├── requirements-dev.txt   # 依赖列表
└── README.md             # 项目文档
```

## 开发

### 开发环境设置

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 代码格式化
black src/

# 类型检查
mypy src/

# 运行测试
pytest tests/
```

### 代码质量工具

- **Black**: 代码格式化
- **MyPy**: 静态类型检查
- **Flake8**: 代码风格检查
- **iSort**: 导入排序

## 游戏规则

1. 使用方向键移动所有数字块
2. 相同数字的块碰撞时会合并成一个
3. 每次移动后会随机出现一个新的 2 或 4
4. 当达到 2048 时获胜
5. 当无法移动时游戏结束

## 技术实现

### 核心组件

- **Game2048**: 游戏逻辑核心，处理移动、合并、状态检测
- **MainWindow**: 主窗口，包含UI布局和事件处理
- **TileWidget**: 数字块组件，支持动画效果
- **GameBoardWidget**: 游戏板组件，管理所有数字块

### 动画系统

- **位置动画**: 使用 `QPropertyAnimation` 实现平滑移动
- **缩放动画**: 合并和新出现时的弹性效果
- **动画队列**: 确保动画顺序执行，避免视觉混乱

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件