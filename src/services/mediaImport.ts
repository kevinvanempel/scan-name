import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';
import { slugify } from '../../src/utils/slug';

export async function pickMedia() {
  const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
  if (!permission.granted) {
    throw new Error('Geen toestemming voor fotobibliotheek.');
  }

  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ['images', 'videos'],
    quality: 1,
    allowsMultipleSelection: false
  });

  if (result.canceled) return null;
  return result.assets[0];
}

export async function persistImportedFile(uri: string, title: string) {
  const dir = `${FileSystem.documentDirectory}media/`;
  const info = await FileSystem.getInfoAsync(dir);
  if (!info.exists) {
    await FileSystem.makeDirectoryAsync(dir, { intermediates: true });
  }

  const ext = uri.split('.').pop() || 'jpg';
  const fileName = `${slugify(title)}_${Date.now()}.${ext}`;
  const target = `${dir}${fileName}`;
  await FileSystem.copyAsync({ from: uri, to: target });
  return target;
}
