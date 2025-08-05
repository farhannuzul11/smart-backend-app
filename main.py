from agent.agent_initializer import create_agent
from llm.ollama_llm import get_llm
from tools.tool_calculator import calculator_tool
from tools.tool_weather import weather_tool
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles  # Add this import
from pydantic import BaseModel
import json
import asyncio
import re

app = FastAPI()

class QueryInput(BaseModel):
    query: str

# Initialize your existing components
llm = get_llm()
tools = [calculator_tool, weather_tool]
agent = create_agent(llm, tools)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Your existing HTTP endpoint (keep this!)
def infer_tool_from_query(query: str):
    """Your existing tool inference logic"""
    query_lower = query.lower()
    
    if any(keyword in query_lower for keyword in ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cloudy']):
        return "weather_tool"
    elif re.search(r'\d+\s*[\+\-\*/×÷]\s*\d+', query):
        return "calculator_tool"
    elif 'what is' in query_lower and re.search(r'what is\s+\d+.*[\+\-\*/×÷].*\d+', query_lower):
        return "calculator_tool"
    elif any(keyword in query_lower for keyword in ['calculate', 'compute', 'solve', 'multiply', 'divide']):
        return "calculator_tool"
    else:
        return "llm"

@app.post("/query")
async def query_tool(data: QueryInput):
    """Your existing HTTP endpoint - keep this for compatibility"""
    response = agent.run(data.query)
    tool_used = infer_tool_from_query(data.query)
    
    return {
        "query": data.query,
        "tool_used": tool_used,
        "result": response
    }

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_json_message(self, data: dict, websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(data))
        except Exception as e:
            print(f"Error sending message: {e}")

manager = ConnectionManager()

# WebSocket endpoint for streaming responses
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                query_data = json.loads(data)
                query = query_data.get("query", "").strip()
                
                if not query:
                    await manager.send_json_message({
                        "type": "error",
                        "message": "Empty query received"
                    }, websocket)
                    continue
                
                # Send status updates
                await manager.send_json_message({
                    "type": "status",
                    "message": "Processing your query...",
                    "query": query
                }, websocket)
                
                # Determine which tool will be used
                tool_to_use = infer_tool_from_query(query)
                
                if tool_to_use != "the llm":
                    await manager.send_json_message({
                        "type": "status", 
                        "message": f"Using {tool_to_use.replace('_', ' ')}...",
                        "tool": tool_to_use
                    }, websocket)
                
                # Add small delay for better UX
                await asyncio.sleep(0.5)
                
                # Process with agent
                try:
                    response = agent.run(query)
                    
                    # Send final result
                    await manager.send_json_message({
                        "type": "result",
                        "query": query,
                        "tool_used": tool_to_use,
                        "result": response,
                        "status": "completed"
                    }, websocket)
                    
                except Exception as e:
                    await manager.send_json_message({
                        "type": "error",
                        "message": f"Error processing query: {str(e)}"
                    }, websocket)
                    
            except json.JSONDecodeError:
                await manager.send_json_message({
                    "type": "error",
                    "message": "Invalid JSON format"
                }, websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Redirect root to static HTML
@app.get("/")
async def read_root():
    """Redirect to the HTML file"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "LLM Tool Integration API is running",
        "endpoints": {
            "http": "/query",
            "websocket": "/ws", 
            "web_interface": "/static/index.html"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Build the Docker image
# Run: sudo docker build -t my-fastapi-app .

# Run the container
# Run: sudo docker run --network host my-fastapi-app
