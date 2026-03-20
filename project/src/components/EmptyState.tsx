import { StyleSheet, Text, View } from 'react-native';
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
