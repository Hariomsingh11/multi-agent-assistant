import json
import os

TASK_FILE = os.path.join(os.path.dirname(__file__), "..", "focusflow_tasks.json")

def load_tasks():
    """Load tasks from JSON file"""
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(task):
    """Add new task if not already present"""
    task = task.strip()
    if not task:
        return "⚠️ Please enter a valid task."
    
    data = load_tasks()
    for t in data:
        if t["task"].lower() == task.lower():
            return f"⚠️ Task '{task}' already exists."

    data.append({"task": task, "done": False})
    save_tasks(data)
    return f"✅ Added: {task}"

def list_tasks(show_completed=False):
    """List all tasks (optionally show completed ones)"""
    data = load_tasks()
    if not data:
        return "📭 No tasks found."
    
    result = []
    for i, t in enumerate(data, 1):
        if not show_completed and t["done"]:
            continue
        status = "✅ done" if t["done"] else "⏳ pending"
        result.append(f"{i}. {t['task']} — {status}")
    return "\n".join(result)

def complete_task(task_id):
    """Mark task as complete"""
    data = load_tasks()
    if 0 < task_id <= len(data):
        data[task_id - 1]["done"] = True
        save_tasks(data)
        return f"🎯 Marked complete: {data[task_id - 1]['task']}"
    return "⚠️ Invalid task ID."

def delete_task(task_id):
    """Delete task"""
    data = load_tasks()
    if 0 < task_id <= len(data):
        removed = data.pop(task_id - 1)
        save_tasks(data)
        return f"🗑️ Deleted: {removed['task']}"
    return "⚠️ Invalid task ID."

def clear_all_tasks():
    """Clear all tasks"""
    save_tasks([])
    return "🧹 All tasks cleared!"
