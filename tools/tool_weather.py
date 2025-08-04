from langchain.tools import tool # Learn about this library later

@tool
def weather_tool(input: str) -> str:
    """Returns current weather for a city."""
    if "paris" in input.lower():
        return "It's 26°C and sunny in Paris."
    return "It's 24°C and cloudy in San Francisco."
