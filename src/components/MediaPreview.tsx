import { Image, StyleSheet, View } from 'react-native';
import { colors } from '../constants/colors';

export function MediaPreview({ uri }: { uri: string }) {
  return (
    <View style={styles.frame}>
      <Image source={{ uri }} style={styles.image} resizeMode="cover" />
    </View>
  );
}

const styles = StyleSheet.create({
  frame: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 18,
    overflow: 'hidden',
    height: 220,
    marginBottom: 18
  },
  image: { width: '100%', height: '100%' }
});
