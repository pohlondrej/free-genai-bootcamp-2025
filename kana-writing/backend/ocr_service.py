import base64
import io
import logging
from PIL import Image
from manga_ocr import MangaOcr
import numpy as np
from functools import lru_cache
import time
import concurrent.futures

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
        self.timeout = 2.0  # 2 second timeout
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
            
            # Run OCR with timeout
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.mocr, image)
                try:
                    text = future.result(timeout=self.timeout)
                    logger.info(f"OCR completed in {time.time() - start_time:.2f} seconds")
                    return text.strip()
                except concurrent.futures.TimeoutError:
                    logger.error("OCR timed out, using fallback")
                    raise ValueError("OCR processing took too long")
                
        except Exception as e:
            logger.error(f"OCR processing failed: {str(e)}")
            # Fallback: return empty result but don't crash
            return ""

    def compare_text(self, detected: str, expected: str) -> bool:
        # More lenient comparison if OCR failed
        if not detected:
            return False
        return detected.strip() == expected.strip()
