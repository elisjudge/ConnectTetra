import unittest
from game.player import Player

class TestPlayer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nRunning tests for Player class...\n")
    
    def setUp(self):
        """Set up the player instance for testing"""
        self.expected_name = "Player 1"
        self.expected_symbol = 1
        self.player = Player(name=self.expected_name, symbol=self.expected_symbol)

    def test_1_initialization(self):
        self.assertEqual(self.player.name, self.expected_name)
        self.assertEqual(self.player.symbol, self.expected_symbol)
    
    def test_2_attribute_type(self):
        self.assertIsInstance(self.player.name, str)
        self.assertIsInstance(self.player.symbol, int)

    def test_3_select_move(self):
        # Check if select_move method exists
        self.assertTrue(hasattr(self.player, "select_move"))

        # Test the method 
        try:
            self.player.select_move()
        except Exception as e:
            self.fail(f"select_move raised an unexpected exception: {e}")

if __name__ == "__main__":
    unittest.main()