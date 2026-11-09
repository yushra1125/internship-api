from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserAuthResponse,
    RefreshTokenRequest,
)

from app.services.auth_services import (
    register_user,
    authenticate_user,
    create_user_session,
    refresh_user_session,
    logout_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserAuthResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    return register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        login_data.email,
        login_data.password
    )

    return create_user_session(db, user)


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    return refresh_user_session(db, token_data.refresh_token)


@router.post("/logout")
def logout(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    return logout_user(db, token_data.refresh_token)


@router.get("/me", response_model=UserAuthResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user