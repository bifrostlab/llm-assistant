import path from 'node:path';

export function getOutputFileName(userId: string): string {
  return path.resolve(__dirname, 'resumes', `resume-${userId}.pdf`);
}
