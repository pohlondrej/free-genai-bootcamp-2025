from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from typing import Dict, List, Optional
import asyncio
from agent import TopicExplorerAgent

app = FastAPI()

class Topic(BaseModel):
    english_text: str

class TopicResult(BaseModel):
    translation: Dict[str, str]
    vocabulary: List[Dict[str, str]]

# Store results by job ID
results: Dict[str, Optional[TopicResult]] = {}

@app.post("/api/v1/topic")
async def create_topic(topic: Topic):
    job_id = str(uuid.uuid4())
    
    # Store None initially to indicate job is in progress
    results[job_id] = None
    
    # Start processing in background
    asyncio.create_task(process_topic(job_id, topic.english_text))
    
    return {"job_id": job_id}

@app.get("/api/v1/topic/{job_id}")
async def get_topic(job_id: str):
    if job_id not in results:
        raise HTTPException(status_code=404, detail="Job not found")
        
    result = results[job_id]
    if result is None:
        return {"status": "processing"}
        
    return {
        "status": "complete",
        "result": result
    }

async def process_topic(job_id: str, english_text: str):
    """Process the topic using the agent."""
    try:
        agent = TopicExplorerAgent()
        result = agent.run(english_text)
        
        # Store the result
        results[job_id] = result
        
    except Exception as e:
        # Store error result
        results[job_id] = {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
