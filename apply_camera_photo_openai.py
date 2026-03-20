from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parent

FILES = {
    "app/camera.tsx": r"""
import { useRef, useState } from 'react';
import { Alert, Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { Screen } from '../src/components/Screen';
import { AppHeader } from '../src/components/AppHeader';
import { colors } from '../src/constants/colors';
import { analyzeMediaInCloud } from '../src/services/openaiCloud';
import { useDraftStore } from '../src/store/draftStore';
import { incrementMonthlyUsage } from '../src/services/quota';

export default function CameraScreen() {
  const cameraRef = useRef<CameraView | null>(null);
  const [permission, requestPermission] = useCameraPermissions();
  const [isBusy, setIsBusy] = useState(false);
  const setDraft = useDraftStore((s) => s.setDraft);

  async function handleTakePhoto() {
    try {
      if (!cameraRef.current || isBusy) return;
      setIsBusy(true);

      const photo = await cameraRef.current.takePictureAsync({
        quality: 0.9,
        imageType: 'jpg'
      });

      if (!photo?.uri) {
        throw new Error('Er is geen foto gemaakt.');
      }

      const suggestion = await analyzeMediaInCloud({
        uri: photo.uri,
        fileName: `camera_${Date.now()}.jpg`,
        mimeType: 'image/jpeg'
      });

      setDraft(
        {
          uri: photo.uri,
          fileName: `camera_${Date.now()}.jpg`,
          fileSize: undefined,
          mimeType: 'image/jpeg'
        },
        suggestion
      );

      await incrementMonthlyUsage();
      router.replace('/review');
    } catch (error: any) {
      Alert.alert('Fout', error?.message ?? 'Foto maken of analyseren mislukt');
    } finally {
      setIsBusy(false);
    }
  }

  if (!permission) {
    return (
      <Screen>
        <AppHeader title="Camera" subtitle="Camera rechten laden..." />
      </Screen>
    );
  }

  if (!permission.granted) {
    return (
      <Screen>
        <AppHeader title="Camera" subtitle="Toegang nodig tot je camera" />
        <Pressable style={styles.button} onPress={requestPermission}>
          <Text style={styles.buttonText}>Geef camera toegang</Text>
        </Pressable>
      </Screen>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.top}>
        <Text style={styles.title}>Maak een foto</Text>
        <Text style={styles.subtitle}>De foto wordt direct door AI geanalyseerd</Text>
      </View>

      <CameraView
        ref={cameraRef}
        style={styles.camera}
        facing="back"
        mode="picture"
      />

      <View style={styles.bottomBar}>
        <Pressable style={[styles.captureButton, isBusy && styles.captureDisabled]} onPress={handleTakePhoto}>
          <Text style={styles.captureText}>{isBusy ? 'Bezig...' : 'Foto maken'}</Text>
        </Pressable>

        <Pressable style={styles.secondaryButton} onPress={() => router.back()}>
          <Text style={styles.secondaryText}>Terug</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.bg
  },
  top: {
    paddingTop: 60,
    paddingHorizontal: 18,
    paddingBottom: 12
  },
  title: {
    color: colors.text,
    fontSize: 28,
    fontWeight: '800'
  },
  subtitle: {
    color: colors.textSoft,
    marginTop: 4
  },
  camera: {
    flex: 1,
    marginHorizontal: 18,
    borderRadius: 18,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: colors.border
  },
  bottomBar: {
    padding: 18,
    gap: 12
  },
  button: {
    backgroundColor: colors.card2,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    paddingVertical: 14,
    alignItems: 'center'
  },
  buttonText: {
    color: colors.text,
    fontWeight: '700',
    fontSize: 16
  },
  captureButton: {
    backgroundColor: colors.accent,
    borderRadius: 999,
    paddingVertical: 16,
    alignItems: 'center'
  },
  captureDisabled: {
    opacity: 0.7
  },
  captureText: {
    color: '#fff',
    fontWeight: '800',
    fontSize: 18
  },
  secondaryButton: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    paddingVertical: 14,
    alignItems: 'center'
  },
  secondaryText: {
    color: colors.text,
    fontWeight: '700'
  }
});
""",
    "app/scan.tsx": r"""
import { useState } from 'react';
import { Alert, ActivityIndicator, Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Screen } from '../src/components/Screen';
import { AppHeader } from '../src/components/AppHeader';
import { PrimaryButton } from '../src/components/PrimaryButton';
import { SectionTitle } from '../src/components/SectionTitle';
import { TagPill } from '../src/components/TagPill';
import { colors } from '../src/constants/colors';
import { t } from '../src/i18n';
import { useSettingsStore } from '../src/store/settingsStore';
import { useMediaStore } from '../src/store/mediaStore';
import { pickMedia } from '../src/services/mediaImport';
import { analyzeMediaInCloud } from '../src/services/openaiCloud';
import { canProcessMore, getMonthlyUsage, incrementMonthlyUsage } from '../src/services/quota';
import { useDraftStore } from '../src/store/draftStore';

export default function ScanScreen() {
  const language = useSettingsStore((s) => s.language);
  const items = useMediaStore((s) => s.items);
  const setDraft = useDraftStore((s) => s.setDraft);
  const [loading, setLoading] = useState(false);
  const [usage, setUsage] = useState<number | null>(null);

  async function ensureAllowed() {
    const allowed = await canProcessMore();
    const currentUsage = await getMonthlyUsage();
    setUsage(currentUsage);

    if (!allowed) {
      router.push('/modal/paywall');
      return false;
    }
    return true;
  }

  async function handlePick() {
    const allowed = await ensureAllowed();
    if (!allowed) return;

    try {
      setLoading(true);
      const asset = await pickMedia();
      if (!asset) return;

      const suggestion = await analyzeMediaInCloud({
        uri: asset.uri,
        fileName: asset.fileName,
        mimeType: asset.mimeType
      });

      setDraft(
        {
          uri: asset.uri,
          fileName: asset.fileName,
          fileSize: asset.fileSize,
          mimeType: asset.mimeType
        },
        suggestion
      );

      await incrementMonthlyUsage();
      router.push('/review');
    } catch (error: any) {
      Alert.alert('Fout', error?.message ?? 'Import mislukt');
    } finally {
      setLoading(false);
      const after = await getMonthlyUsage();
      setUsage(after);
    }
  }

  async function handleOpenCamera() {
    const allowed = await ensureAllowed();
    if (!allowed) return;
    router.push('/camera');
  }

  return (
    <Screen>
      <AppHeader title={t(language, 'scan')} subtitle="Kies uit galerij of maak direct een foto" />

      <View style={styles.dropZone}>
        <Text style={styles.camera}>📷</Text>
        <Text style={styles.big}>{t(language, 'addMedia')}</Text>
        <Text style={styles.sub}>Galerij of directe camera-opname met AI analyse</Text>

        <PrimaryButton
          label={loading ? t(language, 'processing') : t(language, 'chooseFile')}
          onPress={handlePick}
          disabled={loading}
        />

        <Pressable style={styles.secondaryButton} onPress={handleOpenCamera}>
          <Text style={styles.secondaryText}>Foto maken</Text>
        </Pressable>

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
  secondaryButton: {
    marginTop: 12,
    backgroundColor: colors.card2,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    paddingVertical: 14,
    paddingHorizontal: 24
  },
  secondaryText: {
    color: colors.text,
    fontWeight: '700',
    fontSize: 16
  },
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
    "app/_layout.tsx": r"""
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
      <Tabs.Screen name="modal/paywall" options={{ href: null, presentation: 'modal' }} />
      <Tabs.Screen name="review" options={{ href: null }} />
      <Tabs.Screen name="auth" options={{ href: null }} />
      <Tabs.Screen name="camera" options={{ href: null }} />
    </Tabs>
  );
}
""",
    "src/services/openaiCloud.ts": r"""
import { API_BASE_URL } from './api';
import { ProcessedSuggestion } from '../types/media';

export async function analyzeMediaInCloud(params: {
  uri: string;
  fileName?: string | null;
  mimeType?: string | null;
}): Promise<ProcessedSuggestion> {
  const form = new FormData();
  form.append('file', {
    uri: params.uri,
    name: params.fileName ?? 'upload.jpg',
    type: params.mimeType ?? 'image/jpeg'
  } as any);

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    body: form,
    headers: {
      Accept: 'application/json'
    }
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'Cloud AI analyse mislukt');
  }

  return response.json();
}
"""
}

def write_file(rel_path: str, content: str):
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print(f"[ok] {rel_path}")

def main():
    if not (ROOT / "app").exists() or not (ROOT / "src").exists():
        raise SystemExit("Run dit script in de root van scan-name-mvp.")

    for rel, content in FILES.items():
        write_file(rel, content)

    print("\nKlaar.")
    print("Voer nu uit:")
    print("  npx expo install expo-camera")
    print("  npx expo start -c")

if __name__ == "__main__":
    main()