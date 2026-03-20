from pathlib import Path

FILES = {
    "package.json": """{
  "name": "scan-name",
  "version": "1.0.0",
  "private": true,
  "main": "expo-router/entry",
  "scripts": {
    "start": "expo start",
    "android": "expo run:android",
    "ios": "expo run:ios",
    "web": "expo start --web"
  },
  "dependencies": {
    "@expo/vector-icons": "^14.1.0",
    "@react-native-async-storage/async-storage": "2.1.2",
    "expo": "~53.0.0",
    "expo-file-system": "~18.0.12",
    "expo-image-picker": "~16.0.6",
    "expo-localization": "~16.0.1",
    "expo-router": "~5.0.2",
    "expo-sqlite": "~15.1.2",
    "react": "19.0.0",
    "react-native": "0.79.2",
    "react-native-safe-area-context": "5.4.0",
    "zustand": "^5.0.3"
  },
  "devDependencies": {
    "@types/react": "~19.0.10",
    "typescript": "~5.8.3"
  }
}
""",
    "app.json": """{
  "expo": {
    "name": "Scan & Name",
    "slug": "scan-name",
    "scheme": "scanname",
    "orientation": "portrait",
    "userInterfaceStyle": "dark",
    "plugins": [
      "expo-router",
      [
        "expo-image-picker",
        {
          "photosPermission": "Scan & Name heeft toegang nodig tot je foto's om media te importeren.",
          "cameraPermission": "Scan & Name heeft toegang nodig tot je camera om media op te nemen."
        }
      ]
    ],
    "ios": {
      "supportsTablet": false,
      "bundleIdentifier": "com.kevinvanempel.scanname"
    },
    "android": {
      "package": "com.kevinvanempel.scanname"
    },
    "experiments": {
      "typedRoutes": true
    }
  }
}
""",
    "babel.config.js": """module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: ['expo-router/babel']
  };
};
""",
    "tsconfig.json": """{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": [
    "**/*.ts",
    "**/*.tsx",
    ".expo/types/**/*.ts",
    "expo-env.d.ts"
  ]
}
""",
    "README.md": """# Scan & Name MVP

## Wat zit erin
- React Native + Expo + TypeScript
- Expo Router tabs
- SQLite opslag
- media import
- mock AI herkenning
- automatische titel/map/tags/beschrijving
- zoeken
- mappenoverzicht
- instellingen
- freemium teller
- paywall scherm

## Gebruik van het script
Plaats dit script in een lege map en run:

```bash
python setup_scan_name.py
```

Daarna:

```bash
npm install
npx expo start -c
```
""",
    "app/_layout.tsx": """import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '@/src/constants/colors';
import { useHydrateApp } from '@/src/hooks/useHydrateApp';
import { useSettingsStore } from '@/src/store/settingsStore';
import { t } from '@/src/i18n';

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
""",
    "app/index.tsx": """import { useMemo, useState } from 'react';
import { StyleSheet, TextInput, View } from 'react-native';
import { router } from 'expo-router';
import { Screen } from '@/src/components/Screen';
import { AppHeader } from '@/src/components/AppHeader';
import { FileCard } from '@/src/components/FileCard';
import { FilterChips } from '@/src/components/FilterChips';
import { EmptyState } from '@/src/components/EmptyState';
import { colors } from '@/src/constants/colors';
import { useMediaStore } from '@/src/store/mediaStore';
import { useSettingsStore } from '@/src/store/settingsStore';
import { t } from '@/src/i18n';
import { filterMedia } from '@/src/utils/search';

export default function HomeScreen() {
  const items = useMediaStore((s) => s.items);
  const language = useSettingsStore((s) => s.language);
  const [query, setQuery] = useState('');
  const [selectedFolder, setSelectedFolder] = useState<string | null>(null);

  const folders = useMemo(() => ['Alles', ...new Set(items.map((x) => x.folder))], [items]);
  const filtered = useMemo(() => filterMedia(items, query, selectedFolder), [items, query, selectedFolder]);

  return (
    <Screen>
      <AppHeader title="Scan & Name" subtitle={`${items.length} bestanden • ${Math.max(new Set(items.map((x) => x.folder)).size, 0)} mappen`} />
      <TextInput
        value={query}
        onChangeText={setQuery}
        placeholder={t(language, 'searchPlaceholder')}
        placeholderTextColor={colors.textSoft}
        style={styles.input}
      />
      <FilterChips options={folders} selected={selectedFolder} onSelect={setSelectedFolder} />
      <View style={styles.grid}>
        {filtered.length ? filtered.map((item) => (
          <FileCard key={item.id} item={item} language={language} onPress={() => router.push(`/detail/${item.id}`)} />
        )) : <EmptyState title={t(language, 'noItems')} subtitle={t(language, 'noItemsSub')} />}
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  input: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    color: colors.text,
    borderRadius: 14,
    paddingHorizontal: 14,
    paddingVertical: 13,
    marginBottom: 8
  },
  grid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between' }
});
""",
    "app/scan.tsx": """import { useState } from 'react';
import { Alert, ActivityIndicator, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Screen } from '@/src/components/Screen';
import { AppHeader } from '@/src/components/AppHeader';
import { PrimaryButton } from '@/src/components/PrimaryButton';
import { SectionTitle } from '@/src/components/SectionTitle';
import { TagPill } from '@/src/components/TagPill';
import { colors } from '@/src/constants/colors';
import { t } from '@/src/i18n';
import { useSettingsStore } from '@/src/store/settingsStore';
import { useMediaStore } from '@/src/store/mediaStore';
import { pickMedia, persistImportedFile } from '@/src/services/mediaImport';
import { analyzeMedia } from '@/src/services/ai';
import { canProcessMore, getMonthlyUsage, incrementMonthlyUsage } from '@/src/services/quota';
import { MediaItem } from '@/src/types/media';

export default function ScanScreen() {
  const language = useSettingsStore((s) => s.language);
  const addItem = useMediaStore((s) => s.addItem);
  const items = useMediaStore((s) => s.items);
  const [loading, setLoading] = useState(false);
  const [usage, setUsage] = useState<number | null>(null);

  async function handlePick() {
    const allowed = await canProcessMore();
    const currentUsage = await getMonthlyUsage();
    setUsage(currentUsage);
    if (!allowed) {
      router.push('/modal/paywall');
      return;
    }
    try {
      setLoading(true);
      const asset = await pickMedia();
      if (!asset) return;

      const suggestion = await analyzeMedia(asset.fileName ?? 'bestand', asset.mimeType);
      const storedUri = await persistImportedFile(asset.uri, suggestion.title);
      const now = new Date().toISOString();

      const item: MediaItem = {
        id: `${Date.now()}`,
        originalUri: asset.uri,
        storedUri,
        kind: suggestion.kind,
        title: suggestion.title,
        description: suggestion.description,
        tags: suggestion.tags,
        folder: suggestion.folder,
        fileSize: asset.fileSize,
        mimeType: asset.mimeType ?? undefined,
        createdAt: now,
        updatedAt: now,
        aiRecognized: suggestion.aiRecognized
      };

      addItem(item);
      await incrementMonthlyUsage();
      router.push(`/detail/${item.id}`);
    } catch (error: any) {
      Alert.alert('Fout', error?.message ?? 'Import mislukt');
    } finally {
      setLoading(false);
      setUsage(await getMonthlyUsage());
    }
  }

  return (
    <Screen>
      <AppHeader title={t(language, 'scan')} subtitle="AI herkent inhoud automatisch" />
      <View style={styles.dropZone}>
        <Text style={styles.camera}>📷</Text>
        <Text style={styles.big}>{t(language, 'addMedia')}</Text>
        <Text style={styles.sub}>Screenshot, foto of video vanuit je bibliotheek of camera</Text>
        <PrimaryButton label={loading ? t(language, 'processing') : t(language, 'chooseFile')} onPress={handlePick} disabled={loading} />
        {loading ? <ActivityIndicator style={{ marginTop: 12 }} /> : null}
      </View>

      <SectionTitle>{t(language, 'recentProcessed')}</SectionTitle>
      {items.slice(0, 3).map((item) => (
        <View style={styles.recent} key={item.id}>
          <Text style={styles.recentTitle}>{item.title}</Text>
          <Text style={styles.recentMeta}>{item.kind} • {Math.round((item.fileSize ?? 0) / 1024)} KB</Text>
          <TagPill label={item.aiRecognized ? t(language, 'recognized') : 'Manual'} green={item.aiRecognized} />
        </View>
      ))}

      <View style={styles.usageCard}>
        <Text style={styles.usageBadge}>{t(language, 'freePlan')}</Text>
        <Text style={styles.usageText}>{usage ?? 0}/10 {t(language, 'used')}</Text>
        <Text style={styles.usageSub}>{t(language, 'upgradePrompt')}</Text>
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  dropZone: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderStyle: 'dashed',
    borderRadius: 20,
    padding: 22,
    alignItems: 'center'
  },
  camera: { fontSize: 34, marginBottom: 8 },
  big: { color: colors.text, fontWeight: '800', fontSize: 23, marginBottom: 4 },
  sub: { color: colors.textSoft, textAlign: 'center', marginBottom: 16 },
  recent: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    padding: 14,
    marginBottom: 10
  },
  recentTitle: { color: colors.text, fontWeight: '700' },
  recentMeta: { color: colors.textSoft, marginVertical: 6, fontSize: 12 },
  usageCard: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 18,
    padding: 16,
    marginTop: 12
  },
  usageBadge: { color: colors.text, backgroundColor: '#3E8FF7', alignSelf: 'flex-start', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 999, fontSize: 12, fontWeight: '700' },
  usageText: { color: colors.text, fontSize: 30, fontWeight: '800', marginTop: 10 },
  usageSub: { color: colors.textSoft, marginTop: 4 }
});
""",
    "app/folders.tsx": """import { StyleSheet, Text, View } from 'react-native';
import { Screen } from '@/src/components/Screen';
import { AppHeader } from '@/src/components/AppHeader';
import { colors } from '@/src/constants/colors';
import { useMediaStore } from '@/src/store/mediaStore';
import { useSettingsStore } from '@/src/store/settingsStore';
import { t } from '@/src/i18n';

export default function FoldersScreen() {
  const items = useMediaStore((s) => s.items);
  const language = useSettingsStore((s) => s.language);
  const grouped = Object.entries(
    items.reduce<Record<string, number>>((acc, item) => {
      acc[item.folder] = (acc[item.folder] ?? 0) + 1;
      return acc;
    }, {})
  );

  return (
    <Screen>
      <AppHeader title={t(language, 'folders')} subtitle={t(language, 'autoFoldering')} />
      {grouped.map(([name, count]) => (
        <View key={name} style={styles.row}>
          <Text style={styles.icon}>📁</Text>
          <View style={{ flex: 1 }}>
            <Text style={styles.name}>{name}</Text>
            <Text style={styles.sub}>{count} {t(language, 'files')}</Text>
          </View>
        </View>
      ))}
    </Screen>
  );
}

const styles = StyleSheet.create({
  row: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    padding: 14,
    marginBottom: 10,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12
  },
  icon: { fontSize: 24 },
  name: { color: colors.text, fontWeight: '700', fontSize: 18 },
  sub: { color: colors.textSoft, marginTop: 4 }
});
""",
    "app/settings.tsx": """import { Pressable, StyleSheet, Text, View } from 'react-native';
import { useEffect, useState } from 'react';
import { Screen } from '@/src/components/Screen';
import { AppHeader } from '@/src/components/AppHeader';
import { SettingRow } from '@/src/components/SettingRow';
import { colors } from '@/src/constants/colors';
import { useSettingsStore } from '@/src/store/settingsStore';
import { t } from '@/src/i18n';
import { getMonthlyUsage } from '@/src/services/quota';

export default function SettingsScreen() {
  const { aiAutomatic, manualInput, cloudSync, language, patch } = useSettingsStore();
  const [usage, setUsage] = useState(0);

  useEffect(() => { getMonthlyUsage().then(setUsage); }, []);

  return (
    <Screen>
      <AppHeader title={t(language, 'settings')} />
      <View style={styles.planCard}>
        <Text style={styles.badge}>{t(language, 'freePlan')}</Text>
        <Text style={styles.big}>{usage}/10 {t(language, 'used')}</Text>
        <Text style={styles.sub}>{t(language, 'upgradePrompt')}</Text>
        <View style={styles.progressTrack}><View style={[styles.progressBar, { width: `${Math.min((usage / 10) * 100, 100)}%` }]} /></View>
      </View>

      <Text style={styles.section}>HERKENNING</Text>
      <SettingRow title={t(language, 'aiAutomatic')} subtitle="GPT-4o Vision herkent inhoud" value={aiAutomatic} onValueChange={(value) => patch({ aiAutomatic: value })} />
      <SettingRow title={t(language, 'manualInput')} subtitle="Altijd zelf naam opgeven" value={manualInput} onValueChange={(value) => patch({ manualInput: value })} />

      <Text style={styles.section}>OPSLAG</Text>
      <SettingRow title={t(language, 'cloudSync')} subtitle="Google Drive / iCloud later" value={cloudSync} onValueChange={(value) => patch({ cloudSync: value })} />

      <Text style={styles.section}>ACCOUNT</Text>
      <Pressable style={styles.row} onPress={() => patch({ language: language === 'nl' ? 'en' : 'nl' })}>
        <Text style={styles.rowText}>{t(language, 'language')}</Text>
        <Text style={styles.rowRight}>{language === 'nl' ? 'Nederlands' : 'English'} ›</Text>
      </Pressable>

      <View style={styles.row}>
        <Text style={styles.rowText}>{t(language, 'privacyData')}</Text>
        <Text style={styles.rowRight}>›</Text>
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  planCard: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 18,
    padding: 16,
    marginBottom: 16
  },
  badge: { color: colors.text, backgroundColor: '#3E8FF7', alignSelf: 'flex-start', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 999, fontSize: 12, fontWeight: '700' },
  big: { color: colors.text, fontSize: 28, fontWeight: '800', marginTop: 10 },
  sub: { color: colors.textSoft, marginTop: 4 },
  progressTrack: { height: 10, borderRadius: 999, backgroundColor: '#244B79', marginTop: 12, overflow: 'hidden' },
  progressBar: { height: '100%', borderRadius: 999, backgroundColor: colors.accent },
  section: { color: colors.textSoft, fontWeight: '700', fontSize: 12, marginBottom: 10, marginTop: 8 },
  row: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    padding: 16,
    marginBottom: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  rowText: { color: colors.text, fontWeight: '700', fontSize: 16 },
  rowRight: { color: colors.textSoft }
});
""",
    "app/detail/[id].tsx": """import { useLocalSearchParams } from 'expo-router';
import { StyleSheet, Text, View } from 'react-native';
import { Screen } from '@/src/components/Screen';
import { AppHeader } from '@/src/components/AppHeader';
import { TagPill } from '@/src/components/TagPill';
import { colors } from '@/src/constants/colors';
import { useMediaStore } from '@/src/store/mediaStore';
import { useSettingsStore } from '@/src/store/settingsStore';
import { t } from '@/src/i18n';
import { formatShortDate } from '@/src/utils/date';

export default function DetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const getById = useMediaStore((s) => s.getById);
  const language = useSettingsStore((s) => s.language);
  const item = getById(id);

  if (!item) {
    return (
      <Screen>
        <Text style={{ color: 'white' }}>Bestand niet gevonden.</Text>
      </Screen>
    );
  }

  return (
    <Screen>
      <View style={styles.hero}>
        <Text style={styles.emoji}>{item.kind === 'video' ? '🎬' : item.kind === 'screenshot' ? '📄' : '🧾'}</Text>
        <TagPill label={t(language, 'aiRecognized')} green />
      </View>

      <AppHeader title={item.title} />
      <Text style={styles.label}>{t(language, 'tags')}</Text>
      <View style={styles.tagsRow}>{item.tags.map((tag) => <TagPill key={tag} label={tag} />)}</View>

      <Text style={styles.label}>{t(language, 'aiDescription')}</Text>
      <Text style={styles.paragraph}>{item.description}</Text>

      <View style={styles.metaGrid}>
        <View style={styles.metaBlock}>
          <Text style={styles.metaLabel}>{t(language, 'folder')}</Text>
          <Text style={styles.metaValue}>{item.folder}</Text>
        </View>
        <View style={styles.metaBlock}>
          <Text style={styles.metaLabel}>{t(language, 'date')}</Text>
          <Text style={styles.metaValue}>{formatShortDate(item.createdAt, language)}</Text>
        </View>
        <View style={styles.metaBlock}>
          <Text style={styles.metaLabel}>{t(language, 'type')}</Text>
          <Text style={styles.metaValue}>{item.kind}</Text>
        </View>
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  hero: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 18,
    height: 180,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
    marginBottom: 18
  },
  emoji: { fontSize: 48 },
  label: { color: colors.textSoft, fontWeight: '700', fontSize: 12, marginTop: 10, marginBottom: 8 },
  tagsRow: { flexDirection: 'row', flexWrap: 'wrap' },
  paragraph: { color: colors.text, lineHeight: 22, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, borderRadius: 14, padding: 14 },
  metaGrid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', marginTop: 14 },
  metaBlock: { width: '31%', backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, borderRadius: 14, padding: 12 },
  metaLabel: { color: colors.textSoft, fontSize: 11, fontWeight: '700', marginBottom: 6 },
  metaValue: { color: colors.text, fontWeight: '700' }
});
""",
    "app/modal/paywall.tsx": """import { StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Screen } from '@/src/components/Screen';
import { PrimaryButton } from '@/src/components/PrimaryButton';
import { colors } from '@/src/constants/colors';
import { useSettingsStore } from '@/src/store/settingsStore';
import { t } from '@/src/i18n';

export default function PaywallModal() {
  const language = useSettingsStore((s) => s.language);

  return (
    <Screen>
      <View style={styles.card}>
        <Text style={styles.title}>{t(language, 'monthlyLimitReached')}</Text>
        <Text style={styles.sub}>Upgrade later met RevenueCat of native store subscriptions.</Text>
        <View style={styles.feature}><Text style={styles.featureText}>• Onbeperkt verwerken</Text></View>
        <View style={styles.feature}><Text style={styles.featureText}>• Toegang tot batch-verwerking</Text></View>
        <View style={styles.feature}><Text style={styles.featureText}>• Toekomstige cloud sync</Text></View>
        <PrimaryButton label={t(language, 'cancel')} onPress={() => router.back()} />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 18,
    padding: 18,
    marginTop: 60
  },
  title: { color: colors.text, fontWeight: '800', fontSize: 24 },
  sub: { color: colors.textSoft, marginTop: 10, marginBottom: 16 },
  feature: { marginBottom: 8 },
  featureText: { color: colors.text, fontSize: 15 }
});
""",
    "src/constants/colors.ts": """export const colors = {
  bg: '#081D36',
  bgSoft: '#0D2A4D',
  card: '#123760',
  card2: '#163F6F',
  border: '#2C6FB7',
  text: '#F3F7FF',
  textSoft: '#9BB7D5',
  accent: '#4DA1FF',
  success: '#46C167',
  warning: '#E7AE31',
  danger: '#FF6B6B',
  chip: '#1B4677',
  tab: '#0A2341'
};
""",
    "src/constants/limits.ts": """export const FREE_MONTHLY_LIMIT = 10;
""",
    "src/types/media.ts": """export type MediaKind = 'photo' | 'screenshot' | 'video';

export type MediaItem = {
  id: string;
  originalUri: string;
  storedUri: string;
  kind: MediaKind;
  title: string;
  description: string;
  tags: string[];
  folder: string;
  fileSize?: number;
  mimeType?: string;
  createdAt: string;
  updatedAt: string;
  aiRecognized: boolean;
};

export type ProcessedSuggestion = {
  title: string;
  folder: string;
  tags: string[];
  description: string;
  aiRecognized: boolean;
  kind: MediaKind;
};
""",
    "src/types/settings.ts": """export type AppSettings = {
  aiAutomatic: boolean;
  manualInput: boolean;
  cloudSync: boolean;
  language: 'nl' | 'en';
};
""",
    "src/utils/date.ts": """export function formatShortDate(iso: string, locale: 'nl' | 'en' = 'nl') {
  return new Date(iso).toLocaleDateString(locale === 'nl' ? 'nl-NL' : 'en-US', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
}
""",
    "src/utils/file.ts": """import { MediaKind } from '@/src/types/media';

export function detectMediaKind(fileName: string, mimeType?: string | null): MediaKind {
  const lower = `${fileName} ${mimeType ?? ''}`.toLowerCase();
  if (lower.includes('video')) return 'video';
  if (lower.includes('screenshot') || lower.includes('scherm')) return 'screenshot';
  return 'photo';
}
""",
    "src/utils/search.ts": """import { MediaItem } from '@/src/types/media';

export function filterMedia(items: MediaItem[], query: string, selectedFolder: string | null) {
  const q = query.trim().toLowerCase();
  return items.filter((item) => {
    const matchesFolder = selectedFolder ? item.folder === selectedFolder : true;
    if (!matchesFolder) return false;
    if (!q) return true;

    const haystack = [
      item.title,
      item.description,
      item.folder,
      ...item.tags,
      item.kind,
      item.createdAt
    ].join(' ').toLowerCase();

    return haystack.includes(q);
  });
}
""",
    "src/utils/slug.ts": """export function slugify(input: string): string {
  return input
    .normalize('NFD')
    .replace(/[\\u0300-\\u036f]/g, '')
    .replace(/[^a-zA-Z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
    .toLowerCase();
}
""",
    "src/i18n/nl.ts": """export default {
  home: 'Home',
  scan: 'Scannen',
  folders: 'Mappen',
  settings: 'Instellingen',
  searchPlaceholder: 'Zoek bestanden, tags...',
  all: 'Alles',
  addMedia: 'Voeg media toe',
  chooseFile: 'Kies bestand',
  aiRecognized: 'AI herkend',
  recognized: 'AI herkend',
  processing: 'Verwerken...',
  recentProcessed: 'Recent verwerkt',
  used: 'gebruikt',
  freePlan: 'Gratis plan',
  upgradePrompt: 'Upgrade voor onbeperkt gebruik vanaf €2/maand',
  aiAutomatic: 'AI automatisch',
  manualInput: 'Handmatige invoer',
  cloudSync: 'Cloud synchronisatie',
  language: 'Taal',
  privacyData: 'Privacy & data',
  noItems: 'Nog geen bestanden',
  noItemsSub: 'Importeer je eerste screenshot, foto of video.',
  save: 'Opslaan',
  cancel: 'Annuleren',
  fileDetail: 'Detail',
  tags: 'Tags',
  aiDescription: 'AI beschrijving',
  type: 'Type',
  date: 'Datum',
  folder: 'Map',
  openPaywall: 'Upgrade',
  monthlyLimitReached: 'Je gratis limiet is bereikt.',
  monthUsage: 'Deze maand verwerkt',
  files: 'bestanden',
  autoFoldering: 'Automatische mapindeling',
  manualRenameFallback: 'Geen internet? Dan kan handmatige invoer nog steeds.'
} as const;
""",
    "src/i18n/en.ts": """export default {
  home: 'Home',
  scan: 'Scan',
  folders: 'Folders',
  settings: 'Settings',
  searchPlaceholder: 'Search files, tags...',
  all: 'All',
  addMedia: 'Add media',
  chooseFile: 'Choose file',
  aiRecognized: 'AI recognized',
  recognized: 'Recognized',
  processing: 'Processing...',
  recentProcessed: 'Recently processed',
  used: 'used',
  freePlan: 'Free plan',
  upgradePrompt: 'Upgrade for unlimited use from €2/month',
  aiAutomatic: 'AI automatic',
  manualInput: 'Manual input',
  cloudSync: 'Cloud sync',
  language: 'Language',
  privacyData: 'Privacy & data',
  noItems: 'No files yet',
  noItemsSub: 'Import your first screenshot, photo or video.',
  save: 'Save',
  cancel: 'Cancel',
  fileDetail: 'Detail',
  tags: 'Tags',
  aiDescription: 'AI description',
  type: 'Type',
  date: 'Date',
  folder: 'Folder',
  openPaywall: 'Upgrade',
  monthlyLimitReached: 'Your free limit has been reached.',
  monthUsage: 'Processed this month',
  files: 'files',
  autoFoldering: 'Automatic foldering',
  manualRenameFallback: 'No internet? Manual input still works.'
} as const;
""",
    "src/i18n/index.ts": """import nl from './nl';
import en from './en';

export type TranslationKey = keyof typeof nl;
const dictionaries = { nl, en };

export function t(lang: 'nl' | 'en', key: TranslationKey): string {
  return dictionaries[lang][key] ?? key;
}
""",
    "src/db/client.ts": """import * as SQLite from 'expo-sqlite';
export const db = SQLite.openDatabaseSync('scan_name.db');
""",
    "src/db/migrations.ts": """import { db } from './client';

export function runMigrations() {
  db.execSync(`
    CREATE TABLE IF NOT EXISTS media_items (
      id TEXT PRIMARY KEY NOT NULL,
      original_uri TEXT NOT NULL,
      stored_uri TEXT NOT NULL,
      kind TEXT NOT NULL,
      title TEXT NOT NULL,
      description TEXT NOT NULL,
      tags_json TEXT NOT NULL,
      folder TEXT NOT NULL,
      file_size INTEGER,
      mime_type TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      ai_recognized INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS app_settings (
      key TEXT PRIMARY KEY NOT NULL,
      value TEXT NOT NULL
    );
  `);
}
""",
    "src/db/mediaRepo.ts": """import { db } from './client';
import { MediaItem } from '@/src/types/media';

export function getAllMedia(): MediaItem[] {
  const rows = db.getAllSync<any>(`SELECT * FROM media_items ORDER BY datetime(created_at) DESC`);
  return rows.map(mapRow);
}

export function getMediaById(id: string): MediaItem | null {
  const row = db.getFirstSync<any>(`SELECT * FROM media_items WHERE id = ?`, [id]);
  return row ? mapRow(row) : null;
}

export function insertMedia(item: MediaItem) {
  db.runSync(
    `INSERT INTO media_items (
      id, original_uri, stored_uri, kind, title, description, tags_json, folder, file_size, mime_type,
      created_at, updated_at, ai_recognized
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    [
      item.id,
      item.originalUri,
      item.storedUri,
      item.kind,
      item.title,
      item.description,
      JSON.stringify(item.tags),
      item.folder,
      item.fileSize ?? null,
      item.mimeType ?? null,
      item.createdAt,
      item.updatedAt,
      item.aiRecognized ? 1 : 0
    ]
  );
}

function mapRow(row: any): MediaItem {
  return {
    id: row.id,
    originalUri: row.original_uri,
    storedUri: row.stored_uri,
    kind: row.kind,
    title: row.title,
    description: row.description,
    tags: JSON.parse(row.tags_json ?? '[]'),
    folder: row.folder,
    fileSize: row.file_size ?? undefined,
    mimeType: row.mime_type ?? undefined,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
    aiRecognized: Boolean(row.ai_recognized)
  };
}
""",
    "src/db/settingsRepo.ts": """import { db } from './client';
import { AppSettings } from '@/src/types/settings';

const defaults: AppSettings = {
  aiAutomatic: true,
  manualInput: false,
  cloudSync: false,
  language: 'nl'
};

export function getSettings(): AppSettings {
  const rows = db.getAllSync<any>(`SELECT key, value FROM app_settings`);
  if (!rows.length) {
    saveSettings(defaults);
    return defaults;
  }
  const map = Object.fromEntries(rows.map((r) => [r.key, r.value]));
  return {
    aiAutomatic: map.aiAutomatic === 'true',
    manualInput: map.manualInput === 'true',
    cloudSync: map.cloudSync === 'true',
    language: map.language === 'en' ? 'en' : 'nl'
  };
}

export function saveSettings(settings: AppSettings) {
  const entries = Object.entries(settings).map(([key, value]) => [key, String(value)]);
  db.withTransactionSync(() => {
    for (const [key, value] of entries) {
      db.runSync(
        `INSERT INTO app_settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value`,
        [key, value]
      );
    }
  });
}
""",
    "src/services/quota.ts": """import AsyncStorage from '@react-native-async-storage/async-storage';
import { FREE_MONTHLY_LIMIT } from '@/src/constants/limits';

function usageKey() {
  const now = new Date();
  return `usage:${now.getFullYear()}-${now.getMonth() + 1}`;
}

export async function getMonthlyUsage(): Promise<number> {
  const value = await AsyncStorage.getItem(usageKey());
  return Number(value ?? '0');
}

export async function incrementMonthlyUsage(): Promise<number> {
  const current = await getMonthlyUsage();
  const next = current + 1;
  await AsyncStorage.setItem(usageKey(), String(next));
  return next;
}

export async function canProcessMore(): Promise<boolean> {
  const current = await getMonthlyUsage();
  return current < FREE_MONTHLY_LIMIT;
}
""",
    "src/services/ai.ts": """import { detectMediaKind } from '@/src/utils/file';
import { ProcessedSuggestion } from '@/src/types/media';

function mockFromName(name: string): ProcessedSuggestion {
  const lower = name.toLowerCase();

  if (lower.includes('ah') || lower.includes('albert') || lower.includes('receipt') || lower.includes('bon')) {
    return {
      title: 'Bon_AH_€12,40',
      folder: 'Bonnetjes',
      tags: ['bonnetje', 'boodschappen', 'albert heijn'],
      description: 'Kassabon van Albert Heijn, totaalbedrag €12,40. Aankoop van dagelijkse boodschappen.',
      aiRecognized: true,
      kind: 'photo'
    };
  }

  if (lower.includes('invoice') || lower.includes('factuur') || lower.includes('ziggo')) {
    return {
      title: 'Factuur_Ziggo_Feb2026',
      folder: 'Screenshots',
      tags: ['factuur', 'ziggo'],
      description: 'Screenshot of foto van een Ziggo factuur over februari 2026.',
      aiRecognized: true,
      kind: 'screenshot'
    };
  }

  if (lower.includes('todo') || lower.includes('note') || lower.includes('notitie')) {
    return {
      title: 'Handgeschreven_Todo',
      folder: 'Notities',
      tags: ['todo', 'notitie'],
      description: 'Handgeschreven notitie of takenlijst.',
      aiRecognized: true,
      kind: 'photo'
    };
  }

  return {
    title: 'Zonsondergang_Rotterdam',
    folder: "Foto's",
    tags: ['foto'],
    description: 'Algemene foto zonder specifieke documentcontext.',
    aiRecognized: true,
    kind: 'photo'
  };
}

export async function analyzeMedia(fileName: string, mimeType?: string | null): Promise<ProcessedSuggestion> {
  await new Promise((resolve) => setTimeout(resolve, 1200));
  const base = mockFromName(fileName);
  return {
    ...base,
    kind: detectMediaKind(fileName, mimeType)
  };
}
""",
    "src/services/mediaImport.ts": """import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';
import { slugify } from '@/src/utils/slug';

export async function pickMedia() {
  const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
  if (!permission.granted) {
    throw new Error('Geen toestemming voor fotobibliotheek.');
  }

  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ['images', 'videos'],
    quality: 1,
    allowsMultipleSelection: false
  });

  if (result.canceled) return null;
  return result.assets[0];
}

export async function persistImportedFile(uri: string, title: string) {
  const dir = `${FileSystem.documentDirectory}media/`;
  const info = await FileSystem.getInfoAsync(dir);
  if (!info.exists) {
    await FileSystem.makeDirectoryAsync(dir, { intermediates: true });
  }

  const ext = uri.split('.').pop() || 'jpg';
  const fileName = `${slugify(title)}_${Date.now()}.${ext}`;
  const target = `${dir}${fileName}`;
  await FileSystem.copyAsync({ from: uri, to: target });
  return target;
}
""",
    "src/store/settingsStore.ts": """import { create } from 'zustand';
import { AppSettings } from '@/src/types/settings';
import { getSettings, saveSettings } from '@/src/db/settingsRepo';

interface SettingsState extends AppSettings {
  hydrated: boolean;
  hydrate: () => void;
  patch: (patch: Partial<AppSettings>) => void;
}

export const useSettingsStore = create<SettingsState>((set, get) => ({
  hydrated: false,
  aiAutomatic: true,
  manualInput: false,
  cloudSync: false,
  language: 'nl',
  hydrate: () => {
    const settings = getSettings();
    set({ ...settings, hydrated: true });
  },
  patch: (patch) => {
    const next = {
      aiAutomatic: patch.aiAutomatic ?? get().aiAutomatic,
      manualInput: patch.manualInput ?? get().manualInput,
      cloudSync: patch.cloudSync ?? get().cloudSync,
      language: patch.language ?? get().language
    };
    saveSettings(next);
    set(next);
  }
}));
""",
    "src/store/mediaStore.ts": """import { create } from 'zustand';
import { MediaItem } from '@/src/types/media';
import { getAllMedia, getMediaById, insertMedia } from '@/src/db/mediaRepo';

interface MediaState {
  hydrated: boolean;
  items: MediaItem[];
  hydrate: () => void;
  addItem: (item: MediaItem) => void;
  getById: (id: string) => MediaItem | null;
}

export const useMediaStore = create<MediaState>((set) => ({
  hydrated: false,
  items: [],
  hydrate: () => {
    set({ items: getAllMedia(), hydrated: true });
  },
  addItem: (item) => {
    insertMedia(item);
    set({ items: getAllMedia() });
  },
  getById: (id) => getMediaById(id)
}));
""",
    "src/hooks/useHydrateApp.ts": """import { useEffect } from 'react';
import { runMigrations } from '@/src/db/migrations';
import { useMediaStore } from '@/src/store/mediaStore';
import { useSettingsStore } from '@/src/store/settingsStore';

export function useHydrateApp() {
  const hydrateMedia = useMediaStore((s) => s.hydrate);
  const hydrateSettings = useSettingsStore((s) => s.hydrate);

  useEffect(() => {
    runMigrations();
    hydrateSettings();
    hydrateMedia();
  }, [hydrateMedia, hydrateSettings]);
}
""",
    "src/components/Screen.tsx": """import { PropsWithChildren } from 'react';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ScrollView, StyleSheet, View } from 'react-native';
import { colors } from '@/src/constants/colors';

export function Screen({ children, scroll = true }: PropsWithChildren<{ scroll?: boolean }>) {
  const content = <View style={styles.content}>{children}</View>;
  return (
    <SafeAreaView style={styles.safe} edges={['top', 'left', 'right']}>
      {scroll ? <ScrollView contentContainerStyle={styles.scroll}>{content}</ScrollView> : content}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.bg },
  scroll: { paddingBottom: 96 },
  content: { paddingHorizontal: 18, paddingTop: 12 }
});
""",
    "src/components/AppHeader.tsx": """import { StyleSheet, Text, View } from 'react-native';
import { colors } from '@/src/constants/colors';

export function AppHeader({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <View style={styles.wrap}>
      <Text style={styles.title}>{title}</Text>
      {subtitle ? <Text style={styles.subtitle}>{subtitle}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { marginBottom: 16 },
  title: { color: colors.text, fontSize: 32, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 4, fontSize: 14 }
});
""",
    "src/components/PrimaryButton.tsx": """import { Pressable, StyleSheet, Text } from 'react-native';
import { colors } from '@/src/constants/colors';

export function PrimaryButton({ label, onPress, disabled }: { label: string; onPress: () => void; disabled?: boolean }) {
  return (
    <Pressable onPress={onPress} disabled={disabled} style={({ pressed }) => [styles.btn, pressed && styles.pressed, disabled && styles.disabled]}>
      <Text style={styles.label}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  btn: {
    backgroundColor: colors.card2,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    paddingVertical: 14,
    paddingHorizontal: 18,
    alignItems: 'center'
  },
  pressed: { opacity: 0.9 },
  disabled: { opacity: 0.6 },
  label: { color: colors.text, fontWeight: '700', fontSize: 17 }
});
""",
    "src/components/TagPill.tsx": """import { StyleSheet, Text, View } from 'react-native';
import { colors } from '@/src/constants/colors';

export function TagPill({ label, green = false }: { label: string; green?: boolean }) {
  return (
    <View style={[styles.pill, green && styles.green]}>
      <Text style={styles.label}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  pill: {
    backgroundColor: colors.chip,
    borderRadius: 999,
    paddingHorizontal: 10,
    paddingVertical: 6,
    marginRight: 8,
    marginBottom: 8
  },
  green: { backgroundColor: '#1E6C2F' },
  label: { color: colors.text, fontSize: 12, fontWeight: '600' }
});
""",
    "src/components/FileCard.tsx": """import { Pressable, StyleSheet, Text, View } from 'react-native';
import { MediaItem } from '@/src/types/media';
import { colors } from '@/src/constants/colors';
import { TagPill } from './TagPill';
import { formatShortDate } from '@/src/utils/date';

const emojiMap = {
  screenshot: '📸',
  photo: '🌅',
  video: '🎬'
} as const;

export function FileCard({ item, onPress, language }: { item: MediaItem; onPress: () => void; language: 'nl' | 'en' }) {
  return (
    <Pressable style={styles.card} onPress={onPress}>
      <View style={styles.thumb}><Text style={styles.emoji}>{emojiMap[item.kind]}</Text></View>
      <Text style={styles.title} numberOfLines={1}>{item.title}</Text>
      <Text style={styles.meta} numberOfLines={1}>{item.folder} • {formatShortDate(item.createdAt, language)}</Text>
      <View style={styles.row}>
        <TagPill label={item.aiRecognized ? 'AI' : 'Manual'} green={item.aiRecognized} />
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.card,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: colors.border,
    padding: 12,
    width: '48%',
    marginBottom: 12
  },
  thumb: {
    height: 96,
    borderRadius: 12,
    backgroundColor: '#1F4F87',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10
  },
  emoji: { fontSize: 28 },
  title: { color: colors.text, fontWeight: '700', fontSize: 15 },
  meta: { color: colors.textSoft, fontSize: 12, marginTop: 4 },
  row: { flexDirection: 'row', flexWrap: 'wrap', marginTop: 8 }
});
""",
    "src/components/EmptyState.tsx": """import { StyleSheet, Text, View } from 'react-native';
import { colors } from '@/src/constants/colors';

export function EmptyState({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <View style={styles.box}>
      <Text style={styles.emoji}>🗂️</Text>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.subtitle}>{subtitle}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  box: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 18,
    padding: 18,
    alignItems: 'center'
  },
  emoji: { fontSize: 28, marginBottom: 10 },
  title: { color: colors.text, fontWeight: '800', fontSize: 18 },
  subtitle: { color: colors.textSoft, textAlign: 'center', marginTop: 8 }
});
""",
    "src/components/FilterChips.tsx": """import { ScrollView, Pressable, StyleSheet, Text } from 'react-native';
import { colors } from '@/src/constants/colors';

export function FilterChips({ options, selected, onSelect }: { options: string[]; selected: string | null; onSelect: (value: string | null) => void }) {
  return (
    <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.row}>
      {options.map((option) => {
        const active = selected === option || (!selected && option === 'Alles');
        return (
          <Pressable key={option} onPress={() => onSelect(option === 'Alles' ? null : option)} style={[styles.chip, active && styles.active]}>
            <Text style={styles.label}>{option}</Text>
          </Pressable>
        );
      })}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  row: { paddingVertical: 4, marginBottom: 14 },
  chip: {
    backgroundColor: colors.chip,
    paddingHorizontal: 14,
    paddingVertical: 9,
    borderRadius: 999,
    marginRight: 8
  },
  active: { backgroundColor: colors.accent },
  label: { color: colors.text, fontWeight: '600' }
});
""",
    "src/components/SectionTitle.tsx": """import { StyleSheet, Text } from 'react-native';
import { colors } from '@/src/constants/colors';

export function SectionTitle({ children }: { children: string }) {
  return <Text style={styles.title}>{children}</Text>;
}

const styles = StyleSheet.create({
  title: { color: colors.textSoft, fontSize: 13, fontWeight: '700', marginBottom: 10, marginTop: 12, textTransform: 'uppercase' }
});
""",
    "src/components/SettingRow.tsx": """import { StyleSheet, Switch, Text, View } from 'react-native';
import { colors } from '@/src/constants/colors';

export function SettingRow({ title, subtitle, value, onValueChange }: { title: string; subtitle?: string; value?: boolean; onValueChange?: (value: boolean) => void }) {
  return (
    <View style={styles.row}>
      <View style={{ flex: 1 }}>
        <Text style={styles.title}>{title}</Text>
        {subtitle ? <Text style={styles.subtitle}>{subtitle}</Text> : null}
      </View>
      {typeof value === 'boolean' ? (
        <Switch value={value} onValueChange={onValueChange} />
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 14,
    padding: 14,
    marginBottom: 10,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12
  },
  title: { color: colors.text, fontWeight: '700', fontSize: 16 },
  subtitle: { color: colors.textSoft, marginTop: 2, fontSize: 12 }
});
""",
}

ROOT = Path.cwd()

for rel_path, content in FILES.items():
    target = ROOT / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')

print(f"Klaar. {len(FILES)} bestanden aangemaakt in: {ROOT}")
print("Volgende stap:")
print("1) npm install")
print("2) npx expo start -c")
