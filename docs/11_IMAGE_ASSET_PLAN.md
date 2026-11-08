# StoryPulse AI — Visual & Image Asset Plan
**Document ID:** `11_IMAGE_ASSET_PLAN`  
**Version:** `1.0.0`  
**Status:** Approved  
**Last Updated:** 2026-11-08  

---

## 1. Visual Strategy: "Image-Led Cinematic Fiction"

Every story in StoryPulse is supported by an original suite of visual assets:
- **Story Domain Covers (5):** Hero banner cards with distinct palettes and symbolic motifs.
- **Character Portraits (3 per story):** High-detail circular avatar badges with lighting matching the story.
- **Scene Backgrounds (3–6 per story):** Full-bleed mobile portrait format (9:16 or 4:5 aspect ratio) showing atmospheric locations.
- **Clue Dossier Illustrations (3–5 per story):** Tactile evidence cards with parchment, wax seals, or futuristic tech artifacts.
- **Ending Epilogue Illustrations (2–3 per story):** Grand resolution scenes.

---

## 2. Flagship Story Asset Manifest: *The Archive of Unsent Goodbyes*

| Asset ID | Category | Target Filename | Aspect Ratio | Visual Description & Lighting Prompt |
| :--- | :--- | :--- | :--- | :--- |
| `cov_mystery` | Cover | `cover_mystery.png` | 16:9 / 4:3 | Coastal cliff lighthouse at twilight, storm clouds, violet and amber atmospheric glow, solitary silhouette holding a lantern. |
| `char_mira` | Character | `char_mira.png` | 1:1 | Mira (30s), thoughtful expression, dark trench coat, scarf, holding brass library key, coastal warm lantern rim light. |
| `char_dev` | Character | `char_dev.png` | 1:1 | Dev (20s), postman in weathered canvas jacket, bewildered expression, holding an aged leather satchel. |
| `char_listener`| Character | `char_listener.png`| 1:1 | Shadowy silhouette against an illuminated stained glass window, anonymous, amber backlighting. |
| `scene_cliff` | Scene 1 | `scene_cliffside.png` | 4:5 (Mobile) | Windswept coastal path overlooking churning ocean, salt spray, stone postbox glowing faintly. |
| `scene_vault` | Scene 2 | `scene_archive_vault.png` | 4:5 (Mobile) | Underground cavern library, floor-to-ceiling wooden mail pigeonholes, dust motes caught in amber rays. |
| `scene_desk` | Scene 3 | `scene_reading_desk.png` | 4:5 (Mobile) | Heavy mahogany desk, unrolled parchment, brass desk lamp, fountain pen, open drawer revealing secret slot. |
| `scene_shore` | Scene 4 | `scene_shoreline_dawn.png` | 4:5 (Mobile) | Foggy dawn shoreline, waves lapping at an overturned rowboat, scattered letters floating on wet sand. |
| `clue_letter` | Clue 1 | `clue_tomorrow_letter.png` | 1:1 | Thick cream envelope, purple wax seal, ink postmark clearly reading "TOMORROW, 06:00 AM". |
| `clue_key` | Clue 2 | `clue_brass_vault_key.png` | 1:1 | Heavy ornate brass key with sea-salt patina and numeral '7' carved into the bow. |
| `clue_logbook` | Clue 3 | `clue_archivist_log.png` | 1:1 | Leather-bound delivery ledger with crossed-out recipient names written in familiar handwriting. |
| `clue_teardrop`| Clue 4 | `clue_silver_locket.png` | 1:1 | Tarnished silver teardrop locket containing folded blank rice paper. |
| `clue_telegram`| Clue 5 | `clue_weather_telegram.png`| 1:1 | Faded meteorological telegram warning of "Memories drifting inland on the eastern tide". |
| `end_secret` | Ending 1 | `end_archivist_secret.png` | 4:5 (Mobile) | Mira locking the grand vault doors, smiling in peace as the lighthouse beam sweeps across the room. |
| `end_delivery`| Ending 2 | `end_final_delivery.png` | 4:5 (Mobile) | Player handing the tomorrow-letter back to Dev as dawn breaks over the calm coastal harbor. |
| `end_erased` | Ending 3 | `end_memory_erased.png` | 4:5 (Mobile) | The archive empty, drifting mist, a single blank envelope resting on the stone steps. |

---

## 3. Asset Generation & Fallback Pipeline

1. **Integrated Image Generation:**
   - In environments equipped with the image generator subagent, artwork is generated matching these strict artistic prompts and saved into `mobile/assets/images/`.
2. **Deterministic High-Fidelity SVG / Canvas Fallbacks:**
   - For offline or local testing before remote asset generation, high-aesthetic vector gradient artwork with domain iconography is provided natively, guaranteeing zero missing asset crashes and beautiful visual presentation.

