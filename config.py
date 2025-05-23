# Game Configuration
"""
Game configuration settings
Modify these values to customize the game experience
"""

class GameConfig:
    # Database settings
    DATABASE_NAME = "adventure_game.db"
    LOG_FILE_NAME = "game_logs.txt"
    
    # Game balance settings
    STARTING_HEALTH = 100
    STARTING_ATTACK = 20
    STARTING_DEFENSE = 5
    
    # Experience and leveling
    BASE_XP_REQUIREMENT = 100
    HEALTH_PER_LEVEL = 20
    ATTACK_PER_LEVEL = 5
    DEFENSE_PER_LEVEL = 2
    
    # Combat settings
    FLEE_SUCCESS_RATE = 0.4
    ENEMY_ENCOUNTER_RATE = 0.6
    
    # Item values
    ITEM_VALUES = {
        "rusty_sword": 25,
        "health_potion": 30,
        "magic_crystal": 100,
        "ancient_key": 50,
        "leather_armor": 40,
        "gold_coin": 10,
        "enchanted_bow": 75
    }
    
    # Scoring system
    ITEM_PICKUP_BONUS = 10
    COMBAT_VICTORY_BONUS = 50
    PUZZLE_SOLUTION_BONUS = 100
    FINAL_VICTORY_BONUS = 500
    
    # Merchant prices
    MERCHANT_PRICES = {
        "health_potion": 2,  # gold coins
        "leather_armor": 3,  # gold coins
    }
