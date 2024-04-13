import { readPdfText } from 'pdf-text-reader';
import { logger } from '../../utils/logger';

export async function readPDF(filename: string): Promise<string> {
  logger.info(`[parsePDF]: Parsing PDF file: ${filename}`);
  const doc = await readPdfText({ url: filename });
  return doc;
}
