'''import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_email(subject: str, purpose: str, sender: str = "User") -> str:
    prompt = f"Write a professional email about '{subject}'. Purpose: {purpose}. Sender: {sender}."
    try:
        # Use the correct model name here:
        model = genai.GenerativeModel("models/gemini-2.5-pro")  # <-- update this
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        return f"Error generating email: {e}"
'''
'''import os
from dotenv import load_dotenv
import google.generativeai as genai

# --- Load .env using absolute path (works inside Streamlit) ---
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

# --- Configure Gemini API ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file.")
genai.configure(api_key=api_key)

def generate_email(subject: str):
    """
    Generate a professional email using only the subject.
    Automatically includes greeting, body, and signature.
    """
    if not subject:
        return "⚠️ Please enter a subject to generate an email."

    try:
        # Use the latest Gemini model (as of 2025)
        model = genai.GenerativeModel("models/gemini-2.5-pro")

        prompt = f"""
        You are a professional email writer. 
        Write a complete, well-formatted email based on the subject below.

        Subject: "{subject}"

        The email should include:
        - A polite greeting
        - A short, relevant body (2–4 sentences)
        - A professional closing
        - A signature (Hariom)

        The tone should match the subject automatically 
        (formal for work-related topics, friendly for personal topics).
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"⚠️ Error generating email: {e}"'''
        
import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_email(subject, context="", sender="Hariom"):
    """
    Generate a professional email using Gemini.
    Supports both manual and auto-email generation.
    """
    try:
        prompt = (
            f"Write a professional email from {sender} on the topic: '{subject}'.\n\n"
            f"Context or purpose:\n{context}\n\n"
            "Make it clear, polite, and well-structured. "
            "Include greetings and a proper closing."
        )

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error generating email: {e}"

