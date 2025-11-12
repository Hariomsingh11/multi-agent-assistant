import os
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from agents.email_agent_simulated import send_email  # Reuse your simulated sender

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def auto_email(topic, recipient, sender="Hariom", context=""):
    """
    Generate and send an email automatically using Gemini,
    then save it to local JSON inbox (simulated send).
    """
    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        prompt = (
            f"Write a professional email about '{topic}'.\n"
            f"Sender: {sender}\n"
            f"Recipient: {recipient}\n"
            f"Context: {context}\n\n"
            f"The email should have a subject and body, concise and natural tone."
        )

        response = model.generate_content(prompt)
        email_text = response.text.strip()

        # 🧠 Separate subject and body if Gemini provides both
        subject_line = "No Subject"
        if "Subject:" in email_text:
            parts = email_text.split("Subject:", 1)[1].strip().split("\n", 1)
            subject_line = parts[0].strip()
            body = parts[1].strip() if len(parts) > 1 else ""
        else:
            body = email_text

        # ✅ Use simulated send_email (this also saves to JSON)
        send_result = send_email(recipient, subject_line, body)

        # ✅ Explicitly ensure auto emails are saved in simulated_inbox.json
        inbox_file = "simulated_inbox.json"
        email_data = {
            "to": recipient,
            "subject": subject_line,
            "body": body,
            "sender": sender,
            "topic": topic,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "auto"
        }

        if os.path.exists(inbox_file):
            with open(inbox_file, "r") as f:
                inbox = json.load(f)
        else:
            inbox = []

        inbox.append(email_data)
        with open(inbox_file, "w") as f:
            json.dump(inbox, f, indent=4)

        return f"✅ Auto email generated and sent to {recipient}.\nSubject: {subject_line}"

    except Exception as e:
        return f"⚠️ Error sending email: {e}"
