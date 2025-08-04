from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType

from fastapi import FastAPI, Request
from pydantic import BaseModel




# Define some tools

@tool
def weather_tool(input: str) -> str:
    """Returns the current weather for a city."""
    if "paris" in input.lower():
        return "It's 26°C and sunny in Paris."
    else:
        return "It's 24°C and cloudy in San Francisco."
    
@tool
def calculator_tool(input: str) -> str:
    """Performs basic math calculations, e.g., '24 * 7'."""
    try:
        return str(eval(input))
    except Exception:
        return "Invalid math expression."

# LLM and Agent Setup
llm = ChatOllama(model="qwen2.5:3b")

tools = [weather_tool, calculator_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# FastAPI Setup
app = FastAPI()


class QueryInput(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(data: QueryInput):
    response = agent.run(data.query)
    return {"response": response}

# if __name__ == "__main__":
#     queries = [
#         "What is 12 * 7?",
#         "What's the weather in Paris today?",
#         "Who is the president of France?"
#     ]

#     for query in queries:
#         print(f"Query: {query}")
#         response = agent.run(query)
#         print(f"Response: {response}\n")
#         print("-----")