import hashlib
import os
from typing import Dict, Any, Optional
from app.services.gnani.gnani_client import gnani_client

CACHE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "audio_cache"))
os.makedirs(CACHE_DIR, exist_ok=True)

class TimbreService:
    def synthesize_sync(
        self,
        text: str,
        voice_id: str = "Nalini",
        language: str = "en-IN"
    ) -> Dict[str, Any]:
        text_hash = hashlib.md5(f"{text}:{voice_id}:{language}".encode("utf-8")).hexdigest()
        cached_file = os.path.join(CACHE_DIR, f"{text_hash}.wav")

        if os.path.exists(cached_file):
            return {
                "audio_url": f"/api/v1/speech/audio-cache/{text_hash}.wav",
                "status": "CACHED",
                "provider": "local_audio_cache"
            }

        result = gnani_client.synthesize_speech_sync(
            text=text,
            voice=voice_id,
            language=language
        )

        audio_bytes = result.get("audio_bytes")
        if audio_bytes:
            with open(cached_file, "wb") as f:
                f.write(audio_bytes)
            return {
                "audio_url": f"/api/v1/speech/audio-cache/{text_hash}.wav",
                "status": "READY",
                "provider": result.get("provider", "gnani_timbre")
            }

        return {
            "audio_url": None,
            "status": result.get("status", "TEXT_FALLBACK"),
            "provider": result.get("provider", "gnani_timbre_mock")
        }

    async def synthesize(
        self,
        text: str,
        voice_id: str = "Nalini",
        language: str = "en-IN"
    ) -> Dict[str, Any]:
        return self.synthesize_sync(text, voice_id, language)

timbre_service = TimbreService()
