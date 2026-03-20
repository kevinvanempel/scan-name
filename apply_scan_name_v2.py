from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parent

FILES = {
    "app/review.tsx": r"""
import { useState } from 'react';
import { Alert } from 'react-native';
import { router } from 'expo-router';
import { Screen } from '../src/components/Screen';
import { AppHeader } from '../src/components/AppHeader';
import { MediaPreview } from '../src/components/MediaPreview';
import { FormField } from '../src/components/FormField';
import { PrimaryButton } from '../src/components/PrimaryButton';
import { persistImportedFile } from '../src/services/mediaImport';
import { useDraftStore } from '../src/store/draftStore';
import { useMediaStore } from '../src/store/mediaStore';
import { MediaItem } from '../src/types/media';

export default function ReviewScreen() {
  const { asset, suggestion, clearDraft } = useDraftStore();
  const addItem = useMediaStore((s) => s.addItem);
  const [title, setTitle] = useState(suggestion?.title ?? '');
  const [folder, setFolder] = useState(suggestion?.folder ?? 'Overig');
  const [tags, setTags] = useState((suggestion?.tags ?? []).join(', '));
  const [description, setDescription] = useState(suggestion?.description ?? '');

  if (!asset || !suggestion) {
    router.replace('/scan');
    return null;
  }

  async function handleSave() {
    try {
      const storedUri = await persistImportedFile(asset.uri, title);
      const now = new Date().toISOString();

      const item: MediaItem = {
        id: `${Date.now()}`,
        originalUri: asset.uri,
        storedUri,
        kind: suggestion.kind,
        title,
        description,
        tags: tags.split(',').map((x) => x.trim()).filter(Boolean),
        folder,
        fileSize: asset.fileSize,
        mimeType: asset.mimeType ?? undefined,
        createdAt: now,
        updatedAt: now,
        aiRecognized: suggestion.aiRecognized
      };

      addItem(item);
      clearDraft();
      router.replace(`/detail/${item.id}`);
    } catch (error: any) {
      Alert.alert('Fout', error?.message ?? 'Opslaan mislukt');
    }
  }

  return (
    <Screen>
      <AppHeader title="Controleren" subtitle="Pas naam, tags en map aan voor opslaan" />
      <MediaPreview uri={asset.uri} />
      <FormField label="Bestandsnaam" value={title} onChangeText={setTitle} />
      <FormField label="Map" value={folder} onChangeText={setFolder} />
      <FormField label="Tags (komma gescheiden)" value={tags} onChangeText={setTags} />
      <FormField label="Beschrijving" value={description} onChangeText={setDescription} multiline />
      <PrimaryButton label="Opslaan" onPress={handleSave} />
    </Screen>
  );
}
""",
    "app/auth.tsx": r"""
import { useState } from 'react';
import { Alert } from 'react-native';
import { Screen } from '../src/components/Screen';
import { AppHeader } from '../src/components/AppHeader';
import { FormField } from '../src/components/FormField';
import { PrimaryButton } from '../src/components/PrimaryButton';
import { useAuthStore } from '../src/store/authStore';

export default function AuthScreen() {
  const [email, setEmail] = useState('');
  const signIn = useAuthStore((s) => s.signIn);

  async function handleMagicLink() {
    try {
      await signIn(email);
      Alert.alert('Gelukt', 'Check je e-mail voor de magic link.');
    } catch (error: any) {
      Alert.alert('Fout', error?.message ?? 'Inloggen mislukt');
    }
  }

  return (
    <Screen>
      <AppHeader title="Inloggen" subtitle="Magic link via e-mail" />
      <FormField label="E-mail" value={email} onChangeText={setEmail} />
      <PrimaryButton label="Verstuur magic link" onPress={handleMagicLink} />
    </Screen>
  );
}
""",
    "src/store/draftStore.ts": r"""
import { create } from 'zustand';
import { ProcessedSuggestion } from '../types/media';

type PickedAsset = {
  uri: string;
  fileName?: string | null;
  fileSize?: number;
  mimeType?: string | null;
};

type DraftState = {
  asset: PickedAsset | null;
  suggestion: ProcessedSuggestion | null;
  setDraft: (asset: PickedAsset, suggestion: ProcessedSuggestion) => void;
  clearDraft: () => void;
};

export const useDraftStore = create<DraftState>((set) => ({
  asset: null,
  suggestion: null,
  setDraft: (asset, suggestion) => set({ asset, suggestion }),
  clearDraft: () => set({ asset: null, suggestion: null })
}));
""",
    "src/store/authStore.ts": r"""
import { create } from 'zustand';
import { supabase } from '../services/supabase';

type AuthState = {
  userEmail: string | null;
  signIn: (email: string) => Promise<void>;
  signOut: () => Promise<void>;
  hydrate: () => Promise<void>;
};

export const useAuthStore = create<AuthState>((set) => ({
  userEmail: null,
  signIn: async (email) => {
    const { error } = await supabase.auth.signInWithOtp({ email });
    if (error) throw error;
    set({ userEmail: email });
  },
  signOut: async () => {
    await supabase.auth.signOut();
    set({ userEmail: null });
  },
  hydrate: async () => {
    const { data } = await supabase.auth.getUser();
    set({ userEmail: data.user?.email ?? null });
  }
}));
""",
    "src/services/api.ts": r"""
export const API_BASE_URL = 'http://192.168.154.203:8787';
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
""",
    "src/services/cameraImport.ts": r"""
import { CameraView, useCameraPermissions } from 'expo-camera';
export { CameraView, useCameraPermissions };
""",
    "src/services/supabase.ts": r"""
import 'react-native-url-polyfill/auto';
import { createClient } from '@supabase/supabase-js';

export const supabase = createClient(
  'https://YOUR_PROJECT.supabase.co',
  'YOUR_SUPABASE_ANON_KEY'
);
""",
    "src/services/subscription.ts": r"""
export async function openSubscriptionFlow() {
  return { ok: true };
}
""",
    "src/components/FormField.tsx": r"""
import { StyleSheet, Text, TextInput, View } from 'react-native';
import { colors } from '../constants/colors';

export function FormField({
  label,
  value,
  onChangeText,
  multiline = false
}: {
  label: string;
  value: string;
  onChangeText: (value: string) => void;
  multiline?: boolean;
}) {
  return (
    <View style={styles.wrap}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        value={value}
        onChangeText={onChangeText}
        multiline={multiline}
        style={[styles.input, multiline && styles.multiline]}
        placeholderTextColor={colors.textSoft}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { marginBottom: 12 },
  label: { color: colors.textSoft, fontWeight: '700', fontSize: 12, marginBottom: 8 },
  input: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 14,
    color: colors.text,
    paddingHorizontal: 14,
    paddingVertical: 12
  },
  multiline: {
    minHeight: 110,
    textAlignVertical: 'top'
  }
});
""",
    "src/components/MediaPreview.tsx": r"""
import { Image, StyleSheet, View } from 'react-native';
import { colors } from '../constants/colors';

export function MediaPreview({ uri }: { uri: string }) {
  return (
    <View style={styles.frame}>
      <Image source={{ uri }} style={styles.image} resizeMode="cover" />
    </View>
  );
}

const styles = StyleSheet.create({
  frame: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 18,
    overflow: 'hidden',
    height: 220,
    marginBottom: 18
  },
  image: { width: '100%', height: '100%' }
});
""",
    "backend/package.json": r"""
{
  "name": "scan-name-backend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "node --watch src/server.ts",
    "start": "node src/server.ts"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.19.2",
    "multer": "^1.4.5-lts.1",
    "openai": "^4.104.0",
    "zod": "^3.23.8"
  }
}
""",
    "backend/.env.example": r"""
OPENAI_API_KEY=your_openai_api_key_here
PORT=8787
""",
    "backend/src/prompts.ts": r"""
export const SYSTEM_PROMPT = `
Je bent een bestands-organisatie assistent voor een mobiele app.
Analyseer de afbeelding en geef ALLEEN JSON terug.

Vereist JSON-formaat:
{
  "title": "korte_bestandsnaam_zonder_extensie",
  "folder": "Bonnetjes | Screenshots | Notities | Foto's | Video's | Overig",
  "tags": ["tag1", "tag2"],
  "description": "korte duidelijke samenvatting in het Nederlands",
  "aiRecognized": true,
  "kind": "photo | screenshot | video"
}

Regels:
- bestandsnaam kort, bruikbaar en duidelijk
- geen markdown
- geen extra uitleg
- max 5 tags
- als het een kassabon is, noem winkel en bedrag als zichtbaar
- als het een screenshot van factuur is, noem merk/bedrijf en periode indien zichtbaar
`;
""",
    "backend/src/schema.ts": r"""
import { z } from 'zod';

export const SuggestionSchema = z.object({
  title: z.string().min(1),
  folder: z.string().min(1),
  tags: z.array(z.string()).default([]),
  description: z.string().min(1),
  aiRecognized: z.boolean(),
  kind: z.enum(['photo', 'screenshot', 'video'])
});
""",
    "backend/src/openai.ts": r"""
import OpenAI from 'openai';
import { SYSTEM_PROMPT } from './prompts.js';
import { SuggestionSchema } from './schema.js';

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function analyzeImage(base64: string, mimeType: string) {
  const response = await client.responses.create({
    model: 'gpt-4.1-mini',
    input: [
      {
        role: 'system',
        content: [{ type: 'input_text', text: SYSTEM_PROMPT }]
      },
      {
        role: 'user',
        content: [
          { type: 'input_text', text: 'Analyseer dit bestand en geef JSON terug.' },
          {
            type: 'input_image',
            image_url: `data:${mimeType};base64,${base64}`
          }
        ]
      }
    ]
  });

  const text = response.output_text;
  const parsed = JSON.parse(text);
  return SuggestionSchema.parse(parsed);
}
""",
    "backend/src/server.ts": r"""
import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import multer from 'multer';
import fs from 'fs';
import { analyzeImage } from './openai.js';

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(cors());
app.use(express.json({ limit: '20mb' }));

app.get('/health', (_req, res) => {
  res.json({ ok: true });
});

app.post('/analyze', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).send('Bestand ontbreekt');
    }

    const buffer = fs.readFileSync(req.file.path);
    const base64 = buffer.toString('base64');
    const mimeType = req.file.mimetype || 'image/jpeg';

    const result = await analyzeImage(base64, mimeType);
    fs.unlinkSync(req.file.path);
    res.json(result);
  } catch (error: any) {
    console.error(error);
    res.status(500).send(error?.message ?? 'AI analyse mislukt');
  }
});

const port = Number(process.env.PORT || 8787);
app.listen(port, '0.0.0.0', () => {
  console.log(`Scan & Name backend draait op poort ${port}`);
});
""",
}

LAYOUT_CONTENT = r"""
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
    </Tabs>
  );
}
"""

SCAN_CONTENT = r"""
import { useState } from 'react';
import { Alert, ActivityIndicator, StyleSheet, Text, View } from 'react-native';
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
"""

PACKAGE_UPDATES = {
    "@supabase/supabase-js": "^2.49.8",
    "expo-camera": "~16.1.11",
    "react-hook-form": "^7.54.2",
    "react-native-url-polyfill": "^2.0.0",
}

def write_file(relative_path: str, content: str):
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print(f"[ok] geschreven: {relative_path}")

def update_package_json():
    import json
    path = ROOT / "package.json"
    if not path.exists():
        print("[skip] package.json niet gevonden")
        return

    data = json.loads(path.read_text(encoding="utf-8"))
    deps = data.setdefault("dependencies", {})
    for name, version in PACKAGE_UPDATES.items():
        deps[name] = version

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("[ok] package.json bijgewerkt")

def main():
    if not (ROOT / "app").exists() or not (ROOT / "src").exists():
        raise SystemExit("Dit script moet in de root van je Scan & Name project staan.")

    for rel, content in FILES.items():
        write_file(rel, content)

    write_file("app/_layout.tsx", LAYOUT_CONTENT)
    write_file("app/scan.tsx", SCAN_CONTENT)
    update_package_json()

    print("\nKlaar.")
    print("Voer nu uit:\n")
    print("  npm install")
    print("  npx expo start -c")
    print("\nVoor de backend:\n")
    print("  cd backend")
    print("  npm install")
    print("  copy .env.example .env")
    print("  npm run dev")

if __name__ == "__main__":
    main()