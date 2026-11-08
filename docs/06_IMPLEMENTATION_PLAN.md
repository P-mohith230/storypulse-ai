# StoryPulse AI — Implementation Plan & Milestone Roadmap
**Document ID:** `06_IMPLEMENTATION_PLAN`  
**Version:** `1.0.0`  
**Status:** Approved  
**Last Updated:** 2026-11-08  

---

## 1. Development Phases & Milestones

| Phase | Milestone Name | Key Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Phase 0** | Workspace Audit | Directory inspection, document inventory, exclusions | **COMPLETED** |
| **Phase 1** | Documentation Suite | 16 comprehensive specifications + `context.md` | **IN PROGRESS** |
| **Phase 2** | Architecture Verification | Cross-document consistency review, schema alignment | PENDING |
| **Phase 3** | Backend & Mobile Init | FastAPI setup, SQLite models, React Native Expo initialization | PENDING |
| **Phase 4** | Narrative State Engine | Deterministic engine, state validator, clue locks | PENDING |
| **Phase 5** | Five Story Packages | Mystery (Flagship), Thriller, Adventure, Comedy, Sci-Fi JSON configs | PENDING |
| **Phase 6** | Visual Assets & Manifest | Original illustrated scene covers, character avatars, clue icons | PENDING |
| **Phase 7** | Gnani AI Integration | Prisma STT service, Timbre TTS service, audio converters | PENDING |
| **Phase 8** | Mobile UI Implementation | Home, Category cards, Gameplay screen, Clue drawer, Voice controller | PENDING |
| **Phase 9** | End-to-End Integration | Full audio-visual dialogue loop, session persistence | PENDING |
| **Phase 10**| Testing & Verification | Unit tests, mock adapter tests, mobile Android testing | PENDING |
| **Phase 11**| Deployment & Demo | Local & cloud deployment configs, demo script, video guide | PENDING |
| **Phase 12**| Final Build Report | Final report (`FINAL_BUILD_REPORT.md`), project delivery | PENDING |

---

## 2. Detailed Task Breakdown

### Phase 1: Documentation Suite
- [x] `docs/00_DOCUMENTATION_INVENTORY.md`
- [x] `docs/01_PRD_Product_Requirements.md`
- [x] `docs/02_TRD_Technical_Requirements.md`
- [x] `docs/03_APP_FLOW.md`
- [x] `docs/04_UI_UX_Design_Brief.md`
- [x] `docs/05_BACKEND_SCHEMA.md`
- [x] `docs/06_IMPLEMENTATION_PLAN.md`
- [ ] `docs/07_MASTER_CONTEXT.md`
- [ ] `docs/08_SYSTEM_ARCHITECTURE.md`
- [ ] `docs/09_STORY_ENGINE_DESIGN.md`
- [ ] `docs/10_GNANI_AI_INTEGRATION.md`
- [ ] `docs/11_IMAGE_ASSET_PLAN.md`
- [ ] `docs/12_ORIGINAL_STORY_BIBLE.md`
- [ ] `docs/13_API_SPECIFICATION.md`
- [ ] `docs/14_TESTING_STRATEGY.md`
- [ ] `docs/15_DEPLOYMENT_GUIDE.md`
- [ ] `docs/16_DOCUMENTATION_VALIDATION_REPORT.md`
- [ ] `context.md` (at root)

### Phase 3 & 4: Backend & Narrative Engine
- Scaffold `backend/` with FastAPI, SQLAlchemy models, Pydantic schemas.
- Implement `StoryEngine` with deterministic scene transitions, clue dependency checks, and session states.
- Implement JSON loaders for all 5 domains.
- Write unit tests for narrative progression.

### Phase 5 & 6: Story Bible & Visual Assets
- Author complete narrative trees for:
  - *The Archive of Unsent Goodbyes* (5 scenes, 5 clues, 3 endings)
  - *Platform Zero* (3 scenes, 3 clues, 2 endings)
  - *The Atlas of Borrowed Weather* (3 scenes, 3 clues, 2 endings)
  - *The Department of Lost Excuses* (3 scenes, 3 clues, 2 endings)
  - *The Moon Sends Voice Notes* (3 scenes, 3 clues, 2 endings)
- Prepare clean visual asset inventory and manifest (`IMAGE_ASSET_PLAN.md`).

### Phase 7: Gnani AI Audio Services
- Implement `gnani_client.py`, `prisma_service.py`, `timbre_service.py`, `audio_service.py`.
- Support official REST endpoints: `https://api.vachana.ai/stt/v3` and `https://api.vachana.ai/api/v1/tts/inference`.
- Build comprehensive test mock mode to ensure zero crashes when credentials are not yet supplied.

### Phase 8 & 9: React Native Mobile Client
- Scaffold mobile client with Expo SDK, TypeScript, Expo Audio / AV.
- Implement Home screen with Mood & Duration filters, Category cards, and Featured story.
- Implement Gameplay screen with scene artwork, character portraits, dynamic dialogue bubbles, voice hold-to-talk button, and clue drawer.
- Connect mobile client to backend endpoints.

---

## 3. Risk Register & Mitigation Strategy

| Risk ID | Description | Impact | Probability | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **R-01** | Missing or rate-limited Gnani API key during local evaluation | High | Medium | Implement robust `MockGnaniService` with realistic transcripts and synthetic audio fallbacks, explicitly labeled in UI. |
| **R-02** | LLM hallucinating impossible clues | High | Low | Ground truth locked in deterministic Narrative Engine; LLM only formats character dialogue. |
| **R-03** | Audio latency on slow cellular connections | Medium | Medium | Pre-cache common audio lines, stream transcripts, show animated typing while audio synthesizes. |
| **R-04** | Android permissions rejection for mic | Medium | Medium | Provide seamless inline keyboard action bar with full feature parity. |
