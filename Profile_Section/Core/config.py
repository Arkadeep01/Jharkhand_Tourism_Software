from pydantic import BaseSettings


class Settings(BaseSettings):
    # -------------------------------
    # Database settings
    # -------------------------------
    DATABASE_URL: str = "sqlite:///./test.db"  # Replace with PostgreSQL/MySQL URL if needed

    # -------------------------------
    # Firebase settings
    # -------------------------------
    FIREBASE_CREDENTIALS_PATH: str = "./path/to/firebase-service-account.json"

    # -------------------------------
    # App settings
    # -------------------------------
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
