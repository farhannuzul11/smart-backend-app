# 🧠 Natural Language Tool Router (Coding Challenge)

> **Author**: Farhan Nuzul  
> **Challenge from**: Manoo Assa 
> **Date**: August 2025
> > **About**: This project builds a small backend app that routes natural language commands to the correct tool (Weather, Calculator, or LLM) and returns structured results. I also includes a simple static frontend and allowing users to interact with the AI directly via a web interface.

<img width="1804" height="1001" alt="image" src="https://github.com/user-attachments/assets/89f3a3e9-ea7c-4731-9adb-466c750fc898" />

## - Objective

- Accept input via POST API or WebSocket
- Detect intent & choose correct tool: LLM / Weather / Math
- Return structured JSON result
- Bonus: 
    - WebSocket 
    - Dockerized
    - Static web interface

## - System Architecture
![my-backend-app-architectue](https://github.com/user-attachments/assets/57fd6147-bbf2-4815-b243-17a42743f72e)

This diagram shows how the user input is processed:

1. User submits a query via REST, WebSocket, or web frontend.
2. Query is analyzed using pattern matching / LangChain agent.
3. The selected tool (LLM / weather / calculator) is executed.
4. A JSON response is returned to the client.

## - Tech Stack

-   **FastAPI** – REST & WebSocket backend
-   **LangChain** – Agent orchestration and tool calling
-   **Ollama** – Local LLM (qwen2.5:3b)
-   **OpenWeatherMap API** – For weather tool
-   **Docker** – Containerized deployment
-   **Static Frontend** - Interact with AI via web interface

## - Features

✅ /query POST endpoint for API requests 
✅ WebSocket /ws streaming support
✅ Three tools:
    - LLM: Local answer generation (via Ollama)
    - Weather: Calls OpenWeather API
    - Math: Performs calculation
✅ '.env 'config for sensitive values
✅ Dockerized and ready to deploy
✅ Static frontend: Easy to use via browser

## - Setup and Deployment

### Requirements

-   Python 3.10+
-   Docker
-   API key from OpenWeatherMap

### .env Example

```bash
WEATHER_API_KEY=your_openweather_api_key_here
```

### Local Installation (Without Docker)

```python
# 1. Clone the repository
git clone https://github.com/farhannuzul11/smart-backend-app
cd smart-backend-app

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
echo "WEATHER_API_KEY=your_api_key" > .env

# 5. Run the app
uvicorn main:app --reload
```
Visit: http://localhost:8000

### 🐳 Dockerized Setup
This project is fully containerized for ease of deployment.
```python
# 1. Build Docker image
sudo docker build -t my-fastapi-app .

# 2. Run Docker container with .env
sudo docker run --network host my-fastapi-app
```
Visit: http://localhost:8000

## Testing & Validation

### ✅ Sample 1 – Math Tool
**Request**:
```
curl -X POST http://127.0.0.1:8000/query   -H "Content-Type: application/json"   -d '{"query":"What is 12 * 7?"}' | jq
```
**Response**:
<img width="816" height="237" alt="image" src="https://github.com/user-attachments/assets/045eff87-c1fc-4586-8099-382213f20171" />


### ✅ Sample 2 – Weather Tool
**Request**:
```
curl -X POST http://127.0.0.1:8000/query   -H "Content-Type: application/json"   -d '{"query":"What’s the weather today in Taipei?"}' | jq
```
**Response**:
<img width="810" height="225" alt="image" src="https://github.com/user-attachments/assets/ee691fae-206b-4de0-8f27-dcc236ca874b" />

### ✅ Sample 3 – LLM Tool
**Request**:
```
curl -X POST http://127.0.0.1:8000/query   -H "Content-Type: application/json"   -d '{"query":"Who is the president of France?"}' | jq
```
**Response**:
<img width="811" height="292" alt="image" src="https://github.com/user-attachments/assets/99927593-5837-47a6-8286-6c0ad194e537" />

### Websocket (Bonus)
- Connecting:' ws://localhost:8000/ws'
- Testing it with Postman
**Example Request**
<img width="508" height="298" alt="image" src="https://github.com/user-attachments/assets/18dc6661-219d-4e59-aaa7-09f4e1131c46" />
**Example Response**
<img width="1434" height="393" alt="image" src="https://github.com/user-attachments/assets/8e117a08-84ee-4dd5-a866-42ccf7e6c4ca" />


### AI Web Interface
The static frontend allows users to interact with the app via browser (JavaScript-based). It communicates with /ws WebSocket endpoint in real-time.
Visit: http://localhost:8000
<img width="1799" height="1001" alt="image" src="https://github.com/user-attachments/assets/a4898a23-648c-44c7-bc5e-0833c6c6958e" />










































<!-- ## System Architecture
![my-backend-app-architectue](https://hackmd.io/_uploads/H163qLldgg.jpg)

This app accepts natural language queries and routes them to the appropriate "tool" based on intent:
- Weather Tool 🌤️
- Math Tool ➗
- LLM Tool 🤖

The output is a structured JSON response indicating:
- The original query
- The tool used
- The result


## 📦 Features

✅ `/query` POST endpoint (main requirement)  
✅ Weather, Math, and LLM tools  
✅ WebSocket support (bonus)  
✅ Dockerized (bonus)  
✅ `.env` support for API key injection  
✅ Modular, testable architecture
 -->






















<!-- 1. Make the .venv
![image](https://hackmd.io/_uploads/Sykpk4hweg.png)

2. Install Dependencies
![image](https://hackmd.io/_uploads/SJFAWVnDle.png)

3. Deprecated version
![image](https://hackmd.io/_uploads/S1yduN3vgl.png)

4. Github
![image](https://hackmd.io/_uploads/rkkHBLRvxe.png)

5. Testing/
![image](https://hackmd.io/_uploads/B1c4Umy_ee.png)

6. Docker File
![image](https://hackmd.io/_uploads/B1mDMVy_lx.png)
 -->

