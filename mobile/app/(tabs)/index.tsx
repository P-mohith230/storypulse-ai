import React, { useState, useEffect } from "react";
import { View, Text, ScrollView, RefreshControl, StyleSheet, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useRouter } from "expo-router";
import { Colors } from "../../src/theme/colors";
import { Header } from "../../src/components/Header";
import { MoodDurationFilter } from "../../src/components/MoodDurationFilter";
import { CategoryCard } from "../../src/components/CategoryCard";
import { fetchStories } from "../../src/api/client";
import { StoryCatalogItem } from "../../src/types";
import { useStory } from "../../src/store/StoryContext";
import { Play, Sparkles } from "lucide-react-native";

export default function HomeScreen() {
  const router = useRouter();
  const { activeSession } = useStory();
  const [stories, setStories] = useState<StoryCatalogItem[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedDuration, setSelectedDuration] = useState<number | null>(null);
  const [selectedMood, setSelectedMood] = useState<string | null>(null);

  const loadStories = async () => {
    const list = await fetchStories(selectedDuration || undefined, selectedMood || undefined);
    if (list && list.length > 0) {
      setStories(list);
    }
  };

  useEffect(() => {
    loadStories();
  }, [selectedDuration, selectedMood]);

  const onRefresh = async () => {
    setRefreshing(true);
    await loadStories();
    setRefreshing(false);
  };

  const handleOpenStory = (storyId: string) => {
    router.push(`/story/${storyId}`);
  };

  const handleResumeStory = () => {
    router.push("/story/play");
  };

  return (
    <SafeAreaView style={styles.container} edges={["top"]}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#8B5CF6" />}
      >
        <Header />

        {/* Active Session Resume Banner */}
        {activeSession && !activeSession.is_completed && (
          <TouchableOpacity style={styles.resumeCard} onPress={handleResumeStory} activeOpacity={0.85}>
            <View style={styles.resumeInfo}>
              <View style={styles.resumeTag}>
                <Sparkles size={12} color="#10B981" />
                <Text style={styles.resumeTagText}>IN PROGRESS</Text>
              </View>
              <Text style={styles.resumeTitle}>{activeSession.current_scene.title}</Text>
              <Text style={styles.resumeSub}>Tap to jump back into your story</Text>
            </View>
            <View style={styles.resumePlayBtn}>
              <Play size={18} color="#FFF" />
            </View>
          </TouchableOpacity>
        )}

        {/* Interactive Mood & Duration Filter */}
        <MoodDurationFilter
          selectedDuration={selectedDuration}
          onSelectDuration={setSelectedDuration}
          selectedMood={selectedMood}
          onSelectMood={setSelectedMood}
        />

        {/* Story Categories Section Header */}
        <View style={styles.sectionHeading}>
          <Text style={styles.sectionHeadingTitle}>Story Worlds</Text>
          <Text style={styles.sectionHeadingCount}>({stories.length} Domains)</Text>
        </View>

        {/* Five Category Cards */}
        {stories.map((story) => (
          <CategoryCard key={story.id} story={story} onPress={() => handleOpenStory(story.id)} />
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  scrollContent: {
    paddingBottom: 32,
  },
  resumeCard: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    backgroundColor: "#064E3B",
    marginHorizontal: 20,
    marginBottom: 16,
    padding: 16,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#10B981",
  },
  resumeInfo: {
    flex: 1,
  },
  resumeTag: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    marginBottom: 4,
  },
  resumeTagText: {
    fontSize: 10,
    fontWeight: "700",
    color: "#34D399",
    letterSpacing: 0.8,
  },
  resumeTitle: {
    fontSize: 16,
    fontWeight: "700",
    color: "#FFF",
  },
  resumeSub: {
    fontSize: 12,
    color: "#A7F3D0",
    marginTop: 2,
  },
  resumePlayBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "#10B981",
    alignItems: "center",
    justifyContent: "center",
    marginLeft: 12,
  },
  sectionHeading: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 20,
    marginBottom: 12,
    gap: 6,
  },
  sectionHeadingTitle: {
    fontSize: 16,
    fontWeight: "700",
    color: Colors.textPrimary,
  },
  sectionHeadingCount: {
    fontSize: 13,
    color: Colors.textMuted,
  },
});

