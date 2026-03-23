"""FastAPI application entry point."""
from fastapi import FastAPI
from app.config import settings
from app.api.v1 import data

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Quantitative backtesting platform API"
)

# Register routers
app.include_router(data.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
