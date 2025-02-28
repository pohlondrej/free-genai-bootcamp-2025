import base64
import io
import logging
from PIL import Image
from manga_ocr import MangaOcr
import numpy as np
from functools import lru_cache
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_mocr():
    """Cache the MangaOcr instance to avoid multiple initializations"""
    logger.info("Initializing MangaOCR...")
    start_time = time.time()
    mocr = MangaOcr()
    logger.info(f"MangaOCR initialized in {time.time() - start_time:.2f} seconds")
    return mocr

class OCRService:
    def __init__(self):
        self.mocr = get_mocr()
        logger.info("OCR Service ready")
    
    def process_base64_image(self, base64_string: str) -> str:
        try:
            start_time = time.time()
            
            # Decode base64 to image
            image_data = base64.b64decode(base64_string)
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Perform OCR with timing
            logger.info("Starting OCR processing...")
            text = self.mocr(image)
            logger.info(f"OCR completed in {time.time() - start_time:.2f} seconds")
            
            return text.strip()
        except Exception as e:
            logger.error(f"OCR processing failed: {str(e)}")
            raise ValueError(f"Failed to process image: {str(e)}")

    def compare_text(self, detected: str, expected: str) -> bool:
        return detected.strip() == expected.strip()
