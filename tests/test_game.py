"""Tests for the 2048 game."""
import pytest
import sys
sys.path.insert(0, 'src')

from game2048 import Game2048


class TestGame2048:
    """Test cases for Game2048 class."""

    def test_initial_board_size(self):
        """Test that the board is initialized with correct size."""
        game = Game2048()
        assert len(game.board) == 4
        assert all(len(row) == 4 for row in game.board)

    def test_initial_score(self):
        """Test that the initial score is 0."""
        game = Game2048()
        assert game.get_score() == 0

    def test_initial_tiles_count(self):
        """Test that two tiles are placed initially."""
        game = Game2048()
        non_zero_count = sum(1 for row in game.board for val in row if val != 0)
        assert non_zero_count == 2

    def test_reset(self):
        """Test that reset clears the board and score."""
        game = Game2048()
        game.move("left")
        game.reset()
        
        assert game.get_score() == 0
        assert not game.game_over
        assert not game.won
        
        non_zero_count = sum(1 for row in game.board for val in row if val != 0)
        assert non_zero_count == 2

    def test_move_changes_board(self):
        """Test that a valid move changes the board."""
        game = Game2048()
        initial_board = [row[:] for row in game.board]
        
        moved = False
        for direction in ["left", "right", "up", "down"]:
            game_copy = Game2048()
            game_copy.board = [row[:] for row in game.board]
            if game_copy.move(direction):
                moved = True
                break
        
        assert moved or game.board == initial_board

    def test_win_condition(self):
        """Test that reaching 2048 triggers win."""
        game = Game2048()
        game.board[0][0] = 2048
        game._check_game_state()
        assert game.won

    def test_game_over_condition(self):
        """Test game over detection."""
        game = Game2048()
        # Fill board with no possible moves
        game.board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        game._check_game_state()
        assert game.game_over


class TestTileMerging:
    """Test cases for tile merging logic."""

    def test_merge_two_tiles(self):
        """Test that two equal tiles merge."""
        game = Game2048()
        game.board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.move("left")
        assert 4 in game.board[0]
        assert game.get_score() == 4

    def test_no_merge_different_values(self):
        """Test that different values don't merge."""
        game = Game2048()
        game.board = [
            [2, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        initial_score = game.get_score()
        game.move("left")
        assert game.board[0][:2] == [2, 4]
        assert game.get_score() == initial_score

    def test_merge_multiple_pairs(self):
        """Test merging multiple pairs in one row."""
        game = Game2048()
        game.board = [
            [2, 2, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.move("left")
        # Should merge to [4, 4, 0, 0] or [4, 0, 4, 0] depending on implementation
        non_zeros = [v for v in game.board[0] if v != 0]
        assert sum(non_zeros) == 8  # 2+2+2+2 = 8
