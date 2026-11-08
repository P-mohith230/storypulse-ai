# StoryPulse AI — Testing & AI Evaluation Strategy
**Document ID:** `14_TESTING_STRATEGY`  
**Version:** `1.0.0`  
**Status:** Approved  
**Last Updated:** 2026-11-08  

---

## 1. Testing Pyramid

```
                / \
               /   \      E2E Journey Tests (Playthrough on Android Device)
              /     \
             /-------\    API Integration & Gnani Mock/Live Adapter Tests
            /         \
           /-----------\  Deterministic Narrative Engine State Machine Tests
          /             \
         /---------------\ Unit Tests (Schemas, State Models, Audio Utilities)
```

---

## 2. Test Suites & Coverage Targets

### 2.1 Narrative Engine & State Machine Tests (`backend/tests/test_engine.py`)
- **State Initialization:** Verifies initial scene, starting clues, and clean memory state.
- **Valid Transition:** Verifies matching keywords trigger expected scene change and clue rewards.
- **Invalid Action Handling:** Checks that gibberish or out-of-context commands do not mutate scene or clue state.
- **Prerequisite Enforcement:** Asserts that locked scenes reject transitions if required clues are missing.
- **Ending Termination:** Asserts that completing final scene transitions sets `is_completed: True` and resolves `ending_id`.

### 2.2 Gnani AI Integration Tests (`backend/tests/test_gnani_mock.py`)
- **Prisma STT Verification:**
  - Tests multipart file upload handling.
  - Verifies behavior when `GNANI_API_KEY` is present (real network call) versus absent (clean mock fallback).
  - Asserts response schema compatibility (`transcribed_text`, `confidence`, `provider`).
- **Timbre TTS Verification:**
  - Verifies synthesis requests with valid character voice parameters.
  - Asserts audio binary generation / caching mechanism.

### 2.3 Mobile Client Component & Navigation Tests
- **Discovery Screen Filter:** Tests that toggling Mood and Duration alters recommended story cards.
- **Voice Controller Gesture:** Tests press-and-hold microphone interaction and error badges on audio permission denial.

---

## 3. Measurable AI Evaluation Framework

To maintain empirical rigor, StoryPulse measures eight primary performance indices:

| Metric | Target | Measurement Method | Verification Class |
| :--- | :--- | :--- | :--- |
| **STT Word Error Rate (WER)** | `< 12%` | Compare 50 test utterances against human transcript | Automated Benchmark |
| **STT Latency (P95)** | `< 1500 ms` | Stopwatch timer from upload to text return | Automated Network Test |
| **TTS Synthesis Latency (P95)** | `< 1800 ms` | Benchmark timing on 25-word dialogue line | Automated Network Test |
| **Narrative Consistency** | `100%` | Zero state discrepancies across 100 random walks | Automated Simulation |
| **Invalid Action Handling** | `100%` | Zero state corruptions on 50 adversarial prompts | Automated Unit Tests |
| **TTS Playback Success Rate** | `> 98%` | Proportion of lines delivered with playable audio | Client Logging |
| **Story Completion Rate** | `> 75%` | Proportion of started sessions reaching an ending | Real Tester Feedback |
| **Cold Start to Interactive** | `< 2000 ms` | Mobile startup to Home screen ready | Android Device Profiler |
