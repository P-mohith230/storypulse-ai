from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any

VALID_MOODS = {"Curious", "Excited", "Relaxed", "Bored", "Playful"}

# Health Schemas
class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    gnani_stt_status: str
    gnani_tts_status: str
    active_sessions: int

# Story Schemas
class CharacterSummary(BaseModel):
    id: str
    name: str
    role: str
    avatar_url: str

class ClueSummary(BaseModel):
    id: str
    title: str
    description: str
    thumbnail: str
    discovered: bool = False

class StoryCatalogItem(BaseModel):
    id: str
    title: str
    domain: str
    tagline: str
    duration_min: int
    moods: List[str]
    cover_image: str
    character_count: int
    scene_count: int
    clue_count: int
    featured: bool = False

class ActiveCharacterInfo(BaseModel):
    id: str
    name: str
    avatar_url: str

class SceneResponse(BaseModel):
    scene_id: str
    title: str
    background_image: str
    active_character: ActiveCharacterInfo
    dialogue: str
    audio_url: Optional[str] = None
    suggested_actions: List[str]
    audio_status: Optional[str] = "READY"

class CreateSessionRequest(BaseModel):
    story_id: str
    user_id: Optional[str] = None
    duration_target: int = Field(default=5, ge=2, le=30)
    mood_selected: str = Field(default="Curious")
    preferred_lang: str = Field(default="en-IN")

    @field_validator("mood_selected")
    @classmethod
    def validate_mood(cls, v: str) -> str:
        cleaned = v.strip().title()
        if cleaned not in VALID_MOODS:
            return "Curious"
        return cleaned

class SessionHistoryItem(BaseModel):
    session_id: str
    story_id: str
    status: str
    current_scene_id: str
    duration_target: int
    mood_selected: str
    discovered_clues_count: int
    started_at: str
    is_completed: bool

class SessionActionRequest(BaseModel):
    action_text: str
    input_modality: str = Field(default="TEXT")  # 'TEXT', 'VOICE', 'TOUCH_TAP'

class SessionStateResponse(BaseModel):
    session_id: str
    story_id: str
    previous_scene_id: Optional[str] = None
    current_scene: SceneResponse
    discovered_clues: List[ClueSummary]
    newly_unlocked_clue: Optional[ClueSummary] = None
    is_completed: bool = False
    ending_id: Optional[str] = None
    ending_title: Optional[str] = None
    ending_epilogue: Optional[str] = None
    ending_image: Optional[str] = None
    status: str = "ACTIVE"

class TranscribeResponse(BaseModel):
    transcribed_text: str
    confidence: float
    provider: str
    latency_ms: int

class SynthesizeRequest(BaseModel):
    text: str
    voice_id: str = "Nalini"
    language: str = "en-IN"

class SynthesizeResponse(BaseModel):
    audio_url: str
    status: str
    provider: str

