from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import StudySession, ReviewItem, Word, Kanji
from schemas import (
    ReviewItemCreate
)

router = APIRouter(prefix="/review", tags=["review"])

@router.post("/create")
async def create_review_item(
    item_data: ReviewItemCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new review item"""
    # Verify session exists
    query = select(StudySession).filter(StudySession.id == item_data.study_session_id)
    result = await db.execute(query)
    study_session = result.scalar()
    if not study_session:
        raise HTTPException(status_code=404, detail="Study session not found")

    # Verify the item type is valid
    if item_data.item_type not in ['word', 'kanji']:
        raise HTTPException(status_code=400, detail="Invalid item type")
    
    # Verify the item exists
    if item_data.item_type == 'word':
        query = select(Word).filter(Word.id == item_data.item_id)
    else:
        query = select(Kanji).filter(Kanji.id == item_data.item_id)
    result = await db.execute(query)
    item = result.scalar()
    if not item:
        raise HTTPException(status_code=404, detail="Item of type {} not found".format(item_data.item_type))
    
    # Create new review item
    new_review_item = ReviewItem(
        item_type=item_data.item_type,
        item_id=item_data.item_id,
        study_session_id=item_data.study_session_id,
        correct=item_data.correct
    )
    
    db.add(new_review_item)
    await db.commit()
    await db.refresh(new_review_item)