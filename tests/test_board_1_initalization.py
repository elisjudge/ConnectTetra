import numpy as np
import unittest
from game.board import GameBoard
import config as c

class TestBoardInitialization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n Running Board Initialization Tests... \n")

    def setUp(self):
        self.game_board = GameBoard()
        self.default_rows = 6
        self.default_columns = 7
        self.initial_board_value = 0
        self.custom_columns = 9
        self.custom_rows = 12

    def test_1_initialization_default_dimensions(self):
        self.assertTrue(hasattr(self.game_board, "rows"), "GameBoard should have property 'rows'.")
        self.assertTrue(hasattr(self.game_board, "columns"), "GameBoard should have property 'columns'.")
        self.assertEqual(self.game_board.rows, self.default_rows, "Default rows should equal 6.")
        self.assertEqual(self.game_board.columns, self.default_columns, "Default columns should equal 7.")
        self.assertTrue(np.all(self.game_board.board == self.initial_board_value), "All values of the board should equal zero.")

    def test_2_initialization_custom_dimensions(self):
        game_board = GameBoard(rows=self.custom_rows, columns=self.custom_columns)
        self.assertEqual(game_board.rows, self.custom_rows, "Custom rows are not being initialized.")
        self.assertEqual(game_board.columns, self.custom_columns, "Custom columns are not being initialized.")
        self.assertTrue(np.all(game_board.board == self.initial_board_value), "All values of the board should equal zero.")
    
    def test_3a_initialization_config_dimensions(self):
        config_max_cols = c.MAX_COLS
        config_min_cols = c.MIN_COLS
        self.assertEqual(GameBoard.MAX_COLS, config_max_cols, "Config MAX COLS does not equate to class MAX COLS.")
        self.assertEqual(GameBoard.MIN_COLS, config_min_cols, "Config MIN COLS does not equate to class MIN COLS.")

    def test_3b_enforce_max_cols(self):
        game_board = GameBoard(columns=c.MAX_COLS)      
        game_board.add_column()
        self.assertEqual(game_board.columns, GameBoard.MAX_COLS, "Maximum Column functionality is not being applied, columns exceed maximum")

    def test_3c_enforce_min_cols(self):
        game_board = GameBoard(columns=c.MIN_COLS)      
        game_board.remove_column(0) # Remove First Column
        self.assertEqual(game_board.columns, GameBoard.MIN_COLS, "Minimum Column functionality is not being applied, columns exceed minimum")

    def test_3d_initialization_raises_error_above_max_cols(self):
        with self.assertRaises(ValueError, msg="Initializing with columns greater than MAX_COLS should raise an error"):
            GameBoard(columns=GameBoard.MAX_COLS + 1)

    def test_3e_initialization_raises_error_below_min_cols(self):
        with self.assertRaises(ValueError, msg="Initializing with columns lesser than MIN_COLS should raise an error"):
            GameBoard(columns=GameBoard.MIN_COLS - 1)

    def test_4_initialization_column_addition_side(self):
        add_end_values = set()

        for _ in range(20):
            game_board = GameBoard()
            add_end_values.add(game_board._add_end)
            if len(add_end_values) == 2:
                break
        
        self.assertIn(True, add_end_values, "Gameboard is not initializing with randomized alternating side column add functionality: add_end is never initialized to True")
        self.assertIn(False, add_end_values, "Gameboard is not initializing with randomized alternating side column add functionality: add_end is never initialized to False")
            
if __name__ == "__main__":
    unittest.main()