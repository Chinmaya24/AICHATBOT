# cli_assistant.py - Command Line Interface version
from ai_assistant import AIAssistant

def run_cli():
    """Command Line Interface version of the AI Assistant"""
    assistant = AIAssistant()
    print("="*60)
    print("🤖 Welcome to Your AI Assistant!")
    print("="*60)
    
    while True:
        print("\n📋 Available Functions:")
        print("1. 🧠 Answer Questions")
        print("2. 📄 Summarize Text")
        print("3. ✨ Generate Creative Content")
        print("4. 📚 Study Tips")
        print("5. 📊 View Feedback Statistics")
        print("6. 🚪 Exit")
        
        try:
            choice = input("\n🔤 Select an option (1-6): ").strip()
            
            if choice == '6':
                print("\n👋 Thank you for using AI Assistant! Goodbye!")
                break
            
            elif choice == '5':
                # Show feedback statistics
                total_feedback = len(assistant.feedback_data)
                if total_feedback == 0:
                    print("\n📈 No feedback data available yet.")
                else:
                    helpful_count = sum(1 for f in assistant.feedback_data if f['helpful'])
                    helpful_rate = (helpful_count / total_feedback) * 100
                    print(f"\n📈 Feedback Statistics:")
                    print(f"   Total responses: {total_feedback}")
                    print(f"   Helpful responses: {helpful_count} ({helpful_rate:.1f}%)")
                    
                    # Function breakdown
                    function_stats = {}
                    for f in assistant.feedback_data:
                        func = f['function_type']
                        if func not in function_stats:
                            function_stats[func] = {'total': 0, 'helpful': 0}
                        function_stats[func]['total'] += 1
                        if f['helpful']:
                            function_stats[func]['helpful'] += 1
                    
                    print("\n   📊 By function:")
                    for func, stats in function_stats.items():
                        rate = (stats['helpful'] / stats['total']) * 100
                        print(f"   • {func}: {stats['helpful']}/{stats['total']} ({rate:.1f}%)")
                continue
            
            elif choice in ['1', '2', '3', '4']:
                if choice == '1':
                    print("\n❓ Ask me any question!")
                    print("Examples: 'What is the capital of France?', 'What is 15 + 27?'")
                    user_input = input("Your question: ").strip()
                    if not user_input:
                        print("❌ Please provide a question.")
                        continue
                    
                    print("\n🤔 Processing your question...")
                    response = assistant.answer_question(user_input)
                    function_type = "Answer Question"
                
                elif choice == '2':
                    print("\n📝 Paste the text you want me to summarize:")
                    print("(Press Enter twice when finished)")
                    lines = []
                    while True:
                        line = input()
                        if line == "" and len(lines) > 0 and lines[-1] == "":
                            break
                        lines.append(line)
                    
                    user_input = "\n".join(lines).strip()
                    if not user_input:
                        print("❌ Please provide text to summarize.")
                        continue
                    
                    print("\n📊 Creating summary...")
                    response = assistant.summarize_text(user_input)
                    function_type = "Summarize Text"
                
                elif choice == '3':
                    print("\n🎨 What creative content would you like?")
                    print("Examples: 'Write a story about adventure', 'Create a poem about nature'")
                    user_input = input("Your creative prompt: ").strip()
                    if not user_input:
                        print("❌ Please provide a creative prompt.")
                        continue
                    
                    print("\n✨ Generating creative content...")
                    response = assistant.generate_creative_content(user_input)
                    function_type = "Generate Creative Content"
                
                elif choice == '4':
                    print("\n📚 Here are some effective study tips:")
                    user_input = "study tips request"
                    response = assistant.get_study_advice()
                    function_type = "Study Tips"
                
                # Display response
                print(f"\n{'='*60}")
                print("🤖 AI Assistant Response:")
                print(f"{'='*60}")
                print(response)
                print(f"{'='*60}")
                
                # Collect feedback
                print("\n💬 Feedback (helps improve the assistant):")
                while True:
                    helpful = input("Was this response helpful? (y/n): ").lower().strip()
                    if helpful in ['y', 'yes', '1', 'true']:
                        helpful_bool = True
                        break
                    elif helpful in ['n', 'no', '0', 'false']:
                        helpful_bool = False
                        break
                    else:
                        print("Please enter 'y' for yes or 'n' for no.")
                
                comment = input("Any additional comments (optional): ").strip()
                
                # Save feedback
                assistant.save_feedback(function_type, user_input, response, helpful_bool, comment)
                print("✅ Thank you for your feedback!")
            
            else:
                print("❌ Invalid choice. Please select 1-6.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    run_cli()