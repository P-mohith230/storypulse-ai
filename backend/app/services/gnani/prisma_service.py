from typing import Dict, Any
from app.services.gnani.gnani_client import gnani_client

class PrismaService:
    def transcribe_sync(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        language_code: str = "en-IN"
    ) -> Dict[str, Any]:
        return gnani_client.transcribe_audio_sync(
            audio_bytes=audio_bytes,
            filename=filename,
            language_code=language_code
        )

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        language_code: str = "en-IN"
    ) -> Dict[str, Any]:
        return self.transcribe_sync(audio_bytes, filename, language_code)

prisma_service = PrismaService()
