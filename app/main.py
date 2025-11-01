from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api import a_auth, a_chat, a_admin, a_user
from app.config import settings
from app.db import SessionLocal, get_session
from app.services.messaging import rabbitmq


async def lifespan(app: FastAPI):
    """Lifespan context — handles startup and shutdown events."""

    # startup
    async with SessionLocal() as session:
        await session.execute(text("SELECT 1"))
        print("✅ Database connection established successfully.")
    await rabbitmq.connect()
    print("✅ Connected to RabbitMQ.")

    yield
    # shutdown
    await rabbitmq.disconnect()
    print("🛑 Disconnected from RabbitMQ.")
    print("🛑 Application shutting down...")


app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)

print(f"==============================={settings.EMAIL_SENDER}")


@app.get("/")
def read_root():
    """Simple health check endpoint."""
    return {"message": "Chat API is running!"}


app.include_router(a_auth.router)
app.include_router(a_chat.router)
app.include_router(a_admin.router)
app.include_router(a_user.router)
