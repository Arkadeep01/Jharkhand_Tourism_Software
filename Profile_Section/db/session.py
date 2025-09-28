from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Example: read DATABASE_URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./profile_section.db")

# SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Session Local class for creating DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
