from sqlmodel import Session, select

from app.database import engine
from app.models import UserIdentity, Team, TeamMembership


with Session(engine) as session:
    users = session.exec(select(UserIdentity)).all()
    teams = session.exec(select(Team)).all()
    memberships = session.exec(select(TeamMembership)).all()

    print("\nUSERS:")
    for user in users:
        print(user)

    print("\nTEAMS:")
    for team in teams:
        print(team)

    print("\nMEMBERSHIPS:")
    for membership in memberships:
        print(membership)