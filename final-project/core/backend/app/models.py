from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func
from typing import List

class Base(DeclarativeBase):
    pass

class Word(Base):
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True)
    word_level = Column(String, nullable=False)
    kana = Column(String, nullable=False)
    japanese = Column(String, nullable=False)
    romaji = Column(String)
    english = Column(String, nullable=False)
    groups = relationship("Group", secondary="group_items", 
                        primaryjoin="and_(Word.id==group_items.c.item_id, "
                                  "group_items.c.item_type=='word')",
                        back_populates="words")
    reviews = relationship("WordReviewItem", back_populates="word")

class Kanji(Base):
    __tablename__ = "kanji"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    kanji_level = Column(String, nullable=False)
    primary_meaning = Column(String, nullable=False)
    primary_reading = Column(String, nullable=False)
    primary_reading_type = Column(String, nullable=False)
    groups = relationship("Group", secondary="group_items",
                        primaryjoin="and_(Kanji.id==group_items.c.item_id, "
                                  "group_items.c.item_type=='kanji')",
                        back_populates="kanji")

class GroupItem(Base):
    __tablename__ = "group_items"
    
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    item_type = Column(String, nullable=False)
    item_id = Column(Integer, nullable=False)

class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    words = relationship("Word", secondary="group_items",
                      secondaryjoin="and_(Group.id==group_items.c.group_id, "
                                  "group_items.c.item_type=='word')",
                      back_populates="groups")
    kanji = relationship("Kanji", secondary="group_items",
                      secondaryjoin="and_(Group.id==group_items.c.group_id, "
                                  "group_items.c.item_type=='kanji')",
                      back_populates="groups")
    study_sessions = relationship("StudySession", back_populates="group")
    study_activities = relationship("StudyActivity", back_populates="group")

class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    group = relationship("Group", back_populates="study_sessions")
    activities = relationship("StudyActivity", back_populates="session")
    word_reviews = relationship("WordReviewItem", back_populates="session")

class StudyActivity(Base):
    __tablename__ = "study_activities"
    
    id = Column(Integer, primary_key=True)
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    session = relationship("StudySession", back_populates="activities")
    group = relationship("Group", back_populates="study_activities")

class WordReviewItem(Base):
    __tablename__ = "word_review_items"
    
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    word = relationship("Word", back_populates="reviews")
    session = relationship("StudySession", back_populates="word_reviews")

class User(Base):
    """Configuration store for user settings and preferences"""
    __tablename__ = "user"
    
    key = Column(String, primary_key=True)
    value = Column(String)

    @classmethod
    async def get_setting(cls, db, key: str) -> str | None:
        """Get a configuration value by key"""
        result = await db.execute(
            text("SELECT value FROM user WHERE key = :key"),
            {"key": key}
        )
        row = result.first()
        return row[0] if row else None

    @classmethod
    async def set_setting(cls, db, key: str, value: str) -> None:
        """Set a configuration value"""
        await db.execute(
            text("INSERT INTO user (key, value) VALUES (:key, :value) "
                 "ON CONFLICT (key) DO UPDATE SET value = :value"),
            {"key": key, "value": value}
        )
        await db.commit()
