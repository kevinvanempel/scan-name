import { useEffect } from 'react';
import { runMigrations } from '@/src/db/migrations';
import { useMediaStore } from '@/src/store/mediaStore';
import { useSettingsStore } from '@/src/store/settingsStore';

export function useHydrateApp() {
  const hydrateMedia = useMediaStore((s) => s.hydrate);
  const hydrateSettings = useSettingsStore((s) => s.hydrate);

  useEffect(() => {
    runMigrations();
    hydrateSettings();
    hydrateMedia();
  }, [hydrateMedia, hydrateSettings]);
}
