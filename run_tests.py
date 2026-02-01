"""自动化冒烟测试 - 运行命令脚本"""
import subprocess
import sys
import os


def run_smoke_test():
    """运行冒烟测试"""
    print("🚀 启动 2048 游戏冒烟测试...")
    
    try:
        # 检查 Python 环境
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"Python 版本: {result.stdout.strip()}")
        
        # 检查 PySide6 安装
        try:
            import PySide6
            print(f"PySide6 版本: {PySide6.__version__}")
        except ImportError:
            print("❌ PySide6 未安装，请先运行: pip install PySide6")
            return False
        
        # 运行冒烟测试
        print("\n开始执行冒烟测试...\n")
        result = subprocess.run([sys.executable, "smoke_test.py"], 
                              cwd=os.getcwd())
        
        if result.returncode == 0:
            print("\n✅ 冒烟测试执行成功")
            return True
        else:
            print(f"\n❌ 冒烟测试执行失败，返回码: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ 运行冒烟测试时出错: {e}")
        return False


def run_unit_tests():
    """运行单元测试"""
    print("\n🧪 运行单元测试...")
    
    try:
        # 运行 pytest
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", 
            "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"运行单元测试时出错: {e}")
        return False


def run_code_quality_checks():
    """运行代码质量检查"""
    print("\n🔍 运行代码质量检查...")
    
    checks = {
        "black": ["black", "--check", "src/"],
        "mypy": ["mypy", "src/"],
        "flake8": ["flake8", "src/"]
    }
    
    all_passed = True
    
    for check_name, cmd in checks.items():
        try:
            print(f"运行 {check_name}...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {check_name} 检查通过")
            else:
                print(f"❌ {check_name} 检查失败:")
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                all_passed = False
                
        except FileNotFoundError:
            print(f"⚠️  {check_name} 未安装，跳过检查")
        except Exception as e:
            print(f"运行 {check_name} 时出错: {e}")
            all_passed = False
    
    return all_passed


def main():
    """主函数"""
    print("=" * 60)
    print("🎮 2048 游戏 - 自动化测试套件")
    print("=" * 60)
    
    # 1. 冒烟测试
    smoke_passed = run_smoke_test()
    
    # 2. 单元测试
    unit_passed = run_unit_tests()
    
    # 3. 代码质量检查
    quality_passed = run_code_quality_checks()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结:")
    print(f"冒烟测试: {'✅ 通过' if smoke_passed else '❌ 失败'}")
    print(f"单元测试: {'✅ 通过' if unit_passed else '❌ 失败'}")
    print(f"代码质量: {'✅ 通过' if quality_passed else '❌ 失败'}")
    
    if smoke_passed and unit_passed and quality_passed:
        print("\n🎉 所有测试通过！游戏已准备就绪。")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查相关问题。")
        return 1


if __name__ == "__main__":
    sys.exit(main())