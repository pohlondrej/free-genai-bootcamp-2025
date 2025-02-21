from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from uuid import UUID
from .quiz_manager import QuizManager
from .models import QuizSession
from .audio_manager import AudioManager

app = FastAPI()
quiz_manager = QuizManager()
audio_manager = AudioManager()

@app.post("/session/", response_model=QuizSession)
async def create_session():
    return quiz_manager.create_session()

@app.get("/session/{session_id}", response_model=QuizSession)
async def get_session(session_id: UUID):
    session = quiz_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.post("/session/{session_id}/answer")
async def submit_answer(session_id: UUID, answer: str):
    if not quiz_manager.get_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    correct = quiz_manager.submit_answer(session_id, answer)
    return {"correct": correct}

@app.get("/audio/{cache_key}")
async def get_audio(cache_key: str):
    """Stream audio file from cache"""
    audio_path = audio_manager.get_audio_path(cache_key)
    if not audio_path:
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        headers={"Accept-Ranges": "bytes"}
    )
