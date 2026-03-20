import { StyleSheet, Text, View } from 'react-native';
import { colors } from '../../src/constants/colors';

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
