import type { SlashCommand } from './slash-commands/builder';

import askLLMCommand from './slash-commands/ask-llm/command';
import reviewResumeCommand from './slash-commands/review-resume/command';

export const commands: SlashCommand[] = [askLLMCommand, reviewResumeCommand];
