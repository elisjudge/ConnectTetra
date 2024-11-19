import unittest
import config as c
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

    def test_1_initialize_game_attributes(self):
        self.assertTrue(hasattr(self.game, "gameboard"), "Game is supposed to initialize with a gameboard")
        self.assertTrue(hasattr(self.game, "player1"), "Game is supposed to initialize with a Player 1")
        self.assertTrue(hasattr(self.game, "player2"), "Game is supposed to initialize with a Player 2")
        self.assertTrue(hasattr(self.game, "current_player"), "Game is supposed to initialize with a current player")
        self.assertTrue(hasattr(self.game, "valid_moves"), "Game is supposed to initialize with valid moves")
        self.assertTrue(hasattr(self.game, "winner"), "Game is supposed to initialize with a winner")
        self.assertTrue(hasattr(self.game, "n_moves"), "Game is supposed to initialize with a move counter 'n_moves'")

    def test_2_check_game_attribute_types(self):
        self.assertIsInstance(self.game.gameboard, GameBoard, "The gameboard of Game is meant to be of type Gameboard")
        self.assertIsInstance(self.game.player1, Player, "Player 1 of Game is meant to be of type Player")
        self.assertIsInstance(self.game.player2, Player, "Player 2 of Game is meant to be of type Player")
        self.assertIsInstance(self.game.current_player, Player, "Current Player of Game is meant to be of type Player")
        self.assertIsInstance(self.game.valid_moves, list, "Valid moves of Game is meant to be of type list")
        self.assertIsNone(self.game.winner, "Winner of Game is meant to be None")
        self.assertIsInstance(self.game.n_moves, int, "Game counter 'n_moves' is meant to be of type int")
        
    def test_3a_distinct_player_symbols(self):
        self.assertNotEqual(self.game.player1.symbol, self.player2.symbol, "Player symbols must be distinct from each other")

    def test_3b_correct_player_symbols(self):
        expected_player_1_symbol = 1
        expected_player_2_symbol = 2
        self.assertEqual(self.game.player1.symbol, expected_player_1_symbol, f"Player 1 symbol must be equal to {expected_player_1_symbol}")
        self.assertEqual(self.game.player2.symbol, expected_player_2_symbol, f"Player 2 symbol must be equal to {expected_player_2_symbol}")

    def test_3c_i_incorrect_player_symbols_raises_error_player_swap(self):
        """Swap the players around so that symbol 2 is player 1"""
        with self.assertRaisesRegex(ValueError, "Players not initialized with correct symbols"):
            Game(player1=self.player2, player2=self.player2)
        with self.assertRaisesRegex(ValueError, "Players not initialized with correct symbols"):
            Game(player1=self.player1, player2=self.player1)
    
    def test_3c_ii_incorrect_player_symbols_raises_error_invalid_symbol(self):
        incorrect_player_1_symbol = 3
        incorrect_player_2_symbol = "a"
        invalid_player_1 = Player(name="Player 1", symbol=incorrect_player_1_symbol)
        invalid_player_2 = Player(name="Player 2", symbol=incorrect_player_2_symbol)

        with self.assertRaisesRegex(ValueError, "Players not initialized with correct symbols"):
            Game(player1=invalid_player_1, player2=self.player2)
        with self.assertRaisesRegex(ValueError, "Players not initialized with correct symbols"):
            Game(player1=self.player1, player2=invalid_player_2)
        
    def test_4_check_first_player(self):
        self.assertEqual(self.game.current_player, self.game.player1, "First turn is not initialized correctly: Player 1 is not initialized as the Current Player")

    def test_5_test_initial_valid_moves(self):
        expected_moves = list(range(self.game.gameboard.columns))
        self.assertEqual(self.game.valid_moves, expected_moves, "Valid moves content does not match expected column indices")

    def test_6_initialize_game_counter(self):
        self.assertEqual(self.game.n_moves, 0, "Move counter 'n_moves' should be initialized to 0")
