import fs from 'node:fs';
import path from 'node:path';
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('https://example.com/dummy.pdf', () => {
    const buffer = fs.readFileSync(path.resolve(__dirname, 'dummy.pdf'));
    return HttpResponse.arrayBuffer(buffer, {
      headers: {
        'Content-Type': 'application/pdf;qs=0.001',
      },
    });
  }),

  http.get('https://example.com/invalid.pdf', () => {
    return new HttpResponse(null, { status: 404, statusText: 'Not Found' });
  }),

  http.get('https://docs.google.com/uc', ({ request }) => {
    const url = new URL(request.url);
    const id = url.searchParams.get('id');
    if (!id) {
      return new HttpResponse(null, { status: 400, statusText: 'Bad Request' });
    }

    const buffer = fs.readFileSync(path.resolve(__dirname, 'dummy.pdf'));
    return HttpResponse.arrayBuffer(buffer, {
      headers: {
        'Content-Type': 'application/octet-stream',
      },
    });
  }),
];
