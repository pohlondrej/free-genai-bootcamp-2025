from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from kana_dict import get_random_word
import logging

app = FastAPI(title="Kana Practice API")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OCR service at startup
ocr_service = None
def init_ocr():
    global ocr_service
    try:
        from ocr_service import OCRService
        ocr_service = OCRService()
        logger.info("OCR service initialized successfully")
    except ImportError as e:
        logger.error(f"Failed to initialize OCR service: {e}")
        
@app.on_event("startup")
async def startup_event():
    init_ocr()

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

class DrawingSubmission(BaseModel):
    image: str  # base64 encoded image
    expected_word: str

@app.post("/submit")
async def check_drawing(submission: DrawingSubmission):
    if ocr_service is None:
        raise HTTPException(
            status_code=503,
            detail="OCR service not available"
        )
    try:
        detected_text = ocr_service.process_base64_image(submission.image)
        match = ocr_service.compare_text(detected_text, submission.expected_word)
        return {
            "match": match,
            "detected_text": detected_text
        }
    except Exception as e:
        logger.error(f"Error processing submission: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
