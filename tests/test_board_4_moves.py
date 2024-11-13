import unittest
from game.board import GameBoard

class TestBoardMoves(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n Running Board Move Tests... \n")

    def setUp(self):
        self.player_1_token = 1
        self.player_2_token = 2

        self.valid_move_test_moves = [
            (0, self.player_1_token),
            (1, self.player_2_token),
            (2, self.player_1_token),
            (3, self.player_2_token),
            (4, self.player_1_token),
            (5, self.player_2_token),
            (6, self.player_1_token)]
        
        self.bottom_up_test_moves = [
            (0, self.player_1_token),
            (0, self.player_2_token),
            (0, self.player_1_token),
            (0, self.player_2_token),
            (0, self.player_1_token),
            (0, self.player_2_token)]
        
        self.fill_column_moves = [
            (0, self.player_1_token),
            (0, self.player_2_token),
            (0, self.player_1_token),
            (0, self.player_2_token),
            (0, self.player_1_token),
            (0, self.player_2_token)]
        
        self.invalid_move = (0, self.player_1_token)

        
    def test_1_valid_move(self):
        game_board = GameBoard(rows=6, columns=7)

        for move in self.valid_move_test_moves:
            game_board.board = move

        bottom_row_full = game_board.is_bottomrow_full()

        self.assertTrue(bottom_row_full, "One or more tokens did not get placed in their columns")

        if not bottom_row_full:
            for column, token in self.valid_move_test_moves:
                with self.subTest(column=column, token=token):
                    self.assertEqual(game_board.board[-1, column], token, f"Token {token} was not correctly placed in column {column}")
        
    def test_2_move_fills_column_bottom_up(self):
        game_board = GameBoard(rows=6, columns=7)
        expected_row_index = game_board.rows - 1

        for column, token in self.bottom_up_test_moves:
            game_board.board = (column, token)
            with self.subTest(column=column, token=token):
                self.assertEqual(game_board.board[expected_row_index, column], token, f"Token {token} was not placed correctly at expected row {expected_row_index}")
            expected_row_index -= 1

    def test_3_invalid_move(self):
        game_board = GameBoard(rows=6, columns=7)
        
        for move in self.fill_column_moves:
            game_board.board = move

        self.assertTrue(game_board.is_column_full(0), "Column is not full as expected")    

        with self.assertRaises(Exception, msg="Adding a move to a full column should raise an error"):
            game_board.board = self.invalid_move
        
if __name__ == "__main__":
    unittest.main()