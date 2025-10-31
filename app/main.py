from fastapi import FastAPI
from contextlib import asynccontextmanager

# from app.database import init_db
from app.config import settings

# from app.api import a_auth, a_chat, a_admin


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Lifespan context — handles startup and shutdown events."""
#     await init_db()
#     yield
#     # await some_cleanup_function()


# app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)
print(f"==============================={settings.EMAIL_SENDER}")


@app.get("/")
def read_root():
    """Simple health check endpoint."""
    return {"message": "Chat API is running!"}


# app.include_router(a_admin.router)
# app.include_router(a_chat.router)
# app.include_router(a_admin.router)
