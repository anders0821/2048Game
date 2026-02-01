# 🎮 2048 Game

一个使用 PySide6 实现的 2048 益智游戏，具有流畅的动画效果和精美的界面设计。

![2048 Game](https://img.shields.io/badge/Version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.12+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.0+-blue.svg)

## ✨ 特性

### 🎮 游戏功能
- 经典的 2048 游戏规则
- 键盘方向键控制（↑↓←→）
- 实时分数统计
- 游戏胜利/失败检测
- 新游戏重置功能

### 🎨 视觉效果
- 精美的界面设计和配色方案
- 流畅的动画系统：
  - 数字块平滑移动
  - 合并时的多阶段缩放动画
  - 金色高亮和闪光效果
  - 新块弹性出现动画
- 响应式设计和阴影效果

### 🛠️ 技术特性
- 面向对象架构设计
- 完整的动画框架
- 模块化代码结构
- 完善的错误处理

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

## 📁 项目结构

```
2048-game/
├── 📂 src/                    # 源代码目录
│   ├── __init__.py            # 包初始化
│   ├── main.py               # 主程序入口
│   ├── main_window.py        # 主窗口和UI组件
│   └── game2048.py           # 游戏逻辑核心
├── 📂 tests/                  # 测试文件
│   ├── __init__.py
│   └── test_main.py          # 单元测试
├── 📂 release/                # 打包发布目录
├── 🔧 package_game.py         # 自动化打包脚本
├── 🔧 2048Game.spec          # PyInstaller 配置
├── 🧪 smoke_test.py          # 冒烟测试
├── 🧪 run_tests.py           # 测试套件
├── 📄 setup.py              # 安装配置
├── 📄 pyproject.toml         # 项目配置
├── 📄 requirements-dev.txt  # 开发依赖
└── 📖 README.md             # 项目文档
```

## 🛠️ 开发指南

### 环境配置

```bash
# 克隆项目
git clone <repository-url>
cd 2048-game

# 安装开发依赖
pip install -r requirements-dev.txt

# 或手动安装
pip install PySide6>=6.0.0 pytest black mypy flake8 isort
```

### 开发工具

```bash
# 代码格式化
black src/ --line-length 88

# 导入排序
isort src/

# 类型检查
mypy src/ --python-version 3.12

# 代码风格检查
flake8 src/

# 运行测试
pytest tests/ -v

# 完整测试套件
python run_tests.py
```

### 测试

项目包含完整的测试体系：

```bash
# 运行所有测试
python run_tests.py

# 仅冒烟测试
python smoke_test.py

# 仅单元测试
pytest tests/ -v
```

### 代码质量

- ✅ **Black** - 代码格式化
- ✅ **MyPy** - 静态类型检查  
- ✅ **Flake8** - 代码风格检查
- ✅ **iSort** - 导入语句排序
- ✅ **冒烟测试** - 功能验证
- ✅ **单元测试** - 组件测试

## 🎯 游戏规则

### 基本玩法
1. **移动**: 使用方向键 (↑↓←→) 移动所有数字块
2. **合并**: 相同数字的块碰撞时会合并成它们的和
3. **新生**: 每次移动后会随机出现一个新的 2 或 4
4. **胜利**: 当出现 2048 数字块时游戏获胜
5. **失败**: 当棋盘填满且无法移动时游戏结束

### 策略技巧
- 优先保持大数字在角落
- 尽量不要让小数字分隔大数字
- 建立递增的数字序列
- 保持移动的规律性

## 🏗️ 技术架构

### 核心组件

| 组件 | 功能 | 特性 |
|------|------|------|
| **Game2048** | 游戏逻辑核心 | 移动算法、合并检测、状态管理 |
| **MainWindow** | 主窗口控制器 | 事件处理、UI布局、游戏流程 |
| **TileWidget** | 数字块组件 | 动画系统、样式管理、交互反馈 |
| **GameBoardWidget** | 游戏板管理 | 网格布局、动画协调、状态同步 |

### 动画引擎

- **🎬 位置动画**: `QPropertyAnimation` 实现平滑移动
- **🎭 缩放动画**: `QSequentialAnimationGroup` 实现多阶段效果
- **🌈 颜色过渡**: 动态样式变化增强视觉反馈
- **⚡ 性能优化**: 智能动画队列避免重叠和卡顿

### 设计模式

- **MVC架构**: 清晰的模型-视图-控制器分离
- **组件化设计**: 可复用的UI组件
- **事件驱动**: 响应式的用户交互
- **状态管理**: 集中的游戏状态控制

## 📦 分发与部署

### 可执行文件

项目支持多种分发方式：

```bash
# 自动化打包（推荐）
python package_game.py
```

打包特性：
- ✅ 单文件可执行程序 (~15-20MB)
- ✅ 无需 Python 环境
- ✅ 跨 Windows 版本兼容
- ✅ 包含完整依赖库

### 发布版本

打包完成后：
```
📁 dist/
└── 📄 2048Game.exe           # 主可执行文件

📁 release/
├── 📄 2048Game.exe          # 便携版本
└── 📄 README.txt            # 使用说明
```

## 🤝 贡献指南

欢迎贡献代码和改进建议！

### 贡献方式
1. 🐛 **报告问题**: 提交 Issue 描述 bug
2. 💡 **功能建议**: 提出新功能想法
3. 🔧 **代码贡献**: 提交 Pull Request
4. 📖 **文档完善**: 改进文档和说明

### 开发流程
1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范
- 遵循 PEP 8 代码风格
- 使用 Black 格式化代码
- 添加适当的类型注解
- 编写单元测试
- 更新相关文档

## 📄 许可证

本项目采用 MIT License - 详见 [LICENSE](LICENSE) 文件

### 许可证要点
- ✅ 商业使用
- ✅ 修改和分发
- ✅ 私人使用
- ⚠️ 需要包含许可证和版权声明
- ⚠️ 不提供责任担保

---

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

**技术栈**:
- [PySide6](https://doc.qt.io/qtforpython/) - Qt for Python GUI 框架
- [Python](https://www.python.org/) - 编程语言
- [PyInstaller](https://pyinstaller.org/) - 打包工具

**灵感来源**:
- [2048 原版游戏](https://play2048.co/) by Gabriele Cirulli
- PySide6 官方文档和社区

---

<div align="center">

**🎮 享受游戏，享受编程！**

Made with ❤️ by [Your Name]

</div>