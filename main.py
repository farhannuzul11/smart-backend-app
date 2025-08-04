from agent.agent_initializer import create_agent
from llm.ollama_llm import get_llm
from tools.tool_calculator import calculator_tool
from tools.tool_weather import weather_tool
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryInput(BaseModel):
    query: str

llm = get_llm()
tools = [calculator_tool, weather_tool]
agent = create_agent(llm, tools)

def parse_agent_response(response: str):
    # Format response to match the expected structure
    if response.startswith("[") and "]" in response:
        tool_used = response[1:response.index("]")]
        result = response[response.index("]") + 1:].strip()
        return tool_used, result
    else:
        return "the llm", response

@app.post("/query")
async def query_tool(data: QueryInput):
    response = agent.run(data.query)
    tool_used, result = parse_agent_response(response)

    return{
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

# command to run it: uvicorn main:app --reload