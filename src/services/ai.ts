import { detectMediaKind } from '../../src/utils/file';
import { ProcessedSuggestion } from '../../src/types/media';

function mockFromName(name: string): ProcessedSuggestion {
  const lower = name.toLowerCase();

  if (lower.includes('ah') || lower.includes('albert') || lower.includes('receipt') || lower.includes('bon')) {
    return {
      title: 'Bon_AH_€12,40',
      folder: 'Bonnetjes',
      tags: ['bonnetje', 'boodschappen', 'albert heijn'],
      description: 'Kassabon van Albert Heijn, totaalbedrag €12,40. Aankoop van dagelijkse boodschappen.',
      aiRecognized: true,
      kind: 'photo'
    };
  }

  if (lower.includes('invoice') || lower.includes('factuur') || lower.includes('ziggo')) {
    return {
      title: 'Factuur_Ziggo_Feb2026',
      folder: 'Screenshots',
      tags: ['factuur', 'ziggo'],
      description: 'Screenshot of foto van een Ziggo factuur over februari 2026.',
      aiRecognized: true,
      kind: 'screenshot'
    };
  }

  if (lower.includes('todo') || lower.includes('note') || lower.includes('notitie')) {
    return {
      title: 'Handgeschreven_Todo',
      folder: 'Notities',
      tags: ['todo', 'notitie'],
      description: 'Handgeschreven notitie of takenlijst.',
      aiRecognized: true,
      kind: 'photo'
    };
  }

  return {
    title: 'Zonsondergang_Rotterdam',
    folder: "Foto's",
    tags: ['foto'],
    description: 'Algemene foto zonder specifieke documentcontext.',
    aiRecognized: true,
    kind: 'photo'
  };
}

export async function analyzeMedia(fileName: string, mimeType?: string | null): Promise<ProcessedSuggestion> {
  await new Promise((resolve) => setTimeout(resolve, 1200));
  const base = mockFromName(fileName);
  return {
    ...base,
    kind: detectMediaKind(fileName, mimeType)
  };
}
