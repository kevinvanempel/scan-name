import { useMemo, useState } from 'react';
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
