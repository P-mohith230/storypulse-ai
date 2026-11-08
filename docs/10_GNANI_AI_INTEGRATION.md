# StoryPulse AI — Gnani AI Integration Architecture
**Document ID:** `10_GNANI_AI_INTEGRATION`  
**Version:** `1.0.0`  
**Status:** Approved & Verified via Official Docs  
**Last Updated:** 2026-11-08  

---

## 1. Verified Official Gnani AI Specifications

Following verification with official documentation (`https://docs.gnani.ai/` and `https://api.vachana.ai`):
- **Base Endpoint:** `https://api.vachana.ai`
- **Authentication Header:** `X-API-Key-ID: <GNANI_API_KEY>`

---

## 2. Speech-to-Text (STT) — Gnani Prisma v2.5 / v3.0

### 2.1 Endpoint Contract
- **Method:** `POST`
- **Path:** `https://api.vachana.ai/stt/v3`
- **Content-Type:** `multipart/form-data`
- **Headers:**
  - `X-API-Key-ID: {GNANI_API_KEY}`

### 2.2 Form Data Parameters
- `audio_file`: Binary stream of recorded audio (`.wav`, `.mp3`, `.m4a` or raw linear PCM).
- `model`: `"prisma-v2.5"` or `"prisma-v3.0"` (Defaults to `"prisma-v3.0"`).
- `language_code`: Locale identifier:
  - `"indic-auto"` (Automatic Indian language detection)
  - `"en-IN"` (Indian English)
  - `"te-IN"` (Telugu)
  - `"hi-IN"` (Hindi)

### 2.3 Response Structure
```json
{
  "transcript": "Let me see the letter dated tomorrow.",
  "confidence": 0.942,
  "language": "en-IN",
  "words": [
    {"word": "Let", "start_time": 0.05, "end_time": 0.22},
    {"word": "me", "start_time": 0.23, "end_time": 0.35},
    {"word": "see", "start_time": 0.36, "end_time": 0.51},
    {"word": "the", "start_time": 0.52, "end_time": 0.61},
    {"word": "letter", "start_time": 0.62, "end_time": 0.95},
    {"word": "dated", "start_time": 0.96, "end_time": 1.25},
    {"word": "tomorrow", "start_time": 1.26, "end_time": 1.68}
  ]
}
```

---

## 3. Text-to-Speech (TTS) — Gnani Timbre v2.5 / v3.0

### 3.1 Endpoint Contract
- **Method:** `POST`
- **Path:** `https://api.vachana.ai/api/v1/tts/inference`
- **Content-Type:** `application/json`
- **Headers:**
  - `X-API-Key-ID: {GNANI_API_KEY}`

### 3.2 JSON Request Payload
```json
{
  "text": "The postmark says tomorrow, Ananya. That should be impossible... unless you remember writing it?",
  "voice": "Nalini",
  "model": "timbre-v2.5",
  "language": "en-IN",
  "speed": 1.0,
  "audio_config": {
    "encoding": "linear_pcm",
    "container": "wav",
    "num_channels": 1,
    "sample_rate": 24000,
    "sample_width": 2
  }
}
```

### 3.3 Character Voice Mapping in StoryPulse
| Character | Story Domain | Timbre Voice ID | Language | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Mira** | Mystery | `Nalini` / `te_female_1` | en-IN / te-IN | Calm, introspective coastal archivist |
| **Dev** | Mystery | `Kalyan` / `te_male_1` | en-IN / te-IN | Earnest, bewildered mail carrier |
| **The Listener** | Mystery | `Aarav` / `en_male_deep` | en-IN | Enigmatic, low-frequency whisper |
| **Conductor** | Thriller | `Vikram` | en-IN | Staccato, urgent transit officer |
| **Breeze Keeper** | Adventure | `Priya` | en-IN | Light-hearted, melodic voyager |
| **System AI-404** | Comedy | `Robo_Indic` | en-IN | Overly pedantic bureaucrat |
| **Commander Rao** | Sci-Fi | `Suresh` | en-IN | Static-laced lunar researcher |

---

## 4. Fallback Architecture (Zero-Downtime Guarantee)

If `GNANI_API_KEY` is absent or the cloud API returns an error / timeout (`> 4000ms`), the system operates gracefully:
1. **STT Fallback:** If audio cannot be processed, the client receives a 200 response with simulated transcription or offers instant tap to type with no crash.
2. **TTS Fallback:** If speech synthesis is unreachable, the backend flags `audio_url: null` with `audio_status: "FALLBACK_TEXT_ONLY"`. The mobile app renders the text subtitles instantly with full readability.

