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
    } catch { }

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