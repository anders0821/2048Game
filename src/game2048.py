import random
from typing import List, Tuple, Optional


class Game2048:
    """2048 game logic implementation."""
    
    def __init__(self, size: int = 4):
        self.size = size
        self.board: List[List[int]] = [[0] * size for _ in range(size)]
        self.score: int = 0
        self.game_over: bool = False
        self.won: bool = False
        self.moved: bool = False
        
        # Start with two random tiles
        self._add_random_tile()
        self._add_random_tile()
    
    def _add_random_tile(self) -> None:
        """Add a random tile (2 or 4) to an empty position."""
        empty_cells: List[Tuple[int, int]] = [
            (row, col) for row in range(self.size) 
            for col in range(self.size) if self.board[row][col] == 0
        ]
        
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = 2 if random.random() < 0.9 else 4
    
    def _move_left(self) -> bool:
        """Move and merge tiles to the left."""
        moved = False
        
        for row in range(self.size):
            # Extract non-zero tiles
            tiles = [tile for tile in self.board[row] if tile != 0]
            
            # Merge tiles
            merged_tiles = []
            i = 0
            while i < len(tiles):
                if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                    merged_tiles.append(tiles[i] * 2)
                    self.score += tiles[i] * 2
                    i += 2
                else:
                    merged_tiles.append(tiles[i])
                    i += 1
            
            # Pad with zeros
            new_row = merged_tiles + [0] * (self.size - len(merged_tiles))
            
            # Check if row changed
            if new_row != self.board[row]:
                moved = True
                self.board[row] = new_row
        
        return moved
    
    def _rotate_board(self) -> None:
        """Rotate the board 90 degrees clockwise."""
        self.board = [[self.board[self.size - 1 - row][col] 
                      for row in range(self.size)] 
                     for col in range(self.size)]
    
    def move(self, direction: str) -> bool:
        """Move tiles in the specified direction."""
        if self.game_over or self.won:
            return False
        
        self.moved = False
        
        if direction == "left":
            self.moved = self._move_left()
        elif direction == "right":
            self._rotate_board()
            self._rotate_board()
            self.moved = self._move_left()
            self._rotate_board()
            self._rotate_board()
        elif direction == "up":
            self._rotate_board()
            self._rotate_board()
            self._rotate_board()
            self.moved = self._move_left()
            self._rotate_board()
        elif direction == "down":
            self._rotate_board()
            self.moved = self._move_left()
            self._rotate_board()
            self._rotate_board()
            self._rotate_board()
        
        if self.moved:
            self._add_random_tile()
            self._check_game_state()
        
        return self.moved
    
    def _check_game_state(self) -> None:
        """Check if the game is won or over."""
        # Check for 2048 tile (win)
        for row in self.board:
            if 2048 in row:
                self.won = True
                return
        
        # Check for empty cells
        for row in self.board:
            if 0 in row:
                return
        
        # Check for possible moves
        for row in range(self.size):
            for col in range(self.size):
                current = self.board[row][col]
                # Check right neighbor
                if col < self.size - 1 and current == self.board[row][col + 1]:
                    return
                # Check bottom neighbor
                if row < self.size - 1 and current == self.board[row + 1][col]:
                    return
        
        # No moves left
        self.game_over = True
    
    def reset(self) -> None:
        """Reset the game."""
        self.board = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.moved = False
        self._add_random_tile()
        self._add_random_tile()
    
    def get_board(self) -> List[List[int]]:
        """Get current board state."""
        return self.board.copy()
    
    def get_score(self) -> int:
        """Get current score."""
        return self.score