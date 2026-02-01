"""自动化打包脚本"""
import os
import sys
import subprocess
import shutil
from pathlib import Path


def install_pyinstaller():
    """安装 PyInstaller"""
    print("📦 检查并安装 PyInstaller...")
    try:
        import PyInstaller
        print("✅ PyInstaller 已安装")
        return True
    except ImportError:
        print("📥 安装 PyInstaller...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "pyinstaller"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ PyInstaller 安装成功")
            return True
        else:
            print(f"❌ PyInstaller 安装失败: {result.stderr}")
            return False


def build_package():
    """构建可执行文件"""
    print("\n🔨 开始打包 2048 游戏...")
    
    # 确保在项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=2048Game",
        "--windowed",
        "--onefile",
        "--clean",
        "--add-data=src;src",
        "src/main.py"
    ]
    
    print(f"🚀 执行命令: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 打包成功！")
        return True
    else:
        print("❌ 打包失败！")
        print("错误信息:")
        print(result.stderr)
        print("输出信息:")
        print(result.stdout)
        return False


def find_executable():
    """查找生成的可执行文件"""
    dist_dir = Path("dist")
    if dist_dir.exists():
        exe_files = list(dist_dir.glob("*.exe"))
        if exe_files:
            return exe_files[0]
    
    # 检查 build 目录
    build_dir = Path("dist")
    if build_dir.exists():
        for item in build_dir.iterdir():
            if item.is_file() and item.suffix == '.exe':
                return item
    
    return None


def create_portable_package():
    """创建便携版本包"""
    print("\n📦 创建便携版本...")
    
    exe_file = find_executable()
    if not exe_file:
        print("❌ 找不到可执行文件")
        return False
    
    # 创建发布目录
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    # 复制可执行文件
    release_exe = release_dir / "2048Game.exe"
    shutil.copy2(exe_file, release_exe)
    
    # 创建说明文件
    readme_content = """# 2048 游戏

## 运行方法
双击 `2048Game.exe` 即可开始游戏。

## 游戏控制
- 使用方向键 (↑↓←→) 控制数字块移动
- 点击 "New Game" 按钮开始新游戏
- 目标是合并相同数字达到 2048

## 系统要求
- Windows 64位系统
- 无需额外安装 Python 或依赖

祝游戏愉快！
"""
    
    (release_dir / "README.txt").write_text(readme_content, encoding='utf-8')
    
    print(f"✅ 便携版本已创建: {release_dir.absolute()}")
    return True


def clean_build_files():
    """清理构建文件"""
    print("\n🧹 清理构建文件...")
    
    dirs_to_clean = ["build", "dist", "2048Game.spec"]
    for item in dirs_to_clean:
        path = Path(item)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
                print(f"🗑️  删除目录: {item}")
            else:
                path.unlink()
                print(f"🗑️  删除文件: {item}")


def main():
    """主函数"""
    print("=" * 60)
    print("🎮 2048 游戏 - 自动化打包工具")
    print("=" * 60)
    
    # 检查 Python 版本
    python_version = sys.version_info
    print(f"Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 安装 PyInstaller
    if not install_pyinstaller():
        print("❌ 无法安装 PyInstaller，打包终止")
        return 1
    
    # 清理旧的构建文件
    clean_build_files()
    
    # 打包应用
    if not build_package():
        print("❌ 打包失败")
        return 1
    
    # 创建便携版本
    if not create_portable_package():
        print("❌ 创建便携版本失败")
        return 1
    
    # 显示结果
    exe_file = find_executable()
    if exe_file:
        exe_size = exe_file.stat().st_size / (1024 * 1024)  # MB
        print(f"\n📊 打包完成:")
        print(f"   📁 可执行文件: {exe_file}")
        print(f"   📏 文件大小: {exe_size:.1f} MB")
        print(f"   📂 便携版本: {Path('release').absolute()}")
    
    print("\n🎉 打包完成！现在可以分发游戏了。")
    return 0


if __name__ == "__main__":
    sys.exit(main())