from typing import Optional, Any
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.db.models.user import UserRole

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    matricule: Optional[str] = None
    department: Optional[str] = None
    level: Optional[str] = None
    role: Optional[UserRole] = UserRole.USER
    is_active: Optional[bool] = True
    avatar_url: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    full_name: str
    matricule: str
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class UserResponse(UserInDBBase):
    pass

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
