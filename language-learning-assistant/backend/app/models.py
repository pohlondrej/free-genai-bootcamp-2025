from pydantic import BaseModel, UUID4
from typing import List, Optional
from uuid import uuid4

class VocabularyEntry(BaseModel):
    """A single vocabulary item with its Japanese audio and English translation.
    
    Attributes:
        jp_audio (str): Cache key or path to the Japanese audio file
        en_text (str): English translation of the vocabulary word
    """
    jp_audio: str
    en_text: str

class VocabularyStage(BaseModel):
    """First quiz stage focused on vocabulary matching.
    
    Attributes:
        stage_id (UUID4): Unique identifier for this stage
        entries (List[VocabularyEntry]): List of 4 vocabulary items to match
    """
    stage_id: UUID4 = uuid4()
    entries: List[VocabularyEntry]

class ComprehensionStage(BaseModel):
    """Second quiz stage testing comprehension with yes/no questions.
    
    Attributes:
        stage_id (UUID4): Unique identifier for this stage
        jp_audio (str): Cache key or path to the Japanese audio question
        correct_answer (bool): True for 'yes', False for 'no' answer
    """
    stage_id: UUID4 = uuid4()
    jp_audio: str
    correct_answer: bool

class RecallStage(BaseModel):
    """Final quiz stage testing vocabulary recall.
    
    Attributes:
        stage_id (UUID4): Unique identifier for this stage
        jp_audio (str): Cache key or path to the Japanese audio segment
        options (List[str]): List of 3 Japanese words to choose from
        incorrect_option (str): The deliberately incorrect option
    """
    stage_id: UUID4 = uuid4()
    jp_audio: str
    options: List[str]
    incorrect_option: str

class QuizSession(BaseModel):
    """Represents a complete quiz session with all its stages.
    
    Attributes:
        session_id (UUID4): Unique identifier for the session
        en_intro_audio (str): Cache key for English introduction audio
        en_outro_audio (str): Cache key for English conclusion audio
        vocabulary_stage (VocabularyStage): First stage of the quiz
        comprehension_stage (ComprehensionStage): Second stage of the quiz
        recall_stage (RecallStage): Final stage of the quiz
        current_stage (int): Current progress (0-2)
        score (int): Number of correct answers (0-3)
    """
    session_id: UUID4 = uuid4()
    en_intro_audio: str = "placeholder.mp3"
    en_outro_audio: str = "placeholder.mp3"
    vocabulary_stage: VocabularyStage
    comprehension_stage: ComprehensionStage
    recall_stage: RecallStage
    current_stage: int = 0
    score: int = 0
