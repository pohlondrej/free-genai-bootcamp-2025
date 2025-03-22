from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from database import get_db
from models import Word, WordReviewItem, WordGroup, Group
from schemas import WordListResponse, WordDetail, PaginationResponse, WordInList, WordStats, GroupBase

router = APIRouter(prefix="/words", tags=["words"])

@router.get("", response_model=WordListResponse)
async def list_words(
    page: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of words with their stats"""
    # Calculate offset
    offset = (page - 1) * 100
    
    # Get total count
    result = await db.execute(select(func.count()).select_from(Word))
    total_count = result.scalar()
    
    # Get words with their review stats
    query = select(
        Word,
        func.count(WordReviewItem.id).filter(WordReviewItem.correct == True).label("correct_count"),
        func.count(WordReviewItem.id).filter(WordReviewItem.correct == False).label("wrong_count")
    ).outerjoin(WordReviewItem).group_by(Word.id).offset(offset).limit(100)
    
    result = await db.execute(query)
    words = result.all()
    
    # Convert to response model
    items = [
        WordInList(
            japanese=word.japanese,
            romaji=word.romaji,
            english=word.english,
            correct_count=correct or 0,
            wrong_count=wrong or 0
        )
        for word, correct, wrong in words
    ]
    
    return WordListResponse(
        items=items,
        pagination=PaginationResponse(
            current_page=page,
            total_pages=(total_count + 99) // 100,  # ceiling division
            total_items=total_count
        )
    )

@router.get("/{word_id}", response_model=WordDetail)
async def get_word(
    word_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific word"""
    # Get word with its review stats and groups
    query = select(
        Word,
        func.count(WordReviewItem.id).filter(WordReviewItem.correct == True).label("correct_count"),
        func.count(WordReviewItem.id).filter(WordReviewItem.correct == False).label("wrong_count")
    ).outerjoin(WordReviewItem).filter(Word.id == word_id).group_by(Word.id)
    
    result = await db.execute(query)
    word_data = result.first()
    
    if not word_data:
        raise HTTPException(status_code=404, detail="Word not found")
    
    word, correct, wrong = word_data
    
    # Get groups for this word
    query = select(Group).join(WordGroup).filter(WordGroup.word_id == word_id)
    result = await db.execute(query)
    groups = result.scalars().all()
    
    return WordDetail(
        id=word.id,
        japanese=word.japanese,
        romaji=word.romaji,
        english=word.english,
        stats=WordStats(
            correct_count=correct or 0,
            wrong_count=wrong or 0
        ),
        groups=[GroupBase(id=g.id, name=g.name) for g in groups]
    )
