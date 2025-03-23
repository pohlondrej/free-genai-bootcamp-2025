from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db
from models import StudySession, Group, WordReviewItem
from schemas import (
    StudySessionListResponse,
    StudySessionDetail,
    StudySessionCreate,
    StudySessionInList,
    PaginationResponse
)
from datetime import datetime, timedelta
from typing import List, Optional

router = APIRouter(
    prefix="/study_sessions",
    tags=["study_sessions"]
)

@router.get("", response_model=StudySessionListResponse)
async def list_study_sessions(
    activity_type: Optional[str] = None,
    page: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Get all study sessions, optionally filtered by activity type"""
    query = select(StudySession)
    if activity_type:
        query = query.filter(StudySession.activity_type == activity_type)
    
    # Add pagination
    offset = (page - 1) * 20
    query = query.order_by(StudySession.created_at.desc()).offset(offset).limit(20)
    
    # Get total count for pagination
    count_query = select(func.count()).select_from(StudySession)
    if activity_type:
        count_query = count_query.filter(StudySession.activity_type == activity_type)
    
    result = await db.execute(query)
    sessions = result.scalars().all()
    total_count = (await db.execute(count_query)).scalar()
    
    # Convert to response model
    items = []
    for session in sessions:
        # Get group name
        group_query = select(Group).filter(Group.id == session.group_id)
        group = (await db.execute(group_query)).scalar()
        
        # Get review count
        review_count_query = (
            select(func.count())
            .select_from(WordReviewItem)
            .filter(WordReviewItem.study_session_id == session.id)
        )
        review_count = (await db.execute(review_count_query)).scalar()
        
        items.append(StudySessionInList(
            id=session.id,
            activity_type=session.activity_type,
            group_name=group.name if group else "Unknown Group",
            start_time=session.created_at,
            end_time=session.completed_at,
            review_items_count=review_count
        ))
    
    return StudySessionListResponse(
        items=items,
        pagination=PaginationResponse(
            current_page=page,
            total_pages=(total_count + 19) // 20,  # Ceiling division
            total_items=total_count,
            items_per_page=20
        )
    )

@router.get("/{session_id}", response_model=StudySessionDetail)
async def get_study_session(session_id: int, db: AsyncSession = Depends(get_db)):
    """Get details of a specific study session"""
    query = select(StudySession).filter(StudySession.id == session_id)
    result = await db.execute(query)
    session = result.scalar()
    
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    
    # Get group info
    group_query = select(Group).filter(Group.id == session.group_id)
    group = (await db.execute(group_query)).scalar()
    
    # Get review stats
    review_stats_query = (
        select(
            func.count().label("total"),
            func.sum(WordReviewItem.correct.cast(func.int)).label("correct")
        )
        .select_from(WordReviewItem)
        .filter(WordReviewItem.study_session_id == session_id)
    )
    stats = (await db.execute(review_stats_query)).first()
    
    return StudySessionDetail(
        id=session.id,
        activity_type=session.activity_type,
        group_id=session.group_id,
        group_name=group.name if group else "Unknown Group",
        start_time=session.created_at,
        end_time=session.completed_at,
        total_items=stats.total or 0,
        correct_items=stats.correct or 0
    )

@router.post("", response_model=dict)
async def create_study_session(
    session: StudySessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new study session"""
    # Verify group exists
    group_query = select(Group).filter(Group.id == session.group_id)
    group = (await db.execute(group_query)).scalar()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Create study session
    new_session = StudySession(
        group_id=session.group_id,
        activity_type=session.activity_type,
        created_at=datetime.utcnow()
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    return {
        "id": new_session.id,
        "group_id": new_session.group_id,
        "activity_type": new_session.activity_type
    }
