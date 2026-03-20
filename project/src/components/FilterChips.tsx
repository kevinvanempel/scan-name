import { ScrollView, Pressable, StyleSheet, Text } from 'react-native';
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
