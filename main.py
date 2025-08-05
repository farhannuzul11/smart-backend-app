from agent.agent_initializer import create_agent
from llm.ollama_llm import get_llm
from tools.tool_calculator import calculator_tool
from tools.tool_weather import weather_tool
from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

class QueryInput(BaseModel):
    query: str

llm = get_llm()
tools = [calculator_tool, weather_tool]
agent = create_agent(llm, tools)

def parse_agent_response(response: str, query: str = ""):
    """Parse agent response and infer tool usage from query content"""
    
    query_lower = query.lower()
    
    # FIRST: Check for weather-related queries (higher priority)
    if any(keyword in query_lower for keyword in ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cloudy']):
        return "weather_tool", response
    
    # SECOND: Check for mathematical expressions
    if re.search(r'\d+\s*[\+\-\*/×÷]\s*\d+', query):
        return "calculator_tool", response
    
    # THIRD: Check "what is" only if it's mathematical context
    if 'what is' in query_lower:
        # Only classify as calculator if "what is" is followed by math
        if re.search(r'what is\s+\d+.*[\+\-\*/×÷].*\d+', query_lower):
            return "calculator_tool", response
    
    # FOURTH: Other explicit math keywords
    if any(keyword in query_lower for keyword in ['calculate', 'compute', 'solve', 'multiply', 'divide']):
        return "calculator_tool", response
    
    return "the llm", response

@app.post("/query")
async def query_tool(data: QueryInput):
    response = agent.run(data.query)
    tool_used, result = parse_agent_response(response, data.query)  # Pass query here
    return {
        "query": data.query,
        "tool_used": tool_used,
        "result": result
    }

# llm = get_llm()
# tools = [calculator_tool, weather_tool]
# agent = create_agent(llm, tools)

# @app.post("/ask")
# async def ask_question(data: QueryInput):
#     response = agent.run(data.query)
#     return {
#         "query": data.query,
#         "tool_used": "agent",
#         "result": response,
#     }
