from typing import Dict, Optional
from uuid import UUID, uuid4
from .models import QuizSession, VocabularyStage, ComprehensionStage, RecallStage
from .audio_manager import AudioManager
from .llm_manager import LLMManager
from .tts_manager import TTSManager

class QuizManager:
    def __init__(self):
        self.active_sessions: Dict[UUID, QuizSession] = {}
        self.audio_manager = AudioManager()
        self.llm_manager = LLMManager()
        self.tts_manager = TTSManager()
    
    async def create_session(self) -> QuizSession:
        placeholder_audio = bytes([0] * 44100 * 2)
        
        # Generate content using LLM
        session_content = self.llm_manager.generate_session_content()
        if not session_content:
            return self._create_demo_session(placeholder_audio)

        # Generate audio for each text
        intro_audio = self.tts_manager.generate_speech(session_content["intro_text"], "en")
        outro_audio = self.tts_manager.generate_speech(session_content["outro_text"], "en")
        
        # Cache audio files
        intro_key = self.audio_manager.save_audio(intro_audio or placeholder_audio, f"intro_{uuid4()}.wav")
        outro_key = self.audio_manager.save_audio(outro_audio or placeholder_audio, f"outro_{uuid4()}.wav")
        
        # Generate vocabulary audio
        vocab_keys = []
        for word in session_content["vocabulary"]["words"]:
            audio = self.tts_manager.generate_speech(word["jp_text"], "jp")
            key = self.audio_manager.save_audio(audio or placeholder_audio, f"vocab_{uuid4()}.wav")
            vocab_keys.append(key)
        
        # Generate monologue audio
        monologue1_audio = self.tts_manager.generate_speech(session_content["monologue"]["jp_text"], "jp")
        monologue2_audio = self.tts_manager.generate_speech(session_content["recall"]["continuation"]["jp_text"], "jp")
        
        monologue1_key = self.audio_manager.save_audio(monologue1_audio or placeholder_audio, f"monologue1_{uuid4()}.wav")
        monologue2_key = self.audio_manager.save_audio(monologue2_audio or placeholder_audio, f"monologue2_{uuid4()}.wav")

        session = QuizSession(
            en_intro_audio=intro_key,
            en_outro_audio=outro_key,
            vocabulary_stage=VocabularyStage(
                entries=[
                    {"jp_audio": key, "en_text": word["en_text"]}
                    for key, word in zip(vocab_keys, session_content["vocabulary"]["words"])
                ]
            ),
            comprehension_stage=ComprehensionStage(
                jp_audio=monologue1_key,
                correct_answer=session_content["monologue"]["correct_answer"]
            ),
            recall_stage=RecallStage(
                jp_audio=monologue2_key,  # Using the continuation monologue audio
                options=session_content["recall"]["quiz"]["words"],
                incorrect_option=session_content["recall"]["quiz"]["incorrect_word"]
            )
        )
        
        self.active_sessions[session.session_id] = session
        return session

    def _create_demo_session(self, placeholder_audio: bytes) -> QuizSession:
        """Create a fallback demo session when LLM fails"""
        demo_key = self.audio_manager.save_audio(placeholder_audio, "demo.mp3")
        return QuizSession(
            vocabulary_stage=VocabularyStage(
                entries=[{"jp_audio": demo_key, "en_text": "Hello"} for _ in range(4)]
            ),
            comprehension_stage=ComprehensionStage(
                jp_audio=demo_key,
                correct_answer=True
            ),
            recall_stage=RecallStage(
                jp_audio=demo_key,
                options=["日本", "はい", "こんにちは"],
                incorrect_option="こんにちは"
            )
        )

    def get_session(self, session_id: UUID) -> Optional[QuizSession]:
        return self.active_sessions.get(session_id)

    def submit_answer(self, session_id: UUID, answer: str) -> bool:
        session = self.get_session(session_id)
        if not session:
            return False

        correct = False
        if session.current_stage == 0:
            # Vocabulary stage logic
            correct = True  # Simplified for demo
        elif session.current_stage == 1:
            # Comprehension stage logic
            correct = answer.lower() == str(session.comprehension_stage.correct_answer).lower()
        elif session.current_stage == 2:
            # Recall stage logic
            correct = answer != session.recall_stage.incorrect_option

        if correct:
            session.score += 1
        
        session.current_stage += 1
        return correct
