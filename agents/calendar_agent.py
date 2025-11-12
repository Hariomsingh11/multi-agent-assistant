import json, os
from datetime import datetime, timedelta

DATA_FILE = "calendar_data.json"

# ------------------------------
# Utility
# ------------------------------
def load_events():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_events(events):
    with open(DATA_FILE, "w") as f:
        json.dump(events, f, indent=2)

# ------------------------------
# Core Functions
# ------------------------------
def add_event(title, date_str, time_str, description=""):
    events = load_events()
    dt_str = f"{date_str} {time_str}"

    # Prevent duplicate meetings
    for e in events:
        if e["title"].lower() == title.lower() and e["datetime"] == dt_str:
            return f"⚠️ Meeting '{title}' already exists at {dt_str}."

    event = {
        "id": len(events) + 1,
        "title": title,
        "datetime": dt_str,
        "description": description,
    }
    events.append(event)
    save_events(events)
    return f"✅ Meeting '{title}' scheduled for {dt_str}"

def parse_and_add_event(text):
    """Parse natural language commands like 'Schedule meeting tomorrow at 10 AM with John about project'."""
    now = datetime.now()
    if "tomorrow" in text.lower():
        date = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        date = now.strftime("%Y-%m-%d")

    # Extract time
    import re
    match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(AM|PM|am|pm)?", text)
    hour = 10
    minute = 0
    if match:
        hour = int(match.group(1))
        if match.group(3) and match.group(3).lower() == "pm" and hour < 12:
            hour += 12
        if match.group(2):
            minute = int(match.group(2))

    time_str = f"{hour:02d}:{minute:02d}"
    title = "Voice Scheduled Meeting"
    if "with" in text:
        title = text.split("with", 1)[1].split("about")[0].strip().title()
    desc = "Auto-created from voice input"
    if "about" in text:
        desc = text.split("about", 1)[1].strip().capitalize()

    return add_event(title, date, time_str, desc)

def list_events():
    events = load_events()
    if not events:
        return "📭 No meetings scheduled."
    out = "📅 Upcoming Meetings:\n"
    for e in events:
        out += f"{e['id']}. {e['title']} — {e['datetime']} — {e.get('description','')}\n"
    return out

def list_events_next(minutes=10):
    events = load_events()
    now = datetime.now()
    upcoming = []
    for e in events:
        dt = datetime.strptime(e["datetime"], "%Y-%m-%d %H:%M")
        if 0 <= (dt - now).total_seconds() <= minutes * 60:
            upcoming.append(e)
    return upcoming

def delete_event(event_id):
    events = load_events()
    events = [e for e in events if e["id"] != event_id]
    save_events(events)
    return f"🗑️ Meeting ID {event_id} deleted."

def clear_all_events():
    save_events([])
    return "🧹 All meetings cleared."

# ------------------------------
# Weekly Summary
# ------------------------------
def list_events_week():
    events = load_events()
    now = datetime.now()
    week_ahead = now + timedelta(days=7)
    return [e for e in events if now <= datetime.strptime(e["datetime"], "%Y-%m-%d %H:%M") <= week_ahead]

def weekly_summary_text():
    events = list_events_week()
    if not events:
        return "No meetings scheduled for this week."
    summary = "🗓 This week's meetings:\n"
    for e in events:
        summary += f"- {e['title']} at {e['datetime']}\n"
    return summary

def google_calendar_sync_placeholder():
    """Placeholder for future Google Calendar API sync."""
    return "🧩 Google Calendar sync feature coming soon!"
