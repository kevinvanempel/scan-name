import { useLocalSearchParams } from 'expo-router';
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
