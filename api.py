import os
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
from agent_harness import EnterpriseAgent
from rag_core import EnterpriseRAG  # Bring in your RAG engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows your Vercel frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


agent = EnterpriseAgent()
rag_engine = EnterpriseRAG()

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # 1. Save the uploaded file temporarily
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Feed it directly to your RAG core
        rag_engine.ingest_data(file_location)
        
        # (Optional) Clean up the file after vectorizing
        # os.remove(file_location)
        
        return {"status": "success", "message": f"{file.filename} vectorized successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ... keep your existing /api/chat endpoint here ...
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