import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load keys and import your working architecture
load_dotenv()
from agent_harness import EnterpriseAgent

app = FastAPI(title="IronLabs AIOPL Agent API")

# Enable CORS so your React frontend can talk to this backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your React port (e.g., http://localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request schema
class ChatRequest(BaseModel):
    message: str

# Instantiate the agent once when the server starts
agent = EnterpriseAgent()

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Execute your proven tool-calling loop
        agent_response = agent.execute_task(request.message)
        return {"status": "success", "response": agent_response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run server on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)