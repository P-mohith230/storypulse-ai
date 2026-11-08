import os
import time
import requests
from typing import Optional, Dict, Any
from app.core.config import settings

class GnaniClient:
    def __init__(self):
        self.api_key = settings.GNANI_API_KEY
        self.base_url = settings.GNANI_BASE_URL.rstrip("/")
        self.prisma_endpoint = settings.GNANI_PRISMA_ENDPOINT
        self.timbre_endpoint = settings.GNANI_TIMBRE_ENDPOINT
        self.mock_fallback = settings.GNANI_MOCK_FALLBACK or (not bool(self.api_key))

    def is_live_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def transcribe_audio_sync(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        language_code: str = "en-IN",
        model: str = "prisma-v3.0"
    ) -> Dict[str, Any]:
        """
        Synchronous call to official Gnani Prisma v3 STT endpoint: POST https://api.vachana.ai/stt/v3
        """
        start_time = time.time()

        if self.is_live_configured():
            try:
                url = f"{self.base_url}{self.prisma_endpoint}"
                headers = {
                    "X-API-Key-ID": self.api_key
                }
                files = {
                    "audio_file": (filename, audio_bytes, "audio/wav")
                }
                data = {
                    "model": model,
                    "language_code": language_code
                }

                resp = requests.post(url, headers=headers, files=files, data=data, timeout=10.0)
                latency = int((time.time() - start_time) * 1000)

                if resp.status_code == 200:
                    payload = resp.json()
                    transcript = payload.get("transcript", "") or payload.get("text", "")
                    return {
                        "transcribed_text": transcript,
                        "confidence": payload.get("confidence", 0.95),
                        "provider": "gnani_prisma_v3_live",
                        "latency_ms": latency
                    }
                else:
                    print(f"[Gnani STT Live Error] {resp.status_code}: {resp.text}")
            except Exception as e:
                print(f"[Gnani STT Exception] {e}")

        # Transparent mock fallback
        latency = int((time.time() - start_time) * 1000)
        return {
            "transcribed_text": "Examine the tomorrow postmark closely",
            "confidence": 0.98,
            "provider": "gnani_prisma_v3_mock_fallback",
            "latency_ms": max(latency, 240)
        }

    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        language_code: str = "en-IN",
        model: str = "prisma-v3.0"
    ) -> Dict[str, Any]:
        return self.transcribe_audio_sync(audio_bytes, filename, language_code, model)

    def synthesize_speech_sync(
        self,
        text: str,
        voice: str = "Nalini",
        language: str = "en-IN",
        model: str = "timbre-v2.5"
    ) -> Dict[str, Any]:
        """
        Synchronous call to official Gnani Timbre v2.5/v3 TTS endpoint: POST https://api.vachana.ai/api/v1/tts/inference
        """
        start_time = time.time()

        if self.is_live_configured():
            try:
                url = f"{self.base_url}{self.timbre_endpoint}"
                headers = {
                    "X-API-Key-ID": self.api_key,
                    "Content-Type": "application/json"
                }
                payload = {
                    "text": text,
                    "voice": voice,
                    "model": model,
                    "language": language,
                    "speed": 1.0,
                    "audio_config": {
                        "encoding": "linear_pcm",
                        "container": "wav",
                        "num_channels": 1,
                        "sample_rate": 24000,
                        "sample_width": 2
                    }
                }

                resp = requests.post(url, headers=headers, json=payload, timeout=10.0)
                latency = int((time.time() - start_time) * 1000)

                if resp.status_code == 200:
                    return {
                        "audio_bytes": resp.content,
                        "status": "READY",
                        "provider": "gnani_timbre_v2.5_live",
                        "latency_ms": latency
                    }
                else:
                    print(f"[Gnani TTS Live Error] {resp.status_code}: {resp.text}")
            except Exception as e:
                print(f"[Gnani TTS Exception] {e}")

        # Fallback response
        latency = int((time.time() - start_time) * 1000)
        return {
            "audio_bytes": None,
            "audio_url": None,
            "status": "TEXT_FALLBACK",
            "provider": "gnani_timbre_mock_fallback",
            "latency_ms": max(latency, 120)
        }

    async def synthesize_speech(
        self,
        text: str,
        voice: str = "Nalini",
        language: str = "en-IN",
        model: str = "timbre-v2.5"
    ) -> Dict[str, Any]:
        return self.synthesize_speech_sync(text, voice, language, model)

gnani_client = GnaniClient()
