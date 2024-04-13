import { Result } from 'oxide.ts';
import { askQuestion } from '../src/llm/utils';
import { logger } from '../src/utils/logger';

async function ask(): Promise<void> {
  const response = await Result.safe(askQuestion('tinydolphin', 'What is the capital of Australia?'));
  if (response.isErr()) {
    logger.error(response.unwrapErr());
  }

  const data = response.unwrap();
  logger.info(data);
}

ask();
