# StoryPulse AI — Master Context & Project State
**Document ID:** `07_MASTER_CONTEXT`  
**Version:** `1.0.0`  
**Status:** Living Document  
**Last Updated:** 2026-11-08  

---

## 1. Project Purpose & Challenge Identity
- **Project Name:** StoryPulse AI
- **Tagline:** Your moments. Your mood. Your story.
- **Challenge:** Gnani AI Great Indian AI Internship Challenge (Submission Target: Nov 10, 2026).
- **Core Technology Requirement:** Real voice AI integration using Gnani AI's Prisma (STT) and Timbre (TTS), paired with mobile-first interactive storytelling.

---

## 2. Definitive Architectural Decisions

1. **Deterministic Narrative Ground Truth:**
   - The LLM does *not* invent clues, modify canon, or trigger story endings.
   - The backend `StoryEngine` is a deterministic finite state machine backed by structured JSON story packages.
   - The LLM acts purely as an emotional dialogue stylist given bounded character knowledge and facts.
2. **Gnani AI Audio Protocol:**
   - Base URL: `https://api.vachana.ai`
   - STT: `POST /stt/v3` (multipart/form-data with `audio_file`, `model="prisma-v3.0"` or `"prisma-v2.5"`, `language_code="indic-auto"` or `"en-IN"` / `"te-IN"`).
   - TTS: `POST /api/v1/tts/inference` (JSON payload with `text`, `voice`, `model="timbre-v2.5"`, `language`, `audio_config`).
   - Graceful Fallback: When `GNANI_API_KEY` is not present, the backend switches to transparent mock mode with explicit `[MOCK_FALLBACK]` flags, preventing unhandled exceptions.
3. **Five Original Story Domains:**
   - Mystery / Investigation: *The Archive of Unsent Goodbyes* (Flagship)
   - Thriller / Suspense: *Platform Zero*
   - Adventure / Exploration: *The Atlas of Borrowed Weather*
   - Comedy / Fun: *The Department of Lost Excuses*
   - Science Fiction: *The Moon Sends Voice Notes*
4. **Mobile Client Stack:**
   - React Native with Expo (SDK 52), TypeScript, Expo AV, and Native styling.
   - Mobile-first Android optimization, portrait-oriented layouts, full-bleed artwork, accessible 48dp+ tap targets.

---

## 3. Current Implementation Status

- [x] Phase 0: Workspace audit & document inventory completed.
- [x] Phase 1: Core specifications authored (`01_PRD` to `07_MASTER_CONTEXT`).
- [ ] Phase 1 (Cont.): Remaining technical specs (`08` to `16`) & `context.md`.
- [ ] Phase 2: Document validation report.
- [ ] Phase 3: Project scaffolding (Backend & Mobile).
- [ ] Phase 4–12: Complete execution roadmap.

