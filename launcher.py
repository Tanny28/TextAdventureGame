#!/usr/bin/env python3
"""
Adventure Game Launcher
Provides a simple interface to start the game with various options
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all required components are available"""
    required_modules = ['sqlite3', 'json', 'logging', 'datetime', 'dataclasses', 'typing', 'enum', 'random']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing required modules: {', '.join(missing_modules)}")
        print("Please install Python 3.7+ with standard library")
        return False
    
    return True

def display_banner():
    """Display game banner"""
    banner = """
    ╔══════════════════════════════════════════════════╗
    ║        🗡️  ADVENTURE GAME LAUNCHER  🗡️           ║
    ╠══════════════════════════════════════════════════╣
    ║  Advanced Text-Based Adventure Game              ║
    ║  Developed for Virtunexa Internship              ║
    ║  Python 3.7+ Required                           ║
    ╚══════════════════════════════════════════════════╝
    """
    print(banner)

def show_menu():
    """Display launcher menu"""
    print("\n🎮 Game Options:")
    print("1. Start New Adventure")
    print("2. View Game Documentation")
    print("3. Check System Requirements")
    print("4. View Game Statistics")
    print("5. Clean Game Data")
    print("6. Exit")
    print("\n" + "─" * 50)

def start_game():
    """Launch the main game"""
    game_file = Path("adventure_quest.py")
    
    if not game_file.exists():
        print("❌ Game file 'adventure_quest.py' not found!")
        print("Please ensure the game file is in the same directory.")
        return
    
    print("🚀 Starting Adventure Game...")
    print("─" * 30)
    
    try:
        # Import and run the game
        import adventure_quest
        adventure_quest.main()
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        print("Please check the game file for errors.")

def view_documentation():
    """Display game documentation"""
    doc_file = Path("README.md")
    
    if doc_file.exists():
        print("📖 Opening game documentation...")
        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Display first 2000 characters
                print(content[:2000] + "..." if len(content) > 2000 else content)
        except Exception as e:
            print(f"❌ Error reading documentation: {e}")
    else:
        print("📖 Game Documentation Summary:")
        print("─" * 40)
        print("• Advanced text-based adventure game")
        print("• SQLite database integration")
        print("• Character progression system")
        print("• Combat and inventory mechanics")
        print("• Multiple storyline paths")
        print("• Save/load functionality")
        print("• Comprehensive logging system")

def check_system():
    """Check system requirements"""
    print("🔍 System Requirements Check:")
    print("─" * 35)
    
    # Python version
    python_version = sys.version_info
    print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version >= (3, 7):
        print("✅ Python version is compatible")
    else:
        print("❌ Python 3.7+ required")
    
    # Required modules
    print("\nChecking required modules...")
    if check_requirements():
        print("✅ All required modules available")
    
    # File system
    game_file = Path("adventure_quest.py")
    print(f"\nGame file exists: {'✅ Yes' if game_file.exists() else '❌ No'}")
    
    # Database
    db_file = Path("adventure_game.db")
    print(f"Database file: {'📁 Exists' if db_file.exists() else '🆕 Will be created'}")
    
    # Logs
    log_file = Path("game_logs.txt")
    print(f"Log file: {'📁 Exists' if log_file.exists() else '🆕 Will be created'}")

def view_statistics():
    """View game statistics from database"""
    try:
        import sqlite3
        from pathlib import Path
        
        db_file = Path("adventure_game.db")
        if not db_file.exists():
            print("📊 No game statistics available yet.")
            print("Play the game first to generate statistics!")
            return
        
        conn = sqlite3.connect("adventure_game.db")
        cursor = conn.cursor()
        
        print("📊 Game Statistics:")
        print("─" * 25)
        
        # Total sessions
        cursor.execute("SELECT COUNT(*) FROM game_sessions")
        total_sessions = cursor.fetchone()[0]
        print(f"Total Game Sessions: {total_sessions}")
        
        # Completed games
        cursor.execute("SELECT COUNT(*) FROM game_sessions WHERE game_state = 'victory'")
        victories = cursor.fetchone()[0]
        print(f"Victories: {victories}")
        
        # Average score
        cursor.execute("SELECT AVG(final_score) FROM game_sessions WHERE final_score IS NOT NULL")
        avg_score = cursor.fetchone()[0]
        if avg_score:
            print(f"Average Score: {avg_score:.1f}")
        
        # Top players
        cursor.execute("""
            SELECT player_name, MAX(final_score) as best_score 
            FROM game_sessions 
            WHERE final_score IS NOT NULL 
            GROUP BY player_name 
            ORDER BY best_score DESC 
            LIMIT 5
        """)
        
        top_players = cursor.fetchall()
        if top_players:
            print("\n🏆 Top Players:")
            for i, (name, score) in enumerate(top_players, 1):
                print(f"  {i}. {name}: {score} points")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading statistics: {e}")

def clean_data():
    """Clean game data files"""
    print("🧹 Game Data Cleanup:")
    print("─" * 25)
    
    files_to_clean = [
        ("adventure_game.db", "Game database"),
        ("game_logs.txt", "Game logs"),
    ]
    
    # Find save files
    save_files = list(Path(".").glob("save_*.json"))
    
    print("Files that will be removed:")
    for file_path, description in files_to_clean:
        if Path(file_path).exists():
            print(f"  • {description} ({file_path})")
    
    for save_file in save_files:
        print(f"  • Save file ({save_file.name})")
    
    if not any(Path(f[0]).exists() for f in files_to_clean) and not save_files:
        print("🎉 No data files to clean!")
        return
    
    confirm = input("\n⚠️  Are you sure you want to delete all game data? (yes/no): ").lower()
    
    if confirm == "yes":
        cleaned_count = 0
        
        for file_path, description in files_to_clean:
            if Path(file_path).exists():
                try:
                    Path(file_path).unlink()
                    print(f"✅ Removed {description}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"❌ Error removing {description}: {e}")
        
        for save_file in save_files:
            try:
                save_file.unlink()
                print(f"✅ Removed {save_file.name}")
                cleaned_count += 1
            except Exception as e:
                print(f"❌ Error removing {save_file.name}: {e}")
        
        print(f"\n🎉 Cleanup complete! Removed {cleaned_count} files.")
    else:
        print("❌ Cleanup cancelled.")

def main():
    """Main launcher function"""
    if not check_requirements():
        input("\nPress Enter to exit...")
        return
    
    while True:
        try:
            display_banner()
            show_menu()
            
            choice = input("Select an option (1-6): ").strip()
            
            if choice == "1":
                start_game()
            elif choice == "2":
                view_documentation()
            elif choice == "3":
                check_system()
            elif choice == "4":
                view_statistics()
            elif choice == "5":
                clean_data()
            elif choice == "6":
                print("\n👋 Thanks for using the Adventure Game Launcher!")
                break
            else:
                print("❌ Invalid option. Please choose 1-6.")
            
            if choice != "1":  # Don't pause after starting game
                input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Launcher interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Launcher error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()