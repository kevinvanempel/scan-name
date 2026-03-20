import { useState } from 'react';
import { Alert } from 'react-native';
import { router } from 'expo-router';
import { Screen } from '../src/components/Screen';
import { AppHeader } from '../src/components/AppHeader';
import { MediaPreview } from '../src/components/MediaPreview';
import { FormField } from '../src/components/FormField';
import { PrimaryButton } from '../src/components/PrimaryButton';
import { persistImportedFile } from '../src/services/mediaImport';
import { useDraftStore } from '../src/store/draftStore';
import { useMediaStore } from '../src/store/mediaStore';
import { MediaItem } from '../src/types/media';

export default function ReviewScreen() {
  const { asset, suggestion, clearDraft } = useDraftStore();
  const addItem = useMediaStore((s) => s.addItem);
  const [title, setTitle] = useState(suggestion?.title ?? '');
  const [folder, setFolder] = useState(suggestion?.folder ?? 'Overig');
  const [tags, setTags] = useState((suggestion?.tags ?? []).join(', '));
  const [description, setDescription] = useState(suggestion?.description ?? '');

  if (!asset || !suggestion) {
    router.replace('/scan');
    return null;
  }

  async function handleSave() {
    try {
      const storedUri = await persistImportedFile(asset.uri, title);
      const now = new Date().toISOString();

      const item: MediaItem = {
        id: `${Date.now()}`,
        originalUri: asset.uri,
        storedUri,
        kind: suggestion.kind,
        title,
        description,
        tags: tags.split(',').map((x) => x.trim()).filter(Boolean),
        folder,
        fileSize: asset.fileSize,
        mimeType: asset.mimeType ?? undefined,
        createdAt: now,
        updatedAt: now,
        aiRecognized: suggestion.aiRecognized
      };

      addItem(item);
      clearDraft();
      router.replace(`/detail/${item.id}`);
    } catch (error: any) {
      Alert.alert('Fout', error?.message ?? 'Opslaan mislukt');
    }
  }

  return (
    <Screen>
      <AppHeader title="Controleren" subtitle="Pas naam, tags en map aan voor opslaan" />
      <MediaPreview uri={asset.uri} />
      <FormField label="Bestandsnaam" value={title} onChangeText={setTitle} />
      <FormField label="Map" value={folder} onChangeText={setFolder} />
      <FormField label="Tags (komma gescheiden)" value={tags} onChangeText={setTags} />
      <FormField label="Beschrijving" value={description} onChangeText={setDescription} multiline />
      <PrimaryButton label="Opslaan" onPress={handleSave} />
    </Screen>
  );
}
