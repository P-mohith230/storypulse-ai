from typing import Dict, Any

class DialogueSentimentTagger:
    """
    Contextual dialogue emotion tagger.
    Maps emotional cues and keywords to expressive speech parameters for Gnani Timbre TTS.
    """
    
    EMOTION_MAP = {
        "urgent": {"speed": 1.15, "pitch": "high", "aura_color": "#EF4444"},
        "mysterious": {"speed": 0.92, "pitch": "low", "aura_color": "#8B5CF6"},
        "playful": {"speed": 1.05, "pitch": "medium", "aura_color": "#FACC15"},
        "solemn": {"speed": 0.88, "pitch": "low", "aura_color": "#64748B"},
        "curious": {"speed": 1.0, "pitch": "medium", "aura_color": "#06B6D4"}
    }

    @classmethod
    def tag_dialogue(cls, text: str, domain: str = "mystery") -> Dict[str, Any]:
        lower = text.lower()
        if any(w in lower for w in ["hurry", "quick", "warning", "emergency", "run", "stop", "train", "platform"]):
            emotion = "urgent"
        elif any(w in lower for w in ["secret", "whisper", "memory", "tide", "fog", "envelope", "postmark"]):
            emotion = "mysterious"
        elif any(w in lower for w in ["excuse", "dog", "boss", "traffic", "certificate", "audit", "bureau"]):
            emotion = "playful"
        elif any(w in lower for w in ["tomb", "ancient", "sorrow", "erased", "farewell", "silent"]):
            emotion = "solemn"
        else:
            emotion = "curious"

        config = cls.EMOTION_MAP[emotion].copy()
        config["emotion"] = emotion
        return config

sentiment_tagger = DialogueSentimentTagger()
