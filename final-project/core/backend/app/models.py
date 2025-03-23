from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

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
    groups = relationship(
        "Group",
        secondary="group_items",
        primaryjoin="and_(Word.id == GroupItem.item_id, GroupItem.item_type == 'word')",
        back_populates="words",
        overlaps="groups,kanji"
    )
    reviews = relationship("WordReviewItem", back_populates="word")

class Kanji(Base):
    __tablename__ = "kanji"
    id = Column(Integer, primary_key=True)
    kanji_level = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    primary_meaning = Column(String, nullable=False)
    primary_reading = Column(String, nullable=False)
    primary_reading_type = Column(String, nullable=False)
    
    # Relationships
    groups = relationship(
        "Group",
        secondary="group_items",
        primaryjoin="and_(Kanji.id == GroupItem.item_id, GroupItem.item_type == 'kanji')",
        back_populates="kanji",
        overlaps="groups,words"
    )

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    # Relationships with proper overlaps parameters
    words = relationship(
        "Word",
        secondary="group_items",
        primaryjoin="and_(Group.id == GroupItem.group_id, GroupItem.item_type == 'word')",
        secondaryjoin="Word.id == GroupItem.item_id",
        back_populates="groups",
        overlaps="kanji,groups"
    )
    kanji = relationship(
        "Kanji",
        secondary="group_items",
        primaryjoin="and_(Group.id == GroupItem.group_id, GroupItem.item_type == 'kanji')",
        secondaryjoin="Kanji.id == GroupItem.item_id",
        back_populates="groups",
        overlaps="words,groups"
    )
    study_sessions = relationship("StudySession", back_populates="group")
    study_activities = relationship("StudyActivity", back_populates="group")

class GroupItem(Base):
    __tablename__ = "group_items"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    item_type = Column(String, nullable=False)  # 'word' or 'kanji'
    item_id = Column(Integer, nullable=False)

class StudySession(Base):
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    group = relationship("Group", back_populates="study_sessions")
    activities = relationship("StudyActivity", back_populates="study_session")
    word_reviews = relationship("WordReviewItem", back_populates="study_session")

class StudyActivity(Base):
    __tablename__ = "study_activities"
    id = Column(Integer, primary_key=True)
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    study_session = relationship("StudySession", back_populates="activities")
    group = relationship("Group", back_populates="study_activities")

class WordReviewItem(Base):
    __tablename__ = "word_review_items"
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    word = relationship("Word", back_populates="reviews")
    study_session = relationship("StudySession", back_populates="word_reviews")

class User(Base):
    """Simple key-value store for user settings and configuration"""
    __tablename__ = "user"
    key = Column(String, primary_key=True)
    value = Column(Text)
    
    @classmethod
    async def get_setting(cls, db: AsyncSession, key: str) -> Optional[str]:
        """Get a setting value by key"""
        result = await db.get(cls, key)
        return result.value if result else None
    
    @classmethod
    async def set_setting(cls, db: AsyncSession, key: str, value: str):
        """Set a setting value"""
        setting = await db.get(cls, key)
        if setting:
            setting.value = value
        else:
            setting = cls(key=key, value=value)
            db.add(setting)
        await db.commit()
