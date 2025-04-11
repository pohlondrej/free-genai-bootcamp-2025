from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, and_, or_
from database import get_db
from models import Word, ReviewItem, GroupItem, Group
from schemas import (
    WordListResponse,
    WordDetail,
    WordCreate,
    WordInList,
    WordStats,
    PaginationResponse,
    UnifiedItemListResponse,
    UnifiedItemBase,
    GroupBase
)
from typing import List, Optional

router = APIRouter(prefix="/words", tags=["words"])

ITEMS_PER_PAGE = 30

@router.get("", response_model=WordListResponse)
async def list_words(
    page: int = 1,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of words"""
    # Calculate offset
    offset = (page - 1) * ITEMS_PER_PAGE
    
    # Base query for filtering
    base_query = select(Word)
    if search:
        search_term = f"%{search.lower()}%"
        base_query = base_query.filter(
            or_(
                func.lower(Word.english).like(search_term),
                func.lower(Word.japanese).like(search_term),
                func.lower(Word.kana).like(search_term)
            )
        )
    
    # Get total count with search filter
    result = await db.execute(select(func.count()).select_from(base_query.subquery()))
    total_count = result.scalar()
    
    # Get words with their stats
    query = (
        select(
            Word,
            func.count(ReviewItem.id).label("total_reviews"),
            func.sum(case((ReviewItem.correct == True, 1), else_=0)).label("correct_reviews")
        )
        .outerjoin(ReviewItem, and_(ReviewItem.item_id == Word.id, ReviewItem.item_type == 'word'))
    )
    
    # Apply search filter to main query
    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                func.lower(Word.english).like(search_term),
                func.lower(Word.japanese).like(search_term),
                func.lower(Word.kana).like(search_term)
            )
        )
    
    # Add grouping, offset and limit
    query = (
        query
        .group_by(Word.id)
        .offset(offset)
        .limit(ITEMS_PER_PAGE)
    )
    
    result = await db.execute(query)
    word_list = result.all()
    
    # Convert to response model
    items = [
        WordInList(
            id=word.id,
            word_level=word.word_level,
            japanese=word.japanese,
            kana=word.kana,
            romaji=word.romaji,
            english=word.english,
            stats=WordStats(
                total_reviews=total_reviews or 0,
                correct_reviews=correct_reviews or 0,
                wrong_reviews=(total_reviews or 0) - (correct_reviews or 0)
            )
        )
        for word, total_reviews, correct_reviews in word_list
    ]
    
    return WordListResponse(
        items=items,
        pagination=PaginationResponse(
            current_page=page,
            total_pages=(total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE,
            total_items=total_count,
            items_per_page=ITEMS_PER_PAGE
        )
    )

@router.get("/{word_id}", response_model=WordDetail)
async def get_word(word_id: int, db: AsyncSession = Depends(get_db)):
    """Get details of a specific word"""
    query = select(Word).filter(Word.id == word_id)
    result = await db.execute(query)
    word = result.scalar()
    
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # Get review stats
    stats_query = (
        select(
            func.count(ReviewItem.id).label("total_reviews"),
            func.sum(case((ReviewItem.correct == True, 1), else_=0)).label("correct_reviews")
        )
        .select_from(ReviewItem)
        .filter(ReviewItem.item_id == word_id, ReviewItem.item_type == 'word')
    )
    result = await db.execute(stats_query)
    total_reviews, correct_reviews = result.first()
    
    # Get groups for this word
    query = select(Group).join(GroupItem).filter(
        and_(
            GroupItem.item_id == word_id,
            GroupItem.item_type == 'word'
        )
    )
    result = await db.execute(query)
    groups = result.scalars().all()
    
    return WordDetail(
        id=word.id,
        word_level=word.word_level,
        japanese=word.japanese,
        kana=word.kana,
        romaji=word.romaji,
        english=word.english,
        stats=WordStats(
            total_reviews=total_reviews or 0,
            correct_reviews=correct_reviews or 0,
            wrong_reviews=(total_reviews or 0) - (correct_reviews or 0)
        ),
        groups=[GroupBase(id=g.id, name=g.name) for g in groups]
    )
