# main.py - Main Application Runner
import sys
import os

def main():
    """Main function to choose between CLI and Web interface"""
    print("="*60)
    print("🤖 AI Assistant - Choose Your Interface")
    print("="*60)
    print("1. 💻 Command Line Interface (CLI)")
    print("2. 🌐 Web Application")
    print("3. 🚪 Exit")
    print("="*60)
    
    while True:
        try:
            choice = input("\nSelect an interface (1-3): ").strip()
            
            if choice == '1':
                print("\n🚀 Starting CLI Assistant...")
                from cli_assistant import run_cli
                run_cli()
                break
                
            elif choice == '2':
                print("\n🚀 Starting Web Assistant...")
                try:
                    from web_app import run_web_app
                    run_web_app()
                except ImportError:
                    print("❌ Flask is not installed!")
                    print("Install it using: pip install flask")
                    print("Then try again.")
                break
                
            elif choice == '3':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()