import { db } from './client';

export function runMigrations() {
  db.execSync(`
    CREATE TABLE IF NOT EXISTS media_items (
      id TEXT PRIMARY KEY NOT NULL,
      original_uri TEXT NOT NULL,
      stored_uri TEXT NOT NULL,
      kind TEXT NOT NULL,
      title TEXT NOT NULL,
      description TEXT NOT NULL,
      tags_json TEXT NOT NULL,
      folder TEXT NOT NULL,
      file_size INTEGER,
      mime_type TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      ai_recognized INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS app_settings (
      key TEXT PRIMARY KEY NOT NULL,
      value TEXT NOT NULL
    );
  `);
}
