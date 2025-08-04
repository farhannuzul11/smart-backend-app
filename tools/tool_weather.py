import requests
from typing import Optional
from langchain.tools import tool # Learn about this library later

API_KEY = "2e551eddc221109dc3c74d277f3df41d"

@tool
def weather_tool(city: str) -> str:
    """Get the current weather information for a given city.

    This tool queries a weather API to retrieve current weather details 
    (temperature, humidity, and weather condition) for the specified city. 
    You can specify the temperature unit as either "Celsius" or "Fahrenheit".

    Parameters:
        city (str): Name of the city to get the weather for.
        unit (str, optional): Unit of temperature. Accepts "Celsius" or "Fahrenheit".
                              Defaults to "Celsius".

    Returns:
        str: A human-readable summary of the current weather, such as:
             "In Jakarta, it is currently 31°C with clear skies and 70% humidity."

    Example:
        >>> get_current_weather("Jakarta", unit="Celsius")
        "In Jakarta, it is currently 31°C with clear skies and 70% humidity."

    Notes:
        - Ensure your system is connected to the internet.
        - The accuracy depends on the external weather API used.

    Category:
        Weather Tool

    Capabilities:
        - Informational
        - Stateless
        - Deterministic output (no randomness)

    Ideal for:
        - User queries about current weather
        - Travel apps or trip planners
        - Daily assistant summaries
    """
    # find the meaning why using """

    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params ={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        # Still dont understand this part
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        data = response.json()
        weather = data["weather"][0]["description"] #Still dont understand this part
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


