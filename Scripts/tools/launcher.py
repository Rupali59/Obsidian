#!/usr/bin/env python3
"""
GitHub Metrics Launcher
Quick access to common tasks
"""

import sys
import subprocess
from pathlib import Path

def show_menu():
    """Show the main menu"""
    print("🚀 GitHub Metrics Launcher")
    print("=" * 30)
    print("1. Capture today's data")
    print("2. List all repositories")
    print("3. Run August capture")
    print("4. Run Year capture")
    print("5. Setup system")
    print("6. Log management")
    print("7. Exit")
    print()

def run_command(command, description):
    """Run a command with description"""
    print(f"🔄 {description}...")
    print("-" * 40)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        print("✅ Completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print()

def main():
    """Main function"""
    while True:
        show_menu()
        choice = input("Select option (1-6): ").strip()
        
        if choice == "1":
            run_command("python3 ../scripts/capture_today.py", "Capturing today's GitHub data")
        elif choice == "2":
            run_command("python3 list_all_repos.py", "Listing all repositories")
        elif choice == "3":
            run_command("cd ../parallel && ./run_august.sh", "Running August capture")
        elif choice == "4":
            run_command("cd ../parallel && ./run_year.sh", "Running Year capture")
        elif choice == "5":
            run_command("python3 setup.py", "Setting up the system")
        elif choice == "6":
            show_log_menu()
        elif choice == "7":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-7.")
        
        input("\nPress Enter to continue...")
        print()

def show_log_menu():
    """Show the log management menu"""
    print("\n📊 Log Management")
    print("=" * 20)
    print("1. Show log statistics")
    print("2. Clean up old logs")
    print("3. Back to main menu")
    print()
    
    while True:
        choice = input("Select option (1-3): ").strip()
        
        if choice == "1":
            run_command("python3 log_manager.py . stats", "Showing log statistics")
        elif choice == "2":
            run_command("python3 log_manager.py . cleanup", "Cleaning up old logs")
        elif choice == "3":
            break
        else:
            print("❌ Invalid choice. Please select 1-3.")
        
        input("\nPress Enter to continue...")
        print()

if __name__ == "__main__":
    main()
