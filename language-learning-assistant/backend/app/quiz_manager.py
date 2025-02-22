from typing import Dict, Optional
from uuid import UUID
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
        
        # Cache all audio files
        intro_key = self.audio_manager.save_audio(placeholder_audio, "intro.mp3")
        outro_key = self.audio_manager.save_audio(placeholder_audio, "outro.mp3")
        demo_key = self.audio_manager.save_audio(placeholder_audio, "demo.mp3")

        # Generate content using LLM
        vocab_data = self.llm_manager.generate_vocabulary()
        comp_data = self.llm_manager.generate_comprehension()
        recall_data = self.llm_manager.generate_recall()

        # Create vocabulary entries with fallback
        vocab_entries = []
        if vocab_data:
            vocab_entries = [
                {"jp_audio": demo_key, "en_text": item["en_text"]}
                for item in vocab_data[:4]
            ]
        if not vocab_entries:
            vocab_entries = [{"jp_audio": demo_key, "en_text": "Hello"} for _ in range(4)]

        # Create session with LLM content or fallback to demo content
        session = QuizSession(
            en_intro_audio=intro_key,
            en_outro_audio=outro_key,
            vocabulary_stage=VocabularyStage(entries=vocab_entries),
            comprehension_stage=ComprehensionStage(
                jp_audio=demo_key,
                correct_answer=comp_data["correct_answer"] if comp_data else True
            ),
            recall_stage=RecallStage(
                jp_audio=demo_key,
                options=recall_data["words"] if recall_data else ["日本", "はい", "こんにちは"],
                incorrect_option=recall_data["incorrect_word"] if recall_data else "こんにちは"
            )
        )
        self.active_sessions[session.session_id] = session
        return session

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
