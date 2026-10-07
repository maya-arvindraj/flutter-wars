from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from pydantic import BaseModel
from sqlmodel import Session, select 

from auth.jwt import decode_access_token
from core.database import engine
from models import UserIdentity, TeamMembership, Team

bearer_scheme = HTTPBearer()


class AuthenticatedPrincipal(BaseModel):
    user_id: str
    email: str
    team_id: str
    auth_type: str
    role: str = "participant"


def get_db() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_principal(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> AuthenticatedPrincipal:

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")
        email = payload.get("email")
        team_id = payload.get("team_id")
        role = payload.get("role", "participant")

        if not user_id or not email or not team_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims.",
            )

        # Check that the user still belongs to this team
        user = db.get(UserIdentity, int(user_id))

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is no longer registered.",
            )

        membership = db.exec(
            select(TeamMembership).where(
                TeamMembership.user_identity_id == user.id,
                TeamMembership.team_id == int(team_id),
            )
        ).first()

        if membership is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of this team.",
            )

        # Check that the team is still active
        team = db.get(Team, int(team_id))

        if team is None or team.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Team is not active.",
            )

        return AuthenticatedPrincipal(
            user_id=str(user.id),
            email=user.email,
            team_id=str(team.id),
            role=membership.role,
            auth_type="JWT",
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )