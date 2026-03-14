import enum
from sqlalchemy import Column, String, Integer, Enum, Boolean, DateTime, func
from app.db.base import Base

class UserRole(str, enum.Enum):
    VISITOR = "VISITOR"
    USER = "USER"
    EDITOR = "EDITOR"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    matricule = Column(String, unique=True, index=True, nullable=True)
    department = Column(String, nullable=True)
    level = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_banned = Column(Boolean(), default=False)
    avatar_url = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
