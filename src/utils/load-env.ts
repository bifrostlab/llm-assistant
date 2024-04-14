import dotenv from 'dotenv';
import { z } from 'zod';
import { logger } from './logger';

const configSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),

  // Discord config
  TOKEN: z.string(),
  CLIENT_ID: z.string(),
  GUILD_ID: z.string().optional(),

  // AI Server URL
  AI_SERVER_URL: z.string().url(),
});
type ConfigSchema = z.infer<typeof configSchema>;

declare global {
  namespace NodeJS {
    interface ProcessEnv extends ConfigSchema {}
  }
}

export function loadEnv(): void {
  dotenv.config();

  const validatedEnv = configSchema.safeParse(process.env);
  if (!validatedEnv.success) {
    logger.error(`Error loading environment details. ${validatedEnv.error.message}`);
    throw new Error('INVALID CONFIG!', { cause: validatedEnv.error.issues });
  }
}
