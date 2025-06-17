# agents/planning_agent.py


from datetime import datetime
import difflib

def match_goal(goal):
    goal = goal.lower()
    possibilities = {
        "Attend lectures": ["lecture", "lectures", "class"],
        "Go out": ["go out", "goout", "outside", "hangout", "walk"],
        "Workout session": ["exercise", "workout", "gym", "train"]
    }

    for task, keywords in possibilities.items():
        for keyword in keywords:
            if keyword in goal or difflib.get_close_matches(keyword, goal.split(), cutoff=0.7):
                return task
    return None

def plan_tasks(user_goals, energy_level):
    tasks = []
    for goal in user_goals:
        matched = match_goal(goal)
        if matched == "Attend lectures":
            tasks.append({"task": "Attend lectures", "duration": 180})
        elif matched == "Go out":
            tasks.append({"task": "Go out", "duration": 60})
        elif matched == "Workout session":
            tasks.append({"task": "Workout session", "duration": 60})
        else:
            tasks.append({"task": f"Work on: {goal}", "duration": 45})

    return tasks



