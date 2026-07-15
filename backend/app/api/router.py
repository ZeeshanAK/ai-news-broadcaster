from fastapi import APIRouter

from app.api.routes import articles, sources, summaries, broadcasts, settings

api_router = APIRouter()

api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(summaries.router, prefix="/summaries", tags=["summaries"])
api_router.include_router(broadcasts.router, prefix="/broadcasts", tags=["broadcasts"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])