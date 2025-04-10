from pydantic import BaseModel, UUID4, Field
from typing import List, Optional, Literal, Union
from uuid import uuid4
from datetime import datetime

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
        question (str): The LLM-generated question in English
        correct_answer (bool): True for 'yes', False for 'no' answer
    """
    stage_id: UUID4 = uuid4()
    jp_audio: str
    question: str
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
        session_id (int): Unique identifier for the session
        en_intro_audio (str): Cache key for English introduction audio
        en_outro_audio (str): Cache key for English conclusion audio
        vocabulary_stage (VocabularyStage): First stage of the quiz
        comprehension_stage (ComprehensionStage): Second stage of the quiz
        recall_stage (RecallStage): Final stage of the quiz
        current_stage (int): Current progress (0-2)
        score (int): Number of correct answers (0-3)
    """
    session_id: int = None
    en_intro_audio: str = "placeholder.mp3"
    en_outro_audio: str = "placeholder.mp3"
    vocabulary_stage: VocabularyStage
    comprehension_stage: ComprehensionStage
    recall_stage: RecallStage
    current_stage: int = 0
    score: int = 0

class WordItem(BaseModel):
    id: int
    word_level: str
    japanese: str
    kana: str
    romaji: str
    english: str
    item_type: Literal["word"] = "word"

class KanjiItem(BaseModel):
    id: int
    kanji_level: str
    symbol: str
    primary_meaning: str
    primary_reading: str
    primary_reading_type: str
    item_type: Literal["kanji"] = "kanji"

class ReviewItem(BaseModel):
    id: int
    item_type: Literal["word", "kanji"]
    correct: bool
    created_at: datetime
    item: Union[WordItem, KanjiItem]

    class Config:
        smart_union = True

class StudySession(BaseModel):
    id: int
    activity_type: str
    group_name: str
    created_at: datetime
    completed_at: Optional[datetime]
    review_items_count: int
    group_id: int
    review_items: List[ReviewItem]

class GroupWordItem(BaseModel):
    id: int
    item_type: Literal["word"]
    name: str
    level: str
    total_reviews: int
    correct_reviews: int
    wrong_reviews: int

class GroupKanjiItem(BaseModel):
    id: int
    item_type: Literal["kanji"]
    name: str
    level: str
    total_reviews: int
    correct_reviews: int
    wrong_reviews: int

class PaginationInfo(BaseModel):
    current_page: int
    total_pages: int
    total_items: int
    items_per_page: int

class GroupItemsResponse(BaseModel):
    items: List[Union[GroupWordItem, GroupKanjiItem]]
    pagination: PaginationInfo
