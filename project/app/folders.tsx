import { StyleSheet, Text, View } from 'react-native';
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
