# StoryPulse AI — REST API Specification
**Document ID:** `13_API_SPECIFICATION`  
**Version:** `1.0.0`  
**Status:** Approved  
**Base URL:** `http://localhost:8000/api/v1`  
**Last Updated:** 2026-11-08  

---

## 1. System Health & Metadata

### `GET /health`
Returns system status, database health, and Gnani AI adapter state.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "gnani_stt_status": "ONLINE",
  "gnani_tts_status": "ONLINE",
  "active_sessions": 3
}
```

---

## 2. Stories Catalog

### `GET /api/v1/stories`
Fetches all available story domains and catalog metadata.

**Query Parameters:**
- `duration`: (Optional) Integer filter (2, 5, 10, 15).
- `mood`: (Optional) String filter ("Curious", "Bored", "Excited", "Relaxed").

**Response (200 OK):**
```json
[
  {
    "id": "mystery",
    "title": "The Archive of Unsent Goodbyes",
    "domain": "mystery",
    "tagline": "Some memories are sealed for a reason.",
    "duration_min": 10,
    "moods": ["Curious", "Reflective"],
    "cover_image": "/assets/images/covers/cover_mystery.png",
    "character_count": 3,
    "scene_count": 4,
    "clue_count": 5
  }
]
```

### `GET /api/v1/stories/{story_id}`
Returns details, characters, and beginning hooks for a specific story.

---

## 3. Story Sessions

### `POST /api/v1/sessions`
Spawns a new interactive story session.

**Request Body:**
```json
{
  "story_id": "mystery",
  "duration_target": 10,
  "mood_selected": "Curious",
  "preferred_lang": "en-IN"
}
```

**Response (201 Created):**
```json
{
  "session_id": "a9c2e0bb-713e-48a6-981f-762281df6f88",
  "story_id": "mystery",
  "current_scene": {
    "scene_id": "scene_cliffside",
    "title": "The Salt Cliff Road",
    "background_image": "/assets/images/scenes/scene_cliffside.png",
    "active_character": {
      "id": "dev",
      "name": "Dev (The Postman)",
      "avatar_url": "/assets/images/characters/char_dev.png"
    },
    "dialogue": "I swear on my badge, Ananya... I found this in my delivery bag, but look at the postmark. It's dated tomorrow at 6:00 AM.",
    "audio_url": "/api/v1/speech/audio-cache/dev_intro_hash.wav",
    "suggested_actions": [
      "Examine the tomorrow postmark",
      "Ask Dev who gave him the satchel",
      "Look toward the old lighthouse"
    ]
  },
  "discovered_clues": [
    {
      "id": "clue_tomorrow_letter",
      "title": "The Tomorrow Letter",
      "description": "Sealed with purple wax and stamped with tomorrow's date.",
      "thumbnail": "/assets/images/clues/clue_tomorrow_letter.png"
    }
  ],
  "is_completed": false,
  "status": "ACTIVE"
}
```

### `POST /api/v1/sessions/{session_id}/action`
Executes a narrative action (typed or transcribed text).

**Request Body:**
```json
{
  "action_text": "Examine the tomorrow postmark",
  "input_modality": "TEXT"
}
```

**Response (200 OK):**
```json
{
  "session_id": "a9c2e0bb-713e-48a6-981f-762281df6f88",
  "previous_scene_id": "scene_cliffside",
  "current_scene": {
    "scene_id": "scene_archive_vault",
    "title": "The Subterranean Vault",
    "background_image": "/assets/images/scenes/scene_archive_vault.png",
    "active_character": {
      "id": "mira",
      "name": "Mira (The Archivist)",
      "avatar_url": "/assets/images/characters/char_mira.png"
    },
    "dialogue": "The salt air will ruin that envelope if you keep standing in the spray. Step inside the vault where the ink can dry.",
    "audio_url": "/api/v1/speech/audio-cache/mira_scene2_hash.wav",
    "suggested_actions": [
      "Ask Mira about the whispers in the pigeonholes",
      "Use the brass key on Drawer 7"
    ]
  },
  "newly_unlocked_clue": {
    "id": "clue_brass_vault_key",
    "title": "The Sea-Salt Brass Key (#7)",
    "description": "Carved with the numeral 7, cold to the touch.",
    "thumbnail": "/assets/images/clues/clue_brass_vault_key.png"
  },
  "is_completed": false,
  "ending_id": null
}
```

---

## 4. Voice Processing Endpoints

### `POST /api/v1/speech/transcribe`
Transcribes raw uploaded audio via Gnani Prisma v2.5 / v3.0.

- **Content-Type:** `multipart/form-data`
- **Fields:**
  - `audio_file`: Binary file (`.wav` or `.m4a`).
  - `language_code`: `"indic-auto"` or `"en-IN"` (Default: `"en-IN"`).

**Response (200 OK):**
```json
{
  "transcribed_text": "Examine the postmark closely",
  "confidence": 0.96,
  "provider": "gnani_prisma_v3",
  "latency_ms": 780
}
```

### `POST /api/v1/speech/synthesize`
Synthesizes character speech via Gnani Timbre v2.5 / v3.0.

**Request Body:**
```json
{
  "text": "Step inside the vault where the ink can dry.",
  "voice_id": "Nalini",
  "language": "en-IN"
}
```

**Response (200 OK):** Returns binary audio/wav or JSON payload containing Base64 / CDN audio URL.

