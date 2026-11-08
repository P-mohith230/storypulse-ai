import { Platform } from "react-native";
import { StoryCatalogItem, SessionState, UserPreferences } from "../types";

const DEFAULT_LOCAL_URL = Platform.OS === "android" ? "http://10.0.2.2:8000" : "http://localhost:8000";
export const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || DEFAULT_LOCAL_URL;

export async function fetchHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    return await res.json();
  } catch (e) {
    console.warn("[API] Health check failed:", e);
    return null;
  }
}

export async function fetchStories(duration?: number, mood?: string): Promise<StoryCatalogItem[]> {
  try {
    const params = new URLSearchParams();
    if (duration) params.append("duration", duration.toString());
    if (mood) params.append("mood", mood);

    const res = await fetch(`${API_BASE_URL}/api/v1/stories?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (e) {
    console.error("[API] fetchStories error:", e);
    return [];
  }
}

export async function createSession(
  storyId: string,
  durationTarget: number = 5,
  moodSelected: string = "Curious",
  preferredLang: string = "en-IN"
): Promise<SessionState> {
  const res = await fetch(`${API_BASE_URL}/api/v1/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      story_id: storyId,
      duration_target: durationTarget,
      mood_selected: moodSelected,
      preferred_lang: preferredLang,
    }),
  });
  if (!res.ok) throw new Error(`Failed to create session: ${res.statusText}`);
  return await res.json();
}

export async function getSession(sessionId: string): Promise<SessionState> {
  const res = await fetch(`${API_BASE_URL}/api/v1/sessions/${sessionId}`);
  if (!res.ok) throw new Error(`Failed to get session: ${res.statusText}`);
  return await res.json();
}

export async function performAction(
  sessionId: string,
  actionText: string,
  inputModality: "TEXT" | "VOICE" | "TOUCH_TAP" = "TEXT"
): Promise<SessionState> {
  const res = await fetch(`${API_BASE_URL}/api/v1/sessions/${sessionId}/action`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      action_text: actionText,
      input_modality: inputModality,
    }),
  });
  if (!res.ok) throw new Error(`Action failed: ${res.statusText}`);
  return await res.json();
}

export async function transcribeAudio(audioUri: string, languageCode: string = "en-IN") {
  const formData = new FormData();
  formData.append("audio_file", {
    uri: audioUri,
    name: "recording.wav",
    type: "audio/wav",
  } as any);
  formData.append("language_code", languageCode);

  const res = await fetch(`${API_BASE_URL}/api/v1/speech/transcribe`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error(`Transcription failed: ${res.statusText}`);
  return await res.json();
}

export async function synthesizeSpeech(text: string, voiceId: string = "Nalini", language: string = "en-IN") {
  const res = await fetch(`${API_BASE_URL}/api/v1/speech/synthesize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text,
      voice_id: voiceId,
      language,
    }),
  });
  if (!res.ok) throw new Error(`Synthesis failed: ${res.statusText}`);
  return await res.json();
}

export async function fetchPreferences(): Promise<UserPreferences> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/preferences`);
    if (!res.ok) throw new Error();
    return await res.json();
  } catch {
    return {
      preferred_lang: "en-IN",
      audio_mode: "auto_tts",
      haptic_enabled: true,
      subtitles_enabled: true,
    };
  }
}

