from datetime import timedelta
from typing import Optional, Any
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.core.exceptions import AuthenticationError, AppException
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, Token
from app.core.logging_config import auth_logger

class AuthService:
    @staticmethod
    def register_user(db: Session, user_in: UserCreate):
        user = UserRepository.get_by_email(db, email=user_in.email)
        if user:
            raise AppException(message="The user with this email already exists in the system.", code="EMAIL_EXISTS")
        
        if user_in.matricule:
            user = UserRepository.get_by_matricule(db, matricule=user_in.matricule)
            if user:
                raise AppException(message="The user with this matricule already exists.", code="MATRICULE_EXISTS")
            
        new_user = UserRepository.create(db, obj_in=user_in)
        auth_logger.info(f"New user registered: {new_user.email}")
        return new_user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[Any]:
        user = UserRepository.get_by_email(db, email=email)
        if not user:
            auth_logger.warning(f"Failed login attempt for email: {email} (user not found)")
            return None
        if not verify_password(password, user.hashed_password):
            auth_logger.warning(f"Failed login attempt for email: {email} (wrong password)")
            return None
        if user.is_banned:
            auth_logger.warning(f"Login attempt for banned user: {email}")
            raise AuthenticationError(message="Your account is banned.", code="ACCOUNT_BANNED")
            
        auth_logger.info(f"User logged in: {email}")
        return user

    @staticmethod
    def login(db: Session, email: str, password: str) -> Token:
        user = AuthService.authenticate(db, email=email, password=password)
        if not user:
            raise AuthenticationError(message="Incorrect email or password", code="INVALID_CREDENTIALS")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            token_type="bearer",
        )

    @staticmethod
    def create_super_admin(db: Session, user_in: UserCreate):
        if UserRepository.count_super_admins(db) > 0:
            raise AppException(message="A super admin already exists.", code="SUPER_ADMIN_EXISTS")
            
        from app.db.models.user import UserRole
        user_in.role = UserRole.SUPER_ADMIN
        return UserRepository.create(db, obj_in=user_in)
