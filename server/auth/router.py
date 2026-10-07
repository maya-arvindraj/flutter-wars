from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session

from auth.google import verify_google_token
from auth.jwt import create_access_token
from auth.service import get_user_team
from core.dependencies import (
    AuthenticatedPrincipal,
    get_db,
    get_principal,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


class GoogleLoginRequest(BaseModel):
    credential: str


@router.post("/google")
def google_login(
    request: GoogleLoginRequest,
    db: Session = Depends(get_db),
):
    google_user = verify_google_token(request.credential)

    if google_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google credential.",
        )

    principal = get_user_team(
        db,
        google_user["google_subject"],
    )

    if principal is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Google account is not registered for Flutter Wars.",
        )

    token = create_access_token(
        user_id=str(principal.user_id),
        email=google_user["email"],
        team_id=str(principal.team_id),
        role=principal.role,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me")
def get_me(
    principal: AuthenticatedPrincipal = Depends(get_principal),
):
    return {
        "user_id": principal.user_id,
        "email": principal.email,
        "team_id": principal.team_id,
        "role": principal.role,
        "auth_type": principal.auth_type,
    }