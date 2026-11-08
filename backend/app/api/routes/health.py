from fastapi import APIRouter
from app.schemas.schemas import HealthResponse
from app.repositories.session_repo import session_repo
from app.services.gnani.gnani_client import gnani_client

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        database="connected",
        gnani_stt_status="ONLINE" if gnani_client.is_live_configured() else "MOCK_MODE",
        gnani_tts_status="ONLINE" if gnani_client.is_live_configured() else "MOCK_MODE",
        active_sessions=session_repo.count_active_sessions()
    )
