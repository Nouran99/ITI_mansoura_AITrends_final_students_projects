def log_user_input(reflection, goals, energy):
    with open("user_log.txt", "a", encoding="utf-8") as f:  # ✅ Add encoding="utf-8"
        f.write(f"\n📝 Reflection: {reflection}\n")
        f.write(f"🎯 Goals: {', '.join(goals)}\n")
        f.write(f"⚡ Energy: {energy}\n")
        f.write("-" * 40 + "\n")
