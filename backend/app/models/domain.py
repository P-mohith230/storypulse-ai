from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any

@dataclass
class User:
    user_id: str
    device_id: str
    preferred_lang: str = "en-IN"
    audio_mode: str = "auto_tts"
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_active_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class StorySession:
    session_id: str
    story_id: str
    current_scene_id: str
    user_id: Optional[str] = None
    status: str = "ACTIVE"
    duration_target: int = 5
    mood_selected: str = "Curious"
    ending_id: Optional[str] = None
    discovered_clues: List[str] = field(default_factory=list)
    character_memory: Dict[str, Any] = field(default_factory=dict)
    started_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

@dataclass
class SessionAction:
    action_id: str
    session_id: str
    scene_id: str
    actor_type: str  # 'USER', 'CHARACTER', 'NARRATOR'
    action_text: str
    character_id: Optional[str] = None
    input_modality: str = "TEXT"  # 'VOICE', 'TEXT', 'TOUCH_TAP'
    audio_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

