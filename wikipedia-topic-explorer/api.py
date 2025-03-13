from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from agent import TopicExplorerAgent

app = FastAPI()
agent = TopicExplorerAgent()

class Topic(BaseModel):
    topic: str

# Store results in memory (replace with proper storage in production)
results = {}

# Dummy responses (except vocabulary will be real)
DUMMY_TEXT = {
    "english_summary": "Cats are small, furry pets that love to sleep and play.",
    "japanese_summary": "猫は小さくて、毛深いペットです。寝ることと遊ぶことが大好きです。",
    "images": [
        "https://example.com/cat1.jpg",
        "https://example.com/cat2.jpg"
    ]
}

@app.post("/api/v1/topic")
async def create_topic(topic: Topic):
    job_id = str(uuid.uuid4())
    try:
        # For now, we'll use the Japanese dummy text for vocabulary extraction
        result = agent.run(DUMMY_TEXT["japanese_summary"])
        results[job_id] = {
            "status": "success",
            **DUMMY_TEXT,
            "vocabulary": result["vocabulary"]
        }
        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in results:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": "completed"}

@app.get("/api/v1/result/{job_id}")
async def get_result(job_id: str):
    if job_id not in results:
        raise HTTPException(status_code=404, detail="Job not found")
    
    result = results[job_id]
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
