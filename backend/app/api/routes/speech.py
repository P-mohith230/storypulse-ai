import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from app.schemas.schemas import TranscribeResponse, SynthesizeRequest, SynthesizeResponse
from app.services.gnani.prisma_service import prisma_service
from app.services.gnani.timbre_service import timbre_service, CACHE_DIR

router = APIRouter()

@router.post("/transcribe", response_model=TranscribeResponse)
def transcribe_speech(
    audio_file: UploadFile = File(...),
    language_code: str = Form("en-IN")
):
    try:
        content = audio_file.file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Audio file is empty")

        result = prisma_service.transcribe_sync(
            audio_bytes=content,
            filename=audio_file.filename or "audio.wav",
            language_code=language_code
        )
        return TranscribeResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech transcription failed: {str(e)}")

@router.post("/synthesize", response_model=SynthesizeResponse)
def synthesize_speech(payload: SynthesizeRequest):
    try:
        result = timbre_service.synthesize_sync(
            text=payload.text,
            voice_id=payload.voice_id,
            language=payload.language
        )
        return SynthesizeResponse(
            audio_url=result.get("audio_url") or "",
            status=result.get("status", "READY"),
            provider=result.get("provider", "gnani_timbre")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(e)}")

@router.get("/audio-cache/{filename}")
def get_cached_audio(filename: str):
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(CACHE_DIR, safe_filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Audio file not found in cache")
    return FileResponse(filepath, media_type="audio/wav")
