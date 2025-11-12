import os
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Local inbox storage
INBOX_FILE = "email_inbox.json"

# Create inbox file if missing
if not os.path.exists(INBOX_FILE):
    with open(INBOX_FILE, "w") as f:
        json.dump([], f)


# --- AI Email Generator ---
def generate_email(subject: str, purpose: str = "", sender: str = "Hariom"):
    """
    Generate a professional email using Gemini AI.
    """
    if not subject.strip():
        return "⚠️ Please enter a subject before generating."

    prompt = (
        f"Write a professional email about '{subject}'.\n"
        f"Context/Purpose: {purpose if purpose else 'General business communication'}.\n"
        f"Sender Name: {sender}.\n"
        f"Keep it short, polite, and structured (Subject, Greeting, Body, Closing)."
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error generating email: {e}"


# --- Local Send Email ---
def send_email(recipient: str, subject: str, body: str):
    """
    Simulate sending an email locally and store it in inbox JSON.
    """
    if not (recipient and subject and body):
        return "⚠️ Please fill all fields before sending."

    email = {
        "to": recipient,
        "subject": subject,
        "body": body,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(INBOX_FILE, "r+") as f:
            inbox = json.load(f)
            inbox.insert(0, email)
            f.seek(0)
            json.dump(inbox, f, indent=4)
        return f"✅ Email successfully sent to {recipient}!"
    except Exception as e:
        return f"❌ Error saving email: {e}"


# --- Read Inbox ---
def read_inbox(limit=5):
    """
    Read the most recent few emails from the local inbox.
    """
    if not os.path.exists(INBOX_FILE):
        return "📭 Inbox file missing."

    try:
        with open(INBOX_FILE, "r") as f:
            emails = json.load(f)
        if not emails:
            return "📭 No emails found."

        latest = emails[:limit]
        output = []
        for e in latest:
            output.append(
                f"📧 **To:** {e['to']}\n"
                f"**Subject:** {e['subject']}\n"
                f"**Time:** {e['timestamp']}\n\n"
                f"{e['body']}\n"
            )
        return "\n---\n".join(output)
    except Exception as e:
        return f"❌ Error reading inbox: {e}"
