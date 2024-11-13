import numpy as np
import unittest
from game.board import GameBoard

class TestBoardRowManipulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n Running Board Row Manipulation Tests... \n")

    def setUp(self):
        self.test_rows = 6
        self.test_expected_rows_after_add = self.test_rows + 1
        self.test_expected_rows_after_remove = self.test_rows - 1
        self.test_value = 1

    def test_1_add_row(self):
        game_board = GameBoard(rows=self.test_rows)
        game_board.board[:, :] = self.test_value

        game_board.add_row()
        self.assertEqual(game_board.rows, self.test_expected_rows_after_add, "Adding a row did not increase the row count by 1.")
        self.assertTrue(np.all(game_board.board[0, :] == 0), "The new row is not filled with zeros." )
        self.assertTrue(np.all(game_board.board[-1, :] == self.test_value), "The new row was not allocated to the top of the board.")

    def test_2_remove_row(self):
        game_board = GameBoard(rows=self.test_rows)
        game_board.remove_row()
        self.assertEqual(game_board.rows, self.test_expected_rows_after_remove, "Removing a row did not decrease the row count by 1.")

    def test_3a_bottom_row_is_full(self):
        game_board = GameBoard()
        game_board.board[-1, :] = self.test_value
        self.assertTrue(game_board.is_bottomrow_full(), "Board is not detecting that the bottom row is full")

    def test_3b_bottom_row_is_not_full(self):
        game_board = GameBoard()
        game_board.board[-1, :-1] = self.test_value # Add values to all but bottom right corner
        self.assertFalse(game_board.is_bottomrow_full(), "Board is detecting that the bottom row is full when it should not be")  

if __name__ == "__main__":
    unittest.main()