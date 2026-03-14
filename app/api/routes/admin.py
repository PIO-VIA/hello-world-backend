from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.db.models.user import User, UserRole
from app.schemas.user import UserResponse, UserUpdate
from app.repositories.user_repository import UserRepository
from app.utils.responses import standard_response
from app.core.exceptions import NotFoundError

router = APIRouter()

@router.get("/users")
def list_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    dependencies=[Depends(deps.RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN]))]
):
    """
    List all users (Admin only).
    """
    users = UserRepository.list_users(db, skip=skip, limit=limit)
    return standard_response(
        data=[UserResponse.from_orm(u) for u in users],
        message="Users list retrieved",
        code="USERS_RETRIEVED"
    )

@router.post("/users/{user_id}/ban")
def ban_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """
    Ban a user (Admin only).
    """
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise NotFoundError(message="User not found", code="USER_NOT_FOUND")
    
    user.is_banned = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return standard_response(message="User banned", code="USER_BANNED")

@router.post("/users/{user_id}/unban")
def unban_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """
    Unban a user (Admin only).
    """
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise NotFoundError(message="User not found", code="USER_NOT_FOUND")
    
    user.is_banned = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return standard_response(message="User unbanned", code="USER_UNBANNED")

@router.post("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    role: UserRole,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.RoleChecker([UserRole.SUPER_ADMIN]))
):
    """
    Change user role (Super Admin only).
    """
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise NotFoundError(message="User not found", code="USER_NOT_FOUND")
    
    user.role = role
    db.add(user)
    db.commit()
    db.refresh(user)
    return standard_response(
        data=UserResponse.from_orm(user),
        message=f"User role changed to {role.value}",
        code="USER_ROLE_CHANGED"
    )
