import React from "react";
import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { StoryProvider } from "../src/store/StoryContext";
import { Colors } from "../src/theme/colors";

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <StoryProvider>
        <StatusBar style="light" backgroundColor={Colors.background} />
        <Stack
          screenOptions={{
            headerShown: false,
            contentStyle: { backgroundColor: Colors.background },
          }}
        >
          <Stack.Screen name="(tabs)" />
          <Stack.Screen name="story/[storyId]" options={{ presentation: "modal" }} />
          <Stack.Screen name="story/play" options={{ gestureEnabled: false }} />
        </Stack>
      </StoryProvider>
    </SafeAreaProvider>
  );
}
