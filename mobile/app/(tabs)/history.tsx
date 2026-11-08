import React from "react";
import { View, Text, ScrollView, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Colors } from "../../src/theme/colors";
import { useStory } from "../../src/store/StoryContext";
import { BookOpen, Award, ShieldCheck } from "lucide-react-native";

export default function HistoryScreen() {
  const { completedSessions, discoveredClues } = useStory();

  return (
    <SafeAreaView style={styles.container} edges={["top"]}>
      <ScrollView contentContainerStyle={styles.content}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>Investigative Dossier</Text>
          <Text style={styles.subtitle}>Your accumulated clues and completed narrative endings.</Text>
        </View>

        {/* Stats Row */}
        <View style={styles.statsRow}>
          <View style={styles.statBox}>
            <Award size={20} color="#F59E0B" />
            <Text style={styles.statNumber}>{completedSessions.length}</Text>
            <Text style={styles.statLabel}>Stories Finished</Text>
          </View>
          <View style={styles.statBox}>
            <ShieldCheck size={20} color="#10B981" />
            <Text style={styles.statNumber}>{discoveredClues.length}</Text>
            <Text style={styles.statLabel}>Active Clues</Text>
          </View>
        </View>

        {/* Collected Clues Section */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Case Evidence Discovered</Text>
        </View>

        {discoveredClues.length === 0 ? (
          <View style={styles.emptyCard}>
            <BookOpen size={32} color={Colors.textMuted} />
            <Text style={styles.emptyTitle}>No Evidence On File</Text>
            <Text style={styles.emptyDesc}>Enter any story from the Discover tab to begin finding clues.</Text>
          </View>
        ) : (
          discoveredClues.map((clue) => (
            <View key={clue.id} style={styles.clueCard}>
              <View style={styles.clueBadge}>
                <ShieldCheck size={18} color="#10B981" />
              </View>
              <View style={styles.clueInfo}>
                <Text style={styles.clueTitle}>{clue.title}</Text>
                <Text style={styles.clueDesc}>{clue.description}</Text>
              </View>
            </View>
          ))
        )}

        {/* Completed Stories Section */}
        {completedSessions.length > 0 && (
          <>
            <View style={[styles.sectionHeader, { marginTop: 24 }]}>
              <Text style={styles.sectionTitle}>Archived Resolutions</Text>
            </View>
            {completedSessions.map((sess) => (
              <View key={sess.session_id} style={styles.completedCard}>
                <Text style={styles.completedTitle}>{sess.ending_title || "Story Concluded"}</Text>
                <Text style={styles.completedEpilogue}>{sess.ending_epilogue}</Text>
              </View>
            ))}
          </>
        )}
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
    marginBottom: 20,
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
  statsRow: {
    flexDirection: "row",
    gap: 12,
    marginBottom: 24,
  },
  statBox: {
    flex: 1,
    backgroundColor: Colors.surface1,
    padding: 16,
    borderRadius: 16,
    alignItems: "center",
    borderWidth: 1,
    borderColor: Colors.border,
  },
  statNumber: {
    fontSize: 22,
    fontWeight: "700",
    color: Colors.textPrimary,
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  sectionHeader: {
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: "700",
    color: Colors.textPrimary,
  },
  emptyCard: {
    backgroundColor: Colors.surface1,
    borderRadius: 16,
    padding: 32,
    alignItems: "center",
    borderWidth: 1,
    borderColor: Colors.border,
  },
  emptyTitle: {
    fontSize: 16,
    fontWeight: "700",
    color: Colors.textPrimary,
    marginTop: 12,
  },
  emptyDesc: {
    fontSize: 13,
    color: Colors.textSecondary,
    textAlign: "center",
    marginTop: 6,
    lineHeight: 18,
  },
  clueCard: {
    flexDirection: "row",
    backgroundColor: Colors.surface1,
    padding: 14,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: Colors.border,
    marginBottom: 10,
    gap: 12,
  },
  clueBadge: {
    width: 34,
    height: 34,
    borderRadius: 17,
    backgroundColor: "rgba(16, 185, 129, 0.15)",
    alignItems: "center",
    justifyContent: "center",
  },
  clueInfo: {
    flex: 1,
  },
  clueTitle: {
    fontSize: 15,
    fontWeight: "700",
    color: Colors.textPrimary,
    marginBottom: 3,
  },
  clueDesc: {
    fontSize: 13,
    color: Colors.textSecondary,
    lineHeight: 18,
  },
  completedCard: {
    backgroundColor: Colors.surface1,
    padding: 16,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#8B5CF6",
    marginBottom: 12,
  },
  completedTitle: {
    fontSize: 16,
    fontWeight: "700",
    color: "#A78BFA",
    marginBottom: 6,
  },
  completedEpilogue: {
    fontSize: 13,
    color: Colors.textSecondary,
    lineHeight: 19,
  },
});

