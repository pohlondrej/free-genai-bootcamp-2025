from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PaginationResponse(BaseModel):
    current_page: int
    total_pages: int
    total_items: int
    items_per_page: int = 100

class WordBase(BaseModel):
    word_level: str
    kana: str
    japanese: str
    english: str

class WordStats(BaseModel):
    correct_count: int
    wrong_count: int

class GroupBase(BaseModel):
    id: int
    name: str

class WordInList(WordBase, WordStats):
    pass

class WordDetail(WordBase):
    id: int
    romaji: str
    stats: WordStats
    groups: List[GroupBase]

class WordListResponse(BaseModel):
    items: List[WordInList]
    pagination: PaginationResponse

class KanjiBase(BaseModel):
    symbol: str
    kanji_level: str
    primary_reading: str
    primary_meaning: str

class KanjiStats(BaseModel):
    correct_count: int
    wrong_count: int

class KanjiInList(KanjiBase, KanjiStats):
    pass

class KanjiDetail(KanjiBase):
    id: int
    primary_reading_type: str
    stats: KanjiStats
    groups: List[GroupBase]

class KanjiListResponse(BaseModel):
    items: List[KanjiInList]
    pagination: PaginationResponse

class GroupStats(BaseModel):
    total_word_count: int

class GroupInList(BaseModel):
    id: int
    name: str
    word_count: int

class GroupListResponse(BaseModel):
    items: List[GroupInList]
    pagination: PaginationResponse

class GroupDetail(BaseModel):
    id: int
    name: str
    stats: GroupStats

class StudySessionBase(BaseModel):
    id: int
    activity_name: str
    group_name: str
    start_time: datetime
    end_time: datetime
    review_items_count: int

class StudySessionListResponse(BaseModel):
    items: List[StudySessionBase]
    pagination: PaginationResponse

class LastStudySession(BaseModel):
    id: int
    group_id: int
    activity_name: str
    created_at: datetime
    correct_count: int
    wrong_count: int

class StudyProgress(BaseModel):
    total_words_studied: int
    total_available_words: int

class QuickStats(BaseModel):
    success_rate: float
    total_study_sessions: int
    total_active_groups: int
    study_streak_days: int
