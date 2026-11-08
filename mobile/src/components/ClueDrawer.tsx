import React from "react";
import { View, Text, Modal, TouchableOpacity, ScrollView, StyleSheet } from "react-native";
import { Colors } from "../theme/colors";
import { ClueItem } from "../types";
import { X, Search, ShieldCheck } from "lucide-react-native";

interface ClueDrawerProps {
  visible: boolean;
  clues: ClueItem[];
  onClose: () => void;
}

export const ClueDrawer: React.FC<ClueDrawerProps> = ({ visible, clues, onClose }) => {
  return (
    <Modal visible={visible} animationType="slide" transparent={true} onRequestClose={onClose}>
      <View style={styles.backdrop}>
        <View style={styles.sheetContainer}>
          {/* Header */}
          <View style={styles.header}>
            <View style={styles.headerLeft}>
              <Search size={18} color="#F59E0B" />
              <Text style={styles.headerTitle}>Case Clue Dossier ({clues.length})</Text>
            </View>
            <TouchableOpacity onPress={onClose} style={styles.closeButton}>
              <X size={20} color={Colors.textSecondary} />
            </TouchableOpacity>
          </View>

          {/* Clues List */}
          <ScrollView contentContainerStyle={styles.listContent}>
            {clues.length === 0 ? (
              <View style={styles.emptyContainer}>
                <Text style={styles.emptyText}>No clues discovered yet. Search the environment and question characters!</Text>
              </View>
            ) : (
              clues.map((clue, idx) => (
                <View key={clue.id || idx} style={styles.clueCard}>
                  <View style={styles.iconBadge}>
                    <ShieldCheck size={20} color="#10B981" />
                  </View>
                  <View style={styles.clueDetails}>
                    <Text style={styles.clueTitle}>{clue.title}</Text>
                    <Text style={styles.clueDesc}>{clue.description}</Text>
                  </View>
                </View>
              ))
            )}
          </ScrollView>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.75)",
    justifyContent: "flex-end",
  },
  sheetContainer: {
    backgroundColor: Colors.surface1,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    maxHeight: "75%",
    borderWidth: 1,
    borderColor: Colors.border,
    paddingBottom: 32,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  headerLeft: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  headerTitle: {
    fontSize: 16,
    fontWeight: "700",
    color: Colors.textPrimary,
  },
  closeButton: {
    padding: 6,
  },
  listContent: {
    padding: 20,
    gap: 12,
  },
  clueCard: {
    flexDirection: "row",
    alignItems: "flex-start",
    backgroundColor: Colors.surface2,
    padding: 14,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: Colors.border,
    gap: 12,
  },
  iconBadge: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: "rgba(16, 185, 129, 0.15)",
    alignItems: "center",
    justifyContent: "center",
  },
  clueDetails: {
    flex: 1,
  },
  clueTitle: {
    fontSize: 15,
    fontWeight: "700",
    color: Colors.textPrimary,
    marginBottom: 4,
  },
  clueDesc: {
    fontSize: 13,
    color: Colors.textSecondary,
    lineHeight: 18,
  },
  emptyContainer: {
    padding: 30,
    alignItems: "center",
  },
  emptyText: {
    color: Colors.textMuted,
    fontSize: 14,
    textAlign: "center",
  },
});
