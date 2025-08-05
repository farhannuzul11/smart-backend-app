import re
from langchain.tools import tool

@tool
def calculator_tool(input: str) -> str:
    """A simple calculator tool for basic arithmetic operations.
    
    Args:
        input (str): Mathematical expression or question. 
                    Examples: "12 * 7", "What is 15 + 25?", "Calculate 100 / 4"
    
    Returns:
        str: The calculated result
    """
    try:
        # Remove common question words and phrases
        cleaned_input = input.lower()
        cleaned_input = re.sub(r'\b(what\s+is|calculate|solve|find|compute)\b', '', cleaned_input)
        cleaned_input = re.sub(r'[?!]', '', cleaned_input)
        cleaned_input = cleaned_input.strip()
        
        # Replace word operators with symbols
        cleaned_input = re.sub(r'\btimes\b|\bmultiplied\s+by\b', '*', cleaned_input)
        cleaned_input = re.sub(r'\bdivided\s+by\b', '/', cleaned_input)
        cleaned_input = re.sub(r'\bplus\b|\badded\s+to\b', '+', cleaned_input)
        cleaned_input = re.sub(r'\bminus\b|\bsubtracted\s+from\b', '-', cleaned_input)
        
        # Extract numbers and operators
        tokens = re.findall(r'\d+(?:\.\d+)?|[\+\-\*/\(\)]', cleaned_input)
        
        if len(tokens) < 3:
            return "[calculator] Could not find a complete mathematical expression."
        
        # Join tokens to form expression
        expression = ''.join(tokens)
        
        # Validate expression
        if not re.match(r'^[\d\+\-\*/\(\)\.]+$', expression):
            return "[calculator] Invalid mathematical expression."
        
        # Evaluate
        result = eval(expression)
        return f"[calculator] {result}"
        
    except Exception as e:
        return f"[calculator] Error: {str(e)}"

# For testing purpose, the result will be printed directly
if __name__ == "__main__":
    test_cases = [
        "12 * 7",
        "What is 15 + 25?",
        "Calculate 100 / 4",
        "Solve 10 minus 3",
        "Find 5 plus 8",
        "Compute 9 times 6",
        "100 divided by 5",
        "Invalid input here",
        "2 +",
        "5 multiplied by 3 plus 2"
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"Test {i}: {case}")
        result = calculator_tool(case)
        print(f"Result: {result}\n")