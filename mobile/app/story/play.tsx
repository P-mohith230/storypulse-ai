import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator } from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Colors } from "../../src/theme/colors";
import { useStory } from "../../src/store/StoryContext";
import { performAction, API_BASE_URL } from "../../src/api/client";
import { VoiceController } from "../../src/components/VoiceController";
import { ClueDrawer } from "../../src/components/ClueDrawer";
import { EndingModal } from "../../src/components/EndingModal";
import { ArrowLeft, Search, Volume2, Sparkles, MapPin } from "lucide-react-native";
import { Audio } from "expo-av";

export default function GameplayScreen() {
  const router = useRouter();
  const { activeSession, setActiveSession, addCompletedSession, preferences } = useStory();
  const [loadingAction, setLoadingAction] = useState(false);
  const [clueDrawerVisible, setClueDrawerVisible] = useState(false);
  const [soundObject, setSoundObject] = useState<Audio.Sound | null>(null);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  useEffect(() => {
    // If no active session, return to home
    if (!activeSession) {
      router.replace("/");
    }
  }, [activeSession]);

  // Audio playback effect whenever scene changes
  useEffect(() => {
    const playCurrentDialogue = async () => {
      if (preferences.audio_mode !== "auto_tts") return;
      const audioUrl = activeSession?.current_scene?.audio_url;
      if (!audioUrl) return;

      try {
        if (soundObject) {
          await soundObject.unloadAsync();
        }
        const fullAudioUrl = audioUrl.startsWith("http") ? audioUrl : `${API_BASE_URL}${audioUrl}`;
        const { sound } = await Audio.Sound.createAsync({ uri: fullAudioUrl });
        setSoundObject(sound);
        setIsPlayingAudio(true);
        sound.setOnPlaybackStatusUpdate((status) => {
          if (status.isLoaded && status.didJustFinish) {
            setIsPlayingAudio(false);
          }
        });
        await sound.playAsync();
      } catch (err) {
        console.warn("[Audio] Autoplay failed:", err);
        setIsPlayingAudio(false);
      }
    };

    playCurrentDialogue();

    return () => {
      if (soundObject) {
        soundObject.unloadAsync();
      }
    };
  }, [activeSession?.current_scene?.scene_id]);

  const handleReplayAudio = async () => {
    const audioUrl = activeSession?.current_scene?.audio_url;
    if (!audioUrl) return;

    try {
      const fullAudioUrl = audioUrl.startsWith("http") ? audioUrl : `${API_BASE_URL}${audioUrl}`;
      if (soundObject) {
        await soundObject.replayAsync();
        setIsPlayingAudio(true);
      } else {
        const { sound } = await Audio.Sound.createAsync({ uri: fullAudioUrl });
        setSoundObject(sound);
        setIsPlayingAudio(true);
        await sound.playAsync();
      }
    } catch (e) {
      console.warn("Audio replay error:", e);
    }
  };

  const handleSendAction = async (actionText: string, modality: "VOICE" | "TEXT" = "TEXT") => {
    if (!activeSession || loadingAction) return;
    setLoadingAction(true);

    try {
      const nextState = await performAction(activeSession.session_id, actionText, modality);
      setActiveSession(nextState);

      if (nextState.is_completed) {
        addCompletedSession(nextState);
      }
    } catch (e) {
      console.error("Failed to perform action:", e);
    } finally {
      setLoadingAction(false);
    }
  };

  if (!activeSession) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#8B5CF6" />
      </View>
    );
  }

  const currentScene = activeSession.current_scene;
  const activeChar = currentScene.active_character;
  const domainTheme = Colors.domains[activeSession.story_id as keyof typeof Colors.domains] || Colors.domains.mystery;

  return (
    <SafeAreaView style={styles.container} edges={["top"]}>
      {/* Top Header Bar */}
      <View style={styles.topBar}>
        <TouchableOpacity style={styles.iconBtn} onPress={() => router.replace("/")} activeOpacity={0.7}>
          <ArrowLeft size={18} color="#FFF" />
        </TouchableOpacity>

        <View style={styles.locationBadge}>
          <MapPin size={12} color="#A78BFA" />
          <Text style={styles.locationText} numberOfLines={1}>
            {currentScene.title}
          </Text>
        </View>

        <TouchableOpacity
          style={styles.clueBtn}
          onPress={() => setClueDrawerVisible(true)}
          activeOpacity={0.7}
        >
          <Search size={14} color="#F59E0B" />
          <Text style={styles.clueBtnText}>Clues ({activeSession.discovered_clues.length})</Text>
        </TouchableOpacity>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Cinematic Scene Card */}
        <View style={[styles.cinematicCanvas, { backgroundColor: domainTheme.gradientStart }]}>
          <View style={styles.sceneAtmosphere}>
            <Text style={styles.sceneTitleUpper}>{currentScene.title.toUpperCase()}</Text>
            <Text style={styles.sceneDomainTag}>{domainTheme.name}</Text>
          </View>
        </View>

        {/* Character Dialogue Presentation */}
        <View style={styles.dialogueContainer}>
          <View style={styles.charHeader}>
            <View style={[styles.avatarBadge, isPlayingAudio && styles.avatarSpeaking]}>
              <Text style={styles.avatarInitial}>{activeChar.name.charAt(0)}</Text>
            </View>
            <View style={styles.charNameCol}>
              <Text style={styles.charName}>{activeChar.name}</Text>
              <Text style={styles.charStatus}>
                {isPlayingAudio ? "Speaking via Gnani Timbre..." : "Awaiting your response"}
              </Text>
            </View>
            {currentScene.audio_url && (
              <TouchableOpacity style={styles.audioReplayBtn} onPress={handleReplayAudio} activeOpacity={0.7}>
                <Volume2 size={16} color={isPlayingAudio ? "#8B5CF6" : Colors.textSecondary} />
              </TouchableOpacity>
            )}
          </View>

          {/* Dialogue Speech Card */}
          <View style={styles.speechBubble}>
            <Text style={styles.speechText}>{currentScene.dialogue}</Text>
          </View>
        </View>

        {/* Newly Unlocked Clue Banner */}
        {activeSession.newly_unlocked_clue && (
          <View style={styles.newClueBanner}>
            <Sparkles size={16} color="#10B981" />
            <View style={styles.newClueTextGroup}>
              <Text style={styles.newClueLabel}>NEW EVIDENCE DISCOVERED</Text>
              <Text style={styles.newClueTitle}>{activeSession.newly_unlocked_clue.title}</Text>
            </View>
          </View>
        )}

        {/* Suggested Actions Section */}
        <View style={styles.actionsSection}>
          <Text style={styles.actionsHeading}>Suggested Choices</Text>
          {currentScene.suggested_actions.map((act, index) => (
            <TouchableOpacity
              key={index}
              style={styles.actionChip}
              onPress={() => handleSendAction(act, "TOUCH_TAP")}
              disabled={loadingAction}
              activeOpacity={0.75}
            >
              <Text style={styles.actionChipText}>"{act}"</Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>

      {/* Voice & Keyboard Controller */}
      <VoiceController onSendAction={handleSendAction} isLoading={loadingAction} />

      {/* Clue Dossier Drawer */}
      <ClueDrawer
        visible={clueDrawerVisible}
        clues={activeSession.discovered_clues}
        onClose={() => setClueDrawerVisible(false)}
      />

      {/* Story Resolution Modal */}
      <EndingModal
        visible={activeSession.is_completed}
        title={activeSession.ending_title || null}
        epilogue={activeSession.ending_epilogue || null}
        cluesCount={activeSession.discovered_clues.length}
        onRestart={() => {
          setActiveSession(null);
          router.replace("/");
        }}
        onHome={() => {
          router.replace("/");
        }}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: Colors.background,
  },
  topBar: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
    backgroundColor: Colors.surface1,
  },
  iconBtn: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: Colors.surface2,
    alignItems: "center",
    justifyContent: "center",
  },
  locationBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    maxWidth: "50%",
  },
  locationText: {
    fontSize: 13,
    fontWeight: "700",
    color: Colors.textPrimary,
  },
  clueBtn: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    backgroundColor: "rgba(245, 158, 11, 0.15)",
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#F59E0B",
  },
  clueBtnText: {
    fontSize: 12,
    fontWeight: "700",
    color: "#F59E0B",
  },
  scrollContent: {
    paddingBottom: 20,
  },
  cinematicCanvas: {
    height: 140,
    marginHorizontal: 16,
    marginTop: 12,
    borderRadius: 18,
    borderWidth: 1,
    borderColor: Colors.border,
    justifyContent: "flex-end",
    padding: 16,
  },
  sceneAtmosphere: {},
  sceneTitleUpper: {
    fontSize: 16,
    fontWeight: "800",
    color: "#FFF",
    letterSpacing: 0.5,
  },
  sceneDomainTag: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  dialogueContainer: {
    paddingHorizontal: 16,
    marginTop: 16,
  },
  charHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 10,
  },
  avatarBadge: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: "#1E1B4B",
    borderWidth: 2,
    borderColor: "#8B5CF6",
    alignItems: "center",
    justifyContent: "center",
    marginRight: 10,
  },
  avatarSpeaking: {
    borderColor: "#10B981",
    transform: [{ scale: 1.05 }],
  },
  avatarInitial: {
    color: "#FFF",
    fontSize: 18,
    fontWeight: "700",
  },
  charNameCol: {
    flex: 1,
  },
  charName: {
    fontSize: 15,
    fontWeight: "700",
    color: Colors.textPrimary,
  },
  charStatus: {
    fontSize: 11,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  audioReplayBtn: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: Colors.surface2,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
    borderColor: Colors.border,
  },
  speechBubble: {
    backgroundColor: Colors.surface1,
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    borderLeftWidth: 4,
    borderLeftColor: "#8B5CF6",
  },
  speechText: {
    fontSize: 15,
    color: Colors.textPrimary,
    lineHeight: 23,
    fontWeight: "400",
  },
  newClueBanner: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(16, 185, 129, 0.12)",
    marginHorizontal: 16,
    marginTop: 14,
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#10B981",
    gap: 10,
  },
  newClueTextGroup: {
    flex: 1,
  },
  newClueLabel: {
    fontSize: 10,
    fontWeight: "700",
    color: "#10B981",
    letterSpacing: 0.8,
  },
  newClueTitle: {
    fontSize: 13,
    fontWeight: "700",
    color: Colors.textPrimary,
    marginTop: 2,
  },
  actionsSection: {
    paddingHorizontal: 16,
    marginTop: 18,
  },
  actionsHeading: {
    fontSize: 12,
    fontWeight: "700",
    color: Colors.textSecondary,
    textTransform: "uppercase",
    letterSpacing: 0.8,
    marginBottom: 8,
  },
  actionChip: {
    backgroundColor: Colors.surface1,
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: Colors.border,
    marginBottom: 8,
  },
  actionChipText: {
    fontSize: 14,
    color: Colors.textPrimary,
    fontWeight: "500",
  },
});
