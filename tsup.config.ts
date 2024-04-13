import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['bin/index.ts'],
  outDir: 'dist',
  format: ['cjs', 'esm'],
  dts: true,
  sourcemap: true,
});
