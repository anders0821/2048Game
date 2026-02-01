"""Automated packaging script"""
import os
import sys
import subprocess
import shutil
from pathlib import Path


def install_pyinstaller():
    """Install PyInstaller"""
    print("📦 Checking and installing PyInstaller...")
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
        return True
    except ImportError:
        print("📥 Installing PyInstaller...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "pyinstaller"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ PyInstaller installed successfully")
            return True
        else:
            print(f"❌ PyInstaller installation failed: {result.stderr}")
            return False


def build_package():
    """Build executable file"""
    print("\n🔨 Starting to package 2048 game...")
    
    # Ensure in project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Packaging command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--distpath=.",
        "2048Game.spec"
    ]
    
    print(f"🚀 Executing command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Packaging successful!")
        return True
    else:
        print("❌ Packaging failed!")
        print("Error message:")
        print(result.stderr)
        print("Output message:")
        print(result.stdout)
        return False


def find_executable():
    """Find generated executable file"""
    dist_dir = Path("dist")
    if dist_dir.exists():
        exe_files = list(dist_dir.glob("*.exe"))
        if exe_files:
            return exe_files[0]
    
    # Check build directory
    build_dir = Path("dist")
    if build_dir.exists():
        for item in build_dir.iterdir():
            if item.is_file() and item.suffix == '.exe':
                return item
    
    return None


def create_portable_package():
    """Create portable version package"""
    print("\n📦 Creating portable version...")
    
    exe_file = find_executable()
    if not exe_file:
        print("❌ Cannot find executable file")
        return False
    
    # Create release directory
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    # Copy executable file
    release_exe = release_dir / "2048Game.exe"
    shutil.copy2(exe_file, release_exe)
    
    # Create README file
    readme_content = """# 2048 Game

## How to Run
Double-click `2048Game.exe` to start the game.

## Game Controls
- Use arrow keys (↑↓←→) to move the number tiles
- Click "New Game" button to start a new game
- Goal is to merge identical numbers to reach 2048

## System Requirements
- Windows 64-bit system
- No need to install Python or additional dependencies

Enjoy the game!
"""
    
    (release_dir / "README.txt").write_text(readme_content, encoding='utf-8')
    
    print(f"✅ Portable version created: {release_dir.absolute()}")
    return True


def clean_build_files():
    """Clean build files"""
    print("\n🧹 Cleaning build files...")
    
    dirs_to_clean = ["build", "dist"]
    for item in dirs_to_clean:
        path = Path(item)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
                print(f"🗑️  Deleted directory: {item}")
            else:
                path.unlink()
                print(f"🗑️  Deleted file: {item}")


def main():
    """Main function"""
    print("=" * 60)
    print("🎮 2048 Game - Automated Packaging Tool")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Install PyInstaller
    if not install_pyinstaller():
        print("❌ Cannot install PyInstaller, packaging aborted")
        return 1
    
    # Clean old build files
    clean_build_files()
    
    # Package application
    if not build_package():
        print("❌ Packaging failed")
        return 1
    
    # Display results
    exe_file = Path("2048Game.exe")
    if exe_file.exists():
        exe_size = exe_file.stat().st_size / (1024 * 1024)  # MB
        print(f"\n📊 Packaging completed:")
        print(f"   📁 Executable file: {exe_file.absolute()}")
        print(f"   📏 File size: {exe_size:.1f} MB")
    
    print("\n🎉 Packaging completed! The game is ready for distribution.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
