from sqlmodel import Session

from app.auth.service import get_user_team
from app.database import engine


with Session(engine) as session:
    principal = get_user_team(
        session,
        "google-test-123",
    )

    print("PRINCIPAL:")
    print(principal)