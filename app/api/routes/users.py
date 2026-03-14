from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.api import deps
from app.db.models.user import User, UserRole
from app.schemas.user import UserResponse, UserUpdate
from app.repositories.user_repository import UserRepository
from app.utils.responses import standard_response

router = APIRouter()

@router.get("/me")
def read_user_me(
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get current user profile.
    """
    return standard_response(
        data=UserResponse.from_orm(current_user),
        message="Profile retrieved",
        code="PROFILE_RETRIEVED"
    )

@router.put("/me")
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update own profile.
    """
    # Prevent changing role via this endpoint
    user_in.role = None
    user = UserRepository.update(db, db_obj=current_user, obj_in=user_in)
    return standard_response(
        data=UserResponse.from_orm(user),
        message="Profile updated",
        code="PROFILE_UPDATED"
    )

@router.get("/{user_id}", dependencies=[Depends(deps.RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN]))])
def read_user_by_id(
    user_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Get user by ID (Admin only).
    """
    user = UserRepository.get_by_id(db, user_id=user_id)
    if not user:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(message="User not found", code="USER_NOT_FOUND")
    return standard_response(
        data=UserResponse.from_orm(user),
        message="User details retrieved",
        code="USER_RETRIEVED"
    )

@router.put("/{user_id}", dependencies=[Depends(deps.RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN]))])
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
):
    """
    Update a user (Admin only).
    """
    user = UserRepository.get_by_id(db, user_id=user_id)
    if not user:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(message="User not found", code="USER_NOT_FOUND")
    
    # If a non-super-admin tries to update a super-admin or grant super-admin role
    # This logic could be more complex, but for now we keep it simple
    
    user = UserRepository.update(db, db_obj=user, obj_in=user_in)
    return standard_response(
        data=UserResponse.from_orm(user),
        message="User updated successfully",
        code="USER_UPDATED"
    )
