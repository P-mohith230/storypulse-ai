# StoryPulse AI — Backend Database Schema & Data Models
**Document ID:** `05_BACKEND_SCHEMA`  
**Version:** `1.0.0`  
**Status:** Approved  
**Last Updated:** 2026-11-08  

---

## 1. Database Architecture & ER Diagram

StoryPulse utilizes **SQLAlchemy 2.0 ORM** targeting **SQLite** for development and local testing, while maintaining 100% dialect compatibility for **PostgreSQL** in production deployment.

```
+-------------------------------------------------------------+
|                          USERS                              |
+-------------------------------------------------------------+
| PK  user_id            VARCHAR(64)                          |
|     device_id          VARCHAR(128)   UNIQUE INDEX          |
|     preferred_lang     VARCHAR(10)    DEFAULT 'en-IN'       |
|     created_at         DATETIME                             |
|     last_active_at     DATETIME                             |
+-------------------------------------------------------------+
                              | 1
                              |
                              | N
+-------------------------------------------------------------+
|                      STORY_SESSIONS                         |
+-------------------------------------------------------------+
| PK  session_id         VARCHAR(64)                          |
| FK  user_id            VARCHAR(64)    INDEX                 |
|     story_id           VARCHAR(32)    INDEX                 |
|     current_scene_id   VARCHAR(32)                          |
|     status             VARCHAR(20)    -- ACTIVE, COMPLETED  |
|     duration_target    INTEGER        -- 2, 5, 10, 15 (min) |
|     mood_selected      VARCHAR(20)                          |
|     ending_id          VARCHAR(32)    NULLABLE              |
|     started_at         DATETIME                             |
|     updated_at         DATETIME                             |
|     completed_at       DATETIME       NULLABLE              |
+-------------------------------------------------------------+
          | 1                           | 1
          |                             |
          | N                           | N
+-----------------------------+ +-----------------------------+
|       SESSION_ACTIONS       | |       SESSION_CLUES         |
+-----------------------------+ +-----------------------------+
| PK  action_id   VARCHAR(64) | | PK  id          INTEGER     |
| FK  session_id  VARCHAR(64) | | FK  session_id  VARCHAR(64) |
|     scene_id    VARCHAR(32) | |     clue_id     VARCHAR(32) |
|     actor_type  VARCHAR(10) | |     discovered_at DATETIME  |
|     action_text TEXT        | +-----------------------------+
|     audio_url   VARCHAR(256)|
|     created_at  DATETIME    |
+-----------------------------+
```

---

## 2. Table Specifications & Fields

### 2.1 `users`
Represents an anonymous or authenticated player profile.
- `user_id`: `String(64)`, Primary Key (UUIDv4).
- `device_id`: `String(128)`, Unique, Indexed. Anonymous fingerprint for automatic profile recovery.
- `preferred_lang`: `String(10)`, Default `"en-IN"`. (Supported: `"en-IN"`, `"te-IN"`, `"hi-IN"`).
- `audio_mode`: `String(20)`, Default `"auto_tts"`. Options: `"auto_tts"`, `"text_only"`.
- `created_at`: `DateTime`, Default `utcnow`.
- `last_active_at`: `DateTime`, Default `utcnow`.

### 2.2 `story_sessions`
Tracks active and historical narrative game states.
- `session_id`: `String(64)`, Primary Key (UUIDv4).
- `user_id`: `String(64)`, Foreign Key (`users.user_id`), Indexed.
- `story_id`: `String(32)`, e.g. `"mystery"`, `"thriller"`, `"adventure"`, `"comedy"`, `"sci_fi"`.
- `current_scene_id`: `String(32)`, active scene identifier (e.g., `"scene_archive_vault"`).
- `status`: `String(20)`, Enum: `ACTIVE`, `PAUSED`, `COMPLETED`, `ABANDONED`.
- `duration_target`: `Integer`, minutes (2, 5, 10, 15).
- `mood_selected`: `String(20)`, e.g., `"Curious"`, `"Excited"`, `"Bored"`.
- `ending_id`: `String(32)`, Nullable, resolved ending identifier.
- `discovered_clues_json`: `Text` (JSON array of unlocked clue IDs).
- `character_memory_json`: `Text` (JSON dictionary of character trust/relationship scores).
- `started_at`: `DateTime`, Default `utcnow`.
- `updated_at`: `DateTime`, Default `utcnow`.
- `completed_at`: `DateTime`, Nullable.

### 2.3 `session_actions`
Full narrative transcript and dialogue turns.
- `action_id`: `String(64)`, Primary Key (UUIDv4).
- `session_id`: `String(64)`, Foreign Key (`story_sessions.session_id`), Indexed.
- `scene_id`: `String(32)`, scene in which the action took place.
- `actor_type`: `String(10)`, Enum: `USER`, `CHARACTER`, `NARRATOR`.
- `character_id`: `String(32)`, Nullable (e.g., `"mira"`, `"dev"`).
- `action_text`: `Text`, the dialogue spoken or player choice executed.
- `input_modality`: `String(10)`, Enum: `VOICE`, `TEXT`, `TOUCH_TAP`.
- `audio_url`: `String(256)`, Nullable (link to synthesized speech audio).
- `created_at`: `DateTime`, Default `utcnow`.

### 2.4 `session_clues`
Normalised relational mapping for quick clue progress queries.
- `id`: `Integer`, Primary Key, Auto-increment.
- `session_id`: `String(64)`, Foreign Key (`story_sessions.session_id`), Indexed.
- `clue_id`: `String(32)`, identifier matching story configuration.
- `discovered_at`: `DateTime`, Default `utcnow`.

---

## 3. In-Memory / JSON Story Package Schema

Story definition files are stored under `backend/app/story_data/{domain}/` and loaded at startup into memory structures:

```typescript
interface StoryDefinition {
  id: string; // e.g. "mystery"
  title: string; // "The Archive of Unsent Goodbyes"
  domain: "mystery" | "thriller" | "adventure" | "comedy" | "sci_fi";
  estimated_duration_min: number;
  moods: string[];
  initial_scene_id: string;
  cover_image: string;
  characters: Record<string, CharacterDefinition>;
  scenes: Record<string, SceneDefinition>;
  clues: Record<string, ClueDefinition>;
  endings: Record<string, EndingDefinition>;
}

interface SceneDefinition {
  id: string;
  title: string;
  description: string;
  background_image: string;
  active_character_id: string;
  opening_dialogue: string;
  suggested_actions: string[];
  valid_transitions: Record<string, {
    target_scene_id: string;
    required_clues?: string[];
    action_keywords: string[];
    unlocks_clue?: string;
  }>;
  ending_trigger?: string;
}
```

---

## 4. Data Retention & Hygiene
- **Audio Files:** Temporary user voice recordings are retained in `/tmp/` only for the duration of the transcription request (`max 60 seconds`) and deleted.
- **Synthesized Voice:** Audio cache for character voice lines is cached by content hash (`md5(text + voice_id)`) to minimize latency and redundant Gnani API calls.
- **Sessions:** Inactive sessions remain in SQLite database indefinitely during MVP testing.
