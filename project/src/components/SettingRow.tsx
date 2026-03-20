import { StyleSheet, Switch, Text, View } from 'react-native';
import { colors } from '@/src/constants/colors';

export function SettingRow({ title, subtitle, value, onValueChange }: { title: string; subtitle?: string; value?: boolean; onValueChange?: (value: boolean) => void }) {
  return (
    <View style={styles.row}>
      <View style={{ flex: 1 }}>
        <Text style={styles.title}>{title}</Text>
        {subtitle ? <Text style={styles.subtitle}>{subtitle}</Text> : null}
      </View>
      {typeof value === 'boolean' ? (
        <Switch value={value} onValueChange={onValueChange} />
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 14,
    padding: 14,
    marginBottom: 10,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12
  },
  title: { color: colors.text, fontWeight: '700', fontSize: 16 },
  subtitle: { color: colors.textSoft, marginTop: 2, fontSize: 12 }
});
