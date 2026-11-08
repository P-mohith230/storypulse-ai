from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class UserPreference(BaseModel):
    preferred_lang: str = "en-IN"
    audio_mode: str = "auto_tts"
    haptic_enabled: bool = True
    subtitles_enabled: bool = True

_in_memory_prefs = UserPreference()

@router.get("")
def get_preferences():
    return _in_memory_prefs

@router.put("")
def update_preferences(prefs: UserPreference):
    global _in_memory_prefs
    _in_memory_prefs = prefs
    return _in_memory_prefs
