from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI()

class Topic(BaseModel):
    topic: str

# Dummy responses
DUMMY_RESULT = {
    "english_summary": "Cats are small, furry pets that love to sleep and play.",
    "japanese_summary": "猫は小さくて、毛深いペットです。寝ることと遊ぶことが大好きです。",
    "vocabulary": [
        {"word": "猫", "reading": "ねこ", "meaning": "cat"},
        {"word": "小さい", "reading": "ちいさい", "meaning": "small"},
        {"word": "大好き", "reading": "だいすき", "meaning": "love"},
    ],
    "images": [
        "https://example.com/cat1.jpg",
        "https://example.com/cat2.jpg"
    ]
}

@app.post("/api/v1/topic")
async def create_topic(topic: Topic):
    # Generate a random job ID
    return {"job_id": str(uuid.uuid4())}

@app.get("/api/v1/status/{job_id}")
async def get_status(job_id: str):
    # Always return completed for now
    return {"status": "completed"}

@app.get("/api/v1/result/{job_id}")
async def get_result(job_id: str):
    # Return dummy result
    return DUMMY_RESULT

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
