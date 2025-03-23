from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Table, select
from sqlalchemy.orm import relationship, Mapped
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
    groups: Mapped[List["Group"]] = relationship(
        "Group",
        secondary="group_items",
        primaryjoin="and_(Word.id == GroupItem.item_id, GroupItem.item_type == 'word')",
        secondaryjoin="Group.id == GroupItem.group_id",
        back_populates="words",
        overlaps="groups,kanji"
    )
    reviews: Mapped[List["WordReviewItem"]] = relationship("WordReviewItem", back_populates="word")

class Kanji(Base):
    __tablename__ = "kanji"
    id = Column(Integer, primary_key=True)
    kanji_level = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    primary_meaning = Column(String, nullable=False)
    primary_reading = Column(String, nullable=False)
    primary_reading_type = Column(String, nullable=False)

    # Relationships
    groups: Mapped[List["Group"]] = relationship(
        "Group",
        secondary="group_items",
        primaryjoin="and_(Kanji.id == GroupItem.item_id, GroupItem.item_type == 'kanji')",
        secondaryjoin="Group.id == GroupItem.group_id",
        back_populates="kanji",
        overlaps="groups,words"
    )

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationships
    words: Mapped[List[Word]] = relationship(
        Word,
        secondary="group_items",
        primaryjoin="Group.id == GroupItem.group_id",
        secondaryjoin="and_(Word.id == GroupItem.item_id, GroupItem.item_type == 'word')",
        back_populates="groups",
        overlaps="groups,kanji"
    )
    kanji: Mapped[List[Kanji]] = relationship(
        Kanji,
        secondary="group_items",
        primaryjoin="Group.id == GroupItem.group_id",
        secondaryjoin="and_(Kanji.id == GroupItem.item_id, GroupItem.item_type == 'kanji')",
        back_populates="groups",
        overlaps="groups,words"
    )
    study_sessions: Mapped[List["StudySession"]] = relationship("StudySession", back_populates="group")

class GroupItem(Base):
    __tablename__ = "group_items"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    item_type = Column(String, nullable=False)
    item_id = Column(Integer, nullable=False)

class StudySession(Base):
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    activity_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    group = relationship("Group", back_populates="study_sessions")
    word_reviews: Mapped[List["WordReviewItem"]] = relationship("WordReviewItem", back_populates="study_session")

class WordReviewItem(Base):
    __tablename__ = "word_review_items"
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    study_session = relationship("StudySession", back_populates="word_reviews")
    word = relationship("Word", back_populates="reviews")

class User(Base):
    """Simple key-value store for user settings and configuration"""
    __tablename__ = "user"
    key = Column(String, primary_key=True)
    value = Column(String)
    
    @classmethod
    async def get_setting(cls, db: AsyncSession, key: str) -> Optional[str]:
        """Get a setting value by key"""
        result = await db.execute(
            select(cls).filter(cls.key == key)
        )
        setting = result.scalar()
        return setting.value if setting else None

    @classmethod
    async def set_setting(cls, db: AsyncSession, key: str, value: str) -> None:
        """Set a setting value by key"""
        setting = await db.execute(
            select(cls).filter(cls.key == key)
        )
        existing = setting.scalar()
        
        if existing:
            existing.value = value
        else:
            new_setting = cls(key=key, value=value)
            db.add(new_setting)
        
        await db.commit()
