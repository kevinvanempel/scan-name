import { create } from 'zustand';
import { ProcessedSuggestion } from '../types/media';

type PickedAsset = {
  uri: string;
  fileName?: string | null;
  fileSize?: number;
  mimeType?: string | null;
};

type DraftState = {
  asset: PickedAsset | null;
  suggestion: ProcessedSuggestion | null;
  setDraft: (asset: PickedAsset, suggestion: ProcessedSuggestion) => void;
  clearDraft: () => void;
};

export const useDraftStore = create<DraftState>((set) => ({
  asset: null,
  suggestion: null,
  setDraft: (asset, suggestion) => set({ asset, suggestion }),
  clearDraft: () => set({ asset: null, suggestion: null })
}));
