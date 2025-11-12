import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use latest Gemini model (change if needed)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Store chat history for users
chat_sessions = {}

def get_chat_response(user_id, user_input):
    """
    Maintains a session-based conversation using Gemini.
    """
    try:
        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])

        chat = chat_sessions[user_id]
        response = chat.send_message(user_input)
        return response.text.strip()

    except Exception as e:
        return f"⚠️ AI Error: {e}"
