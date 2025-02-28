from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from kana_dict import get_random_word

app = FastAPI(title="Kana Practice API")

# Allow CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/word/random")
async def random_word():
    try:
        return {"word": get_random_word()}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate word")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
