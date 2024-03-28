from fastapi import FastAPI
from .endpoints.user import router as user_router


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(user_router, prefix="/users", tags=["users"])
    return app
