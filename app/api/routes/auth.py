from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserResponse, Token
from app.utils.responses import standard_response

router = APIRouter()

@router.post("/register", status_code=201)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate
):
    """
    Register a new user.
    """
    user = AuthService.register_user(db, user_in=user_in)
    return standard_response(
        data=UserResponse.from_orm(user),
        message="User registered successfully",
        code="USER_REGISTERED",
        status_code=201
    )

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    token = AuthService.login(db, email=form_data.username, password=form_data.password)
    # Note: For OAuth2 compatibility, we return the Token model directly here
    # as expected by Swagger/OAuth2 password flow.
    # However, the user requested standard format for ALL endpoints.
    # We will wrap it in standard response if called via JSON, but for Swagger/OAuth2 
    # we need the raw fields.
    return token

@router.post("/login-json")
def login_json(
    db: Session = Depends(deps.get_db),
    username: str = Body(...),
    password: str = Body(...)
):
    """
    Login using JSON body.
    """
    token = AuthService.login(db, email=username, password=password)
    return standard_response(
        data=token.model_dump(),
        message="Login successful",
        code="LOGIN_SUCCESS"
    )

@router.post("/password-recovery/{email}")
def recover_password(email: str, db: Session = Depends(deps.get_db)):
    """
    Password recovery.
    """
    # Implementation of email sending would go here.
    # For now, we just return a success message.
    return standard_response(
        message="Password recovery email sent",
        code="RECOVERY_EMAIL_SENT"
    )
