import { create } from 'zustand';
import { MediaItem } from '@/src/types/media';
import { getAllMedia, getMediaById, insertMedia } from '@/src/db/mediaRepo';

interface MediaState {
  hydrated: boolean;
  items: MediaItem[];
  hydrate: () => void;
  addItem: (item: MediaItem) => void;
  getById: (id: string) => MediaItem | null;
}

export const useMediaStore = create<MediaState>((set) => ({
  hydrated: false,
  items: [],
  hydrate: () => {
    set({ items: getAllMedia(), hydrated: true });
  },
  addItem: (item) => {
    insertMedia(item);
    set({ items: getAllMedia() });
  },
  getById: (id) => getMediaById(id)
}));
