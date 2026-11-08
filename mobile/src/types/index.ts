export type StoryDomain = "mystery" | "thriller" | "adventure" | "comedy" | "sci_fi";

export type SessionMood = "Curious" | "Excited" | "Relaxed" | "Bored" | "Playful" | "Stressed";

export interface StoryCatalogItem {
  id: string;
  title: string;
  domain: StoryDomain;
  tagline: string;
  duration_min: number;
  moods: string[];
  cover_image: string;
  character_count: number;
  scene_count: number;
  clue_count: number;
  featured: boolean;
}

export interface ClueItem {
  id: string;
  title: string;
  description: string;
  thumbnail: string;
  discovered: boolean;
}

export interface ActiveCharacter {
  id: string;
  name: string;
  avatar_url: string;
}

export interface SceneData {
  scene_id: string;
  title: string;
  background_image: string;
  active_character: ActiveCharacter;
  dialogue: string;
  audio_url?: string | null;
  suggested_actions: string[];
  audio_status?: string;
}

export interface SessionState {
  session_id: string;
  story_id: string;
  previous_scene_id?: string | null;
  current_scene: SceneData;
  discovered_clues: ClueItem[];
  newly_unlocked_clue?: ClueItem | null;
  is_completed: boolean;
  ending_id?: string | null;
  ending_title?: string | null;
  ending_epilogue?: string | null;
  ending_image?: string | null;
  status: "ACTIVE" | "PAUSED" | "COMPLETED";
}

export interface UserPreferences {
  preferred_lang: string;
  audio_mode: "auto_tts" | "text_only";
  haptic_enabled: boolean;
  subtitles_enabled: boolean;
}

