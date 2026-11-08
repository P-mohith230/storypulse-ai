# StoryPulse AI — Project Context & Decisions (context.md)

## 1. Product Identity
- **Product Name:** StoryPulse AI
- **Tagline:** *Your moments. Your mood. Your story.*
- **Category:** AI-powered interactive storytelling and conversational entertainment platform for short everyday breaks (2–15 minutes).
- **Core Principle:** Cinematic, mobile-first interactive experience with voice and visual storytelling—not a plain chatbot.

## 2. Technical Decisions
- **Mobile Client:** React Native + Expo (SDK 52), TypeScript, Expo AV, Native styles.
- **Backend:** Python 3.12+ / FastAPI, Pydantic v2, SQLAlchemy 2.0 with SQLite (dev) / PostgreSQL (prod).
- **Voice AI:** Gnani AI Prisma (STT) at `https://api.vachana.ai/stt/v3` and Timbre (TTS) at `https://api.vachana.ai/api/v1/tts/inference`.
- **Narrative Architecture:** Dual-Engine Pattern:
  - Deterministic Narrative Engine in Python governs canon, scenes, valid actions, clue unlocks, and endings.
  - LLM/Dialogue Adapter styles character dialogue within strict scene knowledge boundaries.
  - LLM never invents canonical clues or forces transitions.
- **Story Domains:**
  1. Mystery / Investigation: *The Archive of Unsent Goodbyes* (Flagship)
  2. Thriller / Suspense: *Platform Zero*
  3. Adventure / Exploration: *The Atlas of Borrowed Weather*
  4. Comedy / Fun: *The Department of Lost Excuses*
  5. Science Fiction: *The Moon Sends Voice Notes*

## 3. Directory Layout
- `docs/`: 17 comprehensive specification documents.
- `backend/`: FastAPI application, narrative engine, story data JSONs, Gnani AI client services, test suites.
- `mobile/`: React Native Expo mobile application with full audio and visual interface.
- `context.md`: This file.

## 4. Current State
- Documentation suite completed and validated.
- Proceeding with Backend and Mobile implementation.
