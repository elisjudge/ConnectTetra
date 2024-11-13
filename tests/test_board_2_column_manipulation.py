import config as c
import numpy as np
import unittest
from game.board import GameBoard

class TestBoardColumnManipulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n Running Board Column Manipulation Tests... \n")
    
    def setUp(self):
        self.test_columns = 7
        self.expected_columns_after_add = self.test_columns + 1
        self.expected_columns_after_subtract = self.test_columns - 1
        self.test_value = 1

    def test_1a_add_columns(self):
        game_board = GameBoard(columns=self.test_columns)
        game_board.board[:, :] = self.test_value # Fill board with a test value.
        
        # Logic to test for the correct side
        new_column_index = -1 if game_board._add_end else 0
        opposite_index = 0 if new_column_index == -1 else -1

        game_board.add_column()
        self.assertEqual(game_board.columns, self.expected_columns_after_add, "Adding a column did not increase the column count by 1.")
        self.assertTrue(np.all(game_board.board[:, new_column_index] == 0), "The new column is not filled with zeros.")
        self.assertTrue(np.all(game_board.board[:, opposite_index] == self.test_value), "The new column was not allocated to the expected side.")

    def test_1b_add_columns_at_limit(self):
        game_board = GameBoard(columns=c.MAX_COLS)      
        game_board.add_column()
        self.assertEqual(game_board.columns, GameBoard.MAX_COLS, "Maximum Column functionality is not being applied, columns exceed maximum")

    def test_2a_remove_columns(self):
        game_board = GameBoard(columns=self.test_columns)
        game_board.remove_column(0) 
        self.assertEqual(game_board.columns, self.expected_columns_after_subtract, "Removing a column did not decrease the column count by 1.")

    def test_2b_remove_columns_at_limit(self):
        game_board = GameBoard(columns=c.MIN_COLS)      
        game_board.remove_column(0) 
        self.assertEqual(game_board.columns, GameBoard.MIN_COLS, "Minimum Column functionality is not being applied, columns exceed minimum")

    def test_3a_column_is_full(self):
        game_board = GameBoard()
        game_board.board[:, 0] = self.test_value # Add values to entire first column
        self.assertTrue(game_board.is_column_full(0), "Board is not detecting that the column is full")

    def test_3b_column_is_not_full(self):
        game_board = GameBoard()
        game_board.board[-1, 0] = self.test_value # Add value to bottom corner
        game_board.board[-3:, 1] = self.test_value # Add threes values to second column 
        self.assertFalse(game_board.is_column_full(0), "Board is detecting that the column is full when it should not be")
        self.assertFalse(game_board.is_column_full(1), "Board is detecting that the column is full when it should not be")

if __name__ == "__main__":
    unittest.main()