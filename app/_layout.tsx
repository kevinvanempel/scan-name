import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../src/constants/colors';
import { useHydrateApp } from '../src/hooks/useHydrateApp';
import { useSettingsStore } from '../src/store/settingsStore';
import { t } from '../src/i18n';

export default function RootLayout() {
  useHydrateApp();
  const language = useSettingsStore((s) => s.language);

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: { backgroundColor: colors.tab, borderTopColor: '#204C7A', height: 72, paddingBottom: 8 },
        tabBarActiveTintColor: colors.accent,
        tabBarInactiveTintColor: colors.textSoft
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: t(language, 'home'),
          tabBarIcon: ({ color, size }) => <Ionicons name="home-outline" color={color} size={size} />
        }}
      />
      <Tabs.Screen
        name="scan"
        options={{
          title: t(language, 'scan'),
          tabBarIcon: ({ color, size }) => <Ionicons name="add" color={color} size={size} />
        }}
      />
      <Tabs.Screen
        name="folders"
        options={{
          title: t(language, 'folders'),
          tabBarIcon: ({ color, size }) => <Ionicons name="folder-open-outline" color={color} size={size} />
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: t(language, 'settings'),
          tabBarIcon: ({ color, size }) => <Ionicons name="settings-outline" color={color} size={size} />
        }}
      />
      <Tabs.Screen name="detail/[id]" options={{ href: null }} />
      <Tabs.Screen name="modal/paywall" options={{ href: null }} />
    </Tabs>
  );
}
