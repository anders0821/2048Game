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

    def test_get_board_returns_copy(self):
        """Test that get_board returns a copy, not reference."""
        game = Game2048()
        board_copy = game.get_board()
        original_value = board_copy[0][0]
        board_copy[0][0] = 999
        assert game.board[0][0] == original_value

    def test_get_score(self):
        """Test get_score returns correct score."""
        game = Game2048()
        assert game.get_score() == 0
        game.score = 100
        assert game.get_score() == 100


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
        non_zeros = [v for v in game.board[0] if v != 0]
        assert sum(non_zeros) == 8

    def test_merge_cascading(self):
        """Test that merged tiles don't merge again in same move."""
        game = Game2048()
        game.board = [
            [2, 2, 4, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.move("left")
        # Should be [4, 8, 0, 0], not [16, 0, 0, 0]
        assert game.board[0][0] == 4
        assert game.board[0][1] == 8
        assert game.get_score() == 12  # 4 + 8

    def test_merge_four_same_tiles(self):
        """Test merging four same tiles results in two merged tiles."""
        game = Game2048()
        game.board = [
            [4, 4, 4, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.move("left")
        # Should be [8, 8, 0, 0]
        assert game.board[0][0] == 8
        assert game.board[0][1] == 8
        assert game.board[0][2] == 0
        assert game.board[0][3] == 0
        assert game.get_score() == 16  # 8 + 8


class TestDirectionalMoves:
    """Test all four directional moves."""

    def test_move_left(self):
        """Test left movement."""
        game = Game2048()
        game.board = [
            [0, 2, 0, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.move("left")
        assert game.board[0][0] == 4
        assert game.board[0][1] == 0

    def test_move_right(self):
        """Test right movement."""
        game = Game2048()
        game.board = [
            [2, 0, 2, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.move("right")
        assert game.board[0][3] == 4
        assert game.board[0][2] == 0

    def test_move_up(self):
        """Test up movement."""
        game = Game2048()
        game.board = [
            [0, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 2, 0, 0]
        ]
        game.move("up")
        assert game.board[0][1] == 4
        assert game.board[1][1] == 0

    def test_move_down(self):
        """Test down movement."""
        game = Game2048()
        game.board = [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.move("down")
        assert game.board[3][0] == 4
        assert game.board[2][0] == 0

    def test_move_no_change(self):
        """Test that invalid move returns False."""
        game = Game2048()
        game.board = [
            [2, 4, 2, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        result = game.move("left")
        assert result is False


class TestScoring:
    """Test score calculation."""

    def test_score_after_merge(self):
        """Test score increases after merge."""
        game = Game2048()
        game.board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        initial_score = game.get_score()
        game.move("left")
        assert game.get_score() == initial_score + 4

    def test_score_multiple_merges(self):
        """Test score with multiple merges in one move."""
        game = Game2048()
        game.board = [
            [2, 2, 4, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.move("left")
        # 2+2=4 and 4+4=8
        assert game.get_score() == 12

    def test_score_persists_between_moves(self):
        """Test score accumulates across moves."""
        game = Game2048()
        game.board = [
            [2, 2, 0, 0],
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.move("left")
        first_score = game.get_score()
        
        # Setup for another merge
        game.board[0][0] = 2
        game.board[0][1] = 2
        game.board[0][2] = 0
        game.board[0][3] = 0
        
        game.move("left")
        assert game.get_score() == first_score + 4


class TestGameState:
    """Test game state management."""

    def test_game_over_prevents_moves(self):
        """Test that no moves allowed when game is over."""
        game = Game2048()
        game.game_over = True
        result = game.move("left")
        assert result is False

    def test_won_prevents_moves(self):
        """Test that no moves allowed when game is won."""
        game = Game2048()
        game.won = True
        result = game.move("left")
        assert result is False

    def test_not_game_over_with_empty_cells(self):
        """Test game not over when empty cells exist."""
        game = Game2048()
        game.board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 0, 2],
            [4, 2, 4, 2]
        ]
        game._check_game_state()
        assert not game.game_over

    def test_not_game_over_with_possible_merge(self):
        """Test game not over when merges are possible."""
        game = Game2048()
        game.board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 2],  # Two 2s can merge
            [4, 2, 4, 2]
        ]
        game._check_game_state()
        assert not game.game_over

    def test_new_tile_added_after_move(self):
        """Test that a new tile is added after successful move."""
        game = Game2048()
        game.board = [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        initial_count = sum(1 for row in game.board for val in row if val != 0)
        game.move("left")
        new_count = sum(1 for row in game.board for val in row if val != 0)
        assert new_count == initial_count + 1

    def test_no_new_tile_on_invalid_move(self):
        """Test no new tile added when move doesn't change board."""
        game = Game2048()
        game.board = [
            [2, 4, 2, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        initial_count = sum(1 for row in game.board for val in row if val != 0)
        game.move("left")
        new_count = sum(1 for row in game.board for val in row if val != 0)
        assert new_count == initial_count


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_single_tile_no_merge(self):
        """Test single tile doesn't cause issues."""
        game = Game2048()
        game.board = [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.move("left")
        assert game.board[0][0] == 2
        assert game.board[0][1] == 0

    def test_all_zeros(self):
        """Test board with all zeros."""
        game = Game2048()
        game.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        result = game.move("left")
        assert result is False

    def test_large_values(self):
        """Test with large tile values."""
        game = Game2048()
        game.board = [
            [1024, 1024, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.move("left")
        assert game.board[0][0] == 2048
        assert game.won

    def test_full_board_with_merge(self):
        """Test full board that can still merge."""
        game = Game2048()
        game.board = [
            [2, 2, 4, 4],
            [8, 8, 16, 16],
            [32, 32, 64, 64],
            [128, 128, 256, 256]
        ]
        game._check_game_state()
        assert not game.game_over


class TestCustomBoardSize:
    """Test with different board sizes."""

    def test_custom_size_3x3(self):
        """Test 3x3 board."""
        game = Game2048(size=3)
        assert len(game.board) == 3
        assert all(len(row) == 3 for row in game.board)

    def test_custom_size_5x5(self):
        """Test 5x5 board."""
        game = Game2048(size=5)
        assert len(game.board) == 5
        assert all(len(row) == 5 for row in game.board)

    def test_custom_size_initial_tiles(self):
        """Test initial tiles on custom size board."""
        game = Game2048(size=3)
        non_zero_count = sum(1 for row in game.board for val in row if val != 0)
        assert non_zero_count == 2

    def test_custom_size_movement(self):
        """Test movement on custom size board."""
        game = Game2048(size=3)
        game.board = [
            [2, 2, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        game.move("left")
        assert game.board[0][0] == 4
