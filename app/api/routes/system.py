from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.api import deps
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserResponse
from app.utils.responses import standard_response

router = APIRouter()

@router.post("/create-super-admin", status_code=201)
def create_super_admin(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate
):
    """
    Create the first Super Admin. Only works if no Super Admin exists.
    """
    user = AuthService.create_super_admin(db, user_in=user_in)
    return standard_response(
        data=UserResponse.from_orm(user),
        message="Super Admin created successfully",
        code="SUPER_ADMIN_CREATED",
        status_code=201
    )
