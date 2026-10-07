from sqlmodel import Session, select

from app.database import engine
from app.models import UserIdentity, Team, TeamMembership


with Session(engine) as session:
    user = UserIdentity(
        google_subject="google-test-123",
        email="test@vit.ac.in",
    )

    team = Team(
        name="Team Phoenix",
        status="active",
    )

    session.add(user)
    session.add(team)
    session.commit()

    session.refresh(user)
    session.refresh(team)

    membership = TeamMembership(
        user_identity_id=user.id,
        team_id=team.id,
        role="participant",
    )

    session.add(membership)
    session.commit()
    session.refresh(membership)

    print("USER:", user)
    print("TEAM:", team)
    print("MEMBERSHIP:", membership)