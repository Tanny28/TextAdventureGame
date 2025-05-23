🗡️ Advanced Text-Based Adventure Game – VirtuNexa Internship Project

🎮 Project Title: Realm of Endless Adventures

Author: Tanmay Shinde
Role: Python Intern
Duration: 1 Month
Organization: VirtuNexa

📜 Description
An immersive and fully-featured text-based adventure game built in modern Python 3.7+ with professional architecture and game mechanics. It simulates a turn-based RPG with:
Dynamic exploration
Combat system
Inventory management
Merchant trading
Puzzle mechanics
XP and leveling

Every decision is logged and tracked in an SQLite database, and the codebase is structured for clean testing, debugging, and maintainability.


🧠 Technologies Used

Python 3.7+
sqlite3 for game analytics and session tracking
logging module for game logs
json for save/load system
dataclasses, typing, enum for modern Python OOP
unittest for built-in unit testing


📁 Folder Structure

TANMAY_SHINDE_Adventure_Game/
├── adventure_quest.py       
├── launcher.py              
├── config.py               
├── test_game.py             
├── requirements.txt         
├── README.md                
├── setup.py                 
├── game_logs.txt            
├── adventure_game.db        
└── documentation/
    └── doc.pdf              

🚀 How to Run the Game

1. ✅ Prerequisites
Make sure you have Python 3.7+ installed.
No external packages required – standard library only.

2. 📦 Install
If you'd like to install as a package (optional):

pip install .

3. 🎮 Launch the Game
Option A: Via Launcher (Recommended)

python launcher.py

Option B: Run the Game Directly

python adventure_quest.py

4. 🧪 Run Tests

python test_game.py

🧩 Key Features
Feature	Description
🎲 Dynamic RPG World	Explore unique zones with items, enemies, events
⚔️ Combat System	Turn-based combat with XP and level-up
🛍️ Merchant System	Trade gold coins for potions or armor
🧠 Puzzle Elements	Logic-based riddle solving
📈 Database Analytics	Track sessions, scores, choices in SQLite
💾 Save/Load System	Save progress via JSON
🐍 Modern Python Design	Uses dataclasses, type hints, unittest, enum
📜 Logging	Logs events to game_logs.txt with timestamps
💡 Extensible	Easy to add more items, events, locations


📜 License
MIT License – for educational and internship use only.

