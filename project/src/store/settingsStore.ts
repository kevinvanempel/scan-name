import { create } from 'zustand';
import { AppSettings } from '@/src/types/settings';
import { getSettings, saveSettings } from '@/src/db/settingsRepo';

interface SettingsState extends AppSettings {
  hydrated: boolean;
  hydrate: () => void;
  patch: (patch: Partial<AppSettings>) => void;
}

export const useSettingsStore = create<SettingsState>((set, get) => ({
  hydrated: false,
  aiAutomatic: true,
  manualInput: false,
  cloudSync: false,
  language: 'nl',
  hydrate: () => {
    const settings = getSettings();
    set({ ...settings, hydrated: true });
  },
  patch: (patch) => {
    const next = {
      aiAutomatic: patch.aiAutomatic ?? get().aiAutomatic,
      manualInput: patch.manualInput ?? get().manualInput,
      cloudSync: patch.cloudSync ?? get().cloudSync,
      language: patch.language ?? get().language
    };
    saveSettings(next);
    set(next);
  }
}));
