from agents.logger_agent import log_user_input
from agents.feedback_agent import generate_feedback
# from agents.planning_agent import plan_tasks  # Optional
from agents.scheduling_agent import schedule_tasks

def main():
    # User input
    reflection = input("📝 How was your day?\n> ")
    goals_input = input("🎯 What are your top 2-3 goals for tomorrow? (comma-separated)\n> ")
    energy = input("⚡ When do you feel most productive? (morning/afternoon/evening)\n> ")

    # Clean and split goals
    goals = [g.strip() for g in goals_input.split(",")]

    # Log user input
    log_user_input(reflection, goals, energy)

    # Create task list
    tasks = []
    for goal in goals:
        tasks.append({
            "name": goal,
            "duration": 45,  # You can adjust this dynamically later
            "preferred_time": energy
        })

    print("DEBUG - tasks before scheduling:", tasks)

    # Schedule tasks directly (no planning agent needed here)
    schedule = schedule_tasks(tasks)

    # Feedback (make sure your function accepts 3 arguments)
    feedback = generate_feedback(reflection)


    # Output
    print("\n💬 Feedback from AI:\n", feedback)
    print("\n📅 Schedule for Tomorrow:")
    for task in schedule:
        print(f"⏰ {task['start']}–{task['end']} → {task['task']}")

if __name__ == "__main__":
    main()
