import { db } from './client';
import { AppSettings } from '@/src/types/settings';

const defaults: AppSettings = {
  aiAutomatic: true,
  manualInput: false,
  cloudSync: false,
  language: 'nl'
};

export function getSettings(): AppSettings {
  const rows = db.getAllSync<any>(`SELECT key, value FROM app_settings`);
  if (!rows.length) {
    saveSettings(defaults);
    return defaults;
  }
  const map = Object.fromEntries(rows.map((r) => [r.key, r.value]));
  return {
    aiAutomatic: map.aiAutomatic === 'true',
    manualInput: map.manualInput === 'true',
    cloudSync: map.cloudSync === 'true',
    language: map.language === 'en' ? 'en' : 'nl'
  };
}

export function saveSettings(settings: AppSettings) {
  const entries = Object.entries(settings).map(([key, value]) => [key, String(value)]);
  db.withTransactionSync(() => {
    for (const [key, value] of entries) {
      db.runSync(
        `INSERT INTO app_settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value`,
        [key, value]
      );
    }
  });
}
