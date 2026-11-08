import os
import uuid
from typing import Optional

SCRATCH_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "scratch_audio"))
os.makedirs(SCRATCH_DIR, exist_ok=True)

class AudioService:
    @staticmethod
    def save_temp_audio(data: bytes, ext: str = "wav") -> str:
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(SCRATCH_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(data)
        return filepath

    @staticmethod
    def cleanup_file(filepath: Optional[str]):
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass

audio_service = AudioService()
