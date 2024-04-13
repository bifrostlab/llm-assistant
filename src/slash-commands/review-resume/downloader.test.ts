import { faker } from '@faker-js/faker';
import { describe, expect, it } from 'vitest';
import { extractGDriveFileId } from './downloader';

describe('PDF Downloader test', () => {
  describe('Extract Google Drive File ID', () => {
    it('should extract the file ID from a Google Drive URL', () => {
      const fileId = faker.string.alphanumeric();
      const url = `https://drive.google.com/file/d/${fileId}/view?usp=sharing`;
      const output = extractGDriveFileId(url);
      expect(output).toBe(fileId);
    });
  });
});
