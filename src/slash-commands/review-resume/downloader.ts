import fs from 'node:fs';
import wretch from 'wretch';
import QueryStringAddon from 'wretch/addons/queryString';
import { z } from 'zod';
import { logger } from '../../utils/logger';

const genericPDFUrl = z.string().url().endsWith('.pdf');
const gDrivePDFUrl = z.string().url().includes('drive.google.com');
export const PDFURL = z.union([genericPDFUrl, gDrivePDFUrl]);
export type PDFURL = z.infer<typeof PDFURL>;

export async function download(url: string, filename: string): Promise<void> {
  if (url.includes('drive.google.com')) {
    const fileId = extractGDriveFileId(url);
    const blob = await downloadFromGDrive(fileId);
    await saveFile(blob, filename);
    return;
  }

  const blob = await downloadGenericPDF(url);
  await saveFile(blob, filename);
}

export function cleanup(filename: string): void {
  logger.info(`[cleanup]: Cleaning up file: ${filename}`);
  fs.rmSync(filename, { force: true });
}

/**
 * Download the public file from Google Drive.
 * Download URL: https://docs.google.com/uc?export=download&confirm=t&id=1<FILE_ID>
 */
async function downloadFromGDrive(id: string): Promise<Blob> {
  logger.info(`[download] Downloading file from Google Drive: ${id}`);
  return wretch('https://docs.google.com/uc').addon(QueryStringAddon).query({ export: 'download', confirm: 't', id: id }).get().blob();
}

/**
 * Extracts the file ID from a Google Drive URL.
 * input format: https://drive.google.com/file/d/<FILE_ID>/view?usp=sharing
 */
export function extractGDriveFileId(url: string): string {
  logger.info(`[extractFileId] Extracting file ID from URL: ${url}`);
  const match = url.match(/\/d\/([^/]+)\//);
  if (!match) {
    logger.info(`[extractFileId] Invalid Drive URL. ${url}`);
    throw new Error('Invalid Drive URL');
  }

  const fileId = match[1];
  logger.info(`[extractFileId] Extracted file ID: ${fileId}`);
  return fileId;
}

/**
 * Download the file from a generic URL.
 */
async function downloadGenericPDF(url: string): Promise<Blob> {
  logger.info(`[download] Downloading file from URL: ${url}`);
  return wretch(url).get().blob();
}

async function saveFile(blob: Blob, filename: string): Promise<void> {
  logger.info(`[saveFile]: Saving file to ${filename}`);
  fs.writeFileSync(filename, Buffer.from(new Uint8Array(await blob.arrayBuffer())));
}
