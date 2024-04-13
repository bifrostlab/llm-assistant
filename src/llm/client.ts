import 'openai/shims/web';

import { OpenAI } from 'openai';

let client: OpenAI | null = null;

export function getClient(): OpenAI {
  if (!client) {
    client = new OpenAI({
      baseURL: process.env.AI_SERVER_URL,
      apiKey: 'FAKE',
    });
  }

  return client;
}
