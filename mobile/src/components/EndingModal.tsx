import React from "react";
import { View, Text, Modal, TouchableOpacity, StyleSheet } from "react-native";
import { Colors } from "../theme/colors";
import { Sparkles, RotateCcw, Home } from "lucide-react-native";

interface EndingModalProps {
  visible: boolean;
  title: string | null;
  epilogue: string | null;
  cluesCount: number;
  onRestart: () => void;
  onHome: () => void;
}

export const EndingModal: React.FC<EndingModalProps> = ({
  visible,
  title,
  epilogue,
  cluesCount,
  onRestart,
  onHome,
}) => {
  return (
    <Modal visible={visible} animationType="fade" transparent={true}>
      <View style={styles.backdrop}>
        <View style={styles.card}>
          <View style={styles.badge}>
            <Sparkles size={24} color="#F59E0B" />
          </View>

          <Text style={styles.chapterOver}>STORY COMPLETED</Text>
          <Text style={styles.title}>{title || "A Resolution Reached"}</Text>

          <Text style={styles.epilogue}>{epilogue || "Your decisions have concluded this chapter of StoryPulse."}</Text>

          <View style={styles.statsBox}>
            <Text style={styles.statLabel}>CLUES UNLOCKED</Text>
            <Text style={styles.statValue}>{cluesCount} Found</Text>
          </View>

          <View style={styles.buttonRow}>
            <TouchableOpacity style={styles.secondaryButton} onPress={onRestart} activeOpacity={0.8}>
              <RotateCcw size={16} color={Colors.textSecondary} />
              <Text style={styles.secondaryText}>Play Again</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.primaryButton} onPress={onHome} activeOpacity={0.8}>
              <Home size={16} color="#FFF" />
              <Text style={styles.primaryText}>Return Home</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.85)",
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },
  card: {
    backgroundColor: Colors.surface1,
    borderRadius: 24,
    padding: 24,
    width: "100%",
    maxWidth: 400,
    borderWidth: 1.5,
    borderColor: "#8B5CF6",
    alignItems: "center",
  },
  badge: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: "#2E1065",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 16,
    borderWidth: 1,
    borderColor: "#A78BFA",
  },
  chapterOver: {
    fontSize: 12,
    fontWeight: "700",
    color: "#A78BFA",
    letterSpacing: 1.5,
    marginBottom: 6,
  },
  title: {
    fontSize: 22,
    fontWeight: "700",
    color: Colors.textPrimary,
    textAlign: "center",
    marginBottom: 14,
  },
  epilogue: {
    fontSize: 15,
    color: Colors.textSecondary,
    lineHeight: 22,
    textAlign: "center",
    marginBottom: 20,
  },
  statsBox: {
    backgroundColor: Colors.surface2,
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 12,
    alignItems: "center",
    marginBottom: 24,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  statLabel: {
    fontSize: 10,
    color: Colors.textMuted,
    fontWeight: "600",
    letterSpacing: 0.8,
  },
  statValue: {
    fontSize: 16,
    fontWeight: "700",
    color: "#10B981",
    marginTop: 2,
  },
  buttonRow: {
    flexDirection: "row",
    gap: 12,
    width: "100%",
  },
  secondaryButton: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 6,
    paddingVertical: 12,
    borderRadius: 14,
    backgroundColor: Colors.surface2,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  secondaryText: {
    color: Colors.textSecondary,
    fontWeight: "600",
    fontSize: 14,
  },
  primaryButton: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 6,
    paddingVertical: 12,
    borderRadius: 14,
    backgroundColor: "#8B5CF6",
  },
  primaryText: {
    color: "#FFF",
    fontWeight: "700",
    fontSize: 14,
  },
});
