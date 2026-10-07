from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    status: str = Field(default="active")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )