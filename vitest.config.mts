import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    coverage: {
      enabled: true,
      provider: 'v8',
      include: ['src'],
    },
  },
});
