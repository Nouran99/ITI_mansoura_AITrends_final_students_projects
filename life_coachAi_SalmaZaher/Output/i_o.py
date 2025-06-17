# utils/file_io.py
import os
from datetime import date

def save_to_markdown(log, feedback, goals, schedule, folder="logs"):
    today = date.today().isoformat()
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"{today}.md")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# 🧠 AI Life Coach Report – {today}\n\n")
        f.write("## 📝 Daily Reflection\n")
        f.write(log + "\n\n")

        f.write("## 💬 AI Feedback\n")
        f.write(feedback.strip() + "\n\n")

        f.write("## 🎯 Goals\n")
        for g in goals:
            f.write(f"- {g}\n")
        f.write("\n")

        f.write("## 📅 Schedule\n")
        for task in schedule:
            start, end = task['time_slot']
            f.write(f"- {start}–{end}: {task['task']}\n")

    return filepath
