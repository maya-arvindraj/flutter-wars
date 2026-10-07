from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class TeamMembership(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user_identity_id: int = Field(
        foreign_key="useridentity.id",
        unique=True
    )

    team_id: int = Field(
        foreign_key="team.id"
    )

    role: str = Field(default="participant")

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )