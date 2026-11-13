from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import audit, get_current_user
from app.models import User
from app.schemas_api import LoginRequest, TokenResponse
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == body.email))
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(
        user.id,
        {"role": user.role.value, "agency_id": user.agency_id, "client_id": user.client_id},
    )
    audit(db, user, "login")
    return TokenResponse(access_token=token, role=user.role.value)


@router.get("/me")
def me(user: User = Depends(get_current_user)) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role.value,
        "agency_id": user.agency_id,
        "client_id": user.client_id,
        "client_editing_enabled": user.client_editing_enabled,
    }
