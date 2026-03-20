export type MediaKind = 'photo' | 'screenshot' | 'video';

export type MediaItem = {
  id: string;
  originalUri: string;
  storedUri: string;
  kind: MediaKind;
  title: string;
  description: string;
  tags: string[];
  folder: string;
  fileSize?: number;
  mimeType?: string;
  createdAt: string;
  updatedAt: string;
  aiRecognized: boolean;
};

export type ProcessedSuggestion = {
  title: string;
  folder: string;
  tags: string[];
  description: string;
  aiRecognized: boolean;
  kind: MediaKind;
};
