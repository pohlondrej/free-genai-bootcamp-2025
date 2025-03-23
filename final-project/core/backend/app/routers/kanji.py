from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional
from database import get_db
from models import Kanji, Group, GroupItem
from schemas import KanjiListResponse, KanjiDetail, PaginationResponse, KanjiInList, KanjiStats, GroupBase

router = APIRouter(prefix="/kanji", tags=["kanji"])

ITEMS_PER_PAGE = 100

@router.get("", response_model=KanjiListResponse)
async def list_kanji(
    page: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of kanji with their stats"""
    # Calculate offset
    offset = (page - 1) * ITEMS_PER_PAGE
    
    # Get total count
    result = await db.execute(select(func.count()).select_from(Kanji))
    total_count = result.scalar()
    
    # Get kanji with their stats
    # Note: In the future, we'll add KanjiReviewItem table for tracking stats
    query = select(Kanji).offset(offset).limit(ITEMS_PER_PAGE)
    
    result = await db.execute(query)
    kanji_list = result.scalars().all()
    
    # Convert to response model
    # Note: Currently returning 0 for stats as we haven't implemented review tracking yet
    items = [
        KanjiInList(
            id=k.id,
            symbol=k.symbol,
            kanji_level=k.kanji_level,
            primary_reading=k.primary_reading,
            primary_meaning=k.primary_meaning,
            primary_reading_type=k.primary_reading_type,
            stats=KanjiStats(
                correct_count=0,  # To be implemented with review tracking
                wrong_count=0     # To be implemented with review tracking
            )
        )
        for k in kanji_list
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
async def get_kanji(
    kanji_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific kanji"""
    # Get kanji
    query = select(Kanji).filter(Kanji.id == kanji_id)
    result = await db.execute(query)
    kanji = result.scalar()
    
    if not kanji:
        raise HTTPException(status_code=404, detail="Kanji not found")
    
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
        symbol=kanji.symbol,
        kanji_level=kanji.kanji_level,
        primary_reading=kanji.primary_reading,
        primary_reading_type=kanji.primary_reading_type,
        primary_meaning=kanji.primary_meaning,
        stats=KanjiStats(
            correct_count=0,  # To be implemented with review tracking
            wrong_count=0     # To be implemented with review tracking
        ),
        groups=[GroupBase(id=g.id, name=g.name) for g in groups]
    )
