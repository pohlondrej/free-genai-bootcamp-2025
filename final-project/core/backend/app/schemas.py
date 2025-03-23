from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PaginationResponse(BaseModel):
    current_page: int
    total_pages: int
    total_items: int
    items_per_page: int

# Word schemas
class WordStats(BaseModel):
    correct_count: int = 0
    wrong_count: int = 0

class WordBase(BaseModel):
    japanese: str
    kana: str
    romaji: Optional[str] = None
    english: str
    word_level: str

class WordCreate(WordBase):
    pass

class WordInList(WordBase):
    id: int
    stats: Optional[WordStats] = None

    class Config:
        from_attributes = True

class WordDetail(WordBase):
    id: int
    stats: WordStats
    groups: List["GroupBase"]

    class Config:
        from_attributes = True

class WordListResponse(BaseModel):
    items: List[WordInList]
    pagination: PaginationResponse

# Kanji schemas
class KanjiStats(BaseModel):
    correct_count: int = 0
    wrong_count: int = 0

class KanjiBase(BaseModel):
    symbol: str
    primary_meaning: str
    primary_reading: str
    primary_reading_type: str
    kanji_level: str

class KanjiCreate(KanjiBase):
    pass

class KanjiInList(KanjiBase):
    id: int
    stats: Optional[KanjiStats] = None

    class Config:
        from_attributes = True

class KanjiDetail(KanjiBase):
    id: int
    stats: KanjiStats
    groups: List["GroupBase"]

    class Config:
        from_attributes = True

class KanjiListResponse(BaseModel):
    items: List[KanjiInList]
    pagination: PaginationResponse

# Unified item schemas for group items
class UnifiedItemBase(BaseModel):
    id: int
    type: str  # 'word' or 'kanji'
    japanese: str  # word.japanese or kanji.symbol
    english: str   # word.english or kanji.primary_meaning
    correct_count: int = 0
    wrong_count: int = 0

    class Config:
        from_attributes = True

class UnifiedItemListResponse(BaseModel):
    items: List[UnifiedItemBase]
    pagination: PaginationResponse

# Group schemas
class GroupStats(BaseModel):
    total_items: int = 0
    word_count: int = 0
    kanji_count: int = 0
    completed_sessions: int = 0
    active_sessions: int = 0

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class GroupInList(GroupBase):
    id: int
    word_count: int = 0
    kanji_count: int = 0
    stats: Optional[GroupStats] = None

    class Config:
        from_attributes = True

class GroupDetail(GroupBase):
    id: int
    words: List[WordInList]
    kanji: List[KanjiInList]
    stats: GroupStats

    class Config:
        from_attributes = True

class GroupListResponse(BaseModel):
    items: List[GroupInList]
    pagination: PaginationResponse

# Study session schemas
class StudySessionBase(BaseModel):
    group_id: int
    activity_type: str

class StudySessionCreate(StudySessionBase):
    pass

class StudySessionInList(BaseModel):
    id: int
    activity_type: str
    group_name: str
    start_time: datetime
    end_time: Optional[datetime]
    review_items_count: int

    class Config:
        from_attributes = True

class StudySessionDetail(BaseModel):
    id: int
    activity_type: str
    group_id: int
    group_name: str
    start_time: datetime
    end_time: Optional[datetime]
    total_items: int
    correct_items: int

    class Config:
        from_attributes = True

class StudySessionListResponse(BaseModel):
    items: List[StudySessionInList]
    pagination: PaginationResponse

# Review item schemas
class WordReviewItemBase(BaseModel):
    word_id: int
    study_session_id: int
    correct: bool

class WordReviewItemCreate(WordReviewItemBase):
    pass

class WordReviewItemInList(WordReviewItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
