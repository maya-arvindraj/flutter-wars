from sqlmodel import SQLModel, create_engine
from core.config import settings
from models import UserIdentity, Team, TeamMembership

is_sqlite = settings.DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=connect_args,
    pool_recycle=300,
    pool_pre_ping=True,
)

def init_db():
    SQLModel.metadata.create_all(engine)