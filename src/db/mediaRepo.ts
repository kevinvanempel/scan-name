import { db } from './client';
import { MediaItem } from '../../src/types/media';

export function getAllMedia(): MediaItem[] {
  const rows = db.getAllSync<any>(`SELECT * FROM media_items ORDER BY datetime(created_at) DESC`);
  return rows.map(mapRow);
}

export function getMediaById(id: string): MediaItem | null {
  const row = db.getFirstSync<any>(`SELECT * FROM media_items WHERE id = ?`, [id]);
  return row ? mapRow(row) : null;
}

export function insertMedia(item: MediaItem) {
  db.runSync(
    `INSERT INTO media_items (
      id, original_uri, stored_uri, kind, title, description, tags_json, folder, file_size, mime_type,
      created_at, updated_at, ai_recognized
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    [
      item.id,
      item.originalUri,
      item.storedUri,
      item.kind,
      item.title,
      item.description,
      JSON.stringify(item.tags),
      item.folder,
      item.fileSize ?? null,
      item.mimeType ?? null,
      item.createdAt,
      item.updatedAt,
      item.aiRecognized ? 1 : 0
    ]
  );
}

function mapRow(row: any): MediaItem {
  return {
    id: row.id,
    originalUri: row.original_uri,
    storedUri: row.stored_uri,
    kind: row.kind,
    title: row.title,
    description: row.description,
    tags: JSON.parse(row.tags_json ?? '[]'),
    folder: row.folder,
    fileSize: row.file_size ?? undefined,
    mimeType: row.mime_type ?? undefined,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
    aiRecognized: Boolean(row.ai_recognized)
  };
}
