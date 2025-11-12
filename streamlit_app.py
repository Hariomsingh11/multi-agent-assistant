import os
import time
import tempfile
import requests
import streamlit as st
from gtts import gTTS
from dotenv import load_dotenv
import google.generativeai as genai

# --- Import Agents ---
from agents.weather_agent import get_weather
from agents.email_agent_simulated import send_email, read_inbox
from agents.email_generator_gemini import generate_email
from agents.chatbot_agent import get_chat_response

# --- Load environment variables ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Initialize session state ---
if "speak_text" not in st.session_state:
    st.session_state.speak_text = None

# ----------------- Helper Functions -----------------
def speak(text):
    """Convert text to speech and play inside Streamlit"""
    if not text:
        st.warning("⚠️ No text to speak.")
        return
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts = gTTS(text)
            tts.save(tmpfile.name)
            st.audio(tmpfile.name, format="audio/mp3")
    except Exception as e:
        st.error(f"❌ Speech error: {e}")

# ----------------- Streamlit App Setup -----------------
st.set_page_config(page_title="Multi-Agent Voice + Text Assistant", layout="wide")

# --- Modern Header ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;800&display=swap');
    body {
        background-color: #0E1117;
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 55px;
        font-weight: 800;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 3s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #00C9FF; }
        to { text-shadow: 0 0 30px #92FE9D; }
    }
    .subtext {
        text-align: center;
        font-size: 18px;
        color: #BBBBBB;
        margin-bottom: 20px;
        font-style: italic;
    }
    .divider {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #00C9FF, #92FE9D);
        margin: 10px 0 30px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🤖 Multi-Agent Voice + Text Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Talk, Type, and Automate — Your Personal AI Hub 💡</p>", unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ----------------- Sidebar Navigation -----------------
st.sidebar.title("🧭 Navigation")
section = st.sidebar.radio(
    "Choose a section:",
    [
        "🌦 Weather",
        "💌 Email Generator",
        "📧 Email Agent",
        "📤 Auto Email Agent",
        "📆 Calendar Assistant",
        "🤖 Chatbot"
    ],
    index=0
)

st.markdown("## 💬 Multi-Agent Control Panel")

# ----------------- Weather Agent -----------------
if section == "🌦 Weather":
    st.subheader("🌤 Weather Agent")
    city = st.text_input("Enter city name:")
    if st.button("Get Weather"):
        result = get_weather(city)
        st.session_state.speak_text = result
        st.success(result)
    if st.session_state.speak_text and st.checkbox("🔊 Speak result"):
        speak(st.session_state.speak_text)

# ----------------- Email Generator -----------------
elif section == "💌 Email Generator":
    st.subheader("💌 AI Email Generator (Gemini)")
    subject = st.text_input("Enter the subject for your email:")
    if st.button("Generate Email"):
        result = generate_email(subject)
        st.session_state.speak_text = result
        st.text_area("Generated Email:", result, height=250)
    if st.session_state.speak_text and st.checkbox("🔊 Read Email"):
        speak(st.session_state.speak_text)

# ----------------- Email Agent (Simulated Inbox) -----------------
elif section == "📧 Email Agent":
    st.subheader("📧 Local Email Agent (Simulated Inbox)")
    choice = st.radio("Choose Action:", ["Send Email", "Read Inbox"])

    if choice == "Send Email":
        to = st.text_input("Recipient Email:")
        subject = st.text_input("Subject:")
        body = st.text_area("Body:")
        if st.button("Send"):
            result = send_email(to, subject, body)
            st.session_state.speak_text = result
            st.success(result)

    elif choice == "Read Inbox":
        st.write("📬 Latest 5 Emails:")
        result = read_inbox()
        st.session_state.speak_text = result
        st.text(result)

    if st.session_state.speak_text and st.checkbox("🔊 Speak result"):
        speak(st.session_state.speak_text)

# ----------------- Auto Email Agent -----------------
elif section == "📤 Auto Email Agent":
    st.subheader("📤 Automated Email Sender (AI-Powered)")
    st.markdown("Generate and send emails automatically using Gemini AI + Local Email Agent 💡")
    from agents.auto_email_agent import auto_email
    topic = st.text_input("Enter topic (e.g., 'Project Update', 'Daily Report'):")
    recipient = st.text_input("Recipient Email:")
    sender = st.text_input("Sender Name:", "Hariom")
    context = st.text_area("Optional Context:", "Add details or bullet points here.")
    if st.button("🚀 Generate and Send Email"):
        with st.spinner("Generating and sending email..."):
            result = auto_email(topic, recipient, sender, context)
        st.success(result)

# ----------------- Calendar Assistant -----------------
elif section == "📆 Calendar Assistant":
    st.subheader("📆 Smart Calendar & Meeting Assistant")

    from agents.calendar_agent import (
        add_event,
        parse_and_add_event,
        list_events,
        list_events_next,
        delete_event,
        clear_all_events,
        weekly_summary_text
    )

    if "reminder_thread_started" not in st.session_state:
        st.session_state.reminder_thread_started = False

    action = st.selectbox("Choose an action:", [
        "View Meetings", "Add Meeting", "Voice Schedule", "Delete Meeting", "Weekly Summary", "Clear All"
    ])

    if action == "Add Meeting":
        st.markdown("### 📝 Schedule a New Meeting")
        title = st.text_input("Meeting Title:")
        date = st.date_input("Date:")
        time_input = st.time_input("Time:")
        desc = st.text_area("Description (optional):")
        if st.button("📅 Create Meeting"):
            msg = add_event(title, date.strftime("%Y-%m-%d"), time_input.strftime("%H:%M"), desc)
            st.success(msg)

    elif action == "Voice Schedule":
        import speech_recognition as sr
        st.markdown("### 🎤 Schedule by Voice / Natural Language")
        if st.button("🎧 Start Listening"):
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    st.info("🎙 Listening... Speak now.")
                    audio = r.listen(source, timeout=8)
                    text = r.recognize_google(audio)
                    st.success(f"You said: {text}")
                    msg = parse_and_add_event(text)
                    st.success(msg)
            except Exception as e:
                st.error(f"Voice error: {e}")

    elif action == "View Meetings":
        if st.button("👀 Show Upcoming Meetings"):
            st.text(list_events())

    elif action == "Weekly Summary":
        summary = weekly_summary_text()
        st.text_area("🗓 Weekly Summary", summary, height=200)
        if st.button("🔊 Speak Summary"):
            speak(summary)

    elif action == "Delete Meeting":
        eid = st.number_input("Meeting ID:", min_value=1, step=1)
        if st.button("🗑️ Delete"):
            st.warning(delete_event(int(eid)))

    elif action == "Clear All":
        if st.button("🧹 Clear All Meetings"):
            st.warning(clear_all_events())

# ----------------- Chatbot -----------------
elif section == "🤖 Chatbot":
    st.subheader("💬 Voice-Enabled Chatbot")
    import speech_recognition as sr

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("💬 Type or Speak:", key="chat_input")

    if st.button("🎤 Speak"):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                st.info("🎧 Listening...")
                audio = r.listen(source, timeout=8)
                text = r.recognize_google(audio)
                st.success(f"🗣 You said: {text}")
                user_input = text
        except Exception as e:
            st.warning(f"🎤 Voice error: {e}")

    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        reply = get_chat_response("hariom_user", user_input)
        st.session_state.chat_history.append(("Bot", reply))
        st.markdown(f"**🤖 Bot:** {reply}")
        speak(reply)

    st.markdown("### 🧠 Conversation History")
    for role, msg in st.session_state.chat_history:
        st.markdown(f"**{role}:** {msg}")

# ----------------- Footer -----------------
st.sidebar.markdown("---")
if st.sidebar.button("🎤 Test Voice"):
    speak("Hello Hariom! Your multi-agent assistant is running perfectly.")
st.sidebar.info("👨‍💻 Developed by Hariom • v2.1 🚀")
