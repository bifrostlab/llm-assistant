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
  .addStringOption((option) => option.setName('model').setDescription('Choose an LLM model').setRequired(false).setAutocomplete(true))
  .addStringOption((option) => option.setName('url').setDescription('PDF or Google Drive URL').setRequired(true));

export const execute: SlashCommandHandler = async (interaction) => {
  await interaction.deferReply();
  const model = (interaction.options.getString('model', false) || process.env.DEFAULT_MODEL).trim().toLowerCase();
  const url = interaction.options.getString('url', true);
  logger.info(`[review-resume]: Reviewing resume from URL: ${url}`);

  const findModelOp = Result.safe(() => findModel(model));
  if (findModelOp.isErr()) {
    logger.info(`[ask]: Invalid model ${model}`);
    interaction.editReply('Invalid model. Please choose from the available models.');
    return;
  }
  const supportedModel = findModelOp.unwrap();

  const validURL = PDFURL.safeParse(url);
  if (!validURL.success) {
    logger.info(`[review-resume]: Invalid URL ${url}`);
    await interaction.editReply('Invalid URL. The URL must end with `.pdf` or must be valid Google Drive URL.');
    return;
  }

  const filename = getOutputFileName(interaction.user.id);
  const downloadOp = await Result.safe(download(url, filename));
  if (downloadOp.isErr()) {
    logger.error(`[review-resume]: Error downloading file: ${downloadOp.unwrapErr().message}`);
    cleanup(filename);
    await interaction.editReply('Error downloading resume. Please try again later.');
    return;
  }

  const readOp = await Result.safe(readPDF(filename));
  if (readOp.isErr()) {
    logger.error(`[review-resume]: Error reading file: ${readOp.unwrapErr().message}`);
    cleanup(filename);
    await interaction.editReply('Error reading resume. Please try again later.');
    return;
  }

  const doc = readOp.unwrap();
  cleanup(filename);

  const question = `You are a resume reviewer. Your tasks are:
- Show sentences with incorrect grammars, and suggest a way to correct them.
- Provide suggestions to improve the resume:

${doc}
`;
  logger.info('[review-resume]: Sending review resume request to LLM.');
  const answers = await askQuestion(supportedModel, question, false);

  logger.info('[review-resume]: Got response from LLM. Sending to client', answers);
  const [firstChunk, ...chunks] = answers;
  await interaction.editReply(firstChunk);
  for await (const chunk of chunks) {
    interaction.followUp(chunk);
  }
};

const command: SlashCommand = {
  data,
  execute,
  autocomplete: selectModelAutocomplete,
};

export default command;
