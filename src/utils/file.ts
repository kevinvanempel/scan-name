import { MediaKind } from '../../src/types/media';

export function detectMediaKind(fileName: string, mimeType?: string | null): MediaKind {
  const lower = `${fileName} ${mimeType ?? ''}`.toLowerCase();
  if (lower.includes('video')) return 'video';
  if (lower.includes('screenshot') || lower.includes('scherm')) return 'screenshot';
  return 'photo';
}
