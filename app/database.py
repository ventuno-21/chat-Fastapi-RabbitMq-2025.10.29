from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

# Create SQLAlchemy engine using environment variable
engine = create_engine(settings.DATABASE_URL, echo=True)


def init_db():
    """Create tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency injection for FastAPI routes."""
    with Session(engine) as session:
        yield session
