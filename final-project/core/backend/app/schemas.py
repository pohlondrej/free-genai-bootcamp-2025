from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime

class PaginationResponse(BaseModel):
    current_page: int
    total_pages: int
    total_items: int
    items_per_page: int

# Group schemas
class GroupBase(BaseModel):
    id: int
    name: str

class GroupStats(BaseModel):
    total_items: int
    word_count: int
    kanji_count: int
    completed_sessions: int
    active_sessions: int

class GroupCreate(BaseModel):
    name: str

class GroupInList(BaseModel):
    id: int
    name: str
    word_count: int
    kanji_count: int
    total_items: int

    class Config:
        from_attributes = True

class GroupDetail(BaseModel):
    id: int
    name: str
    stats: GroupStats

    class Config:
        from_attributes = True

class GroupListResponse(BaseModel):
    items: List[GroupInList]
    pagination: PaginationResponse

# Word schemas
class WordBase(BaseModel):
    id: int
    word_level: str
    japanese: str
    kana: str
    romaji: Optional[str]
    english: str

class WordStats(BaseModel):
    total_reviews: int
    correct_reviews: int
    wrong_reviews: int

class WordInList(WordBase):
    stats: WordStats

    class Config:
        from_attributes = True

class WordListResponse(BaseModel):
    items: List[WordInList]
    pagination: PaginationResponse

class WordDetail(WordBase):
    stats: WordStats
    groups: List[GroupBase]

    class Config:
        from_attributes = True

class WordCreate(BaseModel):
    word_level: str
    japanese: str
    kana: str
    romaji: Optional[str]
    english: str

# Kanji schemas
class KanjiBase(BaseModel):
    id: int
    kanji_level: str
    symbol: str
    primary_meaning: str
    primary_reading: str
    primary_reading_type: str

class KanjiStats(BaseModel):
    total_reviews: int
    correct_reviews: int
    wrong_reviews: int

class KanjiInList(KanjiBase):
    stats: KanjiStats

    class Config:
        from_attributes = True

class KanjiListResponse(BaseModel):
    items: List[KanjiInList]
    pagination: PaginationResponse

class KanjiDetail(KanjiBase):
    stats: KanjiStats
    groups: List[GroupBase]

    class Config:
        from_attributes = True

class KanjiCreate(BaseModel):
    kanji_level: str
    symbol: str
    primary_meaning: str
    primary_reading: str
    primary_reading_type: str

# Unified item schemas for group items
class UnifiedItemBase(BaseModel):
    id: int
    item_type: str
    name: str
    level: str
    total_reviews: int
    correct_reviews: int
    wrong_reviews: int

class UnifiedItemListResponse(BaseModel):
    items: List[UnifiedItemBase]
    pagination: PaginationResponse

# Study session schemas
class StudySessionBase(BaseModel):
    id: int
    activity_type: str
    group_name: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    review_items_count: int

    class Config:
        from_attributes = True

class StudySessionCreate(BaseModel):
    group_id: int
    activity_type: str

class StudySessionInList(StudySessionBase):
    pass

class ReviewItemBase(BaseModel):
    id: int
    item_type: str
    item_id: int
    study_session_id: int
    correct: bool
    created_at: datetime

class ReviewItem(ReviewItemBase):
    word: Optional[WordBase] = None
    kanji: Optional[KanjiBase] = None

    class Config:
        from_attributes = True

class ReviewItemInSession(BaseModel):
    id: int
    item_type: str  # 'word' or 'kanji'
    correct: bool
    created_at: datetime
    item: Union[WordBase, KanjiBase]

    class Config:
        from_attributes = True

class StudySessionDetail(StudySessionBase):
    group_id: int
    review_items: List[ReviewItemInSession]

    class Config:
        from_attributes = True

class StudySessionListResponse(BaseModel):
    items: List[StudySessionInList]
    pagination: PaginationResponse
