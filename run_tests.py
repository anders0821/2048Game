"""Automated test runner script."""
import subprocess
import sys


def run_unit_tests():
    """Run unit tests."""
    print("\n>> Running unit tests...")
    
    try:
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
    """Run code quality checks."""
    print("\n>> Running code quality checks...")
    
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
                print(f"[PASS] {check_name} check passed")
            else:
                print(f"[FAIL] {check_name} check failed:")
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
                all_passed = False
                
        except FileNotFoundError:
            print(f"[WARN] {check_name} not installed, skipping check")
        except Exception as e:
            print(f"Error running {check_name}: {e}")
            all_passed = False
    
    return all_passed


def main():
    """Main function"""
    print("=" * 60)
    print("2048 Game - Automated Test Suite")
    print("=" * 60)
    
    # 1. Unit tests
    unit_passed = run_unit_tests()
    
    # 2. Code quality checks
    quality_passed = run_code_quality_checks()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"Unit tests: {'[PASS]' if unit_passed else '[FAIL]'}")
    print(f"Code quality: {'[PASS]' if quality_passed else '[FAIL]'}")
    
    if unit_passed and quality_passed:
        print("\nAll tests passed! Game is ready.")
        return 0
    else:
        print("\nSome tests failed, please check related issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
