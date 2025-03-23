from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, and_
from database import get_db
from models import Kanji, ReviewItem, GroupItem, Group
from schemas import (
    KanjiListResponse,
    KanjiDetail,
    KanjiCreate,
    KanjiInList,
    KanjiStats,
    PaginationResponse,
    GroupBase
)
from typing import List, Optional

router = APIRouter(prefix="/kanji", tags=["kanji"])

ITEMS_PER_PAGE = 100

@router.get("", response_model=KanjiListResponse)
async def list_kanji(
    page: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of kanji"""
    # Calculate offset
    offset = (page - 1) * ITEMS_PER_PAGE
    
    # Get total count
    result = await db.execute(select(func.count()).select_from(Kanji))
    total_count = result.scalar()
    
    # Get kanji with their stats
    query = (
        select(
            Kanji,
            func.count(ReviewItem.id).label("total_reviews"),
            func.sum(case((ReviewItem.correct == True, 1), else_=0)).label("correct_reviews")
        )
        .outerjoin(ReviewItem, and_(ReviewItem.item_id == Kanji.id, ReviewItem.item_type == 'kanji'))
        .group_by(Kanji.id)
        .offset(offset)
        .limit(ITEMS_PER_PAGE)
    )
    
    result = await db.execute(query)
    kanji_list = result.all()
    
    # Convert to response model
    items = [
        KanjiInList(
            id=kanji.id,
            kanji_level=kanji.kanji_level,
            symbol=kanji.symbol,
            primary_meaning=kanji.primary_meaning,
            primary_reading=kanji.primary_reading,
            primary_reading_type=kanji.primary_reading_type,
            stats=KanjiStats(
                total_reviews=total_reviews or 0,
                correct_reviews=correct_reviews or 0,
                wrong_reviews=(total_reviews or 0) - (correct_reviews or 0)
            )
        )
        for kanji, total_reviews, correct_reviews in kanji_list
    ]
    
    return KanjiListResponse(
        items=items,
        pagination=PaginationResponse(
            current_page=page,
            total_pages=(total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE,
            total_items=total_count,
            items_per_page=ITEMS_PER_PAGE
        )
    )

@router.get("/{kanji_id}", response_model=KanjiDetail)
async def get_kanji(kanji_id: int, db: AsyncSession = Depends(get_db)):
    """Get details of a specific kanji"""
    query = select(Kanji).filter(Kanji.id == kanji_id)
    result = await db.execute(query)
    kanji = result.scalar()
    
    if not kanji:
        raise HTTPException(status_code=404, detail="Kanji not found")
    
    # Get review stats
    stats_query = (
        select(
            func.count(ReviewItem.id).label("total_reviews"),
            func.sum(case((ReviewItem.correct == True, 1), else_=0)).label("correct_reviews")
        )
        .select_from(ReviewItem)
        .filter(ReviewItem.item_id == kanji_id, ReviewItem.item_type == 'kanji')
    )
    result = await db.execute(stats_query)
    total_reviews, correct_reviews = result.first()
    
    # Get groups for this kanji
    query = select(Group).join(GroupItem).filter(
        and_(
            GroupItem.item_id == kanji_id,
            GroupItem.item_type == 'kanji'
        )
    )
    result = await db.execute(query)
    groups = result.scalars().all()
    
    return KanjiDetail(
        id=kanji.id,
        kanji_level=kanji.kanji_level,
        symbol=kanji.symbol,
        primary_meaning=kanji.primary_meaning,
        primary_reading=kanji.primary_reading,
        primary_reading_type=kanji.primary_reading_type,
        stats=KanjiStats(
            total_reviews=total_reviews or 0,
            correct_reviews=correct_reviews or 0,
            wrong_reviews=(total_reviews or 0) - (correct_reviews or 0)
        ),
        groups=[GroupBase(id=g.id, name=g.name) for g in groups]
    )
