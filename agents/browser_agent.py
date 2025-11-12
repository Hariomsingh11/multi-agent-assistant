import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from duckduckgo_search import DDGS

# --- Load environment variables ---
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

# --- Configure Gemini ---
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    genai.configure(api_key=gemini_key)
else:
    print("⚠️ Warning: GEMINI_API_KEY missing in .env")

# --- GNews key (for headlines) ---
gnews_key = os.getenv("GNEWS_API_KEY")

def _gemini_summarize(prompt: str):
    """
    Try Gemini models in fallback order until one succeeds.
    """
    model_names = [
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro"
    ]
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content(prompt)
            if hasattr(response, "text"):
                return response.text.strip()
            elif isinstance(response, dict):
                return response.get("text", "").strip()
        except Exception as e:
            # Skip unsupported models and continue to next
            if "404" in str(e) or "not found" in str(e).lower():
                continue
            else:
                return f"❌ Gemini error ({name}): {e}"
    return "⚠️ No available Gemini model worked for summarization."

def search_web(query: str):
    """
    🔍 Smart Browser Agent:
    - Detects 'news' queries → uses GNews API
    - For general queries → uses DuckDuckGo + Gemini summarization
    - Auto-fallback for Gemini models
    """
    if not query:
        return "⚠️ Please enter a search query."

    query_lower = query.lower()

    # --- 📰 NEWS DETECTION ---
    if any(word in query_lower for word in ["news", "headline", "breaking", "latest"]):
        if not gnews_key:
            return "⚠️ Missing GNEWS_API_KEY in .env"

        try:
            country = "in" if "india" in query_lower else "us"
            url = f"https://gnews.io/api/v4/top-headlines?lang=en&country={country}&max=5&apikey={gnews_key}"
            res = requests.get(url, timeout=10)
            data = res.json()

            if not data.get("articles"):
                raise ValueError("No articles from GNews")

            articles = data["articles"]
            headlines = [
                f"{i+1}. {a.get('title', 'No title')} ({a.get('source', {}).get('name', '')})\n🔗 {a.get('url', '')}"
                for i, a in enumerate(articles)
            ]
            return "🗞️ **Top Headlines:**\n\n" + "\n\n".join(headlines)

        except Exception as e:
            print(f"⚠️ GNews failed: {e}")
            # Fallback: Gemini generate news summary
            if gemini_key:
                prompt = "Give me the top 5 latest global news headlines with 1-line summaries."
                return _gemini_summarize(prompt)
            return "⚠️ Could not fetch news — both GNews and Gemini failed."

    # --- 🌐 GENERAL SEARCH (DuckDuckGo + Gemini) ---
    try:
        with DDGS() as ddgs:
            results = [r["body"] for r in ddgs.text(query, max_results=5) if "body" in r]
        combined_info = "\n".join(results)

        if not combined_info:
            return "⚠️ No relevant results found."

        # Summarize via Gemini (with fallback)
        if gemini_key:
            prompt = f"Summarize concisely what you found about '{query}'.\n\n{combined_info}"
            return _gemini_summarize(prompt)
        else:
            return combined_info

    except Exception as e:
        return f"❌ Browser Agent Error: {e}"
