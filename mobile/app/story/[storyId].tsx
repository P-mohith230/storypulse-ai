import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Image, TouchableOpacity, ScrollView, ActivityIndicator } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Colors } from "../../src/theme/colors";
import { fetchStories, createSession } from "../../src/api/client";
import { StoryCatalogItem } from "../../src/types";
import { useStory } from "../../src/store/StoryContext";
import { ArrowLeft, Clock, Sparkles, Play, Users, Search } from "lucide-react-native";

export default function StoryPreviewScreen() {
  const router = useRouter();
  const { storyId } = useLocalSearchParams<{ storyId: string }>();
  const { setActiveSession, preferences } = useStory();
  const [story, setStory] = useState<StoryCatalogItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [entering, setEntering] = useState(false);

  useEffect(() => {
    fetchStories().then((list) => {
      const found = list.find((s) => s.id === storyId);
      if (found) setStory(found);
      setLoading(false);
    });
  }, [storyId]);

  const handleEnterStory = async () => {
    if (!story) return;
    setEntering(true);
    try {
      const session = await createSession(
        story.id,
        story.duration_min,
        story.moods[0] || "Curious",
        preferences.preferred_lang
      );
      setActiveSession(session);
      router.replace("/story/play");
    } catch (e) {
      console.error("Failed to start story session:", e);
      setEntering(false);
    }
  };

  if (loading || !story) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#8B5CF6" />
      </View>
    );
  }

  const domainTheme = Colors.domains[story.domain] || Colors.domains.mystery;

  return (
    <SafeAreaView style={styles.container} edges={["top", "bottom"]}>
      {/* Top Back Navigation */}
      <View style={styles.topNav}>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()} activeOpacity={0.7}>
          <ArrowLeft size={20} color="#FFF" />
        </TouchableOpacity>
        <Text style={styles.navTitle}>{domainTheme.name}</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        {/* Story Visual Banner */}
        <View style={[styles.coverContainer, { backgroundColor: domainTheme.gradientStart }]}>
          <View style={styles.coverInner}>
            <View style={[styles.domainPill, { backgroundColor: domainTheme.primary }]}>
              <Text style={styles.domainPillText}>{story.domain.toUpperCase()}</Text>
            </View>
            <Text style={styles.storyHeroTitle}>{story.title}</Text>
            <View style={styles.metaRow}>
              <View style={styles.metaItem}>
                <Clock size={14} color={Colors.textSecondary} />
                <Text style={styles.metaItemText}>{story.duration_min} minutes</Text>
              </View>
              <View style={styles.metaItem}>
                <Sparkles size={14} color="#F59E0B" />
                <Text style={styles.metaItemText}>{story.moods.join(" • ")}</Text>
              </View>
            </View>
          </View>
        </View>

        {/* Premise Section */}
        <View style={styles.section}>
          <Text style={styles.sectionHeading}>The Premise</Text>
          <Text style={styles.premiseText}>{story.tagline}</Text>
        </View>

        {/* Investigation Breakdown */}
        <View style={styles.statsCard}>
          <View style={styles.statCol}>
            <Search size={20} color="#10B981" />
            <Text style={styles.statVal}>{story.clue_count}</Text>
            <Text style={styles.statLbl}>Discoverable Clues</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statCol}>
            <Users size={20} color="#8B5CF6" />
            <Text style={styles.statVal}>{story.character_count}</Text>
            <Text style={styles.statLbl}>Characters to Meet</Text>
          </View>
        </View>

        {/* Experience Instructions */}
        <View style={styles.instructionBox}>
          <Text style={styles.instructionTitle}>How to Experience:</Text>
          <Text style={styles.instructionItem}>• Hold the microphone to converse with characters.</Text>
          <Text style={styles.instructionItem}>• Tap suggested action chips or type custom decisions.</Text>
          <Text style={styles.instructionItem}>• Discovered clues alter canonical scene outcomes.</Text>
        </View>
      </ScrollView>

      {/* Enter Story CTA */}
      <View style={styles.bottomBar}>
        <TouchableOpacity
          style={[styles.enterBtn, { backgroundColor: domainTheme.primary }]}
          onPress={handleEnterStory}
          disabled={entering}
          activeOpacity={0.85}
        >
          {entering ? (
            <ActivityIndicator size="small" color="#FFF" />
          ) : (
            <>
              <Play size={18} color="#FFF" fill="#FFF" />
              <Text style={styles.enterBtnText}>Begin Interactive Experience</Text>
            </>
          )}
        </TouchableOpacity>
      </View>
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
  topNav: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 20,
    paddingVertical: 12,
  },
  backBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: Colors.surface1,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
    borderColor: Colors.border,
  },
  navTitle: {
    fontSize: 14,
    fontWeight: "700",
    color: Colors.textSecondary,
    textTransform: "uppercase",
    letterSpacing: 0.8,
  },
  content: {
    paddingHorizontal: 20,
    paddingBottom: 24,
  },
  coverContainer: {
    borderRadius: 24,
    padding: 24,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: Colors.border,
    minHeight: 200,
    justifyContent: "flex-end",
  },
  coverInner: {},
  domainPill: {
    alignSelf: "flex-start",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 10,
    marginBottom: 10,
  },
  domainPillText: {
    color: "#FFF",
    fontSize: 10,
    fontWeight: "700",
    letterSpacing: 0.8,
  },
  storyHeroTitle: {
    fontSize: 26,
    fontWeight: "800",
    color: "#FFF",
    marginBottom: 10,
    lineHeight: 32,
  },
  metaRow: {
    flexDirection: "row",
    gap: 16,
  },
  metaItem: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
  },
  metaItemText: {
    color: Colors.textSecondary,
    fontSize: 13,
    fontWeight: "600",
  },
  section: {
    marginBottom: 20,
  },
  sectionHeading: {
    fontSize: 16,
    fontWeight: "700",
    color: Colors.textPrimary,
    marginBottom: 8,
  },
  premiseText: {
    fontSize: 15,
    color: Colors.textSecondary,
    lineHeight: 22,
  },
  statsCard: {
    flexDirection: "row",
    backgroundColor: Colors.surface1,
    padding: 16,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    marginBottom: 20,
  },
  statCol: {
    flex: 1,
    alignItems: "center",
  },
  statDivider: {
    width: 1,
    backgroundColor: Colors.border,
    marginVertical: 4,
  },
  statVal: {
    fontSize: 20,
    fontWeight: "700",
    color: Colors.textPrimary,
    marginTop: 6,
  },
  statLbl: {
    fontSize: 11,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  instructionBox: {
    backgroundColor: Colors.surface1,
    padding: 18,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  instructionTitle: {
    fontSize: 14,
    fontWeight: "700",
    color: "#A78BFA",
    marginBottom: 8,
  },
  instructionItem: {
    fontSize: 13,
    color: Colors.textSecondary,
    lineHeight: 20,
    marginBottom: 4,
  },
  bottomBar: {
    paddingHorizontal: 20,
    paddingVertical: 14,
    backgroundColor: Colors.surface1,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
  },
  enterBtn: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    paddingVertical: 14,
    borderRadius: 16,
  },
  enterBtnText: {
    color: "#FFF",
    fontSize: 16,
    fontWeight: "700",
  },
});

