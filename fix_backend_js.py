from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

FILES = {
    "src/prompts.js": r"""
export const SYSTEM_PROMPT = `
Je bent een bestands-organisatie assistent voor een mobiele app.
Analyseer de afbeelding en geef ALLEEN JSON terug.

Vereist JSON-formaat:
{
  "title": "korte_bestandsnaam_zonder_extensie",
  "folder": "Bonnetjes | Screenshots | Notities | Foto's | Video's | Overig",
  "tags": ["tag1", "tag2"],
  "description": "korte duidelijke samenvatting in het Nederlands",
  "aiRecognized": true,
  "kind": "photo | screenshot | video"
}

Regels:
- bestandsnaam kort, bruikbaar en duidelijk
- geen markdown
- geen extra uitleg
- max 5 tags
- als het een kassabon is, noem winkel en bedrag als zichtbaar
- als het een screenshot van factuur is, noem merk/bedrijf en periode indien zichtbaar
`;
""",
    "src/schema.js": r"""
import { z } from 'zod';

export const SuggestionSchema = z.object({
  title: z.string().min(1),
  folder: z.string().min(1),
  tags: z.array(z.string()).default([]),
  description: z.string().min(1),
  aiRecognized: z.boolean(),
  kind: z.enum(['photo', 'screenshot', 'video'])
});
""",
    "src/openai.js": r"""
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
""",
    "src/server.js": r"""
import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import multer from 'multer';
import fs from 'fs';
import { analyzeImage } from './openai.js';

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(cors());
app.use(express.json({ limit: '20mb' }));

app.get('/health', (_req, res) => {
  res.json({ ok: true });
});

app.post('/analyze', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).send('Bestand ontbreekt');
    }

    const buffer = fs.readFileSync(req.file.path);
    const base64 = buffer.toString('base64');
    const mimeType = req.file.mimetype || 'image/jpeg';

    const result = await analyzeImage(base64, mimeType);

    try {
      fs.unlinkSync(req.file.path);
    } catch {}

    res.json(result);
  } catch (error) {
    console.error(error);
    res.status(500).send(error?.message ?? 'AI analyse mislukt');
  }
});

const port = Number(process.env.PORT || 8787);
app.listen(port, '0.0.0.0', () => {
  console.log(`Scan & Name backend draait op poort ${port}`);
});
"""
}

PACKAGE_JSON = r"""
{
  "name": "scan-name-backend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "node --watch src/server.js",
    "start": "node src/server.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.19.2",
    "multer": "^1.4.5-lts.1",
    "openai": "^4.104.0",
    "zod": "^3.23.8"
  }
}
"""

def write_file(rel_path: str, content: str):
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip(), encoding="utf-8")
    print(f"[ok] {rel_path}")

def remove_if_exists(rel_path: str):
    path = ROOT / rel_path
    if path.exists():
        path.unlink()
        print(f"[removed] {rel_path}")

def main():
    for rel_path, content in FILES.items():
        write_file(rel_path, content)

    (ROOT / "package.json").write_text(PACKAGE_JSON.lstrip(), encoding="utf-8")
    print("[ok] package.json bijgewerkt")

    remove_if_exists("src/server.ts")
    remove_if_exists("src/openai.ts")
    remove_if_exists("src/prompts.ts")
    remove_if_exists("src/schema.ts")

    print("\nKlaar.")
    print("Voer nu uit:")
    print("  npm install")
    print("  npm run dev")

if __name__ == "__main__":
    main()