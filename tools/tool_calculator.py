from langchain.tools import tool # Learn about this library later

@tool
def calculator_tool(input: str) -> str:
    """Performs basic math calculations, e.g., '24 * 7'."""
    try:
        return str(eval(input))
    except Exception:
        return "Invalid math expression."
