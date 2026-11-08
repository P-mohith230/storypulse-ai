import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { Colors } from "../theme/colors";
import { StoryCatalogItem } from "../types";
import { ChevronRight, Sparkles } from "lucide-react-native";

interface CategoryCardProps {
  story: StoryCatalogItem;
  onPress: () => void;
}

export const CategoryCard: React.FC<CategoryCardProps> = ({ story, onPress }) => {
  const domainTheme = Colors.domains[story.domain] || Colors.domains.mystery;

  return (
    <TouchableOpacity
      style={[styles.card, { borderColor: domainTheme.primary }]}
      onPress={onPress}
      activeOpacity={0.82}
    >
      <View style={[styles.gradientOverlay, { backgroundColor: domainTheme.gradientStart }]}>
        {/* Top Badges */}
        <View style={styles.topRow}>
          <View style={[styles.domainBadge, { backgroundColor: domainTheme.primary }]}>
            <Text style={styles.domainText}>{domainTheme.name}</Text>
          </View>
          <View style={styles.metaBadge}>
            <Text style={styles.metaText}>{story.duration_min} min</Text>
          </View>
        </View>

        {/* Featured Star */}
        {story.featured && (
          <View style={styles.featuredBadge}>
            <Sparkles size={12} color="#F59E0B" />
            <Text style={styles.featuredText}>Flagship Story</Text>
          </View>
        )}

        {/* Title and Tagline */}
        <View style={styles.content}>
          <Text style={styles.title}>{story.title}</Text>
          <Text style={styles.tagline} numberOfLines={2}>
            {story.tagline}
          </Text>
        </View>

        {/* Bottom Bar */}
        <View style={styles.bottomRow}>
          <View style={styles.statsRow}>
            <Text style={styles.statsText}>{story.clue_count} Clues</Text>
            <Text style={styles.statsDot}>•</Text>
            <Text style={styles.statsText}>{story.character_count} Characters</Text>
          </View>
          <View style={[styles.enterButton, { backgroundColor: domainTheme.primary }]}>
            <Text style={styles.enterText}>Enter</Text>
            <ChevronRight size={14} color="#FFF" />
          </View>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    borderRadius: 20,
    marginHorizontal: 20,
    marginBottom: 16,
    overflow: "hidden",
    borderWidth: 1.5,
    backgroundColor: Colors.surface1,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.35,
    shadowRadius: 10,
    elevation: 6,
  },
  gradientOverlay: {
    padding: 18,
    minHeight: 180,
    justifyContent: "space-between",
  },
  topRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  domainBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  domainText: {
    color: "#FFF",
    fontSize: 11,
    fontWeight: "700",
    textTransform: "uppercase",
  },
  metaBadge: {
    backgroundColor: "rgba(255, 255, 255, 0.12)",
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 10,
  },
  metaText: {
    color: Colors.textSecondary,
    fontSize: 11,
    fontWeight: "600",
  },
  featuredBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    marginTop: 6,
  },
  featuredText: {
    color: "#F59E0B",
    fontSize: 11,
    fontWeight: "700",
  },
  content: {
    marginVertical: 12,
  },
  title: {
    fontSize: 20,
    fontWeight: "700",
    color: Colors.textPrimary,
    marginBottom: 6,
  },
  tagline: {
    fontSize: 14,
    color: Colors.textSecondary,
    lineHeight: 20,
  },
  bottomRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: 4,
  },
  statsRow: {
    flexDirection: "row",
    alignItems: "center",
  },
  statsText: {
    fontSize: 12,
    color: Colors.textMuted,
  },
  statsDot: {
    fontSize: 12,
    color: Colors.textMuted,
    marginHorizontal: 6,
  },
  enterButton: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 14,
    gap: 2,
  },
  enterText: {
    color: "#FFF",
    fontSize: 12,
    fontWeight: "700",
  },
});
