from sqlalchemy import Column, String, Integer, Boolean, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    is_reported = Column(Boolean, default=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    
    user = relationship("User", backref="comments")
    article = relationship("Article", backref="comments")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    
    user = relationship("User", backref="likes")
    article = relationship("Article", backref="likes")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Streak(Base):
    __tablename__ = "streaks"

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, default=1)
    last_login = Column(DateTime(timezone=True), server_default=func.now())
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    user = relationship("User", backref="streak")

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    qr_code_data = Column(String, unique=True, nullable=False)
    is_claimed = Column(Boolean, default=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", backref="rewards")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    claimed_at = Column(DateTime(timezone=True), nullable=True)
