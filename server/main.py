import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, text

from core.config import settings
from core.database import init_db
from core.dependencies import get_db
from core.schemas import ApiResponse, ErrorResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("foundation")
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from core.schemas import ErrorResponse

app = FastAPI(title=settings.APP_NAME)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the full exception internally here
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            message="An unexpected system error occurred."
        ).model_dump()
    )
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Foundation Module A...")
    try:
        init_db()
    except Exception as e:
        logger.error(f"Startup check warning: {e}")
    yield

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unhandled system error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            detail="An internal error occurred."
        ).model_dump()
    )

@app.get("/health", response_model=ApiResponse[dict], tags=["Diagnostics"])
def get_health():
    """Basic process health. Does not leak secrets."""
    return ApiResponse(data={"status": "healthy", "environment": settings.ENV})

@app.get("/ready", response_model=ApiResponse[dict], tags=["Diagnostics"])
def get_ready(db: Session = Depends(get_db)):
    """Readiness check verifying DB connectivity via SELECT 1."""
    try:
        db.exec(text("SELECT 1"))
        return ApiResponse(data={"status": "ready", "database": "connected"})
    except Exception as e:
        logger.error(f"Readiness failure: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=ErrorResponse(
                error_code="SERVICE_UNAVAILABLE",
                detail="Database connectivity unavailable."
            ).model_dump()
        )