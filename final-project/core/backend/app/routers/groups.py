from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, and_, literal
from database import get_db
from models import Group, Word, Kanji, GroupItem, ReviewItem, StudySession
from schemas import (
    GroupListResponse,
    GroupDetail,
    GroupCreate,
    GroupInList,
    GroupStats,
    PaginationResponse,
    WordInList,
    KanjiInList,
    WordStats,
    KanjiStats,
    UnifiedItemBase,
    UnifiedItemListResponse
)
from typing import List, Optional

router = APIRouter(prefix="/groups", tags=["groups"])

ITEMS_PER_PAGE = 30

@router.get("", response_model=GroupListResponse)
async def list_groups(
    page: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of groups with their item counts"""
    # Calculate offset
    offset = (page - 1) * ITEMS_PER_PAGE
    
    # Get total count
    result = await db.execute(select(func.count()).select_from(Group))
    total_count = result.scalar()
    
    # Get paginated list of groups with their stats
    query = (
        select(
            Group.id,
            Group.name,
            func.count(case((GroupItem.item_type == 'word', 1), else_=None)).label("word_count"),
            func.count(case((GroupItem.item_type == 'kanji', 1), else_=None)).label("kanji_count"),
        )
        .select_from(Group)
        .outerjoin(GroupItem)
        .group_by(Group.id)
        .offset(offset)
        .limit(ITEMS_PER_PAGE)
    )
    
    result = await db.execute(query)
    groups = result.all()
    
    # Convert to response model
    items = [
        GroupInList(
            id=group.id,
            name=group.name,
            word_count=group.word_count or 0,
            kanji_count=group.kanji_count or 0,
            total_items=(group.word_count or 0) + (group.kanji_count or 0)
        )
        for group in groups
    ]
    
    return GroupListResponse(
        items=items,
        pagination=PaginationResponse(
            current_page=page,
            total_pages=(total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE,
            total_items=total_count,
            items_per_page=ITEMS_PER_PAGE
        )
    )

@router.get("/{group_id}", response_model=GroupDetail)
async def get_group(group_id: int, db: AsyncSession = Depends(get_db)):
    """Get details of a specific group"""
    # Get group
    query = select(Group).filter(Group.id == group_id)
    result = await db.execute(query)
    group = result.scalar()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Get stats; TODO: Fix the number of completed sessions loading incorrectly
    stats_query = (
        select(
            func.count(StudySession.id).filter(StudySession.completed_at.is_not(None)).label("completed_sessions"),
            func.count(StudySession.id).filter(and_(StudySession.completed_at.is_(None), StudySession.created_at.is_not(None))).label("active_sessions"),
            func.count(GroupItem.id).filter(GroupItem.item_type == 'word').label("word_count"),
            func.count(GroupItem.id).filter(GroupItem.item_type == 'kanji').label("kanji_count")
        )
        .select_from(GroupItem)
        .filter(GroupItem.group_id == group_id)
        .outerjoin(StudySession, StudySession.group_id == GroupItem.group_id)
        .group_by(GroupItem.group_id)
    )
    result = await db.execute(stats_query)
    completed_sessions, active_sessions, word_count, kanji_count = result.first()
    
    stats = GroupStats(
        total_items=(word_count or 0) + (kanji_count or 0),
        word_count=word_count or 0,
        kanji_count=kanji_count or 0,
        completed_sessions=completed_sessions or 0,
        active_sessions=active_sessions or 0
    )
    
    return GroupDetail(
        id=group.id,
        name=group.name,
        stats=stats
    )

@router.get("/{group_id}/items", response_model=UnifiedItemListResponse)
async def list_group_items(
    group_id: int,
    page: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of items (words and kanji) in a group"""
    # Check if group exists
    result = await db.execute(select(func.count()).select_from(GroupItem).filter(GroupItem.group_id == group_id))
    total_count = result.scalar()
    
    if total_count == 0:
        raise HTTPException(status_code=404, detail="Group not found or empty")
    
    # Calculate offset
    offset = (page - 1) * ITEMS_PER_PAGE
    
    # Get unified list of words and kanji with their stats
    words_query = (
        select(
            Word.id,
            Word.word_level.label("level"),
            Word.japanese.label("name"),
            literal('word').label("item_type"),
            func.count(ReviewItem.id).label("total_reviews"),
            func.sum(case((ReviewItem.correct == True, 1), else_=0)).label("correct_reviews")
        )
        .join(GroupItem, and_(GroupItem.item_id == Word.id, GroupItem.item_type == 'word'))
        .outerjoin(ReviewItem, and_(ReviewItem.item_id == Word.id, ReviewItem.item_type == 'word'))
        .filter(GroupItem.group_id == group_id)
        .group_by(Word.id)
    )
    
    kanji_query = (
        select(
            Kanji.id,
            Kanji.kanji_level.label("level"),
            Kanji.symbol.label("name"),
            literal('kanji').label("item_type"),
            func.count(ReviewItem.id).label("total_reviews"),
            func.sum(case((ReviewItem.correct == True, 1), else_=0)).label("correct_reviews")
        )
        .join(GroupItem, and_(GroupItem.item_id == Kanji.id, GroupItem.item_type == 'kanji'))
        .outerjoin(ReviewItem, and_(ReviewItem.item_id == Kanji.id, ReviewItem.item_type == 'kanji'))
        .filter(GroupItem.group_id == group_id)
        .group_by(Kanji.id)
    )
    
    # Combine queries with UNION
    unified_query = words_query.union(kanji_query).offset(offset).limit(ITEMS_PER_PAGE)
    result = await db.execute(unified_query)
    items_data = result.all()
    
    # Convert to response model
    unified_items = [
        UnifiedItemBase(
            id=item.id,
            item_type=item.item_type,
            name=item.name,
            level=item.level,
            total_reviews=item.total_reviews or 0,
            correct_reviews=item.correct_reviews or 0,
            wrong_reviews=(item.total_reviews or 0) - (item.correct_reviews or 0)
        )
        for item in items_data
    ]
    
    return UnifiedItemListResponse(
        items=unified_items,
        pagination=PaginationResponse(
            current_page=page,
            total_pages=(total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE,
            total_items=total_count,
            items_per_page=ITEMS_PER_PAGE
        )
    )
