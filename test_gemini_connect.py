import os
import streamlit as st
import speech_recognition as sr
import simpleaudio as sa
import requests
from gtts import gTTS
from dotenv import load_dotenv
import google.generativeai as genai

# --- Importing Agents ---
from agents.weather_agent import get_weather
from agents.browser_agent import search_web
from agents.email_agent_simulated import send_email, read_inbox
from agents.email_generator_gemini import generate_email
from agents.focusflow_agent import add_task, list_tasks, complete_task, delete_task

# --- Load environment variables ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ----------------- Helper Functions -----------------
from gtts import gTTS
import streamlit as st
import os

def speak(text):
    """Play speech inside the Streamlit browser"""
    if not text:
        return
    tts = gTTS(text)
    tts.save("voice.mp3")
    with open("voice.mp3", "rb") as f:
        audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3")
    os.remove("voice.mp3")




def check_api_status():
    """Check connectivity and API key status"""
    statuses = {}

    # Gemini API check
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            model = genai.GenerativeModel("gemini-pro")
            model.generate_content("ping")
            statuses["Gemini API"] = "✅ Connected"
        except Exception:
            statuses["Gemini API"] = "⚠️ Key found but connection failed"
    else:
        statuses["Gemini API"] = "❌ No key found"

    # OpenWeather API check
    weather_key = os.getenv("OPENWEATHER_API_KEY")
    if weather_key:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={weather_key}"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                statuses["OpenWeather API"] = "✅ Connected"
            else:
                statuses["OpenWeather API"] = "⚠️ Invalid or inactive key"
        except Exception:
            statuses["OpenWeather API"] = "⚠️ Connection failed"
    else:
        statuses["OpenWeather API"] = "❌ No key found"

    # Browser (DuckDuckGo)
    try:
        res = requests.get("https://duckduckgo.com", timeout=5)
        statuses["Browser Agent"] = "✅ Online" if res.status_code == 200 else "⚠️ Unreachable"
    except:
        statuses["Browser Agent"] = "❌ Offline"

    # Local Agents
    statuses["Email Agent"] = "🗂️ Local mode"
    statuses["FocusFlow Agent"] = "🧠 Local mode"
    return statuses


# ----------------- Streamlit App Setup -----------------
st.set_page_config(page_title="Multi-Agent Voice + Text Assistant", layout="wide")

# --- Title and Status Overview ---
st.title("🤖 Multi-Agent Voice + Text Assistant")
st.markdown("Ask me about weather 🌦, search 🔍, emails 💌, or tasks 🧠!")

# --- System Status ---
st.markdown("### 🩺 System Status Overview")
statuses = check_api_status()
cols = st.columns(2)
i = 0
for name, status in statuses.items():
    cols[i % 2].markdown(f"**{name}:** {status}")
    i += 1
st.divider()

# ----------------- Sidebar Navigation -----------------
st.sidebar.title("🧭 Navigation")
section = st.sidebar.radio(
    "Choose a section:",
    ["🌦 Weather", "🔍 Browser Search", "💌 Email Generator", "📧 Email Agent", "🧠 FocusFlow"],
    index=0
)

st.markdown("## 💬 Multi-Agent Control Panel")

# ----------------- Weather Agent -----------------
if section == "🌦 Weather":
    st.subheader("🌤 Weather Agent")
    city = st.text_input("Enter city name:")
    if st.button("Get Weather"):
        result = get_weather(city)
        st.success(result)
        if st.checkbox("🔊 Speak result"):
            speak(result)

# ----------------- Browser Agent -----------------
elif section == "🔍 Browser Search":
    st.subheader("🔍 Browser Agent")
    query = st.text_input("Enter your search query:")
    if st.button("Search Web"):
        result = search_web(query)
        st.success(result)
        if st.checkbox("🔊 Speak result"):
            speak(result)


# ----------------- Email Generator (Gemini AI) -----------------
elif section == "💌 Email Generator":
    st.subheader("💌 AI Email Generator (Gemini)")
    subject = st.text_input("Enter the subject for your email:")

    if st.button("Generate Email"):
        result = generate_email(subject)
        st.text_area("Generated Email:", result, height=250)
        if st.checkbox("🔊 Read Email"):
            speak(result)



# ----------------- Email Agent (Local Simulated Inbox) -----------------
elif section == "📧 Email Agent":
    st.subheader("📧 Local Email Agent (Simulated Inbox)")
    choice = st.radio("Choose Action:", ["Send Email", "Read Inbox"])
    if choice == "Send Email":
        to = st.text_input("Recipient Email:")
        subject = st.text_input("Subject:")
        body = st.text_area("Body:")
        if st.button("Send"):
            result = send_email(to, subject, body)
            st.success(result)
    else:
        st.write("📬 Latest 5 Emails:")
        st.text(read_inbox())

# ----------------- FocusFlow Agent -----------------
'''
elif section == "🧠 FocusFlow":
    st.subheader("🧠 FocusFlow Task Manager")
    action = st.selectbox("Choose action:", ["View Tasks", "Add Task", "Complete Task", "Delete Task"])
    if action == "View Tasks":
        show_completed = st.checkbox("Show completed too")
        if st.button("View Tasks"):
            st.text(list_tasks(show_completed))
    elif action == "Add Task":
        new_task = st.text_input("New Task:")
        if st.button("Add Task"):
            st.success(add_task(new_task))
    elif action == "Complete Task":
        task_id = st.number_input("Task ID to mark complete:", min_value=1, step=1)
        if st.button("Mark Complete"):
            st.success(complete_task(int(task_id)))
    elif action == "Delete Task":
        task_id = st.number_input("Task ID to delete:", min_value=1, step=1)
        if st.button("Delete Task"):
            st.success(delete_task(int(task_id)))'''
            
    # ----------------- FocusFlow Agent -----------------
# ----------------- FocusFlow (Local + API) -----------------
elif section in ["🧠 FocusFlow (Local)", "🌐 FocusFlow (API)"]:
    if section == "🧠 FocusFlow (Local)":
        st.subheader("🧠 FocusFlow (Local JSON Mode)")
        st.info("Tasks are stored locally in focusflow_tasks.json.")
        from agents.focusflow_agent import add_task, list_tasks, complete_task, delete_task

    elif section == "🌐 FocusFlow (API)":
        st.subheader("🌐 FocusFlow (FastAPI Backend Mode)")
        st.info("Tasks are managed via FastAPI and stored in SQLite (focusflow.db).")
        from agents.focusflow_agent_api import add_task, list_tasks, complete_task, delete_task

    action = st.selectbox("Choose action:", ["View Tasks", "Add Task", "Complete Task", "Delete Task"])

    if action == "View Tasks":
        show_completed = st.checkbox("Show completed too")
        if st.button("View Tasks"):
            st.text(list_tasks(show_completed))

    elif action == "Add Task":
        new_task = st.text_input("New Task:")
        if st.button("Add Task"):
            st.success(add_task(new_task))

    elif action == "Complete Task":
        task_id = st.number_input("Task ID to mark complete:", min_value=1, step=1)
        if st.button("Mark Complete"):
            st.success(complete_task(int(task_id)))

    elif action == "Delete Task":
        task_id = st.number_input("Task ID to delete:", min_value=1, step=1)
        if st.button("Delete Task"):
            st.success(delete_task(int(task_id)))



# ----------------- Footer -----------------

st.sidebar.markdown("---")
st.sidebar.info("👨‍💻 Developed by Hariom • v1.0 🚀")
