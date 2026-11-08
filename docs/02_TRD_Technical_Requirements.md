# StoryPulse AI — Technical Requirements Document (TRD)
**Document ID:** `02_TRD`  
**Version:** `1.0.0`  
**Status:** Approved  
**Last Updated:** 2026-11-08  

---

## 1. System Technology Stack

```
+-----------------------------------------------------------------------------------+
|                                STORYPULSE CLIENT                                  |
|   React Native (Expo SDK 52) | TypeScript | Expo Router / React Navigation        |
|   React Native Reanimated | Expo AV / Audio | Lucide React Native | Tailwind / CSS |
+-----------------------------------------------------------------------------------+
                                        | (HTTPS / REST)
                                        v
+-----------------------------------------------------------------------------------+
|                               FASTAPI BACKEND SERVICE                             |
|   Python 3.12+ | FastAPI | Pydantic v2 | SQLAlchemy 2.x | SQLite (Dev) -> PG (Prod) |
+-----------------------------------------------------------------------------------+
        |                               |                               |
        v                               v                               v
+-----------------------+   +-----------------------+   +-----------------------+
|  DETERMINISTIC ENGINE |   |    GNANI AI CLOUD     |   |   AI DIALOGUE ADAPTER  |
|  - JSON Story Packages|   |  - Prisma v2.5 / v3   |   |  - OpenAI / Anthropic /|
|  - State Transitions  |   |    STT (api.vachana)  |   |    Gemini API / Local  |
|  - Clue Lock Engine   |   |  - Timbre v2.5 / v3   |   |  - Deterministic      |
|  - Session Repository |   |    TTS (api.vachana)  |   |    Script Fallback    |
+-----------------------+   +-----------------------+   +-----------------------+
```

| Layer | Component | Chosen Technology | Rationale |
| :--- | :--- | :--- | :--- |
| **Mobile Client** | Framework | React Native (Expo SDK 52) with TypeScript | Fast cross-platform Android & iOS execution, native audio drivers (`expo-av`), rapid hot-reloading. |
| **Mobile Client** | Styling | Native styling + StyleSheet / Utility classes | High-performance 60fps renders without compilation overhead. |
| **Mobile Client** | Audio I/O | `expo-av` | Robust recording, waveform meters, and cross-platform playback. |
| **Backend** | API Framework | FastAPI (Python 3.12+) | High async throughput, native Pydantic validation, OpenAPI docs generation. |
| **Backend** | Database & ORM | SQLite with SQLAlchemy 2.0 (PostgreSQL ready) | Zero-maintenance file database for MVP, fully decoupled relational schema. |
| **Voice AI** | Speech-to-Text | Gnani Prisma v2.5 / v3 (`api.vachana.ai/stt/v3`) | Industry-leading Indic speech recognition (English, Telugu, Hindi code-mix). |
| **Voice AI** | Text-to-Speech | Gnani Timbre v2.5 / v3 (`api.vachana.ai/api/v1/tts/inference`)| Expressive multilingual synthesis with character voice mapping. |
| **Narrative Engine**| State Validator | Custom Python Deterministic State Machine | Strict verification of player choices, preventing hallucinated lore. |
| **Dialogue Gen** | LLM Adapter | Pluggable LLM Adapter + Curated Fallback Script | Ensures system functions 100% reliably even when external LLM keys are absent. |

---

## 2. Architecture & Component Boundaries

### 2.1 Separation of Narrative Logic and Dialogue Generation
A paramount architectural law of StoryPulse is the **Dual-Engine Pattern**:
1. **The Deterministic Narrative Engine:**
   - Holds the ground truth of the universe.
   - Evaluates: Is Scene X accessible from Scene Y? Has the user unlocked Clue C? Is Ending E triggered?
   - Validates user input before mutating any database state.
2. **The Generative Dialogue Engine:**
   - Roleplays the active character within bounded conversational parameters.
   - Injected with: Character Persona, Character Knowledge Boundaries, Discovered Clues, and Permitted Plot Revelations.
   - **Never** mutates game state directly.

### 2.2 Gnani AI Integration Flow
- **Speech-to-Text (STT) via Prisma:**
  - Client records audio chunk (`audio/wav`, 16kHz or 24kHz mono).
  - Client sends multipart request `POST /api/v1/speech/transcribe` with audio blob.
  - Backend forward-relays to `https://api.vachana.ai/stt/v3` with `X-API-Key-ID: {GNANI_API_KEY}`.
  - Transcribed text returned to client or piped directly into narrative action handler.
- **Text-to-Speech (TTS) via Timbre:**
  - When character speaks, backend calls `POST https://api.vachana.ai/api/v1/tts/inference` specifying `voice` (e.g. "Nalini", "Kalyan"), `language` ("en-IN" / "te-IN"), and `model` ("timbre-v2.5").
  - Resulting audio stream/URL returned to mobile client for playback.

---

## 3. Directory & Repository Structure

```
StoryPluse-ai/
├── context.md                          # Single source of truth for AI agents
├── docs/                               # Complete project documentation suite
│   ├── 00_DOCUMENTATION_INVENTORY.md
│   ├── 01_PRD_Product_Requirements.md
│   ├── 02_TRD_Technical_Requirements.md
│   ├── 03_APP_FLOW.md
│   ├── 04_UI_UX_Design_Brief.md
│   ├── 05_BACKEND_SCHEMA.md
│   ├── 06_IMPLEMENTATION_PLAN.md
│   ├── 07_MASTER_CONTEXT.md
│   ├── 08_SYSTEM_ARCHITECTURE.md
│   ├── 09_STORY_ENGINE_DESIGN.md
│   ├── 10_GNANI_AI_INTEGRATION.md
│   ├── 11_IMAGE_ASSET_PLAN.md
│   ├── 12_ORIGINAL_STORY_BIBLE.md
│   ├── 13_API_SPECIFICATION.md
│   ├── 14_TESTING_STRATEGY.md
│   ├── 15_DEPLOYMENT_GUIDE.md
│   └── 16_DOCUMENTATION_VALIDATION_REPORT.md
├── backend/                            # FastAPI Python Backend
│   ├── app/
│   │   ├── api/
│   │   │   ├── api_v1.py
│   │   │   └── routes/
│   │   │       ├── health.py
│   │   │       ├── stories.py
│   │   │       ├── sessions.py
│   │   │       ├── speech.py
│   │   │       └── preferences.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   └── domain.py
│   │   ├── schemas/
│   │   │   └── schemas.py
│   │   ├── repositories/
│   │   │   └── session_repo.py
│   │   ├── services/
│   │   │   ├── narrative/
│   │   │   │   ├── engine.py
│   │   │   │   └── loader.py
│   │   │   ├── dialogue/
│   │   │   │   ├── adapter.py
│   │   │   │   └── prompt_builder.py
│   │   │   └── gnani/
│   │   │       ├── gnani_client.py
│   │   │       ├── prisma_service.py
│   │   │       ├── timbre_service.py
│   │   │       └── audio_service.py
│   │   ├── story_data/
│   │   │   ├── mystery/
│   │   │   │   ├── story.json
│   │   │   │   ├── scenes.json
│   │   │   │   ├── characters.json
│   │   │   │   ├── clues.json
│   │   │   │   └── endings.json
│   │   │   ├── thriller/
│   │   │   ├── adventure/
│   │   │   ├── comedy/
│   │   │   └── sci_fi/
│   │   └── main.py
│   ├── tests/
│   │   ├── test_engine.py
│   │   ├── test_api.py
│   │   └── test_gnani_mock.py
│   ├── requirements.txt
│   └── .env.example
├── mobile/                             # React Native Expo Mobile App
│   ├── app/                            # Expo Router or Navigation Screens
│   │   ├── (tabs)/
│   │   │   ├── index.tsx               # Home & Discover
│   │   │   ├── history.tsx             # History & Dossier
│   │   │   └── settings.tsx            # Settings & Preferences
│   │   ├── story/
│   │   │   ├── [storyId].tsx           # Story Preview
│   │   │   └── play.tsx                # Cinematic Story Gameplay
│   │   └── _layout.tsx
│   ├── assets/
│   │   ├── images/
│   │   │   ├── covers/
│   │   │   ├── characters/
│   │   │   ├── scenes/
│   │   │   └── clues/
│   │   └── audio/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── store/
│   │   └── types/
│   ├── package.json
│   ├── tsconfig.json
│   └── app.json
└── README.md
```

---

## 4. Environment Variables Specification

### 4.1 Backend (`backend/.env`)
```env
# Server
PORT=8000
HOST=0.0.0.0
DEBUG=True
ENVIRONMENT=development
CORS_ORIGINS=["*"]

# Database
DATABASE_URL=sqlite:///./storypulse.db

# Gnani AI API Credentials
GNANI_API_KEY=your_gnani_api_key_here
GNANI_BASE_URL=https://api.vachana.ai
GNANI_PRISMA_ENDPOINT=/stt/v3
GNANI_TIMBRE_ENDPOINT=/api/v1/tts/inference
GNANI_MOCK_FALLBACK=True

# LLM Dialogue Settings
LLM_PROVIDER=mock_fallback # options: gemini, openai, anthropic, mock_fallback
OPENAI_API_KEY=
GEMINI_API_KEY=
```

### 4.2 Mobile (`mobile/.env` or Constants)
```env
EXPO_PUBLIC_API_URL=http://10.0.2.2:8000 # for Android Emulator (or local network IP for physical device)
EXPO_PUBLIC_ENABLE_VOICE=true
EXPO_PUBLIC_DEFAULT_LANG=en-IN
```

---

## 5. Security, Secrets & Privacy
1. **Secrets Isolation:** Under no circumstances are `GNANI_API_KEY` or LLM API keys included in client-side code, git commits, or bundled mobile assets.
2. **Audio File Hygiene:** User microphone recordings uploaded to the backend are saved to an isolated, ephemeral scratch folder (`/tmp/audio_scratch/`), hashed, and unlinked immediately after STT processing.
3. **Session Tokens:** Client sessions are authenticated via crypto-random UUIDv4 session tokens stored in client secure storage and verified on each narrative action.
