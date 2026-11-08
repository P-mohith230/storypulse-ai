import React, { createContext, useContext, useState, useEffect } from "react";
import { SessionState, ClueItem, UserPreferences } from "../types";
import { fetchPreferences } from "../api/client";

interface StoryContextType {
  activeSession: SessionState | null;
  setActiveSession: (session: SessionState | null) => void;
  discoveredClues: ClueItem[];
  completedSessions: SessionState[];
  addCompletedSession: (session: SessionState) => void;
  preferences: UserPreferences;
  setPreferences: React.Dispatch<React.SetStateAction<UserPreferences>>;
}

const StoryContext = createContext<StoryContextType | undefined>(undefined);

export const StoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [activeSession, setActiveSession] = useState<SessionState | null>(null);
  const [completedSessions, setCompletedSessions] = useState<SessionState[]>([]);
  const [preferences, setPreferences] = useState<UserPreferences>({
    preferred_lang: "en-IN",
    audio_mode: "auto_tts",
    haptic_enabled: true,
    subtitles_enabled: true,
  });

  useEffect(() => {
    fetchPreferences().then((prefs) => {
      if (prefs) setPreferences(prefs);
    });
  }, []);

  const addCompletedSession = (session: SessionState) => {
    setCompletedSessions((prev) => [session, ...prev.filter((s) => s.session_id !== session.session_id)]);
  };

  const discoveredClues = activeSession?.discovered_clues || [];

  return (
    <StoryContext.Provider
      value={{
        activeSession,
        setActiveSession,
        discoveredClues,
        completedSessions,
        addCompletedSession,
        preferences,
        setPreferences,
      }}
    >
      {children}
    </StoryContext.Provider>
  );
};

export const useStory = () => {
  const context = useContext(StoryContext);
  if (!context) {
    throw new Error("useStory must be used within a StoryProvider");
  }
  return context;
};

