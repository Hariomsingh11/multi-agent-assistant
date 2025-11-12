import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather(city: str):
    """
    Fetch current weather data for a given city using WeatherAPI.com.
    """
    api_key = os.getenv("WEATHERAPI_KEY")
    if not api_key:
        return "❌ WEATHERAPI_KEY not found in .env file."

    if not city:
        return "⚠️ Please enter a valid city name."

    try:
        # Make the API request
        url = f"http://api.weatherapi.com/v1/current.json"
        params = {"key": api_key, "q": city, "aqi": "no"}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        # Handle errors from API
        if "error" in data:
            return f"⚠️ Error: {data['error']['message']}"

        # Extract relevant weather info
        location = data["location"]["name"]
        country = data["location"]["country"]
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind = data["current"]["wind_kph"]

        # Build user-friendly response
        return (
            f"🌤️ Weather in {location}, {country}:\n"
            f"Condition: {condition}\n"
            f"Temperature: {temp}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind: {wind} kph"
        )

    except Exception as e:
        return f"❌ Error fetching weather: {e}"
        
'''import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather(city: str):
    """
    Fetch live weather data for a given city using OpenWeather API.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "❌ OPENWEATHER_API_KEY not found in .env file."
    if not city:
        return "⚠️ Please enter a valid city name."

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric"}
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        # Handle errors
        if res.status_code != 200:
            return f"⚠️ Error: {data.get('message', 'Invalid response from OpenWeather')}"

        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        city_name = data["name"]
        country = data["sys"]["country"]

        return (
            f"🌦 Weather in {city_name}, {country}:\n"
            f"Condition: {weather}\n"
            f"Temperature: {temp}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} m/s"
        )

    except Exception as e:
        return f"❌ Error fetching weather data: {e}"'''

