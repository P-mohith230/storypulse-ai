import React from "react";
import { View, Text, TouchableOpacity, ScrollView, StyleSheet } from "react-native";
import { Colors } from "../theme/colors";
import { Clock, Smile } from "lucide-react-native";

interface FilterProps {
  selectedDuration: number | null;
  onSelectDuration: (dur: number | null) => void;
  selectedMood: string | null;
  onSelectMood: (mood: string | null) => void;
}

const DURATIONS = [2, 5, 10, 15];
const MOODS = [
  { label: "Curious", icon: "🔍" },
  { label: "Excited", icon: "⚡" },
  { label: "Relaxed", icon: "☕" },
  { label: "Bored", icon: "🎭" },
  { label: "Playful", icon: "✨" },
];

export const MoodDurationFilter: React.FC<FilterProps> = ({
  selectedDuration,
  onSelectDuration,
  selectedMood,
  onSelectMood,
}) => {
  return (
    <View style={styles.container}>
      {/* Duration selector */}
      <View style={styles.sectionHeader}>
        <Clock size={14} color={Colors.textSecondary} />
        <Text style={styles.sectionTitle}>Available Time</Text>
      </View>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chipRow}>
        {DURATIONS.map((dur) => {
          const isSelected = selectedDuration === dur;
          return (
            <TouchableOpacity
              key={dur}
              style={[styles.chip, isSelected && styles.chipActive]}
              onPress={() => onSelectDuration(isSelected ? null : dur)}
              activeOpacity={0.7}
            >
              <Text style={[styles.chipText, isSelected && styles.chipTextActive]}>{dur} min</Text>
            </TouchableOpacity>
          );
        })}
      </ScrollView>

      {/* Mood selector */}
      <View style={[styles.sectionHeader, { marginTop: 14 }]}>
        <Smile size={14} color={Colors.textSecondary} />
        <Text style={styles.sectionTitle}>Current Mood</Text>
      </View>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chipRow}>
        {MOODS.map((m) => {
          const isSelected = selectedMood === m.label;
          return (
            <TouchableOpacity
              key={m.label}
              style={[styles.chip, isSelected && styles.chipActiveMood]}
              onPress={() => onSelectMood(isSelected ? null : m.label)}
              activeOpacity={0.7}
            >
              <Text style={styles.moodEmoji}>{m.icon}</Text>
              <Text style={[styles.chipText, isSelected && styles.chipTextActive]}>{m.label}</Text>
            </TouchableOpacity>
          );
        })}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 20,
    marginBottom: 16,
  },
  sectionHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    marginBottom: 8,
  },
  sectionTitle: {
    fontSize: 12,
    fontWeight: "600",
    color: Colors.textSecondary,
    textTransform: "uppercase",
    letterSpacing: 0.8,
  },
  chipRow: {
    gap: 8,
    paddingRight: 10,
  },
  chip: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: Colors.surface1,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  chipActive: {
    backgroundColor: "#1E1B4B",
    borderColor: "#8B5CF6",
  },
  chipActiveMood: {
    backgroundColor: "#2E1065",
    borderColor: "#A78BFA",
  },
  moodEmoji: {
    marginRight: 6,
    fontSize: 13,
  },
  chipText: {
    fontSize: 13,
    color: Colors.textSecondary,
    fontWeight: "500",
  },
  chipTextActive: {
    color: Colors.textPrimary,
    fontWeight: "600",
  },
});
