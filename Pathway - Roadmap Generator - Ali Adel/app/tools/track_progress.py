def track_progress(plan, session):
    total_items, completed_items = 0, 0

    for week in plan:
        week_num = week.get("week_number", 0)

        # Topics
        for i, topic in enumerate(week.get("topics", [])):
            key = f"w{week_num}_topic_{i}"
            checked = session.get(key, False)
            topic["completed"] = checked
            total_items += 1
            if checked:
                completed_items += 1

        # Tasks
        for i, task in enumerate(week.get("tasks", [])):
            key = f"w{week_num}_task_{i}"
            checked = session.get(key, False)
            task["completed"] = checked
            total_items += 1
            if checked:
                completed_items += 1

    return total_items, completed_items
