import enum
from sqlalchemy import Column, String, Integer, Enum, Boolean, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class ArticleStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    PUBLISHED = "PUBLISHED"

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    articles = relationship("Article", back_populates="category")

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum(ArticleStatus), default=ArticleStatus.DRAFT, nullable=False)
    image_url = Column(String, nullable=True)
    
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    author = relationship("User", backref="articles")
    category = relationship("Category", back_populates="articles")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
