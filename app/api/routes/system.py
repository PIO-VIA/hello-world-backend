from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.api import deps
from app.db.models.user import User, UserRole
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserResponse, SuperAdminCreate, UserUpdate
from app.utils.responses import standard_response

router = APIRouter()

@router.post("/create-super-admin", status_code=201)
def create_super_admin(
    *,
    db: Session = Depends(deps.get_db),
    user_in: SuperAdminCreate
):
    """
    Create the first Super Admin. Only works if no Super Admin exists.
    """
    # Convert SuperAdminCreate to UserCreate for AuthService
    full_user_in = UserCreate(email=user_in.email, password=user_in.password)
    user = AuthService.create_super_admin(db, user_in=full_user_in)
    return standard_response(
        data=UserResponse.from_orm(user),
        message="Super Admin created successfully",
        code="SUPER_ADMIN_CREATED",
        status_code=201
    )

@router.put("/me")
def update_super_admin_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.RoleChecker([UserRole.SUPER_ADMIN])),
):
    """
    Update super admin own profile.
    """
    from app.repositories.user_repository import UserRepository
    user = UserRepository.update(db, db_obj=current_user, obj_in=user_in)
    return standard_response(
        data=UserResponse.from_orm(user),
        message="Super Admin profile updated",
        code="SUPER_ADMIN_PROFILE_UPDATED"
    )
