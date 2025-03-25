from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, and_, Text, func, select
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List, Optional

Base = declarative_base()

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    word_level = Column(String, nullable=False)
    japanese = Column(String, nullable=False)
    kana = Column(String, nullable=False)
    romaji = Column(String)
    english = Column(String, nullable=False)
    
    # Relationships
    reviews = relationship(
        "ReviewItem",
        primaryjoin="and_(Word.id == foreign(ReviewItem.item_id), ReviewItem.item_type == 'word')",
        back_populates="word"
    )
    group_items = relationship(
        "GroupItem",
        primaryjoin="and_(Word.id == foreign(GroupItem.item_id), GroupItem.item_type == 'word')",
        back_populates="word"
    )

class Kanji(Base):
    __tablename__ = "kanji"
    id = Column(Integer, primary_key=True)
    kanji_level = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    primary_meaning = Column(String, nullable=False)
    primary_reading = Column(String, nullable=False)
    primary_reading_type = Column(String, nullable=False)
    
    # Relationships
    reviews = relationship(
        "ReviewItem",
        primaryjoin="and_(Kanji.id == foreign(ReviewItem.item_id), ReviewItem.item_type == 'kanji')",
        back_populates="kanji"
    )
    group_items = relationship(
        "GroupItem",
        primaryjoin="and_(Kanji.id == foreign(GroupItem.item_id), GroupItem.item_type == 'kanji')",
        back_populates="kanji"
    )

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    # Relationships
    items = relationship("GroupItem", back_populates="group")
    study_sessions = relationship("StudySession", back_populates="group")

class GroupItem(Base):
    __tablename__ = "group_items"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    item_id = Column(Integer, nullable=False)
    item_type = Column(String, nullable=False)  # 'word' or 'kanji'
    
    # Relationships
    group = relationship("Group", back_populates="items")
    word = relationship(
        "Word",
        primaryjoin="and_(GroupItem.item_id == Word.id, GroupItem.item_type == 'word')",
        foreign_keys=[item_id],
        back_populates="group_items"
    )
    kanji = relationship(
        "Kanji",
        primaryjoin="and_(GroupItem.item_id == Kanji.id, GroupItem.item_type == 'kanji')",
        foreign_keys=[item_id],
        back_populates="group_items"
    )

class StudySession(Base):
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    activity_type = Column(String, nullable=False)  # e.g. 'review', 'learn'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    group = relationship("Group", back_populates="study_sessions")
    review_items = relationship("ReviewItem", back_populates="study_session")

class ReviewItem(Base):
    __tablename__ = "review_items"
    id = Column(Integer, primary_key=True)
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    item_id = Column(Integer, nullable=False)
    item_type = Column(String, nullable=False)  # 'word' or 'kanji'
    correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    study_session = relationship("StudySession", back_populates="review_items")
    word = relationship(
        "Word",
        primaryjoin="and_(ReviewItem.item_id == Word.id, ReviewItem.item_type == 'word')",
        foreign_keys=[item_id],
        back_populates="reviews"
    )
    kanji = relationship(
        "Kanji",
        primaryjoin="and_(ReviewItem.item_id == Kanji.id, ReviewItem.item_type == 'kanji')",
        foreign_keys=[item_id],
        back_populates="reviews"
    )

class User(Base):
    __tablename__ = "user"
    key = Column(String, primary_key=True)
    value = Column(String)

    @classmethod
    async def get_setting(cls, db: AsyncSession, key: str) -> Optional[str]:
        """Get a user setting by key"""
        result = await db.execute(select(cls).filter(cls.key == key))
        setting = result.scalar()
        return setting.value if setting else None

    @classmethod
    async def set_setting(cls, db: AsyncSession, key: str, value: str):
        """Set a user setting"""
        setting = cls(key=key, value=value)
        db.add(setting)
        await db.commit()
