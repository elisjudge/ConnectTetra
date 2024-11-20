import unittest
from game.connect_tetra import ConnectTetra as Game
from game.player import Player
from game.board import GameBoard

class TestGameInitialization(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print("\n Running Game Initialization Tests... \n")

    def setUp(self):
        self.player1 = Player(name="Player 1", symbol = 1)
        self.player2 = Player(name="Player 2", symbol = 2)
        self.game = Game(player1=self.player1, player2=self.player2)
        self.expected_attributes  = [
            "gameboard",
            "player1",
            "player2",
            "current_player",
            "valid_moves",
            "winner",
            "history",
            "n_moves",
            "strict_mode"
        ]
        self.expected_methods = [
            "execute_move",
            "check_full_board",
            "validate_game_state",
            "is_winner",
            "is_4_in_a_row_horizontal",
            "is_4_in_a_row_vertical",
            "is_4_in_a_row_diag_left",
            "is_4_in_a_row_diag_right",
            "check_rows_columns_state",
            "update_valid_moves",
            "switch_turns",
            "announce_winner",
        ]

    def test_1_initialize_game_attributes(self):
        for attribute in self.expected_attributes:
            with self.subTest(attribute=attribute):
                self.assertTrue(hasattr(self.game, attribute), f"Game is supposed to initialize with attribute called {attribute}")

    def test_2_check_game_methods(self):
        for method_name in self.expected_methods:
            with self.subTest(method=method_name):
                self.assertTrue(callable(getattr(self.game, method_name, None)), f"Game class should have method {method_name}")
        
    def test_3_check_game_attribute_types(self):
        self.assertIsInstance(self.game.gameboard, GameBoard, "The gameboard of Game is meant to be of type Gameboard")
        self.assertIsInstance(self.game.player1, Player, "Player 1 of Game is meant to be of type Player")
        self.assertIsInstance(self.game.player2, Player, "Player 2 of Game is meant to be of type Player")
        self.assertIsInstance(self.game.current_player, Player, "Current Player of Game is meant to be of type Player")
        self.assertIsInstance(self.game.valid_moves, list, "Valid moves of Game is meant to be of type list")
        self.assertIsNone(self.game.winner, "Winner of Game is meant to be None")
        self.assertIsInstance(self.game.n_moves, int, "Game counter 'n_moves' is meant to be of type int")
        self.assertIsInstance(self.game.strict_mode, bool, "Game Strict Mode is meant to be of type bool")

    def test_4a_distinct_player_symbols(self):
        self.assertNotEqual(self.game.player1.symbol, self.player2.symbol, "Player symbols must be distinct from each other")

    def test_4b_correct_player_symbols(self):
        expected_player_1_symbol = 1
        expected_player_2_symbol = 2
        self.assertEqual(self.game.player1.symbol, expected_player_1_symbol, f"Player 1 symbol must be equal to {expected_player_1_symbol}")
        self.assertEqual(self.game.player2.symbol, expected_player_2_symbol, f"Player 2 symbol must be equal to {expected_player_2_symbol}")

    def test_4c_i_incorrect_player_symbols_raises_error_player_swap(self):
        """Swap the players around so that symbol 2 is player 1"""
        with self.assertRaisesRegex(ValueError, "Players not initialized with correct symbols"):
            Game(player1=self.player2, player2=self.player2)
        with self.assertRaisesRegex(ValueError, "Players not initialized with correct symbols"):
            Game(player1=self.player1, player2=self.player1)
    
    def test_4c_ii_incorrect_player_symbols_raises_error_invalid_symbol(self):
        incorrect_player_1_symbol = 3
        incorrect_player_2_symbol = "a"
        invalid_player_1 = Player(name="Player 1", symbol=incorrect_player_1_symbol)
        invalid_player_2 = Player(name="Player 2", symbol=incorrect_player_2_symbol)

        with self.assertRaisesRegex(ValueError, "Players not initialized with correct symbols"):
            Game(player1=invalid_player_1, player2=self.player2)
        with self.assertRaisesRegex(ValueError, "Players not initialized with correct symbols"):
            Game(player1=self.player1, player2=invalid_player_2)
        
    def test_5_check_first_player(self):
        self.assertEqual(self.game.current_player, self.game.player1, "First turn is not initialized correctly: Player 1 is not initialized as the Current Player")

    def test_6_test_initial_valid_moves(self):
        expected_moves = list(range(self.game.gameboard.columns))
        self.assertEqual(self.game.valid_moves, expected_moves, "Valid moves content does not match expected column indices")

    def test_7_initialize_game_counter(self):
        self.assertEqual(self.game.n_moves, 0, "Move counter 'n_moves' should be initialized to 0")

    def test_8a_check_default_game_history_tracking(self):
        self.assertIsNone(self.game.history, "Game history should be initialized to None")

    def test_8b_initialize_with_history_tracking(self):
        expected_default_history = []
        track_history_game = Game(player1=self.player1, player2=self.player2, track_history=True)
        self.assertEqual(track_history_game.history, expected_default_history, f"Game history should be initialized to {expected_default_history}")

    def test_9a_check_default_strict_mode(self):
        self.assertFalse(self.game.strict_mode, "Game default strict mode should be set to False")

    def test_9b_initialize_with_strict_mode(self):
        strict_mode_game = Game(player1=self.player1, player2=self.player2, strict_mode=True)
        self.assertTrue(strict_mode_game.strict_mode, "Game default strict mode should be set to True")

if __name__ == "__main__":
    unittest.main()