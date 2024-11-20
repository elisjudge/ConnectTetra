import numpy as np
import unittest
from game.connect_tetra import ConnectTetra as Game
from game.player import Player
from utils.errors import FullBoardError

class TestGameLogic(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print("\n Running Game Logic Tests... \n")

    def setUp(self):
        self.player1 = Player(name="Player 1", symbol = 1)
        self.player2 = Player(name="Player 2", symbol = 2)
        self.first_move = {"player":self.player1, "column": 0}
        self.game = Game(player1=self.player1, player2=self.player2)
        self.game_with_history = Game(player1=self.player1, player2=self.player2, track_history=True)
        self.game_with_strict_mode = Game(player1=self.player1, player2=self.player2, strict_mode=True)

    def test_1a_check_move_execution_default(self):
        n_moves = self.game.n_moves
        expected_valid_moves = self.game.valid_moves.copy()
        self.game.execute_move(player=self.first_move["player"], move=self.first_move["column"])

        with self.subTest("Move count increments"):
            expected_n_moves = n_moves + 1
            self.assertEqual(self.game.n_moves, expected_n_moves, "The move count did not increment by 1")

        with self.subTest("Turn switches to next player"):
            expected_current_player = self.player2
            self.assertEqual(self.game.current_player, expected_current_player, "Turn switching is not occuring in the game")

        with self.subTest("Board reflects the move"):
            placed_token = self.game.gameboard.board[-1, self.first_move["column"]]
            self.assertEqual(placed_token, self.player1.symbol, 
                f"Token for {self.player1.name} was not placed correctly in column {self.first_move['column']}")
        
        with self.subTest("Valid moves remain unchanged (initial turn)"):
            self.assertEqual(self.game.valid_moves, expected_valid_moves, 
                "Valid moves should remain unchanged between first turn and second turn")

    def test_1b_check_move_execution_track_history(self):
        expected_history = [self._create_expected_record(
            board=self.game_with_history.gameboard.board,
            column=self.first_move["column"],
            player=self.player1
        )]
        self.game_with_history.execute_move(player=self.first_move["player"], move=self.first_move["column"])
        self._verify_history(self.game_with_history.history, expected_history)

    def test_1c_check_move_execution_strict_mode(self):
        invalid_first_move = {"player":self.player2, "column": 0}
        with self.assertRaises(ValueError, msg="Strict mode should prevent moves by non-current players."):
            self.game_with_strict_mode.execute_move(player=invalid_first_move["player"], move=invalid_first_move["column"])

    def test_2_check_full_board_raises_error(self):
        invalid_game = Game(player1=self.player1, player2=self.player2)
        invalid_game.gameboard.board[:] = self.player1.symbol

        # Verify board state before calling the method
        self.assertTrue(np.all(invalid_game.gameboard.board != 0), 
            "Board state is not full as expected before calling check_full_board.")

        with self.assertRaisesRegex(FullBoardError, "Board is unexpectedly full. Game cannot continue."):
            invalid_game.check_full_board()

    def test_3_column_behaviours(self):
        """Tests the column removal logic of game"""
        game = Game(player1=self.player1, player2=self.player2)
        expected_column_count = game.gameboard.columns
        i = game.gameboard.columns

        while i >= game.gameboard.MIN_COLS:
            mid_col = game.gameboard.columns // 2

            with self.subTest("Check test column is empty"):
                self.assertFalse(np.all(game.gameboard.board[:, mid_col] != 0), "Column should not be full before filling.")
            
            with self.subTest("Check test column is full"):
                game.gameboard.board[:, mid_col] = self.player1.symbol
                self.assertTrue(np.all(game.gameboard.board[:, mid_col] != 0), "Column should be full before removal.")
            
            with self.subTest(f"Test column removal: n_cols = {game.gameboard.columns}"):
                game.check_rows_columns_state(move=mid_col)
                expected_column_count = max(expected_column_count - 1, game.gameboard.MIN_COLS)
                self.assertTrue(np.all(game.gameboard.board) == 0, "Column deletion is not working as expected. Full column remains on board")
                self.assertEqual(game.gameboard.columns, expected_column_count, 
                    f"Column deletion is not updating the column count correctly: Expected column count: {expected_column_count}, but got {game.gameboard.columns}.")
            i -= 1    

    def test_4_bottom_row_behaviours(self):
        game = Game(player1=self.player1, player2=self.player2)
        expected_row_count = game.gameboard.rows
        expected_column_count = game.gameboard.columns
        i = game.gameboard.columns

        while i <= game.gameboard.MAX_COLS:
            with self.subTest("Check bottom row and top row is empty"):
                self.assertFalse(np.all(game.gameboard.board[-1, :] != 0), "Bottom row should not be full before filling.")
                self.assertFalse(np.all(game.gameboard.board[0, :] != 0), "Top row should not be full before filling.")
            
            with self.subTest("Check test column is full"):
                game.gameboard.board[-1, :] = self.player1.symbol
                game.gameboard.board[0, :] = self.player1.symbol
                self.assertTrue(np.all(game.gameboard.board[-1, :] != 0), "Bottom row should be full before removal.")
                self.assertTrue(np.all(game.gameboard.board[0, :] != 0), "Top row should be full before removal.")

            game.check_rows_columns_state(move=0) # Just move to the left most column on board

            with self.subTest(f"Test bottom row removal and top row replacement"):
                self.assertTrue(np.all(game.gameboard.board[-1,:]) == 0, "Bottom row deletion is not working as expected. Full column remains on board")
                self.assertTrue(np.any(game.gameboard.board[1,:]) == self.player1.symbol, "Previous top row has not shifted to second row as expected")
                self.assertEqual(game.gameboard.rows, expected_row_count, 
                    f"Row deletion/addition is not updating the row count correctly: Expected row count: {expected_row_count}, but got {game.gameboard.rows}.")

            with self.subTest(f"Test column addtion: n_cols = {game.gameboard.columns}"):
                expected_column_count = min(expected_column_count + 1, game.gameboard.MAX_COLS)
                self.assertEqual(game.gameboard.board.shape, (game.gameboard.rows, expected_column_count), 
                    "The board shape does not match the expected dimensions after column addition.")
                
                if i != game.gameboard.MAX_COLS:
                    self.assertTrue(
                        game.gameboard.board[1, 0] == 0 or game.gameboard.board[1, -1] == 0,
                        "Neither the new leftmost column nor the rightmost column was initialized to zeros after row and column update.")
                elif i == game.gameboard.MAX_COLS:
                    self.assertTrue(
                        np.all(game.gameboard.board[1,:]) == self.player1.symbol, 
                        "Board edges do not contain symbol, suggesting that new column was added beyond maximum column allowance")
                
                self.assertEqual(game.gameboard.columns, expected_column_count, 
                f"Column addition is not updating the column count correctly: Expected column count: {expected_column_count}, but got {game.gameboard.columns}.")

            with self.subTest("Check second row is cleared before next iteration"):
                game.gameboard.board[1, :] = 0
                self.assertTrue(np.all(game.gameboard.board[1, :]) == 0, "The second row was not cleared as expected.")
            i += 1

    def test_5a_valid_move_updates_column_removal(self):
        game = Game(player1=self.player1, player2=self.player2)
        expected_column_count = game.gameboard.columns
        i = game.gameboard.columns

        while i >= game.gameboard.MIN_COLS:
            mid_col = game.gameboard.columns // 2
            game.gameboard.board[:, mid_col] = self.player1.symbol
            self.assertTrue(game.gameboard.is_column_full(mid_col), "Mid column is not full")

            game.check_rows_columns_state(move=mid_col)
            expected_column_count = max(expected_column_count - 1, game.gameboard.MIN_COLS)
            self.assertEqual(game.gameboard.columns, expected_column_count, "Columns are not equal")

            with self.subTest(f"Checking valid moves at n_cols: {game.gameboard.columns}"):
                expected_valid_moves = list(range(expected_column_count))
                self.assertEqual(game.valid_moves, expected_valid_moves, "Valid moves content does not match expected column indices")
            i -= 1

    def test_5b_valid_move_updates_column_addition(self):
        game = Game(player1=self.player1, player2=self.player2)
        expected_column_count = game.gameboard.columns
        i = game.gameboard.columns

        while i <= game.gameboard.MAX_COLS:
            game.gameboard.board[-1, :] = self.player1.symbol
            game.check_rows_columns_state(move=0)
            expected_column_count = min(expected_column_count + 1, game.gameboard.MAX_COLS)

            with self.subTest(f"Checking valid moves at n_cols: {game.gameboard.columns}"):
                expected_valid_moves = list(range(expected_column_count))
                self.assertEqual(game.valid_moves, expected_valid_moves, "Valid moves content does not match expected column indices")
            i += 1

    
    def test_6_board_state_validation(self):
        game = Game(player1=self.player1, player2=self.player2, track_history=True)

        # Initial state validation
        with self.subTest("Validate initial board state"):
            self.assertFalse(np.any(game.gameboard.board != 0), "Initial board state should be empty.")
            try:
                game.validate_game_state()  # Assuming this checks for anomalies
            except ValueError:
                self.fail("Initial board state validation unexpectedly failed.")

        # Valid Board State After Move
        with self.subTest("Validate board state after a move"):
            valid_move = {"player": self.player1, "column": 0}
            game.execute_move(player=valid_move["player"], move=valid_move["column"])

        with self.subTest("Check game history after single move"):
            self.assertEqual(len(game.history), 1, "History should contain one record after a single move.")
            
        with self.subTest("Check that end of history array contains the single move"):
            last_history_state = game.history[-1][0]
            self.assertTrue(
                np.array_equal(last_history_state, game.gameboard.board),
                "History does not match the latest board state after the move.")
            
        with self.subTest("Affrim that multiple calls of validate_game_state without new move raises error"):
            with self.assertRaises(ValueError, msg="Game History is not being properly updated"):
                game.validate_game_state()

        # Detect Board Corruption
        with self.subTest("Detect board corruption"):
            corrupted_game = Game(player1=self.player1, player2=self.player2, track_history=True)
            valid_move = {"player": self.player1, "column": 0}
            corrupted_game.execute_move(player=valid_move["player"], move=valid_move["column"])
            
            # Simulate corruption: overwrite the board with random values
            corrupted_game.gameboard._board[:, :] = np.random.randint(1, 3, corrupted_game.gameboard.board.shape)

            with self.assertRaises(ValueError, msg="Board corruption was not detected."):
                corrupted_game.validate_game_state()

    def _create_expected_record(self, board, column, player:Player):
        """Helper to create an expected history record."""
        expected_board = np.copy(board)
        expected_board[-1, column] = player.symbol
        return (expected_board, column, player)

    def _verify_history(self, actual_history, expected_history):
        """Helper to verify the game history."""
        self.assertEqual(len(actual_history), len(expected_history), "History length mismatch")
        for i, (actual_record, expected_record) in enumerate(zip(actual_history, expected_history)):
            with self.subTest(f"Checking history record {i}"):
                # Compare board states
                self.assertTrue(
                    np.array_equal(actual_record[0], expected_record[0]),
                    f"Mismatch in board state for history record {i}"
                )
                # Compare moves
                self.assertEqual(actual_record[1], expected_record[1], f"Mismatch in move for history record {i}")
                # Compare players
                self.assertEqual(actual_record[2], expected_record[2], f"Mismatch in player for history record {i}")

if __name__ == "__main__":
    unittest.main()