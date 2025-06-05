import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from crew import run_scheduling_process

load_dotenv()

def main():
    print("🤖 Smart Task Manager with AI Agents")
    print("Intelligent task scheduling system with deadline priority using CrewAI")
    print("-" * 50)
    
    # Check for API Key
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️ Error: Please add GROQ_API_KEY to your .env file")
        return
    
    # Use sample tasks or get user input
    use_sample = input("Would you like to use sample tasks? (y/n): ").lower().strip()
    
    if use_sample == 'y':
        tasks_content = """- Complete quarterly presentation (deadline: today 4pm, 2 hours)
- Client meeting preparation (deadline: tomorrow 9am, 1 hour)
- Review and respond to emails (deadline: today end of day, 30 minutes)
- Gym workout session (deadline: today evening, 45 minutes)
- Read development book chapter (deadline: this week, 1 hour)"""
    else:
        print("\n📝 Enter your tasks (format: Task name (deadline: when, duration))")
        print("Enter a blank line when finished:")
        
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        
        tasks_content = "\n".join(lines)
    
    # Display input tasks
    if tasks_content:
        print("\n📋 Input Tasks:")
        print(tasks_content)
        
        # Confirm processing
        confirm = input("\nGenerate to-do list with these tasks? (y/n): ").lower().strip()
        
        if confirm == 'y':
            print("\n🤖 Creating your to-do list...")
            
            # Run scheduling process
            result = run_scheduling_process(tasks_content)
            
            # Check for errors
            if "Rate limit reached" in str(result) or "Error" in str(result):
                print(f"⚠️ Error: {result}")
                print("💡 Please wait a few seconds and try again")
            else:
                # Success
                print("\n✅ Your to-do list is ready!")
                print("\n📋 Your Daily To-Do List")
                print("-" * 50)
                
                # Print the result
                print(result)
                
                # Also print this specific string
                print("also print this")
                
                # Ask if user wants to save the result
                save = input("\nSave to-do list to file? (y/n): ").lower().strip()
                
                if save == 'y':
                    filename = f"todo_list_{datetime.now().strftime('%Y%m%d')}.txt"
                    with open(filename, 'w') as f:
                        f.write(str(result))
                        f.write("\nalso print this")  # Also include this in the saved file
                    print(f"✅ Saved to {filename}")
    
    else:
        print("No tasks provided. Exiting.")

if __name__ == "__main__":
    main()
    print("\nThank you for using Smart Task Manager!")
    input("Press Enter to exit...")