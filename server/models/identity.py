from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class UserIdentity(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    google_subject: str = Field(unique=True, index=True)
    email: str = Field(index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )