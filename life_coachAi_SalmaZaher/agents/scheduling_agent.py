from datetime import datetime, timedelta

def schedule_tasks(tasks):
    # Default time ranges
    time_blocks = {
        "morning": (9, 12),
        "afternoon": (13, 17),
        "evening": (18, 21)
    }

    schedule = []
    used_slots = set()

    for task in tasks:
        name = task.get("name", "Unnamed Task")
        duration = task.get("duration", 45)
        print("DEBUG - scheduling this task:", task)
        preferred = task.get("preferred_time", "morning")

        start_hour, end_hour = time_blocks.get(preferred, time_blocks["morning"])
        slot = find_available_slot(start_hour, end_hour, duration, used_slots)

        if slot:
            start_time, end_time = slot
            schedule.append({
                "task": name,
                "start": start_time.strftime("%H:%M"),
                "end": end_time.strftime("%H:%M")
            })
        else:
            schedule.append({
                "task": name,
                "start": "No available slot",
                "end": ""
            })

    return schedule

def find_available_slot(start_hour, end_hour, duration_minutes, used_slots):
    """
    Returns the first available time slot of given duration between start_hour and end_hour
    avoiding used_slots.
    """
    current_time = datetime.strptime(f"{start_hour:02}:00", "%H:%M")

    while current_time.hour < end_hour:
        end_time = current_time + timedelta(minutes=duration_minutes)

        # Prevent overlapping
        overlap = False
        for used_start, used_end in used_slots:
            if (current_time < used_end and end_time > used_start):
                overlap = True
                break

        if not overlap and end_time.hour <= end_hour:
            used_slots.add((current_time, end_time))
            return current_time, end_time

        current_time += timedelta(minutes=15)  # try next slot

    return None

