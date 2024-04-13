import { faker } from '@faker-js/faker';
import type { ChatInputCommandInteraction } from 'discord.js';
import type { OpenAI } from 'openai';
import type { ChatCompletion } from 'openai/resources/chat/completions';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { captor, mockDeep, mockReset } from 'vitest-mock-extended';
import { getClient } from '../../llm/client';
import { execute } from './command';
import * as reader from './reader';

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

const readerSpy = vi.spyOn(reader, 'readPDF');

describe('review resume command', () => {
  describe('execute', () => {
    beforeEach(() => {
      mockReset(mockChatInputInteraction);
    });

    it('Should respond with error if model is invalid', async () => {
      mockChatInputInteraction.options.getString.mockImplementation((param) => {
        switch (param) {
          case 'model':
            return 'invalidmodel';

          case 'url':
            return 'https://example.com/dummy.pdf';

          default:
            throw new Error('Invalid');
        }
      });
      const respondInput = captor<Parameters<ChatInputCommandInteraction['reply']>['0']>();

      await execute(mockChatInputInteraction);

      expect(mockChatInputInteraction.reply).toBeCalledWith(respondInput);
      expect(respondInput.value).toContain('Invalid model');
    });

    it('Should respond with error if URL is invalid', async () => {
      mockChatInputInteraction.options.getString.mockImplementation((param) => {
        switch (param) {
          case 'model':
            return 'tinydolphin';

          case 'url':
            return 'https://example.com';

          default:
            throw new Error('Invalid');
        }
      });
      const respondInput = captor<Parameters<ChatInputCommandInteraction['reply']>['0']>();

      await execute(mockChatInputInteraction);

      expect(mockChatInputInteraction.reply).toBeCalledWith(respondInput);
      expect(respondInput.value).toContain('Invalid URL');
    });

    it('Should respond with error with invalid Google Drive URL', async () => {
      mockChatInputInteraction.options.getString.mockImplementation((param) => {
        switch (param) {
          case 'model':
            return 'tinydolphin';

          case 'url':
            return 'https://drive.google.com';

          default:
            throw new Error('Invalid');
        }
      });
      const respondInput = captor<Parameters<ChatInputCommandInteraction['reply']>['0']>();

      await execute(mockChatInputInteraction);

      expect(mockChatInputInteraction.reply).toBeCalledWith(respondInput);
      expect(respondInput.value).toContain('Error downloading resume');
    });

    it('Should respond with error if there is an error downloading the file', async () => {
      mockChatInputInteraction.options.getString.mockImplementation((param) => {
        switch (param) {
          case 'model':
            return 'tinydolphin';

          case 'url':
            return 'https://example.com/invalid.pdf';

          default:
            throw new Error('Invalid');
        }
      });
      const respondInput = captor<Parameters<ChatInputCommandInteraction['reply']>['0']>();

      await execute(mockChatInputInteraction);

      expect(mockChatInputInteraction.reply).toBeCalledWith(respondInput);
      expect(respondInput.value).toContain('Error downloading resume');
    });

    it('Should respond with error if there is an error reading the file', async () => {
      mockChatInputInteraction.options.getString.mockImplementation((param) => {
        switch (param) {
          case 'model':
            return 'tinydolphin';

          case 'url':
            return 'https://example.com/dummy.pdf';

          default:
            throw new Error('Invalid');
        }
      });
      readerSpy.mockRejectedValueOnce(new Error('Synthetic Error.'));
      const respondInput = captor<Parameters<ChatInputCommandInteraction['reply']>['0']>();

      await execute(mockChatInputInteraction);

      expect(mockChatInputInteraction.reply).toBeCalledWith(respondInput);
      expect(respondInput.value).toContain('Error reading resume');
    });

    it('Should respond with error if there is an error asking the LLM', async () => {
      mockChatInputInteraction.options.getString.mockImplementation((param) => {
        switch (param) {
          case 'model':
            return 'tinydolphin';

          case 'url':
            return 'https://example.com/dummy.pdf';

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

          case 'url':
            return 'https://example.com/dummy.pdf';

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

    it('Should respond with the LLM response if it can download from Google Drive', async () => {
      mockChatInputInteraction.options.getString.mockImplementation((param) => {
        switch (param) {
          case 'model':
            return 'tinydolphin';

          case 'url':
            return `https://drive.google.com/file/d/${faker.string.alphanumeric()}/view?usp=sharing`;

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
      expect(respondInput.value).toContain(`${mockAnswer}`);
    });

    it('Should respond with the LLM response if it can download from regular URL', async () => {
      mockChatInputInteraction.options.getString.mockImplementation((param) => {
        switch (param) {
          case 'model':
            return 'tinydolphin';

          case 'url':
            return 'https://example.com/dummy.pdf';

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
      expect(respondInput.value).toContain(`${mockAnswer}`);
    });
  });
});
