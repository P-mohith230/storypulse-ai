# StoryPulse AI — Product Requirements Document (PRD)
**Document ID:** `01_PRD`  
**Version:** `1.0.0`  
**Status:** Approved  
**Last Updated:** 2026-11-08  

---

## 1. Product Vision & Tagline

> **Tagline:** *Your moments. Your mood. Your story.*

**StoryPulse AI** transforms small, dead gaps in everyday life (commutes, waiting rooms, coffee breaks, boarding gates) into cinematic, personalized, interactive storytelling adventures. Instead of doomscrolling social media, users step into bite-sized (2 to 15-minute) narrative worlds where they become the central decision-maker.

Through natural voice conversations, contextual text interactions, tangible clue investigations, and dynamic branching, StoryPulse delivers the emotional depth of an interactive audio drama paired with the visual richness of a graphic novel.

---

## 2. Problem Statement & Market Opportunity

### 2.1 The Problem
1. **Pervasive Micro-Boredom:** Urban adults experience 15–45 minutes of fragmented idle time daily (waiting for cabs, public transport, dentist queues). This time is largely consumed by passive, low-gratification algorithmic feeds (reels, shorts, doomscrolling) that leave users fatigued rather than refreshed.
2. **Generic Interactive Fiction:** Existing interactive text adventures (e.g., visual novels, basic text bots) either require 45+ minute uninterrupted sessions or rely on static, multiple-choice walls of text with zero atmospheric immersion.
3. **Chatbot Monotony:** Conversational AI products treat interactions as utilitarian queries or unstructured roleplays lacking dramatic arc, persistent clue tracking, consequence trees, or audiovisual polish.

### 2.2 The Opportunity
By unifying:
- **Time & Mood Sensitivity:** Tailoring story intensity to exact free time (2m, 5m, 10m, 15m) and emotional state (Curious, Bored, Stressed, Excited, Relaxed).
- **Indic-First Voice AI:** Incorporating Gnani AI's state-of-the-art Prisma (speech recognition) and Timbre (expressive voice synthesis) supporting English and Indian languages (starting with English and Telugu).
- **Deterministic Narrative Integrity:** Guaranteeing that while characters converse naturally via LLMs, the underlying plot, clues, and endings are strictly bound by a canonical state machine.

---

## 3. Target Audience & Personas

### Persona A: "The Urban Commuter" — Ananya (27, Hyderabad)
- **Context:** Commutes 40 minutes on the Hyderabad Metro daily with intermittent 5–10 minute wait periods.
- **Pain Points:** Reels cause eye fatigue and feel repetitive. Wants immersive escapism that fits within a train ride.
- **Goal:** Jump into a quick mystery like *The Archive of Unsent Goodbyes* using voice notes or quick tap responses.
- **Preferred Mode:** Audio-first with subtitles; high appreciation for Telugu-English code-mixed dialogue.

### Persona B: "The Quick Breaker" — Vikram (34, Bengaluru)
- **Context:** Software engineering lead with 10-minute pauses between code reviews and sprint syncs.
- **Pain Points:** Needs mental reset without opening heavy video games or starting long videos.
- **Goal:** Play a fast-paced thriller (*Platform Zero*) or laugh at *The Department of Lost Excuses*.
- **Preferred Mode:** Rapid decision taps + voice reaction; visual scene cards with immediate consequences.

---

## 4. Value Proposition & Differentiation

| Dimension | Standard Chatbot / AI Roleplay | Legacy Interactive Fiction | **StoryPulse AI** |
| :--- | :--- | :--- | :--- |
| **Pacing** | Open-ended, meandering, forgets goals | Long, static, text-heavy | **Bite-sized (2–15 min), curated dramatic arcs** |
| **Logic & Truth** | Hallucinates clues, resets lore | Hardcoded tree, brittle choices | **Dual-Engine: Deterministic State Machine + Dynamic LLM Dialogue** |
| **Voice Experience** | Generic TTS, high latency | No voice | **Gnani AI Prisma (STT) + Timbre (Expressive Indic TTS)** |
| **Visual Immersion** | Text-only chat bubbles | Static stock 2D sprites | **Cinematic visual cards, character portraits, collectible clue dossiers** |
| **Discovery** | Generic search prompt | Filter by genre only | **Contextual Mood & Duration intelligence engine** |

---

## 5. Product Features & MVP Scope

### 5.1 Must-Have (P0 — MVP Baseline)
1. **Five Curated Story Domains:**
   - *Mystery / Investigation:* "The Archive of Unsent Goodbyes" (Flagship playable end-to-end)
   - *Thriller / Suspense:* "Platform Zero"
   - *Adventure / Exploration:* "The Atlas of Borrowed Weather"
   - *Comedy / Fun:* "The Department of Lost Excuses"
   - *Sci-Fi / Futurist:* "The Moon Sends Voice Notes"
2. **Deterministic Narrative Engine:**
   - JSON-driven story packages containing scenes, clues, characters, actions, and ending rules.
   - Server-side state validation: LLM cannot hallucinate clues or bypass plot locks.
3. **Voice & Text Multimodal Input:**
   - One-tap push-to-talk voice recording sending audio to Gnani Prisma STT (`POST /api/v1/speech/transcribe`).
   - Gnani Timbre TTS playback for character lines (`POST /api/v1/speech/synthesize`).
   - Seamless manual keyboard fallback with full feature parity.
4. **Cinematic Mobile UX:**
   - Scene artwork cards, character portraits with emotional cues, clue drawer, action pills, live transcript.
5. **Mood & Duration Discovery:**
   - Filter experiences by duration (2m, 5m, 10m, 15m) and mood (Curious, Bored, Stressed, Excited, Relaxed).
6. **Session Resilience:**
   - Session pause, auto-save, and resume without state corruption.

### 5.2 Important (P1 — Post-MVP Polish)
1. Full interactive tree for all 5 stories with multiple branches.
2. Clue synthesis mechanics (combining two clues to unlock a hidden revelation).
3. Session history log with replayable audio snippets and branching charts.
4. Deep Indic language customization (seamless toggle between English and Telugu).

### 5.3 Nice-to-Have / Out-of-Scope (P2)
- Real-time multiplayer co-op storytelling.
- User-generated story creation portal.
- On-the-fly dynamic image generation for every single line of dialogue (prevented to maintain sub-second response times and visual continuity).

---

## 6. User Stories & Acceptance Criteria

### US-01: Quick Discovery by Context
- **As a** busy user waiting 5 minutes in line,  
- **I want to** specify my available time ("5 mins") and mood ("Curious"),  
- **So that** StoryPulse instantly recommends a gripping, appropriately paced story without decision fatigue.

### US-02: Seamless Voice Conversation
- **As a** mobile user holding my phone,  
- **I want to** press the microphone icon, speak naturally to a character (in English or Telugu),  
- **So that** my voice is transcribed accurately by Gnani Prisma and the character responds in their unique voice via Gnani Timbre.

### US-03: Clue Discovery & Investigation
- **As a** player investigating the mystery,  
- **I want to** uncover explicit clues (e.g., "The Damp Letter dated Tomorrow") that are added to my Clue Dossier,  
- **So that** I can present them to characters and unlock specific canonical endings.

---

## 7. Non-Functional Requirements (NFRs)

1. **Performance & Latency:**
   - STT transcription via Gnani Prisma roundtrip: `< 1500 ms` on 4G/Wi-Fi.
   - Narrative state transition & dialogue generation: `< 1200 ms`.
   - TTS synthesis roundtrip: `< 1800 ms`.
   - Cold start launch to interactive home screen: `< 2.0 s`.
2. **Reliability & Fallbacks:**
   - If Gnani AI service is unreachable or credentials missing, gracefully present typed fallback text with clear non-blocking error badge.
   - If user denies microphone permission, automatically transition to keyboard-first layout without crashing.
3. **Security & Privacy:**
   - Ephemeral voice audio: raw user audio files stored only in temporary cache during transcription, wiped immediately afterward.
   - Zero hardcoded API keys in client-side mobile bundles.
4. **Accessibility:**
   - Minimum 48x48 dp touch targets.
   - High-contrast text overlays on visual cards (WCAG AA compliant).
   - Complete closed captions for every synthesized voice line.
