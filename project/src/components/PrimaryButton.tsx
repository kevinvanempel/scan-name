import { Pressable, StyleSheet, Text } from 'react-native';
import { colors } from '@/src/constants/colors';

export function PrimaryButton({ label, onPress, disabled }: { label: string; onPress: () => void; disabled?: boolean }) {
  return (
    <Pressable onPress={onPress} disabled={disabled} style={({ pressed }) => [styles.btn, pressed && styles.pressed, disabled && styles.disabled]}>
      <Text style={styles.label}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  btn: {
    backgroundColor: colors.card2,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    paddingVertical: 14,
    paddingHorizontal: 18,
    alignItems: 'center'
  },
  pressed: { opacity: 0.9 },
  disabled: { opacity: 0.6 },
  label: { color: colors.text, fontWeight: '700', fontSize: 17 }
});
