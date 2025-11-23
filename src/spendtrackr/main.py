# src/spendtrackr/main.py

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from spendtrackr.core.config import get_settings
from spendtrackr.db.base import Base
from spendtrackr.db.session import engine
from spendtrackr.apps.auth.routes import router as auth_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    Base.metadata.create_all(bind=engine)
    # You could also test DB/Redis connections here later
    yield
    # Shutdown logic (if needed)
    # e.g. close engine, cleanup resources, etc.


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)


@app.get("/health", tags=["health"])
def health_check():
    return JSONResponse({"status": "ok", "app": settings.app_name})


# API routers
app.include_router(auth_router, prefix="/api/v1")
