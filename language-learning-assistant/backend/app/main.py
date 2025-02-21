from fastapi import FastAPI, HTTPException
from uuid import UUID
from .quiz_manager import QuizManager
from .models import QuizSession

app = FastAPI()
quiz_manager = QuizManager()

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
