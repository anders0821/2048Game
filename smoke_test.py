"""冒烟测试脚本 - 验证 2048 游戏基本功能"""
import sys
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt

# 添加 src 目录到路径
sys.path.insert(0, 'src')

from main_window import MainWindow
from game2048 import Game2048


class SmokeTest:
    """2048 游戏冒烟测试"""
    
    def __init__(self):
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)
        
        self.window = MainWindow()
        self.window.show()
        
        self.test_results = []
        self.current_test = 0
        
        print("🧪 开始冒烟测试...")
    
    def test_initial_state(self):
        """测试初始状态"""
        try:
            # 验证游戏板初始化
            board = self.window.game.get_board()
            assert len(board) == 4, "游戏板大小应为4x4"
            assert len(board[0]) == 4, "游戏板大小应为4x4"
            
            # 验证初始有两个非零块
            non_zero_count = sum(1 for row in board for val in row if val != 0)
            assert non_zero_count == 2, f"初始应有2个非零块，实际有{non_zero_count}个"
            
            # 验证分数初始为0
            assert self.window.game.get_score() == 0, "初始分数应为0"
            
            print("✅ 初始状态测试通过")
            self.test_results.append(("初始状态", True))
            return True
        except Exception as e:
            print(f"❌ 初始状态测试失败: {e}")
            self.test_results.append(("初始状态", False))
            return False
    
    def test_game_logic(self):
        """测试游戏逻辑"""
        try:
            # 创建独立游戏实例测试
            game = Game2048()
            
            # 测试移动
            initial_board = [row[:] for row in game.get_board()]
            moved = game.move("left")
            
            if moved:
                # 验证移动后板状态改变
                assert game.get_board() != initial_board, "移动后游戏板状态应改变"
            
            # 测试重置
            game.reset()
            assert game.get_score() == 0, "重置后分数应为0"
            assert not game.game_over, "重置后游戏不应结束"
            assert not game.won, "重置后不应获胜"
            
            print("✅ 游戏逻辑测试通过")
            self.test_results.append(("游戏逻辑", True))
            return True
        except Exception as e:
            print(f"❌ 游戏逻辑测试失败: {e}")
            self.test_results.append(("游戏逻辑", False))
            return False
    
    def test_keyboard_input(self):
        """测试键盘输入"""
        try:
            # 测试方向键
            QTest.keyClick(self.window, Qt.Key.Key_Left)
            QTest.keyClick(self.window, Qt.Key.Key_Right)
            QTest.keyClick(self.window, Qt.Key.Key_Up)
            QTest.keyClick(self.window, Qt.Key.Key_Down)
            
            # 测试新游戏按钮
            self.window.new_game_button.click()
            
            print("✅ 键盘输入测试通过")
            self.test_results.append(("键盘输入", True))
            return True
        except Exception as e:
            print(f"❌ 键盘输入测试失败: {e}")
            self.test_results.append(("键盘输入", False))
            return False
    
    def test_ui_components(self):
        """测试UI组件"""
        try:
            # 验证主要UI组件存在
            assert self.window.score_label is not None, "分数标签不存在"
            assert self.window.new_game_button is not None, "新游戏按钮不存在"
            assert self.window.game_board is not None, "游戏板不存在"
            
            # 验证游戏板有正确的子组件
            assert len(self.window.game_board.tiles) == 4, "游戏板应有4行"
            assert len(self.window.game_board.tiles[0]) == 4, "游戏板应有4列"
            
            print("✅ UI组件测试通过")
            self.test_results.append(("UI组件", True))
            return True
        except Exception as e:
            print(f"❌ UI组件测试失败: {e}")
            self.test_results.append(("UI组件", False))
            return False
    
    def test_animation_system(self):
        """测试动画系统"""
        try:
            # 验证动画对象存在
            first_tile = self.window.game_board.tiles[0][0]
            assert hasattr(first_tile, 'pos_animation'), "位置动画不存在"
            assert hasattr(first_tile, 'scale_animation'), "缩放动画不存在"
            
            # 测试动画方法存在
            assert hasattr(first_tile, 'animate_move_to'), "移动动画方法不存在"
            assert hasattr(first_tile, 'animate_appearance'), "出现动画方法不存在"
            
            print("✅ 动画系统测试通过")
            self.test_results.append(("动画系统", True))
            return True
        except Exception as e:
            print(f"❌ 动画系统测试失败: {e}")
            self.test_results.append(("动画系统", False))
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
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
                time.sleep(0.5)  # 测试间隔
            except Exception as e:
                print(f"测试执行错误: {e}")
        
        self.print_results()
    
    def print_results(self):
        """打印测试结果"""
        print("\n📊 冒烟测试结果:")
        print("=" * 50)
        
        passed = 0
        total = len(self.test_results)
        
        for test_name, result in self.test_results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{test_name:12} : {status}")
            if result:
                passed += 1
        
        print("=" * 50)
        print(f"总计: {passed}/{total} 测试通过")
        
        if passed == total:
            print("🎉 所有冒烟测试通过！游戏可以正常使用。")
            return True
        else:
            print("⚠️  部分测试失败，请检查相关功能。")
            return False
    
    def close(self):
        """关闭测试"""
        if self.window:
            self.window.close()


def main():
    """主函数"""
    test = SmokeTest()
    
    # 延迟执行测试，确保UI完全加载
    QTimer.singleShot(1000, test.run_all_tests)
    
    # 延迟关闭
    QTimer.singleShot(5000, test.close)
    
    sys.exit(test.app.exec())


if __name__ == "__main__":
    main()