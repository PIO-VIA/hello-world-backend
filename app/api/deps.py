from typing import Generator, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import SessionLocal
from app.db.models.user import User, UserRole
from app.schemas.user import TokenPayload
from app.repositories.user_repository import UserRepository
from app.core.exceptions import AuthenticationError, PermissionDeniedError

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise AuthenticationError(
            message="Could not validate credentials",
            code="COULD_NOT_VALIDATE_CREDENTIALS",
        )
    user = UserRepository.get_by_id(db, user_id=token_data.sub)
    if not user:
        raise AuthenticationError(message="User not found", code="USER_NOT_FOUND")
    if not user.is_active:
        raise AuthenticationError(message="Inactive user", code="USER_INACTIVE")
    if user.is_banned:
        raise AuthenticationError(message="Banned user", code="USER_BANNED")
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise PermissionDeniedError(
                message=f"The user doesn't have enough privileges. Required: {[r.value for r in self.allowed_roles]}",
                code="INSUFFICIENT_PRIVILEGES"
            )
        return user
