from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from database import get_db
from models import Group, Word, GroupItem
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/favorites", tags=["favorites"])

class FavoriteWordRequest(BaseModel):
    word: str      # japanese
    reading: str   # kana
    romaji: str    # romaji
    meaning: str   # english

FAVORITES_GROUP_NAME = "Favorites"

async def get_or_create_favorites_group(db: AsyncSession) -> Group:
    """Get the favorites group or create it if it doesn't exist"""
    query = select(Group).filter(Group.name == FAVORITES_GROUP_NAME)
    result = await db.execute(query)
    group = result.scalar()
    
    if not group:
        group = Group(name=FAVORITES_GROUP_NAME)
        db.add(group)
        await db.commit()
        await db.refresh(group)
    
    return group

@router.post("/add")
async def add_to_favorites(
    word_data: FavoriteWordRequest,
    db: AsyncSession = Depends(get_db)
):
    """Add a word to favorites"""
    # Get or create favorites group
    favorites_group = await get_or_create_favorites_group(db)
    
    # Check if word already exists
    query = select(Word).filter(
        and_(
            Word.japanese == word_data.word,
            Word.kana == word_data.reading
        )
    )
    result = await db.execute(query)
    word = result.scalar()
    
    # Create word if it doesn't exist
    if not word:
        word = Word(
            japanese=word_data.word,
            kana=word_data.reading,
            romaji=word_data.romaji,
            english=word_data.meaning,
            word_level='1'  # Default level for favorited words
        )
        db.add(word)
        await db.commit()
        await db.refresh(word)
    
    # Check if word is already in favorites
    query = select(GroupItem).filter(
        and_(
            GroupItem.group_id == favorites_group.id,
            GroupItem.item_id == word.id,
            GroupItem.item_type == 'word'
        )
    )
    result = await db.execute(query)
    existing_item = result.scalar()
    
    if existing_item:
        return {"message": "Word is already in favorites"}
    
    # Add word to favorites group
    group_item = GroupItem(
        group_id=favorites_group.id,
        item_id=word.id,
        item_type='word'
    )
    db.add(group_item)
    await db.commit()
    
    return {"message": "Word added to favorites"}
