import requests
import os
from dotenv import load_dotenv
from langchain.tools import tool 
load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

@tool
def weather_tool(city: str) -> str:
    """
    Get current weather for a city using OpenWeather API.

    Parameters:
        city (str): City name.

    Returns:
        str: Weather summary like
        "It's 25°C with clear skies in Jakarta."

    Usage:
        Ask about current weather or travel info.

    Notes:
        Requires internet and a valid API key.
    """

    try:
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params ={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]

        return f"[weather] It's {temperature}°C with {weather} in {city}."
    
    except requests.RequestException as e:
        if response.status_code == 404:
            return f"City '{city}' not found."
        return f"HTTP Error: {e}"
    except Exception as e:
        return f"Error retrieving weather data: {e}"

# For testing pupose, the result will be printed directly
if __name__ == "__main__":
    city = input("Enter city: ")
    print(weather_tool(city))


