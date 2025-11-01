from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "ChatApp"
    DEBUG: bool = True

    BACKEND_URL: str
    ALEMBIC_DATABASE_URL: str

    DATABASE_URL: str

    RABBITMQ_URL: str

    SMTP_SERVER: str
    SMTP_PORT: int
    EMAIL_SENDER: str
    SMTP_PASSWORD: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
