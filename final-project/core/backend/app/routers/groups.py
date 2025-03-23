from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, and_, union, literal_column
from typing import Optional, List, Union
from database import get_db
from models import Group, Word, Kanji, GroupItem, ReviewItem, StudySession
from schemas import (
    GroupListResponse, GroupDetail, GroupInList, 
    PaginationResponse, GroupStats, UnifiedItemListResponse,
    UnifiedItemBase, WordInList, KanjiInList, WordStats, KanjiStats
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
    
    # Get words in this group with their stats
    words_query = (
        select(
            Word,
            func.count(ReviewItem.id).label("total_reviews"),
            func.sum(case((ReviewItem.correct == True, 1), else_=0)).label("correct_reviews")
        )
        .join(GroupItem, and_(GroupItem.item_id == Word.id, GroupItem.item_type == 'word'))
        .outerjoin(ReviewItem, and_(ReviewItem.item_id == Word.id, ReviewItem.item_type == 'word'))
        .filter(GroupItem.group_id == group_id)
        .group_by(Word.id)
    )
    result = await db.execute(words_query)
    words = result.all()
    
    # Get kanji in this group with their stats
    kanji_query = (
        select(
            Kanji,
            func.count(ReviewItem.id).label("total_reviews"),
            func.sum(case((ReviewItem.correct == True, 1), else_=0)).label("correct_reviews")
        )
        .join(GroupItem, and_(GroupItem.item_id == Kanji.id, GroupItem.item_type == 'kanji'))
        .outerjoin(ReviewItem, and_(ReviewItem.item_id == Kanji.id, ReviewItem.item_type == 'kanji'))
        .filter(GroupItem.group_id == group_id)
        .group_by(Kanji.id)
    )
    result = await db.execute(kanji_query)
    kanji_list = result.all()
    
    word_items = [
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
        for word, total_reviews, correct_reviews in words
    ]
    
    kanji_items = [
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
    
    # Get stats
    query = (
        select(
            func.count(StudySession.id).filter(StudySession.completed_at.is_not(None)).label("completed_sessions"),
            func.count(StudySession.id).filter(StudySession.completed_at.is_(None)).label("active_sessions")
        )
        .select_from(StudySession)
        .filter(StudySession.group_id == group_id)
    )
    result = await db.execute(query)
    completed_sessions, active_sessions = result.first()
    
    return GroupDetail(
        id=group.id,
        name=group.name,
        stats=GroupStats(
            total_items=len(word_items) + len(kanji_items),
            word_count=len(word_items),
            kanji_count=len(kanji_items),
            completed_sessions=completed_sessions or 0,
            active_sessions=active_sessions or 0
        ),
        words=word_items,
        kanji=kanji_items
    )

@router.get("/{group_id}/items", response_model=UnifiedItemListResponse)
async def list_group_items(
    group_id: int,
    page: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of all items (words and kanji) in a group with their review stats"""
    # Get total count
    count_query = (
        select(func.count())
        .select_from(GroupItem)
        .filter(GroupItem.group_id == group_id)
    )
    total_count = (await db.execute(count_query)).scalar()
    
    # Calculate offset
    offset = (page - 1) * ITEMS_PER_PAGE
    
    # Get word stats
    word_query = (
        select(
            Word.id,
            literal_column("'word'").label("type"),
            Word.japanese.label("japanese"),
            Word.english.label("english"),
            func.count(ReviewItem.id).label("total_count"),
            func.sum(case((ReviewItem.correct == True, 1), else_=0)).label("correct_count")
        )
        .join(GroupItem, and_(GroupItem.item_id == Word.id, GroupItem.item_type == 'word'))
        .outerjoin(ReviewItem, and_(ReviewItem.item_id == Word.id, ReviewItem.item_type == 'word'))
        .filter(GroupItem.group_id == group_id)
        .group_by(Word.id)
    )
    
    # Get kanji stats
    kanji_query = (
        select(
            Kanji.id,
            literal_column("'kanji'").label("type"),
            Kanji.symbol.label("japanese"),
            Kanji.primary_meaning.label("english"),
            func.count(ReviewItem.id).label("total_count"),
            func.sum(case((ReviewItem.correct == True, 1), else_=0)).label("correct_count")
        )
        .join(GroupItem, and_(GroupItem.item_id == Kanji.id, GroupItem.item_type == 'kanji'))
        .outerjoin(ReviewItem, and_(ReviewItem.item_id == Kanji.id, ReviewItem.item_type == 'kanji'))
        .filter(GroupItem.group_id == group_id)
        .group_by(Kanji.id)
    )
    
    # Combine queries with union and add pagination
    query = (
        word_query.union(kanji_query)
        .offset(offset)
        .limit(ITEMS_PER_PAGE)
    )
    
    result = await db.execute(query)
    items = result.all()
    
    # Convert to response model
    unified_items = [
        UnifiedItemBase(
            id=item.id,
            type=item.type,
            japanese=item.japanese,
            english=item.english,
            correct_count=item.correct_count or 0,
            wrong_count=(item.total_count or 0) - (item.correct_count or 0)
        )
        for item in items
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
