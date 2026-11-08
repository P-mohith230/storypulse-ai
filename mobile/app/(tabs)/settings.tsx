import React from "react";
import { View, Text, TouchableOpacity, Switch, StyleSheet, ScrollView } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Colors } from "../../src/theme/colors";
import { useStory } from "../../src/store/StoryContext";
import { Mic, Volume2, Globe, Shield, Info } from "lucide-react-native";

export default function SettingsScreen() {
  const { preferences, setPreferences } = useStory();

  const toggleTts = () => {
    setPreferences((prev) => ({
      ...prev,
      audio_mode: prev.audio_mode === "auto_tts" ? "text_only" : "auto_tts",
    }));
  };

  const toggleSubtitles = () => {
    setPreferences((prev) => ({
      ...prev,
      subtitles_enabled: !prev.subtitles_enabled,
    }));
  };

  const toggleHaptics = () => {
    setPreferences((prev) => ({
      ...prev,
      haptic_enabled: !prev.haptic_enabled,
    }));
  };

  const selectLang = (lang: string) => {
    setPreferences((prev) => ({
      ...prev,
      preferred_lang: lang,
    }));
  };

  return (
    <SafeAreaView style={styles.container} edges={["top"]}>
      <ScrollView contentContainerStyle={styles.content}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>Preferences</Text>
          <Text style={styles.subtitle}>Configure voice speech, subtitles, and Indic language support.</Text>
        </View>

        {/* Audio Engine (Gnani AI) Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Gnani AI Audio Engine</Text>

          <View style={styles.settingItem}>
            <View style={styles.settingTextGroup}>
              <View style={styles.settingIconRow}>
                <Volume2 size={18} color="#8B5CF6" />
                <Text style={styles.settingLabel}>Character Speech (Timbre TTS)</Text>
              </View>
              <Text style={styles.settingDesc}>Play dynamic character voice notes automatically</Text>
            </View>
            <Switch
              value={preferences.audio_mode === "auto_tts"}
              onValueChange={toggleTts}
              trackColor={{ false: Colors.surface2, true: "#8B5CF6" }}
              thumbColor="#FFF"
            />
          </View>

          <View style={styles.settingItem}>
            <View style={styles.settingTextGroup}>
              <View style={styles.settingIconRow}>
                <Mic size={18} color="#10B981" />
                <Text style={styles.settingLabel}>Always Show Subtitles</Text>
              </View>
              <Text style={styles.settingDesc}>Render typed captions alongside speech audio</Text>
            </View>
            <Switch
              value={preferences.subtitles_enabled}
              onValueChange={toggleSubtitles}
              trackColor={{ false: Colors.surface2, true: "#10B981" }}
              thumbColor="#FFF"
            />
          </View>

          <View style={styles.settingItem}>
            <View style={styles.settingTextGroup}>
              <View style={styles.settingIconRow}>
                <Shield size={18} color="#F59E0B" />
                <Text style={styles.settingLabel}>Haptic Feedback</Text>
              </View>
              <Text style={styles.settingDesc}>Tactile vibration on recording and clue discovery</Text>
            </View>
            <Switch
              value={preferences.haptic_enabled}
              onValueChange={toggleHaptics}
              trackColor={{ false: Colors.surface2, true: "#F59E0B" }}
              thumbColor="#FFF"
            />
          </View>
        </View>

        {/* Language Selection Section */}
        <View style={styles.section}>
          <View style={styles.settingIconRow}>
            <Globe size={18} color="#06B6D4" />
            <Text style={styles.sectionTitle}>Speech Language</Text>
          </View>

          <View style={styles.langSelector}>
            {[
              { code: "en-IN", name: "Indian English (Primary)" },
              { code: "te-IN", name: "Telugu (తెలుగు)" },
              { code: "hi-IN", name: "Hindi (हिंदी)" },
            ].map((lang) => {
              const isSelected = preferences.preferred_lang === lang.code;
              return (
                <TouchableOpacity
                  key={lang.code}
                  style={[styles.langItem, isSelected && styles.langItemActive]}
                  onPress={() => selectLang(lang.code)}
                >
                  <Text style={[styles.langName, isSelected && styles.langNameActive]}>{lang.name}</Text>
                  {isSelected && <View style={styles.radioDot} />}
                </TouchableOpacity>
              );
            })}
          </View>
        </View>

        {/* System & Architecture Info */}
        <View style={styles.infoCard}>
          <View style={styles.infoRow}>
            <Info size={16} color={Colors.textSecondary} />
            <Text style={styles.infoTitle}>About StoryPulse AI</Text>
          </View>
          <Text style={styles.infoText}>
            Dual-Engine Interactive Fiction powered by Gnani AI Prisma v3.0 (STT) and Timbre v2.5 (TTS).
            Version 1.0.0 — Build 2026.11
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  header: {
    marginBottom: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
    color: Colors.textPrimary,
  },
  subtitle: {
    fontSize: 14,
    color: Colors.textSecondary,
    marginTop: 4,
  },
  section: {
    marginBottom: 28,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: "700",
    color: Colors.textSecondary,
    textTransform: "uppercase",
    letterSpacing: 0.8,
    marginBottom: 12,
  },
  settingItem: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    backgroundColor: Colors.surface1,
    padding: 16,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    marginBottom: 10,
  },
  settingTextGroup: {
    flex: 1,
    paddingRight: 12,
  },
  settingIconRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 4,
  },
  settingLabel: {
    fontSize: 15,
    fontWeight: "600",
    color: Colors.textPrimary,
  },
  settingDesc: {
    fontSize: 12,
    color: Colors.textMuted,
  },
  langSelector: {
    backgroundColor: Colors.surface1,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    overflow: "hidden",
  },
  langItem: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  langItemActive: {
    backgroundColor: "rgba(139, 92, 246, 0.12)",
  },
  langName: {
    fontSize: 15,
    color: Colors.textSecondary,
    fontWeight: "500",
  },
  langNameActive: {
    color: "#A78BFA",
    fontWeight: "700",
  },
  radioDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: "#8B5CF6",
  },
  infoCard: {
    backgroundColor: Colors.surface1,
    padding: 18,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    marginTop: 10,
  },
  infoRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    marginBottom: 8,
  },
  infoTitle: {
    fontSize: 14,
    fontWeight: "700",
    color: Colors.textPrimary,
  },
  infoText: {
    fontSize: 12,
    color: Colors.textSecondary,
    lineHeight: 18,
  },
});
