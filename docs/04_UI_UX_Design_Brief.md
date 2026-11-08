# StoryPulse AI — UI/UX Design Brief & Design System
**Document ID:** `04_UI_UX_Design_Brief`  
**Version:** `1.0.0`  
**Status:** Approved  
**Last Updated:** 2026-11-08  

---

## 1. Design Philosophy: "The Cinematic Pocket Cinema"

StoryPulse bridges the gap between literary adventure, graphic novels, and prestige audio dramas. It rejects the utilitarian look of generic messaging chatbots.

### 1.1 Core Design Pillars
1. **Atmospheric Immersion:** Every story domain has a distinct ambient lighting palette and visual weight.
2. **Subconscious Ergonomics:** One-thumb mobile reachability; primary actions and voice triggers reside comfortably within the lower 40% of the screen.
3. **Auditory & Haptic Feedback:** Physical cues (subtle haptic pulses on microphone activation, audio waveforms, distinct clue-unlock chimes).
4. **Legibility in Motion:** High contrast typography with dark, atmospheric backgrounds so users can read comfortably on shaking trains or in bright daylight.

---

## 2. Color System & Design Tokens

### 2.1 Core Neutral Palette
- **Background Deep:** `#0A0D14` (Midnight Obsidian)
- **Surface Elevation 1:** `#121722` (Charcoal Slate)
- **Surface Elevation 2:** `#1A2232` (Luminous Steel)
- **Border Subtle:** `#253146` (Muted Steel Line)
- **Text Primary:** `#F8FAFC` (Pure Pearl)
- **Text Secondary:** `#94A3B8` (Cool Grey)
- **Text Muted:** `#64748B` (Slate Fog)

### 2.2 Domain-Specific Color Gradients & Accents

| Story Domain | Primary Accent | Secondary Accent | Surface Gradient Tokens |
| :--- | :--- | :--- | :--- |
| **Mystery / Investigation** | `#8B5CF6` (Electric Violet) | `#F59E0B` (Amber Flame) | `linear-gradient(135deg, #101026 0%, #1E1B4B 100%)` |
| **Thriller / Suspense** | `#EF4444` (Crimson Pulse) | `#7F1D1D` (Blood Charcoal) | `linear-gradient(135deg, #1A090D 0%, #3B0712 100%)` |
| **Adventure / Exploration**| `#10B981` (Emerald Jade) | `#F97316` (Sunset Orange) | `linear-gradient(135deg, #042F2E 0%, #064E3B 100%)` |
| **Comedy / Fun** | `#FACC15` (Canary Spark) | `#EC4899` (Playful Magenta) | `linear-gradient(135deg, #2D1A38 0%, #4A1D4E 100%)` |
| **Science Fiction** | `#06B6D4` (Cyan Laser) | `#6366F1` (Ultraviolet) | `linear-gradient(135deg, #081B33 0%, #0C2A52 100%)` |

---

## 3. Typography Hierarchy

- **Primary Font Family:** System Sans-Serif (`Inter`, `SF Pro Display`, `Roboto`), selected for crisp readability at small sizes.
- **Display / Title Scale:**
  - `Hero Title`: 28sp / Line Height 34sp / SemiBold (700)
  - `Section Header`: 20sp / Line Height 26sp / Medium (600)
  - `Card Header`: 17sp / Line Height 22sp / SemiBold (600)
- **Body & Dialogue Scale:**
  - `Dialogue Spoken Text`: 16sp / Line Height 24sp / Regular (400) — enhanced line spacing for effortless reading.
  - `Action Button Text`: 14sp / Line Height 18sp / Medium (500)
  - `Metadata / Tags`: 12sp / Line Height 16sp / Regular (400) uppercase with `letter-spacing: 0.05em`.

---

## 4. Key UI Components & Interactions

### 4.1 The Story Domain Card
- Card height: 180dp with smooth rounded corners (`border-radius: 20px`).
- Deep layered background combining domain gradient, stylized emblem/silhouette, and subtle glassmorphism overlay (`rgba(255, 255, 255, 0.04)`).
- Quick tags at the top right: `[5 min]` and `[Curious]`.
- Bottom: Story Title + One-line hook.

### 4.2 The Cinematic Gameplay Viewport
- **Upper Canvas (45% viewport):** High-impact full-bleed scene artwork with gentle gradient fade at the base into `Surface Elevation 1`.
- **Character Avatar & Speach Bubble:**
  - 52x52 dp circular portrait badge with an active glowing ring indicating speaking status.
  - Spoken dialogue container with high-contrast text, speaker name tag, and inline audio replay icon.
- **Clue Drawer Button:** Floating badge showing unlocked count (`Clues: 2/5`) with indicator dot.
- **Decision Chips:** 2 to 3 pre-computed contextual action suggestions (e.g. `[ "Examine the envelope" ]`, `[ "Confront Dev about the postmark" ]`) that give players immediate touch options.
- **The Voice Controller (Floating Action Bar):**
  - High-affordance glowing microphone button in the lower center (64x64 dp).
  - Press & hold gesture activates pulsating concentric rings representing live voice capture.
  - Accompanying keyboard icon allows swift switch to typed text input.

### 4.3 Clue Dossier Card
- Dimensions: 100% width card with a metallic border indicator (`#F59E0B` for key evidence).
- Shows: Clue title, item thumbnail, discovery timestamp, and investigative note.

---

## 5. Accessibility & Motion Guidelines

1. **Touch Targets:** All interactive icons and chips have a minimum hit target of `48x48 dp`.
2. **Reduced Motion:** If user enables `prefers-reduced-motion` in device settings, disable parallax transforms and continuous pulsing rings, replacing them with simple opacity transitions.
3. **Color Contrast:** All dialogue text against background surfaces exceeds `7:1` contrast ratio (WCAG AAA).
4. **Captions & Transcript:** Spoken voice is accompanied by verbatim typed dialogue in real time so users in silent environments can enjoy the complete narrative without turning on audio.

