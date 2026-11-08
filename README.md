# StoryPulse AI 🎙️📖✨
> **Your moments. Your mood. Your story.**  
> *AI-Powered Interactive Storytelling and Conversational Entertainment Platform for Micro-Breaks.*

---

## 🌟 Executive Summary

**StoryPulse AI** transforms small gaps in everyday life (commutes, waiting lounges, coffee pauses, micro-breaks) into immersive, cinematic storytelling experiences. Instead of aimless algorithmic feed scrolling, users step into 2–15 minute interactive audio-visual narratives where they become the central character.

### Core Value Pillars
1. **Mobile-First Cinematic Interface:** Designed for one-thumb ergonomics on Android with rich scene artwork, character portraits, clue dossiers, and responsive ambient lighting.
2. **Dual-Engine Narrative Integrity:** A deterministic state engine guarantees ground truth, canonical clues, and multiple endings, while dynamic dialogue stylist agents give characters natural voice personality without plot hallucinations.
3. **Gnani AI Voice Intelligence:** State-of-the-art Indic speech-to-text (**Prisma v3.0**) and expressive multilingual text-to-speech (**Timbre v2.5**) supporting Indian English and Telugu with zero-downtime offline fallbacks.
4. **Context-Aware Discovery:** Filter experiences by exact free time (`2 min`, `5 min`, `10 min`, `15 min`) and current mood (`Curious`, `Excited`, `Relaxed`, `Bored`, `Playful`).
5. **Five Original Intellectual Property Universes:** Built entirely from scratch across five story genres.

---

## 🎭 The Five Story Worlds

| Domain | Story Title | Premise | Duration | Flagship Status |
| :--- | :--- | :--- | :--- | :--- |
| 🔍 **Mystery / Investigation** | **The Archive of Unsent Goodbyes** | Letters arrive from loved ones with forgotten memories—stamped with tomorrow's date. | 10 min | **Flagship (Playable Start-to-End)** |
| ⚡ **Thriller / Suspense** | **Platform Zero** | A midnight metro train where intercom announcements predict passenger actions. | 5 min | Playable Prototype |
| 🧭 **Adventure / Exploration** | **The Atlas of Borrowed Weather** | An airship voyager maps islands that appear only under traded monsoon storms. | 10 min | Playable Prototype |
| 🎭 **Comedy / Fun** | **The Department of Lost Excuses** | A rogue municipal AI rejects every excuse in the city until hit with a paradox. | 5 min | Playable Prototype |
| 🌌 **Science Fiction** | **The Moon Sends Voice Notes** | Deep-space communications receive an urgent lunar voice note from 19 hours in the future. | 10 min | Playable Prototype |

---

## 📐 Dual-Engine Architecture

```
+-----------------------------------------------------------------------------------+
|                           STORYPULSE MOBILE CLIENT                                |
|           React Native (Expo SDK 52) • TypeScript • Expo AV • Native Styles       |
+-----------------------------------------------------------------------------------+
                                         │ (HTTPS REST)
                                         ▼
+-----------------------------------------------------------------------------------+
|                              FASTAPI BACKEND SERVICE                              |
|           Python 3.12+ • FastAPI • Pydantic v2 • SQLite / SQLAlchemy 2.0          |
+-----------------------------------------------------------------------------------+
        │                                │                                │
        ▼                                ▼                                ▼
+───────────────────────+    +───────────────────────+    +────────────────────────+
|  DETERMINISTIC ENGINE |    |    GNANI AI CLOUD     |    |   AUDIO CACHE & STORE  |
|  • Canonical Facts    |    |  • Prisma v3 STT      |    |  • MD5 Voice Caching   |
|  • Clue Dependencies  |    |    (api.vachana.ai)   |    |  • Clue Lore Records   |
|  • Scene Transitions  |    |  • Timbre v2.5 TTS    |    |  • Session DB Tables   |
|  • Ending Triggers    |    |    (api.vachana.ai)   |    |                        |
+───────────────────────+    +───────────────────────+    +────────────────────────+
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python:** 3.11+
- **Node.js:** v18+ (Verified on v22.16)
- **Expo Go App:** Installed on your Android mobile device (or Android Emulator)

### 2. Backend Setup & Launch
```bash
# Navigate to backend directory
cd backend

# Create & configure .env
copy .env.example .env
# Optional: Add GNANI_API_KEY from https://platform.gnani.ai/
# If unset, StoryPulse automatically runs with high-fidelity transparent mock fallback.

# Run backend verification test suite (100% Pass)
python run_tests.py

# Launch FastAPI development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive OpenAPI documentation will be accessible at: `http://localhost:8000/docs`.

### 3. Mobile Client Setup & Launch
```bash
# Open a new terminal in mobile/ directory
cd mobile

# Install dependencies
npm install

# Start Expo development server
npx expo start
```
- Press `a` to run on Android Emulator.
- Or scan the terminal QR code with **Expo Go** on any physical Android smartphone on the same Wi-Fi network.

---

## 🧪 Testing & Verification Results

The automated test runner validates all 5 core subsystems:
```
============================================================
STORYPULSE AI BACKEND VERIFICATION SUITE
============================================================
[TEST 1/5] Verifying Story Loader for all 5 domains...
 -> PASS: All 5 domains loaded with complete scene and ending graphs.
[TEST 2/5] Verifying Narrative Engine State Transitions...
 -> PASS: Full flagship narrative tree traversed from opening to canonical ending.
[TEST 3/5] Verifying Invalid Action Handling...
 -> PASS: Narrative engine safely rejected out-of-context action without state corruption.
[TEST 4/5] Verifying Gnani Prisma & Timbre Service integration...
 -> PASS: Gnani Prisma STT & Timbre TTS adapters functioning properly.
[TEST 5/5] Verifying FastAPI Endpoint Handlers (Health, Stories, Sessions, Actions)...
 -> PASS: All API endpoint contracts validated (Health, Catalog, Creation, Action).
============================================================
ALL 5 BACKEND VERIFICATION TEST SUITES PASSED (100% SUCCESS)
============================================================
```

---

## 🛡️ Security, Privacy & Compliance
- **Zero API Keys in Client Bundles:** All Gnani AI credentials reside strictly on backend servers.
- **Ephemeral Audio Storage:** Audio recorded via microphone is cached only for transcription and unlinked immediately.
- **Microphone Permissions:** Explicit permission requests with push-to-talk activation only (no ambient recording).
- **Graceful Fallbacks:** Full keyboard typing mode and subtitle display available for quiet transit spaces.

---

## 📜 Complete Documentation Index
All 17 technical documents are available in `docs/`:
- [`00_DOCUMENTATION_INVENTORY.md`](docs/00_DOCUMENTATION_INVENTORY.md)
- [`01_PRD_Product_Requirements.md`](docs/01_PRD_Product_Requirements.md)
- [`02_TRD_Technical_Requirements.md`](docs/02_TRD_Technical_Requirements.md)
- [`03_APP_FLOW.md`](docs/03_APP_FLOW.md)
- [`04_UI_UX_Design_Brief.md`](docs/04_UI_UX_Design_Brief.md)
- [`05_BACKEND_SCHEMA.md`](docs/05_BACKEND_SCHEMA.md)
- [`06_IMPLEMENTATION_PLAN.md`](docs/06_IMPLEMENTATION_PLAN.md)
- [`07_MASTER_CONTEXT.md`](docs/07_MASTER_CONTEXT.md)
- [`08_SYSTEM_ARCHITECTURE.md`](docs/08_SYSTEM_ARCHITECTURE.md)
- [`09_STORY_ENGINE_DESIGN.md`](docs/09_STORY_ENGINE_DESIGN.md)
- [`10_GNANI_AI_INTEGRATION.md`](docs/10_GNANI_AI_INTEGRATION.md)
- [`11_IMAGE_ASSET_PLAN.md`](docs/11_IMAGE_ASSET_PLAN.md)
- [`12_ORIGINAL_STORY_BIBLE.md`](docs/12_ORIGINAL_STORY_BIBLE.md)
- [`13_API_SPECIFICATION.md`](docs/13_API_SPECIFICATION.md)
- [`14_TESTING_STRATEGY.md`](docs/14_TESTING_STRATEGY.md)
- [`15_DEPLOYMENT_GUIDE.md`](docs/15_DEPLOYMENT_GUIDE.md)
- [`16_DOCUMENTATION_VALIDATION_REPORT.md`](docs/16_DOCUMENTATION_VALIDATION_REPORT.md)

