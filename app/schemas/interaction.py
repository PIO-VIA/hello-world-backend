from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse

# Comment Schemas
class CommentBase(BaseModel):
    content: str
    article_id: int

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    user_id: int
    is_reported: bool
    created_at: datetime
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# Like Schemas
class LikeResponse(BaseModel):
    id: int
    user_id: int
    article_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Streak Schemas
class StreakResponse(BaseModel):
    count: int
    last_login: datetime

    class Config:
        from_attributes = True

# Reward Schemas
class RewardBase(BaseModel):
    name: str
    description: Optional[str] = None

class RewardCreate(RewardBase):
    qr_code_data: str

class RewardResponse(RewardBase):
    id: int
    qr_code_data: str
    is_claimed: bool
    claimed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
