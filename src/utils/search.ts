import { MediaItem } from '../../src/types/media';

export function filterMedia(items: MediaItem[], query: string, selectedFolder: string | null) {
  const q = query.trim().toLowerCase();
  return items.filter((item) => {
    const matchesFolder = selectedFolder ? item.folder === selectedFolder : true;
    if (!matchesFolder) return false;
    if (!q) return true;

    const haystack = [
      item.title,
      item.description,
      item.folder,
      ...item.tags,
      item.kind,
      item.createdAt
    ].join(' ').toLowerCase();

    return haystack.includes(q);
  });
}
