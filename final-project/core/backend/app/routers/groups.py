from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List, Union
from database import get_db
from models import Group, Word, Kanji, WordGroup, WordReviewItem
from schemas import (
    GroupListResponse, GroupDetail, GroupInList, 
    PaginationResponse, GroupStats, UnifiedItemListResponse
)

router = APIRouter(prefix="/groups", tags=["groups"])

@router.get("", response_model=GroupListResponse)
async def list_groups(
    page: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of groups with their item counts"""
    # Calculate offset
    offset = (page - 1) * 100
    
    # Get total count
    result = await db.execute(select(func.count()).select_from(Group))
    total_count = result.scalar()
    
    # Get groups with their word counts
    query = select(
        Group,
        func.count(WordGroup.word_id).label("item_count")
    ).outerjoin(WordGroup).group_by(Group.id).offset(offset).limit(100)
    
    result = await db.execute(query)
    groups = result.all()
    
    # Convert to response model
    items = [
        GroupInList(
            id=group.id,
            name=group.name,
            item_count=count or 0
        )
        for group, count in groups
    ]
    
    return GroupListResponse(
        items=items,
        pagination=PaginationResponse(
            current_page=page,
            total_pages=(total_count + 99) // 100,  # ceiling division
            total_items=total_count
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
    
    # Get total item count
    query = select(func.count(WordGroup.word_id)).filter(WordGroup.group_id == group_id)
    result = await db.execute(query)
    total_items = result.scalar() or 0
    
    return GroupDetail(
        id=group.id,
        name=group.name,
        stats=GroupStats(
            total_item_count=total_items
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
    
    # Get words in this group with their stats
    word_query = select(
        Word,
        func.count(WordReviewItem.id).filter(WordReviewItem.correct == True).label("correct_count"),
        func.count(WordReviewItem.id).filter(WordReviewItem.correct == False).label("wrong_count")
    ).join(WordGroup).filter(
        WordGroup.group_id == group_id
    ).outerjoin(WordReviewItem).group_by(Word.id)
    
    result = await db.execute(word_query)
    words = result.all()
    
    # Convert to unified response format
    items = []
    for word, correct, wrong in words:
        items.append({
            "id": word.id,
            "type": "word",
            "japanese": word.japanese,
            "english": word.english,
            "correct_count": correct or 0,
            "wrong_count": wrong or 0
        })
    
    # Get total count for pagination
    total_query = select(func.count()).select_from(WordGroup).filter(WordGroup.group_id == group_id)
    result = await db.execute(total_query)
    total_count = result.scalar() or 0
    
    # Apply pagination
    offset = (page - 1) * 100
    items = items[offset:offset + 100]
    
    return UnifiedItemListResponse(
        items=items,
        pagination=PaginationResponse(
            current_page=page,
            total_pages=(total_count + 99) // 100,
            total_items=total_count,
            items_per_page=100
        )
    )
