import { API_BASE_URL } from './api';
import { ProcessedSuggestion } from '../types/media';

export async function analyzeMediaInCloud(params: {
  uri: string;
  fileName?: string | null;
  mimeType?: string | null;
}): Promise<ProcessedSuggestion> {
  const form = new FormData();
  form.append('file', {
    uri: params.uri,
    name: params.fileName ?? 'upload.jpg',
    type: params.mimeType ?? 'image/jpeg'
  } as any);

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    body: form,
    headers: {
      Accept: 'application/json'
    }
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'Cloud AI analyse mislukt');
  }

  return response.json();
}
