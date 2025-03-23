from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, and_
from database import get_db
from models import StudySession, ReviewItem, Word, Kanji, Group
from schemas import (
    StudySessionListResponse,
    StudySessionDetail,
    StudySessionCreate,
    StudySessionInList,
    ReviewItem as ReviewItemSchema,
    PaginationResponse,
    WordBase,
    KanjiBase
)
from datetime import datetime
from typing import List, Optional

router = APIRouter(prefix="/study-sessions", tags=["study_sessions"])

ITEMS_PER_PAGE = 100

@router.get("", response_model=StudySessionListResponse)
async def list_study_sessions(
    page: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of study sessions"""
    # Calculate offset
    offset = (page - 1) * ITEMS_PER_PAGE
    
    # Get total count
    result = await db.execute(select(func.count()).select_from(StudySession))
    total_count = result.scalar()
    
    # Get study sessions with their stats
    query = (
        select(
            StudySession,
            Group.name.label("group_name"),
            func.count(ReviewItem.id).label("review_items_count")
        )
        .join(Group)
        .outerjoin(ReviewItem)
        .group_by(StudySession.id, Group.name)
        .offset(offset)
        .limit(ITEMS_PER_PAGE)
    )
    
    result = await db.execute(query)
    sessions = result.all()
    
    # Convert to response model
    items = [
        StudySessionInList(
            id=session.id,
            activity_type=session.activity_type,
            group_name=group_name,
            start_time=session.start_time,
            end_time=session.end_time,
            review_items_count=review_items_count or 0
        )
        for session, group_name, review_items_count in sessions
    ]
    
    return StudySessionListResponse(
        items=items,
        pagination=PaginationResponse(
            current_page=page,
            total_pages=(total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE,
            total_items=total_count,
            items_per_page=ITEMS_PER_PAGE
        )
    )

@router.get("/{session_id}", response_model=StudySessionDetail)
async def get_study_session(session_id: int, db: AsyncSession = Depends(get_db)):
    """Get details of a specific study session"""
    query = (
        select(StudySession, Group.name.label("group_name"))
        .join(Group)
        .filter(StudySession.id == session_id)
    )
    result = await db.execute(query)
    session_data = result.first()
    
    if not session_data:
        raise HTTPException(status_code=404, detail="Study session not found")
    
    session, group_name = session_data
    
    # Get review items with their associated words/kanji
    query = (
        select(
            ReviewItem,
            Word,
            Kanji
        )
        .outerjoin(Word, and_(Word.id == ReviewItem.item_id, ReviewItem.item_type == 'word'))
        .outerjoin(Kanji, and_(Kanji.id == ReviewItem.item_id, ReviewItem.item_type == 'kanji'))
        .filter(ReviewItem.study_session_id == session_id)
    )
    result = await db.execute(query)
    review_items_data = result.all()
    
    review_items = []
    correct_count = 0
    for review_item, word, kanji in review_items_data:
        if review_item.correct:
            correct_count += 1
        
        word_data = None
        if word:
            word_data = WordBase(
                id=word.id,
                word_level=word.word_level,
                japanese=word.japanese,
                kana=word.kana,
                romaji=word.romaji,
                english=word.english
            )
        
        kanji_data = None
        if kanji:
            kanji_data = KanjiBase(
                id=kanji.id,
                kanji_level=kanji.kanji_level,
                symbol=kanji.symbol,
                primary_meaning=kanji.primary_meaning,
                primary_reading=kanji.primary_reading,
                primary_reading_type=kanji.primary_reading_type
            )
        
        review_items.append(
            ReviewItemSchema(
                id=review_item.id,
                item_type=review_item.item_type,
                item_id=review_item.item_id,
                study_session_id=review_item.study_session_id,
                correct=review_item.correct,
                created_at=review_item.created_at,
                word=word_data,
                kanji=kanji_data
            )
        )
    
    total_items = len(review_items)
    return StudySessionDetail(
        id=session.id,
        activity_type=session.activity_type,
        group_name=group_name,
        start_time=session.start_time,
        end_time=session.end_time,
        total_items=total_items,
        correct_items=correct_count,
        wrong_items=total_items - correct_count,
        review_items=review_items
    )

@router.post("", response_model=StudySessionDetail)
async def create_study_session(
    session_data: StudySessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new study session"""
    # Verify group exists
    query = select(Group).filter(Group.id == session_data.group_id)
    result = await db.execute(query)
    group = result.scalar()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Create new session
    new_session = StudySession(
        group_id=session_data.group_id,
        activity_type=session_data.activity_type,
        start_time=datetime.utcnow()
    )
    
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    return StudySessionDetail(
        id=new_session.id,
        activity_type=new_session.activity_type,
        group_name=group.name,
        start_time=new_session.start_time,
        end_time=new_session.end_time,
        total_items=0,
        correct_items=0,
        wrong_items=0,
        review_items=[]
    )
