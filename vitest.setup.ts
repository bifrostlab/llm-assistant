import { afterAll, afterEach, beforeAll } from 'vitest';
import { server } from './mocks/server';
import { logger } from './src/utils/logger';

beforeAll(() => {
  logger.silent = true;
  server.listen();
});

afterEach(() => {
  server.resetHandlers();
});

afterAll(() => {
  logger.silent = false;
  server.close();
});
