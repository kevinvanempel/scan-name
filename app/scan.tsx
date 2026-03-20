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
