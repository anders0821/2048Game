"""Smoke test script - Verify 2048 game basic functionality"""
import sys
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt

# Add src directory to path
sys.path.insert(0, 'src')

from main_window import MainWindow
from game2048 import Game2048


class SmokeTest:
    """2048 game smoke test"""
    
    def __init__(self):
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)
        
        self.window = MainWindow()
        self.window.show()
        
        self.test_results = []
        self.current_test = 0
        
        print("🧪 Starting smoke test...")
    
    def test_initial_state(self):
        """Test initial state"""
        try:
            # Verify board initialization
            board = self.window.game.get_board()
            assert len(board) == 4, "Board size should be 4x4"
            assert len(board[0]) == 4, "Board size should be 4x4"
            
            # Verify initial two non-zero tiles
            non_zero_count = sum(1 for row in board for val in row if val != 0)
            assert non_zero_count == 2, f"Should have 2 non-zero tiles initially, found {non_zero_count}"
            
            # Verify initial score is 0
            assert self.window.game.get_score() == 0, "Initial score should be 0"
            
            print("✅ Initial state test passed")
            self.test_results.append(("Initial State", True))
            return True
        except Exception as e:
            print(f"❌ Initial state test failed: {e}")
            self.test_results.append(("Initial State", False))
            return False
    
    def test_game_logic(self):
        """Test game logic"""
        try:
            # Create independent game instance for testing
            game = Game2048()
            
            # Test movement
            initial_board = [row[:] for row in game.get_board()]
            moved = game.move("left")
            
            if moved:
                # Verify board state changed after move
                assert game.get_board() != initial_board, "Board state should change after move"
            
            # Test reset
            game.reset()
            assert game.get_score() == 0, "Score should be 0 after reset"
            assert not game.game_over, "Game should not be over after reset"
            assert not game.won, "Should not be won after reset"
            
            print("✅ Game logic test passed")
            self.test_results.append(("Game Logic", True))
            return True
        except Exception as e:
            print(f"❌ Game logic test failed: {e}")
            self.test_results.append(("Game Logic", False))
            return False
    
    def test_keyboard_input(self):
        """Test keyboard input"""
        try:
            # Test arrow keys
            QTest.keyClick(self.window, Qt.Key.Key_Left)
            QTest.keyClick(self.window, Qt.Key.Key_Right)
            QTest.keyClick(self.window, Qt.Key.Key_Up)
            QTest.keyClick(self.window, Qt.Key.Key_Down)
            
            # Test new game button
            self.window.new_game_button.click()
            
            print("✅ Keyboard input test passed")
            self.test_results.append(("Keyboard Input", True))
            return True
        except Exception as e:
            print(f"❌ Keyboard input test failed: {e}")
            self.test_results.append(("Keyboard Input", False))
            return False
    
    def test_ui_components(self):
        """Test UI components"""
        try:
            # Verify main UI components exist
            assert self.window.score_label is not None, "Score label does not exist"
            assert self.window.new_game_button is not None, "New game button does not exist"
            assert self.window.game_board is not None, "Game board does not exist"
            
            # Verify game board has correct child components
            assert len(self.window.game_board.tiles) == 4, "Game board should have 4 rows"
            assert len(self.window.game_board.tiles[0]) == 4, "Game board should have 4 columns"
            
            print("✅ UI components test passed")
            self.test_results.append(("UI Components", True))
            return True
        except Exception as e:
            print(f"❌ UI components test failed: {e}")
            self.test_results.append(("UI Components", False))
            return False
    
    def test_animation_system(self):
        """Test animation system"""
        try:
            # Verify animation objects exist
            first_tile = self.window.game_board.tiles[0][0]
            assert hasattr(first_tile, 'pos_animation'), "Position animation does not exist"
            assert hasattr(first_tile, 'scale_animation'), "Scale animation does not exist"
            
            # Test animation methods exist
            assert hasattr(first_tile, 'animate_move_to'), "Move animation method does not exist"
            assert hasattr(first_tile, 'animate_appearance'), "Appearance animation method does not exist"
            
            print("✅ Animation system test passed")
            self.test_results.append(("Animation System", True))
            return True
        except Exception as e:
            print(f"❌ Animation system test failed: {e}")
            self.test_results.append(("Animation System", False))
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        tests = [
            self.test_initial_state,
            self.test_game_logic,
            self.test_keyboard_input,
            self.test_ui_components,
            self.test_animation_system
        ]
        
        for test_func in tests:
            try:
                test_func()
                time.sleep(0.5)  # Test interval
            except Exception as e:
                print(f"Test execution error: {e}")
        
        self.print_results()
    
    def print_results(self):
        """Print test results"""
        print("\n📊 Smoke Test Results:")
        print("=" * 50)
        
        passed = 0
        total = len(self.test_results)
        
        for test_name, result in self.test_results:
            status = "✅ Passed" if result else "❌ Failed"
            print(f"{test_name:12} : {status}")
            if result:
                passed += 1
        
        print("=" * 50)
        print(f"Total: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All smoke tests passed! Game is working properly.")
            return True
        else:
            print("⚠️  Some tests failed, please check related functionality.")
            return False
    
    def close(self):
        """Close test"""
        if self.window:
            self.window.close()


def main():
    """Main function"""
    test = SmokeTest()
    
    # Delay test execution to ensure UI fully loads
    QTimer.singleShot(1000, test.run_all_tests)
    
    # Delay close
    
    sys.exit(test.app.exec())


if __name__ == "__main__":
    main()