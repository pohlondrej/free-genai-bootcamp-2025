from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, union, literal_column, and_
from typing import Optional, List, Union
from database import get_db
from models import Group, Word, Kanji, GroupItem, WordReviewItem, StudySession
from schemas import (
    GroupListResponse, GroupDetail, GroupInList, 
    PaginationResponse, GroupStats, UnifiedItemListResponse,
    UnifiedItemBase
)

router = APIRouter(prefix="/groups", tags=["groups"])

ITEMS_PER_PAGE = 100

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
    
    # Get groups with their stats
    query = (
        select(
            Group,
            func.count(GroupItem.id).filter(GroupItem.item_type == 'word').label("word_count"),
            func.count(GroupItem.id).filter(GroupItem.item_type == 'kanji').label("kanji_count"),
            func.count(StudySession.id).filter(StudySession.completed_at.is_not(None)).label("completed_sessions"),
            func.count(StudySession.id).filter(StudySession.completed_at.is_(None)).label("active_sessions")
        )
        .select_from(Group)
        .outerjoin(GroupItem)
        .outerjoin(StudySession, StudySession.group_id == Group.id)
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
            word_count=word_count or 0,
            kanji_count=kanji_count or 0,
            stats=GroupStats(
                total_items=(word_count or 0) + (kanji_count or 0),
                word_count=word_count or 0,
                kanji_count=kanji_count or 0,
                completed_sessions=completed_sessions or 0,
                active_sessions=active_sessions or 0
            )
        )
        for group, word_count, kanji_count, completed_sessions, active_sessions in groups
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
async def get_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific group"""
    # Get group
    query = select(Group).filter(Group.id == group_id)
    result = await db.execute(query)
    group = result.scalar()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Get stats
    query = (
        select(
            func.count(GroupItem.id).filter(GroupItem.item_type == 'word').label("word_count"),
            func.count(GroupItem.id).filter(GroupItem.item_type == 'kanji').label("kanji_count"),
            func.count(StudySession.id).filter(StudySession.completed_at.is_not(None)).label("completed_sessions"),
            func.count(StudySession.id).filter(StudySession.completed_at.is_(None)).label("active_sessions")
        )
        .select_from(GroupItem)
        .filter(GroupItem.group_id == group_id)
        .outerjoin(StudySession, StudySession.group_id == GroupItem.group_id)
    )
    result = await db.execute(query)
    word_count, kanji_count, completed_sessions, active_sessions = result.first()
    
    # Get words
    query = (
        select(Word)
        .join(GroupItem, and_(GroupItem.item_id == Word.id, GroupItem.item_type == 'word'))
        .filter(GroupItem.group_id == group_id)
    )
    result = await db.execute(query)
    words = result.scalars().all()
    
    # Get kanji
    query = (
        select(Kanji)
        .join(GroupItem, and_(GroupItem.item_id == Kanji.id, GroupItem.item_type == 'kanji'))
        .filter(GroupItem.group_id == group_id)
    )
    result = await db.execute(query)
    kanji = result.scalars().all()
    
    return GroupDetail(
        id=group.id,
        name=group.name,
        words=words,
        kanji=kanji,
        stats=GroupStats(
            total_items=(word_count or 0) + (kanji_count or 0),
            word_count=word_count or 0,
            kanji_count=kanji_count or 0,
            completed_sessions=completed_sessions or 0,
            active_sessions=active_sessions or 0
        )
    )

@router.get("/{group_id}/items", response_model=UnifiedItemListResponse)
async def list_group_items(
    group_id: int,
    page: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of items (words and kanji) in a group"""
    # Verify group exists
    query = select(Group).filter(Group.id == group_id)
    result = await db.execute(query)
    group = result.scalar()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Get total count for pagination
    total_query = select(func.count()).select_from(GroupItem).filter(GroupItem.group_id == group_id)
    result = await db.execute(total_query)
    total_count = result.scalar() or 0
    
    # Calculate offset
    offset = (page - 1) * ITEMS_PER_PAGE
    
    # Create unified query for words and kanji
    words_query = (
        select(
            Word.id,
            literal_column("'word'").label("type"),
            Word.japanese.label("japanese"),
            Word.english.label("english"),
            func.count(WordReviewItem.id).filter(WordReviewItem.correct == True).label("correct_count"),
            func.count(WordReviewItem.id).filter(WordReviewItem.correct == False).label("wrong_count")
        )
        .join(GroupItem, and_(GroupItem.item_id == Word.id, GroupItem.item_type == 'word'))
        .outerjoin(WordReviewItem)
        .filter(GroupItem.group_id == group_id)
        .group_by(Word.id)
    )

    kanji_query = (
        select(
            Kanji.id,
            literal_column("'kanji'").label("type"),
            Kanji.symbol.label("japanese"),
            Kanji.primary_meaning.label("english"),
            literal_column("0").label("correct_count"),
            literal_column("0").label("wrong_count")
        )
        .join(GroupItem, and_(GroupItem.item_id == Kanji.id, GroupItem.item_type == 'kanji'))
        .filter(GroupItem.group_id == group_id)
    )
    
    # Combine queries and apply pagination
    unified_query = union(words_query, kanji_query).offset(offset).limit(ITEMS_PER_PAGE)
    result = await db.execute(unified_query)
    items = result.all()
    
    return UnifiedItemListResponse(
        items=[
            UnifiedItemBase(
                id=item.id,
                type=item.type,
                japanese=item.japanese,
                english=item.english,
                correct_count=item.correct_count or 0,
                wrong_count=item.wrong_count or 0
            )
            for item in items
        ],
        pagination=PaginationResponse(
            current_page=page,
            total_pages=(total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE,
            total_items=total_count,
            items_per_page=ITEMS_PER_PAGE
        )
    )
