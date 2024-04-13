import { faker } from '@faker-js/faker';
import type { ChatInputCommandInteraction } from 'discord.js';
import type { OpenAI } from 'openai';
import type { ChatCompletion } from 'openai/resources/chat/completions';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { captor, mockDeep, mockReset } from 'vitest-mock-extended';
import { getClient } from '../../llm/client';
import { execute } from './command';

const mockChatInputInteraction = mockDeep<ChatInputCommandInteraction>();

const mockChatCompletions = vi.fn();
vi.mock('../../llm/client');
const mockGetClient = vi.mocked(getClient);
mockGetClient.mockReturnValue({
  chat: {
    completions: {
      create: mockChatCompletions,
    },
  },
} as unknown as OpenAI);

describe('ask command', () => {
  describe('execute', () => {
    beforeEach(() => {
      mockReset(mockChatInputInteraction);
    });

    it('Should respond with error if model is invalid', async () => {
      mockChatInputInteraction.options.getString.mockImplementation((param) => {
        switch (param) {
          case 'model':
            return 'invalidmodel';

          case 'question':
            return 'asdf1234';

          default:
            throw new Error('Invalid');
        }
      });
      const respondInput = captor<Parameters<ChatInputCommandInteraction['reply']>['0']>();

      await execute(mockChatInputInteraction);

      expect(mockChatInputInteraction.reply).toBeCalledWith(respondInput);
      expect(respondInput.value).toContain('Invalid model');
    });

    it('Should respond with error if there is an error asking the LLM', async () => {
      mockChatInputInteraction.options.getString.mockImplementation((param) => {
        switch (param) {
          case 'model':
            return 'tinydolphin';

          case 'question':
            return 'asdf1234';

          default:
            throw new Error('Invalid');
        }
      });
      mockChatCompletions.mockRejectedValueOnce(new Error('Synthetic Error.'));
      const respondInput = captor<Parameters<ChatInputCommandInteraction['reply']>['0']>();

      await execute(mockChatInputInteraction);

      expect(mockChatInputInteraction.reply).toBeCalledWith(respondInput);
      expect(respondInput.value).toContain('Error in asking the LLM');
    });

    it('Should respond with no response if there is no response', async () => {
      mockChatInputInteraction.options.getString.mockImplementation((param) => {
        switch (param) {
          case 'model':
            return 'tinydolphin';

          case 'question':
            return 'asdf1234';

          default:
            throw new Error('Invalid');
        }
      });
      mockChatCompletions.mockResolvedValueOnce({
        id: faker.string.uuid(),
        created: faker.number.int(),
        model: 'tinydolphin',
        object: 'chat.completion',
        choices: [
          {
            finish_reason: 'stop',
            index: 0,
            logprobs: null,
            message: {
              content: null,
            },
          },
        ] as ChatCompletion.Choice[],
      });
      const respondInput = captor<Parameters<ChatInputCommandInteraction['reply']>['0']>();

      await execute(mockChatInputInteraction);

      expect(mockChatInputInteraction.reply).toBeCalledWith(respondInput);
      expect(respondInput.value).toContain('No response');
    });

    it('Should respond with the LLM response', async () => {
      mockChatInputInteraction.options.getString.mockImplementation((param) => {
        switch (param) {
          case 'model':
            return 'tinydolphin';

          case 'question':
            return 'asdf1234';

          default:
            throw new Error('Invalid');
        }
      });
      const mockAnswer = faker.lorem.sentence();
      mockChatCompletions.mockResolvedValueOnce({
        id: faker.string.uuid(),
        created: faker.number.int(),
        model: 'tinydolphin',
        object: 'chat.completion',
        choices: [
          {
            finish_reason: 'stop',
            index: 0,
            logprobs: null,
            message: {
              content: mockAnswer,
            },
          },
        ] as ChatCompletion.Choice[],
      });
      const respondInput = captor<Parameters<ChatInputCommandInteraction['reply']>['0']>();

      await execute(mockChatInputInteraction);

      expect(mockChatInputInteraction.reply).toBeCalledWith(respondInput);
      expect(respondInput.value).toContain(`Q: asdf1234\nA: ${mockAnswer}`);
    });
  });
});
