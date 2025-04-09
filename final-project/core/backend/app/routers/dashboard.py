from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, desc, and_, Integer
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from models import Word, Kanji, StudySession, Group, ReviewItem, User

class StudyProgress(BaseModel):
    total_words: int
    studied_words: int
    total_kanji: int
    studied_kanji: int

class WanikaniLevel(BaseModel):
    level: int

class StudyItem(BaseModel):
    id: int
    type: str  # 'word' or 'kanji'
    count: Optional[int] = None
    success_rate: Optional[float] = None

class GroupStats(BaseModel):
    id: int
    name: str
    activity_count: int

class LastStudied(BaseModel):
    item_id: int
    item_type: str
    studied_at: datetime

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/study-progress", response_model=StudyProgress)
async def get_study_progress(db: AsyncSession = Depends(get_db)):
    """Get the total progress of words and kanji studied."""
    # Get total counts
    total_words = await db.scalar(select(func.count()).select_from(Word))
    total_kanji = await db.scalar(select(func.count()).select_from(Kanji))
    
    # Get counts of studied items (items that have been reviewed at least once)
    studied_words = await db.scalar(
        select(func.count(Word.id))
        .select_from(Word)
        .join(ReviewItem, and_(
            ReviewItem.item_type == 'word',
            ReviewItem.item_id == Word.id
        ))
        .group_by(Word.id)
    )
    
    studied_kanji = await db.scalar(
        select(func.count(Kanji.id))
        .select_from(Kanji)
        .join(ReviewItem, and_(
            ReviewItem.item_type == 'kanji',
            ReviewItem.item_id == Kanji.id
        ))
        .group_by(Kanji.id)
    )
    
    return StudyProgress(
        total_words=total_words or 0,
        studied_words=studied_words or 0,
        total_kanji=total_kanji or 0,
        studied_kanji=studied_kanji or 0
    )

@router.get("/wanikani-level", response_model=Optional[WanikaniLevel])
async def get_wanikani_level(db: AsyncSession = Depends(get_db)):
    """Get the current Wanikani level if enabled."""
    # Check if Wanikani is enabled in user settings
    use_wanikani = await db.scalar(
        select(User.value)
        .where(User.key == "use_wanikani")
    )
    
    if not use_wanikani:
        return None
    
    # Find the highest WK_ it
    highest_level = await db.scalar(
        select(func.max(func.cast(
            func.substr(Word.word_level, 4),  # Extract number after "WK_"
            type_=Integer
        )))
        .where(Word.word_level.like("WK_%"))
    )
    
    if highest_level is None:
        return WanikaniLevel(level=0)
        
    return WanikaniLevel(level=highest_level)

@router.get("/most-studied", response_model=List[StudyItem])
async def get_most_studied(limit: int = 5, db: AsyncSession = Depends(get_db)):
    """Get the most frequently studied items."""
    most_studied = await db.execute(
        select(
            ReviewItem.item_id,
            ReviewItem.item_type,
            func.count(ReviewItem.id).label("study_count")
        )
        .group_by(ReviewItem.item_id, ReviewItem.item_type)
        .order_by(desc("study_count"))
        .limit(limit)
    )
    
    return [
        StudyItem(
            id=item.item_id,
            type=item.item_type,
            count=item.study_count
        )
        for item in most_studied
    ]

@router.get("/problematic-items", response_model=List[StudyItem])
async def get_problematic_items(limit: int = 5, db: AsyncSession = Depends(get_db)):
    """Get items with lowest success rate."""
    problematic = await db.execute(
        select(
            ReviewItem.item_id,
            ReviewItem.item_type,
            func.round(
                (100.0 * func.sum(func.cast(ReviewItem.correct, Integer))) / 
                func.nullif(func.count(ReviewItem.id), 0)
            ).label("success_rate")
        )
        .group_by(ReviewItem.item_id, ReviewItem.item_type)
        .having(func.count(ReviewItem.id) >= 5)  # Minimum attempts threshold
        .order_by("success_rate")
        .limit(limit)
    )
    
    return [
        StudyItem(
            id=item.item_id,
            type=item.item_type,
            success_rate=item.success_rate
        )
        for item in problematic
    ]

@router.get("/most-studied-group", response_model=GroupStats)
async def get_most_studied_group(db: AsyncSession = Depends(get_db)):
    """Get the most frequently studied group."""
    most_active_group = await db.execute(
        select(
            Group.id,
            Group.name,
            func.count(StudySession.id).label("activity_count")
        )
        .join(StudySession, StudySession.group_id == Group.id)
        .group_by(Group.id, Group.name)
        .order_by(desc("activity_count"))
        .limit(1)
    )
    
    group = most_active_group.first()
    if not group:
        raise HTTPException(status_code=404, detail="No study groups found")
    
    return GroupStats(
        id=group.id,
        name=group.name,
        activity_count=group.activity_count
    )

@router.get("/last-studied", response_model=LastStudied)
async def get_last_studied(db: AsyncSession = Depends(get_db)):
    """Get the most recently studied item."""
    last_review = await db.execute(
        select(ReviewItem)
        .order_by(desc(ReviewItem.id))
        .limit(1)
    )
    
    result = last_review.first()
    if not result:
        raise HTTPException(status_code=404, detail="No study activity found")
    
    review = result[0]  # Get the actual ReviewItem from the result tuple
    
    return LastStudied(
        item_id=review.item_id,
        item_type=review.item_type,
        studied_at=review.created_at
    )
