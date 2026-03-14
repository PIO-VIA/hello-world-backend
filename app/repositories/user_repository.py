from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_matricule(db: Session, matricule: str) -> Optional[User]:
        return db.query(User).filter(User.matricule == matricule).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create(db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            matricule=obj_in.matricule,
            phone=obj_in.phone,
            department=obj_in.department,
            level=obj_in.level,
            role=obj_in.role if obj_in.role else UserRole.USER,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            db_obj.hashed_password = hashed_password
            del update_data["password"]
            
        for field in update_data:
            setattr(db_obj, field, update_data[field])
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def count_super_admins(db: Session) -> int:
        return db.query(User).filter(User.role == UserRole.SUPER_ADMIN).count()
        
    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()
