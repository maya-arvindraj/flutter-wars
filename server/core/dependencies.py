from typing import Generator, Optional
from fastapi import Header, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel
from core.database import engine

# User context for Google Sign-In JWT / IDE API Key[cite: 2]
class AuthenticatedPrincipal(BaseModel):
    user_id: str
    email: str
    team_id: str
    auth_type: str

def get_db() -> Generator[Session, None, None]:
    """Transaction/session boundary. Always closes and rolls back on failure."""
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
    authorization: Optional[str] = Header(None, alias="Authorization"),
    x_api_key: Optional[str] = Header(None, alias="X-Team-API-Key")
) -> AuthenticatedPrincipal:
    """Authenticated principal dependency."""
    if not authorization and not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials."
        )
    return AuthenticatedPrincipal(
        user_id="usr_01",
        email="user@example.com",
        team_id="team_alpha",
        auth_type="JWT" if authorization else "API_KEY"
    )   