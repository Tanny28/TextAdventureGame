# Simple test file
"""
Basic tests for the adventure game
Run this file to verify game functionality
"""

import unittest
import tempfile
import os
from pathlib import Path

# Import the game classes (assuming they're in adventure_quest.py)
try:
    from adventure_quest import AdvancedAdventureGame, GameDatabase, Item, Character
    GAME_AVAILABLE = True
except ImportError:
    GAME_AVAILABLE = False
    print("Game modules not available for testing")

class TestAdventureGame(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        if not GAME_AVAILABLE:
            self.skipTest("Game modules not available")
        
        # Create temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        self.game = AdvancedAdventureGame()
        self.game.db = GameDatabase(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test environment"""
        if hasattr(self, 'temp_db'):
            os.unlink(self.temp_db.name)
    
    def test_item_creation(self):
        """Test item creation"""
        item = Item("Test Sword", "A test weapon", 50, True)
        self.assertEqual(item.name, "Test Sword")
        self.assertEqual(item.value, 50)
        self.assertTrue(item.usable)
    
    def test_character_creation(self):
        """Test character creation"""
        character = Character("Hero", 100, 100, 20, 5)
        self.assertEqual(character.name, "Hero")
        self.assertEqual(character.health, 100)
        self.assertEqual(character.attack_power, 20)
    
    def test_database_operations(self):
        """Test database functionality"""
        db = GameDatabase(self.temp_db.name)
        session_id = db.start_new_session("TestPlayer")
        self.assertIsInstance(session_id, int)
        self.assertGreater(session_id, 0)
    
    def test_game_initialization(self):
        """Test game initialization"""
        self.assertIsNotNone(self.game.items_db)
        self.assertIsNotNone(self.game.locations)
        self.assertEqual(self.game.current_location, "forest_start")

def run_tests():
    """Run all tests"""
    unittest.main(verbosity=2)

if __name__ == "__main__":
    run_tests()