import json

def extract_json_list(text: str):
    """
    Extracts and parses the content between the first '[' and last ']'
    from the given text. Returns a list of strings or an empty list.
    """
    try:
        start = text.find('[')
        end = text.rfind(']')
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Could not find a valid JSON array.")

        json_str = text[start:end+1]
        data = json.loads(json_str)

        if isinstance(data, list) and all(isinstance(item, str) for item in data):
            return data
        else:
            raise ValueError("Parsed data is not a list of strings.")

    except Exception as e:
        print(f"[JSON Extractor] Failed to parse JSON array: {e}")
        print(f"Raw input (truncated): {text[:300]}")
        return "No questions"

def extract_json_plan(text: str):
    """
    Extracts and parses the content between the first '[' and last ']'
    from the given text. Returns a list of strings or an empty list.
    """
    try:
        start = text.find('[')
        end = text.rfind(']')
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Could not find a valid JSON array.")

        json_str = text[start:end+1]
        data = json.loads(json_str)

        return data

    except Exception as e:
        print(f"[JSON Extractor] Failed to parse JSON array: {e}")
        print(f"Raw input: {text}")
        return "No questions"

def normalize_plan_structure(plan):
    """
    Given a list of week dictionaries, enhance each topic/task item
    with 'completed': False and wrap them as structured dicts.
    Returns the normalized plan or an empty list if an error occurs.
    """
    try:
        normalized = []

        for week in plan:
            new_week = {
                "week_number": week.get("week_number"),
                "objective": week.get("objective"),
                "topics": [{"name": topic, "completed": False} for topic in week.get("topics", [])],
                "tasks": [{"description": task, "completed": False} for task in week.get("tasks", [])]
            }
            normalized.append(new_week)

        return normalized

    except Exception as e:
        print(f"[normalize_plan_structure] Error: {e}")
        return []


def validate_plan_schema(plan: list) -> bool:
    """
    Validates that the plan matches the expected structure:
    A list of weeks with week_number, objective, topics[], tasks[]
    Each topic/task must be a dict with required fields.
    """
    if not isinstance(plan, list):
        return False

    for week in plan:
        if not isinstance(week, dict):
            return False
        if "week_number" not in week or "objective" not in week:
            return False
        if not isinstance(week.get("topics", []), list) or not isinstance(week.get("tasks", []), list):
            return False

        for topic in week["topics"]:
            if not isinstance(topic, dict) or "name" not in topic or "completed" not in topic:
                return False

        for task in week["tasks"]:
            if not isinstance(task, dict) or "description" not in task or "completed" not in task:
                return False

    return True
