from fastapi import APIRouter
from app.api.routes import stories, sessions, speech, preferences

api_router = APIRouter()

api_router.include_router(stories.router, prefix="/stories", tags=["Stories"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
api_router.include_router(speech.router, prefix="/speech", tags=["Voice AI (Gnani)"])
api_router.include_router(preferences.router, prefix="/preferences", tags=["Preferences"])

