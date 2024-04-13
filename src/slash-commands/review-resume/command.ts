import { SlashCommandBuilder } from 'discord.js';
import { Result } from 'oxide.ts';
import { selectModelAutocomplete } from '../../autocompletes/select-model/autocomplete';
import { askQuestion, findModel } from '../../llm/utils';
import { logger } from '../../utils/logger';
import type { SlashCommand, SlashCommandHandler } from '../builder';
import { PDFURL, cleanup, download } from './downloader';
import { readPDF } from './reader';
import { getOutputFileName } from './utils';

const data = new SlashCommandBuilder()
  .setName('review-resume')
  .setDescription('Review a resume from a generic PDF URL or Google Drive')
  .addStringOption((option) => option.setName('model').setDescription('Choose an LLM model').setRequired(true).setAutocomplete(true))
  .addStringOption((option) => option.setName('url').setDescription('PDF or Google Drive URL').setRequired(true));

export const execute: SlashCommandHandler = async (interaction) => {
  const model = interaction.options.getString('model', true).trim().toLowerCase();
  const url = interaction.options.getString('url', true);
  logger.info(`[review-resume]: Reviewing resume from URL: ${url}`);

  const findModelOp = Result.safe(() => findModel(model));
  if (findModelOp.isErr()) {
    logger.info(`[ask]: Invalid model ${model}`);
    interaction.reply('Invalid model. Please choose from the available models.');
    return;
  }
  const supportedModel = findModelOp.unwrap();

  const validURL = PDFURL.safeParse(url);
  if (!validURL.success) {
    logger.info(`[review-resume]: Invalid URL ${url}`);
    await interaction.reply('Invalid URL. The URL must end with `.pdf` or must be valid Google Drive URL.');
    return;
  }

  const filename = getOutputFileName(interaction.user.id);
  const downloadOp = await Result.safe(download(url, filename));
  if (downloadOp.isErr()) {
    logger.error(`[review-resume]: Error downloading file: ${downloadOp.unwrapErr().message}`);
    cleanup(filename);
    await interaction.reply('Error downloading resume. Please try again later.');
    return;
  }

  const readOp = await Result.safe(readPDF(filename));
  if (readOp.isErr()) {
    logger.error(`[review-resume]: Error reading file: ${readOp.unwrapErr().message}`);
    cleanup(filename);
    await interaction.reply('Error reading resume. Please try again later.');
    return;
  }

  const doc = readOp.unwrap();
  cleanup(filename);

  const question = `You are a resume reviewer. Your tasks are:
- Show sentences with incorrect grammars, and suggest a way to correct them.
- Provide suggestions to improve the resume:

${doc}
`;
  const answers = await askQuestion(supportedModel, question, false);
  logger.info('[review-resume]: Got response from LLM', data);
  await answers.reduce(async (accum, chunk) => {
    await accum;
    await interaction.reply(chunk);
    return undefined;
  }, Promise.resolve(undefined));
};

const command: SlashCommand = {
  data,
  execute,
  autocomplete: selectModelAutocomplete,
};

export default command;
