# adventure_quest.py
# Advanced Text-Based Adventure Game
# Author: [Your Name]
# Internship Project - Virtunexa

import random
import json
import sqlite3
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum

# Configure logging
logging.basicConfig(
    filename='game_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GameState(Enum):
    PLAYING = "playing"
    GAME_OVER = "game_over"
    VICTORY = "victory"
    PAUSED = "paused"

@dataclass
class Item:
    name: str
    description: str
    value: int
    usable: bool = False
    consumable: bool = False

@dataclass
class Character:
    name: str
    health: int
    max_health: int
    attack_power: int
    defense: int
    experience: int = 0
    level: int = 1

class GameDatabase:
    """Handles all database operations for game persistence"""
    
    def __init__(self, db_name: str = "adventure_game.db"):
        self.db_name = db_name
        self.initialize_database()
    
    def initialize_database(self):
        """Create necessary tables if they don't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                final_score INTEGER,
                game_state TEXT,
                total_decisions INTEGER,
                items_collected INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                decision_point TEXT,
                choice_made TEXT,
                timestamp TEXT,
                FOREIGN KEY (session_id) REFERENCES game_sessions (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def start_new_session(self, player_name: str) -> int:
        """Start a new game session and return session ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO game_sessions (player_name, start_time, game_state, total_decisions, items_collected)
            VALUES (?, ?, ?, 0, 0)
        ''', (player_name, datetime.now().isoformat(), GameState.PLAYING.value))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logging.info(f"New game session started for player: {player_name}")
        return session_id
    
    def log_decision(self, session_id: int, decision_point: str, choice: str):
        """Log a player decision"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO player_decisions (session_id, decision_point, choice_made, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (session_id, decision_point, choice, datetime.now().isoformat()))
        
        # Update decision counter
        cursor.execute('''
            UPDATE game_sessions 
            SET total_decisions = total_decisions + 1 
            WHERE id = ?
        ''', (session_id,))
        
        conn.commit()
        conn.close()
    
    def end_session(self, session_id: int, final_score: int, game_state: GameState, items_count: int):
        """End a game session"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE game_sessions 
            SET end_time = ?, final_score = ?, game_state = ?, items_collected = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), final_score, game_state.value, items_count, session_id))
        
        conn.commit()
        conn.close()

class AdvancedAdventureGame:
    """Main game class with advanced features"""
    
    def __init__(self):
        self.db = GameDatabase()
        self.session_id = None
        self.game_state = GameState.PLAYING
        self.current_location = "forest_start"
        self.player = None
        self.inventory = []
        self.game_score = 0
        self.decision_count = 0
        
        # Game items database
        self.items_db = {
            "rusty_sword": Item("Rusty Sword", "An old but functional sword", 25, True),
            "health_potion": Item("Health Potion", "Restores 30 health points", 30, True, True),
            "magic_crystal": Item("Magic Crystal", "A mysterious glowing crystal", 100),
            "ancient_key": Item("Ancient Key", "Opens mysterious doors", 50, True),
            "leather_armor": Item("Leather Armor", "Provides basic protection", 40, True),
            "gold_coin": Item("Gold Coin", "Currency of the realm", 10),
            "enchanted_bow": Item("Enchanted Bow", "A bow with magical properties", 75, True)
        }
        
        # Location database with dynamic descriptions
        self.locations = {
            "forest_start": {
                "name": "Mysterious Forest Entrance",
                "description": "Ancient trees tower above you, their branches creating a natural canopy. Sunlight filters through, creating dancing shadows on the forest floor.",
                "exits": ["north_trail", "east_clearing", "west_river"],
                "items": ["rusty_sword"],
                "enemies": None,
                "special_events": ["tutorial_guide"]
            },
            "north_trail": {
                "name": "Winding Forest Trail",
                "description": "The path winds deeper into the forest. You hear strange sounds echoing from the darkness ahead.",
                "exits": ["goblin_camp", "forest_start", "hidden_cave"],
                "items": ["health_potion"],
                "enemies": ["forest_wolf"],
                "special_events": None
            },
            "east_clearing": {
                "name": "Sunlit Clearing",
                "description": "A peaceful clearing bathed in golden sunlight. Wildflowers bloom around a crystal-clear spring.",
                "exits": ["forest_start", "ancient_ruins"],
                "items": ["magic_crystal", "gold_coin"],
                "enemies": None,
                "special_events": ["merchant_encounter"]
            },
            "west_river": {
                "name": "Babbling Brook",
                "description": "A gentle stream flows through smooth stones. The water is crystal clear and surprisingly deep.",
                "exits": ["forest_start", "waterfall_cave"],
                "items": ["ancient_key"],
                "enemies": ["river_serpent"],
                "special_events": ["bridge_puzzle"]
            },
            "goblin_camp": {
                "name": "Abandoned Goblin Camp",
                "description": "Crude tents and smoldering fire pits suggest recent goblin activity. The air smells of smoke and danger.",
                "exits": ["north_trail", "treasure_chamber"],
                "items": ["leather_armor", "gold_coin"],
                "enemies": ["goblin_warrior"],
                "special_events": None
            },
            "treasure_chamber": {
                "name": "Hidden Treasure Chamber",
                "description": "A magnificent chamber filled with gleaming treasures and ancient artifacts. This is clearly the end of your quest!",
                "exits": ["goblin_camp"],
                "items": ["enchanted_bow", "magic_crystal", "gold_coin"],
                "enemies": ["treasure_guardian"],
                "special_events": ["final_victory"]
            }
        }
    
    def display_welcome(self):
        """Display game welcome message"""
        print("\n" + "="*70)
        print("    🗡️  WELCOME TO THE REALM OF ENDLESS ADVENTURES  🗡️")
        print("="*70)
        print("A mystical world awaits your exploration...")
        print("Your choices will determine your fate!")
        print("="*70)
    
    def initialize_player(self):
        """Initialize player character"""
        print("\nBefore we begin your adventure...")
        player_name = input("What is your name, brave adventurer? ").strip()
        
        if not player_name:
            player_name = "Unknown Hero"
        
        self.player = Character(
            name=player_name,
            health=100,
            max_health=100,
            attack_power=20,
            defense=5
        )
        
        self.session_id = self.db.start_new_session(player_name)
        
        print(f"\nWelcome, {self.player.name}!")
        print(f"Health: {self.player.health}/{self.player.max_health}")
        print(f"Attack Power: {self.player.attack_power}")
        print(f"Defense: {self.player.defense}")
        
        logging.info(f"Player initialized: {player_name}")
    
    def display_status(self):
        """Display current player status"""
        print(f"\n📊 === STATUS ===")
        print(f"Health: {self.player.health}/{self.player.max_health}")
        print(f"Level: {self.player.level} (XP: {self.player.experience})")
        print(f"Score: {self.game_score}")
        print(f"Items: {len(self.inventory)}")
        
        if self.inventory:
            print("Inventory:", ", ".join([item.name for item in self.inventory]))
    
    def display_location(self):
        """Display current location details"""
        location = self.locations[self.current_location]
        
        print(f"\n🏞️  {location['name']}")
        print("─" * len(location['name']))
        print(location['description'])
        
        # Show available items
        if location['items']:
            available_items = [item for item in location['items'] if item in self.items_db]
            if available_items:
                print(f"\n✨ You notice: {', '.join(available_items)}")
        
        # Show exits
        exits_str = ", ".join(location['exits'])
        print(f"\n🚪 Available paths: {exits_str}")
    
    def handle_combat(self, enemy_name: str) -> bool:
        """Handle combat encounters"""
        enemy_stats = {
            "forest_wolf": {"health": 40, "attack": 15, "defense": 3},
            "goblin_warrior": {"health": 60, "attack": 20, "defense": 5},
            "river_serpent": {"health": 50, "attack": 25, "defense": 2},
            "treasure_guardian": {"health": 100, "attack": 30, "defense": 10}
        }
        
        if enemy_name not in enemy_stats:
            return True
        
        enemy = enemy_stats[enemy_name]
        print(f"\n⚔️  A wild {enemy_name.replace('_', ' ').title()} appears!")
        print(f"Enemy Health: {enemy['health']}")
        
        while enemy['health'] > 0 and self.player.health > 0:
            print(f"\nWhat do you want to do?")
            print("1. Attack")
            print("2. Use Item")
            print("3. Try to Flee")
            
            choice = input("Choose your action (1-3): ").strip()
            
            if choice == "1":
                # Player attacks
                damage = max(1, self.player.attack_power - enemy['defense'])
                enemy['health'] -= damage
                print(f"You deal {damage} damage to the {enemy_name.replace('_', ' ')}!")
                
                if enemy['health'] <= 0:
                    print(f"You defeated the {enemy_name.replace('_', ' ')}!")
                    self.player.experience += 25
                    self.game_score += 50
                    self.check_level_up()
                    return True
                
                # Enemy attacks back
                enemy_damage = max(1, enemy['attack'] - self.player.defense)
                self.player.health -= enemy_damage
                print(f"The {enemy_name.replace('_', ' ')} deals {enemy_damage} damage to you!")
                
            elif choice == "2":
                if self.use_item_in_combat():
                    continue
                else:
                    print("No usable items!")
                    
            elif choice == "3":
                if random.random() < 0.4:  # 40% chance to flee
                    print("You successfully flee from combat!")
                    return False
                else:
                    print("You couldn't escape!")
                    # Enemy gets a free attack
                    enemy_damage = max(1, enemy['attack'] - self.player.defense)
                    self.player.health -= enemy_damage
                    print(f"The {enemy_name.replace('_', ' ')} attacks you for {enemy_damage} damage!")
            
            if self.player.health <= 0:
                self.game_state = GameState.GAME_OVER
                return False
        
        return True
    
    def use_item_in_combat(self) -> bool:
        """Use an item during combat"""
        usable_items = [item for item in self.inventory if item.usable]
        
        if not usable_items:
            return False
        
        print("\nUsable items:")
        for i, item in enumerate(usable_items, 1):
            print(f"{i}. {item.name} - {item.description}")
        
        try:
            choice = int(input("Choose item to use (0 to cancel): "))
            if choice == 0:
                return False
            
            item = usable_items[choice - 1]
            
            if item.name == "Health Potion":
                heal_amount = min(30, self.player.max_health - self.player.health)
                self.player.health += heal_amount
                print(f"You heal for {heal_amount} health!")
                
                if item.consumable:
                    self.inventory.remove(item)
                    print(f"{item.name} was consumed!")
                
                return True
                
        except (ValueError, IndexError):
            print("Invalid choice!")
            return False
        
        return False
    
    def check_level_up(self):
        """Check if player levels up"""
        exp_needed = self.player.level * 100
        if self.player.experience >= exp_needed:
            self.player.level += 1
            self.player.max_health += 20
            self.player.health = self.player.max_health  # Full heal on level up
            self.player.attack_power += 5
            self.player.defense += 2
            print(f"\n🎉 LEVEL UP! You are now level {self.player.level}!")
            print(f"Health increased to {self.player.max_health}!")
            print(f"Attack power increased to {self.player.attack_power}!")
    
    def handle_special_events(self, event_name: str):
        """Handle special story events"""
        if event_name == "tutorial_guide":
            print("\n🧙 An old wizard appears before you...")
            print("'Welcome, young adventurer! Let me teach you the basics of survival.'")
            print("'Type 'help' anytime to see available commands.'")
            print("'Remember, your choices shape your destiny!'")
            
        elif event_name == "merchant_encounter":
            print("\n🏪 A traveling merchant greets you cheerfully...")
            print("'Fine day for an adventure! Care to trade?'")
            self.merchant_trade()
            
        elif event_name == "bridge_puzzle":
            print("\n🌉 You find an ancient stone bridge...")
            self.bridge_puzzle()
            
        elif event_name == "final_victory":
            print("\n🏆 You have reached the legendary treasure chamber!")
            print("Congratulations! You've completed your epic adventure!")
            self.game_state = GameState.VICTORY
            self.game_score += 500
    
    def merchant_trade(self):
        """Handle merchant trading"""
        print("\nMerchant's wares:")
        print("1. Health Potion (Cost: 2 Gold Coins)")
        print("2. Leather Armor (Cost: 3 Gold Coins)")
        print("3. Leave")
        
        gold_count = sum(1 for item in self.inventory if item.name == "Gold Coin")
        print(f"Your gold: {gold_count} coins")
        
        choice = input("What would you like to do? (1-3): ").strip()
        
        if choice == "1" and gold_count >= 2:
            # Remove gold coins
            for _ in range(2):
                for item in self.inventory:
                    if item.name == "Gold Coin":
                        self.inventory.remove(item)
                        break
            self.inventory.append(self.items_db["health_potion"])
            print("You purchased a Health Potion!")
            
        elif choice == "2" and gold_count >= 3:
            # Remove gold coins
            for _ in range(3):
                for item in self.inventory:
                    if item.name == "Gold Coin":
                        self.inventory.remove(item)
                        break
            self.inventory.append(self.items_db["leather_armor"])
            print("You purchased Leather Armor!")
            
        elif choice in ["1", "2"]:
            print("You don't have enough gold!")
        else:
            print("You decide not to trade.")
    
    def bridge_puzzle(self):
        """Handle bridge puzzle"""
        print("The bridge has an ancient riddle carved into it:")
        print("'I have keys but no locks. I have space but no room.")
        print("You can enter, but not go inside. What am I?'")
        
        answer = input("Your answer: ").strip().lower()
        
        if answer in ["keyboard", "a keyboard"]:
            print("✅ Correct! The bridge glows and becomes safe to cross!")
            print("You found a hidden treasure underneath!")
            self.inventory.append(self.items_db["magic_crystal"])
            self.game_score += 100
        else:
            print("❌ The bridge creaks ominously. You carefully cross anyway.")
            print("You take 10 damage from falling stones!")
            self.player.health = max(1, self.player.health - 10)
    
    def process_command(self, command: str):
        """Process player commands"""
        command = command.lower().strip()
        
        if command == "help":
            self.show_help()
        elif command == "status":
            self.display_status()
        elif command == "inventory":
            self.show_inventory()
        elif command.startswith("go "):
            destination = command[3:]
            self.move_to_location(destination)
        elif command.startswith("take "):
            item_name = command[5:]
            self.take_item(item_name)
        elif command.startswith("use "):
            item_name = command[4:]
            self.use_item(item_name)
        elif command == "look":
            self.display_location()
        elif command == "save":
            self.save_game()
        elif command == "quit":
            self.quit_game()
        else:
            print("Unknown command. Type 'help' for available commands.")
    
    def show_help(self):
        """Display help information"""
        print("\n📖 === HELP ===")
        print("Available commands:")
        print("  help        - Show this help")
        print("  status      - Show character status")
        print("  inventory   - Show your items")
        print("  look        - Look around current location")
        print("  go [place]  - Move to a location")
        print("  take [item] - Pick up an item")
        print("  use [item]  - Use an item from inventory")
        print("  save        - Save your progress")
        print("  quit        - Exit the game")
    
    def show_inventory(self):
        """Display player inventory"""
        if not self.inventory:
            print("\n🎒 Your inventory is empty.")
        else:
            print(f"\n🎒 Inventory ({len(self.inventory)} items):")
            for item in self.inventory:
                print(f"  • {item.name} - {item.description}")
    
    def take_item(self, item_name: str):
        """Take an item from current location"""
        location = self.locations[self.current_location]
        
        # Find matching item (partial name matching)
        matching_items = [item for item in location['items'] 
                         if item_name.lower() in item.lower()]
        
        if not matching_items:
            print(f"There's no '{item_name}' here.")
            return
        
        item_key = matching_items[0]
        if item_key in self.items_db:
            item = self.items_db[item_key]
            self.inventory.append(item)
            location['items'].remove(item_key)
            print(f"You picked up: {item.name}")
            self.game_score += item.value
            logging.info(f"Player took item: {item.name}")
        else:
            print("You can't take that.")
    
    def use_item(self, item_name: str):
        """Use an item from inventory"""
        matching_items = [item for item in self.inventory 
                         if item_name.lower() in item.name.lower()]
        
        if not matching_items:
            print(f"You don't have '{item_name}'.")
            return
        
        item = matching_items[0]
        
        if not item.usable:
            print(f"You can't use {item.name}.")
            return
        
        if item.name == "Health Potion":
            heal_amount = min(30, self.player.max_health - self.player.health)
            self.player.health += heal_amount
            print(f"You heal for {heal_amount} health!")
            
            if item.consumable:
                self.inventory.remove(item)
                print(f"{item.name} was consumed!")
        
        elif item.name == "Leather Armor":
            self.player.defense += 3
            print("You equip the leather armor! Defense increased by 3!")
            self.inventory.remove(item)
        
        elif item.name == "Rusty Sword":
            self.player.attack_power += 10
            print("You equip the rusty sword! Attack power increased by 10!")
            self.inventory.remove(item)
    
    def move_to_location(self, destination: str):
        """Move to a new location"""
        current_loc = self.locations[self.current_location]
        
        # Find matching exit (partial name matching)
        matching_exits = [exit_name for exit_name in current_loc['exits'] 
                         if destination.lower() in exit_name.lower()]
        
        if not matching_exits:
            print(f"You can't go to '{destination}' from here.")
            print(f"Available paths: {', '.join(current_loc['exits'])}")
            return
        
        new_location = matching_exits[0]
        self.current_location = new_location
        
        # Log the decision
        self.db.log_decision(self.session_id, f"move_from_{current_loc}", new_location)
        self.decision_count += 1
        
        print(f"\n🚶 You travel to {self.locations[new_location]['name']}...")
        
        # Handle location events
        location = self.locations[new_location]
        
        # Handle enemies
        if location['enemies'] and random.random() < 0.6:
            enemy = random.choice(location['enemies'])
            if not self.handle_combat(enemy):
                return  # Combat failed
        
        # Handle special events
        if location['special_events']:
            for event in location['special_events']:
                self.handle_special_events(event)
        
        # Display new location
        self.display_location()
        
        logging.info(f"Player moved to: {new_location}")
    
    def save_game(self):
        """Save current game state"""
        save_data = {
            "player": {
                "name": self.player.name,
                "health": self.player.health,
                "max_health": self.player.max_health,
                "attack_power": self.player.attack_power,
                "defense": self.player.defense,
                "experience": self.player.experience,
                "level": self.player.level
            },
            "game_state": {
                "current_location": self.current_location,
                "inventory": [item.name for item in self.inventory],
                "game_score": self.game_score,
                "decision_count": self.decision_count
            }
        }
        
        with open(f"save_{self.player.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print("Game saved successfully!")
        logging.info("Game saved")
    
    def quit_game(self):
        """Quit the game"""
        print("\nThank you for playing! Your adventure ends here...")
        
        # End database session
        if self.session_id:
            self.db.end_session(
                self.session_id, 
                self.game_score, 
                self.game_state, 
                len(self.inventory)
            )
        
        self.game_state = GameState.GAME_OVER
    
    def run_game(self):
        """Main game loop"""
        self.display_welcome()
        self.initialize_player()
        
        print(f"\n{self.player.name}, your adventure begins...")
        self.display_location()
        
        while self.game_state == GameState.PLAYING:
            try:
                if self.player.health <= 0:
                    print("\n💀 You have died! Game Over!")
                    self.game_state = GameState.GAME_OVER
                    break
                
                print(f"\n🎮 What would you like to do?")
                command = input(">>> ").strip()
                
                if not command:
                    continue
                
                self.process_command(command)
                
                # Check victory condition
                if self.current_location == "treasure_chamber" and self.game_state == GameState.PLAYING:
                    self.handle_special_events("final_victory")
                
            except KeyboardInterrupt:
                print("\n\nGame interrupted by user.")
                self.quit_game()
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                logging.error(f"Game error: {e}")
        
        # Game end
        self.display_final_score()
    
    def display_final_score(self):
        """Display final game statistics"""
        print("\n" + "="*50)
        print("           🏁 ADVENTURE COMPLETE!")
        print("="*50)
        print(f"Player: {self.player.name}")
        print(f"Final Score: {self.game_score}")
        print(f"Level Reached: {self.player.level}")
        print(f"Items Collected: {len(self.inventory)}")
        print(f"Decisions Made: {self.decision_count}")
        
        if self.game_state == GameState.VICTORY:
            print("\n🎉 VICTORY! You successfully completed your quest!")
        else:
            print("\n💀 Better luck next time, adventurer!")
        
        print("="*50)

def main():
    """Main function to start the game"""
    try:
        game = AdvancedAdventureGame()
        game.run_game()
    except Exception as e:
        print(f"Critical error: {e}")
        logging.critical(f"Critical game error: {e}")

if __name__ == "__main__":
    main()