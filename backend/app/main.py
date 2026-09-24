from fastapi import FastAPI


from app.api.auth import router as auth_router
from app.api.documents import router as documents_router
from app.api.query import router as query_router
from app.core.config import settings
from app.api.feedback import router as feedback_router
from app.api.sources import router as sources_router

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.include_router(
    auth_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    documents_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    query_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    feedback_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    sources_router,
    prefix=settings.api_v1_prefix,
)

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
    }