import hashlib
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.session import UserSession
from app.schemas.auth import RegisterRequest
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


def register_user(db: Session, user_data: RegisterRequest):
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
        role="student",
        status="active"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


def create_user_session(db: Session, user: User):
    new_session = UserSession(
        user_id=user.id,
        refresh_token_hash="temporary",
        expires_at=datetime.now(timezone.utc)
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    access_token = create_access_token(user.id, new_session.id)
    refresh_token = create_refresh_token(user.id, new_session.id)

    new_session.refresh_token_hash = hashlib.sha256(
        refresh_token.encode()
    ).hexdigest()

    expiry_timestamp = decode_token(refresh_token)["exp"]
    new_session.expires_at = datetime.fromtimestamp(
        expiry_timestamp, tz=timezone.utc
    )

    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_user_session(db: Session, refresh_token: str):
    try:
        payload = decode_token(refresh_token)
    except Exception as e:
        print("Refresh token error:", type(e).__name__, str(e))
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Refresh token required"
        )

    user_id = int(payload["sub"])
    session_id = payload["sid"]

    user_session = db.query(UserSession).filter(
        UserSession.id == session_id,
        UserSession.user_id == user_id
    ).first()

    if not user_session:
        raise HTTPException(status_code=401, detail="Session not found")

    if user_session.revoked_at is not None:
        raise HTTPException(status_code=401, detail="Session revoked")

    expires_at = user_session.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired")

    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

    if token_hash != user_session.refresh_token_hash:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).filter(User.id == user_id).first()

    if not user or user.status != "active":
        raise HTTPException(status_code=401, detail="User inactive")

    new_access_token = create_access_token(user.id, user_session.id)
    new_refresh_token = create_refresh_token(user.id, user_session.id)

    user_session.refresh_token_hash = hashlib.sha256(
        new_refresh_token.encode()
    ).hexdigest()

    expiry_timestamp = decode_token(new_refresh_token)["exp"]
    user_session.expires_at = datetime.fromtimestamp(
        expiry_timestamp, tz=timezone.utc
    )

    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


def logout_user(db: Session, refresh_token: str):
    try:
        payload = decode_token(refresh_token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Refresh token required"
        )

    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

    user_session = db.query(UserSession).filter(
        UserSession.id == payload["sid"],
        UserSession.user_id == int(payload["sub"])
    ).first()

    if not user_session or user_session.refresh_token_hash != token_hash:
        raise HTTPException(status_code=401, detail="Invalid session")

    if user_session.revoked_at is None:
        user_session.revoked_at = datetime.now(timezone.utc)
        db.commit()

    return {"message": "Logged out successfully"}