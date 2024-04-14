import { SlashCommandBuilder } from 'discord.js';
import { Result } from 'oxide.ts';
import { selectModelAutocomplete } from '../../autocompletes/select-model/autocomplete';
import { askQuestion, findModel } from '../../llm/utils';
import { logger } from '../../utils/logger';
import type { SlashCommand, SlashCommandHandler } from '../builder';

const data = new SlashCommandBuilder()
  .setName('ask')
  .setDescription('Ask an LLM to answer anything')
  .addStringOption((option) => option.setName('model').setDescription('Choose an LLM model').setRequired(true).setAutocomplete(true))
  .addStringOption((option) => option.setName('question').setDescription('Enter your prompt').setRequired(true).setMinLength(10));

export const execute: SlashCommandHandler = async (interaction) => {
  const model = interaction.options.getString('model', true).trim().toLowerCase();
  const question = interaction.options.getString('question', true).trim();
  logger.info(`[ask]: Asking ${model} model with prompt: ${question}`);

  const findModelOp = Result.safe(() => findModel(model));
  if (findModelOp.isErr()) {
    logger.info(`[ask]: Invalid model ${model}`);
    interaction.reply('Invalid model. Please choose from the available models.');
    return;
  }
  const supportedModel = findModelOp.unwrap();

  const answers = await askQuestion(supportedModel, question);
  logger.info('[ask]: Got response from LLM', data);
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
