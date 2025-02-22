from typing import Dict, Optional
from uuid import UUID, uuid4
from .models import QuizSession, VocabularyStage, ComprehensionStage, RecallStage
from .audio_manager import AudioManager
from .llm_manager import LLMManager

class QuizManager:
    def __init__(self):
        self.active_sessions: Dict[UUID, QuizSession] = {}
        self.audio_manager = AudioManager()
        self.llm_manager = LLMManager()

    async def create_session(self) -> QuizSession:
        # Create placeholder audio data (1 second of silence)
        placeholder_audio = bytes([0] * 44100 * 2)
        
        # Generate content using LLM
        session_content = self.llm_manager.generate_session_content()
        if not session_content:
            # Fallback to demo content if LLM fails
            return self._create_demo_session(placeholder_audio)

        # Cache audio placeholders (will be replaced with TTS later)
        intro_key = self.audio_manager.save_audio(
            placeholder_audio,
            f"intro_{uuid4()}.mp3"
        )
        outro_key = self.audio_manager.save_audio(
            placeholder_audio,
            f"outro_{uuid4()}.mp3"
        )
        vocab_key = self.audio_manager.save_audio(
            placeholder_audio,
            f"vocab_{uuid4()}.mp3"
        )
        conv_key = self.audio_manager.save_audio(
            placeholder_audio,
            f"conv_{uuid4()}.mp3"
        )

        # Create session following the API format
        session = QuizSession(
            en_intro_audio=intro_key,
            en_outro_audio=outro_key,
            vocabulary_stage=VocabularyStage(
                entries=[
                    {"jp_audio": vocab_key, "en_text": word["en_text"]}
                    for word in session_content["vocabulary"]["words"]
                ]
            ),
            comprehension_stage=ComprehensionStage(
                jp_audio=conv_key,
                correct_answer=session_content["conversation"]["correct_answer"]
            ),
            recall_stage=RecallStage(
                jp_audio=conv_key,
                options=session_content["recall"]["words"],
                incorrect_option=session_content["recall"]["incorrect_word"]
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
