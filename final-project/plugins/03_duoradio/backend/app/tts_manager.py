from typing import Optional, Tuple
import io
import numpy as np
import soundfile as sf
from TTS.api import TTS
import logging
import time

class TTSManager:
    def __init__(self):
        # Primary models
        self.jp_model = TTS(model_name="tts_models/ja/kokoro/tacotron2-DDC")
        self.en_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        
        # Backup models (loaded on demand)
        self._jp_backup = None
        self._en_backup = None
        
    def _add_speech_marks(self, text: str, language: str) -> str:
        """Add speech marks for better prosody"""
        if language == "jp":
            # Add proper breaks for Japanese text
            return text.replace("。", "。<break time='1s'/>")
        else:
            # Add commas and periods for natural English pauses
            return text.replace(". ", ".<break time='1s'/>").replace(", ", ",<break time='0.5s'/>")
    
    def _validate_audio(self, wav: np.ndarray) -> bool:
        """Check if audio data is valid"""
        if wav is None or len(wav) == 0:
            return False
        if np.isnan(wav).any() or np.isinf(wav).any():
            return False
        return True
    
    def _get_backup_model(self, language: str) -> TTS:
        """Load backup model if needed"""
        if language == "jp":
            if not self._jp_backup:
                self._jp_backup = TTS(model_name="tts_models/ja/hifigan/tacotron2-DDC")
            return self._jp_backup
        else:
            if not self._en_backup:
                self._en_backup = TTS(model_name="tts_models/en/vctk/vits")
            return self._en_backup

    def generate_speech(self, text: str, language: str = "en") -> Optional[bytes]:
        """Generate speech with fallback and validation"""
        try:
            start_time = time.time()
            logging.info(f"Starting TTS generation for language: {language}")
            logging.debug(f"Text to synthesize: {text[:100]}...")
            
            # Add speech marks for better prosody
            marked_text = self._add_speech_marks(text, language)
            
            # Set appropriate speech rate
            rate = 0.85 if language == "jp" else 1.0
            
            # Try primary model
            model = self.jp_model if language == "jp" else self.en_model
            wav = model.tts(
                text=marked_text,
                speaker_wav=None,
                speed=rate
            )
            
            # Validate audio and try backup if needed
            if not self._validate_audio(wav):
                print(f"Primary TTS failed, trying backup for {language}")
                backup_model = self._get_backup_model(language)
                wav = backup_model.tts(marked_text)
                
                if not self._validate_audio(wav):
                    print("Backup TTS also failed")
                    return None
            
            # Convert to bytes with higher quality settings
            buffer = io.BytesIO()
            sf.write(
                buffer,
                wav,
                model.synthesizer.output_sample_rate,
                format='wav',
                subtype='PCM_16',
                endian='LITTLE'
            )
            
            # Log performance metrics
            duration = time.time() - start_time
            logging.info(f"TTS generation completed in {duration:.2f}s")
            return buffer.getvalue()
            
        except Exception as e:
            logging.error(f"TTS Error: {str(e)}", exc_info=True)
            return None
