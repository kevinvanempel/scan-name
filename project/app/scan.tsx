import { useState } from 'react';
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
