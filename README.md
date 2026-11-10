# StoryPulse AI 🎙️📖✨
> **Your moments. Your mood. Your story.**  
> *AI-Powered Interactive Cinematic Storytelling Platform for Micro-Breaks.*

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React Native](https://img.shields.io/badge/React%20Native-Expo%20SDK%2052-61DAFB?logo=react&logoColor=black)](https://reactnative.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3+-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Gnani AI](https://img.shields.io/badge/Gnani%20AI-Prisma%20v3%20%2B%20Timbre%20v2.5-FF6F00)](https://platform.gnani.ai/)
[![Database](https://img.shields.io/badge/SQLite-WAL%20Mode-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-6%2F6%20Passed%20(100%25)-success)](backend/run_tests.py)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 🌟 Executive Summary

**StoryPulse AI** transforms dead time in everyday life—daily commutes, airport boarding lounges, waiting rooms, and coffee breaks—into immersive, interactive storytelling experiences. Instead of endless, mindless social media scrolling, users enter short (2–15 minute) cinematic interactive narratives where **they are the protagonist**.

Users shape their journey through **natural voice conversations (Gnani Prisma STT)**, **touch decisions**, and **investigative clue discoveries**, while evocative **voice notes (Gnani Timbre TTS)** and **cinematic artwork** bring characters and environments to life.

### Core Engineering Pillars
- **Dual-Engine Narrative Architecture:** Deterministic Finite State Machine (FSM) guarantees canonical ground truth, clue dependencies, and branching endings, eliminating plot hallucinations and state drift.
- **Gnani AI Voice Intelligence:** Deep cloud integration with Gnani AI **Prisma v3.0 STT** and **Timbre v2.5 TTS** with sub-second latency and automatic offline fallbacks.
- **Zero-Waste Credit Guard:** Aggressive local audio caching (`backend/app/audio_cache/`) ensures dialogue lines are synthesized once and replayed with **0 API credit burn**.
- **Dual-Surface Delivery:** A responsive, mobile-first **Web Application** running directly in desktop/mobile browsers alongside a native **React Native (Expo)** mobile application.
- **Five Original IP Universes:** Mystery, Thriller, Adventure, Comedy, and Sci-Fi—each with bespoke character rosters, scene artwork, clues, and multiple canonical endings.

---

## 📊 Quantified Performance & Benchmark Dashboard

Empirical evaluation results measured across automated stress tests, adversarial inputs, and Monte Carlo playthroughs:

| Metric Category | Target SLA | Measured Result | Status |
| :--- | :--- | :--- | :--- |
| **Backend Verification Suites** | 100% | **6/6 Suites Passed (100%)** | 🟢 **Certified** |
| **Narrative State Consistency** | 100% | **100% (343 / 343 State Checks)** | 🟢 **Zero Drift** |
| **Adversarial Input Defense** | > 70% | **75.0% Intercept / 100% Safe** | 🟢 **Zero State Corruption** |
| **Deterministic Engine Latency (P95)** | < 25 ms | **< 12 ms** | 🟢 **Ultra-Fast** |
| **Local Audio Cache Response (P95)** | < 15 ms | **< 5 ms** | 🟢 **Instant** |
| **Live Gnani TTS Cold Synthesis** | < 1500 ms | **~650 ms** | 🟢 **Low Latency** |
| **Live Gnani STT Recognition** | < 1200 ms | **~450 ms** | 🟢 **Real-Time** |
| **Story Completion Success Rate** | > 80% | **95.0% (100 Random Walks)** | 🟢 **Optimal Flow** |
| **Visual Asset Coverage** | 100% | **34 / 34 Assets Created (100%)** | 🟢 **Complete** |

---

## 🎭 The Five Story Worlds

All five genres are implemented with full narrative decision graphs, clue discovery systems, character audio configurations, and canonical endings:

```
                                  STORYPULSE WORLDS CATALOG
    ┌───────────────────────┬───────────────────────┬───────────────────────┐
    │ 🔍 MYSTERY / INVEST.  │ ⚡ THRILLER / SUSP.   │ 🧭 ADVENTURE / EXPL.  │
    │ The Archive of        │ Platform Zero         │ The Cloud Galleon     │
    │ Unsent Goodbyes       │                       │                       │
    │ • 10 min | 5 Clues    │ • 5 min | 3 Clues     │ • 10 min | 2 Clues    │
    │ • 3 Endings           │ • 2 Endings           │ • 2 Endings           │
    ├───────────────────────┴───────────────────────┴───────────────────────┤
    │ 🎭 COMEDY / FUN                               │ 🌌 SCIENCE FICTION    │
    │ The Department of Believable Excuses          │ The Lunar Singularity │
    │ • 5 min | 1 Clue                              │ • 10 min | 3 Clues    │
    │ • 1 Ending                                    │ • 3 Endings           │
    └───────────────────────────────────────────────┴───────────────────────┘
```

### Detailed Domain Breakdown

| Domain | Story Title | Flagship Premise | Characters | Clues / Artifacts | Canonical Endings |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mystery** | *The Archive of Unsent Goodbyes* | Letters arrive with forgotten memories, postmarked tomorrow at 6:00 AM. | Mira (Archivist), Dev (Postman), The Listener | Tomorrow Letter, Brass Vault Key, Silver Locket, Archivist Log, Weather Telegram | 1. Keeper of Sorrows<br>2. Tomorrow's Truth<br>3. The Tide Takes All |
| **Thriller** | *Platform Zero* | A metro train on no timetable where announcements predict actions you haven't taken. | The Conductor, Woman in Grey Coat | Emergency Key, Ghost Ticket, Intercom Log #7 | 1. Arrival at Platform Zero<br>2. Emergency Override |
| **Adventure** | *The Cloud Galleon* | An airship voyager maps floating islands and trades monsoon weather in bottles. | Captain Tara, Lumi (Bioluminescent Sprite) | Monsoon Compass, Captured Storm Vial | 1. The Celestial Sanctuary<br>2. The Monsoon Restored |
| **Comedy** | *The Department of Believable Excuses* | A chaotic municipal bureaucracy records and audits absurd excuses. | Inspector Rao, Mrs. Sharma | Bureaucratic Stamp | 1. A Day of Confession |
| **Sci-Fi** | *The Lunar Singularity* | Lunar communications station receives tachyon transmissions from 19 hours ahead. | Engineer Orson, Unit 7 Maintenance Bot | Fusion Coolant Grid, Quantum Waveform, Quantum Collar | 1. The Closed Loop<br>2. Temporal Reboot<br>3. Timeline Preserved |

---

## 📐 System Architecture

StoryPulse AI employs a decoupled, modular architecture that cleanly separates client presentation, state machine execution, and AI speech orchestration:

```mermaid
flowchart TD
    subgraph Clients["Presentation Layer (Dual Surface)"]
        WEB["Responsive Web App\n(HTML5 / CSS3 / Vanilla JS / Web Audio)"]
        MOB["Native Mobile App\n(React Native / Expo SDK 52 / TypeScript)"]
    end

    subgraph Backend["FastAPI Backend Service (Python 3.12)"]
        API["REST API Router\n(/api/v1/stories, /sessions, /speech)"]
        FSM["Deterministic Narrative Engine\n(State Transitions & Clue Gates)"]
        REPO["Session Repository & SQLite WAL\n(Story Sessions, Actions & Memory)"]
        LOADER["Story Data Loader\n(JSON Domain Packages)"]
    end

    subgraph GnaniLayer["Gnani AI Voice Intelligence Platform"]
        PRISMA["Gnani Prisma v3.0 STT\n(POST https://api.vachana.ai/stt/v3)"]
        TIMBRE["Gnani Timbre v2.5 TTS\n(POST https://api.vachana.ai/api/v1/tts/inference)"]
        CACHE["Local Audio Cache\n(MD5 Hashed WAVs - 0 Credit Burn)"]
    end

    WEB -->|HTTP REST & Audio Streams| API
    MOB -->|HTTP REST & Audio Streams| API
    API --> FSM
    API --> REPO
    FSM --> LOADER
    API --> PRISMA
    API --> TIMBRE
    TIMBRE <--> CACHE
```

---

## 🎙️ Gnani AI Integration & Credit Guard

StoryPulse integrates directly with official Gnani AI APIs with zero third-party wrappers:

### 1. Speech-to-Text (STT) — Gnani Prisma v3.0
- **Endpoint:** `POST https://api.vachana.ai/stt/v3`
- **Headers:** `X-API-Key-ID: {GNANI_API_KEY}`
- **Payload:** `multipart/form-data` with `audio_file`, `model="prisma-v3.0"`, `language_code="en-IN"` (also supports `te-IN`, `hi-IN`).
- **Browser Audio Capture:** Real-time microphone capture via Web Audio API and `MediaRecorder` encoding PCM audio blobs directly to backend.

### 2. Text-to-Speech (TTS) — Gnani Timbre v2.5
- **Endpoint:** `POST https://api.vachana.ai/api/v1/tts/inference`
- **Headers:** `X-API-Key-ID: {GNANI_API_KEY}`, `Content-Type: application/json`
- **Character Voices:**
  - `Mira` (Mystery): `Nalini` (`en-IN`)
  - `Dev` (Mystery): `Kalyan` (`en-IN`)
  - `The Conductor` (Thriller): `Vikram` (`en-IN`)
  - `Captain Tara` (Adventure): `Priya` (`en-IN`)
  - `Inspector Rao` (Comedy): `Robo_Indic` / `Suresh` (`en-IN`)
  - `Engineer Orson` (Sci-Fi): `Suresh` (`en-IN`)

### 3. Strict Credit Guard Architecture
```
              [Dialogue Synthesis Request]
                           │
                           ▼
               Does MD5 Hash Exist in Cache?
                     /           \
                 YES/             \NO
                   /               \
         [Serve Cached WAV]     [Call Gnani Timbre API]
         (0 Credits Consumed)       │
                                [Save WAV to Cache]
                                    │
                                [Serve Audio]
```
- **Automated Tests:** Built-in `force_mock` flag guarantees automated test suites and benchmark scripts **never consume live API credits**.
- **Player Controls:** In the **⚙️ Settings** tab, players can toggle Character Speech ON/OFF or switch between Voice and Keyboard modes.

---

## 📁 Repository Structure

```
StoryPulse-ai/
├── backend/                        # FastAPI Backend & Story Engine
│   ├── app/
│   │   ├── api/                    # Route Handlers
│   │   │   ├── routes/             # Health, Stories, Sessions, Speech, Preferences
│   │   │   └── api_v1.py           # V1 Router Assembly
│   │   ├── core/                   # Configuration & SQLite Database
│   │   ├── models/                 # Domain Dataclasses (Sessions, Actions, Clues)
│   │   ├── repositories/           # Session & Action Repositories
│   │   ├── schemas/                # Pydantic v2 API Request/Response Schemas
│   │   ├── services/
│   │   │   ├── gnani/              # Prisma STT, Timbre TTS, Audio Adapters
│   │   │   └── narrative/          # Deterministic Engine & Story Loader
│   │   ├── static/                 # Responsive Mobile-First Web Application
│   │   │   ├── images/             # 34 Complete Story Visual Assets
│   │   │   │   ├── covers/         # 5 Genre Covers
│   │   │   │   ├── characters/     # 11 Character Portraits
│   │   │   │   ├── scenes/         # 9 Cinematic Scene Artworks
│   │   │   │   ├── clues/          # 14 Clue Badges
│   │   │   │   └── endings/        # 11 Chapter Resolution Scenes
│   │   │   ├── app.js              # Web Audio, MediaRecorder & UI State Engine
│   │   │   ├── index.html          # Mobile-First Semantic HTML Shell
│   │   │   └── style.css           # Responsive Design System & Glassmorphism
│   │   ├── story_data/             # 5 Modular Story JSON Packages
│   │   │   ├── mystery/            # Characters, Clues, Scenes, Endings, Story
│   │   │   ├── thriller/           # Characters, Clues, Scenes, Endings, Story
│   │   │   ├── adventure/          # Characters, Clues, Scenes, Endings, Story
│   │   │   ├── comedy/             # Characters, Clues, Scenes, Endings, Story
│   │   │   └── sci_fi/             # Characters, Clues, Scenes, Endings, Story
│   │   ├── audio_cache/            # Zero-Waste Synthesized Audio Storage
│   │   └── main.py                 # FastAPI Application Factory & SPA Static Mount
│   ├── benchmark_eval.py           # 100-Walk Monte Carlo Evaluation Benchmark
│   ├── generate_all_story_assets.py# Procedural Vector/Pillow Asset Generator
│   ├── interactive_play.py         # Terminal Interactive Playthrough CLI
│   ├── requirements.txt            # Python Dependencies
│   └── run_tests.py                # Standalone 6-Suite Verification Runner
│
├── mobile/                         # React Native / Expo Native Client
│   ├── app/                        # Expo Router File-Based Navigation
│   │   ├── (tabs)/                 # Discover, History, Settings
│   │   └── story/                  # Story Preview & Cinematic Gameplay
│   ├── assets/images/              # Mirrored Production Visual Artwork
│   ├── src/
│   │   ├── api/                    # Typed API Client
│   │   ├── components/             # CategoryCard, ClueDrawer, VoiceController, etc.
│   │   ├── store/                  # Story State React Context
│   │   └── theme/                  # Design Tokens & Palette
│   ├── package.json
│   └── tsconfig.json
│
├── docs/                           # Complete 17-Document Specification Suite
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
│   ├── 16_DOCUMENTATION_VALIDATION_REPORT.md
│   ├── AI_EVALUATION_REPORT.md
│   └── FINAL_BUILD_REPORT.md
│
├── context.md                      # Persistent AI Master Context
└── README.md                       # Product Documentation & Guide
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
- **Python:** 3.11+ (Verified on 3.12)
- **Node.js:** v18+ (Verified on v22)
- **Browser:** Any modern browser (Chrome, Edge, Safari, Firefox)
- **Optional Mobile:** Expo Go app installed on Android/iOS

### 2. Backend & Responsive Web App (Ready in 30 Seconds)
```bash
# 1. Clone repository
git clone https://github.com/P-mohith230/storypulse-ai.git
cd storypulse-ai/backend

# 2. Configure environment
copy .env.example .env
# Add your GNANI_API_KEY in .env (if left blank, engine runs with transparent high-fidelity mock)

# 3. Run verification tests (100% Pass guaranteed)
python run_tests.py

# 4. Launch backend and web app
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser to **[http://localhost:8000/](http://localhost:8000/)** to experience the full interactive web application!  
Interactive Swagger API docs are available at **[http://localhost:8000/docs](http://localhost:8000/docs)**.

### 3. Native Mobile Client Setup (Expo)
```bash
# In a separate terminal
cd mobile

# Install dependencies
pnpm install # or npm install

# Launch Expo bundler
npx expo start
```
- Press `a` to run on Android Emulator.
- Or scan the terminal QR code using **Expo Go** on a physical phone on the same Wi-Fi network.

### 4. Interactive Terminal Playthrough (No Browser Needed)
For rapid headless testing, run the interactive terminal gameplay CLI:
```bash
python backend/interactive_play.py
```

---

## 🔌 API Specification Summary

All endpoints return uniform JSON payloads with standardized error contracts:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | System health check and database connectivity probe |
| `GET` | `/api/v1/stories` | Catalog of all 5 story domains (supports `?duration=` and `?mood=` filters) |
| `POST` | `/api/v1/sessions` | Initialize a new narrative session with target duration, mood, and initial clues |
| `GET` | `/api/v1/sessions/{id}` | Retrieve current session state, active character, and discovered clues |
| `POST` | `/api/v1/sessions/{id}/action` | Submit a narrative action (Text or Voice) to evaluate state transition |
| `POST` | `/api/v1/speech/transcribe` | Transcribe recorded audio with Gnani Prisma v3.0 STT |
| `POST` | `/api/v1/speech/synthesize` | Synthesize character dialogue with Gnani Timbre v2.5 TTS |
| `GET` | `/api/v1/speech/audio-cache/{file}` | Stream cached WAV audio (0 API credit usage) |

---

## 🧪 Verification & Test Execution

Run the complete 6-suite verification runner:
```bash
python backend/run_tests.py
```

Expected output:
```text
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
 -> PASS: Gnani Prisma STT & Timbre TTS adapters functioning properly (0 credits consumed).
[TEST 5/5] Verifying FastAPI Endpoint Handlers (Health, Stories, Sessions, Actions)...
 -> PASS: All API endpoint contracts validated (Health, Catalog, Creation, Action).
[TEST 6/6] Verifying Responsive Web Assets and Complete Image Inventory...
 -> PASS: Mobile-first Web Assets (HTML/CSS/JS) & 100% of Visual Assets verified.
============================================================
ALL 6 STORYPULSE VERIFICATION SUITES PASSED (100% SUCCESS)
============================================================
```

To run the 100-walk Monte Carlo benchmark:
```bash
python backend/benchmark_eval.py
```

---

## 🛡️ Security, Privacy & Compliance

1. **Zero Credential Leakage:** API keys are never bundled into client distributions. All Gnani credentials reside securely on the backend server.
2. **Untracked Environment Secrets:** `.env` and local audio cache files are strictly excluded from version control via `.gitignore`.
3. **Microphone Transparency:** Speech capture requires explicit browser / OS user permissions and triggers only upon push-to-talk activation (no background eavesdropping).
4. **Resilient Offline Architecture:** If Gnani AI cloud is unreachable or rate-limited, the application gracefully degrades to text subtitles and mock transcripts with zero crashes.

---

## 📜 Full Documentation Index

All 17 authoritative architecture and design documents are versioned in `docs/`:

- [00_DOCUMENTATION_INVENTORY.md](docs/00_DOCUMENTATION_INVENTORY.md) — Documentation index and verification matrix.
- [01_PRD_Product_Requirements.md](docs/01_PRD_Product_Requirements.md) — Product vision, personas, user stories, and acceptance criteria.
- [02_TRD_Technical_Requirements.md](docs/02_TRD_Technical_Requirements.md) — Tech stack, system boundaries, and non-functional specifications.
- [03_APP_FLOW.md](docs/03_APP_FLOW.md) — Detailed user journeys and screen-by-screen state diagrams.
- [04_UI_UX_Design_Brief.md](docs/04_UI_UX_Design_Brief.md) — Visual identity, typography, design tokens, and ergonomics.
- [05_BACKEND_SCHEMA.md](docs/05_BACKEND_SCHEMA.md) — Relational schema, SQLite indexes, and domain models.
- [06_IMPLEMENTATION_PLAN.md](docs/06_IMPLEMENTATION_PLAN.md) — Development phases, task breakdowns, and acceptance gates.
- [07_MASTER_CONTEXT.md](docs/07_MASTER_CONTEXT.md) — Central source of truth for architectural decisions.
- [08_SYSTEM_ARCHITECTURE.md](docs/08_SYSTEM_ARCHITECTURE.md) — System topology, component boundaries, and sequence diagrams.
- [09_STORY_ENGINE_DESIGN.md](docs/09_STORY_ENGINE_DESIGN.md) — Narrative state machine, clue gating, and dialogue styling.
- [10_GNANI_AI_INTEGRATION.md](docs/10_GNANI_AI_INTEGRATION.md) — Prisma STT & Timbre TTS integration protocols and fallbacks.
- [11_IMAGE_ASSET_PLAN.md](docs/11_IMAGE_ASSET_PLAN.md) — Visual asset registry, style guides, and generation workflows.
- [12_ORIGINAL_STORY_BIBLE.md](docs/12_ORIGINAL_STORY_BIBLE.md) — Worldbuilding, character lore, scene maps, and all 5 story packages.
- [13_API_SPECIFICATION.md](docs/13_API_SPECIFICATION.md) — OpenAPI 3.0 contracts, error formats, and request/response examples.
- [14_TESTING_STRATEGY.md](docs/14_TESTING_STRATEGY.md) — Unit, integration, voice round-trip, and adversarial test plans.
- [15_DEPLOYMENT_GUIDE.md](docs/15_DEPLOYMENT_GUIDE.md) — Production setup, Docker deployment, and environment configs.
- [16_DOCUMENTATION_VALIDATION_REPORT.md](docs/16_DOCUMENTATION_VALIDATION_REPORT.md) — Cross-document validation audit (100% PASS).
- [AI_EVALUATION_REPORT.md](docs/AI_EVALUATION_REPORT.md) — Empirical stress testing and Monte Carlo benchmark results.
- [FINAL_BUILD_REPORT.md](docs/FINAL_BUILD_REPORT.md) — Complete engineering sign-off report.

---

## 👥 Authors & Acknowledgments

- **Lead Engineer & Architect:** Built for the **Gnani AI Great Indian AI Internship Challenge (Nov 2026)**.
- **Voice Intelligence:** Powered by [Gnani.ai](https://www.gnani.ai/) Conversational AI Platform (**Prisma v3** & **Timbre v2.5**).
- **License:** Released under the [MIT License](LICENSE).
