from sqlmodel import Session, select

from auth.principal import Principal
from models import Team, TeamMembership, UserIdentity


def get_user_team(session: Session, google_subject: str):
    user = session.exec(
        select(UserIdentity).where(
            UserIdentity.google_subject == google_subject
        )
    ).first()

    if user is None:
        return None

    membership = session.exec(
        select(TeamMembership).where(
            TeamMembership.user_identity_id == user.id
        )
    ).first()

    if membership is None:
        return None

    team = session.exec(
        select(Team).where(
            Team.id == membership.team_id
        )
    ).first()

    if team is None:
        return None

    if team.status != "active":
        return None

    return Principal(
        user_id=user.id,
        team_id=team.id,
        role=membership.role,
    )