from typing import Optional
from pydantic import BaseModel

class UserPrincipal(BaseModel):
    user_id: str
    email: str
    role: str = "user"
    team_id: Optional[str] = None

def get_principal() -> Optional[UserPrincipal]:
    """
    Stub for downstream Auth modules to inject authenticated principal context.
    """
    return None