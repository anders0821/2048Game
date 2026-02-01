"""Automated smoke test - command runner script"""
import subprocess
import sys
import os


def run_smoke_test():
    """Run smoke test"""
    print("🚀 Starting 2048 game smoke test...")
    
    try:
        # Check Python environment
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"Python version: {result.stdout.strip()}")
        
        # Check PySide6 installation
        try:
            import PySide6
            print(f"PySide6 version: {PySide6.__version__}")
        except ImportError:
            print("❌ PySide6 not installed, please run: pip install PySide6")
            return False
        
        # Run smoke test
        print("\nStarting smoke test execution...\n")
        result = subprocess.run([sys.executable, "smoke_test.py"], 
                              cwd=os.getcwd())
        
        if result.returncode == 0:
            print("\n✅ Smoke test execution successful")
            return True
        else:
            print(f"\n❌ Smoke test execution failed, return code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running smoke test: {e}")
        return False


def run_unit_tests():
    """Run unit tests"""
    print("\n🧪 Running unit tests...")
    
    try:
        # Run pytest
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", 
            "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Error message:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running unit tests: {e}")
        return False


def run_code_quality_checks():
    """Run code quality checks"""
    print("\n🔍 Running code quality checks...")
    
    checks = {
        "black": ["black", "--check", "src/"],
        "mypy": ["mypy", "src/"],
        "flake8": ["flake8", "src/"]
    }
    
    all_passed = True
    
    for check_name, cmd in checks.items():
        try:
            print(f"Running {check_name}...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {check_name} check passed")
            else:
                print(f"❌ {check_name} check failed:")
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                all_passed = False
                
        except FileNotFoundError:
            print(f"⚠️  {check_name} not installed, skipping check")
        except Exception as e:
            print(f"Error running {check_name}: {e}")
            all_passed = False
    
    return all_passed


def main():
    """Main function"""
    print("=" * 60)
    print("🎮 2048 Game - Automated Test Suite")
    print("=" * 60)
    
    # 1. Smoke test
    smoke_passed = run_smoke_test()
    
    # 2. Unit tests
    unit_passed = run_unit_tests()
    
    # 3. Code quality checks
    quality_passed = run_code_quality_checks()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"Smoke test: {'✅ Passed' if smoke_passed else '❌ Failed'}")
    print(f"Unit tests: {'✅ Passed' if unit_passed else '❌ Failed'}")
    print(f"Code quality: {'✅ Passed' if quality_passed else '❌ Failed'}")
    
    if smoke_passed and unit_passed and quality_passed:
        print("\n🎉 All tests passed! Game is ready.")
        return 0
    else:
        print("\n⚠️  Some tests failed, please check related issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
