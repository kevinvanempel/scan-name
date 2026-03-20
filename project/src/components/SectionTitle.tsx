import { StyleSheet, Text } from 'react-native';
import { colors } from '@/src/constants/colors';

export function SectionTitle({ children }: { children: string }) {
  return <Text style={styles.title}>{children}</Text>;
}

const styles = StyleSheet.create({
  title: { color: colors.textSoft, fontSize: 13, fontWeight: '700', marginBottom: 10, marginTop: 12, textTransform: 'uppercase' }
});
