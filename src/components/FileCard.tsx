import { Pressable, StyleSheet, Text, View } from 'react-native';
import { MediaItem } from '../../src/types/media';
import { colors } from '../../src/constants/colors';
import { TagPill } from './TagPill';
import { formatShortDate } from '../../src/utils/date';

const emojiMap = {
  screenshot: '📸',
  photo: '🌅',
  video: '🎬'
} as const;

export function FileCard({ item, onPress, language }: { item: MediaItem; onPress: () => void; language: 'nl' | 'en' }) {
  return (
    <Pressable style={styles.card} onPress={onPress}>
      <View style={styles.thumb}><Text style={styles.emoji}>{emojiMap[item.kind]}</Text></View>
      <Text style={styles.title} numberOfLines={1}>{item.title}</Text>
      <Text style={styles.meta} numberOfLines={1}>{item.folder} • {formatShortDate(item.createdAt, language)}</Text>
      <View style={styles.row}>
        <TagPill label={item.aiRecognized ? 'AI' : 'Manual'} green={item.aiRecognized} />
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.card,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: colors.border,
    padding: 12,
    width: '48%',
    marginBottom: 12
  },
  thumb: {
    height: 96,
    borderRadius: 12,
    backgroundColor: '#1F4F87',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10
  },
  emoji: { fontSize: 28 },
  title: { color: colors.text, fontWeight: '700', fontSize: 15 },
  meta: { color: colors.textSoft, fontSize: 12, marginTop: 4 },
  row: { flexDirection: 'row', flexWrap: 'wrap', marginTop: 8 }
});
