import { z } from 'zod';

export const SuggestionSchema = z.object({
  title: z.string().min(1),
  folder: z.string().min(1),
  tags: z.array(z.string()).default([]),
  description: z.string().min(1),
  aiRecognized: z.boolean(),
  kind: z.enum(['photo', 'screenshot', 'video'])
});
