import OpenAI from 'openai';
import { SYSTEM_PROMPT } from './prompts.js';
import { SuggestionSchema } from './schema.js';

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function analyzeImage(base64, mimeType) {
  const response = await client.responses.create({
    model: 'gpt-4.1-mini',
    input: [
      {
        role: 'system',
        content: [{ type: 'input_text', text: SYSTEM_PROMPT }]
      },
      {
        role: 'user',
        content: [
          { type: 'input_text', text: 'Analyseer dit bestand en geef JSON terug.' },
          {
            type: 'input_image',
            image_url: `data:${mimeType};base64,${base64}`
          }
        ]
      }
    ]
  });

  const text = response.output_text;
  const parsed = JSON.parse(text);
  return SuggestionSchema.parse(parsed);
}
