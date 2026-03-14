from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.db.models.article import ArticleStatus
from app.schemas.user import UserResponse

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Article Schemas
class ArticleBase(BaseModel):
    title: str
    content: str
    category_id: int
    image_url: Optional[str] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    status: Optional[ArticleStatus] = None

class ArticleResponse(ArticleBase):
    id: int
    status: ArticleStatus
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: Optional[UserResponse] = None
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True
