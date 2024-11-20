import numpy as np
import unittest
from game.connect_tetra import ConnectTetra as Game
from game.player import Player

class TestGameWinConditions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n Running Game Win Tests... \n")
    
    def setUp(self):
        self.player1 = Player(name="Player 1", symbol=1)
        self.player2 = Player(name="Player 2", symbol=2)

    def test_1_horizontal_win(self):
        max_col_game = self._generate_max_col_board()
        rows, columns = max_col_game.gameboard.board.shape
        self.assertEqual(rows, 6, "Maximum sized board has unexpected number of rows")
        self.assertEqual(columns, 10, "Maximum sized board has unexpected number of coumns")

        winning_player_symbol = max_col_game.player1.symbol # we will alternate between player symbols to ensure both trigger win

        for row in range(rows):
            for start_col in range(columns - 3):
                # Reset board from previous test
                max_col_game.gameboard.board[:, :] = 0
                self.assertEqual(max_col_game.is_4_in_a_row_horizontal(), 0, "Horizontal 4 in a row is being detected when it shouldn't be")

                for offset in range(4):
                    max_col_game.gameboard.board[row, start_col + offset] = winning_player_symbol

                ## Add tokens beneath testing row, except when testing row is the last row.
                if row < rows - 1:
                    # Create a single alternating pattern for one row
                    pattern = np.array([1, 2] * (columns // 2) + [1] * (columns % 2))
                    # Tile the pattern across all rows below the current row
                    max_col_game.gameboard.board[row + 1:, :] = np.tile(pattern, (rows - row - 1, 1))

                with self.subTest(f"Horizontal win starting at row {row}, col {start_col}, for player_{winning_player_symbol}"):
                    self.assertEqual(max_col_game.is_4_in_a_row_horizontal(), winning_player_symbol, "Horizontal 4 in a row is not being detected")
                
                winning_player_symbol = max_col_game.player2.symbol if winning_player_symbol == max_col_game.player1.symbol else max_col_game.player1.symbol
        
    def test_2_vertical_win(self):
        pass

    def test_3_diagonal_win_left_right(self):
        pass

    def test_4_diagonal_win_right_left(self):
        pass

    def _generate_max_col_board(self):
        game = Game(player1=self.player1, player2=self.player2)
        
        while game.gameboard.columns < game.gameboard.MAX_COLS:
            game.gameboard.board[-1, :] = game.player1.symbol
            game.check_rows_columns_state(move=0)
        
        self.assertEqual(game.gameboard.columns, game.gameboard.MAX_COLS, "The Board is not increasing to max column size")
        self.assertTrue(np.all(game.gameboard.board) == 0, "Board is not empty for some reason")
        return game

if __name__ == "__main__":
    unittest.main()


# Vertical Win: Verify a win for 4 tokens in a column.
# Diagonal Wins:
# Left-to-right diagonal win.
# Right-to-left diagonal win.